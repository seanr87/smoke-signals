//! Tier 1 state at a moment, read from the merged view from the smoker's
//! side: scores, capture points, ships alive, the smoker's health and
//! detection, and enemy radars.

use std::collections::BTreeMap;

use wows_battle_world::scan::PositionTimeline;
use wows_battle_world::view::BattleView;
use wows_replays::types::EntityId;
use wowsunpack::game_types::ChargeCount;
use wowsunpack::game_types::Consumable;
use wowsunpack::recognized::Recognized;

use crate::records::AliveCount;
use crate::records::CapState;
use crate::records::GameRecord;
use crate::records::StateSnapshot;
use crate::timeline;

/// Capture point letters follow the minimap: index 0 is A.
pub fn cap_letter(index: usize) -> char {
    char::from_u32(u32::from(b'A') + index as u32).unwrap_or('?')
}

/// State at the view's current clock. `our_team` is the smoker's team id;
/// `smoker` is the smoker's vehicle entity when known.
pub fn snapshot(
    view: &BattleView<'_>,
    game: &GameRecord,
    our_team: Option<i64>,
    smoker: Option<EntityId>,
    tl: &PositionTimeline,
) -> StateSnapshot {
    let score_of = |team_id: i64| {
        usize::try_from(team_id)
            .ok()
            .and_then(|i| view.team_scores().iter().find(|s| s.team_index == i).map(|s| s.score))
    };
    let their_team = our_team.and_then(|ours| game.teams.iter().map(|t| t.team_id).find(|t| *t != ours));
    let team_name = |team_id: i64| game.team(team_id).and_then(|t| t.name.clone());

    let cap_state: Vec<CapState> = view
        .capture_points()
        .iter()
        .filter(|cp| cp.is_enabled)
        .map(|cp| CapState {
            cap: cap_letter(cp.index),
            owner: (cp.team_id >= 0).then(|| team_name(cp.team_id)).flatten(),
            progress: cp.progress.0 as f32,
            contested: cp.has_invaders,
            both_inside: cp.both_inside,
        })
        .collect();

    let dead = view.dead_ships();
    let mut alive: BTreeMap<(i64, Option<String>), u32> = BTreeMap::new();
    for team in &game.teams {
        for p in &team.players {
            if !dead.contains_key(&EntityId::from(p.entity_id)) {
                *alive.entry((team.team_id, p.ship_class.clone())).or_default() += 1;
            }
        }
    }
    let ships_alive: Vec<AliveCount> = alive
        .iter()
        .map(|((team_id, class), n)| AliveCount { team: team_name(*team_id), ship_class: class.clone(), alive: *n })
        .collect();
    let count_team = |team: Option<i64>| -> Option<u32> {
        team.map(|t| alive.iter().filter(|((id, _), _)| *id == t).map(|(_, n)| *n).sum())
    };

    let props = smoker.and_then(|e| view.vehicle_props(e));
    let smoker_hp_pct = props.and_then(|p| {
        let max = p.max_health();
        (max > 0.0).then(|| (p.health() / max * 100.0).clamp(0.0, 100.0))
    });
    let flags = props.and_then(|p| p.visibility_flags());

    let inventories = view.consumable_inventories();
    let enemy_radars_alive = their_team.and_then(|theirs| {
        game.team(theirs).map(|t| {
            t.players
                .iter()
                .filter(|p| !dead.contains_key(&EntityId::from(p.entity_id)))
                .filter(|p| {
                    inventories.get(&EntityId::from(p.entity_id)).is_some_and(|slots| {
                        slots.iter().any(|s| {
                            s.consumable == Recognized::Known(Consumable::Radar)
                                && match s.charges_remaining() {
                                    ChargeCount::Unlimited => true,
                                    ChargeCount::Finite(n) => n > 0,
                                }
                        })
                    })
                })
                .count() as u32
        })
    });

    let clock = view.clock();
    let smoker_pos = smoker.and_then(|e| tl.get(&e).and_then(|t| timeline::world_pos_at(t, clock)));
    let nearest_enemy = match (smoker_pos, their_team.and_then(|t| game.team(t))) {
        (Some(pos), Some(team)) => team
            .players
            .iter()
            .filter(|p| !dead.contains_key(&EntityId::from(p.entity_id)))
            .filter_map(|p| {
                let epos = tl.get(&EntityId::from(p.entity_id)).and_then(|t| timeline::world_pos_at(t, clock))?;
                Some((p.player.clone(), timeline::ground_distance(pos, epos)))
            })
            .min_by(|a, b| a.1.total_cmp(&b.1)),
        _ => None,
    };
    let nearest_cap = smoker_pos.and_then(|pos| {
        view.capture_points()
            .iter()
            .filter(|cp| cp.is_enabled)
            .filter_map(|cp| cp.position.map(|c| (cp.index, timeline::ground_distance(pos, c), cp.has_invaders)))
            .min_by(|a, b| a.1.total_cmp(&b.1))
    });

    StateSnapshot {
        score_ours: our_team.and_then(score_of),
        score_theirs: their_team.and_then(score_of),
        cap_state,
        ships_alive,
        alive_ours: count_team(our_team),
        alive_theirs: count_team(their_team),
        smoker_hp_pct,
        smoker_spotted: flags.map(|f| f.is_detected()),
        smoker_spotted_flags: flags.map(|f| f.to_string()),
        enemy_radars_alive,
        nearest_enemy: nearest_enemy.as_ref().map(|(name, _)| name.clone()),
        nearest_enemy_dist_km: nearest_enemy.map(|(_, d)| d / 1000.0),
        nearest_cap: nearest_cap.map(|(i, _, _)| cap_letter(i)),
        dist_to_nearest_cap_km: nearest_cap.map(|(_, d, _)| d / 1000.0),
        cap_contested: nearest_cap.map(|(_, _, c)| c),
    }
}
