# Round 5, worker c1: C3 danger zones. Run: python -I -X utf8 c1_danger.py
# Writes out-danger.md, danger-zones.json and one working figure per map (round5/figures/c1-danger-<map>).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
import random as _r
HERE_ = os.path.dirname(os.path.abspath(__file__))
S, G = load5()
random.seed(53)
OUT = []
def P(*a):
    s = ' '.join(str(x) for x in a); OUT.append(s); print(s)
REPS, PL_RUNS, PL_REPS, MIN_N = 2000, 120, 300, 8
MAPL = sorted(MAPS, key=lambda m: -sum(s['map'] == m for s in S))
CLANS = sorted({s['team'] for s in S})

# pools: 'dd' = destroyer smokes, outcome on the smoker; 'cr' = any smoke covering a cruiser (inside or behind), outcome per sheltering cruiser
POOL = {'dd': [s for s in S if s['cls'] == 'destroyer'], 'cr': [s for s in S if s['n_cr_in'] > 0]}
def outc(kind, s):
    """(died, hurt, denominator)"""
    return (s['d_smoker'], s['hurt_smoker'], 1) if kind == 'dd' else (min(s['d_cr'], s['n_cr_in']), s['hurt_cr'], s['n_cr_in'])
KLAB = {'dd': 'destroyer smoker', 'cr': 'sheltering cruisers'}

