# Round 5b, worker n2: shared helpers. Ship-smoke pairs with real health and positions from the tracks.
# Used by n2_health.py, n2_danger.py, n2_leave.py, n2_radar.py. Run those as: python -I -X utf8 <script>.py
import sys, os
HERE_ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE_))
from r5lib import *
from tl import *
import json, math, random, bisect
FIGS = os.path.join(R5, 'figures')
MIN_N = 8
GRACE = 20.0          # the batch's death grace: a death up to 20 s after the smoke cleared still belongs to the smoke
STEP = 2.0            # track sampling step, seconds
S, G = load5(); add_times(S)
for s in S:
    s['E1'] = s['e1'] if s['e1'] is not None else s['e0'] + (s['emission_s'] or 0) + (s['life_s'] or 0)
    s['e1_known'] = s['e1'] is not None
DD = [s for s in S if s['cls'] == 'destroyer']
SID = {(s['game'], str(s['id'])): s for s in S}
TOPS = lambda ss: [s for s in ss if s['grp'] == 'top']
RESTS = lambda ss: [s for s in ss if s['grp'] == 'rest']
STATES = ['ahead 50+', 'level', 'behind 50+']
MAPL = sorted(MAPS, key=lambda m: -sum(s['map'] == m for s in S))
MAPL = [m for m in MAPL if any(s['map'] == m for s in S)]
def r1(x, d=1): return None if x is None else round(x, d)
def sm(n): return 'too few' if n < MIN_N else 'small n' if n < 15 else ''
def fv(x, f='{:.1f}'): return 'too few' if x is None else f.format(x)
def state_at(s, t):
    """Score state of the smoking team at elapsed t, from the score timeline."""
    g = TL(s['game']); a, b = g.score_at(s['team'], t), g.score_at(s['opponent'], t)
    return None if a is None or b is None else score_state(a - b)

def samples(tr, t0, t1):
    """Indices of track samples with t0 <= t <= t1."""
    return range(bisect.bisect_left(tr.t, t0), bisect.bisect_right(tr.t, t1))

_pairs = None
def build_pairs():
    """One record per ship a smoke covered (smoker, inside, behind, line_of_fire), with real health from the ship's own track.
    Fields: s (smoke), x (the r5lib shelter entry), eid, cls, how, own (track from the ship's own team's replay: health trusted),
      ok (own track and health known at e0), died (batch smoke death, same as round 5), td (track death time or None),
      died_win (track death in [e0, E1 + 20 s]), h0, maxhp, h1 (health at E1, 0 when dead by then),
      net (share of max health lost from e0 to E1, never below 0),
      trough (largest fall from a running high inside [e0, E1], share of max health),
      hurt (died or net >= 1/3), hurt_pt (died or trough >= 1/3),
      drop_t, drop_pos, drop_share (time, raw position and size of the largest 2 s health fall in [e0, E1], to E1 + 20 s if it died),
      death_pos (raw, last alive position), p0 (raw position at e0), pmid (raw position half way through the smoke)."""
    global _pairs
    if _pairs is not None: return _pairs
    out = []
    for s in S:
        g = TL(s['game']); e0, E1 = s['e0'], s['E1']
        xs = list(s['shelter'])
        if s['smoker_eid'] not in {x['eid'] for x in xs}:
            # the smoker was never concealed by its own smoke (batch how = none): keep it at risk so rates stay per 100 smokes
            xs.append(dict(eid=s['smoker_eid'], ship=s['ship'], cls=s['cls'], how='smoker', taken=0.0, hp_est=None, died=False, hurt=False, uncovered=True))
        for x in xs:
            tr = g.tracks.get(x['eid'])
            p = dict(s=s, x=x, eid=x['eid'], cls=x['cls'], how=x['how'], ship=x['ship'], died=x['died'], own=bool(tr and tr.own), tr=tr, ok=False, td=None, died_win=False)
            out.append(p)
            if tr is None: continue
            td = tr.death_t(); p['td'] = td
            p['died_win'] = td is not None and e0 <= td <= E1 + GRACE + STEP
            p['death_pos'] = tr.last_alive_pos() if td is not None else None
            p['p0'] = tr.pos(e0); p['pmid'] = tr.pos((e0 + min(E1, tr.t[-1])) / 2)
            h = tr.health(e0)
            if h is None or not h[1]: continue
            h0, mx = h; p['h0'], p['maxhp'] = h0, mx
            dead_by_end = td is not None and td <= E1
            h1 = 0.0 if dead_by_end else (tr.health(min(E1, tr.t[-1])) or (h0, mx))[0]
            p['h1'] = h1; p['net'] = max(0.0, h0 - h1) / mx
            hi = h0; tro = 0.0
            for i in samples(tr, e0, E1):
                v = 0.0 if not tr.alive[i] else tr.hp[i]
                if v is None: continue
                hi = max(hi, v); tro = max(tro, hi - v)
            p['trough'] = tro / mx
            p['hurt'] = p['died'] or p['net'] >= HURT_SHARE; p['hurt_pt'] = p['died'] or p['trough'] >= HURT_SHARE
            best = (0.0, None); prev = h0
            for i in samples(tr, e0, E1 + (GRACE + STEP if p['died'] else 0)):
                v = 0.0 if not tr.alive[i] else tr.hp[i]
                if v is None: continue
                if prev - v > best[0]: best = (prev - v, i)
                prev = v
            p['drop_t'] = p['drop_pos'] = None; p['drop_share'] = 0.0
            if best[1] is not None:
                i = best[1]; j = i
                while j > 0 and tr.x[j] is None: j -= 1
                p['drop_t'] = tr.t[i]; p['drop_pos'] = (tr.x[j], tr.z[j]) if tr.x[j] is not None else None; p['drop_share'] = best[0] / mx
            p['ok'] = p['own']
    _pairs = out
    return out

