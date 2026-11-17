# Read-only analysis: how the top 8 clans by win % use smoke versus the rest.
# Run from the repo root:  python -I -X utf8 smoke/analysis/top_clans.py output/20261116-214739
# Reads smokes-enriched.csv and games.csv (inside the data zip). Writes nothing; prints markdown.
import csv, io, sys, zipfile, random, statistics, collections, os

batch = sys.argv[1]
MIN_GAMES, TOP_N, REPS = 7, 8, 4000
random.seed(19)

smokes = list(csv.DictReader(open(os.path.join(batch, 'smokes-enriched.csv'), encoding='utf-8')))
zname = [f for f in os.listdir(batch) if f.endswith('.zip')][0]
with zipfile.ZipFile(os.path.join(batch, zname)) as z:
    games = list(csv.DictReader(io.TextIOWrapper(z.open('games.csv'), encoding='utf-8')))

def secs(c):
    m, s = c.split(':'); return int(m) * 60 + int(s)

# ---- groups
n_g, n_w = collections.Counter(), collections.Counter()
for g in games:
    g['key'] = (g['match_id'], g['game_no'])
    g['tl'] = g['teams'].split(' vs ')
    g['len'] = secs(g['end_elapsed']) if g['end_elapsed'] else None
    for t in g['tl']:
        n_g[t] += 1; n_w[t] += (g['winner'] == t)
elig = sorted([t for t in n_g if n_g[t] >= MIN_GAMES], key=lambda t: -n_w[t] / n_g[t])
TOP = set(elig[:TOP_N])
grp = lambda t: 'top' if t in TOP else 'rest'

# ---- smokes
F = lambda v: float(v) if v not in ('', None) else None
no_clock = 0
for s in smokes:
    s['key'] = (s['match_id'].split('_')[1], s['game_no'])
    c = s['t_activate_clock'] or s['t_created_clock']
    if not s['t_activate_clock']: no_clock += 1
    s['el'] = 1200 - secs(c) if c else None
    s['conc'] = F(s['smoke_damage_concealed']) or 0.0
    s['guns'] = (F(s['damage_shell']) or 0) + (F(s['damage_fire']) or 0) + (F(s['damage_airstrike']) or 0)
    s['dist'] = F(s['avg_contested_cap_dist_m'])
    s['deaths'] = int(s['smoke_deaths'] or 0)
    s['kills'] = int(s['kills_from_smoke'] or 0)
    s['pp'] = s['primary_purpose'] or 'none'
    s['mv'] = s['movement'] or 'unclassified'
gmap = {g['key']: g for g in games}
# two games carry no end time: use the last smoke activation plus one minute (a lower bound)
no_end = [g for g in games if g['len'] is None]
for g in no_end:
    g['len'] = max(s['el'] for s in smokes if s['key'] == g['key'] and s['el'] is not None) + 60
by_tg = collections.defaultdict(list)
for s in smokes:
    by_tg[(s['key'], s['team'])].append(s)
    s['won'] = gmap[s['key']]['winner'] == s['team']
    s['grp'] = grp(s['team'])

# team-game table
TG = []
for g in games:
    for t in g['tl']:
        ss = by_tg.get((g['key'], t), [])
        els = [x['el'] for x in ss if x['el'] is not None]
        TG.append(dict(key=g['key'], team=t, grp=grp(t), won=g['winner'] == t, len=g['len'], map=g['map'],
                       n=len(ss), first=min(els) if els else None, ss=ss,
                       per10=len(ss) / (g['len'] / 600)))

# ---- metric definitions: each returns (numerator, denominator) summed over a list of team-games
def m_tg(field):
    return lambda tgs: (sum(x[field] for x in tgs if x[field] is not None), sum(1 for x in tgs if x[field] is not None))
def m_sm(num, cond=lambda s: True):
    def f(tgs):
        ss = [s for x in tgs for s in x['ss'] if cond(s)]
        return (sum(num(s) for s in ss), len(ss))
    return f
