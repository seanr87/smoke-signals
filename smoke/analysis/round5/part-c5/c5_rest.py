import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c5lib import *
R = {}
def by_ship_clan(v):
    return {sh: clan_dict(w) for sh, w in sorted(by(v, 'ship').items(), key=lambda x: -len(x[1]))}
def spotline(nm, pool, mem, g):
    P(f' {nm}: {gtxt(g)} -> {g["mark"]}'); P('   ', clan_counts(mem))
    for sh, w in sorted(by(mem, 'ship').items(), key=lambda x: -len(x[1])): P(f'     {sh} {len(w)}: {clan_counts(w)}')
    for t, w in sorted(by(pool, 'team').items(), key=lambda x: (grp_of(x[0]) != 'top', -len(x[1]))): P(f'       {t} ({grp_of(t)}): {sum(1 for s in w if s in mem)} of {len(w)} of the clan\'s smokes with this ship group on the map')

# ---------------- Mountain Range
m = 'Mountain Range'; ms = on(m)
P('=== MR-1 far-west parked cruiser smoke (Svea / Jinan)')
rec = r4_spot('mr-parked-h1'); park = [s for s in ms if s['habit'] == 'parked cruiser smoke']; mem = [s for s in park if in_r4(rec, s)]
g = gap(park, lambda s: in_r4(rec, s)); spotline('spot', park, mem, g)
for sh in ('Svea', 'Jinan'):
    v = [s for s in park if s['ship'] == sh]; P(f'   {sh} on the map: {clan_counts(v)} | in spot {gtxt(gap(v, lambda s: in_r4(rec, s)))}')
P('   fielded (team-games with the ship): ' + ', '.join(f'{sh}: Top 6 {len({(g_["key"], p["team"]) for g_ in games_on(m) for p in g_["roster"].values() if p["ship"] == sh and p["team"] in TOP})}, Rest {len({(g_["key"], p["team"]) for g_ in games_on(m) for p in g_["roster"].values() if p["ship"] == sh and p["team"] not in TOP})}' for sh in ('Svea', 'Jinan')))
P('   Jinan lineups by clan', cc(C(p['team'] for g_ in games_on(m) for p in g_['roster'].values() if p['ship'] == 'Jinan')), '| Svea lineups', cc(C(p['team'] for g_ in games_on(m) for p in g_['roster'].values() if p['ship'] == 'Svea'), 12))
P(f'   members: conc {kf(mean(s["conc"] for s in mem))} median {kf(med(s["conc"] for s in mem))} deaths {sum(s["deaths"] for s in mem)} | cells {cc(C(s["ncell_name"] for s in mem))} | median time {clock(med(s["el"] for s in mem))} | games {len(set(s["game"] for s in mem))} | selfish {sum(s["selfish"] for s in mem)} | pp {cc(C(s["pp"] for s in mem))} | radar from inside {sum(bool(s["off_radar"]) for s in mem)}')
P('   any ship, any class in the ellipse:', gtxt(gap(ms, lambda s: in_r4(rec, s))), '|', cc(C(s['ship'] for s in ms if in_r4(rec, s))), '|', clan_counts([s for s in ms if in_r4(rec, s)]))
gsv = gap([s for s in park if s['ship'] == 'Svea'], lambda s: in_r4(rec, s))
R['MR-1'] = dict(spot=g, clans=clan_dict(mem), by_ship=by_ship_clan(mem), svea_only=gsv, all_ships_in_ellipse=gap(ms, lambda s: in_r4(rec, s)))
SPOTS.append(dict(id='c5-mr-parked-west', **spot_record(m, 'top6_spot', 'top6', 'Parked cruiser smoke (Jinan, Svea), far west edge on the rim of cap A', S, mem, ell_shape(rec),
             dict(subject='parked cruiser smoke (Svea, Jinan)', share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']], by_ship=by_ship_clan(mem),
                  note='Two clans only (HTDOG, BONKZ); 8 of 12 are Jinan, which no Rest clan smoked with on this map.'))))

