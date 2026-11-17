# CHECK: where every number in ATLAS-CONTENT.md comes from

Batch `output/20261117-122135`. Paths are relative to `smoke/analysis/`. "tables.txt" is `atlas/tables.txt`, written by `atlas/scripts/atlas_build.py`.

How to reproduce, from the repo root:

- `python -I -X utf8 smoke/analysis/atlas/scripts/atlas_build.py` rewrites `spots.json`, `caps.json`, `maps/maps.json` and `tables.txt` (one block per map, sections named as below).
- `python -I -X utf8 smoke/analysis/atlas/scripts/atlas_figs.py` redraws the figures from `spots.json` and `caps.json`.
- `python -I -X utf8 smoke/analysis/atlas/scripts/check_copy.py` prints the word counts and the wording check.
- `python -I -X utf8 smoke/analysis/atlas/scripts/validate_package.py` checks the JSON files, links, maps and figures.
- Numbers quoted from a module are reproduced by that module's own scripts (named in each module file).

Two meanings of "cap taken" are used, as in the sources: for **cells and zones** (Module 4) it is the share of all smokes in the cell after which the contested cap was taken ("cap taken after 53%"); for **spots, early clusters and radar addresses** (Part B, Module 3, this build) it counts only smokes whose contested cap was not already ours ("cap taken 3 of 5").

## Page 1: universal rules

| Text | Value | Source | Reproduce |
|---|---|---|---|
| Rule 1: opening smoke short of the cap | 14% inside a cap; 1.8 km outside the cap edge; n 187 (Harugumo, Somers, Gearing, first 5 min); cruiser about 950 m on the spawn side | `round3/module-2/MODULE-2.md` finding 1 | `module-2/stats.py` (`stats.txt`) |
| Rule 2: radar cruiser inside the early smoke | Top 6 60% (61 of 102), Rest 35% (70 of 200), +25 (+13 to +36); Sleeping Giant 47% vs 59% | `round3/module-3/MODULE-3.md` finding 7(a) and its table; counts repeated in tables.txt line "ALL MAPS early destroyer smokes" | `module-3/tables3.py`; `atlas_build.py` |
| Rule 3: caps go with the cruiser, not the press | cap-contest smokes with a radar ship inside, no radar play: 74% of 53; cap control: 58% of 50; no radar ship inside: 32% | `round3/module-3/MODULE-3.md` finding 5 | `module-3/tables2.py` |
| Rule 4: radar from smoke 2.5 times as often | 0.47 vs 0.19 per team-game, 52 and 44 plays, +0.28 (+0.14 to +0.40); cap taken 58% for both (24 and 26 smokes) | `round3/module-3/MODULE-3.md` findings 1 and 6 | `module-3/tables.py`, `tables2.py` |
| Rule 5: deaths follow score and radar, not distance | 23.1 per 100 behind by 50+ (n 277); 6.5 ahead (n 372); 25.0 with enemy radar (n 120) vs 9.9 (n 954); inside the cap 12.1, 3 to 5 km 10.7; Okinawa 22 per 100 (n 82) | `round3/module-5/MODULE-5.md` sections 3 and 4 | `module-5/m5_numbers.py` (`numbers-r4.txt`) |
| Rule 6: Somers vs Gearing | 14.5k (n 260) vs 16.3k (n 180), -1.8k (-5.4k to +3.4k); deaths 10.4 vs 17.8 per 100, -7.4 (-16.5 to -0.6) | `round3/module-5/MODULE-5.md` section 4 | `module-5/m5_numbers2.py` |
| Rule 7: counter-smokes | 8.0k vs 11.2k (-5.5k to -0.9k), n 133 counters; flank smoke lines 13.7k vs 16.0k (-7.2k to +2.1k); most common on Land of Fire (18% of destroyer smokes) | `round3/module-5/MODULE-5.md` section 6 | `module-5/m5_numbers.py` |
| Rule 8: radar cruiser inside, all destroyer smokes | 47% (n 387) vs 29% (n 687), +18 (+8 to +28); with a second destroyer forward 16% vs 9% (+3 to +12) | `round4/part-b/SPOTS.md` "Cast pattern across maps"; 47.3 and 29.0 repeated in tables.txt line "ALL MAPS destroyer smokes" | `part-b/spots_report.py`; `atlas_build.py` |
| Rule 8: Land of Fire Svea parks alone | no cruiser inside any of the 14 Top 6 Svea smokes at F5 | `round4/part-b/SPOTS.md` spot 2; tables.txt Land of Fire, "cast_cruiser: recorded for 0 of 14" | `atlas_build.py` |

## Pages 2 to 8: map pages

Every line of a map page is one line of that map's block in `tables.txt`. Signature and lead numbers are copied from `round4/part-b/spots.json` (the build also recounts the Top 6 smokes inside each Part B ellipse: all 11 match).

