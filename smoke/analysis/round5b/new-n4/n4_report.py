# Writes FINDINGS-N4.md, CHECK-N4.md and page1.json from out-c1/2/3.json (made by n4_c1.py, n4_c2.py, n4_c3.py).
import sys, os, json
OUT = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(OUT, n), encoding='utf-8'))
c1, c2, c3 = J('out-c1.json'), J('out-c2.json'), J('out-c3.json')
MAPORDER = ['Sleeping Giant', 'Hotspot', 'Mountain Range', 'Land of Fire', 'Loop', 'Okinawa', 'Sea of Fortune']
CHECK = []   # (number, script, where)
def ck(num, script, where): CHECK.append((num, script, where)); return num
def table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    return '\n'.join(out + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])
p0 = lambda x: '-' if x is None else f'{x:.0f}%'
km = lambda m: '-' if m is None else f'{m / 1000:.1f} km'
def civ(ci, f='{:+.0f}', clear=None):
    if ci[0] is None: return '-'
    star = (ci[0] * ci[1] > 0) if clear is None else clear
    return f'{f.format(ci[0])} to {f.format(ci[1])}' + (' *' if star else '')
def cikm(ci, clear): return civ([ci[0] / 1000, ci[1] / 1000], '{:+.1f}', clear)
def clans(d):
    f = lambda x: ', '.join(f'{k} {v}' for k, v in x.items()) or 'none'
    return f"Top 6: {f(d['top6'])} | Rest: {f(d['rest'])}"
def status(old, bug, new, interval=False):
    if old == bug == new: return 'unchanged'
    if old == bug: return 'clock fix'
    if interval: return 'same data, interval end moved (resampling redrawn)' + ('' if bug == new else '; then clock fix')
    return 'DIFFERS'
def la(claim):
    same = [f'{w} {o}' for w, o, b, n, s in CH[claim] if s == 'unchanged']; moved = [f'{w}: {o} -> {b} with the clock bug still in -> {n} corrected ({s})' for w, o, b, n, s in CH[claim] if s != 'unchanged']
    return f"{len(same)} of {len(CH[claim])} numbers unchanged (old -> new identical): " + ('; '.join(same) or 'none') + '. ' + ('Moved: ' + '; '.join(moved) + '. ' if moved else '')
L = []; W = L.append
ck_ = c1['clock']
CLK = (f"Clock fix: {len(ck_['games'])} games ran on a 15-minute clock, so rounds 3 to 5 read their {ck_['smokes']} smokes 300 s late. The library now corrects this: {ck_['now_early']} more smokes count as early "
       f"({ck_['now_early_dd']} destroyer smokes, {ck_['now_early_three']} of them by the three ships) and none stop being early. The middle column puts the bug back and reproduces the atlas; the right column is the corrected number, and layer B uses the corrected groups.")
CH = {1: [], 2: [], 3: []}
def arow(claim, what, old, new, interval=False, script='', where='', bug=None):
    bug = new if bug is None else bug
    st = status(old, bug, new, interval); CH[claim].append((what, old, bug, new, st))
    CHECK.append((f'{what}: {bug} (clock bug in) / {new} (corrected)', script, where + ('; A_bug' if bug != new else '')))
    return (what, old, bug, new, st)

W('# Round 5b, worker n4: the page 1 carry-over claims, re-tested\n')
W('Batch `output/20261117-230933` (smoke-signals 0.4.0): 1,547 smokes, 171 games, 30 clans. Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS (110 team-games); Rest = everyone else (232 team-games). '
  'Intervals are 95%, whole clans resampled; * = excludes zero. Minimum n 8; 8 to 14 is small n. Everything is association, not cause.\n')
W('Each claim is done in two layers. **Layer A** reruns the atlas / round 4 computation on the new batch (the smoke fields are identical, so it must give the same numbers). '
  '**Layer B** re-tests the claim with the new timelines: ship tracks every 2 s, the cap ownership timeline, and the radar log.\n')

# =========================================================== claim 1
P3 = c1['pops']['three ships early (round 3 population)']; PI = c1['pops']['early cruiser smoke, cruiser inside']; PS = c1['pops']['early cruiser smoke, cruiser screened']; PA = c1['pops']['all early destroyer smokes']
t3 = P3['B_top_rest']
W('### N4-1. Early smoke distance short of the cap\n')
W(f"**Answer:** Yes, it holds, and it holds on the ships as well as on the smoke outline. The destroyer was inside a cap when it pressed smoke in {P3['B_smoker_in_cap_act_pct'][0]:.0f}% of early Harugumo, Somers and Gearing smokes "
  f"and a typical {km(P3['B_smoker_near_edge_act_m'][0])} outside the nearest cap edge; the covered cruiser stayed a typical {km(P3['B_cruiser_near_edge_m'][0])} outside while the smoke stood. "
  f"The cap in question was usually still neutral ({P3['B_cap_state_contested']['neutral']:.0f}%), and somebody was capturing it while the smoke stood in {P3['B_invaded_cont']['anyone']:.0f}% of cases: the smoke is short of the cap, but the cap is live.\n")
W('**Numbers:**\n')
W('Layer A, same definition, new batch (early smokes by Harugumo, Somers and Gearing; the batch field is smoke edge to contested cap edge, averaged over the smoke\'s life):\n')
AB1 = c1['A_bug']
rows = [arow(1, 'Early smokes by the three ships (n)', '187', str(P3['n']), script='n4_c1.py', where='out-c1.json pops[three ships].n', bug=str(AB1['n'])),
        arow(1, 'Laid inside a cap', '14%', p0(P3['A_inside_cap_pct'][0]), script='n4_c1.py', where='pops[three ships].A_inside_cap_pct', bug=p0(AB1['inside_pct'])),
        arow(1, 'Median distance outside the cap edge', '1.8 km', km(P3['A_median_edge_m'][0]), script='n4_c1.py', where='pops[three ships].A_median_edge_m', bug=km(AB1['median_edge_m']))]
W(table(['Number', 'Atlas / round 4', 'New batch, clock bug still in', 'New batch, clock corrected', 'Status'], rows) + '\n\n' + CLK + '\n')
W(f"New interval for these two: inside a cap {civ(P3['A_inside_cap_pct'][1], '{:.0f}', False)}%, median distance {P3['A_median_edge_m'][1][0] / 1000:.1f} to {P3['A_median_edge_m'][1][1] / 1000:.1f} km ({P3['A_inside_cap_count']} of {P3['n']} smokes inside).\n")
W('Layer B, re-tested with ship tracks and the cap timeline. Four groups of early smokes; "early cruiser smoke" is the round 5 definition (any destroyer, first 5 minutes, covers a cruiser):\n')
def col(P):
    return [f"{P['n']} ({P['n_top']} / {P['n_rest']})",
            f"{p0(P['A_inside_cap_pct'][0])} ({civ(P['A_inside_cap_pct'][1], '{:.0f}', False)})", f"{km(P['A_median_edge_m'][0])}",
            f"{p0(P['B_smoker_in_cap_act_pct'][0])} ({civ(P['B_smoker_in_cap_act_pct'][1], '{:.0f}', False)})", f"{p0(P['B_smoker_in_cap_end_pct'][0])} ({civ(P['B_smoker_in_cap_end_pct'][1], '{:.0f}', False)})",
            f"{km(P['B_smoker_near_edge_act_m'][0])} ({P['B_smoker_near_edge_act_m'][1][0] / 1000:.1f} to {P['B_smoker_near_edge_act_m'][1][1] / 1000:.1f})",
            f"{km(P['B_smoker_near_edge_end_m'][0])} ({P['B_smoker_near_edge_end_m'][1][0] / 1000:.1f} to {P['B_smoker_near_edge_end_m'][1][1] / 1000:.1f})",
            f"{p0(P['B_smoker_own_side_act_pct'])}",
            f"{km(P['B_cruiser_near_edge_m'][0])} ({P['B_cruiser_near_edge_m'][1][0] / 1000:.1f} to {P['B_cruiser_near_edge_m'][1][1] / 1000:.1f}; n {P['n_cruiser_track']})",
            f"{p0(P['B_cruiser_ever_in_cap_pct'][0])} ({civ(P['B_cruiser_ever_in_cap_pct'][1], '{:.0f}', False)})", f"{p0(P['B_cruiser_mostly_in_cap_pct'])}",
            f"{P['B_cap_state_contested']['neutral']:.0f}% / {P['B_cap_state_contested']['ours']:.0f}% / {P['B_cap_state_contested']['theirs']:.0f}%",
            f"{P['B_invaded_cont']['us']:.0f}% / {P['B_invaded_cont']['enemy']:.0f}% / {P['B_invaded_cont']['nobody']:.0f}%"]
