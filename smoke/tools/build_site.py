"""Build the Smoke Signals demo site from a batch output folder.

Usage:
  python -I build_site.py --batch output/<batch> --maps output/<maps>/maps
         [--clips <folder with <smoke_id>.mp4>] [--inventory smoke/inventory.csv]
         [--out site] [--colors "H-SR=#F5C542,RESIN=#5DADE2,PN=#B388FF"]

The site is static: plain HTML, CSS and a little JavaScript, no server.
"""
import argparse
import csv
import html
import json
import math
import os
import shutil
from collections import Counter, defaultdict

TEAMS = ["H-SR", "RESIN", "PN"]
MATCH_SECONDS = 20 * 60
NATIVE = 768


def esc(s):
    return html.escape(str(s if s is not None else ""))


def parse_colors(text):
    colors = {"H-SR": "#F5C542", "RESIN": "#5DADE2", "PN": "#B388FF"}
    for part in (text or "").split(","):
        if "=" in part:
            k, v = part.split("=", 1)
            colors[k.strip()] = v.strip()
    return colors


def clock_remaining_seconds(clock):
    if not clock or ":" not in clock:
        return None
    m, s = clock.split(":")
    return int(m) * 60 + int(s)


def fmt_int(v):
    return f"{int(round(v)):,}" if v is not None else "-"


def fmt_km(m):
    return "-" if m is None else f"{m / 1000:.1f} km"


class Data:
    def __init__(self, batch, maps_dir, clips_dir, inventory):
        self.batch = batch
        self.smokes = json.load(open(os.path.join(batch, "smokes.json"), encoding="utf-8"))
        self.jobs = json.load(open(os.path.join(batch, "jobs.json"), encoding="utf-8"))
        self.job_by_key = {(j["match_id"], j["game_no"], j["team"]): j for j in self.jobs}
        self.games = {}
        self.damage_by_team_game = defaultdict(float)
        for j in self.jobs:
            gdir = os.path.join(batch, "games", j["name"])
            gpath = os.path.join(gdir, "game.json")
            if not os.path.exists(gpath):
                continue
            g = json.load(open(gpath, encoding="utf-8"))
            key = (j["match_id"], j["game_no"])
            self.games.setdefault(key, g)
            spath = os.path.join(gdir, "damage_spike.json")
            if os.path.exists(spath):
                spike = json.load(open(spath, encoding="utf-8"))
                owner_team = {str(p["entity_id"]): t["name"] for t in g["teams"] for p in t["players"]}
                for ent, dmg in spike.get("damage_by_attacker", {}).items():
                    if owner_team.get(ent) == j["team"]:
                        self.damage_by_team_game[(j["team"], key)] += dmg
        self.inventory = {}
        if inventory and os.path.exists(inventory):
            for r in csv.DictReader(open(inventory, encoding="utf-8")):
                self.inventory[(r["match_id"], int(r["game_no"]))] = r
        self.maps = {}
        self.maps_dir = maps_dir
        for m in json.load(open(os.path.join(maps_dir, "maps.json"), encoding="utf-8")):
            self.maps[m["map"]] = m
        self.clips_dir = clips_dir
        self.clip_files = {}
        if clips_dir and os.path.isdir(clips_dir):
            for f in os.listdir(clips_dir):
                if f.endswith(".mp4"):
                    self.clip_files[f.rsplit(".", 1)[0]] = os.path.join(clips_dir, f)
        for s in self.smokes:
            s["_match"] = s["match_id"].split("_")[-1]
            s["_key"] = (s["_match"], s["game_no"])
            s["_job"] = self.job_by_key.get((s["_match"], s["game_no"], s["team"]))
            s["_act_s"] = (s.get("t_activate") or s["t_created"])["seconds"]
            s["_act_clock"] = (s.get("t_activate") or s["t_created"]).get("clock") or ""
            cap = s.get("t_capture") or {}
            s["_cap_clock"] = cap.get("clock") or ""
            disp = s.get("t_dispersed") or {}
            s["_duration"] = (disp["seconds"] - s["_act_s"]) if disp else None
            st_a, st_c = s.get("state_at_activate") or {}, s.get("state_at_capture") or {}
            s["_score_swing"] = None
            if st_a and st_c and st_a.get("score_ours") is not None and st_c.get("score_ours") is not None:
                s["_score_swing"] = (st_c["score_ours"] - st_c["score_theirs"]) - (st_a["score_ours"] - st_a["score_theirs"])
            s["_in"] = s.get("damage_in_smoke") or 0.0
            s["_behind"] = s.get("damage_behind_smoke") or 0.0
            s["_total"] = s.get("smoke_damage_total") or 0.0
            d = s.get("damage_detail") or {}
            s["_owner_damage"] = (d.get("damage_in_smoke_smoker") or 0) + (d.get("damage_behind_smoke_smoker") or 0)
            s["_radar"] = len(s.get("radar_detections_in_smoke") or [])
            s["_games_label"] = self.game_label(s["_key"])
        self.smokes.sort(key=lambda s: (s["_key"], s["_act_s"]))
        self.by_game = defaultdict(list)
        for s in self.smokes:
            self.by_game[s["_key"]].append(s)
        self.games_played = Counter()
        for r in self.inventory.values():
            if r["status"] == "played":
                for t in r["our_teams"].split(";"):
                    if t:
                        self.games_played[t] += 1
        if not self.games_played:
            for (m, g, t) in self.job_by_key:
                self.games_played[t] += 1

    def game_label(self, key):
        g = self.games.get(key)
        inv = self.inventory.get(key)
        if inv:
            stage = inv["stage"]
            part = f"{inv['group']} {inv['round']}".strip() if inv["group"] else inv["round"]
            return f"{inv['teams']} | {stage} {part} | Game {inv['game_no']}"
        if g:
            names = " vs ".join(t["name"] or "?" for t in g["teams"])
            return f"{names} | {g.get('round') or ''} | Game {g.get('game_no') or ''}"
        return f"match {key[0]} game {key[1]}"


def map_px(data, map_name, x, z):
    m = data.maps.get(map_name)
    if not m:
        return None
    scale = NATIVE / m["space_size"]
    return (x * scale + NATIVE / 2, -z * scale + NATIVE / 2)


