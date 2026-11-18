# A4. Counter-smokes: death rates by angle and for the "what pays" rows, both death metrics.
# Geometry and damage columns are those of round5b/part-a/a4.py (copied): counter-smoke = destroyer smoke whose batch field
# counter_smoke_of names an enemy smoke; line of fire of the enemy smoke = direction from its centre to the damage-weighted mean
# position of the ships it hit (fallback: mean position of our ships); angle = angle at the enemy smoke between that line and the
# line to our counter-smoke; bands head-on under 30, oblique 30 to 60, flanking over 60.
# One change: the delay after the enemy smoke uses the replay clock (e0), not the HUD clock (el).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlib import *
J = {}
byid = {(s['game'], s['id']): s for s in S}
CS = []
for s in DD:
    if not s['counter_of']: continue
    e = byid.get((s['game'], s['counter_of']))
    if e and e['team'] != s['team']: s['ans'] = e; CS.append(s)
def raw(e, nx, nz): return norm(e['map'], e['side'], nx, nz)
def ang(ax, az, bx, bz):
    d = math.hypot(ax, az) * math.hypot(bx, bz)
    return math.degrees(math.acos(max(-1, min(1, (ax * bx + az * bz) / d)))) if d else None
BANDS = ['head-on (under 30)', 'oblique (30-60)', 'flanking (over 60)']
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
    s['delay_s'] = s['e0'] - e['e0']; s['delay_old'] = s['el'] - e['el']
    s['angle'] = ang(tx - e['x'], tz - e['z'], vx, vz) if src else None
    s['band'] = None if s['angle'] is None else BANDS[0] if s['angle'] < 30 else BANDS[1] if s['angle'] < 60 else BANDS[2]
    enx, enz = norm(s['map'], s['side'], e['x'], e['z'])
    s['ans_fwd_m'] = forward(s['map'], enx - s['nx'], enz - s['nz'])
    s['ans_side_m'] = math.sqrt(max(0, s['dist_m'] ** 2 - s['ans_fwd_m'] ** 2))
    s['bearing'] = math.degrees(math.atan2(s['ans_side_m'], s['ans_fwd_m']))
    s['win'] = s['conc'] > e['conc']; s['ans_conc'] = e['conc']
USE = [s for s in CS if s['angle'] is not None]
dband = lambda d: '0-10' if d <= 10 else '11-25' if d <= 25 else '26-45'
J['summary'] = dict(n=len(CS), n_top6=len(TOPS(CS)), n_rest=len(RESTS(CS)), usable=len(USE), bands=dict(C(s['band'] for s in USE)), died_base=sum(s['died_ok'] for s in CS),
                    delay_band_moved=sum(dband(s['delay_s']) != dband(s['delay_old']) for s in CS), rates=death_rates(CS))
WIN = Stat('win', 'out-damaged the answered smoke %', lambda ss: 100.0 * sum(s['win'] for s in ss) / len(ss) if ss else None, len)
ACONC = Stat('ans_conc', 'answered smoke concealed damage', lambda ss: sum(s['ans_conc'] for s in ss) / len(ss) if ss else None, len, '{:,.0f}', '{:+,.0f}')
MARGIN = Stat('margin', 'margin (ours minus theirs)', lambda ss: sum(s['conc'] - s['ans_conc'] for s in ss) / len(ss) if ss else None, len, '{:+,.0f}', '{:+,.0f}')
DMG = [CONC, WIN, ACONC, MARGIN]; DTH = [DIED, CAUGHT, DIED_S, CAUGHT_S]
def row(label, ss):
    d = dict(group=label, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)), note=note(len(ss)), clans=clan_counts(ss), rates=death_rates(ss))
    for st in DMG + DTH: d[st.key] = val(ss, st, True)
    for st in (DIED, CAUGHT): d['tr_' + st.key] = gap_tr(ss, st)
    return d
T_ANGLE = [row(b, [s for s in USE if s['band'] == b]) for b in BANDS]
T_PAYS = [row('radar cruiser inside', [s for s in CS if s['cover3'] == 'radar cruiser inside']), row('Gearing', [s for s in CS if s['ship'] == 'Gearing']),
          row('flank-smoke-line ships', [s for s in CS if s['habit'] == 'flank smoke lines']), row('laid 11-25 s after the enemy smoke', [s for s in CS if 10 < s['delay_s'] <= 25]),
          row('6-9 km from the answered smoke', [s for s in CS if 6000 <= s['dist_m'] < 9000]), row('answered smoke within 30 degrees of straight ahead', [s for s in CS if s['bearing'] < 30]),
          row('all counter-smokes', CS), row('all, Top 6', TOPS(CS)), row('all, Rest', RESTS(CS))]