labs = ['Smokes (Top 6 / Rest)', 'Smoke outline inside a cap (batch field)', 'Smoke edge to contested cap edge, median (batch field)', 'Smoker inside a cap when it pressed smoke', 'Smoker inside a cap at the end of laying',
        'Smoker to nearest cap edge at activation, median', 'Smoker to nearest cap edge at the end of laying, median', 'Smoker on the own-spawn side of that cap at activation',
        'Covered cruiser to nearest cap edge while the smoke stood, median', 'Covered cruiser inside a cap at any time while the smoke stood', 'Covered cruiser inside a cap for most of that time',
        'Contested cap at activation: neutral / ours / theirs', 'Contested cap being captured while the smoke stood: by us / by the enemy / by nobody']
cols = [col(P) for P in (P3, PI, PS, PA)]
W(table(['Measure', 'Three ships, early (round 3 group)', 'Early cruiser smoke, cruiser inside', 'Early cruiser smoke, cruiser screened', 'All early destroyer smokes'], [[labs[i]] + [c[i] for c in cols] for i in range(len(labs))]) + '\n')
for i, lab in enumerate(labs): CHECK.append((f'N4-1 layer B row "{lab}"', 'n4_c1.py', 'out-c1.json pops[*] keys A_* and B_* (function block)'))
W(f"- The outline and the ships agree. Of the {P3['n_track']} three-ship smokes with a track, {P3['cross']['outline_out_smoker_out']} have both the outline and the smoker outside every cap, {P3['cross']['outline_in_smoker_in']} have both inside, "
  f"{P3['cross']['outline_out_smoker_in']} have the outline short but the smoker in a cap at the start or end of laying, and {P3['cross']['outline_in_smoker_out']} the reverse.")
W(f"- The smoker does not close on the cap while laying: it is nearer the cap at the end of laying in {P3['B_smoker_closer_at_end_pct']:.0f}% of smokes, about half. It travels a median {km(P3['B_smoker_moved_m'])} while laying and ends no nearer the cap than it started.")
W(f"- The cruiser sits further back than the destroyer: {km(P3['B_cruiser_near_edge_m'][0])} against {km(P3['B_smoker_near_edge_act_m'][0])}. Measured to the contested cap it is {km(P3['B_cruiser_cont_edge_m'])} (round 3 had 3.8 km from the one snapshot per smoke). "
  f"Only while it is actually inside the smoke: {km(P3['B_cruiser_in_smoke_near_edge_m'])}. In {P3['B_cruiser_ever_in_cap_pct'][0]:.0f}% of smokes a covered cruiser did enter a cap at some point before the smoke cleared (about 2.5 minutes), but it spent most of that time in a cap in only {P3['B_cruiser_mostly_in_cap_pct']:.0f}%.")
W(f"- Screened is the exception, as in round 5: when the cruiser is behind the smoke rather than in it, the smoke is nearer the cap ({p0(PS['A_inside_cap_pct'][0])} inside, smoker in a cap {p0(PS['B_smoker_in_cap_act_pct'][0])} at activation) and the cruiser is further away ({km(PS['B_cruiser_near_edge_m'][0])}).")
W(f"- Checks. Track position against the round 5 snapshot at the fully-laid moment, same smokes: median {c1['check_track_vs_snapshot']['median_m']:.0f} m apart, {c1['check_track_vs_snapshot']['within_300m_pct']:.0f}% within 300 m (n {c1['check_track_vs_snapshot']['n']}). "
  f"Smoker in a cap from the snapshot: {c1['check_snapshot_smoker_in_cap']['pct']:.0f}%, from the track at the end of laying: {P3['B_smoker_in_cap_end_pct'][0]:.0f}%. Cap owner at activation, timeline against the batch field: {P3['check_own_tl_vs_batch_agree_pct']:.0f}% the same. "
  f"My own outline distance from the laid path is within a median {P3['check_outline_min_vs_batch_median_abs_m']:.0f} m of the batch field and agrees on inside / outside for {P3['check_outline_inside_agree_pct']:.0f}% of smokes.\n")
W(f"**Top 6 or Shared:** Shared. Everyone lays the early smoke short. Outline inside a cap: Top 6 {p0(P3['A_top_rest_inside']['top'])} vs Rest {p0(P3['A_top_rest_inside']['rest'])} ({civ(P3['A_top_rest_inside']['ci'], clear=P3['A_top_rest_inside']['clear'])}); "
  f"smoker distance at activation {km(t3['smoker_near_edge_act']['top'])} vs {km(t3['smoker_near_edge_act']['rest'])} ({cikm(t3['smoker_near_edge_act']['ci'], t3['smoker_near_edge_act']['clear'])} km); "
  f"cruiser distance {km(t3['cruiser_near_edge']['top'])} vs {km(t3['cruiser_near_edge']['rest'])} ({cikm(t3['cruiser_near_edge']['ci'], t3['cruiser_near_edge']['clear'])} km). "
  f"One gap is clear, and it points the same way as the rule: the Top 6 smoker is inside a cap when it presses smoke even less often, {p0(t3['smoker_in_cap_act']['top'])} vs {p0(t3['smoker_in_cap_act']['rest'])} ({civ(t3['smoker_in_cap_act']['ci'], clear=t3['smoker_in_cap_act']['clear'])}); "
  f"on all early destroyer smokes {p0(PA['B_top_rest']['smoker_in_cap_act']['top'])} vs {p0(PA['B_top_rest']['smoker_in_cap_act']['rest'])} ({civ(PA['B_top_rest']['smoker_in_cap_act']['ci'], clear=PA['B_top_rest']['smoker_in_cap_act']['clear'])}). "
  f"By the end of laying the gap is gone ({p0(t3['smoker_in_cap_end']['top'])} vs {p0(t3['smoker_in_cap_end']['rest'])}, {civ(t3['smoker_in_cap_end']['ci'], clear=t3['smoker_in_cap_end']['clear'])}).\n")
W(f"**Clans:** the {P3['n']} three-ship early smokes: {clans(P3['clan_counts'])}. The {P3['B_smoker_in_cap_act_count']} with the smoker inside a cap at activation: {clans(P3['clan_counts_smoker_in_cap'])}.\n")
W(f"**Could not be done / proxy:** {sum(c1['excluded_no_track'].values()) and 'One smoke in the single-replay game (KSC against -BN-) has no own-team track for the smoker and is left out of layer B' or 'Nothing left out'} "
  f"({P3['n_track']} of {P3['n']}; cruiser tracks for {P3['n_cruiser_track']}, the rest cover no cruiser). The smoke shape is the final laid path, so \"inside the smoke\" is slightly generous while it is still being laid. "
  'The batch distance is to the contested cap; ship distances are given to the nearest cap, which is the stricter test of "short of a cap".\n')
W('**Verdict:** Keep\n')
W('**Changed from the atlas / round 4:**\n')
W('- Layer A: ' + la(1) + 'Why: same smoke fields, same computation.')
W(f"- Layer B (new, no old value unless noted): smoker inside a cap at activation {p0(P3['B_smoker_in_cap_act_pct'][0])} and at the end of laying {p0(P3['B_smoker_in_cap_end_pct'][0])} (outline: {p0(P3['A_inside_cap_pct'][0])}); smoker {km(P3['B_smoker_near_edge_act_m'][0])} then {km(P3['B_smoker_near_edge_end_m'][0])} outside the nearest cap (outline: {km(P3['A_median_edge_m'][0])}, +{(P3['B_smoker_near_edge_act_m'][0] - P3['A_median_edge_m'][0]) / 1000:.1f} km; "
  f"a ship is a point, the outline reaches about half a kilometre further); cruiser to the contested cap 3.8 km -> {km(P3['B_cruiser_cont_edge_m'])} (one snapshot -> average over the smoke's life); cruiser inside a cap 4% of partners at the snapshot -> {p0(P3['B_cruiser_mostly_in_cap_pct'])} of smokes for most of the time, {p0(P3['B_cruiser_ever_in_cap_pct'][0])} at any time. "
  'Why: better data (continuous tracks and cap timeline). The claim itself is unchanged.\n')

