# How the top clans use smoke

Batch `output/20261116-214739`: 1,547 smokes, 171 games, 30 clans. Read-only analysis; reproduce with
`python -I -X utf8 smoke/analysis/top_clans.py output/20261116-214739` (about 4 minutes).

**Groups.** Top 8 by win % with 7+ games: H-SR (91%), RESIN (71%), HTDOG (67%), KITE (64%), VRTUS (64%), MZY (63%), BONKZ (62%), REEEE (62%). They have 142 team-games and 640 smokes. Everyone else (22 clans, 6 of them under 7 games) has 200 team-games and 907 smokes. The cut is close: HFANS, the next clan, is at 59%.

**Damage.** Guns only (shell + fire + airstrike). In this batch the smoke damage columns already hold nothing else, so no torpedo credit is in any number here.

## The 5 clearest differences

1. **Top clans die in their smoke less often.** 8.1 smoke deaths per 100 smokes against 13.8 (difference -5.7, 95% CI -9.8 to -2.4; 7 of the 8 top clans are below the rest-of-field figure). Most of this follows the result, not the clan: in losses the two groups are close (16.0 vs 19.3), and in wins too (4.5 vs 6.1).

2. **More of their smokes produce concealed damage.** 73.9% of top-clan smokes dealt some concealed damage against 63.5% (+10.4 points, CI +2.3 to +18.3). Per smoke that is 10,510 against 8,095 (+2,415, CI -121 to +4,958, so the size is uncertain). In the 78 games where a top clan met a rest clan the gap is +5,389 per smoke (CI +2,597 to +8,219).

3. **They share smoke more.** Stacked share 30.8% against 23.2% (+7.6 points, CI -1.2 to +16.8; 7 of 8 top clans above), selfish share 36.6% against 46.0% (-9.4 points, CI -20.0 to +0.9). This holds whether they win or lose (stacked 32% and 28% for the top 8, 24% and 23% for the rest), so it looks like style, not a side effect of winning. The interval touches zero and HTDOG is the exception (14% stacked, 53% selfish).

4. **They pair smoke with radar about twice as often.** Cap control (radar used from a smoke covering the contested cap) is the main purpose of 8.4% of their smokes against 4.0% (+4.5 points, CI +1.5 to +6.9; 54 and 36 smokes). Radar trap is 2.7% against 1.1%, all 8 top clans above, but that is 17 and 10 smokes: small sample. Both rates are the same in wins and losses.

5. **Where they smoke differs on three maps, not overall.** Sleeping Giant: west 49% against 33%, center 23% against 39%. Land of Fire: west 16% against 38%, center 63% against 43%. Sea of Fortune: west 33% against 53%, center lane 31% against 12%. Across all maps the distance to the contested cap is the same (3,035 m against 2,927 m).

**What does not differ.** Smokes per game (4.51 vs 4.54), time of first smoke (3.66 vs 3.84 minutes), the cap contest share (32% vs 33%), and the movement mix. The top 8 smoke more in the first two minutes (0.24 against 0.10 per team-game), but 12 of those 34 smokes are H-SR, so that is one clan's habit, not a group trait.

## Association versus cause

