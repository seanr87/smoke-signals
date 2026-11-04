//! Output records. Field names follow smoke/DESIGN.md; a time field `t_x`
//! holds replay seconds and `t_x_clock` the HUD battle clock at that moment.
//! A field is `None` when the replays did not yield it.

use serde::Serialize;

use crate::clock::BattleClock;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum SmokeType {
    Standard,
    /// Short cruiser smoke (puff life of a minute or less, e.g. Svea).
    Cruiser,
    Exhaust,
    Crawling,
}

impl SmokeType {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Standard => "standard",
            Self::Cruiser => "cruiser",
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

#[derive(Debug, Clone, Copy, Default, Serialize)]
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
    pub alive_ours: Option<u32>,
    pub alive_theirs: Option<u32>,
    pub smoker_hp_pct: Option<f32>,
    /// `None` when the replay carried no visibility flags for the smoker.
    pub smoker_spotted: Option<bool>,
    /// The game's own reason flags, e.g. `BY_SHIP|IN_SMOKE`.
    pub smoker_spotted_flags: Option<String>,
    /// Enemy ships alive with a radar charge left.
    pub enemy_radars_alive: Option<u32>,
    pub nearest_enemy: Option<String>,
    pub nearest_enemy_dist_km: Option<f32>,
    pub nearest_cap: Option<char>,
    pub dist_to_nearest_cap_km: Option<f32>,
    /// The nearest cap has invaders.
    pub cap_contested: Option<bool>,
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
    /// In-game display name of the map.
    pub map_display: String,
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

    /// Tier 2: ships of the smoker's team inside the smoke at t_capture.
    pub allies_in_smoke: Vec<String>,
    pub enemies_in_smoke: Vec<String>,
    pub ally_ship_seconds_in_smoke: f32,
    pub enemy_ship_seconds_in_smoke: f32,
    pub radar_detections_in_smoke: Vec<crate::tier2::DetectionEvent>,
    pub hydro_detections_in_smoke: Vec<crate::tier2::DetectionEvent>,
    pub fired_while_concealed_detections: Vec<crate::tier2::DetectionEvent>,
    /// Distance at t_capture from the smoke's edge to the nearest cap's
    /// edge, negative when the smoke reaches inside the cap.
    pub cap_proximity_m: Option<f32>,
    pub cap_proximity_name: Option<String>,
    /// Radius of that cap in meters.
    pub cap_radius_m: Option<f32>,
    /// No teammate but the owner was ever inside, and no ally damage went
    /// through it. `None` without damage data.
    pub selfish_smoke: Option<bool>,
    /// The contested cap nearest the smoke for most of its life. A cap is
    /// contested for the smoker's team when the midline crosses it, it lies
    /// on the enemy's side of the midline, or the enemy owns it.
    pub contested_cap_name: Option<String>,
    /// Why that cap counted as contested: `midline`, `enemy_side` or
    /// `enemy_owned`, the first that applied most often.
    pub cap_contested_reason: Option<String>,
    /// Edge-to-edge distance in meters from the standing puffs to the
    /// nearest contested cap, averaged over samples of the smoke's life.
    /// Negative when the smoke reaches inside. `None` when no cap was
    /// contested while the smoke stood.
    pub avg_contested_cap_dist_m: Option<f32>,
    /// Depth into that cap as a share of its radius, from the average
    /// distance of the smoke's edge to the cap centre over the smoke's life:
    /// 0 at the edge, 100 at the centre, negative outside.
    pub contested_cap_depth_pct: Option<f32>,
    /// Radius of that cap in meters.
    pub contested_cap_radius_m: Option<f32>,
    /// Caps within stock main-gun range of a ship of the smoker's team while
    /// it stood inside the smoke.
    pub supported_caps: Vec<String>,
    /// A supported cap that flipped to the smoker's team while the smoke
    /// stood or within 10 s after its last puff faded.
    pub cap_won: Option<String>,
    pub cap_won_at: Option<Moment>,
    /// A contested cap the smoker's team owned while the enemy was invading
    /// it and the smoke stood.
    pub cap_defended: Option<String>,
    pub radar_cap: Option<RadarCapCoverage>,
    pub cap_denial: Option<CapDenial>,
    /// Damage taken by the smoke's team's ships while radar-spotted inside it.
    pub radar_spotted_damage: f32,
    pub offensive_radar: Option<OffensiveRadar>,
    /// Ships of the smoker's team credited with damage through this smoke.
    pub shooters: Vec<String>,
    /// The same shooters with ship, salvos, damage and kills.
    pub shooter_detail: Vec<ShooterDetail>,
    /// Enemy ships hit by credited shots, with whether those shots sank them.
    pub targets_hit: Vec<TargetHit>,
    /// Enemy ships whose last damage before sinking was credited to this smoke.
    pub kills_from_smoke: u32,
    /// Ships of the smoker's team concealed by this smoke (inside it or
    /// firing from behind it), detected afterwards, and sunk while it stood
    /// or within 20 s after its last puff faded.
    pub smoke_deaths: Vec<SmokeDeath>,
    /// Living ships near the smoke at t_capture, for the diagram.
    pub ships_at_capture: Vec<ShipMark>,
    /// Hydro run by the smoker's team from inside the smoke while concealed.
    pub offensive_hydro: Option<OffensiveRadar>,
    /// Round 5 classification: smoker, movement, coverage, purposes, location.
    pub classification: Option<Classification>,
    /// Allied ships the smoke concealed, with how they were detected.
    pub smokees: Vec<Smokee>,

