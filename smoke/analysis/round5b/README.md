# Round 5b: Round 5 redone on the batch with timelines

Analysis of the rerun batch. Nothing outside `smoke/analysis/round5b/` and `smoke/analysis/round3/common.py` (two lines, to
read a batch from another folder) was changed by the analysis step. `output/20261117-122135` and gh-pages are untouched.

- **Batch:** `output/20261117-230933` (smoke-signals 0.4.0, revision `a7129ffa`): 1,547 smokes, 171 games, 30 clans, plus
  the timeline files. Batch report: `smoke/STEP9-R5B-RERUN.md`. Data zip:
  https://github.com/seanr87/smoke-signals/releases/tag/data-r5b
- **Commit:** on branch `r5b`. Analysis content committed as 1ab27d1e; the zip and this line follow in the next commit.
- **Groups and rules:** as Round 5. Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS; Rest = the other 24 clans;
  team-normalized positions; minimum n 8 (8 to 14 small n); 95% intervals by resampling whole clans; association only.

## What is here

| File | What it is |
|---|---|
| `FINDINGS.md` | What changed from Round 5, the verdict table, every number that changed, then every item. Redone items come first in each part; the Round 5 text they replace is kept below, marked superseded. |
| `spots.json` | 45 records. The Round 5 spots rerun; the four Round 5 danger zones removed; five Round 5b danger-zone candidates listed as reference only. |
| `clan_styles.json` | As Round 5, rerun with the clock fix. |
| `ships.json` | The B tables rerun, plus `B3_per_shot` (Harugumo spotting per shot). |
| `CHECK.md` | Numbers traced to scripts, how Round 5 was re-established, and the main session's recheck. |
| `figures/` | Working figures (PNG + SVG), Round 5 ones regenerated plus `n1-` to `n4-` for the redone items. Reference only. |
| `new-n1` | C1 and C2 from the cap timeline; `enemy-took.csv` (one row per smoke); `caps.json`. |
| `new-n2` | Real health, C3 danger zones, A2 leaving the smoke and radar deaths; `deaths.json`, `danger-zones.json`. |
| `new-n3` | B3 Harugumo per shot and the Loop Daring test; `ships-and-loop.json`. |
| `new-n4` | The three page 1 claims re-tested; `page1.json`. |
| `part-a` ... `part-d` | The Round 5 scripts rerun on the new batch, with the Round 5 findings text. |
| `rerun/` | `same-definitions.txt` (Round 5 outputs reproduced before the clock fix) and `clock-fix-changes.md` (every output line the fix changed). |
| `r5lib.py`, `tl.py` | Round 5 library with the clock fix, and the timeline reader. `batch.json` names the batch. |
| `run_round5_scripts.sh`, `compare_with_round5.py`, `clock_fix_changes.py`, `assemble.py` | Rerun, compare and build. |
| `verify/` | Recheck scripts. |

## Definitions that changed or are new

- **Elapsed time:** seconds since battle start from the replay clock (`e0`, `e1` on every smoke), the same moment in both
  runs of a game to within 0.75 seconds. Round 5 used 20:00 minus the HUD clock, which was 300 seconds off in two games
  played on a 15-minute clock.
- **Enemy took the cap (timeline):** the nearest cap was not the enemy's at activation and its owner changed to the enemy
  while the smoke stood ("during") or within 60 seconds after it dispersed. Reported both ways. "We took" is the same test
  for our side. This replaces the Round 5 version built from cap owners at smoke moments.
- **Cap holder at exactly 8:00:** the owner at elapsed 480 seconds from the cap timeline, in the 166 games that reached it.
- **Deaths (tracks):** a ship is dead from the first 2-second sample at which its own team's replay shows it not alive.
  A covered ship counts for a smoke when it died between activation and 20 seconds after the smoke dispersed. This finds
  about twice as many smoking-destroyer deaths as the batch's `smoke_deaths` list, which only holds ships that died while
  concealed by the smoke or just after it cleared around them.
- **Hurt (real health):** died in that window, or lost a third or more of its real maximum health while covered. Replaces
  the Round 5 estimate of ship health.
- **Danger-zone baselines (like with like):** destroyer smoker 12.8 died and 23.1 died-or-hurt per 100 destroyer smokes;
  sheltering cruisers 9.6 and 19.4 per 100. Same flag rule as Round 5 (8+ smokes, clearly above the all-map and the
  same-map baseline), run two ways: placed at the smoke centre, and placed where the ship died or took its largest hit.
- **Left the smoke:** the ship's track moved outside the smoke radius of every puff while the smoke still stood.
- **Radar-lit:** the ship carried the radar detection flag (radar log). "Lit by" a radar ship is attributed by range and
  time; where more than one enemy radar had the ship in range the row is marked ambiguous.
- **Radar press from smoke:** a radar activation by a ship standing inside an allied smoke at that moment (radar log).
  Round 3 and 4 counted destroyer smokes whose primary purpose tag was a radar play.
- **Cap taken after an early smoke (page 1):** from the cap timeline, for the contested cap and for the nearest cap.
  The batch `cap_won` field credits any cap within gun range of a ship in the smoke, so it overstates smokes with a cruiser
  inside; it is no longer used for this claim.
- **Per shot (B3):** each damage event credited to the smoke with the smoker as attacker, placed at its firing time.
  Flood and "unknown" events are left out, which makes the event totals match the smoke records.

## Could not be done

- **Ribbons per smoke:** counted, but unusable as a measure. A replay holds ribbons for its recording player only (341 ships
  of 3,078), so 268 of 1,547 smokes covered a recording player at all. A Defended ribbon does not name its cap.
- **Who spotted a target:** still not recorded. The evidence is whether the target was detected, whether it was radar-lit and
  by whom, and which friendly ship was nearest, at each shot.
- **Top 6 against Rest on Loop Daring smokes:** 3 Top 6 smokes against 45.
- **Danger zones:** two thirds of areas have under 8 smokes and are not rated; none of the rated ones is kept.
- **The single-replay game** (KSC against -BN-, losers bracket round 1 game 3): the other team's health and detection are
  incomplete; its ship-smoke pairs are left out of the health work.
- **171 smokes** have no dispersal time (the replay ended first); their end is estimated from emission time and puff life.
- **Items not redone** (A1, A3, A4, B1, B2, B4, C4, most of C5, D) keep their Round 5 text. Their outputs were regenerated;
  what the clock fix moved in them is in `FINDINGS.md` section 3b and `rerun/clock-fix-changes.md`.

## Known quirks

- Ship lists with equal counts can come out in a different order from run to run (Python's set order). Counts are the same.
- `G[key]['len']` and `s['el']` are corrected for the two 15-minute games inside `load5()`; `round3/common.py` still has the
  old reading, so rounds 3 to 5 reproduce as published.
- PNG rendering through headless Edge failed now and then on this machine; scripts retry.
