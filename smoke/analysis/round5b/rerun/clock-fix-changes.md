# What the 15-minute-clock fix changed in the Round 5 script outputs

Two games (kots19na_7971 game 1 on Hotspot, KSE against PFANS; kots19na_7976 game 1 on Loop, KSE against VRTUS) ran on a 15-minute clock.
Rounds 3 to 5 read elapsed time as 20:00 minus the HUD clock, so their 17 smokes (11 by destroyers) were placed 300 seconds late.
Each block lists the lines that differ: Round 5 first, Round 5b second. Lines that only list equal counts in another order are counted, not shown.
| output | lines changed | lines differing only in tie order |
|---|---|---|
| part-a/out-a1.json | 0 | 0 |
| part-a/out-a1.txt | 3 | 0 |
| part-a/out-a2.json | 660 | 0 |
| part-a/out-a2.txt | 107 | 0 |
| part-a/out-a3.json | 0 | 0 |
| part-a/out-a3.txt | 0 | 0 |
| part-a/out-a4.json | 0 | 0 |
| part-a/out-a4.txt | 0 | 0 |
| part-a/topics.json | 660 | 0 |
| part-b/out.txt | 0 | 0 |
| part-b/ships.json | 0 | 0 |
| part-c1/caps.json | 411 | 0 |
| part-c1/danger-zones.json | 0 | 0 |
| part-c1/enemy-took.csv | 0 | 0 |
| part-c1/out-caps.md | 63 | 0 |
| part-c1/out-danger.md | 0 | 0 |
| part-c4/checks.json | 0 | 0 |
| part-c4/generated.md | 5 | 0 |
| part-c4/out.txt | 6 | 0 |
| part-c4/spots.json | 14 | 0 |
| part-c4/wide.txt | 3 | 0 |
| part-c5/map-questions.json | 109 | 0 |
| part-c5/part-hs.json | 69 | 0 |
| part-c5/part-lp-daring.json | 0 | 0 |
| part-c5/part-lp.json | 58 | 0 |
| part-c5/part-rest.json | 0 | 0 |
| part-c5/part-sg.json | 0 | 0 |
| part-c5/spots.json | 18 | 0 |
| part-d/clan_styles.json | 375 | 1 |
| part-d/d1_scores.json | 122 | 0 |
| part-d/d1_tables.md | 13 | 9 |
| part-d/d2_structure.json | 1286 | 0 |
| part-d/d3_tables.md | 6 | 0 |
| part-c5/out-sg.txt (script output) | 0 | 0 |
| part-c5/out-hs.txt (script output) | 24 | 0 |
| part-c5/out-lp.txt (script output) | 12 | 0 |
| part-c5/out-lp-daring.txt (script output) | 1 | 0 |
| part-c5/out-rest.txt (script output) | 0 | 0 |
| part-c5/out-tables.txt (script output) | 0 | 0 |
| part-d/d2_output.txt (script output) | 132 | 0 |
| part-b/show.txt (script output) | 0 | 0 |


## part-a/out-a1.txt: 3 lines changed

```
round 5 : radar cruiser inside early % 33.7 inside cap % 53.8 median el 416.0 radar_cap set % 98.1 own {'ours': 53, 'neutral': 30, 'theirs': 21} cruisers inside {'Des Moines': 48, 'Brisbane': 19, 'Minotaur': 13, 'Salem': 8, 'Worcester': 7, 'Svea': 6} smoker ships {'Somers': 34, 'Gearing': 33, 'Harugumo': 19, 
round 5b: radar cruiser inside early % 34.6 inside cap % 53.8 median el 409.5 radar_cap set % 98.1 own {'ours': 53, 'neutral': 30, 'theirs': 21} cruisers inside {'Des Moines': 48, 'Brisbane': 19, 'Minotaur': 13, 'Salem': 8, 'Worcester': 7, 'Svea': 6} smoker ships {'Somers': 34, 'Gearing': 33, 'Harugumo': 19, 
```
```
round 5 : no cruiser early % 24.1 inside cap % 73.3 median el 464 radar_cap set % 14.1 own {'theirs': 59, 'neutral': 49, 'ours': 83} cruisers inside {} smoker ships {'Daring': 84, 'Gdańsk': 32, 'Z-42': 23, 'Shimakaze': 11, 'Somers': 11}
round 5b: no cruiser early % 24.6 inside cap % 73.3 median el 463 radar_cap set % 14.1 own {'theirs': 59, 'neutral': 49, 'ours': 83} cruisers inside {} smoker ships {'Daring': 84, 'Gdańsk': 32, 'Z-42': 23, 'Shimakaze': 11, 'Somers': 11}
```
```
round 5 : other early % 41.8 inside cap % 69.6 median el 340 radar_cap set % 8.9 own {'ours': 35, 'neutral': 29, 'theirs': 15} cruisers inside {'Napoli': 1, 'Colbert': 1} smoker ships {'Daring': 21, 'Somers': 17, 'Gearing': 12, 'Shimakaze': 8, 'Gdańsk': 7}
round 5b: other early % 43.0 inside cap % 69.6 median el 333 radar_cap set % 8.9 own {'ours': 35, 'neutral': 29, 'theirs': 15} cruisers inside {'Napoli': 1, 'Colbert': 1} smoker ships {'Daring': 21, 'Somers': 17, 'Gearing': 12, 'Shimakaze': 8, 'Gdańsk': 7}
```

## part-a/out-a2.json: 660 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-a/out-a2.txt: 107 lines changed

