import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m3lib import *
s = max((s for s in DD if s['spots'] >= 2), key=lambda s: s['conc'])
j = s['j']
for k in ('offensive_radar', 'radar_cap', 'cap_denial', 'targets_hit', 'targets_not_counted', 'damage_split', 'radar_spotted_damage', 'cap_won', 'cap_won_at', 'supported_caps'):
    print(k, json.dumps(j.get(k))[:700])
print('damage_detail', json.dumps(j['damage_detail'])[:1500])
print('shooter_detail', json.dumps(j['shooter_detail'])[:900])
print('csv', {k: s['r'][k] for k in ('enemies_near_cap_before', 'enemies_near_cap_during', 'cap_won', 'cap_won_clock', 'cap_defended', 'cap_contested_reason', 'cap_role', 'detected_damage_by')})
g = G[s['game']]['j']
print('game keys', list(g.keys()))
for k in g:
    if any(w in k.lower() for w in ('radar', 'consum', 'event', 'detect')): print(k, json.dumps(g[k])[:600])
print(DD[0]['r']['cap_defended'], C(s['r']['cap_defended'] for s in S), C(s['r']['cap_won'] != '' for s in S))
print('cap_denial ex', [json.dumps(x['j'].get('cap_denial'))[:300] for x in DD if x['cc']][:3])
