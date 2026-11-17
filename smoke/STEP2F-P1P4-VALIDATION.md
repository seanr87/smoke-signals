# STEP 2f: P1 to P4 applied, validation run, STOP

Date: 16 Nov 2026. Batch `output/20261116-210053` (no frames, 341 runs, 30 clans), compared with `output/20261116-172047` (R1 to R3, no frames), `output/20261116-161621` (F4, frames) and round 6 `output/20261104-180332`. Script: `smoke/tools/validate_p.py`.

Commits: 6396a33d (P1), 762decae (P2), 03eeb810 (P3), 07d22067 (P4), plus this report with DESIGN.md, sanity.py and the site's kind line.

## Result: three of the six pass criteria fail, and P1 gives up 7.3% of torpedo damage. Nothing tuned further; the frames batch was not run.

| Criterion | Target | Result | |
|---|---|---|---|
| False positives (ledger torpedo on a ship with no torpedo damage in the result) | at most 139 player-runs, 273k | 9 player-runs, 13,060 | PASS |
| Torpedo ledger | at most 33.1M | 22.95M | PASS, but see the misses |
| Overreach (ledger torpedo more than 10% over the result) | at most 40 player-runs, under 0.5M | 53 player-runs, 734k | FAIL |
| Secondary ledger against the game's secondaries | within 10% | 1.167 | FAIL |
| Shell ledger against the game's main battery | within 3% | 1.016 | PASS |
| P1 torpedo damage given up | under about 1% | 7.27% (1.67M of 22.95M) | FAIL |

Kills from smoke: 118 field-wide (F4 frames batch 120, R1 to R3 run 114); H-SR 12, RESIN 11, PN 0 in all three.

## 1. Torpedoes

| | R1 to R3 run | P1 to P4 run |
|---|---|---|
| Ledger torpedo | 32.79M | 22.95M |
| Game result torpedo | 37.01M | 37.01M |
| False positives | 104 player-runs, 644k | 9 player-runs, 13k |
| Misses (result torpedo, ledger none) | 156 player-runs, 2.41M | 476 player-runs, 7.30M |
| Player-runs within 10% of the result | 777 of 1,375 | 428 of 1,375 |
| Median ledger over result | 1.000 | 0.579 |

The false positives are gone (the largest left is a Brennus with 9,109; the rest are under 1,000), but the victim-aware floor rejects a large share of real hits. The torpedo ledger lost 9.8M: Chateaurenault 3.36M (ledger 3.19M against a result of 7.86M), Somers 0.59M, Gearing 0.46M, Napoli 0.46M, San Martin 0.38M, Thor 0.34M, Daring 0.33M, Shimakaze 0.32M.

Where it went: the rejected hits are now `unknown` (field unknown rose from 10.75M to 16.58M). Chateaurenault's accepted torpedo ticks sit at 9k to 15k; its rejected non-tick unknown events sit at 5k to 9k (330 events, 3.3M), the size of a hit on a ship with torpedo protection. A diagnostic run on H-SR vs SCCC2 g1 shows the torpedo protection lookup works (every ship has a value: Ohio 0.37, R. Lauria 0.39, Libertad 0.31, Utrecht 0.19, destroyers 0), so the loss is the share itself: real hits land well under 0.8 of the listed damage after protection. For torpedo boats (result main battery 0, 214 player-runs) the non-tick events the floor rejected sit at 0.25 to 0.8 of the run's largest accepted torpedo tick (87 events), and 517 small ticks under 0.25 are the flood trains those misses orphaned.

The overreach is 53 player-runs and 734k. The worst ten are a Napoli (42,860 against 10,119: one 32,780 tick that the P1 table below also lists), a Shimakaze that fired no guns at all (111,677 against 79,217, so the excess is the ledger, not the classification), two Somers, a San Martin, a Daring and a Smaland. With the false positives gone the overreach that remains is mostly the ledger carrying more than the game's result, which the classification cannot change.

## 2. P1: ticks with a resolved shell hit

197 events fit a torpedo track but carry a resolved shell hit and are shells now: 1,668,340, 7.27% of the torpedo ledger after the run. By amount: 78 events under 3,000 (60k), 14 at 3k to 8k (81k), 79 at 8k to 15k (900k), 18 at 15k to 25k (336k), 8 above 25k (291k).

