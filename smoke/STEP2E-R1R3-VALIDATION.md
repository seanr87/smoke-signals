# STEP 2e: validation of R1 to R3 and the secondary-battery kind (STOP)

Data: no-frames batch `output/20261116-172047` (341 runs, 0 failures, 1,547 smokes, 103 flagged) after commits ac05bc33 (R1 to R3 with the finishing-hit exception), 45575761 (secondary kind), 692d2edc (sanity check against main plus secondaries, DESIGN notes) and f3f6602d (reconciliation lists damage by projectile; a diagnostic, no method change). "Before" is the F4 batch `output/20261116-164920` for ledger figures and the committed frames batch `output/20261116-161621` for smoke rows. The checks are `smoke/tools/validate_r.py`; the full output is in the appendix.

Two of the eight checks fail, so nothing further was changed. Section 9 proposes the fixes.

| check | result | pass |
|---|---|---|
| field torpedo ledger toward the ceiling, not above it | 27.7 M to 32.8 M; ceiling 33.1 M (34.1 M recomputed after); ledger over ceiling 0.96 | yes |
| false positives | 139 player-runs, 273k to 104 player-runs, 644k: fewer, but 2.4 times the damage | no |
| overreach over 10% | 148 player-runs, 1.75 M excess; Napoli 12, Brisbane 10, Prinz Adalbert 6, San Martin in the worst 10 twice | no |
| same-tick sample | 702 to 372 events; still 241 shell against 131 torpedo by the run-total test | no |
| kills from smoke | 120 to 114 field-wide; H-SR 12, RESIN 11, PN 0 unchanged | yes (see 4) |
| shell ledger against main plus secondaries | field 1.009; shell alone 0.983, secondary 1.59 of the game's secondaries | mapping right, attribution wrong (see 5) |
| original 217 rows | 18 rows changed in damage or flag columns, all explained | yes |
| Smoke of the Tournament, per-clan table | leader unchanged; top 8 unchanged | yes |

## 1. Field torpedo ledger

| | before | after |
|---|---|---|
| ledger torpedo | 27,747,728 | 32,790,161 |
| game result torpedo | 37,011,165 | 37,011,165 |
| ceiling (ledger torpedo plus unknown on players who scored torpedo damage) | 33,087,403 | 34,092,782 |
| ledger over ceiling | 0.839 | 0.962 |
| false positives (ledger torpedo, none in the result) | 139 player-runs, 272,865 | 104 player-runs, 644,150 |
| misses (torpedo in the result, none in the ledger) | 253 player-runs, 4,835,492 | 156 player-runs, 2,408,975 |
| player-runs within 10% of the result | 619 of 1,375 | 777 of 1,375 |

The window recovers the held-position misses (misses halve, the ledger reaches 96% of what the replays carry) and does not exceed the ceiling. The false positives are fewer but larger:

| run | player | ship | false torpedo |
|---|---|---|---|
| LB R4 BONKZ vs HTDOG g2 (both runs) | HTDOG_Miami_Mat | Thor | 43,680 |
| LB R1 KSC vs -BN- g2 (both runs) | BN_HoshimiMiyab | San Martin | 30,548 |
| LB R3 HFANS vs MZY g1 | HFANS_tokai_tei | Napoli | 17,542 |
| Group 4 R4 HFANS vs INCA (both runs) | INCA_TheUnknow_ | St. Vincent | 16,701 |
| WB R1 KITE vs -BN- g1 (both runs) | KITE_RighteousF | Thor | 16,212 |
| Group 2 R4 5D vs OGF | 5D_lh47383 | San Martin | 16,150 |

Traced:

- Thor, 43,680 in one tick with a resolved shell hit at 825.35 s. The game credits the player 101,243 main-battery AP and no torpedo damage; the ledger's shell plus torpedo is exactly 101,243. The tick is a main-battery salvo; a Thor torpedo passed within 400 m of the victim inside the 12 s window while the salvo landed. The 3,000 floor cannot stop it.
- San Martin, 30,548 over five ticks of 4,726 to 7,922, in equal-amount pairs 1.8 s apart (unmerged duplicates of SAP salvos in a drift game). The game credits 90,475 main AP and no torpedoes. Cruiser salvos of 4,000 to 8,000 pass the 3,000 floor.

