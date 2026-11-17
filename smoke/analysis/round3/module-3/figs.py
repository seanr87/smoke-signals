import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m3lib import *
NG = C(g['map'] for g in G.values())
ddp = [s for s in DD if s['play']]
cap_xy = lambda m: {c['cap']: (c['x'], c['z']) for c in map_caps(G, m)}

def diamond(p, x, z, r, fill, opacity=0.8, stroke=None):
    px, py = p.xy(x, z); st = f' stroke="{stroke}" stroke-width="1"' if stroke else ''
    p.raw(f'<polygon points="{px:.1f},{py-r:.1f} {px+r:.1f},{py:.1f} {px:.1f},{py+r:.1f} {px-r:.1f},{py:.1f}" fill="{fill}" opacity="{opacity}"{st}/>')
def square(p, x, z, r, stroke):
    px, py = p.xy(x, z)
    p.raw(f'<rect x="{px-r:.1f}" y="{py-r:.1f}" width="{2*r:.1f}" height="{2*r:.1f}" fill="{BG}" fill-opacity="0.6" stroke="{stroke}" stroke-width="1.6"/>')
def key_circle(fig, x, y, r, fill, label, stroke=None, hollow=False):
    st = f' stroke="{stroke}" stroke-width="1.6"' if stroke else ''
    fig.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BG if hollow else fill}"{st}/>' + T(x + 14, y + 4, label, size=11.5, fill=INK, anchor='start'))
def key_diamond(fig, x, y, r, fill, label):
    fig.add(f'<polygon points="{x},{y-r} {x+r},{y} {x},{y+r} {x-r},{y}" fill="{fill}"/>' + T(x + 14, y + 4, label, size=11.5, fill=INK, anchor='start'))
def note(fig, x, y, lines, size=11.5):
    for i, l in enumerate(lines): fig.add(T(x, y + i * 17, l, size=size, fill=INK if l.startswith('#') else MUTED, anchor='start', weight='600' if l.startswith('#') else '400').replace('>#', '>'))

# ---------- Fig 1: where radar-smoke plays happen, all maps
fig = Fig(1220, 800, 'Where radar is run from inside a smoke (100 destroyer smokes, 22 cruiser smokes)',
          'Team-normalized: own spawn at the bottom (Okinawa: bottom left). Marker = centre of the laid smoke. n under a cap letter = destroyer plays tied to that cap (shown when 8 or more).')
