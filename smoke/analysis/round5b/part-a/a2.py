# A2. Smoke deaths drill-down. Main frame: destroyer smokes (1,074). Other smoker classes shown at the end.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
L = []; P = lambda *a: L.append(' '.join(str(x) for x in a))
J = {}
MAPS_ = sorted({s['map'] for s in DD}, key=lambda m: -sum(s['map'] == m for s in DD))
tbin = lambda el: '0-5 min' if el < 300 else '5-10 min' if el < 600 else '10-15 min' if el < 900 else '15-20 min'
TB = ['0-5 min', '5-10 min', '10-15 min', '15-20 min']
STATES = ['ahead 50+', 'level', 'behind 50+']

# ---- extra per-smoke fields from the raw records
for s in S:
    r, j = s['r'], s['j']
    s['radar_hit'] = s['radar_on_us'] > 0
    s['en_dd_m'] = min([c['dist_m'] for c in s['cast'] if c['how'] == 'enemy' and c['cls'] == 'destroyer'] or [None], key=lambda v: 1e9 if v is None else v)
    s['en_dd_6k'] = s['en_dd_m'] is not None and s['en_dd_m'] < 6000
    s['near_en_km'] = F(r['nearest_enemy_dist_km_act'])
    s['hp_act'] = F(r['smoker_hp_pct_act'])
    s['spotted_act'] = r['smoker_spotted_act'] == 'true'
    ao, at = F(r['alive_ours_act']), F(r['alive_theirs_act'])
    s['outnumbered'] = ao is not None and at is not None and ao < at
    s['stacked'] = bool(s['overlap_ids'])
    kinds = C(x['kind'] for sm_ in j['smokees'] if sm_['how'] != 'none' for x in sm_.get('detected_by', []))
    s['any_radar'] = kinds['radar'] > 0; s['any_surface'] = kinds['surface lit'] > 0; s['any_hydro'] = kinds['hydro'] > 0; s['any_firepen'] = kinds['smoke fire penalty'] > 0
    s['smk_surface'] = s['detect']['surface lit'] > 0; s['smk_firepen'] = s['detect']['smoke fire penalty'] > 0
    s['short_by_s'] = (s['emission_s'] - s['obs_emission_s']) if s['emission_s'] is not None and s['obs_emission_s'] is not None else None
    smk = {x['entity_id']: x for x in j['smokees']}
    ro = G[s['game']]['roster']
    for d in s['dead']:
        raw = next(x for x in j['smoke_deaths'] if x['entity_id'] == d['eid'])
        td = raw['death']['seconds']
        det = [x for x in smk.get(d['eid'], {}).get('detections', []) if td - 40 <= x['seconds'] <= td + 1]
        d['det40'] = sorted({x['kind'] for x in det})
        d['det_all'] = sorted({x['kind'] for x in smk.get(d['eid'], {}).get('detected_by', [])})
        d['undet'] = smk.get(d['eid'], {}).get('undetected_pct')
        rd = [x for x in j['radar_detections_in_smoke'] if x['ship_entity'] == d['eid'] and td - 40 <= x['seconds'] <= td + 1]
        d['radar_range_m'] = ro.get(rd[-1]['source_entity'], {}).get('radar_m') if rd else None
        d['who'] = 'smoker destroyer' if d['is_smoker'] and d['cls'] == 'destroyer' else 'smoker (other class)' if d['is_smoker'] else 'sheltering cruiser' if d['cls'] == 'cruiser' else 'other sheltering ship'
        d['smoke'] = s
P('raw field check: hp_act sample', [s['hp_act'] for s in DD[:6]], 'spotted', dict(C(s['spotted_act'] for s in DD)), 'near_en_km None', sum(s['near_en_km'] is None for s in DD), 'outnumbered', dict(C(s['outnumbered'] for s in DD)))

DEATHS = [d for s in DD for d in s['dead']]
uniq = {(d['smoke']['game'], d['eid']) for d in DEATHS}
P('\n== 1. Totals (destroyer smokes)')
P('death records', len(DEATHS), '| distinct ships', len(uniq), '(a ship covered by two overlapping smokes is listed under both) | smokes with a death', sum(1 for s in DD if s['dead']), 'of', len(DD))
P('all classes: death records', sum(len(s['dead']) for s in S), 'distinct ships', len({(s['game'], d['eid']) for s in S for d in s['dead']}))
who_rows = []
for w in ('smoker destroyer', 'sheltering cruiser', 'other sheltering ship'):
    v = [d for d in DEATHS if d['who'] == w]
    who_rows.append(dict(who=w, n=len(v), share_pct=r1(100 * len(v) / len(DEATHS)), top6=sum(d['smoke']['grp'] == 'top' for d in v), rest=sum(d['smoke']['grp'] == 'rest' for d in v),
                         inside=sum(d['where'] == 'inside' for d in v), behind=sum(d['where'] == 'behind' for d in v), ships=dict(C(d['ship'] for d in v).most_common(8))))
