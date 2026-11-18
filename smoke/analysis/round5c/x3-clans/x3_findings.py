# Round 5c x3: builds FINDINGS-X3.md, CHECK-X3.md and x3_changes.json from the outputs of d1_scores.py, d2_structure.py
# (run on both clocks) and d3_profiles.py, and from round 5b's files (read-only). No batch access; runs in a second.
import sys, os, json, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
R5B = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'round5b')
J = lambda *p: json.load(open(os.path.join(*p), encoding='utf-8'))
N1, N2, NS = J(HERE, 'd1_scores.json'), J(HERE, 'd2_structure.json'), J(HERE, 'clan_styles.json')
NEL = J(HERE, 'd2_structure_el.json')
B1, B2, BS = J(R5B, 'part-d', 'd1_scores.json'), J(R5B, 'part-d', 'd2_structure.json'), J(R5B, 'clan_styles.json')
assert BS == J(R5B, 'part-d', 'clan_styles.json')
TOP = ['H-SR', 'RESIN', 'BONKZ', 'HTDOG', 'KITE', 'VRTUS']
CLANS = list(NS['clans']); SMALL = [t for t in CLANS if NS['clans'][t]['flagged_small']]; CLANS7 = [t for t in CLANS if t not in SMALL]
FOCUS = TOP + ['PN']
LABEL = {s['key']: s['label'] for d in NS['dimensions'] for s in d['scores']}; LABEL.update({s['key']: s['label'] for s in NS['extra_scores']})
OLABEL = {s['key']: s['label'] for d in BS['dimensions'] for s in d['scores']}; OLABEL.update({s['key']: s['label'] for s in BS['extra_scores']})
V, I, PC, GAP, NC = N1['values'], N1['intervals'], N1['percentiles'], N1['gaps'], N1['n_cases']
OV, OI, OPC, OGAP = B1['values'], B1['intervals'], B1['percentiles'], B1['gaps']
NKEY = dict(we_took_n_pct='n_took_n', we_took_c_pct='n_took_c', not_lost_n_pct='n_notlost_n', not_lost_c_pct='n_notlost_c', died_per100='n_died_base',
            died_smoker_per100='n_died_base', caught_per100='n_smokes', caught_smoker_per100='n_smokes')
PER100 = ('died_per100', 'caught_per100', 'died_smoker_per100', 'caught_smoker_per100')
OLD_PER100 = ('deaths_per100',)
BUYS = [s['key'] for s in NS['dimensions'][5]['scores']]
OLD_BUYS = [s['key'] for s in BS['dimensions'][5]['scores']]
DROPPED = [k for k in OLABEL if k not in LABEL]; ADDED = [k for k in LABEL if k not in OLABEL]

def md_table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)
def mmss(v): return f'{int(v) // 60}:{int(v) % 60:02d}'
def fmt(k, v):
    if v is None: return 'too few'
    if k in PER100 or k in OLD_PER100: return f'{v:.1f}'
    if k.endswith('_pg') and k != 'conc_pg': return f'{v:.1f}'
    if k in ('conc_pg', 'conc_per_smoke', 'edge_m'): return f'{v:,.0f}'
    if k == 'first_smoke_s': return mmss(v)
    return f'{v:.0f}'
def fine(k, v):
    """More decimals, for the change tables."""
    if v is None: return 'too few'
    if k == 'first_smoke_s': return f'{v:.1f} s'
    if k.endswith('_pg') and k != 'conc_pg': return f'{v:.2f}'
    if k in ('conc_pg', 'conc_per_smoke', 'edge_m'): return f'{v:,.0f}'
    return f'{v:.1f}'
def pct(k): return '%' if k.endswith('_pct') else ''
def star(t): return ('*' if t in TOP else '') + t + (' (flag)' if t in SMALL else '')
def n_of(t, k): return NC[t][NKEY[k]] if NKEY[k] != 'n_smokes' else V[t]['n_smokes']
def small(n): return ', small n' if 8 <= n < 15 else ''
def cell(t, k, with_n=False):
    if V[t][k] is None: return f'too few (n {n_of(t, k)})' if k in NKEY else 'too few'
    s = f'{fmt(k, V[t][k])} ({fmt(k, I[t][k][0])} to {fmt(k, I[t][k][1])}) p{PC[t][k]:.0f}'
    if with_n: s += f', n {n_of(t, k)}{small(n_of(t, k))}'
    return s
def gapstr(g, f='{:+,.1f}'):
    return f"{f.format(g['lo'])} to {f.format(g['hi'])}" + (' *' if g['clear'] else '')
def lmh(k, vals=None, clans=None):
    vals = vals or V; clans = clans or CLANS7
    xs = sorted((vals[t][k], t) for t in clans if vals[t].get(k) is not None)
    lo, hi = xs[0][0], xs[-1][0]
    names = lambda v: ', '.join(t for x, t in xs if x == v)
    return [f'{fmt(k, lo)}{pct(k)} ({names(lo)})', f'{fmt(k, statistics.median(x for x, _ in xs))}{pct(k)}', f'{fmt(k, hi)}{pct(k)} ({names(hi)})', len(xs)]

out = []; A = out.append
CH = {}   # machine-readable changes -> x3_changes.json
na = N1['n_all']
A('# Round 5c, worker x3: item 8 (D1 to D3, clan styles)\n')
A(f"Batch `{NS['batch']}`: {na['smokes']:,} smokes, 171 games, 30 clans (24 with 7+ games; {', '.join(SMALL)} have 5 or 6 and are flagged). "
  'Everything here is association. Styles describe what clans do; they do not explain winning.\n')
A('What is new against round 5b, in one place:')
A(f"- **Two death scores, side by side.** \"Died\" = a ship the smoke covered (the smoker, or a ship inside or behind it) died between activation and 20 s after the smoke dispersed; each dead ship is counted once. "
  f"\"Caught\" = the batch list of ships that died while the smoke concealed them or just after it cleared around them (round 5's deaths). All smokes: {na['died']} ships died "
  f"({100 * na['died'] / na['died_base']:.1f} per 100) against {na['caught']} caught ({100 * na['caught'] / na['smokes']:.1f} per 100). "
  f"\"Died\" leaves out {na['not_ok']} smokes of the one single-replay game, laid by the team with no replay (clans {', '.join(na['not_ok_clans'])}); they stay in \"caught\".")
A('- **Caps come from the cap timeline**, on one fixed cap per smoke, up to 60 s after the smoke dispersed. "Taken" = the cap changed to the smoking clan (of smokes where it was not already theirs). '
  '"Not lost" = the enemy did not take it (of smokes inside or within 2 km of that cap, where the cap was not the enemy\'s). Both are given for the nearest cap and for the contested cap. '
  'My choice: for the contested-cap "not lost" the 2 km rule is measured to the contested cap.')
A('- **Dropped from every table:** `cap_won`, `cap_def`, `we_took`, `enemy_took` (the round 5 snapshot fields) and the scores built on them: ' + ', '.join(f'`{k}`' for k in DROPPED) + '.')
A('- **Time scores use the replay clock** (`e0`, seconds since battle start at activation), not the HUD clock: first smoke of the game, share after 12:00, share before 5:00.')
A('- Lineup, who, where and movement scores are untouched and identical to round 5b. Clan intervals are 95%, from resampling that clan\'s own games; Top 6 minus Rest intervals resample whole clans; a star means the interval excludes zero. '
  'Rates with fewer than 8 cases read "too few"; 8 to 14 is "small n".\n')

