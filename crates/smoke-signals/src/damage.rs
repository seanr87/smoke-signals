//! The M4 smoke-damage spike: attribute each damage event to its attacker's
//! firing position and time, then credit it to the smokes the attacker was
//! firing from or through.
//!
//! The replay's damage ledger already names the aggressor ship for every
//! damage event, so the open question is the firing moment and position.
//! Three sources are tried per event, best first: a resolved shot hit (same
//! attacker and victim, impact within a second of the damage), the attacker's
//! latest salvo before the damage, and the attacker's position at the damage
//! clock itself.

use std::collections::BTreeMap;
use std::collections::HashMap;

use serde::Serialize;
use wows_battle_world::scan::PositionTimeline;
use wows_replays::analyzer::battle_controller::DamageEvent;
use wows_replays::analyzer::battle_controller::state::ActiveShot;
use wows_replays::analyzer::battle_controller::state::ResolvedShotHit;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::game_types::VisibilityFlags;
use wowsunpack::game_types::WorldPos;

use crate::timeline;

/// Largest gap between a damage event and the shot hit it is matched to.
const HIT_MATCH_SECONDS: f32 = 1.0;
/// Longest shell flight accepted when matching a damage event to a salvo.
const SALVO_MATCH_SECONDS: f32 = 25.0;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum FireSource {
    /// A resolved shot hit gave the fire time and the shell's origin.
    ShotHit,
    /// The attacker's latest salvo before the damage gave both.
    Salvo,
    /// No shot data: the attacker's position at the damage clock.
    DamageClock,
}

/// One damage event with the attacker's firing moment and position.
#[derive(Debug, Clone, Serialize)]
pub struct AttributedDamage {
    pub attacker: u32,
    pub victim: u32,
    pub amount: f32,
    pub damage_seconds: f32,
    pub fire_seconds: f32,
    pub fire_source: FireSource,
    pub attacker_detected_at_fire: Option<bool>,
    /// Smokes the attacker stood in when firing.
    pub in_smokes: Vec<u32>,
    /// Smokes whose standing puffs the line of fire crossed, with the attacker
    /// outside them and undetected.
    pub behind_smokes: Vec<u32>,
}

/// A smoke as the spike needs it: puffs with the time they were laid, the
/// puff life, and the object's life.
pub struct SmokeGeometry {
    pub id: u32,
    pub radius: f32,
    pub puffs: Vec<(f32, WorldPos)>,
    pub puff_life: Option<f32>,
    pub created: f32,
    pub removed: Option<f32>,
}

impl SmokeGeometry {
    /// Puffs standing at `t`.
    fn standing(&self, t: f32) -> impl Iterator<Item = WorldPos> + '_ {
        let end = self.removed.unwrap_or(f32::INFINITY);
        self.puffs
            .iter()
            .filter(move |(laid, _)| *laid <= t && t <= end && self.puff_life.is_none_or(|life| t <= laid + life))
            .map(|(_, p)| *p)
    }

    fn contains(&self, t: f32, pos: WorldPos) -> bool {
        self.standing(t).any(|puff| timeline::ground_distance(pos, puff) <= self.radius)
    }

    /// The line from `from` to `to` passes through a standing puff that lies
    /// on the shooter's side (nearer `from` than `to`), so the smoke hides the
    /// shooter rather than merely standing near the target.
    fn crosses(&self, t: f32, from: WorldPos, to: WorldPos) -> bool {
        self.standing(t).any(|puff| {
            segment_distance_xz(from, to, puff) <= self.radius
                && timeline::ground_distance(from, puff) < timeline::ground_distance(to, puff)
        })
    }
}

/// Horizontal distance from `p` to the segment `a`-`b`.
fn segment_distance_xz(a: WorldPos, b: WorldPos, p: WorldPos) -> f32 {
    let (ax, az, bx, bz, px, pz) = (a.0.x, a.0.z, b.0.x, b.0.z, p.0.x, p.0.z);
    let (dx, dz) = (bx - ax, bz - az);
    let len2 = dx * dx + dz * dz;
    let t = if len2 <= 0.0 { 0.0 } else { (((px - ax) * dx + (pz - az) * dz) / len2).clamp(0.0, 1.0) };
    let (cx, cz) = (ax + dx * t, az + dz * t);
    ((px - cx).powi(2) + (pz - cz).powi(2)).sqrt()
}

