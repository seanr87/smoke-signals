# Overnight log (3 Nov 2026): M3 and M4

Morning summary is added at the top when the run ends. Entries below are in order of work.

## M3 step 1: golden test fails without inputs

- Decision: the reference test now fails when config.toml or the replay and game data folders are missing, unless `SMOKE_SIGNALS_SKIP_GOLDEN=1` is set. The earlier `SMOKE_SIGNALS_REQUIRE_REFERENCE` switch is removed; one switch is enough.
