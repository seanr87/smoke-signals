# Round 5c x3, D2 (round5b/part-d/d2_structure.py on r5clib; the only inputs that can differ are the two time scores, now on s['e0']).
# D2: is it one scale or several styles? PCA by hand, k-means and average-linkage clustering, stability checks.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_lib import *
HERE = os.path.dirname(os.path.abspath(__file__))
OUTNAME = 'd2_structure.json' if CLOCK == 'e0' else 'd2_structure_el.json'
print('clock', CLOCK)
random.seed(520)
# Styles are built from what clans DO (five behaviour dimensions, 17 scores). 'What it buys' is kept out and reported per style afterwards.
KEYS = [k for k in PCA_KEYS if GROUP_OF[k] != 'buys']
BUYS = [k for k in PCA_KEYS if GROUP_OF[k] == 'buys']
V = {t: feats(t) for t in CLANS}
rows7 = [V[t] for t in CLANS7]
Z = zmatrix(rows7, KEYS)
shares, vecs, scores = pca(Z)
# orient PC1 so that smoke cruisers per game loads positive, PC2 so that smokes per game loads positive
def orient(i, key):
    if vecs[i][KEYS.index(key)] < 0:
        vecs[i] = [-x for x in vecs[i]]
        for s in scores: s[i] = -s[i]
orient(0, 'smoke_cruisers_pg'); orient(1, 'smokes_pg'); orient(2, 'pushing_pct')
print('features', len(KEYS), 'clans', len(Z))
print('PC shares', [round(100 * s, 1) for s in shares[:6]], 'cumulative 2:', round(100 * sum(shares[:2]), 1), '3:', round(100 * sum(shares[:3]), 1))
sd = [math.sqrt(shares[i] * len(KEYS)) for i in range(3)]
for i in range(3):
    print(f'PC{i+1} loadings (correlation of the score with each feature):')
    for k, x in sorted(zip(KEYS, vecs[i]), key=lambda x: -abs(x[1])): print(f'   {x * sd[i]:+.2f}  {LABEL[k]}')
for i in range(2):
    print(f'PC{i+1} order:', ', '.join(f"{'*' if t in TOP else ''}{t} {s[i]:+.1f}" for t, s in sorted(zip(CLANS7, scores), key=lambda x: x[1][i])))

# comparison: the same analysis with the five outcome scores included (22 scores)
KF = [k for k in PCA_KEYS if all(r[k] is not None for r in rows7)]
print('outcome scores without a value for every clan (left out of the with-outcomes comparison):', [k for k in PCA_KEYS if k not in KF])
Zf = zmatrix(rows7, KF); shf, vf, scf = pca(Zf)
def pear(a, b):
    ma, mb = mean(a), mean(b); num = sum((x - ma) * (y - mb) for x, y in zip(a, b)); den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else 0
print(f'with outcomes included ({len(KF)} scores): PC shares', [round(100 * s, 1) for s in shf[:3]], '| |r| of its PC1 with behaviour PC1', round(abs(pear([s[0] for s in scf], [s[0] for s in scores])), 2),
      '| PC2', round(abs(pear([s[1] for s in scf], [s[1] for s in scores])), 2))
OUTR = {}; SINGLE = {}
for k in BUYS + ['caps_taken_pg', 'caps_taken_c_pg']:
    ix = [i for i, r in enumerate(rows7) if r[k] is not None]; col = [rows7[i][k] for i in ix]
    OUTR[k] = dict(pc1=pear(col, [scores[i][0] for i in ix]), pc2=pear(col, [scores[i][1] for i in ix]), n_clans=len(ix))
    print(f'   outcome vs axes: {LABEL[k]}: r with PC1 {OUTR[k]["pc1"]:+.2f}, with PC2 {OUTR[k]["pc2"]:+.2f} ({len(ix)} clans)')
