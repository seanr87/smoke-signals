# C1 part 1: cap_defended in the data

| smokes | n | cap_defended set | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all smokes | 1547 | 31.4% (28.1 to 34.9) | 30.3% (n 538) | 32.0% (n 1009) | -1.7 (-9.5 to +5.2) |
| destroyer smokes | 1074 | 33.5% (30.1 to 36.7) | 32.0% (n 387) | 34.4% (n 687) | -2.3 (-11.8 to +4.3) |
| cruiser smokes | 439 | 26.9% (21.6 to 33.3) | 25.5% (n 141) | 27.5% (n 298) | -2.0 (-13.5 to +8.7) |

Smokes with cap_defended: 486 of 1547. Role of the defended cap (team frame): {'middle': 459, 'enemy side': 27}
Defended cap is also the smoke's nearest cap (near_cap): 175 of 486 (36%). It is the batch's "contested cap": 183.
Distance from the smoke edge to the defended cap edge: median 8,949 m, quartiles 2,044 to 16,723 m; touching or inside the cap (<= 0 m): 74; more than 3 km away: 347; more than 6 km: 307.
Defended cap was already ours at activation: 423 of 486 (the rest became ours, then invaded, during the smoke).

Defended cap still ours afterwards = no cap snapshot while the smoke stood or within 60 s after shows the enemy owning it.
| group | n (with a snapshot) | never the enemy's | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all smokes with cap_defended | 486 | 60.5% (54.9 to 65.7) | 62.6% (n 163) | 59.4% (n 323) | +3.1 (-10.7 to +15.3) |
| destroyer smokes | 360 | 58.9% (52.5 to 64.9) | 59.7% (n 124) | 58.5% (n 236) | +1.2 (-15.0 to +13.3) |
| defended cap = nearest cap | 175 | 61.1% (54.9 to 67.0) | 66.7% (n 63) | 58.0% (n 112) | +8.6 (-6.2 to +21.9) |
| defended cap not the nearest | 311 | 60.1% (52.1 to 65.7) | 60.0% (n 100) | 60.2% (n 211) | -0.2 (-16.7 to +14.0) |
Owner of the defended cap at the last snapshot in the window: {'ours': 307, 'theirs': 178, 'neutral': 1}; no snapshot in window: 0.
  grace 0 s: kept 374 of 486 (77.0%)
  grace 120 s: kept 252 of 486 (51.9%)
  grace 300 s: kept 212 of 486 (43.6%)
By map and (team-frame) cap: {'Hotspot A': 16, 'Hotspot C': 51, 'Hotspot D': 51, 'Land of Fire A': 12, 'Land of Fire B': 28, 'Land of Fire C': 1, 'Loop A': 28, 'Loop B': 35, 'Loop C': 18, 'Mountain Range A': 39, 'Mountain Range B': 24, 'Mountain Range C': 20, 'Okinawa C': 37, 'Okinawa D': 4, 'Sea of Fortune A': 2, 'Sea of Fortune C': 42, 'Sea of Fortune D': 19, 'Sleeping Giant A': 31, 'Sleeping Giant B': 20, 'Sleeping Giant C': 8}
For comparison, any smoke whose nearest cap was ours at activation: enemy never took it in the window in 86.3% (n 694).

# C1 part 2: "enemy took the cap during the smoke" (r5lib enemy_took)

Independent re-computation from the raw json (own code, json clocks instead of csv clocks): 1545 of 1547 smokes agree on enemy_took, we_took and the snapshot count; mismatches: 2.
Coverage (all smokes): {'yes': 184, "n/a: cap already the enemy's": 474, 'no': 889}
Owner of the nearest cap at activation: {'neutral': 379, 'theirs': 474, 'ours': 694}
Snapshots in the window (applicable smokes, n 1073): median 5, quartiles 3 to 7; only one snapshot: 111 (10%).
Window length: median 158 s. Largest gap between two snapshots inside the window: median 48 s (quartiles 30 to 73).
Unobserved tail (last snapshot to the end of the window): median 21 s, quartiles 7 to 52; tail longer than 60 s: 241 (22%). Share of the window covered up to the last snapshot: median 85%.
Cross-check with the batch field cap_won (built from the continuous cap history, 10 s grace): cap_won names the nearest cap in 171 smokes; we_took says yes in 144, no in 26, n/a in 1.
   with a 0 s grace: yes 96, no 74, n/a 1
   with a 10 s grace: yes 108, no 62, n/a 1
   with a 60 s grace: yes 144, no 26, n/a 1
   cap_won but we_took = no (flip not seen in any snapshot, i.e. it flipped back or the window is sparse): [('7970_g1_159229', 4), ('7975_g1_221693', 3), ('7920_g1_144958', 1), ('7924_g1_46516', 5), ('7924_g1_46518', 2), ('7899_g1_27088', 1), ('7927_g1_32336', 3), ('7928_g1_68253', 1), ('7986_g1_113717', 3), ('7906_g1_188247', 5), ('7906_g1_188249', 1), ('7909_g1_53994', 3)]

