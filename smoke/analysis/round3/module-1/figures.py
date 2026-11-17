# Module 1 figures. Run: python -I -X utf8 smoke/analysis/round3/module-1/figures.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from m1 import *

# common.Panel names its clip path by id(self); keep every panel alive so ids are never reused within a figure.
KEEP = []
_Panel = Panel
def Panel(*a, **k):
    p = _Panel(*a, **k); KEEP.append(p); return p

def draw_smokes(p, ss, death_rings=False, opacity=0.5):
    """Each smoke at its true size: the laid path as a band one smoke-diameter wide, plus a dot at its centre."""
    for s in ss:
        col = GROUP_COLOR[s['grp']]; w = max(2.0, 2 * p.px(s['radius_m']))
        if len(s['npath']) > 1: p.line(s['npath'], stroke=col, width=w, opacity=opacity * 0.7)
        p.dot(s['nx'], s['nz'], r=max(1.8, w / 2), fill=col, opacity=opacity)
    if death_rings:
        for s in ss:
            if s['deaths']: p.ring(s['nx'], s['nz'], 6.5, stroke=RED, width=1.8)

# ---- Figure 1a / 1b: every ship on every map
def ship_by_map(ships, name, title):
    size, px, py = 150, 168, 190
    fig = Fig(100 + 7 * px + 4, 100 + len(ships) * py + 10, title,
              'Each mark is one smoke at true size, team-normalized (own spawn at the bottom; Okinawa bottom left). Blue = Top 6, orange = Rest. Grey panel = under 8 smokes, not plotted.')
    fig.legend(24, 70, [('Top 6', BLUE), ('Rest', ORANGE)])
    for r, sh in enumerate(ships):
        y0 = 118 + r * py
        fig.add(T(8, y0 + size / 2 - 4, sh, size=13, fill=INK, anchor='start', weight='700') + T(8, y0 + size / 2 + 12, f'n = {len(BY[sh])}', size=10.5, anchor='start')
                + T(8, y0 + size / 2 + 26, KIND[sh], size=10.5, fill=KIND_COLOR[KIND[sh]], anchor='start', weight='600'))
        for c, m in enumerate(MAPLIST):
            ss = [s for s in BY[sh] if s['map'] == m]; n = len(ss)
            few = n < 8
            p = Panel(m, 100 + c * px, y0, size, G, title=f'{m} · {n}' + (' small n' if 8 <= n < 15 else ''), dim=0.82 if few else 0.4, grid_labels=(r == 0), normalized=False)
            if few: p.raw(T(p.x0 + size / 2, p.y0 + size / 2 + 4, f'{n} smokes, not plotted', size=10, fill=MUTED, halo=True))
            else: draw_smokes(p, ss, opacity=0.55)
            fig.add(p)
    fig.save(os.path.join(OUT, name))

# ---- Figure 2: where each cluster smokes (cell heat)
def cluster_heat(clusters, names):
    size, px, py = 150, 168, 205
    fig = Fig(100 + 7 * px + 4, 96 + len(clusters) * py + 10, 'Where each cluster of ships smokes, by map',
              'Cell shade and number = % of that cluster\'s smokes on the map that sit in the cell (cells of 4% or more). Team-normalized: own spawn at the bottom (Okinawa bottom left).')
    for r, (cl, nm) in enumerate(zip(clusters, names)):
        y0 = 122 + r * py
        allss = [s for sh in cl for s in BY[sh]]
        fig.add(T(24, y0 - 30, f'{nm}: {", ".join(cl)} (n = {len(allss)})', size=13, fill=INK, anchor='start', weight='700'))
        for c, m in enumerate(MAPLIST):
            ss = [s for s in allss if s['map'] == m]; n = len(ss)
            p = Panel(m, 100 + c * px - 76, y0, size, G, title=f'{m} · {n}' + (' small n' if n < 15 else ''), dim=0.45, grid_labels=False, normalized=False)
            if n >= 8:
                for (cc, rr), k in C(s['ncell'] for s in ss).items():
                    v = 100 * k / n
                    if v >= 4: p.cellfill(cc, rr, seq_color(v, 30), opacity=0.82, text=f'{v:.0f}', text_fill=seq_text(v, 30))
            else: p.raw(T(p.x0 + size / 2, p.y0 + size / 2 + 4, f'{n} smokes, not plotted', size=10, fill=MUTED, halo=True))
            fig.add(p)
    fig.save(os.path.join(OUT, 'fig2-cluster-cells'))

