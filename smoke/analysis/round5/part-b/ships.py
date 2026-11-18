# Round 5 part B: ship tendencies (B1 cap sitters, B2 getaway smokes, B3 long smokes, B4 hybrids).
# Run: python -I -X utf8 ships.py   -> writes out.txt and ships.json next to this file. Read-only on the batch.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
import json, math, random
HERE_B = os.path.dirname(os.path.abspath(__file__))
S, G = load5()
random.seed(519)
OUT = []
def P(*a):
    line = ' '.join(str(x) for x in a); OUT.append(line); print(line)
J = {}

# ---------- helpers
def set_diff(ss, fa, fb, stat, reps=1000):
    """95% interval of stat(smokes matching fa) - stat(smokes matching fb), resampling whole clans."""
    cl = by([s for s in ss if fa(s) or fb(s)], 'team'); keys = list(cl); out = []
    for _ in range(reps):
        pick = [x for c in random.choices(keys, k=len(keys)) for x in cl[c]]
        a = [x for x in pick if fa(x)]; b = [x for x in pick if fb(x)]
        if not a or not b: continue
        va, vb = stat(a), stat(b)
        if va is not None and vb is not None: out.append(va - vb)
    if len(out) < 100: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def ship_diff(a, b, stat):
    return set_diff(S, lambda s: s['ship'] == a, lambda s: s['ship'] == b, stat)
def dif(a, b):
    return None if a is None or b is None else a - b
def rnd(x, d=1):
    return None if x is None else round(x, d)
def iv(lohi, d=1):
    return None if lohi[0] is None else [round(lohi[0], d), round(lohi[1], d)]
def clear(lohi):
    return lohi[0] is not None and lohi[0] * lohi[1] > 0
def fiv(lohi, d=0):
    if lohi is None or lohi[0] is None: return '-'
    f = '{:,.%df}' % d
    return f'{f.format(lohi[0])} to {f.format(lohi[1])}' + (' *' if lohi[0] * lohi[1] > 0 else '')
def fv(x, d=0):
    return 'too few' if x is None else ('{:,.%df}' % d).format(x)
def grp_rows(label, ss, metrics, digits):
    """All / Top 6 / Rest rows for one group of smokes. metrics: {name: stat}. Rates only when n >= 8."""
    rows = []
    for gname, sub in (('all', ss), ('top6', [s for s in ss if s['grp'] == 'top']), ('rest', [s for s in ss if s['grp'] == 'rest'])):
        r = dict(group=label, split=gname, n=len(sub), small_n=8 <= len(sub) < 15, clans=len({s['team'] for s in sub}))
        for m, st in metrics.items():
            ok = len(sub) >= 8
            r[m] = rnd(st(sub), digits.get(m, 1)) if ok else None
            r[m + '_ci'] = iv(boot_stat(sub, st), digits.get(m, 1)) if ok and r['clans'] >= 3 else None
        rows.append(r)
    t, re_ = rows[1], rows[2]
    d = dict(group=label, split='top6 minus rest')
    for m, st in metrics.items():
        if t['n'] >= 8 and re_['n'] >= 8:
            d[m] = rnd(dif(st([s for s in ss if s['grp'] == 'top']), st([s for s in ss if s['grp'] == 'rest'])), digits.get(m, 1))
            d[m + '_ci'] = iv(boot_diff(ss, st), digits.get(m, 1))
        else:
            d[m] = None; d[m + '_ci'] = None
    rows.append(d)
    return rows
def print_rows(rows, metrics, digits):
    hdr = ['group', 'split', 'n', 'clans'] + list(metrics)
    out = []
    for r in rows:
        cells = [r['group'], r['split'], r.get('n', ''), r.get('clans', '')]
        for m in metrics:
            v = r.get(m); c = r.get(m + '_ci')
            cells.append('too few' if v is None else f"{fv(v, digits.get(m, 1))}" + (f" ({fiv(c, digits.get(m, 1))})" if c else '') + (' sn' if r.get('small_n') else ''))
        out.append(cells)
    P(md_table(hdr, out))
def pctf(f):
    return lambda ss: 100 * sum(1 for s in ss if f(s)) / len(ss) if ss else None
def meanf(k):
    return lambda ss: mean(s[k] for s in ss) if ss else None
def medf(k, filt=None):
    def st(ss):
        v = [s[k] for s in ss if s[k] is not None and (filt is None or filt(s))]
        return med(v) if v else None
    return st
def of(ship): return [s for s in S if s['ship'] == ship]

P('totals', len(S), 'DD top/rest', sum(1 for s in S if s['cls'] == 'destroyer' and s['grp'] == 'top'), sum(1 for s in S if s['cls'] == 'destroyer' and s['grp'] == 'rest'))

# ================= B1 cap sitters
P('\n===== B1 cap sitters')
for s in S:
    cov = s['j']['classification']['coverage']
    s['mate'] = bool(cov['stacked'] or cov['screen'])
B1M = {'edge_med_m': medf('edge'), 'edge_med_no_mrA_m': medf('edge', lambda s: not s['mrA']), 'inside_pct': pctf(lambda s: s['inside']),
       'teammate_pct': pctf(lambda s: s['mate']), 'conc_per_smoke': meanf('conc')}
B1D = {'edge_med_m': 0, 'edge_med_no_mrA_m': 0, 'inside_pct': 1, 'teammate_pct': 1, 'conc_per_smoke': 0}
b1 = []
for sh in SITTERS:
    ss = of(sh); rows = grp_rows(sh, ss, B1M, B1D); b1 += rows
    P(sh, 'mrA smokes', sum(s['mrA'] for s in ss), '| coverage labels', dict(C(s['coverage'] for s in ss)), '| batch selfish flag %', rnd(pctf(lambda s: s['selfish'])(ss)), '|', clan_counts(ss))
print_rows(b1, B1M, B1D)
b1c = []
for m, st in B1M.items():
    for a, b in (('Daring', 'Gdańsk'),):
        d = dif(st(of(a)), st(of(b))); c = ship_diff(a, b, st)
        b1c.append(dict(contrast=f'{a} minus {b}', metric=m, diff=rnd(d, B1D[m]), ci=iv(c, B1D[m]), clear=clear(c)))
        P(f'{a} minus {b}', m, fv(d, B1D[m]), fiv(c, B1D[m]))
