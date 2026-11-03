use std::path::Path;
use std::path::PathBuf;

use clap::Parser;
use clap::Subcommand;
use rootcause::prelude::*;
use tracing::info;
use wowsunpack::game_params::types::GameParamProvider;

use smoke_signals::analysis;
use smoke_signals::batch;
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
    /// Write the minimap image and map info of the named maps, for the site.
    Maps {
        /// Map names, comma separated, with or without the `spaces/` prefix.
        #[arg(long)]
        names: String,
    },
    /// Analyse every played game in the replay inventory, one run per team
    /// in scope with that team's replay as the primary, and write a
    /// combined smoke table.
    Batch {
        /// The inventory CSV.
        #[arg(long, default_value = "smoke/inventory.csv")]
        inventory: PathBuf,
        /// Only these maps, comma separated: the first played game of each.
        #[arg(long)]
        maps: Option<String>,
        /// Only these match ids, comma separated.
        #[arg(long)]
        matches: Option<String>,
        /// Teams in scope, comma separated.
        #[arg(long, default_value = "H-SR,RESIN,PN")]
        teams: String,
        /// Games analysed at the same time.
        #[arg(long, default_value_t = 1)]
        jobs: usize,
        /// Skip the frames (and the Tier 1 state and cap proximity they record).
        #[arg(long)]
        no_frames: bool,
        /// Smoke ids that get a clip, comma separated.
        #[arg(long)]
        clips: Option<String>,
        /// Clip speed for this run, overriding render.clip_speed.
        #[arg(long)]
        clip_speed: Option<f32>,
        /// Clip bitrate in kilobits per second, overriding render.clip_bitrate_kbps.
        #[arg(long)]
        clip_bitrate_kbps: Option<u32>,
    },
}

static WARNINGS: batch::WarningSink = batch::WarningSink::new();

fn main() -> Result<(), Report> {
    use tracing_subscriber::layer::SubscriberExt as _;
    use tracing_subscriber::util::SubscriberInitExt as _;
    tracing_subscriber::registry()
        .with(tracing_subscriber::filter::LevelFilter::INFO)
        .with(tracing_subscriber::fmt::layer().with_target(false).with_writer(std::io::stderr))
        .with(&WARNINGS)
        .init();
    let args = Args::parse();
    let config = Config::load(&args.config)?;

    let out_dir = config.paths.output.join(jiff::Zoned::now().strftime("%Y%m%d-%H%M%S").to_string());
    std::fs::create_dir_all(&out_dir).attach_with(|| format!("creating {}", out_dir.display()))?;

    match args.command {
        Command::Frame { at } => {
            let (replays, game) = load_inputs(&config)?;
            let frame = render::render_frame_at(&config, &game, &replays, at, &out_dir)?;
            write_frame_log(&out_dir, &replays, &game, &frame)?;
            println!("{}", frame.path.display());
        }
        Command::Analyze { no_frames, no_clips, only } => {
            let (replays, game) = load_inputs(&config)?;
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
                &output::SmokesDocument { game: &analysis.game, smokes: &analysis.smokes },
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
        Command::Variants => {
            let (_, game) = load_inputs(&config)?;
            print_smoke_variants(&game);
        }
        Command::Maps { names } => {
            let (_, game) = load_inputs(&config)?;
            let dir = out_dir.join("maps");
            std::fs::create_dir_all(&dir).attach_with(|| format!("creating {}", dir.display()))?;
            let mut info = Vec::new();
            for name in names.split(',').map(str::trim).filter(|n| !n.is_empty()) {
                let bare = name.strip_prefix("spaces/").unwrap_or(name);
                let full = format!("spaces/{bare}");
                let image = wows_minimap_renderer::assets::load_map_image(&full, &game.loaded.vfs);
                let map_info = wows_minimap_renderer::assets::load_map_info(&full, &game.loaded.vfs);
                match (image, map_info) {
                    (Some(image), Some(map_info)) => {
                        let file = frames::save_png_and_webp(&image, &dir, bare)?;
                        info.push(serde_json::json!({
                            "map": bare,
                            "title": smoke_signals::analysis::map_display_name(&game.loaded.game_params, &full),
                            "space_size": map_info.space_size,
                            "width": image.width(),
                            "height": image.height(),
                            "image": file,
                        }));
                    }
                    _ => tracing::warn!(map = bare, "Map image or map info missing"),
                }
            }
            output::write_json(&dir.join("maps.json"), &info)?;
            println!("{}", dir.display());
        }
        Command::Batch { inventory, maps, matches, teams, jobs, no_frames, clips, clip_speed, clip_bitrate_kbps } => {
            let mut config = config;
            if let Some(speed) = clip_speed {
                config.render.clip_speed = speed;
            }
            if clip_bitrate_kbps.is_some() {
                config.render.clip_bitrate_kbps = clip_bitrate_kbps;
            }
            let clip_ids: Vec<u32> = clips
                .as_deref()
                .unwrap_or("")
                .split(',')
                .filter_map(|s| s.trim().parse().ok())
                .collect();
            let teams: Vec<String> = teams.split(',').map(|t| t.trim().to_string()).filter(|t| !t.is_empty()).collect();
            let repo_root = config.paths.replays.parent().map(Path::to_path_buf).unwrap_or_else(|| PathBuf::from("."));
            let mut list = batch::jobs_from_inventory(&inventory, &repo_root, &teams)?;
            if let Some(maps) = maps {
                let wanted: Vec<String> = maps.split(',').map(|m| m.trim().to_string()).collect();
                let mut seen: std::collections::HashSet<String> = std::collections::HashSet::new();
                list.retain(|j| wanted.iter().any(|m| m.eq_ignore_ascii_case(&j.map)) && seen.insert(j.map.clone()));
            }
            if let Some(matches) = matches {
                let wanted: Vec<String> = matches.split(',').map(|m| m.trim().to_string()).collect();
                list.retain(|j| wanted.contains(&j.match_id));
            }
            info!(jobs = list.len(), "Batch jobs");
            let game = batch::load_game_data(&config, &list)?;
            let (smokes, reports) =
                batch::run_batch(&config, &game, &list, &out_dir, jobs, !no_frames, &clip_ids, &WARNINGS)?;
            print!("{}", output::summary_table(&smokes));
            println!("runs: {}, failed: {}", reports.len(), reports.iter().filter(|r| r.error.is_some()).count());
            println!("{}", out_dir.display());
        }
    }
    Ok(())
}

fn load_inputs(config: &Config) -> Result<(ReplaySet, GameData), Report> {
    let replays = replays::load_game_folder(
        &config.paths.replays,
        &config.run.team_prefix,
        config.run.merge,
        config.run.primary_replay.as_deref(),
    )?;
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
