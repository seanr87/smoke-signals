"""Build the Smoke Signals demo site from a batch output folder.

Usage:
  python -I build_site.py --batch output/<batch> --maps output/<maps>/maps
         [--clips <folder with <smoke_id>.mp4>] [--inventory smoke/inventory.csv]
         [--out site] [--colors "H-SR=#F5C542,RESIN=#5DADE2,PN=#B388FF"]

The site is static: plain HTML, CSS and a little JavaScript, no server.
Pages: Home, Analysis, Clans, Players, Smokes, Maps, Games.
"""
import argparse
import csv
import html
import json
import math
import os
import re
import shutil
from collections import Counter, defaultdict

TEAMS = ["H-SR", "RESIN", "PN"]
MATCH_SECONDS = 20 * 60
NATIVE = 768
GRID_LETTERS = "ABCDEFGHIJ"
PHASES = [("opening", 0, 400), ("mid", 400, 800), ("endgame", 800, MATCH_SECONDS)]
SELFISH_DEF = "Selfish smoke: no teammate other than the owner was ever inside it, and no teammate fired through it from behind."
CONTEST_DEF = "A cap is contested for a team when it sits on the midline between the two spawns, lies on the enemy's side of the midline, or is held by the enemy."
REASON_TEXT = {"midline": "it sits on the midline between the spawns", "enemy_side": "it lies on the enemy's side of the midline", "enemy_owned": "the enemy held it"}
METRIC_DEFS = {
    "uptime": "Smoke uptime: seconds per game with at least one of the clan's smokes standing.",
    "charge": "Charge use: smoke charges used over charges carried by the clan's smoke ships.",
    "stacking": "Stacking rate: share of the clan's smokes that overlapped another smoke.",
    "contested": "Contested-cap share: share of smokes that stood within 1 km of a contested cap on average over their life.",
    "swing": "Score swing: change in the point gap (ours minus theirs) from activation to capture, averaged.",
    "survival": "Smoker survival: share of smokes whose smoker was still alive 60 s after the smoke dispersed.",
    "punished": "Radar-punished share: share of smokes in which at least one of the clan's ships was radar-spotted while inside.",
    "offensive": "Offensive radar: enemies spotted by the clan's own radar run from inside its smoke while concealed, inferred from the activation and radar range.",
    "won": "Smoke near a cap capture: a cap within stock gun range of a concealed ship flipped to the clan during the smoke or within 10 s after it.",
    "coverage": "Radar cap coverage: share of a contested cap's area within the range of a radar ship concealed in the smoke.",
}
AWARD_DEFS = {
    "Smoke of the Tournament": "Highest smoke damage: main-gun shells fired from or through the smoke by the smoking team, plus the fires they started.",
    "Deepest Cap Smoke": "Deepest into a contested cap as a share of the cap's radius, among smokes near a cap capture or a defended cap.",
    "Radar Bait": "Most radar spots on the smoking team's ships inside the smoke while it stood; ties broken by the damage those ships took while spotted.",
    "Peekaboo": "Most enemies spotted by the smoking team's own radar, run from inside the smoke while concealed.",
    "Most Selfish Smoke": "The selfish smoke with the most damage by its owner.",
    "Golden Cloud": "Most total smoke damage.",
    "The Smokefather": "Most smokes laid.",
    "Best in Haze": "Highest average smoke damage per smoke, minimum 5 smokes.",
    "Most Selfish Smoker": "Most selfish smokes.",
}
# Playoff bracket shape: rounds in display order with the number of series in each.
BRACKET = [
    ("WB Round 1", "Winners round 1", 8), ("WB Round 2", "Winners round 2", 4), ("WB Round 3", "Winners round 3", 2), ("WB Round 4", "Winners final", 1),
    ("LB Round 1", "Losers round 1", 4), ("LB Round 2", "Losers round 2", 4), ("LB Round 3", "Losers round 3", 2), ("LB Round 4", "Losers round 4", 2),
    ("LB Round 5", "Losers round 5", 1), ("LB Round 6", "Losers final", 1), ("GF Round 1", "Grand final", 1),
]
ROUND_TITLES = {k: v for k, v, _ in BRACKET}


def esc(s):
    return html.escape(str(s if s is not None else ""))


def slug(text):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", str(text)).strip("_") or "x"


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


def elapsed_text(seconds):
    seconds = max(0, int(round(seconds)))
    return f"{seconds // 60}:{seconds % 60:02d}"


def phase_of(elapsed):
    if elapsed is None:
        return None
    for name, lo, hi in PHASES:
        if lo <= elapsed < hi or (name == "endgame" and elapsed >= hi):
            return name
    return None


def fmt_int(v):
    return f"{int(round(v)):,}" if v is not None else "-"


def fmt_km(m):
    return "-" if m is None else f"{m / 1000:.1f} km"


def cap_text(s):
    """One line on a smoke's cap proximity at capture (outside caps only)."""
    m = s.get("cap_proximity_m")
    if m is None:
        return "inside a cap, or no cap proximity at capture"
    name = s.get("cap_proximity_name") or "?"
    r = s.get("cap_radius_m")
    radius = f", cap radius {fmt_km(r)}" if r else ""
    return f"{fmt_km(m)} outside cap {name}{radius}"


def contested_text(s):
    """One line on the smoke's average distance to the nearest contested cap over its life."""
    d = s.get("avg_contested_cap_dist_m")
    if d is None:
        return "no cap was contested while it stood"
    name = s.get("contested_cap_name") or "?"
    why = REASON_TEXT.get(s.get("cap_contested_reason") or "", "")
    why = f", contested because {why}" if why else ""
    depth = s.get("contested_cap_depth_pct")
    if d < 0 and depth is not None:
        return f"{min(100, depth):.0f}% of the way into contested cap {name} (cap radius {fmt_km(s.get('contested_cap_radius_m'))}){why}"
    return f"on average {fmt_km(d)} from the edge of contested cap {name}{why}"


def cap_outcome_text(s):
    if s.get("cap_won"):
        at = (s.get("cap_won_at") or {}).get("clock") or ""
        return f"smoke near a cap capture: cap {s['cap_won']} flipped to the team at {at}"
    if s.get("cap_defended"):
        return f"cap {s['cap_defended']} defended while the enemy invaded it"
    return "no cap changed hands"


class Data:
    def __init__(self, batch, maps_dir, clips_dir, inventory):
        self.batch = batch
        self.smokes = json.load(open(os.path.join(batch, "smokes.json"), encoding="utf-8"))
        self.jobs = json.load(open(os.path.join(batch, "jobs.json"), encoding="utf-8"))
        self.job_by_key = {(j["match_id"], j["game_no"], j["team"]): j for j in self.jobs}
        self.games = {}
        self.damage_by_team_game = defaultdict(float)
        self.spikes = {}
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
                self.spikes[(j["team"], key)] = spike
                owner_team = {str(p["entity_id"]): t["name"] for t in g["teams"] for p in t["players"]}
                for ent, dmg in spike.get("damage_by_attacker_shell_fire", spike.get("damage_by_attacker", {})).items():
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
            s["_disp_s"] = disp.get("seconds")
            s["_duration"] = (disp["seconds"] - s["_act_s"]) if disp else None
            st_a, st_c = s.get("state_at_activate") or {}, s.get("state_at_capture") or {}
            s["_score_swing"] = None
            if st_a and st_c and st_a.get("score_ours") is not None and st_c.get("score_ours") is not None:
                s["_score_swing"] = (st_c["score_ours"] - st_c["score_theirs"]) - (st_a["score_ours"] - st_a["score_theirs"])
            s["_in"] = s.get("damage_in_smoke") or 0.0
            s["_behind"] = s.get("damage_behind_smoke") or 0.0
            s["_total"] = s.get("smoke_damage_total") or 0.0
            d = s.get("damage_detail") or {}
            s["_shell"] = d.get("damage_shell") or 0.0
            s["_fire"] = d.get("damage_fire") or 0.0
            s["_salvos"] = d.get("salvos") or 0
            s["_owner_damage"] = (d.get("damage_in_smoke_smoker") or 0) + (d.get("damage_behind_smoke_smoker") or 0)
            s["_radar"] = len(s.get("radar_detections_in_smoke") or [])
            s["_radar_dmg"] = s.get("radar_spotted_damage") or 0.0
            o = s.get("offensive_radar") or {}
            s["_offensive"] = o.get("enemies_spotted") or 0
            s["_games_label"] = self.game_label(s["_key"])
            rem = clock_remaining_seconds(s["_act_clock"])
            s["_elapsed"] = (MATCH_SECONDS - rem) if rem is not None else None
            s["_phase"] = phase_of(s["_elapsed"])
            depth = s.get("contested_cap_depth_pct")
            s["_depth"] = min(100.0, depth) if depth is not None else None
            s["_won"] = bool(s.get("cap_won"))
            s["_defended"] = bool(s.get("cap_defended"))
            rc = s.get("radar_cap") or {}
            s["_coverage"] = rc.get("coverage_pct")
            s["_coverage_full"] = bool(rc.get("full"))
        self.smokes.sort(key=lambda s: (s["_key"], s["_act_s"]))
        self.by_game = defaultdict(list)
        for s in self.smokes:
            self.by_game[s["_key"]].append(s)
        # Smoker survival 60 s after dispersal, from the roster's death times.
        for s in self.smokes:
            g = self.games.get(s["_key"])
            s["_survived"] = None
            if not g:
                continue
            p = next((p for t in g["teams"] for p in t["players"] if p["player"] == s["player"]), None)
            if p is None:
                continue
            end = (s["_disp_s"] if s["_disp_s"] is not None else g.get("replay_end_s") or 0) + 60
            death = (p.get("death") or {}).get("seconds")
            s["_survived"] = death is None or death > end
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
            if caps:
                self.caps_by_map.setdefault(g["map"], caps)
        # Phase each game ended in, from the battle end clock.
        self.game_end_phase = {}
        for key, g in self.games.items():
            rem = clock_remaining_seconds((g.get("battle_end") or {}).get("clock"))
            self.game_end_phase[key] = phase_of(MATCH_SECONDS - rem) if rem is not None else None

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
        sides = set()
        for g in self.games.values():
            if g["map"] == map_name:
                for t in g["teams"]:
                    if t.get("spawn_side"):
                        sides.add(t["spawn_side"])
        return sides

    def team_games(self, team):
        """Keys of the games a clan played, with its win flag."""
        out = {}
        for key, r in self.inventory.items():
            if r["status"] == "played" and team in r["our_teams"].split(";"):
                out[key] = r["winner"] == team
        if not out:
            for (m, g, t) in self.job_by_key:
                if t == team:
                    out[(m, g)] = None
        return out


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


def bar_chart(title, rows, fmt=fmt_int, note="", width=360, muted=None, label_w=70):
    """Horizontal bars, one per row (label, value, colour, n). Negative values hang left of a zero line."""
    muted = muted or set()
    vals = [v for _, v, _, _ in rows if v is not None]
    hi = max([0.0] + vals)
    lo = min([0.0] + vals)
    span = (hi - lo) or 1.0
    zero = (-lo) / span
    h = 22 * len(rows) + 4
    bar_x0 = label_w
    bar_w = width - label_w - 110
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" class="chart" style="max-width:{width}px" role="img" aria-label="{esc(title)}">']
    for i, (label, v, color, n) in enumerate(rows):
        y = 2 + i * 22
        out.append(f'<text x="0" y="{y + 14}" class="lbl">{esc(label)}</text>')
        if v is not None:
            left = bar_x0 + (zero if v >= 0 else zero + v / span) * bar_w
            w = abs(v) / span * bar_w
            op = ' opacity="0.3"' if label in muted else ""
            out.append(f'<rect x="{left:.1f}" y="{y + 3}" width="{max(1.5, w):.1f}" height="14" rx="3" fill="{color}"{op}/>')
            text = fmt(v)
        else:
            text = "-"
        out.append(f'<text x="{width}" y="{y + 14}" class="val" text-anchor="end">{esc(text)}{" (n=" + str(n) + ")" if n is not None else ""}</text>')
    if lo < 0:
        zx = bar_x0 + zero * bar_w
        out.append(f'<line x1="{zx:.1f}" y1="0" x2="{zx:.1f}" y2="{h}" class="zero"/>')
    out.append("</svg>")
    note = f'<p class="muted small">{note}</p>' if note else ""
    return f'<div class="panel"><h4>{title}</h4>{"".join(out)}{note}</div>'