# within group contrasts Daring vs Gdansk for Top 6 and for Rest
for g in ('top', 'rest'):
    for m, st in B1M.items():
        fa = lambda s, g=g: s['ship'] == 'Daring' and s['grp'] == g; fb = lambda s, g=g: s['ship'] == 'Gdańsk' and s['grp'] == g
        a = [s for s in S if fa(s)]; b = [s for s in S if fb(s)]
        d = dif(st(a), st(b)); c = set_diff(S, fa, fb, st)
        b1c.append(dict(contrast=f'Daring minus Gdańsk ({GROUP_LABEL[g]})', metric=m, n_a=len(a), n_b=len(b), diff=rnd(d, B1D[m]), ci=iv(c, B1D[m]), clear=clear(c)))
        P(f'Daring minus Gdańsk [{g}] n {len(a)}/{len(b)}', m, fv(d, B1D[m]), fiv(c, B1D[m]))
# second way check on medians: mean edge and share within 1 km
for sh in ('Daring', 'Gdańsk'):
    ss = of(sh); P('check', sh, 'mean edge', rnd(mean(s['edge'] for s in ss), 0), 'share edge<1000', rnd(pctf(lambda s: s['edge'] < 1000)(ss)), 'conc median', rnd(med(s['conc'] for s in ss), 0),
                   'share conc>0', rnd(pctf(lambda s: s['conc'] > 0)(ss)), 'stacked%', rnd(pctf(lambda s: s['j']['classification']['coverage']['stacked'])(ss)),
                   'screen%', rnd(pctf(lambda s: s['j']['classification']['coverage']['screen'])(ss)))
J['B1'] = dict(note='edge = metres from smoke edge to contested cap edge (negative inside). teammate_pct = coverage stacked or screen. conc = concealed damage per smoke. ci = 95% by resampling clans. None = fewer than 8 smokes.',
               rows=b1, contrasts=b1c)

# ================= B2 getaway smokes
P('\n===== B2 getaway smokes')
for s in S:
    me = next((x for x in s['j']['smokees'] if x['role'] == 'smoker'), None)
    life = s['t1'] - s['t0'] if s['t1'] and s['t1'] > s['t0'] else None
    s['sm_secs'] = me['seconds_concealed'] if me else None
    s['life_obs'] = life
    s['cov_life'] = min(100, 100 * me['seconds_concealed'] / life) if me and life else None
    s['undet_life'] = s['cov_life'] * s['undetected_pct'] / 100 if s['cov_life'] is not None and s['undetected_pct'] is not None else None
    s['escape_tag'] = 'escape' in s['tags']
def meank(k):
    def st(ss):
        v = [s[k] for s in ss if s[k] is not None]
        return mean(v) if v else None
    return st
B2M = {'deaths_per_100': lambda ss: rate100(ss, 'deaths'), 'smoker_deaths_per_100': lambda ss: rate100(ss, 'd_smoker'), 'hurt_smoker_per_100': lambda ss: rate100(ss, 'hurt_smoker'),
       'undetected_pct_of_covered_time': meank('undetected_pct'), 'undetected_pct_of_smoke_life': meank('undet_life'), 'escape_tag_pct': pctf(lambda s: s['escape_tag']),
       'cut_short_pct': pctf(lambda s: s['cut_short']), 'conc_per_smoke': meanf('conc')}
B2D = {k: 1 for k in B2M}; B2D['conc_per_smoke'] = 0
is_it_ca = lambda s: s['kind'] == 'exhaust' and s['cls'] == 'cruiser'
is_bb = lambda s: s['cls'] == 'battleship'
is_get = lambda s: s['kind'] == 'exhaust' or s['cls'] == 'battleship'
groups2 = [('Napoli', lambda s: s['ship'] == 'Napoli'), ('Venezia', lambda s: s['ship'] == 'Venezia'), ('Italian cruisers (Napoli + Venezia)', is_it_ca),
           ('C. Colombo (battleship)', lambda s: s['ship'] == 'C. Colombo'), ('Conte Verde (battleship)', lambda s: s['ship'] == 'Conte Verde'),
           ('Sicilia (battleship)', lambda s: s['ship'] == 'Sicilia'), ('Irresistible (battleship, ordinary smoke)', lambda s: s['ship'] == 'Irresistible'),
           ('All battleships', is_bb), ('All getaway smokes (exhaust or battleship)', is_get),
           ('BASELINE all smokes', lambda s: True), ('BASELINE all other smokes (not getaway)', lambda s: not is_get(s)),
           ('BASELINE cruiser smokers, all', lambda s: s['cls'] == 'cruiser'), ('BASELINE cruiser smokers, ordinary smoke (Svea, Jinan...)', lambda s: s['cls'] == 'cruiser' and s['kind'] != 'exhaust'),
           ('BASELINE destroyer smokers', lambda s: s['cls'] == 'destroyer')]
b2 = []
for name, f in groups2:
    ss = [s for s in S if f(s)]; b2 += grp_rows(name, ss, B2M, B2D)
    if not name.startswith('BASELINE'): P(name, 'n', len(ss), 'kinds', dict(C(s['kind'] for s in ss)), 'deaths', sum(s['deaths'] for s in ss), 'smoker deaths', sum(s['d_smoker'] for s in ss), '|', clan_counts(ss))
print_rows(b2, B2M, B2D)
b2c = []
pairs = [('Italian cruisers minus cruiser ordinary smoke', is_it_ca, lambda s: s['cls'] == 'cruiser' and s['kind'] != 'exhaust'),
         ('Italian cruisers minus all other smokes', is_it_ca, lambda s: not is_get(s)),
         ('Napoli minus cruiser ordinary smoke', lambda s: s['ship'] == 'Napoli', lambda s: s['cls'] == 'cruiser' and s['kind'] != 'exhaust'),
         ('Battleships minus Italian cruisers', is_bb, is_it_ca),
         ('Battleships minus all other smokes', is_bb, lambda s: not is_get(s)),
         ('Battleships minus cruiser ordinary smoke', is_bb, lambda s: s['cls'] == 'cruiser' and s['kind'] != 'exhaust'),
         ('All getaway minus all other smokes', is_get, lambda s: not is_get(s))]
