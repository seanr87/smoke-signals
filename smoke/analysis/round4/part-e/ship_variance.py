# Part E: ship variance. Read-only on the batch; writes only in this folder.
# Run from the repo root: python -I -X utf8 smoke/analysis/round4/part-e/ship_variance.py
import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'round3'))); from common import *; S, G = load()
OUT = os.path.dirname(os.path.abspath(__file__))
GD = 'Gdańsk'
FOUR = ['Grozovoi', 'Shimakaze', 'Daring', GD]
CAP_REF = ['Daring', 'Z-42', GD]; LINE_REF = ['Somers', 'Gearing', 'Harugumo', 'Delny']
sh = by(S, 'ship')
R = random.Random(19)
J = {'batch': BATCH_NAME, 'ships': {}, 'emission': {}}
P = print

# ---------------------------------------------------------------- features
def lat_fwd(s):
    half = MAPS[s['map']]['space_size'] / 2
    if s['map'] in DIAGONAL: lat = abs(s['nx'] - s['nz']) / math.sqrt(2) / half
    else: lat = abs(s['nx']) / half
    return lat, forward(s['map'], s['nx'], s['nz']) / WU / half
for s in S:
    s['lat'], s['fwd'] = lat_fwd(s)
    s['stat'] = s['movement'] == 'stationary'
    s['path_missing'] = s['path_m'] is None
    if s['path_m'] is None:  # no movement record: use the length of the puff path
        s['path_m'] = sum(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(s['npath'], s['npath'][1:])) * WU
FEATS = [('log path', lambda s: math.log10((s['path_m'] or 0) + 50)), ('edge km', lambda s: max(-3, min(10, s['edge'] / 1000))),
         ('lateral', lambda s: s['lat']), ('forward', lambda s: s['fwd']), ('stationary', lambda s: 1.0 * s['stat']),
         ('stacked', lambda s: 1.0 * (s['coverage'] == 'stacked')), ('selfish', lambda s: 1.0 * (s['coverage'] == 'selfish'))]
def raw(s): return [f(s) for _, f in FEATS]
def scaler(ss):
    X = [raw(s) for s in ss]; mu = [mean(c) for c in zip(*X)]; sd = [statistics.pstdev(c) or 1 for c in zip(*X)]
    return lambda s: [(v - m) / d for v, m, d in zip(raw(s), mu, sd)]
def d2(a, b): return sum((x - y) ** 2 for x, y in zip(a, b))
def cen(X): return [mean(c) for c in zip(*X)]
def kmeans2(X, restarts=25, rng=R):
    best = None
    for _ in range(restarts):
        c = rng.sample(X, 2)
        for _ in range(50):
            lab = [0 if d2(x, c[0]) <= d2(x, c[1]) else 1 for x in X]
            if len(set(lab)) < 2: break
            nc = [cen([x for x, l in zip(X, lab) if l == k]) for k in (0, 1)]
            if nc == c: break
            c = nc
        if len(set(lab)) < 2: continue
        inert = sum(d2(x, c[l]) for x, l in zip(X, lab))
        if best is None or inert < best[0]: best = (inert, lab, c)
    return best
def silhouette(X, lab):
    out = []
    for i, x in enumerate(X):
        a = [math.sqrt(d2(x, y)) for j, y in enumerate(X) if j != i and lab[j] == lab[i]]
        b = [math.sqrt(d2(x, y)) for j, y in enumerate(X) if lab[j] != lab[i]]
        if not a or not b: out.append(0); continue
        a, b = mean(a), mean(b); out.append((b - a) / max(a, b))
    return mean(out)
def split_quality(X, rng=R):
    inert, lab, c = kmeans2(X, rng=rng)
    tot = sum(d2(x, cen(X)) for x in X)
    return silhouette(X, lab), 1 - inert / tot, lab

# ---------------------------------------------------------------- 1a. within-ship spread
P('\n## 1a. Spread within ship')
def pooled_rms(ss, min_n=5):
    """Pooled within-map spread of smoke centres (km): root mean square distance to the ship's own centre on that map."""
    sq, n, k = 0.0, 0, 0
    for m, v in by(ss, 'map').items():
        if len(v) < min_n: continue
        cx, cz = mean(s['nx'] for s in v), mean(s['nz'] for s in v)
        sq += sum((s['nx'] - cx) ** 2 + (s['nz'] - cz) ** 2 for s in v); n += len(v); k += 1
    return math.sqrt(sq / (n - k)) * WU / 1000 if n - k > 0 else None
def iqr(v): return q(v, .75) - q(v, .25)
STATS = {'pos_spread_km': pooled_rms, 'stationary_pct': lambda ss: pct(ss, lambda s: s['stat']), 'inside_pct': lambda ss: pct(ss, lambda s: s['inside']),
         'edge_med_m': lambda ss: med(s['edge'] for s in ss), 'edge_iqr_m': lambda ss: iqr([s['edge'] for s in ss]),
         'path_med_m': lambda ss: med(s['path_m'] for s in ss), 'stacked_pct': lambda ss: pct(ss, lambda s: s['coverage'] == 'stacked'),
         'screen_pct': lambda ss: pct(ss, lambda s: s['coverage'] == 'screen'), 'selfish_pct': lambda ss: pct(ss, lambda s: s['coverage'] == 'selfish')}
rows = []
for k in FOUR:
    v = sh[k]; d = {'n': len(v), 'clans': len(set(s['team'] for s in v)), 'players': len(set(s['player'] for s in v)),
                    'top_clan': C(s['team'] for s in v).most_common(1)[0]}
    for name, f in STATS.items():
        lo, hi = boot_stat(v, f); d[name] = f(v); d[name + '_ci'] = [lo, hi]
    J['ships'][k] = d
    rows.append([k, d['n'], d['clans']] + [f"{n0(d[x], '{:,.1f}' if 'km' in x else '{:,.0f}')} ({n0(d[x+'_ci'][0], '{:,.1f}' if 'km' in x else '{:,.0f}')} to {n0(d[x+'_ci'][1], '{:,.1f}' if 'km' in x else '{:,.0f}')})" for x in STATS])