## 2. Overreach over 10%

148 player-runs, excess 1,747,172. Worst 10:

| run | player | ship | ledger torpedo | result torpedo | excess | ledger shell | result main |
|---|---|---|---|---|---|---|---|
| Group 4 R3 MANBA vs KM (both runs) | MANBA_Your_Soci | San Martin | 61,175 | 25,427 | +35,748 | 102,870 | 104,711 |
| LB R1 MACHX vs VRTUS g2 (both runs) | VRTUS_LightTheB | Napoli | 42,860 | 10,119 | +32,741 | 44,449 | 70,697 |
| Group 1 R6 VRTUS vs UYSC (both runs) | UYSC_DMR7575 | Shimakaze | 111,677 | 79,217 | +32,460 | 0 | 0 |
| Group 2 R4 KITE vs RMN (both runs) | KITE_BroadWish | 20 de Julio | 72,419 | 43,010 | +29,409 | 77,848 | 76,244 |
| Group 3 R1 SCCC2 vs BONKY | BONKY_bartimus_ | Somers | 114,630 | 88,434 | +26,196 | 3,445 | 3,445 |
| Group 3 R4 KITED vs BONKY | KITED_Nyko_Yko | San Martin | 58,128 | 33,941 | +24,187 | 36,783 | 39,762 |

Two patterns. Cruisers with torpedoes that shell the target their torpedoes pass (San Martin, Napoli, 20 de Julio): the Napoli case has a single 32,780 tick with a resolved shell hit called torpedo while the game gives it 10,119 torpedo damage in the whole battle. Destroyers in drift games (Shimakaze, Somers): the ledger carries unmerged duplicate torpedo hits; this is the clock-drift limit, not R1, and the game is one of the known drift pairs.

Watched ships, after: Napoli 230 player-runs, ledger 1,194,143 against 1,063,352 (12 over 10%, 156k; 21 false positives, 106k); Brisbane 990,559 against 1,064,996 (10 over, 107k; 6 false positives, 10k); Prinz Adalbert 219,231 against 192,710 (6 over, 31k; 3 false positives, 19k); Minotaur 76,215 against 119,660 (none over, 1 false positive of 3k). San Martin appears in the worst 10 twice and in the false positives twice.

## 3. Same-tick sample

372 torpedo events share a tick with a resolved shell hit (702 before). Redrawn sample of 10 (seed 11):

| run | attacker | ship | victim | amount | ledger torpedo | result torpedo | as shell instead | verdict |
|---|---|---|---|---|---|---|---|---|
| Group 4 R7 RESIN vs BONKZ | RESIN_Maddog242 | Gdansk | BONKZ_King_Vipe | 1,396 | 41,161 | 63,725 | 39,765 | torpedo (finishing hit) |
| LB R2 MZY vs -BN- g2 | MZY_Inori_Takim | Prinz Adalbert | BN_capitankelvi | 3,697 | 7,395 | 0 | 3,698 | shell |
| LB R1 KITED vs PFANS g1 | KITED_JustRib | Venezia | PFANS_Nolimits_ | 5,148 | 5,148 | 0 | 0 | shell |
| LB R1 MACHX vs VRTUS g2 | VRTUS_LightTheB | Napoli | MACHX_DrobotPri | 32,780 | 42,860 | 10,119 | 10,080 | shell |
| LB R4 BONKZ vs HTDOG g2 | BONKZ_Bows3r | San Martin | HTDOG_Doomed_Yu | 3,060 | 3,060 | 11,919 | 0 | torpedo |
| Group 2 R4 KITE vs RMN | KITE_BroadWish | 20 de Julio | RMN_Tregonsee | 10,558 | 72,419 | 43,010 | 61,861 | shell |
| Group 2 R4 KITE vs RMN | KITE_BroadWish | 20 de Julio | RMN_Tregonsee | 12,762 | 72,419 | 43,010 | 59,657 | shell |
| LB R2 HTDOG vs KITED g1 | HTDOG_Miami_Mat | Thor | KITED_Terminato | 4,504 | 4,504 | 12,125 | 0 | torpedo |
| LB R1 KITED vs PFANS g2 | KITED_JustRib | Napoli | PFANS_Howell119 | 8,100 | 24,400 | 28,341 | 16,300 | torpedo |
| WB R1 HTDOG vs HFANS g2 | HTDOG_Rei | Svea | HFANS_ARP_I_401 | 3,054 | 3,054 | 0 | 0 | shell |

