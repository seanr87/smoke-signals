//! Battle clock: the in-game countdown shown on the HUD, as `mm:ss` remaining.
//!
//! The countdown is a server property that arrives as whole seconds. It runs
//! about a second ahead of "battle start plus elapsed replay time", so every
//! battle clock in this tool is defined by the HUD value the game reported,
//! not by arithmetic on the replay clock.

use std::fmt;
use std::str::FromStr;

use serde::Serialize;
use wows_replays::types::GameClock;

/// Length of a standard battle. The HUD counts down from this value at battle
/// start.
pub const BATTLE_DURATION_SECONDS: u32 = 20 * 60;

/// Largest value the pre-battle countdown takes. The same HUD property
/// carries it, so an in-battle value must exceed it to be accepted first.
pub const PRE_BATTLE_COUNTDOWN_MAX_SECONDS: i64 = 60;

#[derive(Debug, thiserror::Error)]
#[error("battle clock {text:?} is not of the form mm:ss")]
pub struct BattleClockError {
    pub text: String,
}

/// Seconds remaining on the battle countdown.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct BattleClock(pub u32);

impl BattleClock {
    pub fn remaining_seconds(self) -> u32 {
        self.0
    }

    /// Seconds since battle start, assuming a full-length battle.
    pub fn elapsed_seconds(self) -> u32 {
        BATTLE_DURATION_SECONDS.saturating_sub(self.0)
    }

    /// Battle start plus elapsed. An estimate only; see the module note.
    pub fn estimate_game_clock(self, battle_start: GameClock) -> GameClock {
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

impl Serialize for BattleClock {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serializer.collect_str(self)
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

/// The replay clock at which each HUD countdown value first appeared.
///
/// The countdown property also carries the pre-battle countdown and is stale
/// at the battle-start packet, so the first value recorded must exceed
/// [`PRE_BATTLE_COUNTDOWN_MAX_SECONDS`]; after that only smaller values are
/// recorded.
#[derive(Debug, Clone)]
pub struct BattleClockMap {
    battle_start: GameClock,
    transitions: Vec<(GameClock, i64)>,
}

impl BattleClockMap {
    pub fn new(battle_start: GameClock) -> Self {
        Self { battle_start, transitions: Vec::new() }
    }

    pub fn battle_start(&self) -> GameClock {
        self.battle_start
    }

    /// Record the HUD value reported at `clock`.
    pub fn observe(&mut self, clock: GameClock, hud: Option<i64>) {
        let Some(hud) = hud else { return };
        if clock.seconds() < self.battle_start.seconds() {
            return;
        }
        let accept = match self.transitions.last() {
            None => hud > PRE_BATTLE_COUNTDOWN_MAX_SECONDS,
            Some((_, last)) => hud < *last,
        };
        if accept {
            self.transitions.push((clock, hud));
        }
    }

    pub fn is_empty(&self) -> bool {
        self.transitions.is_empty()
    }

    /// The HUD countdown shown at `clock`, or `None` before the first
    /// in-battle value.
    pub fn at(&self, clock: GameClock) -> Option<BattleClock> {
        let idx = self.transitions.partition_point(|(c, _)| c.seconds() <= clock.seconds());
        let (_, hud) = self.transitions.get(idx.checked_sub(1)?)?;
        u32::try_from(*hud).ok().map(BattleClock)
    }

    /// The replay clock at which the HUD first showed `at` (or the first
    /// smaller value, when that exact second was never reported).
    pub fn to_game_clock(&self, at: BattleClock) -> Option<GameClock> {
        let wanted = i64::from(at.remaining_seconds());
        self.transitions.iter().find(|(_, hud)| *hud <= wanted).map(|(clock, _)| *clock)
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
    fn map_ignores_pre_battle_and_stale_values() {
        let mut map = BattleClockMap::new(GameClock(30.0));
        map.observe(GameClock(10.0), Some(20));
        map.observe(GameClock(30.0), Some(0));
        map.observe(GameClock(30.5), Some(1200));
        map.observe(GameClock(31.4), Some(1199));
        map.observe(GameClock(32.4), Some(1198));
        assert_eq!(map.at(GameClock(30.2)), None);
        assert_eq!(map.at(GameClock(31.0)), Some(BattleClock(1200)));
        assert_eq!(map.at(GameClock(31.4)), Some(BattleClock(1199)));
        assert_eq!(map.at(GameClock(99.0)), Some(BattleClock(1198)));
        assert_eq!(map.to_game_clock(BattleClock(1199)), Some(GameClock(31.4)));
        assert_eq!(map.to_game_clock(BattleClock(1000)), None);
    }

    #[test]
    fn map_accepts_a_recording_that_missed_the_first_second() {
        let mut map = BattleClockMap::new(GameClock(30.0));
        map.observe(GameClock(30.0), Some(0));
        map.observe(GameClock(31.0), Some(1199));
        assert_eq!(map.at(GameClock(31.0)), Some(BattleClock(1199)));
    }
}
