# Module 4 helpers (key terrain). Read-only on the batch.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *

MIN_N = 8       # a cell or zone is not rated below this
SOLID_N = 15    # 8 to 14 is flagged small n
HIGH_X, LOW_X = 1.4, 0.6   # high / low cell: concealed damage per smoke at least 1.4x / at most 0.6x the map average

S, G = load()
DD = [s for s in S if s['cls'] == 'destroyer']
GAMES_PER_MAP = C(g['map'] for g in G.values())
MAP_ORDER = sorted(MAPS, key=lambda m: -sum(s['map'] == m for s in DD))

def zone(s):
    """Letter of the cap nearest to the smoke's normalized position (distance to the cap edge), as drawn on the map sheet.
    Not the same as s['ncap'], which is the cap the batch calls 'contested' for that smoke and can be a different cap."""
    return min(map_caps(G, s['map']), key=lambda c: math.hypot(c['x'] - s['nx'], c['z'] - s['nz']) - c['r'])['cap']
for s in DD: s['zone'] = zone(s)

conc = lambda v: mean(s['conc'] for s in v)
d100 = lambda v: 100 * mean(s['deaths'] for s in v)
capw = lambda v: pct(v, lambda s: s['cap_won'])
def stats(v):
    return dict(n=len(v), conc=conc(v), med=med(s['conc'] for s in v), d100=d100(v), deaths=sum(s['deaths'] for s in v), capw=capw(v),
                top=sum(s['grp'] == 'top' for s in v), win=pct(v, lambda s: s['win']), clans=len(set(s['team'] for s in v)), games=len(set(s['game'] for s in v)),
                el=med(s['el'] for s in v))
def in_out_ci(ms, pred, stat=conc, reps=1000):
    """95% interval of stat(smokes where pred) - stat(the map's other smokes), resampling clans."""
    def f(v):
        a = [s for s in v if pred(s)]; b = [s for s in v if not pred(s)]
        return stat(a) - stat(b) if a and b else None
    return boot_stat(ms, f, reps=reps)
def share_ci(ms, pred, reps=1000):
    """Top 6 share minus rest share of smokes where pred (percentage points), with interval."""
    f = lambda v: pct(v, pred)
    t = [s for s in ms if s['grp'] == 'top']; r = [s for s in ms if s['grp'] == 'rest']
    return f(t), f(r), boot_diff(ms, f, reps=reps)
def map_cells(m):
    ms = [s for s in DD if s['map'] == m]
    avg = conc(ms)
    cells = {k: stats(v) for k, v in by(ms, 'ncell').items()}
    for k, st in cells.items():
        st['rated'] = st['n'] >= MIN_N; st['small'] = MIN_N <= st['n'] < SOLID_N
        st['mark'] = ('high' if st['conc'] >= HIGH_X * avg else 'low' if st['conc'] <= LOW_X * avg else '') if st['rated'] else ''
    return ms, avg, cells
def k(x): return '-' if x is None else f'{x/1000:.1f}k'
