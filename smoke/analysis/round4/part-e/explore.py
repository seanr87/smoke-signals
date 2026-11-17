import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'round3'))); from common import *; S, G = load()
sh = by(S, 'ship')
print('ships 20+:', [(k, len(v)) for k, v in sorted(sh.items(), key=lambda kv: -len(kv[1])) if len(v) >= 20])
print('movement', C(s['movement'] for s in S)); print('coverage', C(s['coverage'] for s in S))
for k in ('Grozovoi', 'Shimakaze', 'Daring', 'Gdańsk'):
    v = sh[k]
    print('\n==', k, len(v), 'clans', C(s['team'] for s in v).most_common())
    print(' players', C((s['team'], s['player']) for s in v).most_common())
    print(' maps', C(s['map'] for s in v).most_common())
    print(' movement', C(s['movement'] for s in v), 'coverage', C(s['coverage'] for s in v), 'selfish', sum(s['selfish'] for s in v))
    print(' edge q', [round(q([s['edge'] for s in v], p)) for p in (.1, .25, .5, .75, .9)], 'inside', sum(s['inside'] for s in v))
    print(' path_m q', [round(q([s['path_m'] for s in v if s['path_m'] is not None], p)) for p in (.1, .25, .5, .75, .9)])
    print(' el q', [round(q([s['el'] for s in v], p)) for p in (.1, .25, .5, .75, .9)])
    print(' pp', C(s['pp'] for s in v).most_common(6))
    print(' mrA', sum(s['mrA'] for s in v), 'kind', C(s['kind'] for s in v))
print()
for k, v in sorted(sh.items(), key=lambda kv: -len(kv[1])):
    if len(v) < 20: continue
    o = [s['obs_emission_s'] for s in v if s['obs_emission_s'] is not None]
    print(f"{k:12s} n={len(v):3d} base={C(s['emission_s'] for s in v).most_common(2)} obsNone={len(v)-len(o)} obs q10/25/50/75/90={[round(q(o,p),1) for p in (.1,.25,.5,.75,.9)]} cut={sum(s['cut_short'] for s in v)} radius={C(round(s['radius_m']) for s in v).most_common(4)} baseR={C(s['r']['base_radius'] for s in v).most_common(3)} variant={C(s['r']['variant'] for s in v).most_common(2)} life={C(s['life_s'] for s in v).most_common(2)}")
# raw rounded distribution for a few
for k in ('Daring', 'Harugumo', 'Gearing', 'Shimakaze', 'Grozovoi'):
    print(k, sorted(C(round(s['obs_emission_s']) for s in sh[k] if s['obs_emission_s'] is not None).items()))
s = sh['Daring'][0]; print({k: s['r'][k] for k in ('t_created', 't_activate', 't_emission_end', 't_capture', 't_dispersed', 'observed_emission_s', 'puff_count', 'movement', 'movement_confidence', 'movement_path_m', 'coverage', 'owner_flag')})
print('owner_flag', C(s['r']['owner_flag'] for s in S))