def svg_donut(parts, colors, size=120, hole=0.6):
    total = sum(v for _, v in parts) or 1
    cx = cy = size / 2
    r = size / 2 - 2
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" class="donut">']
    angle = -math.pi / 2
    for i, (label, v) in enumerate(parts):
        frac = v / total
        a2 = angle + frac * 2 * math.pi
        if frac >= 0.999:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{colors[i % len(colors)]}"><title>{esc(label)}: {v}</title></circle>')
        else:
            x1, y1 = cx + r * math.cos(angle), cy + r * math.sin(angle)
            x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
            large = 1 if frac > 0.5 else 0
            out.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large},1 {x2:.1f},{y2:.1f} Z" fill="{colors[i % len(colors)]}"><title>{esc(label)}: {v} ({frac * 100:.0f}%)</title></path>')
        angle = a2
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * hole}" fill="var(--panel)"/>')
    out.append("</svg>")
    legend = "".join(f'<span class="legend"><i style="background:{colors[i % len(colors)]}"></i>{esc(l)} {v}</span>' for i, (l, v) in enumerate(parts))
    return "".join(out) + f'<div class="legend-row">{legend}</div>'


def svg_stacked_bar(parts, colors, width=320, height=18):
    total = sum(v for _, v in parts) or 1
    out = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" class="bar">']
    x = 0
    for i, (label, v) in enumerate(parts):
        w = width * v / total
        out.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="{height}" fill="{colors[i % len(colors)]}"><title>{esc(label)}: {v if isinstance(v, int) else round(v)}</title></rect>')
        x += w
    out.append("</svg>")
    legend = "".join(f'<span class="legend"><i style="background:{colors[i % len(colors)]}"></i>{esc(l)} {v if isinstance(v, int) else fmt_int(v)}</span>' for i, (l, v) in enumerate(parts))
    return "".join(out) + f'<div class="legend-row">{legend}</div>'


def mini_bar(value, max_value, color, width=90):
    frac = 0 if not max_value else max(0.0, min(1.0, value / max_value))
    return f'<span class="mini"><i style="width:{frac * width:.0f}px;background:{color}"></i></span>'


PALETTE = ["#F5C542", "#5DADE2", "#B388FF", "#6EE7B7", "#FB923C", "#F472B6", "#A3E635", "#94A3B8", "#F87171", "#22D3EE"]


class Site:
    def __init__(self, data, out, colors):
        self.d = data
        self.out = out
        self.colors = colors
        self.smoke_href = {}
        for s in data.smokes:
            s["_slug"] = f"{s['_match']}_g{s['game_no']}_{s['smoke_id']}"
            self.smoke_href[s["_slug"]] = f"smokes/{s['_slug']}.html"

    def color(self, team):
        return self.colors.get(team, "#94A3B8")

    def nav(self, depth, active):
        base = "../" * depth
        items = [("Home", "index.html"), ("Analysis", "analysis.html"), ("Awards", "awards.html"), ("Maps", "maps.html"), ("All Smokes", "smokes.html")]
        links = "".join(f'<a href="{base}{h}" class="{"active" if n == active else ""}">{n}</a>' for n, h in items)
        return f'<nav class="top"><span class="brand">Smoke Signals</span>{links}</nav>'

    def page(self, title, body, depth=0, active="", extra_head=""):
        base = "../" * depth
        return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Smoke Signals</title><link rel="stylesheet" href="{base}style.css">{extra_head}</head>
<body>{self.nav(depth, active)}<main>{body}</main>
<footer>KotS XIX NA smoke analysis. Built from replays with Smoke Signals. Purpose and intent tags are pending hand-tagging, so everything here is descriptive.</footer>
<script src="{base}site.js"></script></body></html>"""

    def write(self, rel, text):
        path = os.path.join(self.out, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def team_tag(self, team):
        return f'<span class="tag" style="--c:{self.color(team)}">{esc(team)}</span>'

    def copy_assets(self):
        d = self.d
        os.makedirs(os.path.join(self.out, "img"), exist_ok=True)
        os.makedirs(os.path.join(self.out, "maps"), exist_ok=True)
        for m in d.maps.values():
            src = os.path.join(d.maps_dir, m["map"] + ".webp")
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(self.out, "maps", m["map"] + ".webp"))
        for s in d.smokes:
            job = s["_job"]
            if not job:
                continue
            frames = os.path.join(d.batch, "games", job["name"], "frames")
            s["_img"] = {}
            for field in ["frame_act", "frame_cap", "frame_act_zoom", "frame_cap_zoom"]:
                name = s.get(field)
                if not name:
                    continue
                webp = name.rsplit(".", 1)[0] + ".webp"
                src = os.path.join(frames, webp)
                if os.path.exists(src):
                    rel = f"img/{job['name']}/{webp}"
                    dst = os.path.join(self.out, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    if not os.path.exists(dst):
                        shutil.copyfile(src, dst)
                    s["_img"][field] = rel
            clip = d.clip_files.get(s["_slug"]) or d.clip_files.get(str(s["smoke_id"]))
            s["_clip"] = None
            if clip:
                rel = f"clips/{s['_slug']}.mp4"
                dst = os.path.join(self.out, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(clip, dst)
                s["_clip"] = rel

    def img(self, s, field, depth, cls=""):
        rel = (s.get("_img") or {}).get(field)
        if not rel:
            return '<div class="noimg">no frame</div>'
        return f'<img class="{cls}" src="{"../" * depth}{rel}" alt="{esc(field)}" loading="lazy">'

    def smoke_card(self, s, depth=0, note=""):
        base = "../" * depth
        thumb = (s.get("_img") or {}).get("frame_cap_zoom") or (s.get("_img") or {}).get("frame_cap")
        img = f'<img src="{base}{thumb}" alt="" loading="lazy">' if thumb else '<div class="noimg">no frame</div>'
        return f"""<a class="card smoke-card" href="{base}{self.smoke_href[s['_slug']]}">{img}<div class="card-body">
