# STEP 3: site plan for the full field (proposal, nothing built)

Input: batch `output/20261116-132014` after STEP 2b (1,547 smokes, 171 games, 30 clans, 9 one-sided smokes), maps `output/20261103-143026/maps`, clips `output/20261103-185636/site-clips` (round 6 award clips). Site builder `smoke/tools/build_site.py` (2,103 lines), publisher `smoke/tools/publish_site.py` to the gh-pages branch of seanr87/smoke-signals.

Today's site: 217 smokes, 301 pages, 258 MB, of which 230 MB is 868 frame images (4 per smoke) and 19 MB clips. The largest page is smokes.html at 1.3 MB.

## 0. Before the build: two data decisions

1. F1 from STEP 2b (perspective merge misses offsets over 6 s) changes a headline number. Without it INCA shows 89,671 concealed per game and its 94,628 smoke in the doubled KM game is a candidate for Smoke of the Tournament. Recommendation: apply F1 (one constant in damage.rs), re-run the three doubled games (six runs, about 2 minutes with frames), re-export, then build. If you prefer to build first, the site marks the three games "damage doubled, under review" and the awards exclude them.
2. F2 (drop the 600 m note when an activation confirms the owner) is cosmetic but the flag count shows on every smoke page and in the run log; with F2 the flagged share is about 7% instead of 21%. Recommendation: apply with F1.

Both are method edits and wait for your word.

## 1. Hub home page

One landing page with one card per analysis. Today: Smoke Signals (live, with its headline counts and a "open" link). Room for future analyses as more cards; no placeholder cards for things that do not exist.

Two layouts are possible:

- A. Hub at the root, Smoke Signals moves under `smoke/` (`smoke/index.html`, `smoke/clans.html`, ...). Clean for the long run; every current URL changes, so the old root pages become one-line redirect stubs to the new paths (the builder already writes stubs for awards.html and analysis.html).
- B. Hub takes `index.html`, the Smoke Signals briefing moves to `smoke-signals.html`, every other page stays where it is. No broken links, but future analyses would share the root with Smoke Signals' pages.

Recommendation: A, with redirect stubs kept for one or two publishes.

The hub card for Smoke Signals: title, one line of what it is, the counts (smokes, games, clans), the date of the batch, a thumbnail of the award smoke. The nav of every Smoke Signals page gets a "Hub" link on the left of the brand.

## 2. Clan identity and colours for 30 clans

- A clan registry file, `smoke/clans.csv`: tag, full name (from the tournament API, e.g. "[-BN-] Buenas Noches"), group, colour, and a short note field for your scouting text. The builder reads it; nothing about clans stays in code. Clans in the inventory with played games but missing from the file get a palette colour and a build warning.
- Colours: H-SR #F5C542, RESIN #5DADE2, PN #B388FF stay. The other 27 get fixed colours from a 27-entry palette (nine hues at three lightness levels), assigned once in the file so a clan keeps its colour across builds. 30 colours are never told apart on one chart, so no view shows 30 coloured series without labels: bars are always labelled with the tag, the Maps page draws one clan at a time by default (section 4), and the Smokes table shows the tag in a coloured chip.
- The tag chip (coloured pill with the tag) replaces the coloured dot everywhere; hovering it shows the full name.
- Pages that use the three original colours for non-clan meaning (the gold owner ring, the zone colours, the inside/behind bar, the nav brand) keep them; they are site colours, not clan colours. The clan colours move to CSS variables generated from the registry.

## 3. Clans page over all clans

- Top: a sortable table of the 30 clans, one row per clan, columns = every metric of the current lens plus games played and smokes; click a heading to sort (the Players leaderboard already has this JavaScript; reuse it). Rows with fewer than the minimum sample (section 6) are greyed with a "small sample" mark but stay sortable.
- The per-metric bar charts stay but show the top 12 of the sorted metric by default with a "show all 30" toggle, since 30 bars per chart times 18 charts is a wall. Bars labelled with the tag; best first; lower is better for smoke deaths.
- Clan cards: a grid of 30 tag chips linking to the clan pages; a card with scouting text only for clans that have text in the registry. The three original clans are not special anywhere.
- Clan pages: unchanged in content, generated for all 30. The "Top smokers" strip and the clan awards work as before; the clan awards obey the minimum sample.

## 4. Maps page with a clan filter and a readable default

1,547 lines over 8 maps (about 190 per map, Hotspot more) is not readable. Proposal per map:

- Default view: no lines; a density heatmap of smoke origins on the 10 x 10 grid (the clan page heatmap already exists), all clans, so the map says something at once.
- Picking a clan (or a ship, or a player) draws that selection's lines with the existing time slider, spawn, class and type filters. The clan filter lists only the clans with smokes on that map, with their counts. Several clans can be compared by picking "compare" and up to three clans (three colours stay readable); more than that goes back to the heatmap.
- The four side charts (smokes, average damage, average distance to the contested cap, selfish share) rank the clans shown; with "all" selected they show the top 10 by smokes on that map, with n, and the rest in a "others" row.
- Query strings keep working (`?clan=` draws that clan on every map).
- The lines of each map come from a small JSON per map fetched on demand, not inline SVG for all 1,547 paths, which keeps maps.html near its current size.

## 5. Games page: full bracket and all group games

- Playoffs: the bracket layout already has every slot (8-4-2-1 winners, 4-4-2-2-1-1 losers, final); with the full inventory every box is filled and the "Prototype: only series with H-SR or RESIN replays are linked" line goes. Every series page links every game.
- Groups: four group tables (one per group) with standings (wins, losses, games) computed from the inventory, then the game list filterable by clan (all 30) and map, every played game linked. Forfeits and byes shown greyed with their status.
- "Smokes analysed" now covers both teams. The column becomes two numbers in team order, "7 + 4", with the tag chips, on the games list, the series pages and the game page header. The game page already shows both rosters; the smokes section is split per team with the team's count in its heading.
- The one-sided game (LB R1 KSC vs -BN- G3) says "one replay (-BN-); KSC smokes inferred, no KSC damage" in its header and the four KSC smokes carry a "one-sided" pill.

