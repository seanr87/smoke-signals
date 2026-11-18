# Round 5c findings: the remaining Round 5 items on fixed definitions

Batch: `output/20261117-230933` (smoke-signals 0.4.0). Analysis only: no code change, no batch rerun.
Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS; Rest = the other 24 clans. Minimum n 8 (8 to 14 small n). 95% intervals by
resampling whole clans. Everything is association, not cause.

**Definitions used everywhere in this round**

- **Two death metrics, side by side.** "Died" = a covered ship (the smoker, or a ship the batch lists as inside or behind
  the smoke) whose death falls between activation and exactly 20 seconds after the smoke dispersed, from the exact death
  time in the game record; each ship is counted once, with the last smoke that covered it. "Caught" = the batch
  `smoke_deaths` list. Destroyer smokes: 194 ships died (18.2 per 100 smokes) against 124 caught (11.5 per 100).
  The 9 smokes of the single-replay game laid by the team with no replay are left out of every "died" rate.
- **Early** = replay clock under 300 seconds at activation: 308 destroyer smokes (Round 5b had 306 on the HUD clock).
- **Cap results** come from the cap timeline on one cap fixed at activation, counting owner changes up to 60 seconds after
  the smoke dispersed, for the contested cap and for the nearest cap. `cap_won` and the snapshot fields are not used.

## 1. Verdicts

| Item | Answer in one line | Top 6 or Shared | Verdict | Changed from Round 5b? |
|---|---|---|---|---|
| 1. A1 cap-contest smokes by cover | Rest took the contested cap after 77% of smokes with a radar cruiser inside against 19% with no cruiser. Top 6: 60% against 70%, not clear. Radar pressed from the smoke: only 8 of the 104 smokes. | The cap gain is a Rest pattern | Keep; radar pressed is a lead only | "We took" rises on the timeline (Top 6 with no cruiser 48% to 70%) |
| 2. A2 smoke deaths | 50+ behind: died 34.9 against 12.4 per 100, caught 23.1 against 7.5. A covered ship radar-lit: died 27.1 against 13.1, caught 20.9 against 6.3. Calm smokes: 513, died 8.9, caught 3.7. | Rates are lower for the Top 6; conditions are Shared | Keep | "Died" is new; calm smokes 3.7 becomes 8.9 on "died" |
| 2. A2 radar deaths | Caught (124): radar-lit in the last 40 s 65, still lit at death 34, lit at death with no other detection found 20. Died (194): 85, 39, 25. | Shared | Keep the first two; the third is an upper limit | Three readings replace one |
| 3. A3 Somers against Gearing | Top 6: no difference on either metric. Rest: Gearing loses more, clear on both (died 19.4 against 32.3; caught 11.8 against 23.6). | Team, not ship | Keep | "Died" added; same reading |
| 4. A4 counter-smokes | 24.8 died and 15.0 caught per 100, above all destroyer smokes (18.2 and 11.5). Flanking against head-on: not clear on either metric (12 flanking smokes). | Shared | Keep "what pays"; angle and deaths a lead only | "Died" added |
| 5. B2 getaway smokes | Italian cruiser smoker died 18.5 per 100 (caught 16.1) against 8.2 (6.3) for ordinary cruiser smoke, clear on both. Battleships: 17.6 died, 8.8 caught, no clear gap. Undetected share of the smoke's life from the track: 79.3%, 71.3%, 85.0%. | Shared | Keep | Undetected share corrected upward; battleship deaths double on "died" |
| 6. B3 long smokes | Top 6 against Rest: died 15.2 against 25.2, caught 8.0 against 18.8, both clear. No gap in games won. In games lost "caught" stays clear, "died" does not. | Top 6 lose fewer; mostly goes with winning | Keep | "Died" added |
| 7a. High-paying cells | Cells pay in damage; the cap is not taken more often there. G1: we took after 29% of 21; the enemy took cap A after 7 of 13. | Shared | Keep | 19% becomes 29% at G1; Hotspot 34% becomes 40% |
| 7b. Sleeping Giant cap B | Enemy took B after 1 of 28; we took it after 7 of 18. Not there to stop the enemy taking B. | Shared | Drop the defence reading | 5 becomes 7 |
| 7c. Mountain Range radar at B | B lost after 5 of 9 laid on a held cap. | Top 6 by count | Keep the spot; drop "defends B" | 4 of 8 becomes 5 of 9 |
| 7d. Loop cap sitters at B | We took B after 11 of 17: Top 6 7 of 9, Rest 4 of 8. | Top 6 (gold) | Keep | 5 of 10 and 1 of 8 become 7 of 9 and 4 of 8 |
| 8. D1 clan scores | Top 6 against Rest: died 12.3 against 19.3 per 100 smokes, caught 7.8 against 13.4, nearest cap taken 39% against 28%, all clear. Nearest cap not lost: 86% against 83%, Shared. | As stated | Keep | Caps taken now clear; "not lost" on the nearest cap now Shared |
| 8. D2 styles | No clan changes style (0 of 30). | As Round 5b | Lead | No |
| 8. D3 profiles | Gauge values identical for all 30 clans; each clan gains the new scores. | n/a | Keep | 11 score keys added, 6 removed |

Items not redone in Round 5c (B1, B4, C1, C2, C3, the rest of C4 and C5, the page 1 re-tests) stand as in Round 5b; see the
last section.

## 2. Package fixes

**Four summary lines, reworded to what the numbers support**

| Subject | Round 5b line | Round 5c line |
|---|---|---|
| Radar cruiser inside and the cap | "does not hold" | **The cap link holds at about half the size, mainly for the Rest.** Early smokes with a radar cruiser inside were followed by taking the cap more often (59% against 37% on the nearest cap, 47% against 32% on the contested cap, both clear), where the atlas said 58% against 14%. In cap-contest smokes the gain is the Rest's (77% against 19%); the Top 6 take the cap as often without one. |
| Radar and smoke deaths | "radar is behind half of smoke deaths" | **A ship was radar-lit shortly before death in about half of smoke deaths, and still lit at death in about a quarter.** Caught: 65 of 124 (52%) in the last 40 seconds, 34 (27%) at death. Died: 85 of 194 (44%) and 39 (20%). Most of those lit at death were already detected another way before the radar reached them. |
| Leaving the smoke | "leaving is not the risky moment" | **No difference shown between leaving a smoke and staying in it.** Destroyers died at about 3 to 4 per 100 per 30 seconds inside, after leaving and after dispersal alike; the ships that leave and the ships that stay are in different situations, so this cannot show that leaving is safe. |
| Harugumo | "its targets are spotted by somebody else" | **The nearest friendly ship to a Harugumo's target is usually not the Harugumo.** A ship outside the smoke 45%, the Harugumo itself 31%, a second destroyer 24%, the radar cruiser inside 0.5% (410 shots). Who spotted is not recorded. |

**spots.json**

- Every record has `show` (true or false), `status` and `draw`.
- **Gold** (Top 6 spot, shown): `c5-lp-sitters-b`, `c5-lf-svea-f5`, `c5-sf-svea-h7`.
- **Leads** (shown, drawn neutral): the other six Top 6 records: `c5-sg-somers-east`, `c5-sg-harugumo-g1`, `c5-hs-cap-a`,
  `c5-hs-cap-b`, `c5-mr-parked-west`, `c5-mr-radar-b`.
- **Hidden** (`show` false): the five danger-zone candidates, `c5-ok-death-zone`, `c5-lp-f8`, `c5-lp-f10`.
- **No rates:** `c5-sf-early-d` (n 7).
- `deaths_per_100` is renamed `caught_per_100` (it always was the batch list). The cap numbers built on `cap_won` are
  removed; the five high cells and the Loop cap-sitter spot carry a `timeline` block with the Round 5c values.

## 3. Every number that changed from Round 5b

For an item Round 5b did not redo, "Round 5b" means the Round 5 number after the clock fix. Each block is that item's own old-to-new list. Package changes (spots.json, the four reworded lines) are in section 2 and in README.md.

**A1. Cap-contest smokes by cover, and radar pressed from the smoke** (`x1-topics/FINDINGS-X1.md`)

round 5b did not redo this table, so the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a1.json`). "-" = too few there. The contested-cap columns and the pressed split are new.

| number | round 5b | round 5c | why |
|---|---|---|---|
| radar cruiser inside, Top 6: we took the nearest cap % | 53.3 | 60.0 | cap timeline (was snapshots) |
| radar cruiser inside, Top 6: enemy took the nearest cap % | 9.1 | 11.4 | cap timeline (was snapshots) |
| radar cruiser inside, Top 6: deaths per 100, now died per 100 | 10.9 | 12.7 | new death metric |
| radar cruiser inside, Rest: we took the nearest cap % | 76.2 | 81.0 | cap timeline (was snapshots) |
| radar cruiser inside, Rest: enemy took the nearest cap % | 10.3 | 15.4 | cap timeline (was snapshots) |
| radar cruiser inside, Rest: deaths per 100, now died per 100 | 10.2 | 16.7 | new death metric |
| non-radar cruiser inside, Top 6: deaths per 100, now died per 100 | 12.5 | 25.0 | new death metric |
| non-radar cruiser inside, Rest: enemy took the nearest cap % | 37.5 | 50.0 | cap timeline (was snapshots) |
| non-radar cruiser inside, Rest: deaths per 100, now died per 100 | 33.3 | 11.1 | new death metric |
| no cruiser, Top 6: we took the nearest cap % | 47.8 | 69.6 | cap timeline (was snapshots) |
| no cruiser, Top 6: enemy took the nearest cap % | 5.4 | 16.2 | cap timeline (was snapshots) |
| no cruiser, Top 6: deaths per 100, now died per 100 | 4.3 | 13.0 | new death metric |
| no cruiser, Rest: we took the nearest cap % | 12.9 | 18.8 | cap timeline (was snapshots) |
| no cruiser, Rest: enemy took the nearest cap % | 20.0 | 23.2 | cap timeline (was snapshots) |
| no cruiser, Rest: deaths per 100, now died per 100 | 8.3 | 15.2 | new death metric |
| other, Top 6: we took the nearest cap % | 11.1 | 33.3 | cap timeline (was snapshots) |
| other, Top 6: enemy took the nearest cap % | 6.2 | 18.8 | cap timeline (was snapshots) |
| other, Top 6: deaths per 100, now died per 100 | 14.3 | 19.1 | new death metric |
| other, Rest: we took the nearest cap % | 57.1 | 60.0 | cap timeline (was snapshots) |
| other, Rest: enemy took the nearest cap % | 22.9 | 27.1 | cap timeline (was snapshots) |
| other, Rest: deaths per 100, now died per 100 | 13.8 | 20.7 | new death metric |

19 other numbers are unchanged: concealed damage in every row, and caught per 100 (it is the same list as round 5 deaths).

**A2. Smoke deaths: conditions, calm smokes, map, time and score, and radar deaths three ways** (`x1-topics/FINDINGS-X1.md`)

the "round 5b" column is `round5b/part-a/out-a2.json` (round 5 with the clock fix), or the round 5b redo N2 where the row says so.

| number | round 5b | round 5c | why |
|---|---|---|---|
| deaths in destroyer smokes: died (round 5b N1 counted 201 ships at risk in the smoke window) | 201 | 194 | new death metric: exactly 20 s after dispersal, each ship once, 9 smokes left out |
| 50+ behind at activation: deaths per 100 with / without, now died | 23.1 / 7.5 | 34.9 / 12.4 | new death metric |
| team outnumbered at activation: deaths per 100 with / without, now died | 27.3 / 8.0 | 39.3 / 13.4 | new death metric |
| a covered ship was seen by an enemy ship (surface lit): deaths per 100 with / without, now died | 19.1 / 4.6 | 27.1 / 10.0 | new death metric |
| a covered ship was lit for firing from smoke: deaths per 100 with / without, now died | 25.1 / 8.4 | 28.4 / 15.8 | new death metric |
| radar-lit covered ship: deaths per 100 with / without, now died | 20.9 / 6.3 | 27.1 / 13.1 | new death metric |
| calm smokes: n (round 5b N2) | 515 | 513 | lit_covered from the round 5c library in place of the radar test in the round 5b script; 2 smokes differ |
| calm smokes: deaths per 100, now died | 3.7 | 8.9 | new death metric |
| Sleeping Giant: deaths per 100, now died | 11.8 | 15.1 | new death metric |
| Hotspot: deaths per 100, now died | 7.7 | 15.7 | new death metric |
| Loop: deaths per 100, now died | 10.6 | 18.3 | new death metric |
| Mountain Range: deaths per 100, now died | 8.3 | 18.4 | new death metric |
| Land of Fire: deaths per 100, now died | 14.1 | 21.1 | new death metric |
| Sea of Fortune: deaths per 100, now died | 13.7 | 17.9 | new death metric |
| Okinawa: deaths per 100, now died | 22.0 | 29.3 | new death metric |
| ahead 50+: deaths per 100, now died | 6.5 | 12.9 | new death metric |
| level: deaths per 100, now died | 8.5 | 11.9 | new death metric |
| behind 50+: deaths per 100, now died | 23.1 | 34.9 | new death metric |
| 0-5 min: n | 306 | 308 | time from the replay clock (e0), not the HUD clock |
| 0-5 min: deaths per 100, now died | 7.5 | 8.5 | new death metric |
| 5-10 min: n | 495 | 494 | time from the replay clock (e0), not the HUD clock |
| 5-10 min: deaths per 100, now died | 12.5 | 21.8 | new death metric |
| 10-15 min: n | 247 | 246 | time from the replay clock (e0), not the HUD clock |
| 10-15 min: deaths per 100, now died | 14.2 | 22.4 | new death metric |
| 15+ min: deaths per 100, now died | 15.4 | 23.1 | new death metric |
| caught deaths radar-lit in the last 20 s (round 5b N2: 56 of 124) | 56 | 57 | same radar log; one death sits on the 20 s edge (which rule moved it was not traced) |
| died ships radar-lit in the last 40 s | - | 85 of 194 | new death metric |
| still radar-lit at death (died / caught) | - | 39 of 194 / 34 of 124 | new reading |
| radar-lit at death, no other detection found (died / caught) | - | 25 of 194 / 20 of 124 | new reading |

29 other compared numbers are unchanged (caught per 100 is the same list as round 5 deaths wherever the smokes in the row are the same).

**A3. Somers vs Gearing inside Top 6 and inside Rest** (`x1-topics/FINDINGS-X1.md`)

round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a3.json`).

| number | round 5b | round 5c | why |
|---|---|---|---|
| Top 6, Somers, all ships: deaths per 100, now died | 7.8 | 17.8 | new death metric |
| Top 6, Gearing, all ships: deaths per 100, now died | 9.5 | 16.2 | new death metric |
| Top 6, all ships: Somers minus Gearing, now caught | -1.7 (-6.9 to +4.7) | -1.7 (-6.7 to +4.9) | same list; interval now from diff_ci |
| Top 6, all ships: Somers minus Gearing, now died | -1.7 (-6.9 to +4.7) | +1.6 (-18.2 to +17.4) | new death metric |
| Top 6, Somers, smoker: deaths per 100, now died | 2.2 | 10.0 | new death metric |
| Top 6, Gearing, smoker: deaths per 100, now died | 1.4 | 8.1 | new death metric |
| Top 6, smoker: Somers minus Gearing, now caught | +0.9 (-7.7 to +5.7) | +0.9 (-7.6 to +5.6) | same list; interval now from diff_ci |
| Top 6, smoker: Somers minus Gearing, now died | +0.9 (-7.7 to +5.7) | +1.9 (-19.9 to +14.5) | new death metric |
| Top 6, Somers, sheltering cruisers: deaths per 100, now died | 5.9 | 8.2 | new death metric |
| Top 6, sheltering cruisers: Somers minus Gearing, now caught | -1.0 (-7.1 to +7.0) | -1.0 (-7.2 to +7.3) | same list; interval now from diff_ci |
| Top 6, sheltering cruisers: Somers minus Gearing, now died | -1.0 (-7.1 to +7.0) | +1.4 (-7.2 to +10.8) | new death metric |
| Rest, Somers, all ships: deaths per 100, now died | 11.8 | 19.4 | new death metric |
| Rest, Gearing, all ships: deaths per 100, now died | 23.6 | 32.3 | new death metric |
| Rest, all ships: Somers minus Gearing, now caught | -11.8 (-24.0 to -1.5) | -11.8 (-23.7 to -2.1) | same list; interval now from diff_ci |
| Rest, all ships: Somers minus Gearing, now died | -11.8 (-24.0 to -1.5) | -12.9 (-24.5 to -0.4) | new death metric |
| Rest, Somers, smoker: deaths per 100, now died | 4.7 | 10.6 | new death metric |
| Rest, Gearing, smoker: deaths per 100, now died | 13.2 | 23.2 | new death metric |
| Rest, smoker: Somers minus Gearing, now caught | -8.5 (-25.3 to +1.6) | -8.5 (-23.8 to +1.6) | same list; interval now from diff_ci |
| Rest, smoker: Somers minus Gearing, now died | -8.5 (-25.3 to +1.6) | -12.6 (-28.4 to +0.2) | new death metric |
| Rest, Somers, sheltering cruisers: deaths per 100, now died | 8.1 | 10.1 | new death metric |
| Rest, Gearing, sheltering cruisers: deaths per 100, now died | 11.8 | 9.6 | new death metric |
| Rest, sheltering cruisers: Somers minus Gearing, now caught | -3.8 (-10.4 to +6.5) | -3.8 (-10.4 to +7.0) | same list; interval now from diff_ci |
| Rest, sheltering cruisers: Somers minus Gearing, now died | -3.8 (-10.4 to +6.5) | +0.5 (-7.0 to +11.5) | new death metric |

13 other compared numbers are unchanged (the caught rates).

**A4. Counter-smokes: death rates by angle and for the "what pays" rows** (`x1-topics/FINDINGS-X1.md`)

