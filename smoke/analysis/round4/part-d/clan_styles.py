# Part D: clan smoke styles. Writes STYLES.md, styles.json and two figures into this folder. Read-only on the batch.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_lib import *
OUT = os.path.dirname(os.path.abspath(__file__))
REST = sorted(t for t in GAMES if t not in TOP)
A, B, K = smokes_of(STYLE_A), smokes_of(STYLE_B), smokes_of(MID)
mmss = lambda s: f'{int(s) // 60}:{int(s) % 60:02d}'
STYLE_COLOR = {'A': BLUE, 'B': ORANGE, 'K': VIOLET, 'PN': AQUA}
def style_of(t): return 'A' if t in STYLE_A else 'B' if t in STYLE_B else 'K' if t in MID else 'PN' if t == PN else 'rest'

def smoker_dmg(ss):
    tot = sum(x['conc'] for s in ss for x in s['shooters']); own = sum(x['conc'] for s in ss for x in s['shooters'] if x['is_smoker'])
    return 100 * own / tot if tot else None
def no_smoke_dd(teams):
    v = [sum(p['ship_class'] == 'Destroyer' and not p.get('smoke_variant') for p in G[k]['roster'].values() if p['team'] == t) for k, t in tgs_of(teams)]
    return mean(v)
def full(teams):
    d = numbers(teams); d['smoker_own_dmg_pct'] = smoker_dmg(smokes_of(teams)); c = cast_numbers(teams); c['dd_without_smoke_per_game'] = no_smoke_dd(teams)
    return dict(define=d, cast=c)

groups = {'A': STYLE_A, 'B': STYLE_B, 'K': MID, 'PN': [PN], 'rest': REST}
DATA = {k: full(v) for k, v in groups.items()}
CLAN = {t: full([t]) for t in CLANS7}

# intervals for style A minus style B (resampling games within each style)
DEF_ROWS = [('flank_lines_pct', 'Smokes from flank-smoke-line ships', '{:.0f}%'), ('parked_cruiser_pct', 'Smokes from parked-cruiser-smoke ships', '{:.0f}%'),
            ('cap_sitters_pct', 'Smokes from cap-sitter ships', '{:.0f}%'), ('stacked_pct', 'Stacked (laid on a teammate)', '{:.0f}%'),
            ('selfish_pct', 'Selfish (covers only the smoker)', '{:.0f}%'), ('stationary_pct', 'Stationary', '{:.0f}%'),
            ('first_smoke_s', 'First smoke of the game (median)', 'time'), ('cruiser_dmg_pct', 'Smoke damage dealt by cruisers', '{:.0f}%'),
            ('smokes_per_game', 'Smokes per game', '{:.1f}')]
def spg(ss): return len(ss) / len({(s['game'], s['team']) for s in ss}) if ss else None  # per game with a smoke; every A and B team-game has one
STATF = dict(STATS, smokes_per_game=spg, smoker_own_dmg_pct=smoker_dmg)
random.seed(19)
DIFF = {k: boot2(A, B, STATF[k]) for k, _, _ in DEF_ROWS}
DIFF['smoker_own_dmg_pct'] = boot2(A, B, smoker_dmg)
ddA, ddB, ddR = [[s for s in x if s['cls'] == 'destroyer'] for x in (A, B, smokes_of(REST))]
fwd = lambda ss: pct(ss, second_fwd)
DIFF['second_dd_fwd_pct'] = boot2(ddA, ddB, fwd)
DIFF['second_dd_fwd_pct_A_vs_rest'] = boot2(ddA, ddR, fwd)
early = lambda x: [s for s in x if s['el'] <= 300]
DIFF['second_dd_fwd_pct_early'] = boot2(early(ddA), early(ddB), fwd)
def gdiff(teams_a, teams_b, f):
    """Difference of a per-team-game roster count, resampling team-games."""
    va = [f(k, t) for k, t in tgs_of(teams_a)]; vb = [f(k, t) for k, t in tgs_of(teams_b)]; out = []
    for _ in range(1000): out.append(mean(random.choices(va, k=len(va))) - mean(random.choices(vb, k=len(vb))))
    out.sort(); return out[25], out[974]
