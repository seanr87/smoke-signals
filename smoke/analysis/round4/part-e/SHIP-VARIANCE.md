# Part E: ship variance (Grozovoi, Shimakaze; emission and radius)

Batch `output/20261117-122135` (1,547 smokes, 171 games). Everything here is association, not cause. Intervals are 95%, by resampling clans (1000 reps); `*` = excludes zero. n 8 to 14 = small n.

## Findings

**1. Grozovoi and Shimakaze do not split into two clean modes. They are a mix, and the mix leans toward smoke lines, not cap sitting.**
A two-group split on seven per-smoke features separates Grozovoi (silhouette 0.26, n=30) and Shimakaze (0.25, n=58) no better than it separates Daring (0.26) and Gdansk (0.28). Random Daring samples of the same size split at least as cleanly 57% of the time (vs Grozovoi) and 78% (vs Shimakaze); Gdansk samples 78% and 98%. Every one of these ships has parked smokes and moving smokes with no gap between them (fig 3). What differs is the share of each: smokes that look more like a Somers/Gearing smoke line than a Daring cap sit ("smoke-line mode": long, moving, stacked or on a flank) are **64% of Shimakaze** (52 to 78), **53% of Grozovoi** (34 to 83), 41% of Gdansk (33 to 51) and 10% of Daring (3 to 16). Shimakaze minus Daring +54 points (+40 to +67 *); Grozovoi minus Daring +43 (+25 to +73 *); Shimakaze minus Gdansk +23 (+7 to +38 *); Grozovoi minus Gdansk +13 (-7 to +44, not clear).
For a player: do not read "cap sitter" as the norm for these two ships. Most Shimakaze smokes in this tournament were moving lines laid well outside the cap; a parked Shimakaze smoke in the cap was the minority use.

**2. The other spread numbers say the same thing.** Stationary share: Daring 64%, Gdansk 41%, Shimakaze 26%, Grozovoi 20% (Shimakaze minus Daring -38 points, -52 to -25 *; Grozovoi -44, -63 to -20 *). Stacked with another smoke: Shimakaze 48% vs Daring 10% (+38, +26 to +55 *). Median length laid: Shimakaze 1.7 km, Grozovoi 0.8 km, Gdansk 0.8 km, Daring 0.4 km. Spread of smoke centres on a map: Shimakaze 13.5 km vs Daring 9.7 km (+3.8, +0.6 to +5.9 *); Grozovoi 12.3 km (+2.6, -1.3 to +8.5, not clear). Share inside the cap is similar for all four (26 to 42%; no clear difference for Grozovoi or Shimakaze).
For a player: nothing actionable beyond finding 1.

**3. On Shimakaze the two uses are not a clan, map or time thing: the same players do both.** Mode vs clan: permutation p = 0.23; vs map 0.46; vs win/loss 1.0. All 5 players with 5+ Shimakaze smokes used both; 3 of 4 player-games with 3+ smokes had both in the same game. Smoke-line smokes come about 100 s earlier in the game (median 460 s vs 564 s) but that gap is not clear (p = 0.17). Dropping any one clan moves the smoke-line share only between 61% and 68%. Top 6 (n=15) 60% vs Rest (n=43) 65%: no difference (-36 to +26). No sign of a separate torpedo-run mode: torpedo damage from smoke is similar in both groups (about 1,200 to 1,600 per smoke).
For a player: nothing actionable; the choice looks situational, smoke by smoke.

**4. Grozovoi cannot be settled: half the data is one clan, and most of that is one player.** MACHX laid 15 of 30 (one player, 11). That player's smokes are mostly short solo smokes (3 of 11 smoke-line, none stacked); everyone else is 13 of 19 smoke-line. So mode does line up with player on Grozovoi (p = 0.01), but that is one player against 10 other players with 1 to 3 smokes each. Without MACHX the smoke-line share is 60% (n=15, 7 clans); MACHX alone is 47%. MACHX also tightens the map picture: its smokes spread 8 km around their centre, the other clans' 16 km. The safe statement is "Grozovoi sits between Daring and Shimakaze, interval 34 to 83%"; MACHX pulls it toward the cap-sitting end and does not create the mix on its own. Top 6 have only 6 Grozovoi smokes: no comparison.
For a player: nothing actionable (small n).

**5. Radius never varies within a ship.** All 1,547 smokes have the ship's base radius (Daring, Z-42, Svea 600 m; Italian exhaust 510 m; the rest 450 m). The single exception (a "Napoli" smoke at 450 m) is a smoke whose owner was guessed, so it is an attribution error, not a build.
For a player: nothing actionable.

