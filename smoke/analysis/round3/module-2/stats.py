import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2 import *
import io
out = io.StringIO()
def P(*a):
    print(*a); print(*a, file=out)
f1 = lambda x: '-' if x is None else f'{x:,.1f}'
f2 = lambda x: '-' if x is None else f'{x:.2f}'

# ---------- CSV of every early smoke
cols = ['smoke_id', 'team', 'group', 'opponent', 'match_id', 'game_no', 'map', 'spawn_side', 'ship', 'elapsed_s', 'window', 'norm_x', 'norm_z', 'norm_cell', 'norm_cap',
        'cap_edge_m', 'inside_cap', 'mountain_range_A', 'coverage', 'movement', 'primary_purpose', 'partner_type', 'partners', 'main_partner', 'main_partner_class',
        'main_partner_radar', 'main_partner_how', 'main_partner_norm_x', 'main_partner_norm_z', 'concealed_damage', 'kills', 'deaths', 'cap_won', 'cap_defended', 'score_swing', 'team_won_game']
with open(os.path.join(OUT, 'early-smokes.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(cols)
    for s in sorted(E, key=lambda s: (s['map'], s['game'], s['el'])):
        mp = s['mp'] or {}
        w.writerow([s['id'], s['team'], GROUP_LABEL[s['grp']], s['opponent'], s['game'][0], s['game'][1], s['map'], s['side'], s['ship'], s['el'], WIN_LABEL[s['w']],
                    round(s['nx'], 1), round(s['nz'], 1), s['ncell_name'], s['ncap'], round(s['edge']), int(s['inside']), int(s['mrA']), s['coverage'], s['movement'], s['pp'], s['pt'],
                    '; '.join(f"{p['ship']} ({p['cls']}, {'radar' if p['radar'] else 'no radar'}, {p['how']})" for p in s['partners']),
                    mp.get('ship', ''), mp.get('cls', ''), ('yes' if mp.get('radar') else 'no') if mp else '', mp.get('how', ''),
                    '' if mp.get('nx') is None else round(mp['nx'], 1), '' if mp.get('nz') is None else round(mp['nz'], 1),
                    round(s['conc']), s['kills'], s['deaths'], s['cap_won'], s['cap_def'], s['swing'], int(s['win'])])

P('== A. counts')
P('early smokes', len(E), 'top', sum(s['grp'] == 'top' for s in E), 'rest', sum(s['grp'] == 'rest' for s in E), 'games', len({s['game'] for s in E}), 'clans', len({s['team'] for s in E}))
P('share of these ships smokes that are early', f1(100 * len(E) / sum(s['ship'] in SHIPS for s in S)))
for sh in SHIPS:
    e = [s for s in E if s['ship'] == sh]
    P(sh, len(e), 'top', sum(s['grp'] == 'top' for s in e), 'windows', [sum(s['w'] == i for s in e) for i in range(3)], 'stacked%', f1(pct(e, lambda s: s['coverage'] == 'stacked')),
      'radarCA%', f1(pct(e, lambda s: s['pt'] == 'radar cruiser')), 'inside%', f1(pct(e, lambda s: s['inside'])), 'conc', n0(mean(s['conc'] for s in e)))
for g in ('top', 'rest'):
    e = [s for s in E if s['grp'] == g]; P(g, 'windows', [sum(s['w'] == i for s in e) for i in range(3)], 'coverage', dict(C(s['coverage'] for s in e)), 'pt', dict(C(s['pt'] for s in e)))
P('window x coverage', sorted(C((s['w'], s['coverage']) for s in E).items()))
P('window x pp', [(i, C(s['pp'] for s in E if s['w'] == i).most_common(4)) for i in range(3)])
P('window x movement', [(i, C(s['movement'] for s in E if s['w'] == i).most_common(4)) for i in range(3)])

P('\n== B. top minus rest (early smokes of the three ships)')
noA = [s for s in E if not s['mrA']]
tests = [('stacked %', E, lambda v: pct(v, lambda s: s['coverage'] == 'stacked'), f1), ('radar cruiser partner %', E, lambda v: pct(v, lambda s: s['pt'] == 'radar cruiser'), f1),
         ('2+ partners %', E, lambda v: pct(v, lambda s: len(s['partners']) >= 2), f1),
         ('inside cap %', E, lambda v: pct(v, lambda s: s['inside']), f1), ('inside cap % (no MR A)', noA, lambda v: pct(v, lambda s: s['inside']), f1),
         ('median edge m', E, lambda v: med(s['edge'] for s in v), n0), ('median edge m (no MR A)', noA, lambda v: med(s['edge'] for s in v), n0),
         ('mean elapsed s', E, lambda v: mean(s['el'] for s in v), n0), ('in 0-2 window %', E, lambda v: pct(v, lambda s: s['w'] == 0), f1),
         ('mean conc', E, lambda v: mean(s['conc'] for s in v), n0), ('median conc', E, lambda v: med(s['conc'] for s in v), n0),
         ('conc >= 20k %', E, lambda v: pct(v, lambda s: s['conc'] >= 20000), f1),
         ('kills / smoke', E, lambda v: mean(s['kills'] for s in v), f2), ('deaths / smoke', E, lambda v: mean(s['deaths'] for s in v), f2),
         ('cap won %', E, lambda v: pct(v, lambda s: s['cap_won']), f1), ('mean swing', E, lambda v: mean(s['swing'] for s in v), f1)]
for name, ss, st, fm in tests:
    a, b = st([s for s in ss if s['grp'] == 'top']), st([s for s in ss if s['grp'] == 'rest']); lo, hi = boot_diff(ss, st)
    P(f'{name:28s} top {fm(a):>8s} rest {fm(b):>8s} diff {fm(a - b):>8s} CI {fm(lo)} to {fm(hi)}' + (' *' if lo is not None and lo * hi > 0 else ''))
pn = [s for s in E if s['is_pn']]
P('PN early:', len(pn), [(s['ship'], s['map'], s['ncap'], s['ncell_name'], WIN_LABEL[s['w']], s['coverage'], s['pt'], round(s['conc'])) for s in pn])

P('\n== C. pairings')
for g in ('top', 'rest'):
    for sh in SHIPS:
        e = [s for s in E if s['ship'] == sh and s['grp'] == g]
        P(g, sh, len(e), 'main partners:', C(s['mp']['ship'] + ('*' if s['mp']['radar'] else '') for s in e if s['mp']).most_common(6))
for g in ('top', 'rest'):
    e = [s for s in E if s['grp'] == g and s['mp']]
    P(g, 'main partner ship share:', [(k, f1(100 * v / len(e))) for k, v in C(s['mp']['ship'] for s in e).most_common(6)], 'n', len(e))
P('main partner how', dict(C(s['mp']['how'] for s in E if s['mp'])), 'by grp', sorted(C((s['grp'], s['mp']['how']) for s in E if s['mp']).items()))
P('all partners: cls x how', sorted(C((p['cls'], p['how']) for s in E for p in s['partners']).items()))
P('radar x how (cruisers)', sorted(C((p['radar'], p['how']) for s in E for p in s['partners'] if p['cls'] == 'cruiser').items()))
P('any BB partner', sum(any(p['cls'] == 'battleship' for p in s['partners']) for s in E), 'BB ships', C(p['ship'] for s in E for p in s['partners'] if p['cls'] == 'battleship').most_common(6))
# partner geometry: offset from smoke centre along the forward axis, distance from smoke centre, and distance to the contested cap edge
def geom(s, p):
    fx, fz = fwd(s['map']); dx, dz = p['nx'] - s['nx'], p['nz'] - s['nz']
    ahead = (dx * fx + dz * fz) * WU; dist = math.hypot(dx, dz) * WU
    cx, cz, cr = s['capxz']; capedge = (math.hypot(p['nx'] - cx, p['nz'] - cz) - cr) * WU
    return ahead, dist, capedge
for s in E:
    s['geo'] = geom(s, s['mp']) if s['mp'] and s['mp']['nx'] is not None else None
for lab, f in (('all', lambda s: True), ('top', lambda s: s['grp'] == 'top'), ('rest', lambda s: s['grp'] == 'rest'), ('inside', lambda s: s['mp']['how'] == 'inside'), ('behind', lambda s: s['mp']['how'] == 'behind'),
               ('line_of_fire', lambda s: s['mp']['how'] == 'line_of_fire'), ('radar CA', lambda s: s['pt'] == 'radar cruiser'), ('non-radar CA', lambda s: s['pt'] == 'non-radar cruiser')):
    e = [s for s in E if s['geo'] and f(s)]
    if not e: continue
    P(f'{lab:13s} n {len(e):3d} | partner behind smoke centre % {f1(pct(e, lambda s: s["geo"][0] < 0))} | median ahead m {n0(med(s["geo"][0] for s in e))} | median dist m {n0(med(s["geo"][1] for s in e))}'
      f' | partner inside cap % {f1(pct(e, lambda s: s["geo"][2] < 0))} | median partner to cap edge m {n0(med(s["geo"][2] for s in e))}')
e = [s for s in E if s['geo'] and not s['mrA']]
P('partner inside cap % excluding MR A', f1(pct(e, lambda s: s['geo'][2] < 0)), 'n', len(e))
st = lambda v: pct([s for s in v if s['mp']], lambda s: s['mp']['how'] == 'inside')
P('main partner inside %: top', f1(st([s for s in E if s['grp'] == 'top'])), 'rest', f1(st([s for s in E if s['grp'] == 'rest'])), 'diff CI', boot_diff(E, st))

P('\n== D. outcomes by partner type')
OUTS = [('mean conc', lambda v: mean(s['conc'] for s in v), n0), ('median conc', lambda v: med(s['conc'] for s in v), n0), ('kills/smoke', lambda v: mean(s['kills'] for s in v), f2),
        ('deaths/smoke', lambda v: mean(s['deaths'] for s in v), f2), ('cap won %', lambda v: pct(v, lambda s: s['cap_won']), f1), ('cap def %', lambda v: pct(v, lambda s: s['cap_def']), f1),
        ('mean swing', lambda v: mean(s['swing'] for s in v), f1)]
def outcome_block(groups):
    for lab, e in groups:
        if not e: continue
        P(f'{lab:22s} n {len(e):3d} clans {len({s["team"] for s in e}):2d} | ' + ' | '.join(f'{nm} {fm(st(e))} [{fm(boot_stat(e, st)[0])}, {fm(boot_stat(e, st)[1])}]' for nm, st, fm in OUTS))
outcome_block([(t, [s for s in E if s['pt'] == t]) for t in PT_ORDER])
a, b = [s for s in E if s['pt'] == 'radar cruiser'], [s for s in E if s['pt'] == 'non-radar cruiser']
for nm, st, fm in OUTS:
    lo, hi = boot_cmp(a, b, st); P(f'  radar CA minus non-radar CA, {nm}: {fm(st(a) - st(b))} CI {fm(lo)} to {fm(hi)}' + (' *' if lo * hi > 0 else ''))
a, b = [s for s in E if s['pt'] == 'radar cruiser'], [s for s in E if s['pt'] != 'radar cruiser']
for nm, st, fm in OUTS:
    lo, hi = boot_cmp(a, b, st); P(f'  radar CA minus everything else, {nm}: {fm(st(a) - st(b))} CI {fm(lo)} to {fm(hi)}' + (' *' if lo * hi > 0 else ''))
P('-- with / without a battleship among partners')
outcome_block([('has battleship', [s for s in E if any(p['cls'] == 'battleship' for p in s['partners'])]), ('no battleship', [s for s in E if s['partners'] and not any(p['cls'] == 'battleship' for p in s['partners'])])])
P('-- by coverage')
outcome_block([(c, [s for s in E if s['coverage'] == c]) for c in ('stacked', 'screen', 'selfish')])
a, b = [s for s in E if s['coverage'] == 'stacked'], [s for s in E if s['coverage'] == 'screen']
for nm, st, fm in OUTS:
    lo, hi = boot_cmp(a, b, st); P(f'  stacked minus screen, {nm}: {fm(st(a) - st(b))} CI {fm(lo)} to {fm(hi)}' + (' *' if lo * hi > 0 else ''))
P('-- by window')
outcome_block([(WIN_LABEL[i], [s for s in E if s['w'] == i]) for i in range(3)])
P('-- by main partner ship (n >= 8)')
outcome_block([(k + small(v), [s for s in E if s['mp'] and s['mp']['ship'] == k]) for k, v in C(s['mp']['ship'] for s in E if s['mp']).most_common() if v >= 8])
P('-- by DD ship')
outcome_block([(sh, [s for s in E if s['ship'] == sh]) for sh in SHIPS])
P('-- inside cap vs outside')
outcome_block([('inside cap', [s for s in E if s['inside']]), ('outside cap', [s for s in E if not s['inside']])])
P('who does the concealed damage: smoker share %', f1(100 * sum(x['conc'] for s in E for x in s['shooters'] if x['is_smoker']) / max(1, sum(x['conc'] for s in E for x in s['shooters']))))

P('\n== E. per map cells (three ships, early)')
for m in sorted(MAPS):
    e = [s for s in E if s['map'] == m]
    if not e: continue
    P(m, len(e), 'top', sum(s['grp'] == 'top' for s in e), '| ncap', C(s['ncap'] for s in e).most_common(4), '| cells', C(s['ncell_name'] for s in e).most_common(5), '| ships', dict(C(s['ship'] for s in e)),
      '| conc', n0(mean(s['conc'] for s in e)))
    for g in ('top', 'rest'):
        eg = [s for s in e if s['grp'] == g]
        if eg: P('   ', g, len(eg), 'ncap', C(s['ncap'] for s in eg).most_common(3), 'cells', C(s['ncell_name'] for s in eg).most_common(3), 'main partner', C(s['mp']['ship'] for s in eg if s['mp']).most_common(3),
                 'stacked%', f1(pct(eg, lambda s: s['coverage'] == 'stacked')), 'inside%', f1(pct(eg, lambda s: s['inside'])), 'conc', n0(mean(s['conc'] for s in eg)), 'el', n0(mean(s['el'] for s in eg)))

P('\n== F. opening playbook (all ships; one record per team-game)')
O = openings()
have = [o for o in O if o['n']]
P('team-games', len(O), 'with a smoke', len(have), 'with two', sum(o['n'] == 2 for o in O))
P('first cap: games with a single owner at first sighting', sum(o['fc'] in (0, 1) for o in O) // 2, '| both teams already hold one', sum(o['fc'] == 0.5 for o in O) // 2, '| none', sum(o['fc'] is None for o in O) // 2)
P('first cap sighting elapsed: median', n0(med(o['fc_el'] for o in O if o['fc_el'] is not None)), 'IQR', n0(q([o['fc_el'] for o in O if o['fc_el'] is not None], .25)), n0(q([o['fc_el'] for o in O if o['fc_el'] is not None], .75)))
P('lead at 5:00: games within 60 s', sum(o['lead'] is not None for o in O) // 2, 'within 30 s', sum(o['lead_gap'] is not None and o['lead_gap'] <= 30 for o in O) // 2, 'median gap s', n0(med(o['lead_gap'] for o in O if o['lead'] is not None)))
P('first smoke: median elapsed', n0(med(o['smokes'][0]['el'] for o in have)), 'in first 5 min %', f1(pct(have, lambda o: o['smokes'][0]['el'] < 300)), '| second: median', n0(med(o['smokes'][1]['el'] for o in O if o['n'] == 2)),
  'in first 5 min %', f1(pct([o for o in O if o['n'] == 2], lambda o: o['smokes'][1]['el'] < 300)))
P('first smoke by one of the three ships %', f1(pct(have, lambda o: o['smokes'][0]['ship'] in SHIPS)), 'ships', C(o['smokes'][0]['ship'] for o in have).most_common(8))
def ostat(v):
    fc = [o['fc'] for o in v if o['fc'] in (0, 1)]; ld = [o['lead'] for o in v if o['lead'] is not None]
    return len(v), (100 * mean(fc) if fc else None), len(fc), mean(ld), len(ld), pct(v, lambda o: o['win'])
def oline(lab, v):
    n, fc, nfc, ld, nld, w = ostat(v)
    if not n: return
    lo, hi = boot_stat(v, lambda x: ostat(x)[1]); l2, h2 = boot_stat(v, lambda x: ostat(x)[3]); l3, h3 = boot_stat(v, lambda x: ostat(x)[5])
    P(f'{lab:44s} n {n:3d} | first cap % {f1(fc)} [{f1(lo)}, {f1(hi)}] (n {nfc}) | lead@5 {f1(ld)} [{f1(l2)}, {f1(h2)}] (n {nld}) | win % {f1(w)} [{f1(l3)}, {f1(h3)}]')
def ocmp(lab, a, b):
    for x in a: x['_ab'] = 0
    for x in b: x['_ab'] = 1
    cl = by(a + b, 'team'); keys = list(cl); res = [[], [], []]
    for _ in range(1000):
        smp = [x for c in random.choices(keys, k=len(keys)) for x in cl[c]]
        sa, sb = ostat([x for x in smp if x['_ab'] == 0]), ostat([x for x in smp if x['_ab'] == 1])
        for i, j in enumerate((1, 3, 5)):
            if sa[j] is not None and sb[j] is not None: res[i].append(sa[j] - sb[j])
    sa, sb = ostat(a), ostat(b); o = []
    for i, (j, nm) in enumerate(((1, 'first cap pts'), (3, 'lead@5'), (5, 'win pts'))):
        r = sorted(res[i]); lo, hi = r[int(.025 * len(r))], r[int(.975 * len(r)) - 1]
        o.append(f'{nm} {f1(sa[j] - sb[j])} CI {f1(lo)} to {f1(hi)}' + (' *' if lo * hi > 0 else ''))
    P(f'  DIFF {lab}: ' + ' | '.join(o))
oline('all team-games', O)
P('-- timing of first smoke')
for i, lab in enumerate(WIN_LABEL + ['after 5 min']): oline('first smoke ' + lab, [o for o in have if o['smokes'][0]['w'] == i])
oline('no smoke at all', [o for o in O if not o['n']])
ocmp('first smoke before 4:00 vs later', [o for o in have if o['smokes'][0]['w'] <= 1], [o for o in have if o['smokes'][0]['w'] > 1])
P('-- who lays the first smoke')
for sh in SHIPS: oline('first smoke by ' + sh, [o for o in have if o['smokes'][0]['ship'] == sh])
oline('first smoke by other destroyer', [o for o in have if o['smokes'][0]['cls'] == 'destroyer' and o['smokes'][0]['ship'] not in SHIPS])
oline('first smoke by cruiser/battleship', [o for o in have if o['smokes'][0]['cls'] != 'destroyer'])
ocmp('three ships vs any other first smoker', [o for o in have if o['smokes'][0]['ship'] in SHIPS], [o for o in have if o['smokes'][0]['ship'] not in SHIPS])
P('-- first smoke partner type (first smoke by the three ships, in first 5 min)')
core = [o for o in have if o['smokes'][0]['ship'] in SHIPS and o['smokes'][0]['el'] < 300]
for t in PT_ORDER: oline('first smoke partner: ' + t, [o for o in core if o['smokes'][0]['pt'] == t])
ocmp('radar cruiser partner vs not', [o for o in core if o['smokes'][0]['pt'] == 'radar cruiser'], [o for o in core if o['smokes'][0]['pt'] != 'radar cruiser'])
for c in ('stacked', 'screen'): oline('first smoke ' + c, [o for o in core if o['smokes'][0]['coverage'] == c])
ocmp('stacked vs screen', [o for o in core if o['smokes'][0]['coverage'] == 'stacked'], [o for o in core if o['smokes'][0]['coverage'] == 'screen'])
oline('first smoke inside cap', [o for o in core if o['smokes'][0]['inside']]); oline('first smoke outside cap', [o for o in core if not o['smokes'][0]['inside']])
ocmp('inside vs outside cap', [o for o in core if o['smokes'][0]['inside']], [o for o in core if not o['smokes'][0]['inside']])
P('-- first two smokes: same cap or split')
two = [o for o in O if o['n'] == 2]
oline('both at the same cap', [o for o in two if o['smokes'][0]['ncap'] == o['smokes'][1]['ncap']]); oline('two different caps', [o for o in two if o['smokes'][0]['ncap'] != o['smokes'][1]['ncap']])
ocmp('same cap vs split', [o for o in two if o['smokes'][0]['ncap'] == o['smokes'][1]['ncap']], [o for o in two if o['smokes'][0]['ncap'] != o['smokes'][1]['ncap']])
oline('both first two in first 5 min', [o for o in two if o['smokes'][1]['el'] < 300]); oline('second smoke after 5 min', [o for o in two if o['smokes'][1]['el'] >= 300])
P('-- top vs rest')
for g in ('top', 'rest'):
    v = [o for o in have if o['grp'] == g]
    oline(g, [o for o in O if o['grp'] == g])
    P('   ', g, 'first smoke median el', n0(med(o['smokes'][0]['el'] for o in v)), 'before 4:00 %', f1(pct(v, lambda o: o['smokes'][0]['w'] <= 1)), 'by three ships %', f1(pct(v, lambda o: o['smokes'][0]['ship'] in SHIPS)),
      'radar CA partner %', f1(pct(v, lambda o: o['smokes'][0]['pt'] == 'radar cruiser')), 'same cap first two %', f1(pct([o for o in v if o['n'] == 2], lambda o: o['smokes'][0]['ncap'] == o['smokes'][1]['ncap'])))
P('-- per map: first-smoke cap, then common cap pairs for the first two smokes')
for m in sorted(MAPS):
    v = [o for o in have if o['map'] == m]
    if not v: continue
    P(m, 'team-games', len(v))
    for cap, n in C(o['smokes'][0]['ncap'] for o in v).most_common(3):
        oline(f'   first smoke at {cap}' + small(n), [o for o in v if o['smokes'][0]['ncap'] == cap])
    for (pr, n) in C(tuple(sorted(s['ncap'] for s in o['smokes'])) for o in v if o['n'] == 2).most_common(3):
        oline(f'   first two at {"+".join(pr)}' + small(n), [o for o in v if o['n'] == 2 and tuple(sorted(s['ncap'] for s in o['smokes'])) == pr])
    P('    first smoker', C(o['smokes'][0]['ship'] for o in v).most_common(4), '| first cap taken (norm letter)', C(c for o in v for c in o['fc_caps'] if o['fc'] == 1).most_common(3))
    for g in ('top', 'rest'):
        vg = [o for o in v if o['grp'] == g]
        P('   ', g, len(vg), 'first-smoke cap', C(o['smokes'][0]['ncap'] for o in vg).most_common(3), 'pairs', C('+'.join(sorted(s['ncap'] for s in o['smokes'])) for o in vg if o['n'] == 2).most_common(3))
P('-- did the team take the cap its first smoke was at? (single-owner games, first smoke in first 5 min)')
v = [o for o in have if o['fc'] == 1 and o['smokes'][0]['el'] < 300]
P('team took first cap n', len(v), 'first cap is the first-smoke cap %', f1(pct(v, lambda o: o['smokes'][0]['ncap'] in o['fc_caps'])))
open(os.path.join(OUT, 'stats.txt'), 'w', encoding='utf-8').write(out.getvalue())
