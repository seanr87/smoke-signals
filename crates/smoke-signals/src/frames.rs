//! Pass two: an activation frame and a capture frame per smoke, with the
//! header strip, the smoke overlays, the zoomed inset, and the Tier 1 state
//! at each moment.

use std::collections::HashMap;
use std::path::Path;

use image::RgbImage;
use rootcause::prelude::*;
use tracing::info;
use wows_battle_world::view::BattleView;
use wows_minimap_renderer::MINIMAP_SIZE;
use wows_minimap_renderer::draw_command::DrawCommand;
use wows_minimap_renderer::map_data::MinimapPos;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::game_types::WorldPos;

use crate::clock::BattleClock;
use crate::config::Config;
use crate::header;
use crate::header::HeaderText;
use crate::header::Progress;
use crate::inset;
use crate::overlay;
use crate::overlay::OverlayInput;
use crate::records::GameRecord;
use crate::records::SmokeRecord;
use crate::records::SmokeType;
use crate::records::StateSnapshot;
use crate::render::FrameRenderer;
use crate::render::Projection;
use crate::replays::ReplaySet;
use crate::session::GameData;
use crate::session::GameSession;
use crate::state;
use crate::timeline;

/// Keep letters, digits, `-` and `.`; everything else becomes `_`.
pub fn sanitize(text: &str) -> String {
    text.chars().map(|c| if c.is_ascii_alphanumeric() || c == '-' || c == '.' { c } else { '_' }).collect()
}

/// `<match>_<game>_<team>_<player>_<ship>_s<nn>_<stage>_<mmss>`. A smoke
/// without an owner is named `unowned`, since the file still has to exist.
pub fn file_stem(record: &SmokeRecord, ordinal: usize, stage: &str, clock: Option<BattleClock>) -> String {
    let game = record.game_no.map(|n| format!("g{n}")).unwrap_or_else(|| "g".to_string());
    let clock = clock.map(|c| c.compact()).unwrap_or_else(|| "none".to_string());
    let owner = match (&record.team, &record.player, &record.ship) {
        (Some(team), Some(player), Some(ship)) => format!("{team}_{player}_{ship}"),
        _ => "unowned".to_string(),
    };
    sanitize(&format!("{}_{game}_{owner}_s{ordinal:02}_{stage}_{clock}", record.match_id))
}

/// Smoke types by object id, for recoloring every trail smoke in a frame.
pub fn smoke_types(smokes: &[SmokeRecord]) -> HashMap<u32, SmokeType> {
    smokes.iter().filter_map(|s| s.smoke_type.map(|t| (s.smoke_id, t))).collect()
}

/// Current puffs of every smoke object in the view.
pub fn current_puffs(view: &BattleView<'_>) -> HashMap<u32, Vec<WorldPos>> {
    view.smoke_screens().iter().map(|(id, s)| (id.raw() as u32, s.points.clone())).collect()
}

/// Padding around the target smoke's box in the inset, beyond the puff
/// radius, in map pixels.
const INSET_PAD_PX: f32 = 16.0;
/// Stroke width of a trail smoke's dashed path.
const TRAIL_WIDTH: f32 = 3.0;

/// Apply the frame overlays for `record` to `commands`. `smoker_pos` marks
/// the smoker while the smoke object has no puffs yet (before it appears).
/// A trail smoke gets its dashed path and no outline; a standard smoke gets
/// the outline of its puffs' union.
pub fn apply_overlays(
    projection: &Projection,
    config: &Config,
    record: &SmokeRecord,
    types: &HashMap<u32, SmokeType>,
    puffs: &HashMap<u32, Vec<WorldPos>>,
    smoker_pos: Option<WorldPos>,
    commands: &mut Vec<DrawCommand>,
) {
    let project = |p: WorldPos| projection.project(p);
    let pixel_radius = |r: f32| projection.pixel_radius(r);
    let input = OverlayInput {
        project: &project,
        pixel_radius: &pixel_radius,
        types,
        puffs,
        exhaust_color: config.render.exhaust_color.0,
        highlight_color: config.render.highlight_color.rgba(255),
    };
    overlay::recolor_trail_smoke(commands, &input);
    let is_trail = record.smoke_type.is_some_and(|t| t.is_trail());
    let has_puffs = puffs.get(&record.smoke_id).is_some_and(|p| !p.is_empty());
    if is_trail && let Some(path) = &record.path {
        commands.extend(overlay::dashed_path(path, &input, config.render.trail_color.rgba(255), TRAIL_WIDTH));
    }
    if !has_puffs {
        if let Some(pos) = smoker_pos {
            commands.extend(overlay::position_ring(pos, record.radius, &input));
        }
    } else if !is_trail {
        commands.extend(overlay::union_outline(record.smoke_id, record.radius, &input));
    }
}

