# First Claude Code prompt (milestone M1)

Before pasting:
1. Fork https://github.com/landaire/wows-toolkit and clone the fork; create a `smoke-signals` branch.
2. Copy this package's `smoke/` folder into the fork root.
3. Put the two Grand Final G1 replays (from `exploration/replays/`) in `replays/`.
4. Copy `smoke/config.example.toml` to `config.toml` at the repo root and set the paths.

Paste:

```
Read smoke/DESIGN.md and smoke/CLAUDE.md, then the fork's AGENTS.md. You're building Phase 1 of smoke_signals in this fork.

Start with milestone M1 only:
1. Install the pinned Rust toolchain if missing (ask first).
2. Move the game-data loader from crates/minimap-renderer/src/main.rs into a library module; keep minimap_renderer working.
3. Create crates/smoke-signals. Download game data for build 15.9.0_13357625 from landaire/wows-replay-data (only that build + referenced common/ objects) into the path in config.toml.
4. Render ONE merged frame of replays/ (H-SR primary, RESIN merged) at battle clock 13:46 and save it to output/<timestamp>/.

Use smoke/reference/smoke_probe.rs as a working example of the session loop and rendering, and exploration/NOTES.md (if copied in) for test findings. Then stop, show me the frame, and summarise what you changed and anything that surprised you. Don't start M2 until I say so.
```

Later milestones: "Go ahead with M2 per DESIGN.md; the golden test must pass before you stop." (then M3, M4).
