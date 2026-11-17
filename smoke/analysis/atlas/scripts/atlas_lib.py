# Smoke Atlas helpers. Read-only on the batch and on the round 3 / round 4 outputs; writes only under smoke/analysis/atlas/.
import sys, os
sys.dont_write_bytecode = True
HERE_A = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE_A, '..', '..', 'round3')))
from common import *

ATLAS = os.path.abspath(os.path.join(HERE_A, '..'))
ANALYSIS = os.path.abspath(os.path.join(ATLAS, '..'))
KM = 1000.0 / WU          # world units per km
H_KM = 2.0                # mean-shift bandwidth (Gaussian kernel), km
MERGE_KM = 1.0            # density peaks closer than this are one cluster
MIN_RADIUS_KM = 1.0       # floor on each ellipse radius
SIGMAS = 2.0              # ellipse radii = 2 standard deviations of the cluster along its own axes
MIN_N = 8                 # nothing is reported below this
SOLID_N = 15              # 8 to 14 is small n
EARLY_S = 300             # first 5 minutes
MAP_ORDER = ['Sleeping Giant', 'Hotspot', 'Loop', 'Mountain Range', 'Land of Fire', 'Sea of Fortune', 'Okinawa']
MAP_CODE = {'Sleeping Giant': 'sg', 'Hotspot': 'hs', 'Loop': 'loop', 'Mountain Range': 'mr', 'Land of Fire': 'lof', 'Sea of Fortune': 'sof', 'Okinawa': 'oki'}
FRAME = ('0-1 minimap frame: origin at the top-left corner of the minimap image, u to the right (west to east), v down (north to south), '
         'both 0 to 1 across the full image. Positions are team-normalized so the smoking team spawn is at the bottom (bottom-left on Okinawa): '
         'north-spawn teams are mirrored north-south (v -> 1 - v) on Hotspot, Loop, Land of Fire, Mountain Range, Sleeping Giant and Sea of Fortune, '
         'and across the NW-SE diagonal ((u, v) -> (v, u)) on Okinawa, whose spawns are NE and SW. The mirror is applied to positions only: the frame is the minimap '
         'image in its native orientation, so the images need no flipping. Lengths: radius_u, ru and rv are fractions of the image width. '
         'An ellipse angle_deg is the rotation of the ru axis clockwise on screen from the u axis (as SVG rotate).')

def mean_shift(pts, h_km=H_KM, merge_km=MERGE_KM):
    """Gaussian-kernel mean-shift. Each point climbs to its density peak; peaks closer than merge_km are one cluster.
    Returns clusters as lists of point indices, largest first."""
    h, merge = h_km * KM, merge_km * KM
    modes = []
    for (x, z) in pts:
        for _ in range(200):
            w = [math.exp(-((a - x) ** 2 + (b - z) ** 2) / (2 * h * h)) for a, b in pts]
            sw = sum(w); x2, z2 = sum(wi * p[0] for wi, p in zip(w, pts)) / sw, sum(wi * p[1] for wi, p in zip(w, pts)) / sw
            if math.hypot(x2 - x, z2 - z) < 0.02: break
            x, z = x2, z2
        modes.append((x, z))
    labels, centres = [], []
    for m in modes:
        for i, c in enumerate(centres):
            if math.hypot(m[0] - c[0], m[1] - c[1]) <= merge: labels.append(i); break
        else:
            centres.append(m); labels.append(len(centres) - 1)
    out = collections.defaultdict(list)
    for i, l in enumerate(labels): out[l].append(i)
    return sorted(out.values(), key=lambda v: -len(v))

def ellipse(pts):
    """Centre and 2-sigma ellipse of a point set in world units: (cx, cz, r1, r2, angle); angle of the r1 axis from +x toward +z."""
    cx, cz = mean(p[0] for p in pts), mean(p[1] for p in pts); n = len(pts)
    sxx = sum((p[0] - cx) ** 2 for p in pts) / n; szz = sum((p[1] - cz) ** 2 for p in pts) / n; sxz = sum((p[0] - cx) * (p[1] - cz) for p in pts) / n
    tr, det = sxx + szz, sxx * szz - sxz * sxz
    d = math.sqrt(max(0, tr * tr / 4 - det)); l1, l2 = tr / 2 + d, max(0, tr / 2 - d)
    ang = 0.5 * math.atan2(2 * sxz, sxx - szz); fl = MIN_RADIUS_KM * KM
    return cx, cz, max(fl, SIGMAS * math.sqrt(l1)), max(fl, SIGMAS * math.sqrt(l2)), ang

def ellipse_uv(mapname, e):
    """World ellipse to the 0-1 frame: (centre_uv, shape dict). World z points north and v points south, so the screen angle is -angle."""
    cx, cz, r1, r2, ang = e; size = MAPS[mapname]['space_size']
    u, v = uv(mapname, cx, cz)
    return [round(u, 4), round(v, 4)], dict(type='ellipse', ru=round(r1 / size, 4), rv=round(r2 / size, 4), angle_deg=round(-math.degrees(ang), 1))

def cell_polygon(c, r):
    return dict(type='polygon', points_uv=[[c / 10, r / 10], [(c + 1) / 10, r / 10], [(c + 1) / 10, (r + 1) / 10], [c / 10, (r + 1) / 10]])

def cells_of(mapname, pts, k=3):
    """Most common grid cells of a point set, as names."""
    cc = C(cell_name(*cell(mapname, x, z)) for x, z in pts)
    return [n for n, _ in cc.most_common(k)]

def nearest_cap(G, mapname, x, z):
    """(letter, km from the cap edge; negative inside) of the cap nearest to a normalized position."""
    c = min(map_caps(G, mapname), key=lambda c: math.hypot(c['x'] - x, c['z'] - z) - c['r'])
    return c['cap'], (math.hypot(c['x'] - x, c['z'] - z) - c['r']) / KM

def side_words(G, mapname, x, z):
    """Plain words for where a point sits relative to its nearest cap, as seen from the bottom spawn."""
    c = min(map_caps(G, mapname), key=lambda c: math.hypot(c['x'] - x, c['z'] - z) - c['r'])
    d = (math.hypot(c['x'] - x, c['z'] - z) - c['r']) / KM
    f = forward(mapname, x - c['x'], z - c['z']) / 1000.0   # km toward the enemy from the cap centre
    if d <= 0: where = 'inside cap ' + c['cap'] + (', own half' if f < -0.5 else ', far half' if f > 0.5 else '')
    else:
        lat = math.sqrt(max(0, (math.hypot(c['x'] - x, c['z'] - z) / KM) ** 2 - f * f))
        if f < -abs(lat) * 0.6: where = f'{d:.1f} km short of cap {c["cap"]} (own side)'
        elif f > abs(lat) * 0.6: where = f'{d:.1f} km past cap {c["cap"]} (enemy side)'
        else: where = f'{d:.1f} km beside cap {c["cap"]}'
    return where

def clock(sec): return f'{int(sec) // 60}:{int(sec) % 60:02d}'
def kfmt(x): return '-' if x is None else f'{x / 1000:.1f}k'
