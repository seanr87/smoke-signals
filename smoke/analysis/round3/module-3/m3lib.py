# Module 3 helpers (radar + smoke). Read-only on the batch.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
S, G = load()
OUT = os.path.dirname(os.path.abspath(__file__))
OLDDEF = os.environ.get('M3_OLDDEF') == '1'
MAPORDER = ['Sleeping Giant', 'Hotspot', 'Mountain Range', 'Land of Fire', 'Loop', 'Okinawa', 'Sea of Fortune']
NAME2 = {}
for g in G.values():
    for eid, pl in g['roster'].items(): NAME2[(g['key'], pl.get('name') or pl.get('player'))] = dict(pl, eid=eid)

def radar_ship(s):
    """The radar ship behind a radar play: dict(player, ship, cls, is_smoker, how, nx, nz) or None."""
    rc, orr = s['radar_cap'], s['off_radar']
    name = (orr or {}).get('ship') or ((rc or {}).get('ship') if (rc or {}).get('activated') else None)
    if not name: return None
    sm = next((x for x in s['j']['smokees'] if x['player'] == name), None)
    if not sm: return dict(player=name, ship='?', cls='?', is_smoker=False, how='?', nx=None, nz=None)
    pos = {p['entity_id']: p['position'] for p in s['j']['ships_at_capture'] if p.get('position')}
    p = pos.get(sm['entity_id'])
    nx, nz = norm(s['map'], s['side'], p['x'], p['z']) if p else (None, None)
    return dict(player=name, ship=sm['ship'].replace('\xa0', ' '), cls=sm['ship_class'].lower(), is_smoker=sm['role'] == 'smoker', how=sm['how'], nx=nx, nz=nz)

for s in S:
    if OLDDEF:  # round 3 definition: any radar tag
        s['cc'] = 'cap_control' in s['tags']; s['rt'] = 'radar_trap' in s['tags']
    else:  # round 4: primary purpose is a radar play (common.py radar_play)
        s['cc'] = s['pp'] == 'cap_control'; s['rt'] = s['pp'] == 'radar_trap'
    s['play'] = 'cap_control' if s['cc'] else 'radar_trap' if s['rt'] else None
    s['rship'] = radar_ship(s) if (s['cc'] or s['rt'] or s['off_radar']) else None
    s['spots'] = (s['off_radar'] or {}).get('enemies_spotted', 0)
    s['rsd'] = F(s['r']['radar_spotted_damage']) or 0.0
    s['early'] = s['el'] < 300
    s['stack'] = s['coverage'] == 'stacked'
    s['radar_in'] = any(p['radar'] and p['how'] == 'inside' for p in s['partners'])
    s['radar_any'] = any(p['radar'] for p in s['partners'])
    if not OLDDEF: assert (s['play'] is not None) == s['radar_play']
DD = [s for s in S if s['cls'] == 'destroyer']
CA = [s for s in S if s['cls'] == 'cruiser']
TG = team_games(G)
GAMES = C(t for _, t in TG)

def boot_rate_diff(counts, reps=1000):
    """counts: {team: plays}. 95% interval of plays per team-game, top minus rest, resampling clans."""
    tops = [t for t in GAMES if t in TOP]; rest = [t for t in GAMES if t not in TOP]
    out = []
    for _ in range(reps):
        a = random.choices(tops, k=len(tops)); b = random.choices(rest, k=len(rest))
        out.append(sum(counts.get(t, 0) for t in a) / sum(GAMES[t] for t in a) - sum(counts.get(t, 0) for t in b) / sum(GAMES[t] for t in b))
    out.sort(); return out[int(.025 * len(out))], out[int(.975 * len(out)) - 1]
def rate(counts, grp):
    ts = [t for t in GAMES if (t in TOP) == (grp == 'top')]
    return sum(counts.get(t, 0) for t in ts) / sum(GAMES[t] for t in ts)
def mmss(sec): return f'{int(sec)//60}:{int(sec)%60:02d}'
