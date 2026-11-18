# Independent recheck (main session) of headline numbers from new-n2 (deaths, radar). Does not use its code.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
S, G = load5(); add_times(S)
D = [s for s in S if s['cls'] == 'destroyer']
def end(s): return s['e1'] if s['e1'] is not None else s['e0'] + (s['emission_s'] or 0) + (s['life_s'] or 0)
trk = batch = 0
for s in D:
    g = TL(s['game']); tr = g.tracks.get(s['smoker_eid'])
    batch += s['d_smoker']
    if tr is None: continue
    d = tr.death_t()
    trk += d is not None and s['e0'] <= d <= end(s) + 22
print('n2 smoking destroyers dead between activation and 20 s after dispersal: tracks', trk, 'batch list', batch, 'of', len(D), f'-> {100*trk/len(D):.1f} per 100')
lit40 = lit20 = tot = named = 0; ships = C()
for s in D:
    g = TL(s['game'])
    for d in s['dead']:
        tr = g.tracks.get(d['eid'])
        if tr is None: continue
        td = tr.death_t()
        if td is None: td = d['t']
        tot += 1
        rows = [r for r in g.lit('radar', target=d['eid']) if r['lit_end_elapsed_s'] >= td - 40 and r['lit_start_elapsed_s'] <= td + 2]
        lit40 += bool(rows); lit20 += any(r['lit_end_elapsed_s'] >= td - 20 for r in rows)
        a = [r for r in rows if r['row'] == 'lit']
        if a: named += 1; ships[a[-1]['ship']] += 1
print('n2 deaths in destroyer smokes', tot, 'radar-lit in last 40 s', lit40, 'last 20 s', lit20, 'radar ship named', named, ships.most_common(4))
