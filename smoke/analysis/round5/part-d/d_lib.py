# Part D shared helper: per-clan style scores from the batch. Read-only on the batch.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *

S, G = load5()
random.seed(519)
WLD = win_loss(G)
CLANS = sorted(WLD, key=lambda t: (-sum(WLD[t]), t))
NG = {t: sum(WLD[t]) for t in CLANS}
MIN_GAMES = 7
CLANS7 = [t for t in CLANS if NG[t] >= MIN_GAMES]
SMALL = [t for t in CLANS if NG[t] < MIN_GAMES]
nb = lambda x: (x or '?').replace('\xa0', ' ')

GAMES = collections.defaultdict(list)          # clan -> game keys
for g in G.values():
    for t in g['teams']: GAMES[t].append(g['key'])
SG = collections.defaultdict(list)             # (clan, game) -> smokes
for s in S: SG[(s['team'], s['game'])].append(s)
RO = {(t, k): [p for p in G[k]['roster'].values() if p['team'] == t] for t in CLANS for k in GAMES[t]}

HOLD_NEAR_M = 2000
EXHAUST = ('Napoli', 'Venezia', 'C. Colombo', 'Conte Verde')
PARKED_CA = ('Svea', 'Jinan')
def carries(p): return bool(p.get('smoke_variant'))
def cls(p): return p['ship_class'].lower()

# movement mapping (batch label -> plain word). closing_m in the batch is positive when the range to the nearest enemies OPENED
# while laying and negative when it closed (see the 'reason' text), so: pushing = closing on the enemy, kiting = opening,
# parked = stationary. 'horizontal' (moved across the enemy's front, range about unchanged) is kept as 'sideways';
# 'unclassified' (no enemy position known) stays in the denominator.
MOVE = {'pushing': 'pushing', 'kiting': 'kiting', 'stationary': 'parked', 'horizontal': 'sideways', 'unclassified': 'unknown'}

def P(ss, f): return 100 * sum(1 for s in ss if f(s)) / len(ss) if ss else None

