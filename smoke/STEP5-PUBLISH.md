# STEP 5: published (morning report)

Published 16 Nov 2026, 23:11 EST, from batch `output/20261116-214739`; gh-pages commit cbeeb3e9 replaces the round 6 site. Code commits on `full-field`: e558208c (clan names, drift games, About line) and this report. Nothing merged to main.

## Live URLs

- Hub: https://seanr87.github.io/smoke-signals/
- Smoke Signals: https://seanr87.github.io/smoke-signals/smoke/index.html (Clans, Players, Smokes, Maps, Games, About under `smoke/`)
- Smoke of the Tournament: https://seanr87.github.io/smoke-signals/smoke/smokes/7934_g1_80503.html
- Round 6 site, unchanged: https://seanr87.github.io/smoke-signals/r6/
- Old root URLs redirect into `smoke/` (stubs for the root pages, `404.html` for deep links such as the old smoke pages).

## Verified live

Every checked page returned 200 with the same byte size as the local build: hub, Smoke Signals home, clans, games, maps, smokes, about, the Smoke of the Tournament page, `smoke/data/smokes.json`, a map path file, `r6/index.html`, a root stub and `404.html`. The gh-pages tree matches the local build file for file: 7,868 files, 589 MB on both sides, none missing, none differing. Of the 589 MB, 267 MB is the round 6 copy under `r6/` and 240 MB the 3,086 JPEG frames.

## What changed tonight

1. Clan full names: all 30 filled from the tournament API (`smoke/tools/clan_names.py`, 16 requests). None missing. They show on hover of every tag chip, on the clan page headers and in the group tables.
2. Drift games (PN vs HTDOG, BTLST vs MZY, MANBA vs KM) are back in awards and leaderboards. `smoke/data-quality.csv` now carries a note per game with `exclude=no`; each game page says "ledger about 1.1x the game's totals: the two replays' clocks drift within the game, so some hits are counted twice". The 25% ratio rule stays and flags no game in this build. The About page says so.
3. Hub: cards layout kept.
4. About page: "Award names are tongue-in-cheek; they describe a single smoke, not a player."
5. Rebuilt; `sanity.py` re-run on the batch (341 runs, 0 failures, 1,547 smokes, 103 owner-flagged, ledger median 0.997, no run above 1.25); headless screenshots of the hub, Smoke Signals home (with `--mute-audio` the videos no longer stall it), clans, games, maps, the H-SR clan page, the SCCC2 vs -BN- game page and the Smoke of the Tournament page, all rendered as intended.
6. Published with the round 6 site copied under `r6/`; nothing deleted (the local copy is `smoke-site-r6/`, ignored by git).

## Award changes

Re-including the three drift games changed no award: the winners of both lenses are the same as in the STEP 4 build. Against round 6 (the published scouting report):

| Award | Round 6 (3 clans) | Full field |
|---|---|---|
| Smoke of the Tournament | HSR_Yamiyonohik Somers, 90,686 | BN_jordi_92T Gearing, 97,327 (Group 3 R6 vs SCCC2) |
| Deepest Cap Smoke | RESIN_Fryce Somers (LB R6 vs BONKZ) | BONKZ_CheshireZ Gearing (WB R2 vs MZY g2) |
| Radar Bait | PN_Sean_O_Reill Harugumo (Group 1 R4 vs HTDOG) | RSR_Nick_Jacob Gearing (Group 1 R6 vs HTDOG) |
| Peekaboo | RESIN_Fryce Harugumo | RESIN_Fryce Harugumo, unchanged |
| Most Selfish Smoke | RESIN_Maddog242 Harugumo (WB R3 vs BONKZ) | KSC__Sait Gdansk (Group 1 R6 vs PFANS) |
| Golden Cloud, The Smokefather | HSR_Yamiyonohik | HSR_Yamiyonohik, 921,787 concealed over 50 smokes |
| Best in Haze (10 smokes) | HSR_Yamiyonohik | PFANS_Mugu_9, 26,747 per smoke over 12 |
| Most Selfish Smoker (5 smokes) | RESIN_eagle_lan | REEEE_Harmonieu (destroyer lens), VRTUS_AgentTang (all smokes) |

The four new single-smoke winners have clips rendered at the site's speed and bitrate (`output/20261116-225804`, assembled in `output/20261116-225332/site-clips`).

## Needs your decision or attention

- Nothing blocked. The two known limits stand as documented on the About page (torpedo ledger about 77% of the game's totals; airstrikes 44% classified).
- Clan scouting notes: the `note` column of `smoke/clans.csv` is empty; the Clans page shows a "Scouting notes" section only once a clan has text. Fill and rebuild when you like.
- The hub layout can still be switched (`--hub-layout hero` or `tournament`) with a rebuild and publish.
- Local preview for later checks: `python -m http.server 8765 --directory smoke-site` from the repository folder (file:// does not serve the JSON the Smokes and Maps pages fetch).
