# C1 from the cap timeline (round 5b, worker n1)

Smokes: 1547. End of a smoke = dispersal time; 171 smokes had no dispersal time (replay ended first) and use activation + emission + puff life.
Owner of the nearest cap at activation, timeline vs the round 5 stored value: 1545 of 1547 agree; the 2 that differ: 7898_g1_197676 (timeline neutral, stored ours); 8147_g2_176006 (timeline ours, stored theirs) (the cap flipped within a second of the activation).
Owner at activation (timeline): {'neutral': 380, 'theirs': 473, 'ours': 694}
Team-frame cap letter, timeline file vs r5lib: 0 mismatches of 1547.
Second computation straight from the caps_timeline rows (own loop, not tl.owner_changes): 1547 of 1547 smokes agree on all four yes/no values.

## Enemy took the nearest cap: three ways

| what | applicable smokes | strictly while the smoke stood (grace 0) | only in the 60 s after | during or within 60 s (grace 60) |
|---|---|---|---|---|
| enemy took the nearest cap | 1074 | 155 (14.4%) | 78 (7.3%) | 233 (21.7%) |
| we took the nearest cap | 853 | 196 (23.0%) | 76 (8.9%) | 272 (31.9%) |
Not applicable (cap already the enemy's at activation): 473; (cap already ours, for "we took"): 694.

Grace after the smoke clears (timeline):
| grace | enemy took: yes | no | yes share | round 5 snapshot yes (share) | we took: yes | yes share |
|---|---|---|---|---|---|---|
| 0 s | 155 | 919 | 14.4% | 103 (9.6%) | 196 | 23.0% |
| 10 s | 173 | 901 | 16.1% | - | 214 | 25.1% |
| 30 s | 199 | 875 | 18.5% | - | 242 | 28.4% |
| 60 s | 233 | 841 | 21.7% | 184 (17.1%) | 272 | 31.9% |
| 120 s | 293 | 781 | 27.3% | 233 (21.7%) | 323 | 37.9% |
Flips in the 60 s after: median 26 s after the smoke cleared (quartiles 11 to 45).
Flips during the smoke: median 53 s after activation (quartiles 30 to 104); smoke life median 117 s.

## Timeline against the round 5 snapshot version, same smokes (grace 60 s both)

Enemy took the nearest cap:
| round 5 snapshot \ timeline | yes | no | n/a | total |
|---|---|---|---|---|
| yes | 184 | 0 | 0 | 184 |
| no | 48 | 841 | 0 | 889 |
| n/a | 1 | 0 | 473 | 474 |
| total | 233 | 841 | 473 | 1547 |
Both versions applicable: 1073. Agree: 1025 (95.5%). Snapshot missed a flip (said no, timeline yes): 48. Snapshot wrong the other way (said yes, timeline no): 0.
Real flips in these smokes (timeline yes): 232; the snapshot version found 184 and missed 48 = 20.7% of real flips.

We took the nearest cap:
| round 5 snapshot \ timeline | yes | no | n/a | total |
|---|---|---|---|---|
| yes | 209 | 0 | 0 | 209 |
| no | 62 | 581 | 1 | 644 |
| n/a | 1 | 0 | 693 | 694 |
| total | 272 | 581 | 694 | 1547 |
Both versions applicable: 852. Agree: 790 (92.7%). Snapshot missed a flip (said no, timeline yes): 62. Snapshot wrong the other way (said yes, timeline no): 0.
Real flips in these smokes (timeline yes): 271; the snapshot version found 209 and missed 62 = 22.9% of real flips.

Of the 48 flips the snapshot missed: in 2 the cap had flipped back by the end of the window; in 46 it was still the enemy's at the end of the window, so the flip fell after the last snapshot.
  Top 6: real flips 79, snapshot missed 21 (27%); snapshots in the window per smoke: median 5, mean 5.3.
  Rest: real flips 153, snapshot missed 27 (18%); snapshots in the window per smoke: median 5, mean 5.2.
Cross-check with the batch field cap_won (10 s grace in the batch): it names the nearest cap in 171 smokes. Round 5 snapshot we_took: yes 144, no 26, n/a 1. Timeline, grace 60: yes 170, no 0, n/a 1; timeline, grace 10: yes 170, no 0, n/a 1.

Enemy took the nearest cap, during the smoke or within 60 s after (compare with round 5). Cap already the enemy's at activation is excluded. * = interval excludes zero.
| group | n | enemy took it | Top 6 | Rest | Top 6 - Rest | round 5 snapshot: share (n); gap |
|---|---|---|---|---|---|---|
| all applicable smokes | 1074 | 21.7% (19.5 to 23.9) | 19.9% (n 403) | 22.8% (n 671) | -3.0 (-7.1 to +1.2) | 17.1% (n 1073); gap -4.4 (-8.9 to +0.1) |
| destroyer smokes | 763 | 23.1% (20.1 to 26.5) | 20.9% (n 292) | 24.4% (n 471) | -3.5 (-9.5 to +2.8) | 18.8% (n 762); gap -5.9 (-12.1 to -0.9) * |
| smoke centre inside or within 2 km of the cap | 541 | 16.1% (13.2 to 19.6) | 14.3% (n 189) | 17.0% (n 352) | -2.8 (-8.9 to +3.9) | 11.1% (n 541); gap -4.8 (-9.2 to -0.7) * |
| destroyer smokes inside or within 2 km | 405 | 17.5% (14.0 to 21.8) | 15.5% (n 142) | 18.6% (n 263) | -3.1 (-11.0 to +4.5) | 12.8% (n 405); gap -6.8 (-12.6 to -1.7) * |
| cap ours at activation | 694 | 18.2% (15.1 to 21.6) | 18.4% (n 261) | 18.0% (n 433) | +0.4 (-5.8 to +5.8) | 13.7% (n 694); gap -1.6 (-8.2 to +5.0) |
| cap neutral at activation | 380 | 28.2% (23.3 to 33.9) | 22.5% (n 142) | 31.5% (n 238) | -9.0 (-18.3 to -0.2 *) | 23.5% (n 379); gap -9.4 (-18.4 to -0.5) * |
| cap ours, smoke within 2 km | 349 | 12.3% (8.5 to 16.1) | 11.2% (n 116) | 12.9% (n 233) | -1.7 (-11.1 to +6.8) | 8.0% (n 350); gap -4.2 (-9.7 to +1.5) |
| cap ours, cap_defended set for that cap | 153 | 45.8% (37.9 to 53.3) | 48.1% (n 52) | 44.6% (n 101) | +3.5 (-13.1 to +20.0) | 35.9% (n 153); gap -7.8 (-24.7 to +10.5) |
| cap ours, cap_defended not set for it | 541 | 10.4% (8.1 to 13.0) | 11.0% (n 209) | 9.9% (n 332) | +1.1 (-3.7 to +5.3) | 7.4% (n 541); gap +1.3 (-3.4 to +5.2) |

Enemy took the nearest cap, strictly while the smoke stood. Cap already the enemy's at activation is excluded. * = interval excludes zero.
| group | n | enemy took it | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all applicable smokes | 1074 | 14.4% (12.0 to 17.0) | 11.9% (n 403) | 15.9% (n 671) | -4.0 (-8.0 to +0.3) |
| destroyer smokes | 763 | 16.1% (13.4 to 19.4) | 12.7% (n 292) | 18.3% (n 471) | -5.6 (-11.0 to +0.3) |
| smoke centre inside or within 2 km of the cap | 541 | 9.6% (6.7 to 12.7) | 6.9% (n 189) | 11.1% (n 352) | -4.2 (-10.1 to +1.2) |
| destroyer smokes inside or within 2 km | 405 | 11.1% (7.4 to 15.3) | 7.0% (n 142) | 13.3% (n 263) | -6.3 (-14.8 to +1.1) |
| cap ours at activation | 694 | 11.0% (8.7 to 13.6) | 10.3% (n 261) | 11.3% (n 433) | -1.0 (-5.9 to +3.3) |
| cap neutral at activation | 380 | 20.8% (15.9 to 26.6) | 14.8% (n 142) | 24.4% (n 238) | -9.6 (-17.4 to -0.4 *) |
| cap ours, smoke within 2 km | 349 | 5.7% (2.9 to 9.2) | 3.4% (n 116) | 6.9% (n 233) | -3.4 (-9.4 to +2.3) |
| cap ours, cap_defended set for that cap | 153 | 28.1% (20.8 to 36.4) | 23.1% (n 52) | 30.7% (n 101) | -7.6 (-22.0 to +4.7) |
| cap ours, cap_defended not set for it | 541 | 6.1% (4.1 to 7.9) | 7.2% (n 209) | 5.4% (n 332) | +1.8 (-1.9 to +5.1) |

By map and cap (cap letter in the team frame), grace 60 s:
| map | cap | n | enemy took it (60 s) | Top 6 | Rest | Top 6 - Rest | strictly during | round 5 snapshot |
|---|---|---|---|---|---|---|---|---|
| Hotspot | A | 11 (small n) | 9.1% (0.0 to 37.5) | too few (n 7) | too few (n 4) | - | 9.1% | 0.0% |
| Hotspot | B | 44 | 11.4% (3.8 to 21.6) | 21.4% (n 14) | 6.7% (n 30) | +14.8 (-5.7 to +47.1) | 11.4% | 9.1% |
| Hotspot | C | 65 | 32.3% (22.5 to 44.2) | 33.3% (n 21) | 31.8% (n 44) | +1.5 (-17.9 to +16.4) | 23.1% | 26.2% |
| Hotspot | D | 84 | 25.0% (14.9 to 36.5) | 12.5% (n 24) | 30.0% (n 60) | -17.5 (-35.8 to +10.6) | 17.9% | 23.8% |
| Land of Fire | A | 53 | 22.6% (7.8 to 39.0) | 9.1% (n 11) | 26.2% (n 42) | -17.1 (-41.5 to +10.2) | 18.9% | 20.8% |
| Land of Fire | B | 68 | 14.7% (9.2 to 23.6) | 11.1% (n 36) | 18.8% (n 32) | -7.6 (-25.7 to +4.2) | 10.3% | 11.8% |
| Land of Fire | C | 5 | too few |  |  |  |  |  |
| Land of Fire | D | 26 | 11.5% (0.0 to 26.9) | 21.4% (n 14) | 0.0% (n 12) | +21.4 (+0.0 to +46.7) | 7.7% | 7.7% |
| Loop | A | 47 | 21.3% (7.1 to 34.0) | 9.1% (n 11) | 25.0% (n 36) | -15.9 (-37.0 to +2.9) | 10.6% | 17.0% |
| Loop | B | 30 | 30.0% (13.5 to 48.5) | 20.0% (n 10) | 35.0% (n 20) | -15.0 (-47.1 to +9.1) | 20.0% | 20.0% |
| Loop | C | 33 | 15.2% (4.5 to 34.6) | 5.6% (n 18) | 26.7% (n 15) | -21.1 (-54.5 to +1.9) | 9.1% | 12.1% |
| Mountain Range | A | 41 | 24.4% (8.3 to 40.6) | 26.3% (n 19) | 22.7% (n 22) | +3.6 (-29.2 to +32.9) | 14.6% | 14.6% |
| Mountain Range | B | 46 | 39.1% (28.4 to 55.6) | 36.0% (n 25) | 42.9% (n 21) | -6.9 (-41.7 to +19.0) | 26.1% | 35.6% |
| Mountain Range | C | 56 | 21.4% (9.6 to 37.9) | 8.0% (n 25) | 32.3% (n 31) | -24.3 (-42.6 to -3.5 *) | 17.9% | 17.9% |
| Okinawa | A | 39 | 23.1% (12.8 to 33.3) | too few (n 4) | 22.9% (n 35) | - | 12.8% | 15.4% |
| Okinawa | B | 8 (small n) | 12.5% (0.0 to 50.0) | too few (n 2) | too few (n 6) | - | 12.5% | 12.5% |
| Okinawa | C | 37 | 18.9% (8.3 to 33.3) | too few (n 7) | 16.7% (n 30) | - | 13.5% | 13.5% |
| Okinawa | D | 26 | 30.8% (12.5 to 50.0) | too few (n 3) | 26.1% (n 23) | - | 15.4% | 19.2% |
| Sea of Fortune | A | 12 (small n) | 16.7% (0.0 to 30.8) | too few (n 4) | 25.0% (n 8) | - | 8.3% | 8.3% |
| Sea of Fortune | B | 60 | 13.3% (4.4 to 22.9) | 25.0% (n 12) | 10.4% (n 48) | +14.6 (-12.2 to +43.8) | 6.7% | 10.0% |
| Sea of Fortune | C | 15 | 40.0% (14.3 to 64.7) | too few (n 7) | 25.0% (n 8) | - | 13.3% | 6.7% |
| Sea of Fortune | D | 41 | 17.1% (5.1 to 28.9) | 16.7% (n 18) | 17.4% (n 23) | -0.7 (-25.2 to +23.5) | 12.2% | 17.1% |
| Sleeping Giant | A | 90 | 26.7% (15.2 to 46.0) | 22.4% (n 49) | 31.7% (n 41) | -9.3 (-32.5 to +31.9) | 16.7% | 21.1% |
| Sleeping Giant | B | 46 | 10.9% (1.8 to 27.7) | 5.0% (n 20) | 15.4% (n 26) | -10.4 (-33.3 to +12.7) | 8.7% | 8.7% |
| Sleeping Giant | C | 16 | 18.8% (0.0 to 36.4) | too few (n 7) | 0.0% (n 9) | - | 12.5% | 18.8% |
| Sleeping Giant | D | 75 | 20.0% (8.4 to 32.1) | 25.7% (n 35) | 15.0% (n 40) | +10.7 (-14.1 to +35.7) | 12.0% | 17.3% |

For reference, "we took the nearest cap" (cap not ours at activation), grace 60 s:
| group | n | we took it | Top 6 | Rest | Top 6 - Rest | strictly during | round 5 snapshot |
|---|---|---|---|---|---|---|---|
| all smokes where the nearest cap was not ours | 853 | 31.9% (27.4 to 36.9) | 39.0% (n 277) | 28.5% (n 576) | +10.5 (-0.2 to +22.1) | 23.0% | 24.5% (n 853) |
| destroyer smokes | 582 | 35.6% (29.5 to 41.8) | 45.7% (n 197) | 30.4% (n 385) | +15.3 (+2.1 to +28.1 *) | 25.9% | 27.0% (n 582) |
| within 2 km | 350 | 42.3% (36.8 to 47.2) | 50.4% (n 115) | 38.3% (n 235) | +12.1 (+1.3 to +23.5 *) | 33.7% | 35.0% (n 349) |

## cap_defended follow-up: was the defended cap still ours afterwards?

Smokes with cap_defended: 486. The timeline shows the "ours and invaded by the enemy" moment inside the smoke's life for 485 of them (the rest: the batch saw it at a 2 s sample the change log places just outside the smoke's exact times; activation is used as the start for those).
Defended cap already ours at activation: 423 of 486. Time the enemy stood in the defended cap while the smoke stood: median 39 s (quartiles 23 to 59).

