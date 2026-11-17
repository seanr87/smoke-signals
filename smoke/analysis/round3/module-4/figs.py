import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m4lib import *
OUT = os.path.dirname(os.path.abspath(__file__))
ORG = ['#fde3d6', '#f8c9b6', '#f5b196', '#f29a78', '#eb6834', '#c9521f', '#8f3611']
GRN = ['#d6f1e6', '#aee3cd', '#84d3b2', '#4fc096', '#1baf7a', '#128a5f', '#0b6444']
def ramp(r, v, vmax):
    t = min(1, max(0, v / vmax)); i = min(len(r) - 1, int(t * len(r)))
    return r[i], (BG if i >= 4 else INK)
def ramp_legend(fig, x, y, r, lo, hi):
    for i, col in enumerate(r): fig.add(f'<rect x="{x+i*18}" y="{y}" width="18" height="9" fill="{col}"/>')
    fig.add(T(x - 4, y + 8, lo, size=9.5, anchor='end') + T(x + len(r) * 18 + 4, y + 8, hi, size=9.5, anchor='start'))

MEAS = [('Concealed damage per smoke', SEQ, 25000, lambda x: f"{x['conc']/1000:.1f}k", 'conc', '0', '25k+'),
        ('Deaths per 100 smokes', ORG, 30, lambda x: f"{x['d100']:.0f}", 'd100', '0', '30+'),
        ('Cap won, % of smokes', GRN, 60, lambda x: f"{x['capw']:.0f}%", 'capw', '0%', '60%+')]

def sheet(m):
    ms, avg, cells = map_cells(m); st = stats(ms)
    slug = m.lower().replace(' ', '-')
    fig = Fig(1280, 640, f'{m}: what destroyer smoke returned, by grid cell (team-normalized)',
              f"{GAMES_PER_MAP[m]} games, {st['n']} destroyer smokes. Map average: {k(avg)} concealed damage per smoke, {st['d100']:.0f} deaths per 100, cap won {st['capw']:.0f}%. "
              f"Cells with {MIN_N}+ smokes are rated; dashed = small n ({MIN_N} to {SOLID_N-1}); grey number = n too small to rate.")
    size = 380
    for i, (title, r, vmax, fmt, key, lo, hi) in enumerate(MEAS):
        x0 = 44 + i * 412; y0 = 112
        p = Panel(m, x0, y0, size, G, title=title, dim=0.45)
        s_ = size / 10
        for (c, rr), x in cells.items():
            if not x['rated']:
                p.raw(T(x0 + c * s_ + s_ / 2, y0 + rr * s_ + s_ / 2 + 3, str(x['n']), size=8.5, fill=MUTED, weight='400', halo=True)); continue
            col, tf = ramp(r, x[key], vmax)
            stroke = None
            if key == 'conc' and x['mark']: stroke = GREEN if x['mark'] == 'high' else RED
            p.cellfill(c, rr, col, opacity=0.95 if not x['small'] else 0.85, text=fmt(x), text_fill=tf, sub=f"n {x['n']}", stroke=stroke)
            if x['small']:
                p.raw(f'<rect x="{x0+c*s_+3.5:.1f}" y="{y0+rr*s_+3.5:.1f}" width="{s_-7:.1f}" height="{s_-7:.1f}" rx="1" fill="none" stroke="{tf}" stroke-width="0.9" stroke-dasharray="2.5 2"/>')
        cap_labels(p); fig.add(p)
        ramp_legend(fig, x0 + size - 150, y0 - 27, r, lo, hi)
    fig.add(f'<rect x="44" y="{112+size+24}" width="12" height="12" fill="none" stroke="{GREEN}" stroke-width="2"/>' + T(62, 112 + size + 34, f'high cell: {HIGH_X}x map average or more', size=11, fill=INK, anchor='start'))
    fig.add(f'<rect x="270" y="{112+size+24}" width="12" height="12" fill="none" stroke="{RED}" stroke-width="2"/>' + T(288, 112 + size + 34, f'low cell: {LOW_X}x map average or less (left panel only)', size=11, fill=INK, anchor='start'))
    y = 112 + size + 58
    fig.add(T(44, y, 'Zones (every smoke assigned to its nearest cap):', size=11.5, fill=INK, anchor='start', weight='600')); y += 17
    for z, v in sorted(by(ms, 'zone').items()):
        x = stats(v); t = pct([s for s in ms if s['grp'] == 'top'], lambda s: s['zone'] == z); r_ = pct([s for s in ms if s['grp'] == 'rest'], lambda s: s['zone'] == z)
        fig.add(T(44, y, f"Cap {z}: n {x['n']}{' (too few to rate)' if x['n'] < MIN_N else ' (small n)' if x['n'] < SOLID_N else ''}   |   {k(x['conc'])} concealed damage per smoke (median {k(x['med'])})   |   {x['d100']:.0f} deaths per 100   |   cap won {x['capw']:.0f}%"
                          f"   |   share of own smokes on this map: Top 6 {t:.0f}%, Rest {r_:.0f}%", size=11, fill=INK, anchor='start')); y += 16
    fig.save(os.path.join(OUT, f'sheet-{slug}'))
    print('saved', slug)

