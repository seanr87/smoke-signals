//! Smoke damage credit: attribute each damage event to its attacker's firing
//! position and time, classify it by weapon, and credit it to one smoke (or a
//! split among the smokes that hid the shooter).
//!
//! The replay's damage ledger names the aggressor ship and the amount for
//! every damage event but not the weapon, so the firing moment and the kind
//! are both inferred. Three sources are tried for the moment, best first: a
//! resolved shot hit (same attacker and victim, impact within a second of the
//! damage), the attacker's latest salvo before the damage, and the attacker's
//! position at the damage clock itself.
//!
//! Credit rules (decided 3 Nov 2026):
//! - Only main-gun shells and the fires they start count. Torpedoes, floods
//!   and damage of unknown kind are classified and reported but never
//!   credited.
//! - A shot fired from inside a smoke credits that smoke alone; inside two
//!   overlapping smokes, the first-laid one whose puffs still hide the
//!   shooter.
//! - A shot fired from outside any smoke by an undetected shooter credits the
//!   smokes that were needed: those whose puffs blocked the view from at
//!   least one enemy within the shooter's detection range. Equal shares.
//! - A fire tick is credited like the shell that started it: the shooter's
//!   nearest earlier shell hit on the same target.

use std::cmp::Ordering;
use std::collections::BTreeMap;
use std::collections::BTreeSet;
use std::collections::HashMap;

use serde::Serialize;
use wows_battle_world::scan::PositionTimeline;
use wows_replays::analyzer::battle_controller::DamageEvent;
use wows_replays::analyzer::battle_controller::state::ActiveShot;
use wows_replays::analyzer::battle_controller::state::ActiveTorpedo;
use wows_replays::analyzer::battle_controller::state::ResolvedShotHit;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wows_replays::types::GameParamId;
use wowsunpack::game_types::VisibilityFlags;
use wowsunpack::game_types::WorldPos;

use crate::records::Xz;
use crate::timeline;

/// Largest gap between a damage event and the shot hit it is matched to.
const HIT_MATCH_SECONDS: f32 = 1.0;
/// Longest shell flight accepted when matching a damage event to a salvo.
const SALVO_MATCH_SECONDS: f32 = 25.0;
/// Fire clocks closer than this count as the same moment.
const SAME_FIRE_SECONDS: f32 = 0.01;
/// Aim points closer than this to each other count as the same landing point.
const SAME_TARGET_UNITS: f32 = 1.0;
/// Landing clocks closer than this to each other count as the same moment.
const SAME_LANDING_SECONDS: f32 = 0.1;
/// Fire and flood damage arrive as equal amounts about a second apart; a
/// neighbour of the same amount this far away marks a tick. Shells of one
/// salvo land within a fraction of a second, below the lower bound.
const TICK_GAP_MIN_SECONDS: f32 = 0.7;
const TICK_GAP_MAX_SECONDS: f32 = 1.4;
/// A fire tick is linked to the shooter's latest shell hit on the same target
/// within this long before it.
const FIRE_LINK_SECONDS: f32 = 75.0;
/// A torpedo launched this long before the damage, at most, can be its cause.
const TORPEDO_MAX_RUN_SECONDS: f32 = 150.0;
/// Farthest the torpedo's dead-reckoned track may pass from the victim, in
/// meters. The view keeps a torpedo to the end of the replay, so its
/// disappearance cannot mark the hit.
const TORPEDO_HIT_TOLERANCE_M: f32 = 400.0;
/// The track may pass the victim this long before or after the damage
/// clock: the victim's position is a held sample when the ship is not
/// spotted, and the hit is reported late.
const TORPEDO_PASS_WINDOW_SECONDS: f32 = 12.0;
/// Step of the pass search along the track.
const TORPEDO_PASS_STEP_SECONDS: f32 = 0.25;
/// A torpedo tick carries at least this much damage, unless it sinks the
/// victim: no torpedo in the field has an alpha under 10,000.
const TORPEDO_MIN_DAMAGE: f32 = 3000.0;
/// A hit this close to the victim's death clock is a finishing hit.
const FINISHING_HIT_SECONDS: f32 = 1.0;
/// Detection range used for the line-of-sight test when a ship's build gives none.
const DEFAULT_DETECTION_M: f32 = 12_000.0;

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

/// What dealt the damage, inferred from the ledger's timing.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DamageKind {
    /// A main-gun shell matched to a hit or a salvo.
    Shell,
    /// A secondary-battery shell: its salvo's projectile is not one the
    /// ship's main battery fires.
    Secondary,
    /// A fire tick linked to the shooter's earlier shell on the same target.
    Fire,
    /// A hit that fits a torpedo the attacker launched.
    Torpedo,
    /// A tick train that follows a torpedo hit.
    Flood,
    /// Nothing recorded explains it.
    Unknown,
}

impl DamageKind {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Shell => "shell",
            Self::Secondary => "secondary",
            Self::Fire => "fire",
            Self::Torpedo => "torpedo",
            Self::Flood => "flood",
            Self::Unknown => "unknown",
        }
    }

    /// Only shells and the fires they start earn smoke credit.
    pub fn credited(self) -> bool {
        matches!(self, Self::Shell | Self::Fire)
    }
}