for i, m in enumerate(MAPORDER):
    ss = [s for s in ddp if s['map'] == m]
    p = Panel(m, 40 + (i % 4) * 295, 120 + (i // 4) * 335, 260, G, title=f'{m}: {len(ss)} DD plays in {NG[m]} games' + (' (small n)' if len(ss) < 15 else ''))
    for s in CA:
        if s['play'] and s['map'] == m: square(p, s['nx'], s['nz'], 3.5, VIOLET)
    for s in ss:
        if s['cc']: p.dot(s['nx'], s['nz'], r=4.6, fill=GROUP_COLOR[s['grp']], opacity=0.78, stroke=BG)
        else: diamond(p, s['nx'], s['nz'], 5.6, GROUP_COLOR[s['grp']], stroke=INK)
    cn = C(s['ncap'] for s in ss)
    for c, (x, z) in cap_xy(m).items():
        if cn[c] >= 8: p.text(x, z, f'n={cn[c]}' + ('*' if cn[c] < 15 else ''), size=10, dy=17)
    fig.add(p)
kx, ky = 40 + 3 * 295, 120 + 335
key_circle(fig, kx + 8, ky + 10, 5, BLUE, 'Top 6, cap control (radar covers 90%+ of the cap)')
key_circle(fig, kx + 8, ky + 30, 5, ORANGE, 'Rest, cap control')
key_diamond(fig, kx + 8, ky + 50, 6, BLUE, 'Top 6, radar trap (radar spotted an enemy)')
key_diamond(fig, kx + 8, ky + 70, 6, ORANGE, 'Rest, radar trap')
fig.add(f'<rect x="{kx+4}" y="{ky+86}" width="8" height="8" fill="{BG}" stroke="{VIOLET}" stroke-width="1.6"/>' + T(kx + 22, ky + 94, 'Cruiser smoke (Svea radar from its own smoke)', size=11.5, fill=INK, anchor='start'))
note(fig, kx, ky + 130, ['#Per team-game (destroyer smokes)', 'Top 6: 0.50 plays   Rest: 0.19',
                         'Sleeping Giant 0.45, Mountain Range 0.43,', 'Hotspot 0.40; other maps 0.12 to 0.19.', '* = small n (8 to 14).',
                         'Mountain Range cap A (10 km cap):', '4 plays, all radar traps.'])
fig.save(os.path.join(OUT, 'fig1-radar-plays-where'))

# ---------- Fig 2: pay-off and radar ship position on the three busiest maps
M3 = MAPORDER[:3]
fig = Fig(1260, 960, 'Radar-smoke plays on the three busiest maps: what the smoke returned, and where the radar ship sat',
          'Destroyer smokes only. Team-normalized: own spawn at the bottom. Blue = Top 6, orange = Rest. Association only.')
fig.add(T(40, 78, 'Row 1. Each smoke: line = laid path, dot size = damage dealt from concealment, black ring = a cap not ours was taken while it stood.', size=12, fill=INK, anchor='start'))
rr = lambda dmg: 2.5 + math.sqrt(dmg / 1000) * 1.35
for i, m in enumerate(M3):
    ss = sorted([s for s in ddp if s['map'] == m], key=lambda s: -s['conc'])
    tk = [s for s in ss if s['own'] != 'ours']
    p = Panel(m, 40 + i * 405, 115, 375, G, title=f'{m}: cap taken {sum(s["cap_won"] for s in tk)} of {len(tk)}, mean {mean(s["conc"] for s in ss)/1000:.0f}k concealed damage')
    for s in ss:
        p.line(s['npath'], stroke=GROUP_COLOR[s['grp']], width=1.6, opacity=0.55)
    for s in ss:
        p.dot(s['nx'], s['nz'], r=rr(s['conc']), fill=GROUP_COLOR[s['grp']], opacity=0.45, stroke=GROUP_COLOR[s['grp']])
        if s['cap_won']: p.ring(s['nx'], s['nz'], rr(s['conc']) + 2, stroke=INK, width=1.8)
    fig.add(p)
fig.add(T(40, 528, 'Row 2. Radar ship position (at the smoke snapshot): dot size = enemy ships its radar lit up (hollow = none). Thin line = to the cap it covered.', size=12, fill=INK, anchor='start'))
for i, m in enumerate(M3):
    ss = [s for s in ddp if s['map'] == m]
    p = Panel(m, 40 + i * 405, 565, 375, G, title=f'{m}: {sum(s["spots"] for s in ss)} enemy ships lit by {len(ss)} radar runs')
    for s in ss:
        cp = next((c for c in ncaps(G[s['game']], s['map'], s['side']) if c['cap'] == s['cap']), None)
        if cp and s['cc']: p.line([(s['rship']['nx'], s['rship']['nz']), (cp['x'], cp['z'])], stroke=GROUP_COLOR[s['grp']], width=0.9, opacity=0.45)
    for s in sorted(ss, key=lambda s: -s['spots']):
        x, z = s['rship']['nx'], s['rship']['nz']
        if s['spots'] == 0: p.ring(x, z, 3.5, stroke=GROUP_COLOR[s['grp']], width=1.6)
        else: p.dot(x, z, r=2.5 + 2.6 * s['spots'], fill=GROUP_COLOR[s['grp']], opacity=0.6, stroke=BG)
    fig.add(p)
# keys
x = 870
for d in (5000, 20000, 60000):
    fig.add(f'<circle cx="{x}" cy="74" r="{rr(d):.1f}" fill="{MUTED}" opacity="0.45"/>' + T(x + rr(d) + 4, 78, f'{d//1000}k', size=11, fill=INK, anchor='start')); x += rr(d) * 2 + 42
fig.add(f'<circle cx="{x+6}" cy="74" r="8" fill="none" stroke="{INK}" stroke-width="1.8"/>' + T(x + 19, 78, 'cap taken', size=11, fill=INK, anchor='start'))
x = 960
fig.add(f'<circle cx="{x}" cy="524" r="3.5" fill="none" stroke="{MUTED}" stroke-width="1.6"/>' + T(x + 8, 528, '0', size=11, fill=INK, anchor='start')); x += 32
for k in (1, 2, 3):
    r = 2.5 + 2.6 * k
    fig.add(f'<circle cx="{x}" cy="524" r="{r:.1f}" fill="{MUTED}" opacity="0.6"/>' + T(x + r + 4, 528, str(k), size=11, fill=INK, anchor='start')); x += r * 2 + 26
fig.add(T(x, 528, 'enemies lit', size=11, fill=INK, anchor='start'))
fig.save(os.path.join(OUT, 'fig2-radar-plays-payoff'))

# ---------- Fig 3: early stacks with and without a radar ship
es = [s for s in DD if s['early'] and s['stack']]
fig = Fig(1220, 810, 'Early stacked destroyer smokes (first 5 minutes): is a radar ship inside?',
          'Team-normalized: own spawn at the bottom (Okinawa: bottom left). Filled = a radar ship of the team is inside the smoke, hollow = none. Blue = Top 6, orange = Rest.')
rows = []
for i, m in enumerate(MAPORDER):
    ss = [s for s in es if s['map'] == m]
    a = [s for s in ss if s['grp'] == 'top']; b = [s for s in ss if s['grp'] == 'rest']
    p = Panel(m, 40 + (i % 4) * 295, 120 + (i // 4) * 345, 260, G, title=f'{m}: {len(ss)} early stacks')
    for s in ss:
        if not s['radar_in']: p.ring(s['nx'], s['nz'], 4.2, stroke=GROUP_COLOR[s['grp']], width=1.8)
    for s in ss:
        if s['radar_in']: p.dot(s['nx'], s['nz'], r=4.6, fill=GROUP_COLOR[s['grp']], opacity=0.72, stroke=BG)
    fig.add(p)
    cap = f'Top 6: {sum(s["radar_in"] for s in a)} of {len(a)}{"*" if len(a) < 15 else ""} with radar   Rest: {sum(s["radar_in"] for s in b)} of {len(b)}{"*" if len(b) < 15 else ""}'
    fig.add(T(40 + (i % 4) * 295, 120 + (i // 4) * 345 + 260 + 28, cap, size=10.5, fill=INK, anchor='start'))
    rows.append((m, {'top': pct(a, lambda s: s['radar_in']) if len(a) >= 8 else None, 'rest': pct(b, lambda s: s['radar_in']) if len(b) >= 8 else None}, None))
kx, ky = 40 + 3 * 295, 120 + 345 - 20
a = [s for s in es if s['grp'] == 'top']; b = [s for s in es if s['grp'] == 'rest']
fig.add(T(kx, ky, 'Share with a radar ship inside (%)', size=12.5, fill=INK, anchor='start', weight='600'))
y = bar_rows(fig, kx - 10, ky + 10, 290, [('All maps', {'top': pct(a, lambda s: s['radar_in']), 'rest': pct(b, lambda s: s['radar_in'])}, None)] + rows, vmax=100, label_w=100, row_h=26)
note(fig, kx, y + 18, ['Top 6 77% of 56, Rest 62% of 85', '(difference +15 pts, 95% interval +1 to +32).', 'Bars are hidden under 8 smokes;', '* in the captions = under 15 smokes (small n).'], size=10.5)
fig.legend(kx, y + 100, [('Top 6', BLUE), ('Rest', ORANGE)])
fig.save(os.path.join(OUT, 'fig3-early-stacks-radar'))

# ---------- Fig 4: who and when
fig = Fig(1100, 560, 'Who runs radar from smoke, and when', 'Destroyer smokes with a radar play (cap control or radar trap). Clans with 7 or more games. Blue = Top 6, orange = Rest.')
cnt = C(s['team'] for s in ddp)
cl = sorted([t for t in GAMES if GAMES[t] >= 7], key=lambda t: -cnt[t] / GAMES[t])
fig.add(T(40, 86, 'Radar plays per game, by clan (right: plays / games)', size=12.5, fill=INK, anchor='start', weight='600'))
bar_rows(fig, 40, 96, 470, [(t, {'top' if t in TOP else 'rest': cnt[t] / GAMES[t]}, f'{cnt[t]} / {GAMES[t]}') for t in cl], fmt='{:.2f}', row_h=18.5, label_w=70)
fig.add(T(580, 86, 'When in the game (share of smokes in each window)', size=12.5, fill=INK, anchor='start', weight='600'))
bins = [(0, 120, '0 to 2 min'), (120, 300, '2 to 5'), (300, 600, '5 to 10'), (600, 9999, '10+')]
groups = [('Cap control', [s for s in ddp if s['cc']]), ('Radar trap', [s for s in ddp if not s['cc']]), ('All DD smokes', DD)]
y = 110
for lab, ss in groups:
    fig.add(T(580, y + 12, f'{lab} (n={len(ss):,})', size=11.5, fill=INK, anchor='start'))
    x = 580
    for j, (lo, hi, bl) in enumerate(bins):
        sh = sum(lo <= s['el'] < hi for s in ss) / len(ss); w = 470 * sh
        col = SEQ[1 + j * 2 - (1 if j == 3 else 0)]
        fig.add(f'<rect x="{x:.1f}" y="{y+20}" width="{max(0,w-2):.1f}" height="26" rx="2" fill="{col}"/>')
        if w > 30: fig.add(T(x + w / 2 - 1, y + 38, f'{100*sh:.0f}%', size=11, fill=BG if j >= 2 else INK, weight='600'))
        x += w
    y += 66
x = 580
for j, (lo, hi, bl) in enumerate(bins):
    col = SEQ[1 + j * 2 - (1 if j == 3 else 0)]
    fig.add(f'<rect x="{x}" y="{y+2}" width="12" height="12" rx="2" fill="{col}"/>' + T(x + 17, y + 12, bl, size=11.5, fill=INK, anchor='start')); x += 110
note(fig, 580, y + 50, ['#Which ship carries the radar (100 destroyer smokes)', 'Brisbane 28, Des Moines 23, Minotaur 16, other cruisers 17:', 'a cruiser sitting in a destroyer\'s smoke in 84 of 100.',
                        'Gdansk 16: a radar destroyer using its own smoke.', 'Cruiser smokes (22 plays): all Svea, radar from its own smoke.'])
fig.save(os.path.join(OUT, 'fig4-who-when'))
print('ok')