def feats(clan, games=None, strict=False):
    """All style numbers of one clan over a list of its game keys (repeats allowed, for resampling)."""
    games = GAMES[clan] if games is None else games
    n = len(games)
    ss = [s for k in games for s in SG[(clan, k)]]
    dd = [s for s in ss if s['cls'] == 'destroyer']
    ro = [RO[(clan, k)] for k in games]
    pg = lambda f: sum(sum(1 for p in r if f(p)) for r in ro) / n
    d = dict(n_games=n, n_smokes=len(ss), n_dd_smokes=len(dd))
    # 1 lineup
    d['long_ships_pg'] = pg(lambda p: nb(p['ship']) in LONG_SHIPS and carries(p))
    d['sitter_ships_pg'] = pg(lambda p: nb(p['ship']) in SITTERS and carries(p))
    d['smoke_dd_pg'] = pg(lambda p: cls(p) == 'destroyer' and carries(p))
    d['smoke_cruisers_pg'] = pg(lambda p: cls(p) == 'cruiser' and carries(p))
    d['parked_cruisers_pg'] = pg(lambda p: nb(p['ship']) in PARKED_CA and carries(p))
    d['exhaust_ships_pg'] = pg(lambda p: nb(p['ship']) in EXHAUST and carries(p))
    d['smoke_ships_pg'] = pg(carries)
    d['dd_pg'] = pg(lambda p: cls(p) == 'destroyer')
    d['radar_ships_pg'] = pg(lambda p: bool(p.get('radar_m')))
    # 2 volume and tempo
    d['smokes_pg'] = len(ss) / n
    first = [min(s['el'] for s in SG[(clan, k)]) for k in games if SG[(clan, k)]]
    d['first_smoke_s'] = med(first)
    d['late_pct'] = P(ss, lambda s: s['el'] >= 720)
    d['early_pct'] = P(ss, lambda s: s['el'] < 300)
    # 3 who it is for
    d['teammate_pct'] = P(ss, lambda s: s['coverage'] in ('stacked', 'screen'))
    d['selfish_pct'] = P(ss, lambda s: s['coverage'] == 'selfish')
    d['stacked_pct'] = P(ss, lambda s: s['coverage'] == 'stacked')
    d['radar_ca_inside_pct'] = P(dd, lambda s: s['radar_ca_inside'])
    d['cruiser_inside_pct'] = P(dd, lambda s: s['cr_inside'])
    # 4 where
    d['edge_m'] = med(s['edge'] for s in ss)
    d['inside_cap_pct'] = P(ss, lambda s: s['inside'])
    d['centre_pct'] = P(ss, lambda s: s['lane'] == 'center')
    d['own_half_pct'] = P(ss, lambda s: s['frontline_m'] is not None and s['frontline_m'] < 0)
    # 5 movement
    for lab in ('pushing', 'kiting', 'parked', 'sideways'):
        d[lab + '_pct'] = P(ss, lambda s: MOVE[s['movement']] == lab)
    # 6 what it buys
    d['conc_per_smoke'] = mean(s['conc'] for s in ss)
    d['conc_pg'] = sum(s['conc'] for s in ss) / n
    took = {(i, s['near_cap']) for i, k in enumerate(games) for s in SG[(clan, k)] if s['we_took']}
    d['caps_taken_pg'] = len(took) / n                      # distinct caps (per game) taken next to a smoke; caps already ours excluded
    d['cap_won_pg'] = sum(s['cap_won'] for s in ss) / n     # batch flag, counted per smoke
    d['cap_def_pg'] = sum(s['cap_def'] for s in ss) / n
    el = [s for s in ss if s['we_took'] is not None]; d['n_take_known'] = len(el)
    d['took_pct'] = P(el, lambda s: s['we_took'])
    # enemy_took is only meaningful for smokes inside or within 2 km of the nearest cap (validated by another worker this round)
    hl = [s for s in ss if s['enemy_took'] is not None and s['near_cap_edge_m'] <= HOLD_NEAR_M]; d['n_hold_known'] = len(hl)
    d['held_pct'] = P(hl, lambda s: s['enemy_took'] is False)
    d['deaths_per100'] = 100 * sum(s['deaths'] for s in ss) / len(ss) if ss else None
    d['deaths_pg'] = sum(s['deaths'] for s in ss) / n
    if strict:   # minimum n of 8 for a reported rate ("too few" below that)
        if len(dd) < 8: d['radar_ca_inside_pct'] = d['cruiser_inside_pct'] = None
        if len(el) < 8: d['took_pct'] = None
        if len(hl) < 8: d['held_pct'] = None
    return d

