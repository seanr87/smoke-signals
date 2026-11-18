# Round 5b, worker n1: C1 "enemy took the cap" rebuilt from the cap timeline, compared with the round 5 snapshot version,
# cap_defended follow-up, invaders, and ribbons per smoke.
# Run: python -I -X utf8 n1_c1.py   (writes out-c1.md, c1.json, enemy-took.csv, figure n1-enemy-took-snapshot-vs-timeline)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
from tl import *
HERE_ = os.path.dirname(os.path.abspath(__file__))
S, G = load5(); add_times(S)
random.seed(51)
OUT = []; J = {}
def P(*a):
    s = ' '.join(str(x) for x in a); OUT.append(s); print(s)
def share(key):
    return lambda ss: 100 * sum(1 for s in ss if key(s)) / len(ss) if ss else None
def row_share(ss, key):
    st = share(key); lo, hi = boot_stat(ss, st)
    return len(ss), st(ss), lo, hi
def grp_rows(ss, key, label):
    top = [s for s in ss if s['grp'] == 'top']; rest = [s for s in ss if s['grp'] == 'rest']
    st = share(key); d = boot_diff(ss, st)
    a = row_share(ss, key); t = row_share(top, key); r = row_share(rest, key)
    rec = dict(what=label, n=a[0], pct=round(a[1], 1), ci=[round(a[2], 1), round(a[3], 1)], top6_n=t[0], top6_pct=round(t[1], 1), rest_n=r[0], rest_pct=round(r[1], 1),
               gap=round(t[1] - r[1], 1), gap_ci=[round(d[0], 1), round(d[1], 1)], gap_clear=d[0] * d[1] > 0)
    return [label, a[0], f'{a[1]:.1f}% ({a[2]:.1f} to {a[3]:.1f})', f'{t[1]:.1f}% (n {t[0]})', f'{r[1]:.1f}% (n {r[0]})', f'{t[1]-r[1]:+.1f} ({ci(d, "{:+.1f}")})'], rec
tf = lambda v: '' if v is None else 'yes' if v else 'no'
OLD = json.load(open(os.path.join(ROOT, 'smoke', 'analysis', 'round5', 'part-c1', 'caps.json'), encoding='utf-8')) if os.path.exists(os.path.join(ROOT, 'smoke', 'analysis', 'round5', 'part-c1', 'caps.json')) \
    else json.load(open(os.path.join(R5, 'part-c1', 'caps.json'), encoding='utf-8'))

# ---------------------------------------------------------------- timeline fields on every smoke
GRACE = 60
for s in S:
    g = TL(s['game']); cap = s['near_cap']
    s['end'] = s['e1'] if s['e1'] is not None else s['e0'] + (s['emission_s'] or 0) + (s['life_s'] or 0)
    o = g.owner_at(cap, s['e0']); s['tl_own'] = 'neutral' if o is None else 'ours' if o == s['team'] else 'theirs'
    dur = g.owner_changes(cap, s['e0'], s['end']); aft = g.owner_changes(cap, s['end'], s['end'] + GRACE)
    for who, side, own in (('enemy', s['opponent'], 'theirs'), ('we', s['team'], 'ours')):
        na = s['tl_own'] == own
        d = any(x[1] == side for x in dur); a = any(x[1] == side for x in aft)
        s[f'{who}_during'] = None if na else d
        s[f'{who}_60'] = None if na else (d or a)            # during the smoke or in the 60 s after
        s[f'{who}_after_only'] = None if na else (a and not d)
        s[f'{who}_t'] = next((x[0] for x in dur + aft if x[1] == side), None)
NEAR = lambda s: s['near_cap_edge_m'] <= 2000
P('# C1 from the cap timeline (round 5b, worker n1)\n')
P(f'Smokes: {len(S)}. End of a smoke = dispersal time; {sum(s["e1"] is None for s in S)} smokes had no dispersal time (replay ended first) and use activation + emission + puff life.')
mm = [s for s in S if s['tl_own'] != s['near_own']]
P(f'Owner of the nearest cap at activation, timeline vs the round 5 stored value: {len(S) - len(mm)} of {len(S)} agree; the {len(mm)} that differ: ' +
  '; '.join(f'{s["slug"]} (timeline {s["tl_own"]}, stored {s["near_own"]})' for s in mm) + ' (the cap flipped within a second of the activation).')
P('Owner at activation (timeline):', dict(C(s['tl_own'] for s in S)))
fm = sum(1 for s in S if TL(s['game']).frame_letter(s['team'], s['near_cap']) != s['near_ncap'])
P(f'Team-frame cap letter, timeline file vs r5lib: {fm} mismatches of {len(S)}.')

# second way: straight from the csv rows, own code
def raw_took(s, side, grace):
    g = TL(s['game']); rows = sorted(g.caps[s['near_cap']], key=lambda e: e[0])
    cur = None; hit = False
    for t, o, _ in rows:
        if t <= s['e0']: cur = o; continue
        if t > s['end'] + grace: break
        if o == side and cur != side: hit = True
        cur = o
    start = None
    for t, o, _ in rows:
        if t <= s['e0']: start = o
    return None if start == side else hit
