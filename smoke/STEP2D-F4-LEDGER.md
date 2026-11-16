# STEP 2d: F4 validation and the ledger over-count

Data: a no-frames re-run of the final batch, `output/20261116-164920` (same 341 runs and 1,547 smokes as `output/20261116-161621`, kept on disk, not committed), made after the reconciliation record gained each ship's ledger by classified kind and every non-zero damage field of the game's own result (commit bcd288a9). The checks are `f4check.py` (scratch; full output in the appendix). No method changed in this step.

## 1. F4 validation

### 1a. Ledger torpedo damage against the game's torpedo result, per player per run

6,138 player-runs; 1,375 have torpedo damage in the game result.

| | |
|---|---|
| ratio ledger over result, median | 1.000 |
| within 10% | 619 of 1,375 |
| under 0.5 | 404 |
| over 1.5 | 32 |
| field total | ledger 27.7 M against result 37.0 M (0.75) |
| false positives (ledger torpedo, none in the result) | 139 player-runs, 272,865 in all (0.7% of the result's torpedo damage); largest 11,622 |
| misses (torpedo in the result, none in the ledger) | 253 player-runs, 4,835,492 |

Worst 10 by gap, all misses:

| run | player | ship | ledger torpedo | result torpedo | ledger shell | ledger unknown |
|---|---|---|---|---|---|---|
| Group 3 R7 BONKY vs NGA (both runs) | BONKY_Lalic | Somers | 0 | 118,002 | 2,482 | 39,041 |
| Group 4 R7 INCA vs MANBA (MANBA run) | INCA_run_for_yo | Chateaurenault | 720 | 110,138 | 1,919 | 108,986 |
| Group 3 R1 SCCC2 vs BONKY | BONKY_bartimus_ | Somers | 0 | 88,434 | 3,445 | 93,231 |
| Group 4 R4 HFANS vs INCA (both runs) | INCA_run_for_yo | Chateaurenault | 0 | 79,757 | 0 | 34,647 |
| Group 1 R5 PFANS vs UYSC | UYSC_DMR7575 | Shimakaze | 391 | 66,404 | 0 | 46,864 |
| Group 4 R5 RESIN vs INCA | INCA_run_for_yo | Shimakaze | 0 | 65,039 | 3,110 | 66,176 |
| Group 1 R6 VRTUS vs UYSC | UYSC_DMR7575 | Shimakaze | 17,732 | 79,217 | 0 | 94,737 |
| WB R2 RESIN vs REEEE g2 | REEEE_Daka_Daka | Yueyang | 832 | 61,819 | 1,188 | 77,366 |

The misses have two causes, in this order of size:

1. **Packet coverage.** Many torpedo hits are in neither replay's damage events. BONKY_Lalic's Somers did 120k in the game result and the merged ledger holds 41k of it in seven events. Over the field, the ledger's torpedo plus unknown damage on players who scored torpedo damage is 33.1 M against the result's 37.0 M, so about 11% of torpedo damage never reaches the ledger. That is the replay format (a client is told about hits in its area of interest), not the classifier, and it is the same gap the shell ledger has.
2. **The position test at the damage clock.** Of the hits that are in the ledger, the unmatched ones sit in `unknown` (13.0 M in all, of which about 3 M is ramming and air-support bombs and the rest torpedo hits). Traced example, INCA_run_for_yo's Chateaurenault at 219.84 s in HFANS vs INCA: two hits of 11,574 and 14,800 on HFANS_tokai_tei. The attacker had two salvos in the water; the first passed the victim's position 8 s before the damage clock, the second 10 s after; at the clock itself they were 1.5 km and 2.1 km away. The victim was a held (stale) position of a ship not spotted at that moment, so the exact-clock test cannot succeed.

### 1b. Torpedo events that share a tick with a resolved shell hit

702 of the 3,641 torpedo events. The sample of 10 (appendix) and the whole set:

| | same-tick torpedo events | torpedo events without a shell hit |
|---|---|---|
| count | 702 | 2,939 |
| median amount | 924 | 9,346 |
| under 3,000 | 565 (493,818 damage) | 877 (282,965 damage) |
| judged by which classification brings the player's run nearer the game result | 468 shell, 234 torpedo | |

Nine of the ten sampled same-tick events carry 174 to 3,678 damage and are shells (the game credits the player with no torpedo damage in three of them); the one at 10,096 (KITE_BroadWish, 20 de Julio) is a torpedo. The same-tick override is wrong two times in three. The small-amount events without a shell hit are the same kind of error: a damage tick near a passing torpedo. Together these are 1,442 events and 776,783 damage (0.3% of all credit), which is small in total but it is smoke credit taken from shooters at the moment they fire from smoke.

### 1c. Ships credited torpedo damage

Every ship with ledger torpedo damage also has torpedo damage in the game results, except Goliath: 604 once in two player-runs. The 32 torpedo-less ships (Des Moines, Moskva, Salem, Petropavlovsk, Stalingrad, Kremlin, Vermont, Montana, Ohio, Marseille, Bungo, Sibir, C. Colombo, Utrecht, Prins van Oranje, Willem de Eerste and the rest) have 0 in both columns over 2,000 player-runs. The matcher cannot credit a ship without a torpedo in the water, so this holds by construction; the data confirms it.

### 1d. Proposed tighter rule (not applied)

Three parts, each answering one finding above:

- **R1, a time window instead of the exact clock.** A torpedo fits when its dead-reckoned track passes within 400 m of the victim's last known position at any clock within 12 s before or after the damage clock (today: within 400 m at the damage clock). This recovers the held-position misses like the Chateaurenault case (8 and 10 s) without loosening the distance.
- **R2, a floor on the amount.** A torpedo tick must carry at least 3,000 damage. No torpedo in this field has an alpha under 10,000, and a hit only deals less when the victim had less HP left (a kill), which the 3,000 floor would call a shell; that edge is rare and the kill rule already needs the last event to be a credited shell to count. R2 removes the 1,442 small events (777k).
- **R3, same-tick override only with R2.** A tick that resolved a shell hit becomes a torpedo only when R1 and R2 both hold.

Expected effect: ledger torpedo rises from 27.7 M toward the 33.1 M that the replays actually carry; smoke credit regains about 0.3%. The 11% coverage gap stays and is noted as a limit. The alternative in the review, matching the shooter's own launched salvo, is what R1 already does (the candidates are only the attacker's torpedoes); ending the track at the victim's hit radius is not possible because the view keeps a torpedo to the end of the battle.

