# Round 5b findings: Round 5 redone on the batch with timelines

Batch: `output/20261117-230933` (smoke-signals 0.4.0, revision `a7129ffa`). Every existing smoke field is identical to the
Round 5 batch `output/20261117-122135`; what is new is the timeline files (cap ownership, radar and hydro log, ship tracks
with real health, score, cap ribbons). See `smoke/STEP9-R5B-RERUN.md`.

Same groups (Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS; Rest = everyone else), team-normalized positions, minimum n 8
(8 to 14 = small n), 95% intervals by resampling whole clans. Everything is association, not cause.

How this file is laid out:
1. What changed from Round 5, in short.
2. Verdicts at a glance, with a "changed?" column.
3. Every number that changed from Round 5, with old, new and the difference.
4. The items in Round 5 order. An item redone with the new data has its Round 5b text first; the Round 5 text it replaces
   is kept below it, marked "superseded", so nothing is lost.

## 1. What changed from Round 5, in short

**Reversed or dropped**

- **Danger zones (C3): dropped on every map.** With real health and death positions, the areas flagged are no more than
  shuffled outcomes give by luck. Round 5's one lead, destroyers smoking inside cap C on Hotspot, does not survive
  (27 per 100 against a map baseline of 18.7).
- **"Rest lose the nearby cap more often" (C1): no longer clear.** The snapshots had missed 27% of Top 6 cap flips against
  18% of Rest flips. On the timeline the gap for destroyer smokes within 2 km is -3.1 points (-11.0 to +4.5); it was -6.8
  and clear.
- **"A radar cruiser inside goes with the cap being taken, 58% against 14%" (page 1): does not hold.** The batch field
  behind it credits any cap within gun range of a ship in the smoke, which a cruiser inside inflates. On the cap timeline
  the same pair is 46% against 32% (contested cap) and 59% against 36% (nearest cap); neither is clear.
- **Loop, Daring after a friendly radar (C5): still dropped, for a better reason.** Round 5 could not see radar outside
  smoke (1 of 48 on a thin proxy). With the full radar log it is 17 of 48 (35%) against a chance level of 37%.

**Corrected**

- **Deaths in smoke were undercounted.** The batch list holds 69 smoking destroyers that died in their own smoke; ship
  tracks show 137 dead between activation and 20 seconds after the smoke dispersed. The list left out ships that had sailed
  out, were lit throughout, or died unseen. Like-with-like baselines move from 6.4 died and 15.5 died-or-hurt per 100
  destroyer smokes to 12.8 and 23.1; for sheltering cruisers from 8.0 and 22.0 to 9.6 and 19.4.
- **"Enemy took the cap" was undercounted.** 233 of 1,074 applicable smokes (21.7%), not 184 (17.1%). The snapshot version
  missed 21% of real flips, not the 15% estimated.
- **Radar is behind half of smoke deaths, not one in seven.** 65 of 124 deaths in destroyer smokes were radar-lit in the
  last 40 seconds (Round 5: 19 strict, 45 broad). The radar ship is nearly always a cruiser near maximum range (median
  9.3 km, 89% of its range; Moskva 24 of 64).
- **Two games ran on a 15-minute clock.** Elapsed times in rounds 3 to 5 were 300 seconds too high for their 17 smokes.
  Four destroyer smokes become "early". Fixed in the Round 5b library; section 3 lists what moved.
- **"Second destroyer recorded" (B3) was a snapshot artefact.** The Round 5 snapshot held only ships near the smoke. An
  allied destroyer is alive at 94% or more of these smokes for all three ships. The real difference is distance: one is
  within 5 km for 32% of a Harugumo smoke's life, against 14% (Somers) and 13% (Gearing).

**Confirmed with better data**

- **Early smoke is laid short of the cap.** Measured on ships, not the smoke outline: the smoker is a median 2.6 km outside
  the nearest cap edge when it presses smoke and the covered cruiser stays 3.2 km out.
- **Radar cruiser inside early smokes: Top 6 59% against 35%** (+24, +12 to +35; 60% against 35% before the clock fix).
  New: the cruiser ran radar from the smoke in only about a third of those, the same for both groups. The Top 6 difference
  is having the cruiser in the smoke, not pressing radar from it.
- **Radar from smoke: Top 6 about 2.5 times as often, same return per press.** Direct count from the radar log: 155 presses
  from inside an allied smoke, 0.77 against 0.30 per team-game (was 0.47 against 0.19 on the purpose tag).
- **Most "smoke deaths" happen outside the smoke.** Of 124, 29 died inside a standing smoke and 82 after sailing out. But
  leaving is not itself the risky moment: destroyers died at about 3 to 4 per 100 per 30 seconds inside, after leaving and
  after dispersal alike. Being 50+ behind raises all three.
- **Harugumo's targets are spotted by somebody else.** Per shot (410 shots, 44 smokes): the nearest friendly ship is a ship
  outside the smoke 45%, the Harugumo itself 31%, a second destroyer 24%, the radar cruiser inside 0.5%. Only 3% of its
  shots are at a target lit by a radar ship inside that smoke.
- **Cap holder at 8:00 (C2): same answer on 166 games** (was 154). No pooled row moved by more than 3 points.

**Not usable**

- **Ribbons per smoke.** Replays hold them for one ship per team. Only 268 of 1,547 smokes covered a recording player, and
  11 such smokes have a Defended ribbon on a cap the team owned. They do confirm the timeline: all 91 Captured ribbons sit
  on a recorded flip to that team, and all 284 Defended ribbons fall while an enemy stood in a cap.

## 2. Verdicts at a glance

| Item | Round 5 verdict | Round 5b | Changed? |
|---|---|---|---|
| A1 Cap-contest smokes by cover | Keep | Keep. Not redone; see the page 1 re-test for the cap link | Read with N4-2: the batch "cap won" field over-credits smokes with a cruiser inside |
| A2 Smoke deaths | Lead | Lead | Yes: track deaths, leaving the smoke, radar deaths all redone; baselines doubled for destroyers |
| A3 Somers vs Gearing deaths | Keep | Keep. Not redone | Clock fix only |
| A4 Counter-smokes | Keep; Drop flanking | Same. Not redone | Clock fix only |
| B1 Cap sitters | Keep | Same. Not redone | No |
| B2 Getaway smokes | Keep | Same. Not redone | No |
| B3 Long smokes | Lead | Keep for the Harugumo spotting part (redone per shot); rest as Round 5 | Yes: second-destroyer numbers replaced |
| B4 Hybrids | Keep Shimakaze; Drop Grozovoi | Same. Not redone | No |
| C1 Cap defence | Keep | Keep, timeline version replaces the snapshot version | Yes: counts up, the Top 6 gap no longer clear |
| C2 Cap holder at 8:00 | Keep as a caution | Same, on 166 games | Small moves only |
| C3 Danger zones | Lead for Hotspot C; Drop the rest | Drop on every map | Yes |
| C4 Spots per map | Keep as a catalogue | Same. Not redone | Clock fix only (early cruiser spots) |
| C5 Map questions | Per question | Same; Loop Daring test redone, still Drop | Loop test numbers replaced |
| D1 to D3 Clan styles | Keep / Lead / Keep | Same. Not redone | Clock fix only (first-smoke time, share after 12 minutes) |
| Page 1: early smoke short of the cap | (atlas) | Keep, Shared | Confirmed on ships |
| Page 1: radar cruiser inside early smokes | (atlas) | Keep, reword | 58% against 14% cap link withdrawn |
| Page 1: radar from smoke | (atlas) | Keep | Direct count replaces the tag count |
