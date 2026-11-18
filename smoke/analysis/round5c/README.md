# Round 5c: the remaining Round 5 items on fixed definitions

Analysis only. No crate change, no batch rerun. Batch `output/20261117-230933` (smoke-signals 0.4.0). Written on branch
`r5b`. Package content committed as b6cc85fc; the zip and this line follow in the next commit.

## What is here

| File | What it is |
|---|---|
| `FINDINGS.md` | Verdict table first, then the package fixes, every number that changed from Round 5b (old and new), the eight items, and what stands from Round 5b. |
| `spots.json` | 45 records, each with `show`, `status` and `draw`. Three gold, six leads, eight hidden, one without rates. |
| `clan_styles.json` | Round 5b structure; "what it buys" now holds both death metrics and timeline cap scores. |
| `ships.json` | Round 5b tables plus `B2_5c`, `B3_5c` (both death metrics, undetected share from the track) and `map_cap_rows_5c` (item 7). |
| `CHECK.md` | Numbers traced to scripts, and the main session's recheck. |
| `x1-topics` | Items 1 to 4 (A1 to A4). |
| `x2-ships-maps` | Items 5 to 7 (B2, B3, map rows that quote a cap result). |
| `x3-clans` | Item 8 (D1 to D3). |
| `r5clib.py` | The definitions. `spots_5c.py`, `assemble_5c.py` build the package. `verify/` holds the recheck scripts. |

## Definitions

- **Died:** a covered ship (the smoker, or a ship the batch lists as inside or behind the smoke) whose death, from the exact
  death time in the game record, falls between activation and exactly 20 seconds after the smoke dispersed. Each dead ship is
  counted once, with the latest smoke that covered it, so totals are distinct ships. Round 5b used a window of 22 seconds
  (20 plus one 2-second track sample) and counted ship-smoke pairs: 137 smoking destroyers there, 136 distinct ships here.
- **Caught:** the batch `smoke_deaths` list: a ship the smoke concealed that was detected and sunk while concealed or just
  after the smoke cleared around it.
- **Exclusion:** the single-replay game (KSC against -BN-, losers bracket round 1 game 3). Its 9 smokes laid by the team
  with no replay are left out of every "died" rate; they stay in "caught", as the batch has them. 171 smokes have no
  dispersal time (the replay ended first); their end is activation plus emission time plus puff life.
- **Early:** replay clock under 300 seconds at activation (308 destroyer smokes).
- **Cap results:** from the cap timeline, on the contested cap and on the nearest cap, each fixed at activation; an owner
  change to that side between activation and 60 seconds after the smoke dispersed. Not applicable when the cap was already
  that side's.
- **Radar pressed from the smoke:** a ship of the smoking team pressed radar while standing in that smoke (radar log).
- **A covered ship radar-lit:** a covered ship carried the radar flag at some time while the smoke stood.

## Could not be done

See `FINDINGS.md` section 6. In short: radar pressed from the smoke is too rare to split by group (8 smokes); "lit at death
with no other detection" is an upper limit; flanking counter-smokes are too few; no figures this round.

## Known quirks

- `from r5clib import *` brings in `HERE` from `round3/common.py`. Two workers' first runs therefore wrote four JSON files
  into `smoke/analysis/round3/` (`out-a1.json` to `out-a4.json`). They are stray copies, left in place and not committed.
- "Still radar-lit at death" depends on the tolerance at the end of a lit span: 39 and 34 in the findings, 37 and 33 on the
  recheck's rule.
