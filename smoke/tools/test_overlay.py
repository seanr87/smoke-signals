"""Overlay test: the site's map projection must land smoke paths on the smoke
drawn in the capture frames, and the Maps page must keep the map image inside
the overlay SVG so the two cannot drift apart.

Usage:
  python -I -X utf8 smoke/tools/test_overlay.py --batch output/<batch> --maps output/<maps>/maps
         [--site smoke-site] [--ids 224000,...] [--out output/<batch>/overlay-test]

For each chosen smoke the capture frame PNG is decoded (no image library
needed), every puff of the path is projected with the site's map_px and the
frame's map offset, and the frame must show smoke (a bright grey pixel, or
the gold outline drawn around the target smoke) within a puff radius of each
puff. An overlay image of the half-map crop with
the projected path drawn in magenta is written for eyes. Exit code 1 on any
failure.
"""
import argparse
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_site  # noqa: E402

# The map's top-left corner on a roster frame: side panel width, HUD plus header height.
MAP_OFFSET = (280, 64 + 33)
FRAME_SIZE = (1328, 886)
SEARCH_PAD_PX = 4
# Smoke pixels: bright and nearly grey. Outline pixels: the gold highlight.
MIN_BRIGHT = 140
MAX_SPREAD = 40
MIN_HIT_SHARE = 0.8


def read_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    pos = 8
    width = height = None
    idat = []
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color = struct.unpack(">IIBB", body[:10])
            assert depth == 8 and color in (2, 6), (depth, color)
            channels = 3 if color == 2 else 4
        elif kind == b"IDAT":
            idat.append(body)
        elif kind == b"IEND":
            break
        pos += 12 + length
    raw = zlib.decompress(b"".join(idat))
    stride = width * channels
    rows = []
    prev = bytearray(stride)
    at = 0
    for _ in range(height):
        f = raw[at]
        line = bytearray(raw[at + 1:at + 1 + stride])
        at += 1 + stride
        if f == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                b = prev[i]
                c = prev[i - channels] if i >= channels else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 255
        rows.append(line)
        prev = line
    return width, height, channels, rows


