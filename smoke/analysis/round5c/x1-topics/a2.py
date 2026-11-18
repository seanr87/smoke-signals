# A2. Smoke deaths: conditions table, calm smokes, map / time / score splits, and radar deaths three ways. Both death metrics.
# Conditions as in round5b/part-a/a2.py, except the radar condition is lit_covered (radar log) and time uses e0.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlib import *
J = {}
for s in DD:
    r, j = s['r'], s['j']
    ao, at = F(r['alive_ours_act']), F(r['alive_theirs_act'])
    s['outnumbered'] = ao is not None and at is not None and ao < at
    kinds = C(x['kind'] for sm_ in j['smokees'] if sm_['how'] != 'none' for x in sm_.get('detected_by', []))
    s['any_surface'] = kinds['surface lit'] > 0; s['any_firepen'] = kinds['smoke fire penalty'] > 0
    s['behind'] = s['state'] == 'behind 50+'
    s['tband'] = '0-5 min' if s['e0'] < 300 else '5-10 min' if s['e0'] < 600 else '10-15 min' if s['e0'] < 900 else '15+ min'
CONDS = [('50+ behind at activation', 'behind'), ('team outnumbered at activation', 'outnumbered'), ('a covered ship was radar-lit while the smoke stood', 'lit_covered'),
         ('a covered ship was seen by an enemy ship (surface lit)', 'any_surface'), ('a covered ship was lit for firing from smoke', 'any_firepen')]
base = {st.key: val(DD, st, True) for st in DEATHS6}; J['baseline'] = dict(n=len(DD), n_top6=len(TOPS(DD)), n_rest=len(RESTS(DD)), **base, rates=death_rates(DD))
T1 = []
for name, k in CONDS:
    a = [s for s in DD if s[k]]; b = [s for s in DD if not s[k]]
    row = dict(condition=name, key=k, n_with=len(a), n_without=len(b), n_top6_with=len(TOPS(a)), n_rest_with=len(RESTS(a)), share_with=gap_tr(DD, Stat(k, k, (lambda kk: lambda ss: 100.0 * sum(s[kk] for s in ss) / len(ss) if ss else None)(k), len)))
    for st in DEATHS6: row[st.key] = gap_ab(a, b, st)
    for st in (DIED, CAUGHT): row['tr_' + st.key] = gap_tr(a, st)
    T1.append(row)
J['conditions'] = T1
CALM = [s for s in DD if not s['behind'] and not s['lit_covered']]; NOTCALM = [s for s in DD if s['behind'] or s['lit_covered']]
J['calm'] = dict(n=len(CALM), n_top6=len(TOPS(CALM)), n_rest=len(RESTS(CALM)), rates=death_rates(CALM), other=death_rates(NOTCALM),
                 **{st.key: val(CALM, st, True) for st in DEATHS6}, **{'tr_' + st.key: gap_tr(CALM, st) for st in DEATHS6}, **{'vs_other_' + st.key: gap_ab(CALM, NOTCALM, st) for st in (DIED, CAUGHT)})
def split_rows(keyf, labels):
    rows = []
    for lab in labels:
        ss = [s for s in DD if keyf(s) == lab]
        rows.append(dict(label=lab, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)), note=note(len(ss)), rates=death_rates(ss), clans=clan_counts([s for s in ss if s['died'] and s['died_ok']]),
                         **{st.key: val(ss, st, True) for st in (DIED, CAUGHT, DIED_S, CAUGHT_S)}, **{'tr_' + st.key: gap_tr(ss, st) for st in (DIED, CAUGHT)}))
    return rows
MAPS_ = sorted({s['map'] for s in DD}, key=lambda m: -sum(s['map'] == m for s in DD))
TB = ['0-5 min', '5-10 min', '10-15 min', '15+ min']; STATES = ['ahead 50+', 'level', 'behind 50+']
J['by_map'] = split_rows(lambda s: s['map'], MAPS_); J['by_time'] = split_rows(lambda s: s['tband'], TB); J['by_state'] = split_rows(lambda s: s['state'], STATES)

