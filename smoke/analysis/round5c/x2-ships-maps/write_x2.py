# Round 5c, worker x2: builds FINDINGS-X2.md and CHECK-X2.md from ships-maps.json (run compute_x2.py first).
# Run: python -I -X utf8 write_x2.py
# "Round 5b" comparison numbers: B2 / B3 death rates are read from round5b/part-b/ships.json (round 5 script with the clock fix);
# the cap numbers the round 5 text quoted are typed in below (R5TEXT), each with its place in round5b/FINDINGS.md.
import os, json
X2 = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(X2, 'ships-maps.json'), encoding='utf-8'))
R5B = json.load(open(os.path.join(X2, '..', '..', 'round5b', 'part-b', 'ships.json'), encoding='utf-8'))
OUT = []; CHECK = []
def W(*a): OUT.append(' '.join(str(x) for x in a))
def table(h, rows):
    W('| ' + ' | '.join(h) + ' |'); W('|' + '---|' * len(h))
    for r in rows: W('| ' + ' | '.join(str(c) for c in r) + ' |')
    W('')
def num(x, d=1, sign=False):
    if x is None: return '-'
    return ('{:+,.%df}' % d if sign else '{:,.%df}' % d).format(x)
def fv(o, d=1):
    """value (interval)"""
    if o is None or o['v'] is None: return 'too few'
    return num(o['v'], d) + (f" ({num(o['ci'][0], d)} to {num(o['ci'][1], d)})" if o.get('ci') else '')
def fd(o, d=1):
    """signed gap (interval), clear / not clear"""
    if o is None or o['v'] is None: return 'too few'
    if not o.get('ci'): return num(o['v'], d, True)
    return f"{num(o['v'], d, True)} ({num(o['ci'][0], d, True)} to {num(o['ci'][1], d, True)})" + (', clear' if o['clear'] else '')
def tr(o, d=1):
    """Top 6 vs Rest, gap"""
    if o['top'] is None or o['rest'] is None:
        return f"{num(o['top'], d) if o['top'] is not None else 'too few'} vs {num(o['rest'], d) if o['rest'] is not None else 'too few'}"
    return f"{num(o['top'], d)} vs {num(o['rest'], d)}; {fd(o, d)}"
def kn(o):
    if o['n'] == 0: return '0 of 0'
    if o['n'] < 8: return f"{o['k']} of {o['n']} (too few)"
    return f"{o['k']} of {o['n']} ({o['pct']:.0f}%{', small n' if o['n'] < 15 else ''})"
def tagn(n): return f'{n} (too few)' if n < 8 else f'{n} (small n)' if n < 15 else str(n)
def own(c): return f"{c['ours']} / {c['neutral']} / {c['theirs']}"
def r5b_row(sec, group, split, metric):
    for r in R5B[sec]['rows']:
        if r['group'] == group and r['split'] == split: return r.get(metric), r.get(metric + '_ci')
    raise KeyError((sec, group, split))
def r5b_txt(sec, group, split, metric):
    v, c = r5b_row(sec, group, split, metric)
    if v is None: return 'too few'
    return num(v) + (f' ({num(c[0])} to {num(c[1])})' if c else '')
def r5b_con(sec, contrast, metric):
    contrast = contrast.replace('cruisers with ordinary smoke', 'cruiser ordinary smoke')   # round 5 script wording
    for r in R5B[sec]['contrasts']:
        if r['contrast'] == contrast and r['metric'] == metric:
            return f"{num(r['diff'], 1, True)} ({num(r['ci'][0], 1, True)} to {num(r['ci'][1], 1, True)})" + (', clear' if r['clear'] else '')
    raise KeyError((sec, contrast, metric))
def changed(rows):
    table(['Number', 'Round 5b', 'Round 5c', 'Why'], rows)
def why_cap(old, new):
    """'cap timeline' when the count changed, else say it is the same."""
    return 'cap timeline (same result)' if old.split(' (')[0] == new.split(' (')[0] else 'cap timeline'
def chk(what, value, where):
    CHECK.append([what, value, where])

A = J['anchors']
W('# Round 5c, worker x2: ship tendencies B2, B3 and the cap results quoted in C4 / C5')
W('')
W(f"Batch `output/20261117-230933`, {A['smokes']:,} smokes, {A['dd']:,} destroyer smokes ({A['dd_top']} Top 6, {A['dd_rest']} Rest). "
  f"Destroyer smokes: {A['dd_rates']['died']} ships died ({A['dd_rates']['died_per100']:.1f} per 100) against {A['dd_rates']['caught']} caught ({A['dd_rates']['caught_per100']:.2f} per 100).")
W('')
W('How to read this page:')
W('- "died" = a covered ship (the smoker, or a ship inside or behind the smoke) died between activation and 20 s after the smoke dispersed; each dead ship is counted once. '
  f"\"caught\" = the batch list of ships that died while the smoke concealed them (round 5's \"deaths\"). The {A['died_not_ok']} smokes of the single-replay game laid by the team with no replay are left out of every \"died\" rate.")
W('- Cap results come from the cap timeline, on one fixed cap, up to 60 s after the smoke dispersed. "Contested cap" is the cap the batch ties the smoke to; "nearest cap" is the cap closest to the smoke centre. "We took" is counted over smokes where the cap was not already ours; "enemy took" over smokes where it was not already theirs.')
W('- Intervals are 95%, from resampling whole clans. "Clear" = the interval excludes zero. Under 8 smokes = "too few", no rate; 8 to 14 = "small n". Everything here is association, not cause.')
W('- "Round 5b" in the change tables = the round 5 number after the clock fix (round 5b did not redo these items).')
W('')

# ===================================================================== item 5: B2
b = J['B2']; R = {r['label']: r for r in b['rows']}; U = {r['label']: r for r in b['undet']}
CON = {r['label']: r for r in b['contrasts']}; UC = {r['label']: r for r in b['undet_contrasts']}; TV = {r['label']: r for r in b['tvr']}
IT, BB, ORD, ALL, OTH = 'Italian cruisers together', 'All battleships', 'Baseline: cruiser smokers with ordinary smoke', 'Baseline: all smokes', 'Baseline: all other smokes (not exhaust, not battleship)'
W('### 5. B2. Getaway smokes (exhaust and battleship smoke), both death metrics, and the undetected share from the track')
W('')
W(f"**Answer:** The round 5 reading stands on both metrics: the Italian cruisers' exhaust smoke goes with more losses, not fewer. The smoker died in {R[IT]['died_smoker']['v']} of every 100 smokes "
  f"(caught: {R[IT]['caught_smoker']['v']}) against {R[ORD]['died_smoker']['v']} (caught: {R[ORD]['caught_smoker']['v']}) for cruisers with ordinary smoke. "
  f"From the track, the smoker was undetected for {U[IT]['track_life_mean']['v']}% of the smoke's life (Italian cruisers), {U[BB]['track_life_mean']['v']}% (battleships) and {U[ORD]['track_life_mean']['v']}% (ordinary cruiser smoke). "
  f"Battleships look worse on \"died\" ({R[BB]['died_smoker']['v']} per 100) than on \"caught\" ({R[BB]['caught_smoker']['v']}), but no battleship gap is clear.")
W('')
W('**Numbers (deaths):** per 100 smokes.')
W('')
rows = []
for lab in [r['label'] for r in b['rows']]:
    r = R[lab]
    if lab == 'C. Colombo (battleship)': rows.append(['**Battleships, listed separately**'] + [''] * 6)
    if lab == ALL: rows.append(['**Baselines**'] + [''] * 6)
    rows.append([('**' + lab + '**') if lab in (IT, BB) else lab, tagn(r['n']), r['clans'], fv(r['died']), fv(r['caught']), fv(r['died_smoker']), fv(r['caught_smoker'])])
table(['Group', 'n', 'Clans', 'Ships died per 100', 'Ships caught per 100', 'Smoker died per 100', 'Smoker caught per 100'], rows)
W('Differences with intervals:')
W('')
table(['Contrast', 'Ships died per 100', 'Ships caught per 100', 'Smoker died per 100', 'Smoker caught per 100'],
      [[r['label'], fd(r['died']), fd(r['caught']), fd(r['died_smoker']), fd(r['caught_smoker'])] for r in b['contrasts']])
wd = b['who_died']
W(f"- Who died: in Italian cruiser smokes {wd['Italian cruisers']['died'].get('smoker', 0)} of the {sum(wd['Italian cruisers']['died'].values())} ships that died were the smoker "
  f"(caught: {wd['Italian cruisers']['caught'].get('smoker', 0)} of {sum(wd['Italian cruisers']['caught'].values())}). In battleship smokes all {sum(wd['All battleships']['died'].values())} were the smoker (caught: {sum(wd['All battleships']['caught'].values())}).")
