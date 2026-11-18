# CHECK-N4: where every number in FINDINGS-N4.md comes from

Run order: `python -I -X utf8 n4_c1.py`, `n4_c2.py`, `n4_c3.py` (each writes `out-cN.json` and prints the same tables), then `n4_figs.py`, then `n4_report.py` (writes FINDINGS-N4.md, CHECK-N4.md, page1.json from the JSON files). Shared prep is `n4lib.py`. "Atlas / round 4" values are typed into `n4_report.py` from `atlas/ATLAS-CONTENT.md` page 1, `ROUND4-CHANGES.md`, `round3/module-2/MODULE-2.md` and `round3/module-3/MODULE-3.md` in the old checkout.

| Number | Script | Where |
|---|---|---|
| Early smokes by the three ships (n): 187 (clock bug in) / 188 (corrected) | n4_c1.py | out-c1.json pops[three ships].n; A_bug |
| Laid inside a cap: 14% (clock bug in) / 14% (corrected) | n4_c1.py | pops[three ships].A_inside_cap_pct |
| Median distance outside the cap edge: 1.8 km (clock bug in) / 1.7 km (corrected) | n4_c1.py | pops[three ships].A_median_edge_m; A_bug |
| N4-1 layer B row "Smokes (Top 6 / Rest)" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Smoke outline inside a cap (batch field)" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Smoke edge to contested cap edge, median (batch field)" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Smoker inside a cap when it pressed smoke" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Smoker inside a cap at the end of laying" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Smoker to nearest cap edge at activation, median" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Smoker to nearest cap edge at the end of laying, median" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Smoker on the own-spawn side of that cap at activation" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Covered cruiser to nearest cap edge while the smoke stood, median" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Covered cruiser inside a cap at any time while the smoke stood" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Covered cruiser inside a cap for most of that time" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Contested cap at activation: neutral / ours / theirs" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| N4-1 layer B row "Contested cap being captured while the smoke stood: by us / by the enemy / by nobody" | n4_c1.py | out-c1.json pops[*] keys A_* and B_* (function block) |
| All early destroyer smokes, radar cruiser inside: 60% (61 of 102) vs 35% (70 of 200) (clock bug in) / 59% (61 of 103) vs 35% (71 of 203) (corrected) | n4_c2.py | out-c2.json rungs.inside.table[All maps]; A_bug |
| Gap: +25 (clock bug in) / +24 (corrected) | n4_c2.py | rungs.inside.table[All maps].diff; A_bug |
| Gap interval: +13 to +36 (clock bug in) / +12 to +35 (corrected) | n4_c2.py | rungs.inside.table[All maps].ci; A_bug |
| Sleeping Giant: 47% vs 59% (clock bug in) / 47% vs 59% (corrected) | n4_c2.py | rungs.inside.table[Sleeping Giant] |
| Hotspot: 87% vs 38% (clock bug in) / 87% vs 38% (corrected) | n4_c2.py | rungs.inside.table[Hotspot] |
| Harugumo, Somers, Gearing only: 82% vs 51% (clock bug in) / 82% vs 52% (corrected) | n4_c2.py | three_ships.inside; A_bug |
| Three ships, gap interval: +17 to +47 (clock bug in) / +16 to +46 (corrected) | n4_c2.py | three_ships.inside.ci; A_bug |
| Cap won after: radar cruiser inside vs covered, not inside (three ships): 58% (n 117) vs 14% (n 29) (clock bug in) / 58% (n 118) vs 14% (n 29) (corrected) | n4_c2.py | cap_three_ships.rows.batch_all; A_bug |
| Cap taken, all early destroyer smokes: radar cruiser inside vs not: 61% (of 120) vs 31% (of 150) (clock bug in) / 61% (of 120) vs 31% (of 153) (corrected) | n4_c2.py | cap_all_early.rows.batch_takeable; A_bug |
| N4-2 ladder, all maps, 'Radar cruiser inside (batch field)' | n4_c2.py | out-c2.json rungs.inside.table[All maps]; per_team_game.inside |
| N4-2 ladder, all maps, 'Inside and ran radar from it' | n4_c2.py | out-c2.json rungs.used.table[All maps]; per_team_game.used |
| N4-2 ladder, all maps, 'Ran radar from it and lit an enemy' | n4_c2.py | out-c2.json rungs.lit.table[All maps]; per_team_game.lit |
| N4-2 ladder, all maps, 'Ran radar from it and lit an enemy destroyer' | n4_c2.py | out-c2.json rungs.lit_dd.table[All maps]; per_team_game.lit_dd |
| N4-2 per-map row All maps | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[All maps] |
| N4-2 per-map row Sleeping Giant | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[Sleeping Giant] |
| N4-2 per-map row Hotspot | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[Hotspot] |
| N4-2 per-map row Mountain Range | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[Mountain Range] |
| N4-2 per-map row Land of Fire | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[Land of Fire] |
| N4-2 per-map row Loop | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[Loop] |
| N4-2 per-map row Okinawa | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[Okinawa] |
| N4-2 per-map row Sea of Fortune | n4_c2.py | out-c2.json rungs.inside/used/lit_dd.table[Sea of Fortune] |
| N4-2 cap taken, measure batch_all | n4_c2.py | out-c2.json cap_three_ships.rows / cap_all_early.rows |
| N4-2 cap taken, measure batch_takeable | n4_c2.py | out-c2.json cap_three_ships.rows / cap_all_early.rows |
| N4-2 cap taken, measure tl_cont | n4_c2.py | out-c2.json cap_three_ships.rows / cap_all_early.rows |
| N4-2 cap taken, measure tl_near | n4_c2.py | out-c2.json cap_three_ships.rows / cap_all_early.rows |
| N4-2 cap taken, measure tl_cont10 | n4_c2.py | out-c2.json cap_three_ships.rows / cap_all_early.rows |
| Destroyer smokes tagged as a radar play: 96 (52 Top 6, 44 Rest) (clock bug in) / 96 (52 Top 6, 44 Rest) (corrected) | n4_c3.py | out-c3.json A.dd_plays |
| Per team-game: 0.47 vs 0.19 (clock bug in) / 0.47 vs 0.19 (corrected) | n4_c3.py | A.dd_plays.top/rest |
| Gap interval: +0.14 to +0.40 (clock bug in) / +0.14 to +0.40 (corrected) | n4_c3.py | A.dd_plays.ci |
| Cap taken after cap-control smokes (caps not ours): 58% (of 24) vs 58% (of 26) (clock bug in) / 58% (of 24) vs 58% (of 26) (corrected) | n4_c3.py | A.cap_control_cap_taken |
| Three busiest maps: 69 of 96 (0.45, 0.40, 0.36 per team-game) (clock bug in) / 69 of 96 (0.45, 0.40, 0.36 per team-game) (corrected) | n4_c3.py | A.three_maps, A.by_map |
| Enemy ships lit per smoke with radar run (batch field): 1.1 vs 1.1 (clock bug in) / 1.1 vs 1.1 (corrected) | n4_c3.py | A.spots_per_radar_smoke |
| N4-3 count row "1. Tag-based (old): destroyer smokes tagged as a radar play" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "1b. Tag-based, all smoker classes" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "2. Log: radar presses from inside any allied smoke" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "2a. ... inside a destroyer smoke" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "2a-i. ...... by another ship (a cruiser in the destroyer's smoke)" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "2a-ii. ...... by the smoker itself (a radar destroyer)" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "2b. ... inside a cruiser's own smoke" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "2c. ... inside another cruiser's smoke" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "3. Log: smokes with at least one radar press from inside" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "3a. ... destroyer smokes" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "3b. ... cruiser smokes" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "Context: all radar presses, in smoke or not" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 count row "Context: radar presses not from smoke" | n4_c3.py | out-c3.json A.dd_plays / A.all_class_plays / B.from_smoke / B.from_dd_smoke / B.by_kind / B.smokes_with_activation / B.all_activations / B.not_from_smoke |
| N4-3 map row Sleeping Giant | n4_c3.py | out-c3.json B.by_map[Sleeping Giant], A.by_map[Sleeping Giant] |
| N4-3 map row Hotspot | n4_c3.py | out-c3.json B.by_map[Hotspot], A.by_map[Hotspot] |
| N4-3 map row Mountain Range | n4_c3.py | out-c3.json B.by_map[Mountain Range], A.by_map[Mountain Range] |
| N4-3 map row Land of Fire | n4_c3.py | out-c3.json B.by_map[Land of Fire], A.by_map[Land of Fire] |
| N4-3 map row Loop | n4_c3.py | out-c3.json B.by_map[Loop], A.by_map[Loop] |
| N4-3 map row Okinawa | n4_c3.py | out-c3.json B.by_map[Okinawa], A.by_map[Okinawa] |
| N4-3 map row Sea of Fortune | n4_c3.py | out-c3.json B.by_map[Sea of Fortune], A.by_map[Sea of Fortune] |
| N4-3 return row "Enemy ships lit per play" | n4_c3.py | out-c3.json B.return_from_smoke.lit |
| N4-3 return row "Plays that lit at least one enemy" | n4_c3.py | out-c3.json B.return_from_smoke.lit_any |
| N4-3 return row "Enemy destroyers lit per play" | n4_c3.py | out-c3.json B.return_from_smoke.lit_dd |
| N4-3 return row "Plays that lit at least one enemy destroyer" | n4_c3.py | out-c3.json B.return_from_smoke.lit_dd_any |
| N4-3 return row "Damage on lit enemies while lit, per play" | n4_c3.py | out-c3.json B.return_from_smoke.dmg |
| N4-3 return row "... shells, torpedoes and secondaries only" | n4_c3.py | out-c3.json B.return_from_smoke.dmg_direct |
| N4-3 return row "Plays with any damage on a lit enemy" | n4_c3.py | out-c3.json B.return_from_smoke.dmg_any |
| N4-3 return row "Check: health the lit enemies lost while lit (ship tracks)" | n4_c3.py | out-c3.json B.return_from_smoke.hp_loss |
| N4-3 return row "Check: same damage from the other team's replay" | n4_c3.py | out-c3.json B.return_from_smoke.dmg_run2 |
| N4-3 return row "Nearest cap taken within 60 s (caps not ours)" | n4_c3.py | out-c3.json B.return_from_smoke.cap60 |
| N4-3 return row "Nearest cap taken within 120 s (caps not ours)" | n4_c3.py | out-c3.json B.return_from_smoke.cap120 |

