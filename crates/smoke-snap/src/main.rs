mod clock;
mod config;
mod render;
mod replays;

use std::path::Path;
use std::path::PathBuf;

use clap::Parser;
use clap::Subcommand;
use rootcause::prelude::*;
use tracing::info;

use crate::clock::BattleClock;
use crate::config::Config;

/// Smoke screen analysis for tournament replays.
#[derive(Parser)]
#[command(name = "smoke_snap")]
struct Args {
    /// Path to config.toml. Relative paths inside it resolve against its directory.
    #[arg(long, default_value = "config.toml")]
    config: PathBuf,

    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Render one merged minimap frame at a battle clock (mm:ss remaining).
    Frame {
        #[arg(long)]
        at: BattleClock,
    },
}

fn main() -> Result<(), Report> {
    tracing_subscriber::fmt().with_target(false).with_writer(std::io::stderr).init();
    let args = Args::parse();
    let config = Config::load(&args.config)?;

    let out_dir = config.paths.output.join(jiff::Zoned::now().strftime("%Y%m%d-%H%M%S").to_string());
    std::fs::create_dir_all(&out_dir).attach_with(|| format!("creating {}", out_dir.display()))?;

    match args.command {
        Command::Frame { at } => {
            let replays = replays::load_game_folder(&config.paths.replays, &config.run.team_prefix, config.run.merge)?;
            info!(primary = %replays.primary_path.display(), player = %replays.primary.meta.playerName, "Primary replay");
            for (path, file) in replays.merge_paths.iter().zip(&replays.merges) {
                info!(merge = %path.display(), player = %file.meta.playerName, "Merge replay");
            }
            let game = render::load_game_data(&config.paths.game_data, &replays.primary)?;
            info!(build_dir = %game.build_dir.display(), "Game data");
            let frame = render::render_frame_at(&config, &game, &replays, at, &out_dir)?;
            write_run_log(&out_dir, &replays, &game, &frame)?;
            println!("{}", frame.path.display());
        }
    }
    Ok(())
}

/// Record the inputs and the clock placement next to the outputs.
fn write_run_log(
    out_dir: &Path,
    replays: &replays::ReplaySet,
    game: &render::GameData,
    frame: &render::RenderedFrame,
) -> Result<(), Report> {
    use std::fmt::Write as _;

    let mut log = String::new();
    let _ = writeln!(log, "# smoke_snap run log\n");
    let _ = writeln!(log, "- generated_at: {}", jiff::Zoned::now().strftime("%Y-%m-%d %H:%M:%S %Z"));
    let _ = writeln!(log, "- game_build: {}", replays.primary.meta.clientVersionFromExe);
    let _ = writeln!(log, "- game_data: {}", game.build_dir.display());
    let _ = writeln!(log, "- map: {}", replays.primary.meta.mapName);
    let _ = writeln!(
        log,
        "- primary_replay: {} (recorded by {})",
        replays.primary_path.display(),
        replays.primary.meta.playerName
    );
    for (path, file) in replays.merge_paths.iter().zip(&replays.merges) {
        let _ = writeln!(log, "- merged_replay: {} (recorded by {})", path.display(), file.meta.playerName);
    }
    let _ = writeln!(log, "\n## Frame\n");
    let _ = writeln!(log, "- file: {}", frame.path.file_name().map(|n| n.to_string_lossy()).unwrap_or_default());
    let _ = writeln!(log, "- battle_clock: {}", frame.at);
    let _ = writeln!(log, "- replay_seconds: {:.2}", frame.point.clock.seconds());
    let _ =
        writeln!(log, "- replay_seconds_estimate (battle start plus elapsed): {:.2}", frame.point.estimate.seconds());
    let _ = writeln!(log, "- hud_countdown_seconds: {}", frame.point.hud);
    let path = out_dir.join("run_log.md");
    std::fs::write(&path, log).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}
