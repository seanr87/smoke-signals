//! Draw-command edits for a smoke's frames: trail smoke in the exhaust color,
//! a dashed outline of the target trail's full path, and the highlight
//! outline of the target smoke.

use std::collections::HashMap;
use std::f32::consts::PI;

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
/// Stroke width of the target smoke's outline.
pub const OUTLINE_WIDTH: f32 = 2.0;
/// Arc sampling step along an outline, in pixels.
const ARC_STEP_PX: f32 = 2.0;
/// Puff centers closer than this are the same puff, drawn once.
const SAME_CENTER_PX: f32 = 0.01;

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

/// A ring at `pos`, used to mark the smoker before the smoke exists.
pub fn position_ring(pos: WorldPos, radius: f32, input: &OverlayInput<'_>) -> Vec<DrawCommand> {
    let r = (input.pixel_radius)(radius).max(3.0);
    (input.project)(pos)
        .map(|center| DrawCommand::Annotation {
            shape: AnnotationShape::Circle { center, radius: r, filled: false },
            color: input.highlight_color,
            width: OUTLINE_WIDTH,
        })
        .into_iter()
        .collect()
}

/// Outline of the union of the target smoke's current puffs: only the
/// outer boundary, as one polyline per arc.
pub fn union_outline(smoke_id: u32, radius: f32, input: &OverlayInput<'_>) -> Vec<DrawCommand> {
    let r = (input.pixel_radius)(radius).max(3.0);
    let centers: Vec<MinimapPos> =
        input.puffs.get(&smoke_id).map(|p| p.iter().filter_map(|p| (input.project)(*p)).collect()).unwrap_or_default();
    outer_arcs(&centers, r)
        .into_iter()
        .map(|points| DrawCommand::Annotation {
            shape: AnnotationShape::Polyline { points },
            color: input.highlight_color,
            width: OUTLINE_WIDTH,
        })
        .collect()
}

/// The parts of each circle's edge that no other circle covers, as point
/// runs. Equal radii throughout.
fn outer_arcs(centers: &[MinimapPos], r: f32) -> Vec<Vec<MinimapPos>> {
    let mut arcs = Vec::new();
    for (i, c) in centers.iter().enumerate() {
        let mut covered: Vec<(f32, f32)> = Vec::new();
        let mut duplicate = false;
        for (j, o) in centers.iter().enumerate() {
            if i == j {
                continue;
            }
            let (dx, dy) = (o.x - c.x, o.y - c.y);
            let d = (dx * dx + dy * dy).sqrt();
            if d < SAME_CENTER_PX {
                // Coincident puffs: the first one draws the edge.
                duplicate |= j < i;
                continue;
            }
            if d >= 2.0 * r {
                continue;
            }
            let half = (d / (2.0 * r)).acos();
            let at = dy.atan2(dx);
            push_interval(&mut covered, at - half, at + half);
        }
        if duplicate {
            continue;
        }
        for (start, end) in uncovered(&covered) {
            arcs.push(arc_points(*c, r, start, end));
        }
    }
    arcs
}

/// Add `[start, end]` to `covered`, split where it crosses the -pi/pi seam.
fn push_interval(covered: &mut Vec<(f32, f32)>, start: f32, end: f32) {
    let wrap = |a: f32| {
        let mut a = a;
        while a < -PI {
            a += 2.0 * PI;
        }
        while a > PI {
            a -= 2.0 * PI;
        }
        a
    };
    let (s, e) = (wrap(start), wrap(end));
    if s <= e {
        covered.push((s, e));
    } else {
        covered.push((s, PI));
        covered.push((-PI, e));
    }
}

/// The complement of `covered` within `[-pi, pi]`, with the two pieces at
/// the seam joined into one arc.
fn uncovered(covered: &[(f32, f32)]) -> Vec<(f32, f32)> {
    let mut sorted = covered.to_vec();
    sorted.sort_by(|a, b| a.0.total_cmp(&b.0));
    let mut merged: Vec<(f32, f32)> = Vec::new();
    for (s, e) in sorted {
        match merged.last_mut() {
            Some(last) if s <= last.1 => last.1 = last.1.max(e),
            _ => merged.push((s, e)),
        }
    }
    let mut gaps = Vec::new();
    let mut cursor = -PI;
    for (s, e) in &merged {
        if *s > cursor {
            gaps.push((cursor, *s));
        }
        cursor = cursor.max(*e);
    }
    if cursor < PI {
        gaps.push((cursor, PI));
    }
    if gaps.len() >= 2 && gaps[0].0 <= -PI && gaps[gaps.len() - 1].1 >= PI {
        let first = gaps.remove(0);
        let last = gaps.pop().expect("two gaps");
        gaps.push((last.0, first.1 + 2.0 * PI));
    }
    gaps
}

fn arc_points(center: MinimapPos, r: f32, start: f32, end: f32) -> Vec<MinimapPos> {
    let span = end - start;
    let steps = ((span * r / ARC_STEP_PX).ceil() as usize).max(2);
    (0..=steps)
        .map(|k| {
            let a = start + span * k as f32 / steps as f32;
            MinimapPos { x: center.x + r * a.cos(), y: center.y + r * a.sin() }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn at(x: f32, y: f32) -> MinimapPos {
        MinimapPos { x, y }
    }

    fn dist(a: MinimapPos, b: MinimapPos) -> f32 {
        ((a.x - b.x).powi(2) + (a.y - b.y).powi(2)).sqrt()
    }

    #[test]
    fn lone_circle_is_one_full_arc() {
        let arcs = outer_arcs(&[at(100.0, 100.0)], 20.0);
        assert_eq!(arcs.len(), 1);
        let first = arcs[0][0];
        let last = arcs[0][arcs[0].len() - 1];
        assert!(dist(first, last) < 0.01, "arc closes");
    }

    #[test]
    fn two_overlapping_circles_have_no_interior_points() {
        let a = at(100.0, 100.0);
        let b = at(130.0, 100.0);
        let arcs = outer_arcs(&[a, b], 20.0);
        assert_eq!(arcs.len(), 2);
        for arc in &arcs {
            for p in arc {
                let inside_a = dist(*p, a) < 20.0 - 0.05;
                let inside_b = dist(*p, b) < 20.0 - 0.05;
                assert!(!inside_a && !inside_b, "point {p:?} lies inside a circle");
            }
        }
        // The arc of the left circle faces left and crosses the seam, so it
        // is one run, not two.
        let left = arcs.iter().find(|arc| arc.iter().all(|p| p.x <= 115.1)).expect("left arc");
        assert!(left.iter().any(|p| p.x < 81.0));
    }

    #[test]
    fn coincident_circles_draw_once() {
        let arcs = outer_arcs(&[at(50.0, 50.0), at(50.0, 50.0)], 10.0);
        assert_eq!(arcs.len(), 1);
    }

    #[test]
    fn far_apart_circles_are_two_full_arcs() {
        let arcs = outer_arcs(&[at(50.0, 50.0), at(200.0, 50.0)], 10.0);
        assert_eq!(arcs.len(), 2);
    }
}