P(md_table(['ship', 'n', 'clans'] + list(STATS), rows))
# per map spread
rows = []
for k in FOUR:
    for m, v in sorted(by(sh[k], 'map').items(), key=lambda kv: -len(kv[1])):
        if len(v) < 8: continue
        cx, cz = mean(s['nx'] for s in v), mean(s['nz'] for s in v)
        rms = math.sqrt(mean((s['nx'] - cx) ** 2 + (s['nz'] - cz) ** 2 for s in v)) * WU / 1000
        rows.append([k, m, len(v), f'{rms:.1f}', n0(med(s['edge'] for s in v)), n0(pct(v, lambda s: s['stat']))])
        J['ships'][k].setdefault('by_map', {})[m] = dict(n=len(v), pos_spread_km=rms, edge_med_m=med(s['edge'] for s in v), stationary_pct=pct(v, lambda s: s['stat']))
P(md_table(['ship', 'map', 'n', 'spread km', 'edge med m', 'stationary %'], rows))
# differences vs Daring with clan bootstrap
def boot_two(a, b, stat, reps=1000):
    ca, cb = by(a, 'team'), by(b, 'team'); ka, kb = list(ca), list(cb); out = []
    for _ in range(reps):
        va = stat([x for c in R.choices(ka, k=len(ka)) for x in ca[c]]); vb = stat([x for c in R.choices(kb, k=len(kb)) for x in cb[c]])
        if va is not None and vb is not None: out.append(va - vb)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
P('\nDifferences vs Daring (ship - Daring), 95% interval by resampling clans')
J['vs_daring'] = {}
for k in ('Grozovoi', 'Shimakaze', GD):
    J['vs_daring'][k] = {}
    for name in ('pos_spread_km', 'stationary_pct', 'stacked_pct', 'path_med_m', 'edge_iqr_m', 'inside_pct'):
        f = STATS[name]; dlt = f(sh[k]) - f(sh['Daring']); lo, hi = boot_two(sh[k], sh['Daring'], f)
        J['vs_daring'][k][name] = dict(diff=dlt, ci=[lo, hi]); P(f'  {k:10s} {name:16s} {dlt:+8.1f}  ({lo:+.1f} to {hi:+.1f})' + (' *' if lo * hi > 0 else ''))

# ---------------------------------------------------------------- 1b. modes
P('\n## 1b. Two-cluster split (k-means, k=2) on standardized features, per ship')
z4 = scaler([s for k in FOUR for s in sh[k]])
split = {}
for k in FOUR:
    X = [z4(s) for s in sh[k]]; sil, expl, lab = split_quality(X)
    # orient: cluster 1 = the longer-path cluster
    p0 = mean(s['path_m'] for s, l in zip(sh[k], lab) if l == 0); p1 = mean(s['path_m'] for s, l in zip(sh[k], lab) if l == 1)
    if p0 > p1: lab = [1 - l for l in lab]
    for s, l in zip(sh[k], lab): s['km'] = l
    split[k] = dict(silhouette=sil, var_explained=expl, n_short=lab.count(0), n_long=lab.count(1))
    P(f"  {k:10s} n={len(X):3d} silhouette={sil:.3f} variance explained={expl:.2f} sizes={lab.count(0)}/{lab.count(1)}")
# same split on random subsamples of Daring and Gdansk at n=30 and n=58
P('  Reference: the same split on random subsamples of Daring and Gdansk (300 draws each)')
for k in ('Daring', GD):
    for n in (30, 58):
        sils, exs = [], []
        for _ in range(300):
            sub = R.sample(sh[k], n); a, b, _l = split_quality([z4(s) for s in sub]); sils.append(a); exs.append(b)
        split[k][f'sub{n}'] = dict(sil_med=med(sils), sil_lo=q(sils, .025), sil_hi=q(sils, .975), expl_med=med(exs), expl_lo=q(exs, .025), expl_hi=q(exs, .975))
        P(f"  {k:10s} n={n}: silhouette median {med(sils):.3f} (95% of draws {q(sils,.025):.3f} to {q(sils,.975):.3f}); variance explained {med(exs):.2f} ({q(exs,.025):.2f} to {q(exs,.975):.2f})")
# share of subsample draws with silhouette >= the ship's
for k, n in (('Grozovoi', 30), ('Shimakaze', 58)):
    for ref in ('Daring', GD):
        cnt = 0
        for _ in range(300):
            a, b, _l = split_quality([z4(s) for s in R.sample(sh[ref], n)]); cnt += a >= split[k]['silhouette']
        split[k][f'share_{ref}_draws_at_least_as_separated'] = cnt / 300
        P(f"  {k}: {100*cnt/300:.0f}% of {ref} subsamples (n={n}) split at least as cleanly")
# Grozovoi without MACHX
Xg = [z4(s) for s in sh['Grozovoi'] if s['team'] != 'MACHX']; a, b, _l = split_quality(Xg)
split['Grozovoi']['without_MACHX'] = dict(n=len(Xg), silhouette=a, var_explained=b); P(f"  Grozovoi without MACHX n={len(Xg)}: silhouette {a:.3f}, variance explained {b:.2f}")
Xg = [z4(s) for s in sh['Grozovoi'] if s['team'] == 'MACHX']; a, b, _l = split_quality(Xg)
split['Grozovoi']['MACHX_only'] = dict(n=len(Xg), silhouette=a, var_explained=b); P(f"  Grozovoi MACHX only n={len(Xg)}: silhouette {a:.3f}, variance explained {b:.2f}")
J['two_cluster_split'] = split

