# Claim 1: early smoke distance short of the cap. Layer A (batch fields) and layer B (ship tracks, cap timeline).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n4lib import *

def ship_layer(s):
    """Adds track-based fields to an early smoke. Returns False when the smoker has no usable track."""
    g = G[s['game']]; gt = TL(s['game']); tr = gt.tracks.get(s['smoker_eid'])
    if tr is None or not tr.own: return False
    p0, pe = tr.pos(s['e0']), tr.pos(s['emit_end'])
    if p0 is None or pe is None: return False
    cc = cap_of(g, s['cap'])
    for tag, p in (('a', p0), ('e', pe)):
        nc = nearest_cap(g, p)
        s['sm_near_' + tag] = edge_m(nc, p); s['sm_cont_' + tag] = edge_m(cc, p) if cc else None; s['sm_nearcap_' + tag] = nc['cap']
        nx, nz = norm(s['map'], s['side'], p[0], p[1]); cx, cz = norm(s['map'], s['side'], nc['x'], nc['z'])
        s['sm_fwd_' + tag] = forward(s['map'], nx - cx, nz - cz)       # metres toward the enemy relative to the nearest cap centre
    s['sm_moved'] = dist_m(p0, pe)
    # covered cruisers: the ones inside the smoke when there are any, else the screened ones
    cr = [x for x in s['j']['smokees'] if x['role'] != 'smoker' and x['how'] != 'none' and x['ship_class'].lower() == 'cruiser']
    ins = [x for x in cr if x['how'] == 'inside']; cr = ins or cr
    near, cont, incap, insm_near, insm_incap = [], [], [], [], []
    t = s['e0']
    while t <= s['end']:
        for x in cr:
            ct = gt.tracks.get(x['entity_id'])
            if ct is None or not ct.own: continue
            i = ct.idx(t)
            if i is None or not ct.alive[i]: continue
            p = ct.pos(t)
            if p is None: continue
            d = edge_m(nearest_cap(g, p), p); near.append(d); incap.append(d < 0)
            if cc: cont.append(edge_m(cc, p))
            if in_smoke(s, p): insm_near.append(d); insm_incap.append(d < 0)
        t += 2
    s['cr_n'] = len(cr)
    s['cr_near'] = mean(near); s['cr_cont'] = mean(cont); s['cr_incap_share'] = mean(incap) if incap else None; s['cr_ever_incap'] = any(incap) if incap else None
    s['cr_insm_near'] = mean(insm_near); s['cr_insm_ever_incap'] = any(insm_incap) if insm_incap else None
    s['cr_insm_share'] = len(insm_near) / len(near) if near else None
    # cap state and invaders from the cap timeline
    for tag, cap in (('cont', s['cap']), ('near', s['near_cap'])):
        s['tl_own_' + tag] = own_at(gt, cap, s['team'], s['e0'])
        s['inv_us_' + tag] = gt.invaded(cap, s['team'], s['e0'], s['end']) > 0
        s['inv_en_' + tag] = gt.invaded(cap, s['opponent'], s['e0'], s['end']) > 0
    # own outline distance, to compare with the batch field: smoke edge to contested cap edge from the final laid path
    s['outline_edge'] = (min(math.hypot(x - cc['x'], z - cc['z']) for x, z in s['path']) - cc['r']) * WU - s['radius_m'] if cc else None
    s['outline_edge_mean'] = (mean(math.hypot(x - cc['x'], z - cc['z']) for x, z in s['path']) - cc['r']) * WU - s['radius_m'] if cc else None
    return True

pops = {'three ships early (round 3 population)': E3, 'early cruiser smoke, cruiser inside': [s for s in EC if s['early_mode'] == 'inside'],
        'early cruiser smoke, cruiser screened': [s for s in EC if s['early_mode'] == 'screened'], 'all early destroyer smokes': DDE}