round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a4.json`).

| number | round 5b | round 5c | why |
|---|---|---|---|
| head-on (under 30): deaths per 100, now died | 15.0 | 24.0 | new death metric |
| head-on (under 30): smoker died per 100, now smoker died | 7.0 | 16.0 | new death metric |
| oblique (30-60): deaths per 100, now died | 10.0 | 15.0 | new death metric |
| oblique (30-60): smoker died per 100, now smoker died | 5.0 | 10.0 | new death metric |
| flanking (over 60): deaths per 100, now died | 25.0 | 50.0 | new death metric |
| flanking (over 60): smoker died per 100, now smoker died | 16.7 | 41.7 | new death metric |
| radar cruiser inside: deaths per 100, now died | 18.8 | 28.1 | new death metric |
| radar cruiser inside: smoker died per 100, now smoker died | 3.1 | 12.5 | new death metric |
| Gearing: deaths per 100, now died | 35.0 | 45.0 | new death metric |
| Gearing: smoker died per 100, now smoker died | 10.0 | 20.0 | new death metric |
| flank-smoke-line ships: deaths per 100, now died | 23.1 | 32.7 | new death metric |
| flank-smoke-line ships: smoker died per 100, now smoker died | 5.8 | 15.4 | new death metric |
| laid 11-25 s after the enemy smoke: concealed damage | 12,296 | 10,922 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: deaths per 100, now caught | 18.6 | 20.9 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: deaths per 100, now died | 18.6 | 25.6 | new death metric |
| laid 11-25 s after the enemy smoke: smoker died per 100, now smoker caught | 7.0 | 9.3 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: smoker died per 100, now smoker died | 7.0 | 13.9 | new death metric |
| 6-9 km from the answered smoke: deaths per 100, now died | 19.6 | 29.4 | new death metric |
| 6-9 km from the answered smoke: smoker died per 100, now smoker died | 9.8 | 19.6 | new death metric |
| answered smoke within 30 degrees of straight ahead: deaths per 100, now died | 16.9 | 24.6 | new death metric |
| answered smoke within 30 degrees of straight ahead: smoker died per 100, now smoker died | 4.6 | 12.3 | new death metric |
| all counter-smokes: deaths per 100, now died | 15.0 | 24.8 | new death metric |
| all counter-smokes: smoker died per 100, now smoker died | 7.5 | 17.3 | new death metric |
| flanking minus head-on, deaths per 100, now caught | +10.0 (-13.1 to +35.0) | +10.0 (-15.4 to +41.1) | same list; interval now from diff_ci |
| flanking minus head-on, deaths per 100, now died | +10.0 (-13.1 to +35.0) | +26.0 (-5.0 to +63.3) | new death metric |

37 other compared numbers are unchanged (n, concealed damage and the caught rates wherever the row holds the same smokes).

**5. B2. Getaway smokes (exhaust and battleship smoke), both death metrics, and the undetected share from the track** (`x2-ships-maps/FINDINGS-X2.md`)

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Italian cruisers together: ships lost per 100 smokes | 17.9 (12.7 to 25.0) | caught 17.9 (12.7 to 25.0); died 20.2 (14.6 to 27.6) | caught unchanged; died is the new death metric |
| Italian cruisers together: smoker lost per 100 smokes | 16.1 (11.4 to 22.5) | caught 16.1 (11.5 to 22.3); died 18.5 (13.6 to 25.2) | caught unchanged; died is the new death metric |
| All battleships: ships lost per 100 smokes | 8.8 (0.0 to 17.6) | caught 8.8 (0.0 to 16.7); died 17.6 (8.0 to 28.6) | caught unchanged; died is the new death metric |
| All battleships: smoker lost per 100 smokes | 8.8 (0.0 to 16.7) | caught 8.8 (0.0 to 16.7); died 17.6 (8.1 to 29.2) | caught unchanged; died is the new death metric |
| Napoli: ships lost per 100 smokes | 16.3 (10.6 to 24.1) | caught 16.3 (10.8 to 25.0); died 19.0 (13.1 to 27.0) | caught unchanged; died is the new death metric |
| Napoli: smoker lost per 100 smokes | 15.0 (9.9 to 22.3) | caught 15.0 (9.8 to 21.8); died 17.7 (11.9 to 25.0) | caught unchanged; died is the new death metric |
| Venezia: ships lost per 100 smokes | 28.6 (11.1 to 60.0) | caught 28.6 (11.1 to 60.0); died 28.6 (11.1 to 60.0) | caught unchanged; died is the new death metric |
| Venezia: smoker lost per 100 smokes | 23.8 (11.1 to 40.0) | caught 23.8 (11.1 to 40.0); died 23.8 (11.1 to 40.0) | caught unchanged; died is the new death metric |
| C. Colombo (battleship): ships lost per 100 smokes | 10.0 (0.0 to 23.8) | caught 10.0 (0.0 to 23.8); died 25.0 (9.1 to 42.1) | caught unchanged; died is the new death metric |
| C. Colombo (battleship): smoker lost per 100 smokes | 10.0 (0.0 to 23.8) | caught 10.0 (0.0 to 23.5); died 25.0 (10.0 to 41.2) | caught unchanged; died is the new death metric |
| Conte Verde (battleship): ships lost per 100 smokes | 11.1 | caught 11.1; died 11.1 | caught unchanged; died is the new death metric |
| Conte Verde (battleship): smoker lost per 100 smokes | 11.1 | caught 11.1; died 11.1 | caught unchanged; died is the new death metric |
| Baseline: all smokes: ships lost per 100 smokes | 11.4 (9.4 to 13.9) | caught 11.4 (9.6 to 13.9); died 16.8 (14.1 to 20.5) | caught unchanged; died is the new death metric |
| Baseline: all smokes: smoker lost per 100 smokes | 7.5 (5.9 to 9.8) | caught 7.5 (5.8 to 9.7); died 12.7 (10.3 to 16.1) | caught unchanged; died is the new death metric |
| Baseline: all other smokes (not exhaust, not battleship): ships lost per 100 smokes | 10.8 (8.8 to 13.5) | caught 10.8 (9.0 to 13.5); died 16.4 (13.4 to 20.2) | caught unchanged; died is the new death metric |
| Baseline: all other smokes (not exhaust, not battleship): smoker lost per 100 smokes | 6.4 (4.6 to 8.9) | caught 6.4 (4.6 to 8.7); died 11.8 (9.3 to 15.6) | caught unchanged; died is the new death metric |
| Baseline: cruiser smokers with ordinary smoke: ships lost per 100 smokes | 7.4 (5.2 to 10.1) | caught 7.4 (5.0 to 10.5); died 9.3 (7.0 to 12.5) | caught unchanged; died is the new death metric |
| Baseline: cruiser smokers with ordinary smoke: smoker lost per 100 smokes | 6.3 (4.2 to 9.3) | caught 6.3 (4.3 to 9.3); died 8.2 (6.1 to 11.4) | caught unchanged; died is the new death metric |
| Baseline: all cruiser smokers: ships lost per 100 smokes | 11.4 (9.4 to 14.0) | caught 11.4 (9.4 to 14.0); died 13.5 (11.0 to 16.8) | caught unchanged; died is the new death metric |
| Baseline: all cruiser smokers: smoker lost per 100 smokes | 10.0 (8.2 to 12.4) | caught 10.0 (8.1 to 12.5); died 12.1 (9.9 to 15.1) | caught unchanged; died is the new death metric |
| Baseline: destroyer smokers: ships lost per 100 smokes | 11.5 (9.2 to 14.5) | caught 11.5 (9.2 to 14.4); died 18.2 (14.7 to 22.5) | caught unchanged; died is the new death metric |
| Baseline: destroyer smokers: smoker lost per 100 smokes | 6.4 (4.3 to 9.4) | caught 6.4 (4.4 to 9.0); died 12.7 (9.9 to 16.7) | caught unchanged; died is the new death metric |
| Italian cruisers minus cruisers with ordinary smoke: ships lost per 100 | +10.5 (+3.4 to +18.8), clear | caught +10.5 (+3.7 to +18.4), clear; died +10.9 (+4.0 to +18.5), clear | new death metric (caught interval differs only by resampling) |
| Italian cruisers minus cruisers with ordinary smoke: smoker lost per 100 | +9.8 (+3.3 to +17.3), clear | caught +9.8 (+3.3 to +16.8), clear; died +10.3 (+3.3 to +17.3), clear | new death metric (caught interval differs only by resampling) |
| Italian cruisers minus all other smokes: ships lost per 100 | +7.1 (+0.9 to +15.4), clear | caught +7.1 (+1.3 to +15.2), clear; died +3.9 (-3.3 to +12.9) | new death metric (caught interval differs only by resampling) |
| Italian cruisers minus all other smokes: smoker lost per 100 | +9.7 (+4.2 to +17.1), clear | caught +9.7 (+4.0 to +16.9), clear; died +6.6 (+0.0 to +14.5), clear | new death metric (caught interval differs only by resampling) |
| Battleships minus cruisers with ordinary smoke: ships lost per 100 | +1.4 (-7.2 to +10.7) | caught +1.4 (-7.3 to +11.1); died +8.4 (-2.0 to +20.9) | new death metric (caught interval differs only by resampling) |
| Battleships minus cruisers with ordinary smoke: smoker lost per 100 | +2.6 (-6.3 to +11.4) | caught +2.6 (-6.3 to +12.6); died +9.5 (-0.4 to +22.2) | new death metric (caught interval differs only by resampling) |
| Battleships minus all other smokes: ships lost per 100 | -1.9 (-11.1 to +6.9) | caught -1.9 (-10.9 to +6.4); died +1.3 (-9.8 to +13.2) | new death metric (caught interval differs only by resampling) |
| Battleships minus all other smokes: smoker lost per 100 | +2.4 (-5.9 to +10.5) | caught +2.4 (-6.3 to +10.6); died +5.8 (-5.2 to +17.5) | new death metric (caught interval differs only by resampling) |
| Battleships minus Italian cruisers: ships lost per 100 | -9.0 (-19.7 to +1.4) | caught -9.0 (-19.9 to +0.6); died -2.6 (-13.7 to +9.1) | new death metric (caught interval differs only by resampling) |
| Battleships minus Italian cruisers: smoker lost per 100 | -7.2 (-18.0 to +2.6) | caught -7.2 (-17.8 to +2.0); died -0.8 (-11.4 to +11.0) | new death metric (caught interval differs only by resampling) |
| Italian cruisers together: smoker undetected, % of time under the smoke | 81.7 (76.6 to 85.6) | batch field 81.7 (76.9 to 85.3); track, while inside 80.9 (75.9 to 84.8) | batch field unchanged; track figure is new |
| Italian cruisers together: smoker undetected, % of the smoke's whole life | 69.9 (63.2 to 74.4) | track 79.3 (74.1 to 83.2) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| All battleships: smoker undetected, % of time under the smoke | 71.7 (58.5 to 80.2) | batch field 71.7 (59.3 to 80.5); track, while inside 73.3 (61.9 to 81.5) | batch field unchanged; track figure is new |
| All battleships: smoker undetected, % of the smoke's whole life | 61.8 (50.3 to 69.6) | track 71.3 (60.2 to 78.5) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| Baseline: cruiser smokers with ordinary smoke: smoker undetected, % of time under the smoke | 90.1 (86.6 to 92.5) | batch field 90.1 (86.2 to 92.5); track, while inside 86.5 (82.6 to 89.0) | batch field unchanged; track figure is new |
| Baseline: cruiser smokers with ordinary smoke: smoker undetected, % of the smoke's whole life | 65.8 (60.2 to 71.5) | track 85.0 (80.7 to 88.0) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| Baseline: all smokes: smoker undetected, % of time under the smoke | 87.1 (85.1 to 88.6) | batch field 87.1 (84.9 to 88.7); track, while inside 84.5 (82.0 to 86.1) | batch field unchanged; track figure is new |
| Baseline: all smokes: smoker undetected, % of the smoke's whole life | 47.6 (44.2 to 51.1) | track 83.4 (81.0 to 85.0) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| Italian cruisers minus cruisers with ordinary smoke: undetected % | -8.4 (-13.5 to -3.8), clear (batch field) | track, whole life -5.7 (-10.9 to -0.7), clear; track, inside -5.5 (-11.1 to -0.2), clear | track detected flag |
| Italian cruisers minus all other smokes: undetected % | -6.4 (-11.4 to -2.2), clear (batch field) | track, whole life -4.9 (-9.7 to -0.4), clear; track, inside -4.3 (-9.4 to +0.3) | track detected flag |
| Battleships minus cruisers with ordinary smoke: undetected % | -18.4 (-32.9 to -9.3), clear (batch field) | track, whole life -13.7 (-25.4 to -4.0), clear; track, inside -13.2 (-25.9 to -3.7), clear | track detected flag |
| Battleships minus all other smokes: undetected % | -16.4 (-30.2 to -7.2), clear (batch field) | track, whole life -12.9 (-23.0 to -4.6), clear; track, inside -11.9 (-23.3 to -3.1), clear | track detected flag |
| Battleships minus Italian cruisers: undetected % | -10.0 (-22.6 to -0.9), clear (batch field) | track, whole life -8.0 (-18.4 to +1.0); track, inside -7.6 (-19.7 to +1.8) | track detected flag |
| Italian cruisers, Top 6 minus Rest, smoker lost per 100 | 33.3 vs 14.4; +19.0 (+1.6 to +52.5), clear | caught 33.3 vs 14.4; +19.0 (+1.4 to +53.2), clear; died 33.3 vs 17.0; +16.3 (-2.5 to +49.6) | new death metric |
| Battleships, Top 6 minus Rest, ships lost per 100 | 10.0 vs 8.3, no clear gap | caught 10.0 vs 8.3; +1.7 (-16.0 to +10.0); died 10.0 vs 20.8; -10.8 (-31.6 to +2.0) | new death metric |
| Who died in Italian cruiser smokes | 27 of 30 the smoker | caught 27 of 30; died 31 of 34 | new death metric |

---

**6. B3. Long smokes (Somers, Gearing, Harugumo, Delny): death rates and the Top 6 vs Rest gap, both metrics** (`x2-ships-maps/FINDINGS-X2.md`)

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Somers: ships lost per 100 smokes | 10.4 (7.4 to 13.4) | caught 10.4 (7.0 to 13.4); died 18.8 (12.3 to 25.0) | caught unchanged; died is the new death metric |
| Gearing: ships lost per 100 smokes | 17.8 (11.2 to 26.9) | caught 17.8 (11.8 to 26.8); died 25.4 (17.7 to 35.2) | caught unchanged; died is the new death metric |
| Harugumo: ships lost per 100 smokes | 21.0 (13.0 to 36.5) | caught 21.0 (12.9 to 34.4); died 22.0 (15.3 to 37.7) | caught unchanged; died is the new death metric |
| Delny: ships lost per 100 smokes | 0.0 | caught 0.0; died 4.5 | caught unchanged; died is the new death metric |
| All four: ships lost per 100 smokes | 14.2 (11.0 to 18.6) | caught 14.2 (10.8 to 18.6); died 20.9 (16.4 to 26.7) | caught unchanged; died is the new death metric |
| For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze): ships lost per 100 smokes | 7.4 (5.2 to 10.4) | caught 7.4 (5.0 to 10.6); died 14.1 (10.1 to 20.0) | caught unchanged; died is the new death metric |
| For comparison: all destroyer smokes: ships lost per 100 smokes | 11.5 (9.3 to 14.8) | caught 11.5 (9.2 to 14.6); died 18.2 (14.8 to 22.6) | caught unchanged; died is the new death metric |
| Long-smoke ships minus cap sitters, ships lost per 100 | +6.9 (+3.1 to +11.3), clear | caught +6.9 (+3.1 to +11.1), clear; died +6.8 (+1.0 to +12.4), clear | new death metric |
| Somers: Top 6 vs Rest, ships lost per 100 | 7.8 vs 11.8; -4.0 (-10.9 to +2.3) | caught 7.8 vs 11.8; -4.0 (-11.4 to +2.1); died 17.8 vs 19.4; -1.6 (-17.9 to +12.5) | new death metric |
| Gearing: Top 6 vs Rest, ships lost per 100 | 9.5 vs 23.6; -14.1 (-27.7 to -5.3) | caught 9.5 vs 23.6; -14.1 (-26.0 to -4.6), clear; died 16.2 vs 32.3; -16.1 (-29.5 to -3.4), clear | new death metric |
| Harugumo: Top 6 vs Rest, ships lost per 100 | 9.1 vs 35.6; -26.5 (-42.4 to -12.3) | caught 9.1 vs 35.6; -26.5 (-43.3 to -13.6), clear; died 12.7 vs 33.3; -20.6 (-45.6 to -5.6), clear | new death metric |
| Delny: Top 6 vs Rest, ships lost per 100 | 0.0 vs too few | caught 0.0 vs too few; died 5.6 vs too few | new death metric |
| All four: Top 6 vs Rest, ships lost per 100 | 8.0 vs 18.8; -10.8 (-17.0 to -5.8) | caught 8.0 vs 18.8; -10.8 (-17.8 to -6.0), clear; died 15.2 vs 25.2; -10.0 (-19.1 to -1.6), clear | new death metric |
| For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze): Top 6 vs Rest, ships lost per 100 | 5.9 vs 8.0; -2.0 (-7.5 to +2.2) | caught 5.9 vs 8.0; -2.0 (-7.7 to +2.2); died 9.6 vs 15.9; -6.3 (-14.5 to +1.0) | new death metric |
| For comparison: all destroyer smokes: Top 6 vs Rest, ships lost per 100 | 7.5 vs 13.8; -6.3 (-11.1 to -2.2) | caught 7.5 vs 13.8; -6.3 (-11.0 to -2.4), clear; died 13.4 vs 20.9; -7.4 (-14.7 to -1.2), clear | new death metric |
| Top 6 vs Rest gap once games won and lost are separated (four ships) | round 5 text: "round 3 showed this gap goes away" (no number) | games won: died 10.7 vs 12.3; -1.6 (-10.0 to +7.1); caught 6.8 vs 8.3; -1.5 (-7.1 to +4.3). Games lost: died 28.3 vs 34.0; -5.7 (-25.4 to +6.5); caught 11.7 vs 26.0; -14.4 (-27.7 to -5.0), clear | new: both metrics split by result |
| Smoker and sheltering-cruiser splits for the long ships | not given in round 5 | four ships: smoker died 12.4 (8.7 to 17.3), caught 6.2 (3.8 to 10.2); cruisers died 8.7 (6.3 to 11.7), caught 8.0 (5.8 to 10.9) per 100 sheltering cruisers | new |

---

**7a. High-paying cells (C4: Sleeping Giant G1, Hotspot G10+H10, Sea of Fortune F9+G9; C5: Loop F8 and F10)** (`x2-ships-maps/FINDINGS-X2.md`)

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Sleeping Giant G1: n and concealed damage per smoke | 21; 24,101 | 21; 24,101 | unchanged |
| Sleeping Giant G1: we took the cap (cap not already ours) | 19% of 21 | nearest cap 6 of 21 (29%); contested cap 6 of 21 (29%) | cap timeline |
| Sleeping Giant G1: enemy took the cap | not given | nearest cap 7 of 13 (54%, small n); contested cap 7 of 13 (54%, small n) | cap timeline (new) |
| Sleeping Giant G1: ships lost per 100 smokes | 14.3 | caught 14.3 (0.0 to 30.4); died 19.0 (0.0 to 42.1) | caught unchanged; died is the new death metric |
| Hotspot G10+H10: n and concealed damage per smoke | 40; 16,970 | 40; 16,970 | unchanged |
| Hotspot G10+H10: we took the cap (cap not already ours) | 34% of 35 | nearest cap 14 of 35 (40%); contested cap 14 of 35 (40%) | cap timeline |
| Hotspot G10+H10: enemy took the cap | not given | nearest cap 9 of 26 (35%); contested cap 9 of 26 (35%) | cap timeline (new) |
| Hotspot G10+H10: ships lost per 100 smokes | 10.0 | caught 10.0 (2.7 to 17.8); died 20.0 (4.9 to 41.2) | caught unchanged; died is the new death metric |
| Sea of Fortune F9+G9: n and concealed damage per smoke | 10; 24,597 | 10; 24,597 | unchanged |
| Sea of Fortune F9+G9: we took the cap (cap not already ours) | 25% of 8 | nearest cap 2 of 8 (25%, small n); contested cap 2 of 8 (25%, small n) | cap timeline |
| Sea of Fortune F9+G9: enemy took the cap | not given | nearest cap 2 of 9 (22%, small n); contested cap 2 of 9 (22%, small n) | cap timeline (new) |
| Sea of Fortune F9+G9: ships lost per 100 smokes | 0.0 | caught 0.0 (0.0 to 0.0); died 0.0 (0.0 to 0.0) | caught unchanged; died is the new death metric |
| Loop F8: n and concealed damage per smoke | 15; 18,318 | 15; 18,318 | unchanged |
| Loop F8: we took the cap (cap not already ours) | no cap result quoted | nearest cap 5 of 9 (56%, small n); contested cap 5 of 9 (56%, small n) | cap timeline |
| Loop F8: enemy took the cap | not given | nearest cap 4 of 10 (40%, small n); contested cap 4 of 10 (40%, small n) | cap timeline (new) |
| Loop F8: ships lost per 100 smokes | 13.3 | caught 13.3 (0.0 to 40.0); died 26.7 (7.1 to 54.5) | caught unchanged; died is the new death metric |
| Loop F10: n and concealed damage per smoke | 9; 20,728 | 9; 20,728 | unchanged |
| Loop F10: we took the cap (cap not already ours) | no cap result quoted | nearest cap 3 of 5 (too few); contested cap 3 of 5 (too few) | cap timeline |
| Loop F10: enemy took the cap | not given | nearest cap 1 of 5 (too few); contested cap 1 of 5 (too few) | cap timeline (new) |
| Loop F10: ships lost per 100 smokes | 33.3 | caught 33.3 (8.3 to 66.7); died 33.3 (9.1 to 71.4) | caught unchanged; died is the new death metric |

**7b. Sleeping Giant cap B (C5-SG-3): is the smoke there to stop the enemy taking B** (`x2-ships-maps/FINDINGS-X2.md`)

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Cap A: ours / neutral / theirs at activation | 28 / 12 / 6 | 28 / 12 / 6 | unchanged (timeline agrees with the snapshot) |
| Cap A: enemy took it | 3 of 40 (8%) | 7 of 40 (18%) | cap timeline |
| Cap A: we took it | 7 of 18 (39%) | 10 of 18 (56%) | cap timeline |
| Cap A: ships lost per 100 smokes | 6.5 | caught 6.5 (0.0 to 14.6); died 13.0 (6.1 to 22.6) | caught unchanged; died is the new death metric |
| Cap B: ours / neutral / theirs at activation | 16 / 12 / 6 | 16 / 12 / 6 | unchanged (timeline agrees with the snapshot) |
| Cap B: enemy took it | 1 of 28 (4%) | 1 of 28 (4%) | cap timeline (same result) |
| Cap B: we took it | 5 of 18 (28%) | 7 of 18 (39%) | cap timeline |
| Cap B: ships lost per 100 smokes | 11.8 | caught 11.8 (2.9 to 25.0); died 14.7 (5.4 to 26.5) | caught unchanged; died is the new death metric |
| Cap C: ours / neutral / theirs at activation | 8 / 2 / 7 | 8 / 2 / 7 | unchanged (timeline agrees with the snapshot) |
| Cap C: enemy took it | 2 of 10 (20%, small n) | 2 of 10 (20%, small n) | cap timeline (same result) |
| Cap C: we took it | 4 of 9 (small n) | 4 of 9 (44%, small n) | cap timeline (same result) |
| Cap C: ships lost per 100 smokes | 29.4 | caught 29.4 (10.0 to 56.2); died 29.4 (11.1 to 57.1) | caught unchanged; died is the new death metric |
| Cap D: ours / neutral / theirs at activation | 18 / 0 / 4 | 18 / 0 / 4 | unchanged (timeline agrees with the snapshot) |
| Cap D: enemy took it | 0 of 18 (0%) | 0 of 18 (0%) | cap timeline (same result) |
| Cap D: we took it | 0 of 4 (too few) | 0 of 4 (too few) | cap timeline (same result) |
| Cap D: ships lost per 100 smokes | 13.6 | caught 13.6 (0.0 to 24.1); died 13.6 (0.0 to 24.0) | caught unchanged; died is the new death metric |
| Enemy took B vs the other caps | 1 of 28 (4%) vs 5 of 68 (7%); -4 pts (-13 to +9) | 1 of 28 (4%) vs 9 of 68 (13%); -9.7 (-21.8 to +4.0) | cap timeline |
| B ours at activation, B vs other caps | 47% (27 to 72) vs 64% (52 to 75) | 47.1% vs 63.5% | unchanged values, timeline owner |
| Sign of a real attack on B (of the 16 laid when B was ours) | enemy already contesting at the start 2; batch "cap defended" 2 | enemy was taking B while the smoke stood 3 of 16 | cap timeline (capturing side) replaces the snapshot flags |

**7c. Mountain Range, radar from smoke at B (C5-MR-2): did the enemy take B during those smokes** (`x2-ships-maps/FINDINGS-X2.md`)

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Radar smokes, nearest cap B: ours / neutral / theirs | 8 / 5 / 2 | 9 / 5 / 1 | cap timeline |
| Radar smokes, nearest cap B: enemy took | 5 of 13 (38%, small n) | 6 of 14 (43%, small n) | cap timeline |
| Radar smokes, nearest cap B: enemy took when ours | 4 of 8 (50%, small n) | 5 of 9 (56%, small n) | cap timeline |
| Radar smokes, nearest cap B: we took | 3 of 7 (too few) | 4 of 6 (too few) | cap timeline |
| Other smokes, nearest cap B: ours / neutral / theirs | 15 / 17 / 21 | 15 / 17 / 21 | unchanged |
| Other smokes, nearest cap B: enemy took | 11 of 32 (34%) | 12 of 32 (38%) | cap timeline |
| Other smokes, nearest cap B: enemy took when ours | 5 of 15 (33%) | 5 of 15 (33%) | cap timeline (same result) |
| Other smokes, nearest cap B: we took | 17 of 38 (45%) | 17 of 38 (45%) | cap timeline (same result) |
| Radar smokes within 2 km of B: ours / neutral / theirs | 4 / 2 / 1 | 4 / 2 / 1 | unchanged |
| Radar smokes within 2 km of B: enemy took | 2 of 6 (too few) | 2 of 6 (too few) | cap timeline (same result) |
| Radar smokes within 2 km of B: enemy took when ours | 1 of 4 (too few) | 1 of 4 (too few) | cap timeline (same result) |
| Radar smokes within 2 km of B: we took | 1 of 3 (too few) | 1 of 3 (too few) | cap timeline (same result) |
| Other smokes within 2 km of B: ours / neutral / theirs | 7 / 8 / 9 | 7 / 8 / 9 | unchanged |
| Other smokes within 2 km of B: enemy took | 4 of 15 (27%) | 5 of 15 (33%) | cap timeline |
| Other smokes within 2 km of B: enemy took when ours | 2 of 7 (too few) | 2 of 7 (too few) | cap timeline (same result) |
| Other smokes within 2 km of B: we took | 11 of 17 (65%) | 11 of 17 (65%) | cap timeline (same result) |
| Radar smokes, other maps (nearest cap): ours / neutral / theirs | 52 / 35 / 25 | 52 / 35 / 25 | unchanged |
| Radar smokes, other maps (nearest cap): enemy took | 16 of 87 (18%) | 20 of 87 (23%) | cap timeline |
| Radar smokes, other maps (nearest cap): enemy took when ours | 7 of 52 (13%) | 10 of 52 (19%) | cap timeline |
| Radar smokes, other maps (nearest cap): we took | 23 of 60 (38%) | 28 of 60 (47%) | cap timeline |
| Whole map, enemy took the nearest cap | A 6 of 41 (15%), B 16 of 45 (36%), C 10 of 56 (18%) | A 10 of 41 (24%), B 18 of 46 (39%), C 12 of 56 (21%) | cap timeline |
| Radar smokes at B: ships lost | 1 death | caught 6.7 per 100; died 6.7 per 100 | unchanged (one ship on both metrics) |
| Radar definition | tags: 15 smokes | tags 15, radar log 15, same smokes 15 | radar log added; same set |

**7d. Loop, cap sitters at B (C5-LP-6 and spot `c5-lp-sitters-b`)** (`x2-ships-maps/FINDINGS-X2.md`)

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Members of the spot | 28 (15 Top 6, 13 Rest) | 28 (15 Top 6, 13 Rest) | unchanged |
| We took B during or just after, Top 6 | 5 of 10 | 7 of 9 (78%, small n) on B; 8 of 10 (80%, small n) on the nearest cap | cap timeline |
| We took B during or just after, Rest | 1 of 8 (small n) | 4 of 8 (50%, small n) on B; 4 of 8 (50%, small n) on the nearest cap | cap timeline |
| Enemy took B | not given | 2 of 15 (13%); when ours 1 of 11 (9%, small n) | cap timeline (new) |
| Concealed damage per smoke in the spot | 3,668 (Top 6 5.8k, Rest 1.2k) | 3,668 (Top 6 5,834, Rest 1,169) | unchanged |
| Ships lost per 100 smokes | 3.6 | caught 3.6 (0.0 to 11.1); died 7.1 (0.0 to 16.7) | caught unchanged; died is the new death metric |

---

**D1. Score every clan on the six dimensions ("what it buys" redone)** (`x3-clans/FINDINGS-X3.md`)

Scores replaced (old score -> new score, why):

| Round 5b score | Round 5c score | Why |
|---|---|---|
| Deaths per 100 smokes (`deaths_per100`) | Caught per 100 smokes (same numbers) plus Died per 100 smokes; smoker-only versions of both | new death metric |
| Deaths in or behind smoke per game (`deaths_pg`) | Ships caught per game (same numbers) plus Ships died per game | new death metric |
| Nearest cap taken % (`took_pct`, snapshots) | Nearest cap taken % and Contested cap taken % (timeline) | cap timeline |
| Nearest cap not lost % (`held_pct`, snapshots) | Nearest cap not lost % and Contested cap not lost % (timeline) | cap timeline |
| Caps taken next to a smoke per game (`caps_taken_pg`, snapshots) | Nearest caps taken with a smoke per game (same key) and Contested caps taken per game (timeline) | cap timeline |
| `cap_won_pg`, `cap_def_pg` (batch flags) | dropped | not to be used |
| First smoke of the game, Smokes after 12:00, Smokes before 5:00 (HUD clock) | same scores on the replay clock | clock (`e0` instead of `el`) |

Check: "caught per 100" equals round 5b's deaths per 100 for all 30 clans, and its Top 6 minus Rest interval is the same (-9.5 to -2.9 * then, -9.5 to -2.9 * now).

Top 6 clans and PN, every per-clan score that was replaced or moved: round 5b value and percentile -> round 5c value and percentile.

| Score (round 5b -> round 5c) | *H-SR | *RESIN | *BONKZ | *HTDOG | *KITE | *VRTUS | PN | Why |
|---|---|---|---|---|---|---|---|---|
| Deaths per 100 smokes -> Died per 100 smokes | 4.0 p0 -> 6.0 p0 | 7.8 p22 -> 17.5 p57 | 11.8 p57 -> 17.6 p61 | 6.6 p9 -> 10.4 p17 | 8.9 p30 -> 11.1 p26 | 8.5 p26 -> 9.8 p11 | 28.6 p96 -> 50.0 p100 | new death metric |
| Deaths per 100 smokes -> Caught per 100 smokes | 4.0 p0 -> 4.0 p0 (same) | 7.8 p22 -> 7.8 p22 (same) | 11.8 p57 -> 11.8 p57 (same) | 6.6 p9 -> 6.6 p9 (same) | 8.9 p30 -> 8.9 p30 (same) | 8.5 p26 -> 8.5 p26 (same) | 28.6 p96 -> 28.6 p96 (same) | unchanged |
| Smoker died per 100 smokes | new: 4.0 p4 | new: 9.7 p39 | new: 12.7 p57 | new: 8.5 p30 | new: 6.7 p17 | new: 6.1 p9 | new: 28.6 p83 | new death metric (no round 5b score) |
| Smoker caught per 100 smokes | new: 2.0 p9 | new: 1.9 p4 | new: 6.9 p52 | new: 5.7 p30 | new: 4.4 p17 | new: 4.9 p22 | new: 7.1 p61 | new split (no round 5b score) |
| Nearest cap taken (% of smokes where it was not ours) (snapshots -> timeline) | 38.0 p96 -> 56.0 p100 | 17.5 p35 -> 32.1 p57 | 42.2 p100 -> 53.3 p96 | 24.5 p52 -> 30.2 p48 | 31.8 p78 -> 45.5 p91 | 21.6 p43 -> 23.5 p28 | 12.5 p17 -> 12.5 p9 | cap timeline |
| Contested cap taken (% of smokes where it was not ours) | new: 41.5 p96 | new: 27.1 p57 | new: 44.3 p100 | new: 26.7 p52 | new: 38.5 p91 | new: 18.3 p26 | new: 8.3 p4 | cap timeline (no round 5b score) |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (snapshots -> timeline) | 89.2 p55 -> 86.5 p50 | 87.5 p30 -> 75.0 p10 | 93.0 p70 -> 88.4 p65 | 97.0 p95 -> 84.8 p40 | 93.8 p75 -> 87.5 p58 | 92.9 p65 -> 92.9 p85 | too few -> too few (same) | cap timeline |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 86.4 p70 | new: 73.7 p20 | new: 83.3 p55 | new: 87.8 p80 | new: 87.5 p75 | new: 84.6 p65 | new: too few | cap timeline (no round 5b score) |
| Nearest caps taken with a smoke per game | 0.77 p87 -> 1.14 p96 | 0.33 p26 -> 0.67 p52 | 0.81 p91 -> 1.00 p87 | 0.67 p70 -> 0.72 p65 | 0.50 p43 -> 0.64 p43 | 0.73 p83 -> 0.82 p72 | 0.14 p2 -> 0.14 p0 | cap timeline |
| Contested caps taken with a smoke per game | new: 1.09 p91 | new: 0.71 p52 | new: 1.14 p98 | new: 0.72 p70 | new: 0.64 p43 | new: 0.73 p74 | new: 0.14 p2 | cap timeline (no round 5b score) |
| Deaths in or behind smoke per game -> Ships died per game | 0.18 p0 -> 0.27 p0 | 0.33 p22 -> 0.75 p48 | 0.57 p52 -> 0.86 p61 | 0.39 p35 -> 0.61 p26 | 0.29 p11 -> 0.36 p13 | 0.64 p72 -> 0.73 p43 | 0.57 p52 -> 1.00 p72 | new death metric |
| Deaths in or behind smoke per game -> Ships caught per game | 0.18 p0 -> 0.18 p0 (same) | 0.33 p22 -> 0.33 p22 (same) | 0.57 p52 -> 0.57 p52 (same) | 0.39 p35 -> 0.39 p35 (same) | 0.29 p11 -> 0.29 p11 (same) | 0.64 p72 -> 0.64 p72 (same) | 0.57 p52 -> 0.57 p52 (same) | unchanged |
| First smoke of the game (median, s) | 120.5 s p0 -> 120.1 s p0 | 174.0 s p35 -> 173.4 s p35 | 198.0 s p65 -> 197.4 s p65 | 233.0 s p91 -> 232.4 s p91 | 150.0 s p22 -> 149.2 s p22 | 224.0 s p87 -> 222.8 s p87 | 221.5 s p78 -> 221.0 s p78 | clock |
| Smokes after 12:00 (%) | 8.0 p30 -> 7.0 p26 | 19.4 p91 -> 19.4 p91 (same) | 13.7 p65 -> 13.7 p65 (same) | 17.9 p83 -> 16.0 p78 | 8.9 p48 -> 8.9 p48 (same) | 14.6 p70 -> 14.6 p70 (same) | 7.1 p26 -> 7.1 p30 | clock |
| Smokes before 5:00 (%) | 31.0 p83 -> 32.0 p83 | 28.2 p65 -> 28.2 p65 (same) | 22.5 p26 -> 22.5 p22 | 23.6 p30 -> 23.6 p26 | 24.4 p39 -> 24.4 p39 (same) | 18.3 p0 -> 18.3 p0 (same) | 50.0 p100 -> 50.0 p100 (same) | clock |

Top 6 clans and PN, 95% intervals of the same scores (round 5b -> round 5c).

| Score | *H-SR | *RESIN | *BONKZ | *HTDOG | *KITE | *VRTUS | PN |
|---|---|---|---|---|---|---|---|
| Died per 100 smokes | 0.0 to 8.9 -> 1.2 to 11.2 | 2.9 to 13.3 -> 9.9 to 25.6 | 5.9 to 17.8 -> 10.3 to 25.8 | 2.1 to 12.2 -> 4.1 to 17.4 | 2.4 to 15.9 -> 2.6 to 21.2 | 1.1 to 16.9 -> 3.4 to 16.7 | 7.1 to 50.0 -> 20.0 to 75.0 |
| Caught per 100 smokes | 0.0 to 8.9 -> 0.0 to 8.9 | 2.9 to 13.3 -> 2.9 to 13.3 | 5.9 to 17.8 -> 5.9 to 17.8 | 2.1 to 12.2 -> 2.1 to 12.2 | 2.4 to 15.9 -> 2.4 to 15.9 | 1.1 to 16.9 -> 1.1 to 16.9 | 7.1 to 50.0 -> 7.1 to 50.0 |
| Smoker died per 100 smokes | new: 0.9 to 7.5 | new: 5.3 to 14.5 | new: 6.9 to 20.0 | new: 3.4 to 15.0 | new: 0.0 to 16.7 | new: 1.9 to 10.1 | new: 11.1 to 50.0 |
| Smoker caught per 100 smokes | new: 0.0 to 4.9 | new: 0.0 to 4.9 | new: 2.4 to 12.7 | new: 1.9 to 10.4 | new: 0.0 to 10.8 | new: 0.0 to 10.8 | new: 0.0 to 22.2 |
| Nearest cap taken (% of smokes where it was not ours) | 23.1 to 55.3 -> 46.0 to 69.2 | 8.3 to 26.5 -> 22.0 to 45.5 | 26.2 to 58.3 -> 35.5 to 72.4 | 12.8 to 39.4 -> 16.9 to 47.5 | 12.5 to 50.0 -> 25.0 to 65.2 | 12.2 to 37.5 -> 13.8 to 40.0 | 0.0 to 66.7 -> 0.0 to 66.7 |
| Contested cap taken (% of smokes where it was not ours) | new: 33.3 to 51.7 | new: 18.8 to 37.3 | new: 29.9 to 62.1 | new: 15.1 to 40.0 | new: 19.0 to 60.0 | new: 11.1 to 31.0 | new: 0.0 to 33.3 |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 77.8 to 97.6 -> 74.2 to 96.2 | 76.5 to 96.9 -> 60.0 to 91.7 | 86.8 to 100.0 -> 80.0 to 96.8 | 89.3 to 100.0 -> 65.5 to 100.0 | 72.7 to 100.0 -> 58.3 to 100.0 | 84.9 to 100.0 -> 84.9 to 100.0 | too few -> too few |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 73.3 to 95.7 | new: 62.2 to 86.7 | new: 73.5 to 92.7 | new: 71.8 to 100.0 | new: 57.1 to 100.0 | new: 75.0 to 100.0 | new: too few |
| Nearest caps taken with a smoke per game | 0.50 to 1.05 -> 0.86 to 1.45 | 0.17 to 0.54 -> 0.46 to 0.88 | 0.52 to 1.10 -> 0.67 to 1.33 | 0.33 to 1.00 -> 0.39 to 1.06 | 0.14 to 0.93 -> 0.29 to 1.07 | 0.36 to 1.09 -> 0.45 to 1.09 | 0.00 to 0.43 -> 0.00 to 0.43 |
| Contested caps taken with a smoke per game | new: 0.77 to 1.41 | new: 0.50 to 0.92 | new: 0.81 to 1.43 | new: 0.39 to 1.06 | new: 0.29 to 1.07 | new: 0.45 to 1.00 | new: 0.00 to 0.43 |
| Ships died per game | 0.00 to 0.41 -> 0.05 to 0.50 | 0.12 to 0.54 -> 0.42 to 1.08 | 0.29 to 0.90 -> 0.48 to 1.29 | 0.11 to 0.72 -> 0.22 to 1.00 | 0.07 to 0.50 -> 0.07 to 0.71 | 0.09 to 1.36 -> 0.27 to 1.27 | 0.14 to 1.14 -> 0.29 to 1.71 |
| Ships caught per game | 0.00 to 0.41 -> 0.00 to 0.41 | 0.12 to 0.54 -> 0.12 to 0.54 | 0.29 to 0.90 -> 0.29 to 0.90 | 0.11 to 0.72 -> 0.11 to 0.72 | 0.07 to 0.50 -> 0.07 to 0.50 | 0.09 to 1.36 -> 0.09 to 1.36 | 0.14 to 1.14 -> 0.14 to 1.14 |
| First smoke of the game (median, s) | 104.0 s to 163.0 s -> 102.7 s to 162.3 s | 122.0 s to 229.0 s -> 121.9 s to 229.0 s | 163.0 s to 280.0 s -> 162.4 s to 279.4 s | 170.0 s to 265.0 s -> 169.4 s to 264.4 s | 98.0 s to 296.0 s -> 97.7 s to 295.3 s | 160.0 s to 283.0 s -> 158.9 s to 282.7 s | 145.0 s to 520.0 s -> 143.9 s to 519.7 s |
| Smokes after 12:00 (%) | 2.7 to 14.3 -> 2.2 to 13.3 | 10.4 to 30.1 -> 10.4 to 30.1 | 6.5 to 21.7 -> 6.5 to 21.7 | 8.0 to 29.6 -> 6.6 to 27.0 | 2.4 to 17.6 -> 2.4 to 17.6 | 3.6 to 23.1 -> 3.6 to 23.1 | 0.0 to 27.3 -> 0.0 to 27.3 |
| Smokes before 5:00 (%) | 25.3 to 36.8 -> 26.5 to 37.7 | 22.7 to 34.6 -> 22.7 to 34.6 | 17.7 to 26.8 -> 17.7 to 26.8 | 17.6 to 30.5 -> 17.6 to 30.5 | 18.9 to 29.8 -> 18.9 to 29.8 | 10.5 to 28.3 -> 10.5 to 28.3 | 25.0 to 78.6 -> 25.0 to 78.6 |

The other 23 clans. Replaced scores (round 5b -> round 5c); "died" is new, "caught" is the old deaths number.

| Clan | Deaths per 100 -> Died per 100 | Caught per 100 (was Deaths per 100) | Nearest cap taken % (snapshots -> timeline) | Nearest cap not lost % (snapshots -> timeline) | Caps taken per game (snapshots -> timeline) |
|---|---|---|---|---|---|
| MZY | 14.0 -> 22.0 | 14.0 (same) | 29.0 -> 38.7 | 78.6 -> 78.6 | 0.37 -> 0.53 |
| EPOXY | 12.2 -> 15.9 | 12.2 (same) | 30.6 -> 36.1 | 82.8 -> 75.9 | 0.59 -> 0.65 |
| HFANS | 10.0 -> 13.6 | 10.0 (same) | 26.2 -> 27.9 | 85.0 -> 82.5 | 0.82 -> 0.88 |
| -BN- | 9.9 -> 11.6 | 9.9 (same) | 22.2 -> 31.5 | 96.2 -> 96.2 | 0.71 -> 1.07 |
| KITED | 12.7 -> 15.9 | 12.7 (same) | 25.0 -> 25.0 | 95.7 -> 95.7 | 0.57 -> 0.57 |
| MACHX | 6.1 -> 9.8 | 6.1 (same) | 32.1 -> 35.8 | 88.9 -> 81.5 | 1.07 -> 1.14 |
| REEEE | 7.7 -> 7.7 | 7.7 (same) | 13.3 -> 23.3 | 70.6 -> 70.6 | 0.23 -> 0.38 |
| PFANS | 12.5 -> 16.7 | 12.5 (same) | 11.8 -> 23.5 | 87.5 -> 62.5 | 0.17 -> 0.33 |
| KSC | 11.1 -> 15.3 | 11.1 (same) | 20.6 -> 29.4 | 88.9 -> 88.9 | 0.55 -> 0.82 |
| 5D | 32.4 -> 37.8 | 32.4 (same) | 34.8 -> 34.8 | 88.2 -> 82.4 | 0.60 -> 0.60 |
| BONKY | 11.1 -> 22.2 | 11.1 (same) | 4.3 -> 8.7 | 87.5 -> 87.5 | 0.14 -> 0.29 |
| KSE | 15.0 -> 45.0 | 15.0 (same) | 13.3 -> 33.3 | too few -> too few | 0.29 -> 0.71 |
| MACH | 6.9 -> 27.6 | 6.9 (same) | 15.8 -> 15.8 | 100.0 -> 100.0 | 0.43 -> 0.43 |
| NGA | 14.3 -> 25.0 | 14.3 (same) | 10.0 -> 10.0 | too few -> too few | 0.29 -> 0.29 |
| RSR | 19.2 -> 38.5 | 19.2 (same) | 35.7 -> 35.7 | 90.9 -> 90.9 | 0.71 -> 0.71 |
| SCCC2 | 10.4 -> 10.4 | 10.4 (same) | 12.0 -> 16.0 | 95.5 -> 90.9 | 0.43 -> 0.57 |
| UYSC | 27.8 -> 33.3 | 27.8 (same) | 26.1 -> 43.5 | 85.7 -> 85.7 | 0.57 -> 0.86 |
| BTLST (flag) | 23.5 -> 26.5 | 23.5 (same) | 33.3 -> 33.3 | 92.3 -> 69.2 | 0.83 -> 0.83 |
| INCA (flag) | 7.7 -> 12.8 | 7.7 (same) | 31.2 -> 41.2 | 82.4 -> 82.4 | 0.67 -> 1.00 |
| MANBA (flag) | 22.2 -> 22.2 | 22.2 (same) | too few -> too few | too few -> too few | 0.00 -> 0.17 |
| OGF (flag) | 33.3 -> 66.7 | 33.3 (same) | too few -> too few | too few -> too few | 0.00 -> 0.00 |
| RMN (flag) | 33.3 -> 33.3 | 33.3 (same) | too few -> too few | too few -> too few | 0.00 -> 0.17 |
| KM (flag) | 13.3 -> 20.0 | 13.3 (same) | too few -> too few | too few -> too few | 0.40 -> 0.40 |

Time scores, what the switch from the HUD clock to the replay clock moved: the first smoke of the game moves for all 30 clans, by 0.0 to 1.4 s (median 0.6 s; the replay clock is exact and the HUD clock is in whole seconds). Share after 12:00 moves for H-SR (8.0% -> 7.0%), HTDOG (17.9% -> 16.0%). Share before 5:00 moves for H-SR (31.0% -> 32.0%), KSC (22.2% -> 23.8%).
Other clans where a time score moved by more than a rounding step (1 s, or half a point): EPOXY First smoke of the game (median, s) 192.0 s -> 190.7 s; HFANS First smoke of the game (median, s) 143.0 s -> 142.0 s; MACHX First smoke of the game (median, s) 146.0 s -> 144.6 s; PFANS First smoke of the game (median, s) 185.5 s -> 184.4 s; KSE First smoke of the game (median, s) 251.0 s -> 250.0 s; MANBA First smoke of the game (median, s) 315.0 s -> 313.9 s; KSC Smokes before 5:00 (%) 22.2 -> 23.8.

All Top 6 minus Rest gaps, round 5b and round 5c (Top 6 / Rest / 95% interval).

| Score | Round 5b | Round 5c | Why |
|---|---|---|---|
| Long-smoke destroyers per game (`long_ships_pg`) | 0.89 / 0.66 / -0.14 to +0.52 | 0.89 / 0.66 / -0.14 to +0.52 | unchanged |
| Cap-sitter destroyers per game (`sitter_ships_pg`) | 0.70 / 0.70 / -0.26 to +0.29 | 0.70 / 0.70 / -0.26 to +0.29 | unchanged |
| Destroyers carrying smoke per game (`smoke_dd_pg`) | 1.63 / 1.45 / -0.08 to +0.44 | 1.63 / 1.45 / -0.08 to +0.44 | unchanged |
| Cruisers carrying smoke per game (`smoke_cruisers_pg`) | 0.52 / 0.72 / -0.54 to +0.22 | 0.52 / 0.72 / -0.54 to +0.22 | unchanged |
| Exhaust-smoke ships per game (`exhaust_ships_pg`) | 0.23 / 0.62 / -0.62 to -0.21 * | 0.23 / 0.62 / -0.62 to -0.21 * | unchanged |
| Smokes per game (`smokes_pg`) | 4.89 / 4.35 / -0.43 to +1.58 | 4.89 / 4.35 / -0.43 to +1.58 | unchanged |
| First smoke of the game (median, s) (`first_smoke_s`) | 175.0 s / 196.5 s / -54.0 to +29.5 | 173.9 s / 196.1 s / -53.9 to +29.1 | clock |
| Smokes after 12:00 (%) (`late_pct`) | 14.3 / 11.1 / -1.6 to +7.8 | 13.8 / 11.1 / -2.3 to +7.3 | clock |
| For a teammate (%) (`teammate_pct`) | 63.8 / 54.8 / -2.5 to +20.2 | 63.8 / 54.8 / -2.5 to +20.2 | unchanged |
| Stacked on a teammate (%) (`stacked_pct`) | 31.6 / 23.5 / -3.0 to +18.4 | 31.6 / 23.5 / -3.0 to +18.4 | unchanged |
| Radar cruiser inside (% of destroyer smokes) (`radar_ca_inside_pct`) | 47.3 / 29.0 / +7.8 to +27.0 * | 47.3 / 29.0 / +7.8 to +27.0 * | unchanged |
| Median distance to cap edge (m) (`edge_m`) | 2,060 / 2,089 / -502.0 to +499.7 | 2,060 / 2,089 / -502.0 to +499.7 | unchanged |
| Inside a cap (%) (`inside_cap_pct`) | 22.9 / 24.2 / -7.7 to +4.2 | 22.9 / 24.2 / -7.7 to +4.2 | unchanged |
| Centre lane (%) (`centre_pct`) | 24.3 / 21.0 / -4.9 to +11.9 | 24.3 / 21.0 / -4.9 to +11.9 | unchanged |
| Pushing (%) (`pushing_pct`) | 20.8 / 20.3 / -4.1 to +4.6 | 20.8 / 20.3 / -4.1 to +4.6 | unchanged |
| Kiting (%) (`kiting_pct`) | 17.7 / 20.3 / -7.7 to +2.0 | 17.7 / 20.3 / -7.7 to +2.0 | unchanged |
| Parked (%) (`parked_pct`) | 28.8 / 27.5 / -11.4 to +13.5 | 28.8 / 27.5 / -11.4 to +13.5 | unchanged |
| Concealed damage per smoke (`conc_per_smoke`) | 11,685 / 8,515 / +570.1 to +5,690.5 * | 11,685 / 8,515 / +570.1 to +5,690.5 * | unchanged |
| Concealed damage per game (`conc_pg`) | 57,152 / 37,034 / +5,334.5 to +33,896.9 * | 57,152 / 37,034 / +5,334.5 to +33,896.9 * | unchanged |
| Nearest cap taken (% of smokes where it was not ours) (`took_pct`) | 28.4 / 22.6 / -2.2 to +14.6 | not in this round | dropped |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`held_pct`) | 92.1 / 87.2 / +0.6 to +9.5 * | not in this round | dropped |
| Deaths per 100 smokes (`deaths_per100`) | 7.8 / 13.4 / -9.5 to -2.9 * | not in this round | dropped |
| Svea or Jinan per game (`parked_cruisers_pg`) | 0.35 / 0.19 / -0.11 to +0.57 | 0.35 / 0.19 / -0.11 to +0.57 | unchanged |
| Ships carrying smoke per game (`smoke_ships_pg`) | 2.27 / 2.31 / -0.39 to +0.36 | 2.27 / 2.31 / -0.39 to +0.36 | unchanged |
| Destroyers per game (`dd_pg`) | 3.25 / 3.00 / +0.05 to +0.46 * | 3.25 / 3.00 / +0.05 to +0.46 * | unchanged |
| Radar ships per game (`radar_ships_pg`) | 3.57 / 3.01 / +0.20 to +0.84 * | 3.57 / 3.01 / +0.20 to +0.84 * | unchanged |
| Smokes before 5:00 (%) (`early_pct`) | 24.9 / 27.7 / -7.3 to +1.3 | 25.1 / 27.8 / -7.4 to +1.6 | clock |
| Selfish (%) (`selfish_pct`) | 36.2 / 45.2 / -20.4 to +2.1 | 36.2 / 45.2 / -20.4 to +2.1 | unchanged |
| Any cruiser inside (% of destroyer smokes) (`cruiser_inside_pct`) | 52.7 / 34.9 / +5.0 to +27.9 * | 52.7 / 34.9 / +5.0 to +27.9 * | unchanged |
| Own side of the front line (%) (`own_half_pct`) | 83.8 / 78.3 / +1.4 to +9.8 * | 83.8 / 78.3 / +1.4 to +9.8 * | unchanged |
| Sideways (%) (`sideways_pct`) | 26.0 / 25.5 / -9.4 to +8.7 | 26.0 / 25.5 / -9.4 to +8.7 | unchanged |
| Nearest caps taken with a smoke per game (`caps_taken_pg`) | 0.63 / 0.49 / -0.06 to +0.32 | 0.85 / 0.61 / +0.04 to +0.44 * | cap timeline |
| Smokes with the batch cap-won flag per game (`cap_won_pg`) | 1.20 / 0.81 / +0.15 to +0.61 * | not in this round | dropped |
| Batch cap-defended flag per game (secondary: fires for any owned cap with an enemy inside) (`cap_def_pg`) | 1.48 / 1.39 / -0.32 to +0.48 | not in this round | dropped |
| Deaths in or behind smoke per game (`deaths_pg`) | 0.38 / 0.58 / -0.37 to -0.06 * | not in this round | dropped |
| Nearest cap taken (% of smokes where it was not ours) (`we_took_n_pct`) | not in this round | 39.0 / 28.5 / +0.5 to +21.5 * | new |
| Contested cap taken (% of smokes where it was not ours) (`we_took_c_pct`) | not in this round | 32.2 / 22.8 / +1.1 to +17.6 * | new |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`not_lost_n_pct`) | not in this round | 85.7 / 83.0 / -3.3 to +8.6 | new |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`not_lost_c_pct`) | not in this round | 83.6 / 75.8 / +1.9 to +15.3 * | new |
| Died per 100 smokes (`died_per100`) | not in this round | 12.3 / 19.3 / -13.3 to -2.6 * | new |
| Caught per 100 smokes (`caught_per100`) | not in this round | 7.8 / 13.4 / -9.5 to -2.9 * | new |
| Smoker died per 100 smokes (`died_smoker_per100`) | not in this round | 8.2 / 15.1 / -12.3 to -3.2 * | new |
| Smoker caught per 100 smokes (`caught_smoker_per100`) | not in this round | 4.3 / 9.2 / -8.6 to -2.5 * | new |
| Contested caps taken with a smoke per game (`caps_taken_c_pg`) | not in this round | 0.86 / 0.60 / +0.05 to +0.46 * | new |
| Ships died per game (`died_pg`) | not in this round | 0.60 / 0.83 / -0.49 to -0.03 * | new |
| Ships caught per game (`caught_pg`) | not in this round | 0.38 / 0.58 / -0.37 to -0.06 * | new |

**D2. Group the clans; one scale or several styles?** (`x3-clans/FINDINGS-X3.md`)

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| First scale share | 29.6% | 29.6% | clock |
| Second scale share | 17.8% | 17.8% | clock |
| Third scale share | 11.6% | 11.5% | clock |
| Largest change in a loading | - | 0.01 | clock |
| Largest shift of a clan, first scale | - | 0.02 (HTDOG) | clock |
| Largest shift of a clan, second scale | - | 0.09 (HTDOG) | clock |
| Clans that change style | - | none | unchanged |
| Borderline clans | HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | unchanged |
| Mean share of resamples in which a clan keeps its style | 86% | 86% | clock |
| Top 6 minus Rest, first scale | -1.59 (-3.58 to +0.46) | -1.59 (-3.58 to +0.47) | clock |
| Top 6 minus Rest, second scale | +1.18 (+0.19 to +2.23) | +1.16 (+0.16 to +2.21) | clock |

Style outcome rows, round 5b -> round 5c:

| Score | Team smoke, plenty | Own smoke, plenty | Team smoke, little | Own smoke, little | Why |
|---|---|---|---|---|---|
| Deaths per 100 smokes -> Died per 100 smokes | 9.6 -> 14.5 | 9.4 -> 13.6 | 15.5 -> 25.0 | 19.2 -> 27.5 | new death metric |
| Deaths per 100 smokes -> Caught per 100 smokes | 9.6 -> 9.6 | 9.4 -> 9.4 | 15.5 -> 15.5 | 19.2 -> 19.2 | unchanged |
| Smoker died per 100 smokes | new: 10.0 | new: 11.2 | new: 16.4 | new: 24.2 | new death metric |
| Smoker caught per 100 smokes | new: 5.1 | new: 7.8 | new: 8.6 | new: 15.8 | new split |
| Nearest cap taken (% of smokes where it was not ours) (snapshots -> timeline) | 26.1 -> 35.5 | 23.7 -> 28.6 | 18.4 -> 25.0 | 25.7 -> 30.0 | cap timeline |
| Contested cap taken (% of smokes where it was not ours) | new: 29.6 | new: 22.9 | new: 19.1 | new: 22.7 | cap timeline |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (snapshots -> timeline) | 88.1 -> 84.1 | 93.4 -> 88.2 | 85.3 -> 76.5 | 91.5 -> 89.4 | cap timeline |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 78.6 | new: 86.1 | new: 69.7 | new: 85.4 | cap timeline |
| Nearest caps taken with a smoke per game | 0.59 -> 0.80 | 0.70 -> 0.80 | 0.27 -> 0.38 | 0.52 -> 0.61 | cap timeline |
| First smoke of the game (median, s) | 163.0 s -> 162.2 s | 207.0 s -> 206.3 s | 185.5 s -> 184.4 s | 221.0 s -> 219.7 s | clock |
| Smokes after 12:00 (%) | 13.3 -> 13.2 | 13.8 -> 13.3 | 7.8 -> 7.8 | 5.8 -> 5.8 | clock |

The batch `cap_def` row of the round 5b style table is dropped. Style members, games, smokes and W-L are the same as round 5b.

**D3. Compact profile per clan for a gauge graphic** (`x3-clans/FINDINGS-X3.md`)

| Part of the file | Round 5b | Round 5c | Why |
|---|---|---|---|
| `gauge` (six headline numbers, percentiles, ranges) | 30 clans | identical for 30 of 30 clans | unchanged |
| `style`, `style_id` | 30 clans | identical for all 30 clans | unchanged |
| `axes` (positions and ranges, 2 decimals) | 30 clans | 24 clans differ in some rounded figure; largest position shift 0.09 | clock |
| `values` / `percentiles` / `intervals` | 35 scores | 40 scores: 11 added, 6 removed, `caps_taken_pg` recounted, three time scores on the replay clock | new death metric / cap timeline / clock |
| `style_note`, `style_kept_share` | borderline: HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | borderline: HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | unchanged |
| `top6_minus_rest` | 35 gaps | 40 gaps; see the full old and new list under D1 | new death metric / cap timeline / clock |
| `styles[].numbers` | took_pct, held_pct, deaths_per100, cap_def_pg | the ten "what it buys" scores and two caps-per-game counts | new death metric / cap timeline |

Per-clan numbers that moved are listed in full for the Top 6 and PN, and for the other clans, under D1 "Changed from round 5b". Positions on the two scales for all 30 clans, old and new, are in the D2 table.

Top 6 and PN, positions on the two scales as stored in `axes` (round 5b -> round 5c):

| Clan | First scale | Second scale | Style |
|---|---|---|---|
| *H-SR | -4.58 -> -4.57 | +0.32 -> +0.28 | Team smoke, plenty of it (same) |
| *RESIN | -2.38 -> -2.39 | +1.15 -> +1.15 | Team smoke, plenty of it (same) |
| *BONKZ | -2.22 -> -2.23 | +0.90 -> +0.91 | Team smoke, plenty of it (same) |
| *HTDOG | +2.49 -> +2.51 | +0.74 -> +0.65 | Own smoke, plenty of it (same) |
| *KITE | -1.16 -> -1.16 | +0.25 -> +0.26 | Team smoke, plenty of it (same) |
| *VRTUS | +0.68 -> +0.68 | +1.97 -> +1.97 | Own smoke, plenty of it (same) |
| PN | -2.89 -> -2.89 | -3.29 -> -3.29 | Team smoke, little of it (same) |

## 4. The items redone in Round 5c

---

## Items 1 to 4: topic cards (A1 to A4)

Source: `x1-topics/FINDINGS-X1.md`.


Batch `output/20261117-230933`. Written by `x1-topics/build.py` from `a1.py` to `a4.py`. Two death metrics side by side everywhere: "died" = a covered ship died between activation and exactly 20 s after the smoke dispersed (each ship counted once); "caught" = the batch list of smoke deaths (round 5's deaths). Cap results come from the cap timeline with 60 s after dispersal. Intervals are 95%, resampling whole clans; * = the interval excludes zero ("clear"). Under 8 = too few (no rate); 8 to 14 = small n. Everything is association, not cause.

### A1. Cap-contest smokes by cover, and radar pressed from the smoke

**Answer:** On the cap timeline, the Rest took the contested cap after 77% of their smokes with a radar cruiser inside against 19% with no cruiser (gap clear); the Top 6 took it after 60% against 70% (gap not clear). So round 5's "76% vs 13% for the Rest, no difference for the Top 6" holds on the timeline; on the nearest cap it is 81% vs 19% (Rest) and 60% vs 70% (Top 6). A radar cruiser inside went with more concealed damage (+13,368 (+8,699 to +17,029 *)) and no clear change in deaths (died -0.1 (-8.9 to +9.7), caught +3.2 (-4.3 to +10.6) per 100). Radar pressed from the smoke is rare here: 8 of 104 smokes, with no death on either metric, too few to split by group. On the wider reading (the cruiser inside pressed radar at some time while the smoke stood, 43 smokes) a press went with concealed damage +2,530 (-5,432 to +9,471), we took the contested cap +1.5 (-15.7 to +23.2), died +10.9 (-6.5 to +26.5) and caught +9.7 (-4.7 to +25.9) per 100.

**Numbers:** 391 destroyer smokes carry the `cap_contest` tag (130 Top 6, 261 Rest). The contested cap and the nearest cap are the same cap in 390 of them. Cap results: an owner change on that cap between activation and 60 s after the smoke dispersed; (n) = smokes where the result could happen (the cap was not already that side's). "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them. Here that removes 1 smoke(s) from the died rates. Under 8 = too few, no rate.

Table 1. By cover and group.
| cover | group | n | we took, contested cap % (n) | we took, nearest cap % (n) | enemy took, contested cap % (n) | enemy took, nearest cap % (n) | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| radar cruiser inside | All | 104 | 67.3 (52) | 68.6 (51) | 13.4 (82) | 13.2 (83) | 16,882 | 14.6 | 10.6 |  |
| radar cruiser inside | Top 6 | 55 | 60.0 (30) | 60.0 (30) | 11.4 (44) | 11.4 (44) | 19,099 | 12.7 | 10.9 |  |
| radar cruiser inside | Rest | 49 | 77.3 (22) | 81.0 (21) | 15.8 (38) | 15.4 (39) | 14,394 | 16.7 | 10.2 |  |
| non-radar cruiser inside | All | 17 | 50.0 (8) | 50.0 (8) | 30.8 (13) | 30.8 (13) | 15,049 | 17.6 | 23.5 |  |
| non-radar cruiser inside | Top 6 | 8 | too few (3) | too few (3) | too few (5) | too few (5) | 20,045 | 25.0 | 12.5 | small n |
| non-radar cruiser inside | Rest | 9 | too few (5) | too few (5) | 50.0 (8) | 50.0 (8) | 10,609 | 11.1 | 33.3 | small n |
| no cruiser | All | 191 | 29.6 (108) | 29.6 (108) | 21.2 (132) | 21.2 (132) | 3,515 | 14.7 | 7.3 |  |
| no cruiser | Top 6 | 46 | 69.6 (23) | 69.6 (23) | 16.2 (37) | 16.2 (37) | 4,121 | 13.0 | 4.3 |  |
| no cruiser | Rest | 145 | 18.8 (85) | 18.8 (85) | 23.2 (95) | 23.2 (95) | 3,322 | 15.2 | 8.3 |  |
| other | All | 79 | 54.5 (44) | 54.5 (44) | 25.0 (64) | 25.0 (64) | 7,768 | 20.2 | 13.9 |  |
| other | Top 6 | 21 | 33.3 (9) | 33.3 (9) | 18.8 (16) | 18.8 (16) | 7,222 | 19.1 | 14.3 |  |
| other | Rest | 58 | 60.0 (35) | 60.0 (35) | 27.1 (48) | 27.1 (48) | 7,966 | 20.7 | 13.8 |  |
| all cap-contest smokes | All | 391 | 44.8 (212) | 45.0 (211) | 20.3 (291) | 20.2 (292) | 8,431 | 15.9 | 10.2 |  |
| all cap-contest smokes | Top 6 | 130 | 61.5 (65) | 61.5 (65) | 13.7 (102) | 13.7 (102) | 11,939 | 14.6 | 9.2 |  |
| all cap-contest smokes | Rest | 261 | 37.4 (147) | 37.7 (146) | 23.8 (189) | 23.7 (190) | 6,684 | 16.5 | 10.7 |  |

"other" is a footnote row: a cruiser screened but none inside, or a non-radar cruiser inside next to a radar ship of another class.

Table 2. Top 6 minus Rest inside each cover group (difference, 95% interval; * = clear).
| cover | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 |
|---|---|---|---|---|---|---|---|
| radar cruiser inside | -17.3 (-39.6 to +4.2) | -20.9 (-44.4 to +0.2) | -4.4 (-15.7 to +6.0) | -4.0 (-15.3 to +6.2) | +4,704 (-4,009 to +11,273) | -3.9 (-24.9 to +10.8) | +0.7 (-13.8 to +10.6) |
| non-radar cruiser inside | too few | too few | too few | too few | +9,436 (-13,316 to +25,028) | +13.9 (-22.2 to +66.7) | -20.8 (-66.7 to +37.5) |
| no cruiser | +50.7 (+40.9 to +66.4 *) | +50.7 (+40.9 to +66.4 *) | -6.9 (-24.4 to +7.1) | -6.9 (-24.4 to +7.1) | +799 (-1,648 to +2,620) | -2.1 (-17.9 to +7.5) | -3.9 (-9.8 to +0.4) |
| other | -26.7 (-56.3 to +2.5) | -26.7 (-56.3 to +2.5) | -8.3 (-29.8 to +9.8) | -8.3 (-29.8 to +9.8) | -744 (-6,566 to +6,097) | -1.6 (-25.6 to +20.1) | +0.5 (-17.7 to +18.3) |
| all cap-contest smokes | +24.1 (+10.4 to +38.3 *) | +23.9 (+10.2 to +38.0 *) | -10.1 (-19.5 to -2.4 *) | -10.0 (-19.3 to -2.3 *) | +5,255 (+260 to +8,765 *) | -1.9 (-12.3 to +6.5) | -1.5 (-8.6 to +4.9) |

Table 3. The gap inside each group: one kind of cover minus another (difference, 95% interval; * = clear).
| gap | group | n a / n b | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| radar cruiser inside minus no cruiser | All | 104 / 191 | +37.7 (+21.5 to +55.2 *) | +39.0 (+21.7 to +57.9 *) | -7.8 (-16.8 to +0.3) | -8.0 (-16.9 to +0.0) | +13,368 (+8,699 to +17,029 *) | -0.1 (-8.9 to +9.7) | +3.2 (-4.3 to +10.6) |  |
| radar cruiser inside minus no cruiser | Top 6 | 55 / 46 | -9.6 (-29.0 to +3.8) | -9.6 (-29.0 to +3.8) | -4.8 (-22.2 to +8.5) | -4.8 (-22.2 to +8.5) | +14,977 (+9,602 to +18,875 *) | -0.3 (-14.6 to +11.8) | +6.6 (-1.5 to +12.2) |  |
| radar cruiser inside minus no cruiser | Rest | 49 / 145 | +58.5 (+43.0 to +75.5 *) | +62.1 (+46.1 to +80.6 *) | -7.4 (-20.9 to +3.4) | -7.8 (-21.0 to +2.8) | +11,072 (+6,196 to +16,361 *) | +1.5 (-12.2 to +17.1) | +1.9 (-8.9 to +14.0) |  |
| radar cruiser inside minus non-radar cruiser inside | All | 104 / 17 | +17.3 (-19.5 to +70.6) | +18.6 (-17.4 to +72.1) | -17.4 (-48.2 to +12.5) | -17.5 (-48.4 to +12.1) | +1,833 (-7,864 to +10,479) | -3.1 (-31.2 to +18.3) | -12.9 (-47.1 to +11.4) |  |
| radar cruiser inside minus non-radar cruiser inside | Top 6 | 55 / 8 | too few | too few | too few | too few | -946 (-8,288 to +10,423) | -12.3 (-71.4 to +18.8) | -1.6 (-65.2 to +15.9) | small n |
| radar cruiser inside minus non-radar cruiser inside | Rest | 49 / 9 | too few | too few | -34.2 (-71.2 to +16.2) | -34.6 (-71.4 to +15.6) | +3,785 (-13,779 to +13,376) | +5.6 (-25.2 to +27.3) | -23.1 (-64.8 to +15.5) | small n |

Table 3b. Like with like: only smokes whose contested cap was neutral at activation (a neutral cap is easier to take).
| cover | group | n (early) | we took, contested cap % (n) | enemy took, contested cap % (n) |
|---|---|---|---|---|
| radar cruiser inside | All | 30 (26) | 66.7 (30) | 16.7 (30) |
| radar cruiser inside | Top 6 | 19 (15) | 63.2 (19) | 15.8 (19) |
| radar cruiser inside | Rest | 11 (11) | 72.7 (11) | 18.2 (11) |
| no cruiser | All | 49 (30) | 38.8 (49) | 20.4 (49) |
| no cruiser | Top 6 | 14 (7) | 78.6 (14) | 7.1 (14) |
| no cruiser | Rest | 35 (23) | 22.9 (35) | 25.7 (35) |

Radar cruiser inside minus no cruiser on neutral caps: All: we took +27.9 (+6.9 to +46.4 *), enemy took -3.7 (-20.0 to +12.5); Top 6: we took -15.4 (-60.0 to +12.2), enemy took +8.7 (-11.1 to +28.6); Rest: we took +49.9 (+34.1 to +75.2 *), enemy took -7.5 (-31.7 to +18.8).

Table 4. Cap-contest smokes with a radar cruiser inside (104): radar pressed from the smoke or not. "Pressed" = a ship of the smoking team pressed radar while standing in this smoke (radar log).
|  | group | n (pressed by a cruiser) | we took, contested cap % (n) | we took, nearest cap % (n) | enemy took, contested cap % (n) | enemy took, nearest cap % (n) | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| radar pressed from the smoke | All | 8 (7) | too few (7) | too few (7) | too few (4) | too few (4) | 22,260 | 0.0 | 0.0 | small n |
| radar pressed from the smoke | Top 6 | 5 (4) | too few (5) | too few (5) | too few (2) | too few (2) | too few | too few | too few | too few |
| radar pressed from the smoke | Rest | 3 (3) | too few (2) | too few (2) | too few (2) | too few (2) | too few | too few | too few | too few |
| not pressed | All | 96 (0) | 71.1 (45) | 72.7 (44) | 14.1 (78) | 13.9 (79) | 16,434 | 15.8 | 11.5 |  |
| not pressed | Top 6 | 50 (0) | 64.0 (25) | 64.0 (25) | 11.9 (42) | 11.9 (42) | 17,484 | 14.0 | 12.0 |  |
| not pressed | Rest | 46 (0) | 80.0 (20) | 84.2 (19) | 16.7 (36) | 16.2 (37) | 15,293 | 17.8 | 10.9 |  |

Table 5. Pressed minus not pressed (difference, 95% interval; * = clear).
| group | n pressed / not | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| All | 8 / 96 | too few | too few | too few | too few | +5,826 (-18,281 to +17,351) | -15.8 (-25.0 to -7.2 *) | -11.5 (-17.3 to -4.9 *) | small n |
| Top 6 | 5 / 50 | too few | too few | too few | too few | too few | too few | too few | too few |
| Rest | 3 / 46 | too few | too few | too few | too few | too few | too few | too few | too few |

Table 6. Top 6 minus Rest inside pressed and inside not pressed.
|  | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 |
|---|---|---|---|---|---|---|---|
| radar pressed from the smoke | too few | too few | too few | too few | too few | too few | too few |
| not pressed | -16.0 (-40.7 to +5.0) | -20.2 (-44.9 to -0.9 *) | -4.8 (-16.0 to +6.3) | -4.3 (-15.8 to +6.6) | +2,191 (-4,775 to +8,178) | -3.8 (-25.8 to +10.7) | +1.1 (-13.2 to +10.7) |

Table 7. Wider reading, because Table 4 is so thin: a cruiser that was inside this smoke pressed radar at some time while the smoke stood, whether the log places the press in this smoke or not (the cruiser had often moved out, or the press was at the smoke edge).
|  | group | n | we took, contested cap % (n) | we took, nearest cap % (n) | enemy took, contested cap % (n) | enemy took, nearest cap % (n) | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|---|
| a cruiser from inside pressed radar while the smoke stood | All | 43 | 68.2 (22) | 71.4 (21) | 18.8 (32) | 18.2 (33) | 18,366 | 20.9 | 16.3 |  |
| a cruiser from inside pressed radar while the smoke stood | Top 6 | 23 | 54.5 (11) | 54.5 (11) | 10.5 (19) | 10.5 (19) | 25,057 | 21.7 | 17.4 |  |
| a cruiser from inside pressed radar while the smoke stood | Rest | 20 | 81.8 (11) | 90.0 (10) | 30.8 (13) | 28.6 (14) | 10,672 | 20.0 | 15.0 |  |
| no such press | All | 61 | 66.7 (30) | 66.7 (30) | 10.0 (50) | 10.0 (50) | 15,836 | 10.0 | 6.6 |  |
| no such press | Top 6 | 32 | 63.2 (19) | 63.2 (19) | 12.0 (25) | 12.0 (25) | 14,816 | 6.2 | 6.2 |  |
| no such press | Rest | 29 | 72.7 (11) | 72.7 (11) | 8.0 (25) | 8.0 (25) | 16,962 | 14.3 | 6.9 |  |

Table 8. Wider reading: press minus no press (difference, 95% interval; * = clear).
| group | n press / none | we took, contested cap % | we took, nearest cap % | enemy took, contested cap % | enemy took, nearest cap % | concealed damage per smoke | died per 100 | caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| All | 43 / 61 | +1.5 (-15.7 to +23.2) | +4.8 (-12.7 to +27.0) | +8.8 (-8.8 to +25.5) | +8.2 (-8.8 to +25.0) | +2,530 (-5,432 to +9,471) | +10.9 (-6.5 to +26.5) | +9.7 (-4.7 to +25.9) |  |
| Top 6 | 23 / 32 | -8.6 (-32.2 to +17.9) | -8.6 (-32.2 to +17.9) | -1.5 (-20.0 to +18.8) | -1.5 (-20.0 to +18.8) | +10,242 (+4,275 to +16,568 *) | +15.5 (-9.5 to +34.7) | +11.1 (-9.5 to +32.4) |  |
| Rest | 20 / 29 | +9.1 (-27.8 to +42.9) | +17.3 (-20.8 to +50.0) | +22.8 (-9.1 to +46.7) | +20.6 (-9.1 to +43.8) | -6,290 (-15,154 to +3,461) | +5.7 (-22.0 to +32.9) | +8.1 (-11.8 to +36.1) |  |

Radar was pressed from the smoke in 9% of the Top 6's 55 such smokes and 6% of the Rest's 49 (gap interval -12.9 to +23.1).

**Top 6 or Shared:** Inside "radar cruiser inside" the Top 6 minus Rest gap is: we took the contested cap -17.3 (-39.6 to +4.2), enemy took it -4.4 (-15.7 to +6.0), died per 100 -3.9 (-24.9 to +10.8), caught per 100 +0.7 (-13.8 to +10.6). Inside "no cruiser": +50.7 (+40.9 to +66.4 *), -6.9 (-24.4 to +7.1), -2.1 (-17.9 to +7.5), -3.9 (-9.8 to +0.4). The extra concealed damage with a radar cruiser inside is in both groups (Top 6 +14,977 (+9,602 to +18,875 *), Rest +11,072 (+6,196 to +16,361 *)): Shared. The Top 6 difference is how often they do it (55 of 130 cap-contest smokes against 49 of 261).

**Clans:** radar cruiser inside: Top 6: BONKZ 15, H-SR 14, RESIN 10, KITE 7, VRTUS 5, HTDOG 4 | Rest: -BN- 6, HFANS 6, EPOXY 5, INCA 5, MACHX 5, KSC 4, MZY 3, PFANS 3, PN 2, KITED 2, RSR 2, MACH 1, BTLST 1, UYSC 1, BONKY 1, SCCC2 1, REEEE 1. Radar pressed from it: Top 6: RESIN 5 | Rest: INCA 1, PN 1, SCCC2 1.

**Could not be done / proxy:** Non-radar cruiser inside has 17 smokes (8 Top 6, 9 Rest): small n overall and too few inside a group wherever the table says so. The pressed split is small inside each group; read the direction only.

**Verdict:** Keep (damage and deaths by cover). The cap line: Keep, reworded with the timeline numbers. Radar pressed from the smoke: Lead (8 smokes; the wider reading is in Tables 7 and 8).

**Changed from round 5b:** round 5b did not redo this table, so the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a1.json`). "-" = too few there. The contested-cap columns and the pressed split are new.