bad = sum(1 for s in S if raw_took(s, s['opponent'], 60) != s['enemy_60'] or raw_took(s, s['opponent'], 0) != s['enemy_during'] or raw_took(s, s['team'], 60) != s['we_60'] or raw_took(s, s['team'], 0) != s['we_during'])
P(f'Second computation straight from the caps_timeline rows (own loop, not tl.owner_changes): {len(S) - bad} of {len(S)} smokes agree on all four yes/no values.')
J['checks'] = dict(owner_at_activation_mismatch=len(mm), frame_letter_mismatch=fm, second_way_mismatch=bad)

# ---------------------------------------------------------------- three ways
P('\n## Enemy took the nearest cap: three ways\n')
app = [s for s in S if s['enemy_60'] is not None]; wapp = [s for s in S if s['we_60'] is not None]
def cnt(ss, k): return sum(1 for s in ss if s[k])
rows = []; J['three_ways'] = {}
for who, ss in (('enemy', app), ('we', wapp)):
    n = len(ss); d = cnt(ss, f'{who}_during'); a = cnt(ss, f'{who}_after_only'); b = cnt(ss, f'{who}_60')
    rows.append([('enemy took the nearest cap' if who == 'enemy' else 'we took the nearest cap'), n, f'{d} ({100*d/n:.1f}%)', f'{a} ({100*a/n:.1f}%)', f'{b} ({100*b/n:.1f}%)'])
    J['three_ways'][who] = dict(applicable=n, not_applicable=len(S) - n, during=d, during_pct=round(100 * d / n, 1), after_only=a, after_only_pct=round(100 * a / n, 1), within_60=b, within_60_pct=round(100 * b / n, 1))
P(md_table(['what', 'applicable smokes', 'strictly while the smoke stood (grace 0)', 'only in the 60 s after', 'during or within 60 s (grace 60)'], rows))
P(f'Not applicable (cap already the enemy\'s at activation): {len(S) - len(app)}; (cap already ours, for "we took"): {len(S) - len(wapp)}.')
rows = []; J['grace'] = []
for gr in (0, 10, 30, 60, 120):
    y = sum(1 for s in app if raw_took(s, s['opponent'], gr)); w = sum(1 for s in wapp if raw_took(s, s['team'], gr))
    o = next((x for x in OLD['enemy_took']['grace'] if x['grace_s'] == gr), None)
    rows.append([f'{gr} s', y, len(app) - y, f'{100*y/len(app):.1f}%', f'{o["yes"]} ({o["pct"]}%)' if o else '-', w, f'{100*w/len(wapp):.1f}%'])
    J['grace'].append(dict(grace_s=gr, yes=y, no=len(app) - y, pct=round(100 * y / len(app), 1), we_yes=w, we_pct=round(100 * w / len(wapp), 1), round5_yes=o['yes'] if o else None, round5_pct=o['pct'] if o else None))
P('\nGrace after the smoke clears (timeline):'); P(md_table(['grace', 'enemy took: yes', 'no', 'yes share', 'round 5 snapshot yes (share)', 'we took: yes', 'yes share'], rows))
lag = [s['enemy_t'] - s['end'] for s in app if s['enemy_after_only']]
P(f'Flips in the 60 s after: median {med(lag):.0f} s after the smoke cleared (quartiles {q(lag,.25):.0f} to {q(lag,.75):.0f}).')
dl = [s['enemy_t'] - s['e0'] for s in app if s['enemy_during']]
P(f'Flips during the smoke: median {med(dl):.0f} s after activation (quartiles {q(dl,.25):.0f} to {q(dl,.75):.0f}); smoke life median {med([s["end"] - s["e0"] for s in app]):.0f} s.')

# ---------------------------------------------------------------- cross-tab with round 5 snapshot version
P('\n## Timeline against the round 5 snapshot version, same smokes (grace 60 s both)\n')
J['crosstab'] = {}
for who, old, new in (('enemy', 'enemy_took', 'enemy_60'), ('we', 'we_took', 'we_60')):
    ct = C((tf(s[old]) or 'n/a', tf(s[new]) or 'n/a') for s in S)
    P(f'{"Enemy took" if who == "enemy" else "We took"} the nearest cap:')
    P(md_table(['round 5 snapshot \\ timeline', 'yes', 'no', 'n/a', 'total'], [[o] + [ct[(o, n)] for n in ('yes', 'no', 'n/a')] + [sum(ct[(o, n)] for n in ('yes', 'no', 'n/a'))] for o in ('yes', 'no', 'n/a')] +
               [['total'] + [sum(ct[(o, n)] for o in ('yes', 'no', 'n/a')) for n in ('yes', 'no', 'n/a')] + [len(S)]]))
    both = [s for s in S if s[old] is not None and s[new] is not None]
    agree = sum(1 for s in both if s[old] == s[new]); miss = ct[('no', 'yes')]; wrong = ct[('yes', 'no')]; ty = sum(1 for s in both if s[new])
    P(f'Both versions applicable: {len(both)}. Agree: {agree} ({100*agree/len(both):.1f}%). Snapshot missed a flip (said no, timeline yes): {miss}. Snapshot wrong the other way (said yes, timeline no): {wrong}.')
    P(f'Real flips in these smokes (timeline yes): {ty}; the snapshot version found {ty - miss} and missed {miss} = {100*miss/ty:.1f}% of real flips.\n')
    J['crosstab'][who] = dict(table={f'{o}|{n}': ct[(o, n)] for o in ('yes', 'no', 'n/a') for n in ('yes', 'no', 'n/a')}, both_applicable=len(both), agree=agree, agree_pct=round(100 * agree / len(both), 1),
                              snapshot_missed=miss, snapshot_wrong_other_way=wrong, timeline_yes=ty, missed_pct=round(100 * miss / ty, 1),
                              round5_yes=sum(1 for s in S if s[old]), timeline_yes_all=sum(1 for s in S if s[new]))
