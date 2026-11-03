//! Batch analysis over the replay inventory: one run per game and per team
//! in scope, each with that team's replay as the primary, keeping only that
//! team's smokes.

use std::collections::BTreeMap;
use std::fmt::Write as _;
use std::path::Path;
use std::path::PathBuf;
use std::sync::Mutex;

use rootcause::prelude::*;
use serde::Serialize;
use tracing::info;

use crate::analysis;
use crate::clips;
use crate::config::Config;
use crate::frames;
use crate::output;
use crate::records::SmokeRecord;
use crate::replays;
use crate::session;
use crate::session::GameData;

/// One analysis run: a played game seen from one team's replay.
#[derive(Debug, Clone)]
pub struct Job {
    pub match_id: String,
    pub stage: String,
    pub group: String,
    pub round: String,
    pub game_no: u32,
    pub map: String,
    pub teams: String,
    pub team: String,
    pub opponent: String,
    pub folder: PathBuf,
    pub primary_file: String,
}

impl Job {
    /// Folder name for this run's outputs.
    pub fn name(&self) -> String {
        let folder = self.folder.file_name().map(|f| f.to_string_lossy().to_string()).unwrap_or_default();
        format!("{}_{}", folder, slug(&self.team))
    }
}

/// The inventory rows that can be analysed.
pub fn jobs_from_inventory(path: &Path, repo_root: &Path, teams_in_scope: &[String]) -> Result<Vec<Job>, Report> {
    let text = std::fs::read_to_string(path).attach_with(|| format!("reading {}", path.display()))?;
    let mut lines = text.lines().map(str::trim_end).filter(|l| !l.is_empty());
    let header: Vec<&str> = lines.next().ok_or_else(|| report!("{} is empty", path.display()))?.split(',').collect();
    let col = |name: &str| -> Result<usize, Report> {
        header.iter().position(|h| *h == name).ok_or_else(|| report!("{} has no column {name}", path.display()))
    };
    let (c_match, c_stage, c_group, c_round, c_game, c_map, c_teams, c_ours, c_folder, c_files, c_status) = (
        col("match_id")?,
        col("stage")?,
        col("group")?,
        col("round")?,
        col("game_no")?,
        col("map")?,
        col("teams")?,
        col("our_teams")?,
        col("replay_folder")?,
        col("replay_files")?,
        col("status")?,
    );
    let mut jobs = Vec::new();
    for line in lines {
        let f = split_csv(line);
        if f.len() < header.len() || f[c_status] != "played" || f[c_folder].is_empty() {
            continue;
        }
        let teams: Vec<&str> = f[c_teams].split(" vs ").collect();
        let files: Vec<&str> = f[c_files].split(';').filter(|s| !s.is_empty()).collect();
        for team in f[c_ours].split(';').filter(|t| !t.is_empty()) {
            if !teams_in_scope.is_empty() && !teams_in_scope.iter().any(|t| t == team) {
                continue;
            }
            let suffix = format!("_{}.wowsreplay", slug(team));
            let Some(primary) = files.iter().find(|p| p.ends_with(&suffix)) else {
                tracing::warn!(match_id = f[c_match], game = f[c_game], team, "No replay for this team; skipped");
                continue;
            };
            let primary_file = Path::new(primary).file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
            let opponent = teams.iter().find(|t| **t != team).copied().unwrap_or("").to_string();
            jobs.push(Job {
                match_id: f[c_match].to_string(),
                stage: f[c_stage].to_string(),
                group: f[c_group].to_string(),
                round: f[c_round].to_string(),
                game_no: f[c_game].parse().attach_with(|| format!("game_no {}", f[c_game]))?,
                map: f[c_map].to_string(),
                teams: f[c_teams].to_string(),
                team: team.to_string(),
                opponent,
                folder: repo_root.join(&f[c_folder]),
                primary_file,
            });
        }
    }
    Ok(jobs)
}

/// Fields of one CSV line; a double-quoted field may hold commas.
fn split_csv(line: &str) -> Vec<String> {
    let mut out = Vec::new();
    let mut field = String::new();
    let mut quoted = false;
    let mut chars = line.chars().peekable();
    while let Some(c) = chars.next() {
        match c {
            '"' if quoted && chars.peek() == Some(&'"') => {
                field.push('"');
                chars.next();
            }
            '"' => quoted = !quoted,
            ',' if !quoted => out.push(std::mem::take(&mut field)),
            _ => field.push(c),
        }
    }
    out.push(field);
    out
}

