//! One merged replay session plus the renderer state needed to draw a frame at
//! any replay clock. Mirrors the setup in `minimap_renderer`'s binary.

use std::path::Path;
use std::path::PathBuf;

use rootcause::prelude::*;
use tracing::info;
use tracing::warn;
use wows_battle_world::merged::MergedReplays;
use wows_minimap_renderer::RenderTarget;
use wows_minimap_renderer::assets;
use wows_minimap_renderer::config::CliOverrides;
use wows_minimap_renderer::config::RendererConfig;
use wows_minimap_renderer::drawing::ImageTarget;
use wows_minimap_renderer::drawing::SidePanelLayout;
use wows_minimap_renderer::game_data_loader;
use wows_minimap_renderer::game_data_loader::LoadedGameData;
use wows_minimap_renderer::renderer::MinimapRenderer;
use wows_replays::ReplayFile;
use wows_replays::game_constants::GameConstants;
use wows_replays::types::GameClock;
use wowsunpack::data::Version;
use wowsunpack::game_params::provider::GameMetadataProvider;
use wowsunpack::rpc::entitydefs::EntitySpec;

use crate::clock::BATTLE_DURATION_SECONDS;
use crate::clock::BattleClock;
use crate::config::Config;
use crate::replays::ReplaySet;

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

/// How far past the estimated replay clock the HUD countdown may still arrive
/// before the seek is treated as failed.
const HUD_TOLERANCE_SECONDS: f32 = 5.0;

/// Where a battle clock landed in the replay.
#[derive(Debug, Clone, Copy)]
pub struct SeekPoint {
    /// Replay clock the frame is drawn at.
    pub clock: GameClock,
    /// HUD countdown the game reported there.
    pub hud: i64,
    /// Battle start plus elapsed, for comparison.
    pub estimate: GameClock,
}

/// A session over the primary replay with the others merged in, and a renderer
/// configured for the team-roster (merged) layout.
pub struct FrameSession<'a> {
    session: MergedReplays<'a, 'a, GameMetadataProvider>,
    renderer: MinimapRenderer<'a>,
    target: ImageTarget,
    /// Latest clock every replay has been processed up to.
    covered: Option<GameClock>,
}

impl<'a> FrameSession<'a> {
    pub fn new(config: &Config, game: &'a GameData, replays: &'a ReplaySet) -> Result<Self, Report> {
        let vfs = &game.loaded.vfs;
        let version = game.version;
        let primary = &replays.primary;

        info!("Loading fonts and icons");
        let fonts = assets::load_game_fonts(vfs);
        let v = Some(&version);
        let ship_icons = assets::load_ship_icons(vfs, v);
        let plane_icons = assets::load_plane_icons(vfs, v);
        let building_icons = assets::load_building_icons(vfs, v);
        let consumable_icons = assets::load_consumable_icons(vfs, v);
        let ribbon_icons = assets::load_ribbon_icons(vfs, wowsunpack::game_assets::GuiAssetDir::Ribbons, v);
        let subribbon_icons = assets::load_ribbon_icons(vfs, wowsunpack::game_assets::GuiAssetDir::SubRibbons, v);
        let death_cause_icons = assets::load_death_cause_icons(vfs, assets::ICON_SIZE, v);
        let powerup_icons = assets::load_powerup_icons(vfs, assets::ICON_SIZE, v);
        let flag_icons = assets::load_flag_icons(vfs, v);

        let map_name = &primary.meta.mapName;
        let map_image = assets::load_map_image(map_name, vfs);
        let map_info = assets::load_map_info(map_name, vfs);
        if map_info.is_none() {
            warn!(map = %map_name, "No map info in game data; world positions cannot be projected");
        }

        let merged = !replays.merges.is_empty();
        let mut renderer_config = RendererConfig::default();
        renderer_config.show_player_names = config.render.show_player_names;
        // The roster layout is the analysis view whether or not a second
        // replay was merged; it also avoids the stats panel, whose self
        // silhouette this tool does not load.
        renderer_config.apply_cli_overrides(&CliOverrides { team_rosters: true, ..CliOverrides::default() });
        let mut options = renderer_config.into_render_options();
        options.ship_config_visibility = wows_minimap_renderer::ShipConfigVisibility::SelfOnly;

        let target = ImageTarget::with_side_panel(
            map_image,
            fonts.clone(),
            ship_icons,
            plane_icons,
            building_icons,
            consumable_icons,
            ribbon_icons,
            subribbon_icons,
            death_cause_icons,
            powerup_icons,
            SidePanelLayout::from_options(&options),
        );

        let specs: &[EntitySpec] = &game.loaded.specs;
        let controller_params = &game.loaded.controller_game_params;
        let mut all_replays: Vec<&ReplayFile> = vec![primary];
        all_replays.extend(replays.merges.iter());
        let vehicle_facts = wows_replays::analyzer::battle_controller::merged::gather_replay_facts(
            &game.constants,
            version,
            specs,
            &all_replays,
        );
        let damage_events = wows_battle_world::merged::gather_damage_events(
            controller_params,
            &game.constants,
            version,
            specs,
            &all_replays,
        );

        let mut renderer = MinimapRenderer::new(map_info, &game.loaded.game_params, version, options);
        renderer.set_fonts(fonts);
        renderer.set_flag_icons(flag_icons);
        renderer.set_merged_perspectives(merged);
        renderer.set_vehicle_facts(vehicle_facts.clone());
        renderer.set_damage_events(damage_events);
        let salvo_flight_times = wows_battle_world::scan::scan_salvo_flight_times(
            &primary.meta,
            controller_params,
            &game.constants,
            version,
            primary,
        );
        renderer.set_salvo_flight_times(std::sync::Arc::new(salvo_flight_times));

        let mut session =
            MergedReplays::new(specs, controller_params, &game.constants, version, primary, &replays.merges)?;
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

        Ok(Self { session, renderer, target, covered: None })
    }

