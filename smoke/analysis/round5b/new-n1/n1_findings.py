# Round 5b, worker n1: writes FINDINGS-N1.md, CHECK-N1.md and caps.json from c1.json and c2.json
# (run n1_c1.py and n1_c2.py first). Run: python -I -X utf8 n1_findings.py
import os, json
H = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(H, 'c1.json'), encoding='utf-8'))
B = json.load(open(os.path.join(H, 'c2.json'), encoding='utf-8'))
L = []
def W(*a): L.append(' '.join(str(x) for x in a))
def tab(h, rows):
    W('| ' + ' | '.join(h) + ' |'); W('|' + '---|' * len(h))
    for r in rows: W('| ' + ' | '.join(str(c) for c in r) + ' |')
    W('')
def iv(c, f='{:+.1f}'): return f'{f.format(c[0])} to {f.format(c[1])}'
def gap(r): return f'{r["gap"]:+.1f} ({iv(r["gap_ci"])})' + (' clear' if r['gap_clear'] else '')
def d(new, old, f='{:+.1f}'): return f.format(new - old)
def sm(n): return ' (small n)' if n < 15 else ''
def n_(x): return f'{x:,}'

tw = A['three_ways']; ct = A['crosstab']; e60 = {r['what']: r for r in A['overall']['enemy_60']}; edu = {r['what']: r for r in A['overall']['enemy_during']}
gr = {g['grace_s']: g for g in A['grace']}; cd = A['cap_defended']; inv = A['invaded']; rb = A['ribbons']
ALLK = 'all applicable smokes'

W('# Round 5b findings, worker n1: C1 and C2 redone from the cap timeline')
W('')
W('Batch `output/20261117-230933`. 1,547 smokes, 171 games, 30 clans. Everything is association, not cause. Intervals are 95%, by resampling whole clans (C1) or whole games (C2). "Clear" = the interval excludes zero.')
W('This file is written by `n1_findings.py` from the numbers computed in `n1_c1.py` and `n1_c2.py`.')
W('')
# ------------------------------------------------------------------ C1
W('### C1. Cap defence: "enemy took the cap" from the timeline, and ribbons')
W('')
e = tw['enemy']; ce = ct['enemy']
W(f'**Answer:** With the full cap timeline, the enemy took the nearest cap during the smoke or within 60 seconds after it in {e["within_60_pct"]}% of the smokes where the question applies ({e["within_60"]} of {n_(e["applicable"])}); round 5 said {gr[60]["round5_pct"]}% ({gr[60]["round5_yes"]}). '
  f'Strictly while the smoke stood it is {e["during_pct"]}% ({e["during"]}). The round 5 snapshot version never said yes wrongly, but it missed {ce["snapshot_missed"]} of {ce["timeline_yes"]} real flips ({ce["missed_pct"]}%), more than the 15% estimated then. '
  f'The Top 6 vs Rest gaps that round 5 called clear are not clear any more; the snapshots had missed more Top 6 flips ({ce["by_group"]["top"]["missed_pct"]}%) than Rest flips ({ce["by_group"]["rest"]["missed_pct"]}%). '
  f'Ribbons can now be counted, but only {rb["covered"]} of {n_(1547)} smokes covered a recording player, so they are a check on the timeline, not a measure.')
W('')
W('**Numbers: three ways** (nearest cap by geometry; "not applicable" = the cap was already the enemy\'s at activation)')
W('')
tab(['what', 'applicable smokes', 'strictly while the smoke stood', 'only in the 60 s after it cleared', 'during or within 60 s'],
    [[('enemy took the nearest cap' if k == 'enemy' else 'we took the nearest cap (cap not ours at activation)'), n_(v['applicable']), f'{v["during"]} ({v["during_pct"]}%)', f'{v["after_only"]} ({v["after_only_pct"]}%)', f'{v["within_60"]} ({v["within_60_pct"]}%)'] for k, v in tw.items()])
W('- Grace after the smoke clears, enemy took: ' + '; '.join(f'{g["grace_s"]} s: {g["yes"]} ({g["pct"]}%)' + (f' [round 5: {g["round5_yes"]}, {g["round5_pct"]}%]' if g['round5_yes'] is not None else '') for g in A['grace']) + '.')
W(f'- Not applicable: {e["not_applicable"]} smokes (round 5: 474). Owner of the nearest cap at activation agrees with the round 5 stored value in {1547 - A["checks"]["owner_at_activation_mismatch"]} of 1,547 smokes; the {A["checks"]["owner_at_activation_mismatch"]} others flipped within a second of the activation.')
W('')
W('**Numbers: timeline against the round 5 snapshot version, same smokes, 60 s grace both**')
W('')
t = ce['table']
tab(['enemy took: round 5 snapshot \\ timeline', 'yes', 'no', 'not applicable'], [[o] + [t[f'{o}|{n}'] for n in ('yes', 'no', 'n/a')] for o in ('yes', 'no', 'n/a')])
cw = ct['we']
W(f'- Enemy took: both versions apply to {n_(ce["both_applicable"])} smokes. They agree on {n_(ce["agree"])} ({ce["agree_pct"]}%). Snapshot missed a flip: {ce["snapshot_missed"]}. Snapshot wrong the other way: {ce["snapshot_wrong_other_way"]}. '
  f'So the snapshot version missed {ce["missed_pct"]}% of the {ce["timeline_yes"]} real flips. In {ce["snapshot_missed"] - ce["missed_flipped_back"]} of the {ce["snapshot_missed"]} misses the cap was still the enemy\'s at the end of the window: the flip simply came after the last snapshot.')
