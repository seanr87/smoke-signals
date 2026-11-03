//! Game data loading for renderer tools: a full game install or a dump
//! produced by `wows-data-mgr`.

use std::fs::File;
use std::path::Path;
use std::path::PathBuf;

use rootcause::prelude::*;
use tracing::info;
use tracing::warn;
use wows_replays::game_constants::GameConstants;
use wowsunpack::data::Version;
use wowsunpack::game_data;
use wowsunpack::game_params::provider::GameMetadataProvider;
use wowsunpack::game_params::types::GameParamProvider;
use wowsunpack::game_params::types::Param;
use wowsunpack::rpc::entitydefs::EntitySpec;
use wowsunpack::vfs::VfsPath;

/// Game resources for one build. Two providers are built because the renderer
/// and the battle controller each take ownership of one.
pub struct LoadedGameData {
    pub vfs: VfsPath,
    pub specs: Vec<EntitySpec>,
    pub game_params: GameMetadataProvider,
    pub controller_game_params: GameMetadataProvider,
}

/// Load game data from a full WoWS game installation.
pub fn load_from_game_dir(game_dir: &Path, replay_version: &Version) -> Result<LoadedGameData, Report> {
    let replay_build =
        replay_version.build_number().ok_or_else(|| report!("replay version carries no build number"))?;
    info!(build = replay_build, "Loading game data");
    let resources = game_data::load_game_resources(game_dir, replay_version).map_err(|e| report!("{e}"))?;
    let vfs = resources.vfs;
    let specs = resources.specs;

    info!("Loading game params");
    let mut game_params =
        GameMetadataProvider::from_vfs(&vfs).map_err(|e| report!("Failed to load GameParams: {e:?}"))?;
    let mut controller_game_params =
        GameMetadataProvider::from_vfs(&vfs).map_err(|e| report!("Failed to load GameParams for controller: {e:?}"))?;

    let mo_path = game_data::translations_path(game_dir, replay_build);
    load_translations(Some(&mo_path), &mut game_params, &mut controller_game_params);

    Ok(LoadedGameData { vfs, specs, game_params, controller_game_params })
}

struct ExtractedMetadata {
    version: String,
    build: u32,
}

fn read_metadata(path: &Path) -> Option<ExtractedMetadata> {
    let contents = std::fs::read_to_string(path.join("metadata.toml")).ok()?;
    let table: toml::Table = contents.parse().ok()?;
    Some(ExtractedMetadata {
        version: table.get("version")?.as_str()?.to_string(),
        build: table.get("build")?.as_integer()? as u32,
    })
}