wr_ = [s for s in S if s['enemy_took'] and s['enemy_60'] is False]
for s in wr_[:6]:
    g = TL(s['game']); P(f'  snapshot yes, timeline no: {s["slug"]} cap {s["near_cap"]} e0 {s["e0"]:.0f} end {s["end"]:.0f} (round 5 window end {s["t1"] - s["t0"] + s["e0"] + 60:.0f}); owner changes near: {[(round(t), o) for t, o in g.owner_changes(s["near_cap"], s["e0"] - 5, s["end"] + 90)]}')
# where did the snapshot miss: flipped and flipped back, or sparse?
ms = [s for s in S if s['enemy_took'] is False and s['enemy_60']]
back = 0
for s in ms:
    g = TL(s['game']); ch = g.owner_changes(s['near_cap'], s['e0'], s['end'] + 60)
    if ch and ch[-1][1] != s['opponent']: back += 1
P(f'Of the {len(ms)} flips the snapshot missed: in {back} the cap had flipped back by the end of the window; in {len(ms) - back} it was still the enemy\'s at the end of the window, so the flip fell after the last snapshot.')
J['crosstab']['enemy']['missed_flipped_back'] = back
J['crosstab']['enemy']['by_group'] = {}
for gk, gl in (('top', 'Top 6'), ('rest', 'Rest')):
    yy = [s for s in S if s['grp'] == gk and s['enemy_took'] is not None and s['enemy_60']]; mi = sum(1 for s in yy if not s['enemy_took'])
    sn = [s['took_window'] for s in S if s['grp'] == gk and s['enemy_took'] is not None]
    P(f'  {gl}: real flips {len(yy)}, snapshot missed {mi} ({100*mi/len(yy):.0f}%); snapshots in the window per smoke: median {med(sn):.0f}, mean {mean(sn):.1f}.')
    J['crosstab']['enemy']['by_group'][gk] = dict(flips=len(yy), missed=mi, missed_pct=round(100 * mi / len(yy)), mean_snapshots=round(mean(sn), 1))
# cap_won cross-check
cw = [s for s in S if s['r']['cap_won'] and s['r']['cap_won'] == s['near_cap']]
P(f'Cross-check with the batch field cap_won (10 s grace in the batch): it names the nearest cap in {len(cw)} smokes. Round 5 snapshot we_took: yes {sum(s["we_took"] is True for s in cw)}, no {sum(s["we_took"] is False for s in cw)}, n/a {sum(s["we_took"] is None for s in cw)}. '
  f'Timeline, grace 60: yes {sum(s["we_60"] is True for s in cw)}, no {sum(s["we_60"] is False for s in cw)}, n/a {sum(s["we_60"] is None for s in cw)}; timeline, grace 10: yes {sum(raw_took(s, s["team"], 10) is True for s in cw)}, no {sum(raw_took(s, s["team"], 10) is False for s in cw)}, n/a {sum(raw_took(s, s["team"], 10) is None for s in cw)}.')
J['cap_won_crosscheck'] = dict(n=len(cw), snapshot_yes=sum(s['we_took'] is True for s in cw), timeline60_yes=sum(s['we_60'] is True for s in cw), timeline60_no=sum(s['we_60'] is False for s in cw), timeline60_na=sum(s['we_60'] is None for s in cw),
                               timeline10_yes=sum(raw_took(s, s['team'], 10) is True for s in cw))

# ---------------------------------------------------------------- summary tables
GROUPS = (('all applicable smokes', lambda s: True), ('destroyer smokes', lambda s: s['cls'] == 'destroyer'), ('smoke centre inside or within 2 km of the cap', NEAR),
          ('destroyer smokes inside or within 2 km', lambda s: NEAR(s) and s['cls'] == 'destroyer'),
          ('cap ours at activation', lambda s: s['tl_own'] == 'ours'), ('cap neutral at activation', lambda s: s['tl_own'] == 'neutral'),
          ('cap ours, smoke within 2 km', lambda s: s['tl_own'] == 'ours' and NEAR(s)),
          ('cap ours, cap_defended set for that cap', lambda s: s['tl_own'] == 'ours' and s['r']['cap_defended'] == s['near_cap']),
          ('cap ours, cap_defended not set for it', lambda s: s['tl_own'] == 'ours' and s['r']['cap_defended'] != s['near_cap']))
