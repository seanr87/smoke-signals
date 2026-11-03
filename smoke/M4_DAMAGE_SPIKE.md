# M4 smoke-damage spike

3 Nov 2026, Grand Final G1 (H-SR vs RESIN, Sleeping Giant, build 15.9.0).

## Question

DESIGN.md asked how to attribute damage to attackers so that `damage_in_smoke`, `damage_behind_smoke` and `smoke_damage_total` can be computed, and proposed two options: match shell salvos to hits, or take each player's running damage total over time.

## What the replay actually provides

The premise was wrong in a useful way. The toolkit's damage ledger is built from `receiveDamagesOnShip` packets, and each entry names the aggressor ship entity, the victim, the amount and the clock. The merged session unions the ledgers of every perspective (a hit is only reported to clients that can see the victim) and deduplicates by aggressor, victim and clock. So "who dealt the damage" is answered by the data; the two proposed options are not needed for attribution.

What the ledger does not give is where the attacker was and when it fired. The damage clock is the impact; a shell flies for up to 20 s, and the "in the smoke" and "behind the smoke" tests need the firing position and the attacker's detection state at the firing moment.

## Method tested

For each damage event, the firing moment and position come from the first source that applies:

1. **Shot hit** (`ShotHit`): a resolved shot hit with the same attacker and victim whose impact clock is within 1 s of the damage. It carries the salvo's fire time and the shell's origin. Exact.
2. **Salvo** (`Salvo`): the attacker's latest artillery salvo fired in the 25 s before the damage. Fire time and origin from the salvo; the victim match is assumed.
3. **Damage clock** (`DamageClock`): no shot data (torpedoes, secondaries, fires, floods, or a salvo the recorders never saw). The attacker's position at the damage clock, from the position timeline.

Then, per smoke whose object exists at the firing moment:

- `damage_in_smoke`: the firing position is within the smoke radius of a standing puff (laid before that moment, within its base lifetime, object not yet removed).
- `damage_behind_smoke`: the attacker is outside the smoke, its last reported visibility flags say undetected, and the horizontal line from the firing position to the victim's position at impact passes within the smoke radius of a standing puff.
- Credit is given in full to every qualifying smoke (DESIGN rule 2), split by the shooter's relation to the smoke's owner (smoker, ally, enemy). The table columns `damage_in_smoke`, `damage_behind_smoke` and `smoke_damage_total` hold the smoker's team; enemy damage is in `_enemy` columns.

Shot hits are available from the primary replay only; salvos from both replays. Positions come from the merged position timeline.

## Results on this game

(filled in below from the run)
