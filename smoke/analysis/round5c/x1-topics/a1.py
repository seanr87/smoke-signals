# A1. Cap-contest destroyer smokes by cover, on the cap timeline and both death metrics; radar pressed from the smoke or not.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlib import *
CC = [s for s in DD if 'cap_contest' in s['tags']]
GROUPS = ['radar cruiser inside', 'non-radar cruiser inside', 'no cruiser', 'other']
ALLG = GROUPS + ['all cap-contest smokes']
STATS = [WE_C, WE_N, EN_C, EN_N, CONC, DIED, CAUGHT]
J = dict(n=len(CC), n_top6=len(TOPS(CC)), n_rest=len(RESTS(CC)), contested_is_nearest=sum(s['cap'] == s['near_cap'] for s in CC),
         died_base=len([s for s in CC if s['died_ok']]))
def base_of(g): return CC if g.startswith('all') else [s for s in CC if s['cover3'] == g]
def cells(ss): return {st.key: val(ss, st) for st in STATS}
def row_cells(c): return [fn_(c[st.key]['value'], c[st.key]['n'], st.fmt) if st.key.startswith(('we_', 'enemy_')) else fv(c[st.key]['value'], st.fmt) for st in STATS]
HDR = ['we took, contested cap % (n)', 'we took, nearest cap % (n)', 'enemy took, contested cap % (n)', 'enemy took, nearest cap % (n)', 'concealed damage per smoke', 'died per 100', 'caught per 100']
T1 = []
for g in ALLG:
    for sc, f in SCOPES:
        ss = f(base_of(g)); T1.append(dict(cover=g, scope=sc, n=len(ss), note=note(len(ss)), clans=clan_counts(ss), **cells(ss)))
J['by_cover'] = T1
T2 = [dict(cover=g, **{st.key: gap_tr(base_of(g), st) for st in STATS}) for g in ALLG]
J['top6_minus_rest'] = T2
T3 = []
for a, b in (('radar cruiser inside', 'no cruiser'), ('radar cruiser inside', 'non-radar cruiser inside')):
    for sc, f in SCOPES:
        A = f(base_of(a)); B = f(base_of(b))
        T3.append(dict(a=a, b=b, scope=sc, n_a=len(A), n_b=len(B), note=note(len(A), len(B)), **{st.key: gap_ab(A, B, st) for st in STATS}))
J['cover_gaps'] = T3
# who held the cap at activation (taking is easier on a neutral cap)
J['own_c'] = {g: {sc: dict(C(s['own_c'] for s in f(base_of(g)))) for sc, f in SCOPES} for g in GROUPS}
T3b = []
for g in ('radar cruiser inside', 'no cruiser'):
    for sc, f in SCOPES:
        ss = [s for s in f(base_of(g)) if s['own_c'] == 'neutral']
        T3b.append(dict(cover=g, scope=sc, n=len(ss), we_took_c=val(ss, WE_C), enemy_took_c=val(ss, EN_C), early=sum(s['early'] for s in ss)))
J['neutral_cap_only'] = T3b
T3c = [dict(scope=sc, **{st.key: gap_ab([s for s in f(base_of('radar cruiser inside')) if s['own_c'] == 'neutral'], [s for s in f(base_of('no cruiser')) if s['own_c'] == 'neutral'], st) for st in (WE_C, EN_C)}) for sc, f in SCOPES]
J['neutral_cap_gaps'] = T3c
# radar pressed from the smoke, among radar cruiser inside
RC = base_of('radar cruiser inside')
PR = (('radar pressed from the smoke', True), ('not pressed', False))
T4 = []
for lab, fl in PR:
    for sc, f in SCOPES:
        ss = f([s for s in RC if s['radar_pressed'] == fl]); T4.append(dict(pressed=lab, scope=sc, n=len(ss), note=note(len(ss)), by_cruiser=sum(s['radar_pressed_by_ca'] for s in ss), clans=clan_counts(ss), **cells(ss)))
