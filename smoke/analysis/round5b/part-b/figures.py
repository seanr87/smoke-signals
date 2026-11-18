# Round 5 part B working figures. Run: python -I -X utf8 figures.py  -> round5/figures/b*.svg + .png
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
import math
S, G = load5()
FIGS = os.path.join(R5, 'figures')
def of(ship): return [s for s in S if s['ship'] == ship]
def own_share(ss):
    t = sum(x['conc'] for s in ss for x in s['shooters']); return 100 * sum(x['conc'] for s in ss for x in s['shooters'] if x['is_smoker']) / t if t else None

# ---- b1: distance to cap edge, every smoke, by ship
ships = ['Daring', 'Gdańsk', 'Z-42', 'Z-52', 'Grozovoi', 'Shimakaze']
W, H = 1100, 145 + 78 * len(ships)
fig = Fig(W, H, 'B1. Cap sitters: distance from the smoke edge to the contested cap edge', 'One dot per smoke. Left of the zero line = inside the cap. Black tick = median. Top 6 blue (upper band), Rest orange (lower band).')
x0, x1 = 170, W - 40; lo, hi = -3000, 12000
X = lambda v: x0 + (min(hi, max(lo, v)) - lo) / (hi - lo) * (x1 - x0)
for km in range(-2, 13, 2):
    fig.add(f'<line x1="{X(km*1000):.1f}" y1="92" x2="{X(km*1000):.1f}" y2="{H-34}" stroke="{GRID}" stroke-width="1"/>' + T(X(km * 1000), H - 18, f'{km} km', size=10.5))
fig.add(f'<line x1="{X(0):.1f}" y1="88" x2="{X(0):.1f}" y2="{H-34}" stroke="{INK}" stroke-width="1.2"/>' + T(X(0) - 6, 86, 'inside the cap', size=10.5, anchor='end') + T(X(0) + 6, 86, 'outside', size=10.5, anchor='start'))
random.seed(7)
for i, sh in enumerate(ships):
    ss = of(sh); y = 100 + i * 78
    fig.add(T(x0 - 14, y + 30, sh, size=13, fill=INK, anchor='end', weight='600') + T(x0 - 14, y + 46, f'n = {len(ss)}' + (' (small n)' if len(ss) < 15 else ''), size=10.5, anchor='end')
            + T(x0 - 14, y + 60, f"{100*sum(s['inside'] for s in ss)/len(ss):.0f}% inside", size=10.5, anchor='end'))
    for g, yy in (('top', y + 6), ('rest', y + 38)):
        for s in ss:
            if s['grp'] != g: continue
            fig.add(f'<circle cx="{X(s["edge"]):.1f}" cy="{yy + random.random()*26:.1f}" r="3" fill="{GROUP_COLOR[g]}" opacity="0.55"/>')
    m = med(s['edge'] for s in ss)
    fig.add(f'<line x1="{X(m):.1f}" y1="{y+2}" x2="{X(m):.1f}" y2="{y+68}" stroke="{INK}" stroke-width="2.5"/>' + T(X(m) + 5, y + 76, f'median {m:,.0f} m', size=10, fill=INK, anchor='start'))
fig.legend(x0, 68, [('Top 6', BLUE), ('Rest', ORANGE)])
fig.save(os.path.join(FIGS, 'b1-cap-sitters-distance'))

# ---- b3: long smokes on two maps (paths), three ships
maps = ['Sleeping Giant', 'Hotspot']; lships = ['Harugumo', 'Somers', 'Gearing']
fig = Fig(60 + 3 * 345, 110 + 2 * 380, 'B3. Long smokes: where Harugumo, Somers and Gearing lay them', 'Each line is one smoke as laid (team-normalized). Top 6 blue, Rest orange. A ring marks a smoke where the smoker itself did 5,000+ concealed damage.')
for r, m in enumerate(maps):
    for c, sh in enumerate(lships):
        ss = [s for s in of(sh) if s['map'] == m]
        p = Panel(m, 50 + c * 345, 120 + r * 380, 300, G, title=f'{sh} on {m} (n = {len(ss)})')
        for s in ss:
            p.line(s['npath'], stroke=GROUP_COLOR[s['grp']], width=2.2, opacity=0.6)
            if sum(x['conc'] for x in s['shooters'] if x['is_smoker']) >= 5000: p.ring(s['nx'], s['nz'], 7, stroke=INK, width=1.6)
        fig.add(p)
