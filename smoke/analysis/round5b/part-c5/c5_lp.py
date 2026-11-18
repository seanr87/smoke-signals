import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c5lib import *
m = 'Loop'; ms = on(m); dd = on(m, DD); R = {}
MAPL = sorted(MAPS, key=lambda x: -len(on(x)))

P('=== LP-1 early smoke rate per team-game, by map')
def tg_rows(mm):
    out = []
    for k, t in tgames(mm):
        v = [s for s in S if s['game'] == k and s['team'] == t and s['el'] < 300]
        out.append(dict(team=t, grp=grp_of(t), game=k, dd=sum(s['cls'] == 'destroyer' for s in v), ecr=sum(bool(s['early_cruiser']) for s in v), ins=sum(s['early_mode'] == 'inside' for s in v),
                        scr=sum(s['early_mode'] == 'screened' for s in v), ca=sum(s['cls'] == 'cruiser' for s in v), allc=len(v)))
    return out
lp1 = {}
def rt(rows, key): return mean(r[key] for r in rows)
hdr = ['Map', 'Team-games (Top 6 / Rest)', 'Early destroyer smokes per team-game: all', 'Top 6', 'Rest', 'Gap (interval)', 'Early cruiser smokes per team-game (destroyer smoke covering a cruiser): all', 'Top 6', 'Rest', 'Gap (interval)', 'of which cruiser inside', 'cruiser screened', 'Early smokes laid by cruisers per team-game']
trs = []
for mm in MAPL:
    rows = tg_rows(mm); t = [r for r in rows if r['grp'] == 'top']; r_ = [r for r in rows if r['grp'] == 'rest']
    d = dict(team_games=len(rows), top_tg=len(t), rest_tg=len(r_))
    for key in ('dd', 'ecr', 'ins', 'scr', 'ca', 'allc'):
        lo, hi = boot_diff(rows, lambda v, key=key: rt(v, key)); alo, ahi = boot_stat(rows, lambda v, key=key: rt(v, key))
        d[key] = dict(all=round(rt(rows, key), 2), all_ci=[round(alo, 2), round(ahi, 2)], top=round(rt(t, key), 2), rest=round(rt(r_, key), 2), gap=round(rt(t, key) - rt(r_, key), 2), lo=round(lo, 2), hi=round(hi, 2), clear=lo * hi > 0)
    lp1[mm] = d
    gi = lambda k: f"{d[k]['gap']:+.2f} ({d[k]['lo']:+.2f} to {d[k]['hi']:+.2f}{' *' if d[k]['clear'] else ''})"
    trs.append([mm, f"{len(rows)} ({len(t)} / {len(r_)})", f"{d['dd']['all']:.2f} ({d['dd']['all_ci'][0]:.2f} to {d['dd']['all_ci'][1]:.2f})", d['dd']['top'], d['dd']['rest'], gi('dd'),
                f"{d['ecr']['all']:.2f} ({d['ecr']['all_ci'][0]:.2f} to {d['ecr']['all_ci'][1]:.2f})", d['ecr']['top'], d['ecr']['rest'], gi('ecr'), d['ins']['all'], d['scr']['all'], d['ca']['all']])
P(md_table(hdr, trs))
allrows = [dict(r, loop=(mm == m)) for mm in MAPS for r in tg_rows(mm)]
for key in ('dd', 'ecr', 'ins', 'scr'):
    f = lambda v, key=key: (rt([r for r in v if r['loop']], key) - rt([r for r in v if not r['loop']], key)) if any(r['loop'] for r in v) and any(not r['loop'] for r in v) else None
    P(f' Loop minus other maps, {key}: {f(allrows):+.2f} ci {boot_stat(allrows, f)} | other maps rate {rt([r for r in allrows if not r["loop"]], key):.2f}')
