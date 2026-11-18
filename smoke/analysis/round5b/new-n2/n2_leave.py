# Round 5b, worker n2: A2 "leaving the smoke", from ship tracks. Frame: destroyer smokes, as in round 5 A2.
# Run: python -I -X utf8 n2_leave.py      Writes out-leave.json, out-leave.md and figure n2-leaving-the-smoke.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n2lib import *
random.seed(29)
PR = build_pairs()
L = []
def P(*a):
    t = ' '.join(str(x) for x in a); L.append(t); print(t)
J = {}
FOLLOW = 30.0
CLASSES = ['inside a standing smoke', 'within 30 s of leaving a standing smoke', 'more than 30 s after leaving', 'after the smoke dispersed around it', 'never inside the outline']
SHORT = {'inside a standing smoke': 'inside', 'within 30 s of leaving a standing smoke': 'left, 30 s or less', 'more than 30 s after leaving': 'left, over 30 s', 'after the smoke dispersed around it': 'smoke dispersed', 'never inside the outline': 'never inside'}

def walk(s, tr, t_end):
    """Samples of ship tr from activation to t_end while alive: list of (i, t, standing, outline)."""
    ends = puff_ends(s); out = []
    for i in samples(tr, s['e0'], t_end):
        if not tr.alive[i] or tr.x[i] is None: continue
        p = (tr.x[i], tr.z[i]); out.append((i, tr.t[i], in_standing(s, p, tr.t[i], ends), in_outline(s, p)))
    return out
def classify(s, tr, td):
    """Where a ship that died at td was relative to smoke s. Returns (class, seconds from leaving / dispersal to death or None, metres from death position to the smoke edge)."""
    w = walk(s, tr, td)
    dp = tr.last_alive_pos(); dist = smoke_dist_m(s, dp) - s['radius_m'] if dp else None
    if not w: return CLASSES[4], None, dist
    if w[-1][2]: return CLASSES[0], 0.0, dist
    ks = [n for n, x in enumerate(w) if x[2]]
    if not ks: return CLASSES[4], None, dist
    k = ks[-1]; nxt = w[k + 1]; gap = td - nxt[1]
    if nxt[3]: return CLASSES[3], gap, dist
    return (CLASSES[1] if gap <= FOLLOW else CLASSES[2]), gap, dist

who_of = lambda cls, is_smoker: 'smoking destroyer' if is_smoker and cls == 'destroyer' else 'sheltering cruiser' if cls == 'cruiser' and not is_smoker else 'other ship'
WHO = ['smoking destroyer', 'sheltering cruiser', 'other ship']

# ---- A. the batch death list (round 5's 124 deaths in destroyer smokes)
BD = []
for s in DD:
    g = TL(s['game'])
    for d in s['dead']:
        tr = g.tracks.get(d['eid']); td = tr.death_t() if tr else None
        if td is None: continue
        c, gap, dist = classify(s, tr, td)
        BD.append(dict(s=s, d=d, cls=c, gap=gap, dist=dist, who=who_of(d['cls'], d['is_smoker']), grp=s['grp'], td=td, det=tr.det[tr.idx(td - STEP)] if tr.idx(td - STEP) is not None else None))
n_batch = sum(len(s['dead']) for s in DD)
P(f'## A. Deaths in the batch list (destroyer smokes): {n_batch} records, {len(BD)} with a track death time')
def class_table(rows_, key='cls'):
    out = []; js = {}
    for w in WHO + ['all']:
        v = [x for x in rows_ if w == 'all' or x['who'] == w]
        if not v: continue
        c = C(x[key] for x in v); ct = C(x[key] for x in v if x['grp'] == 'top'); cr_ = C(x[key] for x in v if x['grp'] == 'rest')
        js[w] = dict(n=len(v), n_top6=sum(ct.values()), n_rest=sum(cr_.values()), classes={k: dict(n=c[k], top6=ct[k], rest=cr_[k], pct=r1(100 * c[k] / len(v))) for k in CLASSES})
        out.append([w, f'{len(v)} ({sum(ct.values())} / {sum(cr_.values())})'] + [f'{c[k]} ({ct[k]} / {cr_[k]})' for k in CLASSES])
    return out, js