Over all 372 the run-total test says 241 shell, 131 torpedo. The shells are cruiser salvos of 3,000 to 33,000 landing while a torpedo of the same ship passes the target within the window; the 3,000 floor is below a cruiser salvo and the 12 s window is wider than the exact-clock test the same-tick case needs.

## 4. Kills from smoke

120 before, 114 after; H-SR 12, RESIN 11, PN 0 in both. The six lost kills (5D Napoli, VRTUS Shimakaze, MANBA Napoli, VRTUS Napoli, KITE Z-52, HTDOG Jinan) are sinkings whose final blow is now a torpedo or a secondary rather than a main-battery shell; the kill rule needs a credited shell as the last event, so they drop out by definition. The finishing-hit exception kept the finishing torpedoes as torpedoes, as intended.

## 5. Shell ledger against main plus secondaries

| | before | after |
|---|---|---|
| ledger shell / secondary / fire / torpedo / unknown | 268.0 / 0 / 40.0 / 27.7 / 13.0 M | 248.4 / 18.2 / 38.6 / 32.8 / 10.8 M |
| result main / secondaries / fire / torpedo | 252.8 / 11.4 / 40.3 / 37.0 M | same |
| shell over main | 1.060 | 0.983 |
| secondary over the game's secondaries | | 1.591 |
| shell plus secondary over main plus secondaries | 1.014 | 1.009 |
| fire over fire | 0.993 | 0.958 |
| per-run bands, shell plus secondary plus fire over main plus secondaries plus fire | | 96 within 2%, 101 at 1.02 to 1.10, 31 at 1.10 to 1.25, 89 at 0.90 to 0.98, 24 under 0.90 |

The projectile diagnostic on PN vs UYSC shows the mapping itself is right: every projectile called secondary is a secondary gun's shell (Ohio 127 mm HE Mk41, Sibir 130 mm HE, Napoli 152 mm and 90 mm SAP, Salem 127 mm HE) and Napoli's secondary total matches the game's within 3% (8,665 against 8,898). The excess comes from the salvo fallback: a damage event without a resolved shot hit is matched to the attacker's latest salvo within 25 s, and a battleship's secondaries fire a salvo every few seconds, so main-battery hits without a resolved shot land on a secondary salvo. Ohio in that game: ledger main 128,520 and secondary 55,089 against the game's 163,951 and 23,029; the 32k that moved from main to secondary is the same 35k the main is short. Sibir: 81,359 and 28,704 against 96,317 and 16,131.

Fire is 0.958 of the game's fire because a fire tick that follows only secondary hits is now unknown (by design, DESIGN 6.2); part of that is the same misattribution.

## 6. The original 217 rows against round 6

The no-frames run leaves the Tier 1 state columns empty (score, ships alive, HP, spotting at activation and capture, cap proximity, nearest enemy and the frame file names: 41 columns), so those differ on every row and say nothing about the method. Over the other 123 columns, 18 of the 217 rows changed; none added or lost. By cause:

| cause | rows | smokes |
|---|---|---|
| F2, flag cleared, no value changed | 5 | 87568, 87591, 87611, 190358 (RESIN_thepregna, Svea), 3191 (HSR_Yuzuriha_Ou, Svea) |
| secondary hits no longer credited (shell to secondary, 150 to 2,314 damage each) | 8 | 178501 RESIN_Fryce Somers (-1,188), 178502 RESIN_Hungria15 Napoli (-3,584, label island_killer to hunt), 174224 PN_Sean_O_Reill Harugumo (-2,015 shell, +1,120 fire relinked), 27151 RESIN_Fryce Harugumo (-745), 97311 PN_FiftyForATwe Somers (-2,646), 180816 RESIN_eagle_lan Gdansk (-314), 39294 and 178679 (enemy-side columns only) |
| torpedo reclassification | 3 | 159292 RESIN_Maddog242 Harugumo: 60,967 to 41,812 (four small ticks that the F4 batch called torpedo return to shell under the floor; the rest stays torpedo); 34490 HSR_Mixic37 Gdansk: a 3,548 tick to torpedo (-3,548); 190362 RESIN_thepregna Svea: 12,977 to 16,804 (round 6's false torpedoes back to shells) |
| knock-on | 2 | 195445 PN Harugumo gains a smoke death (its shots from behind the smoke are credited shells now); 90088 HSR_Apex_captai Conte Verde gains 4,950 of fire relinked to its own shell |

Compared with the STEP 2c list, 51294, 178680, 214885, 85026, 166114 and 90086 are back to their round 6 values: the F4 batch had called their small ticks torpedoes, the floor returns them to shells. Of the clan figures in the published round 6 report: H-SR concealed per game 67,832 to 67,671, RESIN 51,866 to 51,078, PN 16,598 to 16,319.

## 7. Smoke of the Tournament and the per-clan table

The top 8 is the same list in the same order before and after; PFANS_Mugu_9's second place returns to 96,006 (its small torpedo ticks are shells again). Concealed per game: -BN- 87,786 to 87,202, H-SR 67,397 to 67,671, INCA 67,990 to 65,529, KSC 64,443 to 65,011, VRTUS 63,858 to 61,420, BONKZ 61,664 to 61,228. The large moves are small clans whose shooting from smoke was torpedoes or secondaries: 5D 19,638 to 10,666 (its four 20k smokes to none), MANBA 8,021 to 4,540, UYSC 22,784 to 16,276, KM 31,731 to 26,512, KITED 22,957 to 20,015, BTLST 26,752 to 23,472. The 5D and UYSC drops include San Martin and Napoli salvos that R1 wrongly calls torpedoes (section 2), so they are overstated.

## 8. Secondaries and airstrikes, noted

A Utrecht in MZY vs MACHX g3 shows 71,494 ledger shell against 24,578 main battery in the game's result; the difference is its air-support bombs (8.1 M over the field under `damage_bomb_airsupport`) matched to recent salvos. Dutch cruisers and ASW airstrikes only; not touched.

## 9. Proposals (nothing applied)

- **P1, same-tick ticks use the exact-clock test.** A resolved shell hit means the victim was spotted, so its position is fresh and the 12 s window is not needed; the window stays for ticks without a resolved hit, where the held position is the problem. Removes the Thor and most of the Napoli, San Martin and 20 de Julio cases.
- **P2, a floor relative to the torpedo.** A torpedo tick must carry at least 0.6 times the alpha damage of the matched torpedo (the projectile's `alpha_damage` in game params), finishing hits excepted; 3,000 is below a cruiser salvo. For San Martin (16.9k alpha) the floor is about 10k, for Napoli about 9.6k, for the destroyers 8k to 14k.
- **P3, the salvo fallback considers main-battery salvos only.** A damage event without a resolved shot hit is matched to the attacker's latest main-battery salvo within 25 s; secondary salvos are matched only through resolved shot hits. Secondaries then stay what the resolved hits say (right on Napoli) and main-battery damage without a resolved hit stays main, as before the change.

Expected after P1 to P3: false positives and overreach well under the F4 figures (139 player-runs, 273k), the same-tick set mostly torpedoes, secondary over the game's secondaries near 1.0, shell over main near 1.0, fire back near 0.99, and the per-clan table close to the "after" column above except 5D, UYSC, San Martin and Napoli users moving back up. Then a frames run for the site batch, since the no-frames batches cannot feed it.

## Appendix: validate_r.py output

The section 6 list in the raw output includes the 41 frame-dependent columns on every row; the table above is the diff over the other columns.

```
# 1. Field torpedo ledger
before: ledger torpedo 27,747,728; result 37,011,165; ceiling (ledger torpedo plus unknown on torpedo scorers) 33,087,403; ledger over ceiling 0.839
  false positives: 139 player-runs, 272,865; misses: 253 player-runs, 4,835,492; median ratio 1.000; within 10%: 619 of 1375
after: ledger torpedo 32,790,161; result 37,011,165; ceiling (ledger torpedo plus unknown on torpedo scorers) 34,092,782; ledger over ceiling 0.962
  false positives: 104 player-runs, 644,150; misses: 156 player-runs, 2,408,975; median ratio 1.000; within 10%: 777 of 1375

False positives after, largest 10:
  playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g2_bonkz HTDOG_Miami_Mat Thor: 43,680
  playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g2_htdog HTDOG_Miami_Mat Thor: 43,680
  playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g2_bn BN_HoshimiMiyab San Martin: 30,548
  playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g2_ksc BN_HoshimiMiyab San Martin: 30,548
  playoffs_losers-bracket_lb-round-3_hfans-vs-mzy_g1_hfans HFANS_tokai_tei Napoli: 17,542
  groups_group-4_round-4_hfans-vs-inca_g1_hfans INCA_TheUnknow_ St. Vincent: 16,701
  groups_group-4_round-4_hfans-vs-inca_g1_inca INCA_TheUnknow_ St. Vincent: 16,701
  playoffs_winners-bracket_wb-round-1_kite-vs-bn_g1_bn KITE_RighteousF Thor: 16,212
  playoffs_winners-bracket_wb-round-1_kite-vs-bn_g1_kite KITE_RighteousF Thor: 16,212
  groups_group-2_round-4_5d-vs-ogf_g1_5d 5D_lh47383 San Martin: 16,150

# 2. Overreach: ledger torpedo above the result by more than 10%, worst 10 (after)
player-runs: 148; excess 1,747,172
| run | player | ship | ledger torpedo | result torpedo | excess | ledger shell | result main |
|---|---|---|---|---|---|---|---|
| groups_group-4_round-3_manba-vs-km_g1_km | MANBA_Your_Soci | San Martin | 61,175 | 25,427 | +35,748 | 102,870 | 104,711 |
| groups_group-4_round-3_manba-vs-km_g1_manba | MANBA_Your_Soci | San Martin | 61,175 | 25,427 | +35,748 | 99,804 | 104,711 |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g2_machx | VRTUS_LightTheB | Napoli | 42,860 | 10,119 | +32,741 | 44,449 | 70,697 |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g2_vrtus | VRTUS_LightTheB | Napoli | 42,860 | 10,119 | +32,741 | 38,785 | 70,697 |
| groups_group-1_round-6_vrtus-vs-uysc_g1_uysc | UYSC_DMR7575 | Shimakaze | 111,677 | 79,217 | +32,460 | 0 | 0 |
| groups_group-1_round-6_vrtus-vs-uysc_g1_vrtus | UYSC_DMR7575 | Shimakaze | 111,677 | 79,217 | +32,460 | 0 | 0 |
| groups_group-2_round-4_kite-vs-rmn_g1_rmn | KITE_BroadWish | 20 de Julio | 72,419 | 43,010 | +29,409 | 77,848 | 76,244 |
| groups_group-2_round-4_kite-vs-rmn_g1_kite | KITE_BroadWish | 20 de Julio | 71,927 | 43,010 | +28,917 | 76,647 | 76,244 |
| groups_group-3_round-1_sccc2-vs-bonky_g1_bonky | BONKY_bartimus_ | Somers | 114,630 | 88,434 | +26,196 | 3,445 | 3,445 |
| groups_group-3_round-4_kited-vs-bonky_g1_bonky | KITED_Nyko_Yko | San Martin | 58,128 | 33,941 | +24,187 | 36,783 | 39,762 |
watched ships (Napoli, Brisbane, Minotaur, Prinz Adalbert, San Martin), after:
  Napoli: 230 player-runs, ledger 1,194,143 vs result 1,063,352; over 10%: 12 (156,415); false positives 21 (106,301)
  Brisbane: 120 player-runs, ledger 990,559 vs result 1,064,996; over 10%: 10 (107,426); false positives 6 (10,285)
  Minotaur: 52 player-runs, ledger 76,215 vs result 119,660; over 10%: 0 (0); false positives 1 (3,488)
  Prinz Adalbert: 62 player-runs, ledger 219,231 vs result 192,710; over 10%: 6 (30,636); false positives 3 (19,305)
  San Mart: 0 player-runs, ledger 0 vs result 0; over 10%: 0 (0); false positives 0 (0)

# 3. Same-tick sample (after)
torpedo events 2913; sharing a tick with a shell hit: 372
| run | attacker | ship | victim | amount | ledger torpedo | result torpedo | as shell instead | verdict |
|---|---|---|---|---|---|---|---|---|
| groups_group-4_round-7_resin-vs-bonkz_g1_bonkz | RESIN_Maddog242 | Gdansk | BONKZ_King_Vipe | 1,396 | 41,161 | 63,725 | 39,765 | torpedo |
| playoffs_losers-bracket_lb-round-2_mzy-vs-bn_g2_mzy | MZY_Inori_Takim | Prinz Adalbert | BN_capitankelvi | 3,697 | 7,395 | 0 | 3,698 | shell |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g1_kited | KITED_JustRib | Venezia | PFANS_Nolimits_ | 5,148 | 5,148 | 0 | 0 | shell |
| playoffs_losers-bracket_lb-round-1_machx-vs-vrtus_g2_machx | VRTUS_LightTheB | Napoli | MACHX_DrobotPri | 32,780 | 42,860 | 10,119 | 10,080 | shell |
| playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g2_bonkz | BONKZ_Bows3r | San Martin | HTDOG_Doomed_Yu | 3,060 | 3,060 | 11,919 | 0 | torpedo |
| groups_group-2_round-4_kite-vs-rmn_g1_rmn | KITE_BroadWish | 20 de Julio | RMN_Tregonsee | 10,558 | 72,419 | 43,010 | 61,861 | shell |
| groups_group-2_round-4_kite-vs-rmn_g1_rmn | KITE_BroadWish | 20 de Julio | RMN_Tregonsee | 12,762 | 72,419 | 43,010 | 59,657 | shell |
| playoffs_losers-bracket_lb-round-2_htdog-vs-kited_g1_htdog | HTDOG_Miami_Mat | Thor | KITED_Terminato | 4,504 | 4,504 | 12,125 | 0 | torpedo |
| playoffs_losers-bracket_lb-round-1_kited-vs-pfans_g2_pfans | KITED_JustRib | Napoli | PFANS_Howell119 | 8,100 | 24,400 | 28,341 | 16,300 | torpedo |
| playoffs_winners-bracket_wb-round-1_htdog-vs-hfans_g2_hfans | HTDOG_Rei | Svea | HFANS_ARP_I_401 | 3,054 | 3,054 | 0 | 0 | shell |
all same-tick events judged by the run total: {'shell': 241, 'torpedo': 131}

# 4. Kills from smoke
before: kills from smoke 120 (H-SR 12, RESIN 11, PN 0); smoke deaths 177
after: kills from smoke 114 (H-SR 12, RESIN 11, PN 0); smoke deaths 177

# 5. Shell ledger against main plus secondaries
before: ledger shell 268.0M, secondary 0.0M, fire 40.0M, torpedo 27.7M, unknown 13.0M | result main 252.8M, secondaries 11.4M, fire 40.3M, torpedo 37.0M
  shell over main: 1.060; shell plus secondary over main plus secondaries: 1.014; secondary over secondaries: 0.000; fire over fire: 0.993; shell plus fire over main plus fire: 1.051
after: ledger shell 248.4M, secondary 18.2M, fire 38.6M, torpedo 32.8M, unknown 10.8M | result main 252.8M, secondaries 11.4M, fire 40.3M, torpedo 37.0M
  shell over main: 0.983; shell plus secondary over main plus secondaries: 1.009; secondary over secondaries: 1.591; fire over fire: 0.958; shell plus fire over main plus fire: 0.979
per-run bands, ledger shell plus secondary plus fire over result main plus secondaries plus fire (after): {'0.98-1.02': 96, '1.02-1.1': 101, '1.1-1.25': 31, '0.9-0.98': 89, '0-0.9': 24}
per-run bands, ledger shell plus fire over result main plus fire (after): {'0.98-1.02': 78, '0.9-0.98': 116, '1.02-1.1': 85, '0-0.9': 45, '1.1-1.25': 17}

# 6. Original 217 rows against round 6
(section 6 raw rows left out: 217 rows, frame-dependent columns)
rows changed: 217 of 217; columns: {'score_ours_act': 217, 'score_theirs_act': 217, 'cap_state_act': 217, 'cap_progress_act': 217, 'ships_alive_act': 217, 'alive_ours_act': 217, 'alive_theirs_act': 217, 'smoker_hp_pct_act': 217, 'smoker_spotted_act': 217, 'smoker_spotted_flags_act': 217, 'enemy_radars_alive_act': 217, 'score_ours_cap': 217, 'score_theirs_cap': 217, 'cap_state_cap': 217, 'cap_progress_cap': 217, 'ships_alive_cap': 217, 'alive_ours_cap': 217, 'alive_theirs_cap': 217, 'smoker_hp_pct_cap': 217, 'smoker_spotted_cap': 217, 'smoker_spotted_flags_cap': 217, 'enemy_radars_alive_cap': 217, 'allies_in_smoke_count': 217, 'frame_act': 217, 'frame_cap': 217, 'frame_act_zoom': 217, 'frame_cap_zoom': 217, 'nearest_enemy_act': 202, 'nearest_enemy_dist_km_act': 202, 'nearest_cap_act': 202, 'dist_to_nearest_cap_km_act': 202, 'cap_contested_act': 202, 'nearest_cap_cap': 198, 'dist_to_nearest_cap_km_cap': 198, 'cap_contested_cap': 198, 'nearest_enemy_cap': 197, 'nearest_enemy_dist_km_cap': 197, 'cap_proximity_m': 159, 'cap_proximity_name': 159, 'cap_radius_m': 159, 'damage_in_smoke': 10, 'smoke_damage_total': 10, 'damage_shell': 9, 'salvos_credited': 9, 'damage_in_smoke_ally': 6, 'smoke_damage_detected': 6, 'detected_damage_by': 6, 'smoke_damage_concealed': 5, 'owner_flag': 5, 'owner_note': 5, 'damage_in_smoke_smoker': 4, 'damage_fire': 3, 'damage_behind_smoke_enemy': 2, 'smoke_deaths': 1, 'dd_damage': 1, 'damage_label': 1, 'damage_in_smoke_enemy': 1, 'damage_behind_smoke': 1, 'damage_behind_smoke_ally': 1, 'shooters': 1}

# 7. Smoke of the Tournament candidates and per-clan concealed per game

before top 8:
  1. 80503 -BN- BN_jordi_92T Gearing, Group 3 / Round 6 vs SCCC2 g1 (Sleeping Giant) 16:25: 97,327 / 97,327
  2. 82507 PFANS PFANS_Mugu_9 Harugumo, Group 1 / Round 1 vs KSE g1 (Hotspot) 07:12: 94,024 / 99,166
  3. 46513 H-SR HSR_Yamiyonohik Somers, Group 3 / Round 3 vs -BN- g1 (Okinawa) 13:36: 90,686 / 91,412
  4. 161895 -BN- BN_jordi_92T Somers, Losers Bracket / LB Round 1 vs KSC g2 (Hotspot) 14:02: 89,662 / 89,662
  5. 27092 EPOXY EPOXY_Your_SAT_ Somers, Group 4 / Round 4 vs MANBA g1 (Land of Fire) 12:07: 84,328 / 85,285
  6. 90084 RESIN RESIN_Big_Boy69 Somers, Grand Final / GF Round 1 vs H-SR g2 (Hotspot) 17:26: 80,375 / 80,375
  7. 51115 EPOXY EPOXY_Your_SAT_ Shimakaze, Group 4 / Round 3 vs BONKZ g1 (Okinawa) 10:48: 77,031 / 77,031
  8. 183534 BONKY BONKY_Lalic Somers, Group 3 / Round 7 vs NGA g1 (Sea of Fortune) 17:41: 74,771 / 74,771

after top 8:
  1. 80503 -BN- BN_jordi_92T Gearing, Group 3 / Round 6 vs SCCC2 g1 (Sleeping Giant) 16:25: 97,327 / 97,327
  2. 82507 PFANS PFANS_Mugu_9 Harugumo, Group 1 / Round 1 vs KSE g1 (Hotspot) 07:12: 96,006 / 102,566
  3. 46513 H-SR HSR_Yamiyonohik Somers, Group 3 / Round 3 vs -BN- g1 (Okinawa) 13:36: 90,686 / 91,412
  4. 161895 -BN- BN_jordi_92T Somers, Losers Bracket / LB Round 1 vs KSC g2 (Hotspot) 14:02: 89,662 / 89,662
  5. 27092 EPOXY EPOXY_Your_SAT_ Somers, Group 4 / Round 4 vs MANBA g1 (Land of Fire) 12:07: 84,328 / 85,285
  6. 90084 RESIN RESIN_Big_Boy69 Somers, Grand Final / GF Round 1 vs H-SR g2 (Hotspot) 17:26: 80,375 / 80,375
  7. 51115 EPOXY EPOXY_Your_SAT_ Shimakaze, Group 4 / Round 3 vs BONKZ g1 (Okinawa) 10:48: 77,031 / 77,031
  8. 183534 BONKY BONKY_Lalic Somers, Group 3 / Round 7 vs NGA g1 (Sea of Fortune) 17:41: 74,771 / 74,771

| clan | games | concealed/game before | after | change | smokes 20k+ before | after |
|---|---|---|---|---|---|---|
| -BN- | 14 | 87,786 | 87,202 | -1% | 20 | 20 |
| H-SR | 22 | 67,397 | 67,671 | +0% | 34 | 35 |
| INCA | 6 | 67,990 | 65,529 | -4% | 7 | 6 |
| KSC | 11 | 64,443 | 65,011 | +1% | 14 | 14 |
| VRTUS | 11 | 63,858 | 61,420 | -4% | 11 | 11 |
| BONKZ | 21 | 61,664 | 61,228 | -1% | 21 | 22 |
| RESIN | 24 | 50,846 | 51,078 | +0% | 26 | 26 |
| HFANS | 17 | 51,350 | 50,930 | -1% | 16 | 16 |
| EPOXY | 17 | 49,456 | 49,551 | +0% | 15 | 15 |
| MACHX | 14 | 49,951 | 48,508 | -3% | 9 | 9 |
| BONKY | 7 | 47,317 | 45,779 | -3% | 6 | 6 |
| HTDOG | 18 | 47,080 | 45,564 | -3% | 12 | 12 |
| SCCC2 | 7 | 48,926 | 45,297 | -7% | 4 | 3 |
| PFANS | 12 | 33,129 | 32,657 | -1% | 9 | 8 |
| REEEE | 13 | 28,997 | 28,038 | -3% | 8 | 9 |
| KM | 5 | 31,731 | 26,512 | -16% | 4 | 3 |
| KITE | 14 | 23,349 | 23,544 | +1% | 5 | 5 |
| BTLST | 6 | 26,752 | 23,472 | -12% | 3 | 3 |
| RSR | 7 | 23,000 | 23,076 | +0% | 4 | 4 |
| MZY | 19 | 20,247 | 20,331 | +0% | 5 | 5 |
| KITED | 14 | 22,957 | 20,015 | -13% | 4 | 3 |
| NGA | 7 | 19,164 | 18,209 | -5% | 1 | 1 |
| PN | 7 | 16,598 | 16,319 | -2% | 2 | 2 |
| UYSC | 7 | 22,784 | 16,276 | -29% | 4 | 2 |
| MACH | 7 | 14,668 | 14,430 | -2% | 3 | 3 |
| 5D | 10 | 19,638 | 10,666 | -46% | 4 | 0 |
| OGF | 6 | 9,217 | 9,124 | -1% | 1 | 1 |
| MANBA | 6 | 8,021 | 4,540 | -43% | 1 | 0 |
| KSE | 7 | 4,503 | 3,801 | -16% | 0 | 0 |
| RMN | 6 | 2,216 | 2,216 | +0% | 0 | 0 |
```
