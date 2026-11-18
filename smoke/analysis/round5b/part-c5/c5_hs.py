import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c5lib import *
m = 'Hotspot'; ms = on(m); dd = on(m, DD); R = {}
P('=== HS-1 west caps A + B')
tab = {}
for nm, pool in (('destroyer smokes', dd), ('all smokes', ms)):
    tab[nm] = {}
    for z in ('A', 'B', 'C', 'D', 'A+B'):
        g = gap(pool, lambda s: s['zone'] in z.split('+')); tab[nm][z] = g; P(f' {nm} {z}: {gtxt(g)}')
west = [s for s in dd if s['zone'] in 'AB']; A = [s for s in dd if s['zone'] == 'A']; B = [s for s in dd if s['zone'] == 'B']
P(' A+B clans (DD)', clan_counts(west)); P(' A clans', clan_counts(A)); P(' B clans', clan_counts(B))
P(' A+B clans (all classes)', clan_counts([s for s in ms if s['zone'] in 'AB']))
for t, v in sorted(by(dd, 'team').items(), key=lambda x: (grp_of(x[0]) != 'top', -len(x[1]))):
    P(f'   {t} ({grp_of(t)}): {sum(s["zone"] in "AB" for s in v)} of {len(v)} at A+B; games {len(set(s["game"] for s in v))}')
P(' top clans with any A+B smoke', len(set(s['team'] for s in west if s['grp'] == 'top')), 'of', len(set(s['team'] for s in dd if s['grp'] == 'top')), '| rest', len(set(s['team'] for s in west if s['grp'] == 'rest')), 'of', len(set(s['team'] for s in dd if s['grp'] == 'rest')))
for t in sorted(set(s['team'] for s in dd if s['grp'] == 'top')):
    w = [s for s in dd if s['team'] != t and s['grp'] == 'top']; P(f'   Top 6 without {t}: {sum(s["zone"] in "AB" for s in w)} of {len(w)} = {pct(w, lambda s: s["zone"] in "AB"):.0f}%')
for nm, v in (('A', A), ('B', B), ('A+B', west), ('C', [s for s in dd if s['zone'] == 'C']), ('D', [s for s in dd if s['zone'] == 'D'])):
    P(f'  {nm}: n {len(v)} conc {kf(mean(s["conc"] for s in v))} ci {boot_stat(v, lambda w: mean(s["conc"] for s in w))} deaths/100 {rate100(v, "deaths"):.0f} ships {cc(C(s["ship"] for s in v), 6)} early {sum(s["el"] < 300 for s in v)} med time {clock(med(s["el"] for s in v))} we_took {sum(1 for s in v if s["we_took"])}/{sum(1 for s in v if s["we_took"] is not None)} edge q80 {q([s["near_cap_edge_m"] for s in v], .8):.0f} max {max(s["near_cap_edge_m"] for s in v):.0f}')
    for gname in ('top', 'rest'):
        w = [s for s in v if s['grp'] == gname]; P(f'     {gname}: n {len(w)} conc {kf(mean(s["conc"] for s in w))} ships {cc(C(s["ship"] for s in w), 6)}')
P(' west share by time: early', gtxt(gap([s for s in dd if s['el'] < 300], lambda s: s['zone'] in 'AB')), '| later', gtxt(gap([s for s in dd if s['el'] >= 300], lambda s: s['zone'] in 'AB')))
# team-game level: share of team-games with at least one destroyer smoke at A or B
tg = tgames(m); has = {(k, t) for k, t in tg if any(s['game'] == k and s['team'] == t and s['zone'] in 'AB' for s in dd)}
P(' team-games with a DD smoke at A or B: Top 6', sum(1 for k, t in has if t in TOP), 'of', sum(1 for k, t in tg if t in TOP), '| Rest', sum(1 for k, t in has if t not in TOP), 'of', sum(1 for k, t in tg if t not in TOP))
g2k = gap(dd, lambda s: s['zone'] in 'AB' and s['near_cap_edge_m'] <= 2000); n2k = [s for s in dd if s['zone'] in 'AB' and s['near_cap_edge_m'] <= 2000]
P(' stricter rule, inside or within 2 km of A or B:', gtxt(g2k), '|', clan_counts(n2k), '| median distance of the 50 west smokes from the cap edge', med(s['near_cap_edge_m'] for s in west))
R['HS-1'] = dict(within_2km=g2k, shares=tab, clans_AB_destroyer=clan_dict(west), clans_A=clan_dict(A), clans_B=clan_dict(B),
                 team_games_with_west_smoke=dict(top6=[sum(1 for k, t in has if t in TOP), sum(1 for k, t in tg if t in TOP)], rest=[sum(1 for k, t in has if t not in TOP), sum(1 for k, t in tg if t not in TOP)]))
