# A3. Somers vs Gearing deaths within the same group and map. Is the gap ship or team?
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
L = []; P = lambda *a: L.append(' '.join(str(x) for x in a))
J = {}
SO = [s for s in DD if s['ship'] == 'Somers']; GE = [s for s in DD if s['ship'] == 'Gearing']; SG = SO + GE
D100 = per100('deaths'); DS = per100('d_smoker'); DCR = ratio100('d_cr', 'n_cr_in'); CONC = avg('conc'); HS = per100('hurt_smoker')
STATS = [('any death per 100 smokes', D100, 1), ('smoker died per 100 smokes', DS, 1), ('smoker hurt per 100 smokes (est. health)', HS, 1), ('cruiser died per 100 sheltering cruisers', DCR, 1), ('concealed damage per smoke', CONC, 0)]
P('Somers n', len(SO), 'T6/Rest', len(TOPS(SO)), len(RESTS(SO)), '| Gearing n', len(GE), 'T6/Rest', len(TOPS(GE)), len(RESTS(GE)))
P('Somers clans:', clan_counts(SO)); P('Gearing clans:', clan_counts(GE))
J['clans'] = dict(Somers=clan_dict(SO), Gearing=clan_dict(GE))
rows = []
for scope, f in (('all clans', lambda s: True), ('Top 6 only', lambda s: s['grp'] == 'top'), ('Rest only', lambda s: s['grp'] == 'rest')):
    a = [s for s in SO if f(s)]; b = [s for s in GE if f(s)]
    for name, st, d in STATS:
        x = diff2(a, b, st, d); x.update(scope=scope, stat=name); rows.append(x)
P(md_table(['scope', 'stat', 'Somers (n)', 'Gearing (n)', 'Somers - Gearing', 'interval'],
           [[x['scope'], x['stat'], f"{fv(x['a'], '{:,.1f}')} ({x['n_a']})", f"{fv(x['b'], '{:,.1f}')} ({x['n_b']})", fv(x['diff'], '{:+,.1f}'), fci(x, '{:+,.1f}')] for x in rows]))
J['by_group'] = rows
# Top 6 vs Rest within each ship (is it team?)
tr = []
for ship, ss in (('Somers', SO), ('Gearing', GE)):
    for name, st, d in STATS:
        x = gap(ss, st, d); x.update(ship=ship, stat=name); tr.append(x)
P('\nTop 6 vs Rest within each ship')
P(md_table(['ship', 'stat', 'Top 6 (n)', 'Rest (n)', 'T6 - Rest', 'interval'], [[x['ship'], x['stat'], f"{fv(x['top6'], '{:,.1f}')} ({x['n_top6']})", f"{fv(x['rest'], '{:,.1f}')} ({x['n_rest']})", fv(x['diff'], '{:+,.1f}'), fci(x, '{:+,.1f}')] for x in tr]))
J['top6_vs_rest_within_ship'] = tr
# within map
MAPS_ = sorted({s['map'] for s in SG}, key=lambda m: -sum(s['map'] == m for s in SG))
mr = []
for m in MAPS_:
    for scope, f in (('all clans', lambda s: True), ('Top 6 only', lambda s: s['grp'] == 'top'), ('Rest only', lambda s: s['grp'] == 'rest')):
        a = [s for s in SO if s['map'] == m and f(s)]; b = [s for s in GE if s['map'] == m and f(s)]
        x = diff2(a, b, D100); y = diff2(a, b, DS); x.update(map=m, scope=scope, smoker_a=y['a'], smoker_b=y['b'], smoker_diff=y['diff'], smoker_lo=y['lo'], smoker_hi=y['hi'], note=sm(min(len(a), len(b)))); mr.append(x)
P('\nWithin map (any death per 100; smoker died per 100)')
P(md_table(['map', 'scope', 'Somers (n)', 'Gearing (n)', 'diff', 'interval', 'smoker died: Somers / Gearing', 'interval', 'note'],
           [[x['map'], x['scope'], f"{fv(x['a'])} ({x['n_a']})", f"{fv(x['b'])} ({x['n_b']})", fv(x['diff'], '{:+.1f}'), fci(x), f"{fv(x['smoker_a'])} / {fv(x['smoker_b'])}", fci(dict(lo=x['smoker_lo'], hi=x['smoker_hi'])), x['note']] for x in mr]))
