# B3 per shot: who is near, and what lights, the targets a long-smoke destroyer hits from its own smoke.
# Run: python -I -X utf8 b3_shots.py  -> b3.json, b3_out.txt
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3lib import *
random.seed(531)
OUT = []
def P(*a):
    line = ' '.join(str(x) for x in a); OUT.append(line); print(line)
SHIPS = ('Harugumo', 'Somers', 'Gearing', 'Delny')
RUN = {(r['key'], r['primary_replay']): r for r in runs()}
_ev = {}
def events(run):
    if run['dir'] not in _ev:
        rows = []
        for r in csv.DictReader(open(os.path.join(GAMES_DIR, run['dir'], 'damage_events.csv'), encoding='utf-8')):
            if not r['attacker']: continue
            cred = {}
            for part in r['credited'].split(';'):
                if ':' in part:
                    a, b = part.split(':'); cred[a] = float(b)
            rows.append(dict(att=int(r['attacker']), vic=int(r['victim']), amt=float(r['amount']), kind=r['kind'], t=float(r['fire_s']) - run['start'] if r['fire_s'] else None,
                             td=float(r['damage_s']) - run['start'], src=r['fire_source'], adet=r['attacker_detected_at_fire'], ins=r['in_smokes'].split(';') if r['in_smokes'] else [],
                             beh=r['behind_smokes'].split(';') if r['behind_smokes'] else [], cred=cred))
        _ev[run['dir']] = by(rows, 'att')
    return _ev[run['dir']]

NEAR = ['a ship outside the smoke', 'a second destroyer', 'the smoker itself', 'another ship in or behind the smoke', 'the radar cruiser inside the smoke']
SPOT = ['radar-lit from inside this smoke', 'radar-lit from elsewhere', 'detected, no radar: nearest ally a ship outside the smoke', 'detected, no radar: nearest ally a second destroyer',
        'detected, no radar: nearest ally the smoker itself', 'detected, no radar: nearest ally another ship in or behind the smoke', 'detected, no radar: nearest ally the radar cruiser inside the smoke',
        'not detected at the shot', 'detection unknown']
def crosses(s, a, b):
    """True when the straight line from raw point a to raw point b passes through the smoke."""
    ax, az = a; bx, bz = b; dx, dz = bx - ax, bz - az; L2 = dx * dx + dz * dz
    rr = s['radius_m'] / WU
    for px, pz in s['path']:
        f = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (pz - az) * dz) / L2))
        if math.hypot(ax + f * dx - px, az + f * dz - pz) <= rr: return True
    return False
def role_of(s, g, tr, p, tp, t, how_batch=None):
    """Role of allied ship tr (at raw p) relative to smoke s and target position tp."""
    ro = G[s['game']]['roster'].get(tr.eid, {})
    cls = (ro.get('ship_class') or '').lower()
    inside = in_smoke(s, p) if how_batch is None else how_batch.get(tr.eid) == 'inside'
    behind = (not inside and smoke_dist_m(s, p) <= 3000 + s['radius_m'] and crosses(s, p, tp)) if how_batch is None else how_batch.get(tr.eid) in ('behind', 'line_of_fire')
    if tr.eid == s['smoker_eid']: return NEAR[2]
    if cls == 'destroyer': return NEAR[1]
    if cls == 'cruiser' and ro.get('radar_m') and inside: return NEAR[4]
    if inside or behind: return NEAR[3]
    return NEAR[0]
def dd2_at(s, g, t, tp=None):
    """Nearest allied destroyer other than the smoker at elapsed t: dict(dist_m to the smoke, fwd_m, where, at_cap, ship) or None."""
    best = None
    for tr in g.ships(s['team'], alive_at=t):
        if tr.eid == s['smoker_eid'] or ship_cls(s['game'], tr.eid) != 'destroyer': continue
        p = tr.pos(t)
        if not p: continue
        d = smoke_dist_m(s, p)
        if best is None or d < best['dist_m']:
            nx, nz = norm(s['map'], s['side'], p[0], p[1])
            fwd = forward(s['map'], nx - s['nx'], nz - s['nz'])
            ins = d <= s['radius_m']
            beh = (not ins) and tp is not None and d <= 3000 + s['radius_m'] and crosses(s, p, tp)
            at_cap = any(math.hypot(c['x'] - p[0], c['z'] - p[1]) <= c['r'] for c in G[s['game']]['caps'])
            best = dict(dist_m=d, fwd_m=fwd, where='in or behind the smoke' if ins or beh else 'forward of the smoke (1 km+)' if fwd > 1000 else 'level or behind', at_cap=at_cap, ship=tr.ship, eid=tr.eid)
    return best
