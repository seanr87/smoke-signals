# Module 2: what changed in round 4

Everything was rerun on the corrected shared loader (`common.py`). The CSV, `stats.txt` and all five figures were regenerated. `stats-r3.txt` is the round 3 output, kept for comparison. Numbers not listed here did not change.

## Loader fix (detail records matched on game + smoke id; ship-name spaces; clip ids)

Small effects only. The 187 smokes, their groups, windows, coverage, damage, kills, deaths and cap results are unchanged.

| Where in MODULE-2.md | Old | New |
|---|---|---|
| Finding 1: partners on the spawn side of the smoke centre | 86% | 87% |
| Finding 1: partner distance outside the cap edge (median) | 3.7 km | 3.8 km |
| Finding 4: Rest Gearing non-radar partners | Napoli 4, Smolensk 4 | Napoli 5, Smolensk 3 |
| Finding 7: games where "first cap" is usable | 87 of 171 (83 with both teams holding one) | 88 of 171 (82) |
| Finding 7: same cap vs split, first cap | +14 points (-4 to +29) | +15 points (-3 to +31) |
| Finding 7: first cap was the first-smoke cap | 35% (n 72) | 34% (n 73) |
| One smoke moved cell (id 214651, Land of Fire, BTLST Gearing) | E4, no partner recorded | F3, Napoli in the line of fire |

Interval end points that moved only because the resampling was redrawn (same data, same point estimates):

| Where | Old interval | New interval |
|---|---|---|
| Finding 2: Top 6 smoke in the first 2 minutes | -1 to +33 | -3 to +34 |
| Finding 2: concealed damage Top 6 minus Rest | -7.3k to +6.4k | -7.2k to +6.3k |
| Finding 4: Des Moines partner damage | 14.0k to 28.5k | 13.9k to 28.5k |
| Finding 4: Brisbane partner damage | 8.5k to 17.3k | 8.6k to 17.5k |
| Finding 5: stacked minus screen damage | -0.4k to +9.8k | -0.2k to +9.5k |
| Finding 5: stacked minus screen swing | -16.6 to -1.5 | -16.1 to -1.5 |
| Finding 7: same cap vs split, lead | -19 to +28 | -19 to +27 |
| Finding 7: stacked vs screen first smoke, win rate | +11 to +38 | +11 to +37 |
| Finding 7: first smoke inside cap, win rate | +0 to +44 | +1 to +47 |
| Finding 7: Top 6 lead at 5:00 | +11 to +48 | +11 to +47 |
| Table: non-radar cruiser damage interval | 5.8k to 19.9k | 5.6k to 19.9k |
| Table: no-partner damage interval | 0 to 7.9k | 0.3k to 7.8k |

## Definition change (headline is now "a radar cruiser inside the smoke")

Round 3 counted a radar cruiser covered in any way (inside, behind, or in the line of fire).

| Where in MODULE-2.md | Old (covered in any way) | New (inside the smoke) |
|---|---|---|
| Share of early smokes with a radar cruiser partner | 78% (146 of 187) | 63% (117 of 187); the 78% is kept and labelled "in any way" |
| Top 6 vs Rest | 93% vs 70%, +23 (+10 to +36) | 82% vs 51%, +31 (+15 to +46) |
| Per-map and all-destroyer versions of that number | not reported | new table at the top of MODULE-2.md |
| Partner-type split | radar cruiser 146 / non-radar cruiser 27 / battleship 1 / none 13 | radar cruiser inside 117 / radar cruiser covered, not inside 29 / non-radar cruiser 27 / battleship only 1 / none 13 |
| Radar cruiser row: damage, cap won, deaths | 16.7k, 49%, 0.09 (n 146) | 15.6k, 58%, 0.06 (n 117); not-inside row 21.4k, 14%, 0.21 (n 29) |
| Radar vs non-radar cruiser, damage | +4.2k (-3.2k to +11.1k) | +3.1k (-4.7k to +10.5k) |
| Radar cruiser vs everything else, damage | +7.6k (+1.2k to +13.5k), clear | +1.3k (-3.9k to +6.8k), not clear |
| Radar cruiser vs everything else, cap won | +15 points (+3 to +30) | +32 points (+22 to +43) |
| Radar cruiser vs everything else, deaths | -0.08 (not reported) | -0.13 (-0.23 to -0.02), clear |
| Finding 3 headline | "a partner matters much more than which partner" | "a radar cruiser inside goes with the cap, not with more damage" |
| Finding 7: first smoke radar cruiser partner vs not, lead at 5:00 | +19 (-19 to +54), not clear | +39 (+13 to +65), clear (n 89 vs 54) |
| Finding 7 headline | "no opening smoke pattern clearly goes with the first cap or the 5:00 lead" | location and timing still do not; radar cruiser inside the first smoke does go with the 5:00 lead |
| PN line | 4 of 5 with a radar cruiser | 4 of 5 with a radar cruiser inside (same four smokes) |
| Figure `outcomes` | 4 partner rows | 5 partner rows (inside / not inside split) |
| Figures `setup-main-maps`, `setup-other-maps` | all partner dots filled | filled = inside the smoke, hollow = behind or line of fire |

New in round 4 (no old value): radar cruiser inside by ship (Harugumo 80%, Somers 64%, Gearing 53%); the Sleeping Giant reversal (Top 6 64% vs Rest 77%, interval -40 to +18).

## Wording

"For a player" lines and finding text were rewritten to describe what Top 6 do and what followed, without saying it makes a team win. Changed lines: findings 1, 2, 3, 5, 6, 7.