oldov = {x['what']: x for x in OLD['enemy_took']['overall']}
J['overall'] = {}
for key, title in (('enemy_60', 'during the smoke or within 60 s after (compare with round 5)'), ('enemy_during', 'strictly while the smoke stood')):
    rows = []; J['overall'][key] = []
    for lab, f in GROUPS:
        ss = [s for s in app if f(s)]
        r, rec = grp_rows(ss, lambda s: s[key], lab)
        o = oldov.get(lab)
        if key == 'enemy_60':
            rec['round5'] = o
            r.append(f'{o["pct"]}% (n {o["n"]}); gap {o["gap"]:+.1f} ({o["gap_ci"][0]:+.1f} to {o["gap_ci"][1]:+.1f}){" *" if o["gap_clear"] else ""}' if o else '-')
        rows.append(r); J['overall'][key].append(rec)
    P(f'\nEnemy took the nearest cap, {title}. Cap already the enemy\'s at activation is excluded. * = interval excludes zero.')
    P(md_table(['group', 'n', 'enemy took it', 'Top 6', 'Rest', 'Top 6 - Rest'] + (['round 5 snapshot: share (n); gap'] if key == 'enemy_60' else []), rows))
oldmc = {(x['map'], x['cap']): x for x in OLD['enemy_took']['by_map_cap']}
rows = []; J['by_map_cap'] = []
for (m, c), ss in sorted(by(app, lambda s: (s['map'], s['near_ncap'])).items()):
    if len(ss) < 8: rows.append([m, c, len(ss), 'too few', '', '', '', '', '']); J['by_map_cap'].append(dict(map=m, cap=c, n=len(ss), too_few=True)); continue
    r, rec = grp_rows(ss, lambda s: s['enemy_60'], f'{m} {c}')
    tn, rn = rec['top6_n'], rec['rest_n']; o = oldmc.get((m, c))
    rec.update(map=m, cap=c, during_pct=round(share(lambda s: s['enemy_during'])(ss), 1), round5_pct=o['pct'] if o else None, round5_gap=o['gap'] if o else None, round5_gap_clear=o['gap_clear'] if o else None,
               top6_small=tn < 15, rest_small=rn < 15)
    rows.append([m, c, f'{len(ss)}{small(len(ss))}', r[2], r[3] if tn >= 8 else f'too few (n {tn})', r[4] if rn >= 8 else f'too few (n {rn})', r[5] if tn >= 8 and rn >= 8 else '-',
                 f'{rec["during_pct"]:.1f}%', f'{o["pct"]}%' if o else '-'])
    J['by_map_cap'].append(rec)
P('\nBy map and cap (cap letter in the team frame), grace 60 s:'); P(md_table(['map', 'cap', 'n', 'enemy took it (60 s)', 'Top 6', 'Rest', 'Top 6 - Rest', 'strictly during', 'round 5 snapshot'], rows))
oldwe = {x['what']: x for x in OLD['we_took']}
rows = []; J['we_took'] = []
for lab, f in (('all smokes where the nearest cap was not ours', lambda s: True), ('destroyer smokes', lambda s: s['cls'] == 'destroyer'), ('within 2 km', NEAR)):
    ss = [s for s in wapp if f(s)]
    r, rec = grp_rows(ss, lambda s: s['we_60'], lab); o = oldwe.get(lab); rec['round5'] = o
    rec['during_pct'] = round(share(lambda s: s['we_during'])(ss), 1)
    rows.append(r + [f'{rec["during_pct"]:.1f}%', f'{o["pct"]}% (n {o["n"]})' if o else '-']); J['we_took'].append(rec)
P('\nFor reference, "we took the nearest cap" (cap not ours at activation), grace 60 s:'); P(md_table(['group', 'n', 'we took it', 'Top 6', 'Rest', 'Top 6 - Rest', 'strictly during', 'round 5 snapshot'], rows))

# ---------------------------------------------------------------- cap_defended follow-up
P('\n## cap_defended follow-up: was the defended cap still ours afterwards?\n')
D = [s for s in S if s['cap_def']]
for s in D:
    g = TL(s['game']); dc = s['r']['cap_defended']; s['def_cap'] = dc
    ev = g.caps[dc]; td = None
    for i, (t, o, inv) in enumerate(ev):
        e = ev[i + 1][0] if i + 1 < len(ev) else 1e9
        if o == s['team'] and inv == s['opponent'] and e > s['e0'] and t <= s['end'] + 2:
            td = max(t, s['e0']); break
    s['def_found'] = td is not None; s['def_t'] = td if td is not None else s['e0']
    s['def_own_act'] = g.owner_at(dc, s['e0']) == s['team']
    for gr in (0, 60, 120):
        s[f'def_lost_{gr}'] = any(o == s['opponent'] for _, o in g.owner_changes(dc, s['def_t'], s['end'] + gr))
    # the round 5 style test: the enemy owned it at any moment after activation up to end + 60
    s['def_lost_r5style'] = any(o == s['opponent'] for _, o in g.owner_changes(dc, s['e0'], s['end'] + 60))
    fin = g.owner_at(dc, s['end'] + 60); s['def_last'] = 'ours' if fin == s['team'] else 'theirs' if fin == s['opponent'] else 'neutral'
    s['def_inv_s'] = sum(max(0, min(ev[i + 1][0] if i + 1 < len(ev) else s['end'], s['end']) - max(t, s['e0'])) for i, (t, o, inv) in enumerate(ev) if o == s['team'] and inv == s['opponent'])