J['by_angle'] = T_ANGLE; J['what_pays'] = T_PAYS
fl = [s for s in USE if s['band'] == BANDS[2]]; ho = [s for s in USE if s['band'] == BANDS[0]]
T_DIFF = [dict(scope=sc, n_a=len(f(fl)), n_b=len(f(ho)), note=note(len(f(fl)), len(f(ho))), **{st.key: gap_ab(f(fl), f(ho), st) for st in [CONC, MARGIN] + DTH}) for sc, f in SCOPES]
J['flanking_minus_head_on'] = T_DIFF
# each "what pays" row against the other counter-smokes
PAYS_F = [('radar cruiser inside', lambda s: s['cover3'] == 'radar cruiser inside'), ('Gearing', lambda s: s['ship'] == 'Gearing'), ('flank-smoke-line ships', lambda s: s['habit'] == 'flank smoke lines'),
          ('laid 11-25 s after the enemy smoke', lambda s: 10 < s['delay_s'] <= 25), ('6-9 km from the answered smoke', lambda s: 6000 <= s['dist_m'] < 9000), ('answered smoke within 30 degrees of straight ahead', lambda s: s['bearing'] < 30)]
T_VS = [dict(group=lab, **{st.key: gap_ab([s for s in CS if f(s)], [s for s in CS if not f(s)], st) for st in [CONC] + DTH}) for lab, f in PAYS_F]
J['what_pays_vs_other'] = T_VS

def tab(rows):
    return md_table(['', 'n (Top 6 / Rest)', 'concealed damage [95%]', 'out-damaged answered %', 'answered smoke damage', 'margin [95%]', 'died per 100 [95%]', 'caught per 100 [95%]', 'smoker died / caught per 100', 'died: Top 6 / Rest (gap)', 'caught: Top 6 / Rest (gap)', 'note'],
                    [[x['group'], f"{x['n']} ({x['n_top6']} / {x['n_rest']})", fvci(x['conc'], '{:,.0f}'), fv(x['win']['value']), fv(x['ans_conc']['value'], '{:,.0f}'), fvci(x['margin'], '{:+,.0f}'), fvci(x['died100']), fvci(x['caught100']),
                      f"{fv(x['died_smoker100']['value'])} / {fv(x['caught_smoker100']['value'])}", f"{fv(x['tr_died100']['top6'])} / {fv(x['tr_died100']['rest'])} ({fci(x['tr_died100'])})",
                      f"{fv(x['tr_caught100']['top6'])} / {fv(x['tr_caught100']['rest'])} ({fci(x['tr_caught100'])})", x['note']] for x in rows])
A = {x['group']: x for x in T_ANGLE}; Pz = {x['group']: x for x in T_PAYS}; dA = find(T_DIFF, scope='All'); dR = find(T_DIFF, scope='Rest'); al = Pz['all counter-smokes']
p = fv
M = ['### A4. Counter-smokes: death rates by angle and for the "what pays" rows', '']
M.append(f"**Answer:** Counter-smokes are costly on both metrics: {p(al['died100']['value'])} died and {p(al['caught100']['value'])} caught per 100, against {p(died100(DD))} and {p(caught100(DD))} for all destroyer smokes. "
         f"By angle, flanking counter-smokes lost {p(A[BANDS[2]]['died100']['value'])} died / {p(A[BANDS[2]]['caught100']['value'])} caught per 100 against {p(A[BANDS[0]]['died100']['value'])} / {p(A[BANDS[0]]['caught100']['value'])} head-on; "
         f"the flanking minus head-on gap is {fdiff(dA['died100'])} on died and {fdiff(dA['caught100'])} on caught, so over all clans angle {'separates' if dA['died100']['clear'] or dA['caught100']['clear'] else 'does not clearly separate'} deaths. "
         f"Inside the Rest the gap on died is {fdiff(dR['died100'])} ({clear_word(dR['died100'])}; only {dR['n_a']} flanking smokes) and on caught {fdiff(dR['caught100'])}. "
         f"Of the \"what pays\" rows, Gearing and flank-smoke-line counter-smokes returned the most damage and also the most deaths (Gearing {p(Pz['Gearing']['died100']['value'])} died / {p(Pz['Gearing']['caught100']['value'])} caught per 100).")