# ---- radar deaths three ways
start = {k: g['j']['battle_start_s'] for k, g in G.items()}
def death_el(game, eid):
    return G[game]['roster'][eid]['death']['seconds'] - start[game]
OTHER_KINDS = ('surface lit', 'proximity', 'aircraft', 'smoke fire penalty')
# every smokee record of every ship, with elapsed onset times: {(game, eid): [(smoke e0, smoke end, [(kind, elapsed)])]}
REC = collections.defaultdict(list)
for s in S:
    j = s['j']; st0 = run_start(j['match_id'], j['game_no'], j['primary_replay'])
    for x in j['smokees']:
        REC[(s['game'], x['entity_id'])].append((s['e0'], s['end'], [(d['kind'], d['seconds'] - st0) for d in x.get('detections', [])]))
def lit_at(g, kind, eid, t, tol=2.0):
    return [r for r in g.lit(kind, target=eid) if r['lit_start_elapsed_s'] is not None and r['lit_start_elapsed_s'] <= t + tol and (r['lit_end_elapsed_s'] or r['lit_start_elapsed_s']) >= t - tol]
def lit_last(g, eid, t, w):
    return [r for r in g.lit('radar', target=eid) if r['lit_start_elapsed_s'] is not None and r['lit_start_elapsed_s'] <= t and (r['lit_end_elapsed_s'] or r['lit_start_elapsed_s']) >= t - w]
def judge(s, eid, t, who):
    g = TL(s['game']); d = dict(game=s['game'], eid=eid, t=t, who=who, grp=s['grp'], team=s['team'], smoke=s['id'], map=s['map'])
    d['a40'] = bool(lit_last(g, eid, t, 40)); d['a20'] = bool(lit_last(g, eid, t, 20))
    at = lit_at(g, 'radar', eid, t); d['b'] = bool(at)
    d['hydro_at'] = bool(lit_at(g, 'hydro', eid, t))
    recs = REC.get((s['game'], eid), [])
    d['rec_covers'] = any(e0 <= t and end >= t - 20 for e0, end, _ in recs)
    d['rec_full'] = any(e0 <= t - 20 and end >= t for e0, end, _ in recs)
    d['other20'] = sorted({k for _, _, ds in recs for k, x in ds if k in OTHER_KINDS and t - 20 <= x <= t + 1})
    d['c'] = d['b'] and not d['hydro_at'] and not d['other20']
    # cross-check from the ship's own track: was it already detected at the last 2 s sample before the radar span that covers its death began
    d['seen_before_radar'] = None
    if at:
        t0 = min(r['lit_start_elapsed_s'] for r in at)
        grew = True
        while grew:   # chain back through radar spans that touch (within 2 s)
            grew = False
            for r in g.lit('radar', target=eid):
                if r['lit_start_elapsed_s'] is not None and r['lit_start_elapsed_s'] < t0 and (r['lit_end_elapsed_s'] or r['lit_start_elapsed_s']) >= t0 - 2: t0 = r['lit_start_elapsed_s']; grew = True
        tr = g.tracks.get(eid); i = tr.idx(t0 - 0.5) if tr else None
        d['seen_before_radar'] = tr.det[i] if i is not None else None
        d['radar_span_s'] = round(t - t0, 1)
        src = [r for r in at if r['row'] == 'lit']
        d['radar_ship'] = src[-1]['ship'].replace('\xa0', ' ') if src else 'unattributed'
    return d