for name, fa, fb in pairs:
    for m in ('deaths_per_100', 'smoker_deaths_per_100', 'hurt_smoker_per_100', 'undetected_pct_of_covered_time', 'undetected_pct_of_smoke_life', 'escape_tag_pct'):
        st = B2M[m]; d = dif(st([s for s in S if fa(s)]), st([s for s in S if fb(s)])); c = set_diff(S, fa, fb, st)
        b2c.append(dict(contrast=name, metric=m, diff=rnd(d), ci=iv(c), clear=clear(c))); P(name, '|', m, fv(d, 1), fiv(c, 1))
# detail: who died in getaway smokes, and escape primary purpose
for name, f in (('Italian cruisers', is_it_ca), ('Battleships', is_bb)):
    ss = [s for s in S if f(s)]
    P(name, 'dead by class', dict(C((d['cls'], 'smoker' if d['is_smoker'] else 'other') for s in ss for d in s['dead'])), '| primary purpose', dict(C(s['pp'] for s in ss).most_common(5)),
      '| undetected None', sum(s['undetected_pct'] is None for s in ss), '| median covered s', rnd(med(s['sm_secs'] for s in ss if s['sm_secs'] is not None)), 'median life s', rnd(med(s['life_obs'] for s in ss if s['life_obs'])),
      '| median undetected % covered', rnd(med(s['undetected_pct'] for s in ss if s['undetected_pct'] is not None)), '| fully detected whole time %', rnd(pctf(lambda s: (s['undetected_pct'] or 0) < 5)(ss)),
      '| movement', dict(C(s['movement'] for s in ss)))
P('escape-tagged getaway smokes vs not: smoker deaths per 100', rnd(rate100([s for s in S if is_get(s) and s['escape_tag']], 'd_smoker')), len([s for s in S if is_get(s) and s['escape_tag']]),
  rnd(rate100([s for s in S if is_get(s) and not s['escape_tag']], 'd_smoker')))
P('smoker hp at activation, mean %: Italian cruisers', rnd(mean(F(s['r']['smoker_hp_pct_act']) for s in S if is_it_ca(s) and F(s['r']['smoker_hp_pct_act']) is not None)),
  'BB', rnd(mean(F(s['r']['smoker_hp_pct_act']) for s in S if is_bb(s) and F(s['r']['smoker_hp_pct_act']) is not None)),
  'cruiser ordinary', rnd(mean(F(s['r']['smoker_hp_pct_act']) for s in S if s['cls'] == 'cruiser' and s['kind'] != 'exhaust' and F(s['r']['smoker_hp_pct_act']) is not None)),
  'spotted at activation %: It CA', rnd(pctf(lambda s: s['r']['smoker_spotted_act'] == 'true')([s for s in S if is_it_ca(s)])), 'BB', rnd(pctf(lambda s: s['r']['smoker_spotted_act'] == 'true')([s for s in S if is_bb(s)])),
  'cruiser ordinary', rnd(pctf(lambda s: s['r']['smoker_spotted_act'] == 'true')([s for s in S if s['cls'] == 'cruiser' and s['kind'] != 'exhaust'])),
  'DD', rnd(pctf(lambda s: s['r']['smoker_spotted_act'] == 'true')([s for s in S if s['cls'] == 'destroyer'])))
J['B2'] = dict(note='deaths_per_100 = ships that died in or behind the smoke per 100 smokes. smoker_deaths_per_100 = the smoker itself. hurt = died or lost >= 1/3 of estimated health (health is an estimate). '
               'undetected_pct_of_covered_time = batch field (share of the time the smoker was covered by the smoke that it was undetected). undetected_pct_of_smoke_life = that time over the whole life of the smoke (activation to dispersal), computed here.',
               rows=b2, contrasts=b2c)

# ================= B3 long smokes
P('\n===== B3 long smokes')
def lat_of(s):
    size = MAPS[s['map']]['space_size']
    if s['map'] in DIAGONAL: return abs(s['nx'] - s['nz']) / math.sqrt(2) / (size / 2)
    return abs(s['nx']) / (size / 2)
def border_of(s):
    size = MAPS[s['map']]['space_size']
    if s['map'] in DIAGONAL: return min(size / 2 - abs(s['nx']), size / 2 - abs(s['nz'])) / size
    return (size / 2 - abs(s['nx'])) / size
for s in S:
    s['lat'] = lat_of(s); s['border'] = border_of(s)
    s['zone'] = 'centre' if s['lat'] < 1 / 3 else 'map edge' if s['border'] <= 0.10 else 'side lane'
    sm = sum(x['conc'] for x in s['shooters'] if x['is_smoker']); al = sum(x['conc'] for x in s['shooters'])
    s['own_conc'] = sm; s['sh_conc'] = al; s['mate_conc'] = al - sm
    s['radar_broad'] = any('radar' in d['kind'].lower() for x in s['j']['smokees'] if x['how'] != 'none' or x['role'] == 'smoker' for d in x.get('detected_by', []))
def mate_share(ss):
    t = sum(s['sh_conc'] for s in ss); return 100 * sum(s['mate_conc'] for s in ss) / t if t else None
def own_share(ss):
    t = sum(s['sh_conc'] for s in ss); return 100 * sum(s['own_conc'] for s in ss) / t if t else None
P('check shooters conc total vs smoke conc total', round(sum(s['sh_conc'] for s in S)), round(sum(s['conc'] for s in S)))
def landf(f):
    def st(ss):
        v = [s['land_m'] for s in ss if s['land_m'] is not None]
        return 100 * sum(1 for x in v if f(x)) / len(v) if v else None
    return st
