# Read-only analysis: why top-clan destroyers smoke further from the contested cap.
# Run from the repo root:  python -I -X utf8 smoke/analysis/cap_distance.py output/20261117-122135
# Prints markdown tables; writes SVG charts to smoke/analysis/cap-distance/.
import csv, json, sys, os, random, statistics, collections, math

batch = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap-distance')
os.makedirs(OUT, exist_ok=True)
MIN_GAMES, TOP_N, REPS = 7, 8, 2000
WU = 30.0  # metres per world unit
random.seed(19)
C = collections.Counter

# games
games = {}
gdir = os.path.join(batch, 'games')
for d in sorted(os.listdir(gdir)):
    p = os.path.join(gdir, d, 'game.json')
    if not os.path.exists(p): continue
    g = json.load(open(p, encoding='utf-8'))
    games.setdefault((g['match_id'], g['game_no']), g)
n_g, n_w = C(), C()
for g in games.values():
    for t in g['teams']:
        n_g[t['name']] += 1
        n_w[t['name']] += (g['outcome'].get('win') or {}).get('team') == t['name']
elig = sorted([t for t in n_g if n_g[t] >= MIN_GAMES], key=lambda t: -n_w[t] / n_g[t])
TOP = set(elig[:TOP_N])

# smokes
rows = list(csv.DictReader(open(os.path.join(batch, 'smokes.csv'), encoding='utf-8')))
js = {str(s['smoke_id']): s for s in json.load(open(os.path.join(batch, 'smokes.json'), encoding='utf-8'))}
F = lambda v: float(v) if v not in ('', None) else None
def secs(c):
    m, s = c.split(':'); return int(m) * 60 + int(s)

def cap_owner(state, cap, team):
    for part in state.split():
        k, v = part.split(':', 1)
        if k == cap:
            v = v.rstrip('!')
            return 'neutral' if v == '-' else ('ours' if v == team else 'theirs')
    return 'unknown'

S = []
for r in rows:
    j = js[r['smoke_id']]
    g = games[(r['match_id'], int(r['game_no']))]
    s = dict(r)
    s['grp'] = 'top' if r['team'] in TOP else 'rest'
    s['edge'] = F(r['avg_contested_cap_dist_m'])
    R = F(r['contested_cap_radius_m'])
    s['centre'] = R * (1 - F(r['contested_cap_depth_pct']) / 100)
    s['mrA'] = R > 9000
    rad = F(r['radius'])
    best = best_noA = None
    for cap in g['caps']:
        if cap.get('kind') not in (None, 'Control'): continue
        d = min(math.hypot(p['x'] - cap['position']['x'], p['z'] - cap['position']['z']) for p in j['path'])
        e = (d - rad - cap['radius']) * WU
        if best is None or e < best[0]: best = (e, cap['cap'])
        if cap['radius_m'] < 9000 and (best_noA is None or e < best_noA[0]): best_noA = (e, cap['cap'])
    s['any'], s['any_cap'] = best
    s['any_noA'] = best_noA[0]
    s['any_is_contested'] = best[1] == r['contested_cap_name']
    c = r['t_activate_clock'] or r['t_created_clock']
    el = 1200 - secs(c)
    s['phase'] = '0 to 4' if el < 240 else '4 to 8' if el < 480 else '8 to 12' if el < 720 else '12+'
    ds = int(r['score_ours_act']) - int(r['score_theirs_act'])
    s['score'] = 'ahead (50+)' if ds >= 50 else 'behind (50+)' if ds <= -50 else 'level'
    s['own'] = cap_owner(r['cap_state_act'], r['contested_cap_name'], r['team'])
    s['pp'] = r['primary_purpose'] or 'none'
    s['conc'] = F(r['smoke_damage_concealed']) or 0.0
    s['guns'] = sum(F(r[k]) or 0 for k in ('damage_shell', 'damage_fire', 'damage_airstrike'))
    s['torp'] = F(r.get('damage_torpedo')) or 0.0
    s['deaths'] = int(r['smoke_deaths'] or 0); s['kills'] = int(r['kills_from_smoke'] or 0)
    s['won'] = 1 if r['cap_won'] else 0; s['defd'] = 1 if r['cap_defended'] else 0
    reason = j['classification']['coverage']['reason']
    ally = None
    if r['coverage'] == 'stacked' and '(' in reason:
        ship = reason[reason.rindex('(') + 1:reason.rindex(')')]
        for t in g['teams']:
            for p in t['players']:
                if p['ship'] == ship: ally = p['ship_class']
    s['ally'] = ally or 'unknown'
    S.append(s)

DD_ALL = [s for s in S if s['smoker_class'] == 'destroyer']
DD = [s for s in DD_ALL if not s['mrA']]
ship_n = C(s['ship'] for s in DD)
for s in S: s['shipg'] = s['ship'] if ship_n[s['ship']] >= 15 else 'other'

def q(v, p):
    v = sorted(v); k = (len(v) - 1) * p; f = int(k)
    return v[f] + (v[min(f + 1, len(v) - 1)] - v[f]) * (k - f)
def mean(v): return sum(v) / len(v) if v else None
def med(v): return statistics.median(v) if v else None
def pct(v, f): return 100 * sum(1 for x in v if f(x)) / len(v) if v else None
def n0(x, f='{:,.0f}'): return '-' if x is None else f.format(x)
def sg(x): return '-' if x is None else '{:+,.0f}'.format(x)

