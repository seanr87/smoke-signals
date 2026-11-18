# Findings C4: spots per map

Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Positions are team-normalized: own spawn at the bottom (bottom-left on Okinawa). Everything here is association: where smokes of a kind pile up and what those smokes returned, not what causes a result.

### C4. Spots per map, each marked Top 6 or Shared

**Answer:** There are 21 spots across six maps, and every one is a Shared spot: at the 1.5 to 2.5 km scale no place is used clearly more by the Top 6 than by the Rest. The two places that come closest to a Top 6 spot are the own-side half of cap B on Loop (cap sitters) and the own-side rim of cap B on Land of Fire (Svea); both clear the test only when the circle is widened to 2.5 km or more.

**Numbers:**

How a spot was found. For each map and each kind, all clans' smoke centres were pooled and the densest circles were taken one after another (radius 1.5 to 2.5 km, set by how tight the cluster is). A circle is a spot when it holds at least 8 smokes and at least 10% of that kind's smokes on that map (the 10% floor stops a busy map from being tiled with circles). High-paying cells use the 10 x 10 grid instead: a cell, or a pair of side-by-side cells, with 8 or more destroyer smokes whose concealed damage per smoke is clearly above the rest of that map.

Spots by map and kind:

| Map | long-smoke | cap sitter | parked cruiser | early cruiser | high-paying cell | all |
|---|---|---|---|---|---|---|
| Sleeping Giant | 1 | 1 | 0 | 1 | 1 | 4 (0 Top 6) |
| Hotspot | 1 | 2 | 0 | 2 | 1 | 6 (0 Top 6) |
| Loop | 1 | 2 | 0 | 0 | 0 | 3 (0 Top 6) |
| Mountain Range | 3 | 1 | 0 | 0 | 0 | 4 (0 Top 6) |
| Land of Fire | 0 | 1 | 1 | 0 | 0 | 2 (0 Top 6) |
| Sea of Fortune | 1 | 0 | 0 | 0 | 1 | 2 (0 Top 6) |
| Okinawa | 0 | 0 | 0 | 0 | 0 | 0 (0 Top 6) |
| All maps | 7 | 7 | 1 | 3 | 3 | 21 (0 Top 6) |

