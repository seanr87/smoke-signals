# C5 Loop: do Daring smokes follow a friendly radar lighting an enemy destroyer? Full radar log version.
# Run: python -I -X utf8 c5_loop.py  -> c5.json, c5_out.txt
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3lib import *
random.seed(532)
OUT = []
def P(*a):
    line = ' '.join(str(x) for x in a); OUT.append(line); print(line)
MAP = 'Loop'; NEAR_M = 3000
DD = [s for s in S if s['cls'] == 'destroyer']
GROUPS = [('Daring on Loop', [s for s in DD if s['ship'] == 'Daring' and s['map'] == MAP]),
          ('Daring on other maps', [s for s in DD if s['ship'] == 'Daring' and s['map'] != MAP]),
          ('Other cap sitters on Loop', [s for s in DD if s['habit'] == 'cap sitters' and s['ship'] != 'Daring' and s['map'] == MAP]),
          ('Other destroyer smokes on Loop', [s for s in DD if s['habit'] != 'cap sitters' and s['map'] == MAP]),
          ('All destroyer smokes, all maps', DD)]
need = {id(s) for _, v in GROUPS[:4] for s in v}

_sp = {}
def spans(gk, team, unattr=False):
    """Radar lit spans on enemy destroyers by radars of `team` in game gk: dicts start, end, tgt, src (entity or None), ship, amb, row."""
    k = (gk, team, unattr)
    if k not in _sp:
        g = TL(gk); opp = next(t for t in G[gk]['teams'] if t != team); out = []
        for r in g.lit('radar', target_team=opp, include_unattributed=unattr):
            if ship_cls(gk, r['target_entity_id']) != 'destroyer': continue
            if r['row'] == 'lit' and r['team'] != team: continue
            out.append(dict(start=r['lit_start_elapsed_s'], end=r['lit_end_elapsed_s'], tgt=r['target_entity_id'], src=r['entity_id'] if r['row'] == 'lit' else None, ship=(r['ship'] or '?').replace('\xa0', ' '),
                            amb=r['ambiguous'], row=r['row'], sx=r['x'], sz=r['z'], act=r['elapsed_s'], tgt_ship=(r['target_ship'] or '').replace('\xa0', ' '), tgt_in_smoke=bool(r['target_in_smoke']),
                            src_in_smoke=bool(r['source_in_smoke'])))
        _sp[k] = sorted(out, key=lambda x: x['start'])
    return _sp[k]
_near = {}
def near_iv(gk, sp, cap):
    """Sub-intervals of a lit span during which the target was within 3 km of the edge of cap (2 s steps)."""
    k = (gk, sp['tgt'], round(sp['start'], 2), cap)
    if k not in _near:
        g = TL(gk); c = cap_of(gk, cap); tr = g.tracks.get(sp['tgt']); out = []; t = sp['start']; cur = None
        while tr and t <= sp['end'] + 1e-6:
            p = tr.pos(t)
            ok = bool(p) and (math.hypot(p[0] - c['x'], p[1] - c['z']) - c['r']) * WU <= NEAR_M
            if ok and cur is None: cur = t
            if not ok and cur is not None: out.append((cur, t)); cur = None
            t += 2
        if cur is not None: out.append((cur, sp['end']))
        _near[k] = out
    return _near[k]
def ivs(s, near, unattr=False):
    """Lit intervals relevant to smoke s: every span (near=False) or only the parts with the target within 3 km of the smoke's nearest cap."""
    out = []
    for sp in spans(s['game'], s['team'], unattr):
        if near: out += [(a, b, sp) for a, b in near_iv(s['game'], sp, s['near_cap'])]
        else: out.append((sp['start'], sp['end'], sp))
    return out
def overlap(I, a, b):
    return [x for x in I if x[0] <= b and x[1] >= a]
def union_len(segs, lo, hi):
    tot = 0; end = lo
    for a, b in sorted(segs):
        a = max(a, end, lo); b = min(b, hi)
        if b > a: tot += b - a; end = b
    return tot