Grace after the smoke clears:
| grace | enemy took: yes | no | n/a | yes share | we took: yes | no | yes share |
|---|---|---|---|---|---|---|---|
| 0 s | 103 | 969 | 475 | 9.6% | 119 | 733 | 14.0% |
| 60 s | 184 | 888 | 475 | 17.2% | 209 | 643 | 24.5% |
| 120 s | 233 | 839 | 475 | 21.7% | 269 | 583 | 31.6% |

Hand check: 10 smokes (seeded sample: 4 yes, 4 no, 2 n/a). Every raw cap state of the game from 30 s before activation to 90 s after the window.

- 7939_g1_90312 MACHX vs SCCC2 on Sea of Fortune; nearest cap B (3,178 m to its edge), owner at activation: ours; smoke 321 to 439 s, window to 499 s; library enemy_took = True, snapshots in window = 8
  294:ours  304:ours  312:ours  317:ours  321:ours  341*:ours  348*:ours  433*:ENEMY  469*:ENEMY  474*:ENEMY  480*:ENEMY  496*:ENEMY  497*:ENEMY  506:ENEMY  508:ENEMY  545:ENEMY  551:ENEMY  555:ENEMY  564:ENEMY  565:ENEMY   (* = inside the window)
  by hand: True -> agrees

- 7924_g1_46507 H-SR vs -BN- on Okinawa; nearest cap D (1,847 m to its edge), owner at activation: neutral; smoke 162 to 335 s, window to 395 s; library enemy_took = True, snapshots in window = 9
  155:neutral  162:neutral  192*:neutral  206*:neutral  345*:neutral  348*:neutral  357*:neutral  359*:ENEMY  382*:ENEMY  384*:ENEMY  389*:ENEMY  398:ENEMY  428:ENEMY  432:ENEMY  461:ENEMY  473:ENEMY   (* = inside the window)
  by hand: True -> agrees

- 8074_g2_70760 HFANS vs HTDOG on Land of Fire; nearest cap B (4,173 m to its edge), owner at activation: neutral; smoke 424 to 476 s, window to 536 s; library enemy_took = True, snapshots in window = 10
  398:neutral  405:neutral  421:neutral  424:neutral  427*:neutral  431*:neutral  436*:neutral  439*:neutral  451*:neutral  461*:neutral  495*:ENEMY  495*:ENEMY  498*:ENEMY  509*:ENEMY  561:ENEMY  572:ENEMY  573:ENEMY  582:ENEMY  596:ENEMY  599:ENEMY   (* = inside the window)
  by hand: True -> agrees

- 8175_g1_63098 BONKZ vs HTDOG on Sleeping Giant; nearest cap C (520 m to its edge), owner at activation: ours; smoke 607 to 776 s, window to 836 s; library enemy_took = True, snapshots in window = 5
  607:ours  616*:ours  629*:ours  646*:ours  800*:ENEMY  805*:ENEMY   (* = inside the window)
  by hand: True -> agrees

- 7888_g1_38995 KM vs INCA on Hotspot; nearest cap B (-1,829 m to its edge), owner at activation: ours; smoke 565 to 623 s, window to 683 s; library enemy_took = False, snapshots in window = 4
  560:ours  562:ours  565:ours  574*:ours  614*:ours  614*:ours  626*:ours   (* = inside the window)
  by hand: False -> agrees

- 7916_g1_26980 BONKY vs SCCC2 on Hotspot; nearest cap D (3,784 m to its edge), owner at activation: neutral; smoke 545 to 725 s, window to 785 s; library enemy_took = False, snapshots in window = 4
  519:neutral  529:neutral  545:neutral  598*:neutral  731*:neutral  738*:neutral  771*:neutral  792:neutral  842:neutral  852:neutral   (* = inside the window)
  by hand: False -> agrees

- 8176_g2_139975 RESIN vs H-SR on Hotspot; nearest cap C (3,135 m to its edge), owner at activation: neutral; smoke 91 to 261 s, window to 321 s; library enemy_took = False, snapshots in window = 3
  91:neutral  131*:neutral  146*:neutral  168*:neutral  326:ENEMY  370:ENEMY   (* = inside the window)
  by hand: False -> agrees

- 8074_g2_70754 HTDOG vs HFANS on Land of Fire; nearest cap B (2,128 m to its edge), owner at activation: neutral; smoke 219 to 270 s, window to 330 s; library enemy_took = False, snapshots in window = 4
  198:neutral  210:neutral  210:neutral  219:neutral  220*:neutral  230*:neutral  318*:neutral  329*:neutral  339:neutral  384:neutral  398:neutral  405:neutral   (* = inside the window)
  by hand: False -> agrees

