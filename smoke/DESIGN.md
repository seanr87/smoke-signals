# Smoke Signals: Design Doc and Source of Truth

Owner: Sean. Last full revision: 4 Nov 2026, after Phase 2 round 6. Method details: `smoke/ANALYSIS.md`; decisions: `smoke/DECISIONS-ROUND5.md` and `smoke/DECISIONS-ROUND6.md`; hand-review list: `smoke/REVIEW-ROUND5.md`; map profiles: `smoke/maps/<map>.yaml` (DRAFT). This document is the only source of truth for the project; a fresh session should need nothing else. Rules in `smoke/CLAUDE.md` and the fork's `AGENTS.md` still apply.

Live site: https://seanr87.github.io/smoke-signals/

## 1. Goal and scope

For every smoke laid by H-SR, RESIN and PN in King of the Sea XIX NA, the tool produces two minimap frames, a zoomed view of each, a metadata record and (for award smokes) a clip, then builds a static site that compares how the three clans use smoke. The goal is to learn how competitive teams use smoke effectively.

- Teams: H-SR (NA regional winner), RESIN (runner-up), PN (our clan, the comparison). PN played the group stage only.
- Games: 45 played games in the replay set (group stage and playoffs for H-SR and RESIN, group stage for PN); 43 of them have at least one analysed smoke. 217 smokes: H-SR 100, RESIN 103, PN 14.
- Framing: a few hundred smokes supports descriptive patterns and strong examples, not causal claims. Purpose and intent tags are hand work that has not started; the site no longer says so on every page.

## 2. Status

| Phase | Scope | State |
| --- | --- | --- |
| 1. Prototype (M1 to M4) | Grand Final G1, H-SR only: pipeline, smoke detection, frames, clips, Tier 1 and 2 metrics, damage spike, golden test | Done 3 Nov 2026 |
| 2. Demo site, round 1 | Replay inventory, batch over every game, awards, first static site, GitHub Pages | Done and published 3 Nov 2026 |
| 2. Demo site, round 2 | Contested caps, in-game map names, cruiser smoke type, Maps paths and filters, Games page | Done and published 3 Nov 2026 |
| 2. Demo site, round 3 | One-smoke-per-shot credit, shell and fire scope with reconciliation, ally-only and offensive radar, cap support and outcome metrics, Home/Analysis/Clans/Players/Smokes/Maps/Games lineup, full bracket, diagram thumbnails, inset dropped, mobile | Done and published 3 Nov 2026 (commit 83d5e48a on `smoke-signals`) |
| 2. Demo site, round 4 | Kills from smoke, smoke deaths, shooter and target tables, 14 km ship reach, half-map zoomed view with fire lines; map-crop thumbnails, Analysis folded into Clans (grouped charts, best first), Home key terms, smoke page in three groups, Maps filters fixed plus ships pie, Smokes table reworked, player chart labelled and clickable | Done and published 3 Nov 2026 |
| 2. Demo site, round 5 | Classification of every smoke (smoker, movement, coverage, purpose tags with priority and confidence, counter_smoke), location context (map profiles, zone, lane, cap role, front line, caps in range), smokees with detection kinds, class and type lenses sitewide with destroyer defaults, Maps zone overlay, ANALYSIS and DECISIONS docs, review list, r5 export | Done and published 4 Nov 2026 (overnight, no approval stops) |
| 2. Demo site, round 6 | Concealed vs detected damage with reasons, DD damage, stationary movement, cap_control on the contested cap with radar activated, damage purpose at 20k only, counter_smoke at 45 s and 12 km, merged Smokees table with badges, bare zoomed view sized to the smokees and targets, Maps overlay and grid orientation fixed with an overlay test, Tendencies group and softer wording, r6 export | Done and published 4 Nov 2026 |
| 2. Full field, round 7 | Every clan and game (171 games, 341 replays, 30 clans): inventory of the whole tournament, one run per team per game, own-run rosters, one-sided runs, offset search to 12 s, torpedo classification by dead reckoning with a victim-aware floor, secondary and airstrike kinds, owner note only without an activation, standing sanity script, STEP reports in smoke/STEP*.md | Analysis done 16 Nov 2026; site plan approved, build pending |
| 3. Interactive | Tagging, comments, hosting, login | Decided after the demo is presented |

Deferred past the demo: build data (commander skills and upgrades) and effective smoke stats; hand tagging (pages show "untagged"); clips for every smoke; a second golden test game; image compression; the desktop app integration.

## 3. Repository, build, test, run, publish

