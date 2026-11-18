# Round 5 check: where every number comes from

Batch `output/20261117-122135`. All scripts run as `python -I -X utf8 <script>` from their own folder; `common.py` seeds the
random generator, so reruns give the same intervals. Shared definitions: `r5lib.py` (round 5) on top of `../round3/common.py`.

## Independent recheck by the main session

The headline numbers of every part were recomputed in separate scripts that do not use the parts' code
(`verify/verify_main.py`, `verify/verify_bd.py`, `verify/verify_c5.py`). All matched, with two small differences:

| Item | Part's number | Recheck | Note |
|---|---|---|---|
| A1 cap taken, radar cruiser inside / no cruiser, Top 6 and Rest | 53.3 / 47.8, 76.2 / 12.9 | same | verify_main.py |
| A2 deaths per 100: Top 6 7.5, Rest 13.8; calm smokes 585 with 17 deaths; by score state | same | same | verify_main.py |
| A3 Somers / Gearing by group: 7.8, 11.8, 9.5, 23.6 | same | same | verify_main.py |
| A4 133 counter-smokes; radar cruiser inside 32 at 18,316; all 8,003 | same | same | verify_main.py |
| C1 cap_defended 486 (31.4%); enemy took yes 184 / no 889 / n.a. 474; within 2 km 8.5% vs 15.2% | same | same | verify_main.py |
| C2 teams with more caps at 8:00 won | 60 of 91 | 61 of 92 | one game differs; the cause was not traced and it does not change the reading |
| C3 Hotspot inside cap C: 22 smokes, 7 hurt, no Top 6 | same | same | verify_main.py |
| C4 Sleeping Giant G1: 21 smokes, 24.1k vs 10.7k | same | same | verify_main.py |
| B1 Daring / Gdansk: 671 m, 42.5%, 43.5%, 3,623 / 1,544 m, 26.3%, 56.8%, 8,205 | same | same | verify_bd.py |
| B2 smoker died per 100: 16.1 / 6.3 / 7.5 | same | same | verify_bd.py |
| B3 own-gun share 21.6 / 5.9 / 3.1% | same | same | verify_bd.py |
| B4 length bands Shimakaze 15 / 2 / 39, Grozovoi 6 / 11 / 10 | same | same | verify_bd.py |
| D1 radar cruiser inside 47% vs 29%; D2 smoke cruisers per game 0.3 vs 1.2; D3 H-SR and HTDOG headline values | same | same | verify_bd.py |
| C5 Sleeping Giant Somers west 17% vs 51%; after 5:00 1 of 22 vs 15 of 30 | same | same | verify_c5.py |
| C5 Hotspot west caps | 36% vs 14% | 35% vs 12% | the part counts by nearest cap; the recheck by the batch's contested cap |
| C5 Hotspot early radar cruiser inside 87% vs 38%; Loop 0.70 early smokes per team-game; Okinawa top 5 ships | same | same | verify_c5.py |

Not rechecked by the main session: the intervals themselves (they come from the shared `boot_diff` / `boot_stat`), the
placebo and shuffle runs, the principal-component and grouping work in D2, and the per-spot clan lists beyond Hotspot cap C.
Figures: 33 working figures. The workers report viewing at least 8 of them (A 3, B 3, C1 2); the main session viewed 3 more (c4-sg, c5-sg-somers-east-west, d2-style-map). The rest were not viewed.

How the part files were written: workers A, B, C1, C5 and D returned their findings text in their reports and the main
session saved it unchanged into `part-*/FINDINGS-*.md` and `CHECK-*.md`. Part C4's files were written by its own script.

---

## Part A

Scripts in `part-a/`.

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

---

## Part B

Scripts in `part-b/`.


All numbers come from `part-b/ships.py` (run `python -I -X utf8 ships.py`; seeded, deterministic; about 3 to 4 minutes). It prints to `out.txt` and writes `ships.json`. `show.py` prints compact views of `ships.json` into `show.txt`. Intervals: `boot_stat` (single value), `boot_diff` (Top 6 minus Rest), `set_diff` / `ship_diff` in `ships.py` (ship A minus ship B, resampling clans).

Sanity checks printed at the top of `out.txt`: 1,547 smokes; destroyer smokes 387 Top 6 / 687 Rest; sum of shooters' concealed damage equals sum of smoke concealed damage (14,878,663 both).