W(f'- By group: Top 6 {ce["by_group"]["top"]["flips"]} real flips, {ce["by_group"]["top"]["missed"]} missed ({ce["by_group"]["top"]["missed_pct"]}%); Rest {ce["by_group"]["rest"]["flips"]} real flips, {ce["by_group"]["rest"]["missed"]} missed ({ce["by_group"]["rest"]["missed_pct"]}%). Both groups had the same number of snapshots per smoke (mean {ce["by_group"]["top"]["mean_snapshots"]} and {ce["by_group"]["rest"]["mean_snapshots"]}), so this is how the misses happened to fall, not a coverage difference.')
W(f'- We took: both apply to {n_(cw["both_applicable"])}; agree {n_(cw["agree"])} ({cw["agree_pct"]}%); snapshot missed {cw["snapshot_missed"]} of {cw["timeline_yes"]} real flips ({cw["missed_pct"]}%); wrong the other way {cw["snapshot_wrong_other_way"]}.')
x = A['cap_won_crosscheck']
W(f'- Checks. (1) A second computation straight from the timeline rows agrees on all 1,547 smokes ({A["checks"]["second_way_mismatch"]} mismatches). (2) The batch field `cap_won` names the nearest cap in {x["n"]} smokes: the timeline says "we took it" in {x["timeline60_yes"]} (1 not applicable); the snapshot version found {x["snapshot_yes"]}. (3) Team-frame cap letters from the timeline file match the round 5 geometry in every smoke.')
W('')
W('**Numbers: summary tables from the timeline** (during the smoke or within 60 s after; last two columns are round 5)')
W('')
tab(['group', 'n', 'enemy took it (interval)', 'Top 6', 'Rest', 'Top 6 - Rest', 'strictly during', 'round 5 share', 'round 5 gap'],
    [[r['what'], n_(r['n']), f'{r["pct"]}% ({r["ci"][0]} to {r["ci"][1]})', f'{r["top6_pct"]}% (n {r["top6_n"]})', f'{r["rest_pct"]}% (n {r["rest_n"]})', gap(r), f'{edu[r["what"]]["pct"]}%; gap {gap(edu[r["what"]])}',
      f'{r["round5"]["pct"]}% (n {n_(r["round5"]["n"])})' if r['round5'] else '-', gap(r['round5']) if r['round5'] else '-'] for r in A['overall']['enemy_60']])
mc = [r for r in A['by_map_cap'] if not r.get('too_few')]
top5 = sorted([r for r in mc if r['n'] >= 15], key=lambda r: -r['pct'])[:5]
W('- By map and cap (team-frame letter; all 26 rows in `out-c1.md` and `caps.json`). Highest: ' + '; '.join(f'{r["map"]} {r["cap"]} {r["pct"]}% (n {r["n"]}; round 5 {r["round5_pct"]}%)' for r in top5) + '.')
clr = [r for r in mc if r['gap_clear'] and r['top6_n'] >= 8 and r['rest_n'] >= 8]
W('- Clear Top 6 vs Rest gaps by map and cap now: ' + ('; '.join(f'{r["map"]} {r["cap"]} (Top 6 {r["top6_pct"]}% of {r["top6_n"]}{sm(r["top6_n"])}, Rest {r["rest_pct"]}% of {r["rest_n"]}{sm(r["rest_n"])}; {gap(r)})' for r in clr) or 'none') +
  f'. One clear row out of {sum(1 for r in mc if r["top6_n"] >= 8 and r["rest_n"] >= 8)} rows with enough smokes on both sides is about what luck alone gives. The three round 5 rows are no longer clear: ' +
  '; '.join(f'{r["map"]} {r["cap"]} {gap(r)} (was {r["round5_gap"]:+.1f} clear)' for r in mc if r.get('round5_gap_clear') and not r['gap_clear'] and r['top6_n'] >= 8 and r['rest_n'] >= 8) + '.')
W('- We took the nearest cap (60 s): ' + '; '.join(f'{r["what"]}: {r["pct"]}% (n {r["n"]}), Top 6 {r["top6_pct"]}% vs Rest {r["rest_pct"]}%, gap {gap(r)}; round 5 {r["round5"]["pct"]}%' for r in A['we_took']) + '.')
W('- One row per smoke is in `new-n1/enemy-took.csv` (timeline values and the round 5 snapshot values side by side).')
W('')
W('**Numbers: `cap_defended` follow-up, was the defended cap still ours afterwards?**')
W('')
W(f'Kept = the enemy did not take the defended cap from the first moment it was ours and invaded until 60 s after the smoke cleared. The timeline shows that moment inside the smoke for {cd["found"]} of {cd["n"]} smokes.')
W('')
ks = {r['what']: r for r in cd['kept_strict']}
tab(['group', 'n', 'kept through 60 s after (interval)', 'Top 6', 'Rest', 'Top 6 - Rest', 'kept while the smoke stood', 'round 5 (snapshot, 60 s)'],
    [[r['what'], r['n'], f'{r["pct"]}% ({r["ci"][0]} to {r["ci"][1]})', f'{r["top6_pct"]}% (n {r["top6_n"]})', f'{r["rest_pct"]}% (n {r["rest_n"]})', gap(r), f'{ks[r["what"]]["pct"]}%', f'{r["round5"]["pct"]}%'] for r in cd['kept']])
g_ = cd['grace']
W(f'- No grace: {g_["0"]["kept"]} of {cd["n"]} kept ({g_["0"]["pct"]}%; round 5 374, 77.0%). 60 s: {g_["60"]["kept"]} ({g_["60"]["pct"]}%; round 5 294, 60.5%). 120 s: {g_["120"]["kept"]} ({g_["120"]["pct"]}%; round 5 252, 51.9%). '
  f'Sixty seconds after the smoke cleared the defended cap was ours in {cd["last_owner"].get("ours", 0)} and the enemy\'s in {cd["last_owner"].get("theirs", 0)}.')