allp = {id(s): s for v in pops.values() for s in v}
ok = {i for i, s in allp.items() if ship_layer(s)}
P = lambda v, f: pct(v, f)
def block(ss):
    """Layer A and layer B numbers for one population."""
    t = [s for s in ss if id(s) in ok]; c = [s for s in t if s['cr_near'] is not None]; ci_ = [s for s in t if s['cr_insm_near'] is not None]
    st = lambda v, f: [rnd(f(v)), lohi(boot_stat(v, f))]
    r = dict(n=len(ss), n_top=len(grp(ss, 'top')), n_rest=len(grp(ss, 'rest')), clans=nclans(ss), clan_counts=clan_dict(ss),
             clan_counts_smoker_in_cap=clan_dict([s for s in t if s['sm_near_a'] < 0]),
             A_inside_cap_pct=st(ss, lambda v: P(v, lambda s: s['inside'])), A_median_edge_m=st(ss, lambda v: med(s['edge'] for s in v)),
             A_inside_cap_count=sum(s['inside'] for s in ss),
             A_top_rest_inside=two(ss, lambda v: P(v, lambda s: s['inside'])), A_top_rest_edge=two(ss, lambda v: med(s['edge'] for s in v), 0),
             n_track=len(t), n_cruiser_track=len(c), n_cruiser_in_smoke=len(ci_),
             B_smoker_in_cap_act_pct=st(t, lambda v: P(v, lambda s: s['sm_near_a'] < 0)), B_smoker_in_cap_act_count=sum(s['sm_near_a'] < 0 for s in t),
             B_smoker_in_cap_end_pct=st(t, lambda v: P(v, lambda s: s['sm_near_e'] < 0)), B_smoker_in_cap_end_count=sum(s['sm_near_e'] < 0 for s in t),
             B_smoker_in_cap_either_pct=rnd(P(t, lambda s: s['sm_near_a'] < 0 or s['sm_near_e'] < 0)),
             B_smoker_near_edge_act_m=st(t, lambda v: med(s['sm_near_a'] for s in v)), B_smoker_near_edge_end_m=st(t, lambda v: med(s['sm_near_e'] for s in v)),
             B_smoker_cont_edge_act_m=rnd(med(s['sm_cont_a'] for s in t)), B_smoker_cont_edge_end_m=rnd(med(s['sm_cont_e'] for s in t)),
             B_smoker_own_side_act_pct=rnd(P(t, lambda s: s['sm_fwd_a'] < 0)), B_smoker_own_side_end_pct=rnd(P(t, lambda s: s['sm_fwd_e'] < 0)),
             B_smoker_moved_m=rnd(med(s['sm_moved'] for s in t)), B_smoker_closer_at_end_pct=rnd(P(t, lambda s: s['sm_near_e'] < s['sm_near_a'])),
             B_cruiser_near_edge_m=st(c, lambda v: med(s['cr_near'] for s in v)), B_cruiser_cont_edge_m=rnd(med(s['cr_cont'] for s in c if s['cr_cont'] is not None)),
             B_cruiser_ever_in_cap_pct=st(c, lambda v: P(v, lambda s: s['cr_ever_incap'])), B_cruiser_ever_in_cap_count=sum(bool(s['cr_ever_incap']) for s in c),
             B_cruiser_mostly_in_cap_pct=rnd(P(c, lambda s: s['cr_incap_share'] > .5)),
             B_cruiser_in_smoke_near_edge_m=rnd(med(s['cr_insm_near'] for s in ci_)), B_cruiser_in_smoke_ever_in_cap_pct=rnd(P(ci_, lambda s: s['cr_insm_ever_incap'])),
             B_cap_state_contested={k: rnd(P(t, lambda s: s['tl_own_cont'] == k)) for k in ('neutral', 'ours', 'theirs')},
             B_cap_state_nearest={k: rnd(P(t, lambda s: s['tl_own_near'] == k)) for k in ('neutral', 'ours', 'theirs')},
             B_invaded_cont={k: rnd(P(t, f)) for k, f in (('us', lambda s: s['inv_us_cont']), ('enemy', lambda s: s['inv_en_cont']), ('anyone', lambda s: s['inv_us_cont'] or s['inv_en_cont']),
                                                           ('nobody', lambda s: not (s['inv_us_cont'] or s['inv_en_cont'])))},
             B_invaded_near={k: rnd(P(t, f)) for k, f in (('us', lambda s: s['inv_us_near']), ('enemy', lambda s: s['inv_en_near']), ('anyone', lambda s: s['inv_us_near'] or s['inv_en_near']))},
             B_top_rest=dict(smoker_in_cap_act=two(t, lambda v: P(v, lambda s: s['sm_near_a'] < 0)), smoker_near_edge_act=two(t, lambda v: med(s['sm_near_a'] for s in v), 0),
                             smoker_near_edge_end=two(t, lambda v: med(s['sm_near_e'] for s in v), 0),
                             smoker_in_cap_end=two(t, lambda v: P(v, lambda s: s['sm_near_e'] < 0)),
                             cruiser_near_edge=two(c, lambda v: med(s['cr_near'] for s in v), 0), cruiser_ever_in_cap=two(c, lambda v: P(v, lambda s: s['cr_ever_incap'])),
                             invaded_us=two(t, lambda v: P(v, lambda s: s['inv_us_cont']))),
             # checks: new-data version against the snapshot version on the same smokes
             check_outline_vs_batch_median_abs_m=rnd(med(abs(s['outline_edge_mean'] - s['edge']) for s in t if s['outline_edge'] is not None)),
             check_outline_min_vs_batch_median_abs_m=rnd(med(abs(s['outline_edge'] - s['edge']) for s in t if s['outline_edge'] is not None)),
             check_outline_min_median_m=rnd(med(s['outline_edge'] for s in t if s['outline_edge'] is not None)),
             check_outline_inside_agree_pct=rnd(P([s for s in t if s['outline_edge'] is not None], lambda s: (s['outline_edge'] < 0) == s['inside'])),
             check_outline_min_inside_pct=rnd(P([s for s in t if s['outline_edge'] is not None], lambda s: s['outline_edge'] < 0)),
             check_outline_median_m=rnd(med(s['outline_edge_mean'] for s in t if s['outline_edge'] is not None)),
             check_own_tl_vs_batch_agree_pct=rnd(P(t, lambda s: s['tl_own_cont'] == s['own'])),
             hist_smoker_act=[sum(1 for s in t if lo <= s['sm_near_a'] < hi) for lo, hi in HB], hist_smoke_edge=[sum(1 for s in ss if lo <= s['edge'] < hi) for lo, hi in HB],
             hist_cruiser=[sum(1 for s in c if lo <= s['cr_near'] < hi) for lo, hi in HB])
    # smoke outline short, ship inside? cross table
    r['cross'] = dict(outline_out_smoker_out=sum(1 for s in t if not s['inside'] and s['sm_near_a'] >= 0 and s['sm_near_e'] >= 0),
                      outline_out_smoker_in=sum(1 for s in t if not s['inside'] and (s['sm_near_a'] < 0 or s['sm_near_e'] < 0)),
                      outline_in_smoker_out=sum(1 for s in t if s['inside'] and s['sm_near_a'] >= 0 and s['sm_near_e'] >= 0),
                      outline_in_smoker_in=sum(1 for s in t if s['inside'] and (s['sm_near_a'] < 0 or s['sm_near_e'] < 0)))
    return r