fig.legend(50, 72, [('Top 6', BLUE), ('Rest', ORANGE)])
fig.save(os.path.join(FIGS, 'b3-long-smokes-maps'))

# ---- b3: who deals the concealed damage (own-gun share) and second destroyer / radar cruiser shares
fig = Fig(980, 430, 'B3. Harugumo fires from its own smoke; Somers and Gearing smoke for others', "Left: the smoker's own share of the concealed damage from its smokes. Right: share of smokes where the smoker did any concealed damage. Top 6 blue, Rest orange.")
rows1 = []; rows2 = []
for sh in ('Harugumo', 'Somers', 'Gearing', 'Delny'):
    ss = of(sh); t = [s for s in ss if s['grp'] == 'top']; r = [s for s in ss if s['grp'] == 'rest']
    rows1.append((sh, {'top': own_share(t) if len(t) >= 8 else None, 'rest': own_share(r) if len(r) >= 8 else None}, f'n {len(t)} / {len(r)}'))
    anyf = lambda v: 100 * sum(1 for s in v if any(x['is_smoker'] and x['conc'] > 0 for x in s['shooters'])) / len(v) if len(v) >= 8 else None
    rows2.append((sh, {'top': anyf(t), 'rest': anyf(r)}, f'n {len(t)} / {len(r)}'))
fig.add(T(30, 92, "Smoker's own share of concealed damage, %", size=12.5, fill=INK, anchor='start', weight='600')); bar_rows(fig, 30, 104, 440, rows1, vmax=50, fmt='{:.0f}%', row_h=44, label_w=90)
fig.add(T(510, 92, 'Smokes where the smoker did concealed damage, %', size=12.5, fill=INK, anchor='start', weight='600')); bar_rows(fig, 510, 104, 440, rows2, vmax=60, fmt='{:.0f}%', row_h=44, label_w=90)
fig.add(T(30, 320, 'Delny Rest has 4 smokes: too few, no bar. Right-hand numbers: smokes Top 6 / Rest.', size=11, anchor='start'))
fig.legend(30, 68, [('Top 6', BLUE), ('Rest', ORANGE)])
fig.save(os.path.join(FIGS, 'b3-own-gun-share'))

