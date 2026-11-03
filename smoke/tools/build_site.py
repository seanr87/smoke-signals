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
GRID_LETTERS = "ABCDEFGHIJ"
SELFISH_DEF = "Selfish smoke: no teammate other than the owner was ever inside it, and no teammate fired through it from behind."
CONTEST_DEF = "A cap is contested for a team when it sits on the midline between the two spawns, lies on the enemy's side of the midline, or is held by the enemy."
REASON_TEXT = {"midline": "it sits on the midline between the spawns", "enemy_side": "it lies on the enemy's side of the midline", "enemy_owned": "the enemy held it"}
PLAYOFF_ROUNDS = ["WB Round 1", "WB Round 2", "WB Round 3", "WB Round 4", "LB Round 6", "GF Round 1"]
ROUND_TITLES = {"WB Round 1": "Winners round 1", "WB Round 2": "Winners round 2", "WB Round 3": "Winners round 3", "WB Round 4": "Winners final", "LB Round 6": "Losers final", "GF Round 1": "Grand final"}


def esc(s):
    return html.escape(str(s if s is not None else ""))


def term(text, title=SELFISH_DEF):
    """A term with its definition as a tooltip."""
    return f'<abbr class="term" title="{esc(title)}">{esc(text)}</abbr>'


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


def cap_short(s):
    """Short cap label for the diagram."""
    m = s.get("cap_proximity_m")
    if m is None:
        return ""
    name = s.get("cap_proximity_name") or "?"
    pct = s.get("cap_depth_pct")
    if m < 0 and pct is not None:
        return f"{pct:.0f}% of the way to the centre, {fmt_km(-m)} inside"
    return f"{fmt_km(m)} from the edge of cap {name}"


def cap_text(s):
    """One line on a smoke's cap proximity at capture: depth as a share of the cap radius when inside."""
    m = s.get("cap_proximity_m")
    if m is None:
        return "no cap proximity"
    name = s.get("cap_proximity_name") or "?"
    pct = s.get("cap_depth_pct")
    r = s.get("cap_radius_m")
    radius = f", cap radius {fmt_km(r)}" if r else ""
    if m < 0 and pct is not None:
        return f"{pct:.0f}% of the way to the centre of cap {name} ({fmt_km(-m)} inside the edge{radius})"
    if m < 0:
        return f"{fmt_km(-m)} inside cap {name}{radius}"
    return f"{fmt_km(m)} outside cap {name}{radius}"


def contested_text(s):
    """One line on the smoke's average distance to the nearest contested cap over its life."""
    d = s.get("avg_contested_cap_dist_m")
    if d is None:
        return "no cap was contested while it stood"
    name = s.get("contested_cap_name") or "?"
    why = REASON_TEXT.get(s.get("cap_contested_reason") or "", "")
    why = f", contested because {why}" if why else ""
    if d < 0:
        return f"on average {fmt_km(-d)} inside contested cap {name}{why}"
    return f"on average {fmt_km(d)} from the edge of contested cap {name}{why}"


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
        self.inventory_rows = []
        if inventory and os.path.exists(inventory):
            for r in csv.DictReader(open(inventory, encoding="utf-8")):
                self.inventory[(r["match_id"], int(r["game_no"]))] = r
                self.inventory_rows.append(r)
        self.maps = {}
        self.maps_dir = maps_dir
        self.map_titles = {}
        for m in json.load(open(os.path.join(maps_dir, "maps.json"), encoding="utf-8")):
            self.maps[m["map"]] = m
            if m.get("title"):
                self.map_titles[m["map"]] = m["title"]
        for s in self.smokes:
            if s.get("map_display"):
                self.map_titles[s["map"]] = s["map_display"]
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
            rem = clock_remaining_seconds(s["_act_clock"])
            s["_elapsed"] = (MATCH_SECONDS - rem) if rem is not None else None
        self.smokes.sort(key=lambda s: (s["_key"], s["_act_s"]))
        self.by_game = defaultdict(list)
        for s in self.smokes:
            self.by_game[s["_key"]].append(s)
        self.games_played = Counter()
        self.played_keys = set()
        for key, r in self.inventory.items():
            if r["status"] == "played":
                self.played_keys.add(key)
                for t in r["our_teams"].split(";"):
                    if t:
                        self.games_played[t] += 1
        if not self.games_played:
            for (m, g, t) in self.job_by_key:
                self.games_played[t] += 1
                self.played_keys.add((m, g))
        self.caps_by_map = {}
        for key, g in self.games.items():
            caps = g.get("caps") or []
            if not caps:
                continue
            have = self.caps_by_map.get(g["map"])
            if have is None:
                self.caps_by_map[g["map"]] = caps
            elif [(c["cap"], round(c["position"]["x"]), round(c["position"]["z"])) for c in caps] != [(c["cap"], round(c["position"]["x"]), round(c["position"]["z"])) for c in have]:
                print(f"warning: cap layout differs on {g['map']} in game {key}")

    def map_title(self, name):
        """In-game display name: from the records, then maps.json, then a fallback table."""
        return self.map_titles.get(name) or FALLBACK_MAP_TITLES.get(name) or name

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

    def spawn_sides_on(self, map_name):
        """Spawn side labels seen on a map, e.g. {north, south}."""
        sides = set()
        for g in self.games.values():
            if g["map"] == map_name:
                for t in g["teams"]:
                    if t.get("spawn_side"):
                        sides.add(t["spawn_side"])
        return sides


def map_px(data, map_name, x, z):
    m = data.maps.get(map_name)
    if not m:
        return None
    scale = NATIVE / m["space_size"]
    return (x * scale + NATIVE / 2, -z * scale + NATIVE / 2)


