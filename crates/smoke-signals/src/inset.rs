//! The zoomed view: a magnified crop of the map around the target smoke,
//! saved on its own, with a scale note and the credited fire lines.

use image::Rgb;
use image::RgbImage;
use image::imageops::FilterType;
use wows_minimap_renderer::GameFonts;
use wows_minimap_renderer::map_data::MinimapPos;

use crate::header;

const NOTE_TEXT: [u8; 3] = [255, 255, 255];
const NOTE_SHADOW: [u8; 3] = [0, 0, 0];
const LABEL_BACK: [u8; 3] = [7, 19, 31];
/// Stroke of a fire line on the zoomed view, in output pixels.
const LINE_WIDTH: f32 = 2.5;
const LABEL_SIZE: f32 = 13.0;
const ARROW_HEAD_PX: f32 = 9.0;

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
    let half = (max_x - min_x).max(max_y - min_y) / 2.0 + pad;
    Some(Region { center: MinimapPos { x: (min_x + max_x) / 2.0, y: (min_y + max_y) / 2.0 }, half })
}

/// A built zoom image, its magnification and the map pixel at its top left.
pub struct Inset {
    pub image: RgbImage,
    pub zoom: f32,
    pub origin: (u32, u32),
}

impl Inset {
    /// Where a map pixel lands on the zoom image.
    pub fn to_image(&self, p: MinimapPos) -> (f32, f32) {
        ((p.x - self.origin.0 as f32) * self.zoom + 1.0, (p.y - self.origin.1 as f32) * self.zoom + 1.0)
    }
}

/// Where the map sits on the frame.
#[derive(Debug, Clone, Copy)]
pub struct MapRect {
    pub x: u32,
    pub y: u32,
    pub size: u32,
}

/// The square of `side` map pixels centered on `center`, kept within the
/// map.
fn crop_rect(center: MinimapPos, side: u32, map: MapRect) -> (u32, u32) {
    let limit = (map.size - side) as f32;
    let half = side as f32 / 2.0;
    let x = (center.x - half).round().clamp(0.0, limit) as u32;
    let y = (center.y - half).round().clamp(0.0, limit) as u32;
    (x, y)
}

