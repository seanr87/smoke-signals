# STEP 9: round 5b batch extension and rerun

Branch `r5b` (from `full-field` at `3d7e73f7`, tagged `pre-r5b`). smoke-signals 0.4.0, code revision `a7129ffa`.

- **New batch:** `output/20261117-230933`. 341 runs, 0 failed, 1,547 smokes, 103 flagged, 1,412 s (23.5 minutes), with frames.
- **Old batch, untouched:** `output/20261117-122135`.
- **Superseded:** `output/20261117-223529`, a first 0.4.0 run (revision `9865c81a`) made before ship tracks moved to once per run. Kept, not used.
- **Not from this work:** `output/20261117-221318`, `-224855`, `-224920`, `-231038`, `-231118` appeared during the evening. They hold the Grand Final game only and are stamped 0.3.0, so the 0.4.0 binary did not write them. Left as found.

## What the batch now writes

| File | Where | How often |
|---|---|---|
| `meta.json`, `caps_timeline.csv`, `radar.csv`, `score.csv` | `timelines/<game>/` | once per game |
| `tracks.csv`, `ribbons.csv` | `games/<run>/` | once per run |
| `max_health` per player | `game.json` and the game block of `smokes.json` | per run |

Field notes are in `smoke/DESIGN.md` section 15.

**Change made during Step 2.** The first rerun put every ship's track in the per-game file. The cross-check showed that a replay knows the other team's health and detection flag only while its own team sees those ships: 37% of the other team's rows were blank and some were stale. `tracks.csv` is now written once per run for the recording team's ships, so every ship comes from its own team's replay and appears once across the two runs. The single-replay game keeps both teams in its one run, with `own_replay` false on the other team.

## a. Nothing moved

- `smokes.csv`: 1,547 rows, 168 columns, same order. No field differs outside version, revision and timestamp.
- `smokes.json` (batch and per run), `game.json`, `damage_events.csv`, per-run `smokes.csv`, `damage_spike.json`: identical outside the expected keys, with two exceptions, both last-digit rounding and both present before this work:
  - `radar_spotted_damage` in `smokes.json`: 9 smokes differ in the seventh significant digit (for example 27678.398 against 27678.406). The CSV column, written to whole numbers, is identical.
  - `self_damage_authoritative` in `damage_spike.json`: 21 runs differ in the last digit (for example 162823.33 against 162823.34). The same field differs in 22 runs between two earlier batches of unchanged code (`20261117-104945` against `20261117-122135`).
  - Cause: both are sums of decimal numbers taken in an order that is not fixed from run to run. No analysis uses either at that precision.
- `games.csv` and `clans.csv` (made by `export_data.py` from the batch): identical between the two batches, as are `clans-destroyer.csv`, `breakdown.csv`, `ship_class.csv`; the exported `smokes.csv` differs only in the three provenance columns. See the end of this file.
- `max_health` is set for 6,113 of 6,138 player entries. The 25 missing are most likely ships of the other team that the run's own team never saw (not traced one by one); the analysis takes each ship's value from its own team's run.

## b. Completeness

- 171 played games, 171 `timelines/` folders, none missing a file. The one game with no kept smoke (RSR against PFANS, group 1 round 2) has its folder.
- `tracks.csv` and `ribbons.csv` in all 341 runs. 3,078 ships, each in exactly one run.
- Ribbons: 172 runs have at least one cap ribbon. 284 Defended, 91 Captured, 67 AssistedInCapture. These are the recording player's only: 341 ships of 3,078.
- The single-replay game (KSC against -BN-, losers bracket round 1 game 3) has `one_sided: true` in `meta.json`, its 9 smokes keep `one_sided` true, and its 9 other-team ships carry `own_replay` false.
- Merged sessions keep only the primary replay's ribbons (read in the merge code, confirmed by a reviewer, and seen in the data: each run holds only its own recorder's ribbons).

## c. Cross-check at every smoke's activation

All 1,547 smokes. The stored values are read when the frame is drawn, at the HUD second of activation, so they can sit up to about a second from the exact activation time.

| Check | Comparisons | Match | Explained | Other |
|---|---|---|---|---|
| Cap owner, every cap | 5,792 | 5,789 (99.95%) | 3: the owner changed within 2.5 s of the activation | 0 |
| Score, both teams | 3,094 | 2,427 at the sample before (78.4%) | 574 at the next sample, 65 between the two (the score ticked inside the 2 s step) | 28 (0.9%) |
| Smoker health | 1,547 | 1,371 within 0.5 points (88.6%) | 99 at the next sample, 50 between the two (health moved inside the step) | 24 (1.6%), plus 3 with no stored value |

- Score "other" (28): most are one tick away (3 or 4 points) beyond the neighbouring samples; at least 3 are a kill scored within a few seconds (44 to 60 points). All timing.
- Health "other" (24): mostly a few points, a ship being hit or healing at the activation; a few larger ones are heals or bursts between samples. The 3 with no stored value are in the single-replay game.
- Time base: the two runs of a game agree on elapsed time to within 0.75 s in all 170 two-replay games (median difference 0.01 s, from 1,408 ship deaths seen in both runs).