J['by_map'] = mr
# standardized: same weight for both ships in each (group, map) stratum where both ships have smokes
def std(ss, key, strat):
    """Directly standardized Somers minus Gearing: per-stratum rates weighted by the stratum's combined n (strata with both ships only)."""
    cells = by(ss, strat); num = den = 0; a_sum = b_sum = 0
    for k, v in cells.items():
        a = [s for s in v if s['ship'] == 'Somers']; b = [s for s in v if s['ship'] == 'Gearing']
        if not a or not b: continue
        w = len(v); ra = 100 * sum(key(s) for s in a) / len(a); rb = 100 * sum(key(s) for s in b) / len(b)
        a_sum += w * ra; b_sum += w * rb; den += w
    return (a_sum / den, b_sum / den, den) if den else None
sr = []
for label, strat in (('group', lambda s: s['grp']), ('map', lambda s: s['map']), ('group and map', lambda s: (s['grp'], s['map'])), ('group, map and score state', lambda s: (s['grp'], s['map'], s['state'])), ('clan', lambda s: s['team'])):
    for name, key in (('any death per 100 smokes', lambda s: s['deaths']), ('smoker died per 100 smokes', lambda s: s['d_smoker'])):
        v = std(SG, key, strat)
        lo, hi = boot_stat(SG, lambda ss: (lambda r: r[0] - r[1] if r else None)(std(ss, key, strat)))
        sr.append(dict(standardized_by=label, stat=name, somers=r1(v[0]), gearing=r1(v[1]), diff=r1(v[0] - v[1]), lo=r1(lo), hi=r1(hi), clear=lo * hi > 0, smokes_used=v[2], of=len(SG)))
P('\nStandardized (both ships given the same mix)')
P(md_table(['same mix of', 'stat', 'Somers', 'Gearing', 'diff', 'interval', 'smokes used'], [[x['standardized_by'], x['stat'], x['somers'], x['gearing'], fv(x['diff'], '{:+.1f}'), fci(x), f"{x['smokes_used']} of {x['of']}"] for x in sr]))
J['standardized'] = sr
# context: what differs between the ships' smokes
P('\nContext')
for name, ss in (('Somers', SO), ('Gearing', GE)):
    P(name, 'behind 50+ %', r1(pct(ss, lambda s: s['state'] == 'behind 50+')), 'radar reached %', r1(pct(ss, lambda s: s['radar_on_us'] > 0)), 'cruiser sheltering %', r1(pct(ss, lambda s: s['n_cr_in'] > 0)), 'radar cruiser inside %', r1(pct(ss, lambda s: s['radar_ca_inside'])),
      'median edge to cap m', round(med(s['edge'] for s in ss)), 'who died', dict(C('smoker' if d['is_smoker'] else d['cls'] for s in ss for d in s['dead'])), 'maps', dict(C(s['map'] for s in ss).most_common()))
ctx = []
for scope, f in (('all', lambda s: True), ('Top 6', lambda s: s['grp'] == 'top'), ('Rest', lambda s: s['grp'] == 'rest')):
    x = diff2([s for s in SO if f(s)], [s for s in GE if f(s)], share(lambda s: s['state'] == 'behind 50+')); x.update(scope=scope, stat='share laid 50+ behind'); ctx.append(x)
P(md_table(['scope', 'stat', 'Somers', 'Gearing', 'diff', 'interval'], [[x['scope'], x['stat'], x['a'], x['b'], x['diff'], fci(x)] for x in ctx])); J['context'] = ctx
# per clan flying both
both = []
for c, v in sorted(by(SG, 'team').items()):
    a = [s for s in v if s['ship'] == 'Somers']; b = [s for s in v if s['ship'] == 'Gearing']
    if len(a) >= MIN_N and len(b) >= MIN_N: both.append(dict(clan=c, group='Top 6' if c in TOP else 'Rest', somers_n=len(a), somers_deaths_per_100=r1(D100(a)), gearing_n=len(b), gearing_deaths_per_100=r1(D100(b))))