# ====================================================================== D1
A('### D1. Score every clan on the six dimensions ("what it buys" redone)\n')
g = GAP
def gp(k, unit=''):
    return f"{fmt(k, g[k]['top6'])}{unit} against {fmt(k, g[k]['rest'])}{unit} ({gapstr(g[k])})"
clear_deaths = [k for k in PER100 if g[k]['clear']]
capk = ['we_took_n_pct', 'we_took_c_pct', 'not_lost_n_pct', 'not_lost_c_pct']
clear_caps = [k for k in capk + ['caps_taken_pg', 'caps_taken_c_pg'] if g[k]['clear']]
shared_caps = [k for k in capk + ['caps_taken_pg', 'caps_taken_c_pg'] if not g[k]['clear']]
ratio = statistics.median(V[t]['died_per100'] / V[t]['caught_per100'] for t in CLANS7 if V[t]['caught_per100'])
A(f"**Answer:** Done for all 30 clans (six flagged). Top 6 smokes went with fewer deaths on {'both' if len(clear_deaths) == 4 else 'some of the'} death scores "
  f"(died {g['died_per100']['top6']:.1f} against {g['died_per100']['rest']:.1f} per 100 smokes; caught {g['caught_per100']['top6']:.1f} against {g['caught_per100']['rest']:.1f}), "
  f"and from the timeline the Top 6 took the cap more often ({g['we_took_n_pct']['top6']:.0f}% against {g['we_took_n_pct']['rest']:.0f}% on the nearest cap). "
  f"\"Not lost\" is {'clear on the contested cap only' if g['not_lost_c_pct']['clear'] and not g['not_lost_n_pct']['clear'] else 'clear on both caps' if g['not_lost_c_pct']['clear'] else 'clear on the nearest cap only' if g['not_lost_n_pct']['clear'] else 'Shared on both caps'}.\n")
A('**Numbers:** lowest clan, middle clan and highest clan among the 24 with 7+ games (only clans with 8+ cases are ranked).\n')
rows = []
for k in ['first_smoke_s', 'late_pct', 'conc_pg', 'conc_per_smoke'] + list(PER100) + capk + ['caps_taken_pg', 'caps_taken_c_pg']:
    a = lmh(k); rows.append([LABEL[k], a[0], a[1], a[2], a[3]])
A(md_table(['Score', 'Lowest', 'Median', 'Highest', 'Clans ranked'], rows))
A(f"\nThe \"died\" score runs higher than \"caught\" for almost every clan (middle clan: {ratio:.1f} times as high), because it also counts ships that died in the 20 s after the smoke had gone and ships the batch did not list as concealed at death.\n")
A('Deaths per 100 smokes, per clan: value (95% interval), percentile among the 24 clans. High percentile = more deaths.\n')
A(md_table(['Clan', 'Games', 'Smokes', 'Died per 100', 'Caught per 100', 'Smoker died per 100', 'Smoker caught per 100'],
           [[star(t), NS['clans'][t]['games'], V[t]['n_smokes']] + [cell(t, k) for k in PER100] for t in CLANS]))
A('\nCaps from the timeline, per clan: value (95% interval), percentile, n = smokes the rate applies to.\n')
A(md_table(['Clan', 'Nearest cap taken %', 'Contested cap taken %', 'Nearest cap not lost %', 'Contested cap not lost %', 'Nearest caps taken per game', 'Contested caps taken per game'],
           [[star(t)] + [cell(t, k, True) for k in capk] + [cell(t, k) for k in ('caps_taken_pg', 'caps_taken_c_pg')] for t in CLANS]))
A(f"\nSmokes the cap rates apply to, all clans: nearest cap taken {na['took_n']:,}, contested cap taken {na['took_c']:,}, nearest cap not lost {na['notlost_n']}, contested cap not lost {na['notlost_c']} (of {na['smokes']:,}).\n")

A('**Top 6 or Shared:** Top 6 minus Rest on the "what it buys" scores (pooled over each group\'s games; 95% interval, whole clans resampled).\n')
gn = N1['group_n']
rows = []
for k in BUYS + ['caps_taken_pg', 'caps_taken_c_pg', 'died_pg', 'caught_pg']:
    nn = f"{gn['top6'][NKEY[k]]} / {gn['rest'][NKEY[k]]}" if k in NKEY else f"{gn['top6']['n_games']} / {gn['rest']['n_games']} games"
    x = N1['gaps_bootdiff'].get(k)
    rows.append([LABEL[k], fmt(k, g[k]['top6']), fmt(k, g[k]['rest']), nn, gapstr(g[k], '{:+,.1f}' if not k.endswith('_pg') or k == 'conc_pg' else '{:+,.2f}'),
                 'Top 6' if g[k]['clear'] else 'Shared', (f"{x['lo']:+.1f} to {x['hi']:+.1f}" + (' *' if x['clear'] else '')) if x else '-'])
A(md_table(['Score', 'Top 6', 'Rest', 'n (Top 6 / Rest)', 'Gap (95%)', 'Reading', 'Same gap with the library helper `boot_diff`'], rows))
A('')
A(f"- Deaths: Top 6 {'clearly lower on all four' if len(clear_deaths) == 4 else 'lower, clear on ' + ', '.join(LABEL[k] for k in clear_deaths)}. Died per 100: {gp('died_per100')}. Caught per 100: {gp('caught_per100')}. "
  f"Smoker only: died {gp('died_smoker_per100')}; caught {gp('caught_smoker_per100')}.")
A(f"- Caps taken: nearest cap {gp('we_took_n_pct', '%')}; contested cap {gp('we_took_c_pct', '%')}. Clear: {', '.join(LABEL[k] for k in clear_caps) or 'none'}. Shared: {', '.join(LABEL[k] for k in shared_caps) or 'none'}.")
A(f"- Cap not lost: nearest cap {gp('not_lost_n_pct', '%')}; contested cap {gp('not_lost_c_pct', '%')}.")
A(f"- Concealed damage is unchanged: per smoke {gp('conc_per_smoke')}; per game {gp('conc_pg')}.")
same = [k for k in OGAP if k in GAP and OGAP[k] == GAP[k]]
moved_g = [k for k in OGAP if k in GAP and OGAP[k] != GAP[k]]
A(f"- Every other Top 6 minus Rest gap ({len(same)} scores: lineup, who, where, movement, concealed damage) is identical to round 5b. The gaps that moved are listed under \"Changed from round 5b\".\n")

A('**Clans:** Top 6 and PN on the new scores (value, 95% interval, percentile).\n')
A(md_table(['Clan', 'Died per 100', 'Caught per 100', 'Smoker died per 100', 'Smoker caught per 100', 'Nearest cap taken %', 'Contested cap taken %', 'Nearest cap not lost %', 'Contested cap not lost %'],
           [[star(t)] + [cell(t, k) for k in PER100] + [cell(t, k, True) for k in capk] for t in FOCUS]))