HB = [(-1e9, 0), (0, 1000), (1000, 2000), (2000, 3000), (3000, 4000), (4000, 6000), (6000, 1e9)]
R = dict(hist_bins=['inside the cap', '0-1 km', '1-2 km', '2-3 km', '3-4 km', '4-6 km', '6 km+'], pops={k: block(v) for k, v in pops.items()})
# second way for the headline: the cast snapshot (round 5 data: one moment, when the smoke was fully laid) against the track at that moment
chk = []
for s in E3:
    if id(s) not in ok: continue
    c = next((x for x in s['cast'] if x['is_smoker']), None); tr = TL(s['game']).tracks[s['smoker_eid']]
    p = tr.pos(s['ecap']) if s['ecap'] is not None else None
    if c and p:
        nx, nz = norm(s['map'], s['side'], p[0], p[1]); chk.append(math.hypot(nx - c['nx'], nz - c['nz']) * WU)
R['check_track_vs_snapshot'] = dict(n=len(chk), median_m=rnd(med(chk)), p90_m=rnd(q(chk, .9)), within_300m_pct=rnd(pct(chk, lambda d: d <= 300)))
# snapshot version of "smoker in a cap" (cast position at the fully-laid moment), same smokes
def snap_in(s):
    c = next((x for x in s['cast'] if x['is_smoker']), None)
    if not c: return None
    g = G[s['game']]
    return min((math.hypot(c['nx'] - cx, c['nz'] - cz) - cp['r']) * WU for cp in g['caps'] for cx, cz in [norm(s['map'], s['side'], cp['x'], cp['z'])]) < 0
v = [snap_in(s) for s in E3 if id(s) in ok]; v = [x for x in v if x is not None]
R['check_snapshot_smoker_in_cap'] = dict(n=len(v), pct=rnd(pct(v, lambda x: x)))
R['excluded_no_track'] = {k: len(v) - sum(id(s) in ok for s in v) for k, v in pops.items()}
R['A_bug'] = dict(n=len(E3_BUG), inside_count=sum(s['inside'] for s in E3_BUG), inside_pct=rnd(pct(E3_BUG, lambda s: s['inside']), 2), median_edge_m=rnd(med(s['edge'] for s in E3_BUG)))
R['clock'] = CLOCK_NOTE
save('out-c1.json', R)
for k, b in R['pops'].items():
    print('==', k)
    for kk, vv in b.items(): print('  ', kk, vv)
print(R['check_track_vs_snapshot'], R['check_snapshot_smoker_in_cap'], R['excluded_no_track'])
