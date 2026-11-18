import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c5lib import *
ensure_maps()
def dots(p, ss, r=4.2, op=0.75):
    for s in ss: p.dot(s['nx'], s['nz'], r=r, fill=GROUP_COLOR[s['grp']], opacity=op, stroke=BG, title=f"{s['team']} {s['ship']} {clock(s['el'])}")
def rect(p, x0, z0, x1, z1, fill=BLUE, op=0.10, stroke=BLUE):
    (a, b), (c, d) = p.xy(x0, z1), p.xy(x1, z0)
    p.raw(f'<rect x="{a:.1f}" y="{b:.1f}" width="{c - a:.1f}" height="{d - b:.1f}" fill="{fill}" opacity="{op}"/><rect x="{a:.1f}" y="{b:.1f}" width="{c - a:.1f}" height="{d - b:.1f}" fill="none" stroke="{stroke}" stroke-width="2" stroke-dasharray="7 4"/>')
def diamond(p, x, z, r=6, fill=VIOLET):
    px, py = p.xy(x, z); p.raw(f'<polygon points="{px:.1f},{py - r:.1f} {px + r:.1f},{py:.1f} {px:.1f},{py + r:.1f} {px - r:.1f},{py:.1f}" fill="{fill}" stroke="{BG}" stroke-width="1"/>')

# 1. Sleeping Giant Somers east / west
m = 'Sleeping Giant'; som = [s for s in on(m) if s['ship'] == 'Somers']
fig = Fig(1120, 640, 'Sleeping Giant: where Somers smokes go', 'Dot = centre of one Somers smoke. Shaded = east half (normalized x > 0). Top 6 blue, Rest orange.')
for i, (ttl, v) in enumerate((('All Somers smokes: west half Top 6 5 of 30 (17%), Rest 23 of 45 (51%)', som), ('First 5 minutes only: west half Top 6 4 of 8, Rest 8 of 15', [s for s in som if s['el'] < 300]))):
    p = Panel(m, 50 + i * 540, 110, 480, G, title=ttl); rect(p, 0, -700, 700, 700); dots(p, v, r=5); fig.add(p)
fig.legend(50, 72, [('Top 6', BLUE), ('Rest', ORANGE)]); fig.save(os.path.join(FIGDIR, 'c5-sg-somers-east-west'))

# 2. Sleeping Giant Harugumo G1/F1 with second destroyers
rec = r4_spot('sg-harugumo-g1'); mem = [s for s in on(m) if s['ship'] == 'Harugumo' and in_r4(rec, s)]
fig = Fig(1000, 760, 'Sleeping Giant: Harugumo at G1/F1 and the second destroyer', 'Line = the laid smoke (Top 6 blue, Rest orange). Violet diamond = another allied destroyer when the smoke was fully laid.')
p = Panel(m, 60, 110, 620, G, title='12 Harugumo smokes in the spot (11 Top 6, 1 Rest)'); ell_svg(p, rec, dash='6 4')
for s in mem:
    p.line(s['npath'], stroke=GROUP_COLOR[s['grp']], width=4, opacity=0.8)
    for d in second_dds(s):
        p.line([(s['nx'], s['nz']), (d['nx'], d['nz'])], stroke=VIOLET, width=1, opacity=0.6, dash='3 3'); diamond(p, d['nx'], d['nz'])
        p.text(d['nx'], d['nz'], d['ship'], size=9, fill=VIOLET, dy=-9)
fig.add(p)
y = 130; fig.add(T(710, y, 'Smoke, time, second destroyer', size=12, fill=INK, anchor='start', weight='600'))
for s in sorted(mem, key=lambda s: (s['grp'] != 'top', s['game'], s['el'])):
    y += 20; d2 = second_dds(s)
    fig.add(T(710, y, f"{s['team']} {clock(s['el'])} {s['ncell_name']}: " + (', '.join(f"{d['ship']} {d['cell']}" for d in d2) or 'none recorded'), size=11, fill=GROUP_COLOR[s['grp']], anchor='start'))
fig.add(T(710, y + 30, 'Second destroyer recorded: 7 of 11 Top 6 smokes.', size=11, fill=INK, anchor='start')); fig.add(T(710, y + 46, 'Up at cap A (F1): 3. Inside the smoke (G1): 2.', size=11, fill=INK, anchor='start')); fig.add(T(710, y + 62, 'Far east (G3/G4), 11 km away: 2.', size=11, fill=INK, anchor='start'))
fig.save(os.path.join(FIGDIR, 'c5-sg-harugumo-g1-second-dd'))