for k in ('smoke_cruisers_pg', 'long_ships_pg', 'teammate_pct', 'smokes_pg', 'parked_pct'):
    col = [r[k] for r in rows7]
    SINGLE[k] = dict(pc1=pear(col, [s[0] for s in scores]), pc2=pear(col, [s[1] for s in scores]))
    print(f'   single score vs axes: {LABEL[k]}: r with PC1 {SINGLE[k]["pc1"]:+.2f}, with PC2 {SINGLE[k]["pc2"]:+.2f}')

# null: shuffle every column independently (keeps each score's spread, removes links between scores)
def shuffled(Z):
    cols = [list(c) for c in zip(*Z)]
    for c in cols: random.shuffle(c)
    return [list(r) for r in zip(*cols)]
null1, null2, nullsil = [], [], {2: [], 3: [], 4: []}
for _ in range(300):
    Zs = shuffled(Z); ev = jacobi(corr(Zs)); tot = sum(v for v, _ in ev)
    null1.append(ev[0][0] / tot); null2.append(ev[1][0] / tot)
    for k in nullsil: nullsil[k].append(silhouette(Zs, kmeans(Zs, k, restarts=8)[0]))
null1.sort(); null2.sort()
print('null PC1 share: median', round(100 * med(null1), 1), '95th', round(100 * null1[int(.95 * len(null1))], 1), '| share of shuffles with PC1 >= observed', sum(x >= shares[0] for x in null1) / len(null1))
print('null PC2 share: median', round(100 * med(null2), 1), '95th', round(100 * null2[int(.95 * len(null2))], 1), '| share of shuffles with PC2 >= observed', sum(x >= shares[1] for x in null2) / len(null2))

# clustering
KM = {}; HC = {}; SIL = {}
for k in (2, 3, 4, 5):
    lab, inertia = kmeans(Z, k, restarts=200); KM[k] = lab; HC[k] = hier(Z, k)
    sil = silhouette(Z, lab); ns = sorted(nullsil.get(k, [0])); SIL[k] = sil
    print(f'k={k}: k-means silhouette {sil:.2f} (shuffled-data median {med(ns):.2f}, 95th pct {ns[int(.95 * len(ns)) - 1]:.2f}; share of shuffles >= observed {sum(x >= sil for x in ns) / len(ns):.2f}), '
          f'sizes {sorted(C(lab).values(), reverse=True)}, hier sizes {sorted(C(HC[k]).values(), reverse=True)}, silhouette hier {silhouette(Z, HC[k]):.2f}, ARI k-means vs hier {ari(lab, HC[k]):.2f}')
    for c in sorted(set(lab), key=lambda c: mean(scores[i][0] for i in range(len(Z)) if lab[i] == c)):
        print('    ', ', '.join(('*' if t in TOP else '') + t for t, l in zip(CLANS7, lab) if l == c))
    print('   hier:', ' | '.join(', '.join(('*' if t in TOP else '') + t for t, l in zip(CLANS7, HC[k]) if l == c) for c in sorted(set(HC[k]))))

# is PC1 a continuum or two lumps? largest gap between neighbours on PC1 relative to the spread
p1 = sorted(s[0] for s in scores); gaps = [b - a for a, b in zip(p1, p1[1:])]
print('PC1 sorted', [round(x, 1) for x in p1], '| largest gap', round(max(gaps), 2), 'of range', round(p1[-1] - p1[0], 2))
p2 = sorted(s[1] for s in scores); gaps2 = [b - a for a, b in zip(p2, p2[1:])]
print('PC2 sorted', [round(x, 1) for x in p2], '| largest gap', round(max(gaps2), 2), 'of range', round(p2[-1] - p2[0], 2))

def switches(lab, base):
    """Clans not in the majority match after pairing each new group with the base group it overlaps most."""
    return sum(1 for i in range(len(lab)) if base[i] != C(base[j] for j in range(len(lab)) if lab[j] == lab[i]).most_common(1)[0][0])
