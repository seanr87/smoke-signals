# A4. Counter-smokes: geometry against the smoke they answer, and which ones pay.
# Counter-smoke = destroyer smoke whose batch field counter_smoke_of names an enemy smoke (same definition as round 3 module 5:
# laid within 45 s of an enemy smoke; lookups match on game + smoke id).
# Line of fire of the enemy smoke = direction from the enemy smoke's centre to the damage-weighted mean position of the ships it hit
# (positions at the moment the enemy smoke was fully laid). Fallback when it hit nobody with a known position: direction to the mean
# position of our ships (the enemy smoke's opponents) at that same moment.
# Angle = angle at the enemy smoke between that line and the line to our counter-smoke. Bands fixed before looking at outcomes:
# head-on under 30 degrees, oblique 30 to 60, flanking over 60.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
L = []; P = lambda *a: L.append(' '.join(str(x) for x in a))
J = {}
byid = {(s['game'], s['id']): s for s in S}
CS = []
for s in DD:
    if not s['counter_of']: continue
    e = byid.get((s['game'], s['counter_of']))
    if e and e['team'] != s['team']: s['ans'] = e; CS.append(s)
P('destroyer counter-smokes', sum(1 for s in DD if s['counter_of']), '| matched to an enemy smoke', len(CS), '| Top 6 / Rest', len(TOPS(CS)), len(RESTS(CS)), '| answered smoke class', dict(C(s['ans']['cls'] for s in CS)))
def raw(e, nx, nz): return norm(e['map'], e['side'], nx, nz)  # norm is its own inverse
def ang(ax, az, bx, bz):
    d = math.hypot(ax, az) * math.hypot(bx, bz)
    return math.degrees(math.acos(max(-1, min(1, (ax * bx + az * bz) / d)))) if d else None
for s in CS:
    e = s['ans']
    tg = [(t['dmg'], raw(e, t['nx'], t['nz'])) for t in e['targets'] if t.get('nx') is not None and t['dmg'] > 0]
    src = None
    if tg:
        w = sum(d for d, _ in tg); tx = sum(d * p[0] for d, p in tg) / w; tz = sum(d * p[1] for d, p in tg) / w; src = 'targets'
    else:
        en = [raw(e, c['nx'], c['nz']) for c in e['cast'] if c['how'] == 'enemy']
        if en: tx = mean(p[0] for p in en); tz = mean(p[1] for p in en); src = 'our ships'
    s['lof_src'] = src
    vx, vz = s['x'] - e['x'], s['z'] - e['z']
    s['dist_m'] = math.hypot(vx, vz) * WU
    s['gap_m'] = min(math.hypot(a - c, b - d) for a, b in s['path'] for c, d in e['path']) * WU   # nearest puff centres
    s['delay_s'] = s['el'] - e['el']
    s['same_cap'] = s['near_cap'] == e['near_cap']
    s['angle'] = ang(tx - e['x'], tz - e['z'], vx, vz) if src else None
    s['band'] = None if s['angle'] is None else 'head-on (under 30)' if s['angle'] < 30 else 'oblique (30-60)' if s['angle'] < 60 else 'flanking (over 60)'
    s['tgt_dist_m'] = math.hypot(tx - e['x'], tz - e['z']) * WU if src else None
    # bearing in our own frame: how far forward (toward the enemy spawn) and sideways the answered smoke lies from our counter-smoke
    enx, enz = norm(s['map'], s['side'], e['x'], e['z'])
    s['ans_fwd_m'] = forward(s['map'], enx - s['nx'], enz - s['nz'])
    s['ans_side_m'] = math.sqrt(max(0, s['dist_m'] ** 2 - s['ans_fwd_m'] ** 2))
    s['bearing'] = math.degrees(math.atan2(s['ans_side_m'], s['ans_fwd_m']))   # 0 = dead ahead, 90 = abeam, 180 = behind us
    s['bear_band'] = 'ahead (under 30 off our forward line)' if s['bearing'] < 30 else 'off the bow (30-60)' if s['bearing'] < 60 else 'abeam or behind (60+)'
    s['win'] = s['conc'] > e['conc']
    s['ans_conc'] = e['conc']; s['ans_deaths'] = e['deaths']
    tg2 = [(t['dmg'], raw(e, t['nx'], t['nz'])) for t in e['targets'] if t.get('nx') is not None and t['dmg'] > 0 and t.get('eid') != s['smoker_eid']]
    s['angle_x'] = None
    if tg2:
        w = sum(d for d, _ in tg2); s['angle_x'] = ang(sum(d * p[0] for d, p in tg2) / w - e['x'], sum(d * p[1] for d, p in tg2) / w - e['z'], vx, vz)
    s['band_x'] = None if s['angle_x'] is None else 'head-on (under 30)' if s['angle_x'] < 30 else 'oblique (30-60)' if s['angle_x'] < 60 else 'flanking (over 60)'
    s['we_targeted'] = any(t.get('eid') == s['smoker_eid'] for t in e['targets'])
