# Round 5b, worker n4: shared prep for the three page 1 carry-over claims. Read-only on the batch.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
import json, csv, math, random, collections

OUT = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(R5, 'figures')
S, G = load5(); add_times(S)
SHIPS3 = ('Harugumo', 'Somers', 'Gearing')
MAPORDER = ['Sleeping Giant', 'Hotspot', 'Mountain Range', 'Land of Fire', 'Loop', 'Okinawa', 'Sea of Fortune']
IDX = {(s['game'], int(s['id'])): s for s in S}
TG = team_games(G)
GAMES = C(t for _, t in TG)
MAPGAMES = {m: C(t for k, t in TG if G[k]['map'] == m) for m in MAPORDER}
RI, RN = 'radar cruiser inside', 'radar cruiser, not inside'

def end_t(s):
    """Elapsed second at which the smoke had dispersed (brief: e1, or e0 + emission + life when the replay ended first)."""
    return s['e1'] if s['e1'] is not None else s['e0'] + (s['emission_s'] or 0) + (s['life_s'] or 0)
def emit_end(s):
    return s['eend'] if s['eend'] is not None else s['e0'] + (s['emission_s'] or 0)
def ptype(s):
    """Module 2 partner type (round 4 definition)."""
    ps = s['partners']
    if s['radar_ca_inside']: return RI
    if s['radar_ca_any']: return RN
    if any(p['cls'] == 'cruiser' for p in ps): return 'non-radar cruiser'
    if any(p['cls'] == 'battleship' for p in ps): return 'battleship only'
    return 'none'
for s in S:
    s['pt'] = ptype(s); s['end'] = end_t(s); s['emit_end'] = emit_end(s)
    s['play'] = s['pp'] if s['pp'] in ('cap_control', 'radar_trap') else None

E3 = [s for s in S if s['ship'] in SHIPS3 and s['el'] < 300]           # Module 2 population (187)
DDE = [s for s in S if s['cls'] == 'destroyer' and s['el'] < 300]      # Module 3 population (302)
EC = [s for s in S if s['early_cruiser']]                              # round 5 "early cruiser smoke"
DD = [s for s in S if s['cls'] == 'destroyer']
# Round 5 clock bug (two games on a 15-minute clock read 300 s late). r5lib now corrects s['el']; el_bug puts the bug back,
# so the atlas / round 4 populations can be reproduced exactly.
for s in S: s['el_bug'] = s['el'] + CLOCK_OFFSET.get(s['game'], 0)
E3_BUG = [s for s in S if s['ship'] in SHIPS3 and s['el_bug'] < 300]
DDE_BUG = [s for s in S if s['cls'] == 'destroyer' and s['el_bug'] < 300]
CLOCK_NOTE = dict(games=[list(k) for k in CLOCK_OFFSET], smokes=sum(1 for s in S if s['game'] in CLOCK_OFFSET),
                  now_early=sum(1 for s in S if s['el'] < 300 <= s['el_bug']), now_early_dd=sum(1 for s in DDE if s['el_bug'] >= 300),
                  now_early_three=sum(1 for s in E3 if s['el_bug'] >= 300), left_early_dd=sum(1 for s in DDE_BUG if s['el'] >= 300))

def cap_of(g, letter):
    return next((c for c in g['caps'] if c['cap'] == letter), None)
def edge_m(c, p):
    """Metres from raw point p to the edge of cap c (negative inside)."""
    return (math.hypot(p[0] - c['x'], p[1] - c['z']) - c['r']) * WU
def nearest_cap(g, p):
    return min(g['caps'], key=lambda c: edge_m(c, p))

def took(gt, cap, team, t0, t1):
    """Cap timeline test. None when the cap was already the team's at t0; else True when the team owned it at some time in (t0, t1]."""
    if not cap: return None
    if gt.owner_at(cap, t0) == team: return None
    return any(o == team for _, o in gt.owner_changes(cap, t0, t1))
def own_at(gt, cap, team, t):
    o = gt.owner_at(cap, t)
    return 'neutral' if o is None else 'ours' if o == team else 'theirs'

def boot_cmp(a, b, stat, reps=1000):
    """95% interval of stat(a) - stat(b), resampling clans across the pooled set (Module 2 method)."""
    for x in a: x['_ab'] = 0
    for x in b: x['_ab'] = 1
    cl = by(a + b, 'team'); keys = list(cl); out = []
    for _ in range(reps):
        smp = [x for c in random.choices(keys, k=len(keys)) for x in cl[c]]
        va, vb = stat([x for x in smp if x['_ab'] == 0]), stat([x for x in smp if x['_ab'] == 1])
        if va is not None and vb is not None: out.append(va - vb)
    if not out: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def boot_rate_diff(counts, games=None, reps=1000):
    """counts: {team: plays}. 95% interval of plays per team-game, Top 6 minus Rest, resampling clans (Module 3 method)."""
    games = games or GAMES
    tops = [t for t in games if t in TOP]; rest = [t for t in games if t not in TOP]
    if not tops or not rest: return (None, None)
    out = []
    for _ in range(reps):
        a = random.choices(tops, k=len(tops)); b = random.choices(rest, k=len(rest))
        out.append(sum(counts.get(t, 0) for t in a) / sum(games[t] for t in a) - sum(counts.get(t, 0) for t in b) / sum(games[t] for t in b))
    out.sort(); return out[int(.025 * len(out))], out[int(.975 * len(out)) - 1]
def rate(counts, grp, games=None):
    games = games or GAMES
    ts = [t for t in games if (t in TOP) == (grp == 'top')]
    d = sum(games[t] for t in ts)
    return sum(counts.get(t, 0) for t in ts) / d if d else None
def grp(ss, g): return [s for s in ss if s['grp'] == g]
def nclans(ss): return len({s['team'] for s in ss})
def rnd(x, k=1): return None if x is None else round(x, k)
def lohi(t, k=1): return [rnd(t[0], k), rnd(t[1], k)]
def two(ss, stat, k=1, reps=1000):
    """Top 6, Rest, difference and its interval for a statistic over a list of dicts with 'grp' and 'team'."""
    a, b = grp(ss, 'top'), grp(ss, 'rest'); va, vb = stat(a) if a else None, stat(b) if b else None
    lo, hi = boot_diff(ss, stat, reps) if a and b else (None, None)
    return dict(top=rnd(va, k), rest=rnd(vb, k), n_top=len(a), n_rest=len(b), clans_top=nclans(a), clans_rest=nclans(b),
                diff=rnd(va - vb, k) if va is not None and vb is not None else None, ci=lohi((lo, hi), k), clear=bool(lo is not None and lo * hi > 0))
def save(name, obj):
    json.dump(obj, open(os.path.join(OUT, name), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
