//! `config.toml`: machine paths and run settings. See `smoke/config.example.toml`.

use std::path::Path;
use std::path::PathBuf;

use serde::Deserialize;

#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("cannot read config file {path}")]
    Read {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("cannot parse config file {path}")]
    Parse {
        path: PathBuf,
        #[source]
        source: toml::de::Error,
    },
    #[error("color {text:?} is not of the form #RRGGBB")]
    Color { text: String },
    #[error("render.clip_fps must be at least 1, got {value}")]
    ClipFps { value: u32 },
}

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub paths: Paths,
    pub run: Run,
    pub render: Render,
    /// Identity of the game in `paths.replays` (Phase 1: one game per folder).
    #[serde(default)]
    pub game: Game,
}

#[derive(Debug, Clone, Deserialize)]
pub struct Paths {
    pub replays: PathBuf,
    pub game_data: PathBuf,
    pub output: PathBuf,
}

#[derive(Debug, Clone, Deserialize)]
pub struct Run {
    /// Player-name prefix of the team being analyzed, e.g. `HSR_`.
    pub team_prefix: String,
    pub primary_team: String,
    pub merge: bool,
}

#[derive(Debug, Clone, Deserialize)]
pub struct Render {
    pub show_player_names: bool,
    pub exhaust_color: HexColor,
    pub highlight_color: HexColor,
    pub clip_fps: u32,
    pub clip_pre_seconds: u32,
}

#[derive(Debug, Clone, Default, Deserialize)]
pub struct Game {
    /// Tournament name for the frame footer, e.g. `KotS XIX NA`.
    pub tournament: Option<String>,
    /// Tournament match identifier, e.g. `kots19na_GF`. Defaults to the
    /// primary replay's file stem.
    pub match_id: Option<String>,
    pub round: Option<String>,
    pub game_no: Option<u32>,
}

/// An opaque `#RRGGBB` color.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(try_from = "String")]
pub struct HexColor(pub [u8; 3]);

impl HexColor {
    pub fn rgba(self, alpha: u8) -> [u8; 4] {
        [self.0[0], self.0[1], self.0[2], alpha]
    }
}

impl TryFrom<String> for HexColor {
    type Error = ConfigError;

    fn try_from(text: String) -> Result<Self, Self::Error> {
        let digits = text.strip_prefix('#').filter(|d| d.len() == 6 && d.is_ascii());
        let parsed = digits.and_then(|d| {
            let channel = |i: usize| u8::from_str_radix(&d[i..i + 2], 16).ok();
            Some([channel(0)?, channel(2)?, channel(4)?])
        });
        parsed.map(HexColor).ok_or(ConfigError::Color { text })
    }
}

impl Config {
    /// Load `path`. Relative paths inside the file are taken relative to the
    /// file's directory, so the same config works from any working directory.
    pub fn load(path: &Path) -> Result<Self, ConfigError> {
        let text =
            std::fs::read_to_string(path).map_err(|source| ConfigError::Read { path: path.to_path_buf(), source })?;
        let mut config: Config =
            toml::from_str(&text).map_err(|source| ConfigError::Parse { path: path.to_path_buf(), source })?;
        if config.render.clip_fps == 0 {
            return Err(ConfigError::ClipFps { value: config.render.clip_fps });
        }
        let base = path.parent().filter(|p| !p.as_os_str().is_empty()).map(Path::to_path_buf);
        if let Some(base) = base {
            for p in [&mut config.paths.replays, &mut config.paths.game_data, &mut config.paths.output] {
                if p.is_relative() {
                    *p = base.join(&*p);
                }
            }
        }
        Ok(config)
    }
}
