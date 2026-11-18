# Round 5b findings, worker n2: danger zones with real health (C3), leaving the smoke and radar deaths (A2)

Batch `output/20261117-230933`. Everything here is association, not cause. Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS. Intervals are 95%, whole clans resampled; * = excludes zero. Round 5 numbers are from `round5/FINDINGS.md`.

Single-replay game (KSC vs -BN-, 9 smokes): the KSC ships have no replay of their own, so their health is blank or stale. Those ships are left out of every health number (5 ship-smoke pairs, all the KSC smoker in 4 smokes). The -BN- ships in that game are complete and stay in.

Library note: `r5lib.py` now corrects two games that ran on a 15-minute clock (17 smokes had `el` 300 s too high in round 5). Nothing here uses `el`; times come from `e0`/`e1`. The round 5 time-of-game splits for those 17 smokes moved for that reason; the radar-death time split below uses the corrected times.

### Real health: old estimate against the tracks, and the baselines redone

**Answer:** The round 5 "hurt" flag was right for about 9 ships in 10, but it was low for destroyers and high for cruisers. With real health and deaths read from the tracks, 23.1 smoking destroyers per 100 destroyer smokes died or lost a third of their health while the smoke stood (round 5 said 15.5), and 19.4 sheltering cruisers per 100 (round 5 said 22.0). The bigger surprise is deaths: the tracks show 137 smoking destroyers dead before 20 s after their smoke cleared, the batch list has 69.

**Numbers:**