def base_window(s):
    """The stretch of the game used for the base rate: first to last smoke of the game (any team), cut at the smoker's death."""
    ts = [x['e0'] for x in BYG[s['game']]]
    lo, hi = min(ts), max(ts)
    d = TL(s['game']).tracks[s['smoker_eid']].death_t() if s['smoker_eid'] in TL(s['game']).tracks else None
    if d is not None: hi = min(hi, max(d, s['e0']))
    return lo, hi
BYG = by(S, 'game')
WS = (30, 60, 90)
def feats(s):
    f = {}
    for near in (False, True):
        I = ivs(s, near); tag = 'near' if near else 'any'
        for W in WS:
            f[f'before_{tag}_{W}'] = bool(overlap(I, s['e0'] - W, s['e0']))
            f[f'after_{tag}_{W}'] = bool(overlap(I, s['e0'] + 0.01, s['e0'] + W))
            f[f'afterstart_{tag}_{W}'] = any(s['e0'] < x[0] <= s['e0'] + W for x in I)
            f[f'beforestart_{tag}_{W}'] = any(s['e0'] - W <= x[0] <= s['e0'] for x in I)
            lo, hi = base_window(s)
            if hi - lo >= 30:
                f[f'base_before_{tag}_{W}'] = union_len([(a, b + W) for a, b, _ in I], lo, hi) / (hi - lo)
                f[f'base_after_{tag}_{W}'] = union_len([(a - W, b) for a, b, _ in I], lo, hi) / (hi - lo)
            else:
                f[f'base_before_{tag}_{W}'] = None; f[f'base_after_{tag}_{W}'] = None
        f[f'earlier_{tag}'] = bool(overlap(I, s['e0'] - 120, s['e0'] - 60.01))     # round 5 control window: 120 to 60 s before
        f[f'later_{tag}'] = bool(overlap(I, s['e0'] + 60.01, s['e0'] + 120))       # 60 to 120 s after
        Iu = ivs(s, near, True)
        f[f'before_{tag}_60_with_unattributed'] = bool(overlap(Iu, s['e0'] - 60, s['e0']))
    f['lit_now_any'] = bool(overlap(ivs(s, False), s['e0'], s['e0'])); f['lit_now_near'] = bool(overlap(ivs(s, True), s['e0'], s['e0']))
    return f
for s in DD: s['f'] = feats(s)
P('destroyer smokes', len(DD), '| groups', [(n, len(v)) for n, v in GROUPS])
P('radar lit spans on enemy destroyers, all games:', sum(len(spans(k, t)) for k in G for t in G[k]['teams']), '| on Loop', sum(len(spans(k, t)) for k in G if G[k]['map'] == MAP for t in G[k]['teams']),
  '| with unattributed, Loop', sum(len(spans(k, t, True)) for k in G if G[k]['map'] == MAP for t in G[k]['teams']), '| Loop games', sum(1 for k in G if G[k]['map'] == MAP),
  '| one-sided Loop games', sum(1 for k in G if G[k]['map'] == MAP and TL(k).one_sided))

def rate(v, k):
    return 100 * sum(1 for s in v if s['f'][k]) / len(v) if v else None
def basep(v, k):
    w = [s['f'][k] for s in v if s['f'][k] is not None]
    return 100 * sum(w) / len(w) if w else None
def cell_(v, k, basek=None):
    n = len(v); kk = sum(1 for s in v if s['f'][k])
    d = dict(k=kk, n=n, clans=len({s['team'] for s in v}), small_n=8 <= n < 15)
    if n >= 8:
        d['pct'] = r1(rate(v, k)); d['ci'] = iv(bstat(v, lambda w: rate(w, k)))
        if basek:
            d['base_pct'] = r1(basep(v, basek)); d['expected_k'] = r1(sum(s['f'][basek] for s in v if s['f'][basek] is not None))
            st = lambda w: (rate(w, k) - basep(w, basek)) if basep(w, basek) is not None else None
            d['minus_base'] = r1(st(v)); d['minus_base_ci'] = iv(bstat(v, st)); d['minus_base_clear'] = clear(bstat(v, st))
    return d