# Reference modes: is a smoke nearer the cap-sitter profile or the flank-line profile? (leave the ship itself out of the profile)
P('\n## 1c. Reference modes: nearer the cap-sitter profile (Daring, Z-42, Gdansk) or the smoke-line profile (Somers, Gearing, Harugumo, Delny)')
refs = [s for k in CAP_REF + LINE_REF for s in sh[k]]
zr = scaler(refs)
for s in S: s['zr'] = zr(s)
def mode_of(s, leave=None):
    cc = cen([x['zr'] for k in CAP_REF if k != leave for x in sh[k]]); lc = cen([x['zr'] for k in LINE_REF if k != leave for x in sh[k]])
    return 'line' if d2(s['zr'], lc) < d2(s['zr'], cc) else 'sit'
cents = {}
for k in set(CAP_REF + LINE_REF + FOUR):
    cc = cen([x['zr'] for r_ in CAP_REF if r_ != k for x in sh[r_]]); lc = cen([x['zr'] for r_ in LINE_REF if r_ != k for x in sh[r_]])
    for s in sh[k]: s['mode'] = 'line' if d2(s['zr'], lc) < d2(s['zr'], cc) else 'sit'
line_pct = lambda ss: pct(ss, lambda s: s['mode'] == 'line')
J['modes'] = {'definition': 'line = nearer the smoke-line ship profile than the cap-sitter ship profile on 7 standardized features; the ship itself is left out of the profiles', 'features': [n for n, _ in FEATS], 'ships': {}}
rows = []
for k in FOUR + ['Z-42'] + LINE_REF:
    v = sh[k]; lo, hi = boot_stat(v, line_pct); J['modes']['ships'][k] = dict(n=len(v), line_pct=line_pct(v), ci=[lo, hi])
    rows.append([k, len(v), f'{line_pct(v):.0f}', f'{lo:.0f} to {hi:.0f}'])
P(md_table(['ship', 'n', 'line-like %', '95% interval'], rows))
for k in ('Grozovoi', 'Shimakaze', GD):
    dlt = line_pct(sh[k]) - line_pct(sh['Daring']); lo, hi = boot_two(sh[k], sh['Daring'], line_pct)
    J['modes']['ships'][k]['minus_daring'] = dict(diff=dlt, ci=[lo, hi]); P(f'  {k} - Daring line-like share: {dlt:+.0f} points ({lo:+.0f} to {hi:+.0f})')
for k in ('Grozovoi', 'Shimakaze'):
    dlt = line_pct(sh[k]) - line_pct(sh[GD]); lo, hi = boot_two(sh[k], sh[GD], line_pct)
    J['modes']['ships'][k]['minus_gdansk'] = dict(diff=dlt, ci=[lo, hi]); P(f'  {k} - Gdansk line-like share: {dlt:+.0f} points ({lo:+.0f} to {hi:+.0f})')
for k in FOUR:
    agree = mean(1.0 * ((s['mode'] == 'line') == (s['km'] == 1)) for s in sh[k]); J['modes']['ships'][k]['agreement_with_kmeans'] = agree
    P(f'  {k}: reference mode agrees with the k-means split on {100*agree:.0f}% of smokes')
# mode profiles
P('\nMode profiles')
rows = []
for k in FOUR:
    J['modes']['ships'][k]['profile'] = {}
    for mo in ('sit', 'line'):
        v = [s for s in sh[k] if s['mode'] == mo]
        if not v: continue
        d = dict(n=len(v), stationary_pct=pct(v, lambda s: s['stat']), path_med_m=med(s['path_m'] for s in v), edge_med_m=med(s['edge'] for s in v), inside_pct=pct(v, lambda s: s['inside']),
                 stacked_pct=pct(v, lambda s: s['coverage'] == 'stacked'), screen_pct=pct(v, lambda s: s['coverage'] == 'screen'), selfish_pct=pct(v, lambda s: s['coverage'] == 'selfish'),
                 lateral_med=med(s['lat'] for s in v), el_med_s=med(s['el'] for s in v), conc_mean=mean(s['conc'] for s in v), torp_mean=mean(s['torp'] for s in v),
                 cap_contest_pct=pct(v, lambda s: s['pp'] == 'cap_contest'), partners_mean=mean(len(s['partners']) for s in v), win_pct=pct(v, lambda s: s['win']))
        J['modes']['ships'][k]['profile'][mo] = d
        rows.append([k, mo, d['n']] + [n0(d[x], '{:,.2f}' if x in ('lateral_med', 'partners_mean') else '{:,.0f}') for x in list(d)[1:]])
P(md_table(['ship', 'mode', 'n'] + list(d)[1:], rows))

# do modes line up with clan, player, map, time?
P('\n## 1d. Do the modes line up with clan, player, map or time?')
def chi2(ss, key):
    g = by(ss, key); p = mean(1.0 * (s['mode'] == 'line') for s in ss)
    if p in (0, 1): return 0
    return sum((sum(s['mode'] == 'line' for s in v) - p * len(v)) ** 2 / (p * (1 - p) * len(v)) for v in g.values())
def perm_p(ss, key, reps=2000):
    obs = chi2(ss, key); labs = [s['mode'] for s in ss]; keys = [key(s) if callable(key) else s[key] for s in ss]; cnt = 0
    p = mean(1.0 * (l == 'line') for l in labs)
    for _ in range(reps):
        R.shuffle(labs); g = collections.defaultdict(lambda: [0, 0])
        for kk, l in zip(keys, labs): g[kk][0] += l == 'line'; g[kk][1] += 1
        cnt += sum((a - p * n) ** 2 / (p * (1 - p) * n) for a, n in g.values()) >= obs - 1e-9
    return (cnt + 1) / (reps + 1)