def by_clan(ss):
    d = collections.defaultdict(list)
    for s in ss: d[s['team']].append(s)
    return d
def boot(ss, stat, key='edge', reps=REPS):
    """stat(top values) - stat(rest values), resampling whole clans within each group."""
    cl = by_clan(ss)
    tv = {c: [s[key] for s in v] for c, v in cl.items()}
    tops = [c for c in cl if c in TOP]; rest = [c for c in cl if c not in TOP]
    if not tops or not rest: return (None, None)
    out = []
    for _ in range(reps):
        a = [x for c in random.choices(tops, k=len(tops)) for x in tv[c]]
        b = [x for c in random.choices(rest, k=len(rest)) for x in tv[c]]
        out.append(stat(a) - stat(b))
    out.sort()
    return out[int(.025 * len(out))], out[int(.975 * len(out)) - 1]
def ci(lohi): return '-' if lohi[0] is None else f'{lohi[0]:+,.0f} to {lohi[1]:+,.0f}' + (' *' if lohi[0] * lohi[1] > 0 else '')

def dist_row(v):
    if not v: return ['0'] + ['-'] * 7
    return [str(len(v)), n0(mean(v)), n0(q(v, .25)), n0(med(v)), n0(q(v, .75)),
            n0(pct(v, lambda x: x < 0), '{:.0f}%'), n0(pct(v, lambda x: x <= 1000), '{:.0f}%'), n0(pct(v, lambda x: x > 5000), '{:.0f}%')]
DH = '| n | Mean | Q1 | Median | Q3 | Inside | Within 1 km | Beyond 5 km |'
DS = '|---|---|---|---|---|---|---|---|'

def breakdown(title, ss, keyf, order=None, key='edge', minn=1, cis=False):
    print(f'\n### {title}\n')
    print('| Level | Group ' + DH + ' Mean gap (top - rest) |' + (' 95% CI (by clan) |' if cis else ''))
    print('|---|---' + DS + '---|' + ('---|' if cis else ''))
    lv = order or [k for k, _ in C(keyf(s) for s in ss).most_common()]
    for k in lv:
        a = [s[key] for s in ss if keyf(s) == k and s['grp'] == 'top']; b = [s[key] for s in ss if keyf(s) == k and s['grp'] == 'rest']
        if len(a) + len(b) < minn: continue
        gap = sg(mean(a) - mean(b)) if a and b else '-'
        small = ' (small n)' if min(len(a), len(b)) < 15 else ''
        cc = ''
        if cis: cc = ' ' + (ci(boot([s for s in ss if keyf(s) == k], mean, key)) if a and b else '-') + ' |'
        print(f'| {k}{small} | Top 8 | ' + ' | '.join(dist_row(a)) + f' | {gap} |' + cc)
        print(f'| | Rest | ' + ' | '.join(dist_row(b)) + ' | |' + (' |' if cis else ''))

print(f'Batch {batch}: {len(S)} smokes, {len(games)} games. Top 8: {sorted(TOP)}')
print(f'Destroyer smokes: {len(DD_ALL)} (top {sum(s["grp"]=="top" for s in DD_ALL)}, rest {sum(s["grp"]=="rest" for s in DD_ALL)}); tied to Mountain Range cap A: top {sum(s["mrA"] and s["grp"]=="top" for s in DD_ALL)}, rest {sum(s["mrA"] and s["grp"]=="rest" for s in DD_ALL)}; all classes {sum(s["mrA"] for s in S)}')
print('Smokes with no contested cap:', sum(s['edge'] is None for s in S), '| contested reason (DD):', dict(C(s['cap_contested_reason'] for s in DD_ALL)))
print('Nearest cap of any status is the contested cap (DD):', n0(pct(DD_ALL, lambda s: s['any_is_contested']), '{:.1f}%'))
print('Torpedo damage inside concealed? sum(conc+det+unk - total):', round(sum((F(s['smoke_damage_concealed']) or 0) + (F(s['smoke_damage_detected']) or 0) + (F(s['smoke_damage_unknown']) or 0) - (F(s['smoke_damage_total']) or 0) for s in S)),
      '| total - guns - torp:', round(sum((F(s['smoke_damage_total']) or 0) - s['guns'] - s['torp'] for s in S)), '| torp sum', round(sum(s['torp'] for s in S)), '| DD smokes with torp', sum(s['torp'] > 0 for s in DD_ALL))
print('MR cap A smokes by clan (DD):', dict(C(s['team'] for s in DD_ALL if s['mrA'])))