A('')
tf = {k: [f'{t} (n {n_of(t, k)})' for t in CLANS if V[t][k] is None] for k in capk}
A('**Could not be done / proxy:**')
A(f"- Rates with fewer than 8 cases are \"too few\": nearest cap taken: {', '.join(tf['we_took_n_pct']) or 'none'}; contested cap taken: {', '.join(tf['we_took_c_pct']) or 'none'}; "
  f"nearest cap not lost: {', '.join(tf['not_lost_n_pct']) or 'none'}; contested cap not lost: {', '.join(tf['not_lost_c_pct']) or 'none'}.")
A(f"- \"Died\" cannot be judged for {na['not_ok']} smokes ({', '.join(na['not_ok_clans'])}, one game with a single replay); those clans' \"died\" rates use their other smokes.")
A('- A clan interval comes from 7 to 24 games, so it is wide: read a clan\'s death score with its interval, not as a ranking.')
A('- "Caps taken per game" counts each cap once per game when a smoke of the clan stood near it as it changed hands; it is not all caps the clan took.\n')
A('**Verdict:** Keep\n')

A('**Changed from round 5b:**\n')
A('Scores replaced (old score -> new score, why):\n')
A(md_table(['Round 5b score', 'Round 5c score', 'Why'], [
    ['Deaths per 100 smokes (`deaths_per100`)', 'Caught per 100 smokes (same numbers) plus Died per 100 smokes; smoker-only versions of both', 'new death metric'],
    ['Deaths in or behind smoke per game (`deaths_pg`)', 'Ships caught per game (same numbers) plus Ships died per game', 'new death metric'],
    ['Nearest cap taken % (`took_pct`, snapshots)', 'Nearest cap taken % and Contested cap taken % (timeline)', 'cap timeline'],
    ['Nearest cap not lost % (`held_pct`, snapshots)', 'Nearest cap not lost % and Contested cap not lost % (timeline)', 'cap timeline'],
    ['Caps taken next to a smoke per game (`caps_taken_pg`, snapshots)', 'Nearest caps taken with a smoke per game (same key) and Contested caps taken per game (timeline)', 'cap timeline'],
    ['`cap_won_pg`, `cap_def_pg` (batch flags)', 'dropped', 'not to be used'],
    ['First smoke of the game, Smokes after 12:00, Smokes before 5:00 (HUD clock)', 'same scores on the replay clock', 'clock (`e0` instead of `el`)']]))
caught_same = all(abs(V[t]['caught_per100'] - OV[t]['deaths_per100']) < 1e-9 for t in CLANS)
A(f"\nCheck: \"caught per 100\" equals round 5b's deaths per 100 for {'all 30 clans' if caught_same else 'NOT all clans'}, and its Top 6 minus Rest interval is the same ({gapstr(OGAP['deaths_per100'])} then, {gapstr(GAP['caught_per100'])} now).\n")

PAIRS = [('deaths_per100', 'died_per100'), ('deaths_per100', 'caught_per100'), (None, 'died_smoker_per100'), (None, 'caught_smoker_per100'), ('took_pct', 'we_took_n_pct'), (None, 'we_took_c_pct'),
         ('held_pct', 'not_lost_n_pct'), (None, 'not_lost_c_pct'), ('caps_taken_pg', 'caps_taken_pg'), (None, 'caps_taken_c_pg'), ('deaths_pg', 'died_pg'), ('deaths_pg', 'caught_pg'),
         ('first_smoke_s', 'first_smoke_s'), ('late_pct', 'late_pct'), ('early_pct', 'early_pct')]
WHY = dict(died_per100='new death metric', caught_per100='unchanged', died_smoker_per100='new death metric (no round 5b score)', caught_smoker_per100='new split (no round 5b score)',
           we_took_n_pct='cap timeline', we_took_c_pct='cap timeline (no round 5b score)', not_lost_n_pct='cap timeline', not_lost_c_pct='cap timeline (no round 5b score)',
           caps_taken_pg='cap timeline', caps_taken_c_pg='cap timeline (no round 5b score)', died_pg='new death metric', caught_pg='unchanged', first_smoke_s='clock', late_pct='clock', early_pct='clock')
def ochg(t, ok, nk):
    o = OV[t].get(ok) if ok else None; n = V[t][nk]
    op = OPC[t].get(ok) if ok else None; np_ = PC[t][nk]
    if ok is None: return f"new: {fine(nk, n)}" + (f' p{np_:.0f}' if np_ is not None else '')
    same = (o == n) or (o is not None and n is not None and abs(o - n) < 1e-9)
    s = f"{fine(ok, o)}" + (f' p{op:.0f}' if op is not None else '') + ' -> ' + f"{fine(nk, n)}" + (f' p{np_:.0f}' if np_ is not None else '')
    return s + (' (same)' if same and op == np_ else '')
A('Top 6 clans and PN, every per-clan score that was replaced or moved: round 5b value and percentile -> round 5c value and percentile.\n')
A(md_table(['Score (round 5b -> round 5c)'] + [star(t) for t in FOCUS] + ['Why'],
           [[(f'{OLABEL[ok]} -> ' if ok and ok != nk and OLABEL[ok] != LABEL[nk] else '') + LABEL[nk] + (' (snapshots -> timeline)' if ok and ok != nk and OLABEL[ok] == LABEL[nk] else '')] + [ochg(t, ok, nk) for t in FOCUS] + [WHY[nk]] for ok, nk in PAIRS]))
CH['focus_clans'] = {t: {nk: dict(old_key=ok, old=OV[t].get(ok) if ok else None, new=V[t][nk], old_pct=OPC[t].get(ok) if ok else None, new_pct=PC[t][nk]) for ok, nk in PAIRS} for t in FOCUS}
A('\nTop 6 clans and PN, 95% intervals of the same scores (round 5b -> round 5c).\n')
def ichg(t, ok, nk):
    n = I[t].get(nk); o = OI[t].get(ok) if ok else None
    f = lambda k, x: 'too few' if x is None else f'{fine(k, x[0])} to {fine(k, x[1])}'
    return (f'{f(ok, o)} -> ' if ok else 'new: ') + f(nk, n)
A(md_table(['Score'] + [star(t) for t in FOCUS], [[LABEL[nk]] + [ichg(t, ok, nk) for t in FOCUS] for ok, nk in PAIRS]))
others = [t for t in CLANS if t not in FOCUS]
A('\nThe other 23 clans. Replaced scores (round 5b -> round 5c); "died" is new, "caught" is the old deaths number.\n')
A(md_table(['Clan', 'Deaths per 100 -> Died per 100', 'Caught per 100 (was Deaths per 100)', 'Nearest cap taken % (snapshots -> timeline)', 'Nearest cap not lost % (snapshots -> timeline)', 'Caps taken per game (snapshots -> timeline)'],
           [[star(t), f"{fine('deaths_per100', OV[t]['deaths_per100'])} -> {fine('died_per100', V[t]['died_per100'])}", f"{fine('caught_per100', V[t]['caught_per100'])} (same)",
             f"{fine('took_pct', OV[t]['took_pct'])} -> {fine('we_took_n_pct', V[t]['we_took_n_pct'])}", f"{fine('held_pct', OV[t]['held_pct'])} -> {fine('not_lost_n_pct', V[t]['not_lost_n_pct'])}",
             f"{fine('caps_taken_pg', OV[t]['caps_taken_pg'])} -> {fine('caps_taken_pg', V[t]['caps_taken_pg'])}"] for t in others]))
