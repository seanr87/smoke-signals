"""Export the shareable data set of a batch as one zip.

Usage:
  python -I -X utf8 export_data.py --batch output/<batch> --maps output/<maps>/maps
         [--inventory smoke/inventory.csv] [--out output/<batch>/smoke-signals-data-r6.zip]

The zip holds smokes.csv (the batch's combined table, every field, plus the
profile zone and grid square), games.csv (one row per played game: match,
map, teams, winner, end clock and phase), clans.csv and clans-destroyer.csv
(every Clans chart value with its count, over all smokes and over destroyer
smokes), breakdown.csv (per clan: purpose x movement x coverage x lane with
counts) and ship_class.csv (per clan and smoker class).
"""
import argparse
import csv
import io
import os
import sys
import zipfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_site  # noqa: E402


def games_rows(data):
    rows = []
    for key, r in sorted(data.inventory.items(), key=lambda kv: (kv[1]["date"], kv[1]["stage"], kv[1]["group"], kv[1]["round"], kv[0][1])):
        if r["status"] != "played":
            continue
        g = data.games.get(key) or {}
        end_clock = (g.get("battle_end") or {}).get("clock") or ""
        rem = build_site.clock_remaining_seconds(end_clock)
        elapsed = build_site.MATCH_SECONDS - rem if rem is not None else None
        rows.append({
            "match_id": key[0], "game_no": key[1], "stage": r["stage"], "group": r["group"], "round": r["round"], "date": r["date"],
            "map": r["map"], "teams": r["teams"], "score": r["score"], "winner": r["winner"],
            "end_clock": end_clock, "end_elapsed": build_site.elapsed_text(elapsed) if elapsed is not None else "",
            "end_phase": build_site.phase_of(elapsed) or "" if elapsed is not None else "", "finish_type": g.get("finish_type") or "",
            "smokes_analysed": len(data.by_game.get(key, [])),
            "data_quality": data.game_quality.get(key, ""),
        })
    return rows


METRIC_NAMES = {
    "smokes_per_game": "Smokes per game", "damage_per_game": "Smoke damage per game", "concealed_per_game": "Concealed smoke damage per game",
    "dd_per_game": "DD damage per game", "avg_damage": "Average damage per smoke",
    "uptime": "Smoke uptime (s per game)", "charge": "Charge use (%)", "stacking": "Stacking rate (%)",
    "contested": "Contested-cap share (%)", "selfish": "Selfish smoke share (%)", "swing": "Score swing while smoke up (pts)",
    "punished": "Radar-punished share (%)", "offensive": "Radar spots from smoke (per game)", "kills": "Kills from smoke (per game)",
    "deaths": "Smoke deaths (per game)", "won": "Smokes near a cap capture", "coverage": "Radar cap coverage (mean %)",
    "coverage_full": "Smokes with full radar cap coverage",
}


def clan_rows(site, subset):
    rows = []
    for team in sorted({s["team"] for s in subset}):
        m = site.clan_metrics(team, subset)
        for key, label in METRIC_NAMES.items():
            value, n = m[key]
            rows.append({"clan": team, "metric": key, "label": label, "value": "" if value is None else f"{value:.4f}", "n": n, "smokes": m["n"], "games": m["games"]})
    return rows


def breakdown_rows(data):
    counts = Counter()
    for s in data.smokes:
        counts[(s["team"], s["_primary"], s["_movement"] or "unknown", s["_cover"] or "unknown", s["_lane"] or "unknown")] += 1
    rows = [{"clan": k[0], "primary_purpose": k[1], "movement": k[2], "coverage": k[3], "lane": k[4], "smokes": v} for k, v in sorted(counts.items())]
    tags = Counter()
    for s in data.smokes:
        for tag in s["_purposes"]:
            tags[(s["team"], tag)] += 1
    rows += [{"clan": k[0], "primary_purpose": f"any:{k[1]}", "movement": "", "coverage": "", "lane": "", "smokes": v} for k, v in sorted(tags.items())]
    return rows


def ship_class_rows(data):
    groups = {}
    for s in data.smokes:
        g = groups.setdefault((s["team"], s["_class"]), {"clan": s["team"], "smoker_class": s["_class"], "smokes": 0, "damage": 0.0, "kills": 0, "smoke_deaths": 0, "selfish": 0, "stacked": 0, "screen": 0, "radar_spots_on_us": 0})
        g["smokes"] += 1
        g["damage"] += s["_total"]
        g["kills"] += s["_kills"]
        g["smoke_deaths"] += s["_deaths"]
        g["selfish"] += 1 if s["_cover"] == "selfish" else 0
        g["stacked"] += 1 if s["_cover"] == "stacked" else 0
        g["screen"] += 1 if s["_cover"] == "screen" else 0
        g["radar_spots_on_us"] += s["_radar"]
    rows = []
    for g in sorted(groups.values(), key=lambda g: (g["clan"], g["smoker_class"])):
        g["avg_damage"] = f"{g['damage'] / g['smokes']:.0f}"
        g["damage"] = f"{g['damage']:.0f}"
        rows.append(g)
    return rows


def csv_bytes(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue().encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--maps", required=True)
    ap.add_argument("--inventory", default="smoke/inventory.csv")
    ap.add_argument("--out")
    args = ap.parse_args()
    data = build_site.Data(args.batch, args.maps, None, args.inventory)
    site = build_site.Site(data, os.path.join(args.batch, "export-unused"), build_site.parse_colors(""))
    out = args.out or os.path.join(args.batch, "smoke-signals-data-r6.zip")
    enriched = os.path.join(args.batch, "smokes-enriched.csv")
    build_site.write_enriched_csv(data, enriched)
    games = games_rows(data)
    clans_all = clan_rows(site, data.smokes)
    clans_dd = clan_rows(site, site.lens_rows("destroyer"))
    breakdown = breakdown_rows(data)
    classes = ship_class_rows(data)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(enriched, "smokes.csv")
        z.writestr("games.csv", csv_bytes(games))
        z.writestr("clans.csv", csv_bytes(clans_all))
        z.writestr("clans-destroyer.csv", csv_bytes(clans_dd))
        z.writestr("breakdown.csv", csv_bytes(breakdown))
        z.writestr("ship_class.csv", csv_bytes(classes))
    print(f"wrote {out}: {len(data.smokes)} smokes, {len(games)} games, {len(clans_all)} clan values (all), {len(clans_dd)} (destroyer), {len(breakdown)} breakdown rows, {len(classes)} class rows")


if __name__ == "__main__":
    main()
