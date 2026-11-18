# Round 5, worker c1: C1 (cap defence, enemy took the cap) and C2 (cap holder at 8:00 and winning).
# Run: python -I -X utf8 c1_caps.py   (writes out-caps.md, enemy-took.csv, caps.json, figure c1-caps-8min)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
import random as _r
HERE_ = os.path.dirname(os.path.abspath(__file__))
S, G = load5()
random.seed(51)
OUT = []; J = {}
def P(*a):
    s = ' '.join(str(x) for x in a); OUT.append(s); print(s)
def pc(x, f='{:.1f}'): return '-' if x is None else f.format(x)
def share(key):
    return lambda ss: 100 * sum(1 for s in ss if key(s)) / len(ss) if ss else None
def row_share(ss, key):
    """n, share %, 95% interval (clans)."""
    st = share(key); lo, hi = boot_stat(ss, st)
    return len(ss), st(ss), lo, hi
def grp_rows(ss, key, label):
    top = [s for s in ss if s['grp'] == 'top']; rest = [s for s in ss if s['grp'] == 'rest']
    st = share(key); d = boot_diff(ss, st)
    a = row_share(ss, key); t = row_share(top, key); r = row_share(rest, key)
    rec = dict(what=label, n=a[0], pct=round(a[1], 1), ci=[round(a[2], 1), round(a[3], 1)], top6_n=t[0], top6_pct=round(t[1], 1), rest_n=r[0], rest_pct=round(r[1], 1),
               gap=round(t[1] - r[1], 1), gap_ci=[round(d[0], 1), round(d[1], 1)], gap_clear=d[0] * d[1] > 0)
    return [label, a[0], f'{a[1]:.1f}% ({a[2]:.1f} to {a[3]:.1f})', f'{t[1]:.1f}% (n {t[0]})', f'{r[1]:.1f}% (n {r[0]})', f'{t[1]-r[1]:+.1f} ({ci(d, "{:+.1f}")})'], rec

DD = [s for s in S if s['cls'] == 'destroyer']
SN = {k: snapshots(S, k) for k in G}

# ---------------------------------------------------------------- C1 part 1: cap_defended
P('# C1 part 1: cap_defended in the data\n')
rows = []; J['cap_defended'] = dict(rates=[])
for lab, ss in (('all smokes', S), ('destroyer smokes', DD), ('cruiser smokes', [s for s in S if s['cls'] == 'cruiser'])):
    r, rec = grp_rows(ss, lambda s: s['cap_def'], lab); rows.append(r); J['cap_defended']['rates'].append(rec)
P(md_table(['smokes', 'n', 'cap_defended set', 'Top 6', 'Rest', 'Top 6 - Rest'], rows))
D = [s for s in S if s['cap_def']]
for s in D:
    s['def_cap'] = s['r']['cap_defended']; g = G[s['game']]
    s['def_ncap'] = ncap_name(g, s['map'], s['side'], s['def_cap'])
    c = next(c for c in g['caps'] if c['cap'] == s['def_cap'])
    s['def_edge_m'] = (min(math.hypot(c['x'] - x, c['z'] - z) for x, z in s['path']) - c['r']) * WU - s['radius_m']
    x, z = norm(s['map'], s['side'], c['x'], c['z']); s['def_fwd_m'] = forward(s['map'], x, z)
    s['def_role'] = 'middle' if abs(s['def_fwd_m']) <= c['r'] * WU else 'enemy side' if s['def_fwd_m'] > 0 else 'own side'
    win = [x for x in SN[s['game']] if s['t0'] < x[0] <= s['t1'] + 60]
    own = [x[2].get(s['def_cap']) for x in win]
    s['def_lost'] = None if not win else any(o == s['opponent'] for o in own)
    s['def_last'] = None if not win else ('ours' if own[-1] == s['team'] else 'theirs' if own[-1] == s['opponent'] else 'neutral')
    s['def_own_act'] = {c['cap']: c['owner'] for c in s['j']['state_at_activate']['cap_state']}.get(s['def_cap']) == s['team']
P(f'\nSmokes with cap_defended: {len(D)} of {len(S)}. Role of the defended cap (team frame): {dict(C(s["def_role"] for s in D))}')
P(f'Defended cap is also the smoke\'s nearest cap (near_cap): {sum(s["def_cap"] == s["near_cap"] for s in D)} of {len(D)} ({pct(D, lambda s: s["def_cap"] == s["near_cap"]):.0f}%).'
  f' It is the batch\'s "contested cap": {sum(s["def_cap"] == s["cap"] for s in D)}.')