def who_of(c): return 'smoker destroyer' if c['is_smoker'] else 'sheltering cruiser' if c['cls'] == 'cruiser' else 'other'
DIED_D = [judge(s, c['eid'], c['t'], who_of(c)) for s in DD if s['died_ok'] for c in s['died_list']]
CAUGHT_D = [judge(s, d['eid'], death_el(s['game'], d['eid']), who_of(d)) for s in DD for d in s['dead']]
WHO = ['smoker destroyer', 'sheltering cruiser', 'other']
def tally(D, key):
    v = [d for d in D if d[key]]
    return dict(n=len(v), of=len(D), pct=r1(100.0 * len(v) / len(D)), distinct_ships=len({(d['game'], d['eid']) for d in v}), who={w: sum(d['who'] == w for d in v) for w in WHO},
                who_of={w: sum(d['who'] == w for d in D) for w in WHO},
                top6=sum(d['grp'] == 'top' for d in v), top6_of=sum(d['grp'] == 'top' for d in D), rest=sum(d['grp'] == 'rest' for d in v), rest_of=sum(d['grp'] == 'rest' for d in D),
                clans=clan_counts(v))
def tr_share(D, key):
    """Top 6 minus Rest in the share of deaths with the mark, resampling whole clans (deaths carry their smoke's team)."""
    stat = lambda dd: 100.0 * sum(1 for d in dd if d[key]) / len(dd) if dd else None
    random.seed(SEED); lo, hi = boot_diff(D, stat)
    t = [d for d in D if d['grp'] == 'top']; r = [d for d in D if d['grp'] == 'rest']
    return dict(top6=r1(stat(t)), rest=r1(stat(r)), diff=r1(stat(t) - stat(r)), lo=r1(lo), hi=r1(hi), clear=bool(lo is not None and lo * hi > 0))
WAYS = [('a40', '(a) radar-lit at some time in its last 40 s'), ('a20', 'radar-lit at some time in its last 20 s (for comparison with round 5b)'), ('b', '(b) still radar-lit at death'),
        ('c', '(c) radar-lit at death, no other detection found')]
RAD = {}
for lab, D in (('died', DIED_D), ('caught', CAUGHT_D)):
    RAD[lab] = dict(n=len(D), distinct_ships=len({(d['game'], d['eid']) for d in D}), ways={k: dict(tally(D, k), tr=tr_share(D, k)) for k, _ in WAYS})
    B = [d for d in D if d['b']]
    RAD[lab]['b_detail'] = dict(n=len(B), hydro_at_death=sum(d['hydro_at'] for d in B), other_onset_20s=sum(bool(d['other20']) for d in B), other_kinds=dict(C(k for d in B for k in d['other20'])),
                                record_covers_last_20s_fully=sum(d['rec_full'] for d in B), record_covers_part=sum(d['rec_covers'] and not d['rec_full'] for d in B), record_missing=sum(not d['rec_covers'] for d in B),
                                seen_before_radar=dict(C(str(d['seen_before_radar']) for d in B)), c_and_unseen_before=sum(1 for d in B if d['c'] and d['seen_before_radar'] is False),
                                radar_ship=dict(C(d.get('radar_ship') for d in B).most_common(6)), median_span_s=med([d['radar_span_s'] for d in B]))
    RAD[lab]['record_missing_all'] = sum(not d['rec_covers'] for d in D)
J['radar_deaths'] = RAD
J['radar_death_rows'] = dict(died=DIED_D, caught=CAUGHT_D)