P(md_table(['who died', 'n', 'share %', 'Top 6', 'Rest', 'inside', 'behind', 'ships'], [[x['who'], x['n'], x['share_pct'], x['top6'], x['rest'], x['inside'], x['behind'], x['ships']] for x in who_rows]))
J['who'] = who_rows
whoshare = share(lambda s: any(d['who'] == 'sheltering cruiser' for d in s['dead']), lambda s: bool(s['dead']))
P('share of death-smokes where a sheltering cruiser died: T6 vs Rest', gap(DD, whoshare))

# ---- rates
D100 = per100('deaths'); DS = per100('d_smoker'); DCR = ratio100('d_cr', 'n_cr_in'); HS = per100('hurt_smoker'); HCR = ratio100('hurt_cr', 'n_cr_in')
def rate_row(label, ss, extra=None):
    row = dict(label=label, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)), deaths=sum(s['deaths'] for s in ss), deaths_per_100=one(ss, D100), split=gap(ss, D100),
               smoker_deaths_per_100=one(ss, DS), cruiser_deaths_per_100_sheltering=one(ss, DCR), note=sm(len(ss)))
    if extra: row.update(extra)
    return row
def rate_table(title, rows):
    P('\n' + title)
    P(md_table(['', 'n (T6/Rest)', 'deaths', 'per 100 [95%]', 'T6', 'Rest', 'T6-Rest', 'smoker per 100', 'cruiser per 100 sheltering (n cruisers)', 'note'],
               [[x['label'], f"{x['n']} ({x['n_top6']}/{x['n_rest']})", x['deaths'], f"{fv(x['deaths_per_100']['value'])} [{fci(x['deaths_per_100'], '{:.1f}')}]", fv(x['split']['top6']), fv(x['split']['rest']), fci(x['split']),
                 fv(x['smoker_deaths_per_100']['value']), f"{fv(x['cruiser_deaths_per_100_sheltering']['value'])} ({x['cruiser_deaths_per_100_sheltering']['n']})", x['note']] for x in rows]))
P('\n== 2. Where and when (deaths per 100 destroyer smokes; smoke placed by activation time and score)')
base = [rate_row('all destroyer smokes', DD)]; rate_table('Baseline', base); J['baseline'] = base
bm = [rate_row(m, [s for s in DD if s['map'] == m]) for m in MAPS_]; rate_table('By map', bm); J['by_map'] = bm
bc = []
for m in MAPS_:
    for cap, ss in sorted(by([s for s in DD if s['map'] == m], 'near_ncap').items()):
        if len(ss) >= MIN_N: bc.append(rate_row(f'{m} cap {cap}', ss, dict(map=m, cap=cap, clans=clan_dict([s for s in ss if s['dead']]), clans_text=clan_counts([s for s in ss if s['dead']]))))
bc.sort(key=lambda x: -(x['deaths_per_100']['value'] or 0)); rate_table('By map and nearest cap (normalized letter; own spawn at the bottom), n >= 8, highest first', bc); J['by_map_cap'] = bc
for x in bc[:6]: P('  clans with a death there:', x['label'], '|', x['clans_text'])
bt = [rate_row(t, [s for s in DD if tbin(s['el']) == t]) for t in TB]; rate_table('By time of activation', bt); J['by_time'] = bt
bs = [rate_row(st, [s for s in DD if s['state'] == st]) for st in STATES]; rate_table('By score state at activation', bs); J['by_state'] = bs
bts = [rate_row(f'{t}, {st}', [s for s in DD if tbin(s['el']) == t and s['state'] == st]) for t in TB for st in STATES]
bts = [x for x in bts if x['n'] >= MIN_N]; rate_table('By time and score state', bts); J['by_time_state'] = bts
P('death-time of the ships (elapsed at death):', dict(C(tbin(d['t']) for d in DEATHS)))
P('who dies by score state:', {st: dict(C(d['who'] for d in DEATHS if d['smoke']['state'] == st)) for st in STATES})
P('who dies by time:', {t: dict(C(d['who'] for d in DEATHS if tbin(d['smoke']['el']) == t)) for t in TB})