b_ = cd['baseline_ours_kept']
W(f'- For comparison, any smoke whose nearest cap was ours at activation kept it through 60 s after in {b_["pct"]}% (n {b_["n"]}); round 5 said {b_["round5_pct"]}%.')
W('')
W('**Numbers (new): was the enemy inside our cap while the smoke stood?** (the timeline records the invading team)')
W('')
tab(['smokes', 'n', 'enemy was invading the cap during the smoke (interval)', 'Top 6', 'Rest', 'Top 6 - Rest'],
    [[r['what'], r['n'], f'{r["pct"]}% ({r["ci"][0]} to {r["ci"][1]})', f'{r["top6_pct"]}% (n {r["top6_n"]})', f'{r["rest_pct"]}% (n {r["rest_n"]})', gap(r)] for r in inv['groups']])
tab(['smokes', 'n', 'cap kept while the smoke stood (interval)', 'Top 6', 'Rest', 'Top 6 - Rest', 'kept through 60 s after', 'Top 6 - Rest (60 s)'],
    [[r['what'], r['n'], f'{r["pct"]}% ({r["ci"][0]} to {r["ci"][1]})', f'{r["top6_pct"]}% (n {r["top6_n"]})', f'{r["rest_pct"]}% (n {r["rest_n"]})', gap(r), f'{r["kept_60"]["pct"]}%', gap(r['kept_60'])] for r in inv['kept']])
k0 = inv['kept'][0]
W(f'- When the enemy stood in a cap we owned and a smoke was within 2 km, the cap was still ours when the smoke cleared in {k0["pct"]}% and 60 s later in {k0["kept_60"]["pct"]}% (n {k0["n"]}). The enemy stood in it for a median of {inv["median_invaded_s"]} s. A cap that was not invaded was never lost while the smoke stood, as it must be.')
W('')
W('**Numbers: ribbons per smoke**')
W('')
W(f'- How thin this is: a replay holds only its own recording player\'s ribbons. That is one ship per team per game: {rb["recorders"]} ships of 3,078. The batch has {rb["rows"]} cap ribbons: ' + ', '.join(f'{k} {v}' for k, v in rb['by_kind'].items()) + '. Each row is one ribbon (the count column is always 1).')
W(f'- Smokes that covered the smoking team\'s recording player: {rb["covered"]} of 1,547 ({100*rb["covered"]/1547:.1f}%): ' + ', '.join(f'{k.replace("_", " ")} {v}' for k, v in sorted(rb['covered_how'].items(), key=lambda kv: -kv[1])) +
  f'. The recording player was the smoker or inside in {rb["inside_or_smoker"]} ({100*rb["inside_or_smoker"]/1547:.1f}%). So {1547 - rb["covered"]:,} smokes ({100 - 100*rb["covered"]/1547:.0f}%) cannot have a ribbon in this data whatever happened.')
W('- Strict count (ribbon by a ship the smoke covered, during the smoke). A Defended ribbon repeats while defending, so events and distinct smokes are both given:')
W('')
def rr(r): return [r['what'].strip(), r['smokes'], f'{r["smokes_with_any"]} ({100*r["smokes_with_any"]/r["smokes"]:.1f}%)'] + [f'{r["events"][k]} in {r["distinct_smokes"][k]} smokes ({r["events_per_100"][k]} per 100)' for k in ('Defended', 'Captured', 'AssistedInCapture')]
tab(['smokes', 'n', 'with any cap ribbon', 'Defended', 'Captured', 'Assisted in capture'], [rr(r) for r in rb['strict']])
W(f'- Looser count (ribbon by a ship of the smoking team during the smoke while that ship was within 2 km of the smoke; the recording player was that close in {rb["near_2km"]} smokes). It is not a superset of the strict count: ships behind a smoke or firing through it are often further than 2 km away.')
W('')
tab(['smokes', 'n', 'with any cap ribbon', 'Defended', 'Captured', 'Assisted in capture'], [rr(r) for r in rb['loose']])
W('- Top 6 vs Rest, share of smokes with a ribbon:')
W('')
tab(['measure', 'n', 'share (interval)', 'Top 6', 'Rest', 'Top 6 - Rest'], [[r['what'], r['n'], f'{r["pct"]}% ({r["ci"][0]} to {r["ci"][1]})', f'{r["top6_pct"]}% (n {r["top6_n"]})', f'{r["rest_pct"]}% (n {r["rest_n"]})', gap(r)] for r in rb['top_vs_rest']])
W('- Do smokes with a Defended ribbon keep the cap more often? (nearest cap ours at activation; the ribbon does not say which cap it was for)')
W('')
def kp(k, n): return f'{k} of {n} ({100*k/n:.0f}%){sm(n)}' if n >= 8 else f'too few (n {n})'
tab(['smokes', 'Defended ribbon: kept while the smoke stood', 'no Defended ribbon', 'Defended ribbon: kept through 60 s after', 'no Defended ribbon', 'gap at 60 s (interval)'],
    [[r['what'], kp(r['with_ribbon_kept_during'], r['with_ribbon_n']), kp(r['without_kept_during'], r['without_n']), kp(r['with_ribbon_kept_60'], r['with_ribbon_n']), kp(r['without_kept_60'], r['without_n']),
      f'{r["gap_60"]:+.0f} ({iv(r["gap_ci"], "{:+.0f}")})' if r['gap_60'] is not None else '-'] for r in rb['defended_vs_kept']])
dk = rb['defended_vs_kept'][0]; tc = rb['timeline_check']; cv = rb['captured_vs_we_took']
W(f'  Only the first row has enough smokes: {dk["with_ribbon_n"]} smokes with a Defended ribbon, all {dk["with_ribbon_kept_during"]} kept the cap while the smoke stood, and {dk["with_ribbon_kept_60"]} still had it 60 s later, against {100*dk["without_kept_60"]/dk["without_n"]:.0f}% without a ribbon. The interval is wide and includes zero. The data cannot say that Defended ribbons go with keeping the cap.')
W(f'- What the ribbons are good for: they confirm the timeline. {tc["captured_on_flip"]} of {tc["captured"]} Captured ribbons fall within 3 s of a cap changing to that team; all {tc["defended_while_any_cap_invaded"]} of {tc["defended"]} Defended ribbons fall while the enemy stood in a cap ({tc["defended_while_invaded"]} in a cap the team owned; the others in a neutral cap). '
  f'Of {cv["n"]} smokes with a strict Captured ribbon, the timeline says "we took the nearest cap during the smoke" in {cv["we_took_during"]}; in the other {cv["already_ours"]} the ribbon was for a different cap.')
