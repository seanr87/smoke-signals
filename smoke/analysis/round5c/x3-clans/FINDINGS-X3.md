# Round 5c, worker x3: item 8 (D1 to D3, clan styles)

Batch `output/20261117-230933`: 1,547 smokes, 171 games, 30 clans (24 with 7+ games; BTLST, INCA, MANBA, OGF, RMN, KM have 5 or 6 and are flagged). Everything here is association. Styles describe what clans do; they do not explain winning.

What is new against round 5b, in one place:
- **Two death scores, side by side.** "Died" = a ship the smoke covered (the smoker, or a ship inside or behind it) died between activation and 20 s after the smoke dispersed; each dead ship is counted once. "Caught" = the batch list of ships that died while the smoke concealed them or just after it cleared around them (round 5's deaths). All smokes: 259 ships died (16.8 per 100) against 177 caught (11.4 per 100). "Died" leaves out 9 smokes of the one single-replay game, laid by the team with no replay (clans -BN-, KSC); they stay in "caught".
- **Caps come from the cap timeline**, on one fixed cap per smoke, up to 60 s after the smoke dispersed. "Taken" = the cap changed to the smoking clan (of smokes where it was not already theirs). "Not lost" = the enemy did not take it (of smokes inside or within 2 km of that cap, where the cap was not the enemy's). Both are given for the nearest cap and for the contested cap. My choice: for the contested-cap "not lost" the 2 km rule is measured to the contested cap.
- **Dropped from every table:** `cap_won`, `cap_def`, `we_took`, `enemy_took` (the round 5 snapshot fields) and the scores built on them: `took_pct`, `held_pct`, `deaths_per100`, `cap_won_pg`, `cap_def_pg`, `deaths_pg`.
- **Time scores use the replay clock** (`e0`, seconds since battle start at activation), not the HUD clock: first smoke of the game, share after 12:00, share before 5:00.
- Lineup, who, where and movement scores are untouched and identical to round 5b. Clan intervals are 95%, from resampling that clan's own games; Top 6 minus Rest intervals resample whole clans; a star means the interval excludes zero. Rates with fewer than 8 cases read "too few"; 8 to 14 is "small n".

### D1. Score every clan on the six dimensions ("what it buys" redone)

**Answer:** Done for all 30 clans (six flagged). Top 6 smokes went with fewer deaths on both death scores (died 12.3 against 19.3 per 100 smokes; caught 7.8 against 13.4), and from the timeline the Top 6 took the cap more often (39% against 28% on the nearest cap). "Not lost" is clear on the contested cap only.

**Numbers:** lowest clan, middle clan and highest clan among the 24 with 7+ games (only clans with 8+ cases are ranked).

| Score | Lowest | Median | Highest | Clans ranked |
|---|---|---|---|---|
| First smoke of the game (median, s) | 2:00 (H-SR) | 3:07 | 4:30 (MZY) | 24 |
| Smokes after 12:00 (%) | 0% (5D, MACH, NGA, RSR) | 9% | 25% (REEEE) | 24 |
| Concealed damage per game | 3,801 (KSE) | 42,794 | 88,963 (-BN-) | 24 |
| Concealed damage per smoke | 1,330 (KSE) | 8,687 | 16,378 (PFANS) | 24 |
| Died per 100 smokes | 6.0 (H-SR) | 16.3 | 50.0 (PN) | 24 |
| Caught per 100 smokes | 4.0 (H-SR) | 11.1 | 32.4 (5D) | 24 |
| Smoker died per 100 smokes | 3.8 (REEEE) | 11.7 | 40.0 (KSE) | 24 |
| Smoker caught per 100 smokes | 1.6 (KSC) | 6.6 | 27.8 (UYSC) | 24 |
| Nearest cap taken (% of smokes where it was not ours) | 9% (BONKY) | 31% | 56% (H-SR) | 24 |
| Contested cap taken (% of smokes where it was not ours) | 4% (NGA) | 26% | 44% (BONKZ) | 24 |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 62% (PFANS) | 86% | 100% (MACH) | 21 |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 50% (PFANS) | 80% | 100% (MACH) | 21 |
| Nearest caps taken with a smoke per game | 0.1 (PN) | 0.7 | 1.1 (MACHX) | 24 |
| Contested caps taken with a smoke per game | 0.1 (NGA, PN) | 0.7 | 1.1 (-BN-, BONKZ) | 24 |

The "died" score runs higher than "caught" for almost every clan (middle clan: 1.4 times as high), because it also counts ships that died in the 20 s after the smoke had gone and ships the batch did not list as concealed at death.

Deaths per 100 smokes, per clan: value (95% interval), percentile among the 24 clans. High percentile = more deaths.

| Clan | Games | Smokes | Died per 100 | Caught per 100 | Smoker died per 100 | Smoker caught per 100 |
|---|---|---|---|---|---|---|
| *RESIN | 24 | 103 | 17.5 (9.9 to 25.6) p57 | 7.8 (2.9 to 13.3) p22 | 9.7 (5.3 to 14.5) p39 | 1.9 (0.0 to 4.9) p4 |
| *H-SR | 22 | 100 | 6.0 (1.2 to 11.2) p0 | 4.0 (0.0 to 8.9) p0 | 4.0 (0.9 to 7.5) p4 | 2.0 (0.0 to 4.9) p9 |
| *BONKZ | 21 | 102 | 17.6 (10.3 to 25.8) p61 | 11.8 (5.9 to 17.8) p57 | 12.7 (6.9 to 20.0) p57 | 6.9 (2.4 to 12.7) p52 |
| MZY | 19 | 50 | 22.0 (10.2 to 39.5) p65 | 14.0 (3.2 to 28.8) p74 | 14.0 (5.0 to 24.4) p61 | 8.0 (0.0 to 17.5) p65 |
| *HTDOG | 18 | 106 | 10.4 (4.1 to 17.4) p17 | 6.6 (2.1 to 12.2) p9 | 8.5 (3.4 to 15.0) p30 | 5.7 (1.9 to 10.4) p30 |
| EPOXY | 17 | 82 | 15.9 (7.5 to 26.7) p43 | 12.2 (5.0 to 21.9) p61 | 9.8 (3.9 to 17.5) p43 | 6.1 (2.0 to 10.8) p37 |
| HFANS | 17 | 110 | 13.6 (6.9 to 22.6) p35 | 10.0 (4.0 to 18.6) p39 | 10.9 (5.0 to 18.5) p48 | 6.4 (2.5 to 11.9) p48 |
| -BN- | 14 | 91 | 11.6 (5.8 to 18.6) p30 | 9.9 (4.3 to 18.5) p35 | 8.1 (2.7 to 14.7) p26 | 5.5 (1.1 to 11.8) p26 |
| *KITE | 14 | 45 | 11.1 (2.6 to 21.2) p26 | 8.9 (2.4 to 15.9) p30 | 6.7 (0.0 to 16.7) p17 | 4.4 (0.0 to 10.8) p17 |
| KITED | 14 | 63 | 15.9 (6.2 to 25.9) p48 | 12.7 (3.2 to 22.4) p70 | 14.3 (5.3 to 23.5) p65 | 11.1 (3.1 to 20.4) p87 |
| MACHX | 14 | 82 | 9.8 (4.4 to 15.6) p11 | 6.1 (1.5 to 11.0) p4 | 8.5 (2.9 to 14.7) p35 | 6.1 (1.5 to 11.0) p37 |
| REEEE | 13 | 52 | 7.7 (0.0 to 18.4) p4 | 7.7 (0.0 to 18.4) p17 | 3.8 (0.0 to 10.8) p0 | 3.8 (0.0 to 10.8) p13 |
| PFANS | 12 | 24 | 16.7 (0.0 to 37.5) p52 | 12.5 (0.0 to 30.0) p65 | 12.5 (0.0 to 30.0) p52 | 8.3 (0.0 to 26.7) p72 |
| KSC | 11 | 63 | 15.3 (6.8 to 22.7) p39 | 11.1 (4.8 to 17.0) p50 | 6.8 (2.0 to 12.5) p22 | 1.6 (0.0 to 4.8) p0 |
| *VRTUS | 11 | 82 | 9.8 (3.4 to 16.7) p11 | 8.5 (1.1 to 16.9) p26 | 6.1 (1.9 to 10.1) p9 | 4.9 (0.0 to 10.8) p22 |
| 5D | 10 | 37 | 37.8 (24.1 to 48.8) p87 | 32.4 (20.9 to 43.8) p100 | 32.4 (21.6 to 41.2) p87 | 27.0 (18.8 to 35.3) p96 |
| BONKY | 7 | 36 | 22.2 (8.5 to 38.5) p70 | 11.1 (3.3 to 19.4) p50 | 19.4 (6.2 to 37.9) p74 | 8.3 (0.0 to 16.7) p72 |
| KSE | 7 | 20 | 45.0 (29.2 to 68.4) p96 | 15.0 (4.5 to 27.3) p83 | 40.0 (19.2 to 66.7) p100 | 10.0 (0.0 to 25.0) p78 |
| MACH | 7 | 29 | 27.6 (11.4 to 52.4) p78 | 6.9 (0.0 to 18.2) p13 | 24.1 (11.4 to 42.9) p78 | 6.9 (0.0 to 18.2) p57 |
| NGA | 7 | 28 | 25.0 (11.1 to 38.5) p74 | 14.3 (6.5 to 22.2) p78 | 17.9 (6.9 to 29.6) p70 | 10.7 (3.4 to 17.9) p83 |
| PN | 7 | 14 | 50.0 (20.0 to 75.0) p100 | 28.6 (7.1 to 50.0) p96 | 28.6 (11.1 to 50.0) p83 | 7.1 (0.0 to 22.2) p61 |
| RSR | 7 | 26 | 38.5 (27.3 to 50.0) p91 | 19.2 (0.0 to 32.1) p87 | 38.5 (27.3 to 50.0) p96 | 19.2 (0.0 to 32.1) p91 |
| SCCC2 | 7 | 48 | 10.4 (3.7 to 19.6) p22 | 10.4 (3.7 to 19.6) p43 | 6.2 (1.8 to 12.5) p13 | 6.2 (1.8 to 12.5) p43 |
| UYSC | 7 | 36 | 33.3 (17.2 to 53.3) p83 | 27.8 (9.4 to 50.0) p91 | 33.3 (17.2 to 53.3) p91 | 27.8 (9.4 to 50.0) p100 |
| BTLST (flag) | 6 | 34 | 26.5 (10.0 to 55.6) p76 | 23.5 (9.1 to 50.0) p89 | 26.5 (10.0 to 55.6) p80 | 17.6 (5.4 to 37.0) p89 |
| INCA (flag) | 6 | 39 | 12.8 (8.7 to 22.2) p33 | 7.7 (1.8 to 18.8) p17 | 12.8 (8.7 to 22.2) p59 | 7.7 (1.8 to 18.8) p63 |
| MANBA (flag) | 6 | 9 | 22.2 (0.0 to 40.0) p70 | 22.2 (0.0 to 40.0) p89 | 0.0 (0.0 to 0.0) p0 | 0.0 (0.0 to 0.0) p0 |
| OGF (flag) | 6 | 9 | 66.7 (54.5 to 85.7) p100 | 33.3 (9.1 to 71.4) p100 | 55.6 (37.5 to 75.0) p100 | 22.2 (0.0 to 54.5) p93 |
| RMN (flag) | 6 | 12 | 33.3 (18.2 to 50.0) p83 | 33.3 (18.2 to 50.0) p100 | 25.0 (9.1 to 45.5) p80 | 25.0 (9.1 to 45.5) p93 |
| KM (flag) | 5 | 15 | 20.0 (0.0 to 30.0) p63 | 13.3 (0.0 to 25.0) p72 | 13.3 (0.0 to 25.0) p59 | 13.3 (0.0 to 25.0) p89 |

Caps from the timeline, per clan: value (95% interval), percentile, n = smokes the rate applies to.

| Clan | Nearest cap taken % | Contested cap taken % | Nearest cap not lost % | Contested cap not lost % | Nearest caps taken per game | Contested caps taken per game |
|---|---|---|---|---|---|---|
| *RESIN | 32 (22 to 45) p57, n 56 | 27 (19 to 37) p57, n 70 | 75 (60 to 92) p10, n 32 | 74 (62 to 87) p20, n 38 | 0.7 (0.5 to 0.9) p52 | 0.7 (0.5 to 0.9) p52 |
| *H-SR | 56 (46 to 69) p100, n 50 | 42 (33 to 52) p96, n 65 | 86 (74 to 96) p50, n 37 | 86 (73 to 96) p70, n 44 | 1.1 (0.9 to 1.5) p96 | 1.1 (0.8 to 1.4) p91 |
| *BONKZ | 53 (35 to 72) p96, n 45 | 44 (30 to 62) p100, n 61 | 88 (80 to 97) p65, n 43 | 83 (73 to 93) p55, n 48 | 1.0 (0.7 to 1.3) p87 | 1.1 (0.8 to 1.4) p98 |
| MZY | 39 (18 to 62) p83, n 31 | 33 (15 to 53) p87, n 33 | 79 (62 to 100) p20, n 14, small n | 79 (58 to 100) p42, n 14, small n | 0.5 (0.2 to 0.9) p26 | 0.5 (0.2 to 0.8) p22 |
| *HTDOG | 30 (17 to 48) p48, n 53 | 27 (15 to 40) p52, n 60 | 85 (66 to 100) p40, n 33 | 88 (72 to 100) p80, n 41 | 0.7 (0.4 to 1.1) p65 | 0.7 (0.4 to 1.1) p70 |
| EPOXY | 36 (21 to 55) p78, n 36 | 30 (18 to 45) p74, n 50 | 76 (66 to 88) p15, n 29 | 69 (55 to 83) p15, n 29 | 0.6 (0.4 to 0.9) p48 | 0.7 (0.4 to 1.0) p48 |
| HFANS | 28 (19 to 39) p39, n 61 | 21 (13 to 31) p39, n 76 | 82 (71 to 94) p35, n 40 | 77 (61 to 90) p30, n 35 | 0.9 (0.6 to 1.2) p83 | 0.8 (0.5 to 1.2) p78 |
| -BN- | 31 (18 to 46) p52, n 54 | 29 (16 to 44) p65, n 63 | 96 (90 to 100) p95, n 26 | 84 (67 to 96) p60, n 25 | 1.1 (0.6 to 1.5) p91 | 1.1 (0.6 to 1.6) p98 |
| *KITE | 45 (25 to 65) p91, n 22 | 38 (19 to 60) p91, n 26 | 88 (58 to 100) p58, n 16 | 88 (57 to 100) p75, n 16 | 0.6 (0.3 to 1.1) p43 | 0.6 (0.3 to 1.1) p43 |
| KITED | 25 (11 to 41) p35, n 32 | 15 (7 to 28) p22, n 46 | 96 (89 to 100) p90, n 23 | 94 (83 to 100) p95, n 18 | 0.6 (0.3 to 0.9) p33 | 0.5 (0.2 to 0.8) p26 |
| MACHX | 36 (21 to 51) p74, n 53 | 28 (16 to 44) p61, n 61 | 81 (63 to 95) p25, n 27 | 80 (65 to 94) p50, n 25 | 1.1 (0.7 to 1.6) p100 | 1.1 (0.6 to 1.6) p87 |
| REEEE | 23 (4 to 38) p22, n 30 | 20 (3 to 33) p35, n 35 | 71 (41 to 94) p5, n 17 | 65 (38 to 89) p10, n 20 | 0.4 (0.1 to 0.8) p17 | 0.4 (0.1 to 0.8) p17 |
| PFANS | 24 (8 to 43) p28, n 17 | 19 (6 to 38) p30, n 21 | 62 (25 to 100) p0, n 8, small n | 50 (14 to 88) p0, n 8, small n | 0.3 (0.1 to 0.6) p13 | 0.3 (0.1 to 0.6) p13 |
| KSC | 29 (17 to 45) p43, n 34 | 25 (16 to 33) p46, n 44 | 89 (77 to 100) p70, n 18 | 78 (58 to 94) p35, n 18 | 0.8 (0.5 to 1.2) p72 | 0.9 (0.6 to 1.2) p83 |
| *VRTUS | 24 (14 to 40) p28, n 51 | 18 (11 to 31) p26, n 60 | 93 (85 to 100) p85, n 28 | 85 (75 to 100) p65, n 26 | 0.8 (0.5 to 1.1) p72 | 0.7 (0.5 to 1.0) p74 |
| 5D | 35 (19 to 57) p65, n 23 | 32 (17 to 53) p80, n 25 | 82 (47 to 100) p30, n 17 | 76 (42 to 100) p25, n 17 | 0.6 (0.3 to 0.9) p39 | 0.6 (0.3 to 0.9) p39 |
| BONKY | 9 (0 to 23) p0, n 23 | 14 (5 to 24) p15, n 28 | 88 (50 to 100) p58, n 8, small n | 89 (57 to 100) p90, n 9, small n | 0.3 (0.0 to 0.6) p7 | 0.6 (0.1 to 1.0) p33 |
| KSE | 33 (13 to 54) p61, n 15 | 29 (12 to 44) p70, n 17 | too few (n 7) | too few (n 6) | 0.7 (0.3 to 1.0) p59 | 0.7 (0.3 to 1.0) p61 |
| MACH | 16 (0 to 25) p13, n 19 | 11 (0 to 25) p9, n 19 | 100 (100 to 100) p100, n 12, small n | 100 (100 to 100) p100, n 13, small n | 0.4 (0.0 to 0.9) p22 | 0.3 (0.0 to 0.7) p9 |
| NGA | 10 (0 to 35) p4, n 20 | 4 (0 to 14) p0, n 23 | too few (n 7) | too few (n 7) | 0.3 (0.0 to 0.9) p7 | 0.1 (0.0 to 0.4) p2 |
| PN | 12 (0 to 67) p9, n 8, small n | 8 (0 to 33) p4, n 12, small n | too few (n 5) | too few (n 4) | 0.1 (0.0 to 0.4) p0 | 0.1 (0.0 to 0.4) p2 |
| RSR | 36 (18 to 53) p70, n 14, small n | 25 (8 to 50) p46, n 20 | 91 (50 to 100) p78, n 11, small n | 62 (33 to 89) p5, n 8, small n | 0.7 (0.3 to 1.3) p59 | 0.7 (0.3 to 1.3) p61 |
| SCCC2 | 16 (3 to 41) p17, n 25 | 14 (3 to 33) p15, n 28 | 91 (75 to 100) p78, n 22 | 88 (76 to 100) p85, n 25 | 0.6 (0.1 to 1.1) p33 | 0.6 (0.1 to 1.1) p33 |
| UYSC | 43 (22 to 59) p87, n 23 | 32 (8 to 55) p80, n 25 | 86 (64 to 100) p45, n 14, small n | 79 (55 to 100) p42, n 14, small n | 0.9 (0.3 to 1.4) p78 | 0.7 (0.1 to 1.4) p61 |
| BTLST (flag) | 33 (13 to 54) p61, n 18 | 26 (10 to 47) p50, n 23 | 69 (47 to 100) p2, n 13, small n | 57 (31 to 85) p2, n 14, small n | 0.8 (0.3 to 1.3) p76 | 0.8 (0.3 to 1.3) p80 |
| INCA (flag) | 41 (29 to 67) p85, n 17 | 35 (25 to 47) p89, n 20 | 82 (67 to 94) p30, n 17 | 69 (45 to 89) p12, n 16 | 1.0 (0.5 to 1.5) p87 | 1.0 (0.5 to 1.5) p85 |
| MANBA (flag) | too few (n 4) | too few (n 6) | too few (n 4) | too few (n 3) | 0.2 (0.0 to 0.5) p2 | 0.3 (0.0 to 0.7) p13 |
| OGF (flag) | too few (n 7) | 0 (0 to 0) p0, n 8, small n | too few (n 4) | too few (n 5) | 0.0 (0.0 to 0.0) p0 | 0.0 (0.0 to 0.0) p0 |
| RMN (flag) | too few (n 6) | 10 (0 to 38) p7, n 10, small n | too few (n 4) | too few (n 2) | 0.2 (0.0 to 0.5) p2 | 0.2 (0.0 to 0.5) p7 |
| KM (flag) | too few (n 6) | 7 (0 to 27) p2, n 14, small n | too few (n 5) | too few (n 0) | 0.4 (0.0 to 0.8) p20 | 0.2 (0.0 to 0.6) p7 |

Smokes the cap rates apply to, all clans: nearest cap taken 853, contested cap taken 1,049, nearest cap not lost 541, contested cap not lost 548 (of 1,547).

**Top 6 or Shared:** Top 6 minus Rest on the "what it buys" scores (pooled over each group's games; 95% interval, whole clans resampled).

| Score | Top 6 | Rest | n (Top 6 / Rest) | Gap (95%) | Reading | Same gap with the library helper `boot_diff` |
|---|---|---|---|---|---|---|
| Concealed damage per smoke | 11,685 | 8,515 | 110 / 232 games | +570.1 to +5,690.5 * | Top 6 | - |
| Concealed damage per game | 57,152 | 37,034 | 110 / 232 games | +5,334.5 to +33,896.9 * | Top 6 | - |
| Nearest cap taken (% of smokes where it was not ours) | 39 | 28 | 277 / 576 | +0.5 to +21.5 * | Top 6 | +0.0 to +22.5 * |
| Contested cap taken (% of smokes where it was not ours) | 32 | 23 | 342 / 707 | +1.1 to +17.6 * | Top 6 | +1.5 to +18.4 * |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 86 | 83 | 189 / 352 | -3.3 to +8.6 | Shared | -3.4 to +9.3 |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 84 | 76 | 213 / 335 | +1.9 to +15.3 * | Top 6 | +1.2 to +13.7 * |
| Died per 100 smokes | 12.3 | 19.3 | 538 / 1000 | -13.3 to -2.6 * | Top 6 | -13.1 to -1.9 * |
| Caught per 100 smokes | 7.8 | 13.4 | 538 / 1009 | -9.5 to -2.9 * | Top 6 | -9.2 to -2.3 * |
| Smoker died per 100 smokes | 8.2 | 15.1 | 538 / 1000 | -12.3 to -3.2 * | Top 6 | -12.2 to -2.9 * |
| Smoker caught per 100 smokes | 4.3 | 9.2 | 538 / 1009 | -8.6 to -2.5 * | Top 6 | -8.4 to -2.1 * |
| Nearest caps taken with a smoke per game | 0.8 | 0.6 | 110 / 232 games | +0.04 to +0.44 * | Top 6 | - |
| Contested caps taken with a smoke per game | 0.9 | 0.6 | 110 / 232 games | +0.05 to +0.46 * | Top 6 | - |
| Ships died per game | 0.6 | 0.8 | 110 / 232 games | -0.49 to -0.03 * | Top 6 | - |
| Ships caught per game | 0.4 | 0.6 | 110 / 232 games | -0.37 to -0.06 * | Top 6 | - |

- Deaths: Top 6 clearly lower on all four. Died per 100: 12.3 against 19.3 (-13.3 to -2.6 *). Caught per 100: 7.8 against 13.4 (-9.5 to -2.9 *). Smoker only: died 8.2 against 15.1 (-12.3 to -3.2 *); caught 4.3 against 9.2 (-8.6 to -2.5 *).
- Caps taken: nearest cap 39% against 28% (+0.5 to +21.5 *); contested cap 32% against 23% (+1.1 to +17.6 *). Clear: Nearest cap taken (% of smokes where it was not ours), Contested cap taken (% of smokes where it was not ours), Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's), Nearest caps taken with a smoke per game, Contested caps taken with a smoke per game. Shared: Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's).
- Cap not lost: nearest cap 86% against 83% (-3.3 to +8.6); contested cap 84% against 76% (+1.9 to +15.3 *).
- Concealed damage is unchanged: per smoke 11,685 against 8,515 (+570.1 to +5,690.5 *); per game 57,152 against 37,034 (+5,334.5 to +33,896.9 *).
- Every other Top 6 minus Rest gap (25 scores: lineup, who, where, movement, concealed damage) is identical to round 5b. The gaps that moved are listed under "Changed from round 5b".

**Clans:** Top 6 and PN on the new scores (value, 95% interval, percentile).

| Clan | Died per 100 | Caught per 100 | Smoker died per 100 | Smoker caught per 100 | Nearest cap taken % | Contested cap taken % | Nearest cap not lost % | Contested cap not lost % |
|---|---|---|---|---|---|---|---|---|
| *H-SR | 6.0 (1.2 to 11.2) p0 | 4.0 (0.0 to 8.9) p0 | 4.0 (0.9 to 7.5) p4 | 2.0 (0.0 to 4.9) p9 | 56 (46 to 69) p100, n 50 | 42 (33 to 52) p96, n 65 | 86 (74 to 96) p50, n 37 | 86 (73 to 96) p70, n 44 |
| *RESIN | 17.5 (9.9 to 25.6) p57 | 7.8 (2.9 to 13.3) p22 | 9.7 (5.3 to 14.5) p39 | 1.9 (0.0 to 4.9) p4 | 32 (22 to 45) p57, n 56 | 27 (19 to 37) p57, n 70 | 75 (60 to 92) p10, n 32 | 74 (62 to 87) p20, n 38 |
| *BONKZ | 17.6 (10.3 to 25.8) p61 | 11.8 (5.9 to 17.8) p57 | 12.7 (6.9 to 20.0) p57 | 6.9 (2.4 to 12.7) p52 | 53 (35 to 72) p96, n 45 | 44 (30 to 62) p100, n 61 | 88 (80 to 97) p65, n 43 | 83 (73 to 93) p55, n 48 |
| *HTDOG | 10.4 (4.1 to 17.4) p17 | 6.6 (2.1 to 12.2) p9 | 8.5 (3.4 to 15.0) p30 | 5.7 (1.9 to 10.4) p30 | 30 (17 to 48) p48, n 53 | 27 (15 to 40) p52, n 60 | 85 (66 to 100) p40, n 33 | 88 (72 to 100) p80, n 41 |
| *KITE | 11.1 (2.6 to 21.2) p26 | 8.9 (2.4 to 15.9) p30 | 6.7 (0.0 to 16.7) p17 | 4.4 (0.0 to 10.8) p17 | 45 (25 to 65) p91, n 22 | 38 (19 to 60) p91, n 26 | 88 (58 to 100) p58, n 16 | 88 (57 to 100) p75, n 16 |
| *VRTUS | 9.8 (3.4 to 16.7) p11 | 8.5 (1.1 to 16.9) p26 | 6.1 (1.9 to 10.1) p9 | 4.9 (0.0 to 10.8) p22 | 24 (14 to 40) p28, n 51 | 18 (11 to 31) p26, n 60 | 93 (85 to 100) p85, n 28 | 85 (75 to 100) p65, n 26 |
| PN | 50.0 (20.0 to 75.0) p100 | 28.6 (7.1 to 50.0) p96 | 28.6 (11.1 to 50.0) p83 | 7.1 (0.0 to 22.2) p61 | 12 (0 to 67) p9, n 8, small n | 8 (0 to 33) p4, n 12, small n | too few (n 5) | too few (n 4) |

**Could not be done / proxy:**
- Rates with fewer than 8 cases are "too few": nearest cap taken: MANBA (n 4), OGF (n 7), RMN (n 6), KM (n 6); contested cap taken: MANBA (n 6); nearest cap not lost: KSE (n 7), NGA (n 7), PN (n 5), MANBA (n 4), OGF (n 4), RMN (n 4), KM (n 5); contested cap not lost: KSE (n 6), NGA (n 7), PN (n 4), MANBA (n 3), OGF (n 5), RMN (n 2), KM (n 0).
- "Died" cannot be judged for 9 smokes (-BN-, KSC, one game with a single replay); those clans' "died" rates use their other smokes.
- A clan interval comes from 7 to 24 games, so it is wide: read a clan's death score with its interval, not as a ranking.
- "Caps taken per game" counts each cap once per game when a smoke of the clan stood near it as it changed hands; it is not all caps the clan took.

**Verdict:** Keep

**Changed from round 5b:**

Scores replaced (old score -> new score, why):

| Round 5b score | Round 5c score | Why |
|---|---|---|
| Deaths per 100 smokes (`deaths_per100`) | Caught per 100 smokes (same numbers) plus Died per 100 smokes; smoker-only versions of both | new death metric |
| Deaths in or behind smoke per game (`deaths_pg`) | Ships caught per game (same numbers) plus Ships died per game | new death metric |
| Nearest cap taken % (`took_pct`, snapshots) | Nearest cap taken % and Contested cap taken % (timeline) | cap timeline |
| Nearest cap not lost % (`held_pct`, snapshots) | Nearest cap not lost % and Contested cap not lost % (timeline) | cap timeline |
| Caps taken next to a smoke per game (`caps_taken_pg`, snapshots) | Nearest caps taken with a smoke per game (same key) and Contested caps taken per game (timeline) | cap timeline |
| `cap_won_pg`, `cap_def_pg` (batch flags) | dropped | not to be used |
| First smoke of the game, Smokes after 12:00, Smokes before 5:00 (HUD clock) | same scores on the replay clock | clock (`e0` instead of `el`) |

Check: "caught per 100" equals round 5b's deaths per 100 for all 30 clans, and its Top 6 minus Rest interval is the same (-9.5 to -2.9 * then, -9.5 to -2.9 * now).

Top 6 clans and PN, every per-clan score that was replaced or moved: round 5b value and percentile -> round 5c value and percentile.

| Score (round 5b -> round 5c) | *H-SR | *RESIN | *BONKZ | *HTDOG | *KITE | *VRTUS | PN | Why |
|---|---|---|---|---|---|---|---|---|
| Deaths per 100 smokes -> Died per 100 smokes | 4.0 p0 -> 6.0 p0 | 7.8 p22 -> 17.5 p57 | 11.8 p57 -> 17.6 p61 | 6.6 p9 -> 10.4 p17 | 8.9 p30 -> 11.1 p26 | 8.5 p26 -> 9.8 p11 | 28.6 p96 -> 50.0 p100 | new death metric |
| Deaths per 100 smokes -> Caught per 100 smokes | 4.0 p0 -> 4.0 p0 (same) | 7.8 p22 -> 7.8 p22 (same) | 11.8 p57 -> 11.8 p57 (same) | 6.6 p9 -> 6.6 p9 (same) | 8.9 p30 -> 8.9 p30 (same) | 8.5 p26 -> 8.5 p26 (same) | 28.6 p96 -> 28.6 p96 (same) | unchanged |
| Smoker died per 100 smokes | new: 4.0 p4 | new: 9.7 p39 | new: 12.7 p57 | new: 8.5 p30 | new: 6.7 p17 | new: 6.1 p9 | new: 28.6 p83 | new death metric (no round 5b score) |
| Smoker caught per 100 smokes | new: 2.0 p9 | new: 1.9 p4 | new: 6.9 p52 | new: 5.7 p30 | new: 4.4 p17 | new: 4.9 p22 | new: 7.1 p61 | new split (no round 5b score) |
| Nearest cap taken (% of smokes where it was not ours) (snapshots -> timeline) | 38.0 p96 -> 56.0 p100 | 17.5 p35 -> 32.1 p57 | 42.2 p100 -> 53.3 p96 | 24.5 p52 -> 30.2 p48 | 31.8 p78 -> 45.5 p91 | 21.6 p43 -> 23.5 p28 | 12.5 p17 -> 12.5 p9 | cap timeline |
| Contested cap taken (% of smokes where it was not ours) | new: 41.5 p96 | new: 27.1 p57 | new: 44.3 p100 | new: 26.7 p52 | new: 38.5 p91 | new: 18.3 p26 | new: 8.3 p4 | cap timeline (no round 5b score) |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (snapshots -> timeline) | 89.2 p55 -> 86.5 p50 | 87.5 p30 -> 75.0 p10 | 93.0 p70 -> 88.4 p65 | 97.0 p95 -> 84.8 p40 | 93.8 p75 -> 87.5 p58 | 92.9 p65 -> 92.9 p85 | too few -> too few (same) | cap timeline |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 86.4 p70 | new: 73.7 p20 | new: 83.3 p55 | new: 87.8 p80 | new: 87.5 p75 | new: 84.6 p65 | new: too few | cap timeline (no round 5b score) |
| Nearest caps taken with a smoke per game | 0.77 p87 -> 1.14 p96 | 0.33 p26 -> 0.67 p52 | 0.81 p91 -> 1.00 p87 | 0.67 p70 -> 0.72 p65 | 0.50 p43 -> 0.64 p43 | 0.73 p83 -> 0.82 p72 | 0.14 p2 -> 0.14 p0 | cap timeline |
| Contested caps taken with a smoke per game | new: 1.09 p91 | new: 0.71 p52 | new: 1.14 p98 | new: 0.72 p70 | new: 0.64 p43 | new: 0.73 p74 | new: 0.14 p2 | cap timeline (no round 5b score) |
| Deaths in or behind smoke per game -> Ships died per game | 0.18 p0 -> 0.27 p0 | 0.33 p22 -> 0.75 p48 | 0.57 p52 -> 0.86 p61 | 0.39 p35 -> 0.61 p26 | 0.29 p11 -> 0.36 p13 | 0.64 p72 -> 0.73 p43 | 0.57 p52 -> 1.00 p72 | new death metric |
| Deaths in or behind smoke per game -> Ships caught per game | 0.18 p0 -> 0.18 p0 (same) | 0.33 p22 -> 0.33 p22 (same) | 0.57 p52 -> 0.57 p52 (same) | 0.39 p35 -> 0.39 p35 (same) | 0.29 p11 -> 0.29 p11 (same) | 0.64 p72 -> 0.64 p72 (same) | 0.57 p52 -> 0.57 p52 (same) | unchanged |
| First smoke of the game (median, s) | 120.5 s p0 -> 120.1 s p0 | 174.0 s p35 -> 173.4 s p35 | 198.0 s p65 -> 197.4 s p65 | 233.0 s p91 -> 232.4 s p91 | 150.0 s p22 -> 149.2 s p22 | 224.0 s p87 -> 222.8 s p87 | 221.5 s p78 -> 221.0 s p78 | clock |
| Smokes after 12:00 (%) | 8.0 p30 -> 7.0 p26 | 19.4 p91 -> 19.4 p91 (same) | 13.7 p65 -> 13.7 p65 (same) | 17.9 p83 -> 16.0 p78 | 8.9 p48 -> 8.9 p48 (same) | 14.6 p70 -> 14.6 p70 (same) | 7.1 p26 -> 7.1 p30 | clock |
| Smokes before 5:00 (%) | 31.0 p83 -> 32.0 p83 | 28.2 p65 -> 28.2 p65 (same) | 22.5 p26 -> 22.5 p22 | 23.6 p30 -> 23.6 p26 | 24.4 p39 -> 24.4 p39 (same) | 18.3 p0 -> 18.3 p0 (same) | 50.0 p100 -> 50.0 p100 (same) | clock |

Top 6 clans and PN, 95% intervals of the same scores (round 5b -> round 5c).

| Score | *H-SR | *RESIN | *BONKZ | *HTDOG | *KITE | *VRTUS | PN |
|---|---|---|---|---|---|---|---|
| Died per 100 smokes | 0.0 to 8.9 -> 1.2 to 11.2 | 2.9 to 13.3 -> 9.9 to 25.6 | 5.9 to 17.8 -> 10.3 to 25.8 | 2.1 to 12.2 -> 4.1 to 17.4 | 2.4 to 15.9 -> 2.6 to 21.2 | 1.1 to 16.9 -> 3.4 to 16.7 | 7.1 to 50.0 -> 20.0 to 75.0 |
| Caught per 100 smokes | 0.0 to 8.9 -> 0.0 to 8.9 | 2.9 to 13.3 -> 2.9 to 13.3 | 5.9 to 17.8 -> 5.9 to 17.8 | 2.1 to 12.2 -> 2.1 to 12.2 | 2.4 to 15.9 -> 2.4 to 15.9 | 1.1 to 16.9 -> 1.1 to 16.9 | 7.1 to 50.0 -> 7.1 to 50.0 |
| Smoker died per 100 smokes | new: 0.9 to 7.5 | new: 5.3 to 14.5 | new: 6.9 to 20.0 | new: 3.4 to 15.0 | new: 0.0 to 16.7 | new: 1.9 to 10.1 | new: 11.1 to 50.0 |
| Smoker caught per 100 smokes | new: 0.0 to 4.9 | new: 0.0 to 4.9 | new: 2.4 to 12.7 | new: 1.9 to 10.4 | new: 0.0 to 10.8 | new: 0.0 to 10.8 | new: 0.0 to 22.2 |
| Nearest cap taken (% of smokes where it was not ours) | 23.1 to 55.3 -> 46.0 to 69.2 | 8.3 to 26.5 -> 22.0 to 45.5 | 26.2 to 58.3 -> 35.5 to 72.4 | 12.8 to 39.4 -> 16.9 to 47.5 | 12.5 to 50.0 -> 25.0 to 65.2 | 12.2 to 37.5 -> 13.8 to 40.0 | 0.0 to 66.7 -> 0.0 to 66.7 |
| Contested cap taken (% of smokes where it was not ours) | new: 33.3 to 51.7 | new: 18.8 to 37.3 | new: 29.9 to 62.1 | new: 15.1 to 40.0 | new: 19.0 to 60.0 | new: 11.1 to 31.0 | new: 0.0 to 33.3 |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 77.8 to 97.6 -> 74.2 to 96.2 | 76.5 to 96.9 -> 60.0 to 91.7 | 86.8 to 100.0 -> 80.0 to 96.8 | 89.3 to 100.0 -> 65.5 to 100.0 | 72.7 to 100.0 -> 58.3 to 100.0 | 84.9 to 100.0 -> 84.9 to 100.0 | too few -> too few |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 73.3 to 95.7 | new: 62.2 to 86.7 | new: 73.5 to 92.7 | new: 71.8 to 100.0 | new: 57.1 to 100.0 | new: 75.0 to 100.0 | new: too few |
| Nearest caps taken with a smoke per game | 0.50 to 1.05 -> 0.86 to 1.45 | 0.17 to 0.54 -> 0.46 to 0.88 | 0.52 to 1.10 -> 0.67 to 1.33 | 0.33 to 1.00 -> 0.39 to 1.06 | 0.14 to 0.93 -> 0.29 to 1.07 | 0.36 to 1.09 -> 0.45 to 1.09 | 0.00 to 0.43 -> 0.00 to 0.43 |
| Contested caps taken with a smoke per game | new: 0.77 to 1.41 | new: 0.50 to 0.92 | new: 0.81 to 1.43 | new: 0.39 to 1.06 | new: 0.29 to 1.07 | new: 0.45 to 1.00 | new: 0.00 to 0.43 |
| Ships died per game | 0.00 to 0.41 -> 0.05 to 0.50 | 0.12 to 0.54 -> 0.42 to 1.08 | 0.29 to 0.90 -> 0.48 to 1.29 | 0.11 to 0.72 -> 0.22 to 1.00 | 0.07 to 0.50 -> 0.07 to 0.71 | 0.09 to 1.36 -> 0.27 to 1.27 | 0.14 to 1.14 -> 0.29 to 1.71 |
| Ships caught per game | 0.00 to 0.41 -> 0.00 to 0.41 | 0.12 to 0.54 -> 0.12 to 0.54 | 0.29 to 0.90 -> 0.29 to 0.90 | 0.11 to 0.72 -> 0.11 to 0.72 | 0.07 to 0.50 -> 0.07 to 0.50 | 0.09 to 1.36 -> 0.09 to 1.36 | 0.14 to 1.14 -> 0.14 to 1.14 |
| First smoke of the game (median, s) | 104.0 s to 163.0 s -> 102.7 s to 162.3 s | 122.0 s to 229.0 s -> 121.9 s to 229.0 s | 163.0 s to 280.0 s -> 162.4 s to 279.4 s | 170.0 s to 265.0 s -> 169.4 s to 264.4 s | 98.0 s to 296.0 s -> 97.7 s to 295.3 s | 160.0 s to 283.0 s -> 158.9 s to 282.7 s | 145.0 s to 520.0 s -> 143.9 s to 519.7 s |
| Smokes after 12:00 (%) | 2.7 to 14.3 -> 2.2 to 13.3 | 10.4 to 30.1 -> 10.4 to 30.1 | 6.5 to 21.7 -> 6.5 to 21.7 | 8.0 to 29.6 -> 6.6 to 27.0 | 2.4 to 17.6 -> 2.4 to 17.6 | 3.6 to 23.1 -> 3.6 to 23.1 | 0.0 to 27.3 -> 0.0 to 27.3 |
| Smokes before 5:00 (%) | 25.3 to 36.8 -> 26.5 to 37.7 | 22.7 to 34.6 -> 22.7 to 34.6 | 17.7 to 26.8 -> 17.7 to 26.8 | 17.6 to 30.5 -> 17.6 to 30.5 | 18.9 to 29.8 -> 18.9 to 29.8 | 10.5 to 28.3 -> 10.5 to 28.3 | 25.0 to 78.6 -> 25.0 to 78.6 |

The other 23 clans. Replaced scores (round 5b -> round 5c); "died" is new, "caught" is the old deaths number.

| Clan | Deaths per 100 -> Died per 100 | Caught per 100 (was Deaths per 100) | Nearest cap taken % (snapshots -> timeline) | Nearest cap not lost % (snapshots -> timeline) | Caps taken per game (snapshots -> timeline) |
|---|---|---|---|---|---|
| MZY | 14.0 -> 22.0 | 14.0 (same) | 29.0 -> 38.7 | 78.6 -> 78.6 | 0.37 -> 0.53 |
| EPOXY | 12.2 -> 15.9 | 12.2 (same) | 30.6 -> 36.1 | 82.8 -> 75.9 | 0.59 -> 0.65 |
| HFANS | 10.0 -> 13.6 | 10.0 (same) | 26.2 -> 27.9 | 85.0 -> 82.5 | 0.82 -> 0.88 |
| -BN- | 9.9 -> 11.6 | 9.9 (same) | 22.2 -> 31.5 | 96.2 -> 96.2 | 0.71 -> 1.07 |
| KITED | 12.7 -> 15.9 | 12.7 (same) | 25.0 -> 25.0 | 95.7 -> 95.7 | 0.57 -> 0.57 |
| MACHX | 6.1 -> 9.8 | 6.1 (same) | 32.1 -> 35.8 | 88.9 -> 81.5 | 1.07 -> 1.14 |
| REEEE | 7.7 -> 7.7 | 7.7 (same) | 13.3 -> 23.3 | 70.6 -> 70.6 | 0.23 -> 0.38 |
| PFANS | 12.5 -> 16.7 | 12.5 (same) | 11.8 -> 23.5 | 87.5 -> 62.5 | 0.17 -> 0.33 |
| KSC | 11.1 -> 15.3 | 11.1 (same) | 20.6 -> 29.4 | 88.9 -> 88.9 | 0.55 -> 0.82 |
| 5D | 32.4 -> 37.8 | 32.4 (same) | 34.8 -> 34.8 | 88.2 -> 82.4 | 0.60 -> 0.60 |
| BONKY | 11.1 -> 22.2 | 11.1 (same) | 4.3 -> 8.7 | 87.5 -> 87.5 | 0.14 -> 0.29 |
| KSE | 15.0 -> 45.0 | 15.0 (same) | 13.3 -> 33.3 | too few -> too few | 0.29 -> 0.71 |
| MACH | 6.9 -> 27.6 | 6.9 (same) | 15.8 -> 15.8 | 100.0 -> 100.0 | 0.43 -> 0.43 |
| NGA | 14.3 -> 25.0 | 14.3 (same) | 10.0 -> 10.0 | too few -> too few | 0.29 -> 0.29 |
| RSR | 19.2 -> 38.5 | 19.2 (same) | 35.7 -> 35.7 | 90.9 -> 90.9 | 0.71 -> 0.71 |
| SCCC2 | 10.4 -> 10.4 | 10.4 (same) | 12.0 -> 16.0 | 95.5 -> 90.9 | 0.43 -> 0.57 |
| UYSC | 27.8 -> 33.3 | 27.8 (same) | 26.1 -> 43.5 | 85.7 -> 85.7 | 0.57 -> 0.86 |
| BTLST (flag) | 23.5 -> 26.5 | 23.5 (same) | 33.3 -> 33.3 | 92.3 -> 69.2 | 0.83 -> 0.83 |
| INCA (flag) | 7.7 -> 12.8 | 7.7 (same) | 31.2 -> 41.2 | 82.4 -> 82.4 | 0.67 -> 1.00 |
| MANBA (flag) | 22.2 -> 22.2 | 22.2 (same) | too few -> too few | too few -> too few | 0.00 -> 0.17 |
| OGF (flag) | 33.3 -> 66.7 | 33.3 (same) | too few -> too few | too few -> too few | 0.00 -> 0.00 |
| RMN (flag) | 33.3 -> 33.3 | 33.3 (same) | too few -> too few | too few -> too few | 0.00 -> 0.17 |
| KM (flag) | 13.3 -> 20.0 | 13.3 (same) | too few -> too few | too few -> too few | 0.40 -> 0.40 |

Time scores, what the switch from the HUD clock to the replay clock moved: the first smoke of the game moves for all 30 clans, by 0.0 to 1.4 s (median 0.6 s; the replay clock is exact and the HUD clock is in whole seconds). Share after 12:00 moves for H-SR (8.0% -> 7.0%), HTDOG (17.9% -> 16.0%). Share before 5:00 moves for H-SR (31.0% -> 32.0%), KSC (22.2% -> 23.8%).
Other clans where a time score moved by more than a rounding step (1 s, or half a point): EPOXY First smoke of the game (median, s) 192.0 s -> 190.7 s; HFANS First smoke of the game (median, s) 143.0 s -> 142.0 s; MACHX First smoke of the game (median, s) 146.0 s -> 144.6 s; PFANS First smoke of the game (median, s) 185.5 s -> 184.4 s; KSE First smoke of the game (median, s) 251.0 s -> 250.0 s; MANBA First smoke of the game (median, s) 315.0 s -> 313.9 s; KSC Smokes before 5:00 (%) 22.2 -> 23.8.

All Top 6 minus Rest gaps, round 5b and round 5c (Top 6 / Rest / 95% interval).

| Score | Round 5b | Round 5c | Why |
|---|---|---|---|
| Long-smoke destroyers per game (`long_ships_pg`) | 0.89 / 0.66 / -0.14 to +0.52 | 0.89 / 0.66 / -0.14 to +0.52 | unchanged |
| Cap-sitter destroyers per game (`sitter_ships_pg`) | 0.70 / 0.70 / -0.26 to +0.29 | 0.70 / 0.70 / -0.26 to +0.29 | unchanged |
| Destroyers carrying smoke per game (`smoke_dd_pg`) | 1.63 / 1.45 / -0.08 to +0.44 | 1.63 / 1.45 / -0.08 to +0.44 | unchanged |
| Cruisers carrying smoke per game (`smoke_cruisers_pg`) | 0.52 / 0.72 / -0.54 to +0.22 | 0.52 / 0.72 / -0.54 to +0.22 | unchanged |
| Exhaust-smoke ships per game (`exhaust_ships_pg`) | 0.23 / 0.62 / -0.62 to -0.21 * | 0.23 / 0.62 / -0.62 to -0.21 * | unchanged |
| Smokes per game (`smokes_pg`) | 4.89 / 4.35 / -0.43 to +1.58 | 4.89 / 4.35 / -0.43 to +1.58 | unchanged |
| First smoke of the game (median, s) (`first_smoke_s`) | 175.0 s / 196.5 s / -54.0 to +29.5 | 173.9 s / 196.1 s / -53.9 to +29.1 | clock |
| Smokes after 12:00 (%) (`late_pct`) | 14.3 / 11.1 / -1.6 to +7.8 | 13.8 / 11.1 / -2.3 to +7.3 | clock |
| For a teammate (%) (`teammate_pct`) | 63.8 / 54.8 / -2.5 to +20.2 | 63.8 / 54.8 / -2.5 to +20.2 | unchanged |
| Stacked on a teammate (%) (`stacked_pct`) | 31.6 / 23.5 / -3.0 to +18.4 | 31.6 / 23.5 / -3.0 to +18.4 | unchanged |
| Radar cruiser inside (% of destroyer smokes) (`radar_ca_inside_pct`) | 47.3 / 29.0 / +7.8 to +27.0 * | 47.3 / 29.0 / +7.8 to +27.0 * | unchanged |
| Median distance to cap edge (m) (`edge_m`) | 2,060 / 2,089 / -502.0 to +499.7 | 2,060 / 2,089 / -502.0 to +499.7 | unchanged |
| Inside a cap (%) (`inside_cap_pct`) | 22.9 / 24.2 / -7.7 to +4.2 | 22.9 / 24.2 / -7.7 to +4.2 | unchanged |
| Centre lane (%) (`centre_pct`) | 24.3 / 21.0 / -4.9 to +11.9 | 24.3 / 21.0 / -4.9 to +11.9 | unchanged |
| Pushing (%) (`pushing_pct`) | 20.8 / 20.3 / -4.1 to +4.6 | 20.8 / 20.3 / -4.1 to +4.6 | unchanged |
| Kiting (%) (`kiting_pct`) | 17.7 / 20.3 / -7.7 to +2.0 | 17.7 / 20.3 / -7.7 to +2.0 | unchanged |
| Parked (%) (`parked_pct`) | 28.8 / 27.5 / -11.4 to +13.5 | 28.8 / 27.5 / -11.4 to +13.5 | unchanged |
| Concealed damage per smoke (`conc_per_smoke`) | 11,685 / 8,515 / +570.1 to +5,690.5 * | 11,685 / 8,515 / +570.1 to +5,690.5 * | unchanged |
| Concealed damage per game (`conc_pg`) | 57,152 / 37,034 / +5,334.5 to +33,896.9 * | 57,152 / 37,034 / +5,334.5 to +33,896.9 * | unchanged |
| Nearest cap taken (% of smokes where it was not ours) (`took_pct`) | 28.4 / 22.6 / -2.2 to +14.6 | not in this round | dropped |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`held_pct`) | 92.1 / 87.2 / +0.6 to +9.5 * | not in this round | dropped |
| Deaths per 100 smokes (`deaths_per100`) | 7.8 / 13.4 / -9.5 to -2.9 * | not in this round | dropped |
| Svea or Jinan per game (`parked_cruisers_pg`) | 0.35 / 0.19 / -0.11 to +0.57 | 0.35 / 0.19 / -0.11 to +0.57 | unchanged |
| Ships carrying smoke per game (`smoke_ships_pg`) | 2.27 / 2.31 / -0.39 to +0.36 | 2.27 / 2.31 / -0.39 to +0.36 | unchanged |
| Destroyers per game (`dd_pg`) | 3.25 / 3.00 / +0.05 to +0.46 * | 3.25 / 3.00 / +0.05 to +0.46 * | unchanged |
| Radar ships per game (`radar_ships_pg`) | 3.57 / 3.01 / +0.20 to +0.84 * | 3.57 / 3.01 / +0.20 to +0.84 * | unchanged |
| Smokes before 5:00 (%) (`early_pct`) | 24.9 / 27.7 / -7.3 to +1.3 | 25.1 / 27.8 / -7.4 to +1.6 | clock |
| Selfish (%) (`selfish_pct`) | 36.2 / 45.2 / -20.4 to +2.1 | 36.2 / 45.2 / -20.4 to +2.1 | unchanged |
| Any cruiser inside (% of destroyer smokes) (`cruiser_inside_pct`) | 52.7 / 34.9 / +5.0 to +27.9 * | 52.7 / 34.9 / +5.0 to +27.9 * | unchanged |
| Own side of the front line (%) (`own_half_pct`) | 83.8 / 78.3 / +1.4 to +9.8 * | 83.8 / 78.3 / +1.4 to +9.8 * | unchanged |
| Sideways (%) (`sideways_pct`) | 26.0 / 25.5 / -9.4 to +8.7 | 26.0 / 25.5 / -9.4 to +8.7 | unchanged |
| Nearest caps taken with a smoke per game (`caps_taken_pg`) | 0.63 / 0.49 / -0.06 to +0.32 | 0.85 / 0.61 / +0.04 to +0.44 * | cap timeline |
| Smokes with the batch cap-won flag per game (`cap_won_pg`) | 1.20 / 0.81 / +0.15 to +0.61 * | not in this round | dropped |
| Batch cap-defended flag per game (secondary: fires for any owned cap with an enemy inside) (`cap_def_pg`) | 1.48 / 1.39 / -0.32 to +0.48 | not in this round | dropped |
| Deaths in or behind smoke per game (`deaths_pg`) | 0.38 / 0.58 / -0.37 to -0.06 * | not in this round | dropped |
| Nearest cap taken (% of smokes where it was not ours) (`we_took_n_pct`) | not in this round | 39.0 / 28.5 / +0.5 to +21.5 * | new |
| Contested cap taken (% of smokes where it was not ours) (`we_took_c_pct`) | not in this round | 32.2 / 22.8 / +1.1 to +17.6 * | new |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`not_lost_n_pct`) | not in this round | 85.7 / 83.0 / -3.3 to +8.6 | new |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`not_lost_c_pct`) | not in this round | 83.6 / 75.8 / +1.9 to +15.3 * | new |
| Died per 100 smokes (`died_per100`) | not in this round | 12.3 / 19.3 / -13.3 to -2.6 * | new |
| Caught per 100 smokes (`caught_per100`) | not in this round | 7.8 / 13.4 / -9.5 to -2.9 * | new |
| Smoker died per 100 smokes (`died_smoker_per100`) | not in this round | 8.2 / 15.1 / -12.3 to -3.2 * | new |
| Smoker caught per 100 smokes (`caught_smoker_per100`) | not in this round | 4.3 / 9.2 / -8.6 to -2.5 * | new |
| Contested caps taken with a smoke per game (`caps_taken_c_pg`) | not in this round | 0.86 / 0.60 / +0.05 to +0.46 * | new |
| Ships died per game (`died_pg`) | not in this round | 0.60 / 0.83 / -0.49 to -0.03 * | new |
| Ships caught per game (`caught_pg`) | not in this round | 0.38 / 0.58 / -0.37 to -0.06 * | new |

