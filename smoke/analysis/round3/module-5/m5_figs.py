import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5lib import *
from m5_cluster import *
which = sys.argv[1:] or list('123456')
OUT = lambda n: os.path.join(HERE5, n)
GREY = '#8a8985'

def hstack(fig, x, y, w, rows, segs, vmax, row_h=20, label_w=110, fmt='{:.0f}', total_fmt=None):
    """Stacked horizontal bars. rows: [(label, [values per segment], right note)]; segs: [colour]."""
    for lab, vals, note in rows:
        fig.add(T(x + label_w - 8, y + row_h / 2 + 4, lab, size=11.5, fill=INK, anchor='end'))
        bx = x + label_w
        for v, col in zip(vals, segs):
            bw = (w - label_w - 80) * v / vmax
            if bw > 0.3:
                fig.add(f'<rect x="{bx:.1f}" y="{y+3}" width="{max(0.5, bw-1):.1f}" height="{row_h-6}" rx="2" fill="{col}"/>')
                if bw > 24: fig.add(T(bx + bw / 2, y + row_h / 2 + 3.5, fmt.format(v), size=9.5, fill=BG, weight='600'))
            bx += bw
        if total_fmt: fig.add(T(bx + 4, y + row_h / 2 + 3.5, total_fmt.format(sum(vals)), size=9.5, anchor='start'))
        if note is not None: fig.add(T(x + w, y + row_h / 2 + 4, str(note), size=9.5, anchor='end'))
        y += row_h
    return y

if '1' in which:
    pair = collections.defaultdict(list)
    for s in DD:
        seen = {}
        for p in s['partners']: seen.setdefault(p['ship'], 0.0)
        for x in s['shooters']:
            if not x['is_smoker']: seen[x['ship']] = seen.get(x['ship'], 0.0) + x['conc']
        for ship, v in seen.items(): pair[(s['ship'], ship)].append((v, s))
    rows = sorted(((kk, len(v), mean(a for a, _ in v), len({s['team'] for _, s in v})) for kk, v in pair.items() if len(v) >= 20), key=lambda r: -r[2])
    for kk, n, m, nc in rows:
        v = pair[kk]; print(kk, n, k(m), 'clans', nc, 'ci', ci(boot_stat([dict(s, pv=a) for a, s in v], lambda ss: mean(x['pv'] for x in ss)), '{:,.0f}'), 'maps', C(s['map'] for _, s in v).most_common(3))
    def share(ss, cls=None, smoker=None):
        tot = sum(x['conc'] for s in ss for x in s['shooters'])
        return 100 * sum(x['conc'] for s in ss for x in s['shooters'] if (cls is None or x['cls'] == cls) and (smoker is None or x['is_smoker'] == smoker)) / tot if tot else 0
    fig = Fig(1240, 560, 'Who shoots from destroyer smoke', 'Destroyer smokes. Concealed damage (guns and torpedoes) while hidden by the smoke. Association only.')
    fig.add(T(24, 84, 'Best destroyer + shooter pairs: concealed damage by the shooter ship per smoke', size=12.5, fill=INK, anchor='start', weight='600'))
    fig.add(T(24, 100, 'Counted on every smoke where that ship was covered or fired. Pairs with 20+ smokes. Right column: smokes / clans.', size=10.5, anchor='start'))
    y = bar_rows(fig, 24, 112, 500, [(f'{a} + {b}', m, f'{n} / {nc}') for (a, b), n, m, nc in rows], label_w=170, row_h=24)
    y += 34
    fig.add(T(24, y, 'Who deals the concealed damage (share, %)', size=12.5, fill=INK, anchor='start', weight='600'))
    segs = [(BLUE, 'the smoking destroyer'), (ORANGE, 'cruisers'), (VIOLET, 'battleships'), (GREY, 'other destroyers')]
    fig.legend(24, y + 22, [(l, c) for c, l in segs])
    grows = []
    for lab, ss in (('Top 6', [s for s in DD if s['grp'] == 'top']), ('Rest', [s for s in DD if s['grp'] == 'rest']), ('H-SR', [s for s in DD if s['team'] == 'H-SR']), ('PN (small n)', [s for s in DD if s['is_pn']])):
        grows.append((lab, [share(ss, smoker=True), share(ss, 'cruiser'), share(ss, 'battleship'), share(ss, 'destroyer', False)], f'n {len(ss)}'))
    hstack(fig, 24, y + 36, 500, grows, [c for c, _ in segs], 100, row_h=24, label_w=100)
    # map view: the most used pair on its most used map
    (a, b), n, m, nc = max(rows, key=lambda r: r[1])
    mp = C(s['map'] for _, s in pair[(a, b)]).most_common(1)[0][0]
    ss = [(v, s) for v, s in pair[(a, b)] if s['map'] == mp]
    p = Panel(mp, 600, 110, 400, G, title=f'{a} smoke + {b}: {mp}, {len(ss)} smokes' + small(len(ss)))
    for v, s in ss:
        p.line(s['npath'], stroke=BLUE, width=3, opacity=0.75)
        for pt in s['partners']:
            if pt['ship'] == b and pt['nx'] is not None:
                p.line([(s['nx'], s['nz']), (pt['nx'], pt['nz'])], stroke=INK, width=0.7, opacity=0.35)
                p.dot(pt['nx'], pt['nz'], r=4, fill=ORANGE, opacity=0.9, stroke=BG)
    fig.add(p)
    fig.add(f'<line x1="1020" y1="130" x2="1046" y2="130" stroke="{BLUE}" stroke-width="3"/>' + T(1052, 134, f'{a} smoke as laid', size=11, fill=INK, anchor='start'))
    fig.add(f'<circle cx="1033" cy="152" r="4.5" fill="{ORANGE}"/>' + T(1052, 156, f'{b} it covered,', size=11, fill=INK, anchor='start') + T(1052, 170, 'when the smoke finished', size=11, fill=INK, anchor='start'))
    fig.add(T(1020, 196, 'Thin line joins a smoke', size=10.5, anchor='start') + T(1020, 210, 'to the cruiser it covered.', size=10.5, anchor='start'))
    print('map', mp, len(ss), 'conc on map', k(mean(v for v, _ in ss)), 'clans', C(s['team'] for _, s in ss), 'cells', C(s['ncell_name'] for _, s in ss).most_common(5), 'dist smoke-partner m', med(math.hypot(s['nx'] - pt['nx'], s['nz'] - pt['nz']) * WU for _, s in ss for pt in s['partners'] if pt['ship'] == b and pt['nx'] is not None), 'how', C(pt['how'] for _, s in ss for pt in s['partners'] if pt['ship'] == b))
    fig.save(OUT('fig1-partnerships'))

