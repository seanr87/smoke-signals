# Claim 2: radar cruiser inside early destroyer smokes. Layer A (batch fields) and layer B (radar log, cap timeline).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n4lib import *

def radar_layer(s):
    """Radar use by the radar cruisers the batch puts inside the smoke, from the radar log."""
    g = G[s['game']]; gt = TL(s['game']); ro = g['roster']; sid = int(s['id'])
    inside = [x['entity_id'] for x in s['j']['smokees'] if x['role'] != 'smoker' and x['how'] == 'inside' and x['ship_class'].lower() == 'cruiser' and ro.get(x['entity_id'], {}).get('radar_m')]
    acts = [a for a in gt.activations('radar', s['team']) if s['e0'] <= a['elapsed_s'] <= s['end']]
    strict = [a for a in acts if a['entity_id'] in inside and sid in a['source_in_smoke']]
    loose = [a for a in acts if a['entity_id'] in inside and (sid in a['source_in_smoke'] or in_smoke(s, (a['x'], a['z'])))]
    anyship = [a for a in acts if sid in a['source_in_smoke']]          # any radar ship of the team standing in this smoke
    ids = {a['activation_id'] for a in loose}
    lit = [r for r in gt.sensor if r['kind'] == 'radar' and r['row'] == 'lit' and r['activation_id'] in ids]
    tg = {r['target_entity_id'] for r in lit}; dd = {e for e in tg if (ro.get(e, {}).get('ship_class') or '').lower() == 'destroyer'}
    s['rc_inside_n'] = len(inside); s['rc_strict'] = bool(strict); s['rc_used'] = bool(loose); s['rc_acts'] = len(loose); s['rc_anyship'] = bool(anyship)
    s['rc_lit'] = len(tg); s['rc_lit_dd'] = len(dd); s['rc_lit_any'] = bool(tg); s['rc_lit_dd_any'] = bool(dd)
    s['rc_amb'] = sum(r['ambiguous'] for r in lit); s['rc_litrows'] = len(lit)
    # the batch's own flag for the same thing (needs the ship undetected at activation)
    s['batch_run'] = bool(s['off_radar'])
    # cap taken, several ways
    s['takeable'] = s['own'] != 'ours'
    s['tk_cont'] = took(gt, s['cap'], s['team'], s['e0'], s['end'] + 60)
    s['tk_near'] = took(gt, s['near_cap'], s['team'], s['e0'], s['end'] + 60)
    s['tk_cont10'] = took(gt, s['cap'], s['team'], s['e0'], s['end'] + 10)
    anyc = [took(gt, c['cap'], s['team'], s['e0'], s['end'] + 10) for c in g['caps']]
    s['tk_any10'] = any(x for x in anyc if x)
    cw = s['r']['cap_won']
    s['tk_batchcap'] = took(gt, cw, s['team'], s['e0'], s['end'] + 10) if cw else None
for s in DDE: radar_layer(s)
for s in E3 + E3_BUG + DDE_BUG:
    if 'rc_used' not in s: radar_layer(s)
one = [s for s in DDE if TL(s['game']).one_sided]

RUNGS = [('inside', 'Radar cruiser inside (batch field)', lambda s: s['radar_ca_inside']),
         ('used', 'Inside and ran radar from it', lambda s: s['radar_ca_inside'] and s['rc_used']),
         ('lit', 'Ran radar from it and lit an enemy', lambda s: s['radar_ca_inside'] and s['rc_lit_any']),
         ('lit_dd', 'Ran radar from it and lit an enemy destroyer', lambda s: s['radar_ca_inside'] and s['rc_lit_dd_any'])]
def tab(pop, f):
    rows = {}
    for m in ['All maps'] + MAPORDER:
        ss = pop if m == 'All maps' else [s for s in pop if s['map'] == m]
        r = two(ss, lambda v: pct(v, f)); r['x_top'] = sum(bool(f(s)) for s in grp(ss, 'top')); r['x_rest'] = sum(bool(f(s)) for s in grp(ss, 'rest'))
        r['flag_top'] = 'too few' if r['n_top'] < 8 else 'small n' if r['n_top'] < 15 else ''; r['flag_rest'] = 'too few' if r['n_rest'] < 8 else 'small n' if r['n_rest'] < 15 else ''
        r['clan_counts'] = clan_dict([s for s in ss if f(s)])
        rows[m] = r
    return rows