rows, J['batch_deaths'] = class_table(BD)
P(md_table(['who died', 'n (Top 6 / Rest)'] + [SHORT[k] for k in CLASSES], rows))
P('Each cell: count (Top 6 / Rest). "Left" = the ship moved outside the radius of every puff while the puffs it had been in still stood. "Smoke dispersed" = the puffs around the ship ended and the ship was still inside the old outline at the next sample.')
# round 5 proxies against the track
ac = [x for x in BD if x['d']['after_cleared']]; bh = [x for x in BD if x['d']['where'] == 'behind']
J['proxies'] = dict(after_cleared=dict(n=len(ac), classes=dict(C(SHORT[x['cls']] for x in ac))), behind=dict(n=len(bh), classes=dict(C(SHORT[x['cls']] for x in bh))),
                    inside_list=dict(n=sum(x['d']['where'] == 'inside' for x in BD), classes=dict(C(SHORT[x['cls']] for x in BD if x['d']['where'] == 'inside'))))
P(f'\nRound 5 proxy 1, "died just after the smoke cleared" ({len(ac)}): by track: {dict(C(SHORT[x["cls"]] for x in ac).most_common())}.')
P(f'Round 5 proxy 2, "died behind rather than inside" ({len(bh)}): by track: {dict(C(SHORT[x["cls"]] for x in bh).most_common())}.')
P(f'Batch "inside" deaths ({J["proxies"]["inside_list"]["n"]}): by track: {dict(C(SHORT[x["cls"]] for x in BD if x["d"]["where"] == "inside").most_common())}.')
left = [x for x in BD if x['cls'] in CLASSES[1:3]]
J['batch_left'] = dict(n=len(left), within_30=sum(x['cls'] == CLASSES[1] for x in left), median_gap_s=r1(med(x['gap'] for x in left)), median_dist_m=r1(med(x['dist'] for x in left), 0), detected_at_death=sum(bool(x['det']) for x in left))
P(f'Deaths after leaving a standing smoke: {len(left)} of {len(BD)} ({100*len(left)/len(BD):.0f}%); {J["batch_left"]["within_30"]} within 30 s; median {J["batch_left"]["median_gap_s"]} s after leaving and {J["batch_left"]["median_dist_m"]:,.0f} m past the smoke edge.')

# ---- B. every ship at risk in a destroyer smoke whose track shows a death in the window (the batch list misses some)
RISK = [p for p in PR if p['s']['cls'] == 'destroyer' and p['how'] in ('smoker', 'inside', 'behind') and p['own']]
for p in RISK: p['who'] = who_of(p['cls'], p['how'] == 'smoker'); p['grp'] = p['s']['grp']
WD = []
for p in RISK:
    if not p['died_win']: continue
    c, gap, dist = classify(p['s'], p['tr'], p['td'])
    WD.append(dict(s=p['s'], p=p, cls=c, gap=gap, dist=dist, who=p['who'], grp=p['grp'], in_batch=p['died']))
P(f'\n## B. All track deaths of ships at risk in destroyer smokes (activation to 20 s after dispersal): {len(WD)} ship-smoke pairs, {len({(x["s"]["game"], x["p"]["eid"]) for x in WD})} distinct ships; {sum(x["in_batch"] for x in WD)} are in the batch list')
rows, J['track_deaths'] = class_table(WD)
P(md_table(['who died', 'n (Top 6 / Rest)'] + [SHORT[k] for k in CLASSES], rows))
rows, J['track_only_deaths'] = class_table([x for x in WD if not x['in_batch']])
P('\nOf which not in the batch list:'); P(md_table(['who died', 'n (Top 6 / Rest)'] + [SHORT[k] for k in CLASSES], rows))

