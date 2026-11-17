# Smoke Atlas: content package

Everything a designer needs to lay out the Smoke Atlas: the copy, the spots as data, the maps, and working figures to redraw from. The analysis behind it is in `smoke/analysis/round3/` and `smoke/analysis/round4/`; this folder only assembles it and adds the per-map pages.

Commit: analysis and atlas content committed on full-field as 0cb17cd1 (the zip and this line follow in the next commit)

- Batch: `output/20261117-122135` (1,547 smokes, 171 games, 7 maps; 1,074 destroyer smokes). King of the Sea XIX NA.
- Concealed damage = damage dealt while hidden by the smoke; it includes torpedoes launched from smoke.
- Everything is association, not cause. The copy describes where teams smoked and what those smokes returned. It never says a spot or a habit produces a result.

## Files

| File | What it is |
|---|---|
| `ATLAS-CONTENT.md` | Final copy, page by page: page 1 rules, pages 2 to 8 maps, page 9 clan styles, sidebar, footer. Spot ids are in HTML comments next to the lines they belong to. |
| `spots.json` | `{batch, frame, rules, spots: [...]}`. 91 records: signature 6, lead 5, paying_high 10, paying_low 11, early_smoke 14, radar 5, deaths 7, cast_cruiser 12, cast_second_dd 21. |
| `caps.json` | Per map: caps (letter, `centre_uv`, `radius_u`, radius in km) and, for each cap, the cap-choice numbers of its zone (share of Top 6 and Rest destroyer smokes, gap, interval). |
| `maps/` | The 7 minimap images, unchanged copies of `output/20261103-143026/maps/*.png` (768 x 768) plus `.webp` copies used by the SVG figures, and `maps.json` (file, title, size in km, transform). |
| `figures/` | Working figures, PNG + SVG: `map-sg`, `map-hs`, `map-loop`, `map-mr`, `map-lof`, `map-sof`, `map-oki` (one per map page) and `clan-styles` (page 9), plus `clan-styles-numbers`. SVG width 1,232 to 1,280; the PNGs are rendered at 2x. They are for reference when redrawing, not final art. |
| `CHECK.md` | Every number in the copy traced to its source file and section, and how to reproduce it. Lists where sources disagree. |
| `tables.txt` | Plain-text output of the build: one block per map with every number used on that map's page. |
| `scripts/` | `atlas_lib.py` (helpers), `atlas_build.py` (writes `spots.json`, `caps.json`, `maps/`, `tables.txt`), `atlas_figs.py` (figures, drawn from `spots.json` and `caps.json`), `check_copy.py` (word limits and wording), `validate_package.py` (JSON, links, maps, figures), `explore_clusters.py` (the first look at cluster sizes; prints only). Run as `python -I -X utf8 smoke/analysis/atlas/scripts/<script>.py` from the repo root. Plain Python 3.13, no extra packages. |

## The frame (same text as `frame` in `spots.json` and `caps.json`)

- Origin at the **top-left** corner of the minimap image. `u` runs to the right (west to east), `v` runs down (north to south). Both go from 0 to 1 across the full image.
- **The images need no flipping.** The frame is the minimap in its native orientation. Positions were team-normalized before plotting (the mirror is applied to the positions, not to the picture), so the smoking team's spawn is always at the bottom, bottom-left on Okinawa.
- Lengths (`radius_u`, `ru`, `rv`) are fractions of the image width. An ellipse `angle_deg` is the rotation of the `ru` axis clockwise on screen from the `u` axis (the same as SVG `rotate`). A grid cell is a 4-point polygon; the grid is 10 x 10, numbers 1 to 10 west to east, letters A to J north to south.
- Cap letters are the real map letters. Each map's mirror maps caps onto caps, so the letters are the same for both teams once positions are normalized.

Transform per map (applied to north-spawn teams only; south-spawn teams are unchanged):

