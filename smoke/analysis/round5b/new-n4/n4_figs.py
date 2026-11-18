# Working figures for the three claims, drawn from out-c1/2/3.json. Top 6 blue, Rest orange.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
import json
OUT = os.path.dirname(os.path.abspath(__file__)); FIGDIR = os.path.join(R5, 'figures')
J = lambda n: json.load(open(os.path.join(OUT, n), encoding='utf-8'))
c1, c2, c3 = J('out-c1.json'), J('out-c2.json'), J('out-c3.json')
MAPORDER = ['Sleeping Giant', 'Hotspot', 'Mountain Range', 'Land of Fire', 'Loop', 'Okinawa', 'Sea of Fortune']
def cis(d, f='{:+.0f}'):
    return '-' if d['ci'][0] is None else f"{f.format(d['ci'][0])} to {f.format(d['ci'][1])}" + (' *' if d['clear'] else '')
def head(fig, x, y, s): fig.add(T(x, y, s, size=13, fill=INK, anchor='start', weight='600'))
def note(fig, x, y, s): fig.add(T(x, y, s, size=10.5, anchor='start'))

# ---------- claim 1
p = c1['pops']['three ships early (round 3 population)']; tr = p['B_top_rest']
fig = Fig(1180, 470, 'Claim 1. Early smokes are laid short of the cap: smoke outline against where the ships were',
          f"Early Harugumo, Somers and Gearing smokes (n {p['n']}: Top 6 {p['n_top']}, Rest {p['n_rest']}). Right-hand text: interval of Top 6 minus Rest, * = excludes zero.")
fig.legend(24, 72, [('Top 6', BLUE), ('Rest', ORANGE)])
head(fig, 24, 104, 'Share inside a cap (%)')
rows = [('Smoke outline (batch field)', p['A_top_rest_inside']), ('Smoker when it pressed smoke', tr['smoker_in_cap_act']), ('Smoker at the end of laying', tr['smoker_in_cap_end']),
        ('Covered cruiser, at any time while the smoke stood', tr['cruiser_ever_in_cap'])]
bar_rows(fig, 24, 116, 550, [(lab, {'top': d['top'], 'rest': d['rest']}, cis(d)) for lab, d in rows], vmax=45, fmt='{:.0f}%', row_h=44, label_w=285)
note(fig, 24, 310, 'All groups together: outline %.0f%%, smoker %.0f%% at activation and %.0f%% at the end of laying, cruiser ever inside %.0f%%.' % (
    p['A_inside_cap_pct'][0], p['B_smoker_in_cap_act_pct'][0], p['B_smoker_in_cap_end_pct'][0], p['B_cruiser_ever_in_cap_pct'][0]))
head(fig, 610, 104, 'Median distance outside the cap edge (km)')
rows = [('Smoke edge to contested cap (batch field)', p['A_top_rest_edge']), ('Smoker to nearest cap, at activation', tr['smoker_near_edge_act']), ('Smoker to nearest cap, end of laying', tr['smoker_near_edge_end']),
        ('Covered cruiser to nearest cap, while it stood', tr['cruiser_near_edge'])]
bar_rows(fig, 610, 116, 550, [(lab, {'top': d['top'] / 1000, 'rest': d['rest'] / 1000}, cis(dict(ci=[d['ci'][0] / 1000, d['ci'][1] / 1000], clear=d['clear']), '{:+.1f}')) for lab, d in rows],
         vmax=4.5, fmt='{:.1f} km', row_h=44, label_w=285)
note(fig, 610, 310, 'All groups together: outline %.1f km, smoker %.1f km then %.1f km, cruiser %.1f km.' % (
    p['A_median_edge_m'][0] / 1000, p['B_smoker_near_edge_act_m'][0] / 1000, p['B_smoker_near_edge_end_m'][0] / 1000, p['B_cruiser_near_edge_m'][0] / 1000))
