# C4: spot catalogue per map (long-smoke, selfish, early cruiser smoke, high-paying cells), each marked Top 6 or Shared.
# Run: python -I -X utf8 c4_spots.py   (read-only on the batch; writes spots.json, generated.md, FINDINGS-C4.md, out.txt, figures)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
OUT = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(R5, 'figures')
S, G = load5()
RNG = random.Random(519)
KM = 1000.0 / WU                       # world units per km
H_KM, MERGE_KM = 1.0, 0.7              # mean-shift bandwidth and peak merge distance
R_MIN, R_MAX, R_SEED = 1.5, 2.5, 2.0   # circle radius limits and the first-pass radius, km
MIN_N, MIN_SHARE = 8, 0.10             # a spot holds >= 8 smokes and >= 10% of that kind's smokes on the map
REPS = 2000
WL_GAP, WL_N = 5000, 5                 # win/loss split is shown when the two means are > 5k apart with n >= 5 on each side
MAPORDER = ['Sleeping Giant', 'Hotspot', 'Loop', 'Mountain Range', 'Land of Fire', 'Sea of Fortune', 'Okinawa']
AB = {'Sleeping Giant': 'sg', 'Hotspot': 'hs', 'Mountain Range': 'mr', 'Land of Fire': 'lof', 'Sea of Fortune': 'sof', 'Loop': 'loop', 'Okinawa': 'oki'}
PARKED = ('Svea', 'Jinan')
FAMILIES = [  # (family, id tag, json kind (None = top6_spot / shared_spot by mode), member test, plain label)
    ('long_smoke', 'long', None, lambda s: s['cls'] == 'destroyer' and s['ship'] in LONG_SHIPS, 'long-smoke'),
    ('cap_sitter', 'sit', 'selfish_spot', lambda s: s['cls'] == 'destroyer' and s['ship'] in SITTERS, 'selfish: cap sitter'),
    ('parked_cruiser', 'park', 'selfish_spot', lambda s: s['ship'] in PARKED, 'selfish: parked cruiser'),
    ('early_cruiser', 'early', 'early_cruiser_spot', lambda s: s['early_cruiser'], 'early cruiser smoke'),
]
LOG = []
def P(*a):
    line = ' '.join(str(x) for x in a); LOG.append(line); print(line)

# ---------- spot finder (all clans pooled)
def modes(pts, h):
    out = []
    for (x, z) in pts:
        for _ in range(100):
            w = [math.exp(-((a - x) ** 2 + (b - z) ** 2) / (2 * h * h)) for a, b in pts]
            sw = sum(w); x2, z2 = sum(wi * p[0] for wi, p in zip(w, pts)) / sw, sum(wi * p[1] for wi, p in zip(w, pts)) / sw
            if math.hypot(x2 - x, z2 - z) < 0.02: break
            x, z = x2, z2
        if not any(math.hypot(x - a, z - b) <= MERGE_KM * KM for a, b in out): out.append((x, z))
    return out
def circle(pts, cx, cz):
    """Settle a circle on a density peak: centre = mean of the points within 2 km (3 passes); radius = 1.6 x the rms distance of
    those points (about the edge of an evenly filled disc), kept between 1.5 and 2.5 km."""
    for _ in range(3):
        near = [p for p in pts if math.hypot(p[0] - cx, p[1] - cz) <= R_SEED * KM]
        if not near: return None
        cx, cz = mean(p[0] for p in near), mean(p[1] for p in near)
    near = [p for p in pts if math.hypot(p[0] - cx, p[1] - cz) <= R_SEED * KM]
    if not near: return None
    rms = math.sqrt(mean((p[0] - cx) ** 2 + (p[1] - cz) ** 2 for p in near))
    r = min(R_MAX * KM, max(R_MIN * KM, 1.6 * rms))
    return cx, cz, r
