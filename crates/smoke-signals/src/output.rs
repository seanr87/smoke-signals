//! Writers for the smoke table, the game record and the run log.

use std::fmt::Write as _;
use std::path::Path;

use rootcause::prelude::*;
use serde::Serialize;

use crate::records::GameRecord;
use crate::records::Moment;
use crate::records::SmokeRecord;
use crate::records::StateSnapshot;
use crate::records::Xz;

pub fn write_json<T: Serialize>(path: &Path, value: &T) -> Result<(), Report> {
    let text = serde_json::to_string_pretty(value).attach_with(|| format!("serializing {}", path.display()))?;
    std::fs::write(path, text).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}

/// Quote a CSV field when it holds a separator, a quote or a line break.
pub fn csv_field(text: &str) -> String {
    if text.contains([',', '"', '\n', '\r']) { format!("\"{}\"", text.replace('"', "\"\"")) } else { text.to_string() }
}

pub fn csv_line(fields: &[String]) -> String {
    fields.iter().map(|f| csv_field(f)).collect::<Vec<_>>().join(",")
}

pub fn opt<T: std::fmt::Display>(v: Option<T>) -> String {
    v.map(|v| v.to_string()).unwrap_or_default()
}

fn opt_f(v: Option<f32>) -> String {
    v.map(|v| format!("{v:.2}")).unwrap_or_default()
}

fn moment_s(m: Option<Moment>) -> String {
    m.map(|m| format!("{:.2}", m.seconds)).unwrap_or_default()
}

fn moment_clock(m: Option<Moment>) -> String {
    m.map(|m| m.clock_text()).unwrap_or_default()
}

fn xz(p: &Xz) -> String {
    format!("{:.0}:{:.0}", p.x, p.z)
}

/// Tier 1 columns of one moment, in `STATE_COLUMNS` order.
fn state_fields(s: Option<&StateSnapshot>) -> Vec<String> {
    match s {
        None => vec![String::new(); STATE_COLUMNS.len()],
        Some(s) => vec![
            opt(s.score_ours),
            opt(s.score_theirs),
            s.caps_text(),
            s.cap_state.iter().map(|c| format!("{}:{:.2}", c.cap, c.progress)).collect::<Vec<_>>().join(" "),
            s.ships_alive
                .iter()
                .map(|a| format!("{}/{}:{}", opt(a.team.as_deref()), opt(a.ship_class.as_deref()), a.alive))
                .collect::<Vec<_>>()
                .join(" "),
            s.alive_ours.to_string(),
            s.alive_theirs.to_string(),
            opt_f(s.smoker_hp_pct),
            opt(s.smoker_spotted),
            opt(s.smoker_spotted_flags.as_deref()),
            opt(s.enemy_radars_alive),
        ],
    }
}

const STATE_COLUMNS: &[&str] = &[
    "score_ours",
    "score_theirs",
    "cap_state",
    "cap_progress",
    "ships_alive",
    "alive_ours",
    "alive_theirs",
    "smoker_hp_pct",
    "smoker_spotted",
    "smoker_spotted_flags",
    "enemy_radars_alive",
];

const BASE_COLUMNS: &[&str] = &[
    "smoke_id",
    "activation_id",
    "match_id",
    "round",
    "game_no",
    "map",
    "game_build",
    "primary_replay",
    "merged_replays",
    "team",
    "opponent",
    "spawn_side",
    "player",
    "ship",
    "ship_class",
    "ship_tier",
    "smoke_type",
    "variant",
    "charge_no",
    "charges_total",
    "base_emission_s",
    "base_puff_life_s",
    "base_radius",
    "radius",
    "observed_emission_s",
    "emission_cut_short",
    "owner_flag",
    "owner_note",
    "owner_distance_m",
    "overlap_flag",
    "overlapping_smoke_ids",
    "origin_xy",
    "bbox",
    "puff_count",
    "path",
    "t_created",
    "t_created_clock",
    "t_activate",
    "t_activate_clock",
    "t_capture",
    "t_capture_clock",
    "t_emission_end",
    "t_emission_end_clock",
    "t_dispersed",
    "t_dispersed_clock",
];

const TAIL_COLUMNS: &[&str] =
    &["wows_toolkit_rev", "smoke_signals_version", "generated_at", "frame_act", "frame_cap", "clip"];

/// All columns: base, Tier 1 at activation (`_act`), Tier 1 at capture
/// (`_cap`), then provenance and files.
pub fn smoke_csv_columns() -> Vec<String> {
    let mut cols: Vec<String> = BASE_COLUMNS.iter().map(|c| c.to_string()).collect();
    cols.extend(STATE_COLUMNS.iter().map(|c| format!("{c}_act")));
    cols.extend(STATE_COLUMNS.iter().map(|c| format!("{c}_cap")));
    cols.extend(TAIL_COLUMNS.iter().map(|c| c.to_string()));
    cols
}

