import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
S, G = load5(); add_times(S)
print(len(S), len(G), BATCH)
E=[s for s in S if s['ship'] in ('Harugumo','Somers','Gearing') and s['el']<300]
print('E',len(E), pct(E,lambda s:s['inside']), med(s['edge'] for s in E))
DDE=[s for s in S if s['cls']=='destroyer' and s['el']<300]
print('DDE',len(DDE), C((s['grp'],s['radar_ca_inside']) for s in DDE))
print('early_cruiser', C((s['grp'],s['early_mode']) for s in S if s['early_cruiser']))
print('plays', C((s['cls'],s['grp'],s['pp']) for s in S if s['radar_play']))
s=E[0]; g=TL(s['game'])
print(s['e0'],s['ecap'],s['eend'],s['e1'],s['el'],s['emission_s'],s['life_s'], s['j'].keys())
print([ (k,v) for k,v in s['r'].items()][:60])
a=g.activations('radar'); print(len(a)); print(a[0]); print(g.lit('radar')[0])
print(g.caps); print(g.frame)
print(g.ribbons[:3])
tr=next(iter(g.tracks.values())); print(tr.eid,tr.team,tr.ship,tr.t[:5],tr.x[:3],tr.hp[:3])
print(list(G[s['game']]['roster'].items())[:1])
print(G[s['game']]['caps'])
print(runs()[0]['dir'], runs()[0]['start'])
print(s['j']['smokees'][:2])
print('e1 None', sum(s['e1'] is None for s in S), 'e0 none', sum(s['e0'] is None for s in S))
import statistics
print('el-e0 diff', statistics.quantiles([s['el']-s['e0'] for s in S], n=10))
n=0; ins=0
for k in G:
    g=TL(k)
    for a in g.activations('radar'):
        n+=1; ins+= bool(a['source_in_smoke'])
print('radar act', n, ins)
