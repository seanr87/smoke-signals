# Round 5b, worker n2: C3 danger zones with real health, keyed two ways, plus death-position maps.
# Run: python -I -X utf8 n2_danger.py      Writes out-danger.json, out-danger.md, danger-zones.json and figures n2-danger-<map>, n2-deaths-<map>.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n2lib import *
import random as _r
random.seed(53)
QUICK = '--quick' in sys.argv
REPS, PL_RUNS, PL_REPS = (400, 10, 100) if QUICK else (2000, 120, 300)
PR = build_pairs(); add_radar_flags()
L = []
def P(*a):
    t = ' '.join(str(x) for x in a); L.append(t); print(t)
J = {}
CLANS = sorted({s['team'] for s in S})
KINDS = ('dd', 'cr')
KLAB = {'dd': 'destroyer smoker', 'cr': 'sheltering cruisers'}
CORE = [p for p in PR if p['ok'] and p['how'] in ('smoker', 'inside', 'behind')]
for p in CORE:
    p['hurt_w'] = p['died_win'] or p['net'] >= HURT_SHARE
    ref = p['death_pos'] if p['died_win'] else p['drop_pos'] if p['hurt_w'] and p['drop_pos'] else p['pmid'] or p['p0']
    p['ref'] = npt(p['s'], ref); p['np0'] = npt(p['s'], p['p0'])
DDP = [p for p in CORE if p['how'] == 'smoker' and p['s']['cls'] == 'destroyer']
CRP = [p for p in CORE if p['cls'] == 'cruiser' and p['how'] in ('inside', 'behind')]
CAPS = {m: map_caps(G, m) for m in MAPL}
def cap_at(m, pt):
    for c in CAPS[m]:
        if math.hypot(c['x'] - pt[0], c['z'] - pt[1]) <= c['r']: return c['cap']
    return None

# ---- units. Version 1: one unit per smoke, placed at the smoke centre. Version 2: one unit per ship at risk, placed where it was hit.
def units_v1(new=True):
    U = []
    bys = collections.defaultdict(list)
    for p in DDP: bys[('dd', id(p['s']))].append(p)
    for p in CRP: bys[('cr', id(p['s']))].append(p)
    for (k, _), ps in bys.items():
        s = ps[0]['s']
        if new: val = (sum(p['died_win'] for p in ps), sum(p['hurt_w'] for p in ps), len(ps))
        else: val = (sum(p['died'] for p in ps), sum(p['x']['hurt'] for p in ps), len(ps))   # round 5 outcomes on the same units
        U.append(dict(kind=k, map=s['map'], team=s['team'], grp=s['grp'], cell=s['ncell'], cap=s['near_ncap'] if s['near_cap_edge_m'] <= 0 else None, val=val, s=s, ps=ps))
    return U
def units_v2(key='ref'):
    U = []
    for k, ps in (('dd', DDP), ('cr', CRP)):
        for p in ps:
            s = p['s']; pt = p[key]
            if pt is None: continue
            U.append(dict(kind=k, map=s['map'], team=s['team'], grp=s['grp'], cell=cell(s['map'], pt[0], pt[1]), cap=cap_at(s['map'], pt), val=(int(p['died_win']), int(p['hurt_w']), 1), s=s, ps=[p], pt=pt))
    return U