# distribution strip, all groups
head(fig, 24, 348, 'How far outside the nearest cap edge (all groups, number of smokes)')
bins = c1['hist_bins']; x0 = 24
for j, (lab, key, col) in enumerate((('Smoke outline (batch, contested cap)', 'hist_smoke_edge', MUTED), ('Smoker at activation', 'hist_smoker_act', VIOLET), ('Covered cruiser, average', 'hist_cruiser', AQUA))):
    y = 366 + j * 28; fig.add(T(x0 + 245, y + 14, lab, size=11, fill=INK, anchor='end'))
    tot = sum(p[key]); x = x0 + 255
    for i, v in enumerate(p[key]):
        w = 860 * v / tot
        fig.add(f'<rect x="{x:.1f}" y="{y}" width="{max(0, w - 1.5):.1f}" height="20" rx="2" fill="{col}" opacity="{0.35 + 0.1 * i:.2f}"/>')
        if w > 34: fig.add(T(x + w / 2, y + 14, f'{bins[i].replace(" the cap", "")} {v}', size=9.5, fill=INK))
        x += w
fig.save(os.path.join(FIGDIR, 'n4-claim1-short-of-cap'))

# ---------- claim 2
R = c2['rungs']
fig = Fig(1400, 520, 'Claim 2. Radar cruiser inside the early destroyer smoke, and whether it ran radar from it',
          f"All early destroyer smokes (Top 6 {c2['n_top']}, Rest {c2['n_rest']}). Share of smokes. Right-hand text: interval of Top 6 minus Rest in points, * = excludes zero.")
fig.legend(24, 72, [('Top 6', BLUE), ('Rest', ORANGE)])
head(fig, 24, 104, 'All maps: the ladder')
rows = [(R[k]['label'].replace(' (batch field)', ''), R[k]['table']['All maps']) for k in ('inside', 'used', 'lit', 'lit_dd')]
bar_rows(fig, 24, 116, 560, [(lab, {'top': d['top'], 'rest': d['rest']}, cis(d)) for lab, d in rows], vmax=75, fmt='{:.0f}%', row_h=46, label_w=270)
o = c2['of_inside']
note(fig, 24, 318, f"Of the smokes with a radar cruiser inside, it ran radar from the smoke in {o['used']['top']:.0f}% (Top 6, n {o['used']['n_top']})")
note(fig, 24, 334, f"and {o['used']['rest']:.0f}% (Rest, n {o['used']['n_rest']}); interval {cis(o['used'])}. The Top 6 lead is in having the cruiser there.")
cp = c2['cap_all_early']['rows']
head(fig, 24, 372, 'Cap taken after the smoke: radar cruiser inside (dark) against none inside (light)')
for j, (key, lab) in enumerate((('batch_takeable', 'Batch field cap_won (round 4)'), ('tl_cont', 'Cap timeline, contested cap'), ('tl_near', 'Cap timeline, nearest cap'))):
    d = cp[key]; y = 386 + j * 40
    fig.add(T(24 + 262, y + 22, lab, size=11.5, fill=INK, anchor='end'))
    for i, (v, n, op) in enumerate(((d['a'], d['n_a'], 1), (d['b'], d['n_b'], 0.4))):
        w = 150 * v / 75
        fig.add(f'<rect x="294" y="{y + 4 + i * 15}" width="{w:.1f}" height="13" rx="2" fill="{INK}" opacity="{op}"/>' + T(294 + w + 4, y + 15 + i * 15, f'{v:.0f}% (n {n})', size=9.5, anchor='start'))
    fig.add(T(600, y + 22, f"{d['diff']:+.0f} ({cis(d)})", size=9.5, anchor='end'))
for col, (k, ttl) in enumerate((('inside', 'Per map: radar cruiser inside'), ('used', 'Per map: inside and ran radar from it'))):
    x = 640 + col * 380; head(fig, x, 104, ttl)
    rows = []
    for m in MAPORDER:
        d = R[k]['table'][m]
        lab = m + (' (too few)' if d['flag_top'] == 'too few' else ' (small n)' if d['flag_top'] else '')
        rows.append((lab, {'top': 100 * d['x_top'] / d['n_top'] if d['flag_top'] != 'too few' else None, 'rest': 100 * d['x_rest'] / d['n_rest']}, f"{d['x_top']}/{d['n_top']} v {d['x_rest']}/{d['n_rest']}"))
    bar_rows(fig, x, 116, 360, rows, vmax=130, fmt='{:.0f}%', row_h=46, label_w=160)