### D2. Group the clans; one scale or several styles?

**Answer:** No clan changes style. The grouping is built from 17 behaviour scores; only two of them changed at all (first smoke of the game and share after 12:00, now on the replay clock), and they moved by at most 1.4 s and one or two smokes. Clan positions shift by at most 0.02 on the first scale and 0.09 on the second. It is still two separate scales with four soft-bordered corners.

**Numbers:**
- Scores used: the same 17 as round 5b; no death or cap score is among them, so the new death and cap definitions cannot move the grouping. The two time scores are the only inputs that differ.
- Shares of the differences between clans: first scale 29.6% (round 5b 29.6%), second 17.8% (17.8%), third 11.5% (11.6%). Together the first two carry 47%. Shuffled data gives at most 19.1% and 15.7% (95th percentile), so both scales are real.
- Check that the rerun is the same method: run on the HUD clock, the script reproduces round 5b's clan positions exactly and the same four groups.
- Shape: on the first scale the largest gap between neighbours is 1.7 of a range of 8.6. On the second there is a break: 7 clans sit low (PN, MZY, 5D, KITED, NGA, KSE, PFANS; -1.6 or below) and everyone else is at +0.0 or above.
- Grouping on all 17 scores at once is still a smear: silhouette 0.18 (2 groups), 0.16 (3), 0.18 (4), where 1 would be clean groups. Agreement with the original under resampling of games: 0.54 for 2 groups, 0.34 for 3 (round 5b 0.54 and 0.34). Clan positions under resampling correlate 0.90 with the original on the first scale and 0.79 on the second (round 5b 0.90 and 0.79).
- On the two-scale map four corners fit best (silhouette 0.46); clans keep their corner in 86% of resamples on average (round 5b 86%).

