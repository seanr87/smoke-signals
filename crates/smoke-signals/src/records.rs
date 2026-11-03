//! Output records. Field names follow smoke/DESIGN.md; a time field `t_x`
//! holds replay seconds and `t_x_clock` the HUD battle clock at that moment.
//! A field is `None` when the replays did not yield it.

use serde::Serialize;

use crate::clock::BattleClock;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum SmokeType {
    Standard,
    Exhaust,
    Crawling,
}

impl SmokeType {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Standard => "standard",
            Self::Exhaust => "exhaust",
            Self::Crawling => "crawling",
        }
    }

    /// Exhaust and crawling smoke trail behind a moving ship.
    pub fn is_trail(self) -> bool {
        matches!(self, Self::Exhaust | Self::Crawling)
    }
}

/// A replay moment: seconds into the replay and the HUD countdown shown then.
#[derive(Debug, Clone, Copy, Serialize)]
pub struct Moment {
    pub seconds: f32,
    pub clock: Option<BattleClock>,
}

impl Moment {
    pub fn clock_text(&self) -> String {
        self.clock.map(|c| c.to_string()).unwrap_or_default()
    }
}

#[derive(Debug, Clone, Copy, Serialize)]
pub struct Xz {
    pub x: f32,
    pub z: f32,
}

#[derive(Debug, Clone, Copy, Serialize)]
pub struct Bbox {
    pub min_x: f32,
    pub min_z: f32,
    pub max_x: f32,
    pub max_z: f32,
}

/// One capture point at a moment.
#[derive(Debug, Clone, Serialize)]
pub struct CapState {
    /// Letter shown on the minimap (A, B, ...).
    pub cap: char,
    /// Team label of the owner, `None` when neutral.
    pub owner: Option<String>,
    /// Capture progress 0..1 of the current invasion.
    pub progress: f32,
    /// An enemy of the owner (or anyone, for a neutral cap) is inside.
    pub contested: bool,
    /// Ships of both teams are inside, which blocks the capture.
    pub both_inside: bool,
}

/// Ships alive of one team and class.
#[derive(Debug, Clone, Serialize)]
pub struct AliveCount {
    pub team: Option<String>,
    pub ship_class: Option<String>,
    pub alive: u32,
}

/// Tier 1 state at one moment, from the smoker's side.
#[derive(Debug, Clone, Serialize)]
pub struct StateSnapshot {
    pub score_ours: Option<i64>,
    pub score_theirs: Option<i64>,
    pub cap_state: Vec<CapState>,
    pub ships_alive: Vec<AliveCount>,
    pub alive_ours: u32,
    pub alive_theirs: u32,
    pub smoker_hp_pct: Option<f32>,
    /// `None` when the replay carried no visibility flags for the smoker.
    pub smoker_spotted: Option<bool>,
    /// The game's own reason flags, e.g. `BY_SHIP|IN_SMOKE`.
    pub smoker_spotted_flags: Option<String>,
    /// Enemy ships alive with a radar charge left.
    pub enemy_radars_alive: Option<u32>,
}