W(f"- \"Died\" finds {R[IT]['died_ships']} ships against {R[IT]['caught_ships']} caught for the Italian cruisers, and {R[BB]['died_ships']} against {R[BB]['caught_ships']} for battleships: "
  "the extra ones died inside the window (activation to 20 s after dispersal) without the batch listing them as caught in the smoke.")
W(f"- Italian cruisers against all other smokes: the gap is clear on \"caught\" ({fd(CON['Italian cruisers minus all other smokes']['caught'])}) but not on \"died\" for all ships ({fd(CON['Italian cruisers minus all other smokes']['died'])}); "
  f"for the smoker alone it is {fd(CON['Italian cruisers minus all other smokes']['died_smoker'])} (the interval starts at zero: borderline).")
W('')
W("**Numbers (undetected share, from the smoker's track):** the track has a \"detected by the enemy\" flag every 2 s. For each smoke: the share of the smoker's samples between activation and dispersal (or its death, if earlier) with the flag off. "
  "\"Inside\" = only the samples where the smoker's track position is inside the smoke. Means per group (interval), medians beside them.")
W('')
rows = []
for lab in [r['label'] for r in b['undet']]:
    u = U[lab]
    if lab == 'C. Colombo (battleship)': rows.append(['**Battleships, listed separately**'] + [''] * 8)
    if lab == ALL: rows.append(['**Baselines**'] + [''] * 8)
    rows.append([('**' + lab + '**') if lab in (IT, BB) else lab, tagn(u['n_track']), fv(u['track_life_mean']), num(u['track_life_median']), fv(u['track_in_mean']), num(u['track_in_median']),
                 fv(u['batch_covered_mean']), fv(u['r5_life_mean']), num(u['in_share_mean'])])
table(['Group', 'Smokes with track data', "Undetected, % of the smoke's life (track), mean", 'median', 'Undetected while inside the smoke (track), mean', 'median',
       'Round 5 column 7: batch field, % of covered time, mean', 'Round 5 column 8: "whole life" figure, mean', "Share of the smoke's life the smoker is inside it, %"], rows)
table(['Contrast', "Undetected % of the smoke's life (track)", 'Undetected % while inside (track)', 'Batch field (round 5 column 7)', 'Round 5 "whole life" figure (column 8)'],
      [[r['label'], fd(r['track_life_mean']), fd(r['track_in_mean']), fd(r['batch_covered_mean']), fd(r['r5_life_mean'])] for r in b['undet_contrasts']])
W(f"- How the track figure compares with round 5: round 5 gave {U[IT]['batch_covered_mean']['v']}% / {U[BB]['batch_covered_mean']['v']}% / {U[ORD]['batch_covered_mean']['v']}% (Italian cruisers / battleships / ordinary cruiser smoke) on the batch field, "
  f"and {U[IT]['r5_life_mean']['v']} / {U[BB]['r5_life_mean']['v']} / {U[ORD]['r5_life_mean']['v']} on its own \"whole life\" figure. The track gives {U[IT]['track_life_mean']['v']} / {U[BB]['track_life_mean']['v']} / {U[ORD]['track_life_mean']['v']} for the whole life "
  f"and {U[IT]['track_in_mean']['v']} / {U[BB]['track_in_mean']['v']} / {U[ORD]['track_in_mean']['v']} while inside.")
W("- The track's whole-life figure sits close to the batch field and well above round 5's \"whole life\" figure. Round 5's figure counted only seconds that were both undetected and covered, so every second outside the smoke counted as detected. "
  "The track shows the smoker is mostly undetected outside the smoke as well.")
W(f"- The order of the groups is the same on every reading: ordinary cruiser smoke highest, Italian cruisers a few points lower, battleships lowest. Italian cruisers minus ordinary cruiser smoke: {fd(UC['Italian cruisers minus cruisers with ordinary smoke']['track_life_mean'])} on the track "
  f"(batch field: {fd(UC['Italian cruisers minus cruisers with ordinary smoke']['batch_covered_mean'])}). Battleships minus ordinary cruiser smoke: {fd(UC['Battleships minus cruisers with ordinary smoke']['track_life_mean'])}. "
  f"Battleships minus Italian cruisers: {fd(UC['Battleships minus Italian cruisers']['track_life_mean'])}.")
W(f"- Half of all smokes have the smoker undetected for the whole life of the smoke or nearly so (median {U[ALL]['track_life_median']}%); the means are pulled down by a minority of smokes where the smoker stays detected. "
  f"Smoker undetected for over 95% of the smoke's life: Italian cruisers {U[IT]['fully_undetected_pct']}%, battleships {U[BB]['fully_undetected_pct']}%, ordinary cruiser smoke {U[ORD]['fully_undetected_pct']}%.")
W(f"- Samples with no flag were left out: {b['samples']['none']:,} of {b['samples']['total']:,} samples. That drops {b['dropped_total']} smokes entirely (no sample with a flag; {b['dropped_one_sided']} of them in the single-replay game){', all destroyer smokes' if U['Baseline: destroyer smokers']['dropped'] == b['dropped_total'] else ''}; "
  f"{b['some_none_total']} more smoke lost part of its samples. No Italian cruiser or battleship smoke is dropped. {b['no_inside_sample']} smokes have no sample inside the smoke and are left out of the \"inside\" columns only.")
W('')
t1, t2, t3, t4 = TV['Italian cruisers'], TV['All battleships'], TV['Italian cruisers, undetected'], TV['All battleships, undetected']
W(f"**Top 6 or Shared:** Shared, and mostly a Rest tool: {t1['n_rest']} of the {R[IT]['n']} Italian cruiser smokes are by Rest clans. Top 6 (n={t1['n_top']}, {t1['clans_top']} clans) against Rest, smoker died per 100: {tr(t1['died_smoker'])}; smoker caught: {tr(t1['caught_smoker'])}. "
  f"The gap that round 5 called clear is clear only on \"caught\", and it rests on 5 deaths. Battleships Top 6 n={t2['n_top']} (small n, 8 are H-SR's Conte Verde): smoker died {tr(t2['died_smoker'])}; caught {tr(t2['caught_smoker'])}. "
  f"Undetected share of the smoke's life: Italian cruisers {tr(t3['track_life_mean'])}; battleships {tr(t4['track_life_mean'])}.")
W('')
W('**Clans:**')
for k in ('Napoli', 'Venezia', 'C. Colombo (battleship)', 'Conte Verde (battleship)', 'All battleships'): W(f"- {k}: {b['clans'][k]}")
W('')
W("**Could not be done / proxy:** \"Inside the smoke\" uses the smoke's full footprint for its whole life (the laid path and radius), so early samples can count as inside before that part of the smoke existed. Samples are 2 s apart. "
  "The detected flag says the enemy could see the ship, not which enemy or how.")
W('')
W('**Verdict:** Keep.')
W('')
W('**Changed from round 5b:**')
W('')
G5 = {IT: 'Italian cruisers (Napoli + Venezia)', BB: 'All battleships', 'Napoli': 'Napoli', 'Venezia': 'Venezia', 'C. Colombo (battleship)': 'C. Colombo (battleship)', 'Conte Verde (battleship)': 'Conte Verde (battleship)',
      ALL: 'BASELINE all smokes', OTH: 'BASELINE all other smokes (not getaway)', ORD: 'BASELINE cruiser smokers, ordinary smoke (Svea, Jinan...)', 'Baseline: all cruiser smokers': 'BASELINE cruiser smokers, all', 'Baseline: destroyer smokers': 'BASELINE destroyer smokers'}
rows = []
for lab, g5 in G5.items():
    r = R[lab]
    rows.append([f'{lab}: ships lost per 100 smokes', r5b_txt('B2', g5, 'all', 'deaths_per_100'), f"caught {fv(r['caught'])}; died {fv(r['died'])}", 'caught unchanged; died is the new death metric'])
    rows.append([f'{lab}: smoker lost per 100 smokes', r5b_txt('B2', g5, 'all', 'smoker_deaths_per_100'), f"caught {fv(r['caught_smoker'])}; died {fv(r['died_smoker'])}", 'caught unchanged; died is the new death metric'])
for r in b['contrasts']:
    rows.append([f"{r['label']}: ships lost per 100", r5b_con('B2', r['label'], 'deaths_per_100'), f"caught {fd(r['caught'])}; died {fd(r['died'])}", 'new death metric (caught interval differs only by resampling)'])
    rows.append([f"{r['label']}: smoker lost per 100", r5b_con('B2', r['label'], 'smoker_deaths_per_100'), f"caught {fd(r['caught_smoker'])}; died {fd(r['died_smoker'])}", 'new death metric (caught interval differs only by resampling)'])
for lab, g5 in ((IT, G5[IT]), (BB, G5[BB]), (ORD, G5[ORD]), (ALL, G5[ALL])):
    rows.append([f'{lab}: smoker undetected, % of time under the smoke', r5b_txt('B2', g5, 'all', 'undetected_pct_of_covered_time'),
                 f"batch field {fv(U[lab]['batch_covered_mean'])}; track, while inside {fv(U[lab]['track_in_mean'])}", 'batch field unchanged; track figure is new'])
    rows.append([f"{lab}: smoker undetected, % of the smoke's whole life", r5b_txt('B2', g5, 'all', 'undetected_pct_of_smoke_life'),
                 f"track {fv(U[lab]['track_life_mean'])}", 'track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected)'])