/// Totals credited to one smoke, split by the shooter's relation to the
/// smoke's owner.
#[derive(Debug, Clone, Default, Serialize)]
pub struct SmokeDamage {
    pub damage_in_smoke_smoker: f32,
    pub damage_in_smoke_ally: f32,
    pub damage_in_smoke_enemy: f32,
    pub damage_behind_smoke_smoker: f32,
    pub damage_behind_smoke_ally: f32,
    pub damage_behind_smoke_enemy: f32,
    pub events_in_smoke: u32,
    pub events_behind_smoke: u32,
}

impl SmokeDamage {
    pub fn damage_in_smoke(&self) -> f32 {
        self.damage_in_smoke_smoker + self.damage_in_smoke_ally
    }

    pub fn damage_behind_smoke(&self) -> f32 {
        self.damage_behind_smoke_smoker + self.damage_behind_smoke_ally
    }

    pub fn smoke_damage_total(&self) -> f32 {
        self.damage_in_smoke() + self.damage_behind_smoke()
    }
}

/// Damage ledgers of every replay, primary first, each from its own parse.
pub fn ledgers_per_replay<G: wowsunpack::data::ResourceLoader>(
    game_resources: &G,
    constants: &wows_replays::game_constants::GameConstants,
    version: wowsunpack::data::Version,
    specs: &[wowsunpack::rpc::entitydefs::EntitySpec],
    replays: &[&wows_replays::ReplayFile],
) -> Vec<HashMap<EntityId, Vec<DamageEvent>>> {
    use wows_battle_world::BattleWorld;
    use wows_replays::analyzer::Analyzer;
    use wows_replays::packet2::Parser;

    replays
        .iter()
        .map(|replay| {
            let mut world = BattleWorld::new(&replay.meta, game_resources, Some(constants));
            let mut parser = Parser::with_version(specs, version);
            let mut remaining = replay.packet_data();
            while !remaining.is_empty() {
                let Ok(packet) = parser.parse_packet(&mut remaining) else { break };
                world.process(&packet);
            }
            world.finish();
            world.damage_ledger().clone()
        })
        .collect()
}

/// Largest clock difference between two perspectives' reports of one hit.
const DUPLICATE_WINDOW_SECONDS: f32 = 1.5;

/// Union of the per-replay ledgers. A client is told every hit on a ship
/// inside its area of interest, so perspectives overlap, and their clocks for
/// one hit differ by a fraction of a second. An event from a later replay is
/// matched one-to-one to an unmatched event of an earlier replay with the
/// same attacker, victim and amount within [`DUPLICATE_WINDOW_SECONDS`];
/// matched events are the same hit and are kept once. Several shells of one
/// salvo with equal damage each find their own match, so they survive.
/// Returns the ledger and how many events were folded as duplicates.
pub fn merge_ledgers(ledgers: &[HashMap<EntityId, Vec<DamageEvent>>]) -> (HashMap<EntityId, Vec<DamageEvent>>, u32) {
    let mut merged: HashMap<EntityId, Vec<(DamageEvent, bool)>> = HashMap::new();
    let mut folded = 0;
    for (index, ledger) in ledgers.iter().enumerate() {
        for (attacker, events) in ledger {
            let existing = merged.entry(*attacker).or_default();
            for event in events {
                if index > 0 {
                    let best = existing
                        .iter_mut()
                        .filter(|(e, matched)| {
                            !matched
                                && e.victim == event.victim
                                && e.amount == event.amount
                                && (e.clock.seconds() - event.clock.seconds()).abs() <= DUPLICATE_WINDOW_SECONDS
                        })
                        .min_by(|a, b| {
                            (a.0.clock.seconds() - event.clock.seconds())
                                .abs()
                                .total_cmp(&(b.0.clock.seconds() - event.clock.seconds()).abs())
                        });
                    if let Some(slot) = best {
                        slot.1 = true;
                        folded += 1;
                        continue;
                    }
                }
                existing.push((*event, false));
            }
        }
        // Matches are only against earlier replays; reset for the next one.
        for list in merged.values_mut() {
            for slot in list.iter_mut() {
                slot.1 = false;
            }
        }
    }
    let mut out: HashMap<EntityId, Vec<DamageEvent>> =
        merged.into_iter().map(|(k, v)| (k, v.into_iter().map(|(e, _)| e).collect())).collect();
    for events in out.values_mut() {
        events.sort_by(|a, b| a.clock.seconds().total_cmp(&b.clock.seconds()));
    }
    (out, folded)
}

