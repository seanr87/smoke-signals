# Smoke Signals analysis method (DRAFT, round 6, 4 Nov 2026)

How every smoke in King of the Sea XIX NA is classified, how its damage is split, what the location fields mean, and how to compare clans without fooling yourself. Numbers are from batch `output/20261104-180332` (217 smokes: H-SR 100, RESIN 103, PN 14). Thresholds are constants in `crates/smoke-signals/src/classify.rs`; the reasoning behind each is in `DECISIONS-ROUND5.md` and `DECISIONS-ROUND6.md`.

A note on scale: the game compresses distance, so ships cover map distance at about 2.6 times their listed speed. A destroyer lays a 40 to 55 s smoke over 2 to 5 km of map. All distances here are map metres as the replay records them.

## 1. The four structured fields

Every smoke carries four fields. Rule-based fields apply to all 217 smokes; fuzzy fields carry a confidence (high, medium, low) and are labelled "auto-tagged" on the site, where a coloured dot shows the confidence and the numbers sit in the tooltip.

### 1.1 Smoker (mechanic, not purpose)

- `smoker_class`: destroyer, cruiser or battleship, from the ship's class.
- `smoke_type`: standard, cruiser (a standard variant whose puffs last 60 s or less, Svea), exhaust (Italian oil smoke), crawling (none in this replay set).
- Special cases flagged separately: `svea` (13 smokes), `battleship_exhaust` (10, all Conte Verde and C. Colombo), `battleship_crawling` (none).

Counts: H-SR 89 destroyer / 3 cruiser / 8 battleship; RESIN 87 / 15 / 1; PN 10 / 3 / 1.

### 1.2 Movement (fuzzy)

How the smoker moved while laying, judged against the centroid of the 3 nearest living enemies at the start of emission.

- Displacement: the smoker's position at the start of emission to its position at the end of emission (straight line).
- **stationary** (round 6): displacement under 500 m, judged first, confidence high (it is measured, not inferred).
- Otherwise the angle between that displacement and the line to the enemy group: **pushing** at 60 degrees or less, **kiting** at 120 degrees or more, **horizontal** between.
- Confidence: high when the displacement is 2.5 km or more, medium at 1 km or more, low below 1 km (the angle means little when the ship barely moved); one step lower when the angle is within 15 degrees of a threshold.
- Unknown (23 smokes): the smoker or every enemy lacked a position at laying start. These are mostly second-perspective recorders, whose live position the merge never receives.

Counts: H-SR 8 stationary / 26 pushing / 39 horizontal / 13 kiting / 14 unknown; RESIN 22 / 24 / 31 / 19 / 7; PN 2 / 5 / 3 / 2 / 2. Confidence over all: 95 high, 69 medium, 30 low (62 low before stationary existed; all 32 stationary smokes were low-confidence direction tags).

### 1.3 Coverage (rule-based)

Who the smoke protected. Precedence: stacked, then screen, then selfish.

- **stacked**: a destroyer laid it within 2.5 km of an allied cruiser or battleship at the start of laying.
- **screen**: it hid teammates who sat inside it or fired from behind it (the complement of selfish).
- **selfish**: no teammate other than the owner was ever inside it, and no teammate fired through it from behind (the round 2 definition). A tendency, not a flaw: some ships smoke selfishly by design, and how often a clan or player does it is a style signal.

All three booleans stay in the record. Counts: H-SR 50 stacked / 32 screen / 18 selfish; RESIN 35 / 36 / 32; PN 5 / 2 / 7.

### 1.4 Purpose (tactic tags)

Every tag that applies is recorded; the primary tag is the first in this priority order.

