# Site review round 2: torpedoes earn smoke credit; maps draw up to 50

Published 17 Nov 2026, 12:46 EST, from batch `output/20261117-122135` (full field, frames; 341 runs, 0 failures, 1,547 smokes, 103 owner-flagged). Code commits on `full-field`: e455ef11 (torpedo credit, `damage_torpedo` column, sanity check 7 counts torpedoes), 4deb6777 (site builder) and this report. Nothing merged to main; nothing deleted; round 6 stays at `/r6/`. Before means the round 1 batch `output/20261117-104945`.

## 1. The rule

A torpedo now earns smoke credit under the airstrike rule: it is placed where and when the ship launched it; it counts when the launcher stood inside a smoke, or outside, undetected, with the smoke on its line to an enemy in detection range; concealed or detected follows the launcher's spotted state at launch; a sinking whose last hit was a credited torpedo is a kill from smoke. Flooding stays uncredited (as before; say so if it should follow the torpedo the way fires follow shells). Secondaries and unclassified hits stay uncredited and are still listed on the smoke pages as not counted.

Smoke damage is now shell + fire + airstrike + torpedo. The breakdown shows on every smoke page (shells, fires, airstrikes, torpedoes, and "guns only" in brackets), the clan table and clan pages (Guns-only smoke damage per game, Torpedo smoke damage per game, both in the Damage group with percentiles), the players leaderboard (Guns only and Torpedoes columns, sortable), `smokes.json` (shell, fire, airstrike, torpedo, guns per smoke) and `smokes.csv` (`damage_torpedo`). Guns only is shell + fire, the round 6 definition, for comparison with the published round 6 figures.

The ledger's torpedo coverage is a known limit (DESIGN.md section 10: the merged replays classify about 77% of the torpedo damage the game reports), so torpedo credit is a floor.

## 2. Field totals, before and after (two-replay games)

| Measure | Before | After | Change |
|---|---|---|---|
| Smoke damage | 14,876,579 | 15,798,888 | +922,309 (+6.2%) |
| Concealed | 13,791,110 | 14,600,990 | +809,881 (+5.9%) |
| Detected | 1,085,469 | 1,197,898 | +112,428 (+10.4%) |
| Shells | 12,019,506 | 12,019,506 | 0 |
| Fires | 2,653,392 | 2,653,392 | 0 |
| Airstrikes | 203,682 | 203,682 | 0 |
| Torpedoes | 0 | 922,309 | +922,309 |
| Guns only (shells + fires) | 14,672,898 | 14,672,898 | 0 |
| DD damage | 2,249,191 | 2,344,614 | +95,423 (+4.2%) |
| Kills from smoke | 119 | 127 | +8 |
| Smokes with damage | 1,083 | 1,093 | +10 |
| Listed as not counted | 1,629,290 | 706,982 | -922,308 |

Only the torpedo part moved: every shell, fire and airstrike figure is identical to the round 1 batch.

## 3. Concealed smoke damage per game, by clan

All smokes, then destroyer smokes (the default lens on the site). Zero change means the clan fired no credited torpedo from a smoke.

| Clan | Games | Before (all) | After (all) | Change | Before (DD) | After (DD) | Change |
|---|---|---|---|---|---|---|---|
| -BN- | 14 | 74,917 | 74,917 | 0 | 59,530 | 59,530 | 0 |
| INCA | 6 | 65,529 | 69,135 | +3,605 | 54,713 | 58,318 | +3,605 |
| VRTUS | 11 | 61,680 | 68,848 | +7,168 | 38,724 | 40,432 | +1,709 |
| BONKZ | 21 | 61,949 | 68,788 | +6,839 | 50,967 | 56,767 | +5,800 |
| H-SR | 22 | 67,635 | 68,194 | +559 | 65,510 | 66,069 | +559 |
| KSC | 11 | 60,551 | 63,315 | +2,763 | 58,401 | 61,165 | +2,763 |
| HFANS | 17 | 52,722 | 57,059 | +4,338 | 41,311 | 44,616 | +3,305 |
| RESIN | 24 | 51,105 | 55,017 | +3,912 | 47,218 | 50,764 | +3,546 |
| EPOXY | 17 | 49,819 | 50,740 | +921 | 46,529 | 47,450 | +921 |
| HTDOG | 18 | 48,278 | 50,375 | +2,097 | 14,797 | 15,578 | +780 |
| MACHX | 14 | 48,857 | 50,115 | +1,258 | 29,325 | 30,582 | +1,258 |
| BONKY | 7 | 46,557 | 49,585 | +3,028 | 38,563 | 38,563 | 0 |
| SCCC2 | 7 | 45,769 | 48,963 | +3,195 | 26,364 | 26,364 | 0 |
| KM | 5 | 29,311 | 37,737 | +8,426 | 21,566 | 27,900 | +6,334 |
| REEEE | 13 | 33,685 | 36,624 | +2,939 | 32,739 | 35,678 | +2,939 |
| PFANS | 12 | 32,757 | 32,757 | 0 | 27,825 | 27,825 | 0 |
| KITE | 14 | 24,002 | 25,532 | +1,530 | 22,712 | 24,242 | +1,530 |
| BTLST | 6 | 25,010 | 25,010 | 0 | 12,812 | 12,812 | 0 |
| RSR | 7 | 24,207 | 24,207 | 0 | 21,214 | 21,214 | 0 |
| UYSC | 7 | 18,771 | 21,322 | +2,550 | 12,741 | 15,291 | +2,550 |
| KITED | 14 | 20,851 | 20,851 | 0 | 7,095 | 7,095 | 0 |
| NGA | 7 | 18,304 | 20,708 | +2,404 | 12,868 | 12,868 | 0 |
| MZY | 19 | 20,511 | 20,511 | 0 | 18,449 | 18,449 | 0 |
| PN | 7 | 16,319 | 19,989 | +3,670 | 14,064 | 17,734 | +3,670 |
| 5D | 10 | 13,187 | 17,587 | +4,400 | 4,842 | 9,242 | +4,400 |
| MACH | 7 | 14,430 | 14,430 | 0 | 3,290 | 3,290 | 0 |
| OGF | 6 | 9,124 | 11,337 | +2,213 | 9,124 | 11,337 | +2,213 |
| MANBA | 6 | 5,112 | 8,691 | +3,579 | 4,126 | 4,126 | 0 |
| KSE | 7 | 3,801 | 3,801 | 0 | 3,801 | 3,801 | 0 |
| RMN | 6 | 2,216 | 2,216 | 0 | 2,216 | 2,216 | 0 |

