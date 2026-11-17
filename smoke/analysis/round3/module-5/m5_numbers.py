import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m5lib import *
which = sys.argv[1:] or list('123456')

if '1' in which:
    print('=== 1 partnerships')
    print('shooter conc sum', sum(x['conc'] for s in S for x in s['shooters']), 'smoke conc sum', sum(s['conc'] for s in S), 'DD', sum(s['conc'] for s in DD))
    print('unknown cls shooters', C(x['cls'] for s in S for x in s['shooters']))
    # pair: smoker ship + other ship that was covered (partner) or shot. conc by that ship per such smoke.
    pair = collections.defaultdict(list)
    for s in DD:
        seen = {}
        for p in s['partners']: seen.setdefault(p['ship'], 0.0)
        for x in s['shooters']:
            if not x['is_smoker']: seen[x['ship']] = seen.get(x['ship'], 0.0) + x['conc']
        for ship, v in seen.items(): pair[(s['ship'], ship)].append((v, s))
    rows = sorted(((kk, len(v), mean(a for a, _ in v), len({s['team'] for _, s in v}), pct(v, lambda a: a[0] > 0)) for kk, v in pair.items() if len(v) >= 20), key=lambda r: -r[2])
    for r in rows: print(r)
    self_ = by(DD, 'ship')
    for ship, ss in sorted(self_.items(), key=lambda a: -len(a[1])):
        print('self', ship, len(ss), k(mean(sum(x['conc'] for x in s['shooters'] if x['is_smoker']) for s in ss)), 'all', k(conc_per(ss)))
    def share(ss, cls=None, smoker=None):
        tot = sum(x['conc'] for s in ss for x in s['shooters'])
        if not tot: return None
        return 100 * sum(x['conc'] for s in ss for x in s['shooters'] if (cls is None or x['cls'] == cls) and (smoker is None or x['is_smoker'] == smoker)) / tot
    for lab, ss in (('top', [s for s in DD if s['grp'] == 'top']), ('rest', [s for s in DD if s['grp'] == 'rest']), ('H-SR', [s for s in DD if s['team'] == 'H-SR']), ('PN', [s for s in DD if s['is_pn']])):
        print(lab, len(ss), 'smoker', f1(share(ss, smoker=True)), 'cruiser', f1(share(ss, 'cruiser')), 'bb', f1(share(ss, 'battleship')), 'other dd', f1(share(ss, 'destroyer', False)), 'dd all', f1(share(ss, 'destroyer')))
    for c in ('cruiser', 'battleship'):
        print(c, 'diff ci', ci(boot_diff(DD, lambda ss: share(ss, c)), '{:+.1f}'))
    print('smoker diff ci', ci(boot_diff(DD, lambda ss: share(ss, smoker=True)), '{:+.1f}'))
    for t in sorted(NG, key=lambda t: -NG[t]):
        ss = [s for s in DD if s['team'] == t]
        if ss: print('  ', t, len(ss), 'cruiser share', f1(share(ss, 'cruiser')), 'smoker', f1(share(ss, smoker=True)), 'conc/smoke', k(conc_per(ss)))
    print('H-SR all classes cruiser share', f1(share([s for s in S if s['team'] == 'H-SR'], 'cruiser')))

