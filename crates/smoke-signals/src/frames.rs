//! Pass two: a capture frame per smoke, with the smoke's puffs outlined in
//! the highlight color.

use std::path::Path;

use rootcause::prelude::*;
use tracing::info;
use wows_replays::types::EntityId;
use wows_replays::types::GameClock;
use wowsunpack::game_types::WorldPos;

use crate::config::Config;
use crate::records::SmokeRecord;
use crate::render::FrameRenderer;
use crate::replays::ReplaySet;
use crate::session::GameData;
use crate::session::GameSession;

/// Keep letters, digits, `-` and `.`; everything else becomes `_`.
fn sanitize(text: &str) -> String {
    text.chars().map(|c| if c.is_ascii_alphanumeric() || c == '-' || c == '.' { c } else { '_' }).collect()
}

/// `<match>_<game>_<team>_<player>_<ship>_s<nn>_<stage>_<mmss>`. A smoke
/// without an owner is named `unowned`, since the file still has to exist.
fn frame_name(record: &SmokeRecord, ordinal: usize, stage: &str) -> String {
    let game = record.game_no.map(|n| format!("g{n}")).unwrap_or_else(|| "g".to_string());
    let clock = record.t_capture.and_then(|m| m.clock).map(|c| c.compact()).unwrap_or_else(|| "none".to_string());
    let owner = match (&record.team, &record.player, &record.ship) {
        (Some(team), Some(player), Some(ship)) => format!("{team}_{player}_{ship}"),
        _ => "unowned".to_string(),
    };
    sanitize(&format!("{}_{game}_{owner}_s{ordinal:02}_{stage}_{clock}", record.match_id))
}

/// Render the capture frame of every smoke that has one, in clock order, and
/// record each file name on its record. `out_dir` receives the PNGs.
pub fn render_capture_frames(
    config: &Config,
    game: &GameData,
    replays: &ReplaySet,
    smokes: &mut [SmokeRecord],
    out_dir: &Path,
) -> Result<usize, Report> {
    std::fs::create_dir_all(out_dir).attach_with(|| format!("creating {}", out_dir.display()))?;
    let mut session = GameSession::new(game, replays)?;
    let mut renderer = FrameRenderer::new(config, game, replays, &session)?;
    let color = config.render.highlight_color.rgba(255);

    let mut order: Vec<usize> = (0..smokes.len()).filter(|i| smokes[*i].t_capture.is_some()).collect();
    order.sort_by(|a, b| {
        let ta = smokes[*a].t_capture.map(|m| m.seconds).unwrap_or(0.0);
        let tb = smokes[*b].t_capture.map(|m| m.seconds).unwrap_or(0.0);
        ta.total_cmp(&tb)
    });

    let mut written = 0;
    for (ordinal, i) in order.iter().enumerate() {
        let record = &smokes[*i];
        let Some(capture) = record.t_capture else { continue };
        let clock = GameClock(capture.seconds);
        session.seek_clock(clock)?;
        let id = EntityId::from(record.smoke_id);
        let puffs: Vec<WorldPos> = {
            let view = session.view();
            view.smoke_screens().get(&id).map(|s| s.points.clone()).ok_or_else(|| {
                report!(
                    "smoke {} is absent from the merged state at its capture clock {:.2} s",
                    record.smoke_id,
                    capture.seconds
                )
            })?
        };
        let overlay = renderer.rings(&puffs, record.radius, color);
        let name = format!("{}.png", frame_name(record, ordinal + 1, "cap"));
        let path = out_dir.join(&name);
        renderer.render_png(&mut session, clock, &overlay, &path)?;
        info!(smoke = record.smoke_id, file = %name, puffs = puffs.len(), "Capture frame");
        smokes[*i].frame_cap = Some(name);
        written += 1;
    }
    Ok(written)
}
