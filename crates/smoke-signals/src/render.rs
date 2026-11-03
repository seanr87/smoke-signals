//! Drawing merged minimap frames at a replay clock. Mirrors the setup in
//! `minimap_renderer`'s binary, with the team-roster layout always on.

use std::path::Path;
use std::path::PathBuf;

use image::RgbImage;
use rootcause::prelude::*;
use tracing::info;
use tracing::warn;
use wows_battle_world::view::BattleView;
use wows_minimap_renderer::GameFonts;
use wows_minimap_renderer::MINIMAP_SIZE;
use wows_minimap_renderer::RenderTarget;
use wows_minimap_renderer::assets;
use wows_minimap_renderer::config::CliOverrides;
use wows_minimap_renderer::config::RendererConfig;
use wows_minimap_renderer::draw_command::DrawCommand;
use wows_minimap_renderer::drawing::ImageTarget;
use wows_minimap_renderer::drawing::SidePanelLayout;
use wows_minimap_renderer::map_data::MapInfo;
use wows_minimap_renderer::map_data::MinimapPos;
use wows_minimap_renderer::renderer::MinimapRenderer;
use wows_replays::ReplayFile;
use wows_replays::types::GameClock;
use wowsunpack::game_types::WorldPos;

use crate::clock::BattleClock;
use crate::config::Config;
use crate::replays::ReplaySet;
use crate::session::GameData;
use crate::session::GameSession;
use crate::session::SeekPoint;

/// Renderer state for one game. Draws from a [`GameSession`]'s current view.
pub struct FrameRenderer<'a> {
    renderer: MinimapRenderer<'a>,
    target: ImageTarget,
    map_info: Option<MapInfo>,
    fonts: GameFonts,
}

impl<'a> FrameRenderer<'a> {
    pub fn new(config: &Config, game: &'a GameData, replays: &'a ReplaySet, session: &GameSession<'a>) -> Result<Self, Report> {
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

        let controller_params = &game.loaded.controller_game_params;
        let mut all_replays: Vec<&ReplayFile> = vec![primary];
        all_replays.extend(replays.merges.iter());
        let damage_events = wows_battle_world::merged::gather_damage_events(
            controller_params,
            &game.constants,
            version,
            &game.loaded.specs,
            &all_replays,
        );

        let mut renderer = MinimapRenderer::new(map_info.clone(), &game.loaded.game_params, version, options);
        renderer.set_fonts(fonts.clone());
        renderer.set_flag_icons(flag_icons);
        renderer.set_merged_perspectives(merged);
        renderer.set_vehicle_facts(session.vehicle_facts().clone());
        renderer.set_damage_events(damage_events);
        // Every replay's positions, including the second recorder's own ship,
        // which the live merged state never receives.
        renderer.set_position_timeline(session.timeline_arc());
        let salvo_flight_times = wows_battle_world::scan::scan_salvo_flight_times(
            &primary.meta,
            controller_params,
            &game.constants,
            version,
            primary,
        );
        renderer.set_salvo_flight_times(std::sync::Arc::new(salvo_flight_times));

        Ok(Self { renderer, target, map_info, fonts })
    }

    pub fn fonts(&self) -> &GameFonts {
        &self.fonts
    }

    pub fn map_info(&self) -> Option<&MapInfo> {
        self.map_info.as_ref()
    }

    /// A copy of the map projection, usable while the renderer is drawing.
    pub fn projection(&self) -> Projection {
        Projection { map_info: self.map_info.clone() }
    }

    pub fn canvas_size(&self) -> (u32, u32) {
        self.target.canvas_size()
    }

    /// World position to minimap pixels, when the map is known.
    pub fn project(&self, pos: WorldPos) -> Option<MinimapPos> {
        self.map_info.as_ref().map(|m| m.world_to_minimap(pos, MINIMAP_SIZE))
    }

    /// World radius to minimap pixels; zero when the map is unknown.
    pub fn pixel_radius(&self, radius: f32) -> f32 {
        self.map_info.as_ref().map(|m| m.world_distance_to_minimap(radius, MINIMAP_SIZE)).unwrap_or(0.0)
    }

    /// Draw the frame at `clock` (which the session must already cover),
    /// let `edit` change the draw commands, and return the image.
    pub fn render_image(
        &mut self,
        session: &mut GameSession<'a>,
        clock: GameClock,
        edit: impl FnOnce(&BattleView<'_>, &mut Vec<DrawCommand>),
    ) -> Result<RgbImage, Report> {
        match session.covered() {
            Some(covered) if covered.seconds() >= clock.seconds() => {}
            covered => bail!("clock {:.2} s is not covered by the session (covered up to {:?})", clock.seconds(), covered),
        }
        let view = session.view();
        self.renderer.set_render_clock(clock);
        self.renderer.populate_players(&view);
        self.renderer.update_squadron_info(&view);
        self.renderer.update_ship_abilities(&view);
        let mut commands = self.renderer.draw_frame(&view);
        edit(&view, &mut commands);
        self.target.begin_frame();
        for command in &commands {
            self.target.draw(command);
        }
        self.target.end_frame();
        Ok(self.target.frame())
    }

    /// Draw the frame at `clock` with `overlay` on top and save it as PNG.
    pub fn render_png(
        &mut self,
        session: &mut GameSession<'a>,
        clock: GameClock,
        overlay: &[DrawCommand],
        path: &Path,
    ) -> Result<(), Report> {
        let image = self.render_image(session, clock, |_, commands| commands.extend_from_slice(overlay))?;
        image.save(path).attach_with(|| format!("writing {}", path.display()))?;
        Ok(())
    }
}

/// World-to-minimap projection detached from the renderer.
#[derive(Clone)]
pub struct Projection {
    map_info: Option<MapInfo>,
}

impl Projection {
    pub fn project(&self, pos: WorldPos) -> Option<MinimapPos> {
        self.map_info.as_ref().map(|m| m.world_to_minimap(pos, MINIMAP_SIZE))
    }

    pub fn pixel_radius(&self, radius: f32) -> f32 {
        self.map_info.as_ref().map(|m| m.world_distance_to_minimap(radius, MINIMAP_SIZE)).unwrap_or(0.0)
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
    let mut session = GameSession::new(game, replays)?;
    let mut renderer = FrameRenderer::new(config, game, replays, &session)?;
    let point = session.seek(at)?;
    info!(clock = point.clock.seconds(), estimate = point.estimate.seconds(), at = %at, "Seek complete");
    let path = out_dir.join(format!("frame_{}.png", at.compact()));
    renderer.render_png(&mut session, point.clock, &[], &path)?;
    Ok(RenderedFrame { path, at, point })
}