P('land_m missing', sum(s['land_m'] is None for s in S), 'of', len(S), '| on long ships', sum(s['land_m'] is None for s in S if s['ship'] in LONG_SHIPS))
B3M = {'conc_per_smoke': meanf('conc'), 'edge_med_m': medf('edge'), 'teammate_share_of_damage_pct': mate_share, 'selfish_pct': pctf(lambda s: s['selfish']), 'smoker_only_label_pct': pctf(lambda s: s['coverage'] == 'selfish'),
       'enemy_radar_spotted_pct': pctf(lambda s: s['radar_on_us'] > 0), 'enemy_radar_broad_pct': pctf(lambda s: s['radar_broad']), 'centre_pct': pctf(lambda s: s['zone'] == 'centre'), 'side_lane_pct': pctf(lambda s: s['zone'] == 'side lane'),
       'map_edge_pct': pctf(lambda s: s['zone'] == 'map edge'), 'land_med_m': medf('land_m'), 'near_land_pct': landf(lambda v: v <= 1000), 'open_water_pct': landf(lambda v: v > 2000),
       'deaths_per_100': lambda ss: rate100(ss, 'deaths')}
B3D = {k: 1 for k in B3M}; B3D.update(conc_per_smoke=0, edge_med_m=0, land_med_m=0)
P('detected_by kinds', dict(C(d['kind'] for s in S for x in s['j']['smokees'] for d in x.get('detected_by', []))), '| narrow and broad', sum(s['radar_on_us'] > 0 for s in S), sum(s['radar_broad'] for s in S), 'narrow but not broad', sum(s['radar_on_us'] > 0 and not s['radar_broad'] for s in S))
P('selfish flag vs coverage label selfish agree', sum(1 for s in S if s['selfish'] == (s['coverage'] == 'selfish')), 'of', len(S))
P('land_m quantiles all DD', [round(q([s['land_m'] for s in S if s['cls'] == 'destroyer' and s['land_m'] is not None], p)) for p in (.1, .25, .5, .75, .9)])
b3 = []
long_all = [s for s in S if s['ship'] in LONG_SHIPS]
refs = [('All four long-smoke ships', long_all), ('REFERENCE cap sitters (Daring, Z-42, Gdańsk, Grozovoi, Shimakaze)', [s for s in S if s['habit'] == 'cap sitters']),
        ('REFERENCE all destroyer smokes', [s for s in S if s['cls'] == 'destroyer'])]
for name, ss in [(sh, of(sh)) for sh in LONG_SHIPS] + refs:
    b3 += grp_rows(name, ss, B3M, B3D)
    P(name, 'n', len(ss), 'zone', dict(C(s['zone'] for s in ss)), 'batch lane', dict(C(s['lane'] for s in ss)), '|', clan_counts(ss) if len(ss) < 600 else '')
print_rows(b3, B3M, B3D)
b3c = []
for b in ('Somers', 'Gearing'):
    for m, st in B3M.items():
        d = dif(st(of('Harugumo')), st(of(b))); c = ship_diff('Harugumo', b, st)
        b3c.append(dict(contrast=f'Harugumo minus {b}', metric=m, diff=rnd(d, B3D[m]), ci=iv(c, B3D[m]), clear=clear(c))); P(f'Harugumo minus {b}', m, fv(d, B3D[m]), fiv(c, B3D[m]))
fa = lambda s: s['ship'] in LONG_SHIPS; fb = lambda s: s['habit'] == 'cap sitters'
for m, st in B3M.items():
    d = dif(st([s for s in S if fa(s)]), st([s for s in S if fb(s)])); c = set_diff(S, fa, fb, st)
    b3c.append(dict(contrast='Long-smoke ships minus cap sitters', metric=m, diff=rnd(d, B3D[m]), ci=iv(c, B3D[m]), clear=clear(c))); P('Long minus cap sitters', m, fv(d, B3D[m]), fiv(c, B3D[m]))
# zone by map for the long ships
for m_ in sorted(MAPS):
    ss = [s for s in long_all if s['map'] == m_]
    if ss: P('  long ships on', m_, len(ss), {z: round(100 * v / len(ss)) for z, v in C(s['zone'] for s in ss).items()})

# ---- Harugumo: farm from own smoke? who spots?
P('\n----- B3 Harugumo own guns and spotting proxies')
for s in S:
    s['own_any'] = s['own_conc'] > 0; s['own_5k'] = s['own_conc'] >= 5000
    al = [c for c in s['cast'] if c['ally'] and not c['is_smoker']]
    dd2 = sorted([c for c in al if c['cls'] == 'destroyer'], key=lambda c: c['dist_m'])
    s['dd2'] = dd2[0] if dd2 else None
    s['dd2_fwd'] = bool(dd2 and any(c['fwd_m'] > 1000 for c in dd2))
    s['dd2_in'] = bool(dd2 and any(c['how'] in ('inside', 'behind') for c in dd2))
    s['our_radar'] = bool(s['off_radar'])
    s['smoker_cov_life'] = s['cov_life']
B3H = {'own_gun_share_pct': own_share, 'own_conc_per_smoke': meanf('own_conc'), 'mate_conc_per_smoke': meanf('mate_conc'), 'smoker_dealt_any_pct': pctf(lambda s: s['own_any']),
       'smoker_dealt_5k_pct': pctf(lambda s: s['own_5k']), 'smoker_time_in_smoke_s_med': medf('sm_secs'), 'smoker_time_share_of_life_pct': meank('cov_life'),
       'stationary_pct': pctf(lambda s: s['movement'] == 'stationary'), 'path_med_m': medf('path_m'),
       'second_dd_recorded_pct': pctf(lambda s: s['dd2'] is not None), 'second_dd_forward_pct': pctf(lambda s: s['dd2_fwd']), 'second_dd_in_smoke_pct': pctf(lambda s: s['dd2_in']),
       'radar_cruiser_inside_pct': pctf(lambda s: s['radar_ca_inside']), 'our_radar_used_from_smoke_pct': pctf(lambda s: s['our_radar']),
       'cruiser_inside_pct': pctf(lambda s: s['cr_inside']), 'smoker_undetected_pct': meank('undetected_pct')}
B3HD = {k: 1 for k in B3H}; B3HD.update(own_conc_per_smoke=0, mate_conc_per_smoke=0, path_med_m=0)
b3h = []
for sh in ('Harugumo', 'Somers', 'Gearing', 'Delny'):
    b3h += grp_rows(sh, of(sh), B3H, B3HD)