| Page line | Values | Source | tables.txt section |
|---|---|---|---|
| Signature and lead lines (all maps) | Top 6 n of total vs Rest n of total, gap, interval, clans, formation counts | `round4/part-b/spots.json`, `SPOTS.md` | SIGNATURE SPOTS AND LEADS |
| Cruiser inside n of n, destroyer ahead, km away | cast counts and distances for each spot | `round4/part-b/SPOTS.md` cast lines; recomputed in `atlas_build.py` `cast_records()` | SIGNATURE SPOTS AND LEADS, `cast_cruiser` / `cast_second_dd` lines |
| Paying spots | concealed damage per smoke, n, deaths per 100, cap taken after % | `round3/module-4/cells.json` (flags high / low) | PAYING CELLS |
| Cap choice | share of each group's destroyer smokes per cap zone; interval | shares: `round3/module-4/cells.json` zones; intervals: `round3/module-4/tables-r4.txt` "zones (nearest cap)" lines, parsed by `atlas_build.py` | CAPS AND CAP CHOICE |
| Early setup | early smokes per cluster, Top 6 count, cruiser count and km behind the smoke centre, second destroyer ahead | `atlas_build.py` (mean-shift at 2 km on early destroyer smokes; `cast_of()`) | EARLY SETUP and the `cast_*` lines under each cluster |
| Radar cruiser inside, per map | Top 6 x of n vs Rest x of n; intervals | counts: tables.txt EARLY SETUP header line; intervals: `round3/module-3/MODULE-3.md` table (a) | EARLY SETUP |
| Radar | plays per cap, cap taken x of y, Top 6 count; Svea plays | `atlas_build.py`, grouped by contested cap as in `round3/module-3/MODULE-3.md` finding 2 and its table (same counts) | RADAR FROM SMOKE |
| Deaths | smokes with a death per cluster, deaths per 100 smokes laid in the ellipse, map rate, behind by 50+ | `atlas_build.py` (all classes, mean-shift at 2.5 km); zone and cell rates from `cells.json` | DEATHS IN SMOKE |
| Examples | link, clan, ship, cell | `s['link']` of Top 6 smokes; Part B examples or the cluster examples | "example" lines |

Map by map, the exact numbers:

| Page | Text | Value in tables.txt |
|---|---|---|
| 2 Sleeping Giant | Signature 1 | sg-harugumo-g1: 11 of 24 vs 1 of 9, +34.7 (+20.0 to +56.2); cast_cruiser n 9 of 11, radar cruiser 9; cast_second_dd forward 5 of 7 |
| 2 | Signature 2 | sg-flank-f9: 14 of 67 vs 5 of 74, +14.1 (+1.4 to +25.9); cast_cruiser 11 of 14; Somers 11 of the 14 (`SPOTS.md` spot 6) |
| 2 | Lead | sg-gdansk-g6: 10 of 21, HTDOG 7 |
| 2 | Paying spots | G1 24,101 (n 21); E1 25,542 (n 10); F5 6,700, F6 5,111, G6 3,906 |
| 2 | Cap choice | zone A 41.8% vs 35.2% (-9 to +21) |
| 2 | Early setup | sg-early-g1: n 39 of 69, Top 6 22; cast_cruiser n 26 of 39, -0.6 km fwd; radar cruiser inside 15 of 32 (47%) vs 22 of 37 (59%) |
| 2 | Radar | sg-radar-a: n 10, cap won 3 of 5; sg-radar-c: n 13 |
| 2 | Deaths | sg-deaths-e9: 8 smokes, 22.9 per 100 in the ellipse, map 11.5 |
| 3 Hotspot | Lead | hs-flank-g6: 13 of 64 vs 7 of 80 (-7.5 to +27.8); cast_cruiser 12 of 13 |
| 3 | Paying spots | G6 16,679 (n 14, median 2,673; not flagged); F5 3,875 (n 15, Top 6 0); F6 5,370 (n 17) |
| 3 | Cap choice | A 13.8% vs 1.9% (+5 to +16); B 22.5% vs 11.6% (+2 to +23); D 35.0% vs 51.6% (-31 to -4); C 28.8% vs 34.8% |
| 3 | Early setup | hs-early-g10 n 36 of 68; hs-early-g5 n 27; cast_cruiser at G10 -0.6 km fwd; radar cruiser inside 20 of 23 vs 17 of 45 |
| 3 | Radar | hs-radar-d: n 10, cap won 4 of 7; hs-radar-c: n 9, Top 6 7 |
| 3 | Deaths | hs-deaths-g10: 8 smokes, 9.9 per 100 in the ellipse, map 6.2 |
| 4 Loop | Signature 1 | loop-cap-f7: 15 of 23 vs 13 of 65, +45.2 (+24.6 to +70.0); cast_cruiser recorded 1 of 15 |
| 4 | Lead | loop-gdansk-f8: 8 of 12; Rest 0 of 1 |
| 4 | Paying spots | F8 18,318 (n 15); F10 20,728 (n 9); F7 3,113, cap won after 53.3% (n 15) |
| 4 | Cap choice | A 22.0% vs 49.5% (-49 to -7); B 43.9% vs 28.7% (-1 to +45); C 34.1% vs 21.8%; zone A 4,823 per smoke, n 59 |
| 4 | Early setup | loop-early-f4 n 14 (Top 6 4); loop-early-f8 n 10 (Top 6 2); cast_cruiser recorded 4 of 14 and 4 of 10 |
| 4 | Radar | destroyer radar plays 6 |
| 4 | Deaths | no group of 8; cell F10 33.3 per 100 (n 9) |
| 5 Mountain Range | Signature 1 | mr-parked-h1: 12 of 33 vs 0 of 13; Jinan 8, Svea 4 (`SPOTS.md` spot 4); cast_second_dd forward 7 of 8 |
| 5 | Lead | mr-svea-g4: 10 of 24 vs 3 of 13 (-28.0 to +61.5); BONKZ 8 |
| 5 | Paying spots | G7 11,510 (n 13), G4 7,584 (n 13); neither flagged |
| 5 | Cap choice | B 43.6% vs 32.5% (-6 to +30); C 30.9% vs 46.8% (-40 to +3) |
| 5 | Early setup | mr-early-g7 n 17 (Top 6 6), cruiser -0.9 km; mr-early-g4 n 15 (Top 6 7), cruiser -0.6 km, second destroyer forward 11 of 15; radar cruiser inside 9 of 14 vs 8 of 25 |
| 5 | Radar | mr-radar-b: n 10, Top 6 7, cap won 1 of 6; Svea radar plays 7 |
| 5 | Deaths | no group of 8; zones A 6.7, B 8.2, C 9.4 per 100 |
| 6 Land of Fire | Signature 1 | lof-svea-f5: 14 of 19 vs 4 of 21, +54.6 (+8.9 to +87.0); cast_second_dd 2.7 km from the puff |
| 6 | Paying spots | F6 8,775, cap won after 54.5% (n 11); F5 4,017 (n 16) |
| 6 | Cap choice | A 27.1% vs 48.8% (-36 to -8); B 45.8% vs 35.0% (-19 to +37); D 25.0% vs 8.8% (-6 to +41) |
| 6 | Early setup | lof-early-f5 n 15 (Top 6 6); lof-early-f3 n 13 (Top 6 5), cast_cruiser 9 of 13, -0.4 km, Des Moines 5; cast_second_dd forward 11 of 12, cells F5/F4 |
| 6 | Radar | destroyer radar plays 9, cap A 5; Svea radar plays 3, cells F5 |
| 6 | Deaths | lof-deaths-f3: 8 smokes, Top 6 0, 33.3 per 100, map 15.3; lof-deaths-f6: 8 smokes, 13.3 per 100 |
| 7 Sea of Fortune | Signature 1 and Formation | sof-svea-h7: 15 of 18 vs 1 of 14, +76.2 (+41.7 to +100.0); formation 10 of 15, second destroyer most often in F8 |
| 7 | Paying spots | F2 11,972 (n 14); map average 11,566 |
| 7 | Cap choice | B 26.3% vs 41.8% (-36 to +5); D 36.8% vs 29.1% (-9 to +30) |
| 7 | Early setup | sof-early-f2 n 14 (Top 6 4), cast_cruiser 9 of 14, cells G3/F2; sof-early-f9 n 10 (Top 6 2); radar cruiser inside 6 of 9 vs 6 of 22; interval +15 to +62 from `MODULE-3.md` table (a) |
| 7 | Radar | destroyer radar plays 5, cap D 4 |
| 7 | Deaths | sof-deaths-f2: 13 smokes, 20.0 per 100, map 14.1 |
| 8 Okinawa | Summary | destroyer smokes Top 6 15; 22.0 deaths per 100 destroyer smokes (n 82) |
| 8 | Paying spots | D1 12,029 (n 8), 25.0 deaths per 100 |
| 8 | Cap choice | C 53.3% vs 47.8%; A 13.3% vs 35.8% (-43 to +9); Top 6 n per zone 2, 2, 8, 3 |
| 8 | Early setup | oki-early-d2: n 12 of 26, Rest 11; cast recorded 3 and 4 of 12; radar cruiser inside Rest 4 of 23, Top 6 2 of 3 (not quoted, under 8) |
| 8 | Radar | destroyer radar plays 7, cap C 4 |
| 8 | Deaths | oki-deaths-h4: 12 smokes, 30.8 per 100, behind by 50+ 7 |

## Page 9: clan styles