de = [s['def_edge_m'] for s in D]
P(f'Distance from the smoke edge to the defended cap edge: median {med(de):,.0f} m, quartiles {q(de,.25):,.0f} to {q(de,.75):,.0f} m; touching or inside the cap (<= 0 m): {sum(x <= 0 for x in de)}; more than 3 km away: {sum(x > 3000 for x in de)}; more than 6 km: {sum(x > 6000 for x in de)}.')
P(f'Defended cap was already ours at activation: {sum(s["def_own_act"] for s in D)} of {len(D)} (the rest became ours, then invaded, during the smoke).')
kn = [s for s in D if s['def_lost'] is not None]
rows = []; J['cap_defended']['kept'] = []
for lab, ss in (('all smokes with cap_defended', kn), ('destroyer smokes', [s for s in kn if s['cls'] == 'destroyer']), ('defended cap = nearest cap', [s for s in kn if s['def_cap'] == s['near_cap']]),
                ('defended cap not the nearest', [s for s in kn if s['def_cap'] != s['near_cap']])):
    r, rec = grp_rows(ss, lambda s: not s['def_lost'], lab); rows.append(r); J['cap_defended']['kept'].append(rec)
P('\nDefended cap still ours afterwards = no cap snapshot while the smoke stood or within 60 s after shows the enemy owning it.')
P(md_table(['group', 'n (with a snapshot)', 'never the enemy\'s', 'Top 6', 'Rest', 'Top 6 - Rest'], rows))
P(f'Owner of the defended cap at the last snapshot in the window: {dict(C(s["def_last"] for s in kn))}; no snapshot in window: {len(D) - len(kn)}.')
# longer horizon
for gr in (0, 120, 300):
    v = []
    for s in D:
        win = [x for x in SN[s['game']] if s['t0'] < x[0] <= s['t1'] + gr]
        if win: v.append(not any(x[2].get(s['def_cap']) == s['opponent'] for x in win))
    P(f'  grace {gr} s: kept {sum(v)} of {len(v)} ({100*sum(v)/len(v):.1f}%)')
J['cap_defended'].update(n=len(D), role=dict(C(s['def_role'] for s in D)), is_nearest=sum(s['def_cap'] == s['near_cap'] for s in D), median_edge_m=round(med(de)),
                         by_map_cap={f'{m} {c}': n for (m, c), n in sorted(C((s['map'], s['def_ncap']) for s in D).items())})
P('By map and (team-frame) cap:', J['cap_defended']['by_map_cap'])
# comparison: smokes without cap_defended, how often does the nearest cap (ours at activation) stay ours
base = [s for s in S if s['near_own'] == 'ours' and s['enemy_took'] is not None]
P(f'For comparison, any smoke whose nearest cap was ours at activation: enemy never took it in the window in {pct(base, lambda s: not s["enemy_took"]):.1f}% (n {len(base)}).')

# ---------------------------------------------------------------- C1 part 2: enemy_took validation
P('\n# C1 part 2: "enemy took the cap during the smoke" (r5lib enemy_took)\n')
def raw_states(gk):
    """Independent rebuild from the raw json clocks: (elapsed, kind, smoke id, {cap: owner})."""
    out = []
    for s in S:
        if s['game'] != gk: continue
        j = s['j']
        for kind, st, t in (('act', j['state_at_activate'], j['t_activate'] or j['t_created']), ('cap', j['state_at_capture'], j['t_capture'])):
            if st and t: out.append((1200 - secs(t['clock']), kind, s['id'], {c['cap']: c['owner'] for c in st['cap_state']}))
    return sorted(out, key=lambda x: x[0])
RAW = {k: raw_states(k) for k in G}
def my_took(s, grace=60, who='enemy'):
    g = G[s['game']]
    nc = min(g['caps'], key=lambda c: math.hypot(c['x'] - s['x'], c['z'] - s['z']) - c['r'])['cap']
    o0 = {c['cap']: c['owner'] for c in s['j']['state_at_activate']['cap_state']}.get(nc)
    t0 = 1200 - secs((s['j']['t_activate'] or s['j']['t_created'])['clock']); t1 = 1200 - secs(s['j']['t_dispersed']['clock']) if s['j']['t_dispersed'] else s['t1']
    win = [x for x in RAW[s['game']] if t0 < x[0] <= t1 + grace]
    side = s['opponent'] if who == 'enemy' else s['team']
    if o0 == side or not win: return None, len(win)
    return any(x[3].get(nc) == side for x in win), len(win)