print_rows(b3h, B3H, B3HD)
b3hc = []
for b in ('Somers', 'Gearing'):
    for m, st in B3H.items():
        d = dif(st(of('Harugumo')), st(of(b))); c = ship_diff('Harugumo', b, st)
        b3hc.append(dict(contrast=f'Harugumo minus {b}', metric=m, diff=rnd(d, B3HD[m]), ci=iv(c, B3HD[m]), clear=clear(c))); P(f'Harugumo minus {b}', m, fv(d, B3HD[m]), fiv(c, B3HD[m]))
b3split = []
for sh in ('Harugumo', 'Somers', 'Gearing'):
    for lab, f in (('radar cruiser inside', lambda s: s['radar_ca_inside']), ('no radar cruiser inside', lambda s: not s['radar_ca_inside']),
                   ('any cruiser inside', lambda s: s['cr_inside']), ('no cruiser inside', lambda s: not s['cr_inside'])):
        sub = [s for s in of(sh) if f(s)]
        r = dict(ship=sh, case=lab, n=len(sub), clans=len({s['team'] for s in sub}), own_gun_share_pct=rnd(own_share(sub)), own_conc_per_smoke=rnd(mean(s['own_conc'] for s in sub), 0),
                 conc_per_smoke=rnd(mean(s['conc'] for s in sub), 0), smoker_dealt_any_pct=rnd(pctf(lambda s: s['own_any'])(sub)), top6=sum(s['grp'] == 'top' for s in sub))
        b3split.append(r); P(r)
    fa = lambda s, sh=sh: s['ship'] == sh and not s['radar_ca_inside']; fb = lambda s, sh=sh: s['ship'] == sh and s['radar_ca_inside']
    for m in ('own_conc_per_smoke', 'own_gun_share_pct', 'smoker_dealt_any_pct'):
        st = B3H[m]; d = dif(st([s for s in S if fa(s)]), st([s for s in S if fb(s)])); c = set_diff(S, fa, fb, st)
        b3hc.append(dict(contrast=f'{sh}: no radar cruiser inside minus radar cruiser inside', metric=m, diff=rnd(d), ci=iv(c), clear=clear(c))); P(sh, 'no radar CA minus radar CA', m, fv(d, 1), fiv(c, 1))
# who is nearest the targets the smoker itself hit (stand-in for the spotter; same stand-in as round 4 part B)
def nearest_roles(ss, own_only=True):
    cnt = C(); dist = []; nt = 0; npos = 0; dd2_where = C(); dd2_d = []
    for s in ss:
        cast = {c['eid']: c for c in s['cast']}
        allies = [c for c in s['cast'] if c['ally']]
        vict = {}
        for a in s['j']['damage_detail'].get('arrows', []):
            if not a.get('attacker_ally', True): continue
            if own_only and a['attacker'] != s['smoker_eid']: continue
            vict[a['victim']] = vict.get(a['victim'], 0) + a['damage']
        for v, dmg in vict.items():
            nt += 1
            t = cast.get(v)
            if not t or not allies: continue
            npos += 1
            n = min(allies, key=lambda c: math.hypot(c['nx'] - t['nx'], c['nz'] - t['nz']))
            d = math.hypot(n['nx'] - t['nx'], n['nz'] - t['nz']) * WU; dist.append(d)
            role = ('the smoker' if n['is_smoker'] else 'a second destroyer' if n['cls'] == 'destroyer' else 'a radar cruiser inside the smoke' if n['cls'] == 'cruiser' and n['radar'] and n['how'] == 'inside'
                    else 'another ship in or behind the smoke' if n['how'] in ('inside', 'behind', 'line_of_fire') else 'another ship outside the smoke')
            cnt[role] += 1
            if role == 'a second destroyer':
                dd2_where['in or behind the smoke' if n['how'] in ('inside', 'behind') else 'forward of the smoke (1 km+)' if n['fwd_m'] > 1000 else 'level or behind'] += 1; dd2_d.append(n['dist_m'])
    return dict(targets=nt, with_position=npos, nearest=dict(cnt.most_common()), nearest_pct={k: round(100 * v / npos) for k, v in cnt.most_common()} if npos else {},
                median_distance_m=rnd(med(dist), 0) if dist else None, within_8km_pct=rnd(100 * sum(1 for d in dist if d <= 8000) / len(dist)) if dist else None,
                second_dd_where=dict(dd2_where), second_dd_median_dist_from_smoke_m=rnd(med(dd2_d), 0) if dd2_d else None)
spot = {}
for sh in ('Harugumo', 'Somers', 'Gearing'):
    for gname, sub in (('all', of(sh)), ('top6', [s for s in of(sh) if s['grp'] == 'top']), ('rest', [s for s in of(sh) if s['grp'] == 'rest'])):
        r1 = nearest_roles(sub, True); r2 = nearest_roles(sub, False)
        spot[f'{sh} {gname}'] = dict(targets_hit_by_the_smoker=r1, targets_hit_by_anyone_using_the_smoke=r2)
        P(sh, gname, 'OWN-GUN targets:', r1); P(sh, gname, 'ALL targets:', r2)
def near_stat(role, own=True):
    def st(ss):
        r = nearest_roles(ss, own); return 100 * r['nearest'].get(role, 0) / r['with_position'] if r['with_position'] >= 8 else None
    return st
for role in ('a second destroyer', 'the smoker', 'a radar cruiser inside the smoke', 'another ship outside the smoke'):
    for b in ('Somers', 'Gearing'):
        st = near_stat(role); d = dif(st(of('Harugumo')), st(of(b))); c = ship_diff('Harugumo', b, st)
        b3hc.append(dict(contrast=f'Harugumo minus {b}', metric=f'nearest ally to own-gun targets is {role}, %', diff=rnd(d), ci=iv(c), clear=clear(c))); P(f'Harugumo minus {b} nearest={role}', fv(d, 1), fiv(c, 1))
    P('  interval Harugumo', role, fiv(boot_stat(of('Harugumo'), near_stat(role)), 1))
