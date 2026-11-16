"""Standing sanity checks on a batch output.

python -I -X utf8 sanity.py <repo root> <batch dir> [--reference <batch dir>] [--teams H-SR,RESIN,PN]

Checks:
1. Ledger reconciliation: every run's shell-plus-fire ledger against the
   game's own result, with the perspective clock offsets; runs outside
   2 percent are listed.
2. Reference diff: rows of the named teams compared column by column with
   the reference batch (default: the round 6 batch).
3. Dedupe: smokes seen by both runs of a game are counted once.
4. Smokes found against roster activations per team-game.
5. Per-clan summary with outlier flags.
6. Runtime and failures from the run log.
"""
import argparse
import csv
import json
import os
import re
from collections import Counter, defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("root")
ap.add_argument("batch")
ap.add_argument("--reference", default="output/20261104-180332")
ap.add_argument("--teams", default="H-SR,RESIN,PN")
ap.add_argument("--tolerance", type=float, default=0.02)
args = ap.parse_args()

ROOT, NEW = args.root, args.batch
R6 = args.reference if os.path.isabs(args.reference) else os.path.join(ROOT, args.reference)
ORIG = {t.strip() for t in args.teams.split(",") if t.strip()}
VOLATILE = {"generated_at", "wows_toolkit_rev", "smoke_signals_version", "run"}
GAMES = os.path.join(NEW, "games")


