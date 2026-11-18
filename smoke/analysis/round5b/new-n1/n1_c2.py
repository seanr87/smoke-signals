# Round 5b, worker n1: C2 (cap holder at exactly 8:00 and winning) from the cap timeline, all 171 games.
# Method copied from round 5 part-c1/c1_caps.py; only the source of the cap owners changes.
# Run: python -I -X utf8 n1_c2.py   (writes out-c2.md, c2.json, figure n1-caps-8min)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
HERE_ = os.path.dirname(os.path.abspath(__file__))
S, G = load5(); add_times(S)
random.seed(51)
OUT = []; J = {}
def P(*a):
    s = ' '.join(str(x) for x in a); OUT.append(s); print(s)
_old = os.path.join(ROOT, 'smoke', 'analysis', 'round5', 'part-c1', 'caps.json')
OLD = json.load(open(_old if os.path.exists(_old) else os.path.join(R5, 'part-c1', 'caps.json'), encoding='utf-8'))['c2']

P('# C2 from the cap timeline: cap holder at exactly 8:00 and winning (round 5b, worker n1)\n')
wl = win_loss(G)
def p_simple(g, t):
    o = next(x for x in g['teams'] if x != t)
    def odds(c):
        w, l = wl[c]; w -= g['winner'] == c; l -= g['winner'] != c
        return (w + 1) / (l + 1)
    a, b = odds(t), odds(o); return a / (a + b)
def bt_fit(games, clans, iters=60):
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

T8 = 480
END = {k: max(t for ev in TL(k).score.values() for t, _ in ev) for k in G}
def holders(k, t):
    g = TL(k); return {c['cap']: g.owner_at(c['cap'], t) for c in G[k]['caps']}
def lead_at(k, team, opp, t):
    h = holders(k, t); return sum(o == team for o in h.values()) - sum(o == opp for o in h.values())
def time_shares(k, team, opp, t1=T8):
    """Share of [0, t1] during which team held more / fewer caps than opp."""
    g = TL(k); ts = sorted({0.0, float(t1)} | {t for ev in g.caps.values() for t, _, _ in ev if 0 < t < t1})
    more = fewer = 0.0
    for a, b in zip(ts, ts[1:]):
        d = lead_at(k, team, opp, a)
        if d > 0: more += b - a
        elif d < 0: fewer += b - a
    return more / t1, fewer / t1
def team_rows(g, t, h):
    out = []; m = g['map']; cnt = C(o for o in h.values() if o)
    for tm in g['teams']:
        o = next(x for x in g['teams'] if x != tm)
        holds = {ncap_name(g, m, g['sides'][tm], c): (own == tm) for c, own in h.items()}
        ehold = {ncap_name(g, m, g['sides'][tm], c): (own == o) for c, own in h.items()}
        out.append(dict(game=g['key'], team=tm, opp=o, map=m, win=int(g['winner'] == tm), p=p_simple(g, tm), pbt=P_BT[(g['key'], tm)], holds=holds, ehold=ehold, n_held=cnt[tm], n_enemy=cnt[o],
                        rr=tm not in TOP and o not in TOP, top=tm in TOP))
    return out
TG = []; SHORT = []; cover = collections.defaultdict(lambda: C()); fm = 0
for g in GL:
    k = g['key']; m = g['map']; tl = TL(k)
    for tm in g['teams']:
        for c in g['caps']:
            fm += tl.frame_letter(tm, c['cap']) != ncap_name(g, m, g['sides'][tm], c['cap'])
    if END[k] < T8:
        cover[m]['ended before 8:00'] += 1; SHORT += team_rows(g, END[k], holders(k, END[k])); continue
    cover[m]['covered'] += 1
    rows = team_rows(g, T8, holders(k, T8))
    for x in rows:
        x['lead300'] = lead_at(k, x['team'], x['opp'], 300)
        x['lead600'] = lead_at(k, x['team'], x['opp'], 600) if END[k] >= 600 else None
        x['sh_more'], x['sh_fewer'] = time_shares(k, x['team'], x['opp'])
        x['lead'] = tl.score_at(x['team'], T8) - tl.score_at(x['opp'], T8)
    TG += rows
