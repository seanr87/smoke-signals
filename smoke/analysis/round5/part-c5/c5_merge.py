import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
# Joins the per-map outputs into the two files the round's shared JSON is built from.
parts = {n: json.load(open(os.path.join(HERE, f'part-{n}.json'), encoding='utf-8')) for n in ('sg', 'hs', 'lp', 'rest')}
dar = json.load(open(os.path.join(HERE, 'part-lp-daring.json'), encoding='utf-8'))
q = {}; spots = []
for n, p in parts.items():
    for k, v in p['R'].items(): q['C5-' + k] = v
    spots += p['SPOTS']
q['C5-LP-4'] = dar
order = ['C5-SG-1', 'C5-SG-2', 'C5-SG-3', 'C5-HS-1', 'C5-HS-2', 'C5-HS-3', 'C5-LP-1', 'C5-LP-2', 'C5-LP-3', 'C5-LP-4', 'C5-LP-5', 'C5-LP-6', 'C5-MR-1', 'C5-MR-2', 'C5-LF-1', 'C5-LF-2', 'C5-SF-1', 'C5-SF-2', 'C5-SF-3', 'C5-OK-1', 'C5-OK-2']
assert set(order) == set(q), set(order) ^ set(q)
out = dict(part='c5', batch='output/20261117-122135', frame='team-normalized, own spawn at the bottom (bottom-left on Okinawa); u, v in the 0-1 minimap frame, origin top-left',
           groups=dict(top6=['H-SR', 'RESIN', 'BONKZ', 'HTDOG', 'KITE', 'VRTUS'], rest='every other clan'),
           gap_fields='top_k/top_n and rest_k/rest_n are counts; gap is Top 6 share minus Rest share in points; lo/hi the 95% interval (clans resampled); mark is "Top 6" when the interval excludes zero and the gap is positive, else "Shared"',
           questions={k: q[k] for k in order})
json.dump(out, open(os.path.join(HERE, 'map-questions.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump(spots, open(os.path.join(HERE, 'spots.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('questions', len(q), 'spots', len(spots)); 
for s in spots: print(' ', s['id'], s['kind'], s['mode'], 'n', s['n'], 'top6', s['n_top6'], 'rest', s['n_rest'], s['shape']['type'])