cnt = lambda pred: (lambda k, t: sum(pred(p) for p in G[k]['roster'].values() if p['team'] == t))
DIFF['dd_per_game'] = gdiff(STYLE_A, STYLE_B, cnt(lambda p: p['ship_class'] == 'Destroyer'))
DIFF['smoke_cruisers_per_game'] = gdiff(STYLE_A, STYLE_B, cnt(lambda p: p['ship_class'] == 'Cruiser' and bool(p.get('smoke_variant'))))
DIFF['smokes_per_game'] = gdiff(STYLE_A, STYLE_B, lambda k, t: sum(1 for x in BY_TEAM[t] if x['game'] == k))
DIFF['smoke_ships_per_game'] = gdiff(STYLE_A, STYLE_B, cnt(lambda p: bool(p.get('smoke_variant'))))

# ---------- maps
def map_stats(ss, m):
    size = MAPS[m]['space_size']; n = len(ss)
    if not n: return dict(n=0, games=0)
    return dict(n=n, games=len({(s['game'], s['team']) for s in ss}), destroyer_pct=pct(ss, lambda s: s['cls'] == 'destroyer'), cruiser_pct=pct(ss, lambda s: s['cls'] == 'cruiser'),
                west_pct=pct(ss, lambda s: s['nx'] < -size / 6), middle_pct=pct(ss, lambda s: abs(s['nx']) <= size / 6), east_pct=pct(ss, lambda s: s['nx'] > size / 6),
                own_half_pct=pct(ss, lambda s: s['nz'] < 0), inside_cap_pct=pct(ss, lambda s: s['inside']), stationary_pct=pct(ss, lambda s: s['movement'] == 'stationary'),
                caps=dict(C(s['ncap'] for s in ss).most_common()), top_cells=C(s['ncell_name'] for s in ss).most_common(3))
MAPD = {m: {k: map_stats([s for s in x if s['map'] == m], m) for k, x in (('A', A), ('B', B), ('K', K))} for m in MAIN_MAPS}
def mdiff(m, f):
    return boot2([s for s in A if s['map'] == m], [s for s in B if s['map'] == m], lambda ss: pct(ss, f))
sz = {m: MAPS[m]['space_size'] for m in MAIN_MAPS}
P = lambda v: f'{v:.0f}%'
def cap_n(m, k, c): return MAPD[m][k]['caps'].get(c, 0)
d = MAPD; CAP = {}
m = 'Sleeping Giant'; a, b = d[m]['A'], d[m]['B']
i1 = mdiff(m, lambda s: s['nx'] > sz[m] / 6); i2 = mdiff(m, lambda s: s['movement'] == 'stationary')
CAP[m] = (f"The long-smoke style works both flanks ({P(a['west_pct'])} of smokes in the west third, {P(a['east_pct'])} in the east third; {a['n']} smokes, {a['games']} games); "
          f"the cruiser-smoke style stays west and centre ({P(b['west_pct'])} west, {P(b['middle_pct'])} middle, {P(b['east_pct'])} east; {b['n']} smokes, {b['games']} games; east-third gap {ci(i1, '{:+.0f}')} points) "
          f"and parks more ({P(b['stationary_pct'])} stationary against {P(a['stationary_pct'])}; gap {ci(i2, '{:+.0f}')}).")
m = 'Hotspot'; a, b = d[m]['A'], d[m]['B']
CAP[m] = (f"Not enough to separate the styles: the cruiser-smoke clans have {b['n']} smokes in {b['games']} games here (small n), and all {b['n']} are destroyer smokes; they left the smoke cruisers out on this map. "
          f"The long-smoke style ({a['n']} smokes, {a['games']} games, {P(a['destroyer_pct'])} destroyer) uses the east edge most (column 10, rows F and G: {sum(1 for s in A if s['map'] == m and s['ncell_name'] in ('F10', 'G10'))} of {a['n']}).")
m = 'Mountain Range'; a, b = d[m]['A'], d[m]['B']
i1 = mdiff(m, lambda s: s['cls'] == 'destroyer'); i2 = mdiff(m, lambda s: abs(s['nx']) <= sz[m] / 6)
CAP[m] = (f"Who smokes flips: {P(a['destroyer_pct'])} destroyer smoke for the long-smoke style ({a['n']} smokes, {a['games']} games) against {P(b['destroyer_pct'])} for the cruiser-smoke style "
          f"({b['n']} smokes, {b['games']} games; gap {ci(i1, '{:+.0f}')} points). The long-smoke style smokes the middle third ({P(a['middle_pct'])}); the cruiser-smoke style spreads west ({P(b['west_pct'])} west, {P(b['middle_pct'])} middle; middle gap {ci(i2, '{:+.0f}')}).")
