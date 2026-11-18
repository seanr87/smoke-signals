# CHECK-X1: where each headline number comes from

All scripts are in `round5c/x1-topics/`; shared helpers in `xlib.py`; definitions in `round5c/r5clib.py`. Tables are also in `topics.json` (key = item) and `out-aN.json`.

| headline number | script | variable | value |
|---|---|---|---|
| A1 n cap-contest smokes | a1.py | len(CC) | 391 |
| A1 Rest: radar cruiser inside vs no cruiser, we took the contested cap % | a1.py | T1 / J['by_cover'][..]['we_took_c'] | 77.27 vs 18.82 |
| A1 Top 6: radar cruiser inside vs no cruiser, we took the contested cap % | a1.py | T1 / J['by_cover'][..]['we_took_c'] | 60.0 vs 69.57 |
| A1 gap radar cruiser inside minus no cruiser, we took contested: Rest / Top 6 | a1.py | T3 / J['cover_gaps'] | +58.5 (+43.0 to +75.5 *) / -9.6 (-29.0 to +3.8) |
| A1 gap radar cruiser inside minus no cruiser, all: damage, died, caught | a1.py | T3 / J['cover_gaps'] | +13,368 (+8,699 to +17,029 *); -0.1 (-8.9 to +9.7); +3.2 (-4.3 to +10.6) |
| A1 pressed minus not pressed, all: damage, died, caught | a1.py | T5 / J['pressed_gaps'] | +5,826 (-18,281 to +17,351); -15.8 (-25.0 to -7.2 *); -11.5 (-17.3 to -4.9 *) |
| A1 wider reading, press minus no press, all: damage, we took contested, died, caught | a1.py | T8 / J['pressed_wide_gaps'] | +2,530 (-5,432 to +9,471); +1.5 (-15.7 to +23.2); +10.9 (-6.5 to +26.5); +9.7 (-4.7 to +25.9) |
| A2 baseline died / caught per 100 | a2.py | J['baseline'] (death_rates(DD)) | 194 ships, 18.18 / 124, 11.55 |
| A2 50+ behind: died with / without; caught with / without | a2.py | T1 / J['conditions'] key behind | 34.91 / 12.37; 23.1 / 7.53 |
| A2 radar-lit covered ship: died with / without; caught with / without | a2.py | T1 / J['conditions'] key lit_covered | 27.06 / 13.11; 20.88 / 6.27 |
| A2 calm smokes: n, died per 100, caught per 100 | a2.py | CALM / J['calm'] | 513, 8.86, 3.7 |
| A2 radar deaths, died: (a) / (b) / (c) of n | a2.py | RAD['died']['ways'] (DIED_D, judge()) | 85 / 39 / 25 of 194 |
| A2 radar deaths, caught: (a) / (b) / (c) of n | a2.py | RAD['caught']['ways'] (CAUGHT_D, judge()) | 65 / 34 / 20 of 124 |
| A2 caught, radar-lit in the last 20 s | a2.py | RAD['caught']['ways']['a20'] | 57 |
| A3 Top 6: Somers vs Gearing, died / caught per 100 | a3.py | T1 / J['rates'] | 17.78 vs 16.22 / 7.78 vs 9.46 |
| A3 Rest: Somers vs Gearing, died / caught per 100 | a3.py | T1 / J['rates'] | 19.41 vs 32.32 / 11.76 vs 23.58 |
| A3 Somers minus Gearing inside Rest: died / caught | a3.py | T2 / J['somers_minus_gearing'] | -12.9 (-24.5 to -0.4 *) / -11.8 (-23.7 to -2.1 *) |
| A3 Somers minus Gearing inside Top 6: died / caught | a3.py | T2 / J['somers_minus_gearing'] | +1.6 (-18.2 to +17.4) / -1.7 (-6.7 to +4.9) |
| A3 Gearing, Top 6 minus Rest: died / caught | a3.py | T3 / J['top6_minus_rest'] | -16.1 (-30.4 to -3.6 *) / -14.1 (-26.6 to -4.8 *) |
| A4 n counter-smokes, usable line of fire | a4.py | len(CS), len(USE) / J['summary'] | 133, 132 |
| A4 all counter-smokes: died / caught per 100 | a4.py | T_PAYS / J['what_pays'] row 'all counter-smokes' | 24.81 / 15.04 |
| A4 flanking: died / caught per 100; head-on: died / caught | a4.py | T_ANGLE / J['by_angle'] | 50.0 / 25.0; 24.0 / 15.0 |
| A4 flanking minus head-on: died / caught | a4.py | T_DIFF / J['flanking_minus_head_on'] scope All | +26.0 (-5.0 to +63.3) / +10.0 (-15.4 to +41.1) |
| A4 Gearing counter-smokes: died / caught per 100 | a4.py | T_PAYS row 'Gearing' | 45.0 / 35.0 |