W('')
a = e60[ALLK]; dd = e60['destroyer smokes']; n2 = e60['smoke centre inside or within 2 km of the cap']; nu = e60['cap neutral at activation']
W(f'**Top 6 or Shared:** Shared. Enemy took the nearest cap (60 s): Top 6 {a["top6_pct"]}% vs Rest {a["rest_pct"]}%, gap {gap(a)}. Destroyer smokes: {gap(dd)}. Within 2 km: {gap(n2)}. '
  f'The one gap that stays clear is for caps that were neutral at activation: Top 6 {nu["top6_pct"]}% vs Rest {nu["rest_pct"]}%, {gap(nu)}; strictly during the smoke {gap(edu["cap neutral at activation"])}. '
  f'Ribbons: Rest smokes carry a Defended ribbon more often and Top 6 smokes a Captured or Assisted ribbon more often (table above), on 110 and 158 smokes; treat as a hint.')
W('')
W('**Clans:** not a spot item. The clan of every smoke is in `enemy-took.csv`.')
W('')
W('**Could not be done / proxy:** Ribbons per smoke for all smokes: the replays hold them for one ship per team only. "Enemy took the cap" from the timeline is the measure to use; ribbons only confirm it. A Defended ribbon does not name its cap. The nearest cap can be far from the smoke; the "within 2 km" rows are the meaningful ones.')
W('')
W('**Verdict:** Keep (the timeline version replaces the snapshot version). Drop the round 5 statement that Rest lose the cap clearly more often around destroyer smokes and smokes within 2 km. Ribbons: Drop as a per-smoke measure.')
W('')
W('**Changed from round 5:**')
W('')
rows = [['enemy took, 60 s grace: yes', gr[60]['round5_yes'], gr[60]['yes'], f'{gr[60]["yes"] - gr[60]["round5_yes"]:+d}'], ['enemy took, 60 s grace: share', f'{gr[60]["round5_pct"]}%', f'{gr[60]["pct"]}%', d(gr[60]['pct'], gr[60]['round5_pct'])],
        ['enemy took, no grace: yes', gr[0]['round5_yes'], gr[0]['yes'], f'{gr[0]["yes"] - gr[0]["round5_yes"]:+d}'], ['enemy took, no grace: share', f'{gr[0]["round5_pct"]}%', f'{gr[0]["pct"]}%', d(gr[0]['pct'], gr[0]['round5_pct'])],
        ['enemy took, 120 s grace: yes', gr[120]['round5_yes'], gr[120]['yes'], f'{gr[120]["yes"] - gr[120]["round5_yes"]:+d}'], ['enemy took, 120 s grace: share', f'{gr[120]["round5_pct"]}%', f'{gr[120]["pct"]}%', d(gr[120]['pct'], gr[120]['round5_pct'])],
        ['coverage: yes / no / not applicable', '184 / 889 / 474', f'{e["within_60"]} / {e["applicable"] - e["within_60"]} / {e["not_applicable"]}', ''],
        ['share of real flips the snapshot version misses', 'about 15% (estimate)', f'{ce["missed_pct"]}% enemy, {cw["missed_pct"]}% ours (measured)', '']]
for r in A['overall']['enemy_60']:
    o = r['round5']
    if not o: continue
    rows.append([f'{r["what"]}: share', f'{o["pct"]}% (n {o["n"]})', f'{r["pct"]}% (n {r["n"]})', d(r['pct'], o['pct'])])
    rows.append([f'{r["what"]}: Top 6 - Rest', gap(o), gap(r), d(r['gap'], o['gap'])])
for r in cd['kept']:
    o = r['round5']; rows.append([f'cap_defended kept, {r["what"]}', f'{o["pct"]}%; gap {gap(o)}', f'{r["pct"]}%; gap {gap(r)}', d(r['pct'], o['pct'])])
rows.append(['cap_defended kept, no grace / 120 s', '77.0% / 51.9%', f'{g_["0"]["pct"]}% / {g_["120"]["pct"]}%', f'{d(g_["0"]["pct"], 77.0)} / {d(g_["120"]["pct"], 51.9)}'])
rows.append(['nearest cap ours at activation: kept', '86.3% (n 694)', f'{b_["pct"]}% (n {b_["n"]})', d(b_['pct'], 86.3)])
for r in A['we_took']:
    o = r['round5']; rows.append([f'we took, {r["what"]}', f'{o["pct"]}%; gap {gap(o)}', f'{r["pct"]}%; gap {gap(r)}', d(r['pct'], o['pct'])])
for r in mc:
    if r.get('round5_pct') is not None and abs(r['pct'] - r['round5_pct']) >= 0.05: rows.append([f'{r["map"]} {r["cap"]}: enemy took', f'{r["round5_pct"]}%', f'{r["pct"]}% (n {r["n"]})', d(r['pct'], r['round5_pct'])])
rows.append(['ribbons', 'not in the batch', f'{rb["rows"]} ribbons, {rb["covered"]} smokes with a recording player covered', 'new'])
tab(['number', 'round 5', 'round 5b', 'difference'], rows)
W('Why: better data. The timeline has every owner change; round 5 only saw cap owners at the moments other smokes were laid or fully laid. Same definition, same nearest cap, same 60 s grace. '
  'Every share went up because flips after the last snapshot are now seen. The `cap_defended` follow-up also changed its start point slightly (from the first invaded moment instead of from activation; this gives the same count). '
  'Unchanged: the meaning of `cap_defended`, its rates (31.4% of smokes) and the distance facts, which use smoke fields only.')