/// Coverage of the attribution on this game.
#[derive(Debug, Clone, Default, Serialize)]
pub struct SpikeStats {
    pub events_per_replay: Vec<u32>,
    /// Events left out as another perspective's copy of a hit.
    pub events_dropped_as_duplicates: u32,
    pub damage_events: u32,
    pub damage_total: f32,
    /// Damage dealt per attacker entity, for checks against the game's totals.
    pub damage_by_attacker: BTreeMap<u32, f32>,
    /// The primary recorder's damage to enemies as the game's own stats report
    /// it, and as the merged ledger sums it, for a ground-truth check.
    pub self_damage_authoritative: Option<f32>,
    pub self_damage_ledger: Option<f32>,
    pub self_entity: Option<u32>,
    /// Damage per attacker entity as the game's end-of-battle results report
    /// it, when the replay carries them.
    pub damage_by_attacker_authoritative: BTreeMap<u32, f32>,
    pub events_attacker_unknown: u32,
    pub events_by_source: BTreeMap<String, u32>,
    pub damage_by_source: BTreeMap<String, f32>,
    pub events_no_attacker_position: u32,
    pub events_no_victim_position: u32,
    pub shot_hits: u32,
    pub salvos: u32,
}

pub struct SpikeInput<'a> {
    pub ledger: &'a HashMap<EntityId, Vec<DamageEvent>>,
    pub hits: &'a [ResolvedShotHit],
    pub salvos: &'a [ActiveShot],
    pub smokes: &'a [SmokeGeometry],
    pub timeline: &'a PositionTimeline,
    pub flags_at: &'a dyn Fn(EntityId, GameClock) -> Option<VisibilityFlags>,
    pub team_of: &'a dyn Fn(EntityId) -> Option<i64>,
    /// Owner entity and team of each smoke.
    pub smoke_owner: &'a HashMap<u32, (Option<EntityId>, Option<i64>)>,
}

pub struct SpikeOutput {
    pub events: Vec<AttributedDamage>,
    pub per_smoke: HashMap<u32, SmokeDamage>,
    pub stats: SpikeStats,
}

pub fn run(input: &SpikeInput<'_>) -> SpikeOutput {
    let mut events = Vec::new();
    let mut per_smoke: HashMap<u32, SmokeDamage> = HashMap::new();
    let mut stats =
        SpikeStats { shot_hits: input.hits.len() as u32, salvos: input.salvos.len() as u32, ..Default::default() };

    let mut salvos_by_owner: HashMap<EntityId, Vec<&ActiveShot>> = HashMap::new();
    for s in input.salvos {
        salvos_by_owner.entry(s.salvo.owner_id).or_default().push(s);
    }
    for v in salvos_by_owner.values_mut() {
        v.sort_by(|a, b| a.fired_at.seconds().total_cmp(&b.fired_at.seconds()));
    }

    for (attacker, list) in input.ledger {
        for event in list {
            stats.damage_events += 1;
            stats.damage_total += event.amount;
            *stats.damage_by_attacker.entry(attacker.raw() as u32).or_default() += event.amount;
            if (input.team_of)(*attacker).is_none() {
                stats.events_attacker_unknown += 1;
                continue;
            }
            let t = event.clock.seconds();

            // Fire moment and position, best source first.
            let from_hit = input
                .hits
                .iter()
                .filter(|h| {
                    h.hit.owner_id == *attacker
                        && h.victim_entity_id == event.victim
                        && (h.clock.seconds() - t).abs() <= HIT_MATCH_SECONDS
                })
                .find_map(|h| {
                    let fired = h.fired_at?;
                    let origin = h.salvo.as_ref()?.shots.first()?.origin;
                    Some((fired.seconds(), origin, FireSource::ShotHit))
                });
            let from_salvo = from_hit.or_else(|| {
                salvos_by_owner.get(attacker).and_then(|list| {
                    list.iter()
                        .rev()
                        .find(|s| {
                            let f = s.fired_at.seconds();
                            f <= t && t - f <= SALVO_MATCH_SECONDS
                        })
                        .and_then(|s| {
                            s.salvo.shots.first().map(|shot| (s.fired_at.seconds(), shot.origin, FireSource::Salvo))
                        })
                })
            });
            let (fire_seconds, fire_pos, source) = match from_salvo {
                Some(found) => found,
                None => {
                    let Some(pos) = input.timeline.get(attacker).and_then(|tr| timeline::world_pos_at(tr, event.clock))
                    else {
                        stats.events_no_attacker_position += 1;
                        continue;
                    };
                    (t, pos, FireSource::DamageClock)
                }
            };
            *stats.events_by_source.entry(format!("{source:?}")).or_default() += 1;
            *stats.damage_by_source.entry(format!("{source:?}")).or_default() += event.amount;

            let fire_clock = GameClock(fire_seconds);
            let victim_pos = input.timeline.get(&event.victim).and_then(|tr| timeline::world_pos_at(tr, event.clock));
            if victim_pos.is_none() {
                stats.events_no_victim_position += 1;
            }
            let detected = (input.flags_at)(*attacker, fire_clock).map(|f| f.is_detected());
            let attacker_team = (input.team_of)(*attacker);

            let in_smokes: Vec<u32> =
                input.smokes.iter().filter(|s| s.contains(fire_seconds, fire_pos)).map(|s| s.id).collect();
            let behind_smokes: Vec<u32> = match (victim_pos, detected) {
                (Some(target), Some(false)) => input
                    .smokes
                    .iter()
                    .filter(|s| !in_smokes.contains(&s.id) && s.crosses(fire_seconds, fire_pos, target))
                    .map(|s| s.id)
                    .collect(),
                _ => Vec::new(),
            };

            for id in &in_smokes {
                let d = per_smoke.entry(*id).or_default();
                d.events_in_smoke += 1;
                match role(*attacker, attacker_team, input.smoke_owner.get(id)) {
                    Role::Smoker => d.damage_in_smoke_smoker += event.amount,
                    Role::Ally => d.damage_in_smoke_ally += event.amount,
                    Role::Enemy => d.damage_in_smoke_enemy += event.amount,
                }
            }
            for id in &behind_smokes {
                let d = per_smoke.entry(*id).or_default();
                d.events_behind_smoke += 1;
                match role(*attacker, attacker_team, input.smoke_owner.get(id)) {
                    Role::Smoker => d.damage_behind_smoke_smoker += event.amount,
                    Role::Ally => d.damage_behind_smoke_ally += event.amount,
                    Role::Enemy => d.damage_behind_smoke_enemy += event.amount,
                }
            }

            events.push(AttributedDamage {
                attacker: attacker.raw() as u32,
                victim: event.victim.raw() as u32,
                amount: event.amount,
                damage_seconds: t,
                fire_seconds,
                fire_source: source,
                attacker_detected_at_fire: detected,
                in_smokes,
                behind_smokes,
            });
        }
    }
    events.sort_by(|a, b| a.damage_seconds.total_cmp(&b.damage_seconds));
    SpikeOutput { events, per_smoke, stats }
}