STEP = dict(first_smoke_s=1.0, late_pct=0.5, early_pct=0.5)
tm = []
for k in STEP:
    for t in CLANS:
        d_ = V[t][k] - OV[t][k]
        if abs(d_) > 1e-9: tm.append((k, t, OV[t][k], V[t][k], d_))
CH['time_moves'] = [dict(key=k, clan=t, old=o, new=n) for k, t, o, n, _ in tm]
big = [x for x in tm if x[1] in others and abs(x[4]) > STEP[x[0]]]
fs = [abs(x[4]) for x in tm if x[0] == 'first_smoke_s']
A(f"\nTime scores, what the switch from the HUD clock to the replay clock moved: the first smoke of the game moves for all {len(fs)} clans, by {min(fs):.1f} to {max(fs):.1f} s "
  f"(median {statistics.median(fs):.1f} s; the replay clock is exact and the HUD clock is in whole seconds). "
  f"Share after 12:00 moves for {', '.join(f'{t} ({fine(k, o)}% -> {fine(k, n)}%)' for k, t, o, n, _ in tm if k == 'late_pct') or 'no clan'}. "
  f"Share before 5:00 moves for {', '.join(f'{t} ({fine(k, o)}% -> {fine(k, n)}%)' for k, t, o, n, _ in tm if k == 'early_pct') or 'no clan'}.")
A('Other clans where a time score moved by more than a rounding step (1 s, or half a point): ' +
  ('; '.join(f'{t} {LABEL[k]} {fine(k, o)} -> {fine(k, n)}' for k, t, o, n, _ in big) or 'none') + '.\n')
A('All Top 6 minus Rest gaps, round 5b and round 5c (Top 6 / Rest / 95% interval).\n')
def grow(k, G_, lab):
    x = G_.get(k)
    if x is None: return 'not in this round'
    f = '{:+,.2f}' if (k.endswith('_pg') and k != 'conc_pg') else '{:+,.1f}'
    return f"{fine(k, x['top6'])} / {fine(k, x['rest'])} / {gapstr(x, f)}"
rows = []
for k in list(OLABEL) + ADDED:
    st = 'dropped' if k in DROPPED else 'new' if k in ADDED else 'unchanged' if OGAP[k] == GAP[k] else 'cap timeline' if k == 'caps_taken_pg' else 'clock'
    rows.append([(LABEL.get(k) or OLABEL[k]) + f' (`{k}`)', grow(k, OGAP, OLABEL), grow(k, GAP, LABEL), st])
A(md_table(['Score', 'Round 5b', 'Round 5c', 'Why'], rows))
CH['gaps'] = {k: dict(old=OGAP.get(k), new=GAP.get(k)) for k in list(OLABEL) + ADDED}
A('')

# ====================================================================== D2
A('### D2. Group the clans; one scale or several styles?\n')
keys = N2['keys']; assert keys == B2['keys'] and N2['clans'] == B2['clans']
osc = dict(zip(B2['clans'], B2['scores'])); nsc = dict(zip(N2['clans'], N2['scores']))
for t in SMALL: osc[t] = B2['proj'][t]['pc']; nsc[t] = N2['proj'][t]['pc']
ostyle = {t: BS['clans'][t]['style'] for t in CLANS}; nstyle = {t: NS['clans'][t]['style'] for t in CLANS}
moved = [t for t in CLANS if ostyle[t] != nstyle[t]]
sh1 = max(abs(nsc[t][0] - osc[t][0]) for t in CLANS); sh2 = max(abs(nsc[t][1] - osc[t][1]) for t in CLANS)
w1 = max(CLANS, key=lambda t: abs(nsc[t][0] - osc[t][0])); w2 = max(CLANS, key=lambda t: abs(nsc[t][1] - osc[t][1]))
okeep, nkeep = B2['keep2']['4'], N2['keep2']['4']
obord = sorted(t for t in CLANS7 if okeep[t] < 0.75); nbord = sorted(t for t in CLANS7 if nkeep[t] < 0.75)
el_repro = max(abs(a - b) for x, y in zip(NEL['scores'], B2['scores']) for a, b in zip(x, y))
el_same_groups = NEL['km2']['4'] == B2['km2']['4']
A(f"**Answer:** {'No clan changes style' if not moved else str(len(moved)) + ' clan(s) change style: ' + ', '.join(moved)}. The grouping is built from 17 behaviour scores; only two of them changed at all (first smoke of the game and share after 12:00, now on the replay clock), "
  f"and they moved by at most {max(fs):.1f} s and one or two smokes. Clan positions shift by at most {sh1:.2f} on the first scale and {sh2:.2f} on the second. It is still two separate scales with four soft-bordered corners.\n")
A('**Numbers:**')
A(f"- Scores used: the same 17 as round 5b; no death or cap score is among them, so the new death and cap definitions cannot move the grouping. The two time scores are the only inputs that differ.")
A(f"- Shares of the differences between clans: first scale {100 * N2['shares'][0]:.1f}% (round 5b {100 * B2['shares'][0]:.1f}%), second {100 * N2['shares'][1]:.1f}% ({100 * B2['shares'][1]:.1f}%), "
  f"third {100 * N2['shares'][2]:.1f}% ({100 * B2['shares'][2]:.1f}%). Together the first two carry {100 * sum(N2['shares'][:2]):.0f}%. Shuffled data gives at most {100 * N2['null']['pc1_p95']:.1f}% and {100 * N2['null']['pc2_p95']:.1f}% (95th percentile), so both scales are real.")
A(f"- Check that the rerun is the same method: run on the HUD clock, the script reproduces round 5b's clan positions {'exactly' if el_repro == 0 else f'to within {el_repro:.0e}'} and {'the same four groups' if el_same_groups else 'DIFFERENT groups'}.")
sp = N2['shape']
A(f"- Shape: on the first scale the largest gap between neighbours is {sp['pc1_largest_gap']:.1f} of a range of {sp['pc1_range']:.1f}. On the second there is a break: {len(sp['pc2_low_clans'])} clans sit low "
  f"({', '.join(sp['pc2_low_clans'])}; {sp['pc2_low_max']:+.1f} or below) and everyone else is at {sp['pc2_high_min']:+.1f} or above.")
sil = N2['silhouette']; st_ = NS['structure']['stability']; ost = BS['structure']['stability']
A(f"- Grouping on all 17 scores at once is still a smear: silhouette {sil['2']:.2f} (2 groups), {sil['3']:.2f} (3), {sil['4']:.2f} (4), where 1 would be clean groups. Agreement with the original under resampling of games: "
  f"{st_['ari_games_resampled_k2_median']:.2f} for 2 groups, {st_['ari_games_resampled_k3_median']:.2f} for 3 (round 5b {ost['ari_games_resampled_k2_median']:.2f} and {ost['ari_games_resampled_k3_median']:.2f}). "
  f"Clan positions under resampling correlate {st_['axis1_scores_r_median']:.2f} with the original on the first scale and {st_['axis2_scores_r_median']:.2f} on the second (round 5b {ost['axis1_scores_r_median']:.2f} and {ost['axis2_scores_r_median']:.2f}).")