- 7892_g1_80009 INCA vs EPOXY on Loop; nearest cap A (481 m to its edge), owner at activation: theirs; smoke 337 to 389 s, window to 449 s; library enemy_took = None, snapshots in window = 6
  337:ENEMY  349*:ENEMY  349*:ENEMY  384*:ours  405*:ours  430*:ours  441*:ours  491:ours  502:ours  518:ours   (* = inside the window)
  by hand: None -> agrees

- 7934_g1_80510 SCCC2 vs -BN- on Sleeping Giant; nearest cap D (2,489 m to its edge), owner at activation: theirs; smoke 395 to 569 s, window to 629 s; library enemy_took = None, snapshots in window = 8
  374:ENEMY  376:ENEMY  386:ENEMY  387:ENEMY  395:ENEMY  443*:ours  469*:ours  479*:ours  506*:ours  519*:ours  603*:ours  613*:ours  623*:ours  671:ours   (* = inside the window)
  by hand: None -> agrees

Hand check agreement: 10 of 10.

Distance from smoke centre to the nearest cap edge: median 2,314 m; inside the cap: 311; within 2 km: 699; more than 5 km away: 346.

Enemy took the nearest cap (window = smoke life + 60 s). Cap already the enemy's and no-snapshot smokes are excluded.
| group | n | enemy took it | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all applicable smokes | 1073 | 17.1% (14.8 to 19.4) | 14.4% (n 402) | 18.8% (n 671) | -4.4 (-8.9 to +0.1) |
| destroyer smokes | 762 | 18.8% (15.7 to 22.1) | 15.1% (n 291) | 21.0% (n 471) | -5.9 (-12.1 to -0.9 *) |
| smoke centre inside or within 2 km of the cap | 541 | 11.1% (8.8 to 13.8) | 7.9% (n 189) | 12.8% (n 352) | -4.8 (-9.2 to -0.7 *) |
| destroyer smokes inside or within 2 km | 405 | 12.8% (9.5 to 16.2) | 8.5% (n 142) | 15.2% (n 263) | -6.8 (-12.6 to -1.7 *) |
| cap ours at activation | 694 | 13.7% (10.6 to 16.7) | 12.7% (n 260) | 14.3% (n 434) | -1.6 (-8.2 to +5.0) |
| cap neutral at activation | 379 | 23.5% (18.5 to 29.3) | 17.6% (n 142) | 27.0% (n 237) | -9.4 (-18.4 to -0.5 *) |
| cap ours, smoke within 2 km | 350 | 8.0% (5.3 to 10.9) | 5.2% (n 116) | 9.4% (n 234) | -4.2 (-9.7 to +1.5) |
| cap ours, cap_defended set for that cap | 153 | 35.9% (28.1 to 44.0) | 30.8% (n 52) | 38.6% (n 101) | -7.8 (-24.7 to +10.5) |
| cap ours, cap_defended not set for it | 541 | 7.4% (5.5 to 9.4) | 8.2% (n 208) | 6.9% (n 333) | +1.3 (-3.4 to +5.2) |

