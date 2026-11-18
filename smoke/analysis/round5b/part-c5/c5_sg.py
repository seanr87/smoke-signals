import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c5lib import *
m = 'Sleeping Giant'; ms = on(m); R = {}
P('=== SG-1 Somers east / west')
som = [s for s in ms if s['ship'] == 'Somers']; esom = [s for s in som if s['el'] < 300]
g_w = gap(som, lambda s: s['nx'] < 0); g_e = gap(som, lambda s: s['nx'] > 0); g_we = gap(esom, lambda s: s['nx'] < 0); g_ee = gap(esom, lambda s: s['nx'] > 0)
late = [s for s in som if s['el'] >= 300]; g_wl = gap(late, lambda s: s['nx'] < 0)
P('all west', gtxt(g_w)); P('all east', gtxt(g_e)); P('early west', gtxt(g_we)); P('early east', gtxt(g_ee)); P('after 5:00 west', gtxt(g_wl))
east = [s for s in som if s['nx'] > 0]; west = [s for s in som if s['nx'] < 0]
P('east clans', clan_counts(east)); P('west clans', clan_counts(west))
P('somers clans all', clan_counts(som)); P('early clans east', clan_counts([s for s in esom if s['nx'] > 0]), '| early west', clan_counts([s for s in esom if s['nx'] < 0]))
for nm, v in (('east', east), ('west', west)):
    for gname in ('top', 'rest'):
        w = [s for s in v if s['grp'] == gname]
        P(f' {nm} {gname}: n {len(w)} conc {kf(mean(s["conc"] for s in w))} deaths/100 {rate100(w, "deaths")} cells {cc(C(s["ncell_name"] for s in w), 6)} zone {cc(C(s["zone"] for s in w))} cr inside {sum(s["cr_inside"] for s in w)} early {sum(s["el"] < 300 for s in w)}')
P(' east conc all', kf(mean(s['conc'] for s in east)), boot_stat(east, lambda v: mean(s['conc'] for s in v)), 'west', kf(mean(s['conc'] for s in west)), boot_stat(west, lambda v: mean(s['conc'] for s in v)), 'deaths east', rate100(east, 'deaths'), 'west', rate100(west, 'deaths'))
te = [s for s in east if s['grp'] == 'top']
us = [uv(m, s['nx'], s['nz']) for s in te]
P(' top6 east uv box', min(u for u, v in us), max(u for u, v in us), min(v for u, v in us), max(v for u, v in us), 'rows', cc(C(s['ncell_name'][0] for s in te)), 'cols', cc(C(s['ncell'][0] + 1 for s in te)))
for t, v in sorted(by(som, 'team').items()): P('  ', t, grp_of(t), len(v), 'west', sum(s['nx'] < 0 for s in v))
for t in sorted(set(s['team'] for s in som if s['grp'] == 'top')):
    w = [s for s in som if s['team'] != t and s['grp'] == 'top']; P('   top without', t, sum(s['nx'] < 0 for s in w), 'of', len(w))
for sh in ('Gearing', 'Harugumo'):
    v = [s for s in ms if s['ship'] == sh]; P(' context', sh, gtxt(gap(v, lambda s: s['nx'] < 0)))
shape = uvrect(m, 0, -700, 700, 700)
R['SG-1'] = dict(all_west=g_w, all_east=g_e, early_west=g_we, early_east=g_ee, after5_west=g_wl, east_clans=clan_dict(east), west_clans=clan_dict(west), east_rect_uv=shape,
                 east_conc=round(mean(s['conc'] for s in east)), west_conc=round(mean(s['conc'] for s in west)), east_deaths_per_100=round(rate100(east, 'deaths'), 1), west_deaths_per_100=round(rate100(west, 'deaths'), 1))
SPOTS.append(dict(id='c5-sg-somers-east', **spot_record(m, 'top6_spot', 'top6', 'Somers: east half of Sleeping Giant', S, east, shape,
             dict(subject='Somers', share_top6_pct=g_e['top_pct'], share_rest_pct=g_e['rest_pct'], gap_pts=g_e['gap'], ci_pts=[g_e['lo'], g_e['hi']],
                  note='East half = normalized x > 0 (u 0.5 to 1.0). Early (first 5 min) Somers smokes alone do not split: see C5-SG-1.'))))