def areas_for(kind, m):
    """Areas of one map: single cells with >= 8 smokes; smaller cells merged inside their 2 x 2 block; plus 'inside cap X' zones."""
    ss = [s for s in POOL[kind] if s['map'] == m]; out = []
    cells = by(ss, 'ncell'); small_blocks = collections.defaultdict(list)
    for c, v in cells.items():
        if len(v) >= MIN_N: out.append(dict(kind=kind, map=m, type='cell', cells=[c], members=v))
        else: small_blocks[(c[0] // 2, c[1] // 2)].append(c)
    for b, cs in small_blocks.items():
        v = [s for c in cs for s in cells[c]]
        out.append(dict(kind=kind, map=m, type='cells' if len(cs) > 1 else 'cell', cells=sorted(cs), members=v))
    for cap, v in by([s for s in ss if s['near_cap_edge_m'] <= 0], 'near_ncap').items():
        out.append(dict(kind=kind, map=m, type='cap', cap=cap, cells=[], members=v))
    for a in out:
        a['name'] = (f'inside cap {a["cap"]}' if a['type'] == 'cap' else '+'.join(cell_name(*c) for c in a['cells'])); a['n'] = len(a['members'])
    return out
AREAS = [a for k in POOL for m in MAPL for a in areas_for(k, m)]
TEST = [a for a in AREAS if a['n'] >= MIN_N]

def evaluate(val, reps, rng, want_ci=False):
    """val: {smoke id key: (died, hurt, den)}. Returns per tested area: rates, baselines and intervals of (area - baseline), clans resampled."""
    key = lambda s: (s['game'], s['id'])
    tot = {k: {c: [0, 0, 0] for c in CLANS} for k in POOL}; mp = {(k, m): {c: [0, 0, 0] for c in CLANS} for k in POOL for m in MAPL}
    for k in POOL:
        for s in POOL[k]:
            v = val[k][key(s)]
            for t in (tot[k][s['team']], mp[(k, s['map'])][s['team']]):
                t[0] += v[0]; t[1] += v[1]; t[2] += v[2]
    ar = []
    for a in TEST:
        d = {}
        for s in a['members']:
            v = val[a['kind']][key(s)]; t = d.setdefault(s['team'], [0, 0, 0]); t[0] += v[0]; t[1] += v[1]; t[2] += v[2]
        ar.append(d)
    def rate(t, i): return 100 * t[i] / t[2] if t[2] else None
    res = []
    for a, d in zip(TEST, ar):
        k = a['kind']; A = [sum(x[i] for x in d.values()) for i in range(3)]
        T_ = [sum(x[i] for x in tot[k].values()) for i in range(3)]; M_ = [sum(x[i] for x in mp[(k, a['map'])].values()) for i in range(3)]
        res.append(dict(died=rate(A, 0), hurt=rate(A, 1), den=A[2], n_died=A[0], n_hurt=A[1], base_all=(rate(T_, 0), rate(T_, 1)), base_map=(rate(M_, 0), rate(M_, 1)), d=[[], [], [], []]))
    for _ in range(reps):
        w = C(rng.choices(CLANS, k=len(CLANS)))
        T2 = {k: [sum(w[c] * tot[k][c][i] for c in w) for i in range(3)] for k in POOL}
        M2 = {km: [sum(w[c] * v[c][i] for c in w) for i in range(3)] for km, v in mp.items()}
        for a, d, r in zip(TEST, ar, res):
            A = [0, 0, 0]
            for c, x in d.items():
                n = w.get(c)
                if n: A[0] += n * x[0]; A[1] += n * x[1]; A[2] += n * x[2]
            if not A[2]: continue
            k = a['kind']; t = T2[k]; mm = M2[(k, a['map'])]
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

REAL = {k: {(s['game'], s['id']): outc(k, s) for s in POOL[k]} for k in POOL}
RES = evaluate(REAL, REPS, _r.Random(101))
for a, r in zip(TEST, RES): a.update(r)

P('# C3 danger zones\n')
P('Health is an estimate (r5lib: lower quartile of damage taken by ships of that type that died), so "hurt" (died or lost >= 1/3 of estimated health) is approximate; the death-only rate is exact.')
P('\nBaselines (like-with-like):')
rows = []
for k in POOL:
    ss = POOL[k]; t = [sum(outc(k, s)[i] for s in ss) for i in range(3)]
    rows.append([KLAB[k], 'all maps', len(ss), t[2], f'{100*t[0]/t[2]:.1f}', f'{100*t[1]/t[2]:.1f}'])
    for m in MAPL:
        sm = [s for s in ss if s['map'] == m]; t = [sum(outc(k, s)[i] for s in sm) for i in range(3)]
        rows.append([KLAB[k], m, len(sm), t[2], f'{100*t[0]/t[2]:.1f}', f'{100*t[1]/t[2]:.1f}'])
P(md_table(['who', 'map', 'smokes', 'ships at risk', 'died per 100', 'died or hurt per 100'], rows))
dd = POOL['dd']; P(f'Check: destroyer smokes Top 6 {sum(s["grp"] == "top" for s in dd)}, Rest {sum(s["grp"] == "rest" for s in dd)}; smokes covering a cruiser {len(POOL["cr"])}, sheltering cruisers {sum(s["n_cr_in"] for s in POOL["cr"])}.')
P(f'\nAreas built: {len(AREAS)} (grid cells, merged 2 x 2 groups of thin cells, and "inside cap" zones); with >= {MIN_N} smokes and tested: {len(TEST)} '
  f'({sum(a["kind"] == "dd" for a in TEST)} destroyer, {sum(a["kind"] == "cr" for a in TEST)} cruiser); under {MIN_N} smokes, not rated: {len(AREAS) - len(TEST)}.')
FL = [a for a in TEST if a['flag']]
P(f'Flag rule: >= {MIN_N} smokes and the died-or-hurt rate clearly above BOTH the all-map and the same-map baseline (95% interval of the difference excludes zero, clans resampled, {REPS} resamples).')
P(f'Flagged areas: {len(FL)}. Areas clearly above the all-map baseline only (not above their own map): {sum(a["above_all_only"] for a in TEST)}. Areas that would be flagged on deaths alone: {sum(a["flag_died"] for a in TEST)}.')

# placebo: shuffle outcomes among the smokes of the same map (same pool), keep positions and clans
rngp = _r.Random(202); pl = []; pl_died = []; pl_bymap = C()
for run in range(PL_RUNS):
    val = {}
    for k in POOL:
        val[k] = {}
        for m in MAPL:
            ss = [s for s in POOL[k] if s['map'] == m]; o = [REAL[k][(s['game'], s['id'])] for s in ss]; rngp.shuffle(o)
            for s, v in zip(ss, o): val[k][(s['game'], s['id'])] = v
    r = evaluate(val, PL_REPS, rngp)
    pl.append(sum(x['flag'] for x in r)); pl_died.append(sum(x['flag_died'] for x in r))
    for a, x in zip(TEST, r):
        if x['flag']: pl_bymap[a['map']] += 1
real_small = evaluate(REAL, PL_REPS, _r.Random(303))
P(f'\nPlacebo ({PL_RUNS} runs: outcomes shuffled among the smokes of the same map, same {len(TEST)} areas, same rule, {PL_REPS} resamples each): '
  f'areas flagged by luck per run: mean {mean(pl):.2f}, median {med(pl)}, 95th percentile {q(pl, .95):.0f}, max {max(pl)}; runs with no flag at all: {sum(x == 0 for x in pl)} of {PL_RUNS}; '
  f'runs with at least as many flags as the real data ({len(FL)}): {sum(x >= len(FL) for x in pl)} of {PL_RUNS}.')
P(f'Real data with the same {PL_REPS} resamples: {sum(x["flag"] for x in real_small)} flags. Death-only rule by luck: mean {mean(pl_died):.2f} per run (real: {sum(a["flag_died"] for a in TEST)}).')
P('Luck flags per map per run: ' + ', '.join(f'{m} {pl_bymap[m]/PL_RUNS:.2f}' for m in MAPL))

def fmt_ci(c): return '-' if c[0] is None else f'{c[0]:+.0f} to {c[1]:+.0f}' + (' *' if c[0] * c[1] > 0 else '')
def describe(a):
    mem = a['members']; k = a['kind']; pool = [s for s in POOL[k] if s['map'] == a['map']]
    ids = {(s['game'], s['id']) for s in mem}
    stat = lambda ss: 100 * sum((s['game'], s['id']) in ids for s in ss) / len(ss) if ss else None
    top = [s for s in pool if s['grp'] == 'top']; rest = [s for s in pool if s['grp'] == 'rest']
    d = boot_diff(pool, stat); a['share_top'], a['share_rest'], a['share_gap_ci'] = stat(top), stat(rest), d
    a['mode'] = 'top6' if d[0] is not None and d[0] > 0 else 'shared'
    a['behind_pct'] = pct(mem, lambda s: s['state'] == 'behind 50+'); a['radar_pct'] = pct(mem, lambda s: s['radar_on_us'] > 0)
    a['behind_map_pct'] = pct(pool, lambda s: s['state'] == 'behind 50+'); a['radar_map_pct'] = pct(pool, lambda s: s['radar_on_us'] > 0)
    a['n_clans'] = len({s['team'] for s in mem}); a['n_games'] = len({s['game'] for s in mem})
    # leave-one-clan-out: does the gap survive dropping the biggest contributor of bad outcomes
    worst = C()
    for s in mem: worst[s['team']] += outc(k, s)[1]
    wc = worst.most_common(1)[0][0] if worst else None
    m2 = [s for s in mem if s['team'] != wc]; t = [sum(outc(k, s)[i] for s in m2) for i in range(3)]
    a['without_top_clan'] = dict(clan=wc, n=len(m2), hurt_per_100=round(100 * t[1] / t[2], 1) if t[2] else None)
for a in TEST:
    if a['flag'] or a['above_all_only'] or a['flag_died']: describe(a)

HDR = ['map', 'who', 'area', 'smokes', 'ships at risk', 'died or hurt per 100', 'all-map / same-map baseline', 'gap vs all maps (interval)', 'gap vs same map (interval)', 'died per 100 (baseline all / map)', 'death gap vs all maps', 'flag']
def arow(a):
    return [a['map'], KLAB[a['kind']], a['name'], f'{a["n"]}{small(a["n"])}', a['den'], f'{a["hurt"]:.0f} ({a["n_hurt"]} of {a["den"]})', f'{a["base_all"][1]:.1f} / {a["base_map"][1]:.1f}',
            f'{a["hurt"]-a["base_all"][1]:+.0f} ({fmt_ci(a["ci_hurt_all"])})', f'{a["hurt"]-a["base_map"][1]:+.0f} ({fmt_ci(a["ci_hurt_map"])})',
            f'{a["died"]:.0f} ({a["n_died"]}; {a["base_all"][0]:.1f} / {a["base_map"][0]:.1f})', f'{a["died"]-a["base_all"][0]:+.0f} ({fmt_ci(a["ci_died_all"])})',
            'FLAG' if a['flag'] else 'above all-map only' if a['above_all_only'] else 'deaths only' if a['flag_died'] else '']
recs = []
for m in MAPL:
    P(f'\n## {m}')
    tm = [a for a in TEST if a['map'] == m]; fm = [a for a in tm if a['flag']]
    P(f'Areas tested: {sum(a["kind"] == "dd" for a in tm)} destroyer, {sum(a["kind"] == "cr" for a in tm)} cruiser. Flagged: {len(fm)}.' + ('' if fm else ' No area qualifies on this map.'))
    show = sorted([a for a in tm if a['flag'] or a['above_all_only'] or a['flag_died']], key=lambda a: (not a['flag'], a['kind'], -a['hurt']))
    if show: P(md_table(HDR, [arow(a) for a in show]))
    for a in show:
        P(f'- {a["name"]} ({KLAB[a["kind"]]}){" FLAGGED" if a["flag"] else " (not flagged)"}: {"Top 6 spot" if a["mode"] == "top6" else "Shared spot"} '
          f'(share of the map\'s {"destroyer" if a["kind"] == "dd" else "cruiser-covering"} smokes laid here: Top 6 {a["share_top"]:.0f}%, Rest {a["share_rest"]:.0f}%, gap interval {ci(a["share_gap_ci"], "{:+.0f}")}). '
          f'Laid while 50+ behind: {a["behind_pct"]:.0f}% (map: {a["behind_map_pct"]:.0f}%). Enemy radar detection in the smoke: {a["radar_pct"]:.0f}% (map: {a["radar_map_pct"]:.0f}%). '
          f'{a["n_clans"]} clans, {a["n_games"]} games. {clan_counts(a["members"])}. Without the clan with most bad outcomes ({a["without_top_clan"]["clan"]}): {a["without_top_clan"]["hurt_per_100"]} per 100 (n {a["without_top_clan"]["n"]}).')
    for a in fm:
        mem = a['members']
        if a['type'] == 'cap':
            g = next(g for g in G.values() if g['map'] == m); c = next(c for c in g['caps'] if c['cap'] == a['cap'])
            u, v = uv(m, c['x'], c['z']); shape = dict(type='circle', u=round(u, 4), v=round(v, 4), r=round(c['r'] / MAPS[m]['space_size'], 4))
        else:
            u, v = uv(m, mean(s['nx'] for s in mem), mean(s['nz'] for s in mem)); shape = dict(type='cells', cells=[cell_name(*c) for c in a['cells']], u=round(u, 4), v=round(v, 4))
        r1 = lambda x: None if x is None else round(x, 1)
        extra = dict(who=KLAB[a['kind']], ships_at_risk=a['den'], died_or_hurt_per_100=r1(a['hurt']), died_per_100=r1(a['died']), n_died_or_hurt=a['n_hurt'], n_died=a['n_died'],
                     baseline_all_maps=dict(died=r1(a['base_all'][0]), died_or_hurt=r1(a['base_all'][1])), baseline_same_map=dict(died=r1(a['base_map'][0]), died_or_hurt=r1(a['base_map'][1])),
                     gap_vs_all_maps=r1(a['hurt'] - a['base_all'][1]), gap_vs_all_maps_ci=[r1(x) for x in a['ci_hurt_all']], gap_vs_same_map=r1(a['hurt'] - a['base_map'][1]), gap_vs_same_map_ci=[r1(x) for x in a['ci_hurt_map']],
                     death_gap_vs_all_maps=r1(a['died'] - a['base_all'][0]), death_gap_vs_all_maps_ci=[r1(x) for x in a['ci_died_all']], death_only_clear=a['flag_died'],
                     behind_50_pct=r1(a['behind_pct']), radar_detected_pct=r1(a['radar_pct']), share_top6_pct=r1(a['share_top']), share_rest_pct=r1(a['share_rest']), share_gap_ci=[r1(x) for x in a['share_gap_ci']],
                     n_clans=a['n_clans'], n_games=a['n_games'], without_top_clan=a['without_top_clan'], health_is_estimate=True,
                     placebo=dict(flags_by_luck_per_run=round(mean(pl), 2), areas_tested=len(TEST), real_flags=len(FL)))
        recs.append(spot_record(m, 'danger_zone', a['mode'], f'{a["name"]} ({KLAB[a["kind"]]})', S, mem, shape, extra))
json.dump(recs, open(os.path.join(HERE_, 'danger-zones.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
P(f'\nWrote danger-zones.json ({len(recs)} records).')

# figures: one per map, two panels
RAMP = ['#f0efec', '#f6d6d5', '#f0a9a8', '#e97c7b', '#e34948', '#a82f2e']
def col(v, vmax): return RAMP[min(len(RAMP) - 1, int(max(0, v) / vmax * (len(RAMP) - 1) + 0.5))]
for m in MAPL:
    fig = Fig(1120, 640, f'C3 working figure: {m}, ships in smoke that died or were hurt, per 100',
              'Cells with 8+ smokes (thin cells merged in 2 x 2 groups). Number = died or hurt per 100, small = smokes. Red outline = flagged. Health is an estimate.')
    for i, k in enumerate(POOL):
        tm = [a for a in TEST if a['map'] == m and a['kind'] == k]; bm = tm[0]['base_map'][1] if tm else 0; ba = tm[0]['base_all'][1] if tm else 0
        p = Panel(m, 50 + i * 540, 110, 480, G, title=f'{KLAB[k]}: map baseline {bm:.0f}, all maps {ba:.0f} per 100', dim=0.55)
        vmax = 60
        for a in tm:
            if a['type'] == 'cap': continue
            for c in a['cells']:
                p.cellfill(c[0], c[1], col(a['hurt'], vmax), opacity=0.8, text=f'{a["hurt"]:.0f}', text_fill=BG if a['hurt'] / vmax > 0.6 else INK, sub=f'n {a["n"]}' + ('+' if len(a['cells']) > 1 else ''),
                           stroke=RED if a['flag'] else None)
        for a in tm:
            if a['type'] != 'cap': continue
            g = next(g for g in G.values() if g['map'] == m); c = next(c for c in g['caps'] if c['cap'] == a['cap'])
            if a['flag']: p.ring(c['x'], c['z'], c['r'] / p.space * p.size, stroke=RED, width=3)
            p.text(c['x'], c['z'], f'in cap: {a["hurt"]:.0f} (n {a["n"]})', size=9, dy=-12)
        fig.add(p)
    fl = [a for a in TEST if a['map'] == m and a['flag']]
    fig.add(T(50, 625, ('Flagged: ' + '; '.join(f'{a["name"]} ({KLAB[a["kind"]]}) {a["hurt"]:.0f} per 100, n {a["n"]}' for a in fl)) if fl else 'No area on this map is clearly above the baseline.', size=12, fill=INK, anchor='start', weight='600'))
    fig.save(os.path.join(R5, 'figures', 'c1-danger-' + m.lower().replace(' ', '-')))
open(os.path.join(HERE_, 'out-danger.md'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
print('done')
