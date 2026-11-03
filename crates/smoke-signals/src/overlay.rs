//! Draw-command edits for a smoke's frames: trail smoke in the exhaust color,
//! a dashed outline of the target trail's full path, and the highlight ring
//! on the target smoke's puffs.

use std::collections::HashMap;

use wows_minimap_renderer::draw_command::AnnotationShape;
use wows_minimap_renderer::draw_command::DrawCommand;
use wows_minimap_renderer::map_data::MinimapPos;
use wowsunpack::game_types::WorldPos;

use crate::records::SmokeType;
use crate::records::Xz;

/// Pixel distance within which a smoke draw command belongs to a puff.
const PUFF_MATCH_PX: f32 = 1.5;
const DASH_PX: f32 = 6.0;
const GAP_PX: f32 = 4.0;

/// What the overlay needs to know about the frame's smokes.
pub struct OverlayInput<'a> {
    /// Projection from world position to minimap pixels.
    pub project: &'a dyn Fn(WorldPos) -> Option<MinimapPos>,
    /// Pixel radius for a world radius.
    pub pixel_radius: &'a dyn Fn(f32) -> f32,
    /// Smoke type per smoke object present in the frame.
    pub types: &'a HashMap<u32, SmokeType>,
    /// Current puffs of every smoke object in the frame.
    pub puffs: &'a HashMap<u32, Vec<WorldPos>>,
    pub exhaust_color: [u8; 3],
    pub highlight_color: [u8; 4],
}

/// Recolor the smoke commands of every trail-type smoke in the frame.
pub fn recolor_trail_smoke(commands: &mut [DrawCommand], input: &OverlayInput<'_>) {
    let trail_px: Vec<MinimapPos> = input
        .puffs
        .iter()
        .filter(|(id, _)| input.types.get(id).is_some_and(|t| t.is_trail()))
        .flat_map(|(_, puffs)| puffs.iter().filter_map(|p| (input.project)(*p)))
        .collect();
    if trail_px.is_empty() {
        return;
    }
    for command in commands.iter_mut() {
        if let DrawCommand::Smoke { pos, color, .. } = command
            && trail_px.iter().any(|t| (t.x - pos.x).abs() <= PUFF_MATCH_PX && (t.y - pos.y).abs() <= PUFF_MATCH_PX)
        {
            *color = input.exhaust_color;
        }
    }
}

/// Dashed polyline along `path`, as one annotation per dash.
pub fn dashed_path(path: &[Xz], input: &OverlayInput<'_>, color: [u8; 4], width: f32) -> Vec<DrawCommand> {
    let points: Vec<MinimapPos> = path.iter().filter_map(|p| (input.project)(WorldPos::new(p.x, 0.0, p.z))).collect();
    let mut out = Vec::new();
    let mut pen_down = true;
    let mut remaining = DASH_PX;
    let mut dash: Vec<MinimapPos> = Vec::new();
    for pair in points.windows(2) {
        let (a, b) = (pair[0], pair[1]);
        let len = ((b.x - a.x).powi(2) + (b.y - a.y).powi(2)).sqrt();
        if len <= 0.0 {
            continue;
        }
        let mut travelled = 0.0;
        if pen_down && dash.is_empty() {
            dash.push(a);
        }
        while travelled < len {
            let step = remaining.min(len - travelled);
            travelled += step;
            remaining -= step;
            let t = travelled / len;
            let p = MinimapPos { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
            if pen_down {
                dash.push(p);
            }
            if remaining <= 0.0 {
                if pen_down && dash.len() >= 2 {
                    out.push(DrawCommand::Annotation {
                        shape: AnnotationShape::Polyline { points: std::mem::take(&mut dash) },
                        color,
                        width,
                    });
                }
                dash.clear();
                pen_down = !pen_down;
                remaining = if pen_down { DASH_PX } else { GAP_PX };
                if pen_down {
                    dash.push(p);
                }
            }
        }
    }
    if pen_down && dash.len() >= 2 {
        out.push(DrawCommand::Annotation { shape: AnnotationShape::Polyline { points: dash }, color, width });
    }
    out
}

/// Outline rings around the target smoke's current puffs.
pub fn highlight_rings(smoke_id: u32, radius: f32, input: &OverlayInput<'_>) -> Vec<DrawCommand> {
    let r = (input.pixel_radius)(radius).max(3.0);
    input
        .puffs
        .get(&smoke_id)
        .map(|puffs| {
            puffs
                .iter()
                .filter_map(|p| (input.project)(*p))
                .map(|center| DrawCommand::Annotation {
                    shape: AnnotationShape::Circle { center, radius: r, filled: false },
                    color: input.highlight_color,
                    width: 2.0,
                })
                .collect()
        })
        .unwrap_or_default()
}