def shot_features(s, g, vic, t, how_batch=None):
    tgt = g.tracks.get(vic)
    tp = tgt.pos(t) if tgt else None
    if tp is None: return None
    allies = [(tr, tr.pos(t)) for tr in g.ships(s['team'], alive_at=t)]
    allies = [(tr, p) for tr, p in allies if p]
    if not allies: return None
    ntr, np_ = min(allies, key=lambda a: math.hypot(a[1][0] - tp[0], a[1][1] - tp[1]))
    f = dict(near=role_of(s, g, ntr, np_, tp, t, how_batch), near_d=dist_m(np_, tp), near_ship=ntr.ship)
    i = tgt.idx(t); det = tgt.det[i] if i is not None else None
    if g.one_sided and not tgt.own: det = None
    f['det'] = det
    lit = [r for r in g.lit('radar', target=vic) if r['lit_start_elapsed_s'] - 1 <= t <= r['lit_end_elapsed_s'] + 1]
    src = None; f['radar_amb'] = any(r['ambiguous'] for r in lit)
    for r in lit:
        if r['row'] != 'lit' or r['team'] != s['team']:
            src = src or 'unknown'; continue
        p = g.pos(r['entity_id'], t)
        ins = bool(p and in_smoke(s, p))
        if ins: src = 'inside'; f['radar_src_cls'] = ship_cls(s['game'], r['entity_id']); f['radar_src_ship'] = r['ship'].replace('\xa0', ' '); f['radar_batch_in'] = int(s['id']) in r['source_in_smoke']
        elif src != 'inside': src = 'elsewhere'; f['radar_src_cls'] = ship_cls(s['game'], r['entity_id']); f['radar_src_ship'] = r['ship'].replace('\xa0', ' '); f['radar_src_smoker'] = r['entity_id'] == s['smoker_eid']
    f['radar'] = src
    f['hydro'] = any(r['lit_start_elapsed_s'] - 1 <= t <= r['lit_end_elapsed_s'] + 1 for r in g.lit('hydro', target=vic))
    if src == 'inside': f['spot'] = SPOT[0]
    elif src: f['spot'] = SPOT[1]
    elif det is True: f['spot'] = 'detected, no radar: nearest ally ' + f['near']
    elif det is False: f['spot'] = SPOT[7]
    else: f['spot'] = SPOT[8]
    # allied ships outside this smoke that are within the target's own listed detection range
    dm = G[s['game']]['roster'].get(vic, {}).get('detection_m')
    cand = [(tr, p) for tr, p in allies if not in_smoke(s, p) and dm and dist_m(p, tp) <= dm]
    if not dm: f['cand'] = None
    elif not cand: f['cand'] = "no ally outside the smoke within the target's detection range"
    else:
        ctr = min(cand, key=lambda a: dist_m(a[1], tp))[0]
        f['cand'] = 'the smoker (outside its smoke)' if ctr.eid == s['smoker_eid'] else 'a second destroyer' if ship_cls(s['game'], ctr.eid) == 'destroyer' else 'another ship'
    d2 = dd2_at(s, g, t, tp); f['dd2'] = d2
    sp = g.pos(s['smoker_eid'], t); f['smoker_in'] = bool(sp and in_smoke(s, sp)); f['tgt_d'] = dist_m(sp, tp) if sp else None
    f['tgt_cls'] = ship_cls(s['game'], vic)
    return f

