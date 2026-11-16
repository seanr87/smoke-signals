# STEP 2: full-field analysis and sanity checks

Batch: output/20261116-132014 (16 Nov 2026). 341 runs over 171 games, every clan, frames on, no clips, --jobs 6. Wall time 1119 s (18.7 min). Failed runs: 0. Smokes kept: 1547 (round 6: 217). Flagged: 326.

Commits on full-field: abe7c409 (batch matches a team's replay by the lower-cased tag as well as the slug), 6dccb951 (smokes.csv, run_log.md, jobs.json, data zip of the batch; frames are 6188 PNGs, 2.1 GB, and smokes.json 23 MB and the per-game folders 74 MB stay out of git), 2e03e2a8 (export clan tables for every clan), 527aae2d (a clan's roster is read from its own run).

## 1. Original 45 games, 3 clans vs round 6

- smokes.csv: the 217 rows for H-SR, RESIN and PN are identical to round 6 in every field (164 columns, same order); no row added or lost. The run keeps only its own team's smokes, so smokes newly visible from the opponent's side belong to the opponent and appear as that clan's rows, not as changes to the original three.
- Data export (smokes, games, clans, clans-destroyer, breakdown, ship_class): same headers as round 6. ship_class.csv and breakdown.csv rows for the three clans are identical. games.csv rows for the 45 games keep every field except smokes_analysed, which now counts both teams' smokes, and one end clock (KITED vs H-SR, 10:17 to 10:16) because the game file read first is now KITED's run and the two replays' clocks differ by a second.
- One metric moved: H-SR charge use, 60.76% (158 charges carried) to 60.38% (159). Cause: the site tool read a game's roster from the first run of that game; in round 6 that was RESIN's run for the H-SR vs RESIN series, and the opponent's replay sees one H-SR ship with one charge fewer. The tool now reads a clan's roster from its own run; with that rule, round 6's own data gives 60.38% / 159 too, and every clan value for the three clans is identical between round 6 re-exported and this batch. No smoke definition or metric formula changed.

## 2. Dedupe rule

Both replays of a game are merged into one timeline before smokes are found, so a smoke laid in view of both recorders is one object (repeated consumable packets within 1 s are ignored by the merge). Each team's run keeps only the smokes whose owner is that team (smoke.team == run team), and each team runs once per game, so a smoke is written exactly once. Check: in all 170 two-replay games the two runs found the same number of smokes (1538 seen twice, counted once); 9 smokes come from the single-replay game (LB R1 KSC vs -BN- G3, -BN- side); no smoke was seen without being kept by exactly one run. 1538 + 9 = 1547.

## 3. Smokes found vs roster activations

Per team and game, smokes kept vs the roster's smoke_activations: 1547 found vs 1776 activations over 342 team-games; 87 team-games differ by more than 1 (72 with more activations than smokes, 15 with fewer). The activation counter is not a reliable "smokes used" figure: 83 ships show more activations than they carry charges (125 excess), because a use recorded by both replays more than 1 s apart (the clock offset between replays runs 1 to 5 s) is counted twice. The 15 cases with more smokes than activations are owner-attribution flags (a cloud with no activation packet in view, e.g. the single-replay game). The original three clans show the same gaps as in round 6 (e.g. H-SR 8073 G1 6 vs 4, 8183 G2 4 vs 2), so this is a known limit of the counter, not a regression. The full list is in the appendix.

## 4. Per clan

No clan has 0 smokes. Outliers worth a look before they go on a site: -BN- (90,868 concealed damage per game, 6.8 smokes per game, 26 of 95 flagged) and INCA (89,671 per game over only 6 games); MACH has 16 of 29 smokes flagged; KSE (4,712 per game) and RMN (5,206) are low; OGF and MANBA lay 1.5 smokes per game. Flags: 103 "no smoke activation within 5 s before creation" (owner inferred from position) and 223 "nearest ship 600 to 830 m from origin" (soft distance note); overall 21% flagged against 10% in round 6, driven by recorders that saw the opponent's smoke from further away. The table is in the appendix.

## 5. Runtime

341 runs, 1119 s with frames (3.3 s per run; the estimate was 45 min). One skip, as expected: KSC's run of LB R1 KSC vs -BN- G3 (no KSC replay). No errors.

## Appendix: sanity script output