P(f'Team-frame cap letters, timeline file vs the round 5 geometry: {fm} mismatches.')
P(md_table(['map', 'games', 'in the main table (still running at 8:00, owner read at elapsed 480 s)', 'ended before 8:00'],
           [[m, sum(v.values()), v['covered'], v['ended before 8:00']] for m, v in sorted(cover.items())] +
           [['all', len(GL), sum(v['covered'] for v in cover.values()), sum(v['ended before 8:00'] for v in cover.values())]]))
NG = len(TG) // 2
P(f'Round 5 covered {sum(v.get("covered", 0) for v in OLD["coverage"].values())} games; now {NG}. Rest-vs-Rest games in the main table: {sum(t["rr"] for t in TG)//2}; games with a Top 6 clan: {sum(not t["rr"] for t in TG)//2}.')
P('Games that ended before 8:00 (kept out of the main table): ' + '; '.join(f'{k[0].split("_")[1]} g{k[1]} {G[k]["map"]} {" v ".join(G[k]["teams"])} ended {END[k]:.0f} s' for k in sorted(G, key=lambda k: END[k]) if END[k] < T8))

# compare with the round 5 snapshot holders, game by game
same = diff = 0; r5cov = 0; difflist = []; clock15 = []
for g in GL:
    k = g['key']
    sm = [s for s in S if s['game'] == k]
    if sm and abs((sm[0]['e0'] - sm[0]['el'])) > 100: clock15.append(k)
    if g['len'] is not None and g['len'] < 480: continue
    h5 = cap_holders(S, G, k, 480, 60)
    if h5 is None: continue
    r5cov += 1
    if END[k] < T8: difflist.append((k, 'ended before 8:00 by the timeline')); diff += 1; continue
    h = holders(k, T8); nd = sum(h5.get(c) != h[c] for c in h)
    if nd: diff += 1; difflist.append((k, f'{nd} cap(s) differ'))
    else: same += 1
P(f'\nGame by game against round 5: of the {r5cov} games round 5 covered, the cap owners at 8:00 are the same in {same} and differ in {diff}: ' +
  '; '.join(f'{k[0].split("_")[1]} g{k[1]} ({G[k]["map"]}, {w})' for k, w in difflist) + '.')
P(f'Games whose HUD clock started at 15:00 instead of 20:00: {len(clock15)} ({"; ".join(f"{k[0].split(chr(95))[1]} g{k[1]}" for k in clock15)}). Round 5 computed elapsed time as 20:00 minus the clock, so in these games its "8:00" was really 3:00. The timeline uses true elapsed seconds.')
J['coverage'] = {m: dict(v) for m, v in cover.items()}
J['vs_round5'] = dict(round5_games=r5cov, same_owners=same, differ=diff, differ_list=[f'{k[0]} g{k[1]}: {w}' for k, w in difflist], clock_15min_games=[f'{k[0]} g{k[1]}' for k in clock15], games_now=NG, games_added=NG - (r5cov - sum(1 for k, w in difflist if w.startswith('ended'))))