m = 'Land of Fire'; a, b = d[m]['A'], d[m]['B']
i2 = mdiff(m, lambda s: s['movement'] == 'stationary')
CAP[m] = (f"Same place, different smoke: both styles smoke the middle around cap B ({cap_n(m, 'A', 'B')} of {a['n']} and {cap_n(m, 'B', 'B')} of {b['n']} smokes). The cruiser-smoke style parks there "
          f"({P(b['stationary_pct'])} stationary against {P(a['stationary_pct'])}, gap {ci(i2, '{:+.0f}')} points; {dict(b['top_cells']).get('F5', 0)} of {b['n']} smokes in cell F5) and half of it is cruiser smoke ({P(b['cruiser_pct'])} against {P(a['cruiser_pct'])}). "
          f"{a['n']} smokes in {a['games']} games against {b['n']} in {b['games']}.")

# ---------- nearest style
NEAR = {t: dict(zip(('dist_long', 'dist_cruiser', 'nearest'), nearest(t))) for t in CLANS7}
PAIR = {a_: {b_: round(dist(Z[a_], Z[b_]), 2) for b_ in STYLE_A + MID + STYLE_B + [PN]} for a_ in STYLE_A + MID + STYLE_B + [PN]}

# ---------- figure 1: where each style smokes
CLS_COLOR = {'destroyer': BLUE, 'cruiser': ORANGE, 'battleship': VIOLET}
def fig_maps():
    ps, gap, x0, top, rowh = 268, 30, 40, 124, 342
    rows = [('A', f'{A_NAME}: H-SR, RESIN, BONKZ', A), ('B', f'{B_NAME}: HTDOG, VRTUS', B), ('K', 'KITE (nearer the long-smoke style; small n, shown for reference only)', K)]
    fig = Fig(x0 + 4 * ps + 3 * gap + 30, top + 3 * rowh - 10, 'Where each style smokes on the 4 main maps',
              'All classes. Each line is one smoke as laid, the dot is its centre. Own spawn at the bottom (north-spawn teams mirrored north-south).')
    fig.legend(40, 72, [('Destroyer smoke', BLUE), ('Cruiser smoke', ORANGE), ('Battleship smoke', VIOLET)])
    for ri, (k, lab, ss) in enumerate(rows):
        y = top + ri * rowh
        fig.add(T(x0, y - 26, lab, size=13.5, fill=INK, anchor='start', weight='700'))
        for ci_, m in enumerate(MAIN_MAPS):
            st = MAPD[m][k]; note = ' (small n)' if 8 <= st['n'] < 15 else ' (too few)' if st['n'] < 8 else ''
            p = Panel(m, x0 + ci_ * (ps + gap), y, ps, G, title=f"{m}: {st['n']} smokes, {st['games']} game{'s' if st['games'] != 1 else ''}{note}", dim=0.45, grid_labels=False)
            for s in ss:
                if s['map'] != m: continue
                col = CLS_COLOR[s['cls']]
                p.line(s['npath'], stroke=col, width=2.2, opacity=0.5)
                p.dot(s['nx'], s['nz'], r=2.6, fill=col, opacity=0.9, stroke=BG)
            p.base = p.base.replace('../maps/', '../../round3/maps/')  # the shared minimaps live under round3
            fig.add(p)
    fig.save(os.path.join(OUT, 'fig-style-maps'))