R = dict(n=len(DDE), n_top=len(grp(DDE, 'top')), n_rest=len(grp(DDE, 'rest')), one_sided_smokes=len(one))
R['rungs'] = {k: dict(label=lab, table=tab(DDE, f)) for k, lab, f in RUNGS}
R['three_ships'] = {k: two(E3, lambda v, f=f: pct(v, f)) | dict(x_top=sum(bool(f(s)) for s in grp(E3, 'top')), x_rest=sum(bool(f(s)) for s in grp(E3, 'rest'))) for k, lab, f in RUNGS}
# conditional: of smokes with a radar cruiser inside, how many ran radar from it
ins = [s for s in DDE if s['radar_ca_inside']]
R['of_inside'] = dict(n=len(ins), used=two(ins, lambda v: pct(v, lambda s: s['rc_used'])), used_strict=two(ins, lambda v: pct(v, lambda s: s['rc_strict'])),
                      lit=two(ins, lambda v: pct(v, lambda s: s['rc_lit_any'])), lit_dd=two(ins, lambda v: pct(v, lambda s: s['rc_lit_dd_any'])),
                      batch_run=two(ins, lambda v: pct(v, lambda s: s['batch_run'])),
                      counts=dict(used=sum(s['rc_used'] for s in ins), strict=sum(s['rc_strict'] for s in ins), lit=sum(s['rc_lit_any'] for s in ins), lit_dd=sum(s['rc_lit_dd_any'] for s in ins),
                                  batch_run=sum(s['batch_run'] for s in ins), log_and_batch=sum(s['rc_used'] and s['batch_run'] for s in ins),
                                  log_not_batch=sum(s['rc_used'] and not s['batch_run'] for s in ins), batch_not_log=sum(s['batch_run'] and not s['rc_used'] for s in ins)),
                      enemies_lit_per_using_smoke=two([s for s in ins if s['rc_used']], lambda v: mean(s['rc_lit'] for s in v), 2),
                      dd_lit_per_using_smoke=two([s for s in ins if s['rc_used']], lambda v: mean(s['rc_lit_dd'] for s in v), 2),
                      lit_rows=sum(s['rc_litrows'] for s in ins), lit_rows_ambiguous=sum(s['rc_amb'] for s in ins))
notin = [s for s in DDE if not s['radar_ca_inside']]
R['not_inside_anyship_radar'] = dict(n=len(notin), any_radar_from_smoke=sum(s['rc_anyship'] for s in notin))
R['per_team_game'] = {}
for k, lab, f in RUNGS:
    cnt = C(s['team'] for s in DDE if f(s))
    R['per_team_game'][k] = dict(top=rnd(rate(cnt, 'top'), 2), rest=rnd(rate(cnt, 'rest'), 2), ci=lohi(boot_rate_diff(cnt), 2))

# "inside goes with the cap being taken"
MEAS = [('batch_all', 'Batch cap_won, all smokes (round 4, Module 2 number)', lambda v: v, lambda s: s['cap_won']),
        ('batch_takeable', 'Batch cap_won, contested cap not ours at activation (round 4, Module 3 number)', lambda v: [s for s in v if s['takeable']], lambda s: s['cap_won']),
        ('tl_cont', 'Cap timeline: contested cap not ours at activation, ours within 60 s after the smoke cleared', lambda v: [s for s in v if s['tk_cont'] is not None], lambda s: s['tk_cont']),
        ('tl_near', 'Cap timeline: nearest cap, same test', lambda v: [s for s in v if s['tk_near'] is not None], lambda s: s['tk_near']),
        ('tl_cont10', 'Cap timeline: contested cap, the batch window (10 s after)', lambda v: [s for s in v if s['tk_cont10'] is not None], lambda s: s['tk_cont10']),
        ('tl_any10', 'Cap timeline: any cap flipped to us by 10 s after, all smokes', lambda v: v, lambda s: s['tk_any10'])]
def capcmp(a, b, label_a, label_b):
    out = dict(a=label_a, b=label_b, n_a=len(a), n_b=len(b), clans_a=nclans(a), clans_b=nclans(b), rows={})
    for key, name, sel, f in MEAS:
        st = lambda v, sel=sel, f=f: pct(sel(v), f)
        va, vb = st(a), st(b); lo, hi = boot_cmp(a, b, st)
        out['rows'][key] = dict(name=name, a=rnd(va), n_a=len(sel(a)), x_a=sum(bool(f(s)) for s in sel(a)), b=rnd(vb), n_b=len(sel(b)), x_b=sum(bool(f(s)) for s in sel(b)),
                                diff=rnd(va - vb) if va is not None and vb is not None else None, ci=lohi((lo, hi)), clear=bool(lo is not None and lo * hi > 0))
    return out
