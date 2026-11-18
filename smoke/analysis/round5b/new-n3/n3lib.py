# Round 5b worker n3: shared helpers (B3 Harugumo per shot, C5 Loop Daring after radar).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
import json, math, random, csv
HERE_N3 = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(os.path.dirname(HERE_N3), 'figures')
S, G = load5(); add_times(S)

def end_of(s):
    """Elapsed second at which the smoke had dispersed (computed when the replay ended first)."""
    return s['e1'] if s['e1'] is not None else s['e0'] + (s['emission_s'] or 0) + (s['life_s'] or 0)
def ship_cls(gk, eid):
    return (G[gk]['roster'].get(eid, {}).get('ship_class') or '').lower()
def ship_name(gk, eid):
    return (G[gk]['roster'].get(eid, {}).get('ship') or '?').replace('\xa0', ' ')
def cap_of(gk, letter):
    return next(c for c in G[gk]['caps'] if c['cap'] == letter)
def set_diff(recs, fa, fb, stat, reps=1000):
    """95% interval of stat(records matching fa) - stat(records matching fb), resampling whole clans. Records need 'team'."""
    cl = by([r for r in recs if fa(r) or fb(r)], 'team'); keys = sorted(cl); out = []
    for _ in range(reps):
        pick = [x for c in random.choices(keys, k=len(keys)) for x in cl[c]]
        a = [x for x in pick if fa(x)]; b = [x for x in pick if fb(x)]
        if not a or not b: continue
        va, vb = stat(a), stat(b)
        if va is not None and vb is not None: out.append(va - vb)
    if len(out) < 100: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def bstat(recs, stat, reps=1000):
    cl = by(recs, 'team'); keys = sorted(cl); out = []
    if len(keys) < 3: return (None, None)
    for _ in range(reps):
        v = stat([x for c in random.choices(keys, k=len(keys)) for x in cl[c]])
        if v is not None: out.append(v)
    if len(out) < 100: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def bdiff_groups(recs, stat, reps=1000):
    """Top 6 minus Rest, resampling clans inside each group."""
    cl = by(recs, 'team'); tops = sorted(c for c in cl if c in TOP); rest = sorted(c for c in cl if c not in TOP); out = []
    if not tops or not rest: return (None, None)
    for _ in range(reps):
        a = [x for c in random.choices(tops, k=len(tops)) for x in cl[c]]; b = [x for c in random.choices(rest, k=len(rest)) for x in cl[c]]
        va, vb = stat(a), stat(b)
        if va is not None and vb is not None: out.append(va - vb)
    if len(out) < 100: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def r1(x, d=1): return None if x is None else round(x, d)
def iv(lohi, d=1): return None if lohi is None or lohi[0] is None else [round(lohi[0], d), round(lohi[1], d)]
def clear(lohi): return bool(lohi and lohi[0] is not None and lohi[0] * lohi[1] > 0)
def clans_of(recs):
    c = C(r['team'] for r in recs)
    t = ', '.join(f'{k} {v}' for k, v in c.most_common() if k in TOP) or 'none'
    r = ', '.join(f'{k} {v}' for k, v in c.most_common() if k not in TOP) or 'none'
    return f'Top 6: {t} | Rest: {r}'
def clock(sec): return f'{int(sec) // 60}:{int(sec) % 60:02d}'
