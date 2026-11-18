//! Per-game timelines written beside the smoke records: cap owner and invader
//! changes, radar and hydro activations with the enemies they lit, ship
//! tracks with health, the score, and the recording player's cap ribbons.
//!
//! Every row carries three times. `t_s` is the replay clock of the run's
//! primary replay, the clock of the `t_*` columns in `smokes.csv`.
//! `elapsed_s` is `t_s` minus that replay's battle start, so it is the same
//! moment in both runs of a game. `clock` is the HUD countdown.

use std::collections::BTreeMap;
use std::collections::HashMap;
use std::fmt::Write as _;
use std::path::Path;

use rootcause::prelude::*;
use serde::Serialize;
use wows_battle_world::scan::PositionTimeline;
use wows_battle_world::view::BattleView;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::game_types::Ribbon;
use wowsunpack::game_types::VisibilityFlags;
use wowsunpack::game_types::VisionFlag;
use wowsunpack::game_types::WorldPos;

use crate::clock::BattleClockMap;
use crate::output::csv_line;
use crate::output::opt;
use crate::state;
use crate::tier2::ConsumableRanges;
use crate::tier2::SmokeTier2;
use crate::timeline;
use crate::timeline::PosSource;

/// Spacing of the track, health and score samples.
pub const TRACK_STEP_SECONDS: f32 = 2.0;

/// Spacing of the range checks inside a lit interval.
const LIT_CHECK_STEP_SECONDS: f32 = 1.0;

/// A target this far past the nominal range still counts as in range. Ship
/// positions are interpolated, so a target on the edge can sample just outside.
const RANGE_TOLERANCE: f32 = 1.03;

/// An in-smoke evaluation older than this says nothing about the moment asked.
const INSIDE_MAX_AGE_SECONDS: f32 = 1.0;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct CapState {
    /// Owning team id, negative when neutral.
    owner: i64,
    invader: Option<i64>,
}

/// What changed on a cap between two packets.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CapChange {
    /// First time the cap was seen.
    Initial,
    Owner,
    Invader,
    OwnerAndInvader,
}

impl CapChange {
    fn as_str(self) -> &'static str {
        match self {
            Self::Initial => "initial",
            Self::Owner => "owner",
            Self::Invader => "invader",
            Self::OwnerAndInvader => "owner+invader",
        }
    }
}

#[derive(Debug, Clone, Copy)]
struct CapEvent {
    clock: GameClock,
    index: usize,
    change: CapChange,
    state: CapState,
    previous: Option<CapState>,
}

#[derive(Debug, Clone)]
struct Sample {
    clock: GameClock,
    /// `(team index, score)`, sorted.
    scores: Vec<(i64, i64)>,
    /// `(ship, health, max health)`, sorted by ship.
    health: Vec<(EntityId, f32, f32)>,
}

#[derive(Debug, Clone, Copy)]
struct RibbonGain {
    clock: GameClock,
    ribbon: Ribbon,
    count: usize,
}

/// Fed every packet of the analysis pass. Reads the view only.
#[derive(Debug, Default)]
pub struct Collector {
    cap_state: BTreeMap<usize, CapState>,
    /// Where each cap stood when first seen. A cap disabled before the end
    /// of the replay is missing from the final view.
    cap_positions: BTreeMap<usize, WorldPos>,
    cap_events: Vec<CapEvent>,
    ribbon_totals: BTreeMap<Ribbon, usize>,
    ribbon_gains: Vec<RibbonGain>,
    samples: Vec<Sample>,
    next_sample: Option<f32>,
}

impl Collector {
    pub fn observe(&mut self, clock: GameClock, view: &BattleView<'_>) {
        let mut caps: Vec<(usize, WorldPos, CapState)> = view
            .capture_points()
            .iter()
            .filter(|cp| cp.is_enabled && crate::analysis::is_capture_zone(cp))
            .filter_map(|cp| {
                let state = CapState { owner: cp.team_id, invader: cp.has_invaders.then_some(cp.invader_team) };
                Some((cp.index, cp.position?, state))
            })
            .collect();
        caps.sort_by_key(|(i, _, _)| *i);
        for (index, position, state) in caps {
            self.cap_positions.entry(index).or_insert(position);
            self.observe_cap(clock, index, state);
        }

        // A ribbon absent from the totals stands at zero, so its baseline
        // falls with it.
        let totals = view.self_ribbons();
        for ribbon in [Ribbon::Defended, Ribbon::Captured, Ribbon::AssistedInCapture] {
            self.observe_ribbon(clock, ribbon, totals.get(&ribbon).copied().unwrap_or(0));
        }

        if self.next_sample.is_none_or(|t| clock.seconds() >= t) {
            self.next_sample = Some(clock.seconds() + TRACK_STEP_SECONDS);
            let mut scores: Vec<(i64, i64)> = view.team_scores().iter().map(|s| (s.team_index as i64, s.score)).collect();
            scores.sort_unstable();
            let mut health: Vec<(EntityId, f32, f32)> = view
                .vehicle_props_all()
                .iter()
                .filter(|(_, p)| p.max_health() > 0.0)
                .map(|(e, p)| (*e, p.health(), p.max_health()))
                .collect();
            health.sort_by_key(|(e, _, _)| e.raw());
            self.samples.push(Sample { clock, scores, health });
        }
    }