mism = [s['id'] for s in S if my_took(s)[0] != s['enemy_took'] or my_took(s, who='we')[0] != s['we_took'] or my_took(s)[1] != s['took_window']]
P(f'Independent re-computation from the raw json (own code, json clocks instead of csv clocks): {len(S) - len(mism)} of {len(S)} smokes agree on enemy_took, we_took and the snapshot count; mismatches: {len(mism)}.')
cov = C('yes' if s['enemy_took'] else 'no' if s['enemy_took'] is False else 'n/a: cap already the enemy\'s' if s['near_own'] == 'theirs' else 'n/a: no snapshot' for s in S)
P('Coverage (all smokes):', dict(cov))
P('Owner of the nearest cap at activation:', dict(C(s['near_own'] for s in S)))
app = [s for s in S if s['enemy_took'] is not None]
tw = [s['took_window'] for s in app]
P(f'Snapshots in the window (applicable smokes, n {len(app)}): median {med(tw)}, quartiles {q(tw,.25):.0f} to {q(tw,.75):.0f}; only one snapshot: {sum(x == 1 for x in tw)} ({100*sum(x == 1 for x in tw)/len(tw):.0f}%).')
gaps = []; tails = []; lens = []
for s in app:
    ts = [s['t0']] + [x[0] for x in SN[s['game']] if s['t0'] < x[0] <= s['t1'] + 60]
    end = min(s['t1'] + 60, G[s['game']]['len'] or 1200)
    gaps.append(max(b - a for a, b in zip(ts, ts[1:]))); tails.append(max(0, end - ts[-1])); lens.append(end - s['t0'])
    s['_tail'] = tails[-1]; s['_len'] = lens[-1]
P(f'Window length: median {med(lens):.0f} s. Largest gap between two snapshots inside the window: median {med(gaps):.0f} s (quartiles {q(gaps,.25):.0f} to {q(gaps,.75):.0f}).')
P(f'Unobserved tail (last snapshot to the end of the window): median {med(tails):.0f} s, quartiles {q(tails,.25):.0f} to {q(tails,.75):.0f}; tail longer than 60 s: {sum(x > 60 for x in tails)} ({100*sum(x > 60 for x in tails)/len(tails):.0f}%). Share of the window covered up to the last snapshot: median {100*med([1 - t / l for t, l in zip(tails, lens) if l > 0]):.0f}%.')
# cross-check against the batch's cap_won (continuous cap history, +10 s grace): where cap_won is the nearest cap, we_took should be True
cw = [s for s in S if s['r']['cap_won'] and s['r']['cap_won'] == s['near_cap']]
P(f'Cross-check with the batch field cap_won (built from the continuous cap history, 10 s grace): cap_won names the nearest cap in {len(cw)} smokes; we_took says yes in {sum(s["we_took"] is True for s in cw)}, no in {sum(s["we_took"] is False for s in cw)}, n/a in {sum(s["we_took"] is None for s in cw)}.')
for gr in (0, 10, 60):
    P(f'   with a {gr} s grace: yes {sum(my_took(s, gr, "we")[0] is True for s in cw)}, no {sum(my_took(s, gr, "we")[0] is False for s in cw)}, n/a {sum(my_took(s, gr, "we")[0] is None for s in cw)}')
miss = [s for s in cw if s['we_took'] is False]
P('   cap_won but we_took = no (flip not seen in any snapshot, i.e. it flipped back or the window is sparse):', [(s['slug'], s['took_window']) for s in miss][:12])
rows = []; J['enemy_took'] = dict(grace=[])
for gr in (0, 60, 120):
    v = [my_took(s, gr)[0] for s in S]; w = [my_took(s, gr, 'we')[0] for s in S]
    y, n_, na = sum(x is True for x in v), sum(x is False for x in v), sum(x is None for x in v)
    rows.append([f'{gr} s', y, n_, na, f'{100*y/(y+n_):.1f}%', sum(x is True for x in w), sum(x is False for x in w), f'{100*sum(x is True for x in w)/sum(x is not None for x in w):.1f}%'])
    J['enemy_took']['grace'].append(dict(grace_s=gr, yes=y, no=n_, na=na, pct=round(100 * y / (y + n_), 1)))
