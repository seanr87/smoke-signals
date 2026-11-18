# Round 5: deeper analysis for the Smoke Atlas

Analysis only. Nothing outside `smoke/analysis/round5/` was changed, the batch was not rerun, and gh-pages was not touched.

- **Batch:** `output/20261117-122135`, the published batch (site build 17 Nov 2026): 1,547 smokes, 171 games, 30 clans.
- **Commit:** on branch `full-field`, without switching the checkout. Analysis content: see the hand-over message (the zip and this line follow in the next commit).
- **Groups:** Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS. Rest = the other 24 clans.
- **Rules used:** team-normalized positions; minimum n 8 (8 to 14 marked small n); 95% intervals by resampling whole clans;
  association only.

## What is here

| File | What it is |
|---|---|
| `FINDINGS.md` | Every item A1 to D3 in order: answer, numbers, Top 6 or Shared, clans, verdict. Starts with a one-page verdict table. |
| `spots.json` | 44 records: every spot, zone and cell, in the atlas's 0-1 minimap frame, with kind, mode, numbers, clan counts, cruisers, example links. |
| `clan_styles.json` | Per-clan values, percentiles and ranges for each dimension; the four styles; the two-scale structure. |
| `ships.json` | The B1 to B4 tables. |
| `CHECK.md` | Each number traced to its script and table, plus the main session's independent recheck. |
| `figures/` | 33 working figures (PNG + SVG). Reference only, not designed. |
| `part-a` ... `part-d` | Scripts, raw tables and the per-part findings the files above are built from. `part-c1/enemy-took.csv` has the new yes/no cap field for every smoke. `part-a/topics.json`, `part-c1/caps.json` and `part-c5/map-questions.json` hold the A, C1-C2 and C5 tables. |
| `r5lib.py` | Shared round 5 definitions (on top of `../round3/common.py`). |
| `assemble.py` | Builds the top-level files from the parts. |
| `verify/` | The main session's recheck scripts. |
| `maps/` | Minimap images the figures point to. |

## Definitions

- **Early cruiser smoke:** a destroyer smoke activated in the first 5 minutes that covers at least one cruiser, whatever the
  destroyer. "Inside" = a cruiser was inside the smoke. "Screened" = a cruiser was behind the smoke or firing through it, and
  none was inside. Both are always reported separately.
- **Cover groups (A1):** radar cruiser inside; non-radar cruiser inside (a cruiser inside and no radar ship inside, smoker
  included); no cruiser (none inside or screened); other (the remainder, shown as a footnote).
- **`cap_defended` (existing batch field), exactly:** the batch samples the game every 2 seconds. At any sample while the smoke
  stood, if any cap on the map was owned by the smoking team, had an enemy ship inside it, and lay on the middle line or on
  the enemy half, the field stores that cap's letter (the first one found). There is no distance test, so the cap is usually
  not near the smoke (median 8.9 km). It does not say the cap was kept, how long the enemy was in it, or that the smoke had
  anything to do with it. It never fires for a cap on the team's own half.
- **Enemy took the cap during the smoke (new):** for the cap nearest the smoke's centre: the cap was not the enemy's when the
  smoke was activated, and a cap-owner record taken while the smoke stood or within 60 seconds after it cleared shows the
  enemy owning it. "Not applicable" when the cap was already the enemy's. Cap owners are recorded only at the activation and
  capture moments of every smoke in the game, so this misses about 15% of real flips, and nearly half of the "yes" answers
  fall in the 60 seconds after the smoke cleared. Use it only for smokes inside or within 2 km of the cap. "Cap taken" is the
  same test for our side.
- **Cap holder at 8:00:** cap owners from the nearest smoke record within 60 seconds of 8:00 elapsed (154 of 171 games).
  Expected win rate comes from each clan's record with that game left out.
- **Deaths:** ships that died in or behind a smoke (batch field), including 27 that died just after it cleared.
- **Danger-zone baselines (like with like):** a destroyer dying or being hurt in its own smoke is compared with all destroyer
  smokes (6.4 died, 15.5 died or hurt per 100). A cruiser dying or being hurt while sheltering is compared with all sheltering
  cruisers (8.0 died, 22.0 died or hurt per 100). A zone is flagged only with 8+ smokes and a rate clearly above both the
  all-map and the same-map baseline.
- **Hurt:** died, or took damage worth a third or more of the ship's estimated health while covered. The batch has no ship
  health; the estimate is the lower quartile of total damage received by ships of that type that died. It is close for
  destroyers and roughly 10 to 20% high for ships that heal. Death-only figures are exact and shown beside it.
- **Enemy radar on a covered ship:** two readings. Strict = the batch logged a radar detection row (names the radar ship and
  distance). Broad = the ship's own detection list shows a radar flag. The strict field undercounts (120 against 297
  destroyer smokes); both are reported.
- **Top 6 spot / Shared spot:** Top 6 = the share of Top 6 smokes (of that kind on that map) in the spot is clearly higher
  than the Rest's share. Otherwise Shared, including where the Rest use it more. See "Top 6 or Shared: how to read it" in
  `FINDINGS.md` for why parts C4 and C5 differ.
- **0-1 minimap frame:** origin top-left, u to the right, v down, own spawn at the bottom (bottom-left on Okinawa). Same as
  the atlas package; the atlas map images fit without flipping.

## Could not be done

- **Ribbons:** replays carry defence and capture ribbons only for the player who recorded the replay (about 2 ships per
  game), the Smoke Signals code does not read them, and no batch file contains them. Counting them needs a code change and a
  batch rerun. Closest proxy: "enemy took the nearest cap".
- **Friendly radar outside smoke:** not exported. The Loop "Daring after a friendly radar" test uses a thin proxy and is not
  supported (1 of 48).
- **Spotting:** cannot be attributed. Proxy: nearest allied ship to the damaged enemy, at the one moment positions exist.
- **Leaving the smoke, death position, where ships were aiming:** not recorded. Proxies are named in A2 and A4.
- **"% of the smoke's life undetected":** not a batch field. B2 gives the batch's share of covered time plus a computed share
  of the smoke's whole life.
- **Too few smokes:** non-radar cruiser inside (17), flanking counter-smokes (12), Z-52 (10), Grozovoi Top 6 (6), most
  Top 6 cells on Okinawa, Loop F10 and Land of Fire's early A cluster for the Top 6.
- **Okinawa:** no spot of any kind with 8 smokes; one wide death zone.
- **Not rechecked or viewed:** see the end of the recheck section in `CHECK.md` (intervals, placebo runs, the grouping in D2,
  and 22 of the 33 figures).

## Known quirks

- One smoke has more cruiser deaths than sheltering cruisers counted (a cruiser firing through the smoke); capped in C3.
- Ship names in the batch contain non-breaking spaces; the library replaces them.
- The batch's `closing_m` is positive when the range opened.
- Sea of Fortune's west cluster is cap B in the team-normalized frame (the atlas label was right); smoke pages for north-spawn
  teams show the real letter A.
