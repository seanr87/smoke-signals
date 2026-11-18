import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c5lib import *
# LP-4: did Daring smokes on Loop go up shortly after a friendly radar lit an enemy destroyer?
# What the batch has about friendly radar:
#  (a) offensive_radar / radar_cap.activated on OUR smokes: radar run from inside a smoke (no time stamp; bounded by the smoke's life).
#  (b) radar_detections_in_smoke on the ENEMY's smokes: one row each time one of their ships inside their smoke was lit by radar,
#      with the time and the likely source (our nearest radar ship with radar running, wherever it was). This is the only time-stamped
#      record of our radar lighting an enemy ship, and it only exists when that enemy ship was inside its own team's smoke.
#  (c) positions of ships at the one moment each smoke was fully laid (cast).
# Radar activations outside smoke are read by the pipeline but not exported.
m = 'Loop'; W = 60
byg = by(S, 'game')
def ta(s): return s['j']['t_activate']['seconds'] if s['j'].get('t_activate') else s['j']['t_created']['seconds']
def td(s): return s['j']['t_dispersed']['seconds'] if s['j'].get('t_dispersed') else ta(s) + 120
LIT = {}   # (game, lighting team) -> [(sec, victim eid, victim class, source eid, dist)]
for s in S:
    ro = G[s['game']]['roster']
    for r in s['j']['radar_detections_in_smoke']:
        LIT.setdefault((s['game'], s['opponent']), set()).add((round(r['seconds'], 1), r['ship_entity'], (ro.get(r['ship_entity'], {}).get('ship_class') or '').lower(), r.get('source_entity'), r.get('source_distance_m')))
LIT = {k: sorted(v) for k, v in LIT.items()}
P('lit rows (deduped)', sum(len(v) for v in LIT.values()), '| on destroyers', sum(1 for v in LIT.values() for x in v if x[2] == 'destroyer'), '| on Loop', sum(len(v) for k, v in LIT.items() if G[k[0]]['map'] == m), 'destroyers', sum(1 for k, v in LIT.items() if G[k[0]]['map'] == m for x in v if x[2] == 'destroyer'))
def feats(s, W=W):
    t = ta(s); L = LIT.get((s['game'], s['team']), [])
    f = dict()
    f['lit_dd_before'] = any(x[2] == 'destroyer' and t - W <= x[0] <= t for x in L)
    f['lit_any_before'] = any(t - W <= x[0] <= t for x in L)
    f['lit_dd_earlier'] = any(x[2] == 'destroyer' and t - 2 * W <= x[0] < t - W for x in L)     # control window before
    f['lit_dd_after'] = any(x[2] == 'destroyer' and t < x[0] <= t + W for x in L)               # control window after
    f['lit_any_earlier'] = any(t - 2 * W <= x[0] < t - W for x in L); f['lit_any_after'] = any(t < x[0] <= t + W for x in L)
    ally = [y for y in byg[s['game']] if y['team'] == s['team'] and y is not s and (y['off_radar'] or (y['radar_cap'] and y['radar_cap']['activated']))]
    f['radar_smoke_before'] = any(ta(y) <= t and td(y) >= t - W for y in ally)                  # an allied smoke with a radar run from inside stood in the last W seconds
    f['radar_smoke_spotted_before'] = any(ta(y) <= t and td(y) >= t - W and y['off_radar'] and y['off_radar']['enemies_spotted'] > 0 for y in ally)
    f['radar_smoke_earlier'] = any(ta(y) <= t - W and td(y) >= t - 2 * W for y in ally)
    f['own_radar'] = bool(s['off_radar'])
    ro = G[s['game']]['roster']; cp = next(c for c in map_caps(G, s['map']) if c['cap'] == s['zone'])
    rad = [c for c in s['cast'] if c['ally'] and not c['is_smoker'] and ro.get(c['eid'], {}).get('radar_m')]
    f['radar_in_range_of_cap'] = any(math.hypot(c['nx'] - cp['x'], c['nz'] - cp['z']) * WU <= ro[c['eid']]['radar_m'] for c in rad)
    f['radar_covers_cap'] = any(math.hypot(c['nx'] - cp['x'], c['nz'] - cp['z']) * WU + cp['r'] * WU <= ro[c['eid']]['radar_m'] for c in rad)
    edd = [c for c in s['cast'] if not c['ally'] and c['cls'] == 'destroyer']
    f['enemy_dd_known'] = bool(edd)
    if edd:
        e = min(edd, key=lambda c: c['dist_m']); f['enemy_dd_dist_m'] = e['dist_m']
        f['radar_in_range_of_enemy_dd'] = any(math.hypot(c['nx'] - e['nx'], c['nz'] - e['nz']) * WU <= ro[c['eid']]['radar_m'] for c in rad)
    else: f['radar_in_range_of_enemy_dd'] = None
    f['radar_ship_positions'] = len(rad)
    f['any_signal'] = f['lit_dd_before'] or f['radar_smoke_before']
    return f