REC = []      # one record per credited damage event of the smoker
SM = []       # one record per smoke
skipped = C()
for s in S:
    if s['ship'] not in SHIPS: continue
    g = TL(s['game']); run = RUN[(s['game'], s['j']['primary_replay'])]
    ev = [e for e in events(run).get(s['smoker_eid'], []) if (s['id'] in e['cred'] or s['id'] in e['ins']) and e['kind'] in ('shell', 'fire', 'torpedo', 'airstrike') and e['t'] is not None]
    own = sum(x['conc'] for x in s['shooters'] if x['is_smoker']); own_all = sum(x['dmg'] for x in s['shooters'] if x['is_smoker'])
    sm = dict(team=s['team'], grp=s['grp'], ship=s['ship'], id=s['id'], game=s['game'], one_sided=g.one_sided, own_conc=own, own_all=own_all, n_ev=len(ev), s=s, recs=[])
    for e in ev:
        w = e['amt'] * e['cred'].get(s['id'], 1.0)
        f = shot_features(s, g, e['vic'], e['t'])
        if f is None: skipped['no position'] += 1; continue
        r = dict(team=s['team'], grp=s['grp'], ship=s['ship'], sid=s['id'], game=s['game'], vic=e['vic'], t=e['t'], kind=e['kind'], w=w, credited=s['id'] in e['cred'], adet=e['adet'],
                 shot=(e['kind'] in ('shell', 'torpedo', 'airstrike')), key=(s['game'], s['id'], e['vic'], round(e['t'], 1)), one_sided=g.one_sided, **f)
        REC.append(r); sm['recs'].append(r)
    # life of the smoke: second destroyer presence, sampled every 2 s
    t0, t1 = s['e0'], end_of(s); n = 0; cnt = C(); t = t0
    while t <= t1:
        n += 1; dds = []
        for tr in g.ships(s['team'], alive_at=t):
            if tr.eid == s['smoker_eid'] or ship_cls(s['game'], tr.eid) != 'destroyer': continue
            p = tr.pos(t)
            if not p: continue
            nx, nz = norm(s['map'], s['side'], p[0], p[1])
            dds.append((smoke_dist_m(s, p), forward(s['map'], nx - s['nx'], nz - s['nz'])))
        if dds: cnt['alive'] += 1
        if any(d <= 3000 for d, _ in dds): cnt['3km'] += 1
        if any(d <= 5000 for d, _ in dds): cnt['5km'] += 1
        if any(f > 1000 for _, f in dds): cnt['fwd'] += 1
        if any(f > 1000 and d <= 5000 for d, f in dds): cnt['fwd5'] += 1
        if any(d <= s['radius_m'] for d, _ in dds): cnt['in'] += 1
        t += 2
    for k in ('alive', '3km', '5km', 'fwd', 'fwd5', 'in'): sm['life_' + k] = 100 * cnt[k] / n if n else None
    # snapshot at the fully-laid moment from the tracks (same moment as the round 5 cast)
    tc = s['ecap'] if s['ecap'] is not None else s['e0']
    d2 = dd2_at(s, g, tc); sm['cap_dd2'] = d2 is not None
    fw = False
    for tr in g.ships(s['team'], alive_at=tc):
        if tr.eid == s['smoker_eid'] or ship_cls(s['game'], tr.eid) != 'destroyer' or not tr.pos(tc): continue
        nx, nz = norm(s['map'], s['side'], *tr.pos(tc))
        if forward(s['map'], nx - s['nx'], nz - s['nz']) > 1000: fw = True
    sm['cap_dd2_fwd'] = fw
    sm['old_dd2'] = any(c['ally'] and not c['is_smoker'] and c['cls'] == 'destroyer' for c in s['cast'])
    sm['old_dd2_fwd'] = any(c['ally'] and not c['is_smoker'] and c['cls'] == 'destroyer' and c['fwd_m'] > 1000 for c in s['cast'])
    SM.append(sm)
P('smokes', dict(C(m['ship'] for m in SM)), '| events', len(REC), dict(C(r['ship'] for r in REC)), '| skipped', dict(skipped))
P('events credited', sum(r['credited'] for r in REC), 'in smoke but not credited', sum(not r['credited'] for r in REC), '| one-sided game events', sum(r['one_sided'] for r in REC))
P('kinds', dict(C(r['kind'] for r in REC)))
# check 1: credited event damage against the smoke records
CHK1 = {}
for sh in SHIPS:
    a = sum(r['w'] for r in REC if r['ship'] == sh and r['credited']); b = sum(m['own_all'] for m in SM if m['ship'] == sh); c_ = sum(m['own_conc'] for m in SM if m['ship'] == sh)
    cc_ = sum(r['w'] for r in REC if r['ship'] == sh and r['credited'] and r['adet'] == 'false')
    CHK1[sh] = dict(events_damage=round(a), smoke_records_smoker_damage=round(b), smoke_records_smoker_concealed=round(c_), events_damage_attacker_not_detected=round(cc_))
    P(f'check {sh}:', CHK1[sh])
N_UNCRED = sum(not r['credited'] for r in REC)
REC = [r for r in REC if r['credited']]
for m in SM: m['recs'] = [r for r in m['recs'] if r['credited']]