# =========================================================== claim 2
R = c2['rungs']; am = lambda k: R[k]['table']['All maps']; o = c2['of_inside']
W('### N4-2. Radar cruiser inside early destroyer smokes\n')
ins, used, lit, ldd = am('inside'), am('used'), am('lit'), am('lit_dd')
cap3, capA = c2['cap_three_ships']['rows'], c2['cap_all_early']['rows']
W(f"**Answer:** The headline stands: a radar cruiser is inside {p0(ins['top'])} of Top 6 early destroyer smokes against {p0(ins['rest'])} for the Rest. But the radar log shows what that cruiser does there: it ran its radar from the smoke in only about a third of those smokes, "
  f"and that share is the same for both groups ({p0(o['used']['top'])} vs {p0(o['used']['rest'])}). So the Top 6 difference is having the cruiser in the smoke, not pressing radar from it. "
  f"\"Inside goes with the cap being taken\" survives the cap timeline but at about half the size: {p0(capA['tl_near']['a'])} vs {p0(capA['tl_near']['b'])} on the nearest cap, not 58% vs 14%.\n")
W('**Numbers:**\n')
W('Layer A, same definition, new batch:\n')
xp = lambda d, g: f"{100 * d['x_' + g] / d['n_' + g]:.0f}%"   # percent from the counts (avoids rounding twice)
f2 = lambda d: f"{xp(d, 'top')} ({d['x_top']} of {d['n_top']}) vs {xp(d, 'rest')} ({d['x_rest']} of {d['n_rest']})"
sg, hs = R['inside']['table']['Sleeping Giant'], R['inside']['table']['Hotspot']; ts = c2['three_ships']['inside']; AB2 = c2['A_bug']
rows = [arow(2, 'All early destroyer smokes, radar cruiser inside', '60% (61 of 102) vs 35% (70 of 200)', f2(ins), script='n4_c2.py', where='out-c2.json rungs.inside.table[All maps]', bug=f2(AB2['all'])),
        arow(2, 'Gap', '+25', f"{ins['diff']:+.0f}", script='n4_c2.py', where='rungs.inside.table[All maps].diff', bug=f"{AB2['all']['diff']:+.0f}"),
        arow(2, 'Gap interval', '+13 to +36', civ(ins['ci'], clear=False), True, 'n4_c2.py', 'rungs.inside.table[All maps].ci', bug=civ(AB2['all']['ci'], clear=False)),
        arow(2, 'Sleeping Giant', '47% vs 59%', f"{xp(sg, 'top')} vs {xp(sg, 'rest')}", script='n4_c2.py', where='rungs.inside.table[Sleeping Giant]', bug=f"{xp(AB2['sg'], 'top')} vs {xp(AB2['sg'], 'rest')}"),
        arow(2, 'Hotspot', '87% vs 38%', f"{xp(hs, 'top')} vs {xp(hs, 'rest')}", script='n4_c2.py', where='rungs.inside.table[Hotspot]', bug=f"{xp(AB2['hs'], 'top')} vs {xp(AB2['hs'], 'rest')}"),
        arow(2, 'Harugumo, Somers, Gearing only', '82% vs 51%', f"{xp(ts, 'top')} vs {xp(ts, 'rest')}", script='n4_c2.py', where='three_ships.inside', bug=f"{xp(AB2['three'], 'top')} vs {xp(AB2['three'], 'rest')}"),
        arow(2, 'Three ships, gap interval', '+15 to +46', civ(ts['ci'], clear=False), True, 'n4_c2.py', 'three_ships.inside.ci', bug=civ(AB2['three']['ci'], clear=False)),
        arow(2, 'Cap won after: radar cruiser inside vs covered, not inside (three ships)', '58% (n 117) vs 14% (n 29)', f"{p0(cap3['batch_all']['a'])} (n {cap3['batch_all']['n_a']}) vs {p0(cap3['batch_all']['b'])} (n {cap3['batch_all']['n_b']})", script='n4_c2.py', where='cap_three_ships.rows.batch_all', bug=f"{p0(AB2['cap_three']['a'])} (n {AB2['cap_three']['n_a']}) vs {p0(AB2['cap_three']['b'])} (n {AB2['cap_three']['n_b']})"),
        arow(2, 'Cap taken, all early destroyer smokes: radar cruiser inside vs not', '61% (of 120) vs 31% (of 150)', f"{p0(capA['batch_takeable']['a'])} (of {capA['batch_takeable']['n_a']}) vs {p0(capA['batch_takeable']['b'])} (of {capA['batch_takeable']['n_b']})", script='n4_c2.py', where='cap_all_early.rows.batch_takeable', bug=f"{p0(AB2['cap_all']['a'])} (of {AB2['cap_all']['n_a']}) vs {p0(AB2['cap_all']['b'])} (of {AB2['cap_all']['n_b']})")]
W(table(['Number', 'Atlas / round 4', 'New batch, clock bug still in', 'New batch, clock corrected', 'Status'], rows) + '\n\n' + CLK + '\n')
W(f"Second way for the headline (counted straight from the raw list of ships in each smoke and the roster, not from the library flag): {c2['check_headline_second_way']['top']} and {c2['check_headline_second_way']['rest']} smokes. Same.\n")
W('Layer B, the ladder from the radar log. "Ran radar from it" = that cruiser activated radar while the smoke stood, with the smoke listed as the one it stood in, or with its position inside the smoke. All early destroyer smokes:\n')
def cell(d, g):
    n, x, fl = d['n_' + g], d['x_' + g], d['flag_' + g]
    if fl == 'too few': return f'{x} of {n} (too few)'
    return f"{100 * x / n:.0f}% ({x} of {n}{', small n' if fl else ''})"
def gap(d):
    if d['flag_top'] == 'too few' or d['flag_rest'] == 'too few': return '-'
    return f"{d['diff']:+.0f} ({civ(d['ci'], clear=d['clear'])})"
rows = [[R[k]['label'], cell(am(k), 'top'), cell(am(k), 'rest'), gap(am(k)), f"{c2['per_team_game'][k]['top']:.2f} vs {c2['per_team_game'][k]['rest']:.2f} ({civ(c2['per_team_game'][k]['ci'], '{:+.2f}')})"] for k in ('inside', 'used', 'lit', 'lit_dd')]
W(table(['Step (all maps)', 'Top 6', 'Rest', 'Gap in points (interval)', 'Such smokes per team-game (interval of the gap)'], rows) + '\n')
for k in ('inside', 'used', 'lit', 'lit_dd'): CHECK.append((f"N4-2 ladder, all maps, '{R[k]['label']}'", 'n4_c2.py', f'out-c2.json rungs.{k}.table[All maps]; per_team_game.{k}'))
W(f"- Of the {o['n']} early smokes with a radar cruiser inside, the cruiser ran radar from the smoke in {o['counts']['used']} ({o['counts']['strict']} on the strict test, where the log itself lists the smoke). Top 6 {p0(o['used']['top'])} of {o['used']['n_top']}, Rest {p0(o['used']['rest'])} of {o['used']['n_rest']} ({civ(o['used']['ci'], clear=o['used']['clear'])}). "
  f"It lit an enemy in {o['counts']['lit']} and an enemy destroyer in {o['counts']['lit_dd']}.")
