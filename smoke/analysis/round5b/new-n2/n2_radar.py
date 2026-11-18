# Round 5b, worker n2: A2 radar deaths with the full radar log. Frame: destroyer smokes, as in round 5 A2.
# Run: python -I -X utf8 n2_radar.py      Writes out-radar.json, out-radar.md and figure n2-radar-deaths.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n2lib import *
random.seed(31)
PR = build_pairs(); add_radar_flags()
L = []
def P(*a):
    t = ' '.join(str(x) for x in a); L.append(t); print(t)
J = {}
tbin = lambda el: '0-5 min' if el < 300 else '5-10 min' if el < 600 else '10-15 min' if el < 900 else '15-20 min'
TB = ['0-5 min', '5-10 min', '10-15 min', '15-20 min']
who_of = lambda cls, is_smoker: 'smoking destroyer' if is_smoker and cls == 'destroyer' else 'sheltering cruiser' if cls == 'cruiser' and not is_smoker else 'other ship'

# old readings (round 5 fields)
for s in S:
    kinds = C(x['kind'] for sm_ in s['j']['smokees'] if sm_['how'] != 'none' for x in sm_.get('detected_by', []))
    s['old_broad'] = kinds['radar'] > 0; s['old_strict'] = s['radar_on_us'] > 0
    smk = {x['entity_id']: x for x in s['j']['smokees']}
    for d in s['dead']:
        raw = next(x for x in s['j']['smoke_deaths'] if x['entity_id'] == d['eid']); t = raw['death']['seconds']
        d['old_broad'] = any(x['kind'] == 'radar' and t - 40 <= x['seconds'] <= t + 1 for x in smk.get(d['eid'], {}).get('detections', []))

def radar_at_death(s, eid, td, win):
    """Radar log for ship eid in the `win` seconds before its death at td. None when it was not lit."""
    g = TL(s['game']); rows = lit_rows(s, eid, td - win, td + 0.5)
    if not rows: return None
    att = [r for r in rows if r['row'] == 'lit']
    best = max(att or rows, key=lambda r: (r['lit_start_elapsed_s'], -(r['target_distance_m'] or 0)))   # the latest span; of several sources, the nearest
    # how long it had been lit: walk back through spans that touch each other (gap of 3 s or less)
    allr = sorted(g.lit('radar', target=eid), key=lambda r: r['lit_start_elapsed_s'] or 0)
    end_last = max((r['lit_end_elapsed_s'] or r['lit_start_elapsed_s']) for r in rows); start = min(r['lit_start_elapsed_s'] for r in rows if (r['lit_end_elapsed_s'] or r['lit_start_elapsed_s']) >= end_last - 0.01)
    changed = True
    while changed:
        changed = False
        for r in allr:
            a, b = r['lit_start_elapsed_s'], (r['lit_end_elapsed_s'] or r['lit_start_elapsed_s'])
            if a is not None and a < start and b >= start - 3: start = a; changed = True
    ro = G[s['game']]['roster'].get(best['entity_id'], {}) if best['entity_id'] else {}
    sid = int(s['id'])
    return dict(src=(best['ship'] or '?').replace('\xa0', ' ') if best['row'] == 'lit' else None, src_cls=(ro.get('ship_class') or '').lower() or None, range_m=best['range_m'] if best['row'] == 'lit' else None,
                dist_m=best['target_distance_m'] if best['row'] == 'lit' else None, share=(best['target_distance_m'] / best['range_m']) if best['row'] == 'lit' and best['range_m'] and best['target_distance_m'] is not None else None,
                ambiguous=any(r['ambiguous'] for r in rows), unattributed=not att, src_in_smoke=bool(best['source_in_smoke']) if best['row'] == 'lit' else None,
                target_in_this_smoke=any(sid in r['target_in_smoke'] for r in rows), target_in_any_smoke=any(r['target_in_smoke'] for r in rows),
                lit_for_s=max(0.0, min(td, end_last) - start), lit_at_death=end_last >= td - 2 * STEP, gap_to_death_s=max(0.0, td - end_last), n_sources=len({r['entity_id'] for r in att}))