A(f"- On the two-scale map four corners fit best (silhouette {N2['km2_silhouette']['4']:.2f}); clans keep their corner in {100 * st_['style_kept_share_mean']:.0f}% of resamples on average (round 5b {100 * ost['style_kept_share_mean']:.0f}%).\n")
A('Loadings (link of each score with each scale; round 5b -> round 5c):\n')
ol, nl = BS['structure']['loadings'], NS['structure']['loadings']
A(md_table(['Score', 'First scale (who the smoke is for)', 'Second scale (how much smoke)'],
           [[LABEL[k], f"{ol['pc1'][k]:+.2f} -> {nl['pc1'][k]:+.2f}", f"{ol['pc2'][k]:+.2f} -> {nl['pc2'][k]:+.2f}"] for k in sorted(keys, key=lambda k: -abs(nl['pc1'][k]))]))
lmax = max(max(abs(ol[p][k] - nl[p][k]) for k in keys) for p in ('pc1', 'pc2'))
A(f"\nLargest change in any loading: {lmax:.2f}.\n")
A('Each clan\'s position and style, round 5b and round 5c (first scale: negative = smoke laid for a teammate, positive = ships smoke for themselves; second scale: positive = more smoke).\n')
rows = []
for t in CLANS:
    rows.append([star(t), f'{osc[t][0]:+.2f} -> {nsc[t][0]:+.2f}', f'{osc[t][1]:+.2f} -> {nsc[t][1]:+.2f}', ostyle[t], nstyle[t], 'yes' if t in moved else 'no',
                 'flagged: not used to build the map' if t in SMALL else f'{100 * okeep[t]:.0f}% -> {100 * nkeep[t]:.0f}%' + (' (borderline)' if nkeep[t] < 0.75 else '')])
A(md_table(['Clan', 'First scale', 'Second scale', 'Style, round 5b', 'Style, round 5c', 'Moved', 'Kept its style under resampling'], rows))
CH['styles'] = {t: dict(old=ostyle[t], new=nstyle[t], moved=t in moved, old_axes=osc[t][:2], new_axes=nsc[t][:2], old_kept=okeep.get(t), new_kept=nkeep.get(t)) for t in CLANS}
A(f"\nClans that moved style: {', '.join(moved) or 'none (0 of 30)'}.\n")
A('The four corners:\n')
rows = []
for s in NS['styles']:
    rows.append([f"{s['name']} ({len(s['top6']) + len(s['rest'])} clans, {s['games']} games, {s['smokes']} smokes; W-L {s['wins']}-{s['losses']})", ', '.join(s['top6']) or 'none', ', '.join(s['rest']) or 'none',
                 ', '.join(f'{t} {100 * nkeep[t]:.0f}%' for t in s['borderline']) or 'none', ', '.join(s['flagged_small_would_fall_here']) or 'none'])
A(md_table(['Style', 'Top 6', 'Rest', 'Borderline (kept the style in under 75% of resamples)', 'Flagged clans that would fall here'], rows))
A(f"\nBorderline clans: round 5b {', '.join(f'{t} {100 * okeep[t]:.0f}%' for t in obord) or 'none'}; round 5c {', '.join(f'{t} {100 * nkeep[t]:.0f}%' for t in nbord) or 'none'}. "
  + ('The list is the same.' if obord == nbord else f"Joined: {', '.join(t for t in nbord if t not in obord) or 'none'}. Left: {', '.join(t for t in obord if t not in nbord) or 'none'}. A clan joins or leaves the list when its share crosses 75%; the style itself did not change.") + '\n')
A('What each style looks like (pooled; 95% interval, games resampled within the style; n = smokes the rate applies to):\n')
SHOW = [('long_ships_pg', ''), ('smoke_cruisers_pg', ''), ('smoke_dd_pg', ''), ('smokes_pg', ''), ('first_smoke_s', ''), ('late_pct', ''), ('teammate_pct', ''), ('radar_ca_inside_pct', ''), ('parked_pct', ''), ('inside_cap_pct', '')] + \
       [(k, 'What it buys: ') for k in BUYS + ['caps_taken_pg', 'caps_taken_c_pg']]
def scell(s, k):
    x = s['numbers'][k]
    return f"{fmt(k, x['value'])}{pct(k)} ({fmt(k, x['interval'][0])} to {fmt(k, x['interval'][1])})" + (f", n {x['n']}" if 'n' in x else '')
A(md_table(['Score'] + [s['name'].replace(' of it', '') for s in NS['styles']], [[pre + LABEL[k]] + [scell(s, k) for s in NS['styles']] for k, pre in SHOW]))
sd = {s['id']: s['numbers'] for s in NS['styles']}
lo_d = min(NS['styles'], key=lambda s: s['numbers']['died_per100']['value']); hi_d = max(NS['styles'], key=lambda s: s['numbers']['died_per100']['value'])
lo_c = min(NS['styles'], key=lambda s: s['numbers']['caught_per100']['value']); hi_c = max(NS['styles'], key=lambda s: s['numbers']['caught_per100']['value'])
A('\nPlain reading of the styles with the new outcome scores:')
for s in NS['styles']:
    n_ = s['numbers']
    A(f"- **{s['name']}.** {s['description']} Died {n_['died_per100']['value']:.1f} and caught {n_['caught_per100']['value']:.1f} per 100 smokes (smoker only {n_['died_smoker_per100']['value']:.1f} and {n_['caught_smoker_per100']['value']:.1f}); "
      f"nearest cap taken {n_['we_took_n_pct']['value']:.0f}%, contested cap taken {n_['we_took_c_pct']['value']:.0f}%; nearest cap not lost {n_['not_lost_n_pct']['value']:.0f}%, contested {n_['not_lost_c_pct']['value']:.0f}%; "
      f"concealed damage per smoke {n_['conc_per_smoke']['value']:,.0f}.")
A((f"- On both death scores the fewest deaths per 100 smokes are in \"{lo_d['name']}\" and the most in \"{hi_d['name']}\". " if lo_d is lo_c and hi_d is hi_c else
   f"- The two death scores do not order the styles the same way: fewest in \"{lo_d['name']}\" (died) and \"{lo_c['name']}\" (caught), most in \"{hi_d['name']}\" (died) and \"{hi_c['name']}\" (caught). ") +
  'The two "plenty" styles are close to each other on both; the two "little" styles have few smokes, so their intervals are wide.\n')
ax = NS['structure']['top6_vs_rest_on_axes']; oax = BS['structure']['top6_vs_rest_on_axes']; cc = NS['structure']['top6_concentration']
fa = lambda a: f"Top 6 mean {a['top6']:+.2f}, Rest {a['rest']:+.2f}, gap {a['gap']:+.2f} ({a['lo']:+.2f} to {a['hi']:+.2f}{' *' if a['lo'] * a['hi'] > 0 else ''})"
A('**Top 6 or Shared:**')
A(f"- First scale (who the smoke is for): {'Top 6' if ax['who_axis']['lo'] * ax['who_axis']['hi'] > 0 else 'Shared'}. {fa(ax['who_axis'])}. Round 5b: {fa(oax['who_axis'])}.")
A(f"- Second scale (how much smoke): {'Top 6' if ax['amount_axis']['lo'] * ax['amount_axis']['hi'] > 0 else 'Shared'}. {fa(ax['amount_axis'])}. Round 5b: {fa(oax['amount_axis'])}.")
A(f"- Top 6 in a \"plenty\" style: {cc['in_plenty_styles']} of 6 ({cc['plenty_clans']} of 24 clans are in one; chance of all six at random {100 * cc['chance_all_six']:.0f}%). "
  f"Top 6 in \"Team smoke, plenty of it\": {cc['in_team_plenty']} of 6 (chance of 4 or more at random {100 * cc['chance_4_plus']:.0f}%). Six clans is very few; neither count is settled.")