Kept = the enemy did not take the defended cap between the first invaded moment and 60 s after the smoke cleared.
| group | n | kept through 60 s after | Top 6 | Rest | Top 6 - Rest | kept while the smoke stood | round 5 snapshot (60 s) |
|---|---|---|---|---|---|---|---|
| all smokes with cap_defended | 486 | 52.5% (46.1 to 58.3) | 53.4% (n 163) | 52.0% (n 323) | +1.4 (-13.2 to +13.7) | 68.7% (63.9 to 73.1) | 60.5% (n 486); gap +3.1 |
| destroyer smokes | 360 | 50.6% (43.9 to 56.4) | 51.6% (n 124) | 50.0% (n 236) | +1.6 (-14.2 to +14.5) | 66.9% (61.7 to 71.5) | 58.9% (n 360); gap +1.2 |
| defended cap = nearest cap | 175 | 53.7% (46.6 to 60.4) | 52.4% (n 63) | 54.5% (n 112) | -2.1 (-19.1 to +15.6) | 74.3% (66.9 to 80.5) | 61.1% (n 175); gap +8.6 |
| defended cap not the nearest | 311 | 51.8% (44.7 to 58.4) | 54.0% (n 100) | 50.7% (n 211) | +3.3 (-13.2 to +17.9) | 65.6% (60.1 to 70.5) | 60.1% (n 311); gap -0.2 |
  grace 0 s: kept 334 of 486 (68.7%)
  grace 60 s: kept 255 of 486 (52.5%)
  grace 120 s: kept 227 of 486 (46.7%)
  round 5 style test on the timeline (enemy owned it at any moment from activation to 60 s after): kept 255 of 486 (52.5%).