I have not changed the rule. Say the word and R1 to R3 go in as one commit with a re-run.

## 2. The ledger about 5% over the game result

### By damage type, field totals

| ledger kind | ledger | game result type | result | ratio |
|---|---|---|---|---|
| shell | 268.0 M | main battery | 252.8 M | 1.060 |
| shell | 268.0 M | main battery plus secondaries | 264.2 M | 1.014 |
| fire | 40.0 M | fire | 40.3 M | 0.993 |
| shell plus fire | 308.0 M | main plus fire | 293.0 M | 1.051 |
| shell plus fire | 308.0 M | main plus secondaries plus fire | 304.5 M | 1.012 |
| torpedo | 27.7 M | torpedoes | 37.0 M | 0.750 |
| flood | 2.6 M | flood | 3.0 M | 0.855 |
| unknown | 13.0 M | ramming 3.2 M, air-support bombs 8.1 M, the torpedo misses | | |
| not in the ledger | | damage to aircraft 16.0 M | | |

The 5.1% is secondaries. The game counts secondary-battery hits in their own fields (`damage_atba_*`, 11.4 M over the field); the ledger has no way to tell a secondary shell from a main-battery one and books every shell hit as `shell`, so the honest comparison for the shell ledger is main plus secondaries, which gives 1.4% over. Fire reconciles on its own (0.7% under).

