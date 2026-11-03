use clap::Parser;
use indicatif::ProgressBar;
use indicatif::ProgressStyle;
use rootcause::prelude::*;
use std::cell::Cell;
use std::path::PathBuf;
use tracing::info;
use tracing::warn;
use wowsunpack::data::Version;
use wowsunpack::game_params::types::GameParamProvider;

use wows_battle_world::merged::MergedReplays;
use wows_replays::ReplayFile;
use wows_replays::game_constants::GameConstants;

use wows_minimap_renderer::EncoderKind;
use wows_minimap_renderer::VideoCodec;
use wows_minimap_renderer::assets::load_building_icons;
use wows_minimap_renderer::assets::load_consumable_icons;
use wows_minimap_renderer::assets::load_death_cause_icons;
use wows_minimap_renderer::assets::load_flag_icons;
use wows_minimap_renderer::assets::load_game_fonts;
use wows_minimap_renderer::assets::load_map_image;
use wows_minimap_renderer::assets::load_map_info;
use wows_minimap_renderer::assets::load_packed_image;
use wows_minimap_renderer::assets::load_plane_icons;
use wows_minimap_renderer::assets::load_powerup_icons;
use wows_minimap_renderer::assets::load_ribbon_icons;
use wows_minimap_renderer::assets::load_ship_icons;
use wows_minimap_renderer::config::RendererConfig;
use wows_minimap_renderer::drawing::ImageTarget;
use wows_minimap_renderer::encoder::Mode as EncoderMode;
use wows_minimap_renderer::game_data_loader;
use wows_minimap_renderer::game_data_loader::LoadedGameData;
use wows_minimap_renderer::renderer::MinimapRenderer;
use wows_minimap_renderer::video::CodecChoice;
use wows_minimap_renderer::video::DumpMode;
use wows_minimap_renderer::video::RenderStage;
use wows_minimap_renderer::video::VideoEncoder;

#[derive(Clone, Copy, clap::ValueEnum)]
enum CodecArg {
    H264,
    H265,
    Av1,
}

impl From<CodecArg> for VideoCodec {
    fn from(c: CodecArg) -> Self {
        match c {
            CodecArg::H264 => VideoCodec::H264,
            CodecArg::H265 => VideoCodec::H265,
            CodecArg::Av1 => VideoCodec::Av1,
        }
    }
}

/// Generates a minimap timelapse video from a WoWS replay
#[derive(Parser)]
#[command(name = "Minimap Renderer")]
struct Args {
    /// Path to the World of Warships game directory
    #[arg(short = 'g', long = "game", conflicts_with = "extracted_dir", required_unless_present_any = ["generate_config", "check_encoder", "extracted_dir"])]
    game_dir: Option<PathBuf>,

    /// Path to pre-extracted renderer data directory (alternative to --game)
    #[arg(long, conflicts_with = "game_dir", required_unless_present_any = ["generate_config", "check_encoder", "game_dir"])]
    extracted_dir: Option<PathBuf>,

    /// Output MP4 file path, for dumping may not be specified to dump to stdout instead
    #[arg(short, long, required_unless_present_any = ["generate_config", "check_encoder", "dump_frame", "dump_frames"])]
    output: Option<PathBuf>,

    /// Dump a single frame as PNG instead of rendering video (specify frame number, 'mid' for midpoint or 'last' for last frame)
    #[arg(long, conflicts_with = "dump_frames")]
    dump_frame: Option<String>,

    /// Dump all frames as PNGs instead of rendering video
    #[arg(long, conflicts_with = "dump_frame")]
    dump_frames: bool,

    /// Show player names above ship icons (off by default; matches the desktop default)
    #[arg(long, conflicts_with = "no_player_names")]
    show_player_names: bool,

    /// Hide player names above ship icons
    #[arg(long)]
    no_player_names: bool,

    /// Hide ship names above ship icons
    #[arg(long)]
    no_ship_names: bool,

    /// Hide capture point zones
    #[arg(long)]
    no_capture_points: bool,