| Number(s) | Script | Where |
|---|---|---|
| **B1** table: n, clans, median distance, % inside, % for a teammate, concealed damage per smoke, with intervals | ships.py | section "B1 cap sitters", table rows `<ship> / all`; json `B1.rows` (metrics `edge_med_m`, `inside_pct`, `teammate_pct`, `conc_per_smoke`, each with `_ci`) |
| B1 Top 6 / Rest values per ship | ships.py | same table, rows `top6`, `rest`, `top6 minus rest`; json `B1.rows` |
| B1 Daring minus Gdansk, all / Top 6 / Rest, with intervals | ships.py | lines "Daring minus Gdansk ..." and "Daring minus Gdansk [top] / [rest] n 34/60, 166/58"; json `B1.contrasts` |
| B1 medians without Mountain Range cap A (671 / 1,841 / 1,028 / 3,546 m; -1,170 m, -2,261 to +12) and the cap A counts (2, 3, 0, 0, 1, 4) | ships.py | column `edge_med_no_mrA_m`; lines "<ship> mrA smokes N" |
| B1 second check (55% vs 44% within 1 km; 55% vs 75% with any concealed damage; medians 601 vs 3,564) | ships.py | lines "check Daring ..." / "check Gdansk ..." |
| B1 Z-42 Top 6 minus Rest distance +5,326 m (+1,818 to +6,228) | ships.py | B1 table row "Z-42 / top6 minus rest" |
| B1 clan lists | ships.py | lines "<ship> mrA smokes ... | Top 6: ... | Rest: ..." (`clan_counts`) |
| **B2** table: all rows (deaths, smoker died, hurt per 100; unseen % of covered time; unseen % of smoke life; escape tag %) | ships.py | section "B2 getaway smokes" table; json `B2.rows` (`deaths_per_100`, `smoker_deaths_per_100`, `hurt_smoker_per_100`, `undetected_pct_of_covered_time`, `undetected_pct_of_smoke_life`, `escape_tag_pct`) |
| B2 baselines (all smokes 11.4 / 7.5 / 16.2; cruiser ordinary smoke 7.4 / 6.3 / 14.4; all cruisers; destroyers) | ships.py | same table, rows starting "BASELINE" |
| B2 contrasts (Italian cruisers minus ordinary cruiser smoke +10.5 / +9.8 / +8.2 / -8.4; minus all other smokes; battleship contrasts) | ships.py | lines "Italian cruisers minus ...", "Battleships minus ..."; json `B2.contrasts` |
| B2 who dies (27 of 30 the smoker; 3 of 3) | ships.py | lines "Italian cruisers dead by class", "Battleships dead by class" |
| B2 spotted at activation 70 / 68 / 54 / 29%, health 68 / 68 / 73% | ships.py | line "smoker hp at activation, mean % ..." (csv fields `smoker_spotted_act`, `smoker_hp_pct_act`) |
| B2 cut short 11.3 / 11.8 / 2.6%; concealed damage 6,296 (4,464 to 8,322) and 3,969 | ships.py | B2 table columns `cut_short_pct`, `conc_per_smoke` |
| B2 escape tag difference +1.2 (-6.7 to +9.3) | ships.py | line "Italian cruisers minus cruiser ordinary smoke | escape_tag_pct" |
| B2 Top 6 vs Rest (15 vs 153 smokes; 33.3 vs 14.4; +19.0, +1.6 to +52.5; battleships 10.0 vs 8.3) | ships.py | B2 table rows "Italian cruisers ... top6 / rest / top6 minus rest", "All battleships ..." |
| B2 clan lists | ships.py | lines "<group> n ... | Top 6: ... | Rest: ..." |
| **B3** deployment table (damage, distance, teammates' share, selfish, radar narrow / broad) | ships.py | section "B3 long smokes" table; json `B3.rows` (`conc_per_smoke`, `edge_med_m`, `teammate_share_of_damage_pct`, `selfish_pct`, `smoker_only_label_pct`, `enemy_radar_spotted_pct`, `enemy_radar_broad_pct`); also `show.txt` block "--B3" |
| B3 radar narrow 170 vs broad 372 smokes | ships.py | line "detected_by kinds ... narrow and broad 170 372" |
| B3 location table (centre / side lane / map edge; land distance; near land; open water) | ships.py | same table, columns `centre_pct`, `side_lane_pct`, `map_edge_pct`, `land_med_m`, `near_land_pct`, `open_water_pct`; zone definition in `lat_of`, `border_of` |
| B3 land distance missing 106 of 562 | ships.py | line "land_m missing 230 of 1547 | on long ships 106" |
| B3 long ships minus cap sitters (all contrasts) | ships.py | lines "Long minus cap sitters ..."; json `B3.contrasts` |
| B3 map-edge share by map (Hotspot 47% of 144, Sleeping Giant 41% of 141, Mountain Range 10% of 78) | ships.py | lines "long ships on <map>" |
| B3 Harugumo own-gun table (21.6 / 5.9 / 3.1%; 3,978 / 851 / 501; 43.0 / 9.6 / 8.9%; 18.0 / 3.5 / 2.8%; 55 / 41 / 38.5 s; radar cruiser inside; second destroyer shares) and its contrasts | ships.py | section "B3 Harugumo own guns and spotting proxies" table and lines "Harugumo minus Somers / Gearing ..."; json `B3.harugumo.rows`, `B3.harugumo.contrasts` |
| B3 Harugumo median length laid 3.9 km, 4% parked | ships.py | same table, `path_med_m`, `stationary_pct` |
| B3 radar cruiser inside vs not (69 smokes 11.6% / 2,413; 31 smokes 57.1% / 7,462; +45.5, +18.1 to +71.6) | ships.py | lines "{'ship': 'Harugumo', 'case': ...}" and "Harugumo no radar CA minus radar CA"; json `B3.harugumo.by_cruiser_inside` |
| B3 Delny 1 of 22, 1.1% | ships.py | Harugumo table row "Delny / all" (`smoker_dealt_any_pct` 4.5, `own_gun_share_pct` 1.1) |
| B3 nearest-ally table (53 / 30 / 18 enemies; shares; median distances) | ships.py | lines "<ship> all OWN-GUN targets: {...}" (function `nearest_roles`); json `B3.harugumo.nearest_ally_to_targets` |
| B3 nearest-ally contrasts | ships.py | lines "Harugumo minus Somers / Gearing nearest=..."; json `B3.harugumo.contrasts` |
| B3 second destroyer detail (13 cases: 6 / 5 / 2; 28 of 43 smokes, 3.3 km, 46%, 29%; ship names) | ships.py | `second_dd_where` inside "Harugumo all OWN-GUN targets"; line "Harugumo smokes where smoker dealt concealed dmg 43 ..." |
| B3 Top 6 vs Rest gaps (selfish -11.6; deaths -10.8; Harugumo open water +22.3; Gearing radar cruiser +32.3; Somers second destroyer +23.5; own-gun 22.4 vs 20.8) | ships.py | rows "top6 minus rest" in the B3 and Harugumo tables; `show.txt` lines with "top6 minus rest" |
| B3 clan lists | ships.py | lines "<ship> n ... zone ... | Top 6: ... | Rest: ..." |
| Round 4 comparison (12 of 20) | round4/part-b/SPOTS.md | lines 53 and 93 |
| **B4** main table (spread, cap distance IQR, top purpose, entropy, parked / between / line, median length) | ships.py | section "B4 hybrids" table; json `B4.rows`; `show.txt` block "--B4" |
| B4 measured-length counts 27 / 56 / 197 / 115 | ships.py | line "path length missing by ship"; `two_modes` rows `n` |
| B4 contrasts table | ships.py | lines "Shimakaze minus Daring / Gdansk", "Grozovoi minus Daring / Gdansk", "Gdansk minus Daring"; json `B4.contrasts` |
| B4 two-modes table (band counts; bimodality coefficient 0.69 / 0.49 / 0.44 / 0.48; hump positions 340 m and 2.0 km; 0 of 200; 24% and 18%) | ships.py | lines "{'ship': ..., 'bimodality_coefficient': ..., 'path_bands_n': [...]}" and "<ship> vs random <ship> samples of n=..."; json `B4.two_modes` |
| B4 players table | ships.py | lines "{'ship': ..., 'players_6plus': ..., 'players_3plus': ...}" and the per-player rows under them; json `B4.players` |
| B4 without HFANS (12 / 2 / 17 / 12) and without MACHX (15 smokes, 4 / 4 / 1 / 3) | ships.py | lines "bands without HFANS", "bands without MACHX", "without MACHX n 15" |
| B4 grid cells 18 to 20 at n=30 | ships.py | json `B4.matched_n` (`cells_for_80pct_at_n30`) |
| B4 per-map spread on Hotspot (14.8 / 11.4 / 9.6 / 6.8 km) | ships.py | line "same-map spread km Hotspot" |
| B4 Top 6 vs Rest (Shimakaze 26.7 / 66.7 vs 26.8 / 70.7; Gdansk parked +13.2, lines -25.0) | ships.py | B4 table rows top6 / rest / top6 minus rest |
| Round 4 figures quoted (64 / 53 / 41 / 10%; 26 / 20 / 41 / 64%; 13.5 vs 9.7 km) | round4/part-e/SHIP-VARIANCE.md | findings 1 and 2, table 1 |
| Round 3 figures quoted (Daring 56% / Gdansk 43% smoker only; 8 / 13 / 14%) | round3/module-1/MODULE-1.md | supporting table |

Definitions used (all in `ships.py`):
- for a teammate = `classification.coverage.stacked or .screen`
- selfish = batch `selfish_smoke`
- radar narrow = `radar_on_us > 0`; radar broad = any covered smokee with a `detected_by` kind of radar
- parked = movement label stationary (under 500 m); line = length laid 1 km or more
- own-gun share = smoker's concealed damage over all shooters' concealed damage, pooled
- spread = mean distance from the ship's own per-map centre point (maps with 5+ smokes)

---

## Part C1-C3

Scripts in `part-c1/`.

| number | script | where |
|---|---|---|
| cap_defended rates 31.4 / 33.5 / 26.9%, Top 6 vs Rest gaps | c1_caps.py | `grp_rows(..., s['cap_def'])`; out-caps.md "C1 part 1" table; caps.json `cap_defended.rates` |
| 486 smokes; role 459 middle / 27 enemy side | c1_caps.py | `D`, `def_role`; caps.json `cap_defended.role` |
| nearest cap in 175 of 486; median 8,949 m; 74 touching; 307 over 6 km | c1_caps.py | `def_cap == near_cap`, `def_edge_m` (`de`) |
| kept 60.5% (and rows), 77.0% at 0 s, 51.9% at 120 s | c1_caps.py | `def_lost`, grace loop; caps.json `cap_defended.kept` |
| 86.3% (n 694) comparison | c1_caps.py | `base` |
| hand check 10 of 10 | c1_caps.py | `pick`, `HC`; out-caps.md "Hand check" |
| 0 mismatches of 1,547 | c1_caps.py | `my_took`, `mism` |
| cap_won cross-check 171: 144 / 26 / 1 | c1_caps.py | `cw`; caps.json `enemy_took.cap_won_crosscheck` |
| coverage yes 184 / no 889 / n/a 474 | c1_caps.py | `cov`; caps.json `enemy_took.coverage` |
| snapshots median 5, 111 with one; window 158 s; gap 48 s; tail 21 s; 241 over 60 s | c1_caps.py | `tw`, `lens`, `gaps`, `tails` |
| grace 0 / 60 / 120 s: 103 / 184 / 233 | c1_caps.py | grace table; caps.json `enemy_took.grace` |
| median 2,314 m; 346 over 5 km | c1_caps.py | `ne` |
| enemy-took summary table (17.1%, 18.8%, 11.1% ...) | c1_caps.py | `grp_rows(..., s['enemy_took'])`; caps.json `enemy_took.overall` |
| by map and cap rows | c1_caps.py | caps.json `enemy_took.by_map_cap` |
| replays per game 170 x 2, 1 x 1 | c1_caps.py | caps.json `ribbons.replays_per_game` |
| ribbon source lines | read only | decode.rs 2102-2139; resources.rs 605-650; combat.rs 31-116; smoke-signals render.rs 63-64, 93-94; grep of batch folder |
| C2 coverage 154 / 5 / 12 and per map | c1_caps.py | `cover`; caps.json `c2.coverage` |
| favourite won 110 of 158; 128 of 164 | c1_caps.py | `allg` |
| C2 pooled and per-map rows | c1_caps.py | `c2row`; caps.json `c2.pooled`, `c2.maps[map].all / rest_vs_rest` |
| own side / middle / enemy side labels | c1_caps.py | `role_of`; caps.json `c2.maps[map].caps` |
| 66 of 91 already ahead, lead 95; 120 of 153; 63 level; Top 6 30 / 7 / 46 | c1_caps.py | `ml`, `ah`, `tie`, `tr`; caps.json `c2.notes` |
| C3 baselines 6.4 / 15.5 and 8.0 / 22.0, per map | c1_danger.py | baseline table in out-danger.md |
| 313 areas, 109 tested (77 / 32), 204 unrated | c1_danger.py | `AREAS`, `TEST` |
| 4 flags; 0 on deaths alone | c1_danger.py | `FL`, `flag_died` |
| placebo 1.23 per run, 5 of 120 with 4+ | c1_danger.py | `pl` |
| flagged area rows, intervals | c1_danger.py | `evaluate`, `arow`; danger-zones.json |
| behind / radar shares, clan counts, share gaps, without-top-clan | c1_danger.py | `describe`; danger-zones.json |

---

## Part C4

Scripts in `part-c4/`.


Rerun: `python -I -X utf8 c4_spots.py` (writes `spots.json`, `checks.json`, `generated.md`, `out.txt`, `FINDINGS-C4.md` from `head.md`, and the seven figures), then `python -I -X utf8 c4_wide.py` (writes `wide.txt`). Both are seeded (`random.Random(519)` / `520`), so reruns give the same numbers. `explore.py` only prints pool sizes.

| Number in FINDINGS-C4.md | Script | Where |
|---|---|---|
| 1,547 smokes; destroyer smokes 387 Top 6 / 687 Rest | c4_spots.py | last `CHECK` line of `out.txt` |
| 21 spots; counts by map and kind (table) | c4_spots.py | `RECS`, `count_table`; one line per spot in `out.txt` |
| 0 of 21 Top 6 spots; 2 "Rest use it more" | c4_spots.py | `label()` on `share_test()`; `mode` and `note` in `spots.json`; `PLACEBO ... real: top 0 of 21` in `out.txt` |
| Per spot: n, n Top 6 / Rest, clans, damage per smoke, deaths per 100, cruisers, examples | r5lib `spot_record` called from c4_spots.py | `spots.json` fields `n`, `n_top6`, `n_rest`, `clans`, `concealed_damage_per_smoke`, `deaths_per_100`, `cruisers`, `examples` |
| Per spot: share Top 6 vs Rest, gap, interval | c4_spots.py `share_test` (2,000 clan resamples) | `share_top6`, `share_rest`, `diff_pts`, `diff_ci`; pool sizes `pool_top6`, `pool_rest` |
| Per spot: cruisers inside / screened by group | c4_spots.py `cr_by` | `cruisers_by_how` |
| Per spot: median time, cells, radius, where | c4_spots.py `base_extra`, `where`, `cells_of` | `median_time`, `cells`, `radius_km`, `where` |
| Early spots: inside vs screened, Top 6 vs Rest | c4_spots.py (family `early_cruiser` block) | `n_inside`, `n_screened`, `inside_top6`, `inside_rest`, `screened_top6`, `screened_rest` |
| hs-sit-1 6% vs 23% (-30 to -5); loop-sit-1 4% vs 20% (-26 to -2) | c4_spots.py | `out.txt` lines `hs-sit-1`, `loop-sit-1` |
| lof-park-1 58% vs 19% (-6 to +70); loop-sit-2 30% vs 9% (-3 to +50); sg-early-1 36% vs 20% (-8 to +38) | c4_spots.py | `out.txt` lines with those ids |
| Wide scale: 25 spots, 2 Top 6; Loop cap B 8 of 23 vs 6 of 65, 35% vs 9% (+3 to +53); Land of Fire F5 14 of 19 vs 5 of 21, 74% vs 24% (+8 to +84); their clans | c4_wide.py | `wide.txt` (lines `Loop | cap_sitter | inside cap B`, `Land of Fire | parked_cruiser`, `TOTAL`); pool sizes 23/65 and 19/21 from the `pool` lines in `out.txt` |
| Placebo main scale: 12 Rest-only spots, 0.33 labelled top on average, range 0 to 3, 200 draws | c4_spots.py | `PLACEBO` dict; `checks.json` |
| Placebo wide scale: 14 spots, 0.54 average, range 0 to 4, 7% of draws with 2 or more | c4_wide.py | last line of `wide.txt` |
| 137 cells or pairs tested, 3 passed | c4_spots.py `high_cells` | `SHUF['tested']`, `SHUF['real']`; `high cells` lines in `out.txt` |
| G1 24.1k vs 10.7k (+8.2k to +20.2k), n 21; Hotspot G10+H10 17.0k vs 11.4k (+0.8k to +10.7k), n 40; Sea of Fortune F9+G9 24.6k vs 10.3k (+1.0k to +32.5k), n 10 | c4_spots.py `cell_test` | `cell_mean`, `rest_of_map_mean`, `damage_gap_ci` in `spots.json`; second check: G1 24.1k n 21 matches round 3 Module 4 |
| Shuffle check: 1.85 cells pass on average (0 to 4), 20 runs | c4_spots.py | `SHUF`; `checks.json` |
| Win/loss: G1 26.5k (n 14) vs 19.3k (n 7); Hotspot 21.3k (n 16) vs 14.1k (n 24); Sea of Fortune 28.0k (n 8) vs 10.9k (n 2) | c4_spots.py `base_extra` | `damage_win`, `damage_loss`, `n_win`, `n_loss`, `win_loss_differs` (rule: > 5k apart, n >= 5 each side) |
| Cap taken: G1 19% of 21; Hotspot 34% of 35; Sea of Fortune 25% of 8 | c4_spots.py `base_extra` (r5lib `we_took`, None left out) | `cap_taken_pct`, `cap_taken_n` |
| Early spots: sg n 16 (12 inside, 4 screened); hs n 17 (13, 4); hs n 9 (7, 2) | c4_spots.py | `sg-early-1`, `hs-early-1`, `hs-early-2` in `spots.json` |
| Okinawa pools 16 to 40 per kind; Top 6 2 to 10 | c4_spots.py | `Okinawa | ...: pool` lines in `out.txt` |
| "No spot" statements per map | c4_spots.py | `NONE[m]`; needs max(8, 10% of the pool) smokes in one circle |

Method constants (top of `c4_spots.py`): bandwidth 1.0 km, circle radius 1.5 to 2.5 km, minimum 8 smokes and 10% of the pool, 2,000 resamples, win/loss rule 5k and n >= 5. Wide check: bandwidth 1.5 km, radius 2.5 to 3.5 km.

---

## Part C5

Scripts in `part-c5/`.


All scripts are in `round5/part-c5/`, run as `python -I -X utf8 <script>`. Each prints to the matching `out-*.txt`; the "where" column names the printed line (search for the quoted text) and the key in `map-questions.json` under `questions`. Intervals are deterministic per script (common.py seeds random); they shift by a point or two if a script's order of calculations is changed.

| Item | Number | Script | Where |
|---|---|---|---|
| SG-1 | West 5 of 30 vs 23 of 45, -34 (-65 to -6) | c5_sg.py | out-sg "all west"; `C5-SG-1.all_west` |
| SG-1 | East 25 of 30 vs 22 of 45, +34 (+6 to +64) | c5_sg.py | "all east"; `all_east` |
| SG-1 | Early 4 of 8 vs 8 of 15 (-56 to +33); east early (-32 to +53) | c5_sg.py | "early west", "early east"; `early_west`, `early_east` |
| SG-1 | After 5:00 1 of 22 vs 15 of 30, -46 (-73 to -18) | c5_sg.py | "after 5:00 west"; `after5_west` |
| SG-1 | East 14.0k (10.9k to 16.5k), west 16.0k (11.5k to 19.4k); deaths 10.6 / 14.3 | c5_sg.py | "east conc all" |
| SG-1 | u 0.74 to 0.99, v 0.40 to 0.95; columns 8 to 10 | c5_sg.py | "top6 east uv box" |
| SG-1 | Clan counts east / west; PFANS 8 of 8, REEEE 5 of 5, HFANS 7 of 7, EPOXY 4 of 4 | c5_sg.py | "east clans", "west clans", per-clan lines; `east_clans`, `west_clans` |
| SG-2 | 11 of 24 vs 1 of 9, +35 (+20 to +56) | c5_sg.py | "spot Top 6 11 of 24"; `C5-SG-2.spot` |
| SG-2 | 7 of 11; Marceau 5, Chateaurenault 1, Ragnar 1; forward 5; median 3.2 km; cells F1 3, G1 2, G3 1, G4 1 | c5_sg.py | "present 7 of 11"; `top6_with_second_dd`, `second_dd_ships`, `second_dd_cells` |
| SG-2 | The 12-row table | c5_tables.py | out-tables "SG-2 list"; `C5-SG-2.smokes` |
| SG-2 | Median 4 allied positions of 9 alive | c5_sg.py | "all smokes median allied positions" |
| SG-3 | Cap table (A 46, B 34, C 17, D 22 and all columns) | c5_sg.py, c5lib.cap_table(edge=2000) | out-sg table under "SG-3"; `C5-SG-3.cap_table` |
| SG-3 | 119 of 305; B 34 within 2 km, 59 nearest | c5_sg.py | "smokes within 2 km of any cap" |
| SG-3 | Daring 15, Gdansk 6; sitters 23; cap contest 26; no cruiser 25; inside 10; 8:12 | c5_sg.py | "within 2 km of B: n 34" and next 4 lines; `at_B` |
| SG-3 | Ours 16: Daring 11, contesting 2, cap defended 2, enemy took 1; not ours 18, we took 5 | c5_sg.py | "B ours at start: n 16", "B not ours at start: n 18" |
| SG-3 | Ours 47% (27 to 72) vs 64% (52 to 75) | c5_sg.py | "ours at start: B" |
| SG-3 | Enemy took 4% vs 7%, diff -4 (-13 to +9); 5 of 68 = table rows A+C+D | c5_sg.py | "enemy took: B" |
| SG-3 | Share of map 13 of 137 vs 21 of 168 (-12 to +7); ours 8 of 13 vs 8 of 21 (-25 to +65) | c5_sg.py | "share of all map smokes", "B ours share"; `share_of_map_smokes`, `ours_share` |
| SG-3 | Nearest-cap rule: 59, 25/21/13, 4 of 46 | c5_sg.py | "nearest cap B, any distance"; `cap_table_nearest_cap_any_distance.B` |
| HS-1 | A, B, A+B, C, D shares and intervals | c5_hs.py | out-hs "destroyer smokes A:" etc.; `C5-HS-1.shares` |
| HS-1 | Within 2 km 14 of 80 vs 14 of 155 (-5 to +24); median 1.8 km | c5_hs.py | "stricter rule"; `within_2km` |
| HS-1 | Early 3 of 23 vs 2 of 45; later 26 of 57 vs 19 of 110 (+20 to +38) | c5_hs.py | "west share by time" |
| HS-1 | Team-games 13 of 18, 14 of 44; 6 of 6 and 10 of 24 clans; 33% to 39% leave-one-out | c5_hs.py | "team-games with a DD smoke", "top clans with any", "Top 6 without" |
| HS-1 | A 19.7k (10.4k to 30.4k), B 15.6k (8.8k to 23.9k); B Top 6 10.5k, Rest 20.8k | c5_hs.py | "  A: n 14", "  B: n 36" and their group lines |
| HS-1 | All classes 33% vs 22% (+4 to +24) | c5_hs.py | "all smokes A+B" |
| HS-2 | 20 of 23 vs 17 of 45 (+31 to +71) | c5_hs.py | "map-wide radar cruiser inside"; `C5-HS-2.map_wide` |
| HS-2 | G10 36 smokes, 10 of 12 vs 11 of 24 (+6 to +63); G5 27, 7 of 8 vs 5 of 19 | c5_hs.py, c5lib.ms_cluster | "in G10 cluster", "G10 cluster:", "G5 cluster:"; `g10`, `g5` |
| HS-2 | Use 12 of 23 vs 24 of 45 (-25 to +20) | c5_hs.py | "share of early smokes in G10"; `g10_use` |
| HS-2 | Inside / screened / none, map and G10 | c5_hs.py | "standing definition", "in G10:" |
| HS-2 | Other maps' gaps | c5_hs.py | per-map lines after "in G10:"; `per_map` |
| HS-2 | Ships, cruisers, per-clan radar counts, 16.5k | c5_hs.py | "G10 ships", "G10 radar cruiser inside by clan", "G10 conc" |
| HS-3 | 13 of 64 vs 7 of 80 (-7 to +27); cruisers; 17.3k / 13.7k; 6 of 49 | c5_hs.py | "HS-3" block: "spot", "top: n 13", "rest: n 7", "without RESIN"; `C5-HS-3` |
| LP-1 | Whole table | c5_lp.py | out-lp first table; `C5-LP-1` |
| LP-1 | Loop minus other maps (four lines); 21 of 46, 99 of 296; 19% vs 28% | c5_lp.py | "Loop minus other maps", "zero early destroyer smokes", "long-smoke ships share" |
| LP-2 | Whole table; zones A 18, B 18, C 5 | c5_lp.py | second table, "Loop first smokes: cells"; `C5-LP-2` |
| LP-3 | Whole table; -24 (-38 to -7); per-ship clan lines | c5_lp.py | third table, "long-ship share of first smokes", "Loop first smoker clans by ship"; `C5-LP-3` |
| LP-4 | 191 / 77 / 17 / 9 rows | c5_lp_daring.py | out-lp-daring first line |
| LP-4 | Whole table | c5_lp_daring.py | table; `C5-LP-4.table` |
| LP-4 | -35 (-55 to -15), -32 (-56 to -11); control differences | c5_lp_daring.py | "radar_in_range_of_cap:", "Daring on Loop, lit_dd_before minus"; `tests` |
| LP-4 | The one case; 9 / 2 / 1; 41 at A; 16 with no radar position | c5_lp_daring.py | "smokes with a signal", "reverse view", "Daring on Loop clans", "none recorded"; `examples`, `reverse` |
| LP-5 | F8, F10, combined rows; 18.3k, 20.7k, 8.0k; individual smokes | c5_lp.py | "F8 long smokes", "F10 long smokes", "F8+F10", "cell averages", smoke list; `C5-LP-5` |
| LP-6 | 15 of 23 vs 13 of 65 (+25 to +72); ships; without Daring 14 of 20 vs 11 of 20; 5.8k / 1.2k; 5 of 10, 1 of 8 | c5_lp.py | "LP-6" block: "spot", "ships top", "Daring only", "top: n 15", "rest: n 13"; `C5-LP-6` |
| MR-1 | 12 of 33 vs 0 of 13 (+31 to +40); Jinan 8 HTDOG, Svea 4 BONKZ; Svea alone 4 of 24; 19.0k; cells; ellipse 17 of 88 vs 9 of 119 | c5_rest.py | out-rest "MR-1" block; `C5-MR-1` |
| MR-2 | Table rows | c5_rest.py | second table under "MR-2"; `C5-MR-2.sets` |
| MR-2 | A 15%, B 36%, C 18% | c5_rest.py | first table under "MR-2"; `cap_table` |
| MR-2 | 53% (25 to 73) vs 28% (14 to 43); median 2.0 km | c5_rest.py | "B ours at start: radar smokes", "distance of the 15" |
| MR-2 | 12 of 88 vs 3 of 119 (+2 to +22); 12 of 35 vs 3 of 33 (+6 to +40) | c5_rest.py | "share of all the group smokes", "share of smokes at B"; `share_of_all_smokes` |
| MR-2 | 10 plays, Top 6 7, 1 of 6; list of 15 | c5_rest.py | "reproduce atlas", "radar at B list" |
| LF-1 | 13 = 5 + 8 (-18 to +39); ship table; wider 19 | c5_rest.py | "LF-1" block: "cluster (atlas mean-shift membership)", "top: n 5", "rest: n 8", "all early destroyer smokes nearest cap A"; `C5-LF-1` |
| LF-2 | 14 of 19 vs 4 of 21 (+7 to +87); clans; 6 of 10; 14.2k | c5_rest.py | "LF-2" block; `C5-LF-2` |
| SF-1 | Cap positions; 14 in cluster, A 8 / B 6; 0.5 km and 7.7 km | c5_rest.py | "caps in the 0-1 frame", "west cluster:" lines; `C5-SF-1.caps_uv`, `west_cluster` |
| SF-1 | 24 of 31; B 15 (10 / 5), D 7 (5 / 2), C 2, A 0; cruisers; 12 of 15 within 2 km | c5_rest.py | "west own-side cap (drawn B)", "east cap D", and the per-smoke list (edge column); `by_cap` |
| SF-2 | Table; 4.6 km; early / later split; per-clan | c5_rest.py | "long smokes at A/B/C/D", "at D by time", "at D: cruisers", per-clan lines; `C5-SF-2` |
| SF-3 | 15 of 18 vs 1 of 14 (+39 to +100); clans; 9.6k | c5_rest.py | "SF-3" block; `C5-SF-3` |
| OK-1 | Table; 36 team-games, 158 smokes | c5_rest.py, c5_tables.py | "OK-1" block; out-tables "OK-1"; `C5-OK-1` |
| OK-2 | 12 smokes, 15 deaths, 7 behind, 10 inside ellipse | c5_rest.py, c5lib.ms_cluster | "atlas death cluster" |
| OK-2 | 39, 12 deaths, 30.8 (13 to 47); map 17.7 (11 to 24); 22.0 | c5_rest.py | "ellipse centre", "map: smokes"; `C5-OK-2` |
| OK-2 | +17 (-3 to +35); 49% (28 to 72), 30% (17 to 44), 35% (23 to 46); +18 (-7 to +43) | c5_rest.py | "zone minus rest of map", "laid 50+ behind" |
| OK-2 | State table | c5_rest.py | "behind 50+:", "level:", "ahead 50+:" lines |
| OK-2 | Classes, ships, who died, radar 2, lost 24; 7 of 23 vs 32 of 135 | c5_rest.py | "zone: class", "zone share of group smokes" |
| Spots | 19 records with shapes | each map script, c5_merge.py | `part-c5/spots.json` |
| Figures | Five figures | c5_figs.py | `round5/figures/c5-*.png` |

Checks made: totals match the brief (1,547 smokes; destroyer smokes 387 Top 6, 687 Rest). Round 3, round 4 and atlas numbers reproduced exactly: Somers 17% vs 51%; Harugumo 11 of 24 vs 1 of 9; Hotspot 36% vs 14% and 87% vs 38%; atlas clusters 36, 27, 13, 14, 10, 12; Loop sitters 15 of 23 vs 13 of 65; Mountain Range 12 of 33 vs 0 of 13 and 10 plays; Land of Fire 14 of 19 vs 4 of 21; Sea of Fortune 15 of 18 vs 1 of 14; Okinawa 22 per 100 and 31 per 100. Loop early rate cross-checked two ways (32 early destroyer smokes over 46 team-games = 0.70).

---

## Part D

Scripts in `part-d/`.


Run order (from `round5/part-d/`, each with `python -I -X utf8`): `d1_scores.py`, `d2_structure.py`, `d3_profiles.py`. `d_lib.py` holds the score definitions (`feats`), the resampling (`boot_clan`), percentiles (`pctile`) and the hand-written PCA / k-means / clustering. Seeds are fixed (519, 520, 521, 1000), so reruns give the same numbers.

Sanity checks printed by `d1_scores.py`: 1,547 smokes summed over clans; 171 games = 342 team-games; destroyer smokes 387 Top 6 and 687 Rest; 30 clans, 24 with 7+ games; Top 6 538 smokes in 110 team-games, Rest 1,009 in 232.

| Number | Script | Where |
|---|---|---|
| Per-clan values (all tables in D1, heat table) | `d1_scores.py` | `V[clan][key]` from `d_lib.feats(clan, strict=True)`; printed in `d1_tables.md` sections Lineup ... Extra; stored in `d1_scores.json` `values` |
| Lowest / median / highest per score (D1 table) | `d1_scores.py` output | min, median, max of `values[clan][key]` over the 24 clans (`d1_scores.json`); names read from `d1_tables.md` |
| Sideways 26%, unclassified 101 | `d1_scores.py` | printed line `movement labels` (horizontal 397 of 1,547; unclassified 101) |
| Mapping of movement labels | `d_lib.py` | `MOVE` dict and its comment (batch `closing_m` is positive when range opened: pushing median -1,838 m, kiting +1,174 m) |
| Smoke ships brought, Top 6 vs Rest, with gaps | `d1_scores.py` | `grp_brings`, `clan_diff`; `d1_tables.md` section "Smoke ships brought, share of games" |
| Ships inside destroyer smokes, Top 6 vs Rest | `d1_scores.py` | `grp_inside`, `clan_diff`; `d1_tables.md` section "Ships inside destroyer smokes" |
| Per-clan brought ships, inside ships, top caps, lanes | `d1_scores.py` | `NOTES[clan]`; `d1_tables.md` section "Smoke ships brought ... and ships inside"; `clan_styles.json` `clans.<name>.notes` |
| Top 6 minus Rest on every score (47% vs 29% radar cruiser inside, 0.2 vs 0.6 exhaust ships, 11,685 vs 8,515, 57,152 vs 37,034, 8 vs 13 deaths, 84% vs 78%, 3.6 vs 3.0 radar ships, and the Shared rows) | `d1_scores.py` | `grp_feats(top)`, `grp_feats(rest)`, `REPS` (500 clan resamples) -> `GAPS`; `d1_tables.md` last section; `d1_scores.json` `gaps`; `clan_styles.json` `top6_minus_rest` |
| 694 smokes with no "taken" answer; 541 smokes with a "not lost" answer (within 2 km of the nearest cap) | `d1_scores.py` | printed line "no taken answer 694 / not-lost answer within 2 km 541 of 1547"; per clan `n_take_known`, `n_hold_known` in `d1_scores.json` |
| Cap not lost: 71% (REEEE, n 17) to 100% (MACH, n 12), median 89% over 21 clans; KSE, NGA, PN too few (7, 7, 5) | `d1_scores.py` | `values[clan]['held_pct']`, `n_hold_known`; same printed line lists the clans under 8 |
| Cap not lost Top 6 92% vs Rest 87% (+0.6 to +9.5) | `d1_scores.py` | `GAPS['held_pct']`; last section of `d1_tables.md` |
| Delny 37 in lineups, 7 carrying smoke | `d1_scores.py` | printed lines "ships with smoke_variant" (Delny 7) and "long/sitter ships WITHOUT smoke_variant" (Delny 30) |
| Clan 95% ranges (headline table, gauge) | `d1_scores.py` | `I[clan][key]` from `d_lib.boot_clan` (600 resamples of the clan's games); `d1_tables.md` section "Headline value"; `d1_scores.json` `intervals` |
| Percentiles (p4, p91, ...) | `d1_scores.py` | `PC[clan][key]` from `d_lib.pctile` against the 24 clans; same section |
| Scale shares 29.5%, 17.4%, 12.3%; 47% together | `d2_structure.py` | `shares` from `pca(Z)`; `d2_output.txt` line "PC shares"; `d2_structure.json` `shares` |
| Shuffled-data 95th percentiles 19.0% and 15.8% | `d2_structure.py` | `null1`, `null2` (300 column shuffles); lines "null PC1 share", "null PC2 share" |
| Links of scores with each scale (-0.84 ... +0.76 ...) | `d2_structure.py` | "PC1 loadings", "PC2 loadings" blocks; `d2_structure.json` `loadings` |
| Smoke cruisers r +0.71 with the first scale, for a teammate -0.82 | `d2_structure.py` | lines "single score vs axes" |
| Largest gap 1.6 of range 8.6; seven low clans at -1.8 or below, others +0.3 or above | `d2_structure.py` | lines "PC1 sorted", "PC2 sorted", "PC2 order" |
| Silhouettes 0.18 / 0.16 / 0.18, shuffled 0.09 to 0.12 | `d2_structure.py` | lines "k=2:", "k=3:", "k=4:" (k-means silhouette and shuffled-data 95th pct) |
| Agreement under game resampling 0.54 (2 groups), 0.34 (3 groups) | `d2_structure.py` | lines "k=2: ARI vs base median", "k=3: ARI vs base median" (200 resamples) |
| Dropping lineup: agreement 0.31 | `d2_structure.py` | block "drop one group, k=2", row "without Lineup" |
| Scale steadiness 0.90 and 0.78 | `d2_structure.py` | line "games resampled within clan": PC1 scores vs base median, PC2 median |
| Two-scale map: 4 corners silhouette 0.47; kept in 86% | `d2_structure.py` | lines "2-axis map k=4" and "2-axis style kept under game resampling, k=4: mean" |
| Style members, borderline shares (HFANS 60% ... NGA 74%), flagged placements | `d2_structure.py`, `d3_profiles.py` | `km2['4']`, `keep2['4']`, `proj[clan].near2` in `d2_structure.json`; `d3_tables.md` section "Style members" |
| Style pooled numbers and ranges; clans / games / smokes per style | `d3_profiles.py` | `POOL[i]` from `pool()` (400 game resamples); `d3_tables.md` first table; `clan_styles.json` `styles[].numbers` |
| W-L by style (101-66, 32-32, 20-25, 12-19) | `d3_profiles.py` | `d3_tables.md` "Style members" lines |
| Round 4 second check (0.3 vs 1.2, 73% vs 49%, 20% vs 45%, 2:43 vs 3:50) | `d3_profiles.py` | `pool(['H-SR','RESIN','BONKZ'])`, `pool(['HTDOG','VRTUS'])`; `d3_tables.md` section "Second check against round 4" |
| Top 6 vs Rest on the two scales (-1.17 / +0.39, gap -1.56, -3.57 to +0.49; +0.90 / -0.30, gap +1.21, +0.22 to +2.24) | `d3_profiles.py` | `AX[0]`, `AX[1]` (2,000 clan resamples); `d3_tables.md` lines "Axis 1", "Axis 2" |
| Chance figures 24% and 9% | `d3_profiles.py` | `p4` (hypergeometric, 4+ of 6 in an 11-of-24 group) and `p_all` (6 of 6 in a 17-of-24 group); last two lines of `d3_tables.md` |
| H-SR and HTDOG gauge values | `d1_scores.py` | `d1_tables.md` section "Headline value"; `clan_styles.json` `clans.H-SR.gauge`, `clans.HTDOG.gauge` |
| 35 scores kept per clan | `d_lib.py` | `ALLKEYS` (the keys of `LABEL`) |

Notes on definitions that differ from earlier rounds:
- "Smoke ship in the lineup" uses the roster field `smoke_variant` (set when the ship carries smoke), not `smoke_activations`, so a ship that brought smoke but never used it still counts.
- "Cap not lost" uses `enemy_took is False` only for smokes inside or within 2 km of the nearest cap (`near_cap_edge_m <= 2000`, `HOLD_NEAR_M` in `d_lib.py`), following this round's validation by another worker. The batch `cap_def` flag fires for any owned cap with an enemy inside, anywhere on the map, so it is kept only as a secondary column in the Extra table and is not read as "the smoke defended a cap".
- Caps taken per game counts distinct caps per game with `we_took` true; the batch flags `cap_won` / `cap_def` are also kept (per smoke, per game) in the Extra table.
- Style building used 17 behaviour scores; the five outcome scores were left out and reported per style afterwards. With outcomes included the first two scales are almost the same (correlation 0.94 and 0.89 with the behaviour-only scales; `d2_output.txt` line "with outcomes included").
