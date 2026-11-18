# Part B: ship tendencies

Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Everything here is association, not cause.
Intervals are 95%, made by resampling whole clans (1,000 draws). "Clear" = the interval of a difference excludes zero.
n 8 to 14 = small n. Under 8 = "too few". Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS.
Scripts: `ships.py` (all numbers, writes `out.txt` and `ships.json`), `figures.py`, `show.py`. Trace of every number: `CHECK-B.md`.

---

### B1. Cap sitters table

**Answer:** Daring and Z-42 are the true cap sitters: about 43% of their smokes are inside a cap and they are mostly for the smoker alone. Gdansk is a different animal: it is inside a cap less often, covers a teammate more often and returns more than twice the concealed damage per smoke.

**Numbers:** distance = smoke edge to the edge of the contested cap (negative = inside). "For a teammate" = the smoke was stacked with another smoke or screened a teammate.

| Ship | n | Clans | Median distance to cap edge | % inside a cap | % for a teammate | Concealed damage per smoke |
|---|---|---|---|---|---|---|
| **Daring** | 200 | 20 | 671 m (-306 to 1,382) | 42.5 (32.8 to 51.6) | 43.5 (37.7 to 49.7) | 3,623 (2,852 to 4,325) |
| **Gdansk** | 118 | 16 | 1,544 m (631 to 2,398) | 26.3 (16.7 to 37.1) | 56.8 (47.9 to 68.5) | 8,205 (6,154 to 11,068) |
| Z-42 | 56 | 8 | 470 m (-858 to 4,055) | 42.9 (18.8 to 66.7) | 42.9 (24.5 to 64.1) | 4,126 (2,377 to 6,548) |
| Z-52 (small n) | 10 | 4 | 4,522 m (8 to 6,796) | 10.0 | 40.0 | 2,025 |
| Grozovoi | 30 | 8 | 998 m (-500 to 2,142) | 33.3 (21.1 to 61.5) | 53.3 (35.9 to 87.5) | 6,452 (2,998 to 13,916) |
| Shimakaze | 58 | 12 | 3,288 m (-119 to 4,869) | 32.8 (20.7 to 49.0) | 74.1 (62.9 to 84.4) | 5,609 (2,637 to 10,748) |

Daring minus Gdansk (the highlighted contrast):

| Measure | All | Top 6 (34 vs 60 smokes) | Rest (166 vs 58) |
|---|---|---|---|
| Median distance | -873 m (-2,158 to +258), not clear | -630 m (-1,979 to +1,139), not clear | -1,256 m (-3,240 to +925), not clear |
| % inside a cap | +16.2 points (+1.0 to +27.8), clear | +17.8 (+6.2 to +34.4), clear | +13.5 (-12.0 to +32.2), not clear |
| % for a teammate | -13.3 points (-24.5 to -3.8), clear | -5.0 (-35.3 to +14.2), not clear | -16.5 (-31.7 to -5.6), clear |
| Concealed damage per smoke | -4,582 (-7,301 to -2,538), clear | -3,305 (-6,027 to -999), clear | -5,598 (-10,340 to -2,139), clear |

Top 6 vs Rest, same ship:

| Ship | Top 6 n / Rest n | Median distance T6 / Rest | % inside T6 / Rest | % for a teammate T6 / Rest | Concealed dmg T6 / Rest | Clear gap? |
|---|---|---|---|---|---|---|
| Daring | 34 / 166 | 752 / 602 m | 41.2 / 42.8 | 50.0 / 42.2 | 3,991 / 3,548 | none |
| Gdansk | 60 / 58 | 1,382 / 1,858 m | 23.3 / 29.3 | 55.0 / 58.6 | 7,295 / 9,146 | none |
| Z-42 | 20 / 36 | 4,621 / -705 m | 20.0 / 55.6 | 40.0 / 44.4 | 4,177 / 4,098 | distance only: +5,326 m (+1,818 to +6,228), but Top 6 = 2 clans |
| Shimakaze | 15 / 43 | 3,789 / 2,758 m | 33.3 / 32.6 | 66.7 / 76.7 | 5,185 / 5,757 | none |
| Z-52, Grozovoi | 6 / 4 and 6 / 24 | too few on one side | | | | not tested |