for r in b['undet_contrasts']:
    rows.append([f"{r['label']}: undetected %", r5b_con('B2', r['label'], 'undetected_pct_of_covered_time') + ' (batch field)', f"track, whole life {fd(r['track_life_mean'])}; track, inside {fd(r['track_in_mean'])}", 'track detected flag'])
rows.append(['Italian cruisers, Top 6 minus Rest, smoker lost per 100', '33.3 vs 14.4; +19.0 (+1.6 to +52.5), clear', f"caught {tr(t1['caught_smoker'])}; died {tr(t1['died_smoker'])}", 'new death metric'])
rows.append(['Battleships, Top 6 minus Rest, ships lost per 100', '10.0 vs 8.3, no clear gap', f"caught {tr(t2['caught'])}; died {tr(t2['died'])}", 'new death metric'])
rows.append(['Who died in Italian cruiser smokes', '27 of 30 the smoker', f"caught {wd['Italian cruisers']['caught'].get('smoker', 0)} of {sum(wd['Italian cruisers']['caught'].values())}; died {wd['Italian cruisers']['died'].get('smoker', 0)} of {sum(wd['Italian cruisers']['died'].values())}", 'new death metric'])
changed(rows)
chk('B2 Italian cruisers smoker died / caught per 100', f"{R[IT]['died_smoker']['v']} / {R[IT]['caught_smoker']['v']}", "compute_x2.py `b2['rows']` -> ships-maps.json B2.rows[label='Italian cruisers together'].died_smoker / caught_smoker")
chk('B2 battleships ships died / caught per 100', f"{R[BB]['died']['v']} / {R[BB]['caught']['v']}", "compute_x2.py `b2['rows']` -> B2.rows[label='All battleships']")
chk('B2 Italian cruisers minus ordinary cruiser smoke, smoker died', fd(CON['Italian cruisers minus cruisers with ordinary smoke']['died_smoker']), "compute_x2.py `b2['contrasts']` (diff_ci) -> B2.contrasts")
chk("B2 undetected % of the smoke's life, track (Italian / battleships / ordinary cruiser)", f"{U[IT]['track_life_mean']['v']} / {U[BB]['track_life_mean']['v']} / {U[ORD]['track_life_mean']['v']}", "compute_x2.py `s['u_life']`, stat `USTATS['track_life_mean']` -> B2.undet[*].track_life_mean")
chk('B2 undetected % while inside, track', f"{U[IT]['track_in_mean']['v']} / {U[BB]['track_in_mean']['v']} / {U[ORD]['track_in_mean']['v']}", "compute_x2.py `s['u_in']` -> B2.undet[*].track_in_mean")
chk('B2 round 5 columns reproduced (81.7 / 71.7 / 90.1 and 69.9 / 61.8 / 65.8)', f"{U[IT]['batch_covered_mean']['v']} / {U[BB]['batch_covered_mean']['v']} / {U[ORD]['batch_covered_mean']['v']} and {U[IT]['r5_life_mean']['v']} / {U[BB]['r5_life_mean']['v']} / {U[ORD]['r5_life_mean']['v']}", "compute_x2.py `undetected_pct`, `s['r5_undet_life']` -> B2.undet[*].batch_covered_mean / r5_life_mean")
chk('B2 smokes dropped for no detected flag', b['dropped_total'], "compute_x2.py `b2['dropped_total']`")
W('---')
W('')

# ===================================================================== item 6: B3
b = J['B3']; R = {r['label']: r for r in b['rows']}; TV = {r['label']: r for r in b['tvr']}
CS, DDL = 'For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze)', 'For comparison: all destroyer smokes'
lm = b['long_minus_sitters']; t4 = TV['All four']
WS = {(r['ship'], r['result']): r for r in b['win_split']}
won, lost = WS[('All four', 'games won')], WS[('All four', 'games lost')]
W('### 6. B3. Long smokes (Somers, Gearing, Harugumo, Delny): death rates and the Top 6 vs Rest gap, both metrics')
W('')
W(f"**Answer:** The Top 6 lose fewer ships in their long smokes on both metrics: died {tr(t4['died'])}; caught {tr(t4['caught'])}. "
  f"Split by result, there is no gap in games won on either metric (died {tr(won['died'])}). In games lost the \"died\" gap is not clear ({tr(lost['died'])}), but the \"caught\" gap stays clear ({tr(lost['caught'])}). "
  "So round 3's \"the gap goes away once wins and losses are separated\" holds on \"died\" and only in part on \"caught\".")
W('')
W('**Numbers:** per 100 smokes; sheltering cruisers per 100 sheltering cruisers (cruisers inside or behind the smoke, the smoker not counted).')
W('')
table(['Ship', 'n', 'Clans', 'Ships died per 100', 'Ships caught per 100', 'Smoker died per 100', 'Smoker caught per 100', 'Sheltering cruisers died, per 100 of them', 'Sheltering cruisers caught, per 100 of them'],
      [[('**' + r['label'] + '**') if r['label'] == 'All four' else r['label'] + (' (2 clans, 18 of 22 by H-SR)' if r['label'] == 'Delny' else ''), tagn(r['n']), r['clans'], fv(r['died']), fv(r['caught']), fv(r['died_smoker']), fv(r['caught_smoker']),
        f"{fv(r['died_cr'])} [{r['died_cr_n']} of {r['n_cr_cov']}]", f"{fv(r['caught_cr'])} [{r['caught_cr_n']} of {r['n_cr_in']}]"] for r in b['rows']])
W(f"Long-smoke ships minus cap sitters: ships died {fd(lm['died'])}; ships caught {fd(lm['caught'])}; smoker died {fd(lm['died_smoker'])}; smoker caught {fd(lm['caught_smoker'])}; "
  f"sheltering cruisers died {fd(lm['died_cr'])}; caught {fd(lm['caught_cr'])}.")
W('- The extra losses in long smokes are not the smoker and not a higher rate per sheltering cruiser: long smokes simply shelter far more cruisers '
  f"({R['All four']['n_cr_cov']} over {R['All four']['n_died_base']} smokes against {R[CS]['n_cr_cov']} over {R[CS]['n_died_base']} for cap sitters).")
W('')
W('Top 6 against Rest (Top 6 vs Rest; gap with interval):')
W('')
table(['Ship', 'n Top 6 / Rest', 'Ships died per 100', 'Ships caught per 100', 'Smoker died per 100', 'Smoker caught per 100', 'Sheltering cruisers died per 100', 'Sheltering cruisers caught per 100'],
      [[r['label'], f"{tagn(r['n_top'])} / {tagn(r['n_rest'])}", tr(r['died']), tr(r['caught']), tr(r['died_smoker']), tr(r['caught_smoker']), tr(r['died_cr']) if 'died_cr' in r else '-', tr(r['caught_cr']) if 'caught_cr' in r else '-'] for r in b['tvr']])
W('The same, with games won and games lost kept apart:')
W('')
rows = []
for ship in ('Somers', 'Gearing', 'Harugumo', 'Delny', 'All four', DDL):
    sh = WS[(ship, 'share of smokes laid in games won')]
    for res in ('games won', 'games lost'):
        r = WS[(ship, res)]
        rows.append([ship, res, f"{tagn(r['n_top'])} / {tagn(r['n_rest'])}", tr(r['died']), tr(r['caught']), tr(r['died_smoker']), tr(r['caught_smoker']),
                     f"{num(sh['top'], 0)}% vs {num(sh['rest'], 0)}%" if res == 'games won' else ''])
table(['Ship', 'Result', 'n Top 6 / Rest', 'Ships died per 100', 'Ships caught per 100', 'Smoker died per 100', 'Smoker caught per 100', 'Share of the smokes laid in games won, Top 6 vs Rest'], rows)
wl = {r['label'].split(':')[0]: r for r in b['won_minus_lost']}
W(f"- Winning or losing moves the death rate far more than the group does. Four ships together, games won minus games lost: Top 6 died {fd(wl['Top 6']['died'])}, caught {fd(wl['Top 6']['caught'])}; "
  f"Rest died {fd(wl['Rest']['died'])}, caught {fd(wl['Rest']['caught'])}.")
W(f"- The Top 6 lay {num(WS[('All four', 'share of smokes laid in games won')]['top'], 0)}% of their long smokes in games they won, the Rest {num(WS[('All four', 'share of smokes laid in games won')]['rest'], 0)}%. That mix makes most of the overall gap.")
hl = WS[('Harugumo', 'games lost')]; hw = WS[('Harugumo', 'games won')]
W(f"- What is left after the split sits in games lost and mostly in the Harugumo: died {tr(hl['died'])}; caught {tr(hl['caught'])} (Top 6 n {hl['n_top']}, Rest n {hl['n_rest']}). "
  f"In games won the Rest Harugumo lost nothing in {hw['n_rest']} smokes (small n).")
