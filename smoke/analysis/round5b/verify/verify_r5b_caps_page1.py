# Independent recheck (main session) of headline numbers from new-n1 (caps) and new-n4 (page 1). Does not use their code.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
S, G = load5(); add_times(S)
during = within = n = 0
for s in S:
    g = TL(s['game']); cap = s['near_cap']; t0 = s['e0']
    t1 = s['e1'] if s['e1'] is not None else t0 + (s['emission_s'] or 0) + (s['life_s'] or 0)
    if g.owner_at(cap, t0) == s['opponent']: continue
    n += 1
    ch = [t for t, o in g.owner_changes(cap, t0, t1 + 60) if o == s['opponent']]
    during += any(t <= t1 for t in ch); within += bool(ch)
print('n1 enemy took nearest cap: applicable', n, 'during', during, 'during or within 60 s', within, f'{100*within/n:.1f}%')
# cap leader at exactly 8:00
won = tot = short = 0
for k, g in G.items():
    t = TL(k); a, b = g['teams']
    end = max(tr.t[-1] for tr in t.tracks.values())
    if g['len'] is not None and g['len'] < 480: short += 1; continue
    c = C(t.owner_at(cap, 480) for cap in t.caps)
    if c[a] == c[b]: continue
    tot += 1; won += g['winner'] == (a if c[a] > c[b] else b)
print('n1 C2: games ended before 8:00', short, '| team with more caps at 8:00 won', won, 'of', tot, f'{100*won/tot:.0f}%')
# radar presses from inside an allied smoke
tg = C(); 
for k, g in G.items():
    for t in g['teams']: tg['top' if t in TOP else 'rest'] += 1
p = C()
for k in G:
    for r in TL(k).activations('radar'):
        if r['source_in_smoke']: p['top' if r['team'] in TOP else 'rest'] += 1
print('n4 radar presses from inside a smoke', sum(p.values()), dict(p), 'per team-game top', round(p['top']/tg['top'], 2), 'rest', round(p['rest']/tg['rest'], 2), dict(tg))
allr = C('top' if r['team'] in TOP else 'rest' for k in G for r in TL(k).activations('radar'))
print('n4 all radar presses per team-game top', round(allr['top']/tg['top'], 1), 'rest', round(allr['rest']/tg['rest'], 1))
D = [s for s in S if s['cls'] == 'destroyer' and s['el'] < 300]
for grp in ('top', 'rest'):
    ss = [s for s in D if s['grp'] == grp]; print('n4 early dd smokes', grp, len(ss), 'radar cruiser inside', sum(s['radar_ca_inside'] for s in ss))