USE = [s for s in CS if s['angle'] is not None]
P('pairs with a usable line of fire', len(USE), 'of', len(CS), '| from targets hit', sum(s['lof_src'] == 'targets' for s in CS), '| fallback to our ships', sum(s['lof_src'] == 'our ships' for s in CS), '| none', sum(s['lof_src'] is None for s in CS))
P('distance between centres (m): q25', round(q([s['dist_m'] for s in CS], .25)), 'median', round(med(s['dist_m'] for s in CS)), 'q75', round(q([s['dist_m'] for s in CS], .75)),
  '| gap between nearest puffs median', round(med(s['gap_m'] for s in CS)), '| delay median s', med(s['delay_s'] for s in CS), '| same cap %', r1(pct(CS, lambda s: s['same_cap'])))
P('angle off the line of fire: q25', r1(q([s['angle'] for s in USE], .25)), 'median', r1(med(s['angle'] for s in USE)), 'q75', r1(q([s['angle'] for s in USE], .75)), '| bands', dict(C(s['band'] for s in USE)))
P('bearing of the answered smoke from ours (0 = straight ahead): median', r1(med(s['bearing'] for s in CS)), '| bands', dict(C(s['bear_band'] for s in CS)))
P('target distance from the enemy smoke median m', round(med(s['tgt_dist_m'] for s in USE)), '| our smoker was itself a target of the enemy smoke', sum(s['we_targeted'] for s in CS))
CONC = avg('conc'); D100 = per100('deaths'); DS = per100('d_smoker'); WIN = share(lambda s: s['win']); ACONC = avg('ans_conc'); MARGIN = lambda ss: (CONC(ss) - ACONC(ss)) if len(ss) >= MIN_N else None
MARGIN.among = ALWAYS
STATS = [('concealed damage per counter-smoke', CONC, 0), ('deaths per 100', D100, 1), ('smoker died per 100', DS, 1), ('out-damaged the answered smoke %', WIN, 1), ('answered smoke concealed damage', ACONC, 0), ('margin (ours - theirs)', MARGIN, 0)]
def block(title, groups, base):
    rows = []
    for label, f in groups:
        ss = [s for s in base if f(s)]
        row = dict(group=label, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)), note=sm(len(ss)), clans=clan_dict(ss), clans_text=clan_counts(ss))
        for name, st, d in STATS: row[name] = one(ss, st, d)
        row['top6_vs_rest_conc'] = gap(ss, CONC, 0); row['top6_vs_rest_deaths'] = gap(ss, D100, 1)
        rows.append(row)
    P('\n' + title)
    P(md_table(['group', 'n (T6/Rest)', 'concealed damage [95%]', 'deaths per 100 [95%]', 'smoker died per 100', 'out-damaged answered % [95%]', 'answered smoke damage', 'margin [95%]', 'T6 / Rest damage (interval)', 'T6 / Rest deaths (interval)', 'note'],
               [[r['group'], f"{r['n']} ({r['n_top6']}/{r['n_rest']})", f"{fv(r[STATS[0][0]]['value'], '{:,.0f}')} [{fci(r[STATS[0][0]], '{:,.0f}')}]", f"{fv(r[STATS[1][0]]['value'])} [{fci(r[STATS[1][0]], '{:.1f}')}]", fv(r[STATS[2][0]]['value']),
                 f"{fv(r[STATS[3][0]]['value'])} [{fci(r[STATS[3][0]], '{:.1f}')}]", fv(r[STATS[4][0]]['value'], '{:,.0f}'), f"{fv(r[STATS[5][0]]['value'], '{:+,.0f}')} [{fci(r[STATS[5][0]], '{:+,.0f}')}]",
                 f"{fv(r['top6_vs_rest_conc']['top6'], '{:,.0f}')} / {fv(r['top6_vs_rest_conc']['rest'], '{:,.0f}')} ({fci(r['top6_vs_rest_conc'], '{:+,.0f}')})",
                 f"{fv(r['top6_vs_rest_deaths']['top6'])} / {fv(r['top6_vs_rest_deaths']['rest'])} ({fci(r['top6_vs_rest_deaths'])})", r['note']] for r in rows]))
    for r in rows: P('  clans:', r['group'], '|', r['clans_text'])
    return rows
