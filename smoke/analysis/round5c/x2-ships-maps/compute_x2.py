# Round 5c, worker x2: items 5 (B2), 6 (B3), 7 (C4 / C5 cap results on the timeline).
# Run: python -I -X utf8 compute_x2.py   -> writes ships-maps.json next to this file (then run write_x2.py).
# Read-only on the batch and on every other folder.
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from r5clib import *
import r5clib
import random, math, statistics

X2DIR = os.path.dirname(os.path.abspath(__file__))   # common.py also defines HERE; the star import overwrites it
S, G = load5c()
random.seed(5203)          # boot_stat / boot_diff draw from the global generator; diff_ci has its own seed
J = {}
DD = [s for s in S if s['cls'] == 'destroyer']
J['anchors'] = dict(smokes=len(S), dd=len(DD), dd_top=sum(s['grp'] == 'top' for s in DD), dd_rest=sum(s['grp'] == 'rest' for s in DD),
                    dd_early=sum(s['early'] for s in DD), dd_rates=death_rates(DD), died_not_ok=sum(not s['died_ok'] for s in S))

# ---------- helpers
def rd(x, d=1): return None if x is None else round(x, d)
def iv(c, d=1): return None if c is None or c[0] is None else [round(c[0], d), round(c[1], d)]
def died_cr100(ss):
    ok = [s for s in ss if s['died_ok']]; n = sum(s['n_cr_cov'] for s in ok)
    return 100.0 * sum(s['died_cr'] for s in ok) / n if n else None
def caught_cr100(ss):
    n = sum(s['n_cr_in'] for s in ss)
    return 100.0 * sum(s['caught_cr'] for s in ss) / n if n else None
DSTATS = dict(died=died100, caught=caught100, died_smoker=died_smoker100, caught_smoker=caught_smoker100, died_cr=died_cr100, caught_cr=caught_cr100)
def nclans(ss): return len({s['team'] for s in ss})
def val(ss, stat, d=1, min_n=8):
    """value and 95% interval of one statistic; None under 8 smokes; interval only with 3+ clans."""
    if len(ss) < min_n: return dict(v=None, ci=None)
    return dict(v=rd(stat(ss), d), ci=iv(boot_stat(ss, stat), d) if nclans(ss) >= 3 else None)
def drow(label, ss, stats=DSTATS):
    r = dict(label=label, n=len(ss), tag=tag(len(ss)), clans=nclans(ss), top6=sum(s['grp'] == 'top' for s in ss), rest=sum(s['grp'] == 'rest' for s in ss),
             n_died_base=sum(s['died_ok'] for s in ss), died_ships=sum(s['died'] for s in ss if s['died_ok']), caught_ships=sum(s['caught'] for s in ss),
             died_smoker_n=sum(s['died_smoker'] for s in ss if s['died_ok']), caught_smoker_n=sum(s['caught_smoker'] for s in ss),
             n_cr_cov=sum(s['n_cr_cov'] for s in ss if s['died_ok']), n_cr_in=sum(s['n_cr_in'] for s in ss),
             died_cr_n=sum(s['died_cr'] for s in ss if s['died_ok']), caught_cr_n=sum(s['caught_cr'] for s in ss))
    for k, st in stats.items(): r[k] = val(ss, st)
    return r
def contrast(label, a, b, stats, d=1):
    r = dict(label=label, n_a=len(a), n_b=len(b))
    for k, st in stats.items():
        va, vb = (st(a) if len(a) >= 8 else None), (st(b) if len(b) >= 8 else None)
        if va is None or vb is None: r[k] = dict(v=None, ci=None, clear=False); continue
        c = diff_ci(a, b, st); r[k] = dict(v=rd(va - vb, d), ci=iv(c, d), clear=bool(c[0] is not None and c[0] * c[1] > 0))
    return r
def tvr(label, ss, stats, d=1):
    t = [s for s in ss if s['grp'] == 'top']; r_ = [s for s in ss if s['grp'] == 'rest']
    r = dict(label=label, n_top=len(t), n_rest=len(r_), clans_top=nclans(t), clans_rest=nclans(r_))
    for k, st in stats.items():
        va, vb = (st(t) if len(t) >= 8 else None), (st(r_) if len(r_) >= 8 else None)
        o = dict(top=rd(va, d), rest=rd(vb, d), v=None, ci=None, clear=False)
        if va is not None and vb is not None:
            c = boot_diff(ss, st); o.update(v=rd(va - vb, d), ci=iv(c, d), clear=bool(c[0] is not None and c[0] * c[1] > 0))
        r[k] = o
    return r