P('\n=== MR-2 radar from smoke at cap B: defence?')
ct = cap_table(m); P(cap_md(ct))
rp_dd = [s for s in ms if s['cls'] == 'destroyer' and s['radar_play'] and s['ncap'] == 'B']; P(' reproduce atlas: destroyer radar plays with contested cap B:', len(rp_dd), 'Top 6', sum(s['grp'] == 'top' for s in rp_dd), '| cap_won', sum(s['cap_won'] for s in rp_dd if s['own'] != 'ours'), 'of', sum(s['own'] != 'ours' for s in rp_dd))
def radar(s): return s['radar_play'] or bool(s['off_radar'])
sets = [('radar play (primary purpose cap_control or radar_trap), nearest cap B', [s for s in ms if s['radar_play'] and s['zone'] == 'B']),
        ('radar activated from inside (off_radar), nearest cap B', [s for s in ms if s['off_radar'] and s['zone'] == 'B']),
        ('either, nearest cap B', [s for s in ms if radar(s) and s['zone'] == 'B']),
        ('other smokes nearest cap B (no radar)', [s for s in ms if not radar(s) and s['zone'] == 'B']),
        ('radar smokes at other caps on the map', [s for s in ms if radar(s) and s['zone'] != 'B']),
        ('radar smokes at any cap, other maps', [s for s in S if radar(s) and s['map'] != m])]
N2 = lambda s: s['near_cap_edge_m'] <= 2000
sets += [('radar smokes inside or within 2 km of B', [s for s in ms if radar(s) and s['zone'] == 'B' and N2(s)]), ('other smokes inside or within 2 km of B (no radar)', [s for s in ms if not radar(s) and s['zone'] == 'B' and N2(s)]),
         ('radar smokes within 2 km of a cap, other maps', [s for s in S if radar(s) and s['map'] != m and N2(s)])]
P(' distance of the 15 radar smokes from the B edge (m): median', med(s['near_cap_edge_m'] for s in sets[2][1]), 'max', max(s['near_cap_edge_m'] for s in sets[2][1]))
P(cap_md(cap_table(m, edge=2000)))
mr2 = {}; trs = []
for nm, v in sets:
    kn = [s for s in v if s['enemy_took'] is not None]; o = [s for s in v if s['near_own'] == 'ours']; ko = [s for s in o if s['enemy_took'] is not None]; wk = [s for s in v if s['we_took'] is not None]
    d = dict(n=len(v), top6=sum(s['grp'] == 'top' for s in v), ours=len(o), neutral=sum(s['near_own'] == 'neutral' for s in v), theirs=sum(s['near_own'] == 'theirs' for s in v),
             enemy_took=[sum(1 for s in kn if s['enemy_took']), len(kn)], enemy_took_when_ours=[sum(1 for s in ko if s['enemy_took']), len(ko)], we_took=[sum(1 for s in wk if s['we_took']), len(wk)],
             cap_defended_this_cap=sum(s['r']['cap_defended'] == s['near_cap'] for s in v), conc=round(mean(s['conc'] for s in v)) if v else None, deaths=sum(s['deaths'] for s in v),
             ships=dict(C(s['ship'] for s in v).most_common(8)), clans=clan_dict(v), spotted=sum(1 for s in v if s['off_radar'] and s['off_radar']['enemies_spotted'] > 0))
    mr2[nm] = d
    f = lambda k, n: f'{k} of {n}' + (f' ({100 * k / n:.0f}%)' if n >= 8 else ' (too few)')
    trs.append([nm, len(v), d['top6'], f"{d['ours']} / {d['neutral']} / {d['theirs']}", f(*d['enemy_took']), f(*d['enemy_took_when_ours']), f(*d['we_took']), d['cap_defended_this_cap'], kf(d['conc']), d['deaths']])
    P(f'   {nm}: ships {cc(C(s["ship"] for s in v))} | {clan_counts(v)} | pp {cc(C(s["pp"] for s in v))} | cells {cc(C(s["ncell_name"] for s in v), 5)} | cruisers inside {cc(cruiser_counts(v, "inside"), 5)} | radar spotted an enemy {d["spotted"]} | median time {clock(med(s["el"] for s in v)) if v else "-"}')
P(md_table(['Smokes', 'n', 'Top 6', 'Cap ours / neutral / theirs at start', 'Enemy took the cap during the smoke (of not theirs, with a later snapshot)', 'Enemy took it when ours', 'We took it (of not ours)', 'Batch "cap defended" on this cap', 'Concealed dmg', 'Deaths'], trs))
rb = sets[2][1]
P(' radar at B list:')
for s in sorted(rb, key=lambda s: (s['grp'] != 'top', s['game'], s['el'])):
    P(f'    {s["slug"]} {s["team"]} {s["ship"]} {clock(s["el"])} {s["ncell_name"]} own {s["near_own"]} enemy_took {s["enemy_took"]} we_took {s["we_took"]} cap_def {s["r"]["cap_defended"] or "-"} pp {s["pp"]} off_radar {bool(s["off_radar"])} spotted {s["off_radar"]["enemies_spotted"] if s["off_radar"] else "-"} edge {s["near_cap_edge_m"]:.0f} conc {s["conc"]:.0f}')