P(f'Smokes with cap_defended: {len(D)}. The timeline shows the "ours and invaded by the enemy" moment inside the smoke\'s life for {sum(s["def_found"] for s in D)} of them '
  f'(the rest: the batch saw it at a 2 s sample the change log places just outside the smoke\'s exact times; activation is used as the start for those).')
P(f'Defended cap already ours at activation: {sum(s["def_own_act"] for s in D)} of {len(D)}. Time the enemy stood in the defended cap while the smoke stood: median {med([s["def_inv_s"] for s in D]):.0f} s (quartiles {q([s["def_inv_s"] for s in D],.25):.0f} to {q([s["def_inv_s"] for s in D],.75):.0f}).')
oldk = {x['what']: x for x in OLD['cap_defended']['kept']}
rows = []; J['cap_defended'] = dict(n=len(D), found=sum(s['def_found'] for s in D), own_at_activation=sum(s['def_own_act'] for s in D), kept=[], kept_strict=[])
for lab, f in (('all smokes with cap_defended', lambda s: True), ('destroyer smokes', lambda s: s['cls'] == 'destroyer'), ('defended cap = nearest cap', lambda s: s['def_cap'] == s['near_cap']),
               ('defended cap not the nearest', lambda s: s['def_cap'] != s['near_cap'])):
    ss = [s for s in D if f(s)]
    r, rec = grp_rows(ss, lambda s: not s['def_lost_60'], lab); o = oldk.get(lab); rec['round5'] = o
    r2, rec2 = grp_rows(ss, lambda s: not s['def_lost_0'], lab)
    rows.append(r + [r2[2], f'{o["pct"]}% (n {o["n"]}); gap {o["gap"]:+.1f}' if o else '-']); J['cap_defended']['kept'].append(rec); J['cap_defended']['kept_strict'].append(rec2)
P('\nKept = the enemy did not take the defended cap between the first invaded moment and 60 s after the smoke cleared.')
P(md_table(['group', 'n', 'kept through 60 s after', 'Top 6', 'Rest', 'Top 6 - Rest', 'kept while the smoke stood', 'round 5 snapshot (60 s)'], rows))
J['cap_defended']['grace'] = {}
for gr in (0, 60, 120):
    k = sum(1 for s in D if not s[f'def_lost_{gr}']); J['cap_defended']['grace'][gr] = dict(kept=k, pct=round(100 * k / len(D), 1))
    P(f'  grace {gr} s: kept {k} of {len(D)} ({100*k/len(D):.1f}%)')
k5 = sum(1 for s in D if not s['def_lost_r5style'])
P(f'  round 5 style test on the timeline (enemy owned it at any moment from activation to 60 s after): kept {k5} of {len(D)} ({100*k5/len(D):.1f}%).')
P(f'Owner of the defended cap 60 s after the smoke cleared: {dict(C(s["def_last"] for s in D))}.')
J['cap_defended'].update(kept_r5style=k5, last_owner=dict(C(s['def_last'] for s in D)), round5_grace={'0': '374 of 486 (77.0%)', '60': '294 of 486 (60.5%)', '120': '252 of 486 (51.9%)'})
base = [s for s in app if s['tl_own'] == 'ours']
bk = sum(1 for s in base if not s['enemy_60'])
P(f'For comparison, any smoke whose nearest cap was ours at activation: the enemy did not take it (through 60 s after) in {100*bk/len(base):.1f}% (n {len(base)}); round 5 snapshot: 86.3% (n 694).')
J['cap_defended']['baseline_ours_kept'] = dict(n=len(base), pct=round(100 * bk / len(base), 1), round5_pct=86.3, round5_n=694)

# ---------------------------------------------------------------- invaders
P('\n## New: enemy inside the cap while the smoke stood (smokes within 2 km of a cap we own)\n')
OW = [s for s in S if s['tl_own'] == 'ours']
for s in OW:
    s['inv_s'] = TL(s['game']).invaded(s['near_cap'], s['opponent'], s['e0'], s['end']); s['inv'] = s['inv_s'] > 0
J['invaded'] = dict(groups=[], kept=[])
rows = []
for lab, ss in (('within 2 km of a cap we own', [s for s in OW if NEAR(s)]), ('destroyer smokes within 2 km of a cap we own', [s for s in OW if NEAR(s) and s['cls'] == 'destroyer']), ('any smoke whose nearest cap is ours (reference)', OW)):
    r, rec = grp_rows(ss, lambda s: s['inv'], lab); rows.append(r); J['invaded']['groups'].append(rec)
P(md_table(['smokes', 'n', 'enemy was invading the cap while the smoke stood', 'Top 6', 'Rest', 'Top 6 - Rest'], rows))
N2 = [s for s in OW if NEAR(s)]; INV = [s for s in N2 if s['inv']]; NOI = [s for s in N2 if not s['inv']]
iv = [s['inv_s'] for s in INV]
P(f'Seconds the enemy stood in the cap during those smokes: median {med(iv):.0f} s (quartiles {q(iv,.25):.0f} to {q(iv,.75):.0f}).')
J['invaded']['median_invaded_s'] = round(med(iv))
rows = []
for lab, ss in (('invaded, within 2 km', INV), ('invaded, destroyer smokes within 2 km', [s for s in INV if s['cls'] == 'destroyer']), ('not invaded, within 2 km', NOI)):
    r, rec = grp_rows(ss, lambda s: not s['enemy_during'], lab); r2, rec2 = grp_rows(ss, lambda s: not s['enemy_60'], lab)
    rec['kept_60'] = rec2; rows.append(r + [r2[2], r2[5]]); J['invaded']['kept'].append(rec)
