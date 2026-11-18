# Check C5: where every number comes from

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