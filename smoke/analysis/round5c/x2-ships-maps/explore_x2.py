import sys, os, json, time; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5clib import *
t=time.time()
S, G = load5c()
print('load', time.time()-t, len(S))
DD=[s for s in S if s['cls']=='destroyer']
print(len(DD), sum(s['grp']=='top' for s in DD), sum(s['early'] for s in DD), death_rates(DD))
print(C(s['died_ok'] for s in S))
# spots
sp = json.load(open(os.path.join(R5C,'..','round5b','spots.json'),encoding='utf-8'))
print(type(sp), (list(sp.keys()) if isinstance(sp,dict) else len(sp)))
L = sp['spots'] if isinstance(sp,dict) else sp
for x in L:
    if x.get('id') in ('sg-cell-1','hs-cell-1','sof-cell-1','c5-lp-f8','c5-lp-f10','c5-lp-sitters-b','c5-mr-radar-b'):
        print({k:v for k,v in x.items() if k not in ('cruisers','examples','cruisers_by_how')})
# membership
for m,cells in (('Sleeping Giant',['G1']),('Hotspot',['G10','H10']),('Sea of Fortune',['F9','G9']),('Loop',['F8']),('Loop',['F10'])):
    v=[s for s in DD if s['map']==m and s['ncell_name'] in cells]; print(m,cells,len(v), round(mean(s['conc'] for s in v)))
sg=[s for s in S if s['map']=='Sleeping Giant']
print('SG near', len([s for s in sg if s['near_cap_edge_m']<=2000]), C(s['near_ncap'] for s in sg if s['near_cap_edge_m']<=2000))
mr=[s for s in S if s['map']=='Mountain Range']
rad=lambda s: s['radar_play'] or bool(s['off_radar'])
print('MR radar B', len([s for s in mr if rad(s) and s['near_ncap']=='B']), len([s for s in mr if rad(s) and s['near_ncap']=='B' and s['near_cap_edge_m']<=2000]), 'pressed', len([s for s in mr if s['radar_pressed'] and s['near_ncap']=='B']), len([s for s in mr if s['radar_pressed'] and s['near_ncap']=='B' and s['near_cap_edge_m']<=2000]))
# track det
s=S[0]; tr=TL(s['game']).tracks.get(s['smoker_eid']); print(tr.t[:5], C(tr.det), tr.own)
none=0
for s in S:
    tr=TL(s['game']).tracks.get(s['smoker_eid'])
    if tr is None: none+=1
print('no track', none, 'no smoker', sum(s['smoker_eid'] is None for s in S))
print(os.path.exists(os.path.join(R5C,'..','round4','part-b','spots.json')))