# ---- markdown
def pr(d, f='{:.1f}'): return fv(d, f)
M = ['### A2. Smoke deaths: conditions, calm smokes, map, time and score, and radar deaths three ways', '']
c_b, c_r = find(T1, key='behind'), find(T1, key='lit_covered')
rd, rc = RAD['died'], RAD['caught']
cal = J['calm']
M.append(f"**Answer:** Both metrics tell the same story about where deaths are: smokes laid 50+ behind (died {pr(c_b['died100']['a'])} vs {pr(c_b['died100']['b'])} per 100, caught {pr(c_b['caught100']['a'])} vs {pr(c_b['caught100']['b'])}) "
         f"and smokes where a covered ship was radar-lit (died {pr(c_r['died100']['a'])} vs {pr(c_r['died100']['b'])}, caught {pr(c_r['caught100']['a'])} vs {pr(c_r['caught100']['b'])}). "
         f"Calm smokes (neither) are {cal['n']} of {len(DD)} and lose {pr(cal['died100']['value'])} died and {pr(cal['caught100']['value'])} caught per 100. "
         f"Radar: of {rd['n']} ships that died, {rd['ways']['a40']['n']} ({rd['ways']['a40']['pct']:.0f}%) were radar-lit in their last 40 s, {rd['ways']['b']['n']} ({rd['ways']['b']['pct']:.0f}%) were still lit at death, "
         f"and {rd['ways']['c']['n']} ({rd['ways']['c']['pct']:.0f}%) were lit at death with no other detection found; of {rc['n']} caught, {rc['ways']['a40']['n']} ({rc['ways']['a40']['pct']:.0f}%), {rc['ways']['b']['n']} ({rc['ways']['b']['pct']:.0f}%) and {rc['ways']['c']['n']} ({rc['ways']['c']['pct']:.0f}%). "
         f"Radar seldom found these ships first: of the {rd['b_detail']['n']} died ships still lit at death, {rd['b_detail']['seen_before_radar'].get('True', 0)} were already detected just before the radar reached them.")
M.append('')
b = J['baseline']
M.append(f"**Numbers:** {len(DD)} destroyer smokes ({len(TOPS(DD))} Top 6, {len(RESTS(DD))} Rest). Baseline: died {b['rates']['died']} ships, {fvci(b['died100'])} per 100 (smoker {fvci(b['died_smoker100'])}; "
         f"cruisers {fvci(b['died_cr100'])} per 100 sheltering); caught {b['rates']['caught']}, {fvci(b['caught100'])} per 100 (smoker {fvci(b['caught_smoker100'])}; cruisers {fvci(b['caught_cr100'])} per 100 sheltering). {DIED_NOTE}")
M.append('')
M.append('Table 1. Conditions: deaths per 100 destroyer smokes with the condition and without it (difference, 95% interval; * = clear).')
M.append(md_table(['condition', 'n with / without', 'died: with / without', 'died: difference', 'caught: with / without', 'caught: difference', 'with it, Top 6 / Rest (n): died', 'with it, Top 6 / Rest: caught'],
                  [[x['condition'], f"{x['n_with']} / {x['n_without']}", f"{pr(x['died100']['a'])} / {pr(x['died100']['b'])}", fdiff(x['died100']), f"{pr(x['caught100']['a'])} / {pr(x['caught100']['b'])}", fdiff(x['caught100']),
                    f"{pr(x['tr_died100']['top6'])} / {pr(x['tr_died100']['rest'])} ({x['n_top6_with']} / {x['n_rest_with']})", f"{pr(x['tr_caught100']['top6'])} / {pr(x['tr_caught100']['rest'])}"] for x in T1]))
M.append('')
M.append('Table 2. The same conditions, split by who is lost: the smoker (per 100 smokes) and sheltering cruisers (per 100 sheltering cruisers; n = cruisers).')
M.append(md_table(['condition', 'smoker died: with / without (difference)', 'smoker caught: with / without (difference)', 'cruisers died: with (n) / without (n) (difference)', 'cruisers caught: with (n) / without (n) (difference)'],
                  [[x['condition'], f"{pr(x['died_smoker100']['a'])} / {pr(x['died_smoker100']['b'])} ({fdiff(x['died_smoker100'])})", f"{pr(x['caught_smoker100']['a'])} / {pr(x['caught_smoker100']['b'])} ({fdiff(x['caught_smoker100'])})",
                    f"{fn_(x['died_cr100']['a'], x['died_cr100']['n_a'])} / {fn_(x['died_cr100']['b'], x['died_cr100']['n_b'])} ({fdiff(x['died_cr100'])})",
                    f"{fn_(x['caught_cr100']['a'], x['caught_cr100']['n_a'])} / {fn_(x['caught_cr100']['b'], x['caught_cr100']['n_b'])} ({fdiff(x['caught_cr100'])})"] for x in T1]))