    fn observe_cap(&mut self, clock: GameClock, index: usize, state: CapState) {
        let previous = self.cap_state.insert(index, state);
        let change = match previous {
            None => CapChange::Initial,
            Some(p) if p == state => return,
            Some(p) => match (p.owner != state.owner, p.invader != state.invader) {
                (true, true) => CapChange::OwnerAndInvader,
                (true, false) => CapChange::Owner,
                _ => CapChange::Invader,
            },
        };
        self.cap_events.push(CapEvent { clock, index, change, state, previous });
    }

    /// `(cap index, position)` of every capture zone seen, lowest index first.
    pub fn cap_positions(&self) -> Vec<(usize, WorldPos)> {
        self.cap_positions.iter().map(|(i, p)| (*i, *p)).collect()
    }

    /// Largest maximum health sampled per ship.
    pub fn max_health(&self) -> HashMap<EntityId, f32> {
        let mut out: HashMap<EntityId, f32> = HashMap::new();
        for sample in &self.samples {
            for (e, _, m) in &sample.health {
                let best = out.entry(*e).or_insert(*m);
                if *m > *best {
                    *best = *m;
                }
            }
        }
        out
    }

    /// The view holds running totals; a rise is one or more ribbons earned.
    /// A fall is the replay rebasing a slot and earns nothing.
    fn observe_ribbon(&mut self, clock: GameClock, ribbon: Ribbon, total: usize) {
        let previous = self.ribbon_totals.insert(ribbon, total).unwrap_or(0);
        if total > previous {
            self.ribbon_gains.push(RibbonGain { clock, ribbon, count: total - previous });
        }
    }
}

/// One ship of the game, for labelling rows.
#[derive(Debug, Clone)]
pub struct ShipInfo {
    pub entity: EntityId,
    pub team_id: i64,
    pub team: String,
    pub player: String,
    pub ship: String,
}

/// One team, for the team-frame cap letters.
#[derive(Debug, Clone)]
pub struct TeamInfo {
    pub team_id: i64,
    pub name: String,
    pub spawn: Option<WorldPos>,
    pub spawn_side: Option<String>,
}

/// A radar or hydro activation: ship, start, seconds active.
#[derive(Debug, Clone, Copy)]
pub struct SensorUse {
    pub entity: EntityId,
    pub clock: GameClock,
    pub duration: f32,
}

/// Everything `finish` needs that the collector did not see itself.
pub struct Context<'a> {
    pub match_id: &'a str,
    pub game_no: Option<u32>,
    pub primary_replay: &'a str,
    /// The other replays merged into the session.
    pub merged_replays: &'a [String],
    pub clock_map: &'a BattleClockMap,
    pub timeline: &'a PositionTimeline,
    pub flag_history: &'a HashMap<EntityId, Vec<(GameClock, VisibilityFlags)>>,
    pub ranges: &'a HashMap<EntityId, ConsumableRanges>,
    pub deaths: &'a HashMap<EntityId, GameClock>,
    pub per_smoke: &'a HashMap<u32, SmokeTier2>,
    pub radar: &'a [SensorUse],
    pub hydro: &'a [SensorUse],
    /// `(cap index, position)` of the enabled capture zones.
    pub caps: &'a [(usize, WorldPos)],
    pub ships: &'a [ShipInfo],
    pub teams: &'a [TeamInfo],
    /// The ship of the primary replay's recording player.
    pub recorder: Option<EntityId>,
    /// Last replay clock processed.
    pub end: GameClock,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SensorKind {
    Radar,
    Hydro,
}

