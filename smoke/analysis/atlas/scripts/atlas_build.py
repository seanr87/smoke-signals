# Smoke Atlas: builds spots.json, caps.json, maps/ (copies) and tables.txt (every number the copy uses, per map).
# Run from the repo root: python -I -X utf8 smoke/analysis/atlas/scripts/atlas_build.py
# Reads: the batch (through round3/common.py), round4/part-b/spots.json, round3/module-4/cells.json and tables-r4.txt.
import sys, os, re
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_lib import *

S, G = load()
DD = [s for s in S if s['cls'] == 'destroyer']
PB = json.load(open(os.path.join(ANALYSIS, 'round4', 'part-b', 'spots.json'), encoding='utf-8'))
CELLS = json.load(open(os.path.join(ANALYSIS, 'round3', 'module-4', 'cells.json'), encoding='utf-8'))['rows']
M4_TABLES = open(os.path.join(ANALYSIS, 'round3', 'module-4', 'tables-r4.txt'), encoding='utf-8').read()
OUT = []
def P(*a):
    OUT.append(' '.join(str(x) for x in a))

# plain-words labels, written after reading the first run of this script (keys are record ids)
RADAR_TRIM_KM = 8.0   # radar plays farther than this from their group's median point are left out of the drawn ellipse (not out of the counts)
LABELS = {
    'sg-early-g1': 'west flank, short of cap A on the own side',
    'sg-early-g9': 'east edge, beside cap D',
    'sg-early-f5': 'centre, own-side rim of cap B',
    'hs-early-g10': 'east edge, short of cap D on the own side',
    'hs-early-g5': 'centre, short of cap C on the own side',
    'loop-early-f4': 'west, own half of cap A',
    'loop-early-f8': 'between caps B and C, own side',
    'mr-early-g7': 'east-centre, short of cap C on the own side',
    'mr-early-g4': 'west-centre, short of cap B on the own side',
    'lof-early-f5': 'centre, own-side rim of cap B',
    'lof-early-f3': 'west, short of cap A on the own side',
    'sof-early-f2': 'west, in and around cap B',
    'sof-early-f9': 'east, short of cap D on the own side',
    'oki-early-d2': 'north-west, own-side rim of cap A',
    'sg-radar-a': 'west cap A, smoked from below it',
    'sg-radar-c': 'far east cap C, smoked from the east side around cap D (wide)',
    'hs-radar-d': 'east cap D, smoked from its own side',
    'hs-radar-c': 'centre cap C, smoked from the south',
    'mr-radar-b': 'centre cap B, smoked from its own side',
    'sg-deaths-f1': 'west flank, below cap A',
    'sg-deaths-e9': 'east, between caps C and D',
    'hs-deaths-g10': 'east edge, below cap D',
    'lof-deaths-f3': 'west, below cap A',
    'lof-deaths-f6': 'centre, own-side rim of cap B',
    'sof-deaths-f2': 'west lane between caps A and B (wide)',
    'oki-deaths-h4': 'south-west water on the own side of cap C (wide)',
}

def flat_ci(lohi, nd=0):
    return [None, None] if lohi[0] is None else [round(lohi[0], nd), round(lohi[1], nd)]
def capwon(ss):
    """Cap won among smokes whose contested cap was not already ours: (pct, n)."""
    v = [s for s in ss if s['own'] != 'ours']
    return (round(pct(v, lambda s: s['cap_won']), 1) if v else None), len(v)
def base_numbers(ss):
    cw, cwn = capwon(ss)
    return dict(n=len(ss), top6_n=sum(s['grp'] == 'top' for s in ss), rest_n=sum(s['grp'] == 'rest' for s in ss), pn_n=sum(s['is_pn'] for s in ss),
                clans=len(set(s['team'] for s in ss)), games=len(set(s['game'] for s in ss)),
                concealed_damage_per_smoke=round(mean(s['conc'] for s in ss)), deaths_per_100=round(100 * mean(s['deaths'] for s in ss), 1),
                cap_won_pct=cw, cap_won_n=cwn, median_time_s=round(med(s['el'] for s in ss)))
def typical_links(ss, centre, k=3, pred=None):
    """Top 6 smokes nearest the centre (world units), one per clan first, as links."""
    v = [s for s in ss if s['grp'] == 'top' and (pred is None or pred(s))]
    v.sort(key=lambda s: math.hypot(s['nx'] - centre[0], s['nz'] - centre[1]))
    out, seen = [], set()
    for s in v:
        if s['team'] in seen: continue
        seen.add(s['team']); out.append(s)
    for s in v:
        if s not in out: out.append(s)
    return out[:k]
def link_str(s): return f"{s['team']} {s['ship']} {clock(s['el'])} {s['link']}"

def cast_of(ss):
    """Per smoke: the nearest cruiser inside the smoke and the nearest other allied destroyer, from the positions recorded when the smoke was fully laid."""
    cru, dd2 = [], []
    for s in ss:
        c = [x for x in s['cast'] if x['ally'] and not x['is_smoker'] and x['cls'] == 'cruiser' and x['how'] == 'inside']
        if c: cru.append((s, min(c, key=lambda x: x['dist_m'])))
        d = [x for x in s['cast'] if x['ally'] and not x['is_smoker'] and x['cls'] == 'destroyer']
        if d: dd2.append((s, min(d, key=lambda x: x['dist_m'])))
    return cru, dd2

