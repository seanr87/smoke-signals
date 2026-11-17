# Smoke Atlas working figures: one per map page, drawn from spots.json and caps.json (so the files and the frame are checked by eye),
# plus the clan styles figure (Part D's figures, re-pointed at ../maps/ and re-rendered).
# Run from the repo root after atlas_build.py: python -I -X utf8 smoke/analysis/atlas/scripts/atlas_figs.py [map code ...]
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_lib import *

S, G = load()
SP = json.load(open(os.path.join(ATLAS, 'spots.json'), encoding='utf-8'))['spots']
CAPS = json.load(open(os.path.join(ATLAS, 'caps.json'), encoding='utf-8'))['maps']
FIG = os.path.join(ATLAS, 'figures')
SIZE, X1, X2, Y0 = 570, 44, 44 + 570 + 52, 146
C_SIG, C_HIGH, C_LOW, C_EARLY, C_RADAR, C_DEATH, C_CRU, C_DD2 = BLUE, GREEN, ORANGE, YELLOW, MAGENTA, RED, VIOLET, AQUA

def pxy(x0, uvp): return x0 + uvp[0] * SIZE, Y0 + uvp[1] * SIZE
def shape_svg(x0, sp, stroke, width=2.2, dash=None, fill='none', fo=0.0):
    cx, cy = pxy(x0, sp['centre_uv']); sh = sp['shape']; d = f' stroke-dasharray="{dash}"' if dash else ''
    if sh['type'] == 'ellipse':
        return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{sh["ru"] * SIZE:.1f}" ry="{sh["rv"] * SIZE:.1f}" transform="rotate({sh["angle_deg"]} {cx:.1f} {cy:.1f})" '
                f'fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{width}"{d}/>')
    pts = ' '.join(f'{x0 + u * SIZE:.1f},{Y0 + v * SIZE:.1f}' for u, v in sh['points_uv'])
    return f'<polygon points="{pts}" fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{width}"{d}/>'
def top_point(sp, sign=-1):
    """A point on the outline of an ellipse record: topmost (sign -1) or bottommost (+1), in uv."""
    sh = sp['shape']; a = math.radians(sh['angle_deg'])
    ext = math.sqrt((sh['ru'] * math.sin(a)) ** 2 + (sh['rv'] * math.cos(a)) ** 2)
    off = (sh['ru'] ** 2 - sh['rv'] ** 2) * math.sin(a) * math.cos(a) / ext if ext else 0
    return [sp['centre_uv'][0] + sign * off, sp['centre_uv'][1] + sign * ext]
def badge_point(m, recs, sp, prefer=-1):
    """Top or bottom point of the outline, whichever does not sit on a cap letter or on a cell's damage label."""
    def clash(pt):
        if any(math.hypot(pt[0] - c['centre_uv'][0], pt[1] - c['centre_uv'][1]) < 0.04 for c in CAPS[m]['caps']): return True
        for r in recs:
            if r['kind'] in ('paying_high', 'paying_low') and abs(pt[0] - r['centre_uv'][0]) < 0.06 and -0.055 < pt[1] - r['centre_uv'][1] < 0.0: return True
        return not (0.02 < pt[0] < 0.98 and 0.02 < pt[1] < 0.98)
    a, b = top_point(sp, prefer), top_point(sp, -prefer)
    return a if not clash(a) or clash(b) else b
def badge(x, y, txt, col):
    w = 9 + 6.5 * len(txt)
    return (f'<rect x="{x - w / 2:.1f}" y="{y - 8:.1f}" width="{w:.1f}" height="16" rx="8" fill="{col}" stroke="{BG}" stroke-width="1.2"/>'
            + T(x, y + 4, txt, size=10.5, fill='#ffffff', weight='700'))
def diamond(x, y, col, r=6.5):
    return f'<polygon points="{x:.1f},{y - r:.1f} {x + r:.1f},{y:.1f} {x:.1f},{y + r:.1f} {x - r:.1f},{y:.1f}" fill="{col}" stroke="{BG}" stroke-width="1.4"/>'