# ---- deaths
BD = []
for s in DD:
    g = TL(s['game'])
    for d in s['dead']:
        tr = g.tracks.get(d['eid']); td = tr.death_t()
        BD.append(dict(s=s, eid=d['eid'], who=who_of(d['cls'], d['is_smoker']), ship=d['ship'], td=td, strict=d['radar_lit'], broad=d['old_broad'], r40=radar_at_death(s, d['eid'], td, 40), r20=radar_at_death(s, d['eid'], td, 20), in_batch=True))
RISK = [p for p in PR if p['s']['cls'] == 'destroyer' and p['how'] in ('smoker', 'inside', 'behind') and p['own']]
TD = []
for p in RISK:
    if not p['died_win']: continue
    s = p['s']
    TD.append(dict(s=s, eid=p['eid'], who=who_of(p['cls'], p['how'] == 'smoker'), ship=p['ship'], td=p['td'], strict=None, broad=None, r40=radar_at_death(s, p['eid'], p['td'], 40), r20=radar_at_death(s, p['eid'], p['td'], 20), in_batch=p['died']))

def summary(D, label):
    R = [d for d in D if d['r40']]; R20 = [d for d in D if d['r20']]
    out = dict(label=label, deaths=len(D), lit40=len(R), lit40_pct=r1(100 * len(R) / len(D)), lit20=len(R20), lit20_pct=r1(100 * len(R20) / len(D)),
               distinct_ships=len({(d['s']['game'], d['eid']) for d in R}),
               top6=sum(d['s']['grp'] == 'top' for d in R), rest=sum(d['s']['grp'] == 'rest' for d in R), deaths_top6=sum(d['s']['grp'] == 'top' for d in D), deaths_rest=sum(d['s']['grp'] == 'rest' for d in D),
               top6_20=sum(d['s']['grp'] == 'top' for d in R20), rest_20=sum(d['s']['grp'] == 'rest' for d in R20),
               who=dict(C(d['who'] for d in R).most_common()), who_20=dict(C(d['who'] for d in R20).most_common()), who_all=dict(C(d['who'] for d in D).most_common()),
               by_map=dict(C(d['s']['map'] for d in R).most_common()), deaths_by_map=dict(C(d['s']['map'] for d in D).most_common()),
               by_map_cap=dict(C(d['s']['map'] + ' ' + d['s']['near_ncap'] for d in R).most_common(10)),
               by_time=dict(C(tbin(d['s']['e0']) for d in R)), by_state=dict(C(d['s']['state'] for d in R)), deaths_by_state=dict(C(d['s']['state'] for d in D)),
               clans=clan_dict([d['s'] for d in R]), clans_text=clan_counts([d['s'] for d in R]))
    A = [d for d in R if d['r40']['src']]
    out['attributed'] = len(A); out['unattributed'] = len(R) - len(A)
    out['src_class'] = dict(C(d['r40']['src_cls'] for d in A).most_common()); out['src_ship'] = dict(C(d['r40']['src'] for d in A).most_common())
    dist = sorted(d['r40']['dist_m'] for d in A if d['r40']['dist_m'] is not None); sh = [d['r40']['share'] for d in A if d['r40']['share'] is not None]
    out['dist_km'] = dict(n=len(dist), min=r1(dist[0] / 1000), q25=r1(q(dist, .25) / 1000), median=r1(med(dist) / 1000), q75=r1(q(dist, .75) / 1000), max=r1(dist[-1] / 1000))
    out['dist_bands'] = dict(C('under 6 km' if x < 6000 else '6-8 km' if x < 8000 else '8-10 km' if x < 10000 else '10 km+' for x in dist))
    out['share_of_range'] = dict(n=len(sh), median=r1(100 * med(sh)), q25=r1(100 * q(sh, .25)), q75=r1(100 * q(sh, .75)), beyond_80=sum(x > .8 for x in sh), under_60=sum(x < .6 for x in sh))
    out['by_src_class'] = {c: dict(n=len(v), median_km=r1(med(x['r40']['dist_m'] for x in v) / 1000), median_share=r1(100 * med(x['r40']['share'] for x in v))) for c, v in by(A, lambda d: d['r40']['src_cls']).items()}
    out['ambiguous'] = sum(d['r40']['ambiguous'] for d in R); out['ambiguous_pct'] = r1(100 * out['ambiguous'] / len(R))
    out['src_in_smoke'] = sum(bool(d['r40']['src_in_smoke']) for d in A); out['src_in_smoke_pct'] = r1(100 * out['src_in_smoke'] / len(A)) if A else None
    out['target_in_this_smoke'] = sum(d['r40']['target_in_this_smoke'] for d in R); out['target_in_any_smoke'] = sum(d['r40']['target_in_any_smoke'] for d in R)
    lf = [d['r40']['lit_for_s'] for d in R]
    out['lit_for_s'] = dict(median=r1(med(lf)), q25=r1(q(lf, .25)), q75=r1(q(lf, .75)), max=r1(max(lf)), under_10=sum(x < 10 for x in lf), over_20=sum(x >= 20 for x in lf))
    out['lit_at_death'] = sum(d['r40']['lit_at_death'] for d in R); out['median_gap_to_death_s'] = r1(med(d['r40']['gap_to_death_s'] for d in R if not d['r40']['lit_at_death'])) if any(not d['r40']['lit_at_death'] for d in R) else None
    return out