W(f"- When it did run radar, it lit {o['enemies_lit_per_using_smoke']['top']:.1f} (Top 6) and {o['enemies_lit_per_using_smoke']['rest']:.1f} (Rest) enemy ships per smoke, {o['dd_lit_per_using_smoke']['top']:.1f} and {o['dd_lit_per_using_smoke']['rest']:.1f} of them destroyers. No clear gap. {o['lit_rows_ambiguous']} of {o['lit_rows']} lit records could also belong to another radar.")
W(f"- The batch's own \"radar run from inside\" flag marks {o['counts']['batch_run']} of the {o['n']}; the log finds all of those and {o['counts']['log_not_batch']} more (most likely because the batch flag also needs the ship to be undetected at that moment). "
  f"Among the {c2['not_inside_anyship_radar']['n']} early smokes with no radar cruiser inside, {c2['not_inside_anyship_radar']['any_radar_from_smoke']} still saw a radar pressed from inside (a radar destroyer, or a cruiser the batch put behind the smoke).\n")
W('Per map, with the number of clans behind each group (Top 6 clans / Rest clans):\n')
rows = []
for m in ['All maps'] + MAPORDER:
    a, b, c = R['inside']['table'][m], R['used']['table'][m], R['lit_dd']['table'][m]
    rows.append([m, f"{a['clans_top']} / {a['clans_rest']}", cell(a, 'top'), cell(a, 'rest'), gap(a), cell(b, 'top'), cell(b, 'rest'), gap(b), f"{c['x_top']} of {c['n_top']} vs {c['x_rest']} of {c['n_rest']}"])
    CHECK.append((f'N4-2 per-map row {m}', 'n4_c2.py', f'out-c2.json rungs.inside/used/lit_dd.table[{m}]'))
W(table(['Map', 'Clans', 'Inside: Top 6', 'Inside: Rest', 'Gap (interval)', 'Ran radar from it: Top 6', 'Rest', 'Gap (interval)', 'Lit an enemy destroyer (counts)'], rows) + '\n')
mr = R['used']['table']['Mountain Range']
W(f"Per map the \"ran radar from it\" counts are 0 to 6 smokes a side, so only the all-maps row should be read. Mountain Range is the one map with a starred gap ({mr['x_top']} of {mr['n_top']} vs {mr['x_rest']} of {mr['n_rest']}, small n).\n")
W('"Inside goes with the cap being taken", old field against the cap timeline, same smokes. Cap taken = not ours at activation and ours at some time up to 60 s after the smoke cleared:\n')
def caprows(cc_, keys):
    return [[cc_['rows'][k]['name'], f"{p0(cc_['rows'][k]['a'])} ({cc_['rows'][k]['x_a']} of {cc_['rows'][k]['n_a']})", f"{p0(cc_['rows'][k]['b'])} ({cc_['rows'][k]['x_b']} of {cc_['rows'][k]['n_b']})",
             f"{cc_['rows'][k]['diff']:+.0f} ({civ(cc_['rows'][k]['ci'], clear=cc_['rows'][k]['clear'])})"] for k in keys]
KEYS = ('batch_all', 'batch_takeable', 'tl_cont', 'tl_near', 'tl_cont10')
W('Three ships, radar cruiser inside against radar cruiser covered but not inside (the round 4 pair):\n')
W(table(['Measure', 'Inside', 'Covered, not inside', 'Gap (interval)'], caprows(c2['cap_three_ships'], KEYS)) + '\n')
W('All early destroyer smokes, radar cruiser inside against none inside:\n')
W(table(['Measure', 'Inside', 'None inside', 'Gap (interval)'], caprows(c2['cap_all_early'], KEYS)) + '\n')
for k in KEYS: CHECK.append((f'N4-2 cap taken, measure {k}', 'n4_c2.py', 'out-c2.json cap_three_ships.rows / cap_all_early.rows'))
cw = c2['check_cap_won']; uv = c2['cap_used_vs_not']['rows']; ct, cr = c2['cap_all_early_top']['rows'], c2['cap_all_early_rest']['rows']
W(f"- Why the old gap was so wide. The batch field `cap_won` does not follow one fixed cap. It counts any cap within gun range of a ship standing inside the smoke. A cruiser inside brings a longer gun range, so more caps count, so a capture is more likely to be credited. "
  f"Every one of the {cw['batch_cap_won']} batch captures on early destroyer smokes is real (the timeline confirms {cw['timeline_confirms_same_cap']}), but only {cw['batch_cap_is_contested']} are the smoke's contested cap and {cw['batch_cap_is_nearest']} its nearest cap. "
  f"On a fixed cap the \"not inside\" group rises from {p0(cap3['batch_all']['b'])} to {p0(cap3['tl_cont']['b'])} or {p0(cap3['tl_near']['b'])}, and the gap roughly halves.")
W(f"- What is left: on all early destroyer smokes the gap is clear on both fixed caps ({capA['tl_cont']['diff']:+.0f} points contested, {capA['tl_near']['diff']:+.0f} nearest). On the three ships against \"covered, not inside\" it is {cap3['tl_cont']['diff']:+.0f} ({civ(cap3['tl_cont']['ci'], clear=cap3['tl_cont']['clear'])}) contested and {cap3['tl_near']['diff']:+.0f} ({civ(cap3['tl_near']['ci'], clear=cap3['tl_near']['clear'])}) nearest: borderline, n {cap3['tl_near']['n_b']} in the smaller group.")
W(f"- Inside the two groups, nearest cap: Top 6 {p0(ct['tl_near']['a'])} vs {p0(ct['tl_near']['b'])} ({civ(ct['tl_near']['ci'], clear=ct['tl_near']['clear'])}); Rest {p0(cr['tl_near']['a'])} vs {p0(cr['tl_near']['b'])} ({civ(cr['tl_near']['ci'], clear=cr['tl_near']['clear'])}). As in round 5 item A1, the link to the cap is mainly a Rest pattern.")
W(f"- Pressing radar adds nothing visible on the cap: with a radar cruiser inside, nearest cap taken {p0(uv['tl_near']['a'])} (n {uv['tl_near']['n_a']}) when it ran radar from the smoke against {p0(uv['tl_near']['b'])} (n {uv['tl_near']['n_b']}) when it did not ({civ(uv['tl_near']['ci'], clear=uv['tl_near']['clear'])}). This matches atlas rule 3.\n")
W(f"**Top 6 or Shared:** Top 6 for \"a radar cruiser inside\" ({ins['diff']:+.0f} points, {civ(ins['ci'], clear=ins['clear'])}; Sleeping Giant is still the one map the other way, not clear). Shared for what the cruiser does once inside: ran radar from it {p0(o['used']['top'])} vs {p0(o['used']['rest'])} ({civ(o['used']['ci'], clear=o['used']['clear'])}). "
  f"As a share of all early smokes, \"inside and ran radar\" is {p0(used['top'])} vs {p0(used['rest'])} ({civ(used['ci'], clear=used['clear'])}) and \"lit an enemy destroyer\" {p0(ldd['top'])} vs {p0(ldd['rest'])} ({civ(ldd['ci'], clear=ldd['clear'])}): same direction, intervals just touch zero.\n")
W('**Clans:**\n')
W(f"- Radar cruiser inside, all maps ({ins['x_top']} + {ins['x_rest']} smokes): {clans(ins['clan_counts'])}.")
W(f"- Inside and ran radar from it, all maps ({used['x_top']} + {used['x_rest']}): {clans(used['clan_counts'])}.")
W(f"- Ran radar and lit an enemy destroyer ({ldd['x_top']} + {ldd['x_rest']}): {clans(ldd['clan_counts'])}.")
for m in MAPORDER:
    W(f"- {m}, radar cruiser inside: {clans(R['inside']['table'][m]['clan_counts'])}. Ran radar from it: {clans(R['used']['table'][m]['clan_counts'])}.")
W('')
W(f"**Could not be done / proxy:** The replay says a ship is radar-lit, not by whom; the log assigns it by range and time ({o['lit_rows_ambiguous']} of {o['lit_rows']} records here could belong to a second radar). The smoke shape is the final laid path. "
  f"{c2['one_sided_smokes']} early smokes are in the single-replay game; they are kept (the radar log and cap timeline do not depend on the missing replay). Per-map counts for radar use are too small to rank maps.\n")