if '2' in which:
    kinds = ['long DD', 'short DD', 'cruiser', 'exhaust']
    lab = ['long\nDD', 'short\nDD', 'cruiser', 'exhaust']
    own = lambda ss: (100 * sum(x['conc'] for s in ss for x in s['shooters'] if x['is_smoker']) / max(1, sum(x['conc'] for s in ss for x in s['shooters'])))
    K = {kd: [s for s in S if s['kind'] == kd] for kd in kinds}
    fig = Fig(1240, 400, 'Four kinds of smoke, field-wide', 'All classes, all clans. Long DD = standard destroyer smoke; short DD = Daring and Z-42 (10 s lay, 40 s life). Black lines: 95% interval. n: ' + ', '.join(f'{kd} {len(K[kd])}' for kd in kinds) + '.')
    col = {'v': BLUE}
    panels = [('Smokes per team-game', [len(K[kd]) / len(TG) for kd in kinds], None, '{:.2f}'),
              ('Concealed damage per smoke (thousands)', [conc_per(K[kd]) / 1000 for kd in kinds], [tuple(v / 1000 for v in boot_stat(K[kd], conc_per)) for kd in kinds], '{:.1f}'),
              ('Deaths in the smoke per 100 smokes', [d100(K[kd]) for kd in kinds], [boot_stat(K[kd], d100) for kd in kinds], '{:.1f}'),
              ('Own-gun share: % of damage by the smoker', [own(K[kd]) for kd in kinds], [boot_stat(K[kd], own) for kd in kinds], '{:.0f}')]
    for i, (title, vals, err, fmt) in enumerate(panels):
        x = 60 + i * 300
        fig.add(T(x - 20, 92, title, size=12, fill=INK, anchor='start', weight='600'))
        vbars(fig, x, 120, 240, 200, lab, [('v', vals)], fmt=fmt, colors=col, err={'v': err} if err else None, ymax=[2.8, 16, 24, 100][i])
    fig.save(OUT('fig2-smoke-types'))