| Map | Size | Transform | Own spawn |
|---|---|---|---|
| Sleeping Giant | 42 km | mirrored north-south: (u, v) -> (u, 1 - v) | bottom |
| Hotspot | 48 km | mirrored north-south | bottom |
| Loop | 48 km | mirrored north-south | bottom |
| Mountain Range | 48 km | mirrored north-south (cap A is a real 10 km cap on the west edge; kept) | bottom |
| Land of Fire | 48 km | mirrored north-south | bottom |
| Sea of Fortune | 48 km | mirrored north-south | bottom |
| Okinawa | 42 km | spawns are NE and SW; the NE team is mirrored across the NW-SE diagonal: (u, v) -> (v, u) | bottom-left |

East and west are never swapped, except by the Okinawa diagonal mirror.

## Groups

- Top 6: H-SR (20-2), RESIN (17-7), BONKZ (13-8), HTDOG (12-6), KITE (9-5), VRTUS (7-4).
- Rest: every other clan.
- PN (3-4): 10 destroyer smokes (Land of Fire 3, Mountain Range 2, Sea of Fortune 2, Hotspot 1, Loop 1, Okinawa 1). None falls in a signature spot. It gets one line on page 9; per-map PN smokes are listed at the end of each block in `tables.txt`. Small n.

## Definitions

- **Radar cruiser inside**: a cruiser that carries radar and that the batch labels as inside the smoke. This is the one headline definition for the radar partner.
- **Radar play**: a smoke whose primary purpose is cap control (a radar ship hidden in the smoke ran radar while it covered 90% or more of the contested cap) or radar trap. 96 destroyer smokes; 21 cruiser smokes, all Svea.
- **Habit clusters** (set by the ship): flank smoke lines (Somers, Gearing, Harugumo, Delny), cap sitters (Daring, Z-42, Gdańsk, Grozovoi, Shimakaze), parked cruiser smoke (Svea, Jinan), moving exhaust (Napoli, Venezia, C. Colombo).
- **Early**: the first 5 minutes of the game.
- **Cap won / cap taken**: for cells and cap zones (Module 4) it is the share of all smokes in the cell after which the contested cap was taken (`cap_won_pct_all_smokes`). For signature spots, early clusters and radar addresses it counts only smokes whose contested cap was not already ours (`cap_won_pct` with `cap_won_n`).
- **Cap zone / cap choice**: every destroyer smoke is assigned to its nearest cap (distance to the cap edge). Cap choice is the share of a group's destroyer smokes on that map in each zone.
- **Signature spot rule** (Part B): a mean-shift cluster (2 km) of Top 6 smokes of one ship or habit on one map; kept as a signature if its ellipse holds at least 8 Top 6 smokes from at least 2 Top 6 clans, the Rest have at least 8 smokes of that ship or habit on the map, and the 95% interval of the share gap is above zero. A **lead** meets the first two but the interval touches zero or there is nothing to compare.
- **Paying cells**: a grid cell with 8 or more destroyer smokes. High = concealed damage per smoke at least 1.4 times the map average; low = at most 0.6 times. Where a map has no high (or low) cell, the best (or lowest) rated cell is listed with `flag` saying it is not a high (or low) cell; it is drawn dashed in the figures.
- **Early-setup clusters**: mean-shift (2 km, Gaussian kernel) on the centres of all early destroyer smokes on the map, both groups together (Module 2 found that both groups open in the same places). The shape is the 2-standard-deviation ellipse.
- **Radar addresses**: destroyer radar plays grouped by the cap they contested, as in Module 3; a cap needs 8 or more plays. The ellipse shows where those smokes were laid; plays more than 8 km from the group's median point are left out of the drawn ellipse but stay in the counts.
- **Death clusters**: smokes of any class in which the smoker or a covered teammate was lost, clustered at 2.5 km (deaths are sparse); a cluster needs 8 or more such smokes.
- **Supporting cast**: for the smokes of a spot, the nearest cruiser inside each smoke (`cast_cruiser`) and the nearest other allied destroyer (`cast_second_dd`), at the moment the smoke was fully laid. "Forward" means toward the enemy spawn relative to the smoke centre. The record's centre is the mean position and its shape the 2-standard-deviation ellipse.
- **Small-n rule**: nothing is reported below 8 smokes; 8 to 14 is marked small n (`small_n: true`). Exception, marked in `notes`: three cast records under Part B spots count 6 or 7 ships (the spot itself has 10 or 11 smokes); they are kept only so the formation can be drawn.
- **Intervals**: 95%, made by resampling whole clans. Clan-style intervals (page 9) resample games, because a style has only 2 or 3 clans.