def kn(ss, key):
    """count True, count applicable, percent (None under 8 applicable)."""
    v = [s[key] for s in ss if s[key] is not None]; k = sum(1 for x in v if x)
    return dict(k=k, n=len(v), pct=rd(100.0 * k / len(v)) if len(v) >= 8 else None)
def cap_block(ss):
    o = {}
    for suf in ('_c', '_n'):
        own = C(s['own' + suf] for s in ss); ours = [s for s in ss if s['own' + suf] == 'ours']
        o[suf] = dict(ours=own['ours'], neutral=own['neutral'], theirs=own['theirs'], we_took=kn(ss, 'we_took' + suf), enemy_took=kn(ss, 'enemy_took' + suf),
                      enemy_took_when_ours=kn(ours, 'enemy_took' + suf))
    o['same_cap'] = sum(s['cap'] == s['near_cap'] for s in ss)
    return o
def fixed_cap(s, cap):
    """owner / we took / enemy took / enemy capturing, on one named real cap letter, same rules as the library (60 s after dispersal)."""
    g = TL(s['game'])
    if cap not in g.caps: return dict(own=None, we=None, en=None, inv=None)
    o = g.owner_at(cap, s['e0']); we, en = r5clib._took(g, cap, s['e0'], s['end'] + CAP_GRACE_S, s['team'], s['opponent'])
    return dict(own='neutral' if o is None else 'ours' if o == s['team'] else 'theirs', we=we, en=en, inv=g.invaded(cap, s['opponent'], s['e0'], s['end']))
def real_letter(s, letter):
    """Real cap letter of the cap that sits at normalized letter `letter` for this smoke's team."""
    g = G[s['game']]
    return next((c['cap'] for c in g['caps'] if ncap_name(g, s['map'], s['side'], c['cap']) == letter), None)
for s in S:
    f = fixed_cap(s, s['near_cap']); s['inv_n'] = f['inv']; s['inv_n_any'] = None if f['inv'] is None else f['inv'] > 0
def meank(k):
    def st(ss):
        v = [s[k] for s in ss if s[k] is not None]
        return sum(v) / len(v) if v else None
    return st
def medk(k):
    def st(ss):
        v = [s[k] for s in ss if s[k] is not None]
        return statistics.median(v) if v else None
    return st
def pctf(f):
    return lambda ss: 100.0 * sum(1 for s in ss if f(s)) / len(ss) if ss else None

# ================= item 5: B2 getaway smokes
is_it = lambda s: s['kind'] == 'exhaust' and s['cls'] == 'cruiser'
is_bb = lambda s: s['cls'] == 'battleship'
is_get = lambda s: s['kind'] == 'exhaust' or s['cls'] == 'battleship'
is_ord = lambda s: s['cls'] == 'cruiser' and s['kind'] != 'exhaust'
sel = lambda f: [s for s in S if f(s)]
B2G = [('Napoli', lambda s: s['ship'] == 'Napoli'), ('Venezia', lambda s: s['ship'] == 'Venezia'), ('Italian cruisers together', is_it),
       ('C. Colombo (battleship)', lambda s: s['ship'] == 'C. Colombo'), ('Conte Verde (battleship)', lambda s: s['ship'] == 'Conte Verde'), ('All battleships', is_bb),
       ('Baseline: all smokes', lambda s: True), ('Baseline: all other smokes (not exhaust, not battleship)', lambda s: not is_get(s)),
       ('Baseline: cruiser smokers with ordinary smoke', is_ord), ('Baseline: all cruiser smokers', lambda s: s['cls'] == 'cruiser'),
       ('Baseline: destroyer smokers', lambda s: s['cls'] == 'destroyer')]