| Priority | Tag | Rule | Confidence |
| --- | --- | --- | --- |
| 1 | cap_control | A radar ship concealed inside the smoke activated its radar at a moment when the radar covered at least 90% of the contested cap's area | rule |
| 2 | cap_contest | The smoke stood inside, or within 1 km edge to edge on average, of a contested cap, without that radar play | rule |
| 3 | radar_trap | A concealed radar ship in the smoke ran radar and an enemy gained the radar flag within its range (the offensive radar rule), and the smoke is not cap_control | rule |
| 4 | hydro_trap | The same with hydro (kept in the data, hidden on the site) | rule |
| 5 | counter_smoke | Laid within 12 km of an enemy smoke, 0 to 45 s after that smoke appeared (the nearest such smoke) | rule |
| 6 | island_dive | A covered ship moved at least 2 km under the smoke and ended within 1 km of land (and started further away, or moved 4 km or more) | high at 4 km ending within 600 m of land, medium at 3 km, low otherwise |
| 7 | reposition | A covered ship moved at least 3 km under the smoke and was never detected while covered | high at 6 km, medium at 4 km, low at 3 km |
| 8 | damage | 20,000 or more smoke damage. The sub-label describes any smoke that dealt damage: target_rich (2 or more enemies hit), island_killer (one enemy whose mean position while hit was within 1 km of land), hunt (one enemy in the open) | rule for target_rich; island_killer high within 500 m of land; hunt high at 1.5 km or more from land |
| 9 | escape | Movement is kiting and at least one of: spotted at activation, HP at or below 50%, behind on points | high with two conditions and high movement confidence; medium with spotted or low HP; low otherwise |

A smoke with no tag has primary purpose "none" (53 smokes). "Covered" means inside the smoke or with the smoke between the ship and an enemy within 15 km.

Counts, any tag (H-SR / RESIN / PN): cap_control 12 / 11 / 1; cap_contest 31 / 35 / 3; radar_trap 2 / 7 / 1; hydro_trap 0 / 0 / 0; counter_smoke 4 / 5 / 2; island_dive 10 / 15 / 1; reposition 29 / 16 / 2; damage 35 / 26 / 2; escape 8 / 12 / 2.

Primary (H-SR / RESIN / PN): cap_control 12 / 11 / 1; cap_contest 31 / 35 / 3; radar_trap 2 / 4 / 0; counter_smoke 2 / 0 / 2; island_dive 4 / 4 / 0; reposition 14 / 6 / 1; damage 10 / 10 / 1; escape 4 / 6 / 1; none 21 / 27 / 5.

Round 6 moved three rules. cap_control went from 100 smokes (any cap, best coverage at any moment) to 24 (the contested cap, and the radar must have been activated while covering it). The damage purpose went from 93 (20k or two enemies hit) to 63 (20k only); the sub-labels now describe every smoke that dealt damage. counter_smoke went from 0 (25 s, 3 km) to 11 (45 s, 12 km); two of the eleven sit at 12.0 km rounded and are marked borderline in their reason. hydro_trap still never fires: 33 smokes had hydro run from inside, but no enemy gained the sonar flag within range during a run, most likely because enemies that close are already spotted by ships and the game keeps the first reason.

## 2. Damage: concealed, detected, DD

Smoke damage credits main-gun shells fired from or through a smoke by the smoking team, plus the fires they started (round 3 rules). Round 6 splits it by whether the shooter was detected at the firing moment:

- **concealed**: the shooter's visibility flags were clear when it fired. 2,853,287 of 3,090,143 smoke damage (92%) over the set; H-SR 95%, RESIN 90%, PN 90%.
- **detected**: the shooter was spotted when it fired. The reason is the flag set at that moment, one per shot in the priority radar, hydro, smoke fire penalty, aircraft, submarine, proximity (inferred: the ship flag with an enemy within 2 km), surface lit (the ship flag otherwise). Over the set: radar 175,348; surface lit 26,464; smoke fire penalty 22,175; hydro 11,722; aircraft 1,147.
- **unknown**: no flag sample at the firing moment. Zero on every smoke in this set (144 ledger events have it, none credited to a smoke).

Every damage table on a smoke page (enemy ships damaged, smokees) shows concealed and detected side by side; awards that rank on damage use concealed damage with total damage as the tie-break.

**DD damage** is smoke damage, concealed and detected, dealt to enemy destroyers: H-SR 190,625 (8,665 per game), RESIN 263,220 (10,968 per game), PN 13,677 (1,954 per game).

