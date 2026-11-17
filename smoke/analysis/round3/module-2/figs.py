import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2 import *
which = sys.argv[1:] or ['1', '2', '3', '4', '5']
LEG = [(sh + ' smoke', SHIP_COLOR[sh]) for sh in SHIPS] + [('radar cruiser partner', RED), ('non-radar cruiser partner', YELLOW), ('battleship partner', INK)]

def draw_setup(p, ss, mark_top=False):
    """Smokes as arrows along the laid path (first puff to last), partners as dots linked to the smoke centre."""
    for s in ss:
        for pr in s['partners']:
            if pr['nx'] is None or pr['cls'] == 'destroyer': continue
            col = RED if pr['cls'] == 'cruiser' and pr['radar'] else YELLOW if pr['cls'] == 'cruiser' else INK
            p.line([(s['nx'], s['nz']), (pr['nx'], pr['nz'])], stroke=MUTED, width=0.6, opacity=0.45)
            p.dot(pr['nx'], pr['nz'], r=2.6, fill=col, opacity=0.85, stroke=BG)
    for s in ss:
        p.line(s['npath'], stroke=SHIP_COLOR[s['ship']], width=3.2, opacity=0.8, arrow=True)
        if mark_top and s['grp'] == 'top': p.ring(s['nx'], s['nz'], 7, stroke=INK, width=1.2)

if '1' in which:
    maps = ['Hotspot', 'Sleeping Giant', 'Mountain Range']
    fig = Fig(1290, 1010, 'Early smokes (first 5 min) by Harugumo, Somers, Gearing: typical setup, Top 6 vs Rest',
              'Arrow = the smoke as laid (start to end). Dots = allies it covered, at the moment the smoke was fully laid, linked to their smoke. Team-normalized.')
    fig.legend(40, 74, LEG)
    for i, m in enumerate(maps):
        for j, g in enumerate(('top', 'rest')):
            ss = [s for s in E if s['map'] == m and s['grp'] == g]
            p = Panel(m, 44 + i * 418, 126 + j * 448, 384, G, title=f'{m}, {GROUP_LABEL[g]} (n {len(ss)}{", small n" if len(ss) < 15 else ""})')
            draw_setup(p, ss); fig.add(p)
    fig.save(os.path.join(OUT, 'setup-main-maps'))

if '2' in which:
    maps = ['Land of Fire', 'Sea of Fortune', 'Okinawa', 'Loop']
    fig = Fig(1290, 480, 'Early smokes by Harugumo, Somers, Gearing: the four maps with too few Top 6 smokes to split',
              'All teams pooled. Black ring = a Top 6 smoke (under 8 per map, do not read as a pattern). Arrow = smoke as laid; dots = covered allies. Team-normalized.')
    fig.legend(40, 74, LEG)
    for i, m in enumerate(maps):
        ss = [s for s in E if s['map'] == m]
        p = Panel(m, 40 + i * 312, 126, 290, G, title=f'{m} (n {len(ss)}{", small n" if len(ss) < 15 else ""}; Top 6 {sum(s["grp"] == "top" for s in ss)})')
        draw_setup(p, ss, mark_top=True); fig.add(p)
    fig.save(os.path.join(OUT, 'setup-other-maps'))

if '3' in which:
    # where the main partner sits relative to the smoke centre; up = toward the enemy spawn
    HOW = {'inside': BLUE, 'behind': ORANGE, 'line_of_fire': AQUA}
    fig = Fig(1000, 560, 'Where the partner sits relative to the early smoke', 'Smoke centre at the cross, up = toward the enemy spawn. One dot per smoke (its main partner). Filled = radar ship, hollow = no radar. Rings at 1, 2, 3 km.')
    fig.legend(40, 74, [('partner inside the smoke', BLUE), ('behind it', ORANGE), ('in the line of fire', AQUA)])
    R = 4000; size = 400
    for j, g in enumerate(('top', 'rest')):
        x0, y0 = 60 + j * 470, 120; cx, cy = x0 + size / 2, y0 + size / 2; k = size / 2 / R
        ss = [s for s in E if s['grp'] == g and s['mp'] and s['mp']['nx'] is not None]
        o = f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" fill="#ffffff" stroke="{GRID}"/>'
        for km in (1, 2, 3): o += f'<circle cx="{cx}" cy="{cy}" r="{km*1000*k:.1f}" fill="none" stroke="{GRID}" stroke-width="1"/>' + T(cx + 3, cy - km * 1000 * k - 3, f'{km} km', size=9, anchor='start')
        o += f'<circle cx="{cx}" cy="{cy}" r="{450*k:.1f}" fill="{MUTED}" opacity="0.18"/><line x1="{cx-6}" y1="{cy}" x2="{cx+6}" y2="{cy}" stroke="{INK}"/><line x1="{cx}" y1="{cy-6}" x2="{cx}" y2="{cy+6}" stroke="{INK}"/>'
        off = 0
        for s in ss:
            fx, fz = fwd(s['map']); dx, dz = (s['mp']['nx'] - s['nx']) * WU, (s['mp']['nz'] - s['nz']) * WU
            a, r = dx * fx + dz * fz, dx * fz - dz * fx
            if max(abs(a), abs(r)) > R: off += 1; continue
            col = HOW[s['mp']['how']]
            o += f'<circle cx="{cx + r*k:.1f}" cy="{cy - a*k:.1f}" r="4" fill="{col if s["mp"]["radar"] else "#ffffff"}" stroke="{col}" stroke-width="1.5" opacity="0.8"/>'
        beh = pct(ss, lambda s: (s['mp']['nx'] - s['nx']) * fwd(s['map'])[0] + (s['mp']['nz'] - s['nz']) * fwd(s['map'])[1] < 0)
        o += T(x0, y0 - 8, f'{GROUP_LABEL[g]}: n {len(ss)}, {beh:.0f}% on the spawn side' + (f', {off} beyond 4 km not shown' if off else ''), size=12.5, fill=INK, anchor='start', weight='600')
        o += T(cx, y0 + size + 16, 'toward own spawn', size=10) + T(cx, y0 + 12, 'toward the enemy', size=10)
        fig.add(o)
    fig.save(os.path.join(OUT, 'partner-offsets'))

