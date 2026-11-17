# Module 1: round 4 changes

All scripts were rerun on the corrected shared loader (`tables.py`, `extras.py`, `cells.py`, `figures.py`). Round 3 outputs are kept as `tables-r3.txt` and `extras-r3.txt` for comparison.

## Clusters

Unchanged. Same four clusters, same members, same merge order:
- flank smoke lines: Somers, Gearing, Harugumo, Delny (n=562)
- cap sitters: Daring, Z-42, Gdańsk, Grozovoi, Shimakaze (n=462)
- parked cruiser smoke: Svea, Jinan (n=241)
- moving exhaust: Napoli, Venezia, C. Colombo (n=188)

These match the `habit` field in the shared loader exactly. Per map check is still 35 of 39.

## Numbers in MODULE-1.md that changed because of the loader fix

None. The loader fix moved the position of about 3 smokes (one Gearing on Land of Fire, one Gdańsk on Hotspot). No number quoted in MODULE-1.md moved.

## Numbers in MODULE-1.md corrected on recheck (not caused by the loader)

In round 3 these four were added up from rounded cell values read off Figure 2. They are now computed directly (`cells.py`, `cells.txt`):
- Finding 2, flank smoke lines on Sleeping Giant, cells E1/F1/G1/G2: 32% -> 33% (46 of 141)
- Finding 2, cap sitters on Sleeping Giant, cells F5/F6/G6: 29% -> 30% (26 of 87)
- Finding 2, Daring on Land of Fire, cells F5/F6: 49% -> 48% (15 of 31)
- Finding 2, Somers on Land of Fire, cells G1/F1: 37% -> 36% (8 of 22)

## Numbers that changed in tables and figures only (not quoted in MODULE-1.md)

- `tables.txt`: Gearing on Land of Fire busiest cell F3 14% -> 18%, cells used 17 -> 16; Gdańsk on Hotspot third cell G6 13% -> G4 13%, cells used 12 -> 11.
- `tables.txt`: Gearing "how far up the map" Top 6 minus Rest +3.8 -> +3.9; Gdańsk -0.4 -> -0.3; Gdańsk to C. Colombo profile distance 1.10 -> 1.11.
- Figure 2: flank smoke lines, Land of Fire, cell F3 9 -> 11; cap sitters, Hotspot, cell F10 11 -> 10.
- Figures 1a and 4: the few moved smokes are drawn at their corrected positions.

## Wording and names

- Cluster names are now exactly: flank smoke lines, cap sitters, parked cruiser smoke, moving exhaust (was "Moving exhaust cover") in MODULE-1.md and in Figures 2 and 3.
- Association wording: headings of findings 2, 3 and 6 and the "For a player" lines of findings 3, 4, 5 and 6 were rewritten to describe what was seen and where, with no claim that a habit or spot wins games.