pub fn smoke_csv_row(r: &SmokeRecord) -> Vec<String> {
    let mut row = vec![
        r.smoke_id.to_string(),
        opt(r.activation_id.as_deref()),
        r.match_id.clone(),
        opt(r.round.as_deref()),
        opt(r.game_no),
        r.map.clone(),
        r.game_build.clone(),
        r.primary_replay.clone(),
        r.merged_replays.join(";"),
        opt(r.team.as_deref()),
        opt(r.opponent.as_deref()),
        opt(r.spawn_side.as_deref()),
        opt(r.player.as_deref()),
        opt(r.ship.as_deref()),
        opt(r.ship_class.as_deref()),
        opt(r.ship_tier),
        opt(r.smoke_type.map(|t| t.as_str())),
        opt(r.variant.as_deref()),
        opt(r.charge_no),
        opt(r.charges_total),
        opt_f(r.base_emission_s),
        opt_f(r.base_puff_life_s),
        opt_f(r.base_radius),
        format!("{:.2}", r.radius),
        opt_f(r.observed_emission_s),
        r.emission_cut_short.to_string(),
        r.owner_flag.to_string(),
        r.owner_note.clone(),
        opt_f(r.owner_distance_m),
        r.overlap_flag.to_string(),
        r.overlapping_smoke_ids.iter().map(|i| i.to_string()).collect::<Vec<_>>().join(";"),
        xz(&r.origin_xy),
        r.bbox.map(|b| format!("{:.0}:{:.0}:{:.0}:{:.0}", b.min_x, b.min_z, b.max_x, b.max_z)).unwrap_or_default(),
        r.puff_count.to_string(),
        r.path.as_ref().map(|p| p.iter().map(xz).collect::<Vec<_>>().join(";")).unwrap_or_default(),
        moment_s(Some(r.t_created)),
        moment_clock(Some(r.t_created)),
        moment_s(r.t_activate),
        moment_clock(r.t_activate),
        moment_s(r.t_capture),
        moment_clock(r.t_capture),
        moment_s(r.t_emission_end),
        moment_clock(r.t_emission_end),
        moment_s(r.t_dispersed),
        moment_clock(r.t_dispersed),
    ];
    row.extend(state_fields(r.state_at_activate.as_ref()));
    row.extend(state_fields(r.state_at_capture.as_ref()));
    row.extend([
        opt(r.wows_toolkit_rev.as_deref()),
        r.smoke_signals_version.clone(),
        r.generated_at.clone(),
        opt(r.frame_act.as_deref()),
        opt(r.frame_cap.as_deref()),
        opt(r.clip.as_deref()),
    ]);
    row
}

pub fn write_smokes_csv(path: &Path, smokes: &[SmokeRecord]) -> Result<(), Report> {
    let columns = smoke_csv_columns();
    let mut text = String::new();
    text.push_str(&columns.join(","));
    text.push('\n');
    for r in smokes {
        let row = smoke_csv_row(r);
        assert_eq!(row.len(), columns.len(), "smoke CSV row and column list differ");
        text.push_str(&csv_line(&row));
        text.push('\n');
    }
    std::fs::write(path, text).attach_with(|| format!("writing {}", path.display()))?;
    Ok(())
}

/// A short, fixed-width summary table for the terminal and the run log.
pub fn summary_table(smokes: &[SmokeRecord]) -> String {
    let mut out = String::new();
    let _ = writeln!(
        out,
        "{:<5} {:<6} {:<26} {:<13} {:<9} {:<15} {:>7} {:>7} {:>7} {:>8} {:>5} {}",
        "id", "team", "player", "ship", "type", "variant", "act", "capture", "gone", "emit_s", "puffs", "flags"
    );
    for r in smokes {
        let mut flags = Vec::new();
        if r.owner_flag {
            flags.push("owner");
        }
        if r.overlap_flag {
            flags.push("overlap");
        }
        if r.emission_cut_short {
            flags.push("cut");
        }
        let _ = writeln!(
            out,
            "{:<5} {:<6} {:<26} {:<13} {:<9} {:<15} {:>7} {:>7} {:>7} {:>8} {:>5} {}",
            r.smoke_id,
            opt(r.team.as_deref()),
            opt(r.player.as_deref()),
            opt(r.ship.as_deref()),
            opt(r.smoke_type.map(|t| t.as_str())),
            opt(r.variant.as_deref()),
            moment_clock(r.t_activate),
            moment_clock(r.t_capture),
            moment_clock(r.t_dispersed),
            opt_f(r.observed_emission_s),
            r.puff_count,
            flags.join(",")
        );
    }
    out
}

