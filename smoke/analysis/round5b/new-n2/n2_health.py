# Round 5b, worker n2, step 1: real health against the round 5 estimate, and the like-with-like baselines redone.
# Run: python -I -X utf8 n2_health.py     Writes out-health.json and out-health.md
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n2lib import *
random.seed(11)
PR = build_pairs()
L = []; P = lambda *a: (L.append(' '.join(str(x) for x in a)), print(' '.join(str(x) for x in a)))
J = {}
CORE = [p for p in PR if p['how'] in ('smoker', 'inside', 'behind')]
BAD = [p for p in CORE if not p['ok']]
OK = [p for p in CORE if p['ok']]
for p in OK:
    p['hurt_w'] = p['died_win'] or p['net'] >= HURT_SHARE          # the round 5b definition
    p['hurt_w_pt'] = p['died_win'] or p['trough'] >= HURT_SHARE     # peak-to-trough version, shown beside
    p['old'] = p['x']['hurt']
one_sided = [s for s in S if TL(s['game']).one_sided]
J['excluded'] = dict(pairs=len(BAD), smokes_in_single_replay_game=len(one_sided), note='ships of the team without a replay in the single-replay game: health blank or stale')
unc = sum(1 for p in CORE if p['x'].get('uncovered'))
J['excluded'].update(bad_smokes=len({id(p['s']) for p in BAD}), uncovered_smokers=unc)
P(f'Ships at risk (smoker, inside, behind): {len(CORE)} ship-smoke pairs. {unc} of them are smokers the batch never counted as concealed by their own smoke; they stay in so that rates are per 100 smokes, as in round 5. '
  f'Excluded for incomplete health: {len(BAD)} pairs (the KSC smoker in {len({id(p["s"]) for p in BAD})} smokes of the single-replay game KSC vs -BN-; that game has {len(one_sided)} smokes, the -BN- ones are complete and stay in).')
J['no_dispersal_time'] = sum(not s['e1_known'] for s in S); J['smokes'] = len(S)
P(f'Smokes with no dispersal time in the replay (end estimated as activation + emission + puff life): {sum(not s["e1_known"] for s in S)} of {len(S)}.')

GROUPS = {
    'dd': ('destroyer smoker (destroyer smokes)', [p for p in OK if p['how'] == 'smoker' and p['s']['cls'] == 'destroyer']),
    'cr_dd': ('sheltering cruisers in destroyer smokes', [p for p in OK if p['cls'] == 'cruiser' and p['how'] in ('inside', 'behind') and p['s']['cls'] == 'destroyer']),
    'cr': ('sheltering cruisers, any smoke', [p for p in OK if p['cls'] == 'cruiser' and p['how'] in ('inside', 'behind')]),
    'all': ('every covered ship', OK),
}

# ---- 1. old estimate against real health, same pairs, same death list (batch deaths), so only the health source differs
P('\n## 1. Old estimate against real health (same ship-smoke pairs, same death list)')
rows = []; J['agreement'] = {}
for k, (lab, v) in GROUPS.items():
    c = C((p['old'], p['hurt']) for p in v)
    both, neither, new, lost = c[(True, True)], c[(False, False)], c[(False, True)], c[(True, False)]
    J['agreement'][k] = dict(label=lab, n=len(v), both=both, neither=neither, new_flag=new, lost_flag=lost, agree_pct=r1(100 * (both + neither) / len(v)), old_flags=both + lost, real_flags=both + new)
    rows.append([lab, len(v), both + lost, both + new, both, new, lost, f'{100*(both+neither)/len(v):.1f}%'])
P(md_table(['who', 'pairs', 'hurt, old estimate', 'hurt, real health', 'both', 'new flag (real only)', 'flag lost (old only)', 'agree'], rows))
new = [p for p in OK if p['hurt'] and not p['old']]; lost = [p for p in OK if p['old'] and not p['hurt']]
out_new = sum(1 for p in new if p['drop_pos'] and not in_smoke(p['s'], p['drop_pos']))
heal_lost = sum(1 for p in lost if p['trough'] >= HURT_SHARE)
est_lost = sum(1 for p in lost if p['trough'] < HURT_SHARE and p['x']['taken'] < HURT_SHARE * p['maxhp'])
J['flip_reasons'] = dict(new=len(new), new_biggest_hit_outside_outline=out_new, lost=len(lost), lost_healed_back=heal_lost, lost_estimate_too_low=est_lost, lost_other=len(lost) - heal_lost - est_lost)
P(f'Why flags flip. New flags ({len(new)}): the old number counted only damage taken while the ship was covered; the real number counts all health lost between activation and dispersal. '
  f'In {out_new} of {len(new)} the biggest single hit landed outside the smoke outline. '
  f'Lost flags ({len(lost)}): {heal_lost} healed back (the fall from high to low was a third or more, the net loss was not); {est_lost} because the estimate of full health was too low (damage taken was under a third of real full health); {len(lost)-heal_lost-est_lost} other (damage the log counted that did not reduce health by a third over the window).')
