| number | script | where |
|---|---|---|
| cap_defended rates 31.4 / 33.5 / 26.9%, Top 6 vs Rest gaps | c1_caps.py | `grp_rows(..., s['cap_def'])`; out-caps.md "C1 part 1" table; caps.json `cap_defended.rates` |
| 486 smokes; role 459 middle / 27 enemy side | c1_caps.py | `D`, `def_role`; caps.json `cap_defended.role` |
| nearest cap in 175 of 486; median 8,949 m; 74 touching; 307 over 6 km | c1_caps.py | `def_cap == near_cap`, `def_edge_m` (`de`) |
| kept 60.5% (and rows), 77.0% at 0 s, 51.9% at 120 s | c1_caps.py | `def_lost`, grace loop; caps.json `cap_defended.kept` |
| 86.3% (n 694) comparison | c1_caps.py | `base` |
| hand check 10 of 10 | c1_caps.py | `pick`, `HC`; out-caps.md "Hand check" |
| 0 mismatches of 1,547 | c1_caps.py | `my_took`, `mism` |
| cap_won cross-check 171: 144 / 26 / 1 | c1_caps.py | `cw`; caps.json `enemy_took.cap_won_crosscheck` |
| coverage yes 184 / no 889 / n/a 474 | c1_caps.py | `cov`; caps.json `enemy_took.coverage` |
| snapshots median 5, 111 with one; window 158 s; gap 48 s; tail 21 s; 241 over 60 s | c1_caps.py | `tw`, `lens`, `gaps`, `tails` |
| grace 0 / 60 / 120 s: 103 / 184 / 233 | c1_caps.py | grace table; caps.json `enemy_took.grace` |
| median 2,314 m; 346 over 5 km | c1_caps.py | `ne` |
| enemy-took summary table (17.1%, 18.8%, 11.1% ...) | c1_caps.py | `grp_rows(..., s['enemy_took'])`; caps.json `enemy_took.overall` |
| by map and cap rows | c1_caps.py | caps.json `enemy_took.by_map_cap` |
| replays per game 170 x 2, 1 x 1 | c1_caps.py | caps.json `ribbons.replays_per_game` |
| ribbon source lines | read only | decode.rs 2102-2139; resources.rs 605-650; combat.rs 31-116; smoke-signals render.rs 63-64, 93-94; grep of batch folder |
| C2 coverage 154 / 5 / 12 and per map | c1_caps.py | `cover`; caps.json `c2.coverage` |
| favourite won 110 of 158; 128 of 164 | c1_caps.py | `allg` |
| C2 pooled and per-map rows | c1_caps.py | `c2row`; caps.json `c2.pooled`, `c2.maps[map].all / rest_vs_rest` |
| own side / middle / enemy side labels | c1_caps.py | `role_of`; caps.json `c2.maps[map].caps` |
| 66 of 91 already ahead, lead 95; 120 of 153; 63 level; Top 6 30 / 7 / 46 | c1_caps.py | `ml`, `ah`, `tie`, `tr`; caps.json `c2.notes` |
| C3 baselines 6.4 / 15.5 and 8.0 / 22.0, per map | c1_danger.py | baseline table in out-danger.md |
| 313 areas, 109 tested (77 / 32), 204 unrated | c1_danger.py | `AREAS`, `TEST` |
| 4 flags; 0 on deaths alone | c1_danger.py | `FL`, `flag_died` |
| placebo 1.23 per run, 5 of 120 with 4+ | c1_danger.py | `pl` |
| flagged area rows, intervals | c1_danger.py | `evaluate`, `arow`; danger-zones.json |
| behind / radar shares, clan counts, share gaps, without-top-clan | c1_danger.py | `describe`; danger-zones.json |
