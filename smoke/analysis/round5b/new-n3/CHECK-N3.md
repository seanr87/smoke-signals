# CHECK-N3: where each number in FINDINGS-N3.md comes from

All scripts are in `round5b/new-n3/`. `b3.json` and `c5.json` are written by the scripts named; `b3_out.txt` and `c5_out.txt` hold the same tables as printed.

| Number | Script | Where |
|---|---|---|
| Harugumo: 410 shots, 898 events, 461,873 damage, 44 smokes | `b3_shots.py` | `b3.json base.Harugumo` |
| Somers: 83 shots, 152 events, 253,013 damage, 26 smokes | `b3_shots.py` | `b3.json base.Somers` |
| Gearing: 64 shots, 177 events, 94,724 damage, 18 smokes | `b3_shots.py` | `b3.json base.Gearing` |
| Delny: 2 shots, 2 events, 3,872 damage, 2 smokes | `b3_shots.py` | `b3.json base.Delny` |
| Harugumo nearest = a ship outside the smoke: 44.6% shots (183), 55.1% damage, 41.9% per smoke | `b3_shots.py` | `b3.json nearest.Harugumo` |
| Somers nearest = a ship outside the smoke: 37.3% shots (31), 27.7% damage, 27.7% per smoke | `b3_shots.py` | `b3.json nearest.Somers` |
| Gearing nearest = a ship outside the smoke: 7.8% shots (5), 11.2% damage, 15.2% per smoke | `b3_shots.py` | `b3.json nearest.Gearing` |
| Harugumo nearest = a second destroyer: 24.1% shots (99), 20.5% damage, 24.6% per smoke | `b3_shots.py` | `b3.json nearest.Harugumo` |
| Somers nearest = a second destroyer: 10.8% shots (9), 12.8% damage, 10.4% per smoke | `b3_shots.py` | `b3.json nearest.Somers` |
| Gearing nearest = a second destroyer: 1.6% shots (1), 0.5% damage, 5.6% per smoke | `b3_shots.py` | `b3.json nearest.Gearing` |
| Harugumo nearest = the smoker itself: 30.7% shots (126), 24.3% damage, 31.3% per smoke | `b3_shots.py` | `b3.json nearest.Harugumo` |
| Somers nearest = the smoker itself: 48.2% shots (40), 51.0% damage, 54.2% per smoke | `b3_shots.py` | `b3.json nearest.Somers` |
| Gearing nearest = the smoker itself: 90.6% shots (58), 88.3% damage, 79.2% per smoke | `b3_shots.py` | `b3.json nearest.Gearing` |
| Harugumo nearest = another ship in or behind the smoke: 0.0% shots (0), 0.0% damage, 0.0% per smoke | `b3_shots.py` | `b3.json nearest.Harugumo` |
| Somers nearest = another ship in or behind the smoke: 0.0% shots (0), 0.0% damage, 0.0% per smoke | `b3_shots.py` | `b3.json nearest.Somers` |
| Gearing nearest = another ship in or behind the smoke: 0.0% shots (0), 0.0% damage, 0.0% per smoke | `b3_shots.py` | `b3.json nearest.Gearing` |
| Harugumo nearest = the radar cruiser inside the smoke: 0.5% shots (2), 0.1% damage, 2.3% per smoke | `b3_shots.py` | `b3.json nearest.Harugumo` |
| Somers nearest = the radar cruiser inside the smoke: 3.6% shots (3), 8.5% damage, 7.7% per smoke | `b3_shots.py` | `b3.json nearest.Somers` |
| Gearing nearest = the radar cruiser inside the smoke: 0.0% shots (0), 0.0% damage, 0.0% per smoke | `b3_shots.py` | `b3.json nearest.Gearing` |
| nearest contrasts Harugumo minus Somers / Gearing | `b3_shots.py` | `b3.json nearest_contrasts` |
| Harugumo Radar-lit at the shot: 21.7% shots (89), 19.2% damage, 30.5% per smoke | `b3_shots.py` | `b3.json detected.Harugumo` |
| Somers Radar-lit at the shot: 26.5% shots (22), 9.4% damage, 25.6% per smoke | `b3_shots.py` | `b3.json detected.Somers` |
| Gearing Radar-lit at the shot: 42.2% shots (27), 28.4% damage, 34.9% per smoke | `b3_shots.py` | `b3.json detected.Gearing` |
| Harugumo ... by a radar ship inside this smoke: 3.2% shots (13), 2.4% damage, 3.2% per smoke | `b3_shots.py` | `b3.json radar.Harugumo` |
| Somers ... by a radar ship inside this smoke: 7.2% shots (6), 2.6% damage, 11.5% per smoke | `b3_shots.py` | `b3.json radar.Somers` |
| Gearing ... by a radar ship inside this smoke: 3.1% shots (2), 3.1% damage, 5.6% per smoke | `b3_shots.py` | `b3.json radar.Gearing` |
| Harugumo ... by a radar ship elsewhere: 18.3% shots (75), 16.6% damage, 25.0% per smoke | `b3_shots.py` | `b3.json radar.Harugumo` |
| Somers ... by a radar ship elsewhere: 18.1% shots (15), 6.7% damage, 14.0% per smoke | `b3_shots.py` | `b3.json radar.Somers` |
| Gearing ... by a radar ship elsewhere: 39.1% shots (25), 25.3% damage, 29.4% per smoke | `b3_shots.py` | `b3.json radar.Gearing` |
| Harugumo Detected, not radar-lit: 72.2% shots (296), 66.5% damage, 60.0% per smoke | `b3_shots.py` | `b3.json detected.Harugumo` |
| Somers Detected, not radar-lit: 63.9% shots (53), 60.1% damage, 53.7% per smoke | `b3_shots.py` | `b3.json detected.Somers` |
| Gearing Detected, not radar-lit: 42.2% shots (27), 53.0% damage, 39.5% per smoke | `b3_shots.py` | `b3.json detected.Gearing` |
| Harugumo Not detected at the shot: 6.1% shots (25), 14.3% damage, 9.5% per smoke | `b3_shots.py` | `b3.json detected.Harugumo` |
| Somers Not detected at the shot: 9.6% shots (8), 30.5% damage, 20.8% per smoke | `b3_shots.py` | `b3.json detected.Somers` |
| Gearing Not detected at the shot: 15.6% shots (10), 18.6% damage, 25.6% per smoke | `b3_shots.py` | `b3.json detected.Gearing` |
| Harugumo shots with radar cruiser inside 187, lit from inside 13 | `b3_shots.py` | `b3.json radar_cruiser_inside_split` |
| Harugumo radar-lit shots 89: elsewhere 75, inside 13 | `b3_shots.py` | `b3.json radar_detail.Harugumo` |
| Harugumo detected-no-radar by nearest ally | `b3_shots.py` | `b3.json spotter.Harugumo` |
| candidate spotters within the target detection range | `b3_shots.py` | `b3.json candidates` |
| not detected at the shot, by kind | `b3_shots.py` | `b3.json not_detected_detail` |
| Harugumo second destroyer: 3 km life 19.5%, 5 km 31.7%, at shot within 5 km 47.1% | `b3_shots.py` | `b3.json second_destroyer.by_ship.Harugumo` |
| Somers second destroyer: 3 km life 8.2%, 5 km 14.3%, at shot within 5 km 24.1% | `b3_shots.py` | `b3.json second_destroyer.by_ship.Somers` |
| Gearing second destroyer: 3 km life 6.2%, 5 km 12.9%, at shot within 5 km 10.9% | `b3_shots.py` | `b3.json second_destroyer.by_ship.Gearing` |
| second destroyer contrasts | `b3_shots.py` | `b3.json second_destroyer.contrasts` |
| Harugumo Top 6 vs Rest rows | `b3_shots.py` | `b3.json harugumo_top6_vs_rest` |
| snapshot check Harugumo: 46 of 53 same | `b3_shots.py` | `b3.json check_snapshot.Harugumo` |
| Harugumo second destroyer alive at the fully-laid moment (tracks) 94.0%, forward 61.0% | `b3_shots.py` | `b3.json second_destroyer.by_ship.Harugumo.at_capture_*` |
| Somers second destroyer alive at the fully-laid moment (tracks) 99.6%, forward 66.9% | `b3_shots.py` | `b3.json second_destroyer.by_ship.Somers.at_capture_*` |
| Gearing second destroyer alive at the fully-laid moment (tracks) 95.6%, forward 51.7% | `b3_shots.py` | `b3.json second_destroyer.by_ship.Gearing.at_capture_*` |
| events damage vs smoke records | `b3_shots.py` | `b3.json check_damage` |
| radar inside two ways | `b3_shots.py` | `b3.json check_radar_inside` |
| Daring on Loop: 60 s before 17 of 48 (35.4%), chance 36.6% | `c5_loop.py` | `c5.json groups["Daring on Loop"].before_any_60` |
| Daring on other maps: 60 s before 61 of 152 (40.1%), chance 39.7% | `c5_loop.py` | `c5.json groups["Daring on other maps"].before_any_60` |
| Other cap sitters on Loop: 60 s before 16 of 40 (40.0%), chance 39.1% | `c5_loop.py` | `c5.json groups["Other cap sitters on Loop"].before_any_60` |
| Other destroyer smokes on Loop: 60 s before 19 of 54 (35.2%), chance 38.7% | `c5_loop.py` | `c5.json groups["Other destroyer smokes on Loop"].before_any_60` |
| All destroyer smokes, all maps: 60 s before 399 of 1074 (37.2%), chance 42.2% | `c5_loop.py` | `c5.json groups["All destroyer smokes, all maps"].before_any_60` |
| Daring on Loop: near cap 60 s before 2 of 48; after 5 | `c5_loop.py` | `c5.json groups["Daring on Loop"].before_near_60 / after_near_60` |
| Daring on other maps: near cap 60 s before 25 of 152; after 36 | `c5_loop.py` | `c5.json groups["Daring on other maps"].before_near_60 / after_near_60` |
| Other cap sitters on Loop: near cap 60 s before 9 of 40; after 14 | `c5_loop.py` | `c5.json groups["Other cap sitters on Loop"].before_near_60 / after_near_60` |
| Other destroyer smokes on Loop: near cap 60 s before 7 of 54; after 12 | `c5_loop.py` | `c5.json groups["Other destroyer smokes on Loop"].before_near_60 / after_near_60` |
| All destroyer smokes, all maps: near cap 60 s before 129 of 1074; after 227 | `c5_loop.py` | `c5.json groups["All destroyer smokes, all maps"].before_near_60 / after_near_60` |
| reverse: 62 episodes, 55 with Daring alive, 14 followed; base 21.5% | `c5_loop.py` | `c5.json reverse` |
| sequence summary: 17 matched, radar ships, median lead 40.5 s | `c5_loop.py` | `c5.json summary / sequences` |
| Daring on other maps Top 6 vs Rest before_any_60 18.5 | `c5_loop.py` | `c5.json groups["Daring on other maps"].top6_vs_rest_before_any_60` |
| Other cap sitters on Loop Top 6 vs Rest before_any_60 20.0 | `c5_loop.py` | `c5.json groups["Other cap sitters on Loop"].top6_vs_rest_before_any_60` |
| Other destroyer smokes on Loop Top 6 vs Rest before_any_60 -27.8 | `c5_loop.py` | `c5.json groups["Other destroyer smokes on Loop"].top6_vs_rest_before_any_60` |
| All destroyer smokes, all maps Top 6 vs Rest before_any_60 8.6 | `c5_loop.py` | `c5.json groups["All destroyer smokes, all maps"].top6_vs_rest_before_any_60` |
| C5 checks | `c5_loop.py` | `c5.json check` |

Round 5 numbers quoted in the "Changed from round 5" blocks are copied from `wows-toolkit/smoke/analysis/round5/FINDINGS.md` (B3 "Who spots for the Harugumo?" and the Harugumo table; C5-LP-4 table) and are constants in `n3_findings.py` (`R5N`, `R5D2`, `R5C`).