def show(o):
    P(f'\n### {o["label"]}')
    P(f'Radar-lit in the last 40 s: {o["lit40"]} of {o["deaths"]} ({o["lit40_pct"]}%); in the last 20 s: {o["lit20"]} ({o["lit20_pct"]}%). Distinct ships (40 s): {o["distinct_ships"]}.')
    P(f'Top 6 {o["top6"]} of {o["deaths_top6"]} deaths, Rest {o["rest"]} of {o["deaths_rest"]} (last 20 s: {o["top6_20"]} / {o["rest_20"]}).')
    P(f'Who died (40 s): {o["who"]} out of {o["who_all"]}; (20 s): {o["who_20"]}.')
    P(f'By map: {o["by_map"]} (all deaths by map: {o["deaths_by_map"]}). By map and nearest cap: {o["by_map_cap"]}.')
    P(f'By time of the smoke: {o["by_time"]}. By score at activation: {o["by_state"]} (all deaths: {o["deaths_by_state"]}).')
    P(f'Radar ship named for {o["attributed"]} of {o["lit40"]} ({o["unattributed"]} lit with no enemy radar in range in the log). Class: {o["src_class"]}. Ships: {o["src_ship"]}.')
    d = o['dist_km']; sh = o['share_of_range']
    P(f'Distance from the radar ship (n {d["n"]}): median {d["median"]} km (quarter marks {d["q25"]} and {d["q75"]}; range {d["min"]} to {d["max"]}); bands {o["dist_bands"]}. As a share of that radar\'s range: median {sh["median"]}% (quarter marks {sh["q25"]}% and {sh["q75"]}%); {sh["beyond_80"]} of {sh["n"]} beyond 80%, {sh["under_60"]} under 60%. By radar class: {o["by_src_class"]}.')
    P(f'Ambiguous (more than one enemy radar had the ship in range): {o["ambiguous"]} of {o["lit40"]} ({o["ambiguous_pct"]}%). Radar ship itself inside a smoke (a radar play from smoke): {o["src_in_smoke"]} of {o["attributed"]} ({o["src_in_smoke_pct"]}%). '
      f'The log places the dying ship inside this smoke while lit: {o["target_in_this_smoke"]}; inside any smoke: {o["target_in_any_smoke"]}.')
    lf = o['lit_for_s']
    P(f'How long it had been lit when it died (or when the radar ended): median {lf["median"]} s (quarter marks {lf["q25"]} and {lf["q75"]}, longest {lf["max"]}); under 10 s: {lf["under_10"]}, 20 s or more: {lf["over_20"]}. Still lit at the moment of death: {o["lit_at_death"]} of {o["lit40"]}'
      + (f'; for the others the radar had ended a median {o["median_gap_to_death_s"]} s before.' if o['median_gap_to_death_s'] is not None else '.'))
    P(f'Clans: {o["clans_text"]}')
