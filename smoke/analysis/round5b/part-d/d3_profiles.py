# D2 styles and D3 profiles: reads d1_scores.json and d2_structure.json, writes clan_styles.json, d3_tables.md and the three working figures.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_lib import *
HERE = os.path.dirname(os.path.abspath(__file__)); FIGS = os.path.join(os.path.dirname(HERE), 'figures')
random.seed(521)
D1 = json.load(open(os.path.join(HERE, 'd1_scores.json'), encoding='utf-8'))
D2 = json.load(open(os.path.join(HERE, 'd2_structure.json'), encoding='utf-8'))
V, I, PC = D1['values'], D1['intervals'], D1['percentiles']
K = 4
STYLES = [  # index = group number of the 2-axis k-means (ordered by centre on axis 1, see d2_structure.py)
    dict(id='team_plenty', name='Team smoke, plenty of it', short='Team smoke, plenty'),
    dict(id='team_sparse', name='Team smoke, little of it', short='Team smoke, little'),
    dict(id='own_sparse', name='Own smoke, little of it', short='Own smoke, little'),
    dict(id='own_plenty', name='Own smoke, plenty of it', short='Own smoke, plenty'),
]
cen = D2['cen2'][str(K)]
assert cen[0][0] < 0 and cen[0][1] > 0 and cen[1][0] < 0 and cen[1][1] < 0 and cen[2][0] > 0 and cen[2][1] < 0 and cen[3][0] > 0 and cen[3][1] > 0, cen
lab = dict(zip(D2['clans'], D2['km2'][str(K)])); keep = D2['keep2'][str(K)]
SC = dict(zip(D2['clans'], D2['scores']))
BORDER = 0.75
for t in SMALL: SC[t] = D2['proj'][t]['pc']; lab[t] = D2['proj'][t]['near2'][str(K)]

# pooled numbers per style (and round 4's two Top 6 groups as a second check), with intervals from resampling games
for t in CLANS:
    for g in GAMES[t]: SG[('_p', (t, g))] = SG[(t, g)]; RO[('_p', (t, g))] = RO[(t, g)]
def pool(clans, reps=400):
    tg = [(t, g) for t in clans for g in GAMES[t]]
    f = feats('_p', tg); acc = collections.defaultdict(list)
    for _ in range(reps):
        b = feats('_p', random.choices(tg, k=len(tg)))
        for k in ALLKEYS:
            if b[k] is not None: acc[k].append(b[k])
    ci_ = {k: (sorted(v)[int(.025 * len(v))], sorted(v)[int(.975 * len(v)) - 1]) for k, v in acc.items()}
    return f, ci_
def fmt(k, v):
    if v is None: return 'too few'
    if k.endswith('_pg') and k != 'conc_pg': return f'{v:.1f}'
    if k in ('conc_pg', 'conc_per_smoke', 'edge_m'): return f'{v:,.0f}'
    if k == 'first_smoke_s': return f'{int(v) // 60}:{int(v) % 60:02d}'
    return f'{v:.0f}'
members = {i: [t for t in CLANS7 if lab[t] == i] for i in range(K)}
POOL = {i: pool(members[i]) for i in range(K)}
out = ['#### Styles: pooled numbers (95% interval, games resampled within the style)\n']
show = PCA_KEYS + ['caps_taken_pg', 'cap_def_pg']
hdr = ['Score'] + [f"{STYLES[i]['short']} ({len(members[i])} clans, {POOL[i][0]['n_games']} games, {POOL[i][0]['n_smokes']} smokes)" for i in (0, 3, 1, 2)]
out.append(md_table(hdr, [[LABEL[k]] + [f'{fmt(k, POOL[i][0][k])} ({fmt(k, POOL[i][1][k][0])} to {fmt(k, POOL[i][1][k][1])})' for i in (0, 3, 1, 2)] for k in show]))
out.append('\n#### Style members\n')
for i in (0, 3, 1, 2):
    w = sum(WLD[t][0] for t in members[i]); l = sum(WLD[t][1] for t in members[i])
    out.append(f"- **{STYLES[i]['name']}** (W-L {w}-{l}): Top 6: {', '.join(t for t in members[i] if t in TOP) or 'none'} | Rest: {', '.join(t for t in members[i] if t not in TOP) or 'none'}"
               f" | borderline (kept the style in under {BORDER:.0%} of resamples): {', '.join(f'{t} {keep[t]:.0%}' for t in members[i] if keep[t] < BORDER) or 'none'}"
               f" | flagged small clans that would fall here: {', '.join(t for t in SMALL if lab[t] == i) or 'none'}")