def npt(s, p):
    return norm(s['map'], s['side'], p[0], p[1]) if p else None

def clus_ci(items, stat, key=lambda p: p['s']['team'], reps=1000, rng=None):
    """95% interval of stat(items), resampling whole clans. items are pair records (or anything with a clan key)."""
    rng = rng or random
    cl = collections.defaultdict(list)
    for p in items: cl[key(p)].append(p)
    keys = sorted(cl); out = []
    for _ in range(reps):
        v = stat([x for c in rng.choices(keys, k=len(keys)) for x in cl[c]])
        if v is not None: out.append(v)
    if len(out) < 20: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def grp_ci(items, stat, key=lambda p: p['s']['team'], reps=1000, rng=None):
    """95% interval of stat(Top 6 items) - stat(Rest items), clans resampled inside each group."""
    rng = rng or random
    cl = collections.defaultdict(list)
    for p in items: cl[key(p)].append(p)
    tops = sorted(c for c in cl if c in TOP); rest = sorted(c for c in cl if c not in TOP)
    if not tops or not rest: return (None, None)
    out = []
    for _ in range(reps):
        a = stat([x for c in rng.choices(tops, k=len(tops)) for x in cl[c]]); b = stat([x for c in rng.choices(rest, k=len(rest)) for x in cl[c]])
        if a is not None and b is not None: out.append(a - b)
    if len(out) < 20: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def fci(c, f='{:+.1f}'):
    if c is None or c[0] is None: return '-'
    return f'{f.format(c[0])} to {f.format(c[1])}' + (' *' if c[0] * c[1] > 0 else '')
def dump(name, obj):
    json.dump(obj, open(os.path.join(HERE_, name), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)

# ---- radar log
def lit_rows(s, eid, t0, t1):
    """Radar lit rows of ship eid that overlap [t0, t1] (attributed and unattributed)."""
    return [r for r in TL(s['game']).lit('radar', target=eid) if r['lit_start_elapsed_s'] is not None and r['lit_start_elapsed_s'] <= t1 and (r['lit_end_elapsed_s'] if r['lit_end_elapsed_s'] is not None else r['lit_start_elapsed_s']) >= t0]
def add_radar_flags():
    """Per smoke, from the radar log: rad_any (a covered ship, any role, was radar-lit at some moment while the smoke stood),
    rad_in (same, and the log places the ship in this smoke at the lit moment), rad_core (smoker / inside / behind ships only)."""
    for s in S:
        if 'rad_any' in s: return
        sid = int(s['id']); a = b = c = False
        for x in s['shelter']:
            rows = lit_rows(s, x['eid'], s['e0'], s['E1'])
            if rows:
                a = True
                if x['how'] != 'line_of_fire': c = True
                if any(sid in r['target_in_smoke'] for r in rows): b = True
        s['rad_any'], s['rad_in'], s['rad_core'] = a, b, c

# ---- puffs: when each one is gone
def puff_ends(s):
    """Dispersal time of every puff: the last puff goes at E1, earlier ones go earlier by their share of the emission time."""
    n = len(s['path']); em = s.get('obs_emission_s') or s['emission_s'] or 0
    return [s['E1'] - em * (1 - (k / (n - 1) if n > 1 else 1)) for k in range(n)]
def in_outline(s, p):
    return in_smoke(s, p)
def in_standing(s, p, t, ends=None):
    """True when raw point p is within one smoke radius of a puff that still stands at t."""
    ends = ends or puff_ends(s); r = s['radius_m'] / WU
    return any(math.hypot(p[0] - x, p[1] - z) <= r and t <= e + STEP for (x, z), e in zip(s['path'], ends))
