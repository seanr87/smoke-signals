import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m4lib import *
random.seed(4)
print('games without winner', sum(g['winner'] is None for g in G.values()))

def first_owners(gk):
    """{cap: (el, owner)} first observed owner of each cap, from smoke-time snapshots (approximate)."""
    out = {}
    for el, sc, caps in snapshots(S, gk):
        for c, o in caps.items():
            if o and c not in out: out[c] = (el, o)
    return out
def owner_at(gk, t):
    """{cap: owner} at the last snapshot at or before t seconds, or None if no snapshot yet."""
    last = None
    for el, sc, caps in snapshots(S, gk):
        if el <= t: last = caps
    return last

FO = {gk: first_owners(gk) for gk in G}
for m in MAP_ORDER:
    gs = [g for g in G.values() if g['map'] == m and g['winner']]
    print(f'\n== {m} ({len(gs)} games with a winner)')
    # which cap is taken first in the game (real letters; ties count for each)
    firstcap = C(); tfirst = collections.defaultdict(list)
    recs = collections.defaultdict(list)       # real cap -> records of first owner
    trecs = collections.defaultdict(list)      # normalized cap -> records for team whose FIRST cap it was
    for g in gs:
        fo = FO[g['key']]
        if not fo: continue
        t0 = min(el for el, o in fo.values())
        for c, (el, o) in fo.items():
            if el == t0: firstcap[c] += 1
            recs[c].append(dict(team=o, win=o == g['winner'], el=el))
        for t in g['teams']:
            mine = [(el, c) for c, (el, o) in fo.items() if o == t]
            if not mine: trecs['none'].append(dict(team=t, win=t == g['winner'])); continue
            e0 = min(mine)[0]
            for el, c in mine:
                if el == e0: trecs[ncap_name(g, m, g['sides'][t], c)].append(dict(team=t, win=t == g['winner']))
    print('  first cap taken in the game (ties counted for each):', dict(firstcap))
    for c in sorted(recs):
        v = recs[c]; f = lambda x: pct(x, lambda r: r['win'])
        print(f"  cap {c} (real letter): first observed owner won the game {f(v):.0f}% of {len(v)} games, 95% {ci(boot_stat(v, f), '{:.0f}')}; median first-owned at {med(r['el'] for r in v):.0f}s")
    for c in sorted(trecs):
        v = trecs[c]; f = lambda x: pct(x, lambda r: r['win'])
        print(f"  team's first cap = {c} (normalized letter): won {f(v):.0f}% of {len(v)} team-games, 95% {ci(boot_stat(v, f), '{:.0f}')}")
    # owners at 8 minutes: win rate of the holder of each cap (normalized letter per team)
    hold = collections.defaultdict(list)
    for g in gs:
        ow = owner_at(g['key'], 480)
        if not ow: continue
        for c, o in ow.items():
            if o: hold[ncap_name(g, m, g['sides'][o], c)].append(dict(team=o, win=o == g['winner']))
    for c in sorted(hold):
        v = hold[c]; f = lambda x: pct(x, lambda r: r['win'])
        print(f"  holder of cap {c} (normalized) at about 8:00 elapsed won {f(v):.0f}% of {len(v)}, 95% {ci(boot_stat(v, f), '{:.0f}')}")
    # where each team's first DD smoke goes, and early smokes by zone
    ms = [s for s in DD if s['map'] == m]
    firsts = [min(v, key=lambda s: s['el']) for v in by(ms, lambda s: (s['game'], s['team'])).values()]
    print('  first DD smoke of each team-game by zone:', dict(C(s['zone'] for s in firsts)), 'n', len(firsts), '| median el', med(s['el'] for s in firsts))
    for z, v in sorted(by(firsts, 'zone').items()):
        print(f"     first smoke at {z}: n {len(v)} team won {pct(v, lambda s: s['win']):.0f}% conc {k(conc(v))} top {sum(s['grp']=='top' for s in v)}")
    early = [s for s in ms if s['el'] <= 240]
    for z, v in sorted(by(early, 'zone').items()):
        late = [s for s in ms if s['zone'] == z and s['el'] > 240]
        print(f"     zone {z}: first 4 min n {len(v)} conc {k(conc(v))} d100 {d100(v):.0f} capwon {capw(v):.0f}% | later n {len(late)} conc {k(conc(late)) if late else '-'} d100 {d100(late) if late else 0:.0f} capwon {capw(late) if late else 0:.0f}%")