RES = {}
for nm, v in GROUPS:
    r = dict(n=len(v), clans=len({s['team'] for s in v}), clans_txt=clans_of(v) if len(v) < 300 else None, top6_n=sum(s['grp'] == 'top' for s in v), rest_n=sum(s['grp'] == 'rest' for s in v))
    for tag in ('any', 'near'):
        for W in WS:
            r[f'before_{tag}_{W}'] = cell_(v, f'before_{tag}_{W}', f'base_before_{tag}_{W}')
            r[f'after_{tag}_{W}'] = cell_(v, f'after_{tag}_{W}', f'base_after_{tag}_{W}')
            r[f'afterstart_{tag}_{W}'] = cell_(v, f'afterstart_{tag}_{W}'); r[f'beforestart_{tag}_{W}'] = cell_(v, f'beforestart_{tag}_{W}')
        r[f'earlier_{tag}'] = cell_(v, f'earlier_{tag}'); r[f'later_{tag}'] = cell_(v, f'later_{tag}')
        r[f'before_{tag}_60_with_unattributed'] = cell_(v, f'before_{tag}_60_with_unattributed')
        # before minus the round 5 control windows
        for ck in (f'earlier_{tag}', f'later_{tag}'):
            if len(v) >= 8:
                st = lambda w, ck=ck, tag=tag: rate(w, f'before_{tag}_60') - rate(w, ck); c_ = bstat(v, st)
                r[f'before_{tag}_60_minus_{ck}'] = dict(diff=r1(st(v)), ci=iv(c_), clear=clear(c_))
    r['lit_now_any'] = cell_(v, 'lit_now_any'); r['lit_now_near'] = cell_(v, 'lit_now_near')
    # Top 6 vs Rest
    t = [s for s in v if s['grp'] == 'top']; re_ = [s for s in v if s['grp'] == 'rest']
    for k in ('before_any_60', 'before_near_60', 'after_near_60'):
        if len(t) >= 8 and len(re_) >= 8:
            c_ = bdiff_groups(v, lambda w, k=k: rate(w, k))
            r['top6_vs_rest_' + k] = dict(top6=r1(rate(t, k)), top6_n=len(t), rest=r1(rate(re_, k)), rest_n=len(re_), diff=r1(rate(t, k) - rate(re_, k)), ci=iv(c_), clear=clear(c_))
        else:
            r['top6_vs_rest_' + k] = dict(top6_n=len(t), rest_n=len(re_), top6_k=sum(1 for s in t if s['f'][k]), rest_k=sum(1 for s in re_ if s['f'][k]), note='too few in one group')
    RES[nm] = r
def cs(c):
    if 'pct' not in c: return f"{c['k']} of {c['n']} (too few)"
    b = f"; base {c['base_pct']}%, minus base {c['minus_base']:+} ({c['minus_base_ci'][0]:+} to {c['minus_base_ci'][1]:+}{' *' if c['minus_base_clear'] else ''})" if 'base_pct' in c and c.get('minus_base_ci') else ''
    return f"{c['k']} of {c['n']} ({c['pct']}%, {c['ci'][0] if c['ci'] else '-'} to {c['ci'][1] if c['ci'] else '-'}{b})"
for tag in ('any', 'near'):
    P(f'\n--- radar lit an enemy destroyer ({"within 3 km of the cap the smoke is nearest to" if tag == "near" else "anywhere"})')
    cols = [f'before_{tag}_30', f'before_{tag}_60', f'before_{tag}_90', f'earlier_{tag}', f'later_{tag}', f'after_{tag}_60', f'afterstart_{tag}_60', f'beforestart_{tag}_60', f'before_{tag}_60_with_unattributed']
    P(md_table(['group'] + cols, [[nm] + [cs(RES[nm][c]) for c in cols] for nm, _ in GROUPS]))
    for nm, _ in GROUPS:
        P('   ', nm, 'before minus earlier', RES[nm].get(f'before_{tag}_60_minus_earlier_{tag}'), '| minus later', RES[nm].get(f'before_{tag}_60_minus_later_{tag}'))