# ---- C. rates: ships that left a standing smoke against ships that stayed until it dispersed
EV = []; inside_sec = collections.defaultdict(float); inside_loss = collections.defaultdict(float); inside_dead = C(); inside_det = collections.defaultdict(float)
def bucket(p, state): return (p['who'], 'behind 50+' if state == 'behind 50+' else 'not behind', p['grp'])
for p in RISK:
    if p['who'] == 'other ship' or not p['ok']: continue
    s, tr = p['s'], p['tr']; td = p['td']
    w = walk(s, tr, min(s['E1'] + STEP, td if td is not None else 1e9))
    ks = [n for n, x in enumerate(w) if x[2]]
    # exposure inside a standing smoke (for the hazard comparison)
    for n in ks:
        i, t = w[n][0], w[n][1]; b = bucket(p, state_at(s, t)); inside_sec[b] += STEP; inside_det[b] += STEP * bool(tr.det[i])
        if i + 1 < len(tr.t):
            v0 = tr.hp[i]; v1 = 0.0 if not tr.alive[i + 1] else tr.hp[i + 1]
            if v0 is not None and v1 is not None and v0 > v1: inside_loss[b] += (v0 - v1) / p['maxhp']
    if not ks: continue
    k = ks[-1]; i_in, t_in = w[k][0], w[k][1]
    if k + 1 >= len(w):
        # no later live sample inside the window: died inside, or the game / window ended while inside
        if td is not None and td <= t_in + 2 * STEP: inside_dead[bucket(p, state_at(s, t_in))] += 1; p['fate'] = 'died inside'
        else:
            # still inside at the end of the window: treat the end as the dispersal moment
            j = i_in + 1
            if j >= len(tr.t): continue
            EV.append(dict(p=p, kind='stayed', i=j, t=tr.t[j], i_in=i_in))
        continue
    nxt = w[k + 1]
    EV.append(dict(p=p, kind='stayed' if nxt[3] else 'left', i=nxt[0], t=nxt[1], i_in=i_in))
ends_cache = {}
for e in EV:
    p = e['p']; s, tr = p['s'], p['tr']; t0 = e['t']; td = p['td']
    e['who'], e['grp'], e['team'] = p['who'], p['grp'], s['team']
    e['state'] = state_at(s, t0); e['behind'] = e['state'] == 'behind 50+'
    e['followed'] = (tr.t[-1] - t0 >= FOLLOW - STEP) or (td is not None and td <= t0 + FOLLOW + STEP)
    e['died'] = td is not None and td <= t0 + FOLLOW + STEP
    h_in = tr.hp[e['i_in']]; lo = h_in; gross = 0.0; prev = h_in
    for i in samples(tr, t0, t0 + FOLLOW):
        v = 0.0 if not tr.alive[i] else tr.hp[i]
        if v is None: continue
        lo = min(lo, v)
        if prev - v > 0: gross += prev - v
        prev = v
    e['loss'] = (h_in - lo) / p['maxhp']; e['gross'] = gross / p['maxhp']
    e['hurt'] = e['died'] or e['loss'] >= HURT_SHARE; e['hit'] = e['died'] or e['loss'] >= 0.10
    e['det_in'] = bool(tr.det[e['i_in']]); e['det_exit'] = bool(tr.det[e['i']])
    e['det_10'] = any(bool(tr.det[i]) for i in samples(tr, t0, t0 + 10))
    ends = puff_ends(s); pos = (tr.x[e['i_in']], tr.z[e['i_in']]); r = s['radius_m'] / WU
    e['remaining'] = max([en - tr.t[e['i_in']] for (x, z), en in zip(s['path'], ends) if math.hypot(pos[0] - x, pos[1] - z) <= r] or [0])
    e['time_in'] = tr.t[e['i_in']] - s['e0']
E = [e for e in EV if e['followed']]
P(f'\n## C. Leaving against staying (smoking destroyers and sheltering cruisers in destroyer smokes)')
P(f'Ships that were inside a standing smoke at some point: events {len(EV)} with a later live sample ({sum(e["kind"] == "left" for e in EV)} left while the smoke stood, {sum(e["kind"] == "stayed" for e in EV)} stayed until the puffs around them ended); '
  f'{len(EV)-len(E)} dropped because the game ended inside the 30 s that follow; died inside a standing smoke: {sum(inside_dead.values())}.')