Loadings (link of each score with each scale; round 5b -> round 5c):

| Score | First scale (who the smoke is for) | Second scale (how much smoke) |
|---|---|---|
| Stacked on a teammate (%) | -0.85 -> -0.85 | +0.29 -> +0.29 |
| For a teammate (%) | -0.83 -> -0.83 | +0.07 -> +0.07 |
| Radar cruiser inside (% of destroyer smokes) | -0.82 -> -0.82 | +0.15 -> +0.15 |
| Long-smoke destroyers per game | -0.78 -> -0.78 | +0.24 -> +0.24 |
| Cruisers carrying smoke per game | +0.72 -> +0.72 | -0.11 -> -0.11 |
| Cap-sitter destroyers per game | +0.67 -> +0.67 | +0.51 -> +0.51 |
| Kiting (%) | +0.58 -> +0.58 | -0.02 -> -0.02 |
| Parked (%) | +0.56 -> +0.56 | +0.58 -> +0.58 |
| Exhaust-smoke ships per game | +0.41 -> +0.41 | -0.48 -> -0.48 |
| Inside a cap (%) | +0.34 -> +0.34 | +0.24 -> +0.24 |
| Centre lane (%) | +0.32 -> +0.33 | -0.00 -> -0.01 |
| Pushing (%) | -0.31 -> -0.31 | -0.51 -> -0.51 |
| First smoke of the game (median, s) | +0.30 -> +0.30 | -0.46 -> -0.46 |
| Median distance to cap edge (m) | -0.25 -> -0.25 | -0.37 -> -0.37 |
| Smokes per game | +0.23 -> +0.23 | +0.76 -> +0.76 |
| Smokes after 12:00 (%) | -0.19 -> -0.20 | +0.51 -> +0.51 |
| Destroyers carrying smoke per game | -0.05 -> -0.05 | +0.71 -> +0.72 |

