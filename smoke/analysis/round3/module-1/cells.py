# Module 1: the cell shares quoted in finding 2 of MODULE-1.md. Output saved to cells.txt.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from m1 import *
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); out.append(line); print(line)
def show(label, ss, m, cells):
    ss = [s for s in ss if s['map'] == m]; k = sum(s['ncell_name'] in cells for s in ss)
    P(f'{label} on {m}: {"/".join(cells)} = {k} of {len(ss)} = {100*k/len(ss):.1f}%')
FL = [s for s in S if s['habit'] == 'flank smoke lines']; CS = [s for s in S if s['habit'] == 'cap sitters']
P('habit counts', dict(C(s['habit'] for s in S)))
show('flank smoke lines', FL, 'Hotspot', ['G10']); show('flank smoke lines', FL, 'Hotspot', ['G9', 'G10', 'F10'])
show('cap sitters', CS, 'Hotspot', ['F5', 'F6', 'G5', 'G6'])
show('flank smoke lines', FL, 'Sleeping Giant', ['G1']); show('flank smoke lines', FL, 'Sleeping Giant', ['E1', 'F1', 'G1', 'G2'])
show('cap sitters', CS, 'Sleeping Giant', ['F5', 'F6', 'G6'])
show('Daring', BY['Daring'], 'Loop', ['F4']); show('flank smoke lines', FL, 'Loop', ['F8']); show('flank smoke lines', FL, 'Loop', ['F10'])
show('Daring', BY['Daring'], 'Land of Fire', ['F5', 'F6']); show('Somers', BY['Somers'], 'Land of Fire', ['G1', 'F1'])
open(os.path.join(OUT, 'cells.txt'), 'w', encoding='utf-8').write('\n'.join(out))
