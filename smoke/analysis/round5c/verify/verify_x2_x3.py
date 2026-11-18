# Independent recheck (main session) of headline numbers from x2 (items 5 to 7) and x3 (item 8). Does not use their code.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5clib import *
S, G = load5c()
f = lambda v: '-' if v is None else f'{v:.1f}'
it = [s for s in S if s['ship'] in ('Napoli', 'Venezia')]; oc = [s for s in S if s['cls'] == 'cruiser' and s['kind'] != 'exhaust']; bb = [s for s in S if s['cls'] == 'battleship']
print('B2 smoker died / caught per 100: Italian cruisers', len(it), f(died_smoker100(it)), f(caught_smoker100(it)), '| ordinary cruiser smoke', len(oc), f(died_smoker100(oc)), f(caught_smoker100(oc)),
      '| battleships', len(bb), f(died100(bb)), f(caught100(bb)))
lg = [s for s in S if s['ship'] in ('Somers', 'Gearing', 'Harugumo', 'Delny')]
for grp in ('top', 'rest'):
    ss = [s for s in lg if s['grp'] == grp]; print('B3 long smokes', grp, len(ss), 'died', f(died100(ss)), 'caught', f(caught100(ss)))
g1 = [s for s in S if s['cls'] == 'destroyer' and s['map'] == 'Sleeping Giant' and s['ncell_name'] == 'G1']
print('item 7 Sleeping Giant G1', len(g1), 'we took nearest', share(g1, 'we_took_n'), 'contested', share(g1, 'we_took_c'), '| enemy took nearest', share(g1, 'enemy_took_n'),
      sum(1 for s in g1 if s['enemy_took_n']), 'contested', share(g1, 'enemy_took_c'), sum(1 for s in g1 if s['enemy_took_c']))
for grp in ('top', 'rest'):
    ss = [s for s in S if s['grp'] == grp]
    print('D1', grp, len(ss), 'died', f(died100(ss)), 'caught', f(caught100(ss)), 'smoker died', f(died_smoker100(ss)), 'smoker caught', f(caught_smoker100(ss)),
          'nearest cap taken', share(ss, 'we_took_n'), 'contested', share(ss, 'we_took_c'))