/// One damage event with the attacker's firing moment and position.
#[derive(Debug, Clone, Serialize)]
pub struct AttributedDamage {
    pub attacker: u32,
    pub victim: u32,
    pub amount: f32,
    pub kind: DamageKind,
    pub damage_seconds: f32,
    pub fire_seconds: f32,
    pub fire_source: FireSource,
    pub attacker_detected_at_fire: Option<bool>,
    /// Why the attacker was spotted when it fired, when it was.
    pub detected_reason: Option<String>,
    /// Smokes the attacker stood in when firing.
    pub in_smokes: Vec<u32>,
    /// Smokes that hid the attacker from an enemy in detection range, with the
    /// attacker outside them and undetected.
    pub behind_smokes: Vec<u32>,
    /// The smokes credited with this event and each one's share.
    pub credited: Vec<(u32, f32)>,
    pub fire_xz: Option<Xz>,
    pub victim_xz: Option<Xz>,
}

/// A smoke as the spike needs it: puffs with the time they were laid, the
/// puff life (observed from the last puff to the object's removal when the
/// removal was seen, else the base value), and the object's life.
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

/// One shooter-to-target line for the smoke diagram: credited damage and the
/// mean positions of both ends.
#[derive(Debug, Clone, Default, Serialize)]
pub struct Arrow {
    pub attacker: u32,
    pub victim: u32,
    pub attacker_ally: bool,
    pub damage: f32,
    pub from: Xz,
    pub to: Xz,
    #[serde(skip)]
    samples: u32,
}

/// Damage by whether the shooter was detected when it fired, with the
/// detected part by reason.
#[derive(Debug, Clone, Default, Serialize)]
pub struct Split {
    pub concealed: f32,
    pub detected: f32,
    pub unknown: f32,
    pub by_reason: BTreeMap<String, f32>,
}

impl Split {
    fn add(&mut self, event: &AttributedDamage, amount: f32) {
        match event.attacker_detected_at_fire {
            Some(false) => self.concealed += amount,
            Some(true) => {
                self.detected += amount;
                let reason = event.detected_reason.clone().unwrap_or_else(|| "other".to_string());
                *self.by_reason.entry(reason).or_default() += amount;
            }
            None => self.unknown += amount,
        }
    }

    pub fn to_record(&self) -> crate::records::DamageSplit {
        crate::records::DamageSplit {
            concealed: self.concealed,
            detected: self.detected,
            unknown: self.unknown,
            detected_by: self.by_reason.iter().map(|(r, d)| crate::records::ReasonDamage { reason: r.clone(), damage: *d }).collect(),
        }
    }
}

/// Credited damage, salvos and kills of one shooter of the smoker's team.
#[derive(Debug, Clone, Default, Serialize)]
pub struct ShooterStat {
    pub damage: f32,
    pub split: Split,
    pub salvos: u32,
    pub kills: u32,
}

/// Credited damage on one enemy ship and whether the smoke's shots sank it.
#[derive(Debug, Clone, Default, Serialize)]
pub struct TargetStat {
    pub damage: f32,
    pub split: Split,
    pub sunk: bool,
}

/// Totals credited to one smoke, split by the shooter's relation to the
/// smoke's owner. `in_smoke` is credit for shots fired from inside; `behind`
/// is the shooter's share for shots fired from outside with this smoke
/// needed to hide it.
#[derive(Debug, Clone, Default, Serialize)]
pub struct SmokeDamage {
    pub damage_in_smoke_smoker: f32,
    pub damage_in_smoke_ally: f32,
    pub damage_in_smoke_enemy: f32,
    pub damage_behind_smoke_smoker: f32,
    pub damage_behind_smoke_ally: f32,
    pub damage_behind_smoke_enemy: f32,
    /// Credited shell and fire damage of the smoker's team.
    pub damage_shell: f32,
    pub damage_fire: f32,
    /// The smoker's team's credit by the shooter's detection when firing.
    pub split: Split,
    pub events_in_smoke: u32,
    pub events_behind_smoke: u32,
    /// Distinct firing moments of the smoker's team credited to this smoke.
    pub salvos: u32,
    /// Attackers of the smoker's team credited with damage through this smoke.
    pub shooters: BTreeSet<u32>,
    /// Shooter-to-target lines for the diagram, by attacker and victim.
    pub arrows: Vec<Arrow>,
    /// Per shooter of the smoker's team.
    pub shooter_stats: BTreeMap<u32, ShooterStat>,
    /// Per enemy ship hit by the smoker's team.
    pub targets: BTreeMap<u32, TargetStat>,
    /// Enemy ships whose last damage before sinking was credited here.
    pub kills: BTreeSet<u32>,
    #[serde(skip)]
    salvo_keys: BTreeSet<(u32, u32)>,
    #[serde(skip)]
    arrow_index: BTreeMap<(u32, u32), usize>,
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

