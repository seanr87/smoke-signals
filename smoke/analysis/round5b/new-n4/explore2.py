import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
S, G = load5(); add_times(S)
ids=C((s['game'],s['id']) for s in S); print('dup ids', sum(v>1 for v in ids.values()))
idx={(s['game'],int(s['id'])):s for s in S}
miss=0; other=0; tot=0; multi=0; cls=C(); own=C()
for k in G:
    g=TL(k)
    for a in g.activations('radar'):
        if a['source_in_smoke']:
            tot+=1; multi+=len(a['source_in_smoke'])>1
            for i in a['source_in_smoke']:
                s=idx.get((k,i))
                if not s: miss+=1; continue
                if s['team']!=a['team']: other+=1
                cls[(s['cls'], s['smoker_eid']==a['entity_id'])]+=1
                own[s['e0']<=a['elapsed_s']<=(s['e1'] or s['e0']+s['emission_s']+s['life_s'])]+=1
print(tot,miss,other,multi,cls,own)
print('cap empty', sum(not s['cap'] for s in S), 'cap_won vals', C(s['r']['cap_won'] for s in S).most_common(5))
s=next(s for s in S if s['r']['cap_won']); print(s['r']['cap_won'], s['j']['cap_won'], s['j']['cap_won_at'], s['cap'], s['j']['supported_caps'], s['e0'], s['e1'])
print(s['j']['offensive_radar'], s['j']['radar_cap'])
s=next(s for s in S if s['j']['offensive_radar']); print(s['j']['offensive_radar'], s['j']['radar_cap'], s['r']['radar_spotted_damage'])
# damage events two runs compare
rs=by(runs(),'key'); k=next(iter(rs)); import csv
for r in rs[k]:
    rows=list(csv.DictReader(open(os.path.join(GAMES_DIR,r['dir'],'damage_events.csv'),encoding='utf-8')))
    print(r['dir'], len(rows), sum(float(x['amount']) for x in rows), C(x['kind'] for x in rows), C(x['credited'] for x in rows))
    ro=G[k]['roster']; print(C((ro[int(x['victim'])]['team']) for x in rows))
print(G[k]['j']['primary_replay'], [r['primary_replay'] for r in rs[k]])
print(C(len(v) for v in rs.values()))
