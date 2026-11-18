# Round 5c check: where every number comes from

Batch `output/20261117-230933`. Scripts run as `python -I -X utf8 <script>` from their own folder. Shared definitions:
`r5clib.py` (two death metrics, replay-clock early, cap results from the cap timeline) on top of `../round5b/r5lib.py`
and `../round5b/tl.py`.

## Independent recheck by the main session

Every headline number was recomputed in separate scripts that do not use the workers' code (`verify/verify_x1.py`,
`verify/verify_x2_x3.py`), before the package was assembled.

| Item | Worker's number | Recheck |
|---|---|---|
| Base counts: destroyer smokes died / caught; early destroyer smokes | 194 / 124; 308 | same |
| 1. A1 cap-contest smokes; we took the contested cap, Rest: radar cruiser inside / no cruiser | 391; 77% (of 22) / 19% (of 85) | same |
| 1. A1 same, Top 6 | 60% (of 30) / 70% (of 23) | same |
| 1. A1 smokes with a radar cruiser inside; radar pressed from the smoke | 104; 8 | same |
| 2. A2 50+ behind: died / caught, with against without | 34.9 against 12.4; 23.1 against 7.5 | same |
| 2. A2 covered ship radar-lit (388 smokes): died / caught | 27.1 against 13.1; 20.9 against 6.3 | same |
| 2. A2 calm smokes | 513; died 8.9; caught 3.7 | same |
| 2. A2 radar-lit in the last 40 s: died / caught | 85 of 194; 65 of 124 | same |
| 2. A2 still radar-lit at death: died / caught | 39; 34 | 37; 33 (the recheck allows a lit span to end up to 2 s before the death; the worker's rule is a little wider) |
| 3. A3 Somers / Gearing, Top 6: died; caught | 17.8 / 16.2; 7.8 / 9.5 | same |
| 3. A3 Somers / Gearing, Rest: died; caught | 19.4 / 32.3; 11.8 / 23.6 | same |
| 4. A4 counter-smokes: died / caught per 100 | 133; 24.8 / 15.0 | same |
| 5. B2 smoker died / caught per 100: Italian cruisers; ordinary cruiser smoke | 18.5 / 16.1; 8.2 / 6.3 | same |
| 5. B2 battleships: died / caught per 100 | 17.6 / 8.8 | same |
| 6. B3 long smokes, Top 6 against Rest: died; caught | 15.2 against 25.2; 8.0 against 18.8 | same |
| 7a. Sleeping Giant G1: we took; enemy took the nearest cap | 29% of 21; 7 of 13 | same |
| 8. D1 Top 6 against Rest: died; caught; smoker died; smoker caught | 12.3 / 19.3; 7.8 / 13.4; 8.2 / 15.1; 4.3 / 9.2 | same |
| 8. D1 nearest cap taken; contested cap taken | 39% / 28%; 32% / 23% | same |

Not rechecked by the main session: the intervals; the "no other detection" reading of radar deaths; the undetected share
from the track (item 5); items 7b to 7d (membership rebuilt by the worker from the Round 5 scripts); per-clan values and the
style grouping in item 8 beyond the Top 6 against Rest rows; the counter-smoke angle bands. No figures were made.
One difference a worker reported and did not trace: caught deaths radar-lit in the last 20 seconds come out at 57, where
Round 5b had 56.

Part 1 of this run (code review fixes on `r5b`) was checked separately: 31 unit tests, the repeatability test and the
reference-game test pass, and a two-game trial into a scratch folder matched the batch file by file (36 files) apart from
revision, timestamp and the two known last-digit rounding fields.

---

## Items 1 to 4

Scripts in `x1-topics/`.


All scripts are in `round5c/x1-topics/`; shared helpers in `xlib.py`; definitions in `round5c/r5clib.py`. Tables are also in `topics.json` (key = item) and `out-aN.json`.

| headline number | script | variable | value |
|---|---|---|---|
| A1 n cap-contest smokes | a1.py | len(CC) | 391 |
| A1 Rest: radar cruiser inside vs no cruiser, we took the contested cap % | a1.py | T1 / J['by_cover'][..]['we_took_c'] | 77.27 vs 18.82 |
| A1 Top 6: radar cruiser inside vs no cruiser, we took the contested cap % | a1.py | T1 / J['by_cover'][..]['we_took_c'] | 60.0 vs 69.57 |
| A1 gap radar cruiser inside minus no cruiser, we took contested: Rest / Top 6 | a1.py | T3 / J['cover_gaps'] | +58.5 (+43.0 to +75.5 *) / -9.6 (-29.0 to +3.8) |
| A1 gap radar cruiser inside minus no cruiser, all: damage, died, caught | a1.py | T3 / J['cover_gaps'] | +13,368 (+8,699 to +17,029 *); -0.1 (-8.9 to +9.7); +3.2 (-4.3 to +10.6) |
| A1 pressed minus not pressed, all: damage, died, caught | a1.py | T5 / J['pressed_gaps'] | +5,826 (-18,281 to +17,351); -15.8 (-25.0 to -7.2 *); -11.5 (-17.3 to -4.9 *) |
| A1 wider reading, press minus no press, all: damage, we took contested, died, caught | a1.py | T8 / J['pressed_wide_gaps'] | +2,530 (-5,432 to +9,471); +1.5 (-15.7 to +23.2); +10.9 (-6.5 to +26.5); +9.7 (-4.7 to +25.9) |
| A2 baseline died / caught per 100 | a2.py | J['baseline'] (death_rates(DD)) | 194 ships, 18.18 / 124, 11.55 |
| A2 50+ behind: died with / without; caught with / without | a2.py | T1 / J['conditions'] key behind | 34.91 / 12.37; 23.1 / 7.53 |
| A2 radar-lit covered ship: died with / without; caught with / without | a2.py | T1 / J['conditions'] key lit_covered | 27.06 / 13.11; 20.88 / 6.27 |
| A2 calm smokes: n, died per 100, caught per 100 | a2.py | CALM / J['calm'] | 513, 8.86, 3.7 |
| A2 radar deaths, died: (a) / (b) / (c) of n | a2.py | RAD['died']['ways'] (DIED_D, judge()) | 85 / 39 / 25 of 194 |
| A2 radar deaths, caught: (a) / (b) / (c) of n | a2.py | RAD['caught']['ways'] (CAUGHT_D, judge()) | 65 / 34 / 20 of 124 |
| A2 caught, radar-lit in the last 20 s | a2.py | RAD['caught']['ways']['a20'] | 57 |
| A3 Top 6: Somers vs Gearing, died / caught per 100 | a3.py | T1 / J['rates'] | 17.78 vs 16.22 / 7.78 vs 9.46 |
| A3 Rest: Somers vs Gearing, died / caught per 100 | a3.py | T1 / J['rates'] | 19.41 vs 32.32 / 11.76 vs 23.58 |
| A3 Somers minus Gearing inside Rest: died / caught | a3.py | T2 / J['somers_minus_gearing'] | -12.9 (-24.5 to -0.4 *) / -11.8 (-23.7 to -2.1 *) |
| A3 Somers minus Gearing inside Top 6: died / caught | a3.py | T2 / J['somers_minus_gearing'] | +1.6 (-18.2 to +17.4) / -1.7 (-6.7 to +4.9) |
| A3 Gearing, Top 6 minus Rest: died / caught | a3.py | T3 / J['top6_minus_rest'] | -16.1 (-30.4 to -3.6 *) / -14.1 (-26.6 to -4.8 *) |
| A4 n counter-smokes, usable line of fire | a4.py | len(CS), len(USE) / J['summary'] | 133, 132 |
| A4 all counter-smokes: died / caught per 100 | a4.py | T_PAYS / J['what_pays'] row 'all counter-smokes' | 24.81 / 15.04 |
| A4 flanking: died / caught per 100; head-on: died / caught | a4.py | T_ANGLE / J['by_angle'] | 50.0 / 25.0; 24.0 / 15.0 |
| A4 flanking minus head-on: died / caught | a4.py | T_DIFF / J['flanking_minus_head_on'] scope All | +26.0 (-5.0 to +63.3) / +10.0 (-15.4 to +41.1) |
| A4 Gearing counter-smokes: died / caught per 100 | a4.py | T_PAYS row 'Gearing' | 45.0 / 35.0 |

---

## Items 5 to 7

Scripts in `x2-ships-maps/`.


All numbers are computed in `compute_x2.py` and stored in `ships-maps.json`; `write_x2.py` only formats them. Anchors reproduced: 1,547 smokes; 1,074 destroyer smokes (387 Top 6, 687 Rest); 308 early destroyer smokes; destroyer smokes 194 died (18.2 per 100; smoker 12.75) against 124 caught (11.55 per 100; smoker 6.4).

| Headline number | Value | Script and variable |
|---|---|---|
| B2 Italian cruisers smoker died / caught per 100 | 18.5 / 16.1 | compute_x2.py `b2['rows']` -> ships-maps.json B2.rows[label='Italian cruisers together'].died_smoker / caught_smoker |
| B2 battleships ships died / caught per 100 | 17.6 / 8.8 | compute_x2.py `b2['rows']` -> B2.rows[label='All battleships'] |
| B2 Italian cruisers minus ordinary cruiser smoke, smoker died | +10.3 (+3.3 to +17.3), clear | compute_x2.py `b2['contrasts']` (diff_ci) -> B2.contrasts |
| B2 undetected % of the smoke's life, track (Italian / battleships / ordinary cruiser) | 79.3 / 71.3 / 85.0 | compute_x2.py `s['u_life']`, stat `USTATS['track_life_mean']` -> B2.undet[*].track_life_mean |
| B2 undetected % while inside, track | 80.9 / 73.3 / 86.5 | compute_x2.py `s['u_in']` -> B2.undet[*].track_in_mean |
| B2 round 5 columns reproduced (81.7 / 71.7 / 90.1 and 69.9 / 61.8 / 65.8) | 81.7 / 71.7 / 90.1 and 69.9 / 61.8 / 65.8 | compute_x2.py `undetected_pct`, `s['r5_undet_life']` -> B2.undet[*].batch_covered_mean / r5_life_mean |
| B2 smokes dropped for no detected flag | 3 | compute_x2.py `b2['dropped_total']` |
| B3 four ships: ships died / caught per 100 | 20.9 / 14.2 | compute_x2.py `b3['rows']` -> B3.rows[label='All four'] |
| B3 four ships Top 6 minus Rest, died / caught | -10.0 (-19.1 to -1.6), clear / -10.8 (-17.8 to -6.0), clear | compute_x2.py `b3['tvr']` (boot_diff) -> B3.tvr[label='All four'] |
| B3 Harugumo Top 6 vs Rest caught (round 5: 9.1 vs 35.6) | 9.1 vs 35.6; -26.5 (-43.3 to -13.6), clear | B3.tvr[label='Harugumo'].caught |
| B3 long minus cap sitters died / caught (round 5: +6.9) | +6.8 (+1.0 to +12.4), clear / +6.9 (+3.1 to +11.1), clear | compute_x2.py `b3['long_minus_sitters']` (diff_ci) |
| B3 games won, four ships, died / caught gap | -1.6 (-10.0 to +7.1) / -1.5 (-7.1 to +4.3) | compute_x2.py `b3['win_split']` -> B3.win_split[ship='All four', result='games won'] |
| B3 games lost, four ships, died / caught gap | -5.7 (-25.4 to +6.5) / -14.4 (-27.7 to -5.0), clear | B3.win_split[ship='All four', result='games lost'] |
| 7a G1 we took / enemy took cap A | 6 of 21 (29%) / 7 of 13 (54%, small n) | compute_x2.py `cap_block(mem)` -> C7a[id='sg-cell-1'].caps._n |
| 7a G1 enemy took, cell minus rest of map | +35.3 (+6.3 to +57.5), clear | compute_x2.py `r['vs_rest']` (diff_ci, share_stat) -> C7a[0].vs_rest.enemy_took_n |
| 7a Hotspot G10+H10 we took | 14 of 35 (40%) | C7a[id='hs-cell-1'].caps._n.we_took |
| 7a Sea of Fortune F9+G9 we took | 2 of 8 (25%, small n) | C7a[id='sof-cell-1'].caps._n.we_took |
| 7a cell membership and damage reproduce round 5b | Sleeping Giant G1 21 / 24,101; Hotspot G10+H10 40 / 16,970; Sea of Fortune F9+G9 10 / 24,597; Loop F8 15 / 18,318; Loop F10 9 / 20,728 | compute_x2.py `CELLS` loop against round5b/spots.json |
| 7b smokes within 2 km of B | 34 | compute_x2.py `B` (near_cap_edge_m <= 2000 and near_ncap == 'B') -> C7b.rows[label='Cap B'].n |
| 7b enemy took B / other caps | 1 of 28 (4%) / 9 of 68 (13%); -9.7 (-21.8 to +4.0) | C7b.rows[*].caps._n.enemy_took; C7b.b_vs_other.enemy_took_n (diff_ci) |
| 7b we took B | 7 of 18 (39%) | C7b.rows[label='Cap B'].caps._n.we_took |
| 7b enemy was taking B while the smoke stood (all / when ours) | 6 of 34 (18%) / 3 of 16 (19%) | compute_x2.py `s['inv_n_any']` (TL.invaded on s['near_cap']) -> C7b.rows[label='Cap B'].enemy_in_cap |
| 7c radar smokes at B: tags / log / both | 15 / 15 / 15 | compute_x2.py `c7c['overlap']` |
| 7c enemy took B, radar smokes (all / when ours) | 6 of 14 (43%, small n) / 5 of 9 (56%, small n) | C7c.rows[0].caps._n.enemy_took / enemy_took_when_ours |
| 7c enemy took B, other smokes at B | 12 of 32 (38%) | C7c.rows[1].caps._n.enemy_took |
| 7c radar minus other at B, enemy took | +5.4 (-26.2 to +32.4) | C7c.contrasts[0].enemy_took_n (diff_ci) |
| 7d members of the spot | 28 (15 / 13) | compute_x2.py `mem` (in_ell on round5b/spots.json c5-lp-sitters-b shape) -> C7d.rows[0].n |
| 7d we took B: all / Top 6 / Rest | 11 of 17 (65%) / 7 of 9 (78%, small n) / 4 of 8 (50%, small n) | compute_x2.py `fixed_cap(s, real_letter(s, 'B'))` -> C7d.rows[*].B.we_took |
| 7d Top 6 minus Rest, we took B | +27.8 (+8.1 to +54.2), clear | C7d.tvr_caps.we_took_B (boot_diff) |
| 7d enemy took B | 2 of 15 (13%) | C7d.rows[0].B.enemy_took |

---

## Item 8

Scripts in `x3-clans/`.


Run order, from `round5c/x3-clans/`, each with `python -I -X utf8`: `d1_scores.py`, `d2_structure.py`, `d2_structure.py` again with the environment variable `X3_CLOCK=el` (reproduces round 5b, check only), `d3_profiles.py`, `x3_findings.py`. `run_all.py` does all five and saves the printed output as `d1_output.txt`, `d2_output.txt`, `d2_output_el.txt`, `d3_output.txt`. `d_lib.py` holds the score definitions (`feats`), resampling (`boot_clan`), percentiles (`pctile`) and the hand-written PCA and k-means. Seeds are fixed (519, 520, 521, 1000, 1001), so reruns give the same numbers.

Sanity checks (computed here from the output files):

| Check | Result |
|---|---|
| Smokes, all clans | 1,547 (anchor 1,547) |
| Destroyer-smoke anchor (194 died, 18.2 per 100, smoker 12.75; 124 caught, 11.55, smoker 6.4) | printed by `d1_scores.py` as "anchor destroyer smokes" in `d1_output.txt` |
| Top 6 / Rest smokes and team-games | 538 in 110 / 1009 in 232 |
| "Caught per 100" equals round 5b deaths per 100, all 30 clans | yes |
| Scores identical to round 5b (every clan, every lineup / who / where / movement / concealed-damage score) | yes |
| D2 on the HUD clock reproduces round 5b positions | largest difference 0.0e+00; same four groups: yes |
| Top 6 minus Rest gap of each death and cap score, group value equals the library statistic (`died100`, `caught100`, `share_stat`) | asserted in `d1_scores.py`; the `boot_diff` intervals are in `d1_scores.json` `gaps_bootdiff` |
| `clan_styles.json` structure equal to round 5b | yes |
| Gauge identical to round 5b | 30 of 30 clans |

| Number | Script | Where |
|---|---|---|
| All-smokes totals (ships died, caught, the 9 left-out smokes, smokes each cap rate applies to) | `d1_scores.py` | `N_ALL` -> `d1_scores.json` `n_all` |
| Per-clan values: died / caught per 100, smoker versions, caps taken, not lost, caps per game | `d_lib.py`, `d1_scores.py` | `feats(clan, strict=True)` -> `V[clan][key]`; `d1_scores.json` `values`; n per rate in `n_cases` |
| Per-clan 95% intervals | `d1_scores.py` | `I[clan][key]` from `d_lib.boot_clan` (600 resamples of the clan's games); `d1_scores.json` `intervals` |
| Percentiles among the 24 clans | `d1_scores.py` | `PC[clan][key]` from `d_lib.pctile`; `d1_scores.json` `percentiles` |
| Lowest / median / highest table | `x3_findings.py` | `lmh(key)` over `values` of the 24 clans |
| Top 6 minus Rest on every score | `d1_scores.py` | `grp_feats(top)`, `grp_feats(rest)`, `REPS` (500 clan resamples, seed 1000) -> `GAPS`; `d1_scores.json` `gaps`; `clan_styles.json` `top6_minus_rest` |
| Same gaps with the library helper | `d1_scores.py` | `XCHECK` from `boot_diff(S, stat)` (seed 1001); `d1_scores.json` `gaps_bootdiff` |
| What the clock switch moved (first smoke, after 12:00, before 5:00) | `x3_findings.py` | `tm`: `values` here against `round5b/part-d/d1_scores.json`; `x3_changes.json` `time_moves` |
| Scale shares, loadings, clan positions | `d2_structure.py` | `shares`, `vecs`, `scores` from `pca(Z)`; `d2_structure.json` `shares`, `loadings`, `scores`; flagged clans in `proj` |
| Shuffled-data shares | `d2_structure.py` | `null1`, `null2` (300 column shuffles); `d2_structure.json` `null` |
| Shape of the two scales (largest gap, low-smoke clans) | `d2_structure.py` | `SHAPE` -> `d2_structure.json` `shape` |
| Silhouettes, agreement under resampling, scale steadiness | `d2_structure.py` | `SIL`, `aris`, `r1`, `r2`; `d2_structure.json` `silhouette`, `boot`; `clan_styles.json` `structure.stability` |
| Four corners, members, borderline shares | `d2_structure.py`, `d3_profiles.py` | `KM2[4]`, `keep[4]` -> `d2_structure.json` `km2`, `keep2`; `d3_tables.md` "Style members"; `clan_styles.json` `styles` |
| Moved: yes / no per clan | `x3_findings.py` | `moved`: `clans.<name>.style` here against `round5b/clan_styles.json`; `x3_changes.json` `styles` |
| Style pooled numbers and ranges | `d3_profiles.py` | `POOL[i]` from `pool()` (400 game resamples); `d3_tables.md`; `clan_styles.json` `styles[].numbers` |
| Outcome scores against the two scales | `d2_structure.py` | `OUTR` -> `d2_structure.json` `outcome_r` |
| Top 6 against Rest on the two scales; chance figures | `d3_profiles.py` | `AX`, `p_all`, `p4`; `clan_styles.json` `structure.top6_vs_rest_on_axes`, `top6_concentration` |
| Gauge values for H-SR and HTDOG | `d3_profiles.py` | `clan_styles.json` `clans.<name>.gauge` |
| Every "round 5b" number | `x3_findings.py` | read from `round5b/part-d/d1_scores.json`, `round5b/part-d/d2_structure.json`, `round5b/clan_styles.json` |

Headline numbers as computed:

| Headline | Value |
|---|---|
| Died per 100, Top 6 / Rest (gap 95%) | 12.27 / 19.30 (-13.31 to -2.59 *) |
| Caught per 100, Top 6 / Rest | 7.81 / 13.38 (-9.52 to -2.88 *) |
| Smoker died per 100 | 8.18 / 15.10 (-12.28 to -3.15 *) |
| Smoker caught per 100 | 4.28 / 9.22 (-8.60 to -2.55 *) |
| Nearest cap taken % | 38.99 / 28.47 (+0.48 to +21.45 *) |
| Contested cap taken % | 32.16 / 22.77 (+1.10 to +17.60 *) |
| Nearest cap not lost % | 85.71 / 82.95 (-3.29 to +8.62) |
| Contested cap not lost % | 83.57 / 75.82 (+1.89 to +15.27 *) |
| Scale shares | 29.61% / 17.81% (round 5b 29.61% / 17.81%) |
| Clans that moved style | none |

Notes:
- `d_lib.py` never reads `cap_won`, `cap_def`, `s['we_took']`, `s['enemy_took']` or `s['el']` in the default run. `s['el']` is read only when `X3_CLOCK=el` is set, to prove the rerun matches round 5b.
- "Not lost" on the contested cap uses the distance to the contested cap (`s['edge'] <= 2000`); on the nearest cap `near_cap_edge_m <= 2000`, as the brief says.
- The Top 6 minus Rest intervals in the tables come from the round 5 method (pooled group value, whole clans resampled, 500 runs). The library helper `boot_diff` (1,000 runs) gives the same reading for every death and cap score; both are shown in D1.
- No library problem found. `r5clib.py` was not edited.