# undetected share from the smoker's own track
for s in S:
    tr = TL(s['game']).tracks.get(s['smoker_eid'])
    n = u = nin = uin = nnone = nsamp = 0
    if tr:
        for i, t in enumerate(tr.t):
            if t < s['e0'] or t > s['end'] or not tr.alive[i]: continue
            nsamp += 1
            if tr.det[i] is None: nnone += 1; continue
            n += 1; u += tr.det[i] is False
            if tr.x[i] is not None and in_smoke(s, (tr.x[i], tr.z[i])):
                nin += 1; uin += tr.det[i] is False
    s['u_samples'] = nsamp; s['u_none'] = nnone
    s['u_life'] = 100.0 * u / n if n else None           # undetected share of the smoke's life (track)
    s['u_in'] = 100.0 * uin / nin if nin else None       # undetected share of the time the smoker's track is inside the smoke
    s['in_share'] = 100.0 * nin / n if n else None       # share of the smoke's life the smoker is inside it
    # round 5's two columns, recomputed as round 5 did (batch fields)
    me = next((x for x in s['j']['smokees'] if x['role'] == 'smoker'), None)
    life = s['t1'] - s['t0'] if s['t1'] and s['t1'] > s['t0'] else None
    cov = min(100, 100 * me['seconds_concealed'] / life) if me and life else None
    s['r5_undet_life'] = cov * s['undetected_pct'] / 100 if cov is not None and s['undetected_pct'] is not None else None
b2 = dict(rows=[], undet=[], contrasts=[], undet_contrasts=[])
USTATS = dict(track_life_mean=meank('u_life'), track_in_mean=meank('u_in'), batch_covered_mean=meank('undetected_pct'), r5_life_mean=meank('r5_undet_life'))
for name, f in B2G:
    ss = sel(f); b2['rows'].append(drow(name, ss, {k: DSTATS[k] for k in ('died', 'caught', 'died_smoker', 'caught_smoker')}))
    u = dict(label=name, n=len(ss), n_track=sum(s['u_life'] is not None for s in ss), dropped=sum(s['u_life'] is None for s in ss),
             with_some_none=sum(1 for s in ss if s['u_none'] > 0 and s['u_life'] is not None), n_in=sum(s['u_in'] is not None for s in ss),
             track_life_median=rd(medk('u_life')(ss)) if len(ss) >= 8 else None, track_in_median=rd(medk('u_in')(ss)) if len(ss) >= 8 else None,
             batch_covered_median=rd(medk('undetected_pct')(ss)) if len(ss) >= 8 else None, in_share_mean=rd(meank('in_share')(ss)) if len(ss) >= 8 else None,
             fully_detected_pct=rd(pctf(lambda s: s['u_life'] is not None and s['u_life'] < 5)([s for s in ss if s['u_life'] is not None])) if len(ss) >= 8 else None,
             fully_undetected_pct=rd(pctf(lambda s: s['u_life'] > 95)([s for s in ss if s['u_life'] is not None])) if len(ss) >= 8 else None)
    for k, st in USTATS.items(): u[k] = val(ss, st)
    b2['undet'].append(u)
PAIRS = [('Italian cruisers minus cruisers with ordinary smoke', is_it, is_ord), ('Italian cruisers minus all other smokes', is_it, lambda s: not is_get(s)),
         ('Battleships minus cruisers with ordinary smoke', is_bb, is_ord), ('Battleships minus all other smokes', is_bb, lambda s: not is_get(s)),
         ('Battleships minus Italian cruisers', is_bb, is_it)]
for name, fa, fb in PAIRS:
    a, b = sel(fa), sel(fb)
    b2['contrasts'].append(contrast(name, a, b, {k: DSTATS[k] for k in ('died', 'caught', 'died_smoker', 'caught_smoker')}))
    b2['undet_contrasts'].append(contrast(name, a, b, USTATS))
b2['tvr'] = [tvr('Italian cruisers', sel(is_it), {k: DSTATS[k] for k in ('died', 'caught', 'died_smoker', 'caught_smoker')}),
             tvr('All battleships', sel(is_bb), {k: DSTATS[k] for k in ('died', 'caught', 'died_smoker', 'caught_smoker')}),
             tvr('Italian cruisers, undetected', sel(is_it), dict(track_life_mean=USTATS['track_life_mean'])),
             tvr('All battleships, undetected', sel(is_bb), dict(track_life_mean=USTATS['track_life_mean']))]
