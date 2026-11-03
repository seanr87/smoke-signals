//! The zoomed inset: a magnified copy of the map around the target smoke,
//! placed in the map corner farthest from the smoke, with a thin border and
//! a scale note.

use image::Rgb;
use image::RgbImage;
use image::imageops::FilterType;
use wows_minimap_renderer::GameFonts;
use wows_minimap_renderer::map_data::MinimapPos;

use crate::header;

/// Smallest half side of the magnified region, in map pixels.
const MIN_HALF_PX: f32 = 40.0;
/// Largest side of the inset on the frame, in pixels; the zoom is reduced
/// when the region would not fit.
const MAX_SIDE_PX: f32 = 340.0;
/// Smallest magnification worth drawing. A region too large for it is cut
/// down to its center.
const MIN_ZOOM: f32 = 1.5;
/// Gap between the inset and the map edge.
const MARGIN_PX: u32 = 8;
const BORDER: Rgb<u8> = Rgb([225, 225, 225]);
const NOTE_TEXT: [u8; 3] = [255, 255, 255];
const NOTE_SHADOW: [u8; 3] = [0, 0, 0];

/// Square region of the map to magnify, in map pixels.
#[derive(Debug, Clone, Copy)]
pub struct Region {
    pub center: MinimapPos,
    pub half: f32,
}

/// The square around `points`, each padded by `pad`.
pub fn region_around(points: &[MinimapPos], pad: f32) -> Option<Region> {
    let first = points.first()?;
    let (mut min_x, mut min_y, mut max_x, mut max_y) = (first.x, first.y, first.x, first.y);
    for p in points {
        min_x = min_x.min(p.x);
        min_y = min_y.min(p.y);
        max_x = max_x.max(p.x);
        max_y = max_y.max(p.y);
    }
    let half = ((max_x - min_x).max(max_y - min_y) / 2.0 + pad).max(MIN_HALF_PX);
    Some(Region { center: MinimapPos { x: (min_x + max_x) / 2.0, y: (min_y + max_y) / 2.0 }, half })
}

/// A built inset and the magnification it ended up with.
pub struct Inset {
    pub image: RgbImage,
    pub zoom: f32,
}

/// Where the map sits on the frame.
#[derive(Debug, Clone, Copy)]
pub struct MapRect {
    pub x: u32,
    pub y: u32,
    pub size: u32,
}

/// Side of the map square to magnify and the magnification: the region at
/// `zoom_factor` when it fits, else as much of the region as fits at a
/// lower zoom, never below [`MIN_ZOOM`].
fn fit(region: Region, map: MapRect, zoom_factor: f32) -> (u32, f32) {
    let wanted = (region.half * 2.0).round().clamp(1.0, map.size as f32);
    let zoom = zoom_factor.min(MAX_SIDE_PX / wanted);
    if zoom >= MIN_ZOOM {
        (wanted as u32, zoom)
    } else {
        ((MAX_SIDE_PX / MIN_ZOOM).floor().min(map.size as f32) as u32, MIN_ZOOM)
    }
}

/// The square of `side` map pixels centered on `center`, clamped to the
/// map's edges.
fn crop_rect(center: MinimapPos, side: u32, map: MapRect) -> (u32, u32) {
    let limit = (map.size - side) as f32;
    let half = side as f32 / 2.0;
    let x = (center.x - half).round().clamp(0.0, limit) as u32;
    let y = (center.y - half).round().clamp(0.0, limit) as u32;
    (x, y)
}

/// Cut `region` out of `frame`, magnify it by up to `zoom_factor`, add the
/// border and the scale note. `px_per_km` is the map scale before zooming.
pub fn build(
    frame: &RgbImage,
    map: MapRect,
    region: Region,
    zoom_factor: f32,
    px_per_km: f32,
    fonts: &GameFonts,
) -> Inset {
    let (side, zoom) = fit(region, map, zoom_factor);
    let (x, y) = crop_rect(region.center, side, map);
    let crop = image::imageops::crop_imm(frame, map.x + x, map.y + y, side, side).to_image();
    let out_side = (side as f32 * zoom).round().max(1.0) as u32;
    let zoom = out_side as f32 / side as f32;
    let scaled = image::imageops::resize(&crop, out_side, out_side, FilterType::CatmullRom);

    let mut image = RgbImage::from_pixel(out_side + 2, out_side + 2, BORDER);
    image::imageops::replace(&mut image, &scaled, 1, 1);
    draw_scale_note(&mut image, fonts, zoom, px_per_km * zoom);
    Inset { image, zoom }
}

/// A 1 km bar at the bottom left and the magnification at the bottom right.
fn draw_scale_note(image: &mut RgbImage, fonts: &GameFonts, zoom: f32, px_per_km: f32) {
    let (w, h) = (image.width() as i32, image.height() as i32);
    let size = 12.0;
    let bar_y = h - 8;
    let bar_len = px_per_km.round() as i32;
    let bar_fits = bar_len > 0 && bar_len < w / 2;
    if bar_fits {
        for px in 6..6 + bar_len {
            for py in bar_y..bar_y + 2 {
                put(image, px + 1, py + 1, NOTE_SHADOW);
                put(image, px, py, NOTE_TEXT);
            }
        }
        shadowed_text(image, fonts, size, 6.0, (bar_y - 16) as f32, "1 km");
    }
    let note = format!("{zoom:.1}x");
    let width = header::text_width(fonts, size, &note);
    shadowed_text(image, fonts, size, w as f32 - width - 6.0, (h - 20) as f32, &note);
}