/// Resolve the extracted data directory. If the user passed a parent directory
/// containing version subdirectories (e.g. `15.1.0_11965230/`), auto-detect the
/// right one. If they passed the version dir itself, use it directly.
pub fn resolve_extracted_dir(path: &Path, replay_version: &Version) -> Result<PathBuf, Report> {
    if !path.exists() {
        bail!("Extracted data directory does not exist: {}", path.display());
    }

    let replay_build =
        replay_version.build_number().ok_or_else(|| report!("replay version carries no build number"))?;

    // If the path itself contains metadata.toml, it's already the version dir
    if let Some(meta) = read_metadata(path) {
        if meta.build != replay_build {
            bail!(
                "Extracted data is build {} ({}) but replay is build {}. \
                 Entity definitions will not match. Use extracted data for the correct build.",
                meta.build,
                meta.version,
                replay_build
            );
        }
        return Ok(path.to_path_buf());
    }

    // Otherwise, scan for version subdirectories
    let mut candidates: Vec<(PathBuf, ExtractedMetadata)> = Vec::new();
    let entries = std::fs::read_dir(path).attach_with(|| format!("Failed to read directory: {}", path.display()))?;

    for entry in entries.flatten() {
        let sub = entry.path();
        if let Some(meta) = read_metadata(&sub) {
            candidates.push((sub, meta));
        }
    }

    if candidates.is_empty() {
        bail!(
            "No extracted game data found in {}. Expected either a version directory \
             (containing metadata.toml, vfs/, game_params.rkyv) or a parent directory \
             containing version subdirectories (e.g. 15.1.0_11965230/).",
            path.display()
        );
    }

    // Try to match by build number first
    if let Some(matched) = candidates.iter().find(|(_, m)| m.build == replay_build) {
        info!("Matched extracted data for build {}: {}", replay_build, matched.0.display());
        return Ok(matched.0.clone());
    }

    // Try version-based fallback via BuildsIndex (supports cross-region replays)
    let builds_path = path.join("builds.toml");
    if builds_path.exists() {
        let version_str = format!("{}.{}.{}", replay_version.major, replay_version.minor, replay_version.patch);
        let index = wows_data_mgr::builds::BuildsIndex::load(&builds_path);
        if let Some((entry, _exact)) = index.resolve_build(replay_build, Some(&version_str)) {
            let resolved = path.join(&entry.dir);
            warn!("No exact data for build {}; using {} (build {})", replay_build, entry.version, entry.build);
            return Ok(resolved);
        }
    }

    // Also try version prefix match on candidates (legacy dumps without builds.toml)
    let version_str = format!("{}.{}.{}", replay_version.major, replay_version.minor, replay_version.patch);
    if let Some(matched) = candidates.iter().find(|(_, m)| m.version == version_str) {
        warn!("No exact data for build {}; using {} (build {})", replay_build, matched.1.version, matched.1.build);
        return Ok(matched.0.clone());
    }

    let available: Vec<String> = candidates.iter().map(|(_, m)| format!("{} (build {})", m.version, m.build)).collect();
    bail!(
        "No extracted data matches replay build {}. Available versions in {}: {}",
        replay_build,
        path.display(),
        available.join(", ")
    );
}

/// Load game data from a pre-extracted renderer data directory.
pub fn load_from_extracted(
    extracted_dir: &Path,
    recreate_game_params: bool,
    params_cache: Option<&Path>,
) -> Result<LoadedGameData, Report> {
    use std::borrow::Cow;
    use std::io::Read;
    use wows_data_mgr::overrides;
    use wowsunpack::data::DataFileWithCallback;
    use wowsunpack::rpc::entitydefs::parse_scripts;

    info!("Loading from extracted directory: {}", extracted_dir.display());

    let mut dump = wows_data_mgr::Dump::open(extracted_dir);
    if !dump.has_game_files() {
        bail!("no game files found in {}", extracted_dir.display());
    }
    // A dump may be a shared, read-only checkout of the published archive, so a
    // cache rebuilt against the current rkyv format goes to a local per-build
    // directory every tool resolves the same way.
    if let Some(root) =
        params_cache.map(Path::to_path_buf).or_else(|| dump.build().and_then(overrides::build_override_root))
    {
        dump.set_override_root(root);
    }
    let vfs = dump.vfs();

    // Load entity specs from VFS
    info!("Loading entity specs");
    let specs = {
        let vfs_ref = &vfs;
        let loader = DataFileWithCallback::new(move |path: &str| {
            let mut data = Vec::new();
            vfs_ref.join(path)?.open_file()?.read_to_end(&mut data)?;
            Ok(Cow::Owned(data))
        });
        parse_scripts(&loader).map_err(|e| report!("Failed to parse entity specs: {e:?}"))?
    };

    // Load GameParams: try rkyv cache first, fall back to VFS if --recreate-game-params
    let rkyv_path = dump.derived_path("game_params.rkyv");
    let params: Vec<Param> = match rkyv_path.as_deref().and_then(wowsunpack::game_params::cache::load) {
        Some(params) => {
            info!("Loaded game params from rkyv cache");
            params
        }
        None if recreate_game_params => {
            match &rkyv_path {
                Some(path) => warn!("game params cache at {} does not load; recreating", path.display()),
                None => info!("no game params cache in this dump, creating from GameParams.data"),
            }
            let write_path = dump
                .derived_write_path("game_params.rkyv")
                .ok_or_else(|| report!("nowhere to write a rebuilt game params cache"))?;
            recreate_rkyv_from_vfs(&vfs, &write_path)?
        }
        None => {
            bail!(
                "the game params cache for this dump is missing or does not load.\n\
                   Hint: pass --recreate-game-params to rebuild it from GameParams.data"
            );
        }
    };

    // Build providers with entity specs from the extracted VFS. The replay
    // scan (scan_salvo_flight_times) reads entity defs through the provider's
    // entity_specs(); from_params_no_specs would leave that empty and the
    // packet parser would have no specs to resolve EntityCreate against. This
    // matches the game-dir path, which builds providers via from_vfs.
    let mut game_params = GameMetadataProvider::from_params_with_vfs(params.clone(), &vfs)
        .map_err(|e| report!("Failed to build GameMetadataProvider: {e:?}"))?;
    let mut controller_game_params = GameMetadataProvider::from_params_with_vfs(params, &vfs)
        .map_err(|e| report!("Failed to build controller GameMetadataProvider: {e:?}"))?;

    let mo_path = dump.derived_path("translations/en/LC_MESSAGES/global.mo");
    load_translations(mo_path.as_deref(), &mut game_params, &mut controller_game_params);

    Ok(LoadedGameData { vfs, specs, game_params, controller_game_params })
}