# ---------- aggregation
def shots(recs):
    """One record per distinct firing moment and target (shell, torpedo or airstrike rows)."""
    seen = {}
    for r in recs:
        if r['shot'] and r['key'] not in seen: seen[r['key']] = r
    return list(seen.values())
def share(recs, pred, weight=False):
    if weight:
        t = sum(r['w'] for r in recs); return 100 * sum(r['w'] for r in recs if pred(r)) / t if t else None
    return 100 * sum(1 for r in recs if pred(r)) / len(recs) if recs else None
def per_smoke(sms, pred):
    """Mean over smokes (those with own-gun damage) of the share of the smoke's own-gun damage matching pred."""
    v = []
    for m in sms:
        t = sum(r['w'] for r in m['recs'])
        if t > 0: v.append(100 * sum(r['w'] for r in m['recs'] if pred(r)) / t)
    return mean(v) if v else None
J = dict(note='B3 per shot. A shot = one distinct firing moment and target among the smoker\'s shell, torpedo and airstrike events credited to its own smoke. Damage = every credited event (shells, fires, torpedoes) times its credited share. '
              'Per smoke = mean over smokes of each smoke\'s own-gun damage share. Positions from tracks at the firing moment (2 s samples, interpolated). Detection = the target\'s own track flag. Radar = the radar log lit spans.')
J['check_damage'] = CHK1; J['events_in_smoke_not_credited_dropped'] = N_UNCRED
SHOTS = shots(REC)
P('distinct shots', dict(C(r['ship'] for r in SHOTS)))
base = {}
for sh in SHIPS:
    rs = [r for r in REC if r['ship'] == sh]; ss = [r for r in SHOTS if r['ship'] == sh]; sms = [m for m in SM if m['ship'] == sh]; sms_d = [m for m in sms if m['recs']]
    base[sh] = dict(smokes=len(sms), smokes_with_own_damage=len(sms_d), clans=len({m['team'] for m in sms}), clans_with_own_damage=len({m['team'] for m in sms_d}), events=len(rs), shots=len(ss), damage=round(sum(r['w'] for r in rs)),
                    targets=len({(r['game'], r['sid'], r['vic']) for r in rs}), clans_txt=clans_of(sms_d),
                    top6_smokes_with_own_damage=sum(m['grp'] == 'top' for m in sms_d), rest_smokes_with_own_damage=sum(m['grp'] == 'rest' for m in sms_d),
                    top_smoke_share_of_damage_pct=r1(100 * max((sum(r['w'] for r in m['recs']) for m in sms_d), default=0) / sum(r['w'] for r in rs)) if rs else None,
                    one_sided_shots=sum(r['one_sided'] for r in ss))
    P(sh, base[sh])
J['base'] = base
def table(field, cats, ships=SHIPS):
    out = {}
    for sh in ships:
        rs = [r for r in REC if r['ship'] == sh]; ss = [r for r in SHOTS if r['ship'] == sh]; sms = [m for m in SM if m['ship'] == sh]
        out[sh] = {}
        for c in cats:
            pr = lambda r, c=c: r[field] == c
            row = dict(shots_n=sum(1 for r in ss if pr(r)), shots_pct=r1(share(ss, pr)), damage_pct=r1(share(rs, pr, True)), per_smoke_pct=r1(per_smoke(sms, pr)))
            if sh != 'Delny' and len(ss) >= 8:
                row['shots_ci'] = iv(bstat(ss, lambda v: share(v, pr))); row['damage_ci'] = iv(bstat(rs, lambda v: share(v, pr, True)))
                row['per_smoke_ci'] = iv(bstat([m for m in sms if m['recs']], lambda v: per_smoke(v, pr)))
            out[sh][c] = row
    return out
def contrasts(field, cats):
    out = []
    for c in cats:
        pr = lambda r, c=c: r[field] == c
        for b in ('Somers', 'Gearing'):
            fa = lambda r: r['ship'] == 'Harugumo'; fb = lambda r, b=b: r['ship'] == b
            for nm, pool, st in (('shots', SHOTS, lambda v: share(v, pr)), ('damage', REC, lambda v: share(v, pr, True)), ('per smoke', [m for m in SM if m['recs']], lambda v: per_smoke(v, pr))):
                a_ = st([r for r in pool if fa(r)]); b_ = st([r for r in pool if fb(r)])
                ci_ = set_diff(pool, fa, fb, st)
                out.append(dict(what=c, vs=b, weight=nm, diff=r1(a_ - b_) if a_ is not None and b_ is not None else None, ci=iv(ci_), clear=clear(ci_)))
    return out
