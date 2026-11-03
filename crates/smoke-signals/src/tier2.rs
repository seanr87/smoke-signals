//! Tier 2 tracking over the analysis pass: which ships stand in which smoke,
//! and detections (radar, hydro, firing from smoke) of ships the smoke was
//! concealing. Fed one step at a time; finalized per smoke at the end.

use std::collections::BTreeMap;
use std::collections::HashMap;
use std::collections::HashSet;

use serde::Serialize;
use wows_battle_world::components::SmokeScreenState;
use wows_battle_world::scan::PositionTimeline;
use wows_battle_world::view::BattleView;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::game_types::Consumable;
use wowsunpack::game_types::VisibilityFlags;
use wowsunpack::game_types::VisionFlag;
use wowsunpack::recognized::Recognized;

use crate::timeline;

/// How often the in-smoke geometry is evaluated.
const EVAL_INTERVAL_SECONDS: f32 = 0.25;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum DetectionKind {
    Radar,
    Hydro,
    FiredInSmoke,
}

impl DetectionKind {
    fn flag(self) -> VisionFlag {
        match self {
            Self::Radar => VisionFlag::Rls,
            Self::Hydro => VisionFlag::Sonar,
            Self::FiredInSmoke => VisionFlag::Smoke,
        }
    }

    fn consumable(self) -> Option<Consumable> {
        match self {
            Self::Radar => Some(Consumable::Radar),
            Self::Hydro => Some(Consumable::HydroacousticSearch),
            Self::FiredInSmoke => None,
        }
    }
}

/// A ship concealed by a smoke gaining a detection flag.
#[derive(Debug, Clone, Serialize)]
pub struct DetectionEvent {
    pub kind: DetectionKind,
    pub ship_entity: u32,
    pub ship: Option<String>,
    pub seconds: f32,
    pub clock: Option<crate::clock::BattleClock>,
    /// The enemy running the matching consumable nearest to the ship, when
    /// one was active; `None` for firing from smoke.
    pub source_entity: Option<u32>,
    pub source: Option<String>,
    pub source_distance_m: Option<f32>,
    pub source_in_range: Option<bool>,
    /// How long the ship then stayed detected, until the replay ends.
    pub detected_for_s: Option<f32>,
}

/// Per-smoke results of the tracker.
#[derive(Debug, Clone, Default, Serialize)]
pub struct SmokeTier2 {
    /// Ship-seconds inside the smoke, by ship entity.
    pub ship_seconds: BTreeMap<u32, f32>,
    pub detections: Vec<DetectionEvent>,
    /// Ships inside at each evaluation, for lookups at a moment.
    #[serde(skip)]
    pub inside_history: Vec<(f32, Vec<EntityId>)>,
}

impl SmokeTier2 {
    /// Ships inside the smoke at `seconds`, from the nearest evaluation.
    pub fn inside_at(&self, seconds: f32) -> &[EntityId] {
        let idx = self.inside_history.partition_point(|(c, _)| *c <= seconds);
        idx.checked_sub(1).and_then(|i| self.inside_history.get(i)).map(|(_, v)| v.as_slice()).unwrap_or(&[])
    }
}

struct OpenDetection {
    smoke: u32,
    index: usize,
}

/// Consumable ranges per ship, in meters, from the build.
#[derive(Debug, Clone, Default)]
pub struct ConsumableRanges {
    pub radar_m: Option<f32>,
    pub hydro_m: Option<f32>,
}

pub struct Tier2Tracker {
    ranges: HashMap<EntityId, ConsumableRanges>,
    teams: HashMap<EntityId, i64>,
    last_eval: Option<f32>,
    /// Flags as of the previous packet, so "concealed" means undetected
    /// before the detection packet arrived.
    prev_flags: HashMap<EntityId, VisibilityFlags>,
    /// Ships inside each live smoke at the last geometry evaluation.
    inside_now: HashMap<u32, HashSet<EntityId>>,
    per_smoke: HashMap<u32, SmokeTier2>,
    /// Detections whose flag is still set, one per concealing smoke.
    open: HashMap<(EntityId, DetectionKind), Vec<OpenDetection>>,
    /// Every flag change per ship, for queries at a moment.
    flag_history: HashMap<EntityId, Vec<(GameClock, VisibilityFlags)>>,
}

