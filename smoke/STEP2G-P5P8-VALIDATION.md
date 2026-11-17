# STEP 2g: P5 to P8 applied, final tuning round, two gates missed

Date: 16 Nov 2026. Validation batch `output/20261116-213623` (no frames, 341 runs, 30 clans), compared with `output/20261116-210053` (P1 to P4), `output/20261116-161621` (F4, frames) and round 6 `output/20261104-180332`. Script: `smoke/tools/validate_p.py`. The frames batch for the site follows this report (see the end).

Commits: 429637bc (P5), 526a26ef (P6), c91d4a68 (P7), 8e01f868 (P8).

## Gates

| Gate | Target | Result | |
|---|---|---|---|
| False positives (ledger torpedo on a ship with no torpedo damage in the result) | at most 139 player-runs, 273k | 11 player-runs, 35,032 | PASS |
| Torpedo ledger | 30M to 33.1M | 28.39M | FAIL, short by 1.6M |
| Secondary ledger against the game's secondaries | within 10% | 0.974 | PASS |
| Shell ledger against the game's main battery | within 3% | 1.012 | PASS |
| Airstrike ledger against the game's air-support bombs | at least 80% | 44.4% | FAIL |
| Every Dutch ship with bombs in the result has airstrike in the ledger | all | Utrecht 66%, Tromp 66%, Prins van Oranje 45%, Willem de Eerste 23%, Gouden Leeuw 14% | PASS |
| Kills from smoke H-SR / RESIN / PN | unchanged or explained | 12 / 11 / 0, unchanged | PASS |

Both misses are written into `smoke/DESIGN.md` section 10 as known limits with their size. No further tuning.

## 1. Torpedoes

| | P1 to P4 run | P5 to P8 run |
|---|---|---|
| Ledger torpedo | 22.95M | 28.39M |
| Game result torpedo | 37.01M | 37.01M |
| Ceiling (ledger torpedo plus unknown on torpedo scorers) | 31.40M | 32.12M |
| False positives | 9 player-runs, 13k | 11 player-runs, 35k |
| Misses (result torpedo, ledger none) | 476 player-runs, 7.30M | 289 player-runs, 4.43M |
| Player-runs within 10% of the result | 428 of 1,375 | 675 of 1,375 |
| Median ledger over result | 0.579 | 1.000 |

The 0.5 floor brought back 5.4M and the median player-run is back at 1.0, but the field total is 28.4M, 77% of the game's 37.0M and 1.6M short of the 30M gate. What the replays carry at all is about 32M (the ceiling), so the remaining gap is split between the floor (misses 4.43M, half of them hits under half the listed damage) and the resolved-hit rule (P6 gives up 1.73M, 6.1%: 222 events, led by the Thor and Napoli salvos that are shells by right and a tail of destroyer hits under their ship's whole-salvo size).