## d. Radar and hydro

A lit span is one stretch during which a ship carried the radar (or hydro) detection flag. It is attributed to every enemy activation that had the ship in range at the time; "ambiguous" means more than one did.

| | Activations | From inside a smoke | Lit rows attributed | Ambiguous | Target in a smoke | Unattributed spans |
|---|---|---|---|---|---|---|
| Radar, all maps | 2,426 | 155 | 4,303 | 208 (4.8%) | 242 | 140 (3.2%) |
| Hydro, all maps | 2,029 | 127 | 724 | 44 (6.1%) | 32 | 24 (3.2%) |

Radar by map (activations / lit / ambiguous / unattributed): Hotspot 481 / 740 / 44 / 31; Land of Fire 303 / 507 / 12 / 20; Loop 269 / 404 / 14 / 11; Mountain Range 312 / 468 / 25 / 12; Okinawa 214 / 445 / 14 / 23; Sea of Fortune 297 / 608 / 29 / 13; Sleeping Giant 550 / 1,131 / 70 / 30. Hydro by map is in the check output below.

Unattributed spans are flags with no enemy radar in range at that moment: a target just outside the 3% range allowance, or a position known only from the minimap.

## e. Tools, tests, size, time

- `sanity.py`: 341 runs, 0 failed; ledger median 0.997; 217 reference rows, 0 changed; 1,538 smokes seen in both runs counted once, 1,547 kept; enemies table 0 mismatches.
- Tests: 31 unit tests (7 new), the repeatability test (now covering the new files) and the reference-game test pass.
- Size: `timelines/` 9.2 MB, `tracks.csv` files 156.9 MB, ribbons 0.1 MB. Whole batch folder with frames 3.9 GB.
- Zip: `output/20261117-230933/smoke-signals-timelines-r5b.zip`, 1,707 files, 170 MB raw, 16.7 MB. Release link: https://github.com/seanr87/smoke-signals/releases/tag/data-r5b
- Run time: 1,412 s against 1,029 s for the old batch. The cap check on every packet is the main extra cost.

## Known limits of the new files

- Radar attribution is by range and time, not from the game.
- Ribbons cover the recording player only.
- In the single-replay game the other team's health and detection are blank or stale while unseen.
- Positions are from the merged position timeline and are complete for both teams; `pos_source` says when one comes from the minimap.

## Check output

### Output of smoke/tools/check_timelines.py

- new batch: `output/20261117-230933`
- old batch: `output/20261117-122135`

#### a. Nothing moved

- smokes.csv: 1547 rows new, 1547 old; only in new 0, only in old 0; columns new 168, old 168; same column order: True
- smokes.csv fields that differ outside version, revision and timestamp: none
- provenance in the new batch: {'wows_toolkit_rev': [('a7129ffa', 1547)], 'smoke_signals_version': [('0.4.0', 1547)]}
- smokes.json (batch): 1547 records new, 1547 old; differing paths outside the expected keys: {'.radar_spotted_damage': 9}
- run folders: 341 new, 341 old; same names: True
- per-run files differing outside the expected keys (of 341 runs): {'game.json': 0, 'smokes.json': 8, 'smokes.csv': 0, 'damage_events.csv': 0, 'damage_spike.json': 21}
  - damage_spike.json kots19na_groups_group-1_round-4_pn-vs-htdog_g1_pn: ['.self_damage_authoritative']
  - damage_spike.json kots19na_groups_group-1_round-5_ksc-vs-rsr_g1_rsr: ['.self_damage_authoritative']
  - damage_spike.json kots19na_groups_group-1_round-5_pfans-vs-uysc_g1_uysc: ['.self_damage_authoritative']
  - damage_spike.json kots19na_groups_group-1_round-5_pn-vs-vrtus_g1_pn: ['.self_damage_authoritative']
  - damage_spike.json kots19na_groups_group-1_round-6_htdog-vs-rsr_g1_rsr: ['.self_damage_authoritative']
  - smokes.json kots19na_groups_group-3_round-3_bn-vs-h-sr_g1_bn: ['.smokes[2].radar_spotted_damage', '.smokes[3].radar_spotted_damage']
  - smokes.json kots19na_groups_group-3_round-3_kited-vs-nga_g1_nga: ['.smokes[4].radar_spotted_damage']
  - smokes.json kots19na_groups_group-3_round-6_kited-vs-h-sr_g1_kited: ['.smokes[3].radar_spotted_damage']
  - smokes.json kots19na_groups_group-3_round-7_bonky-vs-nga_g1_nga: ['.smokes[4].radar_spotted_damage']
  - smokes.json kots19na_groups_group-4_round-6_resin-vs-epoxy_g1_epoxy: ['.smokes[3].radar_spotted_damage']
- max_health on players in game.json: {'set': 6113, 'missing': 25}

