# STEP 2c: re-run after the method fixes F1 to F4

Batch `output/20261116-161621`: 341 runs, 0 failures, 1,547 smokes, 103 flagged, 1,252 s wall time (frames on, no clips). The standing check is `smoke/tools/sanity.py` (its full output is in the appendix); the before/after figures compare with the STEP 2 batch `output/20261116-132014`. The round 6 reference is `output/20261104-180332`.

Commits, in order: F1 offset search to 12 s with the far-peak guard (829494ff); F2 owner note only without an activation (12013e21); F3 inferred owner and one-sided runs (ef838764); F4 torpedo classification (017ed169, corrected in 4b79fc17); hub mockups; the sanity script; DESIGN.md. The Rust tests pass after each, including the golden Grand Final snapshot. An intermediate batch `output/20261116-154549` (F4 before its correction) stays on disk and is not committed.

## F4 needed a second pass

The first re-run still classified almost nothing as torpedo. Tracing one game showed the dead-reckoned torpedo 135 m from the victim at the hit, but the replay view keeps every torpedo until the end of the battle, so the "torpedo left the view" condition never held. The condition is gone; a hit is a torpedo when the attacker has a torpedo 1 to 150 s into its run whose dead-reckoned position is within 400 m of the victim. The original matcher compared world units with meters and matched 119 events in the whole batch; the corrected one matches 3,641.

| | STEP 2 batch | after the fixes |
|---|---|---|
| torpedo events / damage | 119 / 0.2 M | 3,641 / 27.7 M |
| flood events / damage | 89 / 0.03 M | 5,181 / 2.6 M |
| unknown damage | 34.3 M | 13.0 M |
| shell damage | 279.6 M | 268.0 M |
| shooters credited above their own shell-plus-fire result | 23 (excess 410k, 2.5% of credit) | 8 (excess 65k, 0.4%) |

## 1. Ledger reconciliation, every run

Ledger shell-plus-fire over the game's own result, per run (341 runs, every one with a result):

| band | runs |
|---|---|
| under 0.90 | 14 |
| 0.90 to 0.98 | 54 |
| 0.98 to 1.02 | 56 |
| 1.02 to 1.10 | 119 |
| 1.10 to 1.25 | 92 |
| 1.25 to 1.60 | 6 |
| over 1.60 | 0 |

Median 1.056, mean 1.052 (STEP 2 batch: median 1.093; 20 runs over 1.25, 6 over 1.6). Runs outside 2%: 285 (217 over, 68 under); the full list with each run's clock offset is in the appendix, section 1. No merged replay fell back to offset zero: every pair found a trusted offset, including the three INCA games at +8.5, +8.25 and +6.5 s, which now reconcile at 1.16, 1.22 and 1.18.

The six runs still over 1.25 are three games: BTLST vs MZY (1.34 / 1.26, offset 1.75 s), PN vs HTDOG (1.30 both sides, offset 4.0 s) and MANBA vs KM (1.28 / 1.27, offset 2.0 s). Their offset bins hold 100 to 192 of 700 to 3,000 pairs, which is a flat spread, so the two replays' clocks drift within the game and part of the hits stay unmatched. Backlog.

The whole field sits about 5% over the game's result (median 1.056) with a long tail to 1.25. This is the known behaviour since round 3 (then 1.05 on three clans), not something the fixes introduced; the cause is not established (candidates: secondary-battery hits the result counts elsewhere, or partial drift). The 2% test is the standing check; what it lists today is this systematic band plus the three drift games.

## 2. The original 217 rows against round 6, column by column

Same 217 rows, none added or lost; 164 reference columns plus the new `one_sided` column (false on all 217). 15 rows changed in a non-volatile field; the other 202 are identical in every column. Three causes:

**F2, 5 rows: flag cleared, no value changed.** The owner was confirmed by an activation in all five.

| smoke | who | game | old note |
|---|---|---|---|
| 87568 | RESIN_thepregna, Svea | Group 4 R4 vs KM (Land of Fire) 14:16 | nearest ship 619 m |
| 87591 | RESIN_thepregna, Svea | same game, 12:56 | nearest ship 834 m |
| 87611 | RESIN_thepregna, Svea | same game, 09:46 | nearest ship 636 m |
| 190358 | RESIN_thepregna, Svea | WB R2 vs REEEE g1 (Hotspot) 16:39 | nearest ship 673 m |
| 3191 | HSR_Yuzuriha_Ou, Svea | WB R3 vs EPOXY g2 (Sea of Fortune) 09:40 | nearest ship 630 m |

**F4, 8 rows: torpedo hits no longer credited as shells.** Columns that move: damage_in_smoke or damage_behind_smoke (and the smoker/ally split), smoke_damage_total, smoke_damage_concealed, damage_shell, salvos_credited, and where it applies damage_fire and dd_damage.

| smoke | who | game | concealed before | after | note |
|---|---|---|---|---|---|
| 159292 | RESIN_Maddog242, Harugumo | WB R4 vs H-SR g3 (Land of Fire) 12:17 | 60,967 | 36,200 | the round 6 Most Selfish Smoke winner; its owner's torpedo hits were counted as shells |
| 214885 | HSR_Mixic37, Harugumo | Group 3 R7 vs MACH (Sea of Fortune) 14:58 | 38,254 | 34,078 | also a fire tick train that followed a torpedo (flood now) |
| 90086 | HSR_YuriSayuki, Harugumo | GF g2 vs RESIN (Hotspot) 17:12 | 39,624 | 37,911 | |
| 166114 | RESIN_eagle_lan, Gdansk | LB R6 vs BONKZ g1 (Sleeping Giant) 06:38 | 26,576 | 23,037 | |
| 178680 | HSR_Yamiyonohik, Somers | Group 3 R6 vs KITED (Sleeping Giant) | 22,726 | 21,662 | |
| 51294 | HSR_Yamiyonohik, Somers | Group 3 R5 vs BONKY (Mountain Range) 14:53 | 11,721 | 10,087 | dd_damage moves the same way |
| 85026 | HSR_YuriSayuki, Gdansk | WB R3 vs EPOXY g3 (Hotspot) 13:02 | 20,166 | 19,176 | drops under 20,000, so the `damage` purpose tag and damage_20k go |
| 178679 | HSR_Arona_daisu, Harugumo | Group 3 R6 vs KITED (Sleeping Giant) 12:36 | unchanged | | only damage_in_smoke_enemy moved (4,630 to 3,970), an enemy's torpedo inside our smoke, never counted in totals |

**F4 the other way, 1 row: credit up.** 190362, RESIN_thepregna's Svea, WB R2 vs REEEE g1 (Hotspot) 12:53: concealed 12,977 to 16,804. The old matcher's rare fits were false ones: in that game it called 24 of thepregna's events torpedoes and 25 floods, and those shots went uncredited. The game's result says every point of thepregna's 88,203 was shells and fire; the ledger now reads 79,626 shell-plus-fire for the ship instead of 57,203.

**F4 knock-on, 1 row: a smoke death appears.** 195445, PN_FiftyForATwe's Harugumo, Group 1 R2 vs KSC (Loop) 06:58: smoke_deaths 0 to 1. The ship's shots from behind the smoke are now credited shells, so it counts as concealed by the smoke, and it sank at 05:06 while the smoke stood. Round 6 saw those shots as torpedoes and did not count the ship as concealed.