P('\nWas the cap then kept?'); P(md_table(['smokes', 'n', 'kept while the smoke stood', 'Top 6', 'Rest', 'Top 6 - Rest', 'kept through 60 s after', 'Top 6 - Rest (60 s)'], rows))

# ---------------------------------------------------------------- csv
with open(os.path.join(HERE_, 'enemy-took.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['match_id', 'game_no', 'smoke_id', 'team', 'group', 'smoker_class', 'map', 'nearest_cap', 'nearest_cap_team_frame', 'edge_distance_m', 'activation_elapsed_s', 'end_elapsed_s', 'owner_at_activation',
                'enemy_took_during', 'enemy_took_within_60s', 'we_took_during', 'we_took_within_60s', 'enemy_took_elapsed_s', 'we_took_elapsed_s',
                'round5_owner_at_activation', 'round5_enemy_took', 'round5_we_took', 'round5_snapshots_in_window', 'cap_defended', 'cap_won'])
    for s in S:
        w.writerow([s['r']['match_id'], s['r']['game_no'], s['id'], s['team'], 'Top 6' if s['grp'] == 'top' else 'Rest', s['cls'], s['map'], s['near_cap'], s['near_ncap'], round(s['near_cap_edge_m']), f'{s["e0"]:.1f}', f'{s["end"]:.1f}', s['tl_own'],
                    tf(s['enemy_during']), tf(s['enemy_60']), tf(s['we_during']), tf(s['we_60']), '' if s['enemy_t'] is None or s['enemy_60'] is None else f'{s["enemy_t"]:.1f}', '' if s['we_t'] is None or s['we_60'] is None else f'{s["we_t"]:.1f}',
                    s['near_own'], tf(s['enemy_took']), tf(s['we_took']), s['took_window'], s['r']['cap_defended'], s['r']['cap_won']])
P(f'\nWrote enemy-took.csv ({len(S)} rows). "within_60s" = during the smoke or in the 60 s after it cleared.')

# ---------------------------------------------------------------- ribbons
P('\n## Ribbons per smoke\n')
REC = {}   # (game key, team) -> recorder entity id
for r in runs():
    p = os.path.join(GAMES_DIR, r['dir'], 'damage_spike.json')
    e = json.load(open(p, encoding='utf-8')).get('self_entity') if os.path.exists(p) else None
    if e is not None:
        t = G[r['key']]['roster'].get(e, {}).get('team')
        if t: REC[(r['key'], t)] = e
KINDS = ('Defended', 'Captured', 'AssistedInCapture')
allr = [x for k in G for x in TL(k).ribbons]
P(f'Recording players found: {len(REC)} (one per run; 341 ships of 3,078). Ribbon rows in the batch: {len(allr)}; by kind (rows / sum of the count column): ' +
  ', '.join(f'{k} {sum(x["ribbon"] == k for x in allr)} / {sum(x["count"] for x in allr if x["ribbon"] == k)}' for k in KINDS) + '.')
notrec = sum(1 for k in G for x in TL(k).ribbons if REC.get((k, x['team'])) != x['entity_id'])
P(f'Ribbon rows whose ship is not the run\'s recording player: {notrec}.')
# ribbon events: a row is one rise of the running total
for s in S:
    g = TL(s['game']); rec = REC.get((s['game'], s['team']))
    cov = {x['eid']: x['how'] for x in s['shelter']}
    s['rec_how'] = cov.get(rec) if rec is not None else None
    s['rec_in'] = s['rec_how'] in ('smoker', 'inside')
    rb = [x for x in g.ribbons if x['team'] == s['team'] and s['e0'] <= x['elapsed_s'] <= s['end']]
    s['rib'] = [x for x in rb if x['entity_id'] in cov] if s['rec_how'] else []
    loose = []
    for x in rb:
        p = g.pos(x['entity_id'], x['elapsed_s'])
        if p is not None and smoke_dist_m(s, p) <= 2000: loose.append(x)
    s['rib_loose'] = loose
    tr = g.tracks.get(rec) if rec is not None else None
    # recorder within 2 km of the smoke at any sample while it stood (denominator for the loose count)
    s['rec_near'] = False
    if tr:
        i = bisect.bisect_left(tr.t, s['e0']);
        while i < len(tr.t) and tr.t[i] <= s['end']:
            if tr.alive[i] and tr.x[i] is not None and smoke_dist_m(s, (tr.x[i], tr.z[i])) <= 2000: s['rec_near'] = True; break
            i += 1
CV = [s for s in S if s['rec_how']]; IN = [s for s in S if s['rec_in']]; NR = [s for s in S if s['rec_near']]
P(f'Smokes that covered the recording player of the smoking team (smoker, inside, behind or line of fire): {len(CV)} of {len(S)} ({100*len(CV)/len(S):.1f}%): {dict(C(s["rec_how"] for s in CV))}. '
  f'Recording player was the smoker or inside: {len(IN)} ({100*len(IN)/len(S):.1f}%). Recording player within 2 km of the smoke at some moment while it stood (loose): {len(NR)} ({100*len(NR)/len(S):.1f}%).')
