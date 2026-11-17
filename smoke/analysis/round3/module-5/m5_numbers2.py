import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5lib import *
from m5_cluster import *
print('ids unique', len({s['id'] for s in S}), len(S))
byid = {s['id']: s for s in S}
# counter within kind
for kind in ('long DD', 'short DD'):
    ss = [s for s in DD if s['kind'] == kind]
    a, b = [s for s in ss if s['counter_of']], [s for s in ss if not s['counter_of']]
    dif = lambda ss, fn: (fn([s for s in ss if s['counter_of']]) - fn([s for s in ss if not s['counter_of']])) if any(s['counter_of'] for s in ss) else None
    print(kind, 'counter', len(a), k(conc_per(a)), f1(d100(a)), 'not', len(b), k(conc_per(b)), f1(d100(b)), 'diff', ci(boot_stat(ss, lambda v: dif(v, conc_per))), ci(boot_stat(ss, lambda v: dif(v, d100)), '{:+.1f}'))
cs = [s for s in DD if s['counter_of']]
print('counter coverage', C(s['coverage'] for s in cs), 'movement', C(s['movement'] for s in cs), 'band', C(band(s['edge']) for s in cs))
print('same cap as answered', pct(cs, lambda s: s['cap'] == byid[s['counter_of']]['cap']), 'gap q', q([s['el'] - byid[s['counter_of']]['el'] for s in cs], .25), q([s['el'] - byid[s['counter_of']]['el'] for s in cs], .75))
print('counter by map top/rest', {m: C(s['grp'] for s in v) for m, v in by(cs, 'map').items()})
# chains with path-based distance
def pdist(a, b): return min(math.hypot(x1 - x2, z1 - z2) for x1, z1 in a['path'] for x2, z2 in b['path']) * WU
for lim in (500, 1000, 1500):
    ch = chains(S, lim, 60)
    inch = {s['id'] for v in ch for s in v}
    a, b = [s for s in DD if s['id'] in inch], [s for s in DD if s['id'] not in inch]
    print('lim', lim, 'chains', len(ch), C(len(v) for v in ch), 'DD in', len(a), k(conc_per(a)), f1(d100(a)), 'capwon', f1(pct(a, lambda s: s['cap_won'])), 'solo', len(b), k(conc_per(b)), f1(d100(b)), f1(pct(b, lambda s: s['cap_won'])),
          'cls mix', C(tuple(sorted(C(s['cls'] for s in v).items())) for v in ch).most_common(4), 'same player', sum(1 for v in ch if len({s['player'] for s in v}) == 1))
ch = chains(S, 1000, 60); inch = {s['id'] for v in ch for s in v}
dif3 = lambda ss, fn: (fn([s for s in ss if s['id'] in inch]) - fn([s for s in ss if s['id'] not in inch])) if any(s['id'] in inch for s in ss) else None
print('chain - solo: conc', ci(boot_stat(DD, lambda ss: dif3(ss, conc_per))), 'd100', ci(boot_stat(DD, lambda ss: dif3(ss, d100)), '{:+.1f}'))
print('chain conc total per chain', k(mean(sum(s['conc'] for s in v) for v in ch)), 'deaths per 100 chains', f1(100 * sum(s['deaths'] for v in ch for s in v) / len(ch)))
print('by clan', C(v[0]['team'] for v in ch).most_common(10), 'by map', C(v[0]['map'] for v in ch), 'grp', C(v[0]['grp'] for v in ch))
print('per team-game: top', len([v for v in ch if v[0]['grp'] == 'top']) / sum(NG[t] for t in NG if t in TOP), 'rest', len([v for v in ch if v[0]['grp'] == 'rest']) / sum(NG[t] for t in NG if t not in TOP))
print('chain ships', C(tuple(sorted(s['ship'] for s in v)) for v in ch).most_common(8))
print('chain gap', med(v[-1]['el'] - v[0]['el'] for v in ch), 'time', med(v[0]['el'] for v in ch), 'band', C(band(min(s['edge'] for s in v)) for v in ch), 'win', pct(ch, lambda v: v[0]['win']))

print('=== 5 clusters')
clans, feats, X, Z = features()
print(len(clans), clans)
for i, c in enumerate(clans): print(c.ljust(6), NG[c], WL[c], ' '.join(f'{v:6.2f}' for v in X[i]))
print(feats)
merges, order = agglomerate(Z)
print([clans[i] for i in order])
for kcl in (3, 4, 5):
    lab = cut(merges, len(clans), kcl)
    print(kcl, {l: [clans[i] for i in range(len(clans)) if lab[i] == l] for l in sorted(set(lab))})
h = clans.index('H-SR')
print('nearest to H-SR', sorted(((round(dist(Z[h], Z[i]), 2), c) for i, c in enumerate(clans) if c != 'H-SR'))[:8])
print('farthest', sorted(((round(dist(Z[h], Z[i]), 2), c) for i, c in enumerate(clans) if c != 'H-SR'))[-4:])
p = clans.index('PN')
print('nearest to PN', sorted(((round(dist(Z[p], Z[i]), 2), c) for i, c in enumerate(clans) if c != 'PN'))[:6], 'PN-HSR', dist(Z[p], Z[h]))
print('H-SR z', [(f, round(Z[h][j], 1)) for j, f in enumerate(feats)])
print('PN z', [(f, round(Z[p][j], 1)) for j, f in enumerate(feats)])
tops = [i for i, c in enumerate(clans) if c in TOP]
print('mean dist among top', mean(dist(Z[a], Z[b]) for a in tops for b in tops if a < b), 'overall', mean(dist(Z[a], Z[b]) for a in range(len(clans)) for b in range(a)))
# does distance to H-SR track win rate?
wr = [WL[c][0] / NG[c] for c in clans]; dh = [dist(Z[h], Z[i]) for i in range(len(clans))]
idx = [i for i in range(len(clans)) if i != h]
mx, my = mean(wr[i] for i in idx), mean(dh[i] for i in idx)
r = sum((wr[i] - mx) * (dh[i] - my) for i in idx) / math.sqrt(sum((wr[i] - mx) ** 2 for i in idx) * sum((dh[i] - my) ** 2 for i in idx))
print('corr(win rate, distance to H-SR)', round(r, 2), 'n', len(idx))