for nm, _ in GROUPS: P(nm, {k: v for k, v in RES[nm].items() if k.startswith('top6_vs_rest')}, 'lit at the activation moment:', cs(RES[nm]['lit_now_any']), '| near', cs(RES[nm]['lit_now_near']))
# group differences
TESTS = []
dl = GROUPS[0][1]
for k in ('before_any_30', 'before_any_60', 'before_any_90', 'before_near_60', 'after_near_60', 'afterstart_near_60'):
    for nm, b in ((GROUPS[1][0], GROUPS[1][1]), (GROUPS[2][0], GROUPS[2][1]), (GROUPS[3][0], GROUPS[3][1])):
        ida = {id(s) for s in dl}; idb = {id(s) for s in b}
        c_ = set_diff(DD, lambda s: id(s) in ida, lambda s: id(s) in idb, lambda w, k=k: rate(w, k))
        TESTS.append(dict(measure=k, contrast=f'Daring on Loop minus {nm}', diff=r1(rate(dl, k) - rate(b, k)), ci=iv(c_), clear=clear(c_)))
        P('  ', TESTS[-1])
# excess over base, Daring on Loop minus the other groups
for k, bk in (('before_any_60', 'base_before_any_60'), ('before_near_60', 'base_before_near_60'), ('after_near_60', 'base_after_near_60')):
    st = lambda w, k=k, bk=bk: (rate(w, k) - basep(w, bk)) if basep(w, bk) is not None else None
    for nm, b in ((GROUPS[1][0], GROUPS[1][1]), (GROUPS[2][0], GROUPS[2][1])):
        ida = {id(s) for s in dl}; idb = {id(s) for s in b}
        c_ = set_diff(DD, lambda s: id(s) in ida, lambda s: id(s) in idb, st)
        TESTS.append(dict(measure=k + ' minus base', contrast=f'Daring on Loop minus {nm}', diff=r1(st(dl) - st(b)), ci=iv(c_), clear=clear(c_)))
        P('  ', TESTS[-1])

# ---------- the matching cases: sequence
P('\n--- Daring on Loop: sequences')
def describe(s, W=60):
    g = TL(s['game']); c = cap_of(s['game'], s['near_cap']); I = overlap(ivs(s, False), s['e0'] - W, s['e0']); In = overlap(ivs(s, True), s['e0'] - W, s['e0'])
    rows = []
    for a, b, sp in I:
        tp = g.pos(sp['tgt'], min(max(s['e0'], a), b)); src = g.pos(sp['src'], sp['act']) if sp['src'] else None
        nsrc = norm(s['map'], s['side'], *src) if src else None
        rows.append(dict(radar_ship=sp['ship'], radar_cls=ship_cls(s['game'], sp['src']) if sp['src'] else None, target=sp['tgt_ship'], lit_start_before_s=r1(s['e0'] - a), lit_end_before_s=r1(s['e0'] - b),
                         still_lit_at_activation=b >= s['e0'], radar_ship_to_cap_edge_m=r1((math.hypot(src[0] - c['x'], src[1] - c['z']) - c['r']) * WU, 0) if src else None,
                         radar_ship_cell=cell_name(*cell(s['map'], *nsrc)) if nsrc else None, radar_from_smoke=sp['src_in_smoke'], target_in_smoke=sp['tgt_in_smoke'],
                         target_to_cap_edge_m=r1((math.hypot(tp[0] - c['x'], tp[1] - c['z']) - c['r']) * WU, 0) if tp else None, target_to_smoke_m=r1(smoke_dist_m(s, tp), 0) if tp else None,
                         ambiguous=sp['amb'], radar_is_the_daring=sp['src'] == s['smoker_eid'],
                         src_n=[round(x, 1) for x in nsrc] if nsrc else None, tgt_n=[round(x, 1) for x in norm(s['map'], s['side'], *tp)] if tp else None))
    t1 = end_of(s)
    own0 = g.owner_at(s['near_cap'], s['e0']); ch = g.owner_changes(s['near_cap'], s['e0'], t1 + 60); chb = g.owner_changes(s['near_cap'], s['e0'] - 60, s['e0'])
    tr = g.tracks.get(s['smoker_eid']); i = tr.idx(s['e0']) if tr else None; hp = tr.health(s['e0']) if tr else None
    return dict(link=s['link'], slug=s['slug'], team=s['team'], grp=s['grp'], time=clock(s['e0']), e0=r1(s['e0']), cell=s['ncell_name'], cap=s['near_ncap'], cap_real=s['near_cap'], cap_edge_m=r1(s['near_cap_edge_m'], 0),
                near=bool(In), lit=rows, cap_owner_at_activation='neutral' if own0 is None else 'ours' if own0 == s['team'] else 'theirs',
                cap_changes_after=[(r1(t - s['e0']), 'ours' if o == s['team'] else 'neutral' if o is None else 'theirs') for t, o in ch],
                cap_changes_60s_before=[(r1(t - s['e0']), 'ours' if o == s['team'] else 'neutral' if o is None else 'theirs') for t, o in chb],
                we_invading_s=r1(g.invaded(s['near_cap'], s['team'], s['e0'], t1)), they_invading_s=r1(g.invaded(s['near_cap'], s['opponent'], s['e0'], t1)),
                daring_detected_at_activation=tr.det[i] if tr and i is not None else None, daring_health_pct=r1(100 * hp[0] / hp[1]) if hp and hp[1] else None, conc=round(s['conc']), one_sided=g.one_sided)