# ---- radar deaths
P('\n== 3. Radar deaths (enemy radar detected the ship in this smoke within 40 s before it died)')
RD = [d for d in DEATHS if d['radar_lit']]
P('radar deaths', len(RD), 'of', len(DEATHS), f'({100*len(RD)/len(DEATHS):.0f}%) | distinct ships', len({(d['smoke']['game'], d['eid']) for d in RD}), '| Top 6', sum(d['smoke']['grp'] == 'top' for d in RD), 'Rest', sum(d['smoke']['grp'] == 'rest' for d in RD))
P('who', dict(C(d['who'] for d in RD)), '| where', dict(C(d['where'] for d in RD)), '| after cleared', dict(C(d['after_cleared'] for d in RD)))
P('by map', dict(C(d['smoke']['map'] for d in RD).most_common()))
P('by map+cap', dict(C(d['smoke']['map'] + ' ' + d['smoke']['near_ncap'] for d in RD).most_common()))
P('by time of smoke', dict(C(tbin(d['smoke']['el']) for d in RD)), '| by state', dict(C(d['smoke']['state'] for d in RD)))
P('radar ship class', dict(C(d['radar_src']['cls'] for d in RD)), '| radar ship', dict(C(d['radar_src']['ship'] for d in RD).most_common()))
dist = sorted(d['radar_src']['dist_m'] for d in RD)
P('distance from the radar ship (m): min', round(dist[0]), 'q25', round(q(dist, .25)), 'median', round(med(dist)), 'q75', round(q(dist, .75)), 'max', round(dist[-1]))
P('distance bands:', dict(C('under 6 km' if x < 6000 else '6-8 km' if x < 8000 else '8-10 km' if x < 10000 else '10 km+' for x in dist)))
fr = [d['radar_src']['dist_m'] / d['radar_range_m'] for d in RD if d['radar_range_m']]
P('distance as share of that ship\'s radar range: n', len(fr), 'median', r1(med(fr), 2), 'share beyond 80% of range', r1(pct(fr, lambda v: v > .8)), 'share under 60%', r1(pct(fr, lambda v: v < .6)))
P('by radar class: n, median distance', {c: (len(v), round(med(x['radar_src']['dist_m'] for x in v))) for c, v in by(RD, lambda d: d['radar_src']['cls']).items()})
P('killing damage in radar deaths: top kind', dict(C(d['top_kind'] for d in RD)), '| torpedo damage in last 20 s', sum(d['torp'] for d in RD), '| biggest damage from class', dict(C(max(d['by_cls'], key=d['by_cls'].get) if d['by_cls'] else 'none' for d in RD)))
# rate when radar reached the smoke, by radar source class (all radar detections on our ships in the smoke)
def radar_classes(s):
    ro = G[s['game']]['roster']
    return {(ro.get(x['source_entity'], {}).get('ship_class') or '').lower() for x in s['j']['radar_detections_in_smoke']}
for s in DD: s['radar_cls'] = radar_classes(s)
rr = [rate_row('enemy radar reached the smoke', [s for s in DD if s['radar_hit']]), rate_row('no enemy radar', [s for s in DD if not s['radar_hit']])]
for c in ('cruiser', 'destroyer', 'battleship'):
    rr.append(rate_row(f'radar from an enemy {c}', [s for s in DD if c in s['radar_cls']]))