impl SensorKind {
    fn as_str(self) -> &'static str {
        match self {
            Self::Radar => "radar",
            Self::Hydro => "hydro",
        }
    }

    fn flag(self) -> VisionFlag {
        match self {
            Self::Radar => VisionFlag::Rls,
            Self::Hydro => VisionFlag::Sonar,
        }
    }

    fn range_m(self, ranges: &ConsumableRanges) -> Option<f32> {
        match self {
            Self::Radar => ranges.radar_m,
            Self::Hydro => ranges.hydro_m,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct Meta {
    pub match_id: String,
    pub game_no: Option<u32>,
    /// Replay whose clock `t_s` is.
    pub clock_replay: String,
    pub merged_replays: Vec<String>,
    /// The game has one replay: the other team is seen only through it.
    pub one_sided: bool,
    pub battle_start_s: f32,
    pub step_s: f32,
    pub time_base: &'static str,
    pub teams: Vec<MetaTeam>,
    pub recorder_entity_id: Option<u32>,
    pub files: Vec<&'static str>,
}

#[derive(Debug, Clone, Serialize)]
pub struct MetaTeam {
    pub team_id: i64,
    pub name: String,
    pub spawn_side: Option<String>,
    /// Real cap letter to this team's frame letter, e.g. `A:C`. `None`
    /// when the frame cannot be told.
    pub cap_frame: Option<Vec<String>>,
}

/// The finished timelines of one run, as CSV text.
#[derive(Debug, Clone)]
pub struct Timelines {
    pub meta: Meta,
    pub caps_csv: String,
    pub radar_csv: String,
    pub tracks_csv: String,
    pub score_csv: String,
    pub ribbons_csv: String,
}

/// Flags of `ship` as last reported at or before `clock`.
fn flags_at(history: &HashMap<EntityId, Vec<(GameClock, VisibilityFlags)>>, ship: EntityId, clock: GameClock) -> Option<VisibilityFlags> {
    let list = history.get(&ship)?;
    let idx = list.partition_point(|(c, _)| c.seconds() <= clock.seconds());
    idx.checked_sub(1).map(|i| list[i].1)
}

/// Spans `[start, end)` over which `ship` carried `flag`. An open span ends
/// at the ship's death or at `end`.
fn flag_spans(
    history: &HashMap<EntityId, Vec<(GameClock, VisibilityFlags)>>,
    ship: EntityId,
    flag: VisionFlag,
    end: f32,
) -> Vec<(f32, f32)> {
    let mut spans = Vec::new();
    let mut open: Option<f32> = None;
    for (clock, flags) in history.get(&ship).map(Vec::as_slice).unwrap_or(&[]) {
        match (open, flags.contains(flag)) {
            (None, true) => open = Some(clock.seconds()),
            (Some(start), false) => {
                spans.push((start, clock.seconds()));
                open = None;
            }
            _ => {}
        }
    }
    if let Some(start) = open
        && end > start
    {
        spans.push((start, end));
    }
    spans
}

/// Smokes `ship` stood in at `seconds`, lowest id first.
fn smokes_holding(per_smoke: &HashMap<u32, SmokeTier2>, ship: EntityId, seconds: f32) -> Vec<u32> {
    let mut ids: Vec<u32> = per_smoke
        .iter()
        .filter(|(_, s)| {
            let idx = s.inside_history.partition_point(|(c, _)| *c <= seconds);
            idx.checked_sub(1)
                .and_then(|i| s.inside_history.get(i))
                .is_some_and(|(c, inside)| seconds - *c <= INSIDE_MAX_AGE_SECONDS && inside.contains(&ship))
        })
        .map(|(id, _)| *id)
        .collect();
    ids.sort_unstable();
    ids
}

/// Reflection of `p` across the line halfway between the two spawns.
fn mirror_across_midline(p: WorldPos, a: WorldPos, b: WorldPos) -> WorldPos {
    let (dx, dz) = (b.0.x - a.0.x, b.0.z - a.0.z);
    let len2 = dx * dx + dz * dz;
    if len2 <= f32::EPSILON {
        return p;
    }
    let (mx, mz) = ((a.0.x + b.0.x) / 2.0, (a.0.z + b.0.z) / 2.0);
    let along = ((p.0.x - mx) * dx + (p.0.z - mz) * dz) / len2;
    WorldPos::new(p.0.x - 2.0 * along * dx, 0.0, p.0.z - 2.0 * along * dz)
}

/// The team whose frame is the map as drawn: the south spawn, or the west
/// one when the spawns are east and west.
fn is_base_side(side: Option<&str>) -> bool {
    matches!(side, Some("south") | Some("west"))
}

/// Cap letters in `team`'s frame: the map mirrored across the midline when
/// the team spawns on the far side, so its spawn is at the bottom. A mirror,
/// not a turn: west stays west. The base team keeps the real letters; the
/// other team gets the letter of the cap nearest each cap's mirror image.
///
/// `None` when the frame cannot be told: a spawn is unknown, both teams are
/// on the same side, or the mirrored caps do not land one to one on caps.
fn cap_frame(team: &TeamInfo, teams: &[TeamInfo], caps: &[(usize, WorldPos)]) -> Option<BTreeMap<usize, char>> {
    let other = teams.iter().find(|t| t.team_id != team.team_id)?;
    let (own, far) = (team.spawn?, other.spawn?);
    let (own_base, other_base) = (is_base_side(team.spawn_side.as_deref()), is_base_side(other.spawn_side.as_deref()));
    if own_base == other_base {
        return None;
    }
    if own_base {
        return Some(caps.iter().map(|(i, _)| (*i, state::cap_letter(*i))).collect());
    }
    let mut seen: BTreeMap<usize, usize> = BTreeMap::new();
    for (index, pos) in caps {
        let m = mirror_across_midline(*pos, own, far);
        let nearest =
            caps.iter().min_by(|x, y| timeline::ground_distance(x.1, m).total_cmp(&timeline::ground_distance(y.1, m)))?;
        seen.insert(*index, nearest.0);
    }
    let mut images: Vec<usize> = seen.values().copied().collect();
    images.sort_unstable();
    images.dedup();
    (images.len() == caps.len()).then(|| seen.into_iter().map(|(i, s)| (i, state::cap_letter(s))).collect())
}

fn f2(v: f32) -> String {
    format!("{v:.2}")
}

fn f1(v: f32) -> String {
    format!("{v:.1}")
}

impl Collector {
    pub fn finish(self, ctx: &Context<'_>) -> Timelines {
        let start = ctx.clock_map.battle_start().seconds();
        let game_no = opt(ctx.game_no);
        let ships: HashMap<EntityId, &ShipInfo> = ctx.ships.iter().map(|s| (s.entity, s)).collect();
        let team_name = |id: i64| ctx.teams.iter().find(|t| t.team_id == id).map(|t| t.name.clone());
        // game id, then the three times of a row.
        let stamp = |t: f32| -> Vec<String> {
            vec![ctx.match_id.to_string(), game_no.clone(), f2(t), f2(t - start), opt(ctx.clock_map.at(GameClock(t)))]
        };
        let ship_cols = |e: EntityId| -> Vec<String> {
            match ships.get(&e) {
                Some(s) => vec![e.raw().to_string(), s.player.clone(), s.ship.clone(), s.team.clone()],
                None => vec![e.raw().to_string(), String::new(), String::new(), String::new()],
            }
        };
        let alive_at = |e: EntityId, t: f32| ctx.deaths.get(&e).is_none_or(|d| d.seconds() > t);
        let pos_at = |e: EntityId, t: f32| ctx.timeline.get(&e).and_then(|track| timeline::ship_pos_at(track, GameClock(t)));
        let source_name = |s: PosSource| match s {
            PosSource::World => "exact",
            PosSource::Minimap => "minimap",
        };

        let frames: Vec<Option<BTreeMap<usize, char>>> =
            ctx.teams.iter().map(|t| cap_frame(t, ctx.teams, ctx.caps)).collect();

        let mut caps_csv = String::from("match_id,game_no,t_s,elapsed_s,clock,cap,");
        for i in 0..ctx.teams.len() {
            let _ = write!(caps_csv, "frame_team_{i},cap_frame_{i},");
        }
        caps_csv.push_str("change,owner,owner_team_id,invader,invader_team_id,previous_owner,previous_invader\n");
        let owner_name = |id: i64| if id < 0 { String::new() } else { team_name(id).unwrap_or_else(|| id.to_string()) };
        for ev in &self.cap_events {
            let mut row = stamp(ev.clock.seconds());
            row.push(state::cap_letter(ev.index).to_string());
            for (team, frame) in ctx.teams.iter().zip(&frames) {
                row.push(team.name.clone());
                row.push(opt(frame.as_ref().and_then(|f| f.get(&ev.index))));
            }
            row.push(ev.change.as_str().to_string());
            row.push(owner_name(ev.state.owner));
            row.push(if ev.state.owner < 0 { String::new() } else { ev.state.owner.to_string() });
            row.push(ev.state.invader.map(owner_name).unwrap_or_default());
            row.push(opt(ev.state.invader));
            row.push(ev.previous.map(|p| owner_name(p.owner)).unwrap_or_default());
            row.push(ev.previous.and_then(|p| p.invader).map(owner_name).unwrap_or_default());
            caps_csv.push_str(&csv_line(&row));
            caps_csv.push('\n');
        }

        let radar_csv = self.sensor_csv(ctx, &stamp, &ship_cols, &alive_at, &pos_at, &source_name);

        let mut tracks_csv = String::from(
            "match_id,game_no,t_s,elapsed_s,clock,entity_id,player,ship,team,x,z,pos_source,alive,detected,health,max_health\n",
        );
        let mut score_csv = String::from("match_id,game_no,t_s,elapsed_s,clock,team_id,team,score\n");
        let mut order: Vec<EntityId> = ctx.ships.iter().map(|s| s.entity).collect();
        order.sort_by_key(|e| e.raw());
        for sample in &self.samples {
            let t = sample.clock.seconds();
            let health: HashMap<EntityId, (f32, f32)> = sample.health.iter().map(|(e, h, m)| (*e, (*h, *m))).collect();
            for e in &order {
                let pos = pos_at(*e, t);
                let mut row = stamp(t);
                row.extend(ship_cols(*e));
                row.push(pos.map(|(p, _)| f1(p.0.x)).unwrap_or_default());
                row.push(pos.map(|(p, _)| f1(p.0.z)).unwrap_or_default());
                row.push(pos.map(|(_, s)| source_name(s).to_string()).unwrap_or_default());
                row.push(alive_at(*e, t).to_string());
                row.push(opt(flags_at(ctx.flag_history, *e, sample.clock).map(|f| f.is_detected())));
                row.push(health.get(e).map(|(h, _)| format!("{h:.0}")).unwrap_or_default());
                row.push(health.get(e).map(|(_, m)| format!("{m:.0}")).unwrap_or_default());
                tracks_csv.push_str(&csv_line(&row));
                tracks_csv.push('\n');
            }
            for (team_id, score) in &sample.scores {
                let mut row = stamp(t);
                row.push(team_id.to_string());
                row.push(team_name(*team_id).unwrap_or_default());
                row.push(score.to_string());
                score_csv.push_str(&csv_line(&row));
                score_csv.push('\n');
            }
        }

        let mut ribbons_csv =
            String::from("match_id,game_no,t_s,elapsed_s,clock,entity_id,player,ship,team,ribbon,count,replay\n");
        for gain in &self.ribbon_gains {
            let mut row = stamp(gain.clock.seconds());
            match ctx.recorder {
                Some(e) => row.extend(ship_cols(e)),
                None => row.extend(vec![String::new(); 4]),
            }
            row.push(format!("{:?}", gain.ribbon));
            row.push(gain.count.to_string());
            row.push(ctx.primary_replay.to_string());
            ribbons_csv.push_str(&csv_line(&row));
            ribbons_csv.push('\n');
        }

        let meta = Meta {
            match_id: ctx.match_id.to_string(),
            game_no: ctx.game_no,
            clock_replay: ctx.primary_replay.to_string(),
            merged_replays: ctx.merged_replays.to_vec(),
            one_sided: ctx.merged_replays.is_empty(),
            battle_start_s: start,
            step_s: TRACK_STEP_SECONDS,
            time_base: "t_s is the replay clock of clock_replay, the clock of the t_* columns in that run's smokes.csv. \
                        elapsed_s = t_s - battle_start_s and is the same moment in both runs of the game; add the other \
                        run's battle_start_s (its game.json) to get that run's t_s. clock is the HUD countdown.",
            teams: ctx
                .teams
                .iter()
                .zip(&frames)
                .map(|(t, frame)| MetaTeam {
                    team_id: t.team_id,
                    name: t.name.clone(),
                    spawn_side: t.spawn_side.clone(),
                    cap_frame: frame
                        .as_ref()
                        .map(|f| f.iter().map(|(i, c)| format!("{}:{c}", state::cap_letter(*i))).collect()),
                })
                .collect(),
            recorder_entity_id: ctx.recorder.map(|e| e.raw() as u32),
            files: vec!["caps_timeline.csv", "radar.csv", "tracks.csv", "score.csv"],
        };
        Timelines { meta, caps_csv, radar_csv, tracks_csv, score_csv, ribbons_csv }
    }

    /// One `activation` row per radar or hydro use, one `lit` row per enemy
    /// it lit, and one `lit_unattributed` row per flag span no activation in
    /// range explains. The replay says a ship is lit, not by whom: a ship is
    /// credited to every activation of the other side that had it in range
    /// while it carried the flag, and `ambiguous` marks more than one.
    fn sensor_csv(
        &self,
        ctx: &Context<'_>,
        stamp: &dyn Fn(f32) -> Vec<String>,
        ship_cols: &dyn Fn(EntityId) -> Vec<String>,
        alive_at: &dyn Fn(EntityId, f32) -> bool,
        pos_at: &dyn Fn(EntityId, f32) -> Option<(WorldPos, PosSource)>,
        source_name: &dyn Fn(PosSource) -> &'static str,
    ) -> String {
        let start = ctx.clock_map.battle_start().seconds();
        let team_of: HashMap<EntityId, i64> = ctx.ships.iter().map(|s| (s.entity, s.team_id)).collect();
        let mut csv = String::from(
            "match_id,game_no,t_s,elapsed_s,clock,kind,row,activation_id,entity_id,player,ship,team,x,z,pos_source,\
             range_m,duration_s,end_elapsed_s,source_in_smoke,target_entity_id,target_player,target_ship,target_team,\
             lit_start_elapsed_s,lit_end_elapsed_s,target_x,target_z,target_pos_source,target_distance_m,\
             target_min_distance_m,target_in_smoke,ambiguous,other_sources\n",
        );
        let join = |ids: &[u32]| ids.iter().map(|i| i.to_string()).collect::<Vec<_>>().join(";");
        let blank = |n: usize| vec![String::new(); n];
        for (kind, uses) in [(SensorKind::Radar, ctx.radar), (SensorKind::Hydro, ctx.hydro)] {
            let mut targets: Vec<EntityId> = ctx.ships.iter().map(|s| s.entity).collect();
            targets.sort_by_key(|e| e.raw());
            // (target, span index) pairs explained by at least one activation.
            let mut explained: Vec<(EntityId, usize)> = Vec::new();
            // Per activation: the enemies in range while flagged.
            struct Lit {
                target: EntityId,
                span: usize,
                from: f32,
                to: f32,
                first_distance_m: f32,
                min_distance_m: f32,
            }
            let spans: HashMap<EntityId, Vec<(f32, f32)>> = targets
                .iter()
                .map(|e| {
                    let end = ctx.deaths.get(e).map(|d| d.seconds()).unwrap_or(ctx.end.seconds());
                    (*e, flag_spans(ctx.flag_history, *e, kind.flag(), end))
                })
                .collect();
            let lit_by = |u: &SensorUse| -> Vec<Lit> {
                let Some(range_m) = ctx.ranges.get(&u.entity).and_then(|r| kind.range_m(r)) else { return Vec::new() };
                let Some(team) = team_of.get(&u.entity) else { return Vec::new() };
                let (a0, a1) = (u.clock.seconds(), u.clock.seconds() + u.duration);
                let mut out = Vec::new();
                for target in &targets {
                    if team_of.get(target) == Some(team) || !team_of.contains_key(target) {
                        continue;
                    }
                    for (i, (s0, s1)) in spans[target].iter().enumerate() {
                        let (from, to) = (s0.max(a0), s1.min(a1));
                        // Written so a NaN bound is skipped too.
                        if !(to > from) {
                            continue;
                        }
                        let mut first: Option<(f32, f32)> = None;
                        let mut last = from;
                        let mut min = f32::INFINITY;
                        let mut t = from;
                        loop {
                            if let (Some((sp, _)), Some((tp, _))) = (pos_at(u.entity, t), pos_at(*target, t)) {
                                let d = timeline::meters(timeline::ground_distance(sp, tp));
                                if d <= range_m * RANGE_TOLERANCE {
                                    first.get_or_insert((t, d));
                                    last = t;
                                    min = min.min(d);
                                }
                            }
                            if t >= to {
                                break;
                            }
                            t = (t + LIT_CHECK_STEP_SECONDS).min(to);
                        }
                        if let Some((first_t, first_d)) = first {
                            out.push(Lit {
                                target: *target,
                                span: i,
                                from: first_t,
                                to: last,
                                first_distance_m: first_d,
                                min_distance_m: min,
                            });
                        }
                    }
                }
                out
            };
            let lits: Vec<Vec<Lit>> = uses.iter().map(lit_by).collect();
            for (ui, u) in uses.iter().enumerate() {
                let t0 = u.clock.seconds();
                let activation_id = format!("{}_{}_{:.0}", kind.as_str(), u.entity.raw(), (t0 - start) * 10.0);
                let source_pos = pos_at(u.entity, t0);
                let mut head = stamp(t0);
                head.push(kind.as_str().to_string());
                let mut tail = vec![activation_id];
                tail.extend(ship_cols(u.entity));
                tail.push(source_pos.map(|(p, _)| f1(p.0.x)).unwrap_or_default());
                tail.push(source_pos.map(|(p, _)| f1(p.0.z)).unwrap_or_default());
                tail.push(source_pos.map(|(_, s)| source_name(s).to_string()).unwrap_or_default());
                tail.push(opt(ctx.ranges.get(&u.entity).and_then(|r| kind.range_m(r)).map(|m| format!("{m:.0}"))));
                tail.push(f2(u.duration));
                tail.push(f2(t0 + u.duration - start));
                tail.push(join(&smokes_holding(ctx.per_smoke, u.entity, t0)));
                let mut row = head.clone();
                row.push("activation".to_string());
                row.extend(tail.clone());
                row.extend(blank(14));
                csv.push_str(&csv_line(&row));
                csv.push('\n');
                for lit in &lits[ui] {
                    explained.push((lit.target, lit.span));
                    // Other activations of the same kind, by the same side,
                    // with the same target in range over an overlapping time.
                    let others: Vec<u32> = uses
                        .iter()
                        .enumerate()
                        .filter(|(oi, o)| *oi != ui && o.entity != u.entity)
                        .filter(|(oi, _)| lits[*oi].iter().any(|l| l.target == lit.target && l.from <= lit.to && lit.from <= l.to))
                        .map(|(_, o)| o.entity.raw() as u32)
                        .collect();
                    let target_pos = pos_at(lit.target, lit.from);
                    let mut row = head.clone();
                    row.push("lit".to_string());
                    row.extend(tail.clone());
                    row.extend(ship_cols(lit.target));
                    row.push(f2(lit.from - start));
                    row.push(f2(lit.to - start));
                    row.push(target_pos.map(|(p, _)| f1(p.0.x)).unwrap_or_default());
                    row.push(target_pos.map(|(p, _)| f1(p.0.z)).unwrap_or_default());
                    row.push(target_pos.map(|(_, s)| source_name(s).to_string()).unwrap_or_default());
                    row.push(format!("{:.0}", lit.first_distance_m));
                    row.push(format!("{:.0}", lit.min_distance_m));
                    row.push(join(&smokes_holding(ctx.per_smoke, lit.target, lit.from)));
                    row.push((!others.is_empty()).to_string());
                    row.push(join(&others));
                    csv.push_str(&csv_line(&row));
                    csv.push('\n');
                }
            }
            for target in &targets {
                for (i, (s0, s1)) in spans[target].iter().enumerate() {
                    if explained.contains(&(*target, i)) || !alive_at(*target, *s0) {
                        continue;
                    }
                    let target_pos = pos_at(*target, *s0);
                    let mut row = stamp(*s0);
                    row.push(kind.as_str().to_string());
                    row.push("lit_unattributed".to_string());
                    row.extend(blank(12));
                    row.extend(ship_cols(*target));
                    row.push(f2(s0 - start));
                    row.push(f2(s1 - start));
                    row.push(target_pos.map(|(p, _)| f1(p.0.x)).unwrap_or_default());
                    row.push(target_pos.map(|(p, _)| f1(p.0.z)).unwrap_or_default());
                    row.push(target_pos.map(|(_, s)| source_name(s).to_string()).unwrap_or_default());
                    row.extend(blank(2));
                    row.push(join(&smokes_holding(ctx.per_smoke, *target, *s0)));
                    row.extend(blank(2));
                    csv.push_str(&csv_line(&row));
                    csv.push('\n');
                }
            }
        }
        csv
    }
}

impl Timelines {
    /// The files written once per game: caps, radar and hydro, tracks, score.
    pub fn write_game_files(&self, dir: &Path) -> Result<(), Report> {
        std::fs::create_dir_all(dir).attach_with(|| format!("creating {}", dir.display()))?;
        crate::output::write_json(&dir.join("meta.json"), &self.meta)?;
        for (name, text) in [
            ("caps_timeline.csv", &self.caps_csv),
            ("radar.csv", &self.radar_csv),
            ("tracks.csv", &self.tracks_csv),
            ("score.csv", &self.score_csv),
        ] {
            let path = dir.join(name);
            std::fs::write(&path, text).attach_with(|| format!("writing {}", path.display()))?;
        }
        Ok(())
    }

    /// The file written once per run: the recording player's cap ribbons.
    pub fn write_run_files(&self, dir: &Path) -> Result<(), Report> {
        let path = dir.join("ribbons.csv");
        std::fs::write(&path, &self.ribbons_csv).attach_with(|| format!("writing {}", path.display()))?;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn flags(bits: &[VisionFlag]) -> VisibilityFlags {
        VisibilityFlags::new(bits.iter().fold(0u32, |acc, f| acc | (1 << (*f as u32))))
    }

    #[test]
    fn cap_changes_are_logged_once() {
        let mut c = Collector::default();
        let neutral = CapState { owner: -1, invader: None };
        let invaded = CapState { owner: -1, invader: Some(1) };
        let taken = CapState { owner: 1, invader: None };
        c.observe_cap(GameClock(10.0), 0, neutral);
        c.observe_cap(GameClock(11.0), 0, neutral);
        c.observe_cap(GameClock(12.0), 0, invaded);
        c.observe_cap(GameClock(13.0), 0, invaded);
        c.observe_cap(GameClock(40.0), 0, taken);
        let changes: Vec<CapChange> = c.cap_events.iter().map(|e| e.change).collect();
        assert_eq!(changes, vec![CapChange::Initial, CapChange::Invader, CapChange::OwnerAndInvader]);
        assert_eq!(c.cap_events[2].previous, Some(invaded));
    }

    #[test]
    fn ribbon_totals_become_gains() {
        let mut c = Collector::default();
        c.observe_ribbon(GameClock(5.0), Ribbon::Captured, 1);
        c.observe_ribbon(GameClock(6.0), Ribbon::Captured, 1);
        c.observe_ribbon(GameClock(9.0), Ribbon::Captured, 3);
        c.observe_ribbon(GameClock(9.5), Ribbon::Captured, 2);
        let gains: Vec<(f32, usize)> = c.ribbon_gains.iter().map(|g| (g.clock.seconds(), g.count)).collect();
        assert_eq!(gains, vec![(5.0, 1), (9.0, 2)]);
    }

    #[test]
    fn flag_spans_close_on_loss_and_at_the_end() {
        let ship = EntityId::from(7u32);
        let mut history = HashMap::new();
        history.insert(
            ship,
            vec![
                (GameClock(10.0), flags(&[VisionFlag::Ship])),
                (GameClock(20.0), flags(&[VisionFlag::Ship, VisionFlag::Rls])),
                (GameClock(31.0), flags(&[VisionFlag::Ship])),
                (GameClock(50.0), flags(&[VisionFlag::Rls])),
            ],
        );
        assert_eq!(flag_spans(&history, ship, VisionFlag::Rls, 60.0), vec![(20.0, 31.0), (50.0, 60.0)]);
        assert_eq!(flag_spans(&history, ship, VisionFlag::Sonar, 60.0), vec![]);
        assert!(flags_at(&history, ship, GameClock(25.0)).is_some_and(|f| f.contains(VisionFlag::Rls)));
        assert!(flags_at(&history, ship, GameClock(5.0)).is_none());
    }

    #[test]
    fn mirror_swaps_the_two_sides() {
        let (a, b) = (WorldPos::new(0.0, 0.0, 300.0), WorldPos::new(0.0, 0.0, -300.0));
        let m = mirror_across_midline(WorldPos::new(120.0, 0.0, 80.0), a, b);
        assert!((m.0.x - 120.0).abs() < 1e-3 && (m.0.z + 80.0).abs() < 1e-3);
        // Diagonal spawns: north-east and south-west mirror across the other diagonal.
        let (a, b) = (WorldPos::new(300.0, 0.0, 300.0), WorldPos::new(-300.0, 0.0, -300.0));
        let m = mirror_across_midline(WorldPos::new(100.0, 0.0, 20.0), a, b);
        assert!((m.0.x + 20.0).abs() < 1e-3 && (m.0.z + 100.0).abs() < 1e-3);
    }

    #[test]
    fn the_far_team_sees_mirrored_letters() {
        let caps = vec![(0usize, WorldPos::new(-200.0, 0.0, 150.0)), (1usize, WorldPos::new(-200.0, 0.0, -150.0))];
        let teams = vec![
            TeamInfo { team_id: 0, name: "N".into(), spawn: Some(WorldPos::new(0.0, 0.0, 400.0)), spawn_side: Some("north".into()) },
            TeamInfo { team_id: 1, name: "S".into(), spawn: Some(WorldPos::new(0.0, 0.0, -400.0)), spawn_side: Some("south".into()) },
        ];
        let north = cap_frame(&teams[0], &teams, &caps).expect("north frame");
        let south = cap_frame(&teams[1], &teams, &caps).expect("south frame");
        assert_eq!((north[&0], north[&1]), ('B', 'A'));
        assert_eq!((south[&0], south[&1]), ('A', 'B'));
    }

    #[test]
    fn no_frame_without_two_distinct_sides() {
        let caps = vec![(0usize, WorldPos::new(-200.0, 0.0, 150.0)), (1usize, WorldPos::new(-200.0, 0.0, -150.0))];
        let team = |id: i64, z: f32, side: &str| TeamInfo {
            team_id: id,
            name: id.to_string(),
            spawn: Some(WorldPos::new(0.0, 0.0, z)),
            spawn_side: Some(side.into()),
        };
        let same = vec![team(0, 400.0, "north"), team(1, 300.0, "north")];
        assert!(cap_frame(&same[0], &same, &caps).is_none());
        let mut unknown = vec![team(0, 400.0, "north"), team(1, -400.0, "south")];
        unknown[1].spawn = None;
        assert!(cap_frame(&unknown[0], &unknown, &caps).is_none());
        // Two caps whose mirror images land on the same cap.
        let skewed = vec![(0usize, WorldPos::new(0.0, 0.0, 0.0)), (1usize, WorldPos::new(0.0, 0.0, 60.0)), (2usize, WorldPos::new(0.0, 0.0, -300.0))];
        let teams = vec![team(0, 400.0, "north"), team(1, -400.0, "south")];
        assert!(cap_frame(&teams[0], &teams, &skewed).is_none());
    }

    #[test]
    fn a_ribbon_that_leaves_the_totals_restarts_from_zero() {
        let mut c = Collector::default();
        c.observe_ribbon(GameClock(5.0), Ribbon::Defended, 2);
        c.observe_ribbon(GameClock(6.0), Ribbon::Defended, 0);
        c.observe_ribbon(GameClock(7.0), Ribbon::Defended, 1);
        let gains: Vec<(f32, usize)> = c.ribbon_gains.iter().map(|g| (g.clock.seconds(), g.count)).collect();
        assert_eq!(gains, vec![(5.0, 2), (7.0, 1)]);
    }
}