- Mode test: share of Top 6 smokes of that kind on that map that fall in the spot, minus the same share for the Rest, with a 95% interval from resampling whole clans. "Top 6 spot" also needs two Top 6 clans in it and at least 8 smokes of the kind from each group on the map.
- Result: 0 of 21 are Top 6 spots. 19 are Shared with no clear gap. 2 are Shared with "Rest use it more": cap sitters on the own-side rim of cap C on Hotspot (hs-sit-1: Top 6 6% vs Rest 23%, gap -30 to -5) and inside cap A on Loop (loop-sit-1: 4% vs 20%, gap -26 to -2).
- Closest to a Top 6 spot at this scale: Land of Fire Svea/Jinan at F5 (lof-park-1: 58% vs 19%, gap -6 to +70; the Rest side is one clan, BONKY 4), Loop cap sitters inside cap B (loop-sit-2: 30% vs 9%, gap -3 to +50), Sleeping Giant early cruiser smoke at G1/F1 (sg-early-1: 36% vs 20%, gap -8 to +38).
- Wider scale check (same search, circles 2.5 to 3.5 km; `wide.txt`): 25 spots, 2 labelled Top 6. Loop cap sitters inside cap B: 8 of 23 Top 6 smokes vs 6 of 65 Rest (35% vs 9%, gap +3 to +53; RESIN 3, HTDOG 2, VRTUS 1, BONKZ 1, H-SR 1 / Rest: REEEE 5, SCCC2 1). Land of Fire Svea/Jinan at F5: 14 of 19 vs 5 of 21 (74% vs 24%, gap +8 to +84; VRTUS 8, HTDOG 4, RESIN 2 / Rest: BONKY 4, -BN- 1). These are the same two places round 4 called signature spots; they are zones about 5 km across, not tight spots.
- Placebo for the "Top 6 spot" label (said once): the real Top 6 were left out, the same search was run on the Rest alone, and six of the twelve busiest Rest clans stood in as the top group, 200 draws. At the main scale 12 Rest-only spots were found and 0.33 of them were labelled "top" by chance on average (range 0 to 3). At the wider scale 14 spots, 0.54 on average (range 0 to 4); 7% of draws gave 2 or more. So the two wide-scale Top 6 zones are a little more than chance would give, not a lot more. Treat them as leads.
- High-paying cells: 137 cells or pairs were tested, 3 passed: Sleeping Giant G1 (24.1k per smoke vs 10.7k elsewhere, gap +8.2k to +20.2k, n 21), Hotspot G10+H10 (17.0k vs 11.4k, gap +0.8k to +10.7k, n 40), Sea of Fortune F9+G9 (24.6k vs 10.3k, gap +1.0k to +32.5k, n 10, small n). The cells were picked and scored on the same data, so they will shrink on new data. A shuffle check (concealed damage shuffled among each map's destroyer smokes, 20 runs) passed 1.85 cells on average (range 0 to 4), so only G1, whose interval is far from zero, should be trusted on its own.
- Win/loss split is shown where the two means are more than 5k apart with at least 5 smokes on each side. Sleeping Giant G1 pays in both (wins 26.5k, n 14; losses 19.3k, n 7). Hotspot G10+H10: wins 21.3k (n 16), losses 14.1k (n 24). Sea of Fortune F9+G9 has only 2 losses: too few to split.
- Cap taken (cap nearest the smoke, not already ours, ours within 60 s of the smoke clearing): G1 19% of 21, Hotspot G10+H10 34% of 35, Sea of Fortune F9+G9 25% of 8 (small n).
- Early cruiser smoke spots exist on two maps only: Sleeping Giant G1/F1 (n 16: cruiser inside 12, screened 4), Hotspot G10/F10 (n 17: inside 13, screened 4) and Hotspot G6/G5 (n 9: inside 7, screened 2, small n). The first two are the same water as the long-smoke spot and the high-paying cell on those maps: one opening, seen three ways.

**Top 6 or Shared:** Shared, all 21. No interval of the share gap is above zero at the 1.5 to 2.5 km scale; two are below zero (Rest use them more). Two wider zones (Loop cap B for cap sitters, Land of Fire F5 for Svea) pass at 2.5 km and are flagged as leads.

**Clans:** named with counts for every spot in the map tables below (and in `spots.json`).

**Could not be done / proxy:**
- "Covered by" a spot means a cruiser was inside the smoke or screened by it (behind it or firing through it); this comes from the batch's own per-smoke record, not from a continuous track.
- "Selfish" here means the ship type (cap sitters; Svea/Jinan), not the batch's selfish flag; the flag's share per spot is in `spots.json` (`selfish_flag_pct`).
- Parked cruiser smoke (Svea/Jinan) forms a compact spot on one map only. On Sea of Fortune and Mountain Range the Top 6 Svea smokes sit in wide bands (round 4's zones there were 6 to 10 km across), too spread to be a spot under this round's rule.
- Okinawa has no spot of any kind: pools are small (16 to 40 smokes per kind) and spread out, and the Top 6 laid only 2 to 10 smokes per kind there.
- Cap taken uses cap owners recorded only at smoke moments, so it is unknown for some smokes (they are left out of the rate).

**Verdict:** Keep (as the per-map catalogue; the Top 6 vs Shared marking finds no Top 6 spot at this scale, and the two wide zones are leads, not findings).

### Per-map spot tables

Columns: mode shows the share of each group's smokes of that kind on that map that fall in the spot, the gap and its 95% interval. "Cruisers" lists the cruisers inside the smoke and those screened by it, Top 6 then Rest (top three by count; full lists in `spots.json`). Damage is concealed damage per smoke. "small n" = 8 to 14 smokes. Examples are the three highest-damage smokes in the spot.

Wide-scale leads: loop-sit-2 (Loop, cap B, cap sitters) and lof-park-1 (Land of Fire, F5, Svea) become "Top 6" when the circle is 2.5 km; everything else stays Shared at both scales.

#### Sleeping Giant

Figure: `figures/c4-sg.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 42 such smokes on this map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| sg-long-1 | long-smoke | 2.5 km outside cap A, own side, west edge of the map (G1/F1) | Shared: 18% vs 12% (gap +6, -7 to +22) | 12 / 9 | Top 6: BONKZ 4, VRTUS 3, H-SR 3, RESIN 2 / Rest: BONKY 3, PFANS 2, KSC 2, NGA 1, EPOXY 1 | Top 6: inside Des Moines 3, Worcester 3, Brisbane 1 +1 more; screened Brisbane 3, Utrecht 1 / Rest: inside Brisbane 3, Salem 1, Minotaur 1 +2 more; screened Minotaur 1, Bremen 1 | 20.7k | 10 | 2:40 | wins 27.5k (n 10) vs losses 14.5k (n 11); ships: Harugumo 8, Gearing 7, Somers 6 |
| sg-sit-1 | selfish: cap sitter | 1.7 km outside cap B, own side (G6/F6) | Shared: 12% vs 17% (gap -5, -23 to +8) | 5 / 9 | Top 6: HTDOG 4, VRTUS 1 / Rest: HFANS 3, KSE 2, BONKY 2, EPOXY 1, KSC 1 | Top 6: screened Moskva 1, Stalingrad 1 / Rest: screened Des Moines 1, Stalingrad 1, Petropavlovsk 1 | 8.0k | 14 | 6:36 | small n; wins 11.8k (n 9) vs losses 1.4k (n 5); ships: Daring 7, Gdańsk 6, Z-52 1 |
| sg-early-1 | early cruiser | 2.6 km outside cap A, own side, west edge of the map (G1/F1) | Shared: 36% vs 20% (gap +16, -8 to +38) | 10 / 6 | Top 6: BONKZ 3, RESIN 3, VRTUS 2, H-SR 2 / Rest: PFANS 2, KSC 2, BONKY 1, EPOXY 1 | Top 6: inside Des Moines 3, Worcester 2, Brisbane 1 +1 more; screened Brisbane 2, Utrecht 1 / Rest: inside Salem 1, Brisbane 1, Minotaur 1 +2 more; screened Minotaur 1 | 22.6k | 6 | 2:20 | inside 12 (Top 6 7, Rest 5), screened 4 (Top 6 3, Rest 1); wins 28.2k (n 9) vs losses 15.3k (n 7) |
| sg-cell-1 | high-paying cell | 4.1 km outside cap A, own side, west edge of the map (G1) | Shared: 11% vs 7% (gap +4, -4 to +13) | 12 / 9 | Top 6: RESIN 5, VRTUS 3, BONKZ 2, HTDOG 1, H-SR 1 / Rest: BONKY 3, KSC 2, PFANS 2, NGA 1, -BN- 1 | Top 6: inside Worcester 3, Des Moines 3, Utrecht 1 +4 more; screened Utrecht 1, Brisbane 1 / Rest: inside Brisbane 3, Des Moines 3, Salem 1 +1 more; screened Bremen 1 | 24.1k | 14 | 2:40 | 24.1k vs 10.7k elsewhere on the map (gap +8.2k to +20.2k); median 21.9k; 10 clans, 13 games; cap taken 19% of 21; wins 26.5k (n 14) vs losses 19.3k (n 7) |

Examples: sg-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7990_g1_188224.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7992_g1_29782.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7936_g1_104465.html); sg-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8153_g1_92180.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8150_g2_188191.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8145_g1_161939.html); sg-early-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7990_g1_188224.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7992_g1_29782.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7906_g1_188243.html); sg-cell-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7990_g1_188224.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7992_g1_29782.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7936_g1_104465.html)

#### Hotspot

Figure: `figures/c4-hs.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 27 such smokes on this map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| hs-long-1 | long-smoke | 2.6 km outside cap D, own side, east edge of the map (G10) | Shared: 14% vs 22% (gap -8, -22 to +1) | 9 / 18 | Top 6: RESIN 3, H-SR 2, BONKZ 2, HTDOG 1, KITE 1 / Rest: BONKY 4, BTLST 3, HFANS 2, -BN- 2, REEEE 2, KSC 2, MZY 1, PN 1, PFANS 1 | Top 6: inside Worcester 3, Brisbane 2, Des Moines 2 +1 more; screened Des Moines 1, Prins van Oranje 1 / Rest: inside Brisbane 9, Des Moines 5; screened Bremen 2, Brisbane 1, Des Moines 1 | 16.1k | 4 | 3:16 | ships: Somers 11, Gearing 9, Harugumo 7 |
| hs-sit-1 | selfish: cap sitter | on the rim of cap C, own side (F6/F5/G5) | Shared: 6% vs 23% (gap -17, -30 to -5); Rest use it more | 1 / 17 | Top 6: H-SR 1 / Rest: KSC 5, EPOXY 5, PFANS 2, BTLST 1, UYSC 1, HFANS 1, INCA 1, MACHX 1 | Top 6: inside Petropavlovsk 1 / Rest: screened Petropavlovsk 1, Prins van Oranje 1 | 2.1k | 0 | 5:16 | ships: Daring 10, Gdańsk 7, Grozovoi 1 |
| hs-sit-2 | selfish: cap sitter | 0.5 km outside cap D, own side, east edge of the map (F10/G10) | Shared: 12% vs 12% (gap +0, -22 to +12) | 2 / 9 | Top 6: H-SR 2 / Rest: 5D 3, KITED 2, INCA 1, MACH 1, MACHX 1, SCCC2 1 | Top 6: inside Brisbane 1; screened Brisbane 1 / Rest: screened San Martín 3 | 11.3k | 0 | 5:33 | small n; ships: Grozovoi 4, Daring 4, Shimakaze 3 |
| hs-early-1 | early cruiser | 2.4 km outside cap D, own side, east edge of the map (G10/F10) | Shared: 36% vs 29% (gap +7, -15 to +33) | 8 / 9 | Top 6: H-SR 2, BONKZ 2, RESIN 2, HTDOG 1, KITE 1 / Rest: HFANS 2, BTLST 1, PN 1, -BN- 1, BONKY 1, REEEE 1, PFANS 1, KSC 1 | Top 6: inside Brisbane 2, Des Moines 2, Worcester 2; screened Brisbane 1, Des Moines 1, Prins van Oranje 1 / Rest: inside Brisbane 4, Des Moines 3; screened Des Moines 1, Bremen 1 | 19.0k | 0 | 2:44 | inside 13 (Top 6 6, Rest 7), screened 4 (Top 6 2, Rest 2); wins 16.1k (n 8) vs losses 21.5k (n 9) |
| hs-early-2 | early cruiser | 1.8 km outside cap C, own side (G6/G5) | Shared: 18% vs 16% (gap +2, -16 to +19) | 4 / 5 | Top 6: BONKZ 2, H-SR 1, RESIN 1 / Rest: KSC 2, OGF 1, -BN- 1, MZY 1 | Top 6: inside Brisbane 2, Utrecht 1, Minotaur 1 +1 more; screened Worcester 1 / Rest: inside Minotaur 2, Des Moines 1; screened Brennus 1, Brisbane 1, Petropavlovsk 1 +1 more | 6.8k | 0 | 2:08 | small n; inside 7 (Top 6 4, Rest 3), screened 2 (Top 6 0, Rest 2) |
| hs-cell-1 | high-paying cell | 5.9 km outside cap D, own side, east edge of the map (G10/H10) | Shared: 16% vs 17% (gap -1, -12 to +8) | 13 / 27 | Top 6: H-SR 5, RESIN 4, HTDOG 1, VRTUS 1, KITE 1, BONKZ 1 / Rest: REEEE 5, BONKY 4, BTLST 3, -BN- 3, MZY 2, HFANS 2, KITED 2, KSC 2, NGA 1, SCCC2 1, PFANS 1, EPOXY 1 | Top 6: inside Worcester 4, Brisbane 3, Des Moines 2 +1 more; screened Brisbane 1, Des Moines 1, Prins van Oranje 1 / Rest: inside Brisbane 9, Des Moines 6, Prinz Adalbert 1 +2 more; screened Bremen 4, Brisbane 1, Des Moines 1 +1 more | 17.0k | 10 | 5:35 | 17.0k vs 11.4k elsewhere on the map (gap +0.8k to +10.7k); median 11.0k; 18 clans, 18 games; cap taken 34% of 35; wins 21.3k (n 16) vs losses 14.1k (n 24) |

Examples: hs-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g2_90084.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8141_g2_161896.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8148_g2_125976.html); hs-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8068_g3_48783.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7970_g1_159228.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8072_g1_103842.html); hs-sit-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7959_g1_87003.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8073_g1_34492.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7888_g1_38992.html); hs-early-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g2_90084.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8148_g2_125976.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8139_g2_200262.html); hs-early-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8072_g1_103837.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8067_g1_60864.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8174_g1_94344.html); hs-cell-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8183_g2_90084.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8141_g2_161896.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8178_g2_224008.html)