# round 4 check
a, ca = pool(['H-SR', 'RESIN', 'BONKZ']); b, cb = pool(['HTDOG', 'VRTUS'])
out.append('\n#### Second check against round 4 (Top 6 only)\n')
out.append(md_table(['Score', 'H-SR, RESIN, BONKZ', 'HTDOG, VRTUS'], [[LABEL[k], f'{fmt(k, a[k])} ({fmt(k, ca[k][0])} to {fmt(k, ca[k][1])})', f'{fmt(k, b[k])} ({fmt(k, cb[k][0])} to {fmt(k, cb[k][1])})']
                                                                       for k in ('smoke_cruisers_pg', 'long_ships_pg', 'smokes_pg', 'teammate_pct', 'stacked_pct', 'parked_pct', 'first_smoke_s')]))
# Top 6 vs Rest on the two axes (clans resampled) and the chance of the Top 6 pattern
top = [t for t in CLANS7 if t in TOP]; rest = [t for t in CLANS7 if t not in TOP]
AX = {}
for ax in (0, 1):
    d = mean(SC[t][ax] for t in top) - mean(SC[t][ax] for t in rest); o = []
    for _ in range(2000):
        o.append(mean(SC[t][ax] for t in random.choices(top, k=6)) - mean(SC[t][ax] for t in random.choices(rest, k=len(rest))))
    o.sort(); AX[ax] = dict(top6=mean(SC[t][ax] for t in top), rest=mean(SC[t][ax] for t in rest), gap=d, lo=o[50], hi=o[1949])
    out.append(f"\n- Axis {ax + 1}: Top 6 mean {AX[ax]['top6']:+.2f}, Rest mean {AX[ax]['rest']:+.2f}, gap {d:+.2f} (95% {o[50]:+.2f} to {o[1949]:+.2f}{' *' if o[50] * o[1949] > 0 else ''}); Top 6 range {min(SC[t][ax] for t in top):+.1f} to {max(SC[t][ax] for t in top):+.1f}, Rest range {min(SC[t][ax] for t in rest):+.1f} to {max(SC[t][ax] for t in rest):+.1f}")
