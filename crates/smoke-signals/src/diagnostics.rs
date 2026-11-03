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
}

pub fn summarize_tracks(timeline: &PositionTimeline, roster: &GameRecord) -> Vec<TrackSummary> {
    let mut out = Vec::new();
    for team in &roster.teams {
        for p in &team.players {
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
            });
        }
    }
    out
}

pub fn write_tracks_csv(path: &Path, tracks: &[TrackSummary]) -> Result<(), Report> {
    let mut text = String::from(
        "entity_id,player,ship,team,world_samples,minimap_samples,first_s,last_s,max_gap_s,max_gap_at_s\n",
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
        ];
        text.push_str(&csv_line(&row));
        text.push('\n');
    }
    std::fs::write(path, text).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}
