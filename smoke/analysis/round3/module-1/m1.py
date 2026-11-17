# Module 1 helpers: ship lists, profile features, clustering. Imported by numbers.py and figures.py.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from common import *
S, G = load()
OUT = os.path.dirname(os.path.abspath(__file__))
for s in S: s['ship'] = s['ship'].replace('\xa0', ' ')

DDS = ['Somers', 'Gearing', 'Delny', 'Gdańsk', 'Harugumo', 'Shimakaze', 'Grozovoi', 'Daring', 'Z-42']
OTHERS = ['Svea', 'Jinan', 'Napoli', 'Venezia', 'C. Colombo']  # every non-destroyer with 20 or more smokes
SHIPS = DDS + OTHERS
MAPLIST = sorted(MAPS, key=lambda m: -sum(1 for s in S if s['map'] == m and s['cls'] == 'destroyer'))
BY = {sh: [s for s in S if s['ship'] == sh] for sh in SHIPS}
KIND = {sh: C(s['kind'] for s in BY[sh]).most_common(1)[0][0] for sh in SHIPS}
KIND_COLOR = {'long DD': BLUE, 'short DD': ORANGE, 'cruiser': VIOLET, 'exhaust': AQUA}

def forward(s):
    """How far up the map the smoke sits, 0 = own baseline, 1 = enemy baseline (along the spawn axis)."""
    size = MAPS[s['map']]['space_size']
    if s['map'] in DIAGONAL: return (s['nx'] + s['nz']) / (2 * size) + 0.5
    return s['nz'] / size + 0.5

def share(ss, f): return 100 * sum(1 for s in ss if f(s)) / len(ss) if ss else None
def st_edge(ss): return med(s['edge'] for s in ss)
def st_inside(ss): return share(ss, lambda s: s['inside'])
def st_el(ss): return med(s['el'] for s in ss)
def st_fwd(ss): return 100 * mean(forward(s) for s in ss) if ss else None
def st_conc(ss): return mean(s['conc'] for s in ss)
def st_deaths(ss): return 100 * sum(s['deaths'] for s in ss) / len(ss) if ss else None
def st_mov(m): return lambda ss: share(ss, lambda s: s['movement'] == m)
def st_cov(c): return lambda ss: share(ss, lambda s: s['coverage'] == c)
def st_pp(p): return lambda ss: share(ss, lambda s: s['pp'] == p)

# (key, label, function, format, used for clustering)
FEATS = [
    ('edge', 'Median distance to cap edge (m)', st_edge, '{:,.0f}', True),
    ('inside', '% inside a cap', st_inside, '{:.0f}', True),
    ('fwd', 'How far up the map (%)', st_fwd, '{:.0f}', True),
    ('el', 'Median time used (s)', st_el, '{:.0f}', True),
    ('early', '% in first 3 min', lambda ss: share(ss, lambda s: s['el'] < 180), '{:.0f}', True),
    ('stat', '% stationary', st_mov('stationary'), '{:.0f}', True),
    ('push', '% pushing', st_mov('pushing'), '{:.0f}', True),
    ('kite', '% kiting', st_mov('kiting'), '{:.0f}', True),
    ('horiz', '% sideways', st_mov('horizontal'), '{:.0f}', True),
    ('selfish', '% selfish', st_cov('selfish'), '{:.0f}', True),
    ('screen', '% screen', st_cov('screen'), '{:.0f}', True),
    ('stacked', '% stacked', st_cov('stacked'), '{:.0f}', True),
    ('capc', '% cap contest', st_pp('cap_contest'), '{:.0f}', True),
    ('nopp', '% no purpose tag', st_pp('none'), '{:.0f}', True),
    ('dmg', '% damage', st_pp('damage'), '{:.0f}', True),
    ('esc', '% escape', st_pp('escape'), '{:.0f}', True),
    ('conc', 'Concealed damage per smoke', st_conc, '{:,.0f}', False),
    ('deaths', 'Deaths per 100 smokes', st_deaths, '{:.1f}', False),
]
FKEY = {f[0]: f for f in FEATS}
CLUSTER_KEYS = [f[0] for f in FEATS if f[4]]

def profile(ss): return {k: fn(ss) for k, _, fn, _, _ in FEATS}
PROF = {sh: profile(BY[sh]) for sh in SHIPS}

def zscores(prof, ships, keys):
    """Standardize each feature across the given ships. Returns ({ship: [z...]}, {key: (mean, sd)})."""
    par = {}
    for k in keys:
        v = [prof[sh][k] for sh in ships]; m = mean(v); sd = (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5 or 1.0
        par[k] = (m, sd)
    return {sh: [(prof[sh][k] - par[k][0]) / par[k][1] for k in keys] for sh in ships}, par

def dist(a, b): return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))

def agglomerate(Z, ships):
    """Average-linkage agglomerative clustering. Returns merges [(members a, members b, height)] and the leaf order."""
    cl = {i: [sh] for i, sh in enumerate(ships)}; merges = []; nxt = len(ships)
    d = lambda A, B: mean(dist(Z[a], Z[b]) for a in A for b in B)
    while len(cl) > 1:
        ks = list(cl); best = min(((d(cl[a], cl[b]), a, b) for i, a in enumerate(ks) for b in ks[i + 1:]))
        h, a, b = best
        merges.append((cl[a], cl[b], h)); cl[nxt] = cl[a] + cl[b]; del cl[a], cl[b]; nxt += 1
    return merges, list(cl.values())[0]

def cut(merges, ships, k):
    """Cluster membership after stopping when k clusters remain."""
    cl = [[sh] for sh in ships]
    for a, b, h in merges:
        if len(cl) <= k: break
        cl = [c for c in cl if c != a and c != b] + [a + b]
    return cl