Largest change in any loading: 0.01.

Each clan's position and style, round 5b and round 5c (first scale: negative = smoke laid for a teammate, positive = ships smoke for themselves; second scale: positive = more smoke).

| Clan | First scale | Second scale | Style, round 5b | Style, round 5c | Moved | Kept its style under resampling |
|---|---|---|---|---|---|---|
| *RESIN | -2.38 -> -2.39 | +1.15 -> +1.15 | Team smoke, plenty of it | Team smoke, plenty of it | no | 100% -> 100% |
| *H-SR | -4.58 -> -4.57 | +0.32 -> +0.28 | Team smoke, plenty of it | Team smoke, plenty of it | no | 96% -> 95% |
| *BONKZ | -2.22 -> -2.23 | +0.90 -> +0.91 | Team smoke, plenty of it | Team smoke, plenty of it | no | 95% -> 95% |
| MZY | -1.85 -> -1.85 | -3.25 -> -3.26 | Team smoke, little of it | Team smoke, little of it | no | 97% -> 97% |
| *HTDOG | +2.49 -> +2.51 | +0.74 -> +0.65 | Own smoke, plenty of it | Own smoke, plenty of it | no | 96% -> 98% |
| EPOXY | -1.66 -> -1.67 | +1.27 -> +1.28 | Team smoke, plenty of it | Team smoke, plenty of it | no | 100% -> 100% |
| HFANS | +0.32 -> +0.32 | +1.22 -> +1.23 | Team smoke, plenty of it | Team smoke, plenty of it | no | 57% -> 57% (borderline) |
| -BN- | -1.00 -> -1.00 | +0.82 -> +0.83 | Team smoke, plenty of it | Team smoke, plenty of it | no | 96% -> 96% |
| *KITE | -1.16 -> -1.16 | +0.25 -> +0.26 | Team smoke, plenty of it | Team smoke, plenty of it | no | 72% -> 72% (borderline) |
| KITED | +2.77 -> +2.77 | -2.49 -> -2.48 | Own smoke, little of it | Own smoke, little of it | no | 100% -> 100% |
| MACHX | +1.19 -> +1.18 | +0.53 -> +0.55 | Own smoke, plenty of it | Own smoke, plenty of it | no | 63% -> 62% (borderline) |
| REEEE | -0.08 -> -0.08 | +0.76 -> +0.76 | Team smoke, plenty of it | Team smoke, plenty of it | no | 53% -> 54% (borderline) |
| PFANS | -0.93 -> -0.93 | -1.61 -> -1.61 | Team smoke, little of it | Team smoke, little of it | no | 76% -> 76% |
| KSC | -1.73 -> -1.74 | +2.54 -> +2.55 | Team smoke, plenty of it | Team smoke, plenty of it | no | 100% -> 100% |
| *VRTUS | +0.68 -> +0.68 | +1.97 -> +1.97 | Own smoke, plenty of it | Own smoke, plenty of it | no | 64% -> 64% (borderline) |
| 5D | +1.61 -> +1.61 | -2.77 -> -2.76 | Own smoke, little of it | Own smoke, little of it | no | 98% -> 98% |
| BONKY | -1.74 -> -1.74 | +1.27 -> +1.27 | Team smoke, plenty of it | Team smoke, plenty of it | no | 85% -> 85% |
| KSE | +3.02 -> +3.02 | -2.11 -> -2.11 | Own smoke, little of it | Own smoke, little of it | no | 90% -> 90% |
| MACH | +3.68 -> +3.68 | +0.63 -> +0.62 | Own smoke, plenty of it | Own smoke, plenty of it | no | 98% -> 98% |
| NGA | +0.21 -> +0.21 | -2.15 -> -2.14 | Team smoke, little of it | Team smoke, little of it | no | 72% -> 72% (borderline) |
| PN | -2.89 -> -2.89 | -3.29 -> -3.29 | Team smoke, little of it | Team smoke, little of it | no | 98% -> 98% |
| RSR | -0.56 -> -0.56 | +0.00 -> +0.01 | Team smoke, plenty of it | Team smoke, plenty of it | no | 73% -> 73% (borderline) |
| SCCC2 | +2.80 -> +2.80 | +2.12 -> +2.12 | Own smoke, plenty of it | Own smoke, plenty of it | no | 95% -> 95% |
| UYSC | +4.01 -> +4.01 | +1.19 -> +1.21 | Own smoke, plenty of it | Own smoke, plenty of it | no | 92% -> 92% |
| BTLST (flag) | +0.73 -> +0.73 | -1.46 -> -1.44 | Own smoke, little of it | Own smoke, little of it | no | flagged: not used to build the map |
| INCA (flag) | +0.14 -> +0.14 | +2.11 -> +2.11 | Team smoke, plenty of it | Team smoke, plenty of it | no | flagged: not used to build the map |
| MANBA (flag) | -1.00 -> -1.00 | -5.26 -> -5.26 | Team smoke, little of it | Team smoke, little of it | no | flagged: not used to build the map |
| OGF (flag) | +0.91 -> +0.91 | -2.06 -> -2.06 | Own smoke, little of it | Own smoke, little of it | no | flagged: not used to build the map |
| RMN (flag) | -0.40 -> -0.39 | -2.27 -> -2.27 | Team smoke, little of it | Team smoke, little of it | no | flagged: not used to build the map |
| KM (flag) | -0.73 -> -0.73 | -3.57 -> -3.57 | Team smoke, little of it | Team smoke, little of it | no | flagged: not used to build the map |