<div>{self.team_tag(s['team'])} <b>{esc(s['player'])}</b> <span class="muted">{esc(s['ship'])}</span></div>
<div class="muted small">{esc(s['_games_label'])} | {esc(s['_act_clock'])}</div>
<div class="small">{fmt_int(s['_total'])} smoke damage{(' | ' + esc(note)) if note else ''}</div></div></a>"""

    def build(self):
        self.copy_assets()
        self.write("style.css", CSS.replace("__TEAMCOLORS__", "".join(f'--team-{t.lower().replace("-", "")}:{c};' for t, c in self.colors.items())))
        self.write("site.js", JS)
        self.home()
        self.analysis()
        self.awards()
        self.maps_page()
        self.all_smokes()
        for key in self.d.by_game:
            self.game_page(key)
        for i, s in enumerate(self.d.smokes):
            self.smoke_page(s)

    def home(self):
        d = self.d
        n_games = len(d.by_game)
        cards = [
            ("Analysis", "analysis.html", "Top players, three headline findings and one card per team."),
            ("Awards", "awards.html", "The four smokes of the tournament, player awards and clan awards."),
            ("Maps", "maps.html", "Every smoke as a dot on its map, coloured by team."),
            ("All Smokes", "smokes.html", f"The table of all {len(d.smokes)} analysed smokes, with filters and sorting."),
        ]
        body = f"""<section class="briefing"><h1>Mission briefing</h1>
<p>We want to win games. This site breaks down how top competitive teams use smoke: {len(d.smokes)} smokes from {n_games} King of the Sea XIX NA games played by H-SR, RESIN and PN, read straight from the replays.</p>
<p class="muted">Every smoke has an activation frame, a capture frame, a zoomed close-up and its numbers. Purpose and intent tags come later by hand.</p></section>
<section class="cards">{"".join(f'<a class="card toc" href="{h}"><h2>{esc(n)}</h2><p>{esc(t)}</p></a>' for n, h, t in cards)}</section>"""
        self.write("index.html", self.page("Home", body, active="Home"))

    def player_stats(self):
        d = self.d
        by_player = defaultdict(lambda: {"smokes": 0, "damage": 0.0, "radar": 0, "ships": Counter(), "team": "", "selfish": 0, "games": set()})
        for s in d.smokes:
            p = by_player[s["player"]]
            p["smokes"] += 1
            p["damage"] += s["_total"]
            p["radar"] += s["_radar"]
            p["ships"][s["ship"]] += 1
            p["team"] = s["team"]
            p["selfish"] += 1 if s.get("selfish_smoke") else 0
            p["games"].add(s["_key"])
        return by_player

    def analysis(self):
        d = self.d
        players = self.player_stats()
        top = sorted(players.items(), key=lambda kv: -kv[1]["damage"])[:5]
        max_damage = max((p["damage"] for _, p in top), default=1)
        max_smokes = max((p["smokes"] for _, p in players.values() and top), default=1) if top else 1
        cards = []
        for name, p in top:
            ships = ", ".join(f"{s} x{n}" if n > 1 else s for s, n in p["ships"].most_common())
            avg = p["damage"] / p["smokes"] if p["smokes"] else 0
            cards.append(f"""<div class="card player"><div>{self.team_tag(p['team'])} <b>{esc(name)}</b></div><div class="muted small">{esc(ships)}</div>
<table class="kv"><tr><td>Smokes laid</td><td>{p['smokes']} {mini_bar(p['smokes'], max_smokes, self.color(p['team']))}</td></tr>
<tr><td>Smoke damage</td><td>{fmt_int(p['damage'])} {mini_bar(p['damage'], max_damage, self.color(p['team']))}</td></tr>
<tr><td>Average per smoke</td><td>{fmt_int(avg)}</td></tr>
<tr><td>Radar spots in smoke</td><td>{p['radar']}</td></tr></table></div>""")
        findings = self.findings()
        teams = "".join(self.team_card(t) for t in TEAMS if any(s["team"] == t for s in d.smokes))
        body = f"""<h1>Analysis</h1>
<h2>Top 5 players by smoke damage</h2><section class="cards">{"".join(cards)}</section>
<h2>Three headline findings</h2><ol class="findings">{"".join(f'<li>{f}</li>' for f in findings)}</ol>
<h2>Team cards</h2><p class="muted">Identical layout for easy comparison. Purpose and intent wait for the hand tags, so these cards are descriptive, not conclusions.</p>
<section class="cards teams">{teams}</section>"""
        self.write("analysis.html", self.page("Analysis", body, active="Analysis"))

    def team_rows(self, team):
        return [s for s in self.d.smokes if s["team"] == team]

    def findings(self):
        d = self.d
        out = []
        total = len(d.smokes)
        behind = sum(s["_behind"] for s in d.smokes)
        inside = sum(s["_in"] for s in d.smokes)
        if inside + behind > 0:
            out.append(f"Of {fmt_int(inside + behind)} smoke damage, {behind / (inside + behind) * 100:.0f}% was fired from behind a smoke by ships outside it, and {inside / (inside + behind) * 100:.0f}% from inside one.")
        near = sum(1 for s in d.smokes if s.get("cap_proximity_m") is not None and s["cap_proximity_m"] <= 1000)
        inside_cap = sum(1 for s in d.smokes if s.get("cap_proximity_m") is not None and s["cap_proximity_m"] < 0)
        out.append(f"{near / total * 100:.0f}% of smokes went up within 1 km of a cap edge, and {inside_cap / total * 100:.0f}% reached inside a cap.")
        per_game = {t: len(self.team_rows(t)) / d.games_played[t] for t in TEAMS if d.games_played.get(t)}
        if per_game:
            hi = max(per_game, key=per_game.get)
            lo = min(per_game, key=per_game.get)
            out.append(f"{hi} laid the most smokes per game ({per_game[hi]:.1f}); {lo} the fewest ({per_game[lo]:.1f}). Selfish smokes, with no teammate ever inside or shooting through, made up {sum(1 for s in d.smokes if s.get('selfish_smoke')) / total * 100:.0f}% of all smokes.")
        return out[:3]

    def team_card(self, team):
        d = self.d
        rows = self.team_rows(team)
        games = d.games_played.get(team) or 1
        total_damage = sum(s["_total"] for s in rows)
        ships = Counter(s["ship"] for s in rows).most_common()
        donut = svg_donut(ships[:8] + ([("other", sum(n for _, n in ships[8:]))] if len(ships) > 8 else []), PALETTE)
        timing = Counter()
        for s in rows:
            rem = clock_remaining_seconds(s["_act_clock"])
            if rem is None:
                timing["unknown"] += 1
            elif rem > 800:
                timing["early"] += 1
            elif rem > 400:
                timing["mid"] += 1
            else:
                timing["late"] += 1
        timing_bar = svg_stacked_bar([(k, timing.get(k, 0)) for k in ["early", "mid", "late"] if timing.get(k)], ["#6EE7B7", "#F5C542", "#F87171"])
        inside = sum(s["_in"] for s in rows)
        behind = sum(s["_behind"] for s in rows)
        team_total = sum(v for (t, _), v in d.damage_by_team_game.items() if t == team)
        outside = max(0.0, team_total - inside - behind)
        split = svg_stacked_bar([("in smoke", inside), ("behind smoke", behind), ("outside", outside)], ["#F5C542", "#5DADE2", "#475569"])
        selfish = sum(1 for s in rows if s.get("selfish_smoke"))
        prox = Counter()
        for s in rows:
            m = s.get("cap_proximity_m")
            if m is None:
                prox["unknown"] += 1
            elif m < 0:
                prox["inside cap"] += 1
            elif m < 1000:
                prox["< 1 km"] += 1
            elif m < 3000:
                prox["1-3 km"] += 1
            else:
                prox["> 3 km"] += 1
        prox_bar = svg_stacked_bar([(k, prox[k]) for k in ["inside cap", "< 1 km", "1-3 km", "> 3 km", "unknown"] if prox.get(k)], ["#B388FF", "#5DADE2", "#6EE7B7", "#475569", "#94A3B8"])
        early_share = timing.get("early", 0) / max(1, len(rows))
        near_share = (prox.get("inside cap", 0) + prox.get("< 1 km", 0)) / max(1, len(rows))
        when = "early" if early_share > 0.45 else ("late" if timing.get("late", 0) / max(1, len(rows)) > 0.45 else "through the match")
        where = "close to caps" if near_share > 0.5 else "away from caps"
        takeaway = f"{team} smokes {when} and {where}; {selfish / max(1, len(rows)) * 100:.0f}% of its smokes were selfish."
        return f"""<div class="card team" style="--c:{self.color(team)}"><h3>{self.team_tag(team)} {esc(team)}</h3>