    pub fn battle_start(&self) -> Option<GameClock> {
        self.session.battle_start_clock()
    }

    /// Process packets until the game first reports `at` on the HUD countdown
    /// and every merged replay has caught up to that moment. The session only
    /// moves forward, so calls must be in decreasing battle-clock order.
    pub fn seek(&mut self, at: BattleClock) -> Result<SeekPoint, Report> {
        let battle_start =
            self.battle_start().ok_or_else(|| report!("replay has no battle start; cannot place the battle clock"))?;
        let estimate = at.to_game_clock(battle_start);
        let wanted = i64::from(at.remaining_seconds());
        let mut found: Option<SeekPoint> = None;
        // The same HUD property carries the pre-battle countdown and is stale
        // at the battle-start packet, so a value counts only after a larger
        // in-battle value has been seen (the countdown is monotonic), or when
        // it is the full battle duration itself.
        let mut armed = false;
        while let Some(safe) = self.session.step()? {
            self.covered = Some(safe);
            if found.is_none() {
                let view = self.session.world_mut().view();
                let clock = view.clock();
                let in_battle = clock.seconds() >= battle_start.seconds();
                match view.time_left() {
                    Some(left) if in_battle => {
                        if left > wanted || left == i64::from(BATTLE_DURATION_SECONDS) {
                            armed = true;
                        }
                        if armed && left <= wanted {
                            found = Some(SeekPoint { clock, hud: left, estimate });
                        }
                    }
                    _ => {}
                }
                if found.is_none() && clock.seconds() > estimate.seconds() + HUD_TOLERANCE_SECONDS {
                    bail!(
                        "HUD countdown never reached {at} by replay clock {:.1} s (battle start {:.1} s)",
                        clock.seconds(),
                        battle_start.seconds()
                    );
                }
            }
            if let Some(point) = found
                && safe.seconds() >= point.clock.seconds()
            {
                return Ok(point);
            }
        }
        bail!(
            "replays end at {:.1} s, before battle clock {at} (about {:.1} s)",
            self.session.total_duration().seconds(),
            estimate.seconds()
        );
    }

    /// Draw the frame at `clock` (which `seek` must already cover) and save it
    /// as PNG.
    pub fn render_png(&mut self, clock: GameClock, path: &Path) -> Result<(), Report> {
        match self.covered {
            Some(covered) if covered.seconds() >= clock.seconds() => {}
            covered => {
                bail!("clock {:.2} s is not covered by the session (covered up to {:?})", clock.seconds(), covered)
            }
        }
        let view = self.session.world_mut().view();
        self.renderer.set_render_clock(clock);
        self.renderer.populate_players(&view);
        self.renderer.update_squadron_info(&view);
        self.renderer.update_ship_abilities(&view);
        let commands = self.renderer.draw_frame(&view);
        self.target.begin_frame();
        for command in &commands {
            self.target.draw(command);
        }
        self.target.end_frame();
        self.target.frame().save(path).attach_with(|| format!("writing {}", path.display()))?;
        Ok(())
    }
}

/// The frame written for one battle clock.
pub struct RenderedFrame {
    pub path: PathBuf,
    pub at: BattleClock,
    pub point: SeekPoint,
}

/// Render the merged view at one battle clock into `out_dir`.
pub fn render_frame_at(
    config: &Config,
    game: &GameData,
    replays: &ReplaySet,
    at: BattleClock,
    out_dir: &Path,
) -> Result<RenderedFrame, Report> {
    let mut frame = FrameSession::new(config, game, replays)?;
    let point = frame.seek(at)?;
    info!(
        clock = point.clock.seconds(),
        estimate = point.estimate.seconds(),
        hud = point.hud,
        at = %at,
        "Seek complete"
    );
    let path = out_dir.join(format!("frame_{}.png", at.compact()));
    frame.render_png(point.clock, &path)?;
    Ok(RenderedFrame { path, at, point })
}