Clans that moved style: none (0 of 30).

The four corners:

| Style | Top 6 | Rest | Borderline (kept the style in under 75% of resamples) | Flagged clans that would fall here |
|---|---|---|---|---|
| Team smoke, plenty of it (11 clans, 167 games, 810 smokes; W-L 101-66) | RESIN, H-SR, BONKZ, KITE | EPOXY, HFANS, -BN-, REEEE, KSC, BONKY, RSR | HFANS 57%, KITE 72%, REEEE 54%, RSR 73% | INCA |
| Own smoke, plenty of it (6 clans, 64 games, 383 smokes; W-L 32-32) | HTDOG, VRTUS | MACHX, MACH, SCCC2, UYSC | MACHX 62%, VRTUS 64% | none |
| Team smoke, little of it (4 clans, 45 games, 116 smokes; W-L 20-25) | none | MZY, PFANS, NGA, PN | NGA 72% | MANBA, RMN, KM |
| Own smoke, little of it (3 clans, 31 games, 120 smokes; W-L 12-19) | none | KITED, 5D, KSE | none | BTLST, OGF |

Borderline clans: round 5b HFANS 57%, KITE 72%, MACHX 63%, NGA 72%, REEEE 53%, RSR 73%, VRTUS 64%; round 5c HFANS 57%, KITE 72%, MACHX 62%, NGA 72%, REEEE 54%, RSR 73%, VRTUS 64%. The list is the same.

