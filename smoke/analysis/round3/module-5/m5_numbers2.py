# Clan fingerprint numbers and the clan-styles.json export.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5lib import *
from m5_cluster import *
print('ids unique', len({s['id'] for s in S}), 'game+id unique', len({(s['game'], s['id']) for s in S}), 'smokes', len(S))
print('=== 5 clusters')
clans, feats, X, Z = features()
n = len(clans)
print(n, clans)
for i, c in enumerate(clans): print(c.ljust(6), NG[c], WL[c], ' '.join(f'{v:6.2f}' for v in X[i]))
print(feats)
print('feature means', [(f, round(mean(r[j] for r in X), 1)) for j, f in enumerate(feats)])
merges, order = agglomerate(Z)
print('leaf order', [clans[i] for i in order])
for kcl in (3, 4, 5, 6):
    lab = cut(merges, n, kcl)
    print(kcl, {l: [clans[i] for i in range(n) if lab[i] == l] for l in sorted(set(lab))})
h = clans.index('H-SR'); p = clans.index('PN')
dh = [dist(Z[h], Z[i]) for i in range(n)]
print('distance to H-SR', sorted((round(dh[i], 2), clans[i]) for i in range(n) if i != h))
print('nearest to PN', sorted(((round(dist(Z[p], Z[i]), 2), c) for i, c in enumerate(clans) if c != 'PN'))[:6])
print('H-SR z', [(f, round(Z[h][j], 1)) for j, f in enumerate(feats)])
print('PN z', [(f, round(Z[p][j], 1)) for j, f in enumerate(feats)])
print('typical gap', mean(dist(Z[a], Z[b]) for a in range(n) for b in range(a)))
near = C()
for j in range(len(feats)):
    Zj = [[v for jj, v in enumerate(r) if jj != j] for r in Z]
    for d, c in sorted((dist(Zj[h], Zj[i]), clans[i]) for i in range(n) if i != h)[:3]: near[c] += 1
print('nearest-3 to H-SR when dropping one feature (of %d):' % len(feats), near.most_common())
wr = [WL[c][0] / NG[c] for c in clans]
def corr(idx):
    mx, my = mean(wr[i] for i in idx), mean(dh[i] for i in idx)
    den = math.sqrt(sum((wr[i] - mx) ** 2 for i in idx) * sum((dh[i] - my) ** 2 for i in idx))
    return sum((wr[i] - mx) * (dh[i] - my) for i in idx) / den if den else None
idx = [i for i in range(n) if i != h]
print('corr(win rate, distance to H-SR)', round(corr(idx), 2), lohi([corr(random.choices(idx, k=len(idx))) for _ in range(1000)]), 'n', len(idx))

# export: branch = group after cutting the tree into 6 groups, named by its members in tree order
lab = cut(merges, n, 6)
members = {l: [clans[i] for i in order if lab[i] == l] for l in set(lab)}
out = dict(batch=BATCH_NAME, scope='all classes, clans with 7+ games', features=feats,
           method='z-scores across the 24 clans; distance = root mean squared z difference; average-linkage agglomerative clustering; branch = cut into 6 groups',
           leaf_order=[clans[i] for i in order],
           clans=[dict(clan=c, games=NG[c], wins=WL[c][0], losses=WL[c][1], group='top' if c in TOP else 'rest', smokes=sum(1 for s in S if s['team'] == c),
                       values={f: round(X[i][j], 2) for j, f in enumerate(feats)}, z={f: round(Z[i][j], 2) for j, f in enumerate(feats)},
                       distance_to_hsr=round(dh[i], 3), branch=lab[i], branch_members=members[lab[i]]) for i, c in enumerate(clans)])
json.dump(out, open(os.path.join(HERE5, 'clan-styles.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote clan-styles.json')
