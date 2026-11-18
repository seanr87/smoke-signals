import json, os, sys
J = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ships-maps.json'), encoding='utf-8'))
def f(o):
    if o is None: return '-'
    if isinstance(o, dict) and 'v' in o: return f"{o['v']} {o['ci']}" + ('*' if o.get('clear') else '') + (f" [T {o['top']} R {o['rest']}]" if 'top' in o else '')
    if isinstance(o, dict) and 'k' in o and 'n' in o: return f"{o['k']}/{o['n']}({o['pct']})"
    return str(o)
def cb(c):
    return ' | '.join(f"{suf}: own {x['ours']}/{x['neutral']}/{x['theirs']} we {f(x['we_took'])} en {f(x['enemy_took'])} en|ours {f(x['enemy_took_when_ours'])}" for suf, x in c.items() if suf != 'same_cap') + f" same {c['same_cap']}"
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
if which in ('all', 'B2'):
    b = J['B2']
    for r in b['rows']: print(r['label'], r['n'], r['clans'], 'died', f(r['died']), 'caught', f(r['caught']), 'dS', f(r['died_smoker']), 'cS', f(r['caught_smoker']), r['died_ships'], r['caught_ships'], r['n_died_base'])
    for r in b['undet']: print(r['label'], {k: (f(v) if isinstance(v, dict) else v) for k, v in r.items() if k != 'label'})
    for r in b['contrasts'] + b['undet_contrasts'] + b['tvr']: print(r['label'], {k: f(v) for k, v in r.items() if isinstance(v, dict)}, r.get('n_top'), r.get('n_rest'))
    print({k: v for k, v in b.items() if k not in ('rows', 'undet', 'contrasts', 'undet_contrasts', 'tvr')})
if which in ('all', 'B3'):
    b = J['B3']
    for r in b['rows']: print(r['label'], r['n'], r['clans'], {k: f(r[k]) for k in ('died', 'caught', 'died_smoker', 'caught_smoker', 'died_cr', 'caught_cr')}, r['n_cr_cov'], r['n_cr_in'], r['died_cr_n'], r['caught_cr_n'])
    print({k: f(v) for k, v in b['long_minus_sitters'].items() if isinstance(v, dict)})
    for r in b['tvr'] + b['won_minus_lost']: print(r['label'], r.get('n_top'), r.get('n_rest'), {k: f(v) for k, v in r.items() if isinstance(v, dict)})
    for r in b['win_split']: print(r.get('ship'), r.get('result'), r.get('n_top'), r.get('n_rest'), {k: f(v) for k, v in r.items() if isinstance(v, dict)}, r.get('top'), r.get('rest'))
if which in ('all', '7a'):
    for r in J['C7a']:
        print('\n', r['id'], r['cells'], r['n'], r['top6'], r['rest'], 'conc', r['conc'], r['conc_r5b'], 'rest', r['conc_rest_of_map'], r['conc_gap_ci'], 'r5b cap', r['r5b_cap_taken_pct'], r['r5b_cap_taken_n'], r['near_caps'], r['contested_caps'], 'early', r['early'])
        print('  cell', cb(r['caps'])); print('  rest', cb(r['caps_rest']))
        print('  deaths', {k: f(r['deaths'][k]) for k in ('died', 'caught', 'died_smoker', 'caught_smoker')}, 'rest', {k: f(r['deaths_rest'][k]) for k in ('died', 'caught', 'died_smoker', 'caught_smoker')})
        print('  vs rest', {k: f(v) for k, v in r['vs_rest'].items() if isinstance(v, dict)})
        print('  tvr', {k: (f(v['top']), f(v['rest']), v['ci']) for k, v in r['tvr'].items()}, {k: f(v) for k, v in r['tvr_deaths'].items() if isinstance(v, dict)})
def pr(r):
    print(r['label'], r['n'], 'T', r['top6'], '|', cb(r['caps']), '| inv', f(r['enemy_in_cap']), 'inv|ours', f(r['enemy_in_cap_when_ours']), r['enemy_in_cap_median_s'], '| conc', r['conc'], {k: f(r['deaths'][k]) for k in ('died', 'caught', 'died_smoker', 'caught_smoker')})
    if 'B' in r: print('     B:', {k: f(v) for k, v in r['B'].items()}, r['near_caps'], r['contested_caps'], r['ships'])
if which in ('all', '7b'):
    b = J['C7b']; print('\n7b', b['n_map'], b['n_near'])
    for r in b['rows']: pr(r)
    pr(b['B']['top']); pr(b['B']['rest'])
    print({k: f(v) for k, v in b['b_vs_other'].items() if isinstance(v, dict)}); print(b['ours_share'])
    print({k: v for k, v in b['B'].items() if k not in ('top', 'rest')}); print(b['share_of_map'], b['ours_tvr'])
if which in ('all', '7c'):
    b = J['C7c']; print('\n7c', b['n_map'], b['n_B'], b['overlap'])
    for r in b['rows']: pr(r)
    for r in b['contrasts']: print(r['label'], {k: f(v) for k, v in r.items() if isinstance(v, dict)})
    for x in b['list']: print('  ', x)
    print(b['clan_text'], b['ships'], b['lost_games'], b['share_tvr'])
    for r in b['whole_map'].values(): pr(r)
if which in ('all', '7d'):
    b = J['C7d']; print('\n7d', b['n_sitters'], b['n_sitters_top'], b['n_sitters_rest'])
    for r in b['rows']: pr(r)
    pr(b['outside'])
    for k in ('tvr_deaths', 'tvr_caps', 'tvr_conc', 'tvr_ours', 'in_vs_out'): print(k, {a: f(v) for a, v in b[k].items() if isinstance(v, dict)})
    print(b['clan_text'], b['conc_r5b'], b['deaths_r5b'])