| number | round 5b | round 5c | why |
|---|---|---|---|
| radar cruiser inside, Top 6: we took the nearest cap % | 53.3 | 60.0 | cap timeline (was snapshots) |
| radar cruiser inside, Top 6: enemy took the nearest cap % | 9.1 | 11.4 | cap timeline (was snapshots) |
| radar cruiser inside, Top 6: deaths per 100, now died per 100 | 10.9 | 12.7 | new death metric |
| radar cruiser inside, Rest: we took the nearest cap % | 76.2 | 81.0 | cap timeline (was snapshots) |
| radar cruiser inside, Rest: enemy took the nearest cap % | 10.3 | 15.4 | cap timeline (was snapshots) |
| radar cruiser inside, Rest: deaths per 100, now died per 100 | 10.2 | 16.7 | new death metric |
| non-radar cruiser inside, Top 6: deaths per 100, now died per 100 | 12.5 | 25.0 | new death metric |
| non-radar cruiser inside, Rest: enemy took the nearest cap % | 37.5 | 50.0 | cap timeline (was snapshots) |
| non-radar cruiser inside, Rest: deaths per 100, now died per 100 | 33.3 | 11.1 | new death metric |
| no cruiser, Top 6: we took the nearest cap % | 47.8 | 69.6 | cap timeline (was snapshots) |
| no cruiser, Top 6: enemy took the nearest cap % | 5.4 | 16.2 | cap timeline (was snapshots) |
| no cruiser, Top 6: deaths per 100, now died per 100 | 4.3 | 13.0 | new death metric |
| no cruiser, Rest: we took the nearest cap % | 12.9 | 18.8 | cap timeline (was snapshots) |
| no cruiser, Rest: enemy took the nearest cap % | 20.0 | 23.2 | cap timeline (was snapshots) |
| no cruiser, Rest: deaths per 100, now died per 100 | 8.3 | 15.2 | new death metric |
| other, Top 6: we took the nearest cap % | 11.1 | 33.3 | cap timeline (was snapshots) |
| other, Top 6: enemy took the nearest cap % | 6.2 | 18.8 | cap timeline (was snapshots) |
| other, Top 6: deaths per 100, now died per 100 | 14.3 | 19.1 | new death metric |
| other, Rest: we took the nearest cap % | 57.1 | 60.0 | cap timeline (was snapshots) |
| other, Rest: enemy took the nearest cap % | 22.9 | 27.1 | cap timeline (was snapshots) |
| other, Rest: deaths per 100, now died per 100 | 13.8 | 20.7 | new death metric |

19 other numbers are unchanged: concealed damage in every row, and caught per 100 (it is the same list as round 5 deaths).


### A2. Smoke deaths: conditions, calm smokes, map, time and score, and radar deaths three ways

**Answer:** Both metrics tell the same story about where deaths are: smokes laid 50+ behind (died 34.9 vs 12.4 per 100, caught 23.1 vs 7.5) and smokes where a covered ship was radar-lit (died 27.1 vs 13.1, caught 20.9 vs 6.3). Calm smokes (neither) are 513 of 1074 and lose 8.9 died and 3.7 caught per 100. Radar: of 194 ships that died, 85 (44%) were radar-lit in their last 40 s, 39 (20%) were still lit at death, and 25 (13%) were lit at death with no other detection found; of 124 caught, 65 (52%), 34 (27%) and 20 (16%). Radar seldom found these ships first: of the 39 died ships still lit at death, 36 were already detected just before the radar reached them.

**Numbers:** 1074 destroyer smokes (387 Top 6, 687 Rest). Baseline: died 194 ships, 18.2 [15.0 to 22.5] per 100 (smoker 12.8 [9.8 to 17.0]; cruisers 8.7 [6.5 to 11.4] per 100 sheltering); caught 124, 11.6 [9.4 to 14.7] per 100 (smoker 6.4 [4.5 to 9.4]; cruisers 8.2 [5.9 to 10.7] per 100 sheltering). "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them.

Table 1. Conditions: deaths per 100 destroyer smokes with the condition and without it (difference, 95% interval; * = clear).
| condition | n with / without | died: with / without | died: difference | caught: with / without | caught: difference | with it, Top 6 / Rest (n): died | with it, Top 6 / Rest: caught |
|---|---|---|---|---|---|---|---|
| 50+ behind at activation | 277 / 797 | 34.9 / 12.4 | +22.5 (+15.2 to +30.5 *) | 23.1 / 7.5 | +15.6 (+8.7 to +22.4 *) | 35.6 / 34.7 (59 / 218) | 23.7 / 22.9 |
| team outnumbered at activation | 198 / 876 | 39.3 / 13.4 | +25.9 (+17.6 to +34.3 *) | 27.3 / 8.0 | +19.3 (+11.5 to +26.8 *) | 40.0 / 39.1 (45 / 153) | 26.7 / 27.4 |
| a covered ship was radar-lit while the smoke stood | 388 / 686 | 27.1 / 13.1 | +13.9 (+8.8 to +18.9 *) | 20.9 / 6.3 | +14.6 (+9.3 to +20.5 *) | 22.1 / 30.1 (149 / 239) | 12.1 / 26.4 |
| a covered ship was seen by an enemy ship (surface lit) | 512 / 562 | 27.1 / 10.0 | +17.1 (+12.4 to +23.2 *) | 19.1 / 4.6 | +14.5 (+10.9 to +19.1 *) | 17.3 / 32.7 (185 / 327) | 11.3 / 23.6 |
| a covered ship was lit for firing from smoke | 203 / 871 | 28.4 / 15.8 | +12.5 (+6.7 to +18.7 *) | 25.1 / 8.4 | +16.7 (+9.9 to +25.2 *) | 20.7 / 33.6 (82 / 121) | 14.6 / 32.2 |

Table 2. The same conditions, split by who is lost: the smoker (per 100 smokes) and sheltering cruisers (per 100 sheltering cruisers; n = cruisers).
| condition | smoker died: with / without (difference) | smoker caught: with / without (difference) | cruisers died: with (n) / without (n) (difference) | cruisers caught: with (n) / without (n) (difference) |
|---|---|---|---|---|
| 50+ behind at activation | 25.8 / 8.2 (+17.6 (+11.8 to +24.4 *)) | 14.1 / 3.8 (+10.3 (+5.3 to +16.0 *)) | 18.0 (111) / 6.5 (473) (+11.5 (+4.3 to +19.0 *)) | 17.0 (112) / 6.1 (475) (+10.9 (+4.3 to +16.6 *)) |
| team outnumbered at activation | 28.1 / 9.3 (+18.8 (+10.8 to +27.0 *)) | 16.7 / 4.1 (+12.6 (+5.9 to +19.7 *)) | 27.4 (73) / 6.1 (511) (+21.3 (+12.5 to +29.8 *)) | 24.3 (74) / 5.8 (513) (+18.5 (+9.1 to +26.9 *)) |
| a covered ship was radar-lit while the smoke stood | 18.0 / 9.7 (+8.3 (+4.3 to +12.0 *)) | 11.1 / 3.8 (+7.3 (+3.8 to +11.7 *)) | 12.1 (264) / 5.9 (320) (+6.2 (+1.8 to +10.7 *)) | 12.9 (264) / 4.3 (323) (+8.5 (+3.6 to +13.8 *)) |
| a covered ship was seen by an enemy ship (surface lit) | 18.3 / 7.7 (+10.6 (+6.5 to +15.7 *)) | 10.2 / 3.0 (+7.1 (+3.8 to +11.1 *)) | 12.1 (331) / 4.3 (253) (+7.7 (+3.2 to +13.0 *)) | 12.3 (332) / 2.8 (255) (+9.6 (+5.2 to +14.5 *)) |
| a covered ship was lit for firing from smoke | 14.4 / 12.4 (+2.1 (-2.4 to +6.3)) | 9.8 / 5.6 (+4.2 (-0.1 to +9.8)) | 14.1 (163) / 6.7 (421) (+7.5 (+2.1 to +14.1 *)) | 15.8 (164) / 5.2 (423) (+10.7 (+5.2 to +17.9 *)) |

Definitions: "outnumbered" = fewer of our ships alive than theirs at activation. "Radar-lit" = a covered ship (the smoker or a ship inside or behind) carried the radar flag at some time while the smoke stood, from the radar log. "Seen by an enemy ship" and "lit for firing" = a covered ship has that detection kind recorded while this smoke concealed it.

Calm smokes (not 50+ behind and no covered ship radar-lit): 513 smokes (203 Top 6, 310 Rest). Died 45 ships, 8.9 [6.7 to 12.0] per 100 (smoker 5.7 [3.5 to 8.5]); caught 19, 3.7 [2.2 to 5.7] per 100 (smoker 1.8 [0.6 to 3.2]). The other 561 smokes: died 26.7, caught 18.7 per 100 (calm minus other: died -17.8 (-22.5 to -13.4 *), caught -15.0 (-19.2 to -11.2 *)).

Table 3. Calm smokes, Top 6 against Rest.
| measure | Top 6 (n) | Rest (n) | Top 6 minus Rest |
|---|---|---|---|
| died per 100 | 5.4 (203) | 11.2 (305) | -5.7 (-10.9 to -1.9 *) |
| caught per 100 | 2.5 (203) | 4.5 (310) | -2.0 (-5.1 to +0.9) |
| smoker died per 100 | 3.0 (203) | 7.5 (305) | -4.6 (-9.5 to -0.8 *) |
| smoker caught per 100 | 0.5 (203) | 2.6 (310) | -2.1 (-4.2 to -0.3 *) |
| cruisers died per 100 sheltering | 3.8 (132) | 6.6 (136) | -2.8 (-7.2 to +1.9) |
| cruisers caught per 100 sheltering | 3.0 (132) | 3.6 (138) | -0.6 (-4.9 to +3.5) |

Table 4. By map.
|  | n (Top 6 / Rest) | died per 100 [95%] | died: Top 6 / Rest | died: Top 6 minus Rest | caught per 100 [95%] | caught: Top 6 / Rest | caught: Top 6 minus Rest | smoker died / caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | 238 (110 / 128) | 15.1 [10.9 to 22.0] | 10.9 / 18.8 | -7.8 (-19.7 to +1.8) | 11.8 [8.0 to 18.4] | 6.4 / 16.4 | -10.0 (-20.0 to -2.1 *) | 10.5 / 7.1 |  |
| Hotspot | 235 (80 / 155) | 15.7 [11.3 to 21.1] | 13.8 / 16.8 | -3.0 (-12.8 to +7.9) | 7.7 [5.2 to 10.1] | 7.5 / 7.7 | -0.2 (-6.5 to +6.3) | 9.4 / 3.4 |  |
| Loop | 142 (41 / 101) | 18.3 [11.4 to 27.0] | 17.1 / 18.8 | -1.7 (-20.8 to +14.5) | 10.6 [5.3 to 17.1] | 9.8 / 10.9 | -1.1 (-15.0 to +10.7) | 14.1 / 6.3 |  |
| Mountain Range | 132 (55 / 77) | 18.4 [9.7 to 29.3] | 16.4 / 20.0 | -3.6 (-22.6 to +17.4) | 8.3 [3.4 to 14.7] | 7.3 / 9.1 | -1.8 (-12.5 to +10.7) | 14.4 / 3.8 |  |
| Land of Fire | 128 (48 / 80) | 21.1 [11.1 to 37.9] | 8.3 / 28.8 | -20.4 (-46.7 to +1.4) | 14.1 [6.9 to 25.8] | 4.2 / 20.0 | -15.8 (-34.3 to -2.2 *) | 15.6 / 7.8 |  |
| Sea of Fortune | 117 (38 / 79) | 17.9 [11.4 to 27.3] | 13.2 / 20.2 | -7.1 (-23.6 to +4.9) | 13.7 [7.7 to 21.9] | 7.9 / 16.5 | -8.6 (-22.5 to +3.0) | 12.8 / 8.6 |  |
| Okinawa | 82 (15 / 67) | 29.3 [22.1 to 38.5] | 26.7 / 29.9 | -3.2 (-26.2 to +20.1) | 21.9 [12.8 to 31.5] | 20.0 / 22.4 | -2.4 (-20.0 to +23.1) | 19.5 / 12.2 |  |

Table 5. By time of activation (replay clock).
|  | n (Top 6 / Rest) | died per 100 [95%] | died: Top 6 / Rest | died: Top 6 minus Rest | caught per 100 [95%] | caught: Top 6 / Rest | caught: Top 6 minus Rest | smoker died / caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| 0-5 min | 308 (104 / 204) | 8.5 [5.3 to 12.3] | 5.8 / 9.9 | -4.1 (-11.1 to +1.3) | 7.5 [4.7 to 11.2] | 2.9 / 9.8 | -6.9 (-12.9 to -2.0 *) | 5.6 / 3.6 |  |
| 5-10 min | 494 (179 / 315) | 21.8 [16.2 to 28.5] | 12.8 / 27.0 | -14.2 (-25.7 to -4.1 *) | 12.6 [9.1 to 16.9] | 8.4 / 14.9 | -6.5 (-13.6 to -0.1 *) | 15.5 / 7.5 |  |
| 10-15 min | 246 (97 / 149) | 22.4 [17.6 to 27.3] | 21.6 / 23.0 | -1.3 (-13.3 to +7.6) | 14.2 [9.5 to 19.1] | 9.3 / 17.4 | -8.2 (-17.4 to +0.8) | 15.9 / 7.7 |  |
| 15+ min | 26 (7 / 19) | 23.1 [7.4 to 42.3] | too few / 21.1 | too few | 15.4 [3.7 to 30.0] | too few / 10.5 | too few | 15.4 / 7.7 |  |

Table 6. By score at activation.
|  | n (Top 6 / Rest) | died per 100 [95%] | died: Top 6 / Rest | died: Top 6 minus Rest | caught per 100 [95%] | caught: Top 6 / Rest | caught: Top 6 minus Rest | smoker died / caught per 100 | note |
|---|---|---|---|---|---|---|---|---|---|
| ahead 50+ | 372 (167 / 205) | 12.9 [9.4 to 17.8] | 10.8 / 14.7 | -3.9 (-12.5 to +4.2) | 6.5 [4.4 to 9.1] | 5.4 / 7.3 | -1.9 (-6.8 to +2.1) | 9.4 / 3.8 |  |
| level | 425 (161 / 264) | 11.9 [9.6 to 15.1] | 8.1 / 14.2 | -6.2 (-11.0 to -2.5 *) | 8.5 [6.3 to 11.3] | 3.7 / 11.4 | -7.6 (-11.7 to -4.3 *) | 7.1 / 3.8 |  |
| behind 50+ | 277 (59 / 218) | 34.9 [27.2 to 44.3] | 35.6 / 34.7 | +0.9 (-20.9 to +16.3) | 23.1 [17.1 to 30.0] | 23.7 / 22.9 | +0.8 (-14.8 to +13.6) | 25.8 / 14.1 |  |

Radar deaths. "Died" ships: 194 deaths (194 distinct ships). "Caught" ships: 124 death records (124 distinct ships). Radar-lit comes from the radar log for that ship. (a) a radar-lit span touches its last 40 s. (b) a radar-lit span covers the moment of death, give or take 2 s. (c) as (b), and the hydro log does not have it lit at death, and no smoke record of that ship shows a first detection of another kind (seen by a ship, proximity, aircraft, lit for firing) in its last 20 s.

Table 7. Radar deaths three ways.
| metric | reading | deaths | smoker destroyer | sheltering cruiser | other | Top 6 | Rest | share, Top 6 minus Rest |
|---|---|---|---|---|---|---|---|---|
| died | (a) radar-lit at some time in its last 40 s | 85 of 194 (44%) | 65 of 136 | 18 of 51 | 2 of 7 | 21 of 52 (40%) | 64 of 142 (45%) | -4.7 (-24.2 to +8.2) |
| died | radar-lit at some time in its last 20 s (for comparison with round 5b) | 75 of 194 (39%) | 58 of 136 | 15 of 51 | 2 of 7 | 17 of 52 (33%) | 58 of 142 (41%) | -8.2 (-30.9 to +7.3) |
| died | (b) still radar-lit at death | 39 of 194 (20%) | 31 of 136 | 7 of 51 | 1 of 7 | 8 of 52 (15%) | 31 of 142 (22%) | -6.4 (-22.0 to +3.9) |
| died | (c) radar-lit at death, no other detection found | 25 of 194 (13%) | 21 of 136 | 4 of 51 | 0 of 7 | 5 of 52 (10%) | 20 of 142 (14%) | -4.5 (-14.8 to +3.2) |
| caught | (a) radar-lit at some time in its last 40 s | 65 of 124 (52%) | 41 of 69 | 22 of 48 | 2 of 7 | 10 of 29 (34%) | 55 of 95 (58%) | -23.4 (-43.3 to -4.9 *) |
| caught | radar-lit at some time in its last 20 s (for comparison with round 5b) | 57 of 124 (46%) | 36 of 69 | 19 of 48 | 2 of 7 | 8 of 29 (28%) | 49 of 95 (52%) | -24.0 (-50.1 to -3.1 *) |
| caught | (b) still radar-lit at death | 34 of 124 (27%) | 22 of 69 | 11 of 48 | 1 of 7 | 1 of 29 (3%) | 33 of 95 (35%) | -31.3 (-43.0 to -19.5 *) |
| caught | (c) radar-lit at death, no other detection found | 20 of 124 (16%) | 16 of 69 | 4 of 48 | 0 of 7 | 0 of 29 (0%) | 20 of 95 (21%) | -21.1 (-29.8 to -12.4 *) |

- died: of the 39 still lit at death, 0 were also hydro-lit and 14 had another kind of detection start in the last 20 s ({'surface lit': 12, 'smoke fire penalty': 2}). The smoke record covers the whole last 20 s for 25, part of it for 14, none of it for 0. Cross-check from the ship's own track: at the last sample before that radar span began the ship was undetected in 3, already detected in 36 (unknown 0); 2 deaths are both (c) and undetected before the radar. Median time lit before death 12.4 s. Radar ships: {'Moskva': 15, 'Brisbane': 8, 'San Martín': 5, 'Des Moines': 4, 'Yueyang': 2, 'Gdańsk': 1}.
- caught: of the 34 still lit at death, 1 were also hydro-lit and 13 had another kind of detection start in the last 20 s ({'surface lit': 10, 'smoke fire penalty': 3}). The smoke record covers the whole last 20 s for 22, part of it for 11, none of it for 1. Cross-check from the ship's own track: at the last sample before that radar span began the ship was undetected in 1, already detected in 33 (unknown 0); 0 deaths are both (c) and undetected before the radar. Median time lit before death 13.55 s. Radar ships: {'Moskva': 17, 'Brisbane': 5, 'San Martín': 3, 'Des Moines': 3, 'Gdańsk': 1, 'Småland': 1}.
- Clans, (b) still lit at death, died: Top 6: RESIN 4, BONKZ 3, VRTUS 1 | Rest: EPOXY 5, KITED 3, HFANS 3, REEEE 3, BTLST 2, UYSC 2, -BN- 2, RSR 2, MANBA 1, KM 1, SCCC2 1, 5D 1, KSE 1, INCA 1, MACH 1, MZY 1, PFANS 1.

**Top 6 or Shared:** Shared pattern, Rest pays more. The conditions raise deaths in both groups (Table 1, last columns). Calm smokes: Top 6 minus Rest died -5.7 (-10.9 to -1.9 *), caught -2.0 (-5.1 to +0.9). Share of died ships radar-lit in the last 40 s: Top 6 40%, Rest 45% (-4.7 (-24.2 to +8.2)); still lit at death: 15% vs 22% (-6.4 (-22.0 to +3.9)). On caught ships the Rest share is clearly higher: last 40 s 34% vs 58% (-23.4 (-43.3 to -4.9 *)), still lit at death 1 of 29 vs 33 of 95 (-31.3 (-43.0 to -19.5 *)). The two metrics disagree here, so treat the group gap in radar deaths as a lead.

**Clans:** highest map on "died" is Okinawa (29.3 per 100); smokes with a death there: Top 6: KITE 2, BONKZ 1, HTDOG 1 | Rest: EPOXY 2, -BN- 2, REEEE 2, HFANS 2, BTLST 1, 5D 1, OGF 1, PN 1, RSR 1, KSE 1, KM 1, NGA 1, MACHX 1, MZY 1.

**Could not be done / proxy:** Reading (c) is a floor on other detection, not a full check. The batch keeps, per ship and per smoke, only the first moment of each detection kind while that smoke concealed it; it has no second-by-second list of who saw the ship. So (c) removes deaths where another kind of detection started in the last 20 s, or hydro had the ship, but it cannot see a ship that an enemy had been watching for longer, or one that died after the smoke record ended (the record misses the last 20 s entirely for 0 of the 39 died ships lit at death and 1 of the 34 caught). The track cross-check (undetected just before the radar arrived) is the closest proxy for "radar is what found it". Read (c) as an upper limit on deaths owed to radar alone.

**Verdict:** Keep (conditions, calm smokes, radar readings (a) and (b)). Lead for (c).

**Changed from round 5b:** the "round 5b" column is `round5b/part-a/out-a2.json` (round 5 with the clock fix), or the round 5b redo N2 where the row says so.

| number | round 5b | round 5c | why |
|---|---|---|---|
| deaths in destroyer smokes: died (round 5b N1 counted 201 ships at risk in the smoke window) | 201 | 194 | new death metric: exactly 20 s after dispersal, each ship once, 9 smokes left out |
| 50+ behind at activation: deaths per 100 with / without, now died | 23.1 / 7.5 | 34.9 / 12.4 | new death metric |
| team outnumbered at activation: deaths per 100 with / without, now died | 27.3 / 8.0 | 39.3 / 13.4 | new death metric |
| a covered ship was seen by an enemy ship (surface lit): deaths per 100 with / without, now died | 19.1 / 4.6 | 27.1 / 10.0 | new death metric |
| a covered ship was lit for firing from smoke: deaths per 100 with / without, now died | 25.1 / 8.4 | 28.4 / 15.8 | new death metric |
| radar-lit covered ship: deaths per 100 with / without, now died | 20.9 / 6.3 | 27.1 / 13.1 | new death metric |
| calm smokes: n (round 5b N2) | 515 | 513 | lit_covered from the round 5c library in place of the radar test in the round 5b script; 2 smokes differ |
| calm smokes: deaths per 100, now died | 3.7 | 8.9 | new death metric |
| Sleeping Giant: deaths per 100, now died | 11.8 | 15.1 | new death metric |
| Hotspot: deaths per 100, now died | 7.7 | 15.7 | new death metric |
| Loop: deaths per 100, now died | 10.6 | 18.3 | new death metric |
| Mountain Range: deaths per 100, now died | 8.3 | 18.4 | new death metric |
| Land of Fire: deaths per 100, now died | 14.1 | 21.1 | new death metric |
| Sea of Fortune: deaths per 100, now died | 13.7 | 17.9 | new death metric |
| Okinawa: deaths per 100, now died | 22.0 | 29.3 | new death metric |
| ahead 50+: deaths per 100, now died | 6.5 | 12.9 | new death metric |
| level: deaths per 100, now died | 8.5 | 11.9 | new death metric |
| behind 50+: deaths per 100, now died | 23.1 | 34.9 | new death metric |
| 0-5 min: n | 306 | 308 | time from the replay clock (e0), not the HUD clock |
| 0-5 min: deaths per 100, now died | 7.5 | 8.5 | new death metric |
| 5-10 min: n | 495 | 494 | time from the replay clock (e0), not the HUD clock |
| 5-10 min: deaths per 100, now died | 12.5 | 21.8 | new death metric |
| 10-15 min: n | 247 | 246 | time from the replay clock (e0), not the HUD clock |
| 10-15 min: deaths per 100, now died | 14.2 | 22.4 | new death metric |
| 15+ min: deaths per 100, now died | 15.4 | 23.1 | new death metric |
| caught deaths radar-lit in the last 20 s (round 5b N2: 56 of 124) | 56 | 57 | same radar log; one death sits on the 20 s edge (which rule moved it was not traced) |
| died ships radar-lit in the last 40 s | - | 85 of 194 | new death metric |
| still radar-lit at death (died / caught) | - | 39 of 194 / 34 of 124 | new reading |
| radar-lit at death, no other detection found (died / caught) | - | 25 of 194 / 20 of 124 | new reading |