if '2' in which:
    print('=== 2 smoke type lens (all classes)')
    ntg = len(TG)
    print('other (left out)', sum(1 for s in S if s['habit'] == 'other'), C(s['ship'] for s in S if s['habit'] == 'other').most_common())
    def use(clans, hb):
        return sum(1 for c in clans for s in S if s['team'] == c and s['habit'] == hb) / sum(NG[c] for c in clans)
    for kind in HABITS:
        ss = [s for s in S if s['habit'] == kind]
        print(kind, 'use interval', ci(boot_clans(lambda cl: use(cl, kind), groups=False), '{:.2f}'), 'clans', len({s['team'] for s in ss}), 'classes', dict(C(s['cls'] for s in ss)))
        own = lambda ss: (100 * sum(x['conc'] for s in ss for x in s['shooters'] if x['is_smoker']) / max(1, sum(x['conc'] for s in ss for x in s['shooters'])))
        tgs = len({(s['game'], s['team']) for s in ss})
        print(kind, 'n', len(ss), 'per team-game', f1(len(ss) / ntg, '{:.2f}'), 'team-games using', tgs, 'per using tg', f1(len(ss) / tgs, '{:.2f}'),
              'conc', k(conc_per(ss)), ci(boot_stat(ss, conc_per), '{:,.0f}'), 'median', k(med(s['conc'] for s in ss)), 'zero%', f1(pct(ss, lambda s: s['conc'] == 0)),
              'd100', f1(d100(ss)), ci(boot_stat(ss, d100), '{:.1f}'), 'own', f1(own(ss)), ci(boot_stat(ss, own), '{:.0f}'),
              'selfish%', f1(pct(ss, lambda s: s['coverage'] == 'selfish')), 'radius', med(s['radius_m'] for s in ss), 'life', med(s['life_s'] for s in ss), 'emis', med(s['emission_s'] for s in ss))
    for a, b in (('flank smoke lines', 'cap sitters'), ('flank smoke lines', 'parked cruiser smoke'), ('flank smoke lines', 'moving exhaust')):
        ss = [s for s in S if s['habit'] in (a, b)]
        def diff(ss, f):
            x, y = f([s for s in ss if s['habit'] == a]), f([s for s in ss if s['habit'] == b])
            return None if x is None or y is None or not x and x != 0 else x - y
        print(a, 'minus', b, 'conc', ci(boot_stat(ss, lambda ss: diff(ss, lambda v: conc_per(v) if v else None)), '{:+,.0f}'), 'd100', ci(boot_stat(ss, lambda ss: diff(ss, lambda v: d100(v) if v else None)), '{:+.1f}'))
    for ship, ss in sorted(by(S, 'ship').items(), key=lambda a: -len(a[1])):
        if len(ss) >= 15: print('  ', ship, ss[0]['habit'], len(ss), k(conc_per(ss)), 'd100', f1(d100(ss)), 'emis', ss[0]['emission_s'], 'life', ss[0]['life_s'], 'r', ss[0]['radius_m'])