    fn credit(&mut self, event: &AttributedDamage, share: f32, role: Role, inside: bool) {
        let amount = event.amount * share;
        match (inside, role) {
            (true, Role::Smoker) => self.damage_in_smoke_smoker += amount,
            (true, Role::Ally) => self.damage_in_smoke_ally += amount,
            (true, Role::Enemy) => self.damage_in_smoke_enemy += amount,
            (false, Role::Smoker) => self.damage_behind_smoke_smoker += amount,
            (false, Role::Ally) => self.damage_behind_smoke_ally += amount,
            (false, Role::Enemy) => self.damage_behind_smoke_enemy += amount,
        }
        if inside {
            self.events_in_smoke += 1;
        } else {
            self.events_behind_smoke += 1;
        }
        let ally = !matches!(role, Role::Enemy);
        if ally {
            match event.kind {
                DamageKind::Fire => self.damage_fire += amount,
                _ => self.damage_shell += amount,
            }
            self.split.add(event, amount);
            self.shooters.insert(event.attacker);
            let shooter = self.shooter_stats.entry(event.attacker).or_default();
            shooter.damage += amount;
            shooter.split.add(event, amount);
            if event.kind == DamageKind::Shell && self.salvo_keys.insert((event.attacker, event.fire_seconds.to_bits())) {
                self.salvos += 1;
                shooter.salvos += 1;
            }
            let target = self.targets.entry(event.victim).or_default();
            target.damage += amount;
            target.split.add(event, amount);
        }
        if let (Some(from), Some(to)) = (event.fire_xz, event.victim_xz) {
            let key = (event.attacker, event.victim);
            let index = match self.arrow_index.get(&key) {
                Some(i) => *i,
                None => {
                    self.arrows.push(Arrow { attacker: event.attacker, victim: event.victim, attacker_ally: ally, ..Default::default() });
                    self.arrow_index.insert(key, self.arrows.len() - 1);
                    self.arrows.len() - 1
                }
            };
            let a = &mut self.arrows[index];
            let n = a.samples as f32;
            a.from = Xz { x: (a.from.x * n + from.x) / (n + 1.0), z: (a.from.z * n + from.z) / (n + 1.0) };
            a.to = Xz { x: (a.to.x * n + to.x) / (n + 1.0), z: (a.to.z * n + to.z) / (n + 1.0) };
            a.samples += 1;
            a.damage += amount;
        }
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

/// Largest clock difference between two perspectives' reports of one hit,
/// once the perspectives' clock offset is taken out.
const DUPLICATE_WINDOW_SECONDS: f32 = 0.8;
/// Largest offset between two perspectives' clocks that is searched for.
const PERSPECTIVE_OFFSET_MAX_SECONDS: f32 = 12.0;
/// Offsets beyond this are accepted only when their bin holds at least
/// [`FAR_OFFSET_MIN_RATIO`] times the pairs of the best nearer bin.
const PERSPECTIVE_OFFSET_NEAR_SECONDS: f32 = 6.0;
const FAR_OFFSET_MIN_RATIO: f32 = 2.0;
/// Match window at offset zero when no offset estimate is trusted.
const FALLBACK_WINDOW_SECONDS: f32 = 3.0;
/// Candidate pairs needed before the median offset is trusted.
const OFFSET_MIN_PAIRS: usize = 10;

/// Clock offset estimated for one merged replay against the earlier ones.
#[derive(Debug, Clone, Copy, Default, Serialize)]
pub struct PerspectiveOffset {
    pub offset_s: f32,
    /// Candidate pairs in the chosen bin.
    pub pairs_in_bin: u32,
    /// Candidate pairs over the whole search range.
    pub pairs: u32,
    /// False when the fallback window at offset zero was used.
    pub trusted: bool,
}

/// Union of the per-replay ledgers. A client is told every hit on a ship
/// inside its area of interest, so perspectives overlap, and their clocks for
/// one hit differ by an offset that is close to constant within a game (about
/// 1 to 2 s) but differs between games. For each later replay the offset to
/// the earlier ones is the median clock difference over candidate pairs with
/// the same attacker, victim and amount; an event is then matched one-to-one
/// to an earlier event within [`DUPLICATE_WINDOW_SECONDS`] of that offset, and
/// a matched pair is one hit kept once. Events of the same replay never match
/// each other, so several shells of one salvo with equal damage survive.
/// An offset beyond [`PERSPECTIVE_OFFSET_NEAR_SECONDS`] wins only when its
/// bin clearly outweighs the best nearer bin, so a chance alignment of
/// repeated equal hits cannot pull the estimate away from a real near peak.
/// Returns the ledger, the fold count and the offset estimate per later replay.
pub fn merge_ledgers(
    ledgers: &[HashMap<EntityId, Vec<DamageEvent>>],
) -> (HashMap<EntityId, Vec<DamageEvent>>, u32, Vec<PerspectiveOffset>) {
    // (event, source replay, taken by a later replay's copy)
    let mut merged: HashMap<EntityId, Vec<(DamageEvent, usize, bool)>> = HashMap::new();
    let mut folded = 0;
    let mut offsets = Vec::new();
    for (index, ledger) in ledgers.iter().enumerate() {
        // Clock offset of this replay against the earlier ones: the most
        // common clock difference over candidate pairs, counted in quarter
        // second bins. Fire and flood ticks are left out of the estimate:
        // equal amounts a second apart would otherwise vote for every
        // multiple of a second.
        let mut bins: HashMap<i32, usize> = HashMap::new();
        let mut pairs = 0usize;
        for (attacker, events) in ledger {
            let Some(existing) = merged.get(attacker) else { continue };
            for (i, event) in events.iter().enumerate() {
                if in_tick_train(events, i) {
                    continue;
                }
                for (e, source, _) in existing {
                    if *source < index && e.victim == event.victim && e.amount == event.amount {
                        let d = event.clock.seconds() - e.clock.seconds();
                        if d.abs() <= PERSPECTIVE_OFFSET_MAX_SECONDS {
                            *bins.entry((d * 4.0).round() as i32).or_default() += 1;
                            pairs += 1;
                        }
                    }
                }
            }
        }
        let best_bin = |near_only: bool| {
            bins.iter()
                .filter(|(bin, _)| !near_only || (**bin as f32 / 4.0).abs() <= PERSPECTIVE_OFFSET_NEAR_SECONDS)
                .max_by_key(|(bin, n)| (**n, std::cmp::Reverse(bin.abs())))
                .map(|(bin, n)| (*bin as f32 / 4.0, *n))
        };
        let peak = match (best_bin(false), best_bin(true)) {
            (Some((far, n_far)), Some((near, n_near))) if far.abs() > PERSPECTIVE_OFFSET_NEAR_SECONDS => {
                if n_far as f32 >= FAR_OFFSET_MIN_RATIO * n_near as f32 {
                    Some((far, n_far))
                } else {
                    Some((near, n_near))
                }
            }
            (any, _) => any,
        };
        let (offset, window, trusted) = match peak {
            Some((p, _)) if pairs >= OFFSET_MIN_PAIRS => (p, DUPLICATE_WINDOW_SECONDS, true),
            _ => (0.0, FALLBACK_WINDOW_SECONDS, false),
        };
        if index > 0 {
            offsets.push(PerspectiveOffset {
                offset_s: offset,
                pairs_in_bin: peak.map(|(_, n)| n as u32).unwrap_or(0),
                pairs: pairs as u32,
                trusted,
            });
        }
        for (attacker, events) in ledger {
            let existing = merged.entry(*attacker).or_default();
            for event in events {
                let error = |e: &DamageEvent| (event.clock.seconds() - e.clock.seconds() - offset).abs();
                let best = existing
                    .iter_mut()
                    .filter(|(e, source, taken)| {
                        *source < index && !taken && e.victim == event.victim && e.amount == event.amount && error(e) <= window
                    })
                    .min_by(|a, b| error(&a.0).total_cmp(&error(&b.0)));
                if let Some(slot) = best {
                    slot.2 = true;
                    folded += 1;
                } else {
                    existing.push((*event, index, false));
                }
            }
        }
    }
    let mut out: HashMap<EntityId, Vec<DamageEvent>> =
        merged.into_iter().map(|(k, v)| (k, v.into_iter().map(|(e, _, _)| e).collect())).collect();
    for events in out.values_mut() {
        events.sort_by(|a, b| a.clock.seconds().total_cmp(&b.clock.seconds()));
    }
    (out, folded, offsets)
}

/// Fixed order of one owner's salvos: fire clock, salvo id, first shot id.
fn salvo_order(a: &ActiveShot, b: &ActiveShot) -> Ordering {
    let first = |s: &ActiveShot| s.salvo.shots.first().map(|x| x.shot_id.raw() as u64);
    a.fired_at
        .seconds()
        .total_cmp(&b.fired_at.seconds())
        .then(a.salvo.salvo_id.cmp(&b.salvo.salvo_id))
        .then(first(a).cmp(&first(b)))
}

/// Among salvos fired at the same moment, the one whose shells best match
/// the hit: the aim point nearest the victim at the damage clock, then the
/// recorded landing clock of its shells nearest the damage clock, then the
/// fixed order. `candidates` must arrive in the fixed order.
fn best_salvo<'a>(
    candidates: impl Iterator<Item = &'a ActiveShot>,
    t: f32,
    victim_pos: Option<WorldPos>,
    hits_by_shot: &HashMap<(EntityId, u64), Vec<f32>>,
) -> Option<&'a ActiveShot> {
    let mut best: Option<(&'a ActiveShot, f32, f32)> = None;
    for s in candidates {
        let target_error = victim_pos
            .map(|v| s.salvo.shots.iter().map(|x| timeline::ground_distance(x.target, v)).fold(f32::INFINITY, f32::min))
            .unwrap_or(f32::INFINITY);
        let landing_error = s
            .salvo
            .shots
            .iter()
            .filter_map(|x| hits_by_shot.get(&(s.salvo.owner_id, x.shot_id.raw() as u64)))
            .flatten()
            .map(|c| (c - t).abs())
            .fold(f32::INFINITY, f32::min);
        let better = match best {
            None => true,
            Some((_, best_target, best_landing)) => {
                if (target_error - best_target).abs() > SAME_TARGET_UNITS {
                    target_error < best_target
                } else if (landing_error - best_landing).abs() > SAME_LANDING_SECONDS {
                    landing_error < best_landing
                } else {
                    false
                }
            }
        };
        if better {
            best = Some((s, target_error, landing_error));
        }
    }
    best.map(|(s, _, _)| s)
}

/// One ship's damage as the ledger sums it against the game's own results.
#[derive(Debug, Clone, Default, Serialize)]
pub struct ShipReconciliation {
    pub entity: u32,
    pub player: String,
    pub ledger_total: f32,
    pub ledger_shell_fire: f32,
    pub game_total: Option<f32>,
    /// Main-battery plus fire damage from the game's results.
    pub game_shell_fire: Option<f32>,
    /// Ledger damage by classified kind.
    pub ledger_by_kind: BTreeMap<String, f32>,
    /// The game's results by damage field, non-zero fields only.
    pub game_by_type: BTreeMap<String, f32>,
}

/// Coverage of the attribution on this game.
#[derive(Debug, Clone, Default, Serialize)]
pub struct SpikeStats {
    pub events_per_replay: Vec<u32>,
    /// Events left out as another perspective's copy of a hit.
    pub events_dropped_as_duplicates: u32,
    /// Clock offset of each merged replay against the primary.
    pub perspective_offsets: Vec<PerspectiveOffset>,
    pub damage_events: u32,
    pub damage_total: f32,
    /// Damage dealt per attacker entity, for checks against the game's totals.
    pub damage_by_attacker: BTreeMap<u32, f32>,
    /// Shell plus fire damage per attacker entity.
    pub damage_by_attacker_shell_fire: BTreeMap<u32, f32>,
    /// Damage per attacker entity and classified kind.
    pub damage_by_attacker_kind: BTreeMap<u32, BTreeMap<String, f32>>,
    /// The primary recorder's damage to enemies as the game's own stats report
    /// it, and as the merged ledger sums it, for a ground-truth check.
    pub self_damage_authoritative: Option<f32>,
    pub self_damage_ledger: Option<f32>,
    pub self_entity: Option<u32>,
    /// Damage per attacker entity as the game's end-of-battle results report
    /// it, when the replay carries them.
    pub damage_by_attacker_authoritative: BTreeMap<u32, f32>,
    /// Every ship's ledger sums against the game's results.
    pub reconciliation: Vec<ShipReconciliation>,
    /// Ledger total over the game's total, across every ship with a result.
    pub reconciliation_ratio: Option<f32>,
    /// Ledger shell-plus-fire over the game's main-battery-plus-fire total.
    pub reconciliation_ratio_shell_fire: Option<f32>,
    /// Where the per-type totals came from.
    pub reconciliation_source: String,
    pub events_attacker_unknown: u32,
    pub events_by_source: BTreeMap<String, u32>,
    pub damage_by_source: BTreeMap<String, f32>,
    pub events_by_kind: BTreeMap<String, u32>,
    pub damage_by_kind: BTreeMap<String, f32>,
    pub events_no_attacker_position: u32,
    pub events_no_victim_position: u32,
    pub shot_hits: u32,
    pub salvos: u32,
    pub torpedoes: u32,
}

pub struct SpikeInput<'a> {
    pub ledger: &'a HashMap<EntityId, Vec<DamageEvent>>,
    pub hits: &'a [ResolvedShotHit],
    pub salvos: &'a [ActiveShot],
    pub torpedoes: &'a [ActiveTorpedo],
    pub smokes: &'a [SmokeGeometry],
    pub timeline: &'a PositionTimeline,
    pub flags_at: &'a dyn Fn(EntityId, GameClock) -> Option<VisibilityFlags>,
    pub team_of: &'a dyn Fn(EntityId) -> Option<i64>,
    /// Every ship in the game, so the proximity test sees ships that never
    /// dealt damage.
    pub roster: &'a [EntityId],
    /// Surface detection range of a ship in meters, from its build.
    pub detection_m_of: &'a dyn Fn(EntityId) -> Option<f32>,
    /// Death clock of each ship that died.
    pub deaths: &'a HashMap<EntityId, f32>,
    /// Owner entity and team of each smoke.
    pub smoke_owner: &'a HashMap<u32, (Option<EntityId>, Option<i64>)>,
    /// Whether a salvo's projectile is one the ship's main battery fires;
    /// `None` when the ship's main battery ammunition is unknown.
    pub is_main_battery: &'a dyn Fn(EntityId, GameParamId) -> Option<bool>,
}

