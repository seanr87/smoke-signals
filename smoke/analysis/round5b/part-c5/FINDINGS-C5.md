# Findings C5: map-specific questions

Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS; Rest = everyone else.

How to read this:
- Positions are team-normalized: own spawn at the bottom of the map (bottom left on Okinawa). West and east, and cells such as G1, are in that frame.
- "(a to b)" is a 95% interval made by resampling whole clans. A `*` means it excludes zero, so the gap is clear. "small n" = 8 to 14. Under 8 no rate is given.
- "Top 6 spot" = Top 6 use it clearly more than the Rest. "Shared spot" = no clear gap.
- Everything is association, not cause.
- "Enemy took the cap" comes from the round 5 library (`enemy_took`). It has been checked, but it misses roughly 15% of real flips, and nearly half of its "yes" answers fall in the 60 seconds after the smoke cleared. Read it as "during or just after the smoke".
- "At cap B" means inside the cap or within 2 km of its edge, unless a line says "nearest cap".
- Other ships' positions exist for one moment per smoke only (when it was fully laid), and for a median of 4 of the 9 allied ships. "None recorded" is not "none there".

Figures (working): `round5/figures/c5-sg-somers-east-west.png`, `c5-sg-harugumo-g1-second-dd.png`, `c5-hs-west-caps.png`, `c5-lp-first-smokes.png`, `c5-ok-death-zone.png`.

---

## Sleeping Giant

### C5-SG-1. Somers: Top 6 east, Rest west
**Answer:** Confirmed for the game as a whole: 17% of Top 6 Somers smokes are in the west half against 51% for the Rest. But it is not an opening choice. In the first 5 minutes both groups split evenly; the gap comes entirely from smokes after 5:00.

**Numbers:**

| Somers smokes | Top 6 in the west half | Rest in the west half | Gap (interval) |
|---|---|---|---|
| All (n 75) | 5 of 30 (17%) | 23 of 45 (51%) | -34 pts (-65 to -6 *) |
| First 5 minutes (n 23) | 4 of 8 (50%, small n) | 8 of 15 (53%) | -3 pts (-56 to +33) |
| After 5:00 (n 52) | 1 of 22 (4%) | 15 of 30 (50%) | -46 pts (-73 to -18 *) |

- East half: Top 6 25 of 30 (83%) vs Rest 22 of 45 (49%), +34 pts (+6 to +64 *).
- East half to draw: normalized x > 0, which is the rectangle u 0.5 to 1.0, v 0 to 1 in the 0-1 frame. The Top 6 smokes inside it sit in columns 8 to 10, rows E to J (u 0.74 to 0.99, v 0.40 to 0.95).
- Return is the same on both sides: east 14.0k concealed damage per smoke (10.9k to 16.5k, n 47), west 16.0k (11.5k to 19.4k, n 28). Deaths: east 10.6 per 100, west 14.3.
- Round 3 number reproduced exactly (17% vs 51%, -65 to -6).

**Top 6 or Shared:** Top 6 spot (east half, interval +6 to +64). Not for early smokes (interval -32 to +53 on the east share).

**Clans:** East: Top 6 RESIN 8, BONKZ 8, H-SR 8, VRTUS 1 | Rest HFANS 7, MACHX 5, EPOXY 4, BONKY 3, KITED 2, UYSC 1. West: Top 6 H-SR 3, RESIN 2 | Rest PFANS 8, REEEE 5, BONKY 4, MACHX 3, NGA 2, KITED 1. The Rest's west half rests on two clans (PFANS 8 of 8, REEEE 5 of 5); HFANS (7 of 7) and EPOXY (4 of 4) went east like the Top 6.

**Verdict:** Keep (reword: "after the opening, Top 6 Somers stay east").

### C5-SG-2. Harugumo at G1/F1: where is the second destroyer
**Answer:** A second destroyer has a recorded position in 7 of the 11 Top 6 smokes. In 3 it is up at cap A (cell F1, 2 to 3.4 km ahead of the smoke); in 2 it is inside the smoke itself (G1); in 2 it is far away to the east (G3/G4, 11 km off), both in smokes laid after 5:00.

**Numbers:** Spot reproduced: Top 6 11 of 24 Harugumo smokes vs Rest 1 of 9, +35 pts (+20 to +56 *). Second destroyers: Marceau 5, Chateaurenault 1, Ragnar 1. Forward of the smoke in 5 of 7; median 3.2 km from the smoke. In the 4 smokes with none recorded, at least one other allied destroyer was alive each time, and only 3 to 4 allied positions were recorded, so absence is not proof.