What each style looks like (pooled; 95% interval, games resampled within the style; n = smokes the rate applies to):

| Score | Team smoke, plenty | Own smoke, plenty | Team smoke, little | Own smoke, little |
|---|---|---|---|---|
| Long-smoke destroyers per game | 1.0 (0.9 to 1.1) | 0.4 (0.3 to 0.6) | 0.6 (0.4 to 0.8) | 0.3 (0.2 to 0.5) |
| Cruisers carrying smoke per game | 0.4 (0.3 to 0.5) | 1.1 (0.8 to 1.3) | 0.5 (0.4 to 0.7) | 1.2 (0.9 to 1.4) |
| Destroyers carrying smoke per game | 1.7 (1.6 to 1.8) | 1.6 (1.4 to 1.8) | 0.9 (0.7 to 1.2) | 1.2 (1.0 to 1.3) |
| Smokes per game | 4.8 (4.5 to 5.3) | 6.0 (5.1 to 6.8) | 2.6 (2.0 to 3.2) | 3.9 (3.4 to 4.5) |
| First smoke of the game (median, s) | 2:42 (2:32 to 3:03) | 3:26 (3:00 to 4:04) | 3:04 (2:20 to 4:31) | 3:39 (3:00 to 4:15) |
| Smokes after 12:00 (%) | 13% (10 to 16) | 13% (9 to 18) | 8% (3 to 13) | 6% (2 to 11) |
| For a teammate (%) | 66% (61 to 70) | 45% (39 to 51) | 61% (50 to 70) | 44% (32 to 56) |
| Radar cruiser inside (% of destroyer smokes) | 42% (36 to 48) | 28% (20 to 37) | 41% (29 to 52) | 7% (0 to 15) |
| Parked (%) | 25% (21 to 29) | 40% (34 to 48) | 17% (10 to 25) | 23% (17 to 29) |
| Inside a cap (%) | 24% (20 to 29) | 24% (19 to 29) | 17% (10 to 24) | 26% (19 to 32) |
| What it buys: Concealed damage per smoke | 11,692 (10,402 to 12,964) | 7,725 (6,524 to 9,044) | 9,204 (6,899 to 12,502) | 4,120 (2,772 to 5,724) |
| What it buys: Concealed damage per game | 56,712 (50,377 to 64,535) | 46,230 (35,518 to 56,839) | 23,726 (16,399 to 32,408) | 15,948 (10,177 to 22,684) |
| What it buys: Nearest cap taken (% of smokes where it was not ours) | 36% (30 to 41), n 425 | 29% (22 to 35), n 224 | 25% (15 to 37), n 76 | 30% (22 to 40), n 70 |
| What it buys: Contested cap taken (% of smokes where it was not ours) | 30% (25 to 34), n 538 | 23% (17 to 30), n 253 | 19% (11 to 29), n 89 | 23% (16 to 31), n 88 |
| What it buys: Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 84% (80 to 88), n 277 | 88% (81 to 95), n 136 | 76% (63 to 88), n 34 | 89% (78 to 98), n 47 |
| What it buys: Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 79% (74 to 83), n 290 | 86% (78 to 93), n 144 | 70% (50 to 86), n 33 | 85% (70 to 95), n 41 |
| What it buys: Died per 100 smokes | 14.5 (11.8 to 17.3), n 801 | 13.6 (9.6 to 18.1), n 383 | 25.0 (16.1 to 33.3), n 116 | 27.5 (19.4 to 35.6), n 120 |
| What it buys: Caught per 100 smokes | 9.6 (7.5 to 12.1), n 810 | 9.4 (6.0 to 13.1), n 383 | 15.5 (8.8 to 22.8), n 116 | 19.2 (12.0 to 26.5), n 120 |
| What it buys: Smoker died per 100 smokes | 10.0 (7.8 to 12.4), n 801 | 11.2 (7.6 to 15.3), n 383 | 16.4 (9.8 to 23.2), n 116 | 24.2 (17.1 to 31.7), n 120 |
| What it buys: Smoker caught per 100 smokes | 5.1 (3.6 to 6.9), n 810 | 7.8 (4.7 to 11.1), n 383 | 8.6 (3.5 to 13.5), n 116 | 15.8 (10.2 to 21.7), n 120 |
| What it buys: Nearest caps taken with a smoke per game | 0.8 (0.7 to 0.9) | 0.8 (0.6 to 1.0) | 0.4 (0.2 to 0.6) | 0.6 (0.5 to 0.8) |
| What it buys: Contested caps taken with a smoke per game | 0.8 (0.7 to 0.9) | 0.7 (0.6 to 0.9) | 0.3 (0.2 to 0.5) | 0.6 (0.4 to 0.7) |

