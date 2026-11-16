"""F4 validation and ledger over-count breakdown.

python -I -X utf8 f4check.py <batch dir with ledger_by_kind and game_by_type>
"""
import csv, json, os, sys
from collections import Counter, defaultdict

B = sys.argv[1]
G = os.path.join(B, "games")


def fl(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


def group_types(bt):
    g = Counter()
    for k, v in bt.items():
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
        elif k == "damage":
            g["total"] += v
        else:
            g["other"] += v
    return g


runs = {}
for name in sorted(os.listdir(G)):
    d = os.path.join(G, name)
    if not os.path.exists(os.path.join(d, "damage_spike.json")):
        continue
    runs[name] = (json.load(open(os.path.join(d, "game.json"), encoding="utf-8")), json.load(open(os.path.join(d, "damage_spike.json"), encoding="utf-8")))

print("# 1. F4: ledger torpedo damage vs the game's torpedo result, per player per run")
rows = []
ship_of = {}
for name, (g, sp) in runs.items():
    ships = {p["player"]: (p["ship"], p["ship_class"]) for t in g["teams"] for p in t["players"]}
    for r in sp["reconciliation"]:
        lk = r.get("ledger_by_kind") or {}
        gt = group_types(r.get("game_by_type") or {})
        lt = lk.get("torpedo", 0.0)
        gtp = gt["torpedo"]
        ship_of[r["player"]] = ships.get(r["player"], ("?", "?"))
        rows.append((name, r["player"], ships.get(r["player"], ("?", "?"))[0], lt, gtp, lk, gt))
with_torp = [x for x in rows if x[4] > 0]
ratios = sorted(x[3] / x[4] for x in with_torp)
print(f"player-runs: {len(rows)}; with torpedo damage in the game result: {len(with_torp)}")
print(f"ratio ledger/result over those: median {ratios[len(ratios) // 2]:.3f}, mean {sum(ratios) / len(ratios):.3f}; within 10%: {sum(1 for r in ratios if abs(r - 1) <= 0.1)}; under 0.5: {sum(1 for r in ratios if r < 0.5)}; over 1.5: {sum(1 for r in ratios if r > 1.5)}")
tl = sum(x[3] for x in rows)
tg = sum(x[4] for x in rows)
print(f"field total: ledger torpedo {tl:,.0f} vs game torpedo {tg:,.0f} (ratio {tl / tg:.3f})")
fp = [x for x in rows if x[3] > 0 and x[4] == 0]
miss = [x for x in rows if x[3] == 0 and x[4] > 0]
print(f"player-runs with ledger torpedo but none in the result (false positives): {len(fp)}, damage {sum(x[3] for x in fp):,.0f}")
for x in sorted(fp, key=lambda x: -x[3])[:10]:
    print(f"  {x[0].replace('kots19na_', '')} {x[1].replace('_KOTS19NA', '')} {x[2]}: ledger torpedo {x[3]:,.0f}; ledger shell {x[5].get('shell', 0):,.0f} vs result main {x[6]['main']:,.0f}")
print(f"player-runs with torpedo damage in the result but none in the ledger (misses): {len(miss)}, damage {sum(x[4] for x in miss):,.0f}")
for x in sorted(miss, key=lambda x: -x[4])[:10]:
    print(f"  {x[0].replace('kots19na_', '')} {x[1].replace('_KOTS19NA', '')} {x[2]}: result torpedo {x[4]:,.0f}; ledger shell {x[5].get('shell', 0):,.0f} vs result main {x[6]['main']:,.0f}; ledger unknown {x[5].get('unknown', 0):,.0f}")
print("\nWorst 10 by absolute gap (ledger minus result):")
print("| run | player | ship | ledger torpedo | result torpedo | gap | ledger shell | result main+sec | ledger unknown |")
print("|---|---|---|---|---|---|---|---|---|")
for x in sorted(rows, key=lambda x: -abs(x[3] - x[4]))[:10]:
    print(f"| {x[0].replace('kots19na_', '')} | {x[1].replace('_KOTS19NA', '')} | {x[2]} | {x[3]:,.0f} | {x[4]:,.0f} | {x[3] - x[4]:+,.0f} | {x[5].get('shell', 0):,.0f} | {x[6]['main'] + x[6]['secondaries']:,.0f} | {x[5].get('unknown', 0):,.0f} |")

print("\n# 1b. Torpedo-kind events that share a tick with a resolved shell hit")
same = []
for name, (g, sp) in runs.items():
    ev = list(csv.DictReader(open(os.path.join(G, name, "damage_events.csv"), encoding="utf-8")))
    for e in ev:
        if e["kind"] == "torpedo" and e["fire_source"] == "ShotHit":
            same.append((name, e))
n_torp = sum(sp["events_by_kind"].get("torpedo", 0) for _, sp in runs.values())
print(f"torpedo events: {n_torp}; with a shell hit on the same tick: {len(same)}")
# sample 10: judge by which classification brings the player's run closer to the game result
by_run_player = {(x[0], x[1]): x for x in rows}
import random
random.seed(7)
sample = random.sample(same, min(10, len(same)))
print("| run | attacker | ship | victim | amount | ledger torpedo | result torpedo | if this were a shell | verdict |")
print("|---|---|---|---|---|---|---|---|---|")
for name, e in sample:
    x = by_run_player.get((name, e["attacker_name"]))
    if not x:
        continue
    lt, gt = x[3], x[4]
    as_shell = lt - fl(e["amount"])
    verdict = "torpedo" if abs(lt - gt) <= abs(as_shell - gt) else "shell"
    print(f"| {name.replace('kots19na_', '')} | {e['attacker_name'].replace('_KOTS19NA', '')} | {x[2]} | {e['victim_name'].replace('_KOTS19NA', '')} | {fl(e['amount']):,.0f} | {lt:,.0f} | {gt:,.0f} | {as_shell:,.0f} | {verdict} |")
verdicts = Counter()
for name, e in same:
    x = by_run_player.get((name, e["attacker_name"]))
    if x:
        lt, gt = x[3], x[4]
        verdicts["torpedo" if abs(lt - gt) <= abs(lt - fl(e["amount"]) - gt) else "shell"] += 1
print("same-tick events, all, judged by the player's run total:", dict(verdicts))

print("\n# 1c. Ships credited torpedo damage")
by_ship = defaultdict(lambda: [0.0, 0.0, 0])
for x in rows:
    s = by_ship[x[2]]
    s[0] += x[3]
    s[1] += x[4]
    s[2] += 1
print("| ship | player-runs | ledger torpedo | result torpedo |")
print("|---|---|---|---|")
for ship, (lt, gt, n) in sorted(by_ship.items(), key=lambda kv: -kv[1][1]):
    print(f"| {ship} | {n} | {lt:,.0f} | {gt:,.0f} |")
print("ships with ledger torpedo damage and no torpedo damage in any game result:", [s for s, (lt, gt, n) in by_ship.items() if lt > 0 and gt == 0])

print("\n# 2. Ledger over the game result, by damage type")
L = Counter()
R = Counter()
other_fields = Counter()
for name, (g, sp) in runs.items():
    for rr in sp['reconciliation']:
        for k, v in (rr.get('game_by_type') or {}).items():
            if not (k.startswith('damage_main_') or k.startswith('damage_atba_') or k in ('damage_fire', 'damage_flood', 'damage_ram', 'damage') or k.startswith('damage_tpd')):
                other_fields[k] += v
for x in rows:
    for k, v in x[5].items():
        L[k] += v
    for k, v in x[6].items():
        R[k] += v
print("ledger by kind:", {k: f"{v / 1e6:.1f}M" for k, v in L.items()})
print("result by type:", {k: f"{v / 1e6:.1f}M" for k, v in R.items()})
sf_l = L["shell"] + L["fire"]
sf_r = R["main"] + R["fire"]
print(f"ledger shell+fire {sf_l / 1e6:.1f}M vs result main+fire {sf_r / 1e6:.1f}M: ratio {sf_l / sf_r:.3f}; vs main+secondaries+fire {(sf_r + R['secondaries']) / 1e6:.1f}M: ratio {sf_l / (sf_r + R['secondaries']):.3f}")
print(f"ledger shell {L['shell'] / 1e6:.1f}M vs result main {R['main'] / 1e6:.1f}M (ratio {L['shell'] / R['main']:.3f}); plus secondaries {(R['main'] + R['secondaries']) / 1e6:.1f}M (ratio {L['shell'] / (R['main'] + R['secondaries']):.3f})")
print(f"ledger fire {L['fire'] / 1e6:.1f}M vs result fire {R['fire'] / 1e6:.1f}M (ratio {L['fire'] / R['fire']:.3f})")
print(f"ledger torpedo {L['torpedo'] / 1e6:.1f}M vs result torpedo {R['torpedo'] / 1e6:.1f}M; ledger flood {L['flood'] / 1e6:.2f}M vs result flood {R['flood'] / 1e6:.2f}M; ledger unknown {L['unknown'] / 1e6:.1f}M; result ram {R['ram'] / 1e6:.2f}M, other {R['other'] / 1e6:.2f}M")
tot_res = sum(x[6]['total'] for x in rows)
print("result 'other' fields:", dict(sorted(other_fields.items(), key=lambda kv: -kv[1])[:8]))
amts = sorted(fl(e['amount']) for _, e in same)
print(f"same-tick torpedo events amount: median {amts[len(amts) // 2]:,.0f}; under 3,000: {sum(1 for a in amts if a < 3000)}; under 6,000: {sum(1 for a in amts if a < 6000)}; 6,000 and over: {sum(1 for a in amts if a >= 6000)}")
nohit = sorted(fl(e['amount']) for name, (g, sp) in runs.items() for e in csv.DictReader(open(os.path.join(G, name, 'damage_events.csv'), encoding='utf-8')) if e['kind'] == 'torpedo' and e['fire_source'] != 'ShotHit')
print(f"torpedo events without a shell hit on the tick: {len(nohit)}; amount median {nohit[len(nohit) // 2]:,.0f}; under 3,000: {sum(1 for a in nohit if a < 3000)}; under 6,000: {sum(1 for a in nohit if a < 6000)}")
print("no victim position, top misses:", [(x[0].replace('kots19na_', '')[:40], runs[x[0]][1]['events_no_victim_position'], runs[x[0]][1]['events_by_source']) for x in sorted(miss, key=lambda x: -x[4])[:4]])

print("\nBy run, the shell+fire ratio with secondaries added to the result:")
bands = Counter()
for name, (g, sp) in runs.items():
    l = r = 0.0
    for rr in sp["reconciliation"]:
        lk = rr.get("ledger_by_kind") or {}
        gt = group_types(rr.get("game_by_type") or {})
        l += lk.get("shell", 0) + lk.get("fire", 0)
        r += gt["main"] + gt["secondaries"] + gt["fire"]
    ratio = l / r if r else 0
    for lo, hi in [(0, 0.9), (0.9, 0.98), (0.98, 1.02), (1.02, 1.1), (1.1, 1.25), (1.25, 9)]:
        if lo <= ratio < hi:
            bands[f"{lo}-{hi}"] += 1
print(dict(bands))

print("\n# 2b. Timing: events after the victim's death, and residual duplicates")
after = Counter()
dup = Counter()
total = Counter()
for name, (g, sp) in runs.items():
    deaths = {str(p["entity_id"]): p["death"]["seconds"] for t in g["teams"] for p in t["players"] if p.get("death")}
    ev = list(csv.DictReader(open(os.path.join(G, name, "damage_events.csv"), encoding="utf-8")))
    seen = defaultdict(list)
    for e in ev:
        amt = fl(e["amount"])
        total[e["kind"]] += amt
        d = deaths.get(e["victim"])
        if d is not None and fl(e["damage_s"]) > d + 2.0:
            after[e["kind"]] += amt
        k = (e["attacker"], e["victim"], e["amount"])
        if any(abs(fl(e["damage_s"]) - t0) <= 0.8 for t0 in seen[k]):
            dup[e["kind"]] += amt
        seen[k].append(fl(e["damage_s"]))
print("damage after the victim's death (+2 s), by kind:", {k: f"{v / 1e6:.2f}M" for k, v in after.items()}, "of", {k: f"{v / 1e6:.1f}M" for k, v in total.items()})
print("residual same-amount pairs within 0.8 s (same attacker and victim), by kind:", {k: f"{v / 1e6:.2f}M" for k, v in dup.items()})
