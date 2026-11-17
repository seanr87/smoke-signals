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
    for kind in ('long DD', 'short DD', 'cruiser', 'exhaust'):
        ss = [s for s in S if s['kind'] == kind]
        own = lambda ss: (100 * sum(x['conc'] for s in ss for x in s['shooters'] if x['is_smoker']) / max(1, sum(x['conc'] for s in ss for x in s['shooters'])))
        tgs = len({(s['game'], s['team']) for s in ss})
        print(kind, 'n', len(ss), 'per team-game', f1(len(ss) / ntg, '{:.2f}'), 'team-games using', tgs, 'per using tg', f1(len(ss) / tgs, '{:.2f}'),
              'conc', k(conc_per(ss)), ci(boot_stat(ss, conc_per), '{:,.0f}'), 'median', k(med(s['conc'] for s in ss)), 'zero%', f1(pct(ss, lambda s: s['conc'] == 0)),
              'd100', f1(d100(ss)), ci(boot_stat(ss, d100), '{:.1f}'), 'own', f1(own(ss)), ci(boot_stat(ss, own), '{:.0f}'),
              'selfish%', f1(pct(ss, lambda s: s['coverage'] == 'selfish')), 'radius', med(s['radius_m'] for s in ss), 'life', med(s['life_s'] for s in ss), 'emis', med(s['emission_s'] for s in ss))
    for a, b in (('long DD', 'short DD'),):
        ss = [s for s in S if s['kind'] in (a, b)]
        def diff(ss, f):
            x, y = f([s for s in ss if s['kind'] == a]), f([s for s in ss if s['kind'] == b])
            return None if x is None or y is None or not x and x != 0 else x - y
        print('long-short conc', ci(boot_stat(ss, lambda ss: diff(ss, lambda v: conc_per(v) if v else None)), '{:+,.0f}'), 'd100', ci(boot_stat(ss, lambda ss: diff(ss, lambda v: d100(v) if v else None)), '{:+.1f}'))
    for ship, ss in sorted(by(S, 'ship').items(), key=lambda a: -len(a[1])):
        if len(ss) >= 15: print('  ', ship, ss[0]['kind'], len(ss), k(conc_per(ss)), 'd100', f1(d100(ss)), 'emis', ss[0]['emission_s'], 'life', ss[0]['life_s'], 'r', ss[0]['radius_m'])

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