def write_png(path, width, height, rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def pixel(rows, channels, x, y):
    r = rows[y]
    return r[x * channels], r[x * channels + 1], r[x * channels + 2]


def is_smoke(rgb):
    grey = min(rgb) >= MIN_BRIGHT and max(rgb) - min(rgb) <= MAX_SPREAD
    gold = rgb[0] >= 200 and rgb[1] >= 160 and rgb[2] <= 100
    return grey or gold


def frame_path(data, s):
    job = s["_job"]
    name = s.get("frame_cap")
    if not job or not name:
        return None
    return os.path.join(data.batch, "games", job["name"], "frames", name)


def check_smoke(data, s, out_dir):
    path = frame_path(data, s)
    if not path or not os.path.exists(path):
        return False, f"{s['smoke_id']}: no capture frame"
    width, height, channels, rows = read_png(path)
    if (width, height) != FRAME_SIZE:
        return False, f"{s['smoke_id']}: frame is {width}x{height}, expected {FRAME_SIZE[0]}x{FRAME_SIZE[1]}; the map offset is unknown"
    puffs = [build_site.map_px(data, s["map"], p["x"], p["z"]) for p in (s.get("path") or [s["origin_xy"]])]
    puffs = [p for p in puffs if p]
    search = int(round((s.get("radius") or 15) * build_site.NATIVE / data.maps[s["map"]]["space_size"])) + SEARCH_PAD_PX
    hits = 0
    for px, py in puffs:
        fx, fy = int(round(px)) + MAP_OFFSET[0], int(round(py)) + MAP_OFFSET[1]
        found = False
        for dy in range(-search, search + 1):
            for dx in range(-search, search + 1):
                x, y = fx + dx, fy + dy
                if 0 <= x < width and 0 <= y < height and is_smoke(pixel(rows, channels, x, y)):
                    found = True
                    break
            if found:
                break
        hits += found
    share = hits / len(puffs) if puffs else 0.0
    # The overlay: the half-map crop around the smoke with the projected path in magenta.
    crop = build_site.Site.thumb_crop(_Stub(data), s)
    if crop:
        ox, oy = int(crop[0]), int(crop[1])
        side = int(build_site.THUMB_SIDE)
        out = []
        for y in range(side):
            row = rows[oy + y + MAP_OFFSET[1]]
            x0 = (ox + MAP_OFFSET[0]) * channels
            line = bytearray()
            for x in range(side):
                line += bytes(row[x0 + x * channels:x0 + x * channels + 3])
            out.append(line)
        for px, py in puffs:
            cx, cy = int(round(px)) - ox, int(round(py)) - oy
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < side and 0 <= y < side:
                        out[y][x * 3:x * 3 + 3] = b"\xff\x00\xff"
        os.makedirs(out_dir, exist_ok=True)
        write_png(os.path.join(out_dir, f"overlay_{s['_match']}_g{s['game_no']}_{s['smoke_id']}.png"), side, side, out)
    ok = share >= MIN_HIT_SHARE
    return ok, f"{s['smoke_id']} {s['player']} {s['ship']} on {data.map_title(s['map'])}: {hits} of {len(puffs)} puffs land on smoke ({share:.0%})"


class _Stub:
    def __init__(self, data):
        self.d = data


def check_site(site):
    """The Maps page keeps each map image inside its overlay SVG, and the grid labels follow the game."""
    path = os.path.join(site, "maps.html")
    if not os.path.exists(path):
        return True, "site not built; Maps page check skipped"
    html = open(path, encoding="utf-8").read()
    svgs = html.count('<svg viewBox="0 0 768 768" class="mapsvg')
    images = html.count('<image href=')
    if svgs == 0 or svgs != images:
        return False, f"maps.html: {svgs} map SVGs but {images} image elements inside them"
    if '<text x="38" y="14">1</text>' not in html or '<text x="6" y="42" text-anchor="start">A</text>' not in html:
        return False, "maps.html: grid labels are not numbers across the top and letters down the side"
    return True, f"maps.html: {svgs} maps drawn with the image inside the overlay SVG, grid labels follow the game"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--maps", required=True)
    ap.add_argument("--site", default="smoke-site")
    ap.add_argument("--ids", default="")
    ap.add_argument("--inventory", default="smoke/inventory.csv")
    ap.add_argument("--out")
    args = ap.parse_args()
    data = build_site.Data(args.batch, args.maps, None, args.inventory)
    out_dir = args.out or os.path.join(args.batch, "overlay-test")
    failures = 0
    # The grid convention on one known smoke: Big_Boy69's Somers on Hotspot sits in D7.
    known = next((s for s in data.smokes if s["smoke_id"] == 224000 and s["map"] == "16_OC_bees_to_honey"), None)
    if known:
        square = build_site.grid_square(data.maps[known["map"]]["space_size"], known["origin_xy"]["x"], known["origin_xy"]["z"])
        ok = square == "D7"
        failures += not ok
        print(("ok  " if ok else "FAIL"), f"grid square of smoke 224000 is {square} (expected D7)")
    chosen = []
    if args.ids:
        wanted = {int(x) for x in args.ids.split(",") if x.strip()}
        chosen = [s for s in data.smokes if s["smoke_id"] in wanted]
    else:
        seen = set()
        for s in sorted(data.smokes, key=lambda s: (s["smoke_id"] != 224000, s["map"], s["_key"], s["_act_s"])):
            if s["map"] in seen or not s.get("path") or len(s["path"]) < 5:
                continue
            seen.add(s["map"])
            chosen.append(s)
            if len(chosen) == 4:
                break
    for s in chosen:
        ok, msg = check_smoke(data, s, out_dir)
        failures += not ok
        print(("ok  " if ok else "FAIL"), msg)
    ok, msg = check_site(args.site)
    failures += not ok
    print(("ok  " if ok else "FAIL"), msg)
    print(f"overlays written to {out_dir}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
