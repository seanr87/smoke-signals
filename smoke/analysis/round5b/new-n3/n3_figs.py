# Figures for worker n3. Run after b3_shots.py and c5_loop.py: python -I -X utf8 n3_figs.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
import json, shutil
HERE_N3 = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(os.path.dirname(HERE_N3), 'figures')
S, G = load5()
B = json.load(open(os.path.join(HERE_N3, 'b3.json'), encoding='utf-8'))
Cj = json.load(open(os.path.join(HERE_N3, 'c5.json'), encoding='utf-8'))

# ---------- figure 1: per-shot spotter evidence, Harugumo vs Somers vs Gearing
SP = B['cats']['spotter']
SEG = [('Radar-lit by a radar ship inside this smoke', [SP[0]], VIOLET), ('Radar-lit by a radar ship elsewhere', [SP[1]], MAGENTA),
       ('Detected, no radar; nearest ally a ship outside the smoke', [SP[2]], AQUA), ('... a second destroyer', [SP[3]], GREEN),
       ('... the smoker itself', [SP[4]], YELLOW), ('... a ship in the smoke', [SP[5], SP[6]], RED), ('Target not detected at the shot', [SP[7], SP[8]], '#b9b8b3')]
NR = B['cats']['nearest']
SEG2 = [('A ship outside the smoke', [NR[0]], AQUA), ('A second destroyer', [NR[1]], GREEN), ('The smoker itself', [NR[2]], YELLOW),
        ('Another ship in or behind the smoke', [NR[3]], RED), ('The radar cruiser inside the smoke', [NR[4]], VIOLET)]
W, H = 1180, 620
fig = Fig(W, H, 'Who lights the targets a long-smoke destroyer hits from its own smoke? Per shot, not one snapshot',
          'Each bar adds to 100%. Shots = distinct firing moments; damage = credited damage; per smoke = average of each smoke\'s own split. Evidence only: detection and nearness, not proof of who spotted.')
def block(y, title, segs, table, key_note):
    fig.add(T(24, y, title, size=13.5, fill=INK, anchor='start', weight='600'))
    x = 24; yy = y + 20
    for lab, _, col in segs:
        fig.add(f'<rect x="{x}" y="{yy - 10}" width="12" height="12" rx="2" fill="{col}"/>' + T(x + 16, yy, lab, size=10.5, fill=INK, anchor='start'))
        x += 16 + 5.6 * len(lab) + 16
        if x > W - 260: x = 24; yy += 16
    yy += 14
    x0, bw = 250, W - 250 - 40
    for sh in ('Harugumo', 'Somers', 'Gearing'):
        n = B['base'][sh]
        for wk, wl in (('shots_pct', f"shots (n {n['shots']})"), ('damage_pct', f"damage ({n['damage'] / 1000:.0f}k)"), ('per_smoke_pct', f"per smoke ({n['smokes_with_own_damage']} smokes)")):
            fig.add(T(x0 - 8, yy + 12, (sh + ', ' if wk == 'shots_pct' else '') + wl, size=11, fill=INK if wk == 'shots_pct' else MUTED, anchor='end', weight='600' if wk == 'shots_pct' else '400'))
            cx = x0
            for lab, cats, col in segs:
                v = sum(table[sh][c][wk] or 0 for c in cats); w = bw * v / 100
                if w > 0.3:
                    fig.add(f'<rect x="{cx:.1f}" y="{yy}" width="{max(0.5, w - 1.5):.1f}" height="16" rx="2" fill="{col}"><title>{esc(lab)}: {v:.0f}%</title></rect>')
                    if w > 26: fig.add(T(cx + w / 2, yy + 12, f'{v:.0f}%', size=10, fill=INK if col in (YELLOW, '#b9b8b3', AQUA, MAGENTA) else BG, weight='600'))
                cx += w
            yy += 20
        yy += 8
    return yy