def fl(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


def load_smokes(d):
    return list(csv.DictReader(open(os.path.join(d, "smokes.csv"), encoding="utf-8")))


def key(r):
    return (r["match_id"], r["game_no"], r["team"], r["smoke_id"])


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


inv = list(csv.DictReader(open(os.path.join(ROOT, "smoke", "inventory.csv"), encoding="utf-8")))
played = [r for r in inv if r["status"] == "played"]
games_of = Counter()
for r in played:
    for t in r["teams"].split(" vs "):
        games_of[t] += 1

new = load_smokes(NEW)
runs = {}
for name in sorted(os.listdir(GAMES)):
    d = os.path.join(GAMES, name)
    if os.path.exists(os.path.join(d, "game.json")) and os.path.exists(os.path.join(d, "damage_spike.json")):
        runs[name] = (json.load(open(os.path.join(d, "game.json"), encoding="utf-8")), json.load(open(os.path.join(d, "damage_spike.json"), encoding="utf-8")))

print("# 1. Ledger reconciliation (shell plus fire, ledger over the game's own result)")
ratios = []
outside = []
offsets_untrusted = []
for name, (g, spike) in runs.items():
    r = spike.get("reconciliation_ratio_shell_fire")
    if r is None:
        outside.append((name, None, "no game result in the replay"))
        continue
    ratios.append(r)
    offs = spike.get("perspective_offsets") or []
    for o in offs:
        if not o.get("trusted"):
            offsets_untrusted.append((name, o))
    if abs(r - 1.0) > args.tolerance:
        outside.append((name, r, "; ".join(f"offset {o['offset_s']:+.2f} s ({o['pairs_in_bin']}/{o['pairs']} pairs{'' if o['trusted'] else ', fallback'})" for o in offs)))
bands = [(0, 0.9), (0.9, 0.98), (0.98, 1.02), (1.02, 1.1), (1.1, 1.25), (1.25, 1.6), (1.6, 9)]
print(f"runs: {len(runs)}; with a game result: {len(ratios)}")
print("ratio bands: " + ", ".join(f"{lo}-{hi}: {sum(1 for r in ratios if lo <= r < hi)}" for lo, hi in bands))
print(f"median ratio {sorted(ratios)[len(ratios) // 2]:.3f}; mean {sum(ratios) / len(ratios):.3f}" if ratios else "no ratios")
print(f"runs outside {args.tolerance:.0%}: {len(outside)} (over: {sum(1 for _, r, _ in outside if r and r > 1)}, under: {sum(1 for _, r, _ in outside if r and r < 1)})")
print(f"merged replays whose offset estimate fell back to offset zero: {len(offsets_untrusted)}")
for name, o in offsets_untrusted:
    print(f"  {name}: {o}")
print("\n| run | ratio | perspective offsets |")
print("|---|---|---|")
for name, r, note in sorted(outside, key=lambda x: -(x[1] or 0)):
    print(f"| {name.replace('kots19na_', '')} | {r if r is None else f'{r:.3f}'} | {note} |")

print()
print(f"# 2. Reference diff: {sorted(ORIG)} vs {R6}")
if os.path.exists(os.path.join(R6, "smokes.csv")):
    old = load_smokes(R6)
    oldk = {key(r): r for r in old if r["team"] in ORIG}
    newk = {key(r): r for r in new if r["team"] in ORIG}
    print(f"reference rows: {len(oldk)}; rows for the same teams now: {len(newk)}; rows in total now: {len(new)}")
    missing = [k for k in oldk if k not in newk]
    added = [k for k in newk if k not in oldk]
    print("rows in the reference but not now:", len(missing))
    for k in missing:
        print("  ", k, oldk[k]["player"], oldk[k]["ship"])
    print("rows now that the reference did not have:", len(added))
    for k in added:
        print("  ", k, newk[k]["player"], newk[k]["ship"], "owner_flag=" + newk[k].get("owner_flag", ""))
    cols_old = list(old[0].keys()) if old else []
    cols_new = list(new[0].keys()) if new else []
    print("columns: reference", len(cols_old), "now", len(cols_new), "; new columns:", [c for c in cols_new if c not in cols_old], "; dropped:", [c for c in cols_old if c not in cols_new])
    diffcols = Counter()
    diffrows = 0
    examples = defaultdict(list)
    for k, o in oldk.items():
        n = newk.get(k)
        if not n:
            continue
        changed = [c for c in o if c not in VOLATILE and c in n and o[c] != n[c]]
        if changed:
            diffrows += 1
            for c in changed:
                diffcols[c] += 1
                if len(examples[c]) < 3:
                    examples[c].append((k[0], k[1], k[3], o[c][:40], n[c][:40]))
    print(f"rows with any non-volatile field changed: {diffrows} of {len(oldk)}")
    for c, n in diffcols.most_common():
        print(f"  {c}: {n} rows; e.g. {examples[c]}")
else:
    print("reference batch not found; skipped")

print()
print("# 3. Dedupe: smokes seen per run vs kept")
log = open(os.path.join(NEW, "run_log.md"), encoding="utf-8").read()
found_runs = re.findall(r"### (\S+) \(match (\d+) game (\d+), ([^,]+), ([^)]+)\)\n\n- smokes in game: (\d+), kept for \S+: (\d+), flagged: (\d+), overlapping: (\d+), frames: (\d+), (\d+) s", log)
per_game = defaultdict(list)
for name, mid, gno, mp, team, seen, kept, flagged, overl, frames, secs in found_runs:
    per_game[(mid, gno)].append((team, int(seen), int(kept)))
seen_twice = 0
kept_total = 0
mismatch = []
for g, lst in per_game.items():
    kept_total += sum(k for _, _, k in lst)
    if len(lst) == 2:
        seen_twice += min(s for _, s, _ in lst)
        if len({s for _, s, _ in lst}) > 1:
            mismatch.append((g, lst))
print(f"games with two runs: {sum(len(v) == 2 for v in per_game.values())}, with one run: {sum(len(v) == 1 for v in per_game.values())}")
print(f"smokes seen in both runs of a game (counted once): {seen_twice}; total kept: {kept_total}; rows in smokes.csv: {len(new)}")
print("games where the two runs saw a different number of smokes:", len(mismatch))
for g, lst in mismatch:
    print("  ", g, lst)
one_sided = [r for r in new if r.get("one_sided", "").lower() == "true"]
print(f"one-sided smokes (single-replay games): {len(one_sided)}; inferred owners: {sum(1 for r in one_sided if 'inferred' in r['owner_note'])}")

print()
print("# 4. Smokes found vs roster smoke activations, per game and team")
off = []
tot_found = tot_used = 0
roster = {}
for name, (g, _) in runs.items():
    mid = g["match_id"].replace("kots19na_", "")
    for t in g["teams"]:
        gk = (mid, str(g["game_no"]), t["name"])
        used = sum(pl.get("smoke_activations") or 0 for pl in t["players"])
        roster[gk] = used
found = Counter((r["match_id"].replace("kots19na_", ""), r["game_no"], r["team"]) for r in new)
for gk, used in sorted(roster.items(), key=lambda x: (int(x[0][0]), int(x[0][1]), x[0][2])):
    f = found.get(gk, 0)
    tot_found += f
    tot_used += used
    if abs(f - used) > 1:
        off.append((gk, f, used))
print(f"team-games checked: {len(roster)}; smokes found: {tot_found}; roster activations: {tot_used}")
print("team-games off by more than 1:", len(off), f"(found > activations: {sum(1 for o in off if o[1] > o[2])}; found < activations: {sum(1 for o in off if o[1] < o[2])})")
print("note: the activation counter double counts a use seen by both replays more than 1 s apart (backlog F5)")

print()
print("# 5. Per clan")
by = defaultdict(list)
for r in new:
    by[r["team"]].append(r)
print("| clan | games | smokes | DD smokes | smokes/game | concealed dmg/game | flagged | note |")
print("|---|---|---|---|---|---|---|---|")
conc_per_game = {t: sum(fl(r.get("smoke_damage_concealed")) for r in by[t]) / games_of[t] for t in games_of if games_of[t]}
vals = sorted(conc_per_game.values())
hi = vals[int(len(vals) * 0.9)] if vals else 0
for t in sorted(games_of, key=lambda t: -len(by[t])):
    rows = by[t]
    g = games_of[t]
    dd = sum(r.get("smoker_class", "").lower().startswith("d") for r in rows)
    flg = sum(r.get("owner_flag", "").lower() == "true" for r in rows)
    notes = []
    if not rows:
        notes.append("no smokes")
    if conc_per_game.get(t, 0) >= hi and rows:
        notes.append("top decile damage")
    if rows and flg / len(rows) > 0.35:
        notes.append("many flags")
    if g < 7:
        notes.append("under 7 games")
    print(f"| {t} | {g} | {len(rows)} | {dd} | {len(rows) / g if g else 0:.1f} | {conc_per_game.get(t, 0):,.0f} | {flg} | {', '.join(notes)} |")

print()
print("# 6. Runtime and failures")
for line in log.splitlines()[:8]:
    if line.startswith("- "):
        print(line)
fails = re.findall(r"- error: (.*)", log)
print("errors:", len(fails))
for f in fails:
    print("  ", f)