# stability a: drop one feature group at a time
STAB = {}
for kk in (2, 3):
    print(f'-- drop one group, k={kk} (ARI against the full-feature k-means; 1 = same groups)')
    for d in DIMS[:5]:
        ks = [k for k in KEYS if GROUP_OF[k] != d['id']]; Zd = zmatrix(rows7, ks)
        lab = kmeans(Zd, kk, restarts=100)[0]; a = ari(lab, KM[kk]); sh, _, _ = pca(Zd)
        STAB[(kk, d['id'])] = dict(ari=a, switch=switches(lab, KM[kk]), pc1=sh[0], pc2=sh[1])
        print(f"   without {d['name']:18s} ARI {a:.2f}  clans that switch group {switches(lab, KM[kk]):2d}  PC1 {100 * sh[0]:.0f}% PC2 {100 * sh[1]:.0f}%")
# stability b: resample games within each clan
B = 200; aris = {2: [], 3: []}; pc1s = []; r1 = []; r2 = []; co = {2: collections.defaultdict(int), 3: collections.defaultdict(int)}
base1 = [s[0] for s in scores]; base2 = [s[1] for s in scores]
# styles on the two-axis map: k-means on (PC1, PC2); fixed axes and fixed centres are then used to see how often a clan keeps its style
P2 = [s[:2] for s in scores]; KM2 = {}; CEN2 = {}
for k in (2, 3, 4, 5):
    lab = kmeans(P2, k, restarts=200)[0]
    order = sorted(set(lab), key=lambda c: (mean(P2[i][0] for i in range(len(P2)) if lab[i] == c)))
    lab = [order.index(c) for c in lab]; KM2[k] = lab
    CEN2[k] = [[mean(P2[i][j] for i in range(len(P2)) if lab[i] == c) for j in (0, 1)] for c in range(k)]
    print(f'2-axis map k={k}: silhouette {silhouette(P2, lab):.2f}, ARI vs 17-score k-means {ari(lab, KM[k]):.2f}')
    for c in range(k): print(f'     centre ({CEN2[k][c][0]:+.1f}, {CEN2[k][c][1]:+.1f}):', ', '.join(('*' if t in TOP else '') + t for t, l in zip(CLANS7, lab) if l == c))
MU = [mean(r[k] for r in rows7) for k in KEYS]; SD = [statistics.pstdev([r[k] for r in rows7]) or 1 for k in KEYS]
def project(f):
    z = [(f[k] - m) / s for k, m, s in zip(KEYS, MU, SD)]
    return [sum(z[j] * vecs[i][j] for j in range(len(KEYS))) for i in range(2)]
keep = {k: C() for k in KM2}; PBOOT = collections.defaultdict(list)
for _ in range(B):
    rb = []
    for t in CLANS7:
        while True:
            f = feats(t, random.choices(GAMES[t], k=NG[t]))
            if all(f[k] is not None for k in KEYS): break
        rb.append(f)
        p = project(f); PBOOT[t].append(p)
        for k in KM2:
            if min(range(k), key=lambda c: dist(p, CEN2[k][c])) == KM2[k][CLANS7.index(t)]: keep[k][t] += 1
    Zb = zmatrix(rb, KEYS); sh, vb, sb = pca(Zb)
    pc1s.append(sh[0]); r1.append(abs(pear([s[0] for s in sb], base1))); r2.append(abs(pear([s[1] for s in sb], base2)))
    for kk in (2, 3):
        lab = kmeans(Zb, kk, restarts=15)[0]; aris[kk].append(ari(lab, KM[kk]))
        for i in range(len(lab)):
            for j in range(i + 1, len(lab)):
                if lab[i] == lab[j]: co[kk][(i, j)] += 1
pc1s.sort()
print(f'-- games resampled within clan ({B} runs): PC1 share median {100 * med(pc1s):.0f}% (95% {100 * pc1s[int(.025 * B)]:.0f} to {100 * pc1s[int(.975 * B) - 1]:.0f}); '
      f'PC1 scores vs base |r| median {med(r1):.2f} (5th pct {sorted(r1)[int(.05 * B)]:.2f}); PC2 |r| median {med(r2):.2f} (5th pct {sorted(r2)[int(.05 * B)]:.2f})')