def find_spots(ss):
    """Greedy: take the densest circle, remove its smokes, repeat. Then give every smoke to the nearest centre whose circle
    holds it, and keep circles with >= MIN_N smokes and >= MIN_SHARE of the pool. Returns [(cx, cz, r, members)]."""
    need = max(MIN_N, math.ceil(MIN_SHARE * len(ss)))
    left = list(ss); circ = []
    while len(left) >= need:
        pts = [(s['nx'], s['nz']) for s in left]
        best = None
        for m in modes(pts, H_KM * KM):
            c = circle(pts, *m)
            if not c: continue
            n = sum(math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] for p in pts)
            if best is None or (n, -c[2]) > (best[0], -best[1][2]): best = (n, c)
        if not best or best[0] < need: break
        c = best[1]; circ.append(c)
        left = [s for s in left if math.hypot(s['nx'] - c[0], s['nz'] - c[1]) > c[2]]
    out = [[c, []] for c in circ]
    for s in ss:
        d = [(math.hypot(s['nx'] - c[0], s['nz'] - c[1]), i) for i, (c, _) in enumerate(out) if math.hypot(s['nx'] - c[0], s['nz'] - c[1]) <= c[2]]
        if d: out[min(d)[1]][1].append(s)
    return [(c[0], c[1], c[2], mem) for c, mem in out if len(mem) >= need]

# ---------- share test (clan resampling)
def share_test(pool, members, topset=TOP, reps=REPS):
    """Share of the top group's pool smokes that are in the spot minus the same for the rest, in points, with a 95% interval
    from resampling whole clans within each group. Returns dict(st, sr, lo, hi, nt, nr, testable)."""
    ids = {id(s) for s in members}
    cl = by(pool, 'team')
    ft = [(sum(id(s) in ids for s in v), len(v)) for c, v in cl.items() if c in topset]
    fr = [(sum(id(s) in ids for s in v), len(v)) for c, v in cl.items() if c not in topset]
    nt, nr = sum(n for _, n in ft), sum(n for _, n in fr)
    st = 100 * sum(x for x, _ in ft) / nt if nt else None; sr = 100 * sum(x for x, _ in fr) / nr if nr else None
    res = dict(st=st, sr=sr, nt=nt, nr=nr, lo=None, hi=None, testable=nt >= MIN_N and nr >= MIN_N)
    if res['testable']:
        o = []
        for _ in range(reps):
            a = RNG.choices(ft, k=len(ft)); b = RNG.choices(fr, k=len(fr))
            o.append(100 * sum(x for x, _ in a) / sum(n for _, n in a) - 100 * sum(x for x, _ in b) / sum(n for _, n in b))
        o.sort(); res['lo'], res['hi'] = o[int(.025 * len(o))], o[max(0, int(.975 * len(o)) - 1)]
    return res
def label(t, members, topset=TOP):
    """'top6' needs: both groups laid >= 8 such smokes on the map, the interval of the share gap is above zero, and at least
    two Top 6 clans are in the spot. Everything else is 'shared' (with a note)."""
    ntc = len({s['team'] for s in members if s['team'] in topset})
    if not t['testable']:
        who = 'Top 6' if t['nt'] < MIN_N else 'Rest'
        return 'shared', f"not testable: {who} laid only {t['nt'] if t['nt'] < MIN_N else t['nr']} such smokes on this map"
    if t['lo'] > 0:
        return ('top6', '') if ntc >= 2 else ('shared', 'gap is clear but only one Top 6 clan is in it')
    if t['hi'] < 0: return 'shared', 'Rest use it more'
    return 'shared', ''

# ---------- describing a place
def where(m, cx, cz):
    caps = map_caps(G, m)
    c = min(caps, key=lambda c: math.hypot(c['x'] - cx, c['z'] - cz) - c['r'])
    dx, dz = cx - c['x'], cz - c['z']; d = math.hypot(dx, dz)
    if m in DIAGONAL:
        f, l = (dx + dz) / math.sqrt(2), (dx - dz) / math.sqrt(2)
        side = ('enemy (north-east) side' if f > 0 else 'own (south-west) side') if abs(f) >= abs(l) else ('south-east side' if l > 0 else 'north-west side')
    else:
        side = ('enemy side' if dz > 0 else 'own side') if abs(dz) >= abs(dx) else ('east side' if dx > 0 else 'west side')
    u, v = uv(m, cx, cz)
    edge = ', west edge of the map' if u < 0.15 else ', east edge of the map' if u > 0.85 else ''
    if d <= c['r']:
        txt = f"inside cap {c['cap']}" + (f", {side}" if d > 0.35 * c['r'] else ', middle')
    elif (d - c['r']) * WU < 400:
        txt = f"on the rim of cap {c['cap']}, {side}"
    else:
        txt = f"{(d - c['r']) * WU / 1000:.1f} km outside cap {c['cap']}, {side}"
    return txt + edge