W(f"- In games lost the Rest smoker is caught far more often than the Top 6 smoker (four ships: {tr(lost['caught_smoker'])}), while \"died\" is closer ({tr(lost['died_smoker'])}): "
  "most Top 6 smokers that died in lost games are not on the batch's list of ships caught in the smoke.")
W('')
W(f"**Top 6 or Shared:** Top 6 gap on the four together, clear on both metrics (died {fd(t4['died'])}; caught {fd(t4['caught'])}), led by the Harugumo (died {tr(TV['Harugumo']['died'])}; caught {tr(TV['Harugumo']['caught'])}) "
  f"and the Gearing (died {tr(TV['Gearing']['died'])}). Somers shows no gap (died {tr(TV['Somers']['died'])}). The gap is mostly a won-or-lost effect: none in games won; in games lost clear on \"caught\" only.")
W('')
W('**Clans:**')
for k, v in b['clans'].items(): W(f'- {k}: {v}')
W('')
W(f"**Could not be done / proxy:** Delny has {TV['Delny']['n_rest']} Rest smokes and {WS[('Delny', 'games lost')]['n_top'] + WS[('Delny', 'games lost')]['n_rest']} smokes in a lost game, so it has no Top 6 vs Rest comparison and no win/loss split. "
  f"Within games lost the Top 6 have {lost['n_top']} long smokes (Gearing {WS[('Gearing', 'games lost')]['n_top']}, Harugumo {WS[('Harugumo', 'games lost')]['n_top']}), and the Rest Harugumo has {hw['n_rest']} in games won: the per-ship splits are thin and their intervals are wide.")
W('')
W('**Verdict:** Keep (death rates). The Top 6 vs Rest death gap: Keep as "mostly explained by winning", not as a long-smoke skill.')
W('')
W('**Changed from round 5b:**')
W('')
G5 = {'Somers': 'Somers', 'Gearing': 'Gearing', 'Harugumo': 'Harugumo', 'Delny': 'Delny', 'All four': 'All four long-smoke ships', CS: 'REFERENCE cap sitters (Daring, Z-42, Gdańsk, Grozovoi, Shimakaze)', DDL: 'REFERENCE all destroyer smokes'}
rows = []
for lab, g5 in G5.items():
    rows.append([f'{lab}: ships lost per 100 smokes', r5b_txt('B3', g5, 'all', 'deaths_per_100'), f"caught {fv(R[lab]['caught'])}; died {fv(R[lab]['died'])}", 'caught unchanged; died is the new death metric'])
rows.append(['Long-smoke ships minus cap sitters, ships lost per 100', r5b_con('B3', 'Long-smoke ships minus cap sitters', 'deaths_per_100'), f"caught {fd(lm['caught'])}; died {fd(lm['died'])}", 'new death metric'])
for lab, g5 in G5.items():
    t = TV[lab]; a, _ = r5b_row('B3', g5, 'top6', 'deaths_per_100'); c, _ = r5b_row('B3', g5, 'rest', 'deaths_per_100'); d, dc = r5b_row('B3', g5, 'top6 minus rest', 'deaths_per_100')
    old = f"{num(a) if a is not None else 'too few'} vs {num(c) if c is not None else 'too few'}" + (f"; {num(d, 1, True)} ({num(dc[0], 1, True)} to {num(dc[1], 1, True)})" if d is not None and dc else '')
    rows.append([f'{lab}: Top 6 vs Rest, ships lost per 100', old, f"caught {tr(t['caught'])}; died {tr(t['died'])}", 'new death metric'])
rows.append(['Top 6 vs Rest gap once games won and lost are separated (four ships)', 'round 5 text: "round 3 showed this gap goes away" (no number)',
             f"games won: died {tr(won['died'])}; caught {tr(won['caught'])}. Games lost: died {tr(lost['died'])}; caught {tr(lost['caught'])}", 'new: both metrics split by result'])
rows.append(['Smoker and sheltering-cruiser splits for the long ships', 'not given in round 5', f"four ships: smoker died {fv(R['All four']['died_smoker'])}, caught {fv(R['All four']['caught_smoker'])}; cruisers died {fv(R['All four']['died_cr'])}, caught {fv(R['All four']['caught_cr'])} per 100 sheltering cruisers", 'new'])
changed(rows)
chk('B3 four ships: ships died / caught per 100', f"{R['All four']['died']['v']} / {R['All four']['caught']['v']}", "compute_x2.py `b3['rows']` -> B3.rows[label='All four']")
chk('B3 four ships Top 6 minus Rest, died / caught', f"{fd(t4['died'])} / {fd(t4['caught'])}", "compute_x2.py `b3['tvr']` (boot_diff) -> B3.tvr[label='All four']")
chk('B3 Harugumo Top 6 vs Rest caught (round 5: 9.1 vs 35.6)', tr(TV['Harugumo']['caught']), "B3.tvr[label='Harugumo'].caught")
chk('B3 long minus cap sitters died / caught (round 5: +6.9)', f"{fd(lm['died'])} / {fd(lm['caught'])}", "compute_x2.py `b3['long_minus_sitters']` (diff_ci)")
chk('B3 games won, four ships, died / caught gap', f"{fd(won['died'])} / {fd(won['caught'])}", "compute_x2.py `b3['win_split']` -> B3.win_split[ship='All four', result='games won']")
chk('B3 games lost, four ships, died / caught gap', f"{fd(lost['died'])} / {fd(lost['caught'])}", "B3.win_split[ship='All four', result='games lost']")
W('---')
W('')

# ===================================================================== item 7
W('## 7. C4 and C5 rows that quote a cap result, redone on the cap timeline')
W('')
W('Round 5 took these cap results from cap-owner snapshots (recorded only at smoke moments) or from the batch `cap_won` field. Here every one comes from the cap timeline, on one fixed cap, up to 60 s after the smoke dispersed. '
  '"Enemy was taking it" = the timeline shows the enemy as the capturing side of that cap at some time while the smoke stood.')
W('')

# ---------- 7a
c = J['C7a']; BY = {r['id']: r for r in c}
NAME = {'sg-cell-1': 'Sleeping Giant G1', 'hs-cell-1': 'Hotspot G10+H10', 'sof-cell-1': 'Sea of Fortune F9+G9', 'c5-lp-f8': 'Loop F8', 'c5-lp-f10': 'Loop F10'}
g1, hs, sf, f8, f10 = (BY[k] for k in NAME)
W('### 7a. High-paying cells (C4: Sleeping Giant G1, Hotspot G10+H10, Sea of Fortune F9+G9; C5: Loop F8 and F10)')
W('')
W(f"**Answer:** The round 5 statement stands: these cells pay well in damage, and the cap is not taken more often after smokes there than elsewhere on the map. On the timeline \"we took the cap\" is {kn(g1['caps']['_n']['we_took'])} at G1 (round 5: 19% of 21), "
  f"{kn(hs['caps']['_n']['we_took'])} at Hotspot G10+H10 (34% of 35) and {kn(sf['caps']['_n']['we_took'])} at Sea of Fortune F9+G9 (25% of 8). "
  f"One new thing: at G1 the enemy took cap A during or just after {kn(g1['caps']['_n']['enemy_took'])} of the smokes, against {g1['caps_rest']['_n']['enemy_took']['pct']:.0f}% elsewhere on the map, a clear gap.")
W('')
W('**Numbers (destroyer smokes in the cell, team-normalized grid; concealed damage is unchanged from round 5):**')
W('')
table(['Cell', 'n (Top 6 / Rest)', 'Clans', 'Concealed damage per smoke (round 5b)', 'Rest of the map', 'Gap interval', 'Nearest cap (normalized letter)', 'Contested cap is the nearest cap'],
      [[NAME[r['id']], f"{tagn(r['n'])} ({r['top6']} / {r['rest']})", r['clans'], f"{r['conc']:,} ({r['conc_r5b']:,})", f"{r['conc_rest_of_map']:,}", f"{num(r['conc_gap_ci'][0], 0, True)} to {num(r['conc_gap_ci'][1], 0, True)}",
        ', '.join(f'{k} {v}' for k, v in r['near_caps'].items()), f"{r['caps']['same_cap']} of {r['n']}"] for r in c])
W('Cap results. In all five cells the contested cap and the nearest cap are the same cap for every smoke, so the two columns agree inside the cell; they differ for the rest of the map.')
W('')
rows = []
for r in c:
    for lab, cb, n in ((NAME[r['id']], r['caps'], r['n']), ('rest of ' + r['map'], r['caps_rest'], r['n_map'] - r['n'])):
        rows.append([lab, n, own(cb['_c']), kn(cb['_c']['we_took']), kn(cb['_c']['enemy_took']), own(cb['_n']), kn(cb['_n']['we_took']), kn(cb['_n']['enemy_took'])])
    v = r['vs_rest']
    rows.append(['cell minus rest of the map', '', '', fd(v['we_took_c']), fd(v['enemy_took_c']), '', fd(v['we_took_n']), fd(v['enemy_took_n'])])
