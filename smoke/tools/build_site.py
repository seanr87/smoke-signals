"""Build the Smoke Signals demo site from a batch output folder.

Usage:
  python -I build_site.py --batch output/<batch> --maps output/<maps>/maps
         [--clips <folder with <smoke_id>.mp4>] [--inventory smoke/inventory.csv]
         [--out site] [--colors "H-SR=#F5C542,RESIN=#5DADE2,PN=#B388FF"]

The site is static: plain HTML, CSS and a little JavaScript, no server.
Pages: Home, Clans, Players, Smokes, Maps, Games (awards.html and analysis.html are pointer pages).
"""
import argparse
import sys
import csv
import html
import json
import math
import os
import re
import shutil
from collections import Counter, defaultdict

MATCH_SECONDS = 20 * 60
MAP_DRAW_MAX = 25
# Minimum samples: a clan board or clan award needs this many games; a
# per-smoke average (Best in Haze) this many smokes; the leaderboard hides
# players under PLAYER_MIN_SMOKES by default.
CLAN_MIN_GAMES = 7
AVG_MIN_SMOKES = 10
SELFISH_MIN_SMOKES = 5
PLAYER_MIN_SMOKES = 5
FIXED_COLORS = {"H-SR": "#F5C542", "RESIN": "#5DADE2", "PN": "#B388FF"}
NATIVE = 768
# Thumbnails show half the map side, centred on the smoke.
THUMB_SIDE = NATIVE / 2
GRID_LETTERS = "ABCDEFGHIJ"
PHASES = [("opening", 0, 400), ("mid", 400, 800), ("endgame", 800, MATCH_SECONDS)]
SELFISH_DEF = "Selfish smoke: no teammate other than the owner was ever inside it, and no teammate fired through it from behind. A tendency, not a flaw: some ships (Gdansk, for one) smoke selfishly by design. How often a clan or player smokes selfishly is a style signal."
CONTEST_DEF = "A cap is contested for a team when it sits on the midline between the two spawns, lies on the enemy's side of the midline, or is held by the enemy."
REASON_TEXT = {"midline": "it sits on the midline between the spawns", "enemy_side": "it lies on the enemy's side of the midline", "enemy_owned": "the enemy held it"}
METRIC_DEFS = {
    "uptime": "Smoke uptime: seconds per game with at least one of the clan's smokes standing.",
    "first_smoke": "First smoke: seconds since battle start of the clan's first smoke in a game, averaged over the games with a smoke in the lens.",
    "charge": "Charge use: smoke charges used over charges carried by the clan's smoke ships.",
    "stacking": "Stacking rate: share of the clan's smokes that overlapped another smoke.",
    "contested": "Contested-cap share: share of smokes that stood within 1 km of a contested cap on average over their life.",
    "swing": "Score swing: change in the point gap (ours minus theirs) from activation to capture, averaged.",
    "deaths": "Smoke deaths: ships of the clan that a smoke concealed (inside it, or firing from behind it), were then detected, and sank while the smoke stood or within 20 s after its last puff faded.",
    "kills": "Kills from smoke: enemy ships whose last damage before sinking was a shell or fire tick credited to the smoke.",
    "punished": "Radar-punished share: share of smokes in which at least one of the clan's ships was radar-spotted while inside. Possibly a mistake: smokes are often laid knowing radar is a risk, and one spot is not a failure, but a high rate for a clan or player is a warning sign.",
    "concealed": "Concealed smoke damage: the part of the smoke damage fired while the shooter was undetected. Detected damage is the rest, broken down by how the shooter was spotted (radar, surface lit, hydro, proximity, aircraft, smoke fire penalty).",
    "dd": "DD damage: smoke damage, concealed and detected, dealt to enemy destroyers; same credit rules as smoke damage.",
    "offensive": "Radar spots from smoke: enemies spotted by the clan's own radar run from inside its smoke while concealed, inferred from the activation and radar range.",
    "won": "Smoke near a cap capture: a cap within stock gun range of a concealed ship flipped to the clan during the smoke or within 10 s after it.",
    "coverage": "Radar cap coverage: share of a contested cap's area within the range of a radar ship concealed in the smoke.",
}
AWARD_DEFS = {
    "Smoke of the Tournament": "Highest concealed smoke damage: main-gun shells fired from or through the smoke by the smoking team while the shooter was undetected, plus the fires they started.",
    "Deepest Cap Smoke": "Deepest into a contested cap as a share of the cap's radius, among smokes near a cap capture or a defended cap.",
    "Radar Bait": "Most radar spots on the smoking team's ships inside the smoke while it stood; ties broken by the damage those ships took while spotted.",
    "Peekaboo": "Most enemies spotted by the smoking team's own radar, run from inside the smoke while concealed.",
    "Most Selfish Smoke": "The selfish smoke with the most concealed damage by its owner.",
    "Golden Cloud": "Most total concealed smoke damage.",
    "The Smokefather": "Most smokes laid.",
    "Best in Haze": "Highest average concealed smoke damage per smoke, minimum 5 smokes.",
    "Most Selfish Smoker": "Most selfish smokes: a style signal, not a flaw.",
}
# Round 5 lenses: smoker class and smoke type, used by every filter.
CLASSES = ["destroyer", "cruiser", "battleship"]
SMOKE_TYPE_NAMES = ["standard", "cruiser", "exhaust", "crawling"]
CLASS_SHORT = {"destroyer": "DD", "cruiser": "CA", "battleship": "BB"}
PURPOSE_ORDER = ["cap_control", "cap_contest", "radar_trap", "hydro_trap", "counter_smoke", "island_dive", "reposition", "damage", "escape"]
PURPOSE_DEFS = {
    "cap_control": "Cap control: a radar ship concealed in the smoke activated its radar while covering at least 90% of a contested cap.",
    "cap_contest": "Cap contest: the smoke stood inside or within 1 km of a contested cap, without that radar coverage.",
    "radar_trap": "Radar trap: a concealed radar ship in the smoke caught an enemy with its radar, and the smoke is not cap control.",
    "hydro_trap": "Hydro trap: hydro run from inside the smoke spotted a nearby enemy.",
    "counter_smoke": "Counter smoke: laid within 12 km of an enemy smoke, within 45 s after it appeared.",
    "island_dive": "Island dive: a covered ship moved at least 2 km under the smoke and ended within 1 km of an island (a kind of reposition).",
    "reposition": "Reposition: a covered ship moved at least 3 km under the smoke without ever being detected.",
    "damage": "Damage: 20,000 or more smoke damage. The sub-label describes the damage: target_rich (2+ enemies), hunt (one enemy in the open), island_killer (one enemy parked by an island).",
    "escape": "Escape: laid while kiting and spotted, at 50% HP or less, or behind on points.",
}
MOVEMENT_DEFS = {
    "stationary": "Stationary: the smoker moved under 500 m while laying.",
    "pushing": "Pushing: the smoker closed on the nearest enemies while laying (within 60 degrees of the line to them).",
    "kiting": "Kiting: the smoker moved away from the nearest enemies while laying (more than 120 degrees off the line to them).",
    "horizontal": "Horizontal: laid roughly across the line to the nearest enemies.",
}
COVERAGE_DEFS = {
    "stacked": "Stacked: a destroyer laid it within 2.5 km of an allied cruiser or battleship.",
    "screen": "Screen: it hid teammates who sat inside it or fired from behind it.",
    "selfish": "Selfish: no teammate other than the owner was ever inside it, and no teammate fired through it from behind. A tendency, not a flaw.",
}
# Tags kept in the data but not shown on the site.
HIDDEN_PURPOSES = {"hydro_trap"}
# A run whose shell-plus-fire ledger exceeds the game's own result by more
# than this has unmerged duplicate hits (clock drift between the replays).
# Its game is flagged, kept on the site, and left out of awards and leaderboards.
LEDGER_RATIO_MAX = 1.25


def game_quality(spikes):
    """Data-quality note for a game from its runs' damage_spike records, or ''."""
    ratios = [sp.get("reconciliation_ratio_shell_fire") for sp in spikes if sp.get("reconciliation_ratio_shell_fire")]
    high = [r for r in ratios if r > LEDGER_RATIO_MAX]
    if not high:
        return ""
    return "ledger drift: the replay ledger is " + " and ".join(f"{r:.2f}" for r in sorted(ratios)) + " times the game's own shell and fire damage (unmerged duplicate hits between the two replays); smoke damage in this game is overstated"
AUTO_NOTE = "auto-tagged: rule-based from the replay; fuzzy tags carry a confidence"
# Clan metrics where a lower value is the better one (charts sort best first).
LOWER_IS_BETTER = {"deaths"}
DAMAGE_DEF = "Smoke damage: main-gun shells and air-support bombs fired from or through a smoke by the smoking team, plus the fires they started; each shot is credited to one smoke. Concealed damage is the part fired while the shooter was undetected; detected damage is the rest."
CONCEALED_DEF = METRIC_DEFS["concealed"]
DD_DEF = METRIC_DEFS["dd"]
RADAR_BAIT_DEF = "Radar bait: a smoke where enemy radar spotted our ships inside it. Possibly a mistake: smokes are often laid knowing radar is a risk, and one spot is not a failure, but a high rate of radar-punished smokes for a clan or player is a warning sign."
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


def jiff_date(batch):
    """Batch folder name 20261116-214739 as '16 Nov 2026'."""
    import datetime
    name = os.path.basename(os.path.normpath(batch))
    try:
        return datetime.datetime.strptime(name[:8], "%Y%m%d").strftime("%d %b %Y").lstrip("0")
    except ValueError:
        return name


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
    def __init__(self, batch, maps_dir, clips_dir, inventory, registry=None):
        self.batch = batch
        self.registry = {}
        if registry and os.path.exists(registry):
            for r in csv.DictReader(open(registry, encoding="utf-8")):
                self.registry[r["tag"]] = r
        self.smokes = json.load(open(os.path.join(batch, "smokes.json"), encoding="utf-8"))
        self.jobs = json.load(open(os.path.join(batch, "jobs.json"), encoding="utf-8"))
        self.job_by_key = {(j["match_id"], j["game_no"], j["team"]): j for j in self.jobs}
        self.games = {}
        self.games_by_team = {}
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
            # A replay sees its own team's consumable setup in full; the
            # opponent's can miss a charge, so a clan's roster comes from its own run.
            self.games_by_team[(key, j["team"])] = g
            spath = os.path.join(gdir, "damage_spike.json")
            if os.path.exists(spath):
                spike = json.load(open(spath, encoding="utf-8"))
                self.spikes[(j["team"], key)] = spike
                owner_team = {str(p["entity_id"]): t["name"] for t in g["teams"] for p in t["players"]}
                for ent, dmg in spike.get("damage_by_attacker_shell_fire", spike.get("damage_by_attacker", {})).items():
                    if owner_team.get(ent) == j["team"]:
                        self.damage_by_team_game[(j["team"], key)] += dmg
        self.game_quality = {}
        for (_, key), sp in self.spikes.items():
            if key not in self.game_quality:
                self.game_quality[key] = game_quality([s for (_, k), s in self.spikes.items() if k == key])
        # Games listed by hand (smoke/data-quality.csv next to the inventory) carry a
        # note on their page; a row with exclude=yes is flagged like the ratio rule.
        self.game_notes = {}
        listed = os.path.join(os.path.dirname(os.path.abspath(inventory)), "data-quality.csv") if inventory else ""
        if listed and os.path.exists(listed):
            for r in csv.DictReader(open(listed, encoding="utf-8")):
                key = (r["match_id"], int(r["game_no"]))
                if key not in self.games:
                    continue
                self.game_notes[key] = r["reason"]
                if (r.get("exclude") or "").strip().lower() in ("yes", "true", "1") and not self.game_quality.get(key):
                    self.game_quality[key] = r["reason"]
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
        self.profiles = {}
        profile_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps")
        if os.path.isdir(profile_dir):
            for f in os.listdir(profile_dir):
                if f.endswith(".yaml"):
                    prof = parse_yaml_subset(open(os.path.join(profile_dir, f), encoding="utf-8").read())
                    if prof.get("map"):
                        self.profiles[prof["map"]] = prof
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
            s["_airstrike"] = d.get("damage_airstrike") or 0.0
            s["_salvos"] = d.get("salvos") or 0
            s["_owner_damage"] = (d.get("damage_in_smoke_smoker") or 0) + (d.get("damage_behind_smoke_smoker") or 0)
            sp = s.get("damage_split") or {}
            s["_concealed"] = sp.get("concealed") or 0.0
            s["_detected"] = sp.get("detected") or 0.0
            s["_unknown"] = sp.get("unknown") or 0.0
            s["_detected_by"] = sp.get("detected_by") or []
            s["_dd"] = s.get("dd_damage") or 0.0
            owner_row = next((x for x in s.get("shooter_detail") or [] if x["player"] == s["player"]), None)
            s["_owner_concealed"] = ((owner_row or {}).get("split") or {}).get("concealed") or 0.0
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
            s["_kills"] = s.get("kills_from_smoke") or 0
            s["_deaths"] = len(s.get("smoke_deaths") or [])
            c = s.get("classification") or {}
            s["_c"] = c
            s["_class"] = c.get("smoker_class") or (s.get("ship_class") or "").lower() or "unknown"
            s["_type"] = s.get("smoke_type") or "unknown"
            mv = c.get("movement") or {}
            s["_movement"] = mv.get("label") or ""
            s["_movement_conf"] = mv.get("confidence") or ""
            s["_cover"] = (c.get("coverage") or {}).get("label") or ""
            s["_purposes"] = [p["tag"] for p in c.get("purposes") or [] if p["tag"] not in HIDDEN_PURPOSES]
            s["_primary"] = s["_purposes"][0] if s["_purposes"] else "none"
            s["_lane"] = c.get("lane") or ""
            s["_cap_role"] = c.get("cap_role") or ""
            s["_zone"] = ""
            m = self.maps.get(s["map"])
            prof = self.profiles.get(s["map"])
            if m and prof:
                sq = grid_square(m["space_size"], s["origin_xy"]["x"], s["origin_xy"]["z"])
                s["_grid"] = sq
                for zname, squares in (prof.get("zones") or {}).items():
                    if sq in squares:
                        s["_zone"] = zname
                        break
                for spot in (prof.get("notable_spots") or {}).values() if isinstance(prof.get("notable_spots"), dict) else []:
                    if isinstance(spot, dict) and sq in (spot.get("grid") or []):
                        s["_zone"] = f"{s['_zone']} ({spot.get('name')})" if s["_zone"] else str(spot.get("name"))
            s["_low_conf"] = [p["tag"] for p in c.get("purposes") or [] if p.get("confidence") == "low"] + (["movement"] if mv.get("confidence") == "low" else [])
            s["_short_game"] = f"vs {s.get('opponent') or '?'}, game {s['game_no']}"
            s["_quality"] = self.game_quality.get(s["_key"], "")
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
        # Every clan with a played game, most games first; nothing about clans is in code.
        self.teams = sorted(self.games_played, key=lambda t: (-self.games_played[t], t.upper()))
        self.smokes_by_team = Counter(s["team"] for s in self.smokes)
        for t in self.teams:
            if t not in self.registry:
                print(f"warning: clan {t} is not in the registry; palette colour used", file=sys.stderr)
        # The one-sided games: one replay, the other team's smokes inferred.
        self.one_sided_games = {}
        for s in self.smokes:
            if s.get("one_sided"):
                self.one_sided_games.setdefault(s["_key"], set()).add(s["team"])
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

    def clan_name(self, team):
        """Full name from the registry, else the tag."""
        return (self.registry.get(team) or {}).get("name") or team

    def clan_note(self, team):
        return (self.registry.get(team) or {}).get("note") or ""

    def clan_group(self, team):
        return (self.registry.get(team) or {}).get("group") or ""

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


def parse_yaml_subset(text):
    """The map profiles: two-level mappings, inline {a: b} mappings and [x, y] lists, comments."""
    root = {}
    stack = [(-1, root)]
    for raw in text.split("\n"):
        line = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        value = value.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            node = {}
            parent[key] = node
            stack.append((indent, node))
        elif value.startswith("{") and value.endswith("}"):
            node = {}
            for part in value[1:-1].split(","):
                k, _, v = part.strip().partition(":")
                node[k.strip()] = scalar(v.strip())
            parent[key] = node
        elif value.startswith("[") and value.endswith("]"):
            parent[key] = [scalar(x.strip()) for x in value[1:-1].split(",") if x.strip()]
        else:
            parent[key] = scalar(value)
    return root


def scalar(v):
    if v in ("true", "false"):
        return v == "true"
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v.strip("\"'")


def grid_square(space_size, x, z):
    """The game's grid: numbers 1 to 10 across the top, letters A to J down the side."""
    col = min(max(int((x + space_size / 2) / space_size * 10), 0), 9)
    row = min(max(int((space_size / 2 - z) / space_size * 10), 0), 9)
    return f"{GRID_LETTERS[row]}{col + 1}"


def grid_cell(square):
    """(column, row) indexes of a grid square such as D7."""
    return int(square[1:]) - 1, GRID_LETTERS.index(square[0].upper())


def grid_labels(step):
    return "".join(f'<text x="{(i + 0.5) * step:.0f}" y="14">{i + 1}</text><text x="6" y="{(i + 0.5) * step + 4:.0f}" text-anchor="start">{GRID_LETTERS[i]}</text>' for i in range(10))


def map_svg(href, alt, inner, extra_class=""):
    """The map image inside the overlay SVG, so both share one coordinate system."""
    return f'<svg viewBox="0 0 {NATIVE} {NATIVE}" class="mapsvg {extra_class}" role="img" aria-label="{esc(alt)}"><image href="{href}" width="{NATIVE}" height="{NATIVE}"/>{inner}</svg>'


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
    """Horizontal bars, one per row (label, value, colour, n[, href]). Negative values hang left of a zero line."""
    muted = muted or set()
    rows = [tuple(r) + (None,) * (5 - len(r)) for r in rows]
    vals = [v for _, v, _, _, _ in rows if v is not None]
    hi = max([0.0] + vals)
    lo = min([0.0] + vals)
    span = (hi - lo) or 1.0
    zero = (-lo) / span
    h = 22 * len(rows) + 4
    bar_x0 = label_w
    bar_w = width - label_w - 110
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" class="chart" style="max-width:{width}px" role="img" aria-label="{esc(title)}">']
    for i, (label, v, color, n, href) in enumerate(rows):
        y = 2 + i * 22
        row = [f'<text x="0" y="{y + 14}" class="lbl">{esc(label)}</text>']
        if v is not None:
            left = bar_x0 + (zero if v >= 0 else zero + v / span) * bar_w
            w = abs(v) / span * bar_w
            op = ' opacity="0.3"' if label in muted else ""
            row.append(f'<rect x="{left:.1f}" y="{y + 3}" width="{max(1.5, w):.1f}" height="14" rx="3" fill="{color}"{op}/>')
            text = fmt(v)
        else:
            text = "-"
        row.append(f'<text x="{width}" y="{y + 14}" class="val" text-anchor="end">{esc(text)}{" (n=" + str(n) + ")" if n is not None else ""}</text>')
        if href:
            out.append(f'<a href="{esc(href)}"><title>{esc(label)}: {esc(text)}</title>{"".join(row)}</a>')
        else:
            out.extend(row)
    if lo < 0:
        zx = bar_x0 + zero * bar_w
        out.append(f'<line x1="{zx:.1f}" y1="0" x2="{zx:.1f}" y2="{h}" class="zero"/>')
    out.append("</svg>")
    note = f'<p class="muted small">{note}</p>' if note else ""
    return f'<div class="panel"><h4>{title}</h4>{"".join(out)}{note}</div>'