<table class="kv"><tr><td>Total smokes</td><td>{len(rows)}</td></tr><tr><td>Smokes per game</td><td>{len(rows) / games:.1f}</td></tr><tr><td>Smoke damage per game</td><td>{fmt_int(total_damage / games)}</td></tr></table>
<h4>Ships</h4>{donut}
<h4>Timing across the match clock</h4>{timing_bar}
<h4>Damage split</h4>{split}
<h4>Habits</h4><p class="small">Selfish smokes: {selfish} of {len(rows)} ({selfish / max(1, len(rows)) * 100:.0f}%)</p>{prox_bar}
<p class="takeaway">{esc(takeaway)}</p>
<p class="muted small">Purpose and intent are pending hand tags.</p></div>"""

    def awards(self):
        d = self.d
        rows = d.smokes
        if not rows:
            return
        best = max(rows, key=lambda s: s["_total"])
        with_prox = [s for s in rows if s.get("cap_proximity_m") is not None]
        deep = min(with_prox, key=lambda s: s["cap_proximity_m"]) if with_prox else None
        bait = max(rows, key=lambda s: (s["_radar"], s["_total"]))
        selfish = [s for s in rows if s.get("selfish_smoke")]
        most_selfish = max(selfish, key=lambda s: s["_owner_damage"]) if selfish else None
        smoke_awards = [
            ("Smoke of the Tournament", best, f"{fmt_int(best['_total'])} smoke damage"),
            ("Deepest Cap Smoke", deep, f"{fmt_km(deep['cap_proximity_m'])} inside cap {deep.get('cap_proximity_name')}" if deep else ""),
            ("Radar Bait", bait, f"{bait['_radar']} radar spots on allies in the smoke"),
            ("Most Selfish Smoke", most_selfish, f"{fmt_int(most_selfish['_owner_damage'])} damage by the owner alone" if most_selfish else ""),
        ]
        blocks = []
        for title, s, note in smoke_awards:
            if not s:
                blocks.append(f'<div class="card award"><h3>{esc(title)}</h3><p class="muted">Nothing here, just clear skies.</p></div>')
                continue
            clip = f'<div class="clip"><video controls preload="metadata" src="{s["_clip"]}"></video><div class="clip-controls"><button class="speed" data-rate="1">1x (5x real time)</button><button class="speed" data-rate="2">2x (10x real time)</button></div></div>' if s.get("_clip") else '<p class="muted small">Clip available on request.</p>'
            blocks.append(f"""<div class="card award"><h3>{esc(title)}</h3><p class="note">{esc(note)}</p>
{self.smoke_card(s)}
<div class="frames two">{self.img(s, 'frame_act', 0)}{self.img(s, 'frame_cap', 0)}</div>{clip}</div>""")
        players = self.player_stats()
        def top_by(key, minimum=0):
            items = [(n, p) for n, p in players.items() if p["smokes"] >= minimum]
            return max(items, key=lambda kv: key(kv[1])) if items else None
        golden = top_by(lambda p: p["damage"])
        father = top_by(lambda p: p["smokes"])
        haze = top_by(lambda p: p["damage"] / p["smokes"], minimum=3)
        selfish_p = top_by(lambda p: p["selfish"])
        player_awards = [
            ("Golden Cloud", "Most total smoke damage", golden, lambda p: f"{fmt_int(p['damage'])} damage over {p['smokes']} smokes"),
            ("The Smokefather", "Most smokes laid", father, lambda p: f"{p['smokes']} smokes in {len(p['games'])} games"),
            ("Best in Haze", "Highest average smoke damage per smoke (minimum 3 smokes)", haze, lambda p: f"{fmt_int(p['damage'] / p['smokes'])} per smoke over {p['smokes']} smokes"),
            ("Most Selfish Smoker", "Most selfish smokes", selfish_p, lambda p: f"{p['selfish']} selfish smokes of {p['smokes']}"),
        ]
        pcards = "".join(
            f'<div class="card award-p"><h3>{esc(t)}</h3><p class="muted small">{esc(sub)}</p><p>{self.team_tag(w[1]["team"])} <b>{esc(w[0])}</b></p><p class="note">{esc(fmt(w[1]))}</p></div>' if w else f'<div class="card award-p"><h3>{esc(t)}</h3><p class="muted">Nothing here, just clear skies.</p></div>'
            for t, sub, w, fmt in player_awards)
        clan_rows = []
        for t in TEAMS:
            rows_t = self.team_rows(t)
            g = d.games_played.get(t) or 0
            if not g:
                continue
            clan_rows.append((t, len(rows_t) / g, sum(s["_total"] for s in rows_t) / g, sum(1 for s in rows_t if s.get("selfish_smoke")) / g, g))
        def clan_award(title, idx, fmt):
            if not clan_rows:
                return ""
            w = max(clan_rows, key=lambda r: r[idx])
            return f'<div class="card award-p"><h3>{esc(title)}</h3><p>{self.team_tag(w[0])} <b>{esc(w[0])}</b></p><p class="note">{esc(fmt(w[idx]))} per game over {w[4]} games</p></div>'
        ccards = clan_award("Most smokes laid", 1, lambda v: f"{v:.1f} smokes") + clan_award("Most smoke damage", 2, lambda v: f"{fmt_int(v)} damage") + clan_award("Most selfish smokes", 3, lambda v: f"{v:.1f} selfish smokes")
        body = f"""<h1>Awards</h1>
