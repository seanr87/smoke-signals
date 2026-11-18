# Independent recheck (main session) of the Loop Daring test from new-n3. Does not use its code.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
S, G = load5(); add_times(S)
ss = [s for s in S if s['map'] == 'Loop' and s['ship'] == 'Daring']
def after_radar(s, w):
    g = TL(s['game']); ro = G[s['game']]['roster']
    for r in g.lit('radar', include_unattributed=False):
        if r['team'] != s['team'] or r['target_team'] != s['opponent']: continue
        if (ro.get(r['target_entity_id'], {}).get('ship_class') or '').lower() != 'destroyer': continue
        if r['lit_start_elapsed_s'] <= s['e0'] and r['lit_end_elapsed_s'] >= s['e0'] - w: return True
    return False
for w in (30, 60, 90):
    print('Loop Daring smokes', len(ss), f'within {w} s after a friendly radar lit an enemy destroyer:', sum(after_radar(s, w) for s in ss))
hs = [s for s in S if s['ship'] == 'Harugumo']
print('Harugumo smokes', len(hs))