CLSTAB = {}
for kk in (2, 3):
    a = sorted(aris[kk]); print(f'   k={kk}: ARI vs base median {med(a):.2f} (95% {a[int(.025 * B)]:.2f} to {a[int(.975 * B) - 1]:.2f}), share of runs with ARI >= 0.8: {sum(x >= .8 for x in a) / B:.2f}')
    for i, t in enumerate(CLANS7):
        mates = [j for j in range(len(CLANS7)) if j != i and KM[kk][j] == KM[kk][i]]
        CLSTAB[(kk, t)] = mean(co[kk][(min(i, j), max(i, j))] / B for j in mates) if mates else None
    print('     stays with its group (share of runs, averaged over group mates):', ', '.join(f'{t} {CLSTAB[(kk, t)]:.2f}' if CLSTAB[(kk, t)] is not None else f'{t} alone' for t in CLANS7))

for k in KM2:
    print(f'   2-axis style kept under game resampling, k={k}: mean {mean(keep[k][t] / B for t in CLANS7):.2f};', ', '.join(f'{t} {keep[k][t] / B:.2f}' for t in CLANS7))
PCI = {}
for t in CLANS7:
    a = sorted(p[0] for p in PBOOT[t]); b = sorted(p[1] for p in PBOOT[t])
    PCI[t] = [[a[int(.025 * B)], a[int(.975 * B) - 1]], [b[int(.025 * B)], b[int(.975 * B) - 1]]]
print('   axis-1 95% half-width, median over clans:', round(med((PCI[t][0][1] - PCI[t][0][0]) / 2 for t in CLANS7), 2), '| axis-2:', round(med((PCI[t][1][1] - PCI[t][1][0]) / 2 for t in CLANS7), 2))

# flagged clans projected onto the same axes, and nearest group centre
PROJ = {}
small_ok = [t for t in SMALL if all(V[t][k] is not None for k in KEYS)]
Zs_ = zmatrix([V[t] for t in small_ok], KEYS, ref=rows7)
print('flagged clans with every score available:', small_ok, '| missing some:', [t for t in SMALL if t not in small_ok])
ORDER = {kk: sorted(set(KM[kk]), key=lambda c: mean(scores[i][0] for i in range(len(Z)) if KM[kk][i] == c)) for kk in (2, 3)}
for t, z in zip(small_ok, Zs_):
    sc = [sum(z[j] * vecs[i][j] for j in range(len(KEYS))) for i in range(3)]
    near = {}
    for kk in (2, 3):
        cen = {c: [mean(col) for col in zip(*[Z[i] for i in range(len(Z)) if KM[kk][i] == c])] for c in set(KM[kk])}
        near[kk] = ORDER[kk].index(min(cen, key=lambda c: dist(z, cen[c])))
    near2 = {k: min(range(k), key=lambda c: dist(sc[:2], CEN2[k][c])) for k in KM2}
    PROJ[t] = dict(pc=sc, near=near, near2={str(k): v for k, v in near2.items()}); print('  ', t, [round(x, 1) for x in sc], near, near2)

# group means of raw scores for naming, k = 2 and 3
SUMMARY = {}
for kk in (2, 3):
    print(f'-- group profiles k={kk} (mean of clan values; z in brackets)')
    for c in ORDER[kk]:
        m = [i for i in range(len(Z)) if KM[kk][i] == c]
        print('  group', ORDER[kk].index(c), [('*' if CLANS7[i] in TOP else '') + CLANS7[i] for i in m])
        prof = {k: (mean(rows7[i][k] for i in m if rows7[i][k] is not None) if any(rows7[i][k] is not None for i in m) else None) for k in ALLKEYS}
        zz = {k: mean(Z[i][KEYS.index(k)] for i in m) for k in KEYS}
        w = sum(WLD[CLANS7[i]][0] for i in m); l = sum(WLD[CLANS7[i]][1] for i in m)
        SUMMARY[(kk, ORDER[kk].index(c))] = dict(members=[CLANS7[i] for i in m], profile=prof, z=zz, wins=w, losses=l)
        print('     ', '; '.join(f'{LABEL[k]} {prof[k]:,.1f} ({zz[k]:+.1f})' for k in sorted(KEYS, key=lambda k: -abs(zz[k]))))
        print(f'      W-L {w}-{l} ({100 * w / (w + l):.0f}%)')

