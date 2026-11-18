# Part D: clan styles

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