W('')

# ------------------------------------------------------------------ C2
pa = {r['what']: r for r in B['pooled']['all']}; pr = {r['what']: r for r in B['pooled']['rest_vs_rest']}; nt = B['notes']; vr = B['vs_round5']
MORE = 'holds more caps than the enemy'; TWO = 'holds 2+ more caps than the enemy'
def ame(r, bt=False):
    if r.get('too_few'): return f'too few (n {r["n_holders"]})'
    if bt: return f'{r["ame_bt_pts"]:+.0f} ({iv(r["ame_bt_ci"], "{:+.0f}")})' + (' clear' if r['ame_bt_clear'] else '')
    return f'{r["actual_minus_expected_pts"]:+.0f} ({iv(r["ame_ci"], "{:+.0f}")})' + (' clear' if r['ame_clear'] else '')
def won(r): return f'{r["holder_wins"]}, {r["holder_win_pct"]:.0f}% ({r["holder_ci"][0]:.0f} to {r["holder_ci"][1]:.0f})'
def old(o):
    if not o: return 'not in round 5'
    if o.get('too_few'): return f'too few (n {o["n_holders"]})'
    return f'n {o["n_holders"]}, won {o["holder_wins"]} ({o["holder_win_pct"]:.0f}%), {ame(o)}'
W('### C2. Cap holder at exactly 8:00 and winning')
W('')
m_ = pa[MORE]; mr = pr[MORE]; t2 = pr[TWO]
lofA = next(r for r in B['maps']['Land of Fire']['all'] if r['what'].startswith('A')); lofB = next(r for r in B['maps']['Land of Fire']['all'] if r['what'].startswith('B'))
W(f'**Answer:** Same answer as round 5, now on all {nt["games"]} games that were still running at 8:00 instead of 154. No single cap clearly adds something beyond team strength in a way that holds up. Teams holding more caps than the enemy at exactly 8:00 won {m_["holder_win_pct"]:.0f}% '
  f'(the others {m_["not_win_pct"]:.0f}%), but only {m_["actual_minus_expected_pts"]:+.0f} points more than their strength predicts, and in Rest-vs-Rest games the edge is gone ({mr["holder_win_pct"]:.0f}%, {mr["actual_minus_expected_pts"]:+.0f} points). '
  f'The two middle caps on Land of Fire are still the only caps that stay above expectation. New from the timeline: {nt["more_caps_already_ahead_pct"]}% of the teams with more caps were already ahead on score, and cap leaders who were not ahead on score won only {nt["cap_leader_not_ahead"]["wins"]} of {nt["cap_leader_not_ahead"]["n"]}.')
W('')
W('**Numbers**')
W('')
cvg = B['coverage']
W(f'- Coverage: cap owners read from the timeline at exactly elapsed 480 s. {nt["games"]} of 171 games are in the tables; {B["short_games"]["games"]} ended before 8:00 and are kept apart. Round 5 had 154 (5 ended early, 12 had no snapshot within 60 s). In the tables / all: ' +
  ', '.join(f'{m} {v.get("covered", 0)}/{sum(v.values())}' for m, v in sorted(cvg.items())) + f'. Rest-vs-Rest games: {sum(v["rest_vs_rest_games"] for v in B["maps"].values())} (round 5: 76).')
W(f'- Against round 5, game by game: of the 154 games round 5 covered, the owners at 8:00 are identical in {vr["same_owners"]} and differ in {vr["differ"]} (the snapshot was up to 60 s away from 8:00). '
  f'{len(vr["clock_15min_games"])} games ({", ".join(vr["clock_15min_games"])}) ran on a 15-minute clock; round 5 worked out elapsed time as 20:00 minus the clock, so its "8:00" in those games was really 3:00. The timeline uses true elapsed seconds.')
W('- Cap roles (own side, enemy side, middle), the expected win rate and the Bradley-Terry check are exactly as in round 5 (favourite won 110 of 158 on the simple model, 128 of 164 on Bradley-Terry).')
W('')
W(f'All maps pooled, all {nt["games"]} games (last column: round 5 on 154 games):')
W('')
HD = ['what the team holds at 8:00', 'team-games', 'holders won (interval)', 'others won', 'strength predicts', 'actual - expected (interval)', 'Bradley-Terry check', 'round 5']
LAB = {'holds its own-side cap (maps that have one)': 'its own-side cap', 'holds the enemy-side cap (maps that have one)': 'the enemy-side cap', 'holds at least one middle cap': 'at least one middle cap', 'holds every middle cap': 'every middle cap',
       MORE: 'more caps than the enemy (reference)', TWO: '2+ more caps than the enemy'}
def c2r(r):
    if r.get('too_few'): return [LAB.get(r['what'], r['what']), r['n_holders'], 'too few', '', '', '', '', old(r.get('round5'))]
    return [LAB.get(r['what'], r['what']), f'{r["n_holders"]}{sm(r["n_holders"])}', won(r), f'{r["not_win_pct"]:.0f}%', r['expected_wins'], ame(r), ame(r, True), old(r.get('round5'))]