def cap_labels(p):
    for c in map_caps(G, p.map):
        x = max(-p.space / 2 + 0.02 * p.space, min(p.space / 2 - 0.02 * p.space, c['x']))
        p.text(x, c['z'], c['cap'], size=11, weight='700', dy=4)
def cap_xy(m, cap): c = next(c for c in map_caps(G, m) if c['cap'] == cap); return c
def dots(p, ms, color_of, rmax=25000):
    for s in sorted(ms, key=lambda s: -s['conc']):
        col, op = color_of(s)
        p.dot(s['nx'], s['nz'], r=2 + 5 * min(1, s['conc'] / rmax) ** 0.5, fill=col, opacity=op)
def cell_box(p, names, stroke=INK, width=2):
    s_ = p.size / 10
    for nm in names:
        r = 'ABCDEFGHIJ'.index(nm[0]); c = int(nm[1:]) - 1
        p.raw(f'<rect x="{p.x0+c*s_:.1f}" y="{p.y0+r*s_:.1f}" width="{s_:.1f}" height="{s_:.1f}" fill="none" stroke="{stroke}" stroke-width="{width}"/>')
def notes(fig, x, y, lines):
    for ln in lines: fig.add(T(x, y, ln, size=10.8, fill=INK, anchor='start')); y += 15

def hypo():
    fig = Fig(1280, 700, 'Scouting-report claims: where the smoke goes and what it returns',
              'Dot = one destroyer smoke at its team-normalized position; bigger dot = more concealed damage (largest = 25k or more). Black boxes = the cells discussed.')
    size = 380; y0 = 104
    # Hotspot: D flank
    m = 'Hotspot'; ms = [s for s in DD if s['map'] == m]
    p = Panel(m, 44, y0, size, G, title='Hotspot: "D flank"', dim=0.5)
    dots(p, ms, lambda s: (VIOLET, 0.7) if s['zone'] == 'D' else (MUTED, 0.45)); cell_box(p, ['F10', 'G10', 'H10']); cell_box(p, ['F9'], stroke=RED); cap_labels(p)
    fig.add(p); fig.legend(44, y0 + size + 34, [('nearest cap is D', VIOLET), ('other caps', MUTED)])
    notes(fig, 44, y0 + size + 58, ['D zone: 108 of 235 smokes (46%), 13.0k per smoke vs 11.7k elsewhere;',
                                    'difference -4.4k to +5.8k, not separable from zero.',
                                    'Own-side edge F10+G10+H10 (black): n 62, 16.0k, 11 deaths per 100.',
                                    'F9 inside the cap (red): n 11, 6.0k, small n.',
                                    'The first observed owner of D was the winner in 67% of 30 games',
                                    '(48 to 80); of centre cap C, 77% of 31 (62 to 91). Approximate.',
                                    'Top 6 lay 35% of their Hotspot smokes at D, Rest 52% (-31 to -4 pts).'])
    # Sleeping Giant: A first
    m = 'Sleeping Giant'; ms = [s for s in DD if s['map'] == m]
    p = Panel(m, 456, y0, size, G, title='Sleeping Giant: "A first"', dim=0.5)
    dots(p, ms, lambda s: (BLUE, 0.75) if s['el'] <= 240 else (ORANGE, 0.45)); cell_box(p, ['G1', 'E1']); cap_labels(p)
    fig.add(p); fig.legend(456, y0 + size + 34, [('first 4 minutes', BLUE), ('later', ORANGE)])
    notes(fig, 456, y0 + size + 58, ['First destroyer smoke of a team-game goes to the A side in 37 of 60 (62%).',
                                     'A-zone smokes in the first 4 minutes: n 30, 23.6k per smoke, 7 deaths per 100;',
                                     'A-zone later: n 61, 10.4k, 15 deaths per 100.',
                                     'G1 (black, own side of A): n 21, 24.1k; +8.5k to +20.5k vs rest of map.',
                                     'E1 (black, far side of A): n 10, 25.5k, small n.',
                                     'The first observed owner of A was the winner in 59% of 32 games',
                                     '(38 to 75): no clear link. Centre cap B zone: n 52, 5.4k per smoke.'])
    # Land of Fire: B
    m = 'Land of Fire'; ms = [s for s in DD if s['map'] == m]
    p = Panel(m, 868, y0, size, G, title='Land of Fire: "B"', dim=0.5)
    dots(p, ms, lambda s: (VIOLET, 0.75) if s['zone'] == 'B' else (AQUA, 0.6) if s['zone'] == 'A' else (MUTED, 0.45)); cell_box(p, ['F5', 'F6']); cap_labels(p)
    fig.add(p); fig.legend(868, y0 + size + 34, [('nearest cap is B', VIOLET), ('A', AQUA), ('C or D', MUTED)])
    notes(fig, 868, y0 + size + 58, ['B zone: n 50, 7.6k per smoke, cap won 26%; A zone: n 52, 6.9k, 23%.',
                                     'F5 + F6 (black, own half of B): n 27, 6.0k per smoke, cap won 44%.',
                                     'First observed owner was the winner: B 70% of 23 games (48 to 88);',
                                     'A 72% of 25 (52 to 88); C and D 44% of 25 each. Approximate.',
                                     'Holder at 8:00 was the winner: B 81% of 21 (59 to 96), A 80% of 20 (62 to 96).',
                                     'Top 6 lay 46% of their smokes at B and 27% at A; Rest 35% and 49%',
                                     '(A difference -36 to -8 pts; B difference -19 to +37, not clear).'])
    fig.save(os.path.join(OUT, 'claims-hotspot-sleeping-giant-land-of-fire'))
    print('saved claims')

