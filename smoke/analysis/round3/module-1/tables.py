# Module 1 numbers: prints every table used in MODULE-1.md. Output is saved to tables.txt.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from m1 import *
random.seed(19)
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); out.append(line); print(line)

P('## Ship profiles (all smokes of the ship)')
hdr = ['ship', 'kind', 'n', 'top n', 'clans'] + [f[0] for f in FEATS]
rows = []
for sh in SHIPS:
    ss = BY[sh]
    rows.append([sh, KIND[sh], len(ss), sum(s['grp'] == 'top' for s in ss), len({s['team'] for s in ss})] + [FKEY[k][3].format(PROF[sh][k]) for k in FKEY])
P(md_table(hdr, rows))

P('\n## Mountain Range cap A effect on distance (median edge with and without mrA smokes)')
for sh in SHIPS:
    ss = BY[sh]; a = [s for s in ss if not s['mrA']]
    P(f'{sh:12} mrA n={len(ss)-len(a):3}  edge all={st_edge(ss):7.0f}  without={st_edge(a):7.0f}  inside all={st_inside(ss):4.0f}%  without={st_inside(a):4.0f}%')

P('\n## Intervals on ship profile (95%, resampling clans)')
for sh in SHIPS:
    ss = BY[sh]
    P(f'{sh:12} edge {ci(boot_stat(ss, st_edge, reps=600))} | inside {ci(boot_stat(ss, st_inside, reps=600))} | conc {ci(boot_stat(ss, st_conc, reps=600))} | deaths {ci(boot_stat(ss, st_deaths, reps=600), "{:.1f}")}')

P('\n## Clustering (average linkage on standardized profile, behaviour features only)')
Z, par = zscores(PROF, SHIPS, CLUSTER_KEYS)
merges, order = agglomerate(Z, SHIPS)
for a, b, h in merges: P(f'  merge at {h:.2f}: {a} + {b}')
P('leaf order', order)
for k in (2, 3, 4, 5, 6): P(f'k={k}:', cut(merges, SHIPS, k))
P('\nDistance matrix (root mean square z difference)')
P(' ' * 12 + ' '.join(f'{sh[:6]:>6}' for sh in order))
for a in order: P(f'{a:12}' + ' '.join(f'{dist(Z[a], Z[b]):6.2f}' for b in order))

P('\n## Robustness: with outcome features too')
ALLK = [f[0] for f in FEATS]
Z2, _ = zscores(PROF, SHIPS, ALLK); m2, _ = agglomerate(Z2, SHIPS)
for k in (3, 4, 5): P(f'k={k}:', cut(m2, SHIPS, k))
P('## Robustness: destroyers only')
Z3, _ = zscores(PROF, DDS, CLUSTER_KEYS); m3, o3 = agglomerate(Z3, DDS)
for a, b, h in m3: P(f'  merge at {h:.2f}: {a} + {b}')
for k in (2, 3, 4): P(f'k={k}:', cut(m3, DDS, k))

P('\n## Per map: ship x map profile (n >= 15), nearest ship centroid and nearest cluster')
K = 4
clusters = cut(merges, SHIPS, K)
cent = {i: [mean(Z[sh][j] for sh in c) for j in range(len(CLUSTER_KEYS))] for i, c in enumerate(clusters)}
own = {sh: i for i, c in enumerate(clusters) for sh in c}
P('clusters', clusters)
hit = tot = 0
for sh in SHIPS:
    for m in MAPLIST:
        ss = [s for s in BY[sh] if s['map'] == m]
        if len(ss) < 15: continue
        p = profile(ss); z = [(p[k] - par[k][0]) / par[k][1] for k in CLUSTER_KEYS]
        near = min(cent, key=lambda i: dist(z, cent[i])); tot += 1; hit += near == own[sh]
        P(f'  {sh:10} {m:15} n={len(ss):3} own cluster {own[sh]} nearest {near} {"ok" if near == own[sh] else "DIFFERENT"} | edge {p["edge"]:6.0f} inside {p["inside"]:3.0f}% fwd {p["fwd"]:3.0f} stat {p["stat"]:3.0f}% selfish {p["selfish"]:3.0f}% capc {p["capc"]:3.0f}%')
P(f'ship x map cells matching own cluster: {hit} of {tot}')

