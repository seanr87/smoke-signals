import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
S, G = load()
dd = [s for s in S if s['cls'] == 'destroyer']
# cap letter vs position check: for inside-cap smokes, which cap (by geometry) is nearest vs named
for m in MAPS:
    agree = C()
    for s in dd:
        if s['map'] != m: continue
        g = G[s['game']]
        near = min(g['caps'], key=lambda c: math.hypot(c['x'] - s['x'], c['z'] - s['z']) - c['r'])['cap']
        agree[(s['cap'], near)] += 1
    print(m, dict(agree))
    print('   caps differ between games?', len(set(json.dumps(g['caps']) for g in G.values() if g['map'] == m)))
s = next(s for s in dd if s['map'] == 'Sleeping Giant' and s['ncell_name'] == 'G9')
print(s['side'], s['x'], s['z'], s['cap'], s['ncap'], s['r']['cap_proximity_name'], s['r']['nearest_cap_act'], s['r']['cap_state_act'], s['r']['supported_caps'], s['r']['lane'], s['r']['cap_flank'], s['r']['cap_role'])
print(G[s['game']]['j']['caps'])
print({k: v for k, v in G[s['game']]['j'].items() if k not in ('teams', 'caps')}.keys())
