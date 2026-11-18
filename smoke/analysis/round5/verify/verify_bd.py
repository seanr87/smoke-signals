# Independent recheck of headline numbers from parts B and D (written by the main session).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
S, G = load5()
def p(v): return '-' if v is None else f'{v:.1f}'
for ship in ('Daring', 'Gdańsk'):
    ss = [s for s in S if s['ship'] == ship]
    tm = lambda s: s['j']['classification']['coverage']['stacked'] or s['j']['classification']['coverage']['screen']
    print('B1', ship, len(ss), 'med edge', round(med(s['edge'] for s in ss)), 'inside', p(pct(ss, lambda s: s['inside'])), 'teammate', p(pct(ss, tm)), 'conc', round(mean(s['conc'] for s in ss)))
it = [s for s in S if s['ship'] in ('Napoli', 'Venezia')]; oc = [s for s in S if s['cls'] == 'cruiser' and s['kind'] != 'exhaust']
print('B2 italian cruisers', len(it), 'smoker died /100', p(rate100(it, 'd_smoker')), '| ordinary cruiser smoke', len(oc), p(rate100(oc, 'd_smoker')), '| all', p(rate100(S, 'd_smoker')))
for ship in ('Harugumo', 'Somers', 'Gearing'):
    ss = [s for s in S if s['ship'] == ship]
    own = sum(x['conc'] for s in ss for x in s['shooters'] if x['is_smoker']); tot = sum(x['conc'] for s in ss for x in s['shooters'])
    print('B3', ship, len(ss), 'own-gun share', p(100 * own / tot), 'conc', round(mean(s['conc'] for s in ss)))
for ship in ('Shimakaze', 'Grozovoi'):
    ss = [s for s in S if s['ship'] == ship and s['path_m'] is not None]
    print('B4', ship, len(ss), 'bands <500/500-1k/1k+', sum(s['path_m'] < 500 for s in ss), sum(500 <= s['path_m'] < 1000 for s in ss), sum(s['path_m'] >= 1000 for s in ss))
# D: radar cruiser inside, smoke cruisers per game
D = [s for s in S if s['cls'] == 'destroyer']
print('D1 radar cruiser inside dd smokes: top', p(pct([s for s in D if s['grp']=='top'], lambda s: s['radar_ca_inside'])), 'rest', p(pct([s for s in D if s['grp']=='rest'], lambda s: s['radar_ca_inside'])))
def smoke_cr(teams):
    n = c = 0
    for g in G.values():
        for t in g['teams']:
            if t not in teams: continue
            n += 1; c += sum(1 for pl in g['roster'].values() if pl['team'] == t and pl['ship_class'] == 'Cruiser' and pl.get('smoke_type'))
    return c / n, n
print('D2 smoke cruisers per game H-SR/RESIN/BONKZ', smoke_cr({'H-SR','RESIN','BONKZ'}), 'HTDOG/VRTUS', smoke_cr({'HTDOG','VRTUS'}))
for t in ('H-SR', 'HTDOG', 'VRTUS', 'PN'):
    ss = [s for s in S if s['team'] == t]; ng = sum(1 for g in G.values() if t in g['teams'])
    print('D3', t, 'games', ng, 'smokes/game', p(len(ss)/ng), 'teammate', p(pct(ss, tm)), 'parked', p(pct(ss, lambda s: s['movement']=='stationary')), 'conc/game', round(sum(s['conc'] for s in ss)/ng))