W('**Verdict:** Keep (reword: the Top 6 difference is the cruiser being in the smoke; quote the cap link from the timeline, not 58% vs 14%)\n')
W('**Changed from the atlas / round 4:**\n')
W('- Layer A: ' + la(2) + 'Why: same smoke fields; an interval end can move by a point or two when the resampling is drawn again (the point estimates are identical).')
W(f"- Layer B: \"radar cruiser inside\" {xp(ins, 'top')} vs {xp(ins, 'rest')} ({ins['diff']:+.0f}) -> \"inside and ran radar from it\" {p0(used['top'])} vs {p0(used['rest'])} ({used['diff']:+.0f}, {civ(used['ci'], clear=used['clear'])}) -> \"and lit an enemy destroyer\" {p0(ldd['top'])} vs {p0(ldd['rest'])} ({ldd['diff']:+.0f}, {civ(ldd['ci'], clear=ldd['clear'])}). New: no old value. Why: better data (radar log).")
W(f"- Layer B, cap taken, three ships, inside vs covered-not-inside: 58% vs 14% (+44, +32 to +54) -> {p0(cap3['tl_cont']['a'])} vs {p0(cap3['tl_cont']['b'])} ({cap3['tl_cont']['diff']:+.0f}, {civ(cap3['tl_cont']['ci'], clear=cap3['tl_cont']['clear'])}) on the contested cap; "
  f"{p0(cap3['tl_near']['a'])} vs {p0(cap3['tl_near']['b'])} ({cap3['tl_near']['diff']:+.0f}, {civ(cap3['tl_near']['ci'], clear=cap3['tl_near']['clear'])}) on the nearest cap. Difference in the gap: {cap3['tl_cont']['diff'] - cap3['batch_all']['diff']:+.0f} and {cap3['tl_near']['diff'] - cap3['batch_all']['diff']:+.0f} points. "
  f"All early destroyer smokes: 61% vs 31% (+30, +21 to +38) -> {p0(capA['tl_cont']['a'])} vs {p0(capA['tl_cont']['b'])} ({capA['tl_cont']['diff']:+.0f}, {civ(capA['tl_cont']['ci'], clear=capA['tl_cont']['clear'])}) contested; {p0(capA['tl_near']['a'])} vs {p0(capA['tl_near']['b'])} ({capA['tl_near']['diff']:+.0f}, {civ(capA['tl_near']['ci'], clear=capA['tl_near']['clear'])}) nearest. "
  'Why: different definition made possible by better data (one fixed cap followed on the cap timeline, instead of any cap within gun range of a ship in the smoke).\n')

# =========================================================== claim 3
A, B = c3['A'], c3['B']; fs, fd, sw = B['from_smoke'], B['from_dd_smoke'], B['smokes_with_activation']; rt = B['return_from_smoke']; rd = B['return_from_dd_smoke']; rn = B['return_not_from_smoke']
W('### N4-3. Radar from smoke per team-game, and the return per play\n')
W(f"**Answer:** Still right, and now on a direct count. The radar log has {fs['n']} radar presses made from inside an allied smoke: {fs['top']:.2f} per team-game for the Top 6 against {fs['rest']:.2f} for the Rest, {fs['ratio']:.1f} times as often (the tag-based count said 2.5). "
  f"The return per press is the same for both groups: {rt['lit']['top']:.1f} vs {rt['lit']['rest']:.1f} enemy ships lit, {rt['dmg']['top'] / 1000:.1f}k vs {rt['dmg']['rest'] / 1000:.1f}k damage on them while lit, no clear gap on anything.\n")
W('**Numbers:**\n')
W('Layer A, same definition, new batch (destroyer smokes whose primary purpose tag is a radar play):\n')
d = A['dd_plays']; cct = A['cap_control_cap_taken']; bm = A['by_map']
rows = [arow(3, 'Destroyer smokes tagged as a radar play', '96 (52 Top 6, 44 Rest)', f"{d['n']} ({d['n_top']} Top 6, {d['n_rest']} Rest)", script='n4_c3.py', where='out-c3.json A.dd_plays'),
        arow(3, 'Per team-game', '0.47 vs 0.19', f"{d['top']:.2f} vs {d['rest']:.2f}", script='n4_c3.py', where='A.dd_plays.top/rest'),
        arow(3, 'Gap interval', '+0.14 to +0.40', civ(d['ci'], '{:+.2f}', False), True, 'n4_c3.py', 'A.dd_plays.ci'),
        arow(3, 'Cap taken after cap-control smokes (caps not ours)', '58% (of 24) vs 58% (of 26)', f"{p0(cct['top'])} (of {cct['n_top']}) vs {p0(cct['rest'])} (of {cct['n_rest']})", script='n4_c3.py', where='A.cap_control_cap_taken'),
        arow(3, 'Three busiest maps', '69 of 96 (0.45, 0.40, 0.36 per team-game)', f"{A['three_maps']} of {d['n']} ({bm['Sleeping Giant']['per_team_game']:.2f}, {bm['Hotspot']['per_team_game']:.2f}, {bm['Mountain Range']['per_team_game']:.2f} per team-game)", script='n4_c3.py', where='A.three_maps, A.by_map'),
        arow(3, 'Enemy ships lit per smoke with radar run (batch field)', '1.1 vs 1.1', f"{A['spots_per_radar_smoke']['top']:.1f} vs {A['spots_per_radar_smoke']['rest']:.1f}", script='n4_c3.py', where='A.spots_per_radar_smoke')]
W(table(['Number', 'Atlas / round 4', 'New batch, clock bug still in', 'New batch, clock corrected', 'Status'], rows) + '\n\n' + CLK + '\n')
W('Layer B, plays per team-game counted three ways:\n')
def rrow(lab, d, f='{:.2f}'):
    return [lab, f"{d['n']} ({d['n_top']} / {d['n_rest']})", f.format(d['top']), f.format(d['rest']), '-' if not d['ratio'] else f"{d['ratio']:.1f}x", f"{d['diff']:+.2f} ({civ(d['ci'], '{:+.2f}', d['clear'])})"]
bk = B['by_kind']
rows = [rrow('1. Tag-based (old): destroyer smokes tagged as a radar play', A['dd_plays']), rrow('1b. Tag-based, all smoker classes', A['all_class_plays']),
        rrow('2. Log: radar presses from inside any allied smoke', fs), rrow('2a. ... inside a destroyer smoke', fd),
        rrow('2a-i. ...... by another ship (a cruiser in the destroyer\'s smoke)', bk['destroyer smoke, radar by another ship']), rrow('2a-ii. ...... by the smoker itself (a radar destroyer)', bk['destroyer smoke, radar by the smoker itself']),
        rrow('2b. ... inside a cruiser\'s own smoke', bk["cruiser's own smoke"]), rrow('2c. ... inside another cruiser\'s smoke', bk["another cruiser's smoke"]),
        rrow('3. Log: smokes with at least one radar press from inside', sw), rrow('3a. ... destroyer smokes', B['dd_smokes_with_activation']), rrow('3b. ... cruiser smokes', B['cruiser_smokes_with_activation']),
        rrow('Context: all radar presses, in smoke or not', B['all_activations']), rrow('Context: radar presses not from smoke', B['not_from_smoke'])]
W(table(['Count', 'n (Top 6 / Rest)', 'Top 6 per team-game', 'Rest per team-game', 'Ratio', 'Gap (interval)'], rows) + '\n')
for r in rows: CHECK.append((f'N4-3 count row "{r[0]}"', 'n4_c3.py', 'out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke'))
tv = B['tag_vs_log']; sh = B['share_from_smoke']; tg = B['team_games_with_log_play']
W(f"- Tag against log on the same smokes: all {tv['tagged_dd_with_log_activation']} of the {tv['tagged_dd']} tagged destroyer smokes have a radar press from inside in the log. The log finds {tv['log_dd_smokes']} destroyer smokes with one, so {tv['log_dd_smokes'] - tv['log_dd_smokes_tagged']} more than the tags: "
  f"their primary tag is something else ({', '.join(f'{k} {v}' for k, v in tv['log_dd_smokes_other_tags'].items())}). Cruiser smokes: {tv['tagged_cruiser']} tagged, {tv['log_cruiser_smokes']} in the log.")
