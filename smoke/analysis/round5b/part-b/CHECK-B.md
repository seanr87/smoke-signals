# CHECK-B: where every number in FINDINGS-B.md comes from

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
