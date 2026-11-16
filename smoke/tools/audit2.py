"""STEP 2b part 2: ledger inflation across every run, credit vs game result, flag detail.

python -I -X utf8 audit2.py <repo root> <batch dir>
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict

ROOT, NEW = sys.argv[1:3]
ORIG = {"H-SR", "RESIN", "PN"}
GAMES = os.path.join(NEW, "games")


def fl(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


rows = list(csv.DictReader(open(os.path.join(NEW, "smokes.csv"), encoding="utf-8")))
inv = list(csv.DictReader(open(os.path.join(ROOT, "smoke", "inventory.csv"), encoding="utf-8")))
games_of = Counter()
for r in inv:
    if r["status"] == "played":
        for t in r["teams"].split(" vs "):
            games_of[t] += 1

runs = {}
for name in sorted(os.listdir(GAMES)):
    d = os.path.join(GAMES, name)
    if not os.path.exists(os.path.join(d, "game.json")):
        continue
    g = json.load(open(os.path.join(d, "game.json"), encoding="utf-8"))
    spike = json.load(open(os.path.join(d, "damage_spike.json"), encoding="utf-8"))
    sj = json.load(open(os.path.join(d, "smokes.json"), encoding="utf-8"))["smokes"]
    runs[name] = (g, spike, sj)

print("# A. Perspective merge: ledger vs the game's own result, every run")
ratios = []
bad = []
for name, (g, spike, sj) in runs.items():
    team = next(t["name"] for t in g["teams"] if name.endswith("_" + slug(t["name"])))
    r = spike["reconciliation_ratio_shell_fire"]
    ratios.append(r)
    ledger = {x["player"]: x for x in spike["reconciliation"]}
    clan_players = [p["player"] for t in g["teams"] if t["name"] == team for p in t["players"]]
    clan_ledger = sum(fl(ledger[p]["ledger_shell_fire"]) for p in clan_players if p in ledger)
    clan_game = sum(fl(ledger[p]["game_shell_fire"]) for p in clan_players if p in ledger)
    smoke_total = sum(s["smoke_damage_total"] for s in sj)
    conc = sum(s["damage_split"]["concealed"] for s in sj)
    if r > 1.25:
        bad.append((name, team, r, clan_ledger, clan_game, len(sj), smoke_total, conc, spike["events_per_replay"], spike["events_dropped_as_duplicates"]))
print("game-level shell+fire ratio (ledger over result): " + ", ".join(f"{lo}-{hi}: {sum(1 for r in ratios if lo <= r < hi)}" for lo, hi in [(0, 0.8), (0.8, 0.95), (0.95, 1.05), (1.05, 1.25), (1.25, 1.6), (1.6, 3)]))
print(f"\nruns with ratio over 1.25: {len(bad)} (games: {len({n.rsplit('_', 1)[0] for n, *_ in bad})})")
print("| run | team | ratio | clan ledger | clan result | smokes | smoke dmg | concealed | events per replay | dropped as dup |")
print("|---|---|---|---|---|---|---|---|---|---|")
for b in sorted(bad, key=lambda b: -b[2]):
    print(f"| {b[0].replace('kots19na_', '')} | {b[1]} | {b[2]:.2f} | {b[3]:,.0f} | {b[4]:,.0f} | {b[5]} | {b[6]:,.0f} | {b[7]:,.0f} | {b[8]} | {b[9]} |")

# Clock offset in the inflated games: modal time difference between unmerged copies.
print("\nClock offset between the two perspectives in the inflated games (modal delta of same attacker/victim/amount shell pairs, 0.25 s bins, deltas up to 30 s):")
for b in sorted(bad, key=lambda b: -b[2]):
    d = os.path.join(GAMES, b[0])
    ev = list(csv.DictReader(open(os.path.join(d, "damage_events.csv"), encoding="utf-8")))
    by = defaultdict(list)
    for e in ev:
        if e["kind"] == "shell":
            by[(e["attacker"], e["victim"], e["amount"])].append(fl(e["damage_s"]))
    bins = Counter()
    for k, ts in by.items():
        ts.sort()
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                dt = ts[j] - ts[i]
                if 0 < dt <= 30:
                    bins[round(dt * 4) / 4] += 1
    top = bins.most_common(3)
    print(f"- {b[0].replace('kots19na_', '')}: {top}")

print("\nCredit affected: smokes and concealed damage in inflated runs, per clan:")
per = defaultdict(lambda: [0, 0.0, 0.0])
for b in bad:
    per[b[1]][0] += b[5]
    per[b[1]][1] += b[6]
    per[b[1]][2] += b[7]
tot_conc = {t: sum(fl(r["smoke_damage_concealed"]) for r in rows if r["team"] == t) for t in games_of}
print("| clan | games | inflated runs | smokes in them | smoke dmg in them | concealed in them | clan concealed total | share |")
print("|---|---|---|---|---|---|---|---|")
for t, (n, dmg, conc) in sorted(per.items(), key=lambda x: -x[1][2]):
    k = sum(1 for b in bad if b[1] == t)
    print(f"| {t} | {games_of[t]} | {k} | {n} | {dmg:,.0f} | {conc:,.0f} | {tot_conc[t]:,.0f} | {100 * conc / tot_conc[t] if tot_conc[t] else 0:.0f}% |")

print()
print("# B. Smoke credit per shooter vs the game's own shell+fire result, every run")
over = []
checked = 0
for name, (g, spike, sj) in runs.items():
    ledger = {x["player"]: x for x in spike["reconciliation"]}
    credit = Counter()
    for s in sj:
        for sh in s.get("shooter_detail") or []:
            credit[sh["player"]] += fl(sh.get("damage"))
    for p, c in credit.items():
        checked += 1
        res = fl(ledger.get(p, {}).get("game_shell_fire"))
        if c > res * 1.05 + 100:
            over.append((name, p, c, res, fl(ledger.get(p, {}).get("ledger_shell_fire")), spike["reconciliation_ratio_shell_fire"]))
print(f"shooter-runs checked: {checked}; credit above the shooter's own game result: {len(over)}")
print("| run | shooter | smoke credit | game result shell+fire | ledger shell+fire | run ratio |")
print("|---|---|---|---|---|---|")
for o in sorted(over, key=lambda o: -(o[2] - o[3]))[:25]:
    print(f"| {o[0].replace('kots19na_', '')} | {o[1].replace('_KOTS19NA', '')} | {o[2]:,.0f} | {o[3]:,.0f} | {o[4]:,.0f} | {o[5]:.2f} |")
print("in runs with ratio over 1.25:", sum(1 for o in over if o[5] > 1.25), "; in other runs:", sum(1 for o in over if o[5] <= 1.25))

print()
print("# C. The 'nearest ship over 600 m' note by ship and smoke type")
far = [r for r in rows if "nearest ship" in r["owner_note"] and fl(r["owner_distance_m"]) <= 2000]
print("| ship | smoke type | smokes | with the note | % | median dist of noted | activation matched |")
print("|---|---|---|---|---|---|---|")
byship = defaultdict(list)
for r in rows:
    byship[(r["ship"], r["smoke_type"])].append(r)
for k, rs in sorted(byship.items(), key=lambda x: -len(x[1])):
    f = [r for r in rs if r in far]
    if not f and len(rs) < 20:
        continue
    ds = sorted(fl(r["owner_distance_m"]) for r in f)
    act = sum(1 for r in f if "no smoke activation" not in r["owner_note"])
    print(f"| {k[0]} | {k[1]} | {len(rs)} | {len(f)} | {100 * len(f) / len(rs):.0f} | {ds[len(ds) // 2] if ds else 0:.0f} | {act} |")
print("\nShip mix, original 3 vs others (share of smokes by smoke type):")
for label, pred in (("original 3", lambda t: t in ORIG), ("others", lambda t: t not in ORIG)):
    sub = [r for r in rows if pred(r["team"])]
    c = Counter(r["smoke_type"] for r in sub)
    print(f"- {label}: " + ", ".join(f"{k} {100 * n / len(sub):.0f}%" for k, n in c.most_common()))
print("\nDistance of the attributed ship for unflagged smokes, by smoke type (median, 90th pct):")
for st in ("standard", "cruiser", "exhaust", "crawling"):
    ds = sorted(fl(r["owner_distance_m"]) for r in rows if r["smoke_type"] == st and r["owner_flag"].lower() != "true")
    if ds:
        print(f"- {st}: n {len(ds)}, median {ds[len(ds) // 2]:.0f} m, p90 {ds[int(len(ds) * 0.9)]:.0f} m, max {ds[-1]:.0f} m")
print("Same for the noted smokes (600 to 2000 m):")
for st in ("standard", "cruiser", "exhaust", "crawling"):
    ds = sorted(fl(r["owner_distance_m"]) for r in far if r["smoke_type"] == st)
    if ds:
        print(f"- {st}: n {len(ds)}, median {ds[len(ds) // 2]:.0f} m, p90 {ds[int(len(ds) * 0.9)]:.0f} m, max {ds[-1]:.0f} m")
print("\nRadius of the smoke by type (base_radius, distinct):", {st: sorted({r['base_radius'] for r in rows if r['smoke_type'] == st}) for st in ('standard', 'cruiser', 'exhaust', 'crawling')})

print()
print("# D. 'no activation within 5 s' smokes")
noact = [r for r in rows if "no smoke activation" in r["owner_note"]]
print(f"count {len(noact)}; with a clock: {sum(1 for r in noact if r['t_activate_clock'])}; created clock present: {sum(1 for r in noact if r['t_created_clock'])}")
print("by team:", dict(Counter(r["team"] for r in noact).most_common()))
print("by ship:", dict(Counter(r["ship"] for r in noact).most_common(12)))
# recorder: is the attributed player the recorder of the primary replay?
rec_of = {}
for name, (g, spike, sj) in runs.items():
    log = open(os.path.join(GAMES, name, "run_log.md"), encoding="utf-8").read()
    m = re.search(r"primary_replay: .*?\(recorded by ([^)]+)\)", log)
    rec_of[name] = m.group(1) if m else ""
n_rec = 0
n_all = 0
for r in noact:
    run = next((n for n in runs if n.endswith("_" + slug(r["team"])) and runs[n][0]["match_id"] == r["match_id"] and str(runs[n][0]["game_no"]) == r["game_no"]), None)
    if run:
        n_all += 1
        if rec_of[run] == r["player"]:
            n_rec += 1
print(f"attributed to the recorder of the primary replay: {n_rec} of {n_all}")
# the recorder's own smokes overall
rec_smokes = 0
rec_noact = 0
for r in rows:
    run = next((n for n in runs if n.endswith("_" + slug(r["team"])) and runs[n][0]["match_id"] == r["match_id"] and str(runs[n][0]["game_no"]) == r["game_no"]), None)
    if run and rec_of[run] == r["player"]:
        rec_smokes += 1
        if "no smoke activation" in r["owner_note"]:
            rec_noact += 1
print(f"smokes attributed to a recorder: {rec_smokes}, of which without activation: {rec_noact}")
print("created clock of the no-activation smokes (first 5 minutes vs later):", Counter("first 60 s" if fl(r["t_created"]) < 60 else ("under 5 min" if fl(r["t_created"]) < 300 else "later") for r in noact))
print("damage on them: concealed", f"{sum(fl(r['smoke_damage_concealed']) for r in noact):,.0f}", "total", f"{sum(fl(r['smoke_damage_total']) for r in noact):,.0f}")
