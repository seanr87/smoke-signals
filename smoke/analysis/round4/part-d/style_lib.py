# Part D helper: clan style numbers, supporting cast, distances. Read-only on the batch.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'round3')))
from common import *

S, G = load()
STYLE_A = ['H-SR', 'RESIN', 'BONKZ']   # long smoke, early, for a teammate
STYLE_B = ['HTDOG', 'VRTUS']           # cruiser smoke, selfish, stationary
MID = ['KITE']
A_NAME, B_NAME, K_NAME = 'Long smoke, early, for a teammate', 'Cruiser smoke, selfish, stationary', 'KITE (between)'
MAIN_MAPS = ['Sleeping Giant', 'Hotspot', 'Mountain Range', 'Land of Fire']
FWD_KM = 10.0  # a second destroyer counts as "forward of the smoke" if it is ahead of the smoke centre and within this distance of the smoke

TG = team_games(G)
GAMES = collections.defaultdict(list)
for k, t in TG: GAMES[t].append(k)
WL = win_loss(G)
BY_TEAM = by(S, 'team')

def smokes_of(teams): return [s for s in S if s['team'] in teams]
def tgs_of(teams): return [(k, t) for k, t in TG if t in teams]

def cruiser_dmg_share(ss):
    tot = sum(x['conc'] for s in ss for x in s['shooters']); cr = sum(x['conc'] for s in ss for x in s['shooters'] if x['cls'] == 'cruiser')
    return 100 * cr / tot if tot else None
def first_smoke(ss):
    """Median over team-games of the time of the team's first smoke (seconds)."""
    first = {}
    for s in ss:
        k = (s['game'], s['team']); first[k] = min(first.get(k, 9999), s['el'])
    return med(first.values())
def share(f): return lambda ss: pct(ss, f)
STATS = {
    'flank_lines_pct': share(lambda s: s['habit'] == 'flank smoke lines'),
    'cap_sitters_pct': share(lambda s: s['habit'] == 'cap sitters'),
    'parked_cruiser_pct': share(lambda s: s['habit'] == 'parked cruiser smoke'),
    'moving_exhaust_pct': share(lambda s: s['habit'] == 'moving exhaust'),
    'other_ship_pct': share(lambda s: s['habit'] == 'other'),
    'destroyer_smoke_pct': share(lambda s: s['cls'] == 'destroyer'),
    'long_dd_pct': share(lambda s: s['kind'] == 'long DD'),
    'stacked_pct': share(lambda s: s['coverage'] == 'stacked'),
    'screen_pct': share(lambda s: s['coverage'] == 'screen'),
    'selfish_pct': share(lambda s: s['coverage'] == 'selfish'),
    'stationary_pct': share(lambda s: s['movement'] == 'stationary'),
    'first_smoke_s': first_smoke,
    'cruiser_dmg_pct': cruiser_dmg_share,
    'early_pct': share(lambda s: s['el'] <= 300),
}
# features used for the style distance (each scaled to mean 0, sd 1 across the 24 clans with 7+ games)
FEATURES = ['flank_lines_pct', 'cap_sitters_pct', 'parked_cruiser_pct', 'moving_exhaust_pct', 'stacked_pct', 'selfish_pct', 'stationary_pct', 'first_smoke_s', 'cruiser_dmg_pct']

def numbers(teams):
    ss = smokes_of(teams); ng = sum(len(GAMES[t]) for t in teams)
    d = {k: f(ss) for k, f in STATS.items()}
    d.update(n_smokes=len(ss), n_games=ng, smokes_per_game=len(ss) / ng if ng else None,
             wins=sum(WL[t][0] for t in teams), losses=sum(WL[t][1] for t in teams))
    return d

def cast_numbers(teams):
    """Line-up per team-game from the rosters, and what stands near a destroyer's smoke at the moment it was fully laid."""
    dd, smk, smk_ca, radar = [], [], [], []
    for k, t in tgs_of(teams):
        pl = [p for p in G[k]['roster'].values() if p['team'] == t]
        dd.append(sum(p['ship_class'] == 'Destroyer' for p in pl))
        smk.append(sum(bool(p.get('smoke_variant')) for p in pl))
        smk_ca.append(sum(bool(p.get('smoke_variant')) and p['ship_class'] == 'Cruiser' for p in pl))
        radar.append(sum(bool(p.get('radar_m')) for p in pl))
    dds = [s for s in smokes_of(teams) if s['cls'] == 'destroyer']
    out = dict(n_team_games=len(dd), dd_per_game=mean(dd), dd_lineups={str(k): v for k, v in sorted(C(dd).items())}, smoke_ships_per_game=mean(smk),
               smoke_cruisers_per_game=mean(smk_ca), radar_ships_per_game=mean(radar), n_dd_smokes=len(dds))
    out.update(second_dd_fwd_pct=pct(dds, second_fwd), second_dd_alive_pct=pct(dds, other_dd_known),
               second_dd_fwd_pct_early=pct([s for s in dds if s['el'] <= 300], second_fwd), n_dd_smokes_early=sum(s['el'] <= 300 for s in dds),
               second_dd_fwd_any_dist_pct=pct(dds, lambda s: second_fwd(s, 1e9)),
               radar_cruiser_covered_pct=pct(dds, lambda s: s['radar_ca_any']))
    return out
def other_dds(s): return [c for c in s['cast'] if c['ally'] and c['cls'] == 'destroyer' and not c['is_smoker']]
def other_dd_known(s): return bool(other_dds(s))
def second_fwd(s, km=FWD_KM): return any(c['fwd_m'] > 0 and c['dist_m'] <= km * 1000 for c in other_dds(s))

def boot2(a, b, stat, reps=1000, cluster=lambda s: (s['team'], s['game'])):
    """95% interval of stat(a) - stat(b), resampling whole games (team-games) within each side."""
    ca, cb = by(a, cluster), by(b, cluster); ka, kb = list(ca), list(cb); out = []
    for _ in range(reps):
        va = stat([x for c in random.choices(ka, k=len(ka)) for x in ca[c]]); vb = stat([x for c in random.choices(kb, k=len(kb)) for x in cb[c]])
        if va is not None and vb is not None: out.append(va - vb)
    out.sort(); return (out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]) if out else (None, None)

CLANS7 = sorted(t for t in GAMES if len(GAMES[t]) >= 7)
CLAN_NUM = {t: numbers([t]) for t in GAMES}
def zvecs():
    mu = {f: mean(CLAN_NUM[t][f] for t in CLANS7) for f in FEATURES}
    sd = {f: statistics.pstdev([CLAN_NUM[t][f] for t in CLANS7]) or 1 for f in FEATURES}
    return {t: [(CLAN_NUM[t][f] - mu[f]) / sd[f] for f in FEATURES] for t in CLANS7}
Z = zvecs()
def dist(a, b): return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
def centroid(teams): return [mean(Z[t][i] for t in teams) for i in range(len(FEATURES))]
CA, CB = centroid(STYLE_A), centroid(STYLE_B)
def nearest(t):
    """Nearest style of a clan by distance to the two style centres (a clan inside a style is compared with the centre of the others)."""
    a = dist(Z[t], centroid([x for x in STYLE_A if x != t])); b = dist(Z[t], centroid([x for x in STYLE_B if x != t]))
    lab = 'between' if abs(a - b) / max(a, b) < 0.15 else ('long smoke' if a < b else 'cruiser smoke')
    return a, b, lab
