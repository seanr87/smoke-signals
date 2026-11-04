//! Pass one over the merged session: track every smoke object, attribute an
//! owner and a type, and place the lifecycle times.
//!
//! The replay records no owner and no per-puff times for a smoke object, so
//! the tracker watches the puff list change on every packet and records the
//! times itself. Owners come from ship positions at creation plus the smoke
//! activations seen on those ships.

use std::collections::BTreeMap;
use std::collections::HashMap;
use std::collections::HashSet;

use rootcause::prelude::*;
use tracing::info;
use tracing::warn;
use wows_battle_world::components::SmokeScreenState;
use wows_replay_insights::build::ResolvedBuild;
use wows_replays::analyzer::battle_controller::Player;
use wows_replays::analyzer::battle_controller::merged::VehicleFacts;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::data::ResourceLoader;
use wowsunpack::game_params::provider::GameMetadataProvider;
use wowsunpack::game_params::types::GameParamProvider;
use wowsunpack::game_types::Consumable;
use wowsunpack::game_types::WorldPos;
use wowsunpack::recognized::Recognized;

use crate::clock::BattleClockMap;
use crate::config::Config;
use crate::damage;
use crate::records::Bbox;
use crate::records::CapDenial;
use crate::records::CapLayout;
use crate::records::OffensiveRadar;
use crate::records::RadarCapCoverage;
use crate::records::ShipMark;
use crate::records::GameRecord;
use crate::records::Moment;
use crate::records::Outcome;
use crate::records::PlayerRecord;
use crate::records::SmokeRecord;
use crate::records::SmokeType;
use crate::records::TeamRecord;
use crate::records::Xz;
use crate::replays::ReplaySet;
use crate::session::GameData;
use crate::session::GameSession;
use crate::state;
use crate::tier2;
use crate::timeline;

/// Farthest a ship may be from a smoke's origin at creation and still own
/// it without a flag, in meters. The first puff is laid about one smoke
/// radius (450 m) from the ship, so the bound is a radius plus slack.
pub const OWNER_MAX_DISTANCE_M: f32 = 600.0;

/// Longest gap between a smoke activation and the smoke object's creation.
pub const ACTIVATION_WINDOW_SECONDS: f32 = 5.0;

/// Farthest a ship that activated smoke in the window may be from the origin
/// and still be preferred over a nearer unactivated ship, in meters. A held
/// position is up to 10 s old, and a destroyer covers about 180 m in that
/// time, on top of the one-radius offset of the first puff.
pub const OWNER_ACTIVATED_MAX_DISTANCE_M: f32 = 1000.0;

/// Time between two puffs of one emission. A smoker that dies within this
/// interval after its last new puff died while still emitting.
pub const PUFF_INTERVAL_SECONDS: f32 = 4.0;

pub const SMOKE_SIGNALS_VERSION: &str = env!("CARGO_PKG_VERSION");
pub const WOWS_TOOLKIT_REV: Option<&str> = option_env!("SMOKE_SIGNALS_GIT_REV");

pub struct Analysis {
    pub game: GameRecord,
    pub smokes: Vec<SmokeRecord>,
    pub clock_map: BattleClockMap,
    pub timeline: std::sync::Arc<wows_battle_world::scan::PositionTimeline>,
    pub damage_events: Vec<damage::AttributedDamage>,
    pub damage_stats: damage::SpikeStats,
    /// Every visibility flag change per ship.
    pub flag_history: HashMap<EntityId, Vec<(GameClock, wowsunpack::game_types::VisibilityFlags)>>,
    /// The end-of-battle results blob, as the replay carries it.
    pub battle_results: Option<String>,
}

/// One smoke object, observed from creation to removal.
#[derive(Debug)]
struct SmokeTrack {
    created: GameClock,
    origin: WorldPos,
    radius: f32,
    /// Every new puff, in order of appearance.
    puffs: Vec<(GameClock, WorldPos)>,
    count: usize,
    first_point: Option<WorldPos>,
    last_point: Option<WorldPos>,
    first_fade: Option<GameClock>,
    removed: Option<GameClock>,
    /// The standing puffs every `CONTEST_SAMPLE_INTERVAL_S`.
    samples: Vec<(GameClock, Vec<WorldPos>)>,
}

impl SmokeTrack {
    fn new(clock: GameClock, state: &SmokeScreenState) -> Self {
        Self {
            created: clock,
            origin: state.position,
            radius: state.radius.value(),
            puffs: Vec::new(),
            count: 0,
            first_point: None,
            last_point: None,
            first_fade: None,
            removed: None,
            samples: Vec::new(),
        }
    }

    /// New puffs are the points after the previous last point; when that
    /// point is gone, every point is new. Puffs fade from the front, so a
    /// shorter list or a changed head marks the first fade. One update can
    /// both fade and add.
    fn observe(&mut self, clock: GameClock, state: &SmokeScreenState) {
        let points = &state.points;
        let head_changed = matches!((self.first_point, points.first()), (Some(old), Some(new)) if !same_pos(old, *new));
        if (points.len() < self.count || head_changed) && self.first_fade.is_none() {
            self.first_fade = Some(clock);
        }
        let start = match self.last_point {
            None => 0,
            Some(last) => points.iter().rposition(|p| same_pos(*p, last)).map_or(0, |i| i + 1),
        };
        self.puffs.extend(points[start..].iter().map(|p| (clock, *p)));
        self.count = points.len();
        self.first_point = points.first().copied();
        self.last_point = points.last().copied();
    }

    /// Puff life as seen: the last puff laid fades when the object goes.
    /// `None` until the object was removed.
    fn observed_puff_life(&self) -> Option<f32> {
        Some(self.removed?.seconds() - self.last_new_puff()?.seconds())
    }

    fn last_new_puff(&self) -> Option<GameClock> {
        self.puffs.last().map(|(c, _)| *c)
    }

    fn last_new_puff_before(&self, limit: GameClock) -> Option<GameClock> {
        self.puffs.iter().rev().find(|(c, _)| c.seconds() <= limit.seconds()).map(|(c, _)| *c)
    }

    fn bbox(&self) -> Option<Bbox> {
        let mut it = self.puffs.iter().map(|(_, p)| p);
        let first = it.next()?;
        let mut b = Bbox { min_x: first.0.x, min_z: first.0.z, max_x: first.0.x, max_z: first.0.z };
        for p in it {
            b.min_x = b.min_x.min(p.0.x);
            b.min_z = b.min_z.min(p.0.z);
            b.max_x = b.max_x.max(p.0.x);
            b.max_z = b.max_z.max(p.0.z);
        }
        Some(b)
    }
}

fn same_pos(a: WorldPos, b: WorldPos) -> bool {
    a.0.x == b.0.x && a.0.y == b.0.y && a.0.z == b.0.z
}

/// The smoke consumable fitted to one ship, from GameParams.
#[derive(Debug, Clone)]
struct SmokeFit {
    variant: String,
    smoke_type: SmokeType,
    work_time: f32,
    puff_life: Option<f32>,
    radius: Option<f32>,
    charges_total: Option<u32>,
}

fn smoke_fit(facts: &VehicleFacts, gp: &GameMetadataProvider, version: wowsunpack::data::Version) -> Option<SmokeFit> {
    let ship = GameParamProvider::game_param_by_id(gp, facts.vehicle_id)?;
    let species = ship.species()?.known().copied()?;
    let cfg = &facts.ship_config;
    // The crew blob carries id 0 when no commander is assigned; the build
    // resolver takes `None` for that case.
    let captain_id = (facts.crew.params_id().raw() != 0).then(|| facts.crew.params_id());
    let skills = facts.crew.learned_skills().for_species(&species);
    let build = ResolvedBuild::from_ids(
        cfg.ship_params_id(),
        cfg.units(),
        cfg.modernization(),
        captain_id,
        skills,
        cfg.exteriors(),
        cfg.abilities(),
        species,
        version,
        gp,
    )?;
    let slot = build.slots.iter().find(|s| s.consumable_type == Recognized::Known(Consumable::Smoke))?;
    let category = slot.ability.ability()?.get_category(&slot.variant_name)?;
    let fields = category.effect_fields();
    let charges_total = match slot.total_charges {
        wowsunpack::game_types::ChargeCount::Finite(n) => Some(n),
        wowsunpack::game_types::ChargeCount::Unlimited => None,
    };
    let puff_life = fields.get("lifeTime").copied();
    let mut smoke_type = classify(&slot.variant_name, category.icon_id());
    if smoke_type == SmokeType::Standard && puff_life.is_some_and(|l| l <= CRUISER_PUFF_LIFE_MAX_S) {
        smoke_type = SmokeType::Cruiser;
    }
    Some(SmokeFit {
        smoke_type,
        variant: slot.variant_name.clone(),
        work_time: category.work_time(),
        puff_life,
        radius: fields.get("radius").copied(),
        charges_total,
    })
}