def triangle(x, y, col, r=7):
    return f'<polygon points="{x:.1f},{y - r:.1f} {x + r:.1f},{y + r * 0.8:.1f} {x - r:.1f},{y + r * 0.8:.1f}" fill="{col}" stroke="{BG}" stroke-width="1.4"/>'
def clampx(x0, x): return min(max(x, x0 + 12), x0 + SIZE - 12)
def clampy(y): return min(max(y, Y0 + 10), Y0 + SIZE - 10)

def base_panel(m, x0, title):
    p = Panel(m, x0, Y0, SIZE, G, title=title, dim=0.42, caps=False)
    for c in CAPS[m]['caps']:
        cx, cy = pxy(x0, c['centre_uv'])
        p.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{c["radius_u"] * SIZE:.1f}" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.8"/>')
        p.raw(T(clampx(x0, cx), cy + 4, c['letter'], size=12, fill=INK, weight='700', halo=True))
    return p

def cast_marks(p, x0, parent, recs):
    for r in recs:
        if r['parent'] != parent['id']: continue
        a, b = pxy(x0, parent['centre_uv']), pxy(x0, r['centre_uv'])
        col = C_CRU if r['kind'] == 'cast_cruiser' else C_DD2
        p.raw(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="1.3" opacity="0.9"/>')
        p.raw(diamond(b[0], b[1], col) if r['kind'] == 'cast_cruiser' else triangle(b[0], b[1], col))

def k(v): return f'{v / 1000:.1f}k'
def map_figure(m):
    code = MAP_CODE[m]; recs = [s for s in SP if s['map'] == m]
    ms = [s for s in S if s['map'] == m]
    fig = Fig(1280, 100, f'{m}: working figure for the atlas page',
              f'Own spawn at the bottom{" left" if m in DIAGONAL else ""} ({NORM_NOTE[m]}). Drawn from spots.json and caps.json. Association only: where smokes were laid and what they returned.')
    notes1, notes2 = [], []
    # ----- panel 1: signature spots, leads, paying cells
    p = base_panel(m, X1, 'Signature spots, leads and what cells returned')
    for s in ms:
        if s['cls'] in ('destroyer', 'cruiser'): p.dot(s['nx'], s['nz'], r=2.2, fill=GROUP_COLOR[s['grp']], opacity=0.6)
    for r in recs:
        if r['kind'] in ('paying_high', 'paying_low'):
            col = C_HIGH if r['kind'] == 'paying_high' else C_LOW
            flagged = r['numbers']['flag'] in ('high', 'low')
            p.raw(shape_svg(X1, r, col, 2.0, None if flagged else '3 3', col, 0.30 if flagged else 0.10))
            cx, cy = pxy(X1, r['centre_uv'])
            p.raw(T(cx, cy - SIZE * 0.05 + 12, k(r['numbers']['concealed_damage_per_smoke']), size=11, fill=INK, weight='700', halo=True))
            notes1.append((col, f'{r["id"].split("-")[-1].upper()} {"" if flagged else "(not flagged) "}{k(r["numbers"]["concealed_damage_per_smoke"])} per smoke, n {r["numbers"]["n"]}{"*" if r["small_n"] else ""}, '
                                f'{r["numbers"]["deaths_per_100"]:.0f} deaths/100, cap won after {r["numbers"]["cap_won_pct_all_smokes"]:.0f}%'))
    i = 0; sig_notes = []
    for r in recs:
        if r['kind'] in ('signature', 'lead'):
            i += 1
            p.raw(shape_svg(X1, r, C_SIG, 3.0 if r['kind'] == 'signature' else 2.2, None if r['kind'] == 'signature' else '7 5'))
            cast_marks(p, X1, r, recs)
            tp = badge_point(m, recs, r, -1 if i % 2 else 1); bx, by = pxy(X1, tp)
            p.raw(badge(clampx(X1, bx), clampy(by), ('S' if r['kind'] == 'signature' else 'L') + str(i), C_SIG))
            n = r['numbers']
            sig_notes.append((C_SIG, f'{"S" if r["kind"] == "signature" else "L"}{i} {r["kind"]}: {r["subject"]}, {r["label"]}. Top 6 {n["n"]} of {n["top6_n_total"]} vs Rest {n["rest_n_in"]} of {n["rest_n_total"]}, '
                                     f'gap {n["gap_pts"]:+.0f} ({n["gap_ci_lo"]:+.0f} to {n["gap_ci_hi"]:+.0f}); formation {n["formation_count"]} of {n["formation_of"]}'))
    if not sig_notes: sig_notes = [(MUTED, 'No signature spot or lead on this map.')]
    notes1 = sig_notes + notes1
    fig.add(p)
    # ----- panel 2: early setup, radar addresses, death clusters
    p = base_panel(m, X2, 'Opening setup, radar addresses and deaths in smoke')
    for s in ms:
        if s['cls'] == 'destroyer' and s['el'] < EARLY_S: p.dot(s['nx'], s['nz'], r=2.6, fill=GROUP_COLOR[s['grp']], opacity=0.6)
    for s in ms:
        if s['deaths'] > 0:
            x, y = p.xy(s['nx'], s['nz'])
            p.raw(f'<path d="M{x - 3.2:.1f},{y - 3.2:.1f} L{x + 3.2:.1f},{y + 3.2:.1f} M{x - 3.2:.1f},{y + 3.2:.1f} L{x + 3.2:.1f},{y - 3.2:.1f}" stroke="{C_DEATH}" stroke-width="1.6" opacity="0.85"/>')
        if s['radar_play']:
            x, y = p.xy(s['nx'], s['nz'])
            p.raw(f'<rect x="{x - 3:.1f}" y="{y - 3:.1f}" width="6" height="6" fill="none" stroke="{C_RADAR}" stroke-width="1.6" opacity="0.95"/>')
    cnt = dict(early_smoke=0, radar=0, deaths=0)
    for kind, col, dash, pre, sign in (('deaths', C_DEATH, '2 4', 'D', 1), ('radar', C_RADAR, '8 4', 'R', -1), ('early_smoke', C_EARLY, None, 'E', -1)):
        for r in recs:
            if r['kind'] != kind: continue
            cnt[kind] += 1; n = r['numbers']
            p.raw(shape_svg(X2, r, col, 2.6, dash))
            if kind == 'early_smoke': cast_marks(p, X2, r, recs)
            tp = badge_point(m, [], r, sign); bx, by = pxy(X2, tp)
            if kind == 'radar': bx += 26
            p.raw(badge(clampx(X2, bx), clampy(by), pre + str(cnt[kind]), col if col != YELLOW else '#a36f00'))
            if kind == 'early_smoke':
                notes2.append(('#a36f00', f'E{cnt[kind]} early: {r["label"]}. n {n["n"]}{"*" if r["small_n"] else ""} (Top 6 {n["top6_n"]}, Rest {n["rest_n"]}); radar cruiser inside {n["radar_cruiser_inside_n"]}; '
                                          f'{k(n["concealed_damage_per_smoke"])} per smoke; median {clock(n["median_time_s"])}'))
            elif kind == 'radar':
                notes2.append((col, f'R{cnt[kind]} radar: {r["label"]}. {n["n"]} plays* (Top 6 {n["top6_n"]}), cap won {n["cap_won_count"]} of {n["cap_won_n"]}, {k(n["concealed_damage_per_smoke"])} per smoke'))
            else:
                notes2.append((col, f'D{cnt[kind]} deaths: {r["label"]}. {n["n"]} smokes with a death{"*" if r["small_n"] else ""} (Top 6 {n["top6_n"]}); {n["deaths_per_100_in_ellipse"]:.0f} per 100 smokes laid there (map {n["map_deaths_per_100_all_classes"]:.0f})'))
    notes2.sort(key=lambda t: 'ERD'.index(t[1][0]))
    for kind, txt in (('early_smoke', 'No early cluster of 8 or more smokes.'), ('radar', 'No radar address: no cap has 8 or more radar plays here.'), ('deaths', 'No death cluster of 8 or more smokes.')):
        if not cnt[kind]: notes2.append((MUTED, txt))
    fig.add(p)
    # ----- legend and notes
    y = 72
    x = X1
    def leg(svg, lab, w):
        nonlocal x
        fig.add(svg + T(x + 20, y + 4, lab, size=11.5, fill=INK, anchor='start')); x += w
    leg(f'<circle cx="{x + 7}" cy="{y}" r="4" fill="{BLUE}"/>', 'Top 6 smoke', 100)
    leg(f'<circle cx="{x + 7}" cy="{y}" r="4" fill="{ORANGE}"/>', 'Rest smoke', 96)
    leg(f'<ellipse cx="{x + 7}" cy="{y}" rx="9" ry="6" fill="none" stroke="{C_SIG}" stroke-width="2.6"/>', 'signature (dashed = lead)', 172)
    leg(f'<rect x="{x}" y="{y - 7}" width="14" height="14" fill="{C_HIGH}" fill-opacity="0.35" stroke="{C_HIGH}" stroke-width="1.6"/>', 'high / best cell', 112)
    leg(f'<rect x="{x}" y="{y - 7}" width="14" height="14" fill="{C_LOW}" fill-opacity="0.35" stroke="{C_LOW}" stroke-width="1.6"/>', 'low / lowest cell', 122)
    leg(diamond(x + 7, y, C_CRU), 'cruiser inside (mean)', 150)
    leg(triangle(x + 7, y - 1, C_DD2), 'second destroyer (mean)', 168)
    leg(f'<ellipse cx="{x + 7}" cy="{y}" rx="9" ry="6" fill="none" stroke="{C_EARLY}" stroke-width="2.6"/>', 'early cluster', 104)
    leg(f'<rect x="{x + 3}" y="{y - 4}" width="8" height="8" fill="none" stroke="{C_RADAR}" stroke-width="1.8"/>', 'radar play / address', 142)
    x = X1; y = 96
    leg(f'<path d="M{x + 3},{y - 4} L{x + 11},{y + 4} M{x + 3},{y + 4} L{x + 11},{y - 4}" stroke="{C_DEATH}" stroke-width="1.8"/>', 'smoke with a death (dotted outline = death cluster)', 330)
    fig.add(T(x + 20, y + 4, 'Cell labels = concealed damage per destroyer smoke.  * = small n (8 to 14).  Left: every destroyer and cruiser smoke centre. Right: destroyer smokes of the first 5 minutes.', size=11, anchor='start'))
    yn = Y0 + SIZE + 34
    def wrap(txt, width=100):
        out, cur = [], ''
        for w in txt.split():
            if len(cur) + len(w) + 1 > width: out.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        return out + [cur]
    hmax = 0
    for x0, notes in ((X1, notes1), (X2, notes2)):
        yy = yn
        for col, txt in notes:
            for j, line in enumerate(wrap(txt)):
                if j == 0: fig.add(f'<rect x="{x0}" y="{yy - 9}" width="9" height="9" rx="2" fill="{col}"/>')
                fig.add(T(x0 + 15, yy, line, size=11, fill=INK if j == 0 else MUTED, anchor='start')); yy += 15
            yy += 3
        hmax = max(hmax, yy)
    fig.h = hmax + 14
    fig.body[0] = f'<rect width="{fig.w}" height="{fig.h}" fill="{BG}"/>' + fig.body[0][fig.body[0].index('<text'):]
    fig.save(os.path.join(FIG, f'map-{code}'))
    print('figure', m, fig.w, fig.h)

def clan_figure():
    """Part D's two style figures, re-pointed at ../maps/ so the package is self-contained, re-rendered to PNG."""
    src = os.path.join(ANALYSIS, 'round4', 'part-d')
    for a, b in (('fig-style-maps', 'clan-styles'), ('fig-style-numbers', 'clan-styles-numbers')):
        svg = open(os.path.join(src, a + '.svg'), encoding='utf-8').read().replace('../../round3/maps/', '../maps/')
        open(os.path.join(FIG, b + '.svg'), 'w', encoding='utf-8').write(svg)
        import re
        w, h = (int(x) for x in re.search(r'width="(\d+)" height="(\d+)"', svg).groups())
        render_png(os.path.join(FIG, b + '.svg'), w, h)
        print('figure', b, w, h)

if __name__ == '__main__':
    os.makedirs(FIG, exist_ok=True)
    want = sys.argv[1:]
    for m in MAP_ORDER:
        if not want or MAP_CODE[m] in want: map_figure(m)
    if not want or 'clan' in want: clan_figure()