if '3' in which:
    bins = list(range(0, 960, 120))
    def expo(grp, b): return sum(max(0, min(G[gk]['len'], b + 120) - b) / 120 for gk, t in TG if G[gk]['len'] and grp_of(t) == grp)
    def crate(clans, lo):
        e = sum(max(0, min(G[gk]['len'], lo + 120) - lo) / 120 for c in clans for gk, t in TG if t == c and G[gk]['len'])
        n = sum(1 for c in clans for s in DD if s['team'] == c and lo <= s['el'] < lo + 120 and G[s['game']]['len'])
        return n / e if e else None
    fig = Fig(1240, 420, 'When destroyers smoke, and what it returns', 'Destroyer smokes. Top 6 blue, rest orange. Black lines: 95% interval (resampling clans). 3 games with no recorded length are left out of the rate. Association only.')
    fig.legend(900, 30, [('Top 6', BLUE), ('Rest', ORANGE)])
    cats = [f'{b//60}-{b//60+2}' for b in bins]
    rate = {g: [len([s for s in DD if s['grp'] == g and b <= s['el'] < b + 120 and G[s['game']]['len']]) / expo(g, b) for b in bins] for g in ('top', 'rest')}
    tops = [c for c in NG if c in TOP]; rest = [c for c in NG if c not in TOP]
    rerr = {}
    for g, cl in (('top', tops), ('rest', rest)):
        rerr[g] = [lohi([crate(random.choices(cl, k=len(cl)), b) for _ in range(400)]) for b in bins]
    fig.add(T(30, 92, 'Smokes per team per 2 minutes of game still running', size=12, fill=INK, anchor='start', weight='600'))
    vbars(fig, 50, 120, 400, 200, cats, [('top', rate['top']), ('rest', rate['rest'])], fmt='{:.2f}', colors=GROUP_COLOR, err=rerr, val_size=8, ymax=1.0)
    fig.add(T(250, 362, 'minutes into the game', size=10.5))
    conc = {g: [conc_per([s for s in DD if s['grp'] == g and b <= s['el'] < b + 120]) / 1000 for b in bins] for g in ('top', 'rest')}
    nn = {g: [len([s for s in DD if s['grp'] == g and b <= s['el'] < b + 120]) for b in bins] for g in ('top', 'rest')}
    print('bin n', nn)
    fig.add(T(480, 92, 'Concealed damage per smoke (thousands)', size=12, fill=INK, anchor='start', weight='600'))
    vbars(fig, 500, 120, 400, 200, [c + (f'\n{nn["top"][i]} / {nn["rest"][i]}') for i, c in enumerate(cats)], [('top', conc['top']), ('rest', conc['rest'])], fmt='{:.0f}', colors=GROUP_COLOR, val_size=8.5, ymax=20)
    fig.add(T(700, 374, 'minutes into the game; second line: smokes, top 6 / rest', size=10.5))
    st = lambda s: 'ahead by 50+' if s['score_diff'] >= 50 else 'behind by 50+' if s['score_diff'] <= -50 else 'level'
    states = ['ahead by 50+', 'level', 'behind by 50+']
    dv = {g: [d100([s for s in DD if s['grp'] == g and st(s) == x]) for x in states] for g in ('top', 'rest')}
    de = {g: [boot_stat([s for s in DD if s['grp'] == g and st(s) == x], d100) for x in states] for g in ('top', 'rest')}
    sn = {g: [len([s for s in DD if s['grp'] == g and st(s) == x]) for x in states] for g in ('top', 'rest')}
    fig.add(T(930, 92, 'Deaths in the smoke per 100, by score when laid', size=12, fill=INK, anchor='start', weight='600'))
    vbars(fig, 950, 120, 260, 200, [x + f'\n{sn["top"][i]} / {sn["rest"][i]}' for i, x in enumerate(states)], [('top', dv['top']), ('rest', dv['rest'])], fmt='{:.0f}', colors=GROUP_COLOR, err=de, ymax=48)
    fig.add(T(1080, 374, 'second line: smokes, top 6 / rest', size=10.5))
    pn = [s for s in DD if s['is_pn']]
    print('PN DD smokes el', sorted(s['el'] for s in pn), 'states', C(st(s) for s in pn), 'conc', k(conc_per(pn)))
    fig.save(OUT('fig3-timing'))

