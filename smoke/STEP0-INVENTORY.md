# STEP 0: full-field inventory (KotS XIX NA)

Source: wows-tournaments.com public match API, match ids 7880..8190 (142 matches found, ids 7885..8183), read on 2026-11-16 with smoke/tools/inventory.py --teams all --no-download. No replays were downloaded. Candidate inventory: smoke/inventory-full-step0.csv (smoke/inventory.csv is unchanged until STEP 1).

Status values: played = result and replay on disk; no replay = result on the site, replay on the site but not yet downloaded; forfeit = a side has the forfeit flag and nothing is on disk; bye = BYE slot in Group 4; not played = series game that was not needed.

## By stage
| stage/group | games listed | played | forfeit | not played | bye | both replays have | both on site | one side only | none on site | to download |
|---|---|---|---|---|---|---|---|---|---|---|
| Groups / Group 1 | 28 | 26 | 2 | 0 | 0 | 7 | 27 | 0 | 1 | 40 |
| Groups / Group 2 | 28 | 20 | 8 | 0 | 0 | 0 | 21 | 0 | 7 | 42 |
| Groups / Group 3 | 28 | 28 | 0 | 0 | 0 | 7 | 28 | 0 | 0 | 42 |
| Groups / Group 4 | 28 | 20 | 1 | 0 | 7 | 6 | 20 | 0 | 1 | 28 |
| Playoffs / Grand Final | 5 | 4 | 0 | 1 | 0 | 4 | 4 | 0 | 0 | 0 |
| Playoffs / Losers Bracket | 42 | 35 | 0 | 7 | 0 | 3 | 34 | 1 | 0 | 63 |
| Playoffs / Winners Bracket | 51 | 36 | 0 | 15 | 0 | 18 | 36 | 0 | 0 | 36 |
| TOTAL | 210 | 169 | 11 | 23 | 7 | 45 | 170 | 1 | 9 | 251 |

replays to download: 251  est size 439 MB at 1.75 MB avg
replays already on disk: 90

## Games with no replay on the site or only one side
- 7958/g1 Groups Group 2 Round 1 COB vs KITE (Hotspot, COB 0 - KITE 0): on site = none; missing = COB;KITE
- 7963/g1 Groups Group 2 Round 2 COB vs MZY (Loop, COB 0 - MZY 0): on site = none; missing = COB;MZY
- 7968/g1 Groups Group 2 Round 3 COB vs RMN (Okinawa, COB 0 - RMN 0): on site = none; missing = COB;RMN
- 7978/g1 Groups Group 1 Round 3 KSC vs HTDOG (Okinawa, KSC 0 - HTDOG 0): on site = none; missing = KSC;HTDOG
- 7944/g1 Groups Group 2 Round 4 REEEE vs COB (Land of Fire, REEEE 0 - COB 0): on site = none; missing = REEEE;COB
- 7947/g1 Groups Group 2 Round 5 5D vs COB (Mountain Range, 5D 0 - COB 0): on site = none; missing = 5D;COB
- 7902/g1 Groups Group 4 Round 5 KM vs EPOXY (Mountain Range, KM 0 - EPOXY 0): on site = none; missing = KM;EPOXY
- 7950/g1 Groups Group 2 Round 6 OGF vs COB (Sleeping Giant, OGF 0 - COB 0): on site = none; missing = OGF;COB
- 7953/g1 Groups Group 2 Round 7 BTLST vs COB (Sea of Fortune, BTLST 0 - COB 0): on site = none; missing = BTLST;COB
- 8141/g3 Playoffs Losers Bracket LB Round 1 KSC vs -BN- (Mountain Range, KSC 0 - -BN- 0): on site = -BN-; missing = KSC

## Clans (played games with a result)
| clan | games | W | L |
|---|---|---|---|
| RESIN | 24 | 17 | 7 |
| H-SR | 22 | 20 | 2 |
| BONKZ | 21 | 13 | 8 |
| MZY | 19 | 12 | 7 |
| HTDOG | 18 | 12 | 6 |
| HFANS | 17 | 10 | 7 |
| EPOXY | 17 | 9 | 8 |
| MACHX | 14 | 8 | 6 |
| KITED | 14 | 7 | 7 |
| -BN- | 14 | 6 | 8 |
| KITE | 13 | 8 | 5 |
| REEEE | 13 | 8 | 5 |
| VRTUS | 11 | 7 | 4 |
| KSC | 11 | 6 | 5 |
| PFANS | 11 | 4 | 7 |
| 5D | 10 | 3 | 7 |
| BONKY | 7 | 3 | 4 |
| PN | 7 | 3 | 4 |
| SCCC2 | 7 | 3 | 4 |
| MACH | 7 | 1 | 6 |
| UYSC | 7 | 1 | 6 |
| NGA | 7 | 0 | 7 |
| RSR | 7 | 0 | 7 |
| BTLST | 6 | 2 | 4 |
| INCA | 6 | 2 | 4 |
| KSE | 6 | 2 | 4 |
| MANBA | 6 | 1 | 5 |
| OGF | 6 | 1 | 5 |
| KM | 5 | 0 | 5 |
| RMN | 5 | 0 | 5 |
clans with games: 30

## Runtime estimate
games with at least one replay on site: 171; runs (one per team per game): 342
no frames: 17 min; with frames: 45 min (scaled from 53 runs = 154 s / about 7 min)

## Maps
Counter({'Sleeping Giant': 33, 'Hotspot': 32, 'Land of Fire': 27, 'Loop': 24, 'Mountain Range': 22, 'Sea of Fortune': 22, 'Okinawa': 20})


## Notes for the next steps