J['pressed'] = T4
T5 = []
for sc, f in SCOPES:
    A = f([s for s in RC if s['radar_pressed']]); B = f([s for s in RC if not s['radar_pressed']])
    T5.append(dict(scope=sc, n_a=len(A), n_b=len(B), note=note(len(A), len(B)), **{st.key: gap_ab(A, B, st) for st in STATS}))
J['pressed_gaps'] = T5
T6 = [dict(pressed=lab, **{st.key: gap_tr([s for s in RC if s['radar_pressed'] == fl], st) for st in STATS}) for lab, fl in PR]
J['pressed_top6_minus_rest'] = T6
# wider reading: a cruiser that was inside this smoke pressed radar at some time while the smoke stood (in the smoke or after leaving it)
for s in RC:
    ins = {p['eid'] for p in s['shelter'] if p['how'] == 'inside' and p['cls'] == 'cruiser'}
    s['ca_pressed_window'] = any(r['entity_id'] in ins and s['e0'] - 1 <= r['elapsed_s'] <= s['end'] + 1 for r in TL(s['game']).activations('radar', team=s['team']))
PW = (('a cruiser from inside pressed radar while the smoke stood', True), ('no such press', False))
T7 = []
for lab, fl in PW:
    for sc, f in SCOPES:
        ss = f([s for s in RC if s['ca_pressed_window'] == fl]); T7.append(dict(pressed=lab, scope=sc, n=len(ss), note=note(len(ss)), clans=clan_counts(ss), **cells(ss)))
J['pressed_wide'] = T7
T8 = []
for sc, f in SCOPES:
    A = f([s for s in RC if s['ca_pressed_window']]); B = f([s for s in RC if not s['ca_pressed_window']])
    T8.append(dict(scope=sc, n_a=len(A), n_b=len(B), note=note(len(A), len(B)), **{st.key: gap_ab(A, B, st) for st in STATS}))
J['pressed_wide_gaps'] = T8
J['pressed_share'] = gap_tr(RC, Stat('p', 'pressed %', lambda ss: 100.0 * sum(s['radar_pressed'] for s in ss) / len(ss) if ss else None, len))

rcT, rcR = find(T1, cover='radar cruiser inside', scope='Top 6'), find(T1, cover='radar cruiser inside', scope='Rest')
ncT, ncR = find(T1, cover='no cruiser', scope='Top 6'), find(T1, cover='no cruiser', scope='Rest')
gT, gR, gA = find(T3, b='no cruiser', scope='Top 6'), find(T3, b='no cruiser', scope='Rest'), find(T3, b='no cruiser', scope='All')
pT, pR, pA = find(T5, scope='Top 6'), find(T5, scope='Rest'), find(T5, scope='All'); wA = find(T8, scope='All')
t2r, t2n = find(T2, cover='radar cruiser inside'), find(T2, cover='no cruiser')
def pc(x): return fv(x, '{:.0f}%')
def more(d, a='more', b='fewer'): return a if (d['diff'] or 0) > 0 else b
M = ['### A1. Cap-contest smokes by cover, and radar pressed from the smoke', '']
M.append(f"**Answer:** On the cap timeline, the Rest took the contested cap after {pc(rcR['we_took_c']['value'])} of their smokes with a radar cruiser inside against "
         f"{pc(ncR['we_took_c']['value'])} with no cruiser (gap {clear_word(gR['we_took_c'])}); the Top 6 took it after {pc(rcT['we_took_c']['value'])} against {pc(ncT['we_took_c']['value'])} "
         f"(gap {clear_word(gT['we_took_c'])}). So round 5's \"76% vs 13% for the Rest, no difference for the Top 6\" "
         f"{'holds on the timeline' if gR['we_took_c']['clear'] and not gT['we_took_c']['clear'] else 'does not hold on the timeline'}; on the nearest cap it is {pc(rcR['we_took_n']['value'])} vs {pc(ncR['we_took_n']['value'])} (Rest) and {pc(rcT['we_took_n']['value'])} vs {pc(ncT['we_took_n']['value'])} (Top 6). "
         f"A radar cruiser inside went with more concealed damage ({fdiff(gA['conc'], '{:+,.0f}')}) and no clear change in deaths (died {fdiff(gA['died100'])}, caught {fdiff(gA['caught100'])} per 100). "
         f"Radar pressed from the smoke is rare here: {find(T4, pressed='radar pressed from the smoke', scope='All')['n']} of {len(RC)} smokes, with no death on either metric, too few to split by group. "
         f"On the wider reading (the cruiser inside pressed radar at some time while the smoke stood, {wA['n_a']} smokes) a press went with concealed damage {fdiff(wA['conc'], '{:+,.0f}')}, "
         f"we took the contested cap {fdiff(wA['we_took_c'])}, died {fdiff(wA['died100'])} and caught {fdiff(wA['caught100'])} per 100.")
