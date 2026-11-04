//! Classification of a smoke: the smoker, how it moved while laying, who
//! the smoke covered, the purposes it served (tactic tags with a priority
//! order), the location relative to the team's spawn and the fleets, and the
//! smokees with how each was detected.

use std::collections::BTreeMap;
use std::collections::HashMap;
use std::collections::HashSet;

use image::DynamicImage;
use wows_minimap_renderer::map_data::MapInfo;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::game_types::VisibilityFlags;
use wowsunpack::game_types::VisionFlag;
use wowsunpack::game_types::WorldPos;

use crate::damage::AttributedDamage;
use crate::damage::SmokeDamage;
use crate::records::Classification;
use crate::records::Coverage;
use crate::records::Movement;
use crate::records::OffensiveRadar;
use crate::records::PurposeTag;
use crate::records::Smokee;
use crate::records::SmokeeDetection;
use crate::records::SmokeeReason;
use crate::records::SmokeType;
use crate::tier2::ConsumableRanges;
use crate::tier2::SmokeTier2;
use crate::timeline;

/// Ships cover map distance at about 2.6 times their listed speed, so a
/// destroyer lays a standard smoke over 2 to 5 km of map.
/// Movement: a displacement under this while laying is stationary.
pub const STATIONARY_M: f32 = 500.0;
/// Movement: a laying path shorter than this is too short to judge.
pub const MOVE_MIN_PATH_M: f32 = 1000.0;
/// Movement: a path at least this long gives high confidence.
pub const MOVE_HIGH_PATH_M: f32 = 2500.0;
/// Movement: pushing below this angle to the enemy group, kiting above its complement.
pub const MOVE_PUSH_ANGLE_DEG: f32 = 60.0;
pub const MOVE_KITE_ANGLE_DEG: f32 = 120.0;
/// Movement: an angle this close to a threshold lowers the confidence one step.
pub const MOVE_ANGLE_MARGIN_DEG: f32 = 15.0;
/// Movement: the enemy group is the centroid of the nearest enemies, this many.
pub const MOVE_ENEMY_GROUP: usize = 3;
/// Coverage: a destroyer within this of an allied cruiser or battleship at laying start is stacked.
pub const STACKED_M: f32 = 2500.0;
/// Purpose: cap control needs a concealed radar activated while covering at
/// least this share of the contested cap.
pub const CAP_CONTROL_PCT: f32 = 90.0;
/// Purpose: a smoke within this of a contested cap's edge on average contests it.
pub const CAP_CONTEST_M: f32 = 1000.0;
/// Purpose: a counter smoke is laid within this of an enemy smoke, this long after it.
pub const COUNTER_SMOKE_M: f32 = 12000.0;
pub const COUNTER_SMOKE_SECONDS: f32 = 45.0;
/// A counter smoke candidate this close to the distance limit is borderline.
pub const COUNTER_SMOKE_MARGIN_M: f32 = 100.0;
/// Purpose: "next to an island" is within this of land.
pub const ISLAND_M: f32 = 1000.0;
/// Purpose: island dive and reposition need at least this displacement under the smoke.
pub const DIVE_MIN_M: f32 = 2000.0;
pub const DIVE_HIGH_M: f32 = 4000.0;
pub const REPOSITION_MIN_M: f32 = 3000.0;
pub const REPOSITION_MEDIUM_M: f32 = 4000.0;
pub const REPOSITION_HIGH_M: f32 = 6000.0;
/// Purpose: the damage purpose needs this much smoke damage.
pub const DAMAGE_QUALIFY: f32 = 20000.0;
/// Smokee: a damage event this close to a covered sample happened while covered.
pub const COVERED_HIT_SECONDS: f32 = 2.0;
/// Purpose: escape needs the smoker's HP at or below this share.
pub const ESCAPE_LOW_HP_PCT: f32 = 50.0;
/// Smokee: an enemy within this is a proximity detection.
pub const PROXIMITY_M: f32 = 2000.0;
/// Lane: the centre band is this share of the map side, either side of the spawn axis.
pub const LANE_CENTER_SHARE: f32 = 0.125;
/// Cap role: along the spawn axis, below this share is home and above its complement is enemy.
pub const CAP_HOME_SHARE: f32 = 0.4;
/// Smokee line-of-fire test: enemies within this of the ally.
pub const LINE_OF_FIRE_M: f32 = 15000.0;
/// Smokee: a shot from behind the smoke covers the shooter at samples this close to the firing moment.
pub const BEHIND_WINDOW_SECONDS: f32 = 4.0;
/// How a smokee was covered, ranked so the best seen wins.
const HOW_LINE_OF_FIRE: u8 = 1;
const HOW_BEHIND: u8 = 2;
const HOW_INSIDE: u8 = 3;

/// Land pixels of the map, from the minimap's land layer.
pub struct LandMask {
    land: Vec<bool>,
    size: u32,
    info: MapInfo,
}

impl LandMask {
    /// `image` is the land layer (alpha marks land); `info` holds the map's size.
    pub fn new(image: &DynamicImage, info: MapInfo) -> Self {
        let rgba = image.to_rgba8();
        let size = rgba.width().min(rgba.height());
        let mut land = vec![false; (size * size) as usize];
        for y in 0..size {
            for x in 0..size {
                land[(y * size + x) as usize] = rgba.get_pixel(x, y).0[3] > 64;
            }
        }
        Self { land, size, info }
    }

    pub fn land_share(&self) -> f32 {
        self.land.iter().filter(|l| **l).count() as f32 / self.land.len().max(1) as f32
    }

    fn is_land(&self, x: i32, y: i32) -> bool {
        x >= 0 && y >= 0 && (x as u32) < self.size && (y as u32) < self.size && self.land[(y as u32 * self.size + x as u32) as usize]
    }

    /// Distance from `pos` to the nearest land pixel in meters, searched out
    /// to `limit_m`; `None` beyond it.
    pub fn distance_to_land_m(&self, pos: WorldPos, limit_m: f32) -> Option<f32> {
        let p = self.info.world_to_minimap(pos, self.size);
        let px_per_wu = self.size as f32 / self.info.space_size as f32;
        let limit_px = (timeline::world_units(limit_m) * px_per_wu).ceil() as i32;
        let (cx, cy) = (p.x.round() as i32, p.y.round() as i32);
        let mut best: Option<f32> = None;
        for dy in -limit_px..=limit_px {
            for dx in -limit_px..=limit_px {
                if self.is_land(cx + dx, cy + dy) {
                    let d = ((dx * dx + dy * dy) as f32).sqrt();
                    if best.is_none_or(|b| d < b) {
                        best = Some(d);
                    }
                }
            }
        }
        best.map(|px| timeline::meters(px / px_per_wu)).filter(|m| *m <= limit_m)
    }
}

