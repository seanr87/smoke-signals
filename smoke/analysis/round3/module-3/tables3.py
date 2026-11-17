# Round 4: radar cruiser inside the smoke (common.py radar_ca_inside), early destroyer smokes.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m3lib import *
P = print
def table(pop, key, label):
    f = lambda x: pct(x, lambda s: s[key])
    P(f'\n{label}')
    for m in ['ALL'] + MAPORDER:
        ss = pop if m == 'ALL' else [s for s in pop if s['map'] == m]
        a = [s for s in ss if s['grp'] == 'top']; b = [s for s in ss if s['grp'] == 'rest']
        lo, hi = boot_diff(ss, f)
        P(f'  {m}: top {sum(s[key] for s in a)} of {len(a)} ({n0(f(a))}%){small(len(a))} | rest {sum(s[key] for s in b)} of {len(b)} ({n0(f(b))}%){small(len(b))} | diff {sg(f(a) - f(b)) if a and b else "-"} CI {"-" if lo is None else f"{lo:+.1f} to {hi:+.1f}"}')
    pn = [s for s in pop if s['is_pn']]
    P(f'  PN: {sum(s[key] for s in pn)} of {len(pn)}')
early = [s for s in DD if s['early']]
es = [s for s in early if s['stack']]
table(early, 'radar_ca_inside', '(a) HEADLINE radar cruiser inside, ALL early DD smokes')
table(es, 'radar_ca_inside', '(b) HEADLINE radar cruiser inside, early STACKED DD smokes')
table(es, 'radar_in', 'old Module 3: radar ship of any class inside, early stacked DD smokes')
table([s for s in early if s['ship'] in ('Harugumo', 'Somers', 'Gearing')], 'radar_ca_any', 'old Module 2: radar cruiser covered any way, early smokes by Harugumo/Somers/Gearing')
P('\nships of early DD smokes', C(s['ship'] for s in early).most_common())
P('Sleeping Giant early stacks, Top 6: radar_in but not radar_ca_inside:', [(s['team'], [(p['ship'], p['cls'], p['how']) for p in s['partners'] if p['radar']]) for s in es if s['map'] == 'Sleeping Giant' and s['radar_in'] != s['radar_ca_inside']])
P('all early stacks where the two differ:', C((s['grp'], s['map']) for s in es if s['radar_in'] != s['radar_ca_inside']))
for pop, lab in ((early, 'all early'), (es, 'early stacked')):
    for k in (True, False):
        ss = [s for s in pop if s['radar_ca_inside'] == k]; tk = [s for s in ss if s['own'] in ('neutral', 'theirs')]
        P(f'{lab} radar_ca_inside={k}: n={len(ss)} cap taken {pct(tk, lambda s: s["cap_won"]):.0f}% of {len(tk)} conc mean {mean(s["conc"] for s in ss):,.0f}')
    d = lambda x: (pct([s for s in x if s['radar_ca_inside'] and s['own'] != 'ours'], lambda s: s['cap_won']) - pct([s for s in x if not s['radar_ca_inside'] and s['own'] != 'ours'], lambda s: s['cap_won'])) if any(s['radar_ca_inside'] and s['own'] != 'ours' for s in x) and any(not s['radar_ca_inside'] and s['own'] != 'ours' for s in x) else None
    P('   cap taken diff', round(d(pop), 1), ci(boot_stat(pop, d), '{:+.1f}'))
P('SG west flank (ncap A) early stacks: top', [(s['radar_ca_inside']) for s in es if s['map'] == 'Sleeping Giant' and s['grp'] == 'top' and s['ncap'] == 'A'].count(True), 'of', sum(1 for s in es if s['map'] == 'Sleeping Giant' and s['grp'] == 'top' and s['ncap'] == 'A'),
  '| rest', sum(s['radar_ca_inside'] for s in es if s['map'] == 'Sleeping Giant' and s['grp'] == 'rest' and s['ncap'] == 'A'), 'of', sum(1 for s in es if s['map'] == 'Sleeping Giant' and s['grp'] == 'rest' and s['ncap'] == 'A'))
P('SG by ncap, all early, top/rest with/total:', {(c, g): (sum(s['radar_ca_inside'] for s in early if s['map'] == 'Sleeping Giant' and s['ncap'] == c and s['grp'] == g), sum(1 for s in early if s['map'] == 'Sleeping Giant' and s['ncap'] == c and s['grp'] == g)) for c in 'ABC' for g in ('top', 'rest')})
P('Hotspot by ncap, all early:', {(c, g): (sum(s['radar_ca_inside'] for s in early if s['map'] == 'Hotspot' and s['ncap'] == c and s['grp'] == g), sum(1 for s in early if s['map'] == 'Hotspot' and s['ncap'] == c and s['grp'] == g)) for c in 'ABCD' for g in ('top', 'rest')})