Largest ten (each event appears once per perspective):

| amount | run | attacker | ship | victim | clock s |
|---|---|---|---|---|---|
| 43,680 | lb-round-4 bonkz-vs-htdog g2 | HTDOG_Miami_Mat | Thor | BONKZ_Embeddedd (Conqueror) | 825 |
| 42,563 | group-4 round-6 hfans-vs-manba g1 | HFANS_j_i_u_m_i | Thor | MANBA_Gungnir_4 (Willem de Eerste) | 397 |
| 34,671 | group-1 round-2 uysc-vs-htdog g1 | HTDOG_Forbidden | Thor | UYSC_Rugal4721 (C. Colombo) | 373 |
| 32,780 | lb-round-1 machx-vs-vrtus g2 | VRTUS_LightTheB | Napoli | MACHX_DrobotPri (Brennus) | 757 |
| 25,569 | group-4 round-3 manba-vs-km g1 | MANBA_Your_Soci | San Martin | KM_theJoker117 (San Martin) | 479 |
| 24,491 | wb-round-1 mzy-vs-machx g3 | MACHX_SPAAAAAAA | Grozovoi | MZY_Hina_Suki (Sibir) | 400 |

The Thor 43,680 and 42,563 are main-battery AP salvos (the game credits those Thors no torpedo damage in those games, or far less than the tick). The 8k to 15k band, 900k over 79 events, is the size of a torpedo hit and is the real cost of P1: destroyers that shoot and launch at the same target lose their torpedo hits that land on a shell tick.

## 3. Secondaries and shells

| | R1 to R3 run | P1 to P4 run | game result |
|---|---|---|---|
| shell | 248.37M | 256.69M | main 252.76M |
| secondary | 18.19M | 13.35M | secondaries 11.44M |
| fire | 38.57M | 39.53M | 40.27M |
| airstrike | 0 | 0.48M | 8.15M |
| unknown | 10.75M | 16.58M | |

Shell over main 1.016 (pass). Secondary over secondaries 1.167 (fail). P3 removed the salvo-fallback secondaries (every secondary event now comes from a resolved shot hit, 14,703 events). What remains: a damage tick is matched to the first resolved hit within 1 s of it, and on a battleship a secondary shell lands within 1 s of almost every main-battery hit, so a main-battery tick can be labelled with the secondary hit's projectile. Ohio in PN vs UYSC: ledger 127 mm 42,796 against a result of 7,797 secondaries, while its 457 mm total is short by the same order. Excess by ship: Sibir +876k over 130 player-runs, Ohio +167k, Prinz Adalbert +97k, Marseille +94k, St. Vincent +92k.

Per-run bands of ledger shell plus secondary plus fire plus airstrike over the result's main plus secondaries plus fire plus bombs: under 0.9: 31; 0.9 to 0.98: 91; 0.98 to 1.02: 104; 1.02 to 1.1: 97; 1.1 to 1.25: 18; above 1.25: 0.

## 4. Airstrikes (P4)

The rule as built: an air-support squadron (plane category `airsupport`) of the attacker's in flight, from 5 s after it appears on the minimap to 10 s after it leaves, with its interpolated position within 1,500 m of the victim, and the tick above one main-battery shell's listed damage. The squadron packet names no launching ship, so the owner is the one ship of the squadron's team whose ship param carries the squadron param's ship name (`PHAD020_AS_UTRECHT` and `PHSC520_Utrecht`).

Field-wide: ledger airstrike 481,782 against 8,145,061 of `damage_bomb_airsupport` in the game's results (6%). All of it is Utrecht; no ship is credited airstrike without airstrike damage in its result, and no player-run exceeds its result. Smoke-credited airstrike damage: 50,414 (REEEE 22,745, VRTUS 9,449, RESIN 5,954, EPOXY 4,554, INCA 4,554, KSC 3,158).