Plain reading of the styles with the new outcome scores:
- **Team smoke, plenty of it.** Long-smoke destroyers (Somers, Gearing, Harugumo) lay smoke for a cruiser, usually a radar cruiser, and they lay a lot of it. Few cruisers bring their own smoke. Died 14.5 and caught 9.6 per 100 smokes (smoker only 10.0 and 5.1); nearest cap taken 36%, contested cap taken 30%; nearest cap not lost 84%, contested 79%; concealed damage per smoke 11,692.
- **Own smoke, plenty of it.** Cruisers (Svea, Jinan, Napoli) and cap-sitter destroyers (Daring, Gdansk, Shimakaze) each smoke for themselves, often parked, and there is a lot of smoke per game. Died 13.6 and caught 9.4 per 100 smokes (smoker only 11.2 and 7.8); nearest cap taken 29%, contested cap taken 23%; nearest cap not lost 88%, contested 86%; concealed damage per smoke 7,725.
- **Team smoke, little of it.** The same team-smoke habit, but few smoke ships in the lineup and few smokes per game; the first smoke comes late. Died 25.0 and caught 15.5 per 100 smokes (smoker only 16.4 and 8.6); nearest cap taken 25%, contested cap taken 19%; nearest cap not lost 76%, contested 70%; concealed damage per smoke 9,204.
- **Own smoke, little of it.** Ships smoke for themselves (Napoli exhaust, cap sitters), with few smoke destroyers and few smokes per game. Died 27.5 and caught 19.2 per 100 smokes (smoker only 24.2 and 15.8); nearest cap taken 30%, contested cap taken 23%; nearest cap not lost 89%, contested 85%; concealed damage per smoke 4,120.
- On both death scores the fewest deaths per 100 smokes are in "Own smoke, plenty of it" and the most in "Own smoke, little of it". The two "plenty" styles are close to each other on both; the two "little" styles have few smokes, so their intervals are wide.

**Top 6 or Shared:**
- First scale (who the smoke is for): Shared. Top 6 mean -1.19, Rest +0.40, gap -1.59 (-3.58 to +0.47). Round 5b: Top 6 mean -1.20, Rest +0.40, gap -1.59 (-3.58 to +0.46).
- Second scale (how much smoke): Top 6. Top 6 mean +0.87, Rest -0.29, gap +1.16 (+0.16 to +2.21 *). Round 5b: Top 6 mean +0.89, Rest -0.30, gap +1.18 (+0.19 to +2.23 *).
- Top 6 in a "plenty" style: 6 of 6 (17 of 24 clans are in one; chance of all six at random 9%). Top 6 in "Team smoke, plenty of it": 4 of 6 (chance of 4 or more at random 24%). Six clans is very few; neither count is settled.
- Outcome scores by style are description only: styles were built without them, and clans in different styles played different maps and opponents.

**Clans:** as in the position table and the four-corner table above. Flagged clans are placed on the map but were not used to build it.

**Could not be done / proxy:**
- With 24 clans and 17 scores no method can prove sharp types; the corners have soft borders and the borderline clans can flip under resampling.
- How the new outcome scores line up with the two scales (correlation across the 24 clans, description only): died per 100 +0.17 with the first scale and -0.57 with the second; caught per 100 +0.16 and -0.51; nearest cap taken -0.25 and +0.10; contested cap not lost +0.40 and +0.25 (24 clans).