# 3. Hotspot west caps
m = 'Hotspot'; dd = on(m, DD)
fig = Fig(1120, 640, 'Hotspot: destroyer smoke at the west caps A and B', 'Dot = centre of one destroyer smoke. Bright = nearest cap is A or B; faint = C or D. Top 6 blue, Rest orange.')
for i, (gname, ttl) in enumerate((('top', 'Top 6: 29 of 80 smokes at A or B (36%)'), ('rest', 'Rest: 21 of 155 smokes at A or B (14%)'))):
    p = Panel(m, 50 + i * 540, 110, 480, G, title=ttl)
    v = [s for s in dd if s['grp'] == gname]
    dots(p, [s for s in v if s['zone'] not in 'AB'], r=3.2, op=0.28); dots(p, [s for s in v if s['zone'] in 'AB'], r=5.2, op=0.9)
    for c in map_caps(G, m):
        if c['cap'] in 'AB': p.ring(c['x'], c['z'], c['r'] / 1600 * 480 + 10, stroke=INK, width=2)
    fig.add(p)
fig.legend(50, 72, [('Top 6', BLUE), ('Rest', ORANGE)]); fig.save(os.path.join(FIGDIR, 'c5-hs-west-caps'))

# 4. Loop first smokes (with Hotspot for contrast)
def first_smokes(mm):
    out = []
    for k, t in tgames(mm):
        v = sorted([s for s in S if s['game'] == k and s['team'] == t], key=lambda s: s['el'])
        if v: out.append(v[0])
    return out
fig = Fig(1120, 660, 'First smoke of each team-game: Loop against Hotspot', 'Dot = a team\'s first smoke of the game (any ship). Cross = average position. Letters = ship (D Daring, S Somers, G Gearing, Gd Gdansk, N Napoli, Sh Shimakaze, H Harugumo, Sv Svea). Top 6 blue, Rest orange.')
ab = {'Daring': 'D', 'Somers': 'S', 'Gearing': 'G', 'Gdańsk': 'Gd', 'Napoli': 'N', 'Shimakaze': 'Sh', 'Harugumo': 'H', 'Svea': 'Sv'}
for i, (mm, ttl) in enumerate((('Loop', 'Loop: 41 first smokes, median 4:14, 32% by long-smoke ships'), ('Hotspot', 'Hotspot: 62 first smokes, median 2:37, 65% by long-smoke ships'))):
    p = Panel(mm, 50 + i * 540, 120, 480, G, title=ttl); fs = first_smokes(mm); dots(p, fs, r=6, op=0.85)
    for s in fs:
        if s['ship'] in ab: p.text(s['nx'], s['nz'], ab[s['ship']], size=8.5, dy=-8)
    cx, cz = mean(s['nx'] for s in fs), mean(s['nz'] for s in fs); px, py = p.xy(cx, cz)
    p.raw(f'<path d="M{px - 8:.1f},{py:.1f} L{px + 8:.1f},{py:.1f} M{px:.1f},{py - 8:.1f} L{px:.1f},{py + 8:.1f}" stroke="{INK}" stroke-width="2.5"/>')
    fig.add(p)
fig.legend(50, 80, [('Top 6', BLUE), ('Rest', ORANGE)]); fig.save(os.path.join(FIGDIR, 'c5-lp-first-smokes'))

# 5. Okinawa death zone
m = 'Okinawa'; ms = on(m); rd = atlas_spot('oki-deaths-h4')
fig = Fig(1000, 760, 'Okinawa: where ships died in smoke', 'Grey = no death. Red = smoke with a death (bigger = 2). Black ring = laid while 50+ behind. Red dashed = the death zone.')
p = Panel(m, 60, 110, 620, G, title='All 158 smokes, all classes'); ell_svg(p, rd, stroke=RED, width=2.5, dash='7 4')
for s in ms:
    if s['deaths'] == 0: p.dot(s['nx'], s['nz'], r=3.5, fill=MUTED, opacity=0.45)
for s in ms:
    if s['state'] == 'behind 50+': p.ring(s['nx'], s['nz'], 6.5 if s['deaths'] else 5, stroke=INK, width=1.1, opacity=0.8)
for s in ms:
    if s['deaths']: p.dot(s['nx'], s['nz'], r=4.5 + 1.5 * (s['deaths'] - 1), fill=RED, opacity=0.9, stroke=BG, title=f"{s['team']} {s['ship']}")
fig.add(p)
y = 130
for line in ('Zone: 39 smokes, 12 deaths = 31 per 100.', 'Rest of the map: 119 smokes, 16 deaths = 13 per 100.', 'Laid 50+ behind: zone 19 of 39 (49%),', 'rest of the map 36 of 119 (30%).', 'Deaths per 100 when 50+ behind:', 'zone 42 (n 19), rest of the map 17 (n 36).'):
    fig.add(T(710, y, line, size=11.5, fill=INK, anchor='start')); y += 20
fig.save(os.path.join(FIGDIR, 'c5-ok-death-zone'))
print('figures ok')