```
round 5 : | 0-5 min | 302 (102/200) | 23 | 7.6 [4.6 to 11.4 *] | 2.9 | 10.0 | -12.7 to -1.7 * | 3.6 | 5.2 (213) |  |
round 5b: | 0-5 min | 306 (103/203) | 23 | 7.5 [4.5 to 11.1 *] | 2.9 | 9.9 | -12.8 to -1.8 * | 3.6 | 5.1 (215) |  |
```
```
round 5 : | 5-10 min | 495 (180/315) | 62 | 12.5 [9.1 to 16.5 *] | 8.3 | 14.9 | -13.8 to +0.2 | 7.5 | 8.1 (270) |  |
round 5b: | 5-10 min | 495 (179/316) | 62 | 12.5 [9.1 to 16.5 *] | 8.4 | 14.9 | -13.7 to +0.3 | 7.5 | 8.2 (269) |  |
```
```
round 5 : | 10-15 min | 248 (96/152) | 35 | 14.1 [9.6 to 18.9 *] | 9.4 | 17.1 | -17.3 to +0.7 | 7.7 | 14.4 (97) |  |
round 5b: | 10-15 min | 247 (98/149) | 35 | 14.2 [9.9 to 19.5 *] | 9.2 | 17.4 | -17.0 to +0.4 | 7.7 | 14.3 (98) |  |
```
```
round 5 : | 15-20 min | 29 (9/20) | 4 | 13.8 [3.7 to 25.0 *] | 22.2 | 10.0 | -5.6 to +27.3 | 6.9 | too few (7) |  |
round 5b: | 15-20 min | 26 (7/19) | 4 | 15.4 [3.7 to 29.6 *] | too few | 10.5 | - | 7.7 | too few (5) |  |
```
```
round 5 : | ahead 50+ | 372 (167/205) | 24 | 6.5 [4.4 to 9.2 *] | 5.4 | 7.3 | -6.5 to +3.0 | 3.8 | 4.8 (187) |  |
round 5b: | ahead 50+ | 372 (167/205) | 24 | 6.5 [4.4 to 9.0 *] | 5.4 | 7.3 | -6.3 to +2.8 | 3.8 | 4.8 (187) |  |
```
```
round 5 : | level | 425 (161/264) | 36 | 8.5 [6.2 to 11.3 *] | 3.7 | 11.4 | -11.8 to -4.3 * | 3.8 | 6.9 (288) |  |
round 5b: | level | 425 (161/264) | 36 | 8.5 [6.3 to 11.4 *] | 3.7 | 11.4 | -12.1 to -4.5 * | 3.8 | 6.9 (288) |  |
```
```
round 5 : | behind 50+ | 277 (59/218) | 64 | 23.1 [17.2 to 30.3 *] | 23.7 | 22.9 | -13.9 to +13.5 | 14.1 | 17.0 (112) |  |
round 5b: | behind 50+ | 277 (59/218) | 64 | 23.1 [17.2 to 30.3 *] | 23.7 | 22.9 | -14.1 to +12.8 | 14.1 | 17.0 (112) |  |
```
```
round 5 : | 0-5 min, ahead 50+ | 29 (13/16) | 1 | 3.4 [0.0 to 13.3] | 0.0 | 6.2 | -23.1 to +0.0 | 3.4 | 0.0 (19) |  |
round 5b: | 0-5 min, ahead 50+ | 30 (14/16) | 1 | 3.3 [0.0 to 12.5] | 0.0 | 6.2 | -21.4 to +0.0 | 3.3 | 0.0 (20) |  |
```
```
round 5 : | 0-5 min, level | 249 (87/162) | 20 | 8.0 [5.0 to 11.9 *] | 3.4 | 10.5 | -14.2 to -1.4 * | 3.6 | 6.0 (183) |  |
round 5b: | 0-5 min, level | 252 (87/165) | 20 | 7.9 [5.0 to 11.9 *] | 3.4 | 10.3 | -13.1 to -1.8 * | 3.6 | 6.0 (184) |  |
```
```
round 5 : | 0-5 min, behind 50+ | 24 (2/22) | 2 | 8.3 [0.0 to 20.0] | too few | 9.1 | - | 4.2 | 0.0 (11) |  |
round 5b: | 0-5 min, behind 50+ | 24 (2/22) | 2 | 8.3 [0.0 to 19.2] | too few | 9.1 | - | 4.2 | 0.0 (11) |  |
```
```
round 5 : | 5-10 min, ahead 50+ | 183 (81/102) | 10 | 5.5 [2.7 to 9.8 *] | 4.9 | 5.9 | -8.4 to +4.0 | 4.4 | 2.0 (102) |  |
round 5b: | 5-10 min, ahead 50+ | 184 (80/104) | 10 | 5.4 [2.7 to 9.0 *] | 5.0 | 5.8 | -7.6 to +4.9 | 4.3 | 2.0 (102) |  |
```
```
round 5 : | 5-10 min, level | 157 (66/91) | 13 | 8.3 [4.2 to 13.7 *] | 3.0 | 12.1 | -16.8 to -1.3 * | 3.8 | 7.4 (95) |  |
round 5b: | 5-10 min, level | 154 (66/88) | 13 | 8.4 [4.6 to 14.2 *] | 3.0 | 12.5 | -18.0 to -2.0 * | 3.9 | 7.4 (94) |  |
```
```
round 5 : | 5-10 min, behind 50+ | 155 (33/122) | 39 | 25.2 [17.4 to 34.0 *] | 27.3 | 24.6 | -16.4 to +16.3 | 14.8 | 17.8 (73) |  |
round 5b: | 5-10 min, behind 50+ | 157 (33/124) | 39 | 24.8 [17.3 to 34.3 *] | 27.3 | 24.2 | -15.8 to +17.0 | 14.6 | 17.8 (73) |  |
```
```
round 5 : | 10-15 min, ahead 50+ | 141 (66/75) | 12 | 8.5 [4.5 to 13.2 *] | 6.1 | 10.7 | -12.7 to +3.3 | 3.5 | 9.7 (62) |  |
round 5b: | 10-15 min, ahead 50+ | 141 (68/73) | 12 | 8.5 [4.0 to 13.1 *] | 5.9 | 11.0 | -12.6 to +2.6 | 3.5 | 9.5 (63) |  |
```
```
round 5 : | 10-15 min, level | 18 (7/11) | 3 | 16.7 [0.0 to 30.0] | too few | 18.2 | - | 5.6 | 22.2 (9) |  |
round 5b: | 10-15 min, level | 18 (7/11) | 3 | 16.7 [0.0 to 29.2] | too few | 18.2 | - | 5.6 | 22.2 (9) |  |
```
```
round 5 : | 10-15 min, behind 50+ | 89 (23/66) | 20 | 22.5 [13.6 to 32.1 *] | 17.4 | 24.2 | -26.7 to +8.7 | 14.6 | 23.1 (26) |  |
round 5b: | 10-15 min, behind 50+ | 88 (23/65) | 20 | 22.7 [14.5 to 32.6 *] | 17.4 | 24.6 | -25.0 to +9.2 | 14.8 | 23.1 (26) |  |
```
```
round 5 : | 15-20 min, ahead 50+ | 19 (7/12) | 1 | 5.3 [0.0 to 15.0] | too few | 0.0 | - | 0.0 | too few (4) |  |
round 5b: | 15-20 min, ahead 50+ | 17 (5/12) | 1 | 5.9 [0.0 to 20.0] | too few | 0.0 | - | 0.0 | too few (2) |  |
```
```
round 5 : | 15-20 min, behind 50+ | 9 (1/8) | 3 | 33.3 [11.1 to 55.6 *] | too few | 25.0 | - | 22.2 | too few (2) | small n |
round 5b: | 15-20 min, behind 50+ | 8 (1/7) | 3 | 37.5 [12.5 to 62.5 *] | too few | too few | - | 25.0 | too few (2) | small n |
```
```
round 5 : | enemy radar reached the smoke | 120 (44/76) | 30 | 25.0 [16.5 to 37.5 *] | 13.6 | 31.6 | -35.2 to +3.9 | 13.3 | 16.4 (73) |  |
round 5b: | enemy radar reached the smoke | 120 (44/76) | 30 | 25.0 [16.9 to 35.6 *] | 13.6 | 31.6 | -35.0 to +3.9 | 13.3 | 16.4 (73) |  |
```
```
round 5 : | no enemy radar | 954 (343/611) | 94 | 9.9 [7.5 to 13.0 *] | 6.7 | 11.6 | -9.9 to -0.7 * | 5.6 | 7.0 (514) |  |
round 5b: | no enemy radar | 954 (343/611) | 94 | 9.9 [7.4 to 12.9 *] | 6.7 | 11.6 | -9.6 to -0.8 * | 5.6 | 7.0 (514) |  |
```
```
round 5 : | radar from an enemy cruiser | 101 (34/67) | 25 | 24.8 [15.5 to 37.0 *] | 14.7 | 29.9 | -34.7 to +14.6 | 13.9 | 14.3 (63) |  |
round 5b: | radar from an enemy cruiser | 101 (34/67) | 25 | 24.8 [15.9 to 37.1 *] | 14.7 | 29.9 | -33.3 to +12.7 | 13.9 | 14.3 (63) |  |
```
```
round 5 : | radar reached, Sleeping Giant | 33 (13/20) | 10 | 30.3 [14.7 to 50.0 *] | 0.0 | 50.0 | -70.4 to -27.8 * | 18.2 | 15.0 (20) |  |
round 5b: | radar reached, Sleeping Giant | 33 (13/20) | 10 | 30.3 [14.3 to 51.6 *] | 0.0 | 50.0 | -70.6 to -27.8 * | 18.2 | 15.0 (20) |  |
```
```
round 5 : | radar reached, Hotspot | 18 (4/14) | 3 | 16.7 [0.0 to 31.2] | too few | 14.3 | - | 5.6 | 22.2 (9) |  |
round 5b: | radar reached, Hotspot | 18 (4/14) | 3 | 16.7 [0.0 to 29.4] | too few | 14.3 | - | 5.6 | 22.2 (9) |  |
```
```
round 5 : | radar reached, Mountain Range | 14 (8/6) | 1 | 7.1 [0.0 to 30.0] | 12.5 | too few | - | 0.0 | 8.3 (12) | small n |
round 5b: | radar reached, Mountain Range | 14 (8/6) | 1 | 7.1 [0.0 to 33.3] | 12.5 | too few | - | 0.0 | 8.3 (12) | small n |
```
```
round 5 : | radar reached, Land of Fire | 16 (8/8) | 3 | 18.8 [0.0 to 44.4] | 0.0 | 37.5 | -62.5 to -12.5 * | 0.0 | 30.0 (10) |  |
round 5b: | radar reached, Land of Fire | 16 (8/8) | 3 | 18.8 [3.4 to 44.4 *] | 0.0 | 37.5 | -62.5 to -12.5 * | 0.0 | 30.0 (10) |  |
```
```
round 5 : | radar reached, Okinawa | 10 (3/7) | 5 | 50.0 [11.1 to 92.3 *] | too few | too few | - | 30.0 | too few (6) | small n |
round 5b: | radar reached, Okinawa | 10 (3/7) | 5 | 50.0 [0.0 to 91.7] | too few | too few | - | 30.0 | too few (6) | small n |
```
```
round 5 : | radar reached, 0-5 min | 29 (7/22) | 7 | 24.1 [7.1 to 42.9 *] | too few | 31.8 | - | 13.8 | 13.6 (22) |  |
round 5b: | radar reached, 0-5 min | 29 (7/22) | 7 | 24.1 [7.4 to 43.3 *] | too few | 31.8 | - | 13.8 | 13.6 (22) |  |
```
```
round 5 : | radar reached, 5-10 min | 62 (24/38) | 13 | 21.0 [11.9 to 32.0 *] | 12.5 | 26.3 | -32.1 to +5.5 | 9.7 | 15.8 (38) |  |
round 5b: | radar reached, 5-10 min | 62 (24/38) | 13 | 21.0 [12.3 to 32.1 *] | 12.5 | 26.3 | -30.9 to +8.5 | 9.7 | 15.8 (38) |  |
```
```
round 5 : | radar reached, 10-15 min | 25 (12/13) | 7 | 28.0 [9.5 to 52.2 *] | 16.7 | 38.5 | -61.4 to +25.0 | 16.0 | 25.0 (12) |  |
round 5b: | radar reached, 10-15 min | 25 (12/13) | 7 | 28.0 [10.7 to 54.5 *] | 16.7 | 38.5 | -58.3 to +25.0 | 16.0 | 25.0 (12) |  |
```
```
round 5 : | radar reached, ahead 50+ | 36 (17/19) | 4 | 11.1 [2.5 to 23.3 *] | 11.8 | 10.5 | -19.7 to +25.0 | 8.3 | 6.2 (16) |  |
round 5b: | radar reached, ahead 50+ | 36 (17/19) | 4 | 11.1 [2.4 to 23.3 *] | 11.8 | 10.5 | -21.3 to +23.5 | 8.3 | 6.2 (16) |  |
```
```
round 5 : | radar reached, level | 48 (18/30) | 10 | 20.8 [9.3 to 37.2 *] | 5.6 | 30.0 | -52.2 to -5.3 * | 8.3 | 17.6 (34) |  |
round 5b: | radar reached, level | 48 (18/30) | 10 | 20.8 [8.2 to 37.8 *] | 5.6 | 30.0 | -50.0 to -5.5 * | 8.3 | 17.6 (34) |  |
```
```
round 5 : | radar reached, behind 50+ | 36 (9/27) | 16 | 44.4 [28.9 to 64.9 *] | 33.3 | 48.1 | -46.6 to +14.0 | 25.0 | 21.7 (23) |  |
round 5b: | radar reached, behind 50+ | 36 (9/27) | 16 | 44.4 [28.9 to 63.9 *] | 33.3 | 48.1 | -50.0 to +14.1 | 25.0 | 21.7 (23) |  |
```
```
round 5 : | radar reached, a cruiser sheltering | 67 (24/43) | 17 | 25.4 [14.8 to 39.7 *] | 8.3 | 34.9 | -43.6 to -7.0 * | 7.5 | 15.1 (73) |  |
round 5b: | radar reached, a cruiser sheltering | 67 (24/43) | 17 | 25.4 [14.8 to 40.0 *] | 8.3 | 34.9 | -43.8 to -8.6 * | 7.5 | 15.1 (73) |  |
```
```
round 5 : | radar reached, no cruiser sheltering | 53 (20/33) | 13 | 24.5 [14.5 to 37.2 *] | 20.0 | 27.3 | -31.3 to +14.0 | 20.8 | too few (0) |  |
round 5b: | radar reached, no cruiser sheltering | 53 (20/33) | 13 | 24.5 [14.5 to 37.8 *] | 20.0 | 27.3 | -28.4 to +13.1 | 20.8 | too few (0) |  |
```
```
round 5 : radar reached vs not, difference: {'a': 25.0, 'n_a': 120, 'b': 9.9, 'n_b': 954, 'diff': 15.1, 'lo': 6.2, 'hi': 26.6, 'clear': True}
round 5b: radar reached vs not, difference: {'a': 25.0, 'n_a': 120, 'b': 9.9, 'n_b': 954, 'diff': 15.1, 'lo': 6.5, 'hi': 26.5, 'clear': True}
```
```
round 5 : share of smokes radar reached: T6 vs Rest {'top6': 11.4, 'n_top6': 387, 'rest': 11.1, 'n_rest': 687, 'diff': 0.3, 'lo': -4.2, 'hi': 4.7, 'clear': False}
round 5b: share of smokes radar reached: T6 vs Rest {'top6': 11.4, 'n_top6': 387, 'rest': 11.1, 'n_rest': 687, 'diff': 0.3, 'lo': -4.3, 'hi': 4.8, 'clear': False}
```
```
round 5 : | Sleeping Giant cap D, radar reached | 8 (4/4) | 3 | 37.5 [0.0 to 87.5] | too few | too few | - | 12.5 | too few (7) | small n |
round 5b: | Sleeping Giant cap D, radar reached | 8 (4/4) | 3 | 37.5 [0.0 to 77.8] | too few | too few | - | 12.5 | too few (7) | small n |
```
```
round 5 : | Mountain Range cap B, radar reached | 9 (7/2) | 1 | 11.1 [0.0 to 25.0] | too few | too few | - | 0.0 | too few (6) | small n |
round 5b: | Mountain Range cap B, radar reached | 9 (7/2) | 1 | 11.1 [0.0 to 33.3] | too few | too few | - | 0.0 | too few (6) | small n |
```
```
round 5 : | Land of Fire cap B, radar reached | 11 (7/4) | 1 | 9.1 [0.0 to 25.0] | too few | too few | - | 0.0 | too few (5) | small n |
round 5b: | Land of Fire cap B, radar reached | 11 (7/4) | 1 | 9.1 [0.0 to 27.3] | too few | too few | - | 0.0 | too few (5) | small n |
```
```
round 5 : share of smokes with the broad radar flag:  {'value': 27.7, 'n': 1074, 'lo': 24.1, 'hi': 31.3} {'top6': 28.7, 'n_top6': 387, 'rest': 27.1, 'n_rest': 687, 'diff': 1.6, 'lo': -7.4, 'hi': 8.7, 'clear': False} | strict radar_on_us and broad both 119 strict only 1 broad only 178
round 5b: share of smokes with the broad radar flag:  {'value': 27.7, 'n': 1074, 'lo': 24.0, 'hi': 31.2} {'top6': 28.7, 'n_top6': 387, 'rest': 27.1, 'n_rest': 687, 'diff': 1.6, 'lo': -6.8, 'hi': 8.9, 'clear': False} | strict radar_on_us and broad both 119 strict only 1 broad only 178
```
```
round 5 : | radar flag on a covered ship (broad) | 297 (111/186) | 83 | 27.9 [22.2 to 35.4 *] | 17.1 | 34.4 | -25.9 to -7.6 * | 15.2 | 17.1 (199) |  |
round 5b: | radar flag on a covered ship (broad) | 297 (111/186) | 83 | 27.9 [22.5 to 35.0 *] | 17.1 | 34.4 | -25.8 to -7.8 * | 15.2 | 17.1 (199) |  |
```
```
round 5 : | no radar flag (broad) | 777 (276/501) | 41 | 5.3 [3.3 to 7.9 *] | 3.6 | 6.2 | -6.8 to +1.1 | 3.1 | 3.6 (388) |  |
round 5b: | no radar flag (broad) | 777 (276/501) | 41 | 5.3 [3.3 to 7.9 *] | 3.6 | 6.2 | -7.0 to +1.0 | 3.1 | 3.6 (388) |  |
```
```
round 5 : | radar flag (broad), Sleeping Giant | 79 (35/44) | 20 | 25.3 [16.1 to 37.0 *] | 8.6 | 38.6 | -44.6 to -16.6 * | 15.2 | 14.3 (49) |  |
round 5b: | radar flag (broad), Sleeping Giant | 79 (35/44) | 20 | 25.3 [16.2 to 37.7 *] | 8.6 | 38.6 | -46.2 to -17.4 * | 15.2 | 14.3 (49) |  |
```
```
round 5 : | radar flag (broad), Hotspot | 53 (18/35) | 14 | 26.4 [17.0 to 36.0 *] | 33.3 | 22.9 | -13.5 to +30.5 | 13.2 | 18.9 (37) |  |
round 5b: | radar flag (broad), Hotspot | 53 (18/35) | 14 | 26.4 [16.3 to 36.1 *] | 33.3 | 22.9 | -10.1 to +29.7 | 13.2 | 18.9 (37) |  |
```
```
round 5 : | radar flag (broad), Loop | 29 (6/23) | 11 | 37.9 [18.5 to 60.0 *] | too few | 30.4 | - | 20.7 | 26.7 (15) |  |
round 5b: | radar flag (broad), Loop | 29 (6/23) | 11 | 37.9 [19.4 to 61.9 *] | too few | 30.4 | - | 20.7 | 26.7 (15) |  |
```
```
round 5 : | radar flag (broad), Mountain Range | 31 (16/15) | 5 | 16.1 [2.7 to 33.3 *] | 18.8 | 13.3 | -25.0 to +40.0 | 6.5 | 13.0 (23) |  |
round 5b: | radar flag (broad), Mountain Range | 31 (16/15) | 5 | 16.1 [0.0 to 33.3] | 18.8 | 13.3 | -25.0 to +40.0 | 6.5 | 13.0 (23) |  |
```
```
round 5 : | radar flag (broad), Land of Fire | 35 (12/23) | 9 | 25.7 [10.0 to 46.2 *] | 0.0 | 39.1 | -68.8 to -22.6 * | 8.6 | 25.0 (24) |  |
round 5b: | radar flag (broad), Land of Fire | 35 (12/23) | 9 | 25.7 [9.1 to 47.2 *] | 0.0 | 39.1 | -70.0 to -22.2 * | 8.6 | 25.0 (24) |  |
```
```
round 5 : | radar flag (broad), Sea of Fortune | 41 (17/24) | 9 | 22.0 [9.4 to 40.5 *] | 5.9 | 33.3 | -52.0 to -5.4 * | 14.6 | 7.1 (28) |  |
round 5b: | radar flag (broad), Sea of Fortune | 41 (17/24) | 9 | 22.0 [9.4 to 39.3 *] | 5.9 | 33.3 | -55.3 to -6.6 * | 14.6 | 7.1 (28) |  |
```
```
round 5 : | radar flag (broad), Okinawa | 29 (7/22) | 15 | 51.7 [26.9 to 75.0 *] | too few | 59.1 | - | 31.0 | 21.7 (23) |  |
round 5b: | radar flag (broad), Okinawa | 29 (7/22) | 15 | 51.7 [24.1 to 76.7 *] | too few | 59.1 | - | 31.0 | 21.7 (23) |  |
```
```
round 5 : | radar flag (broad), ahead 50+ | 86 (42/44) | 14 | 16.3 [9.6 to 25.8 *] | 11.9 | 20.5 | -23.3 to +7.6 | 9.3 | 11.3 (53) |  |
round 5b: | radar flag (broad), ahead 50+ | 86 (42/44) | 14 | 16.3 [9.2 to 25.3 *] | 11.9 | 20.5 | -23.0 to +7.5 | 9.3 | 11.3 (53) |  |
```
```
round 5 : | radar flag (broad), level | 125 (48/77) | 29 | 23.2 [16.7 to 31.4 *] | 10.4 | 31.2 | -32.8 to -11.2 * | 12.0 | 14.1 (99) |  |
round 5b: | radar flag (broad), level | 125 (48/77) | 29 | 23.2 [16.7 to 31.1 *] | 10.4 | 31.2 | -32.2 to -11.2 * | 12.0 | 14.1 (99) |  |
```
```
round 5 : | radar flag (broad), behind 50+ | 86 (21/65) | 40 | 46.5 [35.0 to 57.9 *] | 42.9 | 47.7 | -28.5 to +20.2 | 25.6 | 29.8 (47) |  |
round 5b: | radar flag (broad), behind 50+ | 86 (21/65) | 40 | 46.5 [34.7 to 58.1 *] | 42.9 | 47.7 | -29.3 to +19.6 | 25.6 | 29.8 (47) |  |
```
```
round 5 : | radar flag (broad), 0-5 min | 83 (24/59) | 18 | 21.7 [12.3 to 33.8 *] | 8.3 | 27.1 | -35.3 to +9.7 | 9.6 | 13.6 (66) |  |
round 5b: | radar flag (broad), 0-5 min | 83 (24/59) | 18 | 21.7 [12.2 to 32.9 *] | 8.3 | 27.1 | -35.7 to +7.0 | 9.6 | 13.6 (66) |  |
```
```
round 5 : | radar flag (broad), 5-10 min | 139 (56/83) | 36 | 25.9 [17.4 to 35.7 *] | 17.9 | 31.3 | -29.8 to +3.9 | 14.4 | 15.6 (96) |  |
round 5b: | radar flag (broad), 5-10 min | 139 (56/83) | 36 | 25.9 [17.2 to 34.8 *] | 17.9 | 31.3 | -31.2 to +3.1 | 14.4 | 15.6 (96) |  |
```
```
round 5 : | radar flag (broad), 10-15 min | 70 (30/40) | 26 | 37.1 [25.8 to 49.1 *] | 20.0 | 50.0 | -45.9 to -11.7 * | 21.4 | 27.8 (36) |  |
round 5b: | radar flag (broad), 10-15 min | 70 (30/40) | 26 | 37.1 [25.0 to 49.3 *] | 20.0 | 50.0 | -46.0 to -11.6 * | 21.4 | 27.8 (36) |  |
```
```
round 5 : broad radar vs not, difference: {'a': 27.9, 'n_a': 297, 'b': 5.3, 'n_b': 777, 'diff': 22.7, 'lo': 16.6, 'hi': 29.6, 'clear': True}
round 5b: broad radar vs not, difference: {'a': 27.9, 'n_a': 297, 'b': 5.3, 'n_b': 777, 'diff': 22.7, 'lo': 16.3, 'hi': 29.8, 'clear': True}
```
```
round 5 : | smoke emission cut short | 50 / 1024 | 36.0 | 10.4 | +10.3 to +41.0 * | 30.0 / 5.3 (+11.3 to +39.8 *) | 27.3 (11) / 7.8 (576) (-3.1 to +47.5) | 11.1 (9) | 41.5 (41) |
round 5b: | smoke emission cut short | 50 / 1024 | 36.0 | 10.4 | +10.0 to +40.8 * | 30.0 / 5.3 (+9.7 to +39.2 *) | 27.3 (11) / 7.8 (576) (-2.7 to +53.8) | 11.1 (9) | 41.5 (41) |
```
```
round 5 : | enemy hydro reached a covered ship | 17 / 1057 | 35.3 | 11.2 | +2.9 to +43.2 * | 17.6 / 6.2 (-5.8 to +29.1) | 20.0 (10) / 8.0 (577) (-8.3 to +36.0) | too few (6) | 36.4 (11) |
round 5b: | enemy hydro reached a covered ship | 17 / 1057 | 35.3 | 11.2 | +2.1 to +45.6 * | 17.6 / 6.2 (-5.3 to +29.5) | 20.0 (10) / 8.0 (577) (-8.2 to +34.8) | too few (6) | 36.4 (11) |
```
```
round 5 : | a covered ship carried the radar flag while concealed (broad measure) | 297 / 777 | 27.9 | 5.3 | +17.0 to +29.1 * | 15.2 / 3.1 (+6.8 to +18.3 *) | 17.1 (199) / 3.6 (388) (+8.2 to +19.7 *) | 17.1 (111) | 34.4 (186) |
round 5b: | a covered ship carried the radar flag while concealed (broad measure) | 297 / 777 | 27.9 | 5.3 | +16.7 to +30.3 * | 15.2 / 3.1 (+7.0 to +18.2 *) | 17.1 (199) / 3.6 (388) (+8.1 to +19.5 *) | 17.1 (111) | 34.4 (186) |
```
```
round 5 : | team outnumbered at activation | 198 / 876 | 27.3 | 8.0 | +11.7 to +27.5 * | 16.7 / 4.1 (+6.5 to +20.7 *) | 24.3 (74) / 5.8 (513) (+9.1 to +27.3 *) | 26.7 (45) | 27.5 (153) |
round 5b: | team outnumbered at activation | 198 / 876 | 27.3 | 8.0 | +11.8 to +27.5 * | 16.7 / 4.1 (+6.5 to +20.2 *) | 24.3 (74) / 5.8 (513) (+9.4 to +26.7 *) | 26.7 (45) | 27.5 (153) |
```
... and 47 more lines.