# second destroyer position detail in smokes where the smoker dealt concealed damage
for sh in ('Harugumo', 'Somers', 'Gearing'):
    ss = [s for s in of(sh) if s['own_any']]
    w = [s['dd2'] for s in ss if s['dd2']]
    P(sh, 'smokes where smoker dealt concealed dmg', len(ss), '| 2nd DD recorded', len(w), '| median dist to smoke m', rnd(med(c['dist_m'] for c in w), 0) if w else None,
      '| forward 1km+ %', rnd(100 * sum(c['fwd_m'] > 1000 for c in w) / len(w)) if w else None, '| in/behind smoke %', rnd(100 * sum(c['how'] in ('inside', 'behind') for c in w) / len(w)) if w else None,
      '| 2nd DD ships', dict(C(c['ship'] for c in w).most_common(5)), '| radar CA inside %', rnd(pctf(lambda s: s['radar_ca_inside'])(ss)),
      '| allied positions recorded per smoke (median)', med(sum(1 for c in s['cast'] if c['ally']) for s in ss))
    P('   own conc when radar CA inside vs not', rnd(mean(s['own_conc'] for s in of(sh) if s['radar_ca_inside']), 0), sum(s['radar_ca_inside'] for s in of(sh)), rnd(mean(s['own_conc'] for s in of(sh) if not s['radar_ca_inside']), 0),
      '| when 2nd DD forward vs not', rnd(mean(s['own_conc'] for s in of(sh) if s['dd2_fwd']), 0), sum(s['dd2_fwd'] for s in of(sh)), rnd(mean(s['own_conc'] for s in of(sh) if not s['dd2_fwd']), 0))
    P('   by kind own-gun: guns vs torp total', rnd(mean(s['guns'] for s in of(sh)), 0), rnd(mean(s['torp'] for s in of(sh)), 0), '| clans', clan_counts(of(sh)))
J['B3'] = dict(note='teammate_share_of_damage_pct = share of concealed damage dealt by ships other than the smoker (pooled). selfish_pct = batch selfish flag. enemy_radar_spotted_pct = radar_on_us > 0 (narrow: a ship inside gained the radar flag). enemy_radar_broad_pct = any covered ship (smoker included) whose detected_by list has kind radar (broad). '
               'Zones (team-normalized): centre = within the middle third of the map width (offset from the line joining the spawns under 1/3 of the half width); map edge = within 10% of the map width of the west or east border '
               '(any border on Okinawa, outside the centre band); side lane = the rest. near_land = within 1 km of land, open_water = over 2 km.',
               rows=b3, contrasts=b3c, harugumo=dict(rows=b3h, contrasts=b3hc, by_cruiser_inside=b3split, nearest_ally_to_targets=spot,
               note='Spotting cannot be attributed from the batch. Stand-ins: allied positions at the moment the smoke was fully laid (cast); nearest allied ship to each enemy the smoker damaged.'))

# ================= B4 hybrids
P('\n===== B4 hybrids')
HY = ('Grozovoi', 'Shimakaze', 'Daring', 'Gdańsk', 'Z-42', 'Somers', 'Harugumo')
for s in S:
    s['parked'] = s['movement'] == 'stationary'
    s['line'] = s['path_m'] is not None and s['path_m'] >= 1000
    s['between'] = s['path_m'] is not None and not s['parked'] and not s['line']
    s['lp'] = math.log10(max(s['path_m'], 30)) if s['path_m'] is not None else None
def centroid_spread(ss, min_n=5):
    """Mean distance (km) of a smoke from the ship's own centroid on that map; maps with min_n+ smokes."""
    d = []
    for m_, sub in by(ss, 'map').items():
        if len(sub) < min_n: continue
        cx, cz = mean(s['nx'] for s in sub), mean(s['nz'] for s in sub)
        d += [math.hypot(s['nx'] - cx, s['nz'] - cz) * WU / 1000 for s in sub]
    return mean(d) if len(d) >= 8 else None
def iqr(k, filt=None):
    def st(ss):
        v = [s[k] for s in ss if s[k] is not None and (filt is None or filt(s))]
        return q(v, .75) - q(v, .25) if len(v) >= 8 else None
    return st
def entropy(ss, key='pp'):
    c = C(s[key] for s in ss); n = len(ss)
    return -sum(v / n * math.log2(v / n) for v in c.values()) if n else None
def top_share(ss, key='pp'):
    c = C(s[key] for s in ss); return 100 * c.most_common(1)[0][1] / len(ss) if ss else None
def cells80(ss):
    c = sorted(C((s['map'], s['ncell']) for s in ss).values(), reverse=True); need = 0.8 * len(ss); acc = 0
    for i, v in enumerate(c):
        acc += v
        if acc >= need: return i + 1
def matched(ss, stat, n=30, reps=400):
    """Mean of stat over random subsamples of n smokes, so ships with different n can be compared."""
    if len(ss) < n: return None
    return mean(stat(random.sample(ss, n)) for _ in range(reps))
def pctk(f):
    def st(ss):
        v = [s for s in ss if s['path_m'] is not None]
        return 100 * sum(1 for s in v if f(s)) / len(v) if v else None
    return st
P('path length missing by ship', {sh: sum(s['path_m'] is None for s in of(sh)) for sh in HY})
B4M = {'spread_km': centroid_spread, 'edge_iqr_m': iqr('edge'), 'edge_iqr_no_mrA_m': iqr('edge', lambda s: not s['mrA']), 'edge_med_m': medf('edge'),
       'top_purpose_pct': top_share, 'purpose_entropy_bits': entropy, 'parked_pct': pctk(lambda s: s['parked']), 'between_pct': pctk(lambda s: s['between']), 'line_1km_pct': pctk(lambda s: s['line']),
       'path_med_m': medf('path_m'), 'path_iqr_m': iqr('path_m')}