Owner of the defended cap 60 s after the smoke cleared: {'ours': 264, 'theirs': 222}.
For comparison, any smoke whose nearest cap was ours at activation: the enemy did not take it (through 60 s after) in 81.8% (n 694); round 5 snapshot: 86.3% (n 694).

## New: enemy inside the cap while the smoke stood (smokes within 2 km of a cap we own)

| smokes | n | enemy was invading the cap while the smoke stood | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| within 2 km of a cap we own | 349 | 27.2% (19.9 to 33.8) | 29.3% (n 116) | 26.2% (n 233) | +3.1 (-10.9 to +16.5) |
| destroyer smokes within 2 km of a cap we own | 255 | 31.0% (22.8 to 39.7) | 29.5% (n 88) | 31.7% (n 167) | -2.2 (-22.6 to +13.6) |
| any smoke whose nearest cap is ours (reference) | 694 | 33.7% (28.5 to 38.9) | 34.1% (n 261) | 33.5% (n 433) | +0.6 (-10.8 to +11.4) |
Seconds the enemy stood in the cap during those smokes: median 40 s (quartiles 24 to 55).

Was the cap then kept?
| smokes | n | kept while the smoke stood | Top 6 | Rest | Top 6 - Rest | kept through 60 s after | Top 6 - Rest (60 s) |
|---|---|---|---|---|---|---|---|
| invaded, within 2 km | 95 | 78.9% (66.2 to 88.6) | 88.2% (n 34) | 73.8% (n 61) | +14.5 (-1.9 to +37.3) | 58.9% (44.4 to 70.5) | +4.4 (-18.2 to +33.3) |
| invaded, destroyer smokes within 2 km | 79 | 77.2% (65.0 to 87.5) | 88.5% (n 26) | 71.7% (n 53) | +16.8 (-1.3 to +42.6) | 58.2% (44.1 to 70.3) | +4.9 (-19.7 to +39.6) |
| not invaded, within 2 km | 254 | 100.0% (100.0 to 100.0) | 100.0% (n 82) | 100.0% (n 172) | +0.0 (+0.0 to +0.0) | 98.4% (96.2 to 100.0) | +2.3 (+0.0 to +6.0) |