P('## Radar deaths from the radar log')
J['batch'] = summary(BD, 'Batch death list in destroyer smokes (the 124 deaths round 5 used)'); show(J['batch'])
J['track'] = summary(TD, 'All track deaths of ships at risk in destroyer smokes (smoker, inside, behind; activation to 20 s after dispersal)'); show(J['track'])
# death by death against the two round 5 readings
st = [d for d in BD if d['strict']]; br = [d for d in BD if d['broad']]; lg = [d for d in BD if d['r40']]
J['vs_round5_deaths'] = dict(strict=len(st), broad=len(br), log40=len(lg), strict_and_log=sum(bool(d['r40']) for d in st), strict_not_log=sum(not d['r40'] for d in st), log_not_strict=sum(not d['strict'] for d in lg),
                             broad_and_log=sum(bool(d['r40']) for d in br), broad_not_log=sum(not d['r40'] for d in br), log_not_broad=sum(not d['broad'] for d in lg),
                             log_in_this_smoke=sum(d['r40']['target_in_this_smoke'] for d in lg), log_not_broad_in_smoke=sum(d['r40']['target_in_this_smoke'] for d in lg if not d['broad']))
v = J['vs_round5_deaths']
P(f'\nDeath by death against round 5 (124 deaths): strict {v["strict"]}, broad {v["broad"]}, radar log (last 40 s) {v["log40"]}. Strict and log {v["strict_and_log"]}, strict only {v["strict_not_log"]}, log only {v["log_not_strict"]}. '
  f'Broad and log {v["broad_and_log"]}, broad only {v["broad_not_log"]}, log only {v["log_not_broad"]}. Of the {v["log40"]} log deaths the log places {v["log_in_this_smoke"]} inside this smoke while lit; the rest were lit outside it (behind it, or after leaving).')
# same radar distances for the strict 19: old field against the log
chk = [(d['s']['dead'], d) for d in st if d['r40'] and d['r40']['dist_m'] is not None]
old_d = []
for d in st:
    od = next(x for x in d['s']['dead'] if x['eid'] == d['eid'])
    if od['radar_src'] and d['r40'] and d['r40']['dist_m'] is not None: old_d.append((od['radar_src']['dist_m'], d['r40']['dist_m'], od['radar_src']['ship'] == d['r40']['src']))
J['strict_check'] = dict(n=len(old_d), same_radar_ship=sum(x[2] for x in old_d), median_old_km=r1(med(x[0] for x in old_d) / 1000), median_log_km=r1(med(x[1] for x in old_d) / 1000), median_abs_diff_m=round(med(abs(x[0] - x[1]) for x in old_d)))
c = J['strict_check']
P(f'Check on the strict deaths that are also in the log (n {c["n"]}): same radar ship named in {c["same_radar_ship"]}; median distance {c["median_old_km"]} km (round 5 field) against {c["median_log_km"]} km (log); median difference {c["median_abs_diff_m"]} m.')

# ---- rates per 100 destroyer smokes
P('\n## Rates per 100 destroyer smokes')
for s in DD:
    s['track_deaths'] = 0
for p in RISK:
    if p['died_win']: p['s']['track_deaths'] += 1
def stat_of(key):
    return lambda ss: 100 * sum(s[key] for s in ss) / len(ss) if len(ss) >= MIN_N else None
D100 = stat_of('deaths'); T100 = stat_of('track_deaths')
def rate_row(label, ss, st=D100, key='deaths'):
    lo, hi = boot_stat(ss, st) if st(ss) is not None else (None, None)
    t, r = st(TOPS(ss)), st(RESTS(ss)); g = boot_diff(ss, st) if t is not None and r is not None else (None, None)
    return dict(label=label, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)), deaths=sum(s[key] for s in ss), per_100=r1(st(ss)), ci=[r1(lo), r1(hi)], top6=r1(t), rest=r1(r), gap_ci=[r1(g[0]), r1(g[1])], clear=bool(g[0] is not None and g[0] * g[1] > 0))
