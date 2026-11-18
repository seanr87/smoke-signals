All paths under `round5/part-a/`. "Table" = the heading in the `.txt`; the same rows are in the matching `.json` and in `topics.json` under A1..A4.

| Number(s) | Script | Where |
|---|---|---|
| 391 cap-contest smokes, 130/261, tag = primary purpose | a1.py | out-a1.txt lines 1-2; `CC`, `CCP` |
| A1 main table (n, cap taken, cap won, enemy kept off, damage, deaths) and Top 6 vs Rest intervals | a1.py | first table; `rows[*][stat]['all'/'split']` |
| A1 radar minus no cruiser / minus non-radar, all, Top 6, Rest | a1.py | "Differences between cover groups"; `group_differences` |
| A1 neutral caps 60.0 vs 24.5 | a1.py | "By who held the cap" and "Neutral caps only"; `by_cap_owner`, `neutral_only_differences` |
| A1 169 of 211 agreement; median 5 snapshots | a1.py | last line; line 3 |
| A1 clans | a1.py | clan lines after first table; `rows[*].clans` |
| A1 second way (cap_won counts 19/30, 15/23, 19/22, 15/85) | merge.py | printed "A1 cap_won / n" |
| 124 deaths, 117 smokes, who-died table | a2.py | "1. Totals"; `who` |
| A2 baselines (6.4, 8.2, 15.5, 22.5, 11.5 and splits) | a2.py | "5. Like-with-like baselines"; `like_with_like`; any-death interval -10.9 to -2.5 from "Baseline" |
| Cruiser inside 7.9 / behind 8.4 | a2.py | lines after section 5 table; `cruiser_inside`, `cruiser_behind` |
| By map, by cap, by time, by score, time x score | a2.py | "By map", "By map and nearest cap", "By time of activation", "By score state", "By time and score state"; `by_map`, `by_map_cap`, `by_time`, `by_state`, `by_time_state` |
| Death times 12/54/50/8 | a2.py | "death-time of the ships" |
| Strict radar deaths 19, map/cap/time/state, radar ships, distances, 85% of range | a2.py | "3. Radar deaths"; `radar_deaths` |
| Broad radar deaths 45 and breakdowns; 297 smokes; 28.7 vs 27.1 | a2.py | "BROAD radar deaths" block; `radar_deaths_broad`, `radar_rates_broad` |
| Radar rate rows (25.0, 9.9, by state, map, radar class) | a2.py | "Deaths per 100 where enemy radar reached"; `radar_rates` |
| +15.1 and +22.7 differences; 11.4 vs 11.1 | a2.py | "radar reached vs not", "broad radar vs not", "share of smokes radar reached" |
| Conditions table | a2.py | "All destroyer smokes" under section 4; `conditions_all` |
| 585 smokes / 17 deaths / 2.9; 107 deaths elsewhere; calm 2.1 vs 3.5; calm conditions | a2.py | "smokes neither..." line, "Only smokes that were neither..." table, "calm T6 vs Rest"; `calm`, `conditions_calm` |
| 57.1 (n 21) and 2.5 (n 394) | a2.py | "Surface spotting x radar x score"; `combos` |
| Marks on the 105 non-strict-radar deaths; 13 with none | a2.py | "non-radar deaths, marks"; `non_radar_marks` |
| Torpedo 6, shells 102, after cleared 27 (12/12) | a2.py | "Victim level" blocks; `victims` |
| Cut short 50, 15 died while laying, 4 s; calm 0 of 12 | a2.py | "smoke cut short" line; calm table row |
| Other smoker classes; exhaust 16.1, parked 6.3, Napoli 22 | a2.py | "All classes of smoker" and two lines after; `all_classes` |
| A2 second way (297 smokes / 83 deaths; 777 / 41; totals 1,074 / 124, 1,547 / 177) | merge.py | printed "A2 ..." |
| A3 by-group table | a3.py | first table; `by_group` |
| A3 Top 6 vs Rest within ship | a3.py | "Top 6 vs Rest within each ship"; `top6_vs_rest_within_ship` |
| A3 standardized rows | a3.py | "Standardized"; `standardized` |
| A3 within map | a3.py | "Within map"; `by_map` |
| A3 share 50+ behind 17.3 vs 25.0 | a3.py | "Context" table; `context` |
| A3 BONKZ, -BN-; Rest Gearing by clan; leave-one-out 19.6-26.1; Top 6 by clan | a3.py | "Clans with 8+ smokes of each ship" and last lines; `clans_with_both`, `rest_gearing_by_clan`, `rest_gearing_leave_one_out` |
| A3 second way (Somers 90/7, 170/20; Gearing 74/7, 106/25 smokes/deaths) | merge.py | printed "A3 ..." |
| A4 133, 44/89, classes answered | a4.py | line 1 |
| A4 132 usable, 94/38/1; distance, delay, same cap, angle, bands, bearing; 54 self-targeted | a4.py | lines 2-6; `summary` |
| A4 angle table | a4.py | "By angle off the enemy smoke's line of fire"; `by_angle` |
| A4 flanking minus head-on, 45-degree split, Rest only | a4.py | "Differences (a - b)", "Two-way split"; `angle_differences`, `by_angle_2` |
| A4 two checks | a4.py | "Same, only pairs where..." and "Check: line of fire from ships hit, leaving out..."; `by_angle_targets_only`, `by_angle_excl_self` |
| A4 within habit; 9 of 12 cap sitters | a4.py | "Angle bands within ..." and "habit mix by band"; `angle_within_habit` |
| A4 what pays rows | a4.py | "By what the counter-smoke covers", "By ship", "By habit", "By delay", "By distance", "By where the answered smoke lies"; `by_cover`, `by_ship`, `by_habit`, `by_delay`, `by_distance`, `by_bearing` |
| A4 overall Top 6 vs Rest; 6.8% vs 10.2%; medians 10 / 13 degrees, 9.1 / 8.7 km | a4.py | "All matched counter-smokes", "share flanking", "median angle" |
| A4 Rest Gearing 6 deaths in 9, 4 cruisers | a4.py | "Rest Gearing counter-smokes" line |
| A4 clans | a4.py | "clans:" lines under each table; `*.clans` |
