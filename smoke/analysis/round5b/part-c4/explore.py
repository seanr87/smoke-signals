import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
S, G = load5()
print(len(S), C(s['cls'] for s in S))
for m in MAPS:
    ms=[s for s in S if s['map']==m]
    dd=[s for s in ms if s['cls']=='destroyer']
    f=lambda ss: f"{sum(s['grp']=='top' for s in ss)}/{sum(s['grp']=='rest' for s in ss)}"
    print(m, 'space', MAPS[m]['space_size'], 'games', sum(g['map']==m for g in G.values()), 'dd', f(dd), 'long', f([s for s in dd if s['ship'] in LONG_SHIPS]),
          'sit', f([s for s in ms if s['ship'] in SITTERS]), 'park', f([s for s in ms if s['ship'] in ('Svea','Jinan')]), 'early', f([s for s in ms if s['early_cruiser']]),
          'mode', C(s['early_mode'] for s in ms if s['early_cruiser']))
print(C((s['ship'],s['cls']) for s in S if s['ship'] in SITTERS+('Svea','Jinan')+LONG_SHIPS))
print('selfish', C((s['habit'], s['selfish']) for s in S))
print('we_took', C(s['we_took'] for s in S if s['cls']=='destroyer'))
print(len({s['team'] for s in S}), sorted(C(s['team'] for s in S if s['grp']=='rest').items(), key=lambda x:-x[1]))