for r in REC:
    r['det3'] = 'radar-lit' if r['radar'] else 'detected, not radar-lit' if r['det'] is True else 'not detected' if r['det'] is False else 'unknown'
    r['rad3'] = {'inside': 'radar ship inside this smoke', 'elsewhere': 'radar ship elsewhere', 'unknown': 'radar, source not attributed', None: 'no radar on the target'}[r['radar']]
DET3 = ['radar-lit', 'detected, not radar-lit', 'not detected', 'unknown']; RAD3 = ['radar ship inside this smoke', 'radar ship elsewhere', 'radar, source not attributed', 'no radar on the target']
CAND = ['a second destroyer', 'another ship', 'the smoker (outside its smoke)', "no ally outside the smoke within the target's detection range"]
J['cats'] = dict(nearest=NEAR, spotter=SPOT, detected=DET3, radar=RAD3, candidates=CAND)
for nm, field, cats in (('nearest', 'near', NEAR), ('spotter', 'spot', SPOT), ('detected', 'det3', DET3), ('radar', 'rad3', RAD3), ('candidates', 'cand', CAND)):
    J[nm] = table(field, cats); J[nm + '_contrasts'] = contrasts(field, cats)
    P('\n---', nm)
    P(md_table(['class'] + [f'{sh} shots / dmg / per smoke' for sh in SHIPS], [[c] + [f"{J[nm][sh][c]['shots_n']} ({J[nm][sh][c]['shots_pct']}% {J[nm][sh][c].get('shots_ci')}) / {J[nm][sh][c]['damage_pct']}% / {J[nm][sh][c]['per_smoke_pct']}%" for sh in SHIPS] for c in cats]))
    for x in J[nm + '_contrasts']:
        if x['clear']: P('   clear:', x)
# radar detail
rad = {}
for sh in SHIPS:
    ss = [r for r in SHOTS if r['ship'] == sh and r['radar']]; al = [r for r in SHOTS if r['ship'] == sh]
    rad[sh] = dict(radar_lit_shots=len(ss), from_inside=sum(r['radar'] == 'inside' for r in ss), inside_cruiser=sum(r['radar'] == 'inside' and r.get('radar_src_cls') == 'cruiser' for r in ss),
                   elsewhere=sum(r['radar'] == 'elsewhere' for r in ss), elsewhere_is_smoker=sum(bool(r.get('radar_src_smoker')) for r in ss), unattributed=sum(r['radar'] == 'unknown' for r in ss), ambiguous=sum(r['radar_amb'] for r in ss),
                   inside_batch_flag_agrees=sum(bool(r.get('radar_batch_in')) for r in ss if r['radar'] == 'inside'),
                   source_ships=dict(C(r.get('radar_src_ship') for r in ss if r.get('radar_src_ship')).most_common(6)), hydro_lit_shots=sum(r['hydro'] for r in al),
                   smoker_inside_at_shot_pct=r1(share(al, lambda r: r['smoker_in'])), target_class=dict(C(r['tgt_cls'] for r in al)),
                   median_range_to_target_m=r1(med(r['tgt_d'] for r in al if r['tgt_d']), 0), median_nearest_ally_m=r1(med(r['near_d'] for r in al), 0),
                   nearest_within_8km_pct=r1(share(al, lambda r: r['near_d'] <= 8000)))
    P(sh, rad[sh])
J['radar_detail'] = rad
# what the "not detected at the shot" damage is made of
nd = {}
for sh in SHIPS:
    rs = [r for r in REC if r['ship'] == sh and r['det'] is False and not r['radar']]; tot = sum(r['w'] for r in rs)
    nd[sh] = dict(events=len(rs), damage=round(tot), by_kind_pct={k: r1(100 * sum(r['w'] for r in rs if r['kind'] == k) / tot) for k in sorted({r['kind'] for r in rs})} if tot else {},
                  shots_by_kind=dict(C(r['kind'] for r in SHOTS if r['ship'] == sh and r['det'] is False and not r['radar'])))
    P(sh, 'not detected at the shot:', nd[sh])