def diff_row(a, b, st=D100):
    ia = {id(s) for s in a}; u = a + b
    f = lambda ss: (None if st([s for s in ss if id(s) in ia]) is None or st([s for s in ss if id(s) not in ia]) is None else st([s for s in ss if id(s) in ia]) - st([s for s in ss if id(s) not in ia]))
    v_ = f(u); lo, hi = boot_stat(u, f) if v_ is not None else (None, None)
    return dict(diff=r1(v_), ci=[r1(lo), r1(hi)], clear=bool(lo is not None and lo * hi > 0))
def pci(c): return '-' if c[0] is None else f'{c[0]:.1f} to {c[1]:.1f}'
def table(rows):
    P(md_table(['destroyer smokes', 'n (Top 6 / Rest)', 'deaths', 'per 100 [95%]', 'Top 6', 'Rest', 'Top 6 minus Rest'],
               [[r['label'], f'{r["n"]} ({r["n_top6"]} / {r["n_rest"]}){" " + sm(r["n"]) if sm(r["n"]) else ""}', r['deaths'], f'{fv(r["per_100"])} [{pci(r["ci"])}]', fv(r['top6']), fv(r['rest']), fci(r['gap_ci'])] for r in rows]))
READ = [('radar log: a covered ship radar-lit while the smoke stood', 'rad_any'), ('radar log: lit while placed inside this smoke', 'rad_in'), ('round 5 strict', 'old_strict'), ('round 5 broad', 'old_broad')]
J['rates'] = {}; J['rate_diffs'] = {}
for lab, k in READ:
    a = [s for s in DD if s[k]]; b = [s for s in DD if not s[k]]
    rows = [rate_row(f'{lab}: with', a), rate_row(f'{lab}: without', b)]
    for st_ in STATES: rows.append(rate_row(f'{lab}: with, {st_}', [s for s in a if s['state'] == st_])); rows.append(rate_row(f'{lab}: without, {st_}', [s for s in b if s['state'] == st_]))
    J['rates'][k] = rows; J['rate_diffs'][k] = dict(all=diff_row(a, b), **{st_: diff_row([s for s in a if s['state'] == st_], [s for s in b if s['state'] == st_]) for st_ in STATES})
    P(f'\n{lab} (deaths = batch list, as in round 5):'); table(rows)
    P('With minus without: ' + '; '.join(f'{kk}: {vv["diff"]:+.1f} ({fci(vv["ci"])})' for kk, vv in J['rate_diffs'][k].items()))
# same with track deaths for the log reading
a = [s for s in DD if s['rad_any']]; b = [s for s in DD if not s['rad_any']]
rows = [rate_row('radar log: with (track deaths)', a, T100, 'track_deaths'), rate_row('radar log: without (track deaths)', b, T100, 'track_deaths')]
for st_ in STATES: rows.append(rate_row(f'radar log: with, {st_} (track deaths)', [s for s in a if s['state'] == st_], T100, 'track_deaths')); rows.append(rate_row(f'radar log: without, {st_} (track deaths)', [s for s in b if s['state'] == st_], T100, 'track_deaths'))
J['rates']['rad_any_track'] = rows; J['rate_diffs']['rad_any_track'] = dict(all=diff_row(a, b, T100), **{st_: diff_row([s for s in a if s['state'] == st_], [s for s in b if s['state'] == st_], T100) for st_ in STATES})
P('\nRadar log reading with track deaths (every ship at risk that died between activation and 20 s after dispersal):'); table(rows)
P('With minus without: ' + '; '.join(f'{kk}: {vv["diff"]:+.1f} ({fci(vv["ci"])})' for kk, vv in J['rate_diffs']['rad_any_track'].items()))
sh = lambda k: (r1(pct(TOPS(DD), lambda s: s[k])), r1(pct(RESTS(DD), lambda s: s[k])), boot_diff(DD, lambda ss: pct(ss, lambda s: s[k]) if ss else None))
J['reach'] = {}
for lab, k in READ:
    t, r, g = sh(k); J['reach'][k] = dict(top6=t, rest=r, gap_ci=[r1(g[0]), r1(g[1])])