print('\n### Headline gap under each definition (destroyer smokes)\n')
print('| Measure | Smokes | n top / rest | Mean top | Mean rest | Mean gap | 95% CI | Median top | Median rest | Median gap | 95% CI |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for name, key in (('Edge of contested cap (the published field)', 'edge'), ('Centre of contested cap', 'centre'), ('Edge of nearest cap, any status', 'any')):
    for lab, ss in (('all', DD_ALL), ('without Mountain Range cap A', DD)):
        k = key
        if key == 'any' and lab != 'all':
            ss, k = DD_ALL, 'any_noA'; lab = 'cap A ignored as a cap'
        a = [s[k] for s in ss if s['grp'] == 'top']; b = [s[k] for s in ss if s['grp'] == 'rest']
        print(f'| {name} | {lab} | {len(a)} / {len(b)} | {n0(mean(a))} | {n0(mean(b))} | {sg(mean(a)-mean(b))} | {ci(boot(ss, mean, k))} | {n0(med(a))} | {n0(med(b))} | {sg(med(a)-med(b))} | {ci(boot(ss, med, k))} |')

print('\n### Distribution, destroyer smokes, edge of contested cap\n')
print('| Smokes | Group ' + DH); print('|---|---' + DS)
for lab, ss in (('All', DD_ALL), ('Without Mountain Range cap A', DD), ('Mountain Range cap A only', [s for s in DD_ALL if s['mrA']])):
    for g in ('top', 'rest'):
        print(f'| {lab} | {"Top 8" if g == "top" else "Rest"} | ' + ' | '.join(dist_row([s['edge'] for s in ss if s['grp'] == g])) + ' |')

far = [s for s in DD if s['edge'] >= 10000]
print('\n### Far tail: destroyer smokes 10 km or more from the contested cap edge\n')
print('top', sum(s['grp'] == 'top' for s in far), 'of', sum(s['grp'] == 'top' for s in DD), '| rest', sum(s['grp'] == 'rest' for s in far), 'of', sum(s['grp'] == 'rest' for s in DD))
for lab, kf in (('clan', lambda s: s['team']), ('map', lambda s: s['map_display']), ('ship', lambda s: s['ship']), ('purpose', lambda s: s['pp']), ('coverage', lambda s: s['coverage']), ('phase', lambda s: s['phase']), ('cap owner', lambda s: s['own']), ('reason', lambda s: s['cap_contested_reason'])):
    print('-', lab, 'top:', dict(C(kf(s) for s in far if s['grp'] == 'top').most_common()), '| rest:', dict(C(kf(s) for s in far if s['grp'] == 'rest').most_common()))
for g in ('top', 'rest'):
    x = [s for s in far if s['grp'] == g]
    print('-', g, 'far-tail concealed dmg per smoke', n0(mean([s['conc'] for s in x])), 'deaths per 100', n0(100 * mean([s['deaths'] for s in x]), '{:.1f}'), 'kills per 100', n0(100 * mean([s['kills'] for s in x]), '{:.1f}'))
for s in DD: s['cap10'] = min(s['edge'], 10000.0)
near = [s for s in DD if s['edge'] < 10000]
print('- mean gap with distances capped at 10 km:', sg(mean([s['cap10'] for s in DD if s['grp'] == 'top']) - mean([s['cap10'] for s in DD if s['grp'] == 'rest'])), ci(boot(DD, mean, 'cap10')))
print('- mean gap with 10 km+ smokes dropped:', sg(mean([s['edge'] for s in near if s['grp'] == 'top']) - mean([s['edge'] for s in near if s['grp'] == 'rest'])), ci(boot(near, mean)))

print('\nAll tables below: destroyer smokes, Mountain Range cap A smokes excluded, edge of contested cap.')

# 1 ships
ships = [k for k, n in ship_n.most_common() if n >= 15] + ['other']
breakdown('1. By ship', DD, lambda s: s['shipg'], ships, cis=True)
print('\nShip mix (share of group destroyer smokes) and smoke radius:\n\n| Ship | Top 8 | Rest | Smoke radius m | Emission s |\n|---|---|---|---|---|')
nt = sum(s['grp'] == 'top' for s in DD); nr = len(DD) - nt
for k in ships:
    x = [s for s in DD if s['shipg'] == k]
    print(f'| {k} | {100*sum(s["grp"]=="top" for s in x)/nt:.1f}% | {100*sum(s["grp"]=="rest" for s in x)/nr:.1f}% | {n0(med([F(s["radius"])*WU for s in x]))} | {n0(med([F(s["base_emission_s"]) for s in x]))} |')

def decomp(ss, keyf, key='edge'):
    tot = {g: sum(1 for s in ss if s['grp'] == g) for g in ('top', 'rest')}
    if not tot['top'] or not tot['rest']: return None
    cells = collections.defaultdict(lambda: {'top': [], 'rest': []})
    for s in ss: cells[keyf(s)][s['grp']].append(s[key])
    overall = {g: mean([s[key] for s in ss if s['grp'] == g]) for g in ('top', 'rest')}
    pooled = mean([s[key] for s in ss])
    mix = within = 0.0
    for k, c in cells.items():
        pt, pr = len(c['top']) / tot['top'], len(c['rest']) / tot['rest']
        allm = mean(c['top'] + c['rest'])
        mt = mean(c['top']) if c['top'] else allm; mr = mean(c['rest']) if c['rest'] else allm
        mix += (pt - pr) * ((mt + mr) / 2 - pooled)
        within += (pt + pr) / 2 * (mt - mr)
    return overall['top'] - overall['rest'], mix, within
def decomp_ci(ss, keyf, reps=1000):
    cl = by_clan(ss); tops = [c for c in cl if c in TOP]; rest = [c for c in cl if c not in TOP]
    out = []
    for _ in range(reps):
        x = [s for c in random.choices(tops, k=len(tops)) + random.choices(rest, k=len(rest)) for s in cl[c]]
        d = decomp(x, keyf)
        if d: out.append(d)
    res = []
    for i in range(3):
        v = sorted(o[i] for o in out); res.append((v[int(.025 * len(v))], v[int(.975 * len(v)) - 1]))
    return res
print('\nDecomposition of the mean gap (mix = different shares of each level; within = same level, different distance):\n')
print('| Split by | Smokes | Total gap | Mix part | 95% CI | Within part | 95% CI |\n|---|---|---|---|---|---|---|')
for lab, ss, kf in (('ship', DD, lambda s: s['shipg']), ('ship', DD_ALL, lambda s: s['shipg']), ('map', DD, lambda s: s['map_display']), ('ship x map', DD, lambda s: (s['shipg'], s['map_display'])),
                    ('phase', DD, lambda s: s['phase']), ('coverage', DD, lambda s: s['coverage']), ('primary purpose', DD, lambda s: s['pp'])):
    t, m, w = decomp(ss, kf); c = decomp_ci(ss, kf)
    print(f'| {lab} | {"without cap A" if ss is DD else "all"} | {sg(t)} | {sg(m)} | {ci(c[1])} | {sg(w)} | {ci(c[2])} |')

# 2 maps
breakdown('2. By map', DD, lambda s: s['map_display'], cis=True)
breakdown('2b. Mountain Range including cap A smokes', [s for s in DD_ALL if s['map_display'] == 'Mountain Range'], lambda s: 'cap ' + s['contested_cap_name'])
print('\n### 2c. Map x ship (cells with 8+ smokes in both groups)\n')
print('| Map | Ship | n top | n rest | Median top | Median rest | Mean top | Mean rest | Mean gap |\n|---|---|---|---|---|---|---|---|---|')
cells = collections.defaultdict(lambda: {'top': [], 'rest': []})
for s in DD: cells[(s['map_display'], s['shipg'])][s['grp']].append(s['edge'])
pos = tot = 0
for (m, sh), c in sorted(cells.items()):
    if len(c['top']) >= 8 and len(c['rest']) >= 8:
        gap = mean(c['top']) - mean(c['rest']); pos += gap > 0; tot += 1
        print(f'| {m} | {sh} | {len(c["top"])} | {len(c["rest"])} | {n0(med(c["top"]))} | {n0(med(c["rest"]))} | {n0(mean(c["top"]))} | {n0(mean(c["rest"]))} | {sg(gap)} |')
print(f'\nTop 8 further in {pos} of {tot} cells.')

breakdown('3. By phase (minutes elapsed)', DD, lambda s: s['phase'], ['0 to 4', '4 to 8', '8 to 12', '12+'], cis=True)
breakdown('4a. By primary purpose', DD, lambda s: s['pp'], minn=20)
breakdown('4b. By coverage', DD, lambda s: s['coverage'], ['stacked', 'screen', 'selfish'], cis=True)
breakdown('4c. Stacked destroyer smokes by class of the ally they were laid beside', [s for s in DD if s['coverage'] == 'stacked'], lambda s: s['ally'])
print('\nStacked share of destroyer smokes: top', n0(pct([s for s in DD if s['grp']=='top'], lambda s: s['coverage']=='stacked'), '{:.1f}%'), 'rest', n0(pct([s for s in DD if s['grp']=='rest'], lambda s: s['coverage']=='stacked'), '{:.1f}%'))
CR = [s for s in S if s['smoker_class'] == 'cruiser' and not s['mrA']]
breakdown('4d. Cruiser smokes by coverage (for comparison)', CR, lambda s: s['coverage'], ['stacked', 'screen', 'selfish'])
breakdown('5a. By score at activation', DD, lambda s: s['score'], ['ahead (50+)', 'level', 'behind (50+)'], cis=True)
breakdown('5b. By owner of the contested cap at activation', DD, lambda s: s['own'], ['ours', 'neutral', 'theirs'], cis=True)
breakdown('5c. By why the cap counts as contested', DD, lambda s: s['cap_contested_reason'])
breakdown('5d. By result of the game', DD, lambda s: 'won' if (games[(s['match_id'], int(s['game_no']))]['outcome'].get('win') or {}).get('team') == s['team'] else 'lost', ['won', 'lost'])

# 6 clans
print('\n### 6. By clan\n')
print('| Clan | Group | Games ' + DH + ' Top ship |'); print('|---|---|---' + DS + '---|')
cl = by_clan(DD)
for c in sorted(cl, key=lambda c: (c not in TOP, -med([s['edge'] for s in cl[c]]))):
    if c not in TOP and len(cl[c]) < 20: continue
    sh, n = C(s['ship'] for s in cl[c]).most_common(1)[0]
    print(f'| {c} | {"Top 8" if c in TOP else "Rest"} | {n_g[c]} | ' + ' | '.join(dist_row([s['edge'] for s in cl[c]])) + f' | {sh} ({n}) |')
print('\nRest clans with fewer than 20 destroyer smokes are not listed (' + str(sum(1 for c in cl if c not in TOP and len(cl[c]) < 20)) + ' clans).')
rest_meds = [med([s['edge'] for s in cl[c]]) for c in cl if c not in TOP]
restv = [s['edge'] for s in DD if s['grp'] == 'rest']
print(f'Top-8 clans with a median above the rest-of-field median ({n0(med(restv))} m): {sum(med([s["edge"] for s in cl[c]]) > med(restv) for c in TOP)} of 8; above the rest mean ({n0(mean(restv))} m) on their mean: {sum(mean([s["edge"] for s in cl[c]]) > mean(restv) for c in TOP)} of 8')
print('\nLeave one top clan out:\n\n| Left out | n top | Mean gap | 95% CI | Median gap | 95% CI | Mean gap, all smokes incl. cap A |\n|---|---|---|---|---|---|---|')
for c in [None] + sorted(TOP):
    ss = [s for s in DD if s['team'] != c]; sa = [s for s in DD_ALL if s['team'] != c]
    a = [s['edge'] for s in ss if s['grp'] == 'top']
    ga = mean([s['edge'] for s in sa if s['grp'] == 'top']) - mean([s['edge'] for s in sa if s['grp'] == 'rest'])
    print(f'| {c or "(none)"} | {len(a)} | {sg(mean(a)-mean(restv))} | {ci(boot(ss, mean, reps=1000))} | {sg(med(a)-med(restv))} | {ci(boot(ss, med, reps=1000))} | {sg(ga)} |')

# 7 outcomes by distance band
BANDS = [('inside', -1e9, 0), ('0 to 1 km', 0, 1000), ('1 to 3 km', 1000, 3000), ('3 to 5 km', 3000, 5000), ('5 km +', 5000, 1e9)]
band = lambda s: next(b for b, lo, hi in BANDS if lo <= s['edge'] < hi)
def outcome_row(x):
    if not x: return ['0'] + ['-'] * 7
    return [str(len(x)), n0(mean([s['conc'] for s in x])), n0(med([s['conc'] for s in x])), n0(pct(x, lambda s: s['conc'] > 0), '{:.0f}%'),
            n0(100 * mean([s['deaths'] for s in x]), '{:.1f}'), n0(100 * mean([s['kills'] for s in x]), '{:.1f}'),
            n0(pct(x, lambda s: s['won']), '{:.0f}%'), n0(pct(x, lambda s: s['defd']), '{:.0f}%')]
OH = '| n | Concealed dmg per smoke | Median | Any concealed dmg | Deaths per 100 | Kills per 100 | Cap won | Cap defended |'
print('\n### 7a. Outcomes by distance band, all destroyers\n')
print('| Band | Group ' + OH); print('|---|---' + DS)
for b, _, _ in BANDS:
    for g in ('top', 'rest'):
        print(f'| {b if g == "top" else ""} | {"Top 8" if g == "top" else "Rest"} | ' + ' | '.join(outcome_row([s for s in DD if band(s) == b and s['grp'] == g])) + ' |')
print('\n### 7b. Outcomes by distance band within ship (both groups pooled; top / rest concealed damage per smoke in the last columns)\n')
print('| Ship | Band ' + OH + ' Top 8: n, conc. dmg | Rest: n, conc. dmg |'); print('|---|---' + DS + '---|---|')
def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    a, b = rk(x), rk(y); ma, mb = mean(a), mean(b)
    den = math.sqrt(sum((p - ma) ** 2 for p in a) * sum((p - mb) ** 2 for p in b))
    return sum((p - ma) * (q_ - mb) for p, q_ in zip(a, b)) / den if den else 0
rho = []
for sh in ships:
    x = [s for s in DD if s['shipg'] == sh]
    if len(x) < 50: continue
    for b, _, _ in BANDS:
        y = [s for s in x if band(s) == b]
        t = [s for s in y if s['grp'] == 'top']; r_ = [s for s in y if s['grp'] == 'rest']
        print(f'| {sh if b == "inside" else ""} | {b}{" (small n)" if len(y) < 15 else ""} | ' + ' | '.join(outcome_row(y)) + f' | {len(t)}, {n0(mean([s["conc"] for s in t]))} | {len(r_)}, {n0(mean([s["conc"] for s in r_]))} |')
for sh in ships + ['ALL']:
    for g in ('top', 'rest'):
        x = [s for s in DD if (sh == 'ALL' or s['shipg'] == sh) and s['grp'] == g]
        if len(x) >= 15: rho.append((sh, g, len(x), spearman([s['edge'] for s in x], [s['conc'] for s in x]), spearman([s['edge'] for s in x], [s['deaths'] for s in x])))
print('\nRank correlation of distance with concealed damage and with smoke deaths, within ship:\n\n| Ship | Group | n | Distance vs concealed damage | Distance vs smoke deaths |\n|---|---|---|---|---|')
for sh, g, n, a, b in rho: print(f'| {sh} | {"Top 8" if g == "top" else "Rest"} | {n} | {a:+.2f} | {b:+.2f} |')

# 8 model
def solve(A, b):
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n): M[i][i] += 1e-6
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i])); M[i], M[p] = M[p], M[i]
        piv = M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / piv
            if f:
                for c in range(i, n + 1): M[r][c] -= f * M[i][c]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][c] * x[c] for c in range(i + 1, n))) / M[i][i]
    return x
