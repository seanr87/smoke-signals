# Findings C4: spots per map

Batch `output/20261117-122135` (1,547 smokes, 171 games, 30 clans). Positions are team-normalized: own spawn at the bottom (bottom-left on Okinawa). Everything here is association: where smokes of a kind pile up and what those smokes returned, not what causes a result.

### C4. Spots per map, each marked Top 6 or Shared

**Answer:** There are 21 spots across six maps, and every one is a Shared spot: at the 1.5 to 2.5 km scale no place is used clearly more by the Top 6 than by the Rest. The two places that come closest to a Top 6 spot are the own-side half of cap B on Loop (cap sitters) and the own-side rim of cap B on Land of Fire (Svea); both clear the test only when the circle is widened to 2.5 km or more.

**Numbers:**

How a spot was found. For each map and each kind, all clans' smoke centres were pooled and the densest circles were taken one after another (radius 1.5 to 2.5 km, set by how tight the cluster is). A circle is a spot when it holds at least 8 smokes and at least 10% of that kind's smokes on that map (the 10% floor stops a busy map from being tiled with circles). High-paying cells use the 10 x 10 grid instead: a cell, or a pair of side-by-side cells, with 8 or more destroyer smokes whose concealed damage per smoke is clearly above the rest of that map.

Spots by map and kind:

{{COUNTS}}

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
{{MAPS}}