def cells_of(members):
    c = C(s['ncell_name'] for s in members)
    return [k for k, v in c.most_common() if v >= max(2, 0.15 * len(members))] or [c.most_common(1)[0][0]]
def clock(sec): return f'{int(sec) // 60}:{int(sec) % 60:02d}'
def cr_by(members):
    o = {}
    for g, gl in (('top', 'top6'), ('rest', 'rest')):
        ms = [s for s in members if s['grp'] == g]
        o[gl] = dict(inside=dict(cruiser_counts(ms, 'inside').most_common()), screened=dict(cruiser_counts(ms, 'screened').most_common()))
    return o
def cr_txt(d, k=3):
    def one(c): return ', '.join(f'{a} {b}' for a, b in list(c.items())[:k]) + (f' +{len(c) - k} more' if len(c) > k else '')
    parts = []
    for gl, lab in (('top6', 'Top 6'), ('rest', 'Rest')):
        i, s = d[gl]['inside'], d[gl]['screened']
        if not i and not s: parts.append(f'{lab}: none'); continue
        parts.append(f'{lab}: ' + '; '.join(x for x in ((f'inside {one(i)}' if i else ''), (f'screened {one(s)}' if s else '')) if x))
    return ' / '.join(parts)
def base_extra(members, t, note, family, sid):
    win = [s['conc'] for s in members if s['win']]; los = [s['conc'] for s in members if not s['win']]
    took = [s['we_took'] for s in members if s['we_took'] is not None]
    e = dict(id=sid, family=family, share_top6=None if t['st'] is None else round(t['st'], 1), share_rest=None if t['sr'] is None else round(t['sr'], 1),
             pool_top6=t['nt'], pool_rest=t['nr'],
             diff_pts=None if t['st'] is None or t['sr'] is None else round(t['st'] - t['sr'], 1),
             diff_ci=None if t['lo'] is None else [round(t['lo'], 1), round(t['hi'], 1)], note=note,
             median_time_s=round(med(s['el'] for s in members)), median_time=clock(med(s['el'] for s in members)),
             cruisers_by_how=cr_by(members), n_cruiser_inside=sum(s['cr_inside'] for s in members), n_cruiser_screened=sum(s['cr_screened'] for s in members),
             n_no_cruiser=sum(not s['cr_any'] for s in members), selfish_flag_pct=round(pct(members, lambda s: s['selfish'])),
             cells=cells_of(members), ships=dict(C(s['ship'] for s in members).most_common()),
             n_win=len(win), n_loss=len(los), damage_win=round(mean(win)) if win else None, damage_loss=round(mean(los)) if los else None,
             win_loss_differs=bool(len(win) >= WL_N and len(los) >= WL_N and abs(mean(win) - mean(los)) > WL_GAP),
             cap_taken_n=len(took), cap_taken_pct=round(100 * sum(took) / len(took)) if len(took) >= MIN_N else None,
             smoker_deaths_per_100=round(rate100(members, 'd_smoker'), 1))
    return e