def cast_records(m, parent_id, ss, min_n, pb_cast=None):
    """Cast position records (cruiser inside, second destroyer) for the smokes of one spot. Positions: mean, with the 2-sigma ellipse."""
    recs = []
    cru, dd2 = cast_of(ss)
    for kind, key, lst in (('cast_cruiser', 'cruiser', cru), ('cast_second_dd', 'second_dd', dd2)):
        if len(lst) < min_n:
            P(f'     {kind}: recorded for {len(lst)} of {len(ss)} (below {min_n}, no record)')
            continue
        pts = [(x['nx'], x['nz']) for _, x in lst]
        e = ellipse(pts); cuv, shape = ellipse_uv(m, e)
        ships = C(x['ship'] for _, x in lst)
        nums = dict(n=len(lst), n_parent=len(ss), share_of_parent_pct=round(100 * len(lst) / len(ss), 1),
                    top6_n=sum(s['grp'] == 'top' for s, _ in lst), rest_n=sum(s['grp'] == 'rest' for s, _ in lst),
                    median_km_from_nearest_puff=round(med(x['dist_m'] for _, x in lst) / 1000, 1),
                    median_km_forward_of_smoke_centre=round(med(x['fwd_m'] for _, x in lst) / 1000, 1),
                    forward_n=sum(x['fwd_m'] > 0 for _, x in lst), forward_share_pct=round(pct(lst, lambda t: t[1]['fwd_m'] > 0), 1),
                    most_common_ships=', '.join(f'{a} {b}' for a, b in ships.most_common(3)))
        if kind == 'cast_cruiser': nums['radar_cruiser_n'] = sum(x['radar'] for _, x in lst)
        cap, d = nearest_cap(G, m, e[0], e[1])
        nums['km_from_nearest_cap_edge'] = round(d, 1); nums['nearest_cap'] = cap
        if pb_cast and pb_cast.get(key):
            pc = pb_cast[key]['centre_uv']
            if math.hypot(pc[0] - cuv[0], pc[1] - cuv[1]) > 0.002 or pb_cast[key]['n'] != len(lst):
                P(f'     note: {kind} centre recomputed here {cuv} n {len(lst)}; Part B has {pc} n {pb_cast[key]["n"]}; the Part B centre is kept')
            cuv = pc
        what = 'cruiser inside the smoke' if kind == 'cast_cruiser' else 'nearest other allied destroyer'
        recs.append(dict(id=f'{parent_id}-{"cruiser" if kind == "cast_cruiser" else "dd2"}', map=m, kind=kind,
                         label=f'{what}: {side_words(G, m, e[0], e[1])}, cells {"/".join(cells_of(m, pts, 2))}', subject=ships.most_common(1)[0][0], parent=parent_id,
                         centre_uv=cuv, shape=shape, numbers=nums, small_n=len(lst) < SOLID_N, links=[],
                         notes='Mean position at the moment each smoke was fully laid (the only moment the batch records positions). '
                               + ('The nearest cruiser inside each smoke.' if kind == 'cast_cruiser' else 'The nearest other allied destroyer with a recorded position; forward = toward the enemy spawn relative to the smoke centre. Not recorded does not mean absent.')
                               + (' Count is below 8: drawn for the formation only.' if len(lst) < MIN_N else '')))
        P(f'     {kind}: n {len(lst)} of {len(ss)} | centre uv {cuv} | {recs[-1]["label"]} | ships {nums["most_common_ships"]} | {nums["median_km_from_nearest_puff"]} km from puff, '
          f'{nums["median_km_forward_of_smoke_centre"]:+} km fwd, forward {nums["forward_n"]} of {len(lst)}' + (f' | radar cruiser {nums["radar_cruiser_n"]}' if kind == 'cast_cruiser' else ''))
    return recs

def radar_ship_name(s):
    """Ship behind the radar play. The batch names the player; the game roster gives the ship."""
    name = (s['off_radar'] or {}).get('ship') or (s['radar_cap'] or {}).get('ship')
    pl = next((p for p in G[s['game']]['roster'].values() if p.get('player') == name), None)
    return (pl['ship'].replace(' ', ' ') if pl else '?')

def in_pb_ellipse(m, sp, s):
    u, v = uv(m, s['nx'], s['nz']); cu, cv = sp['centre_uv']; e = sp['ellipse_uv']
    a = math.radians(e['angle_deg']); du, dv = u - cu, v - cv
    x, y = du * math.cos(a) + dv * math.sin(a), -du * math.sin(a) + dv * math.cos(a)
    return (x / e['ru']) ** 2 + (y / e['rv']) ** 2 <= 1.0