J['overall'] = block('All matched counter-smokes', [('all', ALWAYS), ('Top 6', lambda s: s['grp'] == 'top'), ('Rest', lambda s: s['grp'] == 'rest')], CS)
BANDS = ['head-on (under 30)', 'oblique (30-60)', 'flanking (over 60)']
J['by_angle'] = block('By angle off the enemy smoke\'s line of fire (usable pairs)', [(b, lambda s, b=b: s['band'] == b) for b in BANDS], USE)
J['by_angle_targets_only'] = block('Same, only pairs where the line of fire comes from ships the enemy smoke actually hit', [(b, lambda s, b=b: s['band'] == b) for b in BANDS], [s for s in USE if s['lof_src'] == 'targets'])
J['by_angle_excl_self'] = block('Check: line of fire from ships hit, leaving out our own counter-smoking destroyer', [(b, lambda s, b=b: s['band_x'] == b) for b in BANDS], [s for s in CS if s['angle_x'] is not None])
J['by_angle_2'] = block('Two-way split at 45 degrees', [('under 45', lambda s: s['angle'] < 45), ('45 and over', lambda s: s['angle'] >= 45)], USE)
fl = [s for s in USE if s['band'] == BANDS[2]]; ho = [s for s in USE if s['band'] == BANDS[0]]
cmp_ = []
for a_l, a, b_l, b in (('flanking', fl, 'head-on', ho), ('flanking', fl, 'not flanking', [s for s in USE if s['band'] != BANDS[2]]), ('45 and over', [s for s in USE if s['angle'] >= 45], 'under 45', [s for s in USE if s['angle'] < 45])):
    for name, st, d in STATS:
        x = diff2(a, b, st, d); x.update(a_group=a_l, b_group=b_l, stat=name); cmp_.append(x)
    for g, f in (('Top 6', TOPS), ('Rest', RESTS)):
        for name, st, d in STATS[:2]:
            x = diff2(f(a), f(b), st, d); x.update(a_group=f'{a_l}, {g}', b_group=f'{b_l}, {g}', stat=name); cmp_.append(x)