# ---------- circle spots
RECS = []; ROWS = collections.defaultdict(list); DRAW = collections.defaultdict(list); NONE = collections.defaultdict(list)
for m in MAPORDER:
    ms = [s for s in S if s['map'] == m]
    for fam, tag, jkind, test, plain in FAMILIES:
        pool = [s for s in ms if test(s)]
        spots = sorted(find_spots(pool), key=lambda x: -len(x[3]))
        P(f'{m} | {fam}: pool {len(pool)} (Top 6 {sum(s["grp"] == "top" for s in pool)}, Rest {sum(s["grp"] == "rest" for s in pool)}), spots {len(spots)}')
        if not spots:
            NONE[m].append(f'no {plain} spot (no compact place holds {max(MIN_N, math.ceil(MIN_SHARE * len(pool)))} of the {len(pool)} such smokes on this map)')
        for i, (cx, cz, r, mem) in enumerate(spots, 1):
            t = share_test(pool, mem); mode, note = label(t, mem)
            sid = f'{AB[m]}-{tag}-{i}'
            u, v = uv(m, cx, cz)
            e = base_extra(mem, t, note, fam, sid)
            e['radius_km'] = round(r / KM, 2); e['where'] = where(m, cx, cz)
            if fam == 'early_cruiser':
                e['n_inside'] = sum(s['early_mode'] == 'inside' for s in mem); e['n_screened'] = sum(s['early_mode'] == 'screened' for s in mem)
                e['inside_top6'] = sum(s['early_mode'] == 'inside' and s['grp'] == 'top' for s in mem); e['inside_rest'] = e['n_inside'] - e['inside_top6']
                e['screened_top6'] = sum(s['early_mode'] == 'screened' and s['grp'] == 'top' for s in mem); e['screened_rest'] = e['n_screened'] - e['screened_top6']
            kind = jkind or ('top6_spot' if mode == 'top6' else 'shared_spot')
            rec = spot_record(m, kind, mode, f"{m}: {plain} spot, {e['where']} ({'/'.join(e['cells'])})", S, mem,
                              dict(type='circle', u=round(u, 4), v=round(v, 4), r=round(uv_len(m, r * WU), 4)), e)
            RECS.append(rec); ROWS[m].append(rec); DRAW[(m, fam)].append((cx, cz, r, mem, rec))
            P(f"  {sid} {e['where']} {e['cells']} r {e['radius_km']} km n {len(mem)} top/rest {rec['n_top6']}/{rec['n_rest']} share {t['st']} vs {t['sr']} ci {t['lo']} {t['hi']} -> {mode} {note}")
            P('     ', clan_counts(mem), '| dmg', rec['concealed_damage_per_smoke'], 'deaths/100', rec['deaths_per_100'], 'time', e['median_time'])

# ---------- high-paying cells (destroyer smokes)
def cell_test(dd, members, reps=REPS, rng=RNG, conc=None):
    """Mean concealed damage in the cell minus the mean over the rest of the map, with a clan-resampled 95% interval."""
    ids = {id(s) for s in members}; g = (lambda s: s['conc']) if conc is None else (lambda s: conc[id(s)])
    cl = by(dd, 'team'); pc = []
    for c, v in cl.items():
        a = [g(s) for s in v if id(s) in ids]; b = [g(s) for s in v if id(s) not in ids]
        pc.append((sum(a), len(a), sum(b), len(b)))
    tot = [sum(x[i] for x in pc) for i in range(4)]
    diff = tot[0] / tot[1] - tot[2] / tot[3]
    o = []
    for _ in range(reps):
        r = rng.choices(pc, k=len(pc)); a, na, b, nb = (sum(x[i] for x in r) for i in range(4))
        if na and nb: o.append(a / na - b / nb)
    o.sort()
    return diff, o[int(.025 * len(o))], o[max(0, int(.975 * len(o)) - 1)], tot[0] / tot[1], tot[2] / tot[3]
def cell_candidates(dd):
    bc = by(dd, 'ncell'); out = [((c,), v) for c, v in sorted(bc.items()) if len(v) >= MIN_N]
    for (c, r), v in sorted(bc.items()):
        for c2, r2 in ((c + 1, r), (c, r + 1)):
            w = bc.get((c2, r2))
            if w and len(v) >= 3 and len(w) >= 3 and len(v) + len(w) >= MIN_N: out.append((((c, r), (c2, r2)), v + w))
    return out