P(' Loop team-games with zero early destroyer smokes:', sum(r['dd'] == 0 for r in tg_rows(m)), 'of', len(tg_rows(m)), '| other maps', sum(r['dd'] == 0 for r in allrows if not r['loop']), 'of', sum(not r['loop'] for r in allrows))
P(' Loop team-games with zero early cruiser smokes:', sum(r['ecr'] == 0 for r in tg_rows(m)), '| other maps', sum(r['ecr'] == 0 for r in allrows if not r['loop']))
P(' Loop early destroyer smoke ships', cc(C(s['ship'] for s in dd if s['el'] < 300)), '| early cruiser smokes: ships', cc(C(s['ship'] for s in dd if s['early_cruiser'])), '| clans', clan_counts([s for s in dd if s['early_cruiser']]))
P(' Loop destroyers fielded (team-games)', cc(C(p['ship'].replace('\xa0', ' ') for g in games_on(m) for p in g['roster'].values() if p['ship_class'] == 'Destroyer'), 12))
P(' long-smoke ships share of destroyer slots: Loop', pct([p for g in games_on(m) for p in g['roster'].values() if p['ship_class'] == 'Destroyer'], lambda p: p['ship'] in LONG_SHIPS),
  '| other maps', pct([p for g in G.values() if g['map'] != m for p in g['roster'].values() if p['ship_class'] == 'Destroyer'], lambda p: p['ship'] in LONG_SHIPS))
R['LP-1'] = lp1

P('\n=== LP-2 spread of opening positions (first smoke of each team-game, any class)')
def first_smokes(mm, pool=None):
    out = []
    for k, t in tgames(mm):
        v = sorted([s for s in (pool or S) if s['game'] == k and s['team'] == t], key=lambda s: s['el'])
        if v: out.append(v[0])
    return out
lp2 = {}; trs = []
def spread(fs):
    cx, cz = mean(s['nx'] for s in fs), mean(s['nz'] for s in fs)
    return mean(math.hypot(s['nx'] - cx, s['nz'] - cz) for s in fs) * WU / 1000
def spread_side(fs):
    """Mean distance from the centre of the smoke's own cluster side (west or east of the map centre line): removes the two-flank effect."""
    out = []
    for side in (True, False):
        v = [s for s in fs if (s['nx'] < 0) == side]
        if v:
            cx, cz = mean(s['nx'] for s in v), mean(s['nz'] for s in v); out += [math.hypot(s['nx'] - cx, s['nz'] - cz) for s in v]
    return mean(out) * WU / 1000
def cells80(fs):
    c = C(s['ncell_name'] for s in fs); tot = 0; n = 0
    for _, k in c.most_common():
        tot += k; n += 1
        if tot >= 0.8 * len(fs): break
    return n, len(c)
for mm in MAPL:
    fs = first_smokes(mm); sp = spread(fs); lo, hi = boot_stat(fs, spread); n80, nc = cells80(fs); sps = spread_side(fs); top_cell = C(s['ncell_name'] for s in fs).most_common(1)[0]
    size_km = MAPS[mm]['space_size'] * WU / 1000
    fdd = first_smokes(mm, DD);
    lp2[mm] = dict(n=len(fs), mean_km_from_centre=round(sp, 2), ci=[round(lo, 2), round(hi, 2)], share_of_map_width_pct=round(100 * sp / size_km, 1), mean_km_from_own_side_centre=round(sps, 2), cells_for_80pct=n80, cells_used=nc,
                   top_cell=top_cell[0], top_cell_share_pct=round(100 * top_cell[1] / len(fs)), median_time=clock(med(s['el'] for s in fs)), first_before_5min_pct=round(pct(fs, lambda s: s['el'] < 300)),
                   top6_km=round(spread([s for s in fs if s['grp'] == 'top']), 2), rest_km=round(spread([s for s in fs if s['grp'] == 'rest']), 2))
    dlo, dhi = boot_diff(fs, lambda v: spread(v) if len(v) >= 3 else None)
    lp2[mm]['top_minus_rest_ci'] = [round(dlo, 2), round(dhi, 2)]
    trs.append([mm, len(fs), f'{sp:.1f} km ({lo:.1f} to {hi:.1f})', f'{100 * sp / size_km:.0f}%', f'{sps:.1f} km', f'{n80} of {nc}', f'{top_cell[0]} ({100 * top_cell[1] / len(fs):.0f}%)', lp2[mm]['median_time'], f"{lp2[mm]['first_before_5min_pct']}%",
                f"{lp2[mm]['top6_km']} / {lp2[mm]['rest_km']} ({dlo:+.1f} to {dhi:+.1f})"])
