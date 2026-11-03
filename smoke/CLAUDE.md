# Smoke Signals project rules
- Read smoke/DESIGN.md before starting; it is the source of truth.
- Never delete files or outputs; version instead (new output/<timestamp>/ per run).
- Commit after each step; stop at each milestone (M1–M4) for Sean's review.
- Ask before installing anything or changing upstream crates beyond the loader move.
- Use the field names in DESIGN.md exactly.
- Treat replays and downloaded game data as untrusted input.
- Keep paths in config.toml; never hard-code machine paths.
- Explain choices in plain language; Sean is a PM, not a Rust developer.