def build_areas(U):
    out = []
    for k in KINDS:
        for m in MAPL:
            uu = [u for u in U if u['kind'] == k and u['map'] == m]
            cells = by(uu, 'cell'); small_blocks = collections.defaultdict(list)
            for c, v in cells.items():
                if len(v) >= MIN_N: out.append(dict(kind=k, map=m, type='cell', cells=[c], members=v))
                else: small_blocks[(c[0] // 2, c[1] // 2)].append(c)
            for b, cs in small_blocks.items():
                v = [u for c in cs for u in cells[c]]
                out.append(dict(kind=k, map=m, type='cells' if len(cs) > 1 else 'cell', cells=sorted(cs), members=v))
            for cap, v in by([u for u in uu if u['cap']], 'cap').items():
                out.append(dict(kind=k, map=m, type='cap', cap=cap, cells=[], members=v))
    for a in out:
        a['name'] = (f'inside cap {a["cap"]}' if a['type'] == 'cap' else '+'.join(cell_name(*c) for c in a['cells'])); a['n'] = len(a['members'])
    return out

def evaluate(U, TEST, vals, reps, rng):
    """vals: one (died, hurt, at risk) per unit, same order as U. Per tested area: rates, both baselines, and the 95% interval of
    (area rate - baseline) with whole clans resampled. Flag = died-or-hurt interval above zero against BOTH baselines."""
    for u, v in zip(U, vals): u['_v'] = v
    tot = {k: {c: [0, 0, 0] for c in CLANS} for k in KINDS}; mp = {(k, m): {c: [0, 0, 0] for c in CLANS} for k in KINDS for m in MAPL}
    for u in U:
        for t in (tot[u['kind']][u['team']], mp[(u['kind'], u['map'])][u['team']]):
            for i in range(3): t[i] += u['_v'][i]
    ar = []
    for a in TEST:
        d = {}
        for u in a['members']:
            t = d.setdefault(u['team'], [0, 0, 0])
            for i in range(3): t[i] += u['_v'][i]
        ar.append(d)
    rate = lambda t, i: 100 * t[i] / t[2] if t[2] else None
    res = []
    for a, d in zip(TEST, ar):
        k = a['kind']; A = [sum(x[i] for x in d.values()) for i in range(3)]
        T_ = [sum(x[i] for x in tot[k].values()) for i in range(3)]; M_ = [sum(x[i] for x in mp[(k, a['map'])].values()) for i in range(3)]
        res.append(dict(died=rate(A, 0), hurt=rate(A, 1), den=A[2], n_died=A[0], n_hurt=A[1], base_all=(rate(T_, 0), rate(T_, 1)), base_map=(rate(M_, 0), rate(M_, 1)), d=[[], [], [], []]))
    for _ in range(reps):
        w = C(rng.choices(CLANS, k=len(CLANS)))
        T2 = {k: [sum(w[c] * tot[k][c][i] for c in w) for i in range(3)] for k in KINDS}
        M2 = {km: [sum(w[c] * v[c][i] for c in w) for i in range(3)] for km, v in mp.items()}
        for a, d, r in zip(TEST, ar, res):
            A = [0, 0, 0]
            for c, x in d.items():
                n = w.get(c)
                if n: A[0] += n * x[0]; A[1] += n * x[1]; A[2] += n * x[2]
            if not A[2]: continue
            k = a['kind']; t = T2[k]; mm = M2[(k, a['map'])]
            if not t[2] or not mm[2]: continue
            for i in (0, 1):
                ra = 100 * A[i] / A[2]
                r['d'][i].append(ra - 100 * t[i] / t[2]); r['d'][2 + i].append(ra - 100 * mm[i] / mm[2])
    for r in res:
        cis = []
        for v in r['d']:
            v.sort(); cis.append((v[int(.025 * len(v))], v[max(0, int(.975 * len(v)) - 1)]) if len(v) >= 20 else (None, None))
        r['ci_died_all'], r['ci_hurt_all'], r['ci_died_map'], r['ci_hurt_map'] = cis; del r['d']
        ok = lambda c: c[0] is not None and c[0] > 0
        r['flag'] = ok(r['ci_hurt_all']) and ok(r['ci_hurt_map'])
        r['flag_died'] = ok(r['ci_died_all']) and ok(r['ci_died_map'])
        r['above_all_only'] = ok(r['ci_hurt_all']) and not ok(r['ci_hurt_map'])
    return res

def placebo(U, TEST, n_real, seed):
    rng = _r.Random(seed); pl = []; pl_died = []; bymap = C()
    groups = collections.defaultdict(list)
    for i, u in enumerate(U): groups[(u['kind'], u['map'])].append(i)
    real = [u['val'] for u in U]
    for run in range(PL_RUNS):
        vals = list(real)
        for idx in groups.values():
            o = [real[i] for i in idx]; rng.shuffle(o)
            for i, v in zip(idx, o): vals[i] = v
        r = evaluate(U, TEST, vals, PL_REPS, rng)
        pl.append(sum(x['flag'] for x in r)); pl_died.append(sum(x['flag_died'] for x in r))
        for a, x in zip(TEST, r):
            if x['flag']: bymap[a['map']] += 1
    small = evaluate(U, TEST, real, PL_REPS, _r.Random(seed + 1))
    return dict(runs=PL_RUNS, reps=PL_REPS, mean=round(mean(pl), 2), median=med(pl), p95=q(pl, .95), max=max(pl), none=sum(x == 0 for x in pl), at_least_real=sum(x >= n_real for x in pl),
                real_same_reps=sum(x['flag'] for x in small), died_mean=round(mean(pl_died), 2), by_map={m: round(bymap[m] / PL_RUNS, 2) for m in MAPL})

def fmt_ci(c): return '-' if c[0] is None else f'{c[0]:+.0f} to {c[1]:+.0f}' + (' *' if c[0] * c[1] > 0 else '')
def describe(a, U):
    mem = a['members']; k = a['kind']; pool = [u for u in U if u['kind'] == k and u['map'] == a['map']]
    ids = {id(u) for u in mem}
    stat = lambda uu: 100 * sum(id(u) in ids for u in uu) / len(uu) if uu else None
    top = [u for u in pool if u['grp'] == 'top']; rest = [u for u in pool if u['grp'] == 'rest']
    d = grp_ci(pool, stat, key=lambda u: u['team'], rng=_r.Random(7)); a['share_top'], a['share_rest'], a['share_gap_ci'] = stat(top), stat(rest), d
    a['mode'] = 'top6' if d[0] is not None and d[0] > 0 else 'shared'
    a['rest_habit'] = bool(d[0] is not None and d[1] < 0)
    sm_ = [u['s'] for u in mem]; ps_ = [u['s'] for u in pool]
    a['behind_pct'] = pct(sm_, lambda s: s['state'] == 'behind 50+'); a['radar_pct'] = pct(sm_, lambda s: s['rad_any']); a['radar_old_pct'] = pct(sm_, lambda s: s['radar_on_us'] > 0)
    a['behind_map_pct'] = pct(ps_, lambda s: s['state'] == 'behind 50+'); a['radar_map_pct'] = pct(ps_, lambda s: s['rad_any'])
    a['n_clans'] = len({u['team'] for u in mem}); a['n_games'] = len({u['s']['game'] for u in mem})
    worst = C()
    for u in mem: worst[u['team']] += u['val'][1]
    wc = worst.most_common(1)[0][0] if worst else None
    m2 = [u for u in mem if u['team'] != wc]; t = [sum(u['val'][i] for u in m2) for i in range(3)]
    a['without_top_clan'] = dict(clan=wc, n=len(m2), hurt_per_100=round(100 * t[1] / t[2], 1) if t[2] else None)
    a['clans_text'] = clan_counts(sm_)
HDR = ['map', 'who', 'area', 'n', 'ships at risk', 'died or hurt per 100', 'baseline all / same map', 'gap vs all maps (interval)', 'gap vs same map (interval)', 'died per 100 (n; baseline all / map)', 'death gap vs all maps', 'mark']
def arow(a, unit):
    return [a['map'], KLAB[a['kind']], a['name'], f'{a["n"]}{small(a["n"])}', a['den'], f'{a["hurt"]:.0f} ({a["n_hurt"]} of {a["den"]})', f'{a["base_all"][1]:.1f} / {a["base_map"][1]:.1f}',
            f'{a["hurt"]-a["base_all"][1]:+.0f} ({fmt_ci(a["ci_hurt_all"])})', f'{a["hurt"]-a["base_map"][1]:+.0f} ({fmt_ci(a["ci_hurt_map"])})',
            f'{a["died"]:.0f} ({a["n_died"]}; {a["base_all"][0]:.1f} / {a["base_map"][0]:.1f})', f'{a["died"]-a["base_all"][0]:+.0f} ({fmt_ci(a["ci_died_all"])})',
            'FLAG' if a['flag'] else 'above all-map only' if a['above_all_only'] else 'deaths only' if a['flag_died'] else '']
def akey(a): return (a['kind'], a['map'], a['name'])

def run(tag, title, U, unit_word, seed):
    AREAS = build_areas(U); TEST = [a for a in AREAS if a['n'] >= MIN_N]
    res = evaluate(U, TEST, [u['val'] for u in U], REPS, _r.Random(seed))
    for a, r in zip(TEST, res): a.update(r)
    FL = [a for a in TEST if a['flag']]
    P(f'\n# {title}\n')
    rows = []; base = {}
    for k in KINDS:
        uu = [u for u in U if u['kind'] == k]; t = [sum(u['val'][i] for u in uu) for i in range(3)]
        base[k] = dict(units=len(uu), at_risk=t[2], died=r1(100 * t[0] / t[2]), hurt=r1(100 * t[1] / t[2]), by_map={})
        rows.append([KLAB[k], 'all maps', len(uu), t[2], f'{100*t[0]/t[2]:.1f}', f'{100*t[1]/t[2]:.1f}'])
        for m in MAPL:
            um = [u for u in uu if u['map'] == m]; t = [sum(u['val'][i] for u in um) for i in range(3)]
            base[k]['by_map'][m] = dict(units=len(um), at_risk=t[2], died=r1(100 * t[0] / t[2]), hurt=r1(100 * t[1] / t[2]))
            rows.append([KLAB[k], m, len(um), t[2], f'{100*t[0]/t[2]:.1f}', f'{100*t[1]/t[2]:.1f}'])
    P(md_table(['who', 'map', unit_word, 'ships at risk', 'died per 100', 'died or hurt per 100'], rows))
    P(f'\nAreas built: {len(AREAS)}; with {MIN_N}+ {unit_word} and tested: {len(TEST)} ({sum(a["kind"] == "dd" for a in TEST)} destroyer, {sum(a["kind"] == "cr" for a in TEST)} cruiser); under {MIN_N}, not rated: {len(AREAS)-len(TEST)}.')
    P(f'Flagged: {len(FL)}. Clearly above the all-map baseline only: {sum(a["above_all_only"] for a in TEST)}. Would be flagged on deaths alone: {sum(a["flag_died"] for a in TEST)}.')
    pl = placebo(U, TEST, len(FL), seed + 100)
    P(f'Placebo ({pl["runs"]} runs, outcomes shuffled among the {unit_word} of the same map, same areas, same rule, {pl["reps"]} resamples each): flags by luck per run: mean {pl["mean"]}, median {pl["median"]}, 95th percentile {pl["p95"]:.0f}, max {pl["max"]}; '
      f'runs with no flag {pl["none"]} of {pl["runs"]}; runs with at least as many flags as the real data ({len(FL)}): {pl["at_least_real"]} of {pl["runs"]}. Real data with the same {pl["reps"]} resamples: {pl["real_same_reps"]} flags. Death-only rule by luck: {pl["died_mean"]} per run (real {sum(a["flag_died"] for a in TEST)}).')
    P('Luck flags per map per run: ' + ', '.join(f'{m} {v}' for m, v in pl['by_map'].items()))
    for a in TEST:
        if a['flag'] or a['above_all_only'] or a['flag_died']: describe(a, U)
    per_map = {}
    for m in MAPL:
        tm = [a for a in TEST if a['map'] == m]; fm = [a for a in tm if a['flag']]
        per_map[m] = dict(tested=len(tm), tested_dd=sum(a['kind'] == 'dd' for a in tm), tested_cr=sum(a['kind'] == 'cr' for a in tm), flagged=[a['name'] + ' (' + KLAB[a['kind']] + ')' for a in fm])
        P(f'\n## {m} ({tag})')
        P(f'Areas tested: {per_map[m]["tested_dd"]} destroyer, {per_map[m]["tested_cr"]} cruiser. Flagged: {len(fm)}.' + ('' if fm else ' No area qualifies on this map.'))
        show = sorted([a for a in tm if a['flag'] or a['above_all_only'] or a['flag_died']], key=lambda a: (not a['flag'], a['kind'], -a['hurt']))
        if show: P(md_table(HDR, [arow(a, unit_word) for a in show]))
        for a in show:
            P(f'- {a["name"]} ({KLAB[a["kind"]]}){" FLAGGED" if a["flag"] else " (not flagged)"}: {"Top 6 spot" if a["mode"] == "top6" else "Shared spot"}{" (a Rest habit)" if a["rest_habit"] else ""} '
              f'(share of the map\'s {unit_word} here: Top 6 {a["share_top"]:.0f}%, Rest {a["share_rest"]:.0f}%, gap interval {fmt_ci(a["share_gap_ci"])}). '
              f'Laid while 50+ behind: {a["behind_pct"]:.0f}% (map {a["behind_map_pct"]:.0f}%). A covered ship radar-lit while the smoke stood (radar log): {a["radar_pct"]:.0f}% (map {a["radar_map_pct"]:.0f}%). '
              f'{a["n_clans"]} clans, {a["n_games"]} games. {a["clans_text"]}. Without the clan with most bad outcomes ({a["without_top_clan"]["clan"]}): {a["without_top_clan"]["hurt_per_100"]} per 100 (n {a["without_top_clan"]["n"]}).')
    def slim(a):
        d = {k: a[k] for k in ('kind', 'map', 'name', 'type', 'n', 'den', 'n_died', 'n_hurt', 'flag', 'flag_died', 'above_all_only')}
        d.update(cells=[cell_name(*c) for c in a['cells']], cap=a.get('cap'), died=r1(a['died']), hurt=r1(a['hurt']), base_all=[r1(x) for x in a['base_all']], base_map=[r1(x) for x in a['base_map']],
                 ci_hurt_all=[r1(x) for x in a['ci_hurt_all']], ci_hurt_map=[r1(x) for x in a['ci_hurt_map']], ci_died_all=[r1(x) for x in a['ci_died_all']], ci_died_map=[r1(x) for x in a['ci_died_map']])
        if 'mode' in a:
            d.update(mode=a['mode'], rest_habit=a['rest_habit'], share_top=r1(a['share_top']), share_rest=r1(a['share_rest']), share_gap_ci=[r1(x) for x in a['share_gap_ci']], behind_pct=r1(a['behind_pct']), behind_map_pct=r1(a['behind_map_pct']),
                     radar_pct=r1(a['radar_pct']), radar_map_pct=r1(a['radar_map_pct']), radar_old_pct=r1(a['radar_old_pct']), n_clans=a['n_clans'], n_games=a['n_games'], clans=clan_dict([u['s'] for u in a['members']]), clans_text=a['clans_text'], without_top_clan=a['without_top_clan'])
        return d
    J[tag] = dict(title=title, unit=unit_word, baselines=base, areas_built=len(AREAS), tested=len(TEST), tested_dd=sum(a['kind'] == 'dd' for a in TEST), tested_cr=sum(a['kind'] == 'cr' for a in TEST),
                  n_flag=len(FL), n_above_all_only=sum(a['above_all_only'] for a in TEST), n_flag_died=sum(a['flag_died'] for a in TEST), placebo=pl, per_map=per_map,
                  shown=[slim(a) for a in TEST if a['flag'] or a['above_all_only'] or a['flag_died']])
    return AREAS, TEST, FL, pl

P('C3 danger zones, round 5b. Health is real (ship tracks, every 2 s). Died = the track shows the ship dead between activation and 20 s after dispersal. '
  'Hurt = died, or its health at dispersal was lower than at activation by a third of full health or more (net loss; heals inside the window count back).')
U1 = units_v1(); A1, T1, F1, PL1 = run('v1', 'Version 1: areas keyed on the smoke centre (round 5 areas), real health', U1, 'smokes', 101)
U2 = units_v2(); A2, T2, F2, PL2 = run('v2', 'Version 2: areas keyed on where the damage happened', U2, 'ships', 151)
P('\nVersion 2 unit and denominator: one entry per ship at risk (the smoking destroyer; each cruiser inside or behind a smoke). Each ship is placed once: at its death position if it died, '
  'at its position at its largest 2 s health fall if it was hurt and lived, otherwise at its position half way through the smoke. An area\'s rate = ships placed there that died or were hurt / all ships placed there. '
  'All positions are in the smoking team\'s frame.')

# ---- round 5 flags: where are they now
P('\n# Round 5 flags, old outcomes and new outcomes on the same areas (version 1)')
U0 = units_v1(new=False); A0 = build_areas(U0); T0 = [a for a in A0 if a['n'] >= MIN_N]
res0 = evaluate(U0, T0, [u['val'] for u in U0], REPS, _r.Random(101))
for a, r in zip(T0, res0): a.update(r)
F0 = [a for a in T0 if a['flag']]
R5FLAGS = [('dd', 'Hotspot', 'inside cap C'), ('dd', 'Sea of Fortune', 'E5+F5+E6'), ('dd', 'Sleeping Giant', 'E7+F7+F8'), ('cr', 'Mountain Range', 'E7+F7+F8')]
P(f'Round 5 outcomes (batch deaths, estimated health) recomputed here on the round 5b units: {len(T0)} areas tested, {len(F0)} flagged: ' + '; '.join(f'{a["map"]} {a["name"]} ({KLAB[a["kind"]]})' for a in F0) + '. Round 5 printed 109 tested and 4 flagged.')
new1 = {akey(a): a for a in T1}; old1 = {akey(a): a for a in T0}; rows = []; J['r5_flags'] = []
for key in R5FLAGS:
    o, n = old1.get(key), new1.get(key)
    if not o or not n:
        a_ = next((a for a in A0 if akey(a) == key), None); n_ = a_['n'] if a_ else 0
        J['r5_flags'].append(dict(map=key[1], who=KLAB[key[0]], area=key[2], n=n_, survives=False, too_few=True))
        rows.append([key[1], KLAB[key[0]], key[2], f'{n_} (too few)', '-', '-', '-', 'not rated: under 8 smokes once the ship with incomplete health (single-replay game) is left out']); continue
    surv = n['flag']
    J['r5_flags'].append(dict(map=key[1], who=KLAB[key[0]], area=key[2], n=n['n'], old_hurt=r1(o['hurt']), old_n_hurt=o['n_hurt'], old_flag=o['flag'], new_hurt=r1(n['hurt']), new_n_hurt=n['n_hurt'], new_den=n['den'], new_died=r1(n['died']), new_n_died=n['n_died'],
                              new_gap_all=r1(n['hurt'] - n['base_all'][1]), new_ci_all=[r1(x) for x in n['ci_hurt_all']], new_gap_map=r1(n['hurt'] - n['base_map'][1]), new_ci_map=[r1(x) for x in n['ci_hurt_map']], survives=surv,
                              new_base_all=r1(n['base_all'][1]), new_base_map=r1(n['base_map'][1])))
    rows.append([key[1], KLAB[key[0]], key[2], f'{n["n"]}{small(n["n"])}', f'{o["hurt"]:.0f} ({o["n_hurt"]} of {o["den"]}){" FLAG" if o["flag"] else ""}', f'{n["hurt"]:.0f} ({n["n_hurt"]} of {n["den"]})',
                 f'{n["hurt"]-n["base_all"][1]:+.0f} ({fmt_ci(n["ci_hurt_all"])}) / {n["hurt"]-n["base_map"][1]:+.0f} ({fmt_ci(n["ci_hurt_map"])})', 'survives' if surv else 'does not survive'])
P(md_table(['map', 'who', 'area', 'smokes', 'round 5 outcomes: died or hurt per 100', 'real health: died or hurt per 100', 'gap vs all maps / same map (intervals)', 'result'], rows))
J['r5_recomputed'] = dict(tested=len(T0), flagged=[f'{a["map"]} {a["name"]} ({KLAB[a["kind"]]})' for a in F0])
# version 2 flags: the same area keyed on the ship's position at activation
P('\nVersion 2 flags checked a second way (ships placed where they were at activation instead of where they were hit):')
U2b = units_v2('np0'); rows = []; J['v2_check_p0'] = []
for a in F2:
    cs = set(a['cells'])
    mem = [u for u in U2b if u['kind'] == a['kind'] and u['map'] == a['map'] and ((u['cap'] == a['cap']) if a['type'] == 'cap' else (u['cell'] in cs))]
    t = [sum(u['val'][i] for u in mem) for i in range(3)]
    J['v2_check_p0'].append(dict(map=a['map'], who=KLAB[a['kind']], area=a['name'], n=len(mem), hurt=r1(100 * t[1] / t[2]) if t[2] >= MIN_N else None, n_hurt=t[1]))
    rows.append([a['map'], KLAB[a['kind']], a['name'], f'{a["hurt"]:.0f} ({a["n_hurt"]} of {a["den"]})', (f'{100*t[1]/t[2]:.0f} ({t[1]} of {t[2]})' if t[2] >= MIN_N else f'too few ({t[2]})'), f'{a["base_map"][1]:.1f}'])
if rows: P(md_table(['map', 'who', 'area', 'keyed on where hit: per 100', 'keyed on position at activation: per 100', 'same-map baseline'], rows))

# ---- death positions
P('\n# Death positions (ships at risk that died between activation and 20 s after dispersal)')
DEAD = [p for p in CORE if p['died_win'] and p['death_pos']]
for p in DEAD:
    s = p['s']; p['dd_m'] = smoke_dist_m(s, p['death_pos']) - s['radius_m']; p['in_outline'] = p['dd_m'] <= 0
    p['who'] = 'smoking destroyer' if p['how'] == 'smoker' and p['cls'] == 'destroyer' else 'smoker (other class)' if p['how'] == 'smoker' else 'sheltering cruiser' if p['cls'] == 'cruiser' else 'other sheltering ship'
band = lambda d: 'inside the outline' if d <= 0 else 'within 1 km of the edge' if d <= 1000 else '1-3 km' if d <= 3000 else 'over 3 km'
BANDS = ['inside the outline', 'within 1 km of the edge', '1-3 km', 'over 3 km']
rows = []; J['death_pos'] = dict(pairs=len(DEAD), distinct_ships=len({(p['s']['game'], p['eid']) for p in DEAD}), who={}, by_map={})
for w in ('smoking destroyer', 'sheltering cruiser', 'smoker (other class)', 'other sheltering ship'):
    v = [p for p in DEAD if p['who'] == w]
    if not v: continue
    c = C(band(p['dd_m']) for p in v); out = [p['dd_m'] for p in v if p['dd_m'] > 0]
    J['death_pos']['who'][w] = dict(n=len(v), bands={b: c[b] for b in BANDS}, inside_pct=r1(100 * c[BANDS[0]] / len(v)), median_outside_m=r1(med(out), 0) if out else None, in_batch_list=sum(p['died'] for p in v),
                                    top6=sum(p['s']['grp'] == 'top' for p in v), rest=sum(p['s']['grp'] == 'rest' for p in v), inside_top6=sum(p['in_outline'] and p['s']['grp'] == 'top' for p in v), inside_rest=sum(p['in_outline'] and p['s']['grp'] == 'rest' for p in v))
    rows.append([w, len(v), sum(p['died'] for p in v)] + [c[b] for b in BANDS] + [f'{100*c[BANDS[0]]/len(v):.0f}%', f'{med(out):,.0f} m' if out else '-'])
P(md_table(['who died', 'deaths (ship-smoke pairs)', 'of which in the batch list'] + BANDS + ['share inside', 'median distance past the edge when outside'], rows))
P(f'{len(DEAD)} ship-smoke pairs, {J["death_pos"]["distinct_ships"]} distinct ships (a ship covered by two standing smokes is listed under both). Distance is from the death position (last position alive, within 2 s) to the edge of the nearest puff of the smoke.')
rows = []
for m in MAPL:
    v = [p for p in DEAD if p['s']['map'] == m]; c = C(band(p['dd_m']) for p in v)
    J['death_pos']['by_map'][m] = dict(n=len(v), inside=c[BANDS[0]], outside=len(v) - c[BANDS[0]])
    rows.append([m, len(v), c[BANDS[0]], len(v) - c[BANDS[0]], f'{100*c[BANDS[0]]/len(v):.0f}%' if v else '-'])
P(md_table(['map', 'deaths', 'inside the outline', 'outside', 'share inside'], rows))

# ---- JSON records
recs = []
def cap_shape(m, cap):
    c = next(c for c in CAPS[m] if c['cap'] == cap); u, v = uv(m, c['x'], c['z'])
    return dict(type='circle', u=round(u, 4), v=round(v, 4), r=round(c['r'] / MAPS[m]['space_size'], 4))
def rec_for(a, version, pl, n_tested, n_flag):
    m = a['map']; mem = a['members']; sm_ = list({id(u['s']): u['s'] for u in mem}.values())
    if a['type'] == 'cap': shape = cap_shape(m, a['cap'])
    else:
        pts = [u.get('pt') or (u['s']['nx'], u['s']['nz']) for u in mem]; u_, v_ = uv(m, mean(p[0] for p in pts), mean(p[1] for p in pts))
        shape = dict(type='cells', cells=[cell_name(*c) for c in a['cells']], u=round(u_, 4), v=round(v_, 4))
    extra = dict(id='dz5b-' + version + '-' + m.lower().replace(' ', '-') + '-' + a['kind'] + '-' + a['name'].lower().replace(' ', '-').replace('+', '-'),
                 keyed_on='smoke centre' if version == 'v1' else 'where the ship was hit (death position, or position at its largest health fall)', unit='smokes' if version == 'v1' else 'ships at risk',
                 who=KLAB[a['kind']], n_units=a['n'], ships_at_risk=a['den'], died_or_hurt_per_100=r1(a['hurt']), died_per_100=r1(a['died']), n_died_or_hurt=a['n_hurt'], n_died=a['n_died'],
                 baseline_all_maps=dict(died=r1(a['base_all'][0]), died_or_hurt=r1(a['base_all'][1])), baseline_same_map=dict(died=r1(a['base_map'][0]), died_or_hurt=r1(a['base_map'][1])),
                 gap_vs_all_maps=r1(a['hurt'] - a['base_all'][1]), gap_vs_all_maps_ci=[r1(x) for x in a['ci_hurt_all']], gap_vs_same_map=r1(a['hurt'] - a['base_map'][1]), gap_vs_same_map_ci=[r1(x) for x in a['ci_hurt_map']],
                 death_gap_vs_all_maps=r1(a['died'] - a['base_all'][0]), death_gap_vs_all_maps_ci=[r1(x) for x in a['ci_died_all']], death_only_clear=a['flag_died'],
                 behind_50_pct=r1(a['behind_pct']), radar_lit_pct=r1(a['radar_pct']), share_top6_pct=r1(a['share_top']), share_rest_pct=r1(a['share_rest']), share_gap_ci=[r1(x) for x in a['share_gap_ci']], rest_habit=a['rest_habit'],
                 n_clans=a['n_clans'], n_games=a['n_games'], without_top_clan=a['without_top_clan'], health_is_estimate=False,
                 hurt_definition='died between activation and 20 s after dispersal (track), or net health loss over the smoke of 1/3+ of full health',
                 placebo=dict(flags_by_luck_per_run=pl['mean'], areas_tested=n_tested, real_flags=n_flag))
    return spot_record(m, 'danger_zone', a['mode'], f'{a["name"]} ({KLAB[a["kind"]]})', S, sm_, shape, extra)
for a in F1: recs.append(rec_for(a, 'v1', PL1, len(T1), len(F1)))
for a in F2: recs.append(rec_for(a, 'v2', PL2, len(T2), len(F2)))
dump('danger-zones.json', recs)
P(f'\nWrote danger-zones.json ({len(recs)} records: {len(F1)} keyed on the smoke centre, {len(F2)} keyed on where the ship was hit).')
dump('out-danger.json', J)
open(os.path.join(HERE_, 'out-danger.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ---- figures
if '--nofig' not in sys.argv:
    RAMP = ['#f0efec', '#f6d6d5', '#f0a9a8', '#e97c7b', '#e34948', '#a82f2e']
    col = lambda v, vmax: RAMP[min(len(RAMP) - 1, int(max(0, v) / vmax * (len(RAMP) - 1) + 0.5))]
    for m in MAPL:
        slug = m.lower().replace(' ', '-')
        fig = Fig(1000, 1070, f'C3 working figure (round 5b): {m}, ships at risk that died or were hurt, per 100',
                  'Real health. Top row: areas by smoke centre. Bottom row: areas by where the ship was hit. Number = died or hurt per 100, small = n. Red outline = flagged.')
        for row, (TT, unit) in enumerate(((T1, 'smokes'), (T2, 'ships'))):
            for i, k in enumerate(KINDS):
                tm = [a for a in TT if a['map'] == m and a['kind'] == k]; bm = tm[0]['base_map'][1] if tm else 0; ba = tm[0]['base_all'][1] if tm else 0
                p = Panel(m, 50 + i * 480, 100 + row * 455, 400, G, title=f'{KLAB[k]}, by {"smoke centre" if row == 0 else "where hit"}: map {bm:.0f}, all maps {ba:.0f} per 100', dim=0.55)
                for a in tm:
                    if a['type'] == 'cap': continue
                    for c in a['cells']:
                        p.cellfill(c[0], c[1], col(a['hurt'], 60), opacity=0.8, text=f'{a["hurt"]:.0f}', text_fill=BG if a['hurt'] / 60 > 0.6 else INK, sub=f'n {a["n"]}' + ('+' if len(a['cells']) > 1 else ''), stroke=RED if a['flag'] else None)
                for a in tm:
                    if a['type'] != 'cap': continue
                    c = next(c for c in CAPS[m] if c['cap'] == a['cap'])
                    if a['flag']: p.ring(c['x'], c['z'], c['r'] / p.space * p.size, stroke=RED, width=3)
                    p.text(c['x'], c['z'], f'in cap: {a["hurt"]:.0f} (n {a["n"]})', size=9, dy=-12)
                fig.add(p)
        fl = [f'{a["name"]} ({KLAB[a["kind"]]}, by smoke centre) {a["hurt"]:.0f} per 100, n {a["n"]}' for a in F1 if a['map'] == m] + [f'{a["name"]} ({KLAB[a["kind"]]}, by where hit) {a["hurt"]:.0f} per 100, n {a["n"]}' for a in F2 if a['map'] == m]
        for n_, line in enumerate([('Flagged: ' + x) for x in fl] or ['No area on this map is clearly above the baselines.']):
            fig.add(T(50, 990 + 18 * n_, line, size=12, fill=INK, anchor='start', weight='600'))
        fig.save(os.path.join(FIGS, 'n2-danger-' + slug))
        # death positions
        dm = [p for p in DEAD if p['s']['map'] == m]
        fig = Fig(1000, 560, f'Death positions (round 5b working figure): {m}', 'Deaths from activation to 20 s after dispersal. Filled = inside the smoke outline, hollow = outside; line = to the smoke centre. Blue Top 6, orange Rest.')
        for i, (lab, f) in enumerate((('smoking destroyers', lambda p: p['who'] == 'smoking destroyer'), ('sheltering cruisers and others', lambda p: p['who'] != 'smoking destroyer'))):
            v = [p for p in dm if f(p)]
            p_ = Panel(m, 50 + i * 480, 100, 400, G, title=f'{lab}: {len(v)} deaths, {sum(x["in_outline"] for x in v)} inside the outline', dim=0.5)
            for x in v:
                s = x['s']; a = npt(s, x['death_pos']); c_ = GROUP_COLOR[s['grp']]
                p_.line([(s['nx'], s['nz']), a], stroke=c_, width=0.8, opacity=0.45)
            for x in v:
                s = x['s']; a = npt(s, x['death_pos']); c_ = GROUP_COLOR[s['grp']]
                if x['in_outline']: p_.dot(a[0], a[1], r=4, fill=c_, opacity=0.9, stroke=BG)
                else: p_.ring(a[0], a[1], 4, stroke=c_, width=1.8)
            fig.add(p_)
        fig.save(os.path.join(FIGS, 'n2-deaths-' + slug))
print('done')
