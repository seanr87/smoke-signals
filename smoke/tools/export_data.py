"""Export the shareable data set of a batch as one zip.

Usage:
  python -I -X utf8 export_data.py --batch output/<batch> --maps output/<maps>/maps
         [--inventory smoke/inventory.csv] [--out output/<batch>/smoke-signals-data.zip]

The zip holds smokes.csv (the batch's combined table, every field), games.csv
(one row per played game: match, map, teams, winner, end clock and phase) and
clans.csv (every clan chart value with its count, as the Clans page shows it).
"""
import argparse
import csv
import io
import os
import sys
import zipfile

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
        })
    return rows


def clan_rows(site):
    metric_names = {
        "smokes_per_game": "Smokes per game", "damage_per_game": "Smoke damage per game", "avg_damage": "Average damage per smoke",
        "uptime": "Smoke uptime (s per game)", "charge": "Charge use (%)", "stacking": "Stacking rate (%)",
        "contested": "Contested-cap share (%)", "selfish": "Selfish smoke share (%)", "swing": "Score swing while smoke up (pts)",
        "punished": "Radar-punished share (%)", "offensive": "Radar spots from smoke (per game)", "kills": "Kills from smoke (per game)",
        "deaths": "Smoke deaths (per game)", "won": "Smokes near a cap capture", "coverage": "Radar cap coverage (mean %)",
        "coverage_full": "Smokes with full radar cap coverage",
    }
    rows = []
    for team in build_site.TEAMS:
        if not any(s["team"] == team for s in site.d.smokes):
            continue
        m = site.clan_metrics(team)
        for key, label in metric_names.items():
            value, n = m[key]
            rows.append({"clan": team, "metric": key, "label": label, "value": "" if value is None else f"{value:.4f}", "n": n, "smokes": m["n"], "games": m["games"]})
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
    out = args.out or os.path.join(args.batch, "smoke-signals-data.zip")
    games = games_rows(data)
    clans = clan_rows(site)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(args.batch, "smokes.csv"), "smokes.csv")
        z.writestr("games.csv", csv_bytes(games))
        z.writestr("clans.csv", csv_bytes(clans))
    print(f"wrote {out}: {len(data.smokes)} smokes, {len(games)} games, {len(clans)} clan values")


if __name__ == "__main__":
    main()
