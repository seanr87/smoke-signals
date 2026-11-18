# Round 5b findings: Round 5 redone on the batch with timelines

Batch: `output/20261117-230933` (smoke-signals 0.4.0, revision `a7129ffa`). Every existing smoke field is identical to the
Round 5 batch `output/20261117-122135`; what is new is the timeline files (cap ownership, radar and hydro log, ship tracks
with real health, score, cap ribbons). See `smoke/STEP9-R5B-RERUN.md`.

Same groups (Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS; Rest = everyone else), team-normalized positions, minimum n 8
(8 to 14 = small n), 95% intervals by resampling whole clans. Everything is association, not cause.

How this file is laid out:
1. What changed from Round 5, in short.
2. Verdicts at a glance, with a "changed?" column.
3. Every number that changed from Round 5, with old, new and the difference.
4. The items in Round 5 order. An item redone with the new data has its Round 5b text first; the Round 5 text it replaces
   is kept below it, marked "superseded", so nothing is lost.

## 1. What changed from Round 5, in short

**Reversed or dropped**

- **Danger zones (C3): dropped on every map.** With real health and death positions, the areas flagged are no more than
  shuffled outcomes give by luck. Round 5's one lead, destroyers smoking inside cap C on Hotspot, does not survive
  (27 per 100 against a map baseline of 18.7).
- **"Rest lose the nearby cap more often" (C1): no longer clear.** The snapshots had missed 27% of Top 6 cap flips against
  18% of Rest flips. On the timeline the gap for destroyer smokes within 2 km is -3.1 points (-11.0 to +4.5); it was -6.8
  and clear.
- **"A radar cruiser inside goes with the cap being taken, 58% against 14%" (page 1): does not hold.** The batch field
  behind it credits any cap within gun range of a ship in the smoke, which a cruiser inside inflates. On the cap timeline
  the same pair is 46% against 32% (contested cap) and 59% against 36% (nearest cap); neither is clear.
- **Loop, Daring after a friendly radar (C5): still dropped, for a better reason.** Round 5 could not see radar outside
  smoke (1 of 48 on a thin proxy). With the full radar log it is 17 of 48 (35%) against a chance level of 37%.

**Corrected**

- **Deaths in smoke were undercounted.** The batch list holds 69 smoking destroyers that died in their own smoke; ship
  tracks show 137 dead between activation and 20 seconds after the smoke dispersed. The list left out ships that had sailed
  out, were lit throughout, or died unseen. Like-with-like baselines move from 6.4 died and 15.5 died-or-hurt per 100
  destroyer smokes to 12.8 and 23.1; for sheltering cruisers from 8.0 and 22.0 to 9.6 and 19.4.
- **"Enemy took the cap" was undercounted.** 233 of 1,074 applicable smokes (21.7%), not 184 (17.1%). The snapshot version
  missed 21% of real flips, not the 15% estimated.
- **Radar is behind half of smoke deaths, not one in seven.** 65 of 124 deaths in destroyer smokes were radar-lit in the
  last 40 seconds (Round 5: 19 strict, 45 broad). The radar ship is nearly always a cruiser near maximum range (median
  9.3 km, 89% of its range; Moskva 24 of 64).
- **Two games ran on a 15-minute clock.** Elapsed times in rounds 3 to 5 were 300 seconds too high for their 17 smokes.
  Four destroyer smokes become "early". Fixed in the Round 5b library; section 3 lists what moved.
- **"Second destroyer recorded" (B3) was a snapshot artefact.** The Round 5 snapshot held only ships near the smoke. An
  allied destroyer is alive at 94% or more of these smokes for all three ships. The real difference is distance: one is
  within 5 km for 32% of a Harugumo smoke's life, against 14% (Somers) and 13% (Gearing).

**Confirmed with better data**

- **Early smoke is laid short of the cap.** Measured on ships, not the smoke outline: the smoker is a median 2.6 km outside
  the nearest cap edge when it presses smoke and the covered cruiser stays 3.2 km out.
- **Radar cruiser inside early smokes: Top 6 59% against 35%** (+24, +12 to +35; 60% against 35% before the clock fix).
  New: the cruiser ran radar from the smoke in only about a third of those, the same for both groups. The Top 6 difference
  is having the cruiser in the smoke, not pressing radar from it.
- **Radar from smoke: Top 6 about 2.5 times as often, same return per press.** Direct count from the radar log: 155 presses
  from inside an allied smoke, 0.77 against 0.30 per team-game (was 0.47 against 0.19 on the purpose tag).
- **Most "smoke deaths" happen outside the smoke.** Of 124, 29 died inside a standing smoke and 82 after sailing out. But
  leaving is not itself the risky moment: destroyers died at about 3 to 4 per 100 per 30 seconds inside, after leaving and
  after dispersal alike. Being 50+ behind raises all three.
- **Harugumo's targets are spotted by somebody else.** Per shot (410 shots, 44 smokes): the nearest friendly ship is a ship
  outside the smoke 45%, the Harugumo itself 31%, a second destroyer 24%, the radar cruiser inside 0.5%. Only 3% of its
  shots are at a target lit by a radar ship inside that smoke.
- **Cap holder at 8:00 (C2): same answer on 166 games** (was 154). No pooled row moved by more than 3 points.

**Not usable**

- **Ribbons per smoke.** Replays hold them for one ship per team. Only 268 of 1,547 smokes covered a recording player, and
  11 such smokes have a Defended ribbon on a cap the team owned. They do confirm the timeline: all 91 Captured ribbons sit
  on a recorded flip to that team, and all 284 Defended ribbons fall while an enemy stood in a cap.

## 2. Verdicts at a glance

| Item | Round 5 verdict | Round 5b | Changed? |
|---|---|---|---|
| A1 Cap-contest smokes by cover | Keep | Keep. Not redone; see the page 1 re-test for the cap link | Read with N4-2: the batch "cap won" field over-credits smokes with a cruiser inside |
| A2 Smoke deaths | Lead | Lead | Yes: track deaths, leaving the smoke, radar deaths all redone; baselines doubled for destroyers |
| A3 Somers vs Gearing deaths | Keep | Keep. Not redone | Clock fix only |
| A4 Counter-smokes | Keep; Drop flanking | Same. Not redone | Clock fix only |
| B1 Cap sitters | Keep | Same. Not redone | No |
| B2 Getaway smokes | Keep | Same. Not redone | No |
| B3 Long smokes | Lead | Keep for the Harugumo spotting part (redone per shot); rest as Round 5 | Yes: second-destroyer numbers replaced |
| B4 Hybrids | Keep Shimakaze; Drop Grozovoi | Same. Not redone | No |
| C1 Cap defence | Keep | Keep, timeline version replaces the snapshot version | Yes: counts up, the Top 6 gap no longer clear |
| C2 Cap holder at 8:00 | Keep as a caution | Same, on 166 games | Small moves only |
| C3 Danger zones | Lead for Hotspot C; Drop the rest | Drop on every map | Yes |
| C4 Spots per map | Keep as a catalogue | Same. Not redone | Clock fix only (early cruiser spots) |
| C5 Map questions | Per question | Same; Loop Daring test redone, still Drop | Loop test numbers replaced |
| D1 to D3 Clan styles | Keep / Lead / Keep | Same. Not redone | Clock fix only (first-smoke time, share after 12 minutes) |
| Page 1: early smoke short of the cap | (atlas) | Keep, Shared | Confirmed on ships |
| Page 1: radar cruiser inside early smokes | (atlas) | Keep, reword | 58% against 14% cap link withdrawn |
| Page 1: radar from smoke | (atlas) | Keep | Direct count replaces the tag count |

## 3. Every number that changed from Round 5

Three sources of change. (a) New data: items redone from the timelines; each block below is the full old-to-new list from that item. (b) The 15-minute-clock fix, which touches items that were not redone. (c) Nothing else: with the Round 5 definitions unchanged, the Round 5 scripts give the Round 5 outputs again on the new batch (`rerun/same-definitions.txt`).

### 3a. Changed because of the new data

**C1. Cap defence: "enemy took the cap" from the timeline, and ribbons** (`new-n1/FINDINGS-N1.md`)

| number | round 5 | round 5b | difference |
|---|---|---|---|
| enemy took, 60 s grace: yes | 184 | 233 | +49 |
| enemy took, 60 s grace: share | 17.1% | 21.7% | +4.6 |
| enemy took, no grace: yes | 103 | 155 | +52 |
| enemy took, no grace: share | 9.6% | 14.4% | +4.8 |
| enemy took, 120 s grace: yes | 233 | 293 | +60 |
| enemy took, 120 s grace: share | 21.7% | 27.3% | +5.6 |
| coverage: yes / no / not applicable | 184 / 889 / 474 | 233 / 841 / 473 |  |
| share of real flips the snapshot version misses | about 15% (estimate) | 20.7% enemy, 22.9% ours (measured) |  |
| all applicable smokes: share | 17.1% (n 1073) | 21.7% (n 1074) | +4.6 |
| all applicable smokes: Top 6 - Rest | -4.4 (-8.9 to +0.1) | -3.0 (-7.1 to +1.2) | +1.4 |
| destroyer smokes: share | 18.8% (n 762) | 23.1% (n 763) | +4.3 |
| destroyer smokes: Top 6 - Rest | -5.9 (-12.1 to -0.9) clear | -3.5 (-9.5 to +2.8) | +2.4 |
| smoke centre inside or within 2 km of the cap: share | 11.1% (n 541) | 16.1% (n 541) | +5.0 |
| smoke centre inside or within 2 km of the cap: Top 6 - Rest | -4.8 (-9.2 to -0.7) clear | -2.8 (-8.9 to +3.9) | +2.0 |
| destroyer smokes inside or within 2 km: share | 12.8% (n 405) | 17.5% (n 405) | +4.7 |
| destroyer smokes inside or within 2 km: Top 6 - Rest | -6.8 (-12.6 to -1.7) clear | -3.1 (-11.0 to +4.5) | +3.7 |
| cap ours at activation: share | 13.7% (n 694) | 18.2% (n 694) | +4.5 |
| cap ours at activation: Top 6 - Rest | -1.6 (-8.2 to +5.0) | +0.4 (-5.8 to +5.8) | +2.0 |
| cap neutral at activation: share | 23.5% (n 379) | 28.2% (n 380) | +4.7 |
| cap neutral at activation: Top 6 - Rest | -9.4 (-18.4 to -0.5) clear | -9.0 (-18.3 to -0.2) clear | +0.4 |
| cap ours, smoke within 2 km: share | 8.0% (n 350) | 12.3% (n 349) | +4.3 |
| cap ours, smoke within 2 km: Top 6 - Rest | -4.2 (-9.7 to +1.5) | -1.7 (-11.1 to +6.8) | +2.5 |
| cap ours, cap_defended set for that cap: share | 35.9% (n 153) | 45.8% (n 153) | +9.9 |
| cap ours, cap_defended set for that cap: Top 6 - Rest | -7.8 (-24.7 to +10.5) | +3.5 (-13.1 to +20.0) | +11.3 |
| cap ours, cap_defended not set for it: share | 7.4% (n 541) | 10.4% (n 541) | +3.0 |
| cap ours, cap_defended not set for it: Top 6 - Rest | +1.3 (-3.4 to +5.2) | +1.1 (-3.7 to +5.3) | -0.2 |
| cap_defended kept, all smokes with cap_defended | 60.5%; gap +3.1 (-10.7 to +15.3) | 52.5%; gap +1.4 (-13.2 to +13.7) | -8.0 |
| cap_defended kept, destroyer smokes | 58.9%; gap +1.2 (-15.0 to +13.3) | 50.6%; gap +1.6 (-14.2 to +14.5) | -8.3 |
| cap_defended kept, defended cap = nearest cap | 61.1%; gap +8.6 (-6.2 to +21.9) | 53.7%; gap -2.1 (-19.1 to +15.6) | -7.4 |
| cap_defended kept, defended cap not the nearest | 60.1%; gap -0.2 (-16.7 to +14.0) | 51.8%; gap +3.3 (-13.2 to +17.9) | -8.3 |
| cap_defended kept, no grace / 120 s | 77.0% / 51.9% | 68.7% / 46.7% | -8.3 / -5.2 |
| nearest cap ours at activation: kept | 86.3% (n 694) | 81.8% (n 694) | -4.5 |
| we took, all smokes where the nearest cap was not ours | 24.5%; gap +5.8 (-1.7 to +14.4) | 31.9%; gap +10.5 (-0.2 to +22.1) | +7.4 |
| we took, destroyer smokes | 27.0%; gap +8.9 (-1.6 to +20.2) | 35.6%; gap +15.3 (+2.1 to +28.1) clear | +8.6 |
| we took, within 2 km | 35.0%; gap +6.2 (-3.5 to +18.5) | 42.3%; gap +12.1 (+1.3 to +23.5) clear | +7.3 |
| Hotspot A: enemy took | 0.0% | 9.1% (n 11) | +9.1 |
| Hotspot B: enemy took | 9.1% | 11.4% (n 44) | +2.3 |
| Hotspot C: enemy took | 26.2% | 32.3% (n 65) | +6.1 |
| Hotspot D: enemy took | 23.8% | 25.0% (n 84) | +1.2 |
| Land of Fire A: enemy took | 20.8% | 22.6% (n 53) | +1.8 |
| Land of Fire B: enemy took | 11.8% | 14.7% (n 68) | +2.9 |
| Land of Fire D: enemy took | 7.7% | 11.5% (n 26) | +3.8 |
| Loop A: enemy took | 17.0% | 21.3% (n 47) | +4.3 |
| Loop B: enemy took | 20.0% | 30.0% (n 30) | +10.0 |
| Loop C: enemy took | 12.1% | 15.2% (n 33) | +3.1 |
| Mountain Range A: enemy took | 14.6% | 24.4% (n 41) | +9.8 |
| Mountain Range B: enemy took | 35.6% | 39.1% (n 46) | +3.5 |
| Mountain Range C: enemy took | 17.9% | 21.4% (n 56) | +3.5 |
| Okinawa A: enemy took | 15.4% | 23.1% (n 39) | +7.7 |
| Okinawa C: enemy took | 13.5% | 18.9% (n 37) | +5.4 |
| Okinawa D: enemy took | 19.2% | 30.8% (n 26) | +11.6 |
| Sea of Fortune A: enemy took | 8.3% | 16.7% (n 12) | +8.4 |
| Sea of Fortune B: enemy took | 10.0% | 13.3% (n 60) | +3.3 |
| Sea of Fortune C: enemy took | 6.7% | 40.0% (n 15) | +33.3 |
| Sleeping Giant A: enemy took | 21.1% | 26.7% (n 90) | +5.6 |
| Sleeping Giant B: enemy took | 8.7% | 10.9% (n 46) | +2.2 |
| Sleeping Giant D: enemy took | 17.3% | 20.0% (n 75) | +2.7 |
| ribbons | not in the batch | 442 ribbons, 268 smokes with a recording player covered | new |

Why: better data. The timeline has every owner change; round 5 only saw cap owners at the moments other smokes were laid or fully laid. Same definition, same nearest cap, same 60 s grace. Every share went up because flips after the last snapshot are now seen. The `cap_defended` follow-up also changed its start point slightly (from the first invaded moment instead of from activation; this gives the same count). Unchanged: the meaning of `cap_defended`, its rates (31.4% of smokes) and the distance facts, which use smoke fields only.

**C2. Cap holder at exactly 8:00 and winning** (`new-n1/FINDINGS-N1.md`)

| number | round 5 (154 games, snapshot within 60 s) | round 5b (exact 8:00, timeline) | difference |
|---|---|---|---|
| games in the tables | 154 | 166 | +12 |
| Rest-vs-Rest games | 76 | 84 | +8 |
| games level on caps at 8:00 | 63 of 154 | 69 of 166 |  |
| cap leaders already ahead on score | 66 of 91 (73%), median +95 | 72 of 97 (74%), median +105 |  |
| score leader at 8:00 won | 120 of 153 (78%) | 131 of 165 (79%) |  |
| Top 6 vs Rest games: Top 6 more / fewer caps / won | 53 games: 30 / 7 / 46 | 57 games: 30 / 10 / 50 |  |
| pooled, all games: its own-side cap | n 184, won 94 (51%), +1 (-3 to +4) | n 199, won 101 (51%), +0 (-3 to +4) | n +15, wins +7, -0 pts |
| pooled, all games: the enemy-side cap | n 47, won 25 (53%), +2 (-10 to +15) | n 50, won 26 (52%), +2 (-11 to +14) | n +3, wins +1, -0 pts |
| pooled, all games: at least one middle cap | n 231, won 131 (57%), +5 (+1 to +8) clear | n 247, won 136 (55%), +3 (+0 to +7) clear | n +16, wins +5, -1 pts |
| pooled, all games: every middle cap | n 43, won 27 (63%), +6 (-5 to +18) | n 49, won 31 (63%), +6 (-5 to +16) | n +6, wins +4, -1 pts |
| pooled, all games: more caps than the enemy (reference) | n 91, won 60 (66%), +8 (-0 to +17) | n 97, won 61 (63%), +6 (-2 to +14) | n +6, wins +1, -2 pts |
| pooled, all games: 2+ more caps than the enemy | n 42, won 31 (74%), +15 (+4 to +26) clear | n 45, won 33 (73%), +13 (+3 to +24) clear | n +3, wins +2, -2 pts |
| pooled, Rest-vs-Rest: its own-side cap | n 88, won 46 (52%), +2 (-3 to +7) | n 100, won 52 (52%), +2 (-3 to +7) | n +12, wins +6, -0 pts |
| pooled, Rest-vs-Rest: the enemy-side cap | n 26, won 15 (58%), +8 (-9 to +26) | n 26, won 15 (58%), +7 (-12 to +26) | n +0, wins +0, -1 pts |
| pooled, Rest-vs-Rest: at least one middle cap | n 119, won 64 (54%), +2 (-2 to +6) | n 131, won 69 (53%), +1 (-3 to +5) | n +12, wins +5, -1 pts |
| pooled, Rest-vs-Rest: every middle cap | n 22, won 14 (64%), +5 (-12 to +23) | n 25, won 16 (64%), +4 (-12 to +18) | n +3, wins +2, -1 pts |
| pooled, Rest-vs-Rest: more caps than the enemy (reference) | n 41, won 23 (56%), +1 (-12 to +15) | n 44, won 24 (54%), -1 (-15 to +13) | n +3, wins +1, -2 pts |
| pooled, Rest-vs-Rest: 2+ more caps than the enemy | n 20, won 16 (80%), +22 (+7 to +36) clear | n 21, won 17 (81%), +20 (+5 to +33) clear | n +1, wins +1, -2 pts |
| Hotspot, all games: A (enemy side) | n 9, won 6 (67%), +12 (-21 to +42) | n 9, won 6 (67%), +12 (-20 to +42) | n +0, wins +0, +0 pts |
| Hotspot, all games: B (own side) | n 49, won 26 (53%), +2 (-3 to +8) | n 53, won 28 (53%), +2 (-3 to +7) | n +4, wins +2, -0 pts |
| Hotspot, all games: C (middle) | n 28, won 20 (71%), +16 (+1 to +30) clear | n 29, won 21 (72%), +16 (+0 to +32) clear | n +1, wins +1, +0 pts |
| Hotspot, all games: D (middle) | n 29, won 16 (55%), +4 (-13 to +20) | n 30, won 16 (53%), +1 (-14 to +17) | n +1, wins +0, -3 pts |
| Hotspot, all games: more caps than the enemy (reference) | n 12, won 10 (83%), +27 (+6 to +45) clear | n 12, won 10 (83%), +25 (+2 to +42) clear | n +0, wins +0, -2 pts |
| Hotspot, Rest-vs-Rest: B (own side) | n 27, won 16 (59%), +8 (+2 to +18) clear | n 31, won 18 (58%), +7 (+2 to +16) clear | n +4, wins +2, -1 pts |
| Hotspot, Rest-vs-Rest: C (middle) | n 15, won 10 (67%), +10 (-15 to +32) | n 16, won 11 (69%), +10 (-14 to +31) | n +1, wins +1, +1 pts |
| Hotspot, Rest-vs-Rest: D (middle) | n 16, won 9 (56%), +2 (-21 to +23) | n 17, won 9 (53%), -2 (-24 to +20) | n +1, wins +0, -4 pts |
| Hotspot, Rest-vs-Rest: more caps than the enemy (reference) | n 10, won 8 (80%), +25 (-3 to +47) | n 10, won 8 (80%), +22 (-2 to +45) | n +0, wins +0, -3 pts |
| Land of Fire, all games: A (middle) | n 18, won 14 (78%), +20 (+2 to +38) clear | n 21, won 16 (76%), +18 (+1 to +34) clear | n +3, wins +2, -2 pts |
| Land of Fire, all games: B (middle) | n 20, won 16 (80%), +19 (+3 to +33) clear | n 21, won 17 (81%), +20 (+6 to +34) clear | n +1, wins +1, +1 pts |
| Land of Fire, all games: C (enemy side) | n 12, won 5 (42%), -5 (-31 to +22) | n 12, won 5 (42%), -5 (-29 to +21) | n +0, wins +0, +0 pts |
| Land of Fire, all games: D (own side) | n 34, won 16 (47%), -2 (-11 to +8) | n 36, won 17 (47%), -2 (-10 to +7) | n +2, wins +1, +0 pts |
| Land of Fire, all games: more caps than the enemy (reference) | n 14, won 12 (86%), +24 (+1 to +42) clear | n 15, won 13 (87%), +25 (+5 to +40) clear | n +1, wins +1, +1 pts |
| Land of Fire, Rest-vs-Rest: A (middle) | n 10, won 7 (70%), +11 (-18 to +35) | n 12, won 8 (67%), +10 (-12 to +31) | n +2, wins +1, -1 pts |
| Land of Fire, Rest-vs-Rest: B (middle) | n 10, won 7 (70%), +15 (-13 to +39) | n 11, won 8 (73%), +17 (-7 to +40) | n +1, wins +1, +2 pts |
| Land of Fire, Rest-vs-Rest: C (enemy side) | n 8, won 4 (50%), +5 (-26 to +33) | n 8, won 4 (50%), +5 (-24 to +34) | n +0, wins +0, +0 pts |
| Land of Fire, Rest-vs-Rest: D (own side) | n 14, won 7 (50%), +3 (-13 to +23) | n 16, won 8 (50%), +2 (-12 to +19) | n +2, wins +1, -0 pts |
| Land of Fire, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 5) | too few (n 6) |  |
| Loop, all games: A (middle) | n 16, won 6 (38%), -10 (-30 to +14) | n 19, won 8 (42%), -7 (-28 to +14) | n +3, wins +2, +2 pts |
| Loop, all games: B (middle) | n 18, won 11 (61%), +8 (-12 to +28) | n 21, won 13 (62%), +9 (-10 to +29) | n +3, wins +2, +1 pts |
| Loop, all games: C (middle) | n 14, won 6 (43%), -16 (-38 to +8) | n 15, won 7 (47%), -12 (-36 to +14) | n +1, wins +1, +4 pts |
| Loop, all games: more caps than the enemy (reference) | n 13, won 6 (46%), -12 (-37 to +13) | n 15, won 8 (53%), -6 (-30 to +19) | n +2, wins +2, +7 pts |
| Loop, Rest-vs-Rest: A (middle) | n 9, won 4 (44%), -3 (-38 to +33) | n 11, won 5 (46%), -4 (-35 to +28) | n +2, wins +1, -1 pts |
| Loop, Rest-vs-Rest: B (middle) | n 10, won 6 (60%), +9 (-22 to +40) | n 12, won 7 (58%), +9 (-25 to +39) | n +2, wins +1, -0 pts |
| Loop, Rest-vs-Rest: C (middle) | n 9, won 1 (11%), -40 (-57 to -15) clear | n 10, won 2 (20%), -31 (-57 to +1) | n +1, wins +1, +9 pts |
| Loop, Rest-vs-Rest: more caps than the enemy (reference) | n 8, won 2 (25%), -26 (-56 to +13) | n 9, won 3 (33%), -18 (-54 to +19) | n +1, wins +1, +8 pts |
| Mountain Range, all games: A (middle) | n 12, won 6 (50%), -2 (-29 to +21) | n 14, won 9 (64%), +8 (-12 to +29) | n +2, wins +3, +9 pts |
| Mountain Range, all games: B (middle) | n 17, won 11 (65%), +11 (-9 to +30) | n 18, won 12 (67%), +11 (-8 to +30) | n +1, wins +1, +0 pts |
| Mountain Range, all games: C (middle) | n 19, won 10 (53%), +1 (-19 to +20) | n 20, won 9 (45%), -5 (-23 to +14) | n +1, wins -1, -6 pts |
| Mountain Range, all games: more caps than the enemy (reference) | n 12, won 9 (75%), +15 (-6 to +35) | n 14, won 10 (71%), +12 (-8 to +30) | n +2, wins +1, -3 pts |
| Mountain Range, Rest-vs-Rest: A (middle) | too few (n 5) | too few (n 6) |  |
| Mountain Range, Rest-vs-Rest: B (middle) | too few (n 7) | n 8, won 6 (75%), +8 (-19 to +34) |  |
| Mountain Range, Rest-vs-Rest: C (middle) | n 8, won 4 (50%), +9 (-21 to +37) | n 9, won 3 (33%), -5 (-31 to +21) | n +1, wins -1, -14 pts |
| Mountain Range, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 5) |  |
| Okinawa, all games: A (own side) | n 22, won 12 (54%), +2 (-11 to +16) | n 23, won 12 (52%), -0 (-13 to +12) | n +1, wins +0, -3 pts |
| Okinawa, all games: B (enemy side) | n 9, won 5 (56%), +5 (-26 to +39) | n 10, won 5 (50%), -2 (-30 to +27) | n +1, wins +0, -6 pts |
| Okinawa, all games: C (middle) | n 15, won 6 (40%), -3 (-26 to +20) | n 16, won 7 (44%), -0 (-24 to +22) | n +1, wins +1, +3 pts |
| Okinawa, all games: D (middle) | n 15, won 6 (40%), -14 (-37 to +9) | n 16, won 7 (44%), -10 (-33 to +12) | n +1, wins +1, +4 pts |
| Okinawa, all games: more caps than the enemy (reference) | n 8, won 3 (38%), -11 (-38 to +17) | too few (n 7) |  |
| Okinawa, Rest-vs-Rest: A (own side) | n 16, won 8 (50%), +3 (-13 to +20) | n 16, won 8 (50%), +2 (-15 to +18) | n +0, wins +0, -1 pts |
| Okinawa, Rest-vs-Rest: C (middle) | n 10, won 6 (60%), +14 (-15 to +41) | n 10, won 6 (60%), +14 (-15 to +41) | n +0, wins +0, +0 pts |
| Okinawa, Rest-vs-Rest: D (middle) | n 10, won 4 (40%), -16 (-42 to +15) | n 10, won 4 (40%), -16 (-42 to +14) | n +0, wins +0, +0 pts |
| Okinawa, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 3) |  |
| Sea of Fortune, all games: A (enemy side) | too few (n 6) | too few (n 7) |  |
| Sea of Fortune, all games: B (own side) | n 32, won 16 (50%), -1 (-8 to +6) | n 35, won 17 (49%), -1 (-7 to +6) | n +3, wins +1, -0 pts |
| Sea of Fortune, all games: C (middle) | n 16, won 6 (38%), -12 (-29 to +8) | n 18, won 6 (33%), -13 (-31 to +4) | n +2, wins +0, -2 pts |
| Sea of Fortune, all games: D (middle) | n 17, won 12 (71%), +15 (-5 to +30) | n 18, won 12 (67%), +14 (-6 to +31) | n +1, wins +0, -1 pts |
| Sea of Fortune, all games: more caps than the enemy (reference) | n 15, won 8 (53%), -0 (-24 to +20) | n 15, won 7 (47%), -2 (-22 to +18) | n +0, wins -1, -2 pts |
| Sea of Fortune, Rest-vs-Rest: B (own side) | n 15, won 7 (47%), -5 (-18 to +3) | n 17, won 8 (47%), -4 (-16 to +3) | n +2, wins +1, +1 pts |
| Sea of Fortune, Rest-vs-Rest: C (middle) | n 8, won 3 (38%), -12 (-38 to +16) | n 9, won 3 (33%), -16 (-38 to +11) | n +1, wins +0, -4 pts |
| Sea of Fortune, Rest-vs-Rest: D (middle) | n 9, won 7 (78%), +16 (-10 to +35) | n 10, won 7 (70%), +14 (-11 to +36) | n +1, wins +0, -2 pts |
| Sea of Fortune, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 6) | too few (n 5) |  |
| Sleeping Giant, all games: A (middle) | n 29, won 17 (59%), +6 (-9 to +20) | n 32, won 15 (47%), -3 (-18 to +11) | n +3, wins -2, -9 pts |
| Sleeping Giant, all games: B (middle) | n 16, won 10 (62%), +10 (-9 to +31) | n 17, won 10 (59%), +7 (-13 to +27) | n +1, wins +0, -3 pts |
| Sleeping Giant, all games: C (enemy side) | n 11, won 6 (54%), +2 (-25 to +28) | n 12, won 7 (58%), +6 (-20 to +30) | n +1, wins +1, +4 pts |
| Sleeping Giant, all games: D (own side) | n 47, won 24 (51%), +0 (-5 to +6) | n 52, won 27 (52%), +1 (-4 to +7) | n +5, wins +3, +1 pts |
| Sleeping Giant, all games: more caps than the enemy (reference) | n 17, won 12 (71%), +11 (-10 to +30) | n 19, won 11 (58%), +3 (-16 to +22) | n +2, wins -1, -8 pts |
| Sleeping Giant, Rest-vs-Rest: A (middle) | n 10, won 5 (50%), +2 (-27 to +31) | n 12, won 5 (42%), -5 (-28 to +22) | n +2, wins +0, -7 pts |
| Sleeping Giant, Rest-vs-Rest: D (own side) | n 16, won 8 (50%), -2 (-16 to +10) | n 20, won 10 (50%), -2 (-14 to +8) | n +4, wins +2, +0 pts |
| Sleeping Giant, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 6) |  |

Rows that were clear in round 5 and are not now: Loop C (middle) (Rest-vs-Rest). Rows that became clear: none.

Why: better data, same definition. Twelve games with no snapshot near 8:00 are now included, the owner is read at the exact second instead of up to 60 s away, and two games on a 15-minute clock are read at the right moment. Intervals also move by a point or so between runs of the same data because they come from resampling. No conclusion changed: every pooled row moved by 3 points or less.

**Real health: old estimate against the tracks, and the baselines redone** (`new-n2/FINDINGS-N2.md`)

- Destroyer smoker died, per 100 destroyer smokes: 6.4 -> 12.8 (+6.4). Different definition: track deaths in the smoke window, not the batch list. The batch list on its own still gives 6.4.
- Destroyer smoker died or hurt, per 100: 15.5 -> 23.1 (+7.6). Better data (real health: 21.0 with the old death list) plus the track deaths.
- Sheltering cruiser died, per 100 cruisers (any smoke): 8.0 -> 9.6 (+1.6). Track deaths. The batch list gives 7.8 on the cruisers with complete health.
- Sheltering cruiser died or hurt, per 100 (any smoke): 22.0 -> 19.4 (-2.6). Better data: cruisers heal and the estimate was too low for Brisbane. High-to-low version: 24.8.
- Sheltering cruiser died or hurt, destroyer smokes only (round 5 A2 table): 22.5 -> 19.6 (-2.9). Same reason.
- Top 6 minus Rest, cruiser died or hurt (any smoke): not clear (-17.7 to +2.6 in destroyer smokes) -> -16.6 to -1.3 *. Real health.
- Destroyer smokes in the health numbers: 1074 -> 1070 (-4). The KSC smoker in the single-replay game is left out.

**C3. Danger zones (real health; two ways of placing the damage)** (`new-n2/FINDINGS-N2.md`)

- Flagged areas, keyed on the smoke centre: 4 -> 2 (-2). Real health and track deaths. Now: Sleeping Giant F5, Sleeping Giant E7+F7+F8.
- Hotspot inside cap C (destroyer smoker), died or hurt per 100: 32 -> 27.3 (-4.7). Real health: 6 of 22 instead of 7 of 22, while the baselines rose (all maps 15.5 -> 23.1, Hotspot 11.9 -> 18.7). The gap is no longer clear (-4 to +52 against the map). Round 5 called this Lead; now Drop.
- Sea of Fortune E5+F5+E6: flag (n 8) -> no flag. Same 5 of 8, but the Sea of Fortune baseline rose and the gap against the map is not clear.
- Sleeping Giant E7+F7+F8: flag, 50 per 100 (n 8) -> flag, 62 per 100 (n 8). Still passes, still n 8, still in line with luck.
- Mountain Range E7+F7+F8 (cruisers): flag (n 8) -> not rated (n 7). One of the 8 smokes is in the single-replay game, health incomplete.
- Placebo, flags by luck per run: 1.23 -> 1.57 (+0.3). Higher baselines make chance flags a little more common.
- Areas tested: 109 -> 108 (-1). Single-replay ships excluded.
- Keyed on where the ship was hit: not possible -> 3 flags, 1.75 by luck. New: death positions and health tracks.
- Death position: unknown -> 268 deaths placed. New: tracks.

**A2. Leaving the smoke (from ship tracks)** (`new-n2/FINDINGS-N2.md`)

- Proxy 1, died just after the smoke cleared: 27 -> 5 (-22). Tracks: only 5 of the 124 died after the smoke dispersed around them. Of round 5's 27, the track puts left, over 30 s 19, smoke dispersed 4, never inside 3, left, 30 s or less 1: most had sailed out long before.
- Proxy 2, died behind rather than inside: 25 -> 8 (-17). Tracks: 8 were never inside the outline. Of round 5's 25 "behind", the track puts left, over 30 s 9, never inside 8, left, 30 s or less 4, inside 3, smoke dispersed 1.
- Died inside the smoke (batch "inside"): 99 -> 29 (-70). The batch "inside" means concealed by the smoke at some point. By position at death: left, over 30 s 48, inside 26, left, 30 s or less 21, smoke dispersed 4.
- Deaths after leaving a standing smoke: could not be told -> 82. New: tracks.
- Leaving against staying, rates: could not be done -> 3.1 vs 3.6 per 100 (smoking destroyers, next 30 s). New: tracks.
- Deaths of ships at risk in destroyer smokes: 124 -> 201 (+77). Track deaths in the smoke window; the batch list misses ships that died unseen or were lit throughout.

**A2. Radar deaths with the full radar log** (`new-n2/FINDINGS-N2.md`)

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

**B3. Harugumo: who is near, and what lights, its targets at the time of each shot** (`new-n3/FINDINGS-N3.md`)

| Number | Round 5 (one snapshot per smoke) | Round 5b (per shot) | Difference |
|---|---|---|---|
| Harugumo: nearest friendly ship is a ship outside the smoke | 42% of 53 targets | 45% of 410 shots | +3 points |
| Somers: nearest friendly ship is a ship outside the smoke | 17% of 30 targets | 37% of 83 shots | +20 points |
| Gearing: nearest friendly ship is a ship outside the smoke | 17% of 18 targets | 8% of 64 shots | -9 points |
| Harugumo: nearest friendly ship is a second destroyer | 25% of 53 targets | 24% of 410 shots | -1 points |
| Somers: nearest friendly ship is a second destroyer | 17% of 30 targets | 11% of 83 shots | -6 points |
| Gearing: nearest friendly ship is a second destroyer | 0% of 18 targets | 2% of 64 shots | +2 points |
| Harugumo: nearest friendly ship is the smoker itself | 21% of 53 targets | 31% of 410 shots | +10 points |
| Somers: nearest friendly ship is the smoker itself | 53% of 30 targets | 48% of 83 shots | -5 points |
| Gearing: nearest friendly ship is the smoker itself | 83% of 18 targets | 91% of 64 shots | +8 points |
| Harugumo: nearest friendly ship is another ship in or behind the smoke | 8% of 53 targets | 0% of 410 shots | -8 points |
| Somers: nearest friendly ship is another ship in or behind the smoke | 3% of 30 targets | 0% of 83 shots | -3 points |
| Gearing: nearest friendly ship is another ship in or behind the smoke | 0% of 18 targets | 0% of 64 shots | +0 points |
| Harugumo: nearest friendly ship is the radar cruiser inside the smoke | 6% of 53 targets | 0% of 410 shots | -6 points |
| Somers: nearest friendly ship is the radar cruiser inside the smoke | 10% of 30 targets | 4% of 83 shots | -6 points |
| Gearing: nearest friendly ship is the radar cruiser inside the smoke | 0% of 18 targets | 0% of 64 shots | +0 points |

- Why: better data and a different unit. Round 5 looked once per smoke, at the moment it was fully laid, and only at targets whose position the snapshot happened to hold (53 of 68 Harugumo targets). Round 5b looks at every shot with every ship's position. Redoing the round 5 question with the tracks at the same single moment, same targets and same rule gives a ship outside the smoke 27, a second destroyer 18, the smoker itself 20, another ship in or behind the smoke 2, the radar cruiser inside the smoke 1 of 68; 46 of the 53 shared targets get the same answer. So part of the shift is the 15 targets round 5 could not place, and part is shots fired later in the smoke's life.
- Harugumo "ship outside the smoke or a second destroyer": 67% -> 69% (+2). "The radar cruiser inside": 6% -> 0.5%. "The smoker itself": 21% -> 31%. The Harugumo against Somers gap on "the smoker itself" was -32.6 (clear) and is now -17.5 (-41.5 to +10.4), not clear by shots, -23.0 (-42.2 to -3.8 *), clear per smoke.