def perm_time(ss, reps=2000):
    a = [s['el'] for s in ss if s['mode'] == 'line']; b = [s['el'] for s in ss if s['mode'] == 'sit']
    if len(a) < 3 or len(b) < 3: return None, None
    obs = med(a) - med(b); allv = a + b; cnt = 0
    for _ in range(reps):
        R.shuffle(allv); cnt += abs(med(allv[:len(a)]) - med(allv[len(a):])) >= abs(obs) - 1e-9
    return obs, (cnt + 1) / (reps + 1)
for k in FOUR:
    v = sh[k]; d = {}
    for name, key in (('clan', 'team'), ('player', 'player'), ('map', 'map'), ('game', 'game'), ('result', 'win')):
        d[name + '_p'] = perm_p(v, key)
    obs, p = perm_time(v); d['time_diff_s'] = obs; d['time_p'] = p
    # players with 5+ smokes: how many use both modes (each at least 20%)
    pl = {k2: v2 for k2, v2 in by(v, 'player').items() if len(v2) >= 5}
    both = sum(1 for v2 in pl.values() if 20 <= line_pct(v2) <= 80)
    d['players_5plus'] = len(pl); d['players_5plus_using_both'] = both
    gm = {k2: v2 for k2, v2 in by(v, lambda s: (s['game'], s['player'])).items() if len(v2) >= 3}
    d['player_games_3plus'] = len(gm); d['player_games_3plus_using_both'] = sum(1 for v2 in gm.values() if 0 < line_pct(v2) < 100)
    J['modes']['ships'][k]['lines_up_with'] = d
    P(f"  {k:10s} permutation p: clan {d['clan_p']:.3f}, player {d['player_p']:.3f}, map {d['map_p']:.3f}, game {d['game_p']:.3f}, win/loss {d['result_p']:.3f}; line minus sit median time {n0(obs, '{:+.0f}')} s (p {n0(p, '{:.3f}')}); "
      f"players with 5+ smokes using both modes {both}/{len(pl)}; player-games with 3+ smokes using both {d['player_games_3plus_using_both']}/{len(gm)}")
P('\nBy clan (and player where a clan has several)')
for k in ('Grozovoi', 'Shimakaze'):
    rows = []; J['ships'][k]['by_clan'] = {}; J['ships'][k]['by_player'] = {}
    for t, v in sorted(by(sh[k], 'team').items(), key=lambda kv: -len(kv[1])):
        d = dict(n=len(v), grp=v[0]['grp'], line_pct=line_pct(v), stationary_pct=pct(v, lambda s: s['stat']), stacked_pct=pct(v, lambda s: s['coverage'] == 'stacked'),
                 selfish_pct=pct(v, lambda s: s['coverage'] == 'selfish'), inside_pct=pct(v, lambda s: s['inside']), edge_med_m=med(s['edge'] for s in v), path_med_m=med(s['path_m'] for s in v),
                 maps=dict(C(s['map'] for s in v)), games=len(set(s['game'] for s in v)), players=len(set(s['player'] for s in v)))
        J['ships'][k]['by_clan'][t] = d
        rows.append([t + (' (top 6)' if d['grp'] == 'top' else ''), d['n'], d['games'], d['players'], f"{sum(s['mode']=='line' for s in v)}/{len(v)}", n0(d['stationary_pct']), n0(d['stacked_pct']), n0(d['inside_pct']), n0(d['edge_med_m']), n0(d['path_med_m']),
                     ', '.join(f'{m} {c}' for m, c in C(s['map'] for s in v).most_common())])
        if d['players'] > 1:
            for pn, pv in sorted(by(v, 'player').items(), key=lambda kv: -len(kv[1])):
                short = pn.replace('_KOTS19NA', '')
                J['ships'][k]['by_player'][short] = dict(n=len(pv), line_pct=line_pct(pv), stationary_pct=pct(pv, lambda s: s['stat']), edge_med_m=med(s['edge'] for s in pv))
                rows.append(['  ' + short, len(pv), len(set(s['game'] for s in pv)), '', f"{sum(s['mode']=='line' for s in pv)}/{len(pv)}", n0(pct(pv, lambda s: s['stat'])), n0(pct(pv, lambda s: s['coverage'] == 'stacked')), n0(pct(pv, lambda s: s['inside'])), n0(med(s['edge'] for s in pv)), n0(med(s['path_m'] for s in pv)), ''])
    P(k); P(md_table(['clan', 'n', 'games', 'players', 'line-like', 'stationary %', 'stacked %', 'inside %', 'edge med m', 'path med m', 'maps'], rows))
    P('  by map:', {m: f"{sum(s['mode']=='line' for s in v)}/{len(v)}" for m, v in by(sh[k], 'map').items()})
# Grozovoi: MACHX vs the rest
gz = sh['Grozovoi']; mx = [s for s in gz if s['team'] == 'MACHX']; ot = [s for s in gz if s['team'] != 'MACHX']
J['ships']['Grozovoi']['MACHX_vs_others'] = {}
for name, v in (('MACHX', mx), ('others', ot)):
    d = dict(n=len(v), clans=len(set(s['team'] for s in v)), line_pct=line_pct(v), stationary_pct=pct(v, lambda s: s['stat']), inside_pct=pct(v, lambda s: s['inside']), edge_med_m=med(s['edge'] for s in v),
             path_med_m=med(s['path_m'] for s in v), stacked_pct=pct(v, lambda s: s['coverage'] == 'stacked'), selfish_pct=pct(v, lambda s: s['coverage'] == 'selfish'), pos_spread_km=pooled_rms(v, 4), maps=dict(C(s['map'] for s in v)))
    J['ships']['Grozovoi']['MACHX_vs_others'][name] = d; P('  Grozovoi', name, {a: (round(b, 1) if isinstance(b, float) else b) for a, b in d.items()})