    /// Tier 3, from the M4 spike: damage by the smoker's team only.
    pub damage_in_smoke: Option<f32>,
    pub damage_behind_smoke: Option<f32>,
    pub smoke_damage_total: Option<f32>,
    pub damage_in_smoke_enemy: Option<f32>,
    pub damage_behind_smoke_enemy: Option<f32>,
    pub damage_detail: Option<crate::damage::SmokeDamage>,

    pub wows_toolkit_rev: Option<String>,
    pub smoke_signals_version: String,
    pub generated_at: String,
    pub frame_act: Option<String>,
    pub frame_cap: Option<String>,
    /// The zoomed inset of each frame, saved on its own.
    pub frame_act_zoom: Option<String>,
    pub frame_cap_zoom: Option<String>,
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
    pub smoke_charges: Option<u32>,
    pub death: Option<Moment>,
    /// Stock main-gun range in meters.
    pub gun_range_m: Option<f32>,
    pub radar_m: Option<f32>,
    /// Base surface detection range in meters.
    pub detection_m: Option<f32>,
}

#[derive(Debug, Clone, Serialize)]
pub struct TeamRecord {
    /// Clan label shared by most of the team's player names.
    pub name: Option<String>,
    pub team_id: i64,
    pub spawn_side: Option<String>,
    /// Mean of the team's first positions, in world units.
    pub spawn_xy: Option<Xz>,
    pub final_score: Option<i64>,
    pub players: Vec<PlayerRecord>,
}

#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    Win { team_id: i64, team: Option<String> },
    Draw,
}

/// A radar ship concealed in the smoke and how much of a cap its radar reached.
#[derive(Debug, Clone, Serialize)]
pub struct RadarCapCoverage {
    pub cap: String,
    pub ship: Option<String>,
    /// Share of the cap's area within radar range, 0 to 100.
    pub coverage_pct: f32,
    /// The whole cap lay within radar range.
    pub full: bool,
    /// The radar was activated while the ship stood in the smoke.
    pub activated: bool,
}

/// Enemy ships in or near the nearest contested cap, averaged over samples
/// in the 60 s before the smoke and over its life.
#[derive(Debug, Clone, Serialize)]
pub struct CapDenial {
    pub cap: String,
    pub enemies_before: f32,
    pub enemies_during: f32,
}

/// Enemies spotted by a radar of the smoker's team run from inside the smoke
/// while concealed. The replay does not name the spotting radar, so a spot
/// is inferred from the activation and the radar's range.
#[derive(Debug, Clone, Serialize)]
pub struct OffensiveRadar {
    pub ship: Option<String>,
    pub activations: u32,
    pub enemies_spotted: u32,
    pub inferred: bool,
}

/// A ship near a smoke at one moment, for the diagram.
#[derive(Debug, Clone, Serialize)]
pub struct ShipMark {
    pub entity_id: u32,
    pub player: String,
    pub team: Option<String>,
    pub ship_class: Option<String>,
    pub position: Xz,
    pub is_owner: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct ShooterDetail {
    pub entity_id: u32,
    pub player: String,
    pub ship: String,
    pub salvos: u32,
    pub damage: f32,
    pub kills: u32,
}

#[derive(Debug, Clone, Serialize)]
pub struct TargetHit {
    pub entity_id: u32,
    pub player: String,
    pub ship: String,
    pub damage: f32,
    pub sunk: bool,
}

/// How a smoke first concealed a ship.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum Concealment {
    Inside,
    Behind,
}

#[derive(Debug, Clone, Serialize)]
pub struct SmokeDeath {
    pub entity_id: u32,
    pub player: String,
    pub ship: String,
    pub concealed: Concealment,
    pub death: Moment,
    /// The ship sank after the last puff faded (within the grace period).
    pub after_cleared: bool,
}

/// How the smoker moved relative to the nearest enemies while laying.
#[derive(Debug, Clone, Serialize)]
pub struct Movement {
    /// `pushing`, `kiting` or `horizontal`.
    pub label: String,
    pub confidence: String,
    /// Straight-line displacement while laying, in meters.
    pub path_m: f32,
    /// Angle between the movement and the direction to the enemy group.
    pub angle_deg: f32,
    /// Change in the distance to the enemy group, in meters; negative closes.
    pub closing_m: f32,
    pub reason: String,
}