def high_cells(dd, reps=REPS, rng=RNG, conc=None):
    """Single cells first; a pair of adjacent cells is added only when neither of its cells passed alone and it does not
    overlap a pair already taken (best lower bound first). Returns (tested, [(cells, members, diff, lo, hi, mean, rest)])."""
    cand = cell_candidates(dd); res = []
    for cells, mem in cand:
        d, lo, hi, mu, rest = cell_test(dd, mem, reps, rng, conc)
        if lo > 0: res.append((cells, mem, d, lo, hi, mu, rest))
    singles = [x for x in res if len(x[0]) == 1]; used = {x[0][0] for x in singles}; out = list(singles)
    for x in sorted([x for x in res if len(x[0]) == 2], key=lambda x: -x[3]):
        if not (set(x[0]) & used): out.append(x); used |= set(x[0])
    return len(cand), out
CELLTESTS = 0; CELLDRAW = collections.defaultdict(list)
for m in MAPORDER:
    dd = [s for s in S if s['map'] == m and s['cls'] == 'destroyer']
    ntest, hc = high_cells(dd); CELLTESTS += ntest
    P(f'{m} | high cells: destroyer smokes {len(dd)}, map mean {mean(s["conc"] for s in dd):,.0f}, cells or pairs tested {ntest}, passed {len(hc)}')
    if not hc: NONE[m].append(f'no high-paying cell (of {ntest} cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map)')
    for i, (cells, mem, d, lo, hi, mu, rest) in enumerate(sorted(hc, key=lambda x: -x[5]), 1):
        t = share_test(dd, mem); mode, note = label(t, mem)
        sid = f'{AB[m]}-cell-{i}'; names = [cell_name(*c) for c in cells]
        cc = [cell_centre(m, *c) for c in cells]; cx, cz = mean(x for x, _ in cc), mean(z for _, z in cc); u, v = uv(m, cx, cz)
        e = base_extra(mem, t, note, 'high_cell', sid); e['cells'] = names; e['where'] = where(m, cx, cz)
        e.update(cell_mean=round(mu), rest_of_map_mean=round(rest), damage_gap=round(d), damage_gap_ci=[round(lo), round(hi)], median_damage=round(med(s['conc'] for s in mem)),
                 n_clans=len({s['team'] for s in mem}), n_games=len({s['game'] for s in mem}))
        rec = spot_record(m, 'high_cell', mode, f"{m}: high-paying cell {'+'.join(names)}, {e['where']}", S, mem, dict(type='cells', cells=names, u=round(u, 4), v=round(v, 4)), e)
        RECS.append(rec); ROWS[m].append(rec); CELLDRAW[m].append((cells, mem, rec))
        P(f"  {sid} {names} n {len(mem)} mean {mu:,.0f} vs rest {rest:,.0f} gap {d:,.0f} ({lo:,.0f} to {hi:,.0f}) median {e['median_damage']:,} win {e['damage_win']} (n {e['n_win']}) loss {e['damage_loss']} (n {e['n_loss']}) "
          f"cap taken {e['cap_taken_pct']} of {e['cap_taken_n']} | share {t['st']:.1f} vs {t['sr']:.1f} ci {t['lo']:.1f} {t['hi']:.1f} -> {mode} {note}")
        P('     ', clan_counts(mem))

# ---------- placebo for the "Top 6 spot" label: six busy Rest clans stand in as the top group, real Top 6 left out
PL_DRAWS = 200
rest_s = [s for s in S if s['grp'] == 'rest']
busy = [k for k, _ in C(s['team'] for s in rest_s).most_common(12)]
pl_spots = []  # (pool, members)
for m in MAPORDER:
    ms = [s for s in rest_s if s['map'] == m]
    for fam, tag, jkind, test, plain in FAMILIES:
        pool = [s for s in ms if test(s)]
        for cx, cz, r, mem in find_spots(pool): pl_spots.append((pool, mem))
    dd = [s for s in ms if s['cls'] == 'destroyer']
    for cells, mem, *_ in high_cells(dd, reps=500)[1]: pl_spots.append((dd, mem))