# ---- b4: length laid, histogram on a log scale
hs = ['Daring', 'Gdańsk', 'Grozovoi', 'Shimakaze', 'Somers']
edges = [10 ** (1.5 + i * 0.125) for i in range(21)]  # 32 m to 10 km
W, H = 1000, 110 + 118 * len(hs)
fig = Fig(W, H, 'B4. Length of smoke laid: one hump or two?', 'Bars = number of smokes by length laid (log scale). Top 6 blue stacked on Rest orange. Dashed lines: 500 m (parked below) and 1 km (line above).')
x0, x1 = 170, W - 40
X = lambda m: x0 + (math.log10(m) - 1.5) / 2.5 * (x1 - x0)
for i, sh in enumerate(hs):
    ss = [s for s in of(sh) if s['path_m'] is not None]; y0 = 100 + i * 118; hh = 84
    cnt = [[0, 0] for _ in range(20)]
    for s in ss:
        k = min(19, max(0, int((math.log10(max(s['path_m'], 32)) - 1.5) / 0.125))); cnt[k][0 if s['grp'] == 'rest' else 1] += 1
    mx = max(a + b for a, b in cnt) or 1
    kn = [s for s in ss]
    pk = 100 * sum(1 for s in kn if s['path_m'] < 500) / len(kn); bt = 100 * sum(1 for s in kn if 500 <= s['path_m'] < 1000) / len(kn); ln = 100 * sum(1 for s in kn if s['path_m'] >= 1000) / len(kn)
    fig.add(T(x0 - 14, y0 + 30, sh, size=13, fill=INK, anchor='end', weight='600') + T(x0 - 14, y0 + 46, f'n = {len(ss)}', size=10.5, anchor='end')
            + T(x0 - 14, y0 + 62, f'{pk:.0f}% / {bt:.0f}% / {ln:.0f}%', size=10.5, anchor='end') + T(x0 - 14, y0 + 76, 'under 500 m / between / 1 km+', size=8.5, anchor='end'))
    fig.add(f'<line x1="{x0}" y1="{y0+hh}" x2="{x1}" y2="{y0+hh}" stroke="{MUTED}" stroke-width="1"/>')
    for k, (a, b) in enumerate(cnt):
        bx = X(edges[k]) + 1; bw = X(edges[k + 1]) - X(edges[k]) - 2
        ha = a / mx * hh; hb = b / mx * hh
        if a: fig.add(f'<rect x="{bx:.1f}" y="{y0+hh-ha:.1f}" width="{bw:.1f}" height="{ha:.1f}" fill="{ORANGE}"/>')
        if b: fig.add(f'<rect x="{bx:.1f}" y="{y0+hh-ha-hb:.1f}" width="{bw:.1f}" height="{hb:.1f}" fill="{BLUE}"/>')
        if a + b == mx: fig.add(T(bx + bw / 2, y0 + hh - ha - hb - 3, str(a + b), size=9.5))
    for v in (500, 1000):
        fig.add(f'<line x1="{X(v):.1f}" y1="{y0-4}" x2="{X(v):.1f}" y2="{y0+hh}" stroke="{INK}" stroke-width="1" stroke-dasharray="4 3" opacity="0.7"/>')
for v, lab in ((50, '50 m'), (100, '100 m'), (200, '200 m'), (500, '500 m'), (1000, '1 km'), (2000, '2 km'), (5000, '5 km'), (10000, '10 km')):
    fig.add(T(X(v), H - 12, lab, size=10.5))
fig.legend(x0, 72, [('Top 6', BLUE), ('Rest', ORANGE)])
fig.save(os.path.join(FIGS, 'b4-length-laid'))

# ---- b4: hybrids on the map: parked dots and moving lines
maps = ['Hotspot', 'Loop']; hy = ['Grozovoi', 'Shimakaze', 'Daring', 'Gdańsk']
fig = Fig(50 + 4 * 285, 110 + 2 * 320, 'B4. Hybrids on the map: parked smokes (dots) and smokes laid over 1 km+ (lines)', 'Team-normalized. Top 6 blue, Rest orange. Short moving smokes (500 m to 1 km) are small hollow rings.')
for r, m in enumerate(maps):
    for c, sh in enumerate(hy):
        ss = [s for s in of(sh) if s['map'] == m]
        p = Panel(m, 40 + c * 285, 120 + r * 320, 250, G, title=f'{sh} on {m} (n = {len(ss)})')
        for s in ss:
            col = GROUP_COLOR[s['grp']]
            if s['path_m'] is not None and s['path_m'] >= 1000: p.line(s['npath'], stroke=col, width=2.2, opacity=0.7)
            elif s['movement'] == 'stationary': p.dot(s['nx'], s['nz'], r=4, fill=col, opacity=0.7)
            else: p.ring(s['nx'], s['nz'], 4, stroke=col, width=1.6, opacity=0.9)
        fig.add(p)
fig.legend(40, 72, [('Top 6', BLUE), ('Rest', ORANGE)])
fig.save(os.path.join(FIGS, 'b4-hybrids-maps'))
print('figures ok')
