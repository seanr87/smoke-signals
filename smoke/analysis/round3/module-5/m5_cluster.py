# Clan style features, simple average-linkage agglomerative clustering, and smoke chains.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5lib import *

FEATS = ['smokes per game', 'stacked %', 'screen %', 'selfish %', 'cap contest %', 'damage %', 'escape %', 'reposition %',
         'pushing %', 'kiting %', 'stationary %', 'inside cap %', 'median km to cap', 'first smoke (s)', 'long DD %', 'short DD %', 'cruiser smoke %', 'exhaust %']

def features(min_games=7):
    """All classes. Returns clans, feature names, raw matrix, standardized matrix (z-scores across clans)."""
    clans = sorted((c for c in NG if NG[c] >= min_games), key=lambda c: -WL[c][0] / NG[c])
    X = []
    for c in clans:
        ss = [s for s in S if s['team'] == c]
        first = [min(s['el'] for s in v) for v in by(ss, 'game').values()]
        sh = lambda f: pct(ss, f)
        X.append([len(ss) / NG[c], sh(lambda s: s['coverage'] == 'stacked'), sh(lambda s: s['coverage'] == 'screen'), sh(lambda s: s['coverage'] == 'selfish'),
                  sh(lambda s: 'cap_contest' in s['tags']), sh(lambda s: 'damage' in s['tags']), sh(lambda s: 'escape' in s['tags']), sh(lambda s: 'reposition' in s['tags']),
                  sh(lambda s: s['movement'] == 'pushing'), sh(lambda s: s['movement'] == 'kiting'), sh(lambda s: s['movement'] == 'stationary'),
                  sh(lambda s: s['inside']), med(max(0, s['edge']) for s in ss) / 1000, med(first),
                  sh(lambda s: s['kind'] == 'long DD'), sh(lambda s: s['kind'] == 'short DD'), sh(lambda s: s['kind'] == 'cruiser'), sh(lambda s: s['kind'] == 'exhaust')])
    Z = [[0.0] * len(FEATS) for _ in clans]
    for j in range(len(FEATS)):
        col = [r[j] for r in X]; m = mean(col); sd = statistics.pstdev(col) or 1
        for i in range(len(clans)): Z[i][j] = (X[i][j] - m) / sd
    return clans, FEATS, X, Z

def dist(a, b): return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))

def agglomerate(Z):
    """Average linkage. Returns merges [(members a, members b, height)] and the leaf order."""
    cl = {i: [i] for i in range(len(Z))}; order = {i: [i] for i in range(len(Z))}; merges = []
    while len(cl) > 1:
        best = None
        ks = sorted(cl)
        for ai, a in enumerate(ks):
            for b in ks[ai + 1:]:
                d = mean(dist(Z[i], Z[j]) for i in cl[a] for j in cl[b])
                if best is None or d < best[0]: best = (d, a, b)
        d, a, b = best
        merges.append((list(order[a]), list(order[b]), d))
        cl[a] = cl[a] + cl[b]; order[a] = order[a] + order[b]; del cl[b]; del order[b]
    return merges, order[min(order)]

def cut(merges, n, kcl):
    """Labels 0..kcl-1 from undoing the last kcl-1 merges."""
    lab = list(range(n))
    for a, b, d in merges[:n - kcl]:
        for i in b: lab[i] = lab[a[0]]
        for i in a: lab[i] = lab[a[0]]
    ids = {l: i for i, l in enumerate(sorted(set(lab), key=lab.index))}
    return [ids[l] for l in lab]

def chains(S, lim_m=1000, gap_s=60):
    """Same-team smokes (all classes, different or same player) whose laid paths come within lim_m of each other and that start within gap_s,
    or that the batch flags as overlapping. Returns lists of smokes (2 or more), each sorted by time."""
    key = lambda s: (s['game'], s['id'])  # smoke ids repeat across games in 3 cases
    par = {key(s): key(s) for s in S}
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for (gk, t), ss in by(S, lambda s: (s['game'], s['team'])).items():
        ss = sorted(ss, key=lambda s: s['el'])
        for i, a in enumerate(ss):
            for b in ss[i + 1:]:
                if b['el'] - a['el'] > gap_s: break
                near = min(math.hypot(x1 - x2, z1 - z2) for x1, z1 in a['path'] for x2, z2 in b['path']) * WU <= lim_m
                if near or b['id'] in a['overlap_ids'] or a['id'] in b['overlap_ids']: par[find(key(a))] = find(key(b))
    comp = by(S, lambda s: find(key(s)))
    return [sorted(v, key=lambda s: s['el']) for v in comp.values() if len(v) > 1]