W(f"- The Top 6 press radar somewhat more overall ({B['all_activations']['top']:.1f} vs {B['all_activations']['rest']:.1f} per team-game, {B['all_activations']['ratio']:.1f}x, {civ(B['all_activations']['ci'], '{:+.2f}', B['all_activations']['clear'])}), but far more of it from smoke: {sh['top']:.1f}% of their radar presses against {sh['rest']:.1f}% ({civ(sh['ci'], '{:+.1f}', sh['clear'])} points). "
  f"{tg['top'][0]} of {tg['top'][1]} Top 6 team-games ({100 * tg['top'][0] / tg['top'][1]:.0f}%) have at least one radar press from smoke, against {tg['rest'][0]} of {tg['rest'][1]} ({100 * tg['rest'][0] / tg['rest'][1]:.0f}%); the tags gave 38% and 17%.")
W(f"- Who presses: {', '.join(f'{k} {v}' for k, v in B['radar_ships'].items())}. Cruisers {B['by_class']['cruiser']['n']}, radar destroyers {B['by_class']['destroyer']['n']}.\n")
W('By map (radar presses from inside an allied smoke):\n')
rows = []
for m in MAPORDER:
    v = B['by_map'][m]; small = ' (small n)' if 8 <= v['n'] < 15 else ' (too few)' if v['n'] < 8 else ''
    rows.append([m, f"{v['n']}{small} ({v['n_top']} / {v['n_rest']})", f"{v['clans_top']} / {v['clans_rest']}", f"{v['per_team_game_all']:.2f}", f"{v['top']:.2f}", f"{v['rest']:.2f}", f"{v['diff']:+.2f} ({civ(v['ci'], '{:+.2f}', v['clear'])})", f"{bm[m]['plays']} ({bm[m]['per_team_game']:.2f})"])
    CHECK.append((f'N4-3 map row {m}', 'n4_c3.py', f'out-c3.json B.by_map[{m}], A.by_map[{m}]'))
W(table(['Map', 'Presses (Top 6 / Rest)', 'Clans (Top 6 / Rest)', 'Per team-game, all clans', 'Top 6', 'Rest', 'Gap (interval)', 'Old tag count (per team-game)'], rows) + '\n')
tm = B['three_maps']
W(f"{', '.join(tm['names'])} hold {tm['plays']} of the {fs['n']} presses ({100 * tm['plays'] / fs['n']:.0f}%; the tags had 69 of 96, 72%). They are also the three highest by rate. Per-map Top 6 rates rest on 1 to 6 clans and 1 to 21 presses: read the direction, not the size.\n")
W(f"Return per play (one play = one radar press from inside an allied smoke, n {rt['n']}):\n")
def ret_row(lab, k, f, cf, R_=rt):
    d = R_[k]; return [lab, f"{f.format(d['top'])} (n {d['n_top']})", f"{f.format(d['rest'])} (n {d['n_rest']})", civ(d['ci'], cf, d['clear'])]
RET = [('Enemy ships lit per play', 'lit', '{:.2f}', '{:+.2f}'), ('Plays that lit at least one enemy', 'lit_any', '{:.0f}%', '{:+.0f}'), ('Enemy destroyers lit per play', 'lit_dd', '{:.2f}', '{:+.2f}'),
       ('Plays that lit at least one enemy destroyer', 'lit_dd_any', '{:.0f}%', '{:+.0f}'), ('Damage on lit enemies while lit, per play', 'dmg', '{:,.0f}', '{:+,.0f}'),
       ('... shells, torpedoes and secondaries only', 'dmg_direct', '{:,.0f}', '{:+,.0f}'), ('Plays with any damage on a lit enemy', 'dmg_any', '{:.0f}%', '{:+.0f}'),
       ('Check: health the lit enemies lost while lit (ship tracks)', 'hp_loss', '{:,.0f}', '{:+,.0f}'), ('Check: same damage from the other team\'s replay', 'dmg_run2', '{:,.0f}', '{:+,.0f}'),
       ('Nearest cap taken within 60 s (caps not ours)', 'cap60', '{:.0f}%', '{:+.0f}'), ('Nearest cap taken within 120 s (caps not ours)', 'cap120', '{:.0f}%', '{:+.0f}')]
W(table(['Per play', 'Top 6', 'Rest', 'Interval of Top 6 minus Rest'], [ret_row(*x) for x in RET]) + '\n')
for x in RET: CHECK.append((f'N4-3 return row "{x[0]}"', 'n4_c3.py', f'out-c3.json B.return_from_smoke.{x[1]}'))
cl = B['cap_control_timeline']
W(f"- No interval excludes zero. Cap rows: {rt['cap60_x'][0]} of {rt['cap60']['n_top']} and {rt['cap60_x'][1]} of {rt['cap60']['n_rest']} within 60 s; {rt['cap120_x'][0]} and {rt['cap120_x'][1]} within 120 s.")
W(f"- Destroyer smokes only (n {rd['n']}), the old population: {rd['lit']['top']:.2f} vs {rd['lit']['rest']:.2f} enemies lit, {rd['lit_dd']['top']:.2f} vs {rd['lit_dd']['rest']:.2f} destroyers, {rd['dmg']['top']:,.0f} vs {rd['dmg']['rest']:,.0f} damage ({civ(rd['dmg']['ci'], '{:+,.0f}', rd['dmg']['clear'])}), cap within 120 s {p0(rd['cap120']['top'])} vs {p0(rd['cap120']['rest'])} ({civ(rd['cap120']['ci'], clear=rd['cap120']['clear'])}).")
W(f"- For scale, a radar press that is not from smoke (n {rn['n']}) lights {rn['lit']['top']:.2f} (Top 6) and {rn['lit']['rest']:.2f} (Rest) enemy ships and goes with {rn['dmg']['top']:,.0f} and {rn['dmg']['rest']:,.0f} damage on them: a press from smoke lights slightly fewer ships and goes with about the same damage as any other press. The smoke does not show a bigger return per press; it is where the Top 6 choose to press from.")
W(f"- Per team-game that adds up to {B['enemies_lit_per_team_game']['top']:.2f} vs {B['enemies_lit_per_team_game']['rest']:.2f} enemy ships lit from smoke ({civ(B['enemies_lit_per_team_game']['ci'], '{:+.2f}')}; round 3 had 0.61 vs 0.25 from the batch field), "
  f"{B['enemy_dd_lit_per_team_game']['top']:.2f} vs {B['enemy_dd_lit_per_team_game']['rest']:.2f} destroyers ({civ(B['enemy_dd_lit_per_team_game']['ci'], '{:+.2f}')}), and {B['damage_on_lit_per_team_game']['top']:,.0f} vs {B['damage_on_lit_per_team_game']['rest']:,.0f} damage on radar-lit enemies ({civ(B['damage_on_lit_per_team_game']['ci'], '{:+,.0f}')}).")
W(f"- The old return test on the cap timeline: after the tagged cap-control smokes, the contested cap (not ours at activation) was ours within 60 s of the smoke clearing in {p0(cl['top'])} ({cl['x_top']} of {cl['n_top']}) for the Top 6 against {p0(cl['rest'])} ({cl['x_rest']} of {cl['n_rest']}) for the Rest ({civ(cl['ci'], clear=cl['clear'])}). "
  'The old "58% for both" came from the batch field that credits any cap in gun range (see N4-2). On a fixed cap the Top 6 are ahead but the interval is wide and includes zero.')
