# Part B helper: find candidate spots (mean-shift on Top 6 smoke centres) and test them against the Rest.
# Read-only on the batch. Imported by spots_build.py.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'round3')))
from common import *

H_KM = 2.0            # mean-shift bandwidth (Gaussian kernel), km
MERGE_KM = 1.0        # density peaks closer than this are one spot
MIN_RADIUS_KM = 1.0   # floor on each ellipse radius
SIGMAS = 2.0          # ellipse radii = 2 standard deviations of the cluster along its own axes
MIN_N = 8
KM = 1000.0 / WU      # world units per km

def mean_shift(pts, h, merge=MERGE_KM * KM):
    """Gaussian-kernel mean-shift (bandwidth h). Each point climbs to its density peak; peaks closer than `merge` are one spot.
    Returns a list of clusters, each a list of point indices."""
    modes = []
    for (x, z) in pts:
        for _ in range(200):
            w = [math.exp(-((a - x) ** 2 + (b - z) ** 2) / (2 * h * h)) for a, b in pts]
            sw = sum(w); nx_, nz_ = sum(wi * p[0] for wi, p in zip(w, pts)) / sw, sum(wi * p[1] for wi, p in zip(w, pts)) / sw
            if math.hypot(nx_ - x, nz_ - z) < 0.02: break
            x, z = nx_, nz_
        modes.append((x, z))
    labels, centres = [], []
    for m in modes:
        for i, c in enumerate(centres):
            if math.hypot(m[0] - c[0], m[1] - c[1]) <= merge: labels.append(i); break
        else:
            centres.append(m); labels.append(len(centres) - 1)
    out = collections.defaultdict(list)
    for i, l in enumerate(labels): out[l].append(i)
    return list(out.values())

def ellipse(pts):
    """Centre and 2-sigma ellipse of a point set: (cx, cz, r1, r2, angle) in world units; angle of the r1 axis from +x toward +z."""
    cx, cz = mean(p[0] for p in pts), mean(p[1] for p in pts)
    n = len(pts)
    sxx = sum((p[0] - cx) ** 2 for p in pts) / n; szz = sum((p[1] - cz) ** 2 for p in pts) / n; sxz = sum((p[0] - cx) * (p[1] - cz) for p in pts) / n
    tr, det = sxx + szz, sxx * szz - sxz * sxz
    d = math.sqrt(max(0, tr * tr / 4 - det)); l1, l2 = tr / 2 + d, max(0, tr / 2 - d)
    ang = 0.5 * math.atan2(2 * sxz, sxx - szz)
    fl = MIN_RADIUS_KM * KM
    return cx, cz, max(fl, SIGMAS * math.sqrt(l1)), max(fl, SIGMAS * math.sqrt(l2)), ang

def inside(e, x, z):
    cx, cz, r1, r2, ang = e
    dx, dz = x - cx, z - cz; ca, sa = math.cos(ang), math.sin(ang)
    a, b = dx * ca + dz * sa, -dx * sa + dz * ca
    return (a / r1) ** 2 + (b / r2) ** 2 <= 1.0

def boot_gap(top, rest, flag, reps, rng):
    """95% interval of share(top) - share(rest) in percentage points, resampling whole clans within each group."""
    ct, cr = by(top, 'team'), by(rest, 'team')
    ft = {c: (sum(flag(s) for s in v), len(v)) for c, v in ct.items()}; fr = {c: (sum(flag(s) for s in v), len(v)) for c, v in cr.items()}
    kt, kr = list(ft), list(fr)
    if not kt or not kr: return (None, None)
    out = []
    for _ in range(reps):
        a = [ft[c] for c in rng.choices(kt, k=len(kt))]; b = [fr[c] for c in rng.choices(kr, k=len(kr))]
        out.append(100 * sum(x for x, _ in a) / sum(n for _, n in a) - 100 * sum(x for x, _ in b) / sum(n for _, n in b))
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]

def candidates(S, topset=TOP, exclude=(), h_km=H_KM, reps=1000, seed=19):
    """Every ship and every habit cluster x map with at least MIN_N 'top' smokes; mean-shift on the top smoke centres; every cluster
    whose ellipse holds at least MIN_N top smokes is a candidate, tested against the rest. `topset` / `exclude` let a placebo run
    use other clans as the top group. Returns (number of subjects, number of clusters, candidates)."""
    rng = random.Random(seed)
    pool = [s for s in S if s['cls'] in ('destroyer', 'cruiser') and s['team'] not in exclude]
    cands = []; n_sub = n_cl = 0
    for m in MAPS:
        ms = [s for s in pool if s['map'] == m]
        for kind in ('ship', 'habit'):
            for name, ss in sorted(by(ms, kind).items()):
                if kind == 'habit' and name == 'other': continue
                top = [s for s in ss if s['team'] in topset]; rest = [s for s in ss if s['team'] not in topset]
                if len(top) < MIN_N: continue
                n_sub += 1
                cl = mean_shift([(s['nx'], s['nz']) for s in top], h_km * KM); n_cl += len(cl)
                for idx in cl:
                    if len(idx) < 3: continue
                    e = ellipse([(top[i]['nx'], top[i]['nz']) for i in idx])
                    fl = lambda s, e=e: inside(e, s['nx'], s['nz'])
                    tin = [s for s in top if fl(s)]; rin = [s for s in rest if fl(s)]
                    if len(tin) < MIN_N: continue
                    ts = 100 * len(tin) / len(top); rs = 100 * len(rin) / len(rest) if rest else None
                    lo, hi = boot_gap(top, rest, fl, reps, rng) if rest else (None, None)
                    clans = C(s['team'] for s in tin)
                    big = clans.most_common(1)[0][0]; t2 = [s for s in top if s['team'] != big]
                    cands.append(dict(map=m, kind=kind, subject=name, e=e, top=top, rest=rest, tin=tin, rin=rin, ts=ts, rs=rs,
                                      gap=ts - rs if rest else None, lo=lo, hi=hi, clans=clans, big=big,
                                      ts_wo=100 * sum(fl(s) for s in t2) / len(t2) if t2 else None))
    return n_sub, n_cl, cands

def passes(c):
    """Signature rule: at least 8 Top 6 smokes in the spot, at least 2 Top 6 clans, Rest field the subject (n >= 8), interval above zero."""
    return len(c['tin']) >= MIN_N and len(c['clans']) >= 2 and len(c['rest']) >= MIN_N and c['lo'] is not None and c['lo'] > 0