/// What the classifier knows about one ship.
pub struct ShipInfo {
    pub team_id: i64,
    pub player: String,
    pub ship: String,
    pub ship_class: Option<String>,
}

/// A consumable run: who, when, how long.
#[derive(Debug, Clone, Copy)]
pub struct Activation {
    pub entity: EntityId,
    pub seconds: f32,
    pub duration: f32,
}

/// Another smoke object in the game, for the counter smoke test.
pub struct OtherSmoke {
    pub id: u32,
    pub team_id: Option<i64>,
    pub created: f32,
    pub origin: WorldPos,
}

/// The game as the classifier sees it.
pub struct GameContext<'a> {
    pub ships: &'a HashMap<EntityId, ShipInfo>,
    pub tl: &'a wows_battle_world::scan::PositionTimeline,
    pub deaths: &'a HashMap<EntityId, f32>,
    pub flags_at: &'a dyn Fn(EntityId, GameClock) -> Option<VisibilityFlags>,
    pub ranges: &'a HashMap<EntityId, ConsumableRanges>,
    /// Caps as (letter, centre, radius in world units).
    pub caps: &'a [(char, WorldPos, f32)],
    /// Spawn centre per team id.
    pub spawns: &'a HashMap<i64, WorldPos>,
    /// Side of the map in world units, when the map's settings were found.
    pub space_size: Option<f32>,
    pub land: Option<&'a LandMask>,
    /// Scores sampled over the game: (seconds, score per team id).
    pub scores: &'a [(f32, Vec<(i64, i64)>)],
    /// HP share sampled over the game, per ship.
    pub hp: &'a HashMap<EntityId, Vec<(f32, f32)>>,
    pub radar_activations: &'a [Activation],
    pub hydro_activations: &'a [Activation],
    pub events: &'a [AttributedDamage],
    pub flag_history: &'a HashMap<EntityId, Vec<(GameClock, VisibilityFlags)>>,
    pub smokes: &'a [OtherSmoke],
}

/// One smoke as the classifier sees it.
pub struct SmokeContext<'a> {
    pub id: u32,
    pub owner: Option<EntityId>,
    pub owner_team: Option<i64>,
    pub smoke_type: Option<SmokeType>,
    pub created: f32,
    pub removed: Option<f32>,
    pub emission_from: f32,
    pub emission_end: Option<f32>,
    pub origin: WorldPos,
    pub radius: f32,
    pub samples: &'a [(GameClock, Vec<WorldPos>)],
    pub tier2: Option<&'a SmokeTier2>,
    pub damage: Option<&'a SmokeDamage>,
    pub selfish: Option<bool>,
    pub contested_cap: Option<char>,
    pub avg_contested_cap_dist_m: Option<f32>,
    pub supported_caps: &'a [String],
    pub offensive_radar: Option<&'a OffensiveRadar>,
    pub offensive_hydro: Option<&'a OffensiveRadar>,
}

fn pos_at(g: &GameContext<'_>, e: EntityId, t: f32) -> Option<WorldPos> {
    g.tl.get(&e).and_then(|tr| timeline::world_pos_at(tr, GameClock(t)))
}

fn alive(g: &GameContext<'_>, e: EntityId, t: f32) -> bool {
    g.deaths.get(&e).is_none_or(|d| *d > t)
}

fn detected(g: &GameContext<'_>, e: EntityId, t: f32) -> bool {
    (g.flags_at)(e, GameClock(t)).is_some_and(|f| f.is_detected())
}

