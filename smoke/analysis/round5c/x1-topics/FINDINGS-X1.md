# Round 5c findings, worker x1 (items A1 to A4)

Batch `output/20261117-230933`. Written by `x1-topics/build.py` from `a1.py` to `a4.py`. Two death metrics side by side everywhere: "died" = a covered ship died between activation and exactly 20 s after the smoke dispersed (each ship counted once); "caught" = the batch list of smoke deaths (round 5's deaths). Cap results come from the cap timeline with 60 s after dispersal. Intervals are 95%, resampling whole clans; * = the interval excludes zero ("clear"). Under 8 = too few (no rate); 8 to 14 = small n. Everything is association, not cause.

### A1. Cap-contest smokes by cover, and radar pressed from the smoke

**Answer:** On the cap timeline, the Rest took the contested cap after 77% of their smokes with a radar cruiser inside against 19% with no cruiser (gap clear); the Top 6 took it after 60% against 70% (gap not clear). So round 5's "76% vs 13% for the Rest, no difference for the Top 6" holds on the timeline; on the nearest cap it is 81% vs 19% (Rest) and 60% vs 70% (Top 6). A radar cruiser inside went with more concealed damage (+13,368 (+8,699 to +17,029 *)) and no clear change in deaths (died -0.1 (-8.9 to +9.7), caught +3.2 (-4.3 to +10.6) per 100). Radar pressed from the smoke is rare here: 8 of 104 smokes, with no death on either metric, too few to split by group. On the wider reading (the cruiser inside pressed radar at some time while the smoke stood, 43 smokes) a press went with concealed damage +2,530 (-5,432 to +9,471), we took the contested cap +1.5 (-15.7 to +23.2), died +10.9 (-6.5 to +26.5) and caught +9.7 (-4.7 to +25.9) per 100.

**Numbers:** 391 destroyer smokes carry the `cap_contest` tag (130 Top 6, 261 Rest). The contested cap and the nearest cap are the same cap in 390 of them. Cap results: an owner change on that cap between activation and 60 s after the smoke dispersed; (n) = smokes where the result could happen (the cap was not already that side's). "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them. Here that removes 1 smoke(s) from the died rates. Under 8 = too few, no rate.

Table 1. By cover and group.
| cover | group | n | we took, contested cap % (n) | we took, nearest cap % (n) | enemy took, contested cap % (n) | enemy took, nearest cap % (n) | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| radar cruiser inside | All | 104 | 67.3 (52) | 68.6 (51) | 13.4 (82) | 13.2 (83) | 16,882 | 14.6 | 10.6 |  |
| radar cruiser inside | Top 6 | 55 | 60.0 (30) | 60.0 (30) | 11.4 (44) | 11.4 (44) | 19,099 | 12.7 | 10.9 |  |
| radar cruiser inside | Rest | 49 | 77.3 (22) | 81.0 (21) | 15.8 (38) | 15.4 (39) | 14,394 | 16.7 | 10.2 |  |
| non-radar cruiser inside | All | 17 | 50.0 (8) | 50.0 (8) | 30.8 (13) | 30.8 (13) | 15,049 | 17.6 | 23.5 |  |
| non-radar cruiser inside | Top 6 | 8 | too few (3) | too few (3) | too few (5) | too few (5) | 20,045 | 25.0 | 12.5 | small n |
| non-radar cruiser inside | Rest | 9 | too few (5) | too few (5) | 50.0 (8) | 50.0 (8) | 10,609 | 11.1 | 33.3 | small n |
| no cruiser | All | 191 | 29.6 (108) | 29.6 (108) | 21.2 (132) | 21.2 (132) | 3,515 | 14.7 | 7.3 |  |
| no cruiser | Top 6 | 46 | 69.6 (23) | 69.6 (23) | 16.2 (37) | 16.2 (37) | 4,121 | 13.0 | 4.3 |  |
| no cruiser | Rest | 145 | 18.8 (85) | 18.8 (85) | 23.2 (95) | 23.2 (95) | 3,322 | 15.2 | 8.3 |  |
| other | All | 79 | 54.5 (44) | 54.5 (44) | 25.0 (64) | 25.0 (64) | 7,768 | 20.2 | 13.9 |  |
| other | Top 6 | 21 | 33.3 (9) | 33.3 (9) | 18.8 (16) | 18.8 (16) | 7,222 | 19.1 | 14.3 |  |
| other | Rest | 58 | 60.0 (35) | 60.0 (35) | 27.1 (48) | 27.1 (48) | 7,966 | 20.7 | 13.8 |  |
| all cap-contest smokes | All | 391 | 44.8 (212) | 45.0 (211) | 20.3 (291) | 20.2 (292) | 8,431 | 15.9 | 10.2 |  |
| all cap-contest smokes | Top 6 | 130 | 61.5 (65) | 61.5 (65) | 13.7 (102) | 13.7 (102) | 11,939 | 14.6 | 9.2 |  |
| all cap-contest smokes | Rest | 261 | 37.4 (147) | 37.7 (146) | 23.8 (189) | 23.7 (190) | 6,684 | 16.5 | 10.7 |  |

"other" is a footnote row: a cruiser screened but none inside, or a non-radar cruiser inside next to a radar ship of another class.

Table 2. Top 6 minus Rest inside each cover group (difference, 95% interval; * = clear).
| cover | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 |
|---|---|---|---|---|---|---|---|
| radar cruiser inside | -17.3 (-39.6 to +4.2) | -20.9 (-44.4 to +0.2) | -4.4 (-15.7 to +6.0) | -4.0 (-15.3 to +6.2) | +4,704 (-4,009 to +11,273) | -3.9 (-24.9 to +10.8) | +0.7 (-13.8 to +10.6) |
| non-radar cruiser inside | too few | too few | too few | too few | +9,436 (-13,316 to +25,028) | +13.9 (-22.2 to +66.7) | -20.8 (-66.7 to +37.5) |
| no cruiser | +50.7 (+40.9 to +66.4 *) | +50.7 (+40.9 to +66.4 *) | -6.9 (-24.4 to +7.1) | -6.9 (-24.4 to +7.1) | +799 (-1,648 to +2,620) | -2.1 (-17.9 to +7.5) | -3.9 (-9.8 to +0.4) |
| other | -26.7 (-56.3 to +2.5) | -26.7 (-56.3 to +2.5) | -8.3 (-29.8 to +9.8) | -8.3 (-29.8 to +9.8) | -744 (-6,566 to +6,097) | -1.6 (-25.6 to +20.1) | +0.5 (-17.7 to +18.3) |
| all cap-contest smokes | +24.1 (+10.4 to +38.3 *) | +23.9 (+10.2 to +38.0 *) | -10.1 (-19.5 to -2.4 *) | -10.0 (-19.3 to -2.3 *) | +5,255 (+260 to +8,765 *) | -1.9 (-12.3 to +6.5) | -1.5 (-8.6 to +4.9) |

Table 3. The gap inside each group: one kind of cover minus another (difference, 95% interval; * = clear).
| gap | group | n a / n b | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| radar cruiser inside minus no cruiser | All | 104 / 191 | +37.7 (+21.5 to +55.2 *) | +39.0 (+21.7 to +57.9 *) | -7.8 (-16.8 to +0.3) | -8.0 (-16.9 to +0.0) | +13,368 (+8,699 to +17,029 *) | -0.1 (-8.9 to +9.7) | +3.2 (-4.3 to +10.6) |  |
| radar cruiser inside minus no cruiser | Top 6 | 55 / 46 | -9.6 (-29.0 to +3.8) | -9.6 (-29.0 to +3.8) | -4.8 (-22.2 to +8.5) | -4.8 (-22.2 to +8.5) | +14,977 (+9,602 to +18,875 *) | -0.3 (-14.6 to +11.8) | +6.6 (-1.5 to +12.2) |  |
| radar cruiser inside minus no cruiser | Rest | 49 / 145 | +58.5 (+43.0 to +75.5 *) | +62.1 (+46.1 to +80.6 *) | -7.4 (-20.9 to +3.4) | -7.8 (-21.0 to +2.8) | +11,072 (+6,196 to +16,361 *) | +1.5 (-12.2 to +17.1) | +1.9 (-8.9 to +14.0) |  |
| radar cruiser inside minus non-radar cruiser inside | All | 104 / 17 | +17.3 (-19.5 to +70.6) | +18.6 (-17.4 to +72.1) | -17.4 (-48.2 to +12.5) | -17.5 (-48.4 to +12.1) | +1,833 (-7,864 to +10,479) | -3.1 (-31.2 to +18.3) | -12.9 (-47.1 to +11.4) |  |
| radar cruiser inside minus non-radar cruiser inside | Top 6 | 55 / 8 | too few | too few | too few | too few | -946 (-8,288 to +10,423) | -12.3 (-71.4 to +18.8) | -1.6 (-65.2 to +15.9) | small n |
| radar cruiser inside minus non-radar cruiser inside | Rest | 49 / 9 | too few | too few | -34.2 (-71.2 to +16.2) | -34.6 (-71.4 to +15.6) | +3,785 (-13,779 to +13,376) | +5.6 (-25.2 to +27.3) | -23.1 (-64.8 to +15.5) | small n |

Table 3b. Like with like: only smokes whose contested cap was neutral at activation (a neutral cap is easier to take).
| cover | group | n (early) | we took, contested cap % (n) | enemy took, contested cap % (n) |
|---|---|---|---|---|
| radar cruiser inside | All | 30 (26) | 66.7 (30) | 16.7 (30) |
| radar cruiser inside | Top 6 | 19 (15) | 63.2 (19) | 15.8 (19) |
| radar cruiser inside | Rest | 11 (11) | 72.7 (11) | 18.2 (11) |
| no cruiser | All | 49 (30) | 38.8 (49) | 20.4 (49) |
| no cruiser | Top 6 | 14 (7) | 78.6 (14) | 7.1 (14) |
| no cruiser | Rest | 35 (23) | 22.9 (35) | 25.7 (35) |

Radar cruiser inside minus no cruiser on neutral caps: All: we took +27.9 (+6.9 to +46.4 *), enemy took -3.7 (-20.0 to +12.5); Top 6: we took -15.4 (-60.0 to +12.2), enemy took +8.7 (-11.1 to +28.6); Rest: we took +49.9 (+34.1 to +75.2 *), enemy took -7.5 (-31.7 to +18.8).

Table 4. Cap-contest smokes with a radar cruiser inside (104): radar pressed from the smoke or not. "Pressed" = a ship of the smoking team pressed radar while standing in this smoke (radar log).
|  | group | n (pressed by a cruiser) | we took, contested cap % (n) | we took, nearest cap % (n) | enemy took, contested cap % (n) | enemy took, nearest cap % (n) | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| radar pressed from the smoke | All | 8 (7) | too few (7) | too few (7) | too few (4) | too few (4) | 22,260 | 0.0 | 0.0 | small n |
| radar pressed from the smoke | Top 6 | 5 (4) | too few (5) | too few (5) | too few (2) | too few (2) | too few | too few | too few | too few |
| radar pressed from the smoke | Rest | 3 (3) | too few (2) | too few (2) | too few (2) | too few (2) | too few | too few | too few | too few |
| not pressed | All | 96 (0) | 71.1 (45) | 72.7 (44) | 14.1 (78) | 13.9 (79) | 16,434 | 15.8 | 11.5 |  |
| not pressed | Top 6 | 50 (0) | 64.0 (25) | 64.0 (25) | 11.9 (42) | 11.9 (42) | 17,484 | 14.0 | 12.0 |  |
| not pressed | Rest | 46 (0) | 80.0 (20) | 84.2 (19) | 16.7 (36) | 16.2 (37) | 15,293 | 17.8 | 10.9 |  |

Table 5. Pressed minus not pressed (difference, 95% interval; * = clear).
| group | n pressed / not | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| All | 8 / 96 | too few | too few | too few | too few | +5,826 (-18,281 to +17,351) | -15.8 (-25.0 to -7.2 *) | -11.5 (-17.3 to -4.9 *) | small n |
| Top 6 | 5 / 50 | too few | too few | too few | too few | too few | too few | too few | too few |
| Rest | 3 / 46 | too few | too few | too few | too few | too few | too few | too few | too few |

Table 6. Top 6 minus Rest inside pressed and inside not pressed.
|  | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 |
|---|---|---|---|---|---|---|---|
| radar pressed from the smoke | too few | too few | too few | too few | too few | too few | too few |
| not pressed | -16.0 (-40.7 to +5.0) | -20.2 (-44.9 to -0.9 *) | -4.8 (-16.0 to +6.3) | -4.3 (-15.8 to +6.6) | +2,191 (-4,775 to +8,178) | -3.8 (-25.8 to +10.7) | +1.1 (-13.2 to +10.7) |

Table 7. Wider reading, because Table 4 is so thin: a cruiser that was inside this smoke pressed radar at some time while the smoke stood, whether the log places the press in this smoke or not (the cruiser had often moved out, or the press was at the smoke edge).
|  | group | n | we took, contested cap % (n) | we took, nearest cap % (n) | enemy took, contested cap % (n) | enemy took, nearest cap % (n) | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| a cruiser from inside pressed radar while the smoke stood | All | 43 | 68.2 (22) | 71.4 (21) | 18.8 (32) | 18.2 (33) | 18,366 | 20.9 | 16.3 |  |
| a cruiser from inside pressed radar while the smoke stood | Top 6 | 23 | 54.5 (11) | 54.5 (11) | 10.5 (19) | 10.5 (19) | 25,057 | 21.7 | 17.4 |  |
| a cruiser from inside pressed radar while the smoke stood | Rest | 20 | 81.8 (11) | 90.0 (10) | 30.8 (13) | 28.6 (14) | 10,672 | 20.0 | 15.0 |  |
| no such press | All | 61 | 66.7 (30) | 66.7 (30) | 10.0 (50) | 10.0 (50) | 15,836 | 10.0 | 6.6 |  |
| no such press | Top 6 | 32 | 63.2 (19) | 63.2 (19) | 12.0 (25) | 12.0 (25) | 14,816 | 6.2 | 6.2 |  |
| no such press | Rest | 29 | 72.7 (11) | 72.7 (11) | 8.0 (25) | 8.0 (25) | 16,962 | 14.3 | 6.9 |  |

Table 8. Wider reading: press minus no press (difference, 95% interval; * = clear).
| group | n press / none | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| All | 43 / 61 | +1.5 (-15.7 to +23.2) | +4.8 (-12.7 to +27.0) | +8.8 (-8.8 to +25.5) | +8.2 (-8.8 to +25.0) | +2,530 (-5,432 to +9,471) | +10.9 (-6.5 to +26.5) | +9.7 (-4.7 to +25.9) |  |
| Top 6 | 23 / 32 | -8.6 (-32.2 to +17.9) | -8.6 (-32.2 to +17.9) | -1.5 (-20.0 to +18.8) | -1.5 (-20.0 to +18.8) | +10,242 (+4,275 to +16,568 *) | +15.5 (-9.5 to +34.7) | +11.1 (-9.5 to +32.4) |  |
| Rest | 20 / 29 | +9.1 (-27.8 to +42.9) | +17.3 (-20.8 to +50.0) | +22.8 (-9.1 to +46.7) | +20.6 (-9.1 to +43.8) | -6,290 (-15,154 to +3,461) | +5.7 (-22.0 to +32.9) | +8.1 (-11.8 to +36.1) |  |

Radar was pressed from the smoke in 9% of the Top 6's 55 such smokes and 6% of the Rest's 49 (gap interval -12.9 to +23.1).

**Top 6 or Shared:** Inside "radar cruiser inside" the Top 6 minus Rest gap is: we took the contested cap -17.3 (-39.6 to +4.2), enemy took it -4.4 (-15.7 to +6.0), died per 100 -3.9 (-24.9 to +10.8), caught per 100 +0.7 (-13.8 to +10.6). Inside "no cruiser": +50.7 (+40.9 to +66.4 *), -6.9 (-24.4 to +7.1), -2.1 (-17.9 to +7.5), -3.9 (-9.8 to +0.4). The extra concealed damage with a radar cruiser inside is in both groups (Top 6 +14,977 (+9,602 to +18,875 *), Rest +11,072 (+6,196 to +16,361 *)): Shared. The Top 6 difference is how often they do it (55 of 130 cap-contest smokes against 49 of 261).

**Clans:** radar cruiser inside: Top 6: BONKZ 15, H-SR 14, RESIN 10, KITE 7, VRTUS 5, HTDOG 4 | Rest: -BN- 6, HFANS 6, EPOXY 5, INCA 5, MACHX 5, KSC 4, MZY 3, PFANS 3, PN 2, KITED 2, RSR 2, MACH 1, BTLST 1, UYSC 1, BONKY 1, SCCC2 1, REEEE 1. Radar pressed from it: Top 6: RESIN 5 | Rest: INCA 1, PN 1, SCCC2 1.

**Could not be done / proxy:** Non-radar cruiser inside has 17 smokes (8 Top 6, 9 Rest): small n overall and too few inside a group wherever the table says so. The pressed split is small inside each group; read the direction only.

**Verdict:** Keep (damage and deaths by cover). The cap line: Keep, reworded with the timeline numbers. Radar pressed from the smoke: Lead (8 smokes; the wider reading is in Tables 7 and 8).

**Changed from round 5b:** round 5b did not redo this table, so the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a1.json`). "-" = too few there. The contested-cap columns and the pressed split are new.

| number | round 5b | round 5c | why |
|---|---|---|---|
| radar cruiser inside, Top 6: we took the nearest cap % | 53.3 | 60.0 | cap timeline (was snapshots) |
| radar cruiser inside, Top 6: enemy took the nearest cap % | 9.1 | 11.4 | cap timeline (was snapshots) |
| radar cruiser inside, Top 6: deaths per 100, now died per 100 | 10.9 | 12.7 | new death metric |
| radar cruiser inside, Rest: we took the nearest cap % | 76.2 | 81.0 | cap timeline (was snapshots) |
| radar cruiser inside, Rest: enemy took the nearest cap % | 10.3 | 15.4 | cap timeline (was snapshots) |
| radar cruiser inside, Rest: deaths per 100, now died per 100 | 10.2 | 16.7 | new death metric |
| non-radar cruiser inside, Top 6: deaths per 100, now died per 100 | 12.5 | 25.0 | new death metric |
| non-radar cruiser inside, Rest: enemy took the nearest cap % | 37.5 | 50.0 | cap timeline (was snapshots) |
| non-radar cruiser inside, Rest: deaths per 100, now died per 100 | 33.3 | 11.1 | new death metric |
| no cruiser, Top 6: we took the nearest cap % | 47.8 | 69.6 | cap timeline (was snapshots) |
| no cruiser, Top 6: enemy took the nearest cap % | 5.4 | 16.2 | cap timeline (was snapshots) |
| no cruiser, Top 6: deaths per 100, now died per 100 | 4.3 | 13.0 | new death metric |
| no cruiser, Rest: we took the nearest cap % | 12.9 | 18.8 | cap timeline (was snapshots) |
| no cruiser, Rest: enemy took the nearest cap % | 20.0 | 23.2 | cap timeline (was snapshots) |
| no cruiser, Rest: deaths per 100, now died per 100 | 8.3 | 15.2 | new death metric |
| other, Top 6: we took the nearest cap % | 11.1 | 33.3 | cap timeline (was snapshots) |
| other, Top 6: enemy took the nearest cap % | 6.2 | 18.8 | cap timeline (was snapshots) |
| other, Top 6: deaths per 100, now died per 100 | 14.3 | 19.1 | new death metric |
| other, Rest: we took the nearest cap % | 57.1 | 60.0 | cap timeline (was snapshots) |
| other, Rest: enemy took the nearest cap % | 22.9 | 27.1 | cap timeline (was snapshots) |
| other, Rest: deaths per 100, now died per 100 | 13.8 | 20.7 | new death metric |

19 other numbers are unchanged: concealed damage in every row, and caught per 100 (it is the same list as round 5 deaths).


### A2. Smoke deaths: conditions, calm smokes, map, time and score, and radar deaths three ways

**Answer:** Both metrics tell the same story about where deaths are: smokes laid 50+ behind (died 34.9 vs 12.4 per 100, caught 23.1 vs 7.5) and smokes where a covered ship was radar-lit (died 27.1 vs 13.1, caught 20.9 vs 6.3). Calm smokes (neither) are 513 of 1074 and lose 8.9 died and 3.7 caught per 100. Radar: of 194 ships that died, 85 (44%) were radar-lit in their last 40 s, 39 (20%) were still lit at death, and 25 (13%) were lit at death with no other detection found; of 124 caught, 65 (52%), 34 (27%) and 20 (16%). Radar seldom found these ships first: of the 39 died ships still lit at death, 36 were already detected just before the radar reached them.

**Numbers:** 1074 destroyer smokes (387 Top 6, 687 Rest). Baseline: died 194 ships, 18.2 [15.0 to 22.5] per 100 (smoker 12.8 [9.8 to 17.0]; cruisers 8.7 [6.5 to 11.4] per 100 sheltering); caught 124, 11.6 [9.4 to 14.7] per 100 (smoker 6.4 [4.5 to 9.4]; cruisers 8.2 [5.9 to 10.7] per 100 sheltering). "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them.

Table 1. Conditions: deaths per 100 destroyer smokes with the condition and without it (difference, 95% interval; * = clear).
| condition | n with / without | died: with / without | died: difference | caught: with / without | caught: difference | with it, Top 6 / Rest (n): died | with it, Top 6 / Rest: caught |
|---|---|---|---|---|---|---|---|
| 50+ behind at activation | 277 / 797 | 34.9 / 12.4 | +22.5 (+15.2 to +30.5 *) | 23.1 / 7.5 | +15.6 (+8.7 to +22.4 *) | 35.6 / 34.7 (59 / 218) | 23.7 / 22.9 |
| team outnumbered at activation | 198 / 876 | 39.3 / 13.4 | +25.9 (+17.6 to +34.3 *) | 27.3 / 8.0 | +19.3 (+11.5 to +26.8 *) | 40.0 / 39.1 (45 / 153) | 26.7 / 27.4 |
| a covered ship was radar-lit while the smoke stood | 388 / 686 | 27.1 / 13.1 | +13.9 (+8.8 to +18.9 *) | 20.9 / 6.3 | +14.6 (+9.3 to +20.5 *) | 22.1 / 30.1 (149 / 239) | 12.1 / 26.4 |
| a covered ship was seen by an enemy ship (surface lit) | 512 / 562 | 27.1 / 10.0 | +17.1 (+12.4 to +23.2 *) | 19.1 / 4.6 | +14.5 (+10.9 to +19.1 *) | 17.3 / 32.7 (185 / 327) | 11.3 / 23.6 |
| a covered ship was lit for firing from smoke | 203 / 871 | 28.4 / 15.8 | +12.5 (+6.7 to +18.7 *) | 25.1 / 8.4 | +16.7 (+9.9 to +25.2 *) | 20.7 / 33.6 (82 / 121) | 14.6 / 32.2 |

Table 2. The same conditions, split by who is lost: the smoker (per 100 smokes) and sheltering cruisers (per 100 sheltering cruisers; n = cruisers).
| condition | smoker died: with / without (difference) | smoker caught: with / without (difference) | cruisers died: with (n) / without (n) (difference) | cruisers caught: with (n) / without (n) (difference) |
|---|---|---|---|---|
| 50+ behind at activation | 25.8 / 8.2 (+17.6 (+11.8 to +24.4 *)) | 14.1 / 3.8 (+10.3 (+5.3 to +16.0 *)) | 18.0 (111) / 6.5 (473) (+11.5 (+4.3 to +19.0 *)) | 17.0 (112) / 6.1 (475) (+10.9 (+4.3 to +16.6 *)) |
| team outnumbered at activation | 28.1 / 9.3 (+18.8 (+10.8 to +27.0 *)) | 16.7 / 4.1 (+12.6 (+5.9 to +19.7 *)) | 27.4 (73) / 6.1 (511) (+21.3 (+12.5 to +29.8 *)) | 24.3 (74) / 5.8 (513) (+18.5 (+9.1 to +26.9 *)) |
| a covered ship was radar-lit while the smoke stood | 18.0 / 9.7 (+8.3 (+4.3 to +12.0 *)) | 11.1 / 3.8 (+7.3 (+3.8 to +11.7 *)) | 12.1 (264) / 5.9 (320) (+6.2 (+1.8 to +10.7 *)) | 12.9 (264) / 4.3 (323) (+8.5 (+3.6 to +13.8 *)) |
| a covered ship was seen by an enemy ship (surface lit) | 18.3 / 7.7 (+10.6 (+6.5 to +15.7 *)) | 10.2 / 3.0 (+7.1 (+3.8 to +11.1 *)) | 12.1 (331) / 4.3 (253) (+7.7 (+3.2 to +13.0 *)) | 12.3 (332) / 2.8 (255) (+9.6 (+5.2 to +14.5 *)) |
| a covered ship was lit for firing from smoke | 14.4 / 12.4 (+2.1 (-2.4 to +6.3)) | 9.8 / 5.6 (+4.2 (-0.1 to +9.8)) | 14.1 (163) / 6.7 (421) (+7.5 (+2.1 to +14.1 *)) | 15.8 (164) / 5.2 (423) (+10.7 (+5.2 to +17.9 *)) |

Definitions: "outnumbered" = fewer of our ships alive than theirs at activation. "Radar-lit" = a covered ship (the smoker or a ship inside or behind) carried the radar flag at some time while the smoke stood, from the radar log. "Seen by an enemy ship" and "lit for firing" = a covered ship has that detection kind recorded while this smoke concealed it.

Calm smokes (not 50+ behind and no covered ship radar-lit): 513 smokes (203 Top 6, 310 Rest). Died 45 ships, 8.9 [6.7 to 12.0] per 100 (smoker 5.7 [3.5 to 8.5]); caught 19, 3.7 [2.2 to 5.7] per 100 (smoker 1.8 [0.6 to 3.2]). The other 561 smokes: died 26.7, caught 18.7 per 100 (calm minus other: died -17.8 (-22.5 to -13.4 *), caught -15.0 (-19.2 to -11.2 *)).

Table 3. Calm smokes, Top 6 against Rest.
| measure | Top 6 (n) | Rest (n) | Top 6 minus Rest |
|---|---|---|---|
| died per 100 | 5.4 (203) | 11.2 (305) | -5.7 (-10.9 to -1.9 *) |
| caught per 100 | 2.5 (203) | 4.5 (310) | -2.0 (-5.1 to +0.9) |
| smoker died per 100 | 3.0 (203) | 7.5 (305) | -4.6 (-9.5 to -0.8 *) |
| smoker caught per 100 | 0.5 (203) | 2.6 (310) | -2.1 (-4.2 to -0.3 *) |
| cruisers died per 100 sheltering | 3.8 (132) | 6.6 (136) | -2.8 (-7.2 to +1.9) |
| cruisers caught per 100 sheltering | 3.0 (132) | 3.6 (138) | -0.6 (-4.9 to +3.5) |

Table 4. By map.
|  | n (Top 6 / Rest) | died per 100 [95%] | died: Top 6 / Rest | died: Top 6 minus Rest | caught per 100 [95%] | caught: Top 6 / Rest | caught: Top 6 minus Rest | smoker died / caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | 238 (110 / 128) | 15.1 [10.9 to 22.0] | 10.9 / 18.8 | -7.8 (-19.7 to +1.8) | 11.8 [8.0 to 18.4] | 6.4 / 16.4 | -10.0 (-20.0 to -2.1 *) | 10.5 / 7.1 |  |
| Hotspot | 235 (80 / 155) | 15.7 [11.3 to 21.1] | 13.8 / 16.8 | -3.0 (-12.8 to +7.9) | 7.7 [5.2 to 10.1] | 7.5 / 7.7 | -0.2 (-6.5 to +6.3) | 9.4 / 3.4 |  |
| Loop | 142 (41 / 101) | 18.3 [11.4 to 27.0] | 17.1 / 18.8 | -1.7 (-20.8 to +14.5) | 10.6 [5.3 to 17.1] | 9.8 / 10.9 | -1.1 (-15.0 to +10.7) | 14.1 / 6.3 |  |
| Mountain Range | 132 (55 / 77) | 18.4 [9.7 to 29.3] | 16.4 / 20.0 | -3.6 (-22.6 to +17.4) | 8.3 [3.4 to 14.7] | 7.3 / 9.1 | -1.8 (-12.5 to +10.7) | 14.4 / 3.8 |  |
| Land of Fire | 128 (48 / 80) | 21.1 [11.1 to 37.9] | 8.3 / 28.8 | -20.4 (-46.7 to +1.4) | 14.1 [6.9 to 25.8] | 4.2 / 20.0 | -15.8 (-34.3 to -2.2 *) | 15.6 / 7.8 |  |
| Sea of Fortune | 117 (38 / 79) | 17.9 [11.4 to 27.3] | 13.2 / 20.2 | -7.1 (-23.6 to +4.9) | 13.7 [7.7 to 21.9] | 7.9 / 16.5 | -8.6 (-22.5 to +3.0) | 12.8 / 8.6 |  |
| Okinawa | 82 (15 / 67) | 29.3 [22.1 to 38.5] | 26.7 / 29.9 | -3.2 (-26.2 to +20.1) | 21.9 [12.8 to 31.5] | 20.0 / 22.4 | -2.4 (-20.0 to +23.1) | 19.5 / 12.2 |  |

Table 5. By time of activation (replay clock).
|  | n (Top 6 / Rest) | died per 100 [95%] | died: Top 6 / Rest | died: Top 6 minus Rest | caught per 100 [95%] | caught: Top 6 / Rest | caught: Top 6 minus Rest | smoker died / caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| 0-5 min | 308 (104 / 204) | 8.5 [5.3 to 12.3] | 5.8 / 9.9 | -4.1 (-11.1 to +1.3) | 7.5 [4.7 to 11.2] | 2.9 / 9.8 | -6.9 (-12.9 to -2.0 *) | 5.6 / 3.6 |  |
| 5-10 min | 494 (179 / 315) | 21.8 [16.2 to 28.5] | 12.8 / 27.0 | -14.2 (-25.7 to -4.1 *) | 12.6 [9.1 to 16.9] | 8.4 / 14.9 | -6.5 (-13.6 to -0.1 *) | 15.5 / 7.5 |  |
| 10-15 min | 246 (97 / 149) | 22.4 [17.6 to 27.3] | 21.6 / 23.0 | -1.3 (-13.3 to +7.6) | 14.2 [9.5 to 19.1] | 9.3 / 17.4 | -8.2 (-17.4 to +0.8) | 15.9 / 7.7 |  |
| 15+ min | 26 (7 / 19) | 23.1 [7.4 to 42.3] | too few / 21.1 | too few | 15.4 [3.7 to 30.0] | too few / 10.5 | too few | 15.4 / 7.7 |  |

Table 6. By score at activation.
|  | n (Top 6 / Rest) | died per 100 [95%] | died: Top 6 / Rest | died: Top 6 minus Rest | caught per 100 [95%] | caught: Top 6 / Rest | caught: Top 6 minus Rest | smoker died / caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| ahead 50+ | 372 (167 / 205) | 12.9 [9.4 to 17.8] | 10.8 / 14.7 | -3.9 (-12.5 to +4.2) | 6.5 [4.4 to 9.1] | 5.4 / 7.3 | -1.9 (-6.8 to +2.1) | 9.4 / 3.8 |  |
| level | 425 (161 / 264) | 11.9 [9.6 to 15.1] | 8.1 / 14.2 | -6.2 (-11.0 to -2.5 *) | 8.5 [6.3 to 11.3] | 3.7 / 11.4 | -7.6 (-11.7 to -4.3 *) | 7.1 / 3.8 |  |
| behind 50+ | 277 (59 / 218) | 34.9 [27.2 to 44.3] | 35.6 / 34.7 | +0.9 (-20.9 to +16.3) | 23.1 [17.1 to 30.0] | 23.7 / 22.9 | +0.8 (-14.8 to +13.6) | 25.8 / 14.1 |  |

Radar deaths. "Died" ships: 194 deaths (194 distinct ships). "Caught" ships: 124 death records (124 distinct ships). Radar-lit comes from the radar log for that ship. (a) a radar-lit span touches its last 40 s. (b) a radar-lit span covers the moment of death, give or take 2 s. (c) as (b), and the hydro log does not have it lit at death, and no smoke record of that ship shows a first detection of another kind (seen by a ship, proximity, aircraft, lit for firing) in its last 20 s.

Table 7. Radar deaths three ways.
| metric | reading | deaths | smoker destroyer | sheltering cruiser | other | Top 6 | Rest | share, Top 6 minus Rest |
|---|---|---|---|---|---|---|---|---|
| died | (a) radar-lit at some time in its last 40 s | 85 of 194 (44%) | 65 of 136 | 18 of 51 | 2 of 7 | 21 of 52 (40%) | 64 of 142 (45%) | -4.7 (-24.2 to +8.2) |
| died | radar-lit at some time in its last 20 s (for comparison with round 5b) | 75 of 194 (39%) | 58 of 136 | 15 of 51 | 2 of 7 | 17 of 52 (33%) | 58 of 142 (41%) | -8.2 (-30.9 to +7.3) |
| died | (b) still radar-lit at death | 39 of 194 (20%) | 31 of 136 | 7 of 51 | 1 of 7 | 8 of 52 (15%) | 31 of 142 (22%) | -6.4 (-22.0 to +3.9) |
| died | (c) radar-lit at death, no other detection found | 25 of 194 (13%) | 21 of 136 | 4 of 51 | 0 of 7 | 5 of 52 (10%) | 20 of 142 (14%) | -4.5 (-14.8 to +3.2) |
| caught | (a) radar-lit at some time in its last 40 s | 65 of 124 (52%) | 41 of 69 | 22 of 48 | 2 of 7 | 10 of 29 (34%) | 55 of 95 (58%) | -23.4 (-43.3 to -4.9 *) |
| caught | radar-lit at some time in its last 20 s (for comparison with round 5b) | 57 of 124 (46%) | 36 of 69 | 19 of 48 | 2 of 7 | 8 of 29 (28%) | 49 of 95 (52%) | -24.0 (-50.1 to -3.1 *) |
| caught | (b) still radar-lit at death | 34 of 124 (27%) | 22 of 69 | 11 of 48 | 1 of 7 | 1 of 29 (3%) | 33 of 95 (35%) | -31.3 (-43.0 to -19.5 *) |
| caught | (c) radar-lit at death, no other detection found | 20 of 124 (16%) | 16 of 69 | 4 of 48 | 0 of 7 | 0 of 29 (0%) | 20 of 95 (21%) | -21.1 (-29.8 to -12.4 *) |

- died: of the 39 still lit at death, 0 were also hydro-lit and 14 had another kind of detection start in the last 20 s ({'surface lit': 12, 'smoke fire penalty': 2}). The smoke record covers the whole last 20 s for 25, part of it for 14, none of it for 0. Cross-check from the ship's own track: at the last sample before that radar span began the ship was undetected in 3, already detected in 36 (unknown 0); 2 deaths are both (c) and undetected before the radar. Median time lit before death 12.4 s. Radar ships: {'Moskva': 15, 'Brisbane': 8, 'San Martín': 5, 'Des Moines': 4, 'Yueyang': 2, 'Gdańsk': 1}.
- caught: of the 34 still lit at death, 1 were also hydro-lit and 13 had another kind of detection start in the last 20 s ({'surface lit': 10, 'smoke fire penalty': 3}). The smoke record covers the whole last 20 s for 22, part of it for 11, none of it for 1. Cross-check from the ship's own track: at the last sample before that radar span began the ship was undetected in 1, already detected in 33 (unknown 0); 0 deaths are both (c) and undetected before the radar. Median time lit before death 13.55 s. Radar ships: {'Moskva': 17, 'Brisbane': 5, 'San Martín': 3, 'Des Moines': 3, 'Gdańsk': 1, 'Småland': 1}.
- Clans, (b) still lit at death, died: Top 6: RESIN 4, BONKZ 3, VRTUS 1 | Rest: EPOXY 5, KITED 3, HFANS 3, REEEE 3, BTLST 2, UYSC 2, -BN- 2, RSR 2, MANBA 1, KM 1, SCCC2 1, 5D 1, KSE 1, INCA 1, MACH 1, MZY 1, PFANS 1.

**Top 6 or Shared:** Shared pattern, Rest pays more. The conditions raise deaths in both groups (Table 1, last columns). Calm smokes: Top 6 minus Rest died -5.7 (-10.9 to -1.9 *), caught -2.0 (-5.1 to +0.9). Share of died ships radar-lit in the last 40 s: Top 6 40%, Rest 45% (-4.7 (-24.2 to +8.2)); still lit at death: 15% vs 22% (-6.4 (-22.0 to +3.9)). On caught ships the Rest share is clearly higher: last 40 s 34% vs 58% (-23.4 (-43.3 to -4.9 *)), still lit at death 1 of 29 vs 33 of 95 (-31.3 (-43.0 to -19.5 *)). The two metrics disagree here, so treat the group gap in radar deaths as a lead.

**Clans:** highest map on "died" is Okinawa (29.3 per 100); smokes with a death there: Top 6: KITE 2, BONKZ 1, HTDOG 1 | Rest: EPOXY 2, -BN- 2, REEEE 2, HFANS 2, BTLST 1, 5D 1, OGF 1, PN 1, RSR 1, KSE 1, KM 1, NGA 1, MACHX 1, MZY 1.

**Could not be done / proxy:** Reading (c) is a floor on other detection, not a full check. The batch keeps, per ship and per smoke, only the first moment of each detection kind while that smoke concealed it; it has no second-by-second list of who saw the ship. So (c) removes deaths where another kind of detection started in the last 20 s, or hydro had the ship, but it cannot see a ship that an enemy had been watching for longer, or one that died after the smoke record ended (the record misses the last 20 s entirely for 0 of the 39 died ships lit at death and 1 of the 34 caught). The track cross-check (undetected just before the radar arrived) is the closest proxy for "radar is what found it". Read (c) as an upper limit on deaths owed to radar alone.

**Verdict:** Keep (conditions, calm smokes, radar readings (a) and (b)). Lead for (c).

**Changed from round 5b:** the "round 5b" column is `round5b/part-a/out-a2.json` (round 5 with the clock fix), or the round 5b redo N2 where the row says so.

| number | round 5b | round 5c | why |
|---|---|---|---|
| deaths in destroyer smokes: died (round 5b N1 counted 201 ships at risk in the smoke window) | 201 | 194 | new death metric: exactly 20 s after dispersal, each ship once, 9 smokes left out |
| 50+ behind at activation: deaths per 100 with / without, now died | 23.1 / 7.5 | 34.9 / 12.4 | new death metric |
| team outnumbered at activation: deaths per 100 with / without, now died | 27.3 / 8.0 | 39.3 / 13.4 | new death metric |
| a covered ship was seen by an enemy ship (surface lit): deaths per 100 with / without, now died | 19.1 / 4.6 | 27.1 / 10.0 | new death metric |
| a covered ship was lit for firing from smoke: deaths per 100 with / without, now died | 25.1 / 8.4 | 28.4 / 15.8 | new death metric |
| radar-lit covered ship: deaths per 100 with / without, now died | 20.9 / 6.3 | 27.1 / 13.1 | new death metric |
| calm smokes: n (round 5b N2) | 515 | 513 | lit_covered from the round 5c library in place of the radar test in the round 5b script; 2 smokes differ |
| calm smokes: deaths per 100, now died | 3.7 | 8.9 | new death metric |
| Sleeping Giant: deaths per 100, now died | 11.8 | 15.1 | new death metric |
| Hotspot: deaths per 100, now died | 7.7 | 15.7 | new death metric |
| Loop: deaths per 100, now died | 10.6 | 18.3 | new death metric |
| Mountain Range: deaths per 100, now died | 8.3 | 18.4 | new death metric |
| Land of Fire: deaths per 100, now died | 14.1 | 21.1 | new death metric |
| Sea of Fortune: deaths per 100, now died | 13.7 | 17.9 | new death metric |
| Okinawa: deaths per 100, now died | 22.0 | 29.3 | new death metric |
| ahead 50+: deaths per 100, now died | 6.5 | 12.9 | new death metric |
| level: deaths per 100, now died | 8.5 | 11.9 | new death metric |
| behind 50+: deaths per 100, now died | 23.1 | 34.9 | new death metric |
| 0-5 min: n | 306 | 308 | time from the replay clock (e0), not the HUD clock |
| 0-5 min: deaths per 100, now died | 7.5 | 8.5 | new death metric |
| 5-10 min: n | 495 | 494 | time from the replay clock (e0), not the HUD clock |
| 5-10 min: deaths per 100, now died | 12.5 | 21.8 | new death metric |
| 10-15 min: n | 247 | 246 | time from the replay clock (e0), not the HUD clock |
| 10-15 min: deaths per 100, now died | 14.2 | 22.4 | new death metric |
| 15+ min: deaths per 100, now died | 15.4 | 23.1 | new death metric |
| caught deaths radar-lit in the last 20 s (round 5b N2: 56 of 124) | 56 | 57 | same radar log; one death sits on the 20 s edge (which rule moved it was not traced) |
| died ships radar-lit in the last 40 s | - | 85 of 194 | new death metric |
| still radar-lit at death (died / caught) | - | 39 of 194 / 34 of 124 | new reading |
| radar-lit at death, no other detection found (died / caught) | - | 25 of 194 / 20 of 124 | new reading |

29 other compared numbers are unchanged (caught per 100 is the same list as round 5 deaths wherever the smokes in the row are the same).


### A3. Somers vs Gearing inside Top 6 and inside Rest

**Answer:** Inside the Top 6 the two ships lose about the same: died 17.8 (Somers) vs 16.2 (Gearing) per 100, caught 7.8 vs 9.5. Inside the Rest the Gearing loses more: died 19.4 vs 32.3 (gap -12.9 (-24.5 to -0.4 *)), caught 11.8 vs 23.6 (gap -11.8 (-23.7 to -2.1 *)). Both metrics agree (caught: clear; died: clear), and the extra loss is the smoker itself, not the sheltering cruisers (smoker died -12.6 (-28.4 to +0.2), cruisers died +0.5 (-7.0 to +11.5)). The gap goes with who sails the Gearing, not with the ship.

**Numbers:** 260 Somers smokes (90 Top 6, 170 Rest) and 180 Gearing smokes (74 Top 6, 106 Rest). "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them. Smoker rates are per 100 smokes; cruiser rates are per 100 sheltering cruisers (n = cruisers).

Table 1. Deaths per 100 by ship and group [95% interval].
| group | ship | n | died: all | caught: all | died: smoker | caught: smoker | died: cruisers (n) | caught: cruisers (n) | note |
|---|---|---|---|---|---|---|---|---|---|
| All | Somers | 260 | 18.9 [12.5 to 25.4] | 10.4 [7.0 to 13.4] | 10.4 [6.2 to 15.2] | 3.9 [1.9 to 6.2] | 9.4 [5.2 to 13.9] (234) | 7.3 [4.2 to 10.3] (234) |  |
| All | Gearing | 180 | 25.4 [18.1 to 35.5] | 17.8 [11.5 to 27.0] | 16.8 [8.8 to 30.5] | 8.3 [2.2 to 20.0] | 8.2 [3.6 to 12.1] (146) | 9.4 [4.5 to 13.9] (149) |  |
| Top 6 | Somers | 90 | 17.8 [2.5 to 30.0] | 7.8 [2.5 to 12.4] | 10.0 [0.0 to 20.3] | 2.2 [0.0 to 5.4] | 8.2 [0.0 to 14.9] (85) | 5.9 [0.0 to 9.9] (85) |  |
| Top 6 | Gearing | 74 | 16.2 [11.1 to 22.6] | 9.5 [5.7 to 10.7] | 8.1 [3.7 to 21.4] | 1.4 [0.0 to 7.1] | 6.8 [0.0 to 8.7] (73) | 6.8 [0.0 to 8.7] (73) |  |
| Rest | Somers | 170 | 19.4 [14.7 to 26.2] | 11.8 [7.7 to 15.6] | 10.6 [6.5 to 16.4] | 4.7 [2.1 to 7.8] | 10.1 [5.1 to 15.9] (149) | 8.1 [4.3 to 12.1] (149) |  |
| Rest | Gearing | 106 | 32.3 [21.3 to 45.5] | 23.6 [13.8 to 36.6] | 23.2 [10.5 to 40.8] | 13.2 [3.0 to 30.9] | 9.6 [0.0 to 14.8] (73) | 11.8 [2.9 to 17.1] (76) |  |

Table 2. Somers minus Gearing inside each group (difference, 95% interval; * = clear).
| group | n Somers / Gearing | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 | cruisers died per 100 sheltering | cruisers caught per 100 sheltering |
|---|---|---|---|---|---|---|---|
| All | 260 / 180 | -6.6 (-18.4 to +3.5) | -7.4 (-16.6 to -0.1 *) | -6.4 (-19.6 to +3.3) | -4.5 (-16.0 to +2.4) | +1.2 (-4.2 to +7.8) | -2.1 (-7.2 to +3.4) |
| Top 6 | 90 / 74 | +1.6 (-18.2 to +17.4) | -1.7 (-6.7 to +4.9) | +1.9 (-19.9 to +14.5) | +0.9 (-7.6 to +5.6) | +1.4 (-7.2 to +10.8) | -1.0 (-7.2 to +7.3) |
| Rest | 170 / 106 | -12.9 (-24.5 to -0.4 *) | -11.8 (-23.7 to -2.1 *) | -12.6 (-28.4 to +0.2) | -8.5 (-23.8 to +1.6) | +0.5 (-7.0 to +11.5) | -3.8 (-10.4 to +7.0) |

Table 3. Top 6 minus Rest on each ship (difference, 95% interval; * = clear).
| ship | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 | cruisers died per 100 sheltering | cruisers caught per 100 sheltering |
|---|---|---|---|---|---|---|
| Somers | -1.6 (-19.1 to +11.8) | -4.0 (-10.7 to +2.1) | -0.6 (-12.2 to +9.4) | -2.5 (-6.2 to +1.9) | -1.8 (-12.2 to +6.8) | -2.2 (-9.2 to +3.4) |
| Gearing | -16.1 (-30.4 to -3.6 *) | -14.1 (-26.6 to -4.8 *) | -15.1 (-32.1 to +1.8) | -11.9 (-27.3 to -1.0 *) | -2.7 (-10.5 to +5.4) | -5.0 (-12.1 to +3.4) |

Rest Gearing, leaving one clan out at a time: died per 100 stays between 28.9 and 34.8, caught between 19.6 and 26.1. By clan (n smokes, died, caught): KSC 29/7/6, -BN- 18/3/2, BTLST 11/4/4, 5D 9/6/6, OGF 9/6/3, RSR 9/3/2, INCA 7/0/0, HFANS 5/1/0, RMN 3/1/1, EPOXY 3/0/0, KM 2/0/0, UYSC 1/1/1.

**Top 6 or Shared:** Top 6. On the Gearing, Top 6 minus Rest is died -16.1 (-30.4 to -3.6 *) and caught -14.1 (-26.6 to -4.8 *); on the Somers it is died -1.6 (-19.1 to +11.8) and caught -4.0 (-10.7 to +2.1). The Rest lose more ships around their Gearing smokes; the Somers numbers are close in both groups.

**Clans:** Somers: Top 6: RESIN 38, H-SR 33, BONKZ 12, VRTUS 7 | Rest: HFANS 28, REEEE 25, MZY 22, EPOXY 18, MACHX 17, BONKY 14, -BN- 12, NGA 11, PFANS 8, PN 5, UYSC 5, KITED 3, RSR 1, INCA 1. Gearing: Top 6: BONKZ 37, KITE 23, VRTUS 10, HTDOG 4 | Rest: KSC 29, -BN- 18, BTLST 11, 5D 9, OGF 9, RSR 9, INCA 7, HFANS 5, RMN 3, EPOXY 3, KM 2, UYSC 1.

**Verdict:** Keep.

**Changed from round 5b:** round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a3.json`).

| number | round 5b | round 5c | why |
|---|---|---|---|
| Top 6, Somers, all ships: deaths per 100, now died | 7.8 | 17.8 | new death metric |
| Top 6, Gearing, all ships: deaths per 100, now died | 9.5 | 16.2 | new death metric |
| Top 6, all ships: Somers minus Gearing, now caught | -1.7 (-6.9 to +4.7) | -1.7 (-6.7 to +4.9) | same list; interval now from diff_ci |
| Top 6, all ships: Somers minus Gearing, now died | -1.7 (-6.9 to +4.7) | +1.6 (-18.2 to +17.4) | new death metric |
| Top 6, Somers, smoker: deaths per 100, now died | 2.2 | 10.0 | new death metric |
| Top 6, Gearing, smoker: deaths per 100, now died | 1.4 | 8.1 | new death metric |
| Top 6, smoker: Somers minus Gearing, now caught | +0.9 (-7.7 to +5.7) | +0.9 (-7.6 to +5.6) | same list; interval now from diff_ci |
| Top 6, smoker: Somers minus Gearing, now died | +0.9 (-7.7 to +5.7) | +1.9 (-19.9 to +14.5) | new death metric |
| Top 6, Somers, sheltering cruisers: deaths per 100, now died | 5.9 | 8.2 | new death metric |
| Top 6, sheltering cruisers: Somers minus Gearing, now caught | -1.0 (-7.1 to +7.0) | -1.0 (-7.2 to +7.3) | same list; interval now from diff_ci |
| Top 6, sheltering cruisers: Somers minus Gearing, now died | -1.0 (-7.1 to +7.0) | +1.4 (-7.2 to +10.8) | new death metric |
| Rest, Somers, all ships: deaths per 100, now died | 11.8 | 19.4 | new death metric |
| Rest, Gearing, all ships: deaths per 100, now died | 23.6 | 32.3 | new death metric |
| Rest, all ships: Somers minus Gearing, now caught | -11.8 (-24.0 to -1.5) | -11.8 (-23.7 to -2.1) | same list; interval now from diff_ci |
| Rest, all ships: Somers minus Gearing, now died | -11.8 (-24.0 to -1.5) | -12.9 (-24.5 to -0.4) | new death metric |
| Rest, Somers, smoker: deaths per 100, now died | 4.7 | 10.6 | new death metric |
| Rest, Gearing, smoker: deaths per 100, now died | 13.2 | 23.2 | new death metric |
| Rest, smoker: Somers minus Gearing, now caught | -8.5 (-25.3 to +1.6) | -8.5 (-23.8 to +1.6) | same list; interval now from diff_ci |
| Rest, smoker: Somers minus Gearing, now died | -8.5 (-25.3 to +1.6) | -12.6 (-28.4 to +0.2) | new death metric |
| Rest, Somers, sheltering cruisers: deaths per 100, now died | 8.1 | 10.1 | new death metric |
| Rest, Gearing, sheltering cruisers: deaths per 100, now died | 11.8 | 9.6 | new death metric |
| Rest, sheltering cruisers: Somers minus Gearing, now caught | -3.8 (-10.4 to +6.5) | -3.8 (-10.4 to +7.0) | same list; interval now from diff_ci |
| Rest, sheltering cruisers: Somers minus Gearing, now died | -3.8 (-10.4 to +6.5) | +0.5 (-7.0 to +11.5) | new death metric |

13 other compared numbers are unchanged (the caught rates).


### A4. Counter-smokes: death rates by angle and for the "what pays" rows

**Answer:** Counter-smokes are costly on both metrics: 24.8 died and 15.0 caught per 100, against 18.2 and 11.5 for all destroyer smokes. By angle, flanking counter-smokes lost 50.0 died / 25.0 caught per 100 against 24.0 / 15.0 head-on; the flanking minus head-on gap is +26.0 (-5.0 to +63.3) on died and +10.0 (-15.4 to +41.1) on caught, so over all clans angle does not clearly separate deaths. Inside the Rest the gap on died is +42.0 (+6.7 to +78.8 *) (clear; only 9 flanking smokes) and on caught +17.9 (-17.3 to +53.0). Of the "what pays" rows, Gearing and flank-smoke-line counter-smokes returned the most damage and also the most deaths (Gearing 45.0 died / 35.0 caught per 100).

**Numbers:** 133 destroyer counter-smokes matched to the enemy smoke they answer (44 Top 6, 89 Rest); 132 have a usable line of fire. "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them. Here that removes 0 smoke(s). Geometry and damage columns are computed as in round 5; the delay after the enemy smoke now uses the replay clock, which moves 6 smoke(s) to another delay band.

Table 1. By angle off the enemy smoke's line of fire.
|  | n (Top 6 / Rest) | concealed damage [95%] | out-damaged answered % | answered smoke damage | margin [95%] | died per 100 [95%] | caught per 100 [95%] | smoker died / caught per 100 | died: Top 6 / Rest (gap) | caught: Top 6 / Rest (gap) | note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| head-on (under 30) | 100 (35 / 65) | 8,947 [5,933 to 12,413] | 42.0 | 8,495 | +452 [-3,039 to +3,635] | 24.0 [16.4 to 34.5] | 15.0 [9.1 to 23.5] | 16.0 / 7.0 | 22.9 / 24.6 (-18.1 to +15.7) | 14.3 / 15.4 (-15.4 to +16.9) |  |
| oblique (30-60) | 20 (6 / 14) | 6,762 [3,330 to 10,424] | 30.0 | 12,781 | -6,019 [-14,290 to +1,287] | 15.0 [0.0 to 30.0] | 10.0 [0.0 to 23.8] | 10.0 / 5.0 | too few / 21.4 (-) | too few / 14.3 (-) |  |
| flanking (over 60) | 12 (3 / 9) | 2,868 [747 to 6,438] | 16.7 | 5,796 | -2,928 [-7,279 to +1,887] | 50.0 [23.5 to 88.9] | 25.0 [0.0 to 50.0] | 41.7 / 16.7 | too few / 66.7 (-) | too few / 33.3 (-) | small n |

Table 2. Flanking minus head-on (difference, 95% interval; * = clear).
| group | n flanking / head-on | concealed damage | margin | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 | note |
|---|---|---|---|---|---|---|---|---|
| All | 12 / 100 | -6,079 (-10,222 to -562 *) | -3,380 (-8,917 to +2,950) | +26.0 (-5.0 to +63.3) | +10.0 (-15.4 to +41.1) | +25.7 (-3.9 to +59.5) | +9.7 (-9.5 to +30.6) | small n |
| Top 6 | 3 / 35 | too few | too few | too few | too few | too few | too few | too few |
| Rest | 9 / 65 | -4,026 (-9,251 to +2,381) | -1,637 (-7,589 to +5,803) | +42.0 (+6.7 to +78.8 *) | +17.9 (-17.3 to +53.0) | +38.6 (+6.8 to +76.5 *) | +14.5 (-11.1 to +43.0) | small n |

Table 3. The "what pays" rows.
|  | n (Top 6 / Rest) | concealed damage [95%] | out-damaged answered % | answered smoke damage | margin [95%] | died per 100 [95%] | caught per 100 [95%] | smoker died / caught per 100 | died: Top 6 / Rest (gap) | caught: Top 6 / Rest (gap) | note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| radar cruiser inside | 32 (15 / 17) | 18,316 [12,796 to 24,231] | 59.4 | 9,814 | +8,502 [+3,083 to +15,949] | 28.1 [15.6 to 45.8] | 18.8 [7.1 to 36.8] | 12.5 / 3.1 | 26.7 / 29.4 (-31.2 to +45.8) | 20.0 / 17.6 (-23.2 to +56.7) |  |
| Gearing | 20 (11 / 9) | 21,202 [14,133 to 27,738] | 60.0 | 8,329 | +12,873 [+7,286 to +18,694] | 45.0 [21.4 to 84.6] | 35.0 [14.8 to 72.7] | 20.0 / 10.0 | 18.2 / 77.8 (-90.9 to -24.7 *) | 9.1 / 66.7 (-80.9 to -30.4 *) |  |
| flank-smoke-line ships | 52 (19 / 33) | 13,696 [8,684 to 18,162] | 46.1 | 9,285 | +4,411 [-107 to +9,258] | 32.7 [20.0 to 52.2] | 23.1 [12.0 to 39.1] | 15.4 / 5.8 | 26.3 / 36.4 (-39.5 to +26.6) | 15.8 / 27.3 (-35.7 to +21.2) |  |
| laid 11-25 s after the enemy smoke | 43 (15 / 28) | 10,922 [6,475 to 15,826] | 41.9 | 11,257 | -335 [-7,449 to +5,091] | 25.6 [13.6 to 42.4] | 20.9 [9.3 to 36.2] | 13.9 / 9.3 | 13.3 / 32.1 (-47.6 to +29.2) | 13.3 / 25.0 (-36.4 to +36.3) |  |
| 6-9 km from the answered smoke | 51 (17 / 34) | 9,740 [4,696 to 15,479] | 39.2 | 9,357 | +383 [-3,868 to +4,770] | 29.4 [14.8 to 47.7] | 19.6 [8.8 to 35.1] | 19.6 / 9.8 | 41.2 / 23.5 (-14.3 to +60.0) | 23.5 / 17.6 (-20.8 to +51.1) |  |
| answered smoke within 30 degrees of straight ahead | 65 (22 / 43) | 9,023 [5,725 to 12,308] | 43.1 | 7,432 | +1,592 [-2,145 to +5,334] | 24.6 [13.2 to 39.2] | 16.9 [7.3 to 29.8] | 12.3 / 4.6 | 22.7 / 25.6 (-28.2 to +24.3) | 18.2 / 16.3 (-18.9 to +31.8) |  |
| all counter-smokes | 133 (44 / 89) | 8,003 [5,499 to 10,381] | 37.6 | 8,832 | -830 [-3,565 to +1,548] | 24.8 [17.4 to 34.8] | 15.0 [9.9 to 22.1] | 17.3 / 7.5 | 18.2 / 28.1 (-24.5 to +5.3) | 11.4 / 16.9 (-16.9 to +8.5) |  |
| all, Top 6 | 44 (44 / 0) | 11,140 [7,212 to 14,552] | 43.2 | 12,184 | -1,044 [-6,108 to +1,940] | 18.2 [8.3 to 29.0] | 11.4 [4.2 to 25.0] | 11.4 / 4.5 | 18.2 / too few (-) | 11.4 / too few (-) |  |
| all, Rest | 89 (0 / 89) | 6,452 [3,959 to 9,194] | 34.8 | 7,175 | -724 [-4,322 to +2,568] | 28.1 [19.5 to 41.2] | 16.9 [10.6 to 26.0] | 20.2 / 9.0 | too few / 28.1 (-) | too few / 16.9 (-) |  |

Table 4. Each "what pays" row minus the other counter-smokes (difference, 95% interval; * = clear).
|  | concealed damage | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 |
|---|---|---|---|---|---|
| radar cruiser inside | +13,581 (+7,799 to +19,231 *) | +4.4 (-13.1 to +23.9) | +4.9 (-11.1 to +23.8) | -6.3 (-18.3 to +7.0) | -5.8 (-13.0 to +3.5) |
| Gearing | +15,536 (+4,982 to +22,170 *) | +23.8 (-3.0 to +69.9) | +23.5 (+1.0 to +63.6 *) | +3.2 (-12.9 to +32.7) | +2.9 (-8.7 to +28.9) |
| flank-smoke-line ships | +9,348 (+3,944 to +13,751 *) | +12.9 (-3.8 to +32.6) | +13.2 (+0.2 to +27.9 *) | -3.1 (-16.0 to +11.0) | -2.9 (-10.1 to +5.8) |
| laid 11-25 s after the enemy smoke | +4,314 (-502 to +8,533) | +1.1 (-13.2 to +21.3) | +8.7 (-2.9 to +26.4) | -4.9 (-18.5 to +11.1) | +2.6 (-6.9 to +15.5) |
| 6-9 km from the answered smoke | +2,818 (-2,392 to +8,362) | +7.5 (-12.4 to +26.4) | +7.4 (-6.7 to +23.4) | +3.8 (-11.7 to +18.4) | +3.7 (-5.1 to +15.2) |
| answered smoke within 30 degrees of straight ahead | +1,996 (-1,978 to +6,485) | -0.4 (-16.7 to +16.1) | +3.7 (-9.7 to +17.7) | -9.8 (-22.7 to +1.9) | -5.7 (-14.9 to +3.6) |

**Top 6 or Shared:** All counter-smokes, Top 6 against Rest: died 18.2 vs 28.1 (-9.9 (-24.5 to +5.3)), caught 11.4 vs 16.9 (-5.5 (-16.9 to +8.5)). Flanking minus head-on inside the Top 6: died too few; inside the Rest: died +42.0 (+6.7 to +78.8 *). Gearing counter-smokes: Top 6 18.2 died / 9.1 caught per 100 against Rest 77.8 / 66.7 (gaps -90.9 to -24.7 * and -80.9 to -30.4 *; n 11 and 9, small). The deaths that go with the high-damage rows are mostly the Rest's.

**Clans:** flanking counter-smokes: Top 6: KITE 2, RESIN 1 | Rest: HFANS 2, 5D 2, -BN- 1, BONKY 1, SCCC2 1, KSE 1, MACHX 1. Gearing counter-smokes: Top 6: BONKZ 8, KITE 3 | Rest: KSC 3, OGF 2, -BN- 2, BTLST 1, 5D 1.

**Could not be done / proxy:** Nothing missing. The line of fire is itself a proxy (where the enemy smoke's damage landed, or where our ships were when it hit nobody), as in round 5.

**Verdict:** Keep the "what pays" rows with both death columns; angle and deaths: Lead only.

**Changed from round 5b:** round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a4.json`).

| number | round 5b | round 5c | why |
|---|---|---|---|
| head-on (under 30): deaths per 100, now died | 15.0 | 24.0 | new death metric |
| head-on (under 30): smoker died per 100, now smoker died | 7.0 | 16.0 | new death metric |
| oblique (30-60): deaths per 100, now died | 10.0 | 15.0 | new death metric |
| oblique (30-60): smoker died per 100, now smoker died | 5.0 | 10.0 | new death metric |
| flanking (over 60): deaths per 100, now died | 25.0 | 50.0 | new death metric |
| flanking (over 60): smoker died per 100, now smoker died | 16.7 | 41.7 | new death metric |
| radar cruiser inside: deaths per 100, now died | 18.8 | 28.1 | new death metric |
| radar cruiser inside: smoker died per 100, now smoker died | 3.1 | 12.5 | new death metric |
| Gearing: deaths per 100, now died | 35.0 | 45.0 | new death metric |
| Gearing: smoker died per 100, now smoker died | 10.0 | 20.0 | new death metric |
| flank-smoke-line ships: deaths per 100, now died | 23.1 | 32.7 | new death metric |
| flank-smoke-line ships: smoker died per 100, now smoker died | 5.8 | 15.4 | new death metric |
| laid 11-25 s after the enemy smoke: concealed damage | 12,296 | 10,922 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: deaths per 100, now caught | 18.6 | 20.9 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: deaths per 100, now died | 18.6 | 25.6 | new death metric |
| laid 11-25 s after the enemy smoke: smoker died per 100, now smoker caught | 7.0 | 9.3 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: smoker died per 100, now smoker died | 7.0 | 13.9 | new death metric |
| 6-9 km from the answered smoke: deaths per 100, now died | 19.6 | 29.4 | new death metric |
| 6-9 km from the answered smoke: smoker died per 100, now smoker died | 9.8 | 19.6 | new death metric |
| answered smoke within 30 degrees of straight ahead: deaths per 100, now died | 16.9 | 24.6 | new death metric |
| answered smoke within 30 degrees of straight ahead: smoker died per 100, now smoker died | 4.6 | 12.3 | new death metric |
| all counter-smokes: deaths per 100, now died | 15.0 | 24.8 | new death metric |
| all counter-smokes: smoker died per 100, now smoker died | 7.5 | 17.3 | new death metric |
| flanking minus head-on, deaths per 100, now caught | +10.0 (-13.1 to +35.0) | +10.0 (-15.4 to +41.1) | same list; interval now from diff_ci |
| flanking minus head-on, deaths per 100, now died | +10.0 (-13.1 to +35.0) | +26.0 (-5.0 to +63.3) | new death metric |

37 other compared numbers are unchanged (n, concealed damage and the caught rates wherever the row holds the same smokes).

