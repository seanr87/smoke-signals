import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m4lib import *
OUT = os.path.dirname(os.path.abspath(__file__))
r1 = lambda x: None if x is None else round(x, 1)
rows = []
for m in MAP_ORDER:
    ms, avg, cells = map_cells(m)
    tt = [s for s in ms if s['grp'] == 'top']; rr = [s for s in ms if s['grp'] == 'rest']
    def rec(kind, name, x, pred, flag):
        return dict(map=m, kind=kind, name=name, n=x['n'], concealed_damage_per_smoke=round(x['conc']), median_concealed_damage=round(x['med']),
                    deaths_per_100=r1(x['d100']), cap_won_pct=r1(x['capw']), flag=flag, small_n=x['n'] < SOLID_N, rated=x['n'] >= MIN_N,
                    top6_share_pct=r1(pct(tt, pred)), rest_share_pct=r1(pct(rr, pred)), top6_n=x['top'], rest_n=x['n'] - x['top'],
                    map_avg_concealed_damage=round(avg), map_smokes=len(ms))
    for c, x in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if x['rated']: rows.append(rec('cell', cell_name(*c), x, lambda s, c=c: s['ncell'] == c, x['mark'] or 'none'))
    for z, v in sorted(by(ms, 'zone').items()):
        rows.append(rec('zone', z, stats(v), lambda s, z=z: s['zone'] == z, 'none'))
doc = dict(batch=BATCH_NAME, scope='destroyer smokes, team-normalized (own spawn at the bottom; Okinawa bottom left)',
           notes=dict(min_n=MIN_N, small_n_below=SOLID_N, high=f'cell concealed damage per smoke >= {HIGH_X} x map average', low=f'<= {LOW_X} x map average',
                      zone='every smoke assigned to its nearest cap (distance to cap edge); zones are not flagged high/low; a zone with rated=false has fewer than 8 smokes',
                      shares='share of each group\'s destroyer smokes on that map laid in the cell or zone', caveat='association only, not cause'),
           rows=rows)
json.dump(doc, open(os.path.join(OUT, 'cells.json'), 'w', encoding='utf-8'), indent=1)
print('rows', len(rows), 'cells', sum(r['kind'] == 'cell' for r in rows), 'zones', sum(r['kind'] == 'zone' for r in rows))
# extras quoted in the write-up
hs = [s for s in DD if s['map'] == 'Hotspot']
d = [s for s in hs if s['zone'] == 'D']; o = [s for s in hs if s['zone'] != 'D']
print('Hotspot D', len(d), k(conc(d)), 'elsewhere', k(conc(o)), 'share', 100 * len(d) / len(hs))
w = lambda s: s['zone'] in 'AB'
print('Hotspot west share top/rest', pct([s for s in hs if s['grp'] == 'top'], w), pct([s for s in hs if s['grp'] == 'rest'], w), 'n', sum(w(s) for s in hs), k(conc([s for s in hs if w(s)])))
low = [s for s in hs if s['ncell_name'] in ('F5', 'G5', 'F6', 'F9')]; print('Hotspot low4', len(low), k(conc(low)))
lf = [s for s in DD if s['map'] == 'Land of Fire']; b = [s for s in lf if s['ncell_name'] in ('F5', 'F6')]
print('LoF F5+F6', len(b), k(conc(b)), capw(b))
