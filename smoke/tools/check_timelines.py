"""Checks on a batch that carries the timeline files (smoke-signals 0.4.0).

python -I -X utf8 check_timelines.py <new batch dir> <old batch dir> [--inventory smoke/inventory.csv]

a. Nothing moved: smokes.csv, smokes.json, every run's game.json, smokes.json,
   damage_events.csv and damage_spike.json against the old batch. Expected
   differences only: version, code revision, timestamp, max_health.
b. Completeness: a timelines folder per played game, a ribbons.csv per run,
   the one-sided flag of single-replay games.
c. Cross-check at every smoke's activation: cap owner, score and smoker
   health from the timelines against the values stored with the smoke.
d. Radar and hydro: lit spans attributed, ambiguous and unattributed, overall
   and per map.
Prints a Markdown report.
"""
import argparse
import bisect
import csv
import json
import os
from collections import Counter, defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("new")
ap.add_argument("old")
ap.add_argument("--inventory", default="smoke/inventory.csv")
args = ap.parse_args()
NEW, OLD = args.new, args.old
PROVENANCE = {"wows_toolkit_rev", "smoke_signals_version", "generated_at"}


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def strip(o):
    """Drop provenance keys and max_health everywhere in a JSON value."""
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in PROVENANCE and k != "max_health"}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def diff_paths(a, b, path="", out=None, limit=20):
    """Paths at which two JSON values differ."""
    out = [] if out is None else out
    if len(out) >= limit:
        return out
    if type(a) is not type(b):
        out.append(path)
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}.{k}")
            else:
                diff_paths(a[k], b[k], f"{path}.{k}", out, limit)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append(f"{path}[len {len(a)} vs {len(b)}]")
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                diff_paths(x, y, f"{path}[{i}]", out, limit)
    elif a != b:
        out.append(path)
    return out


print("# Timeline batch checks\n")
print(f"- new batch: `{NEW}`\n- old batch: `{OLD}`\n")

# ---------------------------------------------------------------- a
print("## a. Nothing moved\n")
key = lambda r: (r["match_id"], r["game_no"], r["team"], r["smoke_id"])
old_rows = {key(r): r for r in read_csv(os.path.join(OLD, "smokes.csv"))}
new_rows = read_csv(os.path.join(NEW, "smokes.csv"))
new_keys = {key(r) for r in new_rows}
col_diff = Counter()
examples = {}
for r in new_rows:
    o = old_rows.get(key(r))
    if o is None:
        continue
    for k in set(r) | set(o):
        if k in PROVENANCE:
            continue
        if r.get(k) != o.get(k):
            col_diff[k] += 1
            examples.setdefault(k, (key(r), o.get(k), r.get(k)))
prov = {k: Counter(r[k] for r in new_rows).most_common(2) for k in ("wows_toolkit_rev", "smoke_signals_version")}
print(f"- smokes.csv: {len(new_rows)} rows new, {len(old_rows)} old; only in new {len(new_keys - set(old_rows))}, only in old {len(set(old_rows) - new_keys)}; "
      f"columns new {len(new_rows[0])}, old {len(next(iter(old_rows.values())))}; same column order: "
      f"{list(new_rows[0]) == list(next(iter(old_rows.values())))}")
print(f"- smokes.csv fields that differ outside version, revision and timestamp: {dict(col_diff) if col_diff else 'none'}")
for k, (kk, a, b) in examples.items():
    print(f"  - `{k}` e.g. {kk}: old `{a}` new `{b}`")
print(f"- provenance in the new batch: {prov}")

old_json = {(s["match_id"], s["game_no"], s["team"], s["smoke_id"]): s for s in read_json(os.path.join(OLD, "smokes.json"))}
new_json = read_json(os.path.join(NEW, "smokes.json"))
jd = Counter()
for s in new_json:
    o = old_json.get((s["match_id"], s["game_no"], s["team"], s["smoke_id"]))
    if o is None:
        jd["<missing in old>"] += 1
        continue
    for p in diff_paths(strip(s), strip(o)):
        jd[p.split("[")[0]] += 1
print(f"- smokes.json (batch): {len(new_json)} records new, {len(old_json)} old; differing paths outside the expected keys: {dict(jd) if jd else 'none'}")

