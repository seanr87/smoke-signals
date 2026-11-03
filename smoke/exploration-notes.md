# Exploration notes (2 Nov 2026)

What was tried while designing the project, and what each finding means. Everything here is reference material; DESIGN.md is the source of truth.

## 1. Sources checked

- **Tournament site:** wows-tournaments.com/king-of-the-sea-xix/na/matches. Each match page links per-team replays at `/api/matches/report/replay?id=<n>` (e.g. match 7969: ids 18189 and 18193). The NA group stage has 21 matches in Group 1; H-SR and RESIN are in the playoffs.
- **wows-toolkit** (github.com/landaire/wows-toolkit, MIT, commit 9ab2388, 18 Oct 2026):
  - `minimap_renderer` CLI: `--dump-frame <N|mid|last>` (frame of a fixed 60 s / 30 fps timelapse, so about 0.67 s granularity on a 20-minute game), `--merge <replay>` (removes fog of war; auto team rosters), `--show-player-names`.
  - Smoke data: `SmokeScreenState { radius, position, points }`, with no owner and no per-puff timestamps.
  - Consumables: `view.active_consumables()` (activated_at), `view.consumable_inventories()` (icon_key, work_time).
  - Detection reasons: `visibilityFlags` bits BY_SHIP, BY_RLS (radar), BY_SONAR (hydro), IN_SMOKE (fired in smoke) and others.
  - Damage events: `DamageEvent { amount, victim, clock }`, with **no attacker** (a risk for smoke-damage metrics).
- **Game data:** github.com/landaire/wows-replay-data has dumped builds through 15.9.0_13357625 (9 Oct 2026). Both replays are 15.9.0_13357625, map 47_Sleeping_Giant. Fetched sparsely (one build plus its common/ objects, about 280 MB).
- **Penetration Nation site** (read-only look): Node/Express behind nginx on Ubuntu, role-based login (`/api/me`), and existing ToolKit Stats and Clan Battle upload pages. Hosting there needs the owner's permission.
- **Hosting research:** private GitHub Pages needs GitHub Enterprise Cloud. giscus comments need a public repo. The Supabase free tier (500 MB database, 1 GB storage, 5 GB egress, pauses after 7 idle days) would fit Phase 3.

## 2. Build (Linux cloud box)

- Built with the system stable Rust 1.97.0, using `RUSTUP_TOOLCHAIN=stable` because the box couldn't download through rustup.
- `cargo build --release -p wows_minimap_renderer --no-default-features --features bin,arc` took about 5 minutes on 2 cores.

## 3. Look check (`look_check/`)

- `no_merge_10-15.png`: H-SR perspective only, with stats panel.
- `merged_10-15.png`: H-SR plus RESIN merged; all ships shown, with team rosters.
- Finding: with merging, **detected ships get a yellow outline**, and undetected ships are drawn normally rather than faded.

## 4. Smoke probe (`scripts/make_probe.py` generates `smoke/reference/smoke_probe.rs`)

The probe replaces the CLI's render loop. On every replay step it tracks smoke objects and finds owners, and on each new H-SR puff it renders a frame with a yellow ring over that smoke. The last render per smoke is its capture frame.

- **v1** (`smoke_frames_first_pass/`, `data/all_smokes_probe_v1.csv`): owner = nearest activation in time and space. Wrong for some RESIN smokes, e.g. 39284 was a RESIN Harugumo smoke credited to H-SR's Harugumo.
- **v2–v4:** owner = nearest ship to the smoke origin. Some RESIN ships, including Fryce (the player whose replay was merged in), have **no position** in the merged view, which broke attribution for their smokes.
- **v5:** deploy end = last new puff before the first puff fades. This fixed Conte Verde, whose exhaust smoke keeps adding and removing puffs.
- **v6** (`data/all_smokes_probe_v6.csv`): adds the consumable icon_key and work_time.
- Note: `smoke_frames_final/06_..._ConteVerde_0807.png` uses the old rule (08:07, when the first puff faded). Under the exhaust rule, the capture should be at the end of emission, about 07:32.
- **Final H-SR result** (`smoke_frames_final/`, `data/hsr_smokes_gf_g1.csv`): 6 smokes. The rule is to accept the owner only when it is within 50 units of the origin and has an activation within 5 s.
- `data/puff_count_timeline.txt`: puff count per smoke over time (`PTS <smoke_id> <replay_s> <count>`).

## 5. GameParams (`data/gameparams_smoke_findings.txt`, `scripts/gp.py`)

| Ship | Variant | workTime | puff lifeTime | radius | speedLimit | charges / reload |
| --- | --- | --- | --- | --- | --- | --- |
| Harugumo (PJSD210) | Lvl_10_Gold | 20 s | 97 s | 15 | 12.5 | 3 / 160 s |
| Somers (PASD510) | US_Lvl_10_Gold | 30 s | 130 s | 15 | 12.5 | 3 / 160 s |
| Conte Verde (PISB720) | IT_Oil_Verde (title PCY014_SmokeGeneratorOil_Premium = exhaust) | 45 s | 10 s | 17 | 60 | 1 / 180 s |

- Every variant has consumableType `smokeGenerator`, so the type has to come from the variant name or title.
- Observed emission is longer than workTime (Harugumo 53 s, Somers 44 s). Sean confirmed that commander skills and upgrades explain this.

## 6. Replays (`replays/`)

King of the Sea XIX NA, Playoffs, Grand Final, GF Round 1, game 1: H-SR vs RESIN, 25 Oct 2026. Recorded by HSR_Arona_daisu (Moskva) and RESIN_Fryce (Somers).