def thin(points, limit=80):
    if len(points) <= limit:
        return points
    step = (len(points) - 1) / (limit - 1)
    return [points[round(i * step)] for i in range(limit)]


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
        items = [("Home", "index.html"), ("Analysis", "analysis.html"), ("Awards", "awards.html"), ("Games", "games.html"), ("Maps", "maps.html"), ("All Smokes", "smokes.html")]
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

    def game_href(self, key, depth=0):
        """Link to a game page, or None when the game has no analysed smokes."""
        if key not in self.d.by_game:
            return None
        return f"{'../' * depth}games/{key[0]}_g{key[1]}.html"

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

    def img(self, s, field, depth, cls="", lazy=True):
        rel = (s.get("_img") or {}).get(field)
        if not rel:
            return '<div class="noimg">no frame</div>'
        return f'<img class="{cls}" src="{"../" * depth}{rel}" alt="{esc(field)}"{" loading=\"lazy\"" if lazy else ""}>'

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
        self.write(".nojekyll", "")
        self.home()
        self.analysis()
        self.awards()
        self.games_page()
        self.maps_page()
        self.all_smokes()
        for key in self.d.by_game:
            self.game_page(key)
        for i, s in enumerate(self.d.smokes):
            self.smoke_page(s)

    def home(self):
        d = self.d
        n_games = len(d.by_game)
        n_played = len(d.played_keys) or n_games
        cards = [
            ("Analysis", "analysis.html", "Top players, three headline findings and one card per team."),
            ("Awards", "awards.html", "The four smokes of the tournament, player awards and clan awards."),
            ("Games", "games.html", "The playoff bracket, series results and every group stage game."),
            ("Maps", "maps.html", "Every smoke's path on its map, with time, clan, spawn and ship filters."),
            ("All Smokes", "smokes.html", f"The table of all {len(d.smokes)} analysed smokes, with filters and sorting."),
        ]
        per_team = Counter(s["team"] for s in d.smokes)
        stats = "".join(f'<div class="stat" style="--c:{self.color(t)}"><b>{per_team[t]}</b><span>{esc(t)} smokes in {d.games_played.get(t, 0)} games</span></div>' for t in TEAMS if per_team.get(t))
        maps = len({s["map"] for s in d.smokes})
        games_text = f"{n_played} games ({n_games} with at least one smoke)" if n_played != n_games else f"{n_games} games"
        body = f"""<section class="briefing"><h1>Mission briefing</h1>
<p>We want to win games. This site breaks down how top competitive teams use smoke: {len(d.smokes)} smokes from {games_text} of King of the Sea XIX NA played by H-SR, RESIN and PN, read straight from the replays.</p>
<p class="muted">Every smoke has an activation frame, a capture frame, a zoomed close-up and its numbers. Purpose and intent tags come later by hand.</p></section>
<section class="stats"><div class="stat"><b>{len(d.smokes)}</b><span>smokes analysed</span></div><div class="stat"><b>{n_played}</b><span>games on {maps} maps ({n_games} with at least one smoke)</span></div>{stats}</section>
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
        max_smokes = max((p["smokes"] for _, p in top), default=1)
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
            selfish_share = sum(1 for s in d.smokes if s.get('selfish_smoke')) / total * 100
            out.append(f"{esc(hi)} laid the most smokes per game ({per_game[hi]:.1f}); {esc(lo)} the fewest ({per_game[lo]:.1f}). {term('Selfish smokes')} made up {selfish_share:.0f}% of all smokes.")
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
        types = Counter(s.get("smoke_type") or "unknown" for s in rows)
        type_parts = [(t, types[t]) for t, _ in SMOKE_TYPES if types.get(t)] + ([("unknown", types["unknown"])] if types.get("unknown") else [])
        types_bar = svg_stacked_bar(type_parts, [dict(SMOKE_TYPES).get(t, "#94A3B8") for t, _ in type_parts])
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
        selfish_pct = selfish / max(1, len(rows)) * 100
        takeaway = f"{esc(team)} smokes {when} and {where}; {selfish_pct:.0f}% of its smokes were {term('selfish')}."
        return f"""<div class="card team" style="--c:{self.color(team)}"><h3>{self.team_tag(team)} {esc(team)}</h3>
