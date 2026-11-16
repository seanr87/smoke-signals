"""Build the KotS XIX NA replay inventory.

Usage: python -I inventory.py <repo root> <scratch dir> [options]

Options:
  --first N / --last N   match id range to enumerate (default 7850..8200)
  --teams all|TAG,TAG    teams in scope (default H-SR,RESIN,PN); "all" keeps
                         every match and puts both teams in our_teams
  --no-download          do not fetch replays; only record which replays the
                         site offers and which files already exist
  --out PATH             inventory path (default <repo root>/smoke/inventory.csv)

Enumerates match ids over the tournament's id range through the public
match API, keeps matches with a team in scope, reads each game's report
page for replay ids, downloads the replays into replays/<game folder>/
(unless --no-download) and writes the inventory CSV.
"""
import argparse
import csv
import json
import os
import re
import struct
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
ap.add_argument("root")
ap.add_argument("scratch")
ap.add_argument("--first", type=int, default=7850)
ap.add_argument("--last", type=int, default=8200)
ap.add_argument("--teams", default="H-SR,RESIN,PN")
ap.add_argument("--no-download", action="store_true")
ap.add_argument("--out", default=None)
args = ap.parse_args()

ROOT = args.root
SCRATCH = args.scratch
FIRST, LAST = args.first, args.last
ALL_TEAMS = args.teams.strip().lower() == "all"
OURS = set() if ALL_TEAMS else {t.strip() for t in args.teams.split(",") if t.strip()}
SITE = "https://wows-tournaments.com"
HEADERS = {"x-tournament-name": "king-of-the-sea-xix", "x-tournament-region": "NA", "User-Agent": "smoke-signals-inventory"}
REPLAY_DIR = os.path.join(ROOT, "replays")
OUT = args.out or os.path.join(ROOT, "smoke", "inventory.csv")


def get(url, binary=False):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
            return r.status, (data if binary else data.decode("utf-8", "replace")), r.headers
    except urllib.error.HTTPError as e:
        return e.code, None, None


def match(mid):
    status, text, _ = get(f"{SITE}/api/matches/match?id={mid}")
    if status != 200:
        return None
    return json.loads(text)


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


def replay_version(path):
    with open(path, "rb") as f:
        head = f.read(12)
        if len(head) < 12:
            return "", ""
        length = struct.unpack("<I", head[8:12])[0]
        meta = json.loads(f.read(length).decode("utf-8", "replace"))
    return meta.get("clientVersionFromExe", ""), meta.get("playerName", "")


print(f"enumerating match ids {FIRST}..{LAST}")
with ThreadPoolExecutor(max_workers=8) as pool:
    found = [m for m in pool.map(match, range(FIRST, LAST + 1)) if m]
print("matches found", len(found), "ids", min(m["id"] for m in found), "to", max(m["id"] for m in found))
json.dump(found, open(os.path.join(SCRATCH, "all_matches.json"), "w", encoding="utf-8"), indent=1)

if ALL_TEAMS:
    selected = found
else:
    selected = [m for m in found if OURS & {o["signup"]["teamTag"] for o in m["matchOpponents"]}]
print("selected matches", len(selected))

rows = []
os.makedirs(REPLAY_DIR, exist_ok=True)
for m in sorted(selected, key=lambda m: (m["scheduledTime"], m["id"])):
    tags = {o["id"]: o["signup"]["teamTag"] for o in m["matchOpponents"]}
    teams = [o["signup"]["teamTag"] for o in m["matchOpponents"]]
    stage = m["stageName"]
    group = m["groupName"] or ""
    rnd = m["roundName"] or ""
    for g in m["matchGames"]:
        gid = g["id"]
        number = g["number"]
        status, html, _ = get(f"{SITE}/king-of-the-sea-xix/na/matches/{m['id']}/game/{gid}")
        reports = {}
        if status == 200:
            text = html.replace("&quot;", '"')
            for rm in re.finditer(r'"id":(\d+),"opponentId":(\d+),"matchGameNumber":(\d+),"replayFileId":(\d+|null)', text):
                rid, oid, gnum, rfid = rm.groups()
                if int(gnum) == number:
                    reports[int(oid)] = (int(rid), rfid != "null")
        results = {r["opponentId"]: r for r in g.get("results", [])}
        winner = next((tags[oid] for oid, r in results.items() if r.get("win")), "")
        score = " - ".join(f"{tags[oid]} {r['score']}" for oid, r in results.items())
        folder = f"kots19na_{slug(stage)}_{slug(group)}_{slug(rnd)}_{slug(teams[0])}-vs-{slug(teams[1])}_g{number}"
        game_dir = os.path.join(REPLAY_DIR, folder)
        files, versions, missing, on_site, to_fetch = [], [], [], [], []
        for oid, tag in tags.items():
            rid, has_file = reports.get(oid, (None, False))
            if rid is None or not has_file:
                missing.append(tag)
                continue
            on_site.append(tag)
            suffixes = (f"_{slug(tag)}.wowsreplay", f"_{tag.lower()}.wowsreplay")
            existing = [f for f in os.listdir(game_dir) if f.endswith(suffixes)] if os.path.isdir(game_dir) else []
            if existing:
                path = os.path.join(game_dir, existing[0])
            elif args.no_download:
                to_fetch.append(tag)
                continue
            else:
                os.makedirs(game_dir, exist_ok=True)
                status, data, headers = get(f"{SITE}/api/matches/report/replay?id={rid}", binary=True)
                if status != 200 or not data or not data.startswith(b"\x12\x32\x34\x11"):
                    missing.append(f"{tag} (download failed, http {status})")
                    continue
                name = None
                cd = headers.get("Content-Disposition", "") if headers else ""
                nm = re.search(r"filename=([^;]+)", cd)
                if nm:
                    name = nm.group(1).strip("\" ")
                if not name or not name.endswith(".wowsreplay"):
                    name = f"report_{rid}_{slug(tag)}.wowsreplay"
                path = os.path.join(game_dir, name)
                with open(path, "wb") as f:
                    f.write(data)
                time.sleep(0.2)
            version, recorder = replay_version(path)
            files.append(os.path.relpath(path, ROOT).replace("\\", "/"))
            versions.append(f"{tag}:{version}")
        if not results:
            state = "not played"
        elif "BYE" in teams:
            state = "bye"
        elif files:
            state = "played"
        elif any(r.get("forfeit") for r in results.values()):
            state = "forfeit"
        else:
            state = "no replay"
        rows.append({
            "match_id": m["id"],
            "game_id": gid,
            "stage": stage,
            "group": group,
            "round": rnd,
            "game_no": number,
            "date": m["scheduledTime"][:10],
            "map": g.get("mapName", ""),
            "teams": " vs ".join(teams),
            "our_teams": ";".join(t for t in teams if ALL_TEAMS or t in OURS),
            "winner": winner,
            "score": score,
            "replay_folder": f"replays/{folder}" if files else "",
            "replay_files": ";".join(files),
            "replay_versions": ";".join(versions),
            "replays_found": len(files),
            "missing_replays": ";".join(missing) if state in ("played", "no replay") else "",
            "missing_flag": ("yes" if missing else "no") if state in ("played", "no replay") else "n/a",
            "status": state,
            "replays_on_site": ";".join(on_site),
            "to_download": ";".join(to_fetch),
        })
        print(f"{m['id']}/{gid} {stage}/{group}/{rnd} g{number} {teams} map={g.get('mapName')} files={len(files)} on_site={on_site} to_download={to_fetch} missing={missing}")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("wrote", OUT, "rows", len(rows))