## part-a/topics.json: 660 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-c1/caps.json: 411 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-c1/out-caps.md: 63 lines changed

```
round 5 : Independent re-computation from the raw json (own code, json clocks instead of csv clocks): 1547 of 1547 smokes agree on enemy_took, we_took and the snapshot count; mismatches: 0.
round 5b: Independent re-computation from the raw json (own code, json clocks instead of csv clocks): 1545 of 1547 smokes agree on enemy_took, we_took and the snapshot count; mismatches: 2.
```
```
round 5 : | 0 s | 103 | 970 | 474 | 9.6% | 119 | 734 | 14.0% |
round 5b: | 0 s | 103 | 969 | 475 | 9.6% | 119 | 733 | 14.0% |
```
```
round 5 : | 60 s | 184 | 889 | 474 | 17.1% | 209 | 644 | 24.5% |
round 5b: | 60 s | 184 | 888 | 475 | 17.2% | 209 | 643 | 24.5% |
```
```
round 5 : | 120 s | 233 | 840 | 474 | 21.7% | 269 | 584 | 31.5% |
round 5b: | 120 s | 233 | 839 | 475 | 21.7% | 269 | 583 | 31.6% |
```
```
round 5 : | Loop | 23 | 18 | 2 | 3 |
round 5b: | Loop | 23 | 19 | 2 | 2 |
```
```
round 5 : | all | 171 | 154 | 5 | 12 |
round 5b: | all | 171 | 155 | 5 | 11 |
```
```
round 5 : Distance of the snapshot used from 8:00: median 11 s, max 59 s. Covered games where both clans are Rest: 76; games with a Top 6 clan: 78.
round 5b: Distance of the snapshot used from 8:00: median 11 s, max 59 s. Covered games where both clans are Rest: 76; games with a Top 6 clan: 79.
```
```
round 5 : | B (own side) | 49 | 26 (53%, 47 to 60) | 36% (n 11) | +17 (-20 to +48) | 24.9 | +2 pts (-3 to +8) | 24.8; +2 pts (-1 to +7) |
round 5b: | B (own side) | 51 | 27 (53%, 47 to 59) | 33% (n 9) | +20 (-24 to +56) | 25.9 | +2 pts (-3 to +8) | 25.8; +2 pts (-1 to +7) |
```
```
round 5 : | B (own side) | 27 | 16 (59%, 53 to 68) | 14% (n 7) | +45 (+20 to +65 *) | 13.7 | +8 pts (+2 to +18 *) | 14.3; +6 pts (+1 to +14 *) |
round 5b: | B (own side) | 29 | 17 (59%, 53 to 68) | 0% (n 5) | +59 (+53 to +68 *) | 14.7 | +8 pts (+2 to +16 *) | 15.3; +6 pts (+1 to +13 *) |
```
```
round 5 : ## Loop  (18 games covered, 10 Rest-vs-Rest)
round 5b: ## Loop  (19 games covered, 10 Rest-vs-Rest)
```
```
round 5 : All covered games (18 games):
round 5b: All covered games (19 games):
```
```
round 5 : | A (middle) | 16 | 6 (38%, 14 to 62) | 60% (n 20) | -22 (-63 to +22) | 7.5 | -10 pts (-31 to +14) | 7.1; -7 pts (-29 to +16) |
round 5b: | A (middle) | 17 | 7 (41%, 19 to 67) | 57% (n 21) | -16 (-54 to +27) | 8.2 | -7 pts (-28 to +14) | 7.9; -5 pts (-26 to +16) |
```
```
round 5 : | B (middle) | 18 | 11 (61%, 39 to 83) | 39% (n 18) | +22 (-22 to +67) | 9.5 | +8 pts (-12 to +28) | 9.4; +9 pts (-12 to +28) |
round 5b: | B (middle) | 19 | 12 (63%, 42 to 84) | 37% (n 19) | +26 (-16 to +68) | 10.2 | +10 pts (-9 to +28) | 10.2; +9 pts (-12 to +28) |
```
```
round 5 : | C (middle) | 14 (small n) | 6 (43%, 17 to 70) | 55% (n 22) | -12 (-54 to +34) | 8.3 | -16 pts (-38 to +8) | 8.6; -19 pts (-42 to +3) |
round 5b: | C (middle) | 14 (small n) | 6 (43%, 17 to 69) | 54% (n 24) | -11 (-53 to +32) | 8.3 | -16 pts (-39 to +6) | 8.6; -19 pts (-41 to +5) |
```
```
round 5 : | holds more caps than the enemy | 13 (small n) | 6 (46%, 20 to 73) | 54% (n 13) | -8 (-60 to +50) | 7.6 | -12 pts (-37 to +13) | 7.6; -13 pts (-38 to +13) |
round 5b: | holds more caps than the enemy | 14 (small n) | 7 (50%, 24 to 75) | 50% (n 14) | +0 (-53 to +54) | 8.3 | -9 pts (-34 to +15) | 8.5; -11 pts (-36 to +13) |
```
```
round 5 : | A (middle) | 9 (small n) | 4 (44%, 11 to 78) | 55% (n 11) | -10 (-62 to +51) | 4.2 | -3 pts (-38 to +33) | 4.2; -2 pts (-39 to +36) |
round 5b: | A (middle) | 9 (small n) | 4 (44%, 11 to 78) | 55% (n 11) | -10 (-71 to +51) | 4.2 | -3 pts (-38 to +31) | 4.2; -2 pts (-40 to +36) |
```
```
round 5 : | B (middle) | 10 (small n) | 6 (60%, 30 to 90) | 40% (n 10) | +20 (-40 to +80) | 5.1 | +9 pts (-23 to +40) | 4.8; +12 pts (-22 to +42) |
round 5b: | B (middle) | 10 (small n) | 6 (60%, 30 to 90) | 40% (n 10) | +20 (-40 to +80) | 5.1 | +9 pts (-25 to +40) | 4.8; +12 pts (-22 to +43) |
```
```
round 5 : | C (middle) | 9 (small n) | 1 (11%, 0 to 33) | 82% (n 11) | -71 (-100 to -30 *) | 4.6 | -40 pts (-57 to -15 *) | 4.4; -38 pts (-62 to -7 *) |
round 5b: | C (middle) | 9 (small n) | 1 (11%, 0 to 33) | 82% (n 11) | -71 (-100 to -30 *) | 4.6 | -40 pts (-57 to -13 *) | 4.4; -38 pts (-62 to -6 *) |
```
```
round 5 : | holds more caps than the enemy | 8 (small n) | 2 (25%, 0 to 57) | 75% (n 8) | -50 (-100 to +14) | 4.1 | -26 pts (-55 to +13) | 4.0; -25 pts (-60 to +14) |
round 5b: | holds more caps than the enemy | 8 (small n) | 2 (25%, 0 to 60) | 75% (n 8) | -50 (-100 to +14) | 4.1 | -26 pts (-56 to +15) | 4.0; -25 pts (-59 to +15) |
```
```
round 5 : | A (middle) | 12 (small n) | 6 (50%, 22 to 79) | 50% (n 26) | +0 (-41 to +41) | 6.2 | -2 pts (-29 to +21) | 5.8; +2 pts (-18 to +24) |
round 5b: | A (middle) | 12 (small n) | 6 (50%, 22 to 80) | 50% (n 26) | +0 (-41 to +41) | 6.2 | -2 pts (-25 to +22) | 5.8; +2 pts (-20 to +25) |
```
```
round 5 : | B (middle) | 17 | 11 (65%, 41 to 88) | 38% (n 21) | +27 (-11 to +69) | 9.2 | +11 pts (-9 to +30) | 9.4; +10 pts (-8 to +29) |
round 5b: | B (middle) | 17 | 11 (65%, 41 to 88) | 38% (n 21) | +27 (-16 to +65) | 9.2 | +11 pts (-10 to +31) | 9.4; +10 pts (-8 to +28) |
```
```
round 5 : | C (middle) | 19 | 10 (53%, 32 to 74) | 47% (n 19) | +5 (-37 to +47) | 9.8 | +1 pts (-19 to +20) | 10.7; -4 pts (-22 to +14) |
round 5b: | C (middle) | 19 | 10 (53%, 32 to 74) | 47% (n 19) | +5 (-47 to +47) | 9.8 | +1 pts (-18 to +21) | 10.7; -4 pts (-21 to +14) |
```
```
round 5 : | holds more caps than the enemy | 12 (small n) | 9 (75%, 50 to 100) | 25% (n 12) | +50 (+0 to +100) | 7.2 | +15 pts (-6 to +35) | 7.7; +10 pts (-9 to +30) |
round 5b: | holds more caps than the enemy | 12 (small n) | 9 (75%, 46 to 100) | 25% (n 12) | +50 (+0 to +100) | 7.2 | +15 pts (-7 to +36) | 7.7; +10 pts (-8 to +29) |
```
```
round 5 : | C (middle) | 8 (small n) | 4 (50%, 12 to 88) | 50% (n 8) | +0 (-75 to +75) | 3.3 | +9 pts (-21 to +37) | 3.2; +10 pts (-15 to +36) |
round 5b: | C (middle) | 8 (small n) | 4 (50%, 12 to 88) | 50% (n 8) | +0 (-75 to +75) | 3.3 | +9 pts (-18 to +39) | 3.2; +10 pts (-15 to +35) |
```
```
round 5 : | A (own side) | 22 | 12 (55%, 41 to 70) | 40% (n 10) | +15 (-33 to +54) | 11.5 | +2 pts (-11 to +16) | 11.6; +2 pts (-11 to +16) |
round 5b: | A (own side) | 22 | 12 (55%, 40 to 68) | 40% (n 10) | +15 (-29 to +58) | 11.5 | +2 pts (-11 to +17) | 11.6; +2 pts (-11 to +14) |
```
```
round 5 : | B (enemy side) | 9 (small n) | 5 (56%, 22 to 88) | 48% (n 23) | +8 (-41 to +54) | 4.6 | +5 pts (-26 to +39) | 4.7; +4 pts (-26 to +38) |
round 5b: | B (enemy side) | 9 (small n) | 5 (56%, 17 to 88) | 48% (n 23) | +8 (-39 to +54) | 4.6 | +5 pts (-27 to +39) | 4.7; +4 pts (-27 to +35) |
```
```
round 5 : | C (middle) | 15 | 6 (40%, 17 to 67) | 59% (n 17) | -19 (-62 to +31) | 6.5 | -3 pts (-26 to +20) | 6.0; +0 pts (-22 to +22) |
round 5b: | C (middle) | 15 | 6 (40%, 15 to 67) | 59% (n 17) | -19 (-62 to +25) | 6.5 | -3 pts (-27 to +20) | 6.0; +0 pts (-22 to +24) |
```
```
round 5 : | D (middle) | 15 | 6 (40%, 13 to 62) | 59% (n 17) | -19 (-63 to +31) | 8.1 | -14 pts (-37 to +9) | 8.0; -14 pts (-33 to +7) |
round 5b: | D (middle) | 15 | 6 (40%, 14 to 67) | 59% (n 17) | -19 (-63 to +31) | 8.1 | -14 pts (-35 to +8) | 8.0; -14 pts (-34 to +8) |
```
```
round 5 : | holds more caps than the enemy | 8 (small n) | 3 (38%, 0 to 71) | 62% (n 8) | -25 (-100 to +43) | 3.9 | -11 pts (-38 to +17) | 3.6; -8 pts (-35 to +20) |
round 5b: | holds more caps than the enemy | 8 (small n) | 3 (38%, 0 to 71) | 62% (n 8) | -25 (-100 to +50) | 3.9 | -11 pts (-38 to +17) | 3.6; -8 pts (-35 to +19) |
```
```
round 5 : | A (own side) | 16 | 8 (50%, 33 to 65) | 50% (n 6) | +0 (-58 to +59) | 7.6 | +3 pts (-13 to +20) | 7.6; +3 pts (-15 to +20) |
round 5b: | A (own side) | 16 | 8 (50%, 33 to 67) | 50% (n 6) | +0 (-52 to +55) | 7.6 | +3 pts (-14 to +19) | 7.6; +3 pts (-12 to +19) |
```
```
round 5 : | C (middle) | 10 (small n) | 6 (60%, 30 to 90) | 42% (n 12) | +18 (-45 to +73) | 4.6 | +14 pts (-15 to +41) | 4.3; +17 pts (-12 to +42) |
round 5b: | C (middle) | 10 (small n) | 6 (60%, 30 to 90) | 42% (n 12) | +18 (-37 to +73) | 4.6 | +14 pts (-14 to +42) | 4.3; +17 pts (-8 to +43) |
```
```
round 5 : | D (middle) | 10 (small n) | 4 (40%, 10 to 70) | 58% (n 12) | -18 (-73 to +37) | 5.5 | -15 pts (-42 to +15) | 5.5; -15 pts (-41 to +13) |
round 5b: | D (middle) | 10 (small n) | 4 (40%, 10 to 70) | 58% (n 12) | -18 (-73 to +45) | 5.5 | -15 pts (-46 to +15) | 5.5; -15 pts (-42 to +12) |
```
```
round 5 : | B (own side) | 32 | 16 (50%, 42 to 58) | 50% (n 6) | +0 (-51 to +54) | 16.3 | -1 pts (-8 to +6) | 16.5; -1 pts (-8 to +3) |
round 5b: | B (own side) | 32 | 16 (50%, 43 to 58) | 50% (n 6) | +0 (-51 to +54) | 16.3 | -1 pts (-8 to +6) | 16.5; -1 pts (-8 to +3) |
```
```
round 5 : | C (middle) | 16 | 6 (38%, 13 to 62) | 59% (n 22) | -22 (-59 to +17) | 7.9 | -12 pts (-29 to +8) | 7.7; -11 pts (-26 to +7) |
round 5b: | C (middle) | 16 | 6 (38%, 17 to 60) | 59% (n 22) | -22 (-59 to +21) | 7.9 | -12 pts (-30 to +8) | 7.7; -11 pts (-27 to +7) |
```
```
round 5 : | D (middle) | 17 | 12 (71%, 47 to 89) | 33% (n 21) | +37 (-5 to +74) | 9.5 | +15 pts (-5 to +31) | 10.2; +10 pts (-5 to +23) |
round 5b: | D (middle) | 17 | 12 (71%, 47 to 89) | 33% (n 21) | +37 (-5 to +76) | 9.5 | +15 pts (-3 to +32) | 10.2; +10 pts (-5 to +24) |
```
```
round 5 : | holds more caps than the enemy | 15 | 8 (53%, 27 to 78) | 47% (n 15) | +7 (-47 to +57) | 8.1 | -0 pts (-24 to +20) | 8.6; -4 pts (-20 to +11) |
round 5b: | holds more caps than the enemy | 15 | 8 (53%, 27 to 78) | 47% (n 15) | +7 (-47 to +56) | 8.1 | -0 pts (-22 to +19) | 8.6; -4 pts (-21 to +12) |
```
```
round 5 : | B (own side) | 15 | 7 (47%, 36 to 57) | 67% (n 3) | -20 (-64 to +56) | 7.7 | -5 pts (-18 to +3) | 7.7; -4 pts (-14 to +3) |
round 5b: | B (own side) | 15 | 7 (47%, 36 to 57) | 67% (n 3) | -20 (-64 to +56) | 7.7 | -5 pts (-18 to +3) | 7.7; -4 pts (-16 to +3) |
```
```
round 5 : | C (middle) | 8 (small n) | 3 (38%, 0 to 75) | 60% (n 10) | -22 (-82 to +35) | 4.0 | -12 pts (-38 to +17) | 3.8; -10 pts (-32 to +18) |
round 5b: | C (middle) | 8 (small n) | 3 (38%, 0 to 75) | 60% (n 10) | -22 (-78 to +45) | 4.0 | -12 pts (-37 to +13) | 3.8; -10 pts (-31 to +16) |
```
```
round 5 : | D (middle) | 9 (small n) | 7 (78%, 44 to 100) | 22% (n 9) | +56 (+11 to +100 *) | 5.6 | +16 pts (-10 to +35) | 5.8; +13 pts (-11 to +31) |
round 5b: | D (middle) | 9 (small n) | 7 (78%, 44 to 100) | 22% (n 9) | +56 (-11 to +100) | 5.6 | +16 pts (-6 to +34) | 5.8; +13 pts (-11 to +31) |
```
```
round 5 : | A (middle) | 29 | 17 (59%, 41 to 76) | 41% (n 29) | +17 (-24 to +52) | 15.4 | +6 pts (-9 to +20) | 15.7; +4 pts (-10 to +18) |
round 5b: | A (middle) | 29 | 17 (59%, 41 to 76) | 41% (n 29) | +17 (-17 to +52) | 15.4 | +6 pts (-11 to +21) | 15.7; +4 pts (-9 to +17) |
```
```
round 5 : | B (middle) | 16 | 10 (62%, 35 to 86) | 45% (n 42) | +17 (-17 to +49) | 8.3 | +10 pts (-9 to +31) | 9.1; +5 pts (-12 to +24) |
round 5b: | B (middle) | 16 | 10 (62%, 36 to 85) | 45% (n 42) | +17 (-15 to +49) | 8.3 | +10 pts (-10 to +31) | 9.1; +5 pts (-13 to +25) |
```
```
round 5 : | C (enemy side) | 11 (small n) | 6 (55%, 27 to 85) | 49% (n 47) | +6 (-33 to +44) | 5.8 | +2 pts (-25 to +28) | 6.7; -7 pts (-32 to +17) |
round 5b: | C (enemy side) | 11 (small n) | 6 (55%, 23 to 85) | 49% (n 47) | +6 (-32 to +42) | 5.8 | +2 pts (-24 to +27) | 6.7; -7 pts (-30 to +16) |
```
```
round 5 : | D (own side) | 47 | 24 (51%, 45 to 58) | 45% (n 11) | +6 (-32 to +44) | 23.8 | +1 pts (-5 to +6) | 24.7; -2 pts (-8 to +4) |
round 5b: | D (own side) | 47 | 24 (51%, 44 to 58) | 45% (n 11) | +6 (-29 to +42) | 23.8 | +1 pts (-5 to +6) | 24.7; -2 pts (-8 to +4) |
```
```
round 5 : | holds more caps than the enemy | 17 | 12 (71%, 47 to 90) | 29% (n 17) | +41 (+0 to +83) | 10.1 | +11 pts (-10 to +30) | 11.9; +1 pts (-16 to +17) |
round 5b: | holds more caps than the enemy | 17 | 12 (71%, 47 to 93) | 29% (n 17) | +41 (-8 to +83) | 10.1 | +11 pts (-10 to +30) | 11.9; +1 pts (-16 to +17) |
```
```
round 5 : | A (middle) | 10 (small n) | 5 (50%, 20 to 80) | 50% (n 10) | +0 (-60 to +60) | 4.8 | +2 pts (-27 to +31) | 4.5; +5 pts (-20 to +31) |
round 5b: | A (middle) | 10 (small n) | 5 (50%, 20 to 80) | 50% (n 10) | +0 (-60 to +60) | 4.8 | +2 pts (-27 to +31) | 4.5; +5 pts (-20 to +32) |
```
```
round 5 : | D (own side) | 16 | 8 (50%, 38 to 64) | 50% (n 4) | +0 (-62 to +59) | 8.4 | -2 pts (-16 to +10) | 8.5; -3 pts (-18 to +8) |
round 5b: | D (own side) | 16 | 8 (50%, 38 to 64) | 50% (n 4) | +0 (-62 to +59) | 8.4 | -2 pts (-16 to +11) | 8.5; -3 pts (-18 to +8) |
```
```
round 5 : All covered games (154 games):
round 5b: All covered games (155 games):
```
```
round 5 : | holds its own-side cap (maps that have one) | 184 | 94 (51%, 48 to 55) | 48% (n 124) | +3 (-7 to +12) | 92.9 | +1 pts (-3 to +4) | 94.2; -0 pts (-3 to +3) |
round 5b: | holds its own-side cap (maps that have one) | 186 | 95 (51%, 47 to 54) | 48% (n 124) | +3 (-6 to +12) | 93.9 | +1 pts (-3 to +4) | 95.2; -0 pts (-3 to +3) |
```
```
round 5 : | holds the enemy-side cap (maps that have one) | 47 | 25 (53%, 39 to 68) | 49% (n 261) | +4 (-14 to +19) | 24.0 | +2 pts (-10 to +15) | 25.3; -1 pts (-13 to +10) |
round 5b: | holds the enemy-side cap (maps that have one) | 47 | 25 (53%, 38 to 66) | 49% (n 263) | +4 (-13 to +22) | 24.0 | +2 pts (-12 to +16) | 25.3; -1 pts (-12 to +10) |
```
```
round 5 : | holds at least one middle cap | 231 | 131 (57%, 53 to 61) | 30% (n 77) | +27 (+13 to +40 *) | 120.3 | +5 pts (+1 to +8 *) | 124.3; +3 pts (+0 to +6 *) |
round 5b: | holds at least one middle cap | 232 | 132 (57%, 53 to 61) | 29% (n 78) | +27 (+14 to +40 *) | 121.0 | +5 pts (+2 to +8 *) | 125.1; +3 pts (+1 to +6 *) |
```
```
round 5 : | holds every middle cap | 43 | 27 (63%, 47 to 77) | 48% (n 265) | +15 (-1 to +33) | 24.3 | +6 pts (-5 to +18) | 25.1; +4 pts (-5 to +16) |
round 5b: | holds every middle cap | 43 | 27 (63%, 47 to 77) | 48% (n 267) | +15 (-1 to +31) | 24.3 | +6 pts (-5 to +19) | 25.1; +4 pts (-5 to +14) |
```
```
round 5 : | holds more caps than the enemy | 91 | 60 (66%, 57 to 75) | 34% (n 91) | +32 (+11 to +49 *) | 52.3 | +9 pts (-0 to +17) | 56.8; +4 pts (-4 to +11) |
round 5b: | holds more caps than the enemy | 92 | 61 (66%, 57 to 76) | 34% (n 92) | +33 (+12 to +52 *) | 53.0 | +9 pts (+1 to +18 *) | 57.6; +4 pts (-4 to +12) |
```
```
round 5 : | holds 2+ more caps than the enemy | 42 | 31 (74%, 60 to 87) | 46% (n 266) | +28 (+11 to +43 *) | 24.7 | +15 pts (+4 to +26 *) | 27.3; +9 pts (-0 to +17) |
round 5b: | holds 2+ more caps than the enemy | 43 | 32 (74%, 61 to 87) | 46% (n 267) | +28 (+13 to +43 *) | 25.4 | +15 pts (+4 to +26 *) | 28.2; +9 pts (-0 to +18) |
```
```
round 5 : | holds its own-side cap (maps that have one) | 88 | 46 (52%, 47 to 58) | 47% (n 64) | +5 (-8 to +20) | 44.0 | +2 pts (-3 to +7) | 44.6; +2 pts (-3 to +6) |
round 5b: | holds its own-side cap (maps that have one) | 90 | 47 (52%, 46 to 58) | 47% (n 62) | +5 (-8 to +18) | 45.0 | +2 pts (-3 to +7) | 45.6; +2 pts (-3 to +6) |
```
```
round 5 : | holds the enemy-side cap (maps that have one) | 26 | 15 (58%, 39 to 77) | 48% (n 126) | +9 (-14 to +31) | 13.0 | +8 pts (-9 to +26) | 13.6; +5 pts (-10 to +21) |
round 5b: | holds the enemy-side cap (maps that have one) | 26 | 15 (58%, 40 to 76) | 48% (n 126) | +9 (-14 to +30) | 13.0 | +8 pts (-10 to +26) | 13.6; +5 pts (-10 to +22) |
```
```
round 5 : | holds at least one middle cap | 119 | 64 (54%, 49 to 59) | 36% (n 33) | +17 (-6 to +38) | 61.6 | +2 pts (-2 to +6) | 62.6; +1 pts (-2 to +5) |
round 5b: | holds at least one middle cap | 119 | 64 (54%, 49 to 59) | 36% (n 33) | +17 (-4 to +38) | 61.6 | +2 pts (-2 to +6) | 62.6; +1 pts (-2 to +5) |
```
```
round 5 : | holds every middle cap | 22 | 14 (64%, 43 to 83) | 48% (n 130) | +16 (-8 to +41) | 13.0 | +5 pts (-12 to +23) | 13.4; +3 pts (-12 to +17) |
round 5b: | holds every middle cap | 22 | 14 (64%, 44 to 85) | 48% (n 130) | +16 (-8 to +38) | 13.0 | +5 pts (-13 to +22) | 13.4; +3 pts (-13 to +17) |
```
```
round 5 : | holds more caps than the enemy | 41 | 23 (56%, 41 to 71) | 44% (n 41) | +12 (-18 to +43) | 22.5 | +1 pts (-12 to +15) | 23.8; -2 pts (-15 to +11) |
round 5b: | holds more caps than the enemy | 41 | 23 (56%, 40 to 71) | 44% (n 41) | +12 (-19 to +41) | 22.5 | +1 pts (-12 to +16) | 23.8; -2 pts (-14 to +11) |
```
```
round 5 : | holds 2+ more caps than the enemy | 20 | 16 (80%, 61 to 95) | 45% (n 132) | +35 (+11 to +53 *) | 11.6 | +22 pts (+7 to +36 *) | 12.7; +17 pts (+3 to +29 *) |
round 5b: | holds 2+ more caps than the enemy | 20 | 16 (80%, 60 to 95) | 45% (n 132) | +35 (+13 to +54 *) | 11.6 | +22 pts (+6 to +36 *) | 12.7; +17 pts (+3 to +29 *) |
```
```
round 5 : Games level on caps at 8:00: 63 of 154. Caps held at 8:00 per team: {0: 10, 1: 107, 2: 152, 3: 37, 4: 2}
round 5b: Games level on caps at 8:00: 63 of 155. Caps held at 8:00 per team: {0: 11, 1: 105, 2: 155, 3: 37, 4: 2}
```
... and 3 more lines.

