"""Mark smokes seen from one replay only and recover the opponent's smokes among them.

Usage: python -I -X utf8 recover_one_sided.py <batch dir>

A game with one replay is analysed from that side only. The analysis sees
every smoke on the map but can attribute a smoke only to a ship whose
position it knows, so the opponent's smokes (laid by unspotted ships) fall to
the nearest ship of the recording team, far away and flagged. This script:

- adds `one_sided` (true/false) to every smoke in the batch's smokes.json and
  smokes.csv; true for smokes from a run with no merged replay;
- for a one-sided smoke whose attributed ship is more than 2 km from the
  origin, reassigns it to the opponent's only ship fitted with smoke, when
  there is exactly one, and says so in owner_note.

Damage, allies inside and the charge number stay as the single replay saw
them. Files are rewritten in place; git keeps the earlier version.
"""
import csv
import json
import os
import re
import sys

FAR_M = 2000.0

batch = sys.argv[1]
json_path = os.path.join(batch, "smokes.json")
csv_path = os.path.join(batch, "smokes.csv")


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


doc = json.load(open(json_path, encoding="utf-8"))
records = doc["smokes"] if isinstance(doc, dict) else doc

rosters = {}


def roster(rec):
    """Teams of the run that produced the record, from its game.json."""
    mid = rec["match_id"]
    key = (mid, rec["game_no"], rec["primary_replay"])
    if key not in rosters:
        games = os.path.join(batch, "games")
        found = None
        for name in os.listdir(games):
            p = os.path.join(games, name, "game.json")
            if not os.path.exists(p):
                continue
            g = json.load(open(p, encoding="utf-8"))
            if g["match_id"] == mid and g["game_no"] == rec["game_no"] and g["primary_replay"] == rec["primary_replay"]:
                found = g
                break
        rosters[key] = found
    return rosters[key]


changes = []
one_sided_ids = set()
reassigned = {}
for rec in records:
    one_sided = not rec.get("merged_replays")
    rec["one_sided"] = one_sided
    if not one_sided:
        continue
    one_sided_ids.add(rec["smoke_id"])
    if rec.get("one_sided_note"):
        continue
    dist = rec.get("owner_distance_m") or 0.0
    if dist <= FAR_M:
        continue
    g = roster(rec)
    if g is None:
        print(f"smoke {rec['smoke_id']}: no game.json for its run; left as is")
        continue
    own = next((t for t in g["teams"] if t["name"] == rec["team"]), None)
    other = next((t for t in g["teams"] if t["name"] != rec["team"]), None)
    if own is None or other is None:
        print(f"smoke {rec['smoke_id']}: teams not found in game.json; left as is")
        continue
    fitted = [p for p in other["players"] if p.get("smoke_type")]
    if len(fitted) != 1:
        print(f"smoke {rec['smoke_id']}: {len(fitted)} enemy ships fitted with smoke; left as is")
        continue
    p = fitted[0]
    before = f"{rec['team']} {rec['player']} {rec['ship']} ({dist:.0f} m from origin)"
    rec["team"], rec["opponent"] = other["name"], own["name"]
    rec["spawn_side"] = other.get("spawn_side")
    rec["player"] = p["player"]
    rec["ship"] = p["ship"]
    rec["ship_class"] = p.get("ship_class")
    rec["ship_tier"] = p.get("ship_tier")
    rec["smoke_type"] = p.get("smoke_type")
    rec["variant"] = p.get("smoke_variant")
    rec["charge_no"] = None
    rec["charges_total"] = p.get("smoke_charges")
    cls = rec.get("classification")
    if isinstance(cls, dict) and p.get("ship_class"):
        cls["smoker_class"] = p["ship_class"].lower()
    note = (
        f"one-sided: seen from the {own['name']} replay only; owner inferred as the only {other['name']} ship fitted with smoke "
        f"(nearest {own['name']} ship was {dist:.0f} m from the origin)"
    )
    rec["owner_note"] = note
    rec["one_sided_note"] = note
    reassigned[rec["smoke_id"]] = rec
    changes.append(f"{rec['smoke_id']}: {before} -> {rec['team']} {rec['player']} {rec['ship']}")

json.dump(doc, open(json_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

with open(csv_path, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    cols = list(reader.fieldnames)
    rows = list(reader)
if "one_sided" not in cols:
    cols.append("one_sided")
by_id = {r["smoke_id"]: r for r in records}
for row in rows:
    rec = by_id.get(int(row["smoke_id"]))
    row["one_sided"] = "true" if rec and rec.get("one_sided") else "false"
    if rec and int(row["smoke_id"]) in reassigned:
        for k in ("team", "opponent", "spawn_side", "player", "ship", "ship_class", "ship_tier", "smoke_type", "variant", "charge_no", "charges_total", "owner_note"):
            v = rec.get(k)
            row[k] = "" if v is None else str(v)
        row["smoker_class"] = (rec.get("classification") or {}).get("smoker_class", row.get("smoker_class", ""))
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

print(f"one-sided smokes: {len(one_sided_ids)}; reassigned: {len(changes)}")
for c in changes:
    print("-", c)