caps = {c['cap']: c for c in map_caps(G, m)}
for z, v in (('A', A), ('B', B)):
    c = caps[z]; g = tab['destroyer smokes'][z]; u, v_ = uv(m, c['x'], c['z'])
    SPOTS.append(dict(id=f'c5-hs-cap-{z.lower()}', **spot_record(m, 'top6_spot', 'top6', f'Destroyer smoke at west cap {z}', S, v, dict(type='circle', u=round(u, 4), v=round(v_, 4), r=round((c['r'] + max(0, q([s['near_cap_edge_m'] for s in v], .8)) / WU) / 1600, 4)),
                 dict(subject='destroyer smokes whose nearest cap is ' + z, share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']],
                      note='Circle = the cap plus the distance that holds 80% of the member smokes. A and B together: Top 6 36% vs Rest 14%.'))))

P('\n=== HS-2 opener at G10')
early = [s for s in dd if s['el'] < 300]
rec = atlas_spot('hs-early-g10'); g10 = ms_cluster(early, 'G10'); rec5 = atlas_spot('hs-early-g5'); g5 = ms_cluster(early, 'G5')
P(' ellipse membership instead of cluster membership: G10', sum(in_r4(rec, s) for s in early), 'G5', sum(in_r4(rec5, s) for s in early))
P(' early DD smokes', len(early), '| in G10 cluster', len(g10), '| in G5 cluster', len(g5))
g_all = gap(early, lambda s: s['radar_ca_inside']); g_g10 = gap(g10, lambda s: s['radar_ca_inside']); g_g5 = gap(g5, lambda s: s['radar_ca_inside'])
P(' map-wide radar cruiser inside:', gtxt(g_all)); P(' G10 cluster:', gtxt(g_g10)); P(' G5 cluster:', gtxt(g_g5))
g_use = gap(early, lambda s: s in g10); P(' share of early smokes in G10:', gtxt(g_use))
P(' G10 clans', clan_counts(g10)); P(' G10 ships', cc(C(s['ship'] for s in g10)), '| cruisers inside top', cc(cruiser_counts([s for s in g10 if s['grp'] == 'top'], 'inside')), '| rest', cc(cruiser_counts([s for s in g10 if s['grp'] == 'rest'], 'inside')),
  '| screened top', cc(cruiser_counts([s for s in g10 if s['grp'] == 'top'], 'screened')), '| rest', cc(cruiser_counts([s for s in g10 if s['grp'] == 'rest'], 'screened')))
P(' G10 Rest without a radar cruiser inside: cover3', cc(C(s['cover3'] for s in g10 if s['grp'] == 'rest' and not s['radar_ca_inside'])), '| clans', clan_counts([s for s in g10 if not s['radar_ca_inside']]))
P(' G10 radar cruiser inside by clan:', ', '.join(f'{t} {sum(s["radar_ca_inside"] for s in v)}/{len(v)}' for t, v in sorted(by(g10, 'team').items(), key=lambda x: (grp_of(x[0]) != 'top', -len(x[1])))))
P(' G10 conc', kf(mean(s['conc'] for s in g10)), 'top', kf(mean(s['conc'] for s in g10 if s['grp'] == 'top')), 'rest', kf(mean(s['conc'] for s in g10 if s['grp'] == 'rest')), 'deaths/100', rate100(g10, 'deaths'))
# standing definition: early cruiser smoke, inside and screened separately
P(' standing definition (early smoke covering a cruiser), Hotspot: inside', gtxt(gap(early, lambda s: s['early_mode'] == 'inside')), '| screened', gtxt(gap(early, lambda s: s['early_mode'] == 'screened')), '| none', gtxt(gap(early, lambda s: not s['early_cruiser'])))
P(' in G10: inside', gtxt(gap(g10, lambda s: s['early_mode'] == 'inside')), '| screened', gtxt(gap(g10, lambda s: s['early_mode'] == 'screened')))
permap = {}
for mm in MAPS:
    e = [s for s in on(mm, DD) if s['el'] < 300]; g = gap(e, lambda s: s['radar_ca_inside']); permap[mm] = g; P(f'   {mm}: {gtxt(g)}')
R['HS-2'] = dict(early_n=len(early), g10_n=len(g10), map_wide=g_all, g10=g_g10, g5=g_g5, g10_use=g_use, per_map=permap, g10_clans=clan_dict(g10),
                 g10_cruisers_inside=dict(top6=dict(cruiser_counts([s for s in g10 if s['grp'] == 'top'], 'inside')), rest=dict(cruiser_counts([s for s in g10 if s['grp'] == 'rest'], 'inside'))))