- Mountain Range cap A (the real 10 km cap) barely matters: 2 Daring, 3 Gdansk, 1 Grozovoi, 4 Shimakaze smokes. Without them the medians are Daring 671 m, Gdansk 1,841 m, Grozovoi 1,028 m, Shimakaze 3,546 m; Daring minus Gdansk becomes -1,170 m (-2,261 to +12), still just short of clear.
- Second check on Daring vs Gdansk: 55% of Daring smokes are within 1 km of the cap vs 44% of Gdansk; 55% of Daring smokes record any concealed damage vs 75% of Gdansk (median 601 vs 3,564).
- Matches round 3 Module 1 (same medians, inside shares and damage). The "for the smoker only" share there (Daring 56%, Gdansk 43%) is 100 minus the "for a teammate" share here.

**Top 6 or Shared:** Shared. No Top 6 minus Rest interval excludes zero for Daring, Gdansk or Shimakaze. The Z-42 distance gap is two clans (VRTUS 14, KITE 6), not a Top 6 habit.

**Clans:**
- Daring: Top 6: HTDOG 21, KITE 6, VRTUS 5, BONKZ 2 | Rest: SCCC2 26, -BN- 22, KITED 16, EPOXY 16, KSC 13, HFANS 13, REEEE 11, MACHX 10, MZY 9, BONKY 6, KSE 5, BTLST 4, INCA 4, MACH 4, NGA 4, UYSC 3
- Gdansk: Top 6: RESIN 21, H-SR 15, BONKZ 13, HTDOG 9, KITE 2 | Rest: HFANS 13, KSE 10, EPOXY 9, UYSC 6, PFANS 6, KSC 5, SCCC2 3, RSR 2, MACHX 2, PN 1, KITED 1
- Z-42: Top 6: VRTUS 14, KITE 6 | Rest: MACH 11, HFANS 7, REEEE 6, MACHX 5, KSC 4, RSR 3
- Z-52: Top 6: KITE 6 | Rest: KITED 2, RSR 1, EPOXY 1
- Grozovoi: Top 6: H-SR 3, RESIN 3 | Rest: MACHX 15, MZY 3, RMN 2, EPOXY 2, INCA 1, MACH 1
- Shimakaze: Top 6: VRTUS 6, HTDOG 4, RESIN 3, BONKZ 2 | Rest: HFANS 13, 5D 8, UYSC 7, MANBA 5, RMN 4, EPOXY 3, INCA 2, BONKY 1

**Could not be done / proxy:** Z-52 has 10 smokes (small n): no Top 6 / Rest split and no interval worth trusting. Grozovoi Top 6 has 6 smokes: too few.

**Verdict:** Keep (the Daring vs Gdansk contrast is the part worth showing).

---

### B2. Getaway smokes (exhaust and battleship smoke)

**Answer:** The Italian cruisers' exhaust smoke goes with more losses, not fewer: the smoker died in about 16 of every 100 smokes, against 6 for cruisers with ordinary smoke and 7.5 for all smokes. The smoker stayed unseen for about 82% of the time it was under the smoke, less than the 90% of an ordinary cruiser smoke; battleships were unseen only 72% of the time but died no more often than the baseline.

**Numbers:** "deaths" = every ship that died in or behind the smoke; "smoker died" = the smoking ship itself; "hurt" = died or lost a third or more of its estimated health (health is an estimate).

| Group | n | Clans | Deaths per 100 | Smoker died per 100 | Smoker hurt per 100 | Unseen, % of time under the smoke | Unseen and covered, % of the smoke's whole life | Escape tag % |
|---|---|---|---|---|---|---|---|---|
| Napoli | 147 | 25 | 16.3 (10.6 to 24.1) | 15.0 (9.9 to 22.3) | 21.8 (16.9 to 27.9) | 81.4 (76.5 to 85.6) | 69.5 (63.7 to 73.8) | 17.0 |
| Venezia (3 clans) | 21 | 3 | 28.6 (11.1 to 60.0) | 23.8 (11.1 to 40.0) | 28.6 | 83.7 | 72.3 | 14.3 |
| **Italian cruisers together** | 168 | 25 | 17.9 (12.7 to 25.0) | 16.1 (11.4 to 22.5) | 22.6 (18.0 to 28.4) | 81.7 (76.6 to 85.6) | 69.9 (63.2 to 74.4) | 16.7 |
| **Battleships, listed separately** | | | | | | | | |
| C. Colombo | 20 | 13 | 10.0 (0.0 to 23.8) | 10.0 (0.0 to 23.8) | 25.0 (9.1 to 44.4) | 64.7 (51.0 to 78.6) | 56.4 (44.1 to 68.8) | 30.0 |
| Conte Verde (small n, 8 of 9 by H-SR) | 9 | 2 | 11.1 | 11.1 | 11.1 | 80.8 | 64.2 | 11.1 |
| Sicilia | 3 | 2 | too few | | | | | |
| Irresistible (ordinary smoke, not exhaust) | 2 | 1 | too few | | | | | |
| All battleships | 34 | 16 | 8.8 (0.0 to 17.6) | 8.8 (0.0 to 16.7) | 20.6 (10.3 to 37.5) | 71.7 (58.5 to 80.2) | 61.8 (50.3 to 69.6) | 23.5 |
| **Baselines** | | | | | | | | |
| All smokes | 1,547 | 30 | 11.4 (9.4 to 13.9) | 7.5 (5.9 to 9.8) | 16.2 (13.9 to 19.3) | 87.1 | 47.6 | 15.5 |
| Like-with-like: cruiser smokers with ordinary smoke (Svea, Jinan, ...) | 271 | 22 | 7.4 (5.2 to 10.1) | 6.3 (4.2 to 9.3) | 14.4 (11.0 to 18.3) | 90.1 | 65.8 | 15.5 |
| All cruiser smokers (includes the Italian cruisers) | 439 | 29 | 11.4 | 10.0 | 17.5 | 86.9 | 67.3 | 15.9 |
| Destroyer smokers | 1,074 | 30 | 11.5 | 6.4 | 15.5 | 87.6 | 38.9 | 15.1 |

