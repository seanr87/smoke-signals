import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5clib import *
import json
S, G = load5c()
DD = [s for s in S if s['cls'] == 'destroyer']
# detection entries: within smoke window? spacing?
late=0; tot=0; pre=0; kinds=C(); gaps=[]
for s in DD:
    j=s['j']; st=run_start(j['match_id'], j['game_no'], j['primary_replay'])
    for x in j['smokees']:
        ds=x.get('detections',[])
        prev={}
        for d in ds:
            t=d['seconds']-st; tot+=1; kinds[d['kind']]+=1
            if t> s['end']+1: late+=1
            if t< s['e0']-1: pre+=1
            if d['kind'] in prev: gaps.append(t-prev[d['kind']])
            prev[d['kind']]=t
print(tot, 'late', late, 'pre', pre, kinds); print(len(gaps))
# sample
n=0
for s in DD:
    j=s['j']; st=run_start(j['match_id'], j['game_no'], j['primary_replay'])
    for x in j['smokees']:
        if len(x.get('detections',[]))>=3 and n<3:
            n+=1; print(s['e0'], s['end'], x['how'], x['seconds_concealed'], x['detected_by'], [(d['kind'], round(d['seconds']-st,1)) for d in x['detections']])
# died ships: start mismatch between runs?
ks=C()
for k,g in G.items():
    rs=[r for r in runs() if r['key']==k]; ks[len(rs)]+=1
print(ks)
# track det at death
c=C(); 
for s in DD:
    g=TL(s['game'])
    for d in s['died_list']:
        tr=g.tracks.get(d['eid'])
        if not tr: c['notrack']+=1; continue
        i=tr.idx(d['t']-0.01); 
        c[(tr.det[i], tr.alive[i], tr.own)]+=1
        dt=tr.death_t()
        c['dt_diff_%d'%round((dt or 0)-d['t'])]+=1
print(c)