<h2>Smoke awards</h2><section class="cards awards">{"".join(blocks)}</section>
<h2>Player awards</h2><section class="cards">{pcards}</section>
<h2>Clan awards (per game played)</h2><section class="cards">{ccards}</section>"""
        self.write("awards.html", self.page("Awards", body, active="Awards"))

    def map_figure(self, map_name, smokes, depth=0, size=768, anchor_prefix="smoke"):
        d = self.d
        m = d.maps.get(map_name)
        base = "../" * depth
        if not m:
            return '<p class="muted">Map image missing.</p>'
        dots = []
        for s in smokes:
            px = map_px(d, map_name, s["origin_xy"]["x"], s["origin_xy"]["z"])
            if not px:
                continue
            dots.append(f'<a href="{base}{self.smoke_href[s["_slug"]]}" id="{anchor_prefix}-{s["_slug"]}"><circle cx="{px[0]:.1f}" cy="{px[1]:.1f}" r="7" fill="{self.color(s["team"])}" stroke="#0B1C2C" stroke-width="1.5"><title>{esc(s["player"])} {esc(s["ship"])} at {esc(s["_act_clock"])}, {fmt_int(s["_total"])} dmg</title></circle></a>')
        return f'<div class="mapwrap" style="max-width:{size}px"><img src="{base}maps/{m["map"]}.webp" alt="{esc(map_name)}"><svg viewBox="0 0 {NATIVE} {NATIVE}">{"".join(dots)}</svg></div>'

    def maps_page(self):
        d = self.d
        sections = []
        by_map = defaultdict(list)
        for s in d.smokes:
            by_map[s["map"]].append(s)
        for map_name, smokes in sorted(by_map.items(), key=lambda kv: -len(kv[1])):
            counts = Counter(s["team"] for s in smokes)
            prox = [s["cap_proximity_m"] for s in smokes if s.get("cap_proximity_m") is not None]
            near = sum(1 for p in prox if p <= 1000)
            games = len({s["_key"] for s in smokes})
            take = [
                f"{len(smokes)} smokes in {games} games: " + ", ".join(f"{t} {n}" for t, n in counts.most_common()) + ".",
                f"{near / max(1, len(prox)) * 100:.0f}% went up within 1 km of a cap edge." if prox else "",
                f"Average smoke damage {fmt_int(sum(s['_total'] for s in smokes) / len(smokes))}.",
            ]
            sections.append(f'<section class="map-section"><h2>{esc(pretty_map(map_name))}</h2>{self.map_figure(map_name, smokes)}<ul class="takeaways">{"".join(f"<li>{esc(t)}</li>" for t in take if t)}</ul></section>')
        body = f"<h1>Maps</h1><p class=\"muted\">One dot per smoke at its origin, coloured by team. Click a dot to open the smoke.</p>{''.join(sections)}"
        self.write("maps.html", self.page("Maps", body, active="Maps"))

    def all_smokes(self):
        d = self.d
        records = []
        for s in d.smokes:
            thumb = (s.get("_img") or {}).get("frame_cap_zoom") or ""
            records.append({
                "id": s["smoke_id"], "team": s["team"], "player": s["player"], "ship": s["ship"], "map": pretty_map(s["map"]),
                "game": s["_games_label"], "game_href": f"games/{s['_match']}_g{s['game_no']}.html", "type": s.get("smoke_type") or "",
                "clock": s["_act_clock"], "total": round(s["_total"]), "inside": round(s["_in"]), "behind": round(s["_behind"]),
                "radar": s["_radar"], "duration": round(s["_duration"]) if s.get("_duration") is not None else None,
                "swing": s["_score_swing"], "cap": s.get("cap_proximity_m"), "cap_name": s.get("cap_proximity_name") or "",
                "selfish": bool(s.get("selfish_smoke")), "flag": bool(s.get("owner_flag")), "thumb": thumb, "href": self.smoke_href[s["_slug"]],
                "color": self.color(s["team"]),
            })
        max_total = max((r["total"] for r in records), default=1)
        body = f"""<h1>All smokes</h1>
<div class="filters">
<label>Team <select id="f-team"><option value="">all</option></select></label>
<label>Player <select id="f-player"><option value="">all</option></select></label>
<label>Ship <select id="f-ship"><option value="">all</option></select></label>
<label>Map <select id="f-map"><option value="">all</option></select></label>
<label>Game <select id="f-game"><option value="">all</option></select></label>
<label>Type <select id="f-type"><option value="">all</option></select></label>
<label>Sort <select id="f-sort"><option value="total">smoke damage (total)</option><option value="inside">damage in smoke</option><option value="behind">damage behind smoke</option><option value="radar">radar spots in smoke</option><option value="duration">duration</option><option value="swing">score change during the smoke</option><option value="cap">cap proximity</option></select></label>
<span id="count" class="muted"></span></div>
<table class="smokes" id="smokes"><thead><tr><th></th><th>Team</th><th>Player</th><th>Ship</th><th>Map</th><th>Game</th><th>Clock</th><th>Damage</th><th>Cap</th><th>Radar</th><th></th></tr></thead><tbody></tbody></table>
<p id="empty" class="muted" hidden>Nothing here, just clear skies.</p>
<script>window.SMOKES = {json.dumps(records)}; window.MAX_TOTAL = {max_total};</script>"""
        self.write("smokes.html", self.page("All Smokes", body, active="All Smokes"))

    def game_page(self, key):
        d = self.d
        smokes = d.by_game[key]
        g = d.games.get(key)
        inv = d.inventory.get(key)
        teams = g["teams"] if g else []
        header = []
        if inv:
            header.append(f"{inv['stage']} {inv['group']} {inv['round']}".replace("  ", " "))
            header.append(f"Game {inv['game_no']} on {pretty_map(smokes[0]['map'])}, {inv['date']}")
            header.append(f"Score {inv['score']}, winner {inv['winner']}")
        if g:
            header.append(f"Ended by {esc(g.get('finish_type') or '?')} at {(g.get('battle_end') or {}).get('clock', '?')}")
        roster = ""
        for t in teams:
            rows = "".join(f"<tr><td>{esc(p['player'])}</td><td>{esc(p['ship'])}</td><td>{p['smoke_activations'] or ''}</td></tr>" for p in t["players"])
            roster += f'<div class="card"><h3>{self.team_tag(t["name"])} {esc(t["name"])} <span class="muted small">{esc(t.get("spawn_side") or "")} spawn</span></h3><table class="roster"><tr><th>Player</th><th>Ship</th><th>Smokes</th></tr>{rows}</table></div>'
        timeline = self.timeline_svg(smokes)
        score = self.score_svg(smokes, teams)
        cards = "".join(self.smoke_card(s, depth=1) for s in smokes)
        body = f"""<h1>{esc(smokes[0]['_games_label'])}</h1><p class="muted">{" | ".join(esc(h) for h in header)}</p>
