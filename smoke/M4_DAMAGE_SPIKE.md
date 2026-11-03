# M4 smoke-damage spike

3 Nov 2026, Grand Final G1 (H-SR vs RESIN, Sleeping Giant, build 15.9.0). Run: `output/20261103-021955`.

## Question

DESIGN.md asked how to attribute damage to attackers so that `damage_in_smoke`, `damage_behind_smoke` and `smoke_damage_total` can be computed, and proposed two options: match shell salvos to hits, or take each player's running damage total over time.

## What the replay actually provides

The premise was wrong in a useful way. The toolkit's damage ledger is built from `receiveDamagesOnShip` packets, and each entry names the aggressor ship entity, the victim, the amount and the clock. So "who dealt the damage" is answered by the data; neither proposed option is needed for attribution.

Two things are not given and had to be solved:

1. **Which perspective to trust.** A client is told about hits on ships inside its area of interest, so the two replays overlap and each one also misses hits far from its recorder. The same hit appears in both replays with clocks that differ by a fraction of a second, so matching by exact clock (what the toolkit's renderer does for its roster totals) leaves duplicates in. Collapsing everything with the same attacker, victim and amount within 1.5 s goes too far the other way: several shells of one salvo legitimately deal the same damage within the same second. The rule used: events from the second replay are matched one to one with unmatched events of the first replay (same attacker, victim and amount, within 1.5 s); a matched pair is one hit, an unmatched event is kept.
2. **The firing moment and position.** The damage clock is the impact. A shell flies for up to 20 s, and the "in the smoke" and "behind the smoke" tests need the firing position and the attacker's detection state when it fired. Three sources, best first: a resolved shot hit (same attacker and victim, impact within 1 s of the damage: exact fire time and shell origin), the attacker's latest salvo in the 25 s before the damage (fire time and origin, victim assumed), or the attacker's position at the damage clock (torpedoes, secondaries, fires, floods, unseen salvos).

Then, per smoke whose object exists at the firing moment:

- `damage_in_smoke`: the firing position is within the smoke radius of a standing puff (laid before that moment, within its base lifetime, object not yet removed).
- `damage_behind_smoke`: the attacker is outside the smoke, its last reported visibility flags say undetected, the horizontal line from the firing position to the victim's position at impact passes within the smoke radius of a standing puff, and that puff is nearer the shooter than the target. The last clause is an addition to DESIGN.md: without it, long-range fire that merely crosses a smoke standing next to the target was credited (the Conte Verde's exhaust trail collected 47k of RESIN damage that way).
- Credit goes in full to every qualifying smoke (DESIGN rule 2), split by the shooter's relation to the smoke's owner. The table columns hold the smoker's team; enemy damage is in `_enemy` columns.

## Validation against the game's own numbers

The replay carries the end-of-battle results blob (`playersPublicInfo`), and the build's `constants.json` carries the field map (`CLIENT_PUBLIC_RESULTS_INDICES`), so every player's official `damage` total can be decoded. Smoke Signals writes it to `battle_results_players.csv` and compares it with the ledger in `run_log.md`:

| | game | ledger | ratio |
| --- | --- | --- | --- |
| all 18 players | 924,639 | 918,646 | 0.99 |
| primary recorder (Arona_daisu), also checked against the recorder's own authoritative stats | 34,902 | 34,450 | 0.99 |
| exact matches | Fryce, Klee_Fleein, PeytonThe | | 1.00 |
| largest deviations | Big_Boy69 1.15, Apex_captai 0.87, KamiSamur 0.86, Yuzuriha_Ma 0.90 | | |

Where the ledger is high (Big_Boy69, a Harugumo firing many equal HE shells), one hit was probably reported by both replays more than 1.5 s apart and kept twice. Where it is low (Apex_captai, a battleship firing at long range; KamiSamur), the victim was outside both recorders' area of interest at the impact, so neither replay recorded the hit. Both effects are a few percent of a player's total and well under the size of the smoke metrics.

Fire-moment sources on this game: shot hit 637 events, salvo 361, damage clock 25 (of 1,029 deduplicated events; 916 in the H-SR replay, 778 in the RESIN replay, 665 folded as the same hit).

## Results per smoke

| id | smoker | type | damage_in_smoke | damage_behind_smoke | total | in, enemy | behind, enemy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 39283 | YuriSayuki (Harugumo) | standard | 22,268 | 6,425 | 28,692 | 0 | 0 |
| 39284 | Big_Boy69 (Harugumo) | standard | 3,695 | 10,151 | 13,845 | 0 | 0 |
| 39285 | YuriSayuki | standard | 7,067 | 0 | 7,067 | 0 | 0 |
| 39286 | Big_Boy69 (flagged owner) | standard | 0 | 0 | 0 | 0 | 0 |
| 39287 | Fryce (Somers) | standard | 20,146 | 0 | 20,146 | 0 | 0 |
| 39288 | Yamiyonohik (Somers) | standard | 924 | 4,422 | 5,346 | 0 | 0 |
| 39289 | eagle_lan (Gdansk) | standard | 0 | 0 | 0 | 0 | 0 |
| 39290 | YuriSayuki | standard | 0 | 0 | 0 | 0 | 0 |
| 39291 | Fryce | standard | 22,895 | 0 | 22,895 | 3,684 | 3,696 |
| 39292 | Yamiyonohik | standard | 41,862 | 1,848 | 43,710 | 0 | 0 |
| 39293 | Apex_captai (Conte Verde) | exhaust | 1,650 | 0 | 1,650 | 0 | 0 |
| 39294 | eagle_lan | standard | 8,379 | 0 | 8,379 | 0 | 0 |
| 39295 | Fryce | standard | 0 | 0 | 0 | 0 | 0 |
| 39296 | Big_Boy69 | standard | 8,490 | 0 | 8,490 | 0 | 0 |

Reading: Yamiyonohik's second smoke (08:37) was the most productive of the game, 42k dealt from inside it, mostly by VoyagingSta's Des Moines, which stood in it (142 ally ship-seconds). Three smokes produced nothing: Big_Boy69's flagged 14:30 smoke, eagle_lan's first, and YuriSayuki's third (a 39 s pass through, 0 ship-seconds inside). The "behind" column is small everywhere; the one clear case is Big_Boy69's first smoke, which hid RESIN cruisers firing past it at 17:12.

## Recommendation for Phase 2

1. Use the damage ledger as the attacker source. Do not implement salvo-to-hit matching or running-total differencing for attribution; they are only needed for the firing moment, and the ledger already carries the attacker.
2. Keep the three-source firing-moment rule. Record the source per event (`fire_source` in `damage_events.csv`) so a summary can be restricted to shot-hit and salvo events when exactness matters.
3. Keep the one-to-one cross-perspective matching, and always run the game's `damage` totals as a check (`battle_results_players.csv` and the ratio table in `run_log.md`). Treat a player ratio outside 0.85 to 1.15 as a flag on that game.
4. Keep the shooter-side clause in `damage_behind_smoke`. It should be added to DESIGN.md's definition.
5. Known limits to state next to any smoke-damage number: hits on ships outside both recorders' area of interest are missing (a few percent on this game, more when only one replay exists); torpedo, fire and flood damage has no firing position and uses the damage clock; shot hits come from the primary replay only.