/// Why a dump's `constants.json` could not be merged. The I/O or JSON error
/// is attached as the report's child, as `error::VideoError` does.
#[derive(Debug)]
pub enum DumpConstantsError {
    Read { path: PathBuf },
    Parse { path: PathBuf },
}

impl std::fmt::Display for DumpConstantsError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Read { path } => write!(f, "cannot read {}", path.display()),
            Self::Parse { path } => write!(f, "cannot parse {}", path.display()),
        }
    }
}

impl std::error::Error for DumpConstantsError {}

/// Merge the dump's `constants.json` into `constants`. Returns the merged
/// path, or `None` when the dump has no such file.
pub fn merge_dump_constants(
    constants: &mut GameConstants,
    extracted_dir: &Path,
    replay_version: Version,
) -> Result<Option<PathBuf>, Report<DumpConstantsError>> {
    let path = extracted_dir.join("constants.json");
    if !path.exists() {
        return Ok(None);
    }
    let data = std::fs::read_to_string(&path).context(DumpConstantsError::Read { path: path.clone() })?;
    let json =
        serde_json::from_str::<serde_json::Value>(&data).context(DumpConstantsError::Parse { path: path.clone() })?;
    constants.merge_replay_constants(&json, replay_version);
    Ok(Some(path))
}

/// Load GameParams from VFS, serialize to rkyv, and write the cache file.
fn recreate_rkyv_from_vfs(vfs: &VfsPath, rkyv_path: &Path) -> Result<Vec<Param>, Report> {
    use std::sync::Arc;

    let game_metadata =
        GameMetadataProvider::from_vfs(vfs).map_err(|e| report!("Failed to load GameParams from VFS: {e:?}"))?;
    let params: Vec<Param> = game_metadata.params().iter().map(|p| Arc::unwrap_or_clone(Arc::clone(p))).collect();
    wowsunpack::game_params::cache::save(rkyv_path, &params)
        .attach_with(|| format!("Failed to write {}", rkyv_path.display()))?;
    info!("Wrote {}", rkyv_path.display());
    Ok(params)
}

/// Apply the gettext catalog at `mo_path` to both providers. Ship names fall
/// back to raw param indices when no catalog is available.
fn load_translations(
    mo_path: Option<&Path>,
    game_params: &mut GameMetadataProvider,
    controller_game_params: &mut GameMetadataProvider,
) {
    let Some(mo_path) = mo_path.filter(|path| path.exists()) else {
        warn!(path = ?mo_path, "Translations not found, ship names will be unavailable");
        return;
    };
    let parse = || File::open(mo_path).ok().and_then(|file| gettext::Catalog::parse(file).ok());
    match (parse(), parse()) {
        (Some(catalog), Some(controller_catalog)) => {
            game_params.set_translations(catalog);
            controller_game_params.set_translations(controller_catalog);
        }
        _ => warn!(path = ?mo_path, "Failed to parse translations"),
    }
}