def write_enriched_csv(data, path):
    """The batch's smokes.csv with the profile-derived zone and grid square appended."""
    by_id = {(s["_match"], s["game_no"], s["smoke_id"]): s for s in data.smokes}
    with open(os.path.join(data.batch, "smokes.csv"), encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames) + ["zone", "grid"]
        rows = []
        for r in reader:
            s = by_id.get((r["match_id"].split("_")[-1], int(r["game_no"]) if r["game_no"] else None, int(r["smoke_id"])))
            r["zone"] = s["_zone"] if s else ""
            r["grid"] = s.get("_grid", "") if s else ""
            rows.append(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return fields


def arrow_head(a, b, size, color):
    """A filled arrow head at `b`, pointing from `a` to `b`."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    if length <= 0:
        return ""
    ux, uy = dx / length, dy / length
    bx, by = b[0] - ux * size, b[1] - uy * size
    px, py = -uy * size * 0.5, ux * size * 0.5
    return f'<polygon points="{b[0]:.1f},{b[1]:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}" fill="{color}" stroke="#07131f" stroke-width="0.8"/>'


def mini_bar(value, max_value, color, width=90):
    frac = 0 if not max_value else max(0.0, min(1.0, value / max_value))
    return f'<span class="mini"><i style="width:{frac * width:.0f}px;background:{color}"></i></span>'


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


PALETTE = ["#F5C542", "#5DADE2", "#B388FF", "#6EE7B7", "#FB923C", "#F472B6", "#A3E635", "#94A3B8", "#F87171", "#22D3EE"]
ENEMY_COLOR = "#F87171"
UNCOUNTED_KIND_TEXT = {"torpedo": "torpedoes", "secondary": "secondaries", "flood": "flooding", "unknown": "unclassified hits"}


class Site:
    def __init__(self, data, out, colors, hub_layout="cards"):
        self.d = data
        self.out = out
        self.hub_layout = hub_layout
        self.colors = dict(FIXED_COLORS)
        palette = iter(PALETTE)
        for t in data.teams:
            reg = (data.registry.get(t) or {}).get("color")
            self.colors[t] = reg or self.colors.get(t) or next(palette, "#94A3B8")
        self.colors.update(colors)
        self.smoke_href = {}
        for s in data.smokes:
            s["_slug"] = f"{s['_match']}_g{s['game_no']}_{s['smoke_id']}"
            self.smoke_href[s["_slug"]] = f"smokes/{s['_slug']}.html"
        # Awards and leaderboards leave out games with a data-quality flag.
        clean = [s for s in data.smokes if not s["_quality"] and not s.get("one_sided")]
        clean_dd = [s for s in clean if self.lens_match(s, "destroyer")]
        self.flagged_games = sorted({s["_key"] for s in data.smokes if s["_quality"]})
        self.players = self.player_stats(clean)
        self.players_dd = self.player_stats(clean_dd)
        self.awards_by_lens = {"destroyer": self.compute_awards(clean_dd, self.players_dd), "all": self.compute_awards(clean, self.players)}
        self.awards = self.awards_by_lens["destroyer"]
        self.badges = defaultdict(list)
        for lens, awards in self.awards_by_lens.items():
            for title, (name, _) in awards["players"].items():
                if name and not any(b[0] == title for b in self.badges[name]):
                    self.badges[name].append((title, lens))
            for title, s in awards["smokes"].items():
                if s and not any(b[0] == title for b in self.badges[s["player"]]):
                    self.badges[s["player"]].append((title, lens))

    def color(self, team):
        return self.colors.get(team, "#94A3B8")

    @staticmethod
    def lens_match(s, cls="all", typ="all"):
        return (cls == "all" or s["_class"] == cls) and (typ == "all" or s["_type"] == typ)

    def lens_rows(self, cls="all", typ="all"):
        return [s for s in self.d.smokes if self.lens_match(s, cls, typ)]

    @staticmethod
    def lens_selects(prefix, with_labels=True):
        cls = "".join(f'<option value="{c}">{c}</option>' for c in CLASSES)
        typ = "".join(f'<option value="{x}">{x}</option>' for x in SMOKE_TYPE_NAMES)
        return (f'<label>Smoker class <select class="lens-class" id="{prefix}-class"><option value="all">all</option>{cls}</select></label>'
                f'<label>Smoke type <select class="lens-type" id="{prefix}-type"><option value="all">all</option>{typ}</select></label>')

    def nav(self, depth, active):
        base = "../" * depth
        items = [("Home", "index.html"), ("Clans", "clans.html"), ("Players", "players.html"), ("Smokes", "smokes.html"), ("Maps", "maps.html"), ("Games", "games.html"), ("About", "about.html")]
        links = "".join(f'<a href="{base}{h}" class="{"active" if n == active else ""}">{n}</a>' for n, h in items)
        return f'<nav class="top"><a class="hub" href="{base}../index.html" title="All analyses">Hub</a><span class="brand">Smoke Signals</span><input type="checkbox" id="navtoggle" class="navtoggle"><label for="navtoggle" class="navbtn" aria-label="Menu">Menu</label><div class="links">{links}</div></nav>'

    def page(self, title, body, depth=0, active="", extra_head=""):
        base = "../" * depth
        return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Smoke Signals</title><link rel="stylesheet" href="{base}style.css">{extra_head}</head>
<body>{self.nav(depth, active)}<main>{body}</main>
<footer>KotS XIX NA smoke analysis. Built from replays with Smoke Signals.</footer>
<script src="{base}site.js"></script></body></html>"""

    def write(self, rel, text):
        path = os.path.join(self.out, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def team_tag(self, team):
        if team not in self.colors:
            return f'<span class="tag other">{esc(team)}</span>'
        name = self.d.clan_name(team)
        title = f' title="{esc(name)}"' if name != team else ""
        return f'<span class="tag" style="--c:{self.color(team)}"{title}>{esc(team)}</span>'

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
        skip_images = os.environ.get("SMOKE_SITE_SKIP_IMAGES") == "1"
        os.makedirs(os.path.join(self.out, "img"), exist_ok=True)
        os.makedirs(os.path.join(self.out, "maps"), exist_ok=True)
        for m in d.maps.values():
            src = os.path.join(d.maps_dir, m["map"] + ".webp")
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(self.out, "maps", m["map"] + ".webp"))
        small_root = os.path.join(d.batch, "frames-small")
        for s in d.smokes:
            job = s["_job"]
            s["_img"] = {}
            s["_clip"] = None
            if not job:
                continue
            # The site ships the two capture frames, shrunk by `smoke_signals shrink-frames`
            # when that has run; the activation frames stay local.
            frames = os.path.join(small_root, job["name"])
            if not os.path.isdir(frames):
                frames = os.path.join(d.batch, "games", job["name"], "frames")
            for field in ["frame_cap", "frame_cap_zoom"]:
                name = s.get(field)
                if not name:
                    continue
                stem = name.rsplit(".", 1)[0]
                webp = stem + ".jpg" if os.path.exists(os.path.join(frames, stem + ".jpg")) else stem + ".webp"
                src = os.path.join(frames, webp)
                if os.path.exists(src):
                    rel = f"img/{job['name']}/{webp}"
                    dst = os.path.join(self.out, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    if not skip_images and (not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst)):
                        shutil.copyfile(src, dst)
                    s["_img"][field] = rel
            clip = d.clip_files.get(s["_slug"]) or d.clip_files.get(str(s["smoke_id"]))
            if clip:
                rel = f"clips/{s['_slug']}.mp4"
                dst = os.path.join(self.out, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(clip, dst)
                s["_clip"] = rel

    def thumb_crop(self, s):
        """Top left of the half-map crop centred on the smoke, in native map pixels."""
        d = self.d
        pts = [map_px(d, s["map"], p["x"], p["z"]) for p in (s.get("path") or [s["origin_xy"]])]
        pts = [p for p in pts if p]
        if not pts:
            return None
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        ox = min(max(cx - THUMB_SIDE / 2, 0.0), NATIVE - THUMB_SIDE)
        oy = min(max(cy - THUMB_SIDE / 2, 0.0), NATIVE - THUMB_SIDE)
        return ox, oy

    def thumb_svg(self, s):
        """Overlay for the map crop: caps, puffs in laying order with an arrow, nearby ships of both teams, credited fire lines with damage, a 1 km bar."""
        if "_thumb_svg" in s:
            return s["_thumb_svg"]
        crop = self.thumb_crop(s)
        d = self.d
        m = d.maps.get(s["map"])
        if not crop or not m:
            s["_thumb_svg"] = ""
            return ""
        ox, oy = crop
        g = d.games.get(s["_key"]) or {}
        k = NATIVE / m["space_size"]
        P = lambda x, z: map_px(d, s["map"], x, z)
        own = s["team"]
        color = self.color(own)
        f = "Segoe UI,sans-serif"
        out = []
        for c in g.get("caps") or []:
            x, y = P(c["position"]["x"], c["position"]["z"])
            r = c["radius"] * k
            if ox - r < x < ox + THUMB_SIDE + r and oy - r < y < oy + THUMB_SIDE + r:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#fff" fill-opacity="0.08" stroke="#fff" stroke-opacity="0.7" stroke-width="1.5" stroke-dasharray="5,4"/><text x="{x:.1f}" y="{y + 8:.1f}" fill="#fff" fill-opacity="0.85" font-size="22" font-weight="700" text-anchor="middle" font-family="{f}">{esc(c["cap"])}</text>')
        pr = (s.get("radius") or 15) * k
        pts = [P(p["x"], p["z"]) for p in thin(s.get("path") or [s["origin_xy"]], 40)]
        pts = [p for p in pts if p]
        for x, y in pts:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pr:.1f}" fill="#E2E8F0" fill-opacity="0.45" stroke="#F8FAFC" stroke-opacity="0.8" stroke-width="0.8"/>')
        if len(pts) >= 2:
            points = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            out.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>')
            out.append(arrow_head(pts[-2], pts[-1], 9, color))
        dd = s.get("damage_detail") or {}
        arrows = sorted((a for a in (dd.get("arrows") or []) if a.get("attacker_ally") and a.get("damage", 0) >= 1), key=lambda a: -a["damage"])[:6]
        labels = []
        for a in arrows:
            x1, y1 = P(a["from"]["x"], a["from"]["z"])
            x2, y2 = P(a["to"]["x"], a["to"]["z"])
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#07131f" stroke-width="4" opacity="0.6"/><line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="2"/>')
            out.append(arrow_head((x1, y1), (x2, y2), 8, color))
            labels.append(((x1 + x2) / 2, (y1 + y2) / 2, fmt_int(a["damage"])))
        for mark in s.get("ships_at_capture") or []:
            x, y = P(mark["position"]["x"], mark["position"]["z"])
            if not (ox <= x <= ox + THUMB_SIDE and oy <= y <= oy + THUMB_SIDE):
                continue
            ally = mark.get("team") == own
            fill = color if ally else ENEMY_COLOR
            ring = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="none" stroke="#F5C542" stroke-width="2"/>' if mark.get("is_owner") else ""
            out.append(f'{ring}<path d="M{x:.1f},{y - 7:.1f} L{x + 6:.1f},{y + 6:.1f} L{x:.1f},{y + 3:.1f} L{x - 6:.1f},{y + 6:.1f} Z" fill="{fill}" stroke="#07131f" stroke-width="1"/>')
        for mx, my, label in labels:
            w = len(label) * 7 + 8
            out.append(f'<rect x="{mx - w / 2:.1f}" y="{my - 8:.1f}" width="{w:.1f}" height="16" rx="3" fill="#07131f" fill-opacity="0.85"/><text x="{mx:.1f}" y="{my + 4:.1f}" fill="#F5C542" font-size="12" font-weight="600" text-anchor="middle" font-family="{f}">{label}</text>')
        km = 1000 / 30 * k
        out.append(f'<line x1="{ox + 10:.1f}" y1="{oy + THUMB_SIDE - 10:.1f}" x2="{ox + 10 + km:.1f}" y2="{oy + THUMB_SIDE - 10:.1f}" stroke="#fff" stroke-width="2"/><text x="{ox + 12 + km:.1f}" y="{oy + THUMB_SIDE - 6:.1f}" fill="#fff" font-size="11" font-family="{f}">1 km</text>')
        s["_thumb_inner"] = "".join(out)
        s["_thumb_svg"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ox:.1f} {oy:.1f} {THUMB_SIDE:.0f} {THUMB_SIDE:.0f}">{s["_thumb_inner"]}</svg>'
        return s["_thumb_svg"]

    def thumb_file(self, s):
        """A standalone SVG of the thumbnail: the map image under the overlay, for lazy loading in the Smokes table."""
        crop = self.thumb_crop(s)
        m = self.d.maps.get(s["map"])
        if not crop or not m:
            return None
        self.thumb_svg(s)
        ox, oy = crop
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{ox:.1f} {oy:.1f} {THUMB_SIDE:.0f} {THUMB_SIDE:.0f}">'
                f'<image href="../../maps/{m["map"]}.webp" x="0" y="0" width="{NATIVE}" height="{NATIVE}"/>{s["_thumb_inner"]}</svg>')

    def thumb(self, s, depth=0):
        """The map crop: the minimap as a background shifted to the crop, with the overlay on top."""
        crop = self.thumb_crop(s)
        m = self.d.maps.get(s["map"])
        if not crop or not m:
            return '<div class="noimg">no map</div>'
        ox, oy = crop
        px = ox / (NATIVE - THUMB_SIDE) * 100
        py = oy / (NATIVE - THUMB_SIDE) * 100
        return f'<div class="thumb" style="background-image:url({"../" * depth}maps/{m["map"]}.webp);background-position:{px:.2f}% {py:.2f}%">{self.thumb_svg(s)}</div>'

    def img(self, s, field, depth, cls="", lazy=True):
        rel = (s.get("_img") or {}).get(field)
        if not rel:
            return '<div class="noimg">no frame</div>'
        lazy_attr = ' loading="lazy"' if lazy else ""
        return f'<img class="{cls}" src="{"../" * depth}{rel}" alt="{esc(field)}"{lazy_attr}>'

    def smoke_card(self, s, depth=0, note=""):
        base = "../" * depth
        return f"""<a class="card smoke-card" href="{base}{self.smoke_href[s['_slug']]}" data-cls="{esc(s['_class'])}" data-type="{esc(s['_type'])}">{self.thumb(s, depth)}<div class="card-body">
<div>{self.team_tag(s['team'])} <b>{esc(s['player'])}</b> <span class="muted">{esc(s['ship'])}</span></div>
<div class="muted small">{esc(s['_games_label'])} | {esc(s['_act_clock'])}</div>
<div class="small">{fmt_int(s['_total'])} smoke damage{(' | ' + esc(note)) if note else ''}{' <span class="pill warn-pill" title="one replay for this game; this smoke is inferred and its damage is not counted">one-sided</span>' if s.get('one_sided') else ''}{' <span class="pill warn-pill" title="data-quality flag: left out of awards and leaderboards">drift</span>' if s['_quality'] else ''}</div><div class="small muted">{esc(CLASS_SHORT.get(s['_class'], '?'))} {esc(s['_movement'])} {esc(s['_cover'])}{(' | ' + esc(s['_primary'])) if s['_primary'] != 'none' else ''}</div></div></a>"""

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
        self.write("site.js", JS.replace("__PLAYER_MIN__", str(PLAYER_MIN_SMOKES)))
        self.write(".nojekyll", "")
        os.makedirs(os.path.join(self.out, "data"), exist_ok=True)
        write_enriched_csv(self.d, os.path.join(self.out, "data", "smokes.csv"))
        self.home()
        self.about()
        self.analysis_redirect()
        self.clans_index()
        for t in self.d.teams:
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

    def player_stats(self, rows):
        by_player = defaultdict(lambda: {"smokes": 0, "damage": 0.0, "concealed": 0.0, "dd": 0.0, "radar": 0, "ships": Counter(), "team": "", "selfish": 0, "games": set(), "won": 0, "offensive": 0, "maps": Counter(), "kills": 0, "deaths": 0})
        for s in rows:
            p = by_player[s["player"]]
            p["smokes"] += 1
            p["damage"] += s["_total"]
            p["concealed"] += s["_concealed"]
            p["dd"] += s["_dd"]
            p["radar"] += s["_radar"]
            p["ships"][s["ship"]] += 1
            p["team"] = s["team"]
            p["selfish"] += 1 if s.get("selfish_smoke") else 0
            p["games"].add(s["_key"])
            p["won"] += 1 if s["_won"] else 0
            p["offensive"] += s["_offensive"]
            p["kills"] += s["_kills"]
            p["deaths"] += s["_deaths"]
            p["maps"][s["map"]] += 1
        return by_player

    def compute_awards(self, rows, players):
        d = self.d
        best = max(rows, key=lambda s: (s["_concealed"], s["_total"])) if rows else None
        eligible = [s for s in rows if s["_depth"] is not None and (s["_won"] or s["_defended"])]
        deep = max(eligible, key=lambda s: (s["_depth"], s["_total"])) if eligible else None
        bait = max(rows, key=lambda s: (s["_radar"], s["_radar_dmg"], s["_total"])) if rows else None
        if bait and bait["_radar"] == 0:
            bait = None
        peek = max(rows, key=lambda s: (s["_offensive"], s["_total"])) if rows else None
        if peek and peek["_offensive"] == 0:
            peek = None
        selfish = [s for s in rows if s.get("selfish_smoke")]
        most_selfish = max(selfish, key=lambda s: (s["_owner_concealed"], s["_owner_damage"])) if selfish else None
        smokes = {"Smoke of the Tournament": best, "Deepest Cap Smoke": deep, "Radar Bait": bait, "Peekaboo": peek, "Most Selfish Smoke": most_selfish}

        def top_by(key, minimum=0):
            items = [(n, p) for n, p in players.items() if p["smokes"] >= minimum]
            return max(items, key=lambda kv: key(kv[1])) if items else (None, None)

        pawards = {
            "Golden Cloud": top_by(lambda p: p["concealed"]),
            "The Smokefather": top_by(lambda p: p["smokes"]),
            "Best in Haze": top_by(lambda p: p["concealed"] / p["smokes"], minimum=AVG_MIN_SMOKES),
            "Most Selfish Smoker": top_by(lambda p: p["selfish"], minimum=SELFISH_MIN_SMOKES),
        }
        clan_rows = {}
        for t in d.teams:
            rows_t = [s for s in rows if s["team"] == t]
            g = d.games_played.get(t) or 0
            if g >= CLAN_MIN_GAMES:
                clan_rows[t] = {"smokes": len(rows_t) / g, "damage": sum(s["_concealed"] for s in rows_t) / g, "selfish": sum(1 for s in rows_t if s.get("selfish_smoke")) / g, "games": g}
        cawards = {}
        for title, key in [("Most smokes laid", "smokes"), ("Most concealed smoke damage", "damage"), ("Most selfish smokes", "selfish")]:
            if clan_rows:
                w = max(clan_rows, key=lambda t: clan_rows[t][key])
                cawards[title] = (w, clan_rows[w][key], clan_rows[w]["games"])
        return {"smokes": smokes, "players": pawards, "clans": cawards}

    def award_note(self, title, s):
        if title == "Smoke of the Tournament":
            return f"{fmt_int(s['_concealed'])} concealed smoke damage ({fmt_int(s['_total'])} in all)"
        if title == "Deepest Cap Smoke":
            return f"{s['_depth']:.0f}% of the way into contested cap {s['contested_cap_name']} (cap radius {fmt_km(s.get('contested_cap_radius_m'))}); {cap_outcome_text(s)}"
        if title == "Radar Bait":
            return f"{s['_radar']} radar spots on the team's ships inside the smoke; {fmt_int(s['_radar_dmg'])} damage taken while spotted"
        if title == "Peekaboo":
            o = s.get("offensive_radar") or {}
            return f"{s['_offensive']} enemies spotted by {o.get('ship') or 'its radar ship'}'s radar from inside the smoke (inferred from the activation and radar range)"
        if title == "Most Selfish Smoke":
            return f"{fmt_int(s['_owner_concealed'])} concealed damage by the smoker ({fmt_int(s['_owner_damage'])} in all; no teammate benefited)"
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
<div class="big">{fmt_int(s['_total'])} smoke damage</div><div class="muted small">{fmt_int(s['_concealed'])} concealed, {fmt_int(s['_detected'])} detected</div><p><a href="{href}">Open the smoke page</a></p></div></div>{clip}</div>"""

    def home(self):
        d = self.d
        n_games = len(d.by_game)
        n_played = len(d.played_keys) or n_games
        maps = len({s["map"] for s in d.smokes})
        games_text = f"{n_played} games ({n_games} with at least one smoke)" if n_played != n_games else f"{n_games} games"
        strips = {lens: "".join(self.award_card(t, s) for t, s in awards["smokes"].items()) for lens, awards in self.awards_by_lens.items()}
        strip = f'<div class="lens-toggle"><button class="on" data-lens="destroyer">Destroyer smokes</button><button data-lens="all">All smokes</button></div><section class="cards awards lens-set" data-lens="destroyer">{strips["destroyer"]}</section><section class="cards awards lens-set" data-lens="all" hidden>{strips["all"]}</section>'
        per_team = d.smokes_by_team
        stats = f'<div class="stat"><b>{len(d.teams)}</b><span>clans</span></div>'
        chips = "".join(f'<a class="chip" href="{self.clan_href(t)}" style="--c:{self.color(t)}" title="{esc(self.d.clan_name(t))}: {per_team.get(t, 0)} smokes in {d.games_played.get(t, 0)} games">{esc(t)} <b>{per_team.get(t, 0)}</b></a>' for t in d.teams)
        terms = [("Smoke damage", DAMAGE_DEF.split(": ", 1)[1]), ("Concealed smoke damage", CONCEALED_DEF.split(": ", 1)[1]), ("DD damage", DD_DEF.split(": ", 1)[1]), ("Selfish smoke", SELFISH_DEF.split(": ", 1)[1]), ("Radar bait", RADAR_BAIT_DEF.split(": ", 1)[1])]
        key_terms = "".join(f'<li><b>{esc(k)}:</b> {esc(v)}</li>' for k, v in terms)
        body = f"""<section class="briefing"><h1>Smoke Signals</h1>
<p>This site breaks down how top competitive teams use smoke: {len(d.smokes)} smokes from {games_text} of King of the Sea XIX NA, played by {len(d.teams)} clans. Every number comes from the public replays; the <a href="about.html">About page</a> has the method and its limits.</p></section>
<section class="stats"><div class="stat"><b>{len(d.smokes)}</b><span>smokes analysed</span></div><div class="stat"><b>{n_played}</b><span>games on {maps} maps ({n_games} with at least one smoke)</span></div>{stats}</section>
<h2>Clans</h2><p class="muted small">Smokes analysed per clan; click a clan for its page.</p><div class="chips">{chips}</div>
<h2>Key terms</h2><ul class="terms">{key_terms}</ul>
<h2>The five award smokes</h2><p class="muted">{esc(CONTEST_DEF)}</p>{strip}"""
        self.write("index.html", self.page("Home", body, active="Home"))

    def about(self):
        d = self.d
        n_games = len(d.played_keys)
        drift = ", ".join(self.d.game_label(k) for k in self.flagged_games) or "none"
        one_sided = "; ".join(f"{self.d.game_label(k)} (one replay; {', '.join(sorted(teams))} smokes inferred, no damage counted)" for k, teams in sorted(d.one_sided_games.items())) or "none"
        terms = [("Smoke damage", DAMAGE_DEF.split(": ", 1)[1]), ("Concealed smoke damage", CONCEALED_DEF.split(": ", 1)[1]), ("DD damage", DD_DEF.split(": ", 1)[1]), ("Selfish smoke", SELFISH_DEF.split(": ", 1)[1]), ("Radar bait", RADAR_BAIT_DEF.split(": ", 1)[1]), ("Contested cap", CONTEST_DEF)]
        key_terms = "".join(f'<li><b>{esc(k)}:</b> {esc(v)}</li>' for k, v in terms)
        metric_terms = "".join(f'<li><b>{esc(k)}:</b> {esc(v.split(": ", 1)[1] if ": " in v else v)}</li>' for k, v in METRIC_DEFS.items())
        body = f"""<h1>About Smoke Signals</h1>