impl Tier2Tracker {
    pub fn new(ranges: HashMap<EntityId, ConsumableRanges>) -> Self {
        Self {
            ranges,
            teams: HashMap::new(),
            last_eval: None,
            prev_flags: HashMap::new(),
            inside_now: HashMap::new(),
            per_smoke: HashMap::new(),
            open: HashMap::new(),
            flag_history: HashMap::new(),
        }
    }

    pub fn flag_history(&self) -> &HashMap<EntityId, Vec<(GameClock, VisibilityFlags)>> {
        &self.flag_history
    }

    /// Visibility flags of `ship` as last reported at or before `clock`.
    pub fn flags_at(&self, ship: EntityId, clock: GameClock) -> Option<VisibilityFlags> {
        let history = self.flag_history.get(&ship)?;
        let idx = history.partition_point(|(c, _)| c.seconds() <= clock.seconds());
        idx.checked_sub(1).map(|i| history[i].1)
    }

    /// One step of the session: `smokes` are the live smoke objects.
    pub fn observe(
        &mut self,
        clock: GameClock,
        view: &BattleView<'_>,
        smokes: &HashMap<EntityId, &SmokeScreenState>,
        tl: &PositionTimeline,
    ) {
        if self.teams.is_empty() {
            for (id, p) in view.player_entities() {
                self.teams.insert(*id, p.initial_state().team_id());
            }
        }
        let t = clock.seconds();
        if self.last_eval.is_none_or(|last| t - last >= EVAL_INTERVAL_SECONDS) {
            let dt = self.last_eval.map(|last| t - last).unwrap_or(0.0);
            self.evaluate(t, dt, view, smokes, tl);
            self.last_eval = Some(t);
        }

        let props = view.vehicle_props_all();
        for (ship, p) in &props {
            let Some(flags) = p.visibility_flags() else { continue };
            let prev = self.prev_flags.insert(*ship, flags);
            if prev.is_some_and(|f| f.raw() == flags.raw()) {
                continue;
            }
            self.flag_history.entry(*ship).or_default().push((clock, flags));
            let was_detected = prev.is_some_and(|f| f.is_detected());
            for kind in [DetectionKind::Radar, DetectionKind::Hydro, DetectionKind::FiredInSmoke] {
                let gained = flags.contains(kind.flag()) && !prev.is_some_and(|f| f.contains(kind.flag()));
                let lost = !flags.contains(kind.flag()) && prev.is_some_and(|f| f.contains(kind.flag()));
                if lost && let Some(opened) = self.open.remove(&(*ship, kind)) {
                    for open in opened {
                        if let Some(event) =
                            self.per_smoke.get_mut(&open.smoke).and_then(|s| s.detections.get_mut(open.index))
                        {
                            event.detected_for_s = Some(t - event.seconds);
                        }
                    }
                }
                if !gained || was_detected {
                    continue;
                }
                // The ship was concealed: inside a smoke and undetected.
                let concealing: Vec<u32> =
                    self.inside_now.iter().filter(|(_, set)| set.contains(ship)).map(|(id, _)| *id).collect();
                for smoke in concealing {
                    let (source, distance, in_range) = self.likely_source(*ship, kind, clock, view, tl);
                    let entry = self.per_smoke.entry(smoke).or_default();
                    entry.detections.push(DetectionEvent {
                        kind,
                        ship_entity: ship.raw() as u32,
                        ship: None,
                        seconds: t,
                        clock: None,
                        source_entity: source.map(|e| e.raw() as u32),
                        source: None,
                        source_distance_m: distance,
                        source_in_range: in_range,
                        detected_for_s: None,
                    });
                    let index = entry.detections.len() - 1;
                    self.open.entry((*ship, kind)).or_default().push(OpenDetection { smoke, index });
                }
            }
        }
    }

