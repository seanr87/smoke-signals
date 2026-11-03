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
use crate::records::Bbox;
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
use crate::timeline;

/// Farthest a ship may be from a smoke's origin at creation and still own it.
pub const OWNER_MAX_DISTANCE: f32 = 50.0;

/// Longest gap between a smoke activation and the smoke object's creation.
pub const ACTIVATION_WINDOW_SECONDS: f32 = 5.0;

/// Farthest a ship that activated smoke in the window may be from the origin
/// and still be preferred over a nearer unactivated ship. A held position is
/// up to 10 s old, and a destroyer covers about 180 m in that time.
pub const OWNER_ACTIVATED_MAX_DISTANCE: f32 = 200.0;

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
    Some(SmokeFit {
        smoke_type: classify(&slot.variant_name, category.icon_id()),
        variant: slot.variant_name.clone(),
        work_time: category.work_time(),
        puff_life: fields.get("lifeTime").copied(),
        radius: fields.get("radius").copied(),
        charges_total,
    })
}

/// Smoke type from the variant's name and icon. Every smoke consumable has
/// consumableType `smokeGenerator`; only the variant tells them apart.
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

fn team_label(config: &Config, player_name: &str) -> String {
    if player_name.starts_with(&config.run.team_prefix) {
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
    Roster {
        team: team_label(config, &name),
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

/// Side of the map a team spawned on, from the mean of its first positions.
/// `None` when no ship of the team has a position.
fn spawn_side(timeline: &wows_battle_world::scan::PositionTimeline, entities: &[EntityId]) -> Option<String> {
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
    let (x, z) = (sum.0 / n as f32, sum.1 / n as f32);
    let side = if z.abs() >= x.abs() {
        if z >= 0.0 { "north" } else { "south" }
    } else if x >= 0.0 {
        "east"
    } else {
        "west"
    };
    Some(side.to_string())
}

pub fn analyze_game(config: &Config, game: &GameData, replays: &ReplaySet) -> Result<Analysis, Report> {
    let mut session = GameSession::new(game, replays)?;
    let mut tracks: BTreeMap<EntityId, SmokeTrack> = BTreeMap::new();
    let mut seen_activations: HashSet<(EntityId, u32)> = HashSet::new();
    let mut activations: Vec<Activation> = Vec::new();

    while session.step()?.is_some() {
        let view = session.view();
        let clock = view.clock();
        let smokes = view.smoke_screens();
        for (id, state) in &smokes {
            tracks.entry(*id).or_insert_with(|| SmokeTrack::new(clock, state)).observe(clock, state);
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
            }
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
    let tl = session.timeline_arc();
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
    drop(view);

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
                        death: deaths.get(e).map(|c| moment(&map, *c)),
                    }
                })
                .collect();
            TeamRecord {
                name: team_name(*team_id),
                team_id: *team_id,
                spawn_side: spawn_side(&tl, &entities),
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
                Some((*entity, timeline::ground_distance(pos, track.origin), source, activated(*entity).copied()))
            })
            .collect();
        candidates.sort_by(|a, b| a.1.total_cmp(&b.1));
        let chosen = candidates
            .iter()
            .find(|c| c.3.is_some() && c.1 <= OWNER_ACTIVATED_MAX_DISTANCE)
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
                } else if d > OWNER_MAX_DISTANCE {
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
            Some(SmokeType::Standard) | None => match track.first_fade {
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
        let path = match smoke_type {
            Some(SmokeType::Exhaust) | Some(SmokeType::Crawling) => {
                Some(track.puffs.iter().map(|(_, p)| Xz { x: p.0.x, z: p.0.z }).collect())
            }
            _ => None,
        };
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
            wows_toolkit_rev: WOWS_TOOLKIT_REV.map(str::to_string),
            smoke_signals_version: SMOKE_SIGNALS_VERSION.to_string(),
            generated_at: generated_at.clone(),
            frame_cap: None,
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
            let (life_a, life_b) = (smokes[i].base_puff_life_s, smokes[j].base_puff_life_s);
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

    let game_record = GameRecord {
        match_id: match_id.clone(),
        round: round.clone(),
        game_no: config.game.game_no,
        map: map_label.clone(),
        map_name: map_name.clone(),
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
    };

    Ok(Analysis { game: game_record, smokes, clock_map: map, timeline: tl })
}
