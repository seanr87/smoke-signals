# Round 5c check: where every number comes from

Batch `output/20261117-230933`. Scripts run as `python -I -X utf8 <script>` from their own folder. Shared definitions:
`r5clib.py` (two death metrics, replay-clock early, cap results from the cap timeline) on top of `../round5b/r5lib.py`
and `../round5b/tl.py`.

## Independent recheck by the main session

Every headline number was recomputed in separate scripts that do not use the workers' code (`verify/verify_x1.py`,
`verify/verify_x2_x3.py`), before the package was assembled.

| Item | Worker's number | Recheck |
|---|---|---|
| Base counts: destroyer smokes died / caught; early destroyer smokes | 194 / 124; 308 | same |
| 1. A1 cap-contest smokes; we took the contested cap, Rest: radar cruiser inside / no cruiser | 391; 77% (of 22) / 19% (of 85) | same |
| 1. A1 same, Top 6 | 60% (of 30) / 70% (of 23) | same |
| 1. A1 smokes with a radar cruiser inside; radar pressed from the smoke | 104; 8 | same |
| 2. A2 50+ behind: died / caught, with against without | 34.9 against 12.4; 23.1 against 7.5 | same |
| 2. A2 covered ship radar-lit (388 smokes): died / caught | 27.1 against 13.1; 20.9 against 6.3 | same |
| 2. A2 calm smokes | 513; died 8.9; caught 3.7 | same |
| 2. A2 radar-lit in the last 40 s: died / caught | 85 of 194; 65 of 124 | same |
| 2. A2 still radar-lit at death: died / caught | 39; 34 | 37; 33 (the recheck allows a lit span to end up to 2 s before the death; the worker's rule is a little wider) |
| 3. A3 Somers / Gearing, Top 6: died; caught | 17.8 / 16.2; 7.8 / 9.5 | same |
| 3. A3 Somers / Gearing, Rest: died; caught | 19.4 / 32.3; 11.8 / 23.6 | same |
| 4. A4 counter-smokes: died / caught per 100 | 133; 24.8 / 15.0 | same |
| 5. B2 smoker died / caught per 100: Italian cruisers; ordinary cruiser smoke | 18.5 / 16.1; 8.2 / 6.3 | same |
| 5. B2 battleships: died / caught per 100 | 17.6 / 8.8 | same |
| 6. B3 long smokes, Top 6 against Rest: died; caught | 15.2 against 25.2; 8.0 against 18.8 | same |
| 7a. Sleeping Giant G1: we took; enemy took the nearest cap | 29% of 21; 7 of 13 | same |
| 8. D1 Top 6 against Rest: died; caught; smoker died; smoker caught | 12.3 / 19.3; 7.8 / 13.4; 8.2 / 15.1; 4.3 / 9.2 | same |
| 8. D1 nearest cap taken; contested cap taken | 39% / 28%; 32% / 23% | same |

Not rechecked by the main session: the intervals; the "no other detection" reading of radar deaths; the undetected share
from the track (item 5); items 7b to 7d (membership rebuilt by the worker from the Round 5 scripts); per-clan values and the
style grouping in item 8 beyond the Top 6 against Rest rows; the counter-smoke angle bands. No figures were made.
One difference a worker reported and did not trace: caught deaths radar-lit in the last 20 seconds come out at 57, where
Round 5b had 56.

Part 1 of this run (code review fixes on `r5b`) was checked separately: 31 unit tests, the repeatability test and the
reference-game test pass, and a two-game trial into a scratch folder matched the batch file by file (36 files) apart from
revision, timestamp and the two known last-digit rounding fields.
