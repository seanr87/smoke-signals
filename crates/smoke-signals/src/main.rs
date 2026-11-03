use std::path::Path;
use std::path::PathBuf;

use clap::Parser;
use clap::Subcommand;
use rootcause::prelude::*;
use tracing::info;
use wowsunpack::game_params::types::GameParamProvider;

use smoke_signals::analysis;
use smoke_signals::clips;
use smoke_signals::clock::BattleClock;
use smoke_signals::config::Config;
use smoke_signals::diagnostics;
use smoke_signals::frames;
use smoke_signals::output;
use smoke_signals::render;
use smoke_signals::replays;
use smoke_signals::replays::ReplaySet;
use smoke_signals::session;
use smoke_signals::session::GameData;

/// Smoke screen analysis for tournament replays.
#[derive(Parser)]
#[command(name = "smoke_signals")]
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
    /// Track every smoke in the game folder and write the smoke table,
    /// frames and clips.
    Analyze {
        /// Skip the per-smoke activation and capture frames (and the Tier 1
        /// state they record).
        #[arg(long)]
        no_frames: bool,
        /// Skip the per-smoke clips.
        #[arg(long)]
        no_clips: bool,
        /// Only the smoke with this id gets frames and a clip.
        #[arg(long)]
        only: Option<u32>,
    },
    /// List every smoke consumable variant in the game data.
    Variants,
}

fn main() -> Result<(), Report> {
    tracing_subscriber::fmt().with_target(false).with_writer(std::io::stderr).init();
    let args = Args::parse();
    let config = Config::load(&args.config)?;

    let out_dir = config.paths.output.join(jiff::Zoned::now().strftime("%Y%m%d-%H%M%S").to_string());
    std::fs::create_dir_all(&out_dir).attach_with(|| format!("creating {}", out_dir.display()))?;

    let (replays, game) = load_inputs(&config)?;
    match args.command {
        Command::Frame { at } => {
            let frame = render::render_frame_at(&config, &game, &replays, at, &out_dir)?;
            write_frame_log(&out_dir, &replays, &game, &frame)?;
            println!("{}", frame.path.display());
        }
        Command::Analyze { no_frames, no_clips, only } => {
            let mut analysis = analysis::analyze_game(&config, &game, &replays)?;
            let selected: Vec<usize> = analysis
                .smokes
                .iter()
                .enumerate()
                .filter(|(_, s)| only.is_none_or(|id| s.smoke_id == id))
                .map(|(i, _)| i)
                .collect();
            let frames_written = if no_frames {
                0
            } else {
                frames::render_smoke_frames(
                    &config,
                    &game,
                    &replays,
                    &analysis.game,
                    &mut analysis.smokes,
                    &selected,
                    &out_dir.join("frames"),
                )?
            };
            let clips_written = if no_clips {
                0
            } else {
                clips::render_clips(
                    &config,
                    &game,
                    &replays,
                    &analysis.game,
                    &mut analysis.smokes,
                    &selected,
                    &out_dir.join("clips"),
                )?
            };
            output::write_smokes_csv(&out_dir.join("smokes.csv"), &analysis.smokes)?;
            output::write_json(
                &out_dir.join("smokes.json"),
                &SmokesDocument { game: &analysis.game, smokes: &analysis.smokes },
            )?;
            output::write_json(&out_dir.join("game.json"), &analysis.game)?;
            let activations = diagnostics::scan_activations(&game, &replays, &analysis.game, &analysis.clock_map);
            diagnostics::write_activations_csv(&out_dir.join("activations.csv"), &activations)?;
            let tracks = diagnostics::summarize_tracks(&analysis.timeline, &analysis.game, &analysis.flag_history);
            if let Some(results) = &analysis.battle_results {
                std::fs::write(out_dir.join("battle_results.json"), results)
                    .attach_with(|| "writing battle_results.json")?;
                match diagnostics::decode_public_results(&game.build_dir.join("constants.json"), results) {
                    Ok(decoded) => {
                        diagnostics::write_public_results_csv(&out_dir.join("battle_results_players.csv"), &decoded)?;
                        for r in &decoded {
                            if let (Some(p), Some(d)) = (analysis.game.player_by_name(&r.name), r.damage) {
                                analysis.damage_stats.damage_by_attacker_authoritative.insert(p.entity_id, d as f32);
                            }
                        }
                    }
                    Err(e) => tracing::warn!("battle results not decoded: {e}"),
                }
            }
            diagnostics::write_tracks_csv(&out_dir.join("tracks.csv"), &tracks)?;
            let name_of = |e: u32| analysis.game.player(e).map(|p| p.player.clone());
            output::write_damage_events_csv(&out_dir.join("damage_events.csv"), &analysis.damage_events, &name_of)?;
            output::write_json(&out_dir.join("damage_spike.json"), &analysis.damage_stats)?;
            let log = output::run_log(
                &analysis.game,
                &analysis.smokes,
                &analysis.damage_stats,
                frames_written,
                clips_written,
            );
            std::fs::write(out_dir.join("run_log.md"), &log).attach_with(|| "writing run_log.md")?;
            print!("{}", output::summary_table(&analysis.smokes));
            println!("{}", out_dir.display());
        }
        Command::Variants => print_smoke_variants(&game),
    }
    Ok(())
}

#[derive(serde::Serialize)]
struct SmokesDocument<'a> {
    game: &'a smoke_signals::records::GameRecord,
    smokes: &'a [smoke_signals::records::SmokeRecord],
}

fn load_inputs(config: &Config) -> Result<(ReplaySet, GameData), Report> {
    let replays = replays::load_game_folder(&config.paths.replays, &config.run.team_prefix, config.run.merge)?;
    info!(primary = %replays.primary_path.display(), player = %replays.primary.meta.playerName, "Primary replay");
    for (path, file) in replays.merge_paths.iter().zip(&replays.merges) {
        info!(merge = %path.display(), player = %file.meta.playerName, "Merge replay");
    }
    let game = session::load_game_data(&config.paths.game_data, &replays.primary)?;
    info!(build_dir = %game.build_dir.display(), "Game data");
    Ok((replays, game))
}

/// Every `smokeGenerator` ability variant, with the fields the smoke type
/// and base stats come from.
fn print_smoke_variants(game: &GameData) {
    let mut rows: Vec<String> = Vec::new();
    for param in game.loaded.game_params.params() {
        let Some(ability) = param.ability() else { continue };
        for (variant, category) in ability.categories() {
            if category.consumable_type_raw() != "smokeGenerator" {
                continue;
            }
            let fields = category.effect_fields();
            let field = |k: &str| fields.get(k).map(|v| format!("{v}")).unwrap_or_else(|| "-".to_string());
            rows.push(format!(
                "{:<36} {:<28} {:<9} work={:<5} life={:<5} radius={:<5} speed={:<5} charges={:<3} icon={}",
                param.name(),
                variant,
                analysis::classify(variant, category.icon_id()).as_str(),
                category.work_time(),
                field("lifeTime"),
                field("radius"),
                field("speedLimit"),
                category.num_consumables(),
                category.icon_id()
            ));
        }
    }
    rows.sort();
    for row in rows {
        println!("{row}");
    }
}

/// Record the inputs and the clock placement next to the frame.
fn write_frame_log(
    out_dir: &Path,
    replays: &ReplaySet,
    game: &GameData,
    frame: &render::RenderedFrame,
) -> Result<(), Report> {
    use std::fmt::Write as _;

    let mut log = String::new();
    let _ = writeln!(log, "# Smoke Signals run log\n");
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
    let path = out_dir.join("run_log.md");
    std::fs::write(&path, log).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}
