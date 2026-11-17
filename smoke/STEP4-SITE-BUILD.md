# STEP 4: site built locally, not published

Date: 17 Nov 2026. Built from `output/20261116-214739` (P5 to P8, frames), maps `output/20261103-143026/maps`, clips `output/20261116-225332/site-clips`, per `smoke/STEP3-SITE-PLAN.md` and the decisions of 16 Nov 2026.

Commits: fb402b9d (clan registry), 39305177 (shrink-frames), 41a9213d (site builder), this report.

## Local preview

```
cd "C:\Users\soreill5\KOTS Analysis\wows-toolkit" && python -m http.server 8765 --directory smoke-site
```

Then http://localhost:8765/ (the hub) and http://localhost:8765/smoke/index.html (Smoke Signals). Opening the files directly (file://) does not work for the Smokes and Maps pages, which fetch JSON. The old round 6 site is kept at `smoke-site-r6/`.

Five pages to check first:

1. http://localhost:8765/ : the hub (layout `cards`; see "did not fit the plan").
2. http://localhost:8765/smoke/clans.html : 30 chips, the sortable table of every metric, the top-12 charts with the "show all" toggle, the small-sample greying.
3. http://localhost:8765/smoke/games.html : the full bracket, the four group tables, the "7 + 4" smokes column, the drift and one-sided pills.
4. http://localhost:8765/smoke/maps.html : the density view, then pick a clan (or `?clan=H-SR`) to draw paths; the top-10 side charts.
5. http://localhost:8765/smoke/smokes/7934_g1_80503.html : Smoke of the Tournament (BN_jordi_92T Gearing, 97,327 concealed) with its two JPEG frames and clip; its row in http://localhost:8765/smoke/smokes.html loads from JSON with lazy thumbnails.

Also worth a look: http://localhost:8765/smoke/about.html (method and Data limits), http://localhost:8765/smoke/players.html (clan filter, "at least 5 smokes" toggle), http://localhost:8765/smoke/games/8141_g3.html (the one-sided KSC vs -BN- game).

## Size and page weights

| Item | Size |
|---|---|
| Whole site (`smoke-site/`) | 322 MB, 6,674 files |
| Frames (`smoke/img`, 3,086 JPEG, two per smoke) | 240 MB |
| Clips (10 award clips) | 32 MB |
| Smoke pages (1,547) | 17 MB |
| Game pages (170) and series pages (36) | 12 MB |
| Data (`smokes.json` 1.3 MB, 7 map path files, 1,547 thumbnail SVGs, `smokes.csv`) | 11 MB |
| Player pages (218) | 8 MB |
| Clan pages (30) | 1.3 MB |

Round 6 site: 258 MB for 217 smokes. GitHub Pages' limit is 1 GB.

Largest five files are the award clips, 3.5 to 3.7 MB each. Largest five pages:

| Page | Weight |
|---|---|
| smoke/clans.html (every metric for every lens, inline) | 341 KB |
| smoke/players/HSR_Yamiyonohik_KOTS19NA.html (50 smoke cards with inline thumbnails) | 302 KB |
| smoke/maps.html (seven maps with the density layer; paths are fetched per map, 145 KB each) | 294 KB |
| smoke/games/8143_g1.html | 173 KB |
| smoke/players/BONKZ_Dyr3_KOTS19NA.html | 168 KB |

Main pages: hub 6 KB, smoke/index.html 68 KB, players.html 113 KB, games.html 67 KB, smokes.html 6 KB plus data/smokes.json 1.3 MB on load, about.html 8 KB, site.js 27 KB, style.css 14 KB. A smoke page is about 11 KB plus its two JPEG frames (about 80 KB together).

## Awards on the full field

| Award | Destroyer lens | All smokes |
|---|---|---|
| Smoke of the Tournament | BN_jordi_92T Gearing, 97,327 concealed (Group 3 R6 vs SCCC2) | same |
| Deepest Cap Smoke | BONKZ_CheshireZ Gearing (WB R2 vs MZY g2) | same |
| Radar Bait | RSR_Nick_Jacob Gearing (Group 1 R6 vs HTDOG) | same |
| Peekaboo | RESIN_Fryce Harugumo (Group 4 R1 vs BONKZ) | same |
| Most Selfish Smoke | KSC__Sait Gdansk (Group 1 R6 vs PFANS) | same |
| Golden Cloud | HSR_Yamiyonohik, 921,787 concealed over 50 smokes | same |
| The Smokefather | HSR_Yamiyonohik, 50 smokes in 18 games | same |
| Best in Haze (10 smokes) | PFANS_Mugu_9, 26,747 per smoke over 12 | same |
| Most Selfish Smoker (5 smokes) | REEEE_Harmonieu, 20 of 32 | VRTUS_AgentTang |