runs_new = sorted(d for d in os.listdir(os.path.join(NEW, "games")) if os.path.isdir(os.path.join(NEW, "games", d)))
runs_old = sorted(d for d in os.listdir(os.path.join(OLD, "games")) if os.path.isdir(os.path.join(OLD, "games", d)))
print(f"- run folders: {len(runs_new)} new, {len(runs_old)} old; same names: {runs_new == runs_old}")
file_diff = Counter()
detail = defaultdict(list)
max_health_seen = Counter()
for run in runs_new:
    if run not in runs_old:
        continue
    for name in ("game.json", "smokes.json", "damage_spike.json"):
        a, b = read_json(os.path.join(NEW, "games", run, name)), read_json(os.path.join(OLD, "games", run, name))
        if name == "game.json":
            for t in a["teams"]:
                for p in t["players"]:
                    max_health_seen["set" if p.get("max_health") else "missing"] += 1
        d = diff_paths(strip(a), strip(b))
        if d:
            file_diff[name] += 1
            if len(detail[name]) < 5:
                detail[name].append((run, d[:4]))
    for name in ("damage_events.csv", "smokes.csv"):
        with open(os.path.join(NEW, "games", run, name), "rb") as f:
            a = f.read()
        with open(os.path.join(OLD, "games", run, name), "rb") as f:
            b = f.read()
        if name == "smokes.csv":
            ra, rb = read_csv(os.path.join(NEW, "games", run, name)), read_csv(os.path.join(OLD, "games", run, name))
            same = len(ra) == len(rb) and all(all(x[k] == y[k] for k in x if k not in PROVENANCE) for x, y in zip(ra, rb))
        else:
            same = a == b
        if not same:
            file_diff[name] += 1
            if len(detail[name]) < 5:
                detail[name].append((run, "content"))
print(f"- per-run files differing outside the expected keys (of {len(runs_new)} runs): "
      f"{ {n: file_diff.get(n, 0) for n in ('game.json', 'smokes.json', 'smokes.csv', 'damage_events.csv', 'damage_spike.json')} }")
for name, rows in detail.items():
    for run, d in rows:
        print(f"  - {name} {run}: {d}")
print(f"- max_health on players in game.json: {dict(max_health_seen)}")

# ---------------------------------------------------------------- b
print("\n## b. Completeness\n")
inv = [r for r in read_csv(args.inventory) if r["status"] == "played" and r["replay_folder"]]
game_folders = sorted({os.path.basename(r["replay_folder"]) for r in inv})
tl_root = os.path.join(NEW, "timelines")
tl_dirs = sorted(os.listdir(tl_root)) if os.path.isdir(tl_root) else []
FILES = ["meta.json", "caps_timeline.csv", "radar.csv", "score.csv"]
incomplete = [d for d in tl_dirs if any(not os.path.exists(os.path.join(tl_root, d, f)) for f in FILES)]
print(f"- played games in the inventory: {len(game_folders)}; timelines folders: {len(tl_dirs)}; "
      f"missing: {sorted(set(game_folders) - set(tl_dirs)) or 'none'}; extra: {sorted(set(tl_dirs) - set(game_folders)) or 'none'}; "
      f"folders lacking a file: {incomplete or 'none'}")