/// Who the smoke protects: `stacked`, `screen` or `selfish`.
#[derive(Debug, Clone, Serialize)]
pub struct Coverage {
    pub label: String,
    pub stacked: bool,
    pub screen: bool,
    pub selfish: bool,
    pub reason: String,
}

/// One purpose tag with its confidence (`None` for rule-based tags).
#[derive(Debug, Clone, Serialize)]
pub struct PurposeTag {
    pub tag: String,
    pub confidence: Option<String>,
    pub reason: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct Classification {
    /// `destroyer`, `cruiser` or `battleship`.
    pub smoker_class: Option<String>,
    /// Special cases: `svea`, `battleship_exhaust`, `battleship_crawling`.
    pub special: Vec<String>,
    pub movement: Option<Movement>,
    pub coverage: Coverage,
    /// Every purpose that applies, in priority order.
    pub purposes: Vec<PurposeTag>,
    pub primary_purpose: Option<String>,
    /// Smoke damage of 20,000 or more.
    pub damage_20k: bool,
    /// 20,000 damage or two or more enemies hit.
    pub damage_qualified: bool,
    /// `target_rich`, `hunt` or `island_killer`.
    pub damage_label: Option<String>,
    /// `left`, `center` or `right`, from the smoker's team's spawn facing the enemy.
    pub lane: Option<String>,
    /// Lateral offset from the spawn-to-spawn axis in meters; positive to the right.
    pub lane_offset_m: Option<f32>,
    /// Role of the nearest contested cap (else the nearest cap): `home`, `center`, `enemy`.
    pub cap_role: Option<String>,
    pub cap_role_cap: Option<String>,
    pub cap_flank: Option<bool>,
    /// Distance from the midpoint between the two fleets at activation, in
    /// meters; positive toward the enemy fleet.
    pub frontline_distance_m: Option<f32>,
    pub nearest_enemy_m: Option<f32>,
    /// Caps within stock gun range of a concealed ship (the supported caps).
    pub caps_in_range: Vec<String>,
    pub counter_smoke_of: Option<u32>,
    /// Distance from the smoke origin to the nearest land, in meters.
    pub land_distance_m: Option<f32>,
}

/// One detection of a smokee while the smoke concealed it.
#[derive(Debug, Clone, Serialize)]
pub struct SmokeeDetection {
    /// `surface lit`, `smoke fire penalty`, `radar`, `hydro`, `proximity`, `aircraft`.
    pub kind: String,
    pub inferred: bool,
    pub seconds: f32,
    pub clock: Option<BattleClock>,
}

/// An allied ship the smoke concealed: inside it, firing from behind it, or
/// with the smoke between it and an enemy in its line of fire.
#[derive(Debug, Clone, Serialize)]
pub struct Smokee {
    pub entity_id: u32,
    pub player: String,
    pub ship: String,
    pub ship_class: Option<String>,
    /// `inside`, `behind` or `line_of_fire`, the first that applied.
    pub how: String,
    pub seconds_concealed: f32,
    pub detections: Vec<SmokeeDetection>,
    pub damage: f32,
    pub kills: u32,
}

/// One capture zone of a game, in world units.
#[derive(Debug, Clone, Serialize)]
pub struct CapLayout {
    pub cap: char,
    pub position: Xz,
    pub radius: f32,
    pub radius_m: f32,
    /// The game's control point type, e.g. `Control` or `Base`.
    pub kind: Option<String>,
}

/// Internal map name without its numeric prefix and underscores.
pub fn map_title_fallback(map: &str) -> String {
    let bare = map.split_once('_').map(|(_, rest)| rest).unwrap_or(map);
    bare.replace('_', " ")
}

#[derive(Debug, Clone, Serialize)]
pub struct GameRecord {
    pub tournament: Option<String>,
    pub match_id: String,
    pub round: Option<String>,
    pub game_no: Option<u32>,
    pub map: String,
    pub map_name: String,
    /// In-game display name of the map, e.g. `Mountain Range`.
    pub map_display: String,
    pub game_build: String,
    pub primary_replay: String,
    pub merged_replays: Vec<String>,
    pub teams: Vec<TeamRecord>,
    /// Enabled capture zones at the end of the replay.
    pub caps: Vec<CapLayout>,
    pub outcome: Option<Outcome>,
    pub finish_type: Option<String>,
    pub battle_start_s: f32,
    pub battle_end: Option<Moment>,
    pub replay_end_s: f32,
    pub replay_truncated: bool,
    /// Share of the minimap that is land, from the map's land layer.
    pub land_share: Option<f32>,
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

    pub fn player_by_name(&self, name: &str) -> Option<&PlayerRecord> {
        self.teams.iter().flat_map(|t| t.players.iter()).find(|p| p.player == name)
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

    /// In-game map name, falling back to the internal name without its
    /// numeric prefix, e.g. `Sleeping Giant`.
    pub fn map_title(&self) -> String {
        if !self.map_display.is_empty() {
            return self.map_display.clone();
        }
        map_title_fallback(&self.map)
    }
}
