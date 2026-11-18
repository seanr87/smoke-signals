# Round 5b findings, worker n3: Harugumo spotting per shot (B3) and Daring smokes after radar on Loop (C5)

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