has_d = lambda s: s['dist'] is not None
METRICS = [
    ('Smokes per game', m_tg('n'), 'tg', '{:.2f}'),
    ('Smokes per 10 min played', lambda t: (sum(x['n'] for x in t), sum(x['len'] for x in t) / 600), 'tg', '{:.2f}'),
    ('First smoke, min elapsed (mean)', lambda t: (sum(x['first'] / 60 for x in t if x['first'] is not None), sum(1 for x in t if x['first'] is not None)), 'tg', '{:.2f}'),
    ('Stacked share', m_sm(lambda s: s['coverage'] == 'stacked'), 'pct', '{:.1f}%'),
    ('Screen share', m_sm(lambda s: s['coverage'] == 'screen'), 'pct', '{:.1f}%'),
    ('Selfish share (coverage)', m_sm(lambda s: s['coverage'] == 'selfish'), 'pct', '{:.1f}%'),
    ('Mean distance to contested cap, m', m_sm(lambda s: s['dist'], has_d), 'sm', '{:.0f}'),
    ('Within 1 km of contested cap', m_sm(lambda s: s['dist'] <= 1000, has_d), 'pct', '{:.1f}%'),
    ('Inside contested cap', m_sm(lambda s: s['dist'] < 0, has_d), 'pct', '{:.1f}%'),
    ('Concealed damage per smoke', m_sm(lambda s: s['conc']), 'sm', '{:,.0f}'),
    ('Smokes with any concealed damage', m_sm(lambda s: s['conc'] > 0), 'pct', '{:.1f}%'),
    ('Concealed damage per game', lambda t: (sum(s['conc'] for x in t for s in x['ss']), len(t)), 'tg', '{:,.0f}'),
    ('Smoke deaths per 100 smokes', m_sm(lambda s: 100 * s['deaths']), 'sm', '{:.1f}'),
    ('Kills from smoke per 100 smokes', m_sm(lambda s: 100 * s['kills']), 'sm', '{:.1f}'),
]
for p in ['cap_contest', 'none', 'reposition', 'counter_smoke', 'escape', 'damage', 'cap_control', 'island_dive', 'radar_trap']:
    METRICS.append(('Purpose: ' + p, m_sm(lambda s, p=p: s['pp'] == p), 'pct', '{:.1f}%'))
for p in ['stationary', 'horizontal', 'pushing', 'kiting', 'unclassified']:
    METRICS.append(('Movement: ' + p, m_sm(lambda s, p=p: s['mv'] == p), 'pct', '{:.1f}%'))

def val(f, tgs, kind):
    a, b = f(tgs)
    if not b: return None
    return (100 if kind == 'pct' else 1) * a / b

def by(tgs, k):
    d = collections.defaultdict(list)
    for x in tgs: d[x[k]].append(x)
    return d

def ci(vals):
    vals = sorted(v for v in vals if v is not None)
    if not vals: return (None, None)
    return vals[int(.025 * len(vals))], vals[min(len(vals) - 1, int(.975 * len(vals)))]

def boot_groups(f, kind, tgs):
    """top minus rest, resampling whole clans within each group."""
    cl = by(tgs, 'team')
    tops = [c for c in cl if c in TOP]; rest = [c for c in cl if c not in TOP]
    out = []
    for _ in range(REPS):
        a = [x for c in random.choices(tops, k=len(tops)) for x in cl[c]]
        b = [x for c in random.choices(rest, k=len(rest)) for x in cl[c]]
        va, vb = val(f, a, kind), val(f, b, kind)
        if va is not None and vb is not None: out.append(va - vb)
    return ci(out)

def fmt(v, f):
    return '-' if v is None else f.format(v)
def dfmt(v, f):
    if v is None: return '-'
    s = f.format(abs(v)).replace('%', ' pt')
    return ('+' if v >= 0 else '-') + s

def group_table(tgs, title, withk=True):
    top = [x for x in tgs if x['grp'] == 'top']; rest = [x for x in tgs if x['grp'] == 'rest']
    print(f'\n### {title}\n')
    print(f'Top 8: {len(top)} team-games, {sum(x["n"] for x in top)} smokes. Rest: {len(rest)} team-games, {sum(x["n"] for x in rest)} smokes.\n')
    print('| Metric | Top 8 | Rest | Difference | 95% CI (by clan) | Top clans above rest value |')
    print('|---|---|---|---|---|---|')
    cl = by(top, 'team')
    for name, f, kind, fm in METRICS:
        a, b = val(f, top, kind), val(f, rest, kind)
        if a is None or b is None: continue
        lo, hi = boot_groups(f, kind, tgs)
        k = sum(1 for c in cl if (val(f, cl[c], kind) or 0) > b)
        star = '' if lo is None or lo * hi <= 0 else ' *'
        print(f'| {name} | {fmt(a, fm)} | {fmt(b, fm)} | {dfmt(a - b, fm)}{star} | {dfmt(lo, fm)} to {dfmt(hi, fm)} | {k} of {len(cl)} |')

print('## Groups\n')
print('| Clan | Games | Wins | Win % | Group |\n|---|---|---|---|---|')
for t in sorted(n_g, key=lambda t: (-(n_g[t] >= MIN_GAMES), -n_w[t] / n_g[t])):
    print(f'| {t} | {n_g[t]} | {n_w[t]} | {100 * n_w[t] / n_g[t]:.1f} | {"TOP" if t in TOP else ("rest" if n_g[t] >= MIN_GAMES else "rest (under 7 games)")} |')