pub struct SpikeOutput {
    pub events: Vec<AttributedDamage>,
    pub per_smoke: HashMap<u32, SmokeDamage>,
    pub stats: SpikeStats,
}

/// A damage event has a neighbour of the same amount about a second away.
fn in_tick_train(events: &[DamageEvent], index: usize) -> bool {
    let e = &events[index];
    let near = |other: &DamageEvent| {
        other.victim == e.victim
            && other.amount == e.amount
            && (TICK_GAP_MIN_SECONDS..=TICK_GAP_MAX_SECONDS).contains(&(other.clock.seconds() - e.clock.seconds()).abs())
    };
    events[..index].iter().rev().take(8).any(near) || events[index + 1..].iter().take(8).any(near)
}

/// A torpedo the attacker launched whose dead-reckoned track passes the
/// victim within the pass window around the damage clock. The direction
/// vector is in world units per second, like the origin.
fn torpedo_fits(torpedoes: &[&ActiveTorpedo], t: f32, victim_pos: Option<WorldPos>) -> bool {
    let Some(victim) = victim_pos else { return false };
    torpedoes.iter().any(|torp| {
        let run = t - torp.launched_at.seconds();
        if !(1.0..=TORPEDO_MAX_RUN_SECONDS).contains(&run) {
            return false;
        }
        let mut s = (t - TORPEDO_PASS_WINDOW_SECONDS).max(torp.launched_at.seconds());
        while s <= t + TORPEDO_PASS_WINDOW_SECONDS {
            let elapsed = s - torp.updated_at.seconds();
            let at = WorldPos(*torp.torpedo.origin + *torp.torpedo.direction * elapsed);
            if timeline::meters(timeline::ground_distance(at, victim)) <= TORPEDO_HIT_TOLERANCE_M {
                return true;
            }
            s += TORPEDO_PASS_STEP_SECONDS;
        }
        false
    })
}

