//! Game data for a replay's build, and a merged replay session that can be
//! driven forward to any replay clock or HUD battle clock.

use std::collections::HashMap;
use std::path::Path;
use std::path::PathBuf;
use std::sync::Arc;

use rootcause::prelude::*;
use tracing::info;
use tracing::warn;
use wows_battle_world::merged::MergedReplays;
use wows_battle_world::scan::PositionTimeline;
use wows_battle_world::view::BattleView;
use wows_minimap_renderer::game_data_loader;
use wows_minimap_renderer::game_data_loader::LoadedGameData;
use wows_replays::ReplayFile;
use wows_replays::analyzer::battle_controller::merged::VehicleFacts;
use wows_replays::game_constants::GameConstants;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::data::Version;
use wowsunpack::game_params::provider::GameMetadataProvider;

use crate::clock::BattleClock;
use crate::clock::BattleClockMap;
use crate::replays::ReplaySet;

/// How far past the estimated replay clock the HUD countdown may still arrive
/// before a seek is treated as failed.
const HUD_TOLERANCE_SECONDS: f32 = 5.0;

/// Game data for the replay's build, resolved from `paths.game_data`.
pub struct GameData {
    pub version: Version,
    pub build_dir: PathBuf,
    pub loaded: LoadedGameData,
    pub constants: GameConstants,
}

pub fn load_game_data(game_data_dir: &Path, primary: &ReplayFile) -> Result<GameData, Report> {
    let version = Version::from_client_exe(&primary.meta.clientVersionFromExe);
    let build_dir = game_data_loader::resolve_extracted_dir(game_data_dir, &version)?;
    let loaded = game_data_loader::load_from_extracted(&build_dir, false, None)?;
    let mut constants = GameConstants::from_vfs(&loaded.vfs);
    match game_data_loader::merge_dump_constants(&mut constants, &build_dir, version)? {
        Some(path) => info!(path = %path.display(), "Merged constants from dump"),
        None => warn!(dir = %build_dir.display(), "No constants.json in dump; using built-in defaults"),
    }
    Ok(GameData { version, build_dir, loaded, constants })
}

/// Where a battle clock landed in the replay.
#[derive(Debug, Clone, Copy)]
pub struct SeekPoint {
    /// Replay clock at which the HUD first showed the requested value.
    pub clock: GameClock,
    /// Battle start plus elapsed, for comparison.
    pub estimate: GameClock,
}

/// The primary replay with the others merged in. Moves forward only.
pub struct GameSession<'a> {
    session: MergedReplays<'a, 'a, GameMetadataProvider>,
    vehicle_facts: HashMap<EntityId, VehicleFacts>,
    timeline: Arc<PositionTimeline>,
    clock_map: BattleClockMap,
    covered: Option<GameClock>,
}

impl<'a> GameSession<'a> {
    pub fn new(game: &'a GameData, replays: &'a ReplaySet) -> Result<Self, Report> {
        let version = game.version;
        let controller_params = &game.loaded.controller_game_params;
        let mut session = MergedReplays::new(
            &game.loaded.specs,
            controller_params,
            &game.constants,
            version,
            &replays.primary,
            &replays.merges,
        )?;
        let vehicle_facts = session.vehicle_facts().clone();
        wows_replay_insights::build::seed_consumable_inventories_from_facts(
            session.world_mut(),
            &vehicle_facts,
            controller_params,
            version,
        );
        for (i, r) in session.replays().iter().enumerate() {
            match session.self_teams()[i] {
                Some(team) => info!(replay = i, player = %r.meta.playerName, team = %team, "Self team"),
                None => warn!(replay = i, player = %r.meta.playerName, "Failed to detect self team"),
            }
        }
        let battle_start = session
            .battle_start_clock()
            .ok_or_else(|| report!("primary replay has no battle start; cannot place the battle clock"))?;
        let timeline = session.position_timeline();
        Ok(Self { session, vehicle_facts, timeline, clock_map: BattleClockMap::new(battle_start), covered: None })
    }

    pub fn battle_start(&self) -> GameClock {
        self.clock_map.battle_start()
    }

    pub fn clock_map(&self) -> &BattleClockMap {
        &self.clock_map
    }

    pub fn timeline(&self) -> &PositionTimeline {
        &self.timeline
    }

    pub fn timeline_arc(&self) -> Arc<PositionTimeline> {
        Arc::clone(&self.timeline)
    }

    pub fn vehicle_facts(&self) -> &HashMap<EntityId, VehicleFacts> {
        &self.vehicle_facts
    }

    /// Latest clock every replay has been processed up to.
    pub fn covered(&self) -> Option<GameClock> {
        self.covered
    }

    pub fn total_duration(&self) -> GameClock {
        self.session.total_duration()
    }

    pub fn truncated(&self) -> bool {
        self.session.truncated()
    }

    pub fn view(&mut self) -> BattleView<'_> {
        self.session.world_mut().view()
    }

    /// Process one packet. Returns the clock every replay has reached, or
    /// `None` once all replays are exhausted.
    pub fn step(&mut self) -> Result<Option<GameClock>, Report> {
        let Some(safe) = self.session.step()? else {
            return Ok(None);
        };
        self.covered = Some(safe);
        let view = self.session.world_mut().view();
        let clock = view.clock();
        let hud = view.time_left();
        self.clock_map.observe(clock, hud);
        Ok(Some(safe))
    }

    pub fn finish(&mut self) {
        self.session.finish();
    }

    /// Process packets until every replay has reached `clock`.
    pub fn seek_clock(&mut self, clock: GameClock) -> Result<(), Report> {
        if self.covered.is_some_and(|c| c.seconds() >= clock.seconds()) {
            return Ok(());
        }
        while let Some(safe) = self.step()? {
            if safe.seconds() >= clock.seconds() {
                return Ok(());
            }
        }
        bail!("replays end at {:.1} s, before replay clock {:.1} s", self.total_duration().seconds(), clock.seconds())
    }

    /// Process packets until the HUD first shows `at` and every replay has
    /// caught up to that moment.
    pub fn seek(&mut self, at: BattleClock) -> Result<SeekPoint, Report> {
        let estimate = at.estimate_game_clock(self.battle_start());
        loop {
            if let Some(clock) = self.clock_map.to_game_clock(at) {
                self.seek_clock(clock)?;
                return Ok(SeekPoint { clock, estimate });
            }
            let Some(safe) = self.step()? else {
                bail!(
                    "replays end at {:.1} s, before battle clock {at} (about {:.1} s)",
                    self.total_duration().seconds(),
                    estimate.seconds()
                );
            };
            if safe.seconds() > estimate.seconds() + HUD_TOLERANCE_SECONDS {
                bail!(
                    "HUD countdown never reached {at} by replay clock {:.1} s (battle start {:.1} s)",
                    safe.seconds(),
                    self.battle_start().seconds()
                );
            }
        }
    }
}