tab(HD, [c2r(r) for r in B['pooled']['all']])
W(f'(a) Rest-vs-Rest games only ({sum(v["rest_vs_rest_games"] for v in B["maps"].values())}):')
W('')
tab(HD, [c2r(r) for r in B['pooled']['rest_vs_rest']])
W('Per map, caps whose holders did clearly better than strength predicts, now or in round 5 (every other cap on every map has an interval including zero; all rows are in `out-c2.md`):')
W('')
rows = []
for m, v in B['maps'].items():
    rv = {r['what']: r for r in v['rest_vs_rest']}
    for r in v['all']:
        if r['what'] == MORE or r.get('too_few'): continue
        o = r.get('round5')
        if r['ame_clear'] or (o and o.get('ame_clear')):
            x = rv.get(r['what'], {})
            rows.append([f'{m} {r["what"]}', f'{r["n_holders"]}{sm(r["n_holders"])}', won(r), f'{r["not_win_pct"]:.0f}%', r['expected_wins'], ame(r), ame(r, True),
                         (f'{x["holder_wins"]} of {x["n_holders"]}{sm(x["n_holders"])}, {ame(x)}' if x and not x.get('too_few') else 'too few'), old(o)])
    for r in v['rest_vs_rest']:
        if r['what'] == MORE or r.get('too_few'): continue
        o = r.get('round5')
        if r['ame_clear'] or (o and o.get('ame_clear')):
            rows.append([f'{m} {r["what"]}, Rest-vs-Rest games', f'{r["n_holders"]}{sm(r["n_holders"])}', won(r), f'{r["not_win_pct"]:.0f}% (n {r["n_not"]})', r['expected_wins'], ame(r), ame(r, True), 'this row', old(o)])
tab(['map, cap', 'holder team-games', 'holders won', 'others won', 'strength predicts', 'actual - expected', 'Bradley-Terry check', 'Rest-vs-Rest only', 'round 5'], rows)
ncl = sum(1 for v in B['maps'].values() for r in v['all'] if r['what'] != MORE and not r.get('too_few') and r['ame_clear'])
ncb = sum(1 for v in B['maps'].values() for r in v['all'] if r['what'] != MORE and not r.get('too_few') and r['ame_clear'] and r['ame_bt_clear'])
ntest = sum(1 for v in B['maps'].values() for r in v['all'] if r['what'] != MORE and not r.get('too_few'))
W(f'- Multiplicity: {ntest} map-and-cap rows tested; fewer than one clear positive row is expected by luck. {ncl} came out clear on the simple model, {ncb} on both models (Land of Fire B). None of the middle caps is clear in Rest-vs-Rest games (small n everywhere). Land of Fire A and B share the same games.')
W('- "More caps than the enemy" per map (all games): ' + '; '.join(
    (f'{m} {r["holder_wins"]} of {r["n_holders"]}{sm(r["n_holders"])}, {ame(r)}' if not r.get('too_few') else f'{m} too few (n {r["n_holders"]})') + f' [round 5: {old(r.get("round5"))}]'
    for m, v in B['maps'].items() for r in v['all'] if r['what'] == MORE) + '.')
lc = next(r for r in B['maps']['Loop']['rest_vs_rest'] if r['what'].startswith('C'))
W(f'- Loop, Rest-vs-Rest: teams holding cap C won {lc["holder_wins"]} of {lc["n_holders"]}{sm(lc["n_holders"])} ({ame(lc)}); round 5 had 1 of 9 and called it clear. It is no longer clear.')
W('')
W('New reference rows from the timeline (all games; the same teams, other moments):')
W('')
ra = B['reference']['all']; rrv = {r['what']: r for r in B['reference']['rest_vs_rest']}
tab(['what', 'team-games', 'they won (interval)', 'the other side won', 'strength predicts', 'actual - expected (interval)', 'Bradley-Terry check', 'Rest-vs-Rest only'],
    [[r['what'], r['n_holders'], won(r), f'{r["not_win_pct"]:.0f}%', r['expected_wins'], ame(r), ame(r, True), f'{rrv[r["what"]]["holder_wins"]} of {rrv[r["what"]]["n_holders"]}, {ame(rrv[r["what"]])}'] for r in ra])
ts = B['time_share']
W(f'- Time-weighted: winners held more caps than the enemy for {ts["winners_mean_pct"]}% of the first 8 minutes on average, losers for {ts["losers_mean_pct"]}%; the two sides were level on caps {ts["level_mean_pct"]}% of the time. '
  f'The side that led on caps for longer won {ra[3]["holder_win_pct"]:.0f}% and beat its strength by {ame(ra[3])}; in Rest-vs-Rest games {ame(rrv[ra[3]["what"]])}. {ts["games_running_at_10"]} of {nt["games"]} games were still running at 10:00.')
W(f'- Holding a cap at 8:00 is partly a result of already winning. Teams with more caps at 8:00 were already ahead on score in {nt["more_caps_already_ahead"]} of {nt["more_caps_n"]} ({nt["more_caps_already_ahead_pct"]}%; median lead {nt["more_caps_median_lead"]:+.0f} points). '
  f'Cap leaders who were also ahead on score won {nt["cap_leader_ahead"]["wins"]} of {nt["cap_leader_ahead"]["n"]}; cap leaders level or behind on score won {nt["cap_leader_not_ahead"]["wins"]} of {nt["cap_leader_not_ahead"]["n"]}. '
  f'The team ahead on score at 8:00 won {nt["score_leader_wins"]} of {nt["score_leader_n"]} ({nt["score_leader_win_pct"]}%). {nt["level_on_caps_games"]} of {nt["games"]} games were level on caps. '
  f'In the {nt["top_vs_rest"]["games"]} Top 6 vs Rest games the Top 6 clan held more caps in {nt["top_vs_rest"]["top_more"]}, fewer in {nt["top_vs_rest"]["top_fewer"]}, and won {nt["top_vs_rest"]["top_won"]}.')