**6. Emission length varies a lot within a ship, in fixed steps, and the step belongs to the player.** Observed emission sits at about 1.1x, 1.3x and 1.45x the base: Somers and Gearing (base 30 s) cluster at 33, 40 and 43 to 44 s; Daring (10 s) at 10 and 11 s; Gdansk, Shimakaze, Grozovoi (20 s) at 20, 22 and 26 to 27 s. Each player sits on one step: 81 to 100% of a player's smokes are within about 1.5 s of that player's own median, and the typical within-player quartile range is 0.2 to 0.7 s. Players account for 98% of the variation on Gearing, 97% Napoli, 72% Gdansk, 60% Somers, 39% Daring (the rest is mostly measurement step on a 10 s smoke). A few players changed step between games (Somers 3 of 16, Svea 4 of 12, Harugumo 2 of 6). This is what build differences would look like. Caveat, exactly: upgrades and captain skills change smoke length and maybe size; the data sees the observed smoke, not the build.
For a player: on Somers and Gearing most players (14 of 25 and 9 of 21 with 3+ smokes) run the middle step, about 40 s; only 3 and 5 run close to base. That is a count of what was brought, not evidence it works better.

**7. Emission length does not line up consistently with how the smoke is used.** Within a ship, median emission is the same whether the smoke is parked or moving, inside or outside the cap, with or without concealed damage (table 3). Comparing longer vs shorter emitters gives one clear pattern on one ship: Somers long (n=202) vs near-base (n=24, small group, 10 clans) are stacked more (67% vs 42%, +8 to +47 *), less often solo (2% vs 33%, -56 to -11 *) and have more concealed damage per smoke (16.2k vs 8.7k, +2.1k to +13.6k *). Gearing (103 vs 55) and Harugumo (48 vs 35) show none of this (all intervals include zero). With 56 comparisons, a few clear ones are expected by chance. Longer emission does lay a longer line when moving (rank correlation 0.33 to 0.42 on Somers, Gearing, Harugumo), which is mechanical.
For a player: nothing actionable.

**8. Cut short is rare except on Italian exhaust smoke.** 80 of 1,547 (5%) ended because the smoker died while emitting: 1 to 8% on destroyers, Svea and Jinan, 11% Napoli, 14% Venezia (n=21), 20% C. Colombo (n=20). A 45 to 50 s moving emission simply leaves more time to be sunk mid-smoke.
For a player: nothing actionable.

PN: one smoke on these four ships (a Gdansk smoke-line smoke on Okinawa); no PN Grozovoi or Shimakaze data.

## Figures

- `fig1-modes-map-views.png`: Grozovoi, Shimakaze, Daring, Gdansk on Hotspot, Loop, Mountain Range, Sea of Fortune, coloured by mode; MACHX outlined.
- `fig2-shimakaze-other-maps.png`: Shimakaze on Okinawa (9 of 11 are flank lines on the west side, small n), Land of Fire, Sleeping Giant, with Daring and Gdansk.
- `fig3-modes-length-vs-cap.png`: length laid against distance to the cap, the same modes without the map.
- `fig4-emission-by-ship.png`: every smoke's observed emission by ship, base marked, cut-short in red.

Position transform: team-normalized, own spawn at the bottom; north-spawn teams mirrored north-south; on Okinawa mirrored across the NW-SE diagonal (own spawn bottom left).

## Tables

**Table 1. Within-ship spread** (95% interval in brackets)

| ship | n | clans | spread of centres, km | stationary % | stacked % | inside cap % | edge to cap, median m | length laid, median m | smoke-line % |
|---|---|---|---|---|---|---|---|---|---|
| Grozovoi | 30 | 8 | 12.3 (8.0 to 17.6) | 20 (6 to 44) | 20 (12 to 42) | 33 (21 to 62) | 998 | 818 | 53 (34 to 83) |
| Shimakaze | 58 | 12 | 13.5 (9.8 to 14.4) | 26 (12 to 37) | 48 (37 to 62) | 33 (21 to 48) | 3,288 | 1,717 | 64 (52 to 78) |
| Daring | 200 | 20 | 9.7 (7.6 to 10.1) | 64 (55 to 73) | 10 (3 to 17) | 42 (32 to 51) | 671 | 386 | 10 (3 to 16) |
| Gdansk | 118 | 16 | 10.3 (7.8 to 10.9) | 41 (34 to 47) | 16 (10 to 26) | 26 (16 to 38) | 1,544 | 765 | 41 (33 to 51) |

For reference, smoke-line %: Z-42 16, Somers 95, Gearing 90, Harugumo 88, Delny 91.

**Table 2. Clans with the most smokes** (smoke-line count / n)

| ship | clan | n | smoke-line | stationary % | stacked % | edge median m | maps |
|---|---|---|---|---|---|---|---|
| Grozovoi | MACHX | 15 | 7/15 | 13 | 13 | 1,381 | Hotspot 6, Sea of Fortune 5, Loop 4 |
| Grozovoi | - MACHX main player | 11 (small n) | 3/11 | 18 | 0 | 2,315 | |
| Grozovoi | 7 other clans together | 15 | 9/15 | 27 | 27 | 692 | Hotspot 8, Mountain Range 5, Loop 2 |
| Shimakaze | HFANS (one player) | 13 (small n) | 9/13 | 23 | 54 | 5,610 | Okinawa 5, Sea of Fortune 4, Mountain Range 3 |
| Shimakaze | 5D (two players, 2/5 and 1/3) | 8 (small n) | 3/8 | 50 | 25 | -46 | Hotspot 4 |
| Shimakaze | 10 other clans together | 37 | 25/37 | 22 | 51 | | |

