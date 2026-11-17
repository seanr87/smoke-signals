# Module 2 shared prep: early smokes (first 5 minutes) by Harugumo, Somers, Gearing, and each team's opening smokes.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
OUT = os.path.dirname(os.path.abspath(__file__))
S, G = load()
SHIPS = ('Harugumo', 'Somers', 'Gearing')
WIN_LABEL = ['0-2 min', '2-4 min', '4-5 min']
RI, RN = 'radar cruiser inside', 'radar cruiser, not inside'
PT_ORDER = [RI, RN, 'non-radar cruiser', 'battleship only', 'none']
SHIP_COLOR = {'Harugumo': VIOLET, 'Somers': BLUE, 'Gearing': GREEN}

def window(el): return 0 if el < 120 else 1 if el < 240 else 2 if el < 300 else 3
def ptype(s):
    """Partner type of a smoke. Headline definition (round 4): a radar cruiser INSIDE the smoke (radar_ca_inside). Then a radar cruiser
    covered but only behind / in the line of fire, then a non-radar cruiser, then battleship only; destroyer-only or no partner = none."""
    ps = s['partners']
    if s['radar_ca_inside']: return RI
    if s['radar_ca_any']: return RN
    if any(p['cls'] == 'cruiser' for p in ps): return 'non-radar cruiser'
    if any(p['cls'] == 'battleship' for p in ps): return 'battleship only'
    return 'none'
def main_partner(s):
    """The partner that defines the smoke's partner type (longest concealed among those of that type)."""
    t = s['pt']
    ps = [p for p in s['partners'] if (t == RI and p['cls'] == 'cruiser' and p['radar'] and p['how'] == 'inside') or (t == RN and p['cls'] == 'cruiser' and p['radar'])
          or (t == 'non-radar cruiser' and p['cls'] == 'cruiser') or (t == 'battleship only' and p['cls'] == 'battleship')]
    return max(ps, key=lambda p: p['secs'] or 0) if ps else None
def fwd(mapname):
    """Unit vector pointing from own spawn toward the enemy spawn in the normalized frame."""
    return (0.7071, 0.7071) if mapname in DIAGONAL else (0.0, 1.0)
for s in S:
    s['w'] = window(s['el']); s['pt'] = ptype(s); s['mp'] = main_partner(s)
    g = G[s['game']]
    nc = next((c for c in ncaps(g, s['map'], s['side']) if c['cap'] == s['cap']), None)  # contested cap in the normalized frame
    s['capxz'] = (nc['x'], nc['z'], nc['r']) if nc else None
E = [s for s in S if s['ship'] in SHIPS and s['el'] < 300]
DDE = [s for s in S if s['cls'] == 'destroyer' and s['el'] < 300]  # Module 3 population: every early destroyer smoke

def boot_cmp(a, b, stat, reps=1000):
    """95% interval of stat(a) - stat(b), resampling clans across the pooled set (a clan keeps its smokes in both sets)."""
    for x in a: x['_ab'] = 0
    for x in b: x['_ab'] = 1
    cl = by(a + b, 'team'); keys = list(cl); out = []
    for _ in range(reps):
        smp = [x for c in random.choices(keys, k=len(keys)) for x in cl[c]]
        va, vb = stat([x for x in smp if x['_ab'] == 0]), stat([x for x in smp if x['_ab'] == 1])
        if va is not None and vb is not None: out.append(va - vb)
    if not out: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]

# ---------- opening playbook: one record per team-game
def first_cap(gkey):
    """(elapsed, {team: [caps]}) at the first snapshot where any cap has an owner, else None."""
    for el, sc, caps in snapshots(S, gkey):
        own = {c: o for c, o in caps.items() if o}
        if own:
            d = collections.defaultdict(list)
            for c, o in own.items(): d[o].append(c)
            return el, dict(d)
    return None
def lead300(gkey):
    """(seconds from 5:00, {team: score}) of the snapshot nearest 300 s elapsed."""
    sn = snapshots(S, gkey)
    if not sn: return None
    el, sc, _ = min(sn, key=lambda x: abs(x[0] - 300))
    return abs(el - 300), sc
def openings():
    out = []
    bygame = by(S, 'game')
    for k, g in G.items():
        fc = first_cap(k); l5 = lead300(k)
        for t in g['teams']:
            opp = next(o for o in g['teams'] if o != t)
            ss = sorted((s for s in bygame.get(k, []) if s['team'] == t), key=lambda s: s['el'])[:2]
            rec = dict(game=k, team=t, grp='top' if t in TOP else 'rest', map=g['map'], side=g['sides'][t], win=g['winner'] == t, smokes=ss, n=len(ss))
            rec['fc'] = None; rec['fc_el'] = None; rec['fc_caps'] = []
            if fc:
                el, own = fc
                rec['fc_el'] = el
                if len(own) == 1: rec['fc'] = 1 if t in own else 0
                else: rec['fc'] = 0.5  # both teams already hold a cap at the first snapshot that shows any owner
                rec['fc_caps'] = [ncap_name(g, g['map'], g['sides'][t], c) for c in own.get(t, [])]
            rec['lead'] = None; rec['lead_gap'] = None
            if l5 and t in l5[1] and opp in l5[1]:
                rec['lead_gap'] = l5[0]
                if l5[0] <= 60: rec['lead'] = l5[1][t] - l5[1][opp]
            out.append(rec)
    return out