b2['who_died'] = {nm: dict(died=dict(C(('smoker' if c['is_smoker'] else c['cls']) for s in sel(f) if s['died_ok'] for c in s['died_list'])),
                           caught=dict(C(('smoker' if d['is_smoker'] else d['cls']) for s in sel(f) for d in s['dead']))) for nm, f in (('Italian cruisers', is_it), ('All battleships', is_bb))}
b2['clans'] = {nm: clan_counts(sel(f)) for nm, f in B2G[:6]}
b2['dropped_total'] = sum(s['u_life'] is None for s in S); b2['dropped_one_sided'] = sum(s['u_life'] is None and not s['died_ok'] for s in S)
b2['some_none_total'] = sum(1 for s in S if s['u_none'] > 0 and s['u_life'] is not None)
b2['samples'] = dict(total=sum(s['u_samples'] for s in S), none=sum(s['u_none'] for s in S))
b2['no_inside_sample'] = sum(s['u_life'] is not None and s['u_in'] is None for s in S)
J['B2'] = b2
print('B2 done')

# ================= item 6: B3 long smokes
LONG = ('Somers', 'Gearing', 'Harugumo', 'Delny')
of = lambda sh: [s for s in S if s['ship'] == sh]
long_all = [s for s in S if s['ship'] in LONG]; sitters = [s for s in S if s['habit'] == 'cap sitters']
B3G = [(sh, of(sh)) for sh in LONG] + [('All four', long_all), ('For comparison: cap sitters (Daring, Z-42, Gdansk, Grozovoi, Shimakaze)', sitters), ('For comparison: all destroyer smokes', DD)]
b3 = dict(rows=[drow(n, ss) for n, ss in B3G])
T4 = {k: DSTATS[k] for k in ('died', 'caught', 'died_smoker', 'caught_smoker')}
b3['long_minus_sitters'] = contrast('Long-smoke ships minus cap sitters', long_all, sitters, DSTATS)
b3['tvr'] = [tvr(n, ss, DSTATS) for n, ss in B3G[:5]] + [tvr(n, ss, T4) for n, ss in B3G[5:]]
ws = []
for n, ss in B3G[:5] + [('For comparison: all destroyer smokes', DD)]:
    for wl, lab in ((True, 'games won'), (False, 'games lost')):
        sub = [s for s in ss if s['win'] == wl]
        r = tvr(f'{n} | {lab}', sub, T4); r['ship'] = n; r['result'] = lab
        ws.append(r)
    t = [s for s in ss if s['grp'] == 'top']; r_ = [s for s in ss if s['grp'] == 'rest']
    ws.append(dict(ship=n, result='share of smokes laid in games won', top=rd(pctf(lambda s: s['win'])(t)) if t else None, rest=rd(pctf(lambda s: s['win'])(r_)) if r_ else None))
b3['win_split'] = ws
# won minus lost inside each group (four ships together)
b3['won_minus_lost'] = [contrast(f'{lab}: games won minus games lost', [s for s in long_all if s['grp'] == g and s['win']], [s for s in long_all if s['grp'] == g and not s['win']], T4)
                        for g, lab in (('top', 'Top 6'), ('rest', 'Rest'))]
b3['clans'] = {sh: clan_counts(of(sh)) for sh in LONG}
J['B3'] = b3
print('B3 done')

# ================= item 7a: high-paying cells
spots = {x.get('id'): x for x in json.load(open(os.path.join(R5C, '..', 'round5b', 'spots.json'), encoding='utf-8'))['spots']}
CELLS = [('sg-cell-1', 'Sleeping Giant', ['G1']), ('hs-cell-1', 'Hotspot', ['G10', 'H10']), ('sof-cell-1', 'Sea of Fortune', ['F9', 'G9']),
         ('c5-lp-f8', 'Loop', ['F8']), ('c5-lp-f10', 'Loop', ['F10'])]