# hp_est against real max health
P('\nEstimate of full health against real full health (ratio estimate / real, one value per ship-smoke pair):')
rows = []; J['hp_est'] = {}
for cl in ('destroyer', 'cruiser', 'battleship'):
    v = [p['x']['hp_est'] / p['maxhp'] for p in OK if p['cls'] == cl and p['x']['hp_est']]
    J['hp_est'][cl] = dict(n=len(v), median=r1(med(v), 3), q25=r1(q(v, .25), 3), q75=r1(q(v, .75), 3), min=r1(min(v), 2), max=r1(max(v), 2), within_10pct=r1(pct(v, lambda x: abs(x - 1) <= .1)))
    rows.append([cl, len(v), f'{med(v):.2f}', f'{q(v,.25):.2f} to {q(v,.75):.2f}', f'{min(v):.2f} to {max(v):.2f}', f'{pct(v, lambda x: abs(x-1) <= .1):.0f}%'])
P(md_table(['class', 'pairs', 'median ratio', 'middle half', 'range', 'within 10% of real'], rows))
ships = collections.defaultdict(list)
for p in OK:
    if p['x']['hp_est']: ships[(p['cls'], p['ship'])].append(p['x']['hp_est'] / p['maxhp'])
worst = sorted(((med(v), k, len(v)) for k, v in ships.items() if len(v) >= 15), key=lambda x: -abs(x[0] - 1))[:8]
J['hp_est_worst_ships'] = [dict(ship=k[1], cls=k[0], n=n, median_ratio=r1(m, 2)) for m, k, n in worst]
P('Furthest off (ships with 15+ pairs): ' + ', '.join(f'{k[1]} {m:.2f} (n {n})' for m, k, n in worst))

# ---- 2. deaths: the batch list against the tracks
P('\n## 2. Deaths: batch list against tracks')
bd = [p for p in CORE if p['died']]; wd = [p for p in CORE if p['died_win']]
J['deaths_check'] = dict(batch=len(bd), batch_confirmed_by_track=sum(p['died_win'] for p in bd), track_window=len(wd), track_only=sum(not p['died'] for p in wd),
                         track_only_by_how=dict(C(p['how'] for p in wd if not p['died'])),
                         track_only_inside_outline=sum(1 for p in wd if not p['died'] and p['death_pos'] and in_smoke(p['s'], p['death_pos'])),
                         track_only_detected_at_death=sum(1 for p in wd if not p['died'] and p['tr'].det[p['tr'].idx(p['td'] - STEP)]))
d = J['deaths_check']
P(f'Batch smoke deaths among covered ships (smoker, inside, behind): {d["batch"]}; the track shows the death inside the smoke window (activation to 20 s after dispersal) for {d["batch_confirmed_by_track"]} '
  f'(the other {d["batch"]-d["batch_confirmed_by_track"]} are in a smoke whose dispersal time is estimated). '
  f'Covered ships whose track shows a death in that window: {d["track_window"]}; not in the batch list: {d["track_only"]} ({d["track_only_by_how"]}). '
  f'Of those {d["track_only"]}, {d["track_only_inside_outline"]} died inside the smoke outline and {d["track_only_detected_at_death"]} were detected at the last sample. '
  f'The batch list needs the ship to be concealed by the smoke and then detected at a flag change before it died, so it leaves out ships that were never concealed (already lit when they smoked and lit throughout), ships that died unseen, and ships that left.')

# ---- 3. baselines
P('\n## 3. Like-with-like baselines')
MEAS = [('died, batch list (round 5 measure)', lambda p: p['died']), ('died, track (activation to 20 s after dispersal)', lambda p: p['died_win']),
        ('died or hurt, old estimate (round 5 measure)', lambda p: p['old']), ('died or hurt, real health, batch deaths', lambda p: p['hurt']),
        ('died or hurt, real health, track deaths (round 5b definition)', lambda p: p['hurt_w']), ('same, peak-to-trough health loss', lambda p: p['hurt_w_pt'])]
