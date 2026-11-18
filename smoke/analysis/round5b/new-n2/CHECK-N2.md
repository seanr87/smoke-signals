# CHECK-N2: where each number comes from

All scripts are in `round5b/new-n2/`; run with `python -I -X utf8 <script>`. Order: n2_health.py, n2_danger.py (about 20 minutes: placebo), n2_leave.py, n2_radar.py, then n2_write.py. `n2lib.py` holds the shared ship-smoke pairs (real health, positions, radar flags).

| number | script | where |
|---|---|---|
| Agreement table, flips, reasons | n2_health.py | out-health.json: agreement, flip_reasons |
| Estimate / real full health by class | n2_health.py | out-health.json: hp_est, hp_est_worst_ships |
| Batch deaths 176, track deaths 270, track only 96 | n2_health.py | out-health.json: deaths_check |
| Destroyer baselines 12.8 died / 23.1 died or hurt | n2_health.py | out-health.json: baselines.dd.measures[1], [4] |
| Cruiser baselines 9.6 / 19.4 | n2_health.py | out-health.json: baselines.cr.measures[1], [4] |
| Round 5 numbers reproduced from the round 5 fields (6.4 / 15.5, 8.0 / 22.0) | n2_health.py | out-health.json: check_r5 |
| Version 1: 108 tested, 2 flagged, placebo 1.57 | n2_danger.py | out-danger.json: v1 (n_flag, placebo, shown) |
| Version 2: 111 tested, 3 flagged, placebo 1.75 | n2_danger.py | out-danger.json: v2 |
| Round 5 flags old vs new | n2_danger.py | out-danger.json: r5_flags, r5_recomputed |
| Flagged-area clans, 50+ behind, radar, Top 6 or Shared | n2_danger.py | out-danger.json: v1.shown / v2.shown (flag true); danger-zones.json |
| Death positions: 268 pairs, inside / outside | n2_danger.py | out-danger.json: death_pos |
| Batch deaths by class: inside 29, left 82, dispersed 5, never 8 | n2_leave.py | out-leave.json: batch_deaths |
| Track deaths by class (201) | n2_leave.py | out-leave.json: track_deaths, track_only_deaths |
| Round 5 proxies against the track | n2_leave.py | out-leave.json: proxies |
| Leaving vs staying rates (3.1 vs 3.6) | n2_leave.py | out-leave.json: rates |
| Per 30 s inside / after leaving / after dispersal, detection | n2_leave.py | out-leave.json: hazard, rates[].det |
| Radar-lit deaths 65 of 124 (40 s), 56 (20 s) | n2_radar.py | out-radar.json: batch |
| Radar-lit deaths, track deaths 92 of 201 | n2_radar.py | out-radar.json: track |
| Radar ship, class, distance, share of range, ambiguous, from smoke, time lit | n2_radar.py | out-radar.json: batch / track (src_class, src_ship, dist_km, share_of_range, ambiguous, src_in_smoke, lit_for_s) |
| Death by death against strict and broad | n2_radar.py | out-radar.json: vs_round5_deaths, strict_check |
| Rates with / without radar (20.9 / 6.3), by score state | n2_radar.py | out-radar.json: rates, rate_diffs |
| Round 5 strict 25.0 / 9.9 and broad 27.9 / 5.3 reproduced | n2_radar.py | out-radar.json: rates.old_strict, rates.old_broad |
| Smoke by smoke comparison | n2_radar.py | out-radar.json: smoke_by_smoke, log_only |
| Calm smokes 515 / 19 / 3.7 (round 5 definition reproduced: 585 / 17 / 2.9) | n2_radar.py | out-radar.json: calm |

## Second-way checks

- Round 5 baselines reproduced from the round 5 fields on the new batch: destroyer 6.4 / 15.5, cruisers 8.0 / 22.0 (round 5: 6.4 / 15.5, 8.0 / 22.0). `n2_health.py`, check_r5.
- Old estimate against real health on the same pairs before trusting either: agreement 91.1% over 2359 pairs. `n2_health.py`, agreement.
- Batch deaths confirmed by the tracks: 174 of 176. `n2_health.py`, deaths_check.
- Round 5 danger flags recomputed with round 5 outcomes on the round 5b units: 3 of the 4 (the fourth lost a smoke to the single-replay exclusion). `n2_danger.py`, r5_recomputed.
- Round 5 strict and broad radar rates and the calm statistic reproduced exactly from the old fields (25.0 / 9.9, 27.9 / 5.3, 585 / 17 / 2.9). `n2_radar.py`.
- Strict radar deaths: same radar ship in 18 of 19, median distance difference 0 m between the round 5 field and the log. `n2_radar.py`, strict_check.
- Deaths inside a standing smoke counted two ways (death classing and the exposure walk): 64 and 64. `n2_leave.py`.