def model(ss, factors, key='edge'):
    levels = []
    for f in factors:
        lv = [k for k, _ in C(f(s) for s in ss).most_common()][1:]
        levels.append(lv)
    def xrow(s):
        r = [1.0, 1.0 if s['grp'] == 'top' else 0.0]
        for f, lv in zip(factors, levels):
            v = f(s); r += [1.0 if v == k else 0.0 for k in lv]
        return r
    p = 2 + sum(len(l) for l in levels)
    per = {}
    for c, x in by_clan(ss).items():
        A = [[0.0] * p for _ in range(p)]; b = [0.0] * p
        for s in x:
            r = xrow(s); nz = [i for i, v in enumerate(r) if v]
            for i in nz:
                b[i] += s[key]
                for j_ in nz: A[i][j_] += 1.0
        per[c] = (A, b)
    def fit(clans):
        A = [[0.0] * p for _ in range(p)]; b = [0.0] * p
        for c in clans:
            a2, b2 = per[c]
            for i in range(p):
                b[i] += b2[i]; ai, a2i = A[i], a2[i]
                for j_ in range(p): ai[j_] += a2i[j_]
        return solve(A, b)[1]
    tops = [c for c in per if c in TOP]; rest = [c for c in per if c not in TOP]
    est = fit(list(per))
    bs = sorted(fit(random.choices(tops, k=len(tops)) + random.choices(rest, k=len(rest))) for _ in range(600))
    return est, bs[int(.025 * len(bs))], bs[int(.975 * len(bs)) - 1], p
