# Overnight log (3 Nov 2026): M3 and M4

Morning summary is added at the top when the run ends. Entries below are in order of work.

## M3 step 1: golden test fails without inputs

- Decision: the reference test now fails when config.toml or the replay and game data folders are missing, unless `SMOKE_SIGNALS_SKIP_GOLDEN=1` is set. The earlier `SMOKE_SIGNALS_REQUIRE_REFERENCE` switch is removed; one switch is enough.

## M3 steps 2 to 4: frames, clips, Tier 1

- Header text is ASCII per the fork's AGENTS.md: fields are separated by `|` and the clocks by `->`, instead of the middle dots and arrow in DESIGN.md.
- Header line 2 shows base stats only (emission base and puff life); the build appears in Phase 2. The rest of line 2 is the Tier 1 state at that frame's moment, so it differs between the activation and capture frames.
- Caps are written `A:H-SR B:- C:RESIN!` where `!` marks a cap with invaders and `!!` a cap with both teams inside. Ships alive are `ours v theirs`; the per-class split is in the CSV and JSON.
- Footer: tournament name (new `[game] tournament` config key), round and game, map title, client version. Placed as a strip below the frame; the header strip (64 px) sits above.
- Exhaust and crawling smoke puffs are recolored to `render.exhaust_color` by matching the renderer's smoke draw commands to the smoke object's puff positions. The dashed outline of the trail is the smoke's full path (every puff laid from activation to capture) drawn as dashed polylines in the same color; it is drawn on both frames.
- Each frame is saved as PNG plus a WebP copy (the image crate's WebP encoder was already in the build, no install).
- Tier 1 state is taken in the frames pass at the activation and capture moments, so `--no-frames` leaves those fields empty. A smoke with no recorded activation uses its first appearance as the activation moment for the frame, the state and the clip start.
- The smoker's `spotted` value is the merged view's visibilityFlags for the smoker's ship. For the analyzed team's own ships that is the game's "detected" indicator; for enemy ships it is whether the recorder's team sees them. Flags are kept verbatim, e.g. `BY_SHIP|IN_SMOKE`.
- Clips: the toolkit's VideoEncoder muxes at a fixed 30 fps, so Smoke Signals drives its encoder worker directly (CPU H.264, openh264) and muxes with muxide at `render.clip_fps` (20). The encoder drops zero-byte skip frames; the muxer then extends the previous frame, so a clip keeps its real-time length (checked from the MP4 header: 1291 frames at 20 fps = 64.55 s). Tracers and torpedoes are on by default in the renderer options and are paced by the render clock, the same as the toolkit's own video mode.
- Clip progress marker: a bar at the bottom of the header strip; yellow ticks at activation and capture, the filled part is elapsed clip time, white tick is now.
- The first test clip (Conte Verde exhaust, 65 s) encoded in 40 s, so the full set of 14 clips is expected to take about 30 minutes.
- Not verified visually: the clips themselves (no video decoder is available here; the frame path is the same as the stills, which were checked).

## M4 step 1: Tier 2

- Tracked inside the analysis pass (no extra replay pass): every 0.25 s of replay time each living ship is tested against every live smoke object (inside = within the smoke radius of any puff), which gives ship-seconds in smoke and the ships inside at t_capture. Visibility flags are checked on every packet.
- A detection counts for a smoke when a ship that was inside that smoke and undetected gains the flag: `BY_RLS` for radar, `BY_SONAR` for hydro, `IN_SMOKE` for firing from smoke. The "behind the smoke" form of concealment is not used for Tier 2, only for the damage spike, because a ship behind a smoke is usually just unspotted rather than concealed by it.
- The likely radar or hydro ship is the nearest enemy whose consumable is running at that packet (activation time plus duration), with the distance and whether the ship is inside that consumable's base range from GameParams. `detected_for_s` is the time until the flag clears.
- `allies_in_smoke` lists the smoker's team inside at t_capture; enemies inside are listed separately. Ship-seconds are split the same way.
- `nearest_enemy_dist_km`, `dist_to_nearest_cap_km` and `cap_contested` (the nearest cap has invaders) are part of the Tier 1 snapshot taken at t_activate and t_capture in the frames pass, since they need a moment. `enemy_radars_alive` was already there.
- Visibility flags come from the merged view, which carries them for the recorder's own team (the game's detection indicator) and for enemy ships as seen by the recorder's team. Detections of enemy ships inside their own smoke therefore mean "our team detected them".

## M4 step 2: damage spike (method)