def ribrow(lab, ss, field):
    ev = {k: sum(1 for s in ss for x in s[field] if x['ribbon'] == k) for k in KINDS}
    ds = {k: sum(1 for s in ss if any(x['ribbon'] == k for x in s[field])) for k in KINDS}
    anyr = sum(1 for s in ss if s[field])
    rec = dict(what=lab, smokes=len(ss), smokes_with_any=anyr, events=ev, distinct_smokes=ds, events_per_100={k: round(100 * v / len(ss), 1) for k, v in ev.items()} if ss else None)
    return [lab, len(ss), f'{anyr} ({100*anyr/len(ss):.1f}%)'] + [f'{ev[k]} in {ds[k]} smokes ({100*ev[k]/len(ss):.1f} per 100)' for k in KINDS], rec
J['ribbons'] = dict(recorders=len(REC), rows=len(allr), by_kind={k: sum(x['ribbon'] == k for x in allr) for k in KINDS}, covered=len(CV), covered_how=dict(C(s['rec_how'] for s in CV)), inside_or_smoker=len(IN), near_2km=len(NR), strict=[], loose=[])
rows = []
for lab, ss in (('recording player covered by the smoke', CV), ('  Top 6', [s for s in CV if s['grp'] == 'top']), ('  Rest', [s for s in CV if s['grp'] == 'rest']), ('recording player the smoker or inside', IN),
                ('  destroyer smokes, recording player covered', [s for s in CV if s['cls'] == 'destroyer'])):
    r, rec = ribrow(lab, ss, 'rib'); rows.append(r); J['ribbons']['strict'].append(rec)
P('\nStrict: ribbon by a ship the smoke covered, during the smoke. Events and distinct smokes (a Defended ribbon repeats while defending).')
P(md_table(['smokes', 'n', 'with any cap ribbon'] + list(KINDS), rows))
rows = []
for lab, ss in (('recording player within 2 km while the smoke stood', NR), ('  Top 6', [s for s in NR if s['grp'] == 'top']), ('  Rest', [s for s in NR if s['grp'] == 'rest'])):
    r, rec = ribrow(lab, ss, 'rib_loose'); rows.append(r); J['ribbons']['loose'].append(rec)
P('\nLoose: ribbon by a ship of the smoking team during the smoke while that ship was within 2 km of the smoke.')
P(md_table(['smokes', 'n', 'with any cap ribbon'] + list(KINDS), rows))
# Top 6 vs Rest with intervals: share of smokes with any ribbon, and with a Defended ribbon
rows = []; J['ribbons']['top_vs_rest'] = []
for lab, ss, key in (('strict: any cap ribbon', CV, lambda s: bool(s['rib'])), ('strict: a Defended ribbon', CV, lambda s: any(x['ribbon'] == 'Defended' for x in s['rib'])),
                     ('strict: a Captured or Assisted ribbon', CV, lambda s: any(x['ribbon'] != 'Defended' for x in s['rib'])),
                     ('loose: any cap ribbon', NR, lambda s: bool(s['rib_loose'])), ('loose: a Defended ribbon', NR, lambda s: any(x['ribbon'] == 'Defended' for x in s['rib_loose']))):
    r, rec = grp_rows(ss, key, lab); rows.append(r); J['ribbons']['top_vs_rest'].append(rec)
P('\nTop 6 vs Rest (share of smokes, intervals by resampling clans):'); P(md_table(['measure', 'n', 'share of smokes', 'Top 6', 'Rest', 'Top 6 - Rest'], rows))
# Defended ribbon vs cap kept
P('\nDo smokes with a Defended ribbon keep the cap more often? (nearest cap ours at activation; the ribbon does not say which cap it was for)')
rows = []; J['ribbons']['defended_vs_kept'] = []
for lab, ss, field in (('strict, recording player covered', [s for s in CV if s['tl_own'] == 'ours'], 'rib'), ('strict, and smoke within 2 km of the cap', [s for s in CV if s['tl_own'] == 'ours' and NEAR(s)], 'rib'),
                       ('loose, recording player within 2 km of the smoke', [s for s in NR if s['tl_own'] == 'ours'], 'rib_loose'), ('loose, and smoke within 2 km of the cap', [s for s in NR if s['tl_own'] == 'ours' and NEAR(s)], 'rib_loose'),
                       ('loose, smoke within 2 km, enemy was invading the cap', [s for s in NR if s['tl_own'] == 'ours' and NEAR(s) and s['inv']], 'rib_loose')):
    a = [s for s in ss if any(x['ribbon'] == 'Defended' for x in s[field])]; b = [s for s in ss if not any(x['ribbon'] == 'Defended' for x in s[field])]
    def kp(xs, k): return f'{sum(1 for s in xs if not s[k])} of {len(xs)} ({100*sum(1 for s in xs if not s[k])/len(xs):.0f}%){small(len(xs))}' if len(xs) >= 8 else f'too few (n {len(xs)})'
    def st(xs, field=field):
        x = [s for s in xs if any(r['ribbon'] == 'Defended' for r in s[field])]; y = [s for s in xs if not any(r['ribbon'] == 'Defended' for r in s[field])]
        return 100 * (mean(not s['enemy_60'] for s in x) - mean(not s['enemy_60'] for s in y)) if x and y else None
    cd = boot_stat(ss, st) if len(a) >= 8 and len(b) >= 8 else (None, None)
    gap = st(ss) if len(a) >= 8 and len(b) >= 8 else None
    rows.append([lab, kp(a, 'enemy_during'), kp(b, 'enemy_during'), kp(a, 'enemy_60'), kp(b, 'enemy_60'), f'{gap:+.0f} ({ci(cd, "{:+.0f}")})' if gap is not None else '-'])
    J['ribbons']['defended_vs_kept'].append(dict(what=lab, with_ribbon_n=len(a), with_ribbon_kept_during=sum(1 for s in a if not s['enemy_during']), with_ribbon_kept_60=sum(1 for s in a if not s['enemy_60']),
                                                 without_n=len(b), without_kept_during=sum(1 for s in b if not s['enemy_during']), without_kept_60=sum(1 for s in b if not s['enemy_60']),
                                                 gap_60=round(gap, 1) if gap is not None else None, gap_ci=[round(cd[0], 1), round(cd[1], 1)] if cd[0] is not None else None))