| Ship | Second destroyer recorded, round 5 | Second destroyer alive at the same moment, tracks | Difference | 1 km+ forward, round 5 | 1 km+ forward, tracks | Difference | Smokes where the two agree on "recorded" |
|---|---|---|---|---|---|---|---|
| Harugumo | 59.0% | 94.0% | +35.0 | 33.0% | 61.0% | +28.0 | 65 of 100 |
| Somers | 45.8% | 99.6% | +53.8 | 22.7% | 66.9% | +44.2 | 120 of 260 |
| Gearing | 37.2% | 95.6% | +58.4 | 17.2% | 51.7% | +34.5 | 75 of 180 |

- Why: the round 5 snapshot held only some of the ships (about 3 to 4 allied ships of up to 9 alive, the ones near the smoke), so "recorded" really meant "close enough to be in the snapshot". With full tracks a second allied destroyer is alive at almost every smoke of all three ships, so the round 5 gaps (+13.2 and +21.8 recorded; +10.3 and +15.8 forward) are not gaps in whether one exists. They are gaps in distance, and that part holds: an allied destroyer is within 5 km of the smoke for 32% of a Harugumo smoke's standing time, against 14% (Somers) and 13% (Gearing), both clear. Different definition, better data.
- Library fix during this round: 17 smokes in two games (15-minute clock) had round 5 elapsed times 300 s too high. Nothing in B3 uses those fields (all times are the exact `e0` / `e1` and the damage event clocks), so no B3 number moved for that reason; the scripts were rerun after the fix.
- New in round 5b (no round 5 number): radar-lit at the shot, 22% of Harugumo shots, of which from inside the smoke 3%.

**Self-checks:**

