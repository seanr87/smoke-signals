# Site review round 1: fixed, verified, published

Published 17 Nov 2026, 11:30 EST, from batch `output/20261117-104945` (full field, frames; 341 runs, 0 failures). Code commits on `full-field`: da78b091 (torpedo placement, uncounted hits, sanity check 7), 3c6fd969 (site builder), this report. Nothing merged to main; nothing deleted. Round 6 stays at `/r6/`.

## 1. Enemies table on smokes/8144_g2_39540.html

Cause: no victim was lost. The credited damage events of this smoke (both replays, 61 events after the two unclassified ones) all hit MZY_LOFTILY_IN_'s Prins van Oranje, 58,732, which is the one row and the smoke's total. The second ship was MZY_Hina_Suki's Bungo: BONKZ_Satori_Ma's Brisbane launched torpedoes at 07:41 from inside the smoke; they hit the Bungo at 07:35 for 29,603 and sank it (the Brisbane itself had been sunk 7 s earlier). Torpedo damage never earns smoke credit (DESIGN.md 6.3, the rule approved in STEP 2e), so the enemies table, which lists credited damage, left the Bungo out, and the zoomed frame drew only the two credited fire lines. Before this round the ledger placed a torpedo hit at the moment of impact (the attacker's position then), so nothing recorded that the torpedoes came from this smoke.

Fix (commit da78b091): a torpedo hit is now placed at its launch, like an airstrike at its take-off, so the smokes it was fired from are known. Each smoke records `targets_not_counted` (enemy ships hit from it by the smoker's team with torpedoes, secondaries, flooding or unclassified hits, with the amount by kind and whether the hit was the victim's last), and the page lists them under the enemies table as "not counted". The credit rules, the smoke totals, the enemies table and every metric are unchanged; the page now reads:

- Prins van Oranje (MZY_LOFTILY_IN_): 58,732 concealed, sunk (counted)
- Not counted: Bungo (MZY_Hina_Suki): 29,603 from torpedoes, sunk; Prins van Oranje: 1,419 from unclassified hits

Field-wide check, now section 7 of `smoke/tools/sanity.py`: for every smoke of a two-replay game, the distinct victims of the credited events fired by the smoker's team must equal the rows of the enemies table, and the rows must sum to the smoke's total.

| Check | Result |
|---|---|
| Smokes checked | 1,538 |
| Enemies table misses or adds a victim | 0 |
| Table total differs from the smoke total | 0 |
| Smokes that now list uncounted hits | 231 (1.63M damage, mostly torpedoes) |
| Smoke totals changed against the published batch | 0 of 1,547 |
| Awards changed | none, in either lens |

One side effect, reported for completeness: two zero-damage smokes change their smoke-deaths count (PN_FiftyForATwe Harugumo at 06:58 in PN vs HTDOG, 1 to 0; KITE_Destroyer_ Z-52 at 12:08 in LB round 4, 0 to 1), because "firing from behind the smoke" now tests a torpedo at its launch instead of at its impact. No other column of any smoke differs.

## 2. Maps page

- The density now follows every filter: map, clans, ships, player, purpose, spawn, smoker class, smoke type and the elapsed-time range (two handles, 0 to 20 minutes, 1-minute steps). It is computed in the browser from the smoke origins the filters leave.
- With 25 or fewer smokes left, the map switches to the smokes themselves: the cloud (the puffs' footprint), the path while laying and an arrow at its end, in the clan's colour, each a link to the smoke's page. The View switch forces either picture; "N of M smokes" updates live, per map and in total.
- One filter bar drives all seven maps; the Map filter shows one map. The side charts cover the smokes shown and, when clans are picked, those clans only.
- Mountain Range, 0 to 4 minutes, holds 40 smokes in the data, not 13 (14 in the first minute, 9, 17, 15 in the next three), so it stays a density; forcing "smokes" draws the 40. With two clans added it drops under 25 and draws automatically. Links: https://seanr87.github.io/smoke-signals/smoke/maps.html?map=58_RidgeNew&t=0-4 and https://seanr87.github.io/smoke-signals/smoke/maps.html?map=58_RidgeNew&t=0-4&view=smokes
- The smoke pages' "its path on the map" link still works (map, clan and the smokes view, scrolled to the smoke).

## 3. Multi-select filters

Clans and Ships are checkbox lists with a search box and a clear link on the Smokes and the Maps page; nothing ticked means all. Selections live in the address bar: `?clan=H-SR,RESIN&ship=Somers,Gearing` on both pages, plus `t=0-4` (minutes), `map`, `player`, `purpose`, `spawn`, `cls`, `type`, `view` on Maps and every single select on Smokes. Old links (`team=`, `from=`/`to=` in seconds) still resolve. Example: https://seanr87.github.io/smoke-signals/smoke/smokes.html?clan=H-SR,RESIN&ship=Somers,Gearing (71 smokes).

## 4. Clans page (add-on)

- Record columns after the clan: Games, W-L, Win %, then Smokes; all sortable (W-L sorts by wins, ties by win rate).
- Percentiles: every metric cell carries the clan's percentile against the other clans with 7 or more games (24 clans in the base; ties count half). Clans under 7 games are ranked against that base, greyed and marked "small sample". The Values / Percentiles switch above the table (also `?mode=pct`) swaps what the cell shows and what its tooltip holds; sorting always uses the value. Cells are shaded by percentile in one steel-blue ramp, light to strong. The page note says a high percentile is not always good.
- New metric for the strip: First smoke (seconds elapsed, mean of each game's first smoke in the lens), in the Volume group.
- Tendency strip on each clan page, for the lens chosen above it: percentiles for smokes per game, first smoke, stacked share, selfish share, cap-contest share, concealed damage per game, smoke deaths per game and radar spots per game, with a word at the 80th or above and the 20th or below (prolific / sparing, late / early, stacker / spread, selfish / sharing, cap-focused / off-cap, lethal / quiet, exposed / safe, radar-hunter / radar-shy). H-SR reads early, sharing, lethal, safe, radar-hunter.
- clans.html grew from 341 KB to 683 KB (the percentiles for every lens are inline).

Percentile against win rate (report only; association, not proof). Pearson r between a metric's percentile and win % over the 24 clans with 7 or more games:

| Lens | Metric | r | n |
|---|---|---|---|
| destroyer smokes (default) | Score swing while smoke up | +0.77 | 24 |
| destroyer smokes | Smokes near a cap capture | +0.67 | 24 |
| destroyer smokes | Concealed smoke damage per game | +0.60 | 24 |
| all smokes | Score swing while smoke up | +0.75 | 24 |
| all smokes | Smokes near a cap capture | +0.74 | 24 |
| all smokes | Concealed smoke damage per game | +0.62 | 24 |

Next in line: smoke damage per game +0.55 and selfish smoke share -0.54 (destroyer lens; -0.61 in the all-smokes lens). Score swing and cap captures are partly the win itself measured during the smoke, so the top two say little; concealed damage per game is the one worth watching.

## Verified

- `cargo test -p smoke-signals` passes (the GF G1 H-SR reference).
- `sanity.py` on the new batch: 341 runs, 0 failures, 1,547 smokes, ledger median 0.997, no run above 1.25; reference diff against the published batch: 1 of 217 H-SR/RESIN/PN rows changed (the PN smoke-deaths row above); section 7 clean.
- Headless screenshots, all rendered as intended: the fixed smoke page, Maps at Mountain Range 0 to 4 minutes, Maps with three clans (heat map), Smokes with two clans and two ships, Clans in Values and in Percentiles mode, the H-SR clan page with its tendency strip.
- Live (gh-pages a2ff840, frames replaced in place, no second copy): 18 checked addresses (hub, every main page, the H-SR clan page, both smoke pages above, smokes.json, two map path files, site.js, the round 6 index, a root stub and 404.html) return 200 with the same byte size as the local build; the branch holds 7,868 files, 590 MB, the same as the local build with none missing or differing. The served pages lagged the push by about two minutes.

## Links to check

- Fixed smoke page: https://seanr87.github.io/smoke-signals/smoke/smokes/8144_g2_39540.html
- Maps, Mountain Range 0 to 4 min: https://seanr87.github.io/smoke-signals/smoke/maps.html?map=58_RidgeNew&t=0-4 (add `&view=smokes` to draw the 40)
- Maps, three clans, heat map: https://seanr87.github.io/smoke-signals/smoke/maps.html?clan=H-SR,RESIN,BONKZ
- Smokes, two clans and two ships: https://seanr87.github.io/smoke-signals/smoke/smokes.html?clan=H-SR,RESIN&ship=Somers,Gearing
- Clans, values: https://seanr87.github.io/smoke-signals/smoke/clans.html ; percentiles: https://seanr87.github.io/smoke-signals/smoke/clans.html?mode=pct
- Clan page: https://seanr87.github.io/smoke-signals/smoke/clans/H-SR.html (clan pages are named by tag; the address is case-sensitive on GitHub Pages)
- About (method note on uncounted hits): https://seanr87.github.io/smoke-signals/smoke/about.html
