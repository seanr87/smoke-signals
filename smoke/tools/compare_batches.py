"""Before/after comparison of two batches.

python -I -X utf8 compare.py <repo root> <before batch> <after batch>
"""
import csv, json, os, sys
from collections import Counter, defaultdict

ROOT, BEFORE, AFTER = sys.argv[1:4]
inv = list(csv.DictReader(open(os.path.join(ROOT, "smoke", "inventory.csv"), encoding="utf-8")))
games_of = Counter()
for r in inv:
    if r["status"] == "played":
        for t in r["teams"].split(" vs "):
            games_of[t] += 1


def fl(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


def load(d):
    return list(csv.DictReader(open(os.path.join(d, "smokes.csv"), encoding="utf-8")))


b, a = load(BEFORE), load(AFTER)
print(f"rows before {len(b)}, after {len(a)}")
print("\n# Concealed damage per game, before and after, every clan")
print("| clan | games | smokes before | smokes after | concealed/game before | after | change |")
print("|---|---|---|---|---|---|---|")
rows = []
for t in games_of:
    bb = [r for r in b if r["team"] == t]
    aa = [r for r in a if r["team"] == t]
    g = games_of[t]
    cb = sum(fl(r["smoke_damage_concealed"]) for r in bb) / g
    ca = sum(fl(r["smoke_damage_concealed"]) for r in aa) / g
    rows.append((t, g, len(bb), len(aa), cb, ca))
for t, g, nb, na, cb, ca in sorted(rows, key=lambda x: -x[5]):
    mark = " <-" if t in ("INCA", "KM", "BONKZ", "HFANS") else ""
    print(f"| {t}{mark} | {g} | {nb} | {na} | {cb:,.0f} | {ca:,.0f} | {100 * (ca - cb) / cb if cb else 0:+.0f}% |")

print("\n# Smoke of the Tournament candidates (top 8 by concealed damage, ties by total)")
for label, rs in (("before", b), ("after", a)):
    print(f"\n{label}:")
    print("| # | smoke | team | player | ship | game | clock | concealed | total | one-sided |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(sorted(rs, key=lambda r: (-fl(r["smoke_damage_concealed"]), -fl(r["smoke_damage_total"])))[:8], 1):
        print(f"| {i} | {r['smoke_id']} | {r['team']} | {r['player'].replace('_KOTS19NA', '')} | {r['ship']} | {r['round'].replace('Groups / ', '').replace('Playoffs / ', '')} vs {r['opponent']} g{r['game_no']} ({r['map_display']}) | {r['t_activate_clock']} | {fl(r['smoke_damage_concealed']):,.0f} | {fl(r['smoke_damage_total']):,.0f} | {r.get('one_sided', '')} |")

print("\n# Flags")
for label, rs in (("before", b), ("after", a)):
    f = [r for r in rs if r["owner_flag"].lower() == "true"]
    kinds = Counter()
    for r in f:
        n = r["owner_note"]
        for k in ("no smoke activation", "nearest ship", "minimap", "inferred"):
            if k in n:
                kinds[k] += 1
    print(f"{label}: flagged {len(f)} of {len(rs)} ({100 * len(f) / len(rs):.1f}%); {dict(kinds)}")

print("\n# Damage kinds across all runs")
for label, d in (("before", BEFORE), ("after", AFTER)):
    c = Counter()
    dmg = Counter()
    ratios = []
    for run in os.listdir(os.path.join(d, "games")):
        p = os.path.join(d, "games", run, "damage_spike.json")
        if os.path.exists(p):
            s = json.load(open(p, encoding="utf-8"))
            for k, v in s["events_by_kind"].items():
                c[k] += v
            for k, v in s["damage_by_kind"].items():
                dmg[k] += v
            if s.get("reconciliation_ratio_shell_fire") is not None:
                ratios.append(s["reconciliation_ratio_shell_fire"])
    ratios.sort()
    print(f"{label}: events {dict(c)}; damage {{" + ", ".join(f"{k}: {v / 1e6:.1f}M" for k, v in dmg.items()) + f"}}; shell+fire ratio median {ratios[len(ratios) // 2]:.3f}, within 2%: {sum(1 for r in ratios if abs(r - 1) <= 0.02)} of {len(ratios)}, over 1.25: {sum(1 for r in ratios if r > 1.25)}")

print("\n# Shooters credited above their own shell+fire result")
for label, d in (("before", BEFORE), ("after", AFTER)):
    over = 0
    excess = 0.0
    tot = 0.0
    for run in os.listdir(os.path.join(d, "games")):
        p = os.path.join(d, "games", run, "damage_spike.json")
        sp = os.path.join(d, "games", run, "smokes.json")
        if not (os.path.exists(p) and os.path.exists(sp)):
            continue
        s = json.load(open(p, encoding="utf-8"))
        sj = json.load(open(sp, encoding="utf-8"))["smokes"]
        led = {x["player"]: x for x in s["reconciliation"]}
        credit = Counter()
        for sm in sj:
            for sh in sm.get("shooter_detail") or []:
                credit[sh["player"]] += sh.get("damage") or 0
        for pl, cr in credit.items():
            tot += cr
            res = led.get(pl, {}).get("game_shell_fire") or 0
            if cr > res * 1.05 + 100:
                over += 1
                excess += cr - res
    print(f"{label}: {over} shooter-runs, excess {excess:,.0f} of {tot:,.0f} credited ({100 * excess / tot if tot else 0:.1f}%)")
