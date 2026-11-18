# Writes FINDINGS-N3.md, CHECK-N3.md and ships-and-loop.json from b3.json and c5.json.
# Run after b3_shots.py and c5_loop.py: python -I -X utf8 n3_findings.py
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, 'b3.json'), encoding='utf-8'))
Cj = json.load(open(os.path.join(HERE, 'c5.json'), encoding='utf-8'))
CK = []          # (number, script, where)
def ck(num, script, where): CK.append((num, script, where))
def tbl(header, rows):
    return '\n'.join(['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])
def ci(c, star=True):
    if not c: return '-'
    return f'{c[0]:+.1f} to {c[1]:+.1f}' + (' *' if star and c[0] * c[1] > 0 else '')
def ci0(c):
    return '-' if not c else f'{c[0]:.0f} to {c[1]:.0f}'
def p0(x): return '-' if x is None else f'{x:.0f}%'
def sm(n): return ' (small n)' if 8 <= n < 15 else ''
SH = ('Harugumo', 'Somers', 'Gearing')
base = B['base']; NR = B['cats']['nearest']; SP = B['cats']['spotter']; DET = B['cats']['detected']; RAD = B['cats']['radar']; CAND = B['cats']['candidates']
def con(key, what, vs, weight):
    return next(x for x in B[key + '_contrasts'] if x['what'] == what and x['vs'] == vs and x['weight'] == weight)
def contxt(key, what, vs, weight='shots'):
    x = con(key, what, vs, weight)
    return f"{x['diff']:+.1f} ({ci(x['ci'])})" + (', clear' if x['clear'] else ', not clear')

# round 5 numbers (round5/FINDINGS.md, B3 "Who spots for the Harugumo?" and C5-LP-4)
R5N = {'Harugumo': dict(n=53, v=[42, 25, 21, 8, 6]), 'Somers': dict(n=30, v=[17, 17, 53, 3, 10]), 'Gearing': dict(n=18, v=[17, 0, 83, 0, 0])}
R5D2 = {'Harugumo': (59.0, 33.0, 12.0), 'Somers': (45.8, 22.7, 5.8), 'Gearing': (37.2, 17.2, 3.9)}
R5C = {'Daring on Loop': (1, 48), 'Daring on other maps': (7, 152), 'Other cap sitters on Loop': (0, 40), 'Other destroyer smokes on Loop': (0, 54), 'All destroyer smokes, all maps': (24, 1074)}

L = []
A = L.append
A('# Round 5b findings, worker n3: Harugumo spotting per shot (B3) and Daring smokes after radar on Loop (C5)')
A('')
A('Batch `output/20261117-230933` (smoke-signals 0.4.0). Scripts in `round5b/new-n3/`. Everything here is association, not cause. Intervals are 95%, from resampling whole clans; a star or the word "clear" means the interval excludes zero. '
  'Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS.')
A('')
# =============================================================== B3
h = base['Harugumo']; so = base['Somers']; ge = base['Gearing']
hn = B['nearest']['Harugumo']; hs = B['spotter']['Harugumo']; hd = B['detected']['Harugumo']; hr = B['radar']['Harugumo']
rc = B['radar_cruiser_inside_split']; rd = B['radar_detail']; d2 = B['second_destroyer']['by_ship']
out_dd = hn[NR[0]]['shots_pct'] + hn[NR[1]]['shots_pct']
A('### B3. Harugumo: who is near, and what lights, its targets at the time of each shot')
A('')
A(f"**Answer:** The round 5 reading mostly holds, with two corrections. Per shot, the nearest friendly ship to a Harugumo's target is a ship outside the smoke or a second destroyer {out_dd:.0f}% of the time "
  f"(round 5 snapshot: 67%), and the radar cruiser sitting in the smoke almost never ({hn[NR[4]]['shots_n']} of {h['shots']} shots). The radar log agrees: only {hr[RAD[0]]['shots_pct']:.0f}% of its shots are at a target lit by a radar ship inside the smoke. "
  f"The corrections: the Harugumo itself is the nearest ship more often than the snapshot said ({hn[NR[2]]['shots_pct']:.0f}%, not 21%), and round 5's \"a second destroyer is recorded more often with a Harugumo\" needs rewording: the snapshot only held ships near the smoke, so \"recorded\" meant \"close by\". A second destroyer is alive at nearly every smoke of all three ships; what differs is that it stays closer to a Harugumo smoke.")
A('')
A('**What was counted.** For every smoke by a Harugumo, Somers, Gearing or Delny, the damage events where the smoker is the attacker and the event is credited to its own smoke (shells, the fires they start, torpedoes), from the run of the smoker\'s own team. '
  'A "shot" is one firing moment at one target. At that moment the tracks give every ship\'s position, the target\'s own track says whether the enemy team was detected, and the radar log says whether it was radar-lit and by which ship.')
A('')
rows = []
for sh in SH + ('Delny',):
    b = base[sh]
    rows.append([sh, b['smokes'], b['smokes_with_own_damage'], b['clans_with_own_damage'], f"{b['top6_smokes_with_own_damage']} / {b['rest_smokes_with_own_damage']}", b['shots'], b['events'], f"{b['damage']:,}", b['targets'], f"{b['top_smoke_share_of_damage_pct']:.0f}%"])
    ck(f"{sh}: {b['shots']} shots, {b['events']} events, {b['damage']:,} damage, {b['smokes_with_own_damage']} smokes", 'b3_shots.py', f"b3.json base.{sh}")
A('**Numbers (what there is to count):**')
A('')
A(tbl(['Ship', 'Smokes', 'Smokes with own-gun damage', 'Clans in those', 'Top 6 / Rest smokes', 'Shots', 'Damage events', 'Own-gun damage', 'Smoke-target pairs', 'Largest single smoke, share of damage'], rows))
A('')
A(f"Delny has {base['Delny']['shots']} shots: too few, not reported further. Somers and Gearing rest on {so['shots']} and {ge['shots']} shots from {so['smokes_with_own_damage']} and {ge['smokes_with_own_damage']} smokes, so their intervals are wide.")
A('')
A('**Numbers (nearest friendly ship to the target, at each shot).** Three weightings: share of shots, share of own-gun damage, and the average of each smoke\'s own split (so one long burst counts once).')
A('')
rows = []
for c in NR:
    r = [c[0].upper() + c[1:]]
    for sh in SH:
        x = B['nearest'][sh][c]
        r.append(f"{x['shots_pct']:.0f}% ({x['shots_n']}; {ci0(x.get('shots_ci'))}) / {x['damage_pct']:.0f}% / {x['per_smoke_pct']:.0f}%")
        ck(f"{sh} nearest = {c}: {x['shots_pct']}% shots ({x['shots_n']}), {x['damage_pct']}% damage, {x['per_smoke_pct']}% per smoke", 'b3_shots.py', f"b3.json nearest.{sh}")
    rows.append(r)
A(tbl(['Nearest friendly ship to the target'] + [f"{sh}: shots (n; interval) / damage / per smoke" for sh in SH], rows))
A('')
A(f"- Median distance from that nearest ship to the target: Harugumo {rd['Harugumo']['median_nearest_ally_m'] / 1000:.1f} km, Somers {rd['Somers']['median_nearest_ally_m'] / 1000:.1f} km, Gearing {rd['Gearing']['median_nearest_ally_m'] / 1000:.1f} km. "
  f"Median range from the smoker to its target: {rd['Harugumo']['median_range_to_target_m'] / 1000:.1f} / {rd['Somers']['median_range_to_target_m'] / 1000:.1f} / {rd['Gearing']['median_range_to_target_m'] / 1000:.1f} km. The Harugumo shoots from further away.")
A(f"- Harugumo minus Somers, share of shots: a ship outside {contxt('nearest', NR[0], 'Somers')}; second destroyer {contxt('nearest', NR[1], 'Somers')}; the smoker itself {contxt('nearest', NR[2], 'Somers')} "
  f"(per smoke {contxt('nearest', NR[2], 'Somers', 'per smoke')}); radar cruiser inside {contxt('nearest', NR[4], 'Somers')}.")
A(f"- Harugumo minus Gearing, share of shots: a ship outside {contxt('nearest', NR[0], 'Gearing')}; second destroyer {contxt('nearest', NR[1], 'Gearing')}; the smoker itself {contxt('nearest', NR[2], 'Gearing')}.")
A('- "In or behind the smoke" here is geometric at the firing moment (inside the smoke, or within 3 km of it with the smoke on the line to the target). Round 5 used the batch label, which also counted any ship that had the smoke in its line of fire at some time in the smoke\'s life.')
ck('nearest contrasts Harugumo minus Somers / Gearing', 'b3_shots.py', 'b3.json nearest_contrasts')
A('')
A('**Numbers (was the target detected, and was it radar-lit, at each shot):**')
A('')
rows = []
for lab, key, cats in (('Radar-lit at the shot', 'detected', [DET[0]]), ('... by a radar ship inside this smoke', 'radar', [RAD[0]]), ('... by a radar ship elsewhere', 'radar', [RAD[1]]),
                       ('Detected, not radar-lit', 'detected', [DET[1]]), ('Not detected at the shot', 'detected', [DET[2]])):
    r = [lab]
    for sh in SH:
        x = B[key][sh][cats[0]]
        r.append(f"{x['shots_pct']:.0f}% ({x['shots_n']}; {ci0(x.get('shots_ci'))}) / {x['damage_pct']:.0f}% / {x['per_smoke_pct']:.0f}%")
        ck(f"{sh} {lab}: {x['shots_pct']}% shots ({x['shots_n']}), {x['damage_pct']}% damage, {x['per_smoke_pct']}% per smoke", 'b3_shots.py', f"b3.json {key}.{sh}")
    rows.append(r)
A(tbl(['At the shot, the target was'] + [f"{sh}: shots (n; interval) / damage / per smoke" for sh in SH], rows))
A('')
x = rc['Harugumo']
A(f"- The direct test of \"the radar cruiser inside spots for it\": {x['shots_with_radar_cruiser_inside']} Harugumo shots came from {x['smokes_with']} smokes that had a radar cruiser inside. In {x['of_those_radar_lit_from_inside_n']} of them ({x['of_those_radar_lit_from_inside_pct']:.0f}%) the target was lit by a radar ship inside that smoke at the shot; "
  f"in {x['of_those_radar_lit_any_pct']:.0f}% it was radar-lit by anyone. Without a radar cruiser inside ({x['shots_without']} shots, {x['smokes_without']} smokes) {x['without_radar_lit_any_pct']:.0f}% were radar-lit. "
  f"Somers: {rc['Somers']['of_those_radar_lit_from_inside_n']} of {rc['Somers']['shots_with_radar_cruiser_inside']} shots ({p0(rc['Somers']['of_those_radar_lit_from_inside_pct'])}). Gearing: {rc['Gearing']['of_those_radar_lit_from_inside_n']} of {rc['Gearing']['shots_with_radar_cruiser_inside']}"
  + (f" ({p0(rc['Gearing']['of_those_radar_lit_from_inside_pct'])}, small n)." if rc['Gearing']['of_those_radar_lit_from_inside_pct'] is not None else ' (too few).'))
ck(f"Harugumo shots with radar cruiser inside {x['shots_with_radar_cruiser_inside']}, lit from inside {x['of_those_radar_lit_from_inside_n']}", 'b3_shots.py', 'b3.json radar_cruiser_inside_split')
x = rd['Harugumo']
A(f"- When a Harugumo target is radar-lit ({x['radar_lit_shots']} shots), the radar ship is elsewhere on the map in {x['elsewhere']} and inside the smoke in {x['from_inside']} (all cruisers); {x['unattributed']} could not be attributed and {x['ambiguous']} had more than one possible radar. "
  f"Radar ships: {', '.join(f'{k} {v}' for k, v in x['source_ships'].items())}. Hydro lit the target in {x['hydro_lit_shots']} shots.")
ck(f"Harugumo radar-lit shots {x['radar_lit_shots']}: elsewhere {x['elsewhere']}, inside {x['from_inside']}", 'b3_shots.py', 'b3.json radar_detail.Harugumo')
A(f"- Most shots are at targets that are detected without radar ({hd[DET[1]]['shots_pct']:.0f}% of Harugumo shots). For those, the nearest friendly ship is a ship outside the smoke in {hs[SP[2]]['shots_n']}, a second destroyer in {hs[SP[3]]['shots_n']}, "
  f"the Harugumo itself in {hs[SP[4]]['shots_n']}, the radar cruiser inside in {hs[SP[6]]['shots_n']}. A ship sitting in smoke does not see out of it beyond about 2 km, so \"the smoker itself is nearest\" does not mean the smoker spotted; it means no friendly ship was closer.")
ck('Harugumo detected-no-radar by nearest ally', 'b3_shots.py', 'b3.json spotter.Harugumo')
cd = B['candidates']
A(f"- A second stand-in: is there a friendly ship outside the smoke within the target's own listed detection range? Harugumo: a second destroyer is the closest such ship in {cd['Harugumo'][CAND[0]]['shots_pct']:.0f}% of shots, another ship in {cd['Harugumo'][CAND[1]]['shots_pct']:.0f}%, "
  f"nobody in {cd['Harugumo'][CAND[3]]['shots_pct']:.0f}%. Somers {cd['Somers'][CAND[0]]['shots_pct']:.0f}% / {cd['Somers'][CAND[1]]['shots_pct']:.0f}% / {cd['Somers'][CAND[3]]['shots_pct']:.0f}%. "
  f"Gearing {cd['Gearing'][CAND[0]]['shots_pct']:.0f}% / {cd['Gearing'][CAND[1]]['shots_pct']:.0f}% / {cd['Gearing'][CAND[3]]['shots_pct']:.0f}%. Harugumo minus Gearing, nobody in range: {contxt('candidates', CAND[3], 'Gearing')}.")
ck('candidate spotters within the target detection range', 'b3_shots.py', 'b3.json candidates')
nd = B['not_detected_detail']
A(f"- \"Not detected at the shot\" ({hd[DET[2]]['shots_pct']:.0f}% of Harugumo shots, {hd[DET[2]]['damage_pct']:.0f}% of damage): by damage this is " + ', '.join(f"{k} {v:.0f}%" for k, v in sorted(nd['Harugumo']['by_kind_pct'].items(), key=lambda x: -x[1]))
  + f" for the Harugumo, and torpedoes {nd['Somers']['by_kind_pct'].get('torpedo', 0):.0f}% for the Somers. Torpedoes are launched at ships nobody sees, and fire ticks keep landing after the target goes dark; the shell part is blind fire or the 2 s sampling step.")
ck('not detected at the shot, by kind', 'b3_shots.py', 'b3.json not_detected_detail')
A('')
A('**Numbers (the second destroyer).** "Second destroyer" = the allied destroyer nearest to the smoke, other than the smoker.')
A('')
rows = []
def lf(sh, k): return f"{d2[sh]['life_' + k + '_pct']:.0f}% ({ci0(d2[sh]['life_' + k + '_ci'])})"
for lab, f in (('Shots with a second destroyer alive', lambda sh: f"{d2[sh]['with_second_dd_pct']:.0f}% ({d2[sh]['with_second_dd_alive']} of {d2[sh]['shots']})"),
               ('At the shot: its median distance to the smoke', lambda sh: f"{d2[sh]['median_dist_to_smoke_m'] / 1000:.1f} km"),
               ('At the shot: within 3 km of the smoke', lambda sh: f"{d2[sh]['within_3km_pct']:.0f}%"), ('At the shot: within 5 km', lambda sh: f"{d2[sh]['within_5km_pct']:.0f}%"),
               ('At the shot: 1 km or more forward of the smoke', lambda sh: f"{d2[sh]['forward_1km_pct_of_shots']:.0f}%"), ('At the shot: in or behind the smoke', lambda sh: f"{d2[sh]['in_or_behind_pct_of_shots']:.0f}%"),
               ('At the shot: sitting in a cap', lambda sh: f"{d2[sh]['at_a_cap_pct_of_shots']:.0f}%"),
               ('Smoke life: share of standing time with an allied destroyer within 3 km (all smokes)', lambda sh: lf(sh, '3km')), ('Smoke life: within 5 km', lambda sh: lf(sh, '5km')),
               ('Smoke life: within 5 km and 1 km+ forward', lambda sh: lf(sh, 'fwd5')), ('Smoke life: 1 km+ forward at any distance', lambda sh: lf(sh, 'fwd')), ('Smoke life: inside the smoke', lambda sh: lf(sh, 'in')),
               ('Smoke life: an allied second destroyer alive at all', lambda sh: lf(sh, 'alive'))):
    rows.append([lab] + [f(sh) for sh in SH])
A(tbl(['Measure'] + [f"{sh} ({d2[sh]['shots']} shots, {d2[sh]['smokes']} smokes)" for sh in SH], rows))
for sh in SH: ck(f"{sh} second destroyer: 3 km life {d2[sh]['life_3km_pct']}%, 5 km {d2[sh]['life_5km_pct']}%, at shot within 5 km {d2[sh]['within_5km_pct']}%", 'b3_shots.py', f'b3.json second_destroyer.by_ship.{sh}')
A('')
dc = B['second_destroyer']['contrasts']
def dcx(what, vs):
    x = next(x for x in dc if x['what'] == what and x['vs'] == vs); return f"{x['diff']:+.1f} ({ci(x['ci'])})" + (', clear' if x['clear'] else ', not clear')
A(f"- Over the smoke's life, Harugumo minus Somers: within 3 km {dcx('life_3km', 'Somers')}; within 5 km {dcx('life_5km', 'Somers')}; within 5 km and forward {dcx('life_fwd5', 'Somers')}. "
  f"Harugumo minus Gearing: within 3 km {dcx('life_3km', 'Gearing')}; within 5 km {dcx('life_5km', 'Gearing')}; within 5 km and forward {dcx('life_fwd5', 'Gearing')}.")
A(f"- At the shot, Harugumo minus Somers: within 5 km {dcx('shot: second destroyer within 5 km of the smoke', 'Somers')}; 1 km+ forward {dcx('shot: second destroyer 1 km+ forward', 'Somers')}. "
  f"Harugumo minus Gearing: within 5 km {dcx('shot: second destroyer within 5 km of the smoke', 'Gearing')}; in or behind the smoke {dcx('shot: second destroyer in or behind the smoke', 'Gearing')}. Per-shot gaps are mostly not clear because few clans supply the Somers and Gearing shots.")
A(f"- The Harugumo's second destroyer is most often a {', '.join(f'{k} ({v} shots)' for k, v in list(d2['Harugumo']['ships'].items())[:4])}.")
ck('second destroyer contrasts', 'b3_shots.py', 'b3.json second_destroyer.contrasts')
A('')
t = B['harugumo_top6_vs_rest']; tn = t['n']
def trow(what): return next(x for x in t['rows'] if x['what'] == what)
A(f"**Top 6 or Shared:** Shared, with one lead. Harugumo shots: Top 6 {tn['top6_shots']} from {tn['top6_smokes']} smokes ({tn['top6_clans']} clans), Rest {tn['rest_shots']} from {tn['rest_smokes']} smokes ({tn['rest_clans']} clans). "
  f"Nearest ship a ship outside the smoke: Top 6 {trow(NR[0])['top6_pct']:.0f}% vs Rest {trow(NR[0])['rest_pct']:.0f}%, {trow(NR[0])['diff']:+.1f} ({ci(trow(NR[0])['ci'])}). Second destroyer: {trow(NR[1])['top6_pct']:.0f}% vs {trow(NR[1])['rest_pct']:.0f}%, {trow(NR[1])['diff']:+.1f} ({ci(trow(NR[1])['ci'])}). "
  f"The smoker itself: {trow(NR[2])['top6_pct']:.0f}% vs {trow(NR[2])['rest_pct']:.0f}%, {trow(NR[2])['diff']:+.1f} ({ci(trow(NR[2])['ci'])}). None clear. "
  f"The one clear gap: the target is radar-lit by a radar ship elsewhere in {trow(RAD[1])['top6_pct']:.0f}% of Top 6 shots against {trow(RAD[1])['rest_pct']:.0f}% of Rest shots, {trow(RAD[1])['diff']:+.1f} ({ci(trow(RAD[1])['ci'])}); "
  f"per smoke {trow(RAD[1])['top6_per_smoke_pct']:.0f}% vs {trow(RAD[1])['rest_per_smoke_pct']:.0f}%, {trow(RAD[1])['per_smoke_diff']:+.1f} ({ci(trow(RAD[1])['per_smoke_ci'])}). "
  f"Top 6 Harugumos shoot more often at targets a friendly radar somewhere else is holding. Four Top 6 clans only, so treat it as a lead.")
ck('Harugumo Top 6 vs Rest rows', 'b3_shots.py', 'b3.json harugumo_top6_vs_rest')
g = B['second_destroyer']['harugumo_top6_vs_rest']
A(f"Second destroyer within 5 km over the smoke's life: Top 6 {g[2]['top6']:.0f}% (n {g[2]['n_top6']}) vs Rest {g[2]['rest']:.0f}% (n {g[2]['n_rest']}), {g[2]['diff']:+.1f} ({ci(g[2]['ci'])}), not clear.")
A('')
A(f"**Clans (smokes with own-gun damage):** Harugumo: {h['clans_txt']}. Somers: {so['clans_txt']}. Gearing: {ge['clans_txt']}.")
A('')
A('**Biggest Harugumo own-gun smokes (share of that smoke\'s own-gun damage by what the data shows at the shot):**')
A('')
for e in B['examples'][:6]:
    A(f"- [{e['team']}, {e['map']}, {e['time']}]({e['link']}): {e['own_damage']:,} in {e['shots']} shots, radar cruiser inside: {'yes' if e['radar_cruiser_inside'] else 'no'}. " + '; '.join(f'{k} {v}%' for k, v in e['by_spotter'].items()) + '.')
A('')
A('**Could not be done / proxy:** Spotting still cannot be proven. The replay does not say which ship\'s sight a shot used. What the data gives is: the target was detected at the shot (its own track), it was or was not radar-lit and by which radar ship (attributed by range and time, a few ambiguous), and which friendly ship was nearest. '
  'Positions are sampled every 2 s. Smoke shape is the final laid path, so "inside the smoke" is slightly generous while a smoke is still being laid. Fire ticks are counted at the tick, not at the shell that started the fire.')
A('')
A('**Verdict:** Keep.')
A('')
A('**Changed from round 5:**')
A('')
rows = []
for i, c in enumerate(NR):
    for sh in SH:
        o = R5N[sh]['v'][i]; n = B['nearest'][sh][c]['shots_pct']
        rows.append([f'{sh}: nearest friendly ship is {c}', f"{o}% of {R5N[sh]['n']} targets", f"{n:.0f}% of {base[sh]['shots']} shots", f'{n - o:+.0f} points'])
A(tbl(['Number', 'Round 5 (one snapshot per smoke)', 'Round 5b (per shot)', 'Difference'], rows))
A('')
ch = B['check_snapshot']['Harugumo']
A(f"- Why: better data and a different unit. Round 5 looked once per smoke, at the moment it was fully laid, and only at targets whose position the snapshot happened to hold ({ch['round5_targets_with_position']} of {ch['targets']} Harugumo targets). "
  f"Round 5b looks at every shot with every ship's position. Redoing the round 5 question with the tracks at the same single moment, same targets and same rule gives {', '.join(f'{k} {v}' for k, v in ch['tracks_same_rule'].items())} of {ch['tracks_targets_with_position']}; "
  f"{ch['same_role_same_rule']} of the {ch['round5_targets_with_position']} shared targets get the same answer. So part of the shift is the 15 targets round 5 could not place, and part is shots fired later in the smoke's life.")
ck(f"snapshot check Harugumo: {ch['same_role_same_rule']} of {ch['round5_targets_with_position']} same", 'b3_shots.py', 'b3.json check_snapshot.Harugumo')
A(f"- Harugumo \"ship outside the smoke or a second destroyer\": 67% -> {out_dd:.0f}% ({out_dd - 67:+.0f}). \"The radar cruiser inside\": 6% -> {hn[NR[4]]['shots_pct']:.1f}%. \"The smoker itself\": 21% -> {hn[NR[2]]['shots_pct']:.0f}%. "
  f"The Harugumo against Somers gap on \"the smoker itself\" was -32.6 (clear) and is now {contxt('nearest', NR[2], 'Somers')} by shots, {contxt('nearest', NR[2], 'Somers', 'per smoke')} per smoke.")
rows = []
for sh in SH:
    o = R5D2[sh]; d = d2[sh]
    rows.append([sh, f'{o[0]}%', f"{d['at_capture_tracks_dd2_pct']:.1f}%", f"{d['at_capture_tracks_dd2_pct'] - o[0]:+.1f}", f'{o[1]}%', f"{d['at_capture_tracks_dd2_fwd_pct']:.1f}%", f"{d['at_capture_tracks_dd2_fwd_pct'] - o[1]:+.1f}", f"{d['at_capture_agree']} of {d['smokes']}"])
    ck(f"{sh} second destroyer alive at the fully-laid moment (tracks) {d['at_capture_tracks_dd2_pct']}%, forward {d['at_capture_tracks_dd2_fwd_pct']}%", 'b3_shots.py', f'b3.json second_destroyer.by_ship.{sh}.at_capture_*')
A('')
A(tbl(['Ship', 'Second destroyer recorded, round 5', 'Second destroyer alive at the same moment, tracks', 'Difference', '1 km+ forward, round 5', '1 km+ forward, tracks', 'Difference', 'Smokes where the two agree on "recorded"'], rows))
A('')
A('- Why: the round 5 snapshot held only some of the ships (about 3 to 4 allied ships of up to 9 alive, the ones near the smoke), so "recorded" really meant "close enough to be in the snapshot". With full tracks a second allied destroyer is alive at almost every smoke of all three ships, so the round 5 gaps (+13.2 and +21.8 recorded; +10.3 and +15.8 forward) are not gaps in whether one exists. '
  f"They are gaps in distance, and that part holds: an allied destroyer is within 5 km of the smoke for {d2['Harugumo']['life_5km_pct']:.0f}% of a Harugumo smoke's standing time, against {d2['Somers']['life_5km_pct']:.0f}% (Somers) and {d2['Gearing']['life_5km_pct']:.0f}% (Gearing), both clear. Different definition, better data.")
A('- Library fix during this round: 17 smokes in two games (15-minute clock) had round 5 elapsed times 300 s too high. Nothing in B3 uses those fields (all times are the exact `e0` / `e1` and the damage event clocks), so no B3 number moved for that reason; the scripts were rerun after the fix.')
A(f"- New in round 5b (no round 5 number): radar-lit at the shot, {hd[DET[0]]['shots_pct']:.0f}% of Harugumo shots, of which from inside the smoke {hr[RAD[0]]['shots_pct']:.0f}%.")
A('')
A('**Self-checks:**')
A('')
cd_ = B['check_damage']
A('- Damage total a second way: credited events against the smoke records (smoker\'s own damage, all of it): ' + '; '.join(f"{sh} {cd_[sh]['events_damage']:,} vs {cd_[sh]['smoke_records_smoker_damage']:,}" for sh in SH) + '.')
ck('events damage vs smoke records', 'b3_shots.py', 'b3.json check_damage')
ca = B['check_radar_inside']
A('- "Radar-lit from inside this smoke" a second way (the radar log\'s own source-in-smoke flag instead of track geometry): ' + '; '.join(f"{sh} {ca[sh]['radar_lit_from_inside_geometry']} vs {ca[sh]['radar_lit_source_in_smoke_flag']} shots" for sh in SH) + '.')
ck('radar inside two ways', 'b3_shots.py', 'b3.json check_radar_inside')
A('')

# =============================================================== C5
G5 = Cj['groups']; dl = G5['Daring on Loop']; SU = Cj['summary']; rev = Cj['reverse']
b60 = dl['before_any_60']; n60 = dl['before_near_60']; a60 = dl['after_near_60']
A('### C5-LP-4. Loop: do Daring smokes follow a friendly radar lighting an enemy destroyer?')
A('')
A(f"**Answer:** No more often than chance. {b60['k']} of {b60['n']} Daring smokes on Loop ({b60['pct']:.0f}%) came within 60 seconds after a friendly radar lit an enemy destroyer somewhere on the map, but a friendly radar has an enemy destroyer lit in the last 60 seconds at {b60['base_pct']:.0f}% of all moments in those games. "
  f"Near the cap the Daring then smoked it is {n60['k']} of {n60['n']} (chance {n60['base_pct']:.0f}%). The reverse reading (smoke first, radar on a destroyer near that cap within 60 s after) is {a60['k']} of {a60['n']}, also at chance.")
A('')
A('**What was counted.** The radar log now has every radar activation and every enemy ship it lit, with start and end times. For each destroyer smoke: was there a lit span on an enemy destroyer, attributed to a radar of the smoking team, that overlaps the 60 s (30 s, 90 s) before the smoke was activated. '
  '"Near the cap" = while that destroyer was within 3 km of the edge of the cap nearest to the smoke. Chance = the share of all moments between the game\'s first and last smoke (cut at the smoker\'s death) at which the same test is true; it is computed exactly, not by random draws. '
  'The round 5 control windows are kept too: 120 to 60 s before, and 60 to 120 s after.')
A('')
def cell(c, base=True):
    if 'pct' not in c: return f"{c['k']} of {c['n']} (too few)"
    s = f"{c['k']} ({c['pct']:.0f}%, {ci0(c['ci'])})"
    if base and 'base_pct' in c: s += f"; chance {c['base_pct']:.0f}%; gap {c['minus_base']:+.1f} ({ci(c.get('minus_base_ci'))})"
    return s
ORDER = ['Daring on Loop', 'Daring on other maps', 'Other cap sitters on Loop', 'Other destroyer smokes on Loop', 'All destroyer smokes, all maps']
A('**Numbers (a friendly radar lit an enemy destroyer anywhere on the map):**')
A('')
rows = [[k, G5[k]['n'], G5[k]['clans'], cell(G5[k]['before_any_30']), cell(G5[k]['before_any_60']), cell(G5[k]['before_any_90']), cell(G5[k]['earlier_any']), cell(G5[k]['later_any'])] for k in ORDER]
A(tbl(['Group', 'Smokes', 'Clans', '30 s before', '60 s before', '90 s before', 'Control: 120 to 60 s before', 'Control: 60 to 120 s after'], rows))
for k in ORDER: ck(f"{k}: 60 s before {G5[k]['before_any_60']['k']} of {G5[k]['n']} ({G5[k]['before_any_60'].get('pct')}%), chance {G5[k]['before_any_60'].get('base_pct')}%", 'c5_loop.py', f'c5.json groups["{k}"].before_any_60')
A('')
A('**Numbers (the lit destroyer was within 3 km of the cap the smoke is nearest to):**')
A('')
rows = [[k, G5[k]['n'], cell(G5[k]['before_near_30']), cell(G5[k]['before_near_60']), cell(G5[k]['before_near_90']), cell(G5[k]['earlier_near']), cell(G5[k]['after_near_60']), cell(G5[k]['afterstart_near_60'])] for k in ORDER]
A(tbl(['Group', 'Smokes', '30 s before', '60 s before', '90 s before', 'Control: 120 to 60 s before', 'Reverse: lit in the 60 s after the smoke', 'Reverse: a new lit span began in the 60 s after'], rows))
for k in ORDER: ck(f"{k}: near cap 60 s before {G5[k]['before_near_60']['k']} of {G5[k]['n']}; after {G5[k]['after_near_60']['k']}", 'c5_loop.py', f'c5.json groups["{k}"].before_near_60 / after_near_60')
A('')
def tst(measure, contrast):
    x = next(x for x in Cj['tests'] if x['measure'] == measure and x['contrast'] == contrast); return f"{x['diff']:+.1f} ({ci(x['ci'])})"
e1 = dl['before_any_60_minus_earlier_any']; e2 = dl['before_any_60_minus_later_any']
A(f"- Daring on Loop, 60 s before against the round 5 control windows: against 120 to 60 s before {e1['diff']:+.1f} ({ci(e1['ci'])}); against 60 to 120 s after {e2['diff']:+.1f} ({ci(e2['ci'])}). No rise just before the smoke. The 60 s before is higher than the window well after the smoke, but Daring smokes on other maps show the same ({G5['Daring on other maps']['before_any_60_minus_later_any']['diff']:+.1f}, {ci(G5['Daring on other maps']['before_any_60_minus_later_any']['ci'])}), so it is not a Loop pattern.")
A(f"- Daring on Loop minus Daring on other maps, anywhere, 60 s: {tst('before_any_60', 'Daring on Loop minus Daring on other maps')}. Minus other cap sitters on Loop: {tst('before_any_60', 'Daring on Loop minus Other cap sitters on Loop')}. "
  f"Near the cap, 60 s: {tst('before_near_60', 'Daring on Loop minus Daring on other maps')} and {tst('before_near_60', 'Daring on Loop minus Other cap sitters on Loop')}: Daring smokes on Loop follow radar near their cap less often than the comparison groups, as round 5 suggested.")
A(f"- After taking chance out, anywhere 60 s: Daring on Loop minus Daring on other maps {tst('before_any_60 minus base', 'Daring on Loop minus Daring on other maps')}; minus other cap sitters on Loop {tst('before_any_60 minus base', 'Daring on Loop minus Other cap sitters on Loop')}. Nothing.")
A(f"- Reverse reading. Radar lit an enemy destroyer near the cap in the 60 s after the smoke: Daring on Loop {cell(a60)}. Other cap sitters on Loop {cell(G5['Other cap sitters on Loop']['after_near_60'])}; Daring on other maps {cell(G5['Daring on other maps']['after_near_60'])}; "
  f"all destroyer smokes {cell(G5['All destroyer smokes, all maps']['after_near_60'])}. So \"smoke, then a friendly radar lights a destroyer near that cap\" is a real pattern for destroyer smokes in general and for the other cap sitters on Loop, but not for the Daring on Loop.")
A(f"- The other way round, as in round 5: our radar lit an enemy destroyer on Loop in {rev['episodes']} separate episodes for teams with a Daring; a Daring was alive for {rev['with_daring_alive']}; it smoked within 60 s after {rev['followed_60']} ({p0(rev['followed_60_pct'])}). "
  f"Chance for a Daring smoke in any 60 s of its life in those games: {p0(rev['base_followed_60_pct'])}; gap {rev['followed_minus_base']:+.1f} ({ci(rev['followed_minus_base_ci'])}). Within 30 s: {rev['followed_30']}; within 90 s: {rev['followed_90']}.")
ck(f"reverse: {rev['episodes']} episodes, {rev['with_daring_alive']} with Daring alive, {rev['followed_60']} followed; base {rev['base_followed_60_pct']}%", 'c5_loop.py', 'c5.json reverse')
ph = Cj['phase']['Daring on Loop']
A(f"- Phase: Daring smokes on Loop are late (median {ph['median_time']} elapsed, {ph['first_5_min_pct']:.0f}% in the first 5 minutes). After minute 5: {ph['before_any_60_later'].replace('; base ', '; chance ').replace('minus base', 'gap')}.")
A('')
m = SU['matched']; u = SU['not_matched']
A(f"**The typical sequence in the {m['n']} cases that match (60 s, anywhere):**")
A('')
A(f"- Who radared: {', '.join(f'{k} {v}' for k, v in SU['radar_ships'].items())} ({SU['lit_spans']} lit spans; by class: {', '.join(f'{k} {v}' for k, v in SU['radar_class'].items())}). {SU['radar_from_smoke']} of these radars were run from inside a smoke, and {SU['radar_is_the_daring']} by the Daring itself.")
A(f"- From where: the radar ship was a median {SU['median_radar_ship_to_cap_edge_m'] / 1000:.1f} km from the edge of the cap the Daring then smoked (cells: {', '.join(f'{k} {v}' for k, v in list(SU['radar_ship_cells'].items())[:5])}), and the lit destroyer a median {SU['median_target_to_cap_edge_m'] / 1000:.1f} km from that cap "
  f"and {SU['median_target_to_smoke_m'] / 1000:.1f} km from the smoke. In other words, the radar and the Daring smoke are usually on different parts of the map: {m['cap'].get('A', 0)} of the {m['n']} smokes are at cap A, while the radar ships are mostly in {' and '.join(list(SU['radar_ship_cells'])[:2])}, on the other side of the map.")
A(f"- How long before: the first lit span in the window began a median {SU['median_lead_s']:.0f} s before the smoke; the destroyer was still lit when the smoke went up in {SU['still_lit_at_activation_smokes']} of {m['n']}. Lit destroyers: {', '.join(f'{k} {v}' for k, v in list(SU['targets'].items())[:6])}.")
A(f"- Did the cap change hands (from activation to 60 s after the smoke cleared): the cap was ours at activation in {m['cap_owner_at_activation'].get('ours', 0)}, theirs in {m['cap_owner_at_activation'].get('theirs', 0)}, neutral in {m['cap_owner_at_activation'].get('neutral', 0)}. "
  f"We took it in {m['we_took_it']} of the {m['not_ours_at_activation']} not ours; the enemy took it in {m['enemy_took_it']} of the {m['not_theirs_at_activation']} not theirs. "
  f"For the {u['n']} smokes with no radar before: we took {u['we_took_it']} of {u['not_ours_at_activation']}, the enemy took {u['enemy_took_it']} of {u['not_theirs_at_activation']}. Counts too small for rates that differ; no sign that the radar cases end differently.")
A(f"- The Daring was itself detected when it smoked in {m['daring_detected_at_activation']} of {m['detection_known']} matching cases and {u['daring_detected_at_activation']} of {u['detection_known']} others. Median concealed damage {m['median_conc']:,.0f} against {u['median_conc']:,.0f}.")
A(f"- The {SU['matched_near']} cases with the destroyer near the cap:")
for x in Cj['sequences']:
    if x['near']:
        r = min(x['lit'], key=lambda r: abs(r['target_to_cap_edge_m'] or 1e9))
        A(f"  - [{x['team']} Daring, {x['time']}, {x['cell']}, cap {x['cap']} ({x['cap_owner_at_activation']})]({x['link']}): {r['radar_ship']} lit a {r['target']} {r['lit_start_before_s']:.0f} s before; the destroyer was {(r['target_to_smoke_m'] or 0) / 1000:.1f} km from the smoke. Cap changes after: {x['cap_changes_after'] or 'none'}.")
ck(f"sequence summary: {m['n']} matched, radar ships, median lead {SU['median_lead_s']} s", 'c5_loop.py', 'c5.json summary / sequences')
A('')
t = dl['top6_vs_rest_before_any_60']
A(f"**Top 6 or Shared:** Not a spot, and not testable for the Daring on Loop: {t['top6_n']} Top 6 smokes against {t['rest_n']} Rest (too few; {t['top6_k']} of {t['top6_n']} and {t['rest_k']} of {t['rest_n']} match). "
  + ' '.join(f"{k}: Top 6 {G5[k]['top6_vs_rest_before_any_60']['top6']:.0f}% (n {G5[k]['top6_vs_rest_before_any_60']['top6_n']}) vs Rest {G5[k]['top6_vs_rest_before_any_60']['rest']:.0f}% (n {G5[k]['top6_vs_rest_before_any_60']['rest_n']}), "
             f"{G5[k]['top6_vs_rest_before_any_60']['diff']:+.1f} ({ci(G5[k]['top6_vs_rest_before_any_60']['ci'])})." for k in ORDER[1:]))
for k in ORDER[1:]: ck(f"{k} Top 6 vs Rest before_any_60 {G5[k]['top6_vs_rest_before_any_60']['diff']}", 'c5_loop.py', f'c5.json groups["{k}"].top6_vs_rest_before_any_60')
A('')
A(f"**Clans:** Daring on Loop: {dl['clans_txt']}. The {m['n']} matching smokes: {SU['matched_clans']} ({SU['games_matched']} of {SU['games_all']} games).")
A('')
A('**Could not be done / proxy:** Which radar lit a ship is attributed by range and time, not read from the game; none of the spans used here for the Daring on Loop were ambiguous, and adding the unattributed spans changes nothing '
  f"({dl['before_any_60_with_unattributed']['k']} of {dl['before_any_60_with_unattributed']['n']}). The data shows timing only; it cannot show whether the Daring player reacted to the radar. The Daring on Loop is almost all Rest clans, so no Top 6 reading is possible.")
A('')
A('**Verdict:** Drop.')
A('')
A('**Changed from round 5:**')
A('')
rows = []
for k in ORDER:
    o = R5C[k]; n = G5[k]['before_any_60']
    rows.append([k, f"{o[0]} of {o[1]} ({100 * o[0] / o[1]:.0f}%)", f"{n['k']} of {n['n']} ({n['pct']:.0f}%)", f"{n['pct'] - 100 * o[0] / o[1]:+.0f} points", f"{n['base_pct']:.0f}%"])
A(tbl(['Group', 'Round 5: our radar lit an enemy destroyer in the 60 s before (seen only when that destroyer sat in its own smoke)', 'Round 5b: same, every radar and every lit destroyer', 'Difference', 'Round 5b chance level'], rows))
A('')
ckk = Cj['check']
A(f"- Why: better data. Round 5 could see a radar lighting an enemy destroyer only when that destroyer was inside its own team's smoke (9 such rows on Loop). The radar log has {SU['loop_spans']} lit spans on enemy destroyers in the {SU['loop_games']} Loop games. "
  f"The single round 5 case is still there ({ckk['round5_proxy_hits_also_in_radar_log']} of {ckk['round5_proxy_hits']} found again). Round 5 described its target, an A. da Barbiano, as a cruiser; the roster lists it as a destroyer.")
A(f"- Reverse view: round 5 had 9 episodes, a Daring alive for 2, 1 followed by a smoke. Round 5b: {rev['episodes']} episodes, {rev['with_daring_alive']} with a Daring alive, {rev['followed_60']} followed ({p0(rev['followed_60_pct'])} against chance {p0(rev['base_followed_60_pct'])}).")
A('- Library fix during this round: two games ran on a 15-minute clock, so the round 5 elapsed times of their 17 smokes were 300 s too high (one of the two games is on Loop). Every time used here is the exact `e0` / `e1` from the timelines, which never had that error; the only library time field used is the game length in the reverse view, rerun after the fix with no change to any count.')
A('- The verdict does not change (Drop), but the reason does. Round 5 said "not supported, on a thin proxy: 1 of 48". Round 5b says: it happens in about a third of Daring smokes on Loop, and that is exactly what chance gives, because some friendly radar has some enemy destroyer lit about a third of the time.')
A('')
A('**Self-checks:**')
A('')
A(f"- Headline a second way: counting straight from the radar rows without the helper functions gives {ckk['before_any_60_straight_from_rows']} of 48, the same as {b60['k']}.")
A(f"- Old field against new on the same smokes: the round 5 proxy finds {ckk['round5_proxy_hits']} Daring smoke on Loop; the radar log finds that one and {b60['k'] - ckk['round5_proxy_hits_also_in_radar_log']} more.")
ck('C5 checks', 'c5_loop.py', 'c5.json check')
A('')
A('### Notes on the new files and `tl.py`')
A('')
A('- No bug found in `tl.py`. Two things to know. `GameTL.lit()` returns spans for both teams; filter on `team` (the radar\'s team) as well as `target_team`. `g.ships(team, alive_at=t)` and `Track.pos(t)` worked as described.')
A('- With `python -I` a script\'s own folder is not on the import path, so a helper module beside the script needs its own `sys.path.insert`.')
A('- `damage_events.csv` also carries `flood` and `unknown` rows with a credited smoke; they are not part of smoke damage and were left out, which makes the event total match the smoke records.')
A('- The round 5 `cast` (ships at the fully-laid moment) holds only part of each team (checked on 25 Harugumo smokes: 0 to 6 allied ships in `cast` against 4 to 9 alive in the tracks). Any round 5 number of the form "a ship of type X was recorded" means "recorded near the smoke", not only for the second destroyer.')
A('')
A('### Files')
A('')
A('- Scripts: `n3lib.py`, `b3_shots.py`, `c5_loop.py`, `n3_figs.py`, `n3_findings.py` (run in that order; each with `python -I -X utf8`).')
A('- Data: `b3.json`, `c5.json`, `ships-and-loop.json`, `b3_out.txt`, `c5_out.txt`.')
A('- Figures: `round5b/figures/n3-harugumo-spotter-per-shot.(svg|png)`, `round5b/figures/n3-loop-daring-after-radar.(svg|png)`.')
open(os.path.join(HERE, 'FINDINGS-N3.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

C_ = ['# CHECK-N3: where each number in FINDINGS-N3.md comes from', '', 'All scripts are in `round5b/new-n3/`. `b3.json` and `c5.json` are written by the scripts named; `b3_out.txt` and `c5_out.txt` hold the same tables as printed.', '',
      tbl(['Number', 'Script', 'Where'], [[a.replace('|', '/'), f'`{b}`', f'`{c}`'] for a, b, c in CK]), '',
      'Round 5 numbers quoted in the "Changed from round 5" blocks are copied from `wows-toolkit/smoke/analysis/round5/FINDINGS.md` (B3 "Who spots for the Harugumo?" and the Harugumo table; C5-LP-4 table) and are constants in `n3_findings.py` (`R5N`, `R5D2`, `R5C`).']
open(os.path.join(HERE, 'CHECK-N3.md'), 'w', encoding='utf-8').write('\n'.join(C_) + '\n')

frag = dict(worker='n3', batch='output/20261117-230933',
            B3=dict(title='Harugumo: nearest ally and detection of its targets at each shot', verdict='Keep', mode='shared', data=B,
                    changed_from_round5=dict(nearest_pct_round5={sh: dict(zip(NR, R5N[sh]['v'])) for sh in SH}, nearest_pct_round5b={sh: {c: B['nearest'][sh][c]['shots_pct'] for c in NR} for sh in SH},
                                             second_destroyer_recorded_round5={sh: R5D2[sh][0] for sh in SH}, second_destroyer_alive_at_capture_round5b={sh: d2[sh]['at_capture_tracks_dd2_pct'] for sh in SH},
                                             why='per shot with full tracks instead of one snapshot with partial positions')),
            C5_LP_4=dict(title='Loop: Daring smokes after a friendly radar lit an enemy destroyer', verdict='Drop', mode='not a spot', data=Cj,
                         changed_from_round5=dict(round5={k: dict(k=v[0], n=v[1]) for k, v in R5C.items()}, round5b={k: dict(k=G5[k]['before_any_60']['k'], n=G5[k]['n'], base_pct=G5[k]['before_any_60'].get('base_pct')) for k in ORDER},
                                                  why='full radar log instead of radar seen only on ships inside their own smoke')),
            figures=['figures/n3-harugumo-spotter-per-shot', 'figures/n3-loop-daring-after-radar'])
json.dump(frag, open(os.path.join(HERE, 'ships-and-loop.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', len(L), 'lines;', len(CK), 'check rows')