Four new clips were rendered (Smoke of the Tournament, Deepest Cap Smoke, Radar Bait, Most Selfish Smoke) at the site's speed and bitrate; Peekaboo keeps its round 6 clip. The single-smoke awards exclude the three drift games and the one-sided game; clan awards need 7 games.

## What was built

- Hub at the root from the mockup (`--hub-layout cards|hero|tournament`, templated from `smoke/mockups/`), Smoke Signals under `smoke/`. Every old root URL has a redirect stub and `404.html` sends any other old path under `smoke/`. Every Smoke Signals page has a Hub link left of the brand and an About link.
- Clan registry `smoke/clans.csv` (tag, name, group, colour, note) drives names and colours; H-SR, RESIN and PN keep theirs, the other 27 have fixed palette colours. Nothing about clans is in code; a clan missing from the file gets a build warning and a palette colour. Names and scouting notes are empty for now: fill the file and rebuild.
- Clans: chips with smokes and games, a sortable table of every metric for the chosen lens, charts showing the top 12 with a "show all 30" toggle, small-sample greying under 7 games, clan pages for all 30 (group and full name in the header).
- Players: 218 players, clan filter, "at least 5 smokes" toggle on by default (110 shown), awards with the minimum samples.
- Games: the full double-elimination bracket from the inventory, four group tables with standings (forfeits counted and marked), the games list and series pages with the "ours + theirs" smokes column and tag chips, drift and one-sided pills, per-team smoke sections on the game pages with the one-sided note.
- Maps: density heatmap of smoke origins over all clans by default; picking a clan, player or ship fetches that map's paths (`data/maps/m<n>.json`) and draws them with the time, spawn, class and type filters; side charts show the top 10 clans and "others"; `?clan=` and the smoke pages' "its path on the map" link still work. Compare mode stays on the backlog.
- Smokes: the table loads `data/smokes.json` (1.3 MB) and renders 100 rows at a time with a "show more" button; thumbnails are standalone SVG files loaded lazily; one-sided and drift smokes are marked.
- Frames: two per smoke (capture and its zoom), written by the new `smoke_signals shrink-frames` subcommand as JPEG at 840 and 540 px wide, quality 82 (`output/<batch>/frames-small/`); the full-size frames stay local.
- About page with the method in brief, the Data limits section (torpedo ledger about 77%, airstrikes partly classified, the three drift games, the one-sided game, coverage, owner flags), key terms and the clan metric definitions.
- Data quality: `smoke/data-quality.csv` lists the three drift games by hand with the reason; the 25% ratio rule stays in force on top.

## What did not fit the plan

- Hub layout: the decision line listed all three mockups, so the hub is built from `hub-1-cards` and the layout is a one-line switch (`--hub-layout hero` or `tournament` rebuilds the root page only). Say which one and I rebuild before publishing.
- Frames are JPEG, not WebP: the Rust image crate's WebP encoder is lossless only and no lossy encoder is installed, so the shrunk WebP came to 574 MB; JPEG at quality 82 is 240 MB for 3,086 frames. The frames are rendered minimaps and read well at this quality.
- The three drift games (PN vs HTDOG, BTLST vs MZY, MANBA vs KM) now sit at 1.10 to 1.16 of the game's totals after P5 to P8, under the 1.25 ratio rule, so they are listed by hand in `smoke/data-quality.csv` to keep them excluded as decided. The rule itself flags no other game.
- Clan full names are not in the registry yet (the tournament API names were not fetched); chips and headers show the tag until the file is filled.
- The builder changes went in as one commit rather than one per plan section; the sections are listed above.
- One game (171 played, 170 with a smoke) has no smoke and no page: 7898 g1 (its row on the Games page says "no smokes").
- Lossless activation frames and the four activation/capture images of the old site are gone from the site; smoke pages show the capture frame and its zoom only.

Nothing is published. `smoke/tools/publish_site.py` pushes `smoke-site/` to gh-pages when you say so.
