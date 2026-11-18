# CHECK-N1: where every number in FINDINGS-N1.md comes from

All numbers are computed by `n1_c1.py` (C1, ribbons) and `n1_c2.py` (C2), stored in `c1.json` / `c2.json` (merged into `caps.json`), printed in `out-c1.md` / `out-c2.md`, and placed into the findings text by `n1_findings.py`. Nothing is typed by hand except the round 5 reference values marked below. FINDINGS rounds from the one-decimal values stored in the json; the out files round from full precision, so an interval end can differ by 1 in the last digit between the two.

| number or table | script | where (json path; section of the out file) |
|---|---|---|
| enemy took: 155 during, 78 only after, 233 within 60 s of 1074 | n1_c1.py | `c1.three_ways.enemy`; out-c1.md "three ways" |
| we took: 196 / 76 / 272 of 853 | n1_c1.py | `c1.three_ways.we` |
| grace 0 / 10 / 30 / 60 / 120 s rows | n1_c1.py | `c1.grace` (round 5 values read from round5/part-c1/caps.json `enemy_took.grace`) |
| cross-tab snapshot vs timeline; missed 48 of 232 (20.7%); wrong the other way 0 | n1_c1.py | `c1.crosstab.enemy` (old values are `s["enemy_took"]` from r5lib on the same smokes) |
| missed by group: Top 6 21 of 79, Rest 27 of 153 | n1_c1.py | `c1.crosstab.enemy.by_group` |
| we took cross-tab: missed 62 of 271 | n1_c1.py | `c1.crosstab.we` |
| second computation: 0 mismatches; owner at activation differs in 2; frame letters 0 mismatches | n1_c1.py | `c1.checks`; function `raw_took` |
| cap_won cross-check 170 of 171 | n1_c1.py | `c1.cap_won_crosscheck` |
| summary table (9 groups), 60 s and strictly during | n1_c1.py | `c1.overall.enemy_60`, `c1.overall.enemy_during`; each record carries `round5` copied from the round 5 caps.json |
| by map and cap (26 rows) | n1_c1.py | `c1.by_map_cap` |
| we took table | n1_c1.py | `c1.we_took` |
| cap_defended: 486 smokes, kept 334 / 255 / 227; kept tables | n1_c1.py | `c1.cap_defended.grace`, `.kept`, `.kept_strict`, `.last_owner`, `.baseline_ours_kept`. Round 5 counts 374 / 294 / 252 and 86.3% are typed from round 5 FINDINGS.md C1 |
| invaders: tables; median 40 s | n1_c1.py | `c1.invaded.groups`, `.kept`, `.median_invaded_s` |
| ribbons: 442 rows, 341 recorders, 268 smokes covered, 188 smoker or inside, 254 within 2 km | n1_c1.py | `c1.ribbons` (recorder = `self_entity` in each run's damage_spike.json) |
| ribbon tables strict / loose / Top 6 vs Rest / Defended vs kept | n1_c1.py | `c1.ribbons.strict`, `.loose`, `.top_vs_rest`, `.defended_vs_kept` |
| ribbons vs timeline: Captured 91 of 91; Defended 284 of 284 | n1_c1.py | `c1.ribbons.timeline_check`, `.captured_vs_we_took` |
| enemy-took.csv (1,547 rows) | n1_c1.py | written near the end of the C1 part |
| C2 coverage: 166 games in tables, 5 ended before 8:00 | n1_c2.py | `c2.coverage`, `c2.short_games`; game end = last row of score.csv |
| C2 against round 5 game by game: 141 same, 13 differ; 15-minute clock games | n1_c2.py | `c2.vs_round5` (round 5 holders recomputed with r5lib `cap_holders`) |
| C2 pooled tables | n1_c2.py | `c2.pooled.all`, `c2.pooled.rest_vs_rest` (function `c2row`, copied from round 5); `round5` on each record from round 5 caps.json |
| C2 per map rows | n1_c2.py | `c2.maps.<map>.all` / `.rest_vs_rest` |
| C2 reference rows 5:00, 8:00, 10:00, time-weighted | n1_c2.py | `c2.reference`, `c2.time_share` (functions `lead_at`, `time_shares`) |
| score lead of cap leaders 72 of 97; score leader won 131 of 165; cap leader not ahead 5 of 25 | n1_c2.py | `c2.notes` (score from `g.score_at(team, 480)`); round 5 values 66 of 91, 120 of 153, 63 of 154, 53 / 30 / 7 / 46 typed from round 5 FINDINGS.md C2 |
| second count of games with a cap leader: 97 | n1_c2.py | `c2.notes.second_way_cap_leader_games` |
| "Changed from round 5" tables | n1_findings.py | built by comparing each record with its `round5` copy |
| figures n1-enemy-took-snapshot-vs-timeline, n1-caps-8min | n1_c1.py, n1_c2.py | round5b/figures/ |