pub fn run(input: &SpikeInput<'_>) -> SpikeOutput {
    let mut events = Vec::new();
    let mut per_smoke: HashMap<u32, SmokeDamage> = HashMap::new();
    let mut stats = SpikeStats {
        shot_hits: input.hits.len() as u32,
        salvos: input.salvos.len() as u32,
        torpedoes: input.torpedoes.len() as u32,
        ..Default::default()
    };

    let mut salvos_by_owner: HashMap<EntityId, Vec<&ActiveShot>> = HashMap::new();
    for s in input.salvos {
        salvos_by_owner.entry(s.salvo.owner_id).or_default().push(s);
    }
    for v in salvos_by_owner.values_mut() {
        v.sort_by(|a, b| salvo_order(a, b));
    }
    let mut torpedoes_by_owner: HashMap<EntityId, Vec<&ActiveTorpedo>> = HashMap::new();
    for t in input.torpedoes {
        torpedoes_by_owner.entry(t.torpedo.owner_id).or_default().push(t);
    }
    let mut hits_by_shot: HashMap<(EntityId, u64), Vec<f32>> = HashMap::new();
    for h in input.hits {
        hits_by_shot.entry((h.hit.owner_id, h.hit.shot_id.raw() as u64)).or_default().push(h.clock.seconds());
    }
    let mut ships: Vec<(EntityId, i64)> = Vec::new();
    for e in input.roster.iter().chain(input.ledger.keys()).chain(input.deaths.keys()) {
        if let Some(team) = (input.team_of)(*e)
            && !ships.iter().any(|(s, _)| s == e)
        {
            ships.push((*e, team));
        }
    }
    let smoke_created: HashMap<u32, f32> = input.smokes.iter().map(|s| (s.id, s.created)).collect();

    // Attackers in id order, so sums and the event list do not depend on map order.
    let mut attackers: Vec<&EntityId> = input.ledger.keys().collect();
    attackers.sort_by_key(|e| e.raw());
    for attacker in attackers {
        let attacker_team = (input.team_of)(*attacker);
        let ledger = &input.ledger[attacker];
        // (victim, damage clock, credited smokes) of this attacker's shells and
        // torpedoes, for linking ticks.
        let mut recent: Vec<(EntityId, f32, DamageKind, Vec<(u32, f32)>, Vec<u32>, Vec<u32>)> = Vec::new();
        for (index, event) in ledger.iter().enumerate() {
            stats.damage_events += 1;
            stats.damage_total += event.amount;
            *stats.damage_by_attacker.entry(attacker.raw() as u32).or_default() += event.amount;
            if attacker_team.is_none() {
                stats.events_attacker_unknown += 1;
                continue;
            }
            let t = event.clock.seconds();
            let victim_pos = input.timeline.get(&event.victim).and_then(|tr| timeline::world_pos_at(tr, event.clock));

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
                    let salvo = h.salvo.as_ref()?;
                    let origin = salvo.shots.first()?.origin;
                    Some((fired.seconds(), origin, FireSource::ShotHit, Some(salvo.params_id)))
                });
            let tick = in_tick_train(ledger, index);
            // A tick's damage is one amount per attacker and victim, so a
            // torpedo landing beside a shell hit is still torpedo damage,
            // when the amount is a torpedo's or the hit sinks the victim.
            let finishing = input.deaths.get(&event.victim).is_some_and(|d| (d - t).abs() <= FINISHING_HIT_SECONDS);
            let torpedo = !tick
                && (event.amount >= TORPEDO_MIN_DAMAGE || finishing)
                && torpedo_fits(torpedoes_by_owner.get(attacker).map(Vec::as_slice).unwrap_or(&[]), t, victim_pos);
            // The latest salvo before the damage; among salvos fired at the
            // same moment, the one whose shells match the hit.
            let from_salvo = from_hit.or_else(|| {
                if tick || torpedo {
                    return None;
                }
                let candidates: Vec<&ActiveShot> = salvos_by_owner
                    .get(attacker)
                    .into_iter()
                    .flatten()
                    .copied()
                    .filter(|s| {
                        let f = s.fired_at.seconds();
                        f <= t && t - f <= SALVO_MATCH_SECONDS
                    })
                    .collect();
                let latest = candidates.iter().map(|s| s.fired_at.seconds()).fold(f32::NEG_INFINITY, f32::max);
                let tied = candidates.into_iter().filter(|s| latest - s.fired_at.seconds() <= SAME_FIRE_SECONDS);
                best_salvo(tied, t, victim_pos, &hits_by_shot).and_then(|s| {
                    s.salvo.shots.first().map(|shot| (s.fired_at.seconds(), shot.origin, FireSource::Salvo, Some(s.salvo.params_id)))
                })
            });
            let (fire_seconds, fire_pos, source, projectile) = match from_salvo {
                Some(found) => found,
                None => {
                    let Some(pos) = input.timeline.get(attacker).and_then(|tr| timeline::world_pos_at(tr, event.clock))
                    else {
                        stats.events_no_attacker_position += 1;
                        continue;
                    };
                    (t, pos, FireSource::DamageClock, None)
                }
            };
            if victim_pos.is_none() {
                stats.events_no_victim_position += 1;
            }
            *stats.events_by_source.entry(format!("{source:?}")).or_default() += 1;
            *stats.damage_by_source.entry(format!("{source:?}")).or_default() += event.amount;

            // Kind: a tick follows the latest shell (fire) or torpedo (flood)
            // on the same victim; otherwise a shell needs a hit or a salvo.
            let linked = if tick {
                recent
                    .iter()
                    .rev()
                    .find(|(v, at, kind, _, _, _)| {
                        *v == event.victim && t - at <= FIRE_LINK_SECONDS && matches!(kind, DamageKind::Shell | DamageKind::Torpedo)
                    })
                    .cloned()
            } else {
                None
            };
            let kind = match (&linked, tick, torpedo, source) {
                (Some((_, _, DamageKind::Shell, _, _, _)), _, _, _) => DamageKind::Fire,
                (Some((_, _, DamageKind::Torpedo, _, _, _)), _, _, _) => DamageKind::Flood,
                (_, true, _, _) => DamageKind::Unknown,
                (_, _, true, _) => DamageKind::Torpedo,
                (_, _, _, FireSource::ShotHit | FireSource::Salvo) => DamageKind::Shell,
                (_, _, _, FireSource::DamageClock) => DamageKind::Unknown,
            };
            // A shell whose salvo fired a projectile the main battery does
            // not use came from the secondary battery; it earns no credit and
            // starts no credited fire.
            let kind = match (kind, projectile.and_then(|p| (input.is_main_battery)(*attacker, p))) {
                (DamageKind::Shell, Some(false)) => DamageKind::Secondary,
                (k, _) => k,
            };
            *stats.events_by_kind.entry(kind.as_str().to_string()).or_default() += 1;
            *stats.damage_by_kind.entry(kind.as_str().to_string()).or_default() += event.amount;
            if kind.credited() {
                *stats.damage_by_attacker_shell_fire.entry(attacker.raw() as u32).or_default() += event.amount;
            }
            *stats
                .damage_by_attacker_kind
                .entry(attacker.raw() as u32)
                .or_default()
                .entry(kind.as_str().to_string())
                .or_default() += event.amount;

            let fire_clock = GameClock(fire_seconds);
            let flags = (input.flags_at)(*attacker, fire_clock);
            let detected = flags.map(|f| f.is_detected());
            let detected_reason = flags.filter(|f| f.is_detected()).map(|f| {
                let proximity = timeline::world_units(crate::classify::PROXIMITY_M);
                let near = ships
                    .iter()
                    .filter(|(e, team)| Some(*team) != attacker_team && input.deaths.get(e).is_none_or(|d| *d > fire_seconds))
                    .filter_map(|(e, _)| input.timeline.get(e).and_then(|tr| timeline::world_pos_at(tr, fire_clock)))
                    .any(|p| timeline::ground_distance(fire_pos, p) <= proximity);
                crate::classify::detection_reason(f, near).0.to_string()
            });

            let (in_smokes, behind_smokes, credited) = match &linked {
                Some((_, _, _, credited, inside, behind)) => (inside.clone(), behind.clone(), credited.clone()),
                None => {
                    let mut in_smokes: Vec<u32> =
                        input.smokes.iter().filter(|s| s.contains(fire_seconds, fire_pos)).map(|s| s.id).collect();
                    in_smokes.sort_by(|a, b| smoke_created[a].total_cmp(&smoke_created[b]).then(a.cmp(b)));
                    if let Some(first) = in_smokes.first() {
                        (in_smokes.clone(), Vec::new(), vec![(*first, 1.0)])
                    } else if detected == Some(false) {
                        // Enemies alive and within the shooter's detection range.
                        let reach = timeline::world_units((input.detection_m_of)(*attacker).unwrap_or(DEFAULT_DETECTION_M));
                        let enemies: Vec<WorldPos> = ships
                            .iter()
                            .filter(|(e, team)| Some(*team) != attacker_team && input.deaths.get(e).is_none_or(|d| *d > fire_seconds))
                            .filter_map(|(e, _)| input.timeline.get(e).and_then(|tr| timeline::world_pos_at(tr, fire_clock)))
                            .filter(|p| timeline::ground_distance(fire_pos, *p) <= reach)
                            .collect();
                        let mut needed: Vec<u32> = input
                            .smokes
                            .iter()
                            .filter(|s| enemies.iter().any(|e| s.crosses(fire_seconds, fire_pos, *e)))
                            .map(|s| s.id)
                            .collect();
                        needed.sort_unstable();
                        let share = if needed.is_empty() { 0.0 } else { 1.0 / needed.len() as f32 };
                        let credited = needed.iter().map(|id| (*id, share)).collect();
                        (Vec::new(), needed, credited)
                    } else {
                        (Vec::new(), Vec::new(), Vec::new())
                    }
                }
            };
            if matches!(kind, DamageKind::Shell | DamageKind::Torpedo) {
                recent.push((event.victim, t, kind, credited.clone(), in_smokes.clone(), behind_smokes.clone()));
                if recent.len() > 64 {
                    recent.remove(0);
                }
            }

            let attributed = AttributedDamage {
                attacker: attacker.raw() as u32,
                victim: event.victim.raw() as u32,
                amount: event.amount,
                kind,
                damage_seconds: t,
                fire_seconds,
                fire_source: source,
                attacker_detected_at_fire: detected,
                detected_reason,
                in_smokes,
                behind_smokes,
                credited,
                fire_xz: Some(Xz { x: fire_pos.0.x, z: fire_pos.0.z }),
                victim_xz: victim_pos.map(|p| Xz { x: p.0.x, z: p.0.z }),
            };
            if kind.credited() {
                for (id, share) in &attributed.credited {
                    let inside = attributed.in_smokes.contains(id);
                    let role = role(*attacker, attacker_team, input.smoke_owner.get(id));
                    per_smoke.entry(*id).or_default().credit(&attributed, *share, role, inside);
                }
            }
            events.push(attributed);
        }
    }
    events.sort_by(|a, b| {
        a.damage_seconds
            .total_cmp(&b.damage_seconds)
            .then(a.attacker.cmp(&b.attacker))
            .then(a.victim.cmp(&b.victim))
            .then(a.fire_seconds.total_cmp(&b.fire_seconds))
            .then(a.amount.total_cmp(&b.amount))
    });
    for d in per_smoke.values_mut() {
        d.arrows.sort_by(|a, b| b.damage.total_cmp(&a.damage).then(a.attacker.cmp(&b.attacker)).then(a.victim.cmp(&b.victim)));
    }
    credit_kills(&events, input, &mut per_smoke);
    SpikeOutput { events, per_smoke, stats }
}