<section class="two-col">{self.map_figure(smokes[0]['map'], smokes, depth=1, size=480, anchor_prefix='g')}<div><h2>Smokes across the match</h2>{timeline}<h2>Score with smoke markers</h2>{score}</div></section>
<h2>Rosters</h2><section class="cards">{roster}</section>
<h2>Smokes in this game</h2><section class="cards">{cards}</section>"""
        self.write(f"games/{key[0]}_g{key[1]}.html", self.page(smokes[0]["_games_label"], body, depth=1))

    def timeline_svg(self, smokes):
        w, h = 520, 70
        out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" class="timeline">', f'<line x1="10" y1="40" x2="{w - 10}" y2="40" stroke="#475569"/>']
        for m in range(0, 21, 5):
            x = 10 + (w - 20) * m / 20
            out.append(f'<text x="{x:.0f}" y="62" fill="#94A3B8" font-size="10" text-anchor="middle">{20 - m}:00</text>')
        for s in smokes:
            rem = clock_remaining_seconds(s["_act_clock"])
            if rem is None:
                continue
            x = 10 + (w - 20) * (MATCH_SECONDS - rem) / MATCH_SECONDS
            dur = s.get("_duration") or 0
            x2 = min(w - 10, x + (w - 20) * dur / MATCH_SECONDS)
            out.append(f'<a href="../{self.smoke_href[s["_slug"]]}"><rect x="{x:.0f}" y="30" width="{max(2, x2 - x):.0f}" height="20" fill="{self.color(s["team"])}" opacity="0.8"><title>{esc(s["player"])} {esc(s["ship"])} at {esc(s["_act_clock"])}</title></rect></a>')
        out.append("</svg>")
        return "".join(out)

    def score_svg(self, smokes, teams):
        points = []
        for s in smokes:
            for st, moment in [(s.get("state_at_activate"), s.get("t_activate") or s["t_created"]), (s.get("state_at_capture"), s.get("t_capture"))]:
                if st and moment and st.get("score_ours") is not None:
                    rem = clock_remaining_seconds(moment.get("clock"))
                    if rem is not None:
                        points.append((MATCH_SECONDS - rem, s["team"], st["score_ours"], st["score_theirs"]))
        if not points:
            return '<p class="muted small">No score samples.</p>'
        points.sort()
        w, h = 520, 160
        max_score = max(max(p[2], p[3]) for p in points) or 1000
        def xy(t, v):
            return 10 + (w - 20) * t / MATCH_SECONDS, h - 20 - (h - 40) * v / max(1000, max_score)
        out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" class="score">']
        team_names = [t["name"] for t in teams] or sorted({p[1] for p in points})
        series = {}
        for t, team, ours, theirs in points:
            other = next((n for n in team_names if n != team), "other")
            series.setdefault(team, []).append(xy(t, ours))
            series.setdefault(other, []).append(xy(t, theirs))
        for team, pts in series.items():
            pts.sort()
            d = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
            out.append(f'<polyline points="{d}" fill="none" stroke="{self.color(team)}" stroke-width="2"/>')
        for s in smokes:
            rem = clock_remaining_seconds(s["_act_clock"])
            if rem is None:
                continue
            x, _ = xy(MATCH_SECONDS - rem, 0)
            out.append(f'<line x1="{x:.0f}" y1="10" x2="{x:.0f}" y2="{h - 20}" stroke="{self.color(s["team"])}" stroke-dasharray="3,3" opacity="0.6"/>')
        out.append(f'<text x="10" y="{h - 4}" fill="#94A3B8" font-size="10">20:00</text><text x="{w - 10}" y="{h - 4}" fill="#94A3B8" font-size="10" text-anchor="end">0:00</text>')
        out.append("".join(f'<text x="{14 + i * 90}" y="14" fill="{self.color(t)}" font-size="11">{esc(t)}</text>' for i, t in enumerate(series)))
        out.append("</svg>")
        return "".join(out)

    def cap_diagram(self, s):
        m = s.get("cap_proximity_m")
        if m is None:
            return '<p class="muted small">No cap proximity (no capture frame).</p>'
        w, h = 300, 90
        smoke_r = (s.get("radius") or 15) * 30
        cap_r = 4000
        scale = (w - 40) / (2 * cap_r + max(0, m) + 2 * smoke_r)
        cx = 20 + cap_r * scale
        sx = cx + (cap_r + m + smoke_r) * scale
        return f"""<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" class="capdiag"><circle cx="{cx:.0f}" cy="{h / 2}" r="{cap_r * scale:.0f}" fill="none" stroke="#5DADE2" stroke-dasharray="4,3"/><text x="{cx:.0f}" y="{h / 2 + 4}" fill="#5DADE2" font-size="12" text-anchor="middle">cap {esc(s.get('cap_proximity_name') or '')}</text>