- Surprise: the toolkit's damage ledger (`receiveDamagesOnShip` from every merged perspective, deduplicated) already names the aggressor ship for each damage event, so "who dealt it" is not the open problem DESIGN.md expected. The open problem is the firing moment and position, which the spike resolves from three sources, best first: a resolved shot hit (same attacker and victim, impact within 1 s of the damage: exact fire time and shell origin), the attacker's latest salvo in the 25 s before the damage (fire time and origin), or the attacker's position at the damage clock.
- `damage_in_smoke`: the attacker's firing position lies within a standing puff of the smoke. `damage_behind_smoke`: the attacker is outside the smoke, undetected at the firing moment (flags as last reported), and the horizontal line from the firing position to the victim's position at impact passes within the smoke radius of a standing puff. A puff stands from the moment it was laid until its base lifetime or the object's removal.
- Credit goes in full to every smoke that qualifies (DESIGN rule 2); the split is smoker / ally / enemy relative to the smoke's owner. `damage_in_smoke` and `damage_behind_smoke` in the table are the smoker's team only; enemy damage is in separate columns, as decided.
- Hits and salvos are accumulated from the merged view during the pass (the toolkit's whole-match logs are crate-private). Resolved shot hits come from the primary replay only; salvos come from both replays.

## M3 full run (output/20261103-012250)

- 14 smokes, 56 frame files (activation and capture, PNG and WebP each), 14 clips (166 MB, 5 to 17 MB each), 23 minutes end to end.
- Tier 1 gaps: 13, all data limits, listed with reasons in that run's run_log.md. Three RESIN smokers (Big_Boy69 twice, Fryce once) have no vehicle state in the merged view at the moment, so their HP and detection are unknown; the merge only creates enemy vehicles the primary recorder has seen. Two smokes were still standing at the replay end.
- Decision: at the activation moment the smoke object does not exist yet (it appears about 2.5 s later), so the activation frame has no puffs to ring. A yellow ring is drawn around the smoker's own position instead, so the frame still marks where the smoke starts. Same for the first seconds of each clip.

## M4 run (output/20261103-021955)

- Tier 2: two "fired while concealed" events (Klee_Fleein in Yamiyonohik's 08:37 smoke, Apex_captai in his own exhaust); no radar or hydro detection of a smoked ship in this game. The flag diagnostics in tracks.csv show radar flags were gained 1 to 6 times per ship over the game, so the detection code sees the flags; the smoked ships were simply never radared while inside. Hydro (`BY_SONAR`) never appears in these replays.
- Yamiyonohik's 13:37 smoke has 0 ship-seconds inside: a Somers laying smoke at speed leaves the puffs behind within a second. Real, not a bug.
- Damage spike: three dedup rules were tried. Exact-clock union (the toolkit's own) left cross-perspective duplicates (1,537 events, 1.41M damage against a 0.98M HP pool). Victim-team-only (take hits on a team from that team's replay) was wrong, because a client sees hits inside its area of interest, not on its team: totals fell to 0.90 of the game's. One-to-one matching within 1.5 s gives 0.99 of the game's total with every player between 0.86 and 1.15. Kept the last.
- The game's own per-player damage totals are decoded from the battle results blob with the field map in the build's constants.json (`CLIENT_PUBLIC_RESULTS_INDICES`, index 426 is `damage`). Written to battle_results_players.csv every run and compared in run_log.md.
- `damage_behind_smoke` got a shooter-side clause (the crossed puff must be nearer the shooter than the target). Without it, RESIN battleship fire crossing the Conte Verde's exhaust trail next to its targets was credited as 47k "behind" that smoke.
- Decision: smoke-damage columns are filled in the table now (DESIGN lists them as Phase 2). They are labeled as spike results in run_log.md and M4_DAMAGE_SPIKE.md.

## Review (fresh subagent, M3 and M4 together) and fixes

Findings fixed before the final run:
- Damage ledger matching could fold two shells of one salvo seen by the same replay into one event; matching now only pairs an event with an earlier replay's event, so same-replay events never fold.
- Shot hits were collected again on every step where the merge skipped a secondary packet (the view's hit list is cleared only when a packet is processed); hits are now deduplicated by shooter, victim, clock and shot id. The attribution was unaffected, the hit count in the stats was inflated.
- A ship concealed by two overlapping smokes recorded a detection for each smoke but only the last one got its duration; both do now.
- Damage columns stay empty when a replay yields no damage events at all, instead of showing zero.
- Ships alive and enemy radars are empty (not zero) when the smoker's team is unknown.
- Puff life for the damage and overlap rules is now the observed value (last puff laid to the object's removal) when the removal was seen, and the base value otherwise. Builds lengthen puff life, and the base value would have ended credit 10 to 30 percent early.
- Header lines are measured with the font and cut with `..` when wider than the frame.
- `render.clip_fps` of 0 is rejected when the config is read instead of being silently raised to 1.
- A results row with no player name is skipped instead of becoming an empty name.
- A wrong field comment in the Tier 2 tracker.

Left as is: the 1.5 s matching window assumes the two replays' clocks are aligned, which the toolkit's own merge already assumes.
