//! Battle clock: the in-game countdown shown on the HUD, as `mm:ss` remaining.

use std::fmt;
use std::str::FromStr;

use wows_replays::types::GameClock;

/// Length of a standard battle. The HUD counts down from this value at battle
/// start; `view.time_left()` is checked against it after seeking.
pub const BATTLE_DURATION_SECONDS: u32 = 20 * 60;

#[derive(Debug, thiserror::Error)]
#[error("battle clock {text:?} is not of the form mm:ss")]
pub struct BattleClockError {
    pub text: String,
}

/// Seconds remaining on the battle countdown.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct BattleClock(pub u32);

impl BattleClock {
    pub fn remaining_seconds(self) -> u32 {
        self.0
    }

    /// Seconds since battle start.
    pub fn elapsed_seconds(self) -> u32 {
        BATTLE_DURATION_SECONDS.saturating_sub(self.0)
    }

    /// The replay clock at which this battle clock is reached.
    pub fn to_game_clock(self, battle_start: GameClock) -> GameClock {
        GameClock(battle_start.seconds() + self.elapsed_seconds() as f32)
    }

    /// `mmss`, for file names.
    pub fn compact(self) -> String {
        format!("{:02}{:02}", self.0 / 60, self.0 % 60)
    }
}

impl fmt::Display for BattleClock {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:02}:{:02}", self.0 / 60, self.0 % 60)
    }
}

impl FromStr for BattleClock {
    type Err = BattleClockError;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        let err = || BattleClockError { text: text.to_string() };
        let (minutes, seconds) = text.split_once(':').ok_or_else(err)?;
        let minutes: u32 = minutes.parse().map_err(|_| err())?;
        let seconds: u32 = seconds.parse().map_err(|_| err())?;
        if seconds >= 60 || minutes * 60 + seconds > BATTLE_DURATION_SECONDS {
            return Err(err());
        }
        Ok(BattleClock(minutes * 60 + seconds))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_and_formats() {
        let clock: BattleClock = "13:46".parse().unwrap();
        assert_eq!(clock, BattleClock(826));
        assert_eq!(clock.to_string(), "13:46");
        assert_eq!(clock.compact(), "1346");
        assert_eq!(clock.elapsed_seconds(), 374);
    }

    #[test]
    fn rejects_malformed() {
        assert!("13:60".parse::<BattleClock>().is_err());
        assert!("21:00".parse::<BattleClock>().is_err());
        assert!("1346".parse::<BattleClock>().is_err());
    }

    #[test]
    fn places_on_replay_clock() {
        let at = BattleClock(826).to_game_clock(GameClock(31.5));
        assert_eq!(at.seconds(), 405.5);
    }
}