29 other compared numbers are unchanged (caught per 100 is the same list as round 5 deaths wherever the smokes in the row are the same).


### A3. Somers vs Gearing inside Top 6 and inside Rest

**Answer:** Inside the Top 6 the two ships lose about the same: died 17.8 (Somers) vs 16.2 (Gearing) per 100, caught 7.8 vs 9.5. Inside the Rest the Gearing loses more: died 19.4 vs 32.3 (gap -12.9 (-24.5 to -0.4 *)), caught 11.8 vs 23.6 (gap -11.8 (-23.7 to -2.1 *)). Both metrics agree (caught: clear; died: clear), and the extra loss is the smoker itself, not the sheltering cruisers (smoker died -12.6 (-28.4 to +0.2), cruisers died +0.5 (-7.0 to +11.5)). The gap goes with who sails the Gearing, not with the ship.

**Numbers:** 260 Somers smokes (90 Top 6, 170 Rest) and 180 Gearing smokes (74 Top 6, 106 Rest). "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them. Smoker rates are per 100 smokes; cruiser rates are per 100 sheltering cruisers (n = cruisers).

Table 1. Deaths per 100 by ship and group [95% interval].
| group | ship | n | died: all | caught: all | died: smoker | caught: smoker | died: cruisers (n) | caught: cruisers (n) | note |
|---|---|---|---|---|---|---|---|---|---|
| All | Somers | 260 | 18.9 [12.5 to 25.4] | 10.4 [7.0 to 13.4] | 10.4 [6.2 to 15.2] | 3.9 [1.9 to 6.2] | 9.4 [5.2 to 13.9] (234) | 7.3 [4.2 to 10.3] (234) |  |
| All | Gearing | 180 | 25.4 [18.1 to 35.5] | 17.8 [11.5 to 27.0] | 16.8 [8.8 to 30.5] | 8.3 [2.2 to 20.0] | 8.2 [3.6 to 12.1] (146) | 9.4 [4.5 to 13.9] (149) |  |
| Top 6 | Somers | 90 | 17.8 [2.5 to 30.0] | 7.8 [2.5 to 12.4] | 10.0 [0.0 to 20.3] | 2.2 [0.0 to 5.4] | 8.2 [0.0 to 14.9] (85) | 5.9 [0.0 to 9.9] (85) |  |
| Top 6 | Gearing | 74 | 16.2 [11.1 to 22.6] | 9.5 [5.7 to 10.7] | 8.1 [3.7 to 21.4] | 1.4 [0.0 to 7.1] | 6.8 [0.0 to 8.7] (73) | 6.8 [0.0 to 8.7] (73) |  |
| Rest | Somers | 170 | 19.4 [14.7 to 26.2] | 11.8 [7.7 to 15.6] | 10.6 [6.5 to 16.4] | 4.7 [2.1 to 7.8] | 10.1 [5.1 to 15.9] (149) | 8.1 [4.3 to 12.1] (149) |  |
| Rest | Gearing | 106 | 32.3 [21.3 to 45.5] | 23.6 [13.8 to 36.6] | 23.2 [10.5 to 40.8] | 13.2 [3.0 to 30.9] | 9.6 [0.0 to 14.8] (73) | 11.8 [2.9 to 17.1] (76) |  |

Table 2. Somers minus Gearing inside each group (difference, 95% interval; * = clear).
| group | n Somers / Gearing | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 | cruisers died per 100 sheltering | cruisers caught per 100 sheltering |
|---|---|---|---|---|---|---|---|
| All | 260 / 180 | -6.6 (-18.4 to +3.5) | -7.4 (-16.6 to -0.1 *) | -6.4 (-19.6 to +3.3) | -4.5 (-16.0 to +2.4) | +1.2 (-4.2 to +7.8) | -2.1 (-7.2 to +3.4) |
| Top 6 | 90 / 74 | +1.6 (-18.2 to +17.4) | -1.7 (-6.7 to +4.9) | +1.9 (-19.9 to +14.5) | +0.9 (-7.6 to +5.6) | +1.4 (-7.2 to +10.8) | -1.0 (-7.2 to +7.3) |
| Rest | 170 / 106 | -12.9 (-24.5 to -0.4 *) | -11.8 (-23.7 to -2.1 *) | -12.6 (-28.4 to +0.2) | -8.5 (-23.8 to +1.6) | +0.5 (-7.0 to +11.5) | -3.8 (-10.4 to +7.0) |

Table 3. Top 6 minus Rest on each ship (difference, 95% interval; * = clear).
| ship | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 | cruisers died per 100 sheltering | cruisers caught per 100 sheltering |
|---|---|---|---|---|---|---|
| Somers | -1.6 (-19.1 to +11.8) | -4.0 (-10.7 to +2.1) | -0.6 (-12.2 to +9.4) | -2.5 (-6.2 to +1.9) | -1.8 (-12.2 to +6.8) | -2.2 (-9.2 to +3.4) |
| Gearing | -16.1 (-30.4 to -3.6 *) | -14.1 (-26.6 to -4.8 *) | -15.1 (-32.1 to +1.8) | -11.9 (-27.3 to -1.0 *) | -2.7 (-10.5 to +5.4) | -5.0 (-12.1 to +3.4) |

Rest Gearing, leaving one clan out at a time: died per 100 stays between 28.9 and 34.8, caught between 19.6 and 26.1. By clan (n smokes, died, caught): KSC 29/7/6, -BN- 18/3/2, BTLST 11/4/4, 5D 9/6/6, OGF 9/6/3, RSR 9/3/2, INCA 7/0/0, HFANS 5/1/0, RMN 3/1/1, EPOXY 3/0/0, KM 2/0/0, UYSC 1/1/1.

**Top 6 or Shared:** Top 6. On the Gearing, Top 6 minus Rest is died -16.1 (-30.4 to -3.6 *) and caught -14.1 (-26.6 to -4.8 *); on the Somers it is died -1.6 (-19.1 to +11.8) and caught -4.0 (-10.7 to +2.1). The Rest lose more ships around their Gearing smokes; the Somers numbers are close in both groups.

**Clans:** Somers: Top 6: RESIN 38, H-SR 33, BONKZ 12, VRTUS 7 | Rest: HFANS 28, REEEE 25, MZY 22, EPOXY 18, MACHX 17, BONKY 14, -BN- 12, NGA 11, PFANS 8, PN 5, UYSC 5, KITED 3, RSR 1, INCA 1. Gearing: Top 6: BONKZ 37, KITE 23, VRTUS 10, HTDOG 4 | Rest: KSC 29, -BN- 18, BTLST 11, 5D 9, OGF 9, RSR 9, INCA 7, HFANS 5, RMN 3, EPOXY 3, KM 2, UYSC 1.

**Verdict:** Keep.

**Changed from round 5b:** round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a3.json`).

| number | round 5b | round 5c | why |
|---|---|---|---|
| Top 6, Somers, all ships: deaths per 100, now died | 7.8 | 17.8 | new death metric |
| Top 6, Gearing, all ships: deaths per 100, now died | 9.5 | 16.2 | new death metric |
| Top 6, all ships: Somers minus Gearing, now caught | -1.7 (-6.9 to +4.7) | -1.7 (-6.7 to +4.9) | same list; interval now from diff_ci |
| Top 6, all ships: Somers minus Gearing, now died | -1.7 (-6.9 to +4.7) | +1.6 (-18.2 to +17.4) | new death metric |
| Top 6, Somers, smoker: deaths per 100, now died | 2.2 | 10.0 | new death metric |
| Top 6, Gearing, smoker: deaths per 100, now died | 1.4 | 8.1 | new death metric |
| Top 6, smoker: Somers minus Gearing, now caught | +0.9 (-7.7 to +5.7) | +0.9 (-7.6 to +5.6) | same list; interval now from diff_ci |
| Top 6, smoker: Somers minus Gearing, now died | +0.9 (-7.7 to +5.7) | +1.9 (-19.9 to +14.5) | new death metric |
| Top 6, Somers, sheltering cruisers: deaths per 100, now died | 5.9 | 8.2 | new death metric |
| Top 6, sheltering cruisers: Somers minus Gearing, now caught | -1.0 (-7.1 to +7.0) | -1.0 (-7.2 to +7.3) | same list; interval now from diff_ci |
| Top 6, sheltering cruisers: Somers minus Gearing, now died | -1.0 (-7.1 to +7.0) | +1.4 (-7.2 to +10.8) | new death metric |
| Rest, Somers, all ships: deaths per 100, now died | 11.8 | 19.4 | new death metric |
| Rest, Gearing, all ships: deaths per 100, now died | 23.6 | 32.3 | new death metric |
| Rest, all ships: Somers minus Gearing, now caught | -11.8 (-24.0 to -1.5) | -11.8 (-23.7 to -2.1) | same list; interval now from diff_ci |
| Rest, all ships: Somers minus Gearing, now died | -11.8 (-24.0 to -1.5) | -12.9 (-24.5 to -0.4) | new death metric |
| Rest, Somers, smoker: deaths per 100, now died | 4.7 | 10.6 | new death metric |
| Rest, Gearing, smoker: deaths per 100, now died | 13.2 | 23.2 | new death metric |
| Rest, smoker: Somers minus Gearing, now caught | -8.5 (-25.3 to +1.6) | -8.5 (-23.8 to +1.6) | same list; interval now from diff_ci |
| Rest, smoker: Somers minus Gearing, now died | -8.5 (-25.3 to +1.6) | -12.6 (-28.4 to +0.2) | new death metric |
| Rest, Somers, sheltering cruisers: deaths per 100, now died | 8.1 | 10.1 | new death metric |
| Rest, Gearing, sheltering cruisers: deaths per 100, now died | 11.8 | 9.6 | new death metric |
| Rest, sheltering cruisers: Somers minus Gearing, now caught | -3.8 (-10.4 to +6.5) | -3.8 (-10.4 to +7.0) | same list; interval now from diff_ci |
| Rest, sheltering cruisers: Somers minus Gearing, now died | -3.8 (-10.4 to +6.5) | +0.5 (-7.0 to +11.5) | new death metric |

13 other compared numbers are unchanged (the caught rates).


### A4. Counter-smokes: death rates by angle and for the "what pays" rows

**Answer:** Counter-smokes are costly on both metrics: 24.8 died and 15.0 caught per 100, against 18.2 and 11.5 for all destroyer smokes. By angle, flanking counter-smokes lost 50.0 died / 25.0 caught per 100 against 24.0 / 15.0 head-on; the flanking minus head-on gap is +26.0 (-5.0 to +63.3) on died and +10.0 (-15.4 to +41.1) on caught, so over all clans angle does not clearly separate deaths. Inside the Rest the gap on died is +42.0 (+6.7 to +78.8 *) (clear; only 9 flanking smokes) and on caught +17.9 (-17.3 to +53.0). Of the "what pays" rows, Gearing and flank-smoke-line counter-smokes returned the most damage and also the most deaths (Gearing 45.0 died / 35.0 caught per 100).

**Numbers:** 133 destroyer counter-smokes matched to the enemy smoke they answer (44 Top 6, 89 Rest); 132 have a usable line of fire. "Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); "caught" rates keep them. Here that removes 0 smoke(s). Geometry and damage columns are computed as in round 5; the delay after the enemy smoke now uses the replay clock, which moves 6 smoke(s) to another delay band.

Table 1. By angle off the enemy smoke's line of fire.
|  | n (Top 6 / Rest) | concealed damage [95%] | out-damaged answered % | answered smoke damage | margin [95%] | died per 100 [95%] | caught per 100 [95%] | smoker died / caught per 100 | died: Top 6 / Rest (gap) | caught: Top 6 / Rest (gap) | note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| head-on (under 30) | 100 (35 / 65) | 8,947 [5,933 to 12,413] | 42.0 | 8,495 | +452 [-3,039 to +3,635] | 24.0 [16.4 to 34.5] | 15.0 [9.1 to 23.5] | 16.0 / 7.0 | 22.9 / 24.6 (-18.1 to +15.7) | 14.3 / 15.4 (-15.4 to +16.9) |  |
| oblique (30-60) | 20 (6 / 14) | 6,762 [3,330 to 10,424] | 30.0 | 12,781 | -6,019 [-14,290 to +1,287] | 15.0 [0.0 to 30.0] | 10.0 [0.0 to 23.8] | 10.0 / 5.0 | too few / 21.4 (-) | too few / 14.3 (-) |  |
| flanking (over 60) | 12 (3 / 9) | 2,868 [747 to 6,438] | 16.7 | 5,796 | -2,928 [-7,279 to +1,887] | 50.0 [23.5 to 88.9] | 25.0 [0.0 to 50.0] | 41.7 / 16.7 | too few / 66.7 (-) | too few / 33.3 (-) | small n |

Table 2. Flanking minus head-on (difference, 95% interval; * = clear).
| group | n flanking / head-on | concealed damage | margin | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 | note |
|---|---|---|---|---|---|---|---|---|
| All | 12 / 100 | -6,079 (-10,222 to -562 *) | -3,380 (-8,917 to +2,950) | +26.0 (-5.0 to +63.3) | +10.0 (-15.4 to +41.1) | +25.7 (-3.9 to +59.5) | +9.7 (-9.5 to +30.6) | small n |
| Top 6 | 3 / 35 | too few | too few | too few | too few | too few | too few | too few |
| Rest | 9 / 65 | -4,026 (-9,251 to +2,381) | -1,637 (-7,589 to +5,803) | +42.0 (+6.7 to +78.8 *) | +17.9 (-17.3 to +53.0) | +38.6 (+6.8 to +76.5 *) | +14.5 (-11.1 to +43.0) | small n |

Table 3. The "what pays" rows.
|  | n (Top 6 / Rest) | concealed damage [95%] | out-damaged answered % | answered smoke damage | margin [95%] | died per 100 [95%] | caught per 100 [95%] | smoker died / caught per 100 | died: Top 6 / Rest (gap) | caught: Top 6 / Rest (gap) | note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| radar cruiser inside | 32 (15 / 17) | 18,316 [12,796 to 24,231] | 59.4 | 9,814 | +8,502 [+3,083 to +15,949] | 28.1 [15.6 to 45.8] | 18.8 [7.1 to 36.8] | 12.5 / 3.1 | 26.7 / 29.4 (-31.2 to +45.8) | 20.0 / 17.6 (-23.2 to +56.7) |  |
| Gearing | 20 (11 / 9) | 21,202 [14,133 to 27,738] | 60.0 | 8,329 | +12,873 [+7,286 to +18,694] | 45.0 [21.4 to 84.6] | 35.0 [14.8 to 72.7] | 20.0 / 10.0 | 18.2 / 77.8 (-90.9 to -24.7 *) | 9.1 / 66.7 (-80.9 to -30.4 *) |  |
| flank-smoke-line ships | 52 (19 / 33) | 13,696 [8,684 to 18,162] | 46.1 | 9,285 | +4,411 [-107 to +9,258] | 32.7 [20.0 to 52.2] | 23.1 [12.0 to 39.1] | 15.4 / 5.8 | 26.3 / 36.4 (-39.5 to +26.6) | 15.8 / 27.3 (-35.7 to +21.2) |  |
| laid 11-25 s after the enemy smoke | 43 (15 / 28) | 10,922 [6,475 to 15,826] | 41.9 | 11,257 | -335 [-7,449 to +5,091] | 25.6 [13.6 to 42.4] | 20.9 [9.3 to 36.2] | 13.9 / 9.3 | 13.3 / 32.1 (-47.6 to +29.2) | 13.3 / 25.0 (-36.4 to +36.3) |  |
| 6-9 km from the answered smoke | 51 (17 / 34) | 9,740 [4,696 to 15,479] | 39.2 | 9,357 | +383 [-3,868 to +4,770] | 29.4 [14.8 to 47.7] | 19.6 [8.8 to 35.1] | 19.6 / 9.8 | 41.2 / 23.5 (-14.3 to +60.0) | 23.5 / 17.6 (-20.8 to +51.1) |  |
| answered smoke within 30 degrees of straight ahead | 65 (22 / 43) | 9,023 [5,725 to 12,308] | 43.1 | 7,432 | +1,592 [-2,145 to +5,334] | 24.6 [13.2 to 39.2] | 16.9 [7.3 to 29.8] | 12.3 / 4.6 | 22.7 / 25.6 (-28.2 to +24.3) | 18.2 / 16.3 (-18.9 to +31.8) |  |
| all counter-smokes | 133 (44 / 89) | 8,003 [5,499 to 10,381] | 37.6 | 8,832 | -830 [-3,565 to +1,548] | 24.8 [17.4 to 34.8] | 15.0 [9.9 to 22.1] | 17.3 / 7.5 | 18.2 / 28.1 (-24.5 to +5.3) | 11.4 / 16.9 (-16.9 to +8.5) |  |
| all, Top 6 | 44 (44 / 0) | 11,140 [7,212 to 14,552] | 43.2 | 12,184 | -1,044 [-6,108 to +1,940] | 18.2 [8.3 to 29.0] | 11.4 [4.2 to 25.0] | 11.4 / 4.5 | 18.2 / too few (-) | 11.4 / too few (-) |  |
| all, Rest | 89 (0 / 89) | 6,452 [3,959 to 9,194] | 34.8 | 7,175 | -724 [-4,322 to +2,568] | 28.1 [19.5 to 41.2] | 16.9 [10.6 to 26.0] | 20.2 / 9.0 | too few / 28.1 (-) | too few / 16.9 (-) |  |

Table 4. Each "what pays" row minus the other counter-smokes (difference, 95% interval; * = clear).
|  | concealed damage | died per 100 | caught per 100 | smoker died per 100 | smoker caught per 100 |
|---|---|---|---|---|---|
| radar cruiser inside | +13,581 (+7,799 to +19,231 *) | +4.4 (-13.1 to +23.9) | +4.9 (-11.1 to +23.8) | -6.3 (-18.3 to +7.0) | -5.8 (-13.0 to +3.5) |
| Gearing | +15,536 (+4,982 to +22,170 *) | +23.8 (-3.0 to +69.9) | +23.5 (+1.0 to +63.6 *) | +3.2 (-12.9 to +32.7) | +2.9 (-8.7 to +28.9) |
| flank-smoke-line ships | +9,348 (+3,944 to +13,751 *) | +12.9 (-3.8 to +32.6) | +13.2 (+0.2 to +27.9 *) | -3.1 (-16.0 to +11.0) | -2.9 (-10.1 to +5.8) |
| laid 11-25 s after the enemy smoke | +4,314 (-502 to +8,533) | +1.1 (-13.2 to +21.3) | +8.7 (-2.9 to +26.4) | -4.9 (-18.5 to +11.1) | +2.6 (-6.9 to +15.5) |
| 6-9 km from the answered smoke | +2,818 (-2,392 to +8,362) | +7.5 (-12.4 to +26.4) | +7.4 (-6.7 to +23.4) | +3.8 (-11.7 to +18.4) | +3.7 (-5.1 to +15.2) |
| answered smoke within 30 degrees of straight ahead | +1,996 (-1,978 to +6,485) | -0.4 (-16.7 to +16.1) | +3.7 (-9.7 to +17.7) | -9.8 (-22.7 to +1.9) | -5.7 (-14.9 to +3.6) |

**Top 6 or Shared:** All counter-smokes, Top 6 against Rest: died 18.2 vs 28.1 (-9.9 (-24.5 to +5.3)), caught 11.4 vs 16.9 (-5.5 (-16.9 to +8.5)). Flanking minus head-on inside the Top 6: died too few; inside the Rest: died +42.0 (+6.7 to +78.8 *). Gearing counter-smokes: Top 6 18.2 died / 9.1 caught per 100 against Rest 77.8 / 66.7 (gaps -90.9 to -24.7 * and -80.9 to -30.4 *; n 11 and 9, small). The deaths that go with the high-damage rows are mostly the Rest's.

**Clans:** flanking counter-smokes: Top 6: KITE 2, RESIN 1 | Rest: HFANS 2, 5D 2, -BN- 1, BONKY 1, SCCC2 1, KSE 1, MACHX 1. Gearing counter-smokes: Top 6: BONKZ 8, KITE 3 | Rest: KSC 3, OGF 2, -BN- 2, BTLST 1, 5D 1.

**Could not be done / proxy:** Nothing missing. The line of fire is itself a proxy (where the enemy smoke's damage landed, or where our ships were when it hit nobody), as in round 5.

**Verdict:** Keep the "what pays" rows with both death columns; angle and deaths: Lead only.

**Changed from round 5b:** round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a4.json`).

| number | round 5b | round 5c | why |
|---|---|---|---|
| head-on (under 30): deaths per 100, now died | 15.0 | 24.0 | new death metric |
| head-on (under 30): smoker died per 100, now smoker died | 7.0 | 16.0 | new death metric |
| oblique (30-60): deaths per 100, now died | 10.0 | 15.0 | new death metric |
| oblique (30-60): smoker died per 100, now smoker died | 5.0 | 10.0 | new death metric |
| flanking (over 60): deaths per 100, now died | 25.0 | 50.0 | new death metric |
| flanking (over 60): smoker died per 100, now smoker died | 16.7 | 41.7 | new death metric |
| radar cruiser inside: deaths per 100, now died | 18.8 | 28.1 | new death metric |
| radar cruiser inside: smoker died per 100, now smoker died | 3.1 | 12.5 | new death metric |
| Gearing: deaths per 100, now died | 35.0 | 45.0 | new death metric |
| Gearing: smoker died per 100, now smoker died | 10.0 | 20.0 | new death metric |
| flank-smoke-line ships: deaths per 100, now died | 23.1 | 32.7 | new death metric |
| flank-smoke-line ships: smoker died per 100, now smoker died | 5.8 | 15.4 | new death metric |
| laid 11-25 s after the enemy smoke: concealed damage | 12,296 | 10,922 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: deaths per 100, now caught | 18.6 | 20.9 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: deaths per 100, now died | 18.6 | 25.6 | new death metric |
| laid 11-25 s after the enemy smoke: smoker died per 100, now smoker caught | 7.0 | 9.3 | delay from the replay clock (different smokes in the row) |
| laid 11-25 s after the enemy smoke: smoker died per 100, now smoker died | 7.0 | 13.9 | new death metric |
| 6-9 km from the answered smoke: deaths per 100, now died | 19.6 | 29.4 | new death metric |
| 6-9 km from the answered smoke: smoker died per 100, now smoker died | 9.8 | 19.6 | new death metric |
| answered smoke within 30 degrees of straight ahead: deaths per 100, now died | 16.9 | 24.6 | new death metric |
| answered smoke within 30 degrees of straight ahead: smoker died per 100, now smoker died | 4.6 | 12.3 | new death metric |
| all counter-smokes: deaths per 100, now died | 15.0 | 24.8 | new death metric |
| all counter-smokes: smoker died per 100, now smoker died | 7.5 | 17.3 | new death metric |
| flanking minus head-on, deaths per 100, now caught | +10.0 (-13.1 to +35.0) | +10.0 (-15.4 to +41.1) | same list; interval now from diff_ci |
| flanking minus head-on, deaths per 100, now died | +10.0 (-13.1 to +35.0) | +26.0 (-5.0 to +63.3) | new death metric |

37 other compared numbers are unchanged (n, concealed damage and the caught rates wherever the row holds the same smokes).

---

## Items 5 to 7: getaway smokes (B2), long smokes (B3), map rows that quote a cap result (C4, C5)

Source: `x2-ships-maps/FINDINGS-X2.md`.


Batch `output/20261117-230933`, 1,547 smokes, 1,074 destroyer smokes (387 Top 6, 687 Rest). Destroyer smokes: 194 ships died (18.2 per 100) against 124 caught (11.55 per 100).