| Text | Value | Source |
|---|---|---|
| Long smoke style definition | 305 smokes, 67 games; 61% flank-smoke-line ships, 40% stacked, 27% selfish, 20% stationary, first smoke 2:43 | `round4/part-d/STYLES.md` conclusion 1 and "Style definition" table; `styles.json` |
| Cruiser smoke style definition | 188 smokes, 29 games; 45% parked-cruiser ships, 20% stacked, 51% selfish, 45% stationary, first smoke 3:50; all gaps clear of zero | same |
| Supporting cast | destroyers per game 3.3 and 3.3; cruisers carrying smoke 0.3 vs 1.2; cruiser share of smoke damage 73% vs 82%; smoker 23% vs 65%; second destroyer forward 29% (n 252) vs 18% (n 92), -1 to +22 | `STYLES.md` conclusions 3, 4, 5 and "Supporting cast" table |
| Conclusions | H-SR 71% flank lines, 50% stacked, first smoke 2:00; KITE 45 smokes | `STYLES.md` conclusion 2 |
| Map captions | Sleeping Giant 39% / 46% (80 smokes) vs 59% / 8% (51); Hotspot 21 of 71, 14 smokes; Mountain Range 74% vs 23% (50, 26); Land of Fire 60% vs 17% stationary, 16 of 40 in F5 | `STYLES.md` "Where each style smokes" |
| PN | 14 smokes, 10 destroyer; nearest the long-smoke style; 0 of 10 destroyer smokes in a spot | `STYLES.md` PN call-out; `round4/part-b/SPOTS.md` "PN: 0 of its 10 destroyer smokes" |

Reproduce: `round4/part-d/clan_styles.py`.

## Sidebar: ship habits

| Text | Value | Source |
|---|---|---|
| Four habits, ships, n, stationary / stacked / inside shares | flank smoke lines n 562, 55% stacked; cap sitters n 462, 50% stationary, 37% inside a cap; parked cruiser smoke n 241, 67% stationary; moving exhaust n 188 | `round3/module-1/MODULE-1.md` finding 1 |
| Return and deaths per habit | 15.8k; 5.3k; 8.4k; 4.1k and 17.0 deaths per 100 | `round3/module-5/MODULE-5.md` section 2 |
| Places | Hotspot G10 (flank lines 20% in G10), Hotspot cap C (cap sitters 40% in F5/F6/G5/G6), Land of Fire F5 (Top 6 Svea) | `round3/module-1/MODULE-1.md` findings 2 and 5 |
| Grozovoi and Shimakaze | moving-line share Shimakaze 64% (52 to 78, n 58), Grozovoi 53% (34 to 83, n 30, MACHX 15 of 30), Gdańsk 41%, Daring 10%; not two clean modes; same players do both | `round4/part-e/SHIP-VARIANCE.md` findings 1, 3, 4 and table 1; `ship-variance.json` |

Reproduce: `round3/module-1/tables.py`, `round3/module-5/m5_numbers.py`, `round4/part-e/ship_variance.py`.

## Footer

| Text | Value | Source |
|---|---|---|
| Batch, smokes, games | `output/20261117-122135`, 1,547 smokes, 171 games | tables.txt line 1 |
| Top 6 W-L | H-SR 20-2, RESIN 17-7, BONKZ 13-8, HTDOG 12-6, KITE 9-5, VRTUS 7-4 | tables.txt line 2 |
| Placebo | 2.5 spots pass on average with six Rest clans as the "top" group (20 draws, range 0 to 5) | `round4/part-b/SPOTS.md` findings; `round4/part-b/checks.json` |

## Where the sources disagree, and which value the atlas uses

| Number | Values | Used |
|---|---|---|
| All early destroyer smokes, radar cruiser inside, interval | Module 2: +13 to +35; Module 3: +13 to +36 (same data, different resampling draw) | +13 to +36 (Module 3, as in the brief) |
| Sea of Fortune, same measure | Module 2: +16 to +62; Module 3: +15 to +62 | +15 to +62 (Module 3, to match the line above) |
| Sleeping Giant Harugumo second destroyer / Hotspot lead cruiser position | Part B centre for the Hotspot lead cruiser is 0.002 to 0.003 off this build's mean (Part B averaged every cruiser inside; this build takes the nearest one per smoke) | Part B centre kept in `spots.json`; the shape is from this build |
| "Cap taken" | Module 4 cells: after % of all smokes; Part B and Module 3: only smokes whose cap was not already ours | each kept as in its source and worded differently (see top of this file) |
| Sleeping Giant deaths | Module 5 names F1/G1 and "between B and D" from destroyer smokes by eye; this build clusters all classes at 2.5 km and finds the west flank (11 smokes) and the east between C and D (8); the B to D group has 4 smokes | this build; the page quotes only the east cluster's rate and notes it is small n |
