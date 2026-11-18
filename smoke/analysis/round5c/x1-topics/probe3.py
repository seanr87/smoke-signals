import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlib import *
CC = [s for s in DD if 'cap_contest' in s['tags']]
RC = [s for s in CC if s['cover3']=='radar cruiser inside']
c=C()
for s in RC:
    g=TL(s['game']); ro=G[s['game']]['roster']
    acts=[r for r in g.activations('radar', team=s['team']) if s['e0']-1<=r['elapsed_s']<=s['end']+1]
    ins={p['eid'] for p in s['shelter'] if p['how']=='inside' and p['cls']=='cruiser'}
    c['any team radar in window']+= bool(acts)
    c['by cruiser inside (batch)']+= any(r['entity_id'] in ins for r in acts)
    c['lib pressed']+= s['radar_pressed']
    c['any in some smoke']+= any(r['source_in_smoke'] for r in acts)
    # geometric: cruiser within smoke at press
    ok=False
    for r in acts:
        if r['entity_id'] in ins and r['x'] is not None and in_smoke(s,(r['x'],r['z'])): ok=True
    c['cruiser inside geometrically at press']+=ok
    c['early']+=s['early']
print(len(RC), c)
print(RC[0]['shelter'][:3], RC[0]['partners'][:2])
EC=[s for s in DD if s['early'] and s['radar_ca_inside']]
print(len(EC), sum(s['radar_pressed'] for s in EC), sum(s['radar_pressed_by_ca'] for s in EC))