/// Radar and hydro ranges of one ship's build, in meters.
fn consumable_ranges(
    facts: &VehicleFacts,
    gp: &GameMetadataProvider,
    version: wowsunpack::data::Version,
) -> Option<tier2::ConsumableRanges> {
    let ship = GameParamProvider::game_param_by_id(gp, facts.vehicle_id)?;
    let species = ship.species()?.known().copied()?;
    let cfg = &facts.ship_config;
    let captain_id = (facts.crew.params_id().raw() != 0).then(|| facts.crew.params_id());
    let skills = facts.crew.learned_skills().for_species(&species);
    let build = ResolvedBuild::from_ids(
        cfg.ship_params_id(),
        cfg.units(),
        cfg.modernization(),
        captain_id,
        skills,
        cfg.exteriors(),
        cfg.abilities(),
        species,
        version,
        gp,
    )?;
    let range = |consumable: Consumable| {
        build
            .slots
            .iter()
            .find(|s| s.consumable_type == Recognized::Known(consumable))
            .and_then(|s| s.ability.ability()?.get_category(&s.variant_name)?.detection_radius())
            .map(|m| m.value())
    };
    // Stock values on purpose: the component's own range and detection,
    // without fire control, upgrades or skills.
    let ttx = build.ship.vehicle().and_then(|v| v.ttx_components());
    let equipped = |uc_type: &str, keys: Vec<&String>| -> Option<String> {
        let module = build
            .modules
            .iter()
            .find(|m| m.unit().and_then(|u| u.uc_type()).is_some_and(|t| t.eq_ignore_ascii_case(uc_type)))
            .map(|m| m.name().to_string());
        module.filter(|m| keys.iter().any(|k| *k == m)).or_else(|| {
            let mut keys = keys;
            keys.sort();
            keys.first().map(|k| k.to_string())
        })
    };
    let gun_m = ttx.and_then(|t| {
        let key = equipped("_Artillery", t.artillery.keys().collect())?;
        t.artillery.get(&key)?.max_dist.map(|m| m.value())
    });
    let detection_m = ttx.and_then(|t| {
        let key = equipped("_Hull", t.hulls.keys().collect())?;
        t.hulls.get(&key)?.visibility_factor.map(|km| km.value() * 1000.0)
    });
    Some(tier2::ConsumableRanges {
        radar_m: range(Consumable::Radar),
        hydro_m: range(Consumable::HydroacousticSearch),
        gun_m,
        detection_m,
    })
}

/// A standard smoke whose puffs last this long or less is the short cruiser
/// kind (Svea: 10 s emission, 40 s puffs). Destroyer smokes last 89 s or more.
const CRUISER_PUFF_LIFE_MAX_S: f32 = 60.0;

/// Smoke type from the variant's name and icon. Every smoke consumable has
/// consumableType `smokeGenerator`; only the variant tells them apart. Short
/// cruiser smoke is told apart afterwards by puff life.
pub fn classify(variant: &str, icon_id: &str) -> SmokeType {
    let text = format!("{variant} {icon_id}").to_ascii_lowercase();
    if text.contains("crawl") || text.contains("creep") {
        SmokeType::Crawling
    } else if text.contains("oil") || text.contains("exhaust") {
        SmokeType::Exhaust
    } else {
        SmokeType::Standard
    }
}

/// In-game display name of a map from the game's string catalog, e.g.
/// `spaces/58_RidgeNew` -> `Mountain Range`; the bare internal name when the
/// catalog has no entry.
pub fn map_display_name(gp: &GameMetadataProvider, map_name: &str) -> String {
    let full = if map_name.starts_with("spaces/") { map_name.to_string() } else { format!("spaces/{map_name}") };
    let key = wowsunpack::data::TranslationKey::new(format!("IDS_{}", full.to_uppercase()));
    gp.localized_name_from_id(&key)
        .filter(|s| !s.trim().is_empty())
        .unwrap_or_else(|| crate::records::map_title_fallback(full.strip_prefix("spaces/").unwrap_or(&full)))
}

#[derive(Debug, Clone, Copy, PartialEq)]
struct Activation {
    entity: EntityId,
    clock: GameClock,
}

struct Roster {
    player: String,
    clan: String,
    team_id: i64,
    team: String,
    ship: String,
    ship_index: String,
    ship_class: Option<String>,
    ship_tier: Option<u32>,
    fit: Option<SmokeFit>,
}

/// Team name of a player: the primary team for the recorder's side, the
/// configured opponent for the other side, else the player-name prefix.
fn team_label(config: &Config, player_name: &str, friendly: bool) -> String {
    if friendly {
        config.run.primary_team.clone()
    } else if let Some(opponent) = &config.run.opponent_team {
        opponent.clone()
    } else if player_name.starts_with(&config.run.team_prefix) {
        config.run.primary_team.clone()
    } else {
        player_name.split('_').next().unwrap_or(player_name).to_string()
    }
}

fn roster_entry(config: &Config, game: &GameData, player: &Player, facts: Option<&VehicleFacts>) -> Roster {
    let gp = &game.loaded.game_params;
    let vehicle = player.vehicle();
    let name = player.initial_state().username().to_string();
    let ship =
        gp.localized_name_from_param(vehicle).map(|s| s.to_string()).unwrap_or_else(|| vehicle.index().to_string());
    let ship_class = vehicle.species().map(|s| match s {
        Recognized::Known(k) => format!("{k:?}"),
        Recognized::Unknown(raw) => raw.to_string(),
    });
    let relation = player.relation();
    Roster {
        team: team_label(config, &name, relation.is_self() || relation.is_ally()),
        player: name,
        clan: player.initial_state().clan().to_string(),
        team_id: player.initial_state().team_id(),
        ship,
        ship_index: vehicle.index().to_string(),
        ship_class,
        ship_tier: vehicle.vehicle().map(|v| v.level()),
        fit: facts.and_then(|f| smoke_fit(f, gp, game.version)),
    }
}

fn moment(map: &BattleClockMap, clock: GameClock) -> Moment {
    Moment { seconds: clock.seconds(), clock: map.at(clock) }
}

/// Mean of a team's first positions. `None` when no ship of the team has a
/// position.
fn spawn_center(timeline: &wows_battle_world::scan::PositionTimeline, entities: &[EntityId]) -> Option<WorldPos> {
    let mut sum = (0.0f32, 0.0f32);
    let mut n = 0;
    for e in entities {
        if let Some(track) = timeline.get(e)
            && let Some((_, p)) = track.world.first()
        {
            sum.0 += p.0.x;
            sum.1 += p.0.z;
            n += 1;
        }
    }
    if n == 0 {
        return None;
    }
    Some(WorldPos::new(sum.0 / n as f32, 0.0, sum.1 / n as f32))
}

/// Side of the map a spawn centre lies on. The two spawns are told apart
/// along the axis they are furthest apart on; north and south unless the
/// east-west separation is clearly larger, so corner spawns on a diagonal
/// map get one consistent pair of labels.
fn spawn_side(center: WorldPos, other: Option<WorldPos>) -> String {
    let (x, z) = (center.0.x, center.0.z);
    let east_west = match other {
        Some(o) => (x - o.0.x).abs() > (z - o.0.z).abs() * EAST_WEST_SPAWN_RATIO,
        None => x.abs() > z.abs() * EAST_WEST_SPAWN_RATIO,
    };
    let side = if !east_west {
        if z >= 0.0 { "north" } else { "south" }
    } else if x >= 0.0 {
        "east"
    } else {
        "west"
    };
    side.to_string()
}

/// Spawns count as east and west only when their east-west separation is
/// this many times the north-south one.
const EAST_WEST_SPAWN_RATIO: f32 = 1.5;

/// How often the standing puffs and the cap state are sampled for the
/// contested cap distance.
const CONTEST_SAMPLE_INTERVAL_S: f32 = 2.0;

/// A capture zone of the domination kind. Size is no test: Mountain Range
/// has a 10 km cap A at the map edge.
pub fn is_capture_zone(cp: &wows_replays::analyzer::battle_controller::state::CapturePointState) -> bool {
    match &cp.control_point_type {
        Some(Recognized::Known(wowsunpack::game_types::ControlPointType::Control)) | None => true,
        Some(_) => false,
    }
}