fn put(image: &mut RgbImage, x: i32, y: i32, color: [u8; 3]) {
    if x >= 0 && y >= 0 && x < image.width() as i32 && y < image.height() as i32 {
        image.put_pixel(x as u32, y as u32, Rgb(color));
    }
}

fn shadowed_text(image: &mut RgbImage, fonts: &GameFonts, size: f32, x: f32, y: f32, text: &str) {
    header::draw_text(image, fonts, size, x + 1.0, y + 1.0, NOTE_SHADOW, text);
    header::draw_text(image, fonts, size, x, y, NOTE_TEXT, text);
}

/// Paste `inset` into the map corner farthest from `region`.
pub fn place(frame: &mut RgbImage, map: MapRect, region: Region, inset: &RgbImage) {
    let (w, h) = (inset.width(), inset.height());
    if w + 2 * MARGIN_PX > map.size || h + 2 * MARGIN_PX > map.size {
        return;
    }
    let far = map.size - MARGIN_PX;
    let corners = [(MARGIN_PX, MARGIN_PX), (far - w, MARGIN_PX), (MARGIN_PX, far - h), (far - w, far - h)];
    let (x, y) = corners
        .into_iter()
        .max_by(|a, b| corner_distance(*a, w, h, region).total_cmp(&corner_distance(*b, w, h, region)))
        .expect("four corners");
    image::imageops::replace(frame, inset, i64::from(map.x + x), i64::from(map.y + y));
}

fn corner_distance(corner: (u32, u32), w: u32, h: u32, region: Region) -> f32 {
    let cx = corner.0 as f32 + w as f32 / 2.0;
    let cy = corner.1 as f32 + h as f32 / 2.0;
    ((cx - region.center.x).powi(2) + (cy - region.center.y).powi(2)).sqrt()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn region_is_square_and_padded() {
        let r = region_around(&[MinimapPos { x: 100.0, y: 100.0 }, MinimapPos { x: 300.0, y: 150.0 }], 10.0)
            .expect("region");
        assert_eq!(r.center.x, 200.0);
        assert_eq!(r.center.y, 125.0);
        assert_eq!(r.half, 110.0);
    }

    #[test]
    fn small_region_has_minimum_size() {
        let r = region_around(&[MinimapPos { x: 5.0, y: 5.0 }], 0.0).expect("region");
        assert_eq!(r.half, MIN_HALF_PX);
    }

    #[test]
    fn crop_stays_inside_the_map() {
        let map = MapRect { x: 0, y: 0, size: 768 };
        assert_eq!(crop_rect(MinimapPos { x: 10.0, y: 760.0 }, 100, map), (0, 668));
        assert_eq!(crop_rect(MinimapPos { x: 384.0, y: 384.0 }, 768, map), (0, 0));
    }

    #[test]
    fn fit_keeps_the_zoom_when_the_region_is_small() {
        let map = MapRect { x: 0, y: 0, size: 768 };
        let (side, zoom) = fit(Region { center: MinimapPos { x: 0.0, y: 0.0 }, half: 50.0 }, map, 2.5);
        assert_eq!((side, zoom), (100, 2.5));
    }

    #[test]
    fn fit_lowers_the_zoom_for_a_wide_region() {
        let map = MapRect { x: 0, y: 0, size: 768 };
        let (side, zoom) = fit(Region { center: MinimapPos { x: 0.0, y: 0.0 }, half: 100.0 }, map, 2.5);
        assert_eq!(side, 200);
        assert!((zoom - 1.7).abs() < 0.01);
    }

    #[test]
    fn fit_cuts_a_huge_region_down_to_the_minimum_zoom() {
        let map = MapRect { x: 0, y: 0, size: 768 };
        let (side, zoom) = fit(Region { center: MinimapPos { x: 0.0, y: 0.0 }, half: 300.0 }, map, 2.5);
        assert_eq!((side, zoom), (226, MIN_ZOOM));
    }

    #[test]
    fn far_corner_is_chosen() {
        let map = MapRect { x: 0, y: 0, size: 768 };
        let region = Region { center: MinimapPos { x: 700.0, y: 700.0 }, half: 40.0 };
        let mut frame = RgbImage::from_pixel(768, 768, Rgb([0, 0, 0]));
        let inset = RgbImage::from_pixel(50, 50, Rgb([255, 255, 255]));
        place(&mut frame, map, region, &inset);
        assert_eq!(frame.get_pixel(MARGIN_PX + 1, MARGIN_PX + 1).0, [255, 255, 255]);
        assert_eq!(frame.get_pixel(700, 700).0, [0, 0, 0]);
    }
}
