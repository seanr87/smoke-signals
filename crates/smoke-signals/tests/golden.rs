//! Reference test for Grand Final G1: every H-SR smoke in
//! `smoke/tests/golden_gf_g1_hsr.csv` must be found with the same type and
//! variant, and its activation and capture battle clocks must be within the
//! row's tolerance.
//!
//! The replays and game data are local inputs (gitignored). The test fails
//! when `config.toml` or the folders it names are missing, unless
//! `SMOKE_SIGNALS_SKIP_GOLDEN=1` is set, in which case it prints a notice and
//! passes.

use std::collections::HashSet;
use std::path::PathBuf;

use smoke_signals::analysis;
use smoke_signals::clock::BattleClock;
use smoke_signals::config::Config;
use smoke_signals::records::SmokeRecord;
use smoke_signals::replays;
use smoke_signals::session;

struct Row {
    n: String,
    player: String,
    ship: String,
    smoke_type: String,
    variant: String,
    activate: BattleClock,
    capture: BattleClock,
    tolerance: u32,
}

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

fn load_rows() -> Vec<Row> {
    let path = repo_root().join("smoke").join("tests").join("golden_gf_g1_hsr.csv");
    let text = std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("reading {}: {e}", path.display()));
    let mut lines = text.lines().filter(|l| !l.trim().is_empty());
    let header: Vec<&str> = lines.next().expect("header row").split(',').collect();
    let col = |name: &str| header.iter().position(|h| *h == name).unwrap_or_else(|| panic!("column {name}"));
    let (n, player, ship, smoke_type, variant, activate, capture, tolerance) = (
        col("n"),
        col("player"),
        col("ship"),
        col("smoke_type"),
        col("variant"),
        col("clock_activate"),
        col("clock_capture"),
        col("tolerance_s"),
    );
    lines
        .map(|line| {
            let f: Vec<&str> = line.split(',').collect();
            Row {
                n: f[n].to_string(),
                player: f[player].to_string(),
                ship: f[ship].to_string(),
                smoke_type: f[smoke_type].to_string(),
                variant: f[variant].to_string(),
                activate: f[activate].parse().expect("clock_activate"),
                capture: f[capture].parse().expect("clock_capture"),
                tolerance: f[tolerance].parse().expect("tolerance_s"),
            }
        })
        .collect()
}

fn within(a: Option<BattleClock>, b: BattleClock, tolerance: u32) -> bool {
    a.is_some_and(|a| a.remaining_seconds().abs_diff(b.remaining_seconds()) <= tolerance)
}

#[test]
fn grand_final_g1_hsr_smokes_match_reference() {
    let config_path = config_path();
    if !config_path.exists() {
        return skip(&format!("{} not found", config_path.display()));
    }
    let config = Config::load(&config_path).expect("config");
    if !config.paths.replays.is_dir() || !config.paths.game_data.is_dir() {
        return skip("replays or game data folder missing");
    }
    let rows = load_rows();
    assert!(!rows.is_empty(), "reference CSV has no rows");

    let replays =
        replays::load_game_folder(&config.paths.replays, &config.run.team_prefix, config.run.merge).expect("replays");
    let game = session::load_game_data(&config.paths.game_data, &replays.primary).expect("game data");
    let analysis = analysis::analyze_game(&config, &game, &replays).expect("analysis");
    let ours: Vec<&SmokeRecord> =
        analysis.smokes.iter().filter(|s| s.team.as_deref() == Some(config.run.primary_team.as_str())).collect();

    let mut failures: Vec<String> = Vec::new();
    let mut used: HashSet<u32> = HashSet::new();
    for row in &rows {
        let found = ours.iter().find(|s| {
            !used.contains(&s.smoke_id)
                && s.player.as_deref() == Some(row.player.as_str())
                && s.ship.as_deref() == Some(row.ship.as_str())
                && within(s.t_activate.and_then(|m| m.clock), row.activate, row.tolerance)
        });
        let Some(s) = found else {
            failures
                .push(format!("row {}: no {} {} smoke activated near {}", row.n, row.player, row.ship, row.activate));
            continue;
        };
        used.insert(s.smoke_id);
        let smoke_type = s.smoke_type.map(|t| t.as_str()).unwrap_or("");
        if smoke_type != row.smoke_type {
            failures.push(format!("row {}: smoke_type {} != {}", row.n, smoke_type, row.smoke_type));
        }
        if s.variant.as_deref() != Some(row.variant.as_str()) {
            failures.push(format!("row {}: variant {:?} != {}", row.n, s.variant, row.variant));
        }
        let capture = s.t_capture.and_then(|m| m.clock);
        if !within(capture, row.capture, row.tolerance) {
            failures.push(format!(
                "row {}: capture {} != {} (tolerance {} s)",
                row.n,
                capture.map(|c| c.to_string()).unwrap_or_default(),
                row.capture,
                row.tolerance
            ));
        }
        if s.owner_flag {
            failures.push(format!("row {}: owner flagged: {}", row.n, s.owner_note));
        }
    }
    if ours.len() != rows.len() {
        failures.push(format!(
            "{} {} smokes found, reference lists {}",
            ours.len(),
            config.run.primary_team,
            rows.len()
        ));
    }
    assert!(failures.is_empty(), "reference mismatches:\n{}", failures.join("\n"));
}
