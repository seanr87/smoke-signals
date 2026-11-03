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
    Some(tier2::ConsumableRanges { radar_m: range(Consumable::Radar), hydro_m: range(Consumable::HydroacousticSearch) })
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

    while session.step()?.is_some() {
        let view = session.view();
        let clock = view.clock();
        let smokes = view.smoke_screens();
        for (id, state) in &smokes {
            tracks.entry(*id).or_insert_with(|| SmokeTrack::new(clock, state)).observe(clock, state);
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
    let tier2_results = tier2.finish_keep_history();
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
            cap_depth_pct: None,
            selfish_smoke: None,
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

    // Tier 2: ships in the smoke and detections while concealed.
    let (tracker, per_smoke) = tier2_results;
    let name_of = |e: u32| roster.get(&EntityId::from(e)).map(|r| r.player.clone());
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
    let flags_at = |e: EntityId, c: GameClock| tracker.flags_at(e, c);
    let team_of = |e: EntityId| roster.get(&e).map(|r| r.team_id);
    let mut spike = damage::run(&damage::SpikeInput {
        ledger: &ledger,
        hits: &hits,
        salvos: &salvo_list,
        smokes: &geometry,
        timeline: &tl,
        flags_at: &flags_at,
        team_of: &team_of,
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
            smokes[i].damage_detail = Some(d);
        }
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