P('\nDifferences (a - b)')
P(md_table(['a', 'b', 'stat', 'a (n)', 'b (n)', 'diff', 'interval'], [[x['a_group'], x['b_group'], x['stat'], f"{fv(x['a'], '{:,.1f}')} ({x['n_a']})", f"{fv(x['b'], '{:,.1f}')} ({x['n_b']})", fv(x['diff'], '{:+,.1f}'), fci(x, '{:+,.1f}')] for x in cmp_]))
J['angle_differences'] = cmp_
J['by_distance'] = block('By distance between the two smokes (centre to centre)', [('under 6 km', lambda s: s['dist_m'] < 6000), ('6-9 km', lambda s: 6000 <= s['dist_m'] < 9000), ('9-12 km', lambda s: 9000 <= s['dist_m'] < 12000), ('12 km+', lambda s: s['dist_m'] >= 12000)], CS)
J['by_bearing'] = block('By where the answered smoke lies from our counter-smoke (own frame)', [(b, lambda s, b=b: s['bear_band'] == b) for b in ('ahead (under 30 off our forward line)', 'off the bow (30-60)', 'abeam or behind (60+)')], CS)
J['by_delay'] = block('By delay after the enemy smoke', [('0-10 s', lambda s: s['delay_s'] <= 10), ('11-25 s', lambda s: 10 < s['delay_s'] <= 25), ('26-45 s', lambda s: s['delay_s'] > 25)], CS)
J['by_cap'] = block('Same cap or not', [('same cap as the answered smoke', lambda s: s['same_cap']), ('different cap', lambda s: not s['same_cap'])], CS)
J['by_habit'] = block('By habit of the counter-smoking ship', [(h, lambda s, h=h: s['habit'] == h) for h in ('flank smoke lines', 'cap sitters', 'other')], CS)
J['by_cover'] = block('By what the counter-smoke covers', [('radar cruiser inside', lambda s: s['cover3'] == 'radar cruiser inside'), ('any cruiser covered', lambda s: s['cr_any']), ('no cruiser', lambda s: not s['cr_any'])], CS)
J['by_answered'] = block('By the class of the answered smoke', [('answers a destroyer smoke', lambda s: s['ans']['cls'] == 'destroyer'), ('answers a cruiser smoke', lambda s: s['ans']['cls'] == 'cruiser')], CS)
J['by_ship'] = block('By ship (8+)', [(sh, lambda s, sh=sh: s['ship'] == sh) for sh, n in C(s['ship'] for s in CS).most_common() if n >= MIN_N], CS)
J['by_map'] = block('By map (8+)', [(m, lambda s, m=m: s['map'] == m) for m, n in C(s['map'] for s in CS).most_common() if n >= MIN_N], CS)
# angle within habit (habit mix drives the return)
J['angle_within_habit'] = block('Angle bands within flank smoke lines', [(b, lambda s, b=b: s['band'] == b and s['habit'] == 'flank smoke lines') for b in BANDS], USE) + \
                          block('Angle bands within cap sitters', [(b, lambda s, b=b: s['band'] == b and s['habit'] == 'cap sitters') for b in BANDS], USE)
