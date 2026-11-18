# CHECK-D: where every number in FINDINGS-D.md comes from

Run order (from `round5/part-d/`, each with `python -I -X utf8`): `d1_scores.py`, `d2_structure.py`, `d3_profiles.py`. `d_lib.py` holds the score definitions (`feats`), the resampling (`boot_clan`), percentiles (`pctile`) and the hand-written PCA / k-means / clustering. Seeds are fixed (519, 520, 521, 1000), so reruns give the same numbers.

Sanity checks printed by `d1_scores.py`: 1,547 smokes summed over clans; 171 games = 342 team-games; destroyer smokes 387 Top 6 and 687 Rest; 30 clans, 24 with 7+ games; Top 6 538 smokes in 110 team-games, Rest 1,009 in 232.

| Number | Script | Where |
|---|---|---|
| Per-clan values (all tables in D1, heat table) | `d1_scores.py` | `V[clan][key]` from `d_lib.feats(clan, strict=True)`; printed in `d1_tables.md` sections Lineup ... Extra; stored in `d1_scores.json` `values` |
| Lowest / median / highest per score (D1 table) | `d1_scores.py` output | min, median, max of `values[clan][key]` over the 24 clans (`d1_scores.json`); names read from `d1_tables.md` |
| Sideways 26%, unclassified 101 | `d1_scores.py` | printed line `movement labels` (horizontal 397 of 1,547; unclassified 101) |
| Mapping of movement labels | `d_lib.py` | `MOVE` dict and its comment (batch `closing_m` is positive when range opened: pushing median -1,838 m, kiting +1,174 m) |
| Smoke ships brought, Top 6 vs Rest, with gaps | `d1_scores.py` | `grp_brings`, `clan_diff`; `d1_tables.md` section "Smoke ships brought, share of games" |
| Ships inside destroyer smokes, Top 6 vs Rest | `d1_scores.py` | `grp_inside`, `clan_diff`; `d1_tables.md` section "Ships inside destroyer smokes" |
| Per-clan brought ships, inside ships, top caps, lanes | `d1_scores.py` | `NOTES[clan]`; `d1_tables.md` section "Smoke ships brought ... and ships inside"; `clan_styles.json` `clans.<name>.notes` |
| Top 6 minus Rest on every score (47% vs 29% radar cruiser inside, 0.2 vs 0.6 exhaust ships, 11,685 vs 8,515, 57,152 vs 37,034, 8 vs 13 deaths, 84% vs 78%, 3.6 vs 3.0 radar ships, and the Shared rows) | `d1_scores.py` | `grp_feats(top)`, `grp_feats(rest)`, `REPS` (500 clan resamples) -> `GAPS`; `d1_tables.md` last section; `d1_scores.json` `gaps`; `clan_styles.json` `top6_minus_rest` |
| 694 smokes with no "taken" answer; 541 smokes with a "not lost" answer (within 2 km of the nearest cap) | `d1_scores.py` | printed line "no taken answer 694 / not-lost answer within 2 km 541 of 1547"; per clan `n_take_known`, `n_hold_known` in `d1_scores.json` |
| Cap not lost: 71% (REEEE, n 17) to 100% (MACH, n 12), median 89% over 21 clans; KSE, NGA, PN too few (7, 7, 5) | `d1_scores.py` | `values[clan]['held_pct']`, `n_hold_known`; same printed line lists the clans under 8 |
| Cap not lost Top 6 92% vs Rest 87% (+0.6 to +9.5) | `d1_scores.py` | `GAPS['held_pct']`; last section of `d1_tables.md` |
| Delny 37 in lineups, 7 carrying smoke | `d1_scores.py` | printed lines "ships with smoke_variant" (Delny 7) and "long/sitter ships WITHOUT smoke_variant" (Delny 30) |
| Clan 95% ranges (headline table, gauge) | `d1_scores.py` | `I[clan][key]` from `d_lib.boot_clan` (600 resamples of the clan's games); `d1_tables.md` section "Headline value"; `d1_scores.json` `intervals` |
| Percentiles (p4, p91, ...) | `d1_scores.py` | `PC[clan][key]` from `d_lib.pctile` against the 24 clans; same section |
| Scale shares 29.5%, 17.4%, 12.3%; 47% together | `d2_structure.py` | `shares` from `pca(Z)`; `d2_output.txt` line "PC shares"; `d2_structure.json` `shares` |
| Shuffled-data 95th percentiles 19.0% and 15.8% | `d2_structure.py` | `null1`, `null2` (300 column shuffles); lines "null PC1 share", "null PC2 share" |
| Links of scores with each scale (-0.84 ... +0.76 ...) | `d2_structure.py` | "PC1 loadings", "PC2 loadings" blocks; `d2_structure.json` `loadings` |
| Smoke cruisers r +0.71 with the first scale, for a teammate -0.82 | `d2_structure.py` | lines "single score vs axes" |
| Largest gap 1.6 of range 8.6; seven low clans at -1.8 or below, others +0.3 or above | `d2_structure.py` | lines "PC1 sorted", "PC2 sorted", "PC2 order" |
| Silhouettes 0.18 / 0.16 / 0.18, shuffled 0.09 to 0.12 | `d2_structure.py` | lines "k=2:", "k=3:", "k=4:" (k-means silhouette and shuffled-data 95th pct) |
| Agreement under game resampling 0.54 (2 groups), 0.34 (3 groups) | `d2_structure.py` | lines "k=2: ARI vs base median", "k=3: ARI vs base median" (200 resamples) |
| Dropping lineup: agreement 0.31 | `d2_structure.py` | block "drop one group, k=2", row "without Lineup" |
| Scale steadiness 0.90 and 0.78 | `d2_structure.py` | line "games resampled within clan": PC1 scores vs base median, PC2 median |
| Two-scale map: 4 corners silhouette 0.47; kept in 86% | `d2_structure.py` | lines "2-axis map k=4" and "2-axis style kept under game resampling, k=4: mean" |
| Style members, borderline shares (HFANS 60% ... NGA 74%), flagged placements | `d2_structure.py`, `d3_profiles.py` | `km2['4']`, `keep2['4']`, `proj[clan].near2` in `d2_structure.json`; `d3_tables.md` section "Style members" |
| Style pooled numbers and ranges; clans / games / smokes per style | `d3_profiles.py` | `POOL[i]` from `pool()` (400 game resamples); `d3_tables.md` first table; `clan_styles.json` `styles[].numbers` |
| W-L by style (101-66, 32-32, 20-25, 12-19) | `d3_profiles.py` | `d3_tables.md` "Style members" lines |
| Round 4 second check (0.3 vs 1.2, 73% vs 49%, 20% vs 45%, 2:43 vs 3:50) | `d3_profiles.py` | `pool(['H-SR','RESIN','BONKZ'])`, `pool(['HTDOG','VRTUS'])`; `d3_tables.md` section "Second check against round 4" |
| Top 6 vs Rest on the two scales (-1.17 / +0.39, gap -1.56, -3.57 to +0.49; +0.90 / -0.30, gap +1.21, +0.22 to +2.24) | `d3_profiles.py` | `AX[0]`, `AX[1]` (2,000 clan resamples); `d3_tables.md` lines "Axis 1", "Axis 2" |
| Chance figures 24% and 9% | `d3_profiles.py` | `p4` (hypergeometric, 4+ of 6 in an 11-of-24 group) and `p_all` (6 of 6 in a 17-of-24 group); last two lines of `d3_tables.md` |
| H-SR and HTDOG gauge values | `d1_scores.py` | `d1_tables.md` section "Headline value"; `clan_styles.json` `clans.H-SR.gauge`, `clans.HTDOG.gauge` |
| 35 scores kept per clan | `d_lib.py` | `ALLKEYS` (the keys of `LABEL`) |

Notes on definitions that differ from earlier rounds:
- "Smoke ship in the lineup" uses the roster field `smoke_variant` (set when the ship carries smoke), not `smoke_activations`, so a ship that brought smoke but never used it still counts.
- "Cap not lost" uses `enemy_took is False` only for smokes inside or within 2 km of the nearest cap (`near_cap_edge_m <= 2000`, `HOLD_NEAR_M` in `d_lib.py`), following this round's validation by another worker. The batch `cap_def` flag fires for any owned cap with an enemy inside, anywhere on the map, so it is kept only as a secondary column in the Extra table and is not read as "the smoke defended a cap".
- Caps taken per game counts distinct caps per game with `we_took` true; the batch flags `cap_won` / `cap_def` are also kept (per smoke, per game) in the Extra table.
- Style building used 17 behaviour scores; the five outcome scores were left out and reported per style afterwards. With outcomes included the first two scales are almost the same (correlation 0.94 and 0.89 with the behaviour-only scales; `d2_output.txt` line "with outcomes included").
