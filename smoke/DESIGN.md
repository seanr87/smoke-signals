# Smoke Signals — Design Doc & Claude Code Handoff

Nov 2, 2026 · Sean
Live version: https://claude.ai/artifact/RjNfs47CQrkYWfZ6vMXPG1

## Goal and scope

For every smoke in King of the Sea XIX NA, the tool produces two minimap frames, a short video clip and a metadata record. The goal is to learn how competitive teams use smoke effectively.

- **Teams:**
  - **H-SR:** NA regional winner
  - **RESIN:** runner-up
  - **PN:** our clan, as the comparison
- **Games:** NA group stage and regional playoffs. PN didn't make the playoffs (confirm), so PN is group stage only.
- **Per smoke:**
  - A frame at activation, showing the situation that led to the decision to smoke
  - A frame at the capture moment, which depends on the smoke type
  - A clip with gunfire visible
  - Context and outcome metrics, including smoke damage and radar detections
- **Analysis framing:**
  - About 300–400 smokes supports descriptive patterns and strong examples, not causal claims.
  - Comparisons: H-SR vs RESIN vs PN, and won vs lost games.

## Project phases

There are three phases. The interactive features wait until clan leadership has seen the Phase 2 demo.

| Phase | Goal | Scope | Main additions | Exit criteria |
| --- | --- | --- | --- | --- |
| 1. Prototype | Prove the pipeline end to end | Grand Final G1, H-SR only | Fork of wows-toolkit with a `smoke_signals` program; smoke detection, owner and type; capture rules; two frames, header and clip; Tier 1 and 2 metrics including radar while concealed; spike on smoke damage; golden test | Golden test passes and Sean's spot-checks match the replay |
| 2. Demo | Show leadership everything except the interactive features | H-SR, RESIN and PN: group stage and playoffs | Replay inventory and batch runs; build data (commander skills and upgrades) and effective smoke stats; Tier 3 smoke damage and outcomes; SQLite database; CSV hand-tagging; read-only local gallery; pattern summary | Demo is presented |
| 3. Interactive | Let clan members tag and discuss smokes | Decided after the demo | Choose a host (Supabase, the clan site, or other); login; tag dropdowns; comments; access control; move SQLite data to the host; host the clips | Leadership sign-off |

**Costs:** none through Phase 2. SQLite is free, open-source software, and the database is a single file. Phase 3 hosting costs depend on the chosen host and on clip storage.

## Inputs

Replays come from the tournament site. Game data comes from a public GitHub repo, so no game install is needed.

**Replays**

