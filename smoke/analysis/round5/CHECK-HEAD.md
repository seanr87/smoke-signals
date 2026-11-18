# Round 5 check: where every number comes from

Batch `output/20261117-122135`. All scripts run as `python -I -X utf8 <script>` from their own folder; `common.py` seeds the
random generator, so reruns give the same intervals. Shared definitions: `r5lib.py` (round 5) on top of `../round3/common.py`.

## Independent recheck by the main session

The headline numbers of every part were recomputed in separate scripts that do not use the parts' code
(`verify/verify_main.py`, `verify/verify_bd.py`, `verify/verify_c5.py`). All matched, with two small differences:

| Item | Part's number | Recheck | Note |
|---|---|---|---|
| A1 cap taken, radar cruiser inside / no cruiser, Top 6 and Rest | 53.3 / 47.8, 76.2 / 12.9 | same | verify_main.py |
| A2 deaths per 100: Top 6 7.5, Rest 13.8; calm smokes 585 with 17 deaths; by score state | same | same | verify_main.py |
| A3 Somers / Gearing by group: 7.8, 11.8, 9.5, 23.6 | same | same | verify_main.py |
| A4 133 counter-smokes; radar cruiser inside 32 at 18,316; all 8,003 | same | same | verify_main.py |
| C1 cap_defended 486 (31.4%); enemy took yes 184 / no 889 / n.a. 474; within 2 km 8.5% vs 15.2% | same | same | verify_main.py |
| C2 teams with more caps at 8:00 won | 60 of 91 | 61 of 92 | one game differs; the cause was not traced and it does not change the reading |
| C3 Hotspot inside cap C: 22 smokes, 7 hurt, no Top 6 | same | same | verify_main.py |
| C4 Sleeping Giant G1: 21 smokes, 24.1k vs 10.7k | same | same | verify_main.py |
| B1 Daring / Gdansk: 671 m, 42.5%, 43.5%, 3,623 / 1,544 m, 26.3%, 56.8%, 8,205 | same | same | verify_bd.py |
| B2 smoker died per 100: 16.1 / 6.3 / 7.5 | same | same | verify_bd.py |
| B3 own-gun share 21.6 / 5.9 / 3.1% | same | same | verify_bd.py |
| B4 length bands Shimakaze 15 / 2 / 39, Grozovoi 6 / 11 / 10 | same | same | verify_bd.py |
| D1 radar cruiser inside 47% vs 29%; D2 smoke cruisers per game 0.3 vs 1.2; D3 H-SR and HTDOG headline values | same | same | verify_bd.py |
| C5 Sleeping Giant Somers west 17% vs 51%; after 5:00 1 of 22 vs 15 of 30 | same | same | verify_c5.py |
| C5 Hotspot west caps | 36% vs 14% | 35% vs 12% | the part counts by nearest cap; the recheck by the batch's contested cap |
| C5 Hotspot early radar cruiser inside 87% vs 38%; Loop 0.70 early smokes per team-game; Okinawa top 5 ships | same | same | verify_c5.py |

Not rechecked by the main session: the intervals themselves (they come from the shared `boot_diff` / `boot_stat`), the
placebo and shuffle runs, the principal-component and grouping work in D2, and the per-spot clan lists beyond Hotspot cap C.
Figures: 33 working figures. The workers report viewing at least 8 of them (A 3, B 3, C1 2); the main session viewed 3 more (c4-sg, c5-sg-somers-east-west, d2-style-map). The rest were not viewed.

How the part files were written: workers A, B, C1, C5 and D returned their findings text in their reports and the main
session saved it unchanged into `part-*/FINDINGS-*.md` and `CHECK-*.md`. Part C4's files were written by its own script.