for m in MAPS_: rr.append(rate_row(f'radar reached, {m}', [s for s in DD if s['radar_hit'] and s['map'] == m]))
for t in TB: rr.append(rate_row(f'radar reached, {t}', [s for s in DD if s['radar_hit'] and tbin(s['el']) == t]))
for st in STATES: rr.append(rate_row(f'radar reached, {st}', [s for s in DD if s['radar_hit'] and s['state'] == st]))
rr.append(rate_row('radar reached, a cruiser sheltering', [s for s in DD if s['radar_hit'] and s['n_cr_in'] > 0]))
rr.append(rate_row('radar reached, no cruiser sheltering', [s for s in DD if s['radar_hit'] and s['n_cr_in'] == 0]))
rate_table('Deaths per 100 where enemy radar reached a ship in the smoke', rr); J['radar_rates'] = rr
P('radar reached vs not, difference:', diff2([s for s in DD if s['radar_hit']], [s for s in DD if not s['radar_hit']], D100))
P('share of smokes radar reached: T6 vs Rest', gap(DD, share(lambda s: s['radar_hit'])))
rc = [rate_row(f'{m} cap {cap}, radar reached', ss) for m in MAPS_ for cap, ss in sorted(by([s for s in DD if s['map'] == m and s['radar_hit']], 'near_ncap').items()) if len(ss) >= MIN_N]
rate_table('Radar-reached smokes by map and cap (n >= 8)', rc); J['radar_by_map_cap'] = rc
J['radar_deaths'] = dict(n=len(RD), of=len(DEATHS), who=dict(C(d['who'] for d in RD)), by_map=dict(C(d['smoke']['map'] for d in RD)), by_time=dict(C(tbin(d['smoke']['el']) for d in RD)), by_state=dict(C(d['smoke']['state'] for d in RD)),
                         radar_class=dict(C(d['radar_src']['cls'] for d in RD)), radar_ship=dict(C(d['radar_src']['ship'] for d in RD)), dist_m=dict(min=round(dist[0]), q25=round(q(dist, .25)), median=round(med(dist)), q75=round(q(dist, .75)), max=round(dist[-1])),
                         dist_share_of_range_median=r1(med(fr), 2), clans=clan_dict([d['smoke'] for d in RD]))
P('clans (radar deaths):', clan_counts([d['smoke'] for d in RD]))
# broad measure: the per-ship detection list shows a radar flag in the 40 s before death (no radar ship or distance recorded there)
RB = [d for d in DEATHS if 'radar' in d['det40']]
P(''); P('BROAD radar deaths (radar flag on the victim in its last 40 s, per-ship detection list):', len(RB), 'of', len(DEATHS), f'({100*len(RB)/len(DEATHS):.0f}%) | of which also strict', sum(d['radar_lit'] for d in RB), '| strict but not broad', sum(1 for d in RD if 'radar' not in d['det40']))
P('  Top 6', sum(d['smoke']['grp'] == 'top' for d in RB), 'Rest', sum(d['smoke']['grp'] == 'rest' for d in RB), '| who', dict(C(d['who'] for d in RB)), '| where', dict(C(d['where'] for d in RB)), '| after cleared', sum(d['after_cleared'] for d in RB))
P('  by map', dict(C(d['smoke']['map'] for d in RB).most_common()), '| deaths on that map', dict(C(d['smoke']['map'] for d in DEATHS).most_common()))
P('  by map+cap', dict(C(d['smoke']['map'] + ' ' + d['smoke']['near_ncap'] for d in RB).most_common(10)))
P('  by time of smoke', dict(C(tbin(d['smoke']['el']) for d in RB)), '| by state', dict(C(d['smoke']['state'] for d in RB)))
P('  also surface lit in the last 40 s', sum('surface lit' in d['det40'] for d in RB), '| biggest damage from class', dict(C(max(d['by_cls'], key=d['by_cls'].get) if d['by_cls'] else 'none' for d in RB)))
P('  clans:', clan_counts([d['smoke'] for d in RB]))
P('  share of smokes with the broad radar flag: ', one(DD, share(lambda s: s['any_radar'])), gap(DD, share(lambda s: s['any_radar'])), '| strict radar_on_us and broad both', sum(1 for s in DD if s['radar_hit'] and s['any_radar']), 'strict only', sum(1 for s in DD if s['radar_hit'] and not s['any_radar']), 'broad only', sum(1 for s in DD if s['any_radar'] and not s['radar_hit']))
rb = [rate_row('radar flag on a covered ship (broad)', [s for s in DD if s['any_radar']]), rate_row('no radar flag (broad)', [s for s in DD if not s['any_radar']])]
for m in MAPS_: rb.append(rate_row(f'radar flag (broad), {m}', [s for s in DD if s['any_radar'] and s['map'] == m]))
for st in STATES: rb.append(rate_row(f'radar flag (broad), {st}', [s for s in DD if s['any_radar'] and s['state'] == st]))
for t in TB: rb.append(rate_row(f'radar flag (broad), {t}', [s for s in DD if s['any_radar'] and tbin(s['el']) == t]))
rate_table('Deaths per 100 by the broad radar measure', rb); J['radar_rates_broad'] = rb
P('broad radar vs not, difference:', diff2([s for s in DD if s['any_radar']], [s for s in DD if not s['any_radar']], D100))
J['radar_deaths_broad'] = dict(n=len(RB), of=len(DEATHS), who=dict(C(d['who'] for d in RB)), by_map=dict(C(d['smoke']['map'] for d in RB)), by_time=dict(C(tbin(d['smoke']['el']) for d in RB)), by_state=dict(C(d['smoke']['state'] for d in RB)), clans=clan_dict([d['smoke'] for d in RB]))