## part-c4/generated.md: 5 lines changed

```
round 5 : | hs-sit-1 | selfish: cap sitter | on the rim of cap C, own side (F6/F5/G5) | Shared: 6% vs 23% (gap -17, -30 to -5); Rest use it more | 1 / 17 | Top 6: H-SR 1 / Rest: KSC 5, EPOXY 5, PFANS 2, BTLST 1, UYSC 1, HFANS 1, INCA 1, MACHX 1 | Top 6: inside Petropavlovsk 1 / Rest: screened Petropavlovsk 1,
round 5b: | hs-sit-1 | selfish: cap sitter | on the rim of cap C, own side (F6/F5/G5) | Shared: 6% vs 23% (gap -17, -30 to -5); Rest use it more | 1 / 17 | Top 6: H-SR 1 / Rest: KSC 5, EPOXY 5, PFANS 2, BTLST 1, UYSC 1, HFANS 1, INCA 1, MACHX 1 | Top 6: inside Petropavlovsk 1 / Rest: screened Petropavlovsk 1,
```
```
round 5 : | hs-early-1 | early cruiser | 2.4 km outside cap D, own side, east edge of the map (G10/F10) | Shared: 36% vs 29% (gap +7, -15 to +33) | 8 / 9 | Top 6: H-SR 2, BONKZ 2, RESIN 2, HTDOG 1, KITE 1 / Rest: HFANS 2, BTLST 1, PN 1, -BN- 1, BONKY 1, REEEE 1, PFANS 1, KSC 1 | Top 6: inside Brisbane 2, Des 
round 5b: | hs-early-1 | early cruiser | 2.4 km outside cap D, own side, east edge of the map (G10/F10) | Shared: 36% vs 28% (gap +8, -13 to +34) | 8 / 9 | Top 6: H-SR 2, BONKZ 2, RESIN 2, HTDOG 1, KITE 1 / Rest: HFANS 2, BTLST 1, PN 1, -BN- 1, BONKY 1, REEEE 1, PFANS 1, KSC 1 | Top 6: inside Brisbane 2, Des 
```
```
round 5 : | hs-early-2 | early cruiser | 1.8 km outside cap C, own side (G6/G5) | Shared: 18% vs 16% (gap +2, -16 to +19) | 4 / 5 | Top 6: BONKZ 2, H-SR 1, RESIN 1 / Rest: KSC 2, OGF 1, -BN- 1, MZY 1 | Top 6: inside Brisbane 2, Utrecht 1, Minotaur 1 +1 more; screened Worcester 1 / Rest: inside Minotaur 2, Des
round 5b: | hs-early-2 | early cruiser | 1.8 km outside cap C, own side (G6/G5) | Shared: 18% vs 16% (gap +3, -15 to +20) | 4 / 5 | Top 6: BONKZ 2, H-SR 1, RESIN 1 / Rest: KSC 2, OGF 1, -BN- 1, MZY 1 | Top 6: inside Brisbane 2, Utrecht 1, Minotaur 1 +1 more; screened Worcester 1 / Rest: inside Minotaur 2, Des
```
```
round 5 : Figure: `figures/c4-loop.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 15 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 20 such smokes on this map); no high-paying cell (of 21 cells or pairs with 8+ destroyer smokes, n
round 5b: Figure: `figures/c4-loop.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 15 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 21 such smokes on this map); no high-paying cell (of 21 cells or pairs with 8+ destroyer smokes, n
```
```
round 5 : | loop-sit-2 | selfish: cap sitter | inside cap B, own side (F7) | Shared: 30% vs 9% (gap +21, -3 to +50) | 7 / 6 | Top 6: RESIN 3, HTDOG 2, VRTUS 1, H-SR 1 / Rest: REEEE 5, SCCC2 1 | Top 6: inside Minotaur 1; screened Petropavlovsk 2, Moskva 1, Prins van Oranje 1 / Rest: none | 2.3k | 0 | 9:43 | sm
round 5b: | loop-sit-2 | selfish: cap sitter | inside cap B, own side (F7) | Shared: 30% vs 9% (gap +21, -3 to +50) | 7 / 6 | Top 6: RESIN 3, HTDOG 2, VRTUS 1, H-SR 1 / Rest: REEEE 5, SCCC2 1 | Top 6: inside Minotaur 1; screened Petropavlovsk 2, Moskva 1, Prins van Oranje 1 / Rest: none | 2.3k | 0 | 9:26 | sm
```

## part-c4/out.txt: 6 lines changed

```
round 5 : Top 6: H-SR 1 | Rest: KSC 5, EPOXY 5, PFANS 2, BTLST 1, UYSC 1, HFANS 1, INCA 1, MACHX 1 | dmg 2104 deaths/100 0.0 time 5:16
round 5b: Top 6: H-SR 1 | Rest: KSC 5, EPOXY 5, PFANS 2, BTLST 1, UYSC 1, HFANS 1, INCA 1, MACHX 1 | dmg 2104 deaths/100 0.0 time 4:56
```
```
round 5 : Hotspot | early_cruiser: pool 53 (Top 6 22, Rest 31), spots 2
round 5b: Hotspot | early_cruiser: pool 54 (Top 6 22, Rest 32), spots 2
```
```
round 5 : hs-early-1 2.4 km outside cap D, own side, east edge of the map ['G10', 'F10'] r 1.95 km n 17 top/rest 8/9 share 36.36363636363637 vs 29.032258064516128 ci -14.666666666666664 33.00492610837439 -> shared
round 5b: hs-early-1 2.4 km outside cap D, own side, east edge of the map ['G10', 'F10'] r 1.95 km n 17 top/rest 8/9 share 36.36363636363637 vs 28.125 ci -12.807881773399014 33.957219251336895 -> shared
```
```
round 5 : hs-early-2 1.8 km outside cap C, own side ['G6', 'G5'] r 2.05 km n 9 top/rest 4/5 share 18.181818181818183 vs 16.129032258064516 ci -15.909090909090908 19.278996865203762 -> shared
round 5b: hs-early-2 1.8 km outside cap C, own side ['G6', 'G5'] r 2.05 km n 9 top/rest 4/5 share 18.181818181818183 vs 15.625 ci -15.15151515151515 19.743589743589745 -> shared
```
```
round 5 : Top 6: RESIN 3, HTDOG 2, VRTUS 1, H-SR 1 | Rest: REEEE 5, SCCC2 1 | dmg 2286 deaths/100 0.0 time 9:43
round 5b: Top 6: RESIN 3, HTDOG 2, VRTUS 1, H-SR 1 | Rest: REEEE 5, SCCC2 1 | dmg 2286 deaths/100 0.0 time 9:26
```
```
round 5 : Loop | early_cruiser: pool 20 (Top 6 6, Rest 14), spots 0
round 5b: Loop | early_cruiser: pool 21 (Top 6 7, Rest 14), spots 0
```

## part-c4/spots.json: 14 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-c4/wide.txt: 3 lines changed

```
round 5 : Hotspot | early_cruiser | 1.8 km outside cap D, own side, east edge of the map ['G10', 'F10'] r 2.8 km | n 25 (Top 6 12, Rest 13) | share 55% vs 42% | interval -13 to +33 | shared  | Top 6: H-SR 5, BONKZ 3, RESIN 2, HTDOG 1, KITE 1 | Rest: 5D 2, HFANS 2, BTLST 1, MZY 1, PN 1, -BN- 1, BONKY 1, REEEE 
round 5b: Hotspot | early_cruiser | 1.8 km outside cap D, own side, east edge of the map ['G10', 'F10'] r 2.8 km | n 25 (Top 6 12, Rest 13) | share 55% vs 41% | interval -11 to +34 | shared  | Top 6: H-SR 5, BONKZ 3, RESIN 2, HTDOG 1, KITE 1 | Rest: 5D 2, HFANS 2, BTLST 1, MZY 1, PN 1, -BN- 1, BONKY 1, REEEE 
```
```
round 5 : Hotspot | early_cruiser | 1.5 km outside cap C, own side ['G6', 'G5', 'F6'] r 2.6 km | n 12 (Top 6 4, Rest 8) | share 18% vs 26% | interval -29 to +11 | shared  | Top 6: BONKZ 2, H-SR 1, RESIN 1 | Rest: -BN- 2, KSC 2, OGF 1, UYSC 1, EPOXY 1, MZY 1 | dmg 6,025
round 5b: Hotspot | early_cruiser | 1.5 km outside cap C, own side ['G6', 'G5', 'F6'] r 2.6 km | n 12 (Top 6 4, Rest 8) | share 18% vs 25% | interval -28 to +13 | shared  | Top 6: BONKZ 2, H-SR 1, RESIN 1 | Rest: -BN- 2, KSC 2, OGF 1, UYSC 1, EPOXY 1, MZY 1 | dmg 6,025
```
```
round 5 : PLACEBO wide: 14 Rest-only spots, labelled top by chance: mean 0.54, range 0 to 4, draws with >= 2: 7%
round 5b: PLACEBO wide: 14 Rest-only spots, labelled top by chance: mean 0.55, range 0 to 4, draws with >= 2: 8%
```

## part-c5/map-questions.json: 109 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-c5/part-hs.json: 69 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-c5/part-lp.json: 58 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-c5/spots.json: 18 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-d/clan_styles.json: 375 lines changed (1 more differ only in the order of ties)

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-d/d1_scores.json: 122 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-d/d1_tables.md: 13 lines changed (9 more differ only in the order of ties)

```
round 5 : | PFANS | 5-7 | 24 | 2.0 | 3:51 | 17 |
round 5b: | PFANS | 5-7 | 24 | 2.0 | 3:05 | 8 |
```
```
round 5 : | *VRTUS | 7-4 | 82 | 7.5 | 3:44 | 20 |
round 5b: | *VRTUS | 7-4 | 82 | 7.5 | 3:44 | 15 |
```
```
round 5 : | KSE | 2-5 | 20 | 2.9 | 5:08 | 20 |
round 5b: | KSE | 2-5 | 20 | 2.9 | 4:11 | 5 |
```
```
round 5 : | PFANS | 5-7 | 24 | 1.5 | 3.0 | 21 | 42 | 50 | 33 | 0.2 | 0.2 | 0.2 | 0.2 |
round 5b: | PFANS | 5-7 | 24 | 1.5 | 3.0 | 29 | 42 | 50 | 33 | 0.2 | 0.2 | 0.2 | 0.2 |
```
```
round 5 : | *VRTUS | 7-4 | 82 | 3.2 | 2.9 | 17 | 48 | 52 | 23 | 0.7 | 1.5 | 2.2 | 0.6 |
round 5b: | *VRTUS | 7-4 | 82 | 3.2 | 2.9 | 18 | 48 | 52 | 23 | 0.7 | 1.5 | 2.2 | 0.6 |
```
```
round 5 : | KSE | 2-5 | 20 | 2.1 | 2.9 | 15 | 50 | 0 | 10 | 0.3 | 0.4 | 0.6 | 0.4 |
round 5b: | KSE | 2-5 | 20 | 2.1 | 2.9 | 20 | 50 | 0 | 10 | 0.3 | 0.4 | 0.6 | 0.4 |
```
```
round 5 : | *HTDOG | 18 | Svea 67%, Jinan 50%, Daring 44%, Gdańsk 33%, Shimakaze 17%, Napoli 11% | 46 | Brisbane 9%, Des Moines 9%, Svea 9%, Delny 4% | Sleeping Giant A (25); Mountain Range A (12); Land of Fire B (10) | 28 / 72 |
round 5b: | *HTDOG | 18 | Svea 67%, Jinan 50%, Daring 44%, Gdańsk 33%, Shimakaze 17%, Gearing 11% | 46 | Brisbane 9%, Des Moines 9%, Svea 9%, Delny 4% | Sleeping Giant A (25); Mountain Range A (12); Land of Fire B (10) | 28 / 72 |
```
```
round 5 : | MACH | 7 | Z-42 71%, Napoli 29%, Daring 29%, Grozovoi 14%, Svea 14%, Cerberus 14% | 18 | Des Moines 6% | Okinawa C (6); Hotspot D (5); Loop A (3) | 31 / 69 |
round 5b: | MACH | 7 | Z-42 71%, Daring 29%, Napoli 29%, Grozovoi 14%, Svea 14%, Fuyutsuki 14% | 18 | Des Moines 6% | Okinawa C (6); Hotspot D (5); Loop A (3) | 31 / 69 |
```
```
round 5 : | Gearing | 21% | 23% | -24 to +21 |
round 5b: | Daring | 12% | 27% | -29 to +1 |
```
```
round 5 : | Daring | 12% | 27% | -30 to +1 |
round 5b: | Gearing | 21% | 23% | -22 to +18 |
```
```
round 5 : | First smoke of the game (median, s) | 2:55 | 3:18 | -56.0 to +26.5 |
round 5b: | First smoke of the game (median, s) | 2:55 | 3:16 | -54.0 to +29.5 |
```
```
round 5 : | Smokes after 12:00 (%) | 15 | 12 | -1.5 to +8.0 |
round 5b: | Smokes after 12:00 (%) | 14 | 11 | -1.6 to +7.8 |
```
```
round 5 : | Smokes before 5:00 (%) | 25 | 27 | -7.3 to +1.6 |
round 5b: | Smokes before 5:00 (%) | 25 | 28 | -7.3 to +1.3 |
```

## part-d/d2_structure.json: 1286 lines changed

(JSON file: the same values appear in the text outputs listed here; line count only.)

## part-d/d3_tables.md: 6 lines changed

```
round 5 : | First smoke of the game (median, s) | 2:43 (2:33 to 3:04) | 3:27 (3:01 to 4:06) | 3:07 (2:21 to 4:53) | 3:45 (3:11 to 4:52) |
round 5b: | First smoke of the game (median, s) | 2:43 (2:33 to 3:04) | 3:27 (3:01 to 4:06) | 3:05 (2:21 to 4:31) | 3:41 (3:01 to 4:16) |
```
```
round 5 : | Smokes after 12:00 (%) | 13 (10 to 17) | 15 (10 to 20) | 9 (4 to 16) | 8 (3 to 14) |
round 5b: | Smokes after 12:00 (%) | 13 (10 to 17) | 14 (9 to 18) | 8 (3 to 13) | 6 (2 to 11) |
```
```
round 5 : - **Team smoke, plenty of it** (W-L 101-66): Top 6: RESIN, H-SR, BONKZ, KITE | Rest: EPOXY, HFANS, -BN-, REEEE, KSC, BONKY, RSR | borderline (kept the style in under 75% of resamples): HFANS 60%, KITE 72%, REEEE 50% | flagged small clans that would fall here: INCA
round 5b: - **Team smoke, plenty of it** (W-L 101-66): Top 6: RESIN, H-SR, BONKZ, KITE | Rest: EPOXY, HFANS, -BN-, REEEE, KSC, BONKY, RSR | borderline (kept the style in under 75% of resamples): HFANS 57%, KITE 72%, REEEE 53%, RSR 73% | flagged small clans that would fall here: INCA
```
```
round 5 : - **Team smoke, little of it** (W-L 20-25): Top 6: none | Rest: MZY, PFANS, NGA, PN | borderline (kept the style in under 75% of resamples): PFANS 74%, NGA 74% | flagged small clans that would fall here: MANBA, RMN, KM
round 5b: - **Team smoke, little of it** (W-L 20-25): Top 6: none | Rest: MZY, PFANS, NGA, PN | borderline (kept the style in under 75% of resamples): NGA 72% | flagged small clans that would fall here: MANBA, RMN, KM
```
```
round 5 : - Axis 1: Top 6 mean -1.17, Rest mean +0.39, gap -1.56 (95% -3.57 to +0.49); Top 6 range -4.6 to +2.6, Rest range -3.0 to +4.0
round 5b: - Axis 1: Top 6 mean -1.20, Rest mean +0.40, gap -1.59 (95% -3.58 to +0.46); Top 6 range -4.6 to +2.5, Rest range -2.9 to +4.0
```
```
round 5 : - Axis 2: Top 6 mean +0.90, Rest mean -0.30, gap +1.21 (95% +0.22 to +2.24 *); Top 6 range +0.3 to +2.1, Rest range -3.3 to +2.4
round 5b: - Axis 2: Top 6 mean +0.89, Rest mean -0.30, gap +1.18 (95% +0.19 to +2.23 *); Top 6 range +0.3 to +2.0, Rest range -3.3 to +2.5
```

## part-c5/out-hs.txt (script output): 24 lines changed

```
round 5 : C: n 77 conc 8.5k ci (4862.752307692308, 12874.47347826087) deaths/100 5 ships Daring 22, Gdańsk 16, Somers 16, Gearing 11, Grozovoi 6, Harugumo 3 early 27 med time 6:56 we_took 14/47 edge q80 3575 max 12792
round 5b: C: n 77 conc 8.5k ci (4862.752307692308, 12874.47347826087) deaths/100 5 ships Daring 22, Gdańsk 16, Somers 16, Gearing 11, Grozovoi 6, Harugumo 3 early 29 med time 6:40 we_took 14/47 edge q80 3575 max 12792
```
```
round 5 : D: n 108 conc 13.0k ci (8813.359902912622, 16568.337115384616) deaths/100 9 ships Somers 41, Gearing 20, Daring 14, Harugumo 13, Shimakaze 8, Grozovoi 6 early 36 med time 6:24 we_took 21/75 edge q80 4834 max 19332
round 5b: D: n 108 conc 13.0k ci (8813.359902912622, 16568.337115384616) deaths/100 9 ships Somers 41, Gearing 20, Daring 14, Harugumo 13, Shimakaze 8, Grozovoi 6 early 37 med time 6:23 we_took 21/75 edge q80 4834 max 19332
```
```
round 5 : west share by time: early Top 6 3 of 23 (13%) vs Rest 2 of 45 (4%); gap +9 pts (-7 to +38) | later Top 6 26 of 57 (46%) vs Rest 19 of 110 (17%); gap +28 pts (+20 to +38 *)
round 5b: west share by time: early Top 6 3 of 23 (13%) vs Rest 2 of 48 (4%); gap +9 pts (-6 to +40) | later Top 6 26 of 57 (46%) vs Rest 19 of 107 (18%); gap +28 pts (+18 to +37 *)
```
```
round 5 : ellipse membership instead of cluster membership: G10 32 G5 23
round 5b: ellipse membership instead of cluster membership: G10 32 G5 24
```
```
round 5 : early DD smokes 68 | in G10 cluster 36 | in G5 cluster 27
round 5b: early DD smokes 71 | in G10 cluster 37 | in G5 cluster 29
```
```
round 5 : map-wide radar cruiser inside: Top 6 20 of 23 (87%) vs Rest 17 of 45 (38%); gap +49 pts (+31 to +71 *)
round 5b: map-wide radar cruiser inside: Top 6 20 of 23 (87%) vs Rest 18 of 48 (38%); gap +50 pts (+30 to +71 *)
```
```
round 5 : G10 cluster: Top 6 10 of 12 (83%) vs Rest 11 of 24 (46%); gap +38 pts (+6 to +63 *)
round 5b: G10 cluster: Top 6 10 of 12 (83%) vs Rest 12 of 25 (48%); gap +35 pts (+6 to +61 *)
```
```
round 5 : G5 cluster: Top 6 7 of 8 (88%) vs Rest 5 of 19 (26%); gap +61 pts (+28 to +91 *)
round 5b: G5 cluster: Top 6 7 of 8 (88%) vs Rest 5 of 21 (24%); gap +64 pts (+33 to +92 *)
```
```
round 5 : share of early smokes in G10: Top 6 12 of 23 (52%) vs Rest 24 of 45 (53%); gap -1 pts (-25 to +20)
round 5b: share of early smokes in G10: Top 6 12 of 23 (52%) vs Rest 25 of 48 (52%); gap +0 pts (-22 to +20)
```
```
round 5 : G10 clans Top 6: H-SR 5, BONKZ 3, RESIN 2, HTDOG 1, KITE 1 | Rest: REEEE 4, MZY 3, 5D 2, KSC 2, HFANS 2, KITED 2, BTLST 1, RMN 1, PN 1, MACH 1, -BN- 1, NGA 1, BONKY 1, PFANS 1, EPOXY 1
round 5b: G10 clans Top 6: H-SR 5, BONKZ 3, RESIN 2, HTDOG 1, KITE 1 | Rest: REEEE 4, MZY 3, 5D 2, KSC 2, PFANS 2, HFANS 2, KITED 2, BTLST 1, RMN 1, PN 1, MACH 1, -BN- 1, NGA 1, BONKY 1, EPOXY 1
```
```
round 5 : G10 ships Somers 16, Gearing 7, Harugumo 5, Shimakaze 3, Daring 3, Grozovoi 2 | cruisers inside top Brisbane 4, Des Moines 4, Worcester 2 | rest Brisbane 5, Des Moines 4, Utrecht 3, Minotaur 1, Stalingrad 1 | screened top Brisbane 1, Des Moines 1, Prins van Oranje 1 | rest San Martín 2, Bremen 2, Br
round 5b: G10 ships Somers 16, Gearing 7, Harugumo 6, Shimakaze 3, Daring 3, Grozovoi 2 | cruisers inside top Brisbane 4, Des Moines 4, Worcester 2 | rest Brisbane 6, Des Moines 4, Utrecht 3, Minotaur 1, Stalingrad 1 | screened top Brisbane 1, Des Moines 1, Prins van Oranje 1 | rest San Martín 2, Bremen 2, Br
```
```
round 5 : G10 radar cruiser inside by clan: H-SR 4/5, BONKZ 3/3, RESIN 1/2, HTDOG 1/1, KITE 1/1, REEEE 1/4, MZY 1/3, 5D 0/2, KSC 2/2, HFANS 2/2, KITED 0/2, BTLST 1/1, RMN 0/1, PN 1/1, MACH 0/1, -BN- 0/1, NGA 0/1, BONKY 1/1, PFANS 1/1, EPOXY 1/1
round 5b: G10 radar cruiser inside by clan: H-SR 4/5, BONKZ 3/3, RESIN 1/2, HTDOG 1/1, KITE 1/1, REEEE 1/4, MZY 1/3, 5D 0/2, KSC 2/2, PFANS 2/2, HFANS 2/2, KITED 0/2, BTLST 1/1, RMN 0/1, PN 1/1, MACH 0/1, -BN- 0/1, NGA 0/1, BONKY 1/1, EPOXY 1/1
```
```
round 5 : G10 conc 16.5k top 17.8k rest 15.9k deaths/100 5.555555555555555
round 5b: G10 conc 16.6k top 17.8k rest 16.0k deaths/100 5.405405405405405
```
```
round 5 : standing definition (early smoke covering a cruiser), Hotspot: inside Top 6 20 of 23 (87%) vs Rest 20 of 45 (44%); gap +42 pts (+25 to +65 *) | screened Top 6 2 of 23 (9%) vs Rest 11 of 45 (24%); gap -16 pts (-34 to -1 *) | none Top 6 1 of 23 (4%) vs Rest 14 of 45 (31%); gap -27 pts (-45 to -10 *)
round 5b: standing definition (early smoke covering a cruiser), Hotspot: inside Top 6 20 of 23 (87%) vs Rest 21 of 48 (44%); gap +43 pts (+25 to +63 *) | screened Top 6 2 of 23 (9%) vs Rest 11 of 48 (23%); gap -14 pts (-34 to +0) | none Top 6 1 of 23 (4%) vs Rest 16 of 48 (33%); gap -29 pts (-47 to -13 *)
```
```
round 5 : in G10: inside Top 6 10 of 12 (83%) vs Rest 13 of 24 (54%); gap +29 pts (+2 to +60 *) | screened Top 6 2 of 12 (17%) vs Rest 6 of 24 (25%); gap -8 pts (-32 to +14)
round 5b: in G10: inside Top 6 10 of 12 (83%) vs Rest 14 of 25 (56%); gap +27 pts (+0 to +56 *) | screened Top 6 2 of 12 (17%) vs Rest 6 of 25 (24%); gap -7 pts (-31 to +17)
```
```
round 5 : Hotspot: Top 6 20 of 23 (87%) vs Rest 17 of 45 (38%); gap +49 pts (+30 to +69 *)
round 5b: Hotspot: Top 6 20 of 23 (87%) vs Rest 18 of 48 (38%); gap +50 pts (+32 to +70 *)
```
```
round 5 : Loop: Top 6 4 of 9 (44%) vs Rest 5 of 23 (22%); gap +23 pts (-25 to +50)
round 5b: Loop: Top 6 4 of 10 (40%) vs Rest 5 of 23 (22%); gap +18 pts (-25 to +45)
```
```
round 5 : Okinawa: Top 6 2 of 3 (too few) vs Rest 4 of 23 (17%); gap +49 pts (-14 to +92)
round 5b: Okinawa: Top 6 2 of 3 (too few) vs Rest 4 of 23 (17%); gap +49 pts (-13 to +92)
```
```
round 5 : Land of Fire: Top 6 5 of 12 (42%) vs Rest 8 of 25 (32%); gap +10 pts (-26 to +50)
round 5b: Land of Fire: Top 6 5 of 12 (42%) vs Rest 8 of 25 (32%); gap +10 pts (-24 to +49)
```
```
round 5 : Mountain Range: Top 6 9 of 14 (64%) vs Rest 8 of 25 (32%); gap +32 pts (-8 to +72)
round 5b: Mountain Range: Top 6 9 of 14 (64%) vs Rest 8 of 25 (32%); gap +32 pts (-7 to +70)
```
```
round 5 : Sleeping Giant: Top 6 15 of 32 (47%) vs Rest 22 of 37 (60%); gap -13 pts (-40 to +18)
round 5b: Sleeping Giant: Top 6 15 of 32 (47%) vs Rest 22 of 37 (60%); gap -13 pts (-39 to +19)
```
```
round 5 : Sea of Fortune: Top 6 6 of 9 (67%) vs Rest 6 of 22 (27%); gap +39 pts (+12 to +62 *)
round 5b: Sea of Fortune: Top 6 6 of 9 (67%) vs Rest 6 of 22 (27%); gap +39 pts (+15 to +60 *)
```
```
round 5 : spot Top 6 13 of 64 (20%) vs Rest 7 of 80 (9%); gap +12 pts (-7 to +27) Top 6: RESIN 7, BONKZ 4, H-SR 2 | Rest: -BN- 4, INCA 1, KSC 1, MZY 1
round 5b: spot Top 6 13 of 64 (20%) vs Rest 7 of 80 (9%); gap +12 pts (-6 to +27) Top 6: RESIN 7, BONKZ 4, H-SR 2 | Rest: -BN- 4, INCA 1, KSC 1, MZY 1
```
```
round 5 : all destroyer smokes in the ellipse Top 6 17 of 80 (21%) vs Rest 17 of 155 (11%); gap +10 pts (-5 to +22) | cruisers inside top Moskva 5, Brisbane 4, Petropavlovsk 3, Utrecht 1, Minotaur 1 | rest Des Moines 2, Brisbane 1, Minotaur 1
round 5b: all destroyer smokes in the ellipse Top 6 17 of 80 (21%) vs Rest 17 of 155 (11%); gap +10 pts (-5 to +21) | cruisers inside top Moskva 5, Brisbane 4, Petropavlovsk 3, Utrecht 1, Minotaur 1 | rest Des Moines 2, Brisbane 1, Minotaur 1
```

## part-c5/out-lp.txt (script output): 12 lines changed

```
round 5 : | Hotspot | 62 (18 / 44) | 1.10 (0.89 to 1.28) | 1.28 | 1.02 | +0.26 (-0.10 to +0.65) | 0.85 (0.64 to 1.08) | 1.22 | 0.7 | +0.52 (+0.19 to +0.83 *) | 0.65 | 0.21 | 0.06 |
round 5b: | Hotspot | 62 (18 / 44) | 1.15 (0.95 to 1.32) | 1.28 | 1.09 | +0.19 (-0.18 to +0.56) | 0.87 (0.66 to 1.09) | 1.22 | 0.73 | +0.49 (+0.17 to +0.82 *) | 0.66 | 0.21 | 0.06 |
```
```
round 5 : | Loop | 46 (13 / 33) | 0.70 (0.48 to 0.94) | 0.69 | 0.7 | -0.00 (-0.58 to +0.45) | 0.43 (0.25 to 0.63) | 0.46 | 0.42 | +0.04 (-0.40 to +0.40) | 0.22 | 0.22 | 0.11 |
round 5b: | Loop | 46 (13 / 33) | 0.72 (0.50 to 0.96) | 0.77 | 0.7 | +0.07 (-0.46 to +0.56) | 0.46 (0.27 to 0.65) | 0.54 | 0.42 | +0.11 (-0.29 to +0.51) | 0.22 | 0.24 | 0.11 |
```
```
round 5 : Loop minus other maps, dd: -0.22 ci (-0.40587983445126297, -0.01665482674244212) | other maps rate 0.91
round 5b: Loop minus other maps, dd: -0.20 ci (-0.3970121381886087, -0.007363132363132352) | other maps rate 0.92
```
```
round 5 : Loop minus other maps, ecr: -0.25 ci (-0.41815823605706876, -0.08562691131498479) | other maps rate 0.69
round 5b: Loop minus other maps, ecr: -0.24 ci (-0.39808006535947715, -0.06108863072705906) | other maps rate 0.69
```
```
round 5 : Loop minus other maps, ins: -0.26 ci (-0.38319423061340246, -0.12941461054668602) | other maps rate 0.48
round 5b: Loop minus other maps, ins: -0.27 ci (-0.386842515998127, -0.13913777431502405) | other maps rate 0.48
```
```
round 5 : Loop minus other maps, scr: +0.01 ci (-0.11282051282051284, 0.16032608695652173) | other maps rate 0.21
round 5b: Loop minus other maps, scr: +0.03 ci (-0.08922558922558924, 0.18713781809019903) | other maps rate 0.21
```
```
round 5 : Loop team-games with zero early destroyer smokes: 21 of 46 | other maps 99 of 296
round 5b: Loop team-games with zero early destroyer smokes: 20 of 46 | other maps 97 of 296
```
```
round 5 : Loop team-games with zero early cruiser smokes: 29 | other maps 133
round 5b: Loop team-games with zero early cruiser smokes: 28 | other maps 132
```
```
round 5 : Loop early destroyer smoke ships Somers 8, Daring 6, Gearing 4, Gdańsk 3, Shimakaze 2, Z-42 2, Delny 2, Harugumo 1 | early cruiser smokes: ships Somers 8, Gearing 2, Gdańsk 2, Shimakaze 1, Harugumo 1, Vampire II 1, Grozovoi 1, La Pampa 1 | clans Top 6: RESIN 3, H-SR 2, BONKZ 1 | Rest: MACHX 2, -BN- 
round 5b: Loop early destroyer smoke ships Somers 8, Daring 6, Gearing 4, Shimakaze 3, Gdańsk 3, Z-42 2, Delny 2, Harugumo 1 | early cruiser smokes: ships Somers 8, Gearing 2, Shimakaze 2, Gdańsk 2, Harugumo 1, Vampire II 1, Grozovoi 1, La Pampa 1 | clans Top 6: RESIN 3, H-SR 2, VRTUS 1, BONKZ 1 | Rest: MACHX
```
```
round 5 : | Hotspot | 62 | 10.7 km (8.2 to 12.3) | 22% | 7.1 km | 7 of 15 | G10 (18%) | 2:37 | 81% | 12.07 / 9.97 (-2.0 to +7.6) |
round 5b: | Hotspot | 62 | 10.7 km (8.2 to 12.3) | 22% | 7.1 km | 7 of 15 | G10 (18%) | 2:37 | 84% | 12.07 / 9.97 (-2.0 to +7.6) |
```
```
round 5 : | Loop | 41 | 10.0 km (8.1 to 11.3) | 21% | 5.2 km | 11 of 18 | F4 (15%) | 4:14 | 68% | 9.93 / 9.9 (-4.4 to +2.1) |
round 5b: | Loop | 41 | 10.0 km (8.1 to 11.3) | 21% | 5.2 km | 11 of 18 | F4 (15%) | 4:14 | 71% | 9.93 / 9.9 (-4.4 to +2.1) |
```
```
round 5 : top: n 15 conc 5.8k deaths 1 own theirs 6, ours 5, neutral 4 we_took 5/10 enemy_took 0/9 zone B 13, C 2 med 8:34
round 5b: top: n 15 conc 5.8k deaths 1 own theirs 6, ours 5, neutral 4 we_took 5/10 enemy_took 0/9 zone B 13, C 2 med 8:04
```

## part-c5/out-lp-daring.txt (script output): 1 lines changed

```
round 5 : team radar ships in Daring team-games on Loop Moskva 8, Des Moines 8, San Martín 8, Petropavlovsk 7, Yueyang 4, Thor 3, Salem 3, Småland 2
round 5b: team radar ships in Daring team-games on Loop Des Moines 8, San Martín 8, Moskva 8, Petropavlovsk 7, Yueyang 4, Salem 3, Thor 3, Småland 2
```

## part-d/d2_output.txt (script output): 132 lines changed

```
round 5 : PC shares [29.5, 17.4, 12.3, 10.9, 9.1, 5.7] cumulative 2: 46.9 3: 59.1
round 5b: PC shares [29.6, 17.8, 11.6, 10.7, 9.1, 5.7] cumulative 2: 47.4 3: 59.0
```
```
round 5 : -0.84  Stacked on a teammate (%)
round 5b: -0.85  Stacked on a teammate (%)
```
```
round 5 : -0.82  For a teammate (%)
round 5b: -0.83  For a teammate (%)
```
```
round 5 : -0.81  Radar cruiser inside (% of destroyer smokes)
round 5b: -0.82  Radar cruiser inside (% of destroyer smokes)
```
```
round 5 : -0.79  Long-smoke destroyers per game
round 5b: -0.78  Long-smoke destroyers per game
```
```
round 5 : +0.71  Cruisers carrying smoke per game
round 5b: +0.72  Cruisers carrying smoke per game
```
```
round 5 : +0.68  Cap-sitter destroyers per game
round 5b: +0.67  Cap-sitter destroyers per game
```
```
round 5 : 
round 5b: +0.58  Kiting (%)
```
```
round 5 : 
round 5b: +0.56  Parked (%)
```
```
round 5 : 
round 5b: +0.41  Exhaust-smoke ships per game
```
```
round 5 : 
round 5b: +0.34  Inside a cap (%)
```
```
round 5 : 
round 5b: +0.32  Centre lane (%)
```
```
round 5 : 
round 5b: -0.31  Pushing (%)
```
```
round 5 : 
round 5b: +0.30  First smoke of the game (median, s)
```
```
round 5 : 
round 5b: -0.25  Median distance to cap edge (m)
```
```
round 5 : 
round 5b: +0.23  Smokes per game
```
```
round 5 : 
round 5b: -0.19  Smokes after 12:00 (%)
```
```
round 5 : 
round 5b: -0.05  Destroyers carrying smoke per game
```
```
round 5 : 
round 5b: PC2 loadings (correlation of the score with each feature):
```
```
round 5 : 
round 5b: +0.76  Smokes per game
```
```
round 5 : 
round 5b: +0.71  Destroyers carrying smoke per game
```
```
round 5 : +0.58  Kiting (%)
round 5b: +0.51  Smokes after 12:00 (%)
```
```
round 5 : +0.40  Exhaust-smoke ships per game
round 5b: -0.51  Pushing (%)
```
```
round 5 : +0.34  Inside a cap (%)
round 5b: +0.51  Cap-sitter destroyers per game
```
```
round 5 : -0.33  Pushing (%)
round 5b: -0.48  Exhaust-smoke ships per game
```
```
round 5 : +0.32  Centre lane (%)
round 5b: -0.46  First smoke of the game (median, s)
```
```
round 5 : +0.31  First smoke of the game (median, s)
round 5b: -0.37  Median distance to cap edge (m)
```
```
round 5 : -0.25  Median distance to cap edge (m)
round 5b: +0.29  Stacked on a teammate (%)
```
```
round 5 : +0.24  Smokes per game
round 5b: +0.24  Long-smoke destroyers per game
```
```
round 5 : -0.05  Destroyers carrying smoke per game
round 5b: 
```
```
round 5 : -0.04  Smokes after 12:00 (%)
round 5b: 
```
```
round 5 : PC2 loadings (correlation of the score with each feature):
round 5b: 
```
```
round 5 : +0.76  Destroyers carrying smoke per game
round 5b: 
```
```
round 5 : +0.76  Smokes per game
round 5b: 
```
```
round 5 : +0.54  Parked (%)
round 5b: 
```
```
round 5 : -0.54  First smoke of the game (median, s)
round 5b: 
```
```
round 5 : +0.52  Cap-sitter destroyers per game
round 5b: 
```
```
round 5 : -0.49  Exhaust-smoke ships per game
round 5b: 
```
```
round 5 : -0.47  Pushing (%)
round 5b: 
```
```
round 5 : -0.36  Median distance to cap edge (m)
round 5b: 
```
```
round 5 : +0.31  Smokes after 12:00 (%)
round 5b: 
```
```
round 5 : +0.31  Stacked on a teammate (%)
round 5b: 
```
```
round 5 : +0.28  Long-smoke destroyers per game
round 5b: 
```
```
round 5 : +0.17  Radar cruiser inside (% of destroyer smokes)
round 5b: +0.15  Radar cruiser inside (% of destroyer smokes)
```
```
round 5 : -0.12  Cruisers carrying smoke per game
round 5b: -0.11  Cruisers carrying smoke per game
```
```
round 5 : +0.08  For a teammate (%)
round 5b: +0.07  For a teammate (%)
```
```
round 5 : +0.02  Centre lane (%)
round 5b: -0.02  Kiting (%)
```
```
round 5 : -0.01  Kiting (%)
round 5b: -0.00  Centre lane (%)
```
```
round 5 : +0.71  Smokes after 12:00 (%)
round 5b: +0.64  Median distance to cap edge (m)
```
```
round 5 : +0.64  First smoke of the game (median, s)
round 5b: +0.58  First smoke of the game (median, s)
```
```
round 5 : -0.53  Inside a cap (%)
round 5b: +0.56  Centre lane (%)
```
```
round 5 : +0.48  Parked (%)
round 5b: -0.56  Inside a cap (%)
```
```
round 5 : +0.42  Median distance to cap edge (m)
round 5b: +0.34  Parked (%)
```
```
round 5 : +0.39  Centre lane (%)
round 5b: +0.33  Smokes after 12:00 (%)
```
```
round 5 : -0.34  Exhaust-smoke ships per game
round 5b: +0.28  Pushing (%)
```
```
round 5 : -0.25  Long-smoke destroyers per game
round 5b: -0.27  Exhaust-smoke ships per game
```
```
round 5 : +0.23  Radar cruiser inside (% of destroyer smokes)
round 5b: +0.26  Smokes per game
```
```
round 5 : -0.20  Kiting (%)
round 5b: +0.26  Radar cruiser inside (% of destroyer smokes)
```
```
round 5 : -0.19  Destroyers carrying smoke per game
round 5b: -0.15  Kiting (%)
```
```
round 5 : +0.14  Stacked on a teammate (%)
round 5b: +0.13  Cruisers carrying smoke per game
```
... and 72 more lines.

