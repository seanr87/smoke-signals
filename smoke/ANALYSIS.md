# Smoke Signals analysis method (DRAFT, round 5, 4 Nov 2026)

How every smoke in King of the Sea XIX NA is classified, what the location fields mean, and how to compare clans without fooling yourself. Numbers are from batch `output/20261104-004230` (217 smokes: H-SR 100, RESIN 103, PN 14). Thresholds are constants in `crates/smoke-signals/src/classify.rs`; the reasoning behind each is in `DECISIONS-ROUND5.md`.

A note on scale: the game compresses distance, so ships cover map distance at about 2.6 times their listed speed. A destroyer lays a 40 to 55 s smoke over 2 to 5 km of map. All distances here are map metres as the replay records them.

## 1. The four structured fields

Every smoke carries four fields. Rule-based fields apply to all 217 smokes; fuzzy fields carry a confidence (high, medium, low) and are labelled "auto-tagged" on the site.

### 1.1 Smoker (mechanic, not purpose)

- `smoker_class`: destroyer, cruiser or battleship, from the ship's class.
- `smoke_type`: standard, cruiser (a standard variant whose puffs last 60 s or less, Svea), exhaust (Italian oil smoke), crawling (none in this replay set).
- Special cases flagged separately: `svea` (13 smokes), `battleship_exhaust` (10, all Conte Verde and C. Colombo), `battleship_crawling` (none).

Counts: H-SR 89 destroyer / 3 cruiser / 8 battleship; RESIN 87 / 15 / 1; PN 10 / 3 / 1.

### 1.2 Movement (fuzzy)

How the smoker moved while laying, judged against the centroid of the 3 nearest living enemies at the start of emission.

- Displacement: the smoker's position at the start of emission to its position at the end of emission (straight line).
- Angle between that displacement and the line to the enemy group: **pushing** at 60 degrees or less, **kiting** at 120 degrees or more, **horizontal** between.
- Confidence: high when the displacement is 2.5 km or more, medium at 1 km or more, low below 1 km (the angle means little when the ship barely moved); one step lower when the angle is within 15 degrees of a threshold.
- Unknown (23 smokes): the smoker or every enemy lacked a position at laying start. These are mostly second-perspective recorders, whose live position the merge never receives.

Counts: H-SR 29 pushing / 43 horizontal / 14 kiting / 14 unknown; RESIN 35 / 34 / 27 / 7; PN 7 / 3 / 2 / 2. Confidence over all: 63 high, 69 medium, 62 low.

### 1.3 Coverage (rule-based)

Who the smoke protected. Precedence: stacked, then screen, then selfish.

- **stacked**: a destroyer laid it within 2.5 km of an allied cruiser or battleship at the start of laying.
- **screen**: it hid teammates who sat inside it or fired from behind it (the complement of selfish).
- **selfish**: no teammate other than the owner was ever inside it, and no teammate fired through it from behind (the round 2 definition).

All three booleans stay in the record. Counts: H-SR 50 stacked / 32 screen / 18 selfish; RESIN 35 / 36 / 32; PN 5 / 2 / 7.

### 1.4 Purpose (tactic tags)

Every tag that applies is recorded; the primary tag is the first in this priority order.

| Priority | Tag | Rule | Confidence |
| --- | --- | --- | --- |
| 1 | cap_control | A radar ship (cruiser or radar destroyer) concealed inside the smoke whose radar covered at least 90% of a cap's area at some 2 s sample | rule |
| 2 | cap_contest | The smoke stood inside, or within 1 km edge to edge on average, of a contested cap, without that radar coverage | rule |
| 3 | radar_trap | A concealed radar ship in the smoke ran radar and an enemy gained the radar flag within its range (the offensive radar rule), and the smoke is not cap_control | rule |
| 4 | hydro_trap | The same with hydro | rule |
| 5 | counter_smoke | Laid within 3 km of an enemy smoke, 0 to 25 s after that smoke appeared | rule |
| 6 | island_dive | A covered ship moved at least 2 km under the smoke and ended within 1 km of land (and started further away, or moved 4 km or more) | high at 4 km ending within 600 m of land, medium at 3 km, low otherwise |
| 7 | reposition | A covered ship moved at least 3 km under the smoke and was never detected while covered | high at 6 km, medium at 4 km, low at 3 km |
| 8 | damage | 20,000 or more smoke damage, or two or more enemies hit. Sub-label target_rich (2 or more enemies hit), island_killer (one enemy whose mean position while hit was within 1 km of land), hunt (one enemy in the open) | rule for target_rich; island_killer high within 500 m of land; hunt high at 1.5 km or more from land |
| 9 | escape | Movement is kiting and at least one of: spotted at activation, HP at or below 50%, behind on points | high with two conditions and high movement confidence; medium with spotted or low HP; low otherwise |

