# Round 4: fixes to Round 3 and where the new work is

Batch: `output/20261117-122135` (the published batch). Everything is association, not cause.

## Where things are

- **Smoke Atlas package:** `atlas/` and `atlas.zip` (copy, spots.json, caps.json, maps, working figures, CHECK.md, README.md).
- **Part B, signature spots:** `round4/part-b/SPOTS.md`.
- **Part D, clan styles:** `round4/part-d/STYLES.md`.
- **Part E, ship variance:** `round4/part-e/SHIP-VARIANCE.md`.
- **Round 3 modules, updated in place:** `round3/module-N/MODULE-N.md`; each folder has `CHANGES-R4.md` with every number that changed, old to new.

## Part A: what was fixed

1. **Radar partner, one definition.** Headline is now "a radar cruiser inside the smoke".
   - Module 2's old 93% vs 70% counted a radar cruiser covered in any way (inside, behind or in the line of fire), on early Harugumo, Somers and Gearing smokes.
   - Module 3's old 77% vs 62% counted a radar ship of any class inside, on early stacked destroyer smokes.
   - New headline, all early destroyer smokes: Top 6 60% (61 of 102), Rest 35% (70 of 200), gap +25 points (+13 to +36). Both modules report it.
   - Per map the Top 6 are ahead everywhere except Sleeping Giant (47% vs 59%, -13, interval -41 to +18). Hotspot is the clearest: 87% vs 38%.
   - On the three ships: 82% vs 51% (+15 to +46).
2. **Radar plays per team-game: 0.47 vs 0.19** (+0.14 to +0.40), used everywhere. This counts destroyer smokes whose primary purpose is a radar play: 96 smokes, 52 Top 6 and 44 Rest. Round 3's 0.50 counted any radar tag (100 smokes); it was a wider definition, not an error. Module 3 is recomputed on the new set.
3. **Smoke-type labels** are Module 1's four habits everywhere: flank smoke lines, cap sitters, parked cruiser smoke, moving exhaust. Module 5 section 2 is redone on them.
4. **Loader** matches detail records on game + smoke id. All five modules were rerun.
5. **Module 4** has the line that the earlier scouting report used H-SR, RESIN and PN data only.

## Numbers that changed

**From the loader fix (small).** Two or three smokes moved. No conclusion changed.
- Module 1: no number in the write-up changed. Four cell shares were also corrected by a point each (they had been added up from rounded figure values).
- Module 4: Hotspot F10 15.1k to 14.2k (n 23 to 22); Hotspot D zone 13.2k to 13.0k; Hotspot B zone 15.1k to 15.6k; Land of Fire A Rest share 50% to 49%; Land of Fire F3 6.0k to 5.5k (n 10 to 11); "contested cap is not the nearest cap" 159 to 158.
- Modules 2, 3 and 5: interval end points moved by a point or two; listed in each `CHANGES-R4.md`.

**From the definition changes (these alter findings).**
- **Module 2, what a radar cruiser inside goes with.** On the stricter definition it is no longer a damage gap (+1.3k, -3.9k to +6.8k; it was +7.6k) but a cap gap: the cap was taken after 58% of early smokes with a radar cruiser inside against 14% when the cruiser was covered but not inside.
- **Module 3.** Plays 100 to 96; RESIN 17 to 14 plays, so H-SR now has the highest rate; Mountain Range 18 to 15; Mountain Range cap A 4 plays to 1.
- **Module 5, counter-smokes.** Across all destroyers they still return less (8.0k vs 11.2k, -5.5k to -0.9k), but inside one habit the gap is not reliable (flank smoke lines 13.7k vs 16.0k, -7.2k to +2.1k). Cap sitters counter-smoke more often, which is part of the overall gap.
- **Module 5, clan fingerprints.** With habit shares as features H-SR is no longer on its own branch; RESIN and BONKZ are still its nearest clans.

## Things to know before design

- **Signature spots are small n.** Six passed the rule, each on 11 to 15 Top 6 smokes. Running the same search with six Rest clans standing in as the top group passes 2.5 spots on average, so 2 or 3 of the six are the kind any group shows. The two tightest are Land of Fire Svea at F5 and Sleeping Giant Harugumo at G1/F1.
- **Earlier examples that did not hold:** Sleeping Giant "Top 6 Daring west" is HTDOG alone; Mountain Range Gearing and Somers under B and C are used by the Rest at nearly the same rate; Hotspot's east edge (G10/F10) is more a Rest spot than a Top 6 one.
- **Supporting cast** is read at one moment per smoke, when it was fully laid; the batch has no other ship positions. A median of about 4 allied ships have a recorded position, so "no second destroyer recorded" does not mean none was there.
- **Spotting** cannot be attributed from the batch. "Nearest allied ship to the target" is the stand-in, at a median of 8 to 9 km: read it as who was closest, not who spotted.
- **KITE** sits nearer the long-smoke style than midway between the two.