Utrecht and Gouden Leeuw player-runs (106): ledger shell 6.58M against result main 4.89M, unknown 1.15M, airstrike 0.48M; result bombs 2.93M. Shell plus airstrike plus unknown over main plus bombs is 1.051, so the bombs are in the ledger: about 1.7M of them are still counted as main-battery shells (the salvo fallback) and 1.15M as unknown.

HSR_VoyagingSta (Utrecht): shooter credit before 572,720, after 572,720: shell 474,792, fire 97,928, airstrike 0. His ledger airstrike is 40,168 against a result of 378,778 over 20 player-runs. His largest smoke credits (29456 EPOXY g1 61,881; 29463 41,351; 39292 GF g1 38,553) are unchanged.

Diagnostic run (H-SR vs SCCC2 g1, HSR_VoyagingSta's Utrecht, result bombs 22,348): the three bomb-sized ticks without a resolved hit are 9,108 at 481.9 s, 6,230 at 780.2 s and 3,898 at 1,215.7 s, each 15.6 to 15.9 s after its squadron appeared, and each with the squadron 1,946 to 2,367 m from the victim at the damage clock. The squadron passed within 155 m of the victim 4.6 s earlier and flew on, so the position test at the damage clock misses the drop. All three went to the salvo fallback as shells. The 1,500 m tolerance is the wrong shape of test; the amount test (above 3,100, one Utrecht HE shell) would have passed all three.

Owner inference: 944 squadrons got a single owner, 1,612 did not. In the diagnostic game the unowned squadrons are `PHAD015_PRINS_V_O_AS` (Prins van Oranje) and `PHAD023_WILLEM_DE_EERSTE_AS` (Willem de Eerste): the Dutch battleships' squadron params put `_AS` at the end and abbreviate the name, so the `_AS_` key matches Utrecht only. Gouden Leeuw, Prins van Oranje and Willem de Eerste strikes are therefore never classified, which is where most of the gap between 0.48M and 8.15M lies (Utrecht and Gouden Leeuw alone account for 2.93M of the result's bombs). No ASW squadron appeared in this game.

## 5. Original 217 rows against round 6

17 of 217 rows changed in damage or flag columns (42 state columns are empty in a no-frames run and were skipped):

- Five are the F2 owner_flag true to false rows (RESIN_thepregna Svea x4, HSR_Yuzuriha_Ou Svea), unchanged since STEP 2c.
- Seven lose or gain shell credit of 300 to 6,000 where the salvo fallback (P3) or the resolved-hit rule (P1) moved a tick: 178501 RESIN_Fryce Somers 37,622 to 36,434; 178502 RESIN_Hungria15 Napoli 9,159 to 5,574 (damage_label island_killer to hunt); 174224 PN_Sean_O_Reill Harugumo 54,400 to 52,384; 27151 RESIN_Fryce Harugumo 60,967 to 60,373 (the 41,812 of STEP 2e is back near round 6, since its torpedo-sized tick on a resolved hit is a shell again); 97311 PN_FiftyForATwe Somers 17,105 to 14,459; 180816 RESIN_eagle_lan Gdansk 974 to 660; 178679 HSR_Arona_daisu Harugumo (enemy columns only).
- 190362 RESIN_thepregna Svea 12,977 to 16,804 and 90088 HSR_Apex_captai Conte Verde 11,550 to 16,500 (fire 0 to 4,950): ticks that R1 to R3 called torpedo or flood are shells and fire again under the new floor.
- 176003 RESIN_Big_Boy69 Somers: total 50,141 unchanged; RESIN_triarch's Utrecht gets a 5,954 airstrike credited from behind the smoke (the one airstrike credit on an original row) and its 10,179 of fire ticks now follow the airstrike instead of an earlier shell fired from inside, so 16,138 moved from inside to behind.
- 195445 PN_FiftyForATwe Harugumo: smoke_deaths 0 to 1; this dates from the F4 frames batch (STEP 2c), not from this step.

HSR_VoyagingSta's shooter total: unchanged in every one of his smokes (no airstrike credit landed on them).