table(['Smokes', 'n', 'Contested cap: ours / neutral / theirs at activation', 'We took it', 'Enemy took it', 'Nearest cap: ours / neutral / theirs', 'We took it', 'Enemy took it'], rows)
W('Deaths, per 100 smokes:')
W('')
rows = []
for r in c:
    d, dr, v = r['deaths'], r['deaths_rest'], r['vs_rest']
    rows.append([NAME[r['id']], tagn(r['n']), fv(d['died']), fv(d['caught']), fv(d['died_smoker']), fv(d['caught_smoker'])])
    rows.append(['rest of ' + r['map'], dr['n'], fv(dr['died']), fv(dr['caught']), fv(dr['died_smoker']), fv(dr['caught_smoker'])])
    rows.append(['cell minus rest of the map', '', fd(v['died']), fd(v['caught']), fd(v['died_smoker']), fd(v['caught_smoker'])])
table(['Smokes', 'n', 'Ships died per 100', 'Ships caught per 100', 'Smoker died per 100', 'Smoker caught per 100'], rows)
W(f"- G1 (Sleeping Giant): cap A was never ours when these smokes were laid ({g1['caps']['_n']['neutral']} neutral, {g1['caps']['_n']['theirs']} theirs); {g1['early']} of the {g1['n']} are early smokes. We took A after {kn(g1['caps']['_n']['we_took'])}; the enemy took it after {kn(g1['caps']['_n']['enemy_took'])}. "
  f"Enemy took, cell minus rest of the map: {fd(g1['vs_rest']['enemy_took_n'])}. The smoke pays in damage while the cap often goes to the other side.")
W(f"- Hotspot G10+H10: we took D after {kn(hs['caps']['_n']['we_took'])}, the enemy after {kn(hs['caps']['_n']['enemy_took'])}; neither differs clearly from the rest of the map.")
W(f"- Sea of Fortune F9+G9: {kn(sf['caps']['_n']['we_took'])} and {kn(sf['caps']['_n']['enemy_took'])}; no ship died or was caught in these {sf['n']} smokes, clearly below the rest of the map (died {fd(sf['vs_rest']['died'])}).")
W(f"- Damage: the three C4 cells stay clearly above the rest of their map. The two Loop cells are well above the rest of Loop on average ({f8['conc']:,} and {f10['conc']:,} against about {f8['conc_rest_of_map']:,}), "
  f"but with whole clans resampled the gap interval crosses zero for both ({num(f8['conc_gap_ci'][0], 0, True)} to {num(f8['conc_gap_ci'][1], 0, True)}; {num(f10['conc_gap_ci'][0], 0, True)} to {num(f10['conc_gap_ci'][1], 0, True)}): they rest on a few big smokes, as round 5 said.")
W(f"- Loop F8 and F10: round 5 quoted no cap result for these two cells. Timeline: F8 we took {kn(f8['caps']['_n']['we_took'])}, enemy took {kn(f8['caps']['_n']['enemy_took'])}; F10 we took {kn(f10['caps']['_n']['we_took'])}, enemy took {kn(f10['caps']['_n']['enemy_took'])}. "
  f"F10 stays the costly one: died {fv(f10['deaths']['died'])}, caught {fv(f10['deaths']['caught'])} per 100 (small n).")
W('')
def tcell(r, key):
    t = r['tvr'][key]; ci = t['ci']
    return f"Top 6 {kn(t['top'])} vs Rest {kn(t['rest'])}" + (f" (gap interval {num(ci[0], 0, True)} to {num(ci[1], 0, True)})" if ci else '')
W(f"**Top 6 or Shared:** Shared, as in round 5 (the cells were found on all clans pooled). We took the nearest cap: G1 {tcell(g1, 'we_took_n')}; Hotspot {tcell(hs, 'we_took_n')}; the other cells have too few on each side. "
  f"Deaths at G1: died {tr(g1['tvr_deaths']['died'])}; Hotspot: died {tr(hs['tvr_deaths']['died'])}. No clear gap.")
W('')
W('**Clans:**')
for r in c: W(f"- {NAME[r['id']]} ({r['clans']} clans, {r['games']} games): {r['clan_text']}")
W('')
W('**Could not be done / proxy:** Nothing missing. The cells were picked and scored on the same data (round 5 caution), so the damage gaps will shrink on new data; that caution is unchanged.')
W('')
W('**Verdict:** Keep (shared high-paying cells; the cap is not taken more often there). Lead: G1 smokes go with the enemy taking A.')
W('')
W('**Changed from round 5b:**')
W('')
rows = []
for r in c:
    rows.append([f"{NAME[r['id']]}: n and concealed damage per smoke", f"{r['n_r5b']}; {r['conc_r5b']:,}", f"{r['n']}; {r['conc']:,}", 'unchanged'])
    old = f"{r['r5b_cap_taken_pct']}% of {r['r5b_cap_taken_n']}" if r['r5b_cap_taken_pct'] is not None else 'no cap result quoted'
    rows.append([f"{NAME[r['id']]}: we took the cap (cap not already ours)", old, f"nearest cap {kn(r['caps']['_n']['we_took'])}; contested cap {kn(r['caps']['_c']['we_took'])}", 'cap timeline'])
    rows.append([f"{NAME[r['id']]}: enemy took the cap", 'not given', f"nearest cap {kn(r['caps']['_n']['enemy_took'])}; contested cap {kn(r['caps']['_c']['enemy_took'])}", 'cap timeline (new)'])
    rows.append([f"{NAME[r['id']]}: ships lost per 100 smokes", num(r['r5b_deaths_per_100']), f"caught {fv(r['deaths']['caught'])}; died {fv(r['deaths']['died'])}", 'caught unchanged; died is the new death metric'])
changed(rows)
chk('7a G1 we took / enemy took cap A', f"{kn(g1['caps']['_n']['we_took'])} / {kn(g1['caps']['_n']['enemy_took'])}", "compute_x2.py `cap_block(mem)` -> C7a[id='sg-cell-1'].caps._n")
chk('7a G1 enemy took, cell minus rest of map', fd(g1['vs_rest']['enemy_took_n']), "compute_x2.py `r['vs_rest']` (diff_ci, share_stat) -> C7a[0].vs_rest.enemy_took_n")
chk('7a Hotspot G10+H10 we took', kn(hs['caps']['_n']['we_took']), "C7a[id='hs-cell-1'].caps._n.we_took")
chk('7a Sea of Fortune F9+G9 we took', kn(sf['caps']['_n']['we_took']), "C7a[id='sof-cell-1'].caps._n.we_took")
chk('7a cell membership and damage reproduce round 5b', '; '.join(f"{NAME[r['id']]} {r['n']} / {r['conc']:,}" for r in c), 'compute_x2.py `CELLS` loop against round5b/spots.json')

# ---------- 7b
c = J['C7b']; RW = {r['label']: r for r in c['rows']}; Bq = RW['Cap B']; O = RW['Other caps together (A, C, D)']; v = c['b_vs_other']; BB_ = c['B']
W('### 7b. Sleeping Giant cap B (C5-SG-3): is the smoke there to stop the enemy taking B')
W('')
W(f"**Answer:** The round 5 statement stands. The enemy took B during or just after {kn(Bq['caps']['_n']['enemy_took'])} of these smokes, the same count as round 5, and that is not clearly different from the other caps ({kn(O['caps']['_n']['enemy_took'])}). "
  f"The timeline adds that the enemy was actually taking B while the smoke stood in only {kn(Bq['enemy_in_cap'])}, and in {Bq['enemy_in_cap_when_ours']['k']} of the {Bq['caps']['_n']['ours']} laid when B was ours. This is cap-holding and cap-contesting smoke, not a reaction to an attack on B.")
W('')
W(f"**Numbers (all smokes inside or within 2 km of a cap edge; {c['n_near']} of the map's {c['n_map']} smokes; cap = nearest cap, team-normalized letter):**")
W('')
table(['Cap', 'Smokes', 'Top 6', 'Ours / neutral / theirs at activation', 'Enemy took it (of not theirs)', 'Enemy took it when ours', 'We took it (of not ours)', 'Enemy was taking it while the smoke stood', 'Same, when ours', 'Concealed dmg', 'Ships died per 100', 'Ships caught per 100'],
      [[r['label'], tagn(r['n']), r['top6'], own(r['caps']['_n']), kn(r['caps']['_n']['enemy_took']), kn(r['caps']['_n']['enemy_took_when_ours']), kn(r['caps']['_n']['we_took']), kn(r['enemy_in_cap']), kn(r['enemy_in_cap_when_ours']),
        f"{r['conc']:,}", fv(r['deaths']['died']), fv(r['deaths']['caught'])] for r in c['rows']])