- Damage total a second way: credited events against the smoke records (smoker's own damage, all of it): Harugumo 461,873 vs 461,960; Somers 253,013 vs 253,009; Gearing 94,724 vs 94,736.
- "Radar-lit from inside this smoke" a second way (the radar log's own source-in-smoke flag instead of track geometry): Harugumo 13 vs 14 shots; Somers 6 vs 8 shots; Gearing 2 vs 1 shots.

**C5-LP-4. Loop: do Daring smokes follow a friendly radar lighting an enemy destroyer?** (`new-n3/FINDINGS-N3.md`)

| Group | Round 5: our radar lit an enemy destroyer in the 60 s before (seen only when that destroyer sat in its own smoke) | Round 5b: same, every radar and every lit destroyer | Difference | Round 5b chance level |
|---|---|---|---|---|
| Daring on Loop | 1 of 48 (2%) | 17 of 48 (35%) | +33 points | 37% |
| Daring on other maps | 7 of 152 (5%) | 61 of 152 (40%) | +35 points | 40% |
| Other cap sitters on Loop | 0 of 40 (0%) | 16 of 40 (40%) | +40 points | 39% |
| Other destroyer smokes on Loop | 0 of 54 (0%) | 19 of 54 (35%) | +35 points | 39% |
| All destroyer smokes, all maps | 24 of 1074 (2%) | 399 of 1074 (37%) | +35 points | 42% |

- Why: better data. Round 5 could see a radar lighting an enemy destroyer only when that destroyer was inside its own team's smoke (9 such rows on Loop). The radar log has 229 lit spans on enemy destroyers in the 23 Loop games. The single round 5 case is still there (1 of 1 found again). Round 5 described its target, an A. da Barbiano, as a cruiser; the roster lists it as a destroyer.
- Reverse view: round 5 had 9 episodes, a Daring alive for 2, 1 followed by a smoke. Round 5b: 62 episodes, 55 with a Daring alive, 14 followed (26% against chance 22%).
- Library fix during this round: two games ran on a 15-minute clock, so the round 5 elapsed times of their 17 smokes were 300 s too high (one of the two games is on Loop). Every time used here is the exact `e0` / `e1` from the timelines, which never had that error; the only library time field used is the game length in the reverse view, rerun after the fix with no change to any count.
- The verdict does not change (Drop), but the reason does. Round 5 said "not supported, on a thin proxy: 1 of 48". Round 5b says: it happens in about a third of Daring smokes on Loop, and that is exactly what chance gives, because some friendly radar has some enemy destroyer lit about a third of the time.

**Self-checks:**

- Headline a second way: counting straight from the radar rows without the helper functions gives 17 of 48, the same as 17.
- Old field against new on the same smokes: the round 5 proxy finds 1 Daring smoke on Loop; the radar log finds that one and 16 more.

**N4-1. Early smoke distance short of the cap** (`new-n4/FINDINGS-N4.md`)

- Layer A: 1 of 3 numbers unchanged (old -> new identical): Laid inside a cap 14%. Moved: Early smokes by the three ships (n): 187 -> 187 with the clock bug still in -> 188 corrected (clock fix); Median distance outside the cap edge: 1.8 km -> 1.8 km with the clock bug still in -> 1.7 km corrected (clock fix). Why: same smoke fields, same computation.
- Layer B (new, no old value unless noted): smoker inside a cap at activation 11% and at the end of laying 10% (outline: 14%); smoker 2.6 km then 2.4 km outside the nearest cap (outline: 1.7 km, +0.8 km; a ship is a point, the outline reaches about half a kilometre further); cruiser to the contested cap 3.8 km -> 3.9 km (one snapshot -> average over the smoke's life); cruiser inside a cap 4% of partners at the snapshot -> 9% of smokes for most of the time, 25% at any time. Why: better data (continuous tracks and cap timeline). The claim itself is unchanged.

**N4-2. Radar cruiser inside early destroyer smokes** (`new-n4/FINDINGS-N4.md`)

- Layer A: 2 of 9 numbers unchanged (old -> new identical): Sleeping Giant 47% vs 59%; Hotspot 87% vs 38%. Moved: All early destroyer smokes, radar cruiser inside: 60% (61 of 102) vs 35% (70 of 200) -> 60% (61 of 102) vs 35% (70 of 200) with the clock bug still in -> 59% (61 of 103) vs 35% (71 of 203) corrected (clock fix); Gap: +25 -> +25 with the clock bug still in -> +24 corrected (clock fix); Gap interval: +13 to +36 -> +13 to +36 with the clock bug still in -> +12 to +35 corrected (clock fix); Harugumo, Somers, Gearing only: 82% vs 51% -> 82% vs 51% with the clock bug still in -> 82% vs 52% corrected (clock fix); Three ships, gap interval: +15 to +46 -> +17 to +47 with the clock bug still in -> +16 to +46 corrected (same data, interval end moved (resampling redrawn); then clock fix); Cap won after: radar cruiser inside vs covered, not inside (three ships): 58% (n 117) vs 14% (n 29) -> 58% (n 117) vs 14% (n 29) with the clock bug still in -> 58% (n 118) vs 14% (n 29) corrected (clock fix); Cap taken, all early destroyer smokes: radar cruiser inside vs not: 61% (of 120) vs 31% (of 150) -> 61% (of 120) vs 31% (of 150) with the clock bug still in -> 61% (of 120) vs 31% (of 153) corrected (clock fix). Why: same smoke fields; an interval end can move by a point or two when the resampling is drawn again (the point estimates are identical).
- Layer B: "radar cruiser inside" 59% vs 35% (+24) -> "inside and ran radar from it" 19% vs 10% (+9, -0 to +17) -> "and lit an enemy destroyer" 16% vs 7% (+8, -0 to +15). New: no old value. Why: better data (radar log).
- Layer B, cap taken, three ships, inside vs covered-not-inside: 58% vs 14% (+44, +32 to +54) -> 46% vs 32% (+14, -4 to +29) on the contested cap; 59% vs 36% (+22, -0 to +41) on the nearest cap. Difference in the gap: -30 and -21 points. All early destroyer smokes: 61% vs 31% (+30, +21 to +38) -> 47% vs 32% (+15, +3 to +25 *) contested; 59% vs 37% (+22, +10 to +32 *) nearest. Why: different definition made possible by better data (one fixed cap followed on the cap timeline, instead of any cap within gun range of a ship in the smoke).

**N4-3. Radar from smoke per team-game, and the return per play** (`new-n4/FINDINGS-N4.md`)

- Layer A: 6 of 6 numbers unchanged (old -> new identical): Destroyer smokes tagged as a radar play 96 (52 Top 6, 44 Rest); Per team-game 0.47 vs 0.19; Gap interval +0.14 to +0.40; Cap taken after cap-control smokes (caps not ours) 58% (of 24) vs 58% (of 26); Three busiest maps 69 of 96 (0.45, 0.40, 0.36 per team-game); Enemy ships lit per smoke with radar run (batch field) 1.1 vs 1.1. Why: same smoke fields.
- Layer B, how often: 0.47 vs 0.19 per team-game (2.5x; 96 tagged destroyer smokes) -> 0.77 vs 0.30 (2.6x; 155 radar presses from any allied smoke; +0.30 and +0.11); destroyer smokes only 0.64 vs 0.25 (2.5x; 129 presses); smokes with a press 0.75 vs 0.28 (2.7x; 149 smokes). Gap interval +0.14 to +0.40 -> +0.26 to +0.65. Why: better data (every radar press is logged; the tags kept only smokes whose first purpose was the radar play) and a wider unit (presses, any smoker class).
- Layer B, three maps: 69 of 96 (72%) -> 103 of 155 (66%). Same three maps. Why: better data.
- Layer B, return per play: enemies lit 1.1 vs 1.1 per smoke -> 1.41 vs 1.33 per press; cap taken 58% vs 58% (batch field, cap-control smokes) -> 62% vs 38% on the contested cap from the timeline (-6 to +55), and 36% vs 21% for the nearest cap within 120 s of a press (-4 to +36); damage on radar-lit enemies, new: 7,488 vs 5,814 per press (-2,321 to +4,748). Why: better data and a fixed-cap definition. "Same return per play" still holds: no gap is clear.

### 3b. Changed because of the 15-minute-clock fix

Two games ran on a 15-minute clock: kots19na_7971 game 1 (Hotspot, KSE against PFANS) and kots19na_7976 game 1 (Loop, KSE
against VRTUS). Rounds 3 to 5 read elapsed time as 20:00 minus the HUD clock, so their 17 smokes (11 by destroyers) were
placed 300 seconds late. Four destroyer smokes become "early" (first 5 minutes); three leave the 15-to-20-minute band.

No verdict changes. No clan changes style. Every changed output line, old and new, is in `rerun/clock-fix-changes.md`
(23 output files touched). The numbers that appear in the Round 5 text and moved:

| Item | Number | Round 5 | Round 5b | Change |
|---|---|---|---|---|
| Page 1 / Module 2 | Early destroyer smokes with a radar cruiser inside, Top 6 | 61 of 102 (60%) | 61 of 103 (59%) | -1 point |
| Page 1 / Module 2 | Same, Rest | 70 of 200 (35%) | 71 of 203 (35%) | 0 |
| Page 1 / Module 2 | Gap | +25 (+13 to +36) | +24 (+12 to +35) | -1 |
| Page 1 / Module 2 | Early Harugumo, Somers, Gearing smokes | 187 | 188 | +1 |
| A1 | Radar cruiser inside: share of those smokes that are early | 33.7% | 34.6% | +0.9 |
| A2 | Destroyer smokes in the first 5 minutes | 302 (102 / 200) | 306 (103 / 203) | +4 |
| A2 | Deaths per 100, first 5 minutes | 7.6 (Rest 10.0) | 7.5 (Rest 9.9) | -0.1 |
| A2 | Destroyer smokes at 10 to 15 minutes | 248 | 247 | -1 |
| A2 | Destroyer smokes at 15 to 20 minutes | 29 (Top 6 9) | 26 (Top 6 7, now too few for a Top 6 rate) | -3 |
| A2 | Deaths per 100, 15 to 20 minutes | 13.8 | 15.4 | +1.6 |
| C1 (snapshot version, superseded) | Smokes where "enemy took" does not apply | 474 | 475 | +1 |
| C2 (snapshot version, superseded) | Games covered at 8:00 | 154 | 155 | +1 |
| C4 | Hotspot early cruiser spot hs-early-1: Rest share | 29% (gap +7, -15 to +33) | 28% (gap +8, -13 to +34) | -1 |
| C4 | Wide Hotspot early cruiser zone: Rest share | 42% | 41% | -1 |
| C5-HS-1 | Hotspot west share, early: Rest | 2 of 45 | 2 of 48 | 3 more early Rest smokes |
| C5-HS-1 | Hotspot west share, later: Rest | 19 of 110 (17%), gap +28 (+20 to +38) | 19 of 107 (18%), gap +28 (+18 to +37) | still clear |
| C5-HS-2 | Hotspot early smokes with a radar cruiser inside | 87% against 38% (17 of 45), +49 (+31 to +71) | 87% against 38% (18 of 48), +50 (+30 to +71) | still clear |
| C5-HS-2 | Hotspot early smokes with the cruiser screened only | 9% against 24%, -16 (-34 to -1), clear | 9% against 23%, -14 (-34 to +0), no longer clear | interval now touches zero |
| C5-HS-2 | Hotspot early destroyer smokes; in the G10 cluster | 68; 36 | 71; 37 | +3; +1 |
| C5-LP-1 | Loop early destroyer smokes per team-game | 0.70 | 0.72 | +0.02 |
| C5-LP-1 | Loop minus other maps | -0.22 (-0.41 to -0.02) | -0.20 (-0.40 to -0.01) | still clear, barely |
| C5-LP-1 | Hotspot early destroyer smokes per team-game | 1.10 | 1.15 | +0.05 |
| D1 | KSE first smoke of the game | 5:08 | 4:11 | 57 s earlier |
| D1 | KSE share of smokes after 12:00 | 20% | 5% | -15 points |
| D1 | PFANS first smoke; share after 12:00 | 3:51; 17% | 3:05; 8% | 46 s earlier; -9 points |
| D1 | VRTUS share of smokes after 12:00 | 20% | 15% | -5 points |
| D2 | First scale's share of the differences between clans | 29.5% | 29.6% | +0.1 |
| D2 | Second scale's share | 17.4% | 17.8% | +0.4 |
| D2 | Top 6 minus Rest on the second scale | +1.21 (+0.22 to +2.24) | +1.18 (+0.19 to +2.23) | still clear |
| D2 | Borderline clans | 7 (PFANS 74% among them) | 6 (PFANS no longer borderline) | -1 |
| D3 | "Team smoke, little" style: first smoke; share after 12:00 | 3:07; 9% | 3:05; 8% | small |
| D3 | "Own smoke, little" style: first smoke; share after 12:00 | 3:45; 8% | 3:41; 6% | small |

Intervals elsewhere in A2 and the other time-split tables move in the last digit because the clans are resampled over
slightly different groups; those lines are in the change file and none crosses zero or stops crossing it, apart from the
Hotspot "screened only" row above.

## 4. The items

---

## Page 1 carry-overs, re-tested (Round 5b)

Source: `new-n4/FINDINGS-N4.md`.


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

### Figures

- `figures/n4-claim1-short-of-cap.png` / `.svg`
- `figures/n4-claim2-radar-cruiser-inside.png` / `.svg`
- `figures/n4-claim3-radar-from-smoke.png` / `.svg`

---

## Part A (Round 5b): deaths with real health, leaving the smoke, radar deaths (A2); danger zones (C3)

Source: `new-n2/FINDINGS-N2.md`.


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

### Figures (working, in `round5b/figures/`)

- `n2-danger-<map>` (7): died or hurt per 100 by area, top row keyed on the smoke centre, bottom row keyed on where the ship was hit.
- `n2-deaths-<map>` (7): death positions, filled = inside the smoke outline.
- `n2-leaving-the-smoke`: where ships died, and leaving against staying.
- `n2-radar-deaths`: distance to the radar ship as a share of range, and rates with and without radar.

---

## Part A: topic cards (A1-A4), Round 5 text

Source: `part-a/FINDINGS-A.md`.

Batch `output/20261117-122135`. Destroyer smokes: 387 Top 6, 687 Rest. Intervals are 95%, whole clans resampled; * = excludes zero. Minimum n 8; 8-14 small n. Association only.

### A1. Cap-contest smokes by cover

**Answer:** For the Rest, a cap-contest smoke with a radar cruiser inside went with taking the cap far more often than one with no cruiser (76% vs 13%). For the Top 6 it made no difference (53% vs 48%). Radar cruiser vs non-radar cruiser cannot be told apart: only 17 smokes have a non-radar cruiser inside.

**Numbers:** 391 destroyer smokes carry the `cap_contest` tag (130 Top 6, 261 Rest). The primary-purpose version is the same 391 smokes.

| Cover | n (Top 6 / Rest) | Cap taken, snapshots (n) | Cap won, batch field (n) | Enemy kept off (n) | Concealed damage | Deaths per 100 |
|---|---|---|---|---|---|---|
| Radar cruiser inside | 104 (55 / 49) | 62.7% (51) | 73.1% (52) | 90.4% (83) | 16,882 | 10.6 |
| Non-radar cruiser inside | 17 (8 / 9) | 37.5% (8, small n) | 62.5% (8, small n) | 76.9% (13, small n) | 15,049 | 23.5 |
| No cruiser | 191 (46 / 145) | 20.4% (108) | 27.8% (108) | 84.1% (132) | 3,515 | 7.3 |
| Footnote: other (cruiser screened only, or mixed) | 79 (21 / 58) | 47.7% (44) | 38.6% (44) | 81.2% (64) | 7,768 | 13.9 |

| Cover | Measure | Top 6 (n) | Rest (n) | Top 6 minus Rest |
|---|---|---|---|---|
| Radar cruiser inside | Cap taken | 53.3% (30) | 76.2% (21) | -42.1 to -5.8 * |
| Radar cruiser inside | Cap won (batch) | 63.3% (30) | 86.4% (22) | -42.8 to +1.4 |
| Radar cruiser inside | Enemy kept off | 90.9% (44) | 89.7% (39) | -7.5 to +10.7 |
| Radar cruiser inside | Concealed damage | 19,099 (55) | 14,394 (49) | -3,637 to +11,740 |
| Radar cruiser inside | Deaths per 100 | 10.9 | 10.2 | -12.3 to +10.8 |
| No cruiser | Cap taken | 47.8% (23) | 12.9% (85) | +16.5 to +60.3 * |
| No cruiser | Cap won (batch) | 65.2% (23) | 17.6% (85) | +36.2 to +67.1 * |
| No cruiser | Enemy kept off | 94.6% (37) | 80.0% (95) | +4.1 to +25.2 * |
| No cruiser | Concealed damage | 4,121 (46) | 3,322 (145) | -1,520 to +2,782 |
| No cruiser | Deaths per 100 | 4.3 | 8.3 | -9.7 to +1.1 |
| Non-radar cruiser inside | Cap taken / won | too few (3) | too few (5) | - |
| Non-radar cruiser inside | Enemy kept off | too few (5) | 62.5% (8, small n) | - |
| Non-radar cruiser inside | Concealed damage | 20,045 (8, small n) | 10,609 (9, small n) | -8,495 to +23,488 |

Radar cruiser inside minus no cruiser:
- All clans: cap taken +42.4 points (+30.3 to +58.9 *); cap won +45.3 (+28.8 to +64.8 *); enemy kept off +6.3 (+0.2 to +14.5 *, borderline); concealed damage +13,368 (+9,359 to +17,048 *); deaths +3.2 per 100 (-4.3 to +9.7).
- Top 6 only: cap taken +5.5 (-11.3 to +15.2); cap won -1.9 (-22.6 to +7.6). No gap.
- Rest only: cap taken +63.2 (+47.0 to +80.3 *); cap won +68.7 (+51.9 to +84.3 *).
- Neutral caps only, all clans: cap taken 60.0% (n 30) vs 24.5% (n 49), +35.5 (+19.0 to +51.2 *); enemy kept off 83.3% vs 87.8% (-19.6 to +10.7).

Radar cruiser inside minus non-radar cruiser inside (all clans): cap taken +25.2 (-2.5 to +51.1), cap won +10.6 (-24.6 to +44.2), enemy kept off +13.4 (-6.6 to +37.1), concealed damage +1,833 (-7,630 to +9,247), deaths -13.0 (-43.1 to +8.8). None clear.

**Top 6 or Shared:** Mixed. The radar-cruiser gain in taking the cap is a Rest pattern (clear for Rest, absent for Top 6). The Top 6 difference is on no-cruiser smokes: cap taken 48% vs 13% (clear), enemy kept off 95% vs 80% (clear). Concealed damage follows the cruiser for everyone.

**Clans:**
- Radar cruiser inside: Top 6: BONKZ 15, H-SR 14, RESIN 10, KITE 7, VRTUS 5, HTDOG 4 | Rest: -BN- 6, HFANS 6, EPOXY 5, INCA 5, MACHX 5, KSC 4, MZY 3, PFANS 3, PN 2, KITED 2, RSR 2, MACH 1, BTLST 1, UYSC 1, BONKY 1, SCCC2 1, REEEE 1.
- Non-radar cruiser inside: Top 6: H-SR 4, RESIN 2, VRTUS 1, HTDOG 1 | Rest: BTLST 2, HFANS 2, OGF 1, REEEE 1, -BN- 1, SCCC2 1, KITED 1.
- No cruiser: Top 6: RESIN 15, BONKZ 10, H-SR 7, HTDOG 6, VRTUS 5, KITE 3 | Rest: EPOXY 16, REEEE 15, HFANS 14, SCCC2 14, KITED 10, KSC 9, MACH 9, MACHX 9, -BN- 8, RSR 6, RMN 5, PFANS 4, UYSC 4, INCA 3, KSE 3, 5D 3, MZY 3, BTLST 2, OGF 2, KM 2, NGA 2, BONKY 1, MANBA 1.
- Other: Top 6: VRTUS 4, BONKZ 4, RESIN 4, HTDOG 4, H-SR 3, KITE 2 | Rest: 5D 8, HFANS 5, MACHX 5, MZY 4, MACH 4, -BN- 4, NGA 4, EPOXY 4, BTLST 3, UYSC 3, REEEE 2, KSC 2, BONKY 2, RSR 2, OGF 1, KM 1, KITED 1, KSE 1, INCA 1, PFANS 1.

**Could not be done / proxy:**
- "Cap taken" and "enemy kept off" come from cap-owner snapshots that exist only when some smoke in the game is activated or captured. Window: activation to 60 s after the smoke cleared (median 5 snapshots, never zero). A flip and flip-back between snapshots is missed. The batch's `cap_won` agrees on 169 of 211 smokes and tells the same story.
- "Enemy kept off" can only be judged where the cap was not already the enemy's. It is high everywhere (77-95%), so it separates groups poorly.
- Cover and ship are tangled: radar-cruiser smokes are mostly Somers, Gearing, Harugumo; no-cruiser smokes mostly Daring, Gdansk, Z-42.

**Verdict:** Keep.

### A2. Smoke deaths drill-down

> **Superseded in Round 5b.** Deaths, leaving the smoke and radar deaths are redone from ship tracks and the radar log: see "A2 (Round 5b)" above this part's Round 5 text. Where, when and score-state patterns below still hold in shape, but the rates use the batch death list, which undercounts. The Round 5 text is kept below for reference.


**Answer:** Deaths in destroyer smokes pile up in three conditions: the team was 50+ behind, enemy radar had a covered ship lit, or a covered ship was seen by an enemy ship. Smokes that were neither behind nor radar-flagged had 2.9 deaths per 100; 107 of 124 deaths were in the other smokes. Top 6 lose fewer ships in smoke overall (7.5 vs 13.8 per 100), but once 50+ behind they lose them at the same rate.

**Numbers:**

Who dies (124 death records in 117 of 1,074 destroyer smokes; no ship counted twice):

| Who died | n | Share | Top 6 | Rest | Inside / behind |
|---|---|---|---|---|---|
| The smoking destroyer | 69 | 56% | 11 | 58 | 65 / 4 |
| A sheltering cruiser | 48 | 39% | 15 | 33 | 27 / 21 |
| Another sheltering ship | 7 | 6% | 3 | 4 | 7 / 0 |

In smokes with a death, a sheltering cruiser was among the dead in 54% of Top 6 cases (n 28) vs 37% of Rest (n 89), -2.2 to +36.2, not clear. Cruisers lost: Des Moines 11, Minotaur 6, San Martin 5, Brisbane 5. Destroyers: Gearing 15, Somers 10, Harugumo 10, Daring 9, Shimakaze 9.

Like-with-like baselines:

| Measure | All (n) | Top 6 (n) | Rest (n) | Top 6 minus Rest |
|---|---|---|---|---|
| Destroyer died in its own smoke, per 100 destroyer smokes | 6.4 (1,074) | 2.8 (387) | 8.4 (687) | -9.6 to -2.5 * |
| Cruiser died while sheltering, per 100 sheltering cruisers | 8.2 (587) | 5.7 (262) | 10.2 (325) | -8.2 to -0.6 * |
| Destroyer hurt in its own smoke (died or lost 1/3+ of estimated health), per 100 | 15.5 | 10.6 | 18.3 | -14.0 to -3.3 * |
| Cruiser hurt while sheltering, per 100 sheltering cruisers | 22.5 | 18.3 | 25.8 | -17.7 to +2.6 |
| Any death, per 100 destroyer smokes | 11.5 | 7.5 | 13.8 | -10.9 to -2.5 * |

Health is an estimate. A cruiser inside the smoke died 7.9 per 100 (n 468), behind it 8.4 (n 119): no difference.

| Map | n (Top 6 / Rest) | Deaths per 100 | Top 6 | Rest | Top 6 minus Rest | Smoker died per 100 | Cruiser died per 100 sheltering (n) |
|---|---|---|---|---|---|---|---|
| Okinawa | 82 (15 / 67) | 22.0 [12.3 to 31.3] | 20.0 | 22.4 | -19.5 to +20.8 | 12.2 | 14.3 (42) |
| Land of Fire | 128 (48 / 80) | 14.1 | 4.2 | 20.0 | -34.2 to -2.3 * | 7.8 | 13.2 (53) |
| Sea of Fortune | 117 (38 / 79) | 13.7 | 7.9 | 16.5 | -25.9 to +3.4 | 8.5 | 6.8 (73) |
| Sleeping Giant | 238 (110 / 128) | 11.8 | 6.4 | 16.4 | -19.6 to -2.3 * | 7.1 | 7.3 (137) |
| Loop | 142 (41 / 101) | 10.6 | 9.8 | 10.9 | -14.5 to +11.2 | 6.3 | 7.8 (51) |
| Mountain Range | 132 (55 / 77) | 8.3 | 7.3 | 9.1 | -13.5 to +11.4 | 3.8 | 8.3 (72) |
| Hotspot | 235 (80 / 155) | 7.7 [5.2 to 10.2] | 7.5 | 7.7 | -6.2 to +6.4 | 3.4 | 6.3 (159) |

Caps with the most deaths per 100 (nearest cap, team-normalized letter): Okinawa C 25.0 (n 40, 10 deaths), Sleeping Giant C 21.4 (n 28, 6), Sea of Fortune C 21.1 (n 19, 4), Okinawa A 19.2 (n 26, 5). Lowest large caps: Hotspot C 5.2 (n 77), Sleeping Giant D 6.0 (n 67), Loop A 6.8 (n 59). All intervals wide.

| Smoke activated | n | Deaths per 100 | Top 6 | Rest | Top 6 minus Rest | Cruiser died per 100 sheltering (n) |
|---|---|---|---|---|---|---|
| 0-5 min | 302 | 7.6 | 2.9 | 10.0 | -12.7 to -1.7 * | 5.2 (213) |
| 5-10 min | 495 | 12.5 | 8.3 | 14.9 | -13.8 to +0.2 | 8.1 (270) |
| 10-15 min | 248 | 14.1 | 9.4 | 17.1 | -17.3 to +0.7 | 14.4 (97) |
| 15-20 min | 29 | 13.8 | 22.2 (n 9, small n) | 10.0 | -5.6 to +27.3 | too few (7) |

| Score at activation | n | Deaths per 100 | Top 6 | Rest | Top 6 minus Rest | Smoker died per 100 | Cruiser died per 100 sheltering (n) |
|---|---|---|---|---|---|---|---|
| Ahead 50+ | 372 | 6.5 | 5.4 | 7.3 | -6.5 to +3.0 | 3.8 | 4.8 (187) |
| Level | 425 | 8.5 | 3.7 | 11.4 | -11.8 to -4.3 * | 3.8 | 6.9 (288) |
| Behind 50+ | 277 | 23.1 [17.2 to 30.3] | 23.7 | 22.9 | -13.9 to +13.5 | 14.1 | 17.0 (112) |

The clock matters little once score is held: 5-10 min and behind 25.2 (n 155), 10-15 min and behind 22.5 (n 89), vs 5.5 (n 183) and 8.5 (n 141) when ahead. Ships died: 12 in the first 5 minutes, 54 in 5-10, 50 in 10-15, 8 after.

Radar deaths (two readings):
- Strict (`radar_lit`: a radar-detection row for that ship in that smoke in its last 40 s; names the radar ship): 19 of 124 (15%). Top 6 3, Rest 16. 13 smoking destroyers, 4 cruisers, 2 others.
- Broad (the ship's own detection list shows the radar flag in its last 40 s): 45 of 124 (36%). Top 6 5, Rest 40. 27 destroyers, 16 cruisers, 2 others. 24 were also seen by an enemy ship.
- Strict by map: Sleeping Giant 7, Loop 5, Hotspot 2, Okinawa 2, Sea of Fortune 2, Land of Fire 1, Mountain Range 0. By cap: Loop B 3, Sleeping Giant A 3, Loop C 2, Sleeping Giant C 2. Broad: Sleeping Giant 12, Hotspot 7, Loop 7, Okinawa 7, Land of Fire 5, Sea of Fortune 5, Mountain Range 2; caps Sleeping Giant A 5, Hotspot D 4, Sleeping Giant B 4, Okinawa A 4.
- Strict by time: 0-5 min 4, 5-10 min 7, 10-15 min 5, 15-20 min 3. By score: behind 11, level 5, ahead 3.
- Radar ship (strict): cruiser 16, destroyer 3. Moskva 6, Brisbane 3, Petropavlovsk 3, San Martin 2, Gdansk 2, Smaland 1, Des Moines 1, Minotaur 1.
- Distance from the radar ship (strict): median 10.0 km (quarter marks 7.5 and 10.9; range 3.5 to 11.7). Median 85% of that ship's radar range; 14 of 19 beyond 80%. Cruiser radars median 10.1 km (n 16); destroyer radars 7.0 km (n 3, too few).
- Killing damage (strict 19): shells in 16; biggest share from cruisers 8, destroyers 7, battleships 3. No torpedoes.

| Destroyer smokes | n (Top 6 / Rest) | Deaths per 100 | Top 6 | Rest | Top 6 minus Rest |
|---|---|---|---|---|---|
| Radar reached (strict) | 120 (44 / 76) | 25.0 [16.5 to 37.5] | 13.6 | 31.6 | -35.2 to +3.9 |
| No radar (strict) | 954 | 9.9 | 6.7 | 11.6 | -9.9 to -0.7 * |
| Radar flag on a covered ship (broad) | 297 (111 / 186) | 27.9 [22.2 to 35.4] | 17.1 | 34.4 | -25.9 to -7.6 * |
| No radar flag (broad) | 777 | 5.3 [3.3 to 7.9] | 3.6 | 6.2 | -6.8 to +1.1 |
| Radar (strict) and behind 50+ | 36 | 44.4 [28.9 to 64.9] | 33.3 (n 9, small n) | 48.1 | -46.6 to +14.0 |
| Radar (strict) and level | 48 | 20.8 | 5.6 | 30.0 | -52.2 to -5.3 * |
| Radar (strict) and ahead 50+ | 36 | 11.1 | 11.8 | 10.5 | -19.7 to +25.0 |
| Radar (strict), Sleeping Giant | 33 (13 / 20) | 30.3 | 0.0 | 50.0 | -70.4 to -27.8 * |
| Radar (strict), Loop | 12 (small n) | 41.7 | too few | 40.0 | - |
| Radar (strict), Okinawa | 10 (small n) | 50.0 | too few | too few | - |
| Radar from an enemy cruiser (strict) | 101 | 24.8 | 14.7 | 29.9 | -34.7 to +14.6 |
| Radar from an enemy destroyer (strict) | 16 | 31.2 [7.7 to 58.8] | 11.1 (n 9, small n) | too few | - |

Radar vs not: +15.1 per 100 (+6.2 to +26.6 *) strict; +22.7 (+16.6 to +29.6 *) broad. Radar reaches Top 6 and Rest smokes equally often (11.4% vs 11.1% strict; 28.7% vs 27.1% broad).

What else goes with deaths (deaths per 100 destroyer smokes, with vs without):

| Condition | n with | With | Without | Difference | Smoker died per 100, with / without | Cruiser died per 100 sheltering, with / without |
|---|---|---|---|---|---|---|
| Team outnumbered at activation | 198 | 27.3 | 8.0 | +11.7 to +27.5 * | 16.7 / 4.1 * | 24.3 / 5.8 * |
| A covered ship carried the radar flag (broad) | 297 | 27.9 | 5.3 | +17.0 to +29.1 * | 15.2 / 3.1 * | 17.1 / 3.6 * |
| A covered ship lit for firing from the smoke | 203 | 25.1 | 8.4 | +9.4 to +24.8 * | 9.9 / 5.6 | 15.9 / 5.2 * |
| 50+ behind at activation | 277 | 23.1 | 7.5 | +9.1 to +22.0 * | 14.1 / 3.8 * | 17.0 / 6.1 * |
| Enemy radar reached a ship (strict) | 120 | 25.0 | 9.9 | +5.7 to +27.1 * | 13.3 / 5.6 * | 16.4 / 7.0 * |
| Smoker seen by an enemy ship | 233 | 22.7 | 8.4 | +8.9 to +20.6 * | 15.9 / 3.8 * | 13.7 / 7.0 * |
| Any covered ship seen by an enemy ship | 512 | 19.1 | 4.6 | +10.7 to +19.0 * | 10.2 / 3.0 * | 12.3 / 2.7 * |
| Enemy hydro reached a covered ship | 17 | 35.3 | 11.2 | +2.9 to +43.2 * | 17.6 / 6.2 | 20.0 / 8.0 |
| Enemy destroyer within 6 km when laid | 145 | 17.9 | 10.5 | -0.2 to +16.2 | 13.8 / 5.3 * | 18.8 / 7.6 |
| Smoker already spotted at activation | 316 | 15.2 | 10.0 | -0.0 to +11.1 | 12.7 / 3.8 * | 8.5 / 8.1 |
| Smoker under half health at activation | 234 | 15.4 | 10.5 | -0.1 to +10.2 | 9.8 / 5.5 * | 14.1 / 7.3 |
| A cruiser sheltering | 535 | 13.6 | 9.5 | -0.0 to +9.2 | 3.9 / 8.9 * (lower) | - |
| Smoke centre inside the cap | 290 | 12.1 | 11.4 | -4.3 to +6.3 | 6.9 / 6.2 | 9.8 / 7.8 |
| First 5 minutes | 302 | 7.6 | 13.1 | -9.4 to -1.5 * (lower) | 3.6 / 7.5 * | 5.2 / 9.9 * |

- An enemy destroyer close by, being spotted already, or low health go with the smoking destroyer dying (about 13 per 100 vs 4-5), not with the cruiser dying.
- A ship lit for firing from the smoke goes with the cruiser dying (15.9 vs 5.2), not the destroyer.
- When a cruiser shelters, the destroyer itself dies less (3.9 vs 8.9).
- Inside the cap or not makes no difference.
- Seen by an enemy ship + radar (strict) + behind 50+: 57.1 deaths per 100 (n 21). None of the three: 2.5 (n 394).
- Smokes neither 50+ behind nor radar-flagged (strict or broad): 585 smokes, 17 deaths, 2.9 per 100 (Top 6 2.1, Rest 3.5, -4.2 to +0.9). Inside those, only "a covered ship seen by an enemy ship" (5.5 vs 1.2, +1.4 to +8.4 *) and "lit for firing" (6.5 vs 2.1, +0.7 to +8.8 *) still stand out.
- Of the 105 deaths without a strict radar row: 53 were 50+ behind, 30 seen by an enemy ship in the last 40 s, 27 carried the broad radar flag, 27 died just after the smoke cleared, 11 lit for firing, 6 took torpedo damage in the last 20 s, 4 lit by hydro; 13 carry none of these.
- Torpedoes are rare: 6 of 124 deaths had torpedo damage in the last 20 s; shells were the top damage in 102.
- 27 of 124 (22%) died just after the smoke cleared: 12 destroyers, 12 cruisers.

Other smoker classes:

| Smoker class | n (Top 6 / Rest) | Smoker died per 100 | Top 6 | Rest | Top 6 minus Rest | Radar reached / not | 50+ behind / not |
|---|---|---|---|---|---|---|---|
| Destroyer | 1,074 (387 / 687) | 6.4 | 2.8 | 8.4 | -10.2 to -2.0 * | 13.3 (120) / 5.6 * | 14.1 (277) / 3.8 * |
| Cruiser | 439 (141 / 298) | 10.0 | 7.8 | 11.1 | -7.0 to -0.0 (borderline) | 34.1 (44) / 7.3 * | 15.7 (153) / 7.0 * |
| Battleship | 34 (10 / 24) | 8.8 | 10.0 (small n) | 8.3 | -11.7 to +11.8 | too few (6) | 23.1 (13, small n) / 0.0 |

Moving exhaust smokes: smoker died 16.1 per 100 (n 168; Napoli 22 of 44 cruiser smoker deaths). Parked cruiser smokes: 6.3 (n 271).

**Top 6 or Shared:** Top 6 pattern for the overall rate (7.5 vs 13.8 *; own destroyer 2.8 vs 8.4 *; sheltering cruiser 5.7 vs 10.2 *). The conditions are Shared: behind 50+ costs both the same (23.7 vs 22.9), radar reaches both equally often, calm smokes show no gap. The Top 6 edge shows when level (3.7 vs 11.4 *), in the first 5 minutes (2.9 vs 10.0 *), on Sleeping Giant (6.4 vs 16.4 *) and Land of Fire (4.2 vs 20.0 *), and under radar at level score (5.6 vs 30.0 *).

**Clans:**
- Strict radar deaths (19): Top 6: KITE 1, HTDOG 1, RESIN 1 | Rest: RSR 3, MANBA 1, KM 1, -BN- 1, SCCC2 1, BTLST 1, INCA 1, KITED 1, UYSC 1, MZY 1, PFANS 1, REEEE 1, HFANS 1, EPOXY 1.
- Broad radar deaths (45): Top 6: BONKZ 2, RESIN 2, HTDOG 1 | Rest: HFANS 5, BTLST 4, UYSC 4, -BN- 3, RSR 3, EPOXY 3, REEEE 3, KITED 2, MZY 2, PFANS 2, 5D 2, MANBA 1, BONKY 1, KM 1, SCCC2 1, KSE 1, INCA 1, MACH 1.
- Smokes with a death at Okinawa C: Top 6: KITE 1 | Rest: EPOXY 2, BTLST 1, 5D 1, PN 1, REEEE 1, MZY 1. Sleeping Giant C: Top 6: RESIN 1, BONKZ 1 | Rest: RSR 2, UYSC 1, SCCC2 1. Sea of Fortune C: Top 6: BONKZ 1 | Rest: 5D 1, UYSC 1, MACHX 1. Okinawa A: Top 6: HTDOG 1 | Rest: HFANS 2, -BN- 1, REEEE 1.

**Could not be done / proxy:**
- Leaving the smoke: no position track. Proxies: died just after the smoke cleared (27), died behind rather than inside (25).
- Spotted by an enemy destroyer: the batch says "seen by an enemy ship" but not which. Proxies: surface lit; an enemy destroyer within 6 km at the one recorded moment.
- Smoke dispersing early: `emission_cut_short` looks strong (36.0 vs 10.4, n 50) but in 15 of the 50 the smoker died while laying, which is what cut it short (median 4 s lost). In calm smokes, cut-short smokes had no deaths (n 12, small n). Not usable as a risk.
- Torpedoes: only damage that landed is logged.
- Radar ship and distance exist only for the strict 19 deaths.
- Death position is unknown; the map figure plots smoke centres.
- Cap-level intervals are wide: leads, not findings.

**Verdict:** Lead.

### A3. Somers vs Gearing deaths

**Answer:** The gap is team, not ship. Inside the Top 6 the two ships lose ships at the same rate (7.8 vs 9.5 per 100). The whole gap sits in the Rest (11.8 vs 23.6).

**Numbers:** Somers 260 smokes (90 / 170); Gearing 180 (74 / 106).

| Scope | Measure | Somers (n) | Gearing (n) | Somers minus Gearing |
|---|---|---|---|---|
| All clans | Any death per 100 smokes | 10.4 (260) | 17.8 (180) | -7.4 (-17.7 to -0.4 *) |
| All clans | Smoker died per 100 | 3.8 | 8.3 | -4.5 (-16.4 to +2.0) |
| All clans | Cruiser died per 100 sheltering | 7.3 (234) | 9.4 (149) | -2.1 (-7.2 to +3.4) |
| All clans | Concealed damage | 14,524 | 16,296 | -1,771 (-5,334 to +3,247) |
| Top 6 only | Any death per 100 | 7.8 (90) | 9.5 (74) | -1.7 (-6.9 to +4.7) |
| Top 6 only | Smoker died per 100 | 2.2 | 1.4 | +0.9 (-7.7 to +5.7) |
| Top 6 only | Cruiser died per 100 sheltering | 5.9 (85) | 6.8 (73) | -1.0 (-7.1 to +7.0) |
| Rest only | Any death per 100 | 11.8 (170) | 23.6 (106) | -11.8 (-24.0 to -1.5 *) |
| Rest only | Smoker died per 100 | 4.7 | 13.2 | -8.5 (-25.3 to +1.6) |
| Rest only | Cruiser died per 100 sheltering | 8.1 (149) | 11.8 (76) | -3.8 (-10.4 to +6.5) |

Top 6 vs Rest on the same ship: Somers 7.8 vs 11.8 (-10.8 to +1.3); Gearing 9.5 vs 23.6 (-26.8 to -4.8 *), smoker died 1.4 vs 13.2 (-28.8 to -0.8 *).

| Same mix of | Somers | Gearing | Difference (any death per 100) |
|---|---|---|---|
| Group | 10.3 | 18.3 | -8.0 (-16.9 to -1.6 *) |
| Map | 10.5 | 17.4 | -6.9 (-15.8 to -0.5 *) |
| Group and map | 10.1 | 18.1 | -8.0 (-19.3 to -2.4 *) |
| Group, map and score state | 11.1 | 16.9 | -5.8 (-16.5 to +2.2) |
| Clan (174 smokes of clans that used both) | 7.1 | 10.7 | -3.6 (-16.3 to +6.0) |

Gearing smokes were laid 50+ behind more often (25.0% vs 17.3%, -18.9 to +0.3).

Within map (any death per 100):
- Sea of Fortune: 3.8 (n 26) vs 26.3 (n 19), -50.0 to -3.3 *. Rest only: 5.0 (n 20) vs 44.4 (n 9, small n), -66.7 to -5.2 *.
- Mountain Range, Top 6 only: 0.0 (n 14, small n) vs 20.0 (n 15), -38.9 to -7.1 *. All clans 6.1 vs 14.7, not clear.
- Loop, Rest only, smoker died: 0.0 (n 10, small n) vs 44.4 (n 9, small n), -66.7 to -10.0 *.
- Hotspot (6.8 vs 4.7), Sleeping Giant (12.0 vs 18.2), Land of Fire (18.2 vs 22.7), Okinawa (16.7 vs 23.5, small n): no clear gap.

Only two clans have 8+ smokes with each ship: BONKZ (8.3, n 12; 10.8, n 37) and -BN- (0.0, n 12; 11.1, n 18).

**Top 6 or Shared:** The dividing line is Top 6 vs Rest, not the ship. Top 6: level (-6.9 to +4.7). Rest: Gearing smokes lose twice as many ships (clear).

**Clans:**
- Somers: Top 6: RESIN 38, H-SR 33, BONKZ 12, VRTUS 7 | Rest: HFANS 28, REEEE 25, MZY 22, EPOXY 18, MACHX 17, BONKY 14, -BN- 12, NGA 11, PFANS 8, PN 5, UYSC 5, KITED 3, RSR 1, INCA 1.
- Gearing: Top 6: BONKZ 37, KITE 23, VRTUS 10, HTDOG 4 | Rest: KSC 29, -BN- 18, BTLST 11, 5D 9, OGF 9, RSR 9, INCA 7, HFANS 5, RMN 3, EPOXY 3, KM 2, UYSC 1.
- Rest Gearing (smokes, deaths, of which the Gearing itself): KSC 29, 6, 0; -BN- 18, 2, 0; BTLST 11, 4, 3; 5D 9, 6, 6; OGF 9, 3, 2; RSR 9, 2, 2. Leaving any one clan out, the Rest rate stays between 19.6 and 26.1.
- Top 6 Gearing: BONKZ 37 smokes, 4 deaths; KITE 23, 2; VRTUS 10, 1; HTDOG 4, 0. One Top 6 Gearing died in its own smoke.

**Could not be done / proxy:** Almost no clan flies both ships, so ship and clan cannot be fully separated. Top 6 within-map cells are too few on Sea of Fortune, Land of Fire, Loop and Okinawa.

**Verdict:** Keep.

### A4. Counter-smokes: which ones pay?

**Answer:** Flanking counter-smokes do not pay: rare (12 of 132), lower return (2.9k vs 8.9k head-on, clear), and no fewer deaths (25 vs 15 per 100, not clear). The ones that paid had a radar cruiser inside (18.3k, out-damaged the answered smoke 59% of the time) or were laid 11-25 s after the enemy smoke.

**Numbers:** 133 destroyer counter-smokes (44 Top 6, 89 Rest); round 3 module 5 definition (`counter_smoke_of` names an enemy smoke laid in the previous 45 s; matched on game + id). All 133 match (102 answer a destroyer smoke, 27 a cruiser smoke, 4 a battleship smoke).

Geometry:
- Centre-to-centre distance: median 9.0 km (quarter marks 7.2 and 10.2). 77% at the same cap. Median delay 17 s.
- Line of fire of the enemy smoke = direction from the enemy smoke to the damage-weighted middle of the ships it hit (positions when that smoke was fully laid). If it hit nobody with a known position: direction to the middle of our ships at that moment. Usable for 132 of 133 pairs (94 from ships hit, 38 fallback, 1 neither).
- Angle = how far our counter-smoke sits off that line, measured at the enemy smoke. Bands fixed before looking at outcomes: head-on under 30 degrees, oblique 30-60, flanking over 60.
- Median angle 12 degrees. Head-on 100, oblique 20, flanking 12.
- Own-frame bearing: answered smoke within 30 degrees of straight ahead 65, 30-60 degrees off 46, abeam or behind 22.

| Angle off the enemy's line of fire | n (Top 6 / Rest) | Concealed damage | Deaths per 100 | Smoker died per 100 | Out-damaged the answered smoke | Margin (ours minus theirs) |
|---|---|---|---|---|---|---|
| Head-on (under 30) | 100 (35 / 65) | 8,947 [5,784 to 12,171] | 15.0 [8.8 to 23.5] | 7.0 | 42.0% [34.3 to 50.0] | +452 [-2,822 to +3,844] |
| Oblique (30-60) | 20 (6 / 14) | 6,762 [3,076 to 10,161] | 10.0 [0.0 to 25.0] | 5.0 | 30.0% | -6,019 [-13,529 to +415] |
| Flanking (over 60), small n | 12 (3 / 9) | 2,868 [816 to 6,823] | 25.0 [0.0 to 50.0] | 16.7 | 16.7% | -2,928 [-7,299 to +1,588] |

- Flanking minus head-on: damage -6,079 (-10,197 to -1,583 *); deaths +10.0 (-13.1 to +35.0); smoker died +9.7 (-8.0 to +30.7); out-damaged -25.3 points (-47.6 to +1.5).
- Split at 45 degrees: 3,801 (n 18) vs 8,736 (n 114), -4,935 (-8,889 to -1,179 *); deaths 16.7 vs 14.9.
- Check, line of fire only from ships actually hit (94 pairs): head-on 9,843 (n 71), oblique 7,234 (n 14, small n), flanking 3,457 (n 9, small n).
- Check, leaving our own counter-smoking destroyer out of the ships hit (71 pairs): 13,489 (n 44), 6,048 (n 17), 3,648 (n 10, small n; deaths 30.0).
- Habit mix: 9 of 12 flanking counter-smokes are cap-sitter ships. Inside cap sitters: head-on 4,397 (n 53), oblique 3,947 (n 12, small n), flanking 1,737 (n 9, small n). Inside flank-smoke-line ships: head-on 14,769 (n 41), oblique 10,984 (n 8, small n), flanking too few (3).
- Top 6 vs Rest: flanking is 6.8% of Top 6 counter-smokes, 10.2% of Rest (-13.6 to +9.2). Top 6 flanking n 3 (too few). Rest only: flanking 2,902 (n 9, small n) vs head-on 6,928 (n 65), -8,727 to +1,115; deaths 33.3 vs 15.4, -13.4 to +50.7.

What pays (high cells only):

| Counter-smoke | n (Top 6 / Rest) | Concealed damage | Deaths per 100 | Out-damaged the answered smoke | Margin |
|---|---|---|---|---|---|
| All counter-smokes | 133 (44 / 89) | 8,003 [5,499 to 10,381] | 15.0 | 37.6% [31.1 to 43.5] | -830 [-3,662 to +1,612] |
| Radar cruiser inside | 32 (15 / 17) | 18,316 [13,065 to 23,380] | 18.8 | 59.4% [47.6 to 75.0] | +8,502 [+2,611 to +15,424 *] |
| Gearing | 20 (11 / 9) | 21,202 [13,145 to 27,187] | 35.0 [14.8 to 72.7] | 60.0% | +12,873 [+6,225 to +18,249 *] |
| Flank-smoke-line ships | 52 (19 / 33) | 13,696 [8,536 to 18,481] | 23.1 | 46.2% | +4,411 [-180 to +9,465] |
| Laid 11-25 s after the enemy smoke | 43 (15 / 28) | 12,296 [7,566 to 17,655] | 18.6 | 46.5% | +975 [-5,964 to +7,335] |
| 6-9 km from the answered smoke | 51 (17 / 34) | 9,740 | 19.6 | 39.2% | +383 |
| Answered smoke within 30 degrees of straight ahead | 65 (22 / 43) | 9,023 | 16.9 | 43.1% | +1,592 [-2,318 to +5,543] |

- Gearing's return comes with the highest death rate, and the deaths are the Rest's: Top 6 9.1 per 100 (n 11, small n), Rest 66.7 (n 9, small n: 6 deaths in 9 smokes, 4 of them cruisers), -80.9 to -31.9 *.
- Top 6 vs Rest overall: 11,140 vs 6,452 (-340 to +8,928, not clear); deaths 11.4 vs 16.9 (-17.1 to +7.7). In the 11-25 s window Top 6 returned 19,064 vs 8,670 (+2,070 to +21,922 *).
- For comparison only: counter-smokes with no cruiser lost the head-to-head by 4,834 (-8,327 to -1,462 *).

**Top 6 or Shared:** Shared. Same frequency (round 3: 11% vs 13%), same angles (median 10 vs 13 degrees), same distance (9.1 vs 8.7 km), no clear overall gap on return or deaths. One clear Top 6 edge: the 11-25 s window.

**Clans:**
- Head-on (100): Top 6: BONKZ 13, HTDOG 7, VRTUS 5, KITE 4, RESIN 3, H-SR 3 | Rest: EPOXY 10, HFANS 9, REEEE 6, MACHX 5, KITED 4, SCCC2 4, MZY 4, KSC 4, OGF 2, PN 2, INCA 2, NGA 2, RSR 2, -BN- 2, PFANS 2, 5D 1, MACH 1, BONKY 1, MANBA 1, UYSC 1.
- Oblique (20): Top 6: KITE 2, HTDOG 2, RESIN 1, H-SR 1 | Rest: MACHX 2, -BN- 2, SCCC2 2, MACH 2, HFANS 2, NGA 1, BTLST 1, KSC 1, MZY 1.
- Flanking (12): Top 6: KITE 2, RESIN 1 | Rest: HFANS 2, 5D 2, -BN- 1, BONKY 1, SCCC2 1, KSE 1, MACHX 1.
- Radar cruiser inside (32): Top 6: BONKZ 9, KITE 3, H-SR 2, HTDOG 1 | Rest: HFANS 5, BONKY 2, EPOXY 2, SCCC2 2, KITED 1, INCA 1, KSC 1, PFANS 1, REEEE 1, -BN- 1.
- Gearing (20): Top 6: BONKZ 8, KITE 3 | Rest: KSC 3, OGF 2, -BN- 2, BTLST 1, 5D 1.
- Laid 11-25 s after (43): Top 6: KITE 6, HTDOG 3, BONKZ 3, RESIN 1, VRTUS 1, H-SR 1 | Rest: HFANS 4, SCCC2 3, MACHX 3, REEEE 3, EPOXY 3, -BN- 2, KSC 2, KM 1, KITED 1, OGF 1, MANBA 1, MACH 1, BONKY 1, UYSC 1, PFANS 1.

**Could not be done / proxy:**
- The batch does not record where a smoke's ships were aiming; the line of fire is built from the ships the enemy smoke hit, at one moment. Our counter-smoking destroyer was one of those ships in 54 of 133 pairs, which pulls the angle toward head-on; the check leaving it out gives the same order.
- 12 flanking counter-smokes (3 Top 6): the Top 6 vs Rest question on flanking cannot be answered.
- "Fewer deaths" cannot be shown either way: every death interval by angle includes zero.
- Whether a counter-smoke reduced what the answered smoke did cannot be seen. Proxy: the margin.

**Verdict:** Keep (radar cruiser inside and timing pay; angle does not). Drop the flanking idea.

---

## Part B (Round 5b): Harugumo per shot (B3); Loop Daring after radar (C5-LP-4)

Source: `new-n3/FINDINGS-N3.md`.


Batch `output/20261117-230933` (smoke-signals 0.4.0). Scripts in `round5b/new-n3/`. Everything here is association, not cause. Intervals are 95%, from resampling whole clans; a star or the word "clear" means the interval excludes zero. Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS.

### B3. Harugumo: who is near, and what lights, its targets at the time of each shot

**Answer:** The round 5 reading mostly holds, with two corrections. Per shot, the nearest friendly ship to a Harugumo's target is a ship outside the smoke or a second destroyer 69% of the time (round 5 snapshot: 67%), and the radar cruiser sitting in the smoke almost never (2 of 410 shots). The radar log agrees: only 3% of its shots are at a target lit by a radar ship inside the smoke. The corrections: the Harugumo itself is the nearest ship more often than the snapshot said (31%, not 21%), and round 5's "a second destroyer is recorded more often with a Harugumo" needs rewording: the snapshot only held ships near the smoke, so "recorded" meant "close by". A second destroyer is alive at nearly every smoke of all three ships; what differs is that it stays closer to a Harugumo smoke.

**What was counted.** For every smoke by a Harugumo, Somers, Gearing or Delny, the damage events where the smoker is the attacker and the event is credited to its own smoke (shells, the fires they start, torpedoes), from the run of the smoker's own team. A "shot" is one firing moment at one target. At that moment the tracks give every ship's position, the target's own track says whether the enemy team was detected, and the radar log says whether it was radar-lit and by which ship.

**Numbers (what there is to count):**

| Ship | Smokes | Smokes with own-gun damage | Clans in those | Top 6 / Rest smokes | Shots | Damage events | Own-gun damage | Smoke-target pairs | Largest single smoke, share of damage |
|---|---|---|---|---|---|---|---|---|---|
| Harugumo | 100 | 44 | 10 | 25 / 19 | 410 | 898 | 461,873 | 68 | 13% |
| Somers | 260 | 26 | 12 | 6 / 20 | 83 | 152 | 253,013 | 35 | 21% |
| Gearing | 180 | 18 | 8 | 5 / 13 | 64 | 177 | 94,724 | 21 | 31% |
| Delny | 22 | 2 | 2 | 1 / 1 | 2 | 2 | 3,872 | 2 | 92% |

Delny has 2 shots: too few, not reported further. Somers and Gearing rest on 83 and 64 shots from 26 and 18 smokes, so their intervals are wide.

**Numbers (nearest friendly ship to the target, at each shot).** Three weightings: share of shots, share of own-gun damage, and the average of each smoke's own split (so one long burst counts once).

| Nearest friendly ship to the target | Harugumo: shots (n; interval) / damage / per smoke | Somers: shots (n; interval) / damage / per smoke | Gearing: shots (n; interval) / damage / per smoke |
|---|---|---|---|
| A ship outside the smoke | 45% (183; 27 to 59) / 55% / 42% | 37% (31; 16 to 61) / 28% / 28% | 8% (5; 2 to 15) / 11% / 15% |
| A second destroyer | 24% (99; 14 to 32) / 20% / 25% | 11% (9; 0 to 24) / 13% / 10% | 2% (1; 0 to 4) / 0% / 6% |
| The smoker itself | 31% (126; 15 to 55) / 24% / 31% | 48% (40; 29 to 67) / 51% / 54% | 91% (58; 84 to 98) / 88% / 79% |
| Another ship in or behind the smoke | 0% (0; 0 to 0) / 0% / 0% | 0% (0; 0 to 0) / 0% / 0% | 0% (0; 0 to 0) / 0% / 0% |
| The radar cruiser inside the smoke | 0% (2; 0 to 2) / 0% / 2% | 4% (3; 0 to 8) / 8% / 8% | 0% (0; 0 to 0) / 0% / 0% |

- Median distance from that nearest ship to the target: Harugumo 7.3 km, Somers 5.6 km, Gearing 5.9 km. Median range from the smoker to its target: 9.9 / 7.1 / 5.8 km. The Harugumo shoots from further away.
- Harugumo minus Somers, share of shots: a ship outside +7.3 (-20.2 to +34.9), not clear; second destroyer +13.3 (-4.7 to +26.0), not clear; the smoker itself -17.5 (-41.5 to +10.4), not clear (per smoke -23.0 (-42.2 to -3.8 *), clear); radar cruiser inside -3.1 (-7.7 to +1.3), not clear.
- Harugumo minus Gearing, share of shots: a ship outside +36.8 (+17.3 to +52.5 *), clear; second destroyer +22.6 (+11.6 to +30.2 *), clear; the smoker itself -59.9 (-79.5 to -32.8 *), clear.
- "In or behind the smoke" here is geometric at the firing moment (inside the smoke, or within 3 km of it with the smoke on the line to the target). Round 5 used the batch label, which also counted any ship that had the smoke in its line of fire at some time in the smoke's life.

**Numbers (was the target detected, and was it radar-lit, at each shot):**

| At the shot, the target was | Harugumo: shots (n; interval) / damage / per smoke | Somers: shots (n; interval) / damage / per smoke | Gearing: shots (n; interval) / damage / per smoke |
|---|---|---|---|
| Radar-lit at the shot | 22% (89; 7 to 32) / 19% / 30% | 26% (22; 11 to 41) / 9% / 26% | 42% (27; 23 to 66) / 28% / 35% |
| ... by a radar ship inside this smoke | 3% (13; 0 to 13) / 2% / 3% | 7% (6; 0 to 16) / 3% / 12% | 3% (2; 0 to 16) / 3% / 6% |
| ... by a radar ship elsewhere | 18% (75; 4 to 28) / 17% / 25% | 18% (15; 5 to 33) / 7% / 14% | 39% (25; 17 to 58) / 25% / 29% |
| Detected, not radar-lit | 72% (296; 61 to 87) / 66% / 60% | 64% (53; 48 to 80) / 60% / 54% | 42% (27; 24 to 52) / 53% / 40% |
| Not detected at the shot | 6% (25; 3 to 9) / 14% / 10% | 10% (8; 6 to 13) / 30% / 21% | 16% (10; 4 to 32) / 19% / 26% |

- The direct test of "the radar cruiser inside spots for it": 187 Harugumo shots came from 25 smokes that had a radar cruiser inside. In 13 of them (7%) the target was lit by a radar ship inside that smoke at the shot; in 27% it was radar-lit by anyone. Without a radar cruiser inside (223 shots, 19 smokes) 18% were radar-lit. Somers: 6 of 34 shots (18%). Gearing: 2 of 9 (22%, small n).
- When a Harugumo target is radar-lit (89 shots), the radar ship is elsewhere on the map in 75 and inside the smoke in 13 (all cruisers); 1 could not be attributed and 8 had more than one possible radar. Radar ships: Salem 29, Moskva 27, Stalingrad 9, Worcester 9, Petropavlovsk 7, Des Moines 4. Hydro lit the target in 16 shots.
- Most shots are at targets that are detected without radar (72% of Harugumo shots). For those, the nearest friendly ship is a ship outside the smoke in 125, a second destroyer in 71, the Harugumo itself in 99, the radar cruiser inside in 1. A ship sitting in smoke does not see out of it beyond about 2 km, so "the smoker itself is nearest" does not mean the smoker spotted; it means no friendly ship was closer.
- A second stand-in: is there a friendly ship outside the smoke within the target's own listed detection range? Harugumo: a second destroyer is the closest such ship in 32% of shots, another ship in 53%, nobody in 11%. Somers 20% / 57% / 16%. Gearing 14% / 39% / 36%. Harugumo minus Gearing, nobody in range: -25.0 (-61.5 to -6.6 *), clear.
- "Not detected at the shot" (6% of Harugumo shots, 14% of damage): by damage this is torpedo 47%, fire 31%, shell 22% for the Harugumo, and torpedoes 95% for the Somers. Torpedoes are launched at ships nobody sees, and fire ticks keep landing after the target goes dark; the shell part is blind fire or the 2 s sampling step.

**Numbers (the second destroyer).** "Second destroyer" = the allied destroyer nearest to the smoke, other than the smoker.

| Measure | Harugumo (410 shots, 100 smokes) | Somers (83 shots, 260 smokes) | Gearing (64 shots, 180 smokes) |
|---|---|---|---|
| Shots with a second destroyer alive | 99% (405 of 410) | 100% (83 of 83) | 92% (59 of 64) |
| At the shot: its median distance to the smoke | 5.2 km | 9.7 km | 17.3 km |
| At the shot: within 3 km of the smoke | 28% | 16% | 11% |
| At the shot: within 5 km | 47% | 24% | 11% |
| At the shot: 1 km or more forward of the smoke | 42% | 22% | 41% |
| At the shot: in or behind the smoke | 8% | 2% | 0% |
| At the shot: sitting in a cap | 25% | 25% | 30% |
| Smoke life: share of standing time with an allied destroyer within 3 km (all smokes) | 20% (12 to 24) | 8% (5 to 11) | 6% (3 to 11) |
| Smoke life: within 5 km | 32% (23 to 38) | 14% (8 to 19) | 13% (7 to 18) |
| Smoke life: within 5 km and 1 km+ forward | 17% (10 to 24) | 6% (3 to 8) | 7% (4 to 11) |
| Smoke life: 1 km+ forward at any distance | 58% (49 to 69) | 66% (62 to 71) | 55% (48 to 60) |
| Smoke life: inside the smoke | 3% (1 to 4) | 2% (0 to 3) | 1% (0 to 1) |
| Smoke life: an allied second destroyer alive at all | 94% (85 to 99) | 98% (96 to 100) | 93% (89 to 96) |

- Over the smoke's life, Harugumo minus Somers: within 3 km +11.4 (+5.2 to +16.2 *), clear; within 5 km +17.4 (+8.4 to +26.1 *), clear; within 5 km and forward +11.6 (+4.8 to +18.0 *), clear. Harugumo minus Gearing: within 3 km +13.4 (+4.6 to +18.5 *), clear; within 5 km +18.8 (+9.3 to +26.2 *), clear; within 5 km and forward +10.0 (+3.1 to +17.0 *), clear.
- At the shot, Harugumo minus Somers: within 5 km +23.0 (-6.5 to +50.4), not clear; 1 km+ forward +20.5 (-10.4 to +41.6), not clear. Harugumo minus Gearing: within 5 km +36.1 (+12.3 to +61.6 *), clear; in or behind the smoke +7.6 (+1.7 to +14.9 *), clear. Per-shot gaps are mostly not clear because few clans supply the Somers and Gearing shots.
- The Harugumo's second destroyer is most often a Marceau (106 shots), Somers (66 shots), Châteaurenault (66 shots), Lüshun (32 shots).

**Top 6 or Shared:** Shared, with one lead. Harugumo shots: Top 6 223 from 25 smokes (4 clans), Rest 187 from 19 smokes (6 clans). Nearest ship a ship outside the smoke: Top 6 55% vs Rest 33%, +22.1 (-12.9 to +37.8). Second destroyer: 28% vs 20%, +8.0 (-12.1 to +25.2). The smoker itself: 18% vs 46%, -29.0 (-50.1 to +7.6). None clear. The one clear gap: the target is radar-lit by a radar ship elsewhere in 29% of Top 6 shots against 6% of Rest shots, +22.8 (+6.3 to +33.1 *); per smoke 35% vs 12%, +22.3 (+0.6 to +43.8 *). Top 6 Harugumos shoot more often at targets a friendly radar somewhere else is holding. Four Top 6 clans only, so treat it as a lead.
Second destroyer within 5 km over the smoke's life: Top 6 35% (n 55) vs Rest 28% (n 45), +7.0 (-6.4 to +26.4), not clear.

**Clans (smokes with own-gun damage):** Harugumo: Top 6: RESIN 12, H-SR 10, HTDOG 2, BONKZ 1 | Rest: EPOXY 9, KM 3, PFANS 2, PN 2, -BN- 2, MZY 1. Somers: Top 6: RESIN 3, BONKZ 2, H-SR 1 | Rest: REEEE 6, HFANS 4, UYSC 2, BONKY 2, MZY 2, PFANS 1, INCA 1, -BN- 1, KITED 1. Gearing: Top 6: KITE 4, BONKZ 1 | Rest: 5D 6, OGF 3, -BN- 1, UYSC 1, RSR 1, KSC 1.

**Biggest Harugumo own-gun smokes (share of that smoke's own-gun damage by what the data shows at the shot):**

- [RESIN, Land of Fire, 7:43](https://seanr87.github.io/smoke-signals/smoke/smokes/8176_g3_159292.html): 60,190 in 29 shots, radar cruiser inside: no. not detected at the shot 42%; detected, no radar: nearest ally a second destroyer 24%; detected, no radar: nearest ally a ship outside the smoke 22%; radar-lit from elsewhere 11%.
- [RESIN, Sleeping Giant, 7:00](https://seanr87.github.io/smoke-signals/smoke/smokes/8147_g1_120803.html): 60,042 in 42 shots, radar cruiser inside: no. detected, no radar: nearest ally a ship outside the smoke 79%; not detected at the shot 13%; radar-lit from elsewhere 9%.
- [PFANS, Hotspot, 7:47](https://seanr87.github.io/smoke-signals/smoke/smokes/7971_g1_82507.html): 32,696 in 29 shots, radar cruiser inside: yes. detected, no radar: nearest ally a second destroyer 57%; detected, no radar: nearest ally a ship outside the smoke 41%; radar-lit from elsewhere 1%.
- [-BN-, Okinawa, 3:22](https://seanr87.github.io/smoke-signals/smoke/smokes/8152_g1_207837.html): 31,913 in 37 shots, radar cruiser inside: no. detected, no radar: nearest ally the smoker itself 81%; detected, no radar: nearest ally a ship outside the smoke 14%; not detected at the shot 4%.
- [PN, Land of Fire, 5:20](https://seanr87.github.io/smoke-signals/smoke/smokes/7981_g1_174224.html): 27,008 in 19 shots, radar cruiser inside: yes. detected, no radar: nearest ally a ship outside the smoke 59%; radar-lit from inside this smoke 40%; radar-lit from elsewhere 1%.
- [H-SR, Sleeping Giant, 1:54](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39283.html): 24,259 in 21 shots, radar cruiser inside: yes. detected, no radar: nearest ally a ship outside the smoke 60%; radar-lit from elsewhere 34%; not detected at the shot 5%.

**Could not be done / proxy:** Spotting still cannot be proven. The replay does not say which ship's sight a shot used. What the data gives is: the target was detected at the shot (its own track), it was or was not radar-lit and by which radar ship (attributed by range and time, a few ambiguous), and which friendly ship was nearest. Positions are sampled every 2 s. Smoke shape is the final laid path, so "inside the smoke" is slightly generous while a smoke is still being laid. Fire ticks are counted at the tick, not at the shell that started the fire.

**Verdict:** Keep.

**Changed from round 5:**

| Number | Round 5 (one snapshot per smoke) | Round 5b (per shot) | Difference |
|---|---|---|---|
| Harugumo: nearest friendly ship is a ship outside the smoke | 42% of 53 targets | 45% of 410 shots | +3 points |
| Somers: nearest friendly ship is a ship outside the smoke | 17% of 30 targets | 37% of 83 shots | +20 points |
| Gearing: nearest friendly ship is a ship outside the smoke | 17% of 18 targets | 8% of 64 shots | -9 points |
| Harugumo: nearest friendly ship is a second destroyer | 25% of 53 targets | 24% of 410 shots | -1 points |
| Somers: nearest friendly ship is a second destroyer | 17% of 30 targets | 11% of 83 shots | -6 points |
| Gearing: nearest friendly ship is a second destroyer | 0% of 18 targets | 2% of 64 shots | +2 points |
| Harugumo: nearest friendly ship is the smoker itself | 21% of 53 targets | 31% of 410 shots | +10 points |
| Somers: nearest friendly ship is the smoker itself | 53% of 30 targets | 48% of 83 shots | -5 points |
| Gearing: nearest friendly ship is the smoker itself | 83% of 18 targets | 91% of 64 shots | +8 points |
| Harugumo: nearest friendly ship is another ship in or behind the smoke | 8% of 53 targets | 0% of 410 shots | -8 points |
| Somers: nearest friendly ship is another ship in or behind the smoke | 3% of 30 targets | 0% of 83 shots | -3 points |
| Gearing: nearest friendly ship is another ship in or behind the smoke | 0% of 18 targets | 0% of 64 shots | +0 points |
| Harugumo: nearest friendly ship is the radar cruiser inside the smoke | 6% of 53 targets | 0% of 410 shots | -6 points |
| Somers: nearest friendly ship is the radar cruiser inside the smoke | 10% of 30 targets | 4% of 83 shots | -6 points |
| Gearing: nearest friendly ship is the radar cruiser inside the smoke | 0% of 18 targets | 0% of 64 shots | +0 points |

- Why: better data and a different unit. Round 5 looked once per smoke, at the moment it was fully laid, and only at targets whose position the snapshot happened to hold (53 of 68 Harugumo targets). Round 5b looks at every shot with every ship's position. Redoing the round 5 question with the tracks at the same single moment, same targets and same rule gives a ship outside the smoke 27, a second destroyer 18, the smoker itself 20, another ship in or behind the smoke 2, the radar cruiser inside the smoke 1 of 68; 46 of the 53 shared targets get the same answer. So part of the shift is the 15 targets round 5 could not place, and part is shots fired later in the smoke's life.
- Harugumo "ship outside the smoke or a second destroyer": 67% -> 69% (+2). "The radar cruiser inside": 6% -> 0.5%. "The smoker itself": 21% -> 31%. The Harugumo against Somers gap on "the smoker itself" was -32.6 (clear) and is now -17.5 (-41.5 to +10.4), not clear by shots, -23.0 (-42.2 to -3.8 *), clear per smoke.

| Ship | Second destroyer recorded, round 5 | Second destroyer alive at the same moment, tracks | Difference | 1 km+ forward, round 5 | 1 km+ forward, tracks | Difference | Smokes where the two agree on "recorded" |
|---|---|---|---|---|---|---|---|
| Harugumo | 59.0% | 94.0% | +35.0 | 33.0% | 61.0% | +28.0 | 65 of 100 |
| Somers | 45.8% | 99.6% | +53.8 | 22.7% | 66.9% | +44.2 | 120 of 260 |
| Gearing | 37.2% | 95.6% | +58.4 | 17.2% | 51.7% | +34.5 | 75 of 180 |

- Why: the round 5 snapshot held only some of the ships (about 3 to 4 allied ships of up to 9 alive, the ones near the smoke), so "recorded" really meant "close enough to be in the snapshot". With full tracks a second allied destroyer is alive at almost every smoke of all three ships, so the round 5 gaps (+13.2 and +21.8 recorded; +10.3 and +15.8 forward) are not gaps in whether one exists. They are gaps in distance, and that part holds: an allied destroyer is within 5 km of the smoke for 32% of a Harugumo smoke's standing time, against 14% (Somers) and 13% (Gearing), both clear. Different definition, better data.
- Library fix during this round: 17 smokes in two games (15-minute clock) had round 5 elapsed times 300 s too high. Nothing in B3 uses those fields (all times are the exact `e0` / `e1` and the damage event clocks), so no B3 number moved for that reason; the scripts were rerun after the fix.
- New in round 5b (no round 5 number): radar-lit at the shot, 22% of Harugumo shots, of which from inside the smoke 3%.

**Self-checks:**

- Damage total a second way: credited events against the smoke records (smoker's own damage, all of it): Harugumo 461,873 vs 461,960; Somers 253,013 vs 253,009; Gearing 94,724 vs 94,736.
- "Radar-lit from inside this smoke" a second way (the radar log's own source-in-smoke flag instead of track geometry): Harugumo 13 vs 14 shots; Somers 6 vs 8 shots; Gearing 2 vs 1 shots.

### C5-LP-4. Loop: do Daring smokes follow a friendly radar lighting an enemy destroyer?

**Answer:** No more often than chance. 17 of 48 Daring smokes on Loop (35%) came within 60 seconds after a friendly radar lit an enemy destroyer somewhere on the map, but a friendly radar has an enemy destroyer lit in the last 60 seconds at 37% of all moments in those games. Near the cap the Daring then smoked it is 2 of 48 (chance 8%). The reverse reading (smoke first, radar on a destroyer near that cap within 60 s after) is 5 of 48, also at chance.

**What was counted.** The radar log now has every radar activation and every enemy ship it lit, with start and end times. For each destroyer smoke: was there a lit span on an enemy destroyer, attributed to a radar of the smoking team, that overlaps the 60 s (30 s, 90 s) before the smoke was activated. "Near the cap" = while that destroyer was within 3 km of the edge of the cap nearest to the smoke. Chance = the share of all moments between the game's first and last smoke (cut at the smoker's death) at which the same test is true; it is computed exactly, not by random draws. The round 5 control windows are kept too: 120 to 60 s before, and 60 to 120 s after.

**Numbers (a friendly radar lit an enemy destroyer anywhere on the map):**

| Group | Smokes | Clans | 30 s before | 60 s before | 90 s before | Control: 120 to 60 s before | Control: 60 to 120 s after |
|---|---|---|---|---|---|---|---|
| Daring on Loop | 48 | 11 | 11 (23%, 11 to 36); chance 23%; gap -0.5 (-11.5 to +10.9) | 17 (35%, 27 to 47); chance 37%; gap -1.2 (-8.3 to +6.9) | 19 (40%, 29 to 51); chance 48%; gap -8.9 (-15.7 to -1.9 *) | 20 (42%, 26 to 58) | 11 (23%, 11 to 36) |
| Daring on other maps | 152 | 19 | 42 (28%, 20 to 37); chance 27%; gap +0.8 (-5.2 to +7.3) | 61 (40%, 31 to 51); chance 40%; gap +0.4 (-7.0 to +6.6) | 77 (51%, 43 to 60); chance 50%; gap +0.4 (-5.0 to +7.2) | 59 (39%, 31 to 47) | 44 (29%, 24 to 35) |
| Other cap sitters on Loop | 40 | 13 | 10 (25%, 11 to 46); chance 27%; gap -1.9 (-15.9 to +16.9) | 16 (40%, 23 to 60); chance 39%; gap +0.9 (-16.6 to +21.2) | 20 (50%, 38 to 65); chance 49%; gap +1.2 (-13.0 to +17.9) | 14 (35%, 25 to 44) | 12 (30%, 22 to 38) |
| Other destroyer smokes on Loop | 54 | 17 | 14 (26%, 14 to 40); chance 25%; gap +0.5 (-10.6 to +10.7) | 19 (35%, 21 to 51); chance 39%; gap -3.5 (-14.4 to +8.3) | 24 (44%, 31 to 60); chance 50%; gap -5.2 (-15.2 to +5.5) | 17 (32%, 19 to 46) | 16 (30%, 17 to 43) |
| All destroyer smokes, all maps | 1074 | 30 | 301 (28%, 25 to 32); chance 28%; gap -0.4 (-2.5 to +1.5) | 399 (37%, 33 to 41); chance 42%; gap -5.1 (-6.9 to -3.2 *) | 516 (48%, 43 to 53); chance 53%; gap -4.9 (-7.1 to -2.7 *) | 369 (34%, 32 to 37) | 387 (36%, 32 to 40) |

**Numbers (the lit destroyer was within 3 km of the cap the smoke is nearest to):**

| Group | Smokes | 30 s before | 60 s before | 90 s before | Control: 120 to 60 s before | Reverse: lit in the 60 s after the smoke | Reverse: a new lit span began in the 60 s after |
|---|---|---|---|---|---|---|---|
| Daring on Loop | 48 | 1 (2%, 0 to 8); chance 5%; gap -2.9 (-8.2 to +2.9) | 2 (4%, 0 to 12); chance 8%; gap -3.9 (-11.1 to +4.9) | 3 (6%, 0 to 13); chance 11%; gap -4.7 (-14.9 to +3.7) | 5 (10%, 5 to 18) | 5 (10%, 3 to 22); chance 8%; gap +2.7 (-4.8 to +11.0) | 4 (8%, 0 to 19) |
| Daring on other maps | 152 | 18 (12%, 7 to 17); chance 10%; gap +1.4 (-2.2 to +6.0) | 25 (16%, 10 to 24); chance 16%; gap +0.0 (-3.4 to +4.2) | 32 (21%, 13 to 31); chance 21%; gap -0.2 (-3.9 to +5.7) | 25 (16%, 10 to 23) | 36 (24%, 17 to 33); chance 16%; gap +7.2 (+2.8 to +12.8 *) | 27 (18%, 13 to 26) |
| Other cap sitters on Loop | 40 | 7 (18%, 8 to 31); chance 12%; gap +5.2 (-7.0 to +19.1) | 9 (22%, 9 to 37); chance 19%; gap +3.5 (-8.4 to +16.8) | 11 (28%, 16 to 40); chance 24%; gap +3.0 (-7.0 to +13.9) | 5 (12%, 0 to 24) | 14 (35%, 21 to 49); chance 20%; gap +14.6 (+3.7 to +26.1 *) | 11 (28%, 13 to 41) |
| Other destroyer smokes on Loop | 54 | 6 (11%, 2 to 24); chance 10%; gap +1.3 (-7.5 to +12.0) | 7 (13%, 4 to 26); chance 16%; gap -2.7 (-10.9 to +8.0) | 10 (18%, 9 to 32); chance 21%; gap -2.7 (-10.5 to +6.3) | 5 (9%, 3 to 16) | 12 (22%, 8 to 36); chance 16%; gap +6.2 (-7.1 to +19.1) | 11 (20%, 6 to 34) |
| All destroyer smokes, all maps | 1074 | 97 (9%, 7 to 11); chance 9%; gap +0.0 (-1.3 to +1.5) | 129 (12%, 10 to 14); chance 14%; gap -2.3 (-3.6 to -0.9 *) | 182 (17%, 14 to 19); chance 19%; gap -1.9 (-3.6 to -0.3 *) | 128 (12%, 10 to 14) | 227 (21%, 18 to 24); chance 14%; gap +7.0 (+4.8 to +9.3 *) | 192 (18%, 15 to 20) |

- Daring on Loop, 60 s before against the round 5 control windows: against 120 to 60 s before -6.2 (-20.0 to +14.6); against 60 to 120 s after +12.5 (+2.9 to +23.1 *). No rise just before the smoke. The 60 s before is higher than the window well after the smoke, but Daring smokes on other maps show the same (+11.2, +1.9 to +20.7 *), so it is not a Loop pattern.
- Daring on Loop minus Daring on other maps, anywhere, 60 s: -4.7 (-19.1 to +11.0). Minus other cap sitters on Loop: -4.6 (-26.9 to +14.1). Near the cap, 60 s: -12.3 (-21.1 to -1.8 *) and -18.3 (-34.5 to -4.8 *): Daring smokes on Loop follow radar near their cap less often than the comparison groups, as round 5 suggested.
- After taking chance out, anywhere 60 s: Daring on Loop minus Daring on other maps -1.6 (-13.0 to +11.0); minus other cap sitters on Loop -2.1 (-24.3 to +15.7). Nothing.
- Reverse reading. Radar lit an enemy destroyer near the cap in the 60 s after the smoke: Daring on Loop 5 (10%, 3 to 22); chance 8%; gap +2.7 (-4.8 to +11.0). Other cap sitters on Loop 14 (35%, 21 to 49); chance 20%; gap +14.6 (+3.7 to +26.1 *); Daring on other maps 36 (24%, 17 to 33); chance 16%; gap +7.2 (+2.8 to +12.8 *); all destroyer smokes 227 (21%, 18 to 24); chance 14%; gap +7.0 (+4.8 to +9.3 *). So "smoke, then a friendly radar lights a destroyer near that cap" is a real pattern for destroyer smokes in general and for the other cap sitters on Loop, but not for the Daring on Loop.
- The other way round, as in round 5: our radar lit an enemy destroyer on Loop in 62 separate episodes for teams with a Daring; a Daring was alive for 55; it smoked within 60 s after 14 (26%). Chance for a Daring smoke in any 60 s of its life in those games: 22%; gap +3.9 (-4.3 to +13.9). Within 30 s: 7; within 90 s: 19.
- Phase: Daring smokes on Loop are late (median 10:27 elapsed, 12% in the first 5 minutes). After minute 5: 16 of 42 (38.1%, 26.9 to 56.0; chance 35.6%, gap +2.5 (-8.8 to +18.4)).

**The typical sequence in the 17 cases that match (60 s, anywhere):**

- Who radared: Des Moines 6, Moskva 3, Stalingrad 3, Minotaur 3, Petropavlovsk 3, Thor 2, San Martín 1, Småland 1, Yueyang 1 (23 lit spans; by class: cruiser 19, battleship 2, destroyer 2). 0 of these radars were run from inside a smoke, and 0 by the Daring itself.
- From where: the radar ship was a median 13.7 km from the edge of the cap the Daring then smoked (cells: F8 6, G8 4, G7 3, G6 2, F3 2), and the lit destroyer a median 10.9 km from that cap and 16.6 km from the smoke. In other words, the radar and the Daring smoke are usually on different parts of the map: 14 of the 17 smokes are at cap A, while the radar ships are mostly in F8 and G8, on the other side of the map.
- How long before: the first lit span in the window began a median 40 s before the smoke; the destroyer was still lit when the smoke went up in 3 of 17. Lit destroyers: Yueyang 7, Daring 3, Z-42 2, Gearing 2, Fuyutsuki 1, Châteaurenault 1.
- Did the cap change hands (from activation to 60 s after the smoke cleared): the cap was ours at activation in 9, theirs in 8, neutral in 0. We took it in 1 of the 8 not ours; the enemy took it in 2 of the 9 not theirs. For the 31 smokes with no radar before: we took 4 of 14, the enemy took 3 of 20. Counts too small for rates that differ; no sign that the radar cases end differently.
- The Daring was itself detected when it smoked in 9 of 17 matching cases and 16 of 31 others. Median concealed damage 462 against 340.
- The 2 cases with the destroyer near the cap:
  - [MACHX Daring, 10:12, G4, cap A (theirs)](https://seanr87.github.io/smoke-signals/smoke/smokes/7917_g1_116012.html): Stalingrad lit a Daring 4 s before; the destroyer was 8.0 km from the smoke. Cap changes after: none.
  - [NGA Daring, 11:18, G8, cap B (theirs)](https://seanr87.github.io/smoke-signals/smoke/smokes/7918_g1_55746.html): Småland lit a Z-42 61 s before; the destroyer was 8.5 km from the smoke. Cap changes after: none.

**Top 6 or Shared:** Not a spot, and not testable for the Daring on Loop: 3 Top 6 smokes against 45 Rest (too few; 1 of 3 and 16 of 45 match). Daring on other maps: Top 6 55% (n 31) vs Rest 36% (n 121), +18.5 (-4.0 to +29.3). Other cap sitters on Loop: Top 6 50% (n 20) vs Rest 30% (n 20), +20.0 (-17.1 to +50.7). Other destroyer smokes on Loop: Top 6 17% (n 18) vs Rest 44% (n 36), -27.8 (-48.7 to -8.3 *). All destroyer smokes, all maps: Top 6 43% (n 387) vs Rest 34% (n 687), +8.6 (+1.0 to +17.3 *).

**Clans:** Daring on Loop: Top 6: KITE 3 | Rest: REEEE 11, KITED 9, EPOXY 6, MACHX 3, -BN- 3, BONKY 3, SCCC2 3, HFANS 3, KSC 2, NGA 2. The 17 matching smokes: Top 6: KITE 1 | Rest: EPOXY 3, KITED 3, REEEE 3, MACHX 2, HFANS 2, NGA 1, -BN- 1, BONKY 1 (8 of 12 games).

**Could not be done / proxy:** Which radar lit a ship is attributed by range and time, not read from the game; none of the spans used here for the Daring on Loop were ambiguous, and adding the unattributed spans changes nothing (17 of 48). The data shows timing only; it cannot show whether the Daring player reacted to the radar. The Daring on Loop is almost all Rest clans, so no Top 6 reading is possible.

**Verdict:** Drop.

**Changed from round 5:**

| Group | Round 5: our radar lit an enemy destroyer in the 60 s before (seen only when that destroyer sat in its own smoke) | Round 5b: same, every radar and every lit destroyer | Difference | Round 5b chance level |
|---|---|---|---|---|
| Daring on Loop | 1 of 48 (2%) | 17 of 48 (35%) | +33 points | 37% |
| Daring on other maps | 7 of 152 (5%) | 61 of 152 (40%) | +35 points | 40% |
| Other cap sitters on Loop | 0 of 40 (0%) | 16 of 40 (40%) | +40 points | 39% |
| Other destroyer smokes on Loop | 0 of 54 (0%) | 19 of 54 (35%) | +35 points | 39% |
| All destroyer smokes, all maps | 24 of 1074 (2%) | 399 of 1074 (37%) | +35 points | 42% |

- Why: better data. Round 5 could see a radar lighting an enemy destroyer only when that destroyer was inside its own team's smoke (9 such rows on Loop). The radar log has 229 lit spans on enemy destroyers in the 23 Loop games. The single round 5 case is still there (1 of 1 found again). Round 5 described its target, an A. da Barbiano, as a cruiser; the roster lists it as a destroyer.
- Reverse view: round 5 had 9 episodes, a Daring alive for 2, 1 followed by a smoke. Round 5b: 62 episodes, 55 with a Daring alive, 14 followed (26% against chance 22%).
- Library fix during this round: two games ran on a 15-minute clock, so the round 5 elapsed times of their 17 smokes were 300 s too high (one of the two games is on Loop). Every time used here is the exact `e0` / `e1` from the timelines, which never had that error; the only library time field used is the game length in the reverse view, rerun after the fix with no change to any count.
- The verdict does not change (Drop), but the reason does. Round 5 said "not supported, on a thin proxy: 1 of 48". Round 5b says: it happens in about a third of Daring smokes on Loop, and that is exactly what chance gives, because some friendly radar has some enemy destroyer lit about a third of the time.

**Self-checks:**

- Headline a second way: counting straight from the radar rows without the helper functions gives 17 of 48, the same as 17.
- Old field against new on the same smokes: the round 5 proxy finds 1 Daring smoke on Loop; the radar log finds that one and 16 more.

### Notes on the new files and `tl.py`

- No bug found in `tl.py`. Two things to know. `GameTL.lit()` returns spans for both teams; filter on `team` (the radar's team) as well as `target_team`. `g.ships(team, alive_at=t)` and `Track.pos(t)` worked as described.
- With `python -I` a script's own folder is not on the import path, so a helper module beside the script needs its own `sys.path.insert`.
- `damage_events.csv` also carries `flood` and `unknown` rows with a credited smoke; they are not part of smoke damage and were left out, which makes the event total match the smoke records.
- The round 5 `cast` (ships at the fully-laid moment) holds only part of each team (checked on 25 Harugumo smokes: 0 to 6 allied ships in `cast` against 4 to 9 alive in the tracks). Any round 5 number of the form "a ship of type X was recorded" means "recorded near the smoke", not only for the second destroyer.

### Files

- Scripts: `n3lib.py`, `b3_shots.py`, `c5_loop.py`, `n3_figs.py`, `n3_findings.py` (run in that order; each with `python -I -X utf8`).
- Data: `b3.json`, `c5.json`, `ships-and-loop.json`, `b3_out.txt`, `c5_out.txt`.
- Figures: `round5b/figures/n3-harugumo-spotter-per-shot.(svg|png)`, `round5b/figures/n3-loop-daring-after-radar.(svg|png)`.

---

## Part B: ship tendencies (B1-B4), Round 5 text

Source: `part-b/FINDINGS-B.md`.


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

> **Superseded in Round 5b.** The "who spots for the Harugumo" and second-destroyer numbers are redone per shot: see "B3 (Round 5b)". The deployment tables below are unchanged. The Round 5 text is kept below for reference.


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

---

## Part C (Round 5b): cap defence from the timeline (C1), cap holder at exactly 8:00 (C2)

Source: `new-n1/FINDINGS-N1.md`.


Batch `output/20261117-230933`. 1,547 smokes, 171 games, 30 clans. Everything is association, not cause. Intervals are 95%, by resampling whole clans (C1) or whole games (C2). "Clear" = the interval excludes zero.
This file is written by `n1_findings.py` from the numbers computed in `n1_c1.py` and `n1_c2.py`.

### C1. Cap defence: "enemy took the cap" from the timeline, and ribbons

**Answer:** With the full cap timeline, the enemy took the nearest cap during the smoke or within 60 seconds after it in 21.7% of the smokes where the question applies (233 of 1,074); round 5 said 17.1% (184). Strictly while the smoke stood it is 14.4% (155). The round 5 snapshot version never said yes wrongly, but it missed 48 of 232 real flips (20.7%), more than the 15% estimated then. The Top 6 vs Rest gaps that round 5 called clear are not clear any more; the snapshots had missed more Top 6 flips (27%) than Rest flips (18%). Ribbons can now be counted, but only 268 of 1,547 smokes covered a recording player, so they are a check on the timeline, not a measure.

**Numbers: three ways** (nearest cap by geometry; "not applicable" = the cap was already the enemy's at activation)

| what | applicable smokes | strictly while the smoke stood | only in the 60 s after it cleared | during or within 60 s |
|---|---|---|---|---|
| enemy took the nearest cap | 1,074 | 155 (14.4%) | 78 (7.3%) | 233 (21.7%) |
| we took the nearest cap (cap not ours at activation) | 853 | 196 (23.0%) | 76 (8.9%) | 272 (31.9%) |

- Grace after the smoke clears, enemy took: 0 s: 155 (14.4%) [round 5: 103, 9.6%]; 10 s: 173 (16.1%); 30 s: 199 (18.5%); 60 s: 233 (21.7%) [round 5: 184, 17.1%]; 120 s: 293 (27.3%) [round 5: 233, 21.7%].
- Not applicable: 473 smokes (round 5: 474). Owner of the nearest cap at activation agrees with the round 5 stored value in 1545 of 1,547 smokes; the 2 others flipped within a second of the activation.

**Numbers: timeline against the round 5 snapshot version, same smokes, 60 s grace both**

| enemy took: round 5 snapshot \ timeline | yes | no | not applicable |
|---|---|---|---|
| yes | 184 | 0 | 0 |
| no | 48 | 841 | 0 |
| n/a | 1 | 0 | 473 |

- Enemy took: both versions apply to 1,073 smokes. They agree on 1,025 (95.5%). Snapshot missed a flip: 48. Snapshot wrong the other way: 0. So the snapshot version missed 20.7% of the 232 real flips. In 46 of the 48 misses the cap was still the enemy's at the end of the window: the flip simply came after the last snapshot.
- By group: Top 6 79 real flips, 21 missed (27%); Rest 153 real flips, 27 missed (18%). Both groups had the same number of snapshots per smoke (mean 5.3 and 5.2), so this is how the misses happened to fall, not a coverage difference.
- We took: both apply to 852; agree 790 (92.7%); snapshot missed 62 of 271 real flips (22.9%); wrong the other way 0.
- Checks. (1) A second computation straight from the timeline rows agrees on all 1,547 smokes (0 mismatches). (2) The batch field `cap_won` names the nearest cap in 171 smokes: the timeline says "we took it" in 170 (1 not applicable); the snapshot version found 144. (3) Team-frame cap letters from the timeline file match the round 5 geometry in every smoke.

**Numbers: summary tables from the timeline** (during the smoke or within 60 s after; last two columns are round 5)

| group | n | enemy took it (interval) | Top 6 | Rest | Top 6 - Rest | strictly during | round 5 share | round 5 gap |
|---|---|---|---|---|---|---|---|---|
| all applicable smokes | 1,074 | 21.7% (19.5 to 23.9) | 19.9% (n 403) | 22.8% (n 671) | -3.0 (-7.1 to +1.2) | 14.4%; gap -4.0 (-8.0 to +0.3) | 17.1% (n 1,073) | -4.4 (-8.9 to +0.1) |
| destroyer smokes | 763 | 23.1% (20.1 to 26.5) | 20.9% (n 292) | 24.4% (n 471) | -3.5 (-9.5 to +2.8) | 16.1%; gap -5.6 (-11.0 to +0.3) | 18.8% (n 762) | -5.9 (-12.1 to -0.9) clear |
| smoke centre inside or within 2 km of the cap | 541 | 16.1% (13.2 to 19.6) | 14.3% (n 189) | 17.0% (n 352) | -2.8 (-8.9 to +3.9) | 9.6%; gap -4.2 (-10.1 to +1.2) | 11.1% (n 541) | -4.8 (-9.2 to -0.7) clear |
| destroyer smokes inside or within 2 km | 405 | 17.5% (14.0 to 21.8) | 15.5% (n 142) | 18.6% (n 263) | -3.1 (-11.0 to +4.5) | 11.1%; gap -6.3 (-14.8 to +1.1) | 12.8% (n 405) | -6.8 (-12.6 to -1.7) clear |
| cap ours at activation | 694 | 18.2% (15.1 to 21.6) | 18.4% (n 261) | 18.0% (n 433) | +0.4 (-5.8 to +5.8) | 11.0%; gap -1.0 (-5.9 to +3.3) | 13.7% (n 694) | -1.6 (-8.2 to +5.0) |
| cap neutral at activation | 380 | 28.2% (23.3 to 33.9) | 22.5% (n 142) | 31.5% (n 238) | -9.0 (-18.3 to -0.2) clear | 20.8%; gap -9.6 (-17.4 to -0.4) clear | 23.5% (n 379) | -9.4 (-18.4 to -0.5) clear |
| cap ours, smoke within 2 km | 349 | 12.3% (8.5 to 16.1) | 11.2% (n 116) | 12.9% (n 233) | -1.7 (-11.1 to +6.8) | 5.7%; gap -3.4 (-9.4 to +2.3) | 8.0% (n 350) | -4.2 (-9.7 to +1.5) |
| cap ours, cap_defended set for that cap | 153 | 45.8% (37.9 to 53.3) | 48.1% (n 52) | 44.6% (n 101) | +3.5 (-13.1 to +20.0) | 28.1%; gap -7.6 (-22.0 to +4.7) | 35.9% (n 153) | -7.8 (-24.7 to +10.5) |
| cap ours, cap_defended not set for it | 541 | 10.4% (8.1 to 13.0) | 11.0% (n 209) | 9.9% (n 332) | +1.1 (-3.7 to +5.3) | 6.1%; gap +1.8 (-1.9 to +5.1) | 7.4% (n 541) | +1.3 (-3.4 to +5.2) |

- By map and cap (team-frame letter; all 26 rows in `out-c1.md` and `caps.json`). Highest: Sea of Fortune C 40.0% (n 15; round 5 6.7%); Mountain Range B 39.1% (n 46; round 5 35.6%); Hotspot C 32.3% (n 65; round 5 26.2%); Okinawa D 30.8% (n 26; round 5 19.2%); Loop B 30.0% (n 30; round 5 20.0%).
- Clear Top 6 vs Rest gaps by map and cap now: Mountain Range C (Top 6 8.0% of 25, Rest 32.3% of 31; -24.3 (-42.6 to -3.5) clear). One clear row out of 17 rows with enough smokes on both sides is about what luck alone gives. The three round 5 rows are no longer clear: Loop A -15.9 (-37.0 to +2.9) (was -22.2 clear); Loop B -15.0 (-47.1 to +9.1) (was -30.0 clear); Mountain Range A +3.6 (-29.2 to +32.9) (was -17.5 clear).
- We took the nearest cap (60 s): all smokes where the nearest cap was not ours: 31.9% (n 853), Top 6 39.0% vs Rest 28.5%, gap +10.5 (-0.2 to +22.1); round 5 24.5%; destroyer smokes: 35.6% (n 582), Top 6 45.7% vs Rest 30.4%, gap +15.3 (+2.1 to +28.1) clear; round 5 27.0%; within 2 km: 42.3% (n 350), Top 6 50.4% vs Rest 38.3%, gap +12.1 (+1.3 to +23.5) clear; round 5 35.0%.
- One row per smoke is in `new-n1/enemy-took.csv` (timeline values and the round 5 snapshot values side by side).

**Numbers: `cap_defended` follow-up, was the defended cap still ours afterwards?**

Kept = the enemy did not take the defended cap from the first moment it was ours and invaded until 60 s after the smoke cleared. The timeline shows that moment inside the smoke for 485 of 486 smokes.

| group | n | kept through 60 s after (interval) | Top 6 | Rest | Top 6 - Rest | kept while the smoke stood | round 5 (snapshot, 60 s) |
|---|---|---|---|---|---|---|---|
| all smokes with cap_defended | 486 | 52.5% (46.1 to 58.3) | 53.4% (n 163) | 52.0% (n 323) | +1.4 (-13.2 to +13.7) | 68.7% | 60.5% |
| destroyer smokes | 360 | 50.6% (43.9 to 56.4) | 51.6% (n 124) | 50.0% (n 236) | +1.6 (-14.2 to +14.5) | 66.9% | 58.9% |
| defended cap = nearest cap | 175 | 53.7% (46.6 to 60.4) | 52.4% (n 63) | 54.5% (n 112) | -2.1 (-19.1 to +15.6) | 74.3% | 61.1% |
| defended cap not the nearest | 311 | 51.8% (44.7 to 58.4) | 54.0% (n 100) | 50.7% (n 211) | +3.3 (-13.2 to +17.9) | 65.6% | 60.1% |

- No grace: 334 of 486 kept (68.7%; round 5 374, 77.0%). 60 s: 255 (52.5%; round 5 294, 60.5%). 120 s: 227 (46.7%; round 5 252, 51.9%). Sixty seconds after the smoke cleared the defended cap was ours in 264 and the enemy's in 222.
- For comparison, any smoke whose nearest cap was ours at activation kept it through 60 s after in 81.8% (n 694); round 5 said 86.3%.

**Numbers (new): was the enemy inside our cap while the smoke stood?** (the timeline records the invading team)

| smokes | n | enemy was invading the cap during the smoke (interval) | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| within 2 km of a cap we own | 349 | 27.2% (19.9 to 33.8) | 29.3% (n 116) | 26.2% (n 233) | +3.1 (-10.9 to +16.5) |
| destroyer smokes within 2 km of a cap we own | 255 | 31.0% (22.8 to 39.7) | 29.5% (n 88) | 31.7% (n 167) | -2.2 (-22.6 to +13.6) |
| any smoke whose nearest cap is ours (reference) | 694 | 33.7% (28.5 to 38.9) | 34.1% (n 261) | 33.5% (n 433) | +0.6 (-10.8 to +11.4) |

| smokes | n | cap kept while the smoke stood (interval) | Top 6 | Rest | Top 6 - Rest | kept through 60 s after | Top 6 - Rest (60 s) |
|---|---|---|---|---|---|---|---|
| invaded, within 2 km | 95 | 78.9% (66.2 to 88.6) | 88.2% (n 34) | 73.8% (n 61) | +14.5 (-1.9 to +37.3) | 58.9% | +4.4 (-18.2 to +33.3) |
| invaded, destroyer smokes within 2 km | 79 | 77.2% (65.0 to 87.5) | 88.5% (n 26) | 71.7% (n 53) | +16.8 (-1.3 to +42.6) | 58.2% | +4.9 (-19.7 to +39.6) |
| not invaded, within 2 km | 254 | 100.0% (100.0 to 100.0) | 100.0% (n 82) | 100.0% (n 172) | +0.0 (+0.0 to +0.0) | 98.4% | +2.3 (+0.0 to +6.0) |

- When the enemy stood in a cap we owned and a smoke was within 2 km, the cap was still ours when the smoke cleared in 78.9% and 60 s later in 58.9% (n 95). The enemy stood in it for a median of 40 s. A cap that was not invaded was never lost while the smoke stood, as it must be.

**Numbers: ribbons per smoke**

- How thin this is: a replay holds only its own recording player's ribbons. That is one ship per team per game: 341 ships of 3,078. The batch has 442 cap ribbons: Defended 284, Captured 91, AssistedInCapture 67. Each row is one ribbon (the count column is always 1).
- Smokes that covered the smoking team's recording player: 268 of 1,547 (17.3%): smoker 129, inside 59, line of fire 49, behind 31. The recording player was the smoker or inside in 188 (12.2%). So 1,279 smokes (83%) cannot have a ribbon in this data whatever happened.
- Strict count (ribbon by a ship the smoke covered, during the smoke). A Defended ribbon repeats while defending, so events and distinct smokes are both given:

| smokes | n | with any cap ribbon | Defended | Captured | Assisted in capture |
|---|---|---|---|---|---|
| recording player covered by the smoke | 268 | 47 (17.5%) | 68 in 24 smokes (25.4 per 100) | 13 in 13 smokes (4.9 per 100) | 11 in 11 smokes (4.1 per 100) |
| Top 6 | 110 | 23 (20.9%) | 19 in 6 smokes (17.3 per 100) | 11 in 11 smokes (10.0 per 100) | 7 in 7 smokes (6.4 per 100) |
| Rest | 158 | 24 (15.2%) | 49 in 18 smokes (31.0 per 100) | 2 in 2 smokes (1.3 per 100) | 4 in 4 smokes (2.5 per 100) |
| recording player the smoker or inside | 188 | 36 (19.1%) | 44 in 15 smokes (23.4 per 100) | 13 in 13 smokes (6.9 per 100) | 9 in 9 smokes (4.8 per 100) |
| destroyer smokes, recording player covered | 208 | 35 (16.8%) | 54 in 16 smokes (26.0 per 100) | 12 in 12 smokes (5.8 per 100) | 8 in 8 smokes (3.8 per 100) |

- Looser count (ribbon by a ship of the smoking team during the smoke while that ship was within 2 km of the smoke; the recording player was that close in 254 smokes). It is not a superset of the strict count: ships behind a smoke or firing through it are often further than 2 km away.

| smokes | n | with any cap ribbon | Defended | Captured | Assisted in capture |
|---|---|---|---|---|---|
| recording player within 2 km while the smoke stood | 254 | 26 (10.2%) | 38 in 15 smokes (15.0 per 100) | 5 in 5 smokes (2.0 per 100) | 6 in 6 smokes (2.4 per 100) |
| Top 6 | 115 | 10 (8.7%) | 9 in 3 smokes (7.8 per 100) | 4 in 4 smokes (3.5 per 100) | 3 in 3 smokes (2.6 per 100) |
| Rest | 139 | 16 (11.5%) | 29 in 12 smokes (20.9 per 100) | 1 in 1 smokes (0.7 per 100) | 3 in 3 smokes (2.2 per 100) |

- Top 6 vs Rest, share of smokes with a ribbon:

| measure | n | share (interval) | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| strict: any cap ribbon | 268 | 17.5% (12.4 to 23.0) | 20.9% (n 110) | 15.2% (n 158) | +5.7 (-6.0 to +16.7) |
| strict: a Defended ribbon | 268 | 9.0% (6.0 to 12.0) | 5.5% (n 110) | 11.4% (n 158) | -5.9 (-11.6 to -0.7) clear |
| strict: a Captured or Assisted ribbon | 268 | 9.0% (3.7 to 14.7) | 16.4% (n 110) | 3.8% (n 158) | +12.6 (+3.1 to +23.6) clear |
| loose: any cap ribbon | 254 | 10.2% (6.5 to 14.5) | 8.7% (n 115) | 11.5% (n 139) | -2.8 (-10.7 to +5.5) |
| loose: a Defended ribbon | 254 | 5.9% (2.9 to 9.4) | 2.6% (n 115) | 8.6% (n 139) | -6.0 (-11.1 to -1.2) clear |

- Do smokes with a Defended ribbon keep the cap more often? (nearest cap ours at activation; the ribbon does not say which cap it was for)

| smokes | Defended ribbon: kept while the smoke stood | no Defended ribbon | Defended ribbon: kept through 60 s after | no Defended ribbon | gap at 60 s (interval) |
|---|---|---|---|---|---|
| strict, recording player covered | 11 of 11 (100%) (small n) | 78 of 96 (81%) | 7 of 11 (64%) (small n) | 74 of 96 (77%) | -13 (-50 to +14) |
| strict, and smoke within 2 km of the cap | too few (n 4) | 43 of 46 (93%) | too few (n 4) | 39 of 46 (85%) | - |
| loose, recording player within 2 km of the smoke | too few (n 6) | 84 of 99 (85%) | too few (n 6) | 79 of 99 (80%) | - |
| loose, and smoke within 2 km of the cap | too few (n 3) | 44 of 46 (96%) | too few (n 3) | 40 of 46 (87%) | - |
| loose, smoke within 2 km, enemy was invading the cap | too few (n 2) | 8 of 10 (80%) (small n) | too few (n 2) | 6 of 10 (60%) (small n) | - |

  Only the first row has enough smokes: 11 smokes with a Defended ribbon, all 11 kept the cap while the smoke stood, and 7 still had it 60 s later, against 77% without a ribbon. The interval is wide and includes zero. The data cannot say that Defended ribbons go with keeping the cap.
- What the ribbons are good for: they confirm the timeline. 91 of 91 Captured ribbons fall within 3 s of a cap changing to that team; all 284 of 284 Defended ribbons fall while the enemy stood in a cap (203 in a cap the team owned; the others in a neutral cap). Of 13 smokes with a strict Captured ribbon, the timeline says "we took the nearest cap during the smoke" in 12; in the other 1 the ribbon was for a different cap.

**Top 6 or Shared:** Shared. Enemy took the nearest cap (60 s): Top 6 19.9% vs Rest 22.8%, gap -3.0 (-7.1 to +1.2). Destroyer smokes: -3.5 (-9.5 to +2.8). Within 2 km: -2.8 (-8.9 to +3.9). The one gap that stays clear is for caps that were neutral at activation: Top 6 22.5% vs Rest 31.5%, -9.0 (-18.3 to -0.2) clear; strictly during the smoke -9.6 (-17.4 to -0.4) clear. Ribbons: Rest smokes carry a Defended ribbon more often and Top 6 smokes a Captured or Assisted ribbon more often (table above), on 110 and 158 smokes; treat as a hint.

**Clans:** not a spot item. The clan of every smoke is in `enemy-took.csv`.

**Could not be done / proxy:** Ribbons per smoke for all smokes: the replays hold them for one ship per team only. "Enemy took the cap" from the timeline is the measure to use; ribbons only confirm it. A Defended ribbon does not name its cap. The nearest cap can be far from the smoke; the "within 2 km" rows are the meaningful ones.

**Verdict:** Keep (the timeline version replaces the snapshot version). Drop the round 5 statement that Rest lose the cap clearly more often around destroyer smokes and smokes within 2 km. Ribbons: Drop as a per-smoke measure.

**Changed from round 5:**

| number | round 5 | round 5b | difference |
|---|---|---|---|
| enemy took, 60 s grace: yes | 184 | 233 | +49 |
| enemy took, 60 s grace: share | 17.1% | 21.7% | +4.6 |
| enemy took, no grace: yes | 103 | 155 | +52 |
| enemy took, no grace: share | 9.6% | 14.4% | +4.8 |
| enemy took, 120 s grace: yes | 233 | 293 | +60 |
| enemy took, 120 s grace: share | 21.7% | 27.3% | +5.6 |
| coverage: yes / no / not applicable | 184 / 889 / 474 | 233 / 841 / 473 |  |
| share of real flips the snapshot version misses | about 15% (estimate) | 20.7% enemy, 22.9% ours (measured) |  |
| all applicable smokes: share | 17.1% (n 1073) | 21.7% (n 1074) | +4.6 |
| all applicable smokes: Top 6 - Rest | -4.4 (-8.9 to +0.1) | -3.0 (-7.1 to +1.2) | +1.4 |
| destroyer smokes: share | 18.8% (n 762) | 23.1% (n 763) | +4.3 |
| destroyer smokes: Top 6 - Rest | -5.9 (-12.1 to -0.9) clear | -3.5 (-9.5 to +2.8) | +2.4 |
| smoke centre inside or within 2 km of the cap: share | 11.1% (n 541) | 16.1% (n 541) | +5.0 |
| smoke centre inside or within 2 km of the cap: Top 6 - Rest | -4.8 (-9.2 to -0.7) clear | -2.8 (-8.9 to +3.9) | +2.0 |
| destroyer smokes inside or within 2 km: share | 12.8% (n 405) | 17.5% (n 405) | +4.7 |
| destroyer smokes inside or within 2 km: Top 6 - Rest | -6.8 (-12.6 to -1.7) clear | -3.1 (-11.0 to +4.5) | +3.7 |
| cap ours at activation: share | 13.7% (n 694) | 18.2% (n 694) | +4.5 |
| cap ours at activation: Top 6 - Rest | -1.6 (-8.2 to +5.0) | +0.4 (-5.8 to +5.8) | +2.0 |
| cap neutral at activation: share | 23.5% (n 379) | 28.2% (n 380) | +4.7 |
| cap neutral at activation: Top 6 - Rest | -9.4 (-18.4 to -0.5) clear | -9.0 (-18.3 to -0.2) clear | +0.4 |
| cap ours, smoke within 2 km: share | 8.0% (n 350) | 12.3% (n 349) | +4.3 |
| cap ours, smoke within 2 km: Top 6 - Rest | -4.2 (-9.7 to +1.5) | -1.7 (-11.1 to +6.8) | +2.5 |
| cap ours, cap_defended set for that cap: share | 35.9% (n 153) | 45.8% (n 153) | +9.9 |
| cap ours, cap_defended set for that cap: Top 6 - Rest | -7.8 (-24.7 to +10.5) | +3.5 (-13.1 to +20.0) | +11.3 |
| cap ours, cap_defended not set for it: share | 7.4% (n 541) | 10.4% (n 541) | +3.0 |
| cap ours, cap_defended not set for it: Top 6 - Rest | +1.3 (-3.4 to +5.2) | +1.1 (-3.7 to +5.3) | -0.2 |
| cap_defended kept, all smokes with cap_defended | 60.5%; gap +3.1 (-10.7 to +15.3) | 52.5%; gap +1.4 (-13.2 to +13.7) | -8.0 |
| cap_defended kept, destroyer smokes | 58.9%; gap +1.2 (-15.0 to +13.3) | 50.6%; gap +1.6 (-14.2 to +14.5) | -8.3 |
| cap_defended kept, defended cap = nearest cap | 61.1%; gap +8.6 (-6.2 to +21.9) | 53.7%; gap -2.1 (-19.1 to +15.6) | -7.4 |
| cap_defended kept, defended cap not the nearest | 60.1%; gap -0.2 (-16.7 to +14.0) | 51.8%; gap +3.3 (-13.2 to +17.9) | -8.3 |
| cap_defended kept, no grace / 120 s | 77.0% / 51.9% | 68.7% / 46.7% | -8.3 / -5.2 |
| nearest cap ours at activation: kept | 86.3% (n 694) | 81.8% (n 694) | -4.5 |
| we took, all smokes where the nearest cap was not ours | 24.5%; gap +5.8 (-1.7 to +14.4) | 31.9%; gap +10.5 (-0.2 to +22.1) | +7.4 |
| we took, destroyer smokes | 27.0%; gap +8.9 (-1.6 to +20.2) | 35.6%; gap +15.3 (+2.1 to +28.1) clear | +8.6 |
| we took, within 2 km | 35.0%; gap +6.2 (-3.5 to +18.5) | 42.3%; gap +12.1 (+1.3 to +23.5) clear | +7.3 |
| Hotspot A: enemy took | 0.0% | 9.1% (n 11) | +9.1 |
| Hotspot B: enemy took | 9.1% | 11.4% (n 44) | +2.3 |
| Hotspot C: enemy took | 26.2% | 32.3% (n 65) | +6.1 |
| Hotspot D: enemy took | 23.8% | 25.0% (n 84) | +1.2 |
| Land of Fire A: enemy took | 20.8% | 22.6% (n 53) | +1.8 |
| Land of Fire B: enemy took | 11.8% | 14.7% (n 68) | +2.9 |
| Land of Fire D: enemy took | 7.7% | 11.5% (n 26) | +3.8 |
| Loop A: enemy took | 17.0% | 21.3% (n 47) | +4.3 |
| Loop B: enemy took | 20.0% | 30.0% (n 30) | +10.0 |
| Loop C: enemy took | 12.1% | 15.2% (n 33) | +3.1 |
| Mountain Range A: enemy took | 14.6% | 24.4% (n 41) | +9.8 |
| Mountain Range B: enemy took | 35.6% | 39.1% (n 46) | +3.5 |
| Mountain Range C: enemy took | 17.9% | 21.4% (n 56) | +3.5 |
| Okinawa A: enemy took | 15.4% | 23.1% (n 39) | +7.7 |
| Okinawa C: enemy took | 13.5% | 18.9% (n 37) | +5.4 |
| Okinawa D: enemy took | 19.2% | 30.8% (n 26) | +11.6 |
| Sea of Fortune A: enemy took | 8.3% | 16.7% (n 12) | +8.4 |
| Sea of Fortune B: enemy took | 10.0% | 13.3% (n 60) | +3.3 |
| Sea of Fortune C: enemy took | 6.7% | 40.0% (n 15) | +33.3 |
| Sleeping Giant A: enemy took | 21.1% | 26.7% (n 90) | +5.6 |
| Sleeping Giant B: enemy took | 8.7% | 10.9% (n 46) | +2.2 |
| Sleeping Giant D: enemy took | 17.3% | 20.0% (n 75) | +2.7 |
| ribbons | not in the batch | 442 ribbons, 268 smokes with a recording player covered | new |

Why: better data. The timeline has every owner change; round 5 only saw cap owners at the moments other smokes were laid or fully laid. Same definition, same nearest cap, same 60 s grace. Every share went up because flips after the last snapshot are now seen. The `cap_defended` follow-up also changed its start point slightly (from the first invaded moment instead of from activation; this gives the same count). Unchanged: the meaning of `cap_defended`, its rates (31.4% of smokes) and the distance facts, which use smoke fields only.

### C2. Cap holder at exactly 8:00 and winning

**Answer:** Same answer as round 5, now on all 166 games that were still running at 8:00 instead of 154. No single cap clearly adds something beyond team strength in a way that holds up. Teams holding more caps than the enemy at exactly 8:00 won 63% (the others 37%), but only +6 points more than their strength predicts, and in Rest-vs-Rest games the edge is gone (54%, -1 points). The two middle caps on Land of Fire are still the only caps that stay above expectation. New from the timeline: 74% of the teams with more caps were already ahead on score, and cap leaders who were not ahead on score won only 5 of 25.

**Numbers**

- Coverage: cap owners read from the timeline at exactly elapsed 480 s. 166 of 171 games are in the tables; 5 ended before 8:00 and are kept apart. Round 5 had 154 (5 ended early, 12 had no snapshot within 60 s). In the tables / all: Hotspot 31/31, Land of Fire 24/25, Loop 21/23, Mountain Range 20/21, Okinawa 17/18, Sea of Fortune 21/21, Sleeping Giant 32/32. Rest-vs-Rest games: 84 (round 5: 76).
- Against round 5, game by game: of the 154 games round 5 covered, the owners at 8:00 are identical in 141 and differ in 13 (the snapshot was up to 60 s away from 8:00). 2 games (kots19na_7971 g1, kots19na_7976 g1) ran on a 15-minute clock; round 5 worked out elapsed time as 20:00 minus the clock, so its "8:00" in those games was really 3:00. The timeline uses true elapsed seconds.
- Cap roles (own side, enemy side, middle), the expected win rate and the Bradley-Terry check are exactly as in round 5 (favourite won 110 of 158 on the simple model, 128 of 164 on Bradley-Terry).

All maps pooled, all 166 games (last column: round 5 on 154 games):

| what the team holds at 8:00 | team-games | holders won (interval) | others won | strength predicts | actual - expected (interval) | Bradley-Terry check | round 5 |
|---|---|---|---|---|---|---|---|
| its own-side cap | 199 | 101, 51% (47 to 54) | 49% | 100.1 | +0 (-3 to +4) | -0 (-3 to +2) | n 184, won 94 (51%), +1 (-3 to +4) |
| the enemy-side cap | 50 | 26, 52% (38 to 65) | 50% | 25.2 | +2 (-11 to +14) | -0 (-12 to +10) | n 47, won 25 (53%), +2 (-10 to +15) |
| at least one middle cap | 247 | 136, 55% (52 to 59) | 35% | 127.6 | +3 (+0 to +7) clear | +2 (-0 to +4) | n 231, won 131 (57%), +5 (+1 to +8) clear |
| every middle cap | 49 | 31, 63% (49 to 75) | 48% | 28.2 | +6 (-5 to +16) | +3 (-7 to +12) | n 43, won 27 (63%), +6 (-5 to +18) |
| more caps than the enemy (reference) | 97 | 61, 63% (54 to 72) | 37% | 54.7 | +6 (-2 to +14) | +2 (-5 to +9) | n 91, won 60 (66%), +8 (-0 to +17) |
| 2+ more caps than the enemy | 45 | 33, 73% (60 to 87) | 46% | 27.0 | +13 (+3 to +24) clear | +7 (-1 to +15) | n 42, won 31 (74%), +15 (+4 to +26) clear |

(a) Rest-vs-Rest games only (84):

| what the team holds at 8:00 | team-games | holders won (interval) | others won | strength predicts | actual - expected (interval) | Bradley-Terry check | round 5 |
|---|---|---|---|---|---|---|---|
| its own-side cap | 100 | 52, 52% (48 to 57) | 47% | 50.1 | +2 (-3 to +7) | +1 (-3 to +5) | n 88, won 46 (52%), +2 (-3 to +7) |
| the enemy-side cap | 26 | 15, 58% (38 to 77) | 49% | 13.1 | +7 (-12 to +26) | +4 (-12 to +20) | n 26, won 15 (58%), +8 (-9 to +26) |
| at least one middle cap | 131 | 69, 53% (48 to 58) | 40% | 67.6 | +1 (-3 to +5) | +0 (-3 to +3) | n 119, won 64 (54%), +2 (-2 to +6) |
| every middle cap | 25 | 16, 64% (46 to 83) | 48% | 15.0 | +4 (-12 to +18) | +2 (-12 to +14) | n 22, won 14 (64%), +5 (-12 to +23) |
| more caps than the enemy (reference) | 44 | 24, 54% (38 to 69) | 46% | 24.3 | -1 (-15 to +13) | -5 (-18 to +8) | n 41, won 23 (56%), +1 (-12 to +15) |
| 2+ more caps than the enemy | 21 | 17, 81% (62 to 96) | 46% | 12.8 | +20 (+5 to +33) clear | +14 (+2 to +24) clear | n 20, won 16 (80%), +22 (+7 to +36) clear |

Per map, caps whose holders did clearly better than strength predicts, now or in round 5 (every other cap on every map has an interval including zero; all rows are in `out-c2.md`):

| map, cap | holder team-games | holders won | others won | strength predicts | actual - expected | Bradley-Terry check | Rest-vs-Rest only | round 5 |
|---|---|---|---|---|---|---|---|---|
| Hotspot C (middle) | 29 | 21, 72% (55 to 87) | 30% | 16.2 | +16 (+0 to +32) clear | +10 (-4 to +23) | 11 of 16, +10 (-14 to +31) | n 28, won 20 (71%), +16 (+1 to +30) clear |
| Hotspot B (own side), Rest-vs-Rest games | 31 | 18, 58% (51 to 67) | 0% (n 5) | 15.7 | +7 (+2 to +16) clear | +6 (+1 to +12) clear | this row | n 27, won 16 (59%), +8 (+2 to +18) clear |
| Land of Fire A (middle) | 21 | 16, 76% (56 to 92) | 30% | 12.3 | +18 (+1 to +34) clear | +13 (-2 to +27) | 8 of 12 (small n), +10 (-12 to +31) | n 18, won 14 (78%), +20 (+2 to +38) clear |
| Land of Fire B (middle) | 21 | 17, 81% (62 to 96) | 26% | 12.9 | +20 (+6 to +34) clear | +14 (+2 to +25) clear | 8 of 11 (small n), +17 (-7 to +40) | n 20, won 16 (80%), +19 (+3 to +33) clear |
| Loop C (middle), Rest-vs-Rest games | 10 (small n) | 2, 20% (0 to 50) | 71% (n 14) | 5.1 | -31 (-57 to +1) | -32 (-59 to +1) | this row | n 9, won 1 (11%), -40 (-57 to -15) clear |

- Multiplicity: 25 map-and-cap rows tested; fewer than one clear positive row is expected by luck. 3 came out clear on the simple model, 1 on both models (Land of Fire B). None of the middle caps is clear in Rest-vs-Rest games (small n everywhere). Land of Fire A and B share the same games.
- "More caps than the enemy" per map (all games): Hotspot 10 of 12 (small n), +25 (+2 to +42) clear [round 5: n 12, won 10 (83%), +27 (+6 to +45) clear]; Land of Fire 13 of 15, +25 (+5 to +40) clear [round 5: n 14, won 12 (86%), +24 (+1 to +42) clear]; Loop 8 of 15, -6 (-30 to +19) [round 5: n 13, won 6 (46%), -12 (-37 to +13)]; Mountain Range 10 of 14 (small n), +12 (-8 to +30) [round 5: n 12, won 9 (75%), +15 (-6 to +35)]; Okinawa too few (n 7) [round 5: n 8, won 3 (38%), -11 (-38 to +17)]; Sea of Fortune 7 of 15, -2 (-22 to +18) [round 5: n 15, won 8 (53%), -0 (-24 to +20)]; Sleeping Giant 11 of 19, +3 (-16 to +22) [round 5: n 17, won 12 (71%), +11 (-10 to +30)].
- Loop, Rest-vs-Rest: teams holding cap C won 2 of 10 (small n) (-31 (-57 to +1)); round 5 had 1 of 9 and called it clear. It is no longer clear.

New reference rows from the timeline (all games; the same teams, other moments):

| what | team-games | they won (interval) | the other side won | strength predicts | actual - expected (interval) | Bradley-Terry check | Rest-vs-Rest only |
|---|---|---|---|---|---|---|---|
| more caps than the enemy at 5:00 | 107 | 70, 65% (56 to 74) | 35% | 61.7 | +8 (-0 to +15) | +6 (-2 to +12) | 29 of 51, +2 (-11 to +14) |
| more caps than the enemy at 8:00 | 97 | 61, 63% (54 to 72) | 37% | 54.7 | +6 (-2 to +14) | +2 (-5 to +9) | 24 of 44, -1 (-14 to +13) |
| more caps than the enemy at 10:00 (games still running then) | 102 | 62, 61% (52 to 70) | 39% | 55.0 | +7 (-2 to +15) | +4 (-4 to +11) | 31 of 51, +8 (-6 to +20) |
| held more caps for longer than the enemy over the first 8 minutes | 166 | 110, 66% (59 to 74) | 34% | 93.3 | +10 (+3 to +17) clear | +7 (+2 to +13) clear | 50 of 84, +5 (-4 to +15) |
| held more caps for at least half of the first 8 minutes | 39 | 28, 72% (57 to 86) | 28% | 24.3 | +9 (-2 to +21) | +6 (-5 to +18) | 12 of 18, +5 (-14 to +20) |

- Time-weighted: winners held more caps than the enemy for 26% of the first 8 minutes on average, losers for 14%; the two sides were level on caps 60% of the time. The side that led on caps for longer won 66% and beat its strength by +10 (+3 to +17) clear; in Rest-vs-Rest games +5 (-4 to +15). 153 of 166 games were still running at 10:00.
- Holding a cap at 8:00 is partly a result of already winning. Teams with more caps at 8:00 were already ahead on score in 72 of 97 (74%; median lead +105 points). Cap leaders who were also ahead on score won 56 of 72; cap leaders level or behind on score won 5 of 25. The team ahead on score at 8:00 won 131 of 165 (79%). 69 of 166 games were level on caps. In the 57 Top 6 vs Rest games the Top 6 clan held more caps in 30, fewer in 10, and won 50.
- Separate row, not in any table above: the 5 games that ended before 8:00, state at the end. The team with more caps at the end won 5 of 5. These are routs; they say nothing about caps.
- Check: the number of games with a cap leader at 8:00 counted a second way, straight from the timeline rows: 97 (table: 97).

**Top 6 or Shared:** Shared. In Rest-vs-Rest games holding more caps is worth -1 (-15 to +13) points over expected. Only a 2+ cap lead stays clear there (+20 (+5 to +33) clear, n 21; Bradley-Terry +14 (+2 to +24) clear).

**Clans:** not a spot item.

**Could not be done / proxy:** Nothing is missing any more: every game has its cap owners at the exact second. The data still cannot separate "holding the cap helped" from "the winning team held the cap"; the score at 8:00 shows most cap leaders were already ahead.

**Verdict:** Keep (as a caution). Land of Fire middle caps A and B: Lead for the Land of Fire page, with the small-n warning (B: +20 (+6 to +34) clear, Bradley-Terry +14 (+2 to +25) clear; A: +18 (+1 to +34) clear).

**Changed from round 5:**

| number | round 5 (154 games, snapshot within 60 s) | round 5b (exact 8:00, timeline) | difference |
|---|---|---|---|
| games in the tables | 154 | 166 | +12 |
| Rest-vs-Rest games | 76 | 84 | +8 |
| games level on caps at 8:00 | 63 of 154 | 69 of 166 |  |
| cap leaders already ahead on score | 66 of 91 (73%), median +95 | 72 of 97 (74%), median +105 |  |
| score leader at 8:00 won | 120 of 153 (78%) | 131 of 165 (79%) |  |
| Top 6 vs Rest games: Top 6 more / fewer caps / won | 53 games: 30 / 7 / 46 | 57 games: 30 / 10 / 50 |  |
| pooled, all games: its own-side cap | n 184, won 94 (51%), +1 (-3 to +4) | n 199, won 101 (51%), +0 (-3 to +4) | n +15, wins +7, -0 pts |
| pooled, all games: the enemy-side cap | n 47, won 25 (53%), +2 (-10 to +15) | n 50, won 26 (52%), +2 (-11 to +14) | n +3, wins +1, -0 pts |
| pooled, all games: at least one middle cap | n 231, won 131 (57%), +5 (+1 to +8) clear | n 247, won 136 (55%), +3 (+0 to +7) clear | n +16, wins +5, -1 pts |
| pooled, all games: every middle cap | n 43, won 27 (63%), +6 (-5 to +18) | n 49, won 31 (63%), +6 (-5 to +16) | n +6, wins +4, -1 pts |
| pooled, all games: more caps than the enemy (reference) | n 91, won 60 (66%), +8 (-0 to +17) | n 97, won 61 (63%), +6 (-2 to +14) | n +6, wins +1, -2 pts |
| pooled, all games: 2+ more caps than the enemy | n 42, won 31 (74%), +15 (+4 to +26) clear | n 45, won 33 (73%), +13 (+3 to +24) clear | n +3, wins +2, -2 pts |
| pooled, Rest-vs-Rest: its own-side cap | n 88, won 46 (52%), +2 (-3 to +7) | n 100, won 52 (52%), +2 (-3 to +7) | n +12, wins +6, -0 pts |
| pooled, Rest-vs-Rest: the enemy-side cap | n 26, won 15 (58%), +8 (-9 to +26) | n 26, won 15 (58%), +7 (-12 to +26) | n +0, wins +0, -1 pts |
| pooled, Rest-vs-Rest: at least one middle cap | n 119, won 64 (54%), +2 (-2 to +6) | n 131, won 69 (53%), +1 (-3 to +5) | n +12, wins +5, -1 pts |
| pooled, Rest-vs-Rest: every middle cap | n 22, won 14 (64%), +5 (-12 to +23) | n 25, won 16 (64%), +4 (-12 to +18) | n +3, wins +2, -1 pts |
| pooled, Rest-vs-Rest: more caps than the enemy (reference) | n 41, won 23 (56%), +1 (-12 to +15) | n 44, won 24 (54%), -1 (-15 to +13) | n +3, wins +1, -2 pts |
| pooled, Rest-vs-Rest: 2+ more caps than the enemy | n 20, won 16 (80%), +22 (+7 to +36) clear | n 21, won 17 (81%), +20 (+5 to +33) clear | n +1, wins +1, -2 pts |
| Hotspot, all games: A (enemy side) | n 9, won 6 (67%), +12 (-21 to +42) | n 9, won 6 (67%), +12 (-20 to +42) | n +0, wins +0, +0 pts |
| Hotspot, all games: B (own side) | n 49, won 26 (53%), +2 (-3 to +8) | n 53, won 28 (53%), +2 (-3 to +7) | n +4, wins +2, -0 pts |
| Hotspot, all games: C (middle) | n 28, won 20 (71%), +16 (+1 to +30) clear | n 29, won 21 (72%), +16 (+0 to +32) clear | n +1, wins +1, +0 pts |
| Hotspot, all games: D (middle) | n 29, won 16 (55%), +4 (-13 to +20) | n 30, won 16 (53%), +1 (-14 to +17) | n +1, wins +0, -3 pts |
| Hotspot, all games: more caps than the enemy (reference) | n 12, won 10 (83%), +27 (+6 to +45) clear | n 12, won 10 (83%), +25 (+2 to +42) clear | n +0, wins +0, -2 pts |
| Hotspot, Rest-vs-Rest: B (own side) | n 27, won 16 (59%), +8 (+2 to +18) clear | n 31, won 18 (58%), +7 (+2 to +16) clear | n +4, wins +2, -1 pts |
| Hotspot, Rest-vs-Rest: C (middle) | n 15, won 10 (67%), +10 (-15 to +32) | n 16, won 11 (69%), +10 (-14 to +31) | n +1, wins +1, +1 pts |
| Hotspot, Rest-vs-Rest: D (middle) | n 16, won 9 (56%), +2 (-21 to +23) | n 17, won 9 (53%), -2 (-24 to +20) | n +1, wins +0, -4 pts |
| Hotspot, Rest-vs-Rest: more caps than the enemy (reference) | n 10, won 8 (80%), +25 (-3 to +47) | n 10, won 8 (80%), +22 (-2 to +45) | n +0, wins +0, -3 pts |
| Land of Fire, all games: A (middle) | n 18, won 14 (78%), +20 (+2 to +38) clear | n 21, won 16 (76%), +18 (+1 to +34) clear | n +3, wins +2, -2 pts |
| Land of Fire, all games: B (middle) | n 20, won 16 (80%), +19 (+3 to +33) clear | n 21, won 17 (81%), +20 (+6 to +34) clear | n +1, wins +1, +1 pts |
| Land of Fire, all games: C (enemy side) | n 12, won 5 (42%), -5 (-31 to +22) | n 12, won 5 (42%), -5 (-29 to +21) | n +0, wins +0, +0 pts |
| Land of Fire, all games: D (own side) | n 34, won 16 (47%), -2 (-11 to +8) | n 36, won 17 (47%), -2 (-10 to +7) | n +2, wins +1, +0 pts |
| Land of Fire, all games: more caps than the enemy (reference) | n 14, won 12 (86%), +24 (+1 to +42) clear | n 15, won 13 (87%), +25 (+5 to +40) clear | n +1, wins +1, +1 pts |
| Land of Fire, Rest-vs-Rest: A (middle) | n 10, won 7 (70%), +11 (-18 to +35) | n 12, won 8 (67%), +10 (-12 to +31) | n +2, wins +1, -1 pts |
| Land of Fire, Rest-vs-Rest: B (middle) | n 10, won 7 (70%), +15 (-13 to +39) | n 11, won 8 (73%), +17 (-7 to +40) | n +1, wins +1, +2 pts |
| Land of Fire, Rest-vs-Rest: C (enemy side) | n 8, won 4 (50%), +5 (-26 to +33) | n 8, won 4 (50%), +5 (-24 to +34) | n +0, wins +0, +0 pts |
| Land of Fire, Rest-vs-Rest: D (own side) | n 14, won 7 (50%), +3 (-13 to +23) | n 16, won 8 (50%), +2 (-12 to +19) | n +2, wins +1, -0 pts |
| Land of Fire, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 5) | too few (n 6) |  |
| Loop, all games: A (middle) | n 16, won 6 (38%), -10 (-30 to +14) | n 19, won 8 (42%), -7 (-28 to +14) | n +3, wins +2, +2 pts |
| Loop, all games: B (middle) | n 18, won 11 (61%), +8 (-12 to +28) | n 21, won 13 (62%), +9 (-10 to +29) | n +3, wins +2, +1 pts |
| Loop, all games: C (middle) | n 14, won 6 (43%), -16 (-38 to +8) | n 15, won 7 (47%), -12 (-36 to +14) | n +1, wins +1, +4 pts |
| Loop, all games: more caps than the enemy (reference) | n 13, won 6 (46%), -12 (-37 to +13) | n 15, won 8 (53%), -6 (-30 to +19) | n +2, wins +2, +7 pts |
| Loop, Rest-vs-Rest: A (middle) | n 9, won 4 (44%), -3 (-38 to +33) | n 11, won 5 (46%), -4 (-35 to +28) | n +2, wins +1, -1 pts |
| Loop, Rest-vs-Rest: B (middle) | n 10, won 6 (60%), +9 (-22 to +40) | n 12, won 7 (58%), +9 (-25 to +39) | n +2, wins +1, -0 pts |
| Loop, Rest-vs-Rest: C (middle) | n 9, won 1 (11%), -40 (-57 to -15) clear | n 10, won 2 (20%), -31 (-57 to +1) | n +1, wins +1, +9 pts |
| Loop, Rest-vs-Rest: more caps than the enemy (reference) | n 8, won 2 (25%), -26 (-56 to +13) | n 9, won 3 (33%), -18 (-54 to +19) | n +1, wins +1, +8 pts |
| Mountain Range, all games: A (middle) | n 12, won 6 (50%), -2 (-29 to +21) | n 14, won 9 (64%), +8 (-12 to +29) | n +2, wins +3, +9 pts |
| Mountain Range, all games: B (middle) | n 17, won 11 (65%), +11 (-9 to +30) | n 18, won 12 (67%), +11 (-8 to +30) | n +1, wins +1, +0 pts |
| Mountain Range, all games: C (middle) | n 19, won 10 (53%), +1 (-19 to +20) | n 20, won 9 (45%), -5 (-23 to +14) | n +1, wins -1, -6 pts |
| Mountain Range, all games: more caps than the enemy (reference) | n 12, won 9 (75%), +15 (-6 to +35) | n 14, won 10 (71%), +12 (-8 to +30) | n +2, wins +1, -3 pts |
| Mountain Range, Rest-vs-Rest: A (middle) | too few (n 5) | too few (n 6) |  |
| Mountain Range, Rest-vs-Rest: B (middle) | too few (n 7) | n 8, won 6 (75%), +8 (-19 to +34) |  |
| Mountain Range, Rest-vs-Rest: C (middle) | n 8, won 4 (50%), +9 (-21 to +37) | n 9, won 3 (33%), -5 (-31 to +21) | n +1, wins -1, -14 pts |
| Mountain Range, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 5) |  |
| Okinawa, all games: A (own side) | n 22, won 12 (54%), +2 (-11 to +16) | n 23, won 12 (52%), -0 (-13 to +12) | n +1, wins +0, -3 pts |
| Okinawa, all games: B (enemy side) | n 9, won 5 (56%), +5 (-26 to +39) | n 10, won 5 (50%), -2 (-30 to +27) | n +1, wins +0, -6 pts |
| Okinawa, all games: C (middle) | n 15, won 6 (40%), -3 (-26 to +20) | n 16, won 7 (44%), -0 (-24 to +22) | n +1, wins +1, +3 pts |
| Okinawa, all games: D (middle) | n 15, won 6 (40%), -14 (-37 to +9) | n 16, won 7 (44%), -10 (-33 to +12) | n +1, wins +1, +4 pts |
| Okinawa, all games: more caps than the enemy (reference) | n 8, won 3 (38%), -11 (-38 to +17) | too few (n 7) |  |
| Okinawa, Rest-vs-Rest: A (own side) | n 16, won 8 (50%), +3 (-13 to +20) | n 16, won 8 (50%), +2 (-15 to +18) | n +0, wins +0, -1 pts |
| Okinawa, Rest-vs-Rest: C (middle) | n 10, won 6 (60%), +14 (-15 to +41) | n 10, won 6 (60%), +14 (-15 to +41) | n +0, wins +0, +0 pts |
| Okinawa, Rest-vs-Rest: D (middle) | n 10, won 4 (40%), -16 (-42 to +15) | n 10, won 4 (40%), -16 (-42 to +14) | n +0, wins +0, +0 pts |
| Okinawa, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 3) |  |
| Sea of Fortune, all games: A (enemy side) | too few (n 6) | too few (n 7) |  |
| Sea of Fortune, all games: B (own side) | n 32, won 16 (50%), -1 (-8 to +6) | n 35, won 17 (49%), -1 (-7 to +6) | n +3, wins +1, -0 pts |
| Sea of Fortune, all games: C (middle) | n 16, won 6 (38%), -12 (-29 to +8) | n 18, won 6 (33%), -13 (-31 to +4) | n +2, wins +0, -2 pts |
| Sea of Fortune, all games: D (middle) | n 17, won 12 (71%), +15 (-5 to +30) | n 18, won 12 (67%), +14 (-6 to +31) | n +1, wins +0, -1 pts |
| Sea of Fortune, all games: more caps than the enemy (reference) | n 15, won 8 (53%), -0 (-24 to +20) | n 15, won 7 (47%), -2 (-22 to +18) | n +0, wins -1, -2 pts |
| Sea of Fortune, Rest-vs-Rest: B (own side) | n 15, won 7 (47%), -5 (-18 to +3) | n 17, won 8 (47%), -4 (-16 to +3) | n +2, wins +1, +1 pts |
| Sea of Fortune, Rest-vs-Rest: C (middle) | n 8, won 3 (38%), -12 (-38 to +16) | n 9, won 3 (33%), -16 (-38 to +11) | n +1, wins +0, -4 pts |
| Sea of Fortune, Rest-vs-Rest: D (middle) | n 9, won 7 (78%), +16 (-10 to +35) | n 10, won 7 (70%), +14 (-11 to +36) | n +1, wins +0, -2 pts |
| Sea of Fortune, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 6) | too few (n 5) |  |
| Sleeping Giant, all games: A (middle) | n 29, won 17 (59%), +6 (-9 to +20) | n 32, won 15 (47%), -3 (-18 to +11) | n +3, wins -2, -9 pts |
| Sleeping Giant, all games: B (middle) | n 16, won 10 (62%), +10 (-9 to +31) | n 17, won 10 (59%), +7 (-13 to +27) | n +1, wins +0, -3 pts |
| Sleeping Giant, all games: C (enemy side) | n 11, won 6 (54%), +2 (-25 to +28) | n 12, won 7 (58%), +6 (-20 to +30) | n +1, wins +1, +4 pts |
| Sleeping Giant, all games: D (own side) | n 47, won 24 (51%), +0 (-5 to +6) | n 52, won 27 (52%), +1 (-4 to +7) | n +5, wins +3, +1 pts |
| Sleeping Giant, all games: more caps than the enemy (reference) | n 17, won 12 (71%), +11 (-10 to +30) | n 19, won 11 (58%), +3 (-16 to +22) | n +2, wins -1, -8 pts |
| Sleeping Giant, Rest-vs-Rest: A (middle) | n 10, won 5 (50%), +2 (-27 to +31) | n 12, won 5 (42%), -5 (-28 to +22) | n +2, wins +0, -7 pts |
| Sleeping Giant, Rest-vs-Rest: D (own side) | n 16, won 8 (50%), -2 (-16 to +10) | n 20, won 10 (50%), -2 (-14 to +8) | n +4, wins +2, +0 pts |
| Sleeping Giant, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 6) |  |

Rows that were clear in round 5 and are not now: Loop C (middle) (Rest-vs-Rest). Rows that became clear: none.

Why: better data, same definition. Twelve games with no snapshot near 8:00 are now included, the owner is read at the exact second instead of up to 60 s away, and two games on a 15-minute clock are read at the right moment. Intervals also move by a point or so between runs of the same data because they come from resampling. No conclusion changed: every pooled row moved by 3 points or less.

---

## Part C: caps and danger zones (C1-C3), Round 5 text

Source: `part-c1/FINDINGS-C1.md`.


Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Everything here is association, not cause.
Full tables: `out-caps.md` (C1, C2) and `out-danger.md` (C3). Cap letters are in the team frame (own spawn at the bottom), so a letter means the same place for both teams.

### C1. Cap defence

> **Superseded in Round 5b.** Redone from the cap timeline: see "C1 (Round 5b)". The definition of `cap_defended` and the ribbon source check below still stand. The Round 5 text is kept below for reference.


**Answer:** `cap_defended` does not mean "this smoke defended a cap". It means "at some moment while this smoke stood, a cap our team owned, on the middle line or the enemy half, had an enemy ship inside it", wherever the smoke was. It fires on 31% of smokes and the cap is usually far away (median 8.9 km). The new yes/no "enemy took the nearest cap" works as described (checked three ways) and says yes for 17% of the smokes where it applies. Defence and capture ribbons exist in replays only for the recording player and the batch does not export them, so they cannot be counted this round.

**Part 1: exact definition of `cap_defended`** (source: `crates/smoke-signals/src/analysis.rs`, `cap_metrics` lines 591-744, `contest_reason` 508-519; `smoke/DESIGN.md` line 198)

- The batch samples the game every 2 seconds. For every sample taken while the smoke existed, it looks at every cap on the map, not only the cap near the smoke.
- A cap counts at a sample when all three hold: (1) the smoking team owns it; (2) the game marks it as invaded and the invading team is the enemy (an enemy ship is inside the circle; "invader" is the game's own flag); (3) it is a "contested" cap for the smoking team: the line halfway between the spawns crosses the cap ("midline"), or the cap lies wholly on the enemy half ("enemy side"). A cap on the team's own half never counts. (The code's third reason, "enemy owns it", cannot apply because the cap must be ours.)
- The field stores the letter of the first cap that passes, in time order (cap order A, B, C, D inside one sample). One letter at most per smoke.
- What it does NOT tell you: whether the cap was kept or lost; how long the invasion lasted (one 2-second sample is enough); whether the smoke was near that cap (no distance test); whether a ship in the smoke did anything about the invader; whether an own-half cap was attacked (never counted). It uses the real cap letter, not the team-frame letter.

**Numbers: `cap_defended` in the data**

| smokes | n | cap_defended set (interval) | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all smokes | 1,547 | 31.4% (28.1 to 34.9) | 30.3% (n 538) | 32.0% (n 1,009) | -1.7 (-9.5 to +5.2) |
| destroyer smokes | 1,074 | 33.5% (30.1 to 36.7) | 32.0% (n 387) | 34.4% (n 687) | -2.3 (-11.8 to +4.3) |
| cruiser smokes | 439 | 26.9% (21.6 to 33.3) | 25.5% (n 141) | 27.5% (n 298) | -2.0 (-13.5 to +8.7) |

- 486 smokes carry it. The cap named is a middle cap in 459 and an enemy-side cap in 27; never an own-side cap.
- The named cap is the smoke's nearest cap in only 175 of 486 (36%). Smoke edge to that cap's edge: median 8,949 m (quartiles 2,044 to 16,723); 74 smokes touch the cap; 307 are more than 6 km from it.
- Was the cap still ours afterwards? (cap-owner snapshots while the smoke stood plus 60 s; all 486 have a snapshot)

| group | n | never the enemy's in the window (interval) | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all smokes with cap_defended | 486 | 60.5% (54.9 to 65.7) | 62.6% (n 163) | 59.4% (n 323) | +3.1 (-10.7 to +15.3) |
| destroyer smokes | 360 | 58.9% (52.5 to 64.9) | 59.7% (n 124) | 58.5% (n 236) | +1.2 (-15.0 to +13.3) |
| defended cap = nearest cap | 175 | 61.1% (54.9 to 67.0) | 66.7% (n 63) | 58.0% (n 112) | +8.6 (-6.2 to +21.9) |
| defended cap not the nearest | 311 | 60.1% (52.1 to 65.7) | 60.0% (n 100) | 60.2% (n 211) | -0.2 (-16.7 to +14.0) |

  With no grace: 374 of 486 kept (77.0%). With 120 s: 252 (51.9%). For comparison, any smoke whose nearest cap was ours at activation kept it in 86.3% (n 694).

**Numbers: "enemy took the cap during the smoke"** (`s['enemy_took']`; nearest cap by geometry; yes = cap not the enemy's at activation and a snapshot while the smoke stood or within 60 s after shows the enemy owning it; includes taking a neutral cap)

- Validation. (1) Hand check of 10 smokes against the raw cap states: 10 of 10 agree. (2) Own re-computation from the raw json for all 1,547: 0 mismatches. (3) Against the batch field `cap_won` (continuous cap history): of 171 smokes where `cap_won` names the nearest cap, `we_took` says yes in 144, no in 26, not applicable in 1. So the snapshot method misses about 15% of real flips. Expect `enemy_took` to under-count similarly. No bug found.
- Coverage (1,547): yes 184, no 889, not applicable 474 (cap already the enemy's). No smoke lacks a snapshot. Snapshots in the window: median 5 (quartiles 3 to 7); 111 of 1,073 (10%) have only one. Window length median 158 s; largest gap between snapshots median 48 s; unobserved tail median 21 s, over 60 s for 241 smokes (22%).
- Grace: 0 s gives 103 yes (9.6%); 60 s gives 184 (17.1%); 120 s gives 233 (21.7%).
- The nearest cap can be far: median 2,314 m from smoke centre to cap edge; 346 smokes are more than 5 km from any cap. The "within 2 km" rows are the meaningful ones.

| group | n | enemy took it (interval) | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all applicable smokes | 1,073 | 17.1% (14.8 to 19.4) | 14.4% (n 402) | 18.8% (n 671) | -4.4 (-8.9 to +0.1) |
| destroyer smokes | 762 | 18.8% (15.7 to 22.1) | 15.1% (n 291) | 21.0% (n 471) | -5.9 (-12.1 to -0.9) clear |
| smoke inside or within 2 km of the cap | 541 | 11.1% (8.8 to 13.8) | 7.9% (n 189) | 12.8% (n 352) | -4.8 (-9.2 to -0.7) clear |
| destroyer smokes inside or within 2 km | 405 | 12.8% (9.5 to 16.2) | 8.5% (n 142) | 15.2% (n 263) | -6.8 (-12.6 to -1.7) clear |
| cap ours at activation | 694 | 13.7% (10.6 to 16.7) | 12.7% (n 260) | 14.3% (n 434) | -1.6 (-8.2 to +5.0) |
| cap neutral at activation | 379 | 23.5% (18.5 to 29.3) | 17.6% (n 142) | 27.0% (n 237) | -9.4 (-18.4 to -0.5) clear |
| cap ours, cap_defended names that cap | 153 | 35.9% (28.1 to 44.0) | 30.8% (n 52) | 38.6% (n 101) | -7.8 (-24.7 to +10.5) |
| cap ours, cap_defended does not name it | 541 | 7.4% (5.5 to 9.4) | 8.2% (n 208) | 6.9% (n 333) | +1.3 (-3.4 to +5.2) |

  By map and cap (26 rows in `out-caps.md` and `caps.json`): highest are Mountain Range B 35.6% (n 45), Hotspot C 26.2% (n 65), Hotspot D 23.8% (n 84), Sleeping Giant A 21.1% (n 90), Land of Fire A 20.8% (n 53). Clear Top 6 vs Rest gaps: Loop A (Top 6 0% of 11 small n, Rest 22% of 36; -22, -37 to -8), Loop B (0% of 10 small n vs 30% of 20; -30, -57 to -9), Mountain Range A (5% of 19 vs 23% of 22; -18, -42 to -2). Land of Fire C: too few (n 5). Okinawa Top 6: too few on every cap.
- One row per smoke is in `enemy-took.csv`.

**Part 3: ribbons**

- Replay format: ribbons are in replays (`crates/wows-replays/src/analyzer/decoder/decode.rs` lines 2102-2139: `onRibbon` ids 9 Defended, 10 Captured, 11 AssistedInCapture; modern replays carry a running total in `privateVehicleState.ribbons`, read in `crates/wows-battle-world/src/ingest/combat.rs`). Only for the recording player: `wows-battle-world/src/resources.rs`, `RibbonLog`, says "Only self-player ribbons are covered".
- Smoke Signals code does not read ribbons. The only mention in `crates/smoke-signals/src/` is loading ribbon icons for the video renderer (`render.rs` lines 63-64, 93-94).
- Batch output: a text search of the whole batch folder finds the word nowhere.
- To count them: a code change in smoke-signals (read the ribbon log, attach each Defended / Captured / AssistedInCapture ribbon to the smokes standing then) and a full batch rerun, both outside this round. Even then only the recording players: 170 games have 2 replays, 1 game has 1, so about 2 ships of roughly 18. Whether the merged session keeps both players' ribbons was not checked.

**Top 6 or Shared:** `cap_defended` fires equally for both groups (-1.7, -9.5 to +5.2). On "enemy took the nearest cap", Rest lose the cap clearly more often around destroyer smokes (15.1% vs 21.0%, gap -5.9, -12.1 to -0.9) and around smokes within 2 km (7.9% vs 12.8%, gap -4.8, -9.2 to -0.7).

**Clans:** not a spot item. Per-smoke clan is in `enemy-took.csv`.

**Could not be done / proxy:** Ribbons; the proxy is `enemy_took` / `we_took` from snapshots, which misses roughly 15% of real flips.

**Verdict:** Keep (the definition and the new yes/no field; drop any reading of `cap_defended` as "the smoke defended a cap").

### C2. Cap holder at 8:00 and winning

> **Superseded in Round 5b.** Redone at exactly 8:00 for 166 games: see "C2 (Round 5b)". The Round 5 text is kept below for reference.


**Answer:** No single cap clearly adds something beyond team strength in a way that holds up. Holding more caps than the enemy at 8:00 goes with winning (66% vs 34%), but most of that is team strength and already being ahead; in Rest-vs-Rest games the edge is gone (56%, +1 point over expected). The two middle caps on Land of Fire are the only caps that stay above expectation, and they are a lead, not a result.

**Numbers**

- Coverage: nearest snapshot within 60 s of 8:00 (median 11 s away). 154 of 171 games covered; 5 ended before 8:00; 12 have no snapshot that close. Covered / all: Hotspot 30/31, Land of Fire 23/25, Loop 18/23, Mountain Range 19/21, Okinawa 16/18, Sea of Fortune 19/21, Sleeping Giant 29/32. Rest-vs-Rest covered: 76.
- "Own side" = a cap on the team's own half, more than one cap radius short of the middle line. Own-side caps: Hotspot B, Land of Fire D, Sleeping Giant D, Sea of Fortune B, Okinawa A (enemy-side twins: Hotspot A, Land of Fire C, Sleeping Giant C, Sea of Fortune A, Okinawa B). Loop and Mountain Range have none: all three caps are on the middle line. Every other cap is a middle cap.
- Expected win rate: each clan's record with this game left out; odds a = (wins + 1) / (losses + 1); chance of beating b = a / (a + b). Check model: Bradley-Terry strengths fitted without the game. Simple model's favourite won 110 of 158 (70%, predicted 67%); Bradley-Terry's won 128 of 164 (78%, predicted 74%).

All maps pooled, all covered games (154):

| what the team holds at 8:00 | team-games | holders won (interval) | others won | strength predicts | actual - expected (interval) | Bradley-Terry check |
|---|---|---|---|---|---|---|
| its own-side cap | 184 | 94, 51% (48 to 55) | 48% | 92.9 | +1 pt (-3 to +4) | -0 (-3 to +3) |
| the enemy-side cap | 47 | 25, 53% (39 to 68) | 49% | 24.0 | +2 (-10 to +15) | -1 (-13 to +10) |
| at least one middle cap | 231 | 131, 57% (53 to 61) | 30% | 120.3 | +5 (+1 to +8) clear | +3 (+0 to +6) |
| every middle cap | 43 | 27, 63% (47 to 77) | 48% | 24.3 | +6 (-5 to +18) | +4 (-5 to +16) |
| more caps than the enemy (reference) | 91 | 60, 66% (57 to 75) | 34% | 52.3 | +9 (-0 to +17) | +4 (-4 to +11) |
| 2+ more caps than the enemy | 42 | 31, 74% (60 to 87) | 46% | 24.7 | +15 (+4 to +26) clear | +9 (-0 to +17) |

(a) Rest-vs-Rest games only (76):

| what the team holds at 8:00 | team-games | holders won (interval) | others won | strength predicts | actual - expected (interval) |
|---|---|---|---|---|---|
| its own-side cap | 88 | 46, 52% (47 to 58) | 47% | 44.0 | +2 (-3 to +7) |
| the enemy-side cap | 26 | 15, 58% (39 to 77) | 48% | 13.0 | +8 (-9 to +26) |
| at least one middle cap | 119 | 64, 54% (49 to 59) | 36% | 61.6 | +2 (-2 to +6) |
| more caps than the enemy | 41 | 23, 56% (41 to 71) | 44% | 22.5 | +1 (-12 to +15) |
| 2+ more caps than the enemy | 20 | 16, 80% (61 to 95) | 45% | 11.6 | +22 (+7 to +36) clear |

Per map, caps whose holders did clearly better than strength predicts (every other cap on every map has an interval including zero; all rows are in `out-caps.md`):

| map, cap | holder team-games | holders won | others won | strength predicts | actual - expected | Bradley-Terry check | Rest-vs-Rest only |
|---|---|---|---|---|---|---|---|
| Land of Fire B (middle) | 20 | 16, 80% (60 to 95) | 27% | 12.2 | +19 pts (+3 to +33) clear | +13 (+1 to +25) clear | 7 of 10 (small n), +15 (-13 to +39) |
| Land of Fire A (middle) | 18 | 14, 78% (58 to 95) | 32% | 10.4 | +20 (+2 to +38) clear | +14 (-2 to +31) | 7 of 10 (small n), +11 (-18 to +35) |
| Hotspot C (middle) | 28 | 20, 71% (54 to 88) | 31% | 15.4 | +16 (+1 to +30) clear | +10 (-6 to +23) | 10 of 15, +10 (-15 to +32) |
| Hotspot B (own side), Rest-vs-Rest games | 27 | 16, 59% (53 to 68) | 14% (n 7) | 13.7 | +8 (+2 to +18) clear | +6 (+1 to +14) clear | this row |

- Hotspot B in Rest-vs-Rest games is really about the 7 team-games where a team had lost its home cap by 8:00 (won 1 of 7).
- Multiplicity: 26 map-and-cap rows tested; fewer than one clear positive row is expected by luck. Three came out clear on the simple model, one (Land of Fire B) on both. None is clear in Rest-vs-Rest games (small n everywhere). Land of Fire A and B share the same games.
- "More caps than the enemy" per map (all games): Hotspot 10 of 12 (small n), +27 pts (+6 to +45) clear; Land of Fire 12 of 14 (small n), +24 (+1 to +42) clear; Mountain Range 9 of 12 (small n), +15 (-6 to +35); Sleeping Giant 12 of 17, +11 (-10 to +30); Sea of Fortune 8 of 15, -0 (-24 to +20); Loop 6 of 13 (small n), -12 (-37 to +13); Okinawa 3 of 8 (small n), -11 (-38 to +17).
- Loop, Rest-vs-Rest: teams holding cap C won 1 of 9 (small n; -40 pts, -57 to -15). One of many rows; not a pattern.
- Holding a cap at 8:00 is partly a result of already winning: teams with more caps were already ahead on score in 66 of 91 (73%, median lead 95 points); the team ahead on score at 8:00 won 120 of 153 (78%). 63 of 154 games were level on caps. In the 53 covered Top 6 vs Rest games the Top 6 clan held more caps in 30, fewer in 7, and won 46.

**Top 6 or Shared:** Shared. In Rest-vs-Rest games holding more caps is worth +1 point over expected (-12 to +15). Only a 2+ cap lead stays clear there (+22, +7 to +36, n 20).

**Clans:** not a spot item.

**Could not be done / proxy:** No continuous cap timeline; "8:00" is the nearest smoke snapshot within 60 s, so 17 games are missing. The data cannot separate "holding the cap helped" from "the winning team held the cap".

**Verdict:** Keep (as a caution). Land of Fire middle caps A and B: Lead for the Land of Fire page, with the small-n warning.

### C3. Danger zones

> **Superseded in Round 5b.** Redone with real health and death positions: see "C3 (Round 5b)". No zone is kept. The Round 5 text is kept below for reference.


**Answer:** Four areas pass the rule (8+ smokes, died-or-hurt rate clearly above both the all-map and same-map baseline), but about 1.2 areas pass by luck when outcomes are shuffled, and three of the four rest on exactly 8 smokes. Only one is sturdy enough to show: destroyers that smoke inside cap C on Hotspot. Land of Fire, Loop and Okinawa have no qualifying area. No area qualifies on deaths alone.

**Numbers**

- Baselines. Destroyer smoker: 6.4 died and 15.5 died-or-hurt per 100 destroyer smokes (n 1,074: Top 6 387, Rest 687). Sheltering cruisers: 8.0 died and 22.0 died-or-hurt per 100 (613 cruisers in 561 smokes). Same-map baselines range 11.9 (Hotspot) to 22.7 (Land of Fire) for destroyers, 16.4 (Hotspot) to 37.8 (Okinawa) for cruisers.
- Health is an estimate (the batch has no ship health). "Hurt" is approximate; death-only numbers are exact.
- Areas: 10 x 10 team-frame cells with 8+ smokes; thinner cells merged inside their 2 x 2 block; plus "smoke centre inside cap X". 313 built, 109 tested (77 destroyer, 32 cruiser), 204 under 8 smokes and not rated.
- Placebo (outcomes shuffled among smokes of the same map, 120 runs): 1.23 flags by luck per run (median 1, 95th percentile 3); 5 of 120 runs had 4 or more. Real data: 4. Expect 1 to 2 of the 4 to be luck.

| map | who | area | smokes | died or hurt per 100 | baseline all / same map | gap vs all maps | gap vs same map | died per 100 (baseline) | death gap |
|---|---|---|---|---|---|---|---|---|---|
| Hotspot | destroyer smoker | inside cap C | 22 | 32 (7 of 22) | 15.5 / 11.9 | +16 (+3 to +52) | +20 (+7 to +58) | 9 (2 of 22; 6.4) | +3 (-8 to +26) |
| Sea of Fortune | destroyer smoker | E5+F5+E6 | 8 (small n) | 62 (5 of 8) | 15.5 / 14.5 | +47 (+9 to +86) | +48 (+12 to +88) | 38 (3 of 8; 6.4) | +31 (-5 to +75) |
| Sleeping Giant | destroyer smoker | E7+F7+F8 | 8 (small n) | 50 (4 of 8) | 15.5 / 16.0 | +34 (+1 to +67) | +34 (+1 to +66) | 25 (2 of 8; 6.4) | +19 (-7 to +56) |
| Mountain Range | sheltering cruisers | E7+F7+F8 | 8 (small n) | 56 (5 of 9 cruisers) | 22.0 / 20.8 | +34 (+3 to +74) | +35 (+7 to +75) | 22 (2 of 9; 8.0) | +14 (-9 to +64) |

- Laid while 50+ behind / enemy radar detection (area vs map): Hotspot cap C 18% (22%) / 23% (8%); Sea of Fortune 50% (28%) / 38% (15%); Sleeping Giant 25% (24%) / 50% (14%); Mountain Range 50% (20%) / 38% (16%).
- Per map: Sleeping Giant 25 tested, 1 flagged. Hotspot 24, 1. Mountain Range 18, 1. Sea of Fortune 13, 1. Land of Fire 9, none. Loop 14, none. Okinawa 6, none.

**Top 6 or Shared:** all four are Shared by the marking rule. Hotspot cap C is in fact a Rest habit: 0% of Top 6 destroyer smokes on Hotspot vs 14% of Rest (gap interval -23 to -4). Others: Sea of Fortune -10 to +11; Sleeping Giant -8 to +1; Mountain Range -40 to +1.

**Clans:**
- Hotspot, inside cap C (22 smokes, 8 clans, 10 games): Top 6: none | Rest: EPOXY 9, KSC 7, BTLST 1, RMN 1, 5D 1, UYSC 1, MACHX 1, MZY 1. Without KSC still 33 per 100 (n 15).
- Sea of Fortune, E5+F5+E6 (8 smokes, 7 clans, 6 games): Top 6: RESIN 2, BONKZ 1 | Rest: 5D 1, NGA 1, MACHX 1, KSE 1, RSR 1.
- Sleeping Giant, E7+F7+F8 (8 smokes, 7 clans, 8 games): Top 6: BONKZ 2 | Rest: RMN 1, SCCC2 1, PFANS 1, -BN- 1, RSR 1, KITED 1.
- Mountain Range, E7+F7+F8 (8 smokes, 6 clans, 7 games): Top 6: BONKZ 1, H-SR 1 | Rest: RSR 3, INCA 1, -BN- 1, KSC 1.

**Could not be done / proxy:** Health is an estimate. Positions are the smoke's centre, not where the ship was hit. Two thirds of areas are unrated.

**Verdict:** Lead for Hotspot cap C only. Drop the other three as map markings (n 8 each, in line with luck). Drop danger zones for Land of Fire, Loop, Okinawa.

---

## Part C: spots per map (C4), rerun with the clock fix

Source: `part-c4/FINDINGS-C4.md`.


Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Positions are team-normalized: own spawn at the bottom (bottom-left on Okinawa). Everything here is association: where smokes of a kind pile up and what those smokes returned, not what causes a result.

### C4. Spots per map, each marked Top 6 or Shared

**Answer:** There are 21 spots across six maps, and every one is a Shared spot: at the 1.5 to 2.5 km scale no place is used clearly more by the Top 6 than by the Rest. The two places that come closest to a Top 6 spot are the own-side half of cap B on Loop (cap sitters) and the own-side rim of cap B on Land of Fire (Svea); both clear the test only when the circle is widened to 2.5 km or more.

**Numbers:**

How a spot was found. For each map and each kind, all clans' smoke centres were pooled and the densest circles were taken one after another (radius 1.5 to 2.5 km, set by how tight the cluster is). A circle is a spot when it holds at least 8 smokes and at least 10% of that kind's smokes on that map (the 10% floor stops a busy map from being tiled with circles). High-paying cells use the 10 x 10 grid instead: a cell, or a pair of side-by-side cells, with 8 or more destroyer smokes whose concealed damage per smoke is clearly above the rest of that map.

Spots by map and kind:

| Map | long-smoke | cap sitter | parked cruiser | early cruiser | high-paying cell | all |
|---|---|---|---|---|---|---|
| Sleeping Giant | 1 | 1 | 0 | 1 | 1 | 4 (0 Top 6) |
| Hotspot | 1 | 2 | 0 | 2 | 1 | 6 (0 Top 6) |
| Loop | 1 | 2 | 0 | 0 | 0 | 3 (0 Top 6) |
| Mountain Range | 3 | 1 | 0 | 0 | 0 | 4 (0 Top 6) |
| Land of Fire | 0 | 1 | 1 | 0 | 0 | 2 (0 Top 6) |
| Sea of Fortune | 1 | 0 | 0 | 0 | 1 | 2 (0 Top 6) |
| Okinawa | 0 | 0 | 0 | 0 | 0 | 0 (0 Top 6) |
| All maps | 7 | 7 | 1 | 3 | 3 | 21 (0 Top 6) |

- Mode test: share of Top 6 smokes of that kind on that map that fall in the spot, minus the same share for the Rest, with a 95% interval from resampling whole clans. "Top 6 spot" also needs two Top 6 clans in it and at least 8 smokes of the kind from each group on the map.
- Result: 0 of 21 are Top 6 spots. 19 are Shared with no clear gap. 2 are Shared with "Rest use it more": cap sitters on the own-side rim of cap C on Hotspot (hs-sit-1: Top 6 6% vs Rest 23%, gap -30 to -5) and inside cap A on Loop (loop-sit-1: 4% vs 20%, gap -26 to -2).
- Closest to a Top 6 spot at this scale: Land of Fire Svea/Jinan at F5 (lof-park-1: 58% vs 19%, gap -6 to +70; the Rest side is one clan, BONKY 4), Loop cap sitters inside cap B (loop-sit-2: 30% vs 9%, gap -3 to +50), Sleeping Giant early cruiser smoke at G1/F1 (sg-early-1: 36% vs 20%, gap -8 to +38).
- Wider scale check (same search, circles 2.5 to 3.5 km; `wide.txt`): 25 spots, 2 labelled Top 6. Loop cap sitters inside cap B: 8 of 23 Top 6 smokes vs 6 of 65 Rest (35% vs 9%, gap +3 to +53; RESIN 3, HTDOG 2, VRTUS 1, BONKZ 1, H-SR 1 / Rest: REEEE 5, SCCC2 1). Land of Fire Svea/Jinan at F5: 14 of 19 vs 5 of 21 (74% vs 24%, gap +8 to +84; VRTUS 8, HTDOG 4, RESIN 2 / Rest: BONKY 4, -BN- 1). These are the same two places round 4 called signature spots; they are zones about 5 km across, not tight spots.
- Placebo for the "Top 6 spot" label (said once): the real Top 6 were left out, the same search was run on the Rest alone, and six of the twelve busiest Rest clans stood in as the top group, 200 draws. At the main scale 12 Rest-only spots were found and 0.33 of them were labelled "top" by chance on average (range 0 to 3). At the wider scale 14 spots, 0.54 on average (range 0 to 4); 7% of draws gave 2 or more. So the two wide-scale Top 6 zones are a little more than chance would give, not a lot more. Treat them as leads.
- High-paying cells: 137 cells or pairs were tested, 3 passed: Sleeping Giant G1 (24.1k per smoke vs 10.7k elsewhere, gap +8.2k to +20.2k, n 21), Hotspot G10+H10 (17.0k vs 11.4k, gap +0.8k to +10.7k, n 40), Sea of Fortune F9+G9 (24.6k vs 10.3k, gap +1.0k to +32.5k, n 10, small n). The cells were picked and scored on the same data, so they will shrink on new data. A shuffle check (concealed damage shuffled among each map's destroyer smokes, 20 runs) passed 1.85 cells on average (range 0 to 4), so only G1, whose interval is far from zero, should be trusted on its own.
- Win/loss split is shown where the two means are more than 5k apart with at least 5 smokes on each side. Sleeping Giant G1 pays in both (wins 26.5k, n 14; losses 19.3k, n 7). Hotspot G10+H10: wins 21.3k (n 16), losses 14.1k (n 24). Sea of Fortune F9+G9 has only 2 losses: too few to split.
- Cap taken (cap nearest the smoke, not already ours, ours within 60 s of the smoke clearing): G1 19% of 21, Hotspot G10+H10 34% of 35, Sea of Fortune F9+G9 25% of 8 (small n).
- Early cruiser smoke spots exist on two maps only: Sleeping Giant G1/F1 (n 16: cruiser inside 12, screened 4), Hotspot G10/F10 (n 17: inside 13, screened 4) and Hotspot G6/G5 (n 9: inside 7, screened 2, small n). The first two are the same water as the long-smoke spot and the high-paying cell on those maps: one opening, seen three ways.

**Top 6 or Shared:** Shared, all 21. No interval of the share gap is above zero at the 1.5 to 2.5 km scale; two are below zero (Rest use them more). Two wider zones (Loop cap B for cap sitters, Land of Fire F5 for Svea) pass at 2.5 km and are flagged as leads.

**Clans:** named with counts for every spot in the map tables below (and in `spots.json`).

**Could not be done / proxy:**
- "Covered by" a spot means a cruiser was inside the smoke or screened by it (behind it or firing through it); this comes from the batch's own per-smoke record, not from a continuous track.
- "Selfish" here means the ship type (cap sitters; Svea/Jinan), not the batch's selfish flag; the flag's share per spot is in `spots.json` (`selfish_flag_pct`).
- Parked cruiser smoke (Svea/Jinan) forms a compact spot on one map only. On Sea of Fortune and Mountain Range the Top 6 Svea smokes sit in wide bands (round 4's zones there were 6 to 10 km across), too spread to be a spot under this round's rule.
- Okinawa has no spot of any kind: pools are small (16 to 40 smokes per kind) and spread out, and the Top 6 laid only 2 to 10 smokes per kind there.
- Cap taken uses cap owners recorded only at smoke moments, so it is unknown for some smokes (they are left out of the rate).

**Verdict:** Keep (as the per-map catalogue; the Top 6 vs Shared marking finds no Top 6 spot at this scale, and the two wide zones are leads, not findings).

### Per-map spot tables

Columns: mode shows the share of each group's smokes of that kind on that map that fall in the spot, the gap and its 95% interval. "Cruisers" lists the cruisers inside the smoke and those screened by it, Top 6 then Rest (top three by count; full lists in `spots.json`). Damage is concealed damage per smoke. "small n" = 8 to 14 smokes. Examples are the three highest-damage smokes in the spot.

Wide-scale leads: loop-sit-2 (Loop, cap B, cap sitters) and lof-park-1 (Land of Fire, F5, Svea) become "Top 6" when the circle is 2.5 km; everything else stays Shared at both scales.

#### Sleeping Giant

Figure: `figures/c4-sg.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 42 such smokes on this map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| sg-long-1 | long-smoke | 2.5 km outside cap A, own side, west edge of the map (G1/F1) | Shared: 18% vs 12% (gap +6, -7 to +22) | 12 / 9 | Top 6: BONKZ 4, VRTUS 3, H-SR 3, RESIN 2 / Rest: BONKY 3, PFANS 2, KSC 2, NGA 1, EPOXY 1 | Top 6: inside Des Moines 3, Worcester 3, Brisbane 1 +1 more; screened Brisbane 3, Utrecht 1 / Rest: inside Brisbane 3, Salem 1, Minotaur 1 +2 more; screened Minotaur 1, Bremen 1 | 20.7k | 10 | 2:40 | wins 27.5k (n 10) vs losses 14.5k (n 11); ships: Harugumo 8, Gearing 7, Somers 6 |
| sg-sit-1 | selfish: cap sitter | 1.7 km outside cap B, own side (G6/F6) | Shared: 12% vs 17% (gap -5, -23 to +8) | 5 / 9 | Top 6: HTDOG 4, VRTUS 1 / Rest: HFANS 3, KSE 2, BONKY 2, EPOXY 1, KSC 1 | Top 6: screened Moskva 1, Stalingrad 1 / Rest: screened Des Moines 1, Stalingrad 1, Petropavlovsk 1 | 8.0k | 14 | 6:36 | small n; wins 11.8k (n 9) vs losses 1.4k (n 5); ships: Daring 7, Gdańsk 6, Z-52 1 |
| sg-early-1 | early cruiser | 2.6 km outside cap A, own side, west edge of the map (G1/F1) | Shared: 36% vs 20% (gap +16, -8 to +38) | 10 / 6 | Top 6: BONKZ 3, RESIN 3, VRTUS 2, H-SR 2 / Rest: PFANS 2, KSC 2, BONKY 1, EPOXY 1 | Top 6: inside Des Moines 3, Worcester 2, Brisbane 1 +1 more; screened Brisbane 2, Utrecht 1 / Rest: inside Salem 1, Brisbane 1, Minotaur 1 +2 more; screened Minotaur 1 | 22.6k | 6 | 2:20 | inside 12 (Top 6 7, Rest 5), screened 4 (Top 6 3, Rest 1); wins 28.2k (n 9) vs losses 15.3k (n 7) |
| sg-cell-1 | high-paying cell | 4.1 km outside cap A, own side, west edge of the map (G1) | Shared: 11% vs 7% (gap +4, -4 to +13) | 12 / 9 | Top 6: RESIN 5, VRTUS 3, BONKZ 2, HTDOG 1, H-SR 1 / Rest: BONKY 3, KSC 2, PFANS 2, NGA 1, -BN- 1 | Top 6: inside Worcester 3, Des Moines 3, Utrecht 1 +4 more; screened Utrecht 1, Brisbane 1 / Rest: inside Brisbane 3, Des Moines 3, Salem 1 +1 more; screened Bremen 1 | 24.1k | 14 | 2:40 | 24.1k vs 10.7k elsewhere on the map (gap +8.2k to +20.2k); median 21.9k; 10 clans, 13 games; cap taken 19% of 21; wins 26.5k (n 14) vs losses 19.3k (n 7) |

Examples: sg-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7990_g1_188224.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7992_g1_29782.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7936_g1_104465.html); sg-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8153_g1_92180.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8150_g2_188191.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8145_g1_161939.html); sg-early-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7990_g1_188224.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7992_g1_29782.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7906_g1_188243.html); sg-cell-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7990_g1_188224.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7992_g1_29782.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7936_g1_104465.html)

#### Hotspot

Figure: `figures/c4-hs.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 27 such smokes on this map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| hs-long-1 | long-smoke | 2.6 km outside cap D, own side, east edge of the map (G10) | Shared: 14% vs 22% (gap -8, -22 to +1) | 9 / 18 | Top 6: RESIN 3, H-SR 2, BONKZ 2, HTDOG 1, KITE 1 / Rest: BONKY 4, BTLST 3, HFANS 2, -BN- 2, REEEE 2, KSC 2, MZY 1, PN 1, PFANS 1 | Top 6: inside Worcester 3, Brisbane 2, Des Moines 2 +1 more; screened Des Moines 1, Prins van Oranje 1 / Rest: inside Brisbane 9, Des Moines 5; screened Bremen 2, Brisbane 1, Des Moines 1 | 16.1k | 4 | 3:16 | ships: Somers 11, Gearing 9, Harugumo 7 |
| hs-sit-1 | selfish: cap sitter | on the rim of cap C, own side (F6/F5/G5) | Shared: 6% vs 23% (gap -17, -30 to -5); Rest use it more | 1 / 17 | Top 6: H-SR 1 / Rest: KSC 5, EPOXY 5, PFANS 2, BTLST 1, UYSC 1, HFANS 1, INCA 1, MACHX 1 | Top 6: inside Petropavlovsk 1 / Rest: screened Petropavlovsk 1, Prins van Oranje 1 | 2.1k | 0 | 4:56 | ships: Daring 10, Gdańsk 7, Grozovoi 1 |
| hs-sit-2 | selfish: cap sitter | 0.5 km outside cap D, own side, east edge of the map (F10/G10) | Shared: 12% vs 12% (gap +0, -22 to +12) | 2 / 9 | Top 6: H-SR 2 / Rest: 5D 3, KITED 2, INCA 1, MACH 1, MACHX 1, SCCC2 1 | Top 6: inside Brisbane 1; screened Brisbane 1 / Rest: screened San Martín 3 | 11.3k | 0 | 5:33 | small n; ships: Grozovoi 4, Daring 4, Shimakaze 3 |
| hs-early-1 | early cruiser | 2.4 km outside cap D, own side, east edge of the map (G10/F10) | Shared: 36% vs 28% (gap +8, -13 to +34) | 8 / 9 | Top 6: H-SR 2, BONKZ 2, RESIN 2, HTDOG 1, KITE 1 / Rest: HFANS 2, BTLST 1, PN 1, -BN- 1, BONKY 1, REEEE 1, PFANS 1, KSC 1 | Top 6: inside Brisbane 2, Des Moines 2, Worcester 2; screened Brisbane 1, Des Moines 1, Prins van Oranje 1 / Rest: inside Brisbane 4, Des Moines 3; screened Des Moines 1, Bremen 1 | 19.0k | 0 | 2:44 | inside 13 (Top 6 6, Rest 7), screened 4 (Top 6 2, Rest 2); wins 16.1k (n 8) vs losses 21.5k (n 9) |
| hs-early-2 | early cruiser | 1.8 km outside cap C, own side (G6/G5) | Shared: 18% vs 16% (gap +3, -15 to +20) | 4 / 5 | Top 6: BONKZ 2, H-SR 1, RESIN 1 / Rest: KSC 2, OGF 1, -BN- 1, MZY 1 | Top 6: inside Brisbane 2, Utrecht 1, Minotaur 1 +1 more; screened Worcester 1 / Rest: inside Minotaur 2, Des Moines 1; screened Brennus 1, Brisbane 1, Petropavlovsk 1 +1 more | 6.8k | 0 | 2:08 | small n; inside 7 (Top 6 4, Rest 3), screened 2 (Top 6 0, Rest 2) |
| hs-cell-1 | high-paying cell | 5.9 km outside cap D, own side, east edge of the map (G10/H10) | Shared: 16% vs 17% (gap -1, -12 to +8) | 13 / 27 | Top 6: H-SR 5, RESIN 4, HTDOG 1, VRTUS 1, KITE 1, BONKZ 1 / Rest: REEEE 5, BONKY 4, BTLST 3, -BN- 3, MZY 2, HFANS 2, KITED 2, KSC 2, NGA 1, SCCC2 1, PFANS 1, EPOXY 1 | Top 6: inside Worcester 4, Brisbane 3, Des Moines 2 +1 more; screened Brisbane 1, Des Moines 1, Prins van Oranje 1 / Rest: inside Brisbane 9, Des Moines 6, Prinz Adalbert 1 +2 more; screened Bremen 4, Brisbane 1, Des Moines 1 +1 more | 17.0k | 10 | 5:35 | 17.0k vs 11.4k elsewhere on the map (gap +0.8k to +10.7k); median 11.0k; 18 clans, 18 games; cap taken 34% of 35; wins 21.3k (n 16) vs losses 14.1k (n 24) |

Examples: hs-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g2_90084.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8141_g2_161896.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8148_g2_125976.html); hs-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8068_g3_48783.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7970_g1_159228.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8072_g1_103842.html); hs-sit-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7959_g1_87003.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8073_g1_34492.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7888_g1_38992.html); hs-early-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g2_90084.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8148_g2_125976.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8139_g2_200262.html); hs-early-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8072_g1_103837.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8067_g1_60864.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8174_g1_94344.html); hs-cell-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g2_90084.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8141_g2_161896.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g2_224008.html)

#### Loop

Figure: `figures/c4-loop.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 15 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 21 such smokes on this map); no high-paying cell (of 21 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| loop-long-1 | long-smoke | 1.6 km outside cap B, own side (F8/G8) | Shared: 22% vs 15% (gap +7, -21 to +85) | 4 / 4 | Top 6: BONKZ 3, RESIN 1 / Rest: OGF 1, KM 1, MACHX 1, HFANS 1 | Top 6: inside Brisbane 3, Des Moines 1; screened Utrecht 1 / Rest: inside Des Moines 2; screened Worcester 1 | 36.0k | 12 | 5:12 | small n; ships: Gearing 4, Somers 3, Harugumo 1 |
| loop-sit-1 | selfish: cap sitter | inside cap A, own side (F4) | Shared: 4% vs 20% (gap -16, -26 to -2); Rest use it more | 1 / 13 | Top 6: KITE 1 / Rest: REEEE 5, EPOXY 3, MACH 2, KITED 1, -BN- 1, HFANS 1 | Top 6: none / Rest: inside Des Moines 1; screened Prins van Oranje 1 | 6.7k | 0 | 8:02 | small n; ships: Daring 12, Z-42 2 |
| loop-sit-2 | selfish: cap sitter | inside cap B, own side (F7) | Shared: 30% vs 9% (gap +21, -3 to +50) | 7 / 6 | Top 6: RESIN 3, HTDOG 2, VRTUS 1, H-SR 1 / Rest: REEEE 5, SCCC2 1 | Top 6: inside Minotaur 1; screened Petropavlovsk 2, Moskva 1, Prins van Oranje 1 / Rest: none | 2.3k | 0 | 9:26 | small n; ships: Z-42 5, Gdańsk 4, Shimakaze 3, Daring 1 |

Examples: loop-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7889_g1_178499.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7891_g1_46432.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8068_g1_178435.html); loop-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7917_g1_116013.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8070_g2_163984.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8148_g1_20502.html); loop-sit-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7976_g1_219218.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8150_g1_34881.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8176_g4_180815.html)

#### Mountain Range

Figure: `figures/c4-mr.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 46 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 28 such smokes on this map); no high-paying cell (of 20 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| mr-long-1 | long-smoke | 2.1 km outside cap B, own side (F4/G4) | Shared: 11% vs 20% (gap -9, -27 to +7) | 4 / 8 | Top 6: KITE 2, H-SR 1, BONKZ 1 / Rest: -BN- 3, HFANS 2, BONKY 2, INCA 1 | Top 6: inside Minotaur 2, Des Moines 1, Svea 1; screened Salem 1 / Rest: inside Brisbane 3, Smolensk 2, Minotaur 1; screened Brisbane 1, Napoli 1, Smolensk 1 | 14.3k | 0 | 3:48 | small n; ships: Gearing 6, Somers 5, Harugumo 1 |
| mr-long-2 | long-smoke | 2.1 km outside cap C, own side (G7) | Shared: 19% vs 7% (gap +12, -5 to +26) | 7 / 3 | Top 6: H-SR 3, BONKZ 2, RESIN 2 / Rest: UYSC 1, NGA 1, KSC 1 | Top 6: inside Minotaur 3, Des Moines 2, Svea 1; screened Brisbane 1, Moskva 1 / Rest: screened Worcester 1, Bremen 1, Des Moines 1 | 17.8k | 30 | 5:25 | small n; wins 22.5k (n 5) vs losses 13.1k (n 5); ships: Somers 6, Gearing 3, Harugumo 1 |
| mr-long-3 | long-smoke | 2.3 km outside cap B, own side (G5/G4) | Shared: 14% vs 10% (gap +4, -15 to +17) | 5 / 4 | Top 6: KITE 3, H-SR 2 / Rest: INCA 2, UYSC 1, PN 1 | Top 6: inside Brisbane 2, Des Moines 1, Moskva 1 +2 more; screened Stalingrad 1, Moskva 1 / Rest: inside Minotaur 2, Des Moines 1, Brisbane 1; screened Svea 1 | 10.0k | 11 | 2:37 | small n; ships: Gearing 5, Somers 4 |
| mr-sit-1 | selfish: cap sitter | on the rim of cap C, own side (F7) | Shared: 25% vs 16% (gap +9, -14 to +35) | 4 / 5 | Top 6: RESIN 2, BONKZ 2 / Rest: HFANS 3, SCCC2 1, MACH 1 | Top 6: none / Rest: screened San Martín 1 | 4.3k | 0 | 4:27 | small n; ships: Gdańsk 4, Daring 4, Z-42 1 |

Examples: mr-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7931_g1_214651.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8146_g2_121102.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159422.html); mr-long-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8069_g2_143195.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159429.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159438.html); mr-long-3: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7901_g1_27149.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7984_g1_15359.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7930_g1_51294.html); mr-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159435.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7901_g1_27140.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159425.html)

#### Land of Fire

Figure: `figures/c4-lof.png`. Not found here: no long-smoke spot (no compact place holds 8 of the 57 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 25 such smokes on this map); no high-paying cell (of 10 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| lof-sit-1 | selfish: cap sitter | on the rim of cap B, own side (F5) | Shared: 10% vs 16% (gap -6, -32 to +13) | 3 / 6 | Top 6: VRTUS 3 / Rest: -BN- 3, SCCC2 1, MACHX 1, HFANS 1 | Top 6: inside Svea 3 / Rest: none | 2.6k | 0 | 7:08 | small n; ships: Daring 6, Z-42 3 |
| lof-park-1 | selfish: parked cruiser | 1.0 km outside cap B, own side (F5) | Shared: 58% vs 19% (gap +39, -6 to +70) | 11 / 4 | Top 6: VRTUS 7, HTDOG 2, RESIN 2 / Rest: BONKY 4 | Top 6: none / Rest: none | 11.0k | 7 | 6:13 | wins 16.1k (n 5) vs losses 8.5k (n 10); ships: Svea 15 |

Examples: lof-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8143_g2_214598.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8154_g1_175939.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7928_g1_68248.html); lof-park-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7982_g1_197657.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8143_g2_214597.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8143_g2_214607.html)

#### Sea of Fortune

Figure: `figures/c4-sof.png`. Not found here: no selfish: cap sitter spot (no compact place holds 8 of the 47 such smokes on this map); no selfish: parked cruiser spot (no compact place holds 8 of the 45 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 24 such smokes on this map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| sof-long-1 | long-smoke | 4.5 km outside cap D, east side, east edge of the map (F9/F10) | Shared: 14% vs 14% (gap +0, -21 to +24) | 3 / 5 | Top 6: BONKZ 3 / Rest: BONKY 2, MZY 2, -BN- 1 | Top 6: inside Brisbane 3 / Rest: inside Des Moines 2, Brisbane 2; screened Des Moines 1 | 28.6k | 0 | 5:40 | small n; ships: Somers 4, Gearing 3, Harugumo 1 |
| sof-cell-1 | high-paying cell | 3.5 km outside cap D, own side (F9/G9) | Shared: 10% vs 8% (gap +3, -10 to +20) | 4 / 6 | Top 6: BONKZ 3, H-SR 1 / Rest: BONKY 2, MZY 2, -BN- 1, HFANS 1 | Top 6: inside Brisbane 3, Utrecht 1; screened Brisbane 1 / Rest: inside Des Moines 2, Brisbane 2, Utrecht 1; screened Des Moines 1 | 24.6k | 0 | 2:31 | small n; 24.6k vs 10.3k elsewhere on the map (gap +1.0k to +32.5k); median 14.1k; 6 clans, 5 games; cap taken 25% of 8; win/loss: 28.0k (n 8) vs 10.9k (n 2); too few on one side to compare |

Examples: sof-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7940_g1_183534.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7937_g1_44423.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8144_g2_39538.html); sof-cell-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7940_g1_183534.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7937_g1_44423.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7912_g1_85162.html)

#### Okinawa

Figure: `figures/c4-oki.png`. Not found here: no long-smoke spot (no compact place holds 8 of the 38 such smokes on this map); no selfish: cap sitter spot (no compact place holds 8 of the 40 such smokes on this map); no selfish: parked cruiser spot (no compact place holds 8 of the 26 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 16 such smokes on this map); no high-paying cell (of 4 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

No spot of any kind on this map.

---

## Part C: map-specific questions (C5), Round 5 text

Source: `part-c5/FINDINGS-C5.md`.


Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS; Rest = everyone else.

How to read this:
- Positions are team-normalized: own spawn at the bottom of the map (bottom left on Okinawa). West and east, and cells such as G1, are in that frame.
- "(a to b)" is a 95% interval made by resampling whole clans. A `*` means it excludes zero, so the gap is clear. "small n" = 8 to 14. Under 8 no rate is given.
- "Top 6 spot" = Top 6 use it clearly more than the Rest. "Shared spot" = no clear gap.
- Everything is association, not cause.
- "Enemy took the cap" comes from the round 5 library (`enemy_took`). It has been checked, but it misses roughly 15% of real flips, and nearly half of its "yes" answers fall in the 60 seconds after the smoke cleared. Read it as "during or just after the smoke".
- "At cap B" means inside the cap or within 2 km of its edge, unless a line says "nearest cap".
- Other ships' positions exist for one moment per smoke only (when it was fully laid), and for a median of 4 of the 9 allied ships. "None recorded" is not "none there".

Figures (working): `round5/figures/c5-sg-somers-east-west.png`, `c5-sg-harugumo-g1-second-dd.png`, `c5-hs-west-caps.png`, `c5-lp-first-smokes.png`, `c5-ok-death-zone.png`.

---

### Sleeping Giant

### C5-SG-1. Somers: Top 6 east, Rest west
**Answer:** Confirmed for the game as a whole: 17% of Top 6 Somers smokes are in the west half against 51% for the Rest. But it is not an opening choice. In the first 5 minutes both groups split evenly; the gap comes entirely from smokes after 5:00.

**Numbers:**

| Somers smokes | Top 6 in the west half | Rest in the west half | Gap (interval) |
|---|---|---|---|
| All (n 75) | 5 of 30 (17%) | 23 of 45 (51%) | -34 pts (-65 to -6 *) |
| First 5 minutes (n 23) | 4 of 8 (50%, small n) | 8 of 15 (53%) | -3 pts (-56 to +33) |
| After 5:00 (n 52) | 1 of 22 (4%) | 15 of 30 (50%) | -46 pts (-73 to -18 *) |

- East half: Top 6 25 of 30 (83%) vs Rest 22 of 45 (49%), +34 pts (+6 to +64 *).
- East half to draw: normalized x > 0, which is the rectangle u 0.5 to 1.0, v 0 to 1 in the 0-1 frame. The Top 6 smokes inside it sit in columns 8 to 10, rows E to J (u 0.74 to 0.99, v 0.40 to 0.95).
- Return is the same on both sides: east 14.0k concealed damage per smoke (10.9k to 16.5k, n 47), west 16.0k (11.5k to 19.4k, n 28). Deaths: east 10.6 per 100, west 14.3.
- Round 3 number reproduced exactly (17% vs 51%, -65 to -6).

**Top 6 or Shared:** Top 6 spot (east half, interval +6 to +64). Not for early smokes (interval -32 to +53 on the east share).

**Clans:** East: Top 6 RESIN 8, BONKZ 8, H-SR 8, VRTUS 1 | Rest HFANS 7, MACHX 5, EPOXY 4, BONKY 3, KITED 2, UYSC 1. West: Top 6 H-SR 3, RESIN 2 | Rest PFANS 8, REEEE 5, BONKY 4, MACHX 3, NGA 2, KITED 1. The Rest's west half rests on two clans (PFANS 8 of 8, REEEE 5 of 5); HFANS (7 of 7) and EPOXY (4 of 4) went east like the Top 6.

**Verdict:** Keep (reword: "after the opening, Top 6 Somers stay east").

### C5-SG-2. Harugumo at G1/F1: where is the second destroyer
**Answer:** A second destroyer has a recorded position in 7 of the 11 Top 6 smokes. In 3 it is up at cap A (cell F1, 2 to 3.4 km ahead of the smoke); in 2 it is inside the smoke itself (G1); in 2 it is far away to the east (G3/G4, 11 km off), both in smokes laid after 5:00.

**Numbers:** Spot reproduced: Top 6 11 of 24 Harugumo smokes vs Rest 1 of 9, +35 pts (+20 to +56 *). Second destroyers: Marceau 5, Chateaurenault 1, Ragnar 1. Forward of the smoke in 5 of 7; median 3.2 km from the smoke. In the 4 smokes with none recorded, at least one other allied destroyer was alive each time, and only 3 to 4 allied positions were recorded, so absence is not proof.

| Smoke | Clan | Time | Cell | Cruiser | Other destroyers alive | Second destroyer recorded (where) |
|---|---|---|---|---|---|---|
| [8147_g1_120797](https://seanr87.github.io/smoke-signals/smoke/smokes/8147_g1_120797.html) | RESIN | 2:23 | G1 | Petropavlovsk inside | Yueyang, Somers | none recorded |
| [8147_g1_120803](https://seanr87.github.io/smoke-signals/smoke/smokes/8147_g1_120803.html) | RESIN | 7:00 | F2 | none | Yueyang, Somers | none recorded |
| [8151_g1_29455](https://seanr87.github.io/smoke-signals/smoke/smokes/8151_g1_29455.html) | H-SR | 1:44 | F1 | Des Moines inside | Marceau, Somers, Marceau | Marceau in F1, 2.0 km from the smoke, 4.0 km forward, 0.2 km outside cap A |
| [8178_g1_166102](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g1_166102.html) | RESIN | 2:03 | G1 | Worcester inside | Ragnar, Gdansk, Chateaurenault | Chateaurenault in G1, inside the smoke |
| [8178_g1_166103](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g1_166103.html) | BONKZ | 2:47 | G1 | Worcester inside | Ragnar, Somers | Ragnar in F1, 3.4 km forward, 0.8 km inside cap A |
| [8178_g1_166106](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g1_166106.html) | BONKZ | 6:16 | F1 | Worcester inside | Somers | none recorded |
| [8183_g1_39283](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39283.html) | H-SR | 1:56 | G1 | Des Moines inside | Marceau, Somers | Marceau in F1, 3.2 km forward, 0.2 km inside cap A |
| [8183_g1_39284](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39284.html) | RESIN | 2:02 | G1 | Des Moines inside | Marceau, Somers, Gdansk | Marceau in G1, inside the smoke (1.0 km behind its centre) |
| [8183_g1_39285](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39285.html) | H-SR | 5:21 | F1 | Des Moines inside | Marceau, Somers | Marceau in G3, 11.7 km away to the east |
| [8183_g1_39286](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39286.html) | RESIN | 5:29 | G1 | Des Moines inside | Marceau, Somers, Gdansk | Marceau in G4, 11.0 km away, 4.3 km outside cap B |
| [8183_g1_39290](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39290.html) | H-SR | 8:46 | F1 | Des Moines inside | Marceau, Somers | none recorded |
| [8177_g1_176201](https://seanr87.github.io/smoke-signals/smoke/smokes/8177_g1_176201.html) (Rest) | EPOXY | 2:42 | F1 | Petropavlovsk inside | Somers, 20 de Julio | 20 de Julio in F5, 13.9 km away, at cap B |

**Top 6 or Shared:** Top 6 spot (+20 to +56).

**Clans:** Top 6 RESIN 5, H-SR 4, BONKZ 2 | Rest EPOXY 1. Five games.

**Could not be done / proxy:** One moment per smoke only. The opening picture (the 5 smokes before 3:00 with a destroyer recorded) is: destroyer at cap A in 3, inside the smoke in 2.

**Verdict:** Keep (small n).

### C5-SG-3. What smoke goes to cap B, and is it there to stop the enemy taking B
**Answer:** Mostly lone cap-sitter destroyers (Daring 15, Gdansk 6 of 34), tagged as cap contest. B was already ours at the start of fewer than half of them, and an enemy was already contesting it in only 2. So it is cap-holding and cap-contesting smoke, not a reaction to an attack on B; the enemy rarely took B during these smokes, but the same is true at the other caps.

**Numbers (inside or within 2 km of the cap edge; 119 of the map's 305 smokes):**

| Cap | Smokes | Top 6 | Ours / neutral / theirs at start | Enemy took it during or just after (of smokes where it was not theirs) | We took it (of not ours) | Batch "cap defended" | Concealed dmg | Deaths per 100 |
|---|---|---|---|---|---|---|---|---|
| A | 46 | 21 | 28 / 12 / 6 | 3 of 40 (8%) | 7 of 18 (39%) | 8 | 12.0k | 6.5 |
| B | 34 | 13 | 16 / 12 / 6 | 1 of 28 (4%) | 5 of 18 (28%) | 4 | 5.7k | 11.8 |
| C | 17 | 7 | 8 / 2 / 7 | 2 of 10 (20%, small n) | 4 of 9 (small n) | 4 | 12.9k | 29.4 |
| D | 22 | 5 | 18 / 0 / 4 | 0 of 18 (0%) | 0 of 4 (too few) | 0 | 7.0k | 13.6 |

- At B: 31 destroyer smokes, 3 cruiser. Habits: cap sitters 23, long smokes 5, other 6. Primary purpose: cap contest 26 of 34. No cruiser covered in 25. 10 are inside the cap. Median time 8:12.
- B ours at the start: 16 of 34 (47%, 27 to 72); other caps 64% (52 to 75). Of those 16: Daring 11; the enemy was already contesting B at the start in 2; the batch's "cap defended" flag (enemy invading a cap we own while the smoke stood) fired on 2; the enemy took B in 1.
- B not ours at the start: 18; we took it during or just after 5.
- Enemy took B: 1 of 28 (4%) vs 5 of 68 (7%) at the other caps; difference -4 pts (-13 to +9). Not clear.
- Lowest return of the four caps: 5.7k per smoke.
- With the looser "nearest cap is B, any distance" rule: 59 smokes, ours 25 / neutral 21 / theirs 13, enemy took 4 of 46 (9%).

**Top 6 or Shared:** Shared spot. Share of all map smokes: Top 6 13 of 137 (10%) vs Rest 21 of 168 (12%), -3 pts (-12 to +7). Top 6 smoke B more often when it is already theirs (8 of 13 vs 8 of 21), not clear (-25 to +65).

**Clans:** Top 6 VRTUS 4, RESIN 4, HTDOG 3, BONKZ 2 | Rest HFANS 7, KITED 4, 5D 3, KSE 3, EPOXY 1, INCA 1, BONKY 1, -BN- 1. With B ours: Top 6 VRTUS 4, HTDOG 3, BONKZ 1 | Rest HFANS 3, KSE 1, BONKY 1, KITED 1, -BN- 1, 5D 1.

**Could not be done / proxy:** The data cannot tell "the smoke stopped the enemy" from "the enemy never came". The closest signs of a real attack are the contested flag at the start (2 of 16) and the batch "cap defended" flag (2 of 16).

**Verdict:** Drop the reading "there to stop the enemy taking B" (C1). Keep as: low-paying shared cap-sitter spot.

---

### Hotspot

### C5-HS-1. West caps A and B: 36% vs 14%
**Answer:** Confirmed: 36% of Top 6 destroyer smokes have A or B as their nearest cap against 14% for the Rest, and all six Top 6 clans do it. Two cautions: it is a west-side habit more than smoke in the caps (within 2 km of A or B the gap is not clear), and it happens after 5:00, not in the opening.

**Numbers (destroyer smokes, 80 Top 6, 155 Rest):**

| Nearest cap | Top 6 | Rest | Gap (interval) |
|---|---|---|---|
| A | 11 (14%) | 3 (2%) | +12 pts (+6 to +16 *) |
| B | 18 (22%) | 18 (12%) | +11 pts (+2 to +22 *) |
| A or B | 29 (36%) | 21 (14%) | +23 pts (+14 to +35 *) |
| C | 23 (29%) | 54 (35%) | -6 pts (-23 to +10) |
| D | 28 (35%) | 80 (52%) | -17 pts (-32 to -4 *) |

- Inside or within 2 km of A or B: Top 6 14 of 80 (18%) vs Rest 14 of 155 (9%), +8 pts (-5 to +24). Not clear. The 50 west smokes sit a median 1.8 km outside the cap edge.
- By time: first 5 minutes 3 of 23 vs 2 of 45 (+9, -7 to +38); after 5:00 26 of 57 (46%) vs 19 of 110 (17%), +28 pts (+20 to +38 *).
- Team-games with at least one destroyer smoke at A or B: Top 6 13 of 18, Rest 14 of 44.
- Without any one Top 6 clan the Top 6 share stays 33% to 39%.
- Return: A 19.7k per smoke (10.4k to 30.4k; n 14, small n), B 15.6k (8.8k to 23.9k; n 36). Within B the Rest returned more (20.8k vs 10.5k), so this is where Top 6 go, not proof that it pays them more.
- All classes (cruiser smokes added): 33% vs 22%, +11 pts (+4 to +24 *). The Rest's west smoke is largely cruiser smoke at B.

**Top 6 or Shared:** Top 6 spot for both A (+6 to +16) and B (+2 to +22), on the nearest-cap rule.

**Clans (destroyer smokes):** A or B: Top 6 H-SR 9, RESIN 6, VRTUS 5, BONKZ 5, HTDOG 2, KITE 2 | Rest HFANS 5, KSC 4, MANBA 2, EPOXY 2, INCA 2, BONKY 2, KSE 1, MACH 1, MACHX 1, MZY 1. A alone: Top 6 H-SR 4, BONKZ 3, VRTUS 2, RESIN 2 | Rest MACH 1, KSC 1, HFANS 1. B alone: Top 6 H-SR 5, RESIN 4, VRTUS 3, HTDOG 2, KITE 2, BONKZ 2 | Rest HFANS 4, KSC 3, MANBA 2, EPOXY 2, INCA 2, BONKY 2, KSE 1, MACHX 1, MZY 1. Six of 6 Top 6 clans; 10 of 24 Rest clans.

**Verdict:** Lead (say "west side, after the opening").

### C5-HS-2. Opener at G10: radar cruiser inside
**Answer:** The 87% vs 38% is for all early destroyer smokes on Hotspot, not G10 alone; it reproduces and is the biggest gap of any map. In the G10 cluster itself it is 83% vs 46%. Both groups use the G10 place equally; what differs is whether the radar cruiser is inside the smoke.

**Numbers (destroyer smokes in the first 5 minutes; 68 on the map):**

| Radar cruiser inside the smoke | Top 6 | Rest | Gap (interval) |
|---|---|---|---|
| Whole map | 20 of 23 (87%) | 17 of 45 (38%) | +49 pts (+31 to +71 *) |
| G10 cluster (36 smokes) | 10 of 12 (83%, small n) | 11 of 24 (46%) | +38 pts (+6 to +63 *) |
| G5 cluster, short of C (27 smokes) | 7 of 8 (88%, small n) | 5 of 19 (26%) | +61 pts (+28 to +91 *) |

- Use of G10: Top 6 12 of 23 early smokes (52%) vs Rest 24 of 45 (53%), -1 pt (-25 to +20).
- Round 5 definition, whole map: cruiser inside 87% vs 44% (+42, +25 to +65 *); cruiser screened only 9% vs 24% (-16, -34 to -1 *); no cruiser covered 4% vs 31% (-27, -45 to -10 *). In G10: inside 10 of 12 vs 13 of 24 (+29, +2 to +60 *); screened 2 of 12 vs 6 of 24.
- Other maps, radar cruiser inside early smokes: Sea of Fortune +39 (+12 to +62 *), Mountain Range +32 (-8 to +72), Loop +23, Land of Fire +10, Sleeping Giant -13 (none clear). Okinawa has only 3 Top 6 early smokes (too few).
- G10 smokers: Somers 16, Gearing 7, Harugumo 5, Shimakaze 3, Daring 3, Grozovoi 2. Cruisers inside: Top 6 Brisbane 4, Des Moines 4, Worcester 2; Rest Brisbane 5, Des Moines 4, Utrecht 3, Minotaur 1, Stalingrad 1.
- G10 return: 16.5k per smoke (Top 6 17.8k, Rest 15.9k).
- The atlas counts (36 at G10, 27 at G5) reproduce exactly.

**Top 6 or Shared:** Shared spot (the place). The radar cruiser inside it is the Top 6 habit.

**Clans (G10 cluster):** Top 6 H-SR 5, BONKZ 3, RESIN 2, HTDOG 1, KITE 1 | Rest REEEE 4, MZY 3, 5D 2, KSC 2, HFANS 2, KITED 2, and 1 each BTLST, RMN, PN, MACH, -BN-, NGA, BONKY, PFANS, EPOXY. Radar cruiser inside by clan: H-SR 4 of 5, BONKZ 3 of 3, RESIN 1 of 2, HTDOG 1 of 1, KITE 1 of 1; Rest clans without one: REEEE 3 of 4, 5D 2 of 2, MZY 2 of 3, KITED 2 of 2.

**Verdict:** Lead.

### C5-HS-3. Rim of C: which cruisers
**Answer:** Top 6 long smokes on the own-side rim of C almost always hold a radar cruiser (12 of 13): Moskva 5, Brisbane 4, Petropavlovsk 2. The Rest have 7 smokes there (too few for a rate): Des Moines 2, Brisbane 1, Minotaur 1 inside, Brisbane screened in 2, no cruiser in 1.

**Numbers:** Long smokes (Somers, Gearing, Harugumo, Delny) in the spot: Top 6 13 of 64 (20%) vs Rest 7 of 80 (9%), +12 pts (-7 to +27). Reproduces the round 4 lead.

| | Top 6 (13 smokes) | Rest (7 smokes) |
|---|---|---|
| Smoker | Somers 8, Gearing 4, Delny 1 | Somers 5, Gearing 2 |
| Cruiser inside | Moskva 5, Brisbane 4, Petropavlovsk 2, Utrecht 1, Minotaur 1 | Des Moines 2, Brisbane 1, Minotaur 1 |
| Cruiser screened | Worcester 1, Moskva 1 | Brisbane 2 |
| Smokes with a cruiser inside | 12 | 4 |
| Concealed dmg per smoke | 17.3k | 13.7k (too few) |

Each Top 6 clan brings its own cruiser: RESIN Moskva (5 inside, 1 screened) and Petropavlovsk 1; BONKZ Brisbane 4; H-SR Petropavlovsk 1 and Utrecht with Minotaur 1. Without RESIN the Top 6 share is 6 of 49 (12%).

**Top 6 or Shared:** Shared spot (interval -7 to +27).

**Clans:** Top 6 RESIN 7, BONKZ 4, H-SR 2 | Rest -BN- 4, INCA 1, KSC 1, MZY 1.

**Verdict:** Keep as a shared spot; drop as a Top 6 lead.

---

### Loop

### C5-LP-1. Early smoke rate per team-game against other maps
**Answer:** Loop has the fewest early smokes of any map: 0.70 early destroyer smokes per team-game against 0.91 on the other maps, and 0.43 early cruiser smokes against 0.69. The shortfall is in smokes with a cruiser inside. Top 6 and Rest are the same on Loop.

**Numbers (first 5 minutes; per team-game):**

| Map | Team-games (Top 6 / Rest) | Early destroyer smokes: all (interval) | Top 6 | Rest | Gap (interval) | Early cruiser smokes: all (interval) | Top 6 | Rest | Gap (interval) | Cruiser inside | Cruiser screened |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | 64 (27 / 37) | 1.08 (0.83 to 1.28) | 1.19 | 1.00 | +0.19 (-0.23 to +0.64) | 0.91 (0.70 to 1.10) | 1.04 | 0.81 | +0.23 (-0.14 to +0.65) | 0.69 | 0.22 |
| Hotspot | 62 (18 / 44) | 1.10 (0.89 to 1.28) | 1.28 | 1.02 | +0.26 (-0.10 to +0.65) | 0.85 (0.64 to 1.08) | 1.22 | 0.70 | +0.52 (+0.19 to +0.83 *) | 0.65 | 0.21 |
| Mountain Range | 42 (16 / 26) | 0.93 (0.63 to 1.24) | 0.88 | 0.96 | -0.09 (-0.70 to +0.52) | 0.67 (0.41 to 0.93) | 0.62 | 0.69 | -0.07 (-0.60 to +0.55) | 0.48 | 0.19 |
| Land of Fire | 50 (16 / 34) | 0.74 (0.53 to 0.95) | 0.75 | 0.74 | +0.01 (-0.38 to +0.62) | 0.50 (0.32 to 0.67) | 0.50 | 0.50 | 0.00 (-0.30 to +0.37) | 0.34 | 0.16 |
| Sea of Fortune | 42 (14 / 28) | 0.74 (0.51 to 0.96) | 0.64 | 0.79 | -0.14 (-0.66 to +0.35) | 0.57 (0.40 to 0.72) | 0.57 | 0.57 | 0.00 (-0.40 to +0.37) | 0.36 | 0.21 |
| **Loop** | 46 (13 / 33) | 0.70 (0.48 to 0.94) | 0.69 | 0.70 | 0.00 (-0.58 to +0.45) | 0.43 (0.25 to 0.63) | 0.46 | 0.42 | +0.04 (-0.40 to +0.40) | 0.22 | 0.22 |
| Okinawa | 36 (6 / 30) | 0.72 (0.50 to 1.00) | 0.50 | 0.77 | -0.27 (-0.76 to +0.19) | 0.44 (0.26 to 0.65) | 0.33 | 0.47 | -0.13 (-0.54 to +0.33) | 0.17 | 0.28 |

"Early cruiser smoke" = a destroyer smoke in the first 5 minutes covering a cruiser, inside or screened.
- Loop minus the other six maps: early destroyer smokes -0.22 (-0.41 to -0.02 *); early cruiser smokes -0.25 (-0.42 to -0.09 *); cruiser inside -0.26 (-0.38 to -0.13 *); cruiser screened +0.01 (-0.11 to +0.16).
- 21 of 46 Loop team-games (46%) had no early destroyer smoke; other maps 99 of 296 (33%).
- Part of this is line-ups: long-smoke ships fill 19% of destroyer slots on Loop against 28% elsewhere.

**Top 6 or Shared:** Shared (0.69 vs 0.70; interval -0.58 to +0.45).

**Clans (Loop early cruiser smokes, n 20):** Top 6 RESIN 3, H-SR 2, BONKZ 1 | Rest MACHX 2, -BN- 2, EPOXY 2, and 1 each 5D, KSC, UYSC, KM, INCA, NGA, MZY, HFANS.

**Verdict:** Keep.

### C5-LP-2. Spread of opening positions
**Answer:** Loop openings are not more scattered than on other maps. What sets Loop apart is that the first smoke is the latest of any map and no single cell dominates.

**Numbers (first smoke of each team-game, any ship):**

| Map | Team-games with a smoke | Mean distance from the map's average first-smoke position (interval) | Share of map width | Same, within the west and east halves | Cells holding 80% (of cells used) | Most used cell | Median time | Before 5:00 |
|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | 60 | 11.1 km (8.2 to 12.8) | 26% | 4.6 km | 10 of 19 | G1 (22%) | 2:41 | 87% |
| Hotspot | 62 | 10.7 km (8.2 to 12.3) | 22% | 7.1 km | 7 of 15 | G10 (18%) | 2:37 | 81% |
| Mountain Range | 41 | 10.7 km (8.0 to 13.2) | 22% | 5.9 km | 11 of 19 | G7 (15%) | 3:05 | 78% |
| Land of Fire | 45 | 9.7 km (7.6 to 11.2) | 20% | 7.1 km | 13 of 22 | F5 (18%) | 3:14 | 73% |
| Sea of Fortune | 39 | 15.7 km (13.5 to 16.5) | 33% | 4.4 km | 10 of 17 | F2 (15%) | 3:49 | 82% |
| **Loop** | 41 | 10.0 km (8.1 to 11.3) | 21% | 5.2 km | 11 of 18 | F4 (15%) | 4:14 | 68% |
| Okinawa | 35 | 12.5 km (10.5 to 13.9) | 30% | 7.8 km | 12 of 19 | D1 (11%) | 3:24 | 77% |

Loop first smokes by nearest cap: A 18, B 18, C 5. Top 6 6 / 5 / 1; Rest 12 / 13 / 4. No clear gap at any cap (A: +9 pts, -30 to +41).

**Top 6 or Shared:** Shared. Spread Top 6 9.9 km vs Rest 9.9 km (difference -4.4 to +2.1).

**Clans:** see C5-LP-3.

**Verdict:** Keep (as "late and with no fixed address", not "spread out").

### C5-LP-3. First smoker by ship
**Answer:** On Loop the first smoke comes from a cap sitter more often than from a long-smoke ship: Daring 7, Gearing 5, Somers 5, Gdansk 4, Napoli 4, Shimakaze 3 of 41. Long-smoke ships lay 32% of first smokes on Loop against 55% on the other maps.

**Numbers:**

| Map | First smokes | First smoker, all | Top 6 | Rest | Long-smoke ships | Cap sitters | Cruisers |
|---|---|---|---|---|---|---|---|
| Sleeping Giant | 60 | Somers 15, Gearing 13, Harugumo 11, Z-42 4, Napoli 4, Gdansk 3 | Harugumo 7, Gearing 5, Somers 5, Gdansk 3 | Somers 10, Gearing 8, Harugumo 4, Z-42 3 | 65% | 20% | 13% |
| Hotspot | 62 | Somers 22, Gearing 11, Harugumo 6, Daring 6, Gdansk 5, Shimakaze 4 | Somers 7, Gearing 4, Harugumo 3, Delny 1 | Somers 15, Gearing 7, Daring 6, Gdansk 4 | 65% | 29% | 5% |
| Mountain Range | 41 | Gearing 12, Somers 9, Svea 6, Gdansk 5, Napoli 5 | Svea 4, Gearing 4, Somers 4, Gdansk 2 | Gearing 8, Napoli 5, Somers 5, Gdansk 3 | 54% | 15% | 29% |
| Land of Fire | 45 | Somers 10, Gearing 9, Svea 5, Gdansk 3, Z-42 3, Harugumo 3 | Gearing 3, Z-52 2, Delny 2, Svea 2 | Somers 9, Gearing 6, Svea 3, Venezia 2 | 53% | 18% | 18% |
| Sea of Fortune | 39 | Napoli 7, Somers 7, Gearing 5, Svea 4, Harugumo 4, Jinan 2 | Svea 2, Gearing 2, Harugumo 2, Cerberus 1 | Somers 7, Napoli 6, Gearing 3, Svea 2 | 46% | 8% | 38% |
| **Loop** | 41 | Daring 7, Gearing 5, Somers 5, Gdansk 4, Napoli 4, Shimakaze 3 | Gdansk 3, Somers 2, Svea 2, Shimakaze 1 | Daring 6, Gearing 4, Napoli 4, Somers 3 | 32% | 39% | 20% |
| Okinawa | 35 | Gearing 6, Daring 5, Napoli 4, Svea 4, Harugumo 4, Somers 3 | Gearing 2, Svea 1, Somers 1, Smolensk 1 | Daring 5, Napoli 4, Gearing 4, Harugumo 4 | 37% | 29% | 31% |

Long-smoke share of first smokes, Loop minus the other maps: -24 pts (-38 to -7 *).

**Top 6 or Shared:** Not a spot. Top 6 has 12 first smokes on Loop: too few per ship to compare.

**Clans (Loop, by first smoker):** Daring 7: KITE 1 | KITED 2, BONKY 1, SCCC2 1, EPOXY 1, HFANS 1 (cells F4 3, G3 2). Gearing 5: BONKZ 1 | KSC, BTLST, 5D, OGF 1 each. Somers 5: RESIN 2 | EPOXY, MACHX, MZY 1 each (median 1:30). Gdansk 4: H-SR, BONKZ, RESIN 1 each | KSE 1. Napoli 4: Rest only (REEEE 2, MACHX 1, MANBA 1). Shimakaze 3: VRTUS 1 | UYSC 1, RMN 1. Svea 2: HTDOG 2.

**Verdict:** Keep.

### C5-LP-4. Test: did Daring smokes follow a friendly radar lighting an enemy destroyer

> **Superseded in Round 5b.** Redone with the full radar log: see "C5-LP-4 (Round 5b)". The Round 5 text is kept below for reference.

**Answer:** Not supported. Of 48 Daring smokes on Loop, one came within 60 seconds after a friendly radar lit an enemy ship that we can see in the data, and none followed an allied radar-from-smoke. Daring smokes on Loop are laid with less radar nearby than Daring smokes elsewhere, not more.

**What the batch records about friendly radar:** Radar activations outside smoke are not exported (the pipeline reads them but writes out only radar run from inside a smoke). There is no timeline of which enemy ships were detected. Three things exist:
1. Radar run from inside one of our own smokes (no time stamp, only the life of that smoke).
2. Each time an enemy ship sitting in its own team's smoke was lit by radar, with the time and the likely radar ship, wherever that radar ship was. This is the only time-stamped record of our radar lighting an enemy. The whole batch has 191 such rows, 77 on destroyers; Loop has 17, 9 on destroyers.
3. Positions at the one moment each smoke was fully laid.

**Numbers (proxy, 60-second window before the smoke was activated):**

| Group | Smokes | Our radar lit an enemy destroyer in its smoke, 60 s before | Same, 120 to 60 s before (control) | Same, 60 s after (control) | An allied smoke with radar run from inside stood in the 60 s before | An allied radar ship within radar range of the cap centre when the smoke was laid | Within radar range of the nearest enemy destroyer with a known position |
|---|---|---|---|---|---|---|---|
| Daring on Loop | 48 | 1 (2%, 0 to 8) | 1 (2%) | 0 | 0 (0%) | 18 (38%, 17 to 56) | 8 of 38 (21%) |
| Daring on other maps | 152 | 7 (5%, 2 to 8) | 4 (3%) | 6 (4%) | 15 (10%, 2 to 19) | 110 (72%, 63 to 79) | 57 of 123 (46%) |
| Other cap sitters on Loop | 40 | 0 | 0 | 0 | 2 (5%, 0 to 12) | 28 (70%, 56 to 84) | 16 of 37 (43%) |
| Other destroyer smokes on Loop | 54 | 0 | 0 | 1 (2%) | 4 (7%, 0 to 17) | 34 (63%, 50 to 77) | 14 of 43 (33%) |
| All destroyer smokes, all maps | 1,074 | 24 (2%, 1 to 3) | 17 (2%) | 23 (2%) | 119 (11%, 7 to 15) | 728 (68%, 63 to 72) | 353 of 873 (40%) |

- Radar ship in range of the cap: Daring on Loop minus Daring on other maps -35 pts (-55 to -15 *); minus other cap sitters on Loop -32 pts (-56 to -11 *).
- Before against the control windows, Daring on Loop: 0 pts (-5 to +7) and +2 pts (0 to +8). No rise before the smoke.
- The one case: [BONKY Daring, 17:51, F3](https://seanr87.github.io/smoke-signals/smoke/smokes/7919_g1_94407.html), 49 seconds after a Moskva lit an A. da Barbiano (a cruiser, not a destroyer) in its smoke.
- The other way round: our radar lit an enemy destroyer in its smoke 9 times on Loop; a Daring of that team was alive for 2 of them and smoked within 60 seconds once.
- Why: 41 of the 48 Daring smokes are at cap A, away from where the radar cruisers sit; 16 have no allied radar ship position recorded at all.

**Top 6 or Shared:** Not a spot. 45 of the 48 smokes are Rest.

**Clans:** Top 6 KITE 3 | Rest REEEE 11, KITED 9, EPOXY 6, MACHX 3, -BN- 3, BONKY 3, SCCC2 3, HFANS 3, KSC 2, NGA 2.

**Could not be done / proxy:** This is a proxy and a thin one. A radar that lit an enemy destroyer in open water leaves no trace in the batch, so the test can miss real cases. To test it properly the batch would need to export every radar activation with its time and the enemies it lit.

**Verdict:** Drop.

### C5-LP-5. Long smokes at F8 and F10
**Answer:** Both cells are shared and both pay well above the map average, on small counts. F8: 4 Top 6 and 4 Rest long smokes. F10: 1 Top 6 and 6 Rest.

**Numbers (long smokes = Somers, Gearing, Harugumo, Delny; 18 Top 6 and 27 Rest on Loop):**

| Cell | Top 6 | Rest | Gap (interval) | Concealed dmg per long smoke | All destroyer smokes in the cell |
|---|---|---|---|---|---|
| F8 | 4 of 18 (22%) | 4 of 27 (15%) | +7 pts (-28 to +82) | 27.5k, median 17.9k (n 8, small n) | 18.3k (n 15; Top 6 7, Rest 8) |
| F10 | 1 of 18 (6%) | 6 of 27 (22%) | -17 pts (-34 to +2) | n 7, too few | 20.7k (n 9, small n; Top 6 2, Rest 7) |
| F8 or F10 | 5 of 18 (28%) | 10 of 27 (37%) | -9 pts (-41 to +50) | 26.9k, median 27.9k (n 15) | 19.2k (n 24) |

Map average for destroyer smokes: 8.0k. The cell figures (18.3k, 20.7k) reproduce the atlas. F8 rests on a few big smokes: RESIN Somers 67k, BONKZ Gearing 52k and 64k (one game). Cruisers inside: F8 Brisbane 3, Des Moines 2; F10 Minotaur 2, Des Moines 1, Petropavlovsk 1, Prins van Oranje 1. Deaths in the 15 long smokes: 4 (3 in F10).

**Top 6 or Shared:** Shared (both cells; intervals cross zero).

**Clans (long smokes):** F8: Top 6 BONKZ 3, RESIN 1 | Rest HFANS 2, OGF 1, MZY 1. F10: Top 6 H-SR 1 | Rest EPOXY 2, MZY 2, 5D 1, KM 1.

**Verdict:** Keep as shared high cells (small n).

### C5-LP-6. Cap-sitter spot on B: clan counts
**Answer:** Reproduced: 15 of 23 Top 6 cap-sitter smokes are on the own side and east half of B against 13 of 65 for the Rest. Most of the gap is ship choice: the Rest's cap sitter on Loop is the Daring, which sits at cap A.

**Numbers:** Top 6 15 of 23 (65%) vs Rest 13 of 65 (20%), +45 pts (+25 to +72 *). Ships in the spot: Top 6 Gdansk 9, Shimakaze 3, Z-42 2, Daring 1; Rest Z-42 7, Grozovoi 3, Daring 2, Shimakaze 1. Leaving the Daring out: Top 6 14 of 20 (70%) vs Rest 11 of 20 (55%), +15 pts (-21 to +57), not clear. Return in the spot: Top 6 5.8k per smoke; Rest 1.2k (small n). We took B during or just after: Top 6 5 of 10, Rest 1 of 8 (small n).

**Top 6 or Shared:** Top 6 spot by the interval rule (+25 to +72), with the ship-choice caution above.

**Clans:** Top 6 RESIN 4, KITE 3, BONKZ 3, H-SR 2, HTDOG 2, VRTUS 1 | Rest REEEE 6, MACHX 2, SCCC2 2, RMN 1, MACH 1, EPOXY 1.

**Verdict:** Keep.

---

### Mountain Range

### C5-MR-1. Far-west Svea / Jinan area: clan counts per ship
**Answer:** It is two clans and two ships: HTDOG with the Jinan (8 smokes) and BONKZ with the Svea (4), in 4 games. No Rest clan parked a cruiser smoke there.

**Numbers:** Parked cruiser smokes in the spot: Top 6 12 of 33 (36%) vs Rest 0 of 13, +36 pts (+31 to +40 *). Reproduces round 4. Svea alone: Top 6 4 of 24 (17%) vs Rest 0 of 13, +17 pts (0 to +31), touching zero. The Jinan was fielded only by HTDOG (3 team-games), so the Jinan part cannot be compared. Cells H1 6, G1 4, H2 2. Return 19.0k per smoke (median 14.3k), 1 death; all 12 are solo smokes; median time 8:10. Any ship in the same ellipse: Top 6 17 of 88 smokes (19%) vs Rest 9 of 119 (8%), +12 pts (-4 to +26).

**Top 6 or Shared:** Top 6 spot by the rule (+31 to +40), but it is two clans in four games and partly ship choice.

**Clans:** Jinan: HTDOG 8. Svea: BONKZ 4. Rest: none. Rest clans with Svea smokes elsewhere on the map: INCA 6, MACHX 6, PN 1.

**Verdict:** Keep (name the two clans; not a lead).

### C5-MR-2. Radar from smoke at B: did the enemy take B during those smokes
**Answer:** Often, yes. The enemy took B during or just after 5 of 13 radar smokes at B, and after 4 of the 8 laid when B was ours. That is no better than ordinary smokes at B, and worse than radar smokes on other maps. B is simply the cap that changes hands most on this map. Small n throughout.

**Numbers:**

| Smokes | n | Top 6 | B ours / neutral / theirs at start | Enemy took B during or just after | Enemy took B when ours | We took B (of not ours) | Batch "cap defended" on B |
|---|---|---|---|---|---|---|---|
| Radar smokes, nearest cap B | 15 | 12 | 8 / 5 / 2 | 5 of 13 (38%, small n) | 4 of 8 (50%, small n) | 3 of 7 (too few) | 4 |
| Other smokes, nearest cap B | 53 | 23 | 15 / 17 / 21 | 11 of 32 (34%) | 5 of 15 (33%) | 17 of 38 (45%) | 4 |
| Radar smokes inside or within 2 km of B | 7 | 5 | 4 / 2 / 1 | 2 of 6 (too few) | 1 of 4 (too few) | 1 of 3 (too few) | 1 |
| Other smokes inside or within 2 km of B | 24 | 11 | 7 / 8 / 9 | 4 of 15 (27%) | 2 of 7 (too few) | 11 of 17 (65%) | 2 |
| Radar smokes, other maps (nearest cap) | 112 | 61 | 52 / 35 / 25 | 16 of 87 (18%) | 7 of 52 (13%) | 23 of 60 (38%) | 14 |

- "Radar smoke" = primary purpose cap control or radar trap, or radar activated from inside. On this map the two tests pick the same 15 smokes.
- The radar smokes sit a median 2.0 km outside the B edge (radar reaches the cap from there), so the 2 km rule keeps only 7. Both rows are shown.
- Whole map, enemy took the nearest cap during the smoke: A 6 of 41 (15%), B 16 of 45 (36%), C 10 of 56 (18%).
- B was ours at the start of 53% of radar smokes (25 to 73) against 28% of other smokes at B (14 to 43): radar smokes are more often laid on a held cap, so part of this is defence in intent.
- The 4 "ours, then lost" cases come from 3 games: BONKZ Svea twice (16:02 and 17:14, same game), H-SR Harugumo 13:58, KITE Gearing 10:42. All late.
- Ships: Gearing 4, Svea 4, Somers 3, Gdansk 3, Harugumo 1. The radar spotted at least one enemy in 11 of 15. Return 12.8k per smoke, 1 death.
- The atlas's "10 plays" counts destroyer plays whose batch-contested cap is B (reproduced: 10, Top 6 7, cap taken 1 of 6). The 15 here adds 4 Svea smokes and uses the nearest cap.

**Top 6 or Shared:** Top 6 spot. Radar smokes at B are 12 of 88 Top 6 smokes on the map (14%) vs 3 of 119 Rest (2%), +11 pts (+2 to +22 *). Of smokes at B, radar smokes are 12 of 35 vs 3 of 33 (+25, +6 to +40 *).

**Clans:** Top 6 KITE 4, BONKZ 4, H-SR 2, RESIN 2 | Rest HFANS 2, SCCC2 1.

**Verdict:** Keep the spot; Drop "radar from smoke defends B" (not supported: B was lost after half of the ones laid on a held cap, small n).

---

### Land of Fire

### C5-LF-1. Early cluster at cap A: ship breakdown
**Answer:** 13 early destroyer smokes short of cap A (F3), 5 Top 6 and 8 Rest. They are Gearing and Somers smokes for a cruiser: inside in 9, screened in 2, none in 2. Top 6 bring Des Moines inside; the Rest bring a mix and screen a Napoli three times.

**Numbers:** Share of early destroyer smokes in the cluster: Top 6 5 of 12 (42%) vs Rest 8 of 25 (32%), +10 pts (-18 to +39). Atlas count (13, Top 6 5) reproduced.

| | Top 6 (5, too few for rates) | Rest (8, small n) |
|---|---|---|
| Smoker | Gearing 2, Somers 1, Gdansk 1, Harugumo 1 | Gearing 4, Somers 3, Daring 1 |
| Cruiser inside | Des Moines 3, Brisbane 1 | Des Moines 2, Brisbane 1, Napoli 1, Svea 1 |
| Cruiser screened | none | Napoli 3, Smolensk 1, San Martin 1 |
| Smokes: inside / screened / no cruiser | 4 / 0 / 1 | 5 / 2 / 1 |
| Concealed dmg per smoke | 9.7k | 7.9k |
| Deaths | 0 | 2 |

Wider view, all early destroyer smokes whose nearest cap is A (19): Gearing 8, Somers 8, Daring 1, Gdansk 1, Harugumo 1; cruisers inside Des Moines 5, Utrecht 2, Brisbane 2, Napoli 1, Minotaur 1, Svea 1; inside 12, screened 3, no cruiser 4. Top 6 6 of 12 vs Rest 13 of 25 (-2 pts, -34 to +28).

**Top 6 or Shared:** Shared spot (-18 to +39).

**Clans:** Top 6 HTDOG 2, VRTUS 1, H-SR 1, RESIN 1 | Rest HFANS 3, BTLST 2, NGA 1, SCCC2 1, MACHX 1.

**Verdict:** Keep (small n).

### C5-LF-2. Svea at F5: clan counts
**Answer:** Reproduced: 14 of 19 Top 6 Svea smokes are on the own-side rim of B against 4 of 21 for the Rest. Three Top 6 clans, led by VRTUS; the Rest's 4 are all one clan.

**Numbers:** Top 6 14 of 19 (74%) vs Rest 4 of 21 (19%), +55 pts (+7 to +87 *). Without VRTUS the Top 6 share is 6 of 10. Six games; median time 6:16; Top 6 smokes there returned 14.2k each; 1 death in 18.

**Top 6 or Shared:** Top 6 spot (+7 to +87).

**Clans:** Top 6 VRTUS 8 (of 9 Svea smokes on the map), HTDOG 4 (of 5), RESIN 2 (of 5) | Rest BONKY 4 (of 4). Rest clans whose Svea never smoked there: -BN- 0 of 5, KSC 0 of 4, HFANS 0 of 4, EPOXY 0 of 3, RMN 0 of 1.

**Verdict:** Keep.

---

### Sea of Fortune

### C5-SF-1. Early cruiser smoke at the west cap and at D; which letter is the west cap
**Answer:** The west cluster is at cap B: the own-side west cap, bottom left as drawn (u 0.20, v 0.65). The atlas label was right. The confusion is that for teams spawning north the game calls that same cap A, so 8 of the 14 smoke pages say A. Early cruiser smoke goes to B (15 smokes) and short of D (7); none to the far west cap A.

**Numbers:**
- Caps in the 0-1 frame: A u 0.20 v 0.35 (far west), B u 0.20 v 0.65 (own-side west), C u 0.44 v 0.50, D u 0.76 v 0.50. Radius 0.083 for A and B, 0.062 for C and D.
- West cluster (14 early destroyer smokes, reproduces the atlas): all 14 have drawn-B as nearest cap; median 0.5 km outside the B edge and 7.7 km from the A edge. Game letter: A for 8 (north spawn), B for 6 (south spawn).
- Early cruiser smokes on the map (destroyer smoke in the first 5 minutes covering a cruiser): 24 of 31 early destroyer smokes.

| Nearest cap | Early cruiser smokes | Top 6 | Rest | Share of the group's early cruiser smokes: gap (interval) | Cruiser inside | Cruiser screened | Concealed dmg |
|---|---|---|---|---|---|---|---|
| B (own-side west) | 15 | 5 of 8 (62%) | 10 of 16 (62%) | 0 pts (-29 to +28) | 10 | 5 | 18.5k |
| D (east) | 7 (too few) | 3 of 8 | 4 of 16 | +12 pts (-16 to +40) | 5 | 2 | too few |
| C (centre) | 2 | 0 | 2 | | 0 | 2 | |
| A (far west) | 0 | 0 | 0 | | | | |

- At B, 12 of the 15 are inside or within 2 km of the cap; the D smokes sit 1.5 to 4.6 km short of it.
- B, smokers: Somers 6, Gearing 5, Harugumo, Shimakaze, Daring, Delny 1 each. Cruisers inside: Top 6 Brisbane 2, Utrecht 1, Worcester 1; Rest Salem, Minotaur, Svea, Utrecht, Worcester, Cerberus 1 each. Screened: Top 6 Brisbane 1, Stalingrad 1; Rest Puerto Rico 2, Napoli 2, Des Moines, Utrecht, Petropavlovsk, Prins van Oranje, Minotaur 1 each.
- D, smokers: Harugumo 3, Somers 2, Gearing 1, Delny 1. Cruisers inside: Top 6 Brisbane 2, Utrecht 1, Worcester 1; Rest Des Moines 1, Utrecht 1, Brisbane 1. Screened: Rest Des Moines 1, Moskva 1.

**Top 6 or Shared:** Shared, both places.

**Clans:** B: Top 6 H-SR 2, VRTUS 1, BONKZ 1, RESIN 1 | Rest 1 each RMN, REEEE, PN, RSR, KSC, INCA, KM, HFANS, SCCC2, MZY. D: Top 6 H-SR 1, BONKZ 1, RESIN 1 | Rest MZY 2, -BN- 1, BONKY 1.

**Verdict:** Keep (label the west spot "cap B, own-side west cap").

### C5-SF-2. Long smokes at D, whole game
**Answer:** Shared. 36% of Top 6 long smokes and 32% of Rest long smokes have D as nearest cap. They returned 17.7k each with no deaths in 20.

**Numbers:** Long smokes on the map: 22 Top 6, 37 Rest.

| Nearest cap | Top 6 | Rest | Gap (interval) | Concealed dmg per smoke | Deaths per 100 |
|---|---|---|---|---|---|
| D | 8 (36%) | 12 (32%) | +4 pts (-23 to +33) | 17.7k (Top 6 18.8k, Rest 17.0k) | 0 (n 20) |
| B | 8 (36%) | 17 (46%) | -10 pts (-44 to +16) | 15.0k | 16 (n 25) |
| A | 3 (14%) | 5 (14%) | 0 pts (-16 to +19) | small n | 25 (n 8) |
| C | 3 | 3 | +6 pts (-12 to +21) | too few | too few |

At D: Harugumo 7, Somers 7, Gearing 4, Delny 2. Cruisers inside: Top 6 Brisbane 5, Utrecht 1, Worcester 1; Rest Brisbane 4, Des Moines 3, Utrecht 2. They sit a median 4.6 km short of the cap edge (cells F9 6, G9 3), so "at D" means the east lane short of D. Same split early and late (early 3 of 8 vs 5 of 14; later 5 of 14 vs 7 of 23).

**Top 6 or Shared:** Shared spot (-23 to +33).

**Clans:** Top 6 BONKZ 4 (of 7 long smokes), H-SR 2 (of 6), RESIN 2 (of 6) | Rest MZY 6 (of 11), -BN- 3 (of 5), BONKY 3 (of 3). Three Top 6 clans of 4 with long smokes; 3 Rest clans of 14.

**Verdict:** Keep (shared; safest long-smoke place on the map).

### C5-SF-3. Svea spot: clan counts
**Answer:** Reproduced: 15 of 18 Top 6 Svea smokes sit in the open water on the own side of D (H7/G7) against 1 of 14 for the Rest.

**Numbers:** Top 6 15 of 18 (83%) vs Rest 1 of 14 (7%), +76 pts (+39 to +100 *). Holds without any one clan (8 of 11 without HTDOG, 9 of 9 without VRTUS). Six games; median time 8:04; 9.6k per smoke; no deaths. The Rest's Svea smokes go to the west cap B (8) and up at D (6).

**Top 6 or Shared:** Top 6 spot (+39 to +100).

**Clans:** Top 6 HTDOG 7 (of 7 Svea smokes on the map), VRTUS 6 (of 9), H-SR 2 (of 2) | Rest EPOXY 1 (of 1). Rest clans whose Svea never smoked there: RSR 0 of 5, KSC 0 of 5, PFANS 0 of 3.

**Verdict:** Keep.

---

### Okinawa

### C5-OK-1. Top 5 smoke ships with games played
**Answer:** By smokes laid: Napoli 32, Svea 25, Daring 22, Gearing 17, Somers 12. Per game played the order changes: the Svea lays 4.2 smokes per team-game, the Napoli 1.5.

**Numbers (18 games, 36 team-games, 158 smokes, all classes):**

| Ship | Class | Smokes | Team-games with the ship in the line-up | Ships fielded | Smokes per team-game played | Top 6 smokes | Concealed dmg per smoke | Deaths per 100 |
|---|---|---|---|---|---|---|---|---|
| Napoli | cruiser | 32 | 21 (Top 6 1) | 24 | 1.52 | 1 | 4.2k | 12.5 |
| Svea | cruiser | 25 | 6 (Top 6 1) | 7 | 4.17 | 3 | 9.6k | 4.0 |
| Daring | destroyer | 22 | 11 (Top 6 2) | 11 | 2.00 | 4 | 6.0k | 9.1 |
| Gearing | destroyer | 17 | 7 (Top 6 2) | 8 | 2.43 | 6 | 10.5k | 23.5 |
| Somers | destroyer | 12 | 4 (Top 6 1) | 5 | 3.00 | 4 | 18.1k (small n) | 16.7 (small n) |

Next: Shimakaze 11 smokes in 10 team-games (1.1), Harugumo 9 in 4 (2.25), Smolensk 8 in 3.

**Top 6 or Shared:** Not a spot. Top 6 played only 6 team-games here, so no comparison.

**Clans:** Napoli: H-SR 1 | BTLST 4, HFANS 4, KM 3, KITED 3, BONKY 3, 5D 2, MACHX 2, MZY 2, and 8 clans with 1. Svea: VRTUS 3 | SCCC2 9, MACH 6, UYSC 3, MACHX 2, BONKY 2. Daring: KITE 3, VRTUS 1 | MZY 9, MACHX 3, -BN- 3, UYSC 2, MACH 1. Gearing: BONKZ 4, KITE 2 | BTLST 3, 5D 2, OGF 2, RSR 2, -BN- 2. Somers: H-SR 4 | MACHX 3, REEEE 3, NGA 2.

**Verdict:** Keep.

### C5-OK-2. Death zone and its share laid while 50+ behind
**Answer:** The zone is the south-west water on the own side of cap C: 39 smokes, 12 deaths, 31 per 100 against 13 per 100 on the rest of the map. 49% of its smokes were laid while 50+ points behind, against 30% elsewhere (35% for the whole map). Neither gap is clear on its own, but the two stack: smokes laid there while 50+ behind lost a ship 42 times per 100.

**Numbers:**
- Shape (0-1 frame): ellipse centred u 0.246, v 0.644; radii 0.240 and 0.150 of the map width (10.1 by 6.3 km); long axis turned 34.5 degrees clockwise. Cells F2, F3, H4, F4, G3. A wide zone.
- Atlas numbers reproduced: the cluster is 12 smokes with a death (15 deaths), 7 of the 12 laid 50+ behind; 10 of those 12 fall inside the drawn ellipse. The ellipse holds 39 smokes of all classes with 12 deaths = 30.8 per 100 (13 to 47). Okinawa as a whole: 28 deaths in 158 smokes = 17.7 per 100 (11 to 24); 22.0 per 100 destroyer smokes (n 82), the highest of any map.
- Zone minus the rest of the map: +17 deaths per 100 (-3 to +35). Not clear.
- Laid 50+ behind: zone 19 of 39 (49%, 28 to 72); rest of the map 36 of 119 (30%, 17 to 44); whole map 55 of 158 (35%, 23 to 46). Difference +18 pts (-7 to +43). Not clear.

| Score when laid | Zone: smokes | Zone: deaths per 100 | Rest of the map: smokes | Rest of the map: deaths per 100 |
|---|---|---|---|---|
| 50+ behind | 19 | 42 | 36 | 17 |
| Level | 8 (small n) | 25 | 45 | 13 |
| 50+ ahead | 12 (small n) | 17 | 38 | 11 |

- Who is in the zone: 20 cruiser smokes, 18 destroyer, 1 battleship (Smolensk 7, Napoli 6, Daring 6, Svea 6, Shimakaze 4). Who died: the smoker in 7 (4 destroyers, 3 cruisers), 4 other cruisers, 1 battleship. Enemy radar had lit the ship in 2 of the 12 deaths. 24 of the 39 smokes were in lost games.

**Top 6 or Shared:** Shared zone. Share of each group's smokes laid there: Top 6 7 of 23 (30%) vs Rest 32 of 135 (24%), +7 pts (-17 to +34).

**Clans:** All 39: Top 6 KITE 3, RESIN 2, BONKZ 1, H-SR 1 | Rest HFANS 7, EPOXY 5, MACH 5, BTLST 2, MACHX 2, -BN- 2, REEEE 2, and 1 each OGF, PN, PFANS, UYSC, MANBA, KITED, MZY. Smokes with a death inside the ellipse (10): Top 6 KITE 1, BONKZ 1 | Rest HFANS 3, EPOXY 2, PN 1, MACH 1, REEEE 1.

**Verdict:** Keep as a danger zone (wide, small n; being behind explains part of it, not all).

---

## Part D: clan styles (D1-D3), Round 5 text

Source: `part-d/FINDINGS-D.md`.


Batch `output/20261117-122135`: 1,547 smokes, 171 games, 30 clans (24 with 7+ games; BTLST, INCA, MANBA, OGF, RMN, KM have 5 or 6 and are flagged).
Everything here is association. Styles describe what clans do; they do not explain winning.
Full tables: `d1_tables.md` (every clan, every score), `d3_tables.md` (styles), `d2_output.txt` (structure checks). Figures: `../figures/d1-clan-heat-table.png`, `d2-style-map.png`, `d3-gauge-strip-example.png`.

How to read the scores:
- Lineup counts ships in the clan's lineup that carry smoke, per game. Long-smoke destroyers = Somers, Gearing, Harugumo, Delny. Cap sitters = Daring, Gdansk, Z-42, Z-52, Grozovoi, Shimakaze. Exhaust ships = Napoli, Venezia, C. Colombo, Conte Verde.
- "For a teammate" = the batch coverage label is stacked or screen. "Selfish" is the remainder.
- Movement uses the batch label: pushing = range to the nearest enemies closed while laying; kiting = range opened; parked = "stationary". The batch label "horizontal" (moved across the front, range about the same) is shown as "sideways" (26% of smokes) and "unclassified" (101 smokes, no enemy position) stays in the denominator.
- Caps taken = the nearest cap was not ours at activation and was ours while the smoke stood or within 60 s after (`we_took`). Cap not lost = for smokes inside or within 2 km of the nearest cap, that cap was not the enemy's and the enemy did not take it (`enemy_took is False`). The batch `cap_def` flag fires for any owned cap with an enemy inside, so it is kept only as a secondary column and not read as "the smoke defended a cap".
- Clan intervals are 95%, from resampling that clan's own games. Top 6 minus Rest intervals resample whole clans. A star means the interval excludes zero.

### D1. Score every clan on the six dimensions

**Answer:** Done for all 30 clans (six flagged). Clans differ most in who the smoke is for and in how much smoke they bring; they differ least in where they put it.

**Numbers:** lowest clan, middle clan and highest clan among the 24 with 7+ games.

| Dimension | Score | Lowest | Median | Highest |
|---|---|---|---|---|
| Lineup | Cruisers carrying smoke per game | 0.1 (KITE, H-SR) | 0.7 | 1.3 (UYSC, KITED, HTDOG) |
| Lineup | Long-smoke destroyers per game | 0.0 (KSE, MACH) | 0.8 | 1.2 (H-SR, KSC) |
| Volume and tempo | Smokes per game | 2.0 (PFANS, PN) | 4.5 | 7.5 (VRTUS) |
| Volume and tempo | First smoke of the game | 2:00 (H-SR) | 3:12 | 5:08 (KSE) |
| Volume and tempo | Smokes after 12:00 | 0% (5D, MACH, NGA, RSR) | 12% | 25% (REEEE) |
| Who it is for | For a teammate | 31% (MACH) | 57% | 82% (H-SR) |
| Who it is for | Radar cruiser inside (destroyer smokes) | 0% (5D, KSE) | 34% | 68% (BONKY) |
| Where | Inside a cap | 7% (PN, small n 14) | 23% | 52% (MACH) |
| Where | Median distance to cap edge | -36 m (MACH) | 2,146 m | 3,832 m (PN) |
| Where | Centre lane | 8% (PFANS) | 22% | 40% (VRTUS) |
| Movement | Parked | 8% (H-SR) | 28% | 50% (SCCC2) |
| Movement | Pushing | 8% (REEEE) | 19% | 36% (PN, small n 14) |
| Movement | Kiting | 8% (KSC) | 19% | 42% (UYSC) |
| What it buys | Concealed damage per game | 3,801 (KSE) | 42,794 | 88,963 (-BN-) |
| What it buys | Concealed damage per smoke | 1,330 (KSE) | 8,687 | 16,378 (PFANS) |
| What it buys | Nearest cap not lost (smokes within 2 km) | 71% (REEEE, n 17) | 89% | 100% (MACH, small n 12) |
| What it buys | Deaths per 100 smokes | 4 (H-SR) | 11 | 32 (5D) |

Smoke ships most often in the lineup (share of team-games), Top 6 (110 team-games) and Rest (232): Somers 31% and 29%; Gdansk 31% and 14% (gap +5 to +27 *); Svea 26% and 14% (-6 to +37); Gearing 21% and 23%; Harugumo 18% and 9% (-6 to +21); Napoli 9% and 39% (-41 to -17 *); Daring 12% and 27% (-30 to +1); Jinan 8% and 3%.

Ships inside destroyer smokes (share of destroyer smokes; Top 6 n 387, Rest n 687): Des Moines 14% and 14%; Brisbane 14% and 6% (-2 to +18); Worcester 6% and 1% (+2 to +9 *); Utrecht 5% and 3%; Minotaur 4% and 5%; Moskva 2% and 1%. Per clan lists are in `d1_tables.md` (for example RESIN: Des Moines 22%, Worcester 15%; BONKZ: Brisbane 36%; BONKY: Brisbane 56%, n 25).

**Top 6 or Shared:** Scores where the Top 6 clearly differ from the Rest (interval excludes zero):
- Radar cruiser inside a destroyer smoke: 47% against 29% (+8 to +27 points *).
- Exhaust-smoke ships per game: 0.2 against 0.6 (-0.6 to -0.2 *).
- Radar ships per game: 3.6 against 3.0 (+0.2 to +0.8 *). Destroyers per game 3.2 against 3.0 (+0.0 to +0.5 *).
- Concealed damage per smoke 11,685 against 8,515 (+570 to +5,691 *); per game 57,152 against 37,034 (+5,335 to +33,897 *).
- Deaths per 100 smokes: 8 against 13 (-9.5 to -2.9 *). Nearest cap not lost (smokes within 2 km): 92% against 87% (+0.6 to +9.5 *, barely).
- Smokes on the clan's own side of the front line: 84% against 78% (+1.4 to +9.8 *).

Shared (no clear gap): smoke cruisers per game (0.5 against 0.7), long-smoke destroyers per game (0.9 against 0.7), smokes per game (4.9 against 4.3), first smoke time (2:55 against 3:18), for a teammate (64% against 55%, -2.5 to +20.2), inside a cap (23% against 24%), centre lane (24% against 21%), pushing, kiting, parked (29% against 27%), caps taken (28% against 23%).

**Clans:** every clan is in `d1_tables.md` and `clan_styles.json`. Top 6 headline values (smoke cruisers per game / smokes per game / for a teammate / inside a cap / parked / concealed damage per game): H-SR 0.1 / 4.5 / 82% / 16% / 8% / 68,194; RESIN 0.3 / 4.3 / 69% / 27% / 21% / 55,017; BONKZ 0.6 / 4.9 / 70% / 29% / 29% / 68,788; KITE 0.1 / 3.2 / 58% / 20% / 22% / 25,532; HTDOG 1.3 / 5.9 / 47% / 25% / 46% / 50,375; VRTUS 1.1 / 7.5 / 52% / 17% / 44% / 68,848.

**Could not be done / proxy:**
- "Caps taken and defended" has no direct record. Cap owners are known only at smoke activation and capture moments, so "taken" and "not lost" mean the nearest cap changed or did not change hands while a smoke stood or within 60 s after. 694 of 1,547 smokes have no "taken" answer (cap already ours or no snapshot). "Not lost" is only read for smokes within 2 km of the cap: 541 smokes; KSE, NGA and PN have too few (7, 7, 5).
- Which caps: listed per clan as the three most-used caps in `d1_tables.md`, but clans played different maps, so this is a note and not a score.
- Lane is the batch's centre / left / right; centre against flanks is the same in the team-normalized frame.
- Flagged clans have 9 to 39 smokes. Rates with fewer than 8 cases are shown as "too few" (MANBA has 5 destroyer smokes; cap rates for MANBA, OGF, RMN, KM).
- Delny is in a lineup 37 times but the batch marks it as carrying smoke only 7 times; only those 7 count as a smoke ship.

**Verdict:** Keep

### D2. Group the clans; one scale or several styles?

**Answer:** It is two separate scales, not one. The first is who the smoke is for (a destroyer lays it for a teammate, against ships smoking for themselves); "adds a smoke cruiser or not" is one part of that scale but not the whole of it. The second is how much smoke a clan brings and uses. The four named styles are the four corners of that two-scale map, with soft borders.

**Numbers:**
- 17 behaviour scores (lineup, tempo, who, where, movement), 24 clans. Outcome scores were kept out so that styles are built only from what clans do.
- First scale carries 29.5% of the differences between clans; second 17.4%; third 12.3%. Shuffled data gives 19.0% and 15.8% at most (95th percentile), so both scales are real. Together 47%: more than half of what separates clans is not on this map.
- First scale, strongest links: stacked on a teammate -0.84, for a teammate -0.82, radar cruiser inside -0.81, long-smoke destroyers per game -0.79, smoke cruisers per game +0.71, cap-sitter destroyers +0.68, parked +0.58, kiting +0.58.
- Second scale: destroyers carrying smoke per game +0.76, smokes per game +0.76, parked +0.54, first smoke time -0.54, cap sitters +0.52, exhaust ships -0.49, pushing -0.47.
- Shape: on the first scale clans are spread out with no break (largest gap 1.6 of a range of 8.6, and that gap is H-SR standing alone at the far end). On the second there is a break: seven clans sit low (MZY, PN, 5D, KITED, KSE, NGA, PFANS; -1.8 or below) and everyone else is at +0.3 or above.
- Are groups real or a smear? Grouping on all 17 scores at once is a smear: silhouette 0.18 (2 groups), 0.16 (3), 0.18 (4), where 1 would be clean groups; shuffled data gives 0.09 to 0.12. Resampling each clan's games reshuffles the groups (agreement with the original 0.54 for 2 groups and 0.34 for 3, where 1 = identical). Dropping the lineup scores changes the groups most (agreement 0.31). The two scales themselves are steady: clan positions on the first scale correlate 0.90 with the original under resampling, on the second 0.78.
- On the two-scale map, four corners are the best fit (silhouette 0.47) and clans keep their corner in 86% of resamples on average.

| Style | Top 6 | Rest | Borderline | Flagged clans that would fall here |
|---|---|---|---|---|
| Team smoke, plenty of it (11 clans, 167 games, 810 smokes) | H-SR, RESIN, BONKZ, KITE | EPOXY, HFANS, -BN-, REEEE, KSC, BONKY, RSR | HFANS, KITE, REEEE | INCA |
| Own smoke, plenty of it (6 clans, 64 games, 383 smokes) | HTDOG, VRTUS | MACHX, MACH, SCCC2, UYSC | MACHX, VRTUS | none |
| Team smoke, little of it (4 clans, 45 games, 116 smokes) | none | MZY, PFANS, NGA, PN | PFANS, NGA | MANBA, RMN, KM |
| Own smoke, little of it (3 clans, 31 games, 120 smokes) | none | KITED, 5D, KSE | none | BTLST, OGF |

Borderline = the clan kept its style in under 75% of resamples of its own games (HFANS 60%, KITE 72%, REEEE 50%, MACHX 63%, VRTUS 64%, PFANS 74%, NGA 74%).

What each style looks like (pooled; 95% interval, games resampled within the style):

| Score | Team smoke, plenty | Own smoke, plenty | Team smoke, little | Own smoke, little |
|---|---|---|---|---|
| Long-smoke destroyers per game | 1.0 (0.9 to 1.1) | 0.4 (0.3 to 0.5) | 0.6 (0.4 to 0.8) | 0.4 (0.2 to 0.5) |
| Cruisers carrying smoke per game | 0.4 (0.3 to 0.5) | 1.1 (0.8 to 1.3) | 0.5 (0.4 to 0.7) | 1.2 (0.9 to 1.4) |
| Destroyers carrying smoke per game | 1.7 (1.6 to 1.8) | 1.6 (1.4 to 1.8) | 0.9 (0.7 to 1.2) | 1.2 (1.0 to 1.3) |
| Smokes per game | 4.9 (4.5 to 5.3) | 6.0 (5.1 to 6.8) | 2.6 (2.0 to 3.2) | 3.9 (3.4 to 4.5) |
| First smoke of the game | 2:43 (2:33 to 3:04) | 3:27 (3:01 to 4:06) | 3:07 (2:21 to 4:53) | 3:45 (3:11 to 4:52) |
| For a teammate | 66% (61 to 70) | 45% (39 to 51) | 61% (50 to 70) | 44% (32 to 56) |
| Radar cruiser inside (destroyer smokes) | 42% (36 to 48) | 28% (20 to 37) | 41% (29 to 52) | 7% (0 to 15) |
| Parked | 25% (21 to 29) | 40% (34 to 48) | 17% (10 to 25) | 23% (17 to 29) |
| Inside a cap | 24% (20 to 29) | 24% (19 to 29) | 17% (10 to 24) | 26% (19 to 32) |
| What it buys: concealed damage per smoke | 11,692 (10,402 to 12,964) | 7,725 (6,524 to 9,044) | 9,204 (6,899 to 12,502) | 4,120 (2,772 to 5,724) |
| What it buys: concealed damage per game | 56,712 (50,377 to 64,535) | 46,230 (35,518 to 56,839) | 23,726 (16,399 to 32,408) | 15,948 (10,177 to 22,684) |
| What it buys: nearest cap taken | 26% (22 to 31) | 24% (18 to 30) | 18% (8 to 30) | 26% (17 to 36) |
| What it buys: nearest cap not lost (smokes within 2 km) | 88% (84 to 92) | 93% (88 to 98) | 85% (74 to 95) | 91% (83 to 98) |
| What it buys: deaths per 100 smokes | 10 (8 to 12) | 9 (6 to 13) | 16 (9 to 23) | 19 (12 to 27) |

Plain reading of the styles:
- **Team smoke, plenty of it.** Somers, Gearing or Harugumo lay smoke for a cruiser, usually a radar cruiser. About one long-smoke destroyer per game and few smoke cruisers. Highest concealed damage per smoke.
- **Own smoke, plenty of it.** Svea, Jinan or Napoli plus cap-sitter destroyers, each smoking for itself, often parked. The most smokes per game; less concealed damage per smoke.
- **Team smoke, little of it.** Same habit as the first style but fewer than one smoke destroyer per game and 2.6 smokes per game.
- **Own smoke, little of it.** Napoli exhaust and cap sitters smoking for themselves, 3.9 smokes per game, a radar cruiser inside only 7% of destroyer smokes. Lowest concealed damage per smoke.

Second check against round 4: H-SR, RESIN, BONKZ bring 0.3 smoke cruisers per game (0.2 to 0.4) and HTDOG, VRTUS 1.2 (0.9 to 1.5); for a teammate 73% against 49%; parked 20% against 45%; first smoke 2:43 against 3:50. Same as round 4. KITE again sits with the long-smoke clans (borderline).

**Top 6 or Shared:**
- First scale (who the smoke is for): Shared. Top 6 mean -1.17, Rest +0.39, gap -1.56 (-3.57 to +0.49). The Top 6 cover almost the whole scale, from H-SR at -4.6 to HTDOG at +2.6.
- Second scale (how much smoke): Top 6. Top 6 mean +0.90, Rest -0.30, gap +1.21 (+0.22 to +2.24 *). All six Top 6 clans are in a "plenty" style; none of the seven low-smoke clans is Top 6.
- Do the Top 6 concentrate in one style? No: four are in "Team smoke, plenty" and two in "Own smoke, plenty". Four or more of six in the largest style happens by chance 24% of the time. All six in the two "plenty" styles (17 of 24 clans) happens by chance 9% of the time. Six clans is very few; neither count is settled.

**Clans:** as in the style table above. W-L by style, for description only: Team smoke plenty 101-66, Own smoke plenty 32-32, Team smoke little 20-25, Own smoke little 12-19.

**Could not be done / proxy:**
- With 24 clans and 17 scores, no method can prove sharp types. The honest reading is a map with two directions and soft borders; seven clans are borderline.
- Much of the first scale restates ship choice: a clan that brings Somers will show long, stacked smokes. Clans also pick ships per map and opponent, and clans played different maps.
- Flagged clans are placed on the same map but were not used to build it; with 5 or 6 games their position is loose.

**Verdict:** Lead

### D3. Compact profile per clan for a gauge graphic

**Answer:** Each clan has one headline number per dimension, its position among the 24 clans with 7+ games (0 = lowest, 100 = highest), and a 95% range from resampling its own games. The full set of 35 scores is kept alongside.

**Numbers:** headline score per dimension and what "high" means:

| Dimension | Headline score | High means |
|---|---|---|
| Lineup | Cruisers carrying smoke per game | more smoke cruisers in the lineup |
| Volume and tempo | Smokes per game | more smokes |
| Who it is for | For a teammate (%) | more smokes laid for a teammate |
| Where | Inside a cap (%) | more smokes inside a cap |
| Movement | Parked (%) | more smokes laid while parked |
| What it buys | Concealed damage per game | more concealed damage |

Two contrasting clans (value, 95% range, percentile):

| Dimension | H-SR | HTDOG |
|---|---|---|
| Lineup | 0.1 (0.0 to 0.2), p4 | 1.3 (1.0 to 1.6), p91 |
| Volume and tempo | 4.5 (3.7 to 5.4), p52 | 5.9 (4.4 to 7.4), p83 |
| Who it is for | 82% (73 to 91), p100 | 47% (32 to 61), p22 |
| Where | 16% (10 to 23), p17 | 25% (17 to 32), p57 |
| Movement | 8% (3 to 15), p0 | 46% (33 to 60), p96 |
| What it buys | 68,194 (48,505 to 89,537), p83 | 50,375 (31,496 to 71,640), p65 |

All 30 clans are in the headline table in `d1_tables.md` and in `clan_styles.json` (`clans.<name>.gauge`; the two scale positions with ranges are in `clans.<name>.axes`).

**Top 6 or Shared:** not a spot item. On the six headline numbers the only clear Top 6 gap is concealed damage per game (+5,335 to +33,897 *); the other five are Shared.

**Clans:** all 30; six flagged (BTLST, INCA, MANBA, OGF, RMN, KM) carry `flagged_small: true` and their percentile is where they would fall among the 24.

**Could not be done / proxy:**
- The ranges are wide for clans with few games: for a 7-game clan a headline value often moves 30 or more percentile points (for example BONKY smoke cruisers per game 0.0 to 1.6). A gauge should draw the range, not only the dot.
- Percentiles rank clans against each other; a high percentile is not "good". Deaths per 100 smokes is the one score where high is worse.

**Verdict:** Keep
