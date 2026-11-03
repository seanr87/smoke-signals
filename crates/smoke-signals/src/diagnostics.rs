//! Evidence written next to the smoke table: smoke activations as each replay
//! recorded them, and how much of each ship's position track the merged
//! timeline holds.

use std::collections::HashMap;
use std::path::Path;

use rootcause::prelude::*;
use serde::Serialize;
use wows_battle_world::scan::PositionTimeline;
use wows_battle_world::scan::ScanCollector;
use wows_battle_world::scan::scan_replay;
use wows_replays::analyzer::decoder::DecodedPacketPayload;
use wows_replays::packet2::Packet;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::game_types::Consumable;
use wowsunpack::game_types::VisibilityFlags;
use wowsunpack::game_types::VisionFlag;
use wowsunpack::recognized::Recognized;

use crate::clock::BattleClockMap;
use crate::output::csv_line;
use crate::output::opt;
use crate::records::GameRecord;
use crate::records::Moment;
use crate::replays::ReplaySet;
use crate::session::GameData;

/// One smoke activation as one replay recorded it. The player fields are
/// `None` when the entity is not on the arena roster.
#[derive(Debug, Clone, Serialize)]
pub struct ActivationRecord {
    pub source: String,
    pub entity_id: u32,
    pub player: Option<String>,
    pub ship: Option<String>,
    pub team: Option<String>,
    pub t: Moment,
    pub duration_s: f32,
}

#[derive(Default)]
struct SmokeActivationCollector {
    seen: Vec<(GameClock, EntityId, f32)>,
}

impl ScanCollector for SmokeActivationCollector {
    fn observe(&mut self, packet: &Packet<'_, '_>, decoded: &DecodedPacketPayload<'_, '_, '_>) {
        if let DecodedPacketPayload::Consumable { entity, consumable, duration, .. } = decoded
            && *consumable == Recognized::Known(Consumable::Smoke)
        {
            self.seen.push((packet.clock, *entity, *duration));
        }
    }
}

/// Smoke activations from every replay, primary first.
pub fn scan_activations(
    game: &GameData,
    replays: &ReplaySet,
    roster: &GameRecord,
    map: &BattleClockMap,
) -> Vec<ActivationRecord> {
    let by_entity: HashMap<u32, (&str, &str, Option<&str>)> = roster
        .teams
        .iter()
        .flat_map(|t| {
            t.players.iter().map(move |p| (p.entity_id, (p.player.as_str(), p.ship.as_str(), t.name.as_deref())))
        })
        .collect();
    let mut sources: Vec<(String, &wows_replays::ReplayFile)> = vec![("primary".to_string(), &replays.primary)];
    sources.extend(replays.merges.iter().enumerate().map(|(i, r)| (format!("merge{}", i + 1), r)));
    let mut out = Vec::new();
    for (source, replay) in sources {
        let mut collector = SmokeActivationCollector::default();
        scan_replay(&game.loaded.specs, &game.constants, game.version, replay, &mut [&mut collector]);
        for (clock, entity, duration) in collector.seen {
            let id = entity.raw() as u32;
            let known = by_entity.get(&id).copied();
            out.push(ActivationRecord {
                source: source.clone(),
                entity_id: id,
                player: known.map(|(p, _, _)| p.to_string()),
                ship: known.map(|(_, s, _)| s.to_string()),
                team: known.and_then(|(_, _, t)| t.map(str::to_string)),
                t: Moment { seconds: clock.seconds(), clock: map.at(clock) },
                duration_s: duration,
            });
        }
    }
    out.sort_by(|a, b| a.t.seconds.total_cmp(&b.t.seconds).then_with(|| a.source.cmp(&b.source)));
    out
}

pub fn write_activations_csv(path: &Path, activations: &[ActivationRecord]) -> Result<(), Report> {
    let mut text = String::from("source,entity_id,player,ship,team,t,t_clock,duration_s\n");
    for a in activations {
        let row = vec![
            a.source.clone(),
            a.entity_id.to_string(),
            opt(a.player.as_deref()),
            opt(a.ship.as_deref()),
            opt(a.team.as_deref()),
            format!("{:.2}", a.t.seconds),
            a.t.clock_text(),
            format!("{:.1}", a.duration_s),
        ];
        text.push_str(&csv_line(&row));
        text.push('\n');
    }
    std::fs::write(path, text).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}