W('The same on the contested cap (the cap the batch ties the smoke to):')
W('')
table(['Smokes near', 'Contested cap is the nearest cap', 'Ours / neutral / theirs', 'Enemy took it', 'We took it'],
      [[r['label'], f"{r['caps']['same_cap']} of {r['n']}", own(r['caps']['_c']), kn(r['caps']['_c']['enemy_took']), kn(r['caps']['_c']['we_took'])] for r in c['rows']])
W(f"- B minus the other caps: enemy took, nearest cap {fd(v['enemy_took_n'])}; contested cap {fd(v['enemy_took_c'])}; we took, nearest cap {fd(v['we_took_n'])}; enemy was taking it {fd(v['enemy_in_cap'])}; "
  f"ships died per 100 {fd(v['died'])}; caught {fd(v['caught'])}. None clear.")
W(f"- B ours at activation: {c['ours_share']['B']['v']}% ({c['ours_share']['B']['ci'][0]} to {c['ours_share']['B']['ci'][1]}); other caps {c['ours_share']['other']['v']}% ({c['ours_share']['other']['ci'][0]} to {c['ours_share']['other']['ci'][1]}); difference {fd(v['ours_share'])}. "
  f"The timeline owner at activation agrees with the round 5 snapshot for {BB_['own_agree']} of the 34 smokes.")
W(f"- At B: {BB_['cls'].get('destroyer', 0)} destroyer smokes, {BB_['cls'].get('cruiser', 0)} cruiser. Ships: " + ', '.join(f'{k} {n}' for k, n in list(BB_['ships'].items())[:5]) + f". Cap sitters {BB_['habits'].get('cap sitters', 0)}, long-smoke ships {BB_['habits'].get('flank smoke lines', 0)}. {BB_['inside']} are inside the cap.")
W(f"- The one smoke after which the enemy took B: " + '; '.join(f"{x['team']} {x['ship']} (B {x['own']} at activation)" for x in BB_['enemy_took_list']) + '.')
W(f"- We took B after {kn(Bq['caps']['_n']['we_took'])} (round 5: 5 of 18): the timeline finds {Bq['caps']['_n']['we_took']['k'] - 5} more captures than the snapshots did. At cap A it finds more on both sides: enemy took {kn(RW['Cap A']['caps']['_n']['enemy_took'])} (round 5: 3 of 40), we took {kn(RW['Cap A']['caps']['_n']['we_took'])} (7 of 18).")
W(f"- D is a special case: {RW['Cap D']['caps']['same_cap']} of the {RW['Cap D']['n']} smokes near D have D as the batch's contested cap; the rest are tied to another cap.")
W('')
st, so = c['share_of_map']['share'], c['ours_tvr']['share']; bt, br = BB_['top'], BB_['rest']
W(f"**Top 6 or Shared:** Shared spot. Share of all map smokes: Top 6 {bt['n']} of {c['share_of_map']['n_top']} ({st['top']:.0f}%) vs Rest {br['n']} of {c['share_of_map']['n_rest']} ({st['rest']:.0f}%), {fd(st)}. "
  f"B ours at activation: Top 6 {BB_['ours_by_grp']['top']} of {bt['n']} vs Rest {BB_['ours_by_grp']['rest']} of {br['n']}, {fd(so)}. "
  f"Enemy took B: Top 6 {kn(bt['caps']['_n']['enemy_took'])}, Rest {kn(br['caps']['_n']['enemy_took'])}. We took B: Top 6 {kn(bt['caps']['_n']['we_took'])}, Rest {kn(br['caps']['_n']['we_took'])}. "
  f"Deaths at B: Top 6 died {fv(bt['deaths']['died'])}, caught {fv(bt['deaths']['caught'])} (small n); Rest died {fv(br['deaths']['died'])}, caught {fv(br['deaths']['caught'])}. Concealed damage Top 6 {bt['conc']:,} vs Rest {br['conc']:,} per smoke.")
W('')
W(f"**Clans:** {BB_['clan_text']}. With B ours: {BB_['clan_text_ours']}.")
W('')
W('**Could not be done / proxy:** The data still cannot tell "the smoke stopped the enemy" from "the enemy never came". The timeline\'s capturing-side field is the closest sign of a real attack on the cap, and it is low at B.')
W('')
W('**Verdict:** Drop the reading "there to stop the enemy taking B". Keep as: low-paying shared cap-sitter spot. Same as round 5.')
W('')
W('**Changed from round 5b:**')
W('')
R5SG = {'Cap A': ('28 / 12 / 6', '3 of 40 (8%)', '7 of 18 (39%)', '6.5'), 'Cap B': ('16 / 12 / 6', '1 of 28 (4%)', '5 of 18 (28%)', '11.8'), 'Cap C': ('8 / 2 / 7', '2 of 10 (20%, small n)', '4 of 9 (small n)', '29.4'), 'Cap D': ('18 / 0 / 4', '0 of 18 (0%)', '0 of 4 (too few)', '13.6')}
rows = []
for k, (o_, e_, w_, d_) in R5SG.items():
    r = RW[k]
    rows.append([f'{k}: ours / neutral / theirs at activation', o_, own(r['caps']['_n']), 'cap timeline' if own(r['caps']['_n']) != o_ else 'unchanged (timeline agrees with the snapshot)'])
    rows.append([f'{k}: enemy took it', e_, kn(r['caps']['_n']['enemy_took']), why_cap(e_, kn(r['caps']['_n']['enemy_took']))])
    rows.append([f'{k}: we took it', w_, kn(r['caps']['_n']['we_took']), why_cap(w_, kn(r['caps']['_n']['we_took']))])
    rows.append([f'{k}: ships lost per 100 smokes', d_, f"caught {fv(r['deaths']['caught'])}; died {fv(r['deaths']['died'])}", 'caught unchanged; died is the new death metric'])
rows.append(['Enemy took B vs the other caps', '1 of 28 (4%) vs 5 of 68 (7%); -4 pts (-13 to +9)', f"{kn(Bq['caps']['_n']['enemy_took'])} vs {kn(O['caps']['_n']['enemy_took'])}; {fd(v['enemy_took_n'])}", 'cap timeline'])
rows.append(['B ours at activation, B vs other caps', '47% (27 to 72) vs 64% (52 to 75)', f"{c['ours_share']['B']['v']}% vs {c['ours_share']['other']['v']}%", 'unchanged values, timeline owner'])
rows.append(['Sign of a real attack on B (of the 16 laid when B was ours)', 'enemy already contesting at the start 2; batch "cap defended" 2', f"enemy was taking B while the smoke stood {Bq['enemy_in_cap_when_ours']['k']} of {Bq['enemy_in_cap_when_ours']['n']}", 'cap timeline (capturing side) replaces the snapshot flags'])
changed(rows)
chk('7b smokes within 2 km of B', Bq['n'], "compute_x2.py `B` (near_cap_edge_m <= 2000 and near_ncap == 'B') -> C7b.rows[label='Cap B'].n")
chk('7b enemy took B / other caps', f"{kn(Bq['caps']['_n']['enemy_took'])} / {kn(O['caps']['_n']['enemy_took'])}; {fd(v['enemy_took_n'])}", "C7b.rows[*].caps._n.enemy_took; C7b.b_vs_other.enemy_took_n (diff_ci)")
chk('7b we took B', kn(Bq['caps']['_n']['we_took']), "C7b.rows[label='Cap B'].caps._n.we_took")
chk('7b enemy was taking B while the smoke stood (all / when ours)', f"{kn(Bq['enemy_in_cap'])} / {kn(Bq['enemy_in_cap_when_ours'])}", "compute_x2.py `s['inv_n_any']` (TL.invaded on s['near_cap']) -> C7b.rows[label='Cap B'].enemy_in_cap")

# ---------- 7c
c = J['C7c']; RW = {r['label']: r for r in c['rows']}
T0, T1, T2, T3 = (RW[k] for k in ('Radar smokes (round 5 tags), nearest cap B', 'Other smokes, nearest cap B (no radar tag)', 'Radar smokes (round 5 tags), within 2 km of B', 'Other smokes within 2 km of B (no radar tag)'))
OM = RW['Radar smokes (round 5 tags), other maps, nearest cap']; con = {r['label']: r for r in c['contrasts']}; ov = c['overlap']
W('### 7c. Mountain Range, radar from smoke at B (C5-MR-2): did the enemy take B during those smokes')
W('')
W(f"**Answer:** Yes, often, and the timeline makes it slightly worse than round 5 said: the enemy took B during or just after {kn(T0['caps']['_n']['enemy_took'])} of the radar smokes at B, and after {T0['caps']['_n']['enemy_took_when_ours']['k']} of the {T0['caps']['_n']['enemy_took_when_ours']['n']} laid when B was ours (round 5: 4 of 8). "
  f"That is no better than other smokes at B ({kn(T1['caps']['_n']['enemy_took'])}). The round 5 statement stands. Small n throughout.")