impl StateSnapshot {
    pub fn caps_text(&self) -> String {
        self.cap_state
            .iter()
            .map(|c| {
                let owner = c.owner.as_deref().unwrap_or("-");
                let mark = if c.both_inside {
                    "!!"
                } else if c.contested {
                    "!"
                } else {
                    ""
                };
                format!("{}:{owner}{mark}", c.cap)
            })
            .collect::<Vec<_>>()
            .join(" ")
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct SmokeRecord {
    pub smoke_id: u32,
    pub activation_id: Option<String>,
    pub match_id: String,
    pub round: Option<String>,
    pub game_no: Option<u32>,
    pub map: String,
    pub game_build: String,
    pub primary_replay: String,
    pub merged_replays: Vec<String>,
    pub team: Option<String>,
    pub opponent: Option<String>,
    pub spawn_side: Option<String>,
    pub player: Option<String>,
    pub ship: Option<String>,
    pub ship_class: Option<String>,
    pub ship_tier: Option<u32>,

    pub smoke_type: Option<SmokeType>,
    pub variant: Option<String>,
    pub charge_no: Option<u32>,
    pub charges_total: Option<u32>,
    pub base_emission_s: Option<f32>,
    pub base_puff_life_s: Option<f32>,
    pub base_radius: Option<f32>,
    /// Puff radius the replay reports for this smoke object.
    pub radius: f32,
    pub observed_emission_s: Option<f32>,
    pub emission_cut_short: bool,
    pub owner_flag: bool,
    pub owner_note: String,
    pub owner_distance_m: Option<f32>,
    pub overlap_flag: bool,
    pub overlapping_smoke_ids: Vec<u32>,
    pub origin_xy: Xz,
    pub bbox: Option<Bbox>,
    pub puff_count: u32,
    pub path: Option<Vec<Xz>>,

    pub t_created: Moment,
    pub t_activate: Option<Moment>,
    pub t_capture: Option<Moment>,
    pub t_emission_end: Option<Moment>,
    pub t_dispersed: Option<Moment>,

    pub state_at_activate: Option<StateSnapshot>,
    pub state_at_capture: Option<StateSnapshot>,

    pub wows_toolkit_rev: Option<String>,
    pub smoke_signals_version: String,
    pub generated_at: String,
    pub frame_act: Option<String>,
    pub frame_cap: Option<String>,
    pub clip: Option<String>,
}

impl SmokeRecord {
    /// The moment the activation frame and the clip start refer to: the
    /// activation, or the object's creation when no activation was recorded.
    pub fn activation_moment(&self) -> Moment {
        self.t_activate.unwrap_or(self.t_created)
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct PlayerRecord {
    pub entity_id: u32,
    pub player: String,
    pub clan: String,
    pub ship: String,
    pub ship_index: String,
    pub ship_class: Option<String>,
    pub ship_tier: Option<u32>,
    pub smoke_variant: Option<String>,
    pub smoke_type: Option<SmokeType>,
    pub smoke_activations: u32,
    pub death: Option<Moment>,
}

#[derive(Debug, Clone, Serialize)]
pub struct TeamRecord {
    /// Clan label shared by most of the team's player names.
    pub name: Option<String>,
    pub team_id: i64,
    pub spawn_side: Option<String>,
    pub final_score: Option<i64>,
    pub players: Vec<PlayerRecord>,
}

#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    Win { team_id: i64, team: Option<String> },
    Draw,
}

#[derive(Debug, Clone, Serialize)]
pub struct GameRecord {
    pub tournament: Option<String>,
    pub match_id: String,
    pub round: Option<String>,
    pub game_no: Option<u32>,
    pub map: String,
    pub map_name: String,
    pub game_build: String,
    pub primary_replay: String,
    pub merged_replays: Vec<String>,
    pub teams: Vec<TeamRecord>,
    pub outcome: Option<Outcome>,
    pub finish_type: Option<String>,
    pub battle_start_s: f32,
    pub battle_end: Option<Moment>,
    pub replay_end_s: f32,
    pub replay_truncated: bool,
    pub wows_toolkit_rev: Option<String>,
    pub smoke_signals_version: String,
    pub generated_at: String,
}

impl GameRecord {
    pub fn team(&self, team_id: i64) -> Option<&TeamRecord> {
        self.teams.iter().find(|t| t.team_id == team_id)
    }

    pub fn team_of_player(&self, entity_id: u32) -> Option<&TeamRecord> {
        self.teams.iter().find(|t| t.players.iter().any(|p| p.entity_id == entity_id))
    }

    pub fn player(&self, entity_id: u32) -> Option<&PlayerRecord> {
        self.teams.iter().flat_map(|t| t.players.iter()).find(|p| p.entity_id == entity_id)
    }

    pub fn outcome_text(&self) -> String {
        match &self.outcome {
            None => String::new(),
            Some(Outcome::Draw) => "draw".to_string(),
            Some(Outcome::Win { team, team_id }) => team.clone().unwrap_or_else(|| format!("team {team_id}")),
        }
    }

    /// Map display name without the numeric prefix, e.g. `Sleeping Giant`.
    pub fn map_title(&self) -> String {
        let bare = self.map.split_once('_').map(|(_, rest)| rest).unwrap_or(&self.map);
        bare.replace('_', " ")
    }
}
