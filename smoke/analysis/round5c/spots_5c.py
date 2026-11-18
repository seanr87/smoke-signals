# Builds round5c/spots.json from round5b/spots.json: adds show and status to every record, renames the death field to say
# which metric it is, and replaces snapshot cap numbers with the cap-timeline numbers from x2-ships-maps where they exist.
# Run: python -I -X utf8 spots_5c.py
import json, os
H = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(os.path.join(H, '..', 'round5b', 'spots.json'), encoding='utf-8'))
x2 = json.load(open(os.path.join(H, 'x2-ships-maps', 'ships-maps.json'), encoding='utf-8'))
GOLD = {'c5-lp-sitters-b', 'c5-lf-svea-f5', 'c5-sf-svea-h7'}
HIDE = {'c5-ok-death-zone', 'c5-lp-f8', 'c5-lp-f10'}
NO_RATES = {'c5-sf-early-d'}
RATE_KEYS = ('share_top6_pct', 'share_rest_pct', 'gap_pts', 'ci_pts', 'share_top6', 'share_rest', 'diff_pts', 'diff_ci', 'concealed_damage_per_smoke',
             'caught_per_100', 'caught_smoker_per_100')
cells = {c['id']: c for c in x2['C7a']}
out = []
for r in src['spots']:
    r = dict(r)
    # the death number in a spot record is the batch list ("caught"), not track deaths
    if 'deaths_per_100' in r: r['caught_per_100'] = r.pop('deaths_per_100')
    if 'smoker_deaths_per_100' in r: r['caught_smoker_per_100'] = r.pop('smoker_deaths_per_100')
    # cap numbers built on the batch cap_won field are withdrawn
    for k in ('cap_taken_n', 'cap_taken_pct'):
        r.pop(k, None)
    if r['id'] in cells:
        r['timeline'] = {k: v for k, v in cells[r['id']].items() if k not in ('id', 'map', 'cells', 'clan_text')}
    if r['id'] == 'c5-lp-sitters-b':
        r['timeline'] = dict(caps=x2['C7d']['tvr_caps'], deaths=x2['C7d']['tvr_deaths'], all=x2['C7d']['rows'][0])
    if r['kind'] == 'danger_zone' or r['id'] in HIDE:
        r['show'] = False
        r['status'] = 'hidden: no danger zone is kept (flags in line with chance)' if r['kind'] == 'danger_zone' else 'hidden: high cell on 15 or fewer smokes, reference only'
        r['draw'] = None
    elif r['id'] in GOLD:
        r['kind'] = 'top6_spot'; r['mode'] = 'top6'; r['show'] = True; r['status'] = 'gold'; r['draw'] = 'gold'
    elif r['kind'] == 'top6_spot':
        r['show'] = True; r['status'] = 'lead'; r['draw'] = 'neutral'
    else:
        r['show'] = True; r['status'] = 'shared'; r['draw'] = 'neutral'
    if r['id'] in NO_RATES:
        for k in RATE_KEYS:
            if k in r: r[k] = None
        r['status'] = 'shared, too few for rates (n 7)'
        r['small_n'] = True
    out.append(r)
ids = [r['id'] for r in out]; assert len(ids) == len(set(ids))
assert sum(r['status'] == 'gold' for r in out) == 3 and sum(r['status'] == 'lead' for r in out) == 6, [r['id'] for r in out if r['status'] in ('gold', 'lead')]
doc = dict(batch='output/20261117-230933', frame=src['frame'], kinds=src['kinds'], mode_rule=src['mode_rule'],
           fields=dict(show='true = draw it on the map page; false = keep in the data only',
                       status="'gold' (Top 6 spot, drawn as such), 'lead' (Top 6 by the interval rule but chosen for the gap: draw neutral), "
                              "'shared', or a 'hidden: ...' reason",
                       draw="'gold', 'neutral' or null",
                       caught_per_100='deaths per 100 smokes on the batch smoke_deaths list ("caught"); track deaths ("died") are in the timeline block where present',
                       timeline='cap results from the cap timeline and both death metrics, for the records redone in round 5c item 7'),
           changed_from_round5b='show, status and draw added to all 45 records. Three records are gold; six other Top 6 records are leads drawn neutral; '
                                'the six danger zones and the two Loop high cells are hidden; c5-sf-early-d has no rates. deaths_per_100 renamed caught_per_100. '
                                'cap_taken_n and cap_taken_pct (batch cap_won) removed; timeline values added for the five high cells and the Loop cap-sitter spot.',
           spots=out)
json.dump(doc, open(os.path.join(H, 'spots.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
from collections import Counter
print(len(out), Counter((r['show'], r['status'].split(':')[0]) for r in out))
