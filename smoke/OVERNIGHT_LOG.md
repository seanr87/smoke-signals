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
