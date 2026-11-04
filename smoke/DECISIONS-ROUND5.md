# Round 5 decisions (overnight run, 4 Nov 2026)

Each entry: the decision, why, and the alternative. Thresholds live in `crates/smoke-signals/src/classify.rs` as named constants.

## Scale of the map

- **Ships cover map distance at about 2.6 times their listed speed.** Measured from the replays: a destroyer sails 2 to 5 km of map while laying a 40 to 55 s smoke, and ships move 2 to 3.8 world units (60 to 110 m) per second. Every distance threshold below is in map metres as the replay records them. Alternative: scale thresholds to listed knots, which would make every movement "stationary".

## Movement (fuzzy; confidence high / medium / low)

- **Reference point: the centroid of the 3 nearest living enemies at laying start.** One nearest enemy is noisy; the whole fleet is too far away to say "closing". Alternative: nearest enemy only.
- **Angle thresholds: pushing at 60 degrees or less between the laying displacement and the line to the enemy group, kiting at 120 degrees or more, horizontal between.** Thirds of the half-circle, no bias. Alternative: 45 / 135.
- **Displacement: start of emission to end of emission, straight line.** The puff path is a close match but the smoker's own track is what "movement" means. Alternative: puff path length.
- **Confidence: high when the displacement is 2.5 km or more, medium at 1 km or more, low below; one step down when the angle is within 15 degrees of a threshold.** Short paths make the angle meaningless. 23 smokes have no movement because the smoker or the enemies had no position at laying start (second-perspective recorders with no live position); they show "unknown".

## Coverage

- **Precedence: stacked over screen over selfish.** Stacked is the most specific description of how the smoke protects; screen and selfish are each other's complement by the existing selfish definition. All three booleans are kept in the record. Alternative: screen over stacked (a stacked smoke that a cruiser actually fired from would then read "screen").
- **Stacked only applies to destroyer smokers**, as the brief says: within 2.5 km of an allied cruiser or battleship at the start of laying.
- **Screen includes teammates who sheltered inside without firing**, since the selfish definition counts them as benefiting.

## Purposes

- **cap_control counts any cap, not only a contested one.** The brief says "a cap". It fires on 100 of 217 smokes (46%), because a Des Moines or Gdansk sits in most of these smokes near a cap. Alternative, logged for tuning: only a contested cap (83 smokes). The coverage share is the radar circle's intersection with the cap area, as the radar cap coverage metric already does.
- **cap_contest: inside or within 1 km (edge to edge, averaged over the smoke's life) of a contested cap.** Reuses the contested-cap share rule. Alternative: inside only.
- **radar_trap: the existing offensive radar rule (enemies gained the radar flag within range during a radar run from inside the smoke), when the smoke is not cap_control.** As the brief orders it.
- **hydro_trap: the same rule with hydro.** 33 smokes had hydro run from inside, none spotted a new enemy, so the tag never fires. Likely cause: an enemy within 5 to 6 km is already spotted by ships, and the sonar flag only appears when it is the first reason. Alternative: count any enemy within hydro range during the run (would over-count).
- **counter_smoke (added by Sean overnight): laid within 3 km of an enemy smoke, 0 to 25 s after that smoke appeared.** 3 km is the distance at which the two smokes are in the same fight; the time is Sean's. Zero smokes qualify. In the Grand Final game the nearest enemy pair is 109 s and 2.9 km apart, so the time window is what limits it. Logged as a tuning candidate: 60 s would start to fire. Priority: after hydro_trap, before island_dive.
- **island_dive: a covered ship moved at least 2 km under the smoke and ended within 1 km of land, and either started further than 1 km from land or moved 4 km or more.** Confidence high at 4 km or more ending within 600 m of land, medium at 3 km or more, low otherwise. Land is the alpha channel of the map's land layer (`minimap.png`); it includes the island art, so "0 m from land" means the ship sat against the drawn coastline. Alternative: a proper collision mesh, which the game data dump does not carry.
- **reposition: a covered ship moved at least 3 km under the smoke and was never detected while covered.** Confidence high at 6 km, medium at 4 km, low at 3 km. "Covered" is inside the smoke or with the smoke between it and an enemy within 15 km. island_dive is also tagged reposition when both hold, with island_dive as the primary.
- **damage: 20,000 or more smoke damage, or two or more enemies hit.** 63 smokes reach 20,000; 93 qualify by either rule. Sub-labels: target_rich (2 or more enemies hit), island_killer (one enemy whose mean position while hit was within 1 km of land; high confidence within 500 m), hunt (one enemy further from land; high at 1.5 km or more). The brief asks for the 20k count so Sean can tune it.
- **escape: movement is kiting and at least one of: spotted at activation, HP at or below 50%, behind on points.** Confidence high with two conditions and high movement confidence, medium with spotted or low HP and non-low movement confidence, low otherwise. Alternative: require two conditions.
- **A smoke with none of the tags has primary purpose "none"** (26 smokes). Alternative: an "other" bucket.
- **Rule-based tags carry no confidence; fuzzy tags do.** Every tag carries a one-line reason, shown on the smoke page and in the review list.

## Location

- **Lane: lateral offset of the smoke origin from the axis between the two spawn centres, from the smoker's team's point of view facing the enemy; centre band is one eighth of the map side either side of the axis** (a quarter of the map), left and right beyond it. Alternative: thirds of the map, which would mislabel Hotspot where both spawns sit east of centre.
- **Cap role of the nearest contested cap (else the nearest cap): the cap centre projected on the spawn axis; below 40% of the way is home, above 60% is enemy, between is centre. Flank when the cap is outside the centre band.**
- **Front-line distance: signed distance from the midpoint between the two fleets' centroids (living ships) at activation, positive toward the enemy fleet.** Nearest-enemy distance is kept alongside.
- **Zones in the map profiles are thirds of the map across the spawn-to-spawn axis, measured from the map centre (west / centre / east, or north / centre / south on corner-spawn maps).** They are map-fixed so they can be drawn; lanes are spawn-relative. Notable spots are left for Sean to add; the profiles are marked DRAFT.
- **Terrain in the profiles: island-heavy at 8% or more land, mixed at 4% or more, open water below**, from the land layer.
- **Caps in range: the existing supported caps field, exposed under the new name.**

## Smokees

- **A smokee is an allied ship that was inside the smoke, fired a shot with the smoke in its `behind_smokes`, or had the smoke between it and an enemy within 15 km, at any 2 s sample of the smoke's life.** Alternative: inside only.
- **Detection kinds come from the replay's visibility flags at the samples where the ship was covered: radar (RLS or personal RLS), hydro (sonar), smoke fire penalty (the smoke flag), aircraft (plane flags), submarine (pinger or locator).** The ship flag splits into "proximity" (inferred: an enemy within 2 km at that sample) and "surface lit" (an enemy had line of sight). The x-ray flag is proximity from the flag itself. Only "proximity" from the ship flag is inferred; everything else is a flag the replay carries.

## Site

- **Awards: destroyer lens and all-smokes lens only**, with a toggle on Home and Players. The full class x type lens applies to the Clans charts, clan page tiles, the Smokes table, Maps and player pages. Rendering 20 award sets with clips was not worth it.
- **Player badges show both lenses** (gold for destroyer, grey for all).
- **Clans charts are rendered in the browser from precomputed values for every lens**, sorted best first in the browser.
- **The smoke page's Classification block sits above the three stats groups; the Smokees table sits below them.**
- **Analysis page, Home key terms and everything else from round 4 are unchanged.**