fs = {'ship': lambda s: s['shipg'], 'map': lambda s: s['map_display'], 'phase': lambda s: s['phase'], 'purpose': lambda s: s['pp'], 'coverage': lambda s: s['coverage'],
      'cap': lambda s: s['map_display'] + ' ' + s['contested_cap_name']}
specs = [('top clan only (raw gap)', []), ('+ ship', ['ship']), ('+ ship + map', ['ship', 'map']), ('+ ship + map + phase', ['ship', 'map', 'phase']),
         ('+ ship + map + phase + coverage', ['ship', 'map', 'phase', 'coverage']), ('+ ship + map + phase + purpose', ['ship', 'map', 'phase', 'purpose']),
         ('+ ship + map + phase + purpose + coverage', ['ship', 'map', 'phase', 'purpose', 'coverage']), ('+ ship + contested cap (map and letter) + phase', ['ship', 'cap', 'phase'])]
MODEL = {}
for lab, ss in (('without Mountain Range cap A', DD), ('all destroyer smokes', DD_ALL)):
    print(f'\n### 8. Model: distance to contested cap edge, {lab} (n = {len(ss)})\n')
    print('| Model | Terms | Top-clan coefficient, m | 95% CI (by clan) | Share of raw gap kept |\n|---|---|---|---|---|')
    raw = None
    for name, f in specs:
        est, lo, hi, p = model(ss, [fs[k] for k in f])
        raw = raw if raw is not None else est
        MODEL.setdefault(lab, []).append((name, est, lo, hi))
        print(f'| {name} | {p} | {sg(est)} | {ci((lo, hi))} | {100*est/raw:.0f}% |')