/// One enabled cap at a sample.
#[derive(Debug, Clone, Copy, PartialEq)]
struct CapSample {
    index: usize,
    position: WorldPos,
    radius: f32,
    /// Owning team id, negative when neutral.
    owner: i64,
    /// The invading team while someone is inside.
    invader: Option<i64>,
}

/// Why a cap counts as contested for a team, in the order checked.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
enum ContestReason {
    /// The midline between the spawns crosses the cap.
    Midline,
    /// The cap lies wholly on the enemy's side of the midline.
    EnemySide,
    /// The enemy owns the cap.
    EnemyOwned,
}

impl ContestReason {
    fn as_str(self) -> &'static str {
        match self {
            Self::Midline => "midline",
            Self::EnemySide => "enemy_side",
            Self::EnemyOwned => "enemy_owned",
        }
    }
}

impl std::fmt::Display for ContestReason {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.as_str())
    }
}

/// The midline is at right angles to the line joining the spawns, halfway
/// along it. Returns how far the cap centre lies past the midline toward
/// the enemy spawn, in world units.
fn across_midline(cap: WorldPos, ours: WorldPos, theirs: WorldPos) -> f32 {
    let (dx, dz) = (theirs.0.x - ours.0.x, theirs.0.z - ours.0.z);
    let len = (dx * dx + dz * dz).sqrt();
    if len == 0.0 {
        return 0.0;
    }
    let (mx, mz) = ((ours.0.x + theirs.0.x) / 2.0, (ours.0.z + theirs.0.z) / 2.0);
    ((cap.0.x - mx) * dx + (cap.0.z - mz) * dz) / len
}

fn contest_reason(cap: &CapSample, ours: Option<WorldPos>, theirs: Option<WorldPos>, enemy: i64) -> Option<ContestReason> {
    if let (Some(o), Some(t)) = (ours, theirs) {
        let s = across_midline(cap.position, o, t);
        if s.abs() <= cap.radius {
            return Some(ContestReason::Midline);
        }
        if s > cap.radius {
            return Some(ContestReason::EnemySide);
        }
    }
    (cap.owner == enemy).then_some(ContestReason::EnemyOwned)
}

/// A radar activation seen in the replay.
#[derive(Debug, Clone, Copy)]
struct RadarActivation {
    entity: EntityId,
    clock: GameClock,
    duration: f32,
}

/// Ships this close to a smoke's origin at t_capture go on its diagram.
const DIAGRAM_REACH_M: f32 = 9000.0;
/// A cap is won by the smoke when it flips this long after the last puff fades, at most.
const CAP_WON_GRACE_SECONDS: f32 = 10.0;
/// "Near" a cap for the denial count: this far beyond the cap's edge.
const CAP_NEAR_M: f32 = 1000.0;
/// The denial baseline covers this long before the smoke object appeared.
const DENIAL_BEFORE_SECONDS: f32 = 60.0;

struct ContestedCap {
    cap: char,
    reason: ContestReason,
    avg_distance_m: f32,
    /// Share of the radius from the smoke's edge to the cap centre.
    depth_pct: f32,
    radius_m: f32,
}

struct CapMetrics {
    contested: Option<ContestedCap>,
    supported: Vec<usize>,
    won: Option<(usize, GameClock)>,
    defended: Option<usize>,
    radar_cap: Option<RadarCapCoverage>,
    denial: Option<CapDenial>,
}

struct CapContext<'a> {
    cap_history: &'a [(GameClock, Vec<CapSample>)],
    ours: &'a TeamRecord,
    theirs: &'a TeamRecord,
    inside: Option<&'a tier2::SmokeTier2>,
    roster: &'a HashMap<EntityId, Roster>,
    ranges: &'a HashMap<EntityId, tier2::ConsumableRanges>,
    tl: &'a wows_battle_world::scan::PositionTimeline,
    deaths: &'a HashMap<EntityId, GameClock>,
    radar_activations: &'a [RadarActivation],
    flags_at: &'a dyn Fn(EntityId, GameClock) -> Option<wowsunpack::game_types::VisibilityFlags>,
    end: GameClock,
}

/// Area of the intersection of two circles with radii `r1` and `r2` whose
/// centres are `d` apart.
fn circle_intersection_area(r1: f32, r2: f32, d: f32) -> f32 {
    if d >= r1 + r2 {
        return 0.0;
    }
    if d <= (r1 - r2).abs() {
        let r = r1.min(r2);
        return std::f32::consts::PI * r * r;
    }
    let a1 = ((d * d + r1 * r1 - r2 * r2) / (2.0 * d * r1)).clamp(-1.0, 1.0).acos();
    let a2 = ((d * d + r2 * r2 - r1 * r1) / (2.0 * d * r2)).clamp(-1.0, 1.0).acos();
    let k = (-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2);
    r1 * r1 * a1 + r2 * r2 * a2 - 0.5 * k.max(0.0).sqrt()
}