/// Coverage of one ship's world-position track in the merged timeline.
#[derive(Debug, Clone, Serialize)]
pub struct TrackSummary {
    pub entity_id: u32,
    pub player: String,
    pub ship: String,
    pub team: Option<String>,
    pub world_samples: usize,
    pub minimap_samples: usize,
    pub first_s: Option<f32>,
    pub last_s: Option<f32>,
    /// Longest gap between consecutive world samples, and where it starts.
    pub max_gap_s: Option<f32>,
    pub max_gap_at_s: Option<f32>,
    /// Visibility flag changes seen for the ship, and how often each flag was gained.
    pub flag_changes: usize,
    pub rls_gains: usize,
    pub sonar_gains: usize,
    pub smoke_gains: usize,
}

pub type FlagHistory = HashMap<EntityId, Vec<(GameClock, VisibilityFlags)>>;

fn gains(history: &[(GameClock, VisibilityFlags)], flag: VisionFlag) -> usize {
    history.windows(2).filter(|w| w[1].1.contains(flag) && !w[0].1.contains(flag)).count()
        + usize::from(history.first().is_some_and(|(_, f)| f.contains(flag)))
}

pub fn summarize_tracks(timeline: &PositionTimeline, roster: &GameRecord, flags: &FlagHistory) -> Vec<TrackSummary> {
    let mut out = Vec::new();
    for team in &roster.teams {
        for p in &team.players {
            let history = flags.get(&EntityId::from(p.entity_id)).map(Vec::as_slice).unwrap_or(&[]);
            let track = timeline.get(&EntityId::from(p.entity_id));
            let world = track.map(|t| t.world.as_slice()).unwrap_or(&[]);
            let mut max_gap: Option<(f32, f32)> = None;
            for w in world.windows(2) {
                let gap = w[1].0.seconds() - w[0].0.seconds();
                if max_gap.is_none_or(|(g, _)| gap > g) {
                    max_gap = Some((gap, w[0].0.seconds()));
                }
            }
            out.push(TrackSummary {
                entity_id: p.entity_id,
                player: p.player.clone(),
                ship: p.ship.clone(),
                team: team.name.clone(),
                world_samples: world.len(),
                minimap_samples: track.map(|t| t.minimap.len()).unwrap_or(0),
                first_s: world.first().map(|(c, _)| c.seconds()),
                last_s: world.last().map(|(c, _)| c.seconds()),
                max_gap_s: max_gap.map(|(g, _)| g),
                max_gap_at_s: max_gap.map(|(_, at)| at),
                flag_changes: history.len(),
                rls_gains: gains(history, VisionFlag::Rls),
                sonar_gains: gains(history, VisionFlag::Sonar),
                smoke_gains: gains(history, VisionFlag::Smoke),
            });
        }
    }
    out
}

pub fn write_tracks_csv(path: &Path, tracks: &[TrackSummary]) -> Result<(), Report> {
    let mut text = String::from(
        "entity_id,player,ship,team,world_samples,minimap_samples,first_s,last_s,max_gap_s,max_gap_at_s,flag_changes,rls_gains,sonar_gains,smoke_gains\n",
    );
    let f = |v: Option<f32>| v.map(|v| format!("{v:.1}")).unwrap_or_default();
    for t in tracks {
        let row = vec![
            t.entity_id.to_string(),
            t.player.clone(),
            t.ship.clone(),
            opt(t.team.as_deref()),
            t.world_samples.to_string(),
            t.minimap_samples.to_string(),
            f(t.first_s),
            f(t.last_s),
            f(t.max_gap_s),
            f(t.max_gap_at_s),
            t.flag_changes.to_string(),
            t.rls_gains.to_string(),
            t.sonar_gains.to_string(),
            t.smoke_gains.to_string(),
        ];
        text.push_str(&csv_line(&row));
        text.push('\n');
    }
    std::fs::write(path, text).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}