# the six dimensions, the single headline number of each, and the full set
DIMS = [
    dict(id='lineup', name='Lineup', headline='smoke_cruisers_pg', keys=['long_ships_pg', 'sitter_ships_pg', 'smoke_dd_pg', 'smoke_cruisers_pg', 'exhaust_ships_pg'],
         high='more cruisers that carry smoke in the lineup'),
    dict(id='tempo', name='Volume and tempo', headline='smokes_pg', keys=['smokes_pg', 'first_smoke_s', 'late_pct'], high='more smokes per game'),
    dict(id='who', name='Who it is for', headline='teammate_pct', keys=['teammate_pct', 'stacked_pct', 'radar_ca_inside_pct'], high='more smokes laid for a teammate'),
    dict(id='where', name='Where', headline='inside_cap_pct', keys=['edge_m', 'inside_cap_pct', 'centre_pct'], high='more smokes inside a cap'),
    dict(id='movement', name='Movement', headline='parked_pct', keys=['pushing_pct', 'kiting_pct', 'parked_pct'], high='more smokes laid while parked'),
    dict(id='buys', name='What it buys', headline='conc_pg', keys=['conc_per_smoke', 'conc_pg', 'took_pct', 'held_pct', 'deaths_per100'], high='more concealed damage per game'),
]
LABEL = dict(long_ships_pg='Long-smoke destroyers per game', sitter_ships_pg='Cap-sitter destroyers per game', smoke_dd_pg='Destroyers carrying smoke per game',
             smoke_cruisers_pg='Cruisers carrying smoke per game', exhaust_ships_pg='Exhaust-smoke ships per game', parked_cruisers_pg='Svea or Jinan per game',
             smoke_ships_pg='Ships carrying smoke per game', dd_pg='Destroyers per game', radar_ships_pg='Radar ships per game',
             smokes_pg='Smokes per game', first_smoke_s='First smoke of the game (median, s)', late_pct='Smokes after 12:00 (%)', early_pct='Smokes before 5:00 (%)',
             teammate_pct='For a teammate (%)', selfish_pct='Selfish (%)', stacked_pct='Stacked on a teammate (%)', radar_ca_inside_pct='Radar cruiser inside (% of destroyer smokes)',
             cruiser_inside_pct='Any cruiser inside (% of destroyer smokes)', edge_m='Median distance to cap edge (m)', inside_cap_pct='Inside a cap (%)', centre_pct='Centre lane (%)',
             own_half_pct='Own side of the front line (%)', pushing_pct='Pushing (%)', kiting_pct='Kiting (%)', parked_pct='Parked (%)', sideways_pct='Sideways (%)',
             conc_per_smoke='Concealed damage per smoke', conc_pg='Concealed damage per game', caps_taken_pg='Caps taken next to a smoke per game',
             cap_won_pg='Smokes with the batch cap-won flag per game', cap_def_pg='Batch cap-defended flag per game (secondary: fires for any owned cap with an enemy inside)', took_pct='Nearest cap taken (% of smokes where it was not ours)',
             held_pct='Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy\'s)', deaths_per100='Deaths per 100 smokes', deaths_pg='Deaths in or behind smoke per game')
DIRECTION = {k: 'high = more / larger' for k in LABEL}
DIRECTION.update(first_smoke_s='high = later first smoke', edge_m='high = farther from the cap', deaths_per100='high = more deaths (worse)', deaths_pg='high = more deaths (worse)')
ALLKEYS = [k for k in LABEL]
PCA_KEYS = [k for d in DIMS for k in d['keys']]
GROUP_OF = {k: d['id'] for d in DIMS for k in d['keys']}

def boot_clan(clan, reps=600):
    """95% interval for every number of one clan, resampling that clan's games."""
    gs = GAMES[clan]; acc = collections.defaultdict(list)
    for _ in range(reps):
        f = feats(clan, random.choices(gs, k=len(gs)))
        for k in ALLKEYS:
            if f[k] is not None: acc[k].append(f[k])
    out = {}
    for k, v in acc.items():
        v.sort(); out[k] = (v[int(.025 * len(v))], v[max(0, int(.975 * len(v)) - 1)])
    return out

def pctile(v, pool):
    """0-100 position of v among the pool (the clans with 7+ games): share of the pool below it, ties counted half.
    0 = lowest, 100 = highest, rescaled so the lowest clan in the pool is 0 and the highest is 100."""
    if v is None: return None
    n = len(pool); below = sum(1 for x in pool if x < v); eq = sum(1 for x in pool if x == v)
    if v in pool:
        r = below + (eq - 1) / 2          # 0-based average rank
        return 100 * r / (n - 1)
    return 100 * min(n - 1, max(0, below + eq / 2 - 0.5)) / (n - 1)

# ---------- small linear algebra, by hand
def zmatrix(rows, keys, ref=None):
    """z-scores of rows (list of dicts) on keys; mean and sd taken from ref rows (default: the rows themselves)."""
    ref = ref or rows
    mu = [mean(r[k] for r in ref) for k in keys]; sd = [statistics.pstdev([r[k] for r in ref]) or 1 for k in keys]
    return [[(r[k] - m) / s for k, m, s in zip(keys, mu, sd)] for r in rows]