M.append('')
M.append('Definitions: "outnumbered" = fewer of our ships alive than theirs at activation. "Radar-lit" = a covered ship (the smoker or a ship inside or behind) carried the radar flag at some time while the smoke stood, from the radar log. '
         '"Seen by an enemy ship" and "lit for firing" = a covered ship has that detection kind recorded while this smoke concealed it.')
M.append('')
M.append(f"Calm smokes (not 50+ behind and no covered ship radar-lit): {cal['n']} smokes ({cal['n_top6']} Top 6, {cal['n_rest']} Rest). Died {cal['rates']['died']} ships, {fvci(cal['died100'])} per 100 "
         f"(smoker {fvci(cal['died_smoker100'])}); caught {cal['rates']['caught']}, {fvci(cal['caught100'])} per 100 (smoker {fvci(cal['caught_smoker100'])}). "
         f"The other {len(NOTCALM)} smokes: died {pr(cal['other']['died_per100'])}, caught {pr(cal['other']['caught_per100'])} per 100 (calm minus other: died {fdiff(cal['vs_other_died100'])}, caught {fdiff(cal['vs_other_caught100'])}).")
M.append('')
M.append('Table 3. Calm smokes, Top 6 against Rest.')
M.append(md_table(['measure', 'Top 6 (n)', 'Rest (n)', 'Top 6 minus Rest'], [[st.label, fn_(cal['tr_' + st.key]['top6'], cal['tr_' + st.key]['n_top6']), fn_(cal['tr_' + st.key]['rest'], cal['tr_' + st.key]['n_rest']), fdiff(cal['tr_' + st.key])] for st in DEATHS6]))
M.append('')
def split_table(title, rows):
    M.append(title)
    M.append(md_table(['', 'n (Top 6 / Rest)', 'died per 100 [95%]', 'died: Top 6 / Rest', 'died: Top 6 minus Rest', 'caught per 100 [95%]', 'caught: Top 6 / Rest', 'caught: Top 6 minus Rest', 'smoker died / caught per 100', 'note'],
                      [[x['label'], f"{x['n']} ({x['n_top6']} / {x['n_rest']})", fvci(x['died100']), f"{pr(x['tr_died100']['top6'])} / {pr(x['tr_died100']['rest'])}", fdiff(x['tr_died100']),
                        fvci(x['caught100']), f"{pr(x['tr_caught100']['top6'])} / {pr(x['tr_caught100']['rest'])}", fdiff(x['tr_caught100']), f"{pr(x['died_smoker100']['value'])} / {pr(x['caught_smoker100']['value'])}", x['note']] for x in rows]))
    M.append('')
split_table('Table 4. By map.', J['by_map'])
split_table('Table 5. By time of activation (replay clock).', J['by_time'])
split_table('Table 6. By score at activation.', J['by_state'])
M.append(f"Radar deaths. \"Died\" ships: {rd['n']} deaths ({rd['distinct_ships']} distinct ships). \"Caught\" ships: {rc['n']} death records ({rc['distinct_ships']} distinct ships). "
         'Radar-lit comes from the radar log for that ship. (a) a radar-lit span touches its last 40 s. (b) a radar-lit span covers the moment of death, give or take 2 s. '
         '(c) as (b), and the hydro log does not have it lit at death, and no smoke record of that ship shows a first detection of another kind (seen by a ship, proximity, aircraft, lit for firing) in its last 20 s.')
M.append('')
def way_rows(lab, R):
    out = []
    for k, name in WAYS:
        w = R['ways'][k]
        out.append([lab, name, f"{w['n']} of {w['of']} ({w['pct']:.0f}%)"] + [f"{w['who'][x]} of {w['who_of'][x]}" for x in WHO] +
                   [f"{w['top6']} of {w['top6_of']} ({w['tr']['top6']:.0f}%)", f"{w['rest']} of {w['rest_of']} ({w['tr']['rest']:.0f}%)", fdiff(w['tr'])])
    return out
