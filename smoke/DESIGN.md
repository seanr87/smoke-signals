# Smoke Signals: Design Doc and Source of Truth

Owner: Sean. Last full revision: 3 Nov 2026, after Phase 2 round 3. This document is the only source of truth for the project; a fresh session should need nothing else. Rules in `smoke/CLAUDE.md` and the fork's `AGENTS.md` still apply.

Live site: https://seanr87.github.io/smoke-signals/

## 1. Goal and scope

For every smoke laid by H-SR, RESIN and PN in King of the Sea XIX NA, the tool produces two minimap frames, zoomed screenshots, a diagram, a metadata record and (for award smokes) a clip, then builds a static site that compares how the three clans use smoke. The goal is to learn how competitive teams use smoke effectively.

- Teams: H-SR (NA regional winner), RESIN (runner-up), PN (our clan, the comparison). PN played the group stage only.
- Games: 45 played games in the replay set (group stage and playoffs for H-SR and RESIN, group stage for PN); 43 of them have at least one analysed smoke. 217 smokes: H-SR 100, RESIN 103, PN 14.
- Framing: a few hundred smokes supports descriptive patterns and strong examples, not causal claims. Purpose and intent tags are hand work that has not started, so every page is descriptive.

## 2. Status

| Phase | Scope | State |
| --- | --- | --- |
| 1. Prototype (M1 to M4) | Grand Final G1, H-SR only: pipeline, smoke detection, frames, clips, Tier 1 and 2 metrics, damage spike, golden test | Done 3 Nov 2026 |
| 2. Demo site, round 1 | Replay inventory, batch over every game, awards, first static site, GitHub Pages | Done and published 3 Nov 2026 |
| 2. Demo site, round 2 | Contested caps, in-game map names, cruiser smoke type, Maps paths and filters, Games page | Done and published 3 Nov 2026 |
| 2. Demo site, round 3 | One-smoke-per-shot credit, shell and fire scope with reconciliation, ally-only and offensive radar, cap support and outcome metrics, Home/Analysis/Clans/Players/Smokes/Maps/Games lineup, full bracket, diagram thumbnails, inset dropped, mobile | Done and published 3 Nov 2026 (commit 83d5e48a on `smoke-signals`) |
| 3. Interactive | Tagging, comments, hosting, login | Decided after the demo is presented |

Deferred past the demo: build data (commander skills and upgrades) and effective smoke stats; hand tagging (pages show "untagged"); clips for every smoke; a second golden test game; image compression; the desktop app integration.

## 3. Repository, build, test, run, publish