# ---------- Module 4 zone share intervals (parsed from its own output)
ZONE_CI = {}
cur = None
for line in M4_TABLES.splitlines():
    mm = re.match(r'== (.+?): games', line)
    if mm: cur = mm.group(1); continue
    if line.startswith('== pooled'): cur = None
    zz = re.match(r'\s+([A-D]) n\s+(\d+) conc .*?share top\s+(\d+)% rest\s+(\d+)% diff ([+-]?\d+) to ([+-]?\d+)( \*)?', line)
    if zz and cur: ZONE_CI[(cur, zz.group(1))] = (int(zz.group(5)), int(zz.group(6)), bool(zz.group(7)))

spots, caps_out = [], {}
P('Smoke Atlas tables. Batch', BATCH_NAME, '|', len(S), 'smokes,', len(G), 'games,', len(DD), 'destroyer smokes')
P('Top 6 W-L:', {t: win_loss(G)[t] for t in sorted(TOP)}, '| PN', win_loss(G).get(PN))
P('Early = first 5 minutes (elapsed < 300 s). Destroyer smokes unless a line says otherwise.')
e_all = [s for s in DD if s['el'] < EARLY_S]
P('ALL MAPS early destroyer smokes: Top 6', sum(s['grp'] == 'top' for s in e_all), 'Rest', sum(s['grp'] == 'rest' for s in e_all),
  '| radar cruiser inside: Top 6', sum(s['radar_ca_inside'] for s in e_all if s['grp'] == 'top'), 'Rest', sum(s['radar_ca_inside'] for s in e_all if s['grp'] == 'rest'))
P('ALL MAPS destroyer smokes: Top 6', sum(s['grp'] == 'top' for s in DD), 'Rest', sum(s['grp'] == 'rest' for s in DD),
  '| radar cruiser inside %: Top 6', round(pct([s for s in DD if s['grp'] == 'top'], lambda s: s['radar_ca_inside']), 1), 'Rest', round(pct([s for s in DD if s['grp'] == 'rest'], lambda s: s['radar_ca_inside']), 1))