M.append('')
sm_ = J['summary']
M.append(f"**Numbers:** {sm_['n']} destroyer counter-smokes matched to the enemy smoke they answer ({sm_['n_top6']} Top 6, {sm_['n_rest']} Rest); {sm_['usable']} have a usable line of fire. {DIED_NOTE} "
         f"Here that removes {sm_['n'] - sm_['died_base']} smoke(s). Geometry and damage columns are computed as in round 5; the delay after the enemy smoke now uses the replay clock, which moves {sm_['delay_band_moved']} smoke(s) to another delay band.")
M.append('')
M.append('Table 1. By angle off the enemy smoke\'s line of fire.')
M.append(tab(T_ANGLE))
M.append('')
M.append('Table 2. Flanking minus head-on (difference, 95% interval; * = clear).')
M.append(md_table(['group', 'n flanking / head-on', 'concealed damage', 'margin', 'died per 100', 'caught per 100', 'smoker died per 100', 'smoker caught per 100', 'note'],
                  [[x['scope'], f"{x['n_a']} / {x['n_b']}", fdiff(x['conc'], '{:+,.0f}'), fdiff(x['margin'], '{:+,.0f}'), fdiff(x['died100']), fdiff(x['caught100']), fdiff(x['died_smoker100']), fdiff(x['caught_smoker100']), x['note']] for x in T_DIFF]))
M.append('')
M.append('Table 3. The "what pays" rows.')
M.append(tab(T_PAYS))
M.append('')
M.append('Table 4. Each "what pays" row minus the other counter-smokes (difference, 95% interval; * = clear).')
M.append(md_table(['', 'concealed damage', 'died per 100', 'caught per 100', 'smoker died per 100', 'smoker caught per 100'],
                  [[x['group'], fdiff(x['conc'], '{:+,.0f}'), fdiff(x['died100']), fdiff(x['caught100']), fdiff(x['died_smoker100']), fdiff(x['caught_smoker100'])] for x in T_VS]))
M.append('')
M.append(f"**Top 6 or Shared:** All counter-smokes, Top 6 against Rest: died {p(al['tr_died100']['top6'])} vs {p(al['tr_died100']['rest'])} ({fdiff(al['tr_died100'])}), caught {p(al['tr_caught100']['top6'])} vs {p(al['tr_caught100']['rest'])} ({fdiff(al['tr_caught100'])}). "
         f"Flanking minus head-on inside the Top 6: died {fdiff(find(T_DIFF, scope='Top 6')['died100'])}; inside the Rest: died {fdiff(find(T_DIFF, scope='Rest')['died100'])}. "
         f"Gearing counter-smokes: Top 6 {p(Pz['Gearing']['tr_died100']['top6'])} died / {p(Pz['Gearing']['tr_caught100']['top6'])} caught per 100 against Rest {p(Pz['Gearing']['tr_died100']['rest'])} / {p(Pz['Gearing']['tr_caught100']['rest'])} "
         f"(gaps {fci(Pz['Gearing']['tr_died100'])} and {fci(Pz['Gearing']['tr_caught100'])}; n {Pz['Gearing']['n_top6']} and {Pz['Gearing']['n_rest']}, small). The deaths that go with the high-damage rows are mostly the Rest's.")
M.append('')
M.append(f"**Clans:** flanking counter-smokes: {A[BANDS[2]]['clans']}. Gearing counter-smokes: {Pz['Gearing']['clans']}.")
M.append('')
M.append('**Could not be done / proxy:** Nothing missing. The line of fire is itself a proxy (where the enemy smoke\'s damage landed, or where our ships were when it hit nobody), as in round 5.')
M.append('')
M.append('**Verdict:** Keep the "what pays" rows with both death columns; angle and deaths: Lead only.')
M.append('')
o = old('out-a4.json'); CH = []
def oldrow(blk, g): return next(x for x in o[blk] if x['group'] == g)
PAIRS = [(BANDS[0], 'by_angle', BANDS[0]), (BANDS[1], 'by_angle', BANDS[1]), (BANDS[2], 'by_angle', BANDS[2]), ('radar cruiser inside', 'by_cover', 'radar cruiser inside'), ('Gearing', 'by_ship', 'Gearing'),
         ('flank-smoke-line ships', 'by_habit', 'flank smoke lines'), ('laid 11-25 s after the enemy smoke', 'by_delay', '11-25 s'), ('6-9 km from the answered smoke', 'by_distance', '6-9 km'),
         ('answered smoke within 30 degrees of straight ahead', 'by_bearing', 'ahead (under 30 off our forward line)'), ('all counter-smokes', 'overall', 'all')]