Report only: overreach is 76 player-runs and 1.02M; 12 of those, 196k, are torpedo boats that fired no gun (UYSC_DMR7575's Shimakaze 111,677 against 79,217 in both perspectives), where the ledger itself holds more than the result. The largest single case is still VRTUS_LightTheB's Napoli at 42,860 against 10,119 (a 32,780 tick on a resolved hit that is under a Napoli salvo and stays a shell; the excess is elsewhere in that run).

## 2. Secondaries and shells

| | P1 to P4 run | P5 to P8 run | game result |
|---|---|---|---|
| shell | 256.69M | 255.79M | main 252.76M |
| secondary | 13.35M | 11.14M | secondaries 11.44M |
| fire | 39.53M | 39.81M | 40.27M |
| airstrike | 0.48M | 3.62M | 8.15M |
| unknown | 16.58M | 10.26M | |

Shell over main 1.012; secondary over secondaries 0.974; shell plus fire plus airstrike over main plus fire plus bombs 0.993. Per-run bands of ledger over result (shell, secondary, fire, airstrike against main, secondaries, fire, bombs): under 0.9: 25; 0.9 to 0.98: 101; 0.98 to 1.02: 102; 1.02 to 1.1: 97; 1.1 to 1.25: 16; above 1.25: 0.

## 3. Airstrikes

Field-wide: ledger airstrike 3,618,656 against 8,145,061 of `damage_bomb_airsupport` (44.4%). Every Dutch ship now has an owner key (2,086 squadrons with an owner, 470 without), nobody is credited airstrike without bombs in the result, and six player-runs exceed their result by more than 10% (29k in all).

| Ship | result bombs | ledger airstrike | share |
|---|---|---|---|
| Willem de Eerste | 2,766,282 | 634,746 | 23% |
| Utrecht | 2,743,398 | 1,814,030 | 66% |
| Prins van Oranje | 2,220,929 | 991,757 | 45% |
| Tromp | 232,190 | 153,438 | 66% |
| Gouden Leeuw | 182,262 | 24,684 | 14% |

Where the rest is: Willem de Eerste's shell ledger is 1.12 times its main-battery result and its unknown is 1.09M; Utrecht's shell ledger is 1.18 times its main battery; Gouden Leeuw's 1.51. Bombs still sit in shells (the salvo fallback) and in unknown. The rule keeps a tick as a shell when it is at or under one main-battery shell's listed damage, and the battleships' shells list at 5,750 (Prins van Oranje) and 13,700 (Willem de Eerste), above most bomb ticks; that floor is what holds the battleships at 23% and 45%.

Smoke-credited airstrike damage: 203,682, 5.6% of the ledger airstrike (REEEE 90,567, EPOXY 40,724, RESIN 25,257, VRTUS 18,898, H-SR 6,230, KITE 6,104, -BN- 4,774, INCA 4,554). Most strikes are called from outside any smoke while the ship is spotted, so they earn nothing.

HSR_VoyagingSta (Utrecht): shooter credit 572,720 before, 563,826 after: shell 459,668, fire 97,928, airstrike 6,230. The one airstrike credit is smoke 144965 (H-SR vs SCCC2 g1): 34,171 = shell 14,893, fire 13,048, airstrike 6,230. The 8,894 he lost is in HSR_Yamiyonohik's Delny smoke 3188 (WB round 3 vs EPOXY g2): bomb ticks that the salvo fallback had credited as shells are airstrikes now, credited at the launch moment, when the Utrecht was outside the smoke.

## 4. Kills from smoke

121 field-wide (P1 to P4 run 118, F4 frames batch 120). H-SR 12, RESIN 11, PN 0 in every run.

## 5. Original 217 rows against round 6

21 of 217 rows changed in damage or flag columns (42 state columns are empty in a no-frames run and were skipped):

- Five are the F2 owner_flag true to false rows (RESIN_thepregna Svea x4, HSR_Yuzuriha_Ou Svea), unchanged since STEP 2c.
- Torpedo ticks that round 6 counted as shells: 159292 RESIN_Maddog242 Harugumo 60,967 to 41,812 (an 18,388 torpedo and its flood on HSR_Klee_Fleein at 603 s, the same figure as STEP 2e); 3188 HSR_Yamiyonohik Delny 50,580 to 41,686 (VoyagingSta's 8,894, see above, airstrike not torpedo); 190362 RESIN_thepregna Svea 12,977 to 16,804 and 90088 HSR_Apex_captai Conte Verde 11,550 to 16,500 (fire 0 to 4,950), where R1 to R3 had called shells and fires torpedo and flood and the floor returns them.
- Secondary hits that round 6 counted as main-battery shells: 178502 RESIN_Hungria15 Napoli 9,159 to 6,210 (2,949 of secondary, damage_label island_killer to hunt); 178501 RESIN_Fryce Somers 37,622 to 36,434; 174224 PN_Sean_O_Reill Harugumo 54,400 to 52,384; 27151 RESIN_Fryce Harugumo 60,967 to 60,373; 97311 PN_FiftyForATwe Somers 17,105 to 14,459; 180816 RESIN_eagle_lan Gdansk 974 to 660; 178679 HSR_Arona_daisu Harugumo and 39294 RESIN_eagle_lan Gdansk (enemy columns only).
- Airstrike credit on the same smoke, total unchanged: 144965 HSR_Yamiyonohik Delny (damage_shell 21,123 to 14,893, the 6,230 is airstrike); 176008 RESIN_Big_Boy69 Somers (damage_shell 20,905 to 17,179); 176003 RESIN_Big_Boy69 Somers (total 50,141; RESIN_triarch's Utrecht strikes and their fires are credited from behind the smoke at launch instead of inside, so inside/behind moved from 47,775/2,367 to 16,058/34,083).
- 195445 PN_FiftyForATwe Harugumo smoke_deaths 0 to 1: from the F4 frames batch (STEP 2c), not this step.

## 6. Smoke of the Tournament and per-clan concealed per game

Top 8 after: 1. BN_jordi_92T Gearing 97,327 (Group 3 R6 vs SCCC2); 2. PFANS_Mugu_9 Harugumo 96,006 (Group 1 R1 vs KSE); 3. HSR_Yamiyonohik Somers 90,686 (Group 3 R3 vs -BN-); 4. BN_jordi_92T Somers 89,662 (LB R1 vs KSC g2); 5. EPOXY_Your_SAT_ Somers 88,882 (Group 4 R4 vs MANBA); 6. RESIN_Big_Boy69 Somers 80,375 (GF R1 vs H-SR g2); 7. EPOXY_Your_SAT_ Shimakaze 77,031 (Group 4 R3 vs BONKZ); 8. BONKY_Lalic Somers 74,771 (Group 3 R7 vs NGA). Against the P1 to P4 run, BN_jordi_92T's Somers WB round 1 (83,433) and KSC__Sait's Gdansk (77,484) drop out: their torpedo-sized ticks are torpedoes again at the 0.5 floor. Against the R1 to R3 run (STEP 2e) the list is the same except EPOXY_Your_SAT_'s Somers rising from 84,328 to 88,882.

Per-clan concealed per game, P1 to P4 run to this run: -BN- 89,312 to 88,963; KSC 69,521 to 67,918; H-SR 67,832 to 67,635; INCA 65,529; BONKZ 61,949; VRTUS 62,790 to 61,680; HFANS 52,722; RESIN 51,876 to 51,105; EPOXY 49,819; MACHX 52,214 to 48,857 (-6.4%); HTDOG 48,504 to 48,278; SCCC2 48,915 to 45,769 (-6.4%); REEEE 30,153 to 33,685 (+11.7%, its Utrecht's airstrikes); KM 32,090 to 29,311 (-8.7%); 5D 11,702 to 13,187 (+12.7%); MANBA 8,252 to 5,112 (-38%, six games, one torpedo-sized tick); PN 16,319 unchanged. Against round 6: H-SR 67,832 to 67,635, RESIN 51,866 to 51,105, PN 16,598 to 16,319.

## Frames batch

Batch `output/20261116-214739`: 341 runs, 0 failures, 1,547 smokes, 103 flagged, 807 s wall time, frames on, no clips. Every value the no-frames validation run carried is identical in it (0 differing cells over 1,547 rows outside the state columns); the figures above are the site's figures. Standing check (`sanity.py`): ledger shell plus secondary plus fire plus airstrike over the result's main plus secondaries plus fire plus bombs has a median of 0.997 and a mean of 0.995 over 341 runs, with 239 runs outside 2% (113 over, 126 under) and no run above 1.25; 1,538 smokes seen in both perspectives, 9 one-sided, 4 inferred owners. The data export is `output/20261116-214739/smoke-signals-data-r7.zip` (1,547 smokes, 171 games). smokes.csv, run_log.md, jobs.json and the zip are committed. The site is not built or published.
