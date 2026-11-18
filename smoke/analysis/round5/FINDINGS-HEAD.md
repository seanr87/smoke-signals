# Round 5 findings: deeper analysis for the Smoke Atlas

Batch: `output/20261117-122135`, the published batch (1,547 smokes, 171 games, 30 clans).
Top 6 = H-SR, RESIN, BONKZ, HTDOG, KITE, VRTUS. Rest = the other 24 clans.
Positions are team-normalized (own spawn at the bottom). Minimum n is 8; 8 to 14 is marked small n.
Intervals are 95%, made by resampling whole clans. "Clear" means the interval excludes zero.
Everything is association, not cause: this says what clans do and what a smoke returned, not what wins.

Each item below has: answer, numbers with n and interval, Top 6 or Shared, clans, what could not be done, and a verdict
(Keep / Lead / Drop). Definitions are in `README.md`. Every number is traced in `CHECK.md`.

## Verdicts at a glance

| Item | Short answer | Top 6 or Shared | Verdict |
|---|---|---|---|
| A1 Cap-contest smokes by cover | For the Rest, a radar cruiser inside goes with taking the cap (76% vs 13% with no cruiser). For the Top 6 it makes no difference (53% vs 48%): they take caps without one. Radar vs non-radar cruiser cannot be told apart (17 smokes). | Mixed | Keep |
| A2 Smoke deaths | Deaths pile up when 50+ behind, under enemy radar, or when a covered ship is seen. Smokes with none of that: 2.9 deaths per 100. | Rate is Top 6 (7.5 vs 13.8); conditions are Shared | Lead |
| A3 Somers vs Gearing deaths | Team, not ship. Top 6: 7.8 vs 9.5 per 100. Rest: 11.8 vs 23.6. | Top 6 vs Rest is the dividing line | Keep |
| A4 Counter-smokes | Flanking does not pay (12 of 132, lower return, no fewer deaths). A radar cruiser inside and laying 11-25 s after the enemy smoke do. | Shared | Keep; Drop flanking |
| B1 Cap sitters | Daring and Z-42 are true cap sitters. Gdansk is not: less often inside, more for a teammate, twice the damage. | Shared | Keep |
| B2 Getaway smokes | Italian cruiser exhaust smoke: smoker died 16.1 per 100 vs 6.3 for ordinary cruiser smoke. Battleships: no different from baseline. | Shared (mostly a Rest tool) | Keep |
| B3 Long smokes | Side lanes and edges, 2 km off the cap, teammates do 92% of the damage. Harugumo also shoots from its own smoke (21.6% of the damage vs 5.9% Somers, 3.1% Gearing). | Shared | Lead |
| B4 Hybrids | Shimakaze has two real modes (parked, or a line of 1 km+), same players doing both. Grozovoi's variety is not there. | Shared | Keep Shimakaze; Drop Grozovoi |
| C1 Cap defence | `cap_defended` does not mean the smoke defended a cap (fires on 31% of smokes, cap usually far away). New field "enemy took the nearest cap" works. Ribbons are not in the batch. | Rest lose the nearby cap more often (15.2% vs 8.5%) | Keep |
| C2 Cap holder at 8:00 | No cap clearly adds beyond team strength. Land of Fire middle caps are the only lead. | Shared | Keep as a caution |
| C3 Danger zones | Only one sturdy zone: destroyers smoking inside cap C on Hotspot (a Rest habit). Three others are n 8 and in line with chance. | Shared | Lead for Hotspot C; Drop the rest |
| C4 Spots per map | 21 spots on six maps (none on Okinawa). A blind search labels none of them Top 6. One solid high-paying cell: Sleeping Giant G1. | All Shared | Keep as a catalogue |
| C5 Map questions | 21 sub-questions answered; see the part. Leads: Hotspot west side after the opening, Hotspot opener with a radar cruiser inside. Dropped: Sleeping Giant cap B as defence, Loop Daring-after-radar, Mountain Range radar at B as defence. | Per question | Per question |
| D1 Clan scores | All 30 clans scored (6 flagged for under 7 games). | Clear gaps: radar cruiser inside, damage, deaths, exhaust ships | Keep |
| D2 Styles | Two scales, not one: who the smoke is for, and how much smoke. Four soft-edged styles. All Top 6 are "plenty of smoke"; they split 4 and 2 on the other scale. | Scale 1 Shared; scale 2 Top 6 | Lead |
| D3 Profiles | One value, percentile and range per dimension per clan, ready for gauges. | n/a | Keep |

## Top 6 or Shared: how to read it

Two parts looked at places on the map and they answer differently on purpose.

- **Part C4 searched blind:** any place where a kind of smoke concentrates for everyone, then asked whether the Top 6 use it
  clearly more. Result: 21 spots, none Top 6. At a wider circle (2.5 to 3.5 km) two become Top 6 zones: Loop cap sitters at
  cap B and Land of Fire Svea at F5.
- **Part C5 re-tested the places Sean named**, most of them carried over from round 4, where they were picked because they
  showed a gap, and each is defined for one ship or habit. Nine of those come out "Top 6" on the interval rule.
- **How to use both:** the nine are real descriptions of where those Top 6 ships went, but they were chosen for the gap, so
  expect them to shrink on new data (round 4's placebo passed 2.5 of 6 by chance). The safest Top 6 markings are the two that
  show up in both parts: Loop cap sitters at B and Land of Fire Svea at F5. Sea of Fortune Svea (15 of 16 smokes) and Mountain
  Range parked cruiser smoke (12 of 12) are Top 6 by count but rest on one or two clans each. In `spots.json` these records
  carry a `selection_note`.

## Things that changed from earlier rounds

- **"Radar cruiser inside goes with the cap being taken"** (round 4) holds for the Rest only. Top 6 take the cap about half
  the time with or without one.
- **"Somers loses fewer ships than Gearing"** (round 3) is a team effect, not a ship effect.
- **`cap_defended`** should not be read as "the smoke defended a cap" anywhere. Use "enemy took the nearest cap" for smokes
  within 2 km of a cap.
- **Enemy radar on ships in smoke** was undercounted by the field used in rounds 3 and 4 (120 destroyer smokes strict, 297
  on the broader reading). Both readings are given in A2 and B3; the conclusions hold on both.
- **Grozovoi as a hybrid** (round 4) is not supported; Shimakaze is.
- **Round 4's two Top 6 styles** are reproduced, and now sit inside a two-scale map of all clans.

## Could not be done (short list; detail in each item and in README.md)

- Defence and capture ribbons: only the recording player's ribbons are in a replay and the batch does not export them.
  Counting them needs a code change and a batch rerun.
- Ship health is not in the batch; "lost a third of its health" uses an estimate per ship type.
- Friendly radar used outside smoke is not exported, so the Loop "Daring after radar" test is a thin proxy.
- Spotting cannot be attributed; "nearest ally to the target" is the stand-in.
- Leaving the smoke, death position and where a smoke's ships were aiming are not recorded.
- No continuous cap timeline: cap owners are known only at smoke moments, which misses about 15% of real flips.