# leave-one-clan-out range of the line share
for k in ('Grozovoi', 'Shimakaze'):
    lo = {t: line_pct([s for s in sh[k] if s['team'] != t]) for t in set(s['team'] for s in sh[k])}
    J['modes']['ships'][k]['leave_one_clan_out_line_pct'] = [min(lo.values()), max(lo.values())]
    P(f"  {k}: line-like share leaving one clan out ranges {min(lo.values()):.0f} to {max(lo.values()):.0f}% (drop {min(lo, key=lo.get)} for the low, {max(lo, key=lo.get)} for the high)")
# top 6 vs rest
for k in ('Shimakaze', 'Grozovoi', GD, 'Daring'):
    v = sh[k]; t = [s for s in v if s['grp'] == 'top']; r_ = [s for s in v if s['grp'] == 'rest']
    if len(t) >= 8 and len(r_) >= 8:
        lo, hi = boot_diff(v, line_pct); lo2, hi2 = boot_diff(v, STATS['stationary_pct'])
        J['modes']['ships'][k]['top_vs_rest'] = dict(n_top=len(t), n_rest=len(r_), line_top=line_pct(t), line_rest=line_pct(r_), line_diff_ci=[lo, hi], stat_top=pct(t, lambda s: s['stat']), stat_rest=pct(r_, lambda s: s['stat']), stat_diff_ci=[lo2, hi2])
        P(f"  {k}: Top 6 n={len(t)} line-like {line_pct(t):.0f}% vs Rest n={len(r_)} {line_pct(r_):.0f}%, diff interval {ci((lo, hi))}; stationary {pct(t, lambda s: s['stat']):.0f}% vs {pct(r_, lambda s: s['stat']):.0f}%, {ci((lo2, hi2))}")
    else: P(f'  {k}: Top 6 n={len(t)}, Rest n={len(r_)}: too few for a Top 6 vs Rest comparison')
pn = [s for s in S if s['is_pn'] and s['ship'] in FOUR]
J['pn'] = [dict(ship=s['ship'], map=s['map'], mode=s['mode'], movement=s['movement'], edge_m=s['edge'], link=s['link']) for s in pn]
P('  PN on these four ships:', [(s['ship'], s['map'], s['mode'], s['movement'], round(s['edge'])) for s in pn])

# ---------------------------------------------------------------- 2. emission and radius
P('\n## 2. Observed emission and radius, ships with 20+ smokes')
E_SHIPS = [k for k, v in sorted(sh.items(), key=lambda kv: -len(kv[1])) if len(v) >= 20]
rows = []
for k in E_SHIPS:
    v = sh[k]; base = v[0]['emission_s']
    for s in v: s['ratio'] = s['obs_emission_s'] / s['emission_s']; s['clean'] = (not s['cut_short']) and s['r']['owner_flag'] == 'false' and s['ratio'] >= 0.9
    o = [s['obs_emission_s'] for s in v]; cl = [s for s in v if s['clean']]
    short_unflagged = sum(1 for s in v if not s['cut_short'] and s['ratio'] < 0.9)
    # between-player share of variance among clean smokes, players with 3+
    pl = {p: pv for p, pv in by(cl, 'player').items() if len(pv) >= 3}
    allv = [s['obs_emission_s'] for pv in pl.values() for s in pv]; gm = mean(allv) if allv else None
    sst = sum((x - gm) ** 2 for x in allv) if allv else 0; ssb = sum(len(pv) * (mean(s['obs_emission_s'] for s in pv) - gm) ** 2 for pv in pl.values()) if allv else 0
    eta = ssb / sst if sst else None
    # null for eta: shuffle player labels
    cnt = 0
    if sst:
        sizes = [len(pv) for pv in pl.values()]
        for _ in range(500):
            R.shuffle(allv); i = 0; b = 0
            for n in sizes: b += n * (mean(allv[i:i + n]) - gm) ** 2; i += n
            cnt += b / sst >= eta
    pmed = {p: med(s['obs_emission_s'] for s in pv) for p, pv in pl.items()}
    near = mean(1.0 * (abs(s['obs_emission_s'] - pmed[p]) <= max(1.5, 0.06 * base)) for p, pv in pl.items() for s in pv) if pl else None
    within_iqr = med(iqr([s['obs_emission_s'] for s in pv]) for pv in pl.values() if len(pv) >= 5) if any(len(pv) >= 5 for pv in pl.values()) else None
    # player medians grouped into steps of the base (ratio rounded to 0.1)
    steps = C(round(m / base * 10) / 10 for m in pmed.values())
    # players whose game medians differ (2+ games with 2+ clean smokes)
    sw = 0; multi = 0
    for p, pv in pl.items():
        gms = [med(s['obs_emission_s'] for s in gv) for gv in by(pv, 'game').values() if len(gv) >= 2]
        if len(gms) >= 2:
            multi += 1; sw += (max(gms) - min(gms)) > max(2.0, 0.08 * base)
    d = dict(n=len(v), base_s=base, median_s=med(o), q1_s=q(o, .25), q3_s=q(o, .75), p10_s=q(o, .1), p90_s=q(o, .9), ratio_median=med(o) / base, cut_short_n=sum(s['cut_short'] for s in v), cut_short_pct=pct(v, lambda s: s['cut_short']),
             short_not_flagged_n=short_unflagged, clean_n=len(cl), clean_median_s=med(s['obs_emission_s'] for s in cl), clean_ratio_q1=q([s['ratio'] for s in cl], .25), clean_ratio_q3=q([s['ratio'] for s in cl], .75),
             players_3plus=len(pl), between_player_variance_share=eta, between_player_perm_p=(cnt + 1) / 501 if sst else None, share_within_tolerance_of_player_median=near, within_player_iqr_s=within_iqr,
             player_median_steps={str(a): b for a, b in sorted(steps.items())}, players_multi_game=multi, players_changed_between_games=sw,
             radius_m=sorted(set(round(s['radius_m']) for s in v)), radius_values={str(a): b for a, b in C(round(s['radius_m']) for s in v).items()}, radius_equals_base_pct=pct(v, lambda s: s['r']['radius'] == s['r']['base_radius']))
    J['emission'][k] = d
    rows.append([k, d['n'], n0(base), f"{d['median_s']:.1f}", f"{d['q1_s']:.1f} to {d['q3_s']:.1f}", f"{d['ratio_median']:.2f}", f"{d['cut_short_n']} ({d['cut_short_pct']:.0f}%)", short_unflagged, len(pl), n0(eta, '{:.2f}'), n0(near and 100 * near), n0(within_iqr, '{:.1f}'),
                 ' '.join(f'{a}x:{b}' for a, b in sorted(steps.items())), f'{sw}/{multi}', '/'.join(str(x) for x in d['radius_m'])])