for m in MAP_ORDER:
    code = MAP_CODE[m]; size = MAPS[m]['space_size']
    ms = [s for s in DD if s['map'] == m]; allm = [s for s in S if s['map'] == m]
    P(''); P('=' * 110); P(f'{m} | {NORM_NOTE[m]} | map {size * WU / 1000:.0f} km across | destroyer smokes {len(ms)} (Top 6 {sum(s["grp"] == "top" for s in ms)}, Rest {sum(s["grp"] == "rest" for s in ms)}, PN {sum(s["is_pn"] for s in ms)})'
      f' | all classes {len(allm)} | map average concealed damage per destroyer smoke {round(mean(s["conc"] for s in ms)):,}')

    # ---- caps and cap choice
    P(' CAPS AND CAP CHOICE (zone = nearest cap; source module-4/cells.json; interval from module-4/tables-r4.txt)')
    caps = []
    for c in sorted(map_caps(G, m), key=lambda c: c['cap']):
        u, v = uv(m, c['x'], c['z'])
        z = next((r for r in CELLS if r['map'] == m and r['kind'] == 'zone' and r['name'] == c['cap']), None)
        rec = dict(letter=c["cap"], centre_uv=[round(u, 4) + 0.0, round(v, 4) + 0.0], radius_u=round(c['r'] / size, 4), radius_km=round(c['r'] * WU / 1000, 2))
        if z:
            lo, hi, star = ZONE_CI.get((m, c['cap']), (None, None, False))
            rec['zone'] = dict(n=z['n'], top6_share_pct=z['top6_share_pct'], rest_share_pct=z['rest_share_pct'], top6_n=z['top6_n'], rest_n=z['rest_n'],
                               gap_pts=round(z['top6_share_pct'] - z['rest_share_pct'], 1), gap_ci_pts=[lo, hi], gap_clear_of_zero=star,
                               concealed_damage_per_smoke=z['concealed_damage_per_smoke'], deaths_per_100=z['deaths_per_100'], cap_won_pct_all_smokes=z['cap_won_pct'],
                               rated=z['rated'], small_n=z['small_n'])
            P(f'   cap {c["cap"]} uv {rec["centre_uv"]} r_u {rec["radius_u"]} ({rec["radius_km"]} km) | zone n {z["n"]} | Top 6 {z["top6_share_pct"]}% ({z["top6_n"]}) vs Rest {z["rest_share_pct"]}% ({z["rest_n"]}) '
              f'gap {rec["zone"]["gap_pts"]:+} ({lo:+} to {hi:+}{" *" if star else ""}) | {z["concealed_damage_per_smoke"]:,} per smoke, {z["deaths_per_100"]} deaths/100, cap won after {z["cap_won_pct"]}% of smokes{"" if z["rated"] else " | NOT RATED (n < 8)"}')
        caps.append(rec)
    caps_out[m] = dict(space_km=size * WU / 1000, transform=NORM_NOTE[m], own_spawn='bottom-left' if m in DIAGONAL else 'bottom', caps=caps)
    # check: the mirror maps caps onto caps
    for c in map_caps(G, m):
        x, z = norm(m, 'north', c['x'], c['z'])
        assert min(math.hypot(o['x'] - x, o['z'] - z) for o in map_caps(G, m)) < 10.0, (m, c)   # within 300 m (Mountain Range cap A sits 83 m off the centre line)

    # ---- signature spots and leads (Part B)
    P(' SIGNATURE SPOTS AND LEADS (source round4/part-b/spots.json; cast shapes recomputed here from the same smokes)')
    for sp in [x for x in PB if x['map'] == m]:
        subj = sp['subject']
        pool = [s for s in allm if s['cls'] in ('destroyer', 'cruiser') and (s['ship'] == subj or s['habit'] == subj)]
        tin = [s for s in pool if s['grp'] == 'top' and in_pb_ellipse(m, sp, s)]
        ok = len(tin) == sp['top6']['n_in']
        nums = dict(n=sp['top6']['n_in'], top6_n_total=sp['top6']['n_total'], top6_share_pct=sp['top6']['share_pct'], rest_n_in=sp['rest']['n_in'], rest_n_total=sp['rest']['n_total'],
                    rest_share_pct=sp['rest']['share_pct'], gap_pts=sp['gap_pts'], gap_ci_lo=sp['ci_pts'][0], gap_ci_hi=sp['ci_pts'][1],
                    top6_clans=', '.join(f'{k} {v}' for k, v in sp['top6']['clans'].items()), concealed_damage_per_smoke=sp['conc_per_smoke'], deaths_per_100=sp['deaths_per_100'],
                    cap_won_pct=sp['cap_won_pct'], cap_won_n=sp['cap_won_n'], median_time_s=sp['median_time_s'], formation_count=sp['formation_top6']['count'], formation_of=sp['formation_top6']['of'],
                    rest_formation_count=sp['formation_rest']['count'], rest_formation_of=sp['formation_rest']['of'], usual_partner=sp['usual_partner'], cells='/'.join(sp['cells']))
        shape = dict(type='ellipse', **sp['ellipse_uv'])
        spots.append(dict(id=sp['id'], map=m, kind=sp['kind'], label=sp['label'], subject=subj, parent=None, centre_uv=sp['centre_uv'], shape=shape, numbers=nums,
                          small_n=sp['top6']['n_in'] < SOLID_N, links=sp['examples'], notes='Formation: ' + sp['formation'] + '. ' + sp.get('notes', '')))
        P(f'   {sp["kind"].upper()} {sp["id"]}: {subj}, {sp["label"]} ({nums["cells"]}) | Top 6 {nums["n"]} of {nums["top6_n_total"]} ({nums["top6_share_pct"]}%) vs Rest {nums["rest_n_in"]} of {nums["rest_n_total"]} ({nums["rest_share_pct"]}%) '
          f'gap {sp["gap_pts"]:+} ({sp["ci_pts"][0]:+} to {sp["ci_pts"][1]:+}) | clans {nums["top6_clans"]} | {sp["conc_per_smoke"]:,} per smoke, {sp["deaths_per_100"]} deaths/100, cap won {sp["cap_won_pct"]}% of {sp["cap_won_n"]} | median {clock(sp["median_time_s"])}'
          f' | membership recomputed {len(tin)} ({"matches" if ok else "DIFFERS"})')
        P(f'     formation: {sp["formation"]}')
        for e in sp['examples']: P('     example', e)
        spots += cast_records(m, sp['id'], tin, 4, sp['cast'])

    # ---- paying cells (Module 4)
    P(' PAYING CELLS (source module-4/cells.json; high = at least 1.4x the map average, low = at most 0.6x; cap won here is after % of all smokes in the cell)')
    rows = [r for r in CELLS if r['map'] == m and r['kind'] == 'cell' and r['rated']]
    chosen = [(r, 'paying_high', 'high') for r in rows if r['flag'] == 'high'] + [(r, 'paying_low', 'low') for r in rows if r['flag'] == 'low']
    if not any(k == 'paying_high' for _, k, _ in chosen) and rows:
        b = max(rows, key=lambda r: r['concealed_damage_per_smoke'])
        chosen.append((b, 'paying_high', 'only_rated_cell_not_high' if len(rows) == 1 else 'best_rated_cell_not_high'))
    if not any(k == 'paying_low' for _, k, _ in chosen) and len(rows) > 1:
        w = min(rows, key=lambda r: r['concealed_damage_per_smoke'])
        chosen.append((w, 'paying_low', 'lowest_rated_cell_not_low'))
    for r, kind, flag in sorted(chosen, key=lambda t: -t[0]['concealed_damage_per_smoke']):
        col, row = int(r['name'][1:]) - 1, 'ABCDEFGHIJ'.index(r['name'][0])
        cs = [s for s in ms if s['ncell'] == (col, row)]
        assert len(cs) == r['n'], (m, r['name'], len(cs), r['n'])
        cx, cz = mean(s['nx'] for s in cs), mean(s['nz'] for s in cs)
        ex = sorted([s for s in cs if s['grp'] == 'top'] or cs, key=lambda s: abs(s['conc'] - r['median_concealed_damage']))[:2]
        nums = dict(n=r['n'], concealed_damage_per_smoke=r['concealed_damage_per_smoke'], median_concealed_damage=r['median_concealed_damage'], deaths_per_100=r['deaths_per_100'],
                    cap_won_pct_all_smokes=r['cap_won_pct'], top6_n=r['top6_n'], rest_n=r['rest_n'], top6_share_pct=r['top6_share_pct'], rest_share_pct=r['rest_share_pct'],
                    map_avg_concealed_damage=r['map_avg_concealed_damage'], times_map_average=round(r['concealed_damage_per_smoke'] / r['map_avg_concealed_damage'], 2), flag=flag,
                    median_time_s=round(med(s['el'] for s in cs)))
        lab = f'cell {r["name"]}: {side_words(G, m, cx, cz)}'
        note = {'high': 'Rated high by Module 4.', 'low': 'Rated low by Module 4.', 'best_rated_cell_not_high': 'Not rated high: the best of the rated cells on a map with no high cell.',
                'lowest_rated_cell_not_low': 'Not rated low: the lowest of the rated cells on a map with no low cell.', 'only_rated_cell_not_high': 'Not rated high: the only cell on this map with 8 or more smokes.'}[flag]
        spots.append(dict(id=f'{code}-cell-{r["name"].lower()}', map=m, kind=kind, label=lab, subject=None, parent=None, centre_uv=[round((col + .5) / 10, 4), round((row + .5) / 10, 4)],
                          shape=cell_polygon(col, row), numbers=nums, small_n=r['small_n'], links=[s['link'] for s in ex],
                          notes=note + ' Destroyer smokes whose centre falls in the grid cell. Association only: what smokes laid here returned.'))
        P(f'   {kind} {r["name"]} [{flag}] n {r["n"]}{"*" if r["small_n"] else ""} | {r["concealed_damage_per_smoke"]:,} per smoke (median {r["median_concealed_damage"]:,}; {nums["times_map_average"]}x map avg) | {r["deaths_per_100"]} deaths/100 | cap won after {r["cap_won_pct"]}% '
          f'| Top 6 {r["top6_n"]} Rest {r["rest_n"]} | median {clock(nums["median_time_s"])} | {lab}')

    # ---- early setup
    early = [s for s in ms if s['el'] < EARLY_S]
    et = [s for s in early if s['grp'] == 'top']; er = [s for s in early if s['grp'] == 'rest']
    P(f' EARLY SETUP (destroyer smokes in the first 5 minutes): n {len(early)} (Top 6 {len(et)}, Rest {len(er)}) | radar cruiser inside: Top 6 {sum(s["radar_ca_inside"] for s in et)} of {len(et)} '
      f'({n0(pct(et, lambda s: s["radar_ca_inside"]))}%), Rest {sum(s["radar_ca_inside"] for s in er)} of {len(er)} ({n0(pct(er, lambda s: s["radar_ca_inside"]))}%)')
    early_centres = []
    for idx in mean_shift([(s['nx'], s['nz']) for s in early]):
        cs = [early[i] for i in idx]
        pts = [(s['nx'], s['nz']) for s in cs]
        cx, cz = mean(p[0] for p in pts), mean(p[1] for p in pts)
        if len(cs) < MIN_N:
            P(f'   (cluster of {len(cs)}, below 8, not reported: {"/".join(cells_of(m, pts, 2))}, {side_words(G, m, cx, cz)}; Top 6 {sum(s["grp"] == "top" for s in cs)})')
            continue
        e = ellipse(pts); cuv, shape = ellipse_uv(m, e)
        sid = f'{code}-early-{cells_of(m, pts, 1)[0].lower()}'
        t = [s for s in cs if s['grp'] == 'top']; r = [s for s in cs if s['grp'] == 'rest']
        cru, dd2 = cast_of(cs)
        nums = base_numbers(cs)
        nums.update(share_of_map_early_smokes_pct=round(100 * len(cs) / len(early), 1), cells='/'.join(cells_of(m, pts, 3)),
                    top6_share_of_top6_early_pct=round(100 * len(t) / len(et), 1) if et else None, rest_share_of_rest_early_pct=round(100 * len(r) / len(er), 1) if er else None,
                    radar_cruiser_inside_n=sum(s['radar_ca_inside'] for s in cs), radar_cruiser_inside_pct=round(pct(cs, lambda s: s['radar_ca_inside']), 1),
                    top6_radar_cruiser_inside_n=sum(s['radar_ca_inside'] for s in t), rest_radar_cruiser_inside_n=sum(s['radar_ca_inside'] for s in r),
                    inside_cap_pct=round(pct(cs, lambda s: s['inside']), 1), median_km_smoke_edge_to_contested_cap_edge=round(med(s['edge'] for s in cs) / 1000, 1),
                    km_centre_to_nearest_cap_edge=round(nearest_cap(G, m, cx, cz)[1], 1), nearest_cap=nearest_cap(G, m, cx, cz)[0],
                    stacked_pct=round(pct(cs, lambda s: s['coverage'] == 'stacked'), 1), ships=', '.join(f'{a} {b}' for a, b in C(s['ship'] for s in cs).most_common(4)),
                    second_dd_recorded_n=len(dd2), second_dd_forward_n=sum(x['fwd_m'] > 0 for _, x in dd2),
                    top6_second_dd_forward_n=sum(x['fwd_m'] > 0 for s, x in dd2 if s['grp'] == 'top'), rest_second_dd_forward_n=sum(x['fwd_m'] > 0 for s, x in dd2 if s['grp'] == 'rest'),
                    radius_km_long=round(e[2] / KM, 1), radius_km_short=round(e[3] / KM, 1))
        ex = typical_links(cs, (cx, cz), 3, lambda s: s['radar_ca_inside']) or typical_links(cs, (cx, cz), 3)
        lab = LABELS.get(sid, f'{side_words(G, m, cx, cz)}, cells {nums["cells"]}')
        spots.append(dict(id=sid, map=m, kind='early_smoke', label=lab, subject='destroyer smoke, first 5 minutes', parent=None, centre_uv=cuv, shape=shape, numbers=nums,
                          small_n=len(cs) < SOLID_N, links=[s['link'] for s in ex],
                          notes='Mean-shift cluster (2 km) of all early destroyer smoke centres on the map, both groups; the ellipse is 2 standard deviations. '
                                'Cap won counts only smokes whose contested cap was not already ours. Links are Top 6 smokes nearest the centre.'))
        early_centres.append((sid, cs, (cx, cz)))
        P(f'   EARLY {sid}: {lab} | cells {nums["cells"]} | centre uv {cuv} radii {nums["radius_km_long"]} x {nums["radius_km_short"]} km | n {len(cs)} = {nums["share_of_map_early_smokes_pct"]}% of the map (Top 6 {len(t)} = {nums["top6_share_of_top6_early_pct"]}% of theirs, Rest {len(r)} = {nums["rest_share_of_rest_early_pct"]}%)')
        P(f'     radar cruiser inside {nums["radar_cruiser_inside_n"]} of {len(cs)} (Top 6 {nums["top6_radar_cruiser_inside_n"]} of {len(t)}, Rest {nums["rest_radar_cruiser_inside_n"]} of {len(r)}) | {nums["concealed_damage_per_smoke"]:,} per smoke, {nums["deaths_per_100"]} deaths/100, '
          f'cap won {nums["cap_won_pct"]}% of {nums["cap_won_n"]} | median {clock(nums["median_time_s"])} | inside a cap {nums["inside_cap_pct"]}%, smoke edge {nums["median_km_smoke_edge_to_contested_cap_edge"]} km from the contested cap edge; centre {nums["km_centre_to_nearest_cap_edge"]} km from cap {nums["nearest_cap"]} edge | stacked {nums["stacked_pct"]}% | {nums["ships"]}')
        P(f'     second destroyer recorded {len(dd2)} of {len(cs)}, forward {nums["second_dd_forward_n"]} (Top 6 {nums["top6_second_dd_forward_n"]} of {len(t)}, Rest {nums["rest_second_dd_forward_n"]} of {len(r)})')
        for s in ex: P('     example', link_str(s))
        spots += cast_records(m, sid, cs, MIN_N)

    # ---- radar addresses
    rp = [s for s in ms if s['radar_play']]
    sv = [s for s in allm if s['radar_play'] and s['cls'] == 'cruiser']
    tg = sum(1 for g in G.values() if g['map'] == m) * 2
    P(f' RADAR FROM SMOKE: destroyer radar plays {len(rp)} (Top 6 {sum(s["grp"] == "top" for s in rp)}) = {len(rp) / tg:.2f} per team-game ({tg} team-games) | by contested cap {dict(sorted(C(s["ncap"] for s in rp).items()))}'
      f' | Svea radar plays {len(sv)} (Top 6 {sum(s["grp"] == "top" for s in sv)}; cells {dict(C(s["ncell_name"] for s in sv))}; contested cap {dict(C(s["ncap"] for s in sv))})')
    radar_centres = []
    for cap, cs in sorted(by(rp, 'ncap').items(), key=lambda kv: -len(kv[1])):
        pts = [(s['nx'], s['nz']) for s in cs]
        cx, cz = mean(p[0] for p in pts), mean(p[1] for p in pts)
        if len(cs) < MIN_N:
            P(f'   (cap {cap}: {len(cs)} plays, below 8, not reported; cells {"/".join(cells_of(m, pts, 3))})')
            continue
        mx, mz = med(p[0] for p in pts), med(p[1] for p in pts)
        kept = [p for p in pts if math.hypot(p[0] - mx, p[1] - mz) <= RADAR_TRIM_KM * KM]   # the drawn shape leaves out far-flung plays
        e = ellipse(kept); cuv, shape = ellipse_uv(m, e)
        core = mean_shift(pts)[0]; cpts = [pts[i] for i in core]
        ships = C(radar_ship_name(s) for s in cs)
        nums = base_numbers(cs)
        nums.update(contested_cap=cap, cap_control_n=sum(s['pp'] == 'cap_control' for s in cs), radar_trap_n=sum(s['pp'] == 'radar_trap' for s in cs),
                    first_5_min_pct=round(pct(cs, lambda s: s['el'] < EARLY_S), 1), cap_won_count=sum(s['cap_won'] for s in cs if s['own'] != 'ours'),
                    cells='/'.join(cells_of(m, pts, 3)), usual_radar_ships=', '.join(f'{a} {b}' for a, b in ships.most_common(3)),
                    plays_inside_drawn_shape=len(kept), tightest_core_n=len(core), tightest_core_cells='/'.join(cells_of(m, cpts, 2)), inside_cap_pct=round(pct(cs, lambda s: s['inside']), 1),
                    radius_km_long=round(e[2] / KM, 1), radius_km_short=round(e[3] / KM, 1))
        sid = f'{code}-radar-{cap.lower()}'
        lab = LABELS.get(sid, f'radar on cap {cap} from {side_words(G, m, cx, cz)}')
        ex = typical_links(cs, (mean(p[0] for p in cpts), mean(p[1] for p in cpts)), 3)
        spots.append(dict(id=sid, map=m, kind='radar', label=lab, subject='destroyer smoke with a radar play', parent=None, centre_uv=cuv, shape=shape, numbers=nums, small_n=len(cs) < SOLID_N,
                          links=[s['link'] for s in ex],
                          notes='Destroyer smokes whose primary purpose is a radar play (cap control or radar trap), grouped by the cap they contested, as in Module 3. '
                                f'The ellipse (2 standard deviations) is where those smokes were laid, not the cap; it is drawn from the {len(kept)} of {len(cs)} plays within {RADAR_TRIM_KM:.0f} km of the group median, '
                                'so far-flung plays do not stretch it. All numbers are for the whole group. tightest_core is the largest 2 km cluster inside the group.'
                                + (' Wide: the smokes are spread, read it as a zone.' if e[2] / KM > 6 else '')))
        radar_centres.append((sid, cs, (cx, cz)))
        P(f'   RADAR {sid}: {lab} | cells {nums["cells"]} | centre uv {cuv} radii {nums["radius_km_long"]} x {nums["radius_km_short"]} km | n {len(cs)} (cap control {nums["cap_control_n"]}, Top 6 {nums["top6_n"]}) | first 5 min {nums["first_5_min_pct"]}% '
          f'| cap won {nums["cap_won_count"]} of {nums["cap_won_n"]} | {nums["concealed_damage_per_smoke"]:,} per smoke | radar ships {nums["usual_radar_ships"]} | tightest core {len(core)} in {nums["tightest_core_cells"]} | inside a cap {nums["inside_cap_pct"]}% | drawn shape uses {len(kept)} of {len(cs)} plays')
        for s in ex: P('     example', link_str(s))

    # ---- deaths
    dth = [s for s in allm if s['deaths'] > 0]
    ddth = [s for s in ms if s['deaths'] > 0]
    P(f' DEATHS IN SMOKE (all classes; clusters at 2.5 km because deaths are sparse): smokes with a death {len(dth)} of {len(allm)} ({sum(s["deaths"] for s in dth)} deaths; {100 * sum(s["deaths"] for s in allm) / len(allm):.1f} per 100 smokes) '
      f'| destroyer smokes only: {len(ddth)} of {len(ms)} ({sum(s["deaths"] for s in ddth)} deaths; {100 * sum(s["deaths"] for s in ms) / len(ms):.1f} per 100)')
    for idx in mean_shift([(s['nx'], s['nz']) for s in dth], 2.5):
        cs = [dth[i] for i in idx]; pts = [(s['nx'], s['nz']) for s in cs]
        cx, cz = mean(p[0] for p in pts), mean(p[1] for p in pts)
        if len(cs) < MIN_N:
            P(f'   (group of {len(cs)}, below 8, not reported: {"/".join(cells_of(m, pts, 2))}, {side_words(G, m, cx, cz)})')
            continue
        e = ellipse(pts); cuv, shape = ellipse_uv(m, e)
        inside = [s for s in allm if (lambda dx, dz, ca, sa: ((dx * ca + dz * sa) / e[2]) ** 2 + ((-dx * sa + dz * ca) / e[3]) ** 2 <= 1)(s['nx'] - e[0], s['nz'] - e[1], math.cos(e[4]), math.sin(e[4]))]
        sid = f'{code}-deaths-{cells_of(m, pts, 1)[0].lower()}'
        nums = dict(n=len(cs), deaths=sum(s['deaths'] for s in cs), top6_n=sum(s['grp'] == 'top' for s in cs), rest_n=sum(s['grp'] == 'rest' for s in cs),
                    clans=len(set(s['team'] for s in cs)), games=len(set(s['game'] for s in cs)), share_of_map_death_smokes_pct=round(100 * len(cs) / len(dth), 1),
                    all_smokes_in_ellipse_n=len(inside), deaths_per_100_in_ellipse=round(100 * mean(s['deaths'] for s in inside), 1),
                    map_deaths_per_100_all_classes=round(100 * sum(s['deaths'] for s in allm) / len(allm), 1),
                    behind_by_50_n=sum(s['score_diff'] <= -50 for s in cs), enemy_radar_reached_n=sum(s['radar_on_us'] > 0 for s in cs), game_lost_n=sum(not s['win'] for s in cs),
                    destroyer_smoke_n=sum(s['cls'] == 'destroyer' for s in cs), cells='/'.join(cells_of(m, pts, 3)), median_time_s=round(med(s['el'] for s in cs)),
                    ships=', '.join(f'{a} {b}' for a, b in C(s['ship'] for s in cs).most_common(4)), radius_km_long=round(e[2] / KM, 1), radius_km_short=round(e[3] / KM, 1))
        lab = LABELS.get(sid, f'{side_words(G, m, cx, cz)}, cells {nums["cells"]}')
        spots.append(dict(id=sid, map=m, kind='deaths', label=lab, subject='smokes with a death in them, all classes', parent=None, centre_uv=cuv, shape=shape, numbers=nums, small_n=len(cs) < SOLID_N,
                          links=[s['link'] for s in sorted(cs, key=lambda s: math.hypot(s['nx'] - cx, s['nz'] - cz))[:3]],
                          notes='Mean-shift cluster (2.5 km) of the centres of smokes, any class, in which the smoker or a covered teammate was lost. The ellipse is 2 standard deviations. '
                                'deaths_per_100_in_ellipse counts every smoke laid inside the ellipse. Association only: deaths go with being behind and with enemy radar (Module 5).'
                                + (' Wide: read it as a zone.' if e[2] / KM > 6 else '')))
        P(f'   DEATHS {sid}: {lab} | centre uv {cuv} radii {nums["radius_km_long"]} x {nums["radius_km_short"]} km | {len(cs)} smokes with a death ({nums["deaths"]} deaths; Top 6 {nums["top6_n"]}, Rest {nums["rest_n"]}; {nums["clans"]} clans) = {nums["share_of_map_death_smokes_pct"]}% of the map '
          f'| all smokes in the ellipse {len(inside)}: {nums["deaths_per_100_in_ellipse"]} deaths/100 (map {nums["map_deaths_per_100_all_classes"]}) | behind by 50+ {nums["behind_by_50_n"]}, enemy radar reached {nums["enemy_radar_reached_n"]}, game lost {nums["game_lost_n"]} | {nums["ships"]} | median {clock(nums["median_time_s"])}')
    zr = [r for r in CELLS if r['map'] == m and r['kind'] == 'zone' and r['rated']]
    P('   destroyer-smoke death rate by cap zone (cells.json): ' + ', '.join(f'{r["name"]} {r["deaths_per_100"]} (n {r["n"]})' for r in zr))
    cr = sorted([r for r in CELLS if r['map'] == m and r['kind'] == 'cell' and r['rated']], key=lambda r: -r['deaths_per_100'])[:3]
    P('   highest destroyer-smoke death rate by rated cell (cells.json): ' + ', '.join(f'{r["name"]} {r["deaths_per_100"]} (n {r["n"]}{"*" if r["small_n"] else ""})' for r in cr))

    # ---- PN and example pool
    pn = [s for s in ms if s['is_pn']]
    P(f' PN destroyer smokes on this map: {len(pn)}' + (' | ' + '; '.join(f'{s["ship"]} {s["ncell_name"]} {clock(s["el"])} {round(s["conc"]):,}' for s in pn) if pn else ''))
    P(' EXAMPLE POOL (Top 6): signature examples are listed above; early and radar examples are listed under their clusters.')