# ---- everything else
P('\n== 4. What else goes with deaths (smoke level: deaths per 100 with the condition vs without)')
CONDS = [('50+ behind at activation', lambda s: s['state'] == 'behind 50+'),
         ('enemy radar reached a ship in the smoke', lambda s: s['radar_hit']),
         ('a covered ship was lit by surface spotting (seen by an enemy ship)', lambda s: s['any_surface']),
         ('smoker lit by surface spotting', lambda s: s['smk_surface']),
         ('a covered ship lit for firing from smoke (smoke fire penalty)', lambda s: s['any_firepen']),
         ('enemy hydro reached a covered ship', lambda s: s['any_hydro']),
         ('enemy destroyer within 6 km of the smoke when laid', lambda s: s['en_dd_6k']),
         ('nearest enemy under 6 km at activation', lambda s: s['near_en_km'] is not None and s['near_en_km'] < 6),
         ('smoker already spotted at activation', lambda s: s['spotted_act']),
         ('smoker under half health at activation', lambda s: s['hp_act'] is not None and s['hp_act'] < 50),
         ('team outnumbered at activation', lambda s: s['outnumbered']),
         ('smoke emission cut short', lambda s: s['cut_short']),
         ('a covered ship carried the radar flag while concealed (broad measure)', lambda s: s['any_radar']),
         ('overlaps another smoke', lambda s: s['stacked']),
         ('several ships share the smoke (batch coverage = stacked)', lambda s: s['coverage'] == 'stacked'),
         ('a cruiser sheltering (inside or behind)', lambda s: s['n_cr_in'] > 0),
         ('smoke centre inside the cap', lambda s: s['inside']),
         ('first 5 minutes', lambda s: s['el'] < 300)]
def cond_table(base, title):
    rows = []
    for name, f in CONDS:
        a = [s for s in base if f(s)]; b = [s for s in base if not f(s)]
        x = diff2(a, b, D100); xs = diff2(a, b, DS); xc = diff2(a, b, DCR)
        rows.append(dict(condition=name, n_with=len(a), n_without=len(b), deaths_per_100_with=x['a'], deaths_per_100_without=x['b'], diff=x['diff'], lo=x['lo'], hi=x['hi'], clear=x['clear'],
                         smoker_with=xs['a'], smoker_without=xs['b'], smoker_lo=xs['lo'], smoker_hi=xs['hi'], smoker_clear=xs['clear'],
                         cruiser_with=xc['a'], cruiser_n_with=xc['n_a'], cruiser_without=xc['b'], cruiser_n_without=xc['n_b'], cruiser_lo=xc['lo'], cruiser_hi=xc['hi'], cruiser_clear=xc['clear'],
                         top6_with=D100(TOPS(a)), rest_with=D100(RESTS(a)), n_top6_with=len(TOPS(a)), n_rest_with=len(RESTS(a))))
    rows.sort(key=lambda r: -(r['diff'] if r['diff'] is not None else -99))
    P('\n' + title)
    P(md_table(['condition', 'n with / without', 'deaths per 100 with', 'without', 'diff interval', 'smoker per 100 with / without (interval)', 'cruiser per 100 sheltering with (n) / without (n) (interval)', 'T6 with (n)', 'Rest with (n)'],
               [[r['condition'], f"{r['n_with']} / {r['n_without']}", fv(r['deaths_per_100_with']), fv(r['deaths_per_100_without']), fci(r), f"{fv(r['smoker_with'])} / {fv(r['smoker_without'])} ({fci(dict(lo=r['smoker_lo'], hi=r['smoker_hi']))})",
                 f"{fv(r['cruiser_with'])} ({r['cruiser_n_with']}) / {fv(r['cruiser_without'])} ({r['cruiser_n_without']}) ({fci(dict(lo=r['cruiser_lo'], hi=r['cruiser_hi']))})", f"{fv(r1(r['top6_with']))} ({r['n_top6_with']})", f"{fv(r1(r['rest_with']))} ({r['n_rest_with']})"] for r in rows]))
    return rows
