# C3 danger zones

Health is an estimate (r5lib: lower quartile of damage taken by ships of that type that died), so "hurt" (died or lost >= 1/3 of estimated health) is approximate; the death-only rate is exact.

Baselines (like-with-like):
| who | map | smokes | ships at risk | died per 100 | died or hurt per 100 |
|---|---|---|---|---|---|
| destroyer smoker | all maps | 1074 | 1074 | 6.4 | 15.5 |
| destroyer smoker | Sleeping Giant | 238 | 238 | 7.1 | 16.0 |
| destroyer smoker | Hotspot | 235 | 235 | 3.4 | 11.9 |
| destroyer smoker | Mountain Range | 132 | 132 | 3.8 | 13.6 |
| destroyer smoker | Land of Fire | 128 | 128 | 7.8 | 22.7 |
| destroyer smoker | Sea of Fortune | 117 | 117 | 8.5 | 14.5 |
| destroyer smoker | Loop | 142 | 142 | 6.3 | 14.8 |
| destroyer smoker | Okinawa | 82 | 82 | 12.2 | 19.5 |
| sheltering cruisers | all maps | 561 | 613 | 8.0 | 22.0 |
| sheltering cruisers | Sleeping Giant | 141 | 146 | 6.8 | 19.2 |
| sheltering cruisers | Hotspot | 144 | 159 | 6.3 | 16.4 |
| sheltering cruisers | Mountain Range | 64 | 72 | 8.3 | 20.8 |
| sheltering cruisers | Land of Fire | 54 | 57 | 14.0 | 24.6 |
| sheltering cruisers | Sea of Fortune | 66 | 79 | 6.3 | 30.4 |
| sheltering cruisers | Loop | 53 | 55 | 7.3 | 20.0 |
| sheltering cruisers | Okinawa | 39 | 45 | 13.3 | 37.8 |
Check: destroyer smokes Top 6 387, Rest 687; smokes covering a cruiser 561, sheltering cruisers 613.

Areas built: 313 (grid cells, merged 2 x 2 groups of thin cells, and "inside cap" zones); with >= 8 smokes and tested: 109 (77 destroyer, 32 cruiser); under 8 smokes, not rated: 204.
Flag rule: >= 8 smokes and the died-or-hurt rate clearly above BOTH the all-map and the same-map baseline (95% interval of the difference excludes zero, clans resampled, 2000 resamples).
Flagged areas: 4. Areas clearly above the all-map baseline only (not above their own map): 0. Areas that would be flagged on deaths alone: 0.

Placebo (120 runs: outcomes shuffled among the smokes of the same map, same 109 areas, same rule, 300 resamples each): areas flagged by luck per run: mean 1.23, median 1.0, 95th percentile 3, max 5; runs with no flag at all: 39 of 120; runs with at least as many flags as the real data (4): 5 of 120.
Real data with the same 300 resamples: 3 flags. Death-only rule by luck: mean 0.30 per run (real: 0).
Luck flags per map per run: Sleeping Giant 0.30, Hotspot 0.13, Mountain Range 0.23, Land of Fire 0.18, Sea of Fortune 0.19, Loop 0.07, Okinawa 0.11