J['not_detected_detail'] = nd
# does a radar cruiser sitting inside light the target? shots from smokes with a radar cruiser inside (batch field)
rc = {}
for sh in SHIPS:
    ids = {(m['game'], m['id']) for m in SM if m['ship'] == sh and m['s']['radar_ca_inside']}
    inn = lambda r: (r['game'], r['sid']) in ids
    ss = [r for r in SHOTS if r['ship'] == sh and inn(r)]; so = [r for r in SHOTS if r['ship'] == sh and not inn(r)]
    rc[sh] = dict(shots_with_radar_cruiser_inside=len(ss), smokes_with=len({(r['game'], r['sid']) for r in ss}),
                  of_those_radar_lit_from_inside_n=sum(r['radar'] == 'inside' for r in ss), of_those_radar_lit_from_inside_pct=r1(share(ss, lambda r: r['radar'] == 'inside')) if len(ss) >= 8 else None,
                  of_those_radar_lit_any_pct=r1(share(ss, lambda r: bool(r['radar']))) if len(ss) >= 8 else None,
                  of_those_nearest_is_radar_cruiser_pct=r1(share(ss, lambda r: r['near'] == NEAR[4])) if len(ss) >= 8 else None,
                  shots_without=len(so), smokes_without=len({(r['game'], r['sid']) for r in so}), without_radar_lit_any_pct=r1(share(so, lambda r: bool(r['radar']))) if len(so) >= 8 else None,
                  own_damage_share_from_smokes_with_radar_cruiser_pct=r1(share([r for r in REC if r['ship'] == sh], inn, True)))
    P(sh, 'radar cruiser inside split', rc[sh])
J['radar_cruiser_inside_split'] = rc
# Top 6 vs Rest, Harugumo
tr = {}
hs = [r for r in SHOTS if r['ship'] == 'Harugumo']; hr = [r for r in REC if r['ship'] == 'Harugumo']
tr['n'] = dict(top6_shots=sum(r['grp'] == 'top' for r in hs), rest_shots=sum(r['grp'] == 'rest' for r in hs), top6_smokes=len({(r['game'], r['sid']) for r in hs if r['grp'] == 'top'}), rest_smokes=len({(r['game'], r['sid']) for r in hs if r['grp'] == 'rest'}),
               top6_clans=len({r['team'] for r in hs if r['grp'] == 'top'}), rest_clans=len({r['team'] for r in hs if r['grp'] == 'rest'}))
rows = []
hsm_d = [m for m in SM if m['ship'] == 'Harugumo' and m['recs']]
for field, cats in (('near', NEAR), ('det3', DET3), ('rad3', RAD3)):
    for c in cats:
        pr = lambda r, c=c: r[field] == c
        st = lambda v: share(v, pr); a = st([r for r in hs if r['grp'] == 'top']); b = st([r for r in hs if r['grp'] == 'rest']); ci_ = bdiff_groups(hs, st)
        stw = lambda v: share(v, pr, True); aw = stw([r for r in hr if r['grp'] == 'top']); bw = stw([r for r in hr if r['grp'] == 'rest'])
        stp = lambda v: per_smoke(v, pr); ap = stp([m for m in hsm_d if m['grp'] == 'top']); bp = stp([m for m in hsm_d if m['grp'] == 'rest']); cip = bdiff_groups(hsm_d, stp)
        rows.append(dict(what=c, top6_pct=r1(a), rest_pct=r1(b), diff=r1(a - b), ci=iv(ci_), clear=clear(ci_), top6_damage_pct=r1(aw), rest_damage_pct=r1(bw),
                         top6_per_smoke_pct=r1(ap), rest_per_smoke_pct=r1(bp), per_smoke_diff=r1(ap - bp), per_smoke_ci=iv(cip), per_smoke_clear=clear(cip)))