def mini_bar(value, max_value, color, width=90):
    frac = 0 if not max_value else max(0.0, min(1.0, value / max_value))
    return f'<span class="mini"><i style="width:{frac * width:.0f}px;background:{color}"></i></span>'


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


PALETTE = ["#F5C542", "#5DADE2", "#B388FF", "#6EE7B7", "#FB923C", "#F472B6", "#A3E635", "#94A3B8", "#F87171", "#22D3EE"]
ENEMY_COLOR = "#F87171"


class Site:
    def __init__(self, data, out, colors):
        self.d = data
        self.out = out
        self.colors = colors
        self.smoke_href = {}
        for s in data.smokes:
            s["_slug"] = f"{s['_match']}_g{s['game_no']}_{s['smoke_id']}"
            self.smoke_href[s["_slug"]] = f"smokes/{s['_slug']}.html"
        self.players = self.player_stats()
        self.awards = self.compute_awards()
        self.badges = defaultdict(list)
        for title, (name, _) in self.awards["players"].items():
            if name:
                self.badges[name].append(title)
        for title, s in self.awards["smokes"].items():
            if s:
                self.badges[s["player"]].append(title)

    def color(self, team):
        return self.colors.get(team, "#94A3B8")

    def nav(self, depth, active):
        base = "../" * depth
        items = [("Home", "index.html"), ("Analysis", "analysis.html"), ("Clans", "clans.html"), ("Players", "players.html"), ("Smokes", "smokes.html"), ("Maps", "maps.html"), ("Games", "games.html")]
        links = "".join(f'<a href="{base}{h}" class="{"active" if n == active else ""}">{n}</a>' for n, h in items)
        return f'<nav class="top"><span class="brand">Smoke Signals</span><input type="checkbox" id="navtoggle" class="navtoggle"><label for="navtoggle" class="navbtn" aria-label="Menu">Menu</label><div class="links">{links}</div></nav>'

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
        if team not in self.colors:
            return f'<span class="tag other">{esc(team)}</span>'
        return f'<span class="tag" style="--c:{self.color(team)}">{esc(team)}</span>'

    def player_href(self, name, depth=0):
        return f"{'../' * depth}players/{slug(name)}.html"

    def clan_href(self, team, depth=0):
        return f"{'../' * depth}clans/{slug(team)}.html"

    def game_href(self, key, depth=0):
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
            s["_img"] = {}
            s["_clip"] = None
            if not job:
                continue
            frames = os.path.join(d.batch, "games", job["name"], "frames")
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
            if clip:
                rel = f"clips/{s['_slug']}.mp4"
                dst = os.path.join(self.out, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(clip, dst)
                s["_clip"] = rel
            rel = f"img/diag/{s['_slug']}.svg"
            self.write(rel, self.diagram_svg(s))
            s["_diag"] = rel

    def diagram_svg(self, s):
        """A clean diagram: puffs, nearby caps, nearby ships as team-coloured icons, and shooter-to-target arrows labelled with damage."""
        d = self.d
        g = d.games.get(s["_key"]) or {}
        pts = s.get("path") or [s["origin_xy"]]
        xs = [p["x"] for p in pts]
        zs = [p["z"] for p in pts]
        cx, cz = (min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2
        half = max((max(xs) - min(xs)) / 2, (max(zs) - min(zs)) / 2) + 100
        half = max(half, 140)
        size = 240
        k = size / (2 * half)

        def px(x, z):
            return (x - cx) * k + size / 2, -(z - cz) * k + size / 2

        own_team = s["team"]
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}"><rect width="{size}" height="{size}" fill="#0B1C2C"/>']
        for c in g.get("caps") or []:
            x, y = px(c["position"]["x"], c["position"]["z"])
            r = c["radius"] * k
            if -r < x < size + r and -r < y < size + r:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#fff" fill-opacity="0.06" stroke="#fff" stroke-opacity="0.5" stroke-dasharray="4,3"/><text x="{x:.1f}" y="{y + 5:.1f}" fill="#fff" fill-opacity="0.7" font-size="14" font-weight="700" text-anchor="middle" font-family="Segoe UI,sans-serif">{esc(c["cap"])}</text>')
        pr = (s.get("radius") or 15) * k
        for p in thin(pts, 40):
            x, y = px(p["x"], p["z"])
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pr:.1f}" fill="#CBD5E1" fill-opacity="0.35" stroke="#E2E8F0" stroke-opacity="0.6" stroke-width="0.8"/>')
        for m in s.get("ships_at_capture") or []:
            x, y = px(m["position"]["x"], m["position"]["z"])
            if not (0 <= x <= size and 0 <= y <= size):
                continue
            ally = m.get("team") == own_team
            color = self.color(own_team) if ally else ENEMY_COLOR
            tri = f"M{x:.1f},{y - 6:.1f} L{x + 5:.1f},{y + 5:.1f} L{x - 5:.1f},{y + 5:.1f} Z"
            ring = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="none" stroke="#F5C542" stroke-width="1.5"/>' if m.get("is_owner") else ""
            out.append(f'{ring}<path d="{tri}" fill="{color}" stroke="#07131f" stroke-width="0.8"/>')
        dd = s.get("damage_detail") or {}
        arrows = [a for a in (dd.get("arrows") or []) if a.get("attacker_ally") and a.get("damage", 0) >= 1]
        arrows.sort(key=lambda a: -a["damage"])
        out.append(f'<defs><marker id="ar" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{self.color(own_team)}"/></marker></defs>')
        for a in arrows[:6]:
            x1, y1 = px(a["from"]["x"], a["from"]["z"])
            x2, y2 = px(a["to"]["x"], a["to"]["z"])
            x1, y1 = min(max(x1, 4), size - 4), min(max(y1, 4), size - 4)
            x2, y2 = min(max(x2, 4), size - 4), min(max(y2, 4), size - 4)
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{self.color(own_team)}" stroke-width="1.6" marker-end="url(#ar)" opacity="0.9"/>')
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            label = fmt_int(a["damage"])
            out.append(f'<rect x="{mx - 3 - len(label) * 3.2:.1f}" y="{my - 7:.1f}" width="{len(label) * 6.4 + 6:.1f}" height="13" rx="3" fill="#07131f" fill-opacity="0.85"/><text x="{mx:.1f}" y="{my + 3:.1f}" fill="#F5C542" font-size="10" text-anchor="middle" font-family="Segoe UI,sans-serif">{label}</text>')
        km = 1000 / 30 * k
        out.append(f'<line x1="8" y1="{size - 8}" x2="{8 + km:.1f}" y2="{size - 8}" stroke="#fff" stroke-width="2"/><text x="{10 + km:.1f}" y="{size - 5}" fill="#fff" font-size="9" font-family="Segoe UI,sans-serif">1 km</text>')
        out.append("</svg>")
        return "".join(out)

    def thumb(self, s, depth=0):
        rel = s.get("_diag")
        if not rel:
            return '<div class="noimg">no diagram</div>'
        return f'<img src="{"../" * depth}{rel}" alt="smoke diagram" loading="lazy">'

    def img(self, s, field, depth, cls="", lazy=True):
        rel = (s.get("_img") or {}).get(field)
        if not rel:
            return '<div class="noimg">no frame</div>'
        lazy_attr = ' loading="lazy"' if lazy else ""
        return f'<img class="{cls}" src="{"../" * depth}{rel}" alt="{esc(field)}"{lazy_attr}>'

    def smoke_card(self, s, depth=0, note=""):
        base = "../" * depth
        return f"""<a class="card smoke-card" href="{base}{self.smoke_href[s['_slug']]}">{self.thumb(s, depth)}<div class="card-body">
<div>{self.team_tag(s['team'])} <b>{esc(s['player'])}</b> <span class="muted">{esc(s['ship'])}</span></div>
<div class="muted small">{esc(s['_games_label'])} | {esc(s['_act_clock'])}</div>
<div class="small">{fmt_int(s['_total'])} smoke damage{(' | ' + esc(note)) if note else ''}</div></div></a>"""

    def summary_line(self, s):
        """One line: who, where, how long, allies firing, salvos and damage, cap outcome."""
        shooters = s.get("shooters") or []
        others = [n for n in shooters if n != s["player"]]
        dur = f"stood {s['_duration']:.0f} s" if s.get("_duration") is not None else "was still standing when the replay ended"
        where = f"on {self.d.map_title(s['map'])}"
        if s.get("contested_cap_name"):
            where += f" near contested cap {s['contested_cap_name']}"
        if s["_total"] > 0:
            if len(shooters) == 1 and shooters[0] == s["player"]:
                who = "the smoker alone"
            else:
                who = f"{len(others)} {'ally' if len(others) == 1 else 'allies'}" + (" and the smoker" if s["player"] in shooters else "")
            firing = f"{who} fired {s['_salvos']} {'salvo' if s['_salvos'] == 1 else 'salvos'} for {fmt_int(s['_total'])} damage"
            if s["_fire"] > 0:
                firing += f" ({fmt_int(s['_fire'])} of it fire)"
        else:
            firing = "no damage was fired from or through it"
        return f"{s['player']} ({s['ship']}, {s['team']}) smoked at {s['_act_clock']} {where}; the smoke {dur}; {firing}; {cap_outcome_text(s)}."

    def build(self):
        self.copy_assets()
        self.write("style.css", CSS.replace("__TEAMCOLORS__", "".join(f'--team-{t.lower().replace("-", "")}:{c};' for t, c in self.colors.items())))
        self.write("site.js", JS)
        self.write(".nojekyll", "")
        self.home()
        self.analysis()
        self.clans_index()
        for t in TEAMS:
            if any(s["team"] == t for s in self.d.smokes):
                self.clan_page(t)
        self.players_page()
        for name in self.players:
            self.player_page(name)
        self.awards_redirect()
        self.games_page()
        self.maps_page()
        self.all_smokes()
        for key in self.d.by_game:
            self.game_page(key)
        for s in self.d.smokes:
            self.smoke_page(s)

    def player_stats(self):
        d = self.d
        by_player = defaultdict(lambda: {"smokes": 0, "damage": 0.0, "radar": 0, "ships": Counter(), "team": "", "selfish": 0, "games": set(), "won": 0, "offensive": 0, "maps": Counter()})
        for s in d.smokes:
            p = by_player[s["player"]]
            p["smokes"] += 1
            p["damage"] += s["_total"]
            p["radar"] += s["_radar"]
            p["ships"][s["ship"]] += 1
            p["team"] = s["team"]
            p["selfish"] += 1 if s.get("selfish_smoke") else 0
            p["games"].add(s["_key"])
            p["won"] += 1 if s["_won"] else 0
            p["offensive"] += s["_offensive"]
            p["maps"][s["map"]] += 1
        return by_player

    def compute_awards(self):
        d = self.d
        rows = d.smokes
        best = max(rows, key=lambda s: s["_total"]) if rows else None
        eligible = [s for s in rows if s["_depth"] is not None and (s["_won"] or s["_defended"])]
        deep = max(eligible, key=lambda s: (s["_depth"], s["_total"])) if eligible else None
        bait = max(rows, key=lambda s: (s["_radar"], s["_radar_dmg"], s["_total"])) if rows else None
        if bait and bait["_radar"] == 0:
            bait = None
        peek = max(rows, key=lambda s: (s["_offensive"], s["_total"])) if rows else None
        if peek and peek["_offensive"] == 0:
            peek = None
        selfish = [s for s in rows if s.get("selfish_smoke")]
        most_selfish = max(selfish, key=lambda s: s["_owner_damage"]) if selfish else None
        smokes = {"Smoke of the Tournament": best, "Deepest Cap Smoke": deep, "Radar Bait": bait, "Peekaboo": peek, "Most Selfish Smoke": most_selfish}
        players = self.players

        def top_by(key, minimum=0):
            items = [(n, p) for n, p in players.items() if p["smokes"] >= minimum]
            return max(items, key=lambda kv: key(kv[1])) if items else (None, None)

        pawards = {
            "Golden Cloud": top_by(lambda p: p["damage"]),
            "The Smokefather": top_by(lambda p: p["smokes"]),
            "Best in Haze": top_by(lambda p: p["damage"] / p["smokes"], minimum=5),
            "Most Selfish Smoker": top_by(lambda p: p["selfish"]),
        }
        clan_rows = {}
        for t in TEAMS:
            rows_t = [s for s in rows if s["team"] == t]
            g = d.games_played.get(t) or 0
            if g:
                clan_rows[t] = {"smokes": len(rows_t) / g, "damage": sum(s["_total"] for s in rows_t) / g, "selfish": sum(1 for s in rows_t if s.get("selfish_smoke")) / g, "games": g}
        cawards = {}
        for title, key in [("Most smokes laid", "smokes"), ("Most smoke damage", "damage"), ("Most selfish smokes", "selfish")]:
            if clan_rows:
                w = max(clan_rows, key=lambda t: clan_rows[t][key])
                cawards[title] = (w, clan_rows[w][key], clan_rows[w]["games"])
        return {"smokes": smokes, "players": pawards, "clans": cawards}

    def award_note(self, title, s):
        if title == "Smoke of the Tournament":
            return f"{fmt_int(s['_total'])} smoke damage"
        if title == "Deepest Cap Smoke":
            return f"{s['_depth']:.0f}% of the way into contested cap {s['contested_cap_name']} (cap radius {fmt_km(s.get('contested_cap_radius_m'))}); {cap_outcome_text(s)}"
        if title == "Radar Bait":
            return f"{s['_radar']} radar spots on the team's ships inside the smoke; {fmt_int(s['_radar_dmg'])} damage taken while spotted"
        if title == "Peekaboo":
            o = s.get("offensive_radar") or {}
            return f"{s['_offensive']} enemies spotted by {o.get('ship') or 'its radar ship'}'s radar from inside the smoke (inferred from the activation and radar range)"
        if title == "Most Selfish Smoke":
            return f"{fmt_int(s['_owner_damage'])} damage by the smoker (no teammate benefited)"
        return ""

    def award_card(self, title, s, depth=0, with_clip=True):
        base = "../" * depth
        sub = term(title, AWARD_DEFS.get(title, "")) if title in AWARD_DEFS else esc(title)
        if not s:
            return f'<div class="card award"><h3>{sub}</h3><p class="muted">Nothing here, just clear skies.</p></div>'
        href = base + self.smoke_href[s["_slug"]]
        clip = ""
        if with_clip:
            clip = f'<div class="clip"><video controls preload="metadata" src="{base}{s["_clip"]}"></video><div class="clip-controls"><button class="speed" data-rate="1">1x (5x real time)</button><button class="speed" data-rate="2">2x (10x real time)</button></div></div>' if s.get("_clip") else '<p class="muted small">Clip available on request.</p>'
        return f"""<div class="card award"><h3>{sub}</h3><p class="note">{esc(self.award_note(title, s))}</p>
<div class="award-hero"><a href="{href}">{self.thumb(s, depth)}</a><div class="award-meta"><div>{self.team_tag(s['team'])} <a href="{self.player_href(s['player'], depth)}"><b>{esc(s['player'])}</b></a> <span class="muted">{esc(s['ship'])}</span></div>
<div class="muted small">{esc(s['_games_label'])}</div><div class="muted small">{esc(self.d.map_title(s['map']))}, activated {esc(s['_act_clock'])}</div>
<div class="big">{fmt_int(s['_total'])} smoke damage</div><p><a href="{href}">Open the smoke page</a></p></div></div>{clip}</div>"""

    def findings(self):
        """Three headline findings, each with one chart (clans side by side)."""
        d = self.d
        total = len(d.smokes)
        out = []
        clans = [t for t in TEAMS if any(s["team"] == t for s in d.smokes)]
        count = lambda t: sum(1 for s in d.smokes if s["team"] == t)
        inside = sum(s["_in"] for s in d.smokes)
        behind = sum(s["_behind"] for s in d.smokes)
        rows = [(t, mean([s["_total"] for s in d.smokes if s["team"] == t]), self.color(t), count(t)) for t in clans]
        if inside + behind > 0:
            text = f"Of {fmt_int(inside + behind)} credited smoke damage, {behind / (inside + behind) * 100:.0f}% was fired from behind a smoke by ships outside it and {inside / (inside + behind) * 100:.0f}% from inside one (n = {total} smokes)."
            out.append((text, bar_chart(f"Average smoke damage per smoke by clan (n = {total})", rows)))
        near = [s for s in d.smokes if s.get("avg_contested_cap_dist_m") is not None and s["avg_contested_cap_dist_m"] <= 1000]
        rows = [(t, 100.0 * sum(1 for s in near if s["team"] == t) / max(1, count(t)), self.color(t), count(t)) for t in clans]
        won = sum(1 for s in d.smokes if s["_won"])
        out.append((f"{len(near) / total * 100:.0f}% of smokes stood within 1 km of a contested cap on average, and {won} smokes ({won / total * 100:.0f}%) were up when a supported cap flipped to the smoking team (n = {total}).",
                    bar_chart(f"Share of smokes within 1 km of a contested cap (n = {total})", rows, fmt=lambda v: f"{v:.0f}%")))
        per_game = {t: count(t) / d.games_played[t] for t in clans if d.games_played.get(t)}
        punished = sum(1 for s in d.smokes if s["_radar"] > 0)
        if per_game:
            hi = max(per_game, key=per_game.get)
            lo = min(per_game, key=per_game.get)
            rows = [(t, 100.0 * sum(1 for s in d.smokes if s["team"] == t and s["_radar"] > 0) / max(1, count(t)), self.color(t), count(t)) for t in clans]
            out.append((f"{esc(hi)} laid the most smokes per game ({per_game[hi]:.1f}) and {esc(lo)} the fewest ({per_game[lo]:.1f}); {punished / total * 100:.0f}% of all smokes had a ship radar-spotted inside them (n = {total}).",
                        bar_chart(f"{term('Radar-punished', METRIC_DEFS['punished'])} share by clan (n = {total})", rows, fmt=lambda v: f"{v:.0f}%")))
        return out[:3]

    def home(self):
        d = self.d
        n_games = len(d.by_game)
        n_played = len(d.played_keys) or n_games
        maps = len({s["map"] for s in d.smokes})
        games_text = f"{n_played} games ({n_games} with at least one smoke)" if n_played != n_games else f"{n_games} games"
        findings = "".join(f'<li><p>{text}</p>{chart}</li>' for text, chart in self.findings())
        strip = "".join(self.award_card(t, s) for t, s in self.awards["smokes"].items())
        per_team = Counter(s["team"] for s in d.smokes)
        stats = "".join(f'<div class="stat" style="--c:{self.color(t)}"><b>{per_team[t]}</b><span>{esc(t)} smokes in {d.games_played.get(t, 0)} games</span></div>' for t in TEAMS if per_team.get(t))
        body = f"""<section class="briefing"><h1>Mission briefing</h1>
<p>We want to win games. This site breaks down how top competitive teams use smoke: {len(d.smokes)} smokes from {games_text} of King of the Sea XIX NA played by H-SR, RESIN and PN, read straight from the replays.</p>
<p class="muted">Smoke damage counts main-gun shells fired from or through the smoke by the smoking team, plus the fires they started; each shot is credited to one smoke. Purpose and intent tags come later by hand.</p></section>
<section class="stats"><div class="stat"><b>{len(d.smokes)}</b><span>smokes analysed</span></div><div class="stat"><b>{n_played}</b><span>games on {maps} maps ({n_games} with at least one smoke)</span></div>{stats}</section>
<h2>Three headline findings</h2><ol class="findings">{findings}</ol>
<h2>The five award smokes</h2><p class="muted">{esc(SELFISH_DEF)} {esc(CONTEST_DEF)}</p><section class="cards awards">{strip}</section>"""
        self.write("index.html", self.page("Home", body, active="Home"))

    def clan_metrics(self, team):
        """Every clan metric with its count, for the Analysis charts and the clan page."""
        d = self.d
        rows = [s for s in d.smokes if s["team"] == team]
        games = d.team_games(team)
        n_games = len(games) or 1
        uptime = 0.0
        for key in games:
            spans = sorted((s["_act_s"], s["_disp_s"] if s["_disp_s"] is not None else (d.games.get(key) or {}).get("replay_end_s") or s["_act_s"]) for s in rows if s["_key"] == key)
            cur = None
            for a, b in spans:
                if cur is None or a > cur[1]:
                    if cur:
                        uptime += cur[1] - cur[0]
                    cur = [a, b]
                else:
                    cur[1] = max(cur[1], b)
            if cur:
                uptime += cur[1] - cur[0]
        used = charges = 0
        for key in games:
            g = d.games.get(key)
            if not g:
                continue
            for t in g["teams"]:
                if t["name"] != team:
                    continue
                for p in t["players"]:
                    if p.get("smoke_charges"):
                        used += p["smoke_activations"]
                        charges += p["smoke_charges"]
        n = len(rows)
        with_surv = sum(1 for s in rows if s["_survived"] is not None)
        return {
            "n": n, "games": n_games,
            "smokes_per_game": (n / n_games, n),
            "damage_per_game": (sum(s["_total"] for s in rows) / n_games, n),
            "avg_damage": (mean([s["_total"] for s in rows]), n),
            "uptime": (uptime / n_games, n_games),
            "charge": (100.0 * used / charges if charges else None, charges),
            "stacking": (100.0 * sum(1 for s in rows if s.get("overlap_flag")) / n if n else None, n),
            "contested": (100.0 * sum(1 for s in rows if s.get("avg_contested_cap_dist_m") is not None and s["avg_contested_cap_dist_m"] <= 1000) / n if n else None, n),
            "selfish": (100.0 * sum(1 for s in rows if s.get("selfish_smoke")) / n if n else None, n),
            "swing": (mean([s["_score_swing"] for s in rows]), sum(1 for s in rows if s["_score_swing"] is not None)),
            "survival": (100.0 * sum(1 for s in rows if s["_survived"]) / with_surv if with_surv else None, with_surv),
            "punished": (100.0 * sum(1 for s in rows if s["_radar"] > 0) / n if n else None, n),
            "offensive": (sum(s["_offensive"] for s in rows), sum(1 for s in rows if s["_offensive"] > 0)),
            "won": (sum(1 for s in rows if s["_won"]), n),
            "coverage": (mean([s["_coverage"] for s in rows if s["_coverage"] is not None]), sum(1 for s in rows if s["_coverage"] is not None)),
            "coverage_full": (sum(1 for s in rows if s["_coverage_full"]), n),
        }

    def analysis(self):
        d = self.d
        clans = [t for t in TEAMS if any(s["team"] == t for s in d.smokes)]
        metrics = {t: self.clan_metrics(t) for t in clans}
        findings = "".join(f'<li><p>{text}</p>{chart}</li>' for text, chart in self.findings())

        def chart(key, title, fmt=fmt_int, note=""):
            rows = [(t, metrics[t][key][0], self.color(t), metrics[t][key][1]) for t in clans]
            return bar_chart(title, rows, fmt=fmt, note=note)

        pctf = lambda v: f"{v:.0f}%"
        charts = [
            chart("smokes_per_game", "Smokes per game", fmt=lambda v: f"{v:.1f}"), chart("damage_per_game", "Smoke damage per game"), chart("avg_damage", "Average damage per smoke"),
            chart("uptime", term("Smoke uptime", METRIC_DEFS["uptime"]) + " (s per game)", fmt=lambda v: f"{v:.0f} s"),
            chart("charge", term("Charge use", METRIC_DEFS["charge"]), fmt=pctf, note="n = charges carried"),
            chart("stacking", term("Stacking rate", METRIC_DEFS["stacking"]), fmt=pctf),
            chart("contested", term("Contested-cap share", METRIC_DEFS["contested"]), fmt=pctf),
            chart("selfish", term("Selfish smoke share"), fmt=pctf),
            chart("swing", term("Score swing while smoke up", METRIC_DEFS["swing"]), fmt=lambda v: f"{v:+.0f} pts"),
            chart("survival", term("Smoker alive 60 s after", METRIC_DEFS["survival"]), fmt=pctf),
            chart("punished", term("Radar-punished share", METRIC_DEFS["punished"]), fmt=pctf),
            chart("offensive", term("Enemies spotted by own radar from smoke", METRIC_DEFS["offensive"]), note="n = smokes with such a spot"),
            chart("won", term("Smokes near a cap capture", METRIC_DEFS["won"])),
            chart("coverage", term("Radar cap coverage", METRIC_DEFS["coverage"]) + " (mean %)", fmt=pctf, note="n = smokes with a concealed radar ship"),
        ]
        recon = [sp.get("reconciliation_ratio_shell_fire") for sp in d.spikes.values() if sp.get("reconciliation_ratio_shell_fire")]
        recon_text = f"Across {len(recon)} games the replay ledger's shell-plus-fire damage comes to {mean(recon) * 100:.0f}% of the game's own main-battery-plus-fire totals (per-ship check on every game page)." if recon else ""
        body = f"""<h1>Analysis</h1>
<h2>Three headline findings</h2><ol class="findings">{findings}</ol>
<h2>Clans compared</h2><p class="muted">One chart per metric, one bar per clan, counts on every bar. {esc(recon_text)}</p>
<section class="charts">{"".join(charts)}</section>"""
        self.write("analysis.html", self.page("Analysis", body, active="Analysis"))

    def clans_index(self):
        d = self.d
        cards = []
        for t in TEAMS:
            if not any(s["team"] == t for s in d.smokes):
                continue
            m = self.clan_metrics(t)
            cards.append(f'<a class="card toc" href="{self.clan_href(t)}" style="border-top:4px solid {self.color(t)}"><h2>{self.team_tag(t)} {esc(t)}</h2><p>{m["n"]} smokes in {m["games"]} games, {fmt_int(m["damage_per_game"][0])} smoke damage per game, uptime {m["uptime"][0]:.0f} s per game.</p></a>')
        body = f'<h1>Clans</h1><section class="cards">{"".join(cards)}</section>'
        self.write("clans.html", self.page("Clans", body, active="Clans"))

    def heatmap(self, team, depth=1):
        """Most-smoked spots: a 10 x 10 cell count over each map the clan smoked on."""
        d = self.d
        out = []
        by_map = defaultdict(list)
        for s in d.smokes:
            if s["team"] == team:
                by_map[s["map"]].append(s)
        for map_name, smokes in sorted(by_map.items(), key=lambda kv: -len(kv[1])):
            m = d.maps.get(map_name)
            if not m:
                continue
            cells = Counter()
            for s in smokes:
                p = map_px(d, map_name, s["origin_xy"]["x"], s["origin_xy"]["z"])
                if p:
                    cells[(min(9, max(0, int(p[0] // (NATIVE / 10)))), min(9, max(0, int(p[1] // (NATIVE / 10)))))] += 1
            peak = max(cells.values()) if cells else 1
            rects = "".join(f'<rect x="{cx * NATIVE / 10:.0f}" y="{cy * NATIVE / 10:.0f}" width="{NATIVE / 10:.0f}" height="{NATIVE / 10:.0f}" fill="{self.color(team)}" fill-opacity="{0.15 + 0.7 * n / peak:.2f}"><title>{GRID_LETTERS[cx]}{cy + 1}: {n} smokes</title></rect>' for (cx, cy), n in cells.items())
            labels = "".join(f'<text x="{(i + 0.5) * NATIVE / 10:.0f}" y="14">{GRID_LETTERS[i]}</text><text x="6" y="{(i + 0.5) * NATIVE / 10 + 4:.0f}" text-anchor="start">{i + 1}</text>' for i in range(10))
            out.append(f'<figure class="heat"><div class="mapwrap"><img src="{"../" * depth}maps/{m["map"]}.webp" alt="{esc(d.map_title(map_name))}"><svg viewBox="0 0 {NATIVE} {NATIVE}">{rects}<g class="gridlabels">{labels}</g></svg></div><figcaption>{esc(d.map_title(map_name))}: {len(smokes)} smokes (n = {len({s["_key"] for s in smokes})} games)</figcaption></figure>')
        return f'<div class="heats">{"".join(out)}</div>'

    def clan_page(self, team):
        d = self.d
        rows = [s for s in d.smokes if s["team"] == team]
        m = self.clan_metrics(team)
        games = d.team_games(team)
        color = self.color(team)
        n = len(rows)

        def stat(label, key, fmt=fmt_int, suffix=""):
            v, cnt = m[key]
            text = fmt(v) if v is not None else "-"
            return f'<div class="stat" style="--c:{color}"><b>{text}{suffix}</b><span>{label} (n = {cnt})</span></div>'

        pctf = lambda v: f"{v:.0f}%"
        lead = (stat(term("smoke uptime per game", METRIC_DEFS["uptime"]), "uptime", fmt=lambda v: f"{v:.0f} s")
                + stat(term("score swing while smoke up", METRIC_DEFS["swing"]), "swing", fmt=lambda v: f"{v:+.0f} pts")
                + stat(term("radar-punished share", METRIC_DEFS["punished"]), "punished", fmt=pctf))
        more = (stat("smokes per game", "smokes_per_game", fmt=lambda v: f"{v:.1f}") + stat("smoke damage per game", "damage_per_game")
                + stat(term("charge use", METRIC_DEFS["charge"]), "charge", fmt=pctf) + stat(term("stacking rate", METRIC_DEFS["stacking"]), "stacking", fmt=pctf)
                + stat(term("contested-cap share", METRIC_DEFS["contested"]), "contested", fmt=pctf) + stat(term("smoker alive 60 s after", METRIC_DEFS["survival"]), "survival", fmt=pctf)
                + stat(term("enemies spotted by own radar", METRIC_DEFS["offensive"]), "offensive") + stat(term("smokes near a cap capture", METRIC_DEFS["won"]), "won")
                + stat(term("radar cap coverage, mean", METRIC_DEFS["coverage"]), "coverage", fmt=pctf) + stat("smokes with full radar cap coverage", "coverage_full"))
        ended = {p: {"win": 0, "loss": 0} for p, _, _ in PHASES}
        for key, won in games.items():
            ph = d.game_end_phase.get(key)
            if ph and won is not None:
                ended[ph]["win" if won else "loss"] += 1
        w, h = 360, 160
        peak = max([1] + [v["win"] + v["loss"] for v in ended.values()])
        cols = []
        for i, (p, lo, hi) in enumerate(PHASES):
            x = 30 + i * 110
            win, loss = ended[p]["win"], ended[p]["loss"]
            hw, hl = (h - 50) * win / peak, (h - 50) * loss / peak
            cols.append(f'<rect x="{x}" y="{h - 30 - hw:.1f}" width="70" height="{hw:.1f}" fill="{color}"/><rect x="{x}" y="{h - 30 - hw - hl:.1f}" width="70" height="{hl:.1f}" fill="#475569"/>'
                        f'<text x="{x + 35}" y="{h - 30 - hw - hl - 4:.1f}" class="val" text-anchor="middle">{win} W / {loss} L</text><text x="{x + 35}" y="{h - 12}" class="lbl" text-anchor="middle">{p} ({elapsed_text(lo)}-{elapsed_text(hi)})</text>')
        ended_svg = f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" class="chart">{"".join(cols)}</svg><div class="legend-row"><span class="legend"><i style="background:{color}"></i>wins</span><span class="legend"><i style="background:#475569"></i>losses</span><span class="muted">time elapsed; n = {sum(v["win"] + v["loss"] for v in ended.values())} games with a known end</span></div>'
        reached = Counter()
        for s in rows:
            a = s["_elapsed"]
            if a is None:
                continue
            b = a + (s["_duration"] or 0)
            for p, lo, hi in PHASES:
                if a < hi and b >= lo:
                    reached[p] += 1
        timing = bar_chart(f"Smokes per game standing in each phase (time elapsed; n = {n} smokes, {m['games']} games)",
                           [(f"{p} {elapsed_text(lo)}-{elapsed_text(hi)}", reached[p] / m["games"], color, reached[p]) for p, lo, hi in PHASES], fmt=lambda v: f"{v:.1f}", label_w=130)
        ships = Counter(s["ship"] for s in rows).most_common()
        lineup = svg_donut(ships[:8] + ([("other", sum(v for _, v in ships[8:]))] if len(ships) > 8 else []), PALETTE)
        ship_rows = []
        seen = set()
        for key in games:
            g = d.games.get(key)
            if not g:
                continue
            for t in g["teams"]:
                if t["name"] != team:
                    continue
                for p in t["players"]:
                    if p["ship"] in seen:
                        continue
                    seen.add(p["ship"])
                    ship_rows.append(f'<tr><td>{esc(p["ship"])}</td><td>{esc(p.get("ship_class") or "")}</td><td>{esc(p.get("smoke_type") or "-")}</td><td>{fmt_km(p.get("gun_range_m"))}</td><td>{fmt_km(p.get("radar_m")) if p.get("radar_m") else "-"}</td><td>{fmt_km(p.get("detection_m"))}</td></tr>')
        top = sorted(((name, p) for name, p in self.players.items() if p["team"] == team), key=lambda kv: -kv[1]["damage"])[:3]
        total_damage = sum(s["_total"] for s in rows) or 1
        strip = "".join(f'<a class="card" href="{self.player_href(name, 1)}"><div>{self.team_tag(team)} <b>{esc(name)}</b></div><div class="big">{p["damage"] / total_damage * 100:.0f}%</div><div class="muted small">of the clan\'s smoke damage, {fmt_int(p["damage"])} over {p["smokes"]} smokes</div></a>' for name, p in top)
        cawards = "".join(f'<div class="card award-p"><h3>{esc(t)}</h3><p>{self.team_tag(w)} <b>{esc(w)}</b></p><p class="note">{fmt_int(v) if "damage" in t else f"{v:.1f}"} per game over {g} games</p></div>' for t, (w, v, g) in self.awards["clans"].items() if w == team) or '<p class="muted">No clan award.</p>'
        body = f"""<h1>{self.team_tag(team)} {esc(team)}</h1><p class="muted">{n} smokes in {m['games']} games. Counts (n) on every number.</p>
<section class="stats lead">{lead}</section><section class="stats">{more}</section>
<div class="two-col"><div><h2>Where their games ended</h2>{ended_svg}</div><div><h2>Timing</h2>{timing}</div></div>
<h2>Most-smoked spots</h2>{self.heatmap(team)}
<div class="two-col"><div><h2>Ship lineup</h2>{lineup}<div class="scroll-x"><table class="games"><thead><tr><th>Ship</th><th>Class</th><th>Smoke</th><th>Stock gun range</th><th>Radar</th><th>Detection</th></tr></thead><tbody>{"".join(ship_rows)}</tbody></table></div></div>
<div><h2>Top smokers</h2><section class="cards">{strip}</section><h2>Clan awards</h2><section class="cards">{cawards}</section></div></div>"""
        self.write(f"clans/{slug(team)}.html", self.page(team, body, depth=1, active="Clans"))

    def players_page(self):
        rows = []
        for name, p in sorted(self.players.items(), key=lambda kv: -kv[1]["damage"]):
            badges = "".join(f'<span class="badge" title="{esc(AWARD_DEFS.get(b, ""))}">{esc(b)}</span>' for b in self.badges.get(name, []))
            ships = ", ".join(f"{s} x{n}" if n > 1 else s for s, n in p["ships"].most_common())
            rows.append(f'<tr data-damage="{p["damage"]:.0f}" data-smokes="{p["smokes"]}" data-avg="{p["damage"] / p["smokes"]:.0f}" data-selfish="{p["selfish"]}" data-radar="{p["radar"]}" data-won="{p["won"]}" data-offensive="{p["offensive"]}"><td>{self.team_tag(p["team"])}</td><td><a href="{self.player_href(name)}">{esc(name)}</a> {badges}</td><td class="small">{esc(ships)}</td><td>{p["smokes"]}</td><td>{fmt_int(p["damage"])}</td><td>{fmt_int(p["damage"] / p["smokes"])}</td><td>{p["selfish"]}</td><td>{p["radar"]}</td><td>{p["won"]}</td><td>{p["offensive"]}</td></tr>')
        pawards = "".join(f'<div class="card award-p"><h3>{term(t, AWARD_DEFS.get(t, ""))}</h3><p>{self.team_tag(p["team"])} <a href="{self.player_href(name)}"><b>{esc(name)}</b></a></p><p class="note">{esc(self.player_award_note(t, p))}</p></div>' if name else f'<div class="card award-p"><h3>{esc(t)}</h3><p class="muted">Nothing here, just clear skies.</p></div>' for t, (name, p) in self.awards["players"].items())
        body = f"""<h1>Players</h1><p class="muted">Click a column heading to sort. Badges are awards; hover for the rule. No limit on awards per player.</p>
<h2>Player awards</h2><section class="cards">{pawards}</section>
<h2>Leaderboard (n = {len(self.players)} players)</h2><div class="scroll-x"><table class="games sortable" id="players"><thead><tr><th>Clan</th><th>Player</th><th>Ships</th><th data-key="smokes">Smokes</th><th data-key="damage">Smoke damage</th><th data-key="avg">Per smoke</th><th data-key="selfish">{term("Selfish")}</th><th data-key="radar">Radar spots</th><th data-key="won">{term("Near cap capture", METRIC_DEFS["won"])}</th><th data-key="offensive">{term("Own radar spots", METRIC_DEFS["offensive"])}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>"""
        self.write("players.html", self.page("Players", body, active="Players"))

    def player_award_note(self, title, p):
        if title == "Golden Cloud":
            return f"{fmt_int(p['damage'])} damage over {p['smokes']} smokes"
        if title == "The Smokefather":
            return f"{p['smokes']} smokes in {len(p['games'])} games"
        if title == "Best in Haze":
            return f"{fmt_int(p['damage'] / p['smokes'])} per smoke over {p['smokes']} smokes"
        return f"{p['selfish']} selfish smokes of {p['smokes']}"

    def player_page(self, name):
        p = self.players[name]
        rows = [s for s in self.d.smokes if s["player"] == name]
        badges = "".join(f'<span class="badge" title="{esc(AWARD_DEFS.get(b, ""))}">{esc(b)}</span>' for b in self.badges.get(name, [])) or '<span class="muted small">no awards</span>'
        ships = svg_donut(p["ships"].most_common(), PALETTE)
        kv = f"""<table class="kv"><tr><td>Smokes laid</td><td>{p['smokes']} in {len(p['games'])} games</td></tr><tr><td>Smoke damage</td><td>{fmt_int(p['damage'])}</td></tr><tr><td>Average per smoke</td><td>{fmt_int(p['damage'] / p['smokes'])}</td></tr>
<tr><td>{term('Selfish smokes')}</td><td>{p['selfish']}</td></tr><tr><td>Radar spots on the team inside</td><td>{p['radar']}</td></tr><tr><td>{term('Smokes near a cap capture', METRIC_DEFS['won'])}</td><td>{p['won']}</td></tr><tr><td>{term('Enemies spotted by own radar', METRIC_DEFS['offensive'])}</td><td>{p['offensive']}</td></tr></table>"""
        cards = "".join(self.smoke_card(s, depth=1, note=f"{phase_of(s['_elapsed']) or ''}") for s in sorted(rows, key=lambda s: -s["_total"]))
        timeline = bar_chart(f"Damage per smoke, top 12 (n = {len(rows)})", [(s["_act_clock"], s["_total"], self.color(p["team"]), None) for s in sorted(rows, key=lambda s: -s["_total"])[:12]])
        body = f"""<h1>{self.team_tag(p['team'])} {esc(name)}</h1><p>{badges}</p>
<div class="two-col"><div class="card"><h3>Stats</h3>{kv}</div><div class="card"><h3>Ships</h3>{ships}{timeline}</div></div>
<h2>Smokes</h2><section class="cards">{cards}</section>
<p><a href="../players.html">Back to the leaderboard</a> | <a href="{self.clan_href(p['team'], 1)}">the clan page</a></p>"""
        self.write(f"players/{slug(name)}.html", self.page(name, body, depth=1, active="Players"))

    def awards_redirect(self):
        body = '<h1>Awards</h1><p>The awards moved: smoke awards are on <a href="index.html">Home</a>, player awards on <a href="players.html">Players</a> and clan awards on each <a href="clans.html">clan page</a>.</p>'
        self.write("awards.html", self.page("Awards", body))

    def map_figure(self, map_name, smokes, depth=0, size=768, anchor_prefix="smoke", fig_id="map"):
        d = self.d
        m = d.maps.get(map_name)
        base = "../" * depth
        if not m:
            return '<p class="muted">Map image missing.</p>'
        step = NATIVE / 10
        grid = "".join(f'<line x1="{i * step:.0f}" y1="0" x2="{i * step:.0f}" y2="{NATIVE}"/><line x1="0" y1="{i * step:.0f}" x2="{NATIVE}" y2="{i * step:.0f}"/>' for i in range(1, 10))
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
            title = f'{s["player"]} {s["ship"]} at {s["_act_clock"]} ({elapsed_text(elapsed) if elapsed >= 0 else "?"} elapsed), {fmt_int(s["_total"])} dmg, {s.get("smoke_type") or ""} smoke'
            paths.append(f'<a href="{base}{self.smoke_href[s["_slug"]]}" id="{anchor_prefix}-{s["_slug"]}" class="smokepath" {data}><polyline points="{points}" stroke="{self.color(s["team"])}"{dashed} marker-end="url(#{marker})"><title>{esc(title)}</title></polyline></a>')
        return f'<div class="mapwrap" style="max-width:{size}px"><img src="{base}maps/{m["map"]}.webp" alt="{esc(self.d.map_title(map_name))}"><svg viewBox="0 0 {NATIVE} {NATIVE}"><defs>{markers}</defs><g class="grid">{grid}</g><g class="gridlabels">{labels}</g><g class="caps">{"".join(caps)}</g><g class="paths">{"".join(paths)}</g></svg></div>'

    def maps_page(self):
        d = self.d
        sections = []
        by_map = defaultdict(list)
        for s in d.smokes:
            by_map[s["map"]].append(s)
        for n, (map_name, smokes) in enumerate(sorted(by_map.items(), key=lambda kv: -len(kv[1]))):
            counts = Counter(s["team"] for s in smokes)
            near = sum(1 for s in smokes if s.get("avg_contested_cap_dist_m") is not None and s["avg_contested_cap_dist_m"] <= 1000)
            games = len({s["_key"] for s in smokes})
            take = [
                f"{len(smokes)} smokes in {games} games: " + ", ".join(f"{t} {n}" for t, n in counts.most_common()) + ".",
                f"{near / len(smokes) * 100:.0f}% stood within 1 km of a contested cap on average.",
                f"Average smoke damage {fmt_int(sum(s['_total'] for s in smokes) / len(smokes))} (n = {len(smokes)}).",
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
<label class="range">Time elapsed <span class="rangevals"><b class="lo">0:00</b> to <b class="hi">20:00</b></span><span class="dual"><input type="range" class="t-lo" min="0" max="{MATCH_SECONDS}" value="0" step="10"><input type="range" class="t-hi" min="0" max="{MATCH_SECONDS}" value="{MATCH_SECONDS}" step="10"></span><span class="muted small">smokes activated between the handles; battle start on the left, 20:00 on the right</span></label>
<label>Clan <select class="f-clan"><option value="">all</option>{clans}</select></label>
<label>Spawn{spawn_note} <select class="f-spawn"><option value="">both</option>{spawns}</select></label>
<label>Ship <select class="f-ship"><option value="">all</option>{ships}</select></label>
<span class="count muted"></span></div>"""
            sections.append(f'<section class="map-section" data-map="{esc(map_name)}"><h2>{esc(self.d.map_title(map_name))}</h2>{filters}<div class="two-col mapcol">{fig}<div><h3>By clan, for the smokes shown</h3><p class="muted small">Clans with fewer than 5 smokes shown are greyed out.</p><div class="chart"></div></div></div><ul class="takeaways">{"".join(f"<li>{esc(t)}</li>" for t in take if t)}</ul></section>')
        legend = "".join(f'<span class="legend"><i style="background:{self.color(t)}"></i>{esc(t)}</span>' for t in TEAMS if any(s["team"] == t for s in d.smokes))
        body = f"""<h1>Maps</h1><p class="muted">One line per smoke: its puffs in laying order with an arrow at the end, coloured by team. Exhaust and crawling smokes are dashed. Circles are the capture zones. Click a line to open the smoke. The filters apply to the map and its four charts. Spawn labels follow each map's real spawns.</p><div class="legend-row">{legend}<span class="legend"><i style="background:#CBD5E1"></i>standard and cruiser smoke: solid</span><span class="legend"><i style="background:#CBD5E1;opacity:.5"></i>exhaust and crawling: dashed</span></div>{''.join(sections)}
<script>window.TEAM_COLORS = {json.dumps(self.colors)}; window.SELFISH_DEF = {json.dumps(SELFISH_DEF)}; window.CONTEST_DEF = {json.dumps(CONTEST_DEF)};</script>"""
        self.write("maps.html", self.page("Maps", body, active="Maps"))

    def series(self):
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
            rows += f'<div class="srow{" won" if t == s["winner"] else ""}">{self.team_tag(t)} <span class="sname">{esc(t)}</span><b>{w}</b></div>'
        return f'<a class="series" href="{href}">{rows}<div class="muted small">{esc(s["date"])}</div></a>'

    def games_page(self):
        d = self.d
        series = self.series()
        cols = []
        for rnd, title, count in BRACKET:
            items = sorted((s for s in series.values() if s["round"] == rnd), key=lambda s: s["match_id"])
            boxes = [self.series_box(s) for s in items]
            for _ in range(max(0, count - len(items))):
                boxes.append('<div class="series tbd"><div class="srow"><span class="tag other">TBD</span> <span class="sname">TBD</span></div><div class="srow"><span class="tag other">TBD</span> <span class="sname">TBD</span></div><div class="muted small">not in the replay set</div></div>')
            cols.append(f'<div class="bcol"><h3>{esc(title)}</h3>{"".join(boxes)}</div>')
        winners = "".join(cols[:4])
        losers = "".join(cols[4:10])
        final = cols[10]
        bracket = f'<div class="bracket"><div class="bside"><h4>Winners bracket</h4><div class="brow">{winners}</div><h4>Losers bracket</h4><div class="brow">{losers}</div></div><div class="bfinal">{final}</div></div>'
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
<p class="warn">Prototype: only series with H-SR or RESIN replays are linked so far.</p>
<h2>Playoffs</h2><p class="muted">Double elimination. Each box is a series; the numbers are games won. Click a linked series for its games. Greyed boxes are series not in the replay set.</p>
{bracket}
<h2>Group stage</h2>
<div class="filters"><label>Clan <select id="g-clan"><option value="">all</option>{clan_opts}</select></label><label>Map <select id="g-map"><option value="">all</option>{map_opts}</select></label><span id="g-count" class="muted"></span></div>
<div class="scroll-x"><table class="games" id="games"><thead><tr><th>Round</th><th>Date</th><th>Teams</th><th>Map</th><th>Score</th><th>Winner</th><th></th></tr></thead><tbody>{"".join(group_rows)}</tbody></table></div>
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
<div class="scroll-x"><table class="games"><thead><tr><th>Game</th><th>Map</th><th>Score</th><th>Winner</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p><a href="../games.html">Back to the bracket</a></p>"""
        self.write(f"games/series_{s['match_id']}.html", self.page(title, body, depth=1, active="Games"))

    def all_smokes(self):
        d = self.d
        records = []
        for s in d.smokes:
            records.append({
                "id": s["smoke_id"], "team": s["team"], "player": s["player"], "ship": s["ship"], "map": self.d.map_title(s["map"]),
                "game": s["_games_label"], "game_href": f"games/{s['_match']}_g{s['game_no']}.html", "type": s.get("smoke_type") or "",
                "clock": s["_act_clock"], "elapsed": s["_elapsed"], "phase": s["_phase"] or "", "total": round(s["_total"]), "inside": round(s["_in"]), "behind": round(s["_behind"]), "fire": round(s["_fire"]),
                "radar": s["_radar"], "offensive": s["_offensive"], "duration": round(s["_duration"]) if s.get("_duration") is not None else None,
                "swing": s["_score_swing"], "cap": s.get("cap_proximity_m"), "cap_name": s.get("cap_proximity_name") or "",
                "contested": s.get("avg_contested_cap_dist_m"), "contested_name": s.get("contested_cap_name") or "", "depth": s["_depth"],
                "won": s.get("cap_won") or "", "defended": s.get("cap_defended") or "",
                "selfish": bool(s.get("selfish_smoke")), "flag": bool(s.get("owner_flag")), "overlap": bool(s.get("overlap_flag")), "thumb": s.get("_diag") or "", "href": self.smoke_href[s["_slug"]],
                "color": self.color(s["team"]),
            })
        max_total = max((r["total"] for r in records), default=1)
        body = f"""<h1>Smokes</h1><p class="muted">Every analysed smoke (n = {len(records)}). Damage counts main-gun shells plus the fires they started, one smoke per shot.</p>
<div class="filters">
<label>Team <select id="f-team"><option value="">all</option></select></label>
<label>Player <select id="f-player"><option value="">all</option></select></label>
<label>Ship <select id="f-ship"><option value="">all</option></select></label>
<label>Map <select id="f-map"><option value="">all</option></select></label>
<label>Game <select id="f-game"><option value="">all</option></select></label>
<label>Type <select id="f-type"><option value="">all</option></select></label>
<label>Phase <select id="f-phase"><option value="">all</option></select></label>
<label>Sort <select id="f-sort"><option value="total">smoke damage (total)</option><option value="inside">damage in smoke</option><option value="behind">damage behind smoke</option><option value="fire">fire damage</option><option value="radar">radar spots on the team inside</option><option value="offensive">enemies spotted by own radar</option><option value="duration">duration</option><option value="swing">score change during the smoke</option><option value="depth">depth into a contested cap</option><option value="cap">cap proximity (nearest first)</option><option value="contested">average distance to a contested cap (nearest first)</option></select></label>
<span id="count" class="muted"></span></div>
<div class="scroll-x"><table class="smokes" id="smokes"><thead><tr><th></th><th>Team</th><th>Player</th><th>Ship</th><th>Map</th><th>Game</th><th>Clock</th><th>Damage</th><th>Cap proximity (outside caps)</th><th><abbr class="term" title="{esc(CONTEST_DEF)}">Contested cap</abbr> (average)</th><th>Cap outcome</th><th>Radar</th><th></th></tr></thead><tbody></tbody></table></div>
<p id="empty" class="muted" hidden>Nothing here, just clear skies.</p>
<script>window.SMOKES = {json.dumps(records)}; window.MAX_TOTAL = {max_total}; window.SELFISH_DEF = {json.dumps(SELFISH_DEF)};</script>"""
        self.write("smokes.html", self.page("Smokes", body, active="Smokes"))

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
            end_clock = (g.get("battle_end") or {}).get("clock", "?")
            rem = clock_remaining_seconds(end_clock)
            phase = d.game_end_phase.get(key)
            header.append(f"Ended by {g.get('finish_type') or '?'} at {end_clock}" + (f" ({elapsed_text(MATCH_SECONDS - rem)} elapsed, {phase})" if rem is not None and phase else ""))
        links = [f'<a href="../games.html">all games</a>']
        if inv and inv["stage"] == "Playoffs":
            links.append(f'<a href="series_{inv["match_id"]}.html">this series</a>')
        roster = ""
        for t in teams:
            rows = "".join(f"<tr><td>{esc(p['player'])}</td><td>{esc(p['ship'])}</td><td>{p['smoke_activations'] or ''}{('/' + str(p['smoke_charges'])) if p.get('smoke_charges') else ''}</td></tr>" for p in t["players"])
            roster += f'<div class="card"><h3>{self.team_tag(t["name"])} {esc(t["name"])} <span class="muted small">{esc(t.get("spawn_side") or "")} spawn</span></h3><table class="roster"><tr><th>Player</th><th>Ship</th><th>Smokes used/carried</th></tr>{rows}</table></div>'
        recon = ""
        for (team, k), sp in d.spikes.items():
            if k != key or not sp.get("reconciliation"):
                continue
            rows = "".join(f'<tr><td>{esc(r["player"])}</td><td>{fmt_int(r["game_total"])}</td><td>{fmt_int(r["ledger_total"])}</td><td>{fmt_int(r["game_shell_fire"])}</td><td>{fmt_int(r["ledger_shell_fire"])}</td></tr>' for r in sp["reconciliation"])
            ratio = sp.get("reconciliation_ratio_shell_fire")
            label = f"ledger shell plus fire = {ratio * 100:.0f}% of the game's main battery plus fire" if ratio else "no per-type totals"
            recon = f'<details><summary>Damage check: the replay ledger against the game\'s own totals ({label})</summary><div class="scroll-x"><table class="games"><thead><tr><th>Player</th><th>Game total</th><th>Ledger total</th><th>Game main battery + fire</th><th>Ledger shell + fire</th></tr></thead><tbody>{rows}</tbody></table><p class="muted small">Source: {esc(sp.get("reconciliation_source") or "")}</p></div></details>'
            break
        timeline = self.timeline_svg(smokes, g)
        score = self.score_svg(smokes, teams, g)
        cards = "".join(self.smoke_card(s, depth=1) for s in smokes)
        body = f"""<h1>{esc(smokes[0]['_games_label'])}</h1><p class="muted">{" | ".join(esc(h) for h in header)} | {" | ".join(links)}</p>
<section class="two-col">{self.map_figure(smokes[0]['map'], smokes, depth=1, size=480, anchor_prefix='g', fig_id='g')}<div><h2>Smokes across the match (n = {len(smokes)})</h2>{timeline}<h2>Score with smoke markers</h2>{score}</div></section>
<h2>Rosters</h2><section class="cards rosters">{roster}</section>{recon}
<h2>Smokes in this game</h2><section class="cards">{cards}</section>"""
        self.write(f"games/{key[0]}_g{key[1]}.html", self.page(smokes[0]["_games_label"], body, depth=1))

    def game_span(self, g):
        """Seconds of play shown on a single game's axes: its real length."""
        rem = clock_remaining_seconds(((g or {}).get("battle_end") or {}).get("clock"))
        return (MATCH_SECONDS - rem) if rem is not None else MATCH_SECONDS

    def timeline_svg(self, smokes, g):
        span = max(60, self.game_span(g))
        w, h = 520, 70
        out = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" class="timeline">', f'<line x1="10" y1="40" x2="{w - 10}" y2="40" stroke="#475569"/>']
        ticks = 5 if span > 600 else 2
        m = 0
        while m * 60 <= span:
            x = 10 + (w - 20) * m * 60 / span
            out.append(f'<text x="{x:.0f}" y="62" fill="#94A3B8" font-size="10" text-anchor="middle">{m}:00</text>')
            m += ticks
        out.append(f'<text x="{w - 10}" y="12" fill="#94A3B8" font-size="10" text-anchor="end">minutes elapsed; this game ran {elapsed_text(span)}</text>')
        for s in smokes:
            if s["_elapsed"] is None:
                continue
            x = 10 + (w - 20) * s["_elapsed"] / span
            dur = s.get("_duration") or 0
            x2 = min(w - 10, x + (w - 20) * dur / span)
            out.append(f'<a href="../{self.smoke_href[s["_slug"]]}"><rect x="{x:.0f}" y="30" width="{max(2, x2 - x):.0f}" height="20" fill="{self.color(s["team"])}" opacity="0.8"><title>{esc(s["player"])} {esc(s["ship"])} at {esc(s["_act_clock"])}</title></rect></a>')
        out.append("</svg>")
        return "".join(out)

    def score_svg(self, smokes, teams, g):
        span = max(60, self.game_span(g))
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
            return 10 + (w - 20) * t / span, h - 20 - (h - 40) * v / max(1000, max_score)

        out = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" class="score">']
        team_names = [t["name"] for t in teams] or sorted({p[1] for p in points})
        series = {}
        for t, team, ours, theirs in points:
            other = next((n for n in team_names if n != team), "other")
            series.setdefault(team, []).append(xy(t, ours))
            series.setdefault(other, []).append(xy(t, theirs))
        for team, pts in series.items():
            pts.sort()
            dd = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
            out.append(f'<polyline points="{dd}" fill="none" stroke="{self.color(team)}" stroke-width="2"/>')
        for s in smokes:
            if s["_elapsed"] is None:
                continue
            x, _ = xy(s["_elapsed"], 0)
            out.append(f'<line x1="{x:.0f}" y1="10" x2="{x:.0f}" y2="{h - 20}" stroke="{self.color(s["team"])}" stroke-dasharray="3,3" opacity="0.6"/>')
        out.append(f'<text x="10" y="{h - 4}" fill="#94A3B8" font-size="10">0:00 elapsed</text><text x="{w - 10}" y="{h - 4}" fill="#94A3B8" font-size="10" text-anchor="end">{elapsed_text(span)}</text>')
        out.append("".join(f'<text x="{14 + i * 90}" y="14" fill="{self.color(t)}" font-size="11">{esc(t)}</text>' for i, t in enumerate(series)))
        out.append("</svg>")
        return "".join(out)

    def smoke_page(self, s):
        d = self.d
        game = d.by_game[s["_key"]]
        idx = game.index(s)
        prev_s = game[idx - 1] if idx > 0 else None
        next_s = game[idx + 1] if idx + 1 < len(game) else None
        st = s.get("state_at_capture") or s.get("state_at_activate") or {}
        alive = ", ".join(f"{a.get('team')} {a.get('ship_class') or ''} {a.get('alive', a.get('count', ''))}" for a in (st.get("ships_alive") or [])) if st else ""
        split = svg_stacked_bar([("fired from inside", s["_in"]), ("fired from outside, hidden by it", s["_behind"])], ["#F5C542", "#5DADE2"]) if s["_total"] > 0 else '<p class="muted small">No smoke damage.</p>'
        kinds = svg_stacked_bar([("shells", s["_shell"]), ("fires started by them", s["_fire"])], ["#CBD5E1", "#FB923C"]) if s["_total"] > 0 else ""
        clip = f'<div class="clip"><video controls preload="metadata" src="../{s["_clip"]}"></video><div class="clip-controls"><button class="speed" data-rate="1">1x (5x real time)</button><button class="speed" data-rate="2">2x (10x real time)</button></div></div>' if s.get("_clip") else '<p class="muted small">Clip available on request.</p>'
        nav = []
        if prev_s:
            nav.append(f'<a href="{prev_s["_slug"]}.html">&larr; previous smoke in this game</a>')
        nav.append(f'<a href="../games/{s["_match"]}_g{s["game_no"]}.html">up to the game</a>')
        nav.append(f'<a href="../maps.html#smoke-{s["_slug"]}">its path on the map</a>')
        nav.append(f'<a href="{self.player_href(s["player"], 1)}">the player</a>')
        if next_s:
            nav.append(f'<a href="{next_s["_slug"]}.html">next smoke in this game &rarr;</a>')
        flag = f'<p class="warn">Owner attribution flagged: {esc(s.get("owner_note"))}</p>' if s.get("owner_flag") else ""
        overlap = ""
        if s.get("overlap_flag"):
            others = ", ".join(str(i) for i in s.get("overlapping_smoke_ids") or [])
            overlap = f'<p class="muted small">Overlapped smoke {others}; every shot was credited to one smoke (the one the shooter sat in, else the first laid), so nothing is counted twice.</p>'
        dur = f"{s['_duration']:.0f} s" if s.get("_duration") is not None else "still standing at the end"
        selfish = 'yes' if s.get('selfish_smoke') else ('no' if s.get('selfish_smoke') is not None else 'unknown')
        rc = s.get("radar_cap")
        radar_cap = f"{rc['coverage_pct']:.0f}% of cap {rc['cap']} within {rc.get('ship') or 'a radar ship'}'s radar range{', the whole cap' if rc.get('full') else ''}; radar {'was' if rc.get('activated') else 'was not'} activated from the smoke" if rc else "no concealed radar ship inside"
        den = s.get("cap_denial")
        denial = f"{den['enemies_before']:.1f} enemy ships in or near cap {den['cap']} in the minute before, {den['enemies_during']:.1f} while the smoke stood" if den else "-"
        o = s.get("offensive_radar")
        offensive = f"{o['enemies_spotted']} enemies spotted over {o['activations']} activation(s) by {o.get('ship') or 'a radar ship'} (inferred from the activation and radar range)" if o else "none"
        shooters = ", ".join(s.get("shooters") or []) or "none"
        body = f"""<h1>{self.team_tag(s['team'])} <a href="{self.player_href(s['player'], 1)}">{esc(s['player'])}</a> <span class="muted">{esc(s['ship'])}</span></h1>
<p class="muted">{esc(self.d.map_title(s['map']))} | {esc(s['_games_label'])} | activated {esc(s['_act_clock'])} ({elapsed_text(s['_elapsed']) if s['_elapsed'] is not None else '?'} elapsed, {s['_phase'] or ''}), captured {esc(s['_cap_clock'])} | {esc(s.get('smoke_type') or '')} smoke {esc(s.get('variant') or '')}</p>
<p class="summary">{esc(self.summary_line(s))}</p>
<p class="big">{fmt_int(s['_total'])} smoke damage</p>{flag}{overlap}
<section class="frames two">{self.img(s, 'frame_act', 1, lazy=False)}{self.img(s, 'frame_cap', 1, lazy=False)}</section>
<section class="frames three"><figure>{self.img(s, 'frame_act_zoom', 1, lazy=False)}<figcaption>Zoomed screenshot at activation</figcaption></figure><figure>{self.img(s, 'frame_cap_zoom', 1, lazy=False)}<figcaption>Zoomed screenshot at capture</figcaption></figure><figure>{self.thumb(s, 1)}<figcaption>Diagram: puffs, caps, nearby ships (team colour = ours, red = enemy, ring = smoker) and credited shots labelled with damage</figcaption></figure></section>
{clip}
<section class="two-col"><div class="card"><h3>Stats</h3><table class="kv">
<tr><td>Duration</td><td>{esc(dur)}</td></tr>
<tr><td>Smoke damage, by where the shooter sat</td><td>{split}</td></tr>
<tr><td>Smoke damage, by kind</td><td>{kinds or '-'}</td></tr>
<tr><td>Shooters credited</td><td>{esc(shooters)} ({s['_salvos']} salvos)</td></tr>
<tr><td>Radar spots on the team inside</td><td>{s['_radar']}{(' (' + fmt_int(s['_radar_dmg']) + ' damage taken while spotted)') if s['_radar'] else ''}</td></tr>
<tr><td>{term('Own radar from the smoke', METRIC_DEFS['offensive'])}</td><td>{esc(offensive)}</td></tr>
<tr><td>Cap proximity at capture</td><td>{esc(cap_text(s))}</td></tr>
<tr><td>{term('Contested cap', CONTEST_DEF)}</td><td>{esc(contested_text(s))}</td></tr>
<tr><td>Supported caps (in stock gun range of a concealed ship)</td><td>{esc(', '.join(s.get('supported_caps') or [])) or 'none'}</td></tr>
<tr><td>Cap outcome</td><td>{esc(cap_outcome_text(s))}</td></tr>
<tr><td>{term('Radar cap coverage', METRIC_DEFS['coverage'])}</td><td>{esc(radar_cap)}</td></tr>
<tr><td>Denial signal</td><td>{esc(denial)}</td></tr>
<tr><td>Allies in smoke at capture</td><td>{esc(', '.join(s.get('allies_in_smoke') or [])) or 'none'}</td></tr>
<tr><td>{term('Selfish smoke')}</td><td>{selfish}</td></tr>
<tr><td>Score at capture</td><td>{esc(st.get('score_ours', '-'))} : {esc(st.get('score_theirs', '-'))}{(' (swing ' + f"{s['_score_swing']:+d}" + ')') if s['_score_swing'] is not None else ''}</td></tr>
<tr><td>Smoker alive 60 s after</td><td>{'yes' if s['_survived'] else ('no' if s['_survived'] is not None else 'unknown')}</td></tr>
<tr><td>Ships alive at capture</td><td>{esc(alive) or '-'}</td></tr></table></div>
<div class="card"><h3>Tags</h3><p class="muted">untagged</p></div></section>
<nav class="smoke-nav">{" | ".join(nav)}</nav>"""
        self.write(f"smokes/{s['_slug']}.html", self.page(f"{s['player']} {s['ship']} {s['_act_clock']}", body, depth=1, active="Smokes"))


FALLBACK_MAP_TITLES = {"16_OC_bees_to_honey": "Hotspot", "45_Zigzag": "Loop", "40_Okinawa": "Okinawa", "22_tierra_del_fuego": "Land of Fire", "58_RidgeNew": "Mountain Range", "47_Sleeping_Giant": "Sleeping Giant", "25_sea_hope": "Sea of Fortune"}
SMOKE_TYPES = [("standard", "#CBD5E1"), ("cruiser", "#6EE7B7"), ("exhaust", "#FB923C"), ("crawling", "#F472B6")]


CSS = """:root{--bg:#0B1C2C;--panel:#16283A;--panel2:#1E3448;--text:#EEF2F5;--muted:#9FB0C0;--line:#2A4258;__TEAMCOLORS__}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.45 "Segoe UI",system-ui,sans-serif}
main{max-width:1180px;margin:0 auto;padding:16px}h1,h2,h3,h4{margin:.6em 0 .3em}h1{font-size:1.7em}h2{font-size:1.25em;border-bottom:1px solid var(--line);padding-bottom:4px}
a{color:#9CD3FF}nav.top{display:flex;gap:4px;align-items:center;background:#07131f;padding:8px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5;flex-wrap:wrap}
nav.top .brand{font-weight:700;letter-spacing:.04em;margin-right:12px;color:#F5C542}nav.top .links{display:flex;gap:4px;flex-wrap:wrap}nav.top a{padding:6px 10px;border-radius:6px;color:var(--text);text-decoration:none}nav.top a.active,nav.top a:hover{background:var(--panel2)}
nav.top .navtoggle,nav.top .navbtn{display:none}
footer{color:var(--muted);font-size:.85em;text-align:center;padding:24px 16px}
abbr.term{text-decoration:underline dotted;cursor:help}
.briefing{background:var(--panel);border-left:6px solid #F5C542;padding:16px 20px;border-radius:8px;margin:16px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin:8px 0 20px}.cards.awards{grid-template-columns:repeat(auto-fill,minmax(520px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px;color:var(--text);text-decoration:none;display:block}.card.toc h2{border:0;margin-top:0}
.smoke-card{padding:0;overflow:hidden}.smoke-card img{width:100%;display:block;aspect-ratio:1;object-fit:cover;background:#0B1C2C}.card-body{padding:8px 10px}
.award-hero{display:flex;gap:14px;align-items:flex-start;margin:8px 0}.award-hero>a{flex:0 0 240px;max-width:48%}.award-hero img{width:100%;height:auto;display:block;border-radius:8px;border:1px solid var(--line)}.award-meta{flex:1;min-width:0}.award-meta .big{margin:6px 0}
.card.award .clip{margin-top:8px}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 20px}.stat{background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--c,#9FB0C0);border-radius:8px;padding:8px 14px;min-width:150px}.stat b{display:block;font-size:1.5em}.stat span{color:var(--muted);font-size:.85em}.stats.lead .stat{min-width:220px;border-width:1px 1px 1px 8px}.stats.lead .stat b{font-size:2em}
.tag{display:inline-block;padding:1px 7px;border-radius:999px;font-size:.78em;font-weight:700;background:var(--c);color:#07131f}.tag.other{background:#475569;color:var(--text)}
.badge{display:inline-block;padding:1px 7px;border-radius:6px;font-size:.75em;background:#2A4258;color:#F5C542;margin-left:4px;cursor:help}
.muted{color:var(--muted)}.small{font-size:.85em}.big{font-size:1.4em;font-weight:700}.note{color:#F5C542}.warn{color:#FB923C}.summary{background:var(--panel2);padding:8px 12px;border-radius:8px}
table.kv td{padding:3px 8px 3px 0;vertical-align:top}table.kv td:first-child{color:var(--muted);max-width:260px}
.mini{display:inline-block;width:92px;height:9px;background:#0B1C2C;border-radius:4px;vertical-align:middle;margin-left:6px}.mini i{display:block;height:100%;border-radius:4px}
.legend-row{display:flex;flex-wrap:wrap;gap:8px;font-size:.8em;margin-top:4px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px}
.frames.two{display:grid;grid-template-columns:1fr 1fr;gap:8px}.frames.three{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:8px 0}.frames img{width:100%;border-radius:6px;border:1px solid var(--line)}.frames figure{margin:0}.frames figcaption{color:var(--muted);font-size:.8em;margin-top:4px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.mapwrap{position:relative;width:100%}.mapwrap img{width:100%;display:block;border-radius:8px}.mapwrap svg{position:absolute;inset:0;width:100%;height:100%}
.mapwrap .grid line{stroke:#fff;stroke-opacity:.18;stroke-width:1}.mapwrap .gridlabels text{fill:#fff;fill-opacity:.7;font-size:12px;text-anchor:middle;font-weight:600}
.mapwrap .caps circle{fill:#fff;fill-opacity:.08;stroke:#fff;stroke-opacity:.6;stroke-width:1.5;stroke-dasharray:5,4}.mapwrap .caplabel{fill:#fff;fill-opacity:.85;font-size:20px;font-weight:700;text-anchor:middle}
.mapwrap .smokepath polyline{fill:none;stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round;opacity:.9}.mapwrap .smokepath:hover polyline{stroke-width:6;opacity:1}.mapwrap .smokepath[hidden]{display:none}
.mapcol{grid-template-columns:3fr 2fr}.chart{display:grid;gap:10px}.charts{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:12px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px}.panel h4{margin:0 0 4px;font-size:.9em;color:var(--muted)}
svg.chart .lbl{fill:var(--text);font-size:11px}svg.chart .val{fill:var(--muted);font-size:11px}svg.chart .zero{stroke:#94A3B8;stroke-width:1}
.chart .row{display:grid;grid-template-columns:52px 1fr 90px;align-items:center;gap:6px;font-size:.85em;margin:2px 0}.chart .row .bar{position:relative;height:12px;background:#0B1C2C;border-radius:3px}.chart .row .bar i{position:absolute;top:0;height:100%;border-radius:3px}.chart .row .bar b{position:absolute;top:-2px;bottom:-2px;width:1px;background:#94A3B8}.chart .row span:last-child{text-align:right}.chart .row.dim{opacity:.4}
.heats{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}.heat{margin:0}.heat figcaption{font-size:.8em;color:var(--muted);margin-top:4px}
.filters.mapfilters{align-items:flex-start}.range{min-width:320px}.rangevals{margin-left:6px}.dual{position:relative;display:block;height:22px}.dual input[type=range]{position:absolute;left:0;top:0;width:100%;margin:0;background:none;pointer-events:none;-webkit-appearance:none;appearance:none;height:22px}
.dual input[type=range]::-webkit-slider-runnable-track{height:4px;background:var(--line);border-radius:2px}
.dual input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;pointer-events:auto;width:16px;height:16px;border-radius:50%;background:#F5C542;border:2px solid #07131f;margin-top:-6px;cursor:pointer}
.dual input[type=range]::-moz-range-track{height:4px;background:var(--line)}.dual input[type=range]::-moz-range-thumb{pointer-events:auto;width:14px;height:14px;border-radius:50%;background:#F5C542;border:2px solid #07131f;cursor:pointer}
.bracket{display:flex;gap:16px;overflow-x:auto;padding:4px 0 12px}.bside{flex:1 1 auto}.bside h4{margin:6px 0;color:var(--muted)}.brow{display:flex;gap:10px}.bfinal{display:flex;align-items:center}.bcol{display:flex;flex-direction:column;justify-content:space-around;gap:8px;flex:1 1 0;min-width:150px}.bcol h3{margin:0;font-size:.85em;color:var(--muted);text-align:center}
.series,a.series{display:block;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:6px 8px;color:var(--text);text-decoration:none;font-size:.9em}a.series:hover{border-color:#9CD3FF}.series.tbd{opacity:.45}.srow{display:flex;align-items:center;gap:6px;padding:2px 0}.srow .sname{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.srow.won{font-weight:700}.srow.won b{color:#F5C542}
table.games{width:100%;border-collapse:collapse;font-size:.9em}table.games th,table.games td{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left}table.games tr[hidden]{display:none}table.sortable th[data-key]{cursor:pointer;text-decoration:underline dotted}
.scroll-x{overflow-x:auto;max-width:100%}
.takeaways{margin:8px 0 20px}.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:end;margin:10px 0}.filters label{display:flex;flex-direction:column;font-size:.8em;color:var(--muted)}
select{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 6px}
table.smokes{width:100%;border-collapse:collapse;font-size:.9em}table.smokes th,table.smokes td{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}table.smokes img{width:56px;height:56px;object-fit:cover;border-radius:4px;background:#0B1C2C}
.cards.rosters{grid-template-columns:repeat(auto-fit,minmax(380px,1fr))}table.roster{width:100%;font-size:.85em;border-collapse:collapse}table.roster th{text-align:left;color:var(--muted)}table.roster td,table.roster th{padding:2px 6px 2px 0}table.roster td:last-child{text-align:right}
.clip video{width:100%;max-width:900px;border-radius:8px;background:#000}.clip-controls{margin:6px 0}.clip-controls button{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 10px;margin-right:6px;cursor:pointer}.clip-controls button.on{background:#F5C542;color:#07131f}
.smoke-nav{margin:20px 0;display:flex;gap:12px;flex-wrap:wrap}.findings li{margin:10px 0}.findings .panel{margin-top:6px}.noimg{background:var(--panel2);color:var(--muted);padding:30px;text-align:center;border-radius:6px}
@media(max-width:800px){.two-col,.frames.two,.frames.three,.mapcol{grid-template-columns:1fr}.award-hero{flex-direction:column}.award-hero>a{flex:none;max-width:100%}.cards.awards,.charts{grid-template-columns:1fr}.brow{flex-direction:column}.bcol{min-width:0}
nav.top .navbtn{display:inline-block;margin-left:auto;padding:6px 10px;border:1px solid var(--line);border-radius:6px;cursor:pointer}nav.top .links{display:none;width:100%;flex-direction:column}nav.top .navtoggle:checked~.links{display:flex}.range{min-width:0;width:100%}}
"""

JS = r"""(function(){
  document.querySelectorAll('.clip').forEach(function(c){
    var v = c.querySelector('video');
    c.querySelectorAll('button.speed').forEach(function(b){
      b.addEventListener('click', function(){ v.playbackRate = parseFloat(b.dataset.rate); c.querySelectorAll('button.speed').forEach(function(x){x.classList.toggle('on', x===b);}); });
    });
    var first = c.querySelector('button.speed'); if (first) first.classList.add('on');
  });
  function clockText(elapsed){ var m = Math.floor(elapsed/60), s = elapsed%60; return m + ':' + (s<10?'0':'') + s; }
  function fmt(n){ return Math.round(n).toLocaleString(); }

  // Maps page: filters per map section and four by-clan charts of the smokes shown.
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
        html += '<div class="row' + (r.n < 5 ? ' dim' : '') + '"><span>' + r.team + '</span><span class="bar">' + bar + '</span><span>' + text + ' (n=' + r.n + ')</span></div>';
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
      function rows(f){ return teams.map(function(t){ var list = vis.filter(function(p){ return p.dataset.team === t; }); return {team:t, v:f(list), n:list.length, color:(window.TEAM_COLORS||{})[t]||'#94A3B8'}; }); }
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

  // Players leaderboard: click a heading to sort.
  document.querySelectorAll('table.sortable').forEach(function(t){
    var tbody = t.querySelector('tbody');
    t.querySelectorAll('th[data-key]').forEach(function(th){
      th.addEventListener('click', function(){
        var key = th.dataset.key, asc = th.dataset.asc === '1';
        var rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort(function(a,b){ var x = parseFloat(a.dataset[key]||0), y = parseFloat(b.dataset[key]||0); return asc ? x - y : y - x; });
        rows.forEach(function(r){ tbody.appendChild(r); });
        th.dataset.asc = asc ? '0' : '1';
      });
    });
  });

  if (!window.SMOKES) return;
  var rows = window.SMOKES, tbody = document.querySelector('#smokes tbody');
  function fill(id, key){ var sel = document.getElementById(id); var vals = Array.from(new Set(rows.map(function(r){return r[key];}))).filter(Boolean).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', render); }
  fill('f-team','team'); fill('f-player','player'); fill('f-ship','ship'); fill('f-map','map'); fill('f-game','game'); fill('f-type','type'); fill('f-phase','phase');
  document.getElementById('f-sort').addEventListener('change', render);
  function val(id){ return document.getElementById(id).value; }
  function bar(v, max, color){ var w = max ? Math.max(0, Math.min(1, v/max))*80 : 0; return '<span class="mini"><i style="width:'+w.toFixed(0)+'px;background:'+color+'"></i></span>'; }
  function render(){
    var f = {team:val('f-team'), player:val('f-player'), ship:val('f-ship'), map:val('f-map'), game:val('f-game'), type:val('f-type'), phase:val('f-phase')};
    var sort = val('f-sort'), asc = sort==='cap' || sort==='contested';
    var list = rows.filter(function(r){ return Object.keys(f).every(function(k){ return !f[k] || r[k]===f[k]; }); });
    list.sort(function(a,b){ var x=a[sort], y=b[sort]; if (x==null) x = asc? Infinity : -Infinity; if (y==null) y = asc? Infinity : -Infinity; return asc ? x-y : y-x; });
    tbody.innerHTML = list.map(function(r){
      var cap = r.cap==null ? '<span class="muted">inside a cap or none</span>' : (r.cap/1000).toFixed(1)+' km to '+r.cap_name;
      var con = r.contested==null ? '-' : (r.contested<0 ? Math.round(r.depth)+'% into '+r.contested_name : (r.contested/1000).toFixed(1)+' km to '+r.contested_name);
      var outcome = r.won ? 'near capture of '+r.won : (r.defended ? 'defended '+r.defended : '-');
      return '<tr><td>'+(r.thumb?'<a href="'+r.href+'"><img src="'+r.thumb+'" loading="lazy" alt=""></a>':'')+'</td>'+
        '<td><span class="tag" style="--c:'+r.color+'">'+r.team+'</span></td><td>'+r.player+'</td><td>'+r.ship+'</td><td>'+r.map+'</td>'+
        '<td class="small"><a href="'+r.game_href+'">'+r.game+'</a></td><td>'+r.clock+'<div class="small muted">'+(r.elapsed!=null?clockText(r.elapsed)+' elapsed':'')+'</div></td>'+
        '<td>'+r.total.toLocaleString()+' '+bar(r.total, window.MAX_TOTAL, '#F5C542')+'<div class="small muted">inside '+r.inside.toLocaleString()+' / outside '+r.behind.toLocaleString()+(r.fire?' / fire '+r.fire.toLocaleString():'')+'</div></td>'+
        '<td>'+cap+'</td><td>'+con+'</td><td>'+outcome+'</td><td>'+r.radar+(r.offensive?' <span class="muted small">own '+r.offensive+'</span>':'')+'</td><td><a href="'+r.href+'">smoke</a>'+(r.selfish?' <abbr class="term muted small" title="'+(window.SELFISH_DEF||'')+'">selfish</abbr>':'')+(r.overlap?' <span class="muted small">overlap</span>':'')+(r.flag?' <span class="warn small">flag</span>':'')+'</td></tr>';
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
    for title, s in site.awards["smokes"].items():
        print(f"award {title}: {s['player'] + ' ' + s['ship'] + ' id ' + str(s['smoke_id']) + ' match ' + s['_match'] if s else 'none'}")
    for title, (name, _) in site.awards["players"].items():
        print(f"award {title}: {name}")


if __name__ == "__main__":
    main()