P('\nClans with 8+ smokes of each ship'); P(md_table(['clan', 'group', 'Somers n', 'Somers deaths/100', 'Gearing n', 'Gearing deaths/100'], [[x['clan'], x['group'], x['somers_n'], x['somers_deaths_per_100'], x['gearing_n'], x['gearing_deaths_per_100']] for x in both]))
P('clans where Somers lower:', sum(x['somers_deaths_per_100'] < x['gearing_deaths_per_100'] for x in both), 'higher:', sum(x['somers_deaths_per_100'] > x['gearing_deaths_per_100'] for x in both), 'of', len(both))
J['clans_with_both'] = both
P('')
P('Rest Gearing by clan (n, deaths, smoker deaths):', {c: (len(v), sum(s['deaths'] for s in v), sum(s['d_smoker'] for s in v)) for c, v in sorted(by(RESTS(GE), 'team').items(), key=lambda kv: -len(kv[1]))})
P('Rest Somers by clan (n, deaths, smoker deaths):', {c: (len(v), sum(s['deaths'] for s in v), sum(s['d_smoker'] for s in v)) for c, v in sorted(by(RESTS(SO), 'team').items(), key=lambda kv: -len(kv[1]))})
P('Top 6 Gearing by clan:', {c: (len(v), sum(s['deaths'] for s in v), sum(s['d_smoker'] for s in v)) for c, v in by(TOPS(GE), 'team').items()}, '| Top 6 Somers by clan:', {c: (len(v), sum(s['deaths'] for s in v), sum(s['d_smoker'] for s in v)) for c, v in by(TOPS(SO), 'team').items()})
loo = []
for c in sorted({s['team'] for s in RESTS(GE)}):
    v = [s for s in RESTS(GE) if s['team'] != c]; loo.append((c, r1(D100(v))))
P('Rest Gearing deaths per 100 leaving one clan out:', loo)
J['rest_gearing_by_clan'] = {c: dict(n=len(v), deaths=sum(s['deaths'] for s in v), smoker_deaths=sum(s['d_smoker'] for s in v)) for c, v in by(RESTS(GE), 'team').items()}; J['rest_gearing_leave_one_out'] = loo
# figure
fig = Fig(900, 330, 'A3. Somers vs Gearing: deaths per 100 smokes', 'Dark = any ship died in or behind the smoke, light = the smoker itself died. Bars compare the two ships inside the same group. Association only.')
y = 90
for scope in ('all clans', 'Top 6 only', 'Rest only'):
    col = {'all clans': VIOLET, 'Top 6 only': BLUE, 'Rest only': ORANGE}[scope]
    d = next(x for x in rows if x['scope'] == scope and x['stat'].startswith('any death')); k = next(x for x in rows if x['scope'] == scope and x['stat'].startswith('smoker died'))
    fig.add(T(40, y + 14, scope, size=13, fill=INK, anchor='start', weight='600'))
    for i, (ship, v, w, n) in enumerate((('Somers', d['a'], k['a'], d['n_a']), ('Gearing', d['b'], k['b'], d['n_b']))):
        yy = y + 22 + i * 24
        fig.add(T(150, yy + 14, f'{ship} (n {n})', size=11.5, fill=INK, anchor='end'))
        fig.add(f'<rect x="160" y="{yy}" width="{v*25:.1f}" height="10" rx="2" fill="{col}"/>' + T(165 + v * 25, yy + 9, f'{v:.1f}', size=10, anchor='start'))
        fig.add(f'<rect x="160" y="{yy+10}" width="{w*25:.1f}" height="8" rx="2" fill="{col}" opacity="0.4"/>' + T(165 + w * 25, yy + 19, f'{w:.1f}', size=9, anchor='start'))
    fig.add(T(640, y + 44, f"Somers - Gearing: {d['diff']:+.1f} ({fci(d)})", size=11.5, fill=INK, anchor='start'))
    y += 78
fig.save(os.path.join(FIGS, 'a3-somers-vs-gearing'))
out('out-a3', J, '\n'.join(L))