tr['rows'] = rows; J['harugumo_top6_vs_rest'] = tr
P('\nHarugumo Top 6 vs Rest', tr['n'])
for x in rows: P('  ', x)
# ---------- second destroyer
P('\n--- second destroyer')
D2 = {}
LK = ('alive', '3km', '5km', 'fwd', 'fwd5', 'in')
for sh in SHIPS:
    ss = [r for r in SHOTS if r['ship'] == sh]; sms = [m for m in SM if m['ship'] == sh]
    w = [r['dd2'] for r in ss if r['dd2']]
    d = dict(shots=len(ss), with_second_dd_alive=len(w), with_second_dd_pct=r1(100 * len(w) / len(ss)) if ss else None,
             median_dist_to_smoke_m=r1(med(x['dist_m'] for x in w), 0) if w else None, median_forward_m=r1(med(x['fwd_m'] for x in w), 0) if w else None,
             where_pct={k: r1(100 * sum(x['where'] == k for x in w) / len(w)) for k in ('in or behind the smoke', 'forward of the smoke (1 km+)', 'level or behind')} if w else None,
             within_3km_pct=r1(100 * sum(x['dist_m'] <= 3000 for x in w) / len(ss)) if ss else None, within_5km_pct=r1(100 * sum(x['dist_m'] <= 5000 for x in w) / len(ss)) if ss else None,
             forward_1km_pct_of_shots=r1(100 * sum(x['fwd_m'] > 1000 for x in w) / len(ss)) if ss else None, at_a_cap_pct_of_shots=r1(100 * sum(x['at_cap'] for x in w) / len(ss)) if ss else None,
             in_or_behind_pct_of_shots=r1(100 * sum(x['where'] == 'in or behind the smoke' for x in w) / len(ss)) if ss else None,
             ships=dict(C(x['ship'] for x in w).most_common(6)))
    for k in LK:
        st = lambda v, k=k: mean(m['life_' + k] for m in v if m['life_' + k] is not None)
        d['life_' + k + '_pct'] = r1(st(sms)); d['life_' + k + '_ci'] = iv(bstat(sms, st)) if len(sms) >= 8 and sh != 'Delny' else None
        sd = [m for m in sms if m['recs']]
        d['life_' + k + '_pct_smokes_with_own_damage'] = r1(st(sd)) if len(sd) >= 8 else None
    d['at_capture_tracks_dd2_pct'] = r1(pct(sms, lambda m: m['cap_dd2'])); d['at_capture_round5_dd2_pct'] = r1(pct(sms, lambda m: m['old_dd2']))
    d['at_capture_tracks_dd2_fwd_pct'] = r1(pct(sms, lambda m: m['cap_dd2_fwd'])); d['at_capture_round5_dd2_fwd_pct'] = r1(pct(sms, lambda m: m['old_dd2_fwd']))
    d['at_capture_agree'] = sum(m['cap_dd2'] == m['old_dd2'] for m in sms); d['at_capture_fwd_agree'] = sum(m['cap_dd2_fwd'] == m['old_dd2_fwd'] for m in sms); d['smokes'] = len(sms)
    D2[sh] = d; P(sh, d)
d2c = []
for b in ('Somers', 'Gearing'):
    fa = lambda r: r['ship'] == 'Harugumo'; fb = lambda r, b=b: r['ship'] == b
    for k in LK:
        st = lambda v, k=k: mean(m['life_' + k] for m in v if m['life_' + k] is not None)
        ci_ = set_diff(SM, fa, fb, st); d2c.append(dict(what='life_' + k, vs=b, diff=r1(st([m for m in SM if fa(m)]) - st([m for m in SM if fb(m)])), ci=iv(ci_), clear=clear(ci_)))
    for nm, pr in (('shot: second destroyer within 3 km of the smoke', lambda r: bool(r['dd2']) and r['dd2']['dist_m'] <= 3000), ('shot: second destroyer within 5 km of the smoke', lambda r: bool(r['dd2']) and r['dd2']['dist_m'] <= 5000),
                   ('shot: second destroyer 1 km+ forward', lambda r: bool(r['dd2']) and r['dd2']['fwd_m'] > 1000), ('shot: second destroyer at a cap', lambda r: bool(r['dd2']) and r['dd2']['at_cap']),
                   ('shot: second destroyer in or behind the smoke', lambda r: bool(r['dd2']) and r['dd2']['where'] == 'in or behind the smoke')):
        st = lambda v, pr=pr: share(v, pr); ci_ = set_diff(SHOTS, fa, fb, st)
        d2c.append(dict(what=nm, vs=b, harugumo=r1(st([r for r in SHOTS if fa(r)])), other=r1(st([r for r in SHOTS if fb(r)])), diff=r1(st([r for r in SHOTS if fa(r)]) - st([r for r in SHOTS if fb(r)])), ci=iv(ci_), clear=clear(ci_)))
for x in d2c: P('  ', x)
d2g = []
hsm = [m for m in SM if m['ship'] == 'Harugumo']
for k in ('alive', '3km', '5km', 'fwd'):
    st = lambda v, k=k: mean(m['life_' + k] for m in v if m['life_' + k] is not None)
    ci_ = bdiff_groups(hsm, st); a = st([m for m in hsm if m['grp'] == 'top']); b = st([m for m in hsm if m['grp'] == 'rest'])
    d2g.append(dict(what='life_' + k, top6=r1(a), rest=r1(b), n_top6=sum(m['grp'] == 'top' for m in hsm), n_rest=sum(m['grp'] == 'rest' for m in hsm), diff=r1(a - b), ci=iv(ci_), clear=clear(ci_)))
    P('  Harugumo top6 vs rest', d2g[-1])