P('\nGrace after the smoke clears:'); P(md_table(['grace', 'enemy took: yes', 'no', 'n/a', 'yes share', 'we took: yes', 'no', 'yes share'], rows))
# hand check list
P('\nHand check: 10 smokes (seeded sample: 4 yes, 4 no, 2 n/a). Every raw cap state of the game from 30 s before activation to 90 s after the window.')
rr = _r.Random(7); pick = rr.sample([s for s in S if s['enemy_took'] is True], 4) + rr.sample([s for s in S if s['enemy_took'] is False], 4) + rr.sample([s for s in S if s['enemy_took'] is None], 2)
HC = []
for s in pick:
    P(f'\n- {s["slug"]} {s["team"]} vs {s["opponent"]} on {s["map"]}; nearest cap {s["near_cap"]} ({s["near_cap_edge_m"]:,.0f} m to its edge), owner at activation: {s["near_own"]}; smoke {s["t0"]} to {s["t1"]} s, window to {s["t1"]+60} s; library enemy_took = {s["enemy_took"]}, snapshots in window = {s["took_window"]}')
    seq = []
    for t, kind, sid, own in RAW[s['game']]:
        if s['t0'] - 30 <= t <= s['t1'] + 150:
            o = own.get(s['near_cap']); o = 'neutral' if o is None else 'ENEMY' if o == s['opponent'] else 'ours'
            seq.append(f'{t}{"*" if s["t0"] < t <= s["t1"] + 60 else ""}:{o}')
    P('  ' + '  '.join(seq) + '   (* = inside the window)')
    inwin = [x.split(':')[1] for x in seq if '*' in x]
    hand = None if s['near_own'] == 'theirs' or not inwin else 'ENEMY' in inwin
    HC.append(hand == s['enemy_took']); P(f'  by hand: {hand} -> {"agrees" if hand == s["enemy_took"] else "DISAGREES"}')
P(f'\nHand check agreement: {sum(HC)} of {len(HC)}.')
# how far is the nearest cap
ne = [s['near_cap_edge_m'] for s in S]
P(f'\nDistance from smoke centre to the nearest cap edge: median {med(ne):,.0f} m; inside the cap: {sum(x <= 0 for x in ne)}; within 2 km: {sum(x <= 2000 for x in ne)}; more than 5 km away: {sum(x > 5000 for x in ne)}.')
NEAR = lambda s: s['near_cap_edge_m'] <= 2000
# summary tables
rows = []; J['enemy_took']['overall'] = []
for lab, ss in (('all applicable smokes', app), ('destroyer smokes', [s for s in app if s['cls'] == 'destroyer']), ('smoke centre inside or within 2 km of the cap', [s for s in app if NEAR(s)]),
                ('destroyer smokes inside or within 2 km', [s for s in app if NEAR(s) and s['cls'] == 'destroyer']),
                ('cap ours at activation', [s for s in app if s['near_own'] == 'ours']), ('cap neutral at activation', [s for s in app if s['near_own'] == 'neutral']),
                ('cap ours, smoke within 2 km', [s for s in app if s['near_own'] == 'ours' and NEAR(s)]),
                ('cap ours, cap_defended set for that cap', [s for s in app if s['near_own'] == 'ours' and s['r']['cap_defended'] == s['near_cap']]),
                ('cap ours, cap_defended not set for it', [s for s in app if s['near_own'] == 'ours' and s['r']['cap_defended'] != s['near_cap']])):
    r, rec = grp_rows(ss, lambda s: s['enemy_took'], lab); rows.append(r); J['enemy_took']['overall'].append(rec)
P('\nEnemy took the nearest cap (window = smoke life + 60 s). Cap already the enemy\'s and no-snapshot smokes are excluded.')
P(md_table(['group', 'n', 'enemy took it', 'Top 6', 'Rest', 'Top 6 - Rest'], rows))
rows = []; J['enemy_took']['by_map_cap'] = []
for (m, c), ss in sorted(by(app, lambda s: (s['map'], s['near_ncap'])).items()):
    if len(ss) < 8: rows.append([m, c, len(ss), 'too few', '', '', '']); continue
    r, rec = grp_rows(ss, lambda s: s['enemy_took'], f'{m} {c}')
    tn, rn = rec['top6_n'], rec['rest_n']
    rows.append([m, c, f'{len(ss)}{small(len(ss))}', r[2], r[3] if tn >= 8 else f'too few (n {tn})', r[4] if rn >= 8 else f'too few (n {rn})', r[5] if tn >= 8 and rn >= 8 else '-'])
    rec.update(map=m, cap=c); J['enemy_took']['by_map_cap'].append(rec)