CAPKEYS = ('we_took_c', 'enemy_took_c', 'we_took_n', 'enemy_took_n')
c7a = []
for sid, m, cells in CELLS:
    dd = [s for s in DD if s['map'] == m]; mem = [s for s in dd if s['ncell_name'] in cells]; rest = [s for s in dd if s['ncell_name'] not in cells]
    sp = spots[sid]
    r = dict(id=sid, map=m, cells=cells, n=len(mem), tag=tag(len(mem)), top6=sum(s['grp'] == 'top' for s in mem), rest=sum(s['grp'] == 'rest' for s in mem), clans=nclans(mem),
             clan_text=clan_counts(mem), games=len({s['game'] for s in mem}), early=sum(s['early'] for s in mem),
             conc=round(mean(s['conc'] for s in mem)), conc_r5b=sp['concealed_damage_per_smoke'], n_r5b=sp['n'], conc_rest_of_map=round(mean(s['conc'] for s in rest)),
             conc_gap_ci=iv(diff_ci(mem, rest, lambda v: mean(s['conc'] for s in v) if v else None), 0),
             r5b_cap_taken_pct=sp.get('cap_taken_pct'), r5b_cap_taken_n=sp.get('cap_taken_n'), r5b_deaths_per_100=sp['deaths_per_100'],
             caps=cap_block(mem), caps_rest=cap_block(rest), near_caps=dict(C(s['near_ncap'] for s in mem)), contested_caps=dict(C(s['ncap'] for s in mem)),
             deaths=drow('cell', mem, T4), deaths_rest=drow('rest of map', rest, T4), n_map=len(dd))
    r['vs_rest'] = contrast('cell minus rest of the map', mem, rest, dict({k: share_stat(k, 8) for k in CAPKEYS}, **T4))
    t = [s for s in mem if s['grp'] == 'top']; r_ = [s for s in mem if s['grp'] == 'rest']
    r['tvr'] = {k: dict(top=kn(t, k), rest=kn(r_, k), ci=iv(boot_diff(mem, share_stat(k, 8))) if kn(t, k)['n'] >= 8 and kn(r_, k)['n'] >= 8 else None) for k in CAPKEYS}
    r['tvr_deaths'] = tvr('cell', mem, T4)
    c7a.append(r)
J['C7a'] = c7a
print('7a done')

# ================= item 7b: Sleeping Giant cap B
sg = [s for s in S if s['map'] == 'Sleeping Giant']; near = [s for s in sg if s['near_cap_edge_m'] <= 2000]
def place_row(label, ss):
    ours = [s for s in ss if s['own_n'] == 'ours']
    return dict(label=label, n=len(ss), tag=tag(len(ss)), top6=sum(s['grp'] == 'top' for s in ss), rest=sum(s['grp'] == 'rest' for s in ss), clans=nclans(ss), caps=cap_block(ss),
                enemy_in_cap=kn(ss, 'inv_n_any'), enemy_in_cap_when_ours=kn(ours, 'inv_n_any'), enemy_in_cap_median_s=rd(med([s['inv_n'] for s in ss if s['inv_n']]), 0) if any(s['inv_n'] for s in ss) else None,
                conc=round(mean(s['conc'] for s in ss)) if ss else None, deaths=drow(label, ss, T4))
c7b = dict(n_map=len(sg), n_near=len(near), rows=[place_row(f'Cap {L}', [s for s in near if s['near_ncap'] == L]) for L in 'ABCD'])
B = [s for s in near if s['near_ncap'] == 'B']; oth = [s for s in near if s['near_ncap'] != 'B']
c7b['rows'].append(place_row('Other caps together (A, C, D)', oth))
OWN_ST = dict(ours_share=pctf(lambda s: s['own_n'] == 'ours'), enemy_in_cap=share_stat('inv_n_any', 8))
c7b['b_vs_other'] = contrast('B minus other caps', B, oth, dict({k: share_stat(k, 8) for k in ('enemy_took_n', 'we_took_n', 'enemy_took_c', 'we_took_c')}, **OWN_ST, **T4))
c7b['ours_share'] = dict(B=val(B, OWN_ST['ours_share']), other=val(oth, OWN_ST['ours_share']))
c7b['B'] = dict(cls=dict(C(s['cls'] for s in B)), ships=dict(C(s['ship'] for s in B).most_common()), habits=dict(C(s['habit'] for s in B)), pp=dict(C(s['pp'] for s in B).most_common()),
                inside=sum(s['near_cap_edge_m'] < 0 for s in B), clan_text=clan_counts(B), clan_text_ours=clan_counts([s for s in B if s['own_n'] == 'ours']),
                own_snapshot=dict(C(s['near_own'] for s in B)), own_agree=sum(s['near_own'] == s['own_n'] for s in B),
                ours_by_grp={g: sum(1 for s in B if s['grp'] == g and s['own_n'] == 'ours') for g in ('top', 'rest')},
                enemy_took_list=[dict(link=s['link'], team=s['team'], ship=s['ship'], own=s['own_n']) for s in B if s['enemy_took_n']],
                top=place_row('B, Top 6', [s for s in B if s['grp'] == 'top']), rest=place_row('B, Rest', [s for s in B if s['grp'] == 'rest']))