- Each [match page](https://wows-tournaments.com/king-of-the-sea-xix/na/matches) links both teams' replays at `/api/matches/report/replay?id=<n>`.
- **Replay inventory (Phase 2, step 1):** a script on the laptop lists every H-SR, RESIN and PN game (match id, round, game number, opponent, and whether each team's replay is available) and downloads them to `replays/<match>/<game>/`. Games missing a replay are logged, and use whichever team's replay is available.
- Always merge both teams' replays. The primary replay is the team being analyzed.

**Game data**

- **Option A (preferred):** download pre-dumped data for the replay's build from [landaire/wows-replay-data](https://github.com/landaire/wows-replay-data), the same source the wows-toolkit app uses. It has builds through 15.9.0 (dumped 9 Oct 2026), and all KotS XIX replays are 15.9.0. Fetch only `<version>_<build>/` and the `common/` objects it references.
- **Option B (fallback):** run `wows-data-mgr dump-renderer-data` on the desktop, which has the game installed.
- Keep every build you download, so that older replays still render.

**Render approach**

- **Fork [landaire/wows-toolkit](https://github.com/landaire/wows-toolkit)** (MIT license) and add a new workspace crate, `crates/smoke-signals`.
- **Loader move:** the game-data loading functions live in `minimap-renderer/src/main.rs`, not in its library. Move them into a small library module. This is the only change to upstream code, and it could be offered to the author upstream.
- **Why a fork:** after a game patch, updating is just pulling the author's changes.
- **Reused as-is:** the merged replay session, the battle state, the minimap drawing code and the image output. The look matches wows-toolkit exactly.
- **Added by smoke_signals:**
  - Rendering at any exact time
  - Smoke tracking, owner and type
  - Overlays and the header
  - Metrics
  - Clips

## Smoke definitions

A smoke is one smoke object in the replay. Its owner and type come from the ship and consumable that created it, and its capture moment depends on the type.

**What the replay provides**

- `view.smoke_screens()` gives each smoke object's `radius`, `position` (origin) and `points` (the puffs).
- The puff list grows as puffs are laid and shrinks as they fade. It records **no owner and no per-puff timestamps**, so the tool watches it change on every replay update and records the times itself.

**Lifecycle**

1. **Activation** (`t_activate`): the player triggers the consumable.
2. **Emission:** new puffs are added until `t_emission_end`.
3. **Standing:** no new puffs. This phase is effectively absent for exhaust and crawling smoke, whose puffs fade quickly.
4. **Dispersed** (`t_dispersed`): the smoke object is removed.

**Owner**

- Candidates are the player ships fitted with a smoke consumable. The owner is the nearest candidate that activated smoke in the 5 s before the object was created.
- If no candidate activated smoke in that window, the nearest candidate is the owner and `owner_flag` is set with a note. The flag is also set when the owner's position came only from minimap samples (a ship outside both recorders' area of interest) or when the nearest candidate was more than 50 m from the origin.
- Each replay records smoke activations for its own team only, so a team without a replay has every smoke flagged. Using nearest-ship alone misattributed smokes to cruisers parked inside a destroyer's smoke in the test.
- Smoke objects are tracked from the primary replay only (the merge keeps entity lifecycle with the primary), so a smoke the primary recorder never saw is not in the table even when the other team's replay is merged.

**Smoke types and capture rules**

The game files label every smoke `smokeGenerator`. The type comes from the variant in the owner's `ShipAbilities` in GameParams.

| smoke_type | How it's identified | Base stats (game data) | t_capture |
| --- | --- | --- | --- |
| standard | Default destroyer and cruiser variants, e.g. `Lvl_10_Gold`, `US_Lvl_10_Gold` | Emission 20–30 s, puffs last 97–130 s, speed limit 12.5 | Last new puff before the first puff fades |
| exhaust | Title contains `Oil`, e.g. `IT_Oil_Verde`; puffs last about 10 s | Emission 45 s, puffs last 10 s, no speed limit | End of emission. Draw a dashed outline of the trail's path. |
| crawling | Crawling-smoke variant (name to confirm; not in the test game) | To confirm | End of emission, as for exhaust. Untested until a replay contains one. |

- **New puff:** the last point changed and the puff count did not drop.
- **Build modifiers:** commander skills and ship upgrades lengthen emission and puff lifetime. Observed emission was 53 s against a 20 s base for Harugumo, and 44 s against 30 s for Somers.
  - Phase 1 records the observed and base values. It doesn't flag the difference.
  - Phase 2 stores each player's build, computes effective stats, and flags only differences from those.

**Edge cases**

- **Smoker dies mid-emission:** set `emission_cut_short`.
- **One activation creating several smoke objects:** keep one record per object, linked by `activation_id`.
- **Clock:** store replay seconds plus the battle clock. The battle clock is the HUD countdown value the game reports (a whole-second server property), which runs about a second ahead of battle start plus elapsed replay time; every `mm:ss` in the outputs is the HUD value at that replay second.

## Metric definitions

Smoke damage has three parts: damage dealt *in* the smoke, damage dealt from *behind* it, and their total. Radar detection of concealed ships is a Tier 2 context metric. Every metric is measured over the smoke's life, from `t_activate` to `t_dispersed`.

**Terms**

- **In the smoke:** a ship's position is within `radius` of any puff of this smoke.
- **Undetected:** the ship's `visibilityFlags` is 0. The replay also records *why* a ship is detected: `BY_SHIP`, `BY_RLS` (radar), `BY_SONAR` (hydro), `IN_SMOKE` (fired from inside smoke) and others.
- **Concealed by the smoke:** in the smoke and undetected, or behind it as defined below.

**Smoke damage (Tier 3)**

| Metric | Definition |
| --- | --- |
| damage_in_smoke | All damage dealt by ships that are in this smoke at the moment they fire. |
| damage_behind_smoke | Main-gun damage from ships that are outside the smoke, undetected when they fire, and whose line of fire to the target passes through a puff of this smoke that lies nearer the shooter than the target (added in M4: without that clause, fire merely crossing a smoke next to the target was credited). |
| smoke_damage_total | damage_in_smoke + damage_behind_smoke |

- Each metric is broken down by shooter (smoker or ally) and by team.
- Damage counts by when the shot was fired, even if it lands after the smoke disperses.
- **Attacker (resolved in M4):** the replay's damage events do name the attacker ship (the toolkit's damage ledger keys `receiveDamagesOnShip` by aggressor). What has to be reconstructed is the firing moment and position; see `smoke/M4_DAMAGE_SPIKE.md` for the three sources used and the recommendation.

**Decided rules (2 Nov)**

- **Behind smoke** requires the line of fire to pass through a puff of this smoke.
- **Overlapping smokes:** damage that qualifies for more than one smoke is credited in full to each, and the record sets `overlap_flag` and lists the other smoke ids. Totals across smokes can therefore double-count, so summaries de-duplicate by shot.
- **Enemies in our smoke:** their damage counts too, in separate columns (`damage_in_smoke_enemy`, and the same for the other metrics).

**Radar while concealed (Tier 2)**

- `radar_detections_in_smoke`: one row for each time a ship concealed by this smoke (inside it and undetected) gains the `BY_RLS` flag. The row records:
  - The ship and the time
  - The likely radar ship: the nearest enemy with radar running at that moment, its distance, and whether the ship is within that radar's base range
  - How long the ship stayed detected (until the flag clears)
- `hydro_detections_in_smoke`: the same rows for `BY_SONAR`.
- `fired_while_concealed_detections`: times a concealed ship became detected by firing (the `IN_SMOKE` flag).

**Other context and outcomes**

| Metric | Tier | Definition |
| --- | --- | --- |
| allies_in_smoke | 2 | Ships of the smoker's team in the smoke at t_capture, and ship-seconds in the smoke over its life (allies and enemies kept apart) |
| nearest_enemy_dist_km | 2 | From the smoker to the nearest living enemy, at t_activate and t_capture |
| dist_to_nearest_cap_km, cap_contested | 2 | From the smoker to the nearest enabled cap, and whether that cap has invaders, at t_activate and t_capture |
| enemy_radars_alive | 2 | Enemy ships with radar charges left, at t_activate |
| kills_during_smoke, deaths_in_smoke | 3 | Over the smoke's life |
| cap_flips_during_smoke | 3 | Over the smoke's life |
| score_delta_60s | 3 | Change in the point gap from t_activate to t_activate + 60 s |
| smoker_survived_60s, game_result | 3 | |

## Outputs

Each smoke produces two frames (activation and capture), one clip and one metadata record. Each run writes them to a new `output/<timestamp>/` folder and never overwrites an earlier run.

**Frames**

- The renderer's normal merged-view frame:
  - Player and ship names, HP bars, and a yellow outline on detected ships
  - Caps, score bar, timer, kill feed and team rosters
  - Gunfire tracers and torpedoes
- **Smoke colors:**
  - Standard smoke: the renderer's grey
  - Exhaust and crawling smoke: light orange (proposed)
  - Target smoke: a highlight ring
- **Exhaust and crawling smoke:** a dashed outline of the trail's full path from activation to t_capture.
- **Files:** `<match>_<game>_<team>_<player>_<ship>_s<nn>_{act|cap}_<mmss>`, as PNG plus a WebP copy for the gallery.

**Header strip (about 60 px, above the render)**

An example with made-up values:

- Line 1: `#2 · H-SR · YuriSayuki · Harugumo (DD X) · standard smoke, charge 2/3 · 14:39 → 13:46 (53 s)`
- Line 2: `Build: <skills/upgrades> · emission 53 s (base 20) · puff life 97 s · Score 486–492 · Caps A● B○ C● D○ · Alive 9v9 · HP 85% · Spotted no · Enemy radars 2`
- Footer: `KotS XIX NA · Grand Final G1 · Sleeping Giant · 15.9.0`
- Phase 1 shows base stats only. The build appears once Phase 2 build data exists.

**Clip**

- Runs from t_activate − 5 s to t_dispersed (the last puff gone), at real time and 20 fps, as MP4 (H.264). Standard smoke clips run about 2–3 minutes (roughly 5–15 MB). Exhaust clips run about 1 minute.
- **Gunfire must be visible:** main-battery tracers, secondary tracers and torpedoes on, with tracer pacing following the render clock as in the renderer's video mode.
- Uses the same overlays and header, plus a progress marker showing activation → capture → now.
- Encoder: the toolkit's CPU H.264 encoder (the `cpu` feature, openh264), so no NASM or GPU is needed.

**Metadata record (unified field names)**

| Group | Fields |
| --- | --- |
| Identity | smoke_id, activation_id, match_id, round, game_no, map, game_build, primary_replay, merged_replays, team, opponent, spawn_side, player, ship, ship_class, ship_tier |
| Smoke | smoke_type, variant, charge_no, charges_total, base_emission_s, base_puff_life_s, base_radius, observed_emission_s, emission_cut_short, owner_flag, overlap_flag, overlapping_smoke_ids, origin_xy, bbox, puff_count, path (exhaust and crawling only) |
| Times (replay s and battle clock) | t_activate, t_capture, t_emission_end, t_dispersed |
| State at t_activate and t_capture (Tier 1) | score_ours, score_theirs, cap_state per cap (owner, progress, contested), ships_alive by team and class, smoker_hp_pct, smoker_spotted (with reason flags) |
| Tier 2 | allies_in_smoke, nearest_enemy_dist_km, dist_to_nearest_cap_km, cap_contested, enemy_radars_alive, radar_detections_in_smoke, hydro_detections_in_smoke, fired_while_concealed_detections |
| Tier 3 (Phase 2) | damage_in_smoke, damage_behind_smoke, smoke_damage_total (each broken down, plus _enemy columns), kills_during_smoke, deaths_in_smoke, cap_flips_during_smoke, score_delta_60s, smoker_survived_60s, game_result |
| Build (Phase 2) | commander_skills, upgrades, effective_emission_s, effective_puff_life_s |
| Provenance | wows_toolkit_rev, smoke_signals_version, generated_at |
| Files | frame_act, frame_cap, clip |

## Hand-tagging (Phase 2)

Sean tags the demo smokes in a spreadsheet, and one command imports the tags. Reruns never overwrite them.

1. Each run writes `tags.csv`: one row per smoke with smoke_id, team, player, ship, map, battle clock, frame file names, and empty tag columns.
2. Sean fills it in Excel or Google Sheets.
3. `smoke_signals import-tags tags.csv` loads it into the `smoke_tags` table, keyed by smoke_id. It reports any rows it doesn't recognise.

| Column | Values |
| --- | --- |
| purposes | One or more, separated by `;`: cap_contest, disengage, cover_ally, cruiser_firing, torpedo_setup, spotting_denial, push_support, bait, other |
| initiative | proactive (planned) or reactive (forced by being spotted or taking damage) |
| rating | 1 = wasted, 2 = little value, 3 = neutral, 4 = useful, 5 = decisive |
| notes | Free text |
| tagged_by, tagged_at | Who tagged it and when, so more people can tag later |

## Phase 1 plan

Phase 1 is done when the golden test passes and Sean's spot-checks match the replay. Claude Code stops at each milestone for Sean to review.

1. **M1: fork, build and one frame.** Fork wows-toolkit, add `smoke_signals`, download the 15.9.0 game data, and render one merged frame at an exact battle-clock time.
2. **M2: smoke table.** Track smokes and find owners and types, using the reference test code. Output must match the golden test (below). Fix the RESIN missing-position gap.
3. **M3: images and clips.**
   - Activation and capture frames, with colors, highlight ring, exhaust path outline and header
   - Clips with gunfire visible
   - Tier 1 fields
4. **M4: Tier 2 and smoke-damage spike.**
   - Radar, hydro and fired-while-concealed detections from visibilityFlags
   - Allies in smoke, distances and radars alive
   - A spike on how to find the attacker for damage, with a written recommendation for Phase 2

**Validation**

- [x] **Golden test** (`cargo test`, data in `smoke/tests/golden_gf_g1_hsr.csv`), Grand Final G1. Activation and capture times must be within 1 s. The test skips with a message when the local replays or game data are absent.
  - YuriSayuki, Harugumo, standard: activations at 18:04, 14:39 and 11:14; captures at 17:11, 13:46 and 10:21
  - Yamiyonohik, Somers, standard: activations at 13:37 and 08:37; captures at 12:54 and 07:53
  - Apex_captai, Conte Verde, exhaust: activation at 08:17; capture at the end of emission, 07:27
  - These are HUD battle clocks (M1). The original formula-based values are kept in `smoke/tests/golden_gf_g1_hsr_v1_formula.csv`; they differ by at most 1 s for standard smoke and by 5 s for the exhaust row, whose capture rule was approximate.
- [ ] Sean spot-checks three smokes in the replay: capture timing, positions, detection outlines, caps and score.
- [ ] Gunfire is visible in every clip.
- [ ] Every Tier 1 field is filled, or run_log.md says why not.
- [ ] The tool builds from a fresh clone on the desktop.

## Setup and handoff

The work lives in a fork of wows-toolkit, on a `smoke-signals` branch. Our own docs sit in `smoke/`, and the fork's existing AGENTS.md and CLAUDE.md conventions still apply.

**Repo layout (fork)**

```
crates/smoke-signals/               new crate: the smoke_signals program
smoke/CLAUDE.md                  project rules for Claude Code
smoke/DESIGN.md                  this document
smoke/PROMPT_M1.md               the first Claude Code prompt
smoke/reference/smoke_probe.rs   working test code from 2 Nov (reference only)
smoke/tests/golden_gf_g1_hsr.csv expected smokes for the golden test
smoke/config.example.toml        paths: replays, game data, output
replays/  output/  game_data/  config.toml   (all gitignored)
```

**Build notes (found in testing)**

- The repo's `rust-toolchain.toml` pins Rust 1.97, so install that toolchain with rustup.
- Build with `cargo build --release -p smoke-signals`. Depend on `wows_minimap_renderer` with `default-features = false, features = ["bin", "arc", "cpu"]`. This leaves out Vulkan and the assembly-optimized AV1 encoder, which needs the NASM assembler. (The test build used `bin,arc`; `cpu` for clips is untested.)
- **Windows:** wows-replay-data stores files as symlinks, which Windows git checks out as plain text by default. Files are found through `metadata.toml`, so this should be harmless, but confirm in M1. If it isn't, enable `core.symlinks` with Windows Developer Mode, or use wows-data-mgr's download code.
- The fork's AGENTS.md says to use `jj` for version control and not to add AI attribution to commits. Follow it on this branch.
- After a game patch: pull the author's changes into the fork, download the new build's game data, and re-run the golden test.

## Prototype test results (2 Nov 2026)

A quick test tool built on wows-toolkit found all 6 H-SR smokes in Grand Final game 1 (Sleeping Giant, build 15.9.0) and rendered each one in about 1 s per game. The method works. These results become the golden test. Raw outputs are in `exploration/`.

| # | Player | Ship | Type (variant) | Activated | Captured | Observed emission (base) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | YuriSayuki | Harugumo | standard (Lvl_10_Gold) | 18:05 | 17:11 | 53 s (20) |
| 2 | YuriSayuki | Harugumo | standard | 14:39 | 13:46 | 53 s (20) |
| 3 | Yamiyonohik | Somers | standard (US_Lvl_10_Gold) | 13:37 | 12:54 | 44 s (30) |
| 4 | YuriSayuki | Harugumo | standard | 11:14 | 10:21 | 53 s (20) |
| 5 | Yamiyonohik | Somers | standard | 08:38 | 07:54 | 44 s (30) |
| 6 | Apex_captai | Conte Verde | exhaust (IT_Oil_Verde) | 08:17 | about 07:32 (end of emission) | about 45 s (45) |

- **Merged replays:** true positions for every ship, with detected ships outlined in yellow.
- **Lessons built into this design:**
  - Use "new puff" rather than puff count to time emission.
  - Exhaust smoke needs its own rule.
  - Owner attribution needs both the proximity and activation checks.
  - The difference from base stats comes from player builds.
- **Known gap (fixed in M2):** some RESIN ships, including Fryce (the player whose replay was merged in), had no position in the merged view. Two causes: the merge never forwards a second replay's own-ship position packets (`PlayerOrientation`), and ships outside both recorders' area of interest have only minimap-resolution positions and no consumable events. Smoke Signals reads positions from the merged position timeline (which has every replay's packets) and falls back to minimap samples, flagged.

## Open questions

Items 1–4 were decided on 2 Nov. Proposed defaults for the rest are in brackets.

- [x] 1. Behind-smoke damage: the line of fire must pass through a puff.
- [x] 2. Overlapping smokes: credit both and flag it.
- [x] 3. Enemies in our smoke: yes, in separate columns.
- [x] 4. Clip window: activation − 5 s until the smoke disperses.
- [ ] 5. **PN scope:** group stage only? Add PN clan battle replays later? [Group stage now; clan battles after the demo]
- [ ] 6. Exhaust and crawling smoke color (light orange) and the header layout: confirm from the M3 renders.
- [ ] 7. Purpose list and rating scale for tagging: confirm before Phase 2.
- [ ] 8. Phase 3 host: decide after the demo; clip storage affects the cost.
- [x] Prototype game: Grand Final G1. Minimap look: wows-toolkit, merged. Smoke types: standard, exhaust and crawling. Emission differences: explained by builds, stored in Phase 2.

**Upstream feature requests (an issue for the wows-toolkit author)**

- `--dump-at <battle clock>`: dump a frame at an exact game time instead of a frame number
- A smoke-event export: smoke id, owner, puff timestamps, and the consumable variant
- Moving the game-data loader into the library

## Claude Code prompt

See `smoke/PROMPT_M1.md`. Later milestones need only short prompts, for example: "Go ahead with M2 per DESIGN.md; the golden test must pass before you stop."