## Self-checks

| Check | Result | Script / where |
|---|---|---|
| Headline counts (radar cruiser inside, Top 6 and Rest) recounted from the raw ship list of each smoke | findings 61 and 71; recount 61 and 71 | n4_c2.py, check_headline_second_way |
| Track position vs round 5 snapshot at the fully-laid moment (three-ship smokes) | median 2.5 m, 90% within 7.0 m, n 175 | n4_c1.py, check_track_vs_snapshot |
| Smoker in a cap: snapshot vs track at end of laying | 10.3% vs 10.2% | n4_c1.py, check_snapshot_smoker_in_cap |
| Cap owner at activation: cap timeline vs batch field | 100.0% agree (three ships), 100.0% (all early) | n4_c1.py, check_own_tl_vs_batch_agree_pct |
| Outline distance recomputed from the laid path vs batch field | median gap 173.0 m; inside / outside agree 97.3% | n4_c1.py, check_outline_* |
| Batch cap_won captures confirmed by the cap timeline (early destroyer smokes) | 127 of 127; the captured cap is the contested cap in 55, the nearest in 60 | n4_c2.py, check_cap_won |
| Radar presses from inside a smoke, whole batch (STEP 9 table says 155 of 2,426) | 155 of 2426 | n4_c3.py, B.from_smoke.n, B.all_activations.n |
| Radar presses from inside a smoke recounted from the raw radar.csv files (no library) | 85 Top 6, 70 Rest = 0.77 and 0.30 per team-game (findings: 85, 70; 0.77, 0.30) | n4_report.py, raw |
| Tagged destroyer radar plays that have a logged press from inside | 96 of 96 | n4_c3.py, B.tag_vs_log |
| Damage on lit enemies: first replay vs the other team's replay vs health lost on tracks (per press, Top 6 / Rest) | 7,488 / 5,814 vs 7,433 / 5,796 vs 5,971 / 4,594 | n4_c3.py, B.return_from_smoke.dmg / dmg_run2 / hp_loss |
| Group sizes | early destroyer smokes 103 + 203; team-games 110 + 232 | n4_c2.py, n4_c3.py |