sg = B['short_games']
W(f'- Separate row, not in any table above: the {sg["games"]} games that ended before 8:00, state at the end. The team with more caps at the end won {sg["more_caps_won"]} of {sg["more_caps_at_end"]}. These are routs; they say nothing about caps.')
W(f'- Check: the number of games with a cap leader at 8:00 counted a second way, straight from the timeline rows: {nt["second_way_cap_leader_games"]} (table: {nt["more_caps_n"]}).')
W('')
W(f'**Top 6 or Shared:** Shared. In Rest-vs-Rest games holding more caps is worth {ame(mr)} points over expected. Only a 2+ cap lead stays clear there ({ame(t2)}, n {t2["n_holders"]}; Bradley-Terry {ame(t2, True)}).')
W('')
W('**Clans:** not a spot item.')
W('')
W('**Could not be done / proxy:** Nothing is missing any more: every game has its cap owners at the exact second. The data still cannot separate "holding the cap helped" from "the winning team held the cap"; the score at 8:00 shows most cap leaders were already ahead.')
W('')
W(f'**Verdict:** Keep (as a caution). Land of Fire middle caps A and B: Lead for the Land of Fire page, with the small-n warning (B: {ame(lofB)}, Bradley-Terry {ame(lofB, True)}; A: {ame(lofA)}).')
W('')
W('**Changed from round 5:**')
W('')
rows = [['games in the tables', 154, nt['games'], f'{nt["games"] - 154:+d}'], ['Rest-vs-Rest games', 76, sum(v['rest_vs_rest_games'] for v in B['maps'].values()), f'{sum(v["rest_vs_rest_games"] for v in B["maps"].values()) - 76:+d}'],
        ['games level on caps at 8:00', '63 of 154', f'{nt["level_on_caps_games"]} of {nt["games"]}', ''],
        ['cap leaders already ahead on score', '66 of 91 (73%), median +95', f'{nt["more_caps_already_ahead"]} of {nt["more_caps_n"]} ({nt["more_caps_already_ahead_pct"]}%), median {nt["more_caps_median_lead"]:+.0f}', ''],
        ['score leader at 8:00 won', '120 of 153 (78%)', f'{nt["score_leader_wins"]} of {nt["score_leader_n"]} ({nt["score_leader_win_pct"]}%)', ''],
        ['Top 6 vs Rest games: Top 6 more / fewer caps / won', '53 games: 30 / 7 / 46', f'{nt["top_vs_rest"]["games"]} games: {nt["top_vs_rest"]["top_more"]} / {nt["top_vs_rest"]["top_fewer"]} / {nt["top_vs_rest"]["top_won"]}', '']]
def mv(scope, r):
    o = r.get('round5')
    if not o: return
    if r.get('too_few') or o.get('too_few'):
        if r.get('too_few') != o.get('too_few') or r['n_holders'] != o['n_holders']: rows.append([f'{scope}: {LAB.get(r["what"], r["what"])}', old(o), 'too few (n %d)' % r['n_holders'] if r.get('too_few') else f'n {r["n_holders"]}, won {r["holder_wins"]} ({r["holder_win_pct"]:.0f}%), {ame(r)}', ''])
        return
    rows.append([f'{scope}: {LAB.get(r["what"], r["what"])}', old(o), f'n {r["n_holders"]}, won {r["holder_wins"]} ({r["holder_win_pct"]:.0f}%), {ame(r)}',
                 f'n {r["n_holders"] - o["n_holders"]:+d}, wins {r["holder_wins"] - o["holder_wins"]:+d}, {r["actual_minus_expected_pts"] - o["actual_minus_expected_pts"]:+.0f} pts'])
for r in B['pooled']['all']: mv('pooled, all games', r)
for r in B['pooled']['rest_vs_rest']: mv('pooled, Rest-vs-Rest', r)
for m, v in B['maps'].items():
    for r in v['all']: mv(f'{m}, all games', r)
    for r in v['rest_vs_rest']: mv(f'{m}, Rest-vs-Rest', r)
tab(['number', 'round 5 (154 games, snapshot within 60 s)', 'round 5b (exact 8:00, timeline)', 'difference'], rows)
lost = [f'{x["scope"]} {x["what"]}' + (' (Rest-vs-Rest)' if x['games'] == 'rest_vs_rest' else '') for x in B['moved'] if x['old'] and x['old'].get('ame_clear') and not x['new'].get('ame_clear')]
gain = [f'{x["scope"]} {x["what"]}' + (' (Rest-vs-Rest)' if x['games'] == 'rest_vs_rest' else '') for x in B['moved'] if x['old'] and not x['old'].get('ame_clear') and x['new'].get('ame_clear')]
W('Rows that were clear in round 5 and are not now: ' + ('; '.join(lost) or 'none') + '. Rows that became clear: ' + ('; '.join(gain) or 'none') + '.')
W('')
W('Why: better data, same definition. Twelve games with no snapshot near 8:00 are now included, the owner is read at the exact second instead of up to 60 s away, and two games on a 15-minute clock are read at the right moment. '
  'Intervals also move by a point or so between runs of the same data because they come from resampling. No conclusion changed: every pooled row moved by 3 points or less.')