/// Every way `flags` says a ship is spotted, in priority order, with whether
/// the kind is inferred. The ship flag is proximity when an enemy is within
/// `PROXIMITY_M` (`near`), else surface lit.
pub fn detection_kinds(flags: VisibilityFlags, near: bool) -> Vec<(&'static str, bool)> {
    let mut kinds: Vec<(&'static str, bool)> = Vec::new();
    if flags.contains(VisionFlag::Rls) || flags.contains(VisionFlag::RlsPersonal) {
        kinds.push(("radar", false));
    }
    if flags.contains(VisionFlag::Sonar) {
        kinds.push(("hydro", false));
    }
    if flags.contains(VisionFlag::Smoke) {
        kinds.push(("smoke fire penalty", false));
    }
    if flags.contains(VisionFlag::MainPlane) || flags.contains(VisionFlag::MiscPlane) || flags.contains(VisionFlag::Recon) {
        kinds.push(("aircraft", false));
    }
    if flags.contains(VisionFlag::Pinger) || flags.contains(VisionFlag::SubmarineLocator) {
        kinds.push(("submarine", false));
    }
    if flags.contains(VisionFlag::CommonXRay) {
        kinds.push(("proximity", false));
    }
    if flags.contains(VisionFlag::Ship) {
        kinds.push(if near { ("proximity", true) } else { ("surface lit", false) });
    }
    if kinds.is_empty() {
        kinds.push(("other", true));
    }
    kinds
}

/// The one reason a spotted ship is charged with: the first of `detection_kinds`.
pub fn detection_reason(flags: VisibilityFlags, near: bool) -> (&'static str, bool) {
    detection_kinds(flags, near)[0]
}

fn near_enemy(g: &GameContext<'_>, enemy: i64, pos: WorldPos, t: f32) -> bool {
    let proximity = timeline::world_units(PROXIMITY_M);
    ships_of_team(g, enemy).filter(|x| alive(g, *x, t)).filter_map(|x| pos_at(g, x, t)).any(|x| timeline::ground_distance(pos, x) <= proximity)
}

fn centroid(points: &[WorldPos]) -> Option<WorldPos> {
    if points.is_empty() {
        return None;
    }
    let n = points.len() as f32;
    Some(WorldPos::new(
        points.iter().map(|p| p.0.x).sum::<f32>() / n,
        0.0,
        points.iter().map(|p| p.0.z).sum::<f32>() / n,
    ))
}

fn ships_of_team<'a>(g: &'a GameContext<'a>, team: i64) -> impl Iterator<Item = EntityId> + 'a {
    let mut ids: Vec<EntityId> = g.ships.iter().filter(|(_, s)| s.team_id == team).map(|(e, _)| *e).collect();
    ids.sort_by_key(|e| e.raw());
    ids.into_iter()
}

fn enemy_team(g: &GameContext<'_>, ours: i64) -> Option<i64> {
    let mut teams: Vec<i64> = g.ships.values().map(|s| s.team_id).filter(|t| *t != ours).collect();
    teams.sort_unstable();
    teams.first().copied()
}

/// Angle in degrees between two ground vectors.
fn angle_deg(ax: f32, az: f32, bx: f32, bz: f32) -> f32 {
    let dot = ax * bx + az * bz;
    let la = (ax * ax + az * az).sqrt();
    let lb = (bx * bx + bz * bz).sqrt();
    if la <= 0.0 || lb <= 0.0 {
        return 90.0;
    }
    (dot / (la * lb)).clamp(-1.0, 1.0).acos().to_degrees()
}

/// Segment `a`-`b` passes within `radius` of `puff`, with the puff nearer `a`.
fn crosses(a: WorldPos, b: WorldPos, puffs: &[WorldPos], radius: f32) -> bool {
    puffs.iter().any(|puff| {
        segment_distance(a, b, *puff) <= radius && timeline::ground_distance(a, *puff) < timeline::ground_distance(b, *puff)
    })
}

fn segment_distance(a: WorldPos, b: WorldPos, p: WorldPos) -> f32 {
    let (ax, az, bx, bz, px, pz) = (a.0.x, a.0.z, b.0.x, b.0.z, p.0.x, p.0.z);
    let (dx, dz) = (bx - ax, bz - az);
    let len2 = dx * dx + dz * dz;
    let t = if len2 <= 0.0 { 0.0 } else { (((px - ax) * dx + (pz - az) * dz) / len2).clamp(0.0, 1.0) };
    ((px - (ax + dx * t)).powi(2) + (pz - (az + dz * t)).powi(2)).sqrt()
}

fn inside(pos: WorldPos, puffs: &[WorldPos], radius: f32) -> bool {
    puffs.iter().any(|p| timeline::ground_distance(pos, *p) <= radius)
}

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

fn fmt_m(m: f32) -> String {
    if m >= 1000.0 { format!("{:.1} km", m / 1000.0) } else { format!("{m:.0} m") }
}

/// Movement while laying: the smoker's displacement from the start to the
/// end of emission against the direction to the nearest enemies.
pub fn movement(g: &GameContext<'_>, s: &SmokeContext<'_>) -> Option<Movement> {
    let owner = s.owner?;
    let team = s.owner_team?;
    let enemy = enemy_team(g, team)?;
    let t0 = s.emission_from;
    let t1 = s.emission_end.unwrap_or(s.removed.unwrap_or(t0 + 20.0)).max(t0 + 1.0);
    let start = pos_at(g, owner, t0)?;
    let end = pos_at(g, owner, t1)?;
    let mut enemies: Vec<(f32, WorldPos)> = ships_of_team(g, enemy)
        .filter(|e| alive(g, *e, t0))
        .filter_map(|e| pos_at(g, e, t0))
        .map(|p| (timeline::ground_distance(start, p), p))
        .collect();
    enemies.sort_by(|a, b| a.0.total_cmp(&b.0));
    let group: Vec<WorldPos> = enemies.iter().take(MOVE_ENEMY_GROUP).map(|(_, p)| *p).collect();
    let target = centroid(&group)?;
    let path_m = timeline::meters(timeline::ground_distance(start, end));
    let angle = angle_deg(end.0.x - start.0.x, end.0.z - start.0.z, target.0.x - start.0.x, target.0.z - start.0.z);
    let closing_m = timeline::meters(timeline::ground_distance(end, target) - timeline::ground_distance(start, target));
    if path_m < STATIONARY_M {
        let reason = format!("moved only {} while laying", fmt_m(path_m));
        return Some(Movement { label: "stationary".to_string(), confidence: "high".to_string(), path_m, angle_deg: angle, closing_m, reason });
    }
    let label = if angle <= MOVE_PUSH_ANGLE_DEG {
        "pushing"
    } else if angle >= MOVE_KITE_ANGLE_DEG {
        "kiting"
    } else {
        "horizontal"
    };
    let margin = (angle - MOVE_PUSH_ANGLE_DEG).abs().min((angle - MOVE_KITE_ANGLE_DEG).abs());
    let mut level = if path_m >= MOVE_HIGH_PATH_M { 2 } else if path_m >= MOVE_MIN_PATH_M { 1 } else { 0 };
    if margin < MOVE_ANGLE_MARGIN_DEG && level > 0 {
        level -= 1;
    }
    let confidence = ["low", "medium", "high"][level];
    let reason = format!(
        "moved {} while laying at {angle:.0} deg to the nearest {} enemies, {} {}",
        fmt_m(path_m),
        group.len(),
        if closing_m <= 0.0 { "closing" } else { "opening" },
        fmt_m(closing_m.abs())
    );
    Some(Movement { label: label.to_string(), confidence: confidence.to_string(), path_m, angle_deg: angle, closing_m, reason })
}

/// Coverage: stacked over screen over selfish.
pub fn coverage(g: &GameContext<'_>, s: &SmokeContext<'_>, smokees: &[Smokee], owner_class: Option<&str>) -> Coverage {
    let mut stacked_with: Option<(String, f32)> = None;
    if let (Some(owner), Some(team)) = (s.owner, s.owner_team)
        && owner_class == Some("destroyer")
        && let Some(start) = pos_at(g, owner, s.emission_from)
    {
        for e in ships_of_team(g, team).filter(|e| *e != owner && alive(g, *e, s.emission_from)) {
            let info = &g.ships[&e];
            let class = info.ship_class.as_deref().unwrap_or("").to_ascii_lowercase();
            if class != "cruiser" && class != "battleship" {
                continue;
            }
            if let Some(p) = pos_at(g, e, s.emission_from) {
                let d = timeline::meters(timeline::ground_distance(start, p));
                if d <= STACKED_M && stacked_with.as_ref().is_none_or(|(_, best)| d < *best) {
                    stacked_with = Some((format!("{} ({})", info.player, info.ship), d));
                }
            }
        }
    }
    // Shooters credited between samples are listed as smokees but were never seen covered.
    let covered: Vec<&Smokee> = smokees.iter().filter(|m| Some(EntityId::from(m.entity_id)) != s.owner && m.how != "none").collect();
    let screen = !covered.is_empty();
    let selfish = stacked_with.is_none() && !screen;
    let (label, reason) = if let Some((who, d)) = &stacked_with {
        ("stacked", format!("laid within {} of {who}", fmt_m(*d)))
    } else if screen {
        let names: Vec<String> = covered.iter().take(3).map(|m| m.player.clone()).collect();
        ("screen", format!("covered {}{}", names.join(", "), if covered.len() > 3 { " and others" } else { "" }))
    } else {
        ("selfish", "no teammate was inside it or hidden behind it".to_string())
    };
    Coverage { label: label.to_string(), stacked: stacked_with.is_some(), screen, selfish, reason }
}

/// Cover seen for one ally over the smoke's samples.
#[derive(Default)]
struct Cover {
    rank: u8,
    seconds: f32,
    times: Vec<f32>,
    undetected_s: f32,
    detected_s: f32,
    /// Covered seconds while spotted, by (kind, inferred).
    by_reason: BTreeMap<(String, bool), f32>,
    detections: Vec<SmokeeDetection>,
}

/// Smokees: allies inside the smoke, firing undetected from behind it, or
/// with the smoke between them and an enemy in their line of fire, sampled
/// over the smoke's life, with every detection while covered. The smoker
/// and every credited shooter are listed even when never covered at a
/// sample.
pub fn smokees(g: &GameContext<'_>, s: &SmokeContext<'_>) -> Vec<Smokee> {
    let Some(team) = s.owner_team else { return Vec::new() };
    let Some(enemy) = enemy_team(g, team) else { return Vec::new() };
    let behind_fires: Vec<(EntityId, f32)> = g
        .events
        .iter()
        .filter(|e| e.behind_smokes.contains(&s.id) && e.attacker_detected_at_fire == Some(false))
        .map(|e| (EntityId::from(e.attacker), e.fire_seconds))
        .collect();
    let mut covered: BTreeMap<u32, Cover> = BTreeMap::new();
    if let Some(owner) = s.owner.filter(|o| g.ships.contains_key(o)) {
        covered.entry(owner.raw() as u32).or_default();
    }
    for e in s.damage.map(|d| d.shooter_stats.keys().copied().collect::<Vec<_>>()).unwrap_or_default() {
        if g.ships.contains_key(&EntityId::from(e)) {
            covered.entry(e).or_default();
        }
    }
    let mut prev_t: Option<f32> = None;
    let mut prev_covered: HashSet<EntityId> = HashSet::new();
    // The smoker stands in its newest puff while laying; the replay shows
    // the puff some seconds later, by which time a moving destroyer has
    // sailed clear of it. The same fallback for the end as `movement`.
    let laying_end = s.emission_end.unwrap_or(s.removed.unwrap_or(s.emission_from + 20.0));
    for (clock, puffs) in s.samples {
        let t = clock.seconds();
        let dt = prev_t.map(|p| t - p).unwrap_or(0.0);
        prev_t = Some(t);
        let laying = t >= s.emission_from && t <= laying_end;
        let enemies: Vec<WorldPos> = ships_of_team(g, enemy).filter(|e| alive(g, *e, t)).filter_map(|e| pos_at(g, e, t)).collect();
        let mut now_covered: HashSet<EntityId> = HashSet::new();
        for ally in ships_of_team(g, team).filter(|e| alive(g, *e, t)) {
            let Some(pos) = pos_at(g, ally, t) else { continue };
            let owner_laying = laying && s.owner == Some(ally);
            if puffs.is_empty() && !owner_laying {
                continue;
            }
            let rank = if owner_laying || inside(pos, puffs, s.radius) {
                HOW_INSIDE
            } else if behind_fires.iter().any(|(e, f)| *e == ally && (f - t).abs() <= BEHIND_WINDOW_SECONDS) {
                HOW_BEHIND
            } else {
                let reach = timeline::world_units(LINE_OF_FIRE_M);
                if enemies.iter().any(|e| timeline::ground_distance(pos, *e) <= reach && crosses(pos, *e, puffs, s.radius)) {
                    HOW_LINE_OF_FIRE
                } else {
                    continue;
                }
            };
            now_covered.insert(ally);
            let entry = covered.entry(ally.raw() as u32).or_default();
            entry.rank = entry.rank.max(rank);
            let continuous = prev_covered.contains(&ally);
            if continuous {
                entry.seconds += dt;
            }
            entry.times.push(t);
            if let Some(flags) = (g.flags_at)(ally, GameClock(t)) {
                if !flags.is_detected() {
                    if continuous {
                        entry.undetected_s += dt;
                    }
                    continue;
                }
                let near = near_enemy(g, enemy, pos, t);
                let kinds = detection_kinds(flags, near);
                if continuous {
                    entry.detected_s += dt;
                    for (kind, inferred) in &kinds {
                        *entry.by_reason.entry((kind.to_string(), *inferred)).or_default() += dt;
                    }
                }
                for (kind, inferred) in kinds {
                    if !entry.detections.iter().any(|d| d.kind == kind) {
                        entry.detections.push(SmokeeDetection { kind: kind.to_string(), inferred, seconds: t, clock: None });
                    }
                }
            }
        }
        prev_covered = now_covered;
    }
    let mut out: Vec<Smokee> = covered
        .into_iter()
        .map(|(raw, cover)| {
            let e = EntityId::from(raw);
            let info = &g.ships[&e];
            let is_owner = s.owner == Some(e);
            let how = match cover.rank {
                HOW_INSIDE => "inside",
                HOW_BEHIND => "behind",
                HOW_LINE_OF_FIRE => "line_of_fire",
                _ => "none",
            };
            // A shooter credited between samples: where its credited shots came from.
            let role = if is_owner {
                "smoker"
            } else if cover.rank == 0 {
                let fired_inside = g.events.iter().any(|ev| ev.attacker == raw && ev.credited.iter().any(|(id, _)| *id == s.id) && ev.in_smokes.contains(&s.id));
                if fired_inside { "inside" } else { "behind" }
            } else {
                how
            };
            let damage_taken: f32 = g
                .events
                .iter()
                .filter(|ev| ev.victim == raw)
                .filter(|ev| {
                    let i = cover.times.partition_point(|t| *t < ev.damage_seconds);
                    [i.checked_sub(1), Some(i)].iter().flatten().any(|j| cover.times.get(*j).is_some_and(|t| (t - ev.damage_seconds).abs() <= COVERED_HIT_SECONDS))
                })
                .map(|ev| ev.amount)
                .sum::<f32>()
                .max(0.0);
            let known = cover.undetected_s + cover.detected_s;
            let stat = s.damage.and_then(|d| d.shooter_stats.get(&raw));
            Smokee {
                entity_id: raw,
                player: info.player.clone(),
                ship: info.ship.clone(),
                ship_class: info.ship_class.clone(),
                badge: 0,
                role: role.to_string(),
                how: how.to_string(),
                seconds_concealed: cover.seconds,
                undetected_pct: (known > 0.0).then(|| 100.0 * cover.undetected_s / known),
                detected_by: cover.by_reason.iter().map(|((kind, inferred), secs)| SmokeeReason { kind: kind.clone(), inferred: *inferred, seconds: *secs }).collect(),
                detections: cover.detections,
                damage: stat.map(|x| x.damage).unwrap_or(0.0),
                split: stat.map(|x| x.split.to_record()).unwrap_or_default(),
                damage_taken,
                kills: stat.map(|x| x.kills).unwrap_or(0),
            }
        })
        .collect();
    out.sort_by(|a, b| {
        let owner = |m: &Smokee| s.owner == Some(EntityId::from(m.entity_id));
        owner(b)
            .cmp(&owner(a))
            .then(b.damage.total_cmp(&a.damage))
            .then(b.seconds_concealed.total_cmp(&a.seconds_concealed))
            .then(a.entity_id.cmp(&b.entity_id))
    });
    for (i, m) in out.iter_mut().enumerate() {
        m.badge = i as u32 + 1;
    }
    out
}

/// Hydro run from inside the smoke while concealed, mirrored on the radar rule.
pub fn offensive_hydro(g: &GameContext<'_>, s: &SmokeContext<'_>) -> Option<OffensiveRadar> {
    let team = s.owner_team?;
    let enemy = enemy_team(g, team)?;
    let life_end = s.removed.unwrap_or(f32::INFINITY);
    let mut spotted: HashSet<EntityId> = HashSet::new();
    let mut ship: Option<EntityId> = None;
    let mut runs = 0;
    for act in g.hydro_activations {
        let t0 = act.seconds;
        if t0 < s.created || t0 > life_end || g.ships.get(&act.entity).is_none_or(|i| i.team_id != team) {
            continue;
        }
        let Some(t2) = s.tier2 else { continue };
        if !t2.inside_at(t0).contains(&act.entity) || detected(g, act.entity, t0) {
            continue;
        }
        let Some(range) = g.ranges.get(&act.entity).and_then(|r| r.hydro_m) else { continue };
        runs += 1;
        ship.get_or_insert(act.entity);
        for e in ships_of_team(g, enemy) {
            let Some(history) = g.flag_history.get(&e) else { continue };
            let gained = history.windows(2).any(|w| {
                let (c, f) = w[1];
                let t = c.seconds();
                t >= t0
                    && t <= t0 + act.duration
                    && f.contains(VisionFlag::Sonar)
                    && !w[0].1.contains(VisionFlag::Sonar)
                    && matches!((pos_at(g, act.entity, t), pos_at(g, e, t)), (Some(a), Some(b)) if timeline::meters(timeline::ground_distance(a, b)) <= range)
            });
            if gained {
                spotted.insert(e);
            }
        }
    }
    (runs > 0).then(|| OffensiveRadar {
        ship: ship.and_then(|e| g.ships.get(&e)).map(|i| i.player.clone()),
        activations: runs,
        enemies_spotted: spotted.len() as u32,
        inferred: true,
    })
}

/// Best coverage of any cap by a concealed radar ship inside the smoke.
fn best_radar_cap(g: &GameContext<'_>, s: &SmokeContext<'_>) -> Option<(char, f32, String)> {
    let team = s.owner_team?;
    let t2 = s.tier2?;
    let mut best: Option<(char, f32, String)> = None;
    for (clock, puffs) in s.samples {
        if puffs.is_empty() {
            continue;
        }
        let t = clock.seconds();
        for e in t2.inside_at(t).iter().copied() {
            if g.ships.get(&e).is_none_or(|i| i.team_id != team) || detected(g, e, t) {
                continue;
            }
            let Some(radar) = g.ranges.get(&e).and_then(|r| r.radar_m) else { continue };
            let Some(pos) = pos_at(g, e, t) else { continue };
            let radar_wu = timeline::world_units(radar);
            for (letter, centre, radius) in g.caps {
                let d = timeline::ground_distance(pos, *centre);
                let pct = (circle_intersection_area(radar_wu, *radius, d) / (std::f32::consts::PI * radius * radius) * 100.0).clamp(0.0, 100.0);
                if best.as_ref().is_none_or(|(_, b, _)| pct > *b) {
                    best = Some((*letter, pct, g.ships[&e].player.clone()));
                }
            }
        }
    }
    best
}

/// Cap control: a radar activated by a concealed ship inside the smoke while
/// its radar covered at least `CAP_CONTROL_PCT` of the contested cap. Returns
/// the cap, the coverage at the activation and the ship.
fn radar_cap_control(g: &GameContext<'_>, s: &SmokeContext<'_>) -> Option<(char, f32, String)> {
    let team = s.owner_team?;
    let t2 = s.tier2?;
    let cap = s.contested_cap?;
    let (letter, centre, radius) = g.caps.iter().find(|(l, _, _)| *l == cap)?;
    let life_end = s.removed.unwrap_or(f32::INFINITY);
    let mut best: Option<(char, f32, String)> = None;
    for act in g.radar_activations {
        let t0 = act.seconds;
        if t0 < s.created || t0 > life_end || g.ships.get(&act.entity).is_none_or(|i| i.team_id != team) {
            continue;
        }
        if !t2.inside_at(t0).contains(&act.entity) || detected(g, act.entity, t0) {
            continue;
        }
        let Some(radar) = g.ranges.get(&act.entity).and_then(|r| r.radar_m) else { continue };
        let Some(pos) = pos_at(g, act.entity, t0) else { continue };
        let radar_wu = timeline::world_units(radar);
        let d = timeline::ground_distance(pos, *centre);
        let pct = (circle_intersection_area(radar_wu, *radius, d) / (std::f32::consts::PI * radius * radius) * 100.0).clamp(0.0, 100.0);
        if pct >= CAP_CONTROL_PCT && best.as_ref().is_none_or(|(_, b, _)| pct > *b) {
            best = Some((*letter, pct, g.ships[&act.entity].player.clone()));
        }
    }
    best
}

/// A ship's displacement under the smoke: positions at its first and last
/// covered sample, and whether it stayed undetected throughout.
struct CoveredMove {
    entity: EntityId,
    start: WorldPos,
    end: WorldPos,
    undetected: bool,
}

fn covered_moves(g: &GameContext<'_>, s: &SmokeContext<'_>, smokees: &[Smokee]) -> Vec<CoveredMove> {
    let Some(team) = s.owner_team else { return Vec::new() };
    let Some(enemy) = enemy_team(g, team) else { return Vec::new() };
    let mut out = Vec::new();
    for m in smokees {
        let e = EntityId::from(m.entity_id);
        let mut first: Option<WorldPos> = None;
        let mut last: Option<WorldPos> = None;
        let mut undetected = true;
        for (clock, puffs) in s.samples {
            let t = clock.seconds();
            if puffs.is_empty() || !alive(g, e, t) {
                continue;
            }
            let Some(pos) = pos_at(g, e, t) else { continue };
            let reach = timeline::world_units(LINE_OF_FIRE_M);
            let covered = inside(pos, puffs, s.radius)
                || ships_of_team(g, enemy)
                    .filter(|x| alive(g, *x, t))
                    .filter_map(|x| pos_at(g, x, t))
                    .any(|x| timeline::ground_distance(pos, x) <= reach && crosses(pos, x, puffs, s.radius));
            if !covered {
                continue;
            }
            first.get_or_insert(pos);
            last = Some(pos);
            if detected(g, e, t) {
                undetected = false;
            }
        }
        if let (Some(start), Some(end)) = (first, last) {
            out.push(CoveredMove { entity: e, start, end, undetected });
        }
    }
    out
}

/// The full classification of one smoke.
pub fn classify(g: &GameContext<'_>, s: &SmokeContext<'_>, smokees: &[Smokee]) -> Classification {
    let owner_info = s.owner.and_then(|e| g.ships.get(&e));
    let smoker_class = owner_info.and_then(|i| i.ship_class.as_ref()).map(|c| c.to_ascii_lowercase());
    let mut special = Vec::new();
    if owner_info.is_some_and(|i| i.ship == "Svea") {
        special.push("svea".to_string());
    }
    if smoker_class.as_deref() == Some("battleship") {
        match s.smoke_type {
            Some(SmokeType::Exhaust) => special.push("battleship_exhaust".to_string()),
            Some(SmokeType::Crawling) => special.push("battleship_crawling".to_string()),
            _ => {}
        }
    }
    let movement = movement(g, s);
    let coverage = coverage(g, s, smokees, smoker_class.as_deref());

    let mut purposes: Vec<PurposeTag> = Vec::new();
    let mut tag = |tag: &str, confidence: Option<&str>, reason: String| {
        purposes.push(PurposeTag { tag: tag.to_string(), confidence: confidence.map(str::to_string), reason });
    };

    // Cap control, else cap contest.
    let radar_cap = best_radar_cap(g, s);
    let cap_control = radar_cap_control(g, s);
    if let Some((cap, pct, who)) = &cap_control {
        tag("cap_control", None, format!("{who} activated radar from inside the smoke while concealed, covering {pct:.0}% of contested cap {cap}"));
    } else if let (Some(cap), Some(d)) = (s.contested_cap, s.avg_contested_cap_dist_m)
        && d <= CAP_CONTEST_M
    {
        let where_ = if d <= 0.0 { "inside".to_string() } else { format!("{} from the edge of", fmt_m(d)) };
        let radar_note = radar_cap.as_ref().map(|(c, pct, _)| format!("; best concealed radar coverage {pct:.0}% of cap {c}")).unwrap_or_default();
        tag("cap_contest", None, format!("on average {where_} contested cap {cap}{radar_note}"));
    }
    // Radar and hydro traps.
    if cap_control.is_none() && let Some(o) = s.offensive_radar.filter(|o| o.enemies_spotted > 0) {
        tag("radar_trap", None, format!("{} spotted {} enemies with radar run from inside the smoke", o.ship.clone().unwrap_or_else(|| "a radar ship".to_string()), o.enemies_spotted));
    }
    if let Some(o) = s.offensive_hydro.filter(|o| o.enemies_spotted > 0) {
        tag("hydro_trap", None, format!("{} spotted {} enemies with hydro run from inside the smoke", o.ship.clone().unwrap_or_else(|| "a hydro ship".to_string()), o.enemies_spotted));
    }
    // Counter smoke.
    let mut counter_smoke_of = None;
    if let Some(team) = s.owner_team {
        let reach = timeline::world_units(COUNTER_SMOKE_M);
        let mut candidates: Vec<&OtherSmoke> = g
            .smokes
            .iter()
            .filter(|o| o.id != s.id && o.team_id.is_some_and(|t| t != team))
            .filter(|o| s.created - o.created >= 0.0 && s.created - o.created <= COUNTER_SMOKE_SECONDS)
            .filter(|o| timeline::ground_distance(o.origin, s.origin) <= reach)
            .collect();
        let distance = |o: &OtherSmoke| timeline::ground_distance(o.origin, s.origin);
        candidates.sort_by(|a, b| distance(a).total_cmp(&distance(b)).then(a.id.cmp(&b.id)));
        if let Some(o) = candidates.first() {
            counter_smoke_of = Some(o.id);
            let d_m = timeline::meters(distance(o));
            let borderline = if COUNTER_SMOKE_M - d_m <= COUNTER_SMOKE_MARGIN_M { " (borderline)" } else { "" };
            tag("counter_smoke", None, format!("laid {:.0} s after enemy smoke {} and {} from it{borderline}", s.created - o.created, o.id, fmt_m(d_m)));
        }
    }
    // Island dive and reposition from the covered moves.
    let moves = covered_moves(g, s, smokees);
    let mut dive: Option<(String, String, String)> = None;
    let mut reposition: Option<(String, String, String)> = None;
    for m in &moves {
        let moved = timeline::meters(timeline::ground_distance(m.start, m.end));
        let name = g.ships.get(&m.entity).map(|i| format!("{} ({})", i.player, i.ship)).unwrap_or_default();
        if let Some(land) = g.land
            && moved >= DIVE_MIN_M
        {
            let end_land = land.distance_to_land_m(m.end, ISLAND_M);
            let start_land = land.distance_to_land_m(m.start, ISLAND_M);
            if let Some(end_d) = end_land
                && (start_land.is_none() || moved >= DIVE_HIGH_M)
            {
                let conf = if moved >= DIVE_HIGH_M && end_d <= ISLAND_M * 0.6 {
                    "high"
                } else if moved >= DIVE_MIN_M * 1.5 {
                    "medium"
                } else {
                    "low"
                };
                let reason = format!("{name} moved {} under the smoke and ended {} from land", fmt_m(moved), fmt_m(end_d));
                if dive.as_ref().is_none_or(|(_, c, _)| rank(conf) > rank(c)) {
                    dive = Some((name.clone(), conf.to_string(), reason));
                }
            }
        }
        if moved >= REPOSITION_MIN_M && m.undetected {
            let conf = if moved >= REPOSITION_HIGH_M {
                "high"
            } else if moved >= REPOSITION_MEDIUM_M {
                "medium"
            } else {
                "low"
            };
            let reason = format!("{name} moved {} while covered and never detected", fmt_m(moved));
            if reposition.as_ref().is_none_or(|(_, c, _)| rank(conf) > rank(c)) {
                reposition = Some((name, conf.to_string(), reason));
            }
        }
    }
    if let Some((_, conf, reason)) = &dive {
        tag("island_dive", Some(conf), reason.clone());
    }
    if let Some((_, conf, reason)) = &reposition {
        tag("reposition", Some(conf), reason.clone());
    }
    // Damage.
    let total = s.damage.map(|d| d.smoke_damage_total()).unwrap_or(0.0);
    let targets: Vec<(u32, f32)> = s
        .damage
        .map(|d| d.targets.iter().filter(|(_, t)| t.damage > 0.0).map(|(e, t)| (*e, t.damage)).collect())
        .unwrap_or_default();
    let damage_20k = total >= DAMAGE_QUALIFY;
    let damage_qualified = damage_20k || targets.len() >= 2;
    let mut damage_label = None;
    if total > 0.0 {
        let (label, conf, reason) = if targets.len() >= 2 {
            ("target_rich", None, format!("{} damage on {} enemies", total.round(), targets.len()))
        } else if let Some((victim, dmg)) = targets.first().copied() {
            let victim_pos = s.damage.and_then(|d| d.arrows.iter().find(|a| a.victim == victim && a.attacker_ally).map(|a| WorldPos::new(a.to.x, 0.0, a.to.z)));
            let land = victim_pos.and_then(|p| g.land.and_then(|l| l.distance_to_land_m(p, ISLAND_M * 2.0)));
            let who = g.ships.get(&EntityId::from(victim)).map(|i| format!("{} ({})", i.player, i.ship)).unwrap_or_default();
            match land {
                Some(d) if d <= ISLAND_M => ("island_killer", Some(if d <= ISLAND_M * 0.5 { "high" } else { "medium" }), format!("{dmg:.0} damage on {who}, parked {} from land", fmt_m(d))),
                Some(d) => ("hunt", Some(if d >= ISLAND_M * 1.5 { "high" } else { "medium" }), format!("{dmg:.0} damage on {who} in the open, {} from land", fmt_m(d))),
                None if victim_pos.is_some() && g.land.is_some() => ("hunt", Some("high"), format!("{dmg:.0} damage on {who} in open water")),
                None => ("hunt", Some("low"), format!("{dmg:.0} damage on {who}; its position or the land layer is unknown")),
            }
        } else {
            ("hunt", Some("low"), format!("{} damage with no target recorded", total.round()))
        };
        damage_label = Some(label.to_string());
        if damage_20k {
            tag("damage", conf, format!("{label}: {reason}"));
        }
    }
    // Escape.
    if let (Some(owner), Some(team), Some(mv)) = (s.owner, s.owner_team, movement.as_ref()) {
        let t0 = s.emission_from;
        let spotted = detected(g, owner, t0);
        let hp = g.hp.get(&owner).and_then(|h| {
            let idx = h.partition_point(|(t, _)| *t <= t0);
            idx.checked_sub(1).and_then(|i| h.get(i)).map(|(_, pct)| *pct)
        });
        let low_hp = hp.is_some_and(|pct| pct <= ESCAPE_LOW_HP_PCT);
        let losing = g.scores.iter().rev().find(|(t, _)| *t <= t0).and_then(|(_, scores)| {
            let ours = scores.iter().find(|(id, _)| *id == team).map(|(_, v)| *v)?;
            let theirs = scores.iter().find(|(id, _)| *id != team).map(|(_, v)| *v)?;
            Some(ours < theirs)
        });
        let conditions = [spotted, low_hp, losing == Some(true)].iter().filter(|c| **c).count();
        if mv.label == "kiting" && (spotted || low_hp || losing == Some(true)) {
            let conf = if conditions >= 2 && mv.confidence == "high" {
                "high"
            } else if (spotted || low_hp) && mv.confidence != "low" {
                "medium"
            } else {
                "low"
            };
            let mut why: Vec<String> = Vec::new();
            if spotted {
                why.push("spotted at activation".to_string());
            }
            if let Some(pct) = hp.filter(|_| low_hp) {
                why.push(format!("HP {pct:.0}%"));
            }
            if losing == Some(true) {
                why.push("behind on points".to_string());
            }
            tag("escape", Some(conf), format!("kiting while {}", why.join(", ")));
        }
    }
    let primary_purpose = purposes.first().map(|p| p.tag.clone());

    // Location: lane and cap role from the spawn axis, front line from the fleets.
    let (mut lane, mut lane_offset_m, mut cap_role, mut cap_role_cap, mut cap_flank) = (None, None, None, None, None);
    let (mut frontline_distance_m, mut nearest_enemy_m) = (None, None);
    if let Some(team) = s.owner_team
        && let Some(enemy) = enemy_team(g, team)
    {
        if let (Some(own), Some(theirs), Some(space)) = (g.spawns.get(&team), g.spawns.get(&enemy), g.space_size) {
            let (ax, az) = (theirs.0.x - own.0.x, theirs.0.z - own.0.z);
            let len = (ax * ax + az * az).sqrt();
            if len > 0.0 {
                let (ux, uz) = (ax / len, az / len);
                let (rx, rz) = (uz, -ux);
                let lateral = |p: WorldPos| (p.0.x - own.0.x) * rx + (p.0.z - own.0.z) * rz;
                let along = |p: WorldPos| ((p.0.x - own.0.x) * ux + (p.0.z - own.0.z) * uz) / len;
                let band = space * LANE_CENTER_SHARE;
                let off = lateral(s.origin);
                lane_offset_m = Some(timeline::meters(off));
                lane = Some(if off.abs() <= band { "center" } else if off > 0.0 { "right" } else { "left" }.to_string());
                let cap = s
                    .contested_cap
                    .and_then(|c| g.caps.iter().find(|(l, _, _)| *l == c))
                    .or_else(|| g.caps.iter().min_by(|a, b| timeline::ground_distance(a.1, s.origin).total_cmp(&timeline::ground_distance(b.1, s.origin))));
                if let Some((letter, centre, _)) = cap {
                    let t = along(*centre);
                    cap_role = Some(if t < CAP_HOME_SHARE { "home" } else if t > 1.0 - CAP_HOME_SHARE { "enemy" } else { "center" }.to_string());
                    cap_role_cap = Some(letter.to_string());
                    cap_flank = Some(lateral(*centre).abs() > band);
                }
            }
        }
        let t0 = s.emission_from;
        let ours: Vec<WorldPos> = ships_of_team(g, team).filter(|e| alive(g, *e, t0)).filter_map(|e| pos_at(g, e, t0)).collect();
        let theirs: Vec<WorldPos> = ships_of_team(g, enemy).filter(|e| alive(g, *e, t0)).filter_map(|e| pos_at(g, e, t0)).collect();
        if let (Some(a), Some(b)) = (centroid(&ours), centroid(&theirs)) {
            let mid = WorldPos::new((a.0.x + b.0.x) / 2.0, 0.0, (a.0.z + b.0.z) / 2.0);
            let (ax, az) = (b.0.x - a.0.x, b.0.z - a.0.z);
            let len = (ax * ax + az * az).sqrt();
            if len > 0.0 {
                frontline_distance_m = Some(timeline::meters(((s.origin.0.x - mid.0.x) * ax + (s.origin.0.z - mid.0.z) * az) / len));
            }
        }
        nearest_enemy_m = theirs.iter().map(|p| timeline::meters(timeline::ground_distance(s.origin, *p))).min_by(|a, b| a.total_cmp(b));
    }
    let land_distance_m = g.land.and_then(|l| l.distance_to_land_m(s.origin, ISLAND_M * 5.0));

    Classification {
        smoker_class,
        special,
        movement,
        coverage,
        purposes,
        primary_purpose,
        damage_20k,
        damage_qualified,
        damage_label,
        lane,
        lane_offset_m,
        cap_role,
        cap_role_cap,
        cap_flank,
        frontline_distance_m,
        nearest_enemy_m,
        caps_in_range: s.supported_caps.to_vec(),
        counter_smoke_of,
        land_distance_m,
    }
}

fn rank(confidence: &str) -> u8 {
    match confidence {
        "high" => 2,
        "medium" => 1,
        _ => 0,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn angles_between_ground_vectors() {
        assert!((angle_deg(1.0, 0.0, 1.0, 0.0)).abs() < 0.01);
        assert!((angle_deg(1.0, 0.0, -1.0, 0.0) - 180.0).abs() < 0.01);
        assert!((angle_deg(1.0, 0.0, 0.0, 1.0) - 90.0).abs() < 0.01);
    }

    #[test]
    fn a_puff_on_the_shooters_side_crosses() {
        let a = WorldPos::new(0.0, 0.0, 0.0);
        let b = WorldPos::new(100.0, 0.0, 0.0);
        assert!(crosses(a, b, &[WorldPos::new(20.0, 0.0, 5.0)], 15.0));
        assert!(!crosses(a, b, &[WorldPos::new(80.0, 0.0, 5.0)], 15.0));
        assert!(!crosses(a, b, &[WorldPos::new(20.0, 0.0, 50.0)], 15.0));
    }

    #[test]
    fn detection_reason_prefers_radar_and_infers_proximity() {
        let radar_and_ship = VisibilityFlags::new(VisionFlag::Rls.bit() | VisionFlag::Ship.bit());
        assert_eq!(detection_reason(radar_and_ship, true), ("radar", false));
        let ship = VisibilityFlags::new(VisionFlag::Ship.bit());
        assert_eq!(detection_reason(ship, true), ("proximity", true));
        assert_eq!(detection_reason(ship, false), ("surface lit", false));
        let smoke = VisibilityFlags::new(VisionFlag::Smoke.bit());
        assert_eq!(detection_kinds(smoke, false), vec![("smoke fire penalty", false)]);
        assert_eq!(detection_kinds(VisibilityFlags::new(1 << 20), false), vec![("other", true)]);
    }

    #[test]
    fn land_distance_from_a_small_mask() {
        let mut img = image::RgbaImage::new(100, 100);
        for y in 40..60 {
            for x in 40..60 {
                img.put_pixel(x, y, image::Rgba([0, 0, 0, 255]));
            }
        }
        let mask = LandMask::new(&DynamicImage::ImageRgba8(img), MapInfo { space_size: 1000 });
        assert!(mask.land_share() > 0.03 && mask.land_share() < 0.05);
        let centre = mask.distance_to_land_m(WorldPos::new(0.0, 0.0, 0.0), 5000.0);
        assert_eq!(centre, Some(0.0));
        let far = mask.distance_to_land_m(WorldPos::new(-450.0, 0.0, 0.0), 2000.0);
        assert!(far.is_none());
    }
}