SEQ = [describe(s) for s in sorted(dl, key=lambda s: (s['game'], s['e0']))]
M = [x for x in SEQ if x['lit']]; U = [x for x in SEQ if not x['lit']]
for x in M:
    P(f"  {x['slug']} {x['team']} {x['time']} {x['cell']} cap {x['cap']} ({x['cap_owner_at_activation']}) near={x['near']} conc {x['conc']} detected={x['daring_detected_at_activation']} hp {x['daring_health_pct']} | changes after {x['cap_changes_after']} before {x['cap_changes_60s_before']}")
    for r in x['lit']: P('       ', {k: v for k, v in r.items() if k not in ('src_n', 'tgt_n')})
def seq_summary(v):
    if not v: return {}
    took = lambda x: x['cap_owner_at_activation'] != 'ours' and any(o == 'ours' for _, o in x['cap_changes_after'])
    lost = lambda x: x['cap_owner_at_activation'] != 'theirs' and any(o == 'theirs' for _, o in x['cap_changes_after'])
    return dict(n=len(v), cap_owner_at_activation=dict(C(x['cap_owner_at_activation'] for x in v)), cap=dict(C(x['cap'] for x in v)),
                we_took_it=sum(took(x) for x in v), not_ours_at_activation=sum(x['cap_owner_at_activation'] != 'ours' for x in v),
                enemy_took_it=sum(lost(x) for x in v), not_theirs_at_activation=sum(x['cap_owner_at_activation'] != 'theirs' for x in v),
                daring_detected_at_activation=sum(x['daring_detected_at_activation'] is True for x in v), detection_known=sum(x['daring_detected_at_activation'] is not None for x in v),
                median_conc=r1(med(x['conc'] for x in v), 0), median_time=clock(med(x['e0'] for x in v)), in_first_3_min=sum(x['e0'] < 180 for x in v))
lits = [r for x in M for r in x['lit']]
first = [min(x['lit'], key=lambda r: -r['lit_start_before_s']) for x in M]   # earliest lit span in the window
SUM = dict(matched=seq_summary(M), not_matched=seq_summary(U),
           radar_ships=dict(C(r['radar_ship'] for r in lits).most_common()), radar_class=dict(C(r['radar_cls'] for r in lits).most_common()), targets=dict(C(r['target'] for r in lits).most_common()),
           lit_spans=len(lits), radar_is_the_daring=sum(r['radar_is_the_daring'] for r in lits), radar_from_smoke=sum(r['radar_from_smoke'] for r in lits), target_in_smoke=sum(r['target_in_smoke'] for r in lits),
           ambiguous=sum(r['ambiguous'] for r in lits), still_lit_at_activation_smokes=sum(any(r['still_lit_at_activation'] for r in x['lit']) for x in M),
           median_lead_s=r1(med(r['lit_start_before_s'] for r in first)) if first else None, lead_range_s=[min(r['lit_start_before_s'] for r in first), max(r['lit_start_before_s'] for r in first)] if first else None,
           median_radar_ship_to_cap_edge_m=r1(med(r['radar_ship_to_cap_edge_m'] for r in lits if r['radar_ship_to_cap_edge_m'] is not None), 0) if lits else None,
           median_target_to_cap_edge_m=r1(med(r['target_to_cap_edge_m'] for r in lits if r['target_to_cap_edge_m'] is not None), 0) if lits else None,
           median_target_to_smoke_m=r1(med(r['target_to_smoke_m'] for r in lits if r['target_to_smoke_m'] is not None), 0) if lits else None,
           radar_ship_cells=dict(C(r['radar_ship_cell'] for r in lits).most_common(8)), matched_clans=clans_of(M), matched_near=sum(x['near'] for x in M),
           games_matched=len({x['slug'].rsplit('_', 1)[0] for x in M}), games_all=len({x['slug'].rsplit('_', 1)[0] for x in SEQ}))