## Word limits

Enforced by `scripts/check_copy.py`. A word is a whitespace-separated token with at least one letter or digit; a link counts its label only; HTML comments are not counted.

| Section | Words | Limit |
|---|---|---|
| Page 1 rules 1 to 8 | 25, 24, 24, 24, 25, 25, 24, 24 | 25 each |
| Page 2 Sleeping Giant | 218 | 220 |
| Page 3 Hotspot | 219 | 220 |
| Page 4 Loop | 210 | 220 |
| Page 5 Mountain Range | 218 | 220 |
| Page 6 Land of Fire | 216 | 220 |
| Page 7 Sea of Fortune | 218 | 220 |
| Page 8 Okinawa | 185 | 220 |
| Signature and lead lines | 13 to 30 | 30 each |
| Page 9 Clan styles | 250 | 250 |
| Sidebar | 113 | 120 |

Page 1 also carries a "fine print" paragraph (intervals and comparison values for each rule) that sits outside the 25-word rules, and the footer has no limit.

## What could not be done, and cautions

- **Ship positions exist only at the moment each smoke was fully laid.** Not at activation and not continuously. Every cruiser and second-destroyer position in this package is that one snapshot. The batch also has a position for only about 4 allied ships per smoke, so "no second destroyer recorded" does not mean there was none.
- **Spotting cannot be attributed.** The batch does not say who spotted a target. Part B uses "nearest allied ship to the target" as a stand-in, and a second destroyer forward of the smoke is the stand-in for "someone is spotting for it".
- **No score or cap timeline.** Scores and cap owners are known only at the moments a smoke is laid or a cap is taken, so nothing here says when a cap changed hands between smokes.
- **The scouting report text is not on disk.** Nothing in the atlas is checked against its wording.
- **Signature spots are small n, and the placebo result applies.** Six Rest clans standing in as the "top" group pass 2.5 signature spots on average (20 draws, range 0 to 5), so 2 to 3 of the 6 signature spots are the kind any group of six clans shows. Best supported: Land of Fire Svea at F5 and Sleeping Giant Harugumo at G1/F1. Weakest: Mountain Range parked cruiser smoke (two clans, mostly a ship the Rest did not bring) and the Sleeping Giant east edge (interval barely clear of zero).
- **Okinawa** has 15 Top 6 destroyer smokes and no signature spot; its page leads with cap choice and deaths. **Hotspot** has no signature spot, only a lead; its page leads with cap choice.
- **Loop, Mountain Range**: no death cluster reaches 8 smokes; the pages give cell and zone death rates instead. **Loop, Land of Fire, Sea of Fortune, Okinawa**: no cap has 8 radar plays, so there is no radar address.
- **Sleeping Giant Somers lead** (`sg-somers-f9`) is in `spots.json` but left off the page: it is the same place as Signature 2 seen for one ship.
- Early-setup clusters mix Top 6 and Rest smokes to reach a usable n; the Top 6 count is given for each. On Loop, Sea of Fortune and Okinawa the Top 6 have 2 to 4 smokes per cluster.
- Wide shapes (marked "wide" in the label or notes: Sea of Fortune Svea, Loop cap sitters, Sleeping Giant radar at C, two death clusters) are zones, not tight spots.