Wrote enemy-took.csv (1547 rows). "within_60s" = during the smoke or in the 60 s after it cleared.

## Ribbons per smoke

Recording players found: 341 (one per run; 341 ships of 3,078). Ribbon rows in the batch: 442; by kind (rows / sum of the count column): Defended 284 / 284, Captured 91 / 91, AssistedInCapture 67 / 67.
Ribbon rows whose ship is not the run's recording player: 0.
Smokes that covered the recording player of the smoking team (smoker, inside, behind or line of fire): 268 of 1547 (17.3%): {'line_of_fire': 49, 'behind': 31, 'smoker': 129, 'inside': 59}. Recording player was the smoker or inside: 188 (12.2%). Recording player within 2 km of the smoke at some moment while it stood (loose): 254 (16.4%).

Strict: ribbon by a ship the smoke covered, during the smoke. Events and distinct smokes (a Defended ribbon repeats while defending).
| smokes | n | with any cap ribbon | Defended | Captured | AssistedInCapture |
|---|---|---|---|---|---|
| recording player covered by the smoke | 268 | 47 (17.5%) | 68 in 24 smokes (25.4 per 100) | 13 in 13 smokes (4.9 per 100) | 11 in 11 smokes (4.1 per 100) |
|   Top 6 | 110 | 23 (20.9%) | 19 in 6 smokes (17.3 per 100) | 11 in 11 smokes (10.0 per 100) | 7 in 7 smokes (6.4 per 100) |
|   Rest | 158 | 24 (15.2%) | 49 in 18 smokes (31.0 per 100) | 2 in 2 smokes (1.3 per 100) | 4 in 4 smokes (2.5 per 100) |
| recording player the smoker or inside | 188 | 36 (19.1%) | 44 in 15 smokes (23.4 per 100) | 13 in 13 smokes (6.9 per 100) | 9 in 9 smokes (4.8 per 100) |
|   destroyer smokes, recording player covered | 208 | 35 (16.8%) | 54 in 16 smokes (26.0 per 100) | 12 in 12 smokes (5.8 per 100) | 8 in 8 smokes (3.8 per 100) |