P(md_table(['ship', 'n', 'base s', 'median s', 'quartiles', 'ratio', 'cut short', 'short, not flagged', 'players 3+', 'between-player share', '% near own median', 'within-player IQR s', 'player medians by step', 'changed between games', 'radius m'], rows))
P('  radius differs from base on', sum(s['r']['radius'] != s['r']['base_radius'] for s in S), 'of', len(S), 'smokes (all ships)')
P('  the one Napoli smoke at 450 m:', [(s['r']['owner_flag'], s['r']['owner_note']) for s in sh['Napoli'] if round(s['radius_m']) == 450])
# clan-level view for the ships with clear steps
P('\nPlayer medians (clean smokes, 3+), ships with more than one step')
J['emission_players'] = {}
for k in E_SHIPS:
    cl = [s for s in sh[k] if s['clean']]; base = sh[k][0]['emission_s']
    pl = sorted(((p, pv) for p, pv in by(cl, 'player').items() if len(pv) >= 3), key=lambda x: med(s['obs_emission_s'] for s in x[1]))
    J['emission_players'][k] = [dict(player=p.replace('_KOTS19NA', ''), clan=pv[0]['team'], n=len(pv), median_s=med(s['obs_emission_s'] for s in pv), min_s=min(s['obs_emission_s'] for s in pv), max_s=max(s['obs_emission_s'] for s in pv)) for p, pv in pl]
    if k in ('Somers', 'Gearing', 'Harugumo', 'Grozovoi', 'Shimakaze', 'Svea'):
        P(' ', k, ' | '.join(f"{p.replace('_KOTS19NA','')[:14]} {med(s['obs_emission_s'] for s in pv):.0f}s n{len(pv)}" for p, pv in pl))
# usage vs emission: long vs short builds within a ship (split at the midpoint between steps), clan bootstrap
P('\nUsage by observed emission (clean smokes): longer group minus shorter group, 95% interval by resampling clans')
CUT = {'Somers': 36.5, 'Gearing': 36.5, 'Harugumo': 49, 'Svea': 11.6, 'Shimakaze': 24.5, 'Grozovoi': 24.5, 'Daring': 10.6, GD: 21.2, 'Napoli': 46.5}
USE = {'stationary_pct': lambda ss: pct(ss, lambda s: s['stat']), 'path_med_m': lambda ss: med(s['path_m'] for s in ss), 'stacked_pct': lambda ss: pct(ss, lambda s: s['coverage'] == 'stacked'),
       'selfish_pct': lambda ss: pct(ss, lambda s: s['coverage'] == 'selfish'), 'inside_pct': lambda ss: pct(ss, lambda s: s['inside']), 'conc_mean': lambda ss: mean(s['conc'] for s in ss), 'win_pct': lambda ss: pct(ss, lambda s: s['win'])}
J['emission_usage'] = {}
rows = []
for k, cut in CUT.items():
    cl = [s for s in sh[k] if s['clean']]; lg = [s for s in cl if s['obs_emission_s'] >= cut]; st = [s for s in cl if s['obs_emission_s'] < cut]
    if len(lg) < 8 or len(st) < 8: P(f'  {k}: long n={len(lg)}, short n={len(st)}: too few'); continue
    d = dict(cut_s=cut, n_long=len(lg), n_short=len(st), clans_long=len(set(s['team'] for s in lg)), clans_short=len(set(s['team'] for s in st)))
    row = [k, f'{cut:g}', f"{len(lg)} ({d['clans_long']} clans)", f"{len(st)} ({d['clans_short']} clans)"]
    for name, f in USE.items():
        def stat(ss, f=f, cut=cut):
            a = [s for s in ss if s['obs_emission_s'] >= cut]; b = [s for s in ss if s['obs_emission_s'] < cut]
            return f(a) - f(b) if a and b else None
        lo, hi = boot_stat(cl, stat); d[name] = dict(long=f(lg), short=f(st), diff=f(lg) - f(st), ci=[lo, hi])
        row.append(f"{f(lg):,.0f} vs {f(st):,.0f} ({lo:+,.0f} to {hi:+,.0f}{' *' if lo * hi > 0 else ''})")
    J['emission_usage'][k] = d; rows.append(row)
