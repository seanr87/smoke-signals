# Claim 3: radar from smoke per team-game and return per play. Layer A (purpose tags) and layer B (radar log, damage events, cap timeline).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n4lib import *

# ---------- damage events per game, elapsed seconds; first run (as r5lib) and second run (check)
RUNS = by(runs(), 'key')
def load_dmg(run):
    out = collections.defaultdict(list)
    p = os.path.join(GAMES_DIR, run['dir'], 'damage_events.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            out[int(r['victim'])].append((float(r['damage_s']) - run['start'], float(r['amount']), r['kind']))
    return out
DMG = {k: load_dmg(v[0]) for k, v in RUNS.items()}
DMG2 = {k: load_dmg(v[1]) for k, v in RUNS.items() if len(v) > 1}
DIRECT = ('shell', 'torpedo', 'secondary')

# ---------- every radar activation
ACT = []
for k, g in G.items():
    gt = TL(k); ro = g['roster']
    litrows = by([r for r in gt.sensor if r['kind'] == 'radar' and r['row'] == 'lit'], 'activation_id')
    for a in gt.activations('radar'):
        pl = ro.get(a['entity_id'], {})
        sm = [IDX[(k, i)] for i in a['source_in_smoke'] if (k, i) in IDX]
        allied = [s for s in sm if s['team'] == a['team']]
        rec = dict(game=k, team=a['team'], grp='top' if a['team'] in TOP else 'rest', map=g['map'], eid=a['entity_id'], ship=a['ship'].replace('\xa0', ' '),
                   cls=(pl.get('ship_class') or '').lower(), t=a['elapsed_s'], from_smoke=bool(allied), smokes=[s['id'] for s in allied], one_sided=gt.one_sided)
        if allied:
            dd = [s for s in allied if s['cls'] == 'destroyer']; own = any(s['smoker_eid'] == a['entity_id'] for s in allied)
            rec['smoke_kind'] = ('destroyer smoke, radar by another ship' if dd and not all(s['smoker_eid'] == a['entity_id'] for s in dd) else 'destroyer smoke, radar by the smoker itself' if dd
                                 else "cruiser's own smoke" if own else "another cruiser's smoke")
            rec['dd_smoke'] = bool(dd); rec['tagged'] = any(s['play'] for s in allied); rec['early'] = any(s['el'] < 300 for s in allied)
        rows = litrows.get(a['activation_id'], [])
        tg = by(rows, 'target_entity_id')
        rec['lit'] = len(tg); rec['lit_dd'] = sum(1 for e in tg if (ro.get(e, {}).get('ship_class') or '').lower() == 'destroyer')
        rec['lit_rows'] = len(rows); rec['amb_rows'] = sum(r['ambiguous'] for r in rows)
        rec['lit_s'] = sum(r['lit_end_elapsed_s'] - r['lit_start_elapsed_s'] for r in rows)
        dmg = direct = dmg2 = hp = 0.0; hp_ok = True
        for e, rr in tg.items():
            for src, acc in ((DMG[k], 0), (DMG2.get(k, {}), 1)):
                for (t, amt, kind) in src.get(e, []):
                    if any(r['lit_start_elapsed_s'] <= t <= r['lit_end_elapsed_s'] for r in rr):
                        if acc == 0:
                            dmg += amt; direct += amt if kind in DIRECT else 0
                        else: dmg2 += amt
            tr = gt.tracks.get(e)
            if tr is None or not tr.own: hp_ok = False; continue
            for r in rr:
                h0, h1 = tr.health(r['lit_start_elapsed_s']), tr.health(r['lit_end_elapsed_s'] + 2)
                if h0 and h1: hp += max(0.0, h0[0] - h1[0])
        rec['dmg'] = dmg; rec['dmg_direct'] = direct; rec['dmg_run2'] = dmg2 if k in DMG2 else None; rec['hp_loss'] = hp if hp_ok else None
        nc = nearest_cap(g, (a['x'], a['z'])); rec['cap'] = nc['cap']; rec['cap_edge_m'] = edge_m(nc, (a['x'], a['z']))
        rec['tk60'] = took(gt, nc['cap'], a['team'], a['elapsed_s'], a['elapsed_s'] + 60); rec['tk120'] = took(gt, nc['cap'], a['team'], a['elapsed_s'], a['elapsed_s'] + 120)
        rib = [r for r in gt.ribbons if r['entity_id'] == a['entity_id'] and a['elapsed_s'] < r['elapsed_s'] <= a['elapsed_s'] + 120]
        rec['ribbons'] = len(rib); rec['recorder'] = any(r['entity_id'] == a['entity_id'] for r in gt.ribbons)
        ACT.append(rec)
FS = [a for a in ACT if a['from_smoke']]; NS = [a for a in ACT if not a['from_smoke']]
FSDD = [a for a in FS if a['dd_smoke']]

def rates(items, games=None, key='team'):
    cnt = C(x[key] for x in items)
    a, b = rate(cnt, 'top', games), rate(cnt, 'rest', games); t = boot_rate_diff(cnt, games)
    return dict(n=len(items), n_top=sum(x['grp'] == 'top' for x in items), n_rest=sum(x['grp'] == 'rest' for x in items), top=rnd(a, 2), rest=rnd(b, 2),
                diff=rnd(a - b, 2) if a is not None and b is not None else None, ratio=rnd(a / b, 1) if a and b else None, ci=lohi(t, 2),
                clear=bool(t[0] is not None and t[0] * t[1] > 0))
R = dict(team_games=dict(top=sum(GAMES[t] for t in GAMES if t in TOP), rest=sum(GAMES[t] for t in GAMES if t not in TOP)))

# ---------- layer A: tag-based
ddp = [s for s in DD if s['play']]; allp = [s for s in S if s['play']]
cc = [s for s in ddp if s['play'] == 'cap_control']; cct = [s for s in cc if s['own'] != 'ours']
# Module 3 "radar run" set: destroyer smokes with radar run from inside by a radar ship that is inside as a partner, or is not the smoker
def _m3_used(s):
    if not s['off_radar']: return False
    radar_in = any(p['radar'] and p['how'] == 'inside' for p in s['partners'])
    name = s['off_radar'].get('ship') or ((s['radar_cap'] or {}).get('ship') if (s['radar_cap'] or {}).get('activated') else None)
    return radar_in or (name is not None and name != s['player'])
USED = [s for s in DD if _m3_used(s)]
A = dict(dd_plays=rates(ddp), radar_run_smokes=len(USED), all_class_plays=rates(allp), cap_control=dict(n=len(cc), traps=len(ddp) - len(cc)),
         cap_control_cap_taken=two(cct, lambda v: pct(v, lambda s: s['cap_won'])) | dict(x_top=sum(s['cap_won'] for s in grp(cct, 'top')), x_rest=sum(s['cap_won'] for s in grp(cct, 'rest'))),
         by_map={m: dict(plays=sum(s['map'] == m for s in ddp), top=sum(s['map'] == m and s['grp'] == 'top' for s in ddp), rest=sum(s['map'] == m and s['grp'] == 'rest' for s in ddp),
                         per_team_game=rnd(sum(s['map'] == m for s in ddp) / sum(MAPGAMES[m].values()), 2)) for m in MAPORDER},
         conc_cap_control=two(cc, lambda v: mean(s['conc'] for s in v), 0),
         spots_per_radar_smoke=two(USED, lambda v: mean((s['off_radar'] or {}).get('enemies_spotted', 0) for s in v), 2),
         team_games_with_play=dict(top=[sum(1 for k, t in TG if t in TOP and any(s['game'] == k and s['team'] == t for s in allp)), R['team_games']['top']],
                                   rest=[sum(1 for k, t in TG if t not in TOP and any(s['game'] == k and s['team'] == t for s in allp)), R['team_games']['rest']]))
A['three_maps'] = sum(sorted((v['plays'] for v in A['by_map'].values()), reverse=True)[:3])
R['A'] = A

# ---------- layer B: counts three ways
log_sm_ids = {(a['game'], i) for a in FS for i in a['smokes']}
LOGSM = [s for s in S if (s['game'], s['id']) in log_sm_ids]
B = dict(all_activations=rates(ACT), from_smoke=rates(FS), from_dd_smoke=rates(FSDD), not_from_smoke=rates(NS),
         by_kind={k: rates([a for a in FS if a['smoke_kind'] == k]) for k in ('destroyer smoke, radar by another ship', 'destroyer smoke, radar by the smoker itself', "cruiser's own smoke", "another cruiser's smoke")},
         smokes_with_activation=rates(LOGSM), dd_smokes_with_activation=rates([s for s in LOGSM if s['cls'] == 'destroyer']), cruiser_smokes_with_activation=rates([s for s in LOGSM if s['cls'] == 'cruiser']),
         share_from_smoke=two(ACT, lambda v: pct(v, lambda a: a['from_smoke'])),
         by_class={c: rates([a for a in FS if a['cls'] == c]) for c in ('cruiser', 'destroyer', 'battleship')},
         radar_ships=dict(C(a['ship'] for a in FS).most_common(8)),
         clans=clan_dict(FS), early_share=two(FS, lambda v: pct(v, lambda a: a['early'])))
B['by_map'] = {}
for m in MAPORDER:
    v = [a for a in FS if a['map'] == m]; r = rates(v, MAPGAMES[m])
    r['per_team_game_all'] = rnd(len(v) / sum(MAPGAMES[m].values()), 2); r['clans_top'] = nclans(grp(v, 'top')); r['clans_rest'] = nclans(grp(v, 'rest'))
    r['all_radar_per_team_game'] = rnd(sum(a['map'] == m for a in ACT) / sum(MAPGAMES[m].values()), 2)
    B['by_map'][m] = r
B['three_maps'] = dict(names=sorted(MAPORDER, key=lambda m: -B['by_map'][m]['n'])[:3], plays=sum(sorted((v['n'] for v in B['by_map'].values()), reverse=True)[:3]),
                       by_rate=sorted(MAPORDER, key=lambda m: -B['by_map'][m]['per_team_game_all'])[:3])
# tag against log, on the same smokes
tag_ids = {(s['game'], s['id']) for s in ddp}
B['tag_vs_log'] = dict(tagged_dd=len(ddp), tagged_dd_with_log_activation=sum((s['game'], s['id']) in log_sm_ids for s in ddp),
                       log_dd_smokes=sum(s['cls'] == 'destroyer' for s in LOGSM), log_dd_smokes_tagged=sum(1 for s in LOGSM if s['cls'] == 'destroyer' and s['play']),
                       log_dd_smokes_other_tags=dict(C(s['pp'] for s in LOGSM if s['cls'] == 'destroyer' and not s['play']).most_common()),
                       batch_radar_run_dd=sum(1 for s in DD if s['off_radar']), batch_radar_run_dd_in_log=sum(1 for s in DD if s['off_radar'] and (s['game'], s['id']) in log_sm_ids),
                       log_dd_not_batch_run=sum(1 for s in LOGSM if s['cls'] == 'destroyer' and not s['off_radar']),
                       tagged_cruiser=len(allp) - len(ddp), log_cruiser_smokes=sum(s['cls'] == 'cruiser' for s in LOGSM))
tl = [s for s in ddp if (s['game'], s['id']) not in log_sm_ids]
B['tag_vs_log']['tagged_without_log_examples'] = [dict(team=s['team'], map=s['map'], id=s['id'], pp=s['pp'], off_radar=bool(s['off_radar'])) for s in tl[:6]]

# ---------- layer B: return per play
def ret(v):
    ok = [a for a in v if not a['one_sided']]; t60 = [a for a in ok if a['tk60'] is not None]; hp = [a for a in ok if a['hp_loss'] is not None]
    lt = [a for a in ok if a['lit']]
    f = lambda st, k=2, vv=None: two(vv if vv is not None else ok, st, k)
    return dict(n=len(v), n_used=len(ok),
                lit=f(lambda x: mean(a['lit'] for a in x)), lit_any=f(lambda x: pct(x, lambda a: a['lit'] > 0), 1),
                lit_dd=f(lambda x: mean(a['lit_dd'] for a in x)), lit_dd_any=f(lambda x: pct(x, lambda a: a['lit_dd'] > 0), 1),
                dmg=f(lambda x: mean(a['dmg'] for a in x), 0), dmg_direct=f(lambda x: mean(a['dmg_direct'] for a in x), 0), dmg_any=f(lambda x: pct(x, lambda a: a['dmg'] > 0), 1),
                dmg_per_lit_play=f(lambda x: mean(a['dmg'] for a in x), 0, lt), hp_loss=f(lambda x: mean(a['hp_loss'] for a in x), 0, hp),
                dmg_run2=f(lambda x: mean(a['dmg_run2'] for a in x), 0, [a for a in ok if a['dmg_run2'] is not None]),
                cap60=f(lambda x: pct(x, lambda a: a['tk60']), 1, t60), cap120=f(lambda x: pct(x, lambda a: a['tk120']), 1, t60),
                cap60_x=[sum(bool(a['tk60']) for a in grp(t60, 'top')), sum(bool(a['tk60']) for a in grp(t60, 'rest'))],
                cap120_x=[sum(bool(a['tk120']) for a in grp(t60, 'top')), sum(bool(a['tk120']) for a in grp(t60, 'rest'))],
                cap_edge_km=f(lambda x: med(a['cap_edge_m'] for a in x) / 1000, 1),
                lit_rows=sum(a['lit_rows'] for a in ok), amb_rows=sum(a['amb_rows'] for a in ok), dmg_total=round(sum(a['dmg'] for a in ok)), dmg_direct_total=round(sum(a['dmg_direct'] for a in ok)),
                ribbons=sum(a['ribbons'] for a in ok), recorder_plays=sum(a['recorder'] for a in ok))
B['return_from_smoke'] = ret(FS); B['return_from_dd_smoke'] = ret(FSDD); B['return_not_from_smoke'] = ret(NS)
B['return_tagged'] = ret([a for a in FS if a['tagged']]); B['return_untagged'] = ret([a for a in FS if not a['tagged']])
# per team-game totals
for key, lab in (('lit', 'enemies_lit_per_team_game'), ('lit_dd', 'enemy_dd_lit_per_team_game'), ('dmg', 'damage_on_lit_per_team_game')):
    cnt = C()
    for a in FS: cnt[a['team']] += a[key]
    B[lab] = dict(top=rnd(rate(cnt, 'top'), 2), rest=rnd(rate(cnt, 'rest'), 2), ci=lohi(boot_rate_diff(cnt), 2))
# the round 4 return test (cap control: cap taken 58% both) on the cap timeline, same smokes
gtk = lambda s: took(TL(s['game']), s['cap'], s['team'], s['e0'], s['end'] + 60)
for s in cc: s['tk_cont'] = gtk(s)
v = [s for s in cc if s['tk_cont'] is not None]
B['cap_control_timeline'] = two(v, lambda x: pct(x, lambda s: s['tk_cont'])) | dict(x_top=sum(bool(s['tk_cont']) for s in grp(v, 'top')), x_rest=sum(bool(s['tk_cont']) for s in grp(v, 'rest')))
# per clan (Top 6 and the busiest Rest clans)
cnt = C(a['team'] for a in FS); cnt_tag = C(s['team'] for s in ddp)
B['per_clan'] = [dict(clan=t, top6=t in TOP, games=GAMES[t], log_plays=cnt[t], per_game=rnd(cnt[t] / GAMES[t], 2), tag_plays=cnt_tag[t]) for t in sorted(GAMES, key=lambda t: -cnt[t] / GAMES[t]) if t in TOP or cnt[t] >= 4]
B['team_games_with_log_play'] = dict(top=[len({(a['game'], a['team']) for a in FS if a['grp'] == 'top'}), R['team_games']['top']], rest=[len({(a['game'], a['team']) for a in FS if a['grp'] == 'rest'}), R['team_games']['rest']])
B['ribbons_total'] = dict(C(r['ribbon'] for k in G for r in TL(k).ribbons))
R['B'] = B
save('out-c3.json', R)
def show(d, ind=0):
    for k, v in d.items():
        if isinstance(v, dict) and any(isinstance(x, dict) for x in v.values()): print(' ' * ind + str(k)); show(v, ind + 2)
        else: print(' ' * ind + str(k), v)
show(R)
