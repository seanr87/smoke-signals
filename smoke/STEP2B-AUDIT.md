# STEP 2b: outlier audit of the full-field batch

Batch `output/20261116-132014` (341 runs, 1,547 smokes, 30 clans). Checks run with
`smoke/tools/audit.py` and `smoke/tools/audit2.py` (their output is in the appendix).
No smoke definition or metric changed. One data correction was applied, by the
committed script `smoke/tools/recover_one_sided.py` (item 4).

## Summary

| Item | Finding | Real? |
|---|---|---|
| -BN- 90,868 concealed/game | One shooter (BN_NAB_LV, Smolensk) behind the clan's destroyer smokes. No doubled ledger, no shooter credited above its ledger, every event credited once. | Yes |
| INCA 89,671 concealed/game | Three of INCA's six games have a doubled damage ledger: the two replays' clocks differ by 6.5 to 8.5 s, beyond the 6 s the merge searches, so every hit seen by both replays was kept twice. 64% of INCA's concealed damage sits in those games. | No, inflated. Roughly 61k/game once halved; needs a re-run with the fix |
| Flagged 21% vs 10% | 218 of the 326 flags are the soft "nearest ship over 600 m" note on the short-burst smoke of Daring, Svea and Z-42, each with a matching activation. The original 3 clans used 6% short-burst smokes, the other 27 use 33%. Not an attribution problem. | Calibration artefact |
| MACH 16 of 29 flagged | MACH smokes from Daring, Z-42 and Svea: 13 carry the 600 m note with a matching activation, 3 have no activation seen (pre-existing category, same rate as round 6). | Not an error |
| KSE and RMN low damage | Real: few smokes (2.9 and 2.0 per game), mostly cap-contest and escape smokes, no 20k damage smoke for KSE and one for RMN. Ledgers reconcile, no replay truncated. | Yes |
| Single-replay game | 4 of the 9 smokes in LB R1 KSC vs -BN- G3 were KSC's, attributed to -BN- ships 8 to 37 km away. Reassigned to KSC's only smoke ship and marked `one_sided`. | Fixed in data |

Two real defects were found. Neither was changed in the method; both are proposed below for approval.

- Perspective merge misses clock offsets over 6 s (3 games fully doubled; INCA, KM, BONKZ, HFANS affected).
- Torpedo damage credited as shell damage for 23 shooter-runs (325k of 16.25 M credited, 2%).

## 1. -BN- and INCA

### -BN-: 14 games, 95 smokes, 1,272,146 concealed (90,868 per game)

Top 10 by concealed damage. The shooter is BN_NAB_LV's Smolensk in every one; the smoker is a destroyer.

| # | game | clock | smoker | ship | concealed | detected | shooters |
|---|---|---|---|---|---|---|---|
| 1 | Group 3 R6 vs SCCC2 (Sleeping Giant) | 16:25 | BN_jordi_92T | Gearing | 97,327 | 0 | BN_NAB_LV |
| 2 | LB R1 vs KSC g2 (Hotspot) | 14:02 | BN_jordi_92T | Somers | 89,662 | 0 | BN_NAB_LV |
| 3 | WB R1 vs KITE g1 (Land of Fire) | 12:41 | BN_jordi_92T | Somers | 83,433 | 1,351 | BN_NAB_LV; BN_jordi_92T |
| 4 | LB R1 vs KSC g3 (Mountain Range) | 11:36 | BN_NAB_LV | Smolensk | 73,837 | 0 | BN_NAB_LV |
| 5 | Group 3 R5 vs NGA (Mountain Range) | 13:41 | BN_TheRuzzO | Gearing | 66,418 | 0 | BN_NAB_LV |
| 6 | Group 3 R7 vs KITED (Sea of Fortune) | 17:52 | BN_jordi_92T | Harugumo | 58,876 | 0 | BN_NAB_LV |
| 7 | LB R1 vs KSC g3 (Mountain Range) | 10:26 | BN_jordi_92T | Gearing | 52,003 | 0 | BN_NAB_LV; BN_BAN_CV_SUB |
| 8 | LB R1 vs KSC g3 (Mountain Range) | 13:39 | BN_jordi_92T | Gearing | 49,720 | 0 | BN_NAB_LV |
| 9 | LB R2 vs MZY g1 (Okinawa) | 16:36 | BN_jordi_92T | Harugumo | 41,579 | 13,970 | BN_NAB_LV; BN_jordi_92T |
| 10 | WB R1 vs KITE g2 (Sleeping Giant) | 15:17 | BN_jordi_92T | Gearing | 40,858 | 0 | BN_NAB_LV |

Reconciliation per game (the clan's smoke credit against its own shell-plus-fire ledger and the game's result blob):

- Smoke credit is 4% to 42% of the clan's ledger in every game; never above it.
- No shooter is credited more than its ledger (highest 1.00, KITED game). Over the 14 runs the only credit above a shooter's game result is BN_jordi_92T in two games, 16,248 in all (the torpedo issue in section 2b).
- No damage event carries credit shares summing above 1.0 in any -BN- run (overlapping smokes split the credit; they do not double it).
- None of -BN-'s 14 runs has an inflated ledger (ratio ledger over result at or under 1.25).

Verdict: real. -BN- plays a Smolensk behind destroyer smokes and it farms. The KSC g3 game (one replay) contributes 196,643 from -BN-'s own replay, which sees -BN-'s own shots in full.

### INCA: 6 games, 39 smokes, 538,028 concealed (89,671 per game)

Top 10 by concealed damage:

| # | game | clock | smoker | ship | concealed | detected | shooters |
|---|---|---|---|---|---|---|---|
| 1 | Group 4 R1 vs KM (Hotspot) | 15:06 | INCA_run_for_yo | Gearing | 94,628 | 1,078 | INCA_AmilcarFro; INCA_HugoPerC02 |
| 2 | Group 4 R6 vs BONKZ (Sleeping Giant) | 14:00 | INCA_AmilcarFro | Gearing | 81,317 | 5,561 | INCA_Icewave; INCA_Timgad |
| 3 | Group 4 R1 vs KM (Hotspot) | 11:24 | INCA_run_for_yo | Gearing | 78,823 | 22,291 | INCA_HugoPerC02 |
| 4 | Group 4 R7 vs MANBA (Sea of Fortune) | 16:07 | INCA_AmilcarFro | Somers | 54,379 | 401 | 4 shooters |
| 5 | Group 4 R2 vs EPOXY (Loop) | 11:22 | INCA_almirandth | Fuyutsuki | 34,319 | 0 | INCA_almirandth |
| 6 | Group 4 R4 vs HFANS (Land of Fire) | 11:57 | INCA_AmilcarFro | F. Sherman | 30,856 | 1,782 | INCA_AmilcarFro; INCA_luoya |
| 7 | Group 4 R5 vs RESIN (Mountain Range) | 07:35 | INCA_AmilcarFro | Gearing | 25,110 | 0 | INCA_Roba_Ninos |
| 8 | Group 4 R4 vs HFANS (Land of Fire) | 10:42 | INCA_almirandth | Fuyutsuki | 22,230 | 0 | INCA_almirandth |
| 9 | Group 4 R5 vs RESIN (Mountain Range) | 16:52 | INCA_Sicilia_Im | Svea | 16,107 | 0 | INCA_Sicilia_Im |
| 10 | Group 4 R1 vs KM (Hotspot) | 10:38 | INCA_Sicilia_Im | Svea | 13,488 | 0 | INCA_Sicilia_Im |

The ledger check fails in three games:

| game | clan ledger shell+fire | clan game result shell+fire | ratio (whole game) | events per replay | dropped as duplicates | clock offset between replays |
|---|---|---|---|---|---|---|
| R1 vs KM | 864,824 | 435,261 | 1.99 | 871, 860 | 275 | 8.5 s |
| R6 vs BONKZ | 676,913 | 383,221 | 1.66 | 669, 560 | 122 | 8.25 s |
| R4 vs HFANS | 468,288 | 297,259 | 1.62 | 411, 568 | 151 | 6.5 s |

Cause: `merge_ledgers` in `crates/smoke-signals/src/damage.rs` searches the clock offset between the two replays within `PERSPECTIVE_OFFSET_MAX_SECONDS` = 6 s. In these three games the offset is 6.5 to 8.5 s (the modal time difference between same attacker, victim and amount shell pairs). No offset is found, the fallback window at offset 0 matches nothing, and almost every hit seen by both replays is kept twice. The game result blob confirms it: the ledger is 1.6 to 2.0 times the result, and INCA_HugoPerC02 is credited 163,380 smoke damage against a game result of 120,659 shell-plus-fire.