<table class="kv"><tr><td>Total smokes</td><td>{len(rows)}</td></tr><tr><td>Smokes per game</td><td>{len(rows) / games:.1f}</td></tr><tr><td>Smoke damage per game</td><td>{fmt_int(total_damage / games)}</td></tr></table>
<h4>Ships</h4>{donut}
<h4>Smoke types</h4>{types_bar}
<h4>Timing across the match clock</h4>{timing_bar}
<h4>Damage split</h4>{split}
<h4>Habits</h4><p class="small">{term('Selfish smokes')}: {selfish} of {len(rows)} ({selfish_pct:.0f}%)</p>{prox_bar}
<p class="takeaway">{takeaway}</p>
<p class="muted small">Purpose and intent are pending hand tags.</p></div>"""

    def award_card(self, title, s, note, big, detail, sub=""):
        """One smoke award: the capture close-up, the smoke's details, the clip and the folded frames."""
        d = self.d
        if not s:
            return f'<div class="card award"><h3>{esc(title)}</h3><p class="muted">Nothing here, just clear skies.</p></div>'
        clip = f'<div class="clip"><video controls preload="metadata" src="{s["_clip"]}"></video><div class="clip-controls"><button class="speed" data-rate="1">1x (5x real time)</button><button class="speed" data-rate="2">2x (10x real time)</button></div></div>' if s.get("_clip") else '<p class="muted small">Clip available on request.</p>'
        thumb = (s.get("_img") or {}).get("frame_cap_zoom") or (s.get("_img") or {}).get("frame_cap")
        href = self.smoke_href[s["_slug"]]
        hero = f'<a href="{href}"><img class="award-thumb" src="{thumb}" alt="capture frame close-up"></a>' if thumb else '<div class="noimg">no frame</div>'
        sub = f'<p class="muted small">{sub}</p>' if sub else ""
        note = f'<p class="note">{note}</p>' if note else ""
        return f"""<div class="card award"><h3>{esc(title)}</h3>{sub}{note}
<div class="award-hero">{hero}<div class="award-meta"><div>{self.team_tag(s['team'])} <b>{esc(s['player'])}</b> <span class="muted">{esc(s['ship'])}</span></div>
<div class="muted small">{esc(s['_games_label'])}</div><div class="muted small">{esc(d.map_title(s['map']))}, activated {esc(s['_act_clock'])}</div>
<div class="big">{big}</div><div class="small">{detail}</div>
<p><a href="{href}">Open the smoke page</a></p></div></div>
{clip}
<details><summary>Activation and capture frames</summary><div class="frames two">{self.img(s, 'frame_act', 0)}{self.img(s, 'frame_cap', 0)}</div></details></div>"""

    def deepest_cap_smoke(self):
        """Lowest average distance to a contested cap, among smokes that did damage or saw their team take or defend a cap."""
        eligible = [s for s in self.d.smokes if s.get("avg_contested_cap_dist_m") is not None and (s["_total"] > 0 or s.get("cap_captured_or_held"))]
        if not eligible:
            return None
        return min(eligible, key=lambda s: (s["avg_contested_cap_dist_m"], -s["_total"]))

    def awards(self):
        d = self.d
        rows = d.smokes
        if not rows:
            return
        best = max(rows, key=lambda s: s["_total"])
        deep = self.deepest_cap_smoke()
        bait = max(rows, key=lambda s: (s["_radar"], s["_total"]))
        selfish = [s for s in rows if s.get("selfish_smoke")]
        most_selfish = max(selfish, key=lambda s: s["_owner_damage"]) if selfish else None
        type_line = lambda s: f"{esc(s.get('smoke_type') or '')} smoke"
        blocks = [
            self.award_card("Smoke of the Tournament", best, f"{fmt_int(best['_total'])} smoke damage", f"{fmt_int(best['_total'])} smoke damage", f"{type_line(best)} | {esc(cap_text(best))}", "Highest smoke damage"),
            self.award_card("Deepest Cap Smoke", deep, esc(contested_text(deep)[0].upper() + contested_text(deep)[1:]) if deep else "", f"{fmt_int(deep['_total'])} smoke damage" if deep else "",
                            (f"{type_line(deep)} | " + (f"the team took or defended a cap while it stood" if deep.get("cap_captured_or_held") else "no cap changed hands while it stood")) if deep else "",
                            f"Lowest average distance to a {term('contested cap', CONTEST_DEF)} over the smoke's life, among smokes that did damage or saw their team take or defend a cap"),
            self.award_card("Radar Bait", bait, f"{bait['_radar']} radar spots on allies in the smoke", f"{fmt_int(bait['_total'])} smoke damage", f"{type_line(bait)} | {esc(cap_text(bait))}", "Most enemy radar spots on allies inside the smoke"),
            self.award_card("Most Selfish Smoke", most_selfish, "", f"{fmt_int(most_selfish['_owner_damage'])} damage by the smoker (no teammate benefited)" if most_selfish else "",
                            f"{type_line(most_selfish)} | {esc(cap_text(most_selfish))}" if most_selfish else "", f"The {term('selfish smoke')} with the most damage by its owner"),
        ]
        players = self.player_stats()
        def top_by(key, minimum=0):
            items = [(n, p) for n, p in players.items() if p["smokes"] >= minimum]
            return max(items, key=lambda kv: key(kv[1])) if items else None
        golden = top_by(lambda p: p["damage"])
        father = top_by(lambda p: p["smokes"])
        haze = top_by(lambda p: p["damage"] / p["smokes"], minimum=5)
        selfish_p = top_by(lambda p: p["selfish"])
        player_awards = [
            ("Golden Cloud", "Most total smoke damage", golden, lambda p: f"{fmt_int(p['damage'])} damage over {p['smokes']} smokes"),
            ("The Smokefather", "Most smokes laid", father, lambda p: f"{p['smokes']} smokes in {len(p['games'])} games"),
            ("Best in Haze", "Highest average smoke damage per smoke (minimum 5 smokes)", haze, lambda p: f"{fmt_int(p['damage'] / p['smokes'])} per smoke over {p['smokes']} smokes"),
            ("Most Selfish Smoker", f"Most {term('selfish smokes')}", selfish_p, lambda p: f"{p['selfish']} selfish smokes of {p['smokes']}"),
        ]
        pcards = "".join(
            f'<div class="card award-p"><h3>{esc(t)}</h3><p class="muted small">{sub}</p><p>{self.team_tag(w[1]["team"])} <b>{esc(w[0])}</b></p><p class="note">{esc(fmt(w[1]))}</p></div>' if w else f'<div class="card award-p"><h3>{esc(t)}</h3><p class="muted">Nothing here, just clear skies.</p></div>'
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
            return f'<div class="card award-p"><h3>{title}</h3><p>{self.team_tag(w[0])} <b>{esc(w[0])}</b></p><p class="note">{esc(fmt(w[idx]))} per game over {w[4]} games</p></div>'
        ccards = clan_award("Most smokes laid", 1, lambda v: f"{v:.1f} smokes") + clan_award("Most smoke damage", 2, lambda v: f"{fmt_int(v)} damage") + clan_award(f"Most {term('selfish smokes')}", 3, lambda v: f"{v:.1f} selfish smokes")
        body = f"""<h1>Awards</h1>
<p class="muted"><b>Selfish smoke:</b> no teammate other than the owner was ever inside it, and no teammate fired through it from behind. <b>Contested cap:</b> a cap is contested for a team when it sits on the midline between the two spawns, lies on the enemy's side of the midline, or is held by the enemy.</p>
<h2>Smoke awards</h2><section class="cards awards">{"".join(blocks)}</section>
<h2>Player awards</h2><section class="cards">{pcards}</section>
<h2>Clan awards (per game played)</h2><section class="cards">{ccards}</section>"""
        self.write("awards.html", self.page("Awards", body, active="Awards"))

    def map_figure(self, map_name, smokes, depth=0, size=768, anchor_prefix="smoke", fig_id="map"):
        """The minimap with the grid, the caps and one path per smoke, puffs in laying order, an arrow at the end."""
        d = self.d
        m = d.maps.get(map_name)
        base = "../" * depth
        if not m:
            return '<p class="muted">Map image missing.</p>'
        step = NATIVE / 10
        grid = []
        for i in range(1, 10):
            grid.append(f'<line x1="{i * step:.0f}" y1="0" x2="{i * step:.0f}" y2="{NATIVE}"/><line x1="0" y1="{i * step:.0f}" x2="{NATIVE}" y2="{i * step:.0f}"/>')
        labels = "".join(f'<text x="{(i + 0.5) * step:.0f}" y="14">{GRID_LETTERS[i]}</text><text x="6" y="{(i + 0.5) * step + 4:.0f}" text-anchor="start">{i + 1}</text>' for i in range(10))
        caps = []
        for c in d.caps_by_map.get(map_name, []):
            px = map_px(d, map_name, c["position"]["x"], c["position"]["z"])
            r = c["radius"] * NATIVE / m["space_size"]
            caps.append(f'<circle cx="{px[0]:.1f}" cy="{px[1]:.1f}" r="{r:.1f}"/><text x="{px[0]:.1f}" y="{px[1] + 7:.1f}" class="caplabel">{esc(c["cap"])}</text>')
        markers = "".join(f'<marker id="{fig_id}-arrow-{t.lower().replace("-", "")}" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="4" markerHeight="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 z" fill="{self.color(t)}"/></marker>' for t in TEAMS)
        paths = []
        for s in smokes:
            pts = [map_px(d, map_name, p["x"], p["z"]) for p in thin(s.get("path") or [s["origin_xy"]])]
            pts = [p for p in pts if p]
            if not pts:
                continue
            if len(pts) == 1:
                pts = pts * 2
            dashed = ' stroke-dasharray="6,4"' if s.get("smoke_type") in ("exhaust", "crawling") else ""
            marker = f"{fig_id}-arrow-{s['team'].lower().replace('-', '')}"
            points = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            elapsed = s["_elapsed"] if s["_elapsed"] is not None else -1
            contested = s.get("avg_contested_cap_dist_m")
            data = f'data-team="{esc(s["team"])}" data-spawn="{esc(s.get("spawn_side") or "")}" data-ship="{esc(s["ship"])}" data-t="{elapsed}" data-dmg="{round(s["_total"])}" data-contested="{"" if contested is None else round(contested)}" data-selfish="{"1" if s.get("selfish_smoke") else ("0" if s.get("selfish_smoke") is not None else "")}"'
            title = f'{s["player"]} {s["ship"]} at {s["_act_clock"]}, {fmt_int(s["_total"])} dmg, {s.get("smoke_type") or ""} smoke'
            paths.append(f'<a href="{base}{self.smoke_href[s["_slug"]]}" id="{anchor_prefix}-{s["_slug"]}" class="smokepath" {data}><polyline points="{points}" stroke="{self.color(s["team"])}"{dashed} marker-end="url(#{marker})"><title>{esc(title)}</title></polyline></a>')
        return f'<div class="mapwrap" style="max-width:{size}px"><img src="{base}maps/{m["map"]}.webp" alt="{esc(self.d.map_title(map_name))}"><svg viewBox="0 0 {NATIVE} {NATIVE}"><defs>{markers}</defs><g class="grid">{"".join(grid)}</g><g class="gridlabels">{labels}</g><g class="caps">{"".join(caps)}</g><g class="paths">{"".join(paths)}</g></svg></div>'

    def maps_page(self):
        d = self.d
        sections = []
        by_map = defaultdict(list)
        for s in d.smokes:
            by_map[s["map"]].append(s)
        for n, (map_name, smokes) in enumerate(sorted(by_map.items(), key=lambda kv: -len(kv[1]))):
            counts = Counter(s["team"] for s in smokes)
            prox = [s["cap_proximity_m"] for s in smokes if s.get("cap_proximity_m") is not None]
            near = sum(1 for p in prox if p <= 1000)
            games = len({s["_key"] for s in smokes})
            take = [
                f"{len(smokes)} smokes in {games} games: " + ", ".join(f"{t} {n}" for t, n in counts.most_common()) + ".",
                f"{near / max(1, len(prox)) * 100:.0f}% went up within 1 km of a cap edge." if prox else "",
                f"Average smoke damage {fmt_int(sum(s['_total'] for s in smokes) / len(smokes))}.",
            ]
            sides = d.spawn_sides_on(map_name)
            if sides & {"east", "west"}:
                spawn_opts = [("east", "East spawn"), ("west", "West spawn")]
                spawn_note = " (this map spawns east and west)"
            else:
                spawn_opts = [("north", "North spawn"), ("south", "South spawn")]
                spawn_note = ""
            clans = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in TEAMS if counts.get(t))
            ships = "".join(f'<option value="{esc(sh)}">{esc(sh)}</option>' for sh in sorted({s["ship"] for s in smokes}))
            spawns = "".join(f'<option value="{v}">{l}</option>' for v, l in spawn_opts)
            fig = self.map_figure(map_name, smokes, fig_id=f"m{n}")
            filters = f"""<div class="filters mapfilters">
<label class="range">Battle clock <span class="rangevals"><b class="lo">20:00</b> to <b class="hi">0:00</b></span><span class="dual"><input type="range" class="t-lo" min="0" max="{MATCH_SECONDS}" value="0" step="10"><input type="range" class="t-hi" min="0" max="{MATCH_SECONDS}" value="{MATCH_SECONDS}" step="10"></span><span class="muted small">smokes activated between the two handles; battle start on the left</span></label>
<label>Clan <select class="f-clan"><option value="">all</option>{clans}</select></label>
<label>Spawn{spawn_note} <select class="f-spawn"><option value="">both</option>{spawns}</select></label>
<label>Ship <select class="f-ship"><option value="">all</option>{ships}</select></label>
<span class="count muted"></span></div>"""
            sections.append(f'<section class="map-section" data-map="{esc(map_name)}"><h2>{esc(self.d.map_title(map_name))}</h2>{filters}<div class="two-col mapcol">{fig}<div><h3>By clan, for the smokes shown</h3><div class="chart"></div></div></div><ul class="takeaways">{"".join(f"<li>{esc(t)}</li>" for t in take if t)}</ul></section>')
        legend = "".join(f'<span class="legend"><i style="background:{self.color(t)}"></i>{esc(t)}</span>' for t in TEAMS if any(s["team"] == t for s in d.smokes))
        body = f"""<h1>Maps</h1><p class="muted">One line per smoke: its puffs in laying order with an arrow at the end, coloured by team. Exhaust and crawling smokes are dashed. Circles are the capture zones. Click a line to open the smoke. The filters apply to the map and its chart.</p><div class="legend-row">{legend}<span class="legend"><i style="background:#CBD5E1"></i>standard and cruiser smoke: solid</span><span class="legend"><i style="background:#CBD5E1;opacity:.5"></i>exhaust and crawling: dashed</span></div>{''.join(sections)}
<script>window.TEAM_COLORS = {json.dumps(self.colors)}; window.SELFISH_DEF = {json.dumps(SELFISH_DEF)}; window.CONTEST_DEF = {json.dumps(CONTEST_DEF)};</script>"""
        self.write("maps.html", self.page("Maps", body, active="Maps"))

    def series(self):
        """Playoff series from the inventory: match id, round, teams, games in order."""
        out = {}
        for r in self.d.inventory_rows:
            if r["stage"] != "Playoffs":
                continue
            s = out.setdefault(r["match_id"], {"match_id": r["match_id"], "round": r["round"], "bracket": r["group"], "teams": [t.strip() for t in r["teams"].split(" vs ")], "date": r["date"], "games": []})
            s["games"].append(r)
        for s in out.values():
            s["games"].sort(key=lambda r: int(r["game_no"]))
            wins = Counter(r["winner"] for r in s["games"] if r["status"] == "played" and r["winner"])
            s["wins"] = [wins.get(t, 0) for t in s["teams"]]
            s["winner"] = max(s["teams"], key=lambda t: wins.get(t, 0)) if wins else None
        return out

    def series_box(self, s, depth=0):
        href = f"{'../' * depth}games/series_{s['match_id']}.html"
        rows = ""
        for t, w in zip(s["teams"], s["wins"]):
            tag = self.team_tag(t) if t in self.colors else f'<span class="tag other">{esc(t)}</span>'
            rows += f'<div class="srow{" won" if t == s["winner"] else ""}">{tag} <span class="sname">{esc(t)}</span><b>{w}</b></div>'
        return f'<a class="series" href="{href}">{rows}<div class="muted small">{esc(s["date"])}</div></a>'

    def games_page(self):
        d = self.d
        series = self.series()
        cols = []
        for rnd in PLAYOFF_ROUNDS:
            items = sorted((s for s in series.values() if s["round"] == rnd), key=lambda s: s["match_id"])
            if items:
                cols.append(f'<div class="bcol"><h3>{esc(ROUND_TITLES.get(rnd, rnd))}</h3>{"".join(self.series_box(s) for s in items)}</div>')
        bracket = f'<div class="bracket">{"".join(cols)}</div>' if cols else '<p class="muted">No playoff series in the inventory.</p>'
        group_rows = []
        for r in sorted(d.inventory_rows, key=lambda r: (r["group"], int(r["round"].split()[-1]) if r["round"].split()[-1].isdigit() else 0, int(r["game_no"]))):
            if r["stage"] != "Groups" or r["status"] == "bye":
                continue
            key = (r["match_id"], int(r["game_no"]))
            href = self.game_href(key)
            teams = [t.strip() for t in r["teams"].split(" vs ")]
            tags = " vs ".join(self.team_tag(t) + " " + esc(t) if t in self.colors else esc(t) for t in teams)
            link = f'<a href="{href}">smokes</a>' if href else ('<span class="muted">no smokes</span>' if r["status"] == "played" else '<span class="muted">not played</span>')
            clans = ";".join(t for t in teams if t in self.colors)
            group_rows.append(f'<tr data-clan="{esc(clans)}" data-map="{esc(r["map"])}"><td>{esc(r["group"])} {esc(r["round"])}</td><td>{esc(r["date"])}</td><td>{tags}</td><td>{esc(r["map"])}</td><td>{esc(r["score"])}</td><td>{esc(r["winner"])}</td><td>{link}</td></tr>')
        maps = sorted({r["map"] for r in d.inventory_rows if r["stage"] == "Groups" and r["status"] != "bye"})
        map_opts = "".join(f'<option value="{esc(m)}">{esc(m)}</option>' for m in maps)
        clan_opts = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in TEAMS)
        body = f"""<h1>Games</h1>
<h2>Playoffs</h2><p class="muted">Each box is a series; the numbers are games won. Click a series for its games. Only series with H-SR or RESIN in them are in the replay set, so the other series of the bracket are not shown.</p>
{bracket}
<h2>Group stage</h2>
<div class="filters"><label>Clan <select id="g-clan"><option value="">all</option>{clan_opts}</select></label><label>Map <select id="g-map"><option value="">all</option>{map_opts}</select></label><span id="g-count" class="muted"></span></div>
<table class="games" id="games"><thead><tr><th>Round</th><th>Date</th><th>Teams</th><th>Map</th><th>Score</th><th>Winner</th><th></th></tr></thead><tbody>{"".join(group_rows)}</tbody></table>
<p id="g-empty" class="muted" hidden>Nothing here, just clear skies.</p>"""
        self.write("games.html", self.page("Games", body, active="Games"))
        for s in series.values():
            self.series_page(s)

    def series_page(self, s):
        d = self.d
        rows = []
        for r in s["games"]:
            key = (r["match_id"], int(r["game_no"]))
            href = self.game_href(key, depth=1)
            n_smokes = len(d.by_game.get(key, []))
            link = f'<a href="{href}">game page ({n_smokes} smokes)</a>' if href else ('<span class="muted">no smokes</span>' if r["status"] == "played" else '<span class="muted">not played</span>')
            winner = self.team_tag(r["winner"]) + " " + esc(r["winner"]) if r["winner"] in self.colors else esc(r["winner"] or "-")
            rows.append(f'<tr><td>Game {esc(r["game_no"])}</td><td>{esc(r["map"])}</td><td>{esc(r["score"] or "-")}</td><td>{winner}</td><td>{link}</td></tr>')
        result = f"{esc(s['winner'])} won {max(s['wins'])}-{min(s['wins'])}" if s["winner"] else "no result"
        title = f"{' vs '.join(s['teams'])}, {ROUND_TITLES.get(s['round'], s['round'])}"
        body = f"""<h1>{esc(title)}</h1><p class="muted">{esc(s['bracket'])} | {esc(s['date'])} | {result}</p>
{self.series_box(s, depth=1)}
<table class="games"><thead><tr><th>Game</th><th>Map</th><th>Score</th><th>Winner</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table>
<p><a href="../games.html">Back to the bracket</a></p>"""
        self.write(f"games/series_{s['match_id']}.html", self.page(title, body, depth=1, active="Games"))

    def all_smokes(self):
        d = self.d
        records = []
        for s in d.smokes:
            thumb = (s.get("_img") or {}).get("frame_cap_zoom") or ""
            records.append({
                "id": s["smoke_id"], "team": s["team"], "player": s["player"], "ship": s["ship"], "map": self.d.map_title(s["map"]),
                "game": s["_games_label"], "game_href": f"games/{s['_match']}_g{s['game_no']}.html", "type": s.get("smoke_type") or "",
                "clock": s["_act_clock"], "total": round(s["_total"]), "inside": round(s["_in"]), "behind": round(s["_behind"]),
                "radar": s["_radar"], "duration": round(s["_duration"]) if s.get("_duration") is not None else None,
                "swing": s["_score_swing"], "cap": s.get("cap_proximity_m"), "cap_name": s.get("cap_proximity_name") or "", "depth": s.get("cap_depth_pct"),
                "contested": s.get("avg_contested_cap_dist_m"), "contested_name": s.get("contested_cap_name") or "",
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
<label>Sort <select id="f-sort"><option value="total">smoke damage (total)</option><option value="inside">damage in smoke</option><option value="behind">damage behind smoke</option><option value="radar">radar spots in smoke</option><option value="duration">duration</option><option value="swing">score change during the smoke</option><option value="depth">cap depth (share of cap radius)</option><option value="cap">cap proximity (nearest first)</option><option value="contested">average distance to a contested cap (nearest first)</option></select></label>
<span id="count" class="muted"></span></div>
<table class="smokes" id="smokes"><thead><tr><th></th><th>Team</th><th>Player</th><th>Ship</th><th>Map</th><th>Game</th><th>Clock</th><th>Damage</th><th>Cap (depth or distance)</th><th><abbr class="term" title="{esc(CONTEST_DEF)}">Contested cap</abbr> (average)</th><th>Radar</th><th></th></tr></thead><tbody></tbody></table>
<p id="empty" class="muted" hidden>Nothing here, just clear skies.</p>
<script>window.SMOKES = {json.dumps(records)}; window.MAX_TOTAL = {max_total}; window.SELFISH_DEF = {json.dumps(SELFISH_DEF)};</script>"""
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
            header.append(f"Game {inv['game_no']} on {self.d.map_title(smokes[0]['map'])}, {inv['date']}")
            header.append(f"Score {inv['score']}, winner {inv['winner']}")
        if g:
            header.append(f"Ended by {g.get('finish_type') or '?'} at {(g.get('battle_end') or {}).get('clock', '?')}")
        links = [f'<a href="../games.html">all games</a>']
        if inv and inv["stage"] == "Playoffs":
            links.append(f'<a href="series_{inv["match_id"]}.html">this series</a>')
        roster = ""
        for t in teams:
            rows = "".join(f"<tr><td>{esc(p['player'])}</td><td>{esc(p['ship'])}</td><td>{p['smoke_activations'] or ''}</td></tr>" for p in t["players"])
            roster += f'<div class="card"><h3>{self.team_tag(t["name"])} {esc(t["name"])} <span class="muted small">{esc(t.get("spawn_side") or "")} spawn</span></h3><table class="roster"><tr><th>Player</th><th>Ship</th><th>Smokes</th></tr>{rows}</table></div>'
        timeline = self.timeline_svg(smokes)
        score = self.score_svg(smokes, teams)
        cards = "".join(self.smoke_card(s, depth=1) for s in smokes)
        body = f"""<h1>{esc(smokes[0]['_games_label'])}</h1><p class="muted">{" | ".join(esc(h) for h in header)} | {" | ".join(links)}</p>
<section class="two-col">{self.map_figure(smokes[0]['map'], smokes, depth=1, size=480, anchor_prefix='g', fig_id='g')}<div><h2>Smokes across the match</h2>{timeline}<h2>Score with smoke markers</h2>{score}</div></section>
<h2>Rosters</h2><section class="cards rosters">{roster}</section>
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
        cap_r = s.get("cap_radius_m") or 4000
        scale = (w - 40) / (2 * cap_r + max(0, m) + 2 * smoke_r)
        cx = 20 + cap_r * scale
        sx = cx + (cap_r + m + smoke_r) * scale
        return f"""<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" class="capdiag"><circle cx="{cx:.0f}" cy="{h / 2}" r="{cap_r * scale:.0f}" fill="none" stroke="#5DADE2" stroke-dasharray="4,3"/><text x="{cx:.0f}" y="{h / 2 + 4}" fill="#5DADE2" font-size="12" text-anchor="middle">cap {esc(s.get('cap_proximity_name') or '')}</text>
<circle cx="{sx:.0f}" cy="{h / 2}" r="{max(4, smoke_r * scale):.0f}" fill="#CBD5E1" opacity="0.8"/><text x="{sx:.0f}" y="{h / 2 - 12}" fill="#E2E8F0" font-size="11" text-anchor="middle">smoke</text>
<text x="{w / 2}" y="{h - 4}" fill="#94A3B8" font-size="11" text-anchor="middle">{esc(cap_short(s))}</text></svg>"""

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
        nav.append(f'<a href="../maps.html#smoke-{s["_slug"]}">its path on the map</a>')
        if next_s:
            nav.append(f'<a href="{next_s["_slug"]}.html">next smoke in this game &rarr;</a>')
        flag = f'<p class="warn">Owner attribution flagged: {esc(s.get("owner_note"))}</p>' if s.get("owner_flag") else ""
        dur = f"{s['_duration']:.0f} s" if s.get("_duration") is not None else "still standing at the end"
        selfish = 'yes' if s.get('selfish_smoke') else ('no' if s.get('selfish_smoke') is not None else 'unknown')
        held = s.get("cap_captured_or_held")
        held_text = "yes" if held else ("no" if held is not None else "unknown")
        body = f"""<h1>{self.team_tag(s['team'])} {esc(s['player'])} <span class="muted">{esc(s['ship'])}</span></h1>
<p class="muted">{esc(self.d.map_title(s['map']))} | {esc(s['_games_label'])} | activated {esc(s['_act_clock'])}, captured {esc(s['_cap_clock'])} | {esc(s.get('smoke_type') or '')} smoke {esc(s.get('variant') or '')}</p>
<p class="big">{fmt_int(s['_total'])} smoke damage</p>{flag}
<section class="frames two">{self.img(s, 'frame_act', 1, lazy=False)}{self.img(s, 'frame_cap', 1, lazy=False)}</section>
<section class="frames two zoom">{self.img(s, 'frame_act_zoom', 1, lazy=False)}{self.img(s, 'frame_cap_zoom', 1, lazy=False)}</section>
{clip}
<section class="two-col"><div class="card"><h3>Stats</h3><table class="kv">
<tr><td>Duration</td><td>{esc(dur)}</td></tr>
<tr><td>Smoke damage</td><td>{split}</td></tr>
<tr><td>Radar spots in smoke</td><td>{s['_radar']}</td></tr>
<tr><td>Cap at capture</td><td>{esc(cap_text(s))}</td></tr>
<tr><td>{term('Contested cap', CONTEST_DEF)}</td><td>{esc(contested_text(s))}</td></tr>
<tr><td>Team took or defended a cap while it stood</td><td>{held_text}</td></tr>
<tr><td>Allies in smoke at capture</td><td>{esc(', '.join(s.get('allies_in_smoke') or [])) or 'none'}</td></tr>
<tr><td>{term('Selfish smoke')}</td><td>{selfish}</td></tr>
<tr><td>Score at capture</td><td>{esc(st.get('score_ours', '-'))} : {esc(st.get('score_theirs', '-'))}</td></tr>
<tr><td>Ships alive at capture</td><td>{esc(alive) or '-'}</td></tr></table></div>
<div class="card"><h3>Cap proximity at capture</h3>{self.cap_diagram(s)}<h3>Tags</h3><p class="muted">untagged</p></div></section>
<nav class="smoke-nav">{" | ".join(nav)}</nav>"""
        self.write(f"smokes/{s['_slug']}.html", self.page(f"{s['player']} {s['ship']} {s['_act_clock']}", body, depth=1))


FALLBACK_MAP_TITLES = {"16_OC_bees_to_honey": "Hotspot", "45_Zigzag": "Loop", "40_Okinawa": "Okinawa", "22_tierra_del_fuego": "Land of Fire", "58_RidgeNew": "Mountain Range", "47_Sleeping_Giant": "Sleeping Giant", "25_sea_hope": "Sea of Fortune"}
SMOKE_TYPES = [("standard", "#CBD5E1"), ("cruiser", "#6EE7B7"), ("exhaust", "#FB923C"), ("crawling", "#F472B6")]


CSS = """:root{--bg:#0B1C2C;--panel:#16283A;--panel2:#1E3448;--text:#EEF2F5;--muted:#9FB0C0;--line:#2A4258;__TEAMCOLORS__}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 "Segoe UI",system-ui,sans-serif}
main{max-width:1180px;margin:0 auto;padding:16px}h1,h2,h3,h4{margin:.6em 0 .3em}h1{font-size:1.7em}h2{font-size:1.25em;border-bottom:1px solid var(--line);padding-bottom:4px}
a{color:#9CD3FF}nav.top{display:flex;gap:4px;align-items:center;background:#07131f;padding:8px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
nav.top .brand{font-weight:700;letter-spacing:.04em;margin-right:12px;color:#F5C542}nav.top a{padding:6px 10px;border-radius:6px;color:var(--text);text-decoration:none}nav.top a.active,nav.top a:hover{background:var(--panel2)}
footer{color:var(--muted);font-size:.85em;text-align:center;padding:24px 16px}
abbr.term{text-decoration:underline dotted;cursor:help}
.briefing{background:var(--panel);border-left:6px solid #F5C542;padding:16px 20px;border-radius:8px;margin:16px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin:8px 0 20px}.cards.teams{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}.cards.awards{grid-template-columns:repeat(auto-fill,minmax(520px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px;color:var(--text);text-decoration:none;display:block}.card.toc h2{border:0;margin-top:0}.card.team{border-top:4px solid var(--c)}
.smoke-card{padding:0;overflow:hidden}.smoke-card img{width:100%;display:block;aspect-ratio:1;object-fit:cover}.card-body{padding:8px 10px}
.award-hero{display:flex;gap:14px;align-items:flex-start;margin:8px 0}.award-hero>a{flex:0 0 300px;max-width:48%}.award-thumb{width:100%;height:auto;display:block;border-radius:8px;border:1px solid var(--line)}.award-meta{flex:1;min-width:0}.award-meta .big{margin:6px 0}
.card.award .clip{margin-top:8px}.card.award details{margin-top:8px}.card.award summary{cursor:pointer;color:var(--muted);font-size:.9em}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 20px}.stat{background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--c,#9FB0C0);border-radius:8px;padding:8px 14px;min-width:150px}.stat b{display:block;font-size:1.5em}.stat span{color:var(--muted);font-size:.85em}
.tag{display:inline-block;padding:1px 7px;border-radius:999px;font-size:.78em;font-weight:700;background:var(--c);color:#07131f}.tag.other{background:#475569;color:var(--text)}
.muted{color:var(--muted)}.small{font-size:.85em}.big{font-size:1.4em;font-weight:700}.note{color:#F5C542}.warn{color:#FB923C}
table.kv td{padding:3px 8px 3px 0;vertical-align:top}table.kv td:first-child{color:var(--muted);white-space:nowrap}
.mini{display:inline-block;width:92px;height:9px;background:#0B1C2C;border-radius:4px;vertical-align:middle;margin-left:6px}.mini i{display:block;height:100%;border-radius:4px}
.legend-row{display:flex;flex-wrap:wrap;gap:8px;font-size:.8em;margin-top:4px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px}
.frames.two{display:grid;grid-template-columns:1fr 1fr;gap:8px}.frames img{width:100%;border-radius:6px;border:1px solid var(--line)}.frames.zoom img{max-width:360px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:800px){.two-col,.frames.two{grid-template-columns:1fr}.award-hero{flex-direction:column}.award-hero>a{flex:none;max-width:100%}.cards.awards{grid-template-columns:1fr}}
.mapwrap{position:relative;width:100%}.mapwrap img{width:100%;display:block;border-radius:8px}.mapwrap svg{position:absolute;inset:0;width:100%;height:100%}
.mapwrap .grid line{stroke:#fff;stroke-opacity:.18;stroke-width:1}.mapwrap .gridlabels text{fill:#fff;fill-opacity:.7;font-size:12px;text-anchor:middle;font-weight:600}
.mapwrap .caps circle{fill:#fff;fill-opacity:.08;stroke:#fff;stroke-opacity:.6;stroke-width:1.5;stroke-dasharray:5,4}.mapwrap .caplabel{fill:#fff;fill-opacity:.85;font-size:20px;font-weight:700;text-anchor:middle}
.mapwrap .smokepath polyline{fill:none;stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round;opacity:.9}.mapwrap .smokepath:hover polyline{stroke-width:6;opacity:1}.mapwrap .smokepath[hidden]{display:none}
.mapcol{grid-template-columns:3fr 2fr}.chart{display:grid;gap:10px}.chart .panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px}.chart h4{margin:0 0 4px;font-size:.9em;color:var(--muted)}
.chart .row{display:grid;grid-template-columns:52px 1fr 70px;align-items:center;gap:6px;font-size:.85em;margin:2px 0}.chart .row .bar{position:relative;height:12px;background:#0B1C2C;border-radius:3px}.chart .row .bar i{position:absolute;top:0;height:100%;border-radius:3px}.chart .row .bar b{position:absolute;top:-2px;bottom:-2px;width:1px;background:#94A3B8}.chart .row span:last-child{text-align:right}
.filters.mapfilters{align-items:flex-start}.range{min-width:320px}.rangevals{margin-left:6px}.dual{position:relative;display:block;height:22px}.dual input[type=range]{position:absolute;left:0;top:0;width:100%;margin:0;background:none;pointer-events:none;-webkit-appearance:none;appearance:none;height:22px}
.dual input[type=range]::-webkit-slider-runnable-track{height:4px;background:var(--line);border-radius:2px}.dual input.t-lo::-webkit-slider-runnable-track{background:linear-gradient(to right,var(--line),var(--line))}
.dual input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;pointer-events:auto;width:16px;height:16px;border-radius:50%;background:#F5C542;border:2px solid #07131f;margin-top:-6px;cursor:pointer}
.dual input[type=range]::-moz-range-track{height:4px;background:var(--line)}.dual input[type=range]::-moz-range-thumb{pointer-events:auto;width:14px;height:14px;border-radius:50%;background:#F5C542;border:2px solid #07131f;cursor:pointer}
.bracket{display:flex;gap:10px;overflow-x:auto;padding:4px 0 12px}.bcol{display:flex;flex-direction:column;justify-content:space-around;gap:10px;flex:1 1 0;min-width:170px}.srow .sname{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bcol h3{margin:0;font-size:.9em;color:var(--muted);text-align:center}
a.series{display:block;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px;color:var(--text);text-decoration:none}a.series:hover{border-color:#9CD3FF}.srow{display:flex;align-items:center;gap:6px;padding:2px 0}.srow .sname{flex:1}.srow.won{font-weight:700}.srow.won b{color:#F5C542}
table.games{width:100%;border-collapse:collapse;font-size:.9em}table.games th,table.games td{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left}table.games tr[hidden]{display:none}
.takeaways{margin:8px 0 20px}.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:end;margin:10px 0}.filters label{display:flex;flex-direction:column;font-size:.8em;color:var(--muted)}
select{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 6px}
table.smokes{width:100%;border-collapse:collapse;font-size:.9em}table.smokes th,table.smokes td{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}table.smokes img{width:56px;height:56px;object-fit:cover;border-radius:4px}
.cards.rosters{grid-template-columns:repeat(auto-fit,minmax(380px,1fr))}table.roster{width:100%;font-size:.85em;border-collapse:collapse}table.roster th{text-align:left;color:var(--muted)}table.roster td,table.roster th{padding:2px 6px 2px 0}table.roster td:last-child{text-align:right}
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
  function clockText(elapsed){ var rem = 1200 - elapsed; var m = Math.floor(rem/60), s = rem%60; return m + ':' + (s<10?'0':'') + s; }
  function fmt(n){ return Math.round(n).toLocaleString(); }

  // Maps page: filters per map section and a by-clan chart of the smokes shown.
  document.querySelectorAll('.map-section').forEach(function(sec){
    var paths = Array.from(sec.querySelectorAll('a.smokepath'));
    var lo = sec.querySelector('.t-lo'), hi = sec.querySelector('.t-hi');
    var clan = sec.querySelector('.f-clan'), spawn = sec.querySelector('.f-spawn'), ship = sec.querySelector('.f-ship');
    var chart = sec.querySelector('.chart'), count = sec.querySelector('.count');
    function shown(p){
      var t = parseInt(p.dataset.t, 10);
      if (t >= 0 && (t < parseInt(lo.value,10) || t > parseInt(hi.value,10))) return false;
      if (clan.value && p.dataset.team !== clan.value) return false;
      if (spawn.value && p.dataset.spawn !== spawn.value) return false;
      if (ship.value && p.dataset.ship !== ship.value) return false;
      return true;
    }
    function panel(title, rows, unit, pct){
      var vals = rows.map(function(r){ return r.v; }).filter(function(v){ return v !== null; });
      var max = Math.max(0, Math.max.apply(null, vals.length ? vals : [0])), min = Math.min(0, Math.min.apply(null, vals.length ? vals : [0]));
      var span = (max - min) || 1, zero = (-min) / span * 100;
      var html = '<h4>' + title + '</h4>';
      rows.forEach(function(r){
        var bar = '';
        if (r.v !== null) {
          var left = r.v >= 0 ? zero : zero + r.v / span * 100, w = Math.abs(r.v) / span * 100;
          bar = '<i style="left:' + left.toFixed(1) + '%;width:' + w.toFixed(1) + '%;background:' + r.color + '"></i>' + (min < 0 ? '<b style="left:' + zero.toFixed(1) + '%"></b>' : '');
        }
        var text = r.v === null ? '-' : (pct ? Math.round(r.v) + '%' : (unit === 'km' ? (r.v/1000).toFixed(1) + ' km' : fmt(r.v)));
        html += '<div class="row"><span>' + r.team + '</span><span class="bar">' + bar + '</span><span>' + text + '</span></div>';
      });
      return '<div class="panel">' + html + '</div>';
    }
    function render(){
      var vis = paths.filter(function(p){ var s = shown(p); p.hidden = !s; return s; });
      count.textContent = vis.length + ' of ' + paths.length + ' smokes shown';
      sec.querySelector('.lo').textContent = clockText(parseInt(lo.value,10));
      sec.querySelector('.hi').textContent = clockText(parseInt(hi.value,10));
      var teams = Array.from(new Set(paths.map(function(p){ return p.dataset.team; })));
      var order = ['H-SR','RESIN','PN']; teams.sort(function(a,b){ return order.indexOf(a) - order.indexOf(b); });
      function rows(f){ return teams.map(function(t){ var list = vis.filter(function(p){ return p.dataset.team === t; }); return {team:t, v:f(list), color:(window.TEAM_COLORS||{})[t]||'#94A3B8'}; }); }
      function avg(list, key){ var xs = list.map(function(p){ return p.dataset[key]; }).filter(function(x){ return x !== ''; }).map(Number); return xs.length ? xs.reduce(function(a,b){return a+b;},0)/xs.length : null; }
      chart.innerHTML =
        panel('Smokes', rows(function(l){ return l.length ? l.length : null; }), '', false) +
        panel('Average smoke damage', rows(function(l){ return avg(l, 'dmg'); }), '', false) +
        panel('<abbr class="term" title="' + (window.CONTEST_DEF||'') + '">Average distance to the nearest contested cap</abbr> (negative = inside)', rows(function(l){ return avg(l, 'contested'); }), 'km', false) +
        panel('<abbr class="term" title="' + (window.SELFISH_DEF||'') + '">Selfish smoke</abbr> share', rows(function(l){ var v = avg(l, 'selfish'); return v === null ? null : v * 100; }), '', true);
    }
    function clamp(){ if (parseInt(lo.value,10) > parseInt(hi.value,10)) { if (document.activeElement === lo) hi.value = lo.value; else lo.value = hi.value; } }
    [lo, hi].forEach(function(r){ r.addEventListener('input', function(){ clamp(); render(); }); });
    [clan, spawn, ship].forEach(function(s){ s.addEventListener('change', render); });
    // Filters can be preset from the query string: ?clan=RESIN&spawn=north&ship=Harugumo&from=0&to=600 (seconds since battle start).
    var q = new URLSearchParams(location.search);
    if (q.get('clan')) clan.value = q.get('clan');
    if (q.get('spawn')) spawn.value = q.get('spawn');
    if (q.get('ship')) ship.value = q.get('ship');
    if (q.get('from')) lo.value = q.get('from');
    if (q.get('to')) hi.value = q.get('to');
    clamp(); render();
  });

  // Games page: group stage filters.
  var gtable = document.getElementById('games');
  if (gtable && document.getElementById('g-clan')) {
    var grows = Array.from(gtable.querySelectorAll('tbody tr'));
    function grender(){
      var c = document.getElementById('g-clan').value, m = document.getElementById('g-map').value, n = 0;
      grows.forEach(function(r){ var ok = (!c || r.dataset.clan.split(';').indexOf(c) >= 0) && (!m || r.dataset.map === m); r.hidden = !ok; if (ok) n++; });
      document.getElementById('g-count').textContent = n + ' of ' + grows.length + ' games';
      document.getElementById('g-empty').hidden = n > 0;
    }
    ['g-clan','g-map'].forEach(function(id){ document.getElementById(id).addEventListener('change', grender); });
    grender();
  }

  if (!window.SMOKES) return;
  var rows = window.SMOKES, tbody = document.querySelector('#smokes tbody');
  function fill(id, key){ var sel = document.getElementById(id); var vals = Array.from(new Set(rows.map(function(r){return r[key];}))).filter(Boolean).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', render); }
  fill('f-team','team'); fill('f-player','player'); fill('f-ship','ship'); fill('f-map','map'); fill('f-game','game'); fill('f-type','type');
  document.getElementById('f-sort').addEventListener('change', render);
  function val(id){ return document.getElementById(id).value; }
  function bar(v, max, color){ var w = max ? Math.max(0, Math.min(1, v/max))*80 : 0; return '<span class="mini"><i style="width:'+w.toFixed(0)+'px;background:'+color+'"></i></span>'; }
  function render(){
    var f = {team:val('f-team'), player:val('f-player'), ship:val('f-ship'), map:val('f-map'), game:val('f-game'), type:val('f-type')};
    var sort = val('f-sort'), asc = sort==='cap' || sort==='contested';
    var list = rows.filter(function(r){ return Object.keys(f).every(function(k){ return !f[k] || r[k]===f[k]; }); });
    list.sort(function(a,b){ var x=a[sort], y=b[sort]; if (x==null) x = asc? Infinity : -Infinity; if (y==null) y = asc? Infinity : -Infinity; return asc ? x-y : y-x; });
    tbody.innerHTML = list.map(function(r){
      var cap = r.cap==null ? '-' : (r.cap<0 ? Math.round(r.depth)+'% into '+r.cap_name : (r.cap/1000).toFixed(1)+' km to '+r.cap_name);
      var capBar = r.cap==null ? '' : bar(Math.max(0, 6000-Math.max(0,r.cap)), 6000, '#5DADE2');
      var con = r.contested==null ? '-' : (r.contested<0 ? (-r.contested/1000).toFixed(1)+' km inside '+r.contested_name : (r.contested/1000).toFixed(1)+' km to '+r.contested_name);
      return '<tr><td>'+(r.thumb?'<a href="'+r.href+'"><img src="'+r.thumb+'" loading="lazy" alt=""></a>':'')+'</td>'+
        '<td><span class="tag" style="--c:'+r.color+'">'+r.team+'</span></td><td>'+r.player+'</td><td>'+r.ship+'</td><td>'+r.map+'</td>'+
        '<td class="small"><a href="'+r.game_href+'">'+r.game+'</a></td><td>'+r.clock+'</td>'+
        '<td>'+r.total.toLocaleString()+' '+bar(r.total, window.MAX_TOTAL, '#F5C542')+'<div class="small muted">in '+r.inside.toLocaleString()+' / behind '+r.behind.toLocaleString()+'</div></td>'+
        '<td>'+cap+' '+capBar+'</td><td>'+con+'</td><td>'+r.radar+'</td><td><a href="'+r.href+'">smoke</a>'+(r.selfish?' <abbr class="term muted small" title="'+(window.SELFISH_DEF||'')+'">selfish</abbr>':'')+(r.flag?' <span class="warn small">flag</span>':'')+'</td></tr>';
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