By map and cap (cap letter in the team frame):
| map | cap | n | enemy took it | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|---|
| Hotspot | A | 11 (small n) | 0.0% (0.0 to 0.0) | too few (n 7) | too few (n 4) | - |
| Hotspot | B | 44 | 9.1% (2.0 to 18.4) | 21.4% (n 14) | 3.3% (n 30) | +18.1 (+0.0 to +55.6) |
| Hotspot | C | 65 | 26.2% (16.4 to 37.8) | 23.8% (n 21) | 27.3% (n 44) | -3.5 (-25.2 to +19.6) |
| Hotspot | D | 84 | 23.8% (13.0 to 35.2) | 12.5% (n 24) | 28.3% (n 60) | -15.8 (-35.1 to +12.0) |
| Land of Fire | A | 53 | 20.8% (6.8 to 36.4) | 9.1% (n 11) | 23.8% (n 42) | -14.7 (-38.9 to +12.6) |
| Land of Fire | B | 68 | 11.8% (6.0 to 23.3) | 5.6% (n 36) | 18.8% (n 32) | -13.2 (-30.6 to +0.2) |
| Land of Fire | C | 5 | too few |  |  |  |
| Land of Fire | D | 26 | 7.7% (0.0 to 23.1) | 14.3% (n 14) | 0.0% (n 12) | +14.3 (+0.0 to +42.9) |
| Loop | A | 47 | 17.0% (5.6 to 29.2) | 0.0% (n 11) | 22.2% (n 36) | -22.2 (-37.1 to -7.5 *) |
| Loop | B | 30 | 20.0% (5.9 to 39.1) | 0.0% (n 10) | 30.0% (n 20) | -30.0 (-57.1 to -8.7 *) |
| Loop | C | 33 | 12.1% (2.8 to 28.6) | 5.6% (n 18) | 20.0% (n 15) | -14.4 (-45.0 to +6.1) |
| Mountain Range | A | 41 | 14.6% (6.0 to 28.0) | 5.3% (n 19) | 22.7% (n 22) | -17.5 (-41.7 to -2.3 *) |
| Mountain Range | B | 45 | 35.6% (25.5 to 51.5) | 33.3% (n 24) | 38.1% (n 21) | -4.8 (-33.9 to +20.0) |
| Mountain Range | C | 56 | 17.9% (6.8 to 30.2) | 8.0% (n 25) | 25.8% (n 31) | -17.8 (-36.4 to +4.2) |
| Okinawa | A | 39 | 15.4% (5.3 to 26.0) | too few (n 4) | 17.1% (n 35) | - |
| Okinawa | B | 8 (small n) | 12.5% (0.0 to 60.0) | too few (n 2) | too few (n 6) | - |
| Okinawa | C | 37 | 13.5% (2.9 to 26.7) | too few (n 7) | 13.3% (n 30) | - |
| Okinawa | D | 26 | 19.2% (4.3 to 36.4) | too few (n 3) | 17.4% (n 23) | - |
| Sea of Fortune | A | 12 (small n) | 8.3% (0.0 to 27.3) | too few (n 4) | 12.5% (n 8) | - |
| Sea of Fortune | B | 60 | 10.0% (1.9 to 19.2) | 25.0% (n 12) | 6.2% (n 48) | +18.8 (-7.1 to +50.0) |
| Sea of Fortune | C | 15 | 6.7% (0.0 to 23.1) | too few (n 7) | 12.5% (n 8) | - |
| Sea of Fortune | D | 41 | 17.1% (5.1 to 30.0) | 16.7% (n 18) | 17.4% (n 23) | -0.7 (-24.2 to +23.8) |
| Sleeping Giant | A | 90 | 21.1% (12.0 to 35.0) | 20.4% (n 49) | 22.0% (n 41) | -1.5 (-21.4 to +32.2) |
| Sleeping Giant | B | 46 | 8.7% (0.0 to 21.6) | 5.0% (n 20) | 11.5% (n 26) | -6.5 (-26.1 to +18.2) |
| Sleeping Giant | C | 16 | 18.8% (0.0 to 35.0) | too few (n 7) | 0.0% (n 9) | - |
| Sleeping Giant | D | 75 | 17.3% (6.8 to 26.9) | 22.9% (n 35) | 12.5% (n 40) | +10.4 (-13.0 to +29.6) |

For reference, "we took the nearest cap" (cap not ours at activation):
| group | n | we took it | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| all smokes where the nearest cap was not ours | 853 | 24.5% (21.0 to 27.9) | 28.4% (n 278) | 22.6% (n 575) | +5.8 (-1.7 to +14.4) |
| destroyer smokes | 582 | 27.0% (22.4 to 31.8) | 32.8% (n 198) | 24.0% (n 384) | +8.9 (-1.6 to +20.2) |
| within 2 km | 349 | 35.0% (29.1 to 40.5) | 39.1% (n 115) | 32.9% (n 234) | +6.2 (-3.5 to +18.5) |

Wrote enemy-took.csv (1547 rows).

Replays per game (primary + merged): {2: 170, 1: 1}

# C2: cap holder at 8:00 and winning

| map | games | covered at 8:00 (snapshot within 60 s) | ended before 8:00 | no snapshot within 60 s |
|---|---|---|---|---|
| Hotspot | 31 | 30 | 0 | 1 |
| Land of Fire | 25 | 23 | 1 | 1 |
| Loop | 23 | 19 | 2 | 2 |
| Mountain Range | 21 | 19 | 1 | 1 |
| Okinawa | 18 | 16 | 1 | 1 |
| Sea of Fortune | 21 | 19 | 0 | 2 |
| Sleeping Giant | 32 | 29 | 0 | 3 |
| all | 171 | 155 | 5 | 11 |
Distance of the snapshot used from 8:00: median 11 s, max 59 s. Covered games where both clans are Rest: 76; games with a Top 6 clan: 79.
Team strength model check (all 171 games): the favourite by the simple record model won 110 of 158; mean predicted for those 0.67. Bradley-Terry: favourite won 128 of 164, mean predicted 0.74.

## Hotspot  (30 games covered, 17 Rest-vs-Rest)
Caps in the team frame (own spawn at the bottom): A: enemy side (+4.7 km toward the enemy, left); B: own side (-4.7 km toward the enemy, left); C: middle (+0.0 km toward the enemy, centre); D: middle (+0.0 km toward the enemy, right)