- Every game that was played on the water has at least one replay on the site. The nine games with nothing on the site are walkovers (COB forfeited all seven Group 2 games; KSC vs HTDOG and KM vs EPOXY were also forfeits). Two further games carry a forfeit flag but have scores and replays (KITE 892 vs RMN, KSE 555 vs PFANS 1000); they are counted as forfeits here and will become "played" once their replays are on disk.
- One game has a single replay: Losers Bracket round 1, KSC vs -BN- game 3 (only -BN-'s side). It can be analysed from -BN-'s perspective only.
- Clans: 31 entered (plus the BYE slot), 30 with a played game; COB has none.
- Download: 251 replays, about 440 MB at the current average of 1.75 MB per file (the site refuses HEAD requests, so sizes cannot be read without downloading).
- Runtime: 342 runs (both teams of 171 games), about 17 min without frames and about 45 min with frames at the round 6 rate; clips are extra.
- Code change needed before STEP 2: crates/smoke-signals/src/batch.rs finds a team's primary replay by the suffix "_<slug>.wowsreplay", which turns "-BN-" into "bn" while the site names the file "..._-bn-.wowsreplay"; -BN-'s own runs would be skipped. inventory.py now accepts both spellings; batch.rs needs the same one-line change.
- The id scan covered 7880..8190; the previous run covered 7850..8200 and found the same edges (7885 and 8183).

## Per game

| match | stage | group | round | game | date | map | teams | result | on site | on disk | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7957 | Groups | Group 2 | Round 1 | 1 | 2026-10-17 | Hotspot | BTLST vs REEEE | BTLST 375 - REEEE 1000 | BTLST, REEEE | 0 | no replay |
| 7958 | Groups | Group 2 | Round 1 | 1 | 2026-10-17 | Hotspot | COB vs KITE | COB 0 - KITE 0 |  | 0 | forfeit |
| 7959 | Groups | Group 2 | Round 1 | 1 | 2026-10-17 | Hotspot | RMN vs 5D | RMN 0 - 5D 772 | RMN, 5D | 0 | no replay |
| 7960 | Groups | Group 2 | Round 1 | 1 | 2026-10-17 | Hotspot | OGF vs MZY | OGF 36 - MZY 1000 | OGF, MZY | 0 | no replay |
| 7969 | Groups | Group 1 | Round 1 | 1 | 2026-10-17 | Hotspot | PN vs RSR | PN 1000 - RSR 342 | PN, RSR | 2 | played |
| 7970 | Groups | Group 1 | Round 1 | 1 | 2026-10-17 | Hotspot | UYSC vs KSC | UYSC 339 - KSC 1000 | UYSC, KSC | 0 | no replay |
| 7971 | Groups | Group 1 | Round 1 | 1 | 2026-10-17 | Hotspot | KSE vs PFANS | KSE 555 - PFANS 1000 | KSE, PFANS | 0 | forfeit |
| 7972 | Groups | Group 1 | Round 1 | 1 | 2026-10-17 | Hotspot | VRTUS vs HTDOG | VRTUS 1000 - HTDOG 883 | VRTUS, HTDOG | 0 | no replay |
| 7885 | Groups | Group 4 | Round 1 | 1 | 2026-10-17 | Hotspot | RESIN vs BYE | RESIN 0 - BYE 0 |  | 0 | bye |
| 7886 | Groups | Group 4 | Round 1 | 1 | 2026-10-17 | Hotspot | BONKZ vs MANBA | BONKZ 1000 - MANBA 856 | BONKZ, MANBA | 0 | no replay |
| 7887 | Groups | Group 4 | Round 1 | 1 | 2026-10-17 | Hotspot | EPOXY vs HFANS | EPOXY 1000 - HFANS 784 | EPOXY, HFANS | 0 | no replay |
| 7888 | Groups | Group 4 | Round 1 | 1 | 2026-10-17 | Hotspot | INCA vs KM | INCA 1000 - KM 370 | INCA, KM | 0 | no replay |
| 7913 | Groups | Group 3 | Round 1 | 1 | 2026-10-17 | Hotspot | KITED vs MACH | KITED 831 - MACH 462 | KITED, MACH | 0 | no replay |
| 7914 | Groups | Group 3 | Round 1 | 1 | 2026-10-17 | Hotspot | -BN- vs MACHX | -BN- 790 - MACHX 1000 | -BN-, MACHX | 0 | no replay |
| 7915 | Groups | Group 3 | Round 1 | 1 | 2026-10-17 | Hotspot | H-SR vs NGA | H-SR 1000 - NGA 348 | H-SR, NGA | 2 | played |
| 7916 | Groups | Group 3 | Round 1 | 1 | 2026-10-17 | Hotspot | SCCC2 vs BONKY | SCCC2 1000 - BONKY 865 | SCCC2, BONKY | 0 | no replay |
| 7961 | Groups | Group 2 | Round 2 | 1 | 2026-10-17 | Loop | BTLST vs KITE | BTLST 0 - KITE 604 | BTLST, KITE | 0 | no replay |
| 7962 | Groups | Group 2 | Round 2 | 1 | 2026-10-17 | Loop | REEEE vs 5D | REEEE 624 - 5D 0 | REEEE, 5D | 0 | no replay |
| 7963 | Groups | Group 2 | Round 2 | 1 | 2026-10-17 | Loop | COB vs MZY | COB 0 - MZY 0 |  | 0 | forfeit |
| 7964 | Groups | Group 2 | Round 2 | 1 | 2026-10-17 | Loop | RMN vs OGF | RMN 144 - OGF 512 | RMN, OGF | 0 | no replay |
| 7973 | Groups | Group 1 | Round 2 | 1 | 2026-10-17 | Loop | PN vs KSC | PN 92 - KSC 756 | PN, KSC | 2 | played |
| 7974 | Groups | Group 1 | Round 2 | 1 | 2026-10-17 | Loop | RSR vs PFANS | RSR 0 - PFANS 432 | RSR, PFANS | 0 | no replay |
| 7975 | Groups | Group 1 | Round 2 | 1 | 2026-10-17 | Loop | UYSC vs HTDOG | UYSC 0 - HTDOG 484 | UYSC, HTDOG | 0 | no replay |
| 7976 | Groups | Group 1 | Round 2 | 1 | 2026-10-17 | Loop | KSE vs VRTUS | KSE 68 - VRTUS 744 | KSE, VRTUS | 0 | no replay |
| 7889 | Groups | Group 4 | Round 2 | 1 | 2026-10-17 | Loop | RESIN vs MANBA | RESIN 960 - MANBA 0 | RESIN, MANBA | 2 | played |
| 7890 | Groups | Group 4 | Round 2 | 1 | 2026-10-17 | Loop | BYE vs HFANS | BYE 0 - HFANS 0 |  | 0 | bye |
| 7891 | Groups | Group 4 | Round 2 | 1 | 2026-10-17 | Loop | BONKZ vs KM | BONKZ 700 - KM 0 | BONKZ, KM | 0 | no replay |
| 7892 | Groups | Group 4 | Round 2 | 1 | 2026-10-17 | Loop | EPOXY vs INCA | EPOXY 1000 - INCA 40 | EPOXY, INCA | 0 | no replay |
| 7917 | Groups | Group 3 | Round 2 | 1 | 2026-10-17 | Loop | KITED vs MACHX | KITED 1000 - MACHX 108 | KITED, MACHX | 0 | no replay |
| 7918 | Groups | Group 3 | Round 2 | 1 | 2026-10-17 | Loop | MACH vs NGA | MACH 828 - NGA 0 | MACH, NGA | 0 | no replay |
| 7919 | Groups | Group 3 | Round 2 | 1 | 2026-10-17 | Loop | -BN- vs BONKY | -BN- 352 - BONKY 828 | -BN-, BONKY | 0 | no replay |
| 7920 | Groups | Group 3 | Round 2 | 1 | 2026-10-17 | Loop | H-SR vs SCCC2 | H-SR 840 - SCCC2 600 | H-SR, SCCC2 | 2 | played |
| 7965 | Groups | Group 2 | Round 3 | 1 | 2026-10-17 | Okinawa | BTLST vs 5D | BTLST 617 - 5D 1000 | BTLST, 5D | 0 | no replay |
| 7966 | Groups | Group 2 | Round 3 | 1 | 2026-10-17 | Okinawa | KITE vs MZY | KITE 453 - MZY 779 | KITE, MZY | 0 | no replay |
| 7967 | Groups | Group 2 | Round 3 | 1 | 2026-10-17 | Okinawa | REEEE vs OGF | REEEE 1000 - OGF 128 | REEEE, OGF | 0 | no replay |
| 7968 | Groups | Group 2 | Round 3 | 1 | 2026-10-17 | Okinawa | COB vs RMN | COB 0 - RMN 0 |  | 0 | forfeit |
| 7977 | Groups | Group 1 | Round 3 | 1 | 2026-10-17 | Okinawa | PN vs PFANS | PN 46 - PFANS 1000 | PN, PFANS | 2 | played |
| 7978 | Groups | Group 1 | Round 3 | 1 | 2026-10-17 | Okinawa | KSC vs HTDOG | KSC 0 - HTDOG 0 |  | 0 | forfeit |
| 7979 | Groups | Group 1 | Round 3 | 1 | 2026-10-17 | Okinawa | RSR vs VRTUS | RSR 72 - VRTUS 1000 | RSR, VRTUS | 0 | no replay |
| 7980 | Groups | Group 1 | Round 3 | 1 | 2026-10-17 | Okinawa | UYSC vs KSE | UYSC 0 - KSE 522 | UYSC, KSE | 0 | no replay |
| 7893 | Groups | Group 4 | Round 3 | 1 | 2026-10-17 | Okinawa | RESIN vs HFANS | RESIN 851 - HFANS 90 | RESIN, HFANS | 2 | played |
| 7894 | Groups | Group 4 | Round 3 | 1 | 2026-10-17 | Okinawa | MANBA vs KM | MANBA 1000 - KM 352 | MANBA, KM | 0 | no replay |
| 7895 | Groups | Group 4 | Round 3 | 1 | 2026-10-17 | Okinawa | BYE vs INCA | BYE 0 - INCA 0 |  | 0 | bye |
| 7896 | Groups | Group 4 | Round 3 | 1 | 2026-10-17 | Okinawa | BONKZ vs EPOXY | BONKZ 1000 - EPOXY 875 | BONKZ, EPOXY | 0 | no replay |
| 7921 | Groups | Group 3 | Round 3 | 1 | 2026-10-17 | Okinawa | KITED vs NGA | KITED 1000 - NGA 536 | KITED, NGA | 0 | no replay |
| 7922 | Groups | Group 3 | Round 3 | 1 | 2026-10-17 | Okinawa | MACHX vs BONKY | MACHX 1000 - BONKY 363 | MACHX, BONKY | 0 | no replay |
| 7923 | Groups | Group 3 | Round 3 | 1 | 2026-10-17 | Okinawa | MACH vs SCCC2 | MACH 0 - SCCC2 963 | MACH, SCCC2 | 0 | no replay |
| 7924 | Groups | Group 3 | Round 3 | 1 | 2026-10-17 | Okinawa | -BN- vs H-SR | -BN- 0 - H-SR 778 | -BN-, H-SR | 2 | played |
| 7941 | Groups | Group 2 | Round 4 | 1 | 2026-10-17 | Land of Fire | BTLST vs MZY | BTLST 236 - MZY 1000 | BTLST, MZY | 0 | no replay |
| 7942 | Groups | Group 2 | Round 4 | 1 | 2026-10-17 | Land of Fire | 5D vs OGF | 5D 1000 - OGF 397 | 5D, OGF | 0 | no replay |
| 7943 | Groups | Group 2 | Round 4 | 1 | 2026-10-17 | Land of Fire | KITE vs RMN | KITE 892 - RMN 0 | KITE, RMN | 0 | forfeit |
| 7944 | Groups | Group 2 | Round 4 | 1 | 2026-10-17 | Land of Fire | REEEE vs COB | REEEE 0 - COB 0 |  | 0 | forfeit |
| 7981 | Groups | Group 1 | Round 4 | 1 | 2026-10-17 | Land of Fire | PN vs HTDOG | PN 312 - HTDOG 1000 | PN, HTDOG | 2 | played |
| 7982 | Groups | Group 1 | Round 4 | 1 | 2026-10-17 | Land of Fire | PFANS vs VRTUS | PFANS 536 - VRTUS 1000 | PFANS, VRTUS | 0 | no replay |
| 7983 | Groups | Group 1 | Round 4 | 1 | 2026-10-17 | Land of Fire | KSC vs KSE | KSC 1000 - KSE 476 | KSC, KSE | 0 | no replay |
| 7984 | Groups | Group 1 | Round 4 | 1 | 2026-10-17 | Land of Fire | RSR vs UYSC | RSR 0 - UYSC 640 | RSR, UYSC | 0 | no replay |
| 7897 | Groups | Group 4 | Round 4 | 1 | 2026-10-17 | Land of Fire | RESIN vs KM | RESIN 969 - KM 139 | RESIN, KM | 2 | played |
| 7898 | Groups | Group 4 | Round 4 | 1 | 2026-10-17 | Land of Fire | HFANS vs INCA | HFANS 1000 - INCA 512 | HFANS, INCA | 0 | no replay |
| 7899 | Groups | Group 4 | Round 4 | 1 | 2026-10-17 | Land of Fire | MANBA vs EPOXY | MANBA 523 - EPOXY 1000 | MANBA, EPOXY | 0 | no replay |
| 7900 | Groups | Group 4 | Round 4 | 1 | 2026-10-17 | Land of Fire | BYE vs BONKZ | BYE 0 - BONKZ 0 |  | 0 | bye |
| 7925 | Groups | Group 3 | Round 4 | 1 | 2026-10-17 | Land of Fire | KITED vs BONKY | KITED 1000 - BONKY 522 | KITED, BONKY | 0 | no replay |
| 7926 | Groups | Group 3 | Round 4 | 1 | 2026-10-17 | Land of Fire | NGA vs SCCC2 | NGA 781 - SCCC2 1000 | NGA, SCCC2 | 0 | no replay |
| 7927 | Groups | Group 3 | Round 4 | 1 | 2026-10-17 | Land of Fire | MACHX vs H-SR | MACHX 453 - H-SR 1000 | MACHX, H-SR | 2 | played |
| 7928 | Groups | Group 3 | Round 4 | 1 | 2026-10-17 | Land of Fire | MACH vs -BN- | MACH 496 - -BN- 1000 | MACH, -BN- | 0 | no replay |
| 7945 | Groups | Group 2 | Round 5 | 1 | 2026-10-17 | Mountain Range | BTLST vs OGF | BTLST 700 - OGF 0 | BTLST, OGF | 0 | no replay |
| 7946 | Groups | Group 2 | Round 5 | 1 | 2026-10-17 | Mountain Range | MZY vs RMN | MZY 776 - RMN 0 | MZY, RMN | 0 | no replay |
| 7947 | Groups | Group 2 | Round 5 | 1 | 2026-10-17 | Mountain Range | 5D vs COB | 5D 0 - COB 0 |  | 0 | forfeit |
| 7948 | Groups | Group 2 | Round 5 | 1 | 2026-10-17 | Mountain Range | KITE vs REEEE | KITE 1000 - REEEE 52 | KITE, REEEE | 0 | no replay |
| 7985 | Groups | Group 1 | Round 5 | 1 | 2026-10-17 | Mountain Range | PN vs VRTUS | PN 0 - VRTUS 500 | PN, VRTUS | 2 | played |
| 7986 | Groups | Group 1 | Round 5 | 1 | 2026-10-17 | Mountain Range | HTDOG vs KSE | HTDOG 652 - KSE 0 | HTDOG, KSE | 0 | no replay |
| 7987 | Groups | Group 1 | Round 5 | 1 | 2026-10-17 | Mountain Range | PFANS vs UYSC | PFANS 812 - UYSC 0 | PFANS, UYSC | 0 | no replay |
| 7988 | Groups | Group 1 | Round 5 | 1 | 2026-10-17 | Mountain Range | KSC vs RSR | KSC 724 - RSR 0 | KSC, RSR | 0 | no replay |
| 7901 | Groups | Group 4 | Round 5 | 1 | 2026-10-17 | Mountain Range | RESIN vs INCA | RESIN 740 - INCA 304 | RESIN, INCA | 2 | played |
| 7902 | Groups | Group 4 | Round 5 | 1 | 2026-10-17 | Mountain Range | KM vs EPOXY | KM 0 - EPOXY 0 |  | 0 | forfeit |
| 7903 | Groups | Group 4 | Round 5 | 1 | 2026-10-17 | Mountain Range | HFANS vs BONKZ | HFANS 692 - BONKZ 0 | HFANS, BONKZ | 0 | no replay |
| 7904 | Groups | Group 4 | Round 5 | 1 | 2026-10-17 | Mountain Range | MANBA vs BYE | MANBA 0 - BYE 0 |  | 0 | bye |
| 7929 | Groups | Group 3 | Round 5 | 1 | 2026-10-17 | Mountain Range | KITED vs SCCC2 | KITED 868 - SCCC2 24 | KITED, SCCC2 | 0 | no replay |
| 7930 | Groups | Group 3 | Round 5 | 1 | 2026-10-17 | Mountain Range | BONKY vs H-SR | BONKY 0 - H-SR 580 | BONKY, H-SR | 2 | played |
| 7931 | Groups | Group 3 | Round 5 | 1 | 2026-10-17 | Mountain Range | NGA vs -BN- | NGA 0 - -BN- 648 | NGA, -BN- | 0 | no replay |
| 7932 | Groups | Group 3 | Round 5 | 1 | 2026-10-17 | Mountain Range | MACHX vs MACH | MACHX 604 - MACH 0 | MACHX, MACH | 0 | no replay |
| 7949 | Groups | Group 2 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | BTLST vs RMN | BTLST 1000 - RMN 356 | BTLST, RMN | 0 | no replay |
| 7950 | Groups | Group 2 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | OGF vs COB | OGF 0 - COB 0 |  | 0 | forfeit |
| 7951 | Groups | Group 2 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | MZY vs REEEE | MZY 646 - REEEE 1000 | MZY, REEEE | 0 | no replay |
| 7952 | Groups | Group 2 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | 5D vs KITE | 5D 633 - KITE 1000 | 5D, KITE | 0 | no replay |
| 7989 | Groups | Group 1 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | PN vs KSE | PN 1000 - KSE 464 | PN, KSE | 2 | played |
| 7990 | Groups | Group 1 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | VRTUS vs UYSC | VRTUS 1000 - UYSC 450 | VRTUS, UYSC | 0 | no replay |
| 7991 | Groups | Group 1 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | HTDOG vs RSR | HTDOG 1000 - RSR 290 | HTDOG, RSR | 0 | no replay |
| 7992 | Groups | Group 1 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | PFANS vs KSC | PFANS 941 - KSC 1000 | PFANS, KSC | 0 | no replay |
| 7905 | Groups | Group 4 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | RESIN vs EPOXY | RESIN 1000 - EPOXY 439 | RESIN, EPOXY | 2 | played |
| 7906 | Groups | Group 4 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | INCA vs BONKZ | INCA 316 - BONKZ 1000 | INCA, BONKZ | 0 | no replay |
| 7907 | Groups | Group 4 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | KM vs BYE | KM 0 - BYE 0 |  | 0 | bye |
| 7908 | Groups | Group 4 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | HFANS vs MANBA | HFANS 1000 - MANBA 378 | HFANS, MANBA | 0 | no replay |
| 7933 | Groups | Group 3 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | KITED vs H-SR | KITED 177 - H-SR 1000 | KITED, H-SR | 2 | played |
| 7934 | Groups | Group 3 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | SCCC2 vs -BN- | SCCC2 571 - -BN- 1000 | SCCC2, -BN- | 0 | no replay |
| 7935 | Groups | Group 3 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | BONKY vs MACH | BONKY 1000 - MACH 859 | BONKY, MACH | 0 | no replay |
| 7936 | Groups | Group 3 | Round 6 | 1 | 2026-10-17 | Sleeping Giant | NGA vs MACHX | NGA 576 - MACHX 1000 | NGA, MACHX | 0 | no replay |
| 7953 | Groups | Group 2 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | BTLST vs COB | BTLST 0 - COB 0 |  | 0 | forfeit |
| 7954 | Groups | Group 2 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | RMN vs REEEE | RMN 140 - REEEE 1000 | RMN, REEEE | 0 | no replay |
| 7955 | Groups | Group 2 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | OGF vs KITE | OGF 50 - KITE 1000 | OGF, KITE | 0 | no replay |
| 7956 | Groups | Group 2 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | MZY vs 5D | MZY 1000 - 5D 30 | MZY, 5D | 0 | no replay |
| 7993 | Groups | Group 1 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | PN vs UYSC | PN 1000 - UYSC 297 | PN, UYSC | 2 | played |
| 7994 | Groups | Group 1 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | KSE vs RSR | KSE 983 - RSR 361 | KSE, RSR | 0 | no replay |
| 7995 | Groups | Group 1 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | VRTUS vs KSC | VRTUS 1000 - KSC 648 | VRTUS, KSC | 0 | no replay |
| 7996 | Groups | Group 1 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | HTDOG vs PFANS | HTDOG 1000 - PFANS 305 | HTDOG, PFANS | 0 | no replay |
| 7909 | Groups | Group 4 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | RESIN vs BONKZ | RESIN 1000 - BONKZ 441 | RESIN, BONKZ | 2 | played |
| 7910 | Groups | Group 4 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | EPOXY vs BYE | EPOXY 0 - BYE 0 |  | 0 | bye |
| 7911 | Groups | Group 4 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | INCA vs MANBA | INCA 1000 - MANBA 32 | INCA, MANBA | 0 | no replay |
| 7912 | Groups | Group 4 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | KM vs HFANS | KM 363 - HFANS 953 | KM, HFANS | 0 | no replay |
| 7937 | Groups | Group 3 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | KITED vs -BN- | KITED 500 - -BN- 1000 | KITED, -BN- | 0 | no replay |
| 7938 | Groups | Group 3 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | H-SR vs MACH | H-SR 512 - MACH 343 | H-SR, MACH | 2 | played |
| 7939 | Groups | Group 3 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | SCCC2 vs MACHX | SCCC2 846 - MACHX 1000 | SCCC2, MACHX | 0 | no replay |
| 7940 | Groups | Group 3 | Round 7 | 1 | 2026-10-17 | Sea of Fortune | BONKY vs NGA | BONKY 1000 - NGA 292 | BONKY, NGA | 0 | no replay |
| 8067 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Hotspot | VRTUS vs BONKZ | VRTUS 666 - BONKZ 1000 | VRTUS, BONKZ | 0 | no replay |
| 8067 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Sleeping Giant | VRTUS vs BONKZ | VRTUS 306 - BONKZ 1000 | VRTUS, BONKZ | 0 | no replay |
| 8067 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Mountain Range | VRTUS vs BONKZ |  |  | 0 | not played |
| 8068 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Loop | MZY vs MACHX | MZY 244 - MACHX 748 | MZY, MACHX | 0 | no replay |
| 8068 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Sleeping Giant | MZY vs MACHX | MZY 1000 - MACHX 860 | MZY, MACHX | 0 | no replay |
| 8068 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Hotspot | MZY vs MACHX | MZY 1000 - MACHX 842 | MZY, MACHX | 0 | no replay |
| 8069 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Sleeping Giant | RESIN vs PFANS | RESIN 1000 - PFANS 815 | RESIN, PFANS | 2 | played |
| 8069 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Mountain Range | RESIN vs PFANS | RESIN 684 - PFANS 0 | RESIN, PFANS | 2 | played |
| 8069 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Land of Fire | RESIN vs PFANS |  |  | 0 | not played |
| 8070 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Hotspot | KITED vs REEEE | KITED 507 - REEEE 1000 | KITED, REEEE | 0 | no replay |
| 8070 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Loop | KITED vs REEEE | KITED 256 - REEEE 560 | KITED, REEEE | 0 | no replay |
| 8070 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Sleeping Giant | KITED vs REEEE |  |  | 0 | not played |
| 8071 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Land of Fire | KITE vs -BN- | KITE 1000 - -BN- 890 | KITE, -BN- | 0 | no replay |
| 8071 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Sleeping Giant | KITE vs -BN- | KITE 1000 - -BN- 827 | KITE, -BN- | 0 | no replay |
| 8071 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Mountain Range | KITE vs -BN- |  |  | 0 | not played |
| 8072 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Hotspot | EPOXY vs KSC | EPOXY 1000 - KSC 424 | EPOXY, KSC | 0 | no replay |
| 8072 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Land of Fire | EPOXY vs KSC | EPOXY 1000 - KSC 686 | EPOXY, KSC | 0 | no replay |
| 8072 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Okinawa | EPOXY vs KSC |  |  | 0 | not played |
| 8073 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Hotspot | H-SR vs 5D | H-SR 1000 - 5D 537 | H-SR, 5D | 2 | played |
| 8073 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Land of Fire | H-SR vs 5D | H-SR 915 - 5D 221 | H-SR, 5D | 2 | played |
| 8073 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Mountain Range | H-SR vs 5D |  |  | 0 | not played |
| 8074 | Playoffs | Winners Bracket | WB Round 1 | 1 | 2026-10-18 | Okinawa | HTDOG vs HFANS | HTDOG 674 - HFANS 932 | HTDOG, HFANS | 0 | no replay |
| 8074 | Playoffs | Winners Bracket | WB Round 1 | 2 | 2026-10-18 | Land of Fire | HTDOG vs HFANS | HTDOG 1000 - HFANS 568 | HTDOG, HFANS | 0 | no replay |
| 8074 | Playoffs | Winners Bracket | WB Round 1 | 3 | 2026-10-18 | Sleeping Giant | HTDOG vs HFANS | HTDOG 1000 - HFANS 642 | HTDOG, HFANS | 0 | no replay |
| 8139 | Playoffs | Losers Bracket | LB Round 1 | 1 | 2026-10-18 | Loop | KITED vs PFANS | KITED 12 - PFANS 732 | KITED, PFANS | 0 | no replay |
| 8139 | Playoffs | Losers Bracket | LB Round 1 | 2 | 2026-10-18 | Hotspot | KITED vs PFANS | KITED 1000 - PFANS 784 | KITED, PFANS | 0 | no replay |
| 8139 | Playoffs | Losers Bracket | LB Round 1 | 3 | 2026-10-18 | Sleeping Giant | KITED vs PFANS | KITED 1000 - PFANS 628 | KITED, PFANS | 0 | no replay |
| 8140 | Playoffs | Winners Bracket | WB Round 2 | 1 | 2026-10-18 | Hotspot | RESIN vs REEEE | RESIN 1000 - REEEE 457 | RESIN, REEEE | 2 | played |
| 8140 | Playoffs | Winners Bracket | WB Round 2 | 2 | 2026-10-18 | Sleeping Giant | RESIN vs REEEE | RESIN 1000 - REEEE 61 | RESIN, REEEE | 2 | played |
| 8140 | Playoffs | Winners Bracket | WB Round 2 | 3 | 2026-10-18 | Loop | RESIN vs REEEE |  |  | 0 | not played |
| 8141 | Playoffs | Losers Bracket | LB Round 1 | 1 | 2026-10-18 | Sleeping Giant | KSC vs -BN- | KSC 941 - -BN- 1000 | KSC, -BN- | 0 | no replay |
| 8141 | Playoffs | Losers Bracket | LB Round 1 | 2 | 2026-10-18 | Hotspot | KSC vs -BN- | KSC 1000 - -BN- 815 | KSC, -BN- | 0 | no replay |
| 8141 | Playoffs | Losers Bracket | LB Round 1 | 3 | 2026-10-18 | Mountain Range | KSC vs -BN- | KSC 0 - -BN- 0 | -BN- | 0 | no replay |
| 8142 | Playoffs | Winners Bracket | WB Round 2 | 1 | 2026-10-18 | Sea of Fortune | KITE vs EPOXY | KITE 488 - EPOXY 1000 | KITE, EPOXY | 0 | no replay |
| 8142 | Playoffs | Winners Bracket | WB Round 2 | 2 | 2026-10-18 | Hotspot | KITE vs EPOXY | KITE 634 - EPOXY 1000 | KITE, EPOXY | 0 | no replay |
| 8142 | Playoffs | Winners Bracket | WB Round 2 | 3 | 2026-10-18 | Loop | KITE vs EPOXY |  |  | 0 | not played |
| 8143 | Playoffs | Losers Bracket | LB Round 1 | 1 | 2026-10-18 | Sea of Fortune | MACHX vs VRTUS | MACHX 1000 - VRTUS 922 | MACHX, VRTUS | 0 | no replay |
| 8143 | Playoffs | Losers Bracket | LB Round 1 | 2 | 2026-10-18 | Land of Fire | MACHX vs VRTUS | MACHX 1000 - VRTUS 687 | MACHX, VRTUS | 0 | no replay |
| 8143 | Playoffs | Losers Bracket | LB Round 1 | 3 | 2026-10-18 | Sleeping Giant | MACHX vs VRTUS |  |  | 0 | not played |
| 8144 | Playoffs | Winners Bracket | WB Round 2 | 1 | 2026-10-18 | Hotspot | BONKZ vs MZY | BONKZ 1000 - MZY 758 | BONKZ, MZY | 0 | no replay |
| 8144 | Playoffs | Winners Bracket | WB Round 2 | 2 | 2026-10-18 | Sea of Fortune | BONKZ vs MZY | BONKZ 1000 - MZY 332 | BONKZ, MZY | 0 | no replay |
| 8144 | Playoffs | Winners Bracket | WB Round 2 | 3 | 2026-10-18 | Sleeping Giant | BONKZ vs MZY |  |  | 0 | not played |
| 8145 | Playoffs | Losers Bracket | LB Round 1 | 1 | 2026-10-18 | Sleeping Giant | HFANS vs 5D | HFANS 1000 - 5D 186 | HFANS, 5D | 0 | no replay |
| 8145 | Playoffs | Losers Bracket | LB Round 1 | 2 | 2026-10-18 | Land of Fire | HFANS vs 5D | HFANS 1000 - 5D 190 | HFANS, 5D | 0 | no replay |
| 8145 | Playoffs | Losers Bracket | LB Round 1 | 3 | 2026-10-18 | Okinawa | HFANS vs 5D |  |  | 0 | not played |
| 8146 | Playoffs | Winners Bracket | WB Round 2 | 1 | 2026-10-18 | Sea of Fortune | H-SR vs HTDOG | H-SR 1000 - HTDOG 899 | H-SR, HTDOG | 2 | played |
| 8146 | Playoffs | Winners Bracket | WB Round 2 | 2 | 2026-10-18 | Mountain Range | H-SR vs HTDOG | H-SR 668 - HTDOG 532 | H-SR, HTDOG | 2 | played |
| 8146 | Playoffs | Winners Bracket | WB Round 2 | 3 | 2026-10-18 | Sleeping Giant | H-SR vs HTDOG |  |  | 0 | not played |
| 8148 | Playoffs | Losers Bracket | LB Round 2 | 1 | 2026-10-18 | Loop | REEEE vs HFANS | REEEE 1000 - HFANS 104 | REEEE, HFANS | 0 | no replay |
| 8148 | Playoffs | Losers Bracket | LB Round 2 | 2 | 2026-10-18 | Hotspot | REEEE vs HFANS | REEEE 718 - HFANS 1000 | REEEE, HFANS | 0 | no replay |
| 8148 | Playoffs | Losers Bracket | LB Round 2 | 3 | 2026-10-18 | Okinawa | REEEE vs HFANS | REEEE 456 - HFANS 1000 | REEEE, HFANS | 0 | no replay |
| 8149 | Playoffs | Losers Bracket | LB Round 2 | 1 | 2026-10-18 | Mountain Range | KITE vs MACHX | KITE 720 - MACHX 312 | KITE, MACHX | 0 | no replay |
| 8149 | Playoffs | Losers Bracket | LB Round 2 | 2 | 2026-10-18 | Land of Fire | KITE vs MACHX | KITE 1000 - MACHX 705 | KITE, MACHX | 0 | no replay |
| 8149 | Playoffs | Losers Bracket | LB Round 2 | 3 | 2026-10-18 | Okinawa | KITE vs MACHX |  |  | 0 | not played |
| 8150 | Playoffs | Losers Bracket | LB Round 2 | 1 | 2026-10-18 | Loop | HTDOG vs KITED | HTDOG 860 - KITED 0 | HTDOG, KITED | 0 | no replay |
| 8150 | Playoffs | Losers Bracket | LB Round 2 | 2 | 2026-10-18 | Sleeping Giant | HTDOG vs KITED | HTDOG 1000 - KITED 471 | HTDOG, KITED | 0 | no replay |
| 8150 | Playoffs | Losers Bracket | LB Round 2 | 3 | 2026-10-18 | Mountain Range | HTDOG vs KITED |  |  | 0 | not played |
| 8152 | Playoffs | Losers Bracket | LB Round 2 | 1 | 2026-10-18 | Okinawa | MZY vs -BN- | MZY 866 - -BN- 366 | MZY, -BN- | 0 | no replay |
| 8152 | Playoffs | Losers Bracket | LB Round 2 | 2 | 2026-10-18 | Land of Fire | MZY vs -BN- | MZY 1000 - -BN- 953 | MZY, -BN- | 0 | no replay |
| 8152 | Playoffs | Losers Bracket | LB Round 2 | 3 | 2026-10-18 | Sea of Fortune | MZY vs -BN- |  |  | 0 | not played |
| 8147 | Playoffs | Winners Bracket | WB Round 3 | 1 | 2026-10-24 | Sleeping Giant | BONKZ vs RESIN | BONKZ 851 - RESIN 1000 | BONKZ, RESIN | 2 | played |
| 8147 | Playoffs | Winners Bracket | WB Round 3 | 2 | 2026-10-24 | Mountain Range | BONKZ vs RESIN | BONKZ 312 - RESIN 808 | BONKZ, RESIN | 2 | played |
| 8147 | Playoffs | Winners Bracket | WB Round 3 | 3 | 2026-10-24 | Land of Fire | BONKZ vs RESIN | BONKZ 660 - RESIN 1000 | BONKZ, RESIN | 2 | played |
| 8147 | Playoffs | Winners Bracket | WB Round 3 | 4 | 2026-10-24 | Hotspot | BONKZ vs RESIN |  |  | 0 | not played |
| 8147 | Playoffs | Winners Bracket | WB Round 3 | 5 | 2026-10-24 | Sea of Fortune | BONKZ vs RESIN |  |  | 0 | not played |
| 8151 | Playoffs | Winners Bracket | WB Round 3 | 1 | 2026-10-24 | Sleeping Giant | EPOXY vs H-SR | EPOXY 655 - H-SR 1000 | EPOXY, H-SR | 2 | played |
| 8151 | Playoffs | Winners Bracket | WB Round 3 | 2 | 2026-10-24 | Sea of Fortune | EPOXY vs H-SR | EPOXY 480 - H-SR 1000 | EPOXY, H-SR | 2 | played |
| 8151 | Playoffs | Winners Bracket | WB Round 3 | 3 | 2026-10-24 | Hotspot | EPOXY vs H-SR | EPOXY 594 - H-SR 1000 | EPOXY, H-SR | 2 | played |
| 8151 | Playoffs | Winners Bracket | WB Round 3 | 4 | 2026-10-24 | Loop | EPOXY vs H-SR |  |  | 0 | not played |
| 8151 | Playoffs | Winners Bracket | WB Round 3 | 5 | 2026-10-24 | Land of Fire | EPOXY vs H-SR |  |  | 0 | not played |
| 8153 | Playoffs | Losers Bracket | LB Round 3 | 1 | 2026-10-24 | Sleeping Giant | HTDOG vs KITE | HTDOG 1000 - KITE 471 | HTDOG, KITE | 0 | no replay |
| 8153 | Playoffs | Losers Bracket | LB Round 3 | 2 | 2026-10-24 | Mountain Range | HTDOG vs KITE | HTDOG 688 - KITE 0 | HTDOG, KITE | 0 | no replay |
| 8153 | Playoffs | Losers Bracket | LB Round 3 | 3 | 2026-10-24 | Loop | HTDOG vs KITE |  |  | 0 | not played |
| 8154 | Playoffs | Losers Bracket | LB Round 3 | 1 | 2026-10-24 | Land of Fire | HFANS vs MZY | HFANS 1000 - MZY 542 | HFANS, MZY | 0 | no replay |
| 8154 | Playoffs | Losers Bracket | LB Round 3 | 2 | 2026-10-24 | Okinawa | HFANS vs MZY | HFANS 315 - MZY 926 | HFANS, MZY | 0 | no replay |
| 8154 | Playoffs | Losers Bracket | LB Round 3 | 3 | 2026-10-24 | Sea of Fortune | HFANS vs MZY | HFANS 571 - MZY 1000 | HFANS, MZY | 0 | no replay |
| 8174 | Playoffs | Losers Bracket | LB Round 4 | 1 | 2026-10-24 | Hotspot | EPOXY vs MZY | EPOXY 1000 - MZY 847 | EPOXY, MZY | 0 | no replay |
| 8174 | Playoffs | Losers Bracket | LB Round 4 | 2 | 2026-10-24 | Okinawa | EPOXY vs MZY | EPOXY 484 - MZY 1000 | EPOXY, MZY | 0 | no replay |
| 8174 | Playoffs | Losers Bracket | LB Round 4 | 3 | 2026-10-24 | Loop | EPOXY vs MZY | EPOXY 760 - MZY 4 | EPOXY, MZY | 0 | no replay |
| 8175 | Playoffs | Losers Bracket | LB Round 4 | 1 | 2026-10-24 | Sleeping Giant | BONKZ vs HTDOG | BONKZ 754 - HTDOG 1000 | BONKZ, HTDOG | 0 | no replay |
| 8175 | Playoffs | Losers Bracket | LB Round 4 | 2 | 2026-10-24 | Loop | BONKZ vs HTDOG | BONKZ 1000 - HTDOG 28 | BONKZ, HTDOG | 0 | no replay |
| 8175 | Playoffs | Losers Bracket | LB Round 4 | 3 | 2026-10-24 | Mountain Range | BONKZ vs HTDOG | BONKZ 624 - HTDOG 268 | BONKZ, HTDOG | 0 | no replay |
| 8176 | Playoffs | Winners Bracket | WB Round 4 | 1 | 2026-10-24 | Sleeping Giant | RESIN vs H-SR | RESIN 703 - H-SR 1000 | RESIN, H-SR | 2 | played |
| 8176 | Playoffs | Winners Bracket | WB Round 4 | 2 | 2026-10-24 | Hotspot | RESIN vs H-SR | RESIN 699 - H-SR 1000 | RESIN, H-SR | 2 | played |
| 8176 | Playoffs | Winners Bracket | WB Round 4 | 3 | 2026-10-24 | Land of Fire | RESIN vs H-SR | RESIN 1000 - H-SR 579 | RESIN, H-SR | 2 | played |
| 8176 | Playoffs | Winners Bracket | WB Round 4 | 4 | 2026-10-24 | Loop | RESIN vs H-SR | RESIN 192 - H-SR 756 | RESIN, H-SR | 2 | played |
| 8176 | Playoffs | Winners Bracket | WB Round 4 | 5 | 2026-10-24 | Sea of Fortune | RESIN vs H-SR |  |  | 0 | not played |
| 8177 | Playoffs | Losers Bracket | LB Round 5 | 1 | 2026-10-24 | Sleeping Giant | EPOXY vs BONKZ | EPOXY 433 - BONKZ 1000 | EPOXY, BONKZ | 0 | no replay |
| 8177 | Playoffs | Losers Bracket | LB Round 5 | 2 | 2026-10-24 | Hotspot | EPOXY vs BONKZ | EPOXY 702 - BONKZ 1000 | EPOXY, BONKZ | 0 | no replay |
| 8177 | Playoffs | Losers Bracket | LB Round 5 | 3 | 2026-10-24 | Sea of Fortune | EPOXY vs BONKZ |  |  | 0 | not played |
| 8178 | Playoffs | Losers Bracket | LB Round 6 | 1 | 2026-10-25 | Sleeping Giant | RESIN vs BONKZ | RESIN 1000 - BONKZ 802 | RESIN, BONKZ | 2 | played |
| 8178 | Playoffs | Losers Bracket | LB Round 6 | 2 | 2026-10-25 | Hotspot | RESIN vs BONKZ | RESIN 732 - BONKZ 1000 | RESIN, BONKZ | 2 | played |
| 8178 | Playoffs | Losers Bracket | LB Round 6 | 3 | 2026-10-25 | Sea of Fortune | RESIN vs BONKZ | RESIN 1000 - BONKZ 726 | RESIN, BONKZ | 2 | played |
| 8183 | Playoffs | Grand Final | GF Round 1 | 1 | 2026-10-25 | Sleeping Giant | H-SR vs RESIN | H-SR 945 - RESIN 1000 | H-SR, RESIN | 2 | played |
| 8183 | Playoffs | Grand Final | GF Round 1 | 2 | 2026-10-25 | Hotspot | H-SR vs RESIN | H-SR 1000 - RESIN 515 | H-SR, RESIN | 2 | played |
| 8183 | Playoffs | Grand Final | GF Round 1 | 3 | 2026-10-25 | Loop | H-SR vs RESIN | H-SR 1000 - RESIN 40 | H-SR, RESIN | 2 | played |
| 8183 | Playoffs | Grand Final | GF Round 1 | 4 | 2026-10-25 | Land of Fire | H-SR vs RESIN | H-SR 1000 - RESIN 424 | H-SR, RESIN | 2 | played |
| 8183 | Playoffs | Grand Final | GF Round 1 | 5 | 2026-10-25 | Sea of Fortune | H-SR vs RESIN |  |  | 0 | not played |
