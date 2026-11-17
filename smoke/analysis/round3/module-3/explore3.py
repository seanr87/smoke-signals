import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m3lib import *
for m in MAPORDER:
    print(m, C(tuple((c['cap'], round(c['x']), round(c['z']), round(c['r'] * 30)) for c in g['caps']) for g in G.values() if g['map'] == m))
for s in DD:
    if s['play'] and s['map'] == 'Sleeping Giant' and s['ncell'][0] >= 5:
        print(s['side'], s['cap'], s['ncap'], s['ncell_name'], round(s['edge']), s['play'], s['r']['cap_contested_reason'], s['r']['supported_caps'], s['r']['cap_state_act'])