/// The game's own end-of-battle numbers for one player, decoded from the
/// replay's `playersPublicInfo` list with the field map
/// (`CLIENT_PUBLIC_RESULTS_INDICES`) of the build's `constants.json`.
#[derive(Debug, Clone, Serialize)]
pub struct PublicResult {
    pub name: String,
    pub team_id: Option<i64>,
    pub max_health: Option<f64>,
    pub remained_hp: Option<f64>,
    pub damage: Option<f64>,
    pub damage_main_ap: Option<f64>,
    pub damage_main_he: Option<f64>,
    pub damage_tpd: Option<f64>,
    pub damage_fire: Option<f64>,
    pub damage_flood: Option<f64>,
    pub received_damage_main: Option<f64>,
    pub scouting_damage: Option<f64>,
}

#[derive(Debug, thiserror::Error)]
pub enum PublicResultsError {
    #[error("cannot read {path}")]
    ReadConstants {
        path: std::path::PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("cannot parse {what}")]
    Parse {
        what: &'static str,
        #[source]
        source: serde_json::Error,
    },
    #[error("constants.json has no CLIENT_PUBLIC_RESULTS_INDICES map")]
    NoFieldMap,
    #[error("battle results have no playersPublicInfo object")]
    NoPlayers,
}

/// Decode every player's public results. `constants_path` is the build's
/// `constants.json`; `results` is the replay's battle results blob.
pub fn decode_public_results(constants_path: &Path, results: &str) -> Result<Vec<PublicResult>, PublicResultsError> {
    let constants_text = std::fs::read_to_string(constants_path)
        .map_err(|source| PublicResultsError::ReadConstants { path: constants_path.to_path_buf(), source })?;
    let constants: serde_json::Value = serde_json::from_str(&constants_text)
        .map_err(|source| PublicResultsError::Parse { what: "constants.json", source })?;
    let indices = constants
        .get("CLIENT_PUBLIC_RESULTS_INDICES")
        .and_then(|v| v.as_object())
        .ok_or(PublicResultsError::NoFieldMap)?;
    let index = |name: &str| indices.get(name).and_then(|v| v.as_u64()).map(|v| v as usize);
    let results: serde_json::Value =
        serde_json::from_str(results).map_err(|source| PublicResultsError::Parse { what: "battle results", source })?;
    let players = results.get("playersPublicInfo").and_then(|v| v.as_object()).ok_or(PublicResultsError::NoPlayers)?;
    let field = |row: &[serde_json::Value], name: &str| index(name).and_then(|i| row.get(i)).and_then(|v| v.as_f64());
    let mut out = Vec::new();
    for row in players.values() {
        let Some(row) = row.as_array() else { continue };
        let name = index("name").and_then(|i| row.get(i)).and_then(|v| v.as_str()).unwrap_or_default().to_string();
        out.push(PublicResult {
            name,
            team_id: index("team_id").and_then(|i| row.get(i)).and_then(|v| v.as_i64()),
            max_health: field(row, "max_health"),
            remained_hp: field(row, "remained_hp"),
            damage: field(row, "damage"),
            damage_main_ap: field(row, "damage_main_ap"),
            damage_main_he: field(row, "damage_main_he"),
            damage_tpd: field(row, "damage_tpd_normal"),
            damage_fire: field(row, "damage_fire"),
            damage_flood: field(row, "damage_flood"),
            received_damage_main: ["received_damage_main_ap", "received_damage_main_he", "received_damage_main_cs"]
                .iter()
                .filter_map(|n| field(row, n))
                .reduce(|a, b| a + b),
            scouting_damage: field(row, "scouting_damage"),
        });
    }
    out.sort_by(|a, b| a.name.cmp(&b.name));
    Ok(out)
}

pub fn write_public_results_csv(path: &Path, results: &[PublicResult]) -> Result<(), Report> {
    let mut text = String::from(
        "name,team_id,max_health,remained_hp,damage,damage_main_ap,damage_main_he,damage_tpd,damage_fire,damage_flood,received_damage_main,scouting_damage\n",
    );
    let f = |v: Option<f64>| v.map(|v| format!("{v:.0}")).unwrap_or_default();
    for r in results {
        let row = vec![
            r.name.clone(),
            opt(r.team_id),
            f(r.max_health),
            f(r.remained_hp),
            f(r.damage),
            f(r.damage_main_ap),
            f(r.damage_main_he),
            f(r.damage_tpd),
            f(r.damage_fire),
            f(r.damage_flood),
            f(r.received_damage_main),
            f(r.scouting_damage),
        ];
        text.push_str(&csv_line(&row));
        text.push('\n');
    }
    std::fs::write(path, text).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}