P(md_table(['ship', 'split at s', 'long n', 'short n'] + list(USE), rows))
# observed emission by movement / coverage / inside within ship (clean)
P('\nMedian observed emission (clean) by usage, within ship')
rows = []
J['emission_by_usage'] = {}
for k in E_SHIPS:
    cl = [s for s in sh[k] if s['clean']]; d = {}
    for name, f in (('stationary', lambda s: s['stat']), ('moving', lambda s: not s['stat'] and s['movement'] != 'unclassified'), ('selfish', lambda s: s['coverage'] == 'selfish'), ('screen', lambda s: s['coverage'] == 'screen'),
                    ('stacked', lambda s: s['coverage'] == 'stacked'), ('inside cap', lambda s: s['inside']), ('outside cap', lambda s: not s['inside']), ('conc dmg > 0', lambda s: s['conc'] > 0), ('no conc dmg', lambda s: s['conc'] == 0)):
        v = [s['obs_emission_s'] for s in cl if f(s)]; d[name] = dict(n=len(v), median_s=med(v))
    J['emission_by_usage'][k] = d
    rows.append([k] + [f"{n0(x['median_s'], '{:.1f}')} ({x['n']})" for x in d.values()])
P(md_table(['ship'] + list(d), rows))
# cut short: where
cs = [s for s in S if s['cut_short']]
J['cut_short_all'] = dict(n=len(cs), pct=100 * len(cs) / len(S), inside_pct=pct(cs, lambda s: s['inside']), inside_pct_others=pct([s for s in S if not s['cut_short']], lambda s: s['inside']),
                          deaths_mean=mean(s['deaths'] for s in cs), win_pct=pct(cs, lambda s: s['win']))
P('  cut short overall:', J['cut_short_all'])
P('  path length vs emission, moving clean smokes, Spearman by ship:')
def spearman(a, b):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for i, j in enumerate(o): r[j] = i
        return r
    ra, rb = rk(a), rk(b); ma, mb = mean(ra), mean(rb)
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / den if den else None
for k in ('Somers', 'Gearing', 'Harugumo'):
    v = [s for s in sh[k] if s['clean'] and not s['stat']]; r_ = spearman([s['obs_emission_s'] for s in v], [s['path_m'] for s in v]); J['emission'][k]['spearman_path_vs_emission_moving'] = r_; P(f'    {k}: {r_:.2f} (n={len(v)})')