#### b. Completeness

- played games in the inventory: 171; timelines folders: 171; missing: none; extra: none; folders lacking a file: none
- games with no kept smoke: 1 (kots19na_groups_group-1_round-2_rsr-vs-pfans_g1); each has its timelines folder: True
- tracks.csv files: 341 of 341 runs; ships across the runs of a game: {'ship in one run': 3078}; own_replay values per ship: {'true': 3069, 'false': 9}
- ribbons.csv files: 341 of 341 runs; runs with at least one cap ribbon: 172; ribbons by kind: {'AssistedInCapture': 67, 'Defended': 284, 'Captured': 91}
- single-replay games in the inventory: ['kots19na_playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g3']; meta.json one_sided true: ['kots19na_playoffs_losers-bracket_lb-round-1_ksc-vs-bn_g3']; agree: True
- smokes.csv one_sided column: {'false': 1538, 'true': 9}; recorder known in meta.json: {True: 171}
- which run wrote the game files: {'first run in name order': 91, 'another run': 80}

#### c. Cross-check at each smoke's activation

Smokes checked: 1,547 of 1,547.

**Cap owner, every cap at every smoke** (5,792 comparisons)

| result | n | share |
|---|---|---|
| match | 5,789 | 99.95% |
| owner changed within 2.5 s of the activation | 3 | 0.05% |

**Score, both teams at every smoke** (3,094 comparisons)

| result | n | share |
|---|---|---|
| match (last sample at or before) | 2,427 | 78.44% |
| match (next sample, score ticked inside the 2 s step) | 574 | 18.55% |
| between the two neighbouring samples | 65 | 2.10% |
| other | 28 | 0.90% |

**Smoker health as a share of max health** (1,547 comparisons)

| result | n | share |
|---|---|---|
| match within 0.5 points (last sample at or before) | 1,371 | 88.62% |
| match within 0.5 points (next sample, health moved inside the 2 s step) | 99 | 6.40% |
| between the two neighbouring samples | 50 | 3.23% |
| other | 24 | 1.55% |
| no value | 3 | 0.19% |

  - other: ('kots19na_7971', 1, 82510, 0.2, 5.8, 5.8)
  - other: ('kots19na_7914', 1, 53659, 87.4, 89.8, 88.6)
  - other: ('kots19na_7976', 1, 219224, 7.7, 10.1, 8.3)
  - other: ('kots19na_7889', 1, 178503, 61.8, 61.2, 59.0)
  - other: ('kots19na_7980', 1, 78011, 80.0, 81.8, 83.0)
  - other: ('kots19na_7980', 1, 78008, 75.7, 77.4, 78.0)
  - other: ('kots19na_7898', 1, 197680, 90.2, 63.0, 88.6)
  - other: ('kots19na_7898', 1, 197679, 52.5, 75.7, 76.9)

#### d. Radar and hydro

**radar**

| map | activations | from inside a smoke | lit rows (attributed) | of which ambiguous | target in a smoke | unattributed spans | share unattributed |
|---|---|---|---|---|---|---|---|
| Hotspot | 481 | 36 | 740 | 44 | 34 | 31 | 4.0% |
| Land of Fire | 303 | 14 | 507 | 12 | 46 | 20 | 3.8% |
| Loop | 269 | 14 | 404 | 14 | 16 | 11 | 2.7% |
| Mountain Range | 312 | 27 | 468 | 25 | 26 | 12 | 2.5% |
| Okinawa | 214 | 10 | 445 | 14 | 35 | 23 | 4.9% |
| Sea of Fortune | 297 | 14 | 608 | 29 | 30 | 13 | 2.1% |
| Sleeping Giant | 550 | 40 | 1,131 | 70 | 55 | 30 | 2.6% |
| All maps | 2,426 | 155 | 4,303 | 208 | 242 | 140 | 3.2% |

**hydro**

| map | activations | from inside a smoke | lit rows (attributed) | of which ambiguous | target in a smoke | unattributed spans | share unattributed |
|---|---|---|---|---|---|---|---|
| Hotspot | 366 | 33 | 63 | 3 | 2 | 5 | 7.4% |
| Land of Fire | 260 | 5 | 118 | 5 | 8 | 8 | 6.3% |
| Loop | 299 | 13 | 71 | 0 | 4 | 0 | 0.0% |
| Mountain Range | 227 | 18 | 46 | 2 | 2 | 3 | 6.1% |
| Okinawa | 200 | 7 | 103 | 15 | 0 | 6 | 5.5% |
| Sea of Fortune | 300 | 19 | 152 | 13 | 7 | 1 | 0.7% |
| Sleeping Giant | 377 | 32 | 171 | 6 | 9 | 1 | 0.6% |
| All maps | 2,029 | 127 | 724 | 44 | 32 | 24 | 3.2% |


#### Size

- timelines/: 9.2 MB in 171 folders; tracks.csv files: 156.9 MB; ribbons.csv files: 109 KB