lv = [e for e in E if e['kind'] == 'left']
J['leavers'] = dict(n=len(lv), median_smoke_left_s=r1(med(e['remaining'] for e in lv)), median_time_in_s=r1(med(e['time_in'] for e in lv)), left_with_20s_or_more=sum(e['remaining'] >= 20 for e in lv))
P(f'Leavers: median {J["leavers"]["median_smoke_left_s"]} s of smoke still to run when they left, median {J["leavers"]["median_time_in_s"]} s after activation; {J["leavers"]["left_with_20s_or_more"]} of {len(lv)} left with 20 s or more of smoke remaining.')
def rate(v, k): return 100 * sum(1 for e in v if e[k]) / len(v) if len(v) >= MIN_N else None
def cmp_row(label, v):
    a = [e for e in v if e['kind'] == 'left']; b = [e for e in v if e['kind'] == 'stayed']
    row = dict(label=label, n_left=len(a), n_stayed=len(b))
    for k in ('died', 'hurt', 'hit'):
        st = lambda ee, k=k: (None if rate([e for e in ee if e['kind'] == 'left'], k) is None or rate([e for e in ee if e['kind'] == 'stayed'], k) is None
                              else rate([e for e in ee if e['kind'] == 'left'], k) - rate([e for e in ee if e['kind'] == 'stayed'], k))
        d = st(v); c = clus_ci(v, st, key=lambda e: e['team']) if d is not None else (None, None)
        row[k] = dict(left=r1(rate(a, k)), stayed=r1(rate(b, k)), n_left=sum(1 for e in a if e[k]), n_stayed=sum(1 for e in b if e[k]), diff=r1(d), ci=[r1(c[0]), r1(c[1])], clear=bool(c[0] is not None and c[0] * c[1] > 0))
    row['det'] = dict(left_inside=r1(rate(a, 'det_in')), left_at_exit=r1(rate(a, 'det_exit')), left_10s=r1(rate(a, 'det_10')), stayed_inside=r1(rate(b, 'det_in')), stayed_at_end=r1(rate(b, 'det_exit')), stayed_10s=r1(rate(b, 'det_10')))
    row['gross'] = dict(left=r1(100 * mean(e['gross'] for e in a)) if a else None, stayed=r1(100 * mean(e['gross'] for e in b)) if b else None)
    return row
def show(rows):
    f = lambda x: fv(x['left']) + f' ({x["n_left"]})'; g = lambda x: fv(x['stayed']) + f' ({x["n_stayed"]})'
    P(md_table(['group', 'left: n', 'stayed: n', 'died in next 30 s: left', 'stayed', 'difference', 'died or lost 1/3+: left', 'stayed', 'difference', 'died or lost 10%+: left', 'stayed', 'difference'],
               [[r['label'], f'{r["n_left"]}{" (" + sm(r["n_left"]) + ")" if sm(r["n_left"]) else ""}', f'{r["n_stayed"]}{" (" + sm(r["n_stayed"]) + ")" if sm(r["n_stayed"]) else ""}',
                 f(r['died']), g(r['died']), fci(r['died']['ci']), f(r['hurt']), g(r['hurt']), fci(r['hurt']['ci']), f(r['hit']), g(r['hit']), fci(r['hit']['ci'])] for r in rows]))
J['rates'] = []
for w in WHO[:2]:
    v = [e for e in E if e['who'] == w]
    rows = [cmp_row(f'{w}, all', v), cmp_row(f'{w}, 50+ behind', [e for e in v if e['behind']]), cmp_row(f'{w}, not behind', [e for e in v if not e['behind']]),
            cmp_row(f'{w}, Top 6', [e for e in v if e['grp'] == 'top']), cmp_row(f'{w}, Rest', [e for e in v if e['grp'] == 'rest']),
            cmp_row(f'{w}, Top 6, 50+ behind', [e for e in v if e['grp'] == 'top' and e['behind']]), cmp_row(f'{w}, Rest, 50+ behind', [e for e in v if e['grp'] == 'rest' and e['behind']]),
            cmp_row(f'{w}, Top 6, not behind', [e for e in v if e['grp'] == 'top' and not e['behind']]), cmp_row(f'{w}, Rest, not behind', [e for e in v if e['grp'] == 'rest' and not e['behind']]),
            cmp_row(f'{w}, left with 20 s+ of smoke remaining (stayers unchanged)', [e for e in v if e['kind'] == 'stayed' or e['remaining'] >= 20])]
    J['rates'] += rows
    P(f'\n{w}: per 100 ships, in the 30 s after leaving a standing smoke against the 30 s after the smoke dispersed around the ship. Score state at that moment (score timeline).'); show(rows)