note(fig, 640, 458, 'Right of each row: Top 6 count of smokes, then Rest. Small n = 8 to 14 Top 6 smokes; under 8 no Top 6 rate is drawn.')
fig.save(os.path.join(FIGDIR, 'n4-claim2-radar-cruiser-inside'))

# ---------- claim 3
A, B = c3['A'], c3['B']
fig = Fig(1180, 500, 'Claim 3. Radar from smoke: how often per team-game, and what a play returned',
          f"Top 6 {c3['team_games']['top']} team-games, Rest {c3['team_games']['rest']}. Right-hand text: interval of Top 6 minus Rest, * = excludes zero.")
fig.legend(24, 72, [('Top 6', BLUE), ('Rest', ORANGE)])
head(fig, 24, 104, 'Plays per team-game, counted three ways')
rows = [('Tag: destroyer smokes tagged as a radar play (round 4)', A['dd_plays']), ('Log: radar pressed inside a destroyer smoke', B['from_dd_smoke']),
        ('Log: radar pressed inside any allied smoke', B['from_smoke']), ('Log: smokes with at least one radar press', B['smokes_with_activation'])]
bar_rows(fig, 24, 116, 590, [(lab, {'top': d['top'], 'rest': d['rest']}, f"{d['n_top']} v {d['n_rest']}; {cis(d, '{:+.2f}')}") for lab, d in rows], vmax=1.35, fmt='{:.2f}', row_h=46, label_w=300)
d = B['all_activations']
note(fig, 24, 320, f"For context, all radar presses: {d['top']:.1f} per team-game (Top 6) against {d['rest']:.1f} (Rest), {d['ratio']:.1f} times. From smoke it is {B['from_smoke']['ratio']:.1f} times.")
head(fig, 24, 356, 'Radar presses from smoke per team-game, by map (all clans)')
mx = max(v['per_team_game_all'] for v in B['by_map'].values())
for i, m in enumerate(MAPORDER):
    v = B['by_map'][m]; x = 24 + i * 84; h = 70 * v['per_team_game_all'] / mx
    fig.add(f'<rect x="{x + 10}" y="{446 - h:.1f}" width="56" height="{h:.1f}" rx="2" fill="{MUTED}" opacity="0.7"/>' + T(x + 38, 442 - h, f"{v['per_team_game_all']:.2f}", size=10, fill=INK)
            + T(x + 38, 460, m, size=9, fill=INK) + T(x + 38, 472, f"{v['n_top']} v {v['n_rest']}", size=9))
rt = B['return_from_smoke']
head(fig, 650, 104, f"Return per radar press from smoke (n {rt['n']})")
y = 116
for lab, k, vmax, fm, cf in (('Enemy ships lit', 'lit', 2.2, '{:.2f}', '{:+.2f}'), ('Enemy destroyers lit', 'lit_dd', 2.2, '{:.2f}', '{:+.2f}'), ('Lit at least one enemy destroyer', 'lit_dd_any', 100, '{:.0f}%', '{:+.0f}'),
                             ('Damage on lit enemies while lit', 'dmg', 11000, '{:,.0f}', '{:+,.0f}'), ('Cap taken within 60 s (caps not ours)', 'cap60', 100, '{:.0f}%', '{:+.0f}'),
                             ('Cap taken within 120 s (caps not ours)', 'cap120', 100, '{:.0f}%', '{:+.0f}')):
    d = rt[k]
    y = bar_rows(fig, 650, y, 510, [(lab, {'top': d['top'], 'rest': d['rest']}, cis(d, cf))], vmax=vmax, fmt=fm, row_h=46, label_w=215)
note(fig, 650, 410, f"Cap rows: {rt['cap60']['n_top']} Top 6 and {rt['cap60']['n_rest']} Rest presses near a cap that was not theirs. No interval excludes zero:")
note(fig, 650, 426, 'the return per press is the same for both groups; the Top 6 press radar from smoke more often.')
fig.save(os.path.join(FIGDIR, 'n4-claim3-radar-from-smoke'))
print('figures ok')