B4D = {k: 1 for k in B4M}; B4D.update(edge_iqr_m=0, edge_iqr_no_mrA_m=0, edge_med_m=0, path_med_m=0, path_iqr_m=0, purpose_entropy_bits=2, spread_km=2)
b4 = []
for sh in HY: b4 += grp_rows(sh, of(sh), B4M, B4D)
print_rows(b4, B4M, B4D)
b4c = []
for a in ('Grozovoi', 'Shimakaze'):
    for b in ('Daring', 'Gdańsk'):
        for m, st in B4M.items():
            d = dif(st(of(a)), st(of(b))); c = ship_diff(a, b, st)
            b4c.append(dict(contrast=f'{a} minus {b}', metric=m, diff=rnd(d, B4D[m]), ci=iv(c, B4D[m]), clear=clear(c))); P(f'{a} minus {b}', m, fv(d, B4D[m]), fiv(c, B4D[m]))
for m, st in B4M.items():
    d = dif(st(of('Gdańsk')), st(of('Daring'))); c = ship_diff('Gdańsk', 'Daring', st)
    b4c.append(dict(contrast='Gdańsk minus Daring', metric=m, diff=rnd(d, B4D[m]), ci=iv(c, B4D[m]), clear=clear(c))); P('Gdańsk minus Daring', m, fv(d, B4D[m]), fiv(c, B4D[m]))
# matched-n (30 smokes) versions so n does not drive the count-type measures
b4m = []
for sh in HY:
    ss = of(sh)
    r = dict(ship=sh, n=len(ss), cells_for_80pct_at_n30=rnd(matched(ss, cells80)), distinct_cells_at_n30=rnd(matched(ss, lambda x: len({(s['map'], s['ncell']) for s in x}))),
             purpose_entropy_bits_at_n30=rnd(matched(ss, entropy), 2), distinct_primary_purposes_at_n30=rnd(matched(ss, lambda x: len({s['pp'] for s in x}))),
             distinct_tags_per_smoke=rnd(mean(len(set(s['tags'])) for s in ss), 2), maps=dict(C(s['map'] for s in ss).most_common()), primary_purposes={k: round(100 * v / len(ss)) for k, v in C(s['pp'] for s in ss).most_common()},
             movement={k: round(100 * v / len(ss)) for k, v in C(s['movement'] for s in ss).most_common()})
    # same-map spread: per map with 8+ smokes
    r['spread_by_map_km'] = {m_: [len(sub), rnd(centroid_spread(sub, 8), 2)] for m_, sub in by(ss, 'map').items() if len(sub) >= 8}
    b4m.append(r); P(r)
# map-mix check: Daring and Gdansk spread on Hotspot only, and reweighted
for m_ in ('Hotspot', 'Sea of Fortune', 'Loop', 'Mountain Range'):
    P('same-map spread km', m_, {sh: (len([s for s in of(sh) if s['map'] == m_]), rnd(centroid_spread([s for s in of(sh) if s['map'] == m_], 5), 2)) for sh in ('Grozovoi', 'Shimakaze', 'Daring', 'Gdańsk')})

# two-modes test on log10(path length)
def moments(v):
    n = len(v); m = sum(v) / n; s2 = sum((x - m) ** 2 for x in v) / n; sd = math.sqrt(s2)
    g1 = sum((x - m) ** 3 for x in v) / n / sd ** 3; g2 = sum((x - m) ** 4 for x in v) / n / s2 ** 2 - 3
    return n, m, sd, g1, g2
def bimod_coef(v):
    n, m, sd, g1, g2 = moments(v)
    G1 = g1 * math.sqrt(n * (n - 1)) / (n - 2); G2 = (n - 1) / ((n - 2) * (n - 3)) * ((n + 1) * g2 + 6)
    return (G1 ** 2 + 1) / (G2 + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))