g_rb = gap([s for s in ms if radar(s)], lambda s: s['zone'] == 'B'); P(' share of the map\'s radar smokes that sit at B:', gtxt(g_rb))
g_all = gap(ms, lambda s: radar(s) and s['zone'] == 'B'); P(' share of all the group smokes on the map that are radar smokes at B:', gtxt(g_all), '->', g_all['mark'])
g_rate = gap([s for s in ms if s['zone'] == 'B'], radar); P(' share of smokes at B that are radar smokes:', gtxt(g_rate))
fo = lambda v: pct(v, lambda s: s['near_own'] == 'ours')
P(' B ours at start: radar smokes', fo(rb), boot_stat(rb, fo), '| other smokes at B', fo(sets[3][1]), boot_stat(sets[3][1], fo))
R['MR-2'] = dict(cap_table=ct, sets=mr2, share_of_map_radar_at_B=g_rb, share_of_all_smokes=g_all, share_of_B_smokes_that_are_radar=g_rate, smokes=[dict(link=s['link'], team=s['team'], ship=s['ship'], time=clock(s['el']), own=s['near_own'], enemy_took=s['enemy_took'], we_took=s['we_took']) for s in rb])
cb = next(c for c in map_caps(G, m) if c['cap'] == 'B'); u, v_ = uv(m, cb['x'], cb['z'])
SPOTS.append(dict(id='c5-mr-radar-b', **spot_record(m, 'shared_spot' if not g_all['clear'] else 'top6_spot', 'shared' if not g_all['clear'] else 'top6', 'Radar from smoke at centre cap B', S, rb,
             dict(type='circle', u=round(u, 4), v=round(v_, 4), r=round((cb['r'] + max(0, q([s['near_cap_edge_m'] for s in rb], .8)) / WU) / 1600, 4)),
             dict(subject='smokes with radar run from inside or a radar purpose, nearest cap B', share_top6_pct=g_all['top_pct'], share_rest_pct=g_all['rest_pct'], gap_pts=g_all['gap'], ci_pts=[g_all['lo'], g_all['hi']],
                  note='Share = share of all of each group smokes on the map that are radar smokes with B as nearest cap. 7 of the 15 are inside or within 2 km of B.'))))

# ---------------- Land of Fire
m = 'Land of Fire'; ms = on(m); dd = on(m, DD)
P('\n=== LF-1 early cluster at cap A: ship breakdown')
ra = atlas_spot('lof-early-f3'); early = [s for s in dd if s['el'] < 300]; mem = ms_cluster(early, 'F3'); P(' ellipse membership instead:', sum(in_r4(ra, s) for s in early))
g = gap(early, lambda s: s in mem); P(' cluster (atlas mean-shift membership)', len(mem), 'of', len(early), gtxt(g), '->', g['mark']); P('  ', clan_counts(mem))
for gname in ('top', 'rest'):
    w = [s for s in mem if s['grp'] == gname]
    P(f'  {gname}: n {len(w)} | smoker {cc(C(s["ship"] for s in w))} | cruisers inside {cc(cruiser_counts(w, "inside"))} | screened {cc(cruiser_counts(w, "screened"))} | early_mode {cc(C(str(s["early_mode"]) for s in w))} | radar cruiser inside {sum(s["radar_ca_inside"] for s in w)} | other partners {cc(C(p["ship"] for s in w for p in s["partners"] if p["cls"] != "cruiser"))} | conc {kf(mean(s["conc"] for s in w))} | deaths {sum(s["deaths"] for s in w)}')
