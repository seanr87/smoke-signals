# Round 5b, worker n2: builds FINDINGS-N2.md, CHECK-N2.md and deaths.json from the out-*.json files of the four scripts.
# Run after n2_health.py, n2_danger.py, n2_leave.py, n2_radar.py:  python -I -X utf8 n2_write.py
import os, json
HERE_ = os.path.dirname(os.path.abspath(__file__))
ld = lambda n: json.load(open(os.path.join(HERE_, n), encoding='utf-8'))
H, D, LV, R = ld('out-health.json'), ld('out-danger.json'), ld('out-leave.json'), ld('out-radar.json')
def tab(header, rows):
    return '\n'.join(['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])
def ci(c, f='{:+.1f}'):
    if not c or c[0] is None: return '-'
    return f'{f.format(c[0])} to {f.format(c[1])}' + (' *' if c[0] * c[1] > 0 else '')
def pci(c): return '-' if not c or c[0] is None else f'{c[0]:.1f} to {c[1]:.1f}'
def fv(x, f='{:.1f}'): return 'too few' if x is None else f.format(x)
def sm(n): return ' (too few)' if n < 8 else ' (small n)' if n < 15 else ''
def ds(d): return ', '.join(f'{k} {v}' for k, v in sorted(d.items(), key=lambda x: -x[1]))
CH = []   # rows for CHECK
def chk(number, script, where): CH.append([number, script, where])
def changed(rows):
    """rows: (what, old, new, why). Numeric pairs get the difference."""
    out = []
    for what, old, new, why in rows:
        d = ''
        if isinstance(old, (int, float)) and isinstance(new, (int, float)): d = f' ({new - old:+.1f})' if isinstance(old, float) or isinstance(new, float) else f' ({new - old:+d})'
        out.append(f'- {what}: {old} -> {new}{d}. {why}')
    return '\n'.join(out)
O = []
W = O.append

# =====================================================================================================================
W('# Round 5b findings, worker n2: danger zones with real health (C3), leaving the smoke and radar deaths (A2)\n')
W('Batch `output/20261117-230933`. Everything here is association, not cause. Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS. Intervals are 95%, whole clans resampled; * = excludes zero. '
  'Round 5 numbers are from `round5/FINDINGS.md`.\n')
ex = H['excluded']
W(f'Single-replay game (KSC vs -BN-, {ex["smokes_in_single_replay_game"]} smokes): the KSC ships have no replay of their own, so their health is blank or stale. Those ships are left out of every health number ({ex["pairs"]} ship-smoke pairs, all the KSC smoker in {ex["bad_smokes"]} smokes). The -BN- ships in that game are complete and stay in.\n')
W('Library note: `r5lib.py` now corrects two games that ran on a 15-minute clock (17 smokes had `el` 300 s too high in round 5). Nothing here uses `el`; times come from `e0`/`e1`. The round 5 time-of-game splits for those 17 smokes moved for that reason; the radar-death time split below uses the corrected times.\n')

# ---------------------------------------------------------------------------------------------------------------------
B = H['baselines']; dd = B['dd']['measures']; cr = B['cr']['measures']; crd = B['cr_dd']['measures']; ag = H['agreement']; fr = H['flip_reasons']; dc = H['deaths_check']; hp = H['hp_est']
W('### Real health: old estimate against the tracks, and the baselines redone\n')
W(f'**Answer:** The round 5 "hurt" flag was right for about 9 ships in 10, but it was low for destroyers and high for cruisers. With real health and deaths read from the tracks, {dd[4]["per_100"]} smoking destroyers per 100 destroyer smokes died or lost a third of their health while the smoke stood (round 5 said 15.5), and {cr[4]["per_100"]} sheltering cruisers per 100 (round 5 said 22.0). '
  f'The bigger surprise is deaths: the tracks show {dd[1]["count"]} smoking destroyers dead before 20 s after their smoke cleared, the batch list has {dd[0]["count"]}.\n')
W('**Numbers:**\n')
W('Definition used from here on. Died = the ship\'s track shows it dead between the smoke\'s activation and 20 s after it dispersed (20 s is the batch\'s own grace). Hurt = died, or its health at dispersal was lower than at activation by a third of full health or more (net loss, so health healed back inside the window does not count). '
  'Beside it: the "high-to-low" version (largest fall from a high point inside the window), which ignores heals.\n')
W('Old estimate against real health, same ships, same death list, so only the health source differs:\n')
W(tab(['who', 'ship-smoke pairs', 'hurt, old estimate', 'hurt, real health', 'flagged by both', 'new flags', 'flags lost', 'agree'],
      [[ag[k]['label'], ag[k]['n'], ag[k]['old_flags'], ag[k]['real_flags'], ag[k]['both'], ag[k]['new_flag'], ag[k]['lost_flag'], f'{ag[k]["agree_pct"]}%'] for k in ('dd', 'cr', 'all')]))
W(f'\n- {fr["new"] + fr["lost"]} flags flip out of {ag["all"]["n"]}: {fr["new"]} new, {fr["lost"]} lost.')
W(f'- New flags: the old number only counted damage taken while the batch had the ship as covered. Real health counts everything between activation and dispersal. In {fr["new_biggest_hit_outside_outline"]} of the {fr["new"]} the biggest hit landed outside the smoke outline (the ship had moved out).')
W(f'- Lost flags: {fr["lost_healed_back"]} healed back (mostly cruisers), {fr["lost_estimate_too_low"]} because the estimate of full health was too low, {fr["lost_other"]} other.')
W('\nHow far the old estimate of full health was from real full health (estimate divided by real):\n')
W(tab(['class', 'pairs', 'median', 'middle half', 'range', 'within 10% of real'], [[c, hp[c]['n'], hp[c]['median'], f'{hp[c]["q25"]} to {hp[c]["q75"]}', f'{hp[c]["min"]} to {hp[c]["max"]}', f'{hp[c]["within_10pct"]:.0f}%'] for c in ('destroyer', 'cruiser', 'battleship')]))
W('\nFurthest off: ' + ', '.join(f'{x["ship"]} {x["median_ratio"]} (n {x["n"]})' for x in H['hp_est_worst_ships']) + '. Brisbane was estimated at under half its real health, so round 5 flagged Brisbanes as hurt far too easily.\n')
W(f'Deaths. Batch list, ships at risk (smoker, inside, behind): {dc["batch"]}; the track confirms {dc["batch_confirmed_by_track"]} inside the window. Track deaths in the window: {dc["track_window"]}; {dc["track_only"]} of them are not in the batch list (by role: {ds(dc["track_only_by_how"])}). '
  f'Of those {dc["track_only"]}, {dc["track_only_inside_outline"]} died inside the smoke outline. The batch list only counts a ship that the smoke concealed and that was then detected at a flag change before it died. It leaves out ships that were lit from the start and stayed lit, ships that died without being detected, and ships that had left.\n')
def brow(m): return [m['measure'], m['count'], f'{m["per_100"]} [{pci(m["ci"])}]', m['top6'], m['rest'], ci(m['gap_ci'])]
W(f'Smoking destroyer, per 100 destroyer smokes (n {B["dd"]["n"]}: Top 6 {B["dd"]["n_top6"]}, Rest {B["dd"]["n_rest"]}):\n')
W(tab(['measure', 'count', 'per 100 [95%]', 'Top 6', 'Rest', 'Top 6 minus Rest'], [brow(m) for m in dd]))
W(f'\nSheltering cruisers (inside or behind), per 100 cruisers, any smoke (n {B["cr"]["n"]}: Top 6 {B["cr"]["n_top6"]}, Rest {B["cr"]["n_rest"]}):\n')
W(tab(['measure', 'count', 'per 100 [95%]', 'Top 6', 'Rest', 'Top 6 minus Rest'], [brow(m) for m in cr]))
W(f'\nSheltering cruisers in destroyer smokes only (n {B["cr_dd"]["n"]}): died (track) {crd[1]["per_100"]}, died or hurt {crd[4]["per_100"]} per 100.\n')
lo = H['loss']
W(f'Typical loss: a smoking destroyer loses {lo["dd"]["mean_net"]}% of full health on average while its smoke stands; {lo["dd"]["none_pct"]:.0f}% lose under 1%. Sheltering cruisers lose {lo["cr"]["mean_net"]}% net, {lo["cr"]["mean_trough"]}% high-to-low (they heal).\n')
W(f'**Top 6 or Shared:** Top 6 pattern. Top 6 smoking destroyers die or get hurt less ({dd[4]["top6"]} vs {dd[4]["rest"]} per 100, {ci(dd[4]["gap_ci"])}); deaths alone {dd[1]["top6"]} vs {dd[1]["rest"]} ({ci(dd[1]["gap_ci"])}). '
  f'Sheltering cruisers {cr[4]["top6"]} vs {cr[4]["rest"]} ({ci(cr[4]["gap_ci"])}); deaths {cr[1]["top6"]} vs {cr[1]["rest"]} ({ci(cr[1]["gap_ci"])}).\n')
W(f'**Could not be done / proxy:** {H['no_dispersal_time']} of {H['smokes']:,} smokes have no dispersal time in the replay (the game ended first, mostly); their end is activation + emission + puff life. '
  'Health is sampled every 2 s, so a fall and a heal inside one step are not seen. "While the smoke stood" is a time window: a ship that left the smoke and was hit elsewhere still counts for that smoke (see A2 leaving).\n')
W('**Verdict:** Keep (use the real-health baselines; retire the estimate).\n')
W('**Changed from round 5:**\n' + changed([
    ('Destroyer smoker died, per 100 destroyer smokes', 6.4, dd[1]['per_100'], 'Different definition: track deaths in the smoke window, not the batch list. The batch list on its own still gives ' + str(dd[0]['per_100']) + '.'),
    ('Destroyer smoker died or hurt, per 100', 15.5, dd[4]['per_100'], f'Better data (real health: {dd[3]["per_100"]} with the old death list) plus the track deaths.'),
    ('Sheltering cruiser died, per 100 cruisers (any smoke)', 8.0, cr[1]['per_100'], 'Track deaths. The batch list gives ' + str(cr[0]['per_100']) + ' on the cruisers with complete health.'),
    ('Sheltering cruiser died or hurt, per 100 (any smoke)', 22.0, cr[4]['per_100'], f'Better data: cruisers heal and the estimate was too low for Brisbane. High-to-low version: {cr[5]["per_100"]}.'),
    ('Sheltering cruiser died or hurt, destroyer smokes only (round 5 A2 table)', 22.5, crd[4]['per_100'], 'Same reason.'),
    ('Top 6 minus Rest, cruiser died or hurt (any smoke)', 'not clear (-17.7 to +2.6 in destroyer smokes)', ci(cr[4]['gap_ci']), 'Real health.'),
    ('Destroyer smokes in the health numbers', 1074, B['dd']['n'], 'The KSC smoker in the single-replay game is left out.'),
]) + '\n')
chk('Agreement table, flips, reasons', 'n2_health.py', 'out-health.json: agreement, flip_reasons')
chk('Estimate / real full health by class', 'n2_health.py', 'out-health.json: hp_est, hp_est_worst_ships')
chk(f'Batch deaths {dc["batch"]}, track deaths {dc["track_window"]}, track only {dc["track_only"]}', 'n2_health.py', 'out-health.json: deaths_check')
chk(f'Destroyer baselines {dd[1]["per_100"]} died / {dd[4]["per_100"]} died or hurt', 'n2_health.py', 'out-health.json: baselines.dd.measures[1], [4]')
chk(f'Cruiser baselines {cr[1]["per_100"]} / {cr[4]["per_100"]}', 'n2_health.py', 'out-health.json: baselines.cr.measures[1], [4]')
chk('Round 5 numbers reproduced from the round 5 fields (6.4 / 15.5, 8.0 / 22.0)', 'n2_health.py', 'out-health.json: check_r5')

# ---------------------------------------------------------------------------------------------------------------------
v1, v2 = D['v1'], D['v2']; p1, p2 = v1['placebo'], v2['placebo']; dp = D['death_pos']
f1 = [a for a in v1['shown'] if a['flag']]; f2 = [a for a in v2['shown'] if a['flag']]
KL = {'dd': 'destroyer smoker', 'cr': 'sheltering cruisers'}
surv = [x for x in D['r5_flags'] if x.get('survives')]
hot = next(x for x in D['r5_flags'] if x['map'] == 'Hotspot')
W('### C3. Danger zones (real health; two ways of placing the damage)\n')
W(f'**Answer:** No. With real health there is no danger zone the data can stand behind. Keyed on the smoke centre, {v1["n_flag"]} of {v1["tested"]} areas pass the rule and shuffled outcomes pass {p1["mean"]} by luck. Keyed on where the ship was hit, {v2["n_flag"]} of {v2["tested"]} pass and luck gives {p2["mean"]}. '
  f'Round 5\'s one sturdy flag, Hotspot inside cap C, does not survive: {hot["new_hurt"]:.0f} per 100 against a same-map baseline of {hot["new_base_map"]}. Every area that passes has 8 to 14 ships.\n')
W('**Numbers:**\n')
W(f'- Rule (unchanged): 8+ in the area, died-or-hurt rate clearly above BOTH the all-map and the same-map like-with-like baseline. Areas: 10 x 10 cells in the smoking team\'s frame, thin cells merged in their 2 x 2 block, plus "inside cap X".')
W(f'- Baselines: destroyer smoker {v1["baselines"]["dd"]["died"]} died and {v1["baselines"]["dd"]["hurt"]} died-or-hurt per 100; sheltering cruisers {v1["baselines"]["cr"]["died"]} and {v1["baselines"]["cr"]["hurt"]}. Same-map died-or-hurt: destroyers '
  + ', '.join(f'{m} {x["hurt"]}' for m, x in v1['baselines']['dd']['by_map'].items()) + '; cruisers ' + ', '.join(f'{m} {x["hurt"]}' for m, x in v1['baselines']['cr']['by_map'].items()) + '.')
W(f'- Version 1, keyed on the smoke centre (the round 5 areas): {v1["areas_built"]} areas, {v1["tested"]} tested ({v1["tested_dd"]} destroyer, {v1["tested_cr"]} cruiser). Flagged {v1["n_flag"]}. On deaths alone: {v1["n_flag_died"]}. '
  f'Placebo ({p1["runs"]} runs, outcomes shuffled within the map): {p1["mean"]} flags by luck per run (median {p1["median"]:.0f}, 95th percentile {p1["p95"]:.0f}); {p1["at_least_real"]} of {p1["runs"]} runs had {v1["n_flag"]} or more.')
W(f'- Version 2, keyed on where the damage happened: {v2["areas_built"]} areas, {v2["tested"]} tested ({v2["tested_dd"]} destroyer, {v2["tested_cr"]} cruiser). Flagged {v2["n_flag"]}. On deaths alone: {v2["n_flag_died"]}. '
  f'Placebo: {p2["mean"]} by luck per run (median {p2["median"]:.0f}, 95th percentile {p2["p95"]:.0f}); {p2["at_least_real"]} of {p2["runs"]} runs had {v2["n_flag"]} or more.')
W('- Version 2 unit and denominator: one entry per ship at risk (the smoking destroyer; each cruiser inside or behind a smoke). Each ship is placed once: at its death position if it died (last position alive, team frame of the smoking team); at its position at its largest 2 s health fall if it was hurt and lived; '
  'otherwise where it was half way through the smoke. Rate = ships placed in the area that died or were hurt / all ships placed in the area. So the denominator is ships, not smokes.\n')
def arow(a, ver):
    return [ver, a['map'], KL[a['kind']], a['name'], f'{a["n"]}{sm(a["n"])}', f'{a["hurt"]:.0f} ({a["n_hurt"]} of {a["den"]})', f'{a["base_all"][1]} / {a["base_map"][1]}', f'{a["hurt"]-a["base_all"][1]:+.0f} ({ci(a["ci_hurt_all"], "{:+.0f}")})',
            f'{a["hurt"]-a["base_map"][1]:+.0f} ({ci(a["ci_hurt_map"], "{:+.0f}")})', f'{a["died"]:.0f} ({a["n_died"]}; {a["base_all"][0]})', ci(a['ci_died_all'], '{:+.0f}')]
W('Areas that pass the rule:\n')
W(tab(['keyed on', 'map', 'who', 'area', 'n', 'died or hurt per 100', 'baseline all / same map', 'gap vs all maps', 'gap vs same map', 'died per 100 (n; baseline)', 'death gap interval'],
      [arow(a, 'smoke centre') for a in f1] + [arow(a, 'where hit') for a in f2]))
W('\nFor each: laid while 50+ behind / a covered ship radar-lit while the smoke stood (area, then the whole map):\n')
for ver, fl in (('smoke centre', f1), ('where hit', f2)):
    for a in fl:
        W(f'- {a["map"]} {a["name"]} ({KL[a["kind"]]}, by {ver}): 50+ behind {a["behind_pct"]:.0f}% (map {a["behind_map_pct"]:.0f}%); radar {a["radar_pct"]:.0f}% (map {a["radar_map_pct"]:.0f}%). Without the clan with most bad outcomes ({a["without_top_clan"]["clan"]}): {a["without_top_clan"]["hurt_per_100"]} per 100 (n {a["without_top_clan"]["n"]}).')
W('\nRound 5 flags on the same areas:\n')
rows = []
for x in D['r5_flags']:
    if x.get('too_few'): rows.append([x['map'], x['who'], x['area'], f'{x["n"]} (too few)', '-', '-', '-', 'not rated: one of its 8 smokes is the KSC smoke in the single-replay game'])
    else: rows.append([x['map'], x['who'], x['area'], f'{x["n"]}{sm(x["n"])}', f'{x["old_hurt"]:.0f} ({x["old_n_hurt"]})', f'{x["new_hurt"]:.0f} ({x["new_n_hurt"]} of {x["new_den"]})', f'{x["new_gap_all"]:+.0f} ({ci(x["new_ci_all"], "{:+.0f}")}) / {x["new_gap_map"]:+.0f} ({ci(x["new_ci_map"], "{:+.0f}")})', 'survives' if x['survives'] else 'does not survive'])
W(tab(['map', 'who', 'area', 'smokes', 'round 5: died or hurt per 100 (n)', 'real health: per 100', 'gap vs all maps / same map', 'result'], rows))
W(f'\nSecond way (check): the round 5 outcomes recomputed here on the same units give {D["r5_recomputed"]["tested"]} areas tested and flag {len(D["r5_recomputed"]["flagged"])}: {"; ".join(D["r5_recomputed"]["flagged"])}. Round 5 printed 109 and 4; the difference is the excluded single-replay ships.')
if D['v2_check_p0']:
    W('Version 2 flags placed a third way (where the ship was at activation): ' + '; '.join(f'{x["map"]} {x["area"]}: ' + (f'{x["hurt"]:.0f} per 100 (n {x["n"]})' if x['hurt'] is not None else f'too few (n {x["n"]})') for x in D['v2_check_p0']) + '.')
W('\nPer map:\n')
W(tab(['map', 'tested, smoke centre', 'flagged', 'tested, where hit', 'flagged'], [[m, v1['per_map'][m]['tested'], ', '.join(v1['per_map'][m]['flagged']) or 'none qualifies', v2['per_map'][m]['tested'], ', '.join(v2['per_map'][m]['flagged']) or 'none qualifies'] for m in v1['per_map']]))
W('\nDeath positions (new). Ships at risk that died between activation and 20 s after dispersal, distance from where they died to the edge of the smoke:\n')
BANDS = ['inside the outline', 'within 1 km of the edge', '1-3 km', 'over 3 km']
W(tab(['who died', 'deaths', 'in the batch list'] + BANDS + ['share inside', 'median distance past the edge'], [[w, x['n'], x['in_batch_list']] + [x['bands'][b] for b in BANDS] + [f'{x["inside_pct"]:.0f}%', f'{x["median_outside_m"]:,.0f} m' if x['median_outside_m'] else '-'] for w, x in dp['who'].items()]))
W(f'\n{dp["pairs"]} ship-smoke pairs, {dp["distinct_ships"]} distinct ships, all smoker classes. By map (deaths, inside the outline): ' + ', '.join(f'{m} {x["n"]}, {x["inside"]}' for m, x in dp['by_map'].items()) + '. Working figures: `figures/n2-deaths-<map>`.\n')
allf = [(a, 'smoke centre') for a in f1] + [(a, 'where hit') for a in f2]
W('**Top 6 or Shared:** ' + (' '.join(f'{a["map"]} {a["name"]} (by {v}): {"Top 6 spot" if a["mode"] == "top6" else "Shared spot"}{", in fact a Rest habit" if a["rest_habit"] else ""} (Top 6 {a["share_top"]:.0f}% vs Rest {a["share_rest"]:.0f}% of the map\'s {"smokes" if v == "smoke centre" else "ships"}, {ci(a["share_gap_ci"], "{:+.0f}")}).' for a, v in allf) or 'No area qualifies.') + '\n')
W('**Clans:**\n' + '\n'.join(f'- {a["map"]} {a["name"]} ({KL[a["kind"]]}, by {v}; {a["n_clans"]} clans, {a["n_games"]} games): {a["clans_text"]}.' for a, v in allf) + '\n')
W('**Could not be done / proxy:** Two thirds of areas have under 8 and are not rated. "Hurt" is a net loss over the whole smoke window, so damage taken after a ship left the smoke counts. In version 2 a hurt ship is placed where it was hit and an unhurt ship where it was at mid-smoke; '
  'the placebo keeps positions and shuffles outcomes, so it cannot mimic that link, and the version 2 luck count is if anything too low. Positions are every 2 s.\n')
W(f'**Verdict:** Drop danger zones as map markings on every map. Both versions flag about as many areas as luck does, all with small n, and no area passes on deaths alone. Keep the per-map death-position maps as a Lead: they show that most ships that die "in smoke" die outside the outline '
  f'({dp["who"]["smoking destroyer"]["inside_pct"]:.0f}% of smoking destroyers and {dp["who"]["sheltering cruiser"]["inside_pct"]:.0f}% of sheltering cruisers died inside it).\n')
names1 = ', '.join(f'{a["map"]} {a["name"]}' for a in f1) or 'none'
W('**Changed from round 5:**\n' + changed([
    ('Flagged areas, keyed on the smoke centre', 4, v1['n_flag'], f'Real health and track deaths. Now: {names1}.'),
    ('Hotspot inside cap C (destroyer smoker), died or hurt per 100', 32, hot['new_hurt'], f'Real health: {hot["new_n_hurt"]} of {hot["new_den"]} instead of 7 of 22, while the baselines rose (all maps 15.5 -> {hot["new_base_all"]}, Hotspot 11.9 -> {hot["new_base_map"]}). The gap is no longer clear ({ci(hot["new_ci_map"], "{:+.0f}")} against the map). Round 5 called this Lead; now Drop.'),
    ('Sea of Fortune E5+F5+E6', 'flag (n 8)', 'no flag', 'Same 5 of 8, but the Sea of Fortune baseline rose and the gap against the map is not clear.'),
    ('Sleeping Giant E7+F7+F8', 'flag, 50 per 100 (n 8)', 'flag, ' + (f'{next((x["new_hurt"] for x in D["r5_flags"] if x["map"] == "Sleeping Giant"), 0):.0f} per 100 (n 8)'), 'Still passes, still n 8, still in line with luck.'),
    ('Mountain Range E7+F7+F8 (cruisers)', 'flag (n 8)', 'not rated (n 7)', 'One of the 8 smokes is in the single-replay game, health incomplete.'),
    ('Placebo, flags by luck per run', 1.23, p1['mean'], 'Higher baselines make chance flags a little more common.'),
    ('Areas tested', 109, v1['tested'], 'Single-replay ships excluded.'),
    ('Keyed on where the ship was hit', 'not possible', f'{v2["n_flag"]} flags, {p2["mean"]} by luck', 'New: death positions and health tracks.'),
    ('Death position', 'unknown', f'{dp["pairs"]} deaths placed', 'New: tracks.'),
]) + '\n')
chk(f'Version 1: {v1["tested"]} tested, {v1["n_flag"]} flagged, placebo {p1["mean"]}', 'n2_danger.py', 'out-danger.json: v1 (n_flag, placebo, shown)')
chk(f'Version 2: {v2["tested"]} tested, {v2["n_flag"]} flagged, placebo {p2["mean"]}', 'n2_danger.py', 'out-danger.json: v2')
chk('Round 5 flags old vs new', 'n2_danger.py', 'out-danger.json: r5_flags, r5_recomputed')
chk('Flagged-area clans, 50+ behind, radar, Top 6 or Shared', 'n2_danger.py', 'out-danger.json: v1.shown / v2.shown (flag true); danger-zones.json')
chk(f'Death positions: {dp["pairs"]} pairs, inside / outside', 'n2_danger.py', 'out-danger.json: death_pos')

# ---------------------------------------------------------------------------------------------------------------------
bd, tdj = LV['batch_deaths'], LV['track_deaths']; pr = LV['proxies']; rates = {r['label']: r for r in LV['rates']}; hz = {(h['who'], h['state']): h for h in LV['hazard']}
CL = ['inside a standing smoke', 'within 30 s of leaving a standing smoke', 'more than 30 s after leaving', 'after the smoke dispersed around it', 'never inside the outline']
SH = ['inside a standing smoke', 'within 30 s of leaving', 'more than 30 s after leaving', 'after it dispersed around the ship', 'never inside the outline']
def crow(js, w): return [w, f'{js[w]["n"]} ({js[w]["n_top6"]} / {js[w]["n_rest"]})'] + [f'{js[w]["classes"][k]["n"]} ({js[w]["classes"][k]["top6"]} / {js[w]["classes"][k]["rest"]})' for k in CL]
ba = bd['all']['classes']; left_b = ba[CL[1]]['n'] + ba[CL[2]]['n']
sdd, scr = rates['smoking destroyer, all'], rates['sheltering cruiser, all']
W('### A2. Leaving the smoke (from ship tracks)\n')
W(f'**Answer:** Most ships that "died in smoke" had already left it. Of round 5\'s 124 deaths in destroyer smokes, {ba[CL[0]]["n"]} died inside a standing smoke, {left_b} died after sailing out of one ({ba[CL[1]]["n"]} within 30 s, {ba[CL[2]]["n"]} later), {ba[CL[3]]["n"]} after the smoke dispersed around them and {ba[CL[4]]["n"]} were never inside. '
  f'But leaving is not the dangerous moment: in the 30 s after leaving a standing smoke {sdd["died"]["left"]} smoking destroyers per 100 died, against {sdd["died"]["stayed"]} in the 30 s after the smoke dispersed around those that stayed, and {hz[("smoking destroyer", "all")]["inside_deaths_per_100"]} per 30 s spent inside. Being 50+ behind raises all three.\n')
W('**Numbers:**\n')
W('How a death is classed, from the track (position every 2 s): inside = last position alive is within the radius of a puff that still stands; left = it moved outside every puff while the puffs it had been in still stood; dispersed = the puffs around it ended while it was still in the old outline; never inside = no sample inside a standing puff. '
  'Each puff ends at its own time (the first puff of a long smoke goes first).\n')
W('Round 5\'s death list (batch smoke deaths in destroyer smokes). Cells: count (Top 6 / Rest):\n')
W(tab(['who died', 'n (Top 6 / Rest)'] + SH, [crow(bd, w) for w in ('smoking destroyer', 'sheltering cruiser', 'other ship', 'all') if w in bd]))
W(f'\nEvery ship at risk whose track shows a death between activation and 20 s after dispersal ({tdj["all"]["n"]} ship-smoke pairs; the batch list has {LV["track_deaths"]["all"]["n"] - LV["track_only_deaths"]["all"]["n"]} of them):\n')
W(tab(['who died', 'n (Top 6 / Rest)'] + SH, [crow(tdj, w) for w in ('smoking destroyer', 'sheltering cruiser', 'other ship', 'all') if w in tdj]))
to = LV['track_only_deaths']
W(f'\nThe {to["all"]["n"]} deaths the batch list misses are mostly smoking destroyers ({to["smoking destroyer"]["n"]}), and {to["smoking destroyer"]["classes"][CL[0]]["n"]} of those died inside their standing smoke.')
bl = LV['batch_left']
W(f'Deaths after leaving (batch list): median {bl["median_gap_s"]} s after leaving, median {bl["median_dist_m"]:,.0f} m past the smoke edge.\n')
lvv = LV['leavers']; ev = LV['events']
W(f'The rate question. Ships at risk in destroyer smokes that were inside a standing smoke at some point: {ev["left"]} left while it stood, {ev["stayed"]} stayed until the puffs around them ended, {ev["died_inside"]} died inside (games that ended inside the next 30 s are dropped). '
  f'Leavers left a median {lvv["median_time_in_s"]:.0f} s after activation with a median {lvv["median_smoke_left_s"]:.0f} s of smoke still to run: destroyers lay smoke and move on. Score state is taken at the moment of leaving or dispersal, from the score timeline.\n')
def rrow(r):
    f = lambda x, k: fv(x[k]) + f' ({x["n_" + k]})'
    return [r['label'], f'{r["n_left"]}{sm(r["n_left"])}', f'{r["n_stayed"]}{sm(r["n_stayed"])}', f(r['died'], 'left'), f(r['died'], 'stayed'), ci(r['died']['ci']), f(r['hurt'], 'left'), f(r['hurt'], 'stayed'), ci(r['hurt']['ci'])]
keep = [r for r in LV['rates'] if not r['label'].endswith('(stayers unchanged)')]
W(tab(['group', 'left: n', 'stayed: n', 'died in next 30 s per 100: left (n)', 'stayed (n)', 'left minus stayed', 'died or lost 1/3+ per 100: left (n)', 'stayed (n)', 'left minus stayed'], [rrow(r) for r in keep]))
W('\nA gap marked * where the stayed count is 0 of about 20 rests on no events and should be read as "no difference shown".\n')
W('Per 30 seconds, three situations side by side (deaths per 100 ship half-minutes; health lost = every fall added up, share of full health; detected = share of time or ships):\n')
W(tab(['who', 'score', 'inside a standing smoke: deaths per 100 (n)', 'health lost', 'detected', '30 s after leaving: deaths per 100', 'health lost', '30 s after it dispersed: deaths per 100', 'health lost'],
      [[h['who'], h['state'], f'{h["inside_deaths_per_100"]} ({h["inside_deaths"]})', f'{h["inside_loss_pct"]}%', f'{h["inside_detected_pct"]}%', f'{fv(h["left_deaths_per_100"])} (n {h["left_n"]})', f'{h["left_loss_pct"]}%', f'{fv(h["stayed_deaths_per_100"])} (n {h["stayed_n"]})', f'{h["stayed_loss_pct"]}%'] for h in LV['hazard']]))
d1, d2 = sdd['det'], scr['det']
W(f'\nDetected when leaving (track `det`). Smoking destroyers: {d1["left_inside"]:.0f}% detected at the last sample inside, {d1["left_at_exit"]:.0f}% at the first sample outside, {d1["left_10s"]:.0f}% at some point in the next 10 s. Those that stayed: {d1["stayed_inside"]:.0f}% before the smoke went, {d1["stayed_at_end"]:.0f}% at the first sample without it, {d1["stayed_10s"]:.0f}% within 10 s. '
  f'Sheltering cruisers: leaving {d2["left_inside"]:.0f}% -> {d2["left_at_exit"]:.0f}% -> {d2["left_10s"]:.0f}%; staying {d2["stayed_inside"]:.0f}% -> {d2["stayed_at_end"]:.0f}% -> {d2["stayed_10s"]:.0f}%.\n')
b1, b2 = rates['smoking destroyer, 50+ behind'], rates['smoking destroyer, not behind']
W(f'- Score state drives it, not leaving: smoking destroyers that left died in the next 30 s at {b1["died"]["left"]} per 100 when 50+ behind and {b2["died"]["left"]} when not. Inside a standing smoke: {hz[("smoking destroyer", "behind 50+")]["inside_deaths_per_100"]} vs {hz[("smoking destroyer", "not behind")]["inside_deaths_per_100"]} per 30 s.')
W(f'- A destroyer that leaves its smoke usually leaves unseen ({d1["left_10s"]:.0f}% detected within 10 s). One that sits until the smoke clears is seen more often ({d1["stayed_10s"]:.0f}%).')
W(f'- Cruisers lose more health in the 30 s after leaving ({hz[("sheltering cruiser", "all")]["left_loss_pct"]}%) or after dispersal ({hz[("sheltering cruiser", "all")]["stayed_loss_pct"]}%) than per 30 s inside ({hz[("sheltering cruiser", "all")]["inside_loss_pct"]}%).\n')
t6, rs = rates['smoking destroyer, Top 6'], rates['smoking destroyer, Rest']
W(f'**Top 6 or Shared:** Shared. Leaving against staying shows no clear gap for Top 6 or for Rest (smoking destroyers, died or lost a third: Top 6 {fv(t6["hurt"]["left"])} left vs {fv(t6["hurt"]["stayed"])} stayed, {ci(t6["hurt"]["ci"])}; Rest {fv(rs["hurt"]["left"])} vs {fv(rs["hurt"]["stayed"])}, {ci(rs["hurt"]["ci"])}). '
  f'Where they died: Top 6 smoking destroyers {tdj["smoking destroyer"]["classes"][CL[0]]["top6"]} of {tdj["smoking destroyer"]["n_top6"]} inside a standing smoke, Rest {tdj["smoking destroyer"]["classes"][CL[0]]["rest"]} of {tdj["smoking destroyer"]["n_rest"]}; counts only, not tested.\n')
W(f'**Clans:** ships that died within 30 s of leaving a standing smoke: {LV["leaver_deaths_clans_text"]}.\n')
W('**Could not be done / proxy:** The smoke outline is the final laid path, so a ship counts as inside a puff a few seconds before that puff exists. Per-puff end times are worked out from the emission time, not read from the replay. Positions every 2 s: a ship that dips out and back inside one step is not seen. '
  'Leavers and stayers are different ships in different situations (leavers are mostly destroyers moving on early, stayers sat still), so the comparison is a description, not a test of "should I leave".\n')
W('**Verdict:** Lead. "Died in smoke" mostly means "died after leaving it", and neither leaving nor the smoke running out is the risky moment; the score state is.\n')
ac, bh = pr['after_cleared'], pr['behind']
W('**Changed from round 5:**\n' + changed([
    ('Proxy 1, died just after the smoke cleared', 27, ba[CL[3]]['n'], f'Tracks: only {ba[CL[3]]["n"]} of the 124 died after the smoke dispersed around them. Of round 5\'s 27, the track puts {ds(ac["classes"])}: most had sailed out long before.'),
    ('Proxy 2, died behind rather than inside', 25, ba[CL[4]]['n'], f'Tracks: {ba[CL[4]]["n"]} were never inside the outline. Of round 5\'s 25 "behind", the track puts {ds(bh["classes"])}.'),
    ('Died inside the smoke (batch "inside")', pr['inside_list']['n'], ba[CL[0]]['n'], f'The batch "inside" means concealed by the smoke at some point. By position at death: {ds(pr["inside_list"]["classes"])}.'),
    ('Deaths after leaving a standing smoke', 'could not be told', left_b, 'New: tracks.'),
    ('Leaving against staying, rates', 'could not be done', f'{sdd["died"]["left"]} vs {sdd["died"]["stayed"]} per 100 (smoking destroyers, next 30 s)', 'New: tracks.'),
    ('Deaths of ships at risk in destroyer smokes', 124, tdj['all']['n'], 'Track deaths in the smoke window; the batch list misses ships that died unseen or were lit throughout.'),
]) + '\n')
chk(f'Batch deaths by class: inside {ba[CL[0]]["n"]}, left {left_b}, dispersed {ba[CL[3]]["n"]}, never {ba[CL[4]]["n"]}', 'n2_leave.py', 'out-leave.json: batch_deaths')
chk(f'Track deaths by class ({tdj["all"]["n"]})', 'n2_leave.py', 'out-leave.json: track_deaths, track_only_deaths')
chk('Round 5 proxies against the track', 'n2_leave.py', 'out-leave.json: proxies')
chk(f'Leaving vs staying rates ({sdd["died"]["left"]} vs {sdd["died"]["stayed"]})', 'n2_leave.py', 'out-leave.json: rates')
chk('Per 30 s inside / after leaving / after dispersal, detection', 'n2_leave.py', 'out-leave.json: hazard, rates[].det')

# ---------------------------------------------------------------------------------------------------------------------
rb, rt = R['batch'], R['track']; vs = R['vs_round5_deaths']; RR = R['rates']; RD = R['rate_diffs']; calm = R['calm']
ra = {r['label']: r for k in RR for r in RR[k]}
A_, B_ = 'radar log: a covered ship radar-lit while the smoke stood', 'radar log: lit while placed inside this smoke'
W('### A2. Radar deaths with the full radar log\n')
W(f'**Answer:** Radar is on far more deaths than round 5 could see. Of the 124 deaths in destroyer smokes, {rb["lit40"]} ({rb["lit40_pct"]:.0f}%) were radar-lit in their last 40 s and {rb["lit20"]} in their last 20 s; round 5 had 19 (strict) or 45 (broad). '
  f'The radar ship is nearly always a cruiser sitting near the edge of its range (median {rb["share_of_range"]["median"]:.0f}% of range, {rb["dist_km"]["median"]} km), Moskva most of all. Destroyer smokes with a covered ship radar-lit lose {ra[A_ + ": with"]["per_100"]} ships per 100, against {ra[A_ + ": without"]["per_100"]} without.\n')
W('**Numbers:**\n')
def rblock(o, title):
    W(f'{title}\n')
    W(f'- Radar-lit in the last 40 s: {o["lit40"]} of {o["deaths"]} ({o["lit40_pct"]}%). In the last 20 s: {o["lit20"]} ({o["lit20_pct"]}%).')
    W(f'- Top 6 {o["top6"]} of {o["deaths_top6"]} deaths, Rest {o["rest"]} of {o["deaths_rest"]} (last 20 s: {o["top6_20"]} and {o["rest_20"]}).')
    W('- Who died: ' + ', '.join(f'{k} {v} of {o["who_all"].get(k, 0)}' for k, v in o['who'].items()) + '.')
    W('- By map (radar-lit deaths of all deaths there): ' + ', '.join(f'{m} {v} of {o["deaths_by_map"].get(m, 0)}' for m, v in o['by_map'].items()) + '. By nearest cap: ' + ', '.join(f'{k} {v}' for k, v in list(o['by_map_cap'].items())[:8]) + '.')
    W('- By time the smoke was laid: ' + ', '.join(f'{k} {o["by_time"].get(k, 0)}' for k in ('0-5 min', '5-10 min', '10-15 min', '15-20 min')) + '. By score at activation: ' + ', '.join(f'{k} {o["by_state"].get(k, 0)} of {o["deaths_by_state"].get(k, 0)}' for k in ('behind 50+', 'level', 'ahead 50+')) + '.')
    W(f'- Radar ship (named for {o["attributed"]} of {o["lit40"]}): ' + ', '.join(f'{k} {v}' for k, v in o['src_class'].items()) + '. ' + ', '.join(f'{k} {v}' for k, v in o['src_ship'].items()) + '.')
    d, s_ = o['dist_km'], o['share_of_range']
    W(f'- Distance from the radar ship: median {d["median"]} km (quarter marks {d["q25"]} and {d["q75"]}; range {d["min"]} to {d["max"]}). As a share of that ship\'s radar range: median {s_["median"]:.0f}% (quarter marks {s_["q25"]:.0f}% and {s_["q75"]:.0f}%); {s_["beyond_80"]} of {s_["n"]} beyond 80% of range, {s_["under_60"]} under 60%. '
      + ' '.join(f'{c.capitalize()} radars: median {x["median_km"]} km, {x["median_share"]:.0f}% of range (n {x["n"]}{sm(x["n"]).strip() and ", " + sm(x["n"]).strip(" ()")}).' for c, x in o['by_src_class'].items()))
    W(f'- Ambiguous (more than one enemy radar had the ship in range): {o["ambiguous"]} of {o["lit40"]} ({o["ambiguous_pct"]}%).')
    W(f'- Radar play from smoke (the radar ship was itself inside a smoke): {o["src_in_smoke"]} of {o["attributed"]} ({o["src_in_smoke_pct"]}%).')
    W(f'- Where the dying ship was while lit: the log places {o["target_in_this_smoke"]} of {o["lit40"]} inside the smoke; the rest were lit outside it (behind it, or after leaving).')
    lf = o['lit_for_s']
    W(f'- How long it had been lit: median {lf["median"]} s (quarter marks {lf["q25"]} and {lf["q75"]}; longest {lf["max"]}). Under 10 s: {lf["under_10"]}; 20 s or more: {lf["over_20"]}. Still lit at the moment of death: {o["lit_at_death"]} of {o["lit40"]}'
      + (f'; for the rest the radar had ended a median {o["median_gap_to_death_s"]} s earlier.' if o['median_gap_to_death_s'] is not None else '.') + '\n')
rblock(rb, 'Round 5\'s death list (124 batch smoke deaths in destroyer smokes):')
rblock(rt, f'Every ship at risk in a destroyer smoke whose track shows a death between activation and 20 s after dispersal ({rt["deaths"]}):')
W(f'Death by death against round 5 (124 deaths): strict 19, broad 45, radar log {vs["log40"]}. All {vs["strict_and_log"]} strict deaths are in the log; the log adds {vs["log_not_strict"]}. {vs["broad_and_log"]} of the 45 broad deaths are in the log, {vs["broad_not_log"]} is not; the log adds {vs["log_not_broad"]} that broad missed. '
  f'Check: for the strict deaths the log names the same radar ship in {R["strict_check"]["same_radar_ship"]} of {R["strict_check"]["n"]} and gives the same distance (median {R["strict_check"]["median_log_km"]} km vs {R["strict_check"]["median_old_km"]} km).\n')
W('Rates per 100 destroyer smokes (deaths = batch list, so the columns compare with round 5):\n')
def rr(r): return [r['label'], f'{r["n"]} ({r["n_top6"]} / {r["n_rest"]}){sm(r["n"])}', r['deaths'], f'{fv(r["per_100"])} [{pci(r["ci"])}]', fv(r['top6']), fv(r['rest']), ci(r['gap_ci'])]
rows = []
for k in ('rad_any', 'rad_in', 'old_strict', 'old_broad'): rows += [rr(r) for r in RR[k][:2]]
W(tab(['reading', 'n (Top 6 / Rest)', 'deaths', 'per 100 [95%]', 'Top 6', 'Rest', 'Top 6 minus Rest'], rows))
W('\nWith radar minus without: ' + '; '.join(f'{lab}: {RD[k]["all"]["diff"]:+.1f} ({ci(RD[k]["all"]["ci"])})' for lab, k in (('log, any covered ship', 'rad_any'), ('log, lit inside the smoke', 'rad_in'), ('round 5 strict', 'old_strict'), ('round 5 broad', 'old_broad'))) + '.\n')
W('By score state at activation (radar log, a covered ship radar-lit while the smoke stood):\n')
W(tab(['reading', 'n (Top 6 / Rest)', 'deaths', 'per 100 [95%]', 'Top 6', 'Rest', 'Top 6 minus Rest'], [rr(r) for r in RR['rad_any'][2:]]))
W('\nWith minus without: ' + '; '.join(f'{k}: {RD["rad_any"][k]["diff"]:+.1f} ({ci(RD["rad_any"][k]["ci"])})' for k in ('ahead 50+', 'level', 'behind 50+')) + '.\n')
W('Same split with track deaths (every ship at risk that died between activation and 20 s after dispersal):\n')
W(tab(['reading', 'n (Top 6 / Rest)', 'deaths', 'per 100 [95%]', 'Top 6', 'Rest', 'Top 6 minus Rest'], [rr(r) for r in RR['rad_any_track']]))
W('\nWith minus without: ' + '; '.join(f'{k}: {RD["rad_any_track"][k]["diff"]:+.1f} ({ci(RD["rad_any_track"][k]["ci"])})' for k in ('all', 'ahead 50+', 'level', 'behind 50+')) + '.\n')
W('Smoke by smoke, 1,074 destroyer smokes:\n')
W(tab(['round 5 reading', 'radar log reading', 'round 5 smokes', 'log smokes', 'in both', 'missed by round 5', 'over-counted by round 5'], [[x['old'], x['new'].replace('radar log: ', ''), x['old_n'], x['new_n'], x['both'], x['new_only'], x['old_only']] for x in R['smoke_by_smoke']]))
lo_ = R['log_only']
W(f'\n- Round 5 strict is the same thing as "lit while inside this smoke" in the log ({R["smoke_by_smoke"][0]["both"]} of {R["smoke_by_smoke"][0]["old_n"]} smokes shared). It was right, just narrow.')
W(f'- Round 5 broad missed {R["smoke_by_smoke"][2]["new_only"]} smokes where a covered ship was lit while out of cover. Those lose only {lo_["per_100"]} per 100 ({lo_["deaths"]} deaths in {lo_["n"]}), which is why the log reading separates deaths a little less sharply than broad did.')
W(f'- Radar reaches Top 6 and Rest equally often: ' + '; '.join(f'{lab}: {R["reach"][k]["top6"]}% vs {R["reach"][k]["rest"]}% ({ci(R["reach"][k]["gap_ci"])})' for lab, k in (('log, any covered ship', 'rad_any'), ('log, inside the smoke', 'rad_in'))) + '.\n')
co, cn, cnt = calm['old'], calm['new'], calm['new_track']
W(f'Calm smokes (neither 50+ behind at activation nor radar): round 5 definition {co["n"]} smokes, {co["deaths"]} deaths, {co["per_100"]} per 100. With the radar log (no covered ship radar-lit while the smoke stood): {cn["n"]} smokes, {cn["deaths"]} deaths, {cn["per_100"]} per 100 [{pci(cn["ci"])}] (Top 6 {cn["top6"]}, Rest {cn["rest"]}, {ci(cn["gap_ci"])}). '
  f'The other {calm["other_new"]["n"]} smokes hold {calm["other_new"]["deaths"]} of the {calm["total_deaths"]} deaths. Counting track deaths instead: {cnt["deaths"]} deaths, {cnt["per_100"]} per 100 in calm smokes, of {calm["total_track_deaths"]} in all.\n')
aw, awo = ra[A_ + ': with'], ra[A_ + ': without']; lv_ = ra[A_ + ': with, level']
W(f'**Top 6 or Shared:** The condition is Shared: radar reaches both groups equally often. The outcome is a Top 6 pattern: with a covered ship radar-lit, Top 6 lose {aw["top6"]} per 100 and Rest {aw["rest"]} ({ci(aw["gap_ci"])}); at level score {lv_["top6"]} vs {lv_["rest"]} ({ci(lv_["gap_ci"])}). '
  f'Once 50+ behind and radar-lit there is no gap ({ra[A_ + ": with, behind 50+"]["top6"]} vs {ra[A_ + ": with, behind 50+"]["rest"]}, {ci(ra[A_ + ": with, behind 50+"]["gap_ci"])}). Radar-lit deaths in the batch list: Top 6 {rb["top6"]} of {rb["deaths_top6"]}, Rest {rb["rest"]} of {rb["deaths_rest"]}.\n')
W(f'**Clans:**\n- Radar-lit deaths, batch list ({rb["lit40"]}): {rb["clans_text"]}.\n- Radar-lit deaths, all track deaths ({rt["lit40"]}): {rt["clans_text"]}.\n')
W('**Could not be done / proxy:** The replay says a ship is radar-lit, not by whom. The log names the enemy radar that had it in range at that time; where two did, the row is marked ambiguous and the most recent, nearest one is used here. One lit death has no radar in range in the log. '
  f'"Lit in its last 40 s" does not mean radar caused the death: {rb["lit40"] - rb["lit_at_death"]} of the {rb["lit40"]} were no longer lit when they died. Distance is at the start of the lit span.\n')
W('**Verdict:** Lead. Radar-lit deaths are half of all deaths in destroyer smokes, not one in seven; the radar is a cruiser near maximum range; almost none are radar plays from smoke.\n')
W('**Changed from round 5:**\n' + changed([
    ('Radar deaths of 124, last 40 s', '19 strict / 45 broad', rb['lit40'], 'Better data: the full radar log sees ships lit outside the smoke and spans the per-smoke rows missed.'),
    ('Share of deaths radar-lit', '15% strict / 36% broad', f'{rb["lit40_pct"]:.0f}%', 'Same reason.'),
    ('Top 6 / Rest radar deaths', '3 / 16 strict, 5 / 40 broad', f'{rb["top6"]} / {rb["rest"]}', 'Same reason.'),
    ('Deaths with the radar ship and distance known', 19, rb['attributed'], 'The log attributes every lit span.'),
    ('Median distance from the radar ship, km', 10.0, rb['dist_km']['median'], 'More deaths; the extra ones are a little closer.'),
    ('Median distance as a share of radar range, %', 85.0, rb['share_of_range']['median'], 'More deaths; same picture (edge of range).'),
    ('Radar ship class', 'cruiser 16, destroyer 3', ', '.join(f'{k} {v}' for k, v in rb['src_class'].items()), 'More deaths.'),
    ('Moskva as the radar ship', 6, rb['src_ship'].get('Moskva', 0), 'More deaths.'),
    ('Smokes with radar', '120 strict / 297 broad', f'{aw["n"]} (any covered ship lit while the smoke stood); {ra[B_ + ": with"]["n"]} (lit inside the smoke)', 'The log counts ships lit out of cover too.'),
    ('Deaths per 100 with / without radar', '25.0 / 9.9 strict; 27.9 / 5.3 broad', f'{aw["per_100"]} / {awo["per_100"]} (any covered ship); {ra[B_ + ": with"]["per_100"]} / {ra[B_ + ": without"]["per_100"]} (inside the smoke)', 'The strict reading is confirmed. The wide log reading adds smokes where a ship was lit out of cover, which are less deadly.'),
    ('Calm smokes', '585 smokes, 17 deaths, 2.9 per 100', f'{cn["n"]} smokes, {cn["deaths"]} deaths, {cn["per_100"]} per 100', f'Radar taken from the log: {co["n"] - cn["n"]} fewer smokes count as radar-free.'),
    ('Radar plays from smoke, time lit, ambiguity', 'not available', f'{rb["src_in_smoke"]} of {rb["attributed"]} from smoke; lit a median {rb["lit_for_s"]["median"]} s; {rb["ambiguous"]} ambiguous', 'New fields.'),
    ('Time-of-game split', 'strict 4 / 7 / 5 / 3', ' / '.join(str(rb['by_time'].get(k, 0)) for k in ('0-5 min', '5-10 min', '10-15 min', '15-20 min')), 'More deaths; and 17 smokes in two 15-minute-clock games had their times corrected in r5lib.'),
]) + '\n')
chk(f'Radar-lit deaths {rb["lit40"]} of 124 (40 s), {rb["lit20"]} (20 s)', 'n2_radar.py', 'out-radar.json: batch')
chk(f'Radar-lit deaths, track deaths {rt["lit40"]} of {rt["deaths"]}', 'n2_radar.py', 'out-radar.json: track')
chk('Radar ship, class, distance, share of range, ambiguous, from smoke, time lit', 'n2_radar.py', 'out-radar.json: batch / track (src_class, src_ship, dist_km, share_of_range, ambiguous, src_in_smoke, lit_for_s)')
chk('Death by death against strict and broad', 'n2_radar.py', 'out-radar.json: vs_round5_deaths, strict_check')
chk(f'Rates with / without radar ({aw["per_100"]} / {awo["per_100"]}), by score state', 'n2_radar.py', 'out-radar.json: rates, rate_diffs')
chk('Round 5 strict 25.0 / 9.9 and broad 27.9 / 5.3 reproduced', 'n2_radar.py', 'out-radar.json: rates.old_strict, rates.old_broad')
chk('Smoke by smoke comparison', 'n2_radar.py', 'out-radar.json: smoke_by_smoke, log_only')
chk(f'Calm smokes {cn["n"]} / {cn["deaths"]} / {cn["per_100"]} (round 5 definition reproduced: {co["n"]} / {co["deaths"]} / {co["per_100"]})', 'n2_radar.py', 'out-radar.json: calm')

W('## Figures (working, in `round5b/figures/`)\n')
W('- `n2-danger-<map>` (7): died or hurt per 100 by area, top row keyed on the smoke centre, bottom row keyed on where the ship was hit.\n- `n2-deaths-<map>` (7): death positions, filled = inside the smoke outline.\n- `n2-leaving-the-smoke`: where ships died, and leaving against staying.\n- `n2-radar-deaths`: distance to the radar ship as a share of range, and rates with and without radar.\n')
text = '\n'.join(O)
open(os.path.join(HERE_, 'FINDINGS-N2.md'), 'w', encoding='utf-8').write(text + '\n')
ck = ['# CHECK-N2: where each number comes from\n', 'All scripts are in `round5b/new-n2/`; run with `python -I -X utf8 <script>`. Order: n2_health.py, n2_danger.py (about 20 minutes: placebo), n2_leave.py, n2_radar.py, then n2_write.py. `n2lib.py` holds the shared ship-smoke pairs (real health, positions, radar flags).\n',
      tab(['number', 'script', 'where'], CH), '',
      '## Second-way checks\n',
      f'- Round 5 baselines reproduced from the round 5 fields on the new batch: destroyer {H["check_r5"]["d_smoker_per_100_smokes"]} / {H["check_r5"]["hurt_smoker_per_100_smokes"]}, cruisers {H["check_r5"]["cr_died"]} / {H["check_r5"]["cr_hurt"]} (round 5: 6.4 / 15.5, 8.0 / 22.0). `n2_health.py`, check_r5.',
      f'- Old estimate against real health on the same pairs before trusting either: agreement {H["agreement"]["all"]["agree_pct"]}% over {H["agreement"]["all"]["n"]} pairs. `n2_health.py`, agreement.',
      f'- Batch deaths confirmed by the tracks: {dc["batch_confirmed_by_track"]} of {dc["batch"]}. `n2_health.py`, deaths_check.',
      f'- Round 5 danger flags recomputed with round 5 outcomes on the round 5b units: {len(D["r5_recomputed"]["flagged"])} of the 4 (the fourth lost a smoke to the single-replay exclusion). `n2_danger.py`, r5_recomputed.',
      f'- Round 5 strict and broad radar rates and the calm statistic reproduced exactly from the old fields (25.0 / 9.9, 27.9 / 5.3, 585 / 17 / 2.9). `n2_radar.py`.',
      f'- Strict radar deaths: same radar ship in {R["strict_check"]["same_radar_ship"]} of {R["strict_check"]["n"]}, median distance difference {R["strict_check"]["median_abs_diff_m"]} m between the round 5 field and the log. `n2_radar.py`, strict_check.',
      f'- Deaths inside a standing smoke counted two ways (death classing and the exposure walk): {tdj["smoking destroyer"]["classes"][CL[0]]["n"] + tdj["sheltering cruiser"]["classes"][CL[0]]["n"]} and {ev["died_inside"]}. `n2_leave.py`.', '']
open(os.path.join(HERE_, 'CHECK-N2.md'), 'w', encoding='utf-8').write('\n'.join(ck))
json.dump(dict(batch='output/20261117-230933', frame='destroyer smokes (1,074), as in round 5 A2', definitions=dict(
    died='track death between activation and 20 s after dispersal', hurt='died, or net health loss over the smoke of 1/3+ of full health (real health)',
    classes='inside = last position within a standing puff; left = moved outside every puff while they stood; dispersed = puffs ended around the ship; never inside',
    radar='radar log lit spans overlapping the last 40 s (or 20 s) before death; smoke-level: a covered ship lit between activation and dispersal'),
    health=H, death_positions=D['death_pos'], leaving=LV, radar=R), open(os.path.join(HERE_, 'deaths.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote FINDINGS-N2.md, CHECK-N2.md, deaths.json')