if '6' in which:
    print('=== 6 counter-smoke and chains (DD smokes; answered smoke can be any class)')
    byid = {s['id']: s for s in S}
    cs = [s for s in DD if s['counter_of']]; non = [s for s in DD if not s['counter_of']]
    print('counter n', len(cs), 'all classes', sum(1 for s in S if s['counter_of']), 'answered found', sum(1 for s in cs if s['counter_of'] in byid), 'answered class', C(byid[s['counter_of']]['cls'] for s in cs if s['counter_of'] in byid))
    f = lambda ss: ('n', len(ss), 'conc', k(conc_per(ss)), 'd100', f1(d100(ss)), 'capwon', f1(pct(ss, lambda s: s['cap_won'])), 'capdef', f1(pct(ss, lambda s: s['cap_def'])), 'inside', f1(pct(ss, lambda s: s['inside'])), 'selfish', f1(pct(ss, lambda s: s['coverage'] == 'selfish')), 'el', med(s['el'] for s in ss), 'win', f1(pct(ss, lambda s: s['win'])))
    print('counter', f(cs)); print('not', f(non))
    for g in ('top', 'rest'): print(g, 'counter share', f1(pct([s for s in DD if s['grp'] == g], lambda s: bool(s['counter_of']))), f([s for s in cs if s['grp'] == g]))
    print('share diff', ci(boot_diff(DD, lambda ss: pct(ss, lambda s: bool(s['counter_of']))), '{:+.1f}'))
    dif = lambda ss, fn: (fn([s for s in ss if s['counter_of']]) - fn([s for s in ss if not s['counter_of']])) if any(s['counter_of'] for s in ss) else None
    print('counter - not: conc', ci(boot_stat(DD, lambda ss: dif(ss, conc_per))), 'd100', ci(boot_stat(DD, lambda ss: dif(ss, d100)), '{:+.1f}'))
    answered_ids = {s['counter_of'] for s in S if s['counter_of']}
    ans = [s for s in DD if s['id'] in answered_ids]; unans = [s for s in DD if s['id'] not in answered_ids]
    print('answered DD smokes', f(ans)); print('unanswered', f(unans))
    dif2 = lambda ss, fn: (fn([s for s in ss if s['id'] in answered_ids]) - fn([s for s in ss if s['id'] not in answered_ids])) if any(s['id'] in answered_ids for s in ss) else None
    print('answered - not: conc', ci(boot_stat(DD, lambda ss: dif2(ss, conc_per))), 'd100', ci(boot_stat(DD, lambda ss: dif2(ss, d100)), '{:+.1f}'))
    # head to head: counter smoke vs the smoke it answered
    h = [(s, byid[s['counter_of']]) for s in cs if s['counter_of'] in byid]
    print('head to head n', len(h), 'counter conc', k(mean(a['conc'] for a, b in h)), 'answered conc', k(mean(b['conc'] for a, b in h)), 'counter wins', f1(pct(h, lambda p: p[0]['conc'] > p[1]['conc'])), 'gap s', med(a['el'] - b['el'] for a, b in h),
          'dist m', med(math.hypot(a['x'] - b['x'], a['z'] - b['z']) * WU for a, b in h))
    print('counter by map', {m: (len(v), f1(100 * len(v) / sum(1 for s in DD if s['map'] == m))) for m, v in by(cs, 'map').items()})
    print('counter by ship', {m: (len(v), f1(100 * len(v) / sum(1 for s in DD if s['ship'] == m))) for m, v in by(cs, 'ship').items() if len(v) >= 5})
    # chains: same-team smokes (all classes) within 1 km (centroid) and 60 s
    par = {s['id']: s['id'] for s in S}
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    links = 0
    for (gk, t), ss in by(S, lambda s: (s['game'], s['team'])).items():
        ss.sort(key=lambda s: s['el'])
        for i, a in enumerate(ss):
            for b in ss[i + 1:]:
                if b['el'] - a['el'] > 60: break
                if b['id'] in a['overlap_ids'] or a['id'] in b['overlap_ids'] or math.hypot(a['x'] - b['x'], a['z'] - b['z']) * WU <= 1000:
                    par[find(a['id'])] = find(b['id']); links += 1
    comp = by(S, lambda s: find(s['id']))
    chains = [v for v in comp.values() if len(v) > 1]
    print('links', links, 'chains', len(chains), 'sizes', C(len(v) for v in chains), 'smokes in chains', sum(len(v) for v in chains), 'overlap flagged', sum(1 for s in S if s['overlap_ids']))
    print('same player chains', sum(1 for v in chains if len({s['player'] for s in v}) == 1), 'class mix', C(tuple(sorted(C(s['cls'] for s in v).items())) for v in chains).most_common(6))
    inch = {s['id'] for v in chains for s in v}
    a, b = [s for s in DD if s['id'] in inch], [s for s in DD if s['id'] not in inch]
    print('DD in chain', f(a)); print('DD solo', f(b))
    dif3 = lambda ss, fn: (fn([s for s in ss if s['id'] in inch]) - fn([s for s in ss if s['id'] not in inch])) if any(s['id'] in inch for s in ss) else None
    print('chain - solo: conc', ci(boot_stat(DD, lambda ss: dif3(ss, conc_per))), 'd100', ci(boot_stat(DD, lambda ss: dif3(ss, d100)), '{:+.1f}'), 'capwon', ci(boot_stat(DD, lambda ss: dif3(ss, lambda v: pct(v, lambda s: s['cap_won']))), '{:+.1f}'))
    print('chain as unit: conc per chain', k(mean(sum(s['conc'] for s in v) for v in chains)), 'per smoke in chain', k(mean(s['conc'] for v in chains for s in v)), 'solo all classes', k(conc_per([s for s in S if s['id'] not in inch])))
    for g in ('top', 'rest'): print(g, 'chain share of DD smokes', f1(pct([s for s in DD if s['grp'] == g], lambda s: s['id'] in inch)))
    print('share diff', ci(boot_diff(DD, lambda ss: pct(ss, lambda s: s['id'] in inch)), '{:+.1f}'))
    print('chains by clan', C(v[0]['team'] for v in chains).most_common(8), 'by map', C(v[0]['map'] for v in chains))
    print('chain time', med(v[0]['el'] for v in chains), 'inside', f1(pct(chains, lambda v: any(s['inside'] for s in v))))