def npdf(x, m, sd): return math.exp(-0.5 * ((x - m) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
def gmm2(v, iters=300):
    """Two-Gaussian mixture by EM (several starts). Returns (loglik, w, m1, s1, m2, s2)."""
    best = None; vs = sorted(v); n = len(v)
    for cut in (.25, .4, .5, .6, .75):
        k = max(2, min(n - 2, int(cut * n))); a, b = vs[:k], vs[k:]
        w, m1, m2 = k / n, mean(a), mean(b); s1 = max(.05, statistics.pstdev(a)); s2 = max(.05, statistics.pstdev(b))
        for _ in range(iters):
            r = []
            for x in v:
                p1 = w * npdf(x, m1, s1); p2 = (1 - w) * npdf(x, m2, s2); r.append(p1 / (p1 + p2) if p1 + p2 > 0 else .5)
            n1 = sum(r); n2 = n - n1
            if n1 < 2 or n2 < 2: break
            w = n1 / n; m1 = sum(ri * x for ri, x in zip(r, v)) / n1; m2 = sum((1 - ri) * x for ri, x in zip(r, v)) / n2
            s1 = max(.05, math.sqrt(sum(ri * (x - m1) ** 2 for ri, x in zip(r, v)) / n1)); s2 = max(.05, math.sqrt(sum((1 - ri) * (x - m2) ** 2 for ri, x in zip(r, v)) / n2))
        ll = sum(math.log(max(1e-300, w * npdf(x, m1, s1) + (1 - w) * npdf(x, m2, s2))) for x in v)
        if best is None or ll > best[0]: best = (ll, w, m1, s1, m2, s2)
    return best
def two_modes(v):
    n, m, sd, g1, g2 = moments(v)
    ll1 = sum(math.log(max(1e-300, npdf(x, m, sd))) for x in v); bic1 = -2 * ll1 + 2 * math.log(n)
    ll2, w, m1, s1, m2, s2 = gmm2(v); bic2 = -2 * ll2 + 5 * math.log(n)
    D = math.sqrt(2) * abs(m1 - m2) / math.sqrt(s1 ** 2 + s2 ** 2)
    # is there a dip between the two component means? density at the midpoint vs the lower of the two peaks
    f = lambda x: w * npdf(x, m1, s1) + (1 - w) * npdf(x, m2, s2)
    lo, hi = sorted((m1, m2)); grid = [lo + (hi - lo) * i / 50 for i in range(51)]; valley = min(f(x) for x in grid); peak = min(f(lo), f(hi))
    return dict(n=n, bimodality_coefficient=rnd(bimod_coef(v), 2), bic_one_minus_two=rnd(bic1 - bic2, 1), ashman_d=rnd(D, 2), weight_low=rnd(min(w, 1 - w) if False else (w if m1 < m2 else 1 - w), 2),
                mode_low_m=round(10 ** min(m1, m2)), mode_high_m=round(10 ** max(m1, m2)), valley_to_peak=rnd(valley / peak if peak else None, 2))
b4t = []
for sh in HY:
    v = [s['lp'] for s in of(sh) if s['lp'] is not None]
    r = dict(ship=sh, **two_modes(v))
    ss = of(sh)
    r['path_bands_pct'] = {'under 500 m': rnd(pctk(lambda s: s['path_m'] < 500)(ss)), '500 m to 1 km': rnd(pctk(lambda s: 500 <= s['path_m'] < 1000)(ss)),
                           '1 to 2 km': rnd(pctk(lambda s: 1000 <= s['path_m'] < 2000)(ss)), 'over 2 km': rnd(pctk(lambda s: s['path_m'] >= 2000)(ss))}
    r['path_bands_n'] = [sum(1 for s in ss if s['path_m'] is not None and a <= s['path_m'] < b) for a, b in ((0, 500), (500, 1000), (1000, 2000), (2000, 1e9))]
    b4t.append(r); P(r)
# reference: is a verdict of "two modes" what random Daring / Gdansk samples of the same size give?
for a, n in (('Grozovoi', 30), ('Shimakaze', 58)):
    va = [s['lp'] for s in of(a) if s['lp'] is not None]; ta = two_modes(va)
    for b in ('Daring', 'Gdańsk', 'Somers'):
        vb = [s['lp'] for s in of(b) if s['lp'] is not None]; ge = 0; ge2 = 0; R = 200
        for _ in range(R):
            t = two_modes(random.sample(vb, len(va))); ge += t['bimodality_coefficient'] >= ta['bimodality_coefficient']; ge2 += t['bic_one_minus_two'] >= ta['bic_one_minus_two']
        P(f'{a} vs random {b} samples of n={len(va)}: share with bimodality coefficient at least as high', round(100 * ge / R), '% | BIC gain at least as high', round(100 * ge2 / R), '%')
        b4t.append(dict(ship=a, reference=b, n=len(va), ref_samples_bimodality_at_least_as_high_pct=round(100 * ge / R), ref_samples_bic_gain_at_least_as_high_pct=round(100 * ge2 / R)))
# per player
b4p = []
for sh in HY:
    pl = by(of(sh), 'player'); rows = []; p3 = []
    for p, sub in pl.items():
        if len(sub) >= 3: p3.append((sum(s['parked'] for s in sub) >= 1, sum(s['line'] for s in sub) >= 1))
        if len(sub) < 6: continue
        rows.append(dict(clan=sub[0]['team'], n=len(sub), parked=sum(s['parked'] for s in sub), line_1km=sum(s['line'] for s in sub), between=sum((not s['parked']) and (not s['line']) for s in sub),
                         inside_cap=sum(s['inside'] for s in sub), maps=len({s['map'] for s in sub}), games=len({s['game'] for s in sub})))
    both1 = sum(1 for r in rows if r['parked'] >= 1 and r['line_1km'] >= 1); both2 = sum(1 for r in rows if r['parked'] >= 2 and r['line_1km'] >= 2)
    bothq = sum(1 for r in rows if r['parked'] / r['n'] >= .25 and r['line_1km'] / r['n'] >= .25)
    # same game: player-games with 3+ smokes that have both
    pg = [sub for sub in by(of(sh), lambda s: (s['player'], s['game'])).values() if len(sub) >= 3]
    pgb = sum(1 for sub in pg if any(s['parked'] for s in sub) and any(s['line'] for s in sub))
    r = dict(ship=sh, players_total=len(pl), players_6plus=len(rows), both_at_least_1_each=both1, both_at_least_2_each=both2, both_at_least_quarter_each=bothq,
             players_3plus=len(p3), players_3plus_with_both=sum(1 for a, b in p3 if a and b), player_games_3plus=len(pg), player_games_with_both=pgb, players=sorted(rows, key=lambda r: -r['n']))
    b4p.append(r); P({k: v for k, v in r.items() if k != 'players'});
    for x in r['players']: P('    ', x)
# clan concentration for the hybrids
for sh in ('Grozovoi', 'Shimakaze'):
    ss = of(sh); P(sh, clan_counts(ss), '| players', C(s['player'].split('_KOTS')[0][:14] + '/' + s['team'] for s in ss).most_common(6))
    big = C(s['team'] for s in ss).most_common(1)[0][0]; rest_ = [s for s in ss if s['team'] != big]
    P('   bands without', big, [sum(1 for s in rest_ if s['path_m'] is not None and a <= s['path_m'] < b) for a, b in ((0, 500), (500, 1000), (1000, 2000), (2000, 1e9))])
    P('   without', big, 'n', len(rest_), 'parked%', rnd(pctk(lambda s: s['parked'])(rest_)), 'line%', rnd(pctk(lambda s: s['line'])(rest_)), 'spread km', rnd(centroid_spread(rest_), 2), 'edge IQR', rnd(iqr('edge')(rest_), 0),
      'entropy', rnd(entropy(rest_), 2))
J['B4'] = dict(note='spread_km = mean distance of a smoke from the ship\'s own centroid on that map (maps with 5+ smokes). edge_iqr = interquartile range of the distance to the cap edge. '
               'parked = movement label stationary (laid over under 500 m). line_1km = laid over 1 km or more. purpose entropy in bits over the primary purpose (higher = more varied). '
               'two-modes test is on log10 of the length laid: bimodality coefficient over 0.555 hints at two modes; bic_one_minus_two above 0 favours two bell curves over one; ashman_d over 2 = cleanly separated; '
               'valley_to_peak under about 0.7 = a visible dip between the two.',
               rows=b4, contrasts=b4c, matched_n=b4m, two_modes=b4t, players=b4p)

json.dump(J, open(os.path.join(HERE_B, 'ships.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(HERE_B, 'out.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
