# Module 3: what changed in round 4

Every number in MODULE-3.md that changed, old -> new. Numbers not listed are unchanged (checked by rerunning the round 3 definition on the corrected loader; outputs in `runs/`).

## Loader fix (detail records matched on game + smoke id)

Finding 4 (radar run or not, DD smokes with a radar ship inside)
- Smokes with a radar ship inside: 385 -> 387. Radar not run: 290 -> 292.
- Radar not run, cap taken: 44% of 200 -> 45% of 202.
- Hit an enemy DD, interval: +17 to +35 -> +17 to +34.
- Total concealed damage, interval: -0.7k to +7.5k -> -0.6k to +7.8k.
- Caps taken, interval: -6 to +21 -> -7 to +21.

Finding 6
- Radar pressed share, Top 6 minus Rest, interval: -1 to +17 -> +0 to +17.

Finding 7, round 3 definition (radar ship of any class inside, early stacked DD smokes), before the definition change below
- Rest: 62% of 85 -> 64% of 85 (53 -> 54 smokes). Difference +15 -> +13 points, interval +1 to +32 -> -2 to +30.
- Land of Fire, Rest: 5 of 11 -> 6 of 11.
- Early stacks, cap taken with vs without a radar ship: 53% of 89 vs 35% of 40 (+18, interval +0 to +35) -> 53% of 90 vs 33% of 39 (+20, interval +2 to +38).

## Definition change

Radar play = primary purpose is a radar play (was: any radar tag)
- DD radar plays: 100 -> 96. Radar traps: 27 -> 23. Cap control: 73, unchanged.
- Finding 1: Top 6 plays per team-game 0.50 -> 0.47; Rest 0.19 -> 0.19. Difference +0.31 -> +0.28, interval +0.14 to +0.44 -> +0.14 to +0.40. Smokes 55 and 45 -> 52 and 44.
- Finding 1: team-games with at least one radar play: Top 6 40% -> 38% (44 -> 42 of 110); Rest 17% -> 17% (40 -> 39 of 232).
- Finding 1: RESIN 17 plays in 24 games -> 14 in 24 (0.71 -> 0.58 per game). PN 2 plays in 7 games -> 1 in 7.
- Finding 2: three busiest maps 72 of 100 -> 69 of 96. Mountain Range 18 plays (0.43 per team-game) -> 15 (0.36). Loop 7 -> 6 (0.15 -> 0.13). "0.40 to 0.45 per team-game" -> 0.45, 0.40, 0.36.
- Finding 2: Mountain Range cap A 4 plays, all traps -> 1 play, a trap.
- Finding 3: radar traps n 27 -> 23; after minute 10: 56% -> 57%; median distance to the contested cap 6 km -> 7 km. Median time 10:06, unchanged.
- Finding 8: cruiser radar plays 22 -> 21 (Top 6 13 -> 12, Rest 9). BONKZ and HTDOG 11 -> 10. Mean concealed damage 11.0k -> 10.7k. Cap taken 25% of 12 -> 27% of 11. Mountain Range caps B and C: 7 of 22 -> 7 of 21.
- Fig 4 note: Des Moines 23 -> 19; a cruiser in a destroyer's smoke 84 of 100 -> 80 of 96.
- Fig 1 note and title: 100 and 22 smokes -> 96 and 21; 0.50 -> 0.47; map rates as above.

Radar partner = a radar cruiser inside the smoke (was: a radar ship of any class inside, early stacked DD smokes only)
- Finding 7 headline, all early DD smokes (new population): Top 6 60% of 102, Rest 35% of 200, +25 points (interval +13 to +36).
- Finding 7, early stacked DD smokes: Top 6 77% of 56 -> 75% of 56; Rest 62% (64% after the loader fix) -> 62% of 85; difference +15 -> +13, interval +1 to +32 -> -1 to +29.
- Sleeping Giant early stacks: 53% of 19 vs 80% of 20 (-27, interval -56 to +5) -> 53% of 19 vs 75% of 20 (-22, interval -50 to +9). All early smokes (new): 47% of 32 vs 59% of 37 (-13, interval -41 to +18).
- Hotspot early stacks: 92% of 12 vs 64% of 22, unchanged. All early smokes (new): 87% of 23 vs 38% of 45.
- Sea of Fortune early stacks, Top 6: 6 of 6 -> 5 of 6.
- Cap taken with vs without: early stacks 53% of 89 vs 35% of 40 (+18) -> 52% of 88 vs 37% of 41 (+16, interval -2 to +33). All early smokes (new): 61% of 120 vs 31% of 150 (+30, interval +21 to +38).
- PN: 3 of 3 early stacks, unchanged; 4 of 5 early DD smokes (new).
- Fig 3 now shows all early DD smokes with the radar cruiser definition (was early stacks, any radar ship).

## Wording (association, not cause)

- "For a player" lines in findings 1 to 5 and 7 now describe what the Top 6 do and what those smokes returned, not what to do to win.
- Finding 4 and 5 titles reworded ("goes with" kept, "the radar press adds little on top" and "that is where the numbers move" removed).
- Fig 2 alt text: "pay-off" -> "what the smokes returned".
