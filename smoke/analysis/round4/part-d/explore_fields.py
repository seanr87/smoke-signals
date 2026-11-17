import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'round3'))); from common import *; S, G = load()
print(len(S), len(G))
for k in ('coverage', 'movement', 'pp', 'kind', 'habit', 'cls', 'map'):
    print(k, dict(C(s[k] for s in S)))
wl = win_loss(G)
tg = C(t for _, t in team_games(G))
print({t: (wl[t], tg[t]) for t in sorted(tg, key=lambda t: -tg[t])})
s = S[0]
print({k: v for k, v in s['r'].items()})
print(s['cast'][:3])
g = next(iter(G.values()))
print(list(g['roster'].values())[0])
print('other ships', C(s['ship'] for s in S if s['habit'] == 'other'))
print('overlap share', pct(S, lambda s: bool(s['overlap_ids'])), 'selfish', pct(S, lambda s: s['selfish']))
for t in ['H-SR', 'RESIN', 'BONKZ', 'HTDOG', 'KITE', 'VRTUS', 'PN']:
    ss = [x for x in S if x['team'] == t]
    print(t, len(ss), 'cov', dict(C(x['coverage'] for x in ss)), 'mov', dict(C(x['movement'] for x in ss)), 'ovl', round(pct(ss, lambda s: bool(s['overlap_ids']))), 'selfish', round(pct(ss, lambda s: s['selfish'])))