/// Map pixels the inset is centered on: the smoke's box over its whole life
/// when known, else its origin. Before the smoke exists the smoker's
/// position is included, since the ring marks it then; afterwards the inset
/// stays on the smoke even when the smoker sails away.
fn inset_points(
    projection: &Projection,
    record: &SmokeRecord,
    smoker_pos: Option<WorldPos>,
    has_puffs: bool,
) -> Vec<MinimapPos> {
    let mut points = Vec::new();
    match &record.bbox {
        Some(b) => {
            for (x, z) in [(b.min_x, b.min_z), (b.max_x, b.max_z)] {
                points.extend(projection.project(WorldPos::new(x, 0.0, z)));
            }
        }
        None => points.extend(projection.project(WorldPos::new(record.origin_xy.x, 0.0, record.origin_xy.z))),
    }
    if !has_puffs {
        points.extend(smoker_pos.and_then(|p| projection.project(p)));
    }
    points
}

/// A rendered frame with its inset, before the header is added.
pub struct SmokeFrame {
    pub image: RgbImage,
    /// The inset on its own; absent when the map is unknown.
    pub zoom: Option<RgbImage>,
}

/// Draw the frame for `record` at `clock`, with overlays and the header.
pub fn render_smoke_frame<'a>(
    renderer: &mut FrameRenderer<'a>,
    session: &mut GameSession<'a>,
    config: &Config,
    record: &SmokeRecord,
    types: &HashMap<u32, SmokeType>,
    clock: GameClock,
    smoker: Option<EntityId>,
    text: &HeaderText,
    progress: Option<Progress>,
) -> Result<SmokeFrame, Report> {
    let projection = renderer.projection();
    let smoker_pos = smoker.and_then(|e| session.timeline().get(&e).and_then(|t| timeline::world_pos_at(t, clock)));
    let mut has_puffs = false;
    let mut image = renderer.render_image(session, clock, |view, commands| {
        let puffs = current_puffs(view);
        has_puffs = puffs.get(&record.smoke_id).is_some_and(|p| !p.is_empty());
        apply_overlays(&projection, config, record, types, &puffs, smoker_pos, commands);
    })?;
    let pad = projection.pixel_radius(record.radius) + INSET_PAD_PX;
    let region = inset::region_around(&inset_points(&projection, record, smoker_pos, has_puffs), pad);
    let zoom = region.map(|region| {
        let (x, y) = renderer.map_origin();
        let map = inset::MapRect { x, y, size: MINIMAP_SIZE };
        let built = inset::build(
            &image,
            map,
            region,
            config.render.zoom_factor,
            projection.pixel_radius(timeline::world_units(1000.0)),
            renderer.fonts(),
        );
        inset::place(&mut image, map, region, &built.image);
        built.image
    });
    Ok(SmokeFrame { image: header::compose(&image, renderer.fonts(), text, progress), zoom })
}

/// The smoker's team id and vehicle entity, from the game record.
pub fn smoker_identity(game: &GameRecord, record: &SmokeRecord) -> (Option<i64>, Option<EntityId>) {
    let owner = record
        .player
        .as_ref()
        .and_then(|name| game.teams.iter().flat_map(|t| t.players.iter()).find(|p| &p.player == name));
    let team = owner.and_then(|p| game.team_of_player(p.entity_id)).map(|t| t.team_id);
    (team, owner.map(|p| EntityId::from(p.entity_id)))
}