/// Damage recorded after the death clock still belongs to the sinking.
const KILL_WINDOW_SECONDS: f32 = 2.0;
/// Damage older than this before the death clock is not the killing blow;
/// the blow is then missing from the ledger and no smoke gets the kill.
const KILL_LOOKBACK_SECONDS: f32 = 10.0;

/// A kill goes to every smoke credited with the last damage a ship took
/// before it sank, when that damage came from the smoker's team. Several
/// events on the same final tick all count.
fn credit_kills(events: &[AttributedDamage], input: &SpikeInput<'_>, per_smoke: &mut HashMap<u32, SmokeDamage>) {
    let mut last_by_victim: BTreeMap<u32, f32> = BTreeMap::new();
    for e in events {
        if let Some(death) = input.deaths.get(&EntityId::from(e.victim))
            && e.damage_seconds <= death + KILL_WINDOW_SECONDS
            && e.damage_seconds >= death - KILL_LOOKBACK_SECONDS
        {
            let last = last_by_victim.entry(e.victim).or_insert(e.damage_seconds);
            *last = last.max(e.damage_seconds);
        }
    }
    for e in events {
        if !e.kind.credited() || last_by_victim.get(&e.victim) != Some(&e.damage_seconds) {
            continue;
        }
        let attacker = EntityId::from(e.attacker);
        let attacker_team = (input.team_of)(attacker);
        for (id, _) in &e.credited {
            if matches!(role(attacker, attacker_team, input.smoke_owner.get(id)), Role::Enemy) {
                continue;
            }
            let d = per_smoke.entry(*id).or_default();
            if d.kills.insert(e.victim) {
                d.targets.entry(e.victim).or_default().sunk = true;
                d.shooter_stats.entry(e.attacker).or_default().kills += 1;
            }
        }
    }
}