Differences with intervals:

| Contrast | Deaths per 100 | Smoker died per 100 | Smoker hurt per 100 | Unseen % of time under the smoke |
|---|---|---|---|---|
| Italian cruisers minus cruisers with ordinary smoke | +10.5 (+3.4 to +18.8), clear | +9.8 (+3.3 to +17.3), clear | +8.2 (+2.0 to +14.7), clear | -8.4 (-13.5 to -3.8), clear |
| Italian cruisers minus all other smokes | +7.1 (+0.9 to +15.4), clear | +9.7 (+4.2 to +17.1), clear | +7.3 (+1.8 to +14.2), clear | -6.4 (-11.4 to -2.2), clear |
| Battleships minus cruisers with ordinary smoke | +1.4 (-7.2 to +10.7) | +2.6 (-6.3 to +11.4) | +6.2 (-5.1 to +23.7) | -18.4 (-32.9 to -9.3), clear |
| Battleships minus all other smokes | -1.9 (-11.1 to +6.9) | +2.4 (-5.9 to +10.5) | +5.2 (-6.9 to +22.7) | -16.4 (-30.2 to -7.2), clear |
| Battleships minus Italian cruisers | -9.0 (-19.7 to +1.4) | -7.2 (-18.0 to +2.6) | -2.0 (-13.3 to +14.8) | -10.0 (-22.6 to -0.9), clear |

- Who dies: in Italian cruiser smokes 27 of the 30 dead ships were the smoker. In battleship smokes all 3 were the smoker.
- These ships smoke when already in trouble: the smoker was already spotted at activation in 70% of Italian cruiser smokes and 68% of battleship smokes, against 54% for cruisers with ordinary smoke and 29% for destroyers. Mean health at activation 68% (both) vs 73%.
- The smoke is cut short by the smoker's death in 11.3% of Italian cruiser smokes and 11.8% of battleship smokes, vs 2.6% for ordinary cruiser smoke.
- The "escape" purpose tag is not what marks these smokes: 16.7% of Italian cruiser smokes carry it, the same as everyone else (difference +1.2, -6.7 to +9.3).
- Battleship smokes return 6,296 concealed damage per smoke (4,464 to 8,322); Italian cruisers 3,969.

