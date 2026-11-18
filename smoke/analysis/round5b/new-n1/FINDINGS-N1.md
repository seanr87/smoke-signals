# Round 5b findings, worker n1: C1 and C2 redone from the cap timeline

Batch `output/20261117-230933`. 1,547 smokes, 171 games, 30 clans. Everything is association, not cause. Intervals are 95%, by resampling whole clans (C1) or whole games (C2). "Clear" = the interval excludes zero.
This file is written by `n1_findings.py` from the numbers computed in `n1_c1.py` and `n1_c2.py`.

### C1. Cap defence: "enemy took the cap" from the timeline, and ribbons

**Answer:** With the full cap timeline, the enemy took the nearest cap during the smoke or within 60 seconds after it in 21.7% of the smokes where the question applies (233 of 1,074); round 5 said 17.1% (184). Strictly while the smoke stood it is 14.4% (155). The round 5 snapshot version never said yes wrongly, but it missed 48 of 232 real flips (20.7%), more than the 15% estimated then. The Top 6 vs Rest gaps that round 5 called clear are not clear any more; the snapshots had missed more Top 6 flips (27%) than Rest flips (18%). Ribbons can now be counted, but only 268 of 1,547 smokes covered a recording player, so they are a check on the timeline, not a measure.

**Numbers: three ways** (nearest cap by geometry; "not applicable" = the cap was already the enemy's at activation)

| what | applicable smokes | strictly while the smoke stood | only in the 60 s after it cleared | during or within 60 s |
|---|---|---|---|---|
| enemy took the nearest cap | 1,074 | 155 (14.4%) | 78 (7.3%) | 233 (21.7%) |
| we took the nearest cap (cap not ours at activation) | 853 | 196 (23.0%) | 76 (8.9%) | 272 (31.9%) |

- Grace after the smoke clears, enemy took: 0 s: 155 (14.4%) [round 5: 103, 9.6%]; 10 s: 173 (16.1%); 30 s: 199 (18.5%); 60 s: 233 (21.7%) [round 5: 184, 17.1%]; 120 s: 293 (27.3%) [round 5: 233, 21.7%].
- Not applicable: 473 smokes (round 5: 474). Owner of the nearest cap at activation agrees with the round 5 stored value in 1545 of 1,547 smokes; the 2 others flipped within a second of the activation.

**Numbers: timeline against the round 5 snapshot version, same smokes, 60 s grace both**

| enemy took: round 5 snapshot \ timeline | yes | no | not applicable |
|---|---|---|---|
| yes | 184 | 0 | 0 |
| no | 48 | 841 | 0 |
| n/a | 1 | 0 | 473 |

- Enemy took: both versions apply to 1,073 smokes. They agree on 1,025 (95.5%). Snapshot missed a flip: 48. Snapshot wrong the other way: 0. So the snapshot version missed 20.7% of the 232 real flips. In 46 of the 48 misses the cap was still the enemy's at the end of the window: the flip simply came after the last snapshot.
- By group: Top 6 79 real flips, 21 missed (27%); Rest 153 real flips, 27 missed (18%). Both groups had the same number of snapshots per smoke (mean 5.3 and 5.2), so this is how the misses happened to fall, not a coverage difference.
- We took: both apply to 852; agree 790 (92.7%); snapshot missed 62 of 271 real flips (22.9%); wrong the other way 0.
- Checks. (1) A second computation straight from the timeline rows agrees on all 1,547 smokes (0 mismatches). (2) The batch field `cap_won` names the nearest cap in 171 smokes: the timeline says "we took it" in 170 (1 not applicable); the snapshot version found 144. (3) Team-frame cap letters from the timeline file match the round 5 geometry in every smoke.

**Numbers: summary tables from the timeline** (during the smoke or within 60 s after; last two columns are round 5)

| group | n | enemy took it (interval) | Top 6 | Rest | Top 6 - Rest | strictly during | round 5 share | round 5 gap |
|---|---|---|---|---|---|---|---|---|
| all applicable smokes | 1,074 | 21.7% (19.5 to 23.9) | 19.9% (n 403) | 22.8% (n 671) | -3.0 (-7.1 to +1.2) | 14.4%; gap -4.0 (-8.0 to +0.3) | 17.1% (n 1,073) | -4.4 (-8.9 to +0.1) |
| destroyer smokes | 763 | 23.1% (20.1 to 26.5) | 20.9% (n 292) | 24.4% (n 471) | -3.5 (-9.5 to +2.8) | 16.1%; gap -5.6 (-11.0 to +0.3) | 18.8% (n 762) | -5.9 (-12.1 to -0.9) clear |
| smoke centre inside or within 2 km of the cap | 541 | 16.1% (13.2 to 19.6) | 14.3% (n 189) | 17.0% (n 352) | -2.8 (-8.9 to +3.9) | 9.6%; gap -4.2 (-10.1 to +1.2) | 11.1% (n 541) | -4.8 (-9.2 to -0.7) clear |
| destroyer smokes inside or within 2 km | 405 | 17.5% (14.0 to 21.8) | 15.5% (n 142) | 18.6% (n 263) | -3.1 (-11.0 to +4.5) | 11.1%; gap -6.3 (-14.8 to +1.1) | 12.8% (n 405) | -6.8 (-12.6 to -1.7) clear |
| cap ours at activation | 694 | 18.2% (15.1 to 21.6) | 18.4% (n 261) | 18.0% (n 433) | +0.4 (-5.8 to +5.8) | 11.0%; gap -1.0 (-5.9 to +3.3) | 13.7% (n 694) | -1.6 (-8.2 to +5.0) |
| cap neutral at activation | 380 | 28.2% (23.3 to 33.9) | 22.5% (n 142) | 31.5% (n 238) | -9.0 (-18.3 to -0.2) clear | 20.8%; gap -9.6 (-17.4 to -0.4) clear | 23.5% (n 379) | -9.4 (-18.4 to -0.5) clear |
| cap ours, smoke within 2 km | 349 | 12.3% (8.5 to 16.1) | 11.2% (n 116) | 12.9% (n 233) | -1.7 (-11.1 to +6.8) | 5.7%; gap -3.4 (-9.4 to +2.3) | 8.0% (n 350) | -4.2 (-9.7 to +1.5) |
| cap ours, cap_defended set for that cap | 153 | 45.8% (37.9 to 53.3) | 48.1% (n 52) | 44.6% (n 101) | +3.5 (-13.1 to +20.0) | 28.1%; gap -7.6 (-22.0 to +4.7) | 35.9% (n 153) | -7.8 (-24.7 to +10.5) |
| cap ours, cap_defended not set for it | 541 | 10.4% (8.1 to 13.0) | 11.0% (n 209) | 9.9% (n 332) | +1.1 (-3.7 to +5.3) | 6.1%; gap +1.8 (-1.9 to +5.1) | 7.4% (n 541) | +1.3 (-3.4 to +5.2) |

- By map and cap (team-frame letter; all 26 rows in `out-c1.md` and `caps.json`). Highest: Sea of Fortune C 40.0% (n 15; round 5 6.7%); Mountain Range B 39.1% (n 46; round 5 35.6%); Hotspot C 32.3% (n 65; round 5 26.2%); Okinawa D 30.8% (n 26; round 5 19.2%); Loop B 30.0% (n 30; round 5 20.0%).
- Clear Top 6 vs Rest gaps by map and cap now: Mountain Range C (Top 6 8.0% of 25, Rest 32.3% of 31; -24.3 (-42.6 to -3.5) clear). One clear row out of 17 rows with enough smokes on both sides is about what luck alone gives. The three round 5 rows are no longer clear: Loop A -15.9 (-37.0 to +2.9) (was -22.2 clear); Loop B -15.0 (-47.1 to +9.1) (was -30.0 clear); Mountain Range A +3.6 (-29.2 to +32.9) (was -17.5 clear).
- We took the nearest cap (60 s): all smokes where the nearest cap was not ours: 31.9% (n 853), Top 6 39.0% vs Rest 28.5%, gap +10.5 (-0.2 to +22.1); round 5 24.5%; destroyer smokes: 35.6% (n 582), Top 6 45.7% vs Rest 30.4%, gap +15.3 (+2.1 to +28.1) clear; round 5 27.0%; within 2 km: 42.3% (n 350), Top 6 50.4% vs Rest 38.3%, gap +12.1 (+1.3 to +23.5) clear; round 5 35.0%.
- One row per smoke is in `new-n1/enemy-took.csv` (timeline values and the round 5 snapshot values side by side).

**Numbers: `cap_defended` follow-up, was the defended cap still ours afterwards?**

Kept = the enemy did not take the defended cap from the first moment it was ours and invaded until 60 s after the smoke cleared. The timeline shows that moment inside the smoke for 485 of 486 smokes.

| group | n | kept through 60 s after (interval) | Top 6 | Rest | Top 6 - Rest | kept while the smoke stood | round 5 (snapshot, 60 s) |
|---|---|---|---|---|---|---|---|
| all smokes with cap_defended | 486 | 52.5% (46.1 to 58.3) | 53.4% (n 163) | 52.0% (n 323) | +1.4 (-13.2 to +13.7) | 68.7% | 60.5% |
| destroyer smokes | 360 | 50.6% (43.9 to 56.4) | 51.6% (n 124) | 50.0% (n 236) | +1.6 (-14.2 to +14.5) | 66.9% | 58.9% |
| defended cap = nearest cap | 175 | 53.7% (46.6 to 60.4) | 52.4% (n 63) | 54.5% (n 112) | -2.1 (-19.1 to +15.6) | 74.3% | 61.1% |
| defended cap not the nearest | 311 | 51.8% (44.7 to 58.4) | 54.0% (n 100) | 50.7% (n 211) | +3.3 (-13.2 to +17.9) | 65.6% | 60.1% |

- No grace: 334 of 486 kept (68.7%; round 5 374, 77.0%). 60 s: 255 (52.5%; round 5 294, 60.5%). 120 s: 227 (46.7%; round 5 252, 51.9%). Sixty seconds after the smoke cleared the defended cap was ours in 264 and the enemy's in 222.
- For comparison, any smoke whose nearest cap was ours at activation kept it through 60 s after in 81.8% (n 694); round 5 said 86.3%.

**Numbers (new): was the enemy inside our cap while the smoke stood?** (the timeline records the invading team)

| smokes | n | enemy was invading the cap during the smoke (interval) | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| within 2 km of a cap we own | 349 | 27.2% (19.9 to 33.8) | 29.3% (n 116) | 26.2% (n 233) | +3.1 (-10.9 to +16.5) |
| destroyer smokes within 2 km of a cap we own | 255 | 31.0% (22.8 to 39.7) | 29.5% (n 88) | 31.7% (n 167) | -2.2 (-22.6 to +13.6) |
| any smoke whose nearest cap is ours (reference) | 694 | 33.7% (28.5 to 38.9) | 34.1% (n 261) | 33.5% (n 433) | +0.6 (-10.8 to +11.4) |

| smokes | n | cap kept while the smoke stood (interval) | Top 6 | Rest | Top 6 - Rest | kept through 60 s after | Top 6 - Rest (60 s) |
|---|---|---|---|---|---|---|---|
| invaded, within 2 km | 95 | 78.9% (66.2 to 88.6) | 88.2% (n 34) | 73.8% (n 61) | +14.5 (-1.9 to +37.3) | 58.9% | +4.4 (-18.2 to +33.3) |
| invaded, destroyer smokes within 2 km | 79 | 77.2% (65.0 to 87.5) | 88.5% (n 26) | 71.7% (n 53) | +16.8 (-1.3 to +42.6) | 58.2% | +4.9 (-19.7 to +39.6) |
| not invaded, within 2 km | 254 | 100.0% (100.0 to 100.0) | 100.0% (n 82) | 100.0% (n 172) | +0.0 (+0.0 to +0.0) | 98.4% | +2.3 (+0.0 to +6.0) |

- When the enemy stood in a cap we owned and a smoke was within 2 km, the cap was still ours when the smoke cleared in 78.9% and 60 s later in 58.9% (n 95). The enemy stood in it for a median of 40 s. A cap that was not invaded was never lost while the smoke stood, as it must be.

**Numbers: ribbons per smoke**

- How thin this is: a replay holds only its own recording player's ribbons. That is one ship per team per game: 341 ships of 3,078. The batch has 442 cap ribbons: Defended 284, Captured 91, AssistedInCapture 67. Each row is one ribbon (the count column is always 1).
- Smokes that covered the smoking team's recording player: 268 of 1,547 (17.3%): smoker 129, inside 59, line of fire 49, behind 31. The recording player was the smoker or inside in 188 (12.2%). So 1,279 smokes (83%) cannot have a ribbon in this data whatever happened.
- Strict count (ribbon by a ship the smoke covered, during the smoke). A Defended ribbon repeats while defending, so events and distinct smokes are both given:

| smokes | n | with any cap ribbon | Defended | Captured | Assisted in capture |
|---|---|---|---|---|---|
| recording player covered by the smoke | 268 | 47 (17.5%) | 68 in 24 smokes (25.4 per 100) | 13 in 13 smokes (4.9 per 100) | 11 in 11 smokes (4.1 per 100) |
| Top 6 | 110 | 23 (20.9%) | 19 in 6 smokes (17.3 per 100) | 11 in 11 smokes (10.0 per 100) | 7 in 7 smokes (6.4 per 100) |
| Rest | 158 | 24 (15.2%) | 49 in 18 smokes (31.0 per 100) | 2 in 2 smokes (1.3 per 100) | 4 in 4 smokes (2.5 per 100) |
| recording player the smoker or inside | 188 | 36 (19.1%) | 44 in 15 smokes (23.4 per 100) | 13 in 13 smokes (6.9 per 100) | 9 in 9 smokes (4.8 per 100) |
| destroyer smokes, recording player covered | 208 | 35 (16.8%) | 54 in 16 smokes (26.0 per 100) | 12 in 12 smokes (5.8 per 100) | 8 in 8 smokes (3.8 per 100) |

- Looser count (ribbon by a ship of the smoking team during the smoke while that ship was within 2 km of the smoke; the recording player was that close in 254 smokes). It is not a superset of the strict count: ships behind a smoke or firing through it are often further than 2 km away.

| smokes | n | with any cap ribbon | Defended | Captured | Assisted in capture |
|---|---|---|---|---|---|
| recording player within 2 km while the smoke stood | 254 | 26 (10.2%) | 38 in 15 smokes (15.0 per 100) | 5 in 5 smokes (2.0 per 100) | 6 in 6 smokes (2.4 per 100) |
| Top 6 | 115 | 10 (8.7%) | 9 in 3 smokes (7.8 per 100) | 4 in 4 smokes (3.5 per 100) | 3 in 3 smokes (2.6 per 100) |
| Rest | 139 | 16 (11.5%) | 29 in 12 smokes (20.9 per 100) | 1 in 1 smokes (0.7 per 100) | 3 in 3 smokes (2.2 per 100) |

- Top 6 vs Rest, share of smokes with a ribbon:

| measure | n | share (interval) | Top 6 | Rest | Top 6 - Rest |
|---|---|---|---|---|---|
| strict: any cap ribbon | 268 | 17.5% (12.4 to 23.0) | 20.9% (n 110) | 15.2% (n 158) | +5.7 (-6.0 to +16.7) |
| strict: a Defended ribbon | 268 | 9.0% (6.0 to 12.0) | 5.5% (n 110) | 11.4% (n 158) | -5.9 (-11.6 to -0.7) clear |
| strict: a Captured or Assisted ribbon | 268 | 9.0% (3.7 to 14.7) | 16.4% (n 110) | 3.8% (n 158) | +12.6 (+3.1 to +23.6) clear |
| loose: any cap ribbon | 254 | 10.2% (6.5 to 14.5) | 8.7% (n 115) | 11.5% (n 139) | -2.8 (-10.7 to +5.5) |
| loose: a Defended ribbon | 254 | 5.9% (2.9 to 9.4) | 2.6% (n 115) | 8.6% (n 139) | -6.0 (-11.1 to -1.2) clear |

- Do smokes with a Defended ribbon keep the cap more often? (nearest cap ours at activation; the ribbon does not say which cap it was for)

| smokes | Defended ribbon: kept while the smoke stood | no Defended ribbon | Defended ribbon: kept through 60 s after | no Defended ribbon | gap at 60 s (interval) |
|---|---|---|---|---|---|
| strict, recording player covered | 11 of 11 (100%) (small n) | 78 of 96 (81%) | 7 of 11 (64%) (small n) | 74 of 96 (77%) | -13 (-50 to +14) |
| strict, and smoke within 2 km of the cap | too few (n 4) | 43 of 46 (93%) | too few (n 4) | 39 of 46 (85%) | - |
| loose, recording player within 2 km of the smoke | too few (n 6) | 84 of 99 (85%) | too few (n 6) | 79 of 99 (80%) | - |
| loose, and smoke within 2 km of the cap | too few (n 3) | 44 of 46 (96%) | too few (n 3) | 40 of 46 (87%) | - |
| loose, smoke within 2 km, enemy was invading the cap | too few (n 2) | 8 of 10 (80%) (small n) | too few (n 2) | 6 of 10 (60%) (small n) | - |

  Only the first row has enough smokes: 11 smokes with a Defended ribbon, all 11 kept the cap while the smoke stood, and 7 still had it 60 s later, against 77% without a ribbon. The interval is wide and includes zero. The data cannot say that Defended ribbons go with keeping the cap.
- What the ribbons are good for: they confirm the timeline. 91 of 91 Captured ribbons fall within 3 s of a cap changing to that team; all 284 of 284 Defended ribbons fall while the enemy stood in a cap (203 in a cap the team owned; the others in a neutral cap). Of 13 smokes with a strict Captured ribbon, the timeline says "we took the nearest cap during the smoke" in 12; in the other 1 the ribbon was for a different cap.

**Top 6 or Shared:** Shared. Enemy took the nearest cap (60 s): Top 6 19.9% vs Rest 22.8%, gap -3.0 (-7.1 to +1.2). Destroyer smokes: -3.5 (-9.5 to +2.8). Within 2 km: -2.8 (-8.9 to +3.9). The one gap that stays clear is for caps that were neutral at activation: Top 6 22.5% vs Rest 31.5%, -9.0 (-18.3 to -0.2) clear; strictly during the smoke -9.6 (-17.4 to -0.4) clear. Ribbons: Rest smokes carry a Defended ribbon more often and Top 6 smokes a Captured or Assisted ribbon more often (table above), on 110 and 158 smokes; treat as a hint.

**Clans:** not a spot item. The clan of every smoke is in `enemy-took.csv`.

**Could not be done / proxy:** Ribbons per smoke for all smokes: the replays hold them for one ship per team only. "Enemy took the cap" from the timeline is the measure to use; ribbons only confirm it. A Defended ribbon does not name its cap. The nearest cap can be far from the smoke; the "within 2 km" rows are the meaningful ones.

**Verdict:** Keep (the timeline version replaces the snapshot version). Drop the round 5 statement that Rest lose the cap clearly more often around destroyer smokes and smokes within 2 km. Ribbons: Drop as a per-smoke measure.

**Changed from round 5:**

| number | round 5 | round 5b | difference |
|---|---|---|---|
| enemy took, 60 s grace: yes | 184 | 233 | +49 |
| enemy took, 60 s grace: share | 17.1% | 21.7% | +4.6 |
| enemy took, no grace: yes | 103 | 155 | +52 |
| enemy took, no grace: share | 9.6% | 14.4% | +4.8 |
| enemy took, 120 s grace: yes | 233 | 293 | +60 |
| enemy took, 120 s grace: share | 21.7% | 27.3% | +5.6 |
| coverage: yes / no / not applicable | 184 / 889 / 474 | 233 / 841 / 473 |  |
| share of real flips the snapshot version misses | about 15% (estimate) | 20.7% enemy, 22.9% ours (measured) |  |
| all applicable smokes: share | 17.1% (n 1073) | 21.7% (n 1074) | +4.6 |
| all applicable smokes: Top 6 - Rest | -4.4 (-8.9 to +0.1) | -3.0 (-7.1 to +1.2) | +1.4 |
| destroyer smokes: share | 18.8% (n 762) | 23.1% (n 763) | +4.3 |
| destroyer smokes: Top 6 - Rest | -5.9 (-12.1 to -0.9) clear | -3.5 (-9.5 to +2.8) | +2.4 |
| smoke centre inside or within 2 km of the cap: share | 11.1% (n 541) | 16.1% (n 541) | +5.0 |
| smoke centre inside or within 2 km of the cap: Top 6 - Rest | -4.8 (-9.2 to -0.7) clear | -2.8 (-8.9 to +3.9) | +2.0 |
| destroyer smokes inside or within 2 km: share | 12.8% (n 405) | 17.5% (n 405) | +4.7 |
| destroyer smokes inside or within 2 km: Top 6 - Rest | -6.8 (-12.6 to -1.7) clear | -3.1 (-11.0 to +4.5) | +3.7 |
| cap ours at activation: share | 13.7% (n 694) | 18.2% (n 694) | +4.5 |
| cap ours at activation: Top 6 - Rest | -1.6 (-8.2 to +5.0) | +0.4 (-5.8 to +5.8) | +2.0 |
| cap neutral at activation: share | 23.5% (n 379) | 28.2% (n 380) | +4.7 |
| cap neutral at activation: Top 6 - Rest | -9.4 (-18.4 to -0.5) clear | -9.0 (-18.3 to -0.2) clear | +0.4 |
| cap ours, smoke within 2 km: share | 8.0% (n 350) | 12.3% (n 349) | +4.3 |
| cap ours, smoke within 2 km: Top 6 - Rest | -4.2 (-9.7 to +1.5) | -1.7 (-11.1 to +6.8) | +2.5 |
| cap ours, cap_defended set for that cap: share | 35.9% (n 153) | 45.8% (n 153) | +9.9 |
| cap ours, cap_defended set for that cap: Top 6 - Rest | -7.8 (-24.7 to +10.5) | +3.5 (-13.1 to +20.0) | +11.3 |
| cap ours, cap_defended not set for it: share | 7.4% (n 541) | 10.4% (n 541) | +3.0 |
| cap ours, cap_defended not set for it: Top 6 - Rest | +1.3 (-3.4 to +5.2) | +1.1 (-3.7 to +5.3) | -0.2 |
| cap_defended kept, all smokes with cap_defended | 60.5%; gap +3.1 (-10.7 to +15.3) | 52.5%; gap +1.4 (-13.2 to +13.7) | -8.0 |
| cap_defended kept, destroyer smokes | 58.9%; gap +1.2 (-15.0 to +13.3) | 50.6%; gap +1.6 (-14.2 to +14.5) | -8.3 |
| cap_defended kept, defended cap = nearest cap | 61.1%; gap +8.6 (-6.2 to +21.9) | 53.7%; gap -2.1 (-19.1 to +15.6) | -7.4 |
| cap_defended kept, defended cap not the nearest | 60.1%; gap -0.2 (-16.7 to +14.0) | 51.8%; gap +3.3 (-13.2 to +17.9) | -8.3 |
| cap_defended kept, no grace / 120 s | 77.0% / 51.9% | 68.7% / 46.7% | -8.3 / -5.2 |
| nearest cap ours at activation: kept | 86.3% (n 694) | 81.8% (n 694) | -4.5 |
| we took, all smokes where the nearest cap was not ours | 24.5%; gap +5.8 (-1.7 to +14.4) | 31.9%; gap +10.5 (-0.2 to +22.1) | +7.4 |
| we took, destroyer smokes | 27.0%; gap +8.9 (-1.6 to +20.2) | 35.6%; gap +15.3 (+2.1 to +28.1) clear | +8.6 |
| we took, within 2 km | 35.0%; gap +6.2 (-3.5 to +18.5) | 42.3%; gap +12.1 (+1.3 to +23.5) clear | +7.3 |
| Hotspot A: enemy took | 0.0% | 9.1% (n 11) | +9.1 |
| Hotspot B: enemy took | 9.1% | 11.4% (n 44) | +2.3 |
| Hotspot C: enemy took | 26.2% | 32.3% (n 65) | +6.1 |
| Hotspot D: enemy took | 23.8% | 25.0% (n 84) | +1.2 |
| Land of Fire A: enemy took | 20.8% | 22.6% (n 53) | +1.8 |
| Land of Fire B: enemy took | 11.8% | 14.7% (n 68) | +2.9 |
| Land of Fire D: enemy took | 7.7% | 11.5% (n 26) | +3.8 |
| Loop A: enemy took | 17.0% | 21.3% (n 47) | +4.3 |
| Loop B: enemy took | 20.0% | 30.0% (n 30) | +10.0 |
| Loop C: enemy took | 12.1% | 15.2% (n 33) | +3.1 |
| Mountain Range A: enemy took | 14.6% | 24.4% (n 41) | +9.8 |
| Mountain Range B: enemy took | 35.6% | 39.1% (n 46) | +3.5 |
| Mountain Range C: enemy took | 17.9% | 21.4% (n 56) | +3.5 |
| Okinawa A: enemy took | 15.4% | 23.1% (n 39) | +7.7 |
| Okinawa C: enemy took | 13.5% | 18.9% (n 37) | +5.4 |
| Okinawa D: enemy took | 19.2% | 30.8% (n 26) | +11.6 |
| Sea of Fortune A: enemy took | 8.3% | 16.7% (n 12) | +8.4 |
| Sea of Fortune B: enemy took | 10.0% | 13.3% (n 60) | +3.3 |
| Sea of Fortune C: enemy took | 6.7% | 40.0% (n 15) | +33.3 |
| Sleeping Giant A: enemy took | 21.1% | 26.7% (n 90) | +5.6 |
| Sleeping Giant B: enemy took | 8.7% | 10.9% (n 46) | +2.2 |
| Sleeping Giant D: enemy took | 17.3% | 20.0% (n 75) | +2.7 |
| ribbons | not in the batch | 442 ribbons, 268 smokes with a recording player covered | new |

Why: better data. The timeline has every owner change; round 5 only saw cap owners at the moments other smokes were laid or fully laid. Same definition, same nearest cap, same 60 s grace. Every share went up because flips after the last snapshot are now seen. The `cap_defended` follow-up also changed its start point slightly (from the first invaded moment instead of from activation; this gives the same count). Unchanged: the meaning of `cap_defended`, its rates (31.4% of smokes) and the distance facts, which use smoke fields only.

### C2. Cap holder at exactly 8:00 and winning

**Answer:** Same answer as round 5, now on all 166 games that were still running at 8:00 instead of 154. No single cap clearly adds something beyond team strength in a way that holds up. Teams holding more caps than the enemy at exactly 8:00 won 63% (the others 37%), but only +6 points more than their strength predicts, and in Rest-vs-Rest games the edge is gone (54%, -1 points). The two middle caps on Land of Fire are still the only caps that stay above expectation. New from the timeline: 74% of the teams with more caps were already ahead on score, and cap leaders who were not ahead on score won only 5 of 25.

**Numbers**

- Coverage: cap owners read from the timeline at exactly elapsed 480 s. 166 of 171 games are in the tables; 5 ended before 8:00 and are kept apart. Round 5 had 154 (5 ended early, 12 had no snapshot within 60 s). In the tables / all: Hotspot 31/31, Land of Fire 24/25, Loop 21/23, Mountain Range 20/21, Okinawa 17/18, Sea of Fortune 21/21, Sleeping Giant 32/32. Rest-vs-Rest games: 84 (round 5: 76).
- Against round 5, game by game: of the 154 games round 5 covered, the owners at 8:00 are identical in 141 and differ in 13 (the snapshot was up to 60 s away from 8:00). 2 games (kots19na_7971 g1, kots19na_7976 g1) ran on a 15-minute clock; round 5 worked out elapsed time as 20:00 minus the clock, so its "8:00" in those games was really 3:00. The timeline uses true elapsed seconds.
- Cap roles (own side, enemy side, middle), the expected win rate and the Bradley-Terry check are exactly as in round 5 (favourite won 110 of 158 on the simple model, 128 of 164 on Bradley-Terry).

All maps pooled, all 166 games (last column: round 5 on 154 games):

| what the team holds at 8:00 | team-games | holders won (interval) | others won | strength predicts | actual - expected (interval) | Bradley-Terry check | round 5 |
|---|---|---|---|---|---|---|---|
| its own-side cap | 199 | 101, 51% (47 to 54) | 49% | 100.1 | +0 (-3 to +4) | -0 (-3 to +2) | n 184, won 94 (51%), +1 (-3 to +4) |
| the enemy-side cap | 50 | 26, 52% (38 to 65) | 50% | 25.2 | +2 (-11 to +14) | -0 (-12 to +10) | n 47, won 25 (53%), +2 (-10 to +15) |
| at least one middle cap | 247 | 136, 55% (52 to 59) | 35% | 127.6 | +3 (+0 to +7) clear | +2 (-0 to +4) | n 231, won 131 (57%), +5 (+1 to +8) clear |
| every middle cap | 49 | 31, 63% (49 to 75) | 48% | 28.2 | +6 (-5 to +16) | +3 (-7 to +12) | n 43, won 27 (63%), +6 (-5 to +18) |
| more caps than the enemy (reference) | 97 | 61, 63% (54 to 72) | 37% | 54.7 | +6 (-2 to +14) | +2 (-5 to +9) | n 91, won 60 (66%), +8 (-0 to +17) |
| 2+ more caps than the enemy | 45 | 33, 73% (60 to 87) | 46% | 27.0 | +13 (+3 to +24) clear | +7 (-1 to +15) | n 42, won 31 (74%), +15 (+4 to +26) clear |

(a) Rest-vs-Rest games only (84):

| what the team holds at 8:00 | team-games | holders won (interval) | others won | strength predicts | actual - expected (interval) | Bradley-Terry check | round 5 |
|---|---|---|---|---|---|---|---|
| its own-side cap | 100 | 52, 52% (48 to 57) | 47% | 50.1 | +2 (-3 to +7) | +1 (-3 to +5) | n 88, won 46 (52%), +2 (-3 to +7) |
| the enemy-side cap | 26 | 15, 58% (38 to 77) | 49% | 13.1 | +7 (-12 to +26) | +4 (-12 to +20) | n 26, won 15 (58%), +8 (-9 to +26) |
| at least one middle cap | 131 | 69, 53% (48 to 58) | 40% | 67.6 | +1 (-3 to +5) | +0 (-3 to +3) | n 119, won 64 (54%), +2 (-2 to +6) |
| every middle cap | 25 | 16, 64% (46 to 83) | 48% | 15.0 | +4 (-12 to +18) | +2 (-12 to +14) | n 22, won 14 (64%), +5 (-12 to +23) |
| more caps than the enemy (reference) | 44 | 24, 54% (38 to 69) | 46% | 24.3 | -1 (-15 to +13) | -5 (-18 to +8) | n 41, won 23 (56%), +1 (-12 to +15) |
| 2+ more caps than the enemy | 21 | 17, 81% (62 to 96) | 46% | 12.8 | +20 (+5 to +33) clear | +14 (+2 to +24) clear | n 20, won 16 (80%), +22 (+7 to +36) clear |

Per map, caps whose holders did clearly better than strength predicts, now or in round 5 (every other cap on every map has an interval including zero; all rows are in `out-c2.md`):

| map, cap | holder team-games | holders won | others won | strength predicts | actual - expected | Bradley-Terry check | Rest-vs-Rest only | round 5 |
|---|---|---|---|---|---|---|---|---|
| Hotspot C (middle) | 29 | 21, 72% (55 to 87) | 30% | 16.2 | +16 (+0 to +32) clear | +10 (-4 to +23) | 11 of 16, +10 (-14 to +31) | n 28, won 20 (71%), +16 (+1 to +30) clear |
| Hotspot B (own side), Rest-vs-Rest games | 31 | 18, 58% (51 to 67) | 0% (n 5) | 15.7 | +7 (+2 to +16) clear | +6 (+1 to +12) clear | this row | n 27, won 16 (59%), +8 (+2 to +18) clear |
| Land of Fire A (middle) | 21 | 16, 76% (56 to 92) | 30% | 12.3 | +18 (+1 to +34) clear | +13 (-2 to +27) | 8 of 12 (small n), +10 (-12 to +31) | n 18, won 14 (78%), +20 (+2 to +38) clear |
| Land of Fire B (middle) | 21 | 17, 81% (62 to 96) | 26% | 12.9 | +20 (+6 to +34) clear | +14 (+2 to +25) clear | 8 of 11 (small n), +17 (-7 to +40) | n 20, won 16 (80%), +19 (+3 to +33) clear |
| Loop C (middle), Rest-vs-Rest games | 10 (small n) | 2, 20% (0 to 50) | 71% (n 14) | 5.1 | -31 (-57 to +1) | -32 (-59 to +1) | this row | n 9, won 1 (11%), -40 (-57 to -15) clear |

- Multiplicity: 25 map-and-cap rows tested; fewer than one clear positive row is expected by luck. 3 came out clear on the simple model, 1 on both models (Land of Fire B). None of the middle caps is clear in Rest-vs-Rest games (small n everywhere). Land of Fire A and B share the same games.
- "More caps than the enemy" per map (all games): Hotspot 10 of 12 (small n), +25 (+2 to +42) clear [round 5: n 12, won 10 (83%), +27 (+6 to +45) clear]; Land of Fire 13 of 15, +25 (+5 to +40) clear [round 5: n 14, won 12 (86%), +24 (+1 to +42) clear]; Loop 8 of 15, -6 (-30 to +19) [round 5: n 13, won 6 (46%), -12 (-37 to +13)]; Mountain Range 10 of 14 (small n), +12 (-8 to +30) [round 5: n 12, won 9 (75%), +15 (-6 to +35)]; Okinawa too few (n 7) [round 5: n 8, won 3 (38%), -11 (-38 to +17)]; Sea of Fortune 7 of 15, -2 (-22 to +18) [round 5: n 15, won 8 (53%), -0 (-24 to +20)]; Sleeping Giant 11 of 19, +3 (-16 to +22) [round 5: n 17, won 12 (71%), +11 (-10 to +30)].
- Loop, Rest-vs-Rest: teams holding cap C won 2 of 10 (small n) (-31 (-57 to +1)); round 5 had 1 of 9 and called it clear. It is no longer clear.

New reference rows from the timeline (all games; the same teams, other moments):

| what | team-games | they won (interval) | the other side won | strength predicts | actual - expected (interval) | Bradley-Terry check | Rest-vs-Rest only |
|---|---|---|---|---|---|---|---|
| more caps than the enemy at 5:00 | 107 | 70, 65% (56 to 74) | 35% | 61.7 | +8 (-0 to +15) | +6 (-2 to +12) | 29 of 51, +2 (-11 to +14) |
| more caps than the enemy at 8:00 | 97 | 61, 63% (54 to 72) | 37% | 54.7 | +6 (-2 to +14) | +2 (-5 to +9) | 24 of 44, -1 (-14 to +13) |
| more caps than the enemy at 10:00 (games still running then) | 102 | 62, 61% (52 to 70) | 39% | 55.0 | +7 (-2 to +15) | +4 (-4 to +11) | 31 of 51, +8 (-6 to +20) |
| held more caps for longer than the enemy over the first 8 minutes | 166 | 110, 66% (59 to 74) | 34% | 93.3 | +10 (+3 to +17) clear | +7 (+2 to +13) clear | 50 of 84, +5 (-4 to +15) |
| held more caps for at least half of the first 8 minutes | 39 | 28, 72% (57 to 86) | 28% | 24.3 | +9 (-2 to +21) | +6 (-5 to +18) | 12 of 18, +5 (-14 to +20) |

- Time-weighted: winners held more caps than the enemy for 26% of the first 8 minutes on average, losers for 14%; the two sides were level on caps 60% of the time. The side that led on caps for longer won 66% and beat its strength by +10 (+3 to +17) clear; in Rest-vs-Rest games +5 (-4 to +15). 153 of 166 games were still running at 10:00.
- Holding a cap at 8:00 is partly a result of already winning. Teams with more caps at 8:00 were already ahead on score in 72 of 97 (74%; median lead +105 points). Cap leaders who were also ahead on score won 56 of 72; cap leaders level or behind on score won 5 of 25. The team ahead on score at 8:00 won 131 of 165 (79%). 69 of 166 games were level on caps. In the 57 Top 6 vs Rest games the Top 6 clan held more caps in 30, fewer in 10, and won 50.
- Separate row, not in any table above: the 5 games that ended before 8:00, state at the end. The team with more caps at the end won 5 of 5. These are routs; they say nothing about caps.
- Check: the number of games with a cap leader at 8:00 counted a second way, straight from the timeline rows: 97 (table: 97).

**Top 6 or Shared:** Shared. In Rest-vs-Rest games holding more caps is worth -1 (-15 to +13) points over expected. Only a 2+ cap lead stays clear there (+20 (+5 to +33) clear, n 21; Bradley-Terry +14 (+2 to +24) clear).

**Clans:** not a spot item.

**Could not be done / proxy:** Nothing is missing any more: every game has its cap owners at the exact second. The data still cannot separate "holding the cap helped" from "the winning team held the cap"; the score at 8:00 shows most cap leaders were already ahead.

**Verdict:** Keep (as a caution). Land of Fire middle caps A and B: Lead for the Land of Fire page, with the small-n warning (B: +20 (+6 to +34) clear, Bradley-Terry +14 (+2 to +25) clear; A: +18 (+1 to +34) clear).

**Changed from round 5:**

| number | round 5 (154 games, snapshot within 60 s) | round 5b (exact 8:00, timeline) | difference |
|---|---|---|---|
| games in the tables | 154 | 166 | +12 |
| Rest-vs-Rest games | 76 | 84 | +8 |
| games level on caps at 8:00 | 63 of 154 | 69 of 166 |  |
| cap leaders already ahead on score | 66 of 91 (73%), median +95 | 72 of 97 (74%), median +105 |  |
| score leader at 8:00 won | 120 of 153 (78%) | 131 of 165 (79%) |  |
| Top 6 vs Rest games: Top 6 more / fewer caps / won | 53 games: 30 / 7 / 46 | 57 games: 30 / 10 / 50 |  |
| pooled, all games: its own-side cap | n 184, won 94 (51%), +1 (-3 to +4) | n 199, won 101 (51%), +0 (-3 to +4) | n +15, wins +7, -0 pts |
| pooled, all games: the enemy-side cap | n 47, won 25 (53%), +2 (-10 to +15) | n 50, won 26 (52%), +2 (-11 to +14) | n +3, wins +1, -0 pts |
| pooled, all games: at least one middle cap | n 231, won 131 (57%), +5 (+1 to +8) clear | n 247, won 136 (55%), +3 (+0 to +7) clear | n +16, wins +5, -1 pts |
| pooled, all games: every middle cap | n 43, won 27 (63%), +6 (-5 to +18) | n 49, won 31 (63%), +6 (-5 to +16) | n +6, wins +4, -1 pts |
| pooled, all games: more caps than the enemy (reference) | n 91, won 60 (66%), +8 (-0 to +17) | n 97, won 61 (63%), +6 (-2 to +14) | n +6, wins +1, -2 pts |
| pooled, all games: 2+ more caps than the enemy | n 42, won 31 (74%), +15 (+4 to +26) clear | n 45, won 33 (73%), +13 (+3 to +24) clear | n +3, wins +2, -2 pts |
| pooled, Rest-vs-Rest: its own-side cap | n 88, won 46 (52%), +2 (-3 to +7) | n 100, won 52 (52%), +2 (-3 to +7) | n +12, wins +6, -0 pts |
| pooled, Rest-vs-Rest: the enemy-side cap | n 26, won 15 (58%), +8 (-9 to +26) | n 26, won 15 (58%), +7 (-12 to +26) | n +0, wins +0, -1 pts |
| pooled, Rest-vs-Rest: at least one middle cap | n 119, won 64 (54%), +2 (-2 to +6) | n 131, won 69 (53%), +1 (-3 to +5) | n +12, wins +5, -1 pts |
| pooled, Rest-vs-Rest: every middle cap | n 22, won 14 (64%), +5 (-12 to +23) | n 25, won 16 (64%), +4 (-12 to +18) | n +3, wins +2, -1 pts |
| pooled, Rest-vs-Rest: more caps than the enemy (reference) | n 41, won 23 (56%), +1 (-12 to +15) | n 44, won 24 (54%), -1 (-15 to +13) | n +3, wins +1, -2 pts |
| pooled, Rest-vs-Rest: 2+ more caps than the enemy | n 20, won 16 (80%), +22 (+7 to +36) clear | n 21, won 17 (81%), +20 (+5 to +33) clear | n +1, wins +1, -2 pts |
| Hotspot, all games: A (enemy side) | n 9, won 6 (67%), +12 (-21 to +42) | n 9, won 6 (67%), +12 (-20 to +42) | n +0, wins +0, +0 pts |
| Hotspot, all games: B (own side) | n 49, won 26 (53%), +2 (-3 to +8) | n 53, won 28 (53%), +2 (-3 to +7) | n +4, wins +2, -0 pts |
| Hotspot, all games: C (middle) | n 28, won 20 (71%), +16 (+1 to +30) clear | n 29, won 21 (72%), +16 (+0 to +32) clear | n +1, wins +1, +0 pts |
| Hotspot, all games: D (middle) | n 29, won 16 (55%), +4 (-13 to +20) | n 30, won 16 (53%), +1 (-14 to +17) | n +1, wins +0, -3 pts |
| Hotspot, all games: more caps than the enemy (reference) | n 12, won 10 (83%), +27 (+6 to +45) clear | n 12, won 10 (83%), +25 (+2 to +42) clear | n +0, wins +0, -2 pts |
| Hotspot, Rest-vs-Rest: B (own side) | n 27, won 16 (59%), +8 (+2 to +18) clear | n 31, won 18 (58%), +7 (+2 to +16) clear | n +4, wins +2, -1 pts |
| Hotspot, Rest-vs-Rest: C (middle) | n 15, won 10 (67%), +10 (-15 to +32) | n 16, won 11 (69%), +10 (-14 to +31) | n +1, wins +1, +1 pts |
| Hotspot, Rest-vs-Rest: D (middle) | n 16, won 9 (56%), +2 (-21 to +23) | n 17, won 9 (53%), -2 (-24 to +20) | n +1, wins +0, -4 pts |
| Hotspot, Rest-vs-Rest: more caps than the enemy (reference) | n 10, won 8 (80%), +25 (-3 to +47) | n 10, won 8 (80%), +22 (-2 to +45) | n +0, wins +0, -3 pts |
| Land of Fire, all games: A (middle) | n 18, won 14 (78%), +20 (+2 to +38) clear | n 21, won 16 (76%), +18 (+1 to +34) clear | n +3, wins +2, -2 pts |
| Land of Fire, all games: B (middle) | n 20, won 16 (80%), +19 (+3 to +33) clear | n 21, won 17 (81%), +20 (+6 to +34) clear | n +1, wins +1, +1 pts |
| Land of Fire, all games: C (enemy side) | n 12, won 5 (42%), -5 (-31 to +22) | n 12, won 5 (42%), -5 (-29 to +21) | n +0, wins +0, +0 pts |
| Land of Fire, all games: D (own side) | n 34, won 16 (47%), -2 (-11 to +8) | n 36, won 17 (47%), -2 (-10 to +7) | n +2, wins +1, +0 pts |
| Land of Fire, all games: more caps than the enemy (reference) | n 14, won 12 (86%), +24 (+1 to +42) clear | n 15, won 13 (87%), +25 (+5 to +40) clear | n +1, wins +1, +1 pts |
| Land of Fire, Rest-vs-Rest: A (middle) | n 10, won 7 (70%), +11 (-18 to +35) | n 12, won 8 (67%), +10 (-12 to +31) | n +2, wins +1, -1 pts |
| Land of Fire, Rest-vs-Rest: B (middle) | n 10, won 7 (70%), +15 (-13 to +39) | n 11, won 8 (73%), +17 (-7 to +40) | n +1, wins +1, +2 pts |
| Land of Fire, Rest-vs-Rest: C (enemy side) | n 8, won 4 (50%), +5 (-26 to +33) | n 8, won 4 (50%), +5 (-24 to +34) | n +0, wins +0, +0 pts |
| Land of Fire, Rest-vs-Rest: D (own side) | n 14, won 7 (50%), +3 (-13 to +23) | n 16, won 8 (50%), +2 (-12 to +19) | n +2, wins +1, -0 pts |
| Land of Fire, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 5) | too few (n 6) |  |
| Loop, all games: A (middle) | n 16, won 6 (38%), -10 (-30 to +14) | n 19, won 8 (42%), -7 (-28 to +14) | n +3, wins +2, +2 pts |
| Loop, all games: B (middle) | n 18, won 11 (61%), +8 (-12 to +28) | n 21, won 13 (62%), +9 (-10 to +29) | n +3, wins +2, +1 pts |
| Loop, all games: C (middle) | n 14, won 6 (43%), -16 (-38 to +8) | n 15, won 7 (47%), -12 (-36 to +14) | n +1, wins +1, +4 pts |
| Loop, all games: more caps than the enemy (reference) | n 13, won 6 (46%), -12 (-37 to +13) | n 15, won 8 (53%), -6 (-30 to +19) | n +2, wins +2, +7 pts |
| Loop, Rest-vs-Rest: A (middle) | n 9, won 4 (44%), -3 (-38 to +33) | n 11, won 5 (46%), -4 (-35 to +28) | n +2, wins +1, -1 pts |
| Loop, Rest-vs-Rest: B (middle) | n 10, won 6 (60%), +9 (-22 to +40) | n 12, won 7 (58%), +9 (-25 to +39) | n +2, wins +1, -0 pts |
| Loop, Rest-vs-Rest: C (middle) | n 9, won 1 (11%), -40 (-57 to -15) clear | n 10, won 2 (20%), -31 (-57 to +1) | n +1, wins +1, +9 pts |
| Loop, Rest-vs-Rest: more caps than the enemy (reference) | n 8, won 2 (25%), -26 (-56 to +13) | n 9, won 3 (33%), -18 (-54 to +19) | n +1, wins +1, +8 pts |
| Mountain Range, all games: A (middle) | n 12, won 6 (50%), -2 (-29 to +21) | n 14, won 9 (64%), +8 (-12 to +29) | n +2, wins +3, +9 pts |
| Mountain Range, all games: B (middle) | n 17, won 11 (65%), +11 (-9 to +30) | n 18, won 12 (67%), +11 (-8 to +30) | n +1, wins +1, +0 pts |
| Mountain Range, all games: C (middle) | n 19, won 10 (53%), +1 (-19 to +20) | n 20, won 9 (45%), -5 (-23 to +14) | n +1, wins -1, -6 pts |
| Mountain Range, all games: more caps than the enemy (reference) | n 12, won 9 (75%), +15 (-6 to +35) | n 14, won 10 (71%), +12 (-8 to +30) | n +2, wins +1, -3 pts |
| Mountain Range, Rest-vs-Rest: A (middle) | too few (n 5) | too few (n 6) |  |
| Mountain Range, Rest-vs-Rest: B (middle) | too few (n 7) | n 8, won 6 (75%), +8 (-19 to +34) |  |
| Mountain Range, Rest-vs-Rest: C (middle) | n 8, won 4 (50%), +9 (-21 to +37) | n 9, won 3 (33%), -5 (-31 to +21) | n +1, wins -1, -14 pts |
| Mountain Range, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 5) |  |
| Okinawa, all games: A (own side) | n 22, won 12 (54%), +2 (-11 to +16) | n 23, won 12 (52%), -0 (-13 to +12) | n +1, wins +0, -3 pts |
| Okinawa, all games: B (enemy side) | n 9, won 5 (56%), +5 (-26 to +39) | n 10, won 5 (50%), -2 (-30 to +27) | n +1, wins +0, -6 pts |
| Okinawa, all games: C (middle) | n 15, won 6 (40%), -3 (-26 to +20) | n 16, won 7 (44%), -0 (-24 to +22) | n +1, wins +1, +3 pts |
| Okinawa, all games: D (middle) | n 15, won 6 (40%), -14 (-37 to +9) | n 16, won 7 (44%), -10 (-33 to +12) | n +1, wins +1, +4 pts |
| Okinawa, all games: more caps than the enemy (reference) | n 8, won 3 (38%), -11 (-38 to +17) | too few (n 7) |  |
| Okinawa, Rest-vs-Rest: A (own side) | n 16, won 8 (50%), +3 (-13 to +20) | n 16, won 8 (50%), +2 (-15 to +18) | n +0, wins +0, -1 pts |
| Okinawa, Rest-vs-Rest: C (middle) | n 10, won 6 (60%), +14 (-15 to +41) | n 10, won 6 (60%), +14 (-15 to +41) | n +0, wins +0, +0 pts |
| Okinawa, Rest-vs-Rest: D (middle) | n 10, won 4 (40%), -16 (-42 to +15) | n 10, won 4 (40%), -16 (-42 to +14) | n +0, wins +0, +0 pts |
| Okinawa, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 3) |  |
| Sea of Fortune, all games: A (enemy side) | too few (n 6) | too few (n 7) |  |
| Sea of Fortune, all games: B (own side) | n 32, won 16 (50%), -1 (-8 to +6) | n 35, won 17 (49%), -1 (-7 to +6) | n +3, wins +1, -0 pts |
| Sea of Fortune, all games: C (middle) | n 16, won 6 (38%), -12 (-29 to +8) | n 18, won 6 (33%), -13 (-31 to +4) | n +2, wins +0, -2 pts |
| Sea of Fortune, all games: D (middle) | n 17, won 12 (71%), +15 (-5 to +30) | n 18, won 12 (67%), +14 (-6 to +31) | n +1, wins +0, -1 pts |
| Sea of Fortune, all games: more caps than the enemy (reference) | n 15, won 8 (53%), -0 (-24 to +20) | n 15, won 7 (47%), -2 (-22 to +18) | n +0, wins -1, -2 pts |
| Sea of Fortune, Rest-vs-Rest: B (own side) | n 15, won 7 (47%), -5 (-18 to +3) | n 17, won 8 (47%), -4 (-16 to +3) | n +2, wins +1, +1 pts |
| Sea of Fortune, Rest-vs-Rest: C (middle) | n 8, won 3 (38%), -12 (-38 to +16) | n 9, won 3 (33%), -16 (-38 to +11) | n +1, wins +0, -4 pts |
| Sea of Fortune, Rest-vs-Rest: D (middle) | n 9, won 7 (78%), +16 (-10 to +35) | n 10, won 7 (70%), +14 (-11 to +36) | n +1, wins +0, -2 pts |
| Sea of Fortune, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 6) | too few (n 5) |  |
| Sleeping Giant, all games: A (middle) | n 29, won 17 (59%), +6 (-9 to +20) | n 32, won 15 (47%), -3 (-18 to +11) | n +3, wins -2, -9 pts |
| Sleeping Giant, all games: B (middle) | n 16, won 10 (62%), +10 (-9 to +31) | n 17, won 10 (59%), +7 (-13 to +27) | n +1, wins +0, -3 pts |
| Sleeping Giant, all games: C (enemy side) | n 11, won 6 (54%), +2 (-25 to +28) | n 12, won 7 (58%), +6 (-20 to +30) | n +1, wins +1, +4 pts |
| Sleeping Giant, all games: D (own side) | n 47, won 24 (51%), +0 (-5 to +6) | n 52, won 27 (52%), +1 (-4 to +7) | n +5, wins +3, +1 pts |
| Sleeping Giant, all games: more caps than the enemy (reference) | n 17, won 12 (71%), +11 (-10 to +30) | n 19, won 11 (58%), +3 (-16 to +22) | n +2, wins -1, -8 pts |
| Sleeping Giant, Rest-vs-Rest: A (middle) | n 10, won 5 (50%), +2 (-27 to +31) | n 12, won 5 (42%), -5 (-28 to +22) | n +2, wins +0, -7 pts |
| Sleeping Giant, Rest-vs-Rest: D (own side) | n 16, won 8 (50%), -2 (-16 to +10) | n 20, won 10 (50%), -2 (-14 to +8) | n +4, wins +2, +0 pts |
| Sleeping Giant, Rest-vs-Rest: more caps than the enemy (reference) | too few (n 4) | too few (n 6) |  |

Rows that were clear in round 5 and are not now: Loop C (middle) (Rest-vs-Rest). Rows that became clear: none.

Why: better data, same definition. Twelve games with no snapshot near 8:00 are now included, the owner is read at the exact second instead of up to 60 s away, and two games on a 15-minute clock are read at the right moment. Intervals also move by a point or so between runs of the same data because they come from resampling. No conclusion changed: every pooled row moved by 3 points or less.