#[derive(Debug, Clone, Copy)]
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

    fn event(victim: u32, t: f32, amount: f32) -> DamageEvent {
        DamageEvent { amount, victim: EntityId::from(victim), clock: GameClock(t) }
    }

    #[test]
    fn split_buckets_by_detection_at_fire() {
        let attributed = |detected: Option<bool>, reason: Option<&str>| AttributedDamage {
            attacker: 1,
            victim: 2,
            amount: 100.0,
            kind: DamageKind::Shell,
            damage_seconds: 10.0,
            fire_seconds: 8.0,
            fire_source: FireSource::Salvo,
            attacker_detected_at_fire: detected,
            detected_reason: reason.map(str::to_string),
            in_smokes: Vec::new(),
            behind_smokes: Vec::new(),
            credited: Vec::new(),
            fire_xz: None,
            victim_xz: None,
        };
        let mut split = Split::default();
        split.add(&attributed(Some(false), None), 100.0);
        split.add(&attributed(Some(true), Some("radar")), 50.0);
        split.add(&attributed(Some(true), Some("radar")), 25.0);
        split.add(&attributed(Some(true), None), 5.0);
        split.add(&attributed(None, None), 7.0);
        assert_eq!(split.concealed, 100.0);
        assert_eq!(split.detected, 80.0);
        assert_eq!(split.unknown, 7.0);
        assert_eq!(split.by_reason["radar"], 75.0);
        assert_eq!(split.by_reason["other"], 5.0);
        let record = split.to_record();
        assert_eq!(record.detected_by.len(), 2);
    }

    #[test]
    fn tick_trains_are_a_second_apart_and_salvo_shells_are_not() {
        let fire = vec![event(7, 10.0, 300.0), event(7, 11.0, 300.0), event(7, 12.0, 300.0)];
        assert!(in_tick_train(&fire, 1));
        assert!(in_tick_train(&fire, 0));
        let salvo = vec![event(7, 10.0, 2100.0), event(7, 10.2, 2100.0), event(7, 10.3, 2100.0)];
        assert!(!in_tick_train(&salvo, 0));
        assert!(!in_tick_train(&salvo, 2));
        let mixed = vec![event(7, 10.0, 300.0), event(8, 11.0, 300.0)];
        assert!(!in_tick_train(&mixed, 0));
    }
}