SUM['loop_spans'] = sum(len(spans(k, t)) for k in G if G[k]['map'] == MAP for t in G[k]['teams']); SUM['loop_games'] = sum(1 for k in G if G[k]['map'] == MAP)
SUM['radar_cells_all'] = dict(C(r['radar_ship_cell'] for r in lits).most_common())
P('summary', SUM)
# timing of the Daring smokes and radar use by the minute (phase)
ph = {}
for nm, v in GROUPS[:4]:
    ph[nm] = dict(median_time=clock(med(s['e0'] for s in v)), first_3_min_pct=r1(pct(v, lambda s: s['e0'] < 180)), first_5_min_pct=r1(pct(v, lambda s: s['e0'] < 300)),
                  before_any_60_first_5_min=cs(cell_([s for s in v if s['e0'] < 300], 'before_any_60', 'base_before_any_60')), before_any_60_later=cs(cell_([s for s in v if s['e0'] >= 300], 'before_any_60', 'base_before_any_60')))
    P('phase', nm, ph[nm])
# team radar ships in Daring team-games on Loop
tg = sorted({(s['game'], s['team']) for s in dl})
radar_ships = C(p['ship'].replace('\xa0', ' ') for k, t in tg for p in G[k]['roster'].values() if p['team'] == t and p['radar_m'])
P('radar ships in Daring team-games on Loop', dict(radar_ships), '| team-games', len(tg), '| radar activations per team-game', r1(mean(len(TL(k).activations('radar', t)) for k, t in tg)),
  '| lit spans on enemy DD per team-game', r1(mean(len(spans(k, t)) for k, t in tg)))

# ---------- reverse view, as in round 5: after each time our radar lit an enemy destroyer on Loop, did a Daring of that team smoke within 60 s?
rev = dict(episodes=0, with_daring_alive=0, followed_60=0, followed_30=0, followed_90=0, alive_seconds=0.0, daring_smokes_in_alive_time=0)
EP = []   # one record per lit episode with a Daring alive: team, followed within 60 s, base (share of the Daring's alive time from which a Daring smoke follows within 60 s)
for k in sorted(G):
    if G[k]['map'] != MAP: continue
    g = TL(k)
    for team in G[k]['teams']:
        dar = [e for e, p in G[k]['roster'].items() if p['team'] == team and p['ship'] == 'Daring']
        if not dar: continue
        ep = []
        for sp in spans(k, team):
            if not ep or sp['start'] - ep[-1] > 30: ep.append(sp['start'])
        sm = [s['e0'] for s in BYG[k] if s['ship'] == 'Daring' and s['team'] == team]
        endt = G[k]['len'] or 1200
        for e in dar:
            d = g.tracks[e].death_t() if e in g.tracks else None
            rev['alive_seconds'] += min(endt, d) if d is not None else endt
        rev['daring_smokes_in_alive_time'] += len(sm)
        for t in ep:
            rev['episodes'] += 1
            alive = [e for e in dar if e in g.tracks and (g.tracks[e].death_t() is None or g.tracks[e].death_t() > t)]
            if not alive: continue
            rev['with_daring_alive'] += 1
            hi = max((min(endt, g.tracks[e].death_t()) if g.tracks[e].death_t() is not None else endt) for e in alive)
            EP.append(dict(team=team, grp='top' if team in TOP else 'rest', followed=any(t <= x <= t + 60 for x in sm), base=union_len([(x - 60, x) for x in sm], 0, hi) / hi if hi > 0 else None))
            for W in (30, 60, 90):
                if any(t <= x <= t + W for x in sm): rev[f'followed_{W}'] += 1