P(md_table(['Map', 'Team-games with a smoke', 'Mean distance of the first smoke from the map average first-smoke position (interval)', 'as share of map width', 'Same, measured within the west and east halves', 'Grid cells holding 80% of first smokes (of cells used)', 'Most used cell (share)', 'Median time of first smoke', 'First smoke before 5:00', 'Top 6 / Rest spread, km (interval of difference)'], trs))
fsl = first_smokes(m)
P(' Loop first smokes: cells', cc(C(s['ncell_name'] for s in fsl), 12), '| zone', cc(C(s['zone'] for s in fsl)), '| top zone', cc(C(s['zone'] for s in fsl if s['grp'] == 'top')), '| rest zone', cc(C(s['zone'] for s in fsl if s['grp'] == 'rest')))
P(' Loop first-smoke at zone A', gtxt(gap(fsl, lambda s: s['zone'] == 'A')), '| B', gtxt(gap(fsl, lambda s: s['zone'] == 'B')), '| C', gtxt(gap(fsl, lambda s: s['zone'] == 'C')))
R['LP-2'] = lp2

P('\n=== LP-3 first smoker by ship')
lp3 = {}; trs = []
for mm in MAPL:
    fs = first_smokes(mm); c = C(s['ship'] for s in fs); ct = C(s['ship'] for s in fs if s['grp'] == 'top'); cr = C(s['ship'] for s in fs if s['grp'] == 'rest')
    lp3[mm] = dict(n=len(fs), all=dict(c.most_common()), top6=dict(ct.most_common()), rest=dict(cr.most_common()), long_ship_share_pct=round(pct(fs, lambda s: s['ship'] in LONG_SHIPS)), sitter_share_pct=round(pct(fs, lambda s: s['habit'] == 'cap sitters')),
                   cruiser_class_share_pct=round(pct(fs, lambda s: s['cls'] == 'cruiser')))
    trs.append([mm, len(fs), cc(c, 6), cc(ct, 4), cc(cr, 4), f"{lp3[mm]['long_ship_share_pct']}%", f"{lp3[mm]['sitter_share_pct']}%", f"{lp3[mm]['cruiser_class_share_pct']}%"])
P(md_table(['Map', 'First smokes', 'First smoker, all', 'Top 6', 'Rest', 'Long-smoke ships (Somers, Gearing, Harugumo, Delny)', 'Cap sitters', 'Cruisers'], trs))
gl = gap([dict(s, loop=s['map'] == m) for mm in MAPS for s in first_smokes(mm)], lambda s: s['ship'] in LONG_SHIPS)
allf = [s for mm in MAPS for s in first_smokes(mm)]
f = lambda v: (pct([s for s in v if s['map'] == m], lambda s: s['ship'] in LONG_SHIPS) - pct([s for s in v if s['map'] != m], lambda s: s['ship'] in LONG_SHIPS)) if any(s['map'] == m for s in v) else None
P(' long-ship share of first smokes, Loop minus other maps', f(allf), boot_stat(allf, f), '| other maps', pct([s for s in allf if s['map'] != m], lambda s: s['ship'] in LONG_SHIPS))
P(' Loop first smoker clans by ship:');
for sh, v in sorted(by(fsl, 'ship').items(), key=lambda x: -len(x[1])): P(f'   {sh} {len(v)}: {clan_counts(v)} | cells {cc(C(s["ncell_name"] for s in v), 5)} | median {clock(med(s["el"] for s in v))}')
R['LP-3'] = lp3

P('\n=== LP-5 long smokes at F8 and F10')
lng = [s for s in dd if s['ship'] in LONG_SHIPS]; lp5 = {}
P(' long smokes on Loop', len(lng), clan_counts(lng), '| ships', cc(C(s['ship'] for s in lng)))
for cells in (('F8',), ('F10',), ('F8', 'F10')):
    for nm, pool in (('long smokes', lng), ('all destroyer smokes', dd)):
        g = gap(pool, lambda s: s['ncell_name'] in cells); v = [s for s in pool if s['ncell_name'] in cells]
        lp5['+'.join(cells) + ' ' + nm] = dict(g, clans=clan_dict(v), conc=round(mean(s['conc'] for s in v)) if v else None, n=len(v))
        P(f' {"+".join(cells)} {nm}: {gtxt(g)} | n {len(v)} | conc {kf(mean(s["conc"] for s in v)) if v else "-"} median {kf(med(s["conc"] for s in v)) if v else "-"} | deaths {sum(s["deaths"] for s in v)} | ships {cc(C(s["ship"] for s in v))} | {clan_counts(v)} | cruisers inside {cc(cruiser_counts(v, "inside"))} | early {sum(s["el"] < 300 for s in v)} | zone {cc(C(s["zone"] for s in v))}')
