"""Validation after P1 to P4 (resolved hit is a shell, victim-aware torpedo
floor, main-battery salvo fallback, airstrike kind).

python -I -X utf8 validate_p.py <repo root> <before batch (R1 to R3)> <after batch> <round 6 batch> <F4 frames batch>
"""
import csv, json, os, sys
from collections import Counter, defaultdict

ROOT, BEFORE, AFTER, R6, F4 = sys.argv[1:6]
ORIG = ("H-SR", "RESIN", "PN")
VOLATILE = {"generated_at", "wows_toolkit_rev", "smoke_signals_version", "run"}
VOYAGER = "HSR_VoyagingSta_KOTS19NA"


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
        elif k == "damage_bomb_airsupport":
            g["airstrike"] += v
        elif k == "damage_ram":
            g["ram"] += v
        elif k not in ("damage", "damage_bomb"):
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


def short(run):
    return run.replace("kots19na_", "")


def name(p):
    return p.replace("_KOTS19NA", "")


before, after = load_runs(BEFORE), load_runs(AFTER)
rb, ra = player_rows(before), player_rows(after)
results = []


def verdict(label, ok, detail):
    results.append((label, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {label}: {detail}")


print("# 1. Torpedo ledger, false positives, misses")
for label, rows in (("before", rb), ("after", ra)):
    lt = sum(x["lt"] for x in rows)
    gt = sum(x["gt"] for x in rows)
    ceiling = sum(x["lk"].get("torpedo", 0) + x["lk"].get("unknown", 0) for x in rows if x["gt"] > 0)
    fp = [x for x in rows if x["lt"] > 0 and x["gt"] == 0]
    miss = [x for x in rows if x["lt"] == 0 and x["gt"] > 0]
    with_t = [x for x in rows if x["gt"] > 0]
    ratios = sorted(x["lt"] / x["gt"] for x in with_t)
    print(f"{label}: ledger torpedo {lt:,.0f}; result {gt:,.0f}; ceiling (ledger torpedo plus unknown on torpedo scorers) {ceiling:,.0f}")
    print(f"  false positives: {len(fp)} player-runs, {sum(x['lt'] for x in fp):,.0f}; misses: {len(miss)} player-runs, {sum(x['gt'] for x in miss):,.0f}; median ratio {ratios[len(ratios) // 2]:.3f}; within 10%: {sum(1 for r in ratios if abs(r - 1) <= 0.1)} of {len(ratios)}")
lt_after = sum(x["lt"] for x in ra)
fp = sorted([x for x in ra if x["lt"] > 0 and x["gt"] == 0], key=lambda x: -x["lt"])
verdict("false positives at most 139 player-runs and 273k", len(fp) <= 139 and sum(x["lt"] for x in fp) <= 273_000, f"{len(fp)} player-runs, {sum(x['lt'] for x in fp):,.0f}")
verdict("torpedo ledger at most the 33.1M ceiling", lt_after <= 33_100_000, f"{lt_after:,.0f}")
print("False positives after, largest 10:")
for x in fp[:10]:
    print(f"  {short(x['run'])} {name(x['player'])} {x['ship']}: {x['lt']:,.0f}")

print("\n# 2. Overreach: ledger torpedo above the result by more than 10%")
over = sorted([x for x in ra if x["gt"] > 0 and x["lt"] > 1.1 * x["gt"]], key=lambda x: -(x["lt"] - x["gt"]))
excess = sum(x["lt"] - x["gt"] for x in over)
verdict("overreach at most 40 player-runs and under 0.5M excess", len(over) <= 40 and excess < 500_000, f"{len(over)} player-runs, excess {excess:,.0f}")
print("| run | player | ship | ledger torpedo | result torpedo | excess | ledger shell | result main |")
print("|---|---|---|---|---|---|---|---|")
for x in over[:10]:
    print(f"| {short(x['run'])} | {name(x['player'])} | {x['ship']} | {x['lt']:,.0f} | {x['gt']:,.0f} | {x['lt'] - x['gt']:+,.0f} | {x['lk'].get('shell', 0):,.0f} | {x['gt_all']['main']:,.0f} |")

print("\n# 3. P1: torpedo damage given up on ticks with a resolved shell hit")
given = []
for run, (g, sp) in after.items():
    names = {p["entity_id"]: (p["player"], p["ship"]) for t in g["teams"] for p in t["players"]}
    for e in sp.get("shell_hits_fitting_torpedo") or []:
        a = names.get(e["attacker"], ("?", "?"))
        v = names.get(e["victim"], ("?", "?"))
        given.append((e["amount"], run, a, v, e["damage_seconds"]))
tot = sum(x[0] for x in given)
share = tot / lt_after if lt_after else 0
print(f"events {len(given)}; damage {tot:,.0f}; {100 * share:.2f}% of the torpedo ledger after ({lt_after:,.0f})")
verdict("P1 gives up under about 1% of torpedo damage", share < 0.012, f"{100 * share:.2f}%")
print("largest 10:")
print("| amount | run | attacker | ship | victim | clock s |")
print("|---|---|---|---|---|---|")
for amt, run, a, v, t in sorted(given, reverse=True)[:10]:
    print(f"| {amt:,.0f} | {short(run)} | {name(a[0])} | {a[1]} | {name(v[0])} ({v[1]}) | {t:.1f} |")

print("\n# 4. Shell and secondary ledgers against the game's results")
for label, rows in (("before", rb), ("after", ra)):
    L = Counter()
    R = Counter()
    for x in rows:
        L.update(x["lk"])
        R.update(x["gt_all"])
    print(f"{label}: ledger shell {L['shell'] / 1e6:.2f}M, secondary {L.get('secondary', 0) / 1e6:.2f}M, fire {L['fire'] / 1e6:.2f}M, airstrike {L.get('airstrike', 0) / 1e6:.2f}M, torpedo {L['torpedo'] / 1e6:.2f}M, flood {L.get('flood', 0) / 1e6:.2f}M, unknown {L['unknown'] / 1e6:.2f}M")
    print(f"  result main {R['main'] / 1e6:.2f}M, secondaries {R['secondaries'] / 1e6:.2f}M, fire {R['fire'] / 1e6:.2f}M, airstrike {R.get('airstrike', 0) / 1e6:.2f}M, torpedo {R['torpedo'] / 1e6:.2f}M, flood {R['flood'] / 1e6:.2f}M")
    print(f"  shell over main {L['shell'] / R['main']:.3f}; secondary over secondaries {L.get('secondary', 0) / R['secondaries']:.3f}; fire over fire {L['fire'] / R['fire']:.3f}; airstrike over airstrike {(L.get('airstrike', 0) / R['airstrike']) if R.get('airstrike') else 0:.3f}; shell plus fire plus airstrike over main plus fire plus airstrike {(L['shell'] + L['fire'] + L.get('airstrike', 0)) / (R['main'] + R['fire'] + R.get('airstrike', 0)):.3f}")
    if label == "after":
        verdict("secondary ledger within 10% of the game's secondaries", abs(L.get("secondary", 0) / R["secondaries"] - 1) <= 0.10, f"{L.get('secondary', 0) / R['secondaries']:.3f}")
        verdict("shell ledger within 3% of the game's main battery", abs(L["shell"] / R["main"] - 1) <= 0.03, f"{L['shell'] / R['main']:.3f}")
        airstrike_after = (L.get("airstrike", 0), R.get("airstrike", 0))
bands = Counter()
for run, (g, sp) in after.items():
    l = r = 0.0
    for rr in sp["reconciliation"]:
        lk = rr.get("ledger_by_kind") or {}
        gt = group_types(rr.get("game_by_type"))
        l += lk.get("shell", 0) + lk.get("secondary", 0) + lk.get("fire", 0) + lk.get("airstrike", 0)
        r += gt["main"] + gt["secondaries"] + gt["fire"] + gt.get("airstrike", 0)
    ratio = l / r if r else 0
    for lo, hi in [(0, 0.9), (0.9, 0.98), (0.98, 1.02), (1.02, 1.1), (1.1, 1.25), (1.25, 9)]:
        if lo <= ratio < hi:
            bands[f"{lo}-{hi}"] += 1
print("per-run bands, ledger shell plus secondary plus fire plus airstrike over result main plus secondaries plus fire plus airstrike (after):", dict(sorted(bands.items())))

print("\n# 5. Airstrikes")
sa = smokes(AFTER)
sb = smokes(BEFORE)
credited = sum(fl(r.get("damage_airstrike")) for r in sa)
print(f"ledger airstrike field-wide {airstrike_after[0]:,.0f}; the game's damage_bomb_airsupport {airstrike_after[1]:,.0f} (ratio {airstrike_after[0] / airstrike_after[1] if airstrike_after[1] else 0:.3f})")
print(f"smoke-credited airstrike damage (sum over smokes) {credited:,.0f}, {100 * credited / airstrike_after[0] if airstrike_after[0] else 0:.1f}% of the ledger airstrike")
by_team = Counter()
for r in sa:
    by_team[r["team"]] += fl(r.get("damage_airstrike"))
print("by clan: " + ", ".join(f"{t} {v:,.0f}" for t, v in by_team.most_common(8) if v > 0))
strike_ships = Counter()
for x in ra:
    if x["lk"].get("airstrike", 0) > 0:
        strike_ships[x["ship"]] += x["lk"]["airstrike"]
print("ledger airstrike by ship: " + ", ".join(f"{s} {v:,.0f}" for s, v in strike_ships.most_common()))
no_strike_fp = [x for x in ra if x["lk"].get("airstrike", 0) > 0 and x["gt_all"].get("airstrike", 0) == 0]
print(f"ships credited airstrike with no airstrike in the result: {len(no_strike_fp)} player-runs, {sum(x['lk']['airstrike'] for x in no_strike_fp):,.0f}")
over_strike = [x for x in ra if x["gt_all"].get("airstrike", 0) > 0 and x["lk"].get("airstrike", 0) > 1.1 * x["gt_all"]["airstrike"]]
print(f"ledger airstrike more than 10% over the result: {len(over_strike)} player-runs, excess {sum(x['lk']['airstrike'] - x['gt_all']['airstrike'] for x in over_strike):,.0f}")


def voyager(batch):
    tot = Counter()
    per_smoke = []
    G = os.path.join(batch, "games")
    for d in sorted(os.listdir(G)):
        p = os.path.join(G, d, "smokes.json")
        if not d.endswith("_h-sr") or not os.path.exists(p):
            continue
        loaded = json.load(open(p, encoding="utf-8"))
        for s in loaded["smokes"] if isinstance(loaded, dict) else loaded:
            dd = s.get("damage_detail") or {}
            for e, st in (dd.get("shooter_stats") or {}).items():
                if any(x["player"] == VOYAGER and str(x["entity_id"]) == str(e) for x in s.get("shooter_detail") or []):
                    tot["damage"] += st["damage"]
                    for k, v in (st.get("by_kind") or {}).items():
                        tot[k] += v
                    per_smoke.append((s["smoke_id"], short(d), st["damage"], st.get("by_kind") or {}))
    return tot, per_smoke


vb, _ = voyager(BEFORE)
va, va_rows = voyager(AFTER)
print(f"\nHSR_VoyagingSta (Utrecht) smoke credit as a shooter: before {vb['damage']:,.0f}; after {va['damage']:,.0f} = shell {va.get('shell', 0):,.0f}, fire {va.get('fire', 0):,.0f}, airstrike {va.get('airstrike', 0):,.0f}")
for sid, run, d, bk in sorted(va_rows, key=lambda x: -x[2])[:8]:
    print(f"  smoke {sid} {run}: {d:,.0f} (" + ", ".join(f"{k} {v:,.0f}" for k, v in bk.items()) + ")")

print("\n# 6. Kills from smoke")
sf4 = smokes(F4)
for label, rows in (("F4 frames batch", sf4), ("before (R1 to R3)", sb), ("after", sa)):
    k = sum(int(r["kills_from_smoke"] or 0) for r in rows)
    per = {t: sum(int(r["kills_from_smoke"] or 0) for r in rows if r["team"] == t) for t in ORIG}
    print(f"{label}: kills from smoke {k} (H-SR {per['H-SR']}, RESIN {per['RESIN']}, PN {per['PN']})")

print("\n# 7. Original 217 rows against round 6 (damage and flag columns; a no-frames run leaves the state columns empty)")
STATE_PREFIX = ("score_", "ships_alive", "hp_", "spotting", "cap_proximity", "nearest_enemy", "frame_", "allies_hp", "enemies_hp", "our_", "their_")
old = {(r["match_id"], r["game_no"], r["team"], r["smoke_id"]): r for r in smokes(R6)}
new = {(r["match_id"], r["game_no"], r["team"], r["smoke_id"]): r for r in sa if r["team"] in ORIG}
blank_cols = set()
for k, o in old.items():
    n = new.get(k)
    if n:
        for c in o:
            if c in n and o[c] != "" and n[c] == "":
                blank_cols.add(c)
print(f"reference rows {len(old)}; now {len(new)}; missing {sum(1 for k in old if k not in new)}; added {sum(1 for k in new if k not in old)}; columns empty in the no-frames run and skipped: {len(blank_cols)}")
changed = 0
cols = Counter()
for k, o in old.items():
    n = new.get(k)
    if not n:
        continue
    ch = [c for c in o if c not in VOLATILE and c not in blank_cols and c in n and o[c] != n[c]]
    if ch:
        changed += 1
        cols.update(ch)
        print(f"- {k[3]} {o['team']} {name(o['player'])} {o['ship']}, {o['round'].replace('Groups / ', '').replace('Playoffs / ', '')} vs {o['opponent']} g{o['game_no']} ({o['map_display']}) {o['t_activate_clock']}: " + "; ".join(f"{c} {o[c][:28]} -> {n[c][:28]}" for c in ch))
print(f"rows changed: {changed} of {len(old)}; columns: {dict(cols.most_common())}")

print("\n# 8. Smoke of the Tournament and per-clan concealed per game")
inv = list(csv.DictReader(open(os.path.join(ROOT, "smoke", "inventory.csv"), encoding="utf-8")))
games_of = Counter()
for r in inv:
    if r["status"] == "played":
        for t in r["teams"].split(" vs "):
            games_of[t] += 1
for label, rows in (("before", sb), ("after", sa)):
    print(f"\n{label} top 8:")
    for i, r in enumerate(sorted(rows, key=lambda r: (-fl(r["smoke_damage_concealed"]), -fl(r["smoke_damage_total"])))[:8], 1):
        print(f"  {i}. {r['smoke_id']} {r['team']} {name(r['player'])} {r['ship']}, {r['round'].replace('Groups / ', '').replace('Playoffs / ', '')} vs {r['opponent']} g{r['game_no']} ({r['map_display']}) {r['t_activate_clock']}: {fl(r['smoke_damage_concealed']):,.0f} / {fl(r['smoke_damage_total']):,.0f}")
print("\n| clan | games | concealed/game before | after | change |")
print("|---|---|---|---|---|")
out = []
for t in games_of:
    cb = sum(fl(r["smoke_damage_concealed"]) for r in sb if r["team"] == t) / games_of[t]
    ca = sum(fl(r["smoke_damage_concealed"]) for r in sa if r["team"] == t) / games_of[t]
    out.append((t, games_of[t], cb, ca))
for t, g, cb, ca in sorted(out, key=lambda x: -x[3]):
    print(f"| {t} | {g} | {cb:,.0f} | {ca:,.0f} | {100 * (ca - cb) / cb if cb else 0:+.1f}% |")

print("\n# Summary")
for label, ok, detail in results:
    print(f"- {'PASS' if ok else 'FAIL'}: {label} ({detail})")
print("all passed" if all(ok for _, ok, _ in results) else "some checks failed")