for s in sorted(mem, key=lambda s: (s['grp'] != 'top', s['game'], s['el'])): P(f'      {s["slug"]} {s["team"]} {s["ship"]} {clock(s["el"])} {s["ncell_name"]} zone {s["zone"]} cr {[(c["ship"], c["how"]) for c in s["cruisers"]]} 2nd DD {[(d["ship"], d["cell"]) for d in second_dds(s)]} conc {s["conc"]:.0f}')
zA = [s for s in early if s['zone'] == 'A']; P(' all early destroyer smokes nearest cap A:', len(zA), gtxt(gap(early, lambda s: s['zone'] == 'A')), '| ships', cc(C(s['ship'] for s in zA)), '| cruisers inside', cc(cruiser_counts(zA, 'inside')), '| screened', cc(cruiser_counts(zA, 'screened')), '|', clan_counts(zA))
P(' standing definition, early cruiser smokes nearest A: inside', sum(s['early_mode'] == 'inside' for s in zA), 'screened', sum(s['early_mode'] == 'screened' for s in zA), 'no cruiser', sum(not s['early_cruiser'] for s in zA))
R['LF-1'] = dict(cluster=g, n=len(mem), clans=clan_dict(mem), smoker_ships=dict(top6=dict(C(s['ship'] for s in mem if s['grp'] == 'top')), rest=dict(C(s['ship'] for s in mem if s['grp'] == 'rest'))),
                 cruisers_inside=dict(top6=dict(cruiser_counts([s for s in mem if s['grp'] == 'top'], 'inside')), rest=dict(cruiser_counts([s for s in mem if s['grp'] == 'rest'], 'inside'))),
                 cruisers_screened=dict(top6=dict(cruiser_counts([s for s in mem if s['grp'] == 'top'], 'screened')), rest=dict(cruiser_counts([s for s in mem if s['grp'] == 'rest'], 'screened'))),
                 zone_A_early=dict(n=len(zA), ships=dict(C(s['ship'] for s in zA)), clans=clan_dict(zA)))
SPOTS.append(dict(id='c5-lf-early-a', **spot_record(m, 'early_cruiser_spot', 'shared', 'Opening smoke short of cap A (F3)', S, mem, ell_shape(ra),
             dict(subject='destroyer smokes in the first 5 minutes', share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']],
                  inside_n=sum(s['early_mode'] == 'inside' for s in mem), screened_n=sum(s['early_mode'] == 'screened' for s in mem)))))

P('\n=== LF-2 Svea F5')
rs = r4_spot('lof-svea-f5'); sv = [s for s in ms if s['ship'] == 'Svea']; mem = [s for s in sv if in_r4(rs, s)]
g = gap(sv, lambda s: in_r4(rs, s)); spotline('spot', sv, mem, g)
P(f'   members conc top {kf(mean(s["conc"] for s in mem if s["grp"] == "top"))} rest (n {sum(s["grp"] == "rest" for s in mem)}) | deaths {sum(s["deaths"] for s in mem)} | median time {clock(med(s["el"] for s in mem))} | games {len(set(s["game"] for s in mem))} | own {cc(C(s["near_own"] for s in mem))} | radar inside {sum(bool(s["off_radar"]) for s in mem)}')
for t in sorted(set(s['team'] for s in sv if s['grp'] == 'top')):
    w = [s for s in sv if s['grp'] == 'top' and s['team'] != t]; P(f'     Top 6 without {t}: {sum(in_r4(rs, s) for s in w)} of {len(w)}')
