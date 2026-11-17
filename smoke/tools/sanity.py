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
7. Enemies table: per smoke, the distinct victims of credited events equal
   the rows of targets_hit and the rows sum to the smoke total.
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

print("# 1. Ledger reconciliation (ledger shell, secondary, fire and airstrike over the game's own main battery, secondaries, fire and air-support bombs)")


def group_types(bt):
    """Game result damage fields grouped into main, secondaries, fire, flood, torpedo, ram, other."""
    g = Counter()
    for k, v in (bt or {}).items():
        if k.startswith("damage_main_"):
            g["main"] += v
        elif k.startswith("damage_atba_"):
            g["secondaries"] += v
        elif k == "damage_fire":
            g["fire"] += v
        elif k == "damage_flood":
            g["flood"] += v
        elif k.startswith("damage_tpd"):
            g["torpedo"] += v
        elif k == "damage_bomb_airsupport":
            g["airstrike"] += v
        elif k == "damage_ram":
            g["ram"] += v
        elif k not in ("damage", "damage_bomb"):
            g["other"] += v
    return g


def run_ratio(spike):
    """Ledger shell, secondary, fire and airstrike over the result's main, secondaries,
    fire and air-support bombs, or the older shell-plus-fire ratio when the record has
    no per-type results."""
    recon = spike.get("reconciliation") or []
    if recon and all("game_by_type" in r for r in recon):
        l = sum(sum((r.get("ledger_by_kind") or {}).get(k, 0.0) for k in ("shell", "secondary", "fire", "airstrike")) for r in recon)
        gt = Counter()
        for r in recon:
            gt.update(group_types(r.get("game_by_type")))
        res = gt["main"] + gt["secondaries"] + gt["fire"] + gt["airstrike"]
        return (l / res) if res else None
    return spike.get("reconciliation_ratio_shell_fire")


ratios = []
outside = []
offsets_untrusted = []
for name, (g, spike) in runs.items():
    r = run_ratio(spike)
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

print()
print("# 7. Enemies table vs credited events, per smoke")
# Per run: the distinct victims of credited events (shell, fire, airstrike)
# fired by the smoker's team with a positive share must equal the rows of the
# smoke's targets_hit, and the rows' total must equal the smoke's total.
# A victim whose only credited row is a sinking with no damage is allowed.
CREDITED_KINDS = {"shell", "fire", "airstrike"}
victim_mismatch, total_mismatch, checked, with_uncounted = [], [], 0, 0
for name, (g, _) in runs.items():
    d = os.path.join(GAMES, name)
    events_path = os.path.join(d, "damage_events.csv")
    if not os.path.exists(events_path):
        continue
    team_of = {}
    for t in g["teams"]:
        for pl in t.get("players", []):
            team_of[str(pl["entity_id"])] = t["name"]
    smokes_run = json.load(open(os.path.join(d, "smokes.json"), encoding="utf-8"))
    smokes_run = smokes_run["smokes"] if isinstance(smokes_run, dict) else smokes_run
    smoke_team = {s["smoke_id"]: s["team"] for s in smokes_run}
    victims = defaultdict(lambda: defaultdict(float))
    for r in csv.DictReader(open(events_path, encoding="utf-8")):
        if r["kind"] not in CREDITED_KINDS or not r["credited"]:
            continue
        for c in r["credited"].split(";"):
            sid, share = c.split(":")
            sid = int(sid)
            amount = fl(r["amount"]) * fl(share)
            if team_of.get(r["attacker"]) == smoke_team.get(sid) and amount > 0:
                victims[sid][r["victim"]] += amount
    for s in smokes_run:
        if s.get("one_sided") or s.get("smoke_damage_total") is None:
            continue
        checked += 1
        if s.get("targets_not_counted"):
            with_uncounted += 1
        ev = victims.get(s["smoke_id"], {})
        rows = {str(t["entity_id"]): t for t in s.get("targets_hit") or []}
        missing = sorted(set(ev) - set(rows))
        extra = sorted(e for e in set(rows) - set(ev) if not (rows[e]["sunk"] and rows[e]["damage"] == 0))
        if missing or extra:
            victim_mismatch.append((name, s["smoke_id"], s["player"], missing, extra))
        table_total = sum(t["damage"] for t in rows.values())
        if abs(table_total - s["smoke_damage_total"]) > 1.0:
            total_mismatch.append((name, s["smoke_id"], s["player"], table_total, s["smoke_damage_total"]))
print(f"smokes checked: {checked} (two-replay games); smokes with uncounted hits listed: {with_uncounted}")
print(f"smokes whose enemies table misses or adds a victim: {len(victim_mismatch)}")
for v in victim_mismatch[:20]:
    print("  ", v)
print(f"smokes whose table total differs from the smoke total by more than 1: {len(total_mismatch)}")
for v in total_mismatch[:20]:
    print("  ", v)