No row changed from F1 (the three original clans' games had offsets within the old 6 s) or F3. Every clan-level figure on the published scouting report that uses concealed damage moves by these 8 rows: H-SR concealed per game 67,832 to 67,397, RESIN 51,866 to 50,846, PN unchanged.

## 3. INCA, KM, BONKZ, HFANS before and after

Concealed smoke damage per game:

| clan | games | before | after | change | cause |
|---|---|---|---|---|---|
| INCA | 6 | 89,671 | 67,990 | -24% | F1: the three doubled games now merge (offsets 8.5, 8.25, 6.5 s) |
| KM | 5 | 37,032 | 31,731 | -14% | F1 (the INCA game) and F4 |
| BONKZ | 21 | 66,346 | 61,664 | -7% | F1 (the INCA game) and F4 |
| HFANS | 17 | 55,386 | 51,350 | -7% | F1 (the INCA game) and F4 |

For the whole field: -BN- 90,868 to 87,786 (F4 only; still first), H-SR 67,397, KSC 64,443, VRTUS 63,858. Largest other moves are F4 on torpedo-heavy clans: RMN 5,206 to 2,216 (-57%: the RMN_Siadant case was a torpedo), MANBA 12,454 to 8,021 (-36%), SCCC2 -12%, MACHX -11%, MACH -9%. Nine clans did not move at all. The full table is in the appendix, part 2 of the compare output.

## 4. Smoke of the Tournament candidates before and after

| # | before | after |
|---|---|---|
| 1 | BN_jordi_92T, Gearing, -BN- vs SCCC2 (Sleeping Giant) 16:25, 97,327 | same, 97,327 |
| 2 | PFANS_Mugu_9, Harugumo, PFANS vs KSE (Hotspot) 07:12, 96,006 | same, 94,024 |
| 3 | INCA_run_for_yo, Gearing, INCA vs KM (Hotspot) 15:06, 94,628 | HSR_Yamiyonohik, Somers, H-SR vs -BN- (Okinawa) 13:36, 90,686 |
| 4 | HSR_Yamiyonohik, 90,686 | BN_jordi_92T, Somers, LB R1 vs KSC g2 (Hotspot) 14:02, 89,662 |
| 5 | BN_jordi_92T, Somers, 89,662 | EPOXY_Your_SAT_, Somers, EPOXY vs MANBA (Land of Fire) 12:07, 84,328 |
| 6 | BONKZ_CheshireZ, Gearing, BONKZ vs INCA (Sleeping Giant) 17:29, 85,022 | RESIN_Big_Boy69, Somers, GF g2 (Hotspot) 17:26, 80,375 |
| 7 | EPOXY_Your_SAT_, 84,328 | EPOXY_Your_SAT_, Shimakaze, EPOXY vs BONKZ (Okinawa) 10:48, 77,031 |
| 8 | BN_jordi_92T, Somers, WB R1 vs KITE g1, 83,433 | BONKY_Lalic, Somers, BONKY vs NGA (Sea of Fortune) 17:41, 74,771 |

The two doubled-game smokes (INCA 94,628 and BONKZ 85,022) leave the top 8; the leader does not change. Round 6's winner (HSR_Yamiyonohik, 90,686) is third in the full field. Awards are computed at site build; the round 6 Most Selfish Smoke winner lost 40% of its damage (section 2) and may move.

## 5. Flags

326 of 1,547 (21.1%) to 103 (6.7%): no activation within 5 s 99 (71 of them also minimap-only positions), nearest ship over 600 m without an activation 5, owner inferred 4 (the KSC smokes of the one-sided game, now produced by the batch itself; `recover_one_sided.py` is no longer needed and stays as history). Dedupe unchanged: 1,538 smokes seen by both runs counted once plus 9 one-sided; both runs of every two-replay game saw the same count.

## 6. Backlog

- F5: roster activation counter double counts uses seen by both replays more than 1 s apart (87 team-games off by more than one; unchanged).
- Clock drift within a game (BTLST vs MZY, PN vs HTDOG, MANBA vs KM at 1.25 to 1.34).
- The systematic 5% ledger excess over the game result.
- Compare mode on the Maps page (from the STEP 3 answers).

## 7. Hub mockups

Three static pages in `smoke/mockups/` (card grid; featured hero plus list; by tournament with a side rail), delivered as HTML. Screenshots were not possible because the browser pane was hidden; they can be taken on request.

## Appendix A: sanity.py output

```
# 1. Ledger reconciliation (shell plus fire, ledger over the game's own result)
runs: 341; with a game result: 341
ratio bands: 0-0.9: 14, 0.9-0.98: 54, 0.98-1.02: 56, 1.02-1.1: 119, 1.1-1.25: 92, 1.25-1.6: 6, 1.6-9: 0
median ratio 1.056; mean 1.052
runs outside 2%: 285 (over: 217, under: 68)
merged replays whose offset estimate fell back to offset zero: 0

| run | ratio | perspective offsets |
|---|---|---|
| groups_group-2_round-4_btlst-vs-mzy_g1_btlst | 1.344 | offset +1.75 s (100/728 pairs) |
| groups_group-1_round-4_pn-vs-htdog_g1_htdog | 1.303 | offset +4.00 s (111/1564 pairs) |
| groups_group-1_round-4_pn-vs-htdog_g1_pn | 1.300 | offset -4.00 s (129/2986 pairs) |
| groups_group-2_round-4_btlst-vs-mzy_g1_mzy | 1.298 | offset -1.75 s (96/696 pairs) |
| groups_group-4_round-3_manba-vs-km_g1_manba | 1.275 | offset -2.00 s (192/2621 pairs) |
| groups_group-4_round-3_manba-vs-km_g1_km | 1.272 | offset +2.00 s (147/981 pairs) |
| groups_group-3_round-7_sccc2-vs-machx_g1_machx | 1.250 | offset -2.00 s (162/2739 pairs) |
| groups_group-3_round-7_sccc2-vs-machx_g1_sccc2 | 1.243 | offset +2.00 s (147/1564 pairs) |
| groups_group-4_round-7_inca-vs-manba_g1_inca | 1.231 | offset +3.75 s (137/1765 pairs) |
| groups_group-4_round-7_inca-vs-manba_g1_manba | 1.228 | offset -3.75 s (128/1090 pairs) |
| groups_group-1_round-4_rsr-vs-uysc_g1_uysc | 1.221 | offset +5.50 s (80/661 pairs) |
| groups_group-1_round-4_rsr-vs-uysc_g1_rsr | 1.218 | offset -5.50 s (84/617 pairs) |
| playoffs_winners-bracket_wb-round-3_bonkz-vs-resin_g3_resin | 1.214 | offset -0.75 s (44/809 pairs) |
| playoffs_winners-bracket_wb-round-3_bonkz-vs-resin_g3_bonkz | 1.212 | offset +0.75 s (58/899 pairs) |
| groups_group-3_round-4_nga-vs-sccc2_g1_nga | 1.211 | offset +4.00 s (208/1738 pairs) |
| groups_group-3_round-4_nga-vs-sccc2_g1_sccc2 | 1.207 | offset -4.00 s (225/2468 pairs) |
| groups_group-2_round-4_kite-vs-rmn_g1_rmn | 1.203 | offset +3.25 s (75/1142 pairs) |
| playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g2_bn | 1.197 | offset +2.75 s (61/744 pairs) |
| groups_group-2_round-1_btlst-vs-reeee_g1_btlst | 1.193 | offset +1.25 s (103/834 pairs) |
| groups_group-2_round-4_kite-vs-rmn_g1_kite | 1.188 | offset -3.25 s (69/695 pairs) |
| groups_group-1_round-7_kse-vs-rsr_g1_rsr | 1.185 | offset -1.00 s (268/1200 pairs) |
| groups_group-1_round-7_kse-vs-rsr_g1_kse | 1.182 | offset +1.00 s (265/1174 pairs) |
| groups_group-1_round-1_vrtus-vs-htdog_g1_vrtus | 1.175 | offset -2.25 s (133/1066 pairs) |
| groups_group-2_round-1_btlst-vs-reeee_g1_reeee | 1.173 | offset -1.25 s (147/2435 pairs) |
| groups_group-1_round-1_vrtus-vs-htdog_g1_htdog | 1.171 | offset +2.25 s (140/1332 pairs) |
| playoffs_losers-bracket_lb-round-2_reeee-vs-hfans_g2_hfans | 1.170 | offset -0.25 s (82/1582 pairs) |
| playoffs_losers-bracket_lb-round-2_reeee-vs-hfans_g2_reeee | 1.169 | offset +0.25 s (68/1063 pairs) |
| groups_group-3_round-6_nga-vs-machx_g1_nga | 1.168 | offset +3.00 s (253/991 pairs) |
| playoffs_winners-bracket_wb-round-2_kite-vs-epoxy_g1_kite | 1.168 | offset -0.75 s (108/1986 pairs) |
| groups_group-3_round-4_mach-vs-bn_g1_mach | 1.164 | offset +1.25 s (145/1519 pairs) |
| playoffs_winners-bracket_wb-round-2_resin-vs-reeee_g1_reeee | 1.163 | offset +1.25 s (88/2166 pairs) |
| playoffs_winners-bracket_wb-round-2_kite-vs-epoxy_g1_epoxy | 1.162 | offset +0.50 s (84/933 pairs) |
| groups_group-3_round-4_mach-vs-bn_g1_bn | 1.162 | offset -1.25 s (174/3607 pairs) |
| groups_group-4_round-2_resin-vs-manba_g1_resin | 1.161 | offset -0.75 s (208/1119 pairs) |
| groups_group-4_round-2_resin-vs-manba_g1_manba | 1.160 | offset +0.75 s (215/1637 pairs) |
| groups_group-3_round-2_mach-vs-nga_g1_mach | 1.159 | offset -4.25 s (151/1288 pairs) |
| playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g2_ksc | 1.157 | offset -2.75 s (69/2028 pairs) |
| playoffs_winners-bracket_wb-round-2_resin-vs-reeee_g1_resin | 1.157 | offset -1.25 s (62/550 pairs) |
| groups_group-1_round-6_vrtus-vs-uysc_g1_vrtus | 1.155 | offset -5.00 s (132/1225 pairs) |
| playoffs_losers-bracket_lb-round-2_mzy-vs-bn_g2_bn | 1.154 | offset +0.75 s (180/2626 pairs) |
| groups_group-2_round-6_5d-vs-kite_g1_5d | 1.153 | offset -0.25 s (240/1242 pairs) |
| groups_group-3_round-6_nga-vs-machx_g1_machx | 1.152 | offset -3.00 s (253/970 pairs) |
| groups_group-3_round-2_mach-vs-nga_g1_nga | 1.152 | offset +4.25 s (168/2579 pairs) |
| groups_group-3_round-4_kited-vs-bonky_g1_bonky | 1.149 | offset -4.00 s (200/767 pairs) |
| playoffs_losers-bracket_lb-round-2_mzy-vs-bn_g2_mzy | 1.148 | offset -0.75 s (148/1635 pairs) |
| groups_group-4_round-1_inca-vs-km_g1_inca | 1.146 | offset +8.50 s (240/1286 pairs) |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g3_htdog | 1.146 | offset -2.75 s (131/2639 pairs) |
| groups_group-4_round-7_km-vs-hfans_g1_hfans | 1.146 | offset +1.50 s (180/1126 pairs) |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g3_hfans | 1.144 | offset +2.75 s (128/2516 pairs) |
| groups_group-2_round-3_btlst-vs-5d_g1_btlst | 1.143 | offset +1.00 s (140/819 pairs) |
| playoffs_losers-bracket_lb-round-3_hfans-vs-mzy_g1_hfans | 1.143 | offset +5.75 s (111/1199 pairs) |
| groups_group-4_round-7_km-vs-hfans_g1_km | 1.141 | offset -1.50 s (177/974 pairs) |
| groups_group-4_round-1_inca-vs-km_g1_km | 1.141 | offset -8.50 s (246/1094 pairs) |
| playoffs_winners-bracket_wb-round-1_epoxy-vs-ksc_g2_epoxy | 1.141 | offset +0.25 s (98/2841 pairs) |
| groups_group-3_round-1_kited-vs-mach_g1_kited | 1.140 | offset +0.75 s (116/2886 pairs) |
| groups_group-2_round-7_mzy-vs-5d_g1_5d | 1.140 | offset -0.75 s (190/1385 pairs) |
| groups_group-3_round-1_kited-vs-mach_g1_mach | 1.140 | offset -0.75 s (81/1020 pairs) |
| groups_group-2_round-6_5d-vs-kite_g1_kite | 1.139 | offset +0.25 s (242/1238 pairs) |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g2_vrtus | 1.138 | offset +1.00 s (72/770 pairs) |
| playoffs_winners-bracket_wb-round-1_resin-vs-pfans_g1_pfans | 1.138 | offset +0.50 s (42/497 pairs) |
| playoffs_losers-bracket_lb-round-3_hfans-vs-mzy_g1_mzy | 1.137 | offset -5.75 s (112/1188 pairs) |
| groups_group-1_round-6_vrtus-vs-uysc_g1_uysc | 1.137 | offset +5.00 s (115/731 pairs) |
| groups_group-2_round-7_mzy-vs-5d_g1_mzy | 1.133 | offset +0.75 s (189/1399 pairs) |
| groups_group-2_round-2_btlst-vs-kite_g1_btlst | 1.133 | offset +2.00 s (81/732 pairs) |
| groups_group-2_round-3_btlst-vs-5d_g1_5d | 1.128 | offset -1.00 s (135/797 pairs) |
| groups_group-3_round-5_kited-vs-sccc2_g1_kited | 1.127 | offset +0.50 s (218/2208 pairs) |
| playoffs_winners-bracket_wb-round-1_epoxy-vs-ksc_g2_ksc | 1.126 | offset -0.25 s (43/577 pairs) |
| groups_group-1_round-2_uysc-vs-htdog_g1_uysc | 1.126 | offset +3.00 s (35/834 pairs) |
| playoffs_winners-bracket_wb-round-1_resin-vs-pfans_g1_resin | 1.125 | offset -0.50 s (52/686 pairs) |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g2_machx | 1.125 | offset -1.00 s (74/1756 pairs) |
| groups_group-3_round-5_kited-vs-sccc2_g1_sccc2 | 1.125 | offset -0.50 s (218/2339 pairs) |
| groups_group-3_round-7_h-sr-vs-mach_g1_h-sr | 1.120 | offset -0.50 s (143/1336 pairs) |
| groups_group-2_round-5_kite-vs-reeee_g1_reeee | 1.119 | offset +2.00 s (186/3875 pairs) |
| playoffs_winners-bracket_wb-round-2_h-sr-vs-htdog_g1_h-sr | 1.118 | offset -1.50 s (196/2751 pairs) |
| playoffs_winners-bracket_wb-round-1_vrtus-vs-bonkz_g1_bonkz | 1.118 | offset +1.50 s (51/964 pairs) |
| groups_group-3_round-7_h-sr-vs-mach_g1_mach | 1.116 | offset +0.50 s (138/1139 pairs) |
| groups_group-3_round-4_machx-vs-h-sr_g1_h-sr | 1.116 | offset -0.50 s (49/1092 pairs) |
| playoffs_grand-final_gf-round-1_h-sr-vs-resin_g3_h-sr | 1.116 | offset +0.00 s (84/1151 pairs) |
| playoffs_winners-bracket_wb-round-1_vrtus-vs-bonkz_g1_vrtus | 1.115 | offset -1.50 s (76/2363 pairs) |
| playoffs_winners-bracket_wb-round-2_h-sr-vs-htdog_g1_htdog | 1.114 | offset +1.50 s (181/1684 pairs) |
| groups_group-3_round-4_machx-vs-h-sr_g1_machx | 1.114 | offset +0.50 s (52/844 pairs) |
| groups_group-4_round-5_resin-vs-inca_g1_inca | 1.114 | offset +5.75 s (229/1242 pairs) |
| groups_group-2_round-2_btlst-vs-kite_g1_kite | 1.112 | offset -2.00 s (77/445 pairs) |
| groups_group-3_round-1_h-sr-vs-nga_g1_h-sr | 1.111 | offset -4.25 s (33/512 pairs) |
| groups_group-1_round-7_pn-vs-uysc_g1_pn | 1.111 | offset -4.50 s (224/969 pairs) |
| groups_group-3_round-6_sccc2-vs-bn_g1_sccc2 | 1.110 | offset -0.25 s (210/2192 pairs) |
| groups_group-3_round-6_sccc2-vs-bn_g1_bn | 1.110 | offset +0.25 s (201/1618 pairs) |
| playoffs_losers-bracket_lb-round-4_epoxy-vs-mzy_g1_epoxy | 1.109 | offset -1.25 s (107/1100 pairs) |
| groups_group-4_round-2_bonkz-vs-km_g1_km | 1.107 | offset +0.50 s (62/1555 pairs) |
| groups_group-2_round-5_kite-vs-reeee_g1_kite | 1.105 | offset -2.00 s (114/699 pairs) |
| groups_group-3_round-4_kited-vs-bonky_g1_kited | 1.104 | offset +4.00 s (200/1197 pairs) |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g3_pfans | 1.104 | offset -2.00 s (54/887 pairs) |
| groups_group-1_round-2_rsr-vs-pfans_g1_rsr | 1.103 | offset +0.00 s (61/412 pairs) |
| groups_group-3_round-1_h-sr-vs-nga_g1_nga | 1.102 | offset +4.25 s (47/1092 pairs) |
| playoffs_winners-bracket_wb-round-1_epoxy-vs-ksc_g1_ksc | 1.102 | offset +0.25 s (101/2539 pairs) |
| groups_group-1_round-6_pn-vs-kse_g1_kse | 1.101 | offset +1.25 s (167/1151 pairs) |
| groups_group-1_round-2_rsr-vs-pfans_g1_pfans | 1.101 | offset +0.00 s (73/943 pairs) |
| groups_group-4_round-1_bonkz-vs-manba_g1_bonkz | 1.100 | offset -0.50 s (80/1739 pairs) |
| playoffs_winners-bracket_wb-round-1_h-sr-vs-5d_g1_5d | 1.100 | offset +1.00 s (57/922 pairs) |
| groups_group-1_round-6_pn-vs-kse_g1_pn | 1.097 | offset -1.25 s (171/1100 pairs) |
| playoffs_winners-bracket_wb-round-1_epoxy-vs-ksc_g1_epoxy | 1.097 | offset -0.25 s (87/1408 pairs) |
| playoffs_winners-bracket_wb-round-2_kite-vs-epoxy_g2_epoxy | 1.095 | offset -0.25 s (84/445 pairs) |
| groups_group-1_round-7_pn-vs-uysc_g1_uysc | 1.094 | offset +4.50 s (221/882 pairs) |
| groups_group-4_round-1_bonkz-vs-manba_g1_manba | 1.093 | offset +0.50 s (74/1907 pairs) |
| playoffs_losers-bracket_lb-round-4_epoxy-vs-mzy_g1_mzy | 1.093 | offset +1.25 s (100/1619 pairs) |
| playoffs_winners-bracket_wb-round-2_kite-vs-epoxy_g2_kite | 1.092 | offset +0.25 s (93/1291 pairs) |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g3_kited | 1.091 | offset +2.00 s (68/1035 pairs) |
| groups_group-2_round-7_rmn-vs-reeee_g1_rmn | 1.091 | offset +1.00 s (147/680 pairs) |
| playoffs_winners-bracket_wb-round-1_kite-vs-bn_g1_kite | 1.090 | offset -2.25 s (135/682 pairs) |
| playoffs_winners-bracket_wb-round-1_h-sr-vs-5d_g1_h-sr | 1.090 | offset -1.00 s (53/921 pairs) |
| groups_group-1_round-3_uysc-vs-kse_g1_uysc | 1.088 | offset +4.00 s (121/712 pairs) |
| groups_group-1_round-3_uysc-vs-kse_g1_kse | 1.088 | offset -4.00 s (121/581 pairs) |
| playoffs_winners-bracket_wb-round-1_kite-vs-bn_g1_bn | 1.088 | offset +2.25 s (150/2011 pairs) |
| playoffs_winners-bracket_wb-round-4_resin-vs-h-sr_g4_h-sr | 1.088 | offset -1.00 s (206/1547 pairs) |
| groups_group-2_round-2_reeee-vs-5d_g1_5d | 1.086 | offset -0.50 s (154/611 pairs) |
| groups_group-4_round-4_resin-vs-km_g1_km | 1.086 | offset +2.75 s (245/1180 pairs) |
| groups_group-2_round-7_rmn-vs-reeee_g1_reeee | 1.086 | offset -1.00 s (146/559 pairs) |
| groups_group-2_round-2_reeee-vs-5d_g1_reeee | 1.085 | offset +0.50 s (162/847 pairs) |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g1_kited | 1.084 | offset +2.75 s (122/1152 pairs) |
| playoffs_winners-bracket_wb-round-4_resin-vs-h-sr_g4_resin | 1.084 | offset +1.00 s (169/561 pairs) |
| playoffs_grand-final_gf-round-1_h-sr-vs-resin_g3_resin | 1.084 | offset -0.75 s (92/1187 pairs) |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g2_kited | 1.084 | offset +2.00 s (102/1973 pairs) |
| playoffs_losers-bracket_lb-round-6_resin-vs-bonkz_g3_resin | 1.083 | offset +0.50 s (149/2234 pairs) |
| playoffs_winners-bracket_wb-round-2_bonkz-vs-mzy_g2_mzy | 1.082 | offset -0.75 s (97/1745 pairs) |
| playoffs_losers-bracket_lb-round-5_epoxy-vs-bonkz_g1_epoxy | 1.081 | offset +0.50 s (130/1275 pairs) |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g2_pfans | 1.081 | offset -2.00 s (129/2451 pairs) |
| playoffs_losers-bracket_lb-round-5_epoxy-vs-bonkz_g1_bonkz | 1.079 | offset -0.50 s (132/1260 pairs) |
| playoffs_winners-bracket_wb-round-2_bonkz-vs-mzy_g2_bonkz | 1.079 | offset +0.75 s (114/1343 pairs) |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g2_hfans | 1.078 | offset -1.25 s (125/1304 pairs) |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g1_pfans | 1.077 | offset -2.75 s (120/1130 pairs) |
| groups_group-4_round-7_resin-vs-bonkz_g1_resin | 1.077 | offset -1.25 s (150/1649 pairs) |
| groups_group-4_round-4_resin-vs-km_g1_resin | 1.076 | offset -2.75 s (247/1099 pairs) |
| groups_group-4_round-2_bonkz-vs-km_g1_bonkz | 1.075 | offset -0.25 s (96/2798 pairs) |
| groups_group-4_round-4_manba-vs-epoxy_g1_manba | 1.075 | offset +0.00 s (85/707 pairs) |
| groups_group-2_round-4_5d-vs-ogf_g1_ogf | 1.074 | offset -0.25 s (212/1001 pairs) |
| groups_group-4_round-3_bonkz-vs-epoxy_g1_bonkz | 1.073 | offset +0.75 s (123/1389 pairs) |
| groups_group-4_round-3_bonkz-vs-epoxy_g1_epoxy | 1.071 | offset -0.75 s (130/1238 pairs) |
| playoffs_losers-bracket_lb-round-2_htdog-vs-kited_g2_htdog | 1.071 | offset +0.75 s (105/1215 pairs) |
| groups_group-4_round-4_manba-vs-epoxy_g1_epoxy | 1.070 | offset +0.00 s (85/761 pairs) |
| playoffs_losers-bracket_lb-round-2_htdog-vs-kited_g1_kited | 1.070 | offset +0.00 s (98/961 pairs) |
| groups_group-1_round-4_pfans-vs-vrtus_g1_pfans | 1.070 | offset +0.25 s (76/1960 pairs) |
| groups_group-4_round-7_resin-vs-bonkz_g1_bonkz | 1.069 | offset +1.25 s (142/1382 pairs) |
| groups_group-1_round-2_uysc-vs-htdog_g1_htdog | 1.068 | offset -3.50 s (27/567 pairs) |
| playoffs_losers-bracket_lb-round-3_hfans-vs-mzy_g3_mzy | 1.068 | offset +0.25 s (206/1479 pairs) |
| groups_group-3_round-6_bonky-vs-mach_g1_bonky | 1.067 | offset -1.25 s (102/744 pairs) |
| playoffs_losers-bracket_lb-round-2_htdog-vs-kited_g2_kited | 1.066 | offset -0.75 s (137/2624 pairs) |
| playoffs_winners-bracket_wb-round-3_epoxy-vs-h-sr_g1_epoxy | 1.066 | offset -0.75 s (83/1107 pairs) |
| groups_group-2_round-4_5d-vs-ogf_g1_5d | 1.066 | offset +0.25 s (213/1045 pairs) |
| groups_group-3_round-6_bonky-vs-mach_g1_mach | 1.066 | offset +1.25 s (106/938 pairs) |
| playoffs_winners-bracket_wb-round-3_epoxy-vs-h-sr_g1_h-sr | 1.066 | offset +0.75 s (99/2763 pairs) |
| groups_group-2_round-3_kite-vs-mzy_g1_mzy | 1.065 | offset +1.00 s (169/1183 pairs) |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g2_htdog | 1.065 | offset +1.25 s (117/914 pairs) |
| playoffs_losers-bracket_lb-round-2_htdog-vs-kited_g1_htdog | 1.065 | offset +0.00 s (84/709 pairs) |
| groups_group-1_round-4_pfans-vs-vrtus_g1_vrtus | 1.065 | offset +0.00 s (53/378 pairs) |
| playoffs_winners-bracket_wb-round-1_vrtus-vs-bonkz_g2_vrtus | 1.064 | offset -0.50 s (49/424 pairs) |
| groups_group-4_round-5_hfans-vs-bonkz_g1_hfans | 1.062 | offset +1.75 s (125/1705 pairs) |
| playoffs_losers-bracket_lb-round-4_epoxy-vs-mzy_g3_mzy | 1.061 | offset +0.50 s (199/1041 pairs) |
| groups_group-3_round-3_kited-vs-nga_g1_kited | 1.061 | offset -5.50 s (266/820 pairs) |
| groups_group-3_round-3_kited-vs-nga_g1_nga | 1.060 | offset +5.50 s (266/850 pairs) |
| playoffs_losers-bracket_lb-round-3_hfans-vs-mzy_g3_hfans | 1.060 | offset -0.25 s (196/989 pairs) |
| playoffs_losers-bracket_lb-round-3_hfans-vs-mzy_g2_mzy | 1.060 | offset -4.00 s (302/1641 pairs) |
| groups_group-3_round-6_kited-vs-h-sr_g1_kited | 1.060 | offset +1.25 s (87/754 pairs) |
| playoffs_losers-bracket_lb-round-3_hfans-vs-mzy_g2_hfans | 1.060 | offset +4.00 s (302/1606 pairs) |
| groups_group-2_round-2_rmn-vs-ogf_g1_rmn | 1.059 | offset +0.75 s (265/1077 pairs) |
| groups_group-1_round-1_uysc-vs-ksc_g1_ksc | 1.058 | offset -0.25 s (83/896 pairs) |
| groups_group-3_round-5_nga-vs-bn_g1_nga | 1.058 | offset +2.25 s (79/505 pairs) |
| groups_group-2_round-2_rmn-vs-ogf_g1_ogf | 1.058 | offset -0.75 s (257/938 pairs) |
| groups_group-2_round-3_kite-vs-mzy_g1_kite | 1.057 | offset -1.00 s (158/716 pairs) |
| playoffs_losers-bracket_lb-round-4_epoxy-vs-mzy_g3_epoxy | 1.057 | offset -0.50 s (192/745 pairs) |
| groups_group-3_round-5_nga-vs-bn_g1_bn | 1.056 | offset -2.25 s (71/366 pairs) |
| playoffs_winners-bracket_wb-round-3_epoxy-vs-h-sr_g2_h-sr | 1.056 | offset -0.50 s (170/1253 pairs) |
| playoffs_winners-bracket_wb-round-3_epoxy-vs-h-sr_g2_epoxy | 1.054 | offset +0.50 s (164/925 pairs) |
| playoffs_losers-bracket_lb-round-1_hfans-vs-5d_g1_hfans | 1.053 | offset +0.25 s (170/1051 pairs) |
| playoffs_losers-bracket_lb-round-1_hfans-vs-5d_g1_5d | 1.051 | offset -0.25 s (170/1106 pairs) |
| groups_group-2_round-6_btlst-vs-rmn_g1_rmn | 1.051 | offset +0.00 s (286/1160 pairs) |
| playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g3_htdog | 1.049 | offset +0.75 s (259/2408 pairs) |
| groups_group-1_round-4_ksc-vs-kse_g1_ksc | 1.049 | offset -0.25 s (90/617 pairs) |
| playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g3_bonkz | 1.048 | offset -0.75 s (231/1557 pairs) |
| groups_group-4_round-5_resin-vs-inca_g1_resin | 1.048 | offset -5.75 s (224/1221 pairs) |
| groups_group-3_round-3_mach-vs-sccc2_g1_sccc2 | 1.046 | offset +0.50 s (73/2675 pairs) |
| groups_group-4_round-4_hfans-vs-inca_g1_inca | 1.046 | offset +6.50 s (81/456 pairs) |
| playoffs_winners-bracket_wb-round-1_vrtus-vs-bonkz_g2_bonkz | 1.045 | offset +0.50 s (50/446 pairs) |
| groups_group-1_round-1_uysc-vs-ksc_g1_uysc | 1.045 | offset +0.25 s (65/371 pairs) |
| groups_group-3_round-6_kited-vs-h-sr_g1_h-sr | 1.045 | offset -1.50 s (91/1174 pairs) |
| playoffs_losers-bracket_lb-round-2_reeee-vs-hfans_g3_hfans | 1.044 | offset -0.75 s (126/766 pairs) |
| groups_group-4_round-5_hfans-vs-bonkz_g1_bonkz | 1.043 | offset -1.75 s (104/914 pairs) |
| groups_group-1_round-4_ksc-vs-kse_g1_kse | 1.043 | offset +0.25 s (90/675 pairs) |
| groups_group-2_round-7_ogf-vs-kite_g1_kite | 1.043 | offset +0.50 s (77/805 pairs) |
| groups_group-2_round-7_ogf-vs-kite_g1_ogf | 1.043 | offset -0.50 s (97/1106 pairs) |
| playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g1_ksc | 1.042 | offset -0.50 s (169/1353 pairs) |
| playoffs_winners-bracket_wb-round-3_bonkz-vs-resin_g1_bonkz | 1.041 | offset +0.50 s (138/1909 pairs) |
| groups_group-3_round-2_kited-vs-machx_g1_machx | 1.041 | offset -0.25 s (72/427 pairs) |
| playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g1_bn | 1.039 | offset +0.50 s (153/938 pairs) |
| playoffs_winners-bracket_wb-round-1_h-sr-vs-5d_g2_5d | 1.039 | offset -0.25 s (224/950 pairs) |
| groups_group-2_round-6_btlst-vs-rmn_g1_btlst | 1.039 | offset +0.00 s (285/928 pairs) |
| playoffs_winners-bracket_wb-round-1_kite-vs-bn_g2_kite | 1.039 | offset -0.25 s (133/2649 pairs) |
| groups_group-2_round-6_mzy-vs-reeee_g1_reeee | 1.038 | offset +0.75 s (254/2009 pairs) |
| groups_group-4_round-1_epoxy-vs-hfans_g1_hfans | 1.037 | offset +2.75 s (47/618 pairs) |
| playoffs_losers-bracket_lb-round-2_reeee-vs-hfans_g3_reeee | 1.037 | offset +0.75 s (124/915 pairs) |
| groups_group-3_round-7_bonky-vs-nga_g1_nga | 1.037 | offset +3.50 s (46/1352 pairs) |
| playoffs_winners-bracket_wb-round-1_h-sr-vs-5d_g2_h-sr | 1.036 | offset +0.25 s (213/648 pairs) |
| groups_group-4_round-1_epoxy-vs-hfans_g1_epoxy | 1.035 | offset -2.75 s (35/211 pairs) |
| groups_group-3_round-3_mach-vs-sccc2_g1_mach | 1.033 | offset -0.50 s (38/456 pairs) |
| groups_group-3_round-7_bonky-vs-nga_g1_bonky | 1.032 | offset -3.50 s (35/734 pairs) |
| playoffs_winners-bracket_wb-round-1_mzy-vs-machx_g2_mzy | 1.032 | offset +1.50 s (140/814 pairs) |
| playoffs_losers-bracket_lb-round-6_resin-vs-bonkz_g3_bonkz | 1.032 | offset -0.25 s (150/2471 pairs) |
| playoffs_losers-bracket_lb-round-2_kite-vs-machx_g1_machx | 1.031 | offset -1.00 s (208/1111 pairs) |
| groups_group-1_round-5_pn-vs-vrtus_g1_vrtus | 1.030 | offset -0.50 s (44/187 pairs) |
| groups_group-2_round-1_rmn-vs-5d_g1_rmn | 1.030 | offset +1.75 s (99/422 pairs) |
| groups_group-1_round-5_pn-vs-vrtus_g1_pn | 1.030 | offset +0.50 s (43/149 pairs) |
| groups_group-2_round-6_mzy-vs-reeee_g1_mzy | 1.029 | offset -0.75 s (256/1774 pairs) |
| playoffs_losers-bracket_lb-round-5_epoxy-vs-bonkz_g2_epoxy | 1.028 | offset -0.25 s (16/233 pairs) |
| playoffs_winners-bracket_wb-round-1_mzy-vs-machx_g2_machx | 1.028 | offset -1.50 s (146/828 pairs) |
| groups_group-2_round-5_btlst-vs-ogf_g1_btlst | 1.025 | offset +2.00 s (105/730 pairs) |
| playoffs_winners-bracket_wb-round-1_mzy-vs-machx_g1_machx | 1.023 | offset -0.25 s (364/914 pairs) |
| playoffs_winners-bracket_wb-round-1_kite-vs-bn_g2_bn | 1.023 | offset +0.25 s (100/868 pairs) |
| playoffs_winners-bracket_wb-round-3_bonkz-vs-resin_g1_resin | 1.022 | offset -0.50 s (132/1317 pairs) |
| playoffs_losers-bracket_lb-round-6_resin-vs-bonkz_g1_resin | 0.980 | offset -0.75 s (184/1694 pairs) |
| groups_group-3_round-5_bonky-vs-h-sr_g1_bonky | 0.980 | offset +0.75 s (29/634 pairs) |
| playoffs_losers-bracket_lb-round-1_hfans-vs-5d_g2_hfans | 0.980 | offset +0.25 s (130/707 pairs) |
| groups_group-3_round-5_bonky-vs-h-sr_g1_h-sr | 0.978 | offset -0.75 s (19/177 pairs) |
| groups_group-1_round-7_vrtus-vs-ksc_g1_ksc | 0.978 | offset +1.00 s (228/1712 pairs) |
| groups_group-4_round-6_hfans-vs-manba_g1_hfans | 0.978 | offset +0.25 s (79/619 pairs) |
| playoffs_losers-bracket_lb-round-6_resin-vs-bonkz_g1_bonkz | 0.978 | offset +0.75 s (182/1218 pairs) |
| groups_group-4_round-6_hfans-vs-manba_g1_manba | 0.977 | offset -0.25 s (79/580 pairs) |
| groups_group-2_round-1_ogf-vs-mzy_g1_mzy | 0.975 | offset +2.50 s (42/674 pairs) |
| playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g2_bonkz | 0.971 | offset -2.25 s (164/1577 pairs) |
| playoffs_losers-bracket_lb-round-2_reeee-vs-hfans_g1_reeee | 0.971 | offset +0.00 s (169/1185 pairs) |
| playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g1_htdog | 0.971 | offset +1.00 s (139/1107 pairs) |
| groups_group-1_round-5_htdog-vs-kse_g1_htdog | 0.969 | offset +0.25 s (212/1474 pairs) |
| playoffs_losers-bracket_lb-round-2_reeee-vs-hfans_g1_hfans | 0.968 | offset +0.00 s (166/967 pairs) |
| groups_group-1_round-5_htdog-vs-kse_g1_kse | 0.968 | offset -0.25 s (208/1126 pairs) |
| groups_group-4_round-2_epoxy-vs-inca_g1_epoxy | 0.968 | offset +0.00 s (168/981 pairs) |
| playoffs_winners-bracket_wb-round-4_resin-vs-h-sr_g3_h-sr | 0.966 | offset +0.75 s (225/1203 pairs) |
| playoffs_winners-bracket_wb-round-4_resin-vs-h-sr_g3_resin | 0.963 | offset -0.75 s (229/1338 pairs) |
| playoffs_winners-bracket_wb-round-4_resin-vs-h-sr_g1_resin | 0.962 | offset +1.00 s (79/398 pairs) |
| groups_group-3_round-3_machx-vs-bonky_g1_bonky | 0.962 | offset +0.00 s (142/551 pairs) |
| groups_group-1_round-7_htdog-vs-pfans_g1_htdog | 0.960 | offset +2.25 s (116/1437 pairs) |
| groups_group-4_round-2_epoxy-vs-inca_g1_inca | 0.960 | offset +0.00 s (163/777 pairs) |
| groups_group-3_round-1_sccc2-vs-bonky_g1_sccc2 | 0.957 | offset +4.75 s (50/535 pairs) |
| playoffs_winners-bracket_wb-round-4_resin-vs-h-sr_g1_h-sr | 0.955 | offset -1.00 s (83/550 pairs) |
| groups_group-2_round-1_ogf-vs-mzy_g1_ogf | 0.955 | offset -2.50 s (49/873 pairs) |
| groups_group-3_round-3_machx-vs-bonky_g1_machx | 0.955 | offset +0.00 s (148/886 pairs) |
| playoffs_winners-bracket_wb-round-1_mzy-vs-machx_g3_machx | 0.953 | offset -0.50 s (124/480 pairs) |
| playoffs_winners-bracket_wb-round-1_resin-vs-pfans_g2_resin | 0.951 | offset -0.50 s (232/582 pairs) |
| playoffs_winners-bracket_wb-round-1_resin-vs-pfans_g2_pfans | 0.949 | offset +0.50 s (230/566 pairs) |
| playoffs_winners-bracket_wb-round-1_kited-vs-reeee_g2_kited | 0.948 | offset -0.75 s (292/718 pairs) |
| playoffs_winners-bracket_wb-round-1_kited-vs-reeee_g2_reeee | 0.946 | offset +0.75 s (290/729 pairs) |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g1_hfans | 0.946 | offset +3.00 s (228/1369 pairs) |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g1_htdog | 0.944 | offset -3.00 s (225/1300 pairs) |
| playoffs_winners-bracket_wb-round-1_mzy-vs-machx_g3_mzy | 0.942 | offset +0.50 s (145/1095 pairs) |
| groups_group-1_round-5_pfans-vs-uysc_g1_uysc | 0.941 | offset +3.50 s (112/871 pairs) |
| groups_group-1_round-7_htdog-vs-pfans_g1_pfans | 0.937 | offset -2.25 s (100/727 pairs) |
| groups_group-4_round-6_inca-vs-bonkz_g1_bonkz | 0.935 | offset -8.25 s (135/666 pairs) |
| playoffs_winners-bracket_wb-round-1_kited-vs-reeee_g1_kited | 0.931 | offset +1.75 s (209/1939 pairs) |
| playoffs_winners-bracket_wb-round-1_kited-vs-reeee_g1_reeee | 0.930 | offset -1.75 s (182/1026 pairs) |
| playoffs_winners-bracket_wb-round-3_epoxy-vs-h-sr_g3_epoxy | 0.929 | offset +1.25 s (29/337 pairs) |
| groups_group-1_round-5_pfans-vs-uysc_g1_pfans | 0.928 | offset -3.50 s (106/530 pairs) |
| playoffs_winners-bracket_wb-round-2_bonkz-vs-mzy_g1_mzy | 0.928 | offset +0.50 s (139/710 pairs) |
| groups_group-3_round-2_h-sr-vs-sccc2_g1_h-sr | 0.926 | offset -1.25 s (199/859 pairs) |
| groups_group-4_round-6_inca-vs-bonkz_g1_inca | 0.926 | offset +8.25 s (134/791 pairs) |
| groups_group-3_round-2_h-sr-vs-sccc2_g1_sccc2 | 0.926 | offset +1.25 s (191/777 pairs) |
| groups_group-1_round-5_ksc-vs-rsr_g1_rsr | 0.926 | offset +0.00 s (111/1043 pairs) |
| playoffs_winners-bracket_wb-round-3_epoxy-vs-h-sr_g3_h-sr | 0.924 | offset -1.25 s (28/197 pairs) |
| playoffs_winners-bracket_wb-round-2_bonkz-vs-mzy_g1_bonkz | 0.920 | offset -0.50 s (139/610 pairs) |
| playoffs_winners-bracket_wb-round-3_bonkz-vs-resin_g2_bonkz | 0.919 | offset -0.25 s (164/3643 pairs) |
| playoffs_losers-bracket_lb-round-2_kite-vs-machx_g2_machx | 0.918 | offset +0.00 s (73/451 pairs) |
| groups_group-1_round-5_ksc-vs-rsr_g1_ksc | 0.916 | offset +0.00 s (99/562 pairs) |
| playoffs_winners-bracket_wb-round-3_bonkz-vs-resin_g2_resin | 0.915 | offset +0.25 s (134/2229 pairs) |
| playoffs_losers-bracket_lb-round-2_kite-vs-machx_g2_kite | 0.906 | offset +0.00 s (75/448 pairs) |
| groups_group-4_round-3_resin-vs-hfans_g1_resin | 0.901 | offset -2.50 s (124/460 pairs) |
| groups_group-4_round-3_resin-vs-hfans_g1_hfans | 0.898 | offset +2.50 s (127/499 pairs) |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g1_vrtus | 0.894 | offset +1.25 s (179/939 pairs) |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g1_machx | 0.882 | offset -1.25 s (177/734 pairs) |
| playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g3_bn | 0.875 |  |
| groups_group-1_round-3_pn-vs-pfans_g1_pn | 0.859 | offset +1.25 s (74/560 pairs) |
| groups_group-1_round-3_pn-vs-pfans_g1_pfans | 0.842 | offset -1.25 s (76/643 pairs) |
| groups_group-2_round-3_reeee-vs-ogf_g1_ogf | 0.827 | offset -2.25 s (153/1076 pairs) |
| groups_group-1_round-3_rsr-vs-vrtus_g1_vrtus | 0.827 | offset -1.50 s (74/449 pairs) |
| playoffs_grand-final_gf-round-1_h-sr-vs-resin_g4_resin | 0.824 | offset -0.75 s (36/485 pairs) |
| groups_group-1_round-3_rsr-vs-vrtus_g1_rsr | 0.823 | offset +1.50 s (70/341 pairs) |
| playoffs_grand-final_gf-round-1_h-sr-vs-resin_g4_h-sr | 0.822 | offset +0.75 s (41/556 pairs) |
| groups_group-3_round-3_bn-vs-h-sr_g1_bn | 0.821 | offset +1.00 s (113/1028 pairs) |
| groups_group-2_round-3_reeee-vs-ogf_g1_reeee | 0.817 | offset +2.25 s (156/1527 pairs) |
| groups_group-3_round-3_bn-vs-h-sr_g1_h-sr | 0.807 | offset -1.00 s (112/889 pairs) |

# 2. Reference diff: ['H-SR', 'PN', 'RESIN'] vs .\output/20261104-180332
reference rows: 217; rows for the same teams now: 217; rows in total now: 1547
rows in the reference but not now: 0
rows now that the reference did not have: 0
columns: reference 164 now 165 ; new columns: ['one_sided'] ; dropped: []
rows with any non-volatile field changed: 15 of 217
  smoke_damage_total: 8 rows; e.g. [('kots19na_7930', '1', '51294', '23782.05', '22148.05'), ('kots19na_7933', '1', '178680', '23531.43', '22467.18'), ('kots19na_7938', '1', '214885', '38254.15', '34078.15')]
  damage_shell: 8 rows; e.g. [('kots19na_7930', '1', '51294', '21653.55', '20019.55'), ('kots19na_7933', '1', '178680', '23531.43', '22467.18'), ('kots19na_7938', '1', '214885', '35865.39', '33395.64')]
  salvos_credited: 8 rows; e.g. [('kots19na_7930', '1', '51294', '16', '15'), ('kots19na_7933', '1', '178680', '11', '10'), ('kots19na_7938', '1', '214885', '31', '28')]
  smoke_damage_concealed: 8 rows; e.g. [('kots19na_7930', '1', '51294', '11720.55', '10086.55'), ('kots19na_7933', '1', '178680', '22725.75', '21661.50'), ('kots19na_7938', '1', '214885', '38254.14', '34078.14')]
  damage_in_smoke: 6 rows; e.g. [('kots19na_7933', '1', '178680', '9817.88', '8753.63'), ('kots19na_7938', '1', '214885', '29043.02', '24867.02'), ('kots19na_8140', '1', '190362', '12976.92', '16803.72')]
  owner_flag: 5 rows; e.g. [('kots19na_7897', '1', '87568', 'true', 'false'), ('kots19na_7897', '1', '87591', 'true', 'false'), ('kots19na_7897', '1', '87611', 'true', 'false')]
  owner_note: 5 rows; e.g. [('kots19na_7897', '1', '87568', 'nearest ship 619 m from origin', ''), ('kots19na_7897', '1', '87591', 'nearest ship 834 m from origin', ''), ('kots19na_7897', '1', '87611', 'nearest ship 636 m from origin', '')]
  damage_in_smoke_smoker: 4 rows; e.g. [('kots19na_8140', '1', '190362', '12976.92', '16803.72'), ('kots19na_8151', '3', '85026', '20166.44', '19176.45'), ('kots19na_8176', '3', '159292', '60967.16', '36200.41')]
  damage_behind_smoke: 2 rows; e.g. [('kots19na_7930', '1', '51294', '4453.00', '2819.00'), ('kots19na_8183', '2', '90086', '35937.27', '34224.97')]
  damage_behind_smoke_ally: 2 rows; e.g. [('kots19na_7930', '1', '51294', '4453.00', '2819.00'), ('kots19na_8183', '2', '90086', '35937.27', '34224.97')]
  dd_damage: 2 rows; e.g. [('kots19na_7930', '1', '51294', '11720.55', '10086.55'), ('kots19na_8151', '3', '85026', '10582.00', '9592.00')]
  damage_in_smoke_ally: 2 rows; e.g. [('kots19na_7933', '1', '178680', '9012.20', '7947.95'), ('kots19na_7938', '1', '214885', '29043.02', '24867.02')]
  damage_fire: 2 rows; e.g. [('kots19na_7938', '1', '214885', '2388.75', '682.50'), ('kots19na_8176', '3', '159292', '18617.00', '15154.00')]
  smoke_deaths: 1 rows; e.g. [('kots19na_7973', '1', '195445', '0', '1')]
  damage_in_smoke_enemy: 1 rows; e.g. [('kots19na_7933', '1', '178679', '4630.30', '3970.30')]
  purposes: 1 rows; e.g. [('kots19na_8151', '3', '85026', 'damage', '')]
  primary_purpose: 1 rows; e.g. [('kots19na_8151', '3', '85026', 'damage', '')]
  damage_20k: 1 rows; e.g. [('kots19na_8151', '3', '85026', 'true', 'false')]

# 3. Dedupe: smokes seen per run vs kept
games with two runs: 170, with one run: 1
smokes seen in both runs of a game (counted once): 1538; total kept: 1547; rows in smokes.csv: 1547
games where the two runs saw a different number of smokes: 0
one-sided smokes (single-replay games): 9; inferred owners: 4

# 4. Smokes found vs roster smoke activations, per game and team
team-games checked: 342; smokes found: 1547; roster activations: 1776
team-games off by more than 1: 87 (found > activations: 15; found < activations: 72)
note: the activation counter double counts a use seen by both replays more than 1 s apart (backlog F5)

# 5. Per clan
| clan | games | smokes | DD smokes | smokes/game | concealed dmg/game | flagged | note |
|---|---|---|---|---|---|---|---|
| HFANS | 17 | 110 | 79 | 6.5 | 51,350 | 5 |  |
| HTDOG | 18 | 106 | 46 | 5.9 | 47,080 | 6 |  |
| RESIN | 24 | 103 | 87 | 4.3 | 50,846 | 4 |  |
| BONKZ | 21 | 102 | 76 | 4.9 | 61,664 | 5 |  |
| H-SR | 22 | 100 | 89 | 4.5 | 67,397 | 11 | top decile damage |
| -BN- | 14 | 91 | 64 | 6.5 | 87,786 | 7 | top decile damage |
| VRTUS | 11 | 82 | 46 | 7.5 | 63,858 | 2 |  |
| EPOXY | 17 | 82 | 68 | 4.8 | 49,456 | 10 |  |
| MACHX | 14 | 82 | 49 | 5.9 | 49,951 | 0 |  |
| KSC | 11 | 63 | 51 | 5.7 | 64,443 | 9 |  |
| KITED | 14 | 63 | 25 | 4.5 | 22,957 | 3 |  |
| REEEE | 13 | 52 | 44 | 4.0 | 28,997 | 2 |  |
| MZY | 19 | 50 | 43 | 2.6 | 20,247 | 8 |  |
| SCCC2 | 7 | 48 | 32 | 6.9 | 48,926 | 2 |  |
| KITE | 14 | 45 | 43 | 3.2 | 23,349 | 2 |  |
| INCA | 6 | 39 | 20 | 6.5 | 67,990 | 3 | top decile damage, under 7 games |
| 5D | 10 | 37 | 17 | 3.7 | 19,638 | 0 |  |
| UYSC | 7 | 36 | 22 | 5.1 | 22,784 | 0 |  |
| BONKY | 7 | 36 | 25 | 5.1 | 47,317 | 4 |  |
| BTLST | 6 | 34 | 17 | 5.7 | 26,752 | 0 | under 7 games |
| MACH | 7 | 29 | 18 | 4.1 | 14,668 | 4 |  |
| NGA | 7 | 28 | 17 | 4.0 | 19,164 | 3 |  |
| RSR | 7 | 26 | 18 | 3.7 | 23,000 | 1 |  |
| PFANS | 12 | 24 | 18 | 2.0 | 33,129 | 3 |  |
| KSE | 7 | 20 | 15 | 2.9 | 4,503 | 0 |  |
| KM | 5 | 15 | 10 | 3.0 | 31,731 | 7 | many flags, under 7 games |
| PN | 7 | 14 | 10 | 2.0 | 16,598 | 2 |  |
| RMN | 6 | 12 | 11 | 2.0 | 2,216 | 0 | under 7 games |
| OGF | 6 | 9 | 9 | 1.5 | 9,217 | 0 | under 7 games |
| MANBA | 6 | 9 | 5 | 1.5 | 8,021 | 0 | under 7 games |

# 6. Runtime and failures
- runs: 341
- failed runs: 0
- smokes kept: 1547
- flagged smokes: 103
- wall time: 1252 s
errors: 0
```

## Appendix B: before/after compare output

```
rows before 1547, after 1547

# Concealed damage per game, before and after, every clan
| clan | games | smokes before | smokes after | concealed/game before | after | change |
|---|---|---|---|---|---|---|
| -BN- | 14 | 91 | 91 | 90,868 | 87,786 | -3% |
| INCA <- | 6 | 39 | 39 | 89,671 | 67,990 | -24% |
| H-SR | 22 | 100 | 100 | 67,832 | 67,397 | -1% |
| KSC | 11 | 63 | 63 | 62,419 | 64,443 | +3% |
| VRTUS | 11 | 82 | 82 | 65,033 | 63,858 | -2% |
| BONKZ <- | 21 | 102 | 102 | 66,346 | 61,664 | -7% |
| HFANS <- | 17 | 110 | 110 | 55,386 | 51,350 | -7% |
| RESIN | 24 | 103 | 103 | 51,866 | 50,846 | -2% |
| MACHX | 14 | 82 | 82 | 56,148 | 49,951 | -11% |
| EPOXY | 17 | 82 | 82 | 50,477 | 49,456 | -2% |
| SCCC2 | 7 | 48 | 48 | 55,757 | 48,926 | -12% |
| BONKY | 7 | 36 | 36 | 49,243 | 47,317 | -4% |
| HTDOG | 18 | 106 | 106 | 49,662 | 47,080 | -5% |
| PFANS | 12 | 24 | 24 | 33,294 | 33,129 | -0% |
| KM <- | 5 | 15 | 15 | 37,032 | 31,731 | -14% |
| REEEE | 13 | 52 | 52 | 29,797 | 28,997 | -3% |
| BTLST | 6 | 34 | 34 | 27,185 | 26,752 | -2% |
| KITE | 14 | 45 | 45 | 24,271 | 23,349 | -4% |
| RSR | 7 | 26 | 26 | 24,207 | 23,000 | -5% |
| KITED | 14 | 63 | 63 | 23,003 | 22,957 | -0% |
| UYSC | 7 | 36 | 36 | 22,784 | 22,784 | +0% |
| MZY | 19 | 50 | 50 | 21,181 | 20,247 | -4% |
| 5D | 10 | 37 | 37 | 20,824 | 19,638 | -6% |
| NGA | 7 | 28 | 28 | 19,164 | 19,164 | +0% |
| PN | 7 | 14 | 14 | 16,598 | 16,598 | +0% |
| MACH | 7 | 29 | 29 | 16,062 | 14,668 | -9% |
| OGF | 6 | 9 | 9 | 9,217 | 9,217 | +0% |
| MANBA | 6 | 9 | 9 | 12,454 | 8,021 | -36% |
| KSE | 7 | 20 | 20 | 4,712 | 4,503 | -4% |
| RMN | 6 | 12 | 12 | 5,206 | 2,216 | -57% |

# Smoke of the Tournament candidates (top 8 by concealed damage, ties by total)

before:
| # | smoke | team | player | ship | game | clock | concealed | total | one-sided |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 80503 | -BN- | BN_jordi_92T | Gearing | Group 3 / Round 6 vs SCCC2 g1 (Sleeping Giant) | 16:25 | 97,327 | 97,327 | false |
| 2 | 82507 | PFANS | PFANS_Mugu_9 | Harugumo | Group 1 / Round 1 vs KSE g1 (Hotspot) | 07:12 | 96,006 | 102,566 | false |
| 3 | 38986 | INCA | INCA_run_for_yo | Gearing | Group 4 / Round 1 vs KM g1 (Hotspot) | 15:06 | 94,628 | 95,706 | false |
| 4 | 46513 | H-SR | HSR_Yamiyonohik | Somers | Group 3 / Round 3 vs -BN- g1 (Okinawa) | 13:36 | 90,686 | 91,412 | false |
| 5 | 161895 | -BN- | BN_jordi_92T | Somers | Losers Bracket / LB Round 1 vs KSC g2 (Hotspot) | 14:02 | 89,662 | 89,662 | false |
| 6 | 188243 | BONKZ | BONKZ_CheshireZ | Gearing | Group 4 / Round 6 vs INCA g1 (Sleeping Giant) | 17:29 | 85,022 | 85,022 | false |
| 7 | 27092 | EPOXY | EPOXY_Your_SAT_ | Somers | Group 4 / Round 4 vs MANBA g1 (Land of Fire) | 12:07 | 84,328 | 85,285 | false |
| 8 | 99131 | -BN- | BN_jordi_92T | Somers | Winners Bracket / WB Round 1 vs KITE g1 (Land of Fire) | 12:41 | 83,433 | 84,784 | false |

after:
| # | smoke | team | player | ship | game | clock | concealed | total | one-sided |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 80503 | -BN- | BN_jordi_92T | Gearing | Group 3 / Round 6 vs SCCC2 g1 (Sleeping Giant) | 16:25 | 97,327 | 97,327 | false |
| 2 | 82507 | PFANS | PFANS_Mugu_9 | Harugumo | Group 1 / Round 1 vs KSE g1 (Hotspot) | 07:12 | 94,024 | 99,166 | false |
| 3 | 46513 | H-SR | HSR_Yamiyonohik | Somers | Group 3 / Round 3 vs -BN- g1 (Okinawa) | 13:36 | 90,686 | 91,412 | false |
| 4 | 161895 | -BN- | BN_jordi_92T | Somers | Losers Bracket / LB Round 1 vs KSC g2 (Hotspot) | 14:02 | 89,662 | 89,662 | false |
| 5 | 27092 | EPOXY | EPOXY_Your_SAT_ | Somers | Group 4 / Round 4 vs MANBA g1 (Land of Fire) | 12:07 | 84,328 | 85,285 | false |
| 6 | 90084 | RESIN | RESIN_Big_Boy69 | Somers | Grand Final / GF Round 1 vs H-SR g2 (Hotspot) | 17:26 | 80,375 | 80,375 | false |
| 7 | 51115 | EPOXY | EPOXY_Your_SAT_ | Shimakaze | Group 4 / Round 3 vs BONKZ g1 (Okinawa) | 10:48 | 77,031 | 77,031 | false |
| 8 | 183534 | BONKY | BONKY_Lalic | Somers | Group 3 / Round 7 vs NGA g1 (Sea of Fortune) | 17:41 | 74,771 | 74,771 | false |

# Flags
before: flagged 326 of 1547 (21.1%); {'nearest ship': 228, 'no smoke activation': 99, 'minimap': 71, 'inferred': 4}
after: flagged 103 of 1547 (6.7%); {'no smoke activation': 99, 'minimap': 71, 'nearest ship': 5, 'inferred': 4}

# Damage kinds across all runs
before: events {'fire': 132414, 'shell': 155712, 'unknown': 15516, 'flood': 89, 'torpedo': 119}; damage {fire: 40.9M, shell: 279.6M, unknown: 34.3M, flood: 0.0M, torpedo: 0.2M}; shell+fire ratio median 1.093, within 2%: 45 of 341, over 1.25: 20
after: events {'fire': 130419, 'shell': 152745, 'torpedo': 3641, 'unknown': 9678, 'flood': 5181}; damage {fire: 40.0M, shell: 268.0M, torpedo: 27.7M, unknown: 13.0M, flood: 2.6M}; shell+fire ratio median 1.056, within 2%: 56 of 341, over 1.25: 6

# Shooters credited above their own shell+fire result
before: 23 shooter-runs, excess 410,010 of 16,252,981 credited (2.5%)
after: 8 shooter-runs, excess 65,098 of 15,346,092 credited (0.4%)
```
