"""Validation after R1 to R3 and the secondary-battery kind.

python -I -X utf8 validate_r.py <repo root> <before batch (per-type)> <after batch> <round 6 batch>
"""
import csv, json, os, random, sys
from collections import Counter, defaultdict

ROOT, BEFORE, AFTER, R6 = sys.argv[1:5]
ORIG = ("H-SR", "RESIN", "PN")
WATCH = ("Napoli", "Brisbane", "Minotaur", "Prinz Adalbert", "San Mart")
VOLATILE = {"generated_at", "wows_toolkit_rev", "smoke_signals_version", "run"}


def fl(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


def group_types(bt):
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
        elif k == "damage_ram":
            g["ram"] += v
        elif k != "damage":
            g["other"] += v
    return g


def load_runs(b):
    runs = {}
    G = os.path.join(b, "games")
    for name in sorted(os.listdir(G)):
        d = os.path.join(G, name)
        if os.path.exists(os.path.join(d, "damage_spike.json")):
            runs[name] = (json.load(open(os.path.join(d, "game.json"), encoding="utf-8")), json.load(open(os.path.join(d, "damage_spike.json"), encoding="utf-8")))
    return runs


def player_rows(runs):
    rows = []
    for name, (g, sp) in runs.items():
        ships = {p["player"]: p["ship"] for t in g["teams"] for p in t["players"]}
        for r in sp["reconciliation"]:
            lk = r.get("ledger_by_kind") or {}
            gt = group_types(r.get("game_by_type"))
            rows.append({"run": name, "player": r["player"], "ship": ships.get(r["player"], "?"), "lt": lk.get("torpedo", 0.0), "gt": gt["torpedo"], "lk": lk, "gt_all": gt})
    return rows


def smokes(b):
    return list(csv.DictReader(open(os.path.join(b, "smokes.csv"), encoding="utf-8")))


before, after = load_runs(BEFORE), load_runs(AFTER)
rb, ra = player_rows(before), player_rows(after)

print("# 1. Field torpedo ledger")
for label, rows in (("before", rb), ("after", ra)):
    lt = sum(x["lt"] for x in rows)
    gt = sum(x["gt"] for x in rows)
    ceiling = sum(x["lk"].get("torpedo", 0) + x["lk"].get("unknown", 0) for x in rows if x["gt"] > 0)
    fp = [x for x in rows if x["lt"] > 0 and x["gt"] == 0]
    miss = [x for x in rows if x["lt"] == 0 and x["gt"] > 0]
    with_t = [x for x in rows if x["gt"] > 0]
    ratios = sorted(x["lt"] / x["gt"] for x in with_t)
    print(f"{label}: ledger torpedo {lt:,.0f}; result {gt:,.0f}; ceiling (ledger torpedo plus unknown on torpedo scorers) {ceiling:,.0f}; ledger over ceiling {lt / ceiling:.3f}")
    print(f"  false positives: {len(fp)} player-runs, {sum(x['lt'] for x in fp):,.0f}; misses: {len(miss)} player-runs, {sum(x['gt'] for x in miss):,.0f}; median ratio {ratios[len(ratios) // 2]:.3f}; within 10%: {sum(1 for r in ratios if abs(r - 1) <= 0.1)} of {len(ratios)}")
print("\nFalse positives after, largest 10:")
fp = sorted([x for x in ra if x["lt"] > 0 and x["gt"] == 0], key=lambda x: -x["lt"])[:10]
for x in fp:
    print(f"  {x['run'].replace('kots19na_', '')} {x['player'].replace('_KOTS19NA', '')} {x['ship']}: {x['lt']:,.0f}")

print("\n# 2. Overreach: ledger torpedo above the result by more than 10%, worst 10 (after)")
over = sorted([x for x in ra if x["gt"] > 0 and x["lt"] > 1.1 * x["gt"]], key=lambda x: -(x["lt"] - x["gt"]))
print(f"player-runs: {len(over)}; excess {sum(x['lt'] - x['gt'] for x in over):,.0f}")
print("| run | player | ship | ledger torpedo | result torpedo | excess | ledger shell | result main |")
print("|---|---|---|---|---|---|---|---|")
for x in over[:10]:
    print(f"| {x['run'].replace('kots19na_', '')} | {x['player'].replace('_KOTS19NA', '')} | {x['ship']} | {x['lt']:,.0f} | {x['gt']:,.0f} | {x['lt'] - x['gt']:+,.0f} | {x['lk'].get('shell', 0):,.0f} | {x['gt_all']['main']:,.0f} |")
print("watched ships (Napoli, Brisbane, Minotaur, Prinz Adalbert, San Martin), after:")
for ship in WATCH:
    xs = [x for x in ra if x["ship"].startswith(ship)]
    lt = sum(x["lt"] for x in xs)
    gt = sum(x["gt"] for x in xs)
    o = [x for x in xs if x["gt"] > 0 and x["lt"] > 1.1 * x["gt"]]
    f = [x for x in xs if x["lt"] > 0 and x["gt"] == 0]
    print(f"  {ship}: {len(xs)} player-runs, ledger {lt:,.0f} vs result {gt:,.0f}; over 10%: {len(o)} ({sum(x['lt'] - x['gt'] for x in o):,.0f}); false positives {len(f)} ({sum(x['lt'] for x in f):,.0f})")

print("\n# 3. Same-tick sample (after)")
same = []
for name, (g, sp) in after.items():
    for e in csv.DictReader(open(os.path.join(AFTER, "games", name, "damage_events.csv"), encoding="utf-8")):
        if e["kind"] == "torpedo" and e["fire_source"] == "ShotHit":
            same.append((name, e))
n_torp = sum(sp["events_by_kind"].get("torpedo", 0) for _, sp in after.values())
print(f"torpedo events {n_torp}; sharing a tick with a shell hit: {len(same)}")
key_rows = {(x["run"], x["player"]): x for x in ra}
random.seed(11)
print("| run | attacker | ship | victim | amount | ledger torpedo | result torpedo | as shell instead | verdict |")
print("|---|---|---|---|---|---|---|---|---|")
verdicts = Counter()
judged = []
for name, e in same:
    x = key_rows.get((name, e["attacker_name"]))
    if not x:
        continue
    as_shell = x["lt"] - fl(e["amount"])
    v = "torpedo" if abs(x["lt"] - x["gt"]) <= abs(as_shell - x["gt"]) else "shell"
    verdicts[v] += 1
    judged.append((name, e, x, as_shell, v))
for name, e, x, as_shell, v in random.sample(judged, min(10, len(judged))):
    print(f"| {name.replace('kots19na_', '')} | {e['attacker_name'].replace('_KOTS19NA', '')} | {x['ship']} | {e['victim_name'].replace('_KOTS19NA', '')} | {fl(e['amount']):,.0f} | {x['lt']:,.0f} | {x['gt']:,.0f} | {as_shell:,.0f} | {v} |")
print("all same-tick events judged by the run total:", dict(verdicts))

print("\n# 4. Kills from smoke")
sb, sa = smokes(os.path.join(ROOT, "output/20261116-161621")), smokes(AFTER)
for label, rows in (("before", sb), ("after", sa)):
    k = sum(int(r["kills_from_smoke"] or 0) for r in rows)
    per = {t: sum(int(r["kills_from_smoke"] or 0) for r in rows if r["team"] == t) for t in ORIG}
    deaths = sum(int(r["smoke_deaths"] or 0) for r in rows)
    print(f"{label}: kills from smoke {k} (H-SR {per['H-SR']}, RESIN {per['RESIN']}, PN {per['PN']}); smoke deaths {deaths}")

print("\n# 5. Shell ledger against main plus secondaries")
for label, rows in (("before", rb), ("after", ra)):
    L = Counter()
    R = Counter()
    for x in rows:
        L.update(x["lk"])
        R.update(x["gt_all"])
    print(f"{label}: ledger shell {L['shell'] / 1e6:.1f}M, secondary {L.get('secondary', 0) / 1e6:.1f}M, fire {L['fire'] / 1e6:.1f}M, torpedo {L['torpedo'] / 1e6:.1f}M, unknown {L['unknown'] / 1e6:.1f}M | result main {R['main'] / 1e6:.1f}M, secondaries {R['secondaries'] / 1e6:.1f}M, fire {R['fire'] / 1e6:.1f}M, torpedo {R['torpedo'] / 1e6:.1f}M")
    print(f"  shell over main: {L['shell'] / R['main']:.3f}; shell plus secondary over main plus secondaries: {(L['shell'] + L.get('secondary', 0)) / (R['main'] + R['secondaries']):.3f}; secondary over secondaries: {L.get('secondary', 0) / R['secondaries']:.3f}; fire over fire: {L['fire'] / R['fire']:.3f}; shell plus fire over main plus fire: {(L['shell'] + L['fire']) / (R['main'] + R['fire']):.3f}")
bands = Counter()
for name, (g, sp) in after.items():
    l = r = 0.0
    for rr in sp["reconciliation"]:
        lk = rr.get("ledger_by_kind") or {}
        gt = group_types(rr.get("game_by_type"))
        l += lk.get("shell", 0) + lk.get("secondary", 0) + lk.get("fire", 0)
        r += gt["main"] + gt["secondaries"] + gt["fire"]
    ratio = l / r if r else 0
    for lo, hi in [(0, 0.9), (0.9, 0.98), (0.98, 1.02), (1.02, 1.1), (1.1, 1.25), (1.25, 9)]:
        if lo <= ratio < hi:
            bands[f"{lo}-{hi}"] += 1
print("per-run bands, ledger shell plus secondary plus fire over result main plus secondaries plus fire (after):", dict(bands))
bands2 = Counter()
for name, (g, sp) in after.items():
    l = r = 0.0
    for rr in sp["reconciliation"]:
        lk = rr.get("ledger_by_kind") or {}
        gt = group_types(rr.get("game_by_type"))
        l += lk.get("shell", 0) + lk.get("fire", 0)
        r += gt["main"] + gt["fire"]
    ratio = l / r if r else 0
    for lo, hi in [(0, 0.9), (0.9, 0.98), (0.98, 1.02), (1.02, 1.1), (1.1, 1.25), (1.25, 9)]:
        if lo <= ratio < hi:
            bands2[f"{lo}-{hi}"] += 1
print("per-run bands, ledger shell plus fire over result main plus fire (after):", dict(bands2))

print("\n# 6. Original 217 rows against round 6")
old = {(r["match_id"], r["game_no"], r["team"], r["smoke_id"]): r for r in smokes(R6)}
new = {(r["match_id"], r["game_no"], r["team"], r["smoke_id"]): r for r in sa if r["team"] in ORIG}
print(f"reference rows {len(old)}; now {len(new)}; missing {sum(1 for k in old if k not in new)}; added {sum(1 for k in new if k not in old)}")
changed = 0
cols = Counter()
for k, o in old.items():
    n = new.get(k)
    if not n:
        continue
    ch = [c for c in o if c not in VOLATILE and c in n and o[c] != n[c]]
    if ch:
        changed += 1
        cols.update(ch)
        print(f"- {k[3]} {o['team']} {o['player'].replace('_KOTS19NA', '')} {o['ship']}, {o['round'].replace('Groups / ', '').replace('Playoffs / ', '')} vs {o['opponent']} g{o['game_no']} ({o['map_display']}) {o['t_activate_clock']}: " + "; ".join(f"{c} {o[c][:28]} -> {n[c][:28]}" for c in ch))
print(f"rows changed: {changed} of {len(old)}; columns: {dict(cols.most_common())}")

print("\n# 7. Smoke of the Tournament candidates and per-clan concealed per game")
inv = list(csv.DictReader(open(os.path.join(ROOT, "smoke", "inventory.csv"), encoding="utf-8")))
games_of = Counter()
for r in inv:
    if r["status"] == "played":
        for t in r["teams"].split(" vs "):
            games_of[t] += 1
for label, rows in (("before", sb), ("after", sa)):
    print(f"\n{label} top 8:")
    for i, r in enumerate(sorted(rows, key=lambda r: (-fl(r["smoke_damage_concealed"]), -fl(r["smoke_damage_total"])))[:8], 1):
        print(f"  {i}. {r['smoke_id']} {r['team']} {r['player'].replace('_KOTS19NA', '')} {r['ship']}, {r['round'].replace('Groups / ', '').replace('Playoffs / ', '')} vs {r['opponent']} g{r['game_no']} ({r['map_display']}) {r['t_activate_clock']}: {fl(r['smoke_damage_concealed']):,.0f} / {fl(r['smoke_damage_total']):,.0f}")
print("\n| clan | games | concealed/game before | after | change | smokes 20k+ before | after |")
print("|---|---|---|---|---|---|---|")
out = []
for t in games_of:
    cb = sum(fl(r["smoke_damage_concealed"]) for r in sb if r["team"] == t) / games_of[t]
    ca = sum(fl(r["smoke_damage_concealed"]) for r in sa if r["team"] == t) / games_of[t]
    kb = sum(1 for r in sb if r["team"] == t and fl(r["smoke_damage_total"]) >= 20000)
    ka = sum(1 for r in sa if r["team"] == t and fl(r["smoke_damage_total"]) >= 20000)
    out.append((t, games_of[t], cb, ca, kb, ka))
for t, g, cb, ca, kb, ka in sorted(out, key=lambda x: -x[3]):
    print(f"| {t} | {g} | {cb:,.0f} | {ca:,.0f} | {100 * (ca - cb) / cb if cb else 0:+.0f}% | {kb} | {ka} |")