J['conditions_all'] = cond_table(DD, 'All destroyer smokes')
CALM = [s for s in DD if s['state'] != 'behind 50+' and not s['radar_hit'] and not s['any_radar']]
P('\nsmokes neither 50+ behind nor reached by radar (strict or broad):', len(CALM), 'deaths', sum(s['deaths'] for s in CALM), 'per 100', r1(D100(CALM)), '| the other smokes:', len(DD) - len(CALM), 'deaths', sum(s['deaths'] for s in DD) - sum(s['deaths'] for s in CALM))
J['conditions_calm'] = cond_table(CALM, 'Only smokes that were neither 50+ behind nor reached by enemy radar')
J['calm'] = dict(n=len(CALM), deaths=sum(s['deaths'] for s in CALM), per_100=r1(D100(CALM)), split=gap(CALM, D100))
P('calm T6 vs Rest', J['calm']['split'])
# combos
cmb = []
for a_name, fa in (('surface lit', lambda s: s['any_surface']), ('not surface lit', lambda s: not s['any_surface'])):
    for b_name, fb in (('radar', lambda s: s['radar_hit']), ('no radar', lambda s: not s['radar_hit'])):
        for c_name, fc in (('behind 50+', lambda s: s['state'] == 'behind 50+'), ('not behind', lambda s: s['state'] != 'behind 50+')):
            cmb.append(rate_row(f'{a_name}, {b_name}, {c_name}', [s for s in DD if fa(s) and fb(s) and fc(s)]))
rate_table('Surface spotting x radar x score', cmb); J['combos'] = cmb
# victim level
P('\nVictim level (each death record in a destroyer smoke)')
def vt(v, label):
    P(label, 'n', len(v))
    P('  detection kinds on the victim in the 40 s before death:', dict(C(k for d in v for k in d['det40']).most_common()), '| none recorded', sum(1 for d in v if not d['det40']))
    P('  died just after the smoke cleared:', sum(d['after_cleared'] for d in v), '| torpedo damage in last 20 s:', sum(d['torp'] for d in v), '| no damage rows in last 20 s:', sum(1 for d in v if not d['kinds']))
    P('  top damage kind:', dict(C(d['top_kind'] for d in v).most_common()), '| biggest damage came from class:', dict(C(max(d['by_cls'], key=d['by_cls'].get) if d['by_cls'] else 'none' for d in v).most_common()))
    P('  median share of concealed time undetected (victim):', r1(med([d['undet'] for d in v if d['undet'] is not None])))
    return dict(n=len(v), det40=dict(C(k for d in v for k in d['det40'])), none_detected=sum(1 for d in v if not d['det40']), after_cleared=sum(d['after_cleared'] for d in v), torpedo=sum(d['torp'] for d in v),
                top_kind=dict(C(str(d['top_kind']) for d in v)), biggest_from_class=dict(C(max(d['by_cls'], key=d['by_cls'].get) if d['by_cls'] else 'none' for d in v)))
J['victims'] = {}
for label, v in (('all deaths', DEATHS), ('smoker destroyer', [d for d in DEATHS if d['who'] == 'smoker destroyer']), ('sheltering cruiser', [d for d in DEATHS if d['who'] == 'sheltering cruiser']),
                 ('radar deaths', RD), ('non-radar deaths', [d for d in DEATHS if not d['radar_lit']]),
                 ('non-radar, not 50+ behind', [d for d in DEATHS if not d['radar_lit'] and d['smoke']['state'] != 'behind 50+'])):
    J['victims'][label] = vt(v, label)
NR = [d for d in DEATHS if not d['radar_lit']]
def tag(d):
    t = []
    if d['smoke']['state'] == 'behind 50+': t.append('behind 50+')
    if 'radar' in d['det40']: t.append('radar flag (broad)')
    if 'surface lit' in d['det40']: t.append('surface lit')
    if 'smoke fire penalty' in d['det40']: t.append('lit for firing')
    if 'hydro' in d['det40']: t.append('hydro')
    if d['after_cleared']: t.append('after smoke cleared')
    if d['torp']: t.append('torpedo')
    return t