Loose: ribbon by a ship of the smoking team during the smoke while that ship was within 2 km of the smoke.
| smokes | n | with any cap ribbon | Defended | Captured | AssistedInCapture |
|---|---|---|---|---|---|
| recording player within 2 km while the smoke stood | 254 | 26 (10.2%) | 38 in 15 smokes (15.0 per 100) | 5 in 5 smokes (2.0 per 100) | 6 in 6 smokes (2.4 per 100) |
|   Top 6 | 115 | 10 (8.7%) | 9 in 3 smokes (7.8 per 100) | 4 in 4 smokes (3.5 per 100) | 3 in 3 smokes (2.6 per 100) |
|   Rest | 139 | 16 (11.5%) | 29 in 12 smokes (20.9 per 100) | 1 in 1 smokes (0.7 per 100) | 3 in 3 smokes (2.2 per 100) |

Top 6 vs Rest (share of smokes, intervals by resampling clans):
| measure | n | share of smokes | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| strict: any cap ribbon | 268 | 17.5% (12.4 to 23.0) | 20.9% (n 110) | 15.2% (n 158) | +5.7 (-6.0 to +16.7) |
| strict: a Defended ribbon | 268 | 9.0% (6.0 to 12.0) | 5.5% (n 110) | 11.4% (n 158) | -5.9 (-11.6 to -0.7 *) |
| strict: a Captured or Assisted ribbon | 268 | 9.0% (3.7 to 14.7) | 16.4% (n 110) | 3.8% (n 158) | +12.6 (+3.1 to +23.6 *) |
| loose: any cap ribbon | 254 | 10.2% (6.5 to 14.5) | 8.7% (n 115) | 11.5% (n 139) | -2.8 (-10.7 to +5.5) |
| loose: a Defended ribbon | 254 | 5.9% (2.9 to 9.4) | 2.6% (n 115) | 8.6% (n 139) | -6.0 (-11.1 to -1.2 *) |