R['cap_three_ships'] = capcmp([s for s in E3 if s['pt'] == RI], [s for s in E3 if s['pt'] == RN], RI, 'radar cruiser covered, not inside')
R['cap_three_ships_vs_rest'] = capcmp([s for s in E3 if s['pt'] == RI], [s for s in E3 if s['pt'] != RI], RI, 'everything else')
R['cap_all_early'] = capcmp([s for s in DDE if s['radar_ca_inside']], [s for s in DDE if not s['radar_ca_inside']], RI, 'no radar cruiser inside')
ins_used = [s for s in DDE if s['radar_ca_inside'] and s['rc_used']]; ins_not = [s for s in DDE if s['radar_ca_inside'] and not s['rc_used']]
R['cap_used_vs_not'] = capcmp(ins_used, ins_not, 'radar cruiser inside, ran radar from it', 'radar cruiser inside, did not')
for g_ in ('top', 'rest'):
    R['cap_all_early_' + g_] = capcmp([s for s in DDE if s['radar_ca_inside'] and s['grp'] == g_], [s for s in DDE if not s['radar_ca_inside'] and s['grp'] == g_], RI + ' (' + GROUP_LABEL[g_] + ')', 'no radar cruiser inside')
# batch cap_won against the timeline on the same smokes
cw = [s for s in DDE if s['cap_won']]
R['check_cap_won'] = dict(batch_cap_won=len(cw), timeline_confirms_same_cap=sum(bool(s['tk_batchcap']) for s in cw),
                          batch_cap_is_contested=sum(s['r']['cap_won'] == s['cap'] for s in cw), batch_cap_is_nearest=sum(s['r']['cap_won'] == s['near_cap'] for s in cw),
                          timeline_any10=sum(s['tk_any10'] for s in DDE), timeline_any10_not_batch=sum(s['tk_any10'] and not s['cap_won'] for s in DDE),
                          contested_is_nearest=sum(s['cap'] == s['near_cap'] for s in DDE), n=len(DDE),
                          tk_cont_agree_with_batch_pct=rnd(pct([s for s in DDE if s['tk_cont'] is not None], lambda s: bool(s['tk_cont']) == bool(s['cap_won']))))
# second way for the headline: count straight from the raw smokees list and roster
alt = lambda s: any(x['how'] == 'inside' and x['role'] != 'smoker' and x['ship_class'] == 'Cruiser' and G[s['game']]['roster'][x['entity_id']].get('radar_m') for x in s['j']['smokees'])
R['check_headline_second_way'] = dict(top=sum(alt(s) for s in grp(DDE, 'top')), rest=sum(alt(s) for s in grp(DDE, 'rest')))
_ins = lambda s: s['radar_ca_inside']
def _a(pop):
    r = two(pop, lambda v: pct(v, _ins)); r['x_top'] = sum(_ins(s) for s in grp(pop, 'top')); r['x_rest'] = sum(_ins(s) for s in grp(pop, 'rest')); return r
R['A_bug'] = dict(n=len(DDE_BUG), all=_a(DDE_BUG), sg=_a([s for s in DDE_BUG if s['map'] == 'Sleeping Giant']), hs=_a([s for s in DDE_BUG if s['map'] == 'Hotspot']), three=_a(E3_BUG),
                  cap_three=capcmp([s for s in E3_BUG if s['pt'] == RI], [s for s in E3_BUG if s['pt'] == RN], RI, 'not inside')['rows']['batch_all'],
                  cap_all=capcmp([s for s in DDE_BUG if s['radar_ca_inside']], [s for s in DDE_BUG if not s['radar_ca_inside']], RI, 'none')['rows']['batch_takeable'])
R['clock'] = CLOCK_NOTE
save('out-c2.json', R)
def show(d, ind=0):
    for k, v in d.items():
        if isinstance(v, dict) and any(isinstance(x, dict) for x in v.values()): print(' ' * ind + str(k)); show(v, ind + 2)
        else: print(' ' * ind + str(k), v)
show(R)