if '4' in which:
    isme = lambda s, d: d['player'] == s['player']
    sd = lambda ss: 100 * sum(1 for s in ss for d in s['j']['smoke_deaths'] if isme(s, d)) / len(ss)
    pd = lambda ss: 100 * sum(1 for s in ss for d in s['j']['smoke_deaths'] if not isme(s, d)) / len(ss)
    fig = Fig(1240, 740, 'Where and when ships die in destroyer smoke', 'Destroyer smokes: 1,074 smokes, 124 deaths (69 the smoking destroyer, 55 a covered teammate). Association only.')
    maps = ['Sleeping Giant', 'Okinawa', 'Land of Fire', 'Sea of Fortune']
    for i, m in enumerate(maps):
        ss = [s for s in DD if s['map'] == m]
        p = Panel(m, 40 + i * 300, 110, 262, G, title=f'{m}: {sum(s["deaths"] for s in ss)} deaths / {len(ss)} smokes')
        for s in ss:
            if not s['deaths']: p.dot(s['nx'], s['nz'], r=2.4, fill=BG, opacity=0.6)
        for s in ss:
            if s['deaths']:
                me = any(isme(s, d) for d in s['j']['smoke_deaths'])
                p.dot(s['nx'], s['nz'], r=4.5, fill=RED if me else VIOLET, opacity=0.9, stroke=BG)
        fig.add(p)
        print(m, 'death cells', C(s['ncell_name'] for s in ss if s['deaths']).most_common(5), 'own half share of deaths', pct([s for s in ss if s['deaths']], lambda s: s['ncell'][1] >= 5), 'of smokes', pct(ss, lambda s: s['ncell'][1] >= 5))
    fig.legend(40, 76, [('smoke with no death (pale dots)', '#d9d8d4'), ('the smoking destroyer died', RED), ('a covered teammate died', VIOLET)])
    segs = [RED, VIOLET]
    def block(x, y, title, key, order, w=380, lw=120, minn=15):
        fig.add(T(x, y, title, size=12.5, fill=INK, anchor='start', weight='600'))
        d = by(DD, key)
        rows = [(str(kk) + (' *' if len(d[kk]) < 15 else ''), [sd(d[kk]), pd(d[kk])], f'n {len(d[kk])}') for kk in order if len(d.get(kk, [])) >= minn]
        return hstack(fig, x, y + 8, w, rows, segs, 27, row_h=21, label_w=lw, fmt='{:.0f}', total_fmt='{:.1f}')
    y0 = 440
    fig.add(T(40, y0 - 12, 'Deaths per 100 smokes: red = the smoker, violet = a covered teammate. Number after the bar is the total.', size=11, anchor='start'))
    ships = [sh for sh, v in sorted(by(DD, 'ship').items(), key=lambda a: -len(a[1])) if len(v) >= 20]
    block(40, y0 + 14, 'By destroyer', 'ship', ships)
    y = block(440, y0 + 14, 'By distance from smoke edge to the cap', lambda s: band(s['edge']), BANDS)
    block(440, y + 26, 'By group', lambda s: GROUP_LABEL[s['grp']], ['Top 6', 'Rest'])
    y = block(840, y0 + 14, 'By who the smoke covered', 'coverage', ['stacked', 'screen', 'selfish'])
    y = block(840, y + 26, 'Enemy radar caught a ship in the smoke', lambda s: 'yes' if s['radar_on_us'] > 0 else 'no', ['no', 'yes'])
    block(840, y + 26, 'Score when laid', lambda s: 'ahead by 50+' if s['score_diff'] >= 50 else 'behind by 50+' if s['score_diff'] <= -50 else 'level', ['ahead by 50+', 'level', 'behind by 50+'])
    fig.save(OUT('fig4-survival'))

