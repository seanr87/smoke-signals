"""Write smoke/clans.csv from the inventory: one row per clan with played games.

python -I -X utf8 smoke/tools/make_clan_registry.py [--inventory smoke/inventory.csv] [--out smoke/clans.csv]

Columns: tag, name, group, color, note. The three original clans keep their
colours; the others get fixed colours from a 27-entry palette (nine hues at
three lightness levels) in tag order. An existing file keeps its colours,
names and notes; only missing clans are added.
"""
import argparse
import colorsys
import csv
import os
from collections import Counter

FIXED = {"H-SR": "#F5C542", "RESIN": "#5DADE2", "PN": "#B388FF"}


def palette():
    out = []
    for light in (0.62, 0.48, 0.76):
        for i in range(9):
            r, g, b = colorsys.hls_to_rgb((i * 40 + 15) / 360.0, light, 0.62)
            out.append("#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", default="smoke/inventory.csv")
    ap.add_argument("--out", default="smoke/clans.csv")
    args = ap.parse_args()
    games = Counter()
    group = {}
    for r in csv.DictReader(open(args.inventory, encoding="utf-8")):
        teams = [t.strip() for t in r["teams"].split(" vs ")]
        if r["stage"] == "Groups":
            for t in teams:
                if t not in ("BYE", "COB"):
                    group.setdefault(t, r["group"])
        if r["status"] == "played":
            for t in teams:
                games[t] += 1
    existing = {}
    if os.path.exists(args.out):
        for r in csv.DictReader(open(args.out, encoding="utf-8")):
            existing[r["tag"]] = r
    used = {r["color"] for r in existing.values()} | set(FIXED.values())
    free = [c for c in palette() if c not in used]
    rows = []
    for tag in sorted(games, key=lambda t: t.upper()):
        if tag in existing:
            rows.append(existing[tag])
            continue
        color = FIXED.get(tag) or (free.pop(0) if free else "#94A3B8")
        rows.append({"tag": tag, "name": "", "group": group.get(tag, ""), "color": color, "note": ""})
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tag", "name", "group", "color", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {args.out}: {len(rows)} clans")


if __name__ == "__main__":
    main()