y = block(84, 'A. What the data shows at each shot: was the target radar-lit (and from where), detected, and who was the nearest friendly ship', SEG, B['spotter'], '')
y = block(y + 14, 'B. Nearest friendly ship to the target at each shot (the round 5 stand-in, now per shot)', SEG2, B['nearest'], '')
fig.add(T(24, H - 14, f"Harugumo: {B['base']['Harugumo']['smokes_with_own_damage']} smokes with own-gun damage from {B['base']['Harugumo']['clans_with_own_damage']} clans; Somers {B['base']['Somers']['smokes_with_own_damage']} / {B['base']['Somers']['clans_with_own_damage']}; "
              f"Gearing {B['base']['Gearing']['smokes_with_own_damage']} / {B['base']['Gearing']['clans_with_own_damage']}. Batch 20261117-230933. Script new-n3/b3_shots.py.", size=10, anchor='start'))
fig.save(os.path.join(FIGDIR, 'n3-harugumo-spotter-per-shot'))

# ---------- figure 2: Loop, Daring smokes that followed a radar-lit enemy destroyer vs those that did not
if not os.path.exists(os.path.join(os.path.dirname(HERE_N3), 'maps')):
    ensure_maps(); shutil.copytree(MAP_DST, os.path.join(os.path.dirname(HERE_N3), 'maps'))
bys = {s['slug']: s for s in S}
seq = Cj['sequences']; M = [x for x in seq if x['lit']]; U = [x for x in seq if not x['lit']]
fig = Fig(1120, 800, 'Loop: Daring smokes and friendly radar on enemy destroyers',
          f"{len(M)} of {len(seq)} Daring smokes came within 60 s after a friendly radar lit an enemy destroyer anywhere (filled). Chance alone gives {Cj['groups']['Daring on Loop']['before_any_60']['base_pct']}%.")