Per run, with secondaries added to the result: 89 runs within 2%, 121 at 1.02 to 1.10, 38 at 1.10 to 1.25, 71 at 0.90 to 0.98, 22 under 0.90.

### By timing

| | damage | share |
|---|---|---|
| events more than 2 s after the victim's death | 0.19 M | 0.06% of the ledger |
| residual same-attacker, same-victim, same-amount pairs within 0.8 s, shell | 9.8 M | 3.6% of shell; an upper bound, since two shells of one salvo can land with equal damage |
| same, fire | 8.6 M | fire ticks repeat by design; not duplicates |
| same, torpedo | 0.75 M | |

So the remaining 1.4% over on shells (3.7 M) fits inside the residual-duplicate bound; it is the part of the drift that the one-to-one merge cannot resolve, concentrated in the three flagged games and the 1.10 to 1.25 band. Nothing comes from post-death events.

Two consequences for the site, neither applied: the standing check should compare the shell ledger against main plus secondaries (sanity.py; cosmetic), and secondary-battery hits from a ship in smoke are credited as smoke damage today although the definition says main-gun shells. Telling them apart needs the gun type on the resolved shot hit; if the replay carries it, that is a small classifier change. Both wait for your call.

### The three drift games

PN vs HTDOG (ratios 1.30 and 1.30), BTLST vs MZY (1.30 and 1.34) and MANBA vs KM (1.27 and 1.27) now carry `data_quality` in games.csv ("ledger drift: the replay ledger is 1.30 and 1.34 times the game's own shell and fire damage (unmerged duplicate hits between the two replays); smoke damage in this game is overstated"), their smokes are left out of the awards and the Players leaderboard (214 of 218 players remain), and their game pages print the note. The threshold is `LEDGER_RATIO_MAX` = 1.25 in build_site.py and the judgement is one function used by the export and the site. Verified on the export and by rendering the three game pages to a scratch folder; no site built or published. Commits 70f249a6 and 39f93a69.

## 3. Hub mockups

Screenshots taken with headless Edge at 1200 x 900, saved as `smoke/mockups/hub-1-cards.png`, `hub-2-hero.png`, `hub-3-tournament.png` and committed (5f86fd83).

## Correction to STEP 2b

STEP 2b said that none of the no-activation smokes belonged to the replay's own recorder. The check behind that line read a "recorded by" field that the run logs do not carry, so it proved nothing. Re-done from the replay headers: 129 of the 1,547 smokes belong to a primary recorder and every one of them has its activation; 0 of the 99 no-activation smokes do. The statement was right; the evidence was not.

## Appendix: f4check.py output