M.append('')
M.append(f"**Numbers:** {len(CC)} destroyer smokes carry the `cap_contest` tag ({len(TOPS(CC))} Top 6, {len(RESTS(CC))} Rest). The contested cap and the nearest cap are the same cap in "
         f"{J['contested_is_nearest']} of them. Cap results: an owner change on that cap between activation and 60 s after the smoke dispersed; (n) = smokes where the result could happen "
         f"(the cap was not already that side's). {DIED_NOTE} Here that removes {len(CC) - J['died_base']} smoke(s) from the died rates. Under 8 = too few, no rate.")
M.append('')
M.append('Table 1. By cover and group.')
M.append(md_table(['cover', 'group', 'n'] + HDR + ['note'], [[x['cover'], x['scope'], x['n']] + row_cells(x) + [x['note']] for x in T1]))
M.append('')
M.append('"other" is a footnote row: a cruiser screened but none inside, or a non-radar cruiser inside next to a radar ship of another class.')
M.append('')
M.append('Table 2. Top 6 minus Rest inside each cover group (difference, 95% interval; * = clear).')
M.append(md_table(['cover'] + [st.label for st in STATS], [[x['cover']] + [fdiff(x[st.key], st.sfmt) for st in STATS] for x in T2]))
M.append('')
M.append('Table 3. The gap inside each group: one kind of cover minus another (difference, 95% interval; * = clear).')
M.append(md_table(['gap', 'group', 'n a / n b'] + [st.label for st in STATS] + ['note'],
                  [[f"{x['a']} minus {x['b']}", x['scope'], f"{x['n_a']} / {x['n_b']}"] + [fdiff(x[st.key], st.sfmt) for st in STATS] + [x['note']] for x in T3]))
M.append('')
M.append('Table 3b. Like with like: only smokes whose contested cap was neutral at activation (a neutral cap is easier to take).')
M.append(md_table(['cover', 'group', 'n (early)', 'we took, contested cap % (n)', 'enemy took, contested cap % (n)'],
                  [[x['cover'], x['scope'], f"{x['n']} ({x['early']})", fn_(x['we_took_c']['value'], x['we_took_c']['n']), fn_(x['enemy_took_c']['value'], x['enemy_took_c']['n'])] for x in T3b]))
