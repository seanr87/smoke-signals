# Round 3 analysis: summary

Findings and working figures for review. Not a designed report. Everything is association, not cause.

## Setup

- **Batch:** `output/20261117-122135`, the batch behind the published site (17 Nov 2026): 1,547 smokes, 171 games. Concealed damage includes torpedoes launched from smoke.
- **Top 6 (W-L):** H-SR 20-2, RESIN 17-7, BONKZ 13-8, HTDOG 12-6, KITE 9-5, VRTUS 7-4. Rest = the other 24 clans, including REEEE and MZY. PN is 3-4 with 10 destroyer smokes, too few to read; each module carries a one-line call-out.
- **Team-normalized positions:** the smoking team's spawn is always at the bottom. Hotspot, Loop, Land of Fire, Mountain Range, Sleeping Giant and Sea of Fortune spawn north and south, so north-spawn teams are mirrored north-south. Okinawa spawns north-east and south-west, so its "north" teams are mirrored across the north-west to south-east diagonal. On every map the caps land on caps under that mirror, so the minimap stays a valid background. A cell such as G1 means the cell as seen from the bottom spawn.
- **Maps:** the renderer's minimap images, 10 x 10 grid (numbers west to east, letters north to south), cap circles from each game's cap positions.
- **Destroyer smokes** unless a finding says otherwise: 387 Top 6, 687 Rest. Intervals are 95% from resampling whole clans.
- Modules: [1 ships](round3/module-1/MODULE-1.md), [2 early smokes](round3/module-2/MODULE-2.md), [3 radar](round3/module-3/MODULE-3.md), [4 terrain](round3/module-4/MODULE-4.md), [5 miscellaneous](round3/module-5/MODULE-5.md). Shared code: `round3/common.py`.

## The strongest findings

1. **The early destroyer smoke is cruiser cover, laid short of the cap.** (Module 2) Of 187 smokes in the first 5 minutes by Harugumo, Somers and Gearing, 78% cover a radar cruiser and only 14% reach inside a cap (median 1.8 km short of the edge). The destroyer deals 6% of the concealed damage. With a radar cruiser the smoke returns 16.7k (n 146); with no partner 2.9k (n 13, small n).

2. **Top 6 almost always bring the radar cruiser, and put it inside.** (Module 2) Radar cruiser partner in 93% of early smokes against 70% (+23 points, +10 to +36). Partner inside the smoke, not behind it: 88% against 67% (+9 to +34). Damage is the same (15.2k vs 15.0k); deaths are 0.04 against 0.14 per smoke.

3. **Top 6 run radar from smoke about 2.5 times as often, with the same return per play.** (Module 3) 0.50 against 0.19 plays per team-game (+0.14 to +0.44; 55 and 45 smokes). The cap was taken in 58% of plays for both groups. Three maps hold 72 of the 100 plays: Sleeping Giant, Hotspot, Mountain Range.

4. **Pressing radar from smoke goes with hitting enemy destroyers; the damage and caps go with the cruiser being there.** (Module 3) Radar run against not run, radar ship inside either way: an enemy destroyer was damaged 62% against 36% (+17 to +35 points; n 95 and 290). Cap-contest smokes with a radar ship inside and no radar play still took the cap 74% of the time with 17.0k damage (n 53), against 32% and 5.3k with no radar ship.

5. **Sleeping Giant G1, the own-side corner of cap A, is the best smoke cell in the tournament.** (Module 4) 24.1k concealed damage per smoke over 21 smokes from 10 clans (+8.5k to +20.5k against the rest of the map). It holds in wins and losses and for both groups. It is an opening play (median 2:40) and 91% of the damage comes from the ships behind the smoke.

6. **Centre-cap smoke buys little damage.** (Module 4) Sleeping Giant B 5.4k (n 52), Hotspot F5 3.9k (n 15), Land of Fire F5 4.0k (n 16), each clearly below its map. Some of those cells still win caps (Loop F7 53%, n 15).

7. **Top 6 and Rest smoke different caps on Hotspot, Loop and Land of Fire.** (Module 4) Hotspot: west caps A and B 36% of Top 6 smokes against 13%; D 35% against 52% (-31 to -5 points). Loop: Rest put 50% at cap A, the weakest zone (4.8k, cap won 17%), against 22% (-49 to -7). Land of Fire: Rest 50% at A against 27% (-37 to -9). Top 6 samples are thin on Loop (41 smokes).

8. **Four smoke habits, and the "long DD smoke" label hides two of them.** (Module 1) Ships cluster as flank smoke lines (Somers, Gearing, Harugumo, Delny), cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze), parked cruiser smoke (Svea, Jinan) and moving exhaust. Gdansk, Grozovoi and Shimakaze carry long smoke but use it like a Daring: Gdansk is stationary 41% against Harugumo's 4%, stacked 16% against 55%. Flank lines return 15.8k per smoke against 5.3k for cap sitters (+8.1k to +12.3k) and lose 14.2 ships per 100 smokes against 7.4.