P('\n=== SG-2 Harugumo G1/F1 second destroyer')
rec = r4_spot('sg-harugumo-g1'); har = [s for s in ms if s['ship'] == 'Harugumo']; mem = sorted([s for s in har if in_r4(rec, s)], key=lambda s: (s['grp'] != 'top', s['game'], s['el']))
g_h = gap(har, lambda s: in_r4(rec, s)); P('spot', gtxt(g_h), clan_counts(mem))
rows = []; alln = []
for s in mem:
    d2 = second_dds(s); alive = other_dds_alive(s); na = sum(c['ally'] for c in s['cast'])
    alln.append(na)
    rows.append(dict(link=s['link'], slug=s['slug'], team=s['team'], grp=s['grp'], time=clock(s['el']), cell=s['ncell_name'], allies_with_position=na, other_dds_alive=alive, second_dds=[{k: v for k, v in d.items() if k not in ('nx', 'nz')} for d in d2],
                     cruisers=[(c['ship'], c['how']) for c in s['cruisers']]))
    P(f" {s['slug']} {s['team']} {clock(s['el'])} {s['ncell_name']} allies pos {na} | cruisers {[(c['ship'], c['how']) for c in s['cruisers']]} | other DDs alive: {', '.join(alive) or 'none'} | recorded: " + ('; '.join(f"{d['ship']} {d['cell']} ({d['how']}), {d['dist_m']/1000:.1f} km from smoke, {d['fwd_m']/1000:+.1f} km fwd, cap {d['cap']} edge {d['cap_edge_m']/1000:+.1f} km" for d in d2) or 'NONE'))
top = [s for s in mem if s['grp'] == 'top']
pres = [s for s in top if second_dds(s)]
allp = [d for s in top for d in second_dds(s)]
P(' present', len(pres), 'of', len(top), '| ships', cc(C(d['ship'] for d in allp)), '| cells', cc(C(d['cell'] for d in allp)), '| caps', cc(C(d['cap'] for d in allp)), '| fwd>0', sum(d['fwd_m'] > 0 for d in allp), '| med dist', med(d['dist_m'] for d in allp), '| inside smoke', sum(d['how'] == 'inside' for d in allp),
  '| within 1.5km of cap A edge', sum(d['cap'] == 'A' and d['cap_edge_m'] <= 1500 for d in allp), '| median allies with position', med(alln))
P(' absent ones: other DD alive?', [(s['slug'], other_dds_alive(s)) for s in top if not second_dds(s)])
P(' all smokes median allied positions', med(sum(c['ally'] for c in s['cast']) for s in S), 'alive allies median', med(s['j']['state_at_capture']['alive_ours'] for s in S if s['j']['state_at_capture']))
P(' in this spot: alive_ours at capture', [s['j']['state_at_capture']['alive_ours'] if s['j']['state_at_capture'] else None for s in mem])
R['SG-2'] = dict(spot=g_h, clans=clan_dict(mem), smokes=rows, top6_with_second_dd=len(pres), top6_n=len(top), second_dd_ships=dict(C(d['ship'] for d in allp)), second_dd_cells=dict(C(d['cell'] for d in allp)),
                 forward_n=sum(d['fwd_m'] > 0 for d in allp), median_dist_m=med(d['dist_m'] for d in allp))
SPOTS.append(dict(id='c5-sg-harugumo-g1', **spot_record(m, 'top6_spot', 'top6', 'Harugumo: west edge below cap A (G1/F1)', S, mem, ell_shape(rec),
             dict(subject='Harugumo', share_top6_pct=g_h['top_pct'], share_rest_pct=g_h['rest_pct'], gap_pts=g_h['gap'], ci_pts=[g_h['lo'], g_h['hi']], second_dd_recorded=f'{len(pres)} of {len(top)} Top 6 smokes',
                  second_dd_positions_uv=[[round(x, 4) for x in uv(m, d['nx'], d['nz'])] + [d['ship']] for d in allp]))))