/// Tier 1 and file fields that are empty, with the reason, one line per gap.
pub fn tier1_gaps(smokes: &[SmokeRecord]) -> Vec<String> {
    let mut gaps = Vec::new();
    for r in smokes {
        let id = r.smoke_id;
        if r.player.is_none() {
            gaps.push(format!("smoke {id}: no owner, so player, ship, team and smoker fields are empty ({})", r.owner_note));
        }
        if r.t_activate.is_none() {
            gaps.push(format!("smoke {id}: no activation recorded; t_activate is empty and the activation frame and clip start use the smoke's first appearance"));
        }
        if r.t_capture.is_none() {
            gaps.push(format!("smoke {id}: no new puff was ever observed, so t_capture and the capture frame are empty"));
        }
        if r.t_dispersed.is_none() {
            gaps.push(format!("smoke {id}: still standing when the replay ended; t_dispersed is empty and the clip ends at the replay end"));
        }
        for (stage, state) in [("activation", &r.state_at_activate), ("capture", &r.state_at_capture)] {
            match state {
                None => gaps.push(format!("smoke {id}: no Tier 1 state at {stage} (no frame was rendered there)")),
                Some(s) => {
                    if s.score_ours.is_none() || s.score_theirs.is_none() {
                        gaps.push(format!("smoke {id}: score unknown at {stage} (no team for the smoker)"));
                    }
                    if s.smoker_hp_pct.is_none() {
                        gaps.push(format!("smoke {id}: smoker HP unknown at {stage} (no vehicle state for the smoker)"));
                    }
                    if s.smoker_spotted.is_none() {
                        gaps.push(format!(
                            "smoke {id}: smoker detection unknown at {stage} (no visibilityFlags seen for the smoker)"
                        ));
                    }
                    if s.enemy_radars_alive.is_none() {
                        gaps.push(format!("smoke {id}: enemy radars unknown at {stage} (no opposing team)"));
                    }
                }
            }
        }
    }
    gaps
}

pub fn run_log(game: &GameRecord, smokes: &[SmokeRecord], frames_written: usize, clips_written: usize) -> String {
    let mut log = String::new();
    let _ = writeln!(log, "# Smoke Signals run log\n");
    let _ = writeln!(log, "- generated_at: {}", game.generated_at);
    let _ = writeln!(
        log,
        "- match: {} {} {} game {}",
        opt(game.tournament.as_deref()),
        game.match_id,
        opt(game.round.as_deref()),
        opt(game.game_no)
    );
    let _ = writeln!(log, "- map: {} ({})", game.map, game.map_name);
    let _ = writeln!(log, "- game_build: {}", game.game_build);
    let _ = writeln!(log, "- primary_replay: {}", game.primary_replay);
    for m in &game.merged_replays {
        let _ = writeln!(log, "- merged_replay: {m}");
    }
    let _ = writeln!(log, "- wows_toolkit_rev: {}", opt(game.wows_toolkit_rev.as_deref()));
    let _ = writeln!(log, "- smoke_signals_version: {}", game.smoke_signals_version);
    let _ = writeln!(log, "\n## Result\n");
    for t in &game.teams {
        let _ = writeln!(
            log,
            "- {} (team {}, spawn {}): score {}, {} players",
            opt(t.name.as_deref()),
            t.team_id,
            opt(t.spawn_side.as_deref()),
            opt(t.final_score),
            t.players.len()
        );
    }
    let _ = writeln!(log, "- outcome: {}", game.outcome_text());
    let _ = writeln!(log, "- finish_type: {}", opt(game.finish_type.as_deref()));
    let _ = writeln!(
        log,
        "- battle_end: {} ({} s)",
        game.battle_end.map(|m| m.clock_text()).unwrap_or_default(),
        moment_s(game.battle_end)
    );
    let _ = writeln!(log, "- replay_end_s: {:.1} (truncated: {})", game.replay_end_s, game.replay_truncated);
    let _ = writeln!(
        log,
        "\n## Smokes ({}), frames written: {}, clips written: {}\n",
        smokes.len(),
        frames_written,
        clips_written
    );
    let _ = writeln!(log, "```\n{}```", summary_table(smokes));
    let flagged: Vec<&SmokeRecord> = smokes.iter().filter(|s| s.owner_flag).collect();
    if !flagged.is_empty() {
        let _ = writeln!(log, "\n## Owner flags\n");
        for s in flagged {
            let _ = writeln!(log, "- smoke {}: {}", s.smoke_id, s.owner_note);
        }
    }
    let gaps = tier1_gaps(smokes);
    let _ = writeln!(log, "\n## Tier 1 gaps ({})\n", gaps.len());
    if gaps.is_empty() {
        let _ = writeln!(log, "- none: every Tier 1 field is filled for every smoke");
    }
    for g in gaps {
        let _ = writeln!(log, "- {g}");
    }
    log
}