c7b['share_of_map'] = tvr('share of map smokes within 2 km of B', sg, dict(share=pctf(lambda s: s['near_ncap'] == 'B' and s['near_cap_edge_m'] <= 2000)))
c7b['ours_tvr'] = tvr('B ours at activation', B, dict(share=OWN_ST['ours_share']))
J['C7b'] = c7b
print('7b done')

# ================= item 7c: Mountain Range radar at B
mr = [s for s in S if s['map'] == 'Mountain Range']; mrB = [s for s in mr if s['near_ncap'] == 'B']
tagr = lambda s: bool(s['radar_play'] or s['off_radar']); logr = lambda s: s['radar_pressed']
N2 = lambda s: s['near_cap_edge_m'] <= 2000
SETS = [('Radar smokes (round 5 tags), nearest cap B', [s for s in mrB if tagr(s)]), ('Other smokes, nearest cap B (no radar tag)', [s for s in mrB if not tagr(s)]),
        ('Radar smokes (round 5 tags), within 2 km of B', [s for s in mrB if tagr(s) and N2(s)]), ('Other smokes within 2 km of B (no radar tag)', [s for s in mrB if not tagr(s) and N2(s)]),
        ('Radar pressed from the smoke (radar log), nearest cap B', [s for s in mrB if logr(s)]), ('Other smokes, nearest cap B (no radar pressed)', [s for s in mrB if not logr(s)]),
        ('Radar pressed from the smoke (radar log), within 2 km of B', [s for s in mrB if logr(s) and N2(s)]), ('Other smokes within 2 km of B (no radar pressed)', [s for s in mrB if not logr(s) and N2(s)]),
        ('Radar smokes (round 5 tags), other maps, nearest cap', [s for s in S if tagr(s) and s['map'] != 'Mountain Range']),
        ('Radar pressed (radar log), other maps, nearest cap', [s for s in S if logr(s) and s['map'] != 'Mountain Range'])]
c7c = dict(n_map=len(mr), n_B=len(mrB), rows=[place_row(n, ss) for n, ss in SETS])
c7c['overlap'] = dict(tag=sum(tagr(s) for s in mrB), log=sum(logr(s) for s in mrB), both=sum(tagr(s) and logr(s) for s in mrB), tag_only=sum(tagr(s) and not logr(s) for s in mrB), log_only=sum(logr(s) and not tagr(s) for s in mrB))
CK = {k: share_stat(k, 8) for k in ('enemy_took_n', 'we_took_n')}
c7c['contrasts'] = [contrast('Radar (tags) minus other, nearest cap B', SETS[0][1], SETS[1][1], dict(CK, **OWN_ST, **T4)),
                    contrast('Radar (log) minus other, nearest cap B', SETS[4][1], SETS[5][1], dict(CK, **OWN_ST, **T4)),
                    contrast('Radar at B (tags) minus radar on other maps', SETS[0][1], SETS[8][1], dict(CK, **OWN_ST))]
rb = SETS[0][1]
c7c['list'] = [dict(link=s['link'], slug=s['slug'], team=s['team'], ship=s['ship'], t=round(s['e0']), own=s['own_n'], own_snapshot=s['near_own'], enemy_took=s['enemy_took_n'], we_took=s['we_took_n'],
                    enemy_in_cap_s=rd(s['inv_n'], 0), edge_m=round(s['near_cap_edge_m']), tag=tagr(s), pressed=logr(s), same_cap=s['cap'] == s['near_cap']) for s in sorted(mrB, key=lambda s: s['e0']) if tagr(s) or logr(s)]