**Top 6 or Shared:** Shared, and mostly a Rest tool: 153 of the 168 Italian cruiser smokes are by Rest clans. Top 6 (n=15, 5 clans): smoker died 33.3 per 100 vs Rest 14.4, difference +19.0 (+1.6 to +52.5), clear but on 5 deaths. Battleships Top 6 n=10 (small n, 8 are H-SR's Conte Verde): deaths 10.0 vs 8.3 per 100, no clear gap.

**Clans:**
- Napoli: Top 6: VRTUS 6, RESIN 3, BONKZ 3, HTDOG 2, H-SR 1 | Rest: KITED 18, MACHX 16, BTLST 14, 5D 14, HFANS 11, UYSC 10, REEEE 8, MZY 6, KSE 5, KM 4, MANBA 4, INCA 4, BONKY 4, PFANS 3, MACH 3, NGA 3, PN 2, SCCC2 1, KSC 1, -BN- 1
- Venezia: Top 6: none | Rest: KITED 9, NGA 7, 5D 5
- C. Colombo: Top 6: VRTUS 1, RESIN 1 | Rest: BTLST 3, KITED 3, -BN- 3, EPOXY 2, PN 1, UYSC 1, BONKY 1, INCA 1, NGA 1, MZY 1, HFANS 1
- Conte Verde: Top 6: H-SR 8 | Rest: EPOXY 1. Sicilia: Rest: HFANS 2, 5D 1. Irresistible: Rest: MACHX 2.

**Could not be done / proxy:**
- "% of the smoke's life the smoker stayed undetected" is not a batch field. The batch gives the share of the time the smoker was covered by the smoke that it was unseen (column 7). Column 8 is my own figure: unseen-and-covered seconds divided by the smoke's whole life. It is high for exhaust smoke simply because the ship travels with its smoke; use column 7 for the comparison.
- For battleships the like-with-like class baseline would be the battleships themselves (all 34 battleship smokes are in this table), so they are compared with cruisers with ordinary smoke and with all other smokes instead.
- A lost ship that was never seen (blind fire, torpedoes) is not counted as a smoke death by the batch.

**Verdict:** Keep.

---

### B3. Long smokes (Somers, Gearing, Harugumo, Delny)

**Answer:** Yes, as a group they are used differently from the cap sitters: laid on the move, on the side lanes and map edges, about 2 km outside the cap, and over 90% of the concealed damage is done by teammates, not the smoker. Harugumo is the exception inside the group: it does about a fifth of the damage itself and fires from its own smoke in 43% of smokes, against under 10% for Somers and Gearing.

**Numbers (deployment and use):**

| Ship | n | Clans | Concealed damage per smoke | Median distance to cap edge | Teammates' share of the concealed damage | Selfish (no teammate ever used it) | Enemy radar spotted a ship inside: narrow / broad |
|---|---|---|---|---|---|---|---|
| Somers | 260 | 18 | 14,524 (12,538 to 16,081) | 2,224 m | 94.1% (90.4 to 97.6) | 17.3% | 11.9% / 31.5% |
| Gearing | 180 | 16 | 16,296 (11,558 to 19,675) | 2,034 m | 96.9% (91.3 to 99.4) | 22.8% | 6.7% / 28.3% |
| Harugumo | 100 | 15 | 18,388 (12,865 to 22,389) | 2,017 m | 78.4% (68.2 to 86.9) | 18.0% | 16.0% / 33.0% |
| Delny (2 clans, 18 of 22 by H-SR) | 22 | 2 | 14,470 | 2,023 m | 98.9% | 22.7% | 4.5% / 22.7% |
| All four | 562 | 27 | 15,777 (13,583 to 17,385) | 2,079 m | 92.0% (87.9 to 95.1) | 19.4% | 10.7% / 30.4% |
| For comparison: cap sitters | 462 | 28 | 5,287 | 1,028 m | 34.7% | 75.5% | 10.8% / 24.7% |
| For comparison: all destroyer smokes | 1,074 | 30 | 10,798 | 1,742 m | 78.4% | 45.9% | 11.2% / 27.7% |

Radar, two readings: narrow = the batch's radar count (a ship inside gained the radar flag); broad = any covered ship, smoker included, that spent time detected by radar. The narrow field undercounts (170 smokes vs 372 on the broad reading, all smokes).
"Selfish" is the batch flag (no teammate was ever inside and none got damage from behind it). The classification label "for the smoker only" is lower: Somers 8.1%, Gearing 13.3%, Harugumo 14.0%, all four 11.0%, cap sitters 48.7%.

**Numbers (where on the map):** centre = middle third of the map's width; map edge = within 10% of the map's width of the west or east border (any border on Okinawa, whose spawns are on a diagonal); side lane = the rest. Land distance is missing for 106 of the 562 smokes; shares are of the smokes that have it.

| Ship | Centre | Side lane | Map edge | Median distance to land | Within 1 km of land | Over 2 km from land (open water) |
|---|---|---|---|---|---|---|
| Somers | 23.5% | 44.2% | 32.3% | 2,276 m | 20.1% | 58.3% |
| Gearing | 26.7% | 45.6% | 27.8% | 1,980 m | 27.9% | 49.4% |
| Harugumo | 17.0% | 41.0% | 42.0% | 2,356 m | 25.0% | 55.0% |
| Delny | 36.4% | 59.1% | 4.5% | 2,151 m | 27.8% | 55.6% |
| All four | 23.8% (19.7 to 28.2) | 44.7% | 31.5% (27.0 to 35.6) | 2,163 m | 23.9% | 54.6% |
| Cap sitters | 53.9% | 36.1% | 10.0% | 1,762 m | 29.1% | 43.1% |

Long-smoke ships minus cap sitters: concealed damage +10,490 (+8,368 to +12,226); distance to cap +1,051 m (+334 to +1,851); teammates' share of damage +57.3 points (+46.3 to +68.5); selfish -56.1 (-61.6 to -50.5); centre -30.1 (-37.9 to -22.6); map edge +21.5 (+15.3 to +27.2); open water +11.5 (+3.5 to +18.3); land distance +400 m (+115 to +696); deaths per 100 smokes +6.9 (+3.1 to +11.3). All clear. Radar: narrow -0.1 (-4.8 to +4.9), not clear; broad +5.8 (+0.1 to +11.5), just clear.
By map, the map-edge share of the long ships is highest on Hotspot (47% of 144) and Sleeping Giant (41% of 141), lowest on Mountain Range (10% of 78, where 49% are in the centre).

**Harugumo: does it sit in its own smoke and farm?** Partly. It still lays a moving line (median length laid 3.9 km, 4% parked, same as Somers), but it stays in it and shoots.

| Measure | Harugumo (n=100) | Somers (n=260) | Gearing (n=180) | Harugumo minus Somers | Harugumo minus Gearing |
|---|---|---|---|---|---|
| Own-gun share of the concealed damage | 21.6% (13.0 to 31.5) | 5.9% (2.5 to 10.0) | 3.1% (0.7 to 10.3) | +15.8 (+7.1 to +24.7), clear | +18.6 (+6.9 to +28.7), clear |
| Smoker's own concealed damage per smoke | 3,978 | 851 | 501 | +3,127 (+1,107 to +4,778), clear | +3,477 (+1,423 to +5,246), clear |
| Teammates' concealed damage per smoke | 14,409 | 13,673 | 15,795 | +736 (-3,771 to +5,319) | -1,385 (-7,383 to +5,549) |
| Smokes where the smoker did any concealed damage | 43.0% | 9.6% | 8.9% | +33.4 (+14.9 to +44.7), clear | +34.1 (+16.4 to +43.4), clear |
| Smokes where the smoker did 5,000+ | 18.0% | 3.5% | 2.8% | +14.5 (+4.7 to +21.9), clear | +15.2 (+4.4 to +24.4), clear |
| Smoker's time under its own smoke (median) | 55 s | 41 s | 38.5 s | +14 s (+7.8 to +28.7), clear | +16.5 s (+12.5 to +32.2), clear |
| Radar cruiser inside the smoke | 69.0% | 63.5% | 56.7% | +5.5 (-11.9 to +23.9) | +12.3 (-4.3 to +35.2) |
| Second destroyer recorded at the capture moment | 59.0% | 45.8% | 37.2% | +13.2 (+0.5 to +31.3), clear | +21.8 (+10.5 to +34.7), clear |
| Second destroyer 1 km+ forward of the smoke | 33.0% | 22.7% | 17.2% | +10.3 (-0.1 to +22.9) | +15.8 (+6.8 to +26.4), clear |
| Second destroyer in or behind the smoke | 12.0% | 5.8% | 3.9% | +6.2 (-0.4 to +10.3) | +8.1 (+0.6 to +13.3), clear |

- So the teammates get the same out of a Harugumo smoke as out of a Somers or Gearing smoke; the Harugumo's own guns come on top.
- The farming happens mostly when no cruiser shares the smoke. With a radar cruiser inside (69 smokes) the Harugumo does 11.6% of the concealed damage (2,413 per smoke); with none (31 smokes) it does 57.1% (7,462 per smoke). Difference in own share +45.5 points (+18.1 to +71.6), clear.
- Delny never does it: 1 of 22 smokes, 1.1% own share.

**Who spots for the Harugumo?** The batch cannot say (see below). The stand-in is "which allied ship was nearest to each enemy the Harugumo itself damaged, at the moment the smoke was fully laid":

| Nearest ally to the enemies the smoker damaged | Harugumo (53 enemies with a position) | Somers (30) | Gearing (18) |
|---|---|---|---|
| Another ship outside the smoke | 42% (22) | 17% (5) | 17% (3) |
| A second destroyer | 25% (13) | 17% (5) | 0 |
| The smoker itself | 21% (11) | 53% (16) | 83% (15) |
| Another ship in or behind the smoke | 8% (4) | 3% (1) | 0 |
| The radar cruiser inside the smoke | 6% (3) | 10% (3) | 0 |
| Median distance from that ally to the enemy | 7.8 km | 6.6 km | 7.3 km |

- Harugumo minus Somers: smoker nearest -32.6 points (-57.1 to -16.8), clear; a ship outside the smoke +24.8 (+1.7 to +40.4), clear; second destroyer +7.9 (-11.7 to +25.0), not clear; radar cruiser -4.3 (-14.6 to +8.5), not clear. Against Gearing: smoker -62.6 (-82.1 to -41.9), outside ship +24.8 (+2.6 to +41.8), second destroyer +24.5 (+14.8 to +28.8), all clear.
- Reading: when a Harugumo fires from its smoke, the closest friendly ship to its target is usually somebody else: a ship outside the smoke (4 in 10) or a second destroyer (1 in 4). It is rarely the radar cruiser sitting in the smoke (3 of 53). When a Somers or Gearing fires from its own smoke, it is itself the closest ship to the target.
- Where the second destroyer is, in the 13 Harugumo cases: 6 in or behind the same smoke, 5 level with or behind it, 2 forward. In the 43 smokes where the Harugumo did concealed damage, a second destroyer is recorded in 28: median 3.3 km from the smoke, 46% of them 1 km or more forward, 29% in or behind the smoke (Marceau 9, Shimakaze 3, Ragnar 3, Chateaurenault 3).
- Round 4 part B looked only at Top 6 Harugumo at G1/F1 on Sleeping Giant (11 smokes, all shooters) and found the nearest ally was mostly a ship outside the smoke (12 of 20). This all-map, own-gun-only version says the same.

**Top 6 or Shared:** Shared. The long-smoke habit (place, distance, damage, teammate share) shows no clear Top 6 minus Rest gap on any ship or on the four together: concealed damage +2,072 (-2,106 to +5,158), map edge +1.0 (-8.1 to +9.5), teammate share -1.1 (-9.4 to +6.2). Harugumo's own-gun share is the same in both groups: Top 6 22.4% (n=55) vs Rest 20.8% (n=45), +1.6 (-22.5 to +18.4).
Clear Top 6 minus Rest gaps that do exist: selfish share on the four together 12.7% vs 24.3%, -11.6 (-20.5 to -3.1), led by Gearing (10.8% vs 31.1%); deaths per 100 smokes 8.0 vs 18.8, -10.8 (-17.0 to -5.8) (Harugumo 9.1 vs 35.6; round 3 showed this gap goes away once games won and lost are separated); Harugumo over 2 km from land 65.9% vs 43.6%, +22.3 (+4.1 to +45.6); Gearing with a radar cruiser inside 75.7% vs 43.4%, +32.3 (+16.4 to +54.6); Somers with a second destroyer recorded 61.1% vs 37.6%, +23.5 (+8.5 to +38.5).

**Clans:**
- Somers: Top 6: RESIN 38, H-SR 33, BONKZ 12, VRTUS 7 | Rest: HFANS 28, REEEE 25, MZY 22, EPOXY 18, MACHX 17, BONKY 14, -BN- 12, NGA 11, PFANS 8, PN 5, UYSC 5, KITED 3, RSR 1, INCA 1
- Gearing: Top 6: BONKZ 37, KITE 23, VRTUS 10, HTDOG 4 | Rest: KSC 29, -BN- 18, BTLST 11, 5D 9, OGF 9, RSR 9, INCA 7, HFANS 5, RMN 3, EPOXY 3, KM 2, UYSC 1
- Harugumo: Top 6: RESIN 22, H-SR 20, BONKZ 7, HTDOG 6 | Rest: EPOXY 14, -BN- 6, PFANS 4, BONKY 4, PN 4, KM 3, SCCC2 3, REEEE 2, KITED 2, MZY 2, RSR 1
- Delny: Top 6: H-SR 18 | Rest: MZY 4

**Could not be done / proxy:**
- Spotting cannot be attributed from the batch. Ship positions exist at one moment per smoke (when it was fully laid) and for about 4 allied ships per smoke (median), so "no second destroyer recorded" does not prove there was none, and "nearest ally" means "closest", not "spotted". The nearest ally is typically 7 to 8 km from the target.
- Delny: one clan in practice, no Rest comparison (4 smokes).
- Numbers match round 3 Module 1 (damage per smoke, distance, deaths). Its "smoker only" column is the classification label (8 / 13 / 14%), not the batch selfish flag used here (17 / 23 / 18%).

**Verdict:** Lead (the Harugumo own-gun finding is the strongest single result on this page).

---

### B4. Hybrids (Grozovoi, Shimakaze, against Daring and Gdansk)

**Answer:** Shimakaze: yes, the variety is real. Its smokes come in two separate kinds, parked (27%) and laid over 1 km or more (70%), with almost nothing in between, and the same players do both. Grozovoi: no, the variety is not there. It looks like a Gdansk (one smear of short-to-medium smokes near the cap), on 30 smokes of which half are one clan.

**Numbers:**

| Measure | Grozovoi (n=30) | Shimakaze (n=58) | Daring (n=200) | Gdansk (n=118) |
|---|---|---|---|---|
| Spread on the map: mean distance from the ship's own centre point on each map | 9.7 km (6.3 to 14.6) | 11.5 km (7.7 to 12.3) | 8.1 km (6.0 to 8.7) | 8.4 km (6.2 to 9.1) |
| Range of cap distance (middle half of smokes, IQR) | 4.7 km | 7.8 km | 4.1 km | 5.0 km |
| Share of the most common purpose (cap contest for all four) | 46.7% | 36.2% | 55.0% | 36.4% |
| Purpose variety (bits; higher = more varied) | 2.21 | 2.27 | 1.88 | 2.62 |
| Parked (laid over under 500 m) | 22.2% | 26.8% | 64.5% | 41.7% |
| In between (500 m to 1 km) | 40.7% | 3.6% | 29.4% | 21.7% |
| Line (laid over 1 km or more) | 37.0% | 69.6% | 6.1% | 36.5% |
| Median length laid | 747 m | 1,684 m | 366 m | 690 m |

(Parked, in-between and line shares are of the smokes with a measured length: 27, 56, 197 and 115.)

Contrasts (hybrid minus comparison ship):

| Measure | Shimakaze - Daring | Shimakaze - Gdansk | Grozovoi - Daring | Grozovoi - Gdansk |
|---|---|---|---|---|
| Spread on the map, km | +3.4 (-0.3 to +5.6) | +3.1 (+0.3 to +5.4), clear | +1.6 (-1.5 to +6.5) | +1.3 (-2.0 to +6.5) |
| Cap distance range, m | +3,711 (+377 to +6,252), clear | +2,870 (-775 to +5,111) | +599 (-2,511 to +3,628) | -243 (-3,319 to +2,693) |
| Top purpose share, points | -18.8 (-31.7 to +3.4) | -0.2 (-11.3 to +19.5) | -8.3 (-22.0 to +15.7) | +10.2 (-1.3 to +32.5) |
| Purpose variety, bits | +0.39 (-0.34 to +0.94) | -0.35 (-1.00 to +0.12) | +0.33 (-0.72 to +0.63) | -0.41 (-1.37 to -0.16), clear (less varied) |
| Parked, points | -37.7 (-54.6 to -22.2), clear | -15.0 (-31.5 to -0.3), clear | -42.2 (-63.2 to -8.7), clear | -19.5 (-37.8 to +9.1) |
| In between, points | -25.9 (-34.4 to -16.9), clear | -18.2 (-25.9 to -10.1), clear | +11.3 (-23.0 to +28.5) | +19.0 (-12.8 to +38.2) |
| Line, points | +63.6 (+48.7 to +77.9), clear | +33.1 (+14.3 to +52.2), clear | +30.9 (+8.1 to +52.0), clear | +0.5 (-20.0 to +21.5) |

Two-modes test on the length laid (figure `b4-length-laid`):

| Ship | Smokes under 500 m / 500 m to 1 km / 1 to 2 km / over 2 km | Two humps? |
|---|---|---|
| Shimakaze | 15 / 2 / 21 / 18 | Yes. Bimodality coefficient 0.69 (over 0.555 points to two humps); two bell curves fit far better than one; a visible dip between humps at about 340 m and 2.0 km. No random Daring or Gdansk sample of the same size came out this two-humped (0 of 200 each). |
| Grozovoi | 6 / 11 / 5 / 5 | No. One hump around 600 m to 1 km plus a few very short smokes. Coefficient 0.49. 24% of random Daring samples and 18% of random Gdansk samples of the same size look at least as two-humped. |
| Gdansk | 48 / 25 / 29 / 13 | No. One smear from 100 m to 3 km. Coefficient 0.44; one bell curve fits as well as two. |
| Daring | 127 / 58 / 12 / 0 | No. One hump around 300 to 500 m. Coefficient 0.48. |

Same players doing both (a parked smoke and a line of 1 km+ on the same ship)?

| Ship | Players with 6+ smokes | ... who did both | Players with 3+ smokes | ... who did both | Player-games with 3+ smokes that had both |
|---|---|---|---|---|---|
| Shimakaze | 2 | 2 (HFANS player 3 parked / 10 lines; UYSC player 3 / 4) | 8 | 6 | 3 of 4 |
| Grozovoi | 1 | 1 (MACHX player: 2 parked, 3 lines, 6 in between) | 4 | 2 | 1 of 4 |
| Gdansk | 8 | 8 (6 with two or more of each) | 14 | 13 | 7 of 14 |
| Daring | 13 | 4 (2 with two or more of each) | 26 | 5 | 5 of 42 |

Plain reading, measure by measure:
- **Shimakaze.** Wider on the map than Gdansk (clear) and probably than Daring (just short of clear). Wider range of cap distances than Daring (clear). Two real modes on length. Both players with enough smokes do both, and 6 of 8 players with 3 or more. Leaving out its biggest clan (HFANS, 13 smokes) changes nothing: 12 / 2 / 17 / 12 across the four length bands. The variety is real. Its purposes are no more varied than Gdansk's.
- **Grozovoi.** No clear difference from Gdansk on any measure except that its purposes are less varied. More lines and fewer parked smokes than Daring, but so has Gdansk. No two modes: its typical smoke is a short moving one (41% between 500 m and 1 km). Half the data is MACHX (15 of 30; one player 11); without MACHX there are 15 smokes from 7 clans (4 / 4 / 1 / 3 across the bands). The variety is not shown.
- **Gdansk is the quiet hybrid.** Against Daring it has fewer parked smokes (-22.7 points, -35.2 to -10.2), more lines (+30.4, +18.9 to +45.6) and more varied purposes (+0.74 bits, +0.33 to +1.10), all clear, and every one of its 8 regular players does both. But it is a smear, not two modes.
- Counting grid cells does not separate the ships: at equal sample size (30 smokes) every ship fills 18 to 20 map cells with 80% of its smokes. The centre-point distance above is the usable spread measure.

Against round 4 part E: its "smoke-line share" (Shimakaze 64%, Grozovoi 53%, Gdansk 41%, Daring 10%) was a seven-feature label; the plain 1 km cut here gives 70%, 37%, 37% and 6%. Shimakaze and Daring agree; Grozovoi drops to Gdansk's level, which is the point: on length alone Grozovoi is no more a line-layer than Gdansk. Round 4 said neither ship splits into two clean groups on seven features together; on length laid alone Shimakaze does. Parked shares match (26%, 20%, 41%, 64% of all smokes there; 27%, 22%, 42%, 64.5% of measured smokes here). Round 4's spread figure used a different formula (13.5 vs 9.7 km); the order is the same.

**Top 6 or Shared:** Shared for Shimakaze: Top 6 (n=15) 26.7% parked and 66.7% lines vs Rest (n=43) 26.8% and 70.7%; no clear gap on any measure. Grozovoi Top 6 has 6 smokes: too few. One clear gap on the comparison ship: Top 6 Gdansk park more and lay fewer lines than Rest Gdansk (parked 48.3% vs 35.1%, +13.2, +1.5 to +25.8; lines 24.1% vs 49.1%, -25.0, -42.1 to -6.1).

**Clans:**
- Shimakaze: Top 6: VRTUS 6, HTDOG 4, RESIN 3, BONKZ 2 | Rest: HFANS 13, 5D 8, UYSC 7, MANBA 5, RMN 4, EPOXY 3, INCA 2, BONKY 1 (18 players)
- Grozovoi: Top 6: H-SR 3, RESIN 3 | Rest: MACHX 15, MZY 3, RMN 2, EPOXY 2, INCA 1, MACH 1 (11 players)

**Could not be done / proxy:**
- "Players with at least 6 smokes" leaves 2 Shimakaze players and 1 Grozovoi player, so the 3+ smokes column is given as a wider, weaker check.
- Grozovoi: 30 smokes cannot settle anything; every interval is wide.
- Per-map spread for the hybrids rests on 13 to 14 smokes on Hotspot (Shimakaze 14.8 km, Grozovoi 11.4 km, Daring 9.6 km, Gdansk 6.8 km) and fewer elsewhere.

**Verdict:** Keep for Shimakaze (two real modes); Drop for Grozovoi (variety not supported by the data).

---

## Figures (working, in `round5/figures/`)

- `b1-cap-sitters-distance`: every smoke's distance to the cap edge, by ship.
- `b3-long-smokes-maps`: Harugumo, Somers, Gearing smoke lines on Sleeping Giant and Hotspot; rings mark smokes where the smoker itself did 5,000+ concealed damage.
- `b3-own-gun-share`: smoker's own share of the concealed damage, Top 6 and Rest.
- `b4-length-laid`: length laid, by ship, on a log scale (the two-modes picture).
- `b4-hybrids-maps`: Grozovoi, Shimakaze, Daring, Gdansk on Hotspot and Loop; parked dots and 1 km+ lines.
