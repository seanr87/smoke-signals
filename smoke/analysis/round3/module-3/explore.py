import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
S, G = load()
print('cls x pp radar tags')
for cls in ('destroyer', 'cruiser', 'battleship'):
    ss = [s for s in S if s['cls'] == cls]
    print(cls, len(ss), 'cap_control', sum('cap_control' in s['tags'] for s in ss), 'radar_trap any', sum('radar_trap' in s['tags'] for s in ss),
          'pp trap', sum(s['pp'] == 'radar_trap' for s in ss), 'off_radar', sum(bool(s['off_radar']) for s in ss), 'radar_cap', sum(bool(s['radar_cap']) for s in ss),
          'smoker_radar', sum(s['smoker_radar'] for s in ss))
ex = next(s for s in S if 'cap_control' in s['tags'])
print(json.dumps(ex['radar_cap']), json.dumps(ex['off_radar']))
print({k: ex['r'][k] for k in ex['r'] if 'radar' in k})
print([k for k in ex['j'].keys()])
print(json.dumps(ex['j']['classification'])[:800])
print(json.dumps(ex['j']['smokees'][:2])[:900])
for k in ex['j']:
    if 'radar' in k: print(k, json.dumps(ex['j'][k])[:600])
R = [s for s in S if 'cap_control' in s['tags'] or 'radar_trap' in s['tags']]
print('radar plays', len(R), C((s['cls'], s['grp']) for s in R))
print('by map', C((s['map'], s['cls']) for s in R))
print('by team', C(s['team'] for s in R))
print('radar ship', C((s['radar_cap'] or s['off_radar'] or {}).get('ship') for s in R))
print('off_radar inferred', C((s['off_radar'] or {}).get('inferred') for s in S if s['off_radar']))
print('off spotted dist', C((s['off_radar'] or {}).get('enemies_spotted') for s in S if s['off_radar']))
print('radar_cap activated/full', C((s['radar_cap']['activated'], s['radar_cap']['full']) for s in S if s['radar_cap']))
print('rsd nonzero', sum(1 for s in S if F(s['r']['radar_spotted_damage'])), 'of off', sum(1 for s in S if s['off_radar']))
print('stack', C((s['coverage'], s['cls']) for s in S))
print('radar ships in roster', C(p['ship'] for g in G.values() for p in g['roster'].values() if p.get('radar_m')))
print('games per map', C(g['map'] for g in G.values()))
print('radar_on_us', C(s['radar_on_us'] > 0 for s in S))
print(list(ex['r'].keys()))