M.append('')
M.append('Radar cruiser inside minus no cruiser on neutral caps: ' + '; '.join(f"{x['scope']}: we took {fdiff(x['we_took_c'])}, enemy took {fdiff(x['enemy_took_c'])}" for x in T3c) + '.')
M.append('')
M.append(f"Table 4. Cap-contest smokes with a radar cruiser inside ({len(RC)}): radar pressed from the smoke or not. \"Pressed\" = a ship of the smoking team pressed radar while standing in this smoke (radar log).")
M.append(md_table(['', 'group', 'n (pressed by a cruiser)'] + HDR + ['note'], [[x['pressed'], x['scope'], f"{x['n']} ({x['by_cruiser']})"] + row_cells(x) + [x['note']] for x in T4]))
M.append('')
M.append('Table 5. Pressed minus not pressed (difference, 95% interval; * = clear).')
M.append(md_table(['group', 'n pressed / not'] + [st.label for st in STATS] + ['note'], [[x['scope'], f"{x['n_a']} / {x['n_b']}"] + [fdiff(x[st.key], st.sfmt) for st in STATS] + [x['note']] for x in T5]))
M.append('')
M.append('Table 6. Top 6 minus Rest inside pressed and inside not pressed.')
M.append(md_table([''] + [st.label for st in STATS], [[x['pressed']] + [fdiff(x[st.key], st.sfmt) for st in STATS] for x in T6]))
M.append('')
M.append('Table 7. Wider reading, because Table 4 is so thin: a cruiser that was inside this smoke pressed radar at some time while the smoke stood, whether the log places the press in this smoke or not (the cruiser had often moved out, or the press was at the smoke edge).')
M.append(md_table(['', 'group', 'n'] + HDR + ['note'], [[x['pressed'], x['scope'], x['n']] + row_cells(x) + [x['note']] for x in T7]))
M.append('')
M.append('Table 8. Wider reading: press minus no press (difference, 95% interval; * = clear).')
M.append(md_table(['group', 'n press / none'] + [st.label for st in STATS] + ['note'], [[x['scope'], f"{x['n_a']} / {x['n_b']}"] + [fdiff(x[st.key], st.sfmt) for st in STATS] + [x['note']] for x in T8]))
M.append('')
ps = J['pressed_share']
M.append(f"Radar was pressed from the smoke in {pc(ps['top6'])} of the Top 6's {ps['n_top6']} such smokes and {pc(ps['rest'])} of the Rest's {ps['n_rest']} (gap interval {fci(ps)}).")
M.append('')
M.append(f"**Top 6 or Shared:** Inside \"radar cruiser inside\" the Top 6 minus Rest gap is: we took the contested cap {fdiff(t2r['we_took_c'])}, enemy took it {fdiff(t2r['enemy_took_c'])}, "
         f"died per 100 {fdiff(t2r['died100'])}, caught per 100 {fdiff(t2r['caught100'])}. Inside \"no cruiser\": {fdiff(t2n['we_took_c'])}, {fdiff(t2n['enemy_took_c'])}, {fdiff(t2n['died100'])}, {fdiff(t2n['caught100'])}. "
         f"The extra concealed damage with a radar cruiser inside is in both groups (Top 6 {fdiff(gT['conc'], '{:+,.0f}')}, Rest {fdiff(gR['conc'], '{:+,.0f}')}): Shared. "
         f"The Top 6 difference is how often they do it ({rcT['n']} of {len(TOPS(CC))} cap-contest smokes against {rcR['n']} of {len(RESTS(CC))}).")
M.append('')
M.append('**Clans:** radar cruiser inside: ' + find(T1, cover='radar cruiser inside', scope='All')['clans'] + '. Radar pressed from it: ' + find(T4, pressed='radar pressed from the smoke', scope='All')['clans'] + '.')
M.append('')
nr = [find(T1, cover='non-radar cruiser inside', scope=sc)['n'] for sc in ('All', 'Top 6', 'Rest')]
M.append(f"**Could not be done / proxy:** Non-radar cruiser inside has {nr[0]} smokes ({nr[1]} Top 6, {nr[2]} Rest): small n overall and too few inside a group wherever the table says so. "
         "The pressed split is small inside each group; read the direction only.")