How to read this page:
- "died" = a covered ship (the smoker, or a ship inside or behind the smoke) died between activation and 20 s after the smoke dispersed; each dead ship is counted once. "caught" = the batch list of ships that died while the smoke concealed them (round 5's "deaths"). The 9 smokes of the single-replay game laid by the team with no replay are left out of every "died" rate.
- Cap results come from the cap timeline, on one fixed cap, up to 60 s after the smoke dispersed. "Contested cap" is the cap the batch ties the smoke to; "nearest cap" is the cap closest to the smoke centre. "We took" is counted over smokes where the cap was not already ours; "enemy took" over smokes where it was not already theirs.
- Intervals are 95%, from resampling whole clans. "Clear" = the interval excludes zero. Under 8 smokes = "too few", no rate; 8 to 14 = "small n". Everything here is association, not cause.
- "Round 5b" in the change tables = the round 5 number after the clock fix (round 5b did not redo these items).

### 5. B2. Getaway smokes (exhaust and battleship smoke), both death metrics, and the undetected share from the track

**Answer:** The round 5 reading stands on both metrics: the Italian cruisers' exhaust smoke goes with more losses, not fewer. The smoker died in 18.5 of every 100 smokes (caught: 16.1) against 8.2 (caught: 6.3) for cruisers with ordinary smoke. From the track, the smoker was undetected for 79.3% of the smoke's life (Italian cruisers), 71.3% (battleships) and 85.0% (ordinary cruiser smoke). Battleships look worse on "died" (17.6 per 100) than on "caught" (8.8), but no battleship gap is clear.

**Numbers (deaths):** per 100 smokes.

| Group | n | Clans | Ships died per 100 | Ships caught per 100 | Smoker died per 100 | Smoker caught per 100 |
|---|---|---|---|---|---|---|
| Napoli | 147 | 25 | 19.0 (13.1 to 27.0) | 16.3 (10.8 to 25.0) | 17.7 (11.9 to 25.0) | 15.0 (9.8 to 21.8) |
| Venezia | 21 | 3 | 28.6 (11.1 to 60.0) | 28.6 (11.1 to 60.0) | 23.8 (11.1 to 40.0) | 23.8 (11.1 to 40.0) |
| **Italian cruisers together** | 168 | 25 | 20.2 (14.6 to 27.6) | 17.9 (12.7 to 25.0) | 18.5 (13.6 to 25.2) | 16.1 (11.5 to 22.3) |
| **Battleships, listed separately** |  |  |  |  |  |  |
| C. Colombo (battleship) | 20 | 13 | 25.0 (9.1 to 42.1) | 10.0 (0.0 to 23.8) | 25.0 (10.0 to 41.2) | 10.0 (0.0 to 23.5) |
| Conte Verde (battleship) | 9 (small n) | 2 | 11.1 | 11.1 | 11.1 | 11.1 |
| **All battleships** | 34 | 16 | 17.6 (8.0 to 28.6) | 8.8 (0.0 to 16.7) | 17.6 (8.1 to 29.2) | 8.8 (0.0 to 16.7) |
| **Baselines** |  |  |  |  |  |  |
| Baseline: all smokes | 1547 | 30 | 16.8 (14.1 to 20.5) | 11.4 (9.6 to 13.9) | 12.7 (10.3 to 16.1) | 7.5 (5.8 to 9.7) |
| Baseline: all other smokes (not exhaust, not battleship) | 1330 | 30 | 16.4 (13.4 to 20.2) | 10.8 (9.0 to 13.5) | 11.8 (9.3 to 15.6) | 6.4 (4.6 to 8.7) |
| Baseline: cruiser smokers with ordinary smoke | 271 | 22 | 9.3 (7.0 to 12.5) | 7.4 (5.0 to 10.5) | 8.2 (6.1 to 11.4) | 6.3 (4.3 to 9.3) |
| Baseline: all cruiser smokers | 439 | 29 | 13.5 (11.0 to 16.8) | 11.4 (9.4 to 14.0) | 12.1 (9.9 to 15.1) | 10.0 (8.1 to 12.5) |
| Baseline: destroyer smokers | 1074 | 30 | 18.2 (14.7 to 22.5) | 11.5 (9.2 to 14.4) | 12.7 (9.9 to 16.7) | 6.4 (4.4 to 9.0) |

Differences with intervals:

| Contrast | Ships died per 100 | Ships caught per 100 | Smoker died per 100 | Smoker caught per 100 |
|---|---|---|---|---|
| Italian cruisers minus cruisers with ordinary smoke | +10.9 (+4.0 to +18.5), clear | +10.5 (+3.7 to +18.4), clear | +10.3 (+3.3 to +17.3), clear | +9.8 (+3.3 to +16.8), clear |
| Italian cruisers minus all other smokes | +3.9 (-3.3 to +12.9) | +7.1 (+1.3 to +15.2), clear | +6.6 (+0.0 to +14.5), clear | +9.7 (+4.0 to +16.9), clear |
| Battleships minus cruisers with ordinary smoke | +8.4 (-2.0 to +20.9) | +1.4 (-7.3 to +11.1) | +9.5 (-0.4 to +22.2) | +2.6 (-6.3 to +12.6) |
| Battleships minus all other smokes | +1.3 (-9.8 to +13.2) | -1.9 (-10.9 to +6.4) | +5.8 (-5.2 to +17.5) | +2.4 (-6.3 to +10.6) |
| Battleships minus Italian cruisers | -2.6 (-13.7 to +9.1) | -9.0 (-19.9 to +0.6) | -0.8 (-11.4 to +11.0) | -7.2 (-17.8 to +2.0) |

- Who died: in Italian cruiser smokes 31 of the 34 ships that died were the smoker (caught: 27 of 30). In battleship smokes all 6 were the smoker (caught: 3).
- "Died" finds 34 ships against 30 caught for the Italian cruisers, and 6 against 3 for battleships: the extra ones died inside the window (activation to 20 s after dispersal) without the batch listing them as caught in the smoke.
- Italian cruisers against all other smokes: the gap is clear on "caught" (+7.1 (+1.3 to +15.2), clear) but not on "died" for all ships (+3.9 (-3.3 to +12.9)); for the smoker alone it is +6.6 (+0.0 to +14.5), clear (the interval starts at zero: borderline).

**Numbers (undetected share, from the smoker's track):** the track has a "detected by the enemy" flag every 2 s. For each smoke: the share of the smoker's samples between activation and dispersal (or its death, if earlier) with the flag off. "Inside" = only the samples where the smoker's track position is inside the smoke. Means per group (interval), medians beside them.

| Group | Smokes with track data | Undetected, % of the smoke's life (track), mean | median | Undetected while inside the smoke (track), mean | median | Round 5 column 7: batch field, % of covered time, mean | Round 5 column 8: "whole life" figure, mean | Share of the smoke's life the smoker is inside it, % |
|---|---|---|---|---|---|---|---|---|
| Napoli | 147 | 79.8 (75.0 to 83.9) | 92.9 | 81.4 (76.6 to 85.2) | 96.3 | 81.4 (76.4 to 85.4) | 69.5 (63.0 to 74.1) | 94.0 |
| Venezia | 21 | 75.3 (52.3 to 89.3) | 89.7 | 77.9 (55.6 to 90.2) | 96.6 | 83.7 (70.3 to 91.1) | 72.3 (52.3 to 85.8) | 93.2 |
| **Italian cruisers together** | 168 | 79.3 (74.1 to 83.2) | 92.6 | 80.9 (75.9 to 84.8) | 96.3 | 81.7 (76.9 to 85.3) | 69.9 (63.2 to 74.6) | 93.9 |
| **Battleships, listed separately** |  |  |  |  |  |  |  |  |
| C. Colombo (battleship) | 20 | 66.1 (54.3 to 76.5) | 64.4 | 67.0 (53.9 to 79.5) | 64.1 | 64.7 (49.5 to 78.3) | 56.4 (44.3 to 68.2) | 96.1 |
| Conte Verde (battleship) | 9 (small n) | 77.1 | 79.3 | 82.7 | 84.6 | 80.8 | 64.2 | 91.8 |
| **All battleships** | 34 | 71.3 (60.2 to 78.5) | 75.0 | 73.3 (61.9 to 81.5) | 78.5 | 71.7 (59.3 to 80.5) | 61.8 (50.9 to 70.0) | 95.2 |
| **Baselines** |  |  |  |  |  |  |  |  |
| Baseline: all smokes | 1544 | 83.4 (81.0 to 85.0) | 92.3 | 84.5 (82.0 to 86.1) | 96.6 | 87.1 (84.9 to 88.7) | 47.6 (44.0 to 51.0) | 55.9 |
| Baseline: all other smokes (not exhaust, not battleship) | 1327 | 84.1 (81.9 to 85.8) | 92.3 | 85.2 (82.7 to 87.0) | 97.8 | 88.1 (86.1 to 89.6) | 44.1 (40.4 to 47.1) | 49.6 |
| Baseline: cruiser smokers with ordinary smoke | 271 | 85.0 (80.7 to 88.0) | 95.0 | 86.5 (82.6 to 89.0) | 95.2 | 90.1 (86.2 to 92.5) | 65.8 (60.3 to 71.2) | 74.2 |
| Baseline: all cruiser smokers | 439 | 82.8 (78.9 to 85.6) | 92.9 | 84.4 (81.1 to 86.8) | 95.8 | 86.9 (83.3 to 89.5) | 67.3 (62.9 to 71.6) | 81.7 |
| Baseline: destroyer smokers | 1071 | 84.0 (81.9 to 85.5) | 92.3 | 84.9 (82.7 to 86.8) | 100.0 | 87.6 (85.6 to 89.2) | 38.9 (36.6 to 41.5) | 44.1 |

| Contrast | Undetected % of the smoke's life (track) | Undetected % while inside (track) | Batch field (round 5 column 7) | Round 5 "whole life" figure (column 8) |
|---|---|---|---|---|
| Italian cruisers minus cruisers with ordinary smoke | -5.7 (-10.9 to -0.7), clear | -5.5 (-11.1 to -0.2), clear | -8.4 (-13.3 to -4.0), clear | +4.1 (-4.2 to +10.7) |
| Italian cruisers minus all other smokes | -4.9 (-9.7 to -0.4), clear | -4.3 (-9.4 to +0.3) | -6.4 (-11.5 to -2.4), clear | +25.8 (+18.1 to +31.3), clear |
| Battleships minus cruisers with ordinary smoke | -13.7 (-25.4 to -4.0), clear | -13.2 (-25.9 to -3.7), clear | -18.4 (-32.3 to -9.0), clear | -4.0 (-16.9 to +7.3) |
| Battleships minus all other smokes | -12.9 (-23.0 to -4.6), clear | -11.9 (-23.3 to -3.1), clear | -16.4 (-29.1 to -7.1), clear | +17.7 (+5.6 to +27.3), clear |
| Battleships minus Italian cruisers | -8.0 (-18.4 to +1.0) | -7.6 (-19.7 to +1.8) | -10.0 (-22.3 to +0.1) | -8.1 (-18.7 to +1.4) |

- How the track figure compares with round 5: round 5 gave 81.7% / 71.7% / 90.1% (Italian cruisers / battleships / ordinary cruiser smoke) on the batch field, and 69.9 / 61.8 / 65.8 on its own "whole life" figure. The track gives 79.3 / 71.3 / 85.0 for the whole life and 80.9 / 73.3 / 86.5 while inside.
- The track's whole-life figure sits close to the batch field and well above round 5's "whole life" figure. Round 5's figure counted only seconds that were both undetected and covered, so every second outside the smoke counted as detected. The track shows the smoker is mostly undetected outside the smoke as well.
- The order of the groups is the same on every reading: ordinary cruiser smoke highest, Italian cruisers a few points lower, battleships lowest. Italian cruisers minus ordinary cruiser smoke: -5.7 (-10.9 to -0.7), clear on the track (batch field: -8.4 (-13.3 to -4.0), clear). Battleships minus ordinary cruiser smoke: -13.7 (-25.4 to -4.0), clear. Battleships minus Italian cruisers: -8.0 (-18.4 to +1.0).
- Half of all smokes have the smoker undetected for the whole life of the smoke or nearly so (median 92.3%); the means are pulled down by a minority of smokes where the smoker stays detected. Smoker undetected for over 95% of the smoke's life: Italian cruisers 44.6%, battleships 17.6%, ordinary cruiser smoke 49.8%.
- Samples with no flag were left out: 207 of 73,113 samples. That drops 3 smokes entirely (no sample with a flag; 2 of them in the single-replay game), all destroyer smokes; 1 more smoke lost part of its samples. No Italian cruiser or battleship smoke is dropped. 3 smokes have no sample inside the smoke and are left out of the "inside" columns only.

**Top 6 or Shared:** Shared, and mostly a Rest tool: 153 of the 168 Italian cruiser smokes are by Rest clans. Top 6 (n=15, 5 clans) against Rest, smoker died per 100: 33.3 vs 17.0; +16.3 (-2.5 to +49.6); smoker caught: 33.3 vs 14.4; +19.0 (+1.4 to +53.2), clear. The gap that round 5 called clear is clear only on "caught", and it rests on 5 deaths. Battleships Top 6 n=10 (small n, 8 are H-SR's Conte Verde): smoker died 10.0 vs 20.8; -10.8 (-31.0 to +2.0); caught 10.0 vs 8.3; +1.7 (-16.0 to +10.0). Undetected share of the smoke's life: Italian cruisers 87.3 vs 78.5; +8.8 (-5.5 to +19.4); battleships 75.6 vs 69.4; +6.2 (-16.8 to +19.7).

**Clans:**
- Napoli: Top 6: VRTUS 6, RESIN 3, BONKZ 3, HTDOG 2, H-SR 1 | Rest: KITED 18, MACHX 16, BTLST 14, 5D 14, HFANS 11, UYSC 10, REEEE 8, MZY 6, KSE 5, KM 4, MANBA 4, INCA 4, BONKY 4, PFANS 3, MACH 3, NGA 3, PN 2, SCCC2 1, KSC 1, -BN- 1
- Venezia: Top 6: none | Rest: KITED 9, NGA 7, 5D 5
- C. Colombo (battleship): Top 6: VRTUS 1, RESIN 1 | Rest: BTLST 3, KITED 3, -BN- 3, EPOXY 2, PN 1, UYSC 1, BONKY 1, INCA 1, NGA 1, MZY 1, HFANS 1
- Conte Verde (battleship): Top 6: H-SR 8 | Rest: EPOXY 1
- All battleships: Top 6: H-SR 8, VRTUS 1, RESIN 1 | Rest: EPOXY 3, BTLST 3, KITED 3, -BN- 3, HFANS 3, MACHX 2, PN 1, UYSC 1, BONKY 1, INCA 1, NGA 1, MZY 1, 5D 1

**Could not be done / proxy:** "Inside the smoke" uses the smoke's full footprint for its whole life (the laid path and radius), so early samples can count as inside before that part of the smoke existed. Samples are 2 s apart. The detected flag says the enemy could see the ship, not which enemy or how.

**Verdict:** Keep.

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Italian cruisers together: ships lost per 100 smokes | 17.9 (12.7 to 25.0) | caught 17.9 (12.7 to 25.0); died 20.2 (14.6 to 27.6) | caught unchanged; died is the new death metric |
| Italian cruisers together: smoker lost per 100 smokes | 16.1 (11.4 to 22.5) | caught 16.1 (11.5 to 22.3); died 18.5 (13.6 to 25.2) | caught unchanged; died is the new death metric |
| All battleships: ships lost per 100 smokes | 8.8 (0.0 to 17.6) | caught 8.8 (0.0 to 16.7); died 17.6 (8.0 to 28.6) | caught unchanged; died is the new death metric |
| All battleships: smoker lost per 100 smokes | 8.8 (0.0 to 16.7) | caught 8.8 (0.0 to 16.7); died 17.6 (8.1 to 29.2) | caught unchanged; died is the new death metric |
| Napoli: ships lost per 100 smokes | 16.3 (10.6 to 24.1) | caught 16.3 (10.8 to 25.0); died 19.0 (13.1 to 27.0) | caught unchanged; died is the new death metric |
| Napoli: smoker lost per 100 smokes | 15.0 (9.9 to 22.3) | caught 15.0 (9.8 to 21.8); died 17.7 (11.9 to 25.0) | caught unchanged; died is the new death metric |
| Venezia: ships lost per 100 smokes | 28.6 (11.1 to 60.0) | caught 28.6 (11.1 to 60.0); died 28.6 (11.1 to 60.0) | caught unchanged; died is the new death metric |
| Venezia: smoker lost per 100 smokes | 23.8 (11.1 to 40.0) | caught 23.8 (11.1 to 40.0); died 23.8 (11.1 to 40.0) | caught unchanged; died is the new death metric |
| C. Colombo (battleship): ships lost per 100 smokes | 10.0 (0.0 to 23.8) | caught 10.0 (0.0 to 23.8); died 25.0 (9.1 to 42.1) | caught unchanged; died is the new death metric |
| C. Colombo (battleship): smoker lost per 100 smokes | 10.0 (0.0 to 23.8) | caught 10.0 (0.0 to 23.5); died 25.0 (10.0 to 41.2) | caught unchanged; died is the new death metric |
| Conte Verde (battleship): ships lost per 100 smokes | 11.1 | caught 11.1; died 11.1 | caught unchanged; died is the new death metric |
| Conte Verde (battleship): smoker lost per 100 smokes | 11.1 | caught 11.1; died 11.1 | caught unchanged; died is the new death metric |
| Baseline: all smokes: ships lost per 100 smokes | 11.4 (9.4 to 13.9) | caught 11.4 (9.6 to 13.9); died 16.8 (14.1 to 20.5) | caught unchanged; died is the new death metric |
| Baseline: all smokes: smoker lost per 100 smokes | 7.5 (5.9 to 9.8) | caught 7.5 (5.8 to 9.7); died 12.7 (10.3 to 16.1) | caught unchanged; died is the new death metric |
| Baseline: all other smokes (not exhaust, not battleship): ships lost per 100 smokes | 10.8 (8.8 to 13.5) | caught 10.8 (9.0 to 13.5); died 16.4 (13.4 to 20.2) | caught unchanged; died is the new death metric |
| Baseline: all other smokes (not exhaust, not battleship): smoker lost per 100 smokes | 6.4 (4.6 to 8.9) | caught 6.4 (4.6 to 8.7); died 11.8 (9.3 to 15.6) | caught unchanged; died is the new death metric |
| Baseline: cruiser smokers with ordinary smoke: ships lost per 100 smokes | 7.4 (5.2 to 10.1) | caught 7.4 (5.0 to 10.5); died 9.3 (7.0 to 12.5) | caught unchanged; died is the new death metric |
| Baseline: cruiser smokers with ordinary smoke: smoker lost per 100 smokes | 6.3 (4.2 to 9.3) | caught 6.3 (4.3 to 9.3); died 8.2 (6.1 to 11.4) | caught unchanged; died is the new death metric |
| Baseline: all cruiser smokers: ships lost per 100 smokes | 11.4 (9.4 to 14.0) | caught 11.4 (9.4 to 14.0); died 13.5 (11.0 to 16.8) | caught unchanged; died is the new death metric |
| Baseline: all cruiser smokers: smoker lost per 100 smokes | 10.0 (8.2 to 12.4) | caught 10.0 (8.1 to 12.5); died 12.1 (9.9 to 15.1) | caught unchanged; died is the new death metric |
| Baseline: destroyer smokers: ships lost per 100 smokes | 11.5 (9.2 to 14.5) | caught 11.5 (9.2 to 14.4); died 18.2 (14.7 to 22.5) | caught unchanged; died is the new death metric |
| Baseline: destroyer smokers: smoker lost per 100 smokes | 6.4 (4.3 to 9.4) | caught 6.4 (4.4 to 9.0); died 12.7 (9.9 to 16.7) | caught unchanged; died is the new death metric |
| Italian cruisers minus cruisers with ordinary smoke: ships lost per 100 | +10.5 (+3.4 to +18.8), clear | caught +10.5 (+3.7 to +18.4), clear; died +10.9 (+4.0 to +18.5), clear | new death metric (caught interval differs only by resampling) |
| Italian cruisers minus cruisers with ordinary smoke: smoker lost per 100 | +9.8 (+3.3 to +17.3), clear | caught +9.8 (+3.3 to +16.8), clear; died +10.3 (+3.3 to +17.3), clear | new death metric (caught interval differs only by resampling) |
| Italian cruisers minus all other smokes: ships lost per 100 | +7.1 (+0.9 to +15.4), clear | caught +7.1 (+1.3 to +15.2), clear; died +3.9 (-3.3 to +12.9) | new death metric (caught interval differs only by resampling) |
| Italian cruisers minus all other smokes: smoker lost per 100 | +9.7 (+4.2 to +17.1), clear | caught +9.7 (+4.0 to +16.9), clear; died +6.6 (+0.0 to +14.5), clear | new death metric (caught interval differs only by resampling) |
| Battleships minus cruisers with ordinary smoke: ships lost per 100 | +1.4 (-7.2 to +10.7) | caught +1.4 (-7.3 to +11.1); died +8.4 (-2.0 to +20.9) | new death metric (caught interval differs only by resampling) |
| Battleships minus cruisers with ordinary smoke: smoker lost per 100 | +2.6 (-6.3 to +11.4) | caught +2.6 (-6.3 to +12.6); died +9.5 (-0.4 to +22.2) | new death metric (caught interval differs only by resampling) |
| Battleships minus all other smokes: ships lost per 100 | -1.9 (-11.1 to +6.9) | caught -1.9 (-10.9 to +6.4); died +1.3 (-9.8 to +13.2) | new death metric (caught interval differs only by resampling) |
| Battleships minus all other smokes: smoker lost per 100 | +2.4 (-5.9 to +10.5) | caught +2.4 (-6.3 to +10.6); died +5.8 (-5.2 to +17.5) | new death metric (caught interval differs only by resampling) |
| Battleships minus Italian cruisers: ships lost per 100 | -9.0 (-19.7 to +1.4) | caught -9.0 (-19.9 to +0.6); died -2.6 (-13.7 to +9.1) | new death metric (caught interval differs only by resampling) |
| Battleships minus Italian cruisers: smoker lost per 100 | -7.2 (-18.0 to +2.6) | caught -7.2 (-17.8 to +2.0); died -0.8 (-11.4 to +11.0) | new death metric (caught interval differs only by resampling) |
| Italian cruisers together: smoker undetected, % of time under the smoke | 81.7 (76.6 to 85.6) | batch field 81.7 (76.9 to 85.3); track, while inside 80.9 (75.9 to 84.8) | batch field unchanged; track figure is new |
| Italian cruisers together: smoker undetected, % of the smoke's whole life | 69.9 (63.2 to 74.4) | track 79.3 (74.1 to 83.2) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| All battleships: smoker undetected, % of time under the smoke | 71.7 (58.5 to 80.2) | batch field 71.7 (59.3 to 80.5); track, while inside 73.3 (61.9 to 81.5) | batch field unchanged; track figure is new |
| All battleships: smoker undetected, % of the smoke's whole life | 61.8 (50.3 to 69.6) | track 71.3 (60.2 to 78.5) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| Baseline: cruiser smokers with ordinary smoke: smoker undetected, % of time under the smoke | 90.1 (86.6 to 92.5) | batch field 90.1 (86.2 to 92.5); track, while inside 86.5 (82.6 to 89.0) | batch field unchanged; track figure is new |
| Baseline: cruiser smokers with ordinary smoke: smoker undetected, % of the smoke's whole life | 65.8 (60.2 to 71.5) | track 85.0 (80.7 to 88.0) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| Baseline: all smokes: smoker undetected, % of time under the smoke | 87.1 (85.1 to 88.6) | batch field 87.1 (84.9 to 88.7); track, while inside 84.5 (82.0 to 86.1) | batch field unchanged; track figure is new |
| Baseline: all smokes: smoker undetected, % of the smoke's whole life | 47.6 (44.2 to 51.1) | track 83.4 (81.0 to 85.0) | track detected flag replaces the round 5 computed figure (which counted time outside the smoke as detected) |
| Italian cruisers minus cruisers with ordinary smoke: undetected % | -8.4 (-13.5 to -3.8), clear (batch field) | track, whole life -5.7 (-10.9 to -0.7), clear; track, inside -5.5 (-11.1 to -0.2), clear | track detected flag |
| Italian cruisers minus all other smokes: undetected % | -6.4 (-11.4 to -2.2), clear (batch field) | track, whole life -4.9 (-9.7 to -0.4), clear; track, inside -4.3 (-9.4 to +0.3) | track detected flag |
| Battleships minus cruisers with ordinary smoke: undetected % | -18.4 (-32.9 to -9.3), clear (batch field) | track, whole life -13.7 (-25.4 to -4.0), clear; track, inside -13.2 (-25.9 to -3.7), clear | track detected flag |
| Battleships minus all other smokes: undetected % | -16.4 (-30.2 to -7.2), clear (batch field) | track, whole life -12.9 (-23.0 to -4.6), clear; track, inside -11.9 (-23.3 to -3.1), clear | track detected flag |
| Battleships minus Italian cruisers: undetected % | -10.0 (-22.6 to -0.9), clear (batch field) | track, whole life -8.0 (-18.4 to +1.0); track, inside -7.6 (-19.7 to +1.8) | track detected flag |
| Italian cruisers, Top 6 minus Rest, smoker lost per 100 | 33.3 vs 14.4; +19.0 (+1.6 to +52.5), clear | caught 33.3 vs 14.4; +19.0 (+1.4 to +53.2), clear; died 33.3 vs 17.0; +16.3 (-2.5 to +49.6) | new death metric |
| Battleships, Top 6 minus Rest, ships lost per 100 | 10.0 vs 8.3, no clear gap | caught 10.0 vs 8.3; +1.7 (-16.0 to +10.0); died 10.0 vs 20.8; -10.8 (-31.6 to +2.0) | new death metric |
| Who died in Italian cruiser smokes | 27 of 30 the smoker | caught 27 of 30; died 31 of 34 | new death metric |

---

### 6. B3. Long smokes (Somers, Gearing, Harugumo, Delny): death rates and the Top 6 vs Rest gap, both metrics

**Answer:** The Top 6 lose fewer ships in their long smokes on both metrics: died 15.2 vs 25.2; -10.0 (-19.1 to -1.6), clear; caught 8.0 vs 18.8; -10.8 (-17.8 to -6.0), clear. Split by result, there is no gap in games won on either metric (died 10.7 vs 12.3; -1.6 (-10.0 to +7.1)). In games lost the "died" gap is not clear (28.3 vs 34.0; -5.7 (-25.4 to +6.5)), but the "caught" gap stays clear (11.7 vs 26.0; -14.4 (-27.7 to -5.0), clear). So round 3's "the gap goes away once wins and losses are separated" holds on "died" and only in part on "caught".

**Numbers:** per 100 smokes; sheltering cruisers per 100 sheltering cruisers (cruisers inside or behind the smoke, the smoker not counted).

| Ship | n | Clans | Ships died per 100 | Ships caught per 100 | Smoker died per 100 | Smoker caught per 100 | Sheltering cruisers died, per 100 of them | Sheltering cruisers caught, per 100 of them |
|---|---|---|---|---|---|---|---|---|
| Somers | 260 | 18 | 18.8 (12.3 to 25.0) | 10.4 (7.0 to 13.4) | 10.4 (6.1 to 15.2) | 3.8 (1.9 to 6.5) | 9.4 (4.9 to 13.7) [22 of 234] | 7.3 (4.2 to 10.1) [17 of 234] |
| Gearing | 180 | 16 | 25.4 (17.7 to 35.2) | 17.8 (11.8 to 26.8) | 16.8 (9.2 to 31.0) | 8.3 (2.2 to 19.8) | 8.2 (3.8 to 11.8) [12 of 146] | 9.4 (5.0 to 13.8) [14 of 149] |
| Harugumo | 100 | 15 | 22.0 (15.3 to 37.7) | 21.0 (12.9 to 34.4) | 12.0 (7.1 to 22.1) | 10.0 (5.0 to 18.8) | 9.4 (5.0 to 16.4) [8 of 85] | 9.4 (4.9 to 17.6) [8 of 85] |
| Delny (2 clans, 18 of 22 by H-SR) | 22 | 2 | 4.5 | 0.0 | 4.5 | 0.0 | 0.0 [0 of 20] | 0.0 [0 of 20] |
| **All four** | 562 | 27 | 20.9 (16.4 to 26.7) | 14.2 (10.8 to 18.6) | 12.4 (8.7 to 17.3) | 6.2 (3.8 to 10.2) | 8.7 (6.3 to 11.7) [42 of 485] | 8.0 (5.8 to 10.9) [39 of 488] |
| For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze) | 462 | 28 | 14.1 (10.1 to 20.0) | 7.4 (5.0 to 10.6) | 12.1 (8.3 to 17.1) | 5.6 (3.1 to 9.1) | 9.2 (3.8 to 16.7) [8 of 87] | 8.0 (2.6 to 15.2) [7 of 87] |
| For comparison: all destroyer smokes | 1074 | 30 | 18.2 (14.8 to 22.6) | 11.5 (9.2 to 14.6) | 12.7 (10.1 to 17.2) | 6.4 (4.6 to 9.5) | 8.7 (6.5 to 11.5) [51 of 584] | 8.2 (6.1 to 10.8) [48 of 587] |

Long-smoke ships minus cap sitters: ships died +6.8 (+1.0 to +12.4), clear; ships caught +6.9 (+3.1 to +11.1), clear; smoker died +0.3 (-4.9 to +5.5); smoker caught +0.6 (-2.7 to +4.7); sheltering cruisers died -0.5 (-8.6 to +6.3); caught -0.1 (-6.8 to +6.2).
- The extra losses in long smokes are not the smoker and not a higher rate per sheltering cruiser: long smokes simply shelter far more cruisers (485 over 555 smokes against 87 over 462 for cap sitters).

Top 6 against Rest (Top 6 vs Rest; gap with interval):

| Ship | n Top 6 / Rest | Ships died per 100 | Ships caught per 100 | Smoker died per 100 | Smoker caught per 100 | Sheltering cruisers died per 100 | Sheltering cruisers caught per 100 |
|---|---|---|---|---|---|---|---|
| Somers | 90 / 170 | 17.8 vs 19.4; -1.6 (-17.9 to +12.5) | 7.8 vs 11.8; -4.0 (-11.4 to +2.1) | 10.0 vs 10.6; -0.6 (-11.5 to +10.2) | 2.2 vs 4.7; -2.5 (-6.5 to +2.0) | 8.2 vs 10.1; -1.8 (-12.3 to +6.6) | 5.9 vs 8.1; -2.2 (-9.5 to +3.4) |
| Gearing | 74 / 106 | 16.2 vs 32.3; -16.1 (-29.5 to -3.4), clear | 9.5 vs 23.6; -14.1 (-26.0 to -4.6), clear | 8.1 vs 23.2; -15.1 (-31.1 to +2.4) | 1.4 vs 13.2; -11.9 (-30.0 to -0.1), clear | 6.8 vs 9.6; -2.7 (-9.8 to +6.8) | 6.8 vs 11.8; -5.0 (-12.9 to +3.5) |
| Harugumo | 55 / 45 | 12.7 vs 33.3; -20.6 (-45.6 to -5.6), clear | 9.1 vs 35.6; -26.5 (-43.3 to -13.6), clear | 5.5 vs 20.0; -14.5 (-29.2 to -4.5), clear | 3.6 vs 17.8; -14.1 (-25.8 to -5.2), clear | 6.4 vs 13.2; -6.8 (-16.8 to +6.5) | 4.3 vs 15.8; -11.5 (-22.5 to -2.3), clear |
| Delny | 18 / 4 (too few) | 5.6 vs too few | 0.0 vs too few | 5.6 vs too few | 0.0 vs too few | 0.0 vs too few | 0.0 vs too few |
| All four | 237 / 325 | 15.2 vs 25.2; -10.0 (-19.1 to -1.6), clear | 8.0 vs 18.8; -10.8 (-17.8 to -6.0), clear | 8.0 vs 15.7; -7.7 (-16.7 to -0.8), clear | 2.1 vs 9.2; -7.1 (-13.2 to -3.1), clear | 6.7 vs 10.4; -3.7 (-8.5 to +1.6) | 5.3 vs 10.3; -4.9 (-9.0 to -0.8), clear |
| For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze) | 135 / 327 | 9.6 vs 15.9; -6.3 (-14.5 to +1.0) | 5.9 vs 8.0; -2.0 (-7.7 to +2.2) | 7.4 vs 14.1; -6.7 (-15.2 to +1.0) | 3.7 vs 6.4; -2.7 (-7.7 to +1.9) | - | - |
| For comparison: all destroyer smokes | 387 / 687 | 13.4 vs 20.9; -7.4 (-14.7 to -1.2), clear | 7.5 vs 13.8; -6.3 (-11.0 to -2.4), clear | 8.0 vs 15.4; -7.4 (-14.3 to -2.4), clear | 2.8 vs 8.4; -5.6 (-10.2 to -2.4), clear | - | - |

The same, with games won and games lost kept apart:

| Ship | Result | n Top 6 / Rest | Ships died per 100 | Ships caught per 100 | Smoker died per 100 | Smoker caught per 100 | Share of the smokes laid in games won, Top 6 vs Rest |
|---|---|---|---|---|---|---|---|
| Somers | games won | 60 / 79 | 10.0 vs 10.1; -0.1 (-10.6 to +11.6) | 5.0 vs 6.3; -1.3 (-6.9 to +3.8) | 5.0 vs 3.8; +1.2 (-5.8 to +9.4) | 1.7 vs 1.3; +0.4 (-3.2 to +3.8) | 67% vs 46% |
| Somers | games lost | 30 / 91 | 33.3 vs 27.5; +5.9 (-28.7 to +21.5) | 13.3 vs 16.5; -3.2 (-17.5 to +6.0) | 20.0 vs 16.5; +3.5 (-16.7 to +12.4) | 3.3 vs 7.7; -4.4 (-10.8 to +2.6) |  |
| Gearing | games won | 60 / 37 | 11.7 vs 23.5; -11.9 (-28.8 to +10.4) | 8.3 vs 16.2; -7.9 (-26.5 to +6.3) | 5.0 vs 14.7; -9.7 (-27.1 to +7.1) | 1.7 vs 8.1; -6.4 (-29.6 to +5.3) | 81% vs 35% |
| Gearing | games lost | 14 (small n) / 69 | 35.7 vs 36.9; -1.2 (-29.3 to +109.7) | 14.3 vs 27.5; -13.3 (-36.1 to +67.6) | 21.4 vs 27.7; -6.3 (-25.0 to +24.3) | 0.0 vs 15.9; -15.9 (-31.8 to -4.8), clear |  |
| Harugumo | games won | 39 / 13 (small n) | 12.8 vs 0.0; +12.8 (+11.1 to +25.0), clear | 10.3 vs 0.0; +10.3 (+5.6 to +25.0), clear | 7.7 vs 0.0; +7.7 (+5.6 to +25.0), clear | 5.1 vs 0.0; +5.1 (+0.0 to +25.0) | 71% vs 29% |
| Harugumo | games lost | 16 / 32 | 12.5 vs 46.9; -34.4 (-65.3 to -13.7), clear | 6.2 vs 50.0; -43.8 (-72.2 to -23.6), clear | 0.0 vs 28.1; -28.1 (-52.4 to -14.6), clear | 0.0 vs 25.0; -25.0 (-45.0 to -13.2), clear |  |
| Delny | games won | 18 / 4 (too few) | 5.6 vs too few | 0.0 vs too few | 5.6 vs too few | 0.0 vs too few | 100% vs 100% |
| Delny | games lost | 0 (too few) / 0 (too few) | too few vs too few | too few vs too few | too few vs too few | too few vs too few |  |
| All four | games won | 177 / 133 | 10.7 vs 12.3; -1.6 (-10.0 to +7.1) | 6.8 vs 8.3; -1.5 (-7.1 to +4.3) | 5.6 vs 6.2; -0.5 (-6.8 to +5.7) | 2.3 vs 3.0; -0.7 (-6.1 to +2.5) | 75% vs 41% |
| All four | games lost | 60 / 192 | 28.3 vs 34.0; -5.7 (-25.4 to +6.5) | 11.7 vs 26.0; -14.4 (-27.7 to -5.0), clear | 15.0 vs 22.3; -7.3 (-18.6 to +2.2) | 1.7 vs 13.5; -11.9 (-19.3 to -6.2), clear |  |
| For comparison: all destroyer smokes | games won | 285 / 313 | 7.7 vs 8.4; -0.7 (-5.6 to +3.5) | 4.6 vs 5.1; -0.6 (-3.7 to +2.1) | 4.2 vs 5.8; -1.6 (-5.7 to +1.1) | 1.4 vs 2.6; -1.2 (-3.7 to +0.7) | 74% vs 46% |
| For comparison: all destroyer smokes | games lost | 102 / 374 | 29.4 vs 31.4; -1.9 (-14.8 to +8.3) | 15.7 vs 21.1; -5.4 (-12.7 to +1.8) | 18.6 vs 23.5; -4.9 (-15.1 to +4.5) | 6.9 vs 13.4; -6.5 (-14.3 to +0.7) |  |

- Winning or losing moves the death rate far more than the group does. Four ships together, games won minus games lost: Top 6 died -17.6 (-28.3 to -0.1), clear, caught -4.9 (-13.4 to +8.1); Rest died -21.7 (-30.9 to -12.6), clear, caught -17.8 (-24.1 to -11.2), clear.
- The Top 6 lay 75% of their long smokes in games they won, the Rest 41%. That mix makes most of the overall gap.
- What is left after the split sits in games lost and mostly in the Harugumo: died 12.5 vs 46.9; -34.4 (-65.3 to -13.7), clear; caught 6.2 vs 50.0; -43.8 (-72.2 to -23.6), clear (Top 6 n 16, Rest n 32). In games won the Rest Harugumo lost nothing in 13 smokes (small n).
- In games lost the Rest smoker is caught far more often than the Top 6 smoker (four ships: 1.7 vs 13.5; -11.9 (-19.3 to -6.2), clear), while "died" is closer (15.0 vs 22.3; -7.3 (-18.6 to +2.2)): most Top 6 smokers that died in lost games are not on the batch's list of ships caught in the smoke.

**Top 6 or Shared:** Top 6 gap on the four together, clear on both metrics (died -10.0 (-19.1 to -1.6), clear; caught -10.8 (-17.8 to -6.0), clear), led by the Harugumo (died 12.7 vs 33.3; -20.6 (-45.6 to -5.6), clear; caught 9.1 vs 35.6; -26.5 (-43.3 to -13.6), clear) and the Gearing (died 16.2 vs 32.3; -16.1 (-29.5 to -3.4), clear). Somers shows no gap (died 17.8 vs 19.4; -1.6 (-17.9 to +12.5)). The gap is mostly a won-or-lost effect: none in games won; in games lost clear on "caught" only.

**Clans:**
- Somers: Top 6: RESIN 38, H-SR 33, BONKZ 12, VRTUS 7 | Rest: HFANS 28, REEEE 25, MZY 22, EPOXY 18, MACHX 17, BONKY 14, -BN- 12, NGA 11, PFANS 8, PN 5, UYSC 5, KITED 3, RSR 1, INCA 1
- Gearing: Top 6: BONKZ 37, KITE 23, VRTUS 10, HTDOG 4 | Rest: KSC 29, -BN- 18, BTLST 11, 5D 9, OGF 9, RSR 9, INCA 7, HFANS 5, RMN 3, EPOXY 3, KM 2, UYSC 1
- Harugumo: Top 6: RESIN 22, H-SR 20, BONKZ 7, HTDOG 6 | Rest: EPOXY 14, -BN- 6, PFANS 4, BONKY 4, PN 4, KM 3, SCCC2 3, REEEE 2, KITED 2, MZY 2, RSR 1
- Delny: Top 6: H-SR 18 | Rest: MZY 4

**Could not be done / proxy:** Delny has 4 Rest smokes and 0 smokes in a lost game, so it has no Top 6 vs Rest comparison and no win/loss split. Within games lost the Top 6 have 60 long smokes (Gearing 14, Harugumo 16), and the Rest Harugumo has 13 in games won: the per-ship splits are thin and their intervals are wide.

**Verdict:** Keep (death rates). The Top 6 vs Rest death gap: Keep as "mostly explained by winning", not as a long-smoke skill.

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Somers: ships lost per 100 smokes | 10.4 (7.4 to 13.4) | caught 10.4 (7.0 to 13.4); died 18.8 (12.3 to 25.0) | caught unchanged; died is the new death metric |
| Gearing: ships lost per 100 smokes | 17.8 (11.2 to 26.9) | caught 17.8 (11.8 to 26.8); died 25.4 (17.7 to 35.2) | caught unchanged; died is the new death metric |
| Harugumo: ships lost per 100 smokes | 21.0 (13.0 to 36.5) | caught 21.0 (12.9 to 34.4); died 22.0 (15.3 to 37.7) | caught unchanged; died is the new death metric |
| Delny: ships lost per 100 smokes | 0.0 | caught 0.0; died 4.5 | caught unchanged; died is the new death metric |
| All four: ships lost per 100 smokes | 14.2 (11.0 to 18.6) | caught 14.2 (10.8 to 18.6); died 20.9 (16.4 to 26.7) | caught unchanged; died is the new death metric |
| For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze): ships lost per 100 smokes | 7.4 (5.2 to 10.4) | caught 7.4 (5.0 to 10.6); died 14.1 (10.1 to 20.0) | caught unchanged; died is the new death metric |
| For comparison: all destroyer smokes: ships lost per 100 smokes | 11.5 (9.3 to 14.8) | caught 11.5 (9.2 to 14.6); died 18.2 (14.8 to 22.6) | caught unchanged; died is the new death metric |
| Long-smoke ships minus cap sitters, ships lost per 100 | +6.9 (+3.1 to +11.3), clear | caught +6.9 (+3.1 to +11.1), clear; died +6.8 (+1.0 to +12.4), clear | new death metric |
| Somers: Top 6 vs Rest, ships lost per 100 | 7.8 vs 11.8; -4.0 (-10.9 to +2.3) | caught 7.8 vs 11.8; -4.0 (-11.4 to +2.1); died 17.8 vs 19.4; -1.6 (-17.9 to +12.5) | new death metric |
| Gearing: Top 6 vs Rest, ships lost per 100 | 9.5 vs 23.6; -14.1 (-27.7 to -5.3) | caught 9.5 vs 23.6; -14.1 (-26.0 to -4.6), clear; died 16.2 vs 32.3; -16.1 (-29.5 to -3.4), clear | new death metric |
| Harugumo: Top 6 vs Rest, ships lost per 100 | 9.1 vs 35.6; -26.5 (-42.4 to -12.3) | caught 9.1 vs 35.6; -26.5 (-43.3 to -13.6), clear; died 12.7 vs 33.3; -20.6 (-45.6 to -5.6), clear | new death metric |
| Delny: Top 6 vs Rest, ships lost per 100 | 0.0 vs too few | caught 0.0 vs too few; died 5.6 vs too few | new death metric |
| All four: Top 6 vs Rest, ships lost per 100 | 8.0 vs 18.8; -10.8 (-17.0 to -5.8) | caught 8.0 vs 18.8; -10.8 (-17.8 to -6.0), clear; died 15.2 vs 25.2; -10.0 (-19.1 to -1.6), clear | new death metric |
| For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze): Top 6 vs Rest, ships lost per 100 | 5.9 vs 8.0; -2.0 (-7.5 to +2.2) | caught 5.9 vs 8.0; -2.0 (-7.7 to +2.2); died 9.6 vs 15.9; -6.3 (-14.5 to +1.0) | new death metric |
| For comparison: all destroyer smokes: Top 6 vs Rest, ships lost per 100 | 7.5 vs 13.8; -6.3 (-11.1 to -2.2) | caught 7.5 vs 13.8; -6.3 (-11.0 to -2.4), clear; died 13.4 vs 20.9; -7.4 (-14.7 to -1.2), clear | new death metric |
| Top 6 vs Rest gap once games won and lost are separated (four ships) | round 5 text: "round 3 showed this gap goes away" (no number) | games won: died 10.7 vs 12.3; -1.6 (-10.0 to +7.1); caught 6.8 vs 8.3; -1.5 (-7.1 to +4.3). Games lost: died 28.3 vs 34.0; -5.7 (-25.4 to +6.5); caught 11.7 vs 26.0; -14.4 (-27.7 to -5.0), clear | new: both metrics split by result |
| Smoker and sheltering-cruiser splits for the long ships | not given in round 5 | four ships: smoker died 12.4 (8.7 to 17.3), caught 6.2 (3.8 to 10.2); cruisers died 8.7 (6.3 to 11.7), caught 8.0 (5.8 to 10.9) per 100 sheltering cruisers | new |

---

### 7. C4 and C5 rows that quote a cap result, redone on the cap timeline

Round 5 took these cap results from cap-owner snapshots (recorded only at smoke moments) or from the batch `cap_won` field. Here every one comes from the cap timeline, on one fixed cap, up to 60 s after the smoke dispersed. "Enemy was taking it" = the timeline shows the enemy as the capturing side of that cap at some time while the smoke stood.

### 7a. High-paying cells (C4: Sleeping Giant G1, Hotspot G10+H10, Sea of Fortune F9+G9; C5: Loop F8 and F10)

**Answer:** The round 5 statement stands: these cells pay well in damage, and the cap is not taken more often after smokes there than elsewhere on the map. On the timeline "we took the cap" is 6 of 21 (29%) at G1 (round 5: 19% of 21), 14 of 35 (40%) at Hotspot G10+H10 (34% of 35) and 2 of 8 (25%, small n) at Sea of Fortune F9+G9 (25% of 8). One new thing: at G1 the enemy took cap A during or just after 7 of 13 (54%, small n) of the smokes, against 19% elsewhere on the map, a clear gap.

**Numbers (destroyer smokes in the cell, team-normalized grid; concealed damage is unchanged from round 5):**

| Cell | n (Top 6 / Rest) | Clans | Concealed damage per smoke (round 5b) | Rest of the map | Gap interval | Nearest cap (normalized letter) | Contested cap is the nearest cap |
|---|---|---|---|---|---|---|---|
| Sleeping Giant G1 | 21 (12 / 9) | 10 | 24,101 (24,101) | 10,709 | +8,134 to +21,004 | A 21 | 21 of 21 |
| Hotspot G10+H10 | 40 (13 / 27) | 18 | 16,970 (16,970) | 11,379 | +437 to +11,146 | D 40 | 40 of 40 |
| Sea of Fortune F9+G9 | 10 (small n) (4 / 6) | 6 | 24,597 (24,597) | 10,348 | +951 to +33,723 | D 10 | 10 of 10 |
| Loop F8 | 15 (7 / 8) | 9 | 18,318 (18,318) | 6,825 | -4,443 to +23,609 | B 11, C 4 | 15 of 15 |
| Loop F10 | 9 (small n) (2 / 7) | 6 | 20,728 (20,728) | 7,181 | -1,094 to +29,325 | C 9 | 9 of 9 |

Cap results. In all five cells the contested cap and the nearest cap are the same cap for every smoke, so the two columns agree inside the cell; they differ for the rest of the map.

| Smokes | n | Contested cap: ours / neutral / theirs at activation | We took it | Enemy took it | Nearest cap: ours / neutral / theirs | We took it | Enemy took it |
|---|---|---|---|---|---|---|---|
| Sleeping Giant G1 | 21 | 0 / 13 / 8 | 6 of 21 (29%) | 7 of 13 (54%, small n) | 0 / 13 / 8 | 6 of 21 (29%) | 7 of 13 (54%, small n) |
| rest of Sleeping Giant | 217 | 78 / 47 / 92 | 35 of 139 (25%) | 23 of 125 (18%) | 128 / 39 / 50 | 29 of 89 (33%) | 31 of 167 (19%) |
| cell minus rest of the map |  |  | +3.4 (-15.0 to +30.2) | +35.4 (+8.4 to +58.4), clear |  | -4.0 (-21.1 to +21.5) | +35.3 (+6.3 to +57.5), clear |
| Hotspot G10+H10 | 40 | 5 / 21 / 14 | 14 of 35 (40%) | 9 of 26 (35%) | 5 / 21 / 14 | 14 of 35 (40%) | 9 of 26 (35%) |
| rest of Hotspot | 195 | 68 / 42 / 85 | 42 of 127 (33%) | 33 of 110 (30%) | 92 / 44 / 59 | 40 of 103 (39%) | 34 of 136 (25%) |
| cell minus rest of the map |  |  | +6.9 (-12.3 to +30.4) | +4.6 (-15.1 to +22.5) |  | +1.2 (-20.6 to +25.3) | +9.6 (-8.8 to +26.6) |
| Sea of Fortune F9+G9 | 10 | 2 / 7 / 1 | 2 of 8 (25%, small n) | 2 of 9 (22%, small n) | 2 / 7 / 1 | 2 of 8 (25%, small n) | 2 of 9 (22%, small n) |
| rest of Sea of Fortune | 107 | 30 / 13 / 64 | 15 of 77 (20%) | 14 of 43 (33%) | 63 / 9 / 35 | 14 of 44 (32%) | 11 of 72 (15%) |
| cell minus rest of the map |  |  | +5.5 (-20.5 to +30.6) | -10.3 (-36.3 to +18.4) |  | -6.8 (-35.2 to +22.2) | +6.9 (-21.4 to +37.7) |
| Loop F8 | 15 | 6 / 4 / 5 | 5 of 9 (56%, small n) | 4 of 10 (40%, small n) | 6 / 4 / 5 | 5 of 9 (56%, small n) | 4 of 10 (40%, small n) |
| rest of Loop | 127 | 51 / 21 / 55 | 30 of 76 (40%) | 17 of 72 (24%) | 51 / 21 / 55 | 30 of 76 (40%) | 17 of 72 (24%) |
| cell minus rest of the map |  |  | +16.1 (-19.4 to +48.5) | +16.4 (-12.2 to +53.8) |  | +16.1 (-19.4 to +48.5) | +16.4 (-12.2 to +53.8) |
| Loop F10 | 9 | 4 / 1 / 4 | 3 of 5 (too few) | 1 of 5 (too few) | 4 / 1 / 4 | 3 of 5 (too few) | 1 of 5 (too few) |
| rest of Loop | 133 | 53 / 24 / 56 | 32 of 80 (40%) | 20 of 77 (26%) | 53 / 24 / 56 | 32 of 80 (40%) | 20 of 77 (26%) |
| cell minus rest of the map |  |  | too few | too few |  | too few | too few |

Deaths, per 100 smokes:

| Smokes | n | Ships died per 100 | Ships caught per 100 | Smoker died per 100 | Smoker caught per 100 |
|---|---|---|---|---|---|
| Sleeping Giant G1 | 21 | 19.0 (0.0 to 42.1) | 14.3 (0.0 to 30.4) | 9.5 (0.0 to 22.7) | 4.8 (0.0 to 13.8) |
| rest of Sleeping Giant | 217 | 14.7 (10.1 to 21.5) | 11.5 (7.6 to 17.3) | 10.6 (6.7 to 16.1) | 7.4 (4.0 to 12.7) |
| cell minus rest of the map |  | +4.3 (-14.8 to +27.0) | +2.8 (-11.4 to +17.2) | -1.1 (-13.1 to +11.7) | -2.6 (-11.5 to +7.4) |
| Hotspot G10+H10 | 40 | 20.0 (4.9 to 41.2) | 10.0 (2.7 to 17.8) | 10.0 (0.0 to 22.0) | 2.5 (0.0 to 7.9) |
| rest of Hotspot | 195 | 14.9 (10.3 to 20.1) | 7.2 (4.5 to 9.6) | 9.2 (5.4 to 13.4) | 3.6 (1.1 to 6.3) |
| cell minus rest of the map |  | +5.1 (-12.5 to +25.5) | +2.8 (-5.6 to +10.9) | +0.8 (-10.3 to +13.0) | -1.1 (-5.9 to +4.8) |
| Sea of Fortune F9+G9 | 10 (small n) | 0.0 (0.0 to 0.0) | 0.0 (0.0 to 0.0) | 0.0 (0.0 to 0.0) | 0.0 (0.0 to 0.0) |
| rest of Sea of Fortune | 107 | 19.6 (12.4 to 30.5) | 15.0 (8.9 to 24.7) | 14.0 (8.0 to 25.3) | 9.3 (3.9 to 17.7) |
| cell minus rest of the map |  | -19.6 (-30.2 to -12.3), clear | -15.0 (-23.4 to -8.6), clear | -14.0 (-24.4 to -7.9), clear | -9.3 (-17.9 to -3.6), clear |
| Loop F8 | 15 | 26.7 (7.1 to 54.5) | 13.3 (0.0 to 40.0) | 26.7 (7.7 to 54.5) | 13.3 (0.0 to 40.0) |
| rest of Loop | 127 | 17.3 (10.4 to 26.3) | 10.2 (5.3 to 16.7) | 12.6 (7.5 to 19.6) | 5.5 (1.9 to 11.1) |
| cell minus rest of the map |  | +9.3 (-13.9 to +42.8) | +3.1 (-12.8 to +31.8) | +14.1 (-7.2 to +45.8) | +7.8 (-8.1 to +37.4) |
| Loop F10 | 9 (small n) | 33.3 (9.1 to 71.4) | 33.3 (8.3 to 66.7) | 22.2 (0.0 to 57.1) | 22.2 (0.0 to 57.1) |
| rest of Loop | 133 | 17.3 (10.4 to 25.2) | 9.0 (4.1 to 14.8) | 13.5 (8.0 to 20.2) | 5.3 (2.0 to 10.1) |
| cell minus rest of the map |  | +16.0 (-16.2 to +55.4) | +24.3 (-8.3 to +63.1) | +8.7 (-16.1 to +51.8) | +17.0 (-6.8 to +58.5) |