W(f"- {rt['amb_rows']} of the {rt['lit_rows']} lit records behind these plays could belong to a second radar.\n")
W(f"**Top 6 or Shared:** Top 6 for how often ({fs['diff']:+.2f} per team-game, {civ(fs['ci'], '{:+.2f}', fs['clear'])}; clear on every count except the two small ones, radar destroyers and cruiser smokes). Shared for the return per play (no interval excludes zero).\n")
pc_ = B['per_clan']
W(f"**Clans:** presses from smoke: {clans(B['clans'])}. Per game: " + ', '.join(f"{x['clan']}{'*' if x['top6'] else ''} {x['per_game']:.2f} ({x['log_plays']} in {x['games']}; tags {x['tag_plays']})" for x in pc_) + '. * = Top 6; Rest clans shown have 4 or more presses.\n')
rb = B['ribbons_total']
W(f"**Could not be done / proxy:** Defended and Captured ribbons are too thin to use: they exist only for the recording player (2 of 18 ships a game; {sum(rb.values())} cap ribbons in the whole batch), only {rt['recorder_plays']} of the {rt['n']} plays were pressed by a recording player, and {rt['ribbons']} cap ribbons followed them within 120 s. "
  'The cap timeline is used instead. "Damage on lit enemies while lit" is all damage those ships took during the lit span, whoever dealt it and whether or not radar was the only thing showing them; the replay does not say which radar lit a ship, so it is assigned by range and time. '
  'Damage from shells still in the air when the radar ran out is not counted.\n')
W('**Verdict:** Keep\n')
W('**Changed from the atlas / round 4:**\n')
W('- Layer A: ' + la(3) + 'Why: same smoke fields.')
W(f"- Layer B, how often: 0.47 vs 0.19 per team-game (2.5x; 96 tagged destroyer smokes) -> {fs['top']:.2f} vs {fs['rest']:.2f} ({fs['ratio']:.1f}x; {fs['n']} radar presses from any allied smoke; +{fs['top'] - 0.47:.2f} and +{fs['rest'] - 0.19:.2f}); destroyer smokes only {fd['top']:.2f} vs {fd['rest']:.2f} ({fd['ratio']:.1f}x; {fd['n']} presses); "
  f"smokes with a press {sw['top']:.2f} vs {sw['rest']:.2f} ({sw['ratio']:.1f}x; {sw['n']} smokes). Gap interval +0.14 to +0.40 -> {civ(fs['ci'], '{:+.2f}', False)}. Why: better data (every radar press is logged; the tags kept only smokes whose first purpose was the radar play) and a wider unit (presses, any smoker class).")
W(f"- Layer B, three maps: 69 of 96 (72%) -> {tm['plays']} of {fs['n']} ({100 * tm['plays'] / fs['n']:.0f}%). Same three maps. Why: better data.")
W(f"- Layer B, return per play: enemies lit 1.1 vs 1.1 per smoke -> {rt['lit']['top']:.2f} vs {rt['lit']['rest']:.2f} per press; cap taken 58% vs 58% (batch field, cap-control smokes) -> {p0(cl['top'])} vs {p0(cl['rest'])} on the contested cap from the timeline ({civ(cl['ci'], clear=cl['clear'])}), "
  f"and {p0(rt['cap120']['top'])} vs {p0(rt['cap120']['rest'])} for the nearest cap within 120 s of a press ({civ(rt['cap120']['ci'], clear=rt['cap120']['clear'])}); "
  f"damage on radar-lit enemies, new: {rt['dmg']['top']:,.0f} vs {rt['dmg']['rest']:,.0f} per press ({civ(rt['dmg']['ci'], '{:+,.0f}', rt['dmg']['clear'])}). Why: better data and a fixed-cap definition. \"Same return per play\" still holds: no gap is clear.\n")