    fn evaluate(
        &mut self,
        t: f32,
        dt: f32,
        view: &BattleView<'_>,
        smokes: &HashMap<EntityId, &SmokeScreenState>,
        tl: &PositionTimeline,
    ) {
        let dead = view.dead_ships();
        let clock = GameClock(t);
        let positions: Vec<(EntityId, wowsunpack::game_types::WorldPos)> = self
            .teams
            .keys()
            .filter(|e| !dead.contains_key(e))
            .filter_map(|e| tl.get(e).and_then(|track| timeline::world_pos_at(track, clock)).map(|p| (*e, p)))
            .collect();
        let mut inside_now: HashMap<u32, HashSet<EntityId>> = HashMap::new();
        for (id, state) in smokes {
            let smoke = id.raw() as u32;
            let radius = state.radius.value();
            let inside: Vec<EntityId> = positions
                .iter()
                .filter(|(_, p)| state.points.iter().any(|puff| timeline::ground_distance(*p, *puff) <= radius))
                .map(|(e, _)| *e)
                .collect();
            let entry = self.per_smoke.entry(smoke).or_default();
            for e in &inside {
                *entry.ship_seconds.entry(e.raw() as u32).or_default() += dt;
            }
            entry.inside_history.push((t, inside.clone()));
            inside_now.insert(smoke, inside.into_iter().collect());
        }
        self.inside_now = inside_now;
    }

    /// The nearest enemy of `ship` with `kind`'s consumable active now, its
    /// distance, and whether the ship lies within that consumable's range.
    fn likely_source(
        &self,
        ship: EntityId,
        kind: DetectionKind,
        clock: GameClock,
        view: &BattleView<'_>,
        tl: &PositionTimeline,
    ) -> (Option<EntityId>, Option<f32>, Option<bool>) {
        let Some(consumable) = kind.consumable() else { return (None, None, None) };
        let Some(team) = self.teams.get(&ship).copied() else { return (None, None, None) };
        let Some(pos) = tl.get(&ship).and_then(|t| timeline::world_pos_at(t, clock)) else {
            return (None, None, None);
        };
        let active = view.active_consumables();
        let mut best: Option<(EntityId, f32)> = None;
        for (enemy, list) in &active {
            if self.teams.get(enemy).copied() == Some(team) {
                continue;
            }
            let running = list.iter().any(|a| {
                a.consumable == Recognized::Known(consumable)
                    && a.activated_at.seconds() <= clock.seconds()
                    && clock.seconds() <= a.activated_at.seconds() + a.duration
            });
            if !running {
                continue;
            }
            let Some(epos) = tl.get(enemy).and_then(|t| timeline::world_pos_at(t, clock)) else { continue };
            let d = timeline::ground_distance(pos, epos);
            if best.is_none_or(|(_, b)| d < b) {
                best = Some((*enemy, d));
            }
        }
        match best {
            None => (None, None, None),
            Some((enemy, d)) => {
                let d = timeline::meters(d);
                let range = self.ranges.get(&enemy).and_then(|r| match kind {
                    DetectionKind::Radar => r.radar_m,
                    DetectionKind::Hydro => r.hydro_m,
                    DetectionKind::FiredInSmoke => None,
                });
                (Some(enemy), Some(d), range.map(|r| d <= r))
            }
        }
    }

    /// Per-smoke results, with the tracker kept for flag lookups.
    pub fn finish_keep_history(mut self) -> (Self, HashMap<u32, SmokeTier2>) {
        for s in self.per_smoke.values_mut() {
            s.inside_history.sort_by(|a, b| a.0.total_cmp(&b.0));
        }
        let per_smoke = std::mem::take(&mut self.per_smoke);
        (self, per_smoke)
    }
}