fn slug(s: &str) -> String {
    let mut out = String::new();
    let mut dash = false;
    for c in s.chars() {
        if c.is_ascii_alphanumeric() {
            out.push(c.to_ascii_lowercase());
            dash = false;
        } else if !dash && !out.is_empty() {
            out.push('-');
            dash = true;
        }
    }
    out.trim_end_matches('-').to_string()
}

/// Config for one job: the game folder, the team names and the match labels.
pub fn job_config(base: &Config, job: &Job) -> Config {
    let mut config = base.clone();
    config.paths.replays = job.folder.clone();
    config.run.primary_team = job.team.clone();
    config.run.opponent_team = Some(job.opponent.clone());
    config.run.primary_replay = Some(job.primary_file.clone());
    config.run.merge = true;
    config.game.match_id = Some(format!("kots19na_{}", job.match_id));
    let round = [job.stage.as_str(), job.group.as_str(), job.round.as_str()]
        .iter()
        .filter(|s| !s.is_empty())
        .copied()
        .collect::<Vec<_>>()
        .join(" / ");
    config.game.round = Some(round);
    config.game.game_no = Some(job.game_no);
    config
}

/// What one job produced, for the batch log.
#[derive(Debug, Clone, Serialize)]
pub struct JobReport {
    pub name: String,
    pub match_id: String,
    pub game_no: u32,
    pub map: String,
    pub team: String,
    pub smokes: usize,
    pub kept: usize,
    pub flagged: usize,
    pub flagged_notes: Vec<String>,
    pub overlaps: usize,
    pub frames: usize,
    pub warnings: Vec<String>,
    pub error: Option<String>,
    pub seconds: f32,
}

/// Run one job: analyse, render frames, keep the team's own smokes.
pub fn run_job(
    base: &Config,
    game_data: &GameData,
    job: &Job,
    out_dir: &Path,
    render_frames: bool,
    clip_ids: &[u32],
) -> Result<(Vec<SmokeRecord>, JobReport), Report> {
    let started = std::time::Instant::now();
    let config = job_config(base, job);
    let replays = replays::load_game_folder(
        &config.paths.replays,
        &config.run.team_prefix,
        config.run.merge,
        config.run.primary_replay.as_deref(),
    )?;
    let version = wowsunpack::data::Version::from_client_exe(&replays.primary.meta.clientVersionFromExe);
    if format!("{version:?}") != format!("{:?}", game_data.version) {
        bail!("replay version {version:?} does not match the loaded game data {:?}", game_data.version);
    }
    let mut analysis = analysis::analyze_game(&config, game_data, &replays)?;
    let total = analysis.smokes.len();
    let selected: Vec<usize> = analysis
        .smokes
        .iter()
        .enumerate()
        .filter(|(_, s)| s.team.as_deref() == Some(job.team.as_str()))
        .map(|(i, _)| i)
        .collect();
    std::fs::create_dir_all(out_dir).attach_with(|| format!("creating {}", out_dir.display()))?;
    let frames_written = if render_frames {
        frames::render_smoke_frames(
            &config,
            game_data,
            &replays,
            &analysis.game,
            &mut analysis.smokes,
            &selected,
            &out_dir.join("frames"),
        )?
    } else {
        0
    };
    let for_clips: Vec<usize> = selected.iter().copied().filter(|i| clip_ids.contains(&analysis.smokes[*i].smoke_id)).collect();
    if !for_clips.is_empty() {
        clips::render_clips(
            &config,
            game_data,
            &replays,
            &analysis.game,
            &mut analysis.smokes,
            &for_clips,
            &out_dir.join("clips"),
        )?;
    }
    let kept: Vec<SmokeRecord> = selected.iter().map(|i| analysis.smokes[*i].clone()).collect();
    output::write_smokes_csv(&out_dir.join("smokes.csv"), &kept)?;
    output::write_json(&out_dir.join("smokes.json"), &output::SmokesDocument { game: &analysis.game, smokes: &kept })?;
    output::write_json(&out_dir.join("game.json"), &analysis.game)?;
    let name_of = |e: u32| analysis.game.player(e).map(|p| p.player.clone());
    output::write_damage_events_csv(&out_dir.join("damage_events.csv"), &analysis.damage_events, &name_of)?;
    output::write_json(&out_dir.join("damage_spike.json"), &analysis.damage_stats)?;
    let log = output::run_log(&analysis.game, &kept, &analysis.damage_stats, frames_written, 0);
    std::fs::write(out_dir.join("run_log.md"), &log).attach_with(|| "writing run_log.md")?;
    let flagged: Vec<&SmokeRecord> = kept.iter().filter(|s| s.owner_flag).collect();
    let report = JobReport {
        name: job.name(),
        match_id: job.match_id.clone(),
        game_no: job.game_no,
        map: job.map.clone(),
        team: job.team.clone(),
        smokes: total,
        kept: kept.len(),
        flagged: flagged.len(),
        flagged_notes: flagged.iter().map(|s| format!("{} {}: {}", s.smoke_id, s.player.clone().unwrap_or_default(), s.owner_note)).collect(),
        overlaps: kept.iter().filter(|s| s.overlap_flag).count(),
        frames: frames_written,
        warnings: Vec::new(),
        error: None,
        seconds: started.elapsed().as_secs_f32(),
    };
    Ok((kept, report))
}

