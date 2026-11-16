"""STEP 2b outlier audit over the full-field batch.

python -I -X utf8 audit.py <repo root> <batch dir> <round 6 batch dir>
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict

ROOT, NEW, R6 = sys.argv[1:4]
ORIG = {"H-SR", "RESIN", "PN"}
GAMES = os.path.join(NEW, "games")


def fl(x):
    try:
        return float(x or 0)
    except ValueError:
        return 0.0


inv = list(csv.DictReader(open(os.path.join(ROOT, "smoke", "inventory.csv"), encoding="utf-8")))
played = [r for r in inv if r["status"] == "played"]
games_of = Counter()
for r in played:
    for t in r["teams"].split(" vs "):
        games_of[t] += 1

rows = list(csv.DictReader(open(os.path.join(NEW, "smokes.csv"), encoding="utf-8")))
old = list(csv.DictReader(open(os.path.join(R6, "smokes.csv"), encoding="utf-8")))
by_team = defaultdict(list)
for r in rows:
    by_team[r["team"]].append(r)

# run folder of a smoke: games/<folder>_<slug(team)>
runs = {}
for name in os.listdir(GAMES):
    p = os.path.join(GAMES, name, "game.json")
    if os.path.exists(p):
        g = json.load(open(p, encoding="utf-8"))
        runs[name] = g


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


def run_of(r):
    mid = r["match_id"].replace("kots19na_", "")
    for name, g in runs.items():
        if g["match_id"] == r["match_id"] and str(g["game_no"]) == r["game_no"] and name.endswith("_" + slug(r["team"])):
            return name
    return None


def short_game(r):
    return f"{r['round'].replace('Groups / ', '').replace('Playoffs / ', '')} {r['team']} vs {r['opponent']} g{r['game_no']} ({r['map_display']})"


print("# 1. -BN- and INCA")
for team in ("-BN-", "INCA"):
    rs = by_team[team]
    g = games_of[team]
    conc = sum(fl(r["smoke_damage_concealed"]) for r in rs)
    tot = sum(fl(r["smoke_damage_total"]) for r in rs)
    print(f"\n## {team}: {g} games, {len(rs)} smokes, concealed {conc:,.0f} ({conc / g:,.0f}/game), total {tot:,.0f} ({tot / g:,.0f}/game)")
    print("\nTop 10 smokes by concealed damage:")
    print("| # | game | clock | smoker | ship | concealed | detected | total | shooters | flag | overlap |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(sorted(rs, key=lambda r: -fl(r["smoke_damage_concealed"]))[:10], 1):
        shooters = r["shooters"].replace("_KOTS19NA", "")
        print(f"| {i} | {short_game(r)} | {r['t_activate_clock']} | {r['player'].replace('_KOTS19NA', '')} | {r['ship']} | {fl(r['smoke_damage_concealed']):,.0f} | {fl(r['smoke_damage_detected']):,.0f} | {fl(r['smoke_damage_total']):,.0f} | {shooters} | {r['owner_note'] or '-'} | {r['overlap_flag']} |")

    # Reconcile per game: credit per shooter across the clan's smokes vs the ledger and the game results.
    print(f"\nPer-game reconciliation ({team}: smoke credit per shooter vs that shooter's ledger shell+fire and the game's own result):")
    print("| game | smokes | smoke dmg total | clan ledger shell+fire | clan game result shell+fire | credit/ledger | max shooter credit/ledger | over-credited shooters | dup events dropped | events per replay |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    per_game = defaultdict(list)
    for r in rs:
        per_game[(r["match_id"], r["game_no"])].append(r)
    worst = []
    for key, grs in sorted(per_game.items(), key=lambda x: (int(x[0][0].split("_")[1]), int(x[0][1]))):
        run = run_of(grs[0])
        d = os.path.join(GAMES, run)
        spike = json.load(open(os.path.join(d, "damage_spike.json"), encoding="utf-8"))
        sj = json.load(open(os.path.join(d, "smokes.json"), encoding="utf-8"))["smokes"]
        credit = Counter()
        for s in sj:
            if s["team"] != team:
                continue
            for sh in s.get("shooter_detail") or []:
                credit[sh["player"]] += fl(sh.get("damage"))
        ledger = {x["player"]: x for x in spike["reconciliation"]}
        g = runs[run]
        clan_players = [p["player"] for t in g["teams"] if t["name"] == team for p in t["players"]]
        clan_ledger = sum(fl(ledger[p]["ledger_shell_fire"]) for p in clan_players if p in ledger)
        clan_game = sum(fl(ledger[p]["game_shell_fire"]) for p in clan_players if p in ledger)
        smoke_total = sum(fl(r["smoke_damage_total"]) for r in grs)
        ratios = []
        over = []
        for p, c in credit.items():
            l = fl(ledger.get(p, {}).get("ledger_shell_fire"))
            if l > 0:
                ratios.append(c / l)
            if c > l + 1:
                over.append(f"{p.replace('_KOTS19NA', '')} {c:,.0f}>{l:,.0f}")
        print(f"| {short_game(grs[0])} | {len(grs)} | {smoke_total:,.0f} | {clan_ledger:,.0f} | {clan_game:,.0f} | {smoke_total / clan_ledger if clan_ledger else 0:.2f} | {max(ratios) if ratios else 0:.2f} | {'; '.join(over) or '-'} | {spike['events_dropped_as_duplicates']} | {spike['events_per_replay']} |")
        # event-level check: shares per event sum to at most 1
        ev = list(csv.DictReader(open(os.path.join(d, "damage_events.csv"), encoding="utf-8")))
        bad = 0
        for e in ev:
            if e["credited"]:
                share = sum(float(x.split(":")[1]) for x in e["credited"].split(";") if x)
                if share > 1.0001:
                    bad += 1
        if bad:
            print(f"  events credited more than once in full: {bad}")
        worst.append((smoke_total / clan_ledger if clan_ledger else 0, short_game(grs[0])))

print()
print("# 2. Flags")


def flag_types(note):
    kinds = []
    if "no smoke activation" in note:
        kinds.append("no activation within 5 s")
    if "nearest ship" in note:
        kinds.append("nearest ship over 600 m")
    if "minimap" in note:
        kinds.append("position from minimap only")
    if "no ship with" in note:
        kinds.append("no fitted ship with a position")
    return kinds or (["other: " + note] if note else [])


def dist(r):
    return fl(r["owner_distance_m"])


flagged = [r for r in rows if r["owner_flag"].lower() == "true"]
print(f"flagged: {len(flagged)} of {len(rows)} ({100 * len(flagged) / len(rows):.1f}%)")
print("\nBy flag type (a smoke can carry two):")
ft = Counter()
for r in flagged:
    for k in flag_types(r["owner_note"]):
        ft[k] += 1
combos = Counter("; ".join(flag_types(r["owner_note"])) for r in flagged)
for k, n in ft.most_common():
    print(f"- {k}: {n}")
print("Combinations:")
for k, n in combos.most_common():
    print(f"- {k}: {n}")

print("\nBy original 3 vs the other 27 clans:")
for label, pred in (("original 3", lambda t: t in ORIG), ("other 27", lambda t: t not in ORIG)):
    sub = [r for r in rows if pred(r["team"])]
    f = [r for r in sub if r["owner_flag"].lower() == "true"]
    c = Counter()
    for r in f:
        for k in flag_types(r["owner_note"]):
            c[k] += 1
    print(f"- {label}: {len(f)} of {len(sub)} ({100 * len(f) / len(sub):.1f}%); {dict(c)}")
oldf = [r for r in old if r["owner_flag"].lower() == "true"]
print(f"- round 6 for comparison: {len(oldf)} of {len(old)} ({100 * len(oldf) / len(old):.1f}%)")

print("\nDistance of the attributed ship from the smoke origin, flagged smokes:")
bins = [(0, 600), (600, 1000), (1000, 2000), (2000, 5000), (5000, 10000), (10000, 1e9)]
for lo, hi in bins:
    n = sum(1 for r in flagged if lo <= dist(r) < hi)
    print(f"- {lo:.0f} to {hi if hi < 1e9 else 'inf'} m: {n}")
print("Same, for smokes flagged only 'no activation within 5 s' (nearest ship within 600 m):")
only_act = [r for r in flagged if flag_types(r["owner_note"]) == ["no activation within 5 s"]]
print(f"- count {len(only_act)}; distance max {max((dist(r) for r in only_act), default=0):.0f} m")

print("\nBy clan:")
print("| clan | original | smokes | flagged | % | no activation only | over 600 m | over 5 km | minimap |")
print("|---|---|---|---|---|---|---|---|---|")
for t in sorted(games_of, key=lambda t: -len(by_team[t])):
    rs = by_team[t]
    f = [r for r in rs if r["owner_flag"].lower() == "true"]
    far = sum(1 for r in f if dist(r) > 600)
    vfar = sum(1 for r in f if dist(r) > 5000)
    mm = sum(1 for r in f if "minimap" in r["owner_note"])
    oa = sum(1 for r in f if flag_types(r["owner_note"]) == ["no activation within 5 s"])
    print(f"| {t} | {'yes' if t in ORIG else ''} | {len(rs)} | {len(f)} | {100 * len(f) / len(rs) if rs else 0:.0f} | {oa} | {far} | {vfar} | {mm} |")

print("\n## MACH flagged smokes")
print("| smoke | game | clock | smoker | ship | charge | note | dist m | concealed |")
print("|---|---|---|---|---|---|---|---|---|")
for r in sorted(by_team["MACH"], key=lambda r: (int(r["match_id"].split("_")[1]), int(r["game_no"]), fl(r["t_activate"]))):
    if r["owner_flag"].lower() == "true":
        print(f"| {r['smoke_id']} | {short_game(r)} | {r['t_activate_clock']} | {r['player'].replace('_KOTS19NA', '')} | {r['ship']} | {r['charge_no']}/{r['charges_total']} | {r['owner_note']} | {dist(r):.0f} | {fl(r['smoke_damage_concealed']):,.0f} |")

print("\n## Attribution checks")
# (a) a ship credited with more smokes than it carries charges
per_ship = Counter((r["match_id"], r["game_no"], r["team"], r["player"]) for r in rows)
charges = {}
for r in rows:
    charges[(r["match_id"], r["game_no"], r["team"], r["player"])] = (r["charges_total"], r["ship"])
over = [(k, n, charges[k]) for k, n in per_ship.items() if charges[k][0] and n > int(charges[k][0])]
print(f"ships credited with more smokes than charges carried: {len(over)}")
for k, n, (c, ship) in sorted(over):
    rs = [r for r in rows if (r["match_id"], r["game_no"], r["team"], r["player"]) == k]
    fl_n = sum(1 for r in rs if r["owner_flag"].lower() == "true")
    print(f"- {short_game(rs[0])}: {k[3].replace('_KOTS19NA', '')} {ship}: {n} smokes, {c} charges, {fl_n} flagged, notes: {Counter(r['owner_note'] for r in rs).most_common(3)}")
# (b) flagged smokes attributed far from any ship: the smoke starts at the ship, so > 2 km cannot be right
far = [r for r in flagged if dist(r) > 2000]
print(f"\nflagged smokes with the attributed ship more than 2 km from the origin (cannot be the owner): {len(far)}")
print("| smoke | game | clock | attributed to | ship | dist m | merged replays | concealed | total |")
print("|---|---|---|---|---|---|---|---|---|")
for r in sorted(far, key=lambda r: -dist(r)):
    print(f"| {r['smoke_id']} | {short_game(r)} | {r['t_activate_clock']} | {r['player'].replace('_KOTS19NA', '')} | {r['ship']} | {dist(r):.0f} | {len([m for m in r['merged_replays'].split(';') if m])} | {fl(r['smoke_damage_concealed']):,.0f} | {fl(r['smoke_damage_total']):,.0f} |")
# (c) distribution of distance for the 600 m note in two-replay games
two = [r for r in flagged if "nearest ship" in r["owner_note"] and r["merged_replays"]]
print(f"\n'nearest ship over 600 m' smokes in two-replay games: {len(two)}; distances: " + ", ".join(f"{lo}-{hi}: {sum(1 for r in two if lo <= dist(r) < hi)}" for lo, hi in [(600, 830), (830, 1000), (1000, 2000), (2000, 1e9)]))
print("their concealed damage total:", f"{sum(fl(r['smoke_damage_concealed']) for r in two):,.0f}")
# (d) smoke types of the attributed ship for flagged smokes vs observed emission
print("\nflagged smokes by attributed smoke type:", Counter(r["smoke_type"] for r in flagged))
print("all smokes by smoke type:", Counter(r["smoke_type"] for r in rows))

print()
print("# 3. KSE and RMN")
for team in ("KSE", "RMN"):
    rs = by_team[team]
    g = games_of[team]
    print(f"\n## {team}: {g} games, {len(rs)} smokes ({len(rs) / g:.1f}/game)")
    print("smoker class:", dict(Counter(r["smoker_class"] for r in rs)))
    print("coverage:", dict(Counter(r["coverage"] for r in rs)))
    print("primary purpose:", dict(Counter(r["primary_purpose"] for r in rs)))
    print("ships:", dict(Counter(r["ship"] for r in rs)))
    conc = sum(fl(r["smoke_damage_concealed"]) for r in rs)
    tot = sum(fl(r["smoke_damage_total"]) for r in rs)
    print(f"concealed {conc:,.0f} ({conc / g:,.0f}/game, {conc / len(rs):,.0f}/smoke); total {tot:,.0f}; smokes with any damage: {sum(1 for r in rs if fl(r['smoke_damage_total']) > 0)}; with 20k+: {sum(1 for r in rs if fl(r['smoke_damage_total']) >= 20000)}")
    print("| game | result | smokes | smoke dmg | clan ledger shell+fire | clan game result | ledger ratio (game) | events per replay | truncated |")
    print("|---|---|---|---|---|---|---|---|---|")
    for inv_r in played:
        if team not in inv_r["teams"].split(" vs "):
            continue
        mid = f"kots19na_{inv_r['match_id']}"
        run = next((n for n, gg in runs.items() if gg["match_id"] == mid and str(gg["game_no"]) == inv_r["game_no"] and n.endswith("_" + slug(team))), None)
        if not run:
            print(f"| {inv_r['teams']} g{inv_r['game_no']} | no run |")
            continue
        d = os.path.join(GAMES, run)
        spike = json.load(open(os.path.join(d, "damage_spike.json"), encoding="utf-8"))
        gg = runs[run]
        ledger = {x["player"]: x for x in spike["reconciliation"]}
        clan_players = [p["player"] for t in gg["teams"] if t["name"] == team for p in t["players"]]
        clan_ledger = sum(fl(ledger[p]["ledger_shell_fire"]) for p in clan_players if p in ledger)
        clan_game = sum(fl(ledger[p]["game_shell_fire"]) for p in clan_players if p in ledger)
        grs = [r for r in rs if r["match_id"] == mid and r["game_no"] == inv_r["game_no"]]
        smoke_total = sum(fl(r["smoke_damage_total"]) for r in grs)
        won = "W" if inv_r["winner"] == team else "L"
        print(f"| {inv_r['round']} vs {[t for t in inv_r['teams'].split(' vs ') if t != team][0]} g{inv_r['game_no']} ({inv_r['map']}) | {won} {inv_r['score']} | {len(grs)} | {smoke_total:,.0f} | {clan_ledger:,.0f} | {clan_game:,.0f} | {spike['reconciliation_ratio']:.2f} | {spike['events_per_replay']} | {gg['replay_truncated']} |")

print("\nFor scale, concealed damage per game and smokes per game, all clans:")
print("| clan | games | smokes | smokes/game | concealed/game | damage smokes (20k+) |")
print("|---|---|---|---|---|---|")
for t in sorted(games_of, key=lambda t: -sum(fl(r["smoke_damage_concealed"]) for r in by_team[t]) / games_of[t]):
    rs = by_team[t]
    print(f"| {t} | {games_of[t]} | {len(rs)} | {len(rs) / games_of[t]:.1f} | {sum(fl(r['smoke_damage_concealed']) for r in rs) / games_of[t]:,.0f} | {sum(1 for r in rs if fl(r['smoke_damage_total']) >= 20000)} |")

print()
print("# 4. Single-replay game LB R1 KSC vs -BN- G3")
run = "kots19na_playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g3_bn"
g = runs[run]
for t in g["teams"]:
    print(f"team {t['name']}: ships with a smoke fit known: {sum(1 for p in t['players'] if p.get('smoke_type'))} of {len(t['players'])}; activations {sum(p.get('smoke_activations') or 0 for p in t['players'])}; charges {sum(p.get('smoke_charges') or 0 for p in t['players'])}")
    for p in t["players"]:
        print(f"  {p['player'].replace('_KOTS19NA', '')} {p['ship']} {p['ship_class']} type={p.get('smoke_type')} act={p.get('smoke_activations')} charges={p.get('smoke_charges')}")
sj = json.load(open(os.path.join(GAMES, run, "smokes.json"), encoding="utf-8"))["smokes"]
print("smokes in the run and their attribution:")
for s in sj:
    print(f"  {s['smoke_id']} {s['team']} {s['player'].replace('_KOTS19NA', '')} {s['ship']} dist={s['owner_distance_m']} note={s['owner_note'] or '-'} concealed={s['damage_split']['concealed']:.0f} total={s['smoke_damage_total']:.0f} origin={s['origin_xy']}")