P('non-radar deaths, marks (a death can carry several):', dict(C(t for d in NR for t in tag(d)).most_common()), '| no mark at all', sum(1 for d in NR if not tag(d)))
P('non-radar deaths, exclusive order (radar flag broad > after cleared > surface lit > lit for firing > hydro > torpedo > behind 50+ only > none):',
  dict(C(next((k for k in ('radar flag (broad)', 'after smoke cleared', 'surface lit', 'lit for firing', 'hydro', 'torpedo', 'behind 50+') if k in tag(d)), 'none') for d in NR).most_common()))
J['non_radar_marks'] = dict(n=len(NR), marks=dict(C(t for d in NR for t in tag(d))), no_mark=sum(1 for d in NR if not tag(d)))
# cut short
cs = [s for s in DD if s['cut_short']]
P('\nsmoke cut short: n', len(cs), 'median seconds lost', r1(med(s['short_by_s'] for s in cs if s['short_by_s'] is not None)), 'smoker died', sum(s['d_smoker'] for s in cs), 'deaths', sum(s['deaths'] for s in cs),
  '| cut short and smoker died BEFORE dispersal (the cut may be the death itself):', sum(1 for s in cs if any(d['is_smoker'] and not d['after_cleared'] for d in s['dead'])))

# ---- like-with-like baselines
P('\n== 5. Like-with-like baselines')
bl = []
for label, st, d in (('destroyer died in its own smoke, per 100 destroyer smokes', DS, None), ('cruiser died while sheltering, per 100 sheltering cruisers', DCR, None),
                     ('destroyer hurt in its own smoke (died or lost 1/3+ of estimated health), per 100', HS, None), ('cruiser hurt while sheltering, per 100 sheltering cruisers', HCR, None), ('any death, per 100 destroyer smokes', D100, None)):
    bl.append(dict(measure=label, all=one(DD, st), split=gap(DD, st)))
P(md_table(['measure', 'all (n) [95%]', 'Top 6 (n)', 'Rest (n)', 'T6-Rest interval'], [[x['measure'], f"{fv(x['all']['value'])} ({x['all']['n']}) [{fci(x['all'], '{:.1f}')}]", f"{fv(x['split']['top6'])} ({x['split']['n_top6']})", f"{fv(x['split']['rest'])} ({x['split']['n_rest']})", fci(x['split'])] for x in bl]))
J['like_with_like'] = bl
ins = ratio100('d_in', 'n_in'); beh = ratio100('d_beh', 'n_beh')
for s in DD:
    s['n_in'] = sum(1 for x in s['shelter'] if x['cls'] == 'cruiser' and x['how'] == 'inside'); s['n_beh'] = sum(1 for x in s['shelter'] if x['cls'] == 'cruiser' and x['how'] == 'behind')
    s['d_in'] = sum(1 for x in s['shelter'] if x['cls'] == 'cruiser' and x['how'] == 'inside' and x['died']); s['d_beh'] = sum(1 for x in s['shelter'] if x['cls'] == 'cruiser' and x['how'] == 'behind' and x['died'])
P('cruiser inside the smoke: died per 100', one(DD, ins), gap(DD, ins)); P('cruiser behind the smoke: died per 100', one(DD, beh), gap(DD, beh))
J['cruiser_inside'] = dict(all=one(DD, ins), split=gap(DD, ins)); J['cruiser_behind'] = dict(all=one(DD, beh), split=gap(DD, beh))
P('radar cruiser vs other cruiser sheltering (deaths / sheltering):', {k: (sum(x['died'] for x in v), len(v)) for k, v in by([dict(x, radar=bool(G[s['game']]['roster'].get(x['eid'], {}).get('radar_m'))) for s in DD for x in s['shelter'] if x['cls'] == 'cruiser' and x['how'] in ('inside', 'behind')], 'radar').items()})
# all smoker classes
P('\nAll classes of smoker')
ac = []
for c in ('destroyer', 'cruiser', 'battleship'):
    ss = [s for s in S if s['cls'] == c]
    ac.append(dict(smoker_class=c, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)), deaths_per_100=one(ss, D100), smoker_deaths_per_100=one(ss, DS), split_smoker=gap(ss, DS),
                   radar_reached=diff2([s for s in ss if s['radar_hit']], [s for s in ss if not s['radar_hit']], DS), behind=diff2([s for s in ss if s['state'] == 'behind 50+'], [s for s in ss if s['state'] != 'behind 50+'], DS),
                   radar_deaths=sum(1 for s in ss for d in s['dead'] if d['radar_lit']), deaths=sum(len(s['dead']) for s in ss), after_cleared=sum(1 for s in ss for d in s['dead'] if d['after_cleared'])))