enum Role {
    Smoker,
    Ally,
    Enemy,
}

fn role(attacker: EntityId, attacker_team: Option<i64>, owner: Option<&(Option<EntityId>, Option<i64>)>) -> Role {
    match owner {
        Some((Some(smoker), _)) if *smoker == attacker => Role::Smoker,
        Some((_, Some(team))) if attacker_team == Some(*team) => Role::Ally,
        _ => Role::Enemy,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn segment_distance_handles_ends_and_middle() {
        let a = WorldPos::new(0.0, 0.0, 0.0);
        let b = WorldPos::new(10.0, 0.0, 0.0);
        assert_eq!(segment_distance_xz(a, b, WorldPos::new(5.0, 0.0, 3.0)), 3.0);
        assert_eq!(segment_distance_xz(a, b, WorldPos::new(-4.0, 0.0, 0.0)), 4.0);
        assert_eq!(segment_distance_xz(a, b, WorldPos::new(13.0, 0.0, 4.0)), 5.0);
    }

    #[test]
    fn standing_puffs_follow_lifetime_and_removal() {
        let smoke = SmokeGeometry {
            id: 1,
            radius: 15.0,
            puffs: vec![(10.0, WorldPos::new(0.0, 0.0, 0.0)), (20.0, WorldPos::new(100.0, 0.0, 0.0))],
            puff_life: Some(50.0),
            created: 10.0,
            removed: Some(65.0),
        };
        assert!(smoke.contains(15.0, WorldPos::new(5.0, 0.0, 0.0)));
        assert!(!smoke.contains(15.0, WorldPos::new(100.0, 0.0, 0.0)));
        assert!(smoke.contains(61.0, WorldPos::new(100.0, 0.0, 0.0)));
        assert!(!smoke.contains(61.0, WorldPos::new(0.0, 0.0, 0.0)));
        assert!(!smoke.contains(66.0, WorldPos::new(100.0, 0.0, 0.0)));
        assert!(!smoke.crosses(30.0, WorldPos::new(50.0, 0.0, -100.0), WorldPos::new(50.0, 0.0, 100.0)));
        // Puff at the shooter's end counts; the same puff at the target's end does not.
        assert!(smoke.crosses(30.0, WorldPos::new(0.0, 0.0, -20.0), WorldPos::new(0.0, 0.0, 500.0)));
        assert!(!smoke.crosses(30.0, WorldPos::new(0.0, 0.0, -500.0), WorldPos::new(0.0, 0.0, 20.0)));
    }
}
