# Round 5b, worker n4: the page 1 carry-over claims, re-tested

Batch `output/20261117-230933` (smoke-signals 0.4.0): 1,547 smokes, 171 games, 30 clans. Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS (110 team-games); Rest = everyone else (232 team-games). Intervals are 95%, whole clans resampled; * = excludes zero. Minimum n 8; 8 to 14 is small n. Everything is association, not cause.

Each claim is done in two layers. **Layer A** reruns the atlas / round 4 computation on the new batch (the smoke fields are identical, so it must give the same numbers). **Layer B** re-tests the claim with the new timelines: ship tracks every 2 s, the cap ownership timeline, and the radar log.

### N4-1. Early smoke distance short of the cap

**Answer:** Yes, it holds, and it holds on the ships as well as on the smoke outline. The destroyer was inside a cap when it pressed smoke in 11% of early Harugumo, Somers and Gearing smokes and a typical 2.6 km outside the nearest cap edge; the covered cruiser stayed a typical 3.2 km outside while the smoke stood. The cap in question was usually still neutral (71%), and somebody was capturing it while the smoke stood in 76% of cases: the smoke is short of the cap, but the cap is live.

**Numbers:**

Layer A, same definition, new batch (early smokes by Harugumo, Somers and Gearing; the batch field is smoke edge to contested cap edge, averaged over the smoke's life):

| Number | Atlas / round 4 | New batch, clock bug still in | New batch, clock corrected | Status |
|---|---|---|---|---|
| Early smokes by the three ships (n) | 187 | 187 | 188 | clock fix |
| Laid inside a cap | 14% | 14% | 14% | unchanged |
| Median distance outside the cap edge | 1.8 km | 1.8 km | 1.7 km | clock fix |

Clock fix: 2 games ran on a 15-minute clock, so rounds 3 to 5 read their 17 smokes 300 s late. The library now corrects this: 4 more smokes count as early (4 destroyer smokes, 1 of them by the three ships) and none stop being early. The middle column puts the bug back and reproduces the atlas; the right column is the corrected number, and layer B uses the corrected groups.

New interval for these two: inside a cap 9 to 21%, median distance 1.4 to 2.3 km (27 of 188 smokes inside).

Layer B, re-tested with ship tracks and the cap timeline. Four groups of early smokes; "early cruiser smoke" is the round 5 definition (any destroyer, first 5 minutes, covers a cruiser):

| Measure | Three ships, early (round 3 group) | Early cruiser smoke, cruiser inside | Early cruiser smoke, cruiser screened | All early destroyer smokes |
|---|---|---|---|---|
| Smokes (Top 6 / Rest) | 188 (68 / 120) | 153 (67 / 86) | 73 (18 / 55) | 306 (103 / 203) |
| Smoke outline inside a cap (batch field) | 14% (9 to 21) | 12% (7 to 18) | 33% (20 to 48) | 26% (20 to 33) |
| Smoke edge to contested cap edge, median (batch field) | 1.7 km | 1.7 km | 1.1 km | 1.4 km |
| Smoker inside a cap when it pressed smoke | 11% (6 to 18) | 12% (7 to 19) | 25% (13 to 37) | 20% (14 to 28) |
| Smoker inside a cap at the end of laying | 10% (5 to 18) | 8% (3 to 13) | 29% (15 to 44) | 17% (12 to 24) |
| Smoker to nearest cap edge at activation, median | 2.6 km (2.1 to 2.9) | 2.6 km (2.1 to 3.0) | 1.8 km (0.9 to 2.3) | 2.0 km (1.4 to 2.5) |
| Smoker to nearest cap edge at the end of laying, median | 2.4 km (2.0 to 2.7) | 2.2 km (1.9 to 2.6) | 1.4 km (0.5 to 2.4) | 1.9 km (1.4 to 2.2) |
| Smoker on the own-spawn side of that cap at activation | 91% | 91% | 90% | 90% |
| Covered cruiser to nearest cap edge while the smoke stood, median | 3.2 km (2.8 to 3.5; n 173) | 2.8 km (2.4 to 3.2; n 153) | 4.0 km (3.0 to 4.7; n 72) | 3.1 km (2.6 to 3.4; n 225) |
| Covered cruiser inside a cap at any time while the smoke stood | 25% (19 to 34) | 27% (19 to 35) | 21% (11 to 33) | 25% (19 to 31) |
| Covered cruiser inside a cap for most of that time | 9% | 10% | 6% | 9% |
| Contested cap at activation: neutral / ours / theirs | 71% / 8% / 21% | 69% / 8% / 22% | 69% / 10% / 21% | 67% / 11% / 23% |
| Contested cap being captured while the smoke stood: by us / by the enemy / by nobody | 54% / 46% / 24% | 56% / 40% / 25% | 50% / 57% / 19% | 50% / 45% / 26% |

- The outline and the ships agree. Of the 187 three-ship smokes with a track, 145 have both the outline and the smoker outside every cap, 18 have both inside, 15 have the outline short but the smoker in a cap at the start or end of laying, and 9 the reverse.
- The smoker does not close on the cap while laying: it is nearer the cap at the end of laying in 49% of smokes, about half. It travels a median 3.8 km while laying and ends no nearer the cap than it started.
- The cruiser sits further back than the destroyer: 3.2 km against 2.6 km. Measured to the contested cap it is 3.9 km (round 3 had 3.8 km from the one snapshot per smoke). Only while it is actually inside the smoke: 2.4 km. In 25% of smokes a covered cruiser did enter a cap at some point before the smoke cleared (about 2.5 minutes), but it spent most of that time in a cap in only 9%.
- Screened is the exception, as in round 5: when the cruiser is behind the smoke rather than in it, the smoke is nearer the cap (33% inside, smoker in a cap 25% at activation) and the cruiser is further away (4.0 km).
- Checks. Track position against the round 5 snapshot at the fully-laid moment, same smokes: median 2 m apart, 100% within 300 m (n 175). Smoker in a cap from the snapshot: 10%, from the track at the end of laying: 10%. Cap owner at activation, timeline against the batch field: 100% the same. My own outline distance from the laid path is within a median 173 m of the batch field and agrees on inside / outside for 97% of smokes.

**Top 6 or Shared:** Shared. Everyone lays the early smoke short. Outline inside a cap: Top 6 9% vs Rest 18% (-20 to +2); smoker distance at activation 2.8 km vs 2.3 km (-0.5 to +1.5 km); cruiser distance 3.1 km vs 3.2 km (-0.8 to +0.9 km). One gap is clear, and it points the same way as the rule: the Top 6 smoker is inside a cap when it presses smoke even less often, 4% vs 15% (-20 to -3 *); on all early destroyer smokes 11% vs 25% (-26 to -2 *). By the end of laying the gap is gone (7% vs 12%, -16 to +8).

**Clans:** the 188 three-ship early smokes: Top 6: RESIN 20, H-SR 17, BONKZ 13, KITE 8, VRTUS 7, HTDOG 3 | Rest: -BN- 13, EPOXY 12, KSC 11, REEEE 10, HFANS 10, MZY 7, BONKY 6, MACHX 6, BTLST 5, 5D 5, PN 5, PFANS 5, NGA 5, RSR 5, OGF 4, INCA 4, UYSC 2, KM 2, KITED 1, SCCC2 1, RMN 1. The 21 with the smoker inside a cap at activation: Top 6: H-SR 2, VRTUS 1 | Rest: 5D 3, RSR 2, BTLST 2, PN 2, PFANS 1, INCA 1, BONKY 1, EPOXY 1, SCCC2 1, -BN- 1, REEEE 1, KM 1, MZY 1.

**Could not be done / proxy:** One smoke in the single-replay game (KSC against -BN-) has no own-team track for the smoker and is left out of layer B (187 of 188; cruiser tracks for 173, the rest cover no cruiser). The smoke shape is the final laid path, so "inside the smoke" is slightly generous while it is still being laid. The batch distance is to the contested cap; ship distances are given to the nearest cap, which is the stricter test of "short of a cap".

**Verdict:** Keep

**Changed from the atlas / round 4:**

- Layer A: 1 of 3 numbers unchanged (old -> new identical): Laid inside a cap 14%. Moved: Early smokes by the three ships (n): 187 -> 187 with the clock bug still in -> 188 corrected (clock fix); Median distance outside the cap edge: 1.8 km -> 1.8 km with the clock bug still in -> 1.7 km corrected (clock fix). Why: same smoke fields, same computation.
- Layer B (new, no old value unless noted): smoker inside a cap at activation 11% and at the end of laying 10% (outline: 14%); smoker 2.6 km then 2.4 km outside the nearest cap (outline: 1.7 km, +0.8 km; a ship is a point, the outline reaches about half a kilometre further); cruiser to the contested cap 3.8 km -> 3.9 km (one snapshot -> average over the smoke's life); cruiser inside a cap 4% of partners at the snapshot -> 9% of smokes for most of the time, 25% at any time. Why: better data (continuous tracks and cap timeline). The claim itself is unchanged.

### N4-2. Radar cruiser inside early destroyer smokes

**Answer:** The headline stands: a radar cruiser is inside 59% of Top 6 early destroyer smokes against 35% for the Rest. But the radar log shows what that cruiser does there: it ran its radar from the smoke in only about a third of those smokes, and that share is the same for both groups (33% vs 30%). So the Top 6 difference is having the cruiser in the smoke, not pressing radar from it. "Inside goes with the cap being taken" survives the cap timeline but at about half the size: 59% vs 37% on the nearest cap, not 58% vs 14%.

**Numbers:**

Layer A, same definition, new batch:

| Number | Atlas / round 4 | New batch, clock bug still in | New batch, clock corrected | Status |
|---|---|---|---|---|
| All early destroyer smokes, radar cruiser inside | 60% (61 of 102) vs 35% (70 of 200) | 60% (61 of 102) vs 35% (70 of 200) | 59% (61 of 103) vs 35% (71 of 203) | clock fix |
| Gap | +25 | +25 | +24 | clock fix |
| Gap interval | +13 to +36 | +13 to +36 | +12 to +35 | clock fix |
| Sleeping Giant | 47% vs 59% | 47% vs 59% | 47% vs 59% | unchanged |
| Hotspot | 87% vs 38% | 87% vs 38% | 87% vs 38% | unchanged |
| Harugumo, Somers, Gearing only | 82% vs 51% | 82% vs 51% | 82% vs 52% | clock fix |
| Three ships, gap interval | +15 to +46 | +17 to +47 | +16 to +46 | same data, interval end moved (resampling redrawn); then clock fix |
| Cap won after: radar cruiser inside vs covered, not inside (three ships) | 58% (n 117) vs 14% (n 29) | 58% (n 117) vs 14% (n 29) | 58% (n 118) vs 14% (n 29) | clock fix |
| Cap taken, all early destroyer smokes: radar cruiser inside vs not | 61% (of 120) vs 31% (of 150) | 61% (of 120) vs 31% (of 150) | 61% (of 120) vs 31% (of 153) | clock fix |

Clock fix: 2 games ran on a 15-minute clock, so rounds 3 to 5 read their 17 smokes 300 s late. The library now corrects this: 4 more smokes count as early (4 destroyer smokes, 1 of them by the three ships) and none stop being early. The middle column puts the bug back and reproduces the atlas; the right column is the corrected number, and layer B uses the corrected groups.

Second way for the headline (counted straight from the raw list of ships in each smoke and the roster, not from the library flag): 61 and 71 smokes. Same.

Layer B, the ladder from the radar log. "Ran radar from it" = that cruiser activated radar while the smoke stood, with the smoke listed as the one it stood in, or with its position inside the smoke. All early destroyer smokes:

| Step (all maps) | Top 6 | Rest | Gap in points (interval) | Such smokes per team-game (interval of the gap) |
|---|---|---|---|---|
| Radar cruiser inside (batch field) | 59% (61 of 103) | 35% (71 of 203) | +24 (+12 to +35 *) | 0.55 vs 0.31 (+0.04 to +0.44 *) |
| Inside and ran radar from it | 19% (20 of 103) | 10% (21 of 203) | +9 (-0 to +17) | 0.18 vs 0.09 (-0.01 to +0.20) |
| Ran radar from it and lit an enemy | 18% (19 of 103) | 8% (17 of 203) | +10 (-1 to +18) | 0.17 vs 0.07 (-0.01 to +0.20) |
| Ran radar from it and lit an enemy destroyer | 16% (16 of 103) | 7% (15 of 203) | +8 (-0 to +15) | 0.15 vs 0.06 (-0.01 to +0.15) |

- Of the 132 early smokes with a radar cruiser inside, the cruiser ran radar from the smoke in 41 (37 on the strict test, where the log itself lists the smoke). Top 6 33% of 61, Rest 30% of 71 (-18 to +18). It lit an enemy in 36 and an enemy destroyer in 31.
- When it did run radar, it lit 1.5 (Top 6) and 1.3 (Rest) enemy ships per smoke, 1.1 and 0.9 of them destroyers. No clear gap. 3 of 61 lit records could also belong to another radar.
- The batch's own "radar run from inside" flag marks 34 of the 132; the log finds all of those and 7 more (most likely because the batch flag also needs the ship to be undetected at that moment). Among the 174 early smokes with no radar cruiser inside, 6 still saw a radar pressed from inside (a radar destroyer, or a cruiser the batch put behind the smoke).

Per map, with the number of clans behind each group (Top 6 clans / Rest clans):

| Map | Clans | Inside: Top 6 | Inside: Rest | Gap (interval) | Ran radar from it: Top 6 | Rest | Gap (interval) | Lit an enemy destroyer (counts) |
|---|---|---|---|---|---|---|---|---|
| All maps | 6 / 23 | 59% (61 of 103) | 35% (71 of 203) | +24 (+12 to +35 *) | 19% (20 of 103) | 10% (21 of 203) | +9 (-0 to +17) | 16 of 103 vs 15 of 203 |
| Sleeping Giant | 6 / 16 | 47% (15 of 32) | 59% (22 of 37) | -13 (-40 to +18) | 16% (5 of 32) | 11% (4 of 37) | +5 (-12 to +19) | 1 of 32 vs 4 of 37 |
| Hotspot | 6 / 19 | 87% (20 of 23) | 38% (18 of 48) | +50 (+31 to +69 *) | 22% (5 of 23) | 12% (6 of 48) | +9 (-10 to +37) | 5 of 23 vs 4 of 48 |
| Mountain Range | 4 / 13 | 64% (9 of 14, small n) | 32% (8 of 25) | +32 (-5 to +73) | 36% (5 of 14, small n) | 8% (2 of 25) | +28 (+2 to +51 *) | 5 of 14 vs 2 of 25 |
| Land of Fire | 6 / 13 | 42% (5 of 12, small n) | 32% (8 of 25) | +10 (-23 to +48) | 8% (1 of 12, small n) | 8% (2 of 25) | +0 (-19 to +19) | 1 of 12 vs 1 of 25 |
| Loop | 5 / 16 | 40% (4 of 10, small n) | 22% (5 of 23) | +18 (-25 to +44) | 20% (2 of 10, small n) | 4% (1 of 23) | +16 (-11 to +39) | 2 of 10 vs 1 of 23 |
| Okinawa | 3 / 14 | 2 of 3 (too few) | 17% (4 of 23) | - | 0 of 3 (too few) | 13% (3 of 23) | - | 0 of 3 vs 1 of 23 |
| Sea of Fortune | 4 / 15 | 67% (6 of 9, small n) | 27% (6 of 22) | +39 (+15 to +60 *) | 22% (2 of 9, small n) | 14% (3 of 22) | +9 (-23 to +43) | 2 of 9 vs 2 of 22 |

Per map the "ran radar from it" counts are 0 to 6 smokes a side, so only the all-maps row should be read. Mountain Range is the one map with a starred gap (5 of 14 vs 2 of 25, small n).

"Inside goes with the cap being taken", old field against the cap timeline, same smokes. Cap taken = not ours at activation and ours at some time up to 60 s after the smoke cleared:

Three ships, radar cruiser inside against radar cruiser covered but not inside (the round 4 pair):

| Measure | Inside | Covered, not inside | Gap (interval) |
|---|---|---|---|
| Batch cap_won, all smokes (round 4, Module 2 number) | 58% (68 of 118) | 14% (4 of 29) | +44 (+30 to +54 *) |
| Batch cap_won, contested cap not ours at activation (round 4, Module 3 number) | 60% (64 of 106) | 14% (4 of 28) | +46 (+31 to +57 *) |
| Cap timeline: contested cap not ours at activation, ours within 60 s after the smoke cleared | 46% (49 of 106) | 32% (9 of 28) | +14 (-4 to +29) |
| Cap timeline: nearest cap, same test | 59% (53 of 90) | 36% (8 of 22) | +22 (-0 to +41) |
| Cap timeline: contested cap, the batch window (10 s after) | 37% (39 of 106) | 29% (8 of 28) | +8 (-11 to +25) |

All early destroyer smokes, radar cruiser inside against none inside:

| Measure | Inside | None inside | Gap (interval) |
|---|---|---|---|
| Batch cap_won, all smokes (round 4, Module 2 number) | 58% (77 of 132) | 29% (50 of 174) | +30 (+22 to +38 *) |
| Batch cap_won, contested cap not ours at activation (round 4, Module 3 number) | 61% (73 of 120) | 31% (48 of 153) | +30 (+20 to +38 *) |
| Cap timeline: contested cap not ours at activation, ours within 60 s after the smoke cleared | 47% (56 of 120) | 32% (49 of 153) | +15 (+3 to +25 *) |
| Cap timeline: nearest cap, same test | 59% (60 of 102) | 37% (50 of 135) | +22 (+10 to +32 *) |
| Cap timeline: contested cap, the batch window (10 s after) | 37% (44 of 120) | 27% (41 of 153) | +10 (-1 to +21) |

- Why the old gap was so wide. The batch field `cap_won` does not follow one fixed cap. It counts any cap within gun range of a ship standing inside the smoke. A cruiser inside brings a longer gun range, so more caps count, so a capture is more likely to be credited. Every one of the 127 batch captures on early destroyer smokes is real (the timeline confirms 127), but only 55 are the smoke's contested cap and 60 its nearest cap. On a fixed cap the "not inside" group rises from 14% to 32% or 36%, and the gap roughly halves.
- What is left: on all early destroyer smokes the gap is clear on both fixed caps (+15 points contested, +22 nearest). On the three ships against "covered, not inside" it is +14 (-4 to +29) contested and +22 (-0 to +41) nearest: borderline, n 22 in the smaller group.
- Inside the two groups, nearest cap: Top 6 63% vs 50% (-8 to +34); Rest 55% vs 33% (+5 to +38 *). As in round 5 item A1, the link to the cap is mainly a Rest pattern.
- Pressing radar adds nothing visible on the cap: with a radar cruiser inside, nearest cap taken 61% (n 33) when it ran radar from the smoke against 58% (n 69) when it did not (-19 to +27). This matches atlas rule 3.

**Top 6 or Shared:** Top 6 for "a radar cruiser inside" (+24 points, +12 to +35 *; Sleeping Giant is still the one map the other way, not clear). Shared for what the cruiser does once inside: ran radar from it 33% vs 30% (-18 to +18). As a share of all early smokes, "inside and ran radar" is 19% vs 10% (-0 to +17) and "lit an enemy destroyer" 16% vs 7% (-0 to +15): same direction, intervals just touch zero.

**Clans:**

- Radar cruiser inside, all maps (61 + 71 smokes): Top 6: H-SR 20, RESIN 15, BONKZ 10, KITE 7, VRTUS 5, HTDOG 4 | Rest: HFANS 11, KSC 7, MACHX 7, EPOXY 7, BONKY 5, MZY 5, -BN- 5, PN 4, RSR 4, PFANS 3, INCA 3, BTLST 2, NGA 2, REEEE 2, UYSC 1, KITED 1, SCCC2 1, KM 1.
- Inside and ran radar from it, all maps (20 + 21): Top 6: H-SR 8, RESIN 6, HTDOG 2, KITE 2, VRTUS 1, BONKZ 1 | Rest: BONKY 4, MACHX 3, BTLST 2, RSR 2, HFANS 2, INCA 1, PN 1, EPOXY 1, SCCC2 1, KM 1, -BN- 1, MZY 1, REEEE 1.
- Ran radar and lit an enemy destroyer (16 + 15): Top 6: RESIN 6, H-SR 5, HTDOG 2, KITE 2, VRTUS 1 | Rest: BTLST 2, HFANS 2, INCA 1, PN 1, RSR 1, EPOXY 1, SCCC2 1, BONKY 1, KM 1, -BN- 1, MACHX 1, MZY 1, REEEE 1.
- Sleeping Giant, radar cruiser inside: Top 6: H-SR 6, RESIN 4, BONKZ 2, KITE 1, VRTUS 1, HTDOG 1 | Rest: EPOXY 5, HFANS 4, -BN- 3, MACHX 3, KSC 2, BONKY 2, KITED 1, SCCC2 1, PFANS 1. Ran radar from it: Top 6: H-SR 3, RESIN 1, BONKZ 1 | Rest: EPOXY 1, HFANS 1, SCCC2 1, BONKY 1.
- Hotspot, radar cruiser inside: Top 6: H-SR 7, BONKZ 5, RESIN 4, VRTUS 2, HTDOG 1, KITE 1 | Rest: KSC 4, MZY 3, PFANS 2, HFANS 2, BONKY 2, BTLST 1, PN 1, -BN- 1, EPOXY 1, REEEE 1. Ran radar from it: Top 6: RESIN 2, HTDOG 1, VRTUS 1, H-SR 1 | Rest: BONKY 2, BTLST 1, -BN- 1, REEEE 1, HFANS 1.
- Mountain Range, radar cruiser inside: Top 6: KITE 4, H-SR 3, RESIN 1, BONKZ 1 | Rest: RSR 2, PN 2, KSC 1, INCA 1, HFANS 1, -BN- 1. Ran radar from it: Top 6: KITE 2, H-SR 2, RESIN 1 | Rest: PN 1, RSR 1.
- Land of Fire, radar cruiser inside: Top 6: HTDOG 2, VRTUS 1, KITE 1, RESIN 1 | Rest: HFANS 3, MACHX 2, MZY 1, INCA 1, NGA 1. Ran radar from it: Top 6: HTDOG 1 | Rest: MACHX 2.
- Loop, radar cruiser inside: Top 6: RESIN 3, H-SR 1 | Rest: UYSC 1, INCA 1, MACHX 1, HFANS 1, EPOXY 1. Ran radar from it: Top 6: RESIN 2 | Rest: INCA 1.
- Okinawa, radar cruiser inside: Top 6: BONKZ 1, H-SR 1 | Rest: BTLST 1, RSR 1, NGA 1, MACHX 1. Ran radar from it: Top 6: none | Rest: BTLST 1, RSR 1, MACHX 1.
- Sea of Fortune, radar cruiser inside: Top 6: H-SR 2, RESIN 2, VRTUS 1, BONKZ 1 | Rest: REEEE 1, PN 1, RSR 1, KM 1, BONKY 1, MZY 1. Ran radar from it: Top 6: H-SR 2 | Rest: KM 1, BONKY 1, MZY 1.

**Could not be done / proxy:** The replay says a ship is radar-lit, not by whom; the log assigns it by range and time (3 of 61 records here could belong to a second radar). The smoke shape is the final laid path. 2 early smokes are in the single-replay game; they are kept (the radar log and cap timeline do not depend on the missing replay). Per-map counts for radar use are too small to rank maps.

**Verdict:** Keep (reword: the Top 6 difference is the cruiser being in the smoke; quote the cap link from the timeline, not 58% vs 14%)

**Changed from the atlas / round 4:**

- Layer A: 2 of 9 numbers unchanged (old -> new identical): Sleeping Giant 47% vs 59%; Hotspot 87% vs 38%. Moved: All early destroyer smokes, radar cruiser inside: 60% (61 of 102) vs 35% (70 of 200) -> 60% (61 of 102) vs 35% (70 of 200) with the clock bug still in -> 59% (61 of 103) vs 35% (71 of 203) corrected (clock fix); Gap: +25 -> +25 with the clock bug still in -> +24 corrected (clock fix); Gap interval: +13 to +36 -> +13 to +36 with the clock bug still in -> +12 to +35 corrected (clock fix); Harugumo, Somers, Gearing only: 82% vs 51% -> 82% vs 51% with the clock bug still in -> 82% vs 52% corrected (clock fix); Three ships, gap interval: +15 to +46 -> +17 to +47 with the clock bug still in -> +16 to +46 corrected (same data, interval end moved (resampling redrawn); then clock fix); Cap won after: radar cruiser inside vs covered, not inside (three ships): 58% (n 117) vs 14% (n 29) -> 58% (n 117) vs 14% (n 29) with the clock bug still in -> 58% (n 118) vs 14% (n 29) corrected (clock fix); Cap taken, all early destroyer smokes: radar cruiser inside vs not: 61% (of 120) vs 31% (of 150) -> 61% (of 120) vs 31% (of 150) with the clock bug still in -> 61% (of 120) vs 31% (of 153) corrected (clock fix). Why: same smoke fields; an interval end can move by a point or two when the resampling is drawn again (the point estimates are identical).
- Layer B: "radar cruiser inside" 59% vs 35% (+24) -> "inside and ran radar from it" 19% vs 10% (+9, -0 to +17) -> "and lit an enemy destroyer" 16% vs 7% (+8, -0 to +15). New: no old value. Why: better data (radar log).
- Layer B, cap taken, three ships, inside vs covered-not-inside: 58% vs 14% (+44, +32 to +54) -> 46% vs 32% (+14, -4 to +29) on the contested cap; 59% vs 36% (+22, -0 to +41) on the nearest cap. Difference in the gap: -30 and -21 points. All early destroyer smokes: 61% vs 31% (+30, +21 to +38) -> 47% vs 32% (+15, +3 to +25 *) contested; 59% vs 37% (+22, +10 to +32 *) nearest. Why: different definition made possible by better data (one fixed cap followed on the cap timeline, instead of any cap within gun range of a ship in the smoke).

### N4-3. Radar from smoke per team-game, and the return per play

**Answer:** Still right, and now on a direct count. The radar log has 155 radar presses made from inside an allied smoke: 0.77 per team-game for the Top 6 against 0.30 for the Rest, 2.6 times as often (the tag-based count said 2.5). The return per press is the same for both groups: 1.4 vs 1.3 enemy ships lit, 7.5k vs 5.8k damage on them while lit, no clear gap on anything.

**Numbers:**

Layer A, same definition, new batch (destroyer smokes whose primary purpose tag is a radar play):

| Number | Atlas / round 4 | New batch, clock bug still in | New batch, clock corrected | Status |
|---|---|---|---|---|
| Destroyer smokes tagged as a radar play | 96 (52 Top 6, 44 Rest) | 96 (52 Top 6, 44 Rest) | 96 (52 Top 6, 44 Rest) | unchanged |
| Per team-game | 0.47 vs 0.19 | 0.47 vs 0.19 | 0.47 vs 0.19 | unchanged |
| Gap interval | +0.14 to +0.40 | +0.14 to +0.40 | +0.14 to +0.40 | unchanged |
| Cap taken after cap-control smokes (caps not ours) | 58% (of 24) vs 58% (of 26) | 58% (of 24) vs 58% (of 26) | 58% (of 24) vs 58% (of 26) | unchanged |
| Three busiest maps | 69 of 96 (0.45, 0.40, 0.36 per team-game) | 69 of 96 (0.45, 0.40, 0.36 per team-game) | 69 of 96 (0.45, 0.40, 0.36 per team-game) | unchanged |
| Enemy ships lit per smoke with radar run (batch field) | 1.1 vs 1.1 | 1.1 vs 1.1 | 1.1 vs 1.1 | unchanged |

Clock fix: 2 games ran on a 15-minute clock, so rounds 3 to 5 read their 17 smokes 300 s late. The library now corrects this: 4 more smokes count as early (4 destroyer smokes, 1 of them by the three ships) and none stop being early. The middle column puts the bug back and reproduces the atlas; the right column is the corrected number, and layer B uses the corrected groups.

Layer B, plays per team-game counted three ways:

| Count | n (Top 6 / Rest) | Top 6 per team-game | Rest per team-game | Ratio | Gap (interval) |
|---|---|---|---|---|---|
| 1. Tag-based (old): destroyer smokes tagged as a radar play | 96 (52 / 44) | 0.47 | 0.19 | 2.5x | +0.28 (+0.14 to +0.40 *) |
| 1b. Tag-based, all smoker classes | 117 (64 / 53) | 0.58 | 0.23 | 2.5x | +0.35 (+0.20 to +0.46 *) |
| 2. Log: radar presses from inside any allied smoke | 155 (85 / 70) | 0.77 | 0.30 | 2.6x | +0.47 (+0.26 to +0.65 *) |
| 2a. ... inside a destroyer smoke | 129 (70 / 59) | 0.64 | 0.25 | 2.5x | +0.38 (+0.16 to +0.58 *) |
| 2a-i. ...... by another ship (a cruiser in the destroyer's smoke) | 107 (60 / 47) | 0.55 | 0.20 | 2.7x | +0.34 (+0.15 to +0.51 *) |
| 2a-ii. ...... by the smoker itself (a radar destroyer) | 22 (10 / 12) | 0.09 | 0.05 | 1.8x | +0.04 (-0.05 to +0.13) |
| 2b. ... inside a cruiser's own smoke | 24 (14 / 10) | 0.13 | 0.04 | 3.0x | +0.08 (-0.02 to +0.20) |
| 2c. ... inside another cruiser's smoke | 2 (1 / 1) | 0.01 | 0.00 | 2.1x | +0.00 (-0.01 to +0.03) |
| 3. Log: smokes with at least one radar press from inside | 149 (83 / 66) | 0.75 | 0.28 | 2.7x | +0.47 (+0.27 to +0.64 *) |
| 3a. ... destroyer smokes | 123 (68 / 55) | 0.62 | 0.24 | 2.6x | +0.38 (+0.18 to +0.56 *) |
| 3b. ... cruiser smokes | 26 (15 / 11) | 0.14 | 0.05 | 2.9x | +0.09 (-0.02 to +0.21) |
| Context: all radar presses, in smoke or not | 2426 (904 / 1522) | 8.22 | 6.56 | 1.3x | +1.66 (+0.04 to +2.98 *) |
| Context: radar presses not from smoke | 2271 (819 / 1452) | 7.45 | 6.26 | 1.2x | +1.19 (-0.36 to +2.37) |

- Tag against log on the same smokes: all 96 of the 96 tagged destroyer smokes have a radar press from inside in the log. The log finds 123 destroyer smokes with one, so 27 more than the tags: their primary tag is something else (cap_contest 9, reposition 6, damage 6, none 5, escape 1). Cruiser smokes: 21 tagged, 26 in the log.
- The Top 6 press radar somewhat more overall (8.2 vs 6.6 per team-game, 1.3x, +0.04 to +2.98 *), but far more of it from smoke: 9.4% of their radar presses against 4.6% (+2.5 to +7.0 * points). 49 of 110 Top 6 team-games (45%) have at least one radar press from smoke, against 50 of 232 (22%); the tags gave 38% and 17%.
- Who presses: Brisbane 33, Des Moines 32, Svea 29, Gdańsk 23, Minotaur 16, Petropavlovsk 5, Salem 4, Worcester 4. Cruisers 131, radar destroyers 24.

By map (radar presses from inside an allied smoke):

| Map | Presses (Top 6 / Rest) | Clans (Top 6 / Rest) | Per team-game, all clans | Top 6 | Rest | Gap (interval) | Old tag count (per team-game) |
|---|---|---|---|---|---|---|---|
| Sleeping Giant | 40 (21 / 19) | 4 / 10 | 0.62 | 0.78 | 0.51 | +0.26 (-0.17 to +0.70) | 29 (0.45) |
| Hotspot | 36 (18 / 18) | 6 / 10 | 0.58 | 1.00 | 0.41 | +0.59 (+0.14 to +1.19 *) | 25 (0.40) |
| Mountain Range | 27 (20 / 7) | 4 / 5 | 0.64 | 1.25 | 0.27 | +0.98 (+0.19 to +1.82 *) | 15 (0.36) |
| Land of Fire | 14 (small n) (6 / 8) | 3 / 5 | 0.28 | 0.38 | 0.24 | +0.14 (-0.28 to +0.83) | 9 (0.18) |
| Loop | 14 (small n) (11 / 3) | 5 / 3 | 0.30 | 0.85 | 0.09 | +0.76 (+0.21 to +1.40 *) | 6 (0.13) |
| Okinawa | 10 (small n) (1 / 9) | 1 / 6 | 0.28 | 0.17 | 0.30 | -0.13 (-0.52 to +0.26) | 7 (0.19) |
| Sea of Fortune | 14 (small n) (8 / 6) | 4 / 5 | 0.33 | 0.57 | 0.21 | +0.36 (-0.10 to +0.96) | 5 (0.12) |

Sleeping Giant, Hotspot, Mountain Range hold 103 of the 155 presses (66%; the tags had 69 of 96, 72%). They are also the three highest by rate. Per-map Top 6 rates rest on 1 to 6 clans and 1 to 21 presses: read the direction, not the size.

Return per play (one play = one radar press from inside an allied smoke, n 155):

| Per play | Top 6 | Rest | Interval of Top 6 minus Rest |
|---|---|---|---|
| Enemy ships lit per play | 1.41 (n 85) | 1.33 (n 70) | -0.32 to +0.40 |
| Plays that lit at least one enemy | 87% (n 85) | 79% (n 70) | -5 to +19 |
| Enemy destroyers lit per play | 0.81 (n 85) | 0.74 (n 70) | -0.17 to +0.27 |
| Plays that lit at least one enemy destroyer | 69% (n 85) | 66% (n 70) | -14 to +19 |
| Damage on lit enemies while lit, per play | 7,488 (n 85) | 5,814 (n 70) | -2,321 to +4,748 |
| ... shells, torpedoes and secondaries only | 6,624 (n 85) | 4,871 (n 70) | -2,118 to +4,503 |
| Plays with any damage on a lit enemy | 67% (n 85) | 60% (n 70) | -12 to +25 |
| Check: health the lit enemies lost while lit (ship tracks) | 5,971 (n 85) | 4,594 (n 70) | -2,236 to +3,763 |
| Check: same damage from the other team's replay | 7,433 (n 85) | 5,796 (n 70) | -2,603 to +4,742 |
| Nearest cap taken within 60 s (caps not ours) | 17% (n 36) | 19% (n 42) | -18 to +19 |
| Nearest cap taken within 120 s (caps not ours) | 36% (n 36) | 21% (n 42) | -4 to +36 |

- No interval excludes zero. Cap rows: 6 of 36 and 8 of 42 within 60 s; 13 and 9 within 120 s.
- Destroyer smokes only (n 129), the old population: 1.49 vs 1.49 enemies lit, 0.84 vs 0.83 destroyers, 8,429 vs 6,795 damage (-2,558 to +4,761), cap within 120 s 33% vs 25% (-9 to +34).
- For scale, a radar press that is not from smoke (n 2271) lights 1.75 (Top 6) and 1.62 (Rest) enemy ships and goes with 7,221 and 6,666 damage on them: a press from smoke lights slightly fewer ships and goes with about the same damage as any other press. The smoke does not show a bigger return per press; it is where the Top 6 choose to press from.
- Per team-game that adds up to 1.09 vs 0.40 enemy ships lit from smoke (+0.23 to +1.13 *; round 3 had 0.61 vs 0.25 from the batch field), 0.63 vs 0.22 destroyers (+0.16 to +0.69 *), and 5,786 vs 1,754 damage on radar-lit enemies (+1,215 to +6,374 *).
- The old return test on the cap timeline: after the tagged cap-control smokes, the contested cap (not ours at activation) was ours within 60 s of the smoke clearing in 62% (15 of 24) for the Top 6 against 38% (10 of 26) for the Rest (-6 to +55). The old "58% for both" came from the batch field that credits any cap in gun range (see N4-2). On a fixed cap the Top 6 are ahead but the interval is wide and includes zero.
- 10 of the 230 lit records behind these plays could belong to a second radar.

**Top 6 or Shared:** Top 6 for how often (+0.47 per team-game, +0.26 to +0.65 *; clear on every count except the two small ones, radar destroyers and cruiser smokes). Shared for the return per play (no interval excludes zero).

**Clans:** presses from smoke: Top 6: RESIN 25, BONKZ 18, H-SR 16, HTDOG 13, VRTUS 8, KITE 5 | Rest: HFANS 11, BONKY 8, SCCC2 7, MACHX 6, KSC 5, REEEE 4, INCA 4, MZY 4, PFANS 3, EPOXY 3, -BN- 3, UYSC 2, RSR 2, KSE 2, PN 2, BTLST 1, KITED 1, MANBA 1, KM 1. Per game: BONKY 1.14 (8 in 7; tags 5), RESIN* 1.04 (25 in 24; tags 14), SCCC2 1.00 (7 in 7; tags 3), BONKZ* 0.86 (18 in 21; tags 10), VRTUS* 0.73 (8 in 11; tags 4), H-SR* 0.73 (16 in 22; tags 14), HTDOG* 0.72 (13 in 18; tags 6), INCA 0.67 (4 in 6; tags 1), HFANS 0.65 (11 in 17; tags 9), KSC 0.45 (5 in 11; tags 4), MACHX 0.43 (6 in 14; tags 5), KITE* 0.36 (5 in 14; tags 4), REEEE 0.31 (4 in 13; tags 4), MZY 0.21 (4 in 19; tags 3). * = Top 6; Rest clans shown have 4 or more presses.

**Could not be done / proxy:** Defended and Captured ribbons are too thin to use: they exist only for the recording player (2 of 18 ships a game; 442 cap ribbons in the whole batch), only 7 of the 155 plays were pressed by a recording player, and 0 cap ribbons followed them within 120 s. The cap timeline is used instead. "Damage on lit enemies while lit" is all damage those ships took during the lit span, whoever dealt it and whether or not radar was the only thing showing them; the replay does not say which radar lit a ship, so it is assigned by range and time. Damage from shells still in the air when the radar ran out is not counted.

**Verdict:** Keep

**Changed from the atlas / round 4:**

- Layer A: 6 of 6 numbers unchanged (old -> new identical): Destroyer smokes tagged as a radar play 96 (52 Top 6, 44 Rest); Per team-game 0.47 vs 0.19; Gap interval +0.14 to +0.40; Cap taken after cap-control smokes (caps not ours) 58% (of 24) vs 58% (of 26); Three busiest maps 69 of 96 (0.45, 0.40, 0.36 per team-game); Enemy ships lit per smoke with radar run (batch field) 1.1 vs 1.1. Why: same smoke fields.
- Layer B, how often: 0.47 vs 0.19 per team-game (2.5x; 96 tagged destroyer smokes) -> 0.77 vs 0.30 (2.6x; 155 radar presses from any allied smoke; +0.30 and +0.11); destroyer smokes only 0.64 vs 0.25 (2.5x; 129 presses); smokes with a press 0.75 vs 0.28 (2.7x; 149 smokes). Gap interval +0.14 to +0.40 -> +0.26 to +0.65. Why: better data (every radar press is logged; the tags kept only smokes whose first purpose was the radar play) and a wider unit (presses, any smoker class).
- Layer B, three maps: 69 of 96 (72%) -> 103 of 155 (66%). Same three maps. Why: better data.
- Layer B, return per play: enemies lit 1.1 vs 1.1 per smoke -> 1.41 vs 1.33 per press; cap taken 58% vs 58% (batch field, cap-control smokes) -> 62% vs 38% on the contested cap from the timeline (-6 to +55), and 36% vs 21% for the nearest cap within 120 s of a press (-4 to +36); damage on radar-lit enemies, new: 7,488 vs 5,814 per press (-2,321 to +4,748). Why: better data and a fixed-cap definition. "Same return per play" still holds: no gap is clear.

## Figures

- `figures/n4-claim1-short-of-cap.png` / `.svg`
- `figures/n4-claim2-radar-cruiser-inside.png` / `.svg`
- `figures/n4-claim3-radar-from-smoke.png` / `.svg`