P(md_table(['smoker class', 'n (T6/Rest)', 'any death per 100', 'smoker died per 100 [95%]', 'T6', 'Rest', 'T6-Rest', 'radar reached: smoker died with/without (interval)', '50+ behind: with/without (interval)', 'death records (radar-lit, after cleared)'],
           [[x['smoker_class'], f"{x['n']} ({x['n_top6']}/{x['n_rest']})", fv(x['deaths_per_100']['value']), f"{fv(x['smoker_deaths_per_100']['value'])} [{fci(x['smoker_deaths_per_100'], '{:.1f}')}]", fv(x['split_smoker']['top6']), fv(x['split_smoker']['rest']), fci(x['split_smoker']),
             f"{fv(x['radar_reached']['a'])} ({x['radar_reached']['n_a']}) / {fv(x['radar_reached']['b'])} ({x['radar_reached']['n_b']}) ({fci(x['radar_reached'])})", f"{fv(x['behind']['a'])} ({x['behind']['n_a']}) / {fv(x['behind']['b'])} ({x['behind']['n_b']}) ({fci(x['behind'])})",
             f"{x['deaths']} ({x['radar_deaths']}, {x['after_cleared']})"] for x in ac]))
J['all_classes'] = ac
crs = [s for s in S if s['cls'] == 'cruiser']
P('cruiser smokes: smoker deaths by ship', dict(C(s['ship'] for s in crs if s['d_smoker']).most_common()), 'smokes by ship', dict(C(s['ship'] for s in crs).most_common(8)))
P('cruiser smokes: smoker died per 100 by kind', {k: (len(v), r1(DS(v))) for k, v in by(crs, 'kind').items()})

# ---- figure: where the deaths are
fig = Fig(1230, 760, 'A2. Destroyer smokes in which a ship died', 'Dot = centre of a smoke with a death. Blue Top 6, orange Rest. Black ring = the ship was lit by enemy radar within 40 s of dying. Grey = all other destroyer smokes.')
fig.legend(40, 72, [('Top 6', BLUE), ('Rest', ORANGE), ('no death', '#b9b8b3')])
for i, m in enumerate(MAPS_):
    ms = [s for s in DD if s['map'] == m]
    p = Panel(m, 40 + (i % 4) * 295, 112 + (i // 4) * 325, 260, G, title=f'{m}: {sum(s["deaths"] for s in ms)} deaths, {D100(ms):.1f} per 100 (n {len(ms)})')
    for s in ms:
        if not s['dead']: p.dot(s['nx'], s['nz'], r=1.8, fill='#8a8984', opacity=0.35)
    for s in ms:
        if s['dead']:
            p.dot(s['nx'], s['nz'], r=4.5, fill=GROUP_COLOR[s['grp']], opacity=0.85, stroke=BG)
            if any(d['radar_lit'] for d in s['dead']): p.ring(s['nx'], s['nz'], 7, stroke=INK, width=1.6)
    fig.add(p)
fig.save(os.path.join(FIGS, 'a2-deaths-by-map'))
# figure: conditions
rows = [r for r in J['conditions_all'] if r['deaths_per_100_with'] is not None]
fig = Fig(980, 120 + 30 * len(rows), 'A2. What goes with deaths in destroyer smokes', 'Deaths per 100 smokes with the condition (dark) and without it (light). n with the condition on the right. * = interval of the difference excludes zero.')
y = 80
for r in rows:
    fig.add(T(430, y + 16, r['condition'] + (' *' if r['clear'] else ''), size=11.5, fill=INK, anchor='end'))
    for k, (v, col) in enumerate(((r['deaths_per_100_with'], VIOLET), (r['deaths_per_100_without'], '#c9c4f0'))):
        fig.add(f'<rect x="440" y="{y+3+k*11}" width="{max(1, v*12):.1f}" height="10" rx="2" fill="{col}"/>' + T(445 + v * 12, y + 12 + k * 11, f'{v:.1f}', size=9.5, anchor='start'))
    fig.add(T(950, y + 16, f"n {r['n_with']}", size=10, anchor='end'))
    y += 30
fig.save(os.path.join(FIGS, 'a2-death-conditions'))
out('out-a2', J, '\n'.join(L))