# ---------- figure 2: defining numbers
def fig_numbers():
    clans = STYLE_A + MID + STYLE_B + [PN]
    mets = [('flank_lines_pct', 'Smokes from flank-smoke-line ships', '{:.0f}%'), ('parked_cruiser_pct', 'Smokes from parked-cruiser ships', '{:.0f}%'),
            ('stacked_pct', 'Stacked (laid on a teammate)', '{:.0f}%'), ('selfish_pct', 'Selfish (covers only the smoker)', '{:.0f}%'),
            ('stationary_pct', 'Stationary smokes', '{:.0f}%'), ('first_smoke_s', 'First smoke of the game (median, m:ss)', 'time'),
            ('cruiser_dmg_pct', 'Smoke damage dealt by cruisers', '{:.0f}%'), ('smokes_per_game', 'Smokes per game', '{:.1f}')]
    pw, ph, x0, top, rh = 290, 190, 30, 112, 20
    fig = Fig(x0 + 4 * pw + 10, top + 2 * ph + 20, 'The numbers that define each style, clan by clan',
              'All classes. Smokes (games): ' + ', '.join(f"{t} {CLAN[t]['define']['n_smokes']} ({CLAN[t]['define']['n_games']})" for t in clans) + '. PN is small n.')
    fig.legend(30, 74, [('Long smoke, early, for a teammate', BLUE), ('KITE', VIOLET), ('Cruiser smoke, selfish, stationary', ORANGE), ('PN (small n)', AQUA)])
    for i, (k, lab, fmt) in enumerate(mets):
        x, y = x0 + (i % 4) * pw, top + (i // 4) * ph
        fig.add(T(x, y, lab, size=12.5, fill=INK, anchor='start', weight='600'))
        vals = {t: CLAN[t]['define'][k] for t in clans}; vmax = max(vals.values()) or 1
        for j, t in enumerate(clans):
            yy = y + 12 + j * rh + (6 if j >= 3 else 0) + (6 if j >= 4 else 0) + (6 if j >= 6 else 0)
            v = vals[t]; bw = max(1, (pw - 135) * v / vmax)
            fig.add(T(x + 48, yy + 13, t, size=11, fill=INK, anchor='end'))
            fig.add(f'<rect x="{x + 54}" y="{yy + 3}" width="{bw:.1f}" height="13" rx="2" fill="{STYLE_COLOR[style_of(t)]}"/>')
            fig.add(T(x + 54 + bw + 5, yy + 13.5, mmss(v) if fmt == 'time' else fmt.format(v), size=10.5, fill=INK, anchor='start'))
    fig.save(os.path.join(OUT, 'fig-style-numbers'))

fig_maps(); fig_numbers()

# ---------- json
def rnd(o):
    if isinstance(o, float): return round(o, 2)
    if isinstance(o, dict): return {str(k): rnd(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [rnd(v) for v in o]
    return o
J = dict(batch=BATCH_NAME, scope='all classes', transform='own spawn at the bottom; north-spawn teams mirrored north-south (the 4 main maps all spawn north and south)',
         grouping=dict(confirmed=True, note='H-SR, RESIN, BONKZ and HTDOG, VRTUS hold as two ends of one scale. KITE is not midway: by the 9-number distance it sits nearer the long-smoke style '
                       '(destroyer smoke only, no parked cruiser smoke), with a selfish share closer to the cruiser-smoke style. BONKZ is the long-smoke clan that leans furthest toward the other end.'),
         styles={'A': dict(name=A_NAME, clans=STYLE_A, **DATA['A']), 'B': dict(name=B_NAME, clans=STYLE_B, **DATA['B']), 'K': dict(name=K_NAME, clans=MID, **DATA['K'])},
         rest=dict(clans=REST, **DATA['rest']), pn=dict(small_n=True, **DATA['PN'], **NEAR[PN]),
         clans={t: dict(style=style_of(t), wins=WL[t][0], losses=WL[t][1], **CLAN[t], **NEAR[t]) for t in CLANS7},
         a_minus_b_intervals_95={k: v for k, v in DIFF.items()}, second_dd_rule=f'an allied destroyer other than the smoker, ahead of the smoke centre (fwd_m > 0) and within {FWD_KM:.0f} km of the smoke, at the moment the smoke was fully laid',
         distance=dict(features=FEATURES, method='each number scaled to mean 0 and spread 1 across the 24 clans with 7+ games; straight-line distance; a clan is compared with the centre of each style (leaving itself out)', pairwise=PAIR),
         maps={m: dict(caption=CAP[m], **MAPD[m]) for m in MAIN_MAPS},
         figures=['fig-style-maps.png', 'fig-style-numbers.png'])
json.dump(rnd(J), open(os.path.join(OUT, 'styles.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---------- markdown
def val(dd, k, fmt): return '-' if dd[k] is None else mmss(dd[k]) if fmt == 'time' else fmt.format(dd[k])
da, db, dk, dr, dp = (DATA[k]['define'] for k in ('A', 'B', 'K', 'rest', 'PN'))
ca, cb, ck, cr, cp = (DATA[k]['cast'] for k in ('A', 'B', 'K', 'rest', 'PN'))
cl = lambda t: CLAN[t]['define']; cc = lambda t: CLAN[t]['cast']
def dci(k, fmt='{:+.0f}'):
    if k == 'first_smoke_s': return ci(DIFF[k], '{:+.0f}') + ' s'
    return ci(DIFF[k], '{:+.1f}' if k.endswith('per_game') else fmt)
hdr = ['', 'Long smoke style', 'H-SR', 'RESIN', 'BONKZ', 'KITE', 'Cruiser smoke style', 'HTDOG', 'VRTUS', 'Gap, long minus cruiser (95%)']
order = [da, cl('H-SR'), cl('RESIN'), cl('BONKZ'), cl('KITE'), db, cl('HTDOG'), cl('VRTUS')]
t1 = [['Smokes (games)'] + [f"{x['n_smokes']} ({x['n_games']})" for x in order] + ['']]
t1 += [[lab] + [val(x, k, fmt) for x in order] + [dci(k)] for k, lab, fmt in DEF_ROWS]
corder = [ca, cc('H-SR'), cc('RESIN'), cc('BONKZ'), cc('KITE'), cb, cc('HTDOG'), cc('VRTUS')]
crow = lambda lab, k, fmt, dk_=None: [lab] + [fmt.format(x[k]) for x in corder] + [dci(dk_) if dk_ else '']
t2 = [crow('Destroyers per game', 'dd_per_game', '{:.1f}', 'dd_per_game'), crow('Ships carrying smoke per game', 'smoke_ships_per_game', '{:.1f}', 'smoke_ships_per_game'),
      crow('Cruisers carrying smoke per game', 'smoke_cruisers_per_game', '{:.1f}', 'smoke_cruisers_per_game'),
      crow('Destroyer smokes (n)', 'n_dd_smokes', '{}'), crow(f'... with a second destroyer forward within {FWD_KM:.0f} km', 'second_dd_fwd_pct', '{:.0f}%', 'second_dd_fwd_pct'),
      ['... same, first 5 minutes only (n)'] + [f"{x['second_dd_fwd_pct_early']:.0f}% ({x['n_dd_smokes_early']})" for x in corder] + [dci('second_dd_fwd_pct_early')],
      crow('... with any other allied destroyer on the map', 'second_dd_alive_pct', '{:.0f}%')]
rest7 = sorted([t for t in CLANS7 if t not in TOP and t != PN], key=lambda t: NEAR[t]['dist_long'] - NEAR[t]['dist_cruiser'])
t3 = [[t, f'{WL[t][0]}-{WL[t][1]}', f"{cl(t)['n_smokes']}", NEAR[t]['nearest'], f"{cl(t)['flank_lines_pct']:.0f}%", f"{cl(t)['parked_cruiser_pct']:.0f}%", f"{cl(t)['moving_exhaust_pct']:.0f}%", f"{cl(t)['selfish_pct']:.0f}%"] for t in rest7]
nn = C(NEAR[t]['nearest'] for t in rest7)
md = f"""# Part D: clan smoke styles

Batch `{BATCH_NAME}` (1,547 smokes, 171 games). All classes unless a line says destroyer. Everything here is association: it describes what clans do and where, not what makes a clan win.

## Conclusions

1. **The two styles hold up, as two ends of one scale.** H-SR, RESIN and BONKZ ({da['n_smokes']} smokes, {da['n_games']} games) lay {da['flank_lines_pct']:.0f}% of their smoke from flank-smoke-line destroyers, {da['stacked_pct']:.0f}% stacked on a teammate, {da['selfish_pct']:.0f}% selfish, {da['stationary_pct']:.0f}% stationary, first smoke at {mmss(da['first_smoke_s'])}. HTDOG and VRTUS ({db['n_smokes']} smokes, {db['n_games']} games) lay {db['parked_cruiser_pct']:.0f}% from parked-smoke cruisers (Svea, Jinan), {db['stacked_pct']:.0f}% stacked, {db['selfish_pct']:.0f}% selfish, {db['stationary_pct']:.0f}% stationary, first smoke at {mmss(db['first_smoke_s'])}. Every one of those gaps has a 95% interval clear of zero.
2. **H-SR is the far end, and KITE is not in the middle.** H-SR: {cl('H-SR')['flank_lines_pct']:.0f}% flank smoke lines, {cl('H-SR')['stacked_pct']:.0f}% stacked, {cl('H-SR')['selfish_pct']:.0f}% selfish, {cl('H-SR')['stationary_pct']:.0f}% stationary, first smoke at {mmss(cl('H-SR')['first_smoke_s'])} (n {cl('H-SR')['n_smokes']}). KITE (n {cl('KITE')['n_smokes']}) measures nearer the long-smoke style: {cl('KITE')['destroyer_smoke_pct']:.0f}% destroyer smoke, no parked cruiser smoke, first smoke at {mmss(cl('KITE')['first_smoke_s'])}. Only its selfish share ({cl('KITE')['selfish_pct']:.0f}%) looks like the cruiser-smoke style. BONKZ is the long-smoke clan that leans furthest the other way ({cl('BONKZ')['parked_cruiser_pct']:.0f}% parked cruiser smoke, {cl('BONKZ')['stationary_pct']:.0f}% stationary).
3. **Both styles bring the same number of destroyers; the difference is cruisers that carry smoke.** Destroyers per game {ca['dd_per_game']:.1f} against {cb['dd_per_game']:.1f}. Cruisers carrying smoke per game {ca['smoke_cruisers_per_game']:.1f} against {cb['smoke_cruisers_per_game']:.1f} (gap {dci('smoke_cruisers_per_game')}). The cruiser-smoke style also smokes more often: {db['smokes_per_game']:.1f} smokes per game against {da['smokes_per_game']:.1f}.
4. **Cruisers do most of the shooting from smoke in both styles; what changes is who lays it.** Cruisers deal {da['cruiser_dmg_pct']:.0f}% of concealed smoke damage in the long-smoke style and {db['cruiser_dmg_pct']:.0f}% in the cruiser-smoke style. The smoker itself deals {da['smoker_own_dmg_pct']:.0f}% against {db['smoker_own_dmg_pct']:.0f}% (gap {dci('smoker_own_dmg_pct')} points). In one style a destroyer lays smoke for a cruiser; in the other the cruiser lays its own.
5. **A second destroyer is forward of the smoke more often in the long-smoke style, but the gap is not settled.** When a destroyer smokes, another allied destroyer is ahead of the smoke and within {FWD_KM:.0f} km in {ca['second_dd_fwd_pct']:.0f}% of cases for the long-smoke style (n {ca['n_dd_smokes']}; H-SR {cc('H-SR')['second_dd_fwd_pct']:.0f}%, n {cc('H-SR')['n_dd_smokes']}), {cb['second_dd_fwd_pct']:.0f}% for the cruiser-smoke style (n {cb['n_dd_smokes']}) and {cr['second_dd_fwd_pct']:.0f}% for the Rest (n {cr['n_dd_smokes']}). Long minus cruiser: {dci('second_dd_fwd_pct')} points; long minus Rest: {ci(DIFF['second_dd_fwd_pct_A_vs_rest'], '{:+.0f}')}. In the first 5 minutes it is {ca['second_dd_fwd_pct_early']:.0f}% (n {ca['n_dd_smokes_early']}) against {cb['second_dd_fwd_pct_early']:.0f}% (n {cb['n_dd_smokes_early']}), gap {dci('second_dd_fwd_pct_early')}.
6. **On the maps, the styles differ more in what they lay than in where.** Both smoke mostly in their own half. The clear location difference is Sleeping Giant (both flanks against west and centre); on Mountain Range the class of the smoker flips; on Land of Fire both use the middle but one parks there. See the captions.

## Style definition (all classes)

{md_table(hdr, t1)}

Rest of the field for scale ({dr['n_smokes']} smokes): {dr['flank_lines_pct']:.0f}% flank smoke lines, {dr['parked_cruiser_pct']:.0f}% parked cruiser, {dr['moving_exhaust_pct']:.0f}% moving exhaust, {dr['stacked_pct']:.0f}% stacked, {dr['selfish_pct']:.0f}% selfish, {dr['stationary_pct']:.0f}% stationary, first smoke {mmss(dr['first_smoke_s'])}, {dr['smokes_per_game']:.1f} smokes per game.

![Defining numbers by clan](fig-style-numbers.png)

## Supporting cast

{md_table(hdr, t2)}

The batch records ship positions only at the moment each smoke was fully laid, so "forward" is one snapshot per smoke. Spotting cannot be attributed from the batch; a second destroyer forward of the smoke is the stand-in for "someone is spotting for it". Forward means toward the enemy spawn relative to the smoke centre. Not every destroyer carries smoke: the long-smoke style runs {ca['dd_without_smoke_per_game']:.1f} destroyers per game without it, the cruiser-smoke style {cb['dd_without_smoke_per_game']:.1f}.

## Where each style smokes (4 main maps)

![Style comparison on 4 maps](fig-style-maps.png)

Own spawn at the bottom; north-spawn teams are mirrored north-south. West, middle and east are thirds of the map width. Gaps are long-smoke minus cruiser-smoke with 95% intervals (games resampled); a star means the interval is clear of zero.

""" + '\n'.join(f'- **{m}.** {CAP[m]}' for m in MAIN_MAPS) + f"""
- KITE has {', '.join(f"{MAPD[m]['K']['n']}" for m in MAIN_MAPS)} smokes on these maps: too few for a map reading; drawn for reference only.

## PN call-out (small n)

PN (3-4, {dp['n_smokes']} smokes in {dp['n_games']} games, {cp['n_dd_smokes']} destroyer) sits nearest the long-smoke style (distance {NEAR[PN]['dist_long']:.1f} against {NEAR[PN]['dist_cruiser']:.1f} to the cruiser-smoke style): {dp['flank_lines_pct']:.0f}% flank smoke lines, {dp['stacked_pct']:.0f}% stacked. It differs from that style by smoking little and late ({dp['smokes_per_game']:.1f} smokes per game, first smoke {mmss(dp['first_smoke_s'])}), by a {dp['selfish_pct']:.0f}% selfish share, and by {dp['moving_exhaust_pct']:.0f}% moving exhaust smoke. With 14 smokes each of these shares moves 7 points per smoke.

## Rest clans with 7 or more games

{md_table(['Clan', 'W-L', 'Smokes', 'Nearest style', 'Flank lines', 'Parked cruiser', 'Moving exhaust', 'Selfish'], t3)}

{nn['long smoke']} sit nearer the long-smoke style, {nn['cruiser smoke']} nearer the cruiser-smoke style, {nn['between']} between (the two distances within 15% of each other). Several Rest clans fit neither style well because they lean on moving exhaust smoke (Italian ships), which neither Top 6 style uses much.

## Method and cautions

- Styles were checked by distance on 9 numbers per clan (4 ship-habit shares, stacked, selfish, stationary, first-smoke time, cruiser share of smoke damage), each scaled across the 24 clans with 7+ games. Distances: HTDOG to VRTUS {PAIR['HTDOG']['VRTUS']}, H-SR to RESIN {PAIR['H-SR']['RESIN']}, RESIN to BONKZ {PAIR['RESIN']['BONKZ']}, RESIN to KITE {PAIR['RESIN']['KITE']}, H-SR to HTDOG {PAIR['H-SR']['HTDOG']}, BONKZ to VRTUS {PAIR['BONKZ']['VRTUS']}, BONKZ to H-SR {PAIR['BONKZ']['H-SR']}.
- Smoke habit is a property of the ship, so the habit shares mostly restate which ships a clan picked. Stacked, selfish and stationary come from the batch's own labels for each smoke.
- Intervals: 95%, 1000 resamples of games within each style (a style has only 2 or 3 clans, so clans cannot be resampled). They show how much the numbers move game to game, not how a different set of clans would look.
- The cruiser-smoke style is 2 clans and {db['n_games']} games. Map rows are thin: {MAPD['Hotspot']['B']['n']} smokes on Hotspot, {MAPD['Mountain Range']['B']['n']} on Mountain Range.
- Clans pick ships per map and per opponent, so some of the map differences are line-up choices on that map, not a fixed habit.
"""
open(os.path.join(OUT, 'STYLES.md'), 'w', encoding='utf-8').write(md)
print(md)
