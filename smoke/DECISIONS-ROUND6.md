# Round 6 decisions (4 Nov 2026)

Each entry: the decision, why, and the alternative. Sean approved the Step 0 assumptions as written; the rest came up while building. Thresholds live in `crates/smoke-signals/src/classify.rs` as named constants.

## Damage split

- **Concealed damage is credited smoke damage whose shooter was undetected at the firing moment; detected damage is the rest.** The damage spike already records the shooter's visibility flags at fire time for every event, so the split is exact per shot and the fires a shot started follow it. Alternative: judge at the hit moment, which would call a shell "detected" because the shooter was lit while it was in the air.
- **The reason is the shooter's visibility flags at fire time, one reason per shot, in the priority radar, hydro, smoke fire penalty, aircraft, submarine, proximity, surface lit.** The game sets one reason at a time almost always; the priority only settles ties. Proximity is inferred from the ship flag with an enemy within 2 km, as the smokee detections already did; everything else is a flag the replay carries.
- **The behind-smoke line-of-sight test sees every ship in the roster.** It had only seen ships that dealt damage or died, so an enemy that fired nothing all game could not make a smoke "needed"; the proximity inference for the detection reason needed the full roster too. Two smokes in the Okinawa game (-BN- vs H-SR) gained credit: Yamiyonohik's 46513 went from 80,520 to 91,412 and keeps Smoke of the Tournament. Alternative: leave the old list, which would have moved the award to a smoke that only led because of the gap.
- **Unknown stays its own bucket.** 144 of 5,596 credited events have no visibility record at fire time (the shooter had no flag sample yet); none of them is credited to a smoke, so every smoke's total is concealed plus detected. The bucket is in the data and only shown when it is not zero.
- **DD damage is total smoke damage, concealed and detected, on enemy destroyers**, by the victim's ship class from the roster. Same credit rules as smoke damage.
- **Awards that rank on damage use concealed damage, with total damage as the tie-break:** Smoke of the Tournament, Most Selfish Smoke (the owner's concealed damage), Golden Cloud, Best in Haze and the clan "most concealed smoke damage" award. Radar Bait's tie-break is damage taken, not dealt, and is unchanged. Leaderboards show total, concealed and DD damage side by side.

## Movement

- **Stationary: displacement under 500 m from the start to the end of emission, judged before the direction labels, confidence high.** It is measured, not inferred, so it carries no angle doubt. 32 smokes, all of which were low-confidence direction tags before. Alternative: path length instead of displacement, which would make a ship circling inside its smoke "moving".

## Smokees

- **One table replaces "Shooters credited" and "Smokees": the smoker, every ally the smoke covered, and every credited shooter.** A credited shooter that was never covered at a sample (it fired between samples) is listed with no covered time and the role its credited shots imply (inside or behind); it does not make the smoke a screen.
- **The smoker stands in its own smoke while laying.** The replay shows each puff some seconds after the ship passed, so a moving destroyer was never "inside" by the sample test: 42 smokers were missing from their own smokee list. The rule marks the owner inside at every sample between the start and end of emission. Alternative: trust the sample test, which is wrong about the game.
- **Behind-smoke cover needs the shooter undetected at fire time.** The damage credit already required it; the smokee role now does too, and a shot fired while spotted does not count as cover.
- **Undetected share is the share of the ship's covered time (between consecutive covered samples) with no detection flag.** Time with no flag sample is left out of both sides. The reasons for the rest are the detection kinds at those samples, weighted by time.
- **Damage taken while a smokee counts every hit within 2 s of a covered sample**, all weapons, since the ship was covered then.
- **Badges: the smoker is 1, then by total damage, then seconds covered, then entity id.** The number is drawn at the ship's position at the frame's clock; a ship that was dead or off the crop gets no badge.

## Classifier

- **cap_control: the cap must be the contested cap, and a concealed radar ship inside the smoke must have activated radar at a moment when its radar covered at least 90% of that cap.** 24 smokes (H-SR 12, RESIN 11, PN 1), down from 100. The coverage is computed at the activation moment, not the best moment of the smoke's life.
- **damage: 20,000 or more only.** 63 smokes (H-SR 35, RESIN 26, PN 2). target_rich, hunt and island_killer are computed for every smoke that dealt damage and describe it; they no longer qualify a smoke. The "two or more enemies hit" rule survives only as the `damage_qualified` field.
- **counter_smoke: 45 s window, 12 km, the nearest enemy smoke in that window.** 11 smokes (H-SR 4, RESIN 5, PN 2). Two candidates sit at 12.0 km rounded (H-SR 90086 on Hotspot and 108992 on Land of Fire, both Grand Final); their reasons say "borderline" and the run log of the batch notes them. Alternative: the most recent enemy smoke rather than the nearest, which the 3 km rule used.
- **hydro_trap stays in the data and off the site.** It never fires (see round 5).

## Maps page

- **The map image sits inside the overlay SVG as an image element.** Overlay and map share one coordinate system, so no CSS can separate them; the column also no longer stretches. Alternative: keep the image and SVG as siblings with an aspect-ratio rule, which still depends on CSS.
- **Grid squares follow the game: numbers 1 to 10 across the top, letters A to J down the side.** The site had them transposed (Big_Boy69's Somers at D7 read G4). Fixed in the site, the enriched CSV and all seven map profiles, whose zone and cap squares were rewritten by script.
- **The overlay test** (`smoke/tools/test_overlay.py`) projects the puff path of one smoke per map (four maps) onto its capture frame with the site's projection and checks for smoke or the gold outline within a puff radius of every puff; it also checks the grid of smoke 224000 is D7 and that every map on the Maps page has its image inside the overlay SVG. It writes an overlay image per smoke for eyes.

## Frames

- **The zoomed view is a second, bare render:** no player names, ship names, HP bars, range circles, planes, buildings, trails, armament or weather; icons, headings, smoke, torpedoes, caps, fire lines and damage labels stay. The capture frame's zoom covers the smoke, every smokee and every damaged enemy at that clock and both ends of every drawn fire line, padded by 1 km, never less than half the map, magnified to the map's own size (so the magnification falls from 2x toward 1x as the crop grows). The activation frame's zoom covers the smoke alone, and clips skip the zoom. The batch takes about 7 minutes instead of 3.
- **The full frame keeps ship names and drops player names** (`show_player_names = false` in config.toml).

## Site wording

- **Radar bait is "possibly a mistake"** and **selfish smoke is a tendency, not a flaw**; both say that a high rate for a clan or player is the signal. Radar-punished share and selfish smoke share moved from Risks to a Tendencies group, which is not ranked "lower is better"; smoke deaths stay in Risks.
- **The Classification block shows plain values with a confidence dot**; the reason and the numbers are in the tooltip. "Tags" is now "Hand tags". "Cap proximity at capture" and "Contested cap" merged into "Distance to contested cap" (the life-average edge distance; the capture proximity is in its tooltip).