R = corr(Z)
for key in ('smoke_cruisers_pg', 'long_ships_pg', 'smokes_pg', 'teammate_pct'):
    a = KEYS.index(key)
    print(f'-- correlation with {LABEL[key]}:', '; '.join(f'{LABEL[k]} {R[a][j]:+.2f}' for j, k in sorted(enumerate(KEYS), key=lambda x: -abs(R[a][x[0]]))[1:9]))
wr = [WLD[t][0] / NG[t] for t in CLANS7]
print('-- win share vs PC1 r', round(pear(wr, base1), 2), 'vs PC2 r', round(pear(wr, base2), 2), 'vs PC3', round(pear(wr, [s[2] for s in scores]), 2))

gi = gaps2.index(max(gaps2))
SHAPE = dict(pc1_largest_gap=max(gaps), pc1_range=p1[-1] - p1[0], pc1_gap_low_side=sum(1 for x in p1 if x <= p1[gaps.index(max(gaps))]),
             pc2_largest_gap=max(gaps2), pc2_range=p2[-1] - p2[0], pc2_low_clans=[t for t, s in sorted(zip(CLANS7, scores), key=lambda x: x[1][1]) if s[1] <= p2[gi]],
             pc2_low_max=p2[gi], pc2_high_min=p2[gi + 1])
json.dump(dict(clock=CLOCK, with_outcomes=dict(n_scores=len(KF), pc1_r=abs(pear([s[0] for s in scf], [s[0] for s in scores])), pc2_r=abs(pear([s[1] for s in scf], [s[1] for s in scores]))),
               outcome_r=OUTR, single_r=SINGLE, shape=SHAPE, km2_silhouette={str(k): silhouette(P2, KM2[k]) for k in KM2}, keys=KEYS, clans=CLANS7, shares=shares[:6], loadings=[[x * sd[i] for x in vecs[i]] for i in range(3)], scores=scores,
               kmeans={str(k): [ORDER[k].index(c) for c in KM[k]] if k in ORDER else KM[k] for k in KM}, hier={str(k): HC[k] for k in HC}, proj=PROJ, silhouette={str(k): v for k, v in SIL.items()},
               null=dict(pc1_median=med(null1), pc1_p95=null1[int(.95 * len(null1))], pc2_median=med(null2), pc2_p95=null2[int(.95 * len(null2))],
                         sil={str(k): dict(median=med(v), p95=sorted(v)[int(.95 * len(v)) - 1]) for k, v in nullsil.items()}),
               drop_group={f'{a}:{b}': v for (a, b), v in STAB.items()}, boot=dict(ari2=sorted(aris[2]), ari3=sorted(aris[3]), pc1=pc1s, r1=sorted(r1), r2=sorted(r2)),
               km2={str(k): v for k, v in KM2.items()}, cen2={str(k): v for k, v in CEN2.items()}, keep2={str(k): {t: keep[k][t] / B for t in CLANS7} for k in KM2}, pc_ci=PCI,
               clan_stay={f'{a}:{b}': v for (a, b), v in CLSTAB.items()}, summary={f'{a}:{b}': v for (a, b), v in SUMMARY.items()},
               win_r=dict(pc1=pear(wr, base1), pc2=pear(wr, base2))),
          open(os.path.join(HERE, OUTNAME), 'w', encoding='utf-8'), indent=1)
print('wrote', OUTNAME)