# charts
BLUE, ORANGE, INK, MUTED, GRID, BG = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
def svg(name, w, h, body, title, sub):
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Segoe UI, Arial, sans-serif"><rect width="{w}" height="{h}" fill="{BG}"/>'
    head += f'<text x="24" y="32" font-size="18" font-weight="600" fill="{INK}">{title}</text><text x="24" y="52" font-size="12.5" fill="{MUTED}">{sub}</text>'
    open(os.path.join(OUT, name + '.svg'), 'w', encoding='utf-8').write(head + body + '</svg>')
def legend(x, y):
    return (f'<rect x="{x}" y="{y-9}" width="12" height="12" rx="2" fill="{BLUE}"/><text x="{x+17}" y="{y+1}" font-size="12.5" fill="{INK}">Top 8</text>'
            f'<rect x="{x+70}" y="{y-9}" width="12" height="12" rx="2" fill="{ORANGE}"/><text x="{x+87}" y="{y+1}" font-size="12.5" fill="{INK}">Rest of field</text>')
def T(x, y, s, size=11.5, fill=MUTED, anchor='middle', weight='400'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'

# chart 1: distribution in 1 km bins
def chart_dist():
    W, H, L, R_, Tp, B = 860, 430, 60, 24, 84, 60
    edges = [-4000 + 1000 * i for i in range(15)]  # -4..10, last bin open
    labels = [f'{e//1000}' for e in edges]
    sh = {}
    for g in ('top', 'rest'):
        v = [s['edge'] for s in DD if s['grp'] == g]
        sh[g] = [100 * sum(1 for x in v if (lo <= x < lo + 1000) or (lo == edges[-1] and x >= lo) or (lo == edges[0] and x < lo + 1000)) / len(v) for lo in edges]
    ymax = 5 * math.ceil(max(max(sh['top']), max(sh['rest'])) / 5)
    pw = (W - L - R_) / len(edges); y = lambda v: H - B - (H - B - Tp) * v / ymax
    b = legend(L, 72)
    for t in range(0, ymax + 1, 5):
        b += f'<line x1="{L}" x2="{W-R_}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="{GRID}" stroke-width="1"/>' + T(L - 8, y(t) + 4, f'{t}%', anchor='end')
    for i, lo in enumerate(edges):
        x0 = L + i * pw
        for k, (g, col) in enumerate((('top', BLUE), ('rest', ORANGE))):
            bw = pw / 2 - 5; x = x0 + 4 + k * (bw + 2); v = sh[g][i]
            b += f'<rect x="{x:.1f}" y="{y(v):.1f}" width="{bw:.1f}" height="{max(0, H-B-y(v)):.1f}" rx="3" fill="{col}"/>'
        lab = ('under -3' if i == 0 else '10+' if i == len(edges) - 1 else f'{lo//1000} to {lo//1000+1}')
        b += T(x0 + pw / 2, H - B + 18, lab, size=10.5)
    x0 = L + 4 * pw
    b += f'<line x1="{x0:.1f}" x2="{x0:.1f}" y1="{Tp}" y2="{H-B}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 3"/>' + T(x0 - 6, Tp + 10, 'inside the cap', anchor='end') + T(x0 + 6, Tp + 10, 'outside', anchor='start')
    b += T((L + W - R_) / 2, H - 16, 'Distance from smoke edge to contested cap edge, km', size=12)
    a = [s['edge'] for s in DD if s['grp'] == 'top']; r = [s['edge'] for s in DD if s['grp'] == 'rest']
    svg('1-distribution', W, H, b, 'Most smokes sit in the same place; the top 8 add a far tail beyond 10 km',
        f'Share of each group\'s destroyer smokes per 1 km band. Top 8 n = {len(a)}, rest n = {len(r)}. Mountain Range cap A excluded.')
chart_dist()

# chart 2: by ship, quartile bars
def chart_ship(fname, keyf, rowsS, title, sub):
    W, L, R_, Tp, rh = 860, 150, 150, 96, 46
    H = Tp + rh * len(rowsS) + 56
    lo, hi = -3000, 9000; x = lambda v: L + (W - L - R_) * (min(max(v, lo), hi) - lo) / (hi - lo)
    b = legend(L, 72) + T(L + 210, 73, 'bar = middle half of smokes, mark = median', anchor='start')
    for t in range(lo, hi + 1, 1000):
        b += f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="{Tp-6}" y2="{H-50}" stroke="{MUTED if t == 0 else GRID}" stroke-width="1"/>' + T(x(t), H - 34, f'{t//1000}')
    for i, k in enumerate(rowsS):
        y0 = Tp + i * rh
        b += T(L - 12, y0 + rh / 2 + 1, k, size=13, fill=INK, anchor='end')
        notes = []
        for j, (g, col) in enumerate((('top', BLUE), ('rest', ORANGE))):
            v = [s['edge'] for s in DD if keyf(s) == k and s['grp'] == g]
            yy = y0 + 8 + j * 16
            if len(v) >= 5:
                op = '1' if len(v) >= 15 else '0.45'
                b += f'<rect x="{x(q(v,.25)):.1f}" y="{yy}" width="{max(2, x(q(v,.75))-x(q(v,.25))):.1f}" height="12" rx="3" fill="{col}" opacity="{op}"/>'
                b += f'<rect x="{x(med(v))-2:.1f}" y="{yy-3}" width="4" height="18" rx="1" fill="{INK}" stroke="{BG}" stroke-width="1"/>'
            notes.append(f'{len(v)}')
        b += T(W - R_ + 12, y0 + rh / 2 + 1, f'n = {notes[0]} top, {notes[1]} rest', anchor='start')
    b += T((L + W - R_) / 2, H - 12, 'Distance from smoke edge to contested cap edge, km (0 = cap edge; faded bar = under 15 smokes)', size=12)
    svg(fname, W, H, b, title, sub)
chart_ship('2-by-ship', lambda s: s['shipg'], [k for k in ships if k != 'other'], 'Same ship, similar distance: within-ship gaps are small and uncertain', 'Destroyer smokes by ship, top 8 against the rest. Mountain Range cap A excluded.')
chart_ship('3-by-map', lambda s: s['map_display'], [k for k, _ in C(s['map_display'] for s in DD).most_common()], 'The gap sits on two maps: Sleeping Giant and Hotspot', 'Destroyer smokes by map, top 8 against the rest. Mountain Range cap A excluded.')

# chart 3: clan medians
def chart_clan():
    cl = by_clan(DD)
    cs = sorted([c for c in cl if len(cl[c]) >= 20], key=lambda c: med([s['edge'] for s in cl[c]]))
    W, L, R_, Tp, rh = 860, 110, 120, 96, 24
    H = Tp + rh * len(cs) + 56
    lo, hi = -2000, 7000; x = lambda v: L + (W - L - R_) * (min(max(v, lo), hi) - lo) / (hi - lo)
    b = legend(L, 72) + T(L + 210, 73, 'line = middle half of the clan\'s smokes, dot = median', anchor='start')
    for t in range(lo, hi + 1, 1000):
        b += f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="{Tp-6}" y2="{H-50}" stroke="{MUTED if t == 0 else GRID}" stroke-width="1"/>' + T(x(t), H - 34, f'{t//1000}')
    for i, c in enumerate(cs):
        v = [s['edge'] for s in cl[c]]; yy = Tp + i * rh + rh / 2; col = BLUE if c in TOP else ORANGE
        b += T(L - 12, yy + 4, c, size=12.5, fill=INK, anchor='end', weight='600' if c in TOP else '400')
        b += f'<line x1="{x(q(v,.25)):.1f}" x2="{x(q(v,.75)):.1f}" y1="{yy}" y2="{yy}" stroke="{col}" stroke-width="2" opacity="0.55"/>'
        b += f'<circle cx="{x(med(v)):.1f}" cy="{yy}" r="5.5" fill="{col}" stroke="{BG}" stroke-width="2"/>'
        b += T(W - R_ + 12, yy + 4, f'n = {len(v)}', anchor='start')
    b += T((L + W - R_) / 2, H - 12, 'Distance from smoke edge to contested cap edge, km (0 = cap edge)', size=12)
    svg('4-by-clan', W, H, b, 'Clan by clan: the top 8 are spread across the field', 'Destroyer smokes, clans with 20+ smokes, sorted by median. Mountain Range cap A excluded.')
chart_clan()

# chart 4: outcomes by band, two panels
def chart_bands():
    W, H, Tp, B = 860, 400, 100, 56
    panels = [('Concealed damage per smoke', lambda x: mean([s['conc'] for s in x]), 1000, 'k'), ('Smoke deaths per 100 smokes', lambda x: 100 * mean([s['deaths'] for s in x]), 1, '')]
    b = legend(60, 72)
    for pi, (ttl, f, div, unit) in enumerate(panels):
        L = 60 + pi * 410; pw = 360
        vals = {g: [(f([s for s in DD if band(s) == bn and s['grp'] == g]) or 0) / div for bn, _, _ in BANDS] for g in ('top', 'rest')}
        ns = {g: [sum(1 for s in DD if band(s) == bn and s['grp'] == g) for bn, _, _ in BANDS] for g in ('top', 'rest')}
        ymax = 5 * math.ceil(max(max(vals['top']), max(vals['rest'])) / 5)
        y = lambda v: H - B - (H - B - Tp - 16) * v / ymax
        b += T(L, Tp, ttl, size=13, fill=INK, anchor='start', weight='600')
        for t in range(0, ymax + 1, 5):
            b += f'<line x1="{L}" x2="{L+pw}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="{GRID}" stroke-width="1"/>' + T(L - 6, y(t) + 4, f'{t}{unit}', anchor='end')
        bw = pw / len(BANDS)
        for i, (bn, _, _) in enumerate(BANDS):
            for k, (g, col) in enumerate((('top', BLUE), ('rest', ORANGE))):
                w = bw / 2 - 7; xx = L + i * bw + 6 + k * (w + 2); v = vals[g][i]
                b += f'<rect x="{xx:.1f}" y="{y(v):.1f}" width="{w:.1f}" height="{max(0, H-B-y(v)):.1f}" rx="3" fill="{col}"/>'
                b += T(xx + w / 2, y(v) - 4, f'{v:.0f}' if div == 1000 else f'{v:.0f}', size=10.5)
            b += T(L + i * bw + bw / 2, H - B + 16, bn, size=10.5) + T(L + i * bw + bw / 2, H - B + 30, f'n {ns["top"][i]} / {ns["rest"][i]}', size=9.5)
    b += T(W / 2, H - 8, 'Distance band from the contested cap edge (n = top 8 / rest)', size=12)
    svg('5-outcomes-by-band', W, H, b, 'Same distance, better results for the top 8; no band is clearly best', 'Destroyer smokes. Concealed damage in thousands. Mountain Range cap A excluded. Association only.')
chart_bands()

# chart 5: model coefficients
def chart_model():
    m = MODEL['without Mountain Range cap A']
    W, L, R_, Tp, rh = 860, 330, 60, 84, 34
    H = Tp + rh * len(m) + 56
    lo = 500 * math.floor(min(x[2] for x in m) / 500); hi = 500 * math.ceil(max(x[3] for x in m) / 500)
    x = lambda v: L + (W - L - R_) * (v - lo) / (hi - lo)
    b = ''
    for t in range(lo, hi + 1, 500):
        b += f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="{Tp-6}" y2="{H-50}" stroke="{MUTED if t == 0 else GRID}" stroke-width="1"/>' + T(x(t), H - 34, f'{t:+,}' if t else '0')
    for i, (name, est, l, h) in enumerate(m):
        yy = Tp + i * rh + rh / 2
        b += T(L - 12, yy + 4, name, size=12, fill=INK, anchor='end')
        b += f'<line x1="{x(l):.1f}" x2="{x(h):.1f}" y1="{yy}" y2="{yy}" stroke="{BLUE}" stroke-width="2" opacity="0.55"/><circle cx="{x(est):.1f}" cy="{yy}" r="5.5" fill="{BLUE}" stroke="{BG}" stroke-width="2"/>'
        b += T(x(est), yy - 9, f'{est:+,.0f}', size=10.5)
    b += T((L + W - R_) / 2, H - 12, 'Extra distance for a top-8 clan, m (dot = estimate, line = 95% interval by clan)', size=12)
    svg('6-model', W, H, b, 'How much of the gap is left after like-for-like comparison', 'Top-clan coefficient as controls are added. Destroyer smokes, Mountain Range cap A excluded.')
chart_model()
print('\ncharts written to', OUT)