W('')
W(f"**Numbers:** radar smoke defined two ways: the round 5 tags (primary purpose cap control or radar trap, or the batch's radar-from-inside record) and the radar log (a ship of the smoking team pressed radar while standing in the smoke). "
  f"At B the two pick the same smokes: {ov['tag']} by tags, {ov['log']} by the log, {ov['both']} in both. So the two sets of rows below are identical at B. Round 5's headline rows used \"nearest cap is B, any distance\"; the 2 km rule keeps {T2['n']}.")
W('')
rows = []
for r in c['rows']:
    rows.append([r['label'], tagn(r['n']), r['top6'], own(r['caps']['_n']), kn(r['caps']['_n']['enemy_took']), kn(r['caps']['_n']['enemy_took_when_ours']), kn(r['caps']['_n']['we_took']), kn(r['enemy_in_cap']),
                 fv(r['deaths']['died']), fv(r['deaths']['caught'])])
table(['Smokes', 'n', 'Top 6', 'B ours / neutral / theirs at activation', 'Enemy took B', 'Enemy took B when ours', 'We took B (of not ours)', 'Enemy was taking B while the smoke stood', 'Ships died per 100', 'Ships caught per 100'], rows)
W('For the "other maps" rows read "the nearest cap" for "B". The same smokes on the contested cap:')
W('')
table(['Smokes', 'Contested cap is the nearest cap', 'Ours / neutral / theirs', 'Enemy took it', 'Enemy took it when ours', 'We took it'],
      [[r['label'], f"{r['caps']['same_cap']} of {r['n']}", own(r['caps']['_c']), kn(r['caps']['_c']['enemy_took']), kn(r['caps']['_c']['enemy_took_when_ours']), kn(r['caps']['_c']['we_took'])] for r in c['rows'] if 'pressed' not in r['label'] or 'other maps' in r['label']])
k0 = con['Radar (tags) minus other, nearest cap B']; k2 = con['Radar at B (tags) minus radar on other maps']
W(f"- Radar smokes minus other smokes at B: enemy took B {fd(k0['enemy_took_n'])}; B ours at activation {fd(k0['ours_share'])}; enemy was taking B while the smoke stood {fd(k0['enemy_in_cap'])}; ships died per 100 {fd(k0['died'])}; caught {fd(k0['caught'])}.")
W(f"- Radar smokes are laid on a held B more often ({T0['caps']['_n']['ours']} of {T0['n']} against {T1['caps']['_n']['ours']} of {T1['n']}), and the enemy was taking B during {kn(T0['enemy_in_cap'])} of them: part of this is defence in intent. It did not hold: B was lost after {T0['caps']['_n']['enemy_took_when_ours']['k']} of {T0['caps']['_n']['enemy_took_when_ours']['n']}.")
W(f"- Against radar smokes on other maps ({kn(OM['caps']['_n']['enemy_took'])} lost the nearest cap; when ours {kn(OM['caps']['_n']['enemy_took_when_ours'])}): difference {fd(k2['enemy_took_n'])}, not clear.")
lostl = [x for x in c['list'] if x['own'] == 'ours' and x['enemy_took']]
W(f"- The {len(lostl)} \"ours, then lost\" smokes come from {c['lost_games']} games: " + '; '.join(f"{x['team']} {x['ship']} {x['t'] // 60}:{x['t'] % 60:02d}" for x in lostl) + f" (elapsed time). The earliest is at {min(x['t'] for x in lostl) // 60} minutes.")
ch = [x for x in c['list'] if x['own'] != x['own_snapshot']]
W(f"- Owner at activation differs from the round 5 snapshot for {len(ch)} of the 15: " + '; '.join(f"{x['team']} {x['ship']} {x['t'] // 60}:{x['t'] % 60:02d}, snapshot \"{x['own_snapshot']}\", timeline \"{x['own']}\", {x['edge_m'] / 1000:.1f} km from the B edge" for x in ch) + '. That is why round 5 had 8 / 5 / 2 and the timeline has ' + own(T0['caps']['_n']) + '.')
wm = c['whole_map']
W('- Whole map, enemy took the nearest cap: ' + ', '.join(f"{L} {kn(r['caps']['_n']['enemy_took'])}" for L, r in wm.items()) + '. B is still the cap that changes hands most on this map.')
W(f"- Ships: " + ', '.join(f'{k} {n}' for k, n in c['ships']['tag'].items()) + f". Return {T0['conc']:,} concealed damage per smoke; {T0['deaths']['died']['v']} died and {T0['deaths']['caught']['v']} caught per 100 (one ship).")
W('')
stv = c['share_tvr']
W(f"**Top 6 or Shared:** Top 6 spot, as in round 5. Radar smokes at B are {T0['top6']} of {stv['n_top']} Top 6 smokes on the map ({stv['tag']['top']:.0f}%) vs {T0['rest']} of {stv['n_rest']} Rest ({stv['tag']['rest']:.0f}%), {fd(stv['tag'])}. "
  f"With {T0['rest']} Rest smokes there is no Top 6 vs Rest comparison of the cap result.")
W('')
W(f"**Clans:** {c['clan_text']['tag']}.")
W('')
W('**Could not be done / proxy:** n is 15 (9 on a held cap), from 6 clans; the 5 losses come from 3 games. No rate here should be read as more than a count.')
W('')
W('**Verdict:** Keep the spot; Drop "radar from smoke defends B". Same as round 5.')
W('')
W('**Changed from round 5b:**')
W('')
R5MR = [('Radar smokes, nearest cap B', T0, '8 / 5 / 2', '5 of 13 (38%, small n)', '4 of 8 (50%, small n)', '3 of 7 (too few)'),
        ('Other smokes, nearest cap B', T1, '15 / 17 / 21', '11 of 32 (34%)', '5 of 15 (33%)', '17 of 38 (45%)'),
        ('Radar smokes within 2 km of B', T2, '4 / 2 / 1', '2 of 6 (too few)', '1 of 4 (too few)', '1 of 3 (too few)'),
        ('Other smokes within 2 km of B', T3, '7 / 8 / 9', '4 of 15 (27%)', '2 of 7 (too few)', '11 of 17 (65%)'),
        ('Radar smokes, other maps (nearest cap)', OM, '52 / 35 / 25', '16 of 87 (18%)', '7 of 52 (13%)', '23 of 60 (38%)')]
rows = []
for lab, r, o_, e_, eo_, w_ in R5MR:
    rows.append([f'{lab}: ours / neutral / theirs', o_, own(r['caps']['_n']), 'cap timeline' if own(r['caps']['_n']) != o_ else 'unchanged'])
    rows.append([f'{lab}: enemy took', e_, kn(r['caps']['_n']['enemy_took']), why_cap(e_, kn(r['caps']['_n']['enemy_took']))])
    rows.append([f'{lab}: enemy took when ours', eo_, kn(r['caps']['_n']['enemy_took_when_ours']), why_cap(eo_, kn(r['caps']['_n']['enemy_took_when_ours']))])
    rows.append([f'{lab}: we took', w_, kn(r['caps']['_n']['we_took']), why_cap(w_, kn(r['caps']['_n']['we_took']))])
rows.append(['Whole map, enemy took the nearest cap', 'A 6 of 41 (15%), B 16 of 45 (36%), C 10 of 56 (18%)', ', '.join(f"{L} {kn(r['caps']['_n']['enemy_took'])}" for L, r in wm.items()), 'cap timeline'])
rows.append(['Radar smokes at B: ships lost', '1 death', f"caught {T0['deaths']['caught']['v']} per 100; died {T0['deaths']['died']['v']} per 100", 'unchanged (one ship on both metrics)'])
rows.append(['Radar definition', 'tags: 15 smokes', f"tags {ov['tag']}, radar log {ov['log']}, same smokes {ov['both']}", 'radar log added; same set'])
changed(rows)
chk('7c radar smokes at B: tags / log / both', f"{ov['tag']} / {ov['log']} / {ov['both']}", "compute_x2.py `c7c['overlap']`")
chk('7c enemy took B, radar smokes (all / when ours)', f"{kn(T0['caps']['_n']['enemy_took'])} / {kn(T0['caps']['_n']['enemy_took_when_ours'])}", "C7c.rows[0].caps._n.enemy_took / enemy_took_when_ours")
chk('7c enemy took B, other smokes at B', kn(T1['caps']['_n']['enemy_took']), 'C7c.rows[1].caps._n.enemy_took')
chk('7c radar minus other at B, enemy took', fd(k0['enemy_took_n']), "C7c.contrasts[0].enemy_took_n (diff_ci)")