P(md_table(['smokes (nearest cap ours)', 'Defended ribbon: kept while the smoke stood', 'no Defended ribbon: kept', 'Defended ribbon: kept through 60 s', 'no Defended ribbon: kept through 60 s', 'gap, 60 s (interval)'], rows))
# ribbon vs timeline consistency: every Captured ribbon should sit on an owner change to that team
ok = tot = 0; dok = dtot = 0; dany = 0
for k in G:
    g = TL(k)
    for x in g.ribbons:
        if x['ribbon'] == 'Captured':
            tot += 1; ok += any(o == x['team'] and abs(t - x['elapsed_s']) <= 3 for c in g.caps for t, o, _ in g.caps[c])
        if x['ribbon'] == 'Defended':
            dtot += 1
            hit = False; hit2 = False
            for c, ev in g.caps.items():
                for i, (t, o, inv) in enumerate(ev):
                    e = ev[i + 1][0] if i + 1 < len(ev) else 1e9
                    if o == x['team'] and inv not in (None, x['team']) and t - 3 <= x['elapsed_s'] <= e + 3: hit = True
                    if inv not in (None, x['team']) and t - 3 <= x['elapsed_s'] <= e + 3: hit2 = True
            dok += hit; dany += hit2
P(f'\nRibbons against the cap timeline: {ok} of {tot} Captured ribbons fall within 3 s of a cap changing to that team; {dok} of {dtot} Defended ribbons fall while the enemy was invading a cap that team owned, {dany} while the enemy was invading any cap (the ribbon is also given for stopping the capture of a neutral cap).')
J['ribbons']['timeline_check'] = dict(captured=tot, captured_on_flip=ok, defended=dtot, defended_while_invaded=dok, defended_while_any_cap_invaded=dany)
# strict Captured ribbons vs we_took
cp = [s for s in CV if any(x['ribbon'] == 'Captured' for x in s['rib'])]
P(f'Smokes with a strict Captured ribbon: {len(cp)}; the timeline says we took the nearest cap during the smoke in {sum(1 for s in cp if s["we_during"])}, the nearest cap was already ours in {sum(1 for s in cp if s["we_during"] is None)} (the ribbon was for another cap).')
J['ribbons']['captured_vs_we_took'] = dict(n=len(cp), we_took_during=sum(1 for s in cp if s['we_during']), already_ours=sum(1 for s in cp if s['we_during'] is None))

# ---------------------------------------------------------------- figure
rowsf = [(lab, o) for lab, o in ((x['what'], x) for x in J['overall']['enemy_60'])][:6]
strict = {x['what']: x for x in J['overall']['enemy_during']}
fig = Fig(1000, 110 + 62 * len(rowsf) + 30, 'N1 working figure: "enemy took the nearest cap", snapshot version vs cap timeline',
          'Share of applicable smokes. Round 5 snapshots missed flips; the timeline sees every owner change.')
fig.legend(330, 74, [('round 5 snapshots, during + 60 s', MUTED), ('timeline, during + 60 s', VIOLET), ('timeline, strictly during the smoke', AQUA)])
y = 96; x0 = 330; wpx = 560; vmax = 35
for lab, rec in rowsf:
    fig.add(T(x0 - 10, y + 24, lab, size=12, fill=INK, anchor='end')); fig.add(T(x0 - 10, y + 39, f'n {rec["n"]:,}', size=10, anchor='end'))
    for i, (v, col) in enumerate(((rec['round5']['pct'], MUTED), (rec['pct'], VIOLET), (strict[lab]['pct'], AQUA))):
        bw = wpx * v / vmax
        fig.add(f'<rect x="{x0}" y="{y + 4 + i * 16}" width="{bw:.1f}" height="13" rx="2" fill="{col}"/>' + T(x0 + bw + 5, y + 15 + i * 16, f'{v:.1f}%', size=10.5, fill=INK, anchor='start'))
    y += 62
fig.save(os.path.join(R5, 'figures', 'n1-enemy-took-snapshot-vs-timeline'))
open(os.path.join(HERE_, 'out-c1.md'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
json.dump(J, open(os.path.join(HERE_, 'c1.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
print('done')