```
# 1. F4: ledger torpedo damage vs the game's torpedo result, per player per run
player-runs: 6138; with torpedo damage in the game result: 1375
ratio ledger/result over those: median 1.000, mean 0.731; within 10%: 619; under 0.5: 404; over 1.5: 32
field total: ledger torpedo 27,747,728 vs game torpedo 37,011,165 (ratio 0.750)
player-runs with ledger torpedo but none in the result (false positives): 139, damage 272,865
  playoffs_losers-bracket_lb-round-2_mzy-vs-bn_g2_mzy MZY_Inori_Takim Prinz Adalbert: ledger torpedo 11,622; ledger shell 77,727 vs result main 15,562
  playoffs_losers-bracket_lb-round-2_mzy-vs-bn_g2_bn MZY_Inori_Takim Prinz Adalbert: ledger torpedo 10,598; ledger shell 79,246 vs result main 15,562
  groups_group-4_round-4_hfans-vs-inca_g1_hfans INCA_TheUnknow_ St. Vincent: ledger torpedo 9,326; ledger shell 39,787 vs result main 47,017
  playoffs_losers-bracket_lb-round-2_kite-vs-machx_g2_machx KITE_OmishNinja Minotaur: ledger torpedo 9,051; ledger shell 28,478 vs result main 43,347
  groups_group-4_round-2_resin-vs-manba_g1_manba RESIN_Hungria15 Napoli: ledger torpedo 6,418; ledger shell 87,052 vs result main 65,892
  groups_group-2_round-1_btlst-vs-reeee_g1_btlst BTLST_Prime_Min Napoli: ledger torpedo 6,151; ledger shell 49,184 vs result main 23,773
  groups_group-1_round-2_pn-vs-ksc_g1_ksc PN_TheStrategyN Thor: ledger torpedo 5,870; ledger shell 99,138 vs result main 105,609
  groups_group-1_round-2_pn-vs-ksc_g1_pn PN_TheStrategyN Thor: ledger torpedo 5,870; ledger shell 99,138 vs result main 105,609
  groups_group-4_round-2_resin-vs-manba_g1_resin RESIN_Hungria15 Napoli: ledger torpedo 5,610; ledger shell 92,276 vs result main 65,892
  playoffs_winners-bracket_wb-round-1_kite-vs-bn_g1_bn BN_JIJIJIJAKEK Marceau: ledger torpedo 5,235; ledger shell 40,595 vs result main 40,657
player-runs with torpedo damage in the result but none in the ledger (misses): 253, damage 4,835,492
  groups_group-3_round-7_bonky-vs-nga_g1_bonky BONKY_Lalic Somers: result torpedo 118,002; ledger shell 2,482 vs result main 2,482; ledger unknown 39,041
  groups_group-3_round-7_bonky-vs-nga_g1_nga BONKY_Lalic Somers: result torpedo 118,002; ledger shell 2,482 vs result main 2,482; ledger unknown 39,041
  groups_group-3_round-1_sccc2-vs-bonky_g1_sccc2 BONKY_bartimus_ Somers: result torpedo 88,434; ledger shell 3,445 vs result main 3,445; ledger unknown 93,231
  groups_group-4_round-4_hfans-vs-inca_g1_hfans INCA_run_for_yo Chateaurenault: result torpedo 79,757; ledger shell 0 vs result main 0; ledger unknown 34,647
  groups_group-4_round-4_hfans-vs-inca_g1_inca INCA_run_for_yo Chateaurenault: result torpedo 79,757; ledger shell 0 vs result main 0; ledger unknown 34,647
  groups_group-4_round-5_resin-vs-inca_g1_resin INCA_run_for_yo Shimakaze: result torpedo 65,039; ledger shell 3,110 vs result main 3,110; ledger unknown 66,176
  groups_group-1_round-1_kse-vs-pfans_g1_kse PFANS_Akatsukl Chateaurenault: result torpedo 59,017; ledger shell 5,009 vs result main 4,912; ledger unknown 8,716
  groups_group-1_round-4_rsr-vs-uysc_g1_rsr UYSC_DMR7575 Shimakaze: result torpedo 56,725; ledger shell 1,244 vs result main 1,244; ledger unknown 37,143
  groups_group-1_round-4_rsr-vs-uysc_g1_uysc UYSC_DMR7575 Shimakaze: result torpedo 56,725; ledger shell 534 vs result main 1,244; ledger unknown 37,853
  groups_group-3_round-6_nga-vs-machx_g1_machx NGA_Edward_the_ Somers: result torpedo 55,018; ledger shell 0 vs result main 0; ledger unknown 55,421

Worst 10 by absolute gap (ledger minus result):
| run | player | ship | ledger torpedo | result torpedo | gap | ledger shell | result main+sec | ledger unknown |
|---|---|---|---|---|---|---|---|---|
| groups_group-3_round-7_bonky-vs-nga_g1_bonky | BONKY_Lalic | Somers | 0 | 118,002 | -118,002 | 2,482 | 2,482 | 39,041 |
| groups_group-3_round-7_bonky-vs-nga_g1_nga | BONKY_Lalic | Somers | 0 | 118,002 | -118,002 | 2,482 | 2,482 | 39,041 |
| groups_group-4_round-7_inca-vs-manba_g1_manba | INCA_run_for_yo | Chateaurenault | 720 | 110,138 | -109,418 | 1,919 | 1,919 | 108,986 |
| groups_group-3_round-1_sccc2-vs-bonky_g1_sccc2 | BONKY_bartimus_ | Somers | 0 | 88,434 | -88,434 | 3,445 | 3,445 | 93,231 |
| groups_group-4_round-4_hfans-vs-inca_g1_hfans | INCA_run_for_yo | Chateaurenault | 0 | 79,757 | -79,757 | 0 | 0 | 34,647 |
| groups_group-4_round-4_hfans-vs-inca_g1_inca | INCA_run_for_yo | Chateaurenault | 0 | 79,757 | -79,757 | 0 | 0 | 34,647 |
| groups_group-1_round-5_pfans-vs-uysc_g1_pfans | UYSC_DMR7575 | Shimakaze | 391 | 66,404 | -66,013 | 0 | 0 | 46,864 |
| groups_group-4_round-5_resin-vs-inca_g1_resin | INCA_run_for_yo | Shimakaze | 0 | 65,039 | -65,039 | 3,110 | 3,110 | 66,176 |
| groups_group-1_round-6_vrtus-vs-uysc_g1_vrtus | UYSC_DMR7575 | Shimakaze | 17,732 | 79,217 | -61,485 | 0 | 0 | 94,737 |
| playoffs_winners-bracket_wb-round-2_resin-vs-reeee_g2_resin | REEEE_Daka_Daka | Yueyang | 832 | 61,819 | -60,987 | 1,188 | 1,188 | 77,366 |

# 1b. Torpedo-kind events that share a tick with a resolved shell hit
torpedo events: 3641; with a shell hit on the same tick: 702
| run | attacker | ship | victim | amount | ledger torpedo | result torpedo | if this were a shell | verdict |
|---|---|---|---|---|---|---|---|---|
| groups_group-4_round-3_manba-vs-km_g1_km | KM_EmperorFilip | Napoli | MANBA_OkumuraHa | 2,277 | 14,629 | 10,462 | 12,352 | shell |
| groups_group-2_round-4_kite-vs-rmn_g1_rmn | KITE_BroadWish | 20 de Julio | RMN_Tregonsee | 10,096 | 44,660 | 43,010 | 34,564 | torpedo |
| groups_group-4_round-7_resin-vs-bonkz_g1_resin | RESIN_Maddog242 | Gdansk | BONKZ_King_Vipe | 671 | 42,677 | 63,725 | 42,006 | torpedo |
| playoffs_winners-bracket_wb-round-2_kite-vs-epoxy_g1_epoxy | KITE_HariKrishn | Kleber | EPOXY_Your_SAT_ | 660 | 38,597 | 36,883 | 37,937 | shell |
| groups_group-1_round-5_ksc-vs-rsr_g1_rsr | KSC_ZombieGnome | Brisbane | RSR_SkinzMafia | 3,678 | 33,558 | 29,750 | 29,880 | shell |
| groups_group-1_round-6_pn-vs-kse_g1_pn | PN_Thunderussi | Bremen | KSE_CheefBeef | 174 | 26,998 | 38,892 | 26,824 | torpedo |
| playoffs_losers-bracket_lb-round-4_bonkz-vs-htdog_g2_htdog | BONKZ_Dyr3 | Gdansk | HTDOG_Amogussy | 330 | 10,734 | 15,919 | 10,404 | torpedo |
| groups_group-2_round-1_rmn-vs-5d_g1_5d | 5D_lh47383 | San Martin | RMN_Balgair | 1,462 | 2,861 | 0 | 1,399 | shell |
| groups_group-4_round-6_hfans-vs-manba_g1_manba | HFANS_tokai_tei | Jinan | MANBA_Gungnir_4 | 1,159 | 30,268 | 13,975 | 29,109 | shell |
| playoffs_winners-bracket_wb-round-1_kite-vs-bn_g1_bn | BN_JIJIJIJAKEK | Marceau | KITE_latelight | 918 | 5,235 | 0 | 4,317 | shell |
same-tick events, all, judged by the player's run total: {'shell': 468, 'torpedo': 234}

# 1c. Ships credited torpedo damage
| ship | player-runs | ledger torpedo | result torpedo |
|---|---|---|---|
| Chateaurenault | 281 | 5,637,937 | 7,859,931 |
| Somers | 226 | 3,556,582 | 5,505,700 |
| Gearing | 174 | 2,393,349 | 3,061,741 |
| Yueyang | 76 | 1,848,862 | 2,311,774 |
| Shimakaze | 96 | 1,754,974 | 2,278,192 |
| Daring | 156 | 1,552,775 | 1,928,212 |
| Kleber | 152 | 991,272 | 1,688,882 |
| Brisbane | 120 | 899,048 | 1,064,996 |
| Napoli | 230 | 836,489 | 1,063,352 |
| Gdansk | 132 | 828,862 | 1,036,936 |
| Cassard | 34 | 706,234 | 837,332 |
| Marceau | 133 | 693,817 | 760,203 |
| Harugumo | 84 | 507,374 | 725,916 |
| Svea | 130 | 585,183 | 684,464 |
| Grozovoi | 32 | 520,261 | 591,154 |
| Thor | 60 | 503,722 | 584,222 |
| Jinan | 34 | 525,326 | 551,440 |
| Smaland | 78 | 461,523 | 541,412 |
| Delny | 74 | 409,561 | 447,924 |
| Lushun | 44 | 175,602 | 446,864 |
| San Martin | 222 | 401,880 | 423,470 |
| 20 de Julio | 112 | 310,113 | 362,586 |
| Z-42 | 46 | 267,554 | 299,412 |
| La Pampa | 8 | 115,105 | 256,884 |
| Prinz Adalbert | 62 | 201,252 | 192,710 |
| Bremen | 44 | 174,474 | 178,904 |
| Vampire II | 4 | 61,081 | 177,478 |
| St. Vincent | 73 | 99,013 | 171,018 |
| Z-52 | 18 | 119,021 | 161,766 |
| Fuyutsuki | 14 | 92,476 | 134,850 |
| Tromp | 16 | 107,237 | 122,400 |
| Minotaur | 52 | 99,650 | 119,660 |
| Cerberus | 16 | 110,865 | 105,602 |
| Khabarovsk | 26 | 0 | 65,872 |
| G. Hoffmann | 10 | 61,957 | 59,160 |
| Schlieffen | 10 | 19,092 | 46,904 |
| Venezia | 20 | 20,616 | 41,370 |
| Zao | 6 | 0 | 31,820 |
| Smolensk | 13 | 31,920 | 27,794 |
| Brennus | 28 | 27,319 | 24,386 |
| Incomparable | 4 | 19,722 | 18,446 |
| Henri IV | 12 | 18,026 | 18,026 |
| Salem | 140 | 0 | 0 |
| Conqueror | 56 | 0 | 0 |
| Marseille | 216 | 0 | 0 |
| Moskva | 353 | 0 | 0 |
| Stalingrad | 172 | 0 | 0 |
| R. Lauria | 36 | 0 | 0 |
| Bungo | 208 | 0 | 0 |
| Des Moines | 296 | 0 | 0 |
| Ragnar | 64 | 0 | 0 |
| C. Colombo | 66 | 0 | 0 |
| Sibir | 130 | 0 | 0 |
| Montana | 56 | 0 | 0 |
| Vermont | 35 | 0 | 0 |
| Kremlin | 124 | 0 | 0 |
| Petropavlovsk | 226 | 0 | 0 |
| Ohio | 194 | 0 | 0 |
| Wisconsin | 52 | 0 | 0 |
| Sete de Setembro | 18 | 0 | 0 |
| Prins van Oranje | 112 | 0 | 0 |
| Willem de Eerste | 104 | 0 | 0 |
| Monmouth | 2 | 0 | 0 |
| G. Kurfurst | 2 | 0 | 0 |
| Utrecht | 98 | 0 | 0 |
| Libertad | 48 | 0 | 0 |
| Colbert | 2 | 0 | 0 |
| Shikishima | 4 | 0 | 0 |
| Goliath | 2 | 604 | 0 |
| Puerto Rico | 24 | 0 | 0 |
| Bourgogne | 22 | 0 | 0 |
| Worcester | 36 | 0 | 0 |
| Hindenburg | 4 | 0 | 0 |
| F. Sherman | 4 | 0 | 0 |
| Rhode Island | 4 | 0 | 0 |
| Republique | 10 | 0 | 0 |
| A. da Barbiano | 2 | 0 | 0 |
| Irresistible | 2 | 0 | 0 |
| Gouden Leeuw | 8 | 0 | 0 |
| Thunderer | 8 | 0 | 0 |
| Almte. Irizar | 2 | 0 | 0 |
| Sicilia | 4 | 0 | 0 |
| Conte Verde | 22 | 0 | 0 |
| Plymouth | 2 | 0 | 0 |
| Elbing | 2 | 0 | 0 |
| Sevastopol | 4 | 0 | 0 |
ships with ledger torpedo damage and no torpedo damage in any game result: ['Goliath']

# 2. Ledger over the game result, by damage type
ledger by kind: {'shell': '268.0M', 'torpedo': '27.7M', 'fire': '40.0M', 'unknown': '13.0M', 'flood': '2.6M'}
result by type: {'fire': '40.3M', 'main': '252.8M', 'flood': '3.0M', 'torpedo': '37.0M', 'secondaries': '11.4M', 'ram': '3.2M', 'other': '32.4M'}
ledger shell+fire 308.0M vs result main+fire 293.0M: ratio 1.051; vs main+secondaries+fire 304.5M: ratio 1.012
ledger shell 268.0M vs result main 252.8M (ratio 1.060); plus secondaries 264.2M (ratio 1.014)
ledger fire 40.0M vs result fire 40.3M (ratio 0.993)
ledger torpedo 27.7M vs result torpedo 37.0M; ledger flood 2.57M vs result flood 3.01M; ledger unknown 13.0M; result ram 3.18M, other 32.36M
result 'other' fields: {'damage_airdefense': 16005930.0, 'damage_bomb': 8145061.0, 'damage_bomb_airsupport': 8145061.0, 'damage_planes_by_plane': 62274.0}
same-tick torpedo events amount: median 924; under 3,000: 565; under 6,000: 591; 6,000 and over: 111
torpedo events without a shell hit on the tick: 2939; amount median 9,346; under 3,000: 877; under 6,000: 943
no victim position, top misses: [('groups_group-3_round-7_bonky-vs-nga_g1_b', 0, {'DamageClock': 166, 'Salvo': 203, 'ShotHit': 224}), ('groups_group-3_round-7_bonky-vs-nga_g1_n', 0, {'DamageClock': 193, 'Salvo': 113, 'ShotHit': 291}), ('groups_group-3_round-1_sccc2-vs-bonky_g1', 0, {'DamageClock': 255, 'Salvo': 252, 'ShotHit': 199}), ('groups_group-4_round-4_hfans-vs-inca_g1_', 0, {'DamageClock': 259, 'Salvo': 87, 'ShotHit': 264})]

By run, the shell+fire ratio with secondaries added to the result:
{'0.98-1.02': 89, '1.02-1.1': 121, '1.1-1.25': 38, '0.9-0.98': 71, '0-0.9': 22}

# 2b. Timing: events after the victim's death, and residual duplicates
damage after the victim's death (+2 s), by kind: {'fire': '0.01M', 'shell': '0.12M', 'unknown': '0.05M', 'torpedo': '0.01M'} of {'shell': '268.0M', 'unknown': '13.0M', 'fire': '40.0M', 'torpedo': '27.7M', 'flood': '2.6M'}
residual same-amount pairs within 0.8 s (same attacker and victim), by kind: {'shell': '9.78M', 'fire': '8.59M', 'unknown': '1.05M', 'flood': '0.48M', 'torpedo': '0.75M'}
```