M.append('')
M.append(f"**Verdict:** Keep (damage and deaths by cover). The cap line: {'Keep, reworded with the timeline numbers' if gR['we_took_c']['clear'] else 'Lead only: the Rest gap is not clear on the timeline'}. Radar pressed from the smoke: Lead (8 smokes; the wider reading is in Tables 7 and 8).")
M.append('')
o = old('out-a1.json'); orow = {r['group']: r for r in o['rows']}
CH = []
for g in GROUPS:
    for sc, k in (('Top 6', 'top6'), ('Rest', 'rest')):
        x = find(T1, cover=g, scope=sc); r = orow[g]
        CH.append(chg_row(f'{g}, {sc}: we took the nearest cap %', r['cap_taken_snapshot_pct']['split'][k], x['we_took_n']['value'], 'cap timeline (was snapshots)'))
        ep = r['enemy_prevented_pct']['split'][k]
        CH.append(chg_row(f'{g}, {sc}: enemy took the nearest cap %', None if ep is None else round(100 - ep, 1), x['enemy_took_n']['value'], 'cap timeline (was snapshots)'))
        CH.append(chg_row(f'{g}, {sc}: concealed damage', r['concealed_damage']['split'][k], x['conc']['value'], 'unchanged', '{:,.0f}'))
        CH.append(chg_row(f'{g}, {sc}: deaths per 100, now caught per 100', r['deaths_per_100']['split'][k], x['caught100']['value'], 'same list'))
        CH.append(chg_row(f'{g}, {sc}: deaths per 100, now died per 100', r['deaths_per_100']['split'][k], x['died100']['value'], 'new death metric'))
M.append('**Changed from round 5b:** round 5b did not redo this table, so the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a1.json`). "-" = too few there. The contested-cap columns and the pressed split are new.')
M.append('')
nun = sum(1 for r in CH if r[3] == 'unchanged'); CH = [r for r in CH if r[3] != 'unchanged']
M.append(md_table(['number', 'round 5b', 'round 5c', 'why'], CH))
M.append('')
M.append(f'{nun} other numbers are unchanged: concealed damage in every row, and caught per 100 (it is the same list as round 5 deaths).')
M.append('')
J['changed'] = CH
CHK = [['A1 n cap-contest smokes', 'a1.py', 'len(CC)', len(CC)],
       ['A1 Rest: radar cruiser inside vs no cruiser, we took the contested cap %', 'a1.py', "T1 / J['by_cover'][..]['we_took_c']", f"{rcR['we_took_c']['value']} vs {ncR['we_took_c']['value']}"],
       ['A1 Top 6: radar cruiser inside vs no cruiser, we took the contested cap %', 'a1.py', "T1 / J['by_cover'][..]['we_took_c']", f"{rcT['we_took_c']['value']} vs {ncT['we_took_c']['value']}"],
       ['A1 gap radar cruiser inside minus no cruiser, we took contested: Rest / Top 6', 'a1.py', "T3 / J['cover_gaps']", f"{fdiff(gR['we_took_c'])} / {fdiff(gT['we_took_c'])}"],
       ['A1 gap radar cruiser inside minus no cruiser, all: damage, died, caught', 'a1.py', "T3 / J['cover_gaps']", f"{fdiff(gA['conc'], '{:+,.0f}')}; {fdiff(gA['died100'])}; {fdiff(gA['caught100'])}"],
       ['A1 pressed minus not pressed, all: damage, died, caught', 'a1.py', "T5 / J['pressed_gaps']", f"{fdiff(pA['conc'], '{:+,.0f}')}; {fdiff(pA['died100'])}; {fdiff(pA['caught100'])}"]]
CHK.append(['A1 wider reading, press minus no press, all: damage, we took contested, died, caught', 'a1.py', "T8 / J['pressed_wide_gaps']", f"{fdiff(wA['conc'], '{:+,.0f}')}; {fdiff(wA['we_took_c'])}; {fdiff(wA['died100'])}; {fdiff(wA['caught100'])}"])
save('out-a1', J, '\n'.join(M), CHK)