M.append('Table 7. Radar deaths three ways.')
M.append(md_table(['metric', 'reading', 'deaths', 'smoker destroyer', 'sheltering cruiser', 'other', 'Top 6', 'Rest', 'share, Top 6 minus Rest'], way_rows('died', rd) + way_rows('caught', rc)))
M.append('')
for lab, R in (('died', rd), ('caught', rc)):
    bd = R['b_detail']
    M.append(f"- {lab}: of the {bd['n']} still lit at death, {bd['hydro_at_death']} were also hydro-lit and {bd['other_onset_20s']} had another kind of detection start in the last 20 s ({bd['other_kinds']}). "
             f"The smoke record covers the whole last 20 s for {bd['record_covers_last_20s_fully']}, part of it for {bd['record_covers_part']}, none of it for {bd['record_missing']}. "
             f"Cross-check from the ship's own track: at the last sample before that radar span began the ship was undetected in {bd['seen_before_radar'].get('False', 0)}, already detected in {bd['seen_before_radar'].get('True', 0)} "
             f"(unknown {bd['seen_before_radar'].get('None', 0)}); {bd['c_and_unseen_before']} deaths are both (c) and undetected before the radar. Median time lit before death {bd['median_span_s']} s. Radar ships: {bd['radar_ship']}.")
M.append(f"- Clans, (b) still lit at death, died: {rd['ways']['b']['clans']}.")
M.append('')
x40 = rd['ways']['a40']['tr']; xb = rd['ways']['b']['tr']
M.append(f"**Top 6 or Shared:** Shared pattern, Rest pays more. The conditions raise deaths in both groups (Table 1, last columns). Calm smokes: Top 6 minus Rest died {fdiff(cal['tr_died100'])}, caught {fdiff(cal['tr_caught100'])}. "
         f"Share of died ships radar-lit in the last 40 s: Top 6 {x40['top6']:.0f}%, Rest {x40['rest']:.0f}% ({fdiff(x40)}); still lit at death: {xb['top6']:.0f}% vs {xb['rest']:.0f}% ({fdiff(xb)}). "
         f"On caught ships the Rest share is clearly higher: last 40 s {rc['ways']['a40']['tr']['top6']:.0f}% vs {rc['ways']['a40']['tr']['rest']:.0f}% ({fdiff(rc['ways']['a40']['tr'])}), "
         f"still lit at death {rc['ways']['b']['top6']} of {rc['ways']['b']['top6_of']} vs {rc['ways']['b']['rest']} of {rc['ways']['b']['rest_of']} ({fdiff(rc['ways']['b']['tr'])}). The two metrics disagree here, so treat the group gap in radar deaths as a lead.")
M.append('')
worst = max((x for x in J['by_map'] if x['n'] >= 15), key=lambda x: x['died100']['value'])
M.append(f"**Clans:** highest map on \"died\" is {worst['label']} ({pr(worst['died100']['value'])} per 100); smokes with a death there: {worst['clans']}.")
M.append('')
M.append(f"**Could not be done / proxy:** Reading (c) is a floor on other detection, not a full check. The batch keeps, per ship and per smoke, only the first moment of each detection kind while that smoke concealed it; it has no second-by-second list of who saw the ship. "
         f"So (c) removes deaths where another kind of detection started in the last 20 s, or hydro had the ship, but it cannot see a ship that an enemy had been watching for longer, or one that died after the smoke record ended "
         f"(the record misses the last 20 s entirely for {rd['b_detail']['record_missing']} of the {rd['b_detail']['n']} died ships lit at death and {rc['b_detail']['record_missing']} of the {rc['b_detail']['n']} caught). "
         "The track cross-check (undetected just before the radar arrived) is the closest proxy for \"radar is what found it\". Read (c) as an upper limit on deaths owed to radar alone.")