/// Captures WARN and ERROR events per thread so the batch log can list them
/// under the game that produced them.
#[derive(Default)]
pub struct WarningSink {
    lines: Mutex<Vec<(std::thread::ThreadId, String)>>,
}

impl WarningSink {
    pub const fn new() -> Self {
        Self { lines: Mutex::new(Vec::new()) }
    }

    pub fn take(&self, thread: std::thread::ThreadId) -> Vec<String> {
        let mut lines = self.lines.lock().expect("warning sink");
        let (mine, rest): (Vec<_>, Vec<_>) = lines.drain(..).partition(|(t, _)| *t == thread);
        *lines = rest;
        mine.into_iter().map(|(_, l)| l).collect()
    }
}

impl<S: tracing::Subscriber> tracing_subscriber::Layer<S> for &'static WarningSink {
    fn on_event(&self, event: &tracing::Event<'_>, _ctx: tracing_subscriber::layer::Context<'_, S>) {
        if *event.metadata().level() > tracing::Level::WARN {
            return;
        }
        struct Visitor(String);
        impl tracing::field::Visit for Visitor {
            fn record_debug(&mut self, field: &tracing::field::Field, value: &dyn std::fmt::Debug) {
                if field.name() == "message" {
                    let _ = write!(self.0, "{value:?} ");
                } else {
                    let _ = write!(self.0, "{}={value:?} ", field.name());
                }
            }
        }
        let mut visitor = Visitor(String::new());
        event.record(&mut visitor);
        let line = format!("{} {}", event.metadata().level(), visitor.0.trim_end());
        self.lines.lock().expect("warning sink").push((std::thread::current().id(), line));
    }
}

/// Load the game data once from the first job's primary replay.
pub fn load_game_data(config: &Config, jobs: &[Job]) -> Result<GameData, Report> {
    let first = jobs.first().ok_or_else(|| report!("no jobs to run"))?;
    let path = first.folder.join(&first.primary_file);
    let replay = wows_replays::ReplayFile::from_file(&path).attach_with(|| format!("loading replay {}", path.display()))?;
    session::load_game_data(&config.paths.game_data, &replay)
}