**Verdict:** Lead

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| First scale share | 29.6% | 29.6% | clock |
| Second scale share | 17.8% | 17.8% | clock |
| Third scale share | 11.6% | 11.5% | clock |
| Largest change in a loading | - | 0.01 | clock |
| Largest shift of a clan, first scale | - | 0.02 (HTDOG) | clock |
| Largest shift of a clan, second scale | - | 0.09 (HTDOG) | clock |
| Clans that change style | - | none | unchanged |
| Borderline clans | HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | unchanged |
| Mean share of resamples in which a clan keeps its style | 86% | 86% | clock |
| Top 6 minus Rest, first scale | -1.59 (-3.58 to +0.46) | -1.59 (-3.58 to +0.47) | clock |
| Top 6 minus Rest, second scale | +1.18 (+0.19 to +2.23) | +1.16 (+0.16 to +2.21) | clock |

Style outcome rows, round 5b -> round 5c:

| Score | Team smoke, plenty | Own smoke, plenty | Team smoke, little | Own smoke, little | Why |
|---|---|---|---|---|---|
| Deaths per 100 smokes -> Died per 100 smokes | 9.6 -> 14.5 | 9.4 -> 13.6 | 15.5 -> 25.0 | 19.2 -> 27.5 | new death metric |
| Deaths per 100 smokes -> Caught per 100 smokes | 9.6 -> 9.6 | 9.4 -> 9.4 | 15.5 -> 15.5 | 19.2 -> 19.2 | unchanged |
| Smoker died per 100 smokes | new: 10.0 | new: 11.2 | new: 16.4 | new: 24.2 | new death metric |
| Smoker caught per 100 smokes | new: 5.1 | new: 7.8 | new: 8.6 | new: 15.8 | new split |
| Nearest cap taken (% of smokes where it was not ours) (snapshots -> timeline) | 26.1 -> 35.5 | 23.7 -> 28.6 | 18.4 -> 25.0 | 25.7 -> 30.0 | cap timeline |
| Contested cap taken (% of smokes where it was not ours) | new: 29.6 | new: 22.9 | new: 19.1 | new: 22.7 | cap timeline |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (snapshots -> timeline) | 88.1 -> 84.1 | 93.4 -> 88.2 | 85.3 -> 76.5 | 91.5 -> 89.4 | cap timeline |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 78.6 | new: 86.1 | new: 69.7 | new: 85.4 | cap timeline |
| Nearest caps taken with a smoke per game | 0.59 -> 0.80 | 0.70 -> 0.80 | 0.27 -> 0.38 | 0.52 -> 0.61 | cap timeline |
| First smoke of the game (median, s) | 163.0 s -> 162.2 s | 207.0 s -> 206.3 s | 185.5 s -> 184.4 s | 221.0 s -> 219.7 s | clock |
| Smokes after 12:00 (%) | 13.3 -> 13.2 | 13.8 -> 13.3 | 7.8 -> 7.8 | 5.8 -> 5.8 | clock |

The batch `cap_def` row of the round 5b style table is dropped. Style members, games, smokes and W-L are the same as round 5b.

### D3. Compact profile per clan for a gauge graphic

**Answer:** The gauge profile is unchanged: one headline number per dimension, its position among the 24 clans, and a 95% range. The six headline numbers are identical to round 5b for 30 of 30 clans. Each clan now also carries the new scores (died and caught per 100, smoker-only versions, caps taken and not lost from the timeline). `clan_styles.json` keeps round 5b's structure, so the file can be swapped in.

**Numbers:** headline score per dimension (as round 5) and what "high" means:

| Dimension | Headline score | High means |
|---|---|---|
| Lineup | Cruisers carrying smoke per game | more cruisers that carry smoke in the lineup |
| Volume and tempo | Smokes per game | more smokes per game |
| Who it is for | For a teammate (%) | more smokes laid for a teammate |
| Where | Inside a cap (%) | more smokes inside a cap |
| Movement | Parked (%) | more smokes laid while parked |
| What it buys | Concealed damage per game | more concealed damage per game |

Two contrasting clans (value, 95% range, percentile):

| Dimension | H-SR | HTDOG |
|---|---|---|
| Lineup | 0.1 (0.0 to 0.2), p4 | 1.3 (1.0 to 1.6), p91 |
| Volume and tempo | 4.5 (3.7 to 5.4), p52 | 5.9 (4.4 to 7.4), p83 |
| Who it is for | 82% (73 to 91), p100 | 47% (32 to 61), p22 |
| Where | 16% (10 to 23), p17 | 25% (17 to 32), p57 |
| Movement | 8% (3 to 15), p0 | 46% (33 to 60), p96 |
| What it buys | 68,194 (48,505 to 89,537), p83 | 50,375 (31,496 to 71,640), p65 |

The new scores as they sit in the same two profiles (value, 95% range, percentile; for deaths a high percentile is worse):

| Score | H-SR | HTDOG |
|---|---|---|
| Died per 100 smokes | 6.0 (1.2 to 11.2) p0 | 10.4 (4.1 to 17.4) p17 |
| Caught per 100 smokes | 4.0 (0.0 to 8.9) p0 | 6.6 (2.1 to 12.2) p9 |
| Smoker died per 100 smokes | 4.0 (0.9 to 7.5) p4 | 8.5 (3.4 to 15.0) p30 |
| Smoker caught per 100 smokes | 2.0 (0.0 to 4.9) p9 | 5.7 (1.9 to 10.4) p30 |
| Nearest cap taken (% of smokes where it was not ours) | 56 (46 to 69) p100, n 50 | 30 (17 to 48) p48, n 53 |
| Contested cap taken (% of smokes where it was not ours) | 42 (33 to 52) p96, n 65 | 27 (15 to 40) p52, n 60 |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 86 (74 to 96) p50, n 37 | 85 (66 to 100) p40, n 33 |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 86 (73 to 96) p70, n 44 | 88 (72 to 100) p80, n 41 |
| Nearest caps taken with a smoke per game | 1.1 (0.9 to 1.5) p96 | 0.7 (0.4 to 1.1) p65 |
| Contested caps taken with a smoke per game | 1.1 (0.8 to 1.4) p91 | 0.7 (0.4 to 1.1) p70 |

JSON: top-level keys `batch`, `note`, `dimensions`, `extra_scores`, `clans`, `styles`, `structure`, `top6_minus_rest`; per clan `games`, `wins`, `losses`, `group`, `flagged_small`, `smokes`, `destroyer_smokes`, `values`, `percentiles`, `intervals`, `gauge`, `axes`, `style`, `style_id`, `style_note`, `style_kept_share`, `notes`. Structure equal to round 5b's file: yes. Each clan has 40 scores in `values` (round 5b 35). Added keys: `we_took_n_pct`, `we_took_c_pct`, `not_lost_n_pct`, `not_lost_c_pct`, `died_per100`, `caught_per100`, `died_smoker_per100`, `caught_smoker_per100`, `caps_taken_c_pg`, `died_pg`, `caught_pg`. Removed keys: `took_pct`, `held_pct`, `deaths_per100`, `cap_won_pg`, `cap_def_pg`, `deaths_pg`. `caps_taken_pg` keeps its key but is now counted from the timeline. `gauge` and `axes` keep their shape; the "What it buys" entry in `dimensions` now lists the new score keys. Style-level numbers (`styles[].numbers`) carry the same new keys, with `n` for the rates.

**Top 6 or Shared:** on the six headline numbers the only clear Top 6 gap is still concealed damage per game (+5,334 to +33,897 *); the other five are Shared: Cruisers carrying smoke per game -0.5 to +0.2; Smokes per game -0.4 to +1.6; For a teammate (%) -2.5 to +20.2; Inside a cap (%) -7.7 to +4.2; Parked (%) -11.4 to +13.5.

**Clans:** all 30; six flagged (BTLST, INCA, MANBA, OGF, RMN, KM) carry `flagged_small: true` and their percentile is where they would fall among the 24.

**Could not be done / proxy:**
- Ranges are wide for clans with few games; a gauge should draw the range, not only the dot.
- Percentiles rank clans against each other; a high percentile is not "good". The four death scores are the ones where high is worse.
- Cap rates are null ("too few") for the clans listed under D1; the design side should show them as missing, not zero.

**Verdict:** Keep

**Changed from round 5b:**

| Part of the file | Round 5b | Round 5c | Why |
|---|---|---|---|
| `gauge` (six headline numbers, percentiles, ranges) | 30 clans | identical for 30 of 30 clans | unchanged |
| `style`, `style_id` | 30 clans | identical for all 30 clans | unchanged |
| `axes` (positions and ranges, 2 decimals) | 30 clans | 24 clans differ in some rounded figure; largest position shift 0.09 | clock |
| `values` / `percentiles` / `intervals` | 35 scores | 40 scores: 11 added, 6 removed, `caps_taken_pg` recounted, three time scores on the replay clock | new death metric / cap timeline / clock |
| `style_note`, `style_kept_share` | borderline: HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | borderline: HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | unchanged |
| `top6_minus_rest` | 35 gaps | 40 gaps; see the full old and new list under D1 | new death metric / cap timeline / clock |
| `styles[].numbers` | took_pct, held_pct, deaths_per100, cap_def_pg | the ten "what it buys" scores and two caps-per-game counts | new death metric / cap timeline |

Per-clan numbers that moved are listed in full for the Top 6 and PN, and for the other clans, under D1 "Changed from round 5b". Positions on the two scales for all 30 clans, old and new, are in the D2 table.

Top 6 and PN, positions on the two scales as stored in `axes` (round 5b -> round 5c):

| Clan | First scale | Second scale | Style |
|---|---|---|---|
| *H-SR | -4.58 -> -4.57 | +0.32 -> +0.28 | Team smoke, plenty of it (same) |
| *RESIN | -2.38 -> -2.39 | +1.15 -> +1.15 | Team smoke, plenty of it (same) |
| *BONKZ | -2.22 -> -2.23 | +0.90 -> +0.91 | Team smoke, plenty of it (same) |
| *HTDOG | +2.49 -> +2.51 | +0.74 -> +0.65 | Own smoke, plenty of it (same) |
| *KITE | -1.16 -> -1.16 | +0.25 -> +0.26 | Team smoke, plenty of it (same) |
| *VRTUS | +0.68 -> +0.68 | +1.97 -> +1.97 | Own smoke, plenty of it (same) |
| PN | -2.89 -> -2.89 | -3.29 -> -3.29 | Team smoke, little of it (same) |

