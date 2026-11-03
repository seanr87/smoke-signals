//! The header strip above a frame and the footer below it, drawn with the
//! game's own font. Text is ASCII: `|` separates fields and `->` joins the
//! activation and capture clocks.

use ab_glyph::Font;
use ab_glyph::FontArc;
use ab_glyph::PxScale;
use ab_glyph::ScaleFont;
use ab_glyph::point;
use image::Rgb;
use image::RgbImage;
use wows_minimap_renderer::GameFonts;

use crate::records::GameRecord;
use crate::records::SmokeRecord;
use crate::records::StateSnapshot;

pub const HEADER_HEIGHT: u32 = 64;
pub const FOOTER_HEIGHT: u32 = 22;
const BACKGROUND: Rgb<u8> = Rgb([18, 22, 28]);
const TEXT: [u8; 3] = [235, 235, 235];
const TEXT_DIM: [u8; 3] = [170, 175, 185];
const BAR_TRACK: Rgb<u8> = Rgb([60, 66, 76]);
const BAR_DONE: Rgb<u8> = Rgb([120, 190, 255]);
const BAR_MARK: Rgb<u8> = Rgb([255, 215, 0]);

/// The three text lines of a frame.
#[derive(Debug, Clone)]
pub struct HeaderText {
    pub line1: String,
    pub line2: String,
    pub footer: String,
}

/// Clip progress: activation and capture as fractions of the clip, and now.
#[derive(Debug, Clone, Copy)]
pub struct Progress {
    pub activation: f32,
    pub capture: Option<f32>,
    pub now: f32,
}

fn opt_num<T: std::fmt::Display>(v: Option<T>) -> String {
    v.map(|v| v.to_string()).unwrap_or_else(|| "?".to_string())
}

/// Header lines for one smoke. `ordinal` is the smoke's number in the table;
/// `state` is the Tier 1 state at the frame's moment.
pub fn header_text(
    game: &GameRecord,
    record: &SmokeRecord,
    ordinal: usize,
    state: Option<&StateSnapshot>,
) -> HeaderText {
    let class = record.ship_class.as_deref().map(class_abbrev).unwrap_or("?");
    let tier = record.ship_tier.map(roman).unwrap_or_else(|| "?".to_string());
    let smoke = match record.smoke_type {
        Some(t) => format!("{} smoke", t.as_str()),
        None => "smoke (type unknown)".to_string(),
    };
    let charge = match (record.charge_no, record.charges_total) {
        (Some(n), Some(total)) => format!(", charge {n}/{total}"),
        (Some(n), None) => format!(", charge {n}"),
        _ => String::new(),
    };
    let act = record.t_activate.map(|m| m.clock_text()).unwrap_or_else(|| "no activation".to_string());
    let cap = record.t_capture.map(|m| m.clock_text()).unwrap_or_else(|| "?".to_string());
    let emission = record.observed_emission_s.map(|e| format!(" ({e:.0} s)")).unwrap_or_default();
    let line1 = format!(
        "#{ordinal} | {} | {} | {} ({class} {tier}) | {smoke}{charge} | {act} -> {cap}{emission}",
        record.team.as_deref().unwrap_or("?"),
        record.player.as_deref().unwrap_or("unknown owner"),
        record.ship.as_deref().unwrap_or("?")
    );

    let base = match (record.base_emission_s, record.base_puff_life_s) {
        (Some(e), Some(l)) => format!("emission base {e:.0} s | puff life {l:.0} s"),
        (Some(e), None) => format!("emission base {e:.0} s"),
        _ => "base stats unknown".to_string(),
    };
    let line2 = match state {
        Some(s) => {
            let spotted = match (s.smoker_spotted, &s.smoker_spotted_flags) {
                (Some(true), Some(flags)) => format!("yes ({flags})"),
                (Some(true), None) => "yes".to_string(),
                (Some(false), _) => "no".to_string(),
                (None, _) => "?".to_string(),
            };
            format!(
                "{base} | Score {}-{} | Caps {} | Alive {}v{} | HP {} | Spotted {} | Enemy radars {}",
                opt_num(s.score_ours),
                opt_num(s.score_theirs),
                s.caps_text(),
                opt_num(s.alive_ours),
                opt_num(s.alive_theirs),
                s.smoker_hp_pct.map(|p| format!("{p:.0}%")).unwrap_or_else(|| "?".to_string()),
                spotted,
                opt_num(s.enemy_radars_alive)
            )
        }
        None => base,
    };

    let mut footer: Vec<String> = Vec::new();
    if let Some(t) = &game.tournament {
        footer.push(t.clone());
    }
    let mut round = game.round.clone().unwrap_or_else(|| game.match_id.clone());
    if let Some(n) = game.game_no {
        round.push_str(&format!(" G{n}"));
    }
    footer.push(round);
    footer.push(game.map_title());
    footer.push(game.game_build.split(',').take(3).collect::<Vec<_>>().join("."));
    HeaderText { line1, line2, footer: footer.join(" | ") }
}

fn class_abbrev(class: &str) -> &str {
    match class {
        "Destroyer" => "DD",
        "Cruiser" => "CA",
        "Battleship" => "BB",
        "AirCarrier" => "CV",
        "Submarine" => "SS",
        other => other,
    }
}

fn roman(tier: u32) -> String {
    const NUMERALS: [&str; 11] = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"];
    NUMERALS.get(tier.wrapping_sub(1) as usize).map(|s| s.to_string()).unwrap_or_else(|| tier.to_string())
}