pl_counts = []
for _ in range(PL_DRAWS):
    fake = set(RNG.sample(busy, 6)); n = 0
    for pool, mem in pl_spots:
        t = share_test(pool, mem, topset=fake, reps=400)
        n += label(t, mem, fake)[0] == 'top6'
    pl_counts.append(n)
n_real_top = sum(r['mode'] == 'top6' for r in RECS)
PLACEBO = dict(draws=PL_DRAWS, spots=len(pl_spots), mean=mean(pl_counts), lo=min(pl_counts), hi=max(pl_counts), p50=med(pl_counts),
               share_ge_real=100 * sum(c >= n_real_top for c in pl_counts) / PL_DRAWS, rate=100 * mean(pl_counts) / len(pl_spots))
P('PLACEBO top label:', PLACEBO, '| real: top', n_real_top, 'of', len(RECS), f'({100 * n_real_top / len(RECS):.0f}%)')

# ---------- shuffle check for high cells: concealed damage shuffled among a map's destroyer smokes
SH = 20; sh_counts = []
for k in range(SH):
    n = 0
    for m in MAPORDER:
        dd = [s for s in S if s['map'] == m and s['cls'] == 'destroyer']
        vals = [s['conc'] for s in dd]; RNG.shuffle(vals); conc = {id(s): v for s, v in zip(dd, vals)}
        n += len(high_cells(dd, reps=400, conc=conc)[1])
    sh_counts.append(n)
n_cells = sum(r['kind'] == 'high_cell' for r in RECS)
SHUF = dict(runs=SH, mean=mean(sh_counts), lo=min(sh_counts), hi=max(sh_counts), tested=CELLTESTS, real=n_cells)
P('SHUFFLE high cells:', SHUF)

# ---------- totals check
dd_all = [s for s in S if s['cls'] == 'destroyer']
P('CHECK smokes', len(S), 'destroyer top/rest', sum(s['grp'] == 'top' for s in dd_all), sum(s['grp'] == 'rest' for s in dd_all), '| records', len(RECS), '| ids unique', len({r['id'] for r in RECS}) == len(RECS))