M.append('')
M.append('**Verdict:** Keep (conditions, calm smokes, radar readings (a) and (b)). Lead for (c).')
M.append('')
# changed from round 5b
o = old('out-a2.json'); oc = {r['condition']: r for r in o['conditions_all']}
CH = []
CH.append(chg_row('deaths in destroyer smokes: caught', o['baseline'][0]['deaths'], b['rates']['caught'], 'same list', '{}'))
CH.append(chg_row('deaths in destroyer smokes: died (round 5b N1 counted 201 ships at risk in the smoke window)', 201, b['rates']['died'], 'new death metric: exactly 20 s after dispersal, each ship once, 9 smokes left out', '{}'))
for old_name, k in (('50+ behind at activation', 'behind'), ('team outnumbered at activation', 'outnumbered'), ('a covered ship was lit by surface spotting (seen by an enemy ship)', 'any_surface'), ('a covered ship lit for firing from smoke (smoke fire penalty)', 'any_firepen')):
    x = find(T1, key=k); r = oc[old_name]
    CH.append(chg_row(f"{x['condition']}: n with", r['n_with'], x['n_with'], 'unchanged', '{}'))
    CH.append(chg_row(f"{x['condition']}: deaths per 100 with / without, now caught", f"{r['deaths_per_100_with']:.1f} / {r['deaths_per_100_without']:.1f}", f"{x['caught100']['a']:.1f} / {x['caught100']['b']:.1f}", 'same list'))
    CH.append(chg_row(f"{x['condition']}: deaths per 100 with / without, now died", f"{r['deaths_per_100_with']:.1f} / {r['deaths_per_100_without']:.1f}", f"{x['died100']['a']:.1f} / {x['died100']['b']:.1f}", 'new death metric'))
x = c_r
CH.append(chg_row('radar-lit covered ship: n with (round 5b N2, radar log)', 388, x['n_with'], 'lit_covered counts the smoker and ships inside or behind only', '{}'))
CH.append(chg_row('radar-lit covered ship: deaths per 100 with / without, now caught (round 5b N2: 20.9 / 6.3)', '20.9 / 6.3', f"{x['caught100']['a']:.1f} / {x['caught100']['b']:.1f}", 'lit_covered definition'))
CH.append(chg_row('radar-lit covered ship: deaths per 100 with / without, now died', '20.9 / 6.3', f"{x['died100']['a']:.1f} / {x['died100']['b']:.1f}", 'new death metric'))
CH.append(chg_row('calm smokes: n (round 5b N2)', 515, cal['n'], 'lit_covered from the round 5c library in place of the radar test in the round 5b script; 2 smokes differ', '{}'))
CH.append(chg_row('calm smokes: deaths, now caught', 19, cal['rates']['caught'], 'lit_covered definition', '{}'))
CH.append(chg_row('calm smokes: deaths per 100, now caught', 3.7, cal['caught100']['value'], 'lit_covered definition'))
CH.append(chg_row('calm smokes: deaths per 100, now died', 3.7, cal['died100']['value'], 'new death metric'))
for okey, rows, lab in (('by_map', J['by_map'], ''), ('by_state', J['by_state'], '')):
    om = {r['label']: r for r in o[okey]}
    for x in rows:
        r = om[x['label']]
        CH.append(chg_row(f"{x['label']}: deaths per 100, now caught", r['deaths_per_100']['value'], x['caught100']['value'], 'same list'))
        CH.append(chg_row(f"{x['label']}: deaths per 100, now died", r['deaths_per_100']['value'], x['died100']['value'], 'new death metric'))
