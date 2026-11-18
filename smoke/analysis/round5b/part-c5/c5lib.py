# Part C5 helpers (map-specific questions). Read-only on the batch; writes only under round5/part-c5 and round5/figures.
import sys, os, json
HERE5 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE5))
from r5lib import *

S, G = load5()
DD = [s for s in S if s['cls'] == 'destroyer']
ANALYSIS = os.path.dirname(R5)
FIGDIR = os.path.join(R5, 'figures')
KM = 1000.0 / WU
OUT = {}      # tables for map-questions.json
SPOTS = []    # records for spots.json
CHECK = []    # (id, number, where)

def P(*a): print(*a)
def on(m, pool=None): return [s for s in (S if pool is None else pool) if s['map'] == m]
def zone(s):
    """Cap nearest to the smoke's normalized position, letter as drawn on the minimap (same as round 3 module 4)."""
    return min(map_caps(G, s['map']), key=lambda c: math.hypot(c['x'] - s['nx'], c['z'] - s['nz']) - c['r'])['cap']
for s in S: s['zone'] = zone(s)

def gap(pool, pred, reps=1000):
    """Share of Top 6 smokes and of Rest smokes in pool where pred, with the 95% interval of the difference (clans resampled)."""
    t = [s for s in pool if s['grp'] == 'top']; r = [s for s in pool if s['grp'] == 'rest']
    f = lambda v: pct(v, pred)
    lo, hi = boot_diff(pool, f, reps=reps) if t and r else (None, None)
    kt, kr = sum(1 for s in t if pred(s)), sum(1 for s in r if pred(s))
    d = dict(top_k=kt, top_n=len(t), rest_k=kr, rest_n=len(r), top_pct=round(f(t), 1) if t else None, rest_pct=round(f(r), 1) if r else None,
             gap=round(f(t) - f(r), 1) if t and r else None, lo=round(lo, 1) if lo is not None else None, hi=round(hi, 1) if hi is not None else None)
    d['clear'] = bool(lo is not None and lo * hi > 0)
    d['mark'] = 'Top 6' if d['clear'] and d['gap'] > 0 else 'Shared'
    return d
def gtxt(d):
    f = lambda k, n, p: f'{k} of {n} ({p:.0f}%)' if n >= 8 else f'{k} of {n} (too few)'
    ci_ = f'{d["gap"]:+.0f} pts ({d["lo"]:+.0f} to {d["hi"]:+.0f}{" *" if d["clear"] else ""})' if d['gap'] is not None and d['lo'] is not None else '-'
    return f'Top 6 {f(d["top_k"], d["top_n"], d["top_pct"] or 0)} vs Rest {f(d["rest_k"], d["rest_n"], d["rest_pct"] or 0)}; gap {ci_}'
def rate_ci(ss, pred, reps=1000):
    """Share with pred (percent) and its 95% interval, clans resampled."""
    if len(ss) < 8: return None, (None, None)
    return pct(ss, pred), boot_stat(ss, lambda v: pct(v, pred), reps=reps)
def rtxt(ss, pred):
    k = sum(1 for s in ss if pred(s))
    if len(ss) < 8: return f'{k} of {len(ss)} (too few)'
    p, (lo, hi) = rate_ci(ss, pred)
    return f'{k} of {len(ss)} ({p:.0f}%, {lo:.0f} to {hi:.0f}){small(len(ss))}'
def r4_spot(sid):
    return next(x for x in json.load(open(os.path.join(ANALYSIS, 'round4', 'part-b', 'spots.json'), encoding='utf-8')) if x['id'] == sid)
def in_r4(rec, s):
    """Is the smoke centre inside a round 4 spot ellipse (rebuilt from its 0-1 frame record)."""
    size = MAPS[rec['map']]['space_size']; u, v = rec['centre_uv']
    cx, cz = u * size - size / 2, size / 2 - v * size
    r1, r2 = rec['ellipse_uv']['ru'] * size, rec['ellipse_uv']['rv'] * size; ang = -math.radians(rec['ellipse_uv']['angle_deg'])
    dx, dz = s['nx'] - cx, s['nz'] - cz; ca, sa = math.cos(ang), math.sin(ang)
    a, b = dx * ca + dz * sa, -dx * sa + dz * ca
    return (a / r1) ** 2 + (b / r2) ** 2 <= 1.0