    /// Hide building markers
    #[arg(long)]
    no_buildings: bool,

    /// Hide camera/look direction indicators
    #[arg(long, alias = "no-turret-direction")]
    no_camera_direction: bool,

    /// Hide selected armament/ammo type below ship icons
    #[arg(long)]
    no_armament: bool,

    /// Hide the kill feed
    #[arg(long)]
    no_kill_feed: bool,

    /// Hide chat messages
    #[arg(long)]
    no_chat: bool,

    /// Show position trail heatmap (rainbow coloring)
    #[arg(long)]
    show_trails: bool,

    /// Hide trails for dead ships
    #[arg(long)]
    no_dead_trails: bool,

    /// Show speed-based trails (blue=slow, red=fast)
    #[arg(long)]
    show_speed_trails: bool,

    /// Show ship config range circles (detection, battery, etc.)
    #[arg(long)]
    show_ship_config: bool,

    /// Force the team-roster side panels on (mutually exclusive with the stats panel).
    /// Auto-enabled when one or more --merge replays are passed.
    #[arg(long, conflicts_with = "no_team_rosters")]
    team_rosters: bool,

    /// Force the team-roster side panels off.
    #[arg(long)]
    no_team_rosters: bool,

    /// Force the self-perspective stats panel on (mutually exclusive with team rosters).
    #[arg(long, conflicts_with = "no_stats_panel")]
    stats_panel: bool,

    /// Force the self-perspective stats panel off.
    #[arg(long)]
    no_stats_panel: bool,

    /// Include the pre-battle phase (spawn and countdown) at the start of the
    /// video. By default rendering begins at battle start.
    #[arg(long)]
    include_pre_battle: bool,

    /// Path to TOML config file
    #[arg(long)]
    config: Option<PathBuf>,

    /// Print default TOML config to stdout and exit
    #[arg(long)]
    generate_config: bool,

    /// Check encoder availability (GPU/CPU) and exit
    #[arg(long)]
    check_encoder: bool,

    /// Force CPU encoder (no GPU). Combine with --codec to pick the CPU encoder.
    #[arg(long)]
    cpu: bool,

    /// Video codec for output. Defaults to the best codec supported by the
    /// active backend (GPU H.265 if available, otherwise CPU AV1).
    #[arg(long, value_enum)]
    codec: Option<CodecArg>,

    /// Target average bitrate in kilobits per second. Applies to H.264/H.265
    /// (VBR target); for AV1 the encoder picks a quantizer to meet the rate.
    /// Mutually exclusive with --max-size-mib.
    #[arg(long, conflicts_with = "max_size_mib")]
    bitrate_kbps: Option<u32>,

    /// Target a maximum encoded file size in MiB. The bitrate is derived from
    /// the match duration with a small safety margin. Mutually exclusive with
    /// --bitrate-kbps.
    #[arg(long, conflicts_with = "bitrate_kbps")]
    max_size_mib: Option<u32>,

    /// Disable progress bar and use log output instead
    #[arg(long)]
    no_progress: bool,

    /// Path to a constants JSON file (from wows-constants repo) to override
    /// consumable IDs, battle stages, etc.
    #[arg(short = 'c', long = "constants")]
    constants: Option<PathBuf>,

    /// Recreate game_params.rkyv from VFS GameParams.data if deserialization fails
    /// (useful when the internal format changes between versions)
    #[arg(long)]
    recreate_game_params: bool,

    /// Directory for a locally rebuilt game params cache. Defaults to a
    /// per-build directory in the toolkit's data dir, shared with the GUI.
    #[arg(long)]
    game_params_cache: Option<PathBuf>,

    /// The replay file to process (primary perspective)
    #[arg(required_unless_present_any = ["generate_config", "check_encoder"])]
    replay: Option<PathBuf>,

    /// Additional replay files from other players in the same match. Their
    /// state is merged into the primary perspective to remove fog of war.
    /// Arena IDs must match across all replays.
    #[arg(long = "merge")]
    merge: Vec<PathBuf>,
}