Definition used from here on. Died = the ship's track shows it dead between the smoke's activation and 20 s after it dispersed (20 s is the batch's own grace). Hurt = died, or its health at dispersal was lower than at activation by a third of full health or more (net loss, so health healed back inside the window does not count). Beside it: the "high-to-low" version (largest fall from a high point inside the window), which ignores heals.

Old estimate against real health, same ships, same death list, so only the health source differs:

| who | ship-smoke pairs | hurt, old estimate | hurt, real health | flagged by both | new flags | flags lost | agree |
|---|---|---|---|---|---|---|---|
| destroyer smoker (destroyer smokes) | 1070 | 167 | 225 | 150 | 75 | 17 | 91.4% |
| sheltering cruisers, any smoke | 612 | 134 | 113 | 88 | 25 | 46 | 88.4% |
| every covered ship | 2359 | 410 | 451 | 326 | 125 | 84 | 91.1% |

- 209 flags flip out of 2359: 125 new, 84 lost.
- New flags: the old number only counted damage taken while the batch had the ship as covered. Real health counts everything between activation and dispersal. In 101 of the 125 the biggest hit landed outside the smoke outline (the ship had moved out).
- Lost flags: 38 healed back (mostly cruisers), 20 because the estimate of full health was too low, 26 other.

How far the old estimate of full health was from real full health (estimate divided by real):

| class | pairs | median | middle half | range | within 10% of real |
|---|---|---|---|---|---|
| destroyer | 1124 | 0.906 | 0.853 to 1.024 | 0.65 to 1.27 | 38% |
| cruiser | 1046 | 1.018 | 0.961 to 1.111 | 0.44 to 1.78 | 53% |
| battleship | 152 | 1.258 | 1.179 to 1.495 | 1.13 to 1.63 | 0% |

Furthest off: Smolensk 1.78 (n 18), Conte Verde 1.63 (n 18), Brisbane 0.44 (n 117), Harugumo 0.68 (n 97), Worcester 1.32 (n 36), Minotaur 1.27 (n 56), Cerberus 1.27 (n 20), Bungo 1.26 (n 22). Brisbane was estimated at under half its real health, so round 5 flagged Brisbanes as hurt far too easily.

Deaths. Batch list, ships at risk (smoker, inside, behind): 176; the track confirms 174 inside the window. Track deaths in the window: 270; 96 of them are not in the batch list (by role: smoker 84, inside 8, behind 4). Of those 96, 50 died inside the smoke outline. The batch list only counts a ship that the smoke concealed and that was then detected at a flag change before it died. It leaves out ships that were lit from the start and stayed lit, ships that died without being detected, and ships that had left.

Smoking destroyer, per 100 destroyer smokes (n 1070: Top 6 387, Rest 683):

| measure | count | per 100 [95%] | Top 6 | Rest | Top 6 minus Rest |
|---|---|---|---|---|---|
| died, batch list (round 5 measure) | 69 | 6.4 [4.5 to 9.4] | 2.8 | 8.5 | -9.7 to -2.3 * |
| died, track (activation to 20 s after dispersal) | 137 | 12.8 [9.9 to 16.8] | 8.5 | 15.2 | -13.9 to -1.6 * |
| died or hurt, old estimate (round 5 measure) | 167 | 15.6 [12.9 to 19.6] | 10.6 | 18.4 | -14.3 to -3.4 * |
| died or hurt, real health, batch deaths | 225 | 21.0 [17.7 to 25.3] | 15.2 | 24.3 | -16.6 to -2.9 * |
| died or hurt, real health, track deaths (round 5b definition) | 247 | 23.1 [19.5 to 27.6] | 17.3 | 26.4 | -17.0 to -2.4 * |
| same, peak-to-trough health loss | 254 | 23.7 [20.2 to 28.6] | 17.6 | 27.2 | -17.9 to -3.1 * |

Sheltering cruisers (inside or behind), per 100 cruisers, any smoke (n 612: Top 6 274, Rest 338):

| measure | count | per 100 [95%] | Top 6 | Rest | Top 6 minus Rest |
|---|---|---|---|---|---|
| died, batch list (round 5 measure) | 48 | 7.8 [5.7 to 10.5] | 5.5 | 9.8 | -8.3 to -0.5 * |
| died, track (activation to 20 s after dispersal) | 59 | 9.6 [7.2 to 12.2] | 6.9 | 11.8 | -9.2 to -0.5 * |
| died or hurt, old estimate (round 5 measure) | 134 | 21.9 [17.0 to 27.0] | 17.5 | 25.4 | -17.9 to +2.7 |
| died or hurt, real health, batch deaths | 113 | 18.5 [14.5 to 22.8] | 13.5 | 22.5 | -16.3 to -1.7 * |
| died or hurt, real health, track deaths (round 5b definition) | 119 | 19.4 [15.2 to 24.2] | 14.6 | 23.4 | -16.6 to -1.3 * |
| same, peak-to-trough health loss | 152 | 24.8 [19.1 to 30.4] | 18.6 | 29.9 | -21.6 to -0.7 * |

Sheltering cruisers in destroyer smokes only (n 586): died (track) 9.7, died or hurt 19.6 per 100.

Typical loss: a smoking destroyer loses 17.3% of full health on average while its smoke stands; 44% lose under 1%. Sheltering cruisers lose 16.2% net, 19.7% high-to-low (they heal).

**Top 6 or Shared:** Top 6 pattern. Top 6 smoking destroyers die or get hurt less (17.3 vs 26.4 per 100, -17.0 to -2.4 *); deaths alone 8.5 vs 15.2 (-13.9 to -1.6 *). Sheltering cruisers 14.6 vs 23.4 (-16.6 to -1.3 *); deaths 6.9 vs 11.8 (-9.2 to -0.5 *).

**Could not be done / proxy:** 171 of 1,547 smokes have no dispersal time in the replay (the game ended first, mostly); their end is activation + emission + puff life. Health is sampled every 2 s, so a fall and a heal inside one step are not seen. "While the smoke stood" is a time window: a ship that left the smoke and was hit elsewhere still counts for that smoke (see A2 leaving).

**Verdict:** Keep (use the real-health baselines; retire the estimate).

**Changed from round 5:**
- Destroyer smoker died, per 100 destroyer smokes: 6.4 -> 12.8 (+6.4). Different definition: track deaths in the smoke window, not the batch list. The batch list on its own still gives 6.4.
- Destroyer smoker died or hurt, per 100: 15.5 -> 23.1 (+7.6). Better data (real health: 21.0 with the old death list) plus the track deaths.
- Sheltering cruiser died, per 100 cruisers (any smoke): 8.0 -> 9.6 (+1.6). Track deaths. The batch list gives 7.8 on the cruisers with complete health.
- Sheltering cruiser died or hurt, per 100 (any smoke): 22.0 -> 19.4 (-2.6). Better data: cruisers heal and the estimate was too low for Brisbane. High-to-low version: 24.8.
- Sheltering cruiser died or hurt, destroyer smokes only (round 5 A2 table): 22.5 -> 19.6 (-2.9). Same reason.
- Top 6 minus Rest, cruiser died or hurt (any smoke): not clear (-17.7 to +2.6 in destroyer smokes) -> -16.6 to -1.3 *. Real health.
- Destroyer smokes in the health numbers: 1074 -> 1070 (-4). The KSC smoker in the single-replay game is left out.

### C3. Danger zones (real health; two ways of placing the damage)

**Answer:** No. With real health there is no danger zone the data can stand behind. Keyed on the smoke centre, 2 of 108 areas pass the rule and shuffled outcomes pass 1.57 by luck. Keyed on where the ship was hit, 3 of 111 pass and luck gives 1.75. Round 5's one sturdy flag, Hotspot inside cap C, does not survive: 27 per 100 against a same-map baseline of 18.7. Every area that passes has 8 to 14 ships.

**Numbers:**

- Rule (unchanged): 8+ in the area, died-or-hurt rate clearly above BOTH the all-map and the same-map like-with-like baseline. Areas: 10 x 10 cells in the smoking team's frame, thin cells merged in their 2 x 2 block, plus "inside cap X".
- Baselines: destroyer smoker 12.8 died and 23.1 died-or-hurt per 100; sheltering cruisers 9.6 and 19.4. Same-map died-or-hurt: destroyers Sleeping Giant 21.4, Hotspot 18.7, Mountain Range 26.6, Land of Fire 26.6, Sea of Fortune 25.6, Loop 20.4, Okinawa 30.5; cruisers Sleeping Giant 19.2, Hotspot 15.1, Mountain Range 16.9, Land of Fire 24.6, Sea of Fortune 20.3, Loop 18.2, Okinawa 33.3.
- Version 1, keyed on the smoke centre (the round 5 areas): 312 areas, 108 tested (77 destroyer, 31 cruiser). Flagged 2. On deaths alone: 0. Placebo (120 runs, outcomes shuffled within the map): 1.57 flags by luck per run (median 1, 95th percentile 4); 58 of 120 runs had 2 or more.
- Version 2, keyed on where the damage happened: 315 areas, 111 tested (73 destroyer, 38 cruiser). Flagged 3. On deaths alone: 0. Placebo: 1.75 by luck per run (median 2, 95th percentile 4); 29 of 120 runs had 3 or more.
- Version 2 unit and denominator: one entry per ship at risk (the smoking destroyer; each cruiser inside or behind a smoke). Each ship is placed once: at its death position if it died (last position alive, team frame of the smoking team); at its position at its largest 2 s health fall if it was hurt and lived; otherwise where it was half way through the smoke. Rate = ships placed in the area that died or were hurt / all ships placed in the area. So the denominator is ships, not smokes.

Areas that pass the rule:

| keyed on | map | who | area | n | died or hurt per 100 | baseline all / same map | gap vs all maps | gap vs same map | died per 100 (n; baseline) | death gap interval |
|---|---|---|---|---|---|---|---|---|---|---|
| smoke centre | Sleeping Giant | destroyer smoker | F5 | 12 (small n) | 42 (5 of 12) | 23.1 / 21.4 | +19 (+2 to +36 *) | +20 (+6 to +35 *) | 17 (2; 12.8) | -15 to +26 |
| smoke centre | Sleeping Giant | destroyer smoker | E7+F7+F8 | 8 (small n) | 62 (5 of 8) | 23.1 / 21.4 | +39 (+8 to +76 *) | +41 (+10 to +77 *) | 25 (2; 12.8) | -14 to +50 |
| where hit | Sleeping Giant | destroyer smoker | E8 | 8 (small n) | 75 (6 of 8) | 23.1 / 21.4 | +52 (+35 to +79 *) | +54 (+35 to +82 *) | 38 (3; 12.8) | -14 to +60 |
| where hit | Sleeping Giant | destroyer smoker | E7+F7+F8 | 10 (small n) | 50 (5 of 10) | 23.1 / 21.4 | +27 (+3 to +60 *) | +29 (+6 to +61 *) | 30 (3; 12.8) | -11 to +53 |
| where hit | Mountain Range | destroyer smoker | G5+H5+G6+H6 | 14 (small n) | 50 (7 of 14) | 23.1 / 26.6 | +27 (+4 to +53 *) | +23 (+2 to +48 *) | 29 (4; 12.8) | -4 to +40 |

For each: laid while 50+ behind / a covered ship radar-lit while the smoke stood (area, then the whole map):

- Sleeping Giant F5 (destroyer smoker, by smoke centre): 50+ behind 17% (map 24%); radar 67% (map 41%). Without the clan with most bad outcomes (VRTUS): 44.4 per 100 (n 9).
- Sleeping Giant E7+F7+F8 (destroyer smoker, by smoke centre): 50+ behind 25% (map 24%); radar 62% (map 41%). Without the clan with most bad outcomes (SCCC2): 57.1 per 100 (n 7).
- Sleeping Giant E8 (destroyer smoker, by where hit): 50+ behind 12% (map 24%); radar 62% (map 41%). Without the clan with most bad outcomes (RESIN): 80.0 per 100 (n 5).
- Sleeping Giant E7+F7+F8 (destroyer smoker, by where hit): 50+ behind 30% (map 24%); radar 70% (map 41%). Without the clan with most bad outcomes (UYSC): 44.4 per 100 (n 9).
- Mountain Range G5+H5+G6+H6 (destroyer smoker, by where hit): 50+ behind 57% (map 24%); radar 36% (map 37%). Without the clan with most bad outcomes (OGF): 50.0 per 100 (n 12).

Round 5 flags on the same areas:

| map | who | area | smokes | round 5: died or hurt per 100 (n) | real health: per 100 | gap vs all maps / same map | result |
|---|---|---|---|---|---|---|---|
| Hotspot | destroyer smoker | inside cap C | 22 | 32 (7) | 27 (6 of 22) | +4 (-9 to +44) / +8 (-4 to +52) | does not survive |
| Sea of Fortune | destroyer smoker | E5+F5+E6 | 8 (small n) | 62 (5) | 62 (5 of 8) | +39 (+1 to +79 *) / +37 (-0 to +76) | does not survive |
| Sleeping Giant | destroyer smoker | E7+F7+F8 | 8 (small n) | 50 (4) | 62 (5 of 8) | +39 (+8 to +76 *) / +41 (+10 to +77 *) | survives |
| Mountain Range | sheltering cruisers | E7+F7+F8 | 7 (too few) | - | - | - | not rated: one of its 8 smokes is the KSC smoke in the single-replay game |

Second way (check): the round 5 outcomes recomputed here on the same units give 108 areas tested and flag 3: Sleeping Giant E7+F7+F8 (destroyer smoker); Hotspot inside cap C (destroyer smoker); Sea of Fortune E5+F5+E6 (destroyer smoker). Round 5 printed 109 and 4; the difference is the excluded single-replay ships.
Version 2 flags placed a third way (where the ship was at activation): Sleeping Giant E8: too few (n 7); Sleeping Giant E7+F7+F8: 62 per 100 (n 8); Mountain Range G5+H5+G6+H6: 38 per 100 (n 16).

Per map:

| map | tested, smoke centre | flagged | tested, where hit | flagged |
|---|---|---|---|---|
| Sleeping Giant | 25 | F5 (destroyer smoker), E7+F7+F8 (destroyer smoker) | 26 | E8 (destroyer smoker), E7+F7+F8 (destroyer smoker) |
| Hotspot | 24 | none qualifies | 25 | none qualifies |
| Mountain Range | 17 | none qualifies | 18 | G5+H5+G6+H6 (destroyer smoker) |
| Land of Fire | 9 | none qualifies | 10 | none qualifies |
| Sea of Fortune | 13 | none qualifies | 13 | none qualifies |
| Loop | 14 | none qualifies | 13 | none qualifies |
| Okinawa | 6 | none qualifies | 6 | none qualifies |

Death positions (new). Ships at risk that died between activation and 20 s after dispersal, distance from where they died to the edge of the smoke:

| who died | deaths | in the batch list | inside the outline | within 1 km of the edge | 1-3 km | over 3 km | share inside | median distance past the edge |
|---|---|---|---|---|---|---|---|---|
| smoking destroyer | 137 | 68 | 57 | 23 | 28 | 29 | 42% | 1,923 m |
| sheltering cruiser | 59 | 48 | 13 | 9 | 25 | 12 | 22% | 1,960 m |
| smoker (other class) | 61 | 47 | 36 | 18 | 6 | 1 | 59% | 739 m |
| other sheltering ship | 11 | 10 | 4 | 1 | 2 | 4 | 36% | 3,971 m |

268 ship-smoke pairs, 262 distinct ships, all smoker classes. By map (deaths, inside the outline): Sleeping Giant 49, 22, Hotspot 40, 18, Mountain Range 32, 11, Land of Fire 43, 16, Sea of Fortune 33, 16, Loop 34, 18, Okinawa 37, 9. Working figures: `figures/n2-deaths-<map>`.

**Top 6 or Shared:** Sleeping Giant F5 (by smoke centre): Shared spot (Top 6 6% vs Rest 5% of the map's smokes, -6 to +9). Sleeping Giant E7+F7+F8 (by smoke centre): Shared spot (Top 6 2% vs Rest 5% of the map's smokes, -8 to +1). Sleeping Giant E8 (by where hit): Shared spot (Top 6 4% vs Rest 3% of the map's ships, -4 to +6). Sleeping Giant E7+F7+F8 (by where hit): Shared spot (Top 6 2% vs Rest 6% of the map's ships, -12 to +1). Mountain Range G5+H5+G6+H6 (by where hit): Shared spot (Top 6 7% vs Rest 14% of the map's ships, -20 to +3).

**Clans:**
- Sleeping Giant F5 (destroyer smoker, by smoke centre; 7 clans, 9 games): Top 6: VRTUS 3, RESIN 2, HTDOG 1 | Rest: KITED 2, HFANS 2, KSE 1, 5D 1.
- Sleeping Giant E7+F7+F8 (destroyer smoker, by smoke centre; 7 clans, 8 games): Top 6: BONKZ 2 | Rest: RMN 1, SCCC2 1, PFANS 1, -BN- 1, RSR 1, KITED 1.
- Sleeping Giant E8 (destroyer smoker, by where hit; 5 clans, 6 games): Top 6: RESIN 3, BONKZ 1 | Rest: MACHX 2, HFANS 1, EPOXY 1.
- Sleeping Giant E7+F7+F8 (destroyer smoker, by where hit; 7 clans, 8 games): Top 6: BONKZ 2 | Rest: KITED 3, RMN 1, UYSC 1, PFANS 1, -BN- 1, RSR 1.
- Mountain Range G5+H5+G6+H6 (destroyer smoker, by where hit; 11 clans, 11 games): Top 6: RESIN 2, H-SR 1, HTDOG 1 | Rest: OGF 2, SCCC2 2, RMN 1, REEEE 1, KSE 1, UYSC 1, KSC 1, MACH 1.

**Could not be done / proxy:** Two thirds of areas have under 8 and are not rated. "Hurt" is a net loss over the whole smoke window, so damage taken after a ship left the smoke counts. In version 2 a hurt ship is placed where it was hit and an unhurt ship where it was at mid-smoke; the placebo keeps positions and shuffles outcomes, so it cannot mimic that link, and the version 2 luck count is if anything too low. Positions are every 2 s.

**Verdict:** Drop danger zones as map markings on every map. Both versions flag about as many areas as luck does, all with small n, and no area passes on deaths alone. Keep the per-map death-position maps as a Lead: they show that most ships that die "in smoke" die outside the outline (42% of smoking destroyers and 22% of sheltering cruisers died inside it).

**Changed from round 5:**
- Flagged areas, keyed on the smoke centre: 4 -> 2 (-2). Real health and track deaths. Now: Sleeping Giant F5, Sleeping Giant E7+F7+F8.
- Hotspot inside cap C (destroyer smoker), died or hurt per 100: 32 -> 27.3 (-4.7). Real health: 6 of 22 instead of 7 of 22, while the baselines rose (all maps 15.5 -> 23.1, Hotspot 11.9 -> 18.7). The gap is no longer clear (-4 to +52 against the map). Round 5 called this Lead; now Drop.
- Sea of Fortune E5+F5+E6: flag (n 8) -> no flag. Same 5 of 8, but the Sea of Fortune baseline rose and the gap against the map is not clear.
- Sleeping Giant E7+F7+F8: flag, 50 per 100 (n 8) -> flag, 62 per 100 (n 8). Still passes, still n 8, still in line with luck.
- Mountain Range E7+F7+F8 (cruisers): flag (n 8) -> not rated (n 7). One of the 8 smokes is in the single-replay game, health incomplete.
- Placebo, flags by luck per run: 1.23 -> 1.57 (+0.3). Higher baselines make chance flags a little more common.
- Areas tested: 109 -> 108 (-1). Single-replay ships excluded.
- Keyed on where the ship was hit: not possible -> 3 flags, 1.75 by luck. New: death positions and health tracks.
- Death position: unknown -> 268 deaths placed. New: tracks.

### A2. Leaving the smoke (from ship tracks)

**Answer:** Most ships that "died in smoke" had already left it. Of round 5's 124 deaths in destroyer smokes, 29 died inside a standing smoke, 82 died after sailing out of one (25 within 30 s, 57 later), 5 after the smoke dispersed around them and 8 were never inside. But leaving is not the dangerous moment: in the 30 s after leaving a standing smoke 3.1 smoking destroyers per 100 died, against 3.6 in the 30 s after the smoke dispersed around those that stayed, and 3.8 per 30 s spent inside. Being 50+ behind raises all three.

**Numbers:**

How a death is classed, from the track (position every 2 s): inside = last position alive is within the radius of a puff that still stands; left = it moved outside every puff while the puffs it had been in still stood; dispersed = the puffs around it ended while it was still in the old outline; never inside = no sample inside a standing puff. Each puff ends at its own time (the first puff of a long smoke goes first).

Round 5's death list (batch smoke deaths in destroyer smokes). Cells: count (Top 6 / Rest):

| who died | n (Top 6 / Rest) | inside a standing smoke | within 30 s of leaving | more than 30 s after leaving | after it dispersed around the ship | never inside the outline |
|---|---|---|---|---|---|---|
| smoking destroyer | 69 (11 / 58) | 21 (1 / 20) | 14 (2 / 12) | 32 (7 / 25) | 2 (1 / 1) | 0 (0 / 0) |
| sheltering cruiser | 48 (15 / 33) | 7 (2 / 5) | 10 (1 / 9) | 20 (9 / 11) | 3 (1 / 2) | 8 (2 / 6) |
| other ship | 7 (3 / 4) | 1 (0 / 1) | 1 (1 / 0) | 5 (2 / 3) | 0 (0 / 0) | 0 (0 / 0) |
| all | 124 (29 / 95) | 29 (3 / 26) | 25 (4 / 21) | 57 (18 / 39) | 5 (2 / 3) | 8 (2 / 6) |

Every ship at risk whose track shows a death between activation and 20 s after dispersal (201 ship-smoke pairs; the batch list has 120 of them):

| who died | n (Top 6 / Rest) | inside a standing smoke | within 30 s of leaving | more than 30 s after leaving | after it dispersed around the ship | never inside the outline |
|---|---|---|---|---|---|---|
| smoking destroyer | 137 (33 / 104) | 53 (10 / 43) | 28 (7 / 21) | 53 (15 / 38) | 2 (1 / 1) | 1 (0 / 1) |
| sheltering cruiser | 57 (19 / 38) | 11 (3 / 8) | 9 (1 / 8) | 21 (10 / 11) | 6 (3 / 3) | 10 (2 / 8) |
| other ship | 7 (3 / 4) | 1 (0 / 1) | 1 (1 / 0) | 4 (2 / 2) | 0 (0 / 0) | 1 (0 / 1) |
| all | 201 (55 / 146) | 65 (13 / 52) | 38 (9 / 29) | 78 (27 / 51) | 8 (4 / 4) | 12 (2 / 10) |

The 81 deaths the batch list misses are mostly smoking destroyers (69), and 32 of those died inside their standing smoke.
Deaths after leaving (batch list): median 53.0 s after leaving, median 1,996 m past the smoke edge.

The rate question. Ships at risk in destroyer smokes that were inside a standing smoke at some point: 1172 left while it stood, 200 stayed until the puffs around them ended, 64 died inside (games that ended inside the next 30 s are dropped). Leavers left a median 41 s after activation with a median 80 s of smoke still to run: destroyers lay smoke and move on. Score state is taken at the moment of leaving or dispersal, from the score timeline.

| group | left: n | stayed: n | died in next 30 s per 100: left (n) | stayed (n) | left minus stayed | died or lost 1/3+ per 100: left (n) | stayed (n) | left minus stayed |
|---|---|---|---|---|---|---|---|---|
| smoking destroyer, all | 862 | 83 | 3.1 (27) | 3.6 (3) | -6.0 to +4.3 | 5.9 (51) | 6.0 (5) | -6.6 to +6.4 |
| smoking destroyer, 50+ behind | 234 | 23 | 5.6 (13) | 4.3 (1) | -11.1 to +8.8 | 10.3 (24) | 4.3 (1) | -6.8 to +14.6 |
| smoking destroyer, not behind | 628 | 60 | 2.2 (14) | 3.3 (2) | -5.5 to +2.9 | 4.3 (27) | 6.7 (4) | -9.0 to +3.6 |
| smoking destroyer, Top 6 | 319 | 26 | 1.9 (6) | 7.7 (2) | -21.5 to +2.8 | 3.4 (11) | 7.7 (2) | -21.1 to +5.6 |
| smoking destroyer, Rest | 543 | 57 | 3.9 (21) | 1.8 (1) | -2.0 to +6.7 | 7.4 (40) | 5.3 (3) | -4.5 to +9.1 |
| smoking destroyer, Top 6, 50+ behind | 48 | 3 (too few) | 2.1 (1) | too few (1) | - | 6.2 (3) | too few (1) | - |
| smoking destroyer, Rest, 50+ behind | 186 | 20 | 6.5 (12) | 0.0 (0) | +3.2 to +11.0 * | 11.3 (21) | 0.0 (0) | +6.6 to +17.4 * |
| smoking destroyer, Top 6, not behind | 271 | 23 | 1.8 (5) | 4.3 (1) | -10.9 to +2.7 | 3.0 (8) | 4.3 (1) | -9.8 to +4.8 |
| smoking destroyer, Rest, not behind | 357 | 37 | 2.5 (9) | 2.7 (1) | -5.0 to +4.5 | 5.3 (19) | 8.1 (3) | -13.7 to +5.8 |
| sheltering cruiser, all | 310 | 117 | 2.9 (9) | 2.6 (3) | -3.5 to +3.6 | 6.1 (19) | 8.5 (10) | -8.2 to +2.6 |
| sheltering cruiser, 50+ behind | 71 | 36 | 4.2 (3) | 2.8 (1) | -7.4 to +8.3 | 9.9 (7) | 13.9 (5) | -17.3 to +8.9 |
| sheltering cruiser, not behind | 239 | 81 | 2.5 (6) | 2.5 (2) | -4.5 to +3.8 | 5.0 (12) | 6.2 (5) | -8.6 to +5.3 |
| sheltering cruiser, Top 6 | 143 | 59 | 0.7 (1) | 1.7 (1) | -6.8 to +1.7 | 4.2 (6) | 6.8 (4) | -9.8 to +1.9 |
| sheltering cruiser, Rest | 167 | 58 | 4.8 (8) | 3.4 (2) | -5.8 to +6.7 | 7.8 (13) | 10.3 (6) | -13.0 to +6.5 |
| sheltering cruiser, Top 6, 50+ behind | 24 | 14 (small n) | 0.0 (0) | 0.0 (0) | +0.0 to +0.0 | 4.2 (1) | 7.1 (1) | -15.8 to +9.4 |
| sheltering cruiser, Rest, 50+ behind | 47 | 22 | 6.4 (3) | 4.5 (1) | -14.3 to +12.9 | 12.8 (6) | 18.2 (4) | -27.0 to +14.5 |
| sheltering cruiser, Top 6, not behind | 119 | 45 | 0.8 (1) | 2.2 (1) | -10.5 to +2.2 | 4.2 (5) | 6.7 (3) | -17.7 to +5.5 |
| sheltering cruiser, Rest, not behind | 120 | 36 | 4.2 (5) | 2.8 (1) | -5.6 to +7.6 | 5.8 (7) | 5.6 (2) | -7.5 to +8.6 |

A gap marked * where the stayed count is 0 of about 20 rests on no events and should be read as "no difference shown".

Per 30 seconds, three situations side by side (deaths per 100 ship half-minutes; health lost = every fall added up, share of full health; detected = share of time or ships):

| who | score | inside a standing smoke: deaths per 100 (n) | health lost | detected | 30 s after leaving: deaths per 100 | health lost | 30 s after it dispersed: deaths per 100 | health lost |
|---|---|---|---|---|---|---|---|---|
| smoking destroyer | all | 3.8 (53) | 6.4% | 12.0% | 3.1 (n 862) | 4.1% | 3.6 (n 83) | 7.8% |
| smoking destroyer | behind 50+ | 8.6 (30) | 9.1% | 13.6% | 5.6 (n 234) | 6.3% | 4.3 (n 23) | 5.3% |
| smoking destroyer | not behind | 2.2 (23) | 5.5% | 11.5% | 2.2 (n 628) | 3.3% | 3.3 (n 60) | 8.8% |
| sheltering cruiser | all | 1.1 (11) | 3.4% | 6.9% | 2.9 (n 310) | 6.7% | 2.6 (n 117) | 8.1% |
| sheltering cruiser | behind 50+ | 2.1 (5) | 4.8% | 9.9% | 4.2 (n 71) | 9.1% | 2.8 (n 36) | 12.7% |
| sheltering cruiser | not behind | 0.7 (6) | 3.0% | 6.1% | 2.5 (n 239) | 6.0% | 2.5 (n 81) | 6.1% |

Detected when leaving (track `det`). Smoking destroyers: 11% detected at the last sample inside, 11% at the first sample outside, 16% at some point in the next 10 s. Those that stayed: 13% before the smoke went, 24% at the first sample without it, 40% within 10 s. Sheltering cruisers: leaving 13% -> 17% -> 33%; staying 15% -> 25% -> 37%.

- Score state drives it, not leaving: smoking destroyers that left died in the next 30 s at 5.6 per 100 when 50+ behind and 2.2 when not. Inside a standing smoke: 8.6 vs 2.2 per 30 s.
- A destroyer that leaves its smoke usually leaves unseen (16% detected within 10 s). One that sits until the smoke clears is seen more often (40%).
- Cruisers lose more health in the 30 s after leaving (6.7%) or after dispersal (8.1%) than per 30 s inside (3.4%).

**Top 6 or Shared:** Shared. Leaving against staying shows no clear gap for Top 6 or for Rest (smoking destroyers, died or lost a third: Top 6 3.4 left vs 7.7 stayed, -21.1 to +5.6; Rest 7.4 vs 5.3, -4.5 to +9.1). Where they died: Top 6 smoking destroyers 10 of 33 inside a standing smoke, Rest 43 of 104; counts only, not tested.

**Clans:** ships that died within 30 s of leaving a standing smoke: Top 6: BONKZ 3, HTDOG 2, KITE 1, RESIN 1 | Rest: MACH 4, HFANS 3, UYSC 3, KITED 3, BONKY 2, OGF 2, BTLST 2, MANBA 1, SCCC2 1, NGA 1, INCA 1, RMN 1, EPOXY 1, RSR 1, -BN- 1, PFANS 1, MZY 1.

**Could not be done / proxy:** The smoke outline is the final laid path, so a ship counts as inside a puff a few seconds before that puff exists. Per-puff end times are worked out from the emission time, not read from the replay. Positions every 2 s: a ship that dips out and back inside one step is not seen. Leavers and stayers are different ships in different situations (leavers are mostly destroyers moving on early, stayers sat still), so the comparison is a description, not a test of "should I leave".

**Verdict:** Lead. "Died in smoke" mostly means "died after leaving it", and neither leaving nor the smoke running out is the risky moment; the score state is.

**Changed from round 5:**
- Proxy 1, died just after the smoke cleared: 27 -> 5 (-22). Tracks: only 5 of the 124 died after the smoke dispersed around them. Of round 5's 27, the track puts left, over 30 s 19, smoke dispersed 4, never inside 3, left, 30 s or less 1: most had sailed out long before.
- Proxy 2, died behind rather than inside: 25 -> 8 (-17). Tracks: 8 were never inside the outline. Of round 5's 25 "behind", the track puts left, over 30 s 9, never inside 8, left, 30 s or less 4, inside 3, smoke dispersed 1.
- Died inside the smoke (batch "inside"): 99 -> 29 (-70). The batch "inside" means concealed by the smoke at some point. By position at death: left, over 30 s 48, inside 26, left, 30 s or less 21, smoke dispersed 4.
- Deaths after leaving a standing smoke: could not be told -> 82. New: tracks.
- Leaving against staying, rates: could not be done -> 3.1 vs 3.6 per 100 (smoking destroyers, next 30 s). New: tracks.
- Deaths of ships at risk in destroyer smokes: 124 -> 201 (+77). Track deaths in the smoke window; the batch list misses ships that died unseen or were lit throughout.

### A2. Radar deaths with the full radar log

**Answer:** Radar is on far more deaths than round 5 could see. Of the 124 deaths in destroyer smokes, 65 (52%) were radar-lit in their last 40 s and 56 in their last 20 s; round 5 had 19 (strict) or 45 (broad). The radar ship is nearly always a cruiser sitting near the edge of its range (median 89% of range, 9.3 km), Moskva most of all. Destroyer smokes with a covered ship radar-lit lose 20.9 ships per 100, against 6.3 without.

**Numbers:**

Round 5's death list (124 batch smoke deaths in destroyer smokes):

- Radar-lit in the last 40 s: 65 of 124 (52.4%). In the last 20 s: 56 (45.2%).
- Top 6 10 of 29 deaths, Rest 55 of 95 (last 20 s: 7 and 49).
- Who died: smoking destroyer 41 of 69, sheltering cruiser 22 of 48, other ship 2 of 7.
- By map (radar-lit deaths of all deaths there): Sleeping Giant 20 of 28, Okinawa 12 of 18, Sea of Fortune 9 of 16, Loop 8 of 15, Hotspot 7 of 18, Land of Fire 7 of 18, Mountain Range 2 of 11. By nearest cap: Okinawa C 7, Sleeping Giant A 7, Sleeping Giant B 5, Sleeping Giant C 5, Sea of Fortune C 4, Hotspot D 4, Okinawa A 4, Loop C 3.
- By time the smoke was laid: 0-5 min 12, 5-10 min 29, 10-15 min 21, 15-20 min 3. By score at activation: behind 50+ 37 of 64, level 17 of 36, ahead 50+ 11 of 24.
- Radar ship (named for 64 of 65): cruiser 56, destroyer 8. Moskva 24, Des Moines 7, Brisbane 6, Gdańsk 5, Petropavlovsk 5, Minotaur 4, San Martín 3, Salem 3, Småland 2, Worcester 2, Svea 1, Stalingrad 1, Yueyang 1.
- Distance from the radar ship: median 9.3 km (quarter marks 7.9 and 10.6; range 2.5 to 11.8). As a share of that ship's radar range: median 89% (quarter marks 77% and 95%); 45 of 64 beyond 80% of range, 5 under 60%. Cruiser radars: median 9.5 km, 89% of range (n 56). Destroyer radars: median 7.2 km, 85% of range (n 8, small n).
- Ambiguous (more than one enemy radar had the ship in range): 2 of 65 (3.1%).
- Radar play from smoke (the radar ship was itself inside a smoke): 2 of 64 (3.1%).
- Where the dying ship was while lit: the log places 21 of 65 inside the smoke; the rest were lit outside it (behind it, or after leaving).
- How long it had been lit: median 14.0 s (quarter marks 7.2 and 25.2; longest 41.4). Under 10 s: 25; 20 s or more: 24. Still lit at the moment of death: 34 of 65; for the rest the radar had ended a median 11.0 s earlier.

Every ship at risk in a destroyer smoke whose track shows a death between activation and 20 s after dispersal (201):

- Radar-lit in the last 40 s: 92 of 201 (45.8%). In the last 20 s: 79 (39.3%).
- Top 6 25 of 55 deaths, Rest 67 of 146 (last 20 s: 18 and 61).
- Who died: smoking destroyer 68 of 137, sheltering cruiser 22 of 57, other ship 2 of 7.
- By map (radar-lit deaths of all deaths there): Sleeping Giant 26 of 39, Hotspot 14 of 37, Okinawa 12 of 23, Sea of Fortune 12 of 21, Land of Fire 11 of 29, Loop 10 of 27, Mountain Range 7 of 25. By nearest cap: Sleeping Giant A 9, Hotspot D 7, Okinawa C 7, Land of Fire A 6, Mountain Range C 6, Sleeping Giant C 6, Sleeping Giant D 6, Okinawa A 5.
- By time the smoke was laid: 0-5 min 14, 5-10 min 43, 10-15 min 32, 15-20 min 3. By score at activation: behind 50+ 49 of 97, level 24 of 55, ahead 50+ 19 of 49.
- Radar ship (named for 91 of 92): cruiser 80, destroyer 11. Moskva 26, Brisbane 10, Petropavlovsk 10, Des Moines 10, San Martín 7, Gdańsk 6, Salem 5, Minotaur 4, Stalingrad 3, Svea 3, Småland 3, Yueyang 2, Worcester 2.
- Distance from the radar ship: median 9.0 km (quarter marks 7.7 and 10.4; range 2.5 to 11.9). As a share of that ship's radar range: median 88% (quarter marks 76% and 95%); 62 of 91 beyond 80% of range, 8 under 60%. Cruiser radars: median 9.3 km, 88% of range (n 80). Destroyer radars: median 7.0 km, 88% of range (n 11, small n).
- Ambiguous (more than one enemy radar had the ship in range): 5 of 92 (5.4%).
- Radar play from smoke (the radar ship was itself inside a smoke): 3 of 91 (3.3%).
- Where the dying ship was while lit: the log places 22 of 92 inside the smoke; the rest were lit outside it (behind it, or after leaving).
- How long it had been lit: median 13.6 s (quarter marks 7.9 and 24.8; longest 41.9). Under 10 s: 32; 20 s or more: 30. Still lit at the moment of death: 42 of 92; for the rest the radar had ended a median 10.5 s earlier.

Death by death against round 5 (124 deaths): strict 19, broad 45, radar log 65. All 19 strict deaths are in the log; the log adds 46. 44 of the 45 broad deaths are in the log, 1 is not; the log adds 21 that broad missed. Check: for the strict deaths the log names the same radar ship in 18 of 19 and gives the same distance (median 10.1 km vs 10.0 km).

Rates per 100 destroyer smokes (deaths = batch list, so the columns compare with round 5):

| reading | n (Top 6 / Rest) | deaths | per 100 [95%] | Top 6 | Rest | Top 6 minus Rest |
|---|---|---|---|---|---|---|
| radar log: a covered ship radar-lit while the smoke stood: with | 388 (149 / 239) | 81 | 20.9 [16.1 to 27.0] | 12.1 | 26.4 | -21.2 to -6.8 * |
| radar log: a covered ship radar-lit while the smoke stood: without | 686 (238 / 448) | 43 | 6.3 [4.2 to 9.0] | 4.6 | 7.1 | -7.4 to +2.4 |
| radar log: lit while placed inside this smoke: with | 120 (44 / 76) | 31 | 25.8 [16.4 to 37.4] | 13.6 | 32.9 | -34.3 to +2.9 |
| radar log: lit while placed inside this smoke: without | 954 (343 / 611) | 93 | 9.7 [7.4 to 12.7] | 6.7 | 11.5 | -9.4 to -0.4 * |
| round 5 strict: with | 120 (44 / 76) | 30 | 25.0 [16.5 to 36.4] | 13.6 | 31.6 | -34.3 to +1.3 |
| round 5 strict: without | 954 (343 / 611) | 94 | 9.9 [7.5 to 13.1] | 6.7 | 11.6 | -9.8 to -0.6 * |
| round 5 broad: with | 297 (111 / 186) | 83 | 27.9 [22.2 to 35.2] | 17.1 | 34.4 | -25.9 to -8.1 * |
| round 5 broad: without | 777 (276 / 501) | 41 | 5.3 [3.3 to 7.9] | 3.6 | 6.2 | -6.9 to +1.0 |

With radar minus without: log, any covered ship: +14.6 (+9.4 to +20.8 *); log, lit inside the smoke: +16.1 (+7.3 to +28.2 *); round 5 strict: +15.1 (+6.9 to +27.1 *); round 5 broad: +22.7 (+16.5 to +30.0 *).

By score state at activation (radar log, a covered ship radar-lit while the smoke stood):

| reading | n (Top 6 / Rest) | deaths | per 100 [95%] | Top 6 | Rest | Top 6 minus Rest |
|---|---|---|---|---|---|---|
| radar log: a covered ship radar-lit while the smoke stood: with, ahead 50+ | 114 (58 / 56) | 15 | 13.2 [6.8 to 21.2] | 10.3 | 16.1 | -18.8 to +9.5 |
| radar log: a covered ship radar-lit while the smoke stood: without, ahead 50+ | 258 (109 / 149) | 9 | 3.5 [1.7 to 6.0] | 2.8 | 4.0 | -5.6 to +2.2 |
| radar log: a covered ship radar-lit while the smoke stood: with, level | 168 (66 / 102) | 26 | 15.5 [10.6 to 22.0] | 6.1 | 21.6 | -24.5 to -7.9 * |
| radar log: a covered ship radar-lit while the smoke stood: without, level | 257 (95 / 162) | 10 | 3.9 [1.6 to 6.3] | 2.1 | 4.9 | -6.7 to +1.2 |
| radar log: a covered ship radar-lit while the smoke stood: with, behind 50+ | 106 (25 / 81) | 40 | 37.7 [27.8 to 47.7] | 32.0 | 39.5 | -24.4 to +8.4 |
| radar log: a covered ship radar-lit while the smoke stood: without, behind 50+ | 171 (34 / 137) | 24 | 14.0 [8.2 to 21.0] | 17.6 | 13.1 | -14.3 to +17.0 |

With minus without: ahead 50+: +9.7 (+2.1 to +17.6 *); level: +11.6 (+6.3 to +18.8 *); behind 50+: +23.7 (+13.1 to +33.8 *).

Same split with track deaths (every ship at risk that died between activation and 20 s after dispersal):

| reading | n (Top 6 / Rest) | deaths | per 100 [95%] | Top 6 | Rest | Top 6 minus Rest |
|---|---|---|---|---|---|---|
| radar log: with (track deaths) | 388 (149 / 239) | 112 | 28.9 [23.7 to 34.6] | 22.8 | 32.6 | -21.1 to -0.1 * |
| radar log: without (track deaths) | 686 (238 / 448) | 89 | 13.0 [9.7 to 17.6] | 8.8 | 15.2 | -14.2 to -0.1 * |
| radar log: with, ahead 50+ (track deaths) | 114 (58 / 56) | 26 | 22.8 [13.5 to 32.5] | 20.7 | 25.0 | -23.2 to +12.6 |
| radar log: without, ahead 50+ (track deaths) | 258 (109 / 149) | 23 | 8.9 [6.0 to 13.2] | 7.3 | 10.1 | -10.5 to +2.2 |
| radar log: with, level (track deaths) | 168 (66 / 102) | 33 | 19.6 [14.6 to 25.9] | 13.6 | 23.5 | -20.3 to -1.6 * |
| radar log: without, level (track deaths) | 257 (95 / 162) | 22 | 8.6 [5.0 to 12.6] | 5.3 | 10.5 | -12.2 to +2.7 |
| radar log: with, behind 50+ (track deaths) | 106 (25 / 81) | 53 | 50.0 [39.8 to 60.2] | 52.0 | 49.4 | -27.0 to +33.3 |
| radar log: without, behind 50+ (track deaths) | 171 (34 / 137) | 44 | 25.7 [16.5 to 37.7] | 23.5 | 26.3 | -21.8 to +10.5 |

With minus without: all: +15.9 (+10.8 to +20.8 *); ahead 50+: +13.9 (+3.0 to +23.7 *); level: +11.1 (+4.0 to +18.0 *); behind 50+: +24.3 (+9.8 to +36.2 *).

Smoke by smoke, 1,074 destroyer smokes:

| round 5 reading | radar log reading | round 5 smokes | log smokes | in both | missed by round 5 | over-counted by round 5 |
|---|---|---|---|---|---|---|
| round 5 strict | lit while placed inside this smoke | 120 | 120 | 117 | 3 | 3 |
| round 5 strict | a covered ship radar-lit while the smoke stood | 120 | 388 | 117 | 271 | 3 |
| round 5 broad | a covered ship radar-lit while the smoke stood | 297 | 388 | 275 | 113 | 22 |
| round 5 broad | lit while placed inside this smoke | 297 | 120 | 119 | 1 | 178 |

- Round 5 strict is the same thing as "lit while inside this smoke" in the log (117 of 120 smokes shared). It was right, just narrow.
- Round 5 broad missed 113 smokes where a covered ship was lit while out of cover. Those lose only 6.2 per 100 (7 deaths in 113), which is why the log reading separates deaths a little less sharply than broad did.
- Radar reaches Top 6 and Rest equally often: log, any covered ship: 38.5% vs 34.8% (-5.6 to +10.8); log, inside the smoke: 11.4% vs 11.1% (-4.4 to +4.4).

Calm smokes (neither 50+ behind at activation nor radar): round 5 definition 585 smokes, 17 deaths, 2.9 per 100. With the radar log (no covered ship radar-lit while the smoke stood): 515 smokes, 19 deaths, 3.7 per 100 [2.2 to 5.6] (Top 6 2.5, Rest 4.5, -5.4 to +0.9). The other 559 smokes hold 105 of the 124 deaths. Counting track deaths instead: 45 deaths, 8.7 per 100 in calm smokes, of 201 in all.

**Top 6 or Shared:** The condition is Shared: radar reaches both groups equally often. The outcome is a Top 6 pattern: with a covered ship radar-lit, Top 6 lose 12.1 per 100 and Rest 26.4 (-21.2 to -6.8 *); at level score 6.1 vs 21.6 (-24.5 to -7.9 *). Once 50+ behind and radar-lit there is no gap (32.0 vs 39.5, -24.4 to +8.4). Radar-lit deaths in the batch list: Top 6 10 of 29, Rest 55 of 95.

**Clans:**
- Radar-lit deaths, batch list (65): Top 6: RESIN 4, BONKZ 3, KITE 1, VRTUS 1, HTDOG 1 | Rest: EPOXY 7, UYSC 6, HFANS 6, BTLST 5, 5D 5, REEEE 4, -BN- 3, RSR 3, KITED 3, MZY 3, SCCC2 2, PFANS 2, MANBA 1, KM 1, KSE 1, INCA 1, MACH 1, MACHX 1.
- Radar-lit deaths, all track deaths (92): Top 6: BONKZ 10, RESIN 9, VRTUS 3, KITE 1, HTDOG 1, H-SR 1 | Rest: EPOXY 8, BTLST 6, UYSC 6, HFANS 6, 5D 5, KSE 4, RSR 4, MZY 4, REEEE 4, -BN- 3, KITED 3, MACH 2, NGA 2, SCCC2 2, PFANS 2, MANBA 1, KM 1, KSC 1, INCA 1, BONKY 1, MACHX 1.

**Could not be done / proxy:** The replay says a ship is radar-lit, not by whom. The log names the enemy radar that had it in range at that time; where two did, the row is marked ambiguous and the most recent, nearest one is used here. One lit death has no radar in range in the log. "Lit in its last 40 s" does not mean radar caused the death: 31 of the 65 were no longer lit when they died. Distance is at the start of the lit span.

**Verdict:** Lead. Radar-lit deaths are half of all deaths in destroyer smokes, not one in seven; the radar is a cruiser near maximum range; almost none are radar plays from smoke.

**Changed from round 5:**
- Radar deaths of 124, last 40 s: 19 strict / 45 broad -> 65. Better data: the full radar log sees ships lit outside the smoke and spans the per-smoke rows missed.
- Share of deaths radar-lit: 15% strict / 36% broad -> 52%. Same reason.
- Top 6 / Rest radar deaths: 3 / 16 strict, 5 / 40 broad -> 10 / 55. Same reason.
- Deaths with the radar ship and distance known: 19 -> 64 (+45). The log attributes every lit span.
- Median distance from the radar ship, km: 10.0 -> 9.3 (-0.7). More deaths; the extra ones are a little closer.
- Median distance as a share of radar range, %: 85.0 -> 88.8 (+3.8). More deaths; same picture (edge of range).
- Radar ship class: cruiser 16, destroyer 3 -> cruiser 56, destroyer 8. More deaths.
- Moskva as the radar ship: 6 -> 24 (+18). More deaths.
- Smokes with radar: 120 strict / 297 broad -> 388 (any covered ship lit while the smoke stood); 120 (lit inside the smoke). The log counts ships lit out of cover too.
- Deaths per 100 with / without radar: 25.0 / 9.9 strict; 27.9 / 5.3 broad -> 20.9 / 6.3 (any covered ship); 25.8 / 9.7 (inside the smoke). The strict reading is confirmed. The wide log reading adds smokes where a ship was lit out of cover, which are less deadly.
- Calm smokes: 585 smokes, 17 deaths, 2.9 per 100 -> 515 smokes, 19 deaths, 3.7 per 100. Radar taken from the log: 70 fewer smokes count as radar-free.
- Radar plays from smoke, time lit, ambiguity: not available -> 2 of 64 from smoke; lit a median 14.0 s; 2 ambiguous. New fields.
- Time-of-game split: strict 4 / 7 / 5 / 3 -> 12 / 29 / 21 / 3. More deaths; and 17 smokes in two 15-minute-clock games had their times corrected in r5lib.

## Figures (working, in `round5b/figures/`)

- `n2-danger-<map>` (7): died or hurt per 100 by area, top row keyed on the smoke centre, bottom row keyed on where the ship was hit.
- `n2-deaths-<map>` (7): death positions, filled = inside the smoke outline.
- `n2-leaving-the-smoke`: where ships died, and leaving against staying.
- `n2-radar-deaths`: distance to the radar ship as a share of range, and rates with and without radar.