def ell_shape(rec):
    return dict(type='ellipse', u=rec['centre_uv'][0], v=rec['centre_uv'][1], **rec['ellipse_uv'])
def ell_svg(p, rec, stroke=INK, width=2, dash=None):
    size = MAPS[rec['map']]['space_size']; u, v = rec['centre_uv']
    px, py = p.xy(u * size - size / 2, size / 2 - v * size)
    d = f' stroke-dasharray="{dash}"' if dash else ''
    p.raw(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{rec["ellipse_uv"]["ru"] * p.size:.1f}" ry="{rec["ellipse_uv"]["rv"] * p.size:.1f}" transform="rotate({rec["ellipse_uv"]["angle_deg"]} {px:.1f} {py:.1f})" fill="none" stroke="{stroke}" stroke-width="{width}"{d}/>')
def cellnm(m, x, z): return cell_name(*cell(m, x, z))
def capnear(m, x, z):
    c = min(map_caps(G, m), key=lambda c: math.hypot(c['x'] - x, c['z'] - z) - c['r'])
    return c['cap'], (math.hypot(c['x'] - x, c['z'] - z) - c['r']) * WU
def games_on(m): return [g for g in G.values() if g['map'] == m]
def tgames(m=None): return [(k, t) for k, t in team_games(G) if m is None or G[k]['map'] == m]
def grp_of(team): return 'top' if team in TOP else 'rest'
def clock(sec): return f'{int(sec) // 60}:{int(sec) % 60:02d}'
def kf(x): return '-' if x is None else f'{x / 1000:.1f}k'
def uvrect(m, x0, z0, x1, z1):
    (u0, v0), (u1, v1) = uv(m, x0, z1), uv(m, x1, z0)
    return dict(type='polygon', points=[[round(u0, 4), round(v0, 4)], [round(u1, 4), round(v0, 4)], [round(u1, 4), round(v1, 4)], [round(u0, 4), round(v1, 4)]])
def save_json(name, obj):
    json.dump(obj, open(os.path.join(HERE5, name), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)

def atlas_spot(sid):
    x = next(x for x in json.load(open(os.path.join(ANALYSIS, 'atlas', 'spots.json'), encoding='utf-8'))['spots'] if x['id'] == sid)
    x = dict(x); x['ellipse_uv'] = {k: x['shape'][k] for k in ('ru', 'rv', 'angle_deg')}
    return x
def second_dds(s):
    """Allied destroyers other than the smoker with a recorded position when the smoke was fully laid."""
    m = s['map']; out = []
    for c in s['cast']:
        if c['ally'] and c['cls'] == 'destroyer' and not c['is_smoker']:
            cp, ed = capnear(m, c['nx'], c['nz'])
            out.append(dict(ship=c['ship'], cell=cellnm(m, c['nx'], c['nz']), cap=cp, cap_edge_m=round(ed), dist_m=round(c['dist_m']), fwd_m=round(c['fwd_m']), how=c['how'], nx=c['nx'], nz=c['nz']))
    return out
def other_dds_alive(s):
    """Ship names of the smoking team's other destroyers still alive when the smoke was fully laid (roster and death times)."""
    g = G[s['game']]; t = s['j']['t_capture']['seconds'] if s['j'].get('t_capture') else s['j']['t_activate']['seconds']
    return [p['ship'].replace('\xa0', ' ') for e, p in g['roster'].items() if p['team'] == s['team'] and p['ship_class'].lower() == 'destroyer' and e != s['smoker_eid']
            and not (p['death'] and p['death']['seconds'] <= t)]
def cap_table(m, pool=None, edge=None):
    """Per cap zone on a map: owner at activation, enemy took / we took (nearest cap, r5lib), cap_defended for that cap."""
    rows = {}
    for z, v in sorted(by([s for s in on(m, pool) if edge is None or s['near_cap_edge_m'] <= edge], 'zone').items()):
        kn = [s for s in v if s['enemy_took'] is not None]; ours = [s for s in kn if s['near_own'] == 'ours']
        wk = [s for s in v if s['we_took'] is not None]
        rows[z] = dict(n=len(v), top6=sum(s['grp'] == 'top' for s in v), ours=sum(s['near_own'] == 'ours' for s in v), neutral=sum(s['near_own'] == 'neutral' for s in v),
                       theirs=sum(s['near_own'] == 'theirs' for s in v), enemy_took_k=sum(1 for s in kn if s['enemy_took']), enemy_took_n=len(kn),
                       enemy_took_ours_k=sum(1 for s in ours if s['enemy_took']), enemy_took_ours_n=len(ours),
                       we_took_k=sum(1 for s in wk if s['we_took']), we_took_n=len(wk),
                       cap_defended_this_cap=sum(1 for s in v if s['r']['cap_defended'] == s['near_cap']),
                       conc=round(mean(s['conc'] for s in v)), deaths_per_100=round(rate100(v, 'deaths'), 1))
    return rows
def cap_md(rows):
    f = lambda k, n: f'{k} of {n}' + (f' ({100 * k / n:.0f}%)' if n >= 8 else ' (too few)')
    return md_table(['Cap', 'Smokes', 'Top 6', 'Ours at start', 'Neutral', 'Theirs', 'Enemy took it (of smokes where it was not theirs and a later snapshot exists)', 'Enemy took it when ours', 'We took it (of not ours)', 'Batch "cap defended" on this cap', 'Concealed dmg', 'Deaths per 100'],
                    [[z, r['n'], r['top6'], r['ours'], r['neutral'], r['theirs'], f(r['enemy_took_k'], r['enemy_took_n']), f(r['enemy_took_ours_k'], r['enemy_took_ours_n']), f(r['we_took_k'], r['we_took_n']),
                      r['cap_defended_this_cap'], kf(r['conc']), r['deaths_per_100']] for z, r in rows.items()])
def cc(counter, k=8): return ', '.join(f'{a} {b}' for a, b in counter.most_common(k)) or 'none'

def mean_shift(pts, h_km=2.0, merge_km=1.0):
    """Same Gaussian mean-shift as atlas/scripts/atlas_lib.py (2 km bandwidth, peaks within 1 km merged), so atlas clusters can be rebuilt exactly."""
    h, merge = h_km * KM, merge_km * KM
    modes = []
    for (x, z) in pts:
        for _ in range(200):
            w = [math.exp(-((a - x) ** 2 + (b - z) ** 2) / (2 * h * h)) for a, b in pts]
            sw = sum(w); x2, z2 = sum(wi * p[0] for wi, p in zip(w, pts)) / sw, sum(wi * p[1] for wi, p in zip(w, pts)) / sw
            if math.hypot(x2 - x, z2 - z) < 0.02: break
            x, z = x2, z2
        modes.append((x, z))
    labels, centres = [], []
    for mo in modes:
        for i, c in enumerate(centres):
            if math.hypot(mo[0] - c[0], mo[1] - c[1]) <= merge: labels.append(i); break
        else:
            centres.append(mo); labels.append(len(centres) - 1)
    out = collections.defaultdict(list)
    for i, l in enumerate(labels): out[l].append(i)
    return sorted(out.values(), key=lambda v: -len(v))
def ms_cluster(pool, cellname, h_km=2.0):
    """The mean-shift cluster of `pool` (smoke centres) whose most common grid cell is `cellname` (how the atlas names its clusters)."""
    for idx in mean_shift([(s['nx'], s['nz']) for s in pool], h_km):
        cs = [pool[i] for i in idx]
        if C(s['ncell_name'] for s in cs).most_common(1)[0][0] == cellname: return cs
    return []
