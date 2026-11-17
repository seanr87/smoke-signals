import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
S, G = load()
dd = [s for s in S if s['cls'] == 'destroyer']
print('dd', len(dd), 'games', len(G))
gm = C(g['map'] for g in G.values())
for m in sorted(MAPS, key=lambda m: -gm[m]):
    ms = [s for s in dd if s['map'] == m]
    print('\n==', m, 'games', gm[m], 'dd smokes', len(ms), 'top', sum(s['grp'] == 'top' for s in ms), 'pn', sum(s['is_pn'] for s in ms),
          'caps', [(c['cap'], round(c['x']), round(c['z']), round(c['r'])) for c in map_caps(G, m)], 'size', MAPS[m]['space_size'])
    print('  overall conc/smoke', round(mean(s['conc'] for s in ms)), 'deaths/100', round(100 * mean(s['deaths'] for s in ms), 1), 'capwon', round(pct(ms, lambda s: s['cap_won'])),
          'win', round(pct(ms, lambda s: s['win'])), 'ncap', dict(C(s['ncap'] for s in ms)))
    cells = by(ms, 'ncell_name')
    for k, v in sorted(cells.items(), key=lambda kv: -len(kv[1])):
        if len(v) < 5: continue
        print('  ', k, 'n', len(v), 'conc', round(mean(s['conc'] for s in v)), 'med', round(med(s['conc'] for s in v)), 'd100', round(100 * mean(s['deaths'] for s in v)),
              'capwon', round(pct(v, lambda s: s['cap_won'])), 'top%', round(pct(v, lambda s: s['grp'] == 'top')), 'win%', round(pct(v, lambda s: s['win'])),
              'clans', len(set(s['team'] for s in v)), 'games', len(set(s['game'] for s in v)), 'el', round(med(s['el'] for s in v)), 'ncap', dict(C(s['ncap'] for s in v)))
# sample snapshot
k = next(iter(G)); sn = snapshots(S, k)
print(k, G[k]['map'], G[k]['teams'], G[k]['winner'], G[k]['sides'], G[k]['len'])
for x in sn[:8]: print(x)
print(dd[0]['r'].keys())
