# CHECK-C4: where every number comes from

Rerun: `python -I -X utf8 c4_spots.py` (writes `spots.json`, `checks.json`, `generated.md`, `out.txt`, `FINDINGS-C4.md` from `head.md`, and the seven figures), then `python -I -X utf8 c4_wide.py` (writes `wide.txt`). Both are seeded (`random.Random(519)` / `520`), so reruns give the same numbers. `explore.py` only prints pool sizes.

| Number in FINDINGS-C4.md | Script | Where |
|---|---|---|
| 1,547 smokes; destroyer smokes 387 Top 6 / 687 Rest | c4_spots.py | last `CHECK` line of `out.txt` |
| 21 spots; counts by map and kind (table) | c4_spots.py | `RECS`, `count_table`; one line per spot in `out.txt` |
| 0 of 21 Top 6 spots; 2 "Rest use it more" | c4_spots.py | `label()` on `share_test()`; `mode` and `note` in `spots.json`; `PLACEBO ... real: top 0 of 21` in `out.txt` |
| Per spot: n, n Top 6 / Rest, clans, damage per smoke, deaths per 100, cruisers, examples | r5lib `spot_record` called from c4_spots.py | `spots.json` fields `n`, `n_top6`, `n_rest`, `clans`, `concealed_damage_per_smoke`, `deaths_per_100`, `cruisers`, `examples` |
| Per spot: share Top 6 vs Rest, gap, interval | c4_spots.py `share_test` (2,000 clan resamples) | `share_top6`, `share_rest`, `diff_pts`, `diff_ci`; pool sizes `pool_top6`, `pool_rest` |
| Per spot: cruisers inside / screened by group | c4_spots.py `cr_by` | `cruisers_by_how` |
| Per spot: median time, cells, radius, where | c4_spots.py `base_extra`, `where`, `cells_of` | `median_time`, `cells`, `radius_km`, `where` |
| Early spots: inside vs screened, Top 6 vs Rest | c4_spots.py (family `early_cruiser` block) | `n_inside`, `n_screened`, `inside_top6`, `inside_rest`, `screened_top6`, `screened_rest` |
| hs-sit-1 6% vs 23% (-30 to -5); loop-sit-1 4% vs 20% (-26 to -2) | c4_spots.py | `out.txt` lines `hs-sit-1`, `loop-sit-1` |
| lof-park-1 58% vs 19% (-6 to +70); loop-sit-2 30% vs 9% (-3 to +50); sg-early-1 36% vs 20% (-8 to +38) | c4_spots.py | `out.txt` lines with those ids |
| Wide scale: 25 spots, 2 Top 6; Loop cap B 8 of 23 vs 6 of 65, 35% vs 9% (+3 to +53); Land of Fire F5 14 of 19 vs 5 of 21, 74% vs 24% (+8 to +84); their clans | c4_wide.py | `wide.txt` (lines `Loop | cap_sitter | inside cap B`, `Land of Fire | parked_cruiser`, `TOTAL`); pool sizes 23/65 and 19/21 from the `pool` lines in `out.txt` |
| Placebo main scale: 12 Rest-only spots, 0.33 labelled top on average, range 0 to 3, 200 draws | c4_spots.py | `PLACEBO` dict; `checks.json` |
| Placebo wide scale: 14 spots, 0.54 average, range 0 to 4, 7% of draws with 2 or more | c4_wide.py | last line of `wide.txt` |
| 137 cells or pairs tested, 3 passed | c4_spots.py `high_cells` | `SHUF['tested']`, `SHUF['real']`; `high cells` lines in `out.txt` |
| G1 24.1k vs 10.7k (+8.2k to +20.2k), n 21; Hotspot G10+H10 17.0k vs 11.4k (+0.8k to +10.7k), n 40; Sea of Fortune F9+G9 24.6k vs 10.3k (+1.0k to +32.5k), n 10 | c4_spots.py `cell_test` | `cell_mean`, `rest_of_map_mean`, `damage_gap_ci` in `spots.json`; second check: G1 24.1k n 21 matches round 3 Module 4 |
| Shuffle check: 1.85 cells pass on average (0 to 4), 20 runs | c4_spots.py | `SHUF`; `checks.json` |
| Win/loss: G1 26.5k (n 14) vs 19.3k (n 7); Hotspot 21.3k (n 16) vs 14.1k (n 24); Sea of Fortune 28.0k (n 8) vs 10.9k (n 2) | c4_spots.py `base_extra` | `damage_win`, `damage_loss`, `n_win`, `n_loss`, `win_loss_differs` (rule: > 5k apart, n >= 5 each side) |
| Cap taken: G1 19% of 21; Hotspot 34% of 35; Sea of Fortune 25% of 8 | c4_spots.py `base_extra` (r5lib `we_took`, None left out) | `cap_taken_pct`, `cap_taken_n` |
| Early spots: sg n 16 (12 inside, 4 screened); hs n 17 (13, 4); hs n 9 (7, 2) | c4_spots.py | `sg-early-1`, `hs-early-1`, `hs-early-2` in `spots.json` |
| Okinawa pools 16 to 40 per kind; Top 6 2 to 10 | c4_spots.py | `Okinawa | ...: pool` lines in `out.txt` |
| "No spot" statements per map | c4_spots.py | `NONE[m]`; needs max(8, 10% of the pool) smokes in one circle |

Method constants (top of `c4_spots.py`): bandwidth 1.0 km, circle radius 1.5 to 2.5 km, minimum 8 smokes and 10% of the pool, 2,000 resamples, win/loss rule 5k and n >= 5. Wide check: bandwidth 1.5 km, radius 2.5 to 3.5 km.
