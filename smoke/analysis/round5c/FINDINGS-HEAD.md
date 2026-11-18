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