p = Panel('Loop', 40, 96, 660, G, title='Daring smokes on Loop (centre of each smoke)')
for x in U:
    s = bys[x['slug']]; px, py = p.xy(s['nx'], s['nz'])
    p.raw(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{BG}" fill-opacity="0.75" stroke="{GROUP_COLOR[s["grp"]]}" stroke-width="2"><title>{esc(x["team"])} {x["time"]}</title></circle>')
for x in M:
    s = bys[x['slug']]
    for r in x['lit']:
        if r['tgt_n']:
            p.line([(s['nx'], s['nz']), tuple(r['tgt_n'])], stroke=VIOLET, width=1.1, opacity=0.55, dash='3 3')
            tx, ty = p.xy(*r['tgt_n']); p.raw(f'<path d="M{tx - 4:.1f},{ty - 4:.1f} L{tx + 4:.1f},{ty + 4:.1f} M{tx - 4:.1f},{ty + 4:.1f} L{tx + 4:.1f},{ty - 4:.1f}" stroke="{RED}" stroke-width="2"/>')
        if r['src_n'] and r['tgt_n']:
            p.line([tuple(r['src_n']), tuple(r['tgt_n'])], stroke=MUTED, width=0.9, opacity=0.5)
            sx, sy = p.xy(*r['src_n']); p.raw(f'<rect x="{sx - 4:.1f}" y="{sy - 4:.1f}" width="8" height="8" fill="{VIOLET}" stroke="{BG}" stroke-width="1"><title>{esc(r["radar_ship"])}</title></rect>')
for x in M:
    s = bys[x['slug']]; px, py = p.xy(s['nx'], s['nz'])
    p.raw(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{GROUP_COLOR[s["grp"]]}" stroke="{INK}" stroke-width="1.2"><title>{esc(x["team"])} {x["time"]}</title></circle>')
    if x['near']: p.raw(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="11" fill="none" stroke="{INK}" stroke-width="2"/>')
fig.add(p)
lx, ly = 730, 120
def leg(y, svg, text, sub=None):
    fig.add(svg + T(lx + 28, y + 4, text, size=12, fill=INK, anchor='start') + (T(lx + 28, y + 19, sub, size=10.5, anchor='start') if sub else ''))
leg(ly, f'<circle cx="{lx + 10}" cy="{ly}" r="6" fill="{ORANGE}" stroke="{INK}" stroke-width="1.2"/>', f'Smoke within 60 s after a friendly radar lit', f'an enemy destroyer anywhere: {len(M)}')
leg(ly + 44, f'<circle cx="{lx + 10}" cy="{ly + 44}" r="5.5" fill="{BG}" stroke="{ORANGE}" stroke-width="2"/>', f'No such radar in the 60 s before: {len(U)}')
leg(ly + 78, f'<circle cx="{lx + 10}" cy="{ly + 78}" r="6" fill="{ORANGE}" stroke="{INK}" stroke-width="1.2"/><circle cx="{lx + 10}" cy="{ly + 78}" r="11" fill="none" stroke="{INK}" stroke-width="2"/>',
    'The lit destroyer was within 3 km of', f'the cap the Daring then smoked: {sum(x["near"] for x in M)}')
leg(ly + 124, f'<path d="M{lx + 6},{ly + 120} L{lx + 14},{ly + 128} M{lx + 6},{ly + 128} L{lx + 14},{ly + 120}" stroke="{RED}" stroke-width="2"/>', 'The enemy destroyer that was lit', 'dashed line: to the smoke that followed')
leg(ly + 168, f'<rect x="{lx + 6}" y="{ly + 164}" width="8" height="8" fill="{VIOLET}"/>', 'The friendly radar ship', 'grey line: to the destroyer it lit')
fig.legend(lx, ly + 214, [('Top 6', BLUE), ('Rest', ORANGE)])
g0 = Cj['groups']
rows = [('Daring on Loop', 'Daring on Loop'), ('Daring, other maps', 'Daring on other maps'), ('Other cap sitters, Loop', 'Other cap sitters on Loop'), ('Other destroyers, Loop', 'Other destroyer smokes on Loop')]
yy = ly + 262
fig.add(T(lx, yy, 'Smokes within 60 s after a friendly radar', size=12, fill=INK, anchor='start', weight='600') + T(lx, yy + 15, 'lit an enemy destroyer (bar) against chance (tick)', size=12, fill=INK, anchor='start', weight='600'))
yy += 30
for lab, k in rows:
    c = g0[k]['before_any_60']; bw = 300
    fig.add(T(lx, yy + 10, f"{lab} (n {c['n']})", size=11, fill=INK, anchor='start'))
    fig.add(f'<rect x="{lx}" y="{yy + 16}" width="{bw * c["pct"] / 100:.1f}" height="12" rx="2" fill="{MUTED if k == "Daring on Loop" else "#b9b8b3"}"/>')
    bx = lx + bw * c['base_pct'] / 100
    fig.add(f'<line x1="{bx:.1f}" y1="{yy + 13}" x2="{bx:.1f}" y2="{yy + 31}" stroke="{INK}" stroke-width="2"/>')
    fig.add(T(lx + bw * max(c['pct'], c['base_pct']) / 100 + 6, yy + 26, f"{c['pct']:.0f}% vs chance {c['base_pct']:.0f}%", size=10.5, fill=INK, anchor='start'))
    yy += 44
fig.add(T(lx, yy + 8, 'Chance = share of the game\'s moments (first to last', size=10, anchor='start') + T(lx, yy + 22, 'smoke) at which the same 60 s test is true.', size=10, anchor='start'))
fig.add(T(40, 790, 'Positions are team-normalized. Radar "lit by whom" is attributed by range and time. Batch 20261117-230933. Script new-n3/c5_loop.py.', size=10, anchor='start'))
fig.save(os.path.join(FIGDIR, 'n3-loop-daring-after-radar'))
print('figures ok')
# Edge sometimes returns without writing the PNG when several renders run at once: retry.
import time
for name, w, h in (('n3-harugumo-spotter-per-shot', 1180, 620), ('n3-loop-daring-after-radar', 1120, 800)):
    for _ in range(5):
        if os.path.exists(os.path.join(FIGDIR, name + '.png')) and os.path.getsize(os.path.join(FIGDIR, name + '.png')) > 0: break
        time.sleep(3); render_png(os.path.join(FIGDIR, name + '.svg'), w, h)
print('png ok', [os.path.exists(os.path.join(FIGDIR, n + '.png')) for n in ('n3-harugumo-spotter-per-shot', 'n3-loop-daring-after-radar')])