for s in S:
    if s['cls'] == 'destroyer': s['f'] = feats(s)
DDs = [s for s in S if s['cls'] == 'destroyer']
groups = [('Daring on Loop', [s for s in DDs if s['ship'] == 'Daring' and s['map'] == m]),
          ('Daring on other maps', [s for s in DDs if s['ship'] == 'Daring' and s['map'] != m]),
          ('Other cap sitters on Loop', [s for s in DDs if s['habit'] == 'cap sitters' and s['ship'] != 'Daring' and s['map'] == m]),
          ('Other destroyer smokes on Loop', [s for s in DDs if s['habit'] != 'cap sitters' and s['map'] == m]),
          ('All destroyer smokes, all maps', DDs)]
keys = [('lit_dd_before', 'Our radar lit an enemy destroyer (in its smoke) in the 60 s before'), ('lit_dd_earlier', 'control: same, 120 to 60 s before'), ('lit_dd_after', 'control: same, 60 s after'),
        ('lit_any_before', 'Our radar lit any enemy ship (in its smoke) in the 60 s before'), ('lit_any_earlier', 'control: 120 to 60 s before'), ('lit_any_after', 'control: 60 s after'),
        ('radar_smoke_before', 'An allied smoke with radar run from inside stood in the 60 s before'), ('radar_smoke_spotted_before', 'same, and that radar spotted an enemy'), ('radar_smoke_earlier', 'control: 120 to 60 s before'),
        ('radar_in_range_of_cap', 'An allied radar ship within radar range of the cap centre when the smoke was laid'), ('radar_covers_cap', 'An allied radar ship covering the whole cap'),
        ('own_radar', 'Radar run from inside this smoke')]
res = {}; trs = []
for nm, v in groups:
    res[nm] = dict(n=len(v), clans=clan_dict(v))
    row = [nm, len(v)]
    for k, lab in keys:
        kk = sum(1 for s in v if s['f'][k]); p, (lo, hi) = rate_ci(v, lambda s, k=k: s['f'][k])
        res[nm][k] = dict(k=kk, n=len(v), pct=round(p, 1), ci=[round(lo, 1), round(hi, 1)]); row.append(f'{kk} ({p:.0f}%, {lo:.0f} to {hi:.0f})')
    kn = [s for s in v if s['f']['enemy_dd_known']]; kk = sum(1 for s in kn if s['f']['radar_in_range_of_enemy_dd'])
    res[nm]['radar_in_range_of_enemy_dd'] = dict(k=kk, n=len(kn)); row.append(f'{kk} of {len(kn)}' + (f' ({100 * kk / len(kn):.0f}%)' if len(kn) >= 8 else ' (too few)'))
    trs.append(row)
P(md_table(['Group', 'Smokes'] + [lab for _, lab in keys] + ['An allied radar ship within radar range of the nearest enemy destroyer with a known position'], trs))
dl = groups[0][1]
P(' Daring on Loop clans', clan_counts(dl), '| zone', cc(C(s['zone'] for s in dl)), '| Top 6 n', sum(s['grp'] == 'top' for s in dl))
P(' radar ship positions recorded per Daring smoke: median', med(s['f']['radar_ship_positions'] for s in dl), '| none recorded', sum(s['f']['radar_ship_positions'] == 0 for s in dl))
P(' team radar ships in Daring team-games on Loop', cc(C(p['ship'].replace('\xa0', ' ') for k, t in {(s['game'], s['team']) for s in dl} for p in G[k]['roster'].values() if p['team'] == t and p['radar_m'])))
# difference tests
def diff(a, b, k):
    pool = [dict(team=s['team'], grp=s['grp'], a=True, v=s['f'][k]) for s in a] + [dict(team=s['team'], grp=s['grp'], a=False, v=s['f'][k]) for s in b]
    f = lambda w: (pct([x for x in w if x['a']], lambda x: x['v']) - pct([x for x in w if not x['a']], lambda x: x['v'])) if any(x['a'] for x in w) and any(not x['a'] for x in w) else None
    return f(pool), boot_stat(pool, f)