<circle cx="{sx:.0f}" cy="{h / 2}" r="{max(4, smoke_r * scale):.0f}" fill="#CBD5E1" opacity="0.8"/><text x="{sx:.0f}" y="{h / 2 - 12}" fill="#E2E8F0" font-size="11" text-anchor="middle">smoke</text>
<text x="{w / 2}" y="{h - 4}" fill="#94A3B8" font-size="11" text-anchor="middle">{"inside the cap by " if m < 0 else "edge to edge "}{fmt_km(abs(m))}</text></svg>"""

    def smoke_page(self, s):
        d = self.d
        game = d.by_game[s["_key"]]
        idx = game.index(s)
        prev_s = game[idx - 1] if idx > 0 else None
        next_s = game[idx + 1] if idx + 1 < len(game) else None
        st = s.get("state_at_capture") or s.get("state_at_activate") or {}
        alive = ", ".join(f"{a.get('team')} {a.get('ship_class') or ''} {a.get('alive', a.get('count', ''))}" for a in (st.get("ships_alive") or [])) if st else ""
        split = svg_stacked_bar([("in smoke", s["_in"]), ("behind smoke", s["_behind"])], ["#F5C542", "#5DADE2"]) if s["_total"] > 0 else '<p class="muted small">No smoke damage.</p>'
        clip = f'<div class="clip"><video controls preload="metadata" src="../{s["_clip"]}"></video><div class="clip-controls"><button class="speed" data-rate="1">1x (5x real time)</button><button class="speed" data-rate="2">2x (10x real time)</button></div></div>' if s.get("_clip") else '<p class="muted small">Clip available on request.</p>'
        nav = []
        if prev_s:
            nav.append(f'<a href="{prev_s["_slug"]}.html">&larr; previous smoke in this game</a>')
        nav.append(f'<a href="../games/{s["_match"]}_g{s["game_no"]}.html">up to the game</a>')
        nav.append(f'<a href="../maps.html#smoke-{s["_slug"]}">its dot on the map</a>')
        if next_s:
            nav.append(f'<a href="{next_s["_slug"]}.html">next smoke in this game &rarr;</a>')
        flag = f'<p class="warn">Owner attribution flagged: {esc(s.get("owner_note"))}</p>' if s.get("owner_flag") else ""
        dur = f"{s['_duration']:.0f} s" if s.get("_duration") is not None else "still standing at the end"
        body = f"""<h1>{self.team_tag(s['team'])} {esc(s['player'])} <span class="muted">{esc(s['ship'])}</span></h1>
