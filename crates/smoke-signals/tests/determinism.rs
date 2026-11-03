//! The analysis of Grand Final G1 must give byte-identical smokes.csv and
//! smokes.json on two runs over the same inputs, apart from the run
//! timestamp, which the test pins to one value on both.
//!
//! The replays and game data are local inputs (gitignored). The test fails
//! when `config.toml` or the folders it names are missing, unless
//! `SMOKE_SIGNALS_SKIP_GOLDEN=1` is set, in which case it prints a notice and
//! passes.

use std::path::Path;
use std::path::PathBuf;

use smoke_signals::analysis;
use smoke_signals::analysis::Analysis;
use smoke_signals::config::Config;
use smoke_signals::output;
use smoke_signals::replays;
use smoke_signals::session;

const PINNED_GENERATED_AT: &str = "2000-01-01T00:00:00+00:00";

fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..").join("..")
}

fn config_path() -> PathBuf {
    std::env::var_os("SMOKE_SIGNALS_CONFIG").map(PathBuf::from).unwrap_or_else(|| repo_root().join("config.toml"))
}

fn skip(reason: &str) {
    if std::env::var_os("SMOKE_SIGNALS_SKIP_GOLDEN").is_none_or(|v| v != "1") {
        panic!("reference inputs missing ({reason}); set SMOKE_SIGNALS_SKIP_GOLDEN=1 to skip this test");
    }
    eprintln!("skipped: {reason}");
}

fn pin_timestamp(analysis: &mut Analysis) {
    analysis.game.generated_at = PINNED_GENERATED_AT.to_string();
    for smoke in &mut analysis.smokes {
        smoke.generated_at = PINNED_GENERATED_AT.to_string();
    }
}

fn write_outputs(analysis: &Analysis, dir: &Path) -> (Vec<u8>, Vec<u8>) {
    std::fs::create_dir_all(dir).expect("output dir");
    let csv = dir.join("smokes.csv");
    let json = dir.join("smokes.json");
    output::write_smokes_csv(&csv, &analysis.smokes).expect("smokes.csv");
    output::write_json(&json, &output::SmokesDocument { game: &analysis.game, smokes: &analysis.smokes })
        .expect("smokes.json");
    (std::fs::read(&csv).expect("read csv"), std::fs::read(&json).expect("read json"))
}

fn first_difference(name: &str, a: &[u8], b: &[u8]) -> Option<String> {
    if a == b {
        return None;
    }
    let (a, b) = (String::from_utf8_lossy(a), String::from_utf8_lossy(b));
    let line = a.lines().zip(b.lines()).enumerate().find(|(_, (x, y))| x != y);
    Some(match line {
        Some((i, (x, y))) => format!("{name} differs at line {}:\n  run 1: {x}\n  run 2: {y}", i + 1),
        None => format!("{name} differs in length only ({} vs {} bytes)", a.len(), b.len()),
    })
}

#[test]
fn grand_final_g1_analysis_is_repeatable() {
    let config_path = config_path();
    if !config_path.exists() {
        return skip(&format!("{} not found", config_path.display()));
    }
    let config = Config::load(&config_path).expect("config");
    if !config.paths.replays.is_dir() || !config.paths.game_data.is_dir() {
        return skip("replays or game data folder missing");
    }
    let replays =
        replays::load_game_folder(
            &config.paths.replays,
            &config.run.team_prefix,
            config.run.merge,
            config.run.primary_replay.as_deref(),
        )
        .expect("replays");
    let game = session::load_game_data(&config.paths.game_data, &replays.primary).expect("game data");

    let scratch = std::env::temp_dir().join(format!("smoke-signals-determinism-{}", std::process::id()));
    let mut outputs = Vec::new();
    for run in 1..=2 {
        let mut analysis = analysis::analyze_game(&config, &game, &replays).expect("analysis");
        pin_timestamp(&mut analysis);
        outputs.push(write_outputs(&analysis, &scratch.join(format!("run{run}"))));
    }
    let _ = std::fs::remove_dir_all(&scratch);

    let failures: Vec<String> = [
        first_difference("smokes.csv", &outputs[0].0, &outputs[1].0),
        first_difference("smokes.json", &outputs[0].1, &outputs[1].1),
    ]
    .into_iter()
    .flatten()
    .collect();
    assert!(failures.is_empty(), "{}", failures.join("\n"));
}