A('- Outcome scores by style are description only: styles were built without them, and clans in different styles played different maps and opponents.\n')
A('**Clans:** as in the position table and the four-corner table above. Flagged clans are placed on the map but were not used to build it.\n')
orr = N2['outcome_r']
A('**Could not be done / proxy:**')
A('- With 24 clans and 17 scores no method can prove sharp types; the corners have soft borders and the borderline clans can flip under resampling.')
A(f"- How the new outcome scores line up with the two scales (correlation across the 24 clans, description only): died per 100 {orr['died_per100']['pc1']:+.2f} with the first scale and {orr['died_per100']['pc2']:+.2f} with the second; "
  f"caught per 100 {orr['caught_per100']['pc1']:+.2f} and {orr['caught_per100']['pc2']:+.2f}; nearest cap taken {orr['we_took_n_pct']['pc1']:+.2f} and {orr['we_took_n_pct']['pc2']:+.2f}; "
  f"contested cap not lost {orr['not_lost_c_pct']['pc1']:+.2f} and {orr['not_lost_c_pct']['pc2']:+.2f} ({orr['not_lost_c_pct']['n_clans']} clans).\n")
A('**Verdict:** Lead\n')
A('**Changed from round 5b:**\n')
rows = [['First scale share', f"{100 * B2['shares'][0]:.1f}%", f"{100 * N2['shares'][0]:.1f}%", 'clock'], ['Second scale share', f"{100 * B2['shares'][1]:.1f}%", f"{100 * N2['shares'][1]:.1f}%", 'clock'],
        ['Third scale share', f"{100 * B2['shares'][2]:.1f}%", f"{100 * N2['shares'][2]:.1f}%", 'clock'],
        ['Largest change in a loading', '-', f'{lmax:.2f}', 'clock'],
        ['Largest shift of a clan, first scale', '-', f'{sh1:.2f} ({w1})', 'clock'], ['Largest shift of a clan, second scale', '-', f'{sh2:.2f} ({w2})', 'clock'],
        ['Clans that change style', '-', ', '.join(moved) or 'none', 'unchanged' if not moved else 'clock'],
        ['Borderline clans', ', '.join(obord), ', '.join(nbord), 'unchanged' if obord == nbord else 'clock (resampled share crosses 75%)'],
        ['Mean share of resamples in which a clan keeps its style', f"{100 * ost['style_kept_share_mean']:.0f}%", f"{100 * st_['style_kept_share_mean']:.0f}%", 'clock'],
        ['Top 6 minus Rest, first scale', f"{oax['who_axis']['gap']:+.2f} ({oax['who_axis']['lo']:+.2f} to {oax['who_axis']['hi']:+.2f})", f"{ax['who_axis']['gap']:+.2f} ({ax['who_axis']['lo']:+.2f} to {ax['who_axis']['hi']:+.2f})", 'clock'],
        ['Top 6 minus Rest, second scale', f"{oax['amount_axis']['gap']:+.2f} ({oax['amount_axis']['lo']:+.2f} to {oax['amount_axis']['hi']:+.2f})", f"{ax['amount_axis']['gap']:+.2f} ({ax['amount_axis']['lo']:+.2f} to {ax['amount_axis']['hi']:+.2f})", 'clock']]
A(md_table(['Number', 'Round 5b', 'Round 5c', 'Why'], rows))
A('\nStyle outcome rows, round 5b -> round 5c:\n')
osd = {s['id']: s['numbers'] for s in BS['styles']}
def sch(sid, ok, nk):
    o = osd[sid][ok]['value'] if ok else None; n = sd[sid][nk]['value']
    return (f'{fine(ok, o)} -> ' if ok else 'new: ') + fine(nk, n)
SP = [('deaths_per100', 'died_per100', 'new death metric'), ('deaths_per100', 'caught_per100', 'unchanged'), (None, 'died_smoker_per100', 'new death metric'), (None, 'caught_smoker_per100', 'new split'),
      ('took_pct', 'we_took_n_pct', 'cap timeline'), (None, 'we_took_c_pct', 'cap timeline'), ('held_pct', 'not_lost_n_pct', 'cap timeline'), (None, 'not_lost_c_pct', 'cap timeline'),
      ('caps_taken_pg', 'caps_taken_pg', 'cap timeline'), ('first_smoke_s', 'first_smoke_s', 'clock'), ('late_pct', 'late_pct', 'clock')]
A(md_table(['Score'] + [s['name'].replace(' of it', '') for s in NS['styles']] + ['Why'],
           [[(f'{OLABEL[ok]} -> ' if ok and ok != nk and OLABEL[ok] != LABEL[nk] else '') + LABEL[nk] + (' (snapshots -> timeline)' if ok and ok != nk and OLABEL[ok] == LABEL[nk] else '')] + [sch(s['id'], ok, nk) for s in NS['styles']] + [why] for ok, nk, why in SP]))
A('\nThe batch `cap_def` row of the round 5b style table is dropped. Style members, games, smokes and W-L are the same as round 5b'
  + ('.' if all([s['top6'], s['rest']] == [o['top6'], o['rest']] for s, o in zip(NS['styles'], BS['styles'])) else ' EXCEPT where a clan moved (see above).') + '\n')

# ====================================================================== D3
A('### D3. Compact profile per clan for a gauge graphic\n')
gauge_same = [t for t in CLANS if NS['clans'][t]['gauge'] == BS['clans'][t]['gauge']]
struct_same = list(NS) == list(BS) and all(list(NS['clans'][t]) == list(BS['clans'][t]) for t in CLANS)
nkeys = len(NS['clans']['H-SR']['values'])
A(f"**Answer:** The gauge profile is unchanged: one headline number per dimension, its position among the 24 clans, and a 95% range. The six headline numbers are identical to round 5b for {len(gauge_same)} of 30 clans. "
  f"Each clan now also carries the new scores (died and caught per 100, smoker-only versions, caps taken and not lost from the timeline). `clan_styles.json` keeps round 5b's structure, so the file can be swapped in.\n")
A('**Numbers:** headline score per dimension (as round 5) and what "high" means:\n')
A(md_table(['Dimension', 'Headline score', 'High means'], [[d['name'], d['headline_label'], d['direction'].split('high = ')[1]] for d in NS['dimensions']]))
A('\nTwo contrasting clans (value, 95% range, percentile):\n')
def gcell(t, i):
    x = NS['clans'][t]['gauge'][i]; k = x['key']
    return f"{fmt(k, x['value'])}{pct(k)} ({fmt(k, x['interval'][0])} to {fmt(k, x['interval'][1])}), p{x['percentile']:.0f}"