9. **Deaths in smoke follow the score and enemy radar, not distance to the cap.** (Module 5) Smokes laid 50+ points behind cost 23.1 deaths per 100 (n 277) against 6.5 ahead (n 372). Smokes where enemy radar caught a ship cost 25.0 (n 120) against 9.9. Distance band is flat. At level score Top 6 lose 3.7 against 11.4 (-12.0 to -4.4), and the gap is the smoker surviving, not the partners.

10. **Counter-smokes underperform.** (Module 5) 133 destroyer smokes answer an enemy smoke within 45 s. Long-smoke counters return 10.2k against 13.4k otherwise (-6.4k to -0.2k) and out-damage the smoke they answer 38% of the time.

11. **Clan style: H-SR is its own branch; RESIN and BONKZ are nearest.** (Module 5) H-SR: 50% stacked, 18% selfish, first smoke at 2:00, 89% long destroyer smoke, 75% of smoke damage from cruisers. HTDOG and VRTUS win with a different, cruiser-smoke style. PN sits with MZY (weak placement, 14 smokes).

12. **Scouting claims** (the report text is not on disk; these test the three phrases in the request). (Module 4) Sleeping Giant "A first": confirmed for smoke (first smoke goes A-side in 37 of 60 team-games; early A smoke 23.6k against 10.4k later), not for owning the cap. Hotspot "D flank": not special (13.2k, n 109, no different from elsewhere). Land of Fire "B": half confirmed; A matters as much.

## What I would lead a clan-facing report with

**Findings (5):**
- **1 and 2 together, "the opening smoke is for the cruiser":** the clearest play in the data, with a map for every main map and a concrete difference between Top 6 and Rest that a team can copy (bring the radar cruiser, put it inside, stop short of the cap).
- **5, Sleeping Giant G1:** one cell, large effect, holds in wins and losses and across clans. Easy to show and to try.
- **7, which caps to smoke on Hotspot, Loop and Land of Fire:** map-specific and actionable, though it needs the caveat that it shows where good teams go, not that going there wins.
- **3 and 4, radar from smoke:** frequency, not skill per play, separates the groups; and the honest version (the cruiser's presence matters more than the button) is more useful than "use radar".
- **9, survival:** tells players when smoke gets ships killed (behind on score, under enemy radar), which is the most direct "avoid this" in the set.

I would hold back 8 and 11 for a second section: they describe styles well but give a player less to do. I would not lead with 10 or 12: 10 is borderline, 12 rests on my reading of three phrases.

**Figures (5):**
- `round3/module-2/setup-main-maps.png`: early setups on Hotspot, Sleeping Giant and Mountain Range, Top 6 above Rest. Shows the play itself.
- `round3/module-4/sheet-sleeping-giant.png`: the cell sheet where G1 stands out; also the template for the other six map sheets.
- `round3/module-4/usage-top6-vs-rest.png`: where each group smokes on the three maps that differ.
- `round3/module-3/fig2-radar-plays-payoff.png`: where radar plays happen and what they returned.
- `round3/module-5/fig4-survival.png`: where ships die in smoke and what goes with it.

## Not done, or done differently

- **Scouting report:** not on disk. Smoke types were compared with a lens built from the smoke's own type (long DD, short DD, cruiser, exhaust); map notes with the three named phrases only.
- **First cap and lead at 5:00:** the batch has no continuous score or cap timeline. Both are approximated from the state recorded at each smoke. "First cap" is clear in only 87 of 171 games; the 5:00 lead covers 152 games within 60 s. No opening feature showed a clear link to either.
- **Damage on radar-spotted targets:** not in the batch (`radar_spotted_damage` is damage our ships took while lit). Module 3 uses damage on enemy destroyers as the stand-in. Every radar spot is inferred from timing and range.
- **Smoke rate by score state:** no time-in-state to divide by; Module 5 reports outcomes per smoke by state.
- **Per-map Top 6 vs Rest:** only where both had enough smokes. Early setups are side by side on three maps and pooled on four; cell ratings exist on four maps, cap zones on the other three.
- **Battleship as a partner type:** one case; battleships nearly always come with a cruiser.
- **Overlapping chains:** 16 same-team pairs in 171 games; dropped as a finding.
- **Delny:** no map with 8 smokes, so no map panel; effectively H-SR alone (18 of 22).

## Known data cautions

- **`cap_won` and the contested cap:** the "contested cap" is not always the nearest cap (159 of 1,074 destroyer smokes differ), and `cap_won` cannot fire for a cap already owned. Modules 3 and 4 work around both; cap-won rates are also higher early because caps start neutral.
- **Deaths:** 27 of 124 destroyer-smoke deaths happened just after the smoke cleared and are counted as the batch counts them. Deaths track winning strongly; in games won the groups lose the same (4.7 against 4.6 per 100).
- **Duplicate smoke ids:** 3 ids appear in two games each. The shared loader matches detail records by id alone, so up to 3 smokes carry another smoke's path and partners. Too few to move any number here; the loader should match on game as well before reuse.
- **Thin groups:** Top 6 comparisons within a ship or map rest on 2 to 5 clans. High and low cells were picked and scored on the same data, so expect them to shrink; only Sleeping Giant G1 clears its own interval.
- **Mountain Range cap A** is kept as a real 10 km cap. No headline finding depends on it; Module 1 lists the three ship medians it shifts.