Do smokes with a Defended ribbon keep the cap more often? (nearest cap ours at activation; the ribbon does not say which cap it was for)
| smokes (nearest cap ours) | Defended ribbon: kept while the smoke stood | no Defended ribbon: kept | Defended ribbon: kept through 60 s | no Defended ribbon: kept through 60 s | gap, 60 s (interval) |
|---|---|---|---|---|---|
| strict, recording player covered | 11 of 11 (100%) (small n) | 78 of 96 (81%) | 7 of 11 (64%) (small n) | 74 of 96 (77%) | -13 (-50 to +14) |
| strict, and smoke within 2 km of the cap | too few (n 4) | 43 of 46 (93%) | too few (n 4) | 39 of 46 (85%) | - |
| loose, recording player within 2 km of the smoke | too few (n 6) | 84 of 99 (85%) | too few (n 6) | 79 of 99 (80%) | - |
| loose, and smoke within 2 km of the cap | too few (n 3) | 44 of 46 (96%) | too few (n 3) | 40 of 46 (87%) | - |
| loose, smoke within 2 km, enemy was invading the cap | too few (n 2) | 8 of 10 (80%) (small n) | too few (n 2) | 6 of 10 (60%) (small n) | - |

Ribbons against the cap timeline: 91 of 91 Captured ribbons fall within 3 s of a cap changing to that team; 203 of 284 Defended ribbons fall while the enemy was invading a cap that team owned, 284 while the enemy was invading any cap (the ribbon is also given for stopping the capture of a neutral cap).
Smokes with a strict Captured ribbon: 13; the timeline says we took the nearest cap during the smoke in 12, the nearest cap was already ours in 1 (the ribbon was for another cap).