P('   Svea lineups on the map by clan', cc(C(p['team'] for g_ in games_on(m) for p in g_['roster'].values() if p['ship'] == 'Svea'), 14))
R['LF-2'] = dict(spot=g, clans=clan_dict(mem))
SPOTS.append(dict(id='c5-lf-svea-f5', **spot_record(m, 'top6_spot', 'top6', 'Svea parked on the own-side rim of cap B (F5)', S, mem, ell_shape(rs),
             dict(subject='Svea', share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']]))))

# ---------------- Sea of Fortune
m = 'Sea of Fortune'; ms = on(m); dd = on(m, DD)
P('\n=== SF-1 early cruiser smoke at the west cap and at D')
P(' caps (real map coordinates, world units; +z is north):', [(c['cap'], c['x'], c['z'], c['r']) for c in map_caps(G, m)])
P(' caps in the 0-1 frame:', [(c['cap'], [round(x, 3) for x in uv(m, c['x'], c['z'])], round(c['r'] / 1600, 3)) for c in map_caps(G, m)])
early = [s for s in dd if s['el'] < 300]; ec = [s for s in early if s['early_cruiser']]
rw = atlas_spot('sof-early-f2'); re_ = atlas_spot('sof-early-f9')
W = ms_cluster(early, 'F2'); E = ms_cluster(early, 'F9')
P(' early destroyer smokes', len(early), '| early cruiser smokes (standing definition)', len(ec), '| atlas west cluster', len(W), '| atlas east cluster', len(E))
P(' west cluster centre uv', rw['centre_uv'], 'cells', cc(C(s['ncell_name'] for s in W)))
P(' west cluster: nearest cap as drawn (normalized)', cc(C(s['zone'] for s in W)), '| real letter in the game', cc(C(s['near_cap'] for s in W)), '| spawn side', cc(C(s['side'] for s in W)), '| inside the cap circle', sum(s['near_cap_edge_m'] < 0 for s in W), '| median distance to B edge m', med(s['near_cap_edge_m'] for s in W))
cb = next(c for c in map_caps(G, m) if c['cap'] == 'B'); ca = next(c for c in map_caps(G, m) if c['cap'] == 'A')
P(' west cluster distance to drawn cap A edge (m): median', med((math.hypot(s['nx'] - ca['x'], s['nz'] - ca['z']) - ca['r']) * WU for s in W), '| to drawn cap B edge', med((math.hypot(s['nx'] - cb['x'], s['nz'] - cb['z']) - cb['r']) * WU for s in W))
sf1 = {}
for nm, zs in (('west own-side cap (drawn B)', ('B',)), ('west far cap (drawn A)', ('A',)), ('centre cap C', ('C',)), ('east cap D', ('D',))):
    v = [s for s in ec if s['zone'] in zs]; allv = [s for s in early if s['zone'] in zs]
    g = gap(ec, lambda s: s['zone'] in zs); gi = gap(v, lambda s: s['early_mode'] == 'inside')
    sf1[nm] = dict(n=len(v), early_dd_smokes_here=len(allv), share=g, inside=sum(s['early_mode'] == 'inside' for s in v), screened=sum(s['early_mode'] == 'screened' for s in v), clans=clan_dict(v), smoker_ships=dict(C(s['ship'] for s in v)),
                   cruisers_inside=dict(top6=dict(cruiser_counts([s for s in v if s['grp'] == 'top'], 'inside')), rest=dict(cruiser_counts([s for s in v if s['grp'] == 'rest'], 'inside'))),
                   cruisers_screened=dict(top6=dict(cruiser_counts([s for s in v if s['grp'] == 'top'], 'screened')), rest=dict(cruiser_counts([s for s in v if s['grp'] == 'rest'], 'screened'))),
                   radar_cruiser_inside=gap(v, lambda s: s['radar_ca_inside']), conc=round(mean(s['conc'] for s in v)) if v else None, deaths=sum(s['deaths'] for s in v))
    P(f' {nm}: early cruiser smokes {len(v)} (of {len(allv)} early destroyer smokes there) | share of group\'s early cruiser smokes: {gtxt(g)} | inside {sf1[nm]["inside"]} screened {sf1[nm]["screened"]} | inside by group {gtxt(gi)}')
    P(f'     smoker {cc(C(s["ship"] for s in v))} | cruisers inside: top {cc(cruiser_counts([s for s in v if s["grp"] == "top"], "inside"))}; rest {cc(cruiser_counts([s for s in v if s["grp"] == "rest"], "inside"))} | screened: top {cc(cruiser_counts([s for s in v if s["grp"] == "top"], "screened"))}; rest {cc(cruiser_counts([s for s in v if s["grp"] == "rest"], "screened"))} | radar cruiser inside {gtxt(sf1[nm]["radar_cruiser_inside"])}')
    P(f'     {clan_counts(v)} | cells {cc(C(s["ncell_name"] for s in v), 6)} | conc {kf(mean(s["conc"] for s in v)) if v else "-"} | deaths {sum(s["deaths"] for s in v)} | real letters {cc(C(s["near_cap"] for s in v))}')
for s in sorted([s for s in ec if s['zone'] in 'BD'], key=lambda s: (s['zone'], s['grp'] != 'top')): P(f'      {s["zone"]} {s["slug"]} {s["team"]} {s["ship"]} {clock(s["el"])} {s["ncell_name"]} {s["early_mode"]} {[(c["ship"], c["how"]) for c in s["cruisers"]]} conc {s["conc"]:.0f} edge {s["near_cap_edge_m"]:.0f}')
R['SF-1'] = dict(caps_uv={c['cap']: dict(u=round(uv(m, c['x'], c['z'])[0], 4), v=round(uv(m, c['x'], c['z'])[1], 4), r=round(c['r'] / 1600, 4)) for c in map_caps(G, m)}, by_cap=sf1,
                 west_cluster=dict(n=len(W), drawn_cap=dict(C(s['zone'] for s in W)), real_letter=dict(C(s['near_cap'] for s in W))))
for sid, nm, z, kind in (('c5-sf-early-west-b', 'Early cruiser smoke at the own-side west cap (drawn B)', 'B', 'early_cruiser_spot'), ('c5-sf-early-d', 'Early cruiser smoke short of east cap D', 'D', 'early_cruiser_spot')):
    v = [s for s in ec if s['zone'] == z]; c = next(c for c in map_caps(G, m) if c['cap'] == z); g = sf1[[k for k in sf1 if f'{z})' in k or k.endswith(z)][0]]['share']
    SPOTS.append(dict(id=sid, **spot_record(m, kind, 'top6' if g['mark'] == 'Top 6' else 'shared', nm, S, v, dict(type='circle', u=round(uv(m, c['x'], c['z'])[0], 4), v=round(uv(m, c['x'], c['z'])[1], 4), r=round((c['r'] + max(0, q([s['near_cap_edge_m'] for s in v], .8)) / WU) / 1600, 4)),
                 dict(subject='destroyer smokes in the first 5 minutes covering a cruiser', share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']],
                      inside_n=sum(s['early_mode'] == 'inside' for s in v), screened_n=sum(s['early_mode'] == 'screened' for s in v)))))

P('\n=== SF-2 long smokes at D, whole game')
lng = [s for s in dd if s['ship'] in LONG_SHIPS]; sf2 = {}
for z in ('A', 'B', 'C', 'D'):
    g = gap(lng, lambda s: s['zone'] == z); v = [s for s in lng if s['zone'] == z]; sf2[z] = dict(g, clans=clan_dict(v), conc=round(mean(s['conc'] for s in v)) if v else None)
    P(f' long smokes at {z}: {gtxt(g)} -> {g["mark"]} | n {len(v)} | conc {kf(mean(s["conc"] for s in v)) if v else "-"} (top {kf(mean(s["conc"] for s in v if s["grp"] == "top"))}, rest {kf(mean(s["conc"] for s in v if s["grp"] == "rest"))}) | deaths/100 {rate100(v, "deaths") if v else "-"} | ships {cc(C(s["ship"] for s in v))} | {clan_counts(v)}')
D = [s for s in lng if s['zone'] == 'D']
P(' at D by time: early', gtxt(gap([s for s in lng if s['el'] < 300], lambda s: s['zone'] == 'D')), '| later', gtxt(gap([s for s in lng if s['el'] >= 300], lambda s: s['zone'] == 'D')))
P(' at D: cruisers inside top', cc(cruiser_counts([s for s in D if s['grp'] == 'top'], 'inside')), '| rest', cc(cruiser_counts([s for s in D if s['grp'] == 'rest'], 'inside')), '| cells', cc(C(s['ncell_name'] for s in D)), '| own', cc(C(s['near_own'] for s in D)), '| median edge m', med(s['near_cap_edge_m'] for s in D))
P(' long smokes on the map', clan_counts(lng)); P(' all destroyer smokes at D', gtxt(gap(dd, lambda s: s['zone'] == 'D')))
for t, w in sorted(by(lng, 'team').items(), key=lambda x: (grp_of(x[0]) != 'top', -len(x[1]))): P(f'     {t} ({grp_of(t)}): {sum(s["zone"] == "D" for s in w)} of {len(w)} at D')
R['SF-2'] = sf2
c = next(c for c in map_caps(G, m) if c['cap'] == 'D'); g = sf2['D']
SPOTS.append(dict(id='c5-sf-long-d', **spot_record(m, 'top6_spot' if g['mark'] == 'Top 6' else 'shared_spot', 'top6' if g['mark'] == 'Top 6' else 'shared', 'Long smokes at east cap D', S, D,
             dict(type='circle', u=round(uv(m, c['x'], c['z'])[0], 4), v=round(uv(m, c['x'], c['z'])[1], 4), r=round((c['r'] + max(0, q([s['near_cap_edge_m'] for s in D], .8)) / WU) / 1600, 4)),
             dict(subject='long smokes (Somers, Gearing, Harugumo, Delny) nearest cap D', share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']]))))

P('\n=== SF-3 Svea spot')
rs = r4_spot('sof-svea-h7'); sv = [s for s in ms if s['ship'] == 'Svea']; mem = [s for s in sv if in_r4(rs, s)]
g = gap(sv, lambda s: in_r4(rs, s)); spotline('spot', sv, mem, g)
for t in sorted(set(s['team'] for s in sv if s['grp'] == 'top')):
    w = [s for s in sv if s['grp'] == 'top' and s['team'] != t]; P(f'     Top 6 without {t}: {sum(in_r4(rs, s) for s in w)} of {len(w)}')
P(f'   members conc {kf(mean(s["conc"] for s in mem))} | deaths {sum(s["deaths"] for s in mem)} | median time {clock(med(s["el"] for s in mem))} | games {len(set(s["game"] for s in mem))} | zone {cc(C(s["zone"] for s in mem))} | rest svea zones {cc(C(s["zone"] for s in sv if s["grp"] == "rest"))} cells {cc(C(s["ncell_name"] for s in sv if s["grp"] == "rest"))}')
P('   Svea lineups on the map by clan', cc(C(p['team'] for g_ in games_on(m) for p in g_['roster'].values() if p['ship'] == 'Svea'), 14))
R['SF-3'] = dict(spot=g, clans=clan_dict(mem))
SPOTS.append(dict(id='c5-sf-svea-h7', **spot_record(m, 'top6_spot', 'top6', 'Svea parked in open water on the own side of cap D (H7/G7)', S, mem, ell_shape(rs),
             dict(subject='Svea', share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']]))))

# ---------------- Okinawa
m = 'Okinawa'; ms = on(m); dd = on(m, DD)
P('\n=== OK-1 top smoke ships')
tg = tgames(m); ok1 = []
def lineups(sh):
    tgs = {(g_['key'], p['team']) for g_ in games_on(m) for p in g_['roster'].values() if p['ship'].replace('\xa0', ' ') == sh}
    slots = sum(1 for g_ in games_on(m) for p in g_['roster'].values() if p['ship'].replace('\xa0', ' ') == sh)
    return tgs, slots
for sh, n in C(s['ship'] for s in ms).most_common(10):
    v = [s for s in ms if s['ship'] == sh]; tgs, slots = lineups(sh)
    acts = sum(p['smoke_activations'] or 0 for g_ in games_on(m) for p in g_['roster'].values() if p['ship'].replace('\xa0', ' ') == sh)
    d = dict(ship=sh, cls=v[0]['cls'], smokes=n, top6_smokes=sum(s['grp'] == 'top' for s in v), team_games_in_lineup=len(tgs), top6_team_games=sum(t in TOP for _, t in tgs), ship_slots=slots, smokes_per_team_game=round(n / len(tgs), 2), smokes_per_ship_slot=round(n / slots, 2),
             team_games_with_a_smoke=len({(s['game'], s['team']) for s in v}), conc=round(mean(s['conc'] for s in v)), deaths_per_100=round(rate100(v, 'deaths'), 1), clans=clan_dict(v), roster_smoke_activations=acts)
    ok1.append(d)
    P(f' {sh} ({d["cls"]}): {n} smokes (Top 6 {d["top6_smokes"]}) | in lineup in {len(tgs)} team-games (Top 6 {d["top6_team_games"]}), {slots} ship slots | {d["smokes_per_team_game"]} per team-game, {d["smokes_per_ship_slot"]} per ship | team-games with at least one smoke {d["team_games_with_a_smoke"]} | conc {kf(d["conc"])} | deaths/100 {d["deaths_per_100"]} | {clan_counts(v)}')
P(' team-games on Okinawa', len(tg), 'games', len(games_on(m)), '| smokes', len(ms), '| destroyer smokes', len(dd))
R['OK-1'] = dict(team_games=len(tg), ships=ok1)

P('\n=== OK-2 death zone')
rd = atlas_spot('oki-deaths-h4'); zone_all = [s for s in ms if in_r4(rd, s)]; dth = [s for s in zone_all if s['deaths'] > 0]
cl = ms_cluster([s for s in ms if s['deaths'] > 0], 'H4', 2.5)
P(' atlas death cluster (mean-shift 2.5 km on smokes with a death):', len(cl), 'smokes,', sum(s['deaths'] for s in cl), 'deaths, laid 50+ behind', sum(s['state'] == 'behind 50+' for s in cl), '| of them inside the drawn ellipse', sum(in_r4(rd, s) for s in cl), '|', clan_counts(cl))
P(' atlas numbers', rd['numbers'])
P(' ellipse centre', rd['centre_uv'], rd['ellipse_uv'], '| smokes inside', len(zone_all), '| with a death', len(dth), '| deaths', sum(s['deaths'] for s in zone_all), '| per 100', round(rate100(zone_all, 'deaths'), 1), boot_stat(zone_all, lambda v: rate100(v, 'deaths')))
P(' map: smokes', len(ms), 'deaths', sum(s['deaths'] for s in ms), 'per 100', round(rate100(ms, 'deaths'), 1), boot_stat(ms, lambda v: rate100(v, 'deaths')), '| destroyer smokes per 100', round(rate100(dd, 'deaths'), 1), 'n', len(dd))
out_ = [s for s in ms if not in_r4(rd, s)]
fz = lambda v: (rate100([s for s in v if in_r4(rd, s)], 'deaths') - rate100([s for s in v if not in_r4(rd, s)], 'deaths')) if any(in_r4(rd, s) for s in v) and any(not in_r4(rd, s) for s in v) else None
P(' zone minus rest of map, deaths per 100:', fz(ms), boot_stat(ms, fz), '| rest of map per 100', rate100(out_, 'deaths'))
b50 = lambda s: s['state'] == 'behind 50+'
P(' laid 50+ behind: zone', rtxt(zone_all, b50), '| map', rtxt(ms, b50), '| rest of map', rtxt(out_, b50), '| death smokes in zone', sum(b50(s) for s in dth), 'of', len(dth))
fb = lambda v: (pct([s for s in v if in_r4(rd, s)], b50) - pct([s for s in v if not in_r4(rd, s)], b50)) if any(in_r4(rd, s) for s in v) and any(not in_r4(rd, s) for s in v) else None
P(' zone minus rest of map, share 50+ behind:', fb(ms), boot_stat(ms, fb))
for st in ('behind 50+', 'level', 'ahead 50+'):
    a = [s for s in zone_all if s['state'] == st]; b = [s for s in out_ if s['state'] == st]
    P(f'   {st}: zone n {len(a)} deaths {sum(s["deaths"] for s in a)} per 100 {rate100(a, "deaths") if len(a) >= 8 else "too few"} | rest of map n {len(b)} deaths {sum(s["deaths"] for s in b)} per 100 {rate100(b, "deaths"):.0f}')
P(' zone: class', cc(C(s['cls'] for s in zone_all)), '| ships', cc(C(s['ship'] for s in zone_all)), '| who died', cc(C(d['cls'] + (' (smoker)' if d['is_smoker'] else '') for s in zone_all for d in s['dead'])), '| radar lit', sum(d['radar_lit'] for s in zone_all for d in s['dead']), '| games', len(set(s['game'] for s in zone_all)), '| lost game', sum(not s['win'] for s in zone_all))
P(' zone', clan_counts(zone_all)); P(' death smokes', clan_counts(dth)); P(' zone share of group smokes', gtxt(gap(ms, lambda s: in_r4(rd, s))), '| zone cells', cc(C(s['ncell_name'] for s in zone_all)), '| zone', cc(C(s['zone'] for s in zone_all)))
P(' destroyer smokes only in zone', len([s for s in zone_all if s['cls'] == 'destroyer']), 'deaths', sum(s['deaths'] for s in zone_all if s['cls'] == 'destroyer'), '| smoker died', sum(s['d_smoker'] for s in zone_all), '| cruisers died', sum(s['d_cr'] for s in zone_all))
P(' map by state:', {st: (len([s for s in ms if s['state'] == st]), round(rate100([s for s in ms if s['state'] == st], 'deaths'), 1)) for st in ('behind 50+', 'level', 'ahead 50+')})
P(' per-map deaths per 100 destroyer smokes:', {mm: (round(rate100(on(mm, DD), 'deaths'), 1), len(on(mm, DD))) for mm in MAPS}, '| all classes', {mm: round(rate100(on(mm), 'deaths'), 1) for mm in MAPS})
gz = gap(ms, lambda s: in_r4(rd, s))
R['OK-2'] = dict(zone_n=len(zone_all), death_smokes=len(dth), deaths=sum(s['deaths'] for s in zone_all), deaths_per_100=round(rate100(zone_all, 'deaths'), 1), map_deaths_per_100=round(rate100(ms, 'deaths'), 1),
                 behind_share_zone=round(pct(zone_all, b50), 1), behind_share_map=round(pct(ms, b50), 1), behind_share_rest_of_map=round(pct(out_, b50), 1), death_smokes_behind=sum(b50(s) for s in dth), clans=clan_dict(zone_all), use=gz)
SPOTS.append(dict(id='c5-ok-death-zone', **spot_record(m, 'danger_zone', 'shared', 'Death zone: south-west water on the own side of cap C', S, zone_all, ell_shape(rd),
             dict(subject='all smokes in the zone, all classes', share_top6_pct=gz['top_pct'], share_rest_pct=gz['rest_pct'], gap_pts=gz['gap'], ci_pts=[gz['lo'], gz['hi']], smokes_with_a_death=len(dth), deaths=sum(s['deaths'] for s in zone_all),
                  laid_50_behind_pct=round(pct(zone_all, b50), 1), map_laid_50_behind_pct=round(pct(ms, b50), 1), map_deaths_per_100=round(rate100(ms, 'deaths'), 1)))))
save_json('part-rest.json', dict(R=R, SPOTS=SPOTS))