All covered games (30 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (enemy side) | 9 (small n) | 6 (67%, 30 to 100) | 47% (n 51) | +20 (-20 to +56) | 4.9 | +12 pts (-21 to +42) | 4.8; +13 pts (-10 to +35) |
| B (own side) | 51 | 27 (53%, 47 to 59) | 33% (n 9) | +20 (-24 to +56) | 25.9 | +2 pts (-3 to +8) | 25.8; +2 pts (-1 to +7) |
| C (middle) | 28 | 20 (71%, 54 to 88) | 31% (n 32) | +40 (+10 to +70 *) | 15.4 | +16 pts (+1 to +30 *) | 17.3; +10 pts (-6 to +23) |
| D (middle) | 29 | 16 (55%, 37 to 72) | 45% (n 31) | +10 (-27 to +43) | 15.0 | +3 pts (-13 to +20) | 14.9; +4 pts (-11 to +17) |
| holds more caps than the enemy | 12 (small n) | 10 (83%, 60 to 100) | 17% (n 12) | +67 (+20 to +100 *) | 6.8 | +27 pts (+6 to +45 *) | 7.6; +20 pts (+0 to +37 *) |

(a) Rest-vs-Rest games only (17 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (enemy side) | 5 | too few |  |  |  |  |  |
| B (own side) | 29 | 17 (59%, 53 to 68) | 0% (n 5) | +59 (+53 to +68 *) | 14.7 | +8 pts (+2 to +16 *) | 15.3; +6 pts (+1 to +13 *) |
| C (middle) | 15 | 10 (67%, 43 to 88) | 37% (n 19) | +30 (-12 to +71) | 8.5 | +10 pts (-15 to +32) | 9.1; +6 pts (-15 to +27) |
| D (middle) | 16 | 9 (56%, 31 to 80) | 44% (n 18) | +12 (-35 to +59) | 8.6 | +2 pts (-21 to +23) | 8.9; +1 pts (-17 to +20) |
| holds more caps than the enemy | 10 (small n) | 8 (80%, 55 to 100) | 20% (n 10) | +60 (+0 to +100) | 5.5 | +25 pts (-3 to +47) | 6.3; +17 pts (-7 to +38) |

## Land of Fire  (23 games covered, 11 Rest-vs-Rest)
Caps in the team frame (own spawn at the bottom): A: middle (+0.0 km toward the enemy, left); B: middle (+0.0 km toward the enemy, left); C: enemy side (+4.7 km toward the enemy, right); D: own side (-4.7 km toward the enemy, right)

All covered games (23 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 18 | 14 (78%, 58 to 95) | 32% (n 28) | +46 (+14 to +74 *) | 10.4 | +20 pts (+2 to +38 *) | 11.4; +14 pts (-2 to +31) |
| B (middle) | 20 | 16 (80%, 60 to 95) | 27% (n 26) | +53 (+18 to +83 *) | 12.2 | +19 pts (+3 to +33 *) | 13.3; +13 pts (+1 to +25 *) |
| C (enemy side) | 12 (small n) | 5 (42%, 12 to 71) | 53% (n 34) | -11 (-51 to +27) | 5.6 | -5 pts (-31 to +22) | 5.6; -5 pts (-28 to +17) |
| D (own side) | 34 | 16 (47%, 38 to 57) | 58% (n 12) | -11 (-48 to +27) | 16.6 | -2 pts (-11 to +8) | 16.6; -2 pts (-9 to +6) |
| holds more caps than the enemy | 14 (small n) | 12 (86%, 64 to 100) | 14% (n 14) | +71 (+33 to +100 *) | 8.7 | +24 pts (+1 to +42 *) | 9.8; +16 pts (-5 to +32) |

(a) Rest-vs-Rest games only (11 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 10 (small n) | 7 (70%, 40 to 100) | 33% (n 12) | +37 (-18 to +82) | 5.9 | +11 pts (-18 to +35) | 6.7; +3 pts (-17 to +21) |
| B (middle) | 10 (small n) | 7 (70%, 40 to 100) | 33% (n 12) | +37 (-18 to +82) | 5.5 | +15 pts (-13 to +39) | 6.2; +8 pts (-10 to +26) |
| C (enemy side) | 8 (small n) | 4 (50%, 12 to 86) | 50% (n 14) | +0 (-55 to +59) | 3.6 | +5 pts (-26 to +33) | 3.6; +5 pts (-19 to +29) |
| D (own side) | 14 (small n) | 7 (50%, 29 to 69) | 50% (n 8) | +0 (-55 to +52) | 6.6 | +3 pts (-13 to +23) | 6.6; +3 pts (-10 to +18) |
| holds more caps than the enemy | 5 | too few |  |  |  |  |  |

## Loop  (19 games covered, 10 Rest-vs-Rest)
Caps in the team frame (own spawn at the bottom): A: middle (+0.0 km toward the enemy, left); B: middle (+0.0 km toward the enemy, right); C: middle (+0.0 km toward the enemy, right)

All covered games (19 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 17 | 7 (41%, 19 to 67) | 57% (n 21) | -16 (-54 to +27) | 8.2 | -7 pts (-28 to +14) | 7.9; -5 pts (-26 to +16) |
| B (middle) | 19 | 12 (63%, 42 to 84) | 37% (n 19) | +26 (-16 to +68) | 10.2 | +10 pts (-9 to +28) | 10.2; +9 pts (-12 to +28) |
| C (middle) | 14 (small n) | 6 (43%, 17 to 69) | 54% (n 24) | -11 (-53 to +32) | 8.3 | -16 pts (-39 to +6) | 8.6; -19 pts (-41 to +5) |
| holds more caps than the enemy | 14 (small n) | 7 (50%, 24 to 75) | 50% (n 14) | +0 (-53 to +54) | 8.3 | -9 pts (-34 to +15) | 8.5; -11 pts (-36 to +13) |

(a) Rest-vs-Rest games only (10 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 9 (small n) | 4 (44%, 11 to 78) | 55% (n 11) | -10 (-71 to +51) | 4.2 | -3 pts (-38 to +31) | 4.2; -2 pts (-40 to +36) |
| B (middle) | 10 (small n) | 6 (60%, 30 to 90) | 40% (n 10) | +20 (-40 to +80) | 5.1 | +9 pts (-25 to +40) | 4.8; +12 pts (-22 to +43) |
| C (middle) | 9 (small n) | 1 (11%, 0 to 33) | 82% (n 11) | -71 (-100 to -30 *) | 4.6 | -40 pts (-57 to -13 *) | 4.4; -38 pts (-62 to -6 *) |
| holds more caps than the enemy | 8 (small n) | 2 (25%, 0 to 60) | 75% (n 8) | -50 (-100 to +14) | 4.1 | -26 pts (-56 to +15) | 4.0; -25 pts (-59 to +15) |

## Mountain Range  (19 games covered, 8 Rest-vs-Rest)
Caps in the team frame (own spawn at the bottom): A: middle (-0.1 km toward the enemy, left); B: middle (+0.0 km toward the enemy, left); C: middle (+0.0 km toward the enemy, right)

All covered games (19 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 12 (small n) | 6 (50%, 22 to 80) | 50% (n 26) | +0 (-41 to +41) | 6.2 | -2 pts (-25 to +22) | 5.8; +2 pts (-20 to +25) |
| B (middle) | 17 | 11 (65%, 41 to 88) | 38% (n 21) | +27 (-16 to +65) | 9.2 | +11 pts (-10 to +31) | 9.4; +10 pts (-8 to +28) |
| C (middle) | 19 | 10 (53%, 32 to 74) | 47% (n 19) | +5 (-47 to +47) | 9.8 | +1 pts (-18 to +21) | 10.7; -4 pts (-21 to +14) |
| holds more caps than the enemy | 12 (small n) | 9 (75%, 46 to 100) | 25% (n 12) | +50 (+0 to +100) | 7.2 | +15 pts (-7 to +36) | 7.7; +10 pts (-8 to +29) |

(a) Rest-vs-Rest games only (8 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 5 | too few |  |  |  |  |  |
| B (middle) | 7 | too few |  |  |  |  |  |
| C (middle) | 8 (small n) | 4 (50%, 12 to 88) | 50% (n 8) | +0 (-75 to +75) | 3.3 | +9 pts (-18 to +39) | 3.2; +10 pts (-15 to +35) |
| holds more caps than the enemy | 4 | too few |  |  |  |  |  |

## Okinawa  (16 games covered, 11 Rest-vs-Rest)
Caps in the team frame (own spawn at the bottom): A: own side (-3.6 km toward the enemy, left); B: enemy side (+3.6 km toward the enemy, left); C: middle (+0.0 km toward the enemy, left); D: middle (+0.0 km toward the enemy, right)

All covered games (16 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (own side) | 22 | 12 (55%, 40 to 68) | 40% (n 10) | +15 (-29 to +58) | 11.5 | +2 pts (-11 to +17) | 11.6; +2 pts (-11 to +14) |
| B (enemy side) | 9 (small n) | 5 (56%, 17 to 88) | 48% (n 23) | +8 (-39 to +54) | 4.6 | +5 pts (-27 to +39) | 4.7; +4 pts (-27 to +35) |
| C (middle) | 15 | 6 (40%, 15 to 67) | 59% (n 17) | -19 (-62 to +25) | 6.5 | -3 pts (-27 to +20) | 6.0; +0 pts (-22 to +24) |
| D (middle) | 15 | 6 (40%, 14 to 67) | 59% (n 17) | -19 (-63 to +31) | 8.1 | -14 pts (-35 to +8) | 8.0; -14 pts (-34 to +8) |
| holds more caps than the enemy | 8 (small n) | 3 (38%, 0 to 71) | 62% (n 8) | -25 (-100 to +50) | 3.9 | -11 pts (-38 to +17) | 3.6; -8 pts (-35 to +19) |

(a) Rest-vs-Rest games only (11 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (own side) | 16 | 8 (50%, 33 to 67) | 50% (n 6) | +0 (-52 to +55) | 7.6 | +3 pts (-14 to +19) | 7.6; +3 pts (-12 to +19) |
| B (enemy side) | 6 | too few |  |  |  |  |  |
| C (middle) | 10 (small n) | 6 (60%, 30 to 90) | 42% (n 12) | +18 (-37 to +73) | 4.6 | +14 pts (-14 to +42) | 4.3; +17 pts (-8 to +43) |
| D (middle) | 10 (small n) | 4 (40%, 10 to 70) | 58% (n 12) | -18 (-73 to +45) | 5.5 | -15 pts (-46 to +15) | 5.5; -15 pts (-42 to +12) |
| holds more caps than the enemy | 4 | too few |  |  |  |  |  |

## Sea of Fortune  (19 games covered, 9 Rest-vs-Rest)
Caps in the team frame (own spawn at the bottom): A: enemy side (+7.2 km toward the enemy, left); B: own side (-7.2 km toward the enemy, left); C: middle (+0.0 km toward the enemy, left); D: middle (+0.0 km toward the enemy, right)

All covered games (19 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (enemy side) | 6 | too few |  |  |  |  |  |
| B (own side) | 32 | 16 (50%, 43 to 58) | 50% (n 6) | +0 (-51 to +54) | 16.3 | -1 pts (-8 to +6) | 16.5; -1 pts (-8 to +3) |
| C (middle) | 16 | 6 (38%, 17 to 60) | 59% (n 22) | -22 (-59 to +21) | 7.9 | -12 pts (-30 to +8) | 7.7; -11 pts (-27 to +7) |
| D (middle) | 17 | 12 (71%, 47 to 89) | 33% (n 21) | +37 (-5 to +76) | 9.5 | +15 pts (-3 to +32) | 10.2; +10 pts (-5 to +24) |
| holds more caps than the enemy | 15 | 8 (53%, 27 to 78) | 47% (n 15) | +7 (-47 to +56) | 8.1 | -0 pts (-22 to +19) | 8.6; -4 pts (-21 to +12) |

(a) Rest-vs-Rest games only (9 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (enemy side) | 3 | too few |  |  |  |  |  |
| B (own side) | 15 | 7 (47%, 36 to 57) | 67% (n 3) | -20 (-64 to +56) | 7.7 | -5 pts (-18 to +3) | 7.7; -4 pts (-16 to +3) |
| C (middle) | 8 (small n) | 3 (38%, 0 to 75) | 60% (n 10) | -22 (-78 to +45) | 4.0 | -12 pts (-37 to +13) | 3.8; -10 pts (-31 to +16) |
| D (middle) | 9 (small n) | 7 (78%, 44 to 100) | 22% (n 9) | +56 (-11 to +100) | 5.6 | +16 pts (-6 to +34) | 5.8; +13 pts (-11 to +31) |
| holds more caps than the enemy | 6 | too few |  |  |  |  |  |

## Sleeping Giant  (29 games covered, 10 Rest-vs-Rest)
Caps in the team frame (own spawn at the bottom): A: middle (+0.0 km toward the enemy, left); B: middle (+0.0 km toward the enemy, left); C: enemy side (+4.2 km toward the enemy, right); D: own side (-4.2 km toward the enemy, right)

All covered games (29 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 29 | 17 (59%, 41 to 76) | 41% (n 29) | +17 (-17 to +52) | 15.4 | +6 pts (-11 to +21) | 15.7; +4 pts (-9 to +17) |
| B (middle) | 16 | 10 (62%, 36 to 85) | 45% (n 42) | +17 (-15 to +49) | 8.3 | +10 pts (-10 to +31) | 9.1; +5 pts (-13 to +25) |
| C (enemy side) | 11 (small n) | 6 (55%, 23 to 85) | 49% (n 47) | +6 (-32 to +42) | 5.8 | +2 pts (-24 to +27) | 6.7; -7 pts (-30 to +16) |
| D (own side) | 47 | 24 (51%, 44 to 58) | 45% (n 11) | +6 (-29 to +42) | 23.8 | +1 pts (-5 to +6) | 24.7; -2 pts (-8 to +4) |
| holds more caps than the enemy | 17 | 12 (71%, 47 to 93) | 29% (n 17) | +41 (-8 to +83) | 10.1 | +11 pts (-10 to +30) | 11.9; +1 pts (-16 to +17) |

(a) Rest-vs-Rest games only (10 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| A (middle) | 10 (small n) | 5 (50%, 20 to 80) | 50% (n 10) | +0 (-60 to +60) | 4.8 | +2 pts (-27 to +31) | 4.5; +5 pts (-20 to +32) |
| B (middle) | 7 | too few |  |  |  |  |  |
| C (enemy side) | 4 | too few |  |  |  |  |  |
| D (own side) | 16 | 8 (50%, 38 to 64) | 50% (n 4) | +0 (-62 to +59) | 8.4 | -2 pts (-16 to +11) | 8.5; -3 pts (-18 to +8) |
| holds more caps than the enemy | 4 | too few |  |  |  |  |  |

## All maps pooled, by the cap's place in the team frame

All covered games (155 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| holds its own-side cap (maps that have one) | 186 | 95 (51%, 47 to 54) | 48% (n 124) | +3 (-6 to +12) | 93.9 | +1 pts (-3 to +4) | 95.2; -0 pts (-3 to +3) |
| holds the enemy-side cap (maps that have one) | 47 | 25 (53%, 38 to 66) | 49% (n 263) | +4 (-13 to +22) | 24.0 | +2 pts (-12 to +16) | 25.3; -1 pts (-12 to +10) |
| holds at least one middle cap | 232 | 132 (57%, 53 to 61) | 29% (n 78) | +27 (+14 to +40 *) | 121.0 | +5 pts (+2 to +8 *) | 125.1; +3 pts (+1 to +6 *) |
| holds every middle cap | 43 | 27 (63%, 47 to 77) | 48% (n 267) | +15 (-1 to +31) | 24.3 | +6 pts (-5 to +19) | 25.1; +4 pts (-5 to +14) |
| holds more caps than the enemy | 92 | 61 (66%, 57 to 76) | 34% (n 92) | +33 (+12 to +52 *) | 53.0 | +9 pts (+1 to +18 *) | 57.6; +4 pts (-4 to +12) |
| holds 2+ more caps than the enemy | 43 | 32 (74%, 61 to 87) | 46% (n 267) | +28 (+13 to +43 *) | 25.4 | +15 pts (+4 to +26 *) | 28.2; +9 pts (-0 to +18) |

(a) Rest-vs-Rest games only (76 games):
| cap (team frame) | holder team-games | holders won (rate, interval) | not holding: win rate | holding - not | team strength predicts (wins) | actual - expected | Bradley-Terry: expected; actual - expected |
|---|---|---|---|---|---|---|---|
| holds its own-side cap (maps that have one) | 90 | 47 (52%, 46 to 58) | 47% (n 62) | +5 (-8 to +18) | 45.0 | +2 pts (-3 to +7) | 45.6; +2 pts (-3 to +6) |
| holds the enemy-side cap (maps that have one) | 26 | 15 (58%, 40 to 76) | 48% (n 126) | +9 (-14 to +30) | 13.0 | +8 pts (-10 to +26) | 13.6; +5 pts (-10 to +22) |
| holds at least one middle cap | 119 | 64 (54%, 49 to 59) | 36% (n 33) | +17 (-4 to +38) | 61.6 | +2 pts (-2 to +6) | 62.6; +1 pts (-2 to +5) |
| holds every middle cap | 22 | 14 (64%, 44 to 85) | 48% (n 130) | +16 (-8 to +38) | 13.0 | +5 pts (-13 to +22) | 13.4; +3 pts (-13 to +17) |
| holds more caps than the enemy | 41 | 23 (56%, 40 to 71) | 44% (n 41) | +12 (-19 to +41) | 22.5 | +1 pts (-12 to +16) | 23.8; -2 pts (-14 to +11) |
| holds 2+ more caps than the enemy | 20 | 16 (80%, 60 to 95) | 45% (n 132) | +35 (+13 to +54 *) | 11.6 | +22 pts (+6 to +36 *) | 12.7; +17 pts (+3 to +29 *) |

Games level on caps at 8:00: 63 of 155. Caps held at 8:00 per team: {0: 11, 1: 105, 2: 155, 3: 37, 4: 2}
In Top 6 vs Rest games covered (54): the Top 6 clan held more caps at 8:00 in 31, fewer in 7; Top 6 won 47.
Teams holding more caps at 8:00 were already ahead on score at that moment in 67 of 92 (73%); median lead +97 points.
Reference: the team ahead on score at 8:00 won 122 of 154 (79%).
