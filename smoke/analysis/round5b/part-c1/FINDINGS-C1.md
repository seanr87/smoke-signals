# Round 5, part C1: findings (caps and danger zones)

Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Everything here is association, not cause.
Full tables: `out-caps.md` (C1, C2) and `out-danger.md` (C3). Cap letters are in the team frame (own spawn at the bottom), so a letter means the same place for both teams.

### C1. Cap defence

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