/// Run every job with `jobs` worker threads, writing per-game folders under
/// `out_dir/games/`, then the combined smoke table and the batch log.
pub fn run_batch(
    config: &Config,
    game_data: &GameData,
    jobs: &[Job],
    out_dir: &Path,
    workers: usize,
    render_frames: bool,
    clip_ids: &[u32],
    sink: &'static WarningSink,
) -> Result<(Vec<SmokeRecord>, Vec<JobReport>), Report> {
    let started = std::time::Instant::now();
    let next = std::sync::atomic::AtomicUsize::new(0);
    let results: Mutex<Vec<(usize, Vec<SmokeRecord>, JobReport)>> = Mutex::new(Vec::new());
    std::thread::scope(|scope| {
        for _ in 0..workers.max(1) {
            scope.spawn(|| {
                loop {
                    let i = next.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                    let Some(job) = jobs.get(i) else { break };
                    let game_dir = out_dir.join("games").join(job.name());
                    info!(job = %job.name(), index = i + 1, total = jobs.len(), "Batch job");
                    let outcome = run_job(config, game_data, job, &game_dir, render_frames, clip_ids);
                    let warnings = sink.take(std::thread::current().id());
                    let (smokes, mut report) = match outcome {
                        Ok(v) => v,
                        Err(e) => {
                            tracing::error!(job = %job.name(), "Job failed: {e:?}");
                            let report = JobReport {
                                name: job.name(),
                                match_id: job.match_id.clone(),
                                game_no: job.game_no,
                                map: job.map.clone(),
                                team: job.team.clone(),
                                smokes: 0,
                                kept: 0,
                                flagged: 0,
                                flagged_notes: Vec::new(),
                                overlaps: 0,
                                frames: 0,
                                warnings: Vec::new(),
                                error: Some(format!("{e:?}")),
                                seconds: 0.0,
                            };
                            (Vec::new(), report)
                        }
                    };
                    report.warnings = warnings;
                    results.lock().expect("results").push((i, smokes, report));
                }
            });
        }
    });
    let mut results = results.into_inner().expect("results");
    results.sort_by_key(|(i, _, _)| *i);
    let mut smokes = Vec::new();
    let mut reports = Vec::new();
    for (_, s, r) in results {
        smokes.extend(s);
        reports.push(r);
    }
    output::write_smokes_csv(&out_dir.join("smokes.csv"), &smokes)?;
    output::write_json(&out_dir.join("smokes.json"), &smokes)?;
    output::write_json(&out_dir.join("jobs.json"), &reports)?;
    std::fs::write(out_dir.join("run_log.md"), batch_log(&reports, &smokes, started.elapsed().as_secs_f32()))
        .attach_with(|| "writing run_log.md")?;
    Ok((smokes, reports))
}

fn batch_log(reports: &[JobReport], smokes: &[SmokeRecord], seconds: f32) -> String {
    let mut log = String::new();
    let _ = writeln!(log, "# Smoke Signals batch log\n");
    let _ = writeln!(log, "- runs: {}", reports.len());
    let _ = writeln!(log, "- failed runs: {}", reports.iter().filter(|r| r.error.is_some()).count());
    let _ = writeln!(log, "- smokes kept: {}", smokes.len());
    let _ = writeln!(log, "- flagged smokes: {}", reports.iter().map(|r| r.flagged).sum::<usize>());
    let _ = writeln!(log, "- wall time: {:.0} s\n", seconds);
    let mut per_team: BTreeMap<&str, (usize, usize)> = BTreeMap::new();
    for s in smokes {
        let e = per_team.entry(s.team.as_deref().unwrap_or("?")).or_default();
        e.0 += 1;
        if s.owner_flag {
            e.1 += 1;
        }
    }
    let _ = writeln!(log, "| team | smokes | flagged |\n| --- | --- | --- |");
    for (team, (n, flagged)) in &per_team {
        let _ = writeln!(log, "| {team} | {n} | {flagged} |");
    }
    let _ = writeln!(log, "\n## Runs\n");
    for r in reports {
        let _ = writeln!(
            log,
            "### {} (match {} game {}, {}, {})\n",
            r.name, r.match_id, r.game_no, r.map, r.team
        );
        match &r.error {
            Some(e) => {
                let _ = writeln!(log, "- FAILED: {e}");
            }
            None => {
                let _ = writeln!(
                    log,
                    "- smokes in game: {}, kept for {}: {}, flagged: {}, overlapping: {}, frames: {}, {:.0} s",
                    r.smokes, r.team, r.kept, r.flagged, r.overlaps, r.frames, r.seconds
                );
            }
        }
        for n in &r.flagged_notes {
            let _ = writeln!(log, "- flagged: {n}");
        }
        for w in &r.warnings {
            let _ = writeln!(log, "- {w}");
        }
        let _ = writeln!(log);
    }
    log
}