P('\nhabit mix by band:', {b: dict(C(s['habit'] for s in USE if s['band'] == b)) for b in BANDS})
P('angle band by group:', {g: dict(C(s['band'] for s in USE if s['grp'] == g)) for g in ('top', 'rest')})
J['band_share'] = gap(USE, share(lambda s: s['band'] == BANDS[2])); P('share flanking, T6 vs Rest:', J['band_share'])
P('median angle T6', r1(med(s['angle'] for s in TOPS(USE))), 'Rest', r1(med(s['angle'] for s in RESTS(USE))), '| median distance T6', round(med(s['dist_m'] for s in TOPS(CS))), 'Rest', round(med(s['dist_m'] for s in RESTS(CS))))
gr = [s for s in CS if s['ship'] == 'Gearing' and s['grp'] == 'rest']; P('Rest Gearing counter-smokes:', clan_counts(gr), '| with a death:', clan_counts([s for s in gr if s['deaths']]), '| who died', dict(C('smoker' if d['is_smoker'] else d['cls'] for s in gr for d in s['dead'])))
P('rank correlation check: mean conc by angle tercile', [(round(a), round(b), round(mean(s['conc'] for s in v)), r1(100 * mean(s['deaths'] for s in v))) for a, b, v in
   [(v[0]['angle'], v[-1]['angle'], v) for v in (lambda z: [z[:len(z)//3], z[len(z)//3:2*len(z)//3], z[2*len(z)//3:]])(sorted(USE, key=lambda s: s['angle']))]])
J['summary'] = dict(n=len(CS), usable=len(USE), from_targets=sum(s['lof_src'] == 'targets' for s in CS), fallback=sum(s['lof_src'] == 'our ships' for s in CS), median_dist_m=round(med(s['dist_m'] for s in CS)),
                    median_angle=r1(med(s['angle'] for s in USE)), bands=dict(C(s['band'] for s in USE)), median_delay_s=med(s['delay_s'] for s in CS), same_cap_pct=r1(pct(CS, lambda s: s['same_cap'])))
# figure: counter-smoke positions relative to the enemy smoke, line of fire pointing up
fig = Fig(1120, 620, 'A4. Where counter-smokes sit relative to the smoke they answer', 'Enemy smoke at the centre, its line of fire pointing up. Each dot is one destroyer counter-smoke. Blue Top 6, orange Rest. Dot size = concealed damage. Ring = a ship died in it.')
cx, cy, sc = 320, 340, 250 / 15000
for rkm in (5, 10, 15):
    fig.add(f'<circle cx="{cx}" cy="{cy}" r="{rkm*1000*sc:.1f}" fill="none" stroke="{GRID}" stroke-width="1.2"/>' + T(cx + 4, cy - rkm * 1000 * sc - 3, f'{rkm} km', size=10, anchor='start'))
for a in (30, 60):
    for sgn in (-1, 1):
        fig.add(f'<line x1="{cx}" y1="{cy}" x2="{cx+sgn*260*math.sin(math.radians(a)):.1f}" y2="{cy-260*math.cos(math.radians(a)):.1f}" stroke="{MUTED}" stroke-width="0.8" stroke-dasharray="4 4"/>')
fig.add(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-262}" stroke="{INK}" stroke-width="1.5"/>' + T(cx, cy - 268, 'line of fire (toward the ships it hit)', size=11, fill=INK))
fig.add(T(cx + 70, cy - 235, 'head-on', size=10.5) + T(cx + 190, cy - 170, 'oblique', size=10.5) + T(cx + 255, cy + 20, 'flanking', size=10.5))
fig.add(f'<rect x="{cx-6}" y="{cy-6}" width="12" height="12" fill="{INK}"/>' + T(cx, cy + 22, 'enemy smoke', size=10.5, fill=INK))
for s in USE:
    # unsigned angle; alternate sides by the true cross-product sign so left/right is real
    e = s['ans']; r = min(s['dist_m'], 16500) * sc; a = math.radians(s['angle'])
    side = 1 if (s['x'] - e['x']) >= 0 else -1
    px, py = cx + side * r * math.sin(a), cy - r * math.cos(a)
    rad = 3 + min(9, math.sqrt(s['conc']) / 22)
    fig.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rad:.1f}" fill="{GROUP_COLOR[s["grp"]]}" opacity="0.55"/>' + (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rad+2:.1f}" fill="none" stroke="{INK}" stroke-width="1.4"/>' if s['deaths'] else ''))
fig.legend(40, 76, [('Top 6', BLUE), ('Rest', ORANGE)])
x0 = 640
fig.add(T(x0, 110, 'By angle off the line of fire', size=13, fill=INK, anchor='start', weight='600'))
y = 122
for title, key, fmt, vmax in (('Concealed damage per counter-smoke', STATS[0][0], '{:,.0f}', None), ('Deaths per 100', STATS[1][0], '{:.1f}', None), ('Out-damaged the answered smoke (%)', STATS[3][0], '{:.0f}%', 100)):
    fig.add(T(x0, y + 16, title, size=11.5, fill=INK, anchor='start')); y += 22
    y = bar_rows(fig, x0, y, 440, [(r['group'], r[key]['value'], f"n {r['n']}") for r in J['by_angle']], fmt=fmt, row_h=24, label_w=150, vmax=vmax) + 14
fig.add(T(x0, y + 10, 'Left or right of the line is drawn by east-west position only; the angle is what is measured.', size=10, anchor='start'))
fig.save(os.path.join(FIGS, 'a4-counter-smoke-geometry'))
out('out-a4', J, '\n'.join(L))