No clan has two players with 8+ smokes on either ship, so a within-clan player comparison is not possible. Full per-clan and per-player rows are in `ship-variance.json` and `run-output.txt`.

**Table 3. Observed emission, ships with 20+ smokes**

| ship | n | base s | median s | quartiles s | x base | cut short | players (3+ smokes) | variation between players | radius m |
|---|---|---|---|---|---|---|---|---|---|
| Somers | 260 | 30 | 39.7 | 39.5 to 43.4 | 1.32 | 10 (4%) | 25 | 60% | 450 |
| Daring | 200 | 10 | 11.0 | 10.3 to 11.3 | 1.10 | 6 (3%) | 24 | 39% | 600 |
| Svea | 199 | 10 | 12.0 | 11.0 to 12.6 | 1.20 | 2 (1%) | 27 | 63% | 600 |
| Gearing | 180 | 30 | 39.6 | 33.3 to 40.1 | 1.32 | 8 (4%) | 21 | 98% | 450 |
| Napoli | 147 | 40 | 48.3 | 44.3 to 48.6 | 1.21 | 16 (11%) | 11 | 97% | 510 |
| Gdansk | 118 | 20 | 22.2 | 22.0 to 22.5 | 1.11 | 9 (8%) | 13 | 72% | 450 |
| Harugumo | 100 | 20 (see cautions) | 52.7 | 44.0 to 55.6 | 2.64 | 3 (3%) | 12 | 57% | 450 |
| Shimakaze | 58 | 20 | 22.1 | 22.0 to 23.0 | 1.11 | 4 (7%) | 6 | 55% | 450 |
| Z-42 | 56 | 10 | 11.4 | 10.5 to 12.2 | 1.14 | 2 (4%) | 11 | 88% | 600 |
| Jinan | 42 | 30 | 31.2 | 30.3 to 33.3 | 1.04 | 3 (7%) | 6 | 84% | 450 |
| Grozovoi | 30 | 20 | 21.8 | 20.2 to 22.4 | 1.09 | 2 (7%) | 2 | too few players | 450 |
| Delny | 22 | 30 | 43.4 | 40.0 to 43.7 | 1.45 | 0 | 3 | too few players | 450 |
| Venezia | 21 | 40 | 48.6 | 44.2 to 53.4 | 1.21 | 3 (14%) | 3 | too few players | 510 |
| C. Colombo | 20 | 45 | 49.5 | 45.1 to 49.9 | 1.10 | 4 (20%) | 0 | - | 510 |

Median emission by use, within ship (smokes not cut short): Daring parked 11.0 s vs moving 11.1; Gdansk 22.2 vs 22.3; Shimakaze 22.1 vs 22.2; Svea 12.0 vs 12.4; inside vs outside the cap and with vs without concealed damage differ by 0.3 s or less on every ship with 100+ smokes.

## Method

- Features per smoke: length laid (log), distance from smoke edge to contested cap edge, sideways distance from the map's centre line, how far forward, stationary or not, stacked or not, solo ("selfish" coverage) or not. Standardized.
- Two-group split: k-means with two groups per ship, 25 restarts; quality = silhouette (0 = no separation, 1 = perfect). Compared with the same split on 300 random samples of Daring and of Gdansk at n=30 and n=58.
- Modes: each smoke is labelled by whichever ship profile it is nearer, cap sitters (Daring, Z-42, Gdansk) or smoke lines (Somers, Gearing, Harugumo, Delny); a ship is left out of its own profile. This label agrees with the unsupervised split on 97% of Grozovoi smokes and 71% of Shimakaze smokes.
- Lines up with clan, player, map, result: permutation test (2000 shuffles of the mode labels). It treats smokes as independent, so treat p-values as rough.
- Emission: `obs_emission_s` = time from activation to the last new puff (before the first puff fades), so it is measured in puff steps and runs a little over the true value (e.g. 33.3 for 33). "Cut short" = the smoker died while emitting. Player and usage comparisons exclude cut-short smokes, smokes whose owner was guessed, and smokes under 0.9x base.

## Cautions

- Grozovoi: 30 smokes, 8 clans, half from MACHX and 11 from one player. Every Grozovoi number has a wide interval.
- Shimakaze: 58 smokes, 12 clans, HFANS 13. Per-map views have 4 to 13 smokes each (small n).
- The modes are a label on a continuum, not two separate clusters; a smoke near the boundary could fall either way.
- Harugumo's base emission in the data (20 s) looks wrong: its smokes cluster at 44, 53 and 58 s, which are the same 1.1x / 1.3x / 1.45x steps on a base of 40 s, not 20 s. The "2.64x" is probably a base-value error, not an extreme build.
- 14 smokes ended well short of base without being flagged cut short (7 on Daring). Cause unknown (not the smoker's death); excluded from the player comparisons.
- Emission steps are read from the observed smoke only. The data does not contain upgrades or captain skills.
