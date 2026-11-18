import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5clib import *
import json
S, G = load5c()
DD = [s for s in S if s['cls'] == 'destroyer']
print(len(S), len(DD), sum(s['early'] for s in DD), death_rates(DD))
s = next(s for s in DD if s['died_list'] and s['dead'])
print(s['died_list'], [ {k:v for k,v in d.items() if k not in ('killers',)} for d in s['dead']])
print(json.dumps(s['j']['smokees'][0], default=str)[:1500])
print(s['j']['smoke_deaths'][0])
print(sorted(s['r'].keys()))
print(sorted(k for k in s.keys()))
g = TL(s['game']); print(g.lit('radar')[:1]); print(G[s['game']]['j']['battle_start_s'], s['e0'], s['j']['t_activate'])
print(C(s['cover3'] for s in DD if 'cap_contest' in s['tags']), C(s['state'] for s in DD), C(s['map'] for s in DD))
print(C(r['row']+r['kind'] for k in G for r in TL(k).sensor))