- Everything here is association. Nothing shows that smoking this way makes a clan win.
- The outcome measures (smoke deaths, concealed damage, kills from smoke) partly run backwards: a team that is losing has ships sunk, including in smoke, and has fewer guns left to fire from it. Differences 1 and 2 mostly describe winning, not a choice.
- The choice measures (stacked share, radar pairing, map zones) do not move with the result, so they are the better candidates for real style differences. They may still reflect ship lineups (top clans' smokes are 74% destroyer against 66%) or the opponents and maps each clan drew.
- The top group is only 8 clans. Intervals resample whole clans, so they are wide; one clan can move a group number (H-SR alone is 100 of the 640 smokes and half its smokes are stacked).
- About 30 metrics and 42 map cells were tested. Expect one or two starred rows in each table by chance alone.

## Supporting tables

A star marks an interval that excludes zero. "Top clans above" counts how many of the 8 sit above the rest-of-field value.

### Top 8 vs rest, all smokes

| Metric | Top 8 | Rest | Difference | 95% CI (by clan) | Top clans above |
|---|---|---|---|---|---|
| Smokes per game | 4.51 | 4.54 | -0.03 | -1.07 to +1.10 | 4 of 8 |
| Smokes per 10 min played | 3.32 | 3.50 | -0.18 | -0.88 to +0.61 | 2 of 8 |
| First smoke, minutes elapsed | 3.66 | 3.84 | -0.18 | -0.81 to +0.41 | 5 of 8 |
| Stacked share | 30.8% | 23.2% | +7.6 pt | -1.2 to +16.8 | 7 of 8 |
| Screen share | 32.7% | 30.9% | +1.8 pt | -3.3 to +6.4 | 6 of 8 |
| Selfish share | 36.6% | 46.0% | -9.4 pt | -20.0 to +0.9 | 2 of 8 |
| Mean distance to contested cap, m | 3,035 | 2,927 | +108 | -400 to +679 | 5 of 8 |
| Within 1 km of contested cap | 37.3% | 35.2% | +2.2 pt | -3.7 to +7.1 | 5 of 8 |
| Concealed damage per smoke | 10,510 | 8,095 | +2,415 | -121 to +4,958 | 6 of 8 |
| Smokes with any concealed damage | 73.9% | 63.5% | +10.4 pt * | +2.3 to +18.3 | 6 of 8 |
| Smoke deaths per 100 smokes | 8.1 | 13.8 | -5.7 * | -9.8 to -2.4 | 1 of 8 |
| Kills from smoke per 100 smokes | 9.5 | 6.6 | +2.9 * | +0.3 to +5.3 | 7 of 8 |
| Purpose: cap contest | 32.2% | 33.0% | -0.8 pt | -6.1 to +4.0 | 3 of 8 |
| Purpose: none tagged | 27.0% | 30.2% | -3.2 pt | -7.8 to +1.9 | 3 of 8 |
| Purpose: cap control | 8.4% | 4.0% | +4.5 pt * | +1.5 to +6.9 | 7 of 8 |
| Purpose: reposition | 6.9% | 7.6% | -0.7 pt | -4.1 to +2.8 | 3 of 8 |
| Purpose: damage | 6.9% | 5.6% | +1.3 pt | -1.3 to +3.8 | 5 of 8 |
| Purpose: counter smoke | 6.7% | 7.3% | -0.6 pt | -4.1 to +3.0 | 5 of 8 |
| Purpose: escape | 5.9% | 6.9% | -1.0 pt | -3.4 to +1.5 | 2 of 8 |
| Purpose: island dive | 3.3% | 4.1% | -0.8 pt | -3.1 to +1.9 | 2 of 8 |
| Purpose: radar trap (small n) | 2.7% | 1.1% | +1.6 pt * | +0.7 to +2.5 | 8 of 8 |
| Movement: stationary | 27.8% | 28.0% | -0.2 pt | -10.8 to +10.1 | 4 of 8 |
| Movement: horizontal | 27.0% | 24.7% | +2.3 pt | -5.8 to +9.9 | 5 of 8 |
| Movement: pushing | 20.8% | 20.3% | +0.5 pt | -4.4 to +5.3 | 4 of 8 |
| Movement: kiting | 17.5% | 20.7% | -3.2 pt | -8.3 to +1.7 | 2 of 8 |

Destroyer smokes only (474 vs 600) tell the same story with three shifts: top-clan destroyers smoke 607 m further from the contested cap (2,904 vs 2,297 m, CI +70 to +1,193), push more (22.4% vs 16.0%, CI -0.2 to +11.9) and no top clan is above the rest on smoke deaths (8.0 vs 14.3 per 100).

### Timing: smokes per team-game still running

| Minutes | Top 8 smokes | Top 8 rate | Rest smokes | Rest rate | Note |
|---|---|---|---|---|---|
| 0 to 2 | 34 | 0.24 | 21 | 0.10 | 12 of the 34 are H-SR |
| 2 to 4 | 80 | 0.56 | 143 | 0.71 | |
| 4 to 6 | 114 | 0.80 | 198 | 0.99 | |
| 6 to 8 | 115 | 0.81 | 173 | 0.86 | |
| 8 to 10 | 112 | 0.81 | 163 | 0.84 | |
| 10 to 12 | 85 | 0.65 | 111 | 0.63 | |
| 12 to 14 | 59 | 0.60 | 64 | 0.58 | |
| 14 to 16 | 25 | 0.42 | 22 | 0.33 | small n |
| 16 to 18 | 11 | 0.50 | 5 | 0.16 | small n |
| 18 to 20 | 5 | 0.33 | 7 | 0.64 | small n |

The rest of the field peaks at 4 to 6 minutes; the top 8 hold a flat rate from 4 to 10. No intervals were run on the bins, so read this as a shape, not a finding.

### Winners vs losers within each game

Paired difference is winner minus loser in the same game, averaged over games (153 games where both teams smoked; 171 for per-game rows).

| Metric | Winners | Losers | Mean paired difference | 95% CI (by game) |
|---|---|---|---|---|
| Smokes per game | 4.78 | 4.26 | +0.52 | -0.05 to +1.08 |
| First smoke, minutes elapsed | 3.66 | 3.86 | -0.20 | -0.65 to +0.25 |
| Stacked share | 28.1% | 24.3% | +1.5 pt | -4.6 to +7.4 |
| Selfish share | 40.6% | 43.8% | +2.9 pt | -4.0 to +9.7 |
| Mean distance to contested cap, m | 2,971 | 2,971 | +129 | -353 to +645 |
| Concealed damage per smoke | 10,853 | 7,121 | +4,484 * | +2,691 to +6,316 |
| Smokes with any concealed damage | 74.1% | 60.8% | +18.2 pt * | +12.1 to +24.0 |
| Smoke deaths per 100 smokes | 5.3 | 18.4 | -16.8 * | -21.5 to -12.1 |
| Kills from smoke per 100 smokes | 12.3 | 2.7 | +10.7 * | +7.4 to +14.0 |
| Purpose: damage | 7.7% | 4.4% | +3.0 pt * | +0.8 to +5.2 |
| Purpose: cap control | 5.9% | 5.8% | -1.4 pt | -4.5 to +1.7 |
| Movement: stationary | 30.4% | 25.1% | +8.0 pt * | +2.2 to +13.8 |
| Movement: kiting | 17.6% | 21.4% | -6.1 pt * | -11.8 to -0.6 |

Winners and losers smoke about as often, as early and as close to the cap. What separates them is what happens afterwards (damage, kills, deaths) and that losers kite more and sit still less, which is what a team under pressure does.

### Group by result

| Metric | Top 8, won | Top 8, lost | Rest, won | Rest, lost |
|---|---|---|---|---|
| Team-games / smokes | 98 / 440 | 44 / 200 | 73 / 378 | 127 / 529 |
| Smokes per game | 4.49 | 4.55 | 5.18 | 4.17 |
| Stacked share | 32.0% | 28.0% | 23.5% | 22.9% |
| Selfish share | 35.0% | 40.0% | 47.1% | 45.2% |
| Purpose: cap control | 7.5% | 10.5% | 4.0% | 4.0% |
| Purpose: radar trap | 2.7% | 2.5% | 1.3% | 0.9% |
| Concealed damage per smoke | 11,669 | 7,961 | 9,903 | 6,803 |
| Smoke deaths per 100 smokes | 4.5 | 16.0 | 6.1 | 19.3 |
| Kills from smoke per 100 smokes | 12.5 | 3.0 | 12.2 | 2.6 |

Rows that change across won and lost follow the result. Rows that change across top 8 and rest but not across won and lost (stacked, selfish, cap control, radar trap) are the style differences.

### Per map: zone and lane

All 7 maps have 10+ games. Zone is the map-profile zone (west, center, east); lane is the `lane` field. Each cell is the share of that group's smokes on the map.

| Map | Games | Group | Smokes | Clans | West | Center | East | Lane left | Lane center | Lane right |
|---|---|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | 32 | Top 8 | 142 | 7 | 49% | 23% | 29% | 46% | 20% | 35% |
| | | Rest | 163 | 18 | 33% | 39% | 28% | 40% | 11% | 49% |
| | | Difference, pt | | | +15 * | -17 * | +1 | +6 | +9 | -15 * |
| Hotspot | 31 | Top 8 | 118 | 8 | 22% | 31% | 47% | 36% | 14% | 51% |
| | | Rest | 170 | 22 | 22% | 35% | 44% | 38% | 12% | 49% |
| | | Difference, pt | | | 0 | -3 | +3 | -3 | +1 | +1 |
| Land of Fire | 26 | Top 8 | 79 | 7 | 16% | 63% | 20% | 25% | 48% | 27% |
| | | Rest | 134 | 20 | 38% | 43% | 19% | 36% | 34% | 31% |
| | | Difference, pt | | | -22 * | +20 | +2 | -11 | +15 | -4 |
| Loop | 23 | Top 8 | 81 | 8 | 9% | 44% | 47% | 41% | 17% | 42% |
| | | Rest | 108 | 20 | 19% | 47% | 34% | 42% | 21% | 37% |
| | | Difference, pt | | | -10 | -3 | +13 | -1 | -4 | +5 |
| Sea of Fortune | 21 | Top 8 | 86 | 8 | 33% | 36% | 31% | 42% | 31% | 27% |
| | | Rest | 112 | 21 | 53% | 22% | 25% | 43% | 12% | 46% |
| | | Difference, pt | | | -20 * | +14 | +6 | -1 | +20 * | -19 * |
| Mountain Range | 20 | Top 8 | 94 | 8 | 37% | 55% | 7% | 50% | 24% | 26% |
| | | Rest | 102 | 18 | 31% | 59% | 10% | 34% | 31% | 34% |
| | | Difference, pt | | | +6 | -4 | -2 | +16 | -7 | -9 |
| Okinawa (small n) | 18 | Top 8 | 40 | 8 | 38% | 45% | 18% | 12% | 35% | 52% |
| | | Rest | 118 | 19 | 40% | 36% | 25% | 40% | 26% | 34% |
| | | Difference, pt | | | -2 | +9 | -7 | -27 * | +9 | +19 |

Reading: Hotspot, Loop and Mountain Range show no clear split. Sleeping Giant (top 8 favour the west over the middle), Land of Fire (middle over the west) and Sea of Fortune (middle over the west and the right lane) do. Okinawa's left-lane gap rests on 40 top-clan smokes (5 of them on the left); treat it as a lead to check on the map, not a result. With 79 to 142 top-clan smokes per map, two or three clans' habits can produce any of these.

## Data notes

- 103 smokes (the owner-flagged ones) have no activation clock; their created clock is used for timing.
- Two games have no end time in games.csv (8074 game 1, 8151 game 3); their length is set to the last smoke plus one minute. This only touches the per-10-minute and timing rows.
- 19 team-games have no smoke at all (9 top, 10 rest); they count as zero in smokes per game and are left out of first-smoke time.
- Distance to contested cap is `avg_contested_cap_dist_m` (negative inside the cap). Concealed damage is `smoke_damage_concealed`.
- Torpedo credit is not in these numbers. If the parallel round adds it, differences 1, 3, 4 and 5 are unaffected; difference 2 should be rerun.