## 6. Players and awards over the full field

About 150 smoking players instead of 21.

- Leaderboard: unchanged columns, plus a clan filter and a "minimum 5 smokes" toggle (on by default) so one-smoke players do not clutter it; the full list is one click away.
- Player pages for everyone; the damage-per-smoke chart keeps its top 12 bars.
- Minimum-sample rules, so a six-game clan or a three-smoke player does not top a board:

| award or board | rule today | proposed |
|---|---|---|
| Smoke of the Tournament, Deepest Cap Smoke, Radar Bait, Peekaboo, Most Selfish Smoke | single smoke, any | single smoke, from a two-replay game that is not under review (F1) |
| Golden Cloud (most total concealed) | any | any (volume award; note the games count on the card) |
| The Smokefather (most smokes) | any | any |
| Best in Haze (concealed per smoke) | minimum 5 smokes | minimum 10 smokes and 4 games |
| Most Selfish Smoker | any | minimum 5 smokes |
| Clan boards: smokes per game, concealed per game, selfish per game, and every per-game or share metric on the Clans page charts | 3 clans, no minimum | minimum 8 games (clans under 8: INCA 6, RMN 6, MANBA 6, OGF 6, BTLST 6, KM 5, MACH 7, NGA 7, PFANS 12 ok, SCCC2 7, RSR 7, UYSC 7, PN 7, BONKY 7, KSE 7); those stay in the tables, greyed, and cannot win a clan award |

8 games is the full group stage (7 rounds) plus one playoff game; it keeps the 15 clans that reached the playoffs or played a long group stage. If 8 is too strict, 7 keeps every clan that played the whole group stage and excludes only KM, INCA, RMN, MANBA, OGF and BTLST.

- Awards are recomputed by the builder over the full field; the five smoke awards each need a clip. The current clips are for round 6's winners; new winners need clips rendered (`batch --clips <ids>` or `analyze --only`), about a minute each. Expected movers on the present data: Smoke of the Tournament goes to BN_jordi_92T's 97,327 (SCCC2 game) unless the INCA 94,628 stands; Golden Cloud is open between HSR_Yamiyonohik and the -BN- and HFANS smokers; the rest need the build to tell.

## 7. Remove the hard-coded clan lists

`TEAMS` and the colour dictionary are used at lines 21, 116, 823, 884, 933, 937, 1043, 1238, 1309, 1322, 1377 and 1989 of build_site.py (Home stat tiles and briefing text, award clan rows, Clans index, Maps markers, legend and filter, Games filter, the JavaScript sort order on the Maps charts). Every use moves to `data.teams`, the clans with played games in the inventory, ordered by games played then tag, with colours from the registry (section 2). The Home briefing's "played by H-SR, RESIN and PN" becomes "played by 30 clans" computed. `--colors` stays as an override for one-off builds. The export tool already iterates the clans in the data.

## 8. Performance at the new scale

| item | today (217 smokes) | full field, as is | plan |
|---|---|---|---|
| frame images | 868 webp, 230 MB (4 per smoke, about 265 KB each) | 6,188 webp, 1.72 GB | ship 2 per smoke (capture frame and its zoom; the activation frames left the page in round 6) re-encoded to about 640 px, quality 75: about 100 KB each, about 310 MB. Measured on the build; target under 400 MB. GitHub Pages wants a site under 1 GB |
| smokes.html | 1.3 MB (every record and its thumbnail SVG inline) | about 9.5 MB | records move to `data/smokes.json` fetched on load; thumbnails drawn client-side from the record; the table renders 100 rows at a time as you scroll or page |
| maps.html | 219 KB | about 1.6 MB of inline paths | per-map path JSON fetched when a clan is picked (section 4) |
| index.html | 70 KB | similar | unchanged |
| smoke pages | 217 files, 2.8 MB | 1,547 files, about 20 MB | fine as static files |
| player pages | 21 | about 150 | fine |
| clips | 19 MB (10 award clips) | same count | re-render for new winners |
| build time | seconds | under a minute plus image re-encoding (about 10 minutes once; cached by mtime after that) | the builder skips images already copied |
| publish | one commit replacing gh-pages | 300 to 400 MB per publish | fine; the publisher force-replaces the branch |

Lazy loading: thumbnails and card images already carry `loading="lazy"`; the two frames on a smoke page stay eager. Nothing else grows with the field.

## 9. What stays the same

Smoke definitions, metrics, lenses, the smoke page layout, the classification block, the Smokees table, the game page content, the export schema (plus the `one_sided` column), the publish flow.

## 10. Order of work for STEP 4 (after approval)

1. F1 and F2 if approved; re-run the affected runs; re-export (own commit each).
2. Clan registry file and the builder changes of section 7 (one commit), then sections 2, 3, 5, 6 (one commit each), 4 and 8 (one commit each), 1 last since it moves paths.
3. Render clips for the new award winners.
4. Build, preview at localhost:8765, check every page type, publish, report totals and open issues.

## Open questions

1. Hub layout A (Smoke Signals under `smoke/`, redirects at the root) or B (hub replaces index.html only)?
2. Apply F1 and F2 before the build?
3. Minimum sample for clan boards: 8 games, or 7?
4. Frames: two per smoke, re-encoded, or keep all four at a larger site?
5. Compare mode on the Maps page (up to three clans) wanted, or one clan at a time?