A(md_table(['Dimension', 'H-SR', 'HTDOG'], [[d['name'], gcell('H-SR', i), gcell('HTDOG', i)] for i, d in enumerate(NS['dimensions'])]))
A('\nThe new scores as they sit in the same two profiles (value, 95% range, percentile; for deaths a high percentile is worse):\n')
A(md_table(['Score', 'H-SR', 'HTDOG'], [[LABEL[k], cell('H-SR', k, k in capk), cell('HTDOG', k, k in capk)] for k in list(PER100) + capk + ['caps_taken_pg', 'caps_taken_c_pg']]))
A(f"\nJSON: top-level keys {', '.join('`' + k + '`' for k in NS)}; per clan {', '.join('`' + k + '`' for k in NS['clans']['H-SR'])}. Structure equal to round 5b's file: {'yes' if struct_same else 'NO'}. "
  f"Each clan has {nkeys} scores in `values` (round 5b {len(BS['clans']['H-SR']['values'])}). Added keys: {', '.join('`' + k + '`' for k in ADDED)}. Removed keys: {', '.join('`' + k + '`' for k in DROPPED)}. "
  f"`caps_taken_pg` keeps its key but is now counted from the timeline. `gauge` and `axes` keep their shape; the \"What it buys\" entry in `dimensions` now lists the new score keys. "
  f"Style-level numbers (`styles[].numbers`) carry the same new keys, with `n` for the rates.\n")
A(f"**Top 6 or Shared:** on the six headline numbers the only clear Top 6 gap is still concealed damage per game ({gapstr(GAP['conc_pg'], '{:+,.0f}')}); the other five are Shared: " +
  '; '.join(f"{d['headline_label']} {gapstr(GAP[d['headline']])}" for d in NS['dimensions'] if d['headline'] != 'conc_pg') + '.\n')
A(f"**Clans:** all 30; six flagged ({', '.join(SMALL)}) carry `flagged_small: true` and their percentile is where they would fall among the 24.\n")
A('**Could not be done / proxy:**')
A('- Ranges are wide for clans with few games; a gauge should draw the range, not only the dot.')
A('- Percentiles rank clans against each other; a high percentile is not "good". The four death scores are the ones where high is worse.')
A('- Cap rates are null ("too few") for the clans listed under D1; the design side should show them as missing, not zero.\n')
A('**Verdict:** Keep\n')
A('**Changed from round 5b:**\n')
axch = [(t, BS['clans'][t]['axes'], NS['clans'][t]['axes']) for t in CLANS if BS['clans'][t]['axes'] != NS['clans'][t]['axes']]
A(md_table(['Part of the file', 'Round 5b', 'Round 5c', 'Why'], [
    ['`gauge` (six headline numbers, percentiles, ranges)', '30 clans', f'identical for {len(gauge_same)} of 30 clans', 'unchanged'],
    ['`style`, `style_id`', '30 clans', f"{'identical for all 30 clans' if not moved else 'changed for ' + ', '.join(moved)}", 'unchanged' if not moved else 'clock'],
    ['`axes` (positions and ranges, 2 decimals)', '30 clans', f'{len(axch)} clans differ in some rounded figure; largest position shift {max(sh1, sh2):.2f}', 'clock'],
    ['`values` / `percentiles` / `intervals`', f"{len(BS['clans']['H-SR']['values'])} scores", f'{nkeys} scores: {len(ADDED)} added, {len(DROPPED)} removed, `caps_taken_pg` recounted, three time scores on the replay clock', 'new death metric / cap timeline / clock'],
    ['`style_note`, `style_kept_share`', 'borderline: ' + ', '.join(obord), 'borderline: ' + ', '.join(nbord), 'unchanged' if obord == nbord else 'clock'],
    ['`top6_minus_rest`', f'{len(OGAP)} gaps', f'{len(GAP)} gaps; see the full old and new list under D1', 'new death metric / cap timeline / clock'],
    ['`styles[].numbers`', 'took_pct, held_pct, deaths_per100, cap_def_pg', 'the ten "what it buys" scores and two caps-per-game counts', 'new death metric / cap timeline']]))
A('\nPer-clan numbers that moved are listed in full for the Top 6 and PN, and for the other clans, under D1 "Changed from round 5b". Positions on the two scales for all 30 clans, old and new, are in the D2 table.\n')
A('Top 6 and PN, positions on the two scales as stored in `axes` (round 5b -> round 5c):\n')
A(md_table(['Clan', 'First scale', 'Second scale', 'Style'], [[star(t), f"{BS['clans'][t]['axes']['who_axis']:+.2f} -> {NS['clans'][t]['axes']['who_axis']:+.2f}",
                                                                f"{BS['clans'][t]['axes']['amount_axis']:+.2f} -> {NS['clans'][t]['axes']['amount_axis']:+.2f}", f'{ostyle[t]} -> {nstyle[t]}' if t in moved else f'{nstyle[t]} (same)'] for t in FOCUS]))