J['baselines'] = {}
for k in ('dd', 'cr_dd', 'cr'):
    lab, v = GROUPS[k]; rows = []; J['baselines'][k] = dict(label=lab, n=len(v), n_top6=sum(p['s']['grp'] == 'top' for p in v), n_rest=sum(p['s']['grp'] == 'rest' for p in v), measures=[])
    for name, f in MEAS:
        st = lambda ps, f=f: 100 * sum(1 for p in ps if f(p)) / len(ps) if len(ps) >= MIN_N else None
        a = st(v); lo, hi = clus_ci(v, st); t, r = st([p for p in v if p['s']['grp'] == 'top']), st([p for p in v if p['s']['grp'] == 'rest']); g = grp_ci(v, st)
        J['baselines'][k]['measures'].append(dict(measure=name, count=sum(1 for p in v if f(p)), per_100=r1(a), ci=[r1(lo), r1(hi)], top6=r1(t), rest=r1(r), gap_ci=[r1(g[0]), r1(g[1])], clear=bool(g[0] is not None and g[0] * g[1] > 0)))
        rows.append([name, sum(1 for p in v if f(p)), f'{a:.1f} [{lo:.1f} to {hi:.1f}]', f'{t:.1f}', f'{r:.1f}', fci(g)])
    b = J['baselines'][k]
    P(f'\n{lab}: {len(v)} at risk (Top 6 {b["n_top6"]}, Rest {b["n_rest"]})')
    P(md_table(['measure', 'count', 'per 100 [95%]', 'Top 6', 'Rest', 'Top 6 minus Rest'], rows))
# round 5 pool check without the exclusion
ddall = [p for p in CORE if p['how'] == 'smoker' and p['s']['cls'] == 'destroyer']
J['check_r5'] = dict(dd_smokes=len(DD), dd_smoker_pairs_all=len(ddall), d_smoker_per_100_smokes=r1(100 * sum(s['d_smoker'] for s in DD) / len(DD)), hurt_smoker_per_100_smokes=r1(100 * sum(s['hurt_smoker'] for s in DD) / len(DD)),
                     cr_pool=sum(s['n_cr_in'] for s in S), cr_died=r1(100 * sum(min(s['d_cr'], s['n_cr_in']) for s in S) / sum(s['n_cr_in'] for s in S)), cr_hurt=r1(100 * sum(s['hurt_cr'] for s in S) / sum(s['n_cr_in'] for s in S)))
c = J['check_r5']
P(f'\nCheck against round 5 with the round 5 fields on this batch: destroyer smoker died {c["d_smoker_per_100_smokes"]} and died-or-hurt {c["hurt_smoker_per_100_smokes"]} per 100 destroyer smokes ({c["dd_smokes"]} smokes; {c["dd_smoker_pairs_all"]} have the smoker listed as covered); '
  f'sheltering cruisers {c["cr_died"]} and {c["cr_hurt"]} per 100 ({c["cr_pool"]} cruisers). Round 5 printed 6.4 / 15.5 and 8.0 / 22.0.')
# health loss distribution
P('\nHealth lost while the smoke stood (share of full health, real):')
rows = []; J['loss'] = {}
for k in ('dd', 'cr'):
    lab, v = GROUPS[k]; net = [100 * p['net'] for p in v]; tro = [100 * p['trough'] for p in v]
    J['loss'][k] = dict(mean_net=r1(mean(net)), median_net=r1(med(net)), mean_trough=r1(mean(tro)), none_pct=r1(pct(net, lambda x: x < 1)), third_net=r1(pct(net, lambda x: x >= 100 / 3)), third_trough=r1(pct(tro, lambda x: x >= 100 / 3)))
    rows.append([lab, len(v), f'{mean(net):.1f}%', f'{mean(tro):.1f}%', f'{pct(net, lambda x: x < 1):.0f}%', f'{pct(net, lambda x: x >= 100/3):.1f}%', f'{pct(tro, lambda x: x >= 100/3):.1f}%'])
P(md_table(['who', 'n', 'mean net loss', 'mean high-to-low fall', 'lost under 1%', 'net loss 1/3+', 'high-to-low fall 1/3+'], rows))
dump('out-health.json', J)
open(os.path.join(HERE_, 'out-health.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