om = {r['label'].replace('15-20 min', '15+ min'): r for r in o['by_time']}
for x in J['by_time']:
    r = om[x['label']]
    CH.append(chg_row(f"{x['label']}: n", r['n'], x['n'], 'time from the replay clock (e0), not the HUD clock', '{}'))
    CH.append(chg_row(f"{x['label']}: deaths per 100, now caught", r['deaths_per_100']['value'], x['caught100']['value'], 'time from the replay clock'))
    CH.append(chg_row(f"{x['label']}: deaths per 100, now died", r['deaths_per_100']['value'], x['died100']['value'], 'new death metric'))
CH.append(chg_row('caught deaths radar-lit in the last 40 s (round 5b N2: 65 of 124)', 65, rc['ways']['a40']['n'], 'same radar log', '{}'))
CH.append(chg_row('caught deaths radar-lit in the last 20 s (round 5b N2: 56 of 124)', 56, rc['ways']['a20']['n'], 'same radar log; one death sits on the 20 s edge (which rule moved it was not traced)', '{}'))
CH.append(chg_row('died ships radar-lit in the last 40 s', None, f"{rd['ways']['a40']['n']} of {rd['n']}", 'new death metric', '{}'))
CH.append(chg_row('still radar-lit at death (died / caught)', None, f"{rd['ways']['b']['n']} of {rd['n']} / {rc['ways']['b']['n']} of {rc['n']}", 'new reading', '{}'))
CH.append(chg_row('radar-lit at death, no other detection found (died / caught)', None, f"{rd['ways']['c']['n']} of {rd['n']} / {rc['ways']['c']['n']} of {rc['n']}", 'new reading', '{}'))
nun = sum(1 for r in CH if r[3] == 'unchanged'); CH = [r for r in CH if r[3] != 'unchanged']
M.append('**Changed from round 5b:** the "round 5b" column is `round5b/part-a/out-a2.json` (round 5 with the clock fix), or the round 5b redo N2 where the row says so.')
M.append('')
M.append(md_table(['number', 'round 5b', 'round 5c', 'why'], CH))
M.append('')
M.append(f'{nun} other compared numbers are unchanged (caught per 100 is the same list as round 5 deaths wherever the smokes in the row are the same).')
M.append('')
J['changed'] = CH
CHK = [['A2 baseline died / caught per 100', 'a2.py', "J['baseline'] (death_rates(DD))", f"{b['rates']['died']} ships, {b['died100']['value']} / {b['rates']['caught']}, {b['caught100']['value']}"],
       ['A2 50+ behind: died with / without; caught with / without', 'a2.py', "T1 / J['conditions'] key behind", f"{c_b['died100']['a']} / {c_b['died100']['b']}; {c_b['caught100']['a']} / {c_b['caught100']['b']}"],
       ['A2 radar-lit covered ship: died with / without; caught with / without', 'a2.py', "T1 / J['conditions'] key lit_covered", f"{c_r['died100']['a']} / {c_r['died100']['b']}; {c_r['caught100']['a']} / {c_r['caught100']['b']}"],
       ['A2 calm smokes: n, died per 100, caught per 100', 'a2.py', "CALM / J['calm']", f"{cal['n']}, {cal['died100']['value']}, {cal['caught100']['value']}"],
       ['A2 radar deaths, died: (a) / (b) / (c) of n', 'a2.py', "RAD['died']['ways'] (DIED_D, judge())", f"{rd['ways']['a40']['n']} / {rd['ways']['b']['n']} / {rd['ways']['c']['n']} of {rd['n']}"],
       ['A2 radar deaths, caught: (a) / (b) / (c) of n', 'a2.py', "RAD['caught']['ways'] (CAUGHT_D, judge())", f"{rc['ways']['a40']['n']} / {rc['ways']['b']['n']} / {rc['ways']['c']['n']} of {rc['n']}"],
       ['A2 caught, radar-lit in the last 20 s', 'a2.py', "RAD['caught']['ways']['a20']", rc['ways']['a20']['n']]]
save('out-a2', J, '\n'.join(M), CHK)