The KM, BONKZ and HFANS runs of the same games are doubled the same way (KM 660 concealed, BONKZ 180,622, HFANS 13,707 in those runs).

Verdict: not real as reported. 342,990 of INCA's 538,028 concealed damage (64%) is in the three doubled games. Halving that part gives about 61,000 per game, which would place INCA with H-SR and BONKZ rather than above everyone; the exact figure needs a re-run after the fix.

Across the whole batch (shell-plus-fire ratio ledger over result): 27 runs under 0.95, 93 at 0.95 to 1.05, 201 at 1.05 to 1.25, 14 at 1.25 to 1.6, 6 above 1.6. The 1.05 to 1.25 band is the known behaviour since round 3 (average 1.05). The 14 runs at 1.25 to 1.4 (7 games: BTLST vs MZY, MANBA vs KM, PN vs HTDOG, KITE vs RMN, 5D vs KITE, UYSC vs HTDOG, SCCC2 vs MACHX, NGA vs SCCC2) have offsets of 3 to 4.5 s, inside the search window, so their partial inflation has another cause (two offset peaks in the same game, likely drift). PN vs HTDOG is an original round 6 game and was the same then. Left as backlog.

Concealed damage in inflated runs, per clan: INCA 64% of its total, KM 44%, MANBA 39%, PN 36%, SCCC2 24%, 5D 14%, NGA 14%, BONKZ 13%, BTLST 8%, HTDOG 7%, UYSC 4%, MACHX 2%, MZY 2%, HFANS 1%, KITE 0%, RMN 0%.

## 2. Flags: 326 of 1,547 (21.1%)

### 2a. By type, by original 3, by clan

| flag type | count | notes |
|---|---|---|
| nearest ship over 600 m (alone) | 223 | owner confirmed by an activation within 5 s and 1 km |
| no activation within 5 s + position from minimap only | 71 | ship outside the recorder's precise-position range |
| no activation within 5 s (alone) | 23 | nearest fitted ship within 600 m |
| no activation + nearest ship over 600 m | 9 | 4 are the one-sided KSC smokes (item 4) |

| group | smokes | flagged | % | no activation | minimap | over 600 m |
|---|---|---|---|---|---|---|
| original 3 (H-SR, RESIN, PN) | 217 | 22 | 10.1 | 17 | 15 | 7 |
| other 27 | 1,330 | 304 | 22.9 | 86 | 56 | 225 |
| round 6 (same 217) | 217 | 22 | 10.1 | | | |

The original 3 are exactly as in round 6. The rise is the 600 m note.

The 600 m note by ship (two-replay games): Daring 101 of 200 smokes, Svea 81 of 199, Z-42 38 of 56, every other ship 0 to 3. All three carry the short-burst "cruiser" smoke. For these smokes the attributed ship is 600 to 834 m from the first puff (median 627 m) and 218 of 220 have a matching activation within 5 s. Unflagged short-burst smokes sit at a median of 137 m; unflagged standard smokes at 484 m (p90 519 m). So the origin of a short-burst smoke is either near the ship or about 630 m from it, and the 600 m threshold, set on the original 3 clans' ship mix (87% standard, 6% short-burst), splits that second mode. The other 27 clans use 33% short-burst smokes.

Is the note an owner-attribution problem? No:

- 218 of the 220 have an activation by the attributed ship within 5 s before creation and within 1 km (the rule's confirmed path). The two without are Gdansk at 1,154 m and Delny at 1,069 m, no activation, in two-replay games; those two are uncertain.
- No ship in a two-replay game is credited more smokes than it carries charges (checked over every ship-game; the only breach is the one-sided KSC game, item 4).
- Charge numbers run in sequence per ship (1/7, 2/7, ... in the MACH table below).

By clan, flagged share: MACH 55%, KM 47%, RSR 42%, KSC 37%, SCCC2 33%, -BN- 27%, HTDOG 27%, EPOXY 27%, KITE 27%, INCA 26%, MZY 26%, BONKY 25%, VRTUS 24%, KITED 22%, NGA 21%, HFANS 17%, MACHX 17%, PFANS 17%, REEEE 17%, BONKZ 15%, PN 14%, H-SR 12%, MANBA 11%, BTLST 9%, UYSC 8%, RESIN 8%, RMN 8%, KSE 5%, 5D 3%, OGF 0%. The high clans are the Daring, Svea and Z-42 users.

### 2b. MACH's 16 of 29

| smoke | game | clock | smoker | ship | charge | note | dist m |
|---|---|---|---|---|---|---|---|
| 111112 | R1 vs KITED (Hotspot) | (none) | MACH_Ariokk | Daring | ?/7 | no activation; 698 m | 698 |
| 111108 | R1 vs KITED (Hotspot) | 15:47 | MACH_Ariokk | Daring | 1/7 | 663 m | 663 |
| 111114 | R1 vs KITED (Hotspot) | 11:28 | MACH_Ariokk | Daring | 2/7 | 726 m | 726 |
| 55740 | R2 vs NGA (Loop) | 13:45 | MACH_CC2341 | Z-42 | 3/6 | 628 m | 628 |
| 55742 | R2 vs NGA (Loop) | 12:17 | MACH_CC2341 | Z-42 | 4/6 | 669 m | 669 |
| 55745 | R2 vs NGA (Loop) | 09:09 | MACH_CC2341 | Z-42 | 6/6 | 632 m | 632 |
| 130511 | R3 vs SCCC2 (Okinawa) | (none) | MACH_Ridonc | Svea | ?/7 | no activation | 335 |
| 130515 | R3 vs SCCC2 (Okinawa) | (none) | MACH_Ridonc | Svea | ?/7 | no activation; minimap position | 601 |
| 130518 | R3 vs SCCC2 (Okinawa) | (none) | MACH_Ridonc | Svea | ?/7 | no activation | 276 |
| 130512 | R3 vs SCCC2 (Okinawa) | 16:50 | MACH_Rasputia | Daring | 1/7 | 652 m | 652 |
| 130520 | R3 vs SCCC2 (Okinawa) | 13:34 | MACH_Ridonc | Svea | 1/7 | 628 m | 628 |
| 68242 | R4 vs -BN- (Land of Fire) | 14:31 | MACH_SureBridge | Z-42 | 2/7 | 647 m | 647 |
| 95020 | R5 vs MACHX (Mountain Range) | 11:44 | MACH_SureBridge | Z-42 | 3/7 | 614 m | 614 |
| 95022 | R5 vs MACHX (Mountain Range) | 09:44 | MACH_SureBridge | Z-42 | 4/7 | 624 m | 624 |
| 71187 | R6 vs BONKY (Sleeping Giant) | 09:54 | MACH_CC2341 | Z-42 | 2/6 | 622 m | 622 |
| 214881 | R7 vs H-SR (Sea of Fortune) | 17:06 | MACH_Ariokk | Z-42 | 1/6 | 612 m | 612 |

MACH smokes almost only from Daring, Z-42 and Svea. 12 flags are the 600 m note with a matching activation (owner certain). 4 have no activation seen: 3 by MACH_Ridonc's Svea in one game (nearest fitted ship at 276 to 601 m, the standard fallback) and one Daring at 698 m. The no-activation category exists in round 6 at the same rate (17 of 217 then, 103 of 1,547 now); none of the 103 is the recorder's own ship, 86 of 103 are after the 5 minute mark, and 71 of them also lack a precise position, which points at ships outside the recorder's position-update range. Those are attributed to the nearest fitted ship and stay flagged.

### 2c. Attribution errors found

| where | smokes | what | fix |
|---|---|---|---|
| LB R1 KSC vs -BN- G3 (one replay) | 178892, 178895, 178898, 178900 | KSC's Gearing smokes attributed to -BN- ships 8 to 37 km away: the KSC ship was unspotted, so it had no position and was not a candidate | Reassigned to KSC_PidgeyArmy's Gearing by `recover_one_sided.py` (item 4); method fix proposed below |
| 5516 (H-SR vs NGA, Hotspot, 09:35, HSR_Arona_daisu Delny, 2,440 concealed) and 29881 (PFANS vs KSC, Sleeping Giant, 06:06, PFANS_THIS_IS_N Gdansk, 0 damage) | 2 | no activation and nearest ship 1,069 and 1,154 m | uncertain; left flagged |

Nothing else in the 326 points at a wrong owner.

### 2d. A second defect found on the way: torpedo damage credited as shell damage

Checking every shooter's smoke credit against the game's own shell-plus-fire result found 23 shooter-runs credited above their result (803 checked). 4 are in the doubled-ledger games. The other 19 share a pattern: the ledger total equals the game total, but the game says most of it was not shells or fire. Examples: MACHX_SPAAAAAAA (Grozovoi) credited 105,982 against a shell-plus-fire result of 20,384; BONKZ_Dyr3 (Somers) 52,555 against 11,626; HTDOG_Amogussy (Napoli) 10,996 against 0. These are torpedo hits that the weapon classifier matched to "the attacker's latest salvo within 25 s" (DESIGN.md 6.2), and credited to a smoke. Total excess over the shooters' results in non-inflated runs: 325,410 of 16.25 M credited (2.0%); MACHX 85,812, BONKZ 40,929, KSC 32,870, EPOXY 24,353, REEEE 22,406, RMN 18,407, others under 18k. H-SR has one mild case (HSR_VoyagingSta, 31,171 against 27,094) that was in round 6.

## 3. KSE and RMN

KSE: 7 games, 20 smokes (2.9 per game): 15 destroyer, 5 cruiser (Gdansk 10, Napoli 5, Daring 5). Coverage: selfish 10, screen 7, stacked 3. Purposes: cap_contest 5, counter_smoke 4, escape 2, island_dive 2, reposition 1, cap_control 1, none 5. 10 smokes have any damage, none reaches 20k. Concealed 32,981 (4,712 per game, 1,649 per smoke). Every game's ledger reconciles (ratios 0.96 to 1.04), both replays present with 400 to 1,013 events each, none truncated. KSE lost 5 of 7.

RMN: 6 games, 12 smokes (2.0 per game): 11 destroyer, 1 cruiser (Shimakaze 4, Gearing 3, F. Sherman 2, Grozovoi 2, Svea 1). Coverage: stacked 4, selfish 4, screen 4. Purposes: cap_contest 5, escape 2, none 5. 4 smokes have any damage, one reaches 20k (26,395, which is the RMN_Siadant torpedo case above, so the real figure is lower). Concealed 31,236 (5,206 per game). Ledgers reconcile (0.95 to 1.06), no truncation. RMN lost all 6.

Verdict: real. Both clans smoke little and use the smokes to contest caps and escape, not to shoot from. The data is complete.

## 4. Single-replay game: LB R1 KSC vs -BN- G3

The -BN- run saw 9 smokes and kept all 9 as -BN-'s. The roster from -BN-'s replay knows the smoke fit of both -BN- smoke ships (Smolensk 3 charges, Gearing 3 charges) and of one KSC ship, KSC_PidgeyArmy's Gearing (4 charges, 0 activations seen). Four smokes were attributed to a -BN- ship 8,189 to 37,425 m from the origin with no activation, which made BN_jordi_92T's Gearing the owner of 6 smokes on 3 charges. Those four are KSC's: KSC has exactly one ship fitted with smoke, it was unspotted when it smoked (no position, so not a candidate), and the four origins lie on KSC's side of the map.

Can they be recovered? Yes, as smokes: position, puffs, timing (18:22, 14:34, 11:29, 07:05 on the clock) and frames are all from -BN-'s replay. Not as damage: KSC's shots from inside its smoke come from an unspotted shooter with no position, so no credit can be given; they stay at 0.

Done: `smoke/tools/recover_one_sided.py` adds a `one_sided` column (true for the 9 smokes of this game, false elsewhere) and reassigned the four to KSC_PidgeyArmy's Gearing (standard smoke, 4 charges) with owner_note "one-sided: seen from the -BN- replay only; owner inferred as the only KSC ship fitted with smoke (nearest -BN- ship was N m from the origin)". Applied to the batch's smokes.json and smokes.csv in place (git keeps the previous version); the run folder is untouched; the data zip was re-exported. Count: 9 one-sided smokes, 4 reassigned. -BN- goes to 91 smokes (concealed damage unchanged, the four had none); KSC to 63.

Caveats on the four: coverage "selfish" and allies inside 0 are what one replay could see; charge_no is blank; the Games page roster for KSC in that game comes from -BN-'s view (4 charges carried, 0 used).

## 5. Backlog (not fixed now)

1. Roster `smoke_activations` double-counts a use seen by both replays more than 1 s apart (83 ships show more activations than charges; 87 team-games off by more than one against smokes found). Not used by any metric except charge use, which the own-run roster rule (527aae2d) keeps on the own replay's count; still, the counter should merge uses within the perspective clock offset.
2. Perspective merge: offsets of 6.5 to 8.5 s are missed (section 1, 3 games doubled); the 1.25 to 1.4 band (7 games) has two offset peaks in one game.
3. Torpedo hits matched to a recent salvo and credited as shell damage (section 2d, 23 shooter-runs, 2% of credit).
4. The 600 m owner note on short-burst smokes (section 2a, 218 flags with a confirmed owner).
5. One-sided attribution in the analysis itself (section 4; the script is a stopgap).

## Proposed method changes (need approval; nothing applied)

| # | change | effect |
|---|---|---|
| F1 | `PERSPECTIVE_OFFSET_MAX_SECONDS` 6 to 12 s in damage.rs, then re-run the 3 doubled games (6 runs) or the whole batch | INCA, KM, BONKZ and HFANS damage in those games halves to the true value; INCA about 61k per game |
| F2 | Do not add the "nearest ship over 600 m" note when an activation within 5 s and 1 km confirms the owner (or raise the note threshold to 850 m for confirmed owners) | 218 fewer flags; no owner changes; flagged share about 7% |
| F3 | In the owner search, when the nearest positioned candidate is over 2 km away and the other team has exactly one fitted ship without a position, attribute to it with a one-sided note | Makes item 4 part of the method; the script becomes unnecessary |
| F4 | Classify a hit as shell only when a shot hit resolves or the attacker has no torpedoes in the water; cap a shooter's smoke credit by its shell-plus-fire result as a last resort | Removes about 325k of torpedo credit (2%) |
| F5 | Merge roster activations within the perspective offset window | Honest activation counts |

Recommendation: F1 before the site build (it changes a headline clan number), F2 with it (cheap, cosmetic), F3 to F5 after the site, since their effect is small or cosmetic.

## Appendix: audit output

Output of the two scripts, run against the batch before the one-sided correction (item 4), with the round 6 batch `output/20261104-180332` for comparison.

### audit.py

```
# 1. -BN- and INCA

## -BN-: 14 games, 95 smokes, concealed 1,272,146 (90,868/game), total 1,375,196 (98,228/game)

Top 10 smokes by concealed damage:
| # | game | clock | smoker | ship | concealed | detected | total | shooters | flag | overlap |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Group 3 / Round 6 -BN- vs SCCC2 g1 (Sleeping Giant) | 16:25 | BN_jordi_92T | Gearing | 97,327 | 0 | 97,327 | BN_NAB_LV | - | false |
| 2 | Losers Bracket / LB Round 1 -BN- vs KSC g2 (Hotspot) | 14:02 | BN_jordi_92T | Somers | 89,662 | 0 | 89,662 | BN_NAB_LV | - | false |
| 3 | Winners Bracket / WB Round 1 -BN- vs KITE g1 (Land of Fire) | 12:41 | BN_jordi_92T | Somers | 83,433 | 1,351 | 84,784 | BN_NAB_LV;BN_jordi_92T | - | false |
| 4 | Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) | 11:36 | BN_NAB_LV | Smolensk | 73,837 | 0 | 73,837 | BN_NAB_LV | - | true |
| 5 | Group 3 / Round 5 -BN- vs NGA g1 (Mountain Range) | 13:41 | BN_TheRuzzO | Gearing | 66,418 | 0 | 66,418 | BN_NAB_LV | - | true |
| 6 | Group 3 / Round 7 -BN- vs KITED g1 (Sea of Fortune) | 17:52 | BN_jordi_92T | Harugumo | 58,876 | 0 | 58,876 | BN_NAB_LV | - | false |
| 7 | Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) | 10:26 | BN_jordi_92T | Gearing | 52,003 | 0 | 52,003 | BN_NAB_LV;BN_BAN_CV_SUB | - | false |
| 8 | Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) | 13:39 | BN_jordi_92T | Gearing | 49,720 | 0 | 49,720 | BN_NAB_LV | - | true |
| 9 | Losers Bracket / LB Round 2 -BN- vs MZY g1 (Okinawa) | 16:36 | BN_jordi_92T | Harugumo | 41,579 | 13,970 | 55,550 | BN_NAB_LV;BN_jordi_92T | - | false |
| 10 | Winners Bracket / WB Round 1 -BN- vs KITE g2 (Sleeping Giant) | 15:17 | BN_jordi_92T | Gearing | 40,858 | 0 | 40,858 | BN_NAB_LV | - | false |

Per-game reconciliation (-BN-: smoke credit per shooter vs that shooter's ledger shell+fire and the game's own result):
| game | smokes | smoke dmg total | clan ledger shell+fire | clan game result shell+fire | credit/ledger | max shooter credit/ledger | over-credited shooters | dup events dropped | events per replay |
|---|---|---|---|---|---|---|---|---|---|
| Group 3 / Round 1 -BN- vs MACHX g1 (Hotspot) | 9 | 29,302 | 200,879 | 210,108 | 0.15 | 0.90 | - | 310 | [412, 372] |
| Group 3 / Round 2 -BN- vs BONKY g1 (Loop) | 8 | 67,883 | 729,547 | 709,586 | 0.09 | 0.90 | - | 1088 | [1285, 1395] |
| Group 3 / Round 3 -BN- vs H-SR g1 (Okinawa) | 6 | 42,930 | 230,978 | 289,722 | 0.19 | 0.56 | - | 490 | [632, 586] |
| Group 3 / Round 4 -BN- vs MACH g1 (Land of Fire) | 6 | 57,262 | 714,285 | 665,934 | 0.08 | 0.40 | - | 706 | [840, 1229] |
| Group 3 / Round 5 -BN- vs NGA g1 (Mountain Range) | 5 | 116,439 | 361,683 | 352,261 | 0.32 | 0.87 | - | 284 | [338, 360] |
| Group 3 / Round 6 -BN- vs SCCC2 g1 (Sleeping Giant) | 9 | 143,762 | 768,656 | 761,839 | 0.19 | 0.71 | - | 1101 | [1310, 1241] |
| Group 3 / Round 7 -BN- vs KITED g1 (Sea of Fortune) | 11 | 158,448 | 642,176 | 652,319 | 0.25 | 1.00 | - | 597 | [756, 753] |
| Winners Bracket / WB Round 1 -BN- vs KITE g1 (Land of Fire) | 4 | 88,989 | 652,063 | 569,943 | 0.14 | 0.57 | - | 447 | [704, 525] |
| Winners Bracket / WB Round 1 -BN- vs KITE g2 (Sleeping Giant) | 10 | 141,933 | 514,155 | 491,673 | 0.28 | 0.94 | - | 692 | [815, 832] |
| Losers Bracket / LB Round 1 -BN- vs KSC g1 (Sleeping Giant) | 6 | 49,617 | 435,049 | 412,463 | 0.11 | 0.54 | - | 723 | [909, 784] |
| Losers Bracket / LB Round 1 -BN- vs KSC g2 (Hotspot) | 7 | 163,894 | 559,559 | 484,969 | 0.29 | 0.62 | - | 479 | [674, 780] |
| Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) | 9 | 196,643 | 466,490 | 543,598 | 0.42 | 0.93 | - | 0 | [888] |
| Losers Bracket / LB Round 2 -BN- vs MZY g1 (Okinawa) | 3 | 93,693 | 418,470 | 404,143 | 0.22 | 0.96 | - | 863 | [959, 976] |
| Losers Bracket / LB Round 2 -BN- vs MZY g2 (Land of Fire) | 2 | 24,401 | 604,615 | 546,247 | 0.04 | 0.47 | - | 1064 | [1267, 1205] |

## INCA: 6 games, 39 smokes, concealed 538,028 (89,671/game), total 585,238 (97,540/game)

Top 10 smokes by concealed damage:
| # | game | clock | smoker | ship | concealed | detected | total | shooters | flag | overlap |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Group 4 / Round 1 INCA vs KM g1 (Hotspot) | 15:06 | INCA_run_for_yo | Gearing | 94,628 | 1,078 | 95,706 | INCA_AmilcarFro;INCA_HugoPerC02 | - | false |
| 2 | Group 4 / Round 6 INCA vs BONKZ g1 (Sleeping Giant) | 14:00 | INCA_AmilcarFro | Gearing | 81,317 | 5,561 | 86,878 | INCA_Icewave;INCA_Timgad | - | false |
| 3 | Group 4 / Round 1 INCA vs KM g1 (Hotspot) | 11:24 | INCA_run_for_yo | Gearing | 78,823 | 22,291 | 101,115 | INCA_HugoPerC02 | - | false |
| 4 | Group 4 / Round 7 INCA vs MANBA g1 (Sea of Fortune) | 16:07 | INCA_AmilcarFro | Somers | 54,379 | 401 | 54,780 | INCA_AmilcarFro;INCA_SirPeterBl;INCA_Icewave;INCA_Timgad | - | false |
| 5 | Group 4 / Round 2 INCA vs EPOXY g1 (Loop) | 11:22 | INCA_almirandth | Fuyutsuki | 34,319 | 0 | 34,319 | INCA_almirandth | - | false |
| 6 | Group 4 / Round 4 INCA vs HFANS g1 (Land of Fire) | 11:57 | INCA_AmilcarFro | F. Sherman | 30,856 | 1,782 | 32,638 | INCA_AmilcarFro;INCA_luoya | - | false |
| 7 | Group 4 / Round 5 INCA vs RESIN g1 (Mountain Range) | 07:35 | INCA_AmilcarFro | Gearing | 25,110 | 0 | 25,110 | INCA_Roba_Ninos | - | false |
| 8 | Group 4 / Round 4 INCA vs HFANS g1 (Land of Fire) | 10:42 | INCA_almirandth | Fuyutsuki | 22,230 | 0 | 22,230 | INCA_almirandth | - | false |
| 9 | Group 4 / Round 5 INCA vs RESIN g1 (Mountain Range) | 16:52 | INCA_Sicilia_Im | Svea | 16,107 | 0 | 16,107 | INCA_Sicilia_Im | - | false |
| 10 | Group 4 / Round 1 INCA vs KM g1 (Hotspot) | 10:38 | INCA_Sicilia_Im | Svea | 13,488 | 0 | 13,488 | INCA_Sicilia_Im | - | false |

Per-game reconciliation (INCA: smoke credit per shooter vs that shooter's ledger shell+fire and the game's own result):
| game | smokes | smoke dmg total | clan ledger shell+fire | clan game result shell+fire | credit/ledger | max shooter credit/ledger | over-credited shooters | dup events dropped | events per replay |
|---|---|---|---|---|---|---|---|---|---|
| Group 4 / Round 1 INCA vs KM g1 (Hotspot) | 11 | 229,347 | 864,824 | 435,261 | 0.27 | 0.85 | - | 275 | [871, 860] |
| Group 4 / Round 2 INCA vs EPOXY g1 (Loop) | 7 | 62,273 | 419,705 | 402,889 | 0.15 | 0.54 | - | 753 | [1131, 954] |
| Group 4 / Round 4 INCA vs HFANS g1 (Land of Fire) | 5 | 57,477 | 468,288 | 297,259 | 0.12 | 0.58 | - | 151 | [411, 568] |
| Group 4 / Round 5 INCA vs RESIN g1 (Mountain Range) | 13 | 94,482 | 504,978 | 467,231 | 0.19 | 0.65 | - | 727 | [910, 823] |
| Group 4 / Round 6 INCA vs BONKZ g1 (Sleeping Giant) | 2 | 86,878 | 676,913 | 383,221 | 0.13 | 0.53 | - | 122 | [669, 560] |
| Group 4 / Round 7 INCA vs MANBA g1 (Sea of Fortune) | 1 | 54,780 | 662,237 | 581,958 | 0.08 | 0.24 | - | 664 | [784, 959] |

# 2. Flags
flagged: 326 of 1547 (21.1%)

By flag type (a smoke can carry two):
- nearest ship over 600 m: 232
- no activation within 5 s: 103
- position from minimap only: 71
Combinations:
- nearest ship over 600 m: 223
- no activation within 5 s; position from minimap only: 71
- no activation within 5 s: 23
- no activation within 5 s; nearest ship over 600 m: 9

By original 3 vs the other 27 clans:
- original 3: 22 of 217 (10.1%); {'no activation within 5 s': 17, 'position from minimap only': 15, 'nearest ship over 600 m': 7}
- other 27: 304 of 1330 (22.9%); {'nearest ship over 600 m': 225, 'no activation within 5 s': 86, 'position from minimap only': 56}
- round 6 for comparison: 22 of 217 (10.1%)

Distance of the attributed ship from the smoke origin, flagged smokes:
- 0 to 600 m: 91
- 600 to 1000 m: 229
- 1000 to 2000 m: 2
- 2000 to 5000 m: 0
- 5000 to 10000 m: 1
- 10000 to inf m: 3
Same, for smokes flagged only 'no activation within 5 s' (nearest ship within 600 m):
- count 23; distance max 526 m

By clan:
| clan | original | smokes | flagged | % | no activation only | over 600 m | over 5 km | minimap |
|---|---|---|---|---|---|---|---|---|
| HFANS |  | 110 | 19 | 17 | 0 | 14 | 0 | 5 |
| HTDOG |  | 106 | 29 | 27 | 3 | 24 | 0 | 2 |
| RESIN | yes | 103 | 8 | 8 | 0 | 4 | 0 | 4 |
| BONKZ |  | 102 | 15 | 15 | 1 | 10 | 0 | 4 |
| H-SR | yes | 100 | 12 | 12 | 0 | 2 | 0 | 10 |
| -BN- |  | 95 | 26 | 27 | 0 | 20 | 4 | 7 |
| VRTUS |  | 82 | 20 | 24 | 2 | 18 | 0 | 0 |
| EPOXY |  | 82 | 22 | 27 | 2 | 12 | 0 | 8 |
| MACHX |  | 82 | 14 | 17 | 0 | 14 | 0 | 0 |
| KITED |  | 63 | 14 | 22 | 2 | 11 | 0 | 1 |
| KSC |  | 59 | 22 | 37 | 0 | 18 | 0 | 5 |
| REEEE |  | 52 | 9 | 17 | 0 | 7 | 0 | 2 |
| MZY |  | 50 | 13 | 26 | 2 | 5 | 0 | 6 |
| SCCC2 |  | 48 | 16 | 33 | 2 | 14 | 0 | 0 |
| KITE |  | 45 | 12 | 27 | 0 | 10 | 0 | 2 |
| INCA |  | 39 | 10 | 26 | 3 | 7 | 0 | 0 |
| 5D |  | 37 | 1 | 3 | 0 | 1 | 0 | 0 |
| UYSC |  | 36 | 3 | 8 | 0 | 3 | 0 | 0 |
| BONKY |  | 36 | 9 | 25 | 1 | 5 | 0 | 3 |
| BTLST |  | 34 | 3 | 9 | 0 | 3 | 0 | 0 |
| MACH |  | 29 | 16 | 55 | 2 | 14 | 0 | 1 |
| NGA |  | 28 | 6 | 21 | 0 | 3 | 0 | 3 |
| RSR |  | 26 | 11 | 42 | 0 | 10 | 0 | 1 |
| PFANS |  | 24 | 4 | 17 | 0 | 2 | 0 | 2 |
| KSE |  | 20 | 1 | 5 | 0 | 1 | 0 | 0 |
| KM |  | 15 | 7 | 47 | 3 | 0 | 0 | 4 |
| PN | yes | 14 | 2 | 14 | 0 | 1 | 0 | 1 |
| RMN |  | 12 | 1 | 8 | 0 | 1 | 0 | 0 |
| OGF |  | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| MANBA |  | 9 | 1 | 11 | 0 | 1 | 0 | 0 |

## MACH flagged smokes
| smoke | game | clock | smoker | ship | charge | note | dist m | concealed |
|---|---|---|---|---|---|---|---|---|
| 111112 | Group 3 / Round 1 MACH vs KITED g1 (Hotspot) |  | MACH_Ariokk | Daring | /7 | no smoke activation within 5 s before creation; nearest ship 698 m from origin | 698 | 1,270 |
| 111108 | Group 3 / Round 1 MACH vs KITED g1 (Hotspot) | 15:47 | MACH_Ariokk | Daring | 1/7 | nearest ship 663 m from origin | 663 | 0 |
| 111114 | Group 3 / Round 1 MACH vs KITED g1 (Hotspot) | 11:28 | MACH_Ariokk | Daring | 2/7 | nearest ship 726 m from origin | 726 | 0 |
| 55740 | Group 3 / Round 2 MACH vs NGA g1 (Loop) | 13:45 | MACH_CC2341 | Z-42 | 3/6 | nearest ship 628 m from origin | 628 | 7,785 |
| 55742 | Group 3 / Round 2 MACH vs NGA g1 (Loop) | 12:17 | MACH_CC2341 | Z-42 | 4/6 | nearest ship 669 m from origin | 669 | 9,378 |
| 55745 | Group 3 / Round 2 MACH vs NGA g1 (Loop) | 09:09 | MACH_CC2341 | Z-42 | 6/6 | nearest ship 632 m from origin | 632 | 396 |
| 130511 | Group 3 / Round 3 MACH vs SCCC2 g1 (Okinawa) |  | MACH_Ridonc | Svea | /7 | no smoke activation within 5 s before creation | 335 | 0 |
| 130515 | Group 3 / Round 3 MACH vs SCCC2 g1 (Okinawa) |  | MACH_Ridonc | Svea | /7 | no smoke activation within 5 s before creation; position from minimap samples only | 601 | 726 |
| 130518 | Group 3 / Round 3 MACH vs SCCC2 g1 (Okinawa) |  | MACH_Ridonc | Svea | /7 | no smoke activation within 5 s before creation | 276 | 0 |
| 130512 | Group 3 / Round 3 MACH vs SCCC2 g1 (Okinawa) | 16:50 | MACH_Rasputia | Daring | 1/7 | nearest ship 652 m from origin | 652 | 0 |
| 130520 | Group 3 / Round 3 MACH vs SCCC2 g1 (Okinawa) | 13:34 | MACH_Ridonc | Svea | 1/7 | nearest ship 628 m from origin | 628 | 21,944 |
| 68242 | Group 3 / Round 4 MACH vs -BN- g1 (Land of Fire) | 14:31 | MACH_SureBridge | Z-42 | 2/7 | nearest ship 647 m from origin | 647 | 0 |
| 95020 | Group 3 / Round 5 MACH vs MACHX g1 (Mountain Range) | 11:44 | MACH_SureBridge | Z-42 | 3/7 | nearest ship 614 m from origin | 614 | 1,980 |
| 95022 | Group 3 / Round 5 MACH vs MACHX g1 (Mountain Range) | 09:44 | MACH_SureBridge | Z-42 | 4/7 | nearest ship 624 m from origin | 624 | 0 |
| 71187 | Group 3 / Round 6 MACH vs BONKY g1 (Sleeping Giant) | 09:54 | MACH_CC2341 | Z-42 | 2/6 | nearest ship 622 m from origin | 622 | 0 |
| 214881 | Group 3 / Round 7 MACH vs H-SR g1 (Sea of Fortune) | 17:06 | MACH_Ariokk | Z-42 | 1/6 | nearest ship 612 m from origin | 612 | 0 |

## Attribution checks
ships credited with more smokes than charges carried: 1
- Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range): BN_jordi_92T Gearing: 6 smokes, 3 charges, 3 flagged, notes: [('', 3), ('no smoke activation within 5 s before creation; nearest ship 16108 m from origin', 1), ('no smoke activation within 5 s before creation; nearest ship 29454 m from origin', 1)]

flagged smokes with the attributed ship more than 2 km from the origin (cannot be the owner): 4
| smoke | game | clock | attributed to | ship | dist m | merged replays | concealed | total |
|---|---|---|---|---|---|---|---|---|
| 178898 | Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) |  | BN_NAB_LV | Smolensk | 37425 | 0 | 0 | 0 |
| 178895 | Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) |  | BN_jordi_92T | Gearing | 29454 | 0 | 0 | 0 |
| 178892 | Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) |  | BN_jordi_92T | Gearing | 16108 | 0 | 0 | 0 |
| 178900 | Losers Bracket / LB Round 1 -BN- vs KSC g3 (Mountain Range) |  | BN_jordi_92T | Gearing | 8189 | 0 | 0 | 0 |

'nearest ship over 600 m' smokes in two-replay games: 228; distances: 600-830: 224, 830-1000: 2, 1000-2000: 2, 2000-1000000000.0: 0
their concealed damage total: 962,542

flagged smokes by attributed smoke type: Counter({'cruiser': 235, 'standard': 71, 'exhaust': 19, 'crawling': 1})
all smokes by smoke type: Counter({'standard': 861, 'cruiser': 455, 'exhaust': 215, 'crawling': 16})

# 3. KSE and RMN

## KSE: 7 games, 20 smokes (2.9/game)
smoker class: {'destroyer': 15, 'cruiser': 5}
coverage: {'selfish': 10, 'stacked': 3, 'screen': 7}
primary purpose: {'': 5, 'reposition': 1, 'cap_contest': 5, 'cap_control': 1, 'counter_smoke': 4, 'escape': 2, 'island_dive': 2}
ships: {'Gdansk': 10, 'Napoli': 5, 'Daring': 5}
concealed 32,981 (4,712/game, 1,649/smoke); total 44,867; smokes with any damage: 10; with 20k+: 0
| game | result | smokes | smoke dmg | clan ledger shell+fire | clan game result | ledger ratio (game) | events per replay | truncated |
|---|---|---|---|---|---|---|---|---|
| Round 1 vs PFANS g1 (Hotspot) | L KSE 555 - PFANS 1000 | 3 | 0 | 302,724 | 298,667 | 1.04 | [919, 972] | False |
| Round 2 vs VRTUS g1 (Loop) | L KSE 68 - VRTUS 744 | 2 | 0 | 351,140 | 342,282 | 0.96 | [811, 873] | False |
| Round 3 vs UYSC g1 (Okinawa) | W UYSC 0 - KSE 522 | 3 | 5,602 | 305,384 | 302,865 | 0.99 | [400, 422] | False |
| Round 4 vs KSC g1 (Land of Fire) | L KSC 1000 - KSE 476 | 2 | 9,462 | 340,328 | 302,978 | 1.01 | [567, 599] | False |
| Round 5 vs HTDOG g1 (Mountain Range) | L HTDOG 652 - KSE 0 | 2 | 3,836 | 277,745 | 256,103 | 0.96 | [939, 900] | False |
| Round 6 vs PN g1 (Sleeping Giant) | L PN 1000 - KSE 464 | 5 | 10,032 | 428,625 | 384,145 | 1.00 | [937, 876] | False |
| Round 7 vs RSR g1 (Sea of Fortune) | W KSE 983 - RSR 361 | 3 | 15,935 | 656,331 | 606,301 | 1.00 | [1013, 1006] | False |

## RMN: 6 games, 12 smokes (2.0/game)
smoker class: {'destroyer': 11, 'cruiser': 1}
coverage: {'stacked': 4, 'selfish': 4, 'screen': 4}
primary purpose: {'cap_contest': 5, '': 5, 'escape': 2}
ships: {'Shimakaze': 4, 'Svea': 1, 'F. Sherman': 2, 'Grozovoi': 2, 'Gearing': 3}
concealed 31,236 (5,206/game, 2,603/smoke); total 42,023; smokes with any damage: 4; with 20k+: 1
| game | result | smokes | smoke dmg | clan ledger shell+fire | clan game result | ledger ratio (game) | events per replay | truncated |
|---|---|---|---|---|---|---|---|---|
| Round 1 vs 5D g1 (Hotspot) | L RMN 0 - 5D 772 | 3 | 26,395 | 224,360 | 139,550 | 0.97 | [315, 336] | False |
| Round 2 vs OGF g1 (Loop) | L RMN 144 - OGF 512 | 1 | 1,774 | 323,429 | 243,443 | 0.95 | [673, 665] | False |
| Round 4 vs KITE g1 (Land of Fire) | L KITE 892 - RMN 0 | 1 | 0 | 188,854 | 162,939 | 1.06 | [537, 399] | False |
| Round 5 vs MZY g1 (Mountain Range) | L MZY 776 - RMN 0 | 4 | 1,559 | 222,814 | 205,484 | 0.97 | [456, 445] | False |
| Round 6 vs BTLST g1 (Sleeping Giant) | L BTLST 1000 - RMN 356 | 1 | 0 | 477,608 | 425,079 | 1.02 | [870, 862] | False |
| Round 7 vs REEEE g1 (Sea of Fortune) | L RMN 140 - REEEE 1000 | 2 | 12,296 | 194,529 | 189,561 | 0.97 | [709, 640] | False |

For scale, concealed damage per game and smokes per game, all clans:
| clan | games | smokes | smokes/game | concealed/game | damage smokes (20k+) |
|---|---|---|---|---|---|
| -BN- | 14 | 95 | 6.8 | 90,868 | 20 |
| INCA | 6 | 39 | 6.5 | 89,671 | 9 |
| H-SR | 22 | 100 | 4.5 | 67,832 | 35 |
| BONKZ | 21 | 102 | 4.9 | 66,346 | 23 |
| VRTUS | 11 | 82 | 7.5 | 65,033 | 11 |
| KSC | 11 | 59 | 5.4 | 62,419 | 12 |
| MACHX | 14 | 82 | 5.9 | 56,148 | 13 |
| SCCC2 | 7 | 48 | 6.9 | 55,757 | 6 |
| HFANS | 17 | 110 | 6.5 | 55,386 | 19 |
| RESIN | 24 | 103 | 4.3 | 51,866 | 26 |
| EPOXY | 17 | 82 | 4.8 | 50,477 | 16 |
| HTDOG | 18 | 106 | 5.9 | 49,662 | 12 |
| BONKY | 7 | 36 | 5.1 | 49,243 | 7 |
| KM | 5 | 15 | 3.0 | 37,032 | 5 |
| PFANS | 12 | 24 | 2.0 | 33,294 | 9 |
| REEEE | 13 | 52 | 4.0 | 29,797 | 9 |
| BTLST | 6 | 34 | 5.7 | 27,185 | 3 |
| KITE | 14 | 45 | 3.2 | 24,271 | 5 |
| RSR | 7 | 26 | 3.7 | 24,207 | 4 |
| KITED | 14 | 63 | 4.5 | 23,003 | 4 |
| UYSC | 7 | 36 | 5.1 | 22,784 | 4 |
| MZY | 19 | 50 | 2.6 | 21,181 | 5 |
| 5D | 10 | 37 | 3.7 | 20,824 | 5 |
| NGA | 7 | 28 | 4.0 | 19,164 | 1 |
| PN | 7 | 14 | 2.0 | 16,598 | 2 |
| MACH | 7 | 29 | 4.1 | 16,062 | 4 |
| MANBA | 6 | 9 | 1.5 | 12,454 | 2 |
| OGF | 6 | 9 | 1.5 | 9,217 | 1 |
| RMN | 6 | 12 | 2.0 | 5,206 | 1 |
| KSE | 7 | 20 | 2.9 | 4,712 | 0 |

# 4. Single-replay game LB R1 KSC vs -BN- G3
team -BN-: ships with a smoke fit known: 2 of 9; activations 5; charges 6
  BN_HoshimiMiyab Moskva Cruiser type=None act=0 charges=None
  BN_NAB_LV Smolensk Cruiser type=standard act=2 charges=3
  BN_capitankelvi St. Vincent Battleship type=None act=0 charges=None
  BN_LEGOMrPanda Kremlin Battleship type=None act=0 charges=None
  BN_jordi_92T Gearing Destroyer type=standard act=3 charges=3
  BN_BAN_CV_SUB Marceau Destroyer type=None act=0 charges=None
  BN_DeiMoonKboom Moskva Cruiser type=None act=0 charges=None
  BN_Dominic_MacP Des Moines Cruiser type=None act=0 charges=None
  BN_TheRuzzO Châteaurenault Destroyer type=None act=0 charges=None
team KSC: ships with a smoke fit known: 1 of 9; activations 0; charges 4
  KSC_ganser Châteaurenault Destroyer type=None act=0 charges=None
  KSC_Kissrell Vermont Battleship type=None act=0 charges=None
  KSC_Obi_JuanKen Kremlin Battleship type=None act=0 charges=None
  KSC_PidgeyArmy Gearing Destroyer type=standard act=0 charges=4
  KSC_NakiriAyame Prins van Oranje Cruiser type=None act=0 charges=None
  KSC_Show_Me_You Des Moines Cruiser type=None act=0 charges=None
  KSC_ZombieGnome Prins van Oranje Cruiser type=None act=0 charges=None
  KSC__Sait Châteaurenault Destroyer type=None act=0 charges=None
  KSC_WH_Knight Moskva Cruiser type=None act=0 charges=None
smokes in the run and their attribution:
  178892 -BN- BN_jordi_92T Gearing dist=16107.711 note=no smoke activation within 5 s before creation; nearest ship 16108 m from origin concealed=0 total=0 origin={'x': 172.4656, 'z': -243.22343}
  178893 -BN- BN_jordi_92T Gearing dist=478.50296 note=- concealed=0 total=0 origin={'x': -155.32632, 'z': 191.90625}
  178894 -BN- BN_NAB_LV Smolensk dist=150.37747 note=- concealed=21083 total=21083 origin={'x': -355.19562, 'z': 216.33348}
  178895 -BN- BN_jordi_92T Gearing dist=29453.916 note=no smoke activation within 5 s before creation; nearest ship 29454 m from origin concealed=0 total=0 origin={'x': 522.99927, 'z': -419.5924}
  178896 -BN- BN_jordi_92T Gearing dist=521.0705 note=- concealed=49720 total=49720 origin={'x': -361.97244, 'z': 215.4292}
  178897 -BN- BN_NAB_LV Smolensk dist=482.92963 note=- concealed=73837 total=73837 origin={'x': -332.9945, 'z': 218.0546}
  178898 -BN- BN_NAB_LV Smolensk dist=37424.656 note=no smoke activation within 5 s before creation; nearest ship 37425 m from origin concealed=0 total=0 origin={'x': 683.1295, 'z': -507.75598}
  178899 -BN- BN_jordi_92T Gearing dist=494.8058 note=- concealed=52003 total=52003 origin={'x': -407.1576, 'z': 368.12592}
  178900 -BN- BN_jordi_92T Gearing dist=8188.511 note=no smoke activation within 5 s before creation; nearest ship 8189 m from origin concealed=0 total=0 origin={'x': 274.19955, 'z': -65.882195}
```

### audit2.py

```
# A. Perspective merge: ledger vs the game's own result, every run
game-level shell+fire ratio (ledger over result): 0-0.8: 0, 0.8-0.95: 27, 0.95-1.05: 93, 1.05-1.25: 201, 1.25-1.6: 14, 1.6-3: 6

runs with ratio over 1.25: 20 (games: 11)
| run | team | ratio | clan ledger | clan result | smokes | smoke dmg | concealed | events per replay | dropped as dup |
|---|---|---|---|---|---|---|---|---|---|
| groups_group-4_round-1_inca-vs-km_g1_inca | INCA | 1.99 | 864,824 | 435,261 | 11 | 229,347 | 205,978 | [871, 860] | 275 |
| groups_group-4_round-1_inca-vs-km_g1_km | KM | 1.99 | 618,968 | 309,816 | 2 | 660 | 660 | [860, 871] | 279 |
| groups_group-4_round-6_inca-vs-bonkz_g1_bonkz | BONKZ | 1.66 | 816,654 | 515,435 | 5 | 180,622 | 180,622 | [560, 669] | 121 |
| groups_group-4_round-6_inca-vs-bonkz_g1_inca | INCA | 1.66 | 676,913 | 383,221 | 2 | 86,878 | 81,317 | [669, 560] | 122 |
| groups_group-4_round-4_hfans-vs-inca_g1_hfans | HFANS | 1.64 | 561,915 | 337,027 | 6 | 23,654 | 13,707 | [568, 411] | 129 |
| groups_group-4_round-4_hfans-vs-inca_g1_inca | INCA | 1.62 | 468,288 | 297,259 | 5 | 57,477 | 55,695 | [411, 568] | 151 |
| groups_group-2_round-4_btlst-vs-mzy_g1_btlst | BTLST | 1.39 | 327,149 | 236,044 | 5 | 15,394 | 12,854 | [540, 461] | 363 |
| groups_group-4_round-3_manba-vs-km_g1_manba | MANBA | 1.37 | 652,991 | 436,171 | 3 | 29,532 | 29,158 | [1134, 686] | 551 |
| groups_group-4_round-3_manba-vs-km_g1_km | KM | 1.37 | 648,330 | 517,080 | 7 | 80,036 | 80,036 | [686, 1134] | 550 |
| groups_group-1_round-4_pn-vs-htdog_g1_pn | PN | 1.36 | 484,295 | 284,116 | 4 | 54,574 | 41,737 | [949, 788] | 576 |
| groups_group-2_round-4_btlst-vs-mzy_g1_mzy | MZY | 1.35 | 505,109 | 371,225 | 3 | 8,405 | 7,900 | [461, 540] | 352 |
| groups_group-1_round-4_pn-vs-htdog_g1_htdog | HTDOG | 1.34 | 687,810 | 583,948 | 6 | 66,199 | 61,290 | [788, 949] | 573 |
| groups_group-2_round-4_kite-vs-rmn_g1_rmn | RMN | 1.33 | 188,854 | 162,939 | 1 | 0 | 0 | [537, 399] | 321 |
| groups_group-2_round-4_kite-vs-rmn_g1_kite | KITE | 1.33 | 476,953 | 338,435 | 1 | 0 | 0 | [399, 537] | 323 |
| groups_group-2_round-6_5d-vs-kite_g1_5d | 5D | 1.31 | 580,484 | 377,751 | 4 | 30,119 | 29,484 | [829, 832] | 761 |
| groups_group-2_round-6_5d-vs-kite_g1_kite | KITE | 1.30 | 487,271 | 439,214 | 2 | 1,280 | 1,000 | [832, 829] | 774 |
| groups_group-1_round-2_uysc-vs-htdog_g1_uysc | UYSC | 1.29 | 186,292 | 155,332 | 4 | 43,634 | 6,280 | [312, 268] | 172 |
| groups_group-3_round-7_sccc2-vs-machx_g1_machx | MACHX | 1.27 | 750,925 | 613,705 | 5 | 27,170 | 11,855 | [1187, 1152] | 960 |
| groups_group-3_round-7_sccc2-vs-machx_g1_sccc2 | SCCC2 | 1.27 | 611,724 | 461,029 | 14 | 101,727 | 92,772 | [1152, 1187] | 960 |
| groups_group-3_round-4_nga-vs-sccc2_g1_nga | NGA | 1.26 | 737,310 | 606,355 | 4 | 20,989 | 19,141 | [1193, 1240] | 1002 |

Clock offset between the two perspectives in the inflated games (modal delta of same attacker/victim/amount shell pairs, 0.25 s bins, deltas up to 30 s):
- groups_group-4_round-1_inca-vs-km_g1_inca: [(8.5, 220), (8.75, 72), (1.5, 56)]
- groups_group-4_round-1_inca-vs-km_g1_km: [(8.5, 216), (8.75, 69), (4.5, 55)]
- groups_group-4_round-6_inca-vs-bonkz_g1_bonkz: [(8.25, 121), (8.0, 102), (1.5, 69)]
- groups_group-4_round-6_inca-vs-bonkz_g1_inca: [(8.25, 121), (8.0, 103), (1.5, 77)]
- groups_group-4_round-4_hfans-vs-inca_g1_hfans: [(6.5, 68), (6.75, 30), (6.25, 22)]
- groups_group-4_round-4_hfans-vs-inca_g1_inca: [(6.5, 66), (6.75, 33), (6.25, 25)]
- groups_group-2_round-4_btlst-vs-mzy_g1_btlst: [(3.0, 18), (2.75, 17), (0.5, 13)]
- groups_group-4_round-3_manba-vs-km_g1_manba: [(3.0, 23), (4.0, 13), (2.75, 13)]
- groups_group-4_round-3_manba-vs-km_g1_km: [(1.5, 56), (8.0, 31), (3.0, 27)]
- groups_group-1_round-4_pn-vs-htdog_g1_pn: [(3.0, 48), (2.75, 44), (2.5, 23)]
- groups_group-2_round-4_btlst-vs-mzy_g1_mzy: [(3.0, 32), (1.5, 21), (2.75, 19)]
- groups_group-1_round-4_pn-vs-htdog_g1_htdog: [(3.0, 71), (2.75, 70), (1.5, 62)]
- groups_group-2_round-4_kite-vs-rmn_g1_rmn: [(4.25, 27), (4.0, 17), (3.75, 12)]
- groups_group-2_round-4_kite-vs-rmn_g1_kite: [(4.25, 33), (1.5, 31), (4.5, 25)]
- groups_group-2_round-6_5d-vs-kite_g1_5d: [(0.5, 24), (8.0, 19), (5.25, 16)]
- groups_group-2_round-6_5d-vs-kite_g1_kite: [(0.5, 19), (8.0, 13), (2.75, 10)]
- groups_group-1_round-2_uysc-vs-htdog_g1_uysc: [(1.5, 14), (4.5, 11), (13.5, 10)]
- groups_group-3_round-7_sccc2-vs-machx_g1_machx: [(1.75, 23), (1.5, 20), (3.5, 15)]
- groups_group-3_round-7_sccc2-vs-machx_g1_sccc2: [(1.5, 47), (4.5, 40), (2.25, 30)]
- groups_group-3_round-4_nga-vs-sccc2_g1_nga: [(1.5, 46), (3.0, 39), (2.75, 25)]

Credit affected: smokes and concealed damage in inflated runs, per clan:
| clan | games | inflated runs | smokes in them | smoke dmg in them | concealed in them | clan concealed total | share |
|---|---|---|---|---|---|---|---|
| INCA | 6 | 3 | 18 | 373,703 | 342,990 | 538,028 | 64% |
| BONKZ | 21 | 1 | 5 | 180,622 | 180,622 | 1,393,272 | 13% |
| SCCC2 | 7 | 1 | 14 | 101,727 | 92,772 | 390,296 | 24% |
| KM | 5 | 2 | 9 | 80,696 | 80,696 | 185,159 | 44% |
| HTDOG | 18 | 1 | 6 | 66,199 | 61,290 | 893,922 | 7% |
| PN | 7 | 1 | 4 | 54,574 | 41,737 | 116,187 | 36% |
| 5D | 10 | 1 | 4 | 30,119 | 29,484 | 208,244 | 14% |
| MANBA | 6 | 1 | 3 | 29,532 | 29,158 | 74,721 | 39% |
| NGA | 7 | 1 | 4 | 20,989 | 19,141 | 134,148 | 14% |
| HFANS | 17 | 1 | 6 | 23,654 | 13,707 | 941,566 | 1% |
| BTLST | 6 | 1 | 5 | 15,394 | 12,854 | 163,108 | 8% |
| MACHX | 14 | 1 | 5 | 27,170 | 11,855 | 786,066 | 2% |
| MZY | 19 | 1 | 3 | 8,405 | 7,900 | 402,441 | 2% |
| UYSC | 7 | 1 | 4 | 43,634 | 6,280 | 159,491 | 4% |
| KITE | 14 | 2 | 3 | 1,280 | 1,000 | 339,795 | 0% |
| RMN | 6 | 1 | 1 | 0 | 0 | 31,236 | 0% |

# B. Smoke credit per shooter vs the game's own shell+fire result, every run
shooter-runs checked: 803; credit above the shooter's own game result: 23
| run | shooter | smoke credit | game result shell+fire | ledger shell+fire | run ratio |
|---|---|---|---|---|---|
| playoffs_winners-bracket_wb-round-1_mzy-vs-machx_g3_machx | MACHX_SPAAAAAAA | 105,982 | 20,384 | 118,411 | 1.10 |
| groups_group-4_round-1_inca-vs-km_g1_inca | INCA_HugoPerC02 | 163,380 | 120,659 | 212,016 | 1.99 |
| playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g1_bonkz | BONKZ_Dyr3 | 52,555 | 11,626 | 52,555 | 1.17 |
| groups_group-1_round-6_pfans-vs-ksc_g1_ksc | KSC__Sait | 103,085 | 74,613 | 118,607 | 1.06 |
| groups_group-4_round-4_manba-vs-epoxy_g1_epoxy | EPOXY_alysa_liu | 85,285 | 60,932 | 100,517 | 1.11 |
| playoffs_winners-bracket_wb-round-2_resin-vs-reeee_g2_reeee | REEEE_Harmonieu | 25,820 | 3,414 | 27,428 | 1.02 |
| groups_group-3_round-7_sccc2-vs-machx_g1_sccc2 | SCCC2_littlefox | 69,019 | 47,375 | 87,360 | 1.27 |
| groups_group-4_round-6_inca-vs-bonkz_g1_bonkz | BONKZ_Bows3r | 95,599 | 74,928 | 127,684 | 1.66 |
| groups_group-2_round-1_rmn-vs-5d_g1_rmn | RMN_Siadant | 26,395 | 7,988 | 26,395 | 1.11 |
| groups_group-3_round-5_bonky-vs-h-sr_g1_bonky | BONKY_Merc85 | 24,995 | 8,364 | 33,173 | 1.03 |
| playoffs_losers-bracket_lb-round-2_mzy-vs-bn_g1_bn | BN_jordi_92T | 49,029 | 33,936 | 51,051 | 1.05 |
| groups_group-3_round-1_h-sr-vs-nga_g1_nga | NGA_HeakyAether | 14,126 | 1,139 | 25,196 | 1.11 |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g2_htdog | HTDOG_Amogussy | 10,996 | 0 | 12,079 | 1.07 |
| playoffs_losers-bracket_lb-round-1_hfans-vs-5d_g1_hfans | HFANS_Flipy47 | 22,465 | 13,367 | 22,861 | 1.14 |
| groups_group-3_round-1_sccc2-vs-bonky_g1_sccc2 | SCCC2_MiqoteGam | 25,514 | 17,115 | 27,197 | 0.97 |
| groups_group-4_round-4_manba-vs-epoxy_g1_manba | MANBA_Catoverfl | 16,353 | 8,432 | 22,954 | 1.11 |
| groups_group-4_round-1_epoxy-vs-hfans_g1_hfans | HFANS_j_i_u_m_i | 54,484 | 50,096 | 60,047 | 1.09 |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g2_vrtus | VRTUS_AgentTang | 78,109 | 73,912 | 84,314 | 1.21 |
| groups_group-4_round-4_hfans-vs-inca_g1_hfans | HFANS_YuanShenG | 13,444 | 9,269 | 18,538 | 1.64 |
| groups_group-3_round-5_bonky-vs-h-sr_g1_h-sr | HSR_VoyagingSta | 31,171 | 27,094 | 32,095 | 1.03 |
| playoffs_losers-bracket_lb-round-1_hfans-vs-5d_g2_hfans | HFANS_j_i_u_m_i | 26,429 | 22,370 | 45,843 | 1.07 |
| groups_group-2_round-3_kite-vs-mzy_g1_kite | KITE_BB_MightyM | 12,782 | 11,149 | 24,068 | 1.11 |
| groups_group-3_round-1_bn-vs-machx_g1_bn | BN_jordi_92T | 2,970 | 1,815 | 3,300 | 1.10 |
in runs with ratio over 1.25: 4 ; in other runs: 19

# C. The 'nearest ship over 600 m' note by ship and smoke type
| ship | smoke type | smokes | with the note | % | median dist of noted | activation matched |
|---|---|---|---|---|---|---|
| Somers | standard | 260 | 1 | 0 | 911 | 0 |
| Daring | cruiser | 200 | 101 | 50 | 627 | 99 |
| Svea | cruiser | 199 | 81 | 41 | 626 | 81 |
| Gearing | standard | 179 | 1 | 1 | 613 | 1 |
| Napoli | exhaust | 147 | 0 | 0 | 0 | 0 |
| Gdansk | standard | 118 | 1 | 1 | 1154 | 0 |
| Harugumo | standard | 100 | 0 | 0 | 0 | 0 |
| Shimakaze | standard | 58 | 2 | 3 | 664 | 2 |
| Z-42 | cruiser | 56 | 38 | 68 | 628 | 38 |
| Jinan | standard | 42 | 0 | 0 | 0 | 0 |
| Grozovoi | standard | 30 | 0 | 0 | 0 | 0 |
| Delny | standard | 22 | 1 | 5 | 1069 | 0 |
| Venezia | exhaust | 21 | 0 | 0 | 0 | 0 |
| C. Colombo | exhaust | 20 | 0 | 0 | 0 | 0 |
| F. Sherman | standard | 4 | 1 | 25 | 667 | 1 |
| Plymouth | standard | 1 | 1 | 100 | 739 | 1 |

Ship mix, original 3 vs others (share of smokes by smoke type):
- original 3: standard 87%, exhaust 7%, cruiser 6%
- others: standard 51%, cruiser 33%, exhaust 15%, crawling 1%

Distance of the attributed ship for unflagged smokes, by smoke type (median, 90th pct):
- standard: n 790, median 484 m, p90 519 m, max 597 m
- cruiser: n 220, median 137 m, p90 491 m, max 596 m
- exhaust: n 196, median 170 m, p90 204 m, max 297 m
- crawling: n 15, median 362 m, p90 483 m, max 491 m
Same for the noted smokes (600 to 2000 m):
- standard: n 8, median 739 m, p90 1154 m, max 1154 m
- cruiser: n 220, median 627 m, p90 656 m, max 834 m

Radius of the smoke by type (base_radius, distinct): {'standard': ['15.00', '20.00'], 'cruiser': ['20.00'], 'exhaust': ['15.00', '17.00', '30.00'], 'crawling': ['15.00']}

# D. 'no activation within 5 s' smokes
count 103; with a clock: 0; created clock present: 103
by team: {'H-SR': 11, '-BN-': 11, 'EPOXY': 10, 'MZY': 8, 'KM': 7, 'HTDOG': 6, 'KSC': 5, 'HFANS': 5, 'BONKZ': 5, 'MACH': 4, 'RESIN': 4, 'BONKY': 4, 'INCA': 3, 'KITED': 3, 'NGA': 3, 'PFANS': 3, 'SCCC2': 2, 'KITE': 2, 'REEEE': 2, 'PN': 2, 'VRTUS': 2, 'RSR': 1}
by ship: {'Somers': 23, 'Harugumo': 14, 'Napoli': 13, 'Gearing': 12, 'Svea': 8, 'Daring': 8, 'Delny': 4, 'Smolensk': 4, 'Grozovoi': 3, 'Gdansk': 3, 'Fuyutsuki': 2, 'Venezia': 2}
attributed to the recorder of the primary replay: 0 of 103
smokes attributed to a recorder: 0, of which without activation: 0
created clock of the no-activation smokes (first 5 minutes vs later): Counter({'later': 86, 'under 5 min': 17})
damage on them: concealed 901,451 total 926,464
```
