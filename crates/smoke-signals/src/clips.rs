//! Pass three: one MP4 clip per smoke, real time at the configured frame
//! rate, from before the activation until the smoke disperses. Frames carry
//! the same overlays and header as the still frames plus a progress marker.

use std::fs::File;
use std::io::BufWriter;
use std::path::Path;

use muxide::api::MuxerBuilder;
use muxide::api::VideoCodec as MuxideCodec;
use rootcause::prelude::*;
use tracing::info;
use wows_minimap_renderer::VideoCodec;
use wows_minimap_renderer::encoder::EncoderConfig;
use wows_minimap_renderer::encoder::Mode;
use wows_minimap_renderer::encoder::worker::EncoderWorker;
use wows_minimap_renderer::video::FPS as ENCODER_FPS;
use wows_replays::types::GameClock;

use crate::config::Config;
use crate::frames;
use crate::header;
use crate::header::Progress;
use crate::records::GameRecord;
use crate::records::SmokeRecord;
use crate::render::FrameRenderer;
use crate::replays::ReplaySet;
use crate::session::GameData;
use crate::session::GameSession;

/// Clip window in replay seconds.
#[derive(Debug, Clone, Copy)]
pub struct ClipWindow {
    pub start: f32,
    pub end: f32,
}

/// From `clip_pre_seconds` before the activation (or the smoke's appearance
/// when no activation was recorded) until the smoke disperses, or the replay
/// ends.
pub fn clip_window(record: &SmokeRecord, pre_seconds: f32, replay_end: f32) -> ClipWindow {
    let start = (record.activation_moment().seconds - pre_seconds).max(0.0);
    let end = record.t_dispersed.map(|m| m.seconds).unwrap_or(replay_end).min(replay_end);
    ClipWindow { start, end }
}

fn fraction(window: ClipWindow, seconds: f32) -> f32 {
    let span = window.end - window.start;
    if span <= 0.0 { 0.0 } else { ((seconds - window.start) / span).clamp(0.0, 1.0) }
}

/// Render and encode the clip for one smoke. Returns the frame count.
pub fn render_clip(
    config: &Config,
    game_data: &GameData,
    replays: &ReplaySet,
    game: &GameRecord,
    record: &SmokeRecord,
    ordinal: usize,
    types: &std::collections::HashMap<u32, crate::records::SmokeType>,
    path: &Path,
) -> Result<usize, Report> {
    let fps = config.render.clip_fps.max(1);
    let mut session = GameSession::new(game_data, replays)?;
    let mut renderer = FrameRenderer::new(config, game_data, replays, &session)?;
    let window = clip_window(record, config.render.clip_pre_seconds as f32, session.total_duration().seconds());
    if window.end <= window.start {
        bail!("clip window for smoke {} is empty ({:.1} s to {:.1} s)", record.smoke_id, window.start, window.end);
    }
    let (width, frame_height) = renderer.canvas_size();
    let height = header::composed_height(frame_height);
    // H.264 macroblocks: both dimensions must be even.
    let (width, height) = (width & !1, height & !1);

    let (worker, codec, kind) = EncoderWorker::spawn(width, height, VideoCodec::H264, Mode::ForceCpu, EncoderConfig::default())?;
    info!(smoke = record.smoke_id, %codec, %kind, fps, start = window.start, end = window.end, "Encoding clip");

    let activation = fraction(window, record.activation_moment().seconds);
    let capture = record.t_capture.map(|m| fraction(window, m.seconds));
    let frame_count = ((window.end - window.start) * fps as f32).ceil() as usize;
    for n in 0..frame_count {
        let seconds = window.start + n as f32 / fps as f32;
        let clock = GameClock(seconds);
        session.seek_clock(clock)?;
        let snapshot = frames::snapshot_for(&mut session, game, record);
        let text = header::header_text(game, record, ordinal, Some(&snapshot));
        let progress = Progress { activation, capture, now: fraction(window, seconds) };
        let image = frames::render_smoke_frame(&mut renderer, &mut session, config, record, types, clock, &text, Some(progress))?;
        let cropped = image::imageops::crop_imm(&image, 0, 0, width, height).to_image();
        worker.submit(cropped.into_raw())?;
    }
    let output = worker.finish()?;

    let file = File::create(path).attach_with(|| format!("creating {}", path.display()))?;
    let mut muxer = MuxerBuilder::new(BufWriter::new(file))
        .video(MuxideCodec::H264, width, height, f64::from(fps))
        .build()
        .attach_with(|| "initializing MP4 muxer")?;
    for sample in &output.samples {
        // The worker stamps each sample at the renderer's own frame rate from
        // the input frame index; recover the index and restamp at the clip rate.
        let index = (sample.pts_seconds * ENCODER_FPS).round();
        muxer
            .write_video(index / f64::from(fps), &sample.data, sample.is_keyframe)
            .attach_with(|| "writing video frame")?;
    }
    muxer.finish().attach_with(|| "finalizing MP4 container")?;
    info!(smoke = record.smoke_id, path = %path.display(), frames = frame_count, "Clip saved");
    Ok(frame_count)
}

/// Clips for every smoke, recording each file name. Returns the clip count.
pub fn render_clips(
    config: &Config,
    game_data: &GameData,
    replays: &ReplaySet,
    game: &GameRecord,
    smokes: &mut [SmokeRecord],
    selected: &[usize],
    out_dir: &Path,
) -> Result<usize, Report> {
    std::fs::create_dir_all(out_dir).attach_with(|| format!("creating {}", out_dir.display()))?;
    let types = frames::smoke_types(smokes);
    let mut written = 0;
    for &i in selected {
        let stem = frames::file_stem(&smokes[i], i + 1, "clip", smokes[i].activation_moment().clock);
        let name = format!("{stem}.mp4");
        let path = out_dir.join(&name);
        render_clip(config, game_data, replays, game, &smokes[i], i + 1, &types, &path)?;
        smokes[i].clip = Some(name);
        written += 1;
    }
    Ok(written)
}