W('## Figures\n')
W('- `figures/n4-claim1-short-of-cap.png` / `.svg`\n- `figures/n4-claim2-radar-cruiser-inside.png` / `.svg`\n- `figures/n4-claim3-radar-from-smoke.png` / `.svg`\n')
open(os.path.join(OUT, 'FINDINGS-N4.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ---------- CHECK
# second way for the claim 3 headline: count straight from the raw radar.csv files, without tl.py or the smoke records
sys.path.insert(0, os.path.dirname(OUT))
import r5lib, csv
raw = {'top': 0, 'rest': 0}
_tld = os.path.join(r5lib.BATCH, 'timelines')
for _d in sorted(os.listdir(_tld)):
    for _r in csv.DictReader(open(os.path.join(_tld, _d, 'radar.csv'), encoding='utf-8')):
        if _r['kind'] == 'radar' and _r['row'] == 'activation' and _r['source_in_smoke']: raw['top' if _r['team'] in r5lib.TOP else 'rest'] += 1
K = ['# CHECK-N4: where every number in FINDINGS-N4.md comes from\n',
     'Run order: `python -I -X utf8 n4_c1.py`, `n4_c2.py`, `n4_c3.py` (each writes `out-cN.json` and prints the same tables), then `n4_figs.py`, then `n4_report.py` (writes FINDINGS-N4.md, CHECK-N4.md, page1.json from the JSON files). '
     'Shared prep is `n4lib.py`. "Atlas / round 4" values are typed into `n4_report.py` from `atlas/ATLAS-CONTENT.md` page 1, `ROUND4-CHANGES.md`, `round3/module-2/MODULE-2.md` and `round3/module-3/MODULE-3.md` in the old checkout.\n',
     table(['Number', 'Script', 'Where'], CHECK), '',
     '## Self-checks\n',
     table(['Check', 'Result', 'Script / where'], [
         ['Headline counts (radar cruiser inside, Top 6 and Rest) recounted from the raw ship list of each smoke', f"findings {ins['x_top']} and {ins['x_rest']}; recount {c2['check_headline_second_way']['top']} and {c2['check_headline_second_way']['rest']}", 'n4_c2.py, check_headline_second_way'],
         ['Track position vs round 5 snapshot at the fully-laid moment (three-ship smokes)', f"median {c1['check_track_vs_snapshot']['median_m']} m, 90% within {c1['check_track_vs_snapshot']['p90_m']} m, n {c1['check_track_vs_snapshot']['n']}", 'n4_c1.py, check_track_vs_snapshot'],
         ['Smoker in a cap: snapshot vs track at end of laying', f"{c1['check_snapshot_smoker_in_cap']['pct']}% vs {P3['B_smoker_in_cap_end_pct'][0]}%", 'n4_c1.py, check_snapshot_smoker_in_cap'],
         ['Cap owner at activation: cap timeline vs batch field', f"{P3['check_own_tl_vs_batch_agree_pct']}% agree (three ships), {PA['check_own_tl_vs_batch_agree_pct']}% (all early)", 'n4_c1.py, check_own_tl_vs_batch_agree_pct'],
         ['Outline distance recomputed from the laid path vs batch field', f"median gap {P3['check_outline_min_vs_batch_median_abs_m']} m; inside / outside agree {P3['check_outline_inside_agree_pct']}%", 'n4_c1.py, check_outline_*'],
         ['Batch cap_won captures confirmed by the cap timeline (early destroyer smokes)', f"{cw['timeline_confirms_same_cap']} of {cw['batch_cap_won']}; the captured cap is the contested cap in {cw['batch_cap_is_contested']}, the nearest in {cw['batch_cap_is_nearest']}", 'n4_c2.py, check_cap_won'],
         ['Radar presses from inside a smoke, whole batch (STEP 9 table says 155 of 2,426)', f"{fs['n']} of {B['all_activations']['n']}", 'n4_c3.py, B.from_smoke.n, B.all_activations.n'],
         ['Radar presses from inside a smoke recounted from the raw radar.csv files (no library)', f"{raw['top']} Top 6, {raw['rest']} Rest = {raw['top'] / c3['team_games']['top']:.2f} and {raw['rest'] / c3['team_games']['rest']:.2f} per team-game (findings: {fs['n_top']}, {fs['n_rest']}; {fs['top']:.2f}, {fs['rest']:.2f})", 'n4_report.py, raw'],
         ['Tagged destroyer radar plays that have a logged press from inside', f"{tv['tagged_dd_with_log_activation']} of {tv['tagged_dd']}", 'n4_c3.py, B.tag_vs_log'],
         ['Damage on lit enemies: first replay vs the other team\'s replay vs health lost on tracks (per press, Top 6 / Rest)', f"{rt['dmg']['top']:,.0f} / {rt['dmg']['rest']:,.0f} vs {rt['dmg_run2']['top']:,.0f} / {rt['dmg_run2']['rest']:,.0f} vs {rt['hp_loss']['top']:,.0f} / {rt['hp_loss']['rest']:,.0f}", 'n4_c3.py, B.return_from_smoke.dmg / dmg_run2 / hp_loss'],
         ['Group sizes', f"early destroyer smokes {c2['n_top']} + {c2['n_rest']}; team-games {c3['team_games']['top']} + {c3['team_games']['rest']}", 'n4_c2.py, n4_c3.py']])]
open(os.path.join(OUT, 'CHECK-N4.md'), 'w', encoding='utf-8').write('\n'.join(K) + '\n')

# ---------- JSON fragment
def _unused(): pass
def ab(claim): return [dict(number=w, atlas=o_, new_batch_clock_bug_in=b, new_batch_corrected=n, status=s) for w, o_, b, n, s in CH[claim]]
page1 = dict(batch='output/20261117-230933', worker='n4', note='Page 1 carry-over claims re-tested. layer_a = same definition on the new batch; layer_b = re-tested with tracks, cap timeline and radar log. Association, not cause.',
    claims=[
        dict(id='N4-1', atlas_rule=1, title='Early smoke distance short of the cap', verdict='Keep', mode='shared', layer_a=ab(1),
             layer_b=dict(population='early Harugumo, Somers, Gearing smokes', n=P3['n'], n_with_track=P3['n_track'],
                          smoker_in_cap_at_activation_pct=P3['B_smoker_in_cap_act_pct'], smoker_in_cap_at_end_of_laying_pct=P3['B_smoker_in_cap_end_pct'],
                          smoker_km_outside_nearest_cap_at_activation=[round(P3['B_smoker_near_edge_act_m'][0] / 1000, 1), [round(x / 1000, 1) for x in P3['B_smoker_near_edge_act_m'][1]]],
                          smoker_km_outside_nearest_cap_at_end_of_laying=round(P3['B_smoker_near_edge_end_m'][0] / 1000, 1), smoker_on_own_side_of_cap_pct=P3['B_smoker_own_side_act_pct'],
                          cruiser_km_outside_nearest_cap=[round(P3['B_cruiser_near_edge_m'][0] / 1000, 1), [round(x / 1000, 1) for x in P3['B_cruiser_near_edge_m'][1]]],
                          cruiser_ever_in_cap_pct=P3['B_cruiser_ever_in_cap_pct'], cruiser_mostly_in_cap_pct=P3['B_cruiser_mostly_in_cap_pct'],
                          contested_cap_at_activation_pct=P3['B_cap_state_contested'], contested_cap_being_captured_pct=P3['B_invaded_cont'],
                          top6_vs_rest=dict(smoker_in_cap_at_activation=t3['smoker_in_cap_act'], smoker_m_outside_at_activation=t3['smoker_near_edge_act'], cruiser_m_outside=t3['cruiser_near_edge']),
                          early_cruiser_smoke=dict(inside={k: PI[k] for k in ('n', 'n_top', 'n_rest', 'A_inside_cap_pct', 'A_median_edge_m', 'B_smoker_in_cap_act_pct', 'B_smoker_near_edge_act_m', 'B_cruiser_near_edge_m', 'B_cruiser_ever_in_cap_pct', 'B_cap_state_contested', 'B_invaded_cont')},
                                                   screened={k: PS[k] for k in ('n', 'n_top', 'n_rest', 'A_inside_cap_pct', 'A_median_edge_m', 'B_smoker_in_cap_act_pct', 'B_smoker_near_edge_act_m', 'B_cruiser_near_edge_m', 'B_cruiser_ever_in_cap_pct', 'B_cap_state_contested', 'B_invaded_cont')}),
                          clans=P3['clan_counts']),
             suggested_wording=f"The opening smoke is cruiser cover laid short of the cap: {P3['A_inside_cap_pct'][0]:.0f}% inside a cap, typically {P3['A_median_edge_m'][0] / 1000:.1f} km outside (n {P3['n']}). The destroyer itself is in a cap when it presses smoke in {P3['B_smoker_in_cap_act_pct'][0]:.0f}%; the cruiser stays {P3['B_cruiser_near_edge_m'][0] / 1000:.1f} km out.",
             figure='figures/n4-claim1-short-of-cap'),
        dict(id='N4-2', atlas_rule=2, title='Radar cruiser inside early destroyer smokes', verdict='Keep', mode='top6', layer_a=ab(2),
             layer_b=dict(population='all early destroyer smokes', n_top=c2['n_top'], n_rest=c2['n_rest'],
                          ladder={k: dict(label=R[k]['label'], all_maps={kk: v for kk, v in am(k).items()}, per_team_game=c2['per_team_game'][k],
                                          per_map={m: R[k]['table'][m] for m in MAPORDER}) for k in ('inside', 'used', 'lit', 'lit_dd')},
                          of_smokes_with_radar_cruiser_inside=o, three_ships=c2['three_ships'],
                          cap_taken=dict(three_ships_inside_vs_covered_not_inside=c2['cap_three_ships'], all_early_inside_vs_none=c2['cap_all_early'], all_early_top6=c2['cap_all_early_top'], all_early_rest=c2['cap_all_early_rest'],
                                         inside_ran_radar_vs_did_not=c2['cap_used_vs_not'], batch_field_check=cw)),
             suggested_wording=f"Top 6 put a radar cruiser inside the early smoke: {f2(ins)}. It ran radar from the smoke in about a third of those, the same for both groups ({o['used']['top']:.0f}% vs {o['used']['rest']:.0f}%). "
                               f"The nearest cap was taken after {capA['tl_near']['a']:.0f}% of these smokes against {capA['tl_near']['b']:.0f}% with no radar cruiser inside.",
             figure='figures/n4-claim2-radar-cruiser-inside'),
        dict(id='N4-3', atlas_rule=4, title='Radar from smoke per team-game and return per play', verdict='Keep', mode='top6 for frequency, shared for return', layer_a=ab(3),
             layer_b=dict(team_games=c3['team_games'], counts=dict(tag_dd_smokes=A['dd_plays'], tag_all_classes=A['all_class_plays'], log_presses_from_smoke=fs, log_presses_from_destroyer_smoke=fd, by_smoke_kind=bk,
                                                                    log_smokes_with_press=sw, log_destroyer_smokes_with_press=B['dd_smokes_with_activation'], log_cruiser_smokes_with_press=B['cruiser_smokes_with_activation'],
                                                                    all_radar_presses=B['all_activations'], not_from_smoke=B['not_from_smoke'], share_of_presses_from_smoke_pct=sh, team_games_with_a_press=tg),
                          tag_vs_log=tv, by_map=B['by_map'], three_maps=tm, return_per_press=rt, return_per_press_destroyer_smoke=rd, return_per_press_not_from_smoke=rn,
                          per_team_game=dict(enemies_lit=B['enemies_lit_per_team_game'], enemy_destroyers_lit=B['enemy_dd_lit_per_team_game'], damage_on_lit=B['damage_on_lit_per_team_game']),
                          cap_control_cap_taken_timeline=cl, per_clan=pc_, clans=B['clans'], ribbons=dict(batch_total=rb, plays_by_recording_player=rt['recorder_plays'], ribbons_after_plays=rt['ribbons'])),
             suggested_wording=f"Top 6 run radar from smoke {fs['ratio']:.1f} times as often: {fs['top']:.2f} vs {fs['rest']:.2f} radar presses from inside a smoke per team-game ({fs['n_top']}, {fs['n_rest']}). Same return per press: {rt['lit']['top']:.1f} vs {rt['lit']['rest']:.1f} enemy ships lit.",
             figure='figures/n4-claim3-radar-from-smoke')])
json.dump(page1, open(os.path.join(OUT, 'page1.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('written: FINDINGS-N4.md, CHECK-N4.md, page1.json;', len(CHECK), 'check rows')
bad = [x for c in CH.values() for x in c if x[3] == 'DIFFERS']
print('layer A rows that differ:', bad)
