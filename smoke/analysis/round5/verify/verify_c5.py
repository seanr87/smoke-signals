# Independent recheck of headline numbers from part C5 (written by the main session).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
S, G = load5()
def p(v): return '-' if v is None else f'{v:.1f}'
for grp in ('top', 'rest'):
    ss = [s for s in S if s['map']=='Sleeping Giant' and s['ship']=='Somers' and s['grp']==grp]
    late = [s for s in ss if s['el'] >= 300]
    print('SG Somers', grp, len(ss), 'west', p(pct(ss, lambda s: s['nx'] < 0)), '| after 5:00 west', sum(s['nx']<0 for s in late), 'of', len(late))
    hs = [s for s in S if s['map']=='Hotspot' and s['cls']=='destroyer' and s['grp']==grp]
    print('HS dd', grp, len(hs), 'contested cap A or B (normalized)', p(pct(hs, lambda s: s['ncap'] in 'AB')), 'early radar ca inside', p(pct([s for s in hs if s['el']<300], lambda s: s['radar_ca_inside'])), len([s for s in hs if s['el']<300]))
for m in sorted({g['map'] for g in G.values()}):
    tg = [(k, t) for k, t in team_games(G) if G[k]['map'] == m]
    e = [s for s in S if s['map']==m and s['cls']=='destroyer' and s['el']<300]
    print('early dd smokes per team-game', m, p(len(e)/len(tg)*10), '/10', len(tg))
ok = C(s['ship'] for s in S if s['map']=='Okinawa'); print('Okinawa', ok.most_common(5))