W('')
open(os.path.join(H, 'FINDINGS-N1.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# ------------------------------------------------------------------ caps.json
json.dump(dict(batch='output/20261117-230933', source='cap timeline (caps_timeline.csv), score.csv, ribbons.csv', c1=A, c2=B), open(os.path.join(H, 'caps.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ CHECK
K = ['# CHECK-N1: where every number in FINDINGS-N1.md comes from', '',
     'All numbers are computed by `n1_c1.py` (C1, ribbons) and `n1_c2.py` (C2), stored in `c1.json` / `c2.json` (merged into `caps.json`), printed in `out-c1.md` / `out-c2.md`, and placed into the findings text by `n1_findings.py`. Nothing is typed by hand except the round 5 reference values marked below. FINDINGS rounds from the one-decimal values stored in the json; the out files round from full precision, so an interval end can differ by 1 in the last digit between the two.', '',
     '| number or table | script | where (json path; section of the out file) |', '|---|---|---|']
def ck(a, b, c): K.append(f'| {a} | {b} | {c} |')
ck(f'enemy took: {e["during"]} during, {e["after_only"]} only after, {e["within_60"]} within 60 s of {e["applicable"]}', 'n1_c1.py', '`c1.three_ways.enemy`; out-c1.md "three ways"')
ck(f'we took: {tw["we"]["during"]} / {tw["we"]["after_only"]} / {tw["we"]["within_60"]} of {tw["we"]["applicable"]}', 'n1_c1.py', '`c1.three_ways.we`')
ck('grace 0 / 10 / 30 / 60 / 120 s rows', 'n1_c1.py', '`c1.grace` (round 5 values read from round5/part-c1/caps.json `enemy_took.grace`)')
ck(f'cross-tab snapshot vs timeline; missed {ce["snapshot_missed"]} of {ce["timeline_yes"]} ({ce["missed_pct"]}%); wrong the other way {ce["snapshot_wrong_other_way"]}', 'n1_c1.py', '`c1.crosstab.enemy` (old values are `s["enemy_took"]` from r5lib on the same smokes)')
ck(f'missed by group: Top 6 {ce["by_group"]["top"]["missed"]} of {ce["by_group"]["top"]["flips"]}, Rest {ce["by_group"]["rest"]["missed"]} of {ce["by_group"]["rest"]["flips"]}', 'n1_c1.py', '`c1.crosstab.enemy.by_group`')
ck(f'we took cross-tab: missed {cw["snapshot_missed"]} of {cw["timeline_yes"]}', 'n1_c1.py', '`c1.crosstab.we`')
ck(f'second computation: {A["checks"]["second_way_mismatch"]} mismatches; owner at activation differs in {A["checks"]["owner_at_activation_mismatch"]}; frame letters {A["checks"]["frame_letter_mismatch"]} mismatches', 'n1_c1.py', '`c1.checks`; function `raw_took`')
ck(f'cap_won cross-check {A["cap_won_crosscheck"]["timeline60_yes"]} of {A["cap_won_crosscheck"]["n"]}', 'n1_c1.py', '`c1.cap_won_crosscheck`')
ck('summary table (9 groups), 60 s and strictly during', 'n1_c1.py', '`c1.overall.enemy_60`, `c1.overall.enemy_during`; each record carries `round5` copied from the round 5 caps.json')
ck('by map and cap (26 rows)', 'n1_c1.py', '`c1.by_map_cap`')
ck('we took table', 'n1_c1.py', '`c1.we_took`')
ck(f'cap_defended: {cd["n"]} smokes, kept {g_["0"]["kept"]} / {g_["60"]["kept"]} / {g_["120"]["kept"]}; kept tables', 'n1_c1.py', '`c1.cap_defended.grace`, `.kept`, `.kept_strict`, `.last_owner`, `.baseline_ours_kept`. Round 5 counts 374 / 294 / 252 and 86.3% are typed from round 5 FINDINGS.md C1')
ck(f'invaders: tables; median {inv["median_invaded_s"]} s', 'n1_c1.py', '`c1.invaded.groups`, `.kept`, `.median_invaded_s`')
ck(f'ribbons: {rb["rows"]} rows, {rb["recorders"]} recorders, {rb["covered"]} smokes covered, {rb["inside_or_smoker"]} smoker or inside, {rb["near_2km"]} within 2 km', 'n1_c1.py', '`c1.ribbons` (recorder = `self_entity` in each run\'s damage_spike.json)')
ck('ribbon tables strict / loose / Top 6 vs Rest / Defended vs kept', 'n1_c1.py', '`c1.ribbons.strict`, `.loose`, `.top_vs_rest`, `.defended_vs_kept`')
ck(f'ribbons vs timeline: Captured {tc["captured_on_flip"]} of {tc["captured"]}; Defended {tc["defended_while_any_cap_invaded"]} of {tc["defended"]}', 'n1_c1.py', '`c1.ribbons.timeline_check`, `.captured_vs_we_took`')
ck('enemy-took.csv (1,547 rows)', 'n1_c1.py', 'written near the end of the C1 part')
ck(f'C2 coverage: {nt["games"]} games in tables, {sg["games"]} ended before 8:00', 'n1_c2.py', '`c2.coverage`, `c2.short_games`; game end = last row of score.csv')
ck(f'C2 against round 5 game by game: {vr["same_owners"]} same, {vr["differ"]} differ; 15-minute clock games', 'n1_c2.py', '`c2.vs_round5` (round 5 holders recomputed with r5lib `cap_holders`)')
ck('C2 pooled tables', 'n1_c2.py', '`c2.pooled.all`, `c2.pooled.rest_vs_rest` (function `c2row`, copied from round 5); `round5` on each record from round 5 caps.json')
ck('C2 per map rows', 'n1_c2.py', '`c2.maps.<map>.all` / `.rest_vs_rest`')
ck('C2 reference rows 5:00, 8:00, 10:00, time-weighted', 'n1_c2.py', '`c2.reference`, `c2.time_share` (functions `lead_at`, `time_shares`)')
ck(f'score lead of cap leaders {nt["more_caps_already_ahead"]} of {nt["more_caps_n"]}; score leader won {nt["score_leader_wins"]} of {nt["score_leader_n"]}; cap leader not ahead {nt["cap_leader_not_ahead"]["wins"]} of {nt["cap_leader_not_ahead"]["n"]}', 'n1_c2.py', '`c2.notes` (score from `g.score_at(team, 480)`); round 5 values 66 of 91, 120 of 153, 63 of 154, 53 / 30 / 7 / 46 typed from round 5 FINDINGS.md C2')
ck(f'second count of games with a cap leader: {nt["second_way_cap_leader_games"]}', 'n1_c2.py', '`c2.notes.second_way_cap_leader_games`')
ck('"Changed from round 5" tables', 'n1_findings.py', 'built by comparing each record with its `round5` copy')
ck('figures n1-enemy-took-snapshot-vs-timeline, n1-caps-8min', 'n1_c1.py, n1_c2.py', 'round5b/figures/')
open(os.path.join(H, 'CHECK-N1.md'), 'w', encoding='utf-8').write('\n'.join(K) + '\n')
print('wrote FINDINGS-N1.md', len(L), 'lines; CHECK-N1.md; caps.json')
