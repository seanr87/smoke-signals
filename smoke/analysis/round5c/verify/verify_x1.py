# Independent recheck (main session) of headline numbers from x1 (items 1 to 4). Does not use its code.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5clib import *
S, G = load5c()
f = lambda v: '-' if v is None else f'{v:.1f}'
D = [s for s in S if s['cls'] == 'destroyer']
cc = [s for s in D if 'cap_contest' in s['tags']]
print('A1 cap-contest smokes', len(cc))
for grp in ('top', 'rest'):
    for cov in ('radar cruiser inside', 'no cruiser'):
        ss = [s for s in cc if s['grp'] == grp and s['cover3'] == cov]
        print('  ', grp, cov, len(ss), 'we took contested', share(ss, 'we_took_c'), 'nearest', share(ss, 'we_took_n'), 'conc', round(mean(s['conc'] for s in ss)), 'died', f(died100(ss)), 'caught', f(caught100(ss)))
rc = [s for s in cc if s['cover3'] == 'radar cruiser inside']; print('   radar cruiser inside', len(rc), 'radar_pressed', sum(s['radar_pressed'] for s in rc))
for name, test in (('50+ behind', lambda s: s['state'] == 'behind 50+'), ('covered ship radar-lit', lambda s: s['lit_covered'])):
    a = [s for s in D if test(s)]; b = [s for s in D if not test(s)]
    print('A2', name, len(a), 'died', f(died100(a)), 'vs', f(died100(b)), '| caught', f(caught100(a)), 'vs', f(caught100(b)))
calm = [s for s in D if s['state'] != 'behind 50+' and not s['lit_covered']]
print('A2 calm', len(calm), 'died', f(died100(calm)), 'caught', f(caught100(calm)))
def radar(ships):
    l40 = at = 0
    for s, eid, t in ships:
        rows = TL(s['game']).lit('radar', target=eid)
        l40 += any(r['lit_end_elapsed_s'] >= t - 40 and r['lit_start_elapsed_s'] <= t for r in rows)
        at += any(r['lit_start_elapsed_s'] <= t and r['lit_end_elapsed_s'] >= t - 2 for r in rows)
    return len(ships), l40, at
died = [(s, d['eid'], d['t']) for s in D if s['died_ok'] for d in s['died_list']]
start = {k: g['j']['battle_start_s'] for k, g in G.items()}
caught = []
for s in D:
    for d in s['dead']:
        p = G[s['game']]['roster'].get(d['eid'], {})
        if p.get('death'): caught.append((s, d['eid'], p['death']['seconds'] - start[s['game']]))
print('A2 radar deaths (n, lit in last 40 s, lit at death): died', radar(died), '| caught', radar(caught))
for grp in ('top', 'rest'):
    for ship in ('Somers', 'Gearing'):
        ss = [s for s in D if s['grp'] == grp and s['ship'] == ship]; print('A3', grp, ship, len(ss), 'died', f(died100(ss)), 'caught', f(caught100(ss)))
cs = [s for s in D if s['counter_of']]; print('A4 counter-smokes', len(cs), 'died', f(died100(cs)), 'caught', f(caught100(cs)))
