# CHECK-X2: where each headline number comes from

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