# ---------- write
os.makedirs(os.path.join(ATLAS, 'maps'), exist_ok=True)
maps_meta = []
for title in MAP_ORDER:
    mm = MAPS[title]
    for ext in ('.png', '.webp'):
        src = os.path.join(MAP_SRC, mm['image'].replace('.png', ext)); dst = os.path.join(ATLAS, 'maps', os.path.basename(src))
        if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src): shutil.copyfile(src, dst)
    maps_meta.append(dict(title=title, file=mm['image'], webp=mm['image'].replace('.png', '.webp'), map_id=mm['map'], width_px=mm['width'], height_px=mm['height'],
                          size_km=mm['space_size'] * WU / 1000, km_per_grid_cell=mm['space_size'] * WU / 10000, transform=NORM_NOTE[title],
                          own_spawn='bottom-left' if title in DIAGONAL else 'bottom'))
json.dump(maps_meta, open(os.path.join(ATLAS, 'maps', 'maps.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump(dict(batch=BATCH_NAME, frame=FRAME, maps=caps_out), open(os.path.join(ATLAS, 'caps.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
ids = [s['id'] for s in spots]; assert len(ids) == len(set(ids)), [i for i, n in C(ids).items() if n > 1]
json.dump(dict(batch=BATCH_NAME, frame=FRAME,
               rules=dict(min_n=MIN_N, small_n='8 to 14', interval='95%, resampling clans', wording='association, not cause',
                          placebo='Six Rest clans standing in as the top group pass 2.5 signature spots on average, so 2 to 3 of the spots are the kind any group shows.'),
               spots=spots), open(os.path.join(ATLAS, 'spots.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
P(''); P('records by kind:', dict(C(s['kind'] for s in spots)), '| total', len(spots))
open(os.path.join(ATLAS, 'tables.txt'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
print('\n'.join(OUT))