P('\nCounts in brackets are ships. Difference = left minus stayed, 95% interval with whole clans resampled; * = excludes zero.')
# detected when leaving
P('\nDetected by the enemy (track `det`), share of ships:')
rows = []
for r in J['rates']:
    if r['label'].endswith(', all') or r['label'].endswith('50+ behind') and 'Top' not in r['label'] and 'Rest' not in r['label'] or r['label'].endswith(', not behind') and 'Top' not in r['label'] and 'Rest' not in r['label']:
        d = r['det']; rows.append([r['label'], fv(d['left_inside'], '{:.0f}%'), fv(d['left_at_exit'], '{:.0f}%'), fv(d['left_10s'], '{:.0f}%'), fv(d['stayed_inside'], '{:.0f}%'), fv(d['stayed_at_end'], '{:.0f}%'), fv(d['stayed_10s'], '{:.0f}%')])
P(md_table(['group', 'leavers: at last sample inside', 'at first sample outside', 'at some point in the next 10 s', 'stayers: at last sample with smoke', 'at first sample without', 'at some point in the next 10 s'], rows))
# hazard: 30 s inside a standing smoke against the 30 s after
P('\nPer 30 seconds: inside a standing smoke, against the 30 s after leaving and the 30 s after it dispersed (deaths per 100 ship half-minutes; health lost = all falls added up, share of full health):')
rows = []; J['hazard'] = []
for w in WHO[:2]:
    for st in ('all', 'behind 50+', 'not behind'):
        ks = [b for b in inside_sec if b[0] == w and (st == 'all' or b[1] == st)]
        sec = sum(inside_sec[b] for b in ks); hm = sec / 30
        v = [e for e in E if e['who'] == w and (st == 'all' or (e['behind'] == (st == 'behind 50+')))]
        a = [e for e in v if e['kind'] == 'left']; b_ = [e for e in v if e['kind'] == 'stayed']
        rec = dict(who=w, state=st, inside_half_minutes=round(hm), inside_deaths=sum(inside_dead[b] for b in ks), inside_deaths_per_100=r1(100 * sum(inside_dead[b] for b in ks) / hm), inside_loss_pct=r1(100 * sum(inside_loss[b] for b in ks) / hm),
                   inside_detected_pct=r1(100 * sum(inside_det[b] for b in ks) / sec), left_n=len(a), left_deaths_per_100=r1(rate(a, 'died')), left_loss_pct=r1(100 * mean(e['gross'] for e in a)) if a else None,
                   stayed_n=len(b_), stayed_deaths_per_100=r1(rate(b_, 'died')), stayed_loss_pct=r1(100 * mean(e['gross'] for e in b_)) if b_ else None)
        J['hazard'].append(rec)
        rows.append([w, st, f'{rec["inside_half_minutes"]:,}', f'{rec["inside_deaths_per_100"]} ({rec["inside_deaths"]})', f'{rec["inside_loss_pct"]}%', f'{rec["inside_detected_pct"]}%', f'{fv(rec["left_deaths_per_100"])} (n {len(a)})', f'{rec["left_loss_pct"]}%', f'{fv(rec["stayed_deaths_per_100"])} (n {len(b_)})', f'{rec["stayed_loss_pct"]}%'])