## Sleeping Giant
Areas tested: 19 destroyer, 6 cruiser. Flagged: 1.
| map | who | area | smokes | ships at risk | died or hurt per 100 | all-map / same-map baseline | gap vs all maps (interval) | gap vs same map (interval) | died per 100 (baseline all / map) | death gap vs all maps | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sleeping Giant | destroyer smoker | E7+F7+F8 | 8 (small n) | 8 | 50 (4 of 8) | 15.5 / 16.0 | +34 (+1 to +67 *) | +34 (+1 to +66 *) | 25 (2; 6.4 / 7.1) | +19 (-7 to +56) | FLAG |
- E7+F7+F8 (destroyer smoker) FLAGGED: Shared spot (share of the map's destroyer smokes laid here: Top 6 2%, Rest 5%, gap interval -8 to +1). Laid while 50+ behind: 25% (map: 24%). Enemy radar detection in the smoke: 50% (map: 14%). 7 clans, 8 games. Top 6: BONKZ 2 | Rest: RMN 1, SCCC2 1, PFANS 1, -BN- 1, RSR 1, KITED 1. Without the clan with most bad outcomes (PFANS): 42.9 per 100 (n 7).

## Hotspot
Areas tested: 15 destroyer, 9 cruiser. Flagged: 1.
| map | who | area | smokes | ships at risk | died or hurt per 100 | all-map / same-map baseline | gap vs all maps (interval) | gap vs same map (interval) | died per 100 (baseline all / map) | death gap vs all maps | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Hotspot | destroyer smoker | inside cap C | 22 | 22 | 32 (7 of 22) | 15.5 / 11.9 | +16 (+3 to +52 *) | +20 (+7 to +58 *) | 9 (2; 6.4 / 3.4) | +3 (-8 to +26) | FLAG |
- inside cap C (destroyer smoker) FLAGGED: Shared spot (share of the map's destroyer smokes laid here: Top 6 0%, Rest 14%, gap interval -23 to -4 *). Laid while 50+ behind: 18% (map: 22%). Enemy radar detection in the smoke: 23% (map: 8%). 8 clans, 10 games. Top 6: none | Rest: EPOXY 9, KSC 7, BTLST 1, RMN 1, 5D 1, UYSC 1, MACHX 1, MZY 1. Without the clan with most bad outcomes (KSC): 33.3 per 100 (n 15).

## Mountain Range
Areas tested: 11 destroyer, 7 cruiser. Flagged: 1.
| map | who | area | smokes | ships at risk | died or hurt per 100 | all-map / same-map baseline | gap vs all maps (interval) | gap vs same map (interval) | died per 100 (baseline all / map) | death gap vs all maps | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mountain Range | sheltering cruisers | E7+F7+F8 | 8 (small n) | 9 | 56 (5 of 9) | 22.0 / 20.8 | +34 (+3 to +74 *) | +35 (+7 to +75 *) | 22 (2; 8.0 / 8.3) | +14 (-9 to +64) | FLAG |
- E7+F7+F8 (sheltering cruisers) FLAGGED: Shared spot (share of the map's cruiser-covering smokes laid here: Top 6 5%, Rest 22%, gap interval -40 to +1). Laid while 50+ behind: 50% (map: 20%). Enemy radar detection in the smoke: 38% (map: 16%). 6 clans, 7 games. Top 6: BONKZ 1, H-SR 1 | Rest: RSR 3, INCA 1, -BN- 1, KSC 1. Without the clan with most bad outcomes (RSR): 60.0 per 100 (n 5).

## Land of Fire
Areas tested: 7 destroyer, 2 cruiser. Flagged: 0. No area qualifies on this map.

## Sea of Fortune
Areas tested: 8 destroyer, 5 cruiser. Flagged: 1.
| map | who | area | smokes | ships at risk | died or hurt per 100 | all-map / same-map baseline | gap vs all maps (interval) | gap vs same map (interval) | died per 100 (baseline all / map) | death gap vs all maps | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sea of Fortune | destroyer smoker | E5+F5+E6 | 8 (small n) | 8 | 62 (5 of 8) | 15.5 / 14.5 | +47 (+9 to +86 *) | +48 (+12 to +88 *) | 38 (3; 6.4 / 8.5) | +31 (-5 to +75) | FLAG |
- E5+F5+E6 (destroyer smoker) FLAGGED: Shared spot (share of the map's destroyer smokes laid here: Top 6 8%, Rest 6%, gap interval -10 to +11). Laid while 50+ behind: 50% (map: 28%). Enemy radar detection in the smoke: 38% (map: 15%). 7 clans, 6 games. Top 6: RESIN 2, BONKZ 1 | Rest: 5D 1, NGA 1, MACHX 1, KSE 1, RSR 1. Without the clan with most bad outcomes (5D): 57.1 per 100 (n 7).

## Loop
Areas tested: 12 destroyer, 2 cruiser. Flagged: 0. No area qualifies on this map.

## Okinawa
Areas tested: 5 destroyer, 1 cruiser. Flagged: 0. No area qualifies on this map.

Wrote danger-zones.json (4 records).