def usage():
    fig = Fig(1280, 680, 'Where Top 6 and Rest put their destroyer smoke on the three maps where it differs',
              'Dot = one destroyer smoke, team-normalized. Labels = share of each group\'s smokes on that map laid nearest that cap (Top 6 / Rest).')
    size = 380; y0 = 104
    info = {'Hotspot': ['Top 6 use the west caps more: A+B 36% vs 14% of smokes',
                        '(A +5 to +16 pts, B +2 to +23 pts) and D less: 35% vs 52%',
                        '(-31 to -4 pts).',
                        'Low cells F5, G5, F6, F9 (red): Top 6 11% of smokes,',
                        'Rest 30% (-34 to -5 pts).',
                        'West zones returned 15.6k (B) and 19.7k (A) per smoke (n 50);',
                        'those four low cells 5.3k (n 55).'],
            'Loop': ['Rest lay half their smokes at A: 50% vs Top 6 22%',
                     '(-49 to -7 pts).',
                     'A is the weakest zone: 4.8k per smoke (-9.7k to -1.4k',
                     'vs elsewhere), cap won 17%.',
                     'F8 and F10 (green): 18.3k (n 15) and 20.7k (n 9, small n,',
                     '33 deaths per 100).',
                     'Observed (approximate): the holder of B at 8:00 was the winner',
                     'in 75% of 20 games (52 to 94); the holder of A in 33% of 18.'],
            'Land of Fire': ['Rest lay half their smokes at A: 49% vs Top 6 27%',
                             '(-36 to -8 pts).',
                             'Top 6 go to B (46% vs 35%) and near cap D (25% vs 9%);',
                             'neither gap is clear.',
                             'Damage is flat across zones here (6.9k to 9.2k). Observed',
                             '(approximate): the holders of A and of B at 8:00 were the',
                             'winners in about 80% of games.']}
    boxes = {'Hotspot': (['F5', 'G5', 'F6', 'F9'], RED), 'Loop': (['F8', 'F10'], GREEN), 'Land of Fire': ([], INK)}
    for i, m in enumerate(['Hotspot', 'Loop', 'Land of Fire']):
        ms = [s for s in DD if s['map'] == m]; x0 = 44 + i * 412
        p = Panel(m, x0, y0, size, G, title=m, dim=0.5)
        for s in ms: p.dot(s['nx'], s['nz'], r=3, fill=GROUP_COLOR[s['grp']], opacity=0.6)
        cell_box(p, boxes[m][0], stroke=boxes[m][1])
        tt = [s for s in ms if s['grp'] == 'top']; rr = [s for s in ms if s['grp'] == 'rest']
        for c in map_caps(G, m):
            t = pct(tt, lambda s: s['zone'] == c['cap']); r_ = pct(rr, lambda s: s['zone'] == c['cap'])
            dy = -(c['r'] / p.space * size) - 6 if c['z'] >= 0 else (c['r'] / p.space * size) + 14
            if m == 'Loop': dy = -(c['r'] / p.space * size) - 6
            x = max(-p.space / 2 + 0.11 * p.space, min(p.space / 2 - 0.11 * p.space, c['x']))
            p.text(x, c['z'], f'{t:.0f}% / {r_:.0f}%', size=11.5, dy=dy)
        cap_labels(p); fig.add(p)
        notes(fig, x0, y0 + size + 58, info[m])
    fig.legend(44, y0 + size + 34, [('Top 6', BLUE), ('Rest', ORANGE)])
    fig.save(os.path.join(OUT, 'usage-top6-vs-rest'))
    print('saved usage')

if __name__ == '__main__':
    which = sys.argv[1:] or ['sheets', 'hypo', 'usage']
    if 'sheets' in which:
        for m in MAP_ORDER: sheet(m)
    if 'hypo' in which: hypo()
    if 'usage' in which: usage()