allg = [dict(win=int(g['winner'] == t), p=p_simple(g, t), pbt=P_BT[(g['key'], t)]) for g in GL for t in g['teams']]
P(f'\nTeam strength model check (all 171 games, unchanged from round 5): the favourite by the simple record model won {sum(x["win"] for x in allg if x["p"] > .5)} of {sum(x["p"] > .5 for x in allg)}; mean predicted {mean(x["p"] for x in allg if x["p"] > .5):.2f}. '
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
def oldtxt(o):
    if not o: return 'not in round 5'
    if o.get('too_few'): return f'too few (n {o["n_holders"]})'
    return f'n {o["n_holders"]}, won {o["holder_wins"]} ({o["holder_win_pct"]:.0f}%), {o["actual_minus_expected_pts"]:+.0f} pts ({o["ame_ci"][0]:+.0f} to {o["ame_ci"][1]:+.0f}){" *" if o["ame_clear"] else ""}'
J.update(maps={}, model='simple: leave-this-game-out record, odds a = (wins+1)/(losses+1), p = a/(a+b). Check: Bradley-Terry strengths fitted without the game, one virtual win and loss vs an average team.')
more = lambda x: x['n_held'] > x['n_enemy']; fewer = lambda x: x['n_held'] < x['n_enemy']
ROLE = {}; MOVED = []
def track(scope, key, rec, o):
    rec['round5'] = o
    MOVED.append(dict(scope=scope, games=key, what=rec['what'], new=rec, old=o))
for m in sorted(cover):
    tg = [x for x in TG if x['map'] == m]
    if not tg: continue
    g = next(g for g in GL if g['map'] == m)
    caps = sorted({c for x in tg for c in x['holds']})
    om = OLD['maps'].get(m, {})
    P(f'\n## {m}  ({len(tg)//2} games, {sum(x["rr"] for x in tg)//2} Rest-vs-Rest; round 5: {om.get("games")} and {om.get("rest_vs_rest_games")})')
    desc = []
    for c in caps:
        ro, f, lat = role_of(m, g, 'south', c); ROLE[(m, c)] = ro
        desc.append(f'{c}: {ro} ({f/1000:+.1f} km toward the enemy, {"left" if lat < -500 else "right" if lat > 500 else "centre"})')
    P('Caps in the team frame (own spawn at the bottom): ' + '; '.join(desc))
    J['maps'][m] = dict(games=len(tg) // 2, rest_vs_rest_games=sum(x['rr'] for x in tg) // 2, caps={c: ROLE[(m, c)] for c in caps}, all=[], rest_vs_rest=[])
    for lab, sub, key in (('All games', tg, 'all'), ('(a) Rest-vs-Rest games only', [x for x in tg if x['rr']], 'rest_vs_rest')):
        rows = []; oo = {x['what']: x for x in om.get(key, [])}
        for c in caps:
            r, rec = c2row(f'{c} ({ROLE[(m, c)]})', sub, lambda x, c=c: x['holds'].get(c)); track(m, key, rec, oo.get(rec['what'])); rows.append(r + [oldtxt(oo.get(rec['what']))]); J['maps'][m][key].append(rec)
        r, rec = c2row('holds more caps than the enemy', sub, more, fewer); track(m, key, rec, oo.get(rec['what'])); rows.append(r + [oldtxt(oo.get(rec['what']))]); J['maps'][m][key].append(rec)
        P(f'\n{lab} ({len(sub)//2} games):'); P(md_table(HDR + ['round 5 (snapshot)'], rows))
P('\n## All maps pooled, by the cap\'s place in the team frame')
J['pooled'] = dict(all=[], rest_vs_rest=[])
def any_role(ro): return lambda x: any(v and ROLE[(x['map'], c)] == ro for c, v in x['holds'].items())
def all_role(ro): return lambda x: all(v for c, v in x['holds'].items() if ROLE[(x['map'], c)] == ro) and any(ROLE[(x['map'], c)] == ro for c in x['holds'])
for lab, sub, key in (('All games', TG, 'all'), ('(a) Rest-vs-Rest games only', [x for x in TG if x['rr']], 'rest_vs_rest')):
    rows = []; oo = {x['what']: x for x in OLD['pooled'][key]}
    for nm, f in (('holds its own-side cap (maps that have one)', any_role('own side')), ('holds the enemy-side cap (maps that have one)', any_role('enemy side')),
                  ('holds at least one middle cap', any_role('middle')), ('holds every middle cap', all_role('middle')),
                  ('holds more caps than the enemy', more), ('holds 2+ more caps than the enemy', lambda x: x['n_held'] >= x['n_enemy'] + 2)):
        if nm.startswith('holds more'): r, rec = c2row(nm, sub, f, fewer)
        else: r, rec = c2row(nm, sub, f)
        track('pooled', key, rec, oo.get(nm)); rows.append(r + [oldtxt(oo.get(nm))]); J['pooled'][key].append(rec)
    P(f'\n{lab} ({len(sub)//2} games):'); P(md_table(HDR + ['round 5 (snapshot)'], rows))
J['moved'] = MOVED

# ---- new reference rows from the timeline
P('\n## New reference rows from the timeline')
J['reference'] = dict(all=[], rest_vs_rest=[])
T10 = [x for x in TG if x['lead600'] is not None]
for lab, sub0, key in (('All games', TG, 'all'), ('(a) Rest-vs-Rest games only', [x for x in TG if x['rr']], 'rest_vs_rest')):
    rows = []
    for nm, sub, f, nf in (('more caps than the enemy at 5:00', sub0, lambda x: x['lead300'] > 0, lambda x: x['lead300'] < 0),
                           ('more caps than the enemy at 8:00', sub0, more, fewer),
                           ('more caps than the enemy at 10:00 (games still running then)', [x for x in sub0 if x['lead600'] is not None], lambda x: x['lead600'] > 0, lambda x: x['lead600'] < 0),
                           ('held more caps for longer than the enemy over the first 8 minutes', sub0, lambda x: x['sh_more'] > x['sh_fewer'], lambda x: x['sh_more'] < x['sh_fewer']),
                           ('held more caps for at least half of the first 8 minutes', sub0, lambda x: x['sh_more'] >= .5, lambda x: x['sh_fewer'] >= .5)):
        r, rec = c2row(nm, sub, f, nf); rec['games'] = len(sub) // 2; rows.append(r); J['reference'][key].append(rec)
    P(f'\n{lab}:'); P(md_table(['what', 'team-games', 'they won (rate, interval)', 'the other side: win rate', 'gap', 'team strength predicts (wins)', 'actual - expected', 'Bradley-Terry: expected; actual - expected'], rows))
P(f'Games still running at 10:00: {len(T10)//2} of {NG}.')
shw = [x['sh_more'] for x in TG if x['win']]; shl = [x['sh_more'] for x in TG if not x['win']]
P(f'Share of the first 8 minutes holding more caps than the enemy: winners mean {100*mean(shw):.0f}% (median {100*med(shw):.0f}%), losers mean {100*mean(shl):.0f}% (median {100*med(shl):.0f}%); level on caps for {100*mean(1 - x["sh_more"] - x["sh_fewer"] for x in TG):.0f}% of the time on average.')
J['time_share'] = dict(winners_mean_pct=round(100 * mean(shw)), losers_mean_pct=round(100 * mean(shl)), level_mean_pct=round(100 * mean(1 - x['sh_more'] - x['sh_fewer'] for x in TG)), games_running_at_10=len(T10) // 2)

# ---- notes
tie = sum(1 for x in TG if x['n_held'] == x['n_enemy']) // 2
P(f'\nGames level on caps at 8:00: {tie} of {NG} (round 5: {OLD["notes"]["level_on_caps_games"]} of 154). Caps held at 8:00 per team: {dict(sorted(C(x["n_held"] for x in TG).items()))}')
tr = [x for x in TG if x['top'] != (x['opp'] in TOP)]
P(f'In Top 6 vs Rest games ({len(tr)//2}): the Top 6 clan held more caps at 8:00 in {sum(more(x) for x in tr if x["top"])}, fewer in {sum(fewer(x) for x in tr if x["top"])}; Top 6 won {sum(x["win"] for x in tr if x["top"])}. (Round 5: 53 games, 30 more, 7 fewer, 46 won.)')
ml = [x for x in TG if more(x)]
P(f'Teams holding more caps at 8:00 were already ahead on score at that moment in {sum(x["lead"] > 0 for x in ml)} of {len(ml)} ({100*sum(x["lead"] > 0 for x in ml)/len(ml):.0f}%); median lead {med([x["lead"] for x in ml]):+.0f} points (quartiles {q([x["lead"] for x in ml],.25):+.0f} to {q([x["lead"] for x in ml],.75):+.0f}). Round 5: 66 of 91 (73%), median +95.')
ah = [x for x in TG if x['lead'] > 0]
P(f'Reference: the team ahead on score at 8:00 won {sum(x["win"] for x in ah)} of {len(ah)} ({wr(ah):.0f}%); round 5: 120 of 153 (78%). Games level on score at 8:00: {sum(x["lead"] == 0 for x in TG)//2}.')
# more caps but behind on score
mb = [x for x in ml if x['lead'] <= 0]; ma = [x for x in ml if x['lead'] > 0]
P(f'Cap leaders already ahead on score won {sum(x["win"] for x in ma)} of {len(ma)} ({wr(ma):.0f}%); cap leaders level or behind on score won {sum(x["win"] for x in mb)} of {len(mb)} ({wr(mb):.0f}%).')
J['notes'] = dict(games=NG, level_on_caps_games=tie, more_caps_n=len(ml), more_caps_already_ahead=sum(x['lead'] > 0 for x in ml), more_caps_already_ahead_pct=round(100 * sum(x['lead'] > 0 for x in ml) / len(ml)),
                  more_caps_median_lead=med([x['lead'] for x in ml]), score_leader_wins=sum(x['win'] for x in ah), score_leader_n=len(ah), score_leader_win_pct=round(wr(ah)),
                  cap_leader_ahead=dict(n=len(ma), wins=sum(x['win'] for x in ma)), cap_leader_not_ahead=dict(n=len(mb), wins=sum(x['win'] for x in mb)),
                  top_vs_rest=dict(games=len(tr) // 2, top_more=sum(more(x) for x in tr if x['top']), top_fewer=sum(fewer(x) for x in tr if x['top']), top_won=sum(x['win'] for x in tr if x['top'])),
                  round5=OLD['notes'])
# games that ended before 8:00, separate
sm = [x for x in SHORT if more(x)]
P(f'\nSeparate row, not in the tables above: the {len(SHORT)//2} games that ended before 8:00, state at the end. The team with more caps at the end won {sum(x["win"] for x in sm)} of {len(sm)}; level on caps at the end: {sum(1 for x in SHORT if x["n_held"] == x["n_enemy"])//2} games.')
J['short_games'] = dict(games=len(SHORT) // 2, more_caps_at_end=len(sm), more_caps_won=sum(x['win'] for x in sm), level=sum(1 for x in SHORT if x['n_held'] == x['n_enemy']) // 2)
# second way: count the "more caps" row straight from the csv rows
chk = 0
for g in GL:
    k = g['key']
    if END[k] < T8: continue
    cnt = C()
    for cap, ev in TL(k).caps.items():
        last = None
        for t, o, _ in sorted(ev, key=lambda e: e[0]):
            if t <= T8: last = o
        if last: cnt[last] += 1
    a, b = g['teams']
    if cnt[a] != cnt[b]: chk += 1
P(f'Second count of games with a cap leader at 8:00, straight from the csv rows: {chk} (table: {len(ml)}).')
J['notes']['second_way_cap_leader_games'] = chk

# ---- figure
rowsf = []
for m, d in J['maps'].items():
    for rec in d['all']:
        if not rec.get('too_few'): rowsf.append((m, rec))
fig = Fig(1100, 100 + 21 * len(rowsf) + 60, 'N1 working figure (C2): teams holding a cap at exactly 8:00, actual win rate minus what team strength predicts',
          f'Points of win rate, {NG} games, cap timeline. Violet dot = now (solid = interval excludes zero), line = 95% interval (games resampled). Grey ring = round 5 (154 games, snapshots).')
x0, wpx, y = 360, 600, 100; sc = lambda v: x0 + wpx / 2 + v * (wpx / 2) / 60
for v in (-60, -40, -20, 0, 20, 40, 60):
    fig.add(f'<line x1="{sc(v):.1f}" y1="90" x2="{sc(v):.1f}" y2="{y + 21 * len(rowsf)}" stroke="{GRID if v else MUTED}" stroke-width="1"/>' + T(sc(v), y + 21 * len(rowsf) + 14, f'{v:+d}', size=10))
for m, rec in rowsf:
    v, (lo, hi) = rec['actual_minus_expected_pts'], rec['ame_ci']; clear = rec['ame_clear']
    fig.add(T(x0 - 8, y + 12, f'{m}: {rec["what"]} (n {rec["n_holders"]})', size=11, fill=INK, anchor='end'))
    fig.add(f'<line x1="{sc(max(-60, lo)):.1f}" y1="{y+8}" x2="{sc(min(60, hi)):.1f}" y2="{y+8}" stroke="{INK}" stroke-width="1.2"/>')
    o = rec.get('round5')
    if o and not o.get('too_few'): fig.add(f'<circle cx="{sc(max(-60, min(60, o["actual_minus_expected_pts"]))):.1f}" cy="{y+8}" r="6.5" fill="none" stroke="{MUTED}" stroke-width="1.3"/>')
    fig.add(f'<circle cx="{sc(max(-60, min(60, v))):.1f}" cy="{y+8}" r="4.5" fill="{VIOLET if clear else BG}" stroke="{VIOLET}" stroke-width="1.5"/>')
    y += 21
fig.save(os.path.join(R5, 'figures', 'n1-caps-8min'))
open(os.path.join(HERE_, 'out-c2.md'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
json.dump(J, open(os.path.join(HERE_, 'c2.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
print('done')