# ---- Figure 3: profile table, dendrogram, distance matrix
SHORT = {'edge': 'to cap m', 'inside': 'in cap %', 'fwd': 'up map %', 'el': 'time s', 'early': 'early %', 'stat': 'still %', 'push': 'push %', 'kite': 'kite %', 'horiz': 'sideways %',
         'selfish': 'selfish %', 'screen': 'screen %', 'stacked': 'stacked %', 'capc': 'cap fight %', 'nopp': 'no tag %', 'dmg': 'damage %', 'esc': 'escape %', 'conc': 'conc dmg', 'deaths': 'deaths /100'}
def cluster_fig(Z, merges, order, clusters, names, ccol):
    own = {sh: i for i, c in enumerate(clusters) for sh in c}
    keys = [f[0] for f in FEATS]; Zall, _ = zscores(PROF, SHIPS, keys)
    rh, cw = 26, 50; x_d, x_l, x_t = 24, 170, 318; y_t = 120
    W = x_t + cw * len(keys) + 20; H = y_t + rh * len(order) + 60 + 30 + 14 * 27 + 50
    fig = Fig(W, H, 'Ship smoke profiles and how they cluster',
              'Rows in clustering order. Cell colour = how far the ship is above (blue) or below (orange) the 14-ship average. The last two columns (outcomes) were not used for clustering.')
    ypos = {sh: y_t + i * rh + rh / 2 for i, sh in enumerate(order)}
    # dendrogram
    hmax = merges[-1][2]; node = {(sh,): (ypos[sh], 0.0) for sh in order}
    X = lambda h: x_l - 8 - (x_l - 8 - x_d) * h / hmax
    for a, b, h in merges:
        (ya, ha), (yb, hb) = node[tuple(a)], node[tuple(b)]
        fig.add(f'<path d="M{X(ha):.1f},{ya:.1f} H{X(h):.1f} V{yb:.1f} H{X(hb):.1f}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
        node[tuple(a + b)] = ((ya + yb) / 2, h)
    fig.add(T(x_d, y_t - 8, 'less alike', size=9.5, anchor='start') + T(x_l - 8, y_t - 8, 'alike', size=9.5, anchor='end'))
    for j, k in enumerate(keys):
        a, b = SHORT[k].rsplit(' ', 1)
        fig.add(T(x_t + j * cw + cw / 2, y_t - 20, a, size=9.5, fill=INK) + T(x_t + j * cw + cw / 2, y_t - 8, b, size=9.5, fill=INK))
    fig.add(T(x_t + 16 * cw + cw, y_t - 34, 'outcomes', size=9.5, weight='600'))
    for sh in order:
        y = ypos[sh]
        fig.add(f'<rect x="{x_l}" y="{y-rh/2+2:.1f}" width="6" height="{rh-4}" fill="{ccol[own[sh]]}"/>' + T(x_l + 12, y + 4, sh, size=12, fill=INK, anchor='start', weight='600')
                + T(x_t - 8, y - 1, KIND[sh], size=9, fill=KIND_COLOR[KIND[sh]], anchor='end', weight='600') + T(x_t - 8, y + 9, f'n {len(BY[sh])}', size=8.5, anchor='end'))
        for j, k in enumerate(keys):
            z = Zall[sh][j]; x = x_t + j * cw + (6 if j >= 16 else 0)
            fig.add(f'<rect x="{x+1}" y="{y-rh/2+1:.1f}" width="{cw-2}" height="{rh-2}" rx="2" fill="{div_color(z, 2)}"/>' + T(x + cw / 2, y + 4, FKEY[k][3].format(PROF[sh][k]), size=10, fill=BG if abs(z) > 1.4 else INK))
    yl = y_t + rh * len(order) + 22
    fig.legend(x_l, yl, [(names[i], ccol[i]) for i in range(len(names))])
    fig.add(T(x_l, yl + 20, 'Smoke type (the lens to compare against) is the coloured word under each ship name: ' + ', '.join(KIND_COLOR), size=10.5, anchor='start'))
    # distance matrix
    y_m = yl + 78; c2 = 27; x_m = x_l + 96
    fig.add(T(24, y_m - 34, 'How alike two ships are (0 = identical profile; darker = more alike)', size=13, fill=INK, anchor='start', weight='600'))
    for i, a in enumerate(order):
        fig.add(T(x_m - 6, y_m + i * c2 + c2 / 2 + 4, a, size=10.5, fill=INK, anchor='end') + f'<rect x="{x_m-100}" y="{y_m+i*c2+3}" width="5" height="{c2-6}" fill="{ccol[own[a]]}"/>')
        fig.add(T(x_m + i * c2 * 1.6 + c2 * 0.8, y_m - 6, a[:7], size=8.5, fill=INK))
        for j, b in enumerate(order):
            d = dist(Z[a], Z[b]); v = max(0, 2.2 - d)
            fig.add(f'<rect x="{x_m+j*c2*1.6+1:.1f}" y="{y_m+i*c2+1}" width="{c2*1.6-2:.1f}" height="{c2-2}" rx="2" fill="{seq_color(v, 2.2)}"/>' + T(x_m + j * c2 * 1.6 + c2 * 0.8, y_m + i * c2 + c2 / 2 + 4, f'{d:.1f}', size=9.5, fill=seq_text(v, 2.2)))
    fig.save(os.path.join(OUT, 'fig3-profile-clusters'))

# ---- Figure 4: Top 6 vs rest, same ship, same map
PLAYS = [('Somers', 'Sleeping Giant'), ('Harugumo', 'Sleeping Giant'), ('Daring', 'Sleeping Giant'), ('Gdańsk', 'Sleeping Giant'),
         ('Gearing', 'Hotspot'), ('Gearing', 'Mountain Range'), ('Somers', 'Mountain Range'), ('Svea', 'Land of Fire')]
def plays_fig():
    size, px, py = 285, 308, 350
    fig = Fig(40 + 4 * px, 110 + 2 * py + 6, 'Same ship, same map: where Top 6 and Rest put the smoke',
              'Each mark is one smoke at true size. Blue = Top 6, orange = Rest. Red ring = a ship was lost in that smoke. Own spawn at the bottom (north-spawn teams mirrored north-south).')
    fig.legend(24, 70, [('Top 6', BLUE), ('Rest', ORANGE), ('ship lost in the smoke (ring)', RED)])
    fig.add(T(40 + 4 * px - 20, 71, 'Numbers in titles = smokes. * = one group has under 15 smokes (small n).', size=11.5, anchor='end'))
    for i, (sh, m) in enumerate(PLAYS):
        ss = [s for s in BY[sh] if s['map'] == m]; a = sum(s['grp'] == 'top' for s in ss); b = len(ss) - a
        p = Panel(m, 40 + (i % 4) * px, 126 + (i // 4) * py, size, G, title=f'{sh}, {m}: Top 6 {a}, Rest {b}' + (' *' if min(a, b) < 15 else ''), dim=0.42)
        draw_smokes(p, ss, death_rings=True, opacity=0.6); fig.add(p)
    fig.save(os.path.join(OUT, 'fig4-top-vs-rest-maps'))

if __name__ == '__main__':
    which = sys.argv[1:] or ['1', '2', '3', '4']
    Z, par = zscores(PROF, SHIPS, CLUSTER_KEYS); merges, order = agglomerate(Z, SHIPS)
    cl = cut(merges, SHIPS, 4)
    pick = lambda sh: next(c for c in cl if sh in c)
    clusters = [pick('Somers'), pick('Daring'), pick('Svea'), pick('Napoli')]
    names = ['Flank smoke lines', 'Cap sitters', 'Parked cruiser smoke', 'Moving exhaust cover']; ccol = [BLUE, ORANGE, VIOLET, AQUA]
    if '1' in which:
        ship_by_map(['Somers', 'Gearing', 'Harugumo', 'Delny', 'Gdańsk', 'Shimakaze'], 'fig1a-ship-by-map-long-smoke', 'Where each ship smokes, by map (1 of 2): standard long destroyer smoke')
        ship_by_map(['Grozovoi', 'Daring', 'Z-42', 'Svea', 'Napoli'], 'fig1b-ship-by-map-short-cruiser-exhaust', 'Where each ship smokes, by map (2 of 2): Grozovoi, short destroyer smoke, cruiser smoke, exhaust')
    if '2' in which: cluster_heat(clusters, names)
    if '3' in which: cluster_fig(Z, merges, order, clusters, names, ccol)
    if '4' in which: plays_fig()
    print('done', which)