```

# 1. Original 3 clans vs round 6
round 6 rows: 217; new rows for the 3 clans: 217; new rows total: 1547
rows in round 6 but not in new: 0
rows new for the 3 clans that round 6 did not have: 0
columns: round 6 164 new 164 same order: True
rows with any non-volatile field changed: 0 of 217

# 2. Dedupe: smokes seen per run vs kept
games with two runs: 170, with one run: 1
smokes seen in both runs of a game (counted once): 1538; total kept: 1547
games where the two runs saw a different number of smokes: 0
smokes seen but kept by neither run (no team or not the run's team): 0

# 3. Smokes found vs roster smoke activations, per game and team
team-games checked: 342; smokes found: 1547; roster activations: 1776
team-games off by more than 1 (match, game, team, found, activations, ships with smoke): 87
   (('7887', '1', 'EPOXY'), 3, 5, 2)
   (('7888', '1', 'INCA'), 11, 14, 4)
   (('7891', '1', 'KM'), 3, 1, 1)
   (('7892', '1', 'EPOXY'), 10, 7, 2)
   (('7896', '1', 'EPOXY'), 6, 4, 2)
   (('7898', '1', 'HFANS'), 6, 9, 3)
   (('7901', '1', 'INCA'), 13, 21, 4)
   (('7901', '1', 'RESIN'), 6, 8, 2)
   (('7903', '1', 'BONKZ'), 10, 17, 3)
   (('7903', '1', 'HFANS'), 14, 21, 5)
   (('7909', '1', 'BONKZ'), 4, 7, 3)
   (('7909', '1', 'RESIN'), 3, 5, 1)
   (('7912', '1', 'HFANS'), 6, 8, 2)
   (('7912', '1', 'KM'), 3, 5, 2)
   (('7914', '1', '-BN-'), 9, 12, 3)
   (('7914', '1', 'MACHX'), 3, 5, 2)
   (('7916', '1', 'SCCC2'), 2, 0, 1)
   (('7918', '1', 'MACH'), 4, 6, 1)
   (('7920', '1', 'SCCC2'), 3, 6, 1)
   (('7923', '1', 'MACH'), 8, 5, 3)
   (('7924', '1', '-BN-'), 6, 2, 4)
   (('7925', '1', 'BONKY'), 5, 8, 3)
   (('7925', '1', 'KITED'), 4, 7, 3)
   (('7926', '1', 'SCCC2'), 10, 16, 3)
   (('7928', '1', 'MACH'), 2, 4, 1)
   (('7931', '1', '-BN-'), 5, 7, 4)
   (('7932', '1', 'MACH'), 7, 12, 3)
   (('7933', '1', 'KITED'), 8, 12, 5)
   (('7936', '1', 'MACHX'), 10, 13, 5)
   (('7937', '1', '-BN-'), 11, 17, 5)
   (('7937', '1', 'KITED'), 2, 4, 2)
   (('7939', '1', 'MACHX'), 5, 10, 2)
   (('7939', '1', 'SCCC2'), 14, 23, 4)
   (('7940', '1', 'BONKY'), 3, 1, 1)
   (('7940', '1', 'NGA'), 5, 7, 2)
   (('7941', '1', 'BTLST'), 5, 8, 4)
   (('7945', '1', 'BTLST'), 5, 8, 3)
   (('7946', '1', 'RMN'), 4, 8, 3)
   (('7957', '1', 'BTLST'), 9, 13, 3)
   (('7959', '1', '5D'), 4, 7, 3)
   (('7959', '1', 'RMN'), 3, 5, 2)
   (('7960', '1', 'MZY'), 3, 1, 1)
   (('7961', '1', 'KITE'), 5, 9, 2)
   (('7967', '1', 'OGF'), 2, 4, 1)
   (('7971', '1', 'KSE'), 3, 5, 1)
   (('7971', '1', 'PFANS'), 5, 8, 3)
   (('7975', '1', 'UYSC'), 4, 6, 3)
   (('7976', '1', 'KSE'), 2, 4, 2)
   (('7976', '1', 'VRTUS'), 7, 10, 3)
   (('7980', '1', 'KSE'), 3, 6, 2)
   (('7980', '1', 'UYSC'), 6, 11, 4)
   (('7984', '1', 'RSR'), 4, 6, 2)
   (('7984', '1', 'UYSC'), 7, 12, 5)
   (('7987', '1', 'UYSC'), 10, 17, 5)
   (('7989', '1', 'KSE'), 5, 9, 3)
   (('7990', '1', 'UYSC'), 3, 6, 4)
   (('7990', '1', 'VRTUS'), 8, 12, 3)
   (('7993', '1', 'UYSC'), 5, 9, 4)
   (('8068', '3', 'MZY'), 5, 3, 2)
   (('8072', '2', 'KSC'), 8, 6, 3)
   (('8073', '1', 'H-SR'), 6, 4, 3)
   (('8074', '1', 'HFANS'), 6, 8, 3)
   (('8074', '2', 'HFANS'), 10, 15, 6)
   (('8074', '2', 'HTDOG'), 11, 15, 4)
   (('8074', '3', 'HFANS'), 5, 7, 3)
   (('8074', '3', 'HTDOG'), 7, 9, 3)
   (('8139', '1', 'KITED'), 3, 5, 2)
   (('8139', '2', 'KITED'), 6, 10, 3)
   (('8141', '3', '-BN-'), 9, 5, 2)
   (('8142', '1', 'EPOXY'), 5, 3, 3)
   (('8143', '1', 'MACHX'), 13, 23, 5)
   (('8143', '1', 'VRTUS'), 15, 20, 5)
   (('8144', '1', 'MZY'), 3, 1, 2)
   (('8146', '1', 'HTDOG'), 7, 11, 2)
   (('8151', '3', 'H-SR'), 7, 9, 4)
   (('8152', '1', '-BN-'), 3, 5, 3)
   (('8152', '1', 'MZY'), 3, 5, 2)
   (('8153', '2', 'HTDOG'), 6, 10, 2)
   (('8154', '1', 'HFANS'), 5, 8, 4)
   (('8154', '1', 'MZY'), 3, 5, 3)
   (('8154', '2', 'HFANS'), 5, 7, 3)
   (('8154', '2', 'MZY'), 3, 5, 2)
   (('8174', '1', 'EPOXY'), 8, 12, 3)
   (('8174', '1', 'MZY'), 5, 7, 2)
   (('8175', '2', 'BONKZ'), 6, 9, 2)
   (('8175', '2', 'HTDOG'), 4, 7, 2)
   (('8183', '2', 'H-SR'), 4, 2, 3)
  found > activations: 15; found < activations: 72

# 4. Per clan
| clan | games | smokes | DD smokes | smokes/game | concealed dmg/game | flagged |
|---|---|---|---|---|---|---|
| HFANS | 17 | 110 | 79 | 6.5 | 55,386 | 19 |
| HTDOG | 18 | 106 | 46 | 5.9 | 49,662 | 29 |
| RESIN | 24 | 103 | 87 | 4.3 | 51,866 | 8 |
| BONKZ | 21 | 102 | 76 | 4.9 | 66,346 | 15 |
| H-SR | 22 | 100 | 89 | 4.5 | 67,832 | 12 |
| -BN- | 14 | 95 | 67 | 6.8 | 90,868 | 26 |
| VRTUS | 11 | 82 | 46 | 7.5 | 65,033 | 20 |
| EPOXY | 17 | 82 | 68 | 4.8 | 50,477 | 22 |
| MACHX | 14 | 82 | 49 | 5.9 | 56,148 | 14 |
| KITED | 14 | 63 | 25 | 4.5 | 23,003 | 14 |
| KSC | 11 | 59 | 47 | 5.4 | 62,419 | 22 |
| REEEE | 13 | 52 | 44 | 4.0 | 29,797 | 9 |
| MZY | 19 | 50 | 43 | 2.6 | 21,181 | 13 |
| SCCC2 | 7 | 48 | 32 | 6.9 | 55,757 | 16 |
| KITE | 14 | 45 | 43 | 3.2 | 24,271 | 12 |
| INCA | 6 | 39 | 20 | 6.5 | 89,671 | 10 |
| 5D | 10 | 37 | 17 | 3.7 | 20,824 | 1 |
| UYSC | 7 | 36 | 22 | 5.1 | 22,784 | 3 |
| BONKY | 7 | 36 | 25 | 5.1 | 49,243 | 9 |
| BTLST | 6 | 34 | 17 | 5.7 | 27,185 | 3 |
| MACH | 7 | 29 | 18 | 4.1 | 16,062 | 16 |
| NGA | 7 | 28 | 17 | 4.0 | 19,164 | 6 |
| RSR | 7 | 26 | 18 | 3.7 | 24,207 | 11 |
| PFANS | 12 | 24 | 18 | 2.0 | 33,294 | 4 |
| KSE | 7 | 20 | 15 | 2.9 | 4,712 | 1 |
| KM | 5 | 15 | 10 | 3.0 | 37,032 | 7 |
| PN | 7 | 14 | 10 | 2.0 | 16,598 | 2 |
| RMN | 6 | 12 | 11 | 2.0 | 5,206 | 1 |
| OGF | 6 | 9 | 9 | 1.5 | 9,217 | 0 |
| MANBA | 6 | 9 | 5 | 1.5 | 12,454 | 1 |
smoker_class values: Counter({'destroyer': 1073, 'cruiser': 440, 'battleship': 34})

# 5. Runtime and failures
- runs: 341
- failed runs: 0
- smokes kept: 1547
- flagged smokes: 326
- wall time: 1119 s
errors: 0
skip lines: []
```