- G1 (Sleeping Giant): cap A was never ours when these smokes were laid (13 neutral, 8 theirs); 14 of the 21 are early smokes. We took A after 6 of 21 (29%); the enemy took it after 7 of 13 (54%, small n). Enemy took, cell minus rest of the map: +35.3 (+6.3 to +57.5), clear. The smoke pays in damage while the cap often goes to the other side.
- Hotspot G10+H10: we took D after 14 of 35 (40%), the enemy after 9 of 26 (35%); neither differs clearly from the rest of the map.
- Sea of Fortune F9+G9: 2 of 8 (25%, small n) and 2 of 9 (22%, small n); no ship died or was caught in these 10 smokes, clearly below the rest of the map (died -19.6 (-30.2 to -12.3), clear).
- Damage: the three C4 cells stay clearly above the rest of their map. The two Loop cells are well above the rest of Loop on average (18,318 and 20,728 against about 6,825), but with whole clans resampled the gap interval crosses zero for both (-4,443 to +23,609; -1,094 to +29,325): they rest on a few big smokes, as round 5 said.
- Loop F8 and F10: round 5 quoted no cap result for these two cells. Timeline: F8 we took 5 of 9 (56%, small n), enemy took 4 of 10 (40%, small n); F10 we took 3 of 5 (too few), enemy took 1 of 5 (too few). F10 stays the costly one: died 33.3 (9.1 to 71.4), caught 33.3 (8.3 to 66.7) per 100 (small n).

**Top 6 or Shared:** Shared, as in round 5 (the cells were found on all clans pooled). We took the nearest cap: G1 Top 6 5 of 12 (42%, small n) vs Rest 1 of 9 (11%, small n) (gap interval -3 to +69); Hotspot Top 6 5 of 12 (42%, small n) vs Rest 9 of 23 (39%) (gap interval -37 to +39); the other cells have too few on each side. Deaths at G1: died 8.3 vs 33.3; -25.0 (-66.7 to +12.5); Hotspot: died 38.5 vs 11.1; +27.4 (-13.3 to +76.0). No clear gap.

**Clans:**
- Sleeping Giant G1 (10 clans, 13 games): Top 6: RESIN 5, VRTUS 3, BONKZ 2, HTDOG 1, H-SR 1 | Rest: BONKY 3, KSC 2, PFANS 2, NGA 1, -BN- 1
- Hotspot G10+H10 (18 clans, 18 games): Top 6: H-SR 5, RESIN 4, HTDOG 1, VRTUS 1, KITE 1, BONKZ 1 | Rest: REEEE 5, BONKY 4, BTLST 3, -BN- 3, MZY 2, HFANS 2, KITED 2, KSC 2, NGA 1, SCCC2 1, PFANS 1, EPOXY 1
- Sea of Fortune F9+G9 (6 clans, 5 games): Top 6: BONKZ 3, H-SR 1 | Rest: BONKY 2, MZY 2, HFANS 1, -BN- 1
- Loop F8 (9 clans, 10 games): Top 6: BONKZ 5, RESIN 1, H-SR 1 | Rest: MACHX 2, HFANS 2, OGF 1, INCA 1, -BN- 1, MZY 1
- Loop F10 (6 clans, 6 games): Top 6: H-SR 2 | Rest: EPOXY 2, MZY 2, 5D 1, KM 1, MACHX 1

**Could not be done / proxy:** Nothing missing. The cells were picked and scored on the same data (round 5 caution), so the damage gaps will shrink on new data; that caution is unchanged.

**Verdict:** Keep (shared high-paying cells; the cap is not taken more often there). Lead: G1 smokes go with the enemy taking A.

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Sleeping Giant G1: n and concealed damage per smoke | 21; 24,101 | 21; 24,101 | unchanged |
| Sleeping Giant G1: we took the cap (cap not already ours) | 19% of 21 | nearest cap 6 of 21 (29%); contested cap 6 of 21 (29%) | cap timeline |
| Sleeping Giant G1: enemy took the cap | not given | nearest cap 7 of 13 (54%, small n); contested cap 7 of 13 (54%, small n) | cap timeline (new) |
| Sleeping Giant G1: ships lost per 100 smokes | 14.3 | caught 14.3 (0.0 to 30.4); died 19.0 (0.0 to 42.1) | caught unchanged; died is the new death metric |
| Hotspot G10+H10: n and concealed damage per smoke | 40; 16,970 | 40; 16,970 | unchanged |
| Hotspot G10+H10: we took the cap (cap not already ours) | 34% of 35 | nearest cap 14 of 35 (40%); contested cap 14 of 35 (40%) | cap timeline |
| Hotspot G10+H10: enemy took the cap | not given | nearest cap 9 of 26 (35%); contested cap 9 of 26 (35%) | cap timeline (new) |
| Hotspot G10+H10: ships lost per 100 smokes | 10.0 | caught 10.0 (2.7 to 17.8); died 20.0 (4.9 to 41.2) | caught unchanged; died is the new death metric |
| Sea of Fortune F9+G9: n and concealed damage per smoke | 10; 24,597 | 10; 24,597 | unchanged |
| Sea of Fortune F9+G9: we took the cap (cap not already ours) | 25% of 8 | nearest cap 2 of 8 (25%, small n); contested cap 2 of 8 (25%, small n) | cap timeline |
| Sea of Fortune F9+G9: enemy took the cap | not given | nearest cap 2 of 9 (22%, small n); contested cap 2 of 9 (22%, small n) | cap timeline (new) |
| Sea of Fortune F9+G9: ships lost per 100 smokes | 0.0 | caught 0.0 (0.0 to 0.0); died 0.0 (0.0 to 0.0) | caught unchanged; died is the new death metric |
| Loop F8: n and concealed damage per smoke | 15; 18,318 | 15; 18,318 | unchanged |
| Loop F8: we took the cap (cap not already ours) | no cap result quoted | nearest cap 5 of 9 (56%, small n); contested cap 5 of 9 (56%, small n) | cap timeline |
| Loop F8: enemy took the cap | not given | nearest cap 4 of 10 (40%, small n); contested cap 4 of 10 (40%, small n) | cap timeline (new) |
| Loop F8: ships lost per 100 smokes | 13.3 | caught 13.3 (0.0 to 40.0); died 26.7 (7.1 to 54.5) | caught unchanged; died is the new death metric |
| Loop F10: n and concealed damage per smoke | 9; 20,728 | 9; 20,728 | unchanged |
| Loop F10: we took the cap (cap not already ours) | no cap result quoted | nearest cap 3 of 5 (too few); contested cap 3 of 5 (too few) | cap timeline |
| Loop F10: enemy took the cap | not given | nearest cap 1 of 5 (too few); contested cap 1 of 5 (too few) | cap timeline (new) |
| Loop F10: ships lost per 100 smokes | 33.3 | caught 33.3 (8.3 to 66.7); died 33.3 (9.1 to 71.4) | caught unchanged; died is the new death metric |

### 7b. Sleeping Giant cap B (C5-SG-3): is the smoke there to stop the enemy taking B

**Answer:** The round 5 statement stands. The enemy took B during or just after 1 of 28 (4%) of these smokes, the same count as round 5, and that is not clearly different from the other caps (9 of 68 (13%)). The timeline adds that the enemy was actually taking B while the smoke stood in only 6 of 34 (18%), and in 3 of the 16 laid when B was ours. This is cap-holding and cap-contesting smoke, not a reaction to an attack on B.