P(md_table(['who', 'score', 'half-minutes inside', 'inside: deaths per 100 (n)', 'inside: health lost per 30 s', 'inside: share of time detected', 'after leaving: deaths per 100', 'health lost', 'after dispersal: deaths per 100', 'health lost'], rows))
# clans among leavers who died
ld = [e for e in E if e['kind'] == 'left' and e['died']]
J['leaver_deaths_clans'] = clan_dict([e['p']['s'] for e in ld]); J['leaver_deaths_clans_text'] = clan_counts([e['p']['s'] for e in ld])
P(f'\nClans, ships that died within 30 s of leaving a standing smoke ({len(ld)}): {clan_counts([e["p"]["s"] for e in ld])}')
J['events'] = dict(total=len(EV), followed=len(E), left=sum(e['kind'] == 'left' for e in E), stayed=sum(e['kind'] == 'stayed' for e in E), died_inside=sum(inside_dead.values()))
dump('out-leave.json', J)
open(os.path.join(HERE_, 'out-leave.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ---- figure
COLS = {'inside a standing smoke': '#184f95', 'within 30 s of leaving a standing smoke': '#e34948', 'more than 30 s after leaving': '#f0a9a8', 'after the smoke dispersed around it': '#eda100', 'never inside the outline': '#8a8984'}
fig = Fig(1100, 640, 'A2 (round 5b): leaving the smoke', 'Left: where ships were when they died (all track deaths of ships at risk in destroyer smokes). Right: what happened in the 30 s after leaving a standing smoke, against the 30 s after it dispersed.')
y = 100; fig.add(T(40, 84, 'Deaths by where the ship was (count)', size=13, fill=INK, anchor='start', weight='600'))
for w in WHO[:2]:
    for gl, gk in (('Top 6', 'top6'), ('Rest', 'rest')):
        d = J['track_deaths'][w]; tot = sum(d['classes'][k][gk] for k in CLASSES); x = 190
        fig.add(T(180, y + 15, f'{w}, {gl} (n {tot})', size=11, fill=INK, anchor='end'))
        for k in CLASSES:
            n = d['classes'][k][gk]; wd = n * 3.2
            if n:
                fig.add(f'<rect x="{x:.1f}" y="{y}" width="{wd:.1f}" height="22" fill="{COLS[k]}"/>')
                if wd > 14: fig.add(T(x + wd / 2, y + 15, str(n), size=10.5, fill=BG if k != CLASSES[2] else INK, weight='600'))
            x += wd
        y += 30
    y += 12
ly = y + 10
for k in CLASSES:
    fig.add(f'<rect x="60" y="{ly-10}" width="12" height="12" rx="2" fill="{COLS[k]}"/>' + T(78, ly, 'died ' + k, size=11.5, fill=INK, anchor='start')); ly += 20
fig.add(T(600, 84, 'Died or lost a third of full health in the next 30 s, per 100 ships', size=13, fill=INK, anchor='start', weight='600'))
y = 100
for r in J['rates']:
    if not (r['label'].endswith(', all') or r['label'].endswith(', 50+ behind') or r['label'].endswith(', not behind')) or 'Top 6,' in r['label'] or 'Rest,' in r['label']: continue
    fig.add(T(600, y + 12, r['label'] + (' *' if r['hurt']['clear'] else ''), size=11.5, fill=INK, anchor='start', weight='600'))
    for n, (lab, key, colr) in enumerate((('left the smoke', 'left', '#e34948'), ('stayed until it dispersed', 'stayed', '#eda100'))):
        v = r['hurt'][key]; yy = y + 20 + n * 18
        fig.add(T(760, yy + 12, f'{lab} (n {r["n_" + key]})', size=10.5, anchor='end'))
        if v is not None: fig.add(f'<rect x="768" y="{yy}" width="{v*9:.1f}" height="14" rx="2" fill="{colr}"/>' + T(774 + v * 9, yy + 11.5, f'{v:.1f}', size=10.5, fill=INK, anchor='start'))
        else: fig.add(T(774, yy + 11.5, 'too few', size=10.5, anchor='start'))
    y += 70
fig.add(T(600, y + 10, '* = the difference between leaving and staying is clear (interval excludes zero).', size=10.5, anchor='start'))
fig.save(os.path.join(FIGS, 'n2-leaving-the-smoke'))
print('done')