if '5' in which:
    clans, feats, X, Z = features()
    merges, order = agglomerate(Z)
    h = clans.index('H-SR')
    n = len(clans); rh = 21; cw = 46; x_d, x_l, x_h = 30, 170, 250; y0 = 190
    fig = Fig(x_h + cw * len(feats) + 110, y0 + rh * n + 60, 'Clan smoke-style fingerprints', 'All classes, clans with 7+ games. Cell: the clan\'s value; colour: how far above (blue) or below (orange) the 24-clan average. Clans that sit together play alike.')
    ypos = {i: y0 + (order.index(i) + .5) * rh for i in range(n)}
    hmax = merges[-1][2]; xs = lambda d: x_d + (x_l - 14 - x_d) * (1 - d / hmax)
    node = {frozenset([i]): (x_l - 14, ypos[i]) for i in range(n)}
    for a, b, d in merges:
        (xa, ya), (xb, yb) = node[frozenset(a)], node[frozenset(b)]; xm = xs(d)
        fig.add(f'<polyline points="{xa:.1f},{ya:.1f} {xm:.1f},{ya:.1f} {xm:.1f},{yb:.1f} {xb:.1f},{yb:.1f}" fill="none" stroke="{MUTED}" stroke-width="1.1"/>')
        node[frozenset(a + b)] = (xm, (ya + yb) / 2)
    fig.add(T(x_d, y0 - 8, 'joined by similarity', size=9.5, anchor='start'))
    for j, f in enumerate(feats):
        cx = x_h + (j + .5) * cw
        fig.add(f'<text x="{cx:.1f}" y="{y0-8}" font-size="10.5" fill="{INK}" transform="rotate(-50 {cx:.1f} {y0-8})">{esc(f)}</text>')
    fig.add(f'<text x="{x_h + (len(feats) + .7) * cw:.1f}" y="{y0-8}" font-size="10.5" fill="{INK}" font-weight="600" transform="rotate(-50 {x_h + (len(feats) + .7) * cw:.1f} {y0-8})">distance to H-SR</text>')
    for i in range(n):
        c = clans[i]; y = ypos[i]
        colr = BLUE if c in TOP else VIOLET if c == PN else INK
        fig.add(T(x_l - 8, y + 4, c, size=11.5, fill=colr, anchor='start', weight='700' if c in TOP or c == PN else '400'))
        fig.add(T(x_h - 6, y + 4, f'{WL[c][0]}-{WL[c][1]}', size=9.5, anchor='end'))
        for j in range(len(feats)):
            z = Z[i][j]; v = X[i][j]
            dark = abs(z) / 2.5 > 0.6
            txt = f'{v:.1f}' if feats[j] in ('smokes per game', 'median km to cap') else f'{v:.0f}'
            fig.add(f'<rect x="{x_h + j * cw + 1}" y="{y - rh / 2 + 1:.1f}" width="{cw - 2}" height="{rh - 2}" rx="2" fill="{div_color(z, 2.5)}"/>' + T(x_h + (j + .5) * cw, y + 3.5, txt, size=9.5, fill=BG if dark else INK))
        dh = dist(Z[h], Z[i])
        fig.add(T(x_h + len(feats) * cw + 14, y + 4, '-' if i == h else f'{dh:.2f}', size=10.5, fill=INK, anchor='start', weight='600' if 0 < dh < 1.1 else '400'))
    fig.add(T(x_l - 8, y0 + rh * n + 22, 'Blue name = Top 6. Violet = PN (7 games, 14 smokes: small n). W-L beside the name. Distance: 0 = same style as H-SR; the typical gap between two clans is 1.4.', size=10.5, anchor='start'))
    fig.add(T(x_l - 8, y0 + rh * n + 38, 'Features are shares of the clan\'s smokes (%), except smokes per game, median km from smoke edge to the cap, and the median time of the first smoke (seconds).', size=10.5, anchor='start'))
    fig.save(OUT('fig5-clan-fingerprints'))
    # stability: drop one feature at a time, how often does each clan stay in H-SR's nearest 3
    near = C()
    for j in range(len(feats)):
        Zj = [[v for jj, v in enumerate(r) if jj != j] for r in Z]
        for d, c in sorted((dist(Zj[h], Zj[i]), clans[i]) for i in range(n) if i != h)[:3]: near[c] += 1
    print('nearest-3 to H-SR when dropping one feature (of 18):', near.most_common())
    wr = [WL[c][0] / NG[c] for c in clans]; dh = [dist(Z[h], Z[i]) for i in range(n)]
    def corr(idx):
        mx, my = mean(wr[i] for i in idx), mean(dh[i] for i in idx)
        den = math.sqrt(sum((wr[i] - mx) ** 2 for i in idx) * sum((dh[i] - my) ** 2 for i in idx))
        return sum((wr[i] - mx) * (dh[i] - my) for i in idx) / den if den else None
    idx = [i for i in range(n) if i != h]
    print('corr', corr(idx), lohi([corr(random.choices(idx, k=len(idx))) for _ in range(1000)]))