/// Cap metrics over the smoke's sampled life: the nearest contested cap and
/// its depth, caps supported by our concealed guns, a cap won or defended,
/// radar coverage of a contested cap from inside, and the denial signal.
fn cap_metrics(track: &SmokeTrack, ctx: &CapContext<'_>) -> Option<CapMetrics> {
    let ours = ctx.ours;
    let theirs = ctx.theirs;
    let our_spawn = ours.spawn_xy.map(|p| WorldPos::new(p.x, 0.0, p.z));
    let their_spawn = theirs.spawn_xy.map(|p| WorldPos::new(p.x, 0.0, p.z));
    let caps_at = |clock: GameClock| {
        ctx.cap_history.iter().rev().find(|(c, _)| c.seconds() <= clock.seconds()).map(|(_, caps)| caps.as_slice())
    };
    let alive = |e: &EntityId, clock: GameClock| ctx.deaths.get(e).is_none_or(|d| d.seconds() > clock.seconds());
    let mut distances: Vec<f32> = Vec::new();
    let mut nearest_counts: HashMap<(usize, ContestReason), usize> = HashMap::new();
    let mut centre_distances: HashMap<usize, Vec<f32>> = HashMap::new();
    let mut radii: HashMap<usize, f32> = HashMap::new();
    let mut supported: Vec<usize> = Vec::new();
    let mut defended: Option<usize> = None;
    let mut radar_best: Option<(usize, f32, bool, EntityId)> = None;
    let mut enemies_during: Vec<f32> = Vec::new();
    for (clock, puffs) in &track.samples {
        let Some(caps) = caps_at(*clock) else { continue };
        let inside_allies: Vec<EntityId> = ctx
            .inside
            .map(|t2| t2.inside_at(clock.seconds()).iter().copied().filter(|e| ctx.roster.get(e).is_some_and(|r| r.team_id == ours.team_id)).collect())
            .unwrap_or_default();
        for cap in caps {
            radii.insert(cap.index, cap.radius);
            if cap.owner == ours.team_id
                && cap.invader == Some(theirs.team_id)
                && contest_reason(cap, our_spawn, their_spawn, theirs.team_id).is_some()
            {
                defended.get_or_insert(cap.index);
            }
            for e in &inside_allies {
                let Some(pos) = ctx.tl.get(e).and_then(|t| timeline::world_pos_at(t, *clock)) else { continue };
                let d = timeline::ground_distance(pos, cap.position);
                let r = ctx.ranges.get(e);
                if let Some(gun) = r.and_then(|r| r.gun_m)
                    && timeline::meters(d - cap.radius) <= gun
                    && !supported.contains(&cap.index)
                {
                    supported.push(cap.index);
                }
                if let Some(radar) = r.and_then(|r| r.radar_m)
                    && contest_reason(cap, our_spawn, their_spawn, theirs.team_id).is_some()
                    && !(ctx.flags_at)(*e, *clock).is_some_and(|f| f.is_detected())
                {
                    let radar_wu = timeline::world_units(radar);
                    let full = d + cap.radius <= radar_wu;
                    let area = circle_intersection_area(radar_wu, cap.radius, d);
                    let pct = (area / (std::f32::consts::PI * cap.radius * cap.radius) * 100.0).clamp(0.0, 100.0);
                    if radar_best.is_none_or(|(_, best, _, _)| pct > best) {
                        radar_best = Some((cap.index, pct, full, *e));
                    }
                }
            }
        }
        if puffs.is_empty() {
            continue;
        }
        let nearest = caps
            .iter()
            .filter_map(|cap| {
                let reason = contest_reason(cap, our_spawn, their_spawn, theirs.team_id)?;
                let d = puffs.iter().map(|p| timeline::ground_distance(*p, cap.position)).fold(f32::INFINITY, f32::min);
                Some((d - track.radius - cap.radius, d - track.radius, cap.index, reason, cap.position, cap.radius))
            })
            .min_by(|a, b| a.0.total_cmp(&b.0));
        if let Some((edge, centre, index, reason, pos, radius)) = nearest {
            distances.push(timeline::meters(edge));
            *nearest_counts.entry((index, reason)).or_default() += 1;
            centre_distances.entry(index).or_default().push(timeline::meters(centre));
            let near = radius + timeline::world_units(CAP_NEAR_M);
            let n = ctx
                .roster
                .iter()
                .filter(|(e, r)| r.team_id == theirs.team_id && alive(e, *clock))
                .filter_map(|(e, _)| ctx.tl.get(e).and_then(|t| timeline::world_pos_at(t, *clock)))
                .filter(|p| timeline::ground_distance(*p, pos) <= near)
                .count();
            enemies_during.push(n as f32);
        }
    }
    let contested = if distances.is_empty() {
        None
    } else {
        let ((index, reason), _) = nearest_counts.iter().max_by_key(|((i, r), n)| (**n, std::cmp::Reverse((*i, *r))))?;
        let radius_m = timeline::meters(radii.get(index).copied().unwrap_or(0.0));
        let centre = &centre_distances[index];
        let avg_centre = centre.iter().sum::<f32>() / centre.len() as f32;
        Some(ContestedCap {
            cap: state::cap_letter(*index),
            reason: *reason,
            avg_distance_m: distances.iter().sum::<f32>() / distances.len() as f32,
            depth_pct: if radius_m > 0.0 { (radius_m - avg_centre) / radius_m * 100.0 } else { 0.0 },
            radius_m,
        })
    };
    // Cap won: a supported cap that flips to us during the smoke or just after.
    let start = track.created.seconds();
    let until = track.removed.unwrap_or(ctx.end).seconds() + CAP_WON_GRACE_SECONDS;
    let mut won: Option<(usize, GameClock)> = None;
    let mut prev: HashMap<usize, i64> = caps_at(track.created).map(|c| c.iter().map(|c| (c.index, c.owner)).collect()).unwrap_or_default();
    for (clock, caps) in ctx.cap_history.iter().filter(|(c, _)| c.seconds() >= start && c.seconds() <= until) {
        for cap in caps {
            let before = prev.insert(cap.index, cap.owner);
            if won.is_none() && cap.owner == ours.team_id && before.is_some_and(|b| b != ours.team_id) && supported.contains(&cap.index) {
                won = Some((cap.index, *clock));
            }
        }
    }
    // Denial baseline: enemies near the contested cap in the minute before.
    let denial = contested.as_ref().and_then(|c| {
        let index = (c.cap as u8 - b'A') as usize;
        let caps = caps_at(track.created)?;
        let cap = caps.iter().find(|x| x.index == index)?;
        let near = cap.radius + timeline::world_units(CAP_NEAR_M);
        let mut before: Vec<f32> = Vec::new();
        let mut t = start - DENIAL_BEFORE_SECONDS;
        while t < start {
            let clock = GameClock(t);
            let n = ctx
                .roster
                .iter()
                .filter(|(e, r)| r.team_id == theirs.team_id && alive(e, clock))
                .filter_map(|(e, _)| ctx.tl.get(e).and_then(|tr| timeline::world_pos_at(tr, clock)))
                .filter(|p| timeline::ground_distance(*p, cap.position) <= near)
                .count();
            before.push(n as f32);
            t += CONTEST_SAMPLE_INTERVAL_S;
        }
        Some(CapDenial {
            cap: c.cap.to_string(),
            enemies_before: if before.is_empty() { 0.0 } else { before.iter().sum::<f32>() / before.len() as f32 },
            enemies_during: if enemies_during.is_empty() { 0.0 } else { enemies_during.iter().sum::<f32>() / enemies_during.len() as f32 },
        })
    });
    let radar_cap = radar_best.map(|(index, pct, full, ship)| {
        let life_end = track.removed.unwrap_or(ctx.end).seconds();
        let activated = ctx.radar_activations.iter().any(|a| {
            a.entity == ship
                && a.clock.seconds() >= start
                && a.clock.seconds() <= life_end
                && ctx.inside.is_some_and(|t2| t2.inside_at(a.clock.seconds()).contains(&ship))
        });
        RadarCapCoverage {
            cap: state::cap_letter(index).to_string(),
            ship: ctx.roster.get(&ship).map(|r| r.player.clone()),
            coverage_pct: pct,
            full,
            activated,
        }
    });
    supported.sort_unstable();
    Some(CapMetrics { contested, supported, won, defended, radar_cap, denial })
}