J['second_destroyer'] = dict(by_ship=D2, contrasts=d2c, harugumo_top6_vs_rest=d2g)

# ---------- check 2: the round 5 snapshot question redone with the tracks at the same moment, same targets
P('\n--- check: round 5 snapshot (cast) against tracks at the fully-laid moment, same targets')
chk = {}
for sh in ('Harugumo', 'Somers', 'Gearing'):
    old = C(); new = C(); newgeo = C(); n = 0; same = 0; samegeo = 0; nold = 0; nvict = 0
    for m in [m for m in SM if m['ship'] == sh]:
        s = m['s']; g = TL(s['game']); cast = {c['eid']: c for c in s['cast']}; allies = [c for c in s['cast'] if c['ally']]
        how = {x['entity_id']: x['how'] for x in s['j']['smokees']}
        vict = {a['victim'] for a in s['j']['damage_detail'].get('arrows', []) if a.get('attacker_ally', True) and a['attacker'] == s['smoker_eid']}
        tc = s['ecap'] if s['ecap'] is not None else s['e0']
        for v in sorted(vict):
            nvict += 1
            t = cast.get(v); ro = None
            if t and allies:
                nn = min(allies, key=lambda c: math.hypot(c['nx'] - t['nx'], c['nz'] - t['nz']))
                ro = (NEAR[2] if nn['is_smoker'] else NEAR[1] if nn['cls'] == 'destroyer' else NEAR[4] if nn['cls'] == 'cruiser' and nn['radar'] and nn['how'] == 'inside'
                      else NEAR[3] if nn['how'] in ('inside', 'behind', 'line_of_fire') else NEAR[0])
                old[ro] += 1; nold += 1
            f = shot_features(s, g, v, tc, how_batch=how); f2 = shot_features(s, g, v, tc)
            if f: new[f['near']] += 1; newgeo[f2['near']] += 1; n += 1
            if f and ro: same += f['near'] == ro; samegeo += f2['near'] == ro
    chk[sh] = dict(targets=nvict, round5_targets_with_position=nold, round5={k: old[k] for k in NEAR}, tracks_targets_with_position=n, tracks_same_rule={k: new[k] for k in NEAR}, tracks_geometric_rule={k: newgeo[k] for k in NEAR},
                   same_role_same_rule=same, same_role_geometric_rule=samegeo)
    P(sh, chk[sh])
J['check_snapshot'] = chk
# check 3: a second way for the radar headline: straight from the radar log's own source_in_smoke flag
alt = {}
for sh in SHIPS:
    ss = [r for r in SHOTS if r['ship'] == sh]; k = 0
    for r in ss:
        g = TL(r['game'])
        if any(x['row'] == 'lit' and int(r['sid']) in x['source_in_smoke'] and x['lit_start_elapsed_s'] - 1 <= r['t'] <= x['lit_end_elapsed_s'] + 1 for x in g.lit('radar', target=r['vic'])): k += 1
    alt[sh] = dict(shots=len(ss), radar_lit_from_inside_geometry=sum(r['radar'] == 'inside' for r in ss), radar_lit_source_in_smoke_flag=k)
    P('check radar inside two ways', sh, alt[sh])
J['check_radar_inside'] = alt
# examples: biggest Harugumo own-gun smokes
ex = []
for m in sorted([m for m in SM if m['ship'] == 'Harugumo' and m['recs']], key=lambda m: -sum(r['w'] for r in m['recs']))[:8]:
    s = m['s']; t = sum(r['w'] for r in m['recs'])
    bs = {c: sum(r['w'] for r in m['recs'] if r['spot'] == c) for c in SPOT}
    ex.append(dict(link=s['link'], team=s['team'], map=s['map'], time=clock(s['e0']), own_damage=round(t), shots=len(shots(m['recs'])), radar_cruiser_inside=s['radar_ca_inside'],
                   by_spotter={k: round(100 * v / t) for k, v in sorted(bs.items(), key=lambda x: -x[1]) if v > 0}))
    P('  ex', ex[-1])
J['examples'] = ex
json.dump(J, open(os.path.join(HERE_N3, 'b3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
open(os.path.join(HERE_N3, 'b3_out.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