A('')
open(os.path.join(HERE, 'FINDINGS-X3.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(CH, open(os.path.join(HERE, 'x3_changes.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ====================================================================== CHECK
c = []; B = c.append
B('# CHECK-X3: where every number in FINDINGS-X3.md comes from\n')
B('Run order, from `round5c/x3-clans/`, each with `python -I -X utf8`: `d1_scores.py`, `d2_structure.py`, `d2_structure.py` again with the environment variable `X3_CLOCK=el` (reproduces round 5b, check only), '
  '`d3_profiles.py`, `x3_findings.py`. `run_all.py` does all five and saves the printed output as `d1_output.txt`, `d2_output.txt`, `d2_output_el.txt`, `d3_output.txt`. '
  '`d_lib.py` holds the score definitions (`feats`), resampling (`boot_clan`), percentiles (`pctile`) and the hand-written PCA and k-means. Seeds are fixed (519, 520, 521, 1000, 1001), so reruns give the same numbers.\n')
B('Sanity checks (computed here from the output files):\n')
anch = N1['group_n']
B(md_table(['Check', 'Result'], [
    ['Smokes, all clans', f"{na['smokes']:,} (anchor 1,547)"],
    ['Destroyer-smoke anchor (194 died, 18.2 per 100, smoker 12.75; 124 caught, 11.55, smoker 6.4)', 'printed by `d1_scores.py` as "anchor destroyer smokes" in `d1_output.txt`'],
    ['Top 6 / Rest smokes and team-games', f"{anch['top6']['n_smokes']} in {anch['top6']['n_games']} / {anch['rest']['n_smokes']} in {anch['rest']['n_games']}"],
    ['"Caught per 100" equals round 5b deaths per 100, all 30 clans', 'yes' if caught_same else 'NO'],
    ['Scores identical to round 5b (every clan, every lineup / who / where / movement / concealed-damage score)',
     'yes' if all(V[t][k] == OV[t][k] for t in CLANS for k in OV[t] if k in V[t] and k not in ('first_smoke_s', 'late_pct', 'early_pct', 'caps_taken_pg')) else 'NO'],
    ['D2 on the HUD clock reproduces round 5b positions', f'largest difference {el_repro:.1e}; same four groups: {"yes" if el_same_groups else "NO"}'],
    ['Top 6 minus Rest gap of each death and cap score, group value equals the library statistic (`died100`, `caught100`, `share_stat`)', 'asserted in `d1_scores.py`; the `boot_diff` intervals are in `d1_scores.json` `gaps_bootdiff`'],
    ['`clan_styles.json` structure equal to round 5b', 'yes' if struct_same else 'NO'],
    ['Gauge identical to round 5b', f'{len(gauge_same)} of 30 clans']]))
B('\n| Number | Script | Where |\n|---|---|---|')
for a, b_, d_ in [
    ('All-smokes totals (ships died, caught, the 9 left-out smokes, smokes each cap rate applies to)', '`d1_scores.py`', '`N_ALL` -> `d1_scores.json` `n_all`'),
    ('Per-clan values: died / caught per 100, smoker versions, caps taken, not lost, caps per game', '`d_lib.py`, `d1_scores.py`', '`feats(clan, strict=True)` -> `V[clan][key]`; `d1_scores.json` `values`; n per rate in `n_cases`'),
    ('Per-clan 95% intervals', '`d1_scores.py`', '`I[clan][key]` from `d_lib.boot_clan` (600 resamples of the clan\'s games); `d1_scores.json` `intervals`'),
    ('Percentiles among the 24 clans', '`d1_scores.py`', '`PC[clan][key]` from `d_lib.pctile`; `d1_scores.json` `percentiles`'),
    ('Lowest / median / highest table', '`x3_findings.py`', '`lmh(key)` over `values` of the 24 clans'),
    ('Top 6 minus Rest on every score', '`d1_scores.py`', '`grp_feats(top)`, `grp_feats(rest)`, `REPS` (500 clan resamples, seed 1000) -> `GAPS`; `d1_scores.json` `gaps`; `clan_styles.json` `top6_minus_rest`'),
    ('Same gaps with the library helper', '`d1_scores.py`', '`XCHECK` from `boot_diff(S, stat)` (seed 1001); `d1_scores.json` `gaps_bootdiff`'),
    ('What the clock switch moved (first smoke, after 12:00, before 5:00)', '`x3_findings.py`', '`tm`: `values` here against `round5b/part-d/d1_scores.json`; `x3_changes.json` `time_moves`'),
    ('Scale shares, loadings, clan positions', '`d2_structure.py`', '`shares`, `vecs`, `scores` from `pca(Z)`; `d2_structure.json` `shares`, `loadings`, `scores`; flagged clans in `proj`'),
    ('Shuffled-data shares', '`d2_structure.py`', '`null1`, `null2` (300 column shuffles); `d2_structure.json` `null`'),
    ('Shape of the two scales (largest gap, low-smoke clans)', '`d2_structure.py`', '`SHAPE` -> `d2_structure.json` `shape`'),
    ('Silhouettes, agreement under resampling, scale steadiness', '`d2_structure.py`', '`SIL`, `aris`, `r1`, `r2`; `d2_structure.json` `silhouette`, `boot`; `clan_styles.json` `structure.stability`'),
    ('Four corners, members, borderline shares', '`d2_structure.py`, `d3_profiles.py`', '`KM2[4]`, `keep[4]` -> `d2_structure.json` `km2`, `keep2`; `d3_tables.md` "Style members"; `clan_styles.json` `styles`'),
    ('Moved: yes / no per clan', '`x3_findings.py`', '`moved`: `clans.<name>.style` here against `round5b/clan_styles.json`; `x3_changes.json` `styles`'),
    ('Style pooled numbers and ranges', '`d3_profiles.py`', '`POOL[i]` from `pool()` (400 game resamples); `d3_tables.md`; `clan_styles.json` `styles[].numbers`'),
    ('Outcome scores against the two scales', '`d2_structure.py`', '`OUTR` -> `d2_structure.json` `outcome_r`'),
    ('Top 6 against Rest on the two scales; chance figures', '`d3_profiles.py`', '`AX`, `p_all`, `p4`; `clan_styles.json` `structure.top6_vs_rest_on_axes`, `top6_concentration`'),
    ('Gauge values for H-SR and HTDOG', '`d3_profiles.py`', '`clan_styles.json` `clans.<name>.gauge`'),
    ('Every "round 5b" number', '`x3_findings.py`', 'read from `round5b/part-d/d1_scores.json`, `round5b/part-d/d2_structure.json`, `round5b/clan_styles.json`')]:
    B(f'| {a} | {b_} | {d_} |')
B('\nHeadline numbers as computed:\n')
B(md_table(['Headline', 'Value'], [
    ['Died per 100, Top 6 / Rest (gap 95%)', f"{g['died_per100']['top6']:.2f} / {g['died_per100']['rest']:.2f} ({gapstr(g['died_per100'], '{:+.2f}')})"],
    ['Caught per 100, Top 6 / Rest', f"{g['caught_per100']['top6']:.2f} / {g['caught_per100']['rest']:.2f} ({gapstr(g['caught_per100'], '{:+.2f}')})"],
    ['Smoker died per 100', f"{g['died_smoker_per100']['top6']:.2f} / {g['died_smoker_per100']['rest']:.2f} ({gapstr(g['died_smoker_per100'], '{:+.2f}')})"],
    ['Smoker caught per 100', f"{g['caught_smoker_per100']['top6']:.2f} / {g['caught_smoker_per100']['rest']:.2f} ({gapstr(g['caught_smoker_per100'], '{:+.2f}')})"],
    ['Nearest cap taken %', f"{g['we_took_n_pct']['top6']:.2f} / {g['we_took_n_pct']['rest']:.2f} ({gapstr(g['we_took_n_pct'], '{:+.2f}')})"],
    ['Contested cap taken %', f"{g['we_took_c_pct']['top6']:.2f} / {g['we_took_c_pct']['rest']:.2f} ({gapstr(g['we_took_c_pct'], '{:+.2f}')})"],
    ['Nearest cap not lost %', f"{g['not_lost_n_pct']['top6']:.2f} / {g['not_lost_n_pct']['rest']:.2f} ({gapstr(g['not_lost_n_pct'], '{:+.2f}')})"],
    ['Contested cap not lost %', f"{g['not_lost_c_pct']['top6']:.2f} / {g['not_lost_c_pct']['rest']:.2f} ({gapstr(g['not_lost_c_pct'], '{:+.2f}')})"],
    ['Scale shares', f"{100 * N2['shares'][0]:.2f}% / {100 * N2['shares'][1]:.2f}% (round 5b {100 * B2['shares'][0]:.2f}% / {100 * B2['shares'][1]:.2f}%)"],
    ['Clans that moved style', ', '.join(moved) or 'none']]))
B('\nNotes:')
B('- `d_lib.py` never reads `cap_won`, `cap_def`, `s[\'we_took\']`, `s[\'enemy_took\']` or `s[\'el\']` in the default run. `s[\'el\']` is read only when `X3_CLOCK=el` is set, to prove the rerun matches round 5b.')
B('- "Not lost" on the contested cap uses the distance to the contested cap (`s[\'edge\'] <= 2000`); on the nearest cap `near_cap_edge_m <= 2000`, as the brief says.')
B('- The Top 6 minus Rest intervals in the tables come from the round 5 method (pooled group value, whole clans resampled, 500 runs). The library helper `boot_diff` (1,000 runs) gives the same reading for every death and cap score; both are shown in D1.')
B('- No library problem found. `r5clib.py` was not edited.')
open(os.path.join(HERE, 'CHECK-X3.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(c) + '\n')
print('wrote FINDINGS-X3.md', len(out), 'blocks; CHECK-X3.md; x3_changes.json | moved:', moved or 'none', '| borderline old', obord, 'new', nbord)