The work lives in a fork of [landaire/wows-toolkit](https://github.com/landaire/wows-toolkit) (MIT), GitHub `seanr87/smoke-signals`, branch `smoke-signals`, checked out at `C:\Users\soreill5\KOTS Analysis\wows-toolkit`. The fork's conventions apply: no AI attribution in commits, ASCII only, short commit messages. `jj` is preferred by the fork's AGENTS.md but is not installed, so `git` is used.

```
crates/smoke-signals/            the smoke_signals program (Rust, edition 2024)
  src/analysis.rs                smoke tracking, owner, type, cap sampling, cap metrics, radar, spike call
  src/damage.rs                  damage ledger merge, weapon classification, smoke credit
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

The second command exports the minimap images and `maps.json` (with in-game titles) that the site needs; the third renders the award clips (the ids are the current winners). Batch options: `--matches`, `--teams`, `--maps`, `--no-frames`, `--clips <ids>`, `--clip-speed`, `--clip-bitrate-kbps`. Never delete an output folder; every run gets its own timestamp. Current data: batch `output/20261103-185243`, maps `output/20261103-143026/maps`, clips `output/20261103-185636`.

**Build the site.** Clips are passed as a folder of `<smoke_id>.mp4`.

```bash
python -I -X utf8 smoke/tools/build_site.py --batch output/<batch> --maps output/<maps>/maps --clips <folder of id.mp4> --out smoke-site
```

The builder prints the award winners. `smoke-site/` is gitignored and about 240 MB; the fork's own tracked `site/` folder must not be touched. Old files in `smoke-site/` are not deleted by a rebuild (stale clips must be removed by hand).

**Verify.** Serve `smoke-site/` locally (`python -m http.server 8765 --directory smoke-site`; the desktop app's launch entry `smoke-site` does the same) and take headless screenshots of every page type:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=8000 --window-size=1280,2400 --screenshot=out.png http://localhost:8765/maps.html
```

Headless Chrome will not shrink below about 500 px, so the phone layout is checked in the desktop app's browser pane at 375 px instead. A link check walks every href and src in the built pages (301 pages, about 6,800 links, none missing in round 3) and greps the visible text for internal map names.

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
- A client is told about every hit in its area of interest, so the two perspectives report the same hit twice with a clock offset that is near constant within a game but differs between games (1 to 5 s seen).
- The results blob at the end of a replay carries every player's totals (`playersPublicInfo`, decoded with `CLIENT_PUBLIC_RESULTS_INDICES` from constants.json: damage, damage_main_ap, damage_main_he, damage_main_cs, damage_fire, and others).

## 5. Smoke definitions

A smoke is one smoke object in the replay. `view.smoke_screens()` gives its radius, origin and puff list; the list grows as puffs are laid and shrinks as they fade, with no owner and no timestamps, so the tool records the times itself.

**Lifecycle.** `t_activate` (the consumable is used), emission until `t_emission_end`, standing, `t_dispersed` (the object is removed). `t_created` is when the object appeared.

**Owner.** Candidates are the ships fitted with a smoke consumable. The owner is the nearest candidate that activated smoke in the 5 s before the object was created; a candidate with an activation beats a nearer one without only within 1000 m of the origin. Otherwise the nearest candidate is the owner and `owner_flag` is set with a note (no activation in the window; position from minimap samples only; nearest candidate more than 600 m away). Smoke objects are tracked from the primary replay only.

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

- Each replay's `receiveDamagesOnShip` events give attacker, victim, amount and clock, but not the weapon. Both replays are parsed and merged. The merge estimates each later replay's clock offset against the earlier ones as the most common clock difference (quarter-second bins, at least 10 pairs) over same-attacker, same-victim, same-amount pairs, leaving out fire and flood ticks, then folds an event onto an unmatched earlier event within 0.8 s of that offset. Without the offset, games with a 4 to 5 s skew doubled every ship's total.
- Reconciliation: for every ship, the ledger total and the ledger's shell-plus-fire total are compared with the game's own results (damage; damage_main_ap + damage_main_he + damage_main_cs + damage_fire). Each game page shows the per-ship table; the Analysis page shows the share across games. Round 3 batch: ledger over game total averages 0.98 per game (range 0.71 to 1.16); shell-plus-fire averages 1.05 (0.81 to 1.36).

### 6.2 Weapon classification (`kind` on every damage event)

- shell: matched to a resolved shot hit (same attacker and victim, impact within 1 s) or to the attacker's latest salvo within 25 s before the damage.
- fire: the event sits in a tick train (a same-amount neighbour 0.7 to 1.4 s away on the same victim) and the attacker's latest shell on that victim was within 75 s before it; the tick is credited like that shell.
- torpedo: no hit, not a tick, and a torpedo the attacker launched 1 to 150 s earlier has run (speed times run time) within 15% of the distance from its launch point to the victim.
- flood: a tick train whose latest linked event is a torpedo.
- unknown: nothing recorded explains it (secondaries, shells with no salvo seen, and so on).
- Only shells and fires earn smoke credit. Torpedo, flood and unknown damage are reported in `damage_spike.json` (events and damage by kind) and never credited.

### 6.3 Smoke credit (one smoke per shot)

- A shot fired from inside a smoke credits that smoke alone. Inside two overlapping smokes, the first-laid one whose puffs still hide the shooter gets the credit; when its puff fades, credit passes to the next.
- A shot fired from outside any smoke by an undetected shooter credits the smokes that were needed, in equal shares: those whose standing puffs lay on the line from the shooter to at least one living enemy within the shooter's base detection range (hull `visibilityFactor`; 12 km when unknown), nearer the shooter than that enemy. If no smoke was needed, nothing is credited.
- A fire tick is credited exactly like the shell that started it.
- Overlaps are still recorded (`overlap_flag`, `overlapping_smoke_ids`: a puff of one smoke within the two radii of a standing puff of the other) and noted on smoke pages; totals no longer double count.
- Per smoke: `damage_in_smoke` (shots from inside) and `damage_behind_smoke` (the shooter's share for shots from outside), each split smoker / ally / enemy; `smoke_damage_total` = inside + behind for the smoker's team; `damage_shell` and `damage_fire`; `salvos` (distinct firing moments of the team's credited shells); `shooters`; `arrows` (one shooter-to-target line per attacker and victim with credited damage and mean positions, for the diagram). Enemy damage inside our smoke is kept in the `_enemy` columns and never counted in totals.

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

- State at t_activate and t_capture (`state_at_activate`, `state_at_capture`): score, cap owners and progress, ships alive by team and class, smoker HP and spotted flags, enemy radars alive, nearest enemy, nearest cap.
- `allies_in_smoke`, `enemies_in_smoke` at t_capture; ally and enemy ship-seconds inside over the life.
- `ships_at_capture`: living ships within 9 km of the origin at t_capture, with team, class, position and the owner mark, for the diagram.
- Score swing (site): the point gap (ours minus theirs) at capture minus the gap at activation. Smoker survival (site): the smoker was alive 60 s after dispersal, from the roster's death times.

### 6.8 Clan metrics (site)

uptime = seconds per game with at least one clan smoke standing (union of smoke lives); charge use = smoke activations over smoke charges carried by the clan's smoke ships; stacking rate = share of smokes overlapping another; contested-cap share = share of smokes within 1 km of a contested cap on average; selfish share; score swing = mean swing; smoker survival = share alive 60 s after; radar-punished share = share of smokes with at least one radar spot on the team's ships inside; offensive radar = enemies spotted by own radar from smoke; smokes near a cap capture; radar cap coverage = mean coverage and the count with full coverage. Every chart and stat shows its count (n).

## 7. Awards (round 3, no limit on awards per player)

Smoke awards each get a 5x clip and live on Home. Winners are from batch `output/20261103-185243`.

| Award | Definition and eligibility | Winner |
| --- | --- | --- |
| Smoke of the Tournament | Highest smoke_damage_total | HSR_Yamiyonohik, Somers, -BN- vs H-SR (Groups G3 R3) on Okinawa at 13:36, id 46513, 80,520 |
| Deepest Cap Smoke | Highest contested_cap_depth_pct among smokes with cap_won or cap_defended; ties by smoke_damage_total. Card shows the depth share, cap name and cap radius | RESIN_Fryce, Somers, RESIN vs BONKZ (LB R6 G3) on Sea of Fortune at 05:35, id 106317, 100% into cap C with cap D defended, 0 damage |
| Radar Bait | Most radar spots on the smoking team's ships inside while it stood; ties by radar_spotted_damage | PN_Sean_O_Reill, Harugumo, PN vs HTDOG (Groups G1 R4) on Land of Fire at 14:39, id 174224, 2 spots, 31,904 taken while spotted |
| Peekaboo | Most enemies spotted by the smoking team's own radar run from inside the smoke (offensive_radar.enemies_spotted); ties by damage | RESIN_Fryce, Harugumo, RESIN vs INCA (Groups G4 R5) on Mountain Range at 08:45, id 27145, 4 enemies by RESIN_thepregna's radar |
| Most Selfish Smoke | The selfish smoke with the most damage by its owner; shown once as "damage by the smoker (no teammate benefited)" | RESIN_Maddog242, Harugumo, BONKZ vs RESIN (WB R3 G1) on Sleeping Giant at 13:00, id 120803, 60,080 |
| Golden Cloud | Most total smoke damage | HSR_Yamiyonohik, 963,784 over 50 smokes |
| The Smokefather | Most smokes laid | HSR_Yamiyonohik, 50 smokes in 18 games |
| Best in Haze | Highest average damage per smoke, minimum 5 smokes | HSR_Yamiyonohik, 19,276 per smoke |
| Most Selfish Smoker | Most selfish smokes | RESIN_eagle_lan, 16 of 29 |
| Clan: most smokes laid (per game) | | H-SR, 4.5 over 22 games |
| Clan: most smoke damage (per game) | | H-SR, 71,046 over 22 games |
| Clan: most selfish smokes (per game) | | RESIN, 1.9 over 24 games |

History: round 1 and 2 Deepest Cap Smoke went to PN_Sean_O_Reill's Harugumo on Mountain Range (raw depth, then contested average distance); round 3's depth-share rule with the cap won or defended eligibility moved it. Round 1 and 2 Smoke of the Tournament was RESIN_Fryce's Harugumo on Mountain Range (88,586) before one-smoke credit and the weapon scope. Best in Haze moved from PN_Sean_O_Reill (4 smokes) when the minimum rose to 5.

## 8. The site

**Format and hosting.** Static HTML, CSS and JavaScript, no server; works from a local folder; published to GitHub Pages from `gh-pages` (section 3). Under 500 MB in total, no file over 100 MB, images as WebP, diagrams as SVG.

**Look.** Dark naval look: deep navy background, smoke-grey panels, white text. Team colours everywhere: H-SR gold #F5C542, RESIN sky blue #5DADE2, PN violet #B388FF; enemies red #F87171 in diagrams. A pinch of whimsy only (award names, "Nothing here, just clear skies." on an empty filter). Terms (selfish smoke, contested cap, every clan metric, every award) carry their definition as a tooltip wherever they appear.

**Navigation.** Home, Analysis, Clans, Players, Smokes, Maps, Games. `awards.html` is a one-line page pointing to Home, Players and Clans (the old link).

**Pages.**

1. Home: the mission briefing (purpose, counts: "217 smokes from 45 games (43 with at least one smoke)", how damage is credited), stat tiles per clan, the three headline findings each with one chart (average damage per smoke by clan; share within 1 km of a contested cap; radar-punished share), and the five award smokes with diagram, details and clip.
2. Analysis: the three findings with charts, then the clans compared: one chart per metric, a bar per clan with n, for every clan metric in 6.8 plus smokes per game, damage per game and average damage, and the reconciliation share.
3. Clans: an index, then one page per clan led by uptime, score swing and radar-punished share; the other metrics as tiles; "Where their games ended" (opening, mid, endgame columns, wins and losses stacked, counts on the bars); the timing bar (smokes per game standing in each phase); the most-smoked-spots heatmap (10 x 10 grid cells per map); the ship lineup (donut plus a table with class, smoke type, stock gun range, radar range, detection); the Top smokers strip (top 3 by share of the clan's smoke damage, linking to Players); the clan awards.
4. Players: the player awards as cards, then a sortable leaderboard (click a heading) with award badges; one page per player with stats, ships, a damage-per-smoke chart and every smoke as a card.
5. Smokes: every smoke in a table with filters (team, player, ship, map, game, type, phase) and sorts (damage total, inside, outside, fire, radar spots, own radar spots, duration, score change, depth, cap proximity, contested distance); each row has the diagram thumbnail, damage bar, cap outcome, flags (selfish, overlap, owner flag) and links.
6. Maps: one section per map with the minimap, the A to J and 1 to 10 grid, every cap as a lettered circle, and one line per smoke (puffs in laying order, arrow at the end, dashed for exhaust and crawling, click to open). Filters per map: a two-handle time-elapsed slider (0:00 left, 20:00 right; a smoke is shown when its activation falls between the handles), clan, spawn (north or south; east and west with a note where a map spawns that way) and ship, also presettable by query string (`?clan=&spawn=&ship=&from=&to=`). Four small charts per map for the smokes shown (smokes, average damage, average distance to the nearest contested cap, selfish share), each bar with n; clans with fewer than 5 smokes shown are greyed out.
7. Games: "Prototype: only series with H-SR or RESIN replays are linked so far." The full double-elimination bracket (winners rounds 1 to 4, losers rounds 1 to 6, grand final): one clickable box per series in the replay set with games won, greyed TBD boxes for the rest. Series pages list the games (score, map, winner) with links. Below, the group stage games filterable by clan and map.
8. Game pages: header (stage, map, date, score, winner, how and when it ended with the phase), the mini map with grid, caps and paths, a timeline and a score chart in real minutes for that game, rosters with smoke charges used over carried and spawn sides, the folded per-ship damage check, and the game's smokes as cards.
9. Smoke pages: header with countdown clock, elapsed time and phase; a one-line "what happened" summary (who, where, how long, allies firing, salvos and damage, cap outcome); an overlap note when it applies; the full activation and capture frames (no inset); the two zoomed screenshots and the diagram as separate images; the clip for award smokes ("Clip available on request" otherwise); the stats table (duration, damage by where the shooter sat and by kind, shooters and salvos, radar spots and damage while spotted, own radar, cap proximity, contested cap, supported caps, cap outcome, radar cap coverage, denial signal, allies inside, selfish, score and swing, smoker alive 60 s after, ships alive); tags ("untagged"); navigation.
10. Thumbnails everywhere are the diagram: puffs, nearby caps, nearby ships as team-coloured triangles (red = enemy, gold ring = smoker), arrows from credited shooters to targets labelled with damage, a 1 km bar; no names or HP.
11. Mobile, light touch: the nav collapses behind a Menu button under 800 px, charts fit the width, wide tables scroll sideways.

## 9. Outputs per smoke

- Frames: activation and capture, the renderer's merged minimap view with names, HP bars, detected outlines, caps, score, timer and rosters; the target smoke outlined in yellow (union of its puffs), a ring on the smoker before the smoke exists, a magenta dashed trail for exhaust and crawling smoke, exhaust puffs in light orange; a header strip (ordinal, team, player, ship, type, charge, activation to capture clocks, base stats, score, caps, alive, HP, spotted, enemy radars) and a footer (tournament, round, map, build). Saved as PNG and WebP, named `<match>_<game>_<team>_<player>_<ship>_s<nn>_{act|cap}_<mmss>`.
- Zoomed screenshots: the map around the smoke at 2.5x, saved on their own as `<stem>_zoom`; no longer pasted into the frame.
- Clips: from activation minus 5 s to dispersal, 20 fps, `render.clip_speed` times real time (award clips at 5x, 1200 kbps, about 35 s and 3.5 MB each), H.264 MP4 from the CPU encoder, with the same overlays and header plus a progress marker; no inset. Every smoke gets a clip when `--clips` names it; the site publishes the five award clips only.
- Metadata record (smokes.json, smokes.csv): identity (smoke_id, activation_id, match_id, round, game_no, map, map_display, game_build, replays, team, opponent, spawn_side, player, ship, ship_class, ship_tier); smoke (smoke_type, variant, charge_no, charges_total, base_emission_s, base_puff_life_s, base_radius, radius, observed_emission_s, emission_cut_short, owner_flag, owner_note, owner_distance_m, overlap_flag, overlapping_smoke_ids, origin_xy, bbox, puff_count, path); times (t_created, t_activate, t_capture, t_emission_end, t_dispersed, each as replay seconds and clock); state_at_activate and state_at_capture; Tier 2 (allies_in_smoke, enemies_in_smoke, ally and enemy ship-seconds, radar, hydro and fired-while-concealed detections); damage (damage_in_smoke, damage_behind_smoke, smoke_damage_total, the _enemy columns, damage_detail with the smoker/ally/enemy split, damage_shell, damage_fire, salvos, shooters, arrows); caps (cap_proximity_m, cap_proximity_name, cap_radius_m, contested_cap_name, cap_contested_reason, avg_contested_cap_dist_m, contested_cap_depth_pct, contested_cap_radius_m, supported_caps, cap_won, cap_won_at, cap_defended, radar_cap, cap_denial); radar (radar_spotted_damage, offensive_radar); selfish_smoke; shooters; ships_at_capture; provenance (wows_toolkit_rev, smoke_signals_version, generated_at); files (frame_act, frame_cap, frame_act_zoom, frame_cap_zoom, clip).
- Game record (game.json): tournament, match_id, round, game_no, map names, build, replays, teams (name, team_id, spawn_side, spawn_xy, final_score, players with entity_id, player, clan, ship, class, tier, smoke variant and type, smoke_activations, smoke_charges, death, gun_range_m, radar_m, detection_m), caps (letter, position, radius, radius_m, kind), outcome, finish_type, battle_start_s, battle_end, replay_end_s, replay_truncated.
- damage_spike.json: events and damage by source and by kind, per-attacker totals (all and shell-plus-fire), the game's per-attacker totals, the per-ship reconciliation table and ratios, duplicate counts, hit, salvo and torpedo counts. damage_events.csv: every event with its kind, firing moment and source, detection at fire, in_smokes, behind_smokes and credited shares.

## 10. Known limits

- Damage kinds are inferred from timing. Fire ticks are linked to the shooter's latest shell on the same target within 75 s, so a long burn is credited to one salvo; "unknown" damage (about 9% of all damage) includes secondaries and shells whose salvo was not seen.
- Reconciliation per game ranges from 0.71 to 1.16 of the game's totals. Games below 1 are missing hits neither perspective saw or where equal-amount events were folded that were real; games above 1 still carry some duplicates whose clocks drifted more than the window. The per-ship table on each game page shows where.
- Offensive radar spots are inferred from our activation and range, not read from the replay, so a spot by another radar in range at the same time is counted too.
- The line-of-sight test uses the hull's base detection range, not the build's concealment; enemies within the base range but outside the real detection range can mark a smoke as needed.
- The Deepest Cap Smoke can be a zero-damage smoke, since defending a contested cap is enough for eligibility (current winner).
- Smoke objects come from the primary replay only; a smoke the primary recorder never saw is not in the table.
- A team without a replay has every smoke flagged for owner attribution; 22 of 217 smokes carry an owner flag.
- Crawling smoke has no test coverage (none in the replay set).
- The bracket shows only the series in the replay set; the other series are TBD placeholders.
- The game and clips folders are large (`smoke-site/` about 240 MB, mostly frames); image compression is deferred.
- Headless Chrome cannot screenshot below about 500 px wide; mobile is checked in the app's browser pane.

## 11. Open questions

- [ ] Deepest Cap Smoke: keep the zero-damage winner (eligible by defence) or also require damage? Asked 3 Nov 2026, not yet answered.
- [ ] PN scope: group stage only now; add PN clan battle replays after the demo?
- [ ] Purpose list and rating scale for hand tagging (section 12): confirm before tagging starts.
- [ ] Phase 3 host: decide after the demo; clip storage drives the cost.
- [ ] Crawling smoke capture rule: untested until a replay contains one.
- [ ] Whether to reduce "unknown" damage by matching secondaries (ATBA) salvos.

Decided and closed: behind-smoke damage needs the line of fire through a puff (2 Nov); overlapping smokes credit one smoke per shot (3 Nov, replacing "credit both and flag"); enemies in our smoke count in separate columns only; clip window activation minus 5 s to dispersal; team colours; five award clips; map names from the game catalog; Mountain Range cap A is real; spawn labels north and south; cap proximity excludes inside-cap smokes; time axes as elapsed with the countdown in per-smoke text; awards.html stays as a pointer page.

## 12. Hand-tagging (deferred, Phase 2 plan)

Sean tags smokes in a spreadsheet and one command imports the tags; reruns never overwrite them. Each run would write `tags.csv` (smoke_id, team, player, ship, map, clock, frame files, empty tag columns); `smoke_signals import-tags tags.csv` would load it into a `smoke_tags` table keyed by smoke_id. Columns: purposes (cap_contest, disengage, cover_ally, cruiser_firing, torpedo_setup, spotting_denial, push_support, bait, other, several separated by `;`), initiative (proactive or reactive), rating (1 wasted to 5 decisive), notes, tagged_by, tagged_at. Not built yet; smoke pages show "untagged".

## 13. History and validation

- 2 Nov 2026 prototype: a test tool found all 6 H-SR smokes in Grand Final G1 and rendered each in about 1 s; those smokes are the golden test (YuriSayuki Harugumo at 18:04, 14:39, 11:14 captured 17:11, 13:46, 10:21; Yamiyonohik Somers at 13:37 and 08:37 captured 12:54 and 07:53; Apex_captai Conte Verde exhaust at 08:17 captured 07:27). Lessons: time emission by new puffs, exhaust needs its own rule, owner needs proximity and activation, emission differences come from builds, merged positions need the position timeline with a minimap fallback.
- 3 Nov 2026: M1 to M4 done overnight; M3.1 visual fixes (union outline, zoomed inset, magenta trail, clip speed); Phase 2 rounds 1 to 3 as in section 2. The ledger duplicate problem was found by the round 3 reconciliation check and fixed the same day.
- Upstream feature requests for the wows-toolkit author: dump a frame at an exact battle clock; a smoke-event export (smoke id, owner, puff timestamps, variant); move the game-data loader into the library (done in the fork as the only upstream change).
