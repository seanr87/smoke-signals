# Module 1 extra intervals for the location findings and cluster contrasts. Output saved to extras.txt.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from m1 import *
random.seed(19); out = []
def P(*a):
    line = ' '.join(str(x) for x in a); out.append(line); print(line)
west = lambda ss: share(ss, lambda s: s['nx'] < 0)
def cellshare(cells): return lambda ss: share(ss, lambda s: s['ncell_name'] in cells)
def cmp(sh, m, nm, fn, f='{:+.0f}'):
    ss = [s for s in BY[sh] if s['map'] == m]; a = [s for s in ss if s['grp'] == 'top']; b = [s for s in ss if s['grp'] == 'rest']
    P(f'{sh} on {m}: {nm}: top {fn(a):.0f} (n={len(a)}, {len({s["team"] for s in a})} clans) rest {fn(b):.0f} (n={len(b)}, {len({s["team"] for s in b})} clans) diff {f.format(fn(a)-fn(b))} [{ci(boot_diff(ss, fn, reps=1000), f)}]')
P('## West-half share (% of smokes with centre west of the map centre line), Top 6 minus Rest')
for sh, m in (('Somers', 'Sleeping Giant'), ('Harugumo', 'Sleeping Giant'), ('Daring', 'Sleeping Giant'), ('Gearing', 'Mountain Range'), ('Gearing', 'Hotspot'), ('Svea', 'Sea of Fortune')):
    cmp(sh, m, 'west %', west)
cmp('Svea', 'Land of Fire', '% in cell F5', cellshare({'F5'}))
cmp('Gearing', 'Hotspot', '% in G9/G10/F10', cellshare({'G9', 'G10', 'F10'}))
cmp('Somers', 'Hotspot', '% in G9/G10/F10', cellshare({'G9', 'G10', 'F10'}))

P('\n## Cluster contrasts (difference of cluster A minus cluster B, resampling clans within each cluster)')
A = [s for sh in ('Somers', 'Gearing', 'Harugumo', 'Delny') for s in BY[sh]]; B = [s for sh in ('Daring', 'Z-42', 'Gdańsk', 'Grozovoi', 'Shimakaze') for s in BY[sh]]
def two(a, b, fn, reps=1000):
    ca, cb = by(a, 'team'), by(b, 'team'); ka, kb = list(ca), list(cb); o = []
    for _ in range(reps):
        o.append(fn([x for c in random.choices(ka, k=len(ka)) for x in ca[c]]) - fn([x for c in random.choices(kb, k=len(kb)) for x in cb[c]]))
    o.sort(); return o[int(.025 * len(o))], o[int(.975 * len(o)) - 1]
for nm, fn, f in (('conc per smoke', st_conc, '{:+,.0f}'), ('deaths per 100', st_deaths, '{:+.1f}'), ('median edge m', st_edge, '{:+,.0f}'), ('% inside', st_inside, '{:+.0f}'), ('% stationary', FKEY['stat'][2], '{:+.0f}'), ('% stacked', FKEY['stacked'][2], '{:+.0f}'), ('% selfish', FKEY['selfish'][2], '{:+.0f}')):
    P(f'flank smoke lines (n={len(A)}) vs cap sitters (n={len(B)}): {nm}: {fn(A):,.1f} vs {fn(B):,.1f}, diff {f.format(fn(A)-fn(B))} [{ci(two(A, B, fn), f)}]')
# Gdansk vs the other long 20 s smokes and vs Daring
for nm, fn, f in (('% stationary', FKEY['stat'][2], '{:+.0f}'), ('conc per smoke', st_conc, '{:+,.0f}'), ('% stacked', FKEY['stacked'][2], '{:+.0f}')):
    P(f'Gdańsk vs Harugumo (same 20 s smoke): {nm}: {fn(BY["Gdańsk"]):,.1f} vs {fn(BY["Harugumo"]):,.1f}, diff [{ci(two(BY["Gdańsk"], BY["Harugumo"], fn), f)}]')

P('\n## Deaths and game result (all destroyer smokes of the 9 ships)')
D = [s for sh in DDS for s in BY[sh]]
for g in ('top', 'rest'):
    for w in (True, False):
        a = [s for s in D if s['grp'] == g and s['win'] == w]; P(f'  {g} {"won" if w else "lost"}: n={len(a)} deaths per 100 = {st_deaths(a):.1f}')
for w in (True, False):
    a = [s for s in D if s['win'] == w]; P(f'  game {"won" if w else "lost"}: top minus rest deaths per 100 [{ci(boot_diff(a, st_deaths, reps=1000), "{:+.1f}")}]')
for sh in ('Harugumo', 'Gearing'):
    for w in (True, False):
        a = [s for s in BY[sh] if s['win'] == w]
        P(f'  {sh} game {"won" if w else "lost"}: top {st_deaths([s for s in a if s["grp"]=="top"])} (n={sum(s["grp"]=="top" for s in a)}) rest {st_deaths([s for s in a if s["grp"]=="rest"])} (n={sum(s["grp"]=="rest" for s in a)})')
open(os.path.join(OUT, 'extras.txt'), 'w', encoding='utf-8').write('\n'.join(out))