A smoke with no tag has primary purpose "none" (26 smokes). "Covered" means inside the smoke or with the smoke between the ship and an enemy within 15 km.

Counts, any tag (H-SR / RESIN / PN): cap_control 48 / 47 / 5; cap_contest 14 / 15 / 1; radar_trap 1 / 4 / 1; hydro_trap 0 / 0 / 0; counter_smoke 0 / 0 / 0; island_dive 10 / 15 / 1; reposition 29 / 16 / 2; damage 52 / 36 / 5; escape 9 / 17 / 2.

Primary (H-SR / RESIN / PN): cap_control 48 / 47 / 5; cap_contest 14 / 15 / 1; radar_trap 1 / 2 / 0; island_dive 2 / 3 / 0; reposition 8 / 4 / 0; damage 13 / 12 / 2; escape 5 / 7 / 2; none 9 / 13 / 4.

Damage threshold: 63 smokes reach 20,000; 93 qualify by either rule (79 target_rich, 7 hunt, 7 island_killer).

Two tags never fire. hydro_trap: 33 smokes had hydro run from inside, but no enemy gained the sonar flag within range during a run, most likely because enemies that close are already spotted by ships and the game keeps the first reason. counter_smoke: no enemy smoke appeared within 25 s and 3 km of one of ours; in the Grand Final game the nearest pair is 109 s and 2.9 km apart.

cap_control is the most common tag (100 of 217) because a radar cruiser sits in most of these smokes near a cap. Restricting it to contested caps gives 83; that is the first thing to tune.

## 2. Location context

Map profiles live in `smoke/maps/<map>.yaml` (DRAFT). Each holds the layout, terrain (land share from the map's land layer: island-heavy at 8% or more, mixed at 4% or more, open water below), the spawn centres, each cap's grid square and role from each spawn, and the zones as grid squares. Zones are thirds of the map across the spawn-to-spawn axis, measured from the map centre (west, centre, east; north, centre, south on corner-spawn maps); notable spots are left for Sean.

Per smoke:

- **zone**: the profile zone of the grid square the smoke was laid in.
- **lane**: left, centre or right from the smoker's team's spawn, facing the enemy spawn. The centre band is one eighth of the map side either side of the spawn axis.
- **cap role**: the nearest contested cap (else the nearest cap) projected on the spawn axis: home below 40% of the way, enemy above 60%, centre between; flank when the cap sits outside the centre band.
- **front-line distance**: signed distance from the midpoint between the two fleets (centroids of living ships) at activation, positive toward the enemy. Nearest-enemy distance is kept alongside.
- **caps in range**: caps within stock gun range of a ship of the smoking team while it stood inside the smoke (the supported caps field).
- **land distance**: from the smoke origin to the nearest land pixel.

Counts: lane left 86, centre 51, right 80; cap role centre 162, enemy 47, home 8.

## 3. Smokees

A smokee is an allied ship the smoke covered: inside it, firing from behind it, or with the smoke between it and an enemy in its line of fire (an enemy within 15 km), at any 2 s sample. Each carries how it was covered first, the seconds covered, its credited damage and kills, and every detection while covered: radar, hydro, smoke fire penalty (the smoke flag), aircraft, submarine, proximity (an enemy within 2 km; inferred when it comes from the ship flag, direct when it comes from the x-ray flag) and surface lit (the ship flag with no enemy within 2 km: an enemy had line of sight, so the smoke failed). Averages 2.0 smokees per smoke; detections over all smokees: surface lit 155, radar 94, smoke fire penalty 57, aircraft 6, hydro 5, proximity 1.

## 4. How to compare clans fairly

- Compare within smoke type and purpose, not across them. A cap_control smoke by a destroyer with a Des Moines in it is a different play from a battleship exhaust smoke; the Clans charts default to destroyer smokes for this reason, and every filter on the site carries class and type.
- State n on every number. Fourteen PN smokes support anecdotes, not rates.
- Separate the group stage from the playoffs; opponents differ, and the playoff set is partial (only series with H-SR or RESIN replays).
- Account for game state: a kiting escape smoke while behind on points is not a failed push. The record carries the score at activation and capture, and escape uses it.
- Account for opponent strength. H-SR and RESIN met different opponents; games.csv carries the opponent and winner for grouping.
- Smoke damage is association, not proof. It credits shells fired from or through the smoke; the smoke did not cause the damage, and the shooter's own position and target choice matter as much.
- Movement, island_dive, reposition, hunt, island_killer and escape are inferred from positions and flags; their confidence is honest about how far the data supports them. Low-confidence tags are listed in `REVIEW-ROUND5.md` for hand review.