json.dump(RECS, open(os.path.join(OUT, 'spots.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump(dict(placebo=PLACEBO, shuffle=SHUF), open(os.path.join(OUT, 'checks.json'), 'w', encoding='utf-8'), indent=1)

# ---------- markdown
KLAB = {'long_smoke': 'long-smoke', 'cap_sitter': 'selfish: cap sitter', 'parked_cruiser': 'selfish: parked cruiser', 'early_cruiser': 'early cruiser', 'high_cell': 'high-paying cell'}
def k1(x): return '-' if x is None else f'{x / 1000:.1f}k'
def clans_txt(c):
    f = lambda d: ', '.join(f'{k} {v}' for k, v in d.items()) or 'none'
    return f"Top 6: {f(c['top6'])} / Rest: {f(c['rest'])}"
def mode_txt(r):
    lab = 'Top 6 spot' if r['mode'] == 'top6' else 'Shared'
    if r['share_top6'] is None or r['share_rest'] is None: return f"{lab} ({r['note']})"
    s = f"{lab}: {r['share_top6']:.0f}% vs {r['share_rest']:.0f}%"
    if r['diff_ci']: s += f" (gap {r['diff_pts']:+.0f}, {r['diff_ci'][0]:+.0f} to {r['diff_ci'][1]:+.0f})"
    return s + (f"; {r['note']}" if r['note'] else '')
def note_txt(r):
    n = []
    if r['small_n']: n.append('small n')
    if r['family'] == 'early_cruiser':
        n.append(f"inside {r['n_inside']} (Top 6 {r['inside_top6']}, Rest {r['inside_rest']}), screened {r['n_screened']} (Top 6 {r['screened_top6']}, Rest {r['screened_rest']})")
    if r['family'] == 'high_cell':
        n.append(f"{k1(r['cell_mean'])} vs {k1(r['rest_of_map_mean'])} elsewhere on the map (gap {r['damage_gap_ci'][0] / 1000:+.1f}k to {r['damage_gap_ci'][1] / 1000:+.1f}k); median {k1(r['median_damage'])}; {r['n_clans']} clans, {r['n_games']} games")
        n.append(f"cap taken {r['cap_taken_pct']}% of {r['cap_taken_n']}" if r['cap_taken_pct'] is not None else f"cap taken: too few ({r['cap_taken_n']} smokes where the cap was not already ours)")
    if r['win_loss_differs']: n.append(f"wins {k1(r['damage_win'])} (n {r['n_win']}) vs losses {k1(r['damage_loss'])} (n {r['n_loss']})")
    elif r['family'] == 'high_cell':
        n.append(f"win/loss: {k1(r['damage_win'])} (n {r['n_win']}) vs {k1(r['damage_loss'])} (n {r['n_loss']})" + ('; too few on one side to compare' if min(r['n_win'], r['n_loss']) < WL_N else '; not far apart'))
    if r['family'] in ('long_smoke', 'cap_sitter', 'parked_cruiser'): n.append('ships: ' + ', '.join(f'{k} {v}' for k, v in r['ships'].items()))
    return '; '.join(n)
ORDER = ['long_smoke', 'cap_sitter', 'parked_cruiser', 'early_cruiser', 'high_cell']
gen = []
cnt_rows = []
for m in MAPORDER:
    rs = sorted(ROWS[m], key=lambda r: (ORDER.index(r['family']), -r['n']))
    row = [m]
    for f in ORDER:
        fr = [r for r in rs if r['family'] == f]; nt = sum(r['mode'] == 'top6' for r in fr)
        row.append(f"{len(fr)}" + (f" ({nt} Top 6)" if nt else '') if fr else '0')
    row.append(f"{len(rs)} ({sum(r['mode'] == 'top6' for r in rs)} Top 6)"); cnt_rows.append(row)
    gen.append(f"\n#### {m}\n")
    gen.append(f"Figure: `figures/c4-{AB[m]}.png`. " + ('Not found here: ' + '; '.join(NONE[m]) + '.' if NONE[m] else ''))
    gen.append('')
    if not rs: gen.append('No spot of any kind on this map.'); continue
    gen.append(md_table(['id', 'kind', 'where (cells)', 'mode: share of Top 6 vs Rest smokes of this kind', 'n Top 6 / Rest', 'clans', 'cruisers inside / screened', 'damage per smoke', 'deaths per 100', 'median time', 'note'],
        [[r['id'], KLAB[r['family']], f"{r['where']} ({'/'.join(r['cells'])})", mode_txt(r), f"{r['n_top6']} / {r['n_rest']}", clans_txt(r['clans']), cr_txt(r['cruisers_by_how']),
          k1(r['concealed_damage_per_smoke']), f"{r['deaths_per_100']:.0f}", r['median_time'], note_txt(r)] for r in rs]))
    gen.append('')
    gen.append('Examples: ' + '; '.join(f"{r['id']}: " + ', '.join(f"[{i + 1}]({l})" for i, l in enumerate(r['examples'])) for r in rs))
tot = ['All maps'] + [f"{sum(r['family'] == f for r in RECS)}" + (f" ({sum(r['family'] == f and r['mode'] == 'top6' for r in RECS)} Top 6)" if any(r['family'] == f and r['mode'] == 'top6' for r in RECS) else '') for f in ORDER] + [f"{len(RECS)} ({n_real_top} Top 6)"]
count_table = md_table(['Map', 'long-smoke', 'cap sitter', 'parked cruiser', 'early cruiser', 'high-paying cell', 'all'], cnt_rows + [tot])
open(os.path.join(OUT, 'generated.md'), 'w', encoding='utf-8').write(count_table + '\n' + '\n'.join(gen) + '\n')
head = os.path.join(OUT, 'head.md')
if os.path.exists(head):
    txt = open(head, encoding='utf-8').read().replace('{{COUNTS}}', count_table).replace('{{MAPS}}', '\n'.join(gen))
    open(os.path.join(OUT, 'FINDINGS-C4.md'), 'w', encoding='utf-8').write(txt)
open(os.path.join(OUT, 'out.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')

# ---------- figures: one per map, four panels
if '--nofig' not in sys.argv:
    DARK = '#2b2b2b'
    for m in MAPORDER:
        ms = [s for s in S if s['map'] == m]
        fig = Fig(1000, 1110, f'C4 working map: {m}', 'Team-normalized. Dots: Top 6 blue, Rest orange. Spot outline: blue = Top 6 spot, dark = Shared spot.')
        titles = ['Long-smoke spots (Somers, Gearing, Harugumo, Delny)', 'Selfish spots: cap sitters (dots, solid ring), Svea/Jinan (squares, dashed ring)',
                  'Early cruiser smoke spots (filled = cruiser inside, hollow = screened)', 'High-paying cells (all destroyer smokes shown)']
        for i in range(4):
            p = Panel(m, 50 + (i % 2) * 480, 120 + (i // 2) * 495, 430, G, title=titles[i], dim=0.45)
            fams = [['long_smoke'], ['cap_sitter', 'parked_cruiser'], ['early_cruiser'], []][i]
            if i == 3:
                for s in ms:
                    if s['cls'] == 'destroyer': p.dot(s['nx'], s['nz'], r=2.4, fill=GROUP_COLOR[s['grp']], opacity=0.5)
                for cells, mem, rec in CELLDRAW[m]:
                    c0 = min(c for c, _ in cells); r0 = min(r for _, r in cells); c1 = max(c for c, _ in cells); r1 = max(r for _, r in cells); sz = 43.0
                    col = BLUE if rec['mode'] == 'top6' else DARK
                    p.raw(f'<rect x="{p.x0 + c0 * sz:.1f}" y="{p.y0 + r0 * sz:.1f}" width="{(c1 - c0 + 1) * sz:.1f}" height="{(r1 - r0 + 1) * sz:.1f}" fill="none" stroke="{col}" stroke-width="2.6"/>')
                    p.raw(T(min(max(p.x0 + (c0 + c1 + 1) / 2 * sz, p.x0 + 34), p.x0 + p.size - 34), p.y0 + r0 * sz - 4 if r0 > 0 else p.y0 + (r1 + 1) * sz + 12, rec['id'], size=10.5, fill=col, weight='700', halo=True))
            for f in fams:
                test = next(x[3] for x in FAMILIES if x[0] == f)
                for s in ms:
                    if not test(s): continue
                    col = GROUP_COLOR[s['grp']]
                    if f == 'parked_cruiser':
                        px, py = p.xy(s['nx'], s['nz']); p.raw(f'<rect x="{px - 2.6:.1f}" y="{py - 2.6:.1f}" width="5.2" height="5.2" fill="{col}" opacity="0.6"/>')
                    elif f == 'early_cruiser' and s['early_mode'] == 'screened':
                        px, py = p.xy(s['nx'], s['nz']); p.raw(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="{BG}" fill-opacity="0.6" stroke="{col}" stroke-width="1.6"/>')
                    else: p.dot(s['nx'], s['nz'], r=3.1, fill=col, opacity=0.6)
                for cx, cz, r, mem, rec in DRAW[(m, f)]:
                    col = BLUE if rec['mode'] == 'top6' else DARK
                    p.ring(cx, cz, p.px(r * WU), stroke=col, width=2.6, dash='6 4' if f == 'parked_cruiser' else None)
                    px, py = p.xy(cx, cz); rr = p.px(r * WU)
                    p.raw(T(min(max(px, p.x0 + 36), p.x0 + p.size - 36), py - rr - 4 if py - rr - 4 > p.y0 + 12 else py + rr + 12, rec['id'], size=10.5, fill=col, weight='700', halo=True))
            fig.add(p)
        fig.legend(50, 76, [('Top 6 smoke', BLUE), ('Rest smoke', ORANGE)])
        fig.save(os.path.join(FIGS, f'c4-{AB[m]}'))
    P('figures ok')