tests = {}
for k in ('lit_dd_before', 'lit_any_before', 'radar_smoke_before', 'radar_in_range_of_cap'):
    for nm, b in (('Daring other maps', groups[1][1]), ('other sitters on Loop', groups[2][1]), ('other DD smokes on Loop', groups[3][1])):
        d, (lo, hi) = diff(dl, b, k); tests[f'{k} | Daring on Loop minus {nm}'] = [round(d, 1), round(lo, 1), round(hi, 1)]
        P(f'  {k}: Daring on Loop minus {nm}: {d:+.0f} pts ({lo:+.0f} to {hi:+.0f}{" *" if lo * hi > 0 else ""})')
# before vs control windows, within Daring on Loop
for a, b in (('lit_dd_before', 'lit_dd_earlier'), ('lit_dd_before', 'lit_dd_after'), ('lit_any_before', 'lit_any_earlier'), ('radar_smoke_before', 'radar_smoke_earlier')):
    f = lambda w: pct(w, lambda s: s['f'][a]) - pct(w, lambda s: s['f'][b]); lo, hi = boot_stat(dl, f)
    tests[f'Daring on Loop: {a} minus {b}'] = [round(f(dl), 1), round(lo, 1), round(hi, 1)]; P(f'  Daring on Loop, {a} minus {b}: {f(dl):+.0f} pts ({lo:+.0f} to {hi:+.0f})')
# the smokes that had a signal
P(' Daring on Loop smokes with a signal:')
ex = []
for s in sorted(dl, key=lambda s: (s['game'], s['el'])):
    f = s['f']
    if f['lit_dd_before'] or f['lit_any_before'] or f['radar_smoke_before']:
        L = [x for x in LIT.get((s['game'], s['team']), []) if ta(s) - W <= x[0] <= ta(s)]
        ro = G[s['game']]['roster']
        ex.append(dict(link=s['link'], team=s['team'], time=clock(s['el']), cell=s['ncell_name'], lit=[(ro[x[1]]['ship'], round(ta(s) - x[0]), ro.get(x[3], {}).get('ship')) for x in L], radar_smoke_before=f['radar_smoke_before']))
        P(f'    {s["slug"]} {s["team"]} {clock(s["el"])} {s["ncell_name"]} zone {s["zone"]} | lit: {[(ro[x[1]]["ship"], str(round(ta(s) - x[0])) + " s before", "by " + str(ro.get(x[3], {}).get("ship"))) for x in L]} | allied radar smoke stood: {f["radar_smoke_before"]} | conc {s["conc"]:.0f}')
# reverse view: after each time our radar lit an enemy destroyer on Loop, did a Daring of that team smoke within 60 s?
rev = dict(episodes=0, with_daring=0, followed=0)
for (gk, team), L in LIT.items():
    if G[gk]['map'] != m: continue
    ep = [];
    for x in L:
        if x[2] != 'destroyer': continue
        if not ep or x[0] - ep[-1] > 30: ep.append(x[0])
    dar = [e for e, p in G[gk]['roster'].items() if p['team'] == team and p['ship'] == 'Daring']
    for t in ep:
        rev['episodes'] += 1
        alive = [e for e in dar if not (G[gk]['roster'][e]['death'] and G[gk]['roster'][e]['death']['seconds'] <= t)]
        if not alive: continue
        rev['with_daring'] += 1
        if any(s['ship'] == 'Daring' and s['team'] == team and t <= ta(s) <= t + W for s in byg[gk]): rev['followed'] += 1
# base rate: Daring smokes per Daring team-game minute on Loop
dtg = {(s['game'], s['team']) for s in dl}; mins = sum((G[k]['len'] or 1200) for k, t in dtg) / 60
rev['base_daring_smokes_per_60s'] = round(len(dl) / mins, 3)
P(' reverse view:', rev, '| Daring team-games', len(dtg), '| Daring smokes per team-game', round(len(dl) / len(dtg), 2))
# all maps reverse, any sitter
OUT = dict(table=res, tests=tests, examples=ex, reverse=rev, window_s=W,
           note='Proxy only. The batch does not export radar activations made outside smoke, and has no timeline of which enemy ships were detected.')
save_json('part-lp-daring.json', OUT)