P('\nShare of destroyer smokes radar reached, Top 6 / Rest: ' + '; '.join(f'{lab}: {J["reach"][k]["top6"]}% / {J["reach"][k]["rest"]}% ({fci(J["reach"][k]["gap_ci"])})' for lab, k in READ))
# smoke by smoke
P('\nSmoke by smoke (1,074 destroyer smokes):')
rows = []; J['smoke_by_smoke'] = []
for (la, ka), (lb, kb) in ((READ[2], READ[1]), (READ[2], READ[0]), (READ[3], READ[0]), (READ[3], READ[1])):
    c = C((s[ka], s[kb]) for s in DD)
    J['smoke_by_smoke'].append(dict(old=la, new=lb, old_n=c[(True, True)] + c[(True, False)], new_n=c[(True, True)] + c[(False, True)], both=c[(True, True)], old_only=c[(True, False)], new_only=c[(False, True)], neither=c[(False, False)]))
    rows.append([la, lb, c[(True, True)] + c[(True, False)], c[(True, True)] + c[(False, True)], c[(True, True)], c[(False, True)], c[(True, False)]])
P(md_table(['round 5 reading', 'radar log reading', 'round 5 smokes', 'log smokes', 'in both', 'missed by round 5 (log only)', 'over-counted by round 5 (not in the log)'], rows))
only = [s for s in DD if s['rad_any'] and not s['old_broad']]
J['log_only'] = rate_row('in the log, not in round 5 broad', only)
P(f'Smokes the log adds over round 5 broad ({len(only)}): {J["log_only"]["per_100"]} deaths per 100 ({J["log_only"]["deaths"]} deaths). These are ships lit while out of cover (before entering, after leaving, or a ship firing over the smoke).')
# calm smokes
P('\n## Calm smokes')
calm_old = [s for s in DD if s['state'] != 'behind 50+' and not s['old_strict'] and not s['old_broad']]
calm_new = [s for s in DD if s['state'] != 'behind 50+' and not s['rad_any']]
calm_in = [s for s in DD if s['state'] != 'behind 50+' and not s['rad_in']]
J['calm'] = dict(old=rate_row('round 5 definition (not 50+ behind, no strict or broad radar)', calm_old), new=rate_row('radar log (not 50+ behind, no covered ship radar-lit while the smoke stood)', calm_new),
                 new_in=rate_row('not 50+ behind, no ship lit inside this smoke (log)', calm_in), new_track=rate_row('radar log definition, track deaths', calm_new, T100, 'track_deaths'), old_track=rate_row('round 5 definition, track deaths', calm_old, T100, 'track_deaths'),
                 other_new=dict(n=len(DD) - len(calm_new), deaths=sum(s['deaths'] for s in DD) - sum(s['deaths'] for s in calm_new)), total_deaths=sum(s['deaths'] for s in DD), total_track_deaths=sum(s['track_deaths'] for s in DD))