# ---------- 7d
c = J['C7d']; A_, T_, R_ = c['rows']; tc = c['tvr_caps']; td = c['tvr_deaths']; io = c['in_vs_out']; out = c['outside']
W('### 7d. Loop, cap sitters at B (C5-LP-6 and spot `c5-lp-sitters-b`)')
W('')
W(f"**Answer:** The spot rebuilds exactly ({A_['n']} smokes: {T_['n']} Top 6, {R_['n']} Rest). On the timeline the cap result is much better than round 5 said: we took B during or just after {kn(A_['B']['we_took'])} of the smokes laid when B was not ours "
  f"(Top 6 {kn(T_['B']['we_took'])}, Rest {kn(R_['B']['we_took'])}; round 5: 5 of 10 and 1 of 8). The enemy took B after {kn(A_['B']['enemy_took'])}. Deaths are low on both metrics. The Top 6 lead in the spot stands.")
W('')
W(f"**Numbers:** membership as round 5: destroyer smokes by cap-sitter ships (Daring, Z-42, Gdansk, Grozovoi, Shimakaze) on Loop whose centre is inside the spot's ellipse; {c['n_sitters']} such smokes on the map ({c['n_sitters_top']} Top 6, {c['n_sitters_rest']} Rest). "
  "\"B\" = the cap at normalized letter B, followed for every smoke whatever its nearest cap.")
W('')
table(['Smokes', 'n', 'B ours / neutral / theirs at activation', 'We took B (of not ours)', 'Enemy took B (of not theirs)', 'Enemy took B when ours', 'Enemy was taking B while the smoke stood', 'Concealed dmg per smoke', 'Ships died per 100', 'Ships caught per 100', 'Smoker died per 100', 'Smoker caught per 100'],
      [[r['label'], tagn(r['n']), f"{r['B']['ours']} / {r['B']['neutral']} / {r['B']['theirs']}", kn(r['B']['we_took']), kn(r['B']['enemy_took']), kn(r['B']['enemy_took_when_ours']), kn(r['B']['enemy_in_cap']), f"{r['conc']:,}",
        fv(r['deaths']['died']), fv(r['deaths']['caught']), fv(r['deaths']['died_smoker']), fv(r['deaths']['caught_smoker'])] for r in c['rows']])
W('The library fields on the same smokes (nearest cap and contested cap; they are the same cap for all 28, and it is B for 26 and C for 2):')
W('')
table(['Smokes', 'Nearest cap: ours / neutral / theirs', 'We took it', 'Enemy took it', 'Contested cap: ours / neutral / theirs', 'We took it', 'Enemy took it'],
      [[r['label'], own(r['caps']['_n']), kn(r['caps']['_n']['we_took']), kn(r['caps']['_n']['enemy_took']), own(r['caps']['_c']), kn(r['caps']['_c']['we_took']), kn(r['caps']['_c']['enemy_took'])] for r in c['rows'] + [out]])
W(f"- Top 6 minus Rest in the spot: we took B {tr(tc['we_took_B'])} (nearest cap: {tr(tc['we_took_n'])}); n is {T_['B']['we_took']['n']} and {R_['B']['we_took']['n']}, small on both sides. "
  f"Concealed damage {tr(c['tvr_conc']['conc'], 0)}. B ours at activation {tr(c['tvr_ours']['share'])}.")
W(f"- Deaths, Top 6 vs Rest: died {tr(td['died'])}; caught {tr(td['caught'])}; smoker died {tr(td['died_smoker'])}. {A_['deaths']['died_ships']} ships died in the {A_['n']} smokes, {A_['deaths']['caught_ships']} was caught.")
W(f"- Against the other {out['n']} cap-sitter smokes on Loop: we took the nearest cap {kn(A_['caps']['_n']['we_took'])} in the spot vs {kn(out['caps']['_n']['we_took'])} outside, {fd(io['we_took_n'])}; "
  f"smoker died per 100 {fv(A_['deaths']['died_smoker'])} vs {fv(out['deaths']['died_smoker'])}, {fd(io['died_smoker'])}; ships died {fd(io['died'])}; caught {fd(io['caught'])}.")
W('- Ships in the spot: Top 6 ' + ', '.join(f'{k} {n}' for k, n in T_['ships'].items()) + '; Rest ' + ', '.join(f'{k} {n}' for k, n in R_['ships'].items()) + '.')
W('')
W(f"**Top 6 or Shared:** Top 6 spot (round 5: 15 of 23 Top 6 cap-sitter smokes against 13 of 65 Rest, +45 pts, +25 to +72; membership unchanged). The cap result now also leans Top 6 ({fd(tc['we_took_B'])}), on small n. "
  "Round 5's caution stays: most of the placement gap is ship choice (the Rest's cap sitter on Loop is the Daring, which sits at cap A).")
W('')
W(f"**Clans:** {c['clan_text']}.")
W('')
W('**Could not be done / proxy:** Nothing missing. The spot was chosen in round 4 because it showed a gap; treat the cap result as a lead on 17 smokes.')
W('')
W('**Verdict:** Keep.')
W('')
W('**Changed from round 5b:**')
W('')
changed([
    ['Members of the spot', '28 (15 Top 6, 13 Rest)', f"{A_['n']} ({T_['n']} Top 6, {R_['n']} Rest)", 'unchanged'],
    ['We took B during or just after, Top 6', '5 of 10', f"{kn(T_['B']['we_took'])} on B; {kn(T_['caps']['_n']['we_took'])} on the nearest cap", 'cap timeline'],
    ['We took B during or just after, Rest', '1 of 8 (small n)', f"{kn(R_['B']['we_took'])} on B; {kn(R_['caps']['_n']['we_took'])} on the nearest cap", 'cap timeline'],
    ['Enemy took B', 'not given', f"{kn(A_['B']['enemy_took'])}; when ours {kn(A_['B']['enemy_took_when_ours'])}", 'cap timeline (new)'],
    ['Concealed damage per smoke in the spot', f"{c['conc_r5b']:,} (Top 6 5.8k, Rest 1.2k)", f"{A_['conc']:,} (Top 6 {T_['conc']:,}, Rest {R_['conc']:,})", 'unchanged'],
    ['Ships lost per 100 smokes', num(c['deaths_r5b']), f"caught {fv(A_['deaths']['caught'])}; died {fv(A_['deaths']['died'])}", 'caught unchanged; died is the new death metric'],
])
chk('7d members of the spot', f"{A_['n']} ({T_['n']} / {R_['n']})", "compute_x2.py `mem` (in_ell on round5b/spots.json c5-lp-sitters-b shape) -> C7d.rows[0].n")
chk('7d we took B: all / Top 6 / Rest', f"{kn(A_['B']['we_took'])} / {kn(T_['B']['we_took'])} / {kn(R_['B']['we_took'])}", "compute_x2.py `fixed_cap(s, real_letter(s, 'B'))` -> C7d.rows[*].B.we_took")
chk('7d Top 6 minus Rest, we took B', fd(tc['we_took_B']), "C7d.tvr_caps.we_took_B (boot_diff)")
chk('7d enemy took B', kn(A_['B']['enemy_took']), 'C7d.rows[0].B.enemy_took')

W('---')
W('')
W('## Notes on method and the library')
W('')
W('- Scripts: `compute_x2.py` (all numbers, writes `ships-maps.json`; resampling seeded) and `write_x2.py` (this file and `CHECK-X2.md`).')
W('- `from r5clib import *` also brings in `HERE` from `round3/common.py` and overwrites a script\'s own `HERE`. A script that then writes to `os.path.join(HERE, ...)` writes into `round3/`. '
  'This happened once here: the first run wrote `ships-maps.json` into `round3/`; it was moved into this folder straight away and the script now uses its own variable. Not a library bug, but a trap worth a line in the library notes.')
W('- No library problem found. The timeline owner at activation agrees with the snapshot owner for all 34 Sleeping Giant smokes near B and for 14 of the 15 Mountain Range radar smokes.')
W('')
open(os.path.join(X2, 'FINDINGS-X2.md'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')

CK = ['# CHECK-X2: where each headline number comes from', '',
      'All numbers are computed in `compute_x2.py` and stored in `ships-maps.json`; `write_x2.py` only formats them. Anchors reproduced: '
      f"{A['smokes']:,} smokes; {A['dd']:,} destroyer smokes ({A['dd_top']} Top 6, {A['dd_rest']} Rest); {A['dd_early']} early destroyer smokes; destroyer smokes {A['dd_rates']['died']} died "
      f"({A['dd_rates']['died_per100']:.1f} per 100; smoker {A['dd_rates']['died_smoker_per100']:.2f}) against {A['dd_rates']['caught']} caught ({A['dd_rates']['caught_per100']:.2f} per 100; smoker {A['dd_rates']['caught_smoker_per100']:.1f}).", '',
      '| Headline number | Value | Script and variable |', '|---|---|---|']
CK += [f'| {a} | {b_} | {c_} |' for a, b_, c_ in CHECK]
open(os.path.join(X2, 'CHECK-X2.md'), 'w', encoding='utf-8').write('\n'.join(CK) + '\n')
print('written', len(OUT), 'lines;', len(CHECK), 'checks')
