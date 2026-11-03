//! Sampling the pre-scanned position timeline at an arbitrary replay clock.
//!
//! The merged world's live positions omit two kinds of ship: the second
//! replay's recorder (its own position arrives as `PlayerOrientation`, which
//! the merge never forwards) and enemy ships the primary replay has not yet
//! created. The timeline that `MergedReplays` builds from every replay has
//! both, so queries at a clock go through it.

use wows_battle_world::scan::EntityTrack;
use wows_replays::types::GameClock;
use wows_replays::types::NormalizedPos;
use wowsunpack::game_types::WorldPos;

/// How long a ship's last known position stays usable after its last sample.
const HOLD_SECONDS: f32 = 10.0;

/// Largest gap between two samples that is still interpolated.
const INTERPOLATE_GAP_SECONDS: f32 = 30.0;

/// World position at `clock`, interpolated between neighboring samples.
pub fn world_pos_at(track: &EntityTrack, clock: GameClock) -> Option<WorldPos> {
    let samples = &track.world;
    if samples.is_empty() {
        return None;
    }
    let t = clock.seconds();
    let idx = samples.partition_point(|(c, _)| c.seconds() <= t);
    match (idx.checked_sub(1).map(|i| samples[i]), samples.get(idx)) {
        (Some((c0, p0)), Some((c1, p1))) => {
            let span = c1.seconds() - c0.seconds();
            if span <= 0.0 || span > INTERPOLATE_GAP_SECONDS {
                return if t - c0.seconds() <= HOLD_SECONDS {
                    Some(p0)
                } else if c1.seconds() - t <= HOLD_SECONDS {
                    Some(*p1)
                } else {
                    None
                };
            }
            let f = (t - c0.seconds()) / span;
            Some(WorldPos::new(
                p0.0.x + (p1.0.x - p0.0.x) * f,
                p0.0.y + (p1.0.y - p0.0.y) * f,
                p0.0.z + (p1.0.z - p0.0.z) * f,
            ))
        }
        (Some((c0, p0)), None) => (t - c0.seconds() <= HOLD_SECONDS).then_some(p0),
        (None, Some((c1, p1))) => (c1.seconds() - t <= HOLD_SECONDS).then_some(*p1),
        (None, None) => None,
    }
}

/// Where a sampled position came from.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PosSource {
    /// Position packets: full precision.
    World,
    /// Minimap vision entries: steps of about 2.4 world units (about 73 m),
    /// and only while the ship is shown on the recorder's minimap.
    Minimap,
}

/// World position of a minimap vision entry. The entry stores an 11-bit value
/// over a fixed box of 5000 world units centered on the map, the same
/// decoding the renderer applies before projecting it.
pub fn minimap_world_pos(pos: NormalizedPos) -> WorldPos {
    let raw_x = (pos.0.x + 1.5) * 512.0;
    let raw_y = (pos.0.y + 1.5) * 512.0;
    let x = f64::from(raw_x) / 2047.0 * 5000.0 - 2500.0;
    let z = f64::from(raw_y) / 2047.0 * 5000.0 - 2500.0;
    WorldPos::new(x as f32, 0.0, z as f32)
}

/// The minimap sample nearest to `clock`, when one lies within the hold window.
pub fn minimap_pos_at(track: &EntityTrack, clock: GameClock) -> Option<WorldPos> {
    let samples = &track.minimap;
    let t = clock.seconds();
    let idx = samples.partition_point(|(c, _)| c.seconds() <= t);
    let before = idx.checked_sub(1).map(|i| samples[i]);
    let after = samples.get(idx).copied();
    let nearest = match (before, after) {
        (Some(b), Some(a)) => Some(if t - b.0.seconds() <= a.0.seconds() - t { b } else { a }),
        (Some(b), None) => Some(b),
        (None, Some(a)) => Some(a),
        (None, None) => None,
    }?;
    ((nearest.0.seconds() - t).abs() <= HOLD_SECONDS).then(|| minimap_world_pos(nearest.1))
}

/// Full-precision position when available, else the minimap fallback.
pub fn ship_pos_at(track: &EntityTrack, clock: GameClock) -> Option<(WorldPos, PosSource)> {
    world_pos_at(track, clock)
        .map(|p| (p, PosSource::World))
        .or_else(|| minimap_pos_at(track, clock).map(|p| (p, PosSource::Minimap)))
}

/// Horizontal (x, z) distance between two world positions.
pub fn ground_distance(a: WorldPos, b: WorldPos) -> f32 {
    let dx = a.0.x - b.0.x;
    let dz = a.0.z - b.0.z;
    (dx * dx + dz * dz).sqrt()
}

/// Length of one world unit. Positions, smoke radii and map sizes are in
/// world units; the renderer uses the same factor for its range circles.
pub const METERS_PER_WORLD_UNIT: f32 = 30.0;

pub fn meters(world_units: f32) -> f32 {
    world_units * METERS_PER_WORLD_UNIT
}

pub fn kilometers(world_units: f32) -> f32 {
    meters(world_units) / 1000.0
}

/// World units for a length in meters.
pub fn world_units(meters: f32) -> f32 {
    meters / METERS_PER_WORLD_UNIT
}

#[cfg(test)]
mod tests {
    use super::*;

    fn track(samples: &[(f32, f32)]) -> EntityTrack {
        EntityTrack {
            world: samples.iter().map(|(c, x)| (GameClock(*c), WorldPos::new(*x, 0.0, 0.0))).collect(),
            minimap: Vec::new(),
        }
    }

    #[test]
    fn interpolates_between_samples() {
        let t = track(&[(10.0, 0.0), (20.0, 100.0)]);
        assert_eq!(world_pos_at(&t, GameClock(15.0)).unwrap().0.x, 50.0);
        assert_eq!(world_pos_at(&t, GameClock(10.0)).unwrap().0.x, 0.0);
    }

    #[test]
    fn does_not_bridge_a_long_gap() {
        let t = track(&[(10.0, 0.0), (200.0, 100.0)]);
        assert_eq!(world_pos_at(&t, GameClock(15.0)).unwrap().0.x, 0.0);
        assert!(world_pos_at(&t, GameClock(100.0)).is_none());
        assert_eq!(world_pos_at(&t, GameClock(195.0)).unwrap().0.x, 100.0);
    }

    #[test]
    fn holds_briefly_then_drops() {
        let t = track(&[(10.0, 0.0)]);
        assert!(world_pos_at(&t, GameClock(15.0)).is_some());
        assert!(world_pos_at(&t, GameClock(25.0)).is_none());
        assert!(world_pos_at(&t, GameClock(5.0)).is_some());
        assert!(world_pos_at(&t, GameClock(-5.0)).is_none());
    }
}