rev['base_daring_smokes_per_60s'] = r1(60 * rev['daring_smokes_in_alive_time'] / rev['alive_seconds'], 3) if rev['alive_seconds'] else None
rev['followed_60_pct'] = r1(100 * rev['followed_60'] / rev['with_daring_alive']) if rev['with_daring_alive'] >= 8 else None
st_ = lambda v: 100 * (mean(x['followed'] for x in v) - mean(x['base'] for x in v))
rev['base_followed_60_pct'] = r1(100 * mean(x['base'] for x in EP)) if EP else None
rev['followed_minus_base'] = r1(st_(EP)) if len(EP) >= 8 else None; rev['followed_minus_base_ci'] = iv(bstat(EP, st_)) if len(EP) >= 8 else None
rev['clans'] = len({x['team'] for x in EP}); rev['clans_txt'] = clans_of(EP)
P('reverse (round 5 style):', rev)

# ---------- second way for the headline: count straight from radar.csv rows, without the helper functions
chk = 0
for s in dl:
    g = TL(s['game']); hit = False
    for r in g.sensor:
        if r['kind'] == 'radar' and r['row'] == 'lit' and r['team'] == s['team'] and r['target_team'] == s['opponent'] and G[s['game']]['roster'].get(r['target_entity_id'], {}).get('ship_class') == 'Destroyer':
            if r['lit_start_elapsed_s'] <= s['e0'] and r['lit_end_elapsed_s'] >= s['e0'] - 60: hit = True
    chk += hit
P('check: Daring on Loop, before_any_60 counted straight from radar rows:', chk, 'vs', RES['Daring on Loop']['before_any_60']['k'])
# round 5 proxy on the same smokes (enemy ship lit inside its own smoke): how many of the round 5 rows the radar log also has
old = 0; old_in_new = 0
for s in dl:
    L = set()
    for y in BYG[s['game']]:
        if y['team'] != s['opponent']: continue
        for r in y['j']['radar_detections_in_smoke']:
            if ship_cls(s['game'], r['ship_entity']) == 'destroyer': L.add((round(r['seconds'], 1), r['ship_entity']))
    st = run_start(s['j']['match_id'], s['j']['game_no'], s['j']['primary_replay'])
    # the detection rows carry the replay clock of the run that recorded the enemy smoke; compare on elapsed seconds per run
    hit = False
    for y in BYG[s['game']]:
        if y['team'] != s['opponent']: continue
        sty = run_start(y['j']['match_id'], y['j']['game_no'], y['j']['primary_replay'])
        for r in y['j']['radar_detections_in_smoke']:
            if ship_cls(s['game'], r['ship_entity']) == 'destroyer' and s['e0'] - 60 <= r['seconds'] - sty <= s['e0']: hit = True
    old += hit; old_in_new += hit and s['f']['before_any_60']
P('check: round 5 proxy (enemy destroyer lit inside its own smoke, 60 s before) on Daring on Loop:', old, '| of those also found by the radar log:', old_in_new)
J = dict(note='C5 Loop. before_X_W = a radar lit span on an enemy destroyer, attributed to a radar of the smoking team, overlapped the W seconds before the smoke was activated. any = anywhere on the map; near = while that destroyer was within 3 km of the edge of the cap nearest to the smoke. '
              'base = share of the moments between the game\'s first and last smoke (cut at the smoker\'s death) at which the same test is true (exact, no random draws). earlier / later = the round 5 control windows (120 to 60 s before; 60 to 120 s after). '
              'after = same test for the W seconds after activation; afterstart = a lit span began in those W seconds.',
         groups=RES, tests=TESTS, sequences=SEQ, summary=SUM, phase=ph, reverse=rev, radar_ships_in_daring_team_games=dict(radar_ships),
         check=dict(before_any_60_straight_from_rows=chk, round5_proxy_hits=old, round5_proxy_hits_also_in_radar_log=old_in_new))
json.dump(J, open(os.path.join(HERE_N3, 'c5.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
open(os.path.join(HERE_N3, 'c5_out.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