table([J['calm']['old'], J['calm']['new'], J['calm']['new_in']]); table([J['calm']['old_track'], J['calm']['new_track']])
P(f'All destroyer smokes: {len(DD)}, {J["calm"]["total_deaths"]} deaths in the batch list, {J["calm"]["total_track_deaths"]} track deaths of ships at risk.')
dump('out-radar.json', J)
open(os.path.join(HERE_, 'out-radar.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ---- figure
fig = Fig(1100, 600, 'A2 (round 5b): radar deaths from the full radar log', 'Left: deaths in destroyer smokes with the ship radar-lit in its last 40 s, by how far the radar ship was (share of its radar range). Right: deaths per 100 destroyer smokes with and without radar.')
A = [d for d in TD if d['r40'] and d['r40']['share'] is not None]
bins = [(0, .4, 'under 40%'), (.4, .6, '40-60%'), (.6, .8, '60-80%'), (.8, .9, '80-90%'), (.9, 1.04, '90-100%')]
CC = {'cruiser': '#184f95', 'destroyer': '#eda100', 'battleship': '#8a8984'}
fig.add(T(40, 90, f'Distance to the radar ship as a share of its range (n {len(A)}, all track deaths)', size=13, fill=INK, anchor='start', weight='600'))
y = 110
for lo, hi, lab in bins:
    v = [d for d in A if lo <= d['r40']['share'] < hi]; x = 150
    fig.add(T(140, y + 16, lab, size=11.5, fill=INK, anchor='end'))
    for cl in ('cruiser', 'destroyer', 'battleship'):
        n = sum(d['r40']['src_cls'] == cl for d in v); w = n * 9
        if n: fig.add(f'<rect x="{x}" y="{y}" width="{w}" height="24" fill="{CC[cl]}"/>' + (T(x + w / 2, y + 16, str(n), size=10.5, fill=BG, weight='600') if w > 12 else ''))
        x += w
    fig.add(T(x + 6, y + 16, str(len(v)), size=11, fill=INK, anchor='start')); y += 32
fig.legend(150, y + 14, [('radar cruiser', CC['cruiser']), ('radar destroyer', CC['destroyer']), ('radar battleship', CC['battleship'])])
y += 50; o = J['track']
for line in (f'{o["lit40"]} of {o["deaths"]} deaths radar-lit in the last 40 s ({o["lit40_pct"]}%); {o["lit20"]} in the last 20 s.', f'Radar ship itself in a smoke: {o["src_in_smoke"]} of {o["attributed"]}. Ambiguous: {o["ambiguous"]}.',
             f'Lit for a median {o["lit_for_s"]["median"]} s before dying; still lit at death: {o["lit_at_death"]}.', 'Top radar ships: ' + ', '.join(f'{k} {v}' for k, v in list(o['src_ship'].items())[:6])):
    fig.add(T(40, y, line, size=11.5, fill=INK, anchor='start')); y += 20
fig.add(T(600, 90, 'Deaths per 100 destroyer smokes (batch death list)', size=13, fill=INK, anchor='start', weight='600'))
y = 110
rr = {r['label']: r for r in J['rates']['rad_any']}
for lab in ['all'] + STATES:
    a_ = rr['radar log: a covered ship radar-lit while the smoke stood: with' + ('' if lab == 'all' else ', ' + lab)]; b_ = rr['radar log: a covered ship radar-lit while the smoke stood: without' + ('' if lab == 'all' else ', ' + lab)]
    fig.add(T(600, y + 12, ('all destroyer smokes' if lab == 'all' else lab) + (' *' if J['rate_diffs']['rad_any'][lab]['clear'] else ''), size=11.5, fill=INK, anchor='start', weight='600'))
    for n, (r_, lb, colr) in enumerate(((a_, 'radar-lit', '#e34948'), (b_, 'no radar', '#b9b8b3'))):
        yy = y + 20 + n * 18; fig.add(T(730, yy + 12, f'{lb} (n {r_["n"]})', size=10.5, anchor='end'))
        if r_['per_100'] is not None: fig.add(f'<rect x="738" y="{yy}" width="{r_["per_100"]*8:.1f}" height="14" rx="2" fill="{colr}"/>' + T(744 + r_['per_100'] * 8, yy + 11.5, f'{r_["per_100"]:.1f}', size=10.5, fill=INK, anchor='start'))
    y += 68
cn = J['calm']['new']
fig.add(T(600, y + 14, f'Calm smokes (not 50+ behind, no radar in the log): {cn["n"]} smokes, {cn["deaths"]} deaths, {cn["per_100"]} per 100.', size=11.5, fill=INK, anchor='start'))
fig.add(T(600, y + 34, '* = with-radar minus no-radar interval excludes zero.', size=10.5, anchor='start'))
fig.save(os.path.join(FIGS, 'n2-radar-deaths'))
print('done')