for s in sorted([s for s in lng if s['ncell_name'] in ('F8', 'F10')], key=lambda s: (s['ncell_name'], s['grp'])): P(f'    {s["ncell_name"]} {s["slug"]} {s["team"]} {s["ship"]} {clock(s["el"])} conc {s["conc"]:.0f} cr {[(c["ship"], c["how"]) for c in s["cruisers"]]}')
P(' cell averages (all DD): F8', kf(mean(s['conc'] for s in dd if s['ncell_name'] == 'F8')), 'n', sum(s['ncell_name'] == 'F8' for s in dd), '| F10', kf(mean(s['conc'] for s in dd if s['ncell_name'] == 'F10')), 'n', sum(s['ncell_name'] == 'F10' for s in dd), '| map avg', kf(mean(s['conc'] for s in dd)))
R['LP-5'] = lp5
for cn in ('F8', 'F10'):
    v = [s for s in dd if s['ncell_name'] == cn]; g = gap(dd, lambda s: s['ncell_name'] == cn); c_, r_ = 'ABCDEFGHIJ'.index(cn[0]), int(cn[1:]) - 1
    SPOTS.append(dict(id=f'c5-lp-{cn.lower()}', **spot_record(m, 'high_cell', 'shared', f'High-paying cell {cn}', S, v, dict(type='polygon', points=[[c0 / 10, r0 / 10] for c0, r0 in ((r_, c_), (r_ + 1, c_), (r_ + 1, c_ + 1), (r_, c_ + 1))]),
                 dict(subject='destroyer smokes in the cell', share_top6_pct=g['top_pct'], share_rest_pct=g['rest_pct'], gap_pts=g['gap'], ci_pts=[g['lo'], g['hi']],
                      long_smokes=dict(top6=sum(1 for s in v if s['ship'] in LONG_SHIPS and s['grp'] == 'top'), rest=sum(1 for s in v if s['ship'] in LONG_SHIPS and s['grp'] == 'rest'))))))

P('\n=== LP-6 cap sitters on B')
rb = r4_spot('loop-cap-f7'); sit = [s for s in dd if s['habit'] == 'cap sitters']; mem = [s for s in sit if in_r4(rb, s)]
g_b = gap(sit, lambda s: in_r4(rb, s)); P(' spot', gtxt(g_b)); P(' ', clan_counts(mem)); P(' ships top', cc(C(s['ship'] for s in mem if s['grp'] == 'top')), '| rest', cc(C(s['ship'] for s in mem if s['grp'] == 'rest')))
P(' sitters on Loop all', clan_counts(sit), '| ships', cc(C((s['grp'], s['ship']) for s in sit), 12))
for gname in ('top', 'rest'):
    w = [s for s in mem if s['grp'] == gname]; P(f'  {gname}: n {len(w)} conc {kf(mean(s["conc"] for s in w))} deaths {sum(s["deaths"] for s in w)} own {cc(C(s["near_own"] for s in w))} we_took {sum(1 for s in w if s["we_took"])}/{sum(1 for s in w if s["we_took"] is not None)} enemy_took {sum(1 for s in w if s["enemy_took"])}/{sum(1 for s in w if s["enemy_took"] is not None)} zone {cc(C(s["zone"] for s in w))} med {clock(med(s["el"] for s in w))}')
P(' Rest sitters elsewhere: zone', cc(C(s['zone'] for s in sit if s['grp'] == 'rest' and not in_r4(rb, s))), '| top elsewhere', cc(C(s['zone'] for s in sit if s['grp'] == 'top' and not in_r4(rb, s))))
P(' Daring only in the spot', gtxt(gap([s for s in sit if s['ship'] == 'Daring'], lambda s: in_r4(rb, s))), '| non-Daring sitters', gtxt(gap([s for s in sit if s['ship'] != 'Daring'], lambda s: in_r4(rb, s))))
R['LP-6'] = dict(spot=g_b, clans=clan_dict(mem), ships=dict(top6=dict(C(s['ship'] for s in mem if s['grp'] == 'top')), rest=dict(C(s['ship'] for s in mem if s['grp'] == 'rest'))))
SPOTS.append(dict(id='c5-lp-sitters-b', **spot_record(m, 'top6_spot', 'top6', 'Cap sitters: own side and east half of cap B (F7/F8)', S, mem, ell_shape(rb),
             dict(subject='cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze)', share_top6_pct=g_b['top_pct'], share_rest_pct=g_b['rest_pct'], gap_pts=g_b['gap'], ci_pts=[g_b['lo'], g_b['hi']]))))
# first-smoke record
fsl_c = C(s['ncell_name'] for s in fsl)
save_json('part-lp.json', dict(R=R, SPOTS=SPOTS))