/// Text drawn with the game font. Returns the caret x after the text.
pub fn draw_text(
    image: &mut RgbImage,
    fonts: &GameFonts,
    size: f32,
    x: f32,
    y: f32,
    color: [u8; 3],
    text: &str,
) -> f32 {
    let scale = PxScale::from(size * fonts.primary_scale_factor);
    draw_with_font(image, &fonts.primary, scale, x, y, color, text)
}

fn draw_with_font(
    image: &mut RgbImage,
    font: &FontArc,
    scale: PxScale,
    x: f32,
    y: f32,
    color: [u8; 3],
    text: &str,
) -> f32 {
    let scaled = font.as_scaled(scale);
    let baseline = y + scaled.ascent();
    let mut caret = x;
    let mut previous = None;
    let (width, height) = (image.width() as i32, image.height() as i32);
    for ch in text.chars() {
        let id = scaled.glyph_id(ch);
        if let Some(prev) = previous {
            caret += scaled.kern(prev, id);
        }
        let glyph = id.with_scale_and_position(scale, point(caret, baseline));
        if let Some(outlined) = scaled.outline_glyph(glyph) {
            let bounds = outlined.px_bounds();
            outlined.draw(|gx, gy, coverage| {
                let px = bounds.min.x as i32 + gx as i32;
                let py = bounds.min.y as i32 + gy as i32;
                if px < 0 || py < 0 || px >= width || py >= height || coverage <= 0.0 {
                    return;
                }
                let pixel = image.get_pixel_mut(px as u32, py as u32);
                for c in 0..3 {
                    let base = f32::from(pixel.0[c]);
                    pixel.0[c] = (base + (f32::from(color[c]) - base) * coverage.min(1.0)).round() as u8;
                }
            });
        }
        caret += scaled.h_advance(id);
        previous = Some(id);
    }
    caret
}

/// Width of `text` at `size`, in pixels.
pub fn text_width(fonts: &GameFonts, size: f32, text: &str) -> f32 {
    let scaled = fonts.primary.as_scaled(PxScale::from(size * fonts.primary_scale_factor));
    let mut width = 0.0;
    let mut previous = None;
    for ch in text.chars() {
        let id = scaled.glyph_id(ch);
        if let Some(prev) = previous {
            width += scaled.kern(prev, id);
        }
        width += scaled.h_advance(id);
        previous = Some(id);
    }
    width
}

/// `text` cut to `max_width` with a trailing `..` when it does not fit.
pub fn fit_text(fonts: &GameFonts, size: f32, max_width: f32, text: &str) -> String {
    if text_width(fonts, size, text) <= max_width {
        return text.to_string();
    }
    let chars: Vec<char> = text.chars().collect();
    let mut end = chars.len();
    while end > 0 {
        end -= 1;
        let candidate: String = chars[..end].iter().collect::<String>() + "..";
        if text_width(fonts, size, &candidate) <= max_width {
            return candidate;
        }
    }
    "..".to_string()
}

/// Rendered frame height once the header and footer are added.
pub fn composed_height(frame_height: u32) -> u32 {
    HEADER_HEIGHT + frame_height + FOOTER_HEIGHT
}

/// The frame with the header strip above it and the footer below.
pub fn compose(frame: &RgbImage, fonts: &GameFonts, text: &HeaderText, progress: Option<Progress>) -> RgbImage {
    let width = frame.width();
    let max = width as f32 - 16.0;
    let mut out = RgbImage::from_pixel(width, composed_height(frame.height()), BACKGROUND);
    draw_text(&mut out, fonts, 17.0, 8.0, 4.0, TEXT, &fit_text(fonts, 17.0, max, &text.line1));
    draw_text(&mut out, fonts, 14.0, 8.0, 27.0, TEXT_DIM, &fit_text(fonts, 14.0, max, &text.line2));
    if let Some(p) = progress {
        draw_progress(&mut out, p, 8, HEADER_HEIGHT as i32 - 12, width as i32 - 16);
    }
    image::imageops::replace(&mut out, frame, 0, i64::from(HEADER_HEIGHT));
    let footer_y = HEADER_HEIGHT + frame.height();
    draw_text(&mut out, fonts, 13.0, 8.0, footer_y as f32 + 3.0, TEXT_DIM, &fit_text(fonts, 13.0, max, &text.footer));
    out
}

/// A thin bar: filled up to `now`, with marks at activation and capture.
fn draw_progress(image: &mut RgbImage, p: Progress, x: i32, y: i32, width: i32) {
    let height = 6;
    let fill = |image: &mut RgbImage, x0: i32, x1: i32, color: Rgb<u8>| {
        for px in x0.max(0)..x1.min(image.width() as i32) {
            for py in y..y + height {
                if py >= 0 && py < image.height() as i32 {
                    image.put_pixel(px as u32, py as u32, color);
                }
            }
        }
    };
    let at = |f: f32| x + (f.clamp(0.0, 1.0) * width as f32) as i32;
    fill(image, x, x + width, BAR_TRACK);
    fill(image, x, at(p.now), BAR_DONE);
    for mark in [Some(p.activation), p.capture].into_iter().flatten() {
        let mx = at(mark);
        fill(image, mx - 1, mx + 2, BAR_MARK);
    }
    let nx = at(p.now);
    fill(image, nx - 1, nx + 2, Rgb([255, 255, 255]));
}