smokes_per_game = Counter((r["match_id"], r["game_no"]) for r in new_rows)
metas = {d: read_json(os.path.join(tl_root, d, "meta.json")) for d in tl_dirs}
no_smokes = [d for d, m in metas.items() if smokes_per_game.get((m["match_id"], str(m["game_no"])), 0) == 0]
print(f"- games with no kept smoke: {len(no_smokes)} ({', '.join(no_smokes) or 'none'}); each has its timelines folder: {all(d in tl_dirs for d in no_smokes)}")
rib = [r for r in runs_new if os.path.exists(os.path.join(NEW, "games", r, "ribbons.csv"))]
trk = [r for r in runs_new if os.path.exists(os.path.join(NEW, "games", r, "tracks.csv"))]
ships_seen = defaultdict(Counter)
own_flag = Counter()
for r in trk:
    g = read_json(os.path.join(NEW, "games", r, "game.json"))
    seen = {}
    with open(os.path.join(NEW, "games", r, "tracks.csv"), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            seen[row["entity_id"]] = row["own_replay"]
    for e, own in seen.items():
        ships_seen[(g["match_id"], g["game_no"])][e] += 1
        own_flag[own] += 1
roster = Counter()
for c in ships_seen.values():
    for k in c.values():
        roster["ship in one run" if k == 1 else f"ship in {k} runs"] += 1
print(f"- tracks.csv files: {len(trk)} of {len(runs_new)} runs; ships across the runs of a game: {dict(roster)}; own_replay values per ship: {dict(own_flag)}")
rib_rows = {r: read_csv(os.path.join(NEW, "games", r, "ribbons.csv")) for r in rib}
kinds = Counter(x["ribbon"] for rows in rib_rows.values() for x in rows for _ in range(int(x["count"])))
print(f"- ribbons.csv files: {len(rib)} of {len(runs_new)} runs; runs with at least one cap ribbon: {sum(1 for v in rib_rows.values() if v)}; "
      f"ribbons by kind: {dict(kinds)}")
recorders = Counter()
for d, m in metas.items():
    recorders[m["recorder_entity_id"] is not None] += 1
one_sided = sorted(d for d, m in metas.items() if m["one_sided"])
single_inv = sorted(os.path.basename(r["replay_folder"]) for r in inv if len([x for x in r["replay_files"].split(";") if x]) < 2)
flag_rows = Counter(r["one_sided"] for r in new_rows)
print(f"- single-replay games in the inventory: {single_inv}; meta.json one_sided true: {one_sided}; agree: {single_inv == one_sided}")
print(f"- smokes.csv one_sided column: {dict(flag_rows)}; recorder known in meta.json: {dict(recorders)}")
writer = Counter()
for d, m in metas.items():
    runs = [r for r in runs_new if r.startswith(d + "_")]
    first = runs[0] if runs else None
    g = read_json(os.path.join(NEW, "games", first, "game.json")) if first else None
    writer["first run in name order" if g and g["primary_replay"] == m["clock_replay"] else "another run"] += 1
print(f"- which run wrote the game files: {dict(writer)}")

# ---------------------------------------------------------------- c
print("\n## c. Cross-check at each smoke's activation\n")
run_start = {}
run_of_game = defaultdict(list)
for run in runs_new:
    g = read_json(os.path.join(NEW, "games", run, "game.json"))
    run_start[(g["match_id"], g["game_no"], g["primary_replay"])] = g["battle_start_s"]
dir_of_game = {(m["match_id"], m["game_no"]): d for d, m in metas.items()}


class Game:
    def __init__(self, d):
        base = os.path.join(tl_root, d)
        self.caps = defaultdict(list)
        for r in read_csv(os.path.join(base, "caps_timeline.csv")):
            self.caps[r["cap"]].append((float(r["elapsed_s"]), r["owner"]))
        self.score = defaultdict(list)
        for r in read_csv(os.path.join(base, "score.csv")):
            self.score[r["team"]].append((float(r["elapsed_s"]), int(r["score"])))


def at(series, t, slack=0.0):
    i = bisect.bisect_right([x[0] for x in series], t + slack) - 1
    return series[i] if i >= 0 else None


def after(series, t):
    i = bisect.bisect_right([x[0] for x in series], t)
    return series[i] if i < len(series) else None


run_dir = {}
for run in runs_new:
    g = read_json(os.path.join(NEW, "games", run, "game.json"))
    run_dir[(g["match_id"], g["game_no"], g["primary_replay"])] = run
health_cache = {}


def run_health(run):
    """Health series per ship from the run's own tracks.csv."""
    if run not in health_cache:
        h = defaultdict(list)
        for r in read_csv(os.path.join(NEW, "games", run, "tracks.csv")):
            if r["health"]:
                h[int(r["entity_id"])].append((float(r["elapsed_s"]), float(r["health"]), float(r["max_health"])))
        health_cache[run] = h
    return health_cache[run]


cache = {}
cap = Counter(); cap_bad = Counter(); sc = Counter(); hp = Counter(); hp_gap = []
n = 0
for s in new_json:
    gk = (s["match_id"], s["game_no"])
    st = s.get("state_at_activate")
    d = dir_of_game.get(gk)
    start = run_start.get((s["match_id"], s["game_no"], s["primary_replay"]))
    if not st or d is None or start is None:
        cap["no state stored" if not st else "no timeline"] += 1
        continue
    if d not in cache:
        cache[d] = Game(d)
    g = cache[d]
    t_act = (s.get("t_activate") or s["t_created"])["seconds"] - start
    n += 1
    # cap owner
    for c in st["cap_state"]:
        hit = at(g.caps[c["cap"]], t_act)
        owner = (hit[1] or None) if hit else None
        if owner == c["owner"]:
            cap["match"] += 1
        else:
            near = [e for e in g.caps[c["cap"]] if abs(e[0] - t_act) <= 2.5]
            cls = "owner changed within 2.5 s of the activation" if any((e[1] or None) == c["owner"] for e in near) or near else "other"
            cap[cls] += 1
            if cls == "other" and len(cap_bad) < 8:
                cap_bad[(s["match_id"], s["game_no"], s["smoke_id"], c["cap"], c["owner"], owner, round(t_act, 1))] += 1
    # score
    for team, stored in ((s["team"], st["score_ours"]), (s["opponent"], st["score_theirs"])):
        series = g.score.get(team)
        if stored is None or not series:
            sc["no value"] += 1
            continue
        a, b = at(series, t_act), after(series, t_act)
        if a and a[1] == stored:
            sc["match (last sample at or before)"] += 1
        elif b and b[1] == stored:
            sc["match (next sample, score ticked inside the 2 s step)"] += 1
        elif a and b and min(a[1], b[1]) <= stored <= max(a[1], b[1]):
            sc["between the two neighbouring samples"] += 1
        else:
            sc["other"] += 1
    # smoker health
    smoker = next((x["entity_id"] for x in s["smokees"] if x.get("role") == "smoker"), None)
    stored = st.get("smoker_hp_pct")
    series = run_health(run_dir[(s["match_id"], s["game_no"], s["primary_replay"])]).get(smoker)
    if stored is None or smoker is None or not series:
        hp["no value"] += 1
        continue
    a, b = at(series, t_act), after(series, t_act)
    pa = a[1] / a[2] * 100 if a else None
    pb = b[1] / b[2] * 100 if b else None
    if pa is not None and abs(pa - stored) <= 0.5:
        hp["match within 0.5 points (last sample at or before)"] += 1
    elif pb is not None and abs(pb - stored) <= 0.5:
        hp["match within 0.5 points (next sample, health moved inside the 2 s step)"] += 1
    elif pa is not None and pb is not None and min(pa, pb) - 0.5 <= stored <= max(pa, pb) + 0.5:
        hp["between the two neighbouring samples"] += 1
    else:
        hp["other"] += 1
        hp_gap.append((s["match_id"], s["game_no"], s["smoke_id"], round(stored, 1), None if pa is None else round(pa, 1), None if pb is None else round(pb, 1)))


def table(title, c):
    tot = sum(c.values())
    print(f"**{title}** ({tot:,} comparisons)\n")
    print("| result | n | share |\n|---|---|---|")
    for k, v in c.most_common():
        print(f"| {k} | {v:,} | {100 * v / tot:.2f}% |")
    print()


print(f"Smokes checked: {n:,} of {len(new_json):,}.\n")
table("Cap owner, every cap at every smoke", cap)
for k in cap_bad:
    print(f"  - other: {k}")
table("Score, both teams at every smoke", sc)
table("Smoker health as a share of max health", hp)
for k in hp_gap[:8]:
    print(f"  - other: {k}")

# ---------------------------------------------------------------- d
print("\n## d. Radar and hydro\n")
game_map = {}
for run in runs_new:
    g = read_json(os.path.join(NEW, "games", run, "game.json"))
    game_map[(g["match_id"], g["game_no"])] = g["map_display"]
stats = defaultdict(Counter)
for d, m in metas.items():
    mp = game_map.get((m["match_id"], m["game_no"]), "?")
    for r in read_csv(os.path.join(tl_root, d, "radar.csv")):
        for scope in (mp, "All maps"):
            c = stats[(r["kind"], scope)]
            if r["row"] == "activation":
                c["activations"] += 1
                c["activation from inside a smoke"] += bool(r["source_in_smoke"])
            elif r["row"] == "lit":
                c["lit rows"] += 1
                c["ambiguous"] += r["ambiguous"] == "true"
                c["target in a smoke"] += bool(r["target_in_smoke"])
            else:
                c["unattributed spans"] += 1
                c["unattributed, target in a smoke"] += bool(r["target_in_smoke"])
for kind in ("radar", "hydro"):
    print(f"**{kind}**\n")
    print("| map | activations | from inside a smoke | lit rows (attributed) | of which ambiguous | target in a smoke | unattributed spans | share unattributed |")
    print("|---|---|---|---|---|---|---|---|")
    for scope in sorted({k[1] for k in stats if k[0] == kind}, key=lambda x: (x == "All maps", x)):
        c = stats[(kind, scope)]
        tot = c["lit rows"] + c["unattributed spans"]
        print(f"| {scope} | {c['activations']:,} | {c['activation from inside a smoke']:,} | {c['lit rows']:,} | {c['ambiguous']:,} | {c['target in a smoke']:,} | "
              f"{c['unattributed spans']:,} | {100 * c['unattributed spans'] / tot if tot else 0:.1f}% |")
    print()

size = 0
for root, _, files in os.walk(tl_root):
    size += sum(os.path.getsize(os.path.join(root, f)) for f in files)
rsize = sum(os.path.getsize(os.path.join(NEW, "games", r, "ribbons.csv")) for r in rib)
tsize = sum(os.path.getsize(os.path.join(NEW, "games", r, "tracks.csv")) for r in trk)
print(f"\n## Size\n\n- timelines/: {size / 1e6:.1f} MB in {len(tl_dirs)} folders; tracks.csv files: {tsize / 1e6:.1f} MB; ribbons.csv files: {rsize / 1e3:.0f} KB")