## 3. Location context

Map profiles live in `smoke/maps/<map>.yaml` (DRAFT). Each holds the layout, terrain (land share from the map's land layer: island-heavy at 8% or more, mixed at 4% or more, open water below), the spawn centres, each cap's grid square and role from each spawn, and the zones as grid squares. Grid squares follow the game: numbers 1 to 10 across the top, letters A to J down the side (round 6 fixed a transposition; Big_Boy69's Somers at 18:59 on Hotspot is D7). Zones are thirds of the map across the spawn-to-spawn axis, measured from the map centre (west, centre, east; north, centre, south on corner-spawn maps); notable spots are left for Sean.

Per smoke:

- **zone**: the profile zone of the grid square the smoke was laid in.
- **lane**: left, centre or right from the smoker's team's spawn, facing the enemy spawn. The centre band is one eighth of the map side either side of the spawn axis.
- **cap role**: the nearest contested cap (else the nearest cap) projected on the spawn axis: home below 40% of the way, enemy above 60%, centre between; flank when the cap sits outside the centre band.
- **front-line distance**: signed distance from the midpoint between the two fleets (centroids of living ships) at activation, positive toward the enemy. Nearest-enemy distance is kept alongside.
- **caps in range**: caps within stock gun range of a ship of the smoking team while it stood inside the smoke (the supported caps field).
- **land distance**: from the smoke origin to the nearest land pixel.

Counts: lane left 86, centre 51, right 80; cap role centre 162, enemy 47, home 8.

## 4. Smokees

A smokee is an allied ship the smoke covered: inside it, firing undetected from behind it, or with the smoke between it and an enemy in its line of fire (an enemy within 15 km), at any 2 s sample. The smoker counts as inside its own smoke while laying it (the replay shows each puff some seconds after the ship passed, so a moving destroyer never tested inside), and every credited shooter is listed even when it fired between samples. Each carries a badge (1 is the smoker, then by damage), a role (smoker, inside, behind, line of fire), the seconds covered, the share of that time undetected, the detection kinds while covered weighted by time (radar, hydro, smoke fire penalty, aircraft, submarine, proximity, surface lit), its credited damage split concealed and detected, the damage it took while covered, and its kills. The zoomed view on each smoke page draws the badge numbers on the ships.

Over the set: 469 smokee rows, 2.2 per smoke (217 smokers, 156 inside, 41 behind, 55 line of fire); the mean undetected share is 85%; covered time while spotted: surface lit 2,227 s, radar 1,801 s, smoke fire penalty 1,222 s, hydro 137 s, aircraft 23 s, proximity 8 s.

## 5. How to compare clans fairly

- Compare within smoke type and purpose, not across them. A cap_control smoke by a destroyer with a Des Moines in it is a different play from a battleship exhaust smoke; the Clans charts default to destroyer smokes for this reason, and every filter on the site carries class and type.
- State n on every number. Fourteen PN smokes support anecdotes, not rates.
- Separate the group stage from the playoffs; opponents differ, and the playoff set is partial (only series with H-SR or RESIN replays).
- Account for game state: a kiting escape smoke while behind on points is not a failed push. The record carries the score at activation and capture, and escape uses it.
- Account for opponent strength. H-SR and RESIN met different opponents; games.csv carries the opponent and winner for grouping.
- Smoke damage is association, not proof. It credits shells fired from or through the smoke; the smoke did not cause the damage, and the shooter's own position and target choice matter as much. Concealed damage is the part the smoke can claim; detected damage was fired by a ship the enemy could see anyway.
- Radar-punished share and selfish share are tendencies, not scores. A radar spot is possibly a mistake, and a selfish smoke is a style; a high rate for a clan or player is the signal, one instance is not.
- Movement, island_dive, reposition, hunt, island_killer and escape are inferred from positions and flags; their confidence is honest about how far the data supports them. Low-confidence tags are listed in `REVIEW-ROUND5.md` for hand review.