**Numbers (all smokes inside or within 2 km of a cap edge; 119 of the map's 305 smokes; cap = nearest cap, team-normalized letter):**

| Cap | Smokes | Top 6 | Ours / neutral / theirs at activation | Enemy took it (of not theirs) | Enemy took it when ours | We took it (of not ours) | Enemy was taking it while the smoke stood | Same, when ours | Concealed dmg | Ships died per 100 | Ships caught per 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cap A | 46 | 21 | 28 / 12 / 6 | 7 of 40 (18%) | 3 of 28 (11%) | 10 of 18 (56%) | 13 of 46 (28%) | 8 of 28 (29%) | 11,952 | 13.0 (6.1 to 22.6) | 6.5 (0.0 to 14.6) |
| Cap B | 34 | 13 | 16 / 12 / 6 | 1 of 28 (4%) | 1 of 16 (6%) | 7 of 18 (39%) | 6 of 34 (18%) | 3 of 16 (19%) | 5,747 | 14.7 (5.4 to 26.5) | 11.8 (2.9 to 25.0) |
| Cap C | 17 | 7 | 8 / 2 / 7 | 2 of 10 (20%, small n) | 2 of 8 (25%, small n) | 4 of 9 (44%, small n) | 4 of 17 (24%) | 2 of 8 (25%, small n) | 12,877 | 29.4 (11.1 to 57.1) | 29.4 (10.0 to 56.2) |
| Cap D | 22 | 5 | 18 / 0 / 4 | 0 of 18 (0%) | 0 of 18 (0%) | 0 of 4 (too few) | 2 of 22 (9%) | 2 of 18 (11%) | 7,035 | 13.6 (0.0 to 24.0) | 13.6 (0.0 to 24.1) |
| Other caps together (A, C, D) | 85 | 33 | 54 / 14 / 17 | 9 of 68 (13%) | 5 of 54 (9%) | 14 of 31 (45%) | 19 of 85 (22%) | 12 of 54 (22%) | 10,864 | 16.5 (10.6 to 22.8) | 12.9 (7.6 to 19.2) |

The same on the contested cap (the cap the batch ties the smoke to):

| Smokes near | Contested cap is the nearest cap | Ours / neutral / theirs | Enemy took it | We took it |
|---|---|---|---|---|
| Cap A | 46 of 46 | 28 / 12 / 6 | 7 of 40 (18%) | 10 of 18 (56%) |
| Cap B | 34 of 34 | 16 / 12 / 6 | 1 of 28 (4%) | 7 of 18 (39%) |
| Cap C | 17 of 17 | 8 / 2 / 7 | 2 of 10 (20%, small n) | 4 of 9 (44%, small n) |
| Cap D | 4 of 22 | 1 / 6 / 15 | 1 of 7 (too few) | 1 of 21 (5%) |
| Other caps together (A, C, D) | 67 of 85 | 37 / 20 / 28 | 10 of 57 (18%) | 15 of 48 (31%) |

- B minus the other caps: enemy took, nearest cap -9.7 (-21.8 to +4.0); contested cap -14.0 (-29.5 to +0.4); we took, nearest cap -6.3 (-38.8 to +27.3); enemy was taking it -4.7 (-17.6 to +6.7); ships died per 100 -1.8 (-14.8 to +14.9); caught -1.2 (-12.3 to +14.0). None clear.
- B ours at activation: 47.1% (26.3 to 68.8); other caps 63.5% (50.7 to 75.5); difference -16.5 (-40.4 to +11.6). The timeline owner at activation agrees with the round 5 snapshot for 34 of the 34 smokes.
- At B: 31 destroyer smokes, 3 cruiser. Ships: Daring 15, Gdańsk 6, Harugumo 3, G. Hoffmann 2, Somers 2. Cap sitters 23, long-smoke ships 5. 10 are inside the cap.
- The one smoke after which the enemy took B: 5D Shimakaze (B ours at activation).
- We took B after 7 of 18 (39%) (round 5: 5 of 18): the timeline finds 2 more captures than the snapshots did. At cap A it finds more on both sides: enemy took 7 of 40 (18%) (round 5: 3 of 40), we took 10 of 18 (56%) (7 of 18).
- D is a special case: 4 of the 22 smokes near D have D as the batch's contested cap; the rest are tied to another cap.

**Top 6 or Shared:** Shared spot. Share of all map smokes: Top 6 13 of 137 (10%) vs Rest 21 of 168 (12%), -3.0 (-12.1 to +7.8). B ours at activation: Top 6 8 of 13 vs Rest 8 of 21, +23.4 (-26.4 to +64.5). Enemy took B: Top 6 0 of 11 (0%, small n), Rest 1 of 17 (6%). We took B: Top 6 4 of 5 (too few), Rest 3 of 13 (23%, small n). Deaths at B: Top 6 died 7.7 (0.0 to 20.0), caught 0.0 (0.0 to 0.0) (small n); Rest died 19.0 (5.6 to 42.9), caught 19.0 (6.2 to 40.0). Concealed damage Top 6 11,440 vs Rest 2,224 per smoke.

**Clans:** Top 6: VRTUS 4, RESIN 4, HTDOG 3, BONKZ 2 | Rest: HFANS 7, KITED 4, 5D 3, KSE 3, EPOXY 1, INCA 1, BONKY 1, -BN- 1. With B ours: Top 6: VRTUS 4, HTDOG 3, BONKZ 1 | Rest: HFANS 3, KSE 1, BONKY 1, KITED 1, -BN- 1, 5D 1.

**Could not be done / proxy:** The data still cannot tell "the smoke stopped the enemy" from "the enemy never came". The timeline's capturing-side field is the closest sign of a real attack on the cap, and it is low at B.

**Verdict:** Drop the reading "there to stop the enemy taking B". Keep as: low-paying shared cap-sitter spot. Same as round 5.

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Cap A: ours / neutral / theirs at activation | 28 / 12 / 6 | 28 / 12 / 6 | unchanged (timeline agrees with the snapshot) |
| Cap A: enemy took it | 3 of 40 (8%) | 7 of 40 (18%) | cap timeline |
| Cap A: we took it | 7 of 18 (39%) | 10 of 18 (56%) | cap timeline |
| Cap A: ships lost per 100 smokes | 6.5 | caught 6.5 (0.0 to 14.6); died 13.0 (6.1 to 22.6) | caught unchanged; died is the new death metric |
| Cap B: ours / neutral / theirs at activation | 16 / 12 / 6 | 16 / 12 / 6 | unchanged (timeline agrees with the snapshot) |
| Cap B: enemy took it | 1 of 28 (4%) | 1 of 28 (4%) | cap timeline (same result) |
| Cap B: we took it | 5 of 18 (28%) | 7 of 18 (39%) | cap timeline |
| Cap B: ships lost per 100 smokes | 11.8 | caught 11.8 (2.9 to 25.0); died 14.7 (5.4 to 26.5) | caught unchanged; died is the new death metric |
| Cap C: ours / neutral / theirs at activation | 8 / 2 / 7 | 8 / 2 / 7 | unchanged (timeline agrees with the snapshot) |
| Cap C: enemy took it | 2 of 10 (20%, small n) | 2 of 10 (20%, small n) | cap timeline (same result) |
| Cap C: we took it | 4 of 9 (small n) | 4 of 9 (44%, small n) | cap timeline (same result) |
| Cap C: ships lost per 100 smokes | 29.4 | caught 29.4 (10.0 to 56.2); died 29.4 (11.1 to 57.1) | caught unchanged; died is the new death metric |
| Cap D: ours / neutral / theirs at activation | 18 / 0 / 4 | 18 / 0 / 4 | unchanged (timeline agrees with the snapshot) |
| Cap D: enemy took it | 0 of 18 (0%) | 0 of 18 (0%) | cap timeline (same result) |
| Cap D: we took it | 0 of 4 (too few) | 0 of 4 (too few) | cap timeline (same result) |
| Cap D: ships lost per 100 smokes | 13.6 | caught 13.6 (0.0 to 24.1); died 13.6 (0.0 to 24.0) | caught unchanged; died is the new death metric |
| Enemy took B vs the other caps | 1 of 28 (4%) vs 5 of 68 (7%); -4 pts (-13 to +9) | 1 of 28 (4%) vs 9 of 68 (13%); -9.7 (-21.8 to +4.0) | cap timeline |
| B ours at activation, B vs other caps | 47% (27 to 72) vs 64% (52 to 75) | 47.1% vs 63.5% | unchanged values, timeline owner |
| Sign of a real attack on B (of the 16 laid when B was ours) | enemy already contesting at the start 2; batch "cap defended" 2 | enemy was taking B while the smoke stood 3 of 16 | cap timeline (capturing side) replaces the snapshot flags |

### 7c. Mountain Range, radar from smoke at B (C5-MR-2): did the enemy take B during those smokes

**Answer:** Yes, often, and the timeline makes it slightly worse than round 5 said: the enemy took B during or just after 6 of 14 (43%, small n) of the radar smokes at B, and after 5 of the 9 laid when B was ours (round 5: 4 of 8). That is no better than other smokes at B (12 of 32 (38%)). The round 5 statement stands. Small n throughout.

**Numbers:** radar smoke defined two ways: the round 5 tags (primary purpose cap control or radar trap, or the batch's radar-from-inside record) and the radar log (a ship of the smoking team pressed radar while standing in the smoke). At B the two pick the same smokes: 15 by tags, 15 by the log, 15 in both. So the two sets of rows below are identical at B. Round 5's headline rows used "nearest cap is B, any distance"; the 2 km rule keeps 7.

| Smokes | n | Top 6 | B ours / neutral / theirs at activation | Enemy took B | Enemy took B when ours | We took B (of not ours) | Enemy was taking B while the smoke stood | Ships died per 100 | Ships caught per 100 |
|---|---|---|---|---|---|---|---|---|---|
| Radar smokes (round 5 tags), nearest cap B | 15 | 12 | 9 / 5 / 1 | 6 of 14 (43%, small n) | 5 of 9 (56%, small n) | 4 of 6 (too few) | 8 of 15 (53%) | 6.7 (0.0 to 16.7) | 6.7 (0.0 to 17.6) |
| Other smokes, nearest cap B (no radar tag) | 53 | 23 | 15 / 17 / 21 | 12 of 32 (38%) | 5 of 15 (33%) | 17 of 38 (45%) | 17 of 53 (32%) | 15.7 (7.7 to 26.2) | 7.5 (1.6 to 16.3) |
| Radar smokes (round 5 tags), within 2 km of B | 7 (too few) | 5 | 4 / 2 / 1 | 2 of 6 (too few) | 1 of 4 (too few) | 1 of 3 (too few) | 3 of 7 (too few) | too few | too few |
| Other smokes within 2 km of B (no radar tag) | 24 | 11 | 7 / 8 / 9 | 5 of 15 (33%) | 2 of 7 (too few) | 11 of 17 (65%) | 6 of 24 (25%) | 16.7 (5.0 to 30.4) | 8.3 (0.0 to 19.2) |
| Radar pressed from the smoke (radar log), nearest cap B | 15 | 12 | 9 / 5 / 1 | 6 of 14 (43%, small n) | 5 of 9 (56%, small n) | 4 of 6 (too few) | 8 of 15 (53%) | 6.7 (0.0 to 17.6) | 6.7 (0.0 to 16.7) |
| Other smokes, nearest cap B (no radar pressed) | 53 | 23 | 15 / 17 / 21 | 12 of 32 (38%) | 5 of 15 (33%) | 17 of 38 (45%) | 17 of 53 (32%) | 15.7 (7.4 to 25.6) | 7.5 (1.7 to 16.7) |
| Radar pressed from the smoke (radar log), within 2 km of B | 7 (too few) | 5 | 4 / 2 / 1 | 2 of 6 (too few) | 1 of 4 (too few) | 1 of 3 (too few) | 3 of 7 (too few) | too few | too few |
| Other smokes within 2 km of B (no radar pressed) | 24 | 11 | 7 / 8 / 9 | 5 of 15 (33%) | 2 of 7 (too few) | 11 of 17 (65%) | 6 of 24 (25%) | 16.7 (4.3 to 29.2) | 8.3 (0.0 to 18.2) |
| Radar smokes (round 5 tags), other maps, nearest cap | 112 | 61 | 52 / 35 / 25 | 20 of 87 (23%) | 10 of 52 (19%) | 28 of 60 (47%) | 47 of 112 (42%) | 14.3 (7.4 to 22.5) | 10.7 (5.3 to 17.6) |
| Radar pressed (radar log), other maps, nearest cap | 124 | 65 | 55 / 38 / 31 | 21 of 93 (23%) | 9 of 55 (16%) | 30 of 69 (44%) | 50 of 124 (40%) | 17.7 (9.9 to 26.2) | 12.9 (7.4 to 19.6) |

For the "other maps" rows read "the nearest cap" for "B". The same smokes on the contested cap:

| Smokes | Contested cap is the nearest cap | Ours / neutral / theirs | Enemy took it | Enemy took it when ours | We took it |
|---|---|---|---|---|---|
| Radar smokes (round 5 tags), nearest cap B | 14 of 15 | 9 / 5 / 1 | 5 of 14 (36%, small n) | 4 of 9 (44%, small n) | 4 of 6 (too few) |
| Other smokes, nearest cap B (no radar tag) | 52 of 53 | 14 / 17 / 22 | 11 of 31 (36%) | 4 of 14 (29%, small n) | 17 of 39 (44%) |
| Radar smokes (round 5 tags), within 2 km of B | 7 of 7 | 4 / 2 / 1 | 2 of 6 (too few) | 1 of 4 (too few) | 1 of 3 (too few) |
| Other smokes within 2 km of B (no radar tag) | 24 of 24 | 7 / 8 / 9 | 5 of 15 (33%) | 2 of 7 (too few) | 11 of 17 (65%) |
| Radar smokes (round 5 tags), other maps, nearest cap | 90 of 112 | 34 / 37 / 41 | 19 of 71 (27%) | 6 of 34 (18%) | 28 of 78 (36%) |
| Radar pressed (radar log), other maps, nearest cap | 101 of 124 | 36 / 40 / 48 | 20 of 76 (26%) | 5 of 36 (14%) | 30 of 88 (34%) |

- Radar smokes minus other smokes at B: enemy took B +5.4 (-26.2 to +32.4); B ours at activation +31.7 (+6.7 to +53.6), clear; enemy was taking B while the smoke stood +21.3 (-6.7 to +54.8); ships died per 100 -9.0 (-23.3 to +3.9); caught -0.9 (-14.6 to +13.2).
- Radar smokes are laid on a held B more often (9 of 15 against 15 of 53), and the enemy was taking B during 8 of 15 (53%) of them: part of this is defence in intent. It did not hold: B was lost after 5 of 9.
- Against radar smokes on other maps (20 of 87 (23%) lost the nearest cap; when ours 10 of 52 (19%)): difference +19.9 (-2.3 to +45.8), not clear.
- The 5 "ours, then lost" smokes come from 3 games: KITE Gearing 10:41; RESIN Gdańsk 13:29; H-SR Harugumo 13:57; BONKZ Svea 16:02; BONKZ Svea 17:13 (elapsed time). The earliest is at 10 minutes.
- Owner at activation differs from the round 5 snapshot for 1 of the 15: RESIN Gdańsk 13:29, snapshot "theirs", timeline "ours", 6.2 km from the B edge. That is why round 5 had 8 / 5 / 2 and the timeline has 9 / 5 / 1.
- Whole map, enemy took the nearest cap: A 10 of 41 (24%), B 18 of 46 (39%), C 12 of 56 (21%). B is still the cap that changes hands most on this map.
- Ships: Gearing 4, Svea 4, Somers 3, Gdańsk 3, Harugumo 1. Return 12,843 concealed damage per smoke; 6.7 died and 6.7 caught per 100 (one ship).

**Top 6 or Shared:** Top 6 spot, as in round 5. Radar smokes at B are 12 of 88 Top 6 smokes on the map (14%) vs 3 of 119 Rest (2%), +11.1 (+1.3 to +21.8), clear. With 3 Rest smokes there is no Top 6 vs Rest comparison of the cap result.

**Clans:** Top 6: KITE 4, BONKZ 4, H-SR 2, RESIN 2 | Rest: HFANS 2, SCCC2 1.

**Could not be done / proxy:** n is 15 (9 on a held cap), from 6 clans; the 5 losses come from 3 games. No rate here should be read as more than a count.

**Verdict:** Keep the spot; Drop "radar from smoke defends B". Same as round 5.

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Radar smokes, nearest cap B: ours / neutral / theirs | 8 / 5 / 2 | 9 / 5 / 1 | cap timeline |
| Radar smokes, nearest cap B: enemy took | 5 of 13 (38%, small n) | 6 of 14 (43%, small n) | cap timeline |
| Radar smokes, nearest cap B: enemy took when ours | 4 of 8 (50%, small n) | 5 of 9 (56%, small n) | cap timeline |
| Radar smokes, nearest cap B: we took | 3 of 7 (too few) | 4 of 6 (too few) | cap timeline |
| Other smokes, nearest cap B: ours / neutral / theirs | 15 / 17 / 21 | 15 / 17 / 21 | unchanged |
| Other smokes, nearest cap B: enemy took | 11 of 32 (34%) | 12 of 32 (38%) | cap timeline |
| Other smokes, nearest cap B: enemy took when ours | 5 of 15 (33%) | 5 of 15 (33%) | cap timeline (same result) |
| Other smokes, nearest cap B: we took | 17 of 38 (45%) | 17 of 38 (45%) | cap timeline (same result) |
| Radar smokes within 2 km of B: ours / neutral / theirs | 4 / 2 / 1 | 4 / 2 / 1 | unchanged |
| Radar smokes within 2 km of B: enemy took | 2 of 6 (too few) | 2 of 6 (too few) | cap timeline (same result) |
| Radar smokes within 2 km of B: enemy took when ours | 1 of 4 (too few) | 1 of 4 (too few) | cap timeline (same result) |
| Radar smokes within 2 km of B: we took | 1 of 3 (too few) | 1 of 3 (too few) | cap timeline (same result) |
| Other smokes within 2 km of B: ours / neutral / theirs | 7 / 8 / 9 | 7 / 8 / 9 | unchanged |
| Other smokes within 2 km of B: enemy took | 4 of 15 (27%) | 5 of 15 (33%) | cap timeline |
| Other smokes within 2 km of B: enemy took when ours | 2 of 7 (too few) | 2 of 7 (too few) | cap timeline (same result) |
| Other smokes within 2 km of B: we took | 11 of 17 (65%) | 11 of 17 (65%) | cap timeline (same result) |
| Radar smokes, other maps (nearest cap): ours / neutral / theirs | 52 / 35 / 25 | 52 / 35 / 25 | unchanged |
| Radar smokes, other maps (nearest cap): enemy took | 16 of 87 (18%) | 20 of 87 (23%) | cap timeline |
| Radar smokes, other maps (nearest cap): enemy took when ours | 7 of 52 (13%) | 10 of 52 (19%) | cap timeline |
| Radar smokes, other maps (nearest cap): we took | 23 of 60 (38%) | 28 of 60 (47%) | cap timeline |
| Whole map, enemy took the nearest cap | A 6 of 41 (15%), B 16 of 45 (36%), C 10 of 56 (18%) | A 10 of 41 (24%), B 18 of 46 (39%), C 12 of 56 (21%) | cap timeline |
| Radar smokes at B: ships lost | 1 death | caught 6.7 per 100; died 6.7 per 100 | unchanged (one ship on both metrics) |
| Radar definition | tags: 15 smokes | tags 15, radar log 15, same smokes 15 | radar log added; same set |

### 7d. Loop, cap sitters at B (C5-LP-6 and spot `c5-lp-sitters-b`)

**Answer:** The spot rebuilds exactly (28 smokes: 15 Top 6, 13 Rest). On the timeline the cap result is much better than round 5 said: we took B during or just after 11 of 17 (65%) of the smokes laid when B was not ours (Top 6 7 of 9 (78%, small n), Rest 4 of 8 (50%, small n); round 5: 5 of 10 and 1 of 8). The enemy took B after 2 of 15 (13%). Deaths are low on both metrics. The Top 6 lead in the spot stands.

**Numbers:** membership as round 5: destroyer smokes by cap-sitter ships (Daring, Z-42, Gdansk, Grozovoi, Shimakaze) on Loop whose centre is inside the spot's ellipse; 88 such smokes on the map (23 Top 6, 65 Rest). "B" = the cap at normalized letter B, followed for every smoke whatever its nearest cap.

| Smokes | n | B ours / neutral / theirs at activation | We took B (of not ours) | Enemy took B (of not theirs) | Enemy took B when ours | Enemy was taking B while the smoke stood | Concealed dmg per smoke | Ships died per 100 | Ships caught per 100 | Smoker died per 100 | Smoker caught per 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| All 28 | 28 | 11 / 4 / 13 | 11 of 17 (65%) | 2 of 15 (13%) | 1 of 11 (9%, small n) | 8 of 28 (29%) | 3,668 | 7.1 (0.0 to 16.7) | 3.6 (0.0 to 11.1) | 3.6 (0.0 to 13.0) | 0.0 (0.0 to 0.0) |
| Top 6 | 15 | 6 / 2 / 7 | 7 of 9 (78%, small n) | 1 of 8 (12%, small n) | 1 of 6 (too few) | 5 of 15 (33%) | 5,834 | 6.7 (0.0 to 16.7) | 6.7 (0.0 to 17.6) | 0.0 (0.0 to 0.0) | 0.0 (0.0 to 0.0) |
| Rest | 13 (small n) | 5 / 2 / 6 | 4 of 8 (50%, small n) | 1 of 7 (too few) | 0 of 5 (too few) | 3 of 13 (23%, small n) | 1,169 | 7.7 (0.0 to 25.0) | 0.0 (0.0 to 0.0) | 7.7 (0.0 to 30.0) | 0.0 (0.0 to 0.0) |

The library fields on the same smokes (nearest cap and contested cap; they are the same cap for all 28, and it is B for 26 and C for 2):

| Smokes | Nearest cap: ours / neutral / theirs | We took it | Enemy took it | Contested cap: ours / neutral / theirs | We took it | Enemy took it |
|---|---|---|---|---|---|---|
| All 28 | 10 / 6 / 12 | 12 of 18 (67%) | 2 of 16 (12%) | 10 / 6 / 12 | 12 of 18 (67%) | 2 of 16 (12%) |
| Top 6 | 5 / 4 / 6 | 8 of 10 (80%, small n) | 1 of 9 (11%, small n) | 5 / 4 / 6 | 8 of 10 (80%, small n) | 1 of 9 (11%, small n) |
| Rest | 5 / 2 / 6 | 4 of 8 (50%, small n) | 1 of 7 (too few) | 5 / 2 / 6 | 4 of 8 (50%, small n) | 1 of 7 (too few) |
| Cap sitters on Loop outside the spot | 29 / 5 / 26 | 5 of 31 (16%) | 6 of 34 (18%) | 29 / 5 / 26 | 5 of 31 (16%) | 6 of 34 (18%) |

- Top 6 minus Rest in the spot: we took B 77.8 vs 50.0; +27.8 (+8.1 to +54.2), clear (nearest cap: 80.0 vs 50.0; +30.0 (+8.1 to +57.1), clear); n is 9 and 8, small on both sides. Concealed damage 5,834 vs 1,169; +4,665 (+1,046 to +8,745), clear. B ours at activation 40.0 vs 38.5; +1.5 (-60.8 to +37.5).
- Deaths, Top 6 vs Rest: died 6.7 vs 7.7; -1.0 (-25.0 to +14.3); caught 6.7 vs 0.0; +6.7 (+0.0 to +16.7); smoker died 0.0 vs 7.7; -7.7 (-27.3 to +0.0). 2 ships died in the 28 smokes, 1 was caught.
- Against the other 60 cap-sitter smokes on Loop: we took the nearest cap 12 of 18 (67%) in the spot vs 5 of 31 (16%) outside, +50.5 (+23.1 to +87.0), clear; smoker died per 100 3.6 (0.0 to 13.0) vs 15.0 (6.8 to 26.4), -11.4 (-24.0 to -1.3), clear; ships died -7.9 (-20.5 to +3.9); caught -1.4 (-10.0 to +7.6).
- Ships in the spot: Top 6 Gdańsk 9, Shimakaze 3, Z-42 2, Daring 1; Rest Z-42 7, Grozovoi 3, Daring 2, Shimakaze 1.

**Top 6 or Shared:** Top 6 spot (round 5: 15 of 23 Top 6 cap-sitter smokes against 13 of 65 Rest, +45 pts, +25 to +72; membership unchanged). The cap result now also leans Top 6 (+27.8 (+8.1 to +54.2), clear), on small n. Round 5's caution stays: most of the placement gap is ship choice (the Rest's cap sitter on Loop is the Daring, which sits at cap A).

**Clans:** Top 6: RESIN 4, KITE 3, BONKZ 3, H-SR 2, HTDOG 2, VRTUS 1 | Rest: REEEE 6, MACHX 2, SCCC2 2, RMN 1, MACH 1, EPOXY 1.

**Could not be done / proxy:** Nothing missing. The spot was chosen in round 4 because it showed a gap; treat the cap result as a lead on 17 smokes.

**Verdict:** Keep.

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| Members of the spot | 28 (15 Top 6, 13 Rest) | 28 (15 Top 6, 13 Rest) | unchanged |
| We took B during or just after, Top 6 | 5 of 10 | 7 of 9 (78%, small n) on B; 8 of 10 (80%, small n) on the nearest cap | cap timeline |
| We took B during or just after, Rest | 1 of 8 (small n) | 4 of 8 (50%, small n) on B; 4 of 8 (50%, small n) on the nearest cap | cap timeline |
| Enemy took B | not given | 2 of 15 (13%); when ours 1 of 11 (9%, small n) | cap timeline (new) |
| Concealed damage per smoke in the spot | 3,668 (Top 6 5.8k, Rest 1.2k) | 3,668 (Top 6 5,834, Rest 1,169) | unchanged |
| Ships lost per 100 smokes | 3.6 | caught 3.6 (0.0 to 11.1); died 7.1 (0.0 to 16.7) | caught unchanged; died is the new death metric |

---

### Notes on method and the library

- Scripts: `compute_x2.py` (all numbers, writes `ships-maps.json`; resampling seeded) and `write_x2.py` (this file and `CHECK-X2.md`).
- `from r5clib import *` also brings in `HERE` from `round3/common.py` and overwrites a script's own `HERE`. A script that then writes to `os.path.join(HERE, ...)` writes into `round3/`. This happened once here: the first run wrote `ships-maps.json` into `round3/`; it was moved into this folder straight away and the script now uses its own variable. Not a library bug, but a trap worth a line in the library notes.
- No library problem found. The timeline owner at activation agrees with the snapshot owner for all 34 Sleeping Giant smokes near B and for 14 of the 15 Mountain Range radar smokes.

---

## Item 8: clan styles (D1 to D3)

Source: `x3-clans/FINDINGS-X3.md`.


Batch `output/20261117-230933`: 1,547 smokes, 171 games, 30 clans (24 with 7+ games; BTLST, INCA, MANBA, OGF, RMN, KM have 5 or 6 and are flagged). Everything here is association. Styles describe what clans do; they do not explain winning.

What is new against round 5b, in one place:
- **Two death scores, side by side.** "Died" = a ship the smoke covered (the smoker, or a ship inside or behind it) died between activation and 20 s after the smoke dispersed; each dead ship is counted once. "Caught" = the batch list of ships that died while the smoke concealed them or just after it cleared around them (round 5's deaths). All smokes: 259 ships died (16.8 per 100) against 177 caught (11.4 per 100). "Died" leaves out 9 smokes of the one single-replay game, laid by the team with no replay (clans -BN-, KSC); they stay in "caught".
- **Caps come from the cap timeline**, on one fixed cap per smoke, up to 60 s after the smoke dispersed. "Taken" = the cap changed to the smoking clan (of smokes where it was not already theirs). "Not lost" = the enemy did not take it (of smokes inside or within 2 km of that cap, where the cap was not the enemy's). Both are given for the nearest cap and for the contested cap. My choice: for the contested-cap "not lost" the 2 km rule is measured to the contested cap.
- **Dropped from every table:** `cap_won`, `cap_def`, `we_took`, `enemy_took` (the round 5 snapshot fields) and the scores built on them: `took_pct`, `held_pct`, `deaths_per100`, `cap_won_pg`, `cap_def_pg`, `deaths_pg`.
- **Time scores use the replay clock** (`e0`, seconds since battle start at activation), not the HUD clock: first smoke of the game, share after 12:00, share before 5:00.
- Lineup, who, where and movement scores are untouched and identical to round 5b. Clan intervals are 95%, from resampling that clan's own games; Top 6 minus Rest intervals resample whole clans; a star means the interval excludes zero. Rates with fewer than 8 cases read "too few"; 8 to 14 is "small n".

### D1. Score every clan on the six dimensions ("what it buys" redone)

**Answer:** Done for all 30 clans (six flagged). Top 6 smokes went with fewer deaths on both death scores (died 12.3 against 19.3 per 100 smokes; caught 7.8 against 13.4), and from the timeline the Top 6 took the cap more often (39% against 28% on the nearest cap). "Not lost" is clear on the contested cap only.

**Numbers:** lowest clan, middle clan and highest clan among the 24 with 7+ games (only clans with 8+ cases are ranked).

| Score | Lowest | Median | Highest | Clans ranked |
|---|---|---|---|---|
| First smoke of the game (median, s) | 2:00 (H-SR) | 3:07 | 4:30 (MZY) | 24 |
| Smokes after 12:00 (%) | 0% (5D, MACH, NGA, RSR) | 9% | 25% (REEEE) | 24 |
| Concealed damage per game | 3,801 (KSE) | 42,794 | 88,963 (-BN-) | 24 |
| Concealed damage per smoke | 1,330 (KSE) | 8,687 | 16,378 (PFANS) | 24 |
| Died per 100 smokes | 6.0 (H-SR) | 16.3 | 50.0 (PN) | 24 |
| Caught per 100 smokes | 4.0 (H-SR) | 11.1 | 32.4 (5D) | 24 |
| Smoker died per 100 smokes | 3.8 (REEEE) | 11.7 | 40.0 (KSE) | 24 |
| Smoker caught per 100 smokes | 1.6 (KSC) | 6.6 | 27.8 (UYSC) | 24 |
| Nearest cap taken (% of smokes where it was not ours) | 9% (BONKY) | 31% | 56% (H-SR) | 24 |
| Contested cap taken (% of smokes where it was not ours) | 4% (NGA) | 26% | 44% (BONKZ) | 24 |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 62% (PFANS) | 86% | 100% (MACH) | 21 |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 50% (PFANS) | 80% | 100% (MACH) | 21 |
| Nearest caps taken with a smoke per game | 0.1 (PN) | 0.7 | 1.1 (MACHX) | 24 |
| Contested caps taken with a smoke per game | 0.1 (NGA, PN) | 0.7 | 1.1 (-BN-, BONKZ) | 24 |

The "died" score runs higher than "caught" for almost every clan (middle clan: 1.4 times as high), because it also counts ships that died in the 20 s after the smoke had gone and ships the batch did not list as concealed at death.

Deaths per 100 smokes, per clan: value (95% interval), percentile among the 24 clans. High percentile = more deaths.

| Clan | Games | Smokes | Died per 100 | Caught per 100 | Smoker died per 100 | Smoker caught per 100 |
|---|---|---|---|---|---|---|
| *RESIN | 24 | 103 | 17.5 (9.9 to 25.6) p57 | 7.8 (2.9 to 13.3) p22 | 9.7 (5.3 to 14.5) p39 | 1.9 (0.0 to 4.9) p4 |
| *H-SR | 22 | 100 | 6.0 (1.2 to 11.2) p0 | 4.0 (0.0 to 8.9) p0 | 4.0 (0.9 to 7.5) p4 | 2.0 (0.0 to 4.9) p9 |
| *BONKZ | 21 | 102 | 17.6 (10.3 to 25.8) p61 | 11.8 (5.9 to 17.8) p57 | 12.7 (6.9 to 20.0) p57 | 6.9 (2.4 to 12.7) p52 |
| MZY | 19 | 50 | 22.0 (10.2 to 39.5) p65 | 14.0 (3.2 to 28.8) p74 | 14.0 (5.0 to 24.4) p61 | 8.0 (0.0 to 17.5) p65 |
| *HTDOG | 18 | 106 | 10.4 (4.1 to 17.4) p17 | 6.6 (2.1 to 12.2) p9 | 8.5 (3.4 to 15.0) p30 | 5.7 (1.9 to 10.4) p30 |
| EPOXY | 17 | 82 | 15.9 (7.5 to 26.7) p43 | 12.2 (5.0 to 21.9) p61 | 9.8 (3.9 to 17.5) p43 | 6.1 (2.0 to 10.8) p37 |
| HFANS | 17 | 110 | 13.6 (6.9 to 22.6) p35 | 10.0 (4.0 to 18.6) p39 | 10.9 (5.0 to 18.5) p48 | 6.4 (2.5 to 11.9) p48 |
| -BN- | 14 | 91 | 11.6 (5.8 to 18.6) p30 | 9.9 (4.3 to 18.5) p35 | 8.1 (2.7 to 14.7) p26 | 5.5 (1.1 to 11.8) p26 |
| *KITE | 14 | 45 | 11.1 (2.6 to 21.2) p26 | 8.9 (2.4 to 15.9) p30 | 6.7 (0.0 to 16.7) p17 | 4.4 (0.0 to 10.8) p17 |
| KITED | 14 | 63 | 15.9 (6.2 to 25.9) p48 | 12.7 (3.2 to 22.4) p70 | 14.3 (5.3 to 23.5) p65 | 11.1 (3.1 to 20.4) p87 |
| MACHX | 14 | 82 | 9.8 (4.4 to 15.6) p11 | 6.1 (1.5 to 11.0) p4 | 8.5 (2.9 to 14.7) p35 | 6.1 (1.5 to 11.0) p37 |
| REEEE | 13 | 52 | 7.7 (0.0 to 18.4) p4 | 7.7 (0.0 to 18.4) p17 | 3.8 (0.0 to 10.8) p0 | 3.8 (0.0 to 10.8) p13 |
| PFANS | 12 | 24 | 16.7 (0.0 to 37.5) p52 | 12.5 (0.0 to 30.0) p65 | 12.5 (0.0 to 30.0) p52 | 8.3 (0.0 to 26.7) p72 |
| KSC | 11 | 63 | 15.3 (6.8 to 22.7) p39 | 11.1 (4.8 to 17.0) p50 | 6.8 (2.0 to 12.5) p22 | 1.6 (0.0 to 4.8) p0 |
| *VRTUS | 11 | 82 | 9.8 (3.4 to 16.7) p11 | 8.5 (1.1 to 16.9) p26 | 6.1 (1.9 to 10.1) p9 | 4.9 (0.0 to 10.8) p22 |
| 5D | 10 | 37 | 37.8 (24.1 to 48.8) p87 | 32.4 (20.9 to 43.8) p100 | 32.4 (21.6 to 41.2) p87 | 27.0 (18.8 to 35.3) p96 |
| BONKY | 7 | 36 | 22.2 (8.5 to 38.5) p70 | 11.1 (3.3 to 19.4) p50 | 19.4 (6.2 to 37.9) p74 | 8.3 (0.0 to 16.7) p72 |
| KSE | 7 | 20 | 45.0 (29.2 to 68.4) p96 | 15.0 (4.5 to 27.3) p83 | 40.0 (19.2 to 66.7) p100 | 10.0 (0.0 to 25.0) p78 |
| MACH | 7 | 29 | 27.6 (11.4 to 52.4) p78 | 6.9 (0.0 to 18.2) p13 | 24.1 (11.4 to 42.9) p78 | 6.9 (0.0 to 18.2) p57 |
| NGA | 7 | 28 | 25.0 (11.1 to 38.5) p74 | 14.3 (6.5 to 22.2) p78 | 17.9 (6.9 to 29.6) p70 | 10.7 (3.4 to 17.9) p83 |
| PN | 7 | 14 | 50.0 (20.0 to 75.0) p100 | 28.6 (7.1 to 50.0) p96 | 28.6 (11.1 to 50.0) p83 | 7.1 (0.0 to 22.2) p61 |
| RSR | 7 | 26 | 38.5 (27.3 to 50.0) p91 | 19.2 (0.0 to 32.1) p87 | 38.5 (27.3 to 50.0) p96 | 19.2 (0.0 to 32.1) p91 |
| SCCC2 | 7 | 48 | 10.4 (3.7 to 19.6) p22 | 10.4 (3.7 to 19.6) p43 | 6.2 (1.8 to 12.5) p13 | 6.2 (1.8 to 12.5) p43 |
| UYSC | 7 | 36 | 33.3 (17.2 to 53.3) p83 | 27.8 (9.4 to 50.0) p91 | 33.3 (17.2 to 53.3) p91 | 27.8 (9.4 to 50.0) p100 |
| BTLST (flag) | 6 | 34 | 26.5 (10.0 to 55.6) p76 | 23.5 (9.1 to 50.0) p89 | 26.5 (10.0 to 55.6) p80 | 17.6 (5.4 to 37.0) p89 |
| INCA (flag) | 6 | 39 | 12.8 (8.7 to 22.2) p33 | 7.7 (1.8 to 18.8) p17 | 12.8 (8.7 to 22.2) p59 | 7.7 (1.8 to 18.8) p63 |
| MANBA (flag) | 6 | 9 | 22.2 (0.0 to 40.0) p70 | 22.2 (0.0 to 40.0) p89 | 0.0 (0.0 to 0.0) p0 | 0.0 (0.0 to 0.0) p0 |
| OGF (flag) | 6 | 9 | 66.7 (54.5 to 85.7) p100 | 33.3 (9.1 to 71.4) p100 | 55.6 (37.5 to 75.0) p100 | 22.2 (0.0 to 54.5) p93 |
| RMN (flag) | 6 | 12 | 33.3 (18.2 to 50.0) p83 | 33.3 (18.2 to 50.0) p100 | 25.0 (9.1 to 45.5) p80 | 25.0 (9.1 to 45.5) p93 |
| KM (flag) | 5 | 15 | 20.0 (0.0 to 30.0) p63 | 13.3 (0.0 to 25.0) p72 | 13.3 (0.0 to 25.0) p59 | 13.3 (0.0 to 25.0) p89 |

Caps from the timeline, per clan: value (95% interval), percentile, n = smokes the rate applies to.

| Clan | Nearest cap taken % | Contested cap taken % | Nearest cap not lost % | Contested cap not lost % | Nearest caps taken per game | Contested caps taken per game |
|---|---|---|---|---|---|---|
| *RESIN | 32 (22 to 45) p57, n 56 | 27 (19 to 37) p57, n 70 | 75 (60 to 92) p10, n 32 | 74 (62 to 87) p20, n 38 | 0.7 (0.5 to 0.9) p52 | 0.7 (0.5 to 0.9) p52 |
| *H-SR | 56 (46 to 69) p100, n 50 | 42 (33 to 52) p96, n 65 | 86 (74 to 96) p50, n 37 | 86 (73 to 96) p70, n 44 | 1.1 (0.9 to 1.5) p96 | 1.1 (0.8 to 1.4) p91 |
| *BONKZ | 53 (35 to 72) p96, n 45 | 44 (30 to 62) p100, n 61 | 88 (80 to 97) p65, n 43 | 83 (73 to 93) p55, n 48 | 1.0 (0.7 to 1.3) p87 | 1.1 (0.8 to 1.4) p98 |
| MZY | 39 (18 to 62) p83, n 31 | 33 (15 to 53) p87, n 33 | 79 (62 to 100) p20, n 14, small n | 79 (58 to 100) p42, n 14, small n | 0.5 (0.2 to 0.9) p26 | 0.5 (0.2 to 0.8) p22 |
| *HTDOG | 30 (17 to 48) p48, n 53 | 27 (15 to 40) p52, n 60 | 85 (66 to 100) p40, n 33 | 88 (72 to 100) p80, n 41 | 0.7 (0.4 to 1.1) p65 | 0.7 (0.4 to 1.1) p70 |
| EPOXY | 36 (21 to 55) p78, n 36 | 30 (18 to 45) p74, n 50 | 76 (66 to 88) p15, n 29 | 69 (55 to 83) p15, n 29 | 0.6 (0.4 to 0.9) p48 | 0.7 (0.4 to 1.0) p48 |
| HFANS | 28 (19 to 39) p39, n 61 | 21 (13 to 31) p39, n 76 | 82 (71 to 94) p35, n 40 | 77 (61 to 90) p30, n 35 | 0.9 (0.6 to 1.2) p83 | 0.8 (0.5 to 1.2) p78 |
| -BN- | 31 (18 to 46) p52, n 54 | 29 (16 to 44) p65, n 63 | 96 (90 to 100) p95, n 26 | 84 (67 to 96) p60, n 25 | 1.1 (0.6 to 1.5) p91 | 1.1 (0.6 to 1.6) p98 |
| *KITE | 45 (25 to 65) p91, n 22 | 38 (19 to 60) p91, n 26 | 88 (58 to 100) p58, n 16 | 88 (57 to 100) p75, n 16 | 0.6 (0.3 to 1.1) p43 | 0.6 (0.3 to 1.1) p43 |
| KITED | 25 (11 to 41) p35, n 32 | 15 (7 to 28) p22, n 46 | 96 (89 to 100) p90, n 23 | 94 (83 to 100) p95, n 18 | 0.6 (0.3 to 0.9) p33 | 0.5 (0.2 to 0.8) p26 |
| MACHX | 36 (21 to 51) p74, n 53 | 28 (16 to 44) p61, n 61 | 81 (63 to 95) p25, n 27 | 80 (65 to 94) p50, n 25 | 1.1 (0.7 to 1.6) p100 | 1.1 (0.6 to 1.6) p87 |
| REEEE | 23 (4 to 38) p22, n 30 | 20 (3 to 33) p35, n 35 | 71 (41 to 94) p5, n 17 | 65 (38 to 89) p10, n 20 | 0.4 (0.1 to 0.8) p17 | 0.4 (0.1 to 0.8) p17 |
| PFANS | 24 (8 to 43) p28, n 17 | 19 (6 to 38) p30, n 21 | 62 (25 to 100) p0, n 8, small n | 50 (14 to 88) p0, n 8, small n | 0.3 (0.1 to 0.6) p13 | 0.3 (0.1 to 0.6) p13 |
| KSC | 29 (17 to 45) p43, n 34 | 25 (16 to 33) p46, n 44 | 89 (77 to 100) p70, n 18 | 78 (58 to 94) p35, n 18 | 0.8 (0.5 to 1.2) p72 | 0.9 (0.6 to 1.2) p83 |
| *VRTUS | 24 (14 to 40) p28, n 51 | 18 (11 to 31) p26, n 60 | 93 (85 to 100) p85, n 28 | 85 (75 to 100) p65, n 26 | 0.8 (0.5 to 1.1) p72 | 0.7 (0.5 to 1.0) p74 |
| 5D | 35 (19 to 57) p65, n 23 | 32 (17 to 53) p80, n 25 | 82 (47 to 100) p30, n 17 | 76 (42 to 100) p25, n 17 | 0.6 (0.3 to 0.9) p39 | 0.6 (0.3 to 0.9) p39 |
| BONKY | 9 (0 to 23) p0, n 23 | 14 (5 to 24) p15, n 28 | 88 (50 to 100) p58, n 8, small n | 89 (57 to 100) p90, n 9, small n | 0.3 (0.0 to 0.6) p7 | 0.6 (0.1 to 1.0) p33 |
| KSE | 33 (13 to 54) p61, n 15 | 29 (12 to 44) p70, n 17 | too few (n 7) | too few (n 6) | 0.7 (0.3 to 1.0) p59 | 0.7 (0.3 to 1.0) p61 |
| MACH | 16 (0 to 25) p13, n 19 | 11 (0 to 25) p9, n 19 | 100 (100 to 100) p100, n 12, small n | 100 (100 to 100) p100, n 13, small n | 0.4 (0.0 to 0.9) p22 | 0.3 (0.0 to 0.7) p9 |
| NGA | 10 (0 to 35) p4, n 20 | 4 (0 to 14) p0, n 23 | too few (n 7) | too few (n 7) | 0.3 (0.0 to 0.9) p7 | 0.1 (0.0 to 0.4) p2 |
| PN | 12 (0 to 67) p9, n 8, small n | 8 (0 to 33) p4, n 12, small n | too few (n 5) | too few (n 4) | 0.1 (0.0 to 0.4) p0 | 0.1 (0.0 to 0.4) p2 |
| RSR | 36 (18 to 53) p70, n 14, small n | 25 (8 to 50) p46, n 20 | 91 (50 to 100) p78, n 11, small n | 62 (33 to 89) p5, n 8, small n | 0.7 (0.3 to 1.3) p59 | 0.7 (0.3 to 1.3) p61 |
| SCCC2 | 16 (3 to 41) p17, n 25 | 14 (3 to 33) p15, n 28 | 91 (75 to 100) p78, n 22 | 88 (76 to 100) p85, n 25 | 0.6 (0.1 to 1.1) p33 | 0.6 (0.1 to 1.1) p33 |
| UYSC | 43 (22 to 59) p87, n 23 | 32 (8 to 55) p80, n 25 | 86 (64 to 100) p45, n 14, small n | 79 (55 to 100) p42, n 14, small n | 0.9 (0.3 to 1.4) p78 | 0.7 (0.1 to 1.4) p61 |
| BTLST (flag) | 33 (13 to 54) p61, n 18 | 26 (10 to 47) p50, n 23 | 69 (47 to 100) p2, n 13, small n | 57 (31 to 85) p2, n 14, small n | 0.8 (0.3 to 1.3) p76 | 0.8 (0.3 to 1.3) p80 |
| INCA (flag) | 41 (29 to 67) p85, n 17 | 35 (25 to 47) p89, n 20 | 82 (67 to 94) p30, n 17 | 69 (45 to 89) p12, n 16 | 1.0 (0.5 to 1.5) p87 | 1.0 (0.5 to 1.5) p85 |
| MANBA (flag) | too few (n 4) | too few (n 6) | too few (n 4) | too few (n 3) | 0.2 (0.0 to 0.5) p2 | 0.3 (0.0 to 0.7) p13 |
| OGF (flag) | too few (n 7) | 0 (0 to 0) p0, n 8, small n | too few (n 4) | too few (n 5) | 0.0 (0.0 to 0.0) p0 | 0.0 (0.0 to 0.0) p0 |
| RMN (flag) | too few (n 6) | 10 (0 to 38) p7, n 10, small n | too few (n 4) | too few (n 2) | 0.2 (0.0 to 0.5) p2 | 0.2 (0.0 to 0.5) p7 |
| KM (flag) | too few (n 6) | 7 (0 to 27) p2, n 14, small n | too few (n 5) | too few (n 0) | 0.4 (0.0 to 0.8) p20 | 0.2 (0.0 to 0.6) p7 |

Smokes the cap rates apply to, all clans: nearest cap taken 853, contested cap taken 1,049, nearest cap not lost 541, contested cap not lost 548 (of 1,547).

**Top 6 or Shared:** Top 6 minus Rest on the "what it buys" scores (pooled over each group's games; 95% interval, whole clans resampled).

| Score | Top 6 | Rest | n (Top 6 / Rest) | Gap (95%) | Reading | Same gap with the library helper `boot_diff` |
|---|---|---|---|---|---|---|
| Concealed damage per smoke | 11,685 | 8,515 | 110 / 232 games | +570.1 to +5,690.5 * | Top 6 | - |
| Concealed damage per game | 57,152 | 37,034 | 110 / 232 games | +5,334.5 to +33,896.9 * | Top 6 | - |
| Nearest cap taken (% of smokes where it was not ours) | 39 | 28 | 277 / 576 | +0.5 to +21.5 * | Top 6 | +0.0 to +22.5 * |
| Contested cap taken (% of smokes where it was not ours) | 32 | 23 | 342 / 707 | +1.1 to +17.6 * | Top 6 | +1.5 to +18.4 * |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 86 | 83 | 189 / 352 | -3.3 to +8.6 | Shared | -3.4 to +9.3 |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 84 | 76 | 213 / 335 | +1.9 to +15.3 * | Top 6 | +1.2 to +13.7 * |
| Died per 100 smokes | 12.3 | 19.3 | 538 / 1000 | -13.3 to -2.6 * | Top 6 | -13.1 to -1.9 * |
| Caught per 100 smokes | 7.8 | 13.4 | 538 / 1009 | -9.5 to -2.9 * | Top 6 | -9.2 to -2.3 * |
| Smoker died per 100 smokes | 8.2 | 15.1 | 538 / 1000 | -12.3 to -3.2 * | Top 6 | -12.2 to -2.9 * |
| Smoker caught per 100 smokes | 4.3 | 9.2 | 538 / 1009 | -8.6 to -2.5 * | Top 6 | -8.4 to -2.1 * |
| Nearest caps taken with a smoke per game | 0.8 | 0.6 | 110 / 232 games | +0.04 to +0.44 * | Top 6 | - |
| Contested caps taken with a smoke per game | 0.9 | 0.6 | 110 / 232 games | +0.05 to +0.46 * | Top 6 | - |
| Ships died per game | 0.6 | 0.8 | 110 / 232 games | -0.49 to -0.03 * | Top 6 | - |
| Ships caught per game | 0.4 | 0.6 | 110 / 232 games | -0.37 to -0.06 * | Top 6 | - |

- Deaths: Top 6 clearly lower on all four. Died per 100: 12.3 against 19.3 (-13.3 to -2.6 *). Caught per 100: 7.8 against 13.4 (-9.5 to -2.9 *). Smoker only: died 8.2 against 15.1 (-12.3 to -3.2 *); caught 4.3 against 9.2 (-8.6 to -2.5 *).
- Caps taken: nearest cap 39% against 28% (+0.5 to +21.5 *); contested cap 32% against 23% (+1.1 to +17.6 *). Clear: Nearest cap taken (% of smokes where it was not ours), Contested cap taken (% of smokes where it was not ours), Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's), Nearest caps taken with a smoke per game, Contested caps taken with a smoke per game. Shared: Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's).
- Cap not lost: nearest cap 86% against 83% (-3.3 to +8.6); contested cap 84% against 76% (+1.9 to +15.3 *).
- Concealed damage is unchanged: per smoke 11,685 against 8,515 (+570.1 to +5,690.5 *); per game 57,152 against 37,034 (+5,334.5 to +33,896.9 *).
- Every other Top 6 minus Rest gap (25 scores: lineup, who, where, movement, concealed damage) is identical to round 5b. The gaps that moved are listed under "Changed from round 5b".

**Clans:** Top 6 and PN on the new scores (value, 95% interval, percentile).

| Clan | Died per 100 | Caught per 100 | Smoker died per 100 | Smoker caught per 100 | Nearest cap taken % | Contested cap taken % | Nearest cap not lost % | Contested cap not lost % |
|---|---|---|---|---|---|---|---|---|
| *H-SR | 6.0 (1.2 to 11.2) p0 | 4.0 (0.0 to 8.9) p0 | 4.0 (0.9 to 7.5) p4 | 2.0 (0.0 to 4.9) p9 | 56 (46 to 69) p100, n 50 | 42 (33 to 52) p96, n 65 | 86 (74 to 96) p50, n 37 | 86 (73 to 96) p70, n 44 |
| *RESIN | 17.5 (9.9 to 25.6) p57 | 7.8 (2.9 to 13.3) p22 | 9.7 (5.3 to 14.5) p39 | 1.9 (0.0 to 4.9) p4 | 32 (22 to 45) p57, n 56 | 27 (19 to 37) p57, n 70 | 75 (60 to 92) p10, n 32 | 74 (62 to 87) p20, n 38 |
| *BONKZ | 17.6 (10.3 to 25.8) p61 | 11.8 (5.9 to 17.8) p57 | 12.7 (6.9 to 20.0) p57 | 6.9 (2.4 to 12.7) p52 | 53 (35 to 72) p96, n 45 | 44 (30 to 62) p100, n 61 | 88 (80 to 97) p65, n 43 | 83 (73 to 93) p55, n 48 |
| *HTDOG | 10.4 (4.1 to 17.4) p17 | 6.6 (2.1 to 12.2) p9 | 8.5 (3.4 to 15.0) p30 | 5.7 (1.9 to 10.4) p30 | 30 (17 to 48) p48, n 53 | 27 (15 to 40) p52, n 60 | 85 (66 to 100) p40, n 33 | 88 (72 to 100) p80, n 41 |
| *KITE | 11.1 (2.6 to 21.2) p26 | 8.9 (2.4 to 15.9) p30 | 6.7 (0.0 to 16.7) p17 | 4.4 (0.0 to 10.8) p17 | 45 (25 to 65) p91, n 22 | 38 (19 to 60) p91, n 26 | 88 (58 to 100) p58, n 16 | 88 (57 to 100) p75, n 16 |
| *VRTUS | 9.8 (3.4 to 16.7) p11 | 8.5 (1.1 to 16.9) p26 | 6.1 (1.9 to 10.1) p9 | 4.9 (0.0 to 10.8) p22 | 24 (14 to 40) p28, n 51 | 18 (11 to 31) p26, n 60 | 93 (85 to 100) p85, n 28 | 85 (75 to 100) p65, n 26 |
| PN | 50.0 (20.0 to 75.0) p100 | 28.6 (7.1 to 50.0) p96 | 28.6 (11.1 to 50.0) p83 | 7.1 (0.0 to 22.2) p61 | 12 (0 to 67) p9, n 8, small n | 8 (0 to 33) p4, n 12, small n | too few (n 5) | too few (n 4) |

**Could not be done / proxy:**
- Rates with fewer than 8 cases are "too few": nearest cap taken: MANBA (n 4), OGF (n 7), RMN (n 6), KM (n 6); contested cap taken: MANBA (n 6); nearest cap not lost: KSE (n 7), NGA (n 7), PN (n 5), MANBA (n 4), OGF (n 4), RMN (n 4), KM (n 5); contested cap not lost: KSE (n 6), NGA (n 7), PN (n 4), MANBA (n 3), OGF (n 5), RMN (n 2), KM (n 0).
- "Died" cannot be judged for 9 smokes (-BN-, KSC, one game with a single replay); those clans' "died" rates use their other smokes.
- A clan interval comes from 7 to 24 games, so it is wide: read a clan's death score with its interval, not as a ranking.
- "Caps taken per game" counts each cap once per game when a smoke of the clan stood near it as it changed hands; it is not all caps the clan took.

**Verdict:** Keep

**Changed from round 5b:**

Scores replaced (old score -> new score, why):

| Round 5b score | Round 5c score | Why |
|---|---|---|
| Deaths per 100 smokes (`deaths_per100`) | Caught per 100 smokes (same numbers) plus Died per 100 smokes; smoker-only versions of both | new death metric |
| Deaths in or behind smoke per game (`deaths_pg`) | Ships caught per game (same numbers) plus Ships died per game | new death metric |
| Nearest cap taken % (`took_pct`, snapshots) | Nearest cap taken % and Contested cap taken % (timeline) | cap timeline |
| Nearest cap not lost % (`held_pct`, snapshots) | Nearest cap not lost % and Contested cap not lost % (timeline) | cap timeline |
| Caps taken next to a smoke per game (`caps_taken_pg`, snapshots) | Nearest caps taken with a smoke per game (same key) and Contested caps taken per game (timeline) | cap timeline |
| `cap_won_pg`, `cap_def_pg` (batch flags) | dropped | not to be used |
| First smoke of the game, Smokes after 12:00, Smokes before 5:00 (HUD clock) | same scores on the replay clock | clock (`e0` instead of `el`) |

Check: "caught per 100" equals round 5b's deaths per 100 for all 30 clans, and its Top 6 minus Rest interval is the same (-9.5 to -2.9 * then, -9.5 to -2.9 * now).

Top 6 clans and PN, every per-clan score that was replaced or moved: round 5b value and percentile -> round 5c value and percentile.

| Score (round 5b -> round 5c) | *H-SR | *RESIN | *BONKZ | *HTDOG | *KITE | *VRTUS | PN | Why |
|---|---|---|---|---|---|---|---|---|
| Deaths per 100 smokes -> Died per 100 smokes | 4.0 p0 -> 6.0 p0 | 7.8 p22 -> 17.5 p57 | 11.8 p57 -> 17.6 p61 | 6.6 p9 -> 10.4 p17 | 8.9 p30 -> 11.1 p26 | 8.5 p26 -> 9.8 p11 | 28.6 p96 -> 50.0 p100 | new death metric |
| Deaths per 100 smokes -> Caught per 100 smokes | 4.0 p0 -> 4.0 p0 (same) | 7.8 p22 -> 7.8 p22 (same) | 11.8 p57 -> 11.8 p57 (same) | 6.6 p9 -> 6.6 p9 (same) | 8.9 p30 -> 8.9 p30 (same) | 8.5 p26 -> 8.5 p26 (same) | 28.6 p96 -> 28.6 p96 (same) | unchanged |
| Smoker died per 100 smokes | new: 4.0 p4 | new: 9.7 p39 | new: 12.7 p57 | new: 8.5 p30 | new: 6.7 p17 | new: 6.1 p9 | new: 28.6 p83 | new death metric (no round 5b score) |
| Smoker caught per 100 smokes | new: 2.0 p9 | new: 1.9 p4 | new: 6.9 p52 | new: 5.7 p30 | new: 4.4 p17 | new: 4.9 p22 | new: 7.1 p61 | new split (no round 5b score) |
| Nearest cap taken (% of smokes where it was not ours) (snapshots -> timeline) | 38.0 p96 -> 56.0 p100 | 17.5 p35 -> 32.1 p57 | 42.2 p100 -> 53.3 p96 | 24.5 p52 -> 30.2 p48 | 31.8 p78 -> 45.5 p91 | 21.6 p43 -> 23.5 p28 | 12.5 p17 -> 12.5 p9 | cap timeline |
| Contested cap taken (% of smokes where it was not ours) | new: 41.5 p96 | new: 27.1 p57 | new: 44.3 p100 | new: 26.7 p52 | new: 38.5 p91 | new: 18.3 p26 | new: 8.3 p4 | cap timeline (no round 5b score) |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (snapshots -> timeline) | 89.2 p55 -> 86.5 p50 | 87.5 p30 -> 75.0 p10 | 93.0 p70 -> 88.4 p65 | 97.0 p95 -> 84.8 p40 | 93.8 p75 -> 87.5 p58 | 92.9 p65 -> 92.9 p85 | too few -> too few (same) | cap timeline |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 86.4 p70 | new: 73.7 p20 | new: 83.3 p55 | new: 87.8 p80 | new: 87.5 p75 | new: 84.6 p65 | new: too few | cap timeline (no round 5b score) |
| Nearest caps taken with a smoke per game | 0.77 p87 -> 1.14 p96 | 0.33 p26 -> 0.67 p52 | 0.81 p91 -> 1.00 p87 | 0.67 p70 -> 0.72 p65 | 0.50 p43 -> 0.64 p43 | 0.73 p83 -> 0.82 p72 | 0.14 p2 -> 0.14 p0 | cap timeline |
| Contested caps taken with a smoke per game | new: 1.09 p91 | new: 0.71 p52 | new: 1.14 p98 | new: 0.72 p70 | new: 0.64 p43 | new: 0.73 p74 | new: 0.14 p2 | cap timeline (no round 5b score) |
| Deaths in or behind smoke per game -> Ships died per game | 0.18 p0 -> 0.27 p0 | 0.33 p22 -> 0.75 p48 | 0.57 p52 -> 0.86 p61 | 0.39 p35 -> 0.61 p26 | 0.29 p11 -> 0.36 p13 | 0.64 p72 -> 0.73 p43 | 0.57 p52 -> 1.00 p72 | new death metric |
| Deaths in or behind smoke per game -> Ships caught per game | 0.18 p0 -> 0.18 p0 (same) | 0.33 p22 -> 0.33 p22 (same) | 0.57 p52 -> 0.57 p52 (same) | 0.39 p35 -> 0.39 p35 (same) | 0.29 p11 -> 0.29 p11 (same) | 0.64 p72 -> 0.64 p72 (same) | 0.57 p52 -> 0.57 p52 (same) | unchanged |
| First smoke of the game (median, s) | 120.5 s p0 -> 120.1 s p0 | 174.0 s p35 -> 173.4 s p35 | 198.0 s p65 -> 197.4 s p65 | 233.0 s p91 -> 232.4 s p91 | 150.0 s p22 -> 149.2 s p22 | 224.0 s p87 -> 222.8 s p87 | 221.5 s p78 -> 221.0 s p78 | clock |
| Smokes after 12:00 (%) | 8.0 p30 -> 7.0 p26 | 19.4 p91 -> 19.4 p91 (same) | 13.7 p65 -> 13.7 p65 (same) | 17.9 p83 -> 16.0 p78 | 8.9 p48 -> 8.9 p48 (same) | 14.6 p70 -> 14.6 p70 (same) | 7.1 p26 -> 7.1 p30 | clock |
| Smokes before 5:00 (%) | 31.0 p83 -> 32.0 p83 | 28.2 p65 -> 28.2 p65 (same) | 22.5 p26 -> 22.5 p22 | 23.6 p30 -> 23.6 p26 | 24.4 p39 -> 24.4 p39 (same) | 18.3 p0 -> 18.3 p0 (same) | 50.0 p100 -> 50.0 p100 (same) | clock |

Top 6 clans and PN, 95% intervals of the same scores (round 5b -> round 5c).

| Score | *H-SR | *RESIN | *BONKZ | *HTDOG | *KITE | *VRTUS | PN |
|---|---|---|---|---|---|---|---|
| Died per 100 smokes | 0.0 to 8.9 -> 1.2 to 11.2 | 2.9 to 13.3 -> 9.9 to 25.6 | 5.9 to 17.8 -> 10.3 to 25.8 | 2.1 to 12.2 -> 4.1 to 17.4 | 2.4 to 15.9 -> 2.6 to 21.2 | 1.1 to 16.9 -> 3.4 to 16.7 | 7.1 to 50.0 -> 20.0 to 75.0 |
| Caught per 100 smokes | 0.0 to 8.9 -> 0.0 to 8.9 | 2.9 to 13.3 -> 2.9 to 13.3 | 5.9 to 17.8 -> 5.9 to 17.8 | 2.1 to 12.2 -> 2.1 to 12.2 | 2.4 to 15.9 -> 2.4 to 15.9 | 1.1 to 16.9 -> 1.1 to 16.9 | 7.1 to 50.0 -> 7.1 to 50.0 |
| Smoker died per 100 smokes | new: 0.9 to 7.5 | new: 5.3 to 14.5 | new: 6.9 to 20.0 | new: 3.4 to 15.0 | new: 0.0 to 16.7 | new: 1.9 to 10.1 | new: 11.1 to 50.0 |
| Smoker caught per 100 smokes | new: 0.0 to 4.9 | new: 0.0 to 4.9 | new: 2.4 to 12.7 | new: 1.9 to 10.4 | new: 0.0 to 10.8 | new: 0.0 to 10.8 | new: 0.0 to 22.2 |
| Nearest cap taken (% of smokes where it was not ours) | 23.1 to 55.3 -> 46.0 to 69.2 | 8.3 to 26.5 -> 22.0 to 45.5 | 26.2 to 58.3 -> 35.5 to 72.4 | 12.8 to 39.4 -> 16.9 to 47.5 | 12.5 to 50.0 -> 25.0 to 65.2 | 12.2 to 37.5 -> 13.8 to 40.0 | 0.0 to 66.7 -> 0.0 to 66.7 |
| Contested cap taken (% of smokes where it was not ours) | new: 33.3 to 51.7 | new: 18.8 to 37.3 | new: 29.9 to 62.1 | new: 15.1 to 40.0 | new: 19.0 to 60.0 | new: 11.1 to 31.0 | new: 0.0 to 33.3 |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 77.8 to 97.6 -> 74.2 to 96.2 | 76.5 to 96.9 -> 60.0 to 91.7 | 86.8 to 100.0 -> 80.0 to 96.8 | 89.3 to 100.0 -> 65.5 to 100.0 | 72.7 to 100.0 -> 58.3 to 100.0 | 84.9 to 100.0 -> 84.9 to 100.0 | too few -> too few |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 73.3 to 95.7 | new: 62.2 to 86.7 | new: 73.5 to 92.7 | new: 71.8 to 100.0 | new: 57.1 to 100.0 | new: 75.0 to 100.0 | new: too few |
| Nearest caps taken with a smoke per game | 0.50 to 1.05 -> 0.86 to 1.45 | 0.17 to 0.54 -> 0.46 to 0.88 | 0.52 to 1.10 -> 0.67 to 1.33 | 0.33 to 1.00 -> 0.39 to 1.06 | 0.14 to 0.93 -> 0.29 to 1.07 | 0.36 to 1.09 -> 0.45 to 1.09 | 0.00 to 0.43 -> 0.00 to 0.43 |
| Contested caps taken with a smoke per game | new: 0.77 to 1.41 | new: 0.50 to 0.92 | new: 0.81 to 1.43 | new: 0.39 to 1.06 | new: 0.29 to 1.07 | new: 0.45 to 1.00 | new: 0.00 to 0.43 |
| Ships died per game | 0.00 to 0.41 -> 0.05 to 0.50 | 0.12 to 0.54 -> 0.42 to 1.08 | 0.29 to 0.90 -> 0.48 to 1.29 | 0.11 to 0.72 -> 0.22 to 1.00 | 0.07 to 0.50 -> 0.07 to 0.71 | 0.09 to 1.36 -> 0.27 to 1.27 | 0.14 to 1.14 -> 0.29 to 1.71 |
| Ships caught per game | 0.00 to 0.41 -> 0.00 to 0.41 | 0.12 to 0.54 -> 0.12 to 0.54 | 0.29 to 0.90 -> 0.29 to 0.90 | 0.11 to 0.72 -> 0.11 to 0.72 | 0.07 to 0.50 -> 0.07 to 0.50 | 0.09 to 1.36 -> 0.09 to 1.36 | 0.14 to 1.14 -> 0.14 to 1.14 |
| First smoke of the game (median, s) | 104.0 s to 163.0 s -> 102.7 s to 162.3 s | 122.0 s to 229.0 s -> 121.9 s to 229.0 s | 163.0 s to 280.0 s -> 162.4 s to 279.4 s | 170.0 s to 265.0 s -> 169.4 s to 264.4 s | 98.0 s to 296.0 s -> 97.7 s to 295.3 s | 160.0 s to 283.0 s -> 158.9 s to 282.7 s | 145.0 s to 520.0 s -> 143.9 s to 519.7 s |
| Smokes after 12:00 (%) | 2.7 to 14.3 -> 2.2 to 13.3 | 10.4 to 30.1 -> 10.4 to 30.1 | 6.5 to 21.7 -> 6.5 to 21.7 | 8.0 to 29.6 -> 6.6 to 27.0 | 2.4 to 17.6 -> 2.4 to 17.6 | 3.6 to 23.1 -> 3.6 to 23.1 | 0.0 to 27.3 -> 0.0 to 27.3 |
| Smokes before 5:00 (%) | 25.3 to 36.8 -> 26.5 to 37.7 | 22.7 to 34.6 -> 22.7 to 34.6 | 17.7 to 26.8 -> 17.7 to 26.8 | 17.6 to 30.5 -> 17.6 to 30.5 | 18.9 to 29.8 -> 18.9 to 29.8 | 10.5 to 28.3 -> 10.5 to 28.3 | 25.0 to 78.6 -> 25.0 to 78.6 |

The other 23 clans. Replaced scores (round 5b -> round 5c); "died" is new, "caught" is the old deaths number.

| Clan | Deaths per 100 -> Died per 100 | Caught per 100 (was Deaths per 100) | Nearest cap taken % (snapshots -> timeline) | Nearest cap not lost % (snapshots -> timeline) | Caps taken per game (snapshots -> timeline) |
|---|---|---|---|---|---|
| MZY | 14.0 -> 22.0 | 14.0 (same) | 29.0 -> 38.7 | 78.6 -> 78.6 | 0.37 -> 0.53 |
| EPOXY | 12.2 -> 15.9 | 12.2 (same) | 30.6 -> 36.1 | 82.8 -> 75.9 | 0.59 -> 0.65 |
| HFANS | 10.0 -> 13.6 | 10.0 (same) | 26.2 -> 27.9 | 85.0 -> 82.5 | 0.82 -> 0.88 |
| -BN- | 9.9 -> 11.6 | 9.9 (same) | 22.2 -> 31.5 | 96.2 -> 96.2 | 0.71 -> 1.07 |
| KITED | 12.7 -> 15.9 | 12.7 (same) | 25.0 -> 25.0 | 95.7 -> 95.7 | 0.57 -> 0.57 |
| MACHX | 6.1 -> 9.8 | 6.1 (same) | 32.1 -> 35.8 | 88.9 -> 81.5 | 1.07 -> 1.14 |
| REEEE | 7.7 -> 7.7 | 7.7 (same) | 13.3 -> 23.3 | 70.6 -> 70.6 | 0.23 -> 0.38 |
| PFANS | 12.5 -> 16.7 | 12.5 (same) | 11.8 -> 23.5 | 87.5 -> 62.5 | 0.17 -> 0.33 |
| KSC | 11.1 -> 15.3 | 11.1 (same) | 20.6 -> 29.4 | 88.9 -> 88.9 | 0.55 -> 0.82 |
| 5D | 32.4 -> 37.8 | 32.4 (same) | 34.8 -> 34.8 | 88.2 -> 82.4 | 0.60 -> 0.60 |
| BONKY | 11.1 -> 22.2 | 11.1 (same) | 4.3 -> 8.7 | 87.5 -> 87.5 | 0.14 -> 0.29 |
| KSE | 15.0 -> 45.0 | 15.0 (same) | 13.3 -> 33.3 | too few -> too few | 0.29 -> 0.71 |
| MACH | 6.9 -> 27.6 | 6.9 (same) | 15.8 -> 15.8 | 100.0 -> 100.0 | 0.43 -> 0.43 |
| NGA | 14.3 -> 25.0 | 14.3 (same) | 10.0 -> 10.0 | too few -> too few | 0.29 -> 0.29 |
| RSR | 19.2 -> 38.5 | 19.2 (same) | 35.7 -> 35.7 | 90.9 -> 90.9 | 0.71 -> 0.71 |
| SCCC2 | 10.4 -> 10.4 | 10.4 (same) | 12.0 -> 16.0 | 95.5 -> 90.9 | 0.43 -> 0.57 |
| UYSC | 27.8 -> 33.3 | 27.8 (same) | 26.1 -> 43.5 | 85.7 -> 85.7 | 0.57 -> 0.86 |
| BTLST (flag) | 23.5 -> 26.5 | 23.5 (same) | 33.3 -> 33.3 | 92.3 -> 69.2 | 0.83 -> 0.83 |
| INCA (flag) | 7.7 -> 12.8 | 7.7 (same) | 31.2 -> 41.2 | 82.4 -> 82.4 | 0.67 -> 1.00 |
| MANBA (flag) | 22.2 -> 22.2 | 22.2 (same) | too few -> too few | too few -> too few | 0.00 -> 0.17 |
| OGF (flag) | 33.3 -> 66.7 | 33.3 (same) | too few -> too few | too few -> too few | 0.00 -> 0.00 |
| RMN (flag) | 33.3 -> 33.3 | 33.3 (same) | too few -> too few | too few -> too few | 0.00 -> 0.17 |
| KM (flag) | 13.3 -> 20.0 | 13.3 (same) | too few -> too few | too few -> too few | 0.40 -> 0.40 |

Time scores, what the switch from the HUD clock to the replay clock moved: the first smoke of the game moves for all 30 clans, by 0.0 to 1.4 s (median 0.6 s; the replay clock is exact and the HUD clock is in whole seconds). Share after 12:00 moves for H-SR (8.0% -> 7.0%), HTDOG (17.9% -> 16.0%). Share before 5:00 moves for H-SR (31.0% -> 32.0%), KSC (22.2% -> 23.8%).
Other clans where a time score moved by more than a rounding step (1 s, or half a point): EPOXY First smoke of the game (median, s) 192.0 s -> 190.7 s; HFANS First smoke of the game (median, s) 143.0 s -> 142.0 s; MACHX First smoke of the game (median, s) 146.0 s -> 144.6 s; PFANS First smoke of the game (median, s) 185.5 s -> 184.4 s; KSE First smoke of the game (median, s) 251.0 s -> 250.0 s; MANBA First smoke of the game (median, s) 315.0 s -> 313.9 s; KSC Smokes before 5:00 (%) 22.2 -> 23.8.

All Top 6 minus Rest gaps, round 5b and round 5c (Top 6 / Rest / 95% interval).

| Score | Round 5b | Round 5c | Why |
|---|---|---|---|
| Long-smoke destroyers per game (`long_ships_pg`) | 0.89 / 0.66 / -0.14 to +0.52 | 0.89 / 0.66 / -0.14 to +0.52 | unchanged |
| Cap-sitter destroyers per game (`sitter_ships_pg`) | 0.70 / 0.70 / -0.26 to +0.29 | 0.70 / 0.70 / -0.26 to +0.29 | unchanged |
| Destroyers carrying smoke per game (`smoke_dd_pg`) | 1.63 / 1.45 / -0.08 to +0.44 | 1.63 / 1.45 / -0.08 to +0.44 | unchanged |
| Cruisers carrying smoke per game (`smoke_cruisers_pg`) | 0.52 / 0.72 / -0.54 to +0.22 | 0.52 / 0.72 / -0.54 to +0.22 | unchanged |
| Exhaust-smoke ships per game (`exhaust_ships_pg`) | 0.23 / 0.62 / -0.62 to -0.21 * | 0.23 / 0.62 / -0.62 to -0.21 * | unchanged |
| Smokes per game (`smokes_pg`) | 4.89 / 4.35 / -0.43 to +1.58 | 4.89 / 4.35 / -0.43 to +1.58 | unchanged |
| First smoke of the game (median, s) (`first_smoke_s`) | 175.0 s / 196.5 s / -54.0 to +29.5 | 173.9 s / 196.1 s / -53.9 to +29.1 | clock |
| Smokes after 12:00 (%) (`late_pct`) | 14.3 / 11.1 / -1.6 to +7.8 | 13.8 / 11.1 / -2.3 to +7.3 | clock |
| For a teammate (%) (`teammate_pct`) | 63.8 / 54.8 / -2.5 to +20.2 | 63.8 / 54.8 / -2.5 to +20.2 | unchanged |
| Stacked on a teammate (%) (`stacked_pct`) | 31.6 / 23.5 / -3.0 to +18.4 | 31.6 / 23.5 / -3.0 to +18.4 | unchanged |
| Radar cruiser inside (% of destroyer smokes) (`radar_ca_inside_pct`) | 47.3 / 29.0 / +7.8 to +27.0 * | 47.3 / 29.0 / +7.8 to +27.0 * | unchanged |
| Median distance to cap edge (m) (`edge_m`) | 2,060 / 2,089 / -502.0 to +499.7 | 2,060 / 2,089 / -502.0 to +499.7 | unchanged |
| Inside a cap (%) (`inside_cap_pct`) | 22.9 / 24.2 / -7.7 to +4.2 | 22.9 / 24.2 / -7.7 to +4.2 | unchanged |
| Centre lane (%) (`centre_pct`) | 24.3 / 21.0 / -4.9 to +11.9 | 24.3 / 21.0 / -4.9 to +11.9 | unchanged |
| Pushing (%) (`pushing_pct`) | 20.8 / 20.3 / -4.1 to +4.6 | 20.8 / 20.3 / -4.1 to +4.6 | unchanged |
| Kiting (%) (`kiting_pct`) | 17.7 / 20.3 / -7.7 to +2.0 | 17.7 / 20.3 / -7.7 to +2.0 | unchanged |
| Parked (%) (`parked_pct`) | 28.8 / 27.5 / -11.4 to +13.5 | 28.8 / 27.5 / -11.4 to +13.5 | unchanged |
| Concealed damage per smoke (`conc_per_smoke`) | 11,685 / 8,515 / +570.1 to +5,690.5 * | 11,685 / 8,515 / +570.1 to +5,690.5 * | unchanged |
| Concealed damage per game (`conc_pg`) | 57,152 / 37,034 / +5,334.5 to +33,896.9 * | 57,152 / 37,034 / +5,334.5 to +33,896.9 * | unchanged |
| Nearest cap taken (% of smokes where it was not ours) (`took_pct`) | 28.4 / 22.6 / -2.2 to +14.6 | not in this round | dropped |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`held_pct`) | 92.1 / 87.2 / +0.6 to +9.5 * | not in this round | dropped |
| Deaths per 100 smokes (`deaths_per100`) | 7.8 / 13.4 / -9.5 to -2.9 * | not in this round | dropped |
| Svea or Jinan per game (`parked_cruisers_pg`) | 0.35 / 0.19 / -0.11 to +0.57 | 0.35 / 0.19 / -0.11 to +0.57 | unchanged |
| Ships carrying smoke per game (`smoke_ships_pg`) | 2.27 / 2.31 / -0.39 to +0.36 | 2.27 / 2.31 / -0.39 to +0.36 | unchanged |
| Destroyers per game (`dd_pg`) | 3.25 / 3.00 / +0.05 to +0.46 * | 3.25 / 3.00 / +0.05 to +0.46 * | unchanged |
| Radar ships per game (`radar_ships_pg`) | 3.57 / 3.01 / +0.20 to +0.84 * | 3.57 / 3.01 / +0.20 to +0.84 * | unchanged |
| Smokes before 5:00 (%) (`early_pct`) | 24.9 / 27.7 / -7.3 to +1.3 | 25.1 / 27.8 / -7.4 to +1.6 | clock |
| Selfish (%) (`selfish_pct`) | 36.2 / 45.2 / -20.4 to +2.1 | 36.2 / 45.2 / -20.4 to +2.1 | unchanged |
| Any cruiser inside (% of destroyer smokes) (`cruiser_inside_pct`) | 52.7 / 34.9 / +5.0 to +27.9 * | 52.7 / 34.9 / +5.0 to +27.9 * | unchanged |
| Own side of the front line (%) (`own_half_pct`) | 83.8 / 78.3 / +1.4 to +9.8 * | 83.8 / 78.3 / +1.4 to +9.8 * | unchanged |
| Sideways (%) (`sideways_pct`) | 26.0 / 25.5 / -9.4 to +8.7 | 26.0 / 25.5 / -9.4 to +8.7 | unchanged |
| Nearest caps taken with a smoke per game (`caps_taken_pg`) | 0.63 / 0.49 / -0.06 to +0.32 | 0.85 / 0.61 / +0.04 to +0.44 * | cap timeline |
| Smokes with the batch cap-won flag per game (`cap_won_pg`) | 1.20 / 0.81 / +0.15 to +0.61 * | not in this round | dropped |
| Batch cap-defended flag per game (secondary: fires for any owned cap with an enemy inside) (`cap_def_pg`) | 1.48 / 1.39 / -0.32 to +0.48 | not in this round | dropped |
| Deaths in or behind smoke per game (`deaths_pg`) | 0.38 / 0.58 / -0.37 to -0.06 * | not in this round | dropped |
| Nearest cap taken (% of smokes where it was not ours) (`we_took_n_pct`) | not in this round | 39.0 / 28.5 / +0.5 to +21.5 * | new |
| Contested cap taken (% of smokes where it was not ours) (`we_took_c_pct`) | not in this round | 32.2 / 22.8 / +1.1 to +17.6 * | new |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`not_lost_n_pct`) | not in this round | 85.7 / 83.0 / -3.3 to +8.6 | new |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) (`not_lost_c_pct`) | not in this round | 83.6 / 75.8 / +1.9 to +15.3 * | new |
| Died per 100 smokes (`died_per100`) | not in this round | 12.3 / 19.3 / -13.3 to -2.6 * | new |
| Caught per 100 smokes (`caught_per100`) | not in this round | 7.8 / 13.4 / -9.5 to -2.9 * | new |
| Smoker died per 100 smokes (`died_smoker_per100`) | not in this round | 8.2 / 15.1 / -12.3 to -3.2 * | new |
| Smoker caught per 100 smokes (`caught_smoker_per100`) | not in this round | 4.3 / 9.2 / -8.6 to -2.5 * | new |
| Contested caps taken with a smoke per game (`caps_taken_c_pg`) | not in this round | 0.86 / 0.60 / +0.05 to +0.46 * | new |
| Ships died per game (`died_pg`) | not in this round | 0.60 / 0.83 / -0.49 to -0.03 * | new |
| Ships caught per game (`caught_pg`) | not in this round | 0.38 / 0.58 / -0.37 to -0.06 * | new |