/// Tier 1 state at the session's current clock, from the smoker's side.
pub fn snapshot_for(session: &mut GameSession<'_>, game: &GameRecord, record: &SmokeRecord) -> StateSnapshot {
    let (team, smoker) = smoker_identity(game, record);
    let tl = session.timeline_arc();
    let view = session.view();
    state::snapshot(&view, game, team, smoker, &tl)
}

fn save_png_and_webp(image: &RgbImage, dir: &Path, stem: &str) -> Result<String, Report> {
    let png = format!("{stem}.png");
    image.save(dir.join(&png)).attach_with(|| format!("writing {}", dir.join(&png).display()))?;
    let webp = dir.join(format!("{stem}.webp"));
    image.save(&webp).attach_with(|| format!("writing {}", webp.display()))?;
    Ok(png)
}

/// Which frame an event produces.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Stage {
    Activation,
    Capture,
}

impl Stage {
    fn name(self) -> &'static str {
        match self {
            Self::Activation => "act",
            Self::Capture => "cap",
        }
    }
}

/// Render both frames of every smoke in clock order, fill the Tier 1 state
/// at each moment, and record the file names. Returns the frame count.
pub fn render_smoke_frames(
    config: &Config,
    game_data: &GameData,
    replays: &ReplaySet,
    game: &GameRecord,
    smokes: &mut [SmokeRecord],
    selected: &[usize],
    out_dir: &Path,
) -> Result<usize, Report> {
    std::fs::create_dir_all(out_dir).attach_with(|| format!("creating {}", out_dir.display()))?;
    let mut session = GameSession::new(game_data, replays)?;
    let mut renderer = FrameRenderer::new(config, game_data, replays, &session)?;
    let types = smoke_types(smokes);

    // Ordinal: position in the table, which is creation order.
    let mut events: Vec<(f32, usize, Stage)> = Vec::new();
    for (i, s) in smokes.iter().enumerate().filter(|(i, _)| selected.contains(i)) {
        events.push((s.activation_moment().seconds, i, Stage::Activation));
        if let Some(c) = s.t_capture {
            events.push((c.seconds, i, Stage::Capture));
        }
    }
    events.sort_by(|a, b| a.0.total_cmp(&b.0));

    let mut written = 0;
    for (seconds, i, stage) in events {
        let clock = GameClock(seconds);
        session.seek_clock(clock)?;
        let snapshot = snapshot_for(&mut session, game, &smokes[i]);
        let text = header::header_text(game, &smokes[i], i + 1, Some(&snapshot));
        let moment_clock = match stage {
            Stage::Activation => smokes[i].activation_moment().clock,
            Stage::Capture => smokes[i].t_capture.and_then(|m| m.clock),
        };
        let stem = file_stem(&smokes[i], i + 1, stage.name(), moment_clock);
        let (_, smoker) = smoker_identity(game, &smokes[i]);
        let frame =
            render_smoke_frame(&mut renderer, &mut session, config, &smokes[i], &types, clock, smoker, &text, None)?;
        let name = save_png_and_webp(&frame.image, out_dir, &stem)?;
        let zoom_name = match &frame.zoom {
            Some(zoom) => Some(save_png_and_webp(zoom, out_dir, &format!("{stem}_zoom"))?),
            None => None,
        };
        info!(smoke = smokes[i].smoke_id, stage = stage.name(), file = %name, "Frame");
        match stage {
            Stage::Activation => {
                smokes[i].frame_act = Some(name);
                smokes[i].frame_act_zoom = zoom_name;
                smokes[i].state_at_activate = Some(snapshot);
            }
            Stage::Capture => {
                smokes[i].frame_cap = Some(name);
                smokes[i].frame_cap_zoom = zoom_name;
                smokes[i].state_at_capture = Some(snapshot);
            }
        }
        written += 1;
    }
    Ok(written)
}