P('\n## Kind lens profile')
for kd in ('long DD', 'short DD', 'cruiser', 'exhaust'):
    ss = [s for s in S if s['kind'] == kd]; p = profile(ss)
    P(f'{kd:9} n={len(ss):4} ' + ' '.join(f'{k}={FKEY[k][3].format(p[k])}' for k in FKEY))

P('\n## Top 6 minus rest within each ship (95% interval by resampling clans; * = excludes zero)')
STATS = [('edge', st_edge, '{:+,.0f}'), ('inside', st_inside, '{:+.0f}'), ('fwd', st_fwd, '{:+.1f}'), ('el', st_el, '{:+.0f}'), ('stat', FKEY['stat'][2], '{:+.0f}'),
         ('selfish', FKEY['selfish'][2], '{:+.0f}'), ('capc', FKEY['capc'][2], '{:+.0f}'), ('conc', st_conc, '{:+,.0f}'), ('deaths', st_deaths, '{:+.1f}')]
for sh in SHIPS:
    ss = BY[sh]; a = [s for s in ss if s['grp'] == 'top']; b = [s for s in ss if s['grp'] == 'rest']
    if len(a) < 15 or len(b) < 15: P(f'{sh}: top n={len(a)}, rest n={len(b)}: too few for a comparison'); continue
    P(f'{sh}: top n={len(a)} ({len({s["team"] for s in a})} clans), rest n={len(b)} ({len({s["team"] for s in b})} clans)')
    for k, fn, f in STATS:
        va, vb = fn(a), fn(b)
        P(f'    {k:8} top {va:9.1f} rest {vb:9.1f} diff {f.format(va - vb):>8}  [{ci(boot_diff(ss, fn, reps=800), f)}]')

P('\n## Top 6 minus rest within ship x map (both groups n >= 12)')
for sh in SHIPS:
    for m in MAPLIST:
        ss = [s for s in BY[sh] if s['map'] == m]; a = [s for s in ss if s['grp'] == 'top']; b = [s for s in ss if s['grp'] == 'rest']
        if len(a) < 12 or len(b) < 12: continue
        P(f'{sh} on {m}: top n={len(a)} ({len({s["team"] for s in a})} clans), rest n={len(b)} ({len({s["team"] for s in b})} clans)')
        for k, fn, f in STATS:
            if k in ('edge', 'inside', 'fwd', 'el', 'conc', 'deaths', 'selfish'):
                va, vb = fn(a), fn(b)
                P(f'    {k:8} top {va:9.1f} rest {vb:9.1f} diff {f.format(va - vb):>8}  [{ci(boot_diff(ss, fn, reps=500), f)}]')
        ca = C(s['ncell_name'] for s in a).most_common(3); cb = C(s['ncell_name'] for s in b).most_common(3)
        P(f'    top cells {ca} | rest cells {cb}')

P('\n## Busiest cells per ship x map (n >= 15)')
for sh in SHIPS:
    for m in MAPLIST:
        ss = [s for s in BY[sh] if s['map'] == m]
        if len(ss) < 15: continue
        top3 = C(s['ncell_name'] for s in ss).most_common(3)
        P(f'  {sh:10} {m:15} n={len(ss):3} ' + ', '.join(f'{c} {100*n/len(ss):.0f}%' for c, n in top3) + f' | cells used {len({s["ncell_name"] for s in ss})}')

P('\n## PN (small n)')
pn = [s for s in S if s['is_pn'] and s['cls'] == 'destroyer']
P(f'PN destroyer smokes n={len(pn)}: ships {dict(C(s["ship"] for s in pn))}, median edge {st_edge(pn):.0f} m, inside {st_inside(pn):.0f}%, conc per smoke {st_conc(pn):.0f}, deaths {sum(s["deaths"] for s in pn)}')
for sh in ('Somers', 'Harugumo'):
    a = [s for s in pn if s['ship'] == sh]
    P(f'  PN {sh} n={len(a)}: median edge {st_edge(a):.0f} (all {sh} {PROF[sh]["edge"]:.0f}), inside {st_inside(a):.0f}%, conc {st_conc(a):.0f} (all {PROF[sh]["conc"]:.0f})')
open(os.path.join(OUT, 'tables.txt'), 'w', encoding='utf-8').write('\n'.join(out))