### D2. Group the clans; one scale or several styles?

**Answer:** No clan changes style. The grouping is built from 17 behaviour scores; only two of them changed at all (first smoke of the game and share after 12:00, now on the replay clock), and they moved by at most 1.4 s and one or two smokes. Clan positions shift by at most 0.02 on the first scale and 0.09 on the second. It is still two separate scales with four soft-bordered corners.

**Numbers:**
- Scores used: the same 17 as round 5b; no death or cap score is among them, so the new death and cap definitions cannot move the grouping. The two time scores are the only inputs that differ.
- Shares of the differences between clans: first scale 29.6% (round 5b 29.6%), second 17.8% (17.8%), third 11.5% (11.6%). Together the first two carry 47%. Shuffled data gives at most 19.1% and 15.7% (95th percentile), so both scales are real.
- Check that the rerun is the same method: run on the HUD clock, the script reproduces round 5b's clan positions exactly and the same four groups.
- Shape: on the first scale the largest gap between neighbours is 1.7 of a range of 8.6. On the second there is a break: 7 clans sit low (PN, MZY, 5D, KITED, NGA, KSE, PFANS; -1.6 or below) and everyone else is at +0.0 or above.
- Grouping on all 17 scores at once is still a smear: silhouette 0.18 (2 groups), 0.16 (3), 0.18 (4), where 1 would be clean groups. Agreement with the original under resampling of games: 0.54 for 2 groups, 0.34 for 3 (round 5b 0.54 and 0.34). Clan positions under resampling correlate 0.90 with the original on the first scale and 0.79 on the second (round 5b 0.90 and 0.79).
- On the two-scale map four corners fit best (silhouette 0.46); clans keep their corner in 86% of resamples on average (round 5b 86%).

Loadings (link of each score with each scale; round 5b -> round 5c):

| Score | First scale (who the smoke is for) | Second scale (how much smoke) |
|---|---|---|
| Stacked on a teammate (%) | -0.85 -> -0.85 | +0.29 -> +0.29 |
| For a teammate (%) | -0.83 -> -0.83 | +0.07 -> +0.07 |
| Radar cruiser inside (% of destroyer smokes) | -0.82 -> -0.82 | +0.15 -> +0.15 |
| Long-smoke destroyers per game | -0.78 -> -0.78 | +0.24 -> +0.24 |
| Cruisers carrying smoke per game | +0.72 -> +0.72 | -0.11 -> -0.11 |
| Cap-sitter destroyers per game | +0.67 -> +0.67 | +0.51 -> +0.51 |
| Kiting (%) | +0.58 -> +0.58 | -0.02 -> -0.02 |
| Parked (%) | +0.56 -> +0.56 | +0.58 -> +0.58 |
| Exhaust-smoke ships per game | +0.41 -> +0.41 | -0.48 -> -0.48 |
| Inside a cap (%) | +0.34 -> +0.34 | +0.24 -> +0.24 |
| Centre lane (%) | +0.32 -> +0.33 | -0.00 -> -0.01 |
| Pushing (%) | -0.31 -> -0.31 | -0.51 -> -0.51 |
| First smoke of the game (median, s) | +0.30 -> +0.30 | -0.46 -> -0.46 |
| Median distance to cap edge (m) | -0.25 -> -0.25 | -0.37 -> -0.37 |
| Smokes per game | +0.23 -> +0.23 | +0.76 -> +0.76 |
| Smokes after 12:00 (%) | -0.19 -> -0.20 | +0.51 -> +0.51 |
| Destroyers carrying smoke per game | -0.05 -> -0.05 | +0.71 -> +0.72 |

Largest change in any loading: 0.01.

Each clan's position and style, round 5b and round 5c (first scale: negative = smoke laid for a teammate, positive = ships smoke for themselves; second scale: positive = more smoke).

| Clan | First scale | Second scale | Style, round 5b | Style, round 5c | Moved | Kept its style under resampling |
|---|---|---|---|---|---|---|
| *RESIN | -2.38 -> -2.39 | +1.15 -> +1.15 | Team smoke, plenty of it | Team smoke, plenty of it | no | 100% -> 100% |
| *H-SR | -4.58 -> -4.57 | +0.32 -> +0.28 | Team smoke, plenty of it | Team smoke, plenty of it | no | 96% -> 95% |
| *BONKZ | -2.22 -> -2.23 | +0.90 -> +0.91 | Team smoke, plenty of it | Team smoke, plenty of it | no | 95% -> 95% |
| MZY | -1.85 -> -1.85 | -3.25 -> -3.26 | Team smoke, little of it | Team smoke, little of it | no | 97% -> 97% |
| *HTDOG | +2.49 -> +2.51 | +0.74 -> +0.65 | Own smoke, plenty of it | Own smoke, plenty of it | no | 96% -> 98% |
| EPOXY | -1.66 -> -1.67 | +1.27 -> +1.28 | Team smoke, plenty of it | Team smoke, plenty of it | no | 100% -> 100% |
| HFANS | +0.32 -> +0.32 | +1.22 -> +1.23 | Team smoke, plenty of it | Team smoke, plenty of it | no | 57% -> 57% (borderline) |
| -BN- | -1.00 -> -1.00 | +0.82 -> +0.83 | Team smoke, plenty of it | Team smoke, plenty of it | no | 96% -> 96% |
| *KITE | -1.16 -> -1.16 | +0.25 -> +0.26 | Team smoke, plenty of it | Team smoke, plenty of it | no | 72% -> 72% (borderline) |
| KITED | +2.77 -> +2.77 | -2.49 -> -2.48 | Own smoke, little of it | Own smoke, little of it | no | 100% -> 100% |
| MACHX | +1.19 -> +1.18 | +0.53 -> +0.55 | Own smoke, plenty of it | Own smoke, plenty of it | no | 63% -> 62% (borderline) |
| REEEE | -0.08 -> -0.08 | +0.76 -> +0.76 | Team smoke, plenty of it | Team smoke, plenty of it | no | 53% -> 54% (borderline) |
| PFANS | -0.93 -> -0.93 | -1.61 -> -1.61 | Team smoke, little of it | Team smoke, little of it | no | 76% -> 76% |
| KSC | -1.73 -> -1.74 | +2.54 -> +2.55 | Team smoke, plenty of it | Team smoke, plenty of it | no | 100% -> 100% |
| *VRTUS | +0.68 -> +0.68 | +1.97 -> +1.97 | Own smoke, plenty of it | Own smoke, plenty of it | no | 64% -> 64% (borderline) |
| 5D | +1.61 -> +1.61 | -2.77 -> -2.76 | Own smoke, little of it | Own smoke, little of it | no | 98% -> 98% |
| BONKY | -1.74 -> -1.74 | +1.27 -> +1.27 | Team smoke, plenty of it | Team smoke, plenty of it | no | 85% -> 85% |
| KSE | +3.02 -> +3.02 | -2.11 -> -2.11 | Own smoke, little of it | Own smoke, little of it | no | 90% -> 90% |
| MACH | +3.68 -> +3.68 | +0.63 -> +0.62 | Own smoke, plenty of it | Own smoke, plenty of it | no | 98% -> 98% |
| NGA | +0.21 -> +0.21 | -2.15 -> -2.14 | Team smoke, little of it | Team smoke, little of it | no | 72% -> 72% (borderline) |
| PN | -2.89 -> -2.89 | -3.29 -> -3.29 | Team smoke, little of it | Team smoke, little of it | no | 98% -> 98% |
| RSR | -0.56 -> -0.56 | +0.00 -> +0.01 | Team smoke, plenty of it | Team smoke, plenty of it | no | 73% -> 73% (borderline) |
| SCCC2 | +2.80 -> +2.80 | +2.12 -> +2.12 | Own smoke, plenty of it | Own smoke, plenty of it | no | 95% -> 95% |
| UYSC | +4.01 -> +4.01 | +1.19 -> +1.21 | Own smoke, plenty of it | Own smoke, plenty of it | no | 92% -> 92% |
| BTLST (flag) | +0.73 -> +0.73 | -1.46 -> -1.44 | Own smoke, little of it | Own smoke, little of it | no | flagged: not used to build the map |
| INCA (flag) | +0.14 -> +0.14 | +2.11 -> +2.11 | Team smoke, plenty of it | Team smoke, plenty of it | no | flagged: not used to build the map |
| MANBA (flag) | -1.00 -> -1.00 | -5.26 -> -5.26 | Team smoke, little of it | Team smoke, little of it | no | flagged: not used to build the map |
| OGF (flag) | +0.91 -> +0.91 | -2.06 -> -2.06 | Own smoke, little of it | Own smoke, little of it | no | flagged: not used to build the map |
| RMN (flag) | -0.40 -> -0.39 | -2.27 -> -2.27 | Team smoke, little of it | Team smoke, little of it | no | flagged: not used to build the map |
| KM (flag) | -0.73 -> -0.73 | -3.57 -> -3.57 | Team smoke, little of it | Team smoke, little of it | no | flagged: not used to build the map |

Clans that moved style: none (0 of 30).

The four corners:

| Style | Top 6 | Rest | Borderline (kept the style in under 75% of resamples) | Flagged clans that would fall here |
|---|---|---|---|---|
| Team smoke, plenty of it (11 clans, 167 games, 810 smokes; W-L 101-66) | RESIN, H-SR, BONKZ, KITE | EPOXY, HFANS, -BN-, REEEE, KSC, BONKY, RSR | HFANS 57%, KITE 72%, REEEE 54%, RSR 73% | INCA |
| Own smoke, plenty of it (6 clans, 64 games, 383 smokes; W-L 32-32) | HTDOG, VRTUS | MACHX, MACH, SCCC2, UYSC | MACHX 62%, VRTUS 64% | none |
| Team smoke, little of it (4 clans, 45 games, 116 smokes; W-L 20-25) | none | MZY, PFANS, NGA, PN | NGA 72% | MANBA, RMN, KM |
| Own smoke, little of it (3 clans, 31 games, 120 smokes; W-L 12-19) | none | KITED, 5D, KSE | none | BTLST, OGF |

Borderline clans: round 5b HFANS 57%, KITE 72%, MACHX 63%, NGA 72%, REEEE 53%, RSR 73%, VRTUS 64%; round 5c HFANS 57%, KITE 72%, MACHX 62%, NGA 72%, REEEE 54%, RSR 73%, VRTUS 64%. The list is the same.

What each style looks like (pooled; 95% interval, games resampled within the style; n = smokes the rate applies to):

| Score | Team smoke, plenty | Own smoke, plenty | Team smoke, little | Own smoke, little |
|---|---|---|---|---|
| Long-smoke destroyers per game | 1.0 (0.9 to 1.1) | 0.4 (0.3 to 0.6) | 0.6 (0.4 to 0.8) | 0.3 (0.2 to 0.5) |
| Cruisers carrying smoke per game | 0.4 (0.3 to 0.5) | 1.1 (0.8 to 1.3) | 0.5 (0.4 to 0.7) | 1.2 (0.9 to 1.4) |
| Destroyers carrying smoke per game | 1.7 (1.6 to 1.8) | 1.6 (1.4 to 1.8) | 0.9 (0.7 to 1.2) | 1.2 (1.0 to 1.3) |
| Smokes per game | 4.8 (4.5 to 5.3) | 6.0 (5.1 to 6.8) | 2.6 (2.0 to 3.2) | 3.9 (3.4 to 4.5) |
| First smoke of the game (median, s) | 2:42 (2:32 to 3:03) | 3:26 (3:00 to 4:04) | 3:04 (2:20 to 4:31) | 3:39 (3:00 to 4:15) |
| Smokes after 12:00 (%) | 13% (10 to 16) | 13% (9 to 18) | 8% (3 to 13) | 6% (2 to 11) |
| For a teammate (%) | 66% (61 to 70) | 45% (39 to 51) | 61% (50 to 70) | 44% (32 to 56) |
| Radar cruiser inside (% of destroyer smokes) | 42% (36 to 48) | 28% (20 to 37) | 41% (29 to 52) | 7% (0 to 15) |
| Parked (%) | 25% (21 to 29) | 40% (34 to 48) | 17% (10 to 25) | 23% (17 to 29) |
| Inside a cap (%) | 24% (20 to 29) | 24% (19 to 29) | 17% (10 to 24) | 26% (19 to 32) |
| What it buys: Concealed damage per smoke | 11,692 (10,402 to 12,964) | 7,725 (6,524 to 9,044) | 9,204 (6,899 to 12,502) | 4,120 (2,772 to 5,724) |
| What it buys: Concealed damage per game | 56,712 (50,377 to 64,535) | 46,230 (35,518 to 56,839) | 23,726 (16,399 to 32,408) | 15,948 (10,177 to 22,684) |
| What it buys: Nearest cap taken (% of smokes where it was not ours) | 36% (30 to 41), n 425 | 29% (22 to 35), n 224 | 25% (15 to 37), n 76 | 30% (22 to 40), n 70 |
| What it buys: Contested cap taken (% of smokes where it was not ours) | 30% (25 to 34), n 538 | 23% (17 to 30), n 253 | 19% (11 to 29), n 89 | 23% (16 to 31), n 88 |
| What it buys: Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 84% (80 to 88), n 277 | 88% (81 to 95), n 136 | 76% (63 to 88), n 34 | 89% (78 to 98), n 47 |
| What it buys: Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 79% (74 to 83), n 290 | 86% (78 to 93), n 144 | 70% (50 to 86), n 33 | 85% (70 to 95), n 41 |
| What it buys: Died per 100 smokes | 14.5 (11.8 to 17.3), n 801 | 13.6 (9.6 to 18.1), n 383 | 25.0 (16.1 to 33.3), n 116 | 27.5 (19.4 to 35.6), n 120 |
| What it buys: Caught per 100 smokes | 9.6 (7.5 to 12.1), n 810 | 9.4 (6.0 to 13.1), n 383 | 15.5 (8.8 to 22.8), n 116 | 19.2 (12.0 to 26.5), n 120 |
| What it buys: Smoker died per 100 smokes | 10.0 (7.8 to 12.4), n 801 | 11.2 (7.6 to 15.3), n 383 | 16.4 (9.8 to 23.2), n 116 | 24.2 (17.1 to 31.7), n 120 |
| What it buys: Smoker caught per 100 smokes | 5.1 (3.6 to 6.9), n 810 | 7.8 (4.7 to 11.1), n 383 | 8.6 (3.5 to 13.5), n 116 | 15.8 (10.2 to 21.7), n 120 |
| What it buys: Nearest caps taken with a smoke per game | 0.8 (0.7 to 0.9) | 0.8 (0.6 to 1.0) | 0.4 (0.2 to 0.6) | 0.6 (0.5 to 0.8) |
| What it buys: Contested caps taken with a smoke per game | 0.8 (0.7 to 0.9) | 0.7 (0.6 to 0.9) | 0.3 (0.2 to 0.5) | 0.6 (0.4 to 0.7) |

Plain reading of the styles with the new outcome scores:
- **Team smoke, plenty of it.** Long-smoke destroyers (Somers, Gearing, Harugumo) lay smoke for a cruiser, usually a radar cruiser, and they lay a lot of it. Few cruisers bring their own smoke. Died 14.5 and caught 9.6 per 100 smokes (smoker only 10.0 and 5.1); nearest cap taken 36%, contested cap taken 30%; nearest cap not lost 84%, contested 79%; concealed damage per smoke 11,692.
- **Own smoke, plenty of it.** Cruisers (Svea, Jinan, Napoli) and cap-sitter destroyers (Daring, Gdansk, Shimakaze) each smoke for themselves, often parked, and there is a lot of smoke per game. Died 13.6 and caught 9.4 per 100 smokes (smoker only 11.2 and 7.8); nearest cap taken 29%, contested cap taken 23%; nearest cap not lost 88%, contested 86%; concealed damage per smoke 7,725.
- **Team smoke, little of it.** The same team-smoke habit, but few smoke ships in the lineup and few smokes per game; the first smoke comes late. Died 25.0 and caught 15.5 per 100 smokes (smoker only 16.4 and 8.6); nearest cap taken 25%, contested cap taken 19%; nearest cap not lost 76%, contested 70%; concealed damage per smoke 9,204.
- **Own smoke, little of it.** Ships smoke for themselves (Napoli exhaust, cap sitters), with few smoke destroyers and few smokes per game. Died 27.5 and caught 19.2 per 100 smokes (smoker only 24.2 and 15.8); nearest cap taken 30%, contested cap taken 23%; nearest cap not lost 89%, contested 85%; concealed damage per smoke 4,120.
- On both death scores the fewest deaths per 100 smokes are in "Own smoke, plenty of it" and the most in "Own smoke, little of it". The two "plenty" styles are close to each other on both; the two "little" styles have few smokes, so their intervals are wide.

**Top 6 or Shared:**
- First scale (who the smoke is for): Shared. Top 6 mean -1.19, Rest +0.40, gap -1.59 (-3.58 to +0.47). Round 5b: Top 6 mean -1.20, Rest +0.40, gap -1.59 (-3.58 to +0.46).
- Second scale (how much smoke): Top 6. Top 6 mean +0.87, Rest -0.29, gap +1.16 (+0.16 to +2.21 *). Round 5b: Top 6 mean +0.89, Rest -0.30, gap +1.18 (+0.19 to +2.23 *).
- Top 6 in a "plenty" style: 6 of 6 (17 of 24 clans are in one; chance of all six at random 9%). Top 6 in "Team smoke, plenty of it": 4 of 6 (chance of 4 or more at random 24%). Six clans is very few; neither count is settled.
- Outcome scores by style are description only: styles were built without them, and clans in different styles played different maps and opponents.

**Clans:** as in the position table and the four-corner table above. Flagged clans are placed on the map but were not used to build it.

**Could not be done / proxy:**
- With 24 clans and 17 scores no method can prove sharp types; the corners have soft borders and the borderline clans can flip under resampling.
- How the new outcome scores line up with the two scales (correlation across the 24 clans, description only): died per 100 +0.17 with the first scale and -0.57 with the second; caught per 100 +0.16 and -0.51; nearest cap taken -0.25 and +0.10; contested cap not lost +0.40 and +0.25 (24 clans).

**Verdict:** Lead

**Changed from round 5b:**

| Number | Round 5b | Round 5c | Why |
|---|---|---|---|
| First scale share | 29.6% | 29.6% | clock |
| Second scale share | 17.8% | 17.8% | clock |
| Third scale share | 11.6% | 11.5% | clock |
| Largest change in a loading | - | 0.01 | clock |
| Largest shift of a clan, first scale | - | 0.02 (HTDOG) | clock |
| Largest shift of a clan, second scale | - | 0.09 (HTDOG) | clock |
| Clans that change style | - | none | unchanged |
| Borderline clans | HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | unchanged |
| Mean share of resamples in which a clan keeps its style | 86% | 86% | clock |
| Top 6 minus Rest, first scale | -1.59 (-3.58 to +0.46) | -1.59 (-3.58 to +0.47) | clock |
| Top 6 minus Rest, second scale | +1.18 (+0.19 to +2.23) | +1.16 (+0.16 to +2.21) | clock |

Style outcome rows, round 5b -> round 5c:

| Score | Team smoke, plenty | Own smoke, plenty | Team smoke, little | Own smoke, little | Why |
|---|---|---|---|---|---|
| Deaths per 100 smokes -> Died per 100 smokes | 9.6 -> 14.5 | 9.4 -> 13.6 | 15.5 -> 25.0 | 19.2 -> 27.5 | new death metric |
| Deaths per 100 smokes -> Caught per 100 smokes | 9.6 -> 9.6 | 9.4 -> 9.4 | 15.5 -> 15.5 | 19.2 -> 19.2 | unchanged |
| Smoker died per 100 smokes | new: 10.0 | new: 11.2 | new: 16.4 | new: 24.2 | new death metric |
| Smoker caught per 100 smokes | new: 5.1 | new: 7.8 | new: 8.6 | new: 15.8 | new split |
| Nearest cap taken (% of smokes where it was not ours) (snapshots -> timeline) | 26.1 -> 35.5 | 23.7 -> 28.6 | 18.4 -> 25.0 | 25.7 -> 30.0 | cap timeline |
| Contested cap taken (% of smokes where it was not ours) | new: 29.6 | new: 22.9 | new: 19.1 | new: 22.7 | cap timeline |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) (snapshots -> timeline) | 88.1 -> 84.1 | 93.4 -> 88.2 | 85.3 -> 76.5 | 91.5 -> 89.4 | cap timeline |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | new: 78.6 | new: 86.1 | new: 69.7 | new: 85.4 | cap timeline |
| Nearest caps taken with a smoke per game | 0.59 -> 0.80 | 0.70 -> 0.80 | 0.27 -> 0.38 | 0.52 -> 0.61 | cap timeline |
| First smoke of the game (median, s) | 163.0 s -> 162.2 s | 207.0 s -> 206.3 s | 185.5 s -> 184.4 s | 221.0 s -> 219.7 s | clock |
| Smokes after 12:00 (%) | 13.3 -> 13.2 | 13.8 -> 13.3 | 7.8 -> 7.8 | 5.8 -> 5.8 | clock |

The batch `cap_def` row of the round 5b style table is dropped. Style members, games, smokes and W-L are the same as round 5b.

### D3. Compact profile per clan for a gauge graphic

**Answer:** The gauge profile is unchanged: one headline number per dimension, its position among the 24 clans, and a 95% range. The six headline numbers are identical to round 5b for 30 of 30 clans. Each clan now also carries the new scores (died and caught per 100, smoker-only versions, caps taken and not lost from the timeline). `clan_styles.json` keeps round 5b's structure, so the file can be swapped in.

**Numbers:** headline score per dimension (as round 5) and what "high" means:

| Dimension | Headline score | High means |
|---|---|---|
| Lineup | Cruisers carrying smoke per game | more cruisers that carry smoke in the lineup |
| Volume and tempo | Smokes per game | more smokes per game |
| Who it is for | For a teammate (%) | more smokes laid for a teammate |
| Where | Inside a cap (%) | more smokes inside a cap |
| Movement | Parked (%) | more smokes laid while parked |
| What it buys | Concealed damage per game | more concealed damage per game |

Two contrasting clans (value, 95% range, percentile):

| Dimension | H-SR | HTDOG |
|---|---|---|
| Lineup | 0.1 (0.0 to 0.2), p4 | 1.3 (1.0 to 1.6), p91 |
| Volume and tempo | 4.5 (3.7 to 5.4), p52 | 5.9 (4.4 to 7.4), p83 |
| Who it is for | 82% (73 to 91), p100 | 47% (32 to 61), p22 |
| Where | 16% (10 to 23), p17 | 25% (17 to 32), p57 |
| Movement | 8% (3 to 15), p0 | 46% (33 to 60), p96 |
| What it buys | 68,194 (48,505 to 89,537), p83 | 50,375 (31,496 to 71,640), p65 |

The new scores as they sit in the same two profiles (value, 95% range, percentile; for deaths a high percentile is worse):

| Score | H-SR | HTDOG |
|---|---|---|
| Died per 100 smokes | 6.0 (1.2 to 11.2) p0 | 10.4 (4.1 to 17.4) p17 |
| Caught per 100 smokes | 4.0 (0.0 to 8.9) p0 | 6.6 (2.1 to 12.2) p9 |
| Smoker died per 100 smokes | 4.0 (0.9 to 7.5) p4 | 8.5 (3.4 to 15.0) p30 |
| Smoker caught per 100 smokes | 2.0 (0.0 to 4.9) p9 | 5.7 (1.9 to 10.4) p30 |
| Nearest cap taken (% of smokes where it was not ours) | 56 (46 to 69) p100, n 50 | 30 (17 to 48) p48, n 53 |
| Contested cap taken (% of smokes where it was not ours) | 42 (33 to 52) p96, n 65 | 27 (15 to 40) p52, n 60 |
| Nearest cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 86 (74 to 96) p50, n 37 | 85 (66 to 100) p40, n 33 |
| Contested cap not lost (% of smokes within 2 km of it, cap not the enemy's) | 86 (73 to 96) p70, n 44 | 88 (72 to 100) p80, n 41 |
| Nearest caps taken with a smoke per game | 1.1 (0.9 to 1.5) p96 | 0.7 (0.4 to 1.1) p65 |
| Contested caps taken with a smoke per game | 1.1 (0.8 to 1.4) p91 | 0.7 (0.4 to 1.1) p70 |

JSON: top-level keys `batch`, `note`, `dimensions`, `extra_scores`, `clans`, `styles`, `structure`, `top6_minus_rest`; per clan `games`, `wins`, `losses`, `group`, `flagged_small`, `smokes`, `destroyer_smokes`, `values`, `percentiles`, `intervals`, `gauge`, `axes`, `style`, `style_id`, `style_note`, `style_kept_share`, `notes`. Structure equal to round 5b's file: yes. Each clan has 40 scores in `values` (round 5b 35). Added keys: `we_took_n_pct`, `we_took_c_pct`, `not_lost_n_pct`, `not_lost_c_pct`, `died_per100`, `caught_per100`, `died_smoker_per100`, `caught_smoker_per100`, `caps_taken_c_pg`, `died_pg`, `caught_pg`. Removed keys: `took_pct`, `held_pct`, `deaths_per100`, `cap_won_pg`, `cap_def_pg`, `deaths_pg`. `caps_taken_pg` keeps its key but is now counted from the timeline. `gauge` and `axes` keep their shape; the "What it buys" entry in `dimensions` now lists the new score keys. Style-level numbers (`styles[].numbers`) carry the same new keys, with `n` for the rates.

**Top 6 or Shared:** on the six headline numbers the only clear Top 6 gap is still concealed damage per game (+5,334 to +33,897 *); the other five are Shared: Cruisers carrying smoke per game -0.5 to +0.2; Smokes per game -0.4 to +1.6; For a teammate (%) -2.5 to +20.2; Inside a cap (%) -7.7 to +4.2; Parked (%) -11.4 to +13.5.

**Clans:** all 30; six flagged (BTLST, INCA, MANBA, OGF, RMN, KM) carry `flagged_small: true` and their percentile is where they would fall among the 24.

**Could not be done / proxy:**
- Ranges are wide for clans with few games; a gauge should draw the range, not only the dot.
- Percentiles rank clans against each other; a high percentile is not "good". The four death scores are the ones where high is worse.
- Cap rates are null ("too few") for the clans listed under D1; the design side should show them as missing, not zero.

**Verdict:** Keep

**Changed from round 5b:**

| Part of the file | Round 5b | Round 5c | Why |
|---|---|---|---|
| `gauge` (six headline numbers, percentiles, ranges) | 30 clans | identical for 30 of 30 clans | unchanged |
| `style`, `style_id` | 30 clans | identical for all 30 clans | unchanged |
| `axes` (positions and ranges, 2 decimals) | 30 clans | 24 clans differ in some rounded figure; largest position shift 0.09 | clock |
| `values` / `percentiles` / `intervals` | 35 scores | 40 scores: 11 added, 6 removed, `caps_taken_pg` recounted, three time scores on the replay clock | new death metric / cap timeline / clock |
| `style_note`, `style_kept_share` | borderline: HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | borderline: HFANS, KITE, MACHX, NGA, REEEE, RSR, VRTUS | unchanged |
| `top6_minus_rest` | 35 gaps | 40 gaps; see the full old and new list under D1 | new death metric / cap timeline / clock |
| `styles[].numbers` | took_pct, held_pct, deaths_per100, cap_def_pg | the ten "what it buys" scores and two caps-per-game counts | new death metric / cap timeline |

Per-clan numbers that moved are listed in full for the Top 6 and PN, and for the other clans, under D1 "Changed from round 5b". Positions on the two scales for all 30 clans, old and new, are in the D2 table.

Top 6 and PN, positions on the two scales as stored in `axes` (round 5b -> round 5c):

| Clan | First scale | Second scale | Style |
|---|---|---|---|
| *H-SR | -4.58 -> -4.57 | +0.32 -> +0.28 | Team smoke, plenty of it (same) |
| *RESIN | -2.38 -> -2.39 | +1.15 -> +1.15 | Team smoke, plenty of it (same) |
| *BONKZ | -2.22 -> -2.23 | +0.90 -> +0.91 | Team smoke, plenty of it (same) |
| *HTDOG | +2.49 -> +2.51 | +0.74 -> +0.65 | Own smoke, plenty of it (same) |
| *KITE | -1.16 -> -1.16 | +0.25 -> +0.26 | Team smoke, plenty of it (same) |
| *VRTUS | +0.68 -> +0.68 | +1.97 -> +1.97 | Own smoke, plenty of it (same) |
| PN | -2.89 -> -2.89 | -3.29 -> -3.29 | Team smoke, little of it (same) |

---

## 5. Items that stand as in Round 5b

Not redone in Round 5c. The text and numbers are in `../round5b/FINDINGS.md`.

| Item | Where | Note for this round |
|---|---|---|
| B1 cap sitters | Round 5b, Part B (Round 5 text) | No death or cap number in it changes. |
| B3 Harugumo per shot | Round 5b, Part B (Round 5b) | Read with the reworded line in section 2: "nearest friendly ship", not "spotted by". |
| B4 hybrids | Round 5b, Part B (Round 5 text) | Unchanged. |
| C1 cap defence from the timeline | Round 5b, Part C (Round 5b) | Already on the timeline. Its "nearest cap" numbers are the same definition as this round's `enemy_took_n` (233 of 1,074). |
| C2 cap holder at 8:00 | Round 5b, Part C (Round 5b) | Already on the timeline. |
| C3 danger zones | Round 5b, Part A (Round 5b) | No zone is kept. Its death window used 22 s (20 s plus one 2-second sample); with exactly 20 s the destroyer-smoker baseline is 12.75 per 100 against Round 5b's 12.8, and 136 distinct ships against 137 ship-smoke pairs. Not rerun: the conclusion (flags in line with chance) does not rest on that margin. |
| A2 leaving the smoke | Round 5b, Part A (Round 5b) | Stands, with the reworded line in section 2. |
| C4 spots per map | Round 5b, Part C (rerun) | Membership and damage unchanged. Death numbers in spot records are "caught". Cap numbers of the high cells are replaced by item 7a. |
| C5 other map questions | Round 5b, Part C (Round 5 text) | Unchanged apart from items 7b to 7d. Where a C5 row counts "early" smokes it is on the Round 5b clock-fixed HUD reading (306 early destroyer smokes); on the replay clock two more smokes are early (308). |
| Page 1 re-tests | Round 5b, first part | Already on the timeline and the radar log. The cap link is reworded in section 2. |

## 6. Could not be done

- **Radar pressed from the smoke, by group (item 1):** only 8 of the 104 cap-contest smokes with a radar cruiser inside have a
  radar press logged from inside that smoke. Closest proxy, given in the item: the cruiser inside pressed radar at some time
  while the smoke stood (43 smokes).
- **"Lit at death with no other detection" (item 2):** the batch keeps only the first moment of each detection kind per ship
  per smoke, so "no other detection" means "none found". Treat the count as an upper limit. The closer evidence is the
  track: of the 39 ships that died while radar-lit, 36 were already detected just before the radar reached them.
- **Flanking counter-smokes (item 4):** 12 smokes, 3 of them Top 6. No rate by group.
- **Clan rates under 8 cases (item 8):** "too few" for "cap not lost" on KSE, NGA, PN and four flagged clans.
- **Figures:** none were made this round.