if '4' in which:
    fig = Fig(1180, 530, 'Early smokes by Harugumo, Somers, Gearing: outcomes by partner, coverage and window',
              'Bar = value, line = 95% interval (resampling clans). n after each label. Association only.')
    def block(x, y, title, rows, vmax, fmt, w=330, lw=150):
        fig.add(T(x, y - 8, title, size=12.5, fill=INK, anchor='start', weight='600'))
        for lab, e, st in rows:
            if len(e) < 8:
                fig.add(T(x + lw - 8, y + 15, f'{lab} (n {len(e)})', size=11, fill=INK, anchor='end') + T(x + lw, y + 15, 'too few to show', size=10, anchor='start')); y += 24; continue
            v = st(e); lo, hi = boot_stat(e, st); sc = (w - lw - 50) / vmax
            fig.add(T(x + lw - 8, y + 15, f'{lab} (n {len(e)}{", small" if len(e) < 15 else ""})', size=11, fill=INK, anchor='end'))
            fig.add(f'<rect x="{x+lw}" y="{y+4}" width="{max(1, v*sc):.1f}" height="14" rx="2" fill="{BLUE}"/>'
                    f'<line x1="{x+lw+max(0, lo)*sc:.1f}" y1="{y+11}" x2="{x+lw+min(vmax * 1.25, hi)*sc:.1f}" y2="{y+11}" stroke="{INK}" stroke-width="1.5"/>' + T(x + lw + min(vmax * 1.25, hi) * sc + 5, y + 15, fmt(v), size=10, anchor='start'))
            y += 24
        return y + 30
    conc = lambda v: mean(s['conc'] for s in v); capw = lambda v: pct(v, lambda s: s['cap_won']); dth = lambda v: mean(s['deaths'] for s in v)
    groups = [('Partner type', [(t, [s for s in E if s['pt'] == t]) for t in PT_ORDER]),
              ('Coverage', [(c, [s for s in E if s['coverage'] == c]) for c in ('stacked', 'screen', 'selfish')]),
              ('Window', [(WIN_LABEL[i], [s for s in E if s['w'] == i]) for i in range(3)]),
              ('Group', [(GROUP_LABEL[g], [s for s in E if s['grp'] == g]) for g in ('top', 'rest')])]
    for c, (nm, st, vmax, fmt) in enumerate((('Concealed damage per smoke (mean)', conc, 26000, lambda v: f'{v:,.0f}'), ('Cap won after the smoke (%)', capw, 80, lambda v: f'{v:.0f}%'),
                                             ('Deaths in the smoke, per smoke', dth, 0.5, lambda v: f'{v:.2f}'))):
        y = 110
        for gname, rows in groups:
            y = block(40 + c * 380, y, f'{gname}: {nm}' if gname == 'Partner type' else gname, [(lab, e, st) for lab, e in rows], vmax, fmt)
    fig.save(os.path.join(OUT, 'outcomes'))

if '5' in which:
    O = openings()
    maps = sorted(MAPS, key=lambda m: -sum(o['map'] == m for o in O))
    fig = Fig(1290, 1500, "Opening playbook: where each team's first and second smoke of the game go (any ship)",
              'Number = team-games whose 1st (left) or 2nd (right) smoke was centred in that cell; darker = more. "early" = before 5:00. All teams. Team-normalized.')
    for i, m in enumerate(maps):
        for j in range(2):
            v = [o['smokes'][j] for o in O if o['map'] == m and o['n'] > j]
            x0 = 40 + (i % 2) * 630 + j * 305; y0 = 110 + (i // 2) * 345
            share3 = pct(v, lambda s: s['ship'] in SHIPS); early = pct(v, lambda s: s['el'] < 300)
            p = Panel(m, x0, y0, 280, G, title=f'{m}: {"1st" if j == 0 else "2nd"} smoke (n {len(v)}, {early:.0f}% early)')
            cc = C(s['ncell'] for s in v); vmax = max(cc.values())
            for (c, r), n in cc.items(): p.cellfill(c, r, seq_color(n, vmax), opacity=0.8, text=str(n), text_fill=seq_text(n, vmax))
            for cp in map_caps(G, m): p.text(cp['x'], cp['z'], cp['cap'], size=11, dy=4)
            fig.add(p)
    fig.save(os.path.join(OUT, 'opening-first-two-smokes'))
print('done', which)
