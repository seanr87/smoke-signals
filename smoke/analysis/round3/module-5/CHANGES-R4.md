# Module 5: what changed in round 4

Old = `MODULE-5-r3.md`. New = `MODULE-5.md`. Numbers not listed did not change.

## Loader fix (records matched on game + smoke id) and rerun

Point values barely moved. Most of these are intervals, which also shift a little on every run because they come from random resampling.

| Section | Number | Old | New |
|---|---|---|---|
| 1 | Rest shooter share (cruiser / smoker / battleship) | 68% / 24% / 5% | 69% / 24% / 6% |
| 1 | Top minus rest cruiser share | +3 points, -6.5 to +12.4 | +2 points, -7.7 to +11.3 |
| 3 | Opening rate gap interval (first 2 min) | -0.04 to +0.29 | -0.06 to +0.28 |
| 3 | Return gap interval, 8 to 12 min | -0.3k to +8.2k | -0.1k to +8.1k |
| 3 | Ahead minus behind, deaths per 100 | -24.0 to -10.2 | -24.8 to -10.5 |
| 3 | Ahead minus behind, return | +0.5k to +5.5k | +0.7k to +5.5k |
| 3 | Top vs rest deaths at level score | -12.0 to -4.4 | -11.6 to -4.5 |
| 4 | Radar caught vs not, deaths per 100 | +6.4 to +27.2 | +6.9 to +27.5 |
| 4 | Inside cap vs 3 km+ | -7.9 to +4.6 | -7.6 to +4.5 |
| 4 | Top vs rest deaths per 100 | -10.9 to -2.6 | -11.0 to -2.1 |
| 5 | Average selfish share across clans (typo fix) | 46% | 45% |
| 6 | Top vs rest counter-smoke share | -6.9 to +4.7 | -6.4 to +4.8 |
| 6 | Top vs rest counter-smoke return | -0.1k to +8.7k | -0.1k to +8.8k |
| 6 | Chain vs solo return interval | -8.8k to +6.9k | -8.9k to +6.3k |
| Notes | Duplicate smoke ids | up to 3 smokes could carry another smoke's detail | fixed in the loader |

## Relabelled to habit clusters

| Section | Number | Old (long DD / short DD / cruiser / exhaust) | New (four habits) |
|---|---|---|---|
| 2 | Groups and n | long DD 802, short DD 256, cruiser 271, exhaust 215 (3 other) | flank smoke lines 562, cap sitters 462, parked cruiser smoke 241, moving exhaust 188 (94 other, left out) |
| 2 | Smokes per team-game | 2.35 / 0.75 / 0.79 / 0.63 | 1.64 / 1.35 / 0.70 / 0.55, now with intervals |
| 2 | Concealed damage per smoke | 13.1k / 3.7k / 8.9k / 4.7k | 15.8k / 5.3k / 8.4k / 4.1k |
| 2 | Deaths per 100 | 14.0 / 4.3 / 7.4 / 15.8 | 14.2 / 7.4 / 6.2 / 17.0 |
| 2 | Own-gun share | 16% / 78% / 95% / 91% | 8% / 65% / 94% / 91% |
| 2 | Return gap, first group minus second | long minus short: +7.3k to +11.0k | flank lines minus cap sitters: +8.5k to +12.4k |
| 2 | Death gap, first group minus second | +5.6 to +14.0 | +2.9 to +11.3 |
| 2 | Share with no concealed damage | short DD 43% | cap sitters 37%, moving exhaust 52% |
| 4 | Deaths by habit (new split) | not given | flank smoke lines 14.2 vs cap sitters 7.4, difference +2.9 to +11.2 |
| 4 | Somers vs Gearing (new) | not given | return 14.5k vs 16.3k, -1.8k (-5.4k to +3.4k); deaths 10.4 vs 17.8, -7.4 (-16.5 to -0.6) |
| 5 | Smoke-type features | long DD %, short DD %, cruiser smoke %, exhaust % | share of smokes in each of the four habits |
| 5 | H-SR's main smoke type | 89% long DD | 71% flank smoke lines (average 36%) |
| 5 | H-SR in the tree | its own branch | joins the main branch of 15 clans |
| 5 | Distance to H-SR: BONKZ | 1.04 | 1.02 |
| 5 | Nearest three stable when a feature is dropped | RESIN 18, BONKZ 18, BONKY 13 of 18 | RESIN, BONKZ, BONKY all 18 of 18 |
| 5 | Next nearest | BONKY, HFANS, EPOXY, PFANS (1.2 to 1.3) | BONKY 1.13, EPOXY 1.20, HFANS 1.26, PFANS 1.30, KITE 1.32 |
| 5 | Distance to H-SR: HTDOG / VRTUS / KITE | 2.27 / 1.88 / 1.39 | 2.25 / 1.82 / 1.32 |
| 5 | VRTUS cruiser smoke share | 35% (all cruiser smoke) | 32% (parked cruiser smoke) |
| 5 | Win rate vs distance to H-SR | -0.48 (-0.75 to -0.13) | -0.51 (-0.78 to -0.17) |
| 5 | PN to MZY / PN to H-SR | 1.04 / 1.57 | 1.06 / 1.58 |
| 6 | Counter vs other return, main destroyer smoke | long DD 10.2k vs 13.4k (n 86 / 716), -6.4k to -0.2k, reliable | flank smoke lines 13.7k vs 16.0k (n 52 / 510), -7.2k to +2.1k, not reliable |
| 6 | Counter vs other deaths per 100 | long DD 18.6 vs 13.4 (-5.5 to +17.3) | flank smoke lines 23.1 vs 13.3 (-4.1 to +26.7) |
| 6 | Counter vs other, second group | short DD 3.3k vs 3.8k (n 46 / 210) | cap sitters 4.0k vs 5.5k (n 74 / 388), -3.0k to +0.2k; deaths 8.1 vs 7.2 |
| 6 | Chain make-up | "a destroyer plus a cruiser" | "a cap sitter plus a parked cruiser smoke" |

The one conclusion that changed: in round 3 counter-smokes returned reliably less within long destroyer smoke. On the habit clusters the gap inside each habit is no longer reliable; the overall gap (8.0k vs 11.2k, -5.5k to -0.9k) is partly because cap sitters counter-smoke more often (16% vs 9%).

## Wording (association, not cause)

Rewritten: all six "For a player" lines (they now state what was observed, not advice that implies a result), section 4 title and "what kills" phrasing, "the top teams' edge", "wins with a different recipe", "answering second is answering from behind", "exhaust is the worst trade".