The order of the top three changes in the all-smokes view (VRTUS and BONKZ pass H-SR, -BN- stays first); in the destroyer lens the order is the same as before.

## 4. Awards

No award changes a winner in either lens. Smoke of the Tournament stays BN_jordi_92T's Gearing (97,327, no torpedo part); Deepest Cap Smoke stays BONKZ_CheshireZ's Gearing, whose page now reads 88,335 smoke damage and 2 kills (the Bungo sunk by the Brisbane's torpedoes is in its enemies table). Golden Cloud, The Smokefather, Best in Haze, Peekaboo, Radar Bait, Most Selfish Smoke and Most Selfish Smoker keep their winners; Golden Cloud's total is unchanged (HSR_Yamiyonohik fired no credited torpedo).

## 5. The 217 rows (H-SR, RESIN, PN)

217 rows before and after, none added or dropped, one new column (`damage_torpedo`). 8 rows change: each gains torpedo damage (smoke_damage_total, smoke_damage_concealed, damage_not_counted on all 8; in-smoke or behind-smoke parts on 7; dd_damage on 2). Two of them cross 20,000 and gain the damage purpose tag (RESIN 3307 in 7893 g1, whose primary purpose turns from escape to damage, and RESIN 224006 in 8178 g2, island_killer to target_rich with a second shooter); one gains a kill (H-SR 178671 in 7933 g1). Largest single change: 178499 in 7889 g1, 42,256 to 67,211.

## 6. Maps

The auto-switch from the density to the drawn smokes now happens at 50 or fewer (was 25); Mountain Range at 0 to 4 minutes (40 smokes) draws them without forcing the view.

## Verified

- `cargo test -p smoke-signals`: 26 tests pass (the GF G1 H-SR golden test checks smoke timing, not damage).
- `sanity.py`: 341 runs, 0 failures; ledger median 0.997, no run above 1.25 (the per-ship reconciliation still compares guns and bombs only); section 7 (enemies table, torpedoes now counted as credited): 1,538 smokes, 0 mismatches; 196 smokes still list uncounted hits.
- Headless screenshots: the 8144 smoke page (Bungo in the enemies table), Maps at Mountain Range 0 to 4 minutes drawn, the Clans table with the two new Damage columns, the Players leaderboard with Guns only and Torpedoes.
- Live (gh-pages ff524ff, 12:46 EST, files replaced in place): 18 checked addresses return 200 with the same byte size as the local build (hub, every main page, the H-SR clan page, both smoke pages, smokes.json, two map path files, site.js, the round 6 index, a root stub, 404.html); the branch holds 7,868 files, 590 MB, the same as the local build, none missing or differing.

## Links

- https://seanr87.github.io/smoke-signals/smoke/smokes/8144_g2_39540.html
- https://seanr87.github.io/smoke-signals/smoke/clans.html (Damage group: Guns-only and Torpedo per game)
- https://seanr87.github.io/smoke-signals/smoke/players.html
- https://seanr87.github.io/smoke-signals/smoke/maps.html?map=58_RidgeNew&t=0-4
- https://seanr87.github.io/smoke-signals/smoke/about.html