#### Loop

Figure: `figures/c4-loop.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 15 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 20 such smokes on this map); no high-paying cell (of 21 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| loop-long-1 | long-smoke | 1.6 km outside cap B, own side (F8/G8) | Shared: 22% vs 15% (gap +7, -21 to +85) | 4 / 4 | Top 6: BONKZ 3, RESIN 1 / Rest: OGF 1, KM 1, MACHX 1, HFANS 1 | Top 6: inside Brisbane 3, Des Moines 1; screened Utrecht 1 / Rest: inside Des Moines 2; screened Worcester 1 | 36.0k | 12 | 5:12 | small n; ships: Gearing 4, Somers 3, Harugumo 1 |
| loop-sit-1 | selfish: cap sitter | inside cap A, own side (F4) | Shared: 4% vs 20% (gap -16, -26 to -2); Rest use it more | 1 / 13 | Top 6: KITE 1 / Rest: REEEE 5, EPOXY 3, MACH 2, KITED 1, -BN- 1, HFANS 1 | Top 6: none / Rest: inside Des Moines 1; screened Prins van Oranje 1 | 6.7k | 0 | 8:02 | small n; ships: Daring 12, Z-42 2 |
| loop-sit-2 | selfish: cap sitter | inside cap B, own side (F7) | Shared: 30% vs 9% (gap +21, -3 to +50) | 7 / 6 | Top 6: RESIN 3, HTDOG 2, VRTUS 1, H-SR 1 / Rest: REEEE 5, SCCC2 1 | Top 6: inside Minotaur 1; screened Petropavlovsk 2, Moskva 1, Prins van Oranje 1 / Rest: none | 2.3k | 0 | 9:43 | small n; ships: Z-42 5, Gdańsk 4, Shimakaze 3, Daring 1 |

Examples: loop-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7889_g1_178499.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7891_g1_46432.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8068_g1_178435.html); loop-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7917_g1_116013.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8070_g2_163984.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8148_g1_20502.html); loop-sit-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7976_g1_219218.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8150_g1_34881.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8176_g4_180815.html)

#### Mountain Range

Figure: `figures/c4-mr.png`. Not found here: no selfish: parked cruiser spot (no compact place holds 8 of the 46 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 28 such smokes on this map); no high-paying cell (of 20 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| mr-long-1 | long-smoke | 2.1 km outside cap B, own side (F4/G4) | Shared: 11% vs 20% (gap -9, -27 to +7) | 4 / 8 | Top 6: KITE 2, H-SR 1, BONKZ 1 / Rest: -BN- 3, HFANS 2, BONKY 2, INCA 1 | Top 6: inside Minotaur 2, Des Moines 1, Svea 1; screened Salem 1 / Rest: inside Brisbane 3, Smolensk 2, Minotaur 1; screened Brisbane 1, Napoli 1, Smolensk 1 | 14.3k | 0 | 3:48 | small n; ships: Gearing 6, Somers 5, Harugumo 1 |
| mr-long-2 | long-smoke | 2.1 km outside cap C, own side (G7) | Shared: 19% vs 7% (gap +12, -5 to +26) | 7 / 3 | Top 6: H-SR 3, BONKZ 2, RESIN 2 / Rest: UYSC 1, NGA 1, KSC 1 | Top 6: inside Minotaur 3, Des Moines 2, Svea 1; screened Brisbane 1, Moskva 1 / Rest: screened Worcester 1, Bremen 1, Des Moines 1 | 17.8k | 30 | 5:25 | small n; wins 22.5k (n 5) vs losses 13.1k (n 5); ships: Somers 6, Gearing 3, Harugumo 1 |
| mr-long-3 | long-smoke | 2.3 km outside cap B, own side (G5/G4) | Shared: 14% vs 10% (gap +4, -15 to +17) | 5 / 4 | Top 6: KITE 3, H-SR 2 / Rest: INCA 2, UYSC 1, PN 1 | Top 6: inside Brisbane 2, Des Moines 1, Moskva 1 +2 more; screened Stalingrad 1, Moskva 1 / Rest: inside Minotaur 2, Des Moines 1, Brisbane 1; screened Svea 1 | 10.0k | 11 | 2:37 | small n; ships: Gearing 5, Somers 4 |
| mr-sit-1 | selfish: cap sitter | on the rim of cap C, own side (F7) | Shared: 25% vs 16% (gap +9, -14 to +35) | 4 / 5 | Top 6: RESIN 2, BONKZ 2 / Rest: HFANS 3, SCCC2 1, MACH 1 | Top 6: none / Rest: screened San Martín 1 | 4.3k | 0 | 4:27 | small n; ships: Gdańsk 4, Daring 4, Z-42 1 |

Examples: mr-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7931_g1_214651.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8146_g2_121102.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159422.html); mr-long-2: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8069_g2_143195.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159429.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159438.html); mr-long-3: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7901_g1_27149.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7984_g1_15359.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7930_g1_51294.html); mr-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159435.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7901_g1_27140.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7903_g1_159425.html)

#### Land of Fire

Figure: `figures/c4-lof.png`. Not found here: no long-smoke spot (no compact place holds 8 of the 57 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 25 such smokes on this map); no high-paying cell (of 10 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| lof-sit-1 | selfish: cap sitter | on the rim of cap B, own side (F5) | Shared: 10% vs 16% (gap -6, -32 to +13) | 3 / 6 | Top 6: VRTUS 3 / Rest: -BN- 3, SCCC2 1, MACHX 1, HFANS 1 | Top 6: inside Svea 3 / Rest: none | 2.6k | 0 | 7:08 | small n; ships: Daring 6, Z-42 3 |
| lof-park-1 | selfish: parked cruiser | 1.0 km outside cap B, own side (F5) | Shared: 58% vs 19% (gap +39, -6 to +70) | 11 / 4 | Top 6: VRTUS 7, HTDOG 2, RESIN 2 / Rest: BONKY 4 | Top 6: none / Rest: none | 11.0k | 7 | 6:13 | wins 16.1k (n 5) vs losses 8.5k (n 10); ships: Svea 15 |

Examples: lof-sit-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/8143_g2_214598.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8154_g1_175939.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7928_g1_68248.html); lof-park-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7982_g1_197657.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/8143_g2_214597.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8143_g2_214607.html)

#### Sea of Fortune

Figure: `figures/c4-sof.png`. Not found here: no selfish: cap sitter spot (no compact place holds 8 of the 47 such smokes on this map); no selfish: parked cruiser spot (no compact place holds 8 of the 45 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 24 such smokes on this map).

| id | kind | where (cells) | mode: share of Top 6 vs Rest smokes of this kind | n Top 6 / Rest | clans | cruisers inside / screened | damage per smoke | deaths per 100 | median time | note |
|---|---|---|---|---|---|---|---|---|---|---|
| sof-long-1 | long-smoke | 4.5 km outside cap D, east side, east edge of the map (F9/F10) | Shared: 14% vs 14% (gap +0, -21 to +24) | 3 / 5 | Top 6: BONKZ 3 / Rest: BONKY 2, MZY 2, -BN- 1 | Top 6: inside Brisbane 3 / Rest: inside Des Moines 2, Brisbane 2; screened Des Moines 1 | 28.6k | 0 | 5:40 | small n; ships: Somers 4, Gearing 3, Harugumo 1 |
| sof-cell-1 | high-paying cell | 3.5 km outside cap D, own side (F9/G9) | Shared: 10% vs 8% (gap +3, -10 to +20) | 4 / 6 | Top 6: BONKZ 3, H-SR 1 / Rest: BONKY 2, MZY 2, -BN- 1, HFANS 1 | Top 6: inside Brisbane 3, Utrecht 1; screened Brisbane 1 / Rest: inside Des Moines 2, Brisbane 2, Utrecht 1; screened Des Moines 1 | 24.6k | 0 | 2:31 | small n; 24.6k vs 10.3k elsewhere on the map (gap +1.0k to +32.5k); median 14.1k; 6 clans, 5 games; cap taken 25% of 8; win/loss: 28.0k (n 8) vs 10.9k (n 2); too few on one side to compare |

Examples: sof-long-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7940_g1_183534.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7937_g1_44423.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/8144_g2_39538.html); sof-cell-1: [1](https://seanr87.github.io/smoke-signals/smoke/smokes/7940_g1_183534.html), [2](https://seanr87.github.io/smoke-signals/smoke/smokes/7937_g1_44423.html), [3](https://seanr87.github.io/smoke-signals/smoke/smokes/7912_g1_85162.html)

#### Okinawa

Figure: `figures/c4-oki.png`. Not found here: no long-smoke spot (no compact place holds 8 of the 38 such smokes on this map); no selfish: cap sitter spot (no compact place holds 8 of the 40 such smokes on this map); no selfish: parked cruiser spot (no compact place holds 8 of the 26 such smokes on this map); no early cruiser smoke spot (no compact place holds 8 of the 16 such smokes on this map); no high-paying cell (of 4 cells or pairs with 8+ destroyer smokes, none is clearly above the rest of the map).

No spot of any kind on this map.