/// Cut `region` out of `frame`, magnify it to `out_side` pixels, add the
/// border and the scale note. `px_per_km` is the map scale before zooming.
pub fn build(frame: &RgbImage, map: MapRect, region: Region, out_side: u32, px_per_km: f32, fonts: &GameFonts) -> Inset {
    let side = (region.half * 2.0).round().clamp(1.0, map.size as f32) as u32;
    let (x, y) = crop_rect(region.center, side, map);
    let crop = image::imageops::crop_imm(frame, map.x + x, map.y + y, side, side).to_image();
    let out_side = out_side.max(1);
    let zoom = out_side as f32 / side as f32;
    let scaled = image::imageops::resize(&crop, out_side, out_side, FilterType::CatmullRom);

    let mut image = RgbImage::from_pixel(out_side + 2, out_side + 2, Rgb(NOTE_TEXT));
    image::imageops::replace(&mut image, &scaled, 1, 1);
    draw_scale_note(&mut image, fonts, zoom, px_per_km * zoom);
    Inset { image, zoom, origin: (x, y) }
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

/// A credited fire line on the zoom image, from the shooter to the target,
/// in image pixels.
pub struct FireLine {
    pub from: (f32, f32),
    pub to: (f32, f32),
    pub damage: f32,
}

/// Draw every fire line with an arrow head, then the damage labels on top.
pub fn draw_fire_lines(inset: &mut Inset, fonts: &GameFonts, lines: &[FireLine], color: [u8; 3]) {
    for line in lines {
        draw_line(&mut inset.image, line.from, line.to, LINE_WIDTH + 2.0, NOTE_SHADOW);
        draw_line(&mut inset.image, line.from, line.to, LINE_WIDTH, color);
        draw_arrow_head(&mut inset.image, line.from, line.to, color);
    }
    for line in lines {
        let label = thousands(line.damage.round() as i64);
        let width = header::text_width(fonts, LABEL_SIZE, &label);
        let (mx, my) = ((line.from.0 + line.to.0) / 2.0, (line.from.1 + line.to.1) / 2.0);
        let (x, y) = (mx - width / 2.0, my - LABEL_SIZE / 2.0 - 2.0);
        fill_rect(&mut inset.image, x - 3.0, y - 1.0, width + 6.0, LABEL_SIZE + 5.0, LABEL_BACK);
        header::draw_text(&mut inset.image, fonts, LABEL_SIZE, x, y, color, &label);
    }
}

/// A numbered marker on an allied ship, in image pixels.
pub struct Badge {
    pub at: (f32, f32),
    pub number: u32,
}

const BADGE_RADIUS: f32 = 9.0;
const BADGE_SIZE: f32 = 12.0;

/// Draw each badge as a filled disc with its number, offset up and right of
/// the ship so the icon stays visible.
pub fn draw_badges(inset: &mut Inset, fonts: &GameFonts, badges: &[Badge], color: [u8; 3]) {
    for b in badges {
        let (cx, cy) = (b.at.0 + BADGE_RADIUS + 3.0, b.at.1 - BADGE_RADIUS - 3.0);
        fill_circle(&mut inset.image, cx, cy, BADGE_RADIUS + 1.5, NOTE_SHADOW);
        fill_circle(&mut inset.image, cx, cy, BADGE_RADIUS, color);
        let label = b.number.to_string();
        let width = header::text_width(fonts, BADGE_SIZE, &label);
        header::draw_text(&mut inset.image, fonts, BADGE_SIZE, cx - width / 2.0, cy - BADGE_SIZE / 2.0 - 1.0, LABEL_BACK, &label);
    }
}

fn fill_circle(image: &mut RgbImage, cx: f32, cy: f32, r: f32, color: [u8; 3]) {
    for py in (cy - r).floor() as i32..=(cy + r).ceil() as i32 {
        for px in (cx - r).floor() as i32..=(cx + r).ceil() as i32 {
            let (dx, dy) = (px as f32 + 0.5 - cx, py as f32 + 0.5 - cy);
            if dx * dx + dy * dy <= r * r {
                put(image, px, py, color);
            }
        }
    }
}

fn thousands(v: i64) -> String {
    let digits = v.abs().to_string();
    let mut out = String::new();
    for (i, c) in digits.chars().enumerate() {
        if i > 0 && (digits.len() - i) % 3 == 0 {
            out.push(',');
        }
        out.push(c);
    }
    if v < 0 { format!("-{out}") } else { out }
}

fn draw_line(image: &mut RgbImage, a: (f32, f32), b: (f32, f32), width: f32, color: [u8; 3]) {
    let (dx, dy) = (b.0 - a.0, b.1 - a.1);
    let len = (dx * dx + dy * dy).sqrt();
    if len <= 0.0 {
        return;
    }
    let steps = (len * 2.0).ceil() as i32;
    let r = width / 2.0;
    for i in 0..=steps {
        let t = i as f32 / steps as f32;
        fill_disc(image, a.0 + dx * t, a.1 + dy * t, r, color);
    }
}

fn draw_arrow_head(image: &mut RgbImage, a: (f32, f32), b: (f32, f32), color: [u8; 3]) {
    let (dx, dy) = (b.0 - a.0, b.1 - a.1);
    let len = (dx * dx + dy * dy).sqrt();
    if len <= 0.0 {
        return;
    }
    let (ux, uy) = (dx / len, dy / len);
    let base = (b.0 - ux * ARROW_HEAD_PX, b.1 - uy * ARROW_HEAD_PX);
    let (px, py) = (-uy * ARROW_HEAD_PX * 0.5, ux * ARROW_HEAD_PX * 0.5);
    fill_triangle(image, b, (base.0 + px, base.1 + py), (base.0 - px, base.1 - py), color);
}

fn fill_disc(image: &mut RgbImage, cx: f32, cy: f32, r: f32, color: [u8; 3]) {
    let (x0, x1) = ((cx - r).floor() as i32, (cx + r).ceil() as i32);
    let (y0, y1) = ((cy - r).floor() as i32, (cy + r).ceil() as i32);
    for y in y0..=y1 {
        for x in x0..=x1 {
            if (x as f32 + 0.5 - cx).powi(2) + (y as f32 + 0.5 - cy).powi(2) <= r * r {
                put(image, x, y, color);
            }
        }
    }
}

fn fill_triangle(image: &mut RgbImage, a: (f32, f32), b: (f32, f32), c: (f32, f32), color: [u8; 3]) {
    let (x0, x1) = (a.0.min(b.0).min(c.0).floor() as i32, a.0.max(b.0).max(c.0).ceil() as i32);
    let (y0, y1) = (a.1.min(b.1).min(c.1).floor() as i32, a.1.max(b.1).max(c.1).ceil() as i32);
    let edge = |p: (f32, f32), q: (f32, f32), r: (f32, f32)| (q.0 - p.0) * (r.1 - p.1) - (q.1 - p.1) * (r.0 - p.0);
    if edge(a, b, c) == 0.0 {
        return;
    }
    for y in y0..=y1 {
        for x in x0..=x1 {
            let p = (x as f32 + 0.5, y as f32 + 0.5);
            let (w0, w1, w2) = (edge(a, b, p), edge(b, c, p), edge(c, a, p));
            if (w0 >= 0.0 && w1 >= 0.0 && w2 >= 0.0) || (w0 <= 0.0 && w1 <= 0.0 && w2 <= 0.0) {
                put(image, x, y, color);
            }
        }
    }
}

fn fill_rect(image: &mut RgbImage, x: f32, y: f32, w: f32, h: f32, color: [u8; 3]) {
    for py in y.round() as i32..(y + h).round() as i32 {
        for px in x.round() as i32..(x + w).round() as i32 {
            put(image, px, py, color);
        }
    }
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
    fn crop_stays_inside_the_map() {
        let map = MapRect { x: 0, y: 0, size: 768 };
        assert_eq!(crop_rect(MinimapPos { x: 10.0, y: 760.0 }, 100, map), (0, 668));
        assert_eq!(crop_rect(MinimapPos { x: 384.0, y: 384.0 }, 768, map), (0, 0));
    }

    #[test]
    fn clamped_crop_maps_map_pixels_onto_the_image() {
        let inset = Inset { image: RgbImage::new(770, 770), zoom: 2.0, origin: (384, 0) };
        assert_eq!(inset.to_image(MinimapPos { x: 384.0, y: 0.0 }), (1.0, 1.0));
        assert_eq!(inset.to_image(MinimapPos { x: 584.0, y: 100.0 }), (401.0, 201.0));
    }

    #[test]
    fn thousands_are_grouped() {
        assert_eq!(thousands(80520), "80,520");
        assert_eq!(thousands(999), "999");
        assert_eq!(thousands(-1234567), "-1,234,567");
    }
}