print(f'\nSmokes without an activation clock (created clock used): {no_clock}. Games: {len(games)}, with smokes: {len(set(s["key"] for s in smokes))}.')
print('Games without an end time (length estimated):', [(g['match_id'], g['game_no'], g['len']) for g in no_end])
print('Top-vs-top games:', sum(1 for g in games if all(t in TOP for t in g['tl'])),
      '| top-vs-rest:', sum(1 for g in games if sum(t in TOP for t in g['tl']) == 1),
      '| rest-vs-rest:', sum(1 for g in games if not any(t in TOP for t in g['tl'])))
for gname in ('top', 'rest'):
    x = [t for t in TG if t['grp'] == gname]
    print(gname, 'mean game length min', round(statistics.mean(t['len'] for t in x) / 60, 2), 'win%', round(100 * sum(t['won'] for t in x) / len(x), 1),
          'team-games with no smoke', sum(1 for t in x if t['n'] == 0),
          'median first smoke min', round(statistics.median(t['first'] for t in x if t['first'] is not None) / 60, 2),
          'median cap dist', round(statistics.median(s['dist'] for t in x for s in t['ss'] if s['dist'] is not None)),
          'median conc', round(statistics.median(s['conc'] for t in x for s in t['ss'])),
          'DD share of smokes', round(100 * sum(s['smoker_class'] == 'destroyer' for t in x for s in t['ss']) / sum(t['n'] for t in x), 1),
          'owner-flag share', round(100 * sum(s['owner_flag'] == 'true' for t in x for s in t['ss']) / sum(t['n'] for t in x), 1))

group_table(TG, 'Top 8 vs rest, all smokes')
# destroyer-only lens
TGd = [dict(x, ss=[s for s in x['ss'] if s['smoker_class'] == 'destroyer']) for x in TG]
for x in TGd:
    x['n'] = len(x['ss']); els = [s['el'] for s in x['ss'] if s['el'] is not None]; x['first'] = min(els) if els else None
group_table(TGd, 'Top 8 vs rest, destroyer smokes only')

# ---- timing bins
print('\n### Timing: smokes per team-game still running, 2-minute bins\n')
print('| Minutes | Top 8 smokes | Top 8 team-games running | Top 8 rate | Rest smokes | Rest team-games running | Rest rate | Top share of own smokes | Rest share |')
print('|---|---|---|---|---|---|---|---|---|')
tot = {g: sum(x['n'] for x in TG if x['grp'] == g) for g in ('top', 'rest')}
for b in range(10):
    lo, hi = b * 120, b * 120 + 120
    row = [f'{b * 2} to {b * 2 + 2}']; sh = []
    for g in ('top', 'rest'):
        x = [t for t in TG if t['grp'] == g]
        n = sum(1 for t in x for s in t['ss'] if s['el'] is not None and lo <= s['el'] < hi)
        alive = sum(1 for t in x if t['len'] > lo)
        row += [str(n), str(alive), f'{n / alive:.2f}' if alive else '-']
        sh.append(f'{100 * n / tot[g]:.1f}%')
    print('| ' + ' | '.join(row + sh) + ' |')

# ---- winners vs losers within each game
print('\n### Winners vs losers, paired within each game\n')
print('| Metric | Winners | Losers | Mean paired difference | 95% CI (by game) | Games compared | Winner higher |')
print('|---|---|---|---|---|---|---|')
gm = by(TG, 'key')
W = [x for x in TG if x['won']]; L = [x for x in TG if not x['won']]
for name, f, kind, fm in METRICS:
    if name.startswith(('Smokes per 10', 'Concealed damage per game')): pass
    diffs = []
    for k, pair in gm.items():
        w = [x for x in pair if x['won']]; l = [x for x in pair if not x['won']]
        a, b = val(f, w, kind), val(f, l, kind)
        if a is not None and b is not None: diffs.append(a - b)
    if not diffs: continue
    bs = [statistics.mean(random.choices(diffs, k=len(diffs))) for _ in range(REPS)]
    lo, hi = ci(bs); md = statistics.mean(diffs)
    star = ' *' if lo * hi > 0 else ''
    nz = [d for d in diffs if d != 0]
    print(f'| {name} | {fmt(val(f, W, kind), fm)} | {fmt(val(f, L, kind), fm)} | {dfmt(md, fm)}{star} | {dfmt(lo, fm)} to {dfmt(hi, fm)} | {len(diffs)} | {sum(d > 0 for d in diffs)} of {len(nz)} untied |')

# ---- 2 x 2
print('\n### Group by result (pooled)\n')
print('| Metric | Top 8, won | Top 8, lost | Rest, won | Rest, lost |\n|---|---|---|---|---|')
cells = [[x for x in TG if x['grp'] == g and x['won'] == w] for g in ('top', 'rest') for w in (True, False)]
print('| Team-games / smokes | ' + ' | '.join(f'{len(c)} / {sum(x["n"] for x in c)}' for c in cells) + ' |')
for name, f, kind, fm in METRICS[:14]:
    print(f'| {name} | ' + ' | '.join(fmt(val(f, c, kind), fm) for c in cells) + ' |')