json.dump(J, open(os.path.join(OUT, 'ship-variance.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=lambda o: None)

# ---------------------------------------------------------------- figures
MODE_COL = {'sit': BLUE, 'line': ORANGE}
def draw_ship_map(p, ss, mark_team=None):
    for s in ss:
        col = MODE_COL[s['mode']]
        if len(s['npath']) > 1: p.line(s['npath'], stroke=col, width=1.6, opacity=0.55)
    for s in ss:
        p.dot(s['nx'], s['nz'], r=3.2, fill=MODE_COL[s['mode']], opacity=0.85, stroke=INK if mark_team and s['team'] == mark_team else None, title=f"{s['team']} {s['movement']} {s['coverage']}")
def cnt_label(ss):
    return f"n={len(ss)}: {sum(s['mode']=='sit' for s in ss)} sit, {sum(s['mode']=='line' for s in ss)} line"
if '--nofig' not in sys.argv:
    maps1 = ['Hotspot', 'Loop', 'Mountain Range', 'Sea of Fortune']; size = 262; gx = 300; gy = 322
    fig = Fig(60 + gx * 4 + 10, 112 + gy * 4, 'Grozovoi and Shimakaze smokes by mode, beside Daring and Gdansk',
              'Each line is one laid smoke, the dot its centre. Team-normalized: north-spawn teams mirrored north-south so own spawn is at the bottom. Dashed circles are caps.')
    fig.legend(60, 74, [('Cap-sitting mode (short, parked, near a cap)', BLUE), ('Smoke-line mode (long, moving, stacked or on a flank)', ORANGE)])
    fig.add(f'<circle cx="760" cy="71" r="4.5" fill="{MUTED}" stroke="{INK}" stroke-width="1.2"/>' + T(770, 75, 'black outline = MACHX (half of all Grozovoi smokes)', size=12, fill=INK, anchor='start'))
    for r_, k in enumerate(FOUR):
        for c_, m in enumerate(maps1):
            v = [s for s in sh[k] if s['map'] == m]
            p = Panel(m, 60 + c_ * gx, 118 + r_ * gy, size, G, title=f"{'Gdansk' if k == GD else k}, {m}", grid_labels=False, normalized=False, dim=0.62); p.base = p.base.replace('../maps/', '../../round3/maps/')
            draw_ship_map(p, v, 'MACHX' if k == 'Grozovoi' else None); fig.add(p)
            fig.add(T(60 + c_ * gx + size / 2, 118 + r_ * gy + size + 13, cnt_label(v) + (' (small n)' if len(v) < 15 else ''), size=10.5))
    fig.save(os.path.join(OUT, 'fig1-modes-map-views'))
    maps2 = ['Okinawa', 'Land of Fire', 'Sleeping Giant']
    ships2 = ['Shimakaze', 'Daring', GD]
    fig = Fig(60 + gx * 3 + 10, 112 + gy * 3, 'Shimakaze on its other maps, beside Daring and Gdansk',
              'Team-normalized. Okinawa: north-east-spawn teams mirrored across the NW-SE diagonal, own spawn bottom left. Other maps: own spawn at the bottom.')
    fig.legend(60, 74, [('Cap-sitting mode', BLUE), ('Smoke-line mode', ORANGE)])
    for r_, k in enumerate(ships2):
        for c_, m in enumerate(maps2):
            v = [s for s in sh[k] if s['map'] == m]
            p = Panel(m, 60 + c_ * gx, 118 + r_ * gy, size, G, title=f"{'Gdansk' if k == GD else k}, {m}", grid_labels=False, normalized=False, dim=0.62); p.base = p.base.replace('../maps/', '../../round3/maps/')
            draw_ship_map(p, v); fig.add(p)
            fig.add(T(60 + c_ * gx + size / 2, 118 + r_ * gy + size + 13, cnt_label(v) + (' (small n)' if len(v) < 15 else ''), size=10.5))
    fig.save(os.path.join(OUT, 'fig2-shimakaze-other-maps'))

    # fig 3: path length vs distance to cap edge
    W = 1240; pw = 262; ph = 230
    fig = Fig(W, 400, 'The two modes without the map: length laid against distance to the contested cap',
              'One dot per smoke. Left of the dashed line = inside the cap. Daring stays short and near the cap; Shimakaze and Grozovoi spread into long smokes far from it, with no clean gap.')
    fig.legend(60, 74, [('Cap-sitting mode', BLUE), ('Smoke-line mode', ORANGE)])
    for i, k in enumerate(FOUR):
        x0 = 70 + i * 295; y0 = 112
        X = lambda e: x0 + (max(-3000, min(11000, e)) + 3000) / 14000 * pw; Y = lambda pm: y0 + ph - min(3000, pm) / 3000 * ph
        o = f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="none" stroke="{GRID}"/>'
        for e in (0, 5000, 10000): o += f'<line x1="{X(e):.1f}" y1="{y0}" x2="{X(e):.1f}" y2="{y0+ph}" stroke="{MUTED if e == 0 else GRID}" stroke-width="1" {"stroke-dasharray=\'4 3\'" if e == 0 else ""}/>' + T(X(e), y0 + ph + 14, f'{e//1000} km', size=10)
        for pm in (0, 1000, 2000, 3000): o += f'<line x1="{x0}" y1="{Y(pm):.1f}" x2="{x0+pw}" y2="{Y(pm):.1f}" stroke="{GRID}" stroke-width="1"/>' + (T(x0 - 5, Y(pm) + 4, f'{pm/1000:g} km', size=10, anchor='end') if i == 0 else '')
        for s in sh[k]: o += f'<circle cx="{X(s["edge"]):.1f}" cy="{Y(s["path_m"] or 0):.1f}" r="3" fill="{MODE_COL[s["mode"]]}" opacity="0.6"/>'
        o += T(x0, y0 - 8, f"{'Gdansk' if k == GD else k} (n={len(sh[k])}, {line_pct(sh[k]):.0f}% smoke-line)", size=12.5, fill=INK, anchor='start', weight='600')
        o += T(x0 + pw / 2, y0 + ph + 30, 'smoke edge to contested cap edge', size=10.5)
        fig.add(o)
    fig.add(T(18, 112 + ph / 2, 'length laid', size=10.5).replace('<text ', f'<text transform="rotate(-90 18 {112 + ph / 2})" '))
    fig.save(os.path.join(OUT, 'fig3-modes-length-vs-cap'))

    # fig 4: observed emission by ship
    order = sorted(E_SHIPS, key=lambda k: (HABITS.index(HABIT[k]) if k in HABIT else 9, -len(sh[k])))
    rh = 34; x0 = 250; pw = 900; y0 = 122; xmax = 65
    fig = Fig(1240, y0 + rh * len(order) + 60, 'Observed smoke emission by ship (ships with 20+ smokes)',
              'One dot per smoke. Black tick = the base value in the game data; dots to the right of it lasted longer. Red = cut short (the smoker died while emitting).')
    fig.legend(60, 78, [('Observed emission, one smoke', BLUE), ('Cut short', RED)])
    fig.add(f'<rect x="420" y="67" width="3" height="14" fill="{INK}"/>' + T(430, 79, 'Base emission', size=12, fill=INK, anchor='start'))
    X = lambda v: x0 + min(xmax, v) / xmax * pw
    for t in range(0, xmax + 1, 10):
        fig.add(f'<line x1="{X(t):.1f}" y1="{y0-6}" x2="{X(t):.1f}" y2="{y0+rh*len(order)}" stroke="{GRID}" stroke-width="1"/>' + T(X(t), y0 + rh * len(order) + 16, f'{t} s', size=10.5))
    last = None
    rj = random.Random(5)
    for i, k in enumerate(order):
        y = y0 + i * rh + rh / 2; v = sh[k]; d = J['emission'][k]
        hb = HABIT.get(k, 'other')
        if hb != last and i: fig.add(f'<line x1="24" y1="{y0+i*rh:.1f}" x2="{x0+pw}" y2="{y0+i*rh:.1f}" stroke="{MUTED}" stroke-width="0.6" opacity="0.6"/>')
        last = hb
        fig.add(T(x0 - 96, y + 4, ('Gdansk' if k == GD else k), size=12, fill=INK, anchor='end', weight='600') + T(x0 - 10, y + 4, f"n={d['n']}, x{d['ratio_median']:.2f}", size=10, anchor='end'))
        o = ''
        for s in v:
            col = RED if s['cut_short'] else BLUE
            o += f'<circle cx="{X(s["obs_emission_s"]):.1f}" cy="{y + rj.uniform(-9, 9):.1f}" r="2.3" fill="{col}" opacity="{0.9 if s["cut_short"] else 0.4}"/>'
        o += f'<rect x="{X(d["base_s"])-1.5:.1f}" y="{y-13}" width="3" height="26" fill="{INK}"/>'
        fig.add(o)
    fig.add(T(x0 + pw / 2, y0 + rh * len(order) + 36, 'seconds from activation to the last new puff. The label gives n and the median as a multiple of the base. Groups, top to bottom: flank smoke lines, cap sitters, parked cruiser smoke, moving exhaust.', size=10.5))
    fig.save(os.path.join(OUT, 'fig4-emission-by-ship'))
    P('figures saved')