| Smoke | Clan | Time | Cell | Cruiser | Other destroyers alive | Second destroyer recorded (where) |
|---|---|---|---|---|---|---|
| [8147_g1_120797](https://seanr87.github.io/smoke-signals/smoke/smokes/8147_g1_120797.html) | RESIN | 2:23 | G1 | Petropavlovsk inside | Yueyang, Somers | none recorded |
| [8147_g1_120803](https://seanr87.github.io/smoke-signals/smoke/smokes/8147_g1_120803.html) | RESIN | 7:00 | F2 | none | Yueyang, Somers | none recorded |
| [8151_g1_29455](https://seanr87.github.io/smoke-signals/smoke/smokes/8151_g1_29455.html) | H-SR | 1:44 | F1 | Des Moines inside | Marceau, Somers, Marceau | Marceau in F1, 2.0 km from the smoke, 4.0 km forward, 0.2 km outside cap A |
| [8178_g1_166102](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g1_166102.html) | RESIN | 2:03 | G1 | Worcester inside | Ragnar, Gdansk, Chateaurenault | Chateaurenault in G1, inside the smoke |
| [8178_g1_166103](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g1_166103.html) | BONKZ | 2:47 | G1 | Worcester inside | Ragnar, Somers | Ragnar in F1, 3.4 km forward, 0.8 km inside cap A |
| [8178_g1_166106](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g1_166106.html) | BONKZ | 6:16 | F1 | Worcester inside | Somers | none recorded |
| [8183_g1_39283](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39283.html) | H-SR | 1:56 | G1 | Des Moines inside | Marceau, Somers | Marceau in F1, 3.2 km forward, 0.2 km inside cap A |
| [8183_g1_39284](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39284.html) | RESIN | 2:02 | G1 | Des Moines inside | Marceau, Somers, Gdansk | Marceau in G1, inside the smoke (1.0 km behind its centre) |
| [8183_g1_39285](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39285.html) | H-SR | 5:21 | F1 | Des Moines inside | Marceau, Somers | Marceau in G3, 11.7 km away to the east |
| [8183_g1_39286](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39286.html) | RESIN | 5:29 | G1 | Des Moines inside | Marceau, Somers, Gdansk | Marceau in G4, 11.0 km away, 4.3 km outside cap B |
| [8183_g1_39290](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g1_39290.html) | H-SR | 8:46 | F1 | Des Moines inside | Marceau, Somers | none recorded |
| [8177_g1_176201](https://seanr87.github.io/smoke-signals/smoke/smokes/8177_g1_176201.html) (Rest) | EPOXY | 2:42 | F1 | Petropavlovsk inside | Somers, 20 de Julio | 20 de Julio in F5, 13.9 km away, at cap B |

**Top 6 or Shared:** Top 6 spot (+20 to +56).

**Clans:** Top 6 RESIN 5, H-SR 4, BONKZ 2 | Rest EPOXY 1. Five games.

**Could not be done / proxy:** One moment per smoke only. The opening picture (the 5 smokes before 3:00 with a destroyer recorded) is: destroyer at cap A in 3, inside the smoke in 2.

**Verdict:** Keep (small n).

### C5-SG-3. What smoke goes to cap B, and is it there to stop the enemy taking B
**Answer:** Mostly lone cap-sitter destroyers (Daring 15, Gdansk 6 of 34), tagged as cap contest. B was already ours at the start of fewer than half of them, and an enemy was already contesting it in only 2. So it is cap-holding and cap-contesting smoke, not a reaction to an attack on B; the enemy rarely took B during these smokes, but the same is true at the other caps.

**Numbers (inside or within 2 km of the cap edge; 119 of the map's 305 smokes):**

| Cap | Smokes | Top 6 | Ours / neutral / theirs at start | Enemy took it during or just after (of smokes where it was not theirs) | We took it (of not ours) | Batch "cap defended" | Concealed dmg | Deaths per 100 |
|---|---|---|---|---|---|---|---|---|
| A | 46 | 21 | 28 / 12 / 6 | 3 of 40 (8%) | 7 of 18 (39%) | 8 | 12.0k | 6.5 |
| B | 34 | 13 | 16 / 12 / 6 | 1 of 28 (4%) | 5 of 18 (28%) | 4 | 5.7k | 11.8 |
| C | 17 | 7 | 8 / 2 / 7 | 2 of 10 (20%, small n) | 4 of 9 (small n) | 4 | 12.9k | 29.4 |
| D | 22 | 5 | 18 / 0 / 4 | 0 of 18 (0%) | 0 of 4 (too few) | 0 | 7.0k | 13.6 |

- At B: 31 destroyer smokes, 3 cruiser. Habits: cap sitters 23, long smokes 5, other 6. Primary purpose: cap contest 26 of 34. No cruiser covered in 25. 10 are inside the cap. Median time 8:12.
- B ours at the start: 16 of 34 (47%, 27 to 72); other caps 64% (52 to 75). Of those 16: Daring 11; the enemy was already contesting B at the start in 2; the batch's "cap defended" flag (enemy invading a cap we own while the smoke stood) fired on 2; the enemy took B in 1.
- B not ours at the start: 18; we took it during or just after 5.
- Enemy took B: 1 of 28 (4%) vs 5 of 68 (7%) at the other caps; difference -4 pts (-13 to +9). Not clear.
- Lowest return of the four caps: 5.7k per smoke.
- With the looser "nearest cap is B, any distance" rule: 59 smokes, ours 25 / neutral 21 / theirs 13, enemy took 4 of 46 (9%).

**Top 6 or Shared:** Shared spot. Share of all map smokes: Top 6 13 of 137 (10%) vs Rest 21 of 168 (12%), -3 pts (-12 to +7). Top 6 smoke B more often when it is already theirs (8 of 13 vs 8 of 21), not clear (-25 to +65).

**Clans:** Top 6 VRTUS 4, RESIN 4, HTDOG 3, BONKZ 2 | Rest HFANS 7, KITED 4, 5D 3, KSE 3, EPOXY 1, INCA 1, BONKY 1, -BN- 1. With B ours: Top 6 VRTUS 4, HTDOG 3, BONKZ 1 | Rest HFANS 3, KSE 1, BONKY 1, KITED 1, -BN- 1, 5D 1.

**Could not be done / proxy:** The data cannot tell "the smoke stopped the enemy" from "the enemy never came". The closest signs of a real attack are the contested flag at the start (2 of 16) and the batch "cap defended" flag (2 of 16).

**Verdict:** Drop the reading "there to stop the enemy taking B" (C1). Keep as: low-paying shared cap-sitter spot.

---

## Hotspot

### C5-HS-1. West caps A and B: 36% vs 14%
**Answer:** Confirmed: 36% of Top 6 destroyer smokes have A or B as their nearest cap against 14% for the Rest, and all six Top 6 clans do it. Two cautions: it is a west-side habit more than smoke in the caps (within 2 km of A or B the gap is not clear), and it happens after 5:00, not in the opening.

**Numbers (destroyer smokes, 80 Top 6, 155 Rest):**

| Nearest cap | Top 6 | Rest | Gap (interval) |
|---|---|---|---|
| A | 11 (14%) | 3 (2%) | +12 pts (+6 to +16 *) |
| B | 18 (22%) | 18 (12%) | +11 pts (+2 to +22 *) |
| A or B | 29 (36%) | 21 (14%) | +23 pts (+14 to +35 *) |
| C | 23 (29%) | 54 (35%) | -6 pts (-23 to +10) |
| D | 28 (35%) | 80 (52%) | -17 pts (-32 to -4 *) |

- Inside or within 2 km of A or B: Top 6 14 of 80 (18%) vs Rest 14 of 155 (9%), +8 pts (-5 to +24). Not clear. The 50 west smokes sit a median 1.8 km outside the cap edge.
- By time: first 5 minutes 3 of 23 vs 2 of 45 (+9, -7 to +38); after 5:00 26 of 57 (46%) vs 19 of 110 (17%), +28 pts (+20 to +38 *).
- Team-games with at least one destroyer smoke at A or B: Top 6 13 of 18, Rest 14 of 44.
- Without any one Top 6 clan the Top 6 share stays 33% to 39%.
- Return: A 19.7k per smoke (10.4k to 30.4k; n 14, small n), B 15.6k (8.8k to 23.9k; n 36). Within B the Rest returned more (20.8k vs 10.5k), so this is where Top 6 go, not proof that it pays them more.
- All classes (cruiser smokes added): 33% vs 22%, +11 pts (+4 to +24 *). The Rest's west smoke is largely cruiser smoke at B.

**Top 6 or Shared:** Top 6 spot for both A (+6 to +16) and B (+2 to +22), on the nearest-cap rule.

**Clans (destroyer smokes):** A or B: Top 6 H-SR 9, RESIN 6, VRTUS 5, BONKZ 5, HTDOG 2, KITE 2 | Rest HFANS 5, KSC 4, MANBA 2, EPOXY 2, INCA 2, BONKY 2, KSE 1, MACH 1, MACHX 1, MZY 1. A alone: Top 6 H-SR 4, BONKZ 3, VRTUS 2, RESIN 2 | Rest MACH 1, KSC 1, HFANS 1. B alone: Top 6 H-SR 5, RESIN 4, VRTUS 3, HTDOG 2, KITE 2, BONKZ 2 | Rest HFANS 4, KSC 3, MANBA 2, EPOXY 2, INCA 2, BONKY 2, KSE 1, MACHX 1, MZY 1. Six of 6 Top 6 clans; 10 of 24 Rest clans.

**Verdict:** Lead (say "west side, after the opening").

### C5-HS-2. Opener at G10: radar cruiser inside
**Answer:** The 87% vs 38% is for all early destroyer smokes on Hotspot, not G10 alone; it reproduces and is the biggest gap of any map. In the G10 cluster itself it is 83% vs 46%. Both groups use the G10 place equally; what differs is whether the radar cruiser is inside the smoke.

**Numbers (destroyer smokes in the first 5 minutes; 68 on the map):**

| Radar cruiser inside the smoke | Top 6 | Rest | Gap (interval) |
|---|---|---|---|
| Whole map | 20 of 23 (87%) | 17 of 45 (38%) | +49 pts (+31 to +71 *) |
| G10 cluster (36 smokes) | 10 of 12 (83%, small n) | 11 of 24 (46%) | +38 pts (+6 to +63 *) |
| G5 cluster, short of C (27 smokes) | 7 of 8 (88%, small n) | 5 of 19 (26%) | +61 pts (+28 to +91 *) |

- Use of G10: Top 6 12 of 23 early smokes (52%) vs Rest 24 of 45 (53%), -1 pt (-25 to +20).
- Round 5 definition, whole map: cruiser inside 87% vs 44% (+42, +25 to +65 *); cruiser screened only 9% vs 24% (-16, -34 to -1 *); no cruiser covered 4% vs 31% (-27, -45 to -10 *). In G10: inside 10 of 12 vs 13 of 24 (+29, +2 to +60 *); screened 2 of 12 vs 6 of 24.
- Other maps, radar cruiser inside early smokes: Sea of Fortune +39 (+12 to +62 *), Mountain Range +32 (-8 to +72), Loop +23, Land of Fire +10, Sleeping Giant -13 (none clear). Okinawa has only 3 Top 6 early smokes (too few).
- G10 smokers: Somers 16, Gearing 7, Harugumo 5, Shimakaze 3, Daring 3, Grozovoi 2. Cruisers inside: Top 6 Brisbane 4, Des Moines 4, Worcester 2; Rest Brisbane 5, Des Moines 4, Utrecht 3, Minotaur 1, Stalingrad 1.
- G10 return: 16.5k per smoke (Top 6 17.8k, Rest 15.9k).
- The atlas counts (36 at G10, 27 at G5) reproduce exactly.

**Top 6 or Shared:** Shared spot (the place). The radar cruiser inside it is the Top 6 habit.

**Clans (G10 cluster):** Top 6 H-SR 5, BONKZ 3, RESIN 2, HTDOG 1, KITE 1 | Rest REEEE 4, MZY 3, 5D 2, KSC 2, HFANS 2, KITED 2, and 1 each BTLST, RMN, PN, MACH, -BN-, NGA, BONKY, PFANS, EPOXY. Radar cruiser inside by clan: H-SR 4 of 5, BONKZ 3 of 3, RESIN 1 of 2, HTDOG 1 of 1, KITE 1 of 1; Rest clans without one: REEEE 3 of 4, 5D 2 of 2, MZY 2 of 3, KITED 2 of 2.

**Verdict:** Lead.

### C5-HS-3. Rim of C: which cruisers
**Answer:** Top 6 long smokes on the own-side rim of C almost always hold a radar cruiser (12 of 13): Moskva 5, Brisbane 4, Petropavlovsk 2. The Rest have 7 smokes there (too few for a rate): Des Moines 2, Brisbane 1, Minotaur 1 inside, Brisbane screened in 2, no cruiser in 1.

**Numbers:** Long smokes (Somers, Gearing, Harugumo, Delny) in the spot: Top 6 13 of 64 (20%) vs Rest 7 of 80 (9%), +12 pts (-7 to +27). Reproduces the round 4 lead.

| | Top 6 (13 smokes) | Rest (7 smokes) |
|---|---|---|
| Smoker | Somers 8, Gearing 4, Delny 1 | Somers 5, Gearing 2 |
| Cruiser inside | Moskva 5, Brisbane 4, Petropavlovsk 2, Utrecht 1, Minotaur 1 | Des Moines 2, Brisbane 1, Minotaur 1 |
| Cruiser screened | Worcester 1, Moskva 1 | Brisbane 2 |
| Smokes with a cruiser inside | 12 | 4 |
| Concealed dmg per smoke | 17.3k | 13.7k (too few) |

Each Top 6 clan brings its own cruiser: RESIN Moskva (5 inside, 1 screened) and Petropavlovsk 1; BONKZ Brisbane 4; H-SR Petropavlovsk 1 and Utrecht with Minotaur 1. Without RESIN the Top 6 share is 6 of 49 (12%).

**Top 6 or Shared:** Shared spot (interval -7 to +27).

**Clans:** Top 6 RESIN 7, BONKZ 4, H-SR 2 | Rest -BN- 4, INCA 1, KSC 1, MZY 1.

**Verdict:** Keep as a shared spot; drop as a Top 6 lead.

---

## Loop

### C5-LP-1. Early smoke rate per team-game against other maps
**Answer:** Loop has the fewest early smokes of any map: 0.70 early destroyer smokes per team-game against 0.91 on the other maps, and 0.43 early cruiser smokes against 0.69. The shortfall is in smokes with a cruiser inside. Top 6 and Rest are the same on Loop.

**Numbers (first 5 minutes; per team-game):**

| Map | Team-games (Top 6 / Rest) | Early destroyer smokes: all (interval) | Top 6 | Rest | Gap (interval) | Early cruiser smokes: all (interval) | Top 6 | Rest | Gap (interval) | Cruiser inside | Cruiser screened |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | 64 (27 / 37) | 1.08 (0.83 to 1.28) | 1.19 | 1.00 | +0.19 (-0.23 to +0.64) | 0.91 (0.70 to 1.10) | 1.04 | 0.81 | +0.23 (-0.14 to +0.65) | 0.69 | 0.22 |
| Hotspot | 62 (18 / 44) | 1.10 (0.89 to 1.28) | 1.28 | 1.02 | +0.26 (-0.10 to +0.65) | 0.85 (0.64 to 1.08) | 1.22 | 0.70 | +0.52 (+0.19 to +0.83 *) | 0.65 | 0.21 |
| Mountain Range | 42 (16 / 26) | 0.93 (0.63 to 1.24) | 0.88 | 0.96 | -0.09 (-0.70 to +0.52) | 0.67 (0.41 to 0.93) | 0.62 | 0.69 | -0.07 (-0.60 to +0.55) | 0.48 | 0.19 |
| Land of Fire | 50 (16 / 34) | 0.74 (0.53 to 0.95) | 0.75 | 0.74 | +0.01 (-0.38 to +0.62) | 0.50 (0.32 to 0.67) | 0.50 | 0.50 | 0.00 (-0.30 to +0.37) | 0.34 | 0.16 |
| Sea of Fortune | 42 (14 / 28) | 0.74 (0.51 to 0.96) | 0.64 | 0.79 | -0.14 (-0.66 to +0.35) | 0.57 (0.40 to 0.72) | 0.57 | 0.57 | 0.00 (-0.40 to +0.37) | 0.36 | 0.21 |
| **Loop** | 46 (13 / 33) | 0.70 (0.48 to 0.94) | 0.69 | 0.70 | 0.00 (-0.58 to +0.45) | 0.43 (0.25 to 0.63) | 0.46 | 0.42 | +0.04 (-0.40 to +0.40) | 0.22 | 0.22 |
| Okinawa | 36 (6 / 30) | 0.72 (0.50 to 1.00) | 0.50 | 0.77 | -0.27 (-0.76 to +0.19) | 0.44 (0.26 to 0.65) | 0.33 | 0.47 | -0.13 (-0.54 to +0.33) | 0.17 | 0.28 |

"Early cruiser smoke" = a destroyer smoke in the first 5 minutes covering a cruiser, inside or screened.
- Loop minus the other six maps: early destroyer smokes -0.22 (-0.41 to -0.02 *); early cruiser smokes -0.25 (-0.42 to -0.09 *); cruiser inside -0.26 (-0.38 to -0.13 *); cruiser screened +0.01 (-0.11 to +0.16).
- 21 of 46 Loop team-games (46%) had no early destroyer smoke; other maps 99 of 296 (33%).
- Part of this is line-ups: long-smoke ships fill 19% of destroyer slots on Loop against 28% elsewhere.

**Top 6 or Shared:** Shared (0.69 vs 0.70; interval -0.58 to +0.45).

**Clans (Loop early cruiser smokes, n 20):** Top 6 RESIN 3, H-SR 2, BONKZ 1 | Rest MACHX 2, -BN- 2, EPOXY 2, and 1 each 5D, KSC, UYSC, KM, INCA, NGA, MZY, HFANS.

**Verdict:** Keep.

### C5-LP-2. Spread of opening positions
**Answer:** Loop openings are not more scattered than on other maps. What sets Loop apart is that the first smoke is the latest of any map and no single cell dominates.

**Numbers (first smoke of each team-game, any ship):**

| Map | Team-games with a smoke | Mean distance from the map's average first-smoke position (interval) | Share of map width | Same, within the west and east halves | Cells holding 80% (of cells used) | Most used cell | Median time | Before 5:00 |
|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | 60 | 11.1 km (8.2 to 12.8) | 26% | 4.6 km | 10 of 19 | G1 (22%) | 2:41 | 87% |
| Hotspot | 62 | 10.7 km (8.2 to 12.3) | 22% | 7.1 km | 7 of 15 | G10 (18%) | 2:37 | 81% |
| Mountain Range | 41 | 10.7 km (8.0 to 13.2) | 22% | 5.9 km | 11 of 19 | G7 (15%) | 3:05 | 78% |
| Land of Fire | 45 | 9.7 km (7.6 to 11.2) | 20% | 7.1 km | 13 of 22 | F5 (18%) | 3:14 | 73% |
| Sea of Fortune | 39 | 15.7 km (13.5 to 16.5) | 33% | 4.4 km | 10 of 17 | F2 (15%) | 3:49 | 82% |
| **Loop** | 41 | 10.0 km (8.1 to 11.3) | 21% | 5.2 km | 11 of 18 | F4 (15%) | 4:14 | 68% |
| Okinawa | 35 | 12.5 km (10.5 to 13.9) | 30% | 7.8 km | 12 of 19 | D1 (11%) | 3:24 | 77% |

Loop first smokes by nearest cap: A 18, B 18, C 5. Top 6 6 / 5 / 1; Rest 12 / 13 / 4. No clear gap at any cap (A: +9 pts, -30 to +41).

**Top 6 or Shared:** Shared. Spread Top 6 9.9 km vs Rest 9.9 km (difference -4.4 to +2.1).

**Clans:** see C5-LP-3.

**Verdict:** Keep (as "late and with no fixed address", not "spread out").

### C5-LP-3. First smoker by ship
**Answer:** On Loop the first smoke comes from a cap sitter more often than from a long-smoke ship: Daring 7, Gearing 5, Somers 5, Gdansk 4, Napoli 4, Shimakaze 3 of 41. Long-smoke ships lay 32% of first smokes on Loop against 55% on the other maps.

**Numbers:**

| Map | First smokes | First smoker, all | Top 6 | Rest | Long-smoke ships | Cap sitters | Cruisers |
|---|---|---|---|---|---|---|---|
| Sleeping Giant | 60 | Somers 15, Gearing 13, Harugumo 11, Z-42 4, Napoli 4, Gdansk 3 | Harugumo 7, Gearing 5, Somers 5, Gdansk 3 | Somers 10, Gearing 8, Harugumo 4, Z-42 3 | 65% | 20% | 13% |
| Hotspot | 62 | Somers 22, Gearing 11, Harugumo 6, Daring 6, Gdansk 5, Shimakaze 4 | Somers 7, Gearing 4, Harugumo 3, Delny 1 | Somers 15, Gearing 7, Daring 6, Gdansk 4 | 65% | 29% | 5% |
| Mountain Range | 41 | Gearing 12, Somers 9, Svea 6, Gdansk 5, Napoli 5 | Svea 4, Gearing 4, Somers 4, Gdansk 2 | Gearing 8, Napoli 5, Somers 5, Gdansk 3 | 54% | 15% | 29% |
| Land of Fire | 45 | Somers 10, Gearing 9, Svea 5, Gdansk 3, Z-42 3, Harugumo 3 | Gearing 3, Z-52 2, Delny 2, Svea 2 | Somers 9, Gearing 6, Svea 3, Venezia 2 | 53% | 18% | 18% |
| Sea of Fortune | 39 | Napoli 7, Somers 7, Gearing 5, Svea 4, Harugumo 4, Jinan 2 | Svea 2, Gearing 2, Harugumo 2, Cerberus 1 | Somers 7, Napoli 6, Gearing 3, Svea 2 | 46% | 8% | 38% |
| **Loop** | 41 | Daring 7, Gearing 5, Somers 5, Gdansk 4, Napoli 4, Shimakaze 3 | Gdansk 3, Somers 2, Svea 2, Shimakaze 1 | Daring 6, Gearing 4, Napoli 4, Somers 3 | 32% | 39% | 20% |
| Okinawa | 35 | Gearing 6, Daring 5, Napoli 4, Svea 4, Harugumo 4, Somers 3 | Gearing 2, Svea 1, Somers 1, Smolensk 1 | Daring 5, Napoli 4, Gearing 4, Harugumo 4 | 37% | 29% | 31% |

Long-smoke share of first smokes, Loop minus the other maps: -24 pts (-38 to -7 *).

**Top 6 or Shared:** Not a spot. Top 6 has 12 first smokes on Loop: too few per ship to compare.

**Clans (Loop, by first smoker):** Daring 7: KITE 1 | KITED 2, BONKY 1, SCCC2 1, EPOXY 1, HFANS 1 (cells F4 3, G3 2). Gearing 5: BONKZ 1 | KSC, BTLST, 5D, OGF 1 each. Somers 5: RESIN 2 | EPOXY, MACHX, MZY 1 each (median 1:30). Gdansk 4: H-SR, BONKZ, RESIN 1 each | KSE 1. Napoli 4: Rest only (REEEE 2, MACHX 1, MANBA 1). Shimakaze 3: VRTUS 1 | UYSC 1, RMN 1. Svea 2: HTDOG 2.

**Verdict:** Keep.

### C5-LP-4. Test: did Daring smokes follow a friendly radar lighting an enemy destroyer
**Answer:** Not supported. Of 48 Daring smokes on Loop, one came within 60 seconds after a friendly radar lit an enemy ship that we can see in the data, and none followed an allied radar-from-smoke. Daring smokes on Loop are laid with less radar nearby than Daring smokes elsewhere, not more.

**What the batch records about friendly radar:** Radar activations outside smoke are not exported (the pipeline reads them but writes out only radar run from inside a smoke). There is no timeline of which enemy ships were detected. Three things exist:
1. Radar run from inside one of our own smokes (no time stamp, only the life of that smoke).
2. Each time an enemy ship sitting in its own team's smoke was lit by radar, with the time and the likely radar ship, wherever that radar ship was. This is the only time-stamped record of our radar lighting an enemy. The whole batch has 191 such rows, 77 on destroyers; Loop has 17, 9 on destroyers.
3. Positions at the one moment each smoke was fully laid.

**Numbers (proxy, 60-second window before the smoke was activated):**

| Group | Smokes | Our radar lit an enemy destroyer in its smoke, 60 s before | Same, 120 to 60 s before (control) | Same, 60 s after (control) | An allied smoke with radar run from inside stood in the 60 s before | An allied radar ship within radar range of the cap centre when the smoke was laid | Within radar range of the nearest enemy destroyer with a known position |
|---|---|---|---|---|---|---|---|
| Daring on Loop | 48 | 1 (2%, 0 to 8) | 1 (2%) | 0 | 0 (0%) | 18 (38%, 17 to 56) | 8 of 38 (21%) |
| Daring on other maps | 152 | 7 (5%, 2 to 8) | 4 (3%) | 6 (4%) | 15 (10%, 2 to 19) | 110 (72%, 63 to 79) | 57 of 123 (46%) |
| Other cap sitters on Loop | 40 | 0 | 0 | 0 | 2 (5%, 0 to 12) | 28 (70%, 56 to 84) | 16 of 37 (43%) |
| Other destroyer smokes on Loop | 54 | 0 | 0 | 1 (2%) | 4 (7%, 0 to 17) | 34 (63%, 50 to 77) | 14 of 43 (33%) |
| All destroyer smokes, all maps | 1,074 | 24 (2%, 1 to 3) | 17 (2%) | 23 (2%) | 119 (11%, 7 to 15) | 728 (68%, 63 to 72) | 353 of 873 (40%) |

- Radar ship in range of the cap: Daring on Loop minus Daring on other maps -35 pts (-55 to -15 *); minus other cap sitters on Loop -32 pts (-56 to -11 *).
- Before against the control windows, Daring on Loop: 0 pts (-5 to +7) and +2 pts (0 to +8). No rise before the smoke.
- The one case: [BONKY Daring, 17:51, F3](https://seanr87.github.io/smoke-signals/smoke/smokes/7919_g1_94407.html), 49 seconds after a Moskva lit an A. da Barbiano (a cruiser, not a destroyer) in its smoke.
- The other way round: our radar lit an enemy destroyer in its smoke 9 times on Loop; a Daring of that team was alive for 2 of them and smoked within 60 seconds once.
- Why: 41 of the 48 Daring smokes are at cap A, away from where the radar cruisers sit; 16 have no allied radar ship position recorded at all.

**Top 6 or Shared:** Not a spot. 45 of the 48 smokes are Rest.

**Clans:** Top 6 KITE 3 | Rest REEEE 11, KITED 9, EPOXY 6, MACHX 3, -BN- 3, BONKY 3, SCCC2 3, HFANS 3, KSC 2, NGA 2.

**Could not be done / proxy:** This is a proxy and a thin one. A radar that lit an enemy destroyer in open water leaves no trace in the batch, so the test can miss real cases. To test it properly the batch would need to export every radar activation with its time and the enemies it lit.

**Verdict:** Drop.

### C5-LP-5. Long smokes at F8 and F10
**Answer:** Both cells are shared and both pay well above the map average, on small counts. F8: 4 Top 6 and 4 Rest long smokes. F10: 1 Top 6 and 6 Rest.

**Numbers (long smokes = Somers, Gearing, Harugumo, Delny; 18 Top 6 and 27 Rest on Loop):**

| Cell | Top 6 | Rest | Gap (interval) | Concealed dmg per long smoke | All destroyer smokes in the cell |
|---|---|---|---|---|---|
| F8 | 4 of 18 (22%) | 4 of 27 (15%) | +7 pts (-28 to +82) | 27.5k, median 17.9k (n 8, small n) | 18.3k (n 15; Top 6 7, Rest 8) |
| F10 | 1 of 18 (6%) | 6 of 27 (22%) | -17 pts (-34 to +2) | n 7, too few | 20.7k (n 9, small n; Top 6 2, Rest 7) |
| F8 or F10 | 5 of 18 (28%) | 10 of 27 (37%) | -9 pts (-41 to +50) | 26.9k, median 27.9k (n 15) | 19.2k (n 24) |

Map average for destroyer smokes: 8.0k. The cell figures (18.3k, 20.7k) reproduce the atlas. F8 rests on a few big smokes: RESIN Somers 67k, BONKZ Gearing 52k and 64k (one game). Cruisers inside: F8 Brisbane 3, Des Moines 2; F10 Minotaur 2, Des Moines 1, Petropavlovsk 1, Prins van Oranje 1. Deaths in the 15 long smokes: 4 (3 in F10).

**Top 6 or Shared:** Shared (both cells; intervals cross zero).

**Clans (long smokes):** F8: Top 6 BONKZ 3, RESIN 1 | Rest HFANS 2, OGF 1, MZY 1. F10: Top 6 H-SR 1 | Rest EPOXY 2, MZY 2, 5D 1, KM 1.

**Verdict:** Keep as shared high cells (small n).

### C5-LP-6. Cap-sitter spot on B: clan counts
**Answer:** Reproduced: 15 of 23 Top 6 cap-sitter smokes are on the own side and east half of B against 13 of 65 for the Rest. Most of the gap is ship choice: the Rest's cap sitter on Loop is the Daring, which sits at cap A.

**Numbers:** Top 6 15 of 23 (65%) vs Rest 13 of 65 (20%), +45 pts (+25 to +72 *). Ships in the spot: Top 6 Gdansk 9, Shimakaze 3, Z-42 2, Daring 1; Rest Z-42 7, Grozovoi 3, Daring 2, Shimakaze 1. Leaving the Daring out: Top 6 14 of 20 (70%) vs Rest 11 of 20 (55%), +15 pts (-21 to +57), not clear. Return in the spot: Top 6 5.8k per smoke; Rest 1.2k (small n). We took B during or just after: Top 6 5 of 10, Rest 1 of 8 (small n).

**Top 6 or Shared:** Top 6 spot by the interval rule (+25 to +72), with the ship-choice caution above.

**Clans:** Top 6 RESIN 4, KITE 3, BONKZ 3, H-SR 2, HTDOG 2, VRTUS 1 | Rest REEEE 6, MACHX 2, SCCC2 2, RMN 1, MACH 1, EPOXY 1.

**Verdict:** Keep.

---

## Mountain Range

### C5-MR-1. Far-west Svea / Jinan area: clan counts per ship
**Answer:** It is two clans and two ships: HTDOG with the Jinan (8 smokes) and BONKZ with the Svea (4), in 4 games. No Rest clan parked a cruiser smoke there.

**Numbers:** Parked cruiser smokes in the spot: Top 6 12 of 33 (36%) vs Rest 0 of 13, +36 pts (+31 to +40 *). Reproduces round 4. Svea alone: Top 6 4 of 24 (17%) vs Rest 0 of 13, +17 pts (0 to +31), touching zero. The Jinan was fielded only by HTDOG (3 team-games), so the Jinan part cannot be compared. Cells H1 6, G1 4, H2 2. Return 19.0k per smoke (median 14.3k), 1 death; all 12 are solo smokes; median time 8:10. Any ship in the same ellipse: Top 6 17 of 88 smokes (19%) vs Rest 9 of 119 (8%), +12 pts (-4 to +26).

**Top 6 or Shared:** Top 6 spot by the rule (+31 to +40), but it is two clans in four games and partly ship choice.

**Clans:** Jinan: HTDOG 8. Svea: BONKZ 4. Rest: none. Rest clans with Svea smokes elsewhere on the map: INCA 6, MACHX 6, PN 1.

**Verdict:** Keep (name the two clans; not a lead).

### C5-MR-2. Radar from smoke at B: did the enemy take B during those smokes
**Answer:** Often, yes. The enemy took B during or just after 5 of 13 radar smokes at B, and after 4 of the 8 laid when B was ours. That is no better than ordinary smokes at B, and worse than radar smokes on other maps. B is simply the cap that changes hands most on this map. Small n throughout.

**Numbers:**

| Smokes | n | Top 6 | B ours / neutral / theirs at start | Enemy took B during or just after | Enemy took B when ours | We took B (of not ours) | Batch "cap defended" on B |
|---|---|---|---|---|---|---|---|
| Radar smokes, nearest cap B | 15 | 12 | 8 / 5 / 2 | 5 of 13 (38%, small n) | 4 of 8 (50%, small n) | 3 of 7 (too few) | 4 |
| Other smokes, nearest cap B | 53 | 23 | 15 / 17 / 21 | 11 of 32 (34%) | 5 of 15 (33%) | 17 of 38 (45%) | 4 |
| Radar smokes inside or within 2 km of B | 7 | 5 | 4 / 2 / 1 | 2 of 6 (too few) | 1 of 4 (too few) | 1 of 3 (too few) | 1 |
| Other smokes inside or within 2 km of B | 24 | 11 | 7 / 8 / 9 | 4 of 15 (27%) | 2 of 7 (too few) | 11 of 17 (65%) | 2 |
| Radar smokes, other maps (nearest cap) | 112 | 61 | 52 / 35 / 25 | 16 of 87 (18%) | 7 of 52 (13%) | 23 of 60 (38%) | 14 |

- "Radar smoke" = primary purpose cap control or radar trap, or radar activated from inside. On this map the two tests pick the same 15 smokes.
- The radar smokes sit a median 2.0 km outside the B edge (radar reaches the cap from there), so the 2 km rule keeps only 7. Both rows are shown.
- Whole map, enemy took the nearest cap during the smoke: A 6 of 41 (15%), B 16 of 45 (36%), C 10 of 56 (18%).
- B was ours at the start of 53% of radar smokes (25 to 73) against 28% of other smokes at B (14 to 43): radar smokes are more often laid on a held cap, so part of this is defence in intent.
- The 4 "ours, then lost" cases come from 3 games: BONKZ Svea twice (16:02 and 17:14, same game), H-SR Harugumo 13:58, KITE Gearing 10:42. All late.
- Ships: Gearing 4, Svea 4, Somers 3, Gdansk 3, Harugumo 1. The radar spotted at least one enemy in 11 of 15. Return 12.8k per smoke, 1 death.
- The atlas's "10 plays" counts destroyer plays whose batch-contested cap is B (reproduced: 10, Top 6 7, cap taken 1 of 6). The 15 here adds 4 Svea smokes and uses the nearest cap.

**Top 6 or Shared:** Top 6 spot. Radar smokes at B are 12 of 88 Top 6 smokes on the map (14%) vs 3 of 119 Rest (2%), +11 pts (+2 to +22 *). Of smokes at B, radar smokes are 12 of 35 vs 3 of 33 (+25, +6 to +40 *).

**Clans:** Top 6 KITE 4, BONKZ 4, H-SR 2, RESIN 2 | Rest HFANS 2, SCCC2 1.

**Verdict:** Keep the spot; Drop "radar from smoke defends B" (not supported: B was lost after half of the ones laid on a held cap, small n).

---

## Land of Fire

### C5-LF-1. Early cluster at cap A: ship breakdown
**Answer:** 13 early destroyer smokes short of cap A (F3), 5 Top 6 and 8 Rest. They are Gearing and Somers smokes for a cruiser: inside in 9, screened in 2, none in 2. Top 6 bring Des Moines inside; the Rest bring a mix and screen a Napoli three times.

**Numbers:** Share of early destroyer smokes in the cluster: Top 6 5 of 12 (42%) vs Rest 8 of 25 (32%), +10 pts (-18 to +39). Atlas count (13, Top 6 5) reproduced.

| | Top 6 (5, too few for rates) | Rest (8, small n) |
|---|---|---|
| Smoker | Gearing 2, Somers 1, Gdansk 1, Harugumo 1 | Gearing 4, Somers 3, Daring 1 |
| Cruiser inside | Des Moines 3, Brisbane 1 | Des Moines 2, Brisbane 1, Napoli 1, Svea 1 |
| Cruiser screened | none | Napoli 3, Smolensk 1, San Martin 1 |
| Smokes: inside / screened / no cruiser | 4 / 0 / 1 | 5 / 2 / 1 |
| Concealed dmg per smoke | 9.7k | 7.9k |
| Deaths | 0 | 2 |

Wider view, all early destroyer smokes whose nearest cap is A (19): Gearing 8, Somers 8, Daring 1, Gdansk 1, Harugumo 1; cruisers inside Des Moines 5, Utrecht 2, Brisbane 2, Napoli 1, Minotaur 1, Svea 1; inside 12, screened 3, no cruiser 4. Top 6 6 of 12 vs Rest 13 of 25 (-2 pts, -34 to +28).

**Top 6 or Shared:** Shared spot (-18 to +39).

**Clans:** Top 6 HTDOG 2, VRTUS 1, H-SR 1, RESIN 1 | Rest HFANS 3, BTLST 2, NGA 1, SCCC2 1, MACHX 1.

**Verdict:** Keep (small n).

### C5-LF-2. Svea at F5: clan counts
**Answer:** Reproduced: 14 of 19 Top 6 Svea smokes are on the own-side rim of B against 4 of 21 for the Rest. Three Top 6 clans, led by VRTUS; the Rest's 4 are all one clan.

**Numbers:** Top 6 14 of 19 (74%) vs Rest 4 of 21 (19%), +55 pts (+7 to +87 *). Without VRTUS the Top 6 share is 6 of 10. Six games; median time 6:16; Top 6 smokes there returned 14.2k each; 1 death in 18.

**Top 6 or Shared:** Top 6 spot (+7 to +87).

**Clans:** Top 6 VRTUS 8 (of 9 Svea smokes on the map), HTDOG 4 (of 5), RESIN 2 (of 5) | Rest BONKY 4 (of 4). Rest clans whose Svea never smoked there: -BN- 0 of 5, KSC 0 of 4, HFANS 0 of 4, EPOXY 0 of 3, RMN 0 of 1.

**Verdict:** Keep.

---

## Sea of Fortune

### C5-SF-1. Early cruiser smoke at the west cap and at D; which letter is the west cap
**Answer:** The west cluster is at cap B: the own-side west cap, bottom left as drawn (u 0.20, v 0.65). The atlas label was right. The confusion is that for teams spawning north the game calls that same cap A, so 8 of the 14 smoke pages say A. Early cruiser smoke goes to B (15 smokes) and short of D (7); none to the far west cap A.

**Numbers:**
- Caps in the 0-1 frame: A u 0.20 v 0.35 (far west), B u 0.20 v 0.65 (own-side west), C u 0.44 v 0.50, D u 0.76 v 0.50. Radius 0.083 for A and B, 0.062 for C and D.
- West cluster (14 early destroyer smokes, reproduces the atlas): all 14 have drawn-B as nearest cap; median 0.5 km outside the B edge and 7.7 km from the A edge. Game letter: A for 8 (north spawn), B for 6 (south spawn).
- Early cruiser smokes on the map (destroyer smoke in the first 5 minutes covering a cruiser): 24 of 31 early destroyer smokes.

| Nearest cap | Early cruiser smokes | Top 6 | Rest | Share of the group's early cruiser smokes: gap (interval) | Cruiser inside | Cruiser screened | Concealed dmg |
|---|---|---|---|---|---|---|---|
| B (own-side west) | 15 | 5 of 8 (62%) | 10 of 16 (62%) | 0 pts (-29 to +28) | 10 | 5 | 18.5k |
| D (east) | 7 (too few) | 3 of 8 | 4 of 16 | +12 pts (-16 to +40) | 5 | 2 | too few |
| C (centre) | 2 | 0 | 2 | | 0 | 2 | |
| A (far west) | 0 | 0 | 0 | | | | |

- At B, 12 of the 15 are inside or within 2 km of the cap; the D smokes sit 1.5 to 4.6 km short of it.
- B, smokers: Somers 6, Gearing 5, Harugumo, Shimakaze, Daring, Delny 1 each. Cruisers inside: Top 6 Brisbane 2, Utrecht 1, Worcester 1; Rest Salem, Minotaur, Svea, Utrecht, Worcester, Cerberus 1 each. Screened: Top 6 Brisbane 1, Stalingrad 1; Rest Puerto Rico 2, Napoli 2, Des Moines, Utrecht, Petropavlovsk, Prins van Oranje, Minotaur 1 each.
- D, smokers: Harugumo 3, Somers 2, Gearing 1, Delny 1. Cruisers inside: Top 6 Brisbane 2, Utrecht 1, Worcester 1; Rest Des Moines 1, Utrecht 1, Brisbane 1. Screened: Rest Des Moines 1, Moskva 1.

**Top 6 or Shared:** Shared, both places.

**Clans:** B: Top 6 H-SR 2, VRTUS 1, BONKZ 1, RESIN 1 | Rest 1 each RMN, REEEE, PN, RSR, KSC, INCA, KM, HFANS, SCCC2, MZY. D: Top 6 H-SR 1, BONKZ 1, RESIN 1 | Rest MZY 2, -BN- 1, BONKY 1.

**Verdict:** Keep (label the west spot "cap B, own-side west cap").

### C5-SF-2. Long smokes at D, whole game
**Answer:** Shared. 36% of Top 6 long smokes and 32% of Rest long smokes have D as nearest cap. They returned 17.7k each with no deaths in 20.

**Numbers:** Long smokes on the map: 22 Top 6, 37 Rest.

| Nearest cap | Top 6 | Rest | Gap (interval) | Concealed dmg per smoke | Deaths per 100 |
|---|---|---|---|---|---|
| D | 8 (36%) | 12 (32%) | +4 pts (-23 to +33) | 17.7k (Top 6 18.8k, Rest 17.0k) | 0 (n 20) |
| B | 8 (36%) | 17 (46%) | -10 pts (-44 to +16) | 15.0k | 16 (n 25) |
| A | 3 (14%) | 5 (14%) | 0 pts (-16 to +19) | small n | 25 (n 8) |
| C | 3 | 3 | +6 pts (-12 to +21) | too few | too few |

At D: Harugumo 7, Somers 7, Gearing 4, Delny 2. Cruisers inside: Top 6 Brisbane 5, Utrecht 1, Worcester 1; Rest Brisbane 4, Des Moines 3, Utrecht 2. They sit a median 4.6 km short of the cap edge (cells F9 6, G9 3), so "at D" means the east lane short of D. Same split early and late (early 3 of 8 vs 5 of 14; later 5 of 14 vs 7 of 23).

**Top 6 or Shared:** Shared spot (-23 to +33).

**Clans:** Top 6 BONKZ 4 (of 7 long smokes), H-SR 2 (of 6), RESIN 2 (of 6) | Rest MZY 6 (of 11), -BN- 3 (of 5), BONKY 3 (of 3). Three Top 6 clans of 4 with long smokes; 3 Rest clans of 14.

**Verdict:** Keep (shared; safest long-smoke place on the map).

### C5-SF-3. Svea spot: clan counts
**Answer:** Reproduced: 15 of 18 Top 6 Svea smokes sit in the open water on the own side of D (H7/G7) against 1 of 14 for the Rest.

**Numbers:** Top 6 15 of 18 (83%) vs Rest 1 of 14 (7%), +76 pts (+39 to +100 *). Holds without any one clan (8 of 11 without HTDOG, 9 of 9 without VRTUS). Six games; median time 8:04; 9.6k per smoke; no deaths. The Rest's Svea smokes go to the west cap B (8) and up at D (6).

**Top 6 or Shared:** Top 6 spot (+39 to +100).

**Clans:** Top 6 HTDOG 7 (of 7 Svea smokes on the map), VRTUS 6 (of 9), H-SR 2 (of 2) | Rest EPOXY 1 (of 1). Rest clans whose Svea never smoked there: RSR 0 of 5, KSC 0 of 5, PFANS 0 of 3.

**Verdict:** Keep.

---

## Okinawa

### C5-OK-1. Top 5 smoke ships with games played
**Answer:** By smokes laid: Napoli 32, Svea 25, Daring 22, Gearing 17, Somers 12. Per game played the order changes: the Svea lays 4.2 smokes per team-game, the Napoli 1.5.

**Numbers (18 games, 36 team-games, 158 smokes, all classes):**

| Ship | Class | Smokes | Team-games with the ship in the line-up | Ships fielded | Smokes per team-game played | Top 6 smokes | Concealed dmg per smoke | Deaths per 100 |
|---|---|---|---|---|---|---|---|---|
| Napoli | cruiser | 32 | 21 (Top 6 1) | 24 | 1.52 | 1 | 4.2k | 12.5 |
| Svea | cruiser | 25 | 6 (Top 6 1) | 7 | 4.17 | 3 | 9.6k | 4.0 |
| Daring | destroyer | 22 | 11 (Top 6 2) | 11 | 2.00 | 4 | 6.0k | 9.1 |
| Gearing | destroyer | 17 | 7 (Top 6 2) | 8 | 2.43 | 6 | 10.5k | 23.5 |
| Somers | destroyer | 12 | 4 (Top 6 1) | 5 | 3.00 | 4 | 18.1k (small n) | 16.7 (small n) |

Next: Shimakaze 11 smokes in 10 team-games (1.1), Harugumo 9 in 4 (2.25), Smolensk 8 in 3.

**Top 6 or Shared:** Not a spot. Top 6 played only 6 team-games here, so no comparison.

**Clans:** Napoli: H-SR 1 | BTLST 4, HFANS 4, KM 3, KITED 3, BONKY 3, 5D 2, MACHX 2, MZY 2, and 8 clans with 1. Svea: VRTUS 3 | SCCC2 9, MACH 6, UYSC 3, MACHX 2, BONKY 2. Daring: KITE 3, VRTUS 1 | MZY 9, MACHX 3, -BN- 3, UYSC 2, MACH 1. Gearing: BONKZ 4, KITE 2 | BTLST 3, 5D 2, OGF 2, RSR 2, -BN- 2. Somers: H-SR 4 | MACHX 3, REEEE 3, NGA 2.

**Verdict:** Keep.

### C5-OK-2. Death zone and its share laid while 50+ behind
**Answer:** The zone is the south-west water on the own side of cap C: 39 smokes, 12 deaths, 31 per 100 against 13 per 100 on the rest of the map. 49% of its smokes were laid while 50+ points behind, against 30% elsewhere (35% for the whole map). Neither gap is clear on its own, but the two stack: smokes laid there while 50+ behind lost a ship 42 times per 100.

**Numbers:**
- Shape (0-1 frame): ellipse centred u 0.246, v 0.644; radii 0.240 and 0.150 of the map width (10.1 by 6.3 km); long axis turned 34.5 degrees clockwise. Cells F2, F3, H4, F4, G3. A wide zone.
- Atlas numbers reproduced: the cluster is 12 smokes with a death (15 deaths), 7 of the 12 laid 50+ behind; 10 of those 12 fall inside the drawn ellipse. The ellipse holds 39 smokes of all classes with 12 deaths = 30.8 per 100 (13 to 47). Okinawa as a whole: 28 deaths in 158 smokes = 17.7 per 100 (11 to 24); 22.0 per 100 destroyer smokes (n 82), the highest of any map.
- Zone minus the rest of the map: +17 deaths per 100 (-3 to +35). Not clear.
- Laid 50+ behind: zone 19 of 39 (49%, 28 to 72); rest of the map 36 of 119 (30%, 17 to 44); whole map 55 of 158 (35%, 23 to 46). Difference +18 pts (-7 to +43). Not clear.

| Score when laid | Zone: smokes | Zone: deaths per 100 | Rest of the map: smokes | Rest of the map: deaths per 100 |
|---|---|---|---|---|
| 50+ behind | 19 | 42 | 36 | 17 |
| Level | 8 (small n) | 25 | 45 | 13 |
| 50+ ahead | 12 (small n) | 17 | 38 | 11 |

- Who is in the zone: 20 cruiser smokes, 18 destroyer, 1 battleship (Smolensk 7, Napoli 6, Daring 6, Svea 6, Shimakaze 4). Who died: the smoker in 7 (4 destroyers, 3 cruisers), 4 other cruisers, 1 battleship. Enemy radar had lit the ship in 2 of the 12 deaths. 24 of the 39 smokes were in lost games.

**Top 6 or Shared:** Shared zone. Share of each group's smokes laid there: Top 6 7 of 23 (30%) vs Rest 32 of 135 (24%), +7 pts (-17 to +34).

**Clans:** All 39: Top 6 KITE 3, RESIN 2, BONKZ 1, H-SR 1 | Rest HFANS 7, EPOXY 5, MACH 5, BTLST 2, MACHX 2, -BN- 2, REEEE 2, and 1 each OGF, PN, PFANS, UYSC, MANBA, KITED, MZY. Smokes with a death inside the ellipse (10): Top 6 KITE 1, BONKZ 1 | Rest HFANS 3, EPOXY 2, PN 1, MACH 1, REEEE 1.

**Verdict:** Keep as a danger zone (wide, small n; being behind explains part of it, not all).