<section class="briefing"><p>Smoke Signals reads the public replays of King of the Sea XIX NA ({n_games} games, {len(d.teams)} clans, {len(d.smokes)} smokes) and measures what every smoke screen did: where and when it was laid, who it hid, what was fired from or through it, and what happened at the caps meanwhile. Both teams' replays are read and merged; a team's own replay gives its roster and consumables.</p></section>
<h2>Method in brief</h2>
<ul class="terms">
<li><b>Smokes:</b> every smoke-screen object the primary replay shows, matched to the ship that activated it (a flag marks the few whose owner is inferred from position alone).</li>
<li><b>Damage credit:</b> each damage event in the replay ledger is classified by weapon from its timing and the shots in flight (shell, secondary, fire, airstrike, torpedo, flood, unknown). Main-battery shells, air-support bombs and the fires they start count as smoke damage when the shot was fired from inside a smoke, or from outside by an undetected shooter whose line to an enemy in detection range crossed the smoke. Secondary, torpedo, flood and unknown damage never earn credit; when a ship fired such a weapon from a smoke (a torpedo is placed at its launch), the smoke's page lists those hits as not counted, so the enemies table and the smoke's total stay main battery, airstrikes and fires only.</li>
<li><b>Concealed vs detected:</b> by the shooter's visibility flags at the firing moment; the detected part is split by reason (radar, hydro, smoke fire penalty, aircraft, proximity, surface lit).</li>
<li><b>Lenses:</b> most boards default to destroyer smokes; "all" includes cruiser and battleship smokes. Tags (purpose, movement, coverage) are rule-based from the replay, with a confidence where the rule is fuzzy.</li>
<li><b>Minimum samples:</b> clan boards and clan awards need {CLAN_MIN_GAMES} games; Best in Haze needs {AVG_MIN_SMOKES} smokes; Most Selfish Smoker {SELFISH_MIN_SMOKES}; the leaderboard hides players under {PLAYER_MIN_SMOKES} smokes by default.</li>
<li><b>Awards:</b> award names are tongue-in-cheek; they describe a single smoke, not a player.</li>
</ul>
<h2>Data limits</h2>
<ul class="terms">
<li><b>Torpedo damage:</b> the replay ledger classifies about 77% of the torpedo damage the game's own results report. A replay only carries hits near its recorder, and hits that fall under the classifier's floor are counted as unknown, not as shells, so they never inflate smoke damage. Torpedo totals on this site are what the two replays saw.</li>
<li><b>Airstrikes:</b> about 44% of the Dutch ships' air-support bomb damage is classified as airstrike. The rest is counted as main-battery shells (when it lands with a salvo) or unknown; the share credited to smokes is small either way, since most strikes are called from outside smoke while spotted.</li>
<li><b>Ledger drift:</b> a game whose merged ledger exceeds the game's own totals by more than 25% is flagged on its page and left out of awards and leaderboards ({len(self.flagged_games)} games in this build{(": " + esc(drift)) if self.flagged_games else ""}). Three games whose two replays' clocks drift within the game (PN vs HTDOG, BTLST vs MZY, MANBA vs KM) sit at 1.10 to 1.16, inside the normal tail, and carry a note on their pages.</li>
<li><b>One-sided games:</b> {esc(one_sided)}.</li>
<li><b>Coverage:</b> smokes come from the primary replay only; a smoke neither recorder saw is not in the table. Charges, rosters and consumables come from a team's own replay.</li>
<li><b>Owner attribution:</b> {sum(1 for s in d.smokes if s.get("owner_flag"))} of {len(d.smokes)} smokes carry an owner flag (no activation within 5 s of the smoke's creation); their owner is the nearest ship with a smoke consumable.</li>
</ul>
<h2>Key terms</h2><ul class="terms">{key_terms}</ul>
<h2>Clan metrics</h2><ul class="terms">{metric_terms}</ul>
<p class="muted small">Source code and the full method document: the smoke-signals repository (smoke/DESIGN.md).</p>"""
        self.write("about.html", self.page("About", body, active="About"))

    def hub(self, root, mockups):
        """The landing page at the site root from the chosen mockup, with the real numbers; old root URLs redirect into smoke/."""
        d = self.d
        layout = {"cards": "hub-1-cards.html", "hero": "hub-2-hero.html", "tournament": "hub-3-tournament.html"}[self.hub_layout]
        html = open(os.path.join(mockups, layout), encoding="utf-8").read()
        css = open(os.path.join(mockups, "mock.css"), encoding="utf-8").read()
        best = self.awards["smokes"].get("Smoke of the Tournament")
        n_games = len(d.played_keys)
        n_maps = len({s["map"] for s in d.smokes})
        batch_date = jiff_date(d.batch)
        html = html.replace('href="mock.css"', 'href="hub.css"')
        html = html.replace("<title>Hub option 1: card grid</title>", "<title>KotS XIX NA analyses</title>").replace("<title>Hub option 2: featured hero and list</title>", "<title>KotS XIX NA analyses</title>").replace("<title>Hub option 3: by tournament</title>", "<title>KotS XIX NA analyses</title>")
        html = html.replace("1,547", f"{len(d.smokes):,}").replace("171", str(n_games)).replace("30 clans", f"{len(d.teams)} clans").replace("<b>30</b>", f"<b>{len(d.teams)}</b>").replace("16 Nov 2026", batch_date).replace("<b>8</b><span>maps</span>", f"<b>{n_maps}</b><span>maps</span>")
        if best:
            html = html.replace("97,327", fmt_int(best["_concealed"]))
            thumb = self.thumb(best, 0).replace("maps/", "smoke/maps/")
            import re
            html = re.sub(r'<div class="thumb">\s*<svg viewBox="0 0 300 180">.*?</svg>\s*</div>', f'<div class="thumb">{thumb}</div>', html, count=1, flags=re.S)
            html = re.sub(r'<div class="hero-art"><svg.*?</svg></div>', f'<div class="hero-art">{thumb}</div>', html, count=1, flags=re.S)
            html = re.sub(r'<div class="thumb small"><svg.*?</svg></div>', f'<div class="thumb small">{thumb}</div>', html, count=1, flags=re.S)
        top_clan = max(d.teams, key=lambda t: d.smokes_by_team.get(t, 0) / max(1, d.games_played.get(t, 1)))
        html = html.replace("<b>6.8</b>", f"<b>{d.smokes_by_team.get(top_clan, 0) / max(1, d.games_played.get(top_clan, 1)):.1f}</b>")
        html = html.replace("<b>341</b><span>replays</span>", f"<b>{sum(len(j) for j in [d.jobs])}</b><span>replays</span>")
        # Links: the Smoke Signals card and nav items.
        html = html.replace('<a class="card analysis live" href="#">', '<a class="card analysis live" href="smoke/index.html">')
        html = html.replace('<a class="button" href="#">Open Smoke Signals</a> <a class="button ghost" href="#">Award smokes</a>', '<a class="button" href="smoke/index.html">Open Smoke Signals</a> <a class="button ghost" href="smoke/index.html#awards">Award smokes</a>')
        html = html.replace('<a class="row-item" href="#">', '<a class="row-item" href="smoke/index.html">')
        html = html.replace('<a class="tile" href="#">', '<a class="tile" href="smoke/index.html">')
        html = html.replace('<a href="#">Smoke Signals</a>', '<a href="smoke/index.html">Smoke Signals</a>')
        html = html.replace('<a href="#">About</a>', '<a href="smoke/about.html">About</a>')
        html = html.replace('<a href="#">games.csv</a>', '<a href="smoke/data/games.csv">games.csv</a>')
        html = html.replace('<a class="active" href="#">Hub</a>', '<a class="active" href="index.html">Hub</a>').replace('<a class="active" href="#">KotS XIX NA</a>', '<a class="active" href="index.html">KotS XIX NA</a>')
        html = html.replace('Winner: see the Games page of any analysis.', f'Winner: {esc(self.tournament_winner() or "see the Games page")}.')
        html = html.replace("Built from the replays published on wows-tournaments.com.", "Built from the replays published for the tournament.")
        css += "\n" + ".thumb{position:relative;aspect-ratio:1;width:100%;max-width:420px;background-size:200% 200%;background-repeat:no-repeat;background-color:#0B1C2C;border-radius:6px;overflow:hidden}.thumb svg{position:absolute;inset:0;width:100%;height:100%;display:block}.card .thumb{max-width:none;aspect-ratio:5/3}.hero .thumb{aspect-ratio:1}.thumb.small{width:160px;aspect-ratio:1;flex:none}\n"
        with open(os.path.join(root, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        with open(os.path.join(root, "hub.css"), "w", encoding="utf-8", newline="\n") as f:
            f.write(css)
        with open(os.path.join(root, ".nojekyll"), "w") as f:
            f.write("")
        # Old URLs: the root pages redirect, and 404.html sends any other old path under smoke/.
        for page in ["clans.html", "players.html", "smokes.html", "maps.html", "games.html", "analysis.html", "awards.html", "about.html"]:
            stub = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=smoke/{page}"><title>Moved</title></head><body><p>Moved to <a href="smoke/{page}">smoke/{page}</a>.</p></body></html>'
            with open(os.path.join(root, page), "w", encoding="utf-8", newline="\n") as f:
                f.write(stub)
        not_found = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><script>
(function(){var p=location.pathname;var i=p.indexOf('/smoke/');if(i<0){var parts=p.split('/');var root=parts.slice(0,-1);var tail=parts[parts.length-1];
// Smoke Signals moved under smoke/: /x/clans.html -> /x/smoke/clans.html, /x/smokes/<id>.html -> /x/smoke/smokes/<id>.html
var m=p.match(/^(.*?)\\/(smokes|games|players|clans|img|clips|data|maps)\\/(.*)$/);if(m){location.replace(m[1]+'/smoke/'+m[2]+'/'+m[3]+location.search+location.hash);return;}
if(tail){location.replace(root.join('/')+'/smoke/'+tail+location.search+location.hash);return;}}
})();</script></head><body><p>This page moved. <a href="/">Open the hub</a>.</p></body></html>"""
        with open(os.path.join(root, "404.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(not_found)

    def tournament_winner(self):
        for r in self.d.inventory_rows:
            if r["stage"] == "Playoffs" and r["round"].startswith("GF") and r["status"] == "played":
                series = self.series().get(r["match_id"])
                if series and series.get("winner"):
                    return series["winner"]
        return None

    def clan_metrics(self, team, subset=None):
        """Every clan metric with its count, for the Clans charts and the clan page; `subset` narrows the smokes (a lens)."""
        d = self.d
        rows = [s for s in (subset if subset is not None else d.smokes) if s["team"] == team]
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
            g = d.games_by_team.get((key, team)) or d.games.get(key)
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
        wins = sum(1 for w in games.values() if w is True)
        losses = sum(1 for w in games.values() if w is False)
        firsts = []
        for key in games:
            starts = [s["_elapsed"] for s in rows if s["_key"] == key and s["_elapsed"] is not None]
            if starts:
                firsts.append(min(starts))
        return {
            "n": n, "games": n_games,
            "wins": wins, "losses": losses, "win_pct": 100.0 * wins / (wins + losses) if wins + losses else None,
            "smokes_per_game": (n / n_games, n),
            "first_smoke": (mean(firsts), len(firsts)),
            "damage_per_game": (sum(s["_total"] for s in rows) / n_games, n),
            "concealed_per_game": (sum(s["_concealed"] for s in rows) / n_games, n),
            "dd_per_game": (sum(s["_dd"] for s in rows) / n_games, n),
            "avg_damage": (mean([s["_total"] for s in rows]), n),
            "uptime": (uptime / n_games, n_games),
            "charge": (100.0 * used / charges if charges else None, charges),
            "stacking": (100.0 * sum(1 for s in rows if s.get("overlap_flag")) / n if n else None, n),
            "contested": (100.0 * sum(1 for s in rows if s.get("avg_contested_cap_dist_m") is not None and s["avg_contested_cap_dist_m"] <= 1000) / n if n else None, n),
            "selfish": (100.0 * sum(1 for s in rows if s.get("selfish_smoke")) / n if n else None, n),
            "swing": (mean([s["_score_swing"] for s in rows]), sum(1 for s in rows if s["_score_swing"] is not None)),
            "deaths": (sum(s["_deaths"] for s in rows) / n_games, n_games),
            "kills": (sum(s["_kills"] for s in rows) / n_games, n_games),
            "punished": (100.0 * sum(1 for s in rows if s["_radar"] > 0) / n if n else None, n),
            "offensive": (sum(s["_offensive"] for s in rows) / n_games, n_games),
            "won": (sum(1 for s in rows if s["_won"]), n),
            "coverage": (mean([s["_coverage"] for s in rows if s["_coverage"] is not None]), sum(1 for s in rows if s["_coverage"] is not None)),
            "coverage_full": (sum(1 for s in rows if s["_coverage_full"]), n),
        }

    def lens_metrics(self, clans):
        """Clan metrics for every lens: {"cls|type": {team: {metric: [value, n]}}}."""
        out = {}
        for cls in ["all"] + CLASSES:
            for typ in ["all"] + SMOKE_TYPE_NAMES:
                rows = self.lens_rows(cls, typ)
                out[f"{cls}|{typ}"] = {team: {k: list(v) if isinstance(v, tuple) else v for k, v in self.clan_metrics(team, rows).items()} for team in clans}
        return out

    @staticmethod
    def percentile_rank(value, others):
        """Percent of `others` below `value`, ties counted half; None without a value or a base."""
        others = [o for o in others if o is not None]
        if value is None or not others:
            return None
        below = sum(1 for o in others if o < value)
        equal = sum(1 for o in others if o == value)
        return 100.0 * (below + 0.5 * equal) / len(others)

    def percentiles(self, metrics):
        """Each clan's percentile per metric against the other clans with at least CLAN_MIN_GAMES games."""
        base = [t for t in metrics if metrics[t]["games"] >= CLAN_MIN_GAMES]
        out = {}
        for t in metrics:
            others = [o for o in base if o != t]
            out[t] = {key: self.percentile_rank(metrics[t][key][0], [metrics[o][key][0] for o in others]) for _, key, _, _, _ in self.CLAN_SPEC}
        return out

    def lens_percentiles(self, clans, lenses):
        """Percentiles for every lens: {"cls|type": {team: {metric: pct}}}, from lens_metrics' output."""
        return {lens: self.percentiles(lenses[lens]) for lens in lenses}

    TENDENCY = [
        ("smokes_per_game", "smokes per game", "prolific", "sparing"),
        ("first_smoke", "first smoke", "late", "early"),
        ("stacking", "stacked share", "stacker", "spread"),
        ("selfish", "selfish share", "selfish", "sharing"),
        ("contested", "cap-contest share", "cap-focused", "off-cap"),
        ("concealed_per_game", "concealed damage per game", "lethal", "quiet"),
        ("deaths", "smoke deaths per game", "exposed", "safe"),
        ("offensive", "radar spots per game", "radar-hunter", "radar-shy"),
    ]

    CLAN_SPEC = [
        ("Volume", "smokes_per_game", "Smokes per game", "f1", ""),
        ("Volume", "first_smoke", "First smoke (s elapsed, mean of each game's first)", "s", "first_smoke"),
        ("Volume", "uptime", "Smoke uptime (s per game)", "s", "uptime"),
        ("Volume", "charge", "Charge use", "pct", "charge"),
        ("Volume", "stacking", "Stacking rate", "pct", "stacking"),
        ("Damage", "damage_per_game", "Smoke damage per game", "int", ""),
        ("Damage", "concealed_per_game", "Concealed smoke damage per game", "int", "concealed"),
        ("Damage", "dd_per_game", "DD damage per game", "int", "dd"),
        ("Damage", "avg_damage", "Average damage per smoke", "int", ""),
        ("Damage", "kills", "Kills from smoke (per game)", "f2", "kills"),
        ("Objectives", "contested", "Contested-cap share", "pct", "contested"),
        ("Objectives", "won", "Smokes near a cap capture", "int", "won"),
        ("Objectives", "swing", "Score swing while smoke up", "pts", "swing"),
        ("Radar plays", "offensive", "Radar spots from smoke (per game)", "f2", "offensive"),
        ("Radar plays", "coverage", "Radar cap coverage (mean %)", "pct", "coverage"),
        ("Tendencies", "selfish", "Selfish smoke share", "pct", "selfish_def"),
        ("Tendencies", "punished", "Radar-punished share", "pct", "punished"),
        ("Risks", "deaths", "Smoke deaths (per game)", "f2", "deaths"),
    ]

    def clan_spec_json(self):
        spec = []
        for group, key, title, fmt, def_key in self.CLAN_SPEC:
            definition = SELFISH_DEF if def_key == "selfish_def" else METRIC_DEFS.get(def_key, "")
            spec.append({"group": group, "key": key, "title": title, "fmt": fmt, "def": definition, "lower": key in LOWER_IS_BETTER})
        return json.dumps(spec)

    def clan_chart(self, metrics, key, title, fmt=fmt_int, note=""):
        """One bar per clan, best first; lower is better for the risk metrics."""
        rows = [(t, metrics[t][key][0], self.color(t), metrics[t][key][1]) for t in metrics]
        known = [r for r in rows if r[1] is not None]
        unknown = [r for r in rows if r[1] is None]
        known.sort(key=lambda r: r[1], reverse=key not in LOWER_IS_BETTER)
        return bar_chart(title, known + unknown, fmt=fmt, note=note)

    def clans_index(self):
        d = self.d
        clans = [t for t in d.teams if any(s["team"] == t for s in d.smokes)]
        metrics = {t: self.clan_metrics(t) for t in clans}
        chips = []
        for t in clans:
            m = metrics[t]
            small = m["games"] < CLAN_MIN_GAMES
            chips.append(f'<a class="chip{" small-sample" if small else ""}" href="{self.clan_href(t)}" style="--c:{self.color(t)}" title="{esc(self.d.clan_name(t))}: {m["n"]} smokes in {m["games"]} games{"; small sample" if small else ""}">{esc(t)} <b>{m["n"]}</b><span class="muted small"> {m["games"]} g</span></a>')
        notes = [t for t in clans if d.clan_note(t)]
        cards = "".join(f'<a class="card toc" href="{self.clan_href(t)}" style="border-top:4px solid {self.color(t)}"><h2>{self.team_tag(t)} {esc(self.d.clan_name(t))}</h2><p>{esc(d.clan_note(t))}</p></a>' for t in notes)
        scouting = f'<h2>Scouting notes</h2><section class="cards">{cards}</section>' if cards else ""
        groups = []
        for group in ["Volume", "Damage", "Objectives", "Radar plays", "Tendencies", "Risks"]:
            panels = "".join(f'<div class="panel cchart" data-key="{key}"></div>' for g, key, _, _, _ in self.CLAN_SPEC if g == group)
            groups.append(f'<h2>{esc(group)}</h2><section class="charts">{panels}</section>')
        heads = "".join(f'<th data-key="{key}">{term(title, SELFISH_DEF if def_key == "selfish_def" else METRIC_DEFS.get(def_key, "")) if def_key else esc(title)}</th>' for g, key, title, fmt, def_key in self.CLAN_SPEC)
        games_of = {t: metrics[t]["games"] for t in clans}
        base = [t for t in clans if metrics[t]["games"] >= CLAN_MIN_GAMES]
        lenses = self.lens_metrics(clans)
        body = f"""<h1>Clans</h1><p class="muted">{len(clans)} clans. Smokes analysed and games played on each chip; click a clan for its page. Clans with fewer than {CLAN_MIN_GAMES} games are greyed: they stay in the table and the charts but cannot win a clan award.</p>
<div class="chips">{"".join(chips)}</div>{scouting}
<div class="filters lens"><span class="muted small">Lens</span>{self.lens_selects("clans")}<span class="count muted small" id="clans-count"></span></div>
<h2>Every clan, every metric</h2><p class="muted small">Click a heading to sort (by the value in both modes). The count behind each value is its n. Lower is better for smoke deaths. Percentiles rank a clan against the other clans with {CLAN_MIN_GAMES} or more games ({len(base)} clans in that base); clans under {CLAN_MIN_GAMES} games are ranked against the same base, greyed and marked. Cells are shaded by percentile, light to strong; a high percentile is not always good (smoke deaths, selfish share, radar-punished share).</p>
<div class="lens-toggle mode-toggle" id="clans-mode"><button data-mode="values" class="on">Values</button><button data-mode="pct">Percentiles</button></div>
<div class="scroll-x"><table class="games sortable clan-table" id="clan-table"><thead><tr><th>Clan</th><th data-key="games">Games</th><th data-key="wins">W-L</th><th data-key="win_pct">Win %</th><th data-key="n">Smokes</th>{heads}</tr></thead><tbody></tbody></table></div>
<h2>Charts</h2><div class="filters"><label class="check"><input type="checkbox" id="clans-all"> show all {len(clans)} clans (default: top 12 of each chart)</label></div>
<p class="muted small">One bar per clan, best first, with the count (n) on every bar. Lower is better for the risks; the tendencies are style signals, not scores. Destroyer smokes are the default lens; pick "all" to include every smoke.</p>
{"".join(groups)}
<script>window.CLAN_METRICS = {json.dumps(lenses)}; window.CLAN_PCT = {json.dumps(self.lens_percentiles(clans, lenses))}; window.CLAN_BASE = {len(base)}; window.CLAN_SPEC = {self.clan_spec_json()}; window.TEAM_COLORS = {json.dumps(self.colors)}; window.CLAN_TEAMS = {json.dumps(clans)}; window.CLAN_GAMES = {json.dumps(games_of)}; window.CLAN_MIN_GAMES = {CLAN_MIN_GAMES}; window.CLAN_HREF = {json.dumps({t: self.clan_href(t) for t in clans})};</script>"""
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
            rects = "".join(f'<rect x="{cx * NATIVE / 10:.0f}" y="{cy * NATIVE / 10:.0f}" width="{NATIVE / 10:.0f}" height="{NATIVE / 10:.0f}" fill="{self.color(team)}" fill-opacity="{0.15 + 0.7 * n / peak:.2f}"><title>{GRID_LETTERS[cy]}{cx + 1}: {n} smokes</title></rect>' for (cx, cy), n in cells.items())
            labels = grid_labels(NATIVE / 10)
            heat_svg = map_svg(f'{"../" * depth}maps/{m["map"]}.webp', d.map_title(map_name), f'{rects}<g class="gridlabels">{labels}</g>')
            out.append(f'<figure class="heat"><div class="mapwrap">{heat_svg}</div><figcaption>{esc(d.map_title(map_name))}: {len(smokes)} smokes (n = {len({s["_key"] for s in smokes})} games)</figcaption></figure>')
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
                + stat(term("concealed smoke damage per game", CONCEALED_DEF), "concealed_per_game") + stat(term("DD damage per game", DD_DEF), "dd_per_game")
                + stat(term("charge use", METRIC_DEFS["charge"]), "charge", fmt=pctf) + stat(term("stacking rate", METRIC_DEFS["stacking"]), "stacking", fmt=pctf)
                + stat(term("contested-cap share", METRIC_DEFS["contested"]), "contested", fmt=pctf) + stat(term("kills from smoke per game", METRIC_DEFS["kills"]), "kills", fmt=lambda v: f"{v:.2f}")
                + stat(term("smoke deaths per game", METRIC_DEFS["deaths"]), "deaths", fmt=lambda v: f"{v:.2f}")
                + stat(term("radar spots from smoke per game", METRIC_DEFS["offensive"]), "offensive", fmt=lambda v: f"{v:.2f}") + stat(term("smokes near a cap capture", METRIC_DEFS["won"]), "won")
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
        tag_counts = Counter(p for s in rows for p in s["_purposes"])
        tag_rows = "".join(f'<tr><td>{term(tag, PURPOSE_DEFS.get(tag, ""))}</td><td>{tag_counts.get(tag, 0)}</td><td>{100 * tag_counts.get(tag, 0) / n:.0f}%</td></tr>' for tag in PURPOSE_ORDER if tag not in HIDDEN_PURPOSES)
        mv_counts = Counter(s["_movement"] for s in rows if s["_movement"])
        cov_counts = Counter(s["_cover"] for s in rows if s["_cover"])
        mix = f'<div class="two-col"><div><h3>Purposes ({esc(AUTO_NOTE)}; every tag that applied, n = {n})</h3><table class="games small"><thead><tr><th>Tag</th><th>Smokes</th><th>Share</th></tr></thead><tbody>{tag_rows}</tbody></table></div><div><h3>Movement and coverage (n = {n})</h3>{bar_chart("Movement while laying", [(k, v, color, None) for k, v in mv_counts.most_common()])}{bar_chart("Coverage", [(k, v, color, None) for k, v in cov_counts.most_common()])}</div></div>'
        small = f' Fewer than {CLAN_MIN_GAMES} games: the per-game figures are a small sample and the clan cannot win a clan award.' if m["games"] < CLAN_MIN_GAMES else ""
        all_clans = [t for t in d.teams if any(s["team"] == t for s in d.smokes)]
        if not hasattr(self, "_all_pcts"):
            lenses = self.lens_metrics(all_clans)
            self._all_pcts = self.lens_percentiles(all_clans, lenses)
            self._all_clans_base = [t for t in all_clans if lenses["all|all"][t]["games"] >= CLAN_MIN_GAMES]
        all_pcts, all_clans_base = self._all_pcts, self._all_clans_base
        note = f'<div class="briefing"><p>{esc(d.clan_note(team))}</p></div>' if d.clan_note(team) else ""
        group = f" | {esc(d.clan_group(team))}" if d.clan_group(team) else ""
        body = f"""<h1>{self.team_tag(team)} {esc(self.d.clan_name(team))}</h1><p class="muted">{n} smokes in {m['games']} games{group}. Counts (n) on every number.{esc(small)}</p>{note}
<div class="filters lens"><span class="muted small">Tiles show</span>{self.lens_selects("clan")}</div>
<section class="stats lead" id="clan-lead">{lead}</section><section class="stats" id="clan-more">{more}</section>
<h2>Tendencies</h2><p class="muted small">Percentile among the clans with {CLAN_MIN_GAMES} or more games ({len(all_clans_base)} in the base{"; this clan is a small sample, ranked against that base" if m["games"] < CLAN_MIN_GAMES else ""}), for the lens chosen above. A word appears at the 80th percentile or above and the 20th or below. Shade is rank only: high is not always good.</p>
<div class="tendency" id="clan-tendency"></div>
<p class="muted small">The charts below cover every smoke by the clan.</p>
{mix}
<script>window.CLAN_METRICS = {json.dumps(self.lens_metrics([team]))}; window.CLAN_PCT = {json.dumps({lens: pcts[team] for lens, pcts in all_pcts.items()})}; window.CLAN_TENDENCY = {json.dumps(self.TENDENCY)}; window.CLAN_SPEC = {self.clan_spec_json()}; window.CLAN_TEAM = {json.dumps(team)}; window.TEAM_COLORS = {json.dumps(self.colors)};</script>
<div class="two-col"><div><h2>Where their games ended</h2>{ended_svg}</div><div><h2>Timing</h2>{timing}</div></div>
<h2>Most-smoked spots</h2>{self.heatmap(team)}
<div class="two-col"><div><h2>Ship lineup</h2>{lineup}<div class="scroll-x"><table class="games"><thead><tr><th>Ship</th><th>Class</th><th>Smoke</th><th>Stock gun range</th><th>Radar</th><th>Detection</th></tr></thead><tbody>{"".join(ship_rows)}</tbody></table></div></div>
<div><h2>Top smokers</h2><section class="cards">{strip}</section><h2>Clan awards</h2><section class="cards">{cawards}</section></div></div>"""
        self.write(f"clans/{slug(team)}.html", self.page(team, body, depth=1, active="Clans"))

    def players_page(self):
        rows = []
        for name, p in sorted(self.players.items(), key=lambda kv: -kv[1]["damage"]):
            badges = "".join(f'<span class="badge{" all" if lens == "all" else ""}" title="{esc(AWARD_DEFS.get(b, ""))} ({lens} smokes)">{esc(b)}</span>' for b, lens in self.badges.get(name, []))
            ships = ", ".join(f"{s} x{n}" if n > 1 else s for s, n in p["ships"].most_common())
            rows.append(f'<tr data-team="{esc(p["team"])}" data-damage="{p["damage"]:.0f}" data-concealed="{p["concealed"]:.0f}" data-dd="{p["dd"]:.0f}" data-smokes="{p["smokes"]}" data-avg="{p["damage"] / p["smokes"]:.0f}" data-selfish="{p["selfish"]}" data-radar="{p["radar"]}" data-won="{p["won"]}" data-offensive="{p["offensive"]}" data-kills="{p["kills"]}"><td>{self.team_tag(p["team"])}</td><td><a href="{self.player_href(name)}">{esc(name)}</a> {badges}</td><td class="small">{esc(ships)}</td><td>{p["smokes"]}</td><td>{fmt_int(p["damage"])}</td><td>{fmt_int(p["concealed"])}</td><td>{fmt_int(p["dd"])}</td><td>{fmt_int(p["damage"] / p["smokes"])}</td><td>{p["kills"]}</td><td>{p["selfish"]}</td><td>{p["radar"]}</td><td>{p["won"]}</td><td>{p["offensive"]}</td></tr>')
        def pcards(awards):
            return "".join(f'<div class="card award-p"><h3>{term(t, AWARD_DEFS.get(t, ""))}</h3><p>{self.team_tag(p["team"])} <a href="{self.player_href(name)}"><b>{esc(name)}</b></a></p><p class="note">{esc(self.player_award_note(t, p))}</p></div>' if name else f'<div class="card award-p"><h3>{esc(t)}</h3><p class="muted">Nothing here, just clear skies.</p></div>' for t, (name, p) in awards["players"].items())
        pawards = f'<div class="lens-toggle"><button class="on" data-lens="destroyer">Destroyer smokes</button><button data-lens="all">All smokes</button></div><section class="cards lens-set" data-lens="destroyer">{pcards(self.awards_by_lens["destroyer"])}</section><section class="cards lens-set" data-lens="all" hidden>{pcards(self.awards_by_lens["all"])}</section>'
        excluded = f" Smokes from {len(self.flagged_games)} game{'s' if len(self.flagged_games) != 1 else ''} with a data-quality flag and from the one-sided game are left out of the leaderboard and the awards." if self.flagged_games else ""
        clan_opts = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in self.d.teams if any(p["team"] == t for p in self.players.values()))
        body = f"""<h1>Players</h1><p class="muted">Click a column heading to sort. Badges are awards (gold for the destroyer lens, grey for all smokes); hover for the rule. No limit on awards per player. Best in Haze needs {AVG_MIN_SMOKES} smokes, Most Selfish Smoker {SELFISH_MIN_SMOKES}.{esc(excluded)}</p>
<h2>Player awards</h2>{pawards}
<h2>Leaderboard (n = {len(self.players)} players)</h2>
<div class="filters"><label>Clan <select id="p-clan"><option value="">all</option>{clan_opts}</select></label><label class="check"><input type="checkbox" id="p-min" checked> at least {PLAYER_MIN_SMOKES} smokes</label><span id="p-count" class="muted"></span></div>
<div class="scroll-x"><table class="games sortable" id="players"><thead><tr><th>Clan</th><th>Player</th><th>Ships</th><th data-key="smokes">Smokes</th><th data-key="damage">Smoke damage</th><th data-key="concealed">{term("Concealed", CONCEALED_DEF)}</th><th data-key="dd">{term("DD damage", DD_DEF)}</th><th data-key="avg">Per smoke</th><th data-key="kills">{term("Kills", METRIC_DEFS["kills"])}</th><th data-key="selfish">{term("Selfish")}</th><th data-key="radar">Radar spots</th><th data-key="won">{term("Near cap capture", METRIC_DEFS["won"])}</th><th data-key="offensive">{term("Own radar spots", METRIC_DEFS["offensive"])}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>"""
        self.write("players.html", self.page("Players", body, active="Players"))

    def player_award_note(self, title, p):
        if title == "Golden Cloud":
            return f"{fmt_int(p['concealed'])} concealed damage over {p['smokes']} smokes ({fmt_int(p['damage'])} in all)"
        if title == "The Smokefather":
            return f"{p['smokes']} smokes in {len(p['games'])} games"
        if title == "Best in Haze":
            return f"{fmt_int(p['concealed'] / p['smokes'])} concealed damage per smoke over {p['smokes']} smokes"
        return f"{p['selfish']} selfish smokes of {p['smokes']}"

    def player_page(self, name):
        p = self.players[name]
        rows = [s for s in self.d.smokes if s["player"] == name]
        badges = "".join(f'<span class="badge{" all" if lens == "all" else ""}" title="{esc(AWARD_DEFS.get(b, ""))} ({lens} smokes)">{esc(b)}</span>' for b, lens in self.badges.get(name, [])) or '<span class="muted small">no awards</span>'
        ship_order = [sh for sh, _ in p["ships"].most_common()]
        ship_color = {sh: PALETTE[i % len(PALETTE)] for i, sh in enumerate(ship_order)}
        ships = svg_donut(p["ships"].most_common(), PALETTE)
        kv = f"""<table class="kv"><tr><td>Smokes laid</td><td>{p['smokes']} in {len(p['games'])} games</td></tr><tr><td>Smoke damage</td><td>{fmt_int(p['damage'])}</td></tr><tr><td>{term('Concealed smoke damage', CONCEALED_DEF)}</td><td>{fmt_int(p['concealed'])}</td></tr><tr><td>{term('DD damage', DD_DEF)}</td><td>{fmt_int(p['dd'])}</td></tr><tr><td>Average per smoke</td><td>{fmt_int(p['damage'] / p['smokes'])}</td></tr>
<tr><td>{term('Kills from smoke', METRIC_DEFS['kills'])}</td><td>{p['kills']}</td></tr><tr><td>{term('Smoke deaths', METRIC_DEFS['deaths'])}</td><td>{p['deaths']}</td></tr>
<tr><td>{term('Selfish smokes')}</td><td>{p['selfish']}</td></tr><tr><td>Radar spots on the team inside</td><td>{p['radar']}</td></tr><tr><td>{term('Smokes near a cap capture', METRIC_DEFS['won'])}</td><td>{p['won']}</td></tr><tr><td>{term('Enemies spotted by own radar', METRIC_DEFS['offensive'])}</td><td>{p['offensive']}</td></tr></table>"""
        cards = "".join(self.smoke_card(s, depth=1, note=f"{phase_of(s['_elapsed']) or ''}") for s in sorted(rows, key=lambda s: -s["_total"]))
        chart_rows = [{"label": f"{self.d.map_title(s['map'])}, {s['_short_game']}, {s['ship']}", "v": round(s["_total"]), "color": ship_color.get(s["ship"], self.color(p["team"])), "href": f"../{self.smoke_href[s['_slug']]}", "cls": s["_class"], "type": s["_type"]} for s in sorted(rows, key=lambda s: -s["_total"])]
        timeline = '<div class="panel" id="player-chart"></div>'
        body = f"""<h1>{self.team_tag(p['team'])} {esc(name)}</h1><p>{badges}</p>
<div class="two-col"><div class="card"><h3>Stats <span class="muted small">(all smokes)</span></h3>{kv}</div><div class="card"><h3>Ships</h3>{ships}{timeline}</div></div>
<div class="filters lens"><span class="muted small">Show</span>{self.lens_selects("player")}<span class="muted small" id="player-count"></span></div>
<h2>Smokes</h2><section class="cards" id="player-cards">{cards}</section>
<script>window.PLAYER_SMOKES = {json.dumps(chart_rows)};</script>
<p><a href="../players.html">Back to the leaderboard</a> | <a href="{self.clan_href(p['team'], 1)}">the clan page</a></p>"""
        self.write(f"players/{slug(name)}.html", self.page(name, body, depth=1, active="Players"))

    def analysis_redirect(self):
        body = '<h1>Analysis</h1><p>The analysis moved: the clan comparison charts are on <a href="clans.html">Clans</a>.</p>'
        self.write("analysis.html", self.page("Analysis", body))

    def awards_redirect(self):
        body = '<h1>Awards</h1><p>The awards moved: smoke awards are on <a href="index.html">Home</a>, player awards on <a href="players.html">Players</a> and clan awards on each <a href="clans.html">clan page</a>.</p>'
        self.write("awards.html", self.page("Awards", body))

    def heat_rects(self, smokes, color=None):
        """10 x 10 density of smoke origins; by clan colour when one is given, else gold."""
        cells = Counter()
        for s in smokes:
            p = map_px(self.d, s["map"], s["origin_xy"]["x"], s["origin_xy"]["z"])
            if p:
                cells[(min(9, max(0, int(p[0] // (NATIVE / 10)))), min(9, max(0, int(p[1] // (NATIVE / 10)))))] += 1
        peak = max(cells.values()) if cells else 1
        return "".join(f'<rect x="{cx * NATIVE / 10:.0f}" y="{cy * NATIVE / 10:.0f}" width="{NATIVE / 10:.0f}" height="{NATIVE / 10:.0f}" fill="{color or "#F5C542"}" fill-opacity="{0.12 + 0.68 * n / peak:.2f}"><title>{GRID_LETTERS[cy]}{cx + 1}: {n} smokes</title></rect>' for (cx, cy), n in sorted(cells.items()))

    def map_figure(self, map_name, smokes, depth=0, size=768, anchor_prefix="smoke", fig_id="map", heat=False, lines=True):
        d = self.d
        m = d.maps.get(map_name)
        base = "../" * depth
        if not m:
            return '<p class="muted">Map image missing.</p>'
        step = NATIVE / 10
        grid = "".join(f'<line x1="{i * step:.0f}" y1="0" x2="{i * step:.0f}" y2="{NATIVE}"/><line x1="0" y1="{i * step:.0f}" x2="{NATIVE}" y2="{i * step:.0f}"/>' for i in range(1, 10))
        labels = grid_labels(step)
        caps = []
        for c in d.caps_by_map.get(map_name, []):
            px = map_px(d, map_name, c["position"]["x"], c["position"]["z"])
            r = c["radius"] * NATIVE / m["space_size"]
            caps.append(f'<circle cx="{px[0]:.1f}" cy="{px[1]:.1f}" r="{r:.1f}"/><text x="{px[0]:.1f}" y="{px[1] + 7:.1f}" class="caplabel">{esc(c["cap"])}</text>')
        markers = "".join(f'<marker id="{fig_id}-arrow-{slug(t)}" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="4" markerHeight="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 z" fill="{self.color(t)}"/></marker>' for t in sorted({s["team"] for s in smokes}))
        paths = []
        for s in smokes:
            pts = [map_px(d, map_name, p["x"], p["z"]) for p in thin(s.get("path") or [s["origin_xy"]])]
            pts = [p for p in pts if p]
            if not pts:
                continue
            if len(pts) == 1:
                pts = pts * 2
            dashed = ' stroke-dasharray="6,4"' if s.get("smoke_type") in ("exhaust", "crawling") else ""
            marker = f"{fig_id}-arrow-{slug(s['team'])}"
            points = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            elapsed = s["_elapsed"] if s["_elapsed"] is not None else -1
            contested = s.get("avg_contested_cap_dist_m")
            data = f'data-team="{esc(s["team"])}" data-spawn="{esc(s.get("spawn_side") or "")}" data-ship="{esc(s["ship"])}" data-cls="{esc(s["_class"])}" data-type="{esc(s["_type"])}" data-t="{elapsed}" data-dmg="{round(s["_total"])}" data-contested="{"" if contested is None else round(contested)}" data-selfish="{"1" if s.get("selfish_smoke") else ("0" if s.get("selfish_smoke") is not None else "")}"'
            title = f'{s["player"]} {s["ship"]} at {s["_act_clock"]} ({elapsed_text(elapsed) if elapsed >= 0 else "?"} elapsed), {fmt_int(s["_total"])} dmg, {s.get("smoke_type") or ""} smoke'
            paths.append(f'<a href="{base}{self.smoke_href[s["_slug"]]}" id="{anchor_prefix}-{s["_slug"]}" class="smokepath" {data}><polyline points="{points}" stroke="{self.color(s["team"])}"{dashed} marker-end="url(#{marker})"><title>{esc(title)}</title></polyline></a>')
        zones = self.zone_overlay(map_name)
        heat_g = f'<g class="heat">{self.heat_rects(smokes) if heat else ""}</g>'
        inner = f'<defs>{markers}</defs>{heat_g}<g class="grid">{grid}</g><g class="gridlabels">{labels}</g>{zones}<g class="caps">{"".join(caps)}</g><g class="paths">{"".join(paths) if lines else ""}</g>'
        figure = map_svg(f'{base}maps/{m["map"]}.webp', self.d.map_title(map_name), inner)
        return f'<div class="mapwrap{" lines" if lines else ""}" style="max-width:{size}px">{figure}</div>'

    ZONE_COLORS = {"west": "#5DADE2", "east": "#F5C542", "north": "#5DADE2", "south": "#F5C542", "center": "#B388FF"}

    def zone_overlay(self, map_name):
        """Zone squares and labels from the map profile, hidden until toggled."""
        prof = self.d.profiles.get(map_name)
        if not prof or not prof.get("zones"):
            return ""
        step = NATIVE / 10
        out = []
        for zname, squares in prof["zones"].items():
            color = self.ZONE_COLORS.get(zname, "#6EE7B7")
            xs, ys = [], []
            for sq in squares:
                col, row = grid_cell(sq)
                xs.append((col + 0.5) * step)
                ys.append((row + 0.5) * step)
                out.append(f'<rect x="{col * step:.0f}" y="{row * step:.0f}" width="{step:.0f}" height="{step:.0f}" fill="{color}" fill-opacity="0.16"/>')
            if xs:
                out.append(f'<text x="{sum(xs) / len(xs):.0f}" y="{sum(ys) / len(ys):.0f}" fill="{color}" font-size="22" font-weight="700" text-anchor="middle" opacity="0.9">{esc(zname)}</text>')
        spots = prof.get("notable_spots")
        if isinstance(spots, dict):
            for spot in spots.values():
                if isinstance(spot, dict) and spot.get("grid"):
                    xs, ys = [], []
                    for sq in spot["grid"]:
                        col, row = grid_cell(sq)
                        xs.append((col + 0.5) * step)
                        ys.append((row + 0.5) * step)
                        out.append(f'<rect x="{col * step:.0f}" y="{row * step:.0f}" width="{step:.0f}" height="{step:.0f}" fill="none" stroke="#fff" stroke-dasharray="4,3"/>')
                    out.append(f'<text x="{sum(xs) / len(xs):.0f}" y="{sum(ys) / len(ys) + 4:.0f}" fill="#fff" font-size="14" text-anchor="middle">{esc(str(spot.get("name")))}</text>')
        return f'<g class="zones">{"".join(out)}</g>'

    def maps_page(self):
        d = self.d
        sections = []
        by_map = defaultdict(list)
        for s in d.smokes:
            by_map[s["map"]].append(s)
        map_order = sorted(by_map.items(), key=lambda kv: -len(kv[1]))
        for n, (map_name, smokes) in enumerate(map_order):
            games = len({s["_key"] for s in smokes})
            fig = self.map_figure(map_name, smokes, fig_id=f"m{n}", heat=False, lines=False)
            self.write_map_paths(map_name, smokes, f"m{n}")
            sections.append(f'<section class="map-section" data-map="{esc(map_name)}" data-paths="data/maps/m{n}.json" data-total="{len(smokes)}"><h2>{esc(self.d.map_title(map_name))} <span class="muted small">{len(smokes)} smokes in {games} games</span> <span class="count muted small"></span></h2><div class="two-col mapcol">{fig}<div><h3>By clan, for the smokes shown</h3><p class="muted small">With every clan shown: the top 10 by smokes on this map, the rest as "others". Clans with fewer than 5 smokes shown are greyed out.</p><div class="chart"></div><h3>Ships that smoked here</h3><div class="ships"></div></div></div></section>')
        clan_counts = Counter(s["team"] for s in d.smokes)
        ship_counts = Counter(s["ship"] for s in d.smokes)
        ship_colors = {sh: PALETTE[i % len(PALETTE)] for i, (sh, _) in enumerate(ship_counts.most_common())}
        slug_index = {s["_slug"]: [s["map"], s["team"]] for s in d.smokes}
        map_opts = "".join(f'<option value="{esc(m)}">{esc(self.d.map_title(m))} ({len(ss)})</option>' for m, ss in map_order)
        players = "".join(f'<option value="{esc(pl)}">{esc(pl)}</option>' for pl in sorted({s["player"] for s in d.smokes}))
        purposes = "".join(f'<option value="{esc(p)}">{esc(p)}</option>' for p, _ in Counter(p for s in d.smokes for p in s["_purposes"]).most_common())
        spawns = "".join(f'<option value="{v}">{v}</option>' for v in ("north", "south", "east", "west") if any(s.get("spawn_side") == v for s in d.smokes))
        classes = "".join(f'<option value="{c}">{c}</option>' for c in CLASSES if any(s["_class"] == c for s in d.smokes))
        types = "".join(f'<option value="{x}">{x}</option>' for x in SMOKE_TYPE_NAMES if any(s["_type"] == x for s in d.smokes))
        filters = f"""<div class="filters mapfilters sticky" id="maps-filters">
<label>Map <select id="m-map"><option value="">all maps</option>{map_opts}</select></label>
<label>Clans <span class="multi" id="m-clan"></span></label>
<label>Ships <span class="multi" id="m-ship"></span></label>
<label>Player <select id="m-player"><option value="">all</option>{players}</select></label>
<label>Purpose (any tag) <select id="m-purpose"><option value="">any</option>{purposes}</select></label>
<label>Spawn <select id="m-spawn"><option value="">all</option>{spawns}</select></label>
<label>Smoker class <select id="m-cls"><option value="">all</option>{classes}</select></label>
<label>Smoke type <select id="m-type"><option value="">all</option>{types}</select></label>
<label class="range">Time elapsed <span class="rangevals"><b class="lo">0:00</b> to <b class="hi">20:00</b></span><span class="dual"><input type="range" id="m-lo" min="0" max="20" value="0" step="1"><input type="range" id="m-hi" min="0" max="20" value="20" step="1"></span><span class="muted small">minutes since battle start, 1-minute steps</span></label>
<label>View <span class="seg"><label><input type="radio" name="m-view" value="auto" checked> auto</label><label><input type="radio" name="m-view" value="heat"> heat map</label><label><input type="radio" name="m-view" value="smokes"> smokes</label></span></label>
<span id="m-count" class="count muted"></span> <a id="m-clear" class="small clear" href="maps.html">clear filters</a></div>"""
        body = f"""<h1>Maps</h1><p class="muted">Each map shows a density of smoke origins (gold squares, darker where more smokes started) for the smokes the filters leave; when {MAP_DRAW_MAX} or fewer remain, the smokes themselves are drawn: the cloud, the path while laying, and an arrow at the end, in the clan's colour. Click a drawn smoke to open its page. The View switch forces either picture. Filters apply to every map and are kept in the address bar, so a view can be shared.</p><div class="legend-row"><label class="legend"><input type="checkbox" id="showzones"> show zones (draft map profiles)</label></div>{filters}{''.join(sections)}
<script>window.TEAM_COLORS = {json.dumps(self.colors)}; window.SHIP_COLORS = {json.dumps(ship_colors)}; window.SELFISH_DEF = {json.dumps(SELFISH_DEF)}; window.CONTEST_DEF = {json.dumps(CONTEST_DEF)}; window.SMOKE_MAP = {json.dumps(slug_index)}; window.MAP_DRAW_MAX = {MAP_DRAW_MAX}; window.MAPS_OPTS = {json.dumps({"clans": [[t, clan_counts[t]] for t in d.teams if clan_counts.get(t)], "ships": [[sh, n] for sh, n in sorted(ship_counts.items())]})};</script>"""
        self.write("maps.html", self.page("Maps", body, active="Maps"))

    def write_map_paths(self, map_name, smokes, fig_id):
        """One JSON per map with every smoke's path in map pixels, loaded by the maps page for the density and the drawn smokes."""
        d = self.d
        m = d.maps.get(map_name)
        rows = []
        for s in smokes:
            pts = [map_px(d, map_name, p["x"], p["z"]) for p in thin(s.get("path") or [s["origin_xy"]])]
            pts = [p for p in pts if p]
            if not pts:
                continue
            if len(pts) == 1:
                pts = pts * 2
            elapsed = s["_elapsed"] if s["_elapsed"] is not None else -1
            contested = s.get("avg_contested_cap_dist_m")
            radius_px = (s.get("radius") or 0) * NATIVE / m["space_size"] if m else 0
            rows.append({
                "slug": s["_slug"], "href": self.smoke_href[s["_slug"]], "team": s["team"], "player": s["player"], "spawn": s.get("spawn_side") or "", "ship": s["ship"],
                "cls": s["_class"], "type": s["_type"], "t": elapsed, "dmg": round(s["_total"]), "contested": None if contested is None else round(contested),
                "selfish": (1 if s.get("selfish_smoke") else 0) if s.get("selfish_smoke") is not None else None,
                "purposes": s["_purposes"],
                "dashed": s.get("smoke_type") in ("exhaust", "crawling"),
                "r": round(radius_px, 1),
                "pts": [[round(x, 1), round(y, 1)] for x, y in pts],
                "title": f'{s["player"]} {s["ship"]} at {s["_act_clock"]} ({elapsed_text(elapsed) if elapsed >= 0 else "?"} elapsed), {fmt_int(s["_total"])} dmg, {s.get("smoke_type") or ""} smoke',
            })
        self.write(f"data/maps/{fig_id}.json", json.dumps(rows, separators=(",", ":")))

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
        standings = defaultdict(lambda: defaultdict(lambda: {"w": 0, "l": 0, "g": 0, "f": 0}))
        for r in sorted(d.inventory_rows, key=lambda r: (r["group"], int(r["round"].split()[-1]) if r["round"].split()[-1].isdigit() else 0, int(r["game_no"]))):
            if r["stage"] != "Groups":
                continue
            teams = [t.strip() for t in r["teams"].split(" vs ")]
            if r["status"] in ("played", "forfeit") and r["winner"]:
                for t in teams:
                    if t in d.teams:
                        row = standings[r["group"]][t]
                        row["g"] += 1
                        if t == r["winner"]:
                            row["w"] += 1
                        else:
                            row["l"] += 1
                        if r["status"] == "forfeit":
                            row["f"] += 1
            if r["status"] == "bye":
                continue
            key = (r["match_id"], int(r["game_no"]))
            group_rows.append(self.game_row(r, key, with_round=True))
        tables = []
        for group in sorted(standings):
            rows_g = sorted(standings[group].items(), key=lambda kv: (-kv[1]["w"], kv[1]["l"], kv[0]))
            trs = "".join(f'<tr><td>{self.team_tag(t)} {esc(self.d.clan_name(t)) if self.d.clan_name(t) != t else ""}</td><td>{v["w"]}</td><td>{v["l"]}</td><td>{v["g"]}{(" (" + str(v["f"]) + " by forfeit)") if v["f"] else ""}</td><td>{self.d.smokes_by_team.get(t, 0)}</td></tr>' for t, v in rows_g)
            tables.append(f'<div class="card"><h3>{esc(group)}</h3><table class="games small"><thead><tr><th>Clan</th><th>W</th><th>L</th><th>Games</th><th>Smokes analysed</th></tr></thead><tbody>{trs}</tbody></table></div>')
        maps = sorted({r["map"] for r in d.inventory_rows if r["stage"] == "Groups" and r["status"] != "bye"})
        map_opts = "".join(f'<option value="{esc(m)}">{esc(m)}</option>' for m in maps)
        clan_opts = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in d.teams)
        n_played = len(d.played_keys)
        body = f"""<h1>Games</h1><p class="muted">{n_played} played games with replays, {len(d.by_game)} of them with at least one smoke. The smokes column counts the smokes analysed for each team, in team order. Games with a data-quality flag are marked and left out of awards and leaderboards.</p>
<h2>Playoffs</h2><p class="muted">Double elimination. Each box is a series; the numbers are games won. Click a series for its games.</p>
{bracket}
<h2>Group stage</h2><section class="cards groups-4">{"".join(tables)}</section>
<div class="filters"><label>Clan <select id="g-clan"><option value="">all</option>{clan_opts}</select></label><label>Map <select id="g-map"><option value="">all</option>{map_opts}</select></label><span id="g-count" class="muted"></span></div>
<div class="scroll-x"><table class="games" id="games"><thead><tr><th>Round</th><th>Date</th><th>Teams</th><th>Map</th><th>Score</th><th>Winner</th><th>Smokes analysed</th><th></th></tr></thead><tbody>{"".join(group_rows)}</tbody></table></div>
<p id="g-empty" class="muted" hidden>Nothing here, just clear skies.</p>"""
        self.write("games.html", self.page("Games", body, active="Games"))
        for s in series.values():
            self.series_page(s)

    def smokes_column(self, key, teams, depth=0):
        """'7 + 4' with the tag chips, in team order; a dash for a team with no smokes analysed."""
        counts = Counter(s["team"] for s in self.d.by_game.get(key, []))
        if not sum(counts.values()):
            return '<span class="muted">-</span>'
        parts = [f'{self.team_tag(t)} {counts.get(t, 0)}' for t in teams]
        notes = ""
        if key in self.d.one_sided_games:
            notes += f' <span class="pill warn-pill" title="one replay: {", ".join(sorted(self.d.one_sided_games[key]))} smokes inferred, no damage counted">one-sided</span>'
        if self.d.game_quality.get(key):
            notes += f' <span class="pill warn-pill" title="{esc(self.d.game_quality[key])}">drift</span>'
        return " + ".join(parts) + notes

    def game_row(self, r, key, depth=0, with_round=False):
        href = self.game_href(key, depth)
        teams = [t.strip() for t in r["teams"].split(" vs ")]
        tags = " vs ".join(self.team_tag(t) if t in self.colors else esc(t) for t in teams)
        link = f'<a href="{href}">game page</a>' if href else ('<span class="muted">no smokes</span>' if r["status"] == "played" else f'<span class="muted">{esc(r["status"])}</span>')
        winner = self.team_tag(r["winner"]) if r["winner"] in self.colors else esc(r["winner"] or "-")
        clans = ";".join(t for t in teams if t in self.colors)
        first = f'<td>{esc(r["group"])} {esc(r["round"])}</td>' if with_round else f'<td>Game {esc(r["game_no"])}</td>'
        date = f'<td>{esc(r["date"])}</td>' if with_round else ""
        return f'<tr data-clan="{esc(clans)}" data-map="{esc(r["map"])}">{first}{date}<td>{tags}</td><td>{esc(r["map"])}</td><td>{esc(r["score"] or "-")}</td><td>{winner}</td><td>{self.smokes_column(key, teams, depth)}</td><td>{link}</td></tr>'

    def series_page(self, s):
        d = self.d
        rows = [self.game_row(r, (r["match_id"], int(r["game_no"])), depth=1) for r in s["games"]]
        result = f"{esc(s['winner'])} won {max(s['wins'])}-{min(s['wins'])}" if s["winner"] else "no result"
        title = f"{' vs '.join(s['teams'])}, {ROUND_TITLES.get(s['round'], s['round'])}"
        body = f"""<h1>{esc(title)}</h1><p class="muted">{esc(s['bracket'])} | {esc(s['date'])} | {result}</p>
{self.series_box(s, depth=1)}
<div class="scroll-x"><table class="games"><thead><tr><th>Game</th><th>Teams</th><th>Map</th><th>Score</th><th>Winner</th><th>Smokes analysed</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p><a href="../games.html">Back to the bracket</a></p>"""
        self.write(f"games/series_{s['match_id']}.html", self.page(title, body, depth=1, active="Games"))

    def all_smokes(self):
        d = self.d
        records = []
        for s in d.smokes:
            records.append({
                "id": s["smoke_id"], "team": s["team"], "player": s["player"], "ship": s["ship"], "map": self.d.map_title(s["map"]),
                "game": s["_games_label"], "game_short": s["_short_game"], "type": s.get("smoke_type") or "",
                "elapsed": s["_elapsed"], "phase": s["_phase"] or "", "total": round(s["_total"]), "concealed": round(s["_concealed"]), "detected": round(s["_detected"]), "dd": round(s["_dd"]), "inside": round(s["_in"]), "behind": round(s["_behind"]), "fire": round(s["_fire"]),
                "radar": s["_radar"], "offensive": s["_offensive"], "kills": s["_kills"], "deaths": s["_deaths"],
                "swing": s["_score_swing"],
                "contested": s.get("avg_contested_cap_dist_m"), "contested_name": s.get("contested_cap_name") or "", "depth": s["_depth"],
                "won": s.get("cap_won") or "", "defended": s.get("cap_defended") or "",
                "selfish": bool(s.get("selfish_smoke")), "thumb": f"data/thumbs/{s['_slug']}.svg" if self.thumb_file(s) else "", "href": self.smoke_href[s["_slug"]],
                "one_sided": bool(s.get("one_sided")), "quality": s["_quality"],
                "color": self.color(s["team"]),
                "cls": s["_class"], "cls_short": CLASS_SHORT.get(s["_class"], "?"), "movement": s["_movement"], "movement_conf": s["_movement_conf"], "coverage": s["_cover"],
                "purposes": s["_purposes"], "primary": s["_primary"], "zone": s["_zone"], "lane": s["_lane"], "cap_role": s["_cap_role"],
                "tags_text": ", ".join(f"{p['tag']}{' (' + p['confidence'] + ')' if p.get('confidence') else ''}" for p in (s["_c"].get("purposes") or []) if p["tag"] not in HIDDEN_PURPOSES),
            })
        max_total = max((r["total"] for r in records), default=1)
        for s in d.smokes:
            svg = self.thumb_file(s)
            if svg:
                self.write(f"data/thumbs/{s['_slug']}.svg", svg)
        self.write("data/smokes.json", json.dumps(records, separators=(",", ":")))
        body = f"""<h1>Smokes</h1><p class="muted">All {len(records)} smokes from the tournament. Click a row to open it. Tags are {esc(AUTO_NOTE)}. Damage shows the total with the concealed and detected parts under it. One-sided smokes (one replay for the game) and smokes from games with a data-quality flag are marked; both are left out of awards and leaderboards.</p>
<div class="filters">
<label>Clans <span class="multi" id="f-team"></span></label>
<label>Player <select id="f-player"><option value="">all</option></select></label>
<label>Ships <span class="multi" id="f-ship"></span></label>
<label>Map <select id="f-map"><option value="">all</option></select></label>
<label>Game <select id="f-game"><option value="">all</option></select></label>
<label>Type <select id="f-type"><option value="">all</option></select></label>
<label>Smoker class <select id="f-cls"><option value="">all</option></select></label>
<label>Movement <select id="f-movement"><option value="">all</option></select></label>
<label>Coverage <select id="f-coverage"><option value="">all</option></select></label>
<label>Purpose (any tag) <select id="f-purpose"><option value="">all</option></select></label>
<label>Primary purpose <select id="f-primary"><option value="">all</option></select></label>
<label>Zone <select id="f-zone"><option value="">all</option></select></label>
<label>Lane <select id="f-lane"><option value="">all</option></select></label>
<label>Phase <select id="f-phase"><option value="">all</option></select></label>
<label>Sort <select id="f-sort"><option value="total">smoke damage</option><option value="concealed">concealed damage</option><option value="dd">DD damage</option><option value="kills">kills from smoke</option><option value="deaths">smoke deaths</option><option value="radar">radar on us</option><option value="offensive">our radar detections</option><option value="swing">score change during the smoke</option><option value="depth">depth into a contested cap</option><option value="contested">distance to contested cap (nearest first)</option><option value="elapsed">time elapsed</option></select></label>
<span id="count" class="muted"></span> <a id="f-clear" class="small clear" href="smokes.html">clear filters</a></div>
<div class="scroll-x"><table class="smokes" id="smokes"><thead><tr><th></th><th>Clan</th><th>Player</th><th>Ship</th><th>Map</th><th>Game</th><th>Clock</th><th><abbr class="term" title="{esc(AUTO_NOTE)}">Tags</abbr></th><th>Zone / lane</th><th>{term("Damage", DAMAGE_DEF)}<br><span class="muted small">concealed / detected</span></th><th>{term("DD damage", DD_DEF)}</th><th>Distance to <abbr class="term" title="{esc(CONTEST_DEF)}">contested cap</abbr></th><th>Cap outcome</th><th><abbr class="term" title="{esc(RADAR_BAIT_DEF)}">Radar on us</abbr></th><th>{term("Our radar detections", METRIC_DEFS["offensive"])}</th><th>{term("Kills", METRIC_DEFS["kills"])}</th><th>{term("Smoke deaths", METRIC_DEFS["deaths"])}</th><th>{term("Selfish")}</th></tr></thead><tbody></tbody></table></div>
<p id="empty" class="muted" hidden>Nothing here, just clear skies.</p>
<button class="showmore" id="showmore" hidden>Show 100 more</button>
<script>window.SMOKES_URL = "data/smokes.json"; window.MAX_TOTAL = {max_total}; window.SELFISH_DEF = {json.dumps(SELFISH_DEF)};</script>"""
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
        team_names = [t["name"] for t in teams] or sorted({s["team"] for s in smokes})
        sections = ""
        for t in team_names:
            own = [s for s in smokes if s["team"] == t]
            one_sided = t in d.one_sided_games.get(key, set())
            note = ' <span class="muted small">(one replay for this game: these smokes are inferred from the other team\'s view and carry no damage)</span>' if one_sided else ""
            sections += f'<h2>{self.team_tag(t)} {esc(t)}: {len(own)} smoke{"s" if len(own) != 1 else ""}{note}</h2><section class="cards">{"".join(self.smoke_card(s, depth=1) for s in own) or "<p class=\"muted\">No smoke analysed.</p>"}</section>'
        quality = d.game_quality.get(key, "")
        quality_note = f'<p class="warn">Data quality: {esc(quality)}. This game is left out of the awards and the Players leaderboard.</p>' if quality else ""
        if d.game_notes.get(key) and not quality:
            quality_note += f'<p class="muted"><b>Note:</b> {esc(d.game_notes[key])}</p>'
        if key in d.one_sided_games:
            missing = ", ".join(sorted(d.one_sided_games[key]))
            present = ", ".join(t for t in team_names if t not in d.one_sided_games[key])
            quality_note += f'<p class="warn">One replay ({esc(present)}); {esc(missing)} smokes inferred, no {esc(missing)} damage.</p>'
        body = f"""<h1>{esc(smokes[0]['_games_label'])}</h1><p class="muted">{" | ".join(esc(h) for h in header)} | smokes analysed {self.smokes_column(key, team_names, 1)} | {" | ".join(links)}</p>{quality_note}
<section class="two-col">{self.map_figure(smokes[0]['map'], smokes, depth=1, size=480, anchor_prefix='g', fig_id='g')}<div><h2>Smokes across the match (n = {len(smokes)})</h2>{timeline}<h2>Score with smoke markers</h2>{score}</div></section>
<h2>Rosters</h2><section class="cards rosters">{roster}</section>{recon}
{sections}"""
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
        if s.get("one_sided"):
            flag += '<p class="warn">One-sided: only the opponent\'s replay exists for this game, so this smoke is inferred from their view; its owner may be uncertain and no damage is credited to it.</p>'
        if s["_quality"]:
            flag += f'<p class="warn">Data quality: {esc(s["_quality"])}. This game is left out of awards and leaderboards.</p>'
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
        # Violence: the damage splits, the targets, then the bad news. Shooters live in the Smokees table.
        if s["_total"] > 0:
            split = svg_stacked_bar([("fired from inside", s["_in"]), ("fired from outside, hidden by it", s["_behind"])], ["#F5C542", "#5DADE2"])
            parts = [("concealed", s["_concealed"]), ("detected", s["_detected"])] + ([("unknown", s["_unknown"])] if s["_unknown"] > 0 else [])
            conceal = svg_stacked_bar(parts, ["#6EE7B7", "#F87171", "#64748B"])
            kinds = f"shells {fmt_int(s['_shell'])}, fires they started {fmt_int(s['_fire'])}"
            if s["_airstrike"] > 0:
                kinds += f", airstrikes {fmt_int(s['_airstrike'])}"
            by = ", ".join(f"{r['reason']} {fmt_int(r['damage'])}" for r in sorted(s["_detected_by"], key=lambda r: -r["damage"])) or "none"
        else:
            split = '<span class="muted">no smoke damage</span>'
            conceal = '<span class="muted">-</span>'
            kinds = "-"
            by = "-"
        targets = s.get("targets_hit") or []
        if targets:
            def trow(x):
                cls = (x.get("ship_class") or "").lower()
                mark = ' <span class="pill dd">DD</span>' if cls == "destroyer" else ""
                sp = x.get("split") or {}
                return f'<tr><td>{esc(x["ship"])}{mark}</td><td>{esc(x["player"])}</td><td>{fmt_int(sp.get("concealed", 0))}</td><td>{fmt_int(sp.get("detected", 0))}</td><td><b>{fmt_int(x["damage"])}</b></td><td>{"yes" if x["sunk"] else "no"}</td></tr>'
            trows = "".join(trow(x) for x in sorted(targets, key=lambda x: -x["damage"]))
            target_table = f'<table class="games small"><thead><tr><th>Ship</th><th>Player</th><th>Concealed</th><th>Detected</th><th>Total</th><th>Sunk</th></tr></thead><tbody>{trows}</tbody></table>'
        else:
            target_table = '<p class="muted small">No enemy ship was damaged from this smoke.</p>'
        uncounted = s.get("targets_not_counted") or []
        if uncounted:
            if not targets:
                target_table = '<p class="muted small">No enemy ship took counted damage from this smoke.</p>'
            items = []
            for x in sorted(uncounted, key=lambda x: -x["damage"]):
                by_kind = sorted(x["by_kind"].items(), key=lambda kv: -kv[1])
                kinds = UNCOUNTED_KIND_TEXT.get(by_kind[0][0], by_kind[0][0]) if len(by_kind) == 1 else ", ".join(f"{UNCOUNTED_KIND_TEXT.get(k, k)} {fmt_int(v)}" for k, v in by_kind)
                items.append(f'<li>{esc(x["ship"])} ({esc(x["player"])}): {fmt_int(x["damage"])} from {kinds}{", sunk" if x["sunk"] else ""}</li>')
            target_table += f'<p class="muted small">Not counted as smoke damage: hits from this smoke by weapons that never earn credit (torpedoes, secondaries, flooding, unclassified hits; see About).</p><ul class="muted small uncounted">{"".join(items)}</ul>'
        spots = s.get("radar_detections_in_smoke") or []
        if spots:
            radar_on_us = f"{len(spots)} ({fmt_int(s['_radar_dmg'])} damage taken while spotted): " + "; ".join(f"{x.get('ship') or '?'} at {x.get('clock') or '?'}" + (f" by {x['source']}" if x.get("source") else "") for x in spots)
        else:
            radar_on_us = "none"
        deaths = s.get("smoke_deaths") or []
        if deaths:
            smoke_deaths = f"{len(deaths)}: " + "; ".join(f"{x['player']} ({x['ship']}) sunk at {x['death'].get('clock') or '?'}, concealed {x['concealed']} the smoke" + (", after it cleared" if x.get("after_cleared") else "") for x in deaths)
        else:
            smoke_deaths = "none"
        # Classification: plain values, a confidence dot, the numbers in tooltips.
        c = s["_c"]
        mv = c.get("movement") or {}
        cov = c.get("coverage") or {}

        def dot(conf):
            if conf:
                return f'<i class="dot {esc(conf)}" title="{esc(conf)} confidence"></i>'
            return '<i class="dot rule" title="rule-based, no confidence"></i>'

        def nice(label):
            return (label or "").replace("_", " ").capitalize()

        def val(text, definition, detail):
            title = definition + (f" | {detail}" if detail else "")
            return f'<abbr class="term val" title="{esc(title)}">{esc(text)}</abbr>'

        purposes = [p for p in c.get("purposes") or [] if p["tag"] not in HIDDEN_PURPOSES]
        if purposes:
            plist = "".join(f'<li>{val(nice(p["tag"]), PURPOSE_DEFS.get(p["tag"], ""), p.get("reason") or "")}{" <span class=\"muted small\">primary</span>" if i == 0 else ""}{dot(p.get("confidence"))}</li>' for i, p in enumerate(purposes))
            purposes_html = f'<ul class="tags">{plist}</ul>'
        else:
            purposes_html = '<span class="muted">none of the tactic tags applied</span>'
        special = ", ".join(c.get("special") or [])
        smoker = f"{esc(nice(s['_class']))}, {esc(s['_type'])} smoke" + (f' <span class="note">{esc(special)}</span>' if special else "")
        if mv:
            movement = val(nice(mv["label"]), MOVEMENT_DEFS.get(mv["label"], ""), mv.get("reason") or "") + dot(mv.get("confidence"))
        else:
            movement = '<span class="muted">unknown (no enemy or smoker position)</span>'
        coverage = val(nice(cov.get("label") or "?"), COVERAGE_DEFS.get(cov.get("label") or "", ""), cov.get("reason") or "") + dot(None)
        where = []
        where_detail = []
        if s["_zone"]:
            where.append(f"zone {s['_zone']}")
            if s.get("_grid"):
                where_detail.append(f"grid {s['_grid']}")
        if s["_lane"]:
            where.append(f"{s['_lane']} lane")
            if c.get("lane_offset_m") is not None:
                where_detail.append(f"{c['lane_offset_m'] / 1000:+.1f} km from the spawn axis")
        if s["_cap_role"]:
            where.append(f"nearest cap {c.get('cap_role_cap') or '?'} is a {s['_cap_role']} cap" + (" on the flank" if c.get("cap_flank") else ""))
        location = val("; ".join(where), "Zone from the map profile, lane and cap role from the smoker's spawn facing the enemy.", "; ".join(where_detail)) if where else "-"
        front_detail = []
        front_text = "-"
        if c.get("frontline_distance_m") is not None:
            v = c["frontline_distance_m"] / 1000
            front_text = f"{'past' if v > 0 else 'behind'} the midpoint between the fleets"
            front_detail.append(f"{abs(v):.1f} km {'past' if v > 0 else 'behind'} the midpoint")
        if c.get("nearest_enemy_m") is not None:
            front_detail.append(f"nearest enemy {c['nearest_enemy_m'] / 1000:.1f} km")
        if c.get("land_distance_m") is not None:
            front_detail.append(f"land {c['land_distance_m'] / 1000:.1f} km away")
            if front_text == "-":
                front_text = "near land" if c["land_distance_m"] <= 1000 else "in open water"
        front = val(front_text, "Where the smoke stood relative to the two fleets at activation.", "; ".join(front_detail)) if front_detail else "-"
        counter = ""
        if c.get("counter_smoke_of"):
            other = next((x for x in self.d.by_game.get(s["_key"], []) if x["smoke_id"] == c["counter_smoke_of"]), None)
            link = f'<a href="{other["_slug"]}.html">{esc(other["player"])} {esc(other["ship"])}</a>' if other else f'enemy smoke {c["counter_smoke_of"]}'
            reason = next((p.get("reason") for p in purposes if p["tag"] == "counter_smoke"), "")
            counter = f'<tr><td>Counter to</td><td>{link} <span class="muted small">{esc(reason)}</span></td></tr>'
        classification = f"""<div class="card classify"><h3>Classification <span class="muted small">{esc(AUTO_NOTE)}; hover a value for the numbers</span></h3><table class="kv">
<tr><td>Smoker</td><td>{smoker}</td></tr>
<tr><td>Movement</td><td>{movement}</td></tr>
<tr><td>Coverage</td><td>{coverage}</td></tr>
<tr><td>Purpose</td><td>{purposes_html}</td></tr>
<tr><td>Location</td><td>{location}</td></tr>
<tr><td>Front line</td><td>{front}</td></tr>
<tr><td>Caps in range</td><td>{esc(", ".join(c.get("caps_in_range") or [])) or "none"}</td></tr>{counter}</table>
<p class="conf-key">Confidence: <i class="dot high"></i> high <i class="dot medium"></i> medium <i class="dot low"></i> low <i class="dot rule"></i> rule-based</p></div>"""
        # Smokees: every covered ally and every credited shooter, numbered as on the zoomed view.
        smokees = s.get("smokees") or []
        if smokees:
            role_text = {"smoker": "smoker", "inside": "inside", "behind": "behind", "line_of_fire": "line of fire"}

            def reasons(m):
                by = sorted(m.get("detected_by") or [], key=lambda r: -r["seconds"])
                if by:
                    return ", ".join(f'{esc(r["kind"])}{" (inferred)" if r.get("inferred") else ""} {r["seconds"]:.0f} s' for r in by)
                if m.get("detections"):
                    return ", ".join(f'{esc(x["kind"])}{" (inferred)" if x.get("inferred") else ""}' for x in m["detections"])
                return '<span class="muted">-</span>'

            def mrow(m):
                sp = m.get("split") or {}
                pct = f'{m["undetected_pct"]:.0f}%' if m.get("undetected_pct") is not None else '<span class="muted">-</span>'
                who = (f'<a href="{self.player_href(m["player"], 1)}">' + esc(m["player"]) + "</a>") if m["player"] in self.players else esc(m["player"])
                return (f'<tr><td><span class="nbadge">{m.get("badge", "")}</span></td><td>{esc(m["ship"])}</td><td>{who}</td><td>{role_text.get(m.get("role"), m.get("role"))}</td>'
                        f'<td title="{m["seconds_concealed"]:.0f} s covered">{pct}</td><td class="small">{reasons(m)}</td><td>{fmt_int(sp.get("concealed", 0))} / {fmt_int(sp.get("detected", 0))}</td><td>{fmt_int(m.get("damage_taken", 0))}</td><td>{m["kills"]}</td></tr>')
            mrows = "".join(mrow(m) for m in sorted(smokees, key=lambda m: m.get("badge", 0)))
            smokees_html = f'<div class="card"><h3>Smokees <span class="muted small">the smoker, every ally the smoke covered (inside it, firing undetected from behind it, or with it in their line of fire) and every credited shooter; numbers match the zoomed view</span></h3><div class="scroll-x"><table class="games small"><thead><tr><th></th><th>Ship</th><th>Player</th><th>Role</th><th title="share of the covered time while undetected">Undetected</th><th>Detected by (time)</th><th>{term("Damage dealt", CONCEALED_DEF)}<br><span class="muted">concealed / detected</span></th><th>Damage taken while covered</th><th>Kills</th></tr></thead><tbody>{mrows}</tbody></table></div></div>'
        else:
            smokees_html = '<div class="card"><h3>Smokees</h3><p class="muted small">No allied ship was covered by this smoke.</p></div>'
        deployment = f"""<div class="card"><h3>Deployment</h3><table class="kv">
<tr><td>Duration</td><td>{esc(dur)}</td></tr>
<tr><td>Allies in smoke at capture</td><td>{esc(', '.join(s.get('allies_in_smoke') or [])) or 'none'}</td></tr>
<tr><td>{term('Selfish smoke')}</td><td>{selfish}</td></tr>
<tr><td>Hand tags</td><td class="muted">untagged</td></tr></table></div>"""
        violence = f"""<div class="card"><h3>Violence</h3><table class="kv">
<tr><td>{term('Smoke damage', DAMAGE_DEF)}</td><td><b>{fmt_int(s['_total'])}</b></td></tr>
<tr><td>{term('Concealed vs detected', CONCEALED_DEF)}</td><td>{conceal}</td></tr>
<tr><td>Detected shooters were spotted by</td><td>{esc(by)}</td></tr>
<tr><td>By where the shooter sat</td><td>{split}</td></tr>
<tr><td>By kind</td><td>{esc(kinds)}</td></tr>
<tr><td>{term('DD damage', DD_DEF)}</td><td><b>{fmt_int(s['_dd'])}</b></td></tr>
<tr><td>{term('Kills from smoke', METRIC_DEFS['kills'])}</td><td><b>{s['_kills']}</b></td></tr></table>
<p class="muted small">Shooters credited are in the Smokees table below.</p>
<h4>Enemy ships damaged from the smoke</h4>{target_table}
<div class="bad"><h4>The bad news</h4><table class="kv">
<tr><td><abbr class="term" title="{esc(RADAR_BAIT_DEF)}">Radar spots on us</abbr></td><td>{esc(radar_on_us)}</td></tr>
<tr><td>{term('Smoke deaths', METRIC_DEFS['deaths'])}</td><td>{esc(smoke_deaths)}</td></tr></table></div></div>"""
        objectives = f"""<div class="card"><h3>Objectives</h3><table class="kv">
<tr><td><abbr class="term" title="{esc(CONTEST_DEF)} Averaged over the smoke's life, edge to edge. At capture: {esc(cap_text(s))}.">Distance to contested cap</abbr></td><td>{esc(contested_text(s))}</td></tr>
<tr><td>Cap outcome</td><td>{esc(cap_outcome_text(s))}</td></tr>
<tr><td>Denial signal</td><td>{esc(denial)}</td></tr>
<tr><td>Score at capture</td><td>{esc(st.get('score_ours', '-'))} : {esc(st.get('score_theirs', '-'))}{(' (swing ' + f"{s['_score_swing']:+d}" + ')') if s['_score_swing'] is not None else ''}</td></tr>
<tr><td>{term('Our radar from the smoke', METRIC_DEFS['offensive'])}</td><td>{esc(offensive)}</td></tr>
<tr><td>{term('Radar cap coverage', METRIC_DEFS['coverage'])}</td><td>{esc(radar_cap)}</td></tr></table></div>"""
        body = f"""<h1>{self.team_tag(s['team'])} <a href="{self.player_href(s['player'], 1)}">{esc(s['player'])}</a> <span class="muted">{esc(s['ship'])}</span></h1>
<p class="muted">{esc(self.d.map_title(s['map']))} | {esc(s['_games_label'])} | activated {esc(s['_act_clock'])} ({elapsed_text(s['_elapsed']) if s['_elapsed'] is not None else '?'} elapsed, {s['_phase'] or ''}), captured {esc(s['_cap_clock'])} | {esc(s.get('smoke_type') or '')} smoke {esc(s.get('variant') or '')}</p>
<p class="big">{fmt_int(s['_total'])} smoke damage{(', ' + str(s['_kills']) + (' kill' if s['_kills'] == 1 else ' kills')) if s['_kills'] else ''} <span class="muted small">{fmt_int(s['_concealed'])} concealed, {fmt_int(s['_detected'])} detected</span></p>{flag}{overlap}
<section class="frames one"><figure>{self.img(s, 'frame_cap', 1, lazy=False)}<figcaption>The full map at capture, when the smoke was fully laid ({esc(s['_cap_clock'])}).</figcaption></figure></section>
<section class="frames zoomed"><figure>{self.img(s, 'frame_cap_zoom', 1, lazy=False)}<figcaption>Zoomed to the smoke, every smokee (numbered as in the Smokees table) and every enemy damaged from it, at least half the map: ships and headings, the smoke, the caps, and the credited fire lines labelled with damage.</figcaption></figure></section>
{clip}
{classification}
<div class="groups"><div>{deployment}{objectives}</div>{violence}</div>
{smokees_html}
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
.smoke-card{padding:0;overflow:hidden}.smoke-card .thumb{border-radius:0;border:0}.card-body{padding:8px 10px}
.thumb{position:relative;aspect-ratio:1;width:100%;background-size:200% 200%;background-repeat:no-repeat;background-color:#0B1C2C;border-radius:6px;overflow:hidden;border:1px solid var(--line)}.thumb svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.award-hero{display:flex;gap:14px;align-items:flex-start;margin:8px 0}.award-hero>a{flex:0 0 300px;max-width:52%}.award-hero .thumb{border-radius:8px}
.terms{margin:4px 0 16px;padding-left:20px}.terms li{margin:4px 0}
.pill{display:inline-block;padding:0 6px;border-radius:999px;background:#2A4258;font-size:.8em}.pill.cls{background:#F5C542;color:#07131f;font-weight:700}.tagcell{min-width:150px}
.conf{display:inline-block;padding:0 5px;border-radius:4px;font-size:.75em;margin-left:4px}.conf.high{background:#166534;color:#DCFCE7}.conf.medium{background:#854D0E;color:#FEF9C3}.conf.low{background:#7F1D1D;color:#FEE2E2}
.tags{margin:0;padding-left:18px}.tags li{margin:2px 0}.classify{border-left:5px solid #B388FF;margin:12px 0}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-left:6px;vertical-align:middle;cursor:help;border:1px solid #07131f}.dot.high{background:#22C55E}.dot.medium{background:#EAB308}.dot.low{background:#EF4444}.dot.rule{background:#94A3B8}
.classify .val{cursor:help;text-decoration:underline dotted}.classify .tags li{list-style:none;margin-left:-18px}
.nbadge{display:inline-block;min-width:20px;height:20px;line-height:18px;border-radius:50%;background:#F5C542;color:#07131f;font-weight:700;text-align:center;font-size:.8em;border:1px solid #07131f}.pill.dd{background:#F87171;color:#07131f;font-weight:700}
.conf-key{font-size:.8em;color:var(--muted)}
.badge.all{background:#334155;color:#CBD5E1}.filters.lens{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:6px 10px;align-items:center}
.lens-toggle{margin:8px 0}.lens-toggle button{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 10px;margin-right:6px;cursor:pointer}.lens-toggle button.on{background:#F5C542;color:#07131f}
.mapwrap .zones{display:none}.mapwrap.showzones .zones{display:block}
.cchart .row{grid-template-columns:52px 1fr 110px}.panel a.row.wide{grid-template-columns:230px 1fr 60px;color:var(--text);text-decoration:none}.panel a.row.wide:hover{background:var(--panel2)}.panel a.row.wide span:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.smoke-card[hidden]{display:none}.award-meta{flex:1;min-width:0}.award-meta .big{margin:6px 0}
.card.award .clip{margin-top:8px}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 20px}.stat{background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--c,#9FB0C0);border-radius:8px;padding:8px 14px;min-width:150px}.stat b{display:block;font-size:1.5em}.stat span{color:var(--muted);font-size:.85em}.stats.lead .stat{min-width:220px;border-width:1px 1px 1px 8px}.stats.lead .stat b{font-size:2em}
.tag{display:inline-block;padding:1px 7px;border-radius:999px;font-size:.78em;font-weight:700;background:var(--c);color:#07131f}.tag.other{background:#475569;color:var(--text)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 16px}.chip{display:inline-flex;align-items:center;gap:5px;padding:3px 10px 3px 6px;border-radius:999px;background:var(--panel);border:1px solid var(--line);border-left:10px solid var(--c);color:var(--text);text-decoration:none;font-size:.85em}.chip b{color:#F5C542}.chip:hover{background:var(--panel2)}.chip.small-sample{opacity:.55}
.pill.warn-pill{background:#7C2D12;color:#FED7AA;font-weight:600;cursor:help}
nav.top a.hub{color:var(--muted);font-size:.85em;padding:4px 8px;border:1px solid var(--line);border-radius:6px;margin-right:8px}
.filters label.check{flex-direction:row;align-items:center;gap:6px;color:var(--text)}
table.clan-table td.small-sample,table.clan-table tr.small-sample td{opacity:.55}table.clan-table td.n{color:var(--muted);font-size:.8em}table.clan-table th{white-space:nowrap}
.cards.groups-4{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.mapwrap .heat rect{pointer-events:auto}.mapwrap.lines .heat{display:none}.mapwrap .paths{display:none}.mapwrap.lines .paths{display:block}
.showmore{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:6px 14px;cursor:pointer;margin:8px 0}
.badge{display:inline-block;padding:1px 7px;border-radius:6px;font-size:.75em;background:#2A4258;color:#F5C542;margin-left:4px;cursor:help}
.muted{color:var(--muted)}.small{font-size:.85em}.big{font-size:1.4em;font-weight:700}.note{color:#F5C542}.warn{color:#FB923C}.summary{background:var(--panel2);padding:8px 12px;border-radius:8px}
table.kv td{padding:3px 8px 3px 0;vertical-align:top}table.kv td:first-child{color:var(--muted);max-width:260px}
.mini{display:inline-block;width:92px;height:9px;background:#0B1C2C;border-radius:4px;vertical-align:middle;margin-left:6px}.mini i{display:block;height:100%;border-radius:4px}
.legend-row{display:flex;flex-wrap:wrap;gap:8px;font-size:.8em;margin-top:4px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px}
.frames.one{margin:8px 0}.frames.zoomed{max-width:780px;margin:8px auto 12px}.frames img{width:100%;border-radius:6px;border:1px solid var(--line)}
.groups{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0}.groups .card{margin-bottom:16px}.groups h4{margin:12px 0 4px}.bad{border-top:2px solid #F87171;margin-top:12px;padding-top:6px}.bad h4{color:#F87171;margin-top:4px}table.games.small{font-size:.85em}.frames figure{margin:0}.frames figcaption{color:var(--muted);font-size:.8em;margin-top:4px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.mapwrap{position:relative;width:100%;align-self:start}.mapwrap svg.mapsvg{display:block;width:100%;height:auto;aspect-ratio:1/1;border-radius:8px}
.mapwrap .grid line{stroke:#fff;stroke-opacity:.18;stroke-width:1}.mapwrap .gridlabels text{fill:#fff;fill-opacity:.7;font-size:12px;text-anchor:middle;font-weight:600}
.mapwrap .caps circle{fill:#fff;fill-opacity:.08;stroke:#fff;stroke-opacity:.6;stroke-width:1.5;stroke-dasharray:5,4}.mapwrap .caplabel{fill:#fff;fill-opacity:.85;font-size:20px;font-weight:700;text-anchor:middle}
.mapwrap .smokepath polyline{fill:none;stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round;opacity:.9}.mapwrap .smokepath:hover polyline{stroke-width:6;opacity:1}.mapwrap .smokepath.hide{display:none}
.ships{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap}.ships .legend-row{flex-direction:column;gap:2px}
.mapcol{grid-template-columns:3fr 2fr;align-items:start}.chart{display:grid;gap:10px}.charts{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:12px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px}.panel h4{margin:0 0 4px;font-size:.9em;color:var(--muted)}
svg.chart .lbl{fill:var(--text);font-size:11px}svg.chart .val{fill:var(--muted);font-size:11px}svg.chart .zero{stroke:#94A3B8;stroke-width:1}
.chart .row,.cchart .row,#player-chart .row{display:grid;grid-template-columns:52px 1fr 90px;align-items:center;gap:6px;font-size:.85em;margin:2px 0}.chart .row .bar,.cchart .row .bar,#player-chart .row .bar{position:relative;height:12px;background:#0B1C2C;border-radius:3px}.chart .row .bar i,.cchart .row .bar i,#player-chart .row .bar i{position:absolute;top:0;height:100%;border-radius:3px}.chart .row .bar b,.cchart .row .bar b{position:absolute;top:-2px;bottom:-2px;width:1px;background:#94A3B8}.chart .row span:last-child,.cchart .row span:last-child,#player-chart .row span:last-child{text-align:right}.chart .row.dim{opacity:.4}
.lens-set[hidden]{display:none}
.heats{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}.heat{margin:0}.heat figcaption{font-size:.8em;color:var(--muted);margin-top:4px}
.filters.mapfilters{align-items:flex-start}.range{min-width:320px}.rangevals{margin-left:6px}.dual{position:relative;display:block;height:22px}.dual input[type=range]{position:absolute;left:0;top:0;width:100%;margin:0;background:none;pointer-events:none;-webkit-appearance:none;appearance:none;height:22px}
.dual input[type=range]::-webkit-slider-runnable-track{height:4px;background:var(--line);border-radius:2px}
.dual input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;pointer-events:auto;width:16px;height:16px;border-radius:50%;background:#F5C542;border:2px solid #07131f;margin-top:-6px;cursor:pointer}
.dual input[type=range]::-moz-range-track{height:4px;background:var(--line)}.dual input[type=range]::-moz-range-thumb{pointer-events:auto;width:14px;height:14px;border-radius:50%;background:#F5C542;border:2px solid #07131f;cursor:pointer}
.multi{position:relative;display:inline-block}.multi .msel-btn{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 8px;cursor:pointer;min-width:130px;max-width:260px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:left;font:inherit;font-size:.95em}.multi .msel-btn.on{border-color:#F5C542;color:#F5C542}
.multi .msel-pop{position:absolute;z-index:30;top:100%;left:0;min-width:230px;max-height:340px;overflow:auto;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:6px;box-shadow:0 8px 24px rgba(0,0,0,.45)}.multi .msel-pop[hidden]{display:none}
.multi .msel-search{width:100%;box-sizing:border-box;background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 6px;margin-bottom:4px;font:inherit;font-size:.9em}
.multi .msel-acts{display:flex;gap:12px;font-size:.85em;margin:2px 0 6px}.multi .msel-acts a{cursor:pointer;color:#9CD3FF}
.multi .msel-list label{display:flex;flex-direction:row;align-items:center;gap:6px;color:var(--text);font-size:.9em;padding:2px;cursor:pointer}.multi .msel-list label.hide{display:none}.multi .msel-list label .n{color:var(--muted);margin-left:auto}
.seg{display:flex;gap:10px;padding:4px 0}.seg label{display:flex;flex-direction:row;align-items:center;gap:4px;color:var(--text);font-size:1em}
.mapwrap .smokepath polyline.cloud{stroke-opacity:.26;opacity:1}.mapwrap .smokepath:hover polyline.cloud{stroke-opacity:.5}
.filters.sticky{position:sticky;top:0;z-index:20;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line)}a.clear{color:#9CD3FF;align-self:center}
ul.uncounted{margin:4px 0 8px 18px}
.mode-toggle{display:inline-block}table.clan-table td.pcell{text-align:right}table.clan-table td:nth-child(-n+5){white-space:nowrap}table.clan-table th[data-key]{text-decoration:underline dotted}
.tendency{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin:8px 0 14px}.tcell{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px;display:flex;flex-direction:column;gap:2px}.tcell b{font-size:1.5em;line-height:1.1}.tcell span{font-size:.78em;color:var(--muted)}.tcell em{font-style:normal;font-weight:700;font-size:.85em;color:#F5C542}.tcell em.none{visibility:hidden}

.bracket{display:flex;gap:16px;overflow-x:auto;padding:4px 0 12px}.bside{flex:1 1 auto}.bside h4{margin:6px 0;color:var(--muted)}.brow{display:flex;gap:10px}.bfinal{display:flex;align-items:center}.bcol{display:flex;flex-direction:column;justify-content:space-around;gap:8px;flex:1 1 0;min-width:150px}.bcol h3{margin:0;font-size:.85em;color:var(--muted);text-align:center}
.series,a.series{display:block;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:6px 8px;color:var(--text);text-decoration:none;font-size:.9em}a.series:hover{border-color:#9CD3FF}.series.tbd{opacity:.45}.srow{display:flex;align-items:center;gap:6px;padding:2px 0}.srow .sname{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.srow.won{font-weight:700}.srow.won b{color:#F5C542}
table.games{width:100%;border-collapse:collapse;font-size:.9em}table.games th,table.games td{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left}table.games tr[hidden]{display:none}table.sortable th[data-key]{cursor:pointer;text-decoration:underline dotted}
.scroll-x{overflow-x:auto;max-width:100%}
.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:end;margin:10px 0}.filters label{display:flex;flex-direction:column;font-size:.8em;color:var(--muted)}
select{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 6px}
table.smokes{width:100%;border-collapse:collapse;font-size:.9em}table.smokes th,table.smokes td{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}table.smokes .thumb{width:84px;height:84px}table.smokes img.thumb{display:block;object-fit:cover;border-radius:6px;border:1px solid var(--line);background:#0B1C2C}table.smokes tr[data-href]{cursor:pointer}table.smokes tr[data-href]:hover{background:var(--panel2)}
.cards.rosters{grid-template-columns:repeat(auto-fit,minmax(380px,1fr))}table.roster{width:100%;font-size:.85em;border-collapse:collapse}table.roster th{text-align:left;color:var(--muted)}table.roster td,table.roster th{padding:2px 6px 2px 0}table.roster td:last-child{text-align:right}
.clip video{width:100%;max-width:900px;border-radius:8px;background:#000}.clip-controls{margin:6px 0}.clip-controls button{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 10px;margin-right:6px;cursor:pointer}.clip-controls button.on{background:#F5C542;color:#07131f}
.smoke-nav{margin:20px 0;display:flex;gap:12px;flex-wrap:wrap}.noimg{background:var(--panel2);color:var(--muted);padding:30px;text-align:center;border-radius:6px}
@media(max-width:800px){.two-col,.groups,.mapcol{grid-template-columns:1fr}.award-hero{flex-direction:column}.award-hero>a{flex:none;max-width:100%}.cards.awards,.charts{grid-template-columns:1fr}.brow{flex-direction:column}.bcol{min-width:0}
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

  // Shared horizontal bar panel: rows of {team, v, n, color}; values formatted by a code.
  function fmtVal(v, fmt){
    if (v === null || v === undefined) return '-';
    if (fmt === 'pct') return Math.round(v) + '%';
    if (fmt === 's') return Math.round(v) + ' s';
    if (fmt === 'f1') return v.toFixed(1);
    if (fmt === 'f2') return v.toFixed(2);
    if (fmt === 'pts') return (v >= 0 ? '+' : '') + Math.round(v) + ' pts';
    if (fmt === 'km') return (v/1000).toFixed(1) + ' km';
    return Math.round(v).toLocaleString();
  }
  function panelHtml(title, rows, fmtCode, note){
    var vals = rows.map(function(r){ return r.v; }).filter(function(v){ return v !== null && v !== undefined; });
    var max = Math.max(0, Math.max.apply(null, vals.length ? vals : [0])), min = Math.min(0, Math.min.apply(null, vals.length ? vals : [0]));
    var span = (max - min) || 1, zero = (-min) / span * 100;
    var html = '<h4>' + title + '</h4>';
    rows.forEach(function(r){
      var bar = '';
      if (r.v !== null && r.v !== undefined) {
        var left = r.v >= 0 ? zero : zero + r.v / span * 100, w = Math.abs(r.v) / span * 100;
        bar = '<i style="left:' + left.toFixed(1) + '%;width:' + w.toFixed(1) + '%;background:' + r.color + '"></i>' + (min < 0 ? '<b style="left:' + zero.toFixed(1) + '%"></b>' : '');
      }
      html += '<div class="row' + (r.dim ? ' dim' : '') + '"><span>' + r.team + '</span><span class="bar">' + bar + '</span><span>' + fmtVal(r.v, fmtCode) + (r.n !== undefined ? ' (n=' + r.n + ')' : '') + '</span></div>';
    });
    if (note) html += '<p class="muted small">' + note + '</p>';
    return html;
  }
  function lensKey(prefix){ return document.getElementById(prefix + '-class').value + '|' + document.getElementById(prefix + '-type').value; }
  function noteFor(spec){ return spec.key === 'charge' ? 'n = charges carried' : (spec.key === 'coverage' ? 'n = smokes with a concealed radar ship' : (spec.key === 'offensive' ? 'n = games' : '')); }
  function termHtml(spec){ return spec.def ? '<abbr class="term" title="' + spec.def.replace(/"/g, '&quot;') + '">' + spec.title + '</abbr>' : spec.title; }

  // Clans page: the sortable table (values or percentiles) and the charts for the chosen lens, bars sorted best first.
  function pctShade(p){ return p === null || p === undefined ? '' : ' style="background:rgba(93,173,226,' + (0.05 + 0.55 * p / 100).toFixed(2) + ')"'; }
  if (window.CLAN_METRICS && window.CLAN_SPEC && document.getElementById('clans-class')) {
    var clansSel = ['clans-class', 'clans-type'].map(function(id){ return document.getElementById(id); });
    clansSel[0].value = 'destroyer';
    var allBox = document.getElementById('clans-all');
    var tableSort = {key: 'concealed_per_game', asc: false};
    var tableMode = new URLSearchParams(location.search).get('mode') === 'pct' ? 'pct' : 'values';
    document.querySelectorAll('#clans-mode button').forEach(function(b){ b.classList.toggle('on', b.dataset.mode === tableMode); });
    var renderClans = function(){
      var key = lensKey('clans'), data = window.CLAN_METRICS[key] || {}, pcts = (window.CLAN_PCT || {})[key] || {};
      var total = 0;
      window.CLAN_TEAMS.forEach(function(t){ total += (data[t] && data[t].n) || 0; });
      document.getElementById('clans-count').textContent = total + ' smokes in this lens';
      var small = function(t){ return (window.CLAN_GAMES||{})[t] < (window.CLAN_MIN_GAMES||0); };
      window.CLAN_SPEC.forEach(function(spec){
        var el = document.querySelector('.cchart[data-key="' + spec.key + '"]');
        if (!el) return;
        var rows = window.CLAN_TEAMS.map(function(t){ var m = (data[t] || {})[spec.key] || [null, 0]; return {team: t, v: m[0], n: m[1], color: (window.TEAM_COLORS||{})[t] || '#94A3B8', dim: small(t)}; });
        var known = rows.filter(function(r){ return r.v !== null; }), unknown = rows.filter(function(r){ return r.v === null; });
        known.sort(function(a, b){ return spec.lower ? a.v - b.v : b.v - a.v; });
        var list = known.concat(unknown);
        if (!(allBox && allBox.checked)) list = list.slice(0, 12);
        el.innerHTML = panelHtml(termHtml(spec), list, spec.fmt, noteFor(spec) + (list.length < rows.length ? (noteFor(spec) ? '; ' : '') + 'top ' + list.length + ' of ' + rows.length : ''));
      });
      // The table: one row per clan, sorted by the chosen column's value in both modes.
      var tbody = document.querySelector('#clan-table tbody');
      if (tbody) {
        var rowsT = window.CLAN_TEAMS.map(function(t){ var m = data[t] || {}; return {team: t, m: m, games: m.games || 0, n: m.n || 0, wins: m.wins || 0, losses: m.losses || 0, win_pct: m.win_pct}; });
        var val = function(r){
          if (tableSort.key === 'games') return r.games;
          if (tableSort.key === 'n') return r.n;
          if (tableSort.key === 'wins') return r.wins + (r.win_pct || 0) / 1000;
          if (tableSort.key === 'win_pct') return r.win_pct === null || r.win_pct === undefined ? (tableSort.asc ? Infinity : -Infinity) : r.win_pct;
          var x = (r.m[tableSort.key] || [null])[0]; return x === null || x === undefined ? (tableSort.asc ? Infinity : -Infinity) : x;
        };
        rowsT.sort(function(a, b){ return tableSort.asc ? val(a) - val(b) : val(b) - val(a); });
        var base = window.CLAN_BASE || 0;
        tbody.innerHTML = rowsT.map(function(r){
          var cells = '<td><a href="' + (window.CLAN_HREF||{})[r.team] + '"><span class="tag" style="--c:' + ((window.TEAM_COLORS||{})[r.team]||'#94A3B8') + '">' + r.team + '</span></a>' + (small(r.team) ? ' <span class="pill warn-pill" title="fewer than ' + window.CLAN_MIN_GAMES + ' games: ranked against the ' + base + ' clans with enough games">small sample</span>' : '') + '</td>'
            + '<td>' + r.games + '</td><td>' + r.wins + '-' + r.losses + '</td><td>' + (r.win_pct === null || r.win_pct === undefined ? '-' : Math.round(r.win_pct) + '%') + '</td><td>' + r.n + '</td>';
          window.CLAN_SPEC.forEach(function(spec){
            var m = r.m[spec.key] || [null, 0], p = (pcts[r.team] || {})[spec.key];
            var pTxt = p === null || p === undefined ? '-' : String(Math.round(p));
            var vTxt = fmtVal(m[0], spec.fmt) + ' (n=' + m[1] + ')';
            if (tableMode === 'pct') cells += '<td class="pcell"' + pctShade(p) + ' title="' + vTxt.replace(/"/g, '&quot;') + '">' + pTxt + '</td>';
            else cells += '<td class="pcell"' + pctShade(p) + ' title="percentile ' + pTxt + ' among ' + base + ' clans with ' + window.CLAN_MIN_GAMES + '+ games">' + fmtVal(m[0], spec.fmt) + ' <span class="n">(' + m[1] + ')</span></td>';
          });
          return '<tr class="' + (small(r.team) ? 'small-sample' : '') + '">' + cells + '</tr>';
        }).join('');
      }
    };
    clansSel.forEach(function(s){ s.addEventListener('change', renderClans); });
    if (allBox) allBox.addEventListener('change', renderClans);
    document.querySelectorAll('#clans-mode button').forEach(function(b){ b.addEventListener('click', function(){ tableMode = b.dataset.mode; document.querySelectorAll('#clans-mode button').forEach(function(x){ x.classList.toggle('on', x === b); }); renderClans(); }); });
    document.querySelectorAll('#clan-table th[data-key]').forEach(function(th){
      th.addEventListener('click', function(){ if (tableSort.key === th.dataset.key) tableSort.asc = !tableSort.asc; else { tableSort.key = th.dataset.key; tableSort.asc = th.dataset.key === 'deaths'; } renderClans(); });
    });
    renderClans();
  }

  // Players leaderboard: clan filter and the minimum-smokes toggle.
  var ptable = document.getElementById('players');
  if (ptable && document.getElementById('p-clan')) {
    var prows = Array.from(ptable.querySelectorAll('tbody tr'));
    var prender = function(){
      var c = document.getElementById('p-clan').value, min = document.getElementById('p-min').checked, n = 0;
      prows.forEach(function(r){ var ok = (!c || r.dataset.team === c) && (!min || parseInt(r.dataset.smokes, 10) >= __PLAYER_MIN__); r.hidden = !ok; if (ok) n++; });
      document.getElementById('p-count').textContent = n + ' of ' + prows.length + ' players';
    };
    ['p-clan', 'p-min'].forEach(function(id){ document.getElementById(id).addEventListener('change', prender); });
    prender();
  }

  // Clan page: the stat tiles and the tendency strip for the chosen lens.
  if (window.CLAN_METRICS && window.CLAN_TEAM && document.getElementById('clan-class')) {
    var leadKeys = ['uptime', 'swing', 'punished'];
    var tile = function(spec, m){
      return '<div class="stat" style="--c:' + ((window.TEAM_COLORS||{})[window.CLAN_TEAM] || '#94A3B8') + '"><b>' + fmtVal(m[0], spec.fmt) + '</b><span>' + termHtml(spec) + ' (n = ' + m[1] + ')</span></div>';
    };
    var specOf = {}; window.CLAN_SPEC.forEach(function(s){ specOf[s.key] = s; });
    var renderClan = function(){
      var key = lensKey('clan');
      var data = (window.CLAN_METRICS[key] || {})[window.CLAN_TEAM] || {};
      var leadHtml = '', moreHtml = '';
      window.CLAN_SPEC.forEach(function(spec){ var m = data[spec.key] || [null, 0]; if (leadKeys.indexOf(spec.key) >= 0) leadHtml += tile(spec, m); else moreHtml += tile(spec, m); });
      document.getElementById('clan-lead').innerHTML = leadHtml;
      document.getElementById('clan-more').innerHTML = moreHtml + '<div class="stat"><b>' + (data.n || 0) + '</b><span>smokes in this lens (' + (data.games || 0) + ' games)</span></div>';
      var strip = document.getElementById('clan-tendency'), pcts = (window.CLAN_PCT || {})[key] || {};
      if (strip) {
        strip.innerHTML = (window.CLAN_TENDENCY || []).map(function(t){
          var p = pcts[t[0]], m = data[t[0]] || [null, 0], spec = specOf[t[0]] || {fmt: 'int'};
          var word = p === null || p === undefined ? '' : (p >= 80 ? t[2] : (p <= 20 ? t[3] : ''));
          var pTxt = p === null || p === undefined ? '-' : Math.round(p);
          return '<div class="tcell"' + pctShade(p) + ' title="' + fmtVal(m[0], spec.fmt).replace(/"/g, '&quot;') + ' (n=' + m[1] + ')"><b>' + pTxt + '</b><span>' + t[1] + '</span>' + (word ? '<em>' + word + '</em>' : '<em class="none">&nbsp;</em>') + '</div>';
        }).join('');
      }
    };
    document.getElementById('clan-class').value = 'destroyer';
    ['clan-class', 'clan-type'].forEach(function(id){ document.getElementById(id).addEventListener('change', renderClan); });
    renderClan();
  }

  // Award lens toggles (Home, Players).
  document.querySelectorAll('.lens-toggle').forEach(function(bar){
    bar.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click', function(){
        bar.querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x === b); });
        var el = bar.nextElementSibling;
        while (el && el.classList.contains('lens-set')) { el.hidden = el.dataset.lens !== b.dataset.lens; el = el.nextElementSibling; }
      });
    });
  });

  // Player page: lens over the cards and the damage chart.
  if (window.PLAYER_SMOKES && document.getElementById('player-class')) {
    var renderPlayer = function(){
      var cls = document.getElementById('player-class').value, typ = document.getElementById('player-type').value, n = 0;
      document.querySelectorAll('#player-cards .smoke-card').forEach(function(c){ var ok = (cls === 'all' || c.dataset.cls === cls) && (typ === 'all' || c.dataset.type === typ); c.hidden = !ok; if (ok) n++; });
      var rows = window.PLAYER_SMOKES.filter(function(r){ return (cls === 'all' || r.cls === cls) && (typ === 'all' || r.type === typ); }).slice(0, 12);
      var max = Math.max(1, Math.max.apply(null, rows.map(function(r){ return r.v; }).concat([0])));
      var html = '<h4>Damage per smoke, top 12 of ' + n + ' shown; click a bar to open the smoke</h4>';
      rows.forEach(function(r){ html += '<a class="row wide" href="' + r.href + '"><span title="' + r.label.replace(/"/g, '&quot;') + '">' + r.label + '</span><span class="bar"><i style="left:0;width:' + (r.v / max * 100).toFixed(1) + '%;background:' + r.color + '"></i></span><span>' + Math.round(r.v).toLocaleString() + '</span></a>'; });
      document.getElementById('player-chart').innerHTML = rows.length ? html : '<p class="muted small">Nothing here, just clear skies.</p>';
      document.getElementById('player-count').textContent = n + ' smokes shown';
    };
    ['player-class', 'player-type'].forEach(function(id){ document.getElementById(id).addEventListener('change', renderPlayer); });
    renderPlayer();
  }

  // Maps page: zone overlay toggle.
  var zonesBox = document.getElementById('showzones');
  if (zonesBox) {
    var applyZones = function(){ document.querySelectorAll('.mapwrap').forEach(function(m){ m.classList.toggle('showzones', zonesBox.checked); }); };
    zonesBox.addEventListener('change', applyZones);
    if (location.hash.indexOf('zones') >= 0 || new URLSearchParams(location.search).get('zones')) { zonesBox.checked = true; applyZones(); }
  }

  // Multi-select: a button that opens a searchable checkbox list. Empty selection means all.
  function makeMulti(el, options, onChange){
    var selected = [];
    el.innerHTML = '<button type="button" class="msel-btn">all</button><div class="msel-pop" hidden><input class="msel-search" placeholder="search"><div class="msel-acts"><a class="msel-clear">clear</a><a class="msel-close">close</a></div><div class="msel-list"></div></div>';
    var btn = el.querySelector('.msel-btn'), pop = el.querySelector('.msel-pop'), list = el.querySelector('.msel-list'), search = el.querySelector('.msel-search');
    list.innerHTML = options.map(function(o){ return '<label data-v="' + escA(o.value) + '"><input type="checkbox" value="' + escA(o.value) + '"> <span>' + escA(o.label) + '</span>' + (o.count !== undefined ? '<span class="n">' + o.count + '</span>' : '') + '</label>'; }).join('');
    function label(){ if (!selected.length) return 'all'; var names = selected.slice(0, 3).join(', '); return selected.length > 3 ? names + ' +' + (selected.length - 3) : names; }
    function sync(){ btn.textContent = label(); btn.classList.toggle('on', selected.length > 0); list.querySelectorAll('input').forEach(function(i){ i.checked = selected.indexOf(i.value) >= 0; }); }
    list.addEventListener('change', function(){ selected = Array.from(list.querySelectorAll('input:checked')).map(function(i){ return i.value; }); sync(); onChange(); });
    search.addEventListener('input', function(){ var q = search.value.toLowerCase(); list.querySelectorAll('label').forEach(function(l){ l.classList.toggle('hide', q && l.dataset.v.toLowerCase().indexOf(q) < 0); }); });
    btn.addEventListener('click', function(e){ e.preventDefault(); pop.hidden = !pop.hidden; if (!pop.hidden) search.focus(); });
    el.querySelector('.msel-clear').addEventListener('click', function(){ selected = []; sync(); onChange(); });
    el.querySelector('.msel-close').addEventListener('click', function(){ pop.hidden = true; });
    document.addEventListener('click', function(e){ if (!el.contains(e.target)) pop.hidden = true; });
    sync();
    return { get: function(){ return selected.slice(); }, set: function(vals){ selected = (vals || []).filter(function(v){ return options.some(function(o){ return o.value === v; }); }); sync(); } };
  }
  function escA(t){ return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function listParam(q, name){ var v = q.get(name); return v ? v.split(',').map(function(x){ return x.trim(); }).filter(Boolean) : []; }

  // Maps page: one filter bar for every map; a density of origins, or the smokes themselves when few remain.
  var mapsBar = document.getElementById('maps-filters');
  if (mapsBar) {
    var wantedSlug = location.hash.indexOf('#smoke-') === 0 ? location.hash.slice(7) : '';
    var opts = window.MAPS_OPTS || {clans: [], ships: []};
    var mMap = document.getElementById('m-map'), mPlayer = document.getElementById('m-player'), mPurpose = document.getElementById('m-purpose'), mSpawn = document.getElementById('m-spawn'), mCls = document.getElementById('m-cls'), mType = document.getElementById('m-type');
    var lo = document.getElementById('m-lo'), hi = document.getElementById('m-hi'), mCount = document.getElementById('m-count');
    var DRAW_MAX = window.MAP_DRAW_MAX || 25, N = 768;
    var mClan = makeMulti(document.getElementById('m-clan'), opts.clans.map(function(c){ return {value: c[0], label: c[0], count: c[1]}; }), renderAll);
    var mShip = makeMulti(document.getElementById('m-ship'), opts.ships.map(function(c){ return {value: c[0], label: c[0], count: c[1]}; }), renderAll);
    var slugId = function(t){ return String(t).replace(/[^A-Za-z0-9_-]+/g, '_').replace(/^_+|_+$/g, '') || 'x'; };
    function view(){ var r = document.querySelector('input[name=m-view]:checked'); return r ? r.value : 'auto'; }
    function setView(v){ var r = document.querySelector('input[name=m-view][value="' + v + '"]'); if (r) r.checked = true; }
    function shown(r){
      var t = r.t;
      if (t >= 0 && (t < parseInt(lo.value,10) * 60 || t >= parseInt(hi.value,10) * 60 + (parseInt(hi.value,10) === 20 ? 1 : 0))) return false;
      var clans = mClan.get(), ships = mShip.get();
      if (clans.length && clans.indexOf(r.team) < 0) return false;
      if (ships.length && ships.indexOf(r.ship) < 0) return false;
      if (mPlayer.value && r.player !== mPlayer.value) return false;
      if (mPurpose.value && r.purposes.indexOf(mPurpose.value) < 0) return false;
      if (mSpawn.value && r.spawn !== mSpawn.value) return false;
      if (mCls.value && r.cls !== mCls.value) return false;
      if (mType.value && r.type !== mType.value) return false;
      return true;
    }
    function heatRects(rows){
      var cells = {}, peak = 0, step = N / 10;
      rows.forEach(function(r){ var p = r.pts[0]; var cx = Math.min(9, Math.max(0, Math.floor(p[0] / step))), cy = Math.min(9, Math.max(0, Math.floor(p[1] / step))); var k = cx + ',' + cy; cells[k] = (cells[k] || 0) + 1; if (cells[k] > peak) peak = cells[k]; });
      var letters = 'ABCDEFGHIJ';
      return Object.keys(cells).map(function(k){ var cx = parseInt(k.split(',')[0], 10), cy = parseInt(k.split(',')[1], 10), n = cells[k]; return '<rect x="' + (cx * step) + '" y="' + (cy * step) + '" width="' + step + '" height="' + step + '" fill="#F5C542" fill-opacity="' + (0.12 + 0.68 * n / peak).toFixed(2) + '"><title>' + letters[cy] + (cx + 1) + ': ' + n + ' smokes</title></rect>'; }).join('');
    }
    function smokeMarkup(r, markerPrefix){
      var pts = r.pts.map(function(p){ return p[0] + ',' + p[1]; }).join(' ');
      var color = (window.TEAM_COLORS||{})[r.team] || '#94A3B8';
      var cloud = r.r > 0 ? '<polyline class="cloud" points="' + pts + '" stroke="' + color + '" style="stroke-width:' + (2 * r.r).toFixed(1) + 'px"/>' : '';
      return '<a href="' + r.href + '" id="smoke-' + r.slug + '" class="smokepath" data-team="' + escA(r.team) + '">' + cloud + '<polyline points="' + pts + '" stroke="' + color + '"' + (r.dashed ? ' stroke-dasharray="6,4"' : '') + ' marker-end="url(#' + markerPrefix + '-arrow-' + slugId(r.team) + ')"/><title>' + escA(r.title) + '</title></a>';
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
    function donut(counts){
      var names = Object.keys(counts).sort(function(a,b){ return counts[b] - counts[a]; });
      var total = names.reduce(function(a,n){ return a + counts[n]; }, 0);
      if (!total) return '<span class="muted small">Nothing here, just clear skies.</span>';
      var size = 120, cx = 60, cy = 60, r = 58, angle = -Math.PI/2, svg = '', legend = '';
      names.forEach(function(n){
        var frac = counts[n]/total, a2 = angle + frac*2*Math.PI, color = (window.SHIP_COLORS||{})[n] || '#94A3B8';
        if (frac >= 0.999) svg += '<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="'+color+'"><title>'+n+': '+counts[n]+'</title></circle>';
        else svg += '<path d="M'+cx+','+cy+' L'+(cx+r*Math.cos(angle)).toFixed(1)+','+(cy+r*Math.sin(angle)).toFixed(1)+' A'+r+','+r+' 0 '+(frac>0.5?1:0)+',1 '+(cx+r*Math.cos(a2)).toFixed(1)+','+(cy+r*Math.sin(a2)).toFixed(1)+' Z" fill="'+color+'"><title>'+n+': '+counts[n]+' ('+Math.round(frac*100)+'%)</title></path>';
        legend += '<span class="legend"><i style="background:'+color+'"></i>'+n+' '+counts[n]+'</span>';
        angle = a2;
      });
      svg += '<circle cx="'+cx+'" cy="'+cy+'" r="'+(r*0.6)+'" fill="var(--panel)"/>';
      return '<svg viewBox="0 0 '+size+' '+size+'" width="'+size+'" height="'+size+'" class="donut">'+svg+'</svg><div class="legend-row">'+legend+'</div>';
    }
    var sections = Array.from(document.querySelectorAll('.map-section')).map(function(sec){
      var wrap = sec.querySelector('.mapwrap'), svg = wrap ? wrap.querySelector('svg') : null;
      var marker = svg ? svg.querySelector('marker') : null;
      return { el: sec, map: sec.dataset.map, url: sec.dataset.paths, rows: null, wrap: wrap, heat: svg ? svg.querySelector('g.heat') : null, paths: svg ? svg.querySelector('g.paths') : null,
        markerPrefix: marker ? marker.id.replace(/-arrow-.*$/, '') : 'm', chart: sec.querySelector('.chart'), count: sec.querySelector('.count'), ships: sec.querySelector('.ships') };
    });
    function renderSection(s){
      var hidden = !!(mMap.value && mMap.value !== s.map);
      s.el.hidden = hidden;
      if (hidden || !s.rows) return 0;
      var vis = s.rows.filter(shown);
      var v = view(), drawn = v === 'smokes' || (v === 'auto' && vis.length <= DRAW_MAX);
      if (s.wrap) s.wrap.classList.toggle('lines', drawn);
      if (drawn) { s.paths.innerHTML = vis.map(function(r){ return smokeMarkup(r, s.markerPrefix); }).join(''); s.heat.innerHTML = ''; }
      else { s.heat.innerHTML = heatRects(vis); s.paths.innerHTML = ''; }
      s.count.textContent = vis.length + ' smokes ' + (drawn ? 'drawn' : 'in the density') + (v === 'auto' && !drawn ? ' (narrow to ' + DRAW_MAX + ' or fewer to draw them)' : '');
      var teams = Array.from(new Set(s.rows.map(function(r){ return r.team; })));
      if (mClan.get().length) teams = teams.filter(function(t){ return mClan.get().indexOf(t) >= 0; });
      var counts0 = {}; vis.forEach(function(r){ counts0[r.team] = (counts0[r.team]||0) + 1; });
      teams.sort(function(a,b){ return (counts0[b]||0) - (counts0[a]||0) || a.localeCompare(b); });
      var others = [];
      if (!mClan.get().length && teams.length > 10) { others = teams.slice(10); teams = teams.slice(0, 10); }
      function rows(f){
        var out = teams.map(function(t){ var list = vis.filter(function(r){ return r.team === t; }); return {team:t, v:f(list), n:list.length, color:(window.TEAM_COLORS||{})[t]||'#94A3B8'}; });
        if (others.length) { var list = vis.filter(function(r){ return others.indexOf(r.team) >= 0; }); out.push({team:'others (' + others.length + ')', v:f(list), n:list.length, color:'#475569'}); }
        return out;
      }
      function avg(list, key){ var xs = list.map(function(r){ return r[key]; }).filter(function(x){ return x !== null && x !== undefined; }).map(Number); return xs.length ? xs.reduce(function(a,b){return a+b;},0)/xs.length : null; }
      s.chart.innerHTML =
        panel('Smokes', rows(function(l){ return l.length ? l.length : null; }), '', false) +
        panel('Average smoke damage', rows(function(l){ return avg(l, 'dmg'); }), '', false) +
        panel('<abbr class="term" title="' + (window.CONTEST_DEF||'') + '">Average distance to the nearest contested cap</abbr> (negative = inside)', rows(function(l){ return avg(l, 'contested'); }), 'km', false) +
        panel('<abbr class="term" title="' + (window.SELFISH_DEF||'') + '">Selfish smoke</abbr> share', rows(function(l){ var v = avg(l, 'selfish'); return v === null ? null : v * 100; }), '', true);
      if (s.ships) { var counts = {}; vis.forEach(function(r){ counts[r.ship] = (counts[r.ship]||0) + 1; }); s.ships.innerHTML = donut(counts); }
      return vis.length;
    }
    function writeUrl(){
      var q = new URLSearchParams();
      if (mMap.value) q.set('map', mMap.value);
      if (mClan.get().length) q.set('clan', mClan.get().join(','));
      if (mShip.get().length) q.set('ship', mShip.get().join(','));
      if (mPlayer.value) q.set('player', mPlayer.value);
      if (mPurpose.value) q.set('purpose', mPurpose.value);
      if (mSpawn.value) q.set('spawn', mSpawn.value);
      if (mCls.value) q.set('cls', mCls.value);
      if (mType.value) q.set('type', mType.value);
      if (lo.value !== '0' || hi.value !== '20') q.set('t', lo.value + '-' + hi.value);
      if (view() !== 'auto') q.set('view', view());
      var s = q.toString().replace(/%2C/g, ',');
      history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + (wantedSlug ? '#smoke-' + wantedSlug : ''));
    }
    function renderAll(){
      document.querySelector('#maps-filters .lo').textContent = clockText(parseInt(lo.value,10) * 60);
      document.querySelector('#maps-filters .hi').textContent = clockText(parseInt(hi.value,10) * 60);
      var total = 0, all = 0;
      sections.forEach(function(s){ total += renderSection(s); if (!s.el.hidden && s.rows) all += s.rows.length; });
      mCount.textContent = total + ' of ' + all + ' smokes';
      writeUrl();
    }
    function clamp(){ if (parseInt(lo.value,10) > parseInt(hi.value,10)) { if (document.activeElement === lo) hi.value = lo.value; else lo.value = hi.value; } }
    [lo, hi].forEach(function(r){ r.addEventListener('input', function(){ clamp(); renderAll(); }); });
    [mMap, mPlayer, mPurpose, mSpawn, mCls, mType].forEach(function(s){ s.addEventListener('change', renderAll); });
    document.querySelectorAll('input[name=m-view]').forEach(function(r){ r.addEventListener('change', renderAll); });
    // Filters from the address bar: ?map=...&clan=A,B&ship=X,Y&player=...&purpose=...&spawn=...&cls=...&type=...&t=0-4&view=smokes (older links: from/to in seconds).
    var q = new URLSearchParams(location.search);
    if (q.get('map')) mMap.value = q.get('map');
    mClan.set(listParam(q, 'clan'));
    mShip.set(listParam(q, 'ship'));
    if (q.get('player')) mPlayer.value = q.get('player');
    if (q.get('purpose')) mPurpose.value = q.get('purpose');
    if (q.get('spawn')) mSpawn.value = q.get('spawn');
    if (q.get('cls')) mCls.value = q.get('cls');
    if (q.get('type')) mType.value = q.get('type');
    if (q.get('t') && /^\d+-\d+$/.test(q.get('t'))) { lo.value = q.get('t').split('-')[0]; hi.value = q.get('t').split('-')[1]; }
    if (q.get('from')) lo.value = Math.floor(parseInt(q.get('from'),10) / 60);
    if (q.get('to')) hi.value = Math.ceil(parseInt(q.get('to'),10) / 60);
    if (q.get('view')) setView(q.get('view'));
    // A smoke page's "its path on the map" link: that smoke's map and clan, drawn, and scrolled to.
    var target = wantedSlug && (window.SMOKE_MAP||{})[wantedSlug];
    if (target) { mMap.value = target[0]; mClan.set([target[1]]); setView('smokes'); }
    clamp();
    Promise.all(sections.map(function(s){ return fetch(s.url).then(function(r){ return r.json(); }).then(function(rows){ s.rows = rows; }).catch(function(){ s.rows = []; s.count.textContent = 'paths could not be loaded'; }); })).then(function(){
      renderAll();
      if (target) { var el = document.getElementById('smoke-' + wantedSlug); if (el) { el.querySelectorAll('polyline:not(.cloud)').forEach(function(p){ p.style.strokeWidth = '7px'; }); el.scrollIntoView({block: 'center'}); } }
    });
  }

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

  if (!window.SMOKES_URL) return;
  var rows = [], tbody = document.querySelector('#smokes tbody'), PAGE = 100, limit = PAGE;
  var more = document.getElementById('showmore');
  var multi = {};
  more.addEventListener('click', function(){ limit += PAGE; render(); });
  fetch(window.SMOKES_URL).then(function(r){ return r.json(); }).then(function(data){ rows = data; start(); }).catch(function(){ document.getElementById('count').textContent = 'the smoke table could not be loaded'; });
  function start(){
  function fill(id, key){ var sel = document.getElementById(id); var vals = Array.from(new Set(rows.map(function(r){return r[key];}))).filter(Boolean).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', function(){ limit = PAGE; render(); }); }
  function fillMulti(id, key){ var counts = {}; rows.forEach(function(r){ if (r[key]) counts[r[key]] = (counts[r[key]]||0) + 1; }); var vals = Object.keys(counts).sort(); multi[key] = makeMulti(document.getElementById(id), vals.map(function(v){ return {value: v, label: v, count: counts[v]}; }), function(){ limit = PAGE; render(); }); }
  fillMulti('f-team','team'); fill('f-player','player'); fillMulti('f-ship','ship'); fill('f-map','map'); fill('f-game','game'); fill('f-type','type'); fill('f-phase','phase');
  fill('f-cls','cls'); fill('f-movement','movement'); fill('f-coverage','coverage'); fill('f-primary','primary'); fill('f-zone','zone'); fill('f-lane','lane');
  (function(){ var sel = document.getElementById('f-purpose'); var vals = Array.from(new Set(rows.flatMap(function(r){ return r.purposes; }))).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', function(){ limit = PAGE; render(); }); })();
  document.getElementById('f-sort').addEventListener('change', function(){ limit = PAGE; render(); });
  // Filters from the address bar: ?clan=A,B&ship=X,Y plus any single select by its name (player, map, game, type, cls, ...); 'team' is the older name of 'clan'.
  var q = new URLSearchParams(location.search);
  multi.team.set(listParam(q, 'clan').concat(listParam(q, 'team')));
  multi.ship.set(listParam(q, 'ship'));
  SINGLE.forEach(function(k){ if (q.get(k)) document.getElementById('f-' + k).value = q.get(k); });
  if (q.get('purpose')) document.getElementById('f-purpose').value = q.get('purpose');
  if (q.get('sort')) document.getElementById('f-sort').value = q.get('sort');
  render();
  }
  var SINGLE = ['player','map','game','type','phase','cls','movement','coverage','primary','zone','lane'];
  function val(id){ return document.getElementById(id).value; }
  function bar(v, max, color){ var w = max ? Math.max(0, Math.min(1, v/max))*80 : 0; return '<span class="mini"><i style="width:'+w.toFixed(0)+'px;background:'+color+'"></i></span>'; }
  function writeUrl(f, purpose, sort){
    var q = new URLSearchParams();
    if (multi.team.get().length) q.set('clan', multi.team.get().join(','));
    if (multi.ship.get().length) q.set('ship', multi.ship.get().join(','));
    SINGLE.forEach(function(k){ if (f[k]) q.set(k, f[k]); });
    if (purpose) q.set('purpose', purpose);
    if (sort !== 'total') q.set('sort', sort);
    var s = q.toString().replace(/%2C/g, ',');
    history.replaceState(null, '', location.pathname + (s ? '?' + s : ''));
  }
  function render(){
    var f = {};
    SINGLE.forEach(function(k){ f[k] = val('f-' + k); });
    var clans = multi.team.get(), ships = multi.ship.get();
    var purpose = val('f-purpose');
    var sort = val('f-sort'), asc = sort==='contested' || sort==='elapsed';
    var list = rows.filter(function(r){ return Object.keys(f).every(function(k){ return !f[k] || r[k]===f[k]; }) && (!clans.length || clans.indexOf(r.team) >= 0) && (!ships.length || ships.indexOf(r.ship) >= 0) && (!purpose || r.purposes.indexOf(purpose) >= 0); });
    list.sort(function(a,b){ var x=a[sort], y=b[sort]; if (x==null) x = asc? Infinity : -Infinity; if (y==null) y = asc? Infinity : -Infinity; return asc ? x-y : y-x; });
    var shownRows = list.slice(0, limit);
    more.hidden = list.length <= limit;
    more.textContent = 'Show ' + Math.min(PAGE, list.length - limit) + ' more (' + shownRows.length + ' of ' + list.length + ' shown)';
    tbody.innerHTML = shownRows.map(function(r){
      var con = r.contested==null ? '-' : (r.contested<0 ? Math.round(r.depth)+'% into '+r.contested_name : (r.contested/1000).toFixed(1)+' km to '+r.contested_name);
      var outcome = r.won ? 'near capture of '+r.won : (r.defended ? 'defended '+r.defended : '-');
      var marks = (r.one_sided ? ' <span class="pill warn-pill" title="one replay for this game: inferred smoke, no damage counted">one-sided</span>' : '') + (r.quality ? ' <span class="pill warn-pill" title="' + r.quality.replace(/"/g, '&quot;') + '">drift</span>' : '');
      var thumb = r.thumb ? '<img class="thumb" loading="lazy" width="84" height="84" src="' + r.thumb + '" alt="">' : '';
      return '<tr data-href="'+r.href+'"><td>'+thumb+'</td>'+
        '<td><span class="tag" style="--c:'+r.color+'">'+r.team+'</span></td><td>'+r.player+marks+'</td><td>'+r.ship+'</td><td>'+r.map+'</td>'+
        '<td class="small" title="'+r.game.replace(/"/g,'&quot;')+'">'+r.game_short+'</td><td>'+(r.elapsed!=null?clockText(r.elapsed):'?')+'</td>'+
        '<td class="small tagcell" title="'+r.tags_text.replace(/"/g,'&quot;')+'"><span class="pill cls">'+r.cls_short+'</span> <span class="pill">'+r.movement+'</span> <span class="pill">'+r.coverage+'</span><br>'+(r.primary==='none'?'<span class="muted">no tactic</span>':'<b>'+r.primary+'</b>')+(r.purposes.length>1?' <span class="muted">+'+(r.purposes.length-1)+'</span>':'')+'</td>'+
        '<td class="small">'+(r.zone||'-')+'<br><span class="muted">'+(r.lane?r.lane+' lane':'')+'</span></td>'+
        '<td>'+r.total.toLocaleString()+' '+bar(r.total, window.MAX_TOTAL, '#F5C542')+'<br><span class="muted small">'+r.concealed.toLocaleString()+' / '+r.detected.toLocaleString()+'</span></td>'+
        '<td>'+r.dd.toLocaleString()+'</td>'+
        '<td>'+con+'</td><td>'+outcome+'</td><td>'+r.radar+'</td><td>'+r.offensive+'</td><td>'+r.kills+'</td><td>'+r.deaths+'</td><td>'+(r.selfish?'yes':'no')+'</td></tr>';
    }).join('');
    Array.from(tbody.querySelectorAll('tr[data-href]')).forEach(function(tr){ tr.addEventListener('click', function(){ location.href = tr.dataset.href; }); });
    document.getElementById('empty').hidden = list.length>0;
    document.getElementById('count').textContent = list.length + ' of ' + rows.length + ' smokes';
    writeUrl(f, purpose, sort);
  }
})();"""



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--maps", required=True)
    ap.add_argument("--clips")
    ap.add_argument("--inventory", default="smoke/inventory.csv")
    ap.add_argument("--out", default="smoke-site")
    ap.add_argument("--colors", default="", help="tag:#hex,... overrides for one build")
    ap.add_argument("--clans", default="smoke/clans.csv", help="clan registry: tag, name, group, color, note")
    ap.add_argument("--hub-layout", default="cards", choices=["cards", "hero", "tournament"])
    ap.add_argument("--mockups", default="smoke/mockups", help="hub templates")
    args = ap.parse_args()
    data = Data(args.batch, args.maps, args.clips, args.inventory, args.clans)
    site = Site(data, os.path.join(args.out, "smoke"), parse_colors(args.colors), args.hub_layout)
    site.build()
    site.hub(args.out, args.mockups)
    total = 0
    largest = (0, "")
    for dp, _, fs in os.walk(args.out):
        for f in fs:
            size = os.path.getsize(os.path.join(dp, f))
            total += size
            largest = max(largest, (size, os.path.join(dp, f)))
    print(f"site written to {args.out}: {len(data.smokes)} smokes, {len(data.by_game)} games, {total / 1e6:.0f} MB, largest file {largest[0] / 1e6:.1f} MB ({largest[1]})")
    for lens, awards in site.awards_by_lens.items():
        for title, s in awards["smokes"].items():
            print(f"award [{lens}] {title}: {s['player'] + ' ' + s['ship'] + ' id ' + str(s['smoke_id']) + ' match ' + s['_match'] + ' g' + str(s['game_no']) + ' team ' + s['team'] + (' clip' if s.get('_clip') else ' NO CLIP') if s else 'none'}")
        for title, (name, _) in awards["players"].items():
            print(f"award [{lens}] {title}: {name}")


if __name__ == "__main__":
    main()