fn main() -> Result<(), Report> {
    let args = Args::parse();

    tracing_subscriber::fmt().with_target(false).with_writer(std::io::stderr).init();

    // Handle --generate-config before anything else
    if args.generate_config {
        print!("{}", RendererConfig::generate_default_toml());
        return Ok(());
    }

    // Handle --check-encoder
    if args.check_encoder {
        let status = wows_minimap_renderer::check_encoder();
        print!("{status}");
        return Ok(());
    }

    let output = match &args.output {
        None => {
            // Checking here so that video rendering can safely unwrap() later
            if !args.dump_frames && args.dump_frame.is_none() {
                bail!("output is required");
            }
            None
        }
        Some(path) => path.to_str(),
    };
    let replay_path = args.replay.as_ref().expect("replay is required");

    let dump_mode = match args.dump_frame.as_deref() {
        Some("mid") => Some(DumpMode::Midpoint),
        Some("last") => Some(DumpMode::Last),
        Some(n) => Some(DumpMode::Frame(n.parse::<usize>().expect("invalid frame number"))),
        None => None,
    };

    info!("Parsing replay");
    let replay_file = ReplayFile::from_file(replay_path)?;
    let replay_version = Version::from_client_exe(&replay_file.meta.clientVersionFromExe);

    // Optional merge replays from other players in the same match. Loaded eagerly
    // so a bad file fails before we touch game data. Arena IDs are validated in
    // the packet loop below, after enough packets have been processed to populate
    // each controller's arena_id from the OnArenaStateReceived RPC.
    let merge_replays: Vec<ReplayFile> = args
        .merge
        .iter()
        .map(|p| ReplayFile::from_file(p).attach_with(|| format!("loading merge replay: {}", p.display())))
        .collect::<Result<_, _>>()?;
    for r in &merge_replays {
        if r.meta.clientVersionFromExe != replay_file.meta.clientVersionFromExe {
            bail!(
                "Merge replay version mismatch (primary={}, merge={}, player={})",
                replay_file.meta.clientVersionFromExe,
                r.meta.clientVersionFromExe,
                r.meta.playerName
            );
        }
        info!(player = %r.meta.playerName, "Loaded merge replay");
    }

    // Load game data from either a full game install or pre-extracted directory
    let resolved_extracted: Option<PathBuf> = args
        .extracted_dir
        .as_ref()
        .map(|extracted| game_data_loader::resolve_extracted_dir(extracted, &replay_version))
        .transpose()?;

    let LoadedGameData { vfs: vfs_owned, specs, game_params, controller_game_params } = if let Some(ref resolved) =
        resolved_extracted
    {
        game_data_loader::load_from_extracted(resolved, args.recreate_game_params, args.game_params_cache.as_deref())?
    } else {
        let game_dir = args.game_dir.as_ref().expect("game directory is required");
        game_data_loader::load_from_game_dir(game_dir, &replay_version)?
    };
    let vfs = &vfs_owned;

    info!("Loading fonts and icons");
    let game_fonts = load_game_fonts(vfs);
    let version = Some(&replay_version);
    let ship_icons = load_ship_icons(vfs, version);
    let plane_icons = load_plane_icons(vfs, version);
    let building_icons = load_building_icons(vfs, version);
    let consumable_icons = load_consumable_icons(vfs, version);
    let ribbon_icons = load_ribbon_icons(vfs, wowsunpack::game_assets::GuiAssetDir::Ribbons, version);
    let subribbon_icons = load_ribbon_icons(vfs, wowsunpack::game_assets::GuiAssetDir::SubRibbons, version);
    let death_cause_icons = load_death_cause_icons(vfs, wows_minimap_renderer::assets::ICON_SIZE, version);
    let powerup_icons = load_powerup_icons(vfs, wows_minimap_renderer::assets::ICON_SIZE, version);
    let flag_icons = load_flag_icons(vfs, version);

    // Load game constants from game data (falls back to hardcoded defaults per-field)
    let mut game_constants = GameConstants::from_vfs(vfs);

    // Auto-load constants.json from extracted dir if present (and no explicit --constants)
    if args.constants.is_none()
        && let Some(ref resolved) = resolved_extracted
    {
        match game_data_loader::merge_dump_constants(&mut game_constants, resolved, replay_version) {
            Ok(Some(path)) => info!("Merged constants from dump: {}", path.display()),
            Ok(None) => {}
            Err(e) => warn!("Ignoring dump constants: {e}"),
        }
    }

    // Explicit --constants flag takes priority (overrides auto-loaded)
    if let Some(ref constants_path) = args.constants {
        let data = std::fs::read_to_string(constants_path)
            .unwrap_or_else(|e| panic!("Failed to read constants file {}: {e}", constants_path.display()));
        let json: serde_json::Value =
            serde_json::from_str(&data).unwrap_or_else(|e| panic!("Failed to parse constants JSON: {e}"));
        game_constants.merge_replay_constants(&json, replay_version);
        info!("Merged replay constants from {}", constants_path.display());
    }

    if let Some(mode_name) = game_constants.game_mode_name(replay_file.meta.gameMode as i32) {
        info!(mode = %mode_name, id = replay_file.meta.gameMode, "Game mode");
    }

    // Load map image and metadata from game files
    let map_name = &replay_file.meta.mapName;
    let map_image = load_map_image(map_name, vfs);
    let map_info = load_map_info(map_name, vfs);

    let game_duration = replay_file.meta.duration as f32;

    // Load config: --config path > exe-adjacent minimap_renderer.toml > defaults
    let mut config = if let Some(config_path) = &args.config {
        RendererConfig::load(config_path)?
    } else {
        // Try exe-adjacent config file
        let exe_config = std::env::current_exe().ok().and_then(|p| p.parent().map(|d| d.join("minimap_renderer.toml")));
        match exe_config {
            Some(path) if path.exists() => {
                info!(path = ?path, "Loading config");
                RendererConfig::load(&path)?
            }
            _ => RendererConfig::default(),
        }
    };
    // Merged replays automatically swap to the team-roster layout for this
    // run (mirrors the desktop renderer). The user can still override either
    // way with the explicit CLI flags below.
    let merge_mode = !args.merge.is_empty();
    config.apply_cli_overrides(&wows_minimap_renderer::config::CliOverrides {
        show_player_names: args.show_player_names,
        no_player_names: args.no_player_names,
        no_ship_names: args.no_ship_names,
        no_capture_points: args.no_capture_points,
        no_buildings: args.no_buildings,
        no_camera_direction: args.no_camera_direction,
        no_armament: args.no_armament,
        no_kill_feed: args.no_kill_feed,
        no_chat: args.no_chat,
        show_trails: args.show_trails,
        no_dead_trails: args.no_dead_trails,
        show_speed_trails: args.show_speed_trails,
        show_ship_config: args.show_ship_config,
        team_rosters: args.team_rosters || (merge_mode && !args.no_team_rosters),
        no_team_rosters: args.no_team_rosters,
        stats_panel: args.stats_panel,
        no_stats_panel: args.no_stats_panel,
        include_pre_battle: args.include_pre_battle,
    });
    let include_pre_battle = config.include_pre_battle;
    let mut options = config.into_render_options();
    options.ship_config_visibility = wows_minimap_renderer::ShipConfigVisibility::SelfOnly;

    let mut target = ImageTarget::with_side_panel(
        map_image,
        game_fonts.clone(),
        ship_icons,
        plane_icons,
        building_icons,
        consumable_icons,
        ribbon_icons,
        subribbon_icons,
        death_cause_icons,
        powerup_icons,
        wows_minimap_renderer::drawing::SidePanelLayout::from_options(&options),
    );

    // Load self player's ship silhouette for the stats panel
    let self_silhouette = replay_file.meta.vehicles.iter().find(|v| v.relation == 0).and_then(|v| {
        let param = GameParamProvider::game_param_by_id(&game_params, v.shipId)?;
        let path = format!("gui/ships_silhouettes/{}.png", param.index());
        let img = load_packed_image(&path, vfs)?;
        Some(img.into_rgba8())
    });

    // Pre-scan vehicle facts + damage events so roster HP, consumable
    // inventories, and damage columns render from frame zero (the desktop
    // renderer does the same in playback.rs). Without this, team-roster mode
    // ships up with empty inventories and damage stuck at 0 until the live
    // controller catches up.
    let mut primary_with_alts: Vec<&ReplayFile> = vec![&replay_file];
    primary_with_alts.extend(merge_replays.iter());
    let vehicle_facts = wows_replays::analyzer::battle_controller::merged::gather_replay_facts(
        &game_constants,
        replay_version,
        &specs,
        &primary_with_alts,
    );
    let damage_events = wows_battle_world::merged::gather_damage_events(
        &controller_game_params,
        &game_constants,
        replay_version,
        &specs,
        &primary_with_alts,
    );

    let mut renderer = MinimapRenderer::new(map_info.clone(), &game_params, replay_version, options);
    renderer.set_fonts(game_fonts);
    renderer.set_flag_icons(flag_icons);
    renderer.set_merged_perspectives(!merge_replays.is_empty());
    renderer.set_vehicle_facts(vehicle_facts.clone());
    renderer.set_damage_events(damage_events);
    let salvo_flight_times = wows_battle_world::scan::scan_salvo_flight_times(
        &replay_file.meta,
        &controller_game_params,
        &game_constants,
        replay_version,
        &replay_file,
    );
    renderer.set_salvo_flight_times(std::sync::Arc::new(salvo_flight_times));
    if let Some(sil) = self_silhouette {
        renderer.set_self_silhouette(sil);
    }

    let (cw, ch) = target.canvas_size();
    let mut encoder = VideoEncoder::new(output, dump_mode, args.dump_frames, game_duration, cw, ch);
    let mode = if args.cpu { EncoderMode::ForceCpu } else { EncoderMode::Auto };
    encoder.set_mode(mode);
    let codec_choice = match args.codec {
        None => CodecChoice::Auto,
        Some(c) => {
            let codec: VideoCodec = c.into();
            let kind = if args.cpu { EncoderKind::Cpu } else { EncoderKind::Gpu };
            let status = wows_minimap_renderer::check_encoder();
            if args.cpu && !status.supports(EncoderKind::Cpu, codec) {
                bail!(
                    "codec {codec} is not supported by the CPU backend on this build; available CPU codecs: {}",
                    available_codecs_for(EncoderKind::Cpu, &status)
                );
            }
            if !args.cpu && !status.supports(kind, codec) {
                bail!(
                    "codec {codec} is not supported by the GPU backend on this system; pass --cpu to use software encoding, or pick a supported codec: {}",
                    available_codecs_for(kind, &status)
                );
            }
            CodecChoice::Explicit(codec)
        }
    };
    encoder.set_codec(codec_choice);
    if let Some(kbps) = args.bitrate_kbps {
        let bps = kbps.saturating_mul(1000);
        encoder.set_encoder_config(wows_minimap_renderer::EncoderConfig {
            target_bitrate_bps: Some(bps),
            max_bitrate_bps: Some(bps.saturating_mul(2)),
            av1_quantizer: None,
        });
    } else if let Some(mib) = args.max_size_mib {
        encoder.target_max_file_size((mib as u64) * 1024 * 1024);
    }
    if args.dump_frame.is_none() {
        encoder.init()?;
    }

    let use_progress_bar = !args.no_progress;
    let progress_bar = if use_progress_bar {
        let pb = ProgressBar::new(0);
        pb.set_style(
            ProgressStyle::default_bar()
                .template("{msg} [{bar:40}] {pos}/{len} ({eta})")
                .expect("valid progress template")
                .progress_chars("=> "),
        );
        pb.set_message("Encoding");
        let pb_clone = pb.clone();
        let current_stage = Cell::new(RenderStage::Encoding);
        encoder.set_progress_callback(move |p| {
            if p.stage != current_stage.get() {
                current_stage.set(p.stage);
                pb_clone.set_position(0);
                pb_clone.set_message(match p.stage {
                    RenderStage::Encoding => "Encoding",
                    RenderStage::Muxing => "Muxing",
                });
            }
            pb_clone.set_length(p.total);
            pb_clone.set_position(p.current);
        });
        Some(pb)
    } else {
        let last_reported = Cell::new(RenderStage::Encoding);
        encoder.set_progress_callback(move |p| {
            if p.stage != last_reported.get() {
                last_reported.set(p.stage);
                info!(stage = ?p.stage, total = p.total, "Starting stage");
            }
            if p.current % 100 == 0 || p.current == p.total {
                info!(stage = ?p.stage, frame = p.current, total = p.total, "Progress");
            }
        });
        None
    };

    let mut session = MergedReplays::new(
        &specs,
        &controller_game_params,
        &game_constants,
        replay_version,
        &replay_file,
        &merge_replays,
    )
    .map_err(|e| report!("{e}"))?;
    wows_replay_insights::build::seed_consumable_inventories_from_facts(
        session.world_mut(),
        &vehicle_facts,
        &controller_game_params,
        replay_version,
    );

    if session.replays().len() > 1 {
        for (i, r) in session.replays().iter().enumerate() {
            match session.self_teams()[i] {
                Some(team) => info!(replay = i, player = %r.meta.playerName, team = %team, "Self team"),
                None => {
                    warn!(replay = i, player = %r.meta.playerName, "Failed to detect self team; merge filtering disabled for this perspective")
                }
            }
        }
    }

    // By default the video starts at battle start, skipping the pre-battle
    // spawn and countdown. --include-pre-battle renders from the replay start.
    let render_start = if include_pre_battle {
        wows_replays::types::GameClock(0.0)
    } else {
        session.battle_start_clock().unwrap_or(wows_replays::types::GameClock(0.0))
    };
    if render_start.seconds() > 0.0 {
        info!(start = %render_start, "Skipping pre-battle phase");
    }
    encoder.set_render_start(render_start);

    if session.total_duration().seconds() > 0.0 {
        encoder.set_battle_duration(session.total_duration());
    }

    let mut prev_render_clock = wows_replays::types::GameClock(0.0);
    let mut arena_logged = false;
    while let Some(safe_clock) = session.step().map_err(|e| report!("{e}"))? {
        if !arena_logged && let Some(arena) = session.arena_id() {
            info!(arena_id = %arena, replays = session.replays().len(), "Arena IDs match");
            arena_logged = true;
        }
        if safe_clock.0 > prev_render_clock.0 {
            let view = session.world_mut().view();
            renderer.populate_players(&view);
            renderer.update_squadron_info(&view);
            renderer.update_ship_abilities(&view);
            encoder.advance_clock(prev_render_clock, &view, &mut renderer, &mut target);
            prev_render_clock = safe_clock;
        }
    }

    let final_clock = session.total_duration();
    if final_clock.0 > prev_render_clock.0 {
        let view = session.world_mut().view();
        renderer.populate_players(&view);
        renderer.update_squadron_info(&view);
        renderer.update_ship_abilities(&view);
        encoder.advance_clock(final_clock, &view, &mut renderer, &mut target);
    }

    session.finish();
    {
        let view = session.world_mut().view();
        encoder.finish(&view, &mut renderer, &mut target)?;
    }

    if let Some(pb) = progress_bar {
        pb.finish_and_clear();
    }

    info!("Done");
    Ok(())
}

fn available_codecs_for(kind: EncoderKind, status: &wows_minimap_renderer::encoder::EncoderStatus) -> String {
    let mut names: Vec<&str> =
        VideoCodec::ALL.into_iter().filter(|c| status.supports(kind, *c)).map(VideoCodec::as_str).collect();
    if names.is_empty() {
        names.push("(none)");
    }
    names.join(", ")
}