if '6' in which:
    byid = {}
    for s in S: byid.setdefault(s['id'], []).append(s)
    def answered(s):
        c = [b for b in byid.get(s['counter_of'], []) if b['game'] == s['game'] and b['team'] != s['team']]
        return c[0] if c else None
    cs = [s for s in DD if s['counter_of'] and answered(s)]
    print('counter DD', len([s for s in DD if s['counter_of']]), 'matched', len(cs), 'PN', len([s for s in cs if s['is_pn']]))
    fig = Fig(1240, 450, 'Counter-smokes: answering an enemy smoke within 45 seconds', 'Destroyer smokes that answer an enemy smoke (blue), joined to the smoke they answer (orange, any class). The answering team\'s spawn is at the bottom. Association only.')
    maps = ['Land of Fire', 'Sea of Fortune', 'Hotspot']
    for i, m in enumerate(maps):
        ss = [s for s in cs if s['map'] == m]; allm = [s for s in DD if s['map'] == m]
        p = Panel(m, 40 + i * 318, 110, 285, G, title=f'{m}: {len(ss)} counter-smokes ({100*len(ss)/len(allm):.0f}% of {len(allm)})')
        for s in ss:
            b = answered(s); bx, bz = norm(m, s['side'], b['x'], b['z'])
            p.line([(s['nx'], s['nz']), (bx, bz)], stroke=INK, width=0.8, opacity=0.4)
            p.dot(bx, bz, r=3.5, fill=ORANGE, opacity=0.85, stroke=BG)
            p.dot(s['nx'], s['nz'], r=4.2, fill=BLUE, opacity=0.9, stroke=BG)
        fig.add(p)
        print(m, 'cells', C(s['ncell_name'] for s in ss).most_common(4), 'own half', pct(ss, lambda s: s['ncell'][1] >= 5), 'dist km', med(math.hypot(s['x'] - answered(s)['x'], s['z'] - answered(s)['z']) * WU / 1000 for s in ss))
    fig.legend(40, 76, [('counter-smoke (destroyer)', BLUE), ('the enemy smoke it answers', ORANGE)])
    x = 1000
    col = {'counter': BLUE, 'other': GREY}
    L = [s for s in DD if s['kind'] == 'long DD']; Sh = [s for s in DD if s['kind'] == 'short DD']
    sp = lambda ss: {'counter': [s for s in ss if s['counter_of']], 'other': [s for s in ss if not s['counter_of']]}
    fig.add(T(x, 96, 'Counter-smoke vs other smokes', size=12.5, fill=INK, anchor='start', weight='600'))
    fig.legend(x, 118, [('counter', BLUE), ('other', GREY)])
    fig.add(T(x, 146, 'Concealed damage per smoke', size=11, fill=INK, anchor='start'))
    y = bar_rows(fig, x, 152, 230, [(lab, {g: conc_per(v) for g, v in sp(ss).items()}, None) for lab, ss in (('long DD', L), ('short DD', Sh))], label_w=62, row_h=34, colors=col)
    fig.add(T(x, y + 26, 'Deaths in the smoke per 100', size=11, fill=INK, anchor='start'))
    y = bar_rows(fig, x, y + 32, 230, [(lab, {g: d100(v) for g, v in sp(ss).items()}, None) for lab, ss in (('long DD', L), ('short DD', Sh))], label_w=62, row_h=34, colors=col, fmt='{:.1f}')
    fig.add(T(x, y + 26, 'Counter-smoke return by group', size=11, fill=INK, anchor='start'))
    y = bar_rows(fig, x, y + 32, 230, [(GROUP_LABEL[g], conc_per([s for s in cs if s['grp'] == g]), None) for g in ('top', 'rest')], label_w=62, row_h=22)
    fig.add(T(x, y + 22, f'n: long DD {len(sp(L)["counter"])} counter / {len(sp(L)["other"])} other;', size=10, anchor='start'))
    fig.add(T(x, y + 36, f'short DD {len(sp(Sh)["counter"])} / {len(sp(Sh)["other"])}; top 6 {len([s for s in cs if s["grp"]=="top"])}, rest {len([s for s in cs if s["grp"]=="rest"])}', size=10, anchor='start'))
    fig.save(OUT('fig6-counter-smoke'))
    h2h = [(s, answered(s)) for s in cs]
    print('h2h counter out-damages answered %', pct(h2h, lambda p: p[0]['conc'] > p[1]['conc']), 'ci', boot_stat(cs, lambda ss: pct(ss, lambda s: s['conc'] > answered(s)['conc'])))
    print('top vs rest counter conc diff', ci(boot_diff(cs, conc_per)))
    dup = [i for i, v in byid.items() if len(v) > 1]
    print('duplicate smoke ids', dup, [(s['game'], s['team'], s['ship'], s['el']) for i in dup for s in byid[i]])