for lab, blk, og in PAIRS:
    x = A.get(lab) or Pz[lab]; r = oldrow(blk, og)
    CH.append(chg_row(f'{lab}: n', r['n'], x['n'], 'delay from the replay clock', '{}'))
    CH.append(chg_row(f'{lab}: concealed damage', r['concealed damage per counter-smoke']['value'], x['conc']['value'], 'delay from the replay clock (different smokes in the row)', '{:,.0f}'))
    CH.append(chg_row(f'{lab}: deaths per 100, now caught', r['deaths per 100']['value'], x['caught100']['value'], 'delay from the replay clock (different smokes in the row)'))
    CH.append(chg_row(f'{lab}: deaths per 100, now died', r['deaths per 100']['value'], x['died100']['value'], 'new death metric'))
    CH.append(chg_row(f'{lab}: smoker died per 100, now smoker caught', r['smoker died per 100']['value'], x['caught_smoker100']['value'], 'delay from the replay clock (different smokes in the row)'))
    CH.append(chg_row(f'{lab}: smoker died per 100, now smoker died', r['smoker died per 100']['value'], x['died_smoker100']['value'], 'new death metric'))
od = next(x for x in o['angle_differences'] if x['a_group'] == 'flanking' and x['b_group'] == 'head-on' and x['stat'] == 'deaths per 100')
CH.append(chg_row('flanking minus head-on, deaths per 100, now caught', f"{od['diff']:+.1f} ({od['lo']:+.1f} to {od['hi']:+.1f})", fdiff(dA['caught100']).replace(' *', ''), 'same list; interval now from diff_ci', '{}'))
CH.append(chg_row('flanking minus head-on, deaths per 100, now died', f"{od['diff']:+.1f} ({od['lo']:+.1f} to {od['hi']:+.1f})", fdiff(dA['died100']).replace(' *', ''), 'new death metric', '{}'))
nun = sum(1 for q_ in CH if q_[3] == 'unchanged'); CH = [q_ for q_ in CH if q_[3] != 'unchanged']
M.append('**Changed from round 5b:** round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a4.json`).')
M.append('')
M.append(md_table(['number', 'round 5b', 'round 5c', 'why'], CH))
M.append('')
M.append(f'{nun} other compared numbers are unchanged (n, concealed damage and the caught rates wherever the row holds the same smokes).')
M.append('')
J['changed'] = CH
CHK = [['A4 n counter-smokes, usable line of fire', 'a4.py', "len(CS), len(USE) / J['summary']", f"{len(CS)}, {len(USE)}"],
       ['A4 all counter-smokes: died / caught per 100', 'a4.py', "T_PAYS / J['what_pays'] row 'all counter-smokes'", f"{al['died100']['value']} / {al['caught100']['value']}"],
       ['A4 flanking: died / caught per 100; head-on: died / caught', 'a4.py', "T_ANGLE / J['by_angle']", f"{A[BANDS[2]]['died100']['value']} / {A[BANDS[2]]['caught100']['value']}; {A[BANDS[0]]['died100']['value']} / {A[BANDS[0]]['caught100']['value']}"],
       ['A4 flanking minus head-on: died / caught', 'a4.py', "T_DIFF / J['flanking_minus_head_on'] scope All", f"{fdiff(dA['died100'])} / {fdiff(dA['caught100'])}"],
       ['A4 Gearing counter-smokes: died / caught per 100', 'a4.py', "T_PAYS row 'Gearing'", f"{Pz['Gearing']['died100']['value']} / {Pz['Gearing']['caught100']['value']}"]]
save('out-a4', J, '\n'.join(M), CHK)