# ---- same-game comparison: top clan vs the rest clan it is playing
print('\n### Top-vs-rest games only (same game, same length)\n')
mixed = [k for k, p in gm.items() if sum(x['grp'] == 'top' for x in p) == 1]
print(f'{len(mixed)} games; the top clan won {sum(1 for k in mixed for x in gm[k] if x["grp"] == "top" and x["won"])}.\n')
print('| Metric | Top clan | Opponent | Mean paired difference | 95% CI (by game) | Games compared |\n|---|---|---|---|---|---|')
A = [x for k in mixed for x in gm[k] if x['grp'] == 'top']; B = [x for k in mixed for x in gm[k] if x['grp'] == 'rest']
for name, f, kind, fm in METRICS[:14]:
    diffs = []
    for k in mixed:
        a = val(f, [x for x in gm[k] if x['grp'] == 'top'], kind); b = val(f, [x for x in gm[k] if x['grp'] == 'rest'], kind)
        if a is not None and b is not None: diffs.append(a - b)
    bs = [statistics.mean(random.choices(diffs, k=len(diffs))) for _ in range(REPS)]
    lo, hi = ci(bs)
    star = ' *' if lo * hi > 0 else ''
    print(f'| {name} | {fmt(val(f, A, kind), fm)} | {fmt(val(f, B, kind), fm)} | {dfmt(statistics.mean(diffs), fm)}{star} | {dfmt(lo, fm)} to {dfmt(hi, fm)} | {len(diffs)} |')

# ---- per map
print('\n### Per map: zone and lane, top 8 vs rest\n')
print('| Map | Games | Split | Smokes | Clans | Zone west | Zone center | Zone east | Lane left | Lane center | Lane right |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
mg = collections.Counter(g['map'] for g in games)
big = []
for m in sorted(mg, key=lambda m: -mg[m]):
    if mg[m] < 10: continue
    tg = [x for x in TG if x['map'] == m]
    rows = {}
    for g in ('top', 'rest'):
        ss = [s for x in tg if x['grp'] == g for s in x['ss']]
        rows[g] = ss
        cl = len(set(s['team'] for s in ss))
        cells = [f'{100 * sum(s["zone"] == z for s in ss) / len(ss):.0f}%' for z in ('west', 'center', 'east')] + \
                [f'{100 * sum(s["lane"] == z for s in ss) / len(ss):.0f}%' for z in ('left', 'center', 'right')]
        print(f'| {m if g == "top" else ""} | {mg[m] if g == "top" else ""} | {"Top 8" if g == "top" else "Rest"} | {len(ss)} | {cl} | ' + ' | '.join(cells) + ' |')
    cells = []
    for fld, zs in (('zone', ('west', 'center', 'east')), ('lane', ('left', 'center', 'right'))):
        for z in zs:
            f = m_sm(lambda s, fld=fld, z=z: s[fld] == z)
            d = val(f, [x for x in tg if x['grp'] == 'top'], 'pct') - val(f, [x for x in tg if x['grp'] == 'rest'], 'pct')
            lo, hi = boot_groups(f, 'pct', tg)
            star = '*' if lo * hi > 0 else ''
            cells.append(f'{d:+.0f}{star}')
            big.append((abs(d), m, fld, z, d, lo, hi))
    print(f'| | | Difference, pt | | | ' + ' | '.join(cells) + ' |')
print('\nLargest map differences (pt, clan-bootstrap CI):')
for a, m, fld, z, d, lo, hi in sorted(big, reverse=True)[:8]:
    print(f'- {m}, {fld} {z}: {d:+.1f} ({lo:+.1f} to {hi:+.1f})')

# zone by spawn side sanity + per-map early-game (first 4 min) zone
print('\n### Per map, first 4 minutes only (opening positions)\n')
print('| Map | Split | Smokes | Zone west | Zone center | Zone east | Lane left | Lane center | Lane right |\n|---|---|---|---|---|---|---|---|---|')
for m in sorted(mg, key=lambda m: -mg[m]):
    for g in ('top', 'rest'):
        ss = [s for x in TG if x['map'] == m and x['grp'] == g for s in x['ss'] if s['el'] is not None and s['el'] < 240]
        if not ss: continue
        cells = [f'{100 * sum(s["zone"] == z for s in ss) / len(ss):.0f}%' for z in ('west', 'center', 'east')] + \
                [f'{100 * sum(s["lane"] == z for s in ss) / len(ss):.0f}%' for z in ('left', 'center', 'right')]
        print(f'| {m if g == "top" else ""} | {"Top 8" if g == "top" else "Rest"} | {len(ss)} | ' + ' | '.join(cells) + ' |')