SPOTS.append(dict(id='c5-hs-opener-g10', **spot_record(m, 'early_cruiser_spot', 'shared', 'Opening smoke short of cap D on the east edge (G10)', S, g10, ell_shape(rec),
             dict(subject='destroyer smokes in the first 5 minutes', share_top6_pct=g_use['top_pct'], share_rest_pct=g_use['rest_pct'], gap_pts=g_use['gap'], ci_pts=[g_use['lo'], g_use['hi']],
                  radar_cruiser_inside=dict(top6=[g_g10['top_k'], g_g10['top_n']], rest=[g_g10['rest_k'], g_g10['rest_n']], gap_pts=g_g10['gap'], ci_pts=[g_g10['lo'], g_g10['hi']]),
                  note='Shared place; what differs is the radar cruiser inside the smoke.'))))

P('\n=== HS-3 rim of C lead')
rc = r4_spot('hs-flank-g6'); fl = [s for s in dd if s['habit'] == 'flank smoke lines']; mem = [s for s in fl if in_r4(rc, s)]
g_c = gap(fl, lambda s: in_r4(rc, s)); P(' spot', gtxt(g_c), clan_counts(mem))
for gname in ('top', 'rest'):
    w = [s for s in mem if s['grp'] == gname]
    P(f'  {gname}: n {len(w)} | smoker {cc(C(s["ship"] for s in w))} | cruisers inside {cc(cruiser_counts(w, "inside"))} | screened {cc(cruiser_counts(w, "screened"))} | smokes with a cruiser inside {sum(s["cr_inside"] for s in w)} | radar cruiser inside {sum(s["radar_ca_inside"] for s in w)} | no cruiser {sum(not s["cr_any"] for s in w)} | conc {kf(mean(s["conc"] for s in w))} | deaths {sum(s["deaths"] for s in w)} | early {sum(s["el"] < 300 for s in w)} | med time {clock(med(s["el"] for s in w))}')
    for s in w: P(f'      {s["slug"]} {s["team"]} {s["ship"]} {clock(s["el"])} {s["ncell_name"]} {[(c["ship"], c["how"]) for c in s["cruisers"]]} conc {s["conc"]:.0f}')
P(' without RESIN: top', sum(1 for s in mem if s['grp'] == 'top' and s['team'] != 'RESIN'), 'of', sum(1 for s in fl if s['grp'] == 'top' and s['team'] != 'RESIN'))
P(' cruisers fielded on Hotspot (roster, team-games): top', cc(C(p['ship'].replace('\xa0', ' ') for g in games_on(m) for p in g['roster'].values() if p['team'] in TOP and p['ship_class'] == 'Cruiser')), '| rest', cc(C(p['ship'].replace('\xa0', ' ') for g in games_on(m) for p in g['roster'].values() if p['team'] not in TOP and p['ship_class'] == 'Cruiser'), 10))
anyc = [s for s in dd if in_r4(rc, s)]; P(' all destroyer smokes in the ellipse', gtxt(gap(dd, lambda s: in_r4(rc, s))), '| cruisers inside top', cc(cruiser_counts([s for s in anyc if s['grp'] == 'top'], 'inside')), '| rest', cc(cruiser_counts([s for s in anyc if s['grp'] == 'rest'], 'inside')))
R['HS-3'] = dict(spot=g_c, clans=clan_dict(mem), cruisers_inside=dict(top6=dict(cruiser_counts([s for s in mem if s['grp'] == 'top'], 'inside')), rest=dict(cruiser_counts([s for s in mem if s['grp'] == 'rest'], 'inside'))),
                 cruisers_screened=dict(top6=dict(cruiser_counts([s for s in mem if s['grp'] == 'top'], 'screened')), rest=dict(cruiser_counts([s for s in mem if s['grp'] == 'rest'], 'screened'))),
                 smokes=[dict(link=s['link'], team=s['team'], ship=s['ship'], time=clock(s['el']), cell=s['ncell_name'], cruisers=[(c['ship'], c['how']) for c in s['cruisers']]) for s in mem])
SPOTS.append(dict(id='c5-hs-rim-c', **spot_record(m, 'shared_spot', 'shared', 'Long smokes on the own-side rim of cap C (G6/F6)', S, mem, ell_shape(rc),
             dict(subject='flank smoke lines (Somers, Gearing, Harugumo, Delny)', share_top6_pct=g_c['top_pct'], share_rest_pct=g_c['rest_pct'], gap_pts=g_c['gap'], ci_pts=[g_c['lo'], g_c['hi']]))))
save_json('part-hs.json', dict(R=R, SPOTS=SPOTS))
