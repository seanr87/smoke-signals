# CHECK-X3: where every number in FINDINGS-X3.md comes from

Run order, from `round5c/x3-clans/`, each with `python -I -X utf8`: `d1_scores.py`, `d2_structure.py`, `d2_structure.py` again with the environment variable `X3_CLOCK=el` (reproduces round 5b, check only), `d3_profiles.py`, `x3_findings.py`. `run_all.py` does all five and saves the printed output as `d1_output.txt`, `d2_output.txt`, `d2_output_el.txt`, `d3_output.txt`. `d_lib.py` holds the score definitions (`feats`), resampling (`boot_clan`), percentiles (`pctile`) and the hand-written PCA and k-means. Seeds are fixed (519, 520, 521, 1000, 1001), so reruns give the same numbers.

Sanity checks (computed here from the output files):

| Check | Result |
|---|---|
| Smokes, all clans | 1,547 (anchor 1,547) |
| Destroyer-smoke anchor (194 died, 18.2 per 100, smoker 12.75; 124 caught, 11.55, smoker 6.4) | printed by `d1_scores.py` as "anchor destroyer smokes" in `d1_output.txt` |
| Top 6 / Rest smokes and team-games | 538 in 110 / 1009 in 232 |
| "Caught per 100" equals round 5b deaths per 100, all 30 clans | yes |
| Scores identical to round 5b (every clan, every lineup / who / where / movement / concealed-damage score) | yes |
| D2 on the HUD clock reproduces round 5b positions | largest difference 0.0e+00; same four groups: yes |
| Top 6 minus Rest gap of each death and cap score, group value equals the library statistic (`died100`, `caught100`, `share_stat`) | asserted in `d1_scores.py`; the `boot_diff` intervals are in `d1_scores.json` `gaps_bootdiff` |
| `clan_styles.json` structure equal to round 5b | yes |
| Gauge identical to round 5b | 30 of 30 clans |

| Number | Script | Where |
|---|---|---|
| All-smokes totals (ships died, caught, the 9 left-out smokes, smokes each cap rate applies to) | `d1_scores.py` | `N_ALL` -> `d1_scores.json` `n_all` |
| Per-clan values: died / caught per 100, smoker versions, caps taken, not lost, caps per game | `d_lib.py`, `d1_scores.py` | `feats(clan, strict=True)` -> `V[clan][key]`; `d1_scores.json` `values`; n per rate in `n_cases` |
| Per-clan 95% intervals | `d1_scores.py` | `I[clan][key]` from `d_lib.boot_clan` (600 resamples of the clan's games); `d1_scores.json` `intervals` |
| Percentiles among the 24 clans | `d1_scores.py` | `PC[clan][key]` from `d_lib.pctile`; `d1_scores.json` `percentiles` |
| Lowest / median / highest table | `x3_findings.py` | `lmh(key)` over `values` of the 24 clans |
| Top 6 minus Rest on every score | `d1_scores.py` | `grp_feats(top)`, `grp_feats(rest)`, `REPS` (500 clan resamples, seed 1000) -> `GAPS`; `d1_scores.json` `gaps`; `clan_styles.json` `top6_minus_rest` |
| Same gaps with the library helper | `d1_scores.py` | `XCHECK` from `boot_diff(S, stat)` (seed 1001); `d1_scores.json` `gaps_bootdiff` |
| What the clock switch moved (first smoke, after 12:00, before 5:00) | `x3_findings.py` | `tm`: `values` here against `round5b/part-d/d1_scores.json`; `x3_changes.json` `time_moves` |
| Scale shares, loadings, clan positions | `d2_structure.py` | `shares`, `vecs`, `scores` from `pca(Z)`; `d2_structure.json` `shares`, `loadings`, `scores`; flagged clans in `proj` |
| Shuffled-data shares | `d2_structure.py` | `null1`, `null2` (300 column shuffles); `d2_structure.json` `null` |
| Shape of the two scales (largest gap, low-smoke clans) | `d2_structure.py` | `SHAPE` -> `d2_structure.json` `shape` |
| Silhouettes, agreement under resampling, scale steadiness | `d2_structure.py` | `SIL`, `aris`, `r1`, `r2`; `d2_structure.json` `silhouette`, `boot`; `clan_styles.json` `structure.stability` |
| Four corners, members, borderline shares | `d2_structure.py`, `d3_profiles.py` | `KM2[4]`, `keep[4]` -> `d2_structure.json` `km2`, `keep2`; `d3_tables.md` "Style members"; `clan_styles.json` `styles` |
| Moved: yes / no per clan | `x3_findings.py` | `moved`: `clans.<name>.style` here against `round5b/clan_styles.json`; `x3_changes.json` `styles` |
| Style pooled numbers and ranges | `d3_profiles.py` | `POOL[i]` from `pool()` (400 game resamples); `d3_tables.md`; `clan_styles.json` `styles[].numbers` |
| Outcome scores against the two scales | `d2_structure.py` | `OUTR` -> `d2_structure.json` `outcome_r` |
| Top 6 against Rest on the two scales; chance figures | `d3_profiles.py` | `AX`, `p_all`, `p4`; `clan_styles.json` `structure.top6_vs_rest_on_axes`, `top6_concentration` |
| Gauge values for H-SR and HTDOG | `d3_profiles.py` | `clan_styles.json` `clans.<name>.gauge` |
| Every "round 5b" number | `x3_findings.py` | read from `round5b/part-d/d1_scores.json`, `round5b/part-d/d2_structure.json`, `round5b/clan_styles.json` |

Headline numbers as computed:

| Headline | Value |
|---|---|
| Died per 100, Top 6 / Rest (gap 95%) | 12.27 / 19.30 (-13.31 to -2.59 *) |
| Caught per 100, Top 6 / Rest | 7.81 / 13.38 (-9.52 to -2.88 *) |
| Smoker died per 100 | 8.18 / 15.10 (-12.28 to -3.15 *) |
| Smoker caught per 100 | 4.28 / 9.22 (-8.60 to -2.55 *) |
| Nearest cap taken % | 38.99 / 28.47 (+0.48 to +21.45 *) |
| Contested cap taken % | 32.16 / 22.77 (+1.10 to +17.60 *) |
| Nearest cap not lost % | 85.71 / 82.95 (-3.29 to +8.62) |
| Contested cap not lost % | 83.57 / 75.82 (+1.89 to +15.27 *) |
| Scale shares | 29.61% / 17.81% (round 5b 29.61% / 17.81%) |
| Clans that moved style | none |

Notes:
- `d_lib.py` never reads `cap_won`, `cap_def`, `s['we_took']`, `s['enemy_took']` or `s['el']` in the default run. `s['el']` is read only when `X3_CLOCK=el` is set, to prove the rerun matches round 5b.
- "Not lost" on the contested cap uses the distance to the contested cap (`s['edge'] <= 2000`); on the nearest cap `near_cap_edge_m <= 2000`, as the brief says.
- The Top 6 minus Rest intervals in the tables come from the round 5 method (pooled group value, whole clans resampled, 500 runs). The library helper `boot_diff` (1,000 runs) gives the same reading for every death and cap score; both are shown in D1.
- No library problem found. `r5clib.py` was not edited.