<p class="muted">{esc(pretty_map(s['map']))} | {esc(s['_games_label'])} | activated {esc(s['_act_clock'])}, captured {esc(s['_cap_clock'])} | {esc(s.get('smoke_type') or '')} smoke {esc(s.get('variant') or '')}</p>
<p class="big">{fmt_int(s['_total'])} smoke damage</p>{flag}
<section class="frames two">{self.img(s, 'frame_act', 1)}{self.img(s, 'frame_cap', 1)}</section>
<section class="frames two zoom">{self.img(s, 'frame_act_zoom', 1)}{self.img(s, 'frame_cap_zoom', 1)}</section>
{clip}
<section class="two-col"><div class="card"><h3>Stats</h3><table class="kv">
<tr><td>Duration</td><td>{esc(dur)}</td></tr>
<tr><td>Smoke damage</td><td>{split}</td></tr>
<tr><td>Radar spots in smoke</td><td>{s['_radar']}</td></tr>
<tr><td>Allies in smoke at capture</td><td>{esc(', '.join(s.get('allies_in_smoke') or [])) or 'none'}</td></tr>
<tr><td>Selfish smoke</td><td>{'yes' if s.get('selfish_smoke') else ('no' if s.get('selfish_smoke') is not None else 'unknown')}</td></tr>
<tr><td>Score at capture</td><td>{esc(st.get('score_ours', '-'))} : {esc(st.get('score_theirs', '-'))}</td></tr>
<tr><td>Ships alive at capture</td><td>{esc(alive) or '-'}</td></tr></table></div>
<div class="card"><h3>Cap proximity</h3>{self.cap_diagram(s)}<h3>Tags</h3><p class="muted">untagged</p></div></section>
<nav class="smoke-nav">{" | ".join(nav)}</nav>"""
        self.write(f"smokes/{s['_slug']}.html", self.page(f"{s['player']} {s['ship']} {s['_act_clock']}", body, depth=1))


def pretty_map(name):
    pretty = {"16_OC_bees_to_honey": "Hotspot", "45_Zigzag": "Loop", "40_Okinawa": "Okinawa", "22_tierra_del_fuego": "Land of Fire", "58_RidgeNew": "Mountain Range", "47_Sleeping_Giant": "Sleeping Giant", "25_sea_hope": "Sea of Fortune"}
    return pretty.get(name, name)


CSS = """:root{--bg:#0B1C2C;--panel:#16283A;--panel2:#1E3448;--text:#EEF2F5;--muted:#9FB0C0;--line:#2A4258;__TEAMCOLORS__}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 "Segoe UI",system-ui,sans-serif}
main{max-width:1180px;margin:0 auto;padding:16px}h1,h2,h3,h4{margin:.6em 0 .3em}h1{font-size:1.7em}h2{font-size:1.25em;border-bottom:1px solid var(--line);padding-bottom:4px}
a{color:#9CD3FF}nav.top{display:flex;gap:4px;align-items:center;background:#07131f;padding:8px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
nav.top .brand{font-weight:700;letter-spacing:.04em;margin-right:12px;color:#F5C542}nav.top a{padding:6px 10px;border-radius:6px;color:var(--text);text-decoration:none}nav.top a.active,nav.top a:hover{background:var(--panel2)}
footer{color:var(--muted);font-size:.85em;text-align:center;padding:24px 16px}
.briefing{background:var(--panel);border-left:6px solid #F5C542;padding:16px 20px;border-radius:8px;margin:16px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin:8px 0 20px}.cards.teams{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}.cards.awards{grid-template-columns:repeat(auto-fill,minmax(520px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px;color:var(--text);text-decoration:none;display:block}.card.toc h2{border:0;margin-top:0}.card.team{border-top:4px solid var(--c)}
.smoke-card{padding:0;overflow:hidden}.smoke-card img{width:100%;display:block;aspect-ratio:1;object-fit:cover}.card-body{padding:8px 10px}
.awards .smoke-card{display:flex;align-items:center;margin:8px 0}.awards .smoke-card img{width:160px;height:160px;flex:none}
.tag{display:inline-block;padding:1px 7px;border-radius:999px;font-size:.78em;font-weight:700;background:var(--c);color:#07131f}
.muted{color:var(--muted)}.small{font-size:.85em}.big{font-size:1.4em;font-weight:700}.note{color:#F5C542}.warn{color:#FB923C}
table.kv td{padding:3px 8px 3px 0;vertical-align:top}table.kv td:first-child{color:var(--muted);white-space:nowrap}
.mini{display:inline-block;width:92px;height:9px;background:#0B1C2C;border-radius:4px;vertical-align:middle;margin-left:6px}.mini i{display:block;height:100%;border-radius:4px}
.legend-row{display:flex;flex-wrap:wrap;gap:8px;font-size:.8em;margin-top:4px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px}
.frames.two{display:grid;grid-template-columns:1fr 1fr;gap:8px}.frames img{width:100%;border-radius:6px;border:1px solid var(--line)}.frames.zoom img{max-width:360px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:800px){.two-col,.frames.two{grid-template-columns:1fr}}
.mapwrap{position:relative;width:100%}.mapwrap img{width:100%;display:block;border-radius:8px}.mapwrap svg{position:absolute;inset:0;width:100%;height:100%}.mapwrap circle:hover{r:10}
.takeaways{margin:8px 0 20px}.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:end;margin:10px 0}.filters label{display:flex;flex-direction:column;font-size:.8em;color:var(--muted)}
select{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 6px}
table.smokes{width:100%;border-collapse:collapse;font-size:.9em}table.smokes th,table.smokes td{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}table.smokes img{width:56px;height:56px;object-fit:cover;border-radius:4px}
table.roster{width:100%;font-size:.9em}table.roster th{text-align:left;color:var(--muted)}
.clip video{width:100%;max-width:900px;border-radius:8px;background:#000}.clip-controls{margin:6px 0}.clip-controls button{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 10px;margin-right:6px;cursor:pointer}.clip-controls button.on{background:#F5C542;color:#07131f}
.smoke-nav{margin:20px 0;display:flex;gap:12px;flex-wrap:wrap}.takeaway{font-weight:600}.findings li{margin:6px 0}.noimg{background:var(--panel2);color:var(--muted);padding:30px;text-align:center;border-radius:6px}
"""

JS = r"""(function(){
  document.querySelectorAll('.clip').forEach(function(c){
    var v = c.querySelector('video');
    c.querySelectorAll('button.speed').forEach(function(b){
      b.addEventListener('click', function(){ v.playbackRate = parseFloat(b.dataset.rate); c.querySelectorAll('button.speed').forEach(function(x){x.classList.toggle('on', x===b);}); });
    });
    var first = c.querySelector('button.speed'); if (first) first.classList.add('on');
  });
  if (!window.SMOKES) return;
  var rows = window.SMOKES, tbody = document.querySelector('#smokes tbody');
  function fill(id, key){ var sel = document.getElementById(id); var vals = Array.from(new Set(rows.map(function(r){return r[key];}))).filter(Boolean).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', render); }
  fill('f-team','team'); fill('f-player','player'); fill('f-ship','ship'); fill('f-map','map'); fill('f-game','game'); fill('f-type','type');
  document.getElementById('f-sort').addEventListener('change', render);
  function val(id){ return document.getElementById(id).value; }
  function bar(v, max, color){ var w = max ? Math.max(0, Math.min(1, v/max))*80 : 0; return '<span class="mini"><i style="width:'+w.toFixed(0)+'px;background:'+color+'"></i></span>'; }
  function render(){
    var f = {team:val('f-team'), player:val('f-player'), ship:val('f-ship'), map:val('f-map'), game:val('f-game'), type:val('f-type')};
    var sort = val('f-sort');
    var list = rows.filter(function(r){ return Object.keys(f).every(function(k){ return !f[k] || r[k]===f[k]; }); });
    list.sort(function(a,b){ var x=a[sort], y=b[sort]; if (x==null) x = sort==='cap'? Infinity : -Infinity; if (y==null) y = sort==='cap'? Infinity : -Infinity; return sort==='cap' ? x-y : y-x; });
    tbody.innerHTML = list.map(function(r){
      var cap = r.cap==null ? '-' : ((r.cap<0?'-':'')+(Math.abs(r.cap)/1000).toFixed(1)+' km '+r.cap_name);
      var capBar = r.cap==null ? '' : bar(Math.max(0, 6000-Math.max(0,r.cap)), 6000, '#5DADE2');
      return '<tr><td>'+(r.thumb?'<a href="'+r.href+'"><img src="'+r.thumb+'" loading="lazy" alt=""></a>':'')+'</td>'+
        '<td><span class="tag" style="--c:'+r.color+'">'+r.team+'</span></td><td>'+r.player+'</td><td>'+r.ship+'</td><td>'+r.map+'</td>'+
        '<td class="small"><a href="'+r.game_href+'">'+r.game+'</a></td><td>'+r.clock+'</td>'+
        '<td>'+r.total.toLocaleString()+' '+bar(r.total, window.MAX_TOTAL, '#F5C542')+'<div class="small muted">in '+r.inside.toLocaleString()+' / behind '+r.behind.toLocaleString()+'</div></td>'+
        '<td>'+cap+' '+capBar+'</td><td>'+r.radar+'</td><td><a href="'+r.href+'">smoke</a>'+(r.selfish?' <span class="muted small">selfish</span>':'')+(r.flag?' <span class="warn small">flag</span>':'')+'</td></tr>';
    }).join('');
    document.getElementById('empty').hidden = list.length>0;
    document.getElementById('count').textContent = list.length + ' of ' + rows.length + ' smokes';
  }
  render();
})();"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--maps", required=True)
    ap.add_argument("--clips")
    ap.add_argument("--inventory", default="smoke/inventory.csv")
    ap.add_argument("--out", default="smoke-site")
    ap.add_argument("--colors", default="")
    args = ap.parse_args()
    data = Data(args.batch, args.maps, args.clips, args.inventory)
    site = Site(data, args.out, parse_colors(args.colors))
    site.build()
    total = 0
    largest = (0, "")
    for dp, _, fs in os.walk(args.out):
        for f in fs:
            size = os.path.getsize(os.path.join(dp, f))
            total += size
            largest = max(largest, (size, os.path.join(dp, f)))
    print(f"site written to {args.out}: {len(data.smokes)} smokes, {len(data.by_game)} games, {total / 1e6:.0f} MB, largest file {largest[0] / 1e6:.1f} MB ({largest[1]})")


if __name__ == "__main__":
    main()