P('\n=== SG-3 smoke at cap B (inside or within 2 km of the cap edge)')
NEAR = 2000
ct = cap_table(m, edge=NEAR); P(cap_md(ct)); ct_all = cap_table(m)
near = [s for s in ms if s['near_cap_edge_m'] <= NEAR]
B = [s for s in near if s['zone'] == 'B']; Bfar = [s for s in ms if s['zone'] == 'B']
P(' smokes within 2 km of any cap', len(near), 'of', len(ms), '| nearest cap B at any distance', len(Bfar), '| within 2 km of B', len(B))
def contest(s): return any(c['cap'] == s['near_cap'] and (c['contested'] or c['both_inside']) for c in s['j']['state_at_activate']['cap_state'])
for nm, v in (('within 2 km of B', B), ('nearest cap B, any distance', Bfar)):
    P(f' {nm}: n {len(v)} | class {cc(C(s["cls"] for s in v))} | ships {cc(C(s["ship"] for s in v))} | habits {cc(C(s["habit"] for s in v))}')
    P(f'   primary purpose {cc(C(s["pp"] for s in v))} | all tags {cc(C(t for s in v for t in s["tags"]))}')
    P(f'   own at start: {cc(C(s["near_own"] for s in v))} | by group {cc(C((s["grp"], s["near_own"]) for s in v), 9)}')
    P(f'   inside the cap {sum(s["near_cap_edge_m"] < 0 for s in v)} | no cruiser covered {sum(not s["cr_any"] for s in v)} | radar play {sum(s["radar_play"] for s in v)} | median time {clock(med(s["el"] for s in v))} | early {sum(s["el"] < 300 for s in v)} | state {cc(C(s["state"] for s in v))}')
    P(f'   batch cap_defended on B {sum(s["r"]["cap_defended"] == s["near_cap"] for s in v)} | enemies near the cap during the smoke (cap_denial) {sum(1 for s in v if s["j"]["cap_denial"] and s["j"]["cap_denial"]["enemies_during"] > 0)} | conc {kf(mean(s["conc"] for s in v))} | deaths {sum(s["deaths"] for s in v)}')
    P('   ', clan_counts(v))
    o = [s for s in v if s['near_own'] == 'ours']
    P(f'   B ours at start: n {len(o)} | ships {cc(C(s["ship"] for s in o))} | pp {cc(C(s["pp"] for s in o))} | enemy took {sum(1 for s in o if s["enemy_took"])} of {sum(1 for s in o if s["enemy_took"] is not None)} | cap_defended(B) {sum(s["r"]["cap_defended"] == s["near_cap"] for s in o)} | enemy already contesting at start {sum(contest(s) for s in o)} | {clan_counts(o)}')
    nn = [s for s in v if s['near_own'] != 'ours']
    P(f'   B not ours at start: n {len(nn)} | we took {sum(1 for s in nn if s["we_took"])} of {sum(1 for s in nn if s["we_took"] is not None)} | pp {cc(C(s["pp"] for s in nn))}')
P(' enemy took B during:', [(s['slug'], s['team'], s['ship'], s['near_own']) for s in B if s['enemy_took']])
g_own = gap(B, lambda s: s['near_own'] == 'ours'); P(' B ours share', gtxt(g_own))
g_Bshare = gap(near, lambda s: s['zone'] == 'B'); P(' share of near-cap smokes that are at B', gtxt(g_Bshare)); g_Bmap = gap(ms, lambda s: s['zone'] == 'B' and s['near_cap_edge_m'] <= NEAR); P(' share of all map smokes', gtxt(g_Bmap))
other = [s for s in near if s['zone'] != 'B']
f_et = lambda v: pct([s for s in v if s['enemy_took'] is not None], lambda s: s['enemy_took'])
def fd(v):
    a = [s for s in v if s['zone'] == 'B' and s['enemy_took'] is not None]; b = [s for s in v if s['zone'] != 'B' and s['enemy_took'] is not None]
    return f_et(a) - f_et(b) if a and b else None
P(' enemy took: B', f_et(B), boot_stat(B, f_et), '| other caps', f_et(other), boot_stat(other, f_et), '| diff', fd(near), boot_stat(near, fd))
f_def = lambda v: pct(v, lambda s: s['r']['cap_defended'] == s['near_cap'])
P(' cap_defended(this cap): B', f_def(B), boot_stat(B, f_def), 'other', f_def(other), boot_stat(other, f_def))
f_o = lambda v: pct(v, lambda s: s['near_own'] == 'ours'); P(' ours at start: B', f_o(B), boot_stat(B, f_o), '| other caps', f_o(other), boot_stat(other, f_o))
sitn = [s for s in near if s['habit'] == 'cap sitters']; P(' sitters at B (of sitter smokes within 2 km of a cap)', gtxt(gap(sitn, lambda s: s['zone'] == 'B')))
R['SG-3'] = dict(rule='inside or within 2 km of the cap edge', cap_table=ct, cap_table_nearest_cap_any_distance=ct_all,
                 at_B=dict(n=len(B), ships=dict(C(s['ship'] for s in B)), habits=dict(C(s['habit'] for s in B)), primary_purpose=dict(C(s['pp'] for s in B)), own=dict(C(s['near_own'] for s in B)),
                 clans=clan_dict(B), share_of_near_cap_smokes=g_Bshare, share_of_map_smokes=g_Bmap, ours_share=g_own))
SPOTS.append(dict(id='c5-sg-cap-b', **spot_record(m, 'shared_spot', 'shared', 'Smoke at cap B (mostly cap sitters)', S, B, dict(type='circle', u=round(uv(m, -39, 0)[0], 4), v=round(uv(m, -39, 0)[1], 4), r=round((99 + NEAR / WU) / 1400, 4)),
             dict(subject='all smokes inside or within 2 km of cap B', share_top6_pct=g_Bmap['top_pct'], share_rest_pct=g_Bmap['rest_pct'], gap_pts=g_Bmap['gap'], ci_pts=[g_Bmap['lo'], g_Bmap['hi']],
                  note='Circle = cap B plus 2 km.'))))
save_json('part-sg.json', dict(R=R, SPOTS=SPOTS))