if '3' in which:
    print('=== 3 timing (DD)')
    for grp in ('top', 'rest'):
        print(grp)
        for b in range(0, 1200, 120):
            expo = sum(max(0, min(G[gk]['len'], b + 120) - b) / 120 for gk, t in TG if G[gk]['len'] and grp_of(t) == grp)
            ss = [s for s in DD if s['grp'] == grp and b <= s['el'] < b + 120 and G[s['game']]['len']]
            print('  ', b // 60, 'expo', f1(expo), 'n', len(ss), 'rate', f1(len(ss) / expo if expo > 3 else None, '{:.2f}'), 'conc', k(conc_per(ss)), 'd100', f1(d100(ss)))
    def rate(clans, lo, hi):
        expo = sum(max(0, min(G[gk]['len'], hi) - lo) / 120 for c in clans for gk, t in TG if t == c and G[gk]['len'])
        n = sum(1 for c in clans for s in DD if s['team'] == c and lo <= s['el'] < hi and G[s['game']]['len'])
        return n / expo if expo else None
    for lo, hi in ((0, 120), (120, 240), (240, 480), (480, 720), (720, 1200)):
        print('rate diff', lo, hi, f1(rate([c for c in NG if c in TOP], lo, hi), '{:.2f}'), f1(rate([c for c in NG if c not in TOP], lo, hi), '{:.2f}'), ci(boot_clans(lambda cl: rate(cl, lo, hi)), '{:+.2f}'),
              'conc diff', ci(boot_diff([s for s in DD if lo <= s['el'] < hi], conc_per), '{:+,.0f}'))
    print('first DD smoke time per team-game: top', med(min(s['el'] for s in v) for kk, v in by([s for s in DD if s['grp'] == 'top'], lambda s: (s['game'], s['team'])).items()),
          'rest', med(min(s['el'] for s in v) for kk, v in by([s for s in DD if s['grp'] == 'rest'], lambda s: (s['game'], s['team'])).items()))
    st = lambda s: 'ahead 50+' if s['score_diff'] >= 50 else 'behind 50+' if s['score_diff'] <= -50 else 'level'
    for grp in ('top', 'rest', 'all'):
        for state in ('ahead 50+', 'level', 'behind 50+'):
            ss = [s for s in DD if (grp == 'all' or s['grp'] == grp) and st(s) == state]
            ss2 = [s for s in ss if s['el'] >= 240]
            print(grp, state, 'n', len(ss), 'share', f1(100 * len(ss) / sum(1 for s in DD if grp == 'all' or s['grp'] == grp)), 'conc', k(conc_per(ss)), 'd100', f1(d100(ss)), 'selfish', f1(pct(ss, lambda s: s['coverage'] == 'selfish')),
                  'inside', f1(pct(ss, lambda s: s['inside'])), 'escape', f1(pct(ss, lambda s: 'escape' in s['tags'])), 'kite', f1(pct(ss, lambda s: s['movement'] == 'kiting')), 'push', f1(pct(ss, lambda s: s['movement'] == 'pushing')), '| after 4 min n', len(ss2), k(conc_per(ss2)), f1(d100(ss2)))
    for state in ('ahead 50+', 'level', 'behind 50+'):
        ss = [s for s in DD if st(s) == state]
        print(state, 'top-rest conc', ci(boot_diff(ss, conc_per)), 'd100', ci(boot_diff(ss, d100), '{:+.1f}'))
    late = [s for s in DD if s['el'] >= 240]
    def ab(ss, f):
        a, b = [s for s in ss if st(s) == 'ahead 50+'], [s for s in ss if st(s) == 'behind 50+']
        return f(a) - f(b) if a and b else None
    print('ahead - behind (after 4 min): conc', ci(boot_stat(late, lambda ss: ab(ss, conc_per)), '{:+,.0f}'), 'd100', ci(boot_stat(late, lambda ss: ab(ss, d100)), '{:+.1f}'))

if '4' in which:
    print('=== 4 survival (DD smokes)')
    print('all DD', len(DD), 'deaths', sum(s['deaths'] for s in DD), f1(d100(DD)), 'smokes with a death', sum(1 for s in DD if s['deaths']))
    dl = [(s, d) for s in DD for d in s['j']['smoke_deaths']]
    print('who: smoker', sum(1 for s, d in dl if d['player'] == s['player']), 'partner', sum(1 for s, d in dl if d['player'] != s['player']), 'concealed', C(d['concealed'] for s, d in dl), 'after_cleared', C(d['after_cleared'] for s, d in dl))
    print('partner death ships', C(d['ship'] for s, d in dl if d['player'] != s['player']), 'cls', C(G[s['game']]['roster'].get(d['entity_id'], {}).get('ship_class') for s, d in dl if d['player'] != s['player']))
    print('all classes: smoker', sum(1 for s in S for d in s['j']['smoke_deaths'] if d['player'] == s['player']), 'partner', sum(1 for s in S for d in s['j']['smoke_deaths'] if d['player'] != s['player']))
    sd = lambda ss: 100 * sum(1 for s in ss for d in s['j']['smoke_deaths'] if d['player'] == s['player']) / len(ss) if ss else None
    pd = lambda ss: 100 * sum(1 for s in ss for d in s['j']['smoke_deaths'] if d['player'] != s['player']) / len(ss) if ss else None
    def tab(name, key, order=None):
        d = by(DD, key)
        for kk in (order or sorted(d, key=lambda a: -len(d[a]))):
            ss = d.get(kk, [])
            if len(ss) < 8: continue
            print('  ', name, kk, 'n', len(ss), 'd100', f1(d100(ss)), ci(boot_stat(ss, d100), '{:.1f}'), 'smoker', f1(sd(ss)), 'partner', f1(pd(ss)), 'conc', k(conc_per(ss)), 'partners/smoke', f1(mean(len(s['partners']) for s in ss)))
    tab('ship', 'ship'); tab('cov', 'coverage'); tab('band', lambda s: band(s['edge']), BANDS); tab('radar', lambda s: s['radar_on_us'] > 0); tab('grp', 'grp'); tab('move', 'movement'); tab('pp', 'pp')
    tab('band no mrA', lambda s: 'mrA' if s['mrA'] else band(s['edge']), BANDS + ['mrA'])
    tab('time', lambda s: min(4, s['el'] // 240))
    print('radar diff', ci(boot_stat(DD, lambda ss: (d100([s for s in ss if s['radar_on_us'] > 0]) or 0) - (d100([s for s in ss if s['radar_on_us'] == 0]) or 0)), '{:+.1f}'))
    print('inside vs 3km+ diff', ci(boot_stat(DD, lambda ss: (d100([s for s in ss if s['edge'] < 0]) or 0) - (d100([s for s in ss if s['edge'] >= 3000]) or 0)), '{:+.1f}'))
    print('top-rest', ci(boot_diff(DD, d100), '{:+.1f}'))
    print('PN', len([s for s in DD if s['is_pn']]), d100([s for s in DD if s['is_pn']]))
    print('radar x inside', {(a, b): (len(v), f1(d100(v))) for (a, b), v in by(DD, lambda s: (s['radar_on_us'] > 0, s['inside'])).items()})
    print('deaths by map', {m: (len(v), sum(s['deaths'] for s in v), f1(d100(v))) for m, v in by(DD, 'map').items()})
    print('smoker hp at act: died', med(F(s['r']['smoker_hp_pct_act']) for s in DD if F(s['r']['smoker_hp_pct_act']) is not None and any(d['player'] == s['player'] for d in s['j']['smoke_deaths'])), 'lived', med(F(s['r']['smoker_hp_pct_act']) for s in DD if F(s['r']['smoker_hp_pct_act']) is not None and not s['deaths']))

    print('--- Somers vs Gearing (DD smokes)')
    so, ge = [s for s in DD if s['ship'] == 'Somers'], [s for s in DD if s['ship'] == 'Gearing']
    sgd = lambda ss, fn: (fn([s for s in ss if s['ship'] == 'Somers']) - fn([s for s in ss if s['ship'] == 'Gearing'])) if any(s['ship'] == 'Somers' for s in ss) and any(s['ship'] == 'Gearing' for s in ss) else None
    both = so + ge
    print('Somers n', len(so), 'clans', len({s['team'] for s in so}), 'conc', k(conc_per(so)), ci(boot_stat(so, conc_per), '{:,.0f}'), 'd100', f1(d100(so)), ci(boot_stat(so, d100), '{:.1f}'))
    print('Gearing n', len(ge), 'clans', len({s['team'] for s in ge}), 'conc', k(conc_per(ge)), ci(boot_stat(ge, conc_per), '{:,.0f}'), 'd100', f1(d100(ge)), ci(boot_stat(ge, d100), '{:.1f}'))
    print('Somers - Gearing: conc', sg(conc_per(so) - conc_per(ge)), ci(boot_stat(both, lambda ss: sgd(ss, conc_per))), 'd100', f1(d100(so) - d100(ge), '{:+.1f}'), ci(boot_stat(both, lambda ss: sgd(ss, d100)), '{:+.1f}'))
    print('clans using both', len({s['team'] for s in so} & {s['team'] for s in ge}), 'top share Somers', f1(pct(so, lambda s: s['grp'] == 'top')), 'Gearing', f1(pct(ge, lambda s: s['grp'] == 'top')),
          'stacked Somers', f1(pct(so, lambda s: s['coverage'] == 'stacked')), 'Gearing', f1(pct(ge, lambda s: s['coverage'] == 'stacked')), 'radar caught Somers', f1(pct(so, lambda s: s['radar_on_us'] > 0)), 'Gearing', f1(pct(ge, lambda s: s['radar_on_us'] > 0)))
    for hb in ('flank smoke lines', 'cap sitters'):
        ss = [s for s in DD if s['habit'] == hb]
        print(hb, 'n', len(ss), 'd100', f1(d100(ss)), ci(boot_stat(ss, d100), '{:.1f}'), 'smoker', f1(sd(ss)), 'partner', f1(pd(ss)), 'conc', k(conc_per(ss)))
    fl = [s for s in DD if s['habit'] in ('flank smoke lines', 'cap sitters')]
    hd = lambda ss: (d100([s for s in ss if s['habit'] == 'flank smoke lines']) - d100([s for s in ss if s['habit'] == 'cap sitters'])) if any(s['habit'] == 'cap sitters' for s in ss) and any(s['habit'] == 'flank smoke lines' for s in ss) else None
    print('flank - cap sitters d100', ci(boot_stat(fl, hd), '{:+.1f}'), 'DD other', sum(1 for s in DD if s['habit'] == 'other'))

if '6' in which:
    print('=== 6 counter-smoke and chains (DD smokes; answered smoke can be any class). Lookups match on game + id.')
    gid = lambda s: (s['game'], s['id'])
    byid = {gid(s): s for s in S}
    ans_of = lambda s: byid.get((s['game'], s['counter_of'])) if s['counter_of'] else None
    cs = [s for s in DD if s['counter_of']]; non = [s for s in DD if not s['counter_of']]
    print('counter n', len(cs), 'all classes', sum(1 for s in S if s['counter_of']), 'answered found', sum(1 for s in cs if ans_of(s)), 'enemy', sum(1 for s in cs if ans_of(s) and ans_of(s)['team'] != s['team']), 'answered class', C(ans_of(s)['cls'] for s in cs if ans_of(s)), 'PN', sum(1 for s in cs if s['is_pn']))
    f = lambda ss: ('n', len(ss), 'conc', k(conc_per(ss)), 'd100', f1(d100(ss)), 'capwon', f1(pct(ss, lambda s: s['cap_won'])), 'inside', f1(pct(ss, lambda s: s['inside'])), 'selfish', f1(pct(ss, lambda s: s['coverage'] == 'selfish')), 'el', med(s['el'] for s in ss))
    print('counter', f(cs)); print('not', f(non))
    for g in ('top', 'rest'): print(g, 'counter share', f1(pct([s for s in DD if s['grp'] == g], lambda s: bool(s['counter_of']))), f([s for s in cs if s['grp'] == g]))
    print('share diff', ci(boot_diff(DD, lambda ss: pct(ss, lambda s: bool(s['counter_of']))), '{:+.1f}'), 'top-rest counter conc', ci(boot_diff(cs, conc_per)))
    dif = lambda ss, fn: (fn([s for s in ss if s['counter_of']]) - fn([s for s in ss if not s['counter_of']])) if any(s['counter_of'] for s in ss) and any(not s['counter_of'] for s in ss) else None
    print('all DD counter - not: conc', ci(boot_stat(DD, lambda ss: dif(ss, conc_per))), 'd100', ci(boot_stat(DD, lambda ss: dif(ss, d100)), '{:+.1f}'))
    for hb in ('flank smoke lines', 'cap sitters'):
        ss = [s for s in DD if s['habit'] == hb]
        a, b = [s for s in ss if s['counter_of']], [s for s in ss if not s['counter_of']]
        print(hb, 'counter', len(a), k(conc_per(a)), f1(d100(a)), 'not', len(b), k(conc_per(b)), f1(d100(b)), 'diff', ci(boot_stat(ss, lambda v: dif(v, conc_per))), ci(boot_stat(ss, lambda v: dif(v, d100)), '{:+.1f}'), 'counter share', f1(100 * len(a) / len(ss)))
    print('DD other habit', sum(1 for s in DD if s['habit'] not in ('flank smoke lines', 'cap sitters')), 'of which counter', sum(1 for s in cs if s['habit'] not in ('flank smoke lines', 'cap sitters')))
    h = [(s, ans_of(s)) for s in cs if ans_of(s)]
    print('head to head n', len(h), 'counter conc', k(mean(a['conc'] for a, b in h)), 'answered conc', k(mean(b['conc'] for a, b in h)), 'counter wins', f1(pct(h, lambda p: p[0]['conc'] > p[1]['conc'])),
          ci(boot_stat([a for a, b in h], lambda ss: pct(ss, lambda s: s['conc'] > ans_of(s)['conc'])), '{:.0f}'), 'gap s', med(a['el'] - b['el'] for a, b in h),
          'dist km', med(math.hypot(a['x'] - b['x'], a['z'] - b['z']) * WU / 1000 for a, b in h), 'same cap', f1(pct(h, lambda p: p[0]['cap'] == p[1]['cap'])))
    print('counter by map', {m: (len(v), f1(100 * len(v) / sum(1 for s in DD if s['map'] == m)), 'own half', f1(pct(v, lambda s: s['ncell'][1] >= 5))) for m, v in by(cs, 'map').items()})
    from m5_cluster import chains
    for lim in (500, 1000, 1500):
        ch = chains(S, lim, 60); inch = {gid(s) for v in ch for s in v}
        a, b = [s for s in DD if gid(s) in inch], [s for s in DD if gid(s) not in inch]
        print('lim', lim, 'chains', len(ch), C(len(v) for v in ch), 'DD in', len(a), k(conc_per(a)), f1(d100(a)), 'solo', len(b), k(conc_per(b)), f1(d100(b)), 'same player', sum(1 for v in ch if len({s['player'] for s in v}) == 1),
              'cls mix', C(tuple(sorted(C(s['cls'] for s in v).items())) for v in ch).most_common(4))
    ch = chains(S, 1000, 60); inch = {gid(s) for v in ch for s in v}
    dif3 = lambda ss, fn: (fn([s for s in ss if gid(s) in inch]) - fn([s for s in ss if gid(s) not in inch])) if any(gid(s) in inch for s in ss) else None
    print('chain - solo: conc', ci(boot_stat(DD, lambda ss: dif3(ss, conc_per))), 'd100', ci(boot_stat(DD, lambda ss: dif3(ss, d100)), '{:+.1f}'))
    print('by clan', C(v[0]['team'] for v in ch).most_common(10), 'grp', C(v[0]['grp'] for v in ch), 'habits', C(tuple(sorted(s['habit'] for s in v)) for v in ch).most_common(6))