Smoke of the Tournament: the top 4 are unchanged (BN_jordi_92T Gearing 97,327; PFANS_Mugu_9 Harugumo 96,006; HSR_Yamiyonohik Somers 90,686; BN_jordi_92T Somers 89,662). EPOXY_Your_SAT_ Somers rises from 84,328 to 88,882 (5th), BN_jordi_92T Somers WB round 1 enters 6th at 83,433, RESIN_Big_Boy69 Somers 80,375 is 7th, KSC__Sait Gdansk 77,484 enters 8th; EPOXY_Your_SAT_ Shimakaze (77,031) and BONKY_Lalic Somers (74,771) drop out.

Per-clan concealed per game, before to after: -BN- 87,202 to 89,312 (+2.4%); KSC 65,011 to 69,521 (+6.9%); H-SR 67,671 to 67,832 (+0.2%); INCA 65,529 unchanged; VRTUS 61,420 to 62,790; BONKZ 61,228 to 61,949; HFANS 50,930 to 52,722; MACHX 48,508 to 52,214 (+7.6%); RESIN 51,078 to 51,876 (+1.6%); EPOXY 49,551 to 49,819; SCCC2 45,297 to 48,915 (+8.0%). The rises are shell damage that R1 to R3 had called torpedo and the floor now returns to shells.

## 6. Proposals (nothing applied)

- P5, torpedo floor share: 0.5 instead of 0.8 of the listed damage after protection (finishing hits still excepted). Evidence: Chateaurenault's accepted ticks sit at 9k to 15k and its rejected ones at 5k to 9k; torpedo boats' rejected hits sit at 0.25 to 0.8 of the largest accepted tick. The floor's purpose (keeping 3k to 8k shell salvos out) survives for destroyers, whose shells list at 2,000 to 3,400; cruisers with large shells (Napoli, San Martin) would need the validation to show whether 0.5 lets salvos back in.
- P6, resolved-hit ticks: a tick with a resolved shell hit stays a shell unless its amount is both at or above the torpedo floor and above the ship's largest main-battery salvo (guns times the largest shell's listed damage), in which case it is a torpedo. This keeps the Thor and Napoli salvos (43,680 against a Thor salvo of about 100k; 32,780 against a Napoli salvo of about 50k) as shells and gives back torpedo hits on destroyers whose whole salvo lists under 8k (Shimakaze, Somers, Chateaurenault), most of the 900k in the 8k to 15k band. Six-gun destroyers (Gearing, Daring) with 12k salvos keep losing hits under 12k.
- P7, secondary labelling: among the resolved hits within 1 s of a tick, take the main-battery hit when there is one; a tick is secondary only when every resolved hit within 1 s is a secondary's. Expected to remove the Ohio-type excess (127 mm labelled on main-battery ticks) and bring the secondary ledger inside 10%.
- P8, airstrikes: (a) owner key: compare the squadron param's name with the `_AS` or `AS_` token removed, and accept an abbreviated match where each token is a prefix of the ship key's token (`PRINS_V_O` against `PRINS_VAN_ORANJE`); (b) the hit test becomes a pass test like the torpedoes': the squadron's interpolated track within 1,000 m of the victim at some clock in the 10 s before the damage, the amount still above one main-battery shell's listed damage. In the diagnostic game this matches all three bomb ticks (19,236 of the 22,348 result).
- The ledger duplicates behind the Shimakaze-type overreach (ledger 111,677 against a result of 79,217 on a ship that fired no gun) are a merge question, not a classification one, and are left as they are.

Each would be its own commit, followed by a no-frames run and the same six checks plus the P1 give-up and the airstrike ledger against the result.

## Files

- Code: `crates/smoke-signals/src/damage.rs` (P1 to P4 classification, `AirstrikeTrack`, `ShellHitFittingTorpedo`, `damage_airstrike`, `by_kind` on shooters), `analysis.rs` (torpedo damage and protection from game params, plane tracking and owner inference), `tier2.rs` (`torpedo_protection`), `output.rs` (`damage_airstrike` column).
- Tools: `smoke/tools/validate_p.py` (this report's checks), `smoke/tools/sanity.py` (section 1 now counts airstrikes and air-support bombs), `smoke/tools/build_site.py` (airstrikes on the game page's kind line).
- `smoke/DESIGN.md`: sections 6.2, 6.3 and 10 updated for P1 to P4.