plenty = [t for t in CLANS7 if lab[t] in (0, 3)]
p_all = math.comb(len(plenty), 6) / math.comb(24, 6)
out.append(f'- Clans in a "plenty" style: {len(plenty)} of 24; Top 6 in them: {sum(t in TOP for t in plenty)} of 6. Chance that 6 clans drawn at random from the 24 all land there: {p_all:.3f}')
n0_ = len(members[0]); p4 = sum(math.comb(n0_, k) * math.comb(24 - n0_, 6 - k) for k in range(4, 7)) / math.comb(24, 6)
out.append(f'- Top 6 in "{STYLES[0]["name"]}": {sum(t in TOP for t in members[0])} of 6 ({n0_} of 24 clans are in it). Chance of 4 or more of 6 at random: {p4:.2f}')
open(os.path.join(HERE, 'd3_tables.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))

# ---------- JSON fragment
def r(x, n=2):
    return None if x is None else round(x, n)
dims = []
for d in DIMS:
    dims.append(dict(id=d['id'], name=d['name'], headline=d['headline'], headline_label=LABEL[d['headline']], direction='0 = lowest clan, 100 = highest clan; high = ' + d['high'],
                     scores=[dict(key=k, label=LABEL[k], direction=DIRECTION[k]) for k in d['keys']]))
extra = [dict(key=k, label=LABEL[k], direction=DIRECTION[k]) for k in ALLKEYS if k not in PCA_KEYS]
clans = {}
for t in CLANS:
    small = t in SMALL
    st = STYLES[lab[t]]
    clans[t] = dict(games=NG[t], wins=WLD[t][0], losses=WLD[t][1], group='top6' if t in TOP else 'rest', flagged_small=small, smokes=V[t]['n_smokes'], destroyer_smokes=V[t]['n_dd_smokes'],
                    values={k: r(V[t][k]) for k in ALLKEYS}, percentiles={k: r(PC[t][k], 0) for k in ALLKEYS},
                    intervals={k: [r(I[t][k][0]), r(I[t][k][1])] for k in ALLKEYS if k in I[t]},
                    gauge=[dict(dimension=d['id'], key=d['headline'], label=LABEL[d['headline']], value=r(V[t][d['headline']]), percentile=r(PC[t][d['headline']], 0),
                                interval=[r(I[t][d['headline']][0]), r(I[t][d['headline']][1])]) for d in DIMS],
                    axes=dict(who_axis=r(SC[t][0]), amount_axis=r(SC[t][1]), who_interval=[r(x) for x in D2['pc_ci'][t][0]] if t in D2['pc_ci'] else None,
                              amount_interval=[r(x) for x in D2['pc_ci'][t][1]] if t in D2['pc_ci'] else None),
                    style=st['name'], style_id=st['id'],
                    style_note=('fewer than 7 games: not used to build the styles; this is where it would fall' if small else
                                f'borderline: kept this style in {keep[t]:.0%} of game resamples' if keep[t] < BORDER else f'kept this style in {keep[t]:.0%} of game resamples'),
                    style_kept_share=None if small else r(keep[t]), notes=D1['notes'][t])
desc = {
 0: 'Long-smoke destroyers (Somers, Gearing, Harugumo) lay smoke for a cruiser, usually a radar cruiser, and they lay a lot of it. Few cruisers bring their own smoke.',
 3: 'Cruisers (Svea, Jinan, Napoli) and cap-sitter destroyers (Daring, Gdansk, Shimakaze) each smoke for themselves, often parked, and there is a lot of smoke per game.',
 1: 'The same team-smoke habit, but few smoke ships in the lineup and few smokes per game; the first smoke comes late.',
 2: 'Ships smoke for themselves (Napoli exhaust, cap sitters), with few smoke destroyers and few smokes per game.'}
styles = []
for i in (0, 3, 1, 2):
    f, c = POOL[i]
    styles.append(dict(id=STYLES[i]['id'], name=STYLES[i]['name'], description=desc[i], top6=[t for t in members[i] if t in TOP], rest=[t for t in members[i] if t not in TOP],
                       borderline=[t for t in members[i] if keep[t] < BORDER], flagged_small_would_fall_here=[t for t in SMALL if lab[t] == i],
                       centre=dict(who_axis=r(cen[i][0]), amount_axis=r(cen[i][1])), games=f['n_games'], smokes=f['n_smokes'],
                       wins=sum(WLD[t][0] for t in members[i]), losses=sum(WLD[t][1] for t in members[i]),
                       numbers={k: dict(value=r(f[k]), interval=[r(c[k][0]), r(c[k][1])]) for k in show}))
structure = dict(
    scores_used=D2['keys'], clans_used=len(D2['clans']),
    pc1_share=r(D2['shares'][0], 3), pc2_share=r(D2['shares'][1], 3), pc3_share=r(D2['shares'][2], 3),
    shuffled_data_95th=dict(pc1=r(D2['null']['pc1_p95'], 3), pc2=r(D2['null']['pc2_p95'], 3)),
    loadings=dict(pc1={k: r(x) for k, x in zip(D2['keys'], D2['loadings'][0])}, pc2={k: r(x) for k, x in zip(D2['keys'], D2['loadings'][1])}),
    what_they_mean=dict(
        pc1='Who the smoke is for. Low end: long-smoke destroyers laying smoke on or in front of a teammate, with a radar cruiser inside. High end: cruisers and cap-sitter destroyers that carry smoke and use it on themselves, more often parked or kiting.',
        pc2='How much smoke. High end: more destroyers carrying smoke, more smokes per game, an earlier first smoke. Low end: few smoke ships, few smokes, later, more of it while pushing.'),
    one_scale_or_several=('Two separate scales, not one, and not sharp types. "Adds a smoke cruiser or not" is one part of the first scale (r +0.71 with it) but who the smoke is laid for tracks it more closely (r -0.82). '
                          'The second scale, how much smoke a clan brings and uses, is unrelated to the first. Together they carry 47% of the differences between clans. Clans are spread along the first scale without a break; on the second there is a gap that sets seven low-smoke clans apart. '
                          'The four named styles are the four corners of that two-scale map. They are regions with soft borders: grouping on all 17 scores at once is not stable when games are resampled.'),
    stability=dict(silhouette_17_scores={k: r(v) for k, v in D2['silhouette'].items()}, silhouette_shuffled_95th={k: r(v['p95']) for k, v in D2['null']['sil'].items()},
                   ari_games_resampled_k2_median=r(med(D2['boot']['ari2'])), ari_games_resampled_k3_median=r(med(D2['boot']['ari3'])),
                   axis1_scores_r_median=r(med(D2['boot']['r1'])), axis2_scores_r_median=r(med(D2['boot']['r2'])),
                   drop_one_group={k: dict(ari=r(v['ari']), clans_switching=v['switch'], pc1_share=r(v['pc1'], 3), pc2_share=r(v['pc2'], 3)) for k, v in D2['drop_group'].items()},
                   style_kept_share_mean=r(mean(keep[t] for t in CLANS7))),
    top6_vs_rest_on_axes=dict(who_axis={k: r(v) for k, v in AX[0].items()}, amount_axis={k: r(v) for k, v in AX[1].items()}),
    top6_concentration=dict(in_plenty_styles=sum(t in TOP for t in plenty), plenty_clans=len(plenty), chance_all_six=r(p_all, 3), in_team_plenty=sum(t in TOP for t in members[0]), chance_4_plus=r(p4, 2),
                            caveat='Six clans is very few; neither count is beyond what chance allows at the usual 5% level. Styles describe; they do not explain winning.'))
frag = dict(batch=BATCH_NAME, note='Association only. Percentiles are positions among the 24 clans with 7+ games (0 = lowest, 100 = highest). Intervals are 95%, from resampling the clan\'s own games. '
            'Rates with fewer than 8 cases are null ("too few"). Movement: pushing = batch label pushing (range to the nearest enemies closed while laying), kiting = batch label kiting (range opened), '
            'parked = batch label stationary; the batch label horizontal is reported as sideways and unclassified stays in the denominator.',
            dimensions=dims, extra_scores=extra, clans=clans, styles=styles, structure=structure, top6_minus_rest=D1['gaps'])
json.dump(frag, open(os.path.join(HERE, 'clan_styles.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote clan_styles.json', len(clans), 'clans')

# ---------- figures
SHORT = dict(long_ships_pg='Long-smoke DD /game', sitter_ships_pg='Cap-sitter DD /game', smoke_dd_pg='Smoke DD /game', smoke_cruisers_pg='Smoke cruisers /game', exhaust_ships_pg='Exhaust ships /game',
             smokes_pg='Smokes /game', first_smoke_s='First smoke', late_pct='After 12:00 %', teammate_pct='For teammate %', stacked_pct='Stacked %', radar_ca_inside_pct='Radar cruiser inside %',
             edge_m='Metres to cap', inside_cap_pct='Inside cap %', centre_pct='Centre lane %', pushing_pct='Pushing %', kiting_pct='Kiting %', parked_pct='Parked %',
             conc_per_smoke='Conc. dmg /smoke (k)', conc_pg='Conc. dmg /game (k)', took_pct='Cap taken %', held_pct='Cap not lost %', deaths_per100='Deaths /100')
def cellval(k, v):
    if v is None: return '-'
    if k in ('conc_per_smoke', 'conc_pg'): return f'{v / 1000:.0f}'
    if k == 'edge_m': return f'{max(v, 0) / 1000:.1f}k' if v > -50 else f'{v / 1000:.1f}k'
    return fmt(k, v)
order = [t for i in (0, 3, 1, 2) for t in sorted(members[i], key=lambda t: SC[t][0])] + SMALL
# figure 1: heat table
cw, rh, x0, y0 = 46, 21, 150, 190
fig = Fig(x0 + cw * len(PCA_KEYS) + 40, y0 + rh * (len(order) + 4) + 60, 'Clan scores on the six dimensions',
          'Cell text = the clan\'s value. Shade = percentile among the 24 clans with 7+ games (darker = higher). Clan names: Top 6 blue, Rest orange. Grey rows = under 7 games (flagged).')
x = x0
for d in DIMS:
    fig.add(T(x + cw * len(d['keys']) / 2, y0 - 118, d['name'], size=12, fill=INK, weight='600'))
    fig.add(f'<line x1="{x + 3}" y1="{y0 - 112}" x2="{x + cw * len(d["keys"]) - 3}" y2="{y0 - 112}" stroke="{MUTED}" stroke-width="1"/>')
    for k in d['keys']:
        fig.add(f'<text transform="translate({x + cw / 2 + 4},{y0 - 6}) rotate(-55)" font-size="10.5" fill="{INK}" text-anchor="start">{esc(SHORT[k])}</text>')
        x += cw
y = y0; prev = None
for t in order:
    grp = 'flag' if t in SMALL else lab[t]
    if grp != prev:
        y += 6
        fig.add(T(8, y + 12, 'Under 7 games (flagged)' if grp == 'flag' else STYLES[grp]['name'], size=11, fill=INK, anchor='start', weight='600')); y += 17; prev = grp
    fig.add(T(x0 - 8, y + rh / 2 + 4, f'{t} ({NG[t]})', size=11, fill=MUTED if t in SMALL else BLUE if t in TOP else ORANGE, anchor='end', weight='600'))
    for j, k in enumerate(PCA_KEYS):
        p = PC[t][k]; v = V[t][k]
        col = GRID if p is None else (seq_color(p, 100) if t not in SMALL else '#ececea')
        tf = INK if (p is None or t in SMALL) else seq_text(p, 100)
        fig.add(f'<rect x="{x0 + j * cw + 1}" y="{y + 1}" width="{cw - 2}" height="{rh - 2}" rx="2" fill="{col}"/>' + T(x0 + j * cw + cw / 2, y + rh / 2 + 4, cellval(k, v), size=9.5, fill=tf))
    y += rh
fig.add(T(8, y + 22, 'Number after the clan name = games. Styles are corners of the two-scale map, not hard types. Association only.', size=10.5, anchor='start'))
fig.h = y + 40
fig.body[0] = f'<rect width="{fig.w}" height="{fig.h}" fill="{BG}"/>' + fig.body[0].split('/>', 1)[1]
fig.save(os.path.join(FIGS, 'd1-clan-heat-table'))

# figure 2: PCA scatter
W, H = 980, 760; px0, py0, pw, ph = 80, 90, 840, 580
xs = [SC[t][0] for t in CLANS]; ys = [SC[t][1] for t in CLANS]
xa, xb, ya, yb = min(xs) - 0.7, max(xs) + 0.9, min(ys) - 0.5, max(ys) + 0.6
X = lambda v: px0 + (v - xa) / (xb - xa) * pw; Y = lambda v: py0 + ph - (v - ya) / (yb - ya) * ph
fig = Fig(W, H, 'Clan smoke styles: two scales', f'Each clan placed by its 17 behaviour scores. Left-right carries {100 * D2["shares"][0]:.0f}% of the differences between clans, up-down {100 * D2["shares"][1]:.0f}%. Top 6 blue, Rest orange, hollow grey = under 7 games.')
fig.add(f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="none" stroke="{GRID}"/>')
fig.add(f'<line x1="{X(0):.1f}" y1="{py0}" x2="{X(0):.1f}" y2="{py0 + ph}" stroke="{GRID}" stroke-width="1.5"/><line x1="{px0}" y1="{Y(0):.1f}" x2="{px0 + pw}" y2="{Y(0):.1f}" stroke="{GRID}" stroke-width="1.5"/>')
for i in range(K):
    fig.add(T(X(cen[i][0]), Y(cen[i][1]) + (-ph * 0.20 if cen[i][1] > 0 else ph * 0.17), STYLES[i]['name'].upper(), size=12, fill='#9a9994', weight='700'))
fig.add(T(px0, py0 + ph + 34, '<- destroyer smoke laid for a teammate, radar cruiser inside', size=12, fill=INK, anchor='start'))
fig.add(T(px0 + pw, py0 + ph + 34, 'ships smoke for themselves (smoke cruisers, cap sitters) ->', size=12, fill=INK, anchor='end'))
fig.add(f'<text transform="translate({px0 - 48},{py0 + ph}) rotate(-90)" font-size="12" fill="{INK}" text-anchor="start">&lt;- few smoke ships, few smokes, later</text>')
fig.add(f'<text transform="translate({px0 - 48},{py0}) rotate(-90)" font-size="12" fill="{INK}" text-anchor="end">more smoke ships, more smokes, earlier -&gt;</text>')
for v in range(int(xa), int(xb) + 1): fig.add(T(X(v), py0 + ph + 14, f'{v:+d}', size=9.5))
for v in range(int(ya), int(yb) + 1): fig.add(T(px0 - 8, Y(v) + 3, f'{v:+d}', size=9.5, anchor='end'))
placed = []
for t in sorted(CLANS, key=lambda t: SC[t][1]):
    x, y = X(SC[t][0]), Y(SC[t][1]); col = MUTED if t in SMALL else BLUE if t in TOP else ORANGE
    if t in SMALL: fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BG}" stroke="{MUTED}" stroke-width="1.5"/>')
    else:
        fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 + NG[t] / 6:.1f}" fill="{col}" opacity="0.85"/>')
        if keep[t] < BORDER: fig.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 + NG[t] / 6:.1f}" fill="none" stroke="{col}" stroke-width="1" stroke-dasharray="3 2"/>')
    ly = y + 4; lx = x + 11 + NG[t] / 6
    for (ox, oy) in placed:
        if abs(ox - lx) < 48 and abs(oy - ly) < 11: ly = oy - 12
    placed.append((lx, ly))
    if t in SMALL: fig.add(T(x - 9, y + 4, t, size=11, fill=col, anchor='end', weight='600', halo=True))
    else: fig.add(T(lx, ly, t, size=11.5, fill=col, anchor='start', weight='600', halo=True))
fig.legend(px0, 72, [('Top 6', BLUE), ('Rest', ORANGE), ('Under 7 games (flagged, placed on the same scales)', MUTED)])
fig.add(T(px0, H - 22, 'Dot size = games played. Dashed ring = borderline: the clan kept its style in under 75% of resamples of its own games. Association only.', size=10.5, anchor='start'))
fig.save(os.path.join(FIGS, 'd2-style-map'))

# figure 3: gauge strip for two contrasting clans
PAIR = ['H-SR', 'HTDOG']
POOLV = {k: sorted(V[t][k] for t in CLANS7 if V[t][k] is not None) for k in ALLKEYS}
fig = Fig(1120, 170 + 6 * 54, 'Example gauge strip: H-SR and HTDOG', 'One number per dimension. Dot = position among the 24 clans with 7+ games (0 = lowest, 100 = highest). Bar = 95% range from resampling the clan\'s games.')
for ci_, t in enumerate(PAIR):
    gx = 40 + ci_ * 550; gw = 250
    fig.add(T(gx, 96, f"{t}  ({WLD[t][0]}-{WLD[t][1]}, {V[t]['n_smokes']} smokes)  {STYLES[lab[t]]['name']}", size=13.5, fill=BLUE if t in TOP else ORANGE, anchor='start', weight='700'))
    for j, d in enumerate(DIMS):
        k = d['headline']; y = 130 + j * 54; bx = gx + 150
        fig.add(T(gx, y + 4, d['name'], size=11.5, fill=INK, anchor='start', weight='600') + T(gx, y + 18, SHORT[k], size=10, anchor='start'))
        fig.add(f'<rect x="{bx}" y="{y - 4}" width="{gw}" height="8" rx="4" fill="{GRID}"/>')
        for tick in (0, 50, 100): fig.add(f'<line x1="{bx + gw * tick / 100}" y1="{y - 8}" x2="{bx + gw * tick / 100}" y2="{y + 8}" stroke="{MUTED}" stroke-width="0.8"/>' + T(bx + gw * tick / 100, y + 20, str(tick), size=8.5))
        lo, hi = [pctile(v, POOLV[k]) for v in I[t][k]]; p = PC[t][k]
        fig.add(f'<rect x="{bx + gw * lo / 100:.1f}" y="{y - 4}" width="{max(2, gw * (hi - lo) / 100):.1f}" height="8" rx="4" fill="{BLUE}" opacity="0.35"/>')
        fig.add(f'<circle cx="{bx + gw * p / 100:.1f}" cy="{y}" r="7" fill="{BLUE}" stroke="{BG}" stroke-width="1.5"/>')
        fig.add(T(bx + gw + 12, y + 4, f'{cellval(k, V[t][k])}', size=12.5, fill=INK, anchor='start', weight='600') + T(bx + gw + 12, y + 18, f'{cellval(k, I[t][k][0])} to {cellval(k, I[t][k][1])}', size=9.5, anchor='start'))
fig.save(os.path.join(FIGS, 'd3-gauge-strip-example'))
print('figures ok')