c7c['clan_text'] = dict(tag=clan_counts(rb), log=clan_counts(SETS[4][1]))
c7c['ships'] = dict(tag=dict(C(s['ship'] for s in rb).most_common()), log=dict(C(s['ship'] for s in SETS[4][1]).most_common()))
c7c['lost_games'] = len({s['game'] for s in rb if s['own_n'] == 'ours' and s['enemy_took_n']})
c7c['share_tvr'] = tvr('radar smokes at B as a share of the map smokes', mr, dict(tag=pctf(lambda s: tagr(s) and s['near_ncap'] == 'B'), log=pctf(lambda s: logr(s) and s['near_ncap'] == 'B')))
c7c['whole_map'] = {L: place_row(f'All smokes, nearest cap {L}', [s for s in mr if s['near_ncap'] == L]) for L in sorted({s['near_ncap'] for s in mr})}
J['C7c'] = c7c
print('7c done')

# ================= item 7d: Loop cap sitters at B
shape = spots['c5-lp-sitters-b']['shape']
def in_ell(sh, s):
    size = MAPS[s['map']]['space_size']; cx, cz = sh['u'] * size - size / 2, size / 2 - sh['v'] * size
    r1, r2 = sh['ru'] * size, sh['rv'] * size; ang = -math.radians(sh['angle_deg'])
    dx, dz = s['nx'] - cx, s['nz'] - cz; ca, sa = math.cos(ang), math.sin(ang)
    a, b = dx * ca + dz * sa, -dx * sa + dz * ca
    return (a / r1) ** 2 + (b / r2) ** 2 <= 1.0
lp = [s for s in DD if s['map'] == 'Loop']; sit = [s for s in lp if s['habit'] == 'cap sitters']; mem = [s for s in sit if in_ell(shape, s)]
for s in mem:
    f = fixed_cap(s, real_letter(s, 'B')); s['ownB'] = f['own']; s['we_took_B'] = f['we']; s['enemy_took_B'] = f['en']; s['invB'] = None if f['inv'] is None else f['inv'] > 0
def d_row(label, ss):
    r = place_row(label, ss)
    r['B'] = dict(ours=sum(s['ownB'] == 'ours' for s in ss), neutral=sum(s['ownB'] == 'neutral' for s in ss), theirs=sum(s['ownB'] == 'theirs' for s in ss),
                  we_took=kn(ss, 'we_took_B'), enemy_took=kn(ss, 'enemy_took_B'), enemy_took_when_ours=kn([s for s in ss if s['ownB'] == 'ours'], 'enemy_took_B'), enemy_in_cap=kn(ss, 'invB'))
    r['near_caps'] = dict(C(s['near_ncap'] for s in ss)); r['contested_caps'] = dict(C(s['ncap'] for s in ss)); r['ships'] = dict(C(s['ship'] for s in ss).most_common())
    return r
c7d = dict(n_sitters=len(sit), n_sitters_top=sum(s['grp'] == 'top' for s in sit), n_sitters_rest=sum(s['grp'] == 'rest' for s in sit),
           rows=[d_row('All 28', mem), d_row('Top 6', [s for s in mem if s['grp'] == 'top']), d_row('Rest', [s for s in mem if s['grp'] == 'rest'])],
           clan_text=clan_counts(mem), conc_r5b=spots['c5-lp-sitters-b']['concealed_damage_per_smoke'], deaths_r5b=spots['c5-lp-sitters-b']['deaths_per_100'])
c7d['tvr_deaths'] = tvr('spot', mem, T4)
c7d['tvr_caps'] = tvr('spot', mem, {k: share_stat(k, 8) for k in ('we_took_B', 'enemy_took_B', 'we_took_n', 'enemy_took_n', 'we_took_c', 'enemy_took_c')})
c7d['tvr_conc'] = tvr('spot', mem, dict(conc=lambda v: mean(s['conc'] for s in v) if v else None), 0)
c7d['tvr_ours'] = tvr('spot', mem, dict(share=pctf(lambda s: s['ownB'] == 'ours')))
# for reference: the Loop cap sitters outside the spot
out = [s for s in sit if not in_ell(shape, s)]
c7d['outside'] = place_row('Cap sitters on Loop outside the spot', out)
c7d['in_vs_out'] = contrast('In the spot minus the other Loop cap-sitter smokes', mem, out, dict({k: share_stat(k, 8) for k in ('we_took_n', 'enemy_took_n')}, **T4))
J['C7d'] = c7d
print('7d done')

json.dump(J, open(os.path.join(X2DIR, 'ships-maps.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print('written')