def corr(Z):
    n, p = len(Z), len(Z[0])
    return [[sum(Z[i][a] * Z[i][b] for i in range(n)) / n for b in range(p)] for a in range(p)]
def jacobi(A, sweeps=60):
    """Eigenvalues and eigenvectors of a symmetric matrix (cyclic Jacobi rotations). Returns [(value, vector)] largest first."""
    n = len(A); A = [r[:] for r in A]; V = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-18: break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-15: continue
                th = (A[q][q] - A[p][p]) / (2 * A[p][q]); t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1); s = t * c
                for k in range(n):
                    a, b = A[k][p], A[k][q]; A[k][p], A[k][q] = c * a - s * b, s * a + c * b
                for k in range(n):
                    a, b = A[p][k], A[q][k]; A[p][k], A[q][k] = c * a - s * b, s * a + c * b
                for k in range(n):
                    a, b = V[k][p], V[k][q]; V[k][p], V[k][q] = c * a - s * b, s * a + c * b
    ev = sorted(((A[i][i], [V[k][i] for k in range(n)]) for i in range(n)), key=lambda x: -x[0])
    return ev
def pca(Z):
    ev = jacobi(corr(Z)); tot = sum(v for v, _ in ev)
    shares = [v / tot for v, _ in ev]
    scores = [[sum(z[j] * vec[j] for j in range(len(z))) for _, vec in ev[:3]] for z in Z]
    return shares, [vec for _, vec in ev], scores
def dist(a, b): return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
def kmeans(Z, k, restarts=60, rng=random):
    best = None; n = len(Z)
    for _ in range(restarts):
        cen = [Z[i][:] for i in rng.sample(range(n), k)]; lab = None
        for _ in range(50):
            new = [min(range(k), key=lambda c: dist(z, cen[c])) for z in Z]
            if new == lab: break
            lab = new
            for c in range(k):
                m = [Z[i] for i in range(n) if lab[i] == c]
                if m: cen[c] = [mean(col) for col in zip(*m)]
        inertia = sum(dist(Z[i], cen[lab[i]]) ** 2 for i in range(n))
        if best is None or inertia < best[0] - 1e-9: best = (inertia, lab[:])
    return best[1], best[0]
def hier(Z, k):
    """Average-linkage agglomerative clustering cut into k groups."""
    cl = [[i] for i in range(len(Z))]
    D = [[dist(a, b) for b in Z] for a in Z]
    while len(cl) > k:
        best = None
        for a in range(len(cl)):
            for b in range(a + 1, len(cl)):
                d = mean(D[i][j] for i in cl[a] for j in cl[b])
                if best is None or d < best[0]: best = (d, a, b)
        _, a, b = best; cl[a] += cl[b]; del cl[b]
    lab = [0] * len(Z)
    for c, m in enumerate(cl):
        for i in m: lab[i] = c
    return lab
def silhouette(Z, lab):
    n = len(Z); out = []
    for i in range(n):
        own = [dist(Z[i], Z[j]) for j in range(n) if j != i and lab[j] == lab[i]]
        if not own: out.append(0); continue
        a = mean(own); b = min(mean(dist(Z[i], Z[j]) for j in range(n) if lab[j] == c) for c in set(lab) if c != lab[i])
        out.append((b - a) / max(a, b))
    return mean(out)
def ari(a, b):
    """Adjusted Rand index of two labelings (1 = identical grouping, about 0 = chance)."""
    n = len(a); c2 = lambda x: x * (x - 1) / 2
    tab = C(zip(a, b)); sa = C(a); sb = C(b)
    idx = sum(c2(v) for v in tab.values()); ea = sum(c2(v) for v in sa.values()); eb = sum(c2(v) for v in sb.values())
    exp = ea * eb / c2(n); mx = (ea + eb) / 2
    return (idx - exp) / (mx - exp) if mx != exp else 1.0
