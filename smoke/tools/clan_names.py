"""Fill the full names in smoke/clans.csv from the tournament API.

python -I -X utf8 smoke/tools/clan_names.py [--inventory smoke/inventory.csv] [--registry smoke/clans.csv]

Reads each match of the inventory (one request per match id, stopping once
every clan in the registry has a name), takes `teamName` of each opponent's
signup ('[TAG] Full Name') and writes the part after the tag. Existing
names are kept; clans with no name found are listed.
"""
import argparse
import csv
import json
import re
import urllib.request

SITE = "https://wows-tournaments.com"
HEADERS = {"x-tournament-name": "king-of-the-sea-xix", "x-tournament-region": "NA", "User-Agent": "smoke-signals-inventory"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", default="smoke/inventory.csv")
    ap.add_argument("--registry", default="smoke/clans.csv")
    args = ap.parse_args()
    rows = list(csv.DictReader(open(args.registry, encoding="utf-8")))
    wanted = {r["tag"] for r in rows if not r["name"]}
    names = {}
    seen = set()
    for inv in csv.DictReader(open(args.inventory, encoding="utf-8")):
        mid = inv["match_id"]
        if mid in seen or not wanted - set(names):
            continue
        seen.add(mid)
        try:
            req = urllib.request.Request(f"{SITE}/api/matches/match?id={mid}", headers=HEADERS)
            data = json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as e:
            print(f"match {mid}: {e}")
            continue
        for opp in data.get("matchOpponents") or []:
            signup = opp.get("signup") or {}
            tag, full = signup.get("teamTag"), signup.get("teamName") or ""
            m = re.match(r"\s*\[([^\]]+)\]\s*(.*)$", full)
            if tag and m and m.group(2).strip():
                names.setdefault(tag, m.group(2).strip())
            elif tag and full.strip():
                names.setdefault(tag, full.strip())
    missing = []
    for r in rows:
        if not r["name"]:
            if r["tag"] in names and names[r["tag"]] != r["tag"]:
                r["name"] = names[r["tag"]]
            else:
                missing.append(r["tag"])
    with open(args.registry, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tag", "name", "group", "color", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"names filled: {sum(1 for r in rows if r['name'])} of {len(rows)}; requests: {len(seen)}")
    for r in rows:
        print(f"  {r['tag']}: {r['name'] or '(none)'}")
    if missing:
        print("missing: " + ", ".join(missing))


if __name__ == "__main__":
    main()