# Sleeping Giant extras: early A-side cell G1
sg = [s for s in DD if s['map'] == 'Sleeping Giant']
g1 = [s for s in sg if s['ncell_name'] == 'G1']
print('\nSG G1 by time:', [(round(s['el']), round(s['conc']), s['team'], s['win']) for s in sorted(g1, key=lambda s: s['el'])])
print('SG G1 ships', dict(C(s['ship'] for s in g1)), 'kinds', dict(C(s['kind'] for s in g1)), 'pp', dict(C(s['pp'] for s in g1)), 'torp share', sum(s['torp'] for s in g1) / max(1, sum(s['total'] for s in g1)))
print('SG G1 partners/smoke', mean(len(s['partners']) for s in g1), 'vs map', mean(len(s['partners']) for s in sg), '| shooters cls', dict(C(x['cls'] for s in g1 for x in s['shooters'] if x['conc'] > 0)))
print('SG G1 conc by smoker vs partners', sum(x['conc'] for s in g1 for x in s['shooters'] if x['is_smoker']), sum(x['conc'] for s in g1 for x in s['shooters'] if not x['is_smoker']))
aw = [s for s in sg if s['zone'] == 'A']
print('SG zone A: early(<=240) n', sum(s['el'] <= 240 for s in aw), 'of', len(aw))
# team-game level: did the team smoke G1/E1 in the game -> win
tg = by(sg, lambda s: (s['game'], s['team']))
a = [dict(team=kk[1], win=v[0]['win']) for kk, v in tg.items() if any(s['ncell_name'] in ('G1', 'E1') for s in v)]
b = [dict(team=kk[1], win=v[0]['win']) for kk, v in tg.items() if not any(s['ncell_name'] in ('G1', 'E1') for s in v)]
print('SG team-games with a G1/E1 smoke: won', pct(a, lambda r: r['win']), 'of', len(a), '| without', pct(b, lambda r: r['win']), 'of', len(b))
# Hotspot: D zone by side-of-cap cells, and team-game D share vs win
hs = [s for s in DD if s['map'] == 'Hotspot']
tg = by(hs, lambda s: (s['game'], s['team']))
w = [pct(v, lambda s: s['zone'] == 'D') for v in tg.values() if v[0]['win']]; l = [pct(v, lambda s: s['zone'] == 'D') for v in tg.values() if not v[0]['win']]
print('Hotspot: mean share of a team-game DD smokes in zone D, winners', mean(w), len(w), 'losers', mean(l), len(l))
dz = [s for s in hs if s['zone'] == 'D']
print('Hotspot D zone pp', dict(C(s['pp'] for s in dz)), 'cells', dict(C(s['ncell_name'] for s in dz)))
near = [s for s in dz if s['ncell_name'] in ('G10', 'F10', 'H10')]; oth = [s for s in dz if s not in near]
print('Hotspot D own-side edge (F10,G10,H10) n', len(near), k(conc(near)), 'd100', d100(near), 'capw', capw(near), '| other D n', len(oth), k(conc(oth)), d100(oth), capw(oth))
print('  col 10 vs rest of map', ci(in_out_ci(hs, lambda s: s['ncell_name'] in ('G10', 'F10', 'H10'))))
# Land of Fire: B
lf = [s for s in DD if s['map'] == 'Land of Fire']
tg = by(lf, lambda s: (s['game'], s['team']))
w = [pct(v, lambda s: s['zone'] == 'B') for v in tg.values() if v[0]['win']]; l = [pct(v, lambda s: s['zone'] == 'B') for v in tg.values() if not v[0]['win']]
print('LoF: mean share of team-game DD smokes in zone B, winners', mean(w), len(w), 'losers', mean(l), len(l))
bz = [s for s in lf if s['zone'] == 'B']
print('LoF B zone win% of smokes', pct(bz, lambda s: s['win']), 'A', pct([s for s in lf if s['zone'] == 'A'], lambda s: s['win']), 'cells', dict(C(s['ncell_name'] for s in bz)))
print('LoF B capwon by win', capw([s for s in bz if s['win']]), capw([s for s in bz if not s['win']]))
print('LoF F6 teams', dict(C(s['team'] for s in lf if s['ncell_name'] == 'F6')))
for nm, ms in (('PN', [s for s in DD if s['is_pn']]),):
    print(nm, [(s['map'], s['ncell_name'], s['zone'], round(s['conc']), s['deaths'], s['cap_won']) for s in ms])