pub fn analyze_game(config: &Config, game: &GameData, replays: &ReplaySet) -> Result<Analysis, Report> {
    let mut session = GameSession::new(game, replays)?;
    let mut tracks: BTreeMap<EntityId, SmokeTrack> = BTreeMap::new();
    let mut seen_activations: HashSet<(EntityId, u32)> = HashSet::new();
    let mut activations: Vec<Activation> = Vec::new();
    let tl = session.timeline_arc();
    let ranges: HashMap<EntityId, tier2::ConsumableRanges> = session
        .vehicle_facts()
        .iter()
        .filter_map(|(id, f)| consumable_ranges(f, &game.loaded.game_params, game.version).map(|r| (*id, r)))
        .collect();
    let mut tier2 = tier2::Tier2Tracker::new(ranges);
    let mut hits: Vec<wows_replays::analyzer::battle_controller::state::ResolvedShotHit> = Vec::new();
    // The view's hit list is cleared when a packet is processed, not when a
    // secondary packet is skipped, so the same hits show up on several steps.
    let mut seen_hits: HashSet<(u32, u32, u32, u32)> = HashSet::new();
    let mut salvos: HashMap<(u32, u32, u32), wows_replays::analyzer::battle_controller::state::ActiveShot> =
        HashMap::new();
    let mut cap_history: Vec<(GameClock, Vec<CapSample>)> = Vec::new();
    let mut next_sample: Option<f32> = None;
    let mut torpedoes: HashMap<(u32, u32, u32), wows_replays::analyzer::battle_controller::state::ActiveTorpedo> =
        HashMap::new();
    let mut radar_activations: Vec<RadarActivation> = Vec::new();
    let mut seen_radar: HashSet<(EntityId, u32)> = HashSet::new();

    while session.step()?.is_some() {
        let view = session.view();
        let clock = view.clock();
        let smokes = view.smoke_screens();
        for (id, state) in &smokes {
            tracks.entry(*id).or_insert_with(|| SmokeTrack::new(clock, state)).observe(clock, state);
        }
        if next_sample.is_none_or(|t| clock.seconds() >= t) {
            next_sample = Some(clock.seconds() + CONTEST_SAMPLE_INTERVAL_S);
            let caps: Vec<CapSample> = view
                .capture_points()
                .iter()
                .filter(|cp| cp.is_enabled && is_capture_zone(cp))
                .filter_map(|cp| {
                    Some(CapSample {
                        index: cp.index,
                        position: cp.position?,
                        radius: cp.radius,
                        owner: cp.team_id,
                        invader: cp.has_invaders.then_some(cp.invader_team),
                    })
                })
                .collect();
            if cap_history.last().is_none_or(|(_, last)| *last != caps) {
                cap_history.push((clock, caps));
            }
            for (id, state) in &smokes {
                if let Some(track) = tracks.get_mut(id) {
                    track.samples.push((clock, state.points.clone()));
                }
            }
        }
        tier2.observe(clock, &view, &smokes, &tl);
        for hit in view.shot_hits() {
            let key = (
                hit.hit.owner_id.raw() as u32,
                hit.victim_entity_id.raw() as u32,
                hit.clock.seconds().to_bits(),
                hit.hit.shot_id.raw(),
            );
            if seen_hits.insert(key) {
                hits.push(hit.clone());
            }
        }
        for shot in view.active_shots() {
            let key = (shot.salvo.owner_id.raw() as u32, shot.salvo.salvo_id, shot.fired_at.seconds().to_bits());
            salvos.entry(key).or_insert(shot);
        }
        for (id, track) in tracks.iter_mut() {
            if track.removed.is_none() && !smokes.contains_key(id) {
                track.removed = Some(clock);
            }
        }
        for (entity, list) in view.active_consumables() {
            for a in list {
                if a.consumable == Recognized::Known(Consumable::Smoke)
                    && seen_activations.insert((entity, a.activated_at.seconds().to_bits()))
                {
                    activations.push(Activation { entity, clock: a.activated_at });
                }
                if a.consumable == Recognized::Known(Consumable::Radar)
                    && seen_radar.insert((entity, a.activated_at.seconds().to_bits()))
                {
                    radar_activations.push(RadarActivation { entity, clock: a.activated_at, duration: a.duration });
                }
            }
        }
        for torp in view.active_torpedoes() {
            let key = (torp.torpedo.owner_id.raw() as u32, torp.torpedo.salvo_id, torp.torpedo.shot_id.raw());
            torpedoes.entry(key).or_insert(torp);
        }
    }
    session.finish();
    activations.sort_by(|a, b| a.clock.seconds().total_cmp(&b.clock.seconds()));
    info!(smokes = tracks.len(), activations = activations.len(), "Tracked smoke objects");
    if session.clock_map().is_empty() {
        bail!("the HUD countdown was never observed; battle clocks cannot be placed");
    }

    let map = session.clock_map().clone();
    let facts = session.vehicle_facts().clone();
    let (tracker, per_smoke) = tier2.finish_keep_history();
    radar_activations.sort_by(|a, b| a.clock.seconds().total_cmp(&b.clock.seconds()).then(a.entity.raw().cmp(&b.entity.raw())));
    let generated_at = jiff::Zoned::now().strftime("%Y-%m-%dT%H:%M:%S%:z").to_string();

    let view = session.view();
    let roster: HashMap<EntityId, Roster> =
        view.player_entities().iter().map(|(id, p)| (*id, roster_entry(config, game, p, facts.get(id)))).collect();
    let deaths: HashMap<EntityId, GameClock> = view.dead_ships().iter().map(|(id, d)| (*id, d.clock)).collect();
    let scores: HashMap<usize, i64> = view.team_scores().iter().map(|s| (s.team_index, s.score)).collect();
    let winner_id = view.winning_team();
    let finish_type = view.finish_type().map(|f| match f {
        Recognized::Known(k) => format!("{k:?}"),
        Recognized::Unknown(raw) => raw.to_string(),
    });
    let battle_end = view.battle_end_clock();
    let caps: Vec<CapLayout> = view
        .capture_points()
        .iter()
        .filter(|cp| cp.is_enabled && is_capture_zone(cp))
        .filter_map(|cp| {
            let p = cp.position?;
            Some(CapLayout {
                cap: state::cap_letter(cp.index),
                position: Xz { x: p.0.x, z: p.0.z },
                radius: cp.radius,
                radius_m: timeline::meters(cp.radius),
                kind: cp.control_point_type.as_ref().map(|k| match k {
                    Recognized::Known(k) => k.name().to_string(),
                    Recognized::Unknown(raw) => raw.to_string(),
                }),
            })
        })
        .collect();
    let self_authoritative: f32 = view
        .self_damage_stats()
        .iter()
        .filter(|((_, category), _)| *category == Recognized::Known(wowsunpack::game_types::DamageStatCategory::Enemy))
        .map(|(_, entry)| entry.total as f32)
        .sum();
    drop(view);
    let battle_results = session.battle_results();

    let mut team_ids: Vec<i64> = roster.values().map(|r| r.team_id).collect();
    team_ids.sort_unstable();
    team_ids.dedup();
    let team_name = |team_id: i64| -> Option<String> {
        let mut counts: BTreeMap<&str, usize> = BTreeMap::new();
        for r in roster.values().filter(|r| r.team_id == team_id) {
            *counts.entry(r.team.as_str()).or_default() += 1;
        }
        counts.into_iter().max_by_key(|(_, n)| *n).map(|(name, _)| name.to_string())
    };

    // Without a configured match id the primary replay's file stem names the
    // game; the stem is the one identity every replay has.
    let match_id = match &config.game.match_id {
        Some(id) => id.clone(),
        None => replays
            .primary_path
            .file_stem()
            .map(|s| s.to_string_lossy().to_string())
            .ok_or_else(|| report!("primary replay path has no file name: {}", replays.primary_path.display()))?,
    };
    let round = config.game.round.clone();
    let map_name = replays.primary.meta.mapName.clone();
    let map_label = map_name.strip_prefix("spaces/").unwrap_or(&map_name).to_string();
    let map_display = map_display_name(&game.loaded.game_params, &map_name);
    let file_name = |p: &std::path::Path| p.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
    let primary_replay = file_name(&replays.primary_path);
    let merged_replays: Vec<String> = replays.merge_paths.iter().map(|p| file_name(p)).collect();

    let teams: Vec<TeamRecord> = team_ids
        .iter()
        .map(|team_id| {
            let mut entities: Vec<EntityId> =
                roster.iter().filter(|(_, r)| r.team_id == *team_id).map(|(id, _)| *id).collect();
            entities.sort_by_key(|e| e.raw());
            let players = entities
                .iter()
                .map(|e| {
                    let r = &roster[e];
                    PlayerRecord {
                        entity_id: e.raw() as u32,
                        player: r.player.clone(),
                        clan: r.clan.clone(),
                        ship: r.ship.clone(),
                        ship_index: r.ship_index.clone(),
                        ship_class: r.ship_class.clone(),
                        ship_tier: r.ship_tier,
                        smoke_variant: r.fit.as_ref().map(|f| f.variant.clone()),
                        smoke_type: r.fit.as_ref().map(|f| f.smoke_type),
                        smoke_activations: activations.iter().filter(|a| a.entity == *e).count() as u32,
                        smoke_charges: r.fit.as_ref().and_then(|f| f.charges_total),
                        death: deaths.get(e).map(|c| moment(&map, *c)),
                        gun_range_m: tracker.ranges().get(e).and_then(|r| r.gun_m),
                        radar_m: tracker.ranges().get(e).and_then(|r| r.radar_m),
                        detection_m: tracker.ranges().get(e).and_then(|r| r.detection_m),
                    }
                })
                .collect();
            let spawn = spawn_center(&tl, &entities);
            let other_spawn = team_ids
                .iter()
                .find(|t| *t != team_id)
                .and_then(|t| spawn_center(&tl, &roster.iter().filter(|(_, r)| r.team_id == *t).map(|(id, _)| *id).collect::<Vec<_>>()));
            TeamRecord {
                name: team_name(*team_id),
                team_id: *team_id,
                spawn_side: spawn.map(|p| spawn_side(p, other_spawn)),
                spawn_xy: spawn.map(|p| Xz { x: p.0.x, z: p.0.z }),
                final_score: usize::try_from(*team_id).ok().and_then(|i| scores.get(&i).copied()),
                players,
            }
        })
        .collect();
    let team_by_id = |id: i64| teams.iter().find(|t| t.team_id == id);

    let ids: Vec<EntityId> = tracks.keys().copied().collect();
    let mut smokes: Vec<SmokeRecord> = Vec::with_capacity(ids.len());
    for id in &ids {
        let track = &tracks[id];

        // Owner: among ships fitted with a smoke consumable, the nearest one
        // that activated smoke in the window before creation; failing that,
        // the nearest fitted ship, flagged. A ship with no precise position
        // falls back to its minimap position, also flagged.
        let activated = |e: EntityId| {
            activations.iter().rev().find(|a| {
                a.entity == e && {
                    let dt = track.created.seconds() - a.clock.seconds();
                    (0.0..=ACTIVATION_WINDOW_SECONDS).contains(&dt)
                }
            })
        };
        let mut candidates: Vec<(EntityId, f32, timeline::PosSource, Option<Activation>)> = roster
            .iter()
            .filter(|(_, r)| r.fit.is_some())
            .filter_map(|(entity, _)| {
                let (pos, source) = tl.get(entity).and_then(|t| timeline::ship_pos_at(t, track.created))?;
                let distance_m = timeline::meters(timeline::ground_distance(pos, track.origin));
                Some((*entity, distance_m, source, activated(*entity).copied()))
            })
            .collect();
        candidates.sort_by(|a, b| a.1.total_cmp(&b.1));
        let chosen = candidates
            .iter()
            .find(|c| c.3.is_some() && c.1 <= OWNER_ACTIVATED_MAX_DISTANCE_M)
            .or_else(|| candidates.first())
            .copied();
        let owner = chosen.map(|c| c.0);
        let distance = chosen.map(|c| c.1);
        let activation: Option<Activation> = chosen.and_then(|c| c.3);
        let mut notes: Vec<String> = Vec::new();
        match chosen {
            None => notes.push("no ship with a smoke consumable had a position at creation".to_string()),
            Some((_, d, source, act)) => {
                if act.is_none() {
                    notes.push(format!("no smoke activation within {ACTIVATION_WINDOW_SECONDS} s before creation"));
                }
                if source == timeline::PosSource::Minimap {
                    notes.push("position from minimap samples only".to_string());
                } else if d > OWNER_MAX_DISTANCE_M {
                    notes.push(format!("nearest ship {d:.0} m from origin"));
                }
            }
        }
        let owner_flag = !notes.is_empty();
        if owner_flag {
            warn!(smoke = id.raw(), note = %notes.join("; "), "Owner attribution flagged");
        }
        let r = owner.and_then(|e| roster.get(&e));
        let fit = r.and_then(|r| r.fit.clone());
        let smoke_type = fit.as_ref().map(|f| f.smoke_type);

        let t_emission_end = match smoke_type {
            Some(SmokeType::Standard) | Some(SmokeType::Cruiser) | None => match track.first_fade {
                Some(fade) => track.last_new_puff_before(fade),
                None => track.last_new_puff(),
            },
            Some(SmokeType::Exhaust) | Some(SmokeType::Crawling) => track.last_new_puff(),
        };
        let t_capture = t_emission_end;
        let t_activate = activation.map(|a| a.clock);
        let emission_from = t_activate.unwrap_or(track.created);
        let observed_emission_s = t_emission_end.map(|e| e.seconds() - emission_from.seconds());
        // A smoker that dies while emitting stops the emission at death.
        let emission_cut_short = match (owner.and_then(|e| deaths.get(&e)), t_emission_end) {
            (Some(death), Some(end)) => {
                death.seconds() >= emission_from.seconds() && death.seconds() <= end.seconds() + PUFF_INTERVAL_SECONDS
            }
            _ => false,
        };
        let charge_no = match (owner, activation) {
            (Some(e), Some(a)) => {
                Some(activations.iter().filter(|x| x.entity == e && x.clock.seconds() <= a.clock.seconds()).count()
                    as u32)
            }
            _ => None,
        };
        let activation_id = match (owner, charge_no) {
            (Some(e), Some(n)) => Some(format!("{}_{n}", e.raw())),
            _ => None,
        };
        let path = Some(track.puffs.iter().map(|(_, p)| Xz { x: p.0.x, z: p.0.z }).collect());
        let contest = r.and_then(|r| {
            let ours = team_by_id(r.team_id)?;
            let theirs = teams.iter().find(|t| t.team_id != r.team_id)?;
            let ctx = CapContext {
                cap_history: &cap_history,
                ours,
                theirs,
                inside: per_smoke.get(&(id.raw() as u32)),
                roster: &roster,
                ranges: tracker.ranges(),
                tl: &tl,
                deaths: &deaths,
                radar_activations: &radar_activations,
                flags_at: &|e, c| tracker.flags_at(e, c),
                end: session.total_duration(),
            };
            cap_metrics(track, &ctx)
        });
        let mark_clock = t_capture.unwrap_or(emission_from);
        let mut ships_at_capture: Vec<ShipMark> = roster
            .iter()
            .filter(|(e, _)| deaths.get(e).is_none_or(|d| d.seconds() > mark_clock.seconds()))
            .filter_map(|(e, rr)| {
                let pos = tl.get(e).and_then(|t| timeline::world_pos_at(t, mark_clock))?;
                (timeline::meters(timeline::ground_distance(pos, track.origin)) <= DIAGRAM_REACH_M).then(|| ShipMark {
                    entity_id: e.raw() as u32,
                    player: rr.player.clone(),
                    team: team_by_id(rr.team_id).and_then(|t| t.name.clone()),
                    ship_class: rr.ship_class.clone(),
                    position: Xz { x: pos.0.x, z: pos.0.z },
                    is_owner: Some(*e) == owner,
                })
            })
            .collect();
        ships_at_capture.sort_by_key(|m| m.entity_id);
        let team = r.map(|r| r.team.clone());
        let opponent = r
            .and_then(|r| team_ids.iter().find(|t| **t != r.team_id))
            .and_then(|t| team_by_id(*t))
            .and_then(|t| t.name.clone());
        let spawn_side = r.and_then(|r| team_by_id(r.team_id)).and_then(|t| t.spawn_side.clone());

        smokes.push(SmokeRecord {
            smoke_id: id.raw() as u32,
            activation_id,
            match_id: match_id.clone(),
            round: round.clone(),
            game_no: config.game.game_no,
            map: map_label.clone(),
            map_display: map_display.clone(),
            game_build: replays.primary.meta.clientVersionFromExe.clone(),
            primary_replay: primary_replay.clone(),
            merged_replays: merged_replays.clone(),
            team,
            opponent,
            spawn_side,
            player: r.map(|r| r.player.clone()),
            ship: r.map(|r| r.ship.clone()),
            ship_class: r.and_then(|r| r.ship_class.clone()),
            ship_tier: r.and_then(|r| r.ship_tier),
            smoke_type,
            variant: fit.as_ref().map(|f| f.variant.clone()),
            charge_no,
            charges_total: fit.as_ref().and_then(|f| f.charges_total),
            base_emission_s: fit.as_ref().map(|f| f.work_time),
            base_puff_life_s: fit.as_ref().and_then(|f| f.puff_life),
            base_radius: fit.as_ref().and_then(|f| f.radius),
            radius: track.radius,
            observed_emission_s,
            emission_cut_short,
            owner_flag,
            owner_note: notes.join("; "),
            owner_distance_m: distance,
            overlap_flag: false,
            overlapping_smoke_ids: Vec::new(),
            origin_xy: Xz { x: track.origin.0.x, z: track.origin.0.z },
            bbox: track.bbox(),
            puff_count: track.puffs.len() as u32,
            path,
            t_created: moment(&map, track.created),
            t_activate: t_activate.map(|c| moment(&map, c)),
            t_capture: t_capture.map(|c| moment(&map, c)),
            t_emission_end: t_emission_end.map(|c| moment(&map, c)),
            t_dispersed: track.removed.map(|c| moment(&map, c)),
            state_at_activate: None,
            state_at_capture: None,
            allies_in_smoke: Vec::new(),
            enemies_in_smoke: Vec::new(),
            ally_ship_seconds_in_smoke: 0.0,
            enemy_ship_seconds_in_smoke: 0.0,
            radar_detections_in_smoke: Vec::new(),
            hydro_detections_in_smoke: Vec::new(),
            fired_while_concealed_detections: Vec::new(),
            cap_proximity_m: None,
            cap_proximity_name: None,
            cap_radius_m: None,
            selfish_smoke: None,
            contested_cap_name: contest.as_ref().and_then(|c| c.contested.as_ref()).map(|c| c.cap.to_string()),
            cap_contested_reason: contest.as_ref().and_then(|c| c.contested.as_ref()).map(|c| c.reason.to_string()),
            avg_contested_cap_dist_m: contest.as_ref().and_then(|c| c.contested.as_ref()).map(|c| c.avg_distance_m),
            contested_cap_depth_pct: contest.as_ref().and_then(|c| c.contested.as_ref()).map(|c| c.depth_pct),
            contested_cap_radius_m: contest.as_ref().and_then(|c| c.contested.as_ref()).map(|c| c.radius_m),
            supported_caps: contest.as_ref().map(|c| c.supported.iter().map(|i| state::cap_letter(*i).to_string()).collect()).unwrap_or_default(),
            cap_won: contest.as_ref().and_then(|c| c.won).map(|(i, _)| state::cap_letter(i).to_string()),
            cap_won_at: contest.as_ref().and_then(|c| c.won).map(|(_, c)| moment(&map, c)),
            cap_defended: contest.as_ref().and_then(|c| c.defended).map(|i| state::cap_letter(i).to_string()),
            radar_cap: contest.as_ref().and_then(|c| c.radar_cap.clone()),
            cap_denial: contest.as_ref().and_then(|c| c.denial.clone()),
            radar_spotted_damage: 0.0,
            offensive_radar: None,
            shooters: Vec::new(),
            ships_at_capture,
            damage_in_smoke: None,
            damage_behind_smoke: None,
            smoke_damage_total: None,
            damage_in_smoke_enemy: None,
            damage_behind_smoke_enemy: None,
            damage_detail: None,
            wows_toolkit_rev: WOWS_TOOLKIT_REV.map(str::to_string),
            smoke_signals_version: SMOKE_SIGNALS_VERSION.to_string(),
            generated_at: generated_at.clone(),
            frame_act: None,
            frame_cap: None,
            frame_act_zoom: None,
            frame_cap_zoom: None,
            clip: None,
        });
    }

    // Overlap: a puff of one smoke within the two radii of a puff of the
    // other while both puffs stand. A puff stands from the moment it is laid
    // until its base lifetime runs out or the smoke object is removed.
    let end = session.total_duration();
    let standing = |track: &SmokeTrack, life: Option<f32>, laid: GameClock| -> (f32, f32) {
        let until = track.removed.unwrap_or(end).seconds();
        (laid.seconds(), life.map_or(until, |l| (laid.seconds() + l).min(until)))
    };
    for i in 0..ids.len() {
        for j in (i + 1)..ids.len() {
            let (a, b) = (&tracks[&ids[i]], &tracks[&ids[j]]);
            let a_end = a.removed.unwrap_or(end).seconds();
            let b_end = b.removed.unwrap_or(end).seconds();
            if a.created.seconds() > b_end || b.created.seconds() > a_end {
                continue;
            }
            let (life_a, life_b) = (
                a.observed_puff_life().or(smokes[i].base_puff_life_s),
                b.observed_puff_life().or(smokes[j].base_puff_life_s),
            );
            let reach = a.radius + b.radius;
            let touching = a.puffs.iter().any(|(ta, pa)| {
                let (a0, a1) = standing(a, life_a, *ta);
                b.puffs.iter().any(|(tb, pb)| {
                    let (b0, b1) = standing(b, life_b, *tb);
                    a0 <= b1 && b0 <= a1 && timeline::ground_distance(*pa, *pb) <= reach
                })
            });
            if touching {
                smokes[i].overlap_flag = true;
                smokes[i].overlapping_smoke_ids.push(ids[j].raw() as u32);
                smokes[j].overlap_flag = true;
                smokes[j].overlapping_smoke_ids.push(ids[i].raw() as u32);
            }
        }
    }

    // Tier 2: ships in the smoke and detections while concealed. A ship
    // inside two overlapping smokes gets each detection counted once, for
    // the first-laid smoke.
    let name_of = |e: u32| roster.get(&EntityId::from(e)).map(|r| r.player.clone());
    let mut spot_owner: HashMap<(u32, u32, tier2::DetectionKind), u32> = HashMap::new();
    for id in &ids {
        let Some(t2) = per_smoke.get(&(id.raw() as u32)) else { continue };
        for event in &t2.detections {
            let key = (event.ship_entity, event.seconds.to_bits(), event.kind);
            let current = spot_owner.entry(key).or_insert(id.raw() as u32);
            if tracks[id].created.seconds() < tracks[&EntityId::from(*current)].created.seconds() {
                *current = id.raw() as u32;
            }
        }
    }
    for (i, id) in ids.iter().enumerate() {
        let Some(t2) = per_smoke.get(&(id.raw() as u32)) else { continue };
        let owner_team =
            smokes[i].player.as_ref().and_then(|name| roster.values().find(|r| &r.player == name)).map(|r| r.team_id);
        let is_ally = |e: EntityId| roster.get(&e).map(|r| Some(r.team_id) == owner_team).unwrap_or(false);
        let owner_entity = smokes[i]
            .player
            .as_ref()
            .and_then(|name| roster.iter().find(|(_, r)| &r.player == name))
            .map(|(e, _)| e.raw() as u32);
        let other_ally_inside = t2
            .ship_seconds
            .iter()
            .any(|(e, secs)| *secs > 0.0 && Some(*e) != owner_entity && is_ally(EntityId::from(*e)));
        smokes[i].selfish_smoke = Some(!other_ally_inside);
        for (e, secs) in &t2.ship_seconds {
            if is_ally(EntityId::from(*e)) {
                smokes[i].ally_ship_seconds_in_smoke += secs;
            } else {
                smokes[i].enemy_ship_seconds_in_smoke += secs;
            }
        }
        if let Some(cap) = smokes[i].t_capture {
            for e in t2.inside_at(cap.seconds) {
                let name = name_of(e.raw() as u32).unwrap_or_else(|| e.raw().to_string());
                if is_ally(*e) {
                    smokes[i].allies_in_smoke.push(name);
                } else {
                    smokes[i].enemies_in_smoke.push(name);
                }
            }
        }
        for event in &t2.detections {
            // Only the smoking team's ships count; an enemy sitting in our smoke never does.
            if !is_ally(EntityId::from(event.ship_entity)) {
                continue;
            }
            if spot_owner.get(&(event.ship_entity, event.seconds.to_bits(), event.kind)) != Some(&(id.raw() as u32)) {
                continue;
            }
            let mut event = event.clone();
            event.ship = name_of(event.ship_entity);
            event.source = event.source_entity.and_then(name_of);
            event.clock = map.at(GameClock(event.seconds));
            match event.kind {
                tier2::DetectionKind::Radar => smokes[i].radar_detections_in_smoke.push(event),
                tier2::DetectionKind::Hydro => smokes[i].hydro_detections_in_smoke.push(event),
                tier2::DetectionKind::FiredInSmoke => smokes[i].fired_while_concealed_detections.push(event),
            }
        }
        // Offensive radar: a radar of the smoker's team run from inside this
        // smoke while concealed; enemies that gained the radar flag within
        // its range during the activation count as spotted by it.
        let track = &tracks[id];
        let life_end = track.removed.unwrap_or(session.total_duration()).seconds();
        let mut spotted: HashSet<EntityId> = HashSet::new();
        let mut radar_ship: Option<EntityId> = None;
        let mut radar_runs = 0;
        for act in &radar_activations {
            let t0 = act.clock.seconds();
            if t0 < track.created.seconds() || t0 > life_end || !is_ally(act.entity) {
                continue;
            }
            if !t2.inside_at(t0).contains(&act.entity) {
                continue;
            }
            if tracker.flags_at(act.entity, act.clock).is_some_and(|f| f.is_detected()) {
                continue;
            }
            let Some(range) = tracker.ranges().get(&act.entity).and_then(|r| r.radar_m) else { continue };
            radar_runs += 1;
            radar_ship.get_or_insert(act.entity);
            for (enemy, rr) in roster.iter().filter(|(_, rr)| Some(rr.team_id) != owner_team) {
                let _ = rr;
                let Some(history) = tracker.flag_history().get(enemy) else { continue };
                let gained = history.windows(2).any(|w| {
                    let (c, f) = w[1];
                    let s = c.seconds();
                    s >= t0
                        && s <= t0 + act.duration
                        && f.contains(wowsunpack::game_types::VisionFlag::Rls)
                        && !w[0].1.contains(wowsunpack::game_types::VisionFlag::Rls)
                        && {
                            let ours = tl.get(&act.entity).and_then(|t| timeline::world_pos_at(t, c));
                            let theirs = tl.get(enemy).and_then(|t| timeline::world_pos_at(t, c));
                            matches!((ours, theirs), (Some(a), Some(b)) if timeline::meters(timeline::ground_distance(a, b)) <= range)
                        }
                });
                if gained {
                    spotted.insert(*enemy);
                }
            }
        }
        if radar_runs > 0 {
            smokes[i].offensive_radar = Some(OffensiveRadar {
                ship: radar_ship.and_then(|e| name_of(e.raw() as u32)),
                activations: radar_runs,
                enemies_spotted: spotted.len() as u32,
                inferred: true,
            });
        }
    }

    // Tier 3 spike: damage credited to smokes.
    let (ledger, events_per_replay, dropped) = {
        let mut all: Vec<&wows_replays::ReplayFile> = vec![&replays.primary];
        all.extend(replays.merges.iter());
        let ledgers = damage::ledgers_per_replay(
            &game.loaded.controller_game_params,
            &game.constants,
            game.version,
            &game.loaded.specs,
            &all,
        );
        let per_replay: Vec<u32> = ledgers.iter().map(|l| l.values().map(|v| v.len() as u32).sum()).collect();
        let (merged, dropped) = damage::merge_ledgers(&ledgers);
        (merged, per_replay, dropped)
    };
    let geometry: Vec<damage::SmokeGeometry> = ids
        .iter()
        .zip(smokes.iter())
        .map(|(id, record)| {
            let track = &tracks[id];
            damage::SmokeGeometry {
                id: id.raw() as u32,
                radius: track.radius,
                puffs: track.puffs.iter().map(|(c, p)| (c.seconds(), *p)).collect(),
                puff_life: track.observed_puff_life().or(record.base_puff_life_s),
                created: track.created.seconds(),
                removed: track.removed.map(|c| c.seconds()),
            }
        })
        .collect();
    let smoke_owner: HashMap<u32, (Option<EntityId>, Option<i64>)> = ids
        .iter()
        .zip(smokes.iter())
        .map(|(id, record)| {
            let owner = record
                .player
                .as_ref()
                .and_then(|name| roster.iter().find(|(_, r)| &r.player == name))
                .map(|(e, r)| (*e, r.team_id));
            (id.raw() as u32, (owner.map(|(e, _)| e), owner.map(|(_, t)| t)))
        })
        .collect();
    let salvo_list: Vec<wows_replays::analyzer::battle_controller::state::ActiveShot> = salvos.into_values().collect();
    let mut torpedo_list: Vec<wows_replays::analyzer::battle_controller::state::ActiveTorpedo> =
        torpedoes.into_values().collect();
    torpedo_list.sort_by(|a, b| {
        a.launched_at.seconds().total_cmp(&b.launched_at.seconds()).then(a.torpedo.shot_id.raw().cmp(&b.torpedo.shot_id.raw()))
    });
    let deaths_s: HashMap<EntityId, f32> = deaths.iter().map(|(e, c)| (*e, c.seconds())).collect();
    let flags_at = |e: EntityId, c: GameClock| tracker.flags_at(e, c);
    let team_of = |e: EntityId| roster.get(&e).map(|r| r.team_id);
    let detection_m_of = |e: EntityId| tracker.ranges().get(&e).and_then(|r| r.detection_m);
    let mut spike = damage::run(&damage::SpikeInput {
        ledger: &ledger,
        hits: &hits,
        salvos: &salvo_list,
        torpedoes: &torpedo_list,
        smokes: &geometry,
        timeline: &tl,
        flags_at: &flags_at,
        team_of: &team_of,
        detection_m_of: &detection_m_of,
        deaths: &deaths_s,
        smoke_owner: &smoke_owner,
    });
    // With no damage events at all the credit is unknown, not zero.
    if spike.stats.damage_events > 0 {
        for (i, id) in ids.iter().enumerate() {
            let d = spike.per_smoke.get(&(id.raw() as u32)).cloned().unwrap_or_default();
            smokes[i].damage_in_smoke = Some(d.damage_in_smoke());
            smokes[i].damage_behind_smoke = Some(d.damage_behind_smoke());
            smokes[i].smoke_damage_total = Some(d.smoke_damage_total());
            smokes[i].damage_in_smoke_enemy = Some(d.damage_in_smoke_enemy);
            smokes[i].damage_behind_smoke_enemy = Some(d.damage_behind_smoke_enemy);
            if d.damage_behind_smoke_ally > 0.0 {
                smokes[i].selfish_smoke = Some(false);
            }
            smokes[i].shooters = d.shooters.iter().filter_map(|e| name_of(*e)).collect();
            // Damage taken by our radar-spotted ships while the spot lasted.
            let mut spotted_damage = 0.0;
            for ev in &smokes[i].radar_detections_in_smoke {
                let until = ev.detected_for_s.map(|d| ev.seconds + d).unwrap_or(f32::INFINITY);
                for events in ledger.values() {
                    for e in events.iter().filter(|e| e.victim.raw() as u32 == ev.ship_entity) {
                        let t = e.clock.seconds();
                        if t >= ev.seconds && t <= until {
                            spotted_damage += e.amount;
                        }
                    }
                }
            }
            smokes[i].radar_spotted_damage = spotted_damage;
            smokes[i].damage_detail = Some(d);
        }
    }
    // Every ship's ledger sums against the game's own results, by type where
    // the results carry it (main battery AP, HE and CS plus fire).
    if let Some(results) = session.battle_results()
        && let Ok(decoded) = crate::diagnostics::decode_public_results(&game.build_dir.join("constants.json"), &results)
    {
        let mut ledger_sum = 0.0;
        let mut game_sum = 0.0;
        let mut ledger_sf = 0.0;
        let mut game_sf = 0.0;
        for r in &decoded {
            let Some((e, _)) = roster.iter().find(|(_, rr)| rr.player == r.name) else { continue };
            let id = e.raw() as u32;
            let entry = damage::ShipReconciliation {
                entity: id,
                player: r.name.clone(),
                ledger_total: spike.stats.damage_by_attacker.get(&id).copied().unwrap_or(0.0),
                ledger_shell_fire: spike.stats.damage_by_attacker_shell_fire.get(&id).copied().unwrap_or(0.0),
                game_total: r.damage.map(|d| d as f32),
                game_shell_fire: [r.damage_main_ap, r.damage_main_he, r.damage_main_cs, r.damage_fire]
                    .iter()
                    .filter_map(|v| *v)
                    .map(|v| v as f32)
                    .reduce(|a, b| a + b),
            };
            if let Some(g) = entry.game_total {
                spike.stats.damage_by_attacker_authoritative.insert(id, g);
                ledger_sum += entry.ledger_total;
                game_sum += g;
            }
            if let Some(g) = entry.game_shell_fire {
                ledger_sf += entry.ledger_shell_fire;
                game_sf += g;
            }
            spike.stats.reconciliation.push(entry);
        }
        spike.stats.reconciliation.sort_by(|a, b| a.player.cmp(&b.player));
        spike.stats.reconciliation_ratio = (game_sum > 0.0).then(|| ledger_sum / game_sum);
        spike.stats.reconciliation_ratio_shell_fire = (game_sf > 0.0).then(|| ledger_sf / game_sf);
        spike.stats.reconciliation_source =
            "battle results playersPublicInfo: damage, damage_main_ap, damage_main_he, damage_main_cs, damage_fire".to_string();
    }
    if spike.stats.damage_events == 0 {
        for s in smokes.iter_mut() {
            s.selfish_smoke = None;
        }
    }
    spike.stats.events_per_replay = events_per_replay;
    spike.stats.events_dropped_as_duplicates = dropped;
    let self_entity = roster.iter().find(|(_, r)| r.player == replays.primary.meta.playerName).map(|(e, _)| *e);
    spike.stats.self_entity = self_entity.map(|e| e.raw() as u32);
    spike.stats.self_damage_authoritative = self_entity.map(|_| self_authoritative);
    spike.stats.self_damage_ledger =
        self_entity.map(|e| spike.stats.damage_by_attacker.get(&(e.raw() as u32)).copied().unwrap_or(0.0));
    info!(
        events = spike.stats.damage_events,
        duplicates_dropped = dropped,
        unknown_attacker = spike.stats.events_attacker_unknown,
        hits = spike.stats.shot_hits,
        salvos = spike.stats.salvos,
        "Damage spike"
    );

    let game_record = GameRecord {
        tournament: config.game.tournament.clone(),
        match_id: match_id.clone(),
        round: round.clone(),
        game_no: config.game.game_no,
        map: map_label.clone(),
        map_name: map_name.clone(),
        map_display: map_display.clone(),
        game_build: replays.primary.meta.clientVersionFromExe.clone(),
        primary_replay: primary_replay.clone(),
        merged_replays: merged_replays.clone(),
        outcome: winner_id.map(|w| match w {
            -1 => Outcome::Draw,
            w => Outcome::Win { team_id: i64::from(w), team: team_by_id(i64::from(w)).and_then(|t| t.name.clone()) },
        }),
        finish_type,
        battle_start_s: session.battle_start().seconds(),
        battle_end: battle_end.map(|c| moment(&map, c)),
        replay_end_s: session.total_duration().seconds(),
        replay_truncated: session.truncated(),
        wows_toolkit_rev: WOWS_TOOLKIT_REV.map(str::to_string),
        smoke_signals_version: SMOKE_SIGNALS_VERSION.to_string(),
        generated_at: generated_at.clone(),
        teams,
        caps,
    };

    Ok(Analysis {
        game: game_record,
        smokes,
        clock_map: map,
        timeline: tl,
        damage_events: spike.events,
        damage_stats: spike.stats,
        flag_history: tracker.flag_history().clone(),
        battle_results,
    })
}