P('\nBy map and cap (cap letter in the team frame):'); P(md_table(['map', 'cap', 'n', 'enemy took it', 'Top 6', 'Rest', 'Top 6 - Rest'], rows))
rows = []; J['we_took'] = []
wapp = [s for s in S if s['we_took'] is not None]
for lab, ss in (('all smokes where the nearest cap was not ours', wapp), ('destroyer smokes', [s for s in wapp if s['cls'] == 'destroyer']), ('within 2 km', [s for s in wapp if NEAR(s)])):
    r, rec = grp_rows(ss, lambda s: s['we_took'], lab); rows.append(r); J['we_took'].append(rec)
P('\nFor reference, "we took the nearest cap" (cap not ours at activation):'); P(md_table(['group', 'n', 'we took it', 'Top 6', 'Rest', 'Top 6 - Rest'], rows))
with open(os.path.join(HERE_, 'enemy-took.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['match_id', 'game_no', 'smoke_id', 'team', 'group', 'smoker_class', 'map', 'nearest_cap', 'nearest_cap_team_frame', 'edge_distance_m', 'owner_at_activation', 'enemy_took', 'we_took', 'snapshots_in_window', 'cap_defended', 'cap_won'])
    tf = lambda v: '' if v is None else 'yes' if v else 'no'
    for s in S:
        w.writerow([s['r']['match_id'], s['r']['game_no'], s['id'], s['team'], 'Top 6' if s['grp'] == 'top' else 'Rest', s['cls'], s['map'], s['near_cap'], s['near_ncap'], round(s['near_cap_edge_m']), s['near_own'],
                    tf(s['enemy_took']), tf(s['we_took']), s['took_window'], s['r']['cap_defended'], s['r']['cap_won']])
P(f'\nWrote enemy-took.csv ({len(S)} rows).')
J['enemy_took'].update(coverage=dict(cov), median_snapshots=med(tw), median_tail_s=med(tails), hand_check=f'{sum(HC)} of {len(HC)}', recompute_mismatches=len(mism),
                       cap_won_crosscheck=dict(n=len(cw), yes=sum(s['we_took'] is True for s in cw), no=sum(s['we_took'] is False for s in cw), na=sum(s['we_took'] is None for s in cw)))
J['ribbons'] = dict(in_replay='self player only (onRibbon ids 9 Defended, 10 Captured, 11 AssistedInCapture; modern replays: privateVehicleState.ribbons)', in_batch=False,
                    replays_per_game=dict(C(1 + len(g['j']['merged_replays']) for g in G.values())), needs='code change in smoke-signals plus a batch rerun; even then at most the recording players (2 of ~18 ships per game)')
P('\nReplays per game (primary + merged):', J['ribbons']['replays_per_game'])

# ---------------------------------------------------------------- C2
P('\n# C2: cap holder at 8:00 and winning\n')
wl = win_loss(G)
def p_simple(g, t):
    o = next(x for x in g['teams'] if x != t)
    def odds(c):
        w, l = wl[c]; w -= g['winner'] == c; l -= g['winner'] != c
        return (w + 1) / (l + 1)
    a, b = odds(t), odds(o); return a / (a + b)
def bt_fit(games, clans, iters=60):
    """Bradley-Terry strengths with one virtual win and one virtual loss against an average (strength 1) team."""
    st = {c: 1.0 for c in clans}
    w = C(g['winner'] for g in games); opp = collections.defaultdict(list)
    for g in games:
        a, b = g['teams']; opp[a].append(b); opp[b].append(a)
    for _ in range(iters):
        new = {}
        for c in clans:
            den = sum(1 / (st[c] + st[o]) for o in opp[c]) + 2 / (st[c] + 1)
            new[c] = (w[c] + 1) / den
        st = new
    return st
clans = sorted(wl); GL = list(G.values())
P_BT = {}
for g in GL:
    st = bt_fit([x for x in GL if x is not g], clans); a, b = g['teams']
    P_BT[(g['key'], a)] = st[a] / (st[a] + st[b]); P_BT[(g['key'], b)] = st[b] / (st[a] + st[b])
def role_of(mapname, g, side, cap):
    c = next(c for c in g['caps'] if c['cap'] == cap); x, z = norm(mapname, side, c['x'], c['z']); f = forward(mapname, x, z)
    lat = ((x - z) / math.sqrt(2) if mapname in DIAGONAL else x) * WU
    return ('middle' if abs(f) <= c['r'] * WU else 'enemy side' if f > 0 else 'own side'), f, lat
TG = []; cover = collections.defaultdict(lambda: C()); snapgap = []
for g in GL:
    m = g['map']
    if g['len'] is not None and g['len'] < 480: cover[m]['ended before 8:00'] += 1; continue
    h = cap_holders(S, G, g['key'], 480, 60)
    if h is None: cover[m]['no snapshot within 60 s'] += 1; continue
    cover[m]['covered'] += 1
    snapgap.append(min(abs(x[0] - 480) for x in SN[g['key']]))
    cnt = C(o for o in h.values() if o)
    for t in g['teams']:
        o = next(x for x in g['teams'] if x != t)
        holds = {ncap_name(g, m, g['sides'][t], c): (own == t) for c, own in h.items()}
        ehold = {ncap_name(g, m, g['sides'][t], c): (own == o) for c, own in h.items()}
        TG.append(dict(game=g['key'], team=t, opp=o, map=m, win=int(g['winner'] == t), p=p_simple(g, t), pbt=P_BT[(g['key'], t)], holds=holds, ehold=ehold, n_held=cnt[t], n_enemy=cnt[o],
                       rr=t not in TOP and o not in TOP, top=t in TOP))
P(md_table(['map', 'games', 'covered at 8:00 (snapshot within 60 s)', 'ended before 8:00', 'no snapshot within 60 s'],
           [[m, sum(v.values()), v['covered'], v['ended before 8:00'], v['no snapshot within 60 s']] for m, v in sorted(cover.items())] +
           [['all', len(GL), sum(v['covered'] for v in cover.values()), sum(v['ended before 8:00'] for v in cover.values()), sum(v['no snapshot within 60 s'] for v in cover.values())]]))
P(f'Distance of the snapshot used from 8:00: median {med(snapgap):.0f} s, max {max(snapgap)} s. Covered games where both clans are Rest: {sum(t["rr"] for t in TG)//2}; games with a Top 6 clan: {sum(not t["rr"] for t in TG)//2}.')
# model check
fav = [t for t in TG if t['p'] > 0.5]; favb = [t for t in TG if t['pbt'] > 0.5]
allg = [dict(win=int(g['winner'] == t), p=p_simple(g, t), pbt=P_BT[(g['key'], t)]) for g in GL for t in g['teams']]
P(f'Team strength model check (all 171 games): the favourite by the simple record model won {sum(x["win"] for x in allg if x["p"] > .5)} of {sum(x["p"] > .5 for x in allg)}; mean predicted for those {mean(x["p"] for x in allg if x["p"] > .5):.2f}. '
  f'Bradley-Terry: favourite won {sum(x["win"] for x in allg if x["pbt"] > .5)} of {sum(x["pbt"] > .5 for x in allg)}, mean predicted {mean(x["pbt"] for x in allg if x["pbt"] > .5):.2f}.')
def wr(xs): return 100 * mean(x['win'] for x in xs) if xs else None
def c2row(label, tg, hold, nothold=None):
    H = [x for x in tg if hold(x)]; N = [x for x in tg if (nothold(x) if nothold else not hold(x))]
    if len(H) < 8: return [label, len(H), 'too few', '', '', '', '', ''], dict(what=label, n_holders=len(H), too_few=True)
    def st_w(xs): return wr([x for x in xs if hold(x)])
    def st_d(xs):
        a = [x for x in xs if hold(x)]; b = [x for x in xs if (nothold(x) if nothold else not hold(x))]
        return wr(a) - wr(b) if a and b else None
    def st_e(xs):
        a = [x for x in xs if hold(x)]; return 100 * mean(x['win'] - x['p'] for x in a) if a else None
    def st_eb(xs):
        a = [x for x in xs if hold(x)]; return 100 * mean(x['win'] - x['pbt'] for x in a) if a else None
    cw_, cd, ce, ceb = (boot_stat(tg, f, cluster='game') for f in (st_w, st_d, st_e, st_eb))
    wins = sum(x['win'] for x in H); ex = sum(x['p'] for x in H); exb = sum(x['pbt'] for x in H)
    rec = dict(what=label, n_holders=len(H), small_n=len(H) < 15, holder_wins=wins, holder_win_pct=round(wr(H), 1), holder_ci=[round(cw_[0], 1), round(cw_[1], 1)],
               n_not=len(N), not_win_pct=round(wr(N), 1) if N else None, gap=round(st_d(tg), 1) if N else None, gap_ci=[round(cd[0], 1), round(cd[1], 1)] if cd[0] is not None else None,
               expected_wins=round(ex, 1), actual_minus_expected_pts=round(st_e(tg), 1), ame_ci=[round(ce[0], 1), round(ce[1], 1)], ame_clear=ce[0] * ce[1] > 0,
               expected_wins_bt=round(exb, 1), ame_bt_pts=round(st_eb(tg), 1), ame_bt_ci=[round(ceb[0], 1), round(ceb[1], 1)], ame_bt_clear=ceb[0] * ceb[1] > 0)
    return [label, f'{len(H)}{small(len(H))}', f'{wins} ({wr(H):.0f}%, {cw_[0]:.0f} to {cw_[1]:.0f})', f'{wr(N):.0f}% (n {len(N)})' if N else '-', f'{st_d(tg):+.0f} ({ci(cd, "{:+.0f}")})' if N and cd[0] is not None else '-',
            f'{ex:.1f}', f'{st_e(tg):+.0f} pts ({ci(ce, "{:+.0f}")})', f'{exb:.1f}; {st_eb(tg):+.0f} pts ({ci(ceb, "{:+.0f}")})'], rec
HDR = ['cap (team frame)', 'holder team-games', 'holders won (rate, interval)', 'not holding: win rate', 'holding - not', 'team strength predicts (wins)', 'actual - expected', 'Bradley-Terry: expected; actual - expected']
J['c2'] = dict(coverage={m: dict(v) for m, v in cover.items()}, maps={}, model='simple: leave-this-game-out record, odds a = (wins+1)/(losses+1), p = a/(a+b). Check: Bradley-Terry strengths fitted without the game, one virtual win and loss vs an average team.')
more = lambda x: x['n_held'] > x['n_enemy']; fewer = lambda x: x['n_held'] < x['n_enemy']
ROLE = {}
for m in sorted(cover):
    tg = [x for x in TG if x['map'] == m]
    if not tg: continue
    g = next(g for g in GL if g['map'] == m)
    caps = sorted({c for x in tg for c in x['holds']})
    P(f'\n## {m}  ({len(tg)//2} games covered, {sum(x["rr"] for x in tg)//2} Rest-vs-Rest)')
    desc = []
    for c in caps:
        ro, f, lat = role_of(m, g, 'south', c); ROLE[(m, c)] = ro
        desc.append(f'{c}: {ro} ({f/1000:+.1f} km toward the enemy, {"left" if lat < -500 else "right" if lat > 500 else "centre"})')
    P('Caps in the team frame (own spawn at the bottom): ' + '; '.join(desc))
    J['c2']['maps'][m] = dict(games=len(tg) // 2, rest_vs_rest_games=sum(x['rr'] for x in tg) // 2, caps={c: ROLE[(m, c)] for c in caps}, all=[], rest_vs_rest=[])
    for lab, sub, key in (('All covered games', tg, 'all'), ('(a) Rest-vs-Rest games only', [x for x in tg if x['rr']], 'rest_vs_rest')):
        rows = []
        for c in caps:
            r, rec = c2row(f'{c} ({ROLE[(m, c)]})', sub, lambda x, c=c: x['holds'].get(c)); rows.append(r); J['c2']['maps'][m][key].append(rec)
        r, rec = c2row('holds more caps than the enemy', sub, more, fewer); rows.append(r); J['c2']['maps'][m][key].append(rec)
        P(f'\n{lab} ({len(sub)//2} games):'); P(md_table(HDR, rows))
P('\n## All maps pooled, by the cap\'s place in the team frame')
J['c2']['pooled'] = dict(all=[], rest_vs_rest=[])
def any_role(ro): return lambda x: any(v and ROLE[(x['map'], c)] == ro for c, v in x['holds'].items())
def all_role(ro): return lambda x: all(v for c, v in x['holds'].items() if ROLE[(x['map'], c)] == ro) and any(ROLE[(x['map'], c)] == ro for c in x['holds'])
def enemy_role(ro): return lambda x: any(v and ROLE[(x['map'], c)] == ro for c, v in x['ehold'].items())
for lab, sub, key in (('All covered games', TG, 'all'), ('(a) Rest-vs-Rest games only', [x for x in TG if x['rr']], 'rest_vs_rest')):
    rows = []
    for nm, f in (('holds its own-side cap (maps that have one)', any_role('own side')), ('holds the enemy-side cap (maps that have one)', any_role('enemy side')),
                  ('holds at least one middle cap', any_role('middle')), ('holds every middle cap', all_role('middle')),
                  ('holds more caps than the enemy', more), ('holds 2+ more caps than the enemy', lambda x: x['n_held'] >= x['n_enemy'] + 2)):
        if nm.startswith('holds more'): r, rec = c2row(nm, sub, f, fewer)
        else: r, rec = c2row(nm, sub, f)
        rows.append(r); J['c2']['pooled'][key].append(rec)
    P(f'\n{lab} ({len(sub)//2} games):'); P(md_table(HDR, rows))
tie = sum(1 for x in TG if x['n_held'] == x['n_enemy']) // 2
P(f'\nGames level on caps at 8:00: {tie} of {len(TG)//2}. Caps held at 8:00 per team: {dict(sorted(C(x["n_held"] for x in TG).items()))}')
# who holds more caps: Top 6?
tr = [x for x in TG if x['top'] != (x['opp'] in TOP)]
P(f'In Top 6 vs Rest games covered ({len(tr)//2}): the Top 6 clan held more caps at 8:00 in {sum(more(x) for x in tr if x["top"])}, fewer in {sum(fewer(x) for x in tr if x["top"])}; Top 6 won {sum(x["win"] for x in tr if x["top"])}.')
# score lead at 8:00 as "already winning" check
lead = []
for x in TG:
    sn = min(SN[x['game']], key=lambda y: abs(y[0] - 480)); sc = sn[1]
    x['lead'] = sc.get(x['team'], 0) - sc.get(x['opp'], 0)
ml = [x for x in TG if more(x)]
P(f'Teams holding more caps at 8:00 were already ahead on score at that moment in {sum(x["lead"] > 0 for x in ml)} of {len(ml)} ({100*sum(x["lead"] > 0 for x in ml)/len(ml):.0f}%); median lead {med([x["lead"] for x in ml]):+.0f} points.')
ah = [x for x in TG if x['lead'] > 0]
P(f'Reference: the team ahead on score at 8:00 won {sum(x["win"] for x in ah)} of {len(ah)} ({wr(ah):.0f}%).')
J['c2']['notes'] = dict(level_on_caps_games=tie, more_caps_already_ahead_pct=round(100 * sum(x['lead'] > 0 for x in ml) / len(ml)), score_leader_win_pct=round(wr(ah)))

# figure: per map, holder win rate minus expected
rowsf = []
for m, d in J['c2']['maps'].items():
    for rec in d['all']:
        if not rec.get('too_few'): rowsf.append((m, rec))
fig = Fig(1100, 70 + 21 * len(rowsf) + 60, 'C2 working figure: teams holding a cap at 8:00, actual win rate minus what team strength predicts',
          'Points of win rate, all covered games. Dot = estimate, line = 95% interval (games resampled). Solid = interval excludes zero.')
x0, wpx, y = 360, 600, 80; sc = lambda v: x0 + wpx / 2 + v * (wpx / 2) / 60
for v in (-60, -40, -20, 0, 20, 40, 60):
    fig.add(f'<line x1="{sc(v):.1f}" y1="70" x2="{sc(v):.1f}" y2="{y + 21 * len(rowsf)}" stroke="{GRID if v else MUTED}" stroke-width="1"/>' + T(sc(v), y + 21 * len(rowsf) + 14, f'{v:+d}', size=10))
for m, rec in rowsf:
    v, (lo, hi) = rec['actual_minus_expected_pts'], rec['ame_ci']; clear = rec['ame_clear']
    fig.add(T(x0 - 8, y + 12, f'{m}: {rec["what"]} (n {rec["n_holders"]})', size=11, fill=INK, anchor='end'))
    fig.add(f'<line x1="{sc(max(-60, lo)):.1f}" y1="{y+8}" x2="{sc(min(60, hi)):.1f}" y2="{y+8}" stroke="{INK}" stroke-width="1.2"/>')
    fig.add(f'<circle cx="{sc(v):.1f}" cy="{y+8}" r="4.5" fill="{VIOLET if clear else BG}" stroke="{VIOLET}" stroke-width="1.5"/>')
    y += 21
fig.save(os.path.join(R5, 'figures', 'c1-caps-8min'))
open(os.path.join(HERE_, 'out-caps.md'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
json.dump(J, open(os.path.join(HERE_, 'caps.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
print('done')