The work lives in a fork of [landaire/wows-toolkit](https://github.com/landaire/wows-toolkit) (MIT), GitHub `seanr87/smoke-signals`, branch `smoke-signals`, checked out at `C:\Users\soreill5\KOTS Analysis\wows-toolkit`. The fork's conventions apply: no AI attribution in commits, ASCII only, short commit messages. `jj` is preferred by the fork's AGENTS.md but is not installed, so `git` is used.

```
crates/smoke-signals/            the smoke_signals program (Rust, edition 2024)
  src/analysis.rs                smoke tracking, owner, type, cap sampling, cap metrics, radar, spike call
  src/damage.rs                  damage ledger merge, weapon classification, smoke credit
  src/classify.rs                round 5: movement, coverage, purpose tags, location, smokees, land mask
  src/tier2.rs                   ships inside smokes, detection flags, consumable ranges
  src/state.rs                   Tier 1 state at a moment, cap proximity
  src/frames.rs  clips.rs        frames, zoom images, clips
  src/records.rs  output.rs      the metadata record, CSV and JSON writers
  src/batch.rs  main.rs          inventory-driven batch, CLI
  tests/golden.rs  determinism.rs
smoke/DESIGN.md                  this document
smoke/CLAUDE.md                  project rules
smoke/inventory.csv              every game: match id, stage, round, map, teams, replays, result
smoke/tools/build_site.py        static site builder
smoke/tools/publish_site.py      GitHub Pages publisher
smoke/tools/export_data.py       data zip (smokes, games, clans, breakdown, ship classes)
smoke/maps/<map>.yaml            DRAFT map profiles (layout, terrain, caps, zones)
smoke/ANALYSIS.md  DECISIONS-ROUND5.md  REVIEW-ROUND5.md   round 5 method, decisions, review list
smoke/tests/golden_gf_g1_hsr.csv golden test reference
smoke/config.example.toml        copy to config.toml (gitignored) and set paths
replays/  game_data/  output/  smoke-site/  config.toml     all gitignored
```

**Toolchain.** Rust 1.97 via rustup (pinned by `rust-toolchain.toml`). In Git Bash prepend `/c/Users/soreill5/.cargo/bin` to PATH. Python 3 for the tools; run it with `-I` (and `-X utf8` for the site builder) because replays and downloaded data are untrusted input. Chrome is installed and used headless for screenshots.

**Build and test.**

```bash
cargo build -p smoke-signals --release --offline
cargo test -p smoke-signals --release --offline
```

The tests are 22 unit tests, the golden test (`smoke/tests/golden_gf_g1_hsr.csv`: Grand Final G1 H-SR smokes must match by player, ship, type, variant and activation and capture clocks within tolerance, with no owner flag) and the determinism test (the analysis run twice gives identical smokes.csv and smokes.json). Both integration tests need `config.toml`, the replays and the game data; set `SMOKE_SIGNALS_SKIP_GOLDEN=1` to skip them elsewhere.

**Analyse every game (the batch).** Reads `smoke/inventory.csv`, finds `replays/<game folder>/`, uses the analysed team's own replay as the primary and merges the opponent's, one run per team in scope, and writes `output/<timestamp>/` with `smokes.json`, `smokes.csv`, `jobs.json`, `run_log.md` and `games/<run>/` (game.json, smokes.json, damage_spike.json, damage_events.csv, frames/, clips/). About 150 s for 53 runs with `--jobs 6`.

```bash
target/release/smoke_signals.exe --config config.toml batch --jobs 6
target/release/smoke_signals.exe --config config.toml maps --names "Hotspot,Loop,Okinawa,Land of Fire,Mountain Range,Sleeping Giant,Sea of Fortune"
target/release/smoke_signals.exe --config config.toml batch --jobs 5 --matches 7924,8178,7901,7981,8147 --clips 46513,106317,27145,174224,120803 --clip-speed 5 --clip-bitrate-kbps 1200
```

The second command exports the minimap images and `maps.json` (with in-game titles) that the site needs; the third renders the award clips (the ids are the current winners). Batch options: `--matches`, `--teams`, `--maps`, `--no-frames`, `--clips <ids>`, `--clip-speed`, `--clip-bitrate-kbps`. Never delete an output folder; every run gets its own timestamp. A full batch with frames takes about 7 minutes (the zoomed view is a second render). Current data: batch `output/20261104-180332`, maps `output/20261103-143026/maps`, clips in `output/20261103-185636/site-clips` (the award clips as `<match>_g<n>_<id>.mp4`, the folder the builder reads).

**Build the site.** Clips are passed as a folder of `<smoke_id>.mp4`.

```bash
python -I -X utf8 smoke/tools/build_site.py --batch output/<batch> --maps output/<maps>/maps --clips <folder of id.mp4> --out smoke-site
```

The builder also copies the batch's `smokes.csv` to `data/smokes.csv` on the site, and `smoke/tools/export_data.py --batch <batch> --maps <maps>` zips `smokes.csv`, `games.csv` (played games with winner, end clock and phase) and `clans.csv` (every Clans chart value) for sharing. The builder prints the award winners. `smoke-site/` is gitignored and about 317 MB; the fork's own tracked `site/` folder must not be touched. A rebuild overwrites frames that are newer in the batch and leaves other old files alone (stale clips must be removed by hand).

**Verify.** Serve `smoke-site/` locally (`python -m http.server 8765 --directory smoke-site`; the desktop app's launch entry `smoke-site` does the same) and take headless screenshots of every page type:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=8000 --window-size=1280,2400 --screenshot=out.png http://localhost:8765/maps.html
```

Headless Chrome will not shrink below about 500 px, so the phone layout is checked in the desktop app's browser pane at 375 px instead. A link check walks every href, src and CSS url() in the built pages, ignoring in-page `#` fragments (301 pages, about 5,700 links, none missing in round 6) and greps the visible text for internal map names.

**Overlay test (round 6).** `python -I -X utf8 smoke/tools/test_overlay.py --batch output/<batch> --maps output/<maps>/maps --site smoke-site` decodes the capture frame of one smoke per map (four maps), projects its puff path with the site's projection and the frame's map offset, and fails unless smoke or the gold outline lies within a puff radius of every puff; it also checks that smoke 224000 is in grid D7 and that every Maps page map has its image inside the overlay SVG. It writes `overlay-test/overlay_<smoke>.png` under the batch for eyes. Run it with the Rust tests before publishing.

**Publish.** GitHub Pages serves the `gh-pages` branch, which holds only the built site as one commit; every publish replaces the branch.

```bash
python -I smoke/tools/publish_site.py --site smoke-site --work C:/Users/soreill5/AppData/Local/Temp/ss-pages --label "what changed"
```

The work folder must be a short path (Windows 260-character limit); the script sets `core.longpaths` and clears git's read-only objects on reuse. Pages builds in under a minute; check a new page returns 200 before reporting.

## 4. Inputs

**Replays.** From the tournament site ([match pages](https://wows-tournaments.com/king-of-the-sea-xix/na/matches), replays at `/api/matches/report/replay?id=<n>`). `smoke/inventory.csv` lists every game with both teams' replays under `replays/<game folder>/`. Both replays are always merged; the primary is the team being analysed. Games with no replay are listed as not played.

**Game data.** Pre-dumped data for build 15.9.0_13357625 from [landaire/wows-replay-data](https://github.com/landaire/wows-replay-data) in `game_data/` (content-addressed `common/` plus `<build>/metadata.toml` and `constants.json`). All KotS XIX replays are 15.9.0. Keep every build downloaded. Map display names come from the game's string catalog (`IDS_SPACES/<NAME>`), so "Mountain Range" and "Sea of Fortune" appear everywhere; the internal name (`58_RidgeNew`) stays in the metadata.

**Replay facts to remember.**

- Replay positions, smoke radii (15 = 450 m) and map sizes are in world units of 30 m; every `_m` and `_km` field is converted.
- The HUD countdown runs about 1.5 s ahead of battle start plus elapsed replay time; every `mm:ss` is the HUD value at that replay second.
- Each replay records the smoke activations its own team made and the enemies it could see; a second replay's recorder has no live merged position, so positions come from the pre-scanned timeline with a minimap fallback.
- A client is told about every hit in its area of interest, so the two perspectives report the same hit twice with a clock offset that is near constant within a game but differs between games (1 to 8.5 s seen over the full field).
- The results blob at the end of a replay carries every player's totals (`playersPublicInfo`, decoded with `CLIENT_PUBLIC_RESULTS_INDICES` from constants.json: damage, damage_main_ap, damage_main_he, damage_main_cs, damage_fire, and others).

## 5. Smoke definitions

A smoke is one smoke object in the replay. `view.smoke_screens()` gives its radius, origin and puff list; the list grows as puffs are laid and shrinks as they fade, with no owner and no timestamps, so the tool records the times itself.

**Lifecycle.** `t_activate` (the consumable is used), emission until `t_emission_end`, standing, `t_dispersed` (the object is removed). `t_created` is when the object appeared.

**Owner.** Candidates are the ships fitted with a smoke consumable. The owner is the nearest candidate that activated smoke in the 5 s before the object was created; a candidate with an activation beats a nearer one without only within 1000 m of the origin. Otherwise the nearest candidate is the owner and `owner_flag` is set with a note (no activation in the window; position from minimap samples only; nearest candidate more than 600 m away, which applies only without an activation since an activation confirms the owner). When the nearest positioned candidate is more than 2 km away, or there is none, and exactly one fitted ship alive at creation has no position at all (an unspotted enemy seen from one replay), that ship is the owner, flagged "owner inferred". Smoke objects are tracked from the primary replay only. Every record of a single-replay game carries `one_sided` = true, and the batch keeps the opponent's smokes from such a run as well as the primary team's.

**Types and capture moment.**

| smoke_type | Identified by | Base stats | t_capture |
| --- | --- | --- | --- |
| standard | Default destroyer variants (`Lvl_10_Gold`, `US_Lvl_10_Gold`) and long cruiser smokes (Smolensk 20 s / 89 s) | Emission 20 to 30 s, puffs last 89 to 130 s | Last new puff before the first puff fades |
| cruiser | A standard variant whose puffs last 60 s or less (Svea: 10 s / 40 s) | Emission 10 s, puffs last 40 s | As standard |
| exhaust | Variant title contains `Oil` (`IT_Oil_Verde`) | Emission 45 s, puffs last 10 s, no speed limit | End of emission |
| crawling | The crawling-smoke variant | To confirm; none in this replay set | End of emission |

Build modifiers lengthen emission (Harugumo 53 s observed against 20 s base). The record keeps observed and base values; `emission_cut_short` marks a smoker that died while emitting. One activation that creates several objects gives one record per object, linked by `activation_id`.

**Contested cap.** A cap is contested for a team at a moment when (a) the midline crosses it, (b) it lies wholly on the enemy's side of the midline, or (c) the enemy owns it. The midline is the line halfway between the two teams' spawn centres (`spawn_xy`, the mean of each team's first positions) at right angles to the line joining them. `cap_contested_reason` records the first reason that applied (midline, enemy_side, enemy_owned). Only control points of the game's `Control` kind count; Mountain Range's 10 km cap A is a real cap and counts like any other.

**Spawn labels.** The two spawns are told apart along the axis they are furthest apart on: north and south unless the east-west separation is 1.5 times larger. Every map in this set resolves to north and south, including the corner spawns on Loop and Okinawa.

**Time phases.** Fixed thirds of the 20-minute clock, counted as time elapsed from battle start: opening 0:00 to 6:40, mid 6:40 to 13:20, endgame 13:20 to 20:00. The phase a game ended in comes from its battle end clock. Axes that compare smokes across games use the fixed 20-minute scale labelled as time elapsed with the start on the left; a single game's own page fills its width with real minutes; per-smoke text keeps the in-game countdown clock, labelled.

## 6. Metric definitions and credit rules

Every metric is measured over the smoke's life unless stated. "Inside" a smoke: a ship's position within `radius` of any standing puff. "Undetected": the ship's visibility flags are 0; the flags also say why a ship is detected (BY_SHIP, BY_RLS radar, BY_SONAR hydro, IN_SMOKE fired from smoke).

### 6.1 Damage ledger

- Each replay's `receiveDamagesOnShip` events give attacker, victim, amount and clock, but not the weapon. Both replays are parsed and merged. The merge estimates each later replay's clock offset against the earlier ones as the most common clock difference (quarter-second bins, at least 10 pairs, searched up to 12 s) over same-attacker, same-victim, same-amount pairs, leaving out fire and flood ticks, then folds an event onto an unmatched earlier event within 0.8 s of that offset. A bin beyond 6 s wins only with at least twice the pairs of the best bin within 6 s, so a chance alignment of repeated equal hits cannot displace a real near peak; without a trusted estimate the fold uses offset zero and a 3 s window. The estimates are written to `damage_spike.json` as `perspective_offsets`. Without the offset, games with a 4 to 8.5 s skew doubled every ship's total.
- Reconciliation: for every ship, the ledger total and the ledger's shell-plus-fire total are compared with the game's own results (damage; damage_main_ap + damage_main_he + damage_main_cs + damage_fire). Each game page shows the per-ship table; the cross-game share is no longer on the site. Round 3 batch: ledger over game total averages 0.98 per game (range 0.71 to 1.16); shell-plus-fire averages 1.05 (0.81 to 1.36).

### 6.2 Weapon classification (`kind` on every damage event)

- shell: matched to a resolved shot hit (same attacker and victim, impact within 1 s; among several hits in the window the main battery's comes first, since a battleship's secondaries land within a second of almost every main-battery hit), or to the attacker's latest main-battery salvo within 25 s before the damage. A resolved hit settles the kind unless the tick is larger than a whole main-battery salvo could list: the event is a shell even when a torpedo of the attacker's passed the victim on the same tick (the torpedo damage given up this way is counted in `damage_spike.json` as `shell_hits_fitting_torpedo`). The salvo fallback considers main-battery salvos only, because a battleship's secondaries fire every few seconds and would claim main-battery hits.
- secondary: a shell whose resolved hit's or salvo's projectile is not one the ship's equipped main battery fires (the artillery component's `ammoList`). Not credited, and a fire tick that follows only secondary hits is unknown, not fire. When a ship's main-battery ammunition is unknown every shell counts as main.
- fire: the event sits in a tick train (a same-amount neighbour 0.7 to 1.4 s away on the same victim) and the attacker's latest shell or airstrike on that victim was within 75 s before it; the tick is credited like that shell or airstrike.
- airstrike: not a tick, no resolved shell hit, the amount is above the listed damage of one main-battery shell of the ship (a smaller tick with the squadron overhead cannot be told from a salvo and stays a shell), and an air-support squadron the ship launched is in flight (from 5 s after it appeared on the minimap to 10 s after it left) whose track, interpolated between the minimap samples, passed within 1,000 m of the victim at some clock in the 10 s before the damage (the bombs fall while the squadron flies on). The squadron packet names no launching ship: the owner is the one ship of the squadron's team whose ship param name matches the squadron param's ship name with the `AS` token removed, token for token, each squadron token a prefix of the ship's (`PHAD020_AS_UTRECHT` and `PHSC520_Utrecht`; `PHAD015_PRINS_V_O_AS` and `Prins_van_Oranje`); a squadron with no or several such ships is left out and counted (`airstrikes_without_owner`). Carrier squadrons and catapult planes are not airstrikes (plane category `airsupport` only); ASW strikes use the same rule.
- torpedo: not a tick, no resolved shell hit (or a resolved hit with a tick larger than a whole main-battery salvo, barrels times the largest shell's listed damage), and a torpedo the attacker launched 1 to 150 s earlier has its dead-reckoned track (origin plus direction times elapsed, in world units, stepped every 0.25 s) pass within 400 m of the victim's position at some clock within 12 s before or after the damage clock, and the amount reaches that torpedo's floor: 0.5 times the torpedo's listed damage (alpha over 3 plus the flooding part, from game params) times one minus the victim's torpedo protection (the equipped hull's stock flood probability; unknown protection takes nothing away). A finishing hit (the victim dies within 1 s) reaches any floor. The window exists because the victim's position is a held sample when it is not spotted and the hit is reported late. The view keeps a torpedo to the end of the replay, so its disappearance cannot mark the hit. The earlier run-length test compared world units with meters and matched almost nothing; the earlier flat 3,000 floor let large shell salvos through, and a 0.8 share rejected most real hits.
- flood: a tick train whose latest linked event is a torpedo.
- A torpedo's firing moment and position are its launch clock and the attacker's position then (fire source `TorpedoLaunch`), so `in_smokes`, `behind_smokes` and the credited shares are known for torpedo events as for shells. They still earn nothing: the shares only feed the uncounted list below.
- unknown: nothing recorded explains it (secondaries, shells with no salvo seen, and so on).
- Smoke damage is main-battery shells, airstrikes and the fires they start. Secondary, torpedo, flood and unknown damage are reported in `damage_spike.json` (events and damage by kind) and never credited. Each smoke also records `targets_not_counted`: the enemy ships hit from it by the smoker's team with those uncredited kinds (torpedo, secondary, flood, unknown; `damage`, `by_kind`, `sunk` when the hit was the victim's last), and the CSV column `damage_not_counted` sums them. The site lists them under the enemies table as not counted; the smoke's total and every metric stay main battery, airstrikes and fires only.

### 6.3 Smoke credit (one smoke per shot)

- A shot fired from inside a smoke credits that smoke alone. Inside two overlapping smokes, the first-laid one whose puffs still hide the shooter gets the credit; when its puff fades, credit passes to the next.
- A shot fired from outside any smoke by an undetected shooter credits the smokes that were needed, in equal shares: those whose standing puffs lay on the line from the shooter to at least one living enemy within the shooter's base detection range (hull `visibilityFactor`; 12 km when unknown), nearer the shooter than that enemy. If no smoke was needed, nothing is credited. Every ship in the roster counts as a possible enemy (until round 6 only ships that had dealt damage or died did, which under-credited two smokes in the Okinawa game).
- A fire tick is credited exactly like the shell or airstrike that started it.
- An airstrike is tested like a shell with the squadron's appearance on the minimap as the firing moment and the launching ship's position then as the firing position: inside a smoke credits that smoke, outside and undetected credits the smokes needed; concealed or detected by the ship's visibility flags at that moment.
- Overlaps are still recorded (`overlap_flag`, `overlapping_smoke_ids`: a puff of one smoke within the two radii of a standing puff of the other) and noted on smoke pages; totals no longer double count.
- Per smoke: `damage_in_smoke` (shots from inside) and `damage_behind_smoke` (the shooter's share for shots from outside), each split smoker / ally / enemy; `smoke_damage_total` = inside + behind for the smoker's team; `damage_shell`, `damage_fire` and `damage_airstrike`; `salvos` (distinct firing moments of the team's credited shells); `shooters`; `arrows` (one shooter-to-target line per attacker and victim with credited damage and mean positions, for the thumbnails and the zoomed view). Enemy damage inside our smoke is kept in the `_enemy` columns and never counted in totals.
- `shooter_detail`: each credited shooter of the smoker's team with player, ship, salvos, damage, its `split` and kills; `damage_detail.shooter_stats` adds each shooter's credit `by_kind` (shell, fire, airstrike). `targets_hit`: each enemy ship hit by credited shots with player, ship, ship_class, damage, `split` and `sunk`.
- Concealed and detected damage (round 6, `damage_split` on the record and `split` on every shooter and target): credit whose shooter was undetected at the firing moment is concealed; the rest is detected, with `detected_by` listing the damage per reason (the shooter's visibility flags at that moment, one reason per shot in the priority radar, hydro, smoke fire penalty, aircraft, submarine, proximity (inferred: the ship flag with an enemy within 2 km of the shooter), surface lit); `unknown` is credit whose shooter had no flag sample (zero on every smoke in this set). `dd_damage`: smoke damage, concealed and detected, on enemy destroyers by roster class. Awards that rank on damage use concealed damage with total damage as the tie-break.
- Kills (`kills_from_smoke`, round 4): an enemy ship counts as a kill for a smoke when the last damage it took before its recorded death (events up to 2 s after the death clock still count; events more than 10 s before it are ignored, so a missing killing blow credits nothing) was a shell or fire tick credited to that smoke and fired by the smoker's team. Several events on the same final tick all count, and a shared behind-smoke final shot credits every smoke in the share. The shot's attacker also gets the kill in `shooter_detail`. Round 4 batch: 23 kills over 217 smokes.

### 6.4 Selfish smoke

`selfish_smoke` is true only if, over the smoke's whole life, no teammate other than the owner was ever inside it and no teammate was credited damage from behind it. Null when the game has no damage events.

### 6.5 Radar, hydro and firing from smoke

- `radar_detections_in_smoke`: one row each time a ship of the smoking team inside the smoke gains the BY_RLS flag, including a ship already spotted by another ship (the game switches the reason). The row records the ship, the time, the likely radar ship (the nearest enemy with radar running, its distance and whether the ship was within that radar's range) and how long the ship stayed detected. Enemy ships inside our smoke never count. A ship inside two overlapping smokes is counted once, for the first-laid smoke. `hydro_detections_in_smoke` is the same for BY_SONAR; `fired_while_concealed_detections` counts a concealed ship becoming detected by firing (IN_SMOKE) and requires it to have been undetected before.
- `radar_spotted_damage`: damage taken by the smoking team's radar-spotted ships while each spot lasted.
- `offensive_radar`: a radar consumable activated by a ship of the smoking team that was inside the smoke and undetected at activation; enemies that gained the radar flag within that radar's range during the activation count as spotted by it (`enemies_spotted`, distinct ships, plus `activations` and `ship`). The replay does not name the spotting radar, so `inferred` is always true and the site says "inferred from the activation and radar range".
- Consumable ranges, stock gun range and base detection come from the ship's build resolved from game params (`tier2::ConsumableRanges`: radar_m, hydro_m, gun_m from the artillery component's maxDist without fire control or modifiers, detection_m from the hull's visibilityFactor). They are on each player in game.json.

### 6.6 Cap metrics

Sampled every 2 s of the smoke's life (standing puffs, cap owners and invaders, ships inside the smoke).

- `cap_proximity_m`, `cap_proximity_name`, `cap_radius_m`: at t_capture, the edge-to-edge distance from the smoke to the nearest cap, only for smokes outside a cap; a smoke inside a cap has none.
- `contested_cap_name`, `cap_contested_reason`, `avg_contested_cap_dist_m`: the contested cap nearest the smoke most often, why it was contested, and the edge-to-edge distance averaged over the samples (negative inside). Absent when no cap was contested while the smoke stood.
- `contested_cap_depth_pct`, `contested_cap_radius_m`: depth into that cap as a share of its radius, from the average distance of the smoke's edge to the cap centre: (radius - average distance) / radius, 0 at the edge, 100 at the centre, negative outside; the site caps it at 100.
- `supported_caps`: caps within stock main-gun range of a ship of the smoking team while it stood inside the smoke (distance to the cap centre minus the cap radius, against gun_m).
- `cap_won`, `cap_won_at`: a supported cap that flipped from neutral or the enemy to the smoking team during the smoke or within 10 s after its last puff faded. Labelled on the site as "smoke near a cap capture", never "smoke won the cap". Caps already ours do not count.
- `cap_defended`: a contested cap the smoking team owned while the enemy was invading it and the smoke stood.
- `radar_cap`: the best coverage of a contested cap by a radar ship of the smoking team inside the smoke and undetected: `full` when the distance to the cap centre plus the cap radius is within radar range; `coverage_pct` is the share of the cap's area within radar range (circle intersection); `activated` when that ship ran its radar from inside the smoke; `ship`, `cap`.
- `cap_denial`: enemy ships in or within 1 km of the nearest contested cap's edge, averaged over samples in the 60 s before the smoke object appeared (`enemies_before`) and over its life (`enemies_during`).

### 6.7 Other context (Tier 1 and 2)

- Classification (round 5 and 6, `classification` on every smoke, `smokees`, `offensive_hydro`): the four structured fields (smoker class and special cases; movement with confidence, stationary under 500 m judged first; coverage with stacked over screen over selfish; purpose tags in the priority order cap_control, cap_contest, radar_trap, hydro_trap, counter_smoke, island_dive, reposition, damage, escape, each with a reason and the fuzzy ones with a confidence), the location fields (lane, cap role, front-line distance, nearest enemy, caps in range, land distance; the zone and grid come from the map profile at site build) and the smokees (the smoker, every ally inside, firing undetected from behind, or with the smoke in its line of fire, and every credited shooter; each with a badge, role, covered seconds, undetected share, detection kinds weighted by time, damage split, damage taken while covered and kills). Round 6 rules: cap_control needs the contested cap and a radar activation by a concealed ship inside the smoke while covering at least 90% of it; the damage purpose needs 20,000 damage, the sub-labels describe any damage; counter_smoke is the nearest enemy smoke within 12 km laid 0 to 45 s before, borderline within 100 m of the limit. Rules and thresholds: `smoke/ANALYSIS.md`; the reasoning: `smoke/DECISIONS-ROUND5.md` and `smoke/DECISIONS-ROUND6.md`. Ships cover map distance at about 2.6 times their listed speed, which sets the distance thresholds.
- Smoke deaths (`smoke_deaths`, round 4): a ship of the smoker's team that the smoke concealed (it appeared in the smoke's inside samples, or fired a shot with the smoke among its `behind_smokes`; the earlier of the two is `concealed`, `inside` or `behind`), was detected at a flag change between that moment and its death, and died between the smoke object's creation and 20 s after its removal. Each entry carries player, ship, the death moment and `after_cleared`. Round 4 batch: 16 over 217 smokes. This replaces the round 3 site stat "smoker alive 60 s after".
- State at t_activate and t_capture (`state_at_activate`, `state_at_capture`): score, cap owners and progress, ships alive by team and class, smoker HP and spotted flags, enemy radars alive, nearest enemy, nearest cap.
- `allies_in_smoke`, `enemies_in_smoke` at t_capture; ally and enemy ship-seconds inside over the life.
- `ships_at_capture`: living ships within 14 km of the origin at t_capture (9 km before round 4), with team, class, position and the owner mark, for the thumbnails.
- Score swing (site): the point gap (ours minus theirs) at capture minus the gap at activation.

### 6.8 Clan metrics (site)

uptime = seconds per game with at least one clan smoke standing (union of smoke lives); charge use = smoke activations over smoke charges carried by the clan's smoke ships; stacking rate = share of smokes overlapping another; contested-cap share = share of smokes within 1 km of a contested cap on average; selfish share; score swing = mean swing; radar-punished share = share of smokes with at least one radar spot on the team's ships inside; radar spots from smoke = enemies spotted by own radar from smoke, per game; kills from smoke per game; smoke deaths per game; smokes near a cap capture (count); radar cap coverage = mean coverage and the count with full coverage; concealed smoke damage per game and DD damage per game (round 6). Every chart and stat shows its count (n). The Clans charts sort the bars best first; lower is better for smoke deaths only. Selfish share and radar-punished share are the Tendencies group: style signals, not scores.

## 7. Awards (round 3, no limit on awards per player)

Smoke awards each get a 5x clip and live on Home. Winners are from batch `output/20261104-180332` under the destroyer lens (round 6 ranks the damage awards on concealed damage; no winner moved; the Deepest Cap Smoke keeps its zero-damage winner by Sean's decision).

| Award | Definition and eligibility | Winner |
| --- | --- | --- |
| Smoke of the Tournament | Highest concealed smoke damage, ties by smoke_damage_total | HSR_Yamiyonohik, Somers, -BN- vs H-SR (Groups G3 R3) on Okinawa at 13:36, id 46513, 90,686 concealed of 91,412 (round 6's line-of-sight fix, which sees enemies that never dealt damage, raised it from 80,520; the runner-up is RESIN_Big_Boy69's 90084 on Hotspot at 80,375, all concealed) |
| Deepest Cap Smoke | Highest contested_cap_depth_pct among smokes with cap_won or cap_defended; ties by smoke_damage_total. Card shows the depth share, cap name and cap radius | RESIN_Fryce, Somers, RESIN vs BONKZ (LB R6 G3) on Sea of Fortune at 05:35, id 106317, 100% into cap C with cap D defended, 0 damage |
| Radar Bait | Most radar spots on the smoking team's ships inside while it stood; ties by radar_spotted_damage | PN_Sean_O_Reill, Harugumo, PN vs HTDOG (Groups G1 R4) on Land of Fire at 14:39, id 174224, 2 spots, 31,904 taken while spotted |
| Peekaboo | Most enemies spotted by the smoking team's own radar run from inside the smoke (offensive_radar.enemies_spotted); ties by damage | RESIN_Fryce, Harugumo, RESIN vs INCA (Groups G4 R5) on Mountain Range at 08:45, id 27145, 4 enemies by RESIN_thepregna's radar |
| Most Selfish Smoke | The selfish smoke with the most concealed damage by its owner, ties by the owner's total | RESIN_Maddog242, Harugumo, BONKZ vs RESIN (WB R3 G1) on Sleeping Giant at 13:00, id 120803 |
| Golden Cloud | Most total concealed smoke damage | HSR_Yamiyonohik, 926,127 concealed over 50 smokes (974,676 in all) |
| The Smokefather | Most smokes laid | HSR_Yamiyonohik, 50 smokes in 18 games |
| Best in Haze | Highest average concealed damage per smoke, minimum 5 smokes | HSR_Yamiyonohik, 18,523 per smoke |
| Most Selfish Smoker | Most selfish smokes (a style signal) | RESIN_eagle_lan, 14 of 27 destroyer smokes |
| Clan: most smokes laid (per game) | | H-SR, 4.0 over 22 games |
| Clan: most concealed smoke damage (per game) | | H-SR, 65,707 over 22 games |
| Clan: most selfish smokes (per game) | | RESIN, 1.3 over 24 games |

History: round 1 and 2 Deepest Cap Smoke went to PN_Sean_O_Reill's Harugumo on Mountain Range (raw depth, then contested average distance); round 3's depth-share rule with the cap won or defended eligibility moved it. Round 1 and 2 Smoke of the Tournament was RESIN_Fryce's Harugumo on Mountain Range (88,586) before one-smoke credit and the weapon scope. Best in Haze moved from PN_Sean_O_Reill (4 smokes) when the minimum rose to 5.

## 8. The site

**Format and hosting.** Static HTML, CSS and JavaScript, no server; works from a local folder; published to GitHub Pages from `gh-pages` (section 3). Under 500 MB in total, no file over 100 MB, images as WebP, thumbnail overlays as inline SVG.

**Look.** Dark naval look: deep navy background, smoke-grey panels, white text. Team colours everywhere: H-SR gold #F5C542, RESIN sky blue #5DADE2, PN violet #B388FF; enemies red #F87171 in diagrams. A pinch of whimsy only (award names, "Nothing here, just clear skies." on an empty filter). Terms (selfish smoke, contested cap, every clan metric, every award) carry their definition as a tooltip wherever they appear.

**Lenses (round 5).** Every comparison carries a smoker-class and smoke-type filter. The Clans charts, clan page tiles and the awards default to destroyer smokes (awards offer destroyer or all; the other pages offer every class and type). Player badges are gold for the destroyer lens and grey for all smokes.

**Navigation.** Home, Clans, Players, Smokes, Maps, Games. `awards.html` and `analysis.html` are one-line pages pointing to where their content moved (Home, Players and Clans; Clans).

**Pages.**

1. Home: "Smoke Signals" briefing ("This site breaks down how top competitive teams use smoke: 217 smokes from 45 games (43 with at least one smoke) ..."), stat tiles per clan, the key terms (smoke damage, concealed smoke damage, DD damage, selfish smoke, radar bait; one bold term and one line each; radar bait is "possibly a mistake" and selfish smoke a tendency), and the five award smokes with the map-crop thumbnail, details (total damage with the concealed and detected parts) and clip. No headline findings.
2. Clans: the clan cards (scouting-report text to come from Sean), then the lens selects and the clan comparison charts drawn in the browser from precomputed values for every lens, one bar chart per metric with n, bars sorted best first (lower is better for the risks), grouped as Volume (smokes per game, uptime, charge use, stacking rate), Damage (damage per game, concealed damage per game, DD damage per game, average damage per smoke, kills from smoke per game), Objectives (contested-cap share, smokes near a cap capture, score swing), Radar plays (radar spots from smoke per game, radar cap coverage), Tendencies (selfish smoke share, radar-punished share; style signals, not ranked lower-is-better) and Risks (smoke deaths per game). Built to take ten or more clans.
3. Clan pages: lens selects (destroyer default) driving the tiles, led by uptime, score swing and radar-punished share, the other metrics as tiles (concealed and DD damage per game, kills from smoke, smoke deaths and radar spots from smoke per game); a purposes table (hydro_trap hidden) and movement and coverage charts over every smoke by the clan; "Where their games ended" (opening, mid, endgame columns, wins and losses stacked, counts on the bars); the timing bar (smokes per game standing in each phase); the most-smoked-spots heatmap (10 x 10 grid cells per map); the ship lineup (donut plus a table with class, smoke type, stock gun range, radar range, detection); the Top smokers strip (top 3 by share of the clan's smoke damage, linking to Players); the clan awards.
4. Players: the player awards as cards for the destroyer and all-smokes lenses (toggle), then a sortable leaderboard (click a heading) with award badges and Smoke damage, Concealed, DD damage and Kills columns; one page per player with stats (including concealed and DD damage, kills from smoke and smoke deaths), the ships donut, a damage-per-smoke chart drawn in the browser (top 12 of the lens; each bar labelled "map, vs opponent, game n, ship", coloured by ship to match the donut, clickable to the smoke page), lens selects, and every smoke as a card with its class, movement, coverage and primary purpose.
5. Smokes: "All 217 smokes from the tournament. Click a row to open it." A table with filters (clan, player, ship, map, game, type, smoker class, movement, coverage, purpose (any tag), primary purpose, zone, lane, phase) and sorts (smoke damage, concealed damage, DD damage, kills, smoke deaths, radar on us, our radar detections, score change, depth, distance to contested cap, time elapsed); columns: thumbnail, clan, player, ship, map, game (short "vs HTDOG, game 2" with the full label as a tooltip), clock (elapsed only), tags (class pill, movement, coverage, primary purpose and the count of other tags, full tags as a tooltip), zone and lane, damage (the total with its bar and "concealed / detected" under it), DD damage, distance to contested cap (depth share when inside), cap outcome, radar on us, our radar detections, kills, smoke deaths, selfish (yes or no). The whole row is the link; no flag or overlap tags (those stay on the smoke page).
6. Maps: "Crawling and exhaust smokes are dashed. Click a line to open the smoke." One section per map with the minimap drawn as an image element inside the overlay SVG (round 6: the overlay and the map share one coordinate system, so the column's height can no longer shift the lines off the islands), the grid as the game labels it (numbers 1 to 10 across the top, letters A to J down the side), every cap as a lettered circle, and one line per smoke (puffs in laying order, arrow at the end, dashed for exhaust and crawling, click to open), coloured by clan. Filters per map: a two-handle time-elapsed slider (0:00 left, 20:00 right; a smoke is shown when its activation falls between the handles), clan, spawn (north or south; east and west with a note where a map spawns that way) and ship, also presettable by query string (`?clan=&spawn=&ship=&from=&to=`). The filters hide and show the lines on the map (round 4 fix: the script now toggles a class; SVG links ignore the `hidden` property) and drive the four small charts for the smokes shown (smokes, average damage, average distance to the nearest contested cap, selfish share; each bar with n; clans with fewer than 5 smokes shown are greyed out) and a ships pie of the ships that smoked there; smoker-class and smoke-type filters per map; a "show zones" checkbox (also `?zones=1`) drawing the profile zones and notable spots over every map. No bullet stats under the maps.
7. Games: "Prototype: only series with H-SR or RESIN replays are linked so far." The full double-elimination bracket (winners rounds 1 to 4, losers rounds 1 to 6, grand final): one clickable box per series in the replay set with games won, greyed TBD boxes for the rest. Series pages list the games (score, map, winner) with links. Below, the group stage games filterable by clan and map.
8. Game pages: header (stage, map, date, score, winner, how and when it ended with the phase), the mini map with grid, caps and paths, a timeline and a score chart in real minutes for that game, rosters with smoke charges used over carried and spawn sides, the folded per-ship damage check, and the game's smokes as cards.
9. Smoke pages: header with countdown clock, elapsed time and phase and the damage (plus kills, with the concealed and detected parts) line; an owner-flag or overlap note when it applies; the full capture frame at page width (the map when the smoke was fully laid, ship names but no player names, no inset); the zoomed view (a bare second render without names, HP bars, range circles, planes or buildings, covering the smoke, every smokee, every damaged enemy and the fire lines, at least half the map, with the credited fire lines, damage labels and the smokee badge numbers drawn on it); the clip for award smokes ("Clip available on request" otherwise); then the Classification block (auto-tagged: plain values such as "Horizontal" with a confidence dot (green, yellow, red; grey for rule-based) and the reason and numbers in the tooltip: smoker, movement, coverage, every purpose with the primary first, location (zone, lane, cap role), front line in words, caps in range, counter-smoke link), then three groups: Deployment (duration, allies inside at capture, selfish, hand tags "untagged"), Violence (smoke damage, the concealed/detected bar, what spotted the detected shooters, the inside/outside split bar, shells and fires, DD damage, kills from smoke, a pointer to the Smokees table for the shooters, the Enemy ships damaged table with ship (DD marked), player, concealed, detected, total and sunk, then a red-ruled "bad news" block with radar spots on us and smoke deaths) and Objectives (distance to contested cap with the capture proximity in its tooltip, cap outcome, denial signal, score at capture with the swing, our radar from the smoke, radar cap coverage); the Smokees table (badge, ship, player, role, undetected share of the covered time, what detected it and for how long, damage dealt concealed / detected, damage taken while covered, kills; the smoker, every covered ally and every credited shooter); navigation. The activation frame, the separate zoom pair, the diagram, the summary sentence, supported caps and ships alive are gone from the page (still in the data).
10. Thumbnails everywhere (Home awards, player and game cards, the Smokes table) are a crop of the real minimap, half the map side, centred on the smoke: the map image as a shifted background with an inline SVG overlay of the caps, the puffs in laying order with an arrow, every ship of both teams within 14 km as team-coloured icons (red = enemy, gold ring = smoker), the credited fire lines labelled with damage, and a 1 km bar; no names or HP. Table thumbnails are 84 px, award thumbnails 300 px.
11. Mobile, light touch: the nav collapses behind a Menu button under 800 px, charts fit the width, wide tables scroll sideways.

## 9. Outputs per smoke

- Frames: activation and capture, the renderer's merged minimap view with ship names (player names off since round 6), HP bars, detected outlines, caps, score, timer and rosters; the target smoke outlined in yellow (union of its puffs), a ring on the smoker before the smoke exists, a magenta dashed trail for exhaust and crawling smoke, exhaust puffs in light orange; a header strip (ordinal, team, player, ship, type, charge, activation to capture clocks, base stats, score, caps, alive, HP, spotted, enemy radars) and a footer (tournament, round, map, build). Saved as PNG and WebP, named `<match>_<game>_<team>_<player>_<ship>_s<nn>_{act|cap}_<mmss>`.
- Zoomed views (round 6): a second render of the same moment with names, HP bars, range circles, planes and buildings off, cropped to the square that holds the smoke, every smokee and every damaged enemy alive at that clock and both ends of every drawn fire line, padded by 1 km, never smaller than `1/zoom_factor` of the map side (half at the configured 2) nor larger than the map, and magnified to the map's own size (768 px) with a 1 km bar, the magnification, the credited fire lines with damage labels and a numbered badge on each smokee matching the Smokees table; saved on their own as `<stem>_zoom`. The minimap size is a constant of the upstream renderer, so the crop is an upscale and a little soft.
- Clips: from activation minus 5 s to dispersal, 20 fps, `render.clip_speed` times real time (award clips at 5x, 1200 kbps, about 35 s and 3.5 MB each), H.264 MP4 from the CPU encoder, with the same overlays and header plus a progress marker; no inset. Every smoke gets a clip when `--clips` names it; the site publishes the five award clips only.
- Round 5 fields on the record: `classification` (smoker_class, special, movement, coverage, purposes, primary_purpose, damage_20k, damage_qualified, damage_label, lane, lane_offset_m, cap_role, cap_role_cap, cap_flank, frontline_distance_m, nearest_enemy_m, caps_in_range, counter_smoke_of, land_distance_m), `smokees`, `offensive_hydro`; the game record carries `land_share`. The CSV adds one column per scalar plus purposes as `tag:confidence;...`, smokees and smokees_detected counts; the site's `data/smokes.csv` and the export add `zone` and `grid` from the profiles.
- Round 6 fields: `damage_split` (concealed, detected, unknown, detected_by as reason and damage), `dd_damage`, `split` on every `shooter_detail` and `targets_hit` row (plus `ship_class` on targets), and on every smokee `badge`, `role`, `undetected_pct`, `detected_by` (kind, inferred, seconds), `split`, `damage_taken`; `movement.label` can be `stationary`. CSV columns: smoke_damage_concealed, smoke_damage_detected, smoke_damage_unknown, detected_damage_by (`reason:damage;...`), dd_damage. `damage_events.csv` gains `detected_reason`. The `smokees` and `smokees_detected` columns now count the smoker and every credited shooter, so they are larger than round 5's.
- Metadata record (smokes.json, smokes.csv): identity (smoke_id, activation_id, match_id, round, game_no, map, map_display, game_build, replays, team, opponent, spawn_side, player, ship, ship_class, ship_tier); smoke (smoke_type, variant, charge_no, charges_total, base_emission_s, base_puff_life_s, base_radius, radius, observed_emission_s, emission_cut_short, owner_flag, owner_note, owner_distance_m, overlap_flag, overlapping_smoke_ids, origin_xy, bbox, puff_count, path); times (t_created, t_activate, t_capture, t_emission_end, t_dispersed, each as replay seconds and clock); state_at_activate and state_at_capture; Tier 2 (allies_in_smoke, enemies_in_smoke, ally and enemy ship-seconds, radar, hydro and fired-while-concealed detections); damage (damage_in_smoke, damage_behind_smoke, smoke_damage_total, the _enemy columns, damage_detail with the smoker/ally/enemy split, damage_shell, damage_fire, salvos, shooters, arrows, shooter_stats, targets, kills; shooter_detail, targets_hit, kills_from_smoke, smoke_deaths); caps (cap_proximity_m, cap_proximity_name, cap_radius_m, contested_cap_name, cap_contested_reason, avg_contested_cap_dist_m, contested_cap_depth_pct, contested_cap_radius_m, supported_caps, cap_won, cap_won_at, cap_defended, radar_cap, cap_denial); radar (radar_spotted_damage, offensive_radar); selfish_smoke; shooters; ships_at_capture; provenance (wows_toolkit_rev, smoke_signals_version, generated_at); files (frame_act, frame_cap, frame_act_zoom, frame_cap_zoom, clip).
- Game record (game.json): tournament, match_id, round, game_no, map names, build, replays, teams (name, team_id, spawn_side, spawn_xy, final_score, players with entity_id, player, clan, ship, class, tier, smoke variant and type, smoke_activations, smoke_charges, death, gun_range_m, radar_m, detection_m), caps (letter, position, radius, radius_m, kind), outcome, finish_type, battle_start_s, battle_end, replay_end_s, replay_truncated.
- damage_spike.json: events and damage by source and by kind, per-attacker totals (all and shell-plus-fire), the game's per-attacker totals, the per-ship reconciliation table and ratios, duplicate counts, hit, salvo and torpedo counts. damage_events.csv: every event with its kind, firing moment and source, detection at fire, in_smokes, behind_smokes and credited shares.

## 10. Known limits

- Damage kinds are inferred from timing. Fire ticks are linked to the shooter's latest shell on the same target within 75 s, so a long burn is credited to one salvo; "unknown" damage (about 9% of all damage) includes secondaries and shells whose salvo was not seen.
- Reconciliation per game ranges from 0.71 to 1.16 of the game's totals. Games below 1 are missing hits neither perspective saw or where equal-amount events were folded that were real; games above 1 still carry some duplicates whose clocks drifted more than the window. The per-ship table on each game page shows where. A game whose shell-plus-fire ledger exceeds the game's result by more than 25% (`LEDGER_RATIO_MAX` in build_site.py) is flagged in games.csv, noted on its page and left out of awards and leaderboards (three games in the full field).
- Airstrikes (known limit, STEP 2g, `smoke/STEP2G-P5P8-VALIDATION.md`): the ledger classifies 44% of the game's air-support bomb damage as airstrike (3.62M of 8.15M): Utrecht 66%, Tromp 66%, Prins van Oranje 45%, Willem de Eerste 23%, Gouden Leeuw 14%. The rest sits in shells (the salvo fallback) and unknown, because a tick at or under one main-battery shell's listed damage is kept as a shell, and the Dutch battleships' shells list at 5,750 to 13,700, above most bomb ticks. The squadron is sampled on the minimap about once a second at some 370 m/s, so its track is interpolated and the pass tolerance is 1,000 m. The launching ship is inferred from the squadron param's ship name, not read from the packet, which carries none; 470 of 2,556 squadrons in the field got no single owner. Smoke-credited airstrike damage is 204k over the field (5.6% of the airstrike ledger), as most strikes are called from outside smoke while spotted.
- Torpedoes (known limit, STEP 2g): the ledger classifies 28.4M of the game's 37.0M torpedo damage (77%; the replays carry about 32M at all). Of the gap, 4.4M is hits under the 0.5 floor on 289 player-runs and 1.7M (6.1%) is ticks on a resolved shell hit under a whole salvo's size. False positives are 11 player-runs and 35k. Torpedo protection is the equipped hull's stock value; build modifiers to it are not applied to the floor.
- Replay coverage: a client is told about hits in its area of interest, so hits far from both recorders are in neither ledger. Over the full field the ledger holds about 89% of the torpedo damage the game's results report (the shell ledger has the same kind of gap, smaller). Torpedo and shell totals on the site are what the two replays saw, not the game's own totals.
- Offensive radar spots are inferred from our activation and range, not read from the replay, so a spot by another radar in range at the same time is counted too.
- The line-of-sight test uses the hull's base detection range, not the build's concealment; enemies within the base range but outside the real detection range can mark a smoke as needed.
- The Deepest Cap Smoke can be a zero-damage smoke, since defending a contested cap is enough for eligibility (current winner).
- Smoke objects come from the primary replay only; a smoke the primary recorder never saw is not in the table.
- A team without a replay has every smoke flagged for owner attribution; 22 of 217 smokes carry an owner flag.
- Crawling smoke has no test coverage (none in the replay set).
- The bracket shows only the series in the replay set; the other series are TBD placeholders.
- The game and clips folders are large (`smoke-site/` about 240 MB, mostly frames); image compression is deferred.
- Headless Chrome cannot screenshot below about 500 px wide; mobile is checked in the app's browser pane.
- The zoomed view is a 2x upscale of the 768 px minimap, so it is softer than a native render; drawing the minimap larger needs a change to the upstream renderer, whose size is a crate constant.
- hydro_trap never fires in this set (33 hydro runs from smoke, no new sonar spot within range); it stays in the data and off the site. counter_smoke fires on 11 smokes at 45 s and 12 km, two of them at 12.0 km rounded (borderline). Movement is unknown for 23 smokes whose smoker or enemies had no position at laying start. Land is the drawn coastline from the map's land layer, not the collision mesh. The smoker counts as inside its own smoke while laying by rule, because the replay shows each puff some seconds after the ship passed.
- Kills use the last damage event in the merged ledger within 10 s of the death; a sinking whose final hit neither replay saw, or whose final blow was a torpedo, flood or unknown damage, credits no smoke.
- A smoke death needs a visible detection flag change after concealment; a ship sunk while still undetected (blind fire, torpedoes) is not counted.

## 11. Open questions

- [ ] Deepest Cap Smoke: keep the zero-damage winner (eligible by defence) or also require damage? Asked 3 Nov 2026, not yet answered.
- [ ] PN scope: group stage only now; add PN clan battle replays after the demo?
- [ ] Purpose list and rating scale for hand tagging (section 12): confirm before tagging starts.
- [ ] Phase 3 host: decide after the demo; clip storage drives the cost.
- [ ] Crawling smoke capture rule: untested until a replay contains one.
- [ ] Whether to reduce "unknown" damage by matching secondaries (ATBA) salvos.
- [ ] Whether to ask upstream for a larger minimap render so the zoomed view is sharp.
- [ ] The map profiles' zones and notable spots (DRAFT); the 25-smoke review list (round 5).
- [ ] The two borderline counter smokes at 12.0 km (H-SR 90086 on Hotspot, 108992 on Land of Fire, Grand Final): keep or drop.
- [ ] Clan scouting-report text for the Clans cards: to come from Sean.

Decided and closed: round 6 (4 Nov): concealed damage at the firing moment with one reason per shot; awards on concealed damage; stationary under 500 m; cap_control on the contested cap with radar activated at 90% coverage; damage purpose at 20k only; counter_smoke 45 s and 12 km; the smoker inside its own smoke while laying; behind-smoke cover needs an undetected shooter; the Maps image inside the SVG; grid letters down the side; radar bait "possibly a mistake" and selfish smoke a tendency (Tendencies group). Earlier: behind-smoke damage needs the line of fire through a puff (2 Nov); overlapping smokes credit one smoke per shot (3 Nov, replacing "credit both and flag"); enemies in our smoke count in separate columns only; clip window activation minus 5 s to dispersal; team colours; five award clips; map names from the game catalog; Mountain Range cap A is real; spawn labels north and south; cap proximity excludes inside-cap smokes; time axes as elapsed with the countdown in per-smoke text; awards.html stays as a pointer page; round 4 (3 Nov): kills by killing blow with shared final shots crediting both smokes, smoke deaths with a 20 s grace replacing smoker survival, per-game radar spots and kills in the Clans charts, Deployment/Violence/Objectives groups on smoke pages, 14 km ship reach, reconciliation share off the site, Analysis folded into Clans.

## 12. Hand-tagging (deferred, Phase 2 plan)

Sean tags smokes in a spreadsheet and one command imports the tags; reruns never overwrite them. Each run would write `tags.csv` (smoke_id, team, player, ship, map, clock, frame files, empty tag columns); `smoke_signals import-tags tags.csv` would load it into a `smoke_tags` table keyed by smoke_id. Columns: purposes (cap_contest, disengage, cover_ally, cruiser_firing, torpedo_setup, spotting_denial, push_support, bait, other, several separated by `;`), initiative (proactive or reactive), rating (1 wasted to 5 decisive), notes, tagged_by, tagged_at. Not built yet; smoke pages show "untagged".

## 13. History and validation

- 2 Nov 2026 prototype: a test tool found all 6 H-SR smokes in Grand Final G1 and rendered each in about 1 s; those smokes are the golden test (YuriSayuki Harugumo at 18:04, 14:39, 11:14 captured 17:11, 13:46, 10:21; Yamiyonohik Somers at 13:37 and 08:37 captured 12:54 and 07:53; Apex_captai Conte Verde exhaust at 08:17 captured 07:27). Lessons: time emission by new puffs, exhaust needs its own rule, owner needs proximity and activation, emission differences come from builds, merged positions need the position timeline with a minimap fallback.
- 3 Nov 2026: M1 to M4 done overnight; M3.1 visual fixes (union outline, zoomed inset, magenta trail, clip speed); Phase 2 rounds 1 to 4 as in section 2. The ledger duplicate problem was found by the round 3 reconciliation check and fixed the same day. Round 4 added the kill, target and smoke-death fields (tests, golden and determinism still pass) and found that the Maps filters never hid the SVG lines because SVG elements ignore the HTML `hidden` property.
- 4 Nov 2026 (round 5, overnight): classification, location context, smokees, lenses, map profiles, docs and the r5 export; 22 unit tests, golden and determinism pass; award winners unchanged in both lenses except the clan and selfish-smoker counts, which are smaller under the destroyer lens.
- 4 Nov 2026 (round 6): the damage split, DD damage, stationary, the retuned classifier, the merged Smokees table, the bare zoomed view, the Maps fix (a CSS grid stretch recentred the overlay; the grid labels were transposed) with the overlay test, Tendencies and wording; 24 unit tests, golden, determinism and the overlay test pass. No award winner moved: under concealed damage HSR_Yamiyonohik's 46513 still leads (90,686 after the line-of-sight fix) ahead of RESIN_Big_Boy69's 90084 (80,375). A clip of 90084 was rendered while it led and stays on its page.
- Upstream feature requests for the wows-toolkit author: dump a frame at an exact battle clock; a smoke-event export (smoke id, owner, puff timestamps, variant); move the game-data loader into the library (done in the fork as the only upstream change).
