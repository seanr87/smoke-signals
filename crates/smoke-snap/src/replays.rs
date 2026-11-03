//! Replay selection: the primary perspective is the recording made by a player
//! of the analyzed team; every other replay in the folder is merged into it.

use std::path::Path;
use std::path::PathBuf;

use rootcause::prelude::*;
use wows_replays::ReplayFile;

pub struct ReplaySet {
    pub primary_path: PathBuf,
    pub primary: ReplayFile,
    pub merge_paths: Vec<PathBuf>,
    /// Parallel to `merge_paths`. Empty when merging is off.
    pub merges: Vec<ReplayFile>,
}

/// Load every `.wowsreplay` in `dir` (one game per folder in Phase 1) and pick
/// the primary by the recording player's name prefix.
pub fn load_game_folder(dir: &Path, team_prefix: &str, merge: bool) -> Result<ReplaySet, Report> {
    let entries = std::fs::read_dir(dir).attach_with(|| format!("reading replay folder {}", dir.display()))?;
    let mut paths: Vec<PathBuf> = Vec::new();
    for entry in entries {
        let path = entry.attach_with(|| format!("reading replay folder {}", dir.display()))?.path();
        if path.extension().is_some_and(|ext| ext.eq_ignore_ascii_case("wowsreplay")) {
            paths.push(path);
        }
    }
    paths.sort();
    if paths.is_empty() {
        bail!("no .wowsreplay files in {}", dir.display());
    }

    let mut loaded: Vec<(PathBuf, ReplayFile)> = Vec::with_capacity(paths.len());
    for path in paths {
        let file = ReplayFile::from_file(&path).attach_with(|| format!("loading replay {}", path.display()))?;
        loaded.push((path, file));
    }

    let is_primary = |file: &ReplayFile| file.meta.playerName.starts_with(team_prefix);
    let primary_count = loaded.iter().filter(|(_, f)| is_primary(f)).count();
    if primary_count != 1 {
        let names: Vec<&str> = loaded.iter().map(|(_, f)| f.meta.playerName.as_str()).collect();
        bail!(
            "expected exactly one replay recorded by a {team_prefix}* player in {}, found {primary_count} (recorders: {})",
            dir.display(),
            names.join(", ")
        );
    }
    let primary_idx = loaded.iter().position(|(_, f)| is_primary(f)).expect("counted above");
    let (primary_path, primary) = loaded.remove(primary_idx);
    let (merge_paths, merges) = if merge { loaded.into_iter().unzip() } else { (Vec::new(), Vec::new()) };
    Ok(ReplaySet { primary_path, primary, merge_paths, merges })
}
