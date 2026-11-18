# A3. Somers vs Gearing inside Top 6 and inside Rest, both death metrics (all ships, the smoker, sheltering cruisers).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlib import *
SO = [s for s in DD if s['ship'] == 'Somers']; GE = [s for s in DD if s['ship'] == 'Gearing']
J = dict(n_somers=len(SO), n_gearing=len(GE), clans=dict(Somers=clan_counts(SO), Gearing=clan_counts(GE)))
T1 = []
for sc, f in SCOPES:
    for ship, ss in (('Somers', f(SO)), ('Gearing', f(GE))):
        T1.append(dict(scope=sc, ship=ship, n=len(ss), note=note(len(ss)), rates=death_rates(ss), **{st.key: val(ss, st, True) for st in DEATHS6}))
J['rates'] = T1
T2 = [dict(scope=sc, n_a=len(f(SO)), n_b=len(f(GE)), **{st.key: gap_ab(f(SO), f(GE), st) for st in DEATHS6}) for sc, f in SCOPES]
J['somers_minus_gearing'] = T2
T3 = [dict(ship=ship, **{st.key: gap_tr(ss, st) for st in DEATHS6}) for ship, ss in (('Somers', SO), ('Gearing', GE))]
J['top6_minus_rest'] = T3
# Rest Gearing by clan, and leaving one clan out
RG = RESTS(GE)
J['rest_gearing_by_clan'] = {c: dict(n=len(v), died=sum(s['died'] for s in v if s['died_ok']), caught=sum(s['caught'] for s in v)) for c, v in sorted(by(RG, 'team').items(), key=lambda kv: -len(kv[1]))}
J['rest_gearing_leave_one_out'] = [dict(clan=c, died100=r1(died100([s for s in RG if s['team'] != c])), caught100=r1(caught100([s for s in RG if s['team'] != c]))) for c in sorted({s['team'] for s in RG})]
loo_d = [x['died100'] for x in J['rest_gearing_leave_one_out']]; loo_c = [x['caught100'] for x in J['rest_gearing_leave_one_out']]

gT, gR, gA = find(T2, scope='Top 6'), find(T2, scope='Rest'), find(T2, scope='All')
r = lambda sc, ship: find(T1, scope=sc, ship=ship)
p = lambda x: fv(x)
M = ['### A3. Somers vs Gearing inside Top 6 and inside Rest', '']
M.append(f"**Answer:** Inside the Top 6 the two ships lose about the same: died {p(r('Top 6', 'Somers')['died100']['value'])} (Somers) vs {p(r('Top 6', 'Gearing')['died100']['value'])} (Gearing) per 100, "
         f"caught {p(r('Top 6', 'Somers')['caught100']['value'])} vs {p(r('Top 6', 'Gearing')['caught100']['value'])}. Inside the Rest the Gearing loses more: died {p(r('Rest', 'Somers')['died100']['value'])} vs {p(r('Rest', 'Gearing')['died100']['value'])} "
         f"(gap {fdiff(gR['died100'])}), caught {p(r('Rest', 'Somers')['caught100']['value'])} vs {p(r('Rest', 'Gearing')['caught100']['value'])} (gap {fdiff(gR['caught100'])}). "
         f"Both metrics agree (caught: {clear_word(gR['caught100'])}; died: {clear_word(gR['died100'])}), and the extra loss is the smoker itself, not the sheltering cruisers "
         f"(smoker died {fdiff(gR['died_smoker100'])}, cruisers died {fdiff(gR['died_cr100'])}). The gap goes with who sails the Gearing, not with the ship.")
M.append('')
M.append(f"**Numbers:** {len(SO)} Somers smokes ({len(TOPS(SO))} Top 6, {len(RESTS(SO))} Rest) and {len(GE)} Gearing smokes ({len(TOPS(GE))} Top 6, {len(RESTS(GE))} Rest). {DIED_NOTE} "
         'Smoker rates are per 100 smokes; cruiser rates are per 100 sheltering cruisers (n = cruisers).')
M.append('')
M.append('Table 1. Deaths per 100 by ship and group [95% interval].')
M.append(md_table(['group', 'ship', 'n', 'died: all', 'caught: all', 'died: smoker', 'caught: smoker', 'died: cruisers (n)', 'caught: cruisers (n)', 'note'],
                  [[x['scope'], x['ship'], x['n'], fvci(x['died100']), fvci(x['caught100']), fvci(x['died_smoker100']), fvci(x['caught_smoker100']),
                    f"{fvci(x['died_cr100'])} ({x['died_cr100']['n']})", f"{fvci(x['caught_cr100'])} ({x['caught_cr100']['n']})", x['note']] for x in T1]))
M.append('')
M.append('Table 2. Somers minus Gearing inside each group (difference, 95% interval; * = clear).')
M.append(md_table(['group', 'n Somers / Gearing'] + [st.label for st in DEATHS6], [[x['scope'], f"{x['n_a']} / {x['n_b']}"] + [fdiff(x[st.key]) for st in DEATHS6] for x in T2]))
M.append('')
M.append('Table 3. Top 6 minus Rest on each ship (difference, 95% interval; * = clear).')
M.append(md_table(['ship'] + [st.label for st in DEATHS6], [[x['ship']] + [fdiff(x[st.key]) for st in DEATHS6] for x in T3]))
M.append('')
M.append(f"Rest Gearing, leaving one clan out at a time: died per 100 stays between {min(loo_d):.1f} and {max(loo_d):.1f}, caught between {min(loo_c):.1f} and {max(loo_c):.1f}. "
         'By clan (n smokes, died, caught): ' + ', '.join(f"{c} {v['n']}/{v['died']}/{v['caught']}" for c, v in J['rest_gearing_by_clan'].items()) + '.')
M.append('')
tG, tS = find(T3, ship='Gearing'), find(T3, ship='Somers')
M.append(f"**Top 6 or Shared:** Top 6. On the Gearing, Top 6 minus Rest is died {fdiff(tG['died100'])} and caught {fdiff(tG['caught100'])}; on the Somers it is died {fdiff(tS['died100'])} and caught {fdiff(tS['caught100'])}. "
         'The Rest lose more ships around their Gearing smokes; the Somers numbers are close in both groups.')
M.append('')
M.append(f"**Clans:** Somers: {J['clans']['Somers']}. Gearing: {J['clans']['Gearing']}.")
M.append('')
M.append('**Verdict:** Keep.')
M.append('')
o = old('out-a3.json'); CH = []
oname = {'died100': 'any death per 100 smokes', 'died_smoker100': 'smoker died per 100 smokes', 'died_cr100': 'cruiser died per 100 sheltering cruisers'}
for sc, osc in (('Top 6', 'Top 6 only'), ('Rest', 'Rest only')):
    for dk, ck, lab in (('died100', 'caught100', 'all ships'), ('died_smoker100', 'caught_smoker100', 'smoker'), ('died_cr100', 'caught_cr100', 'sheltering cruisers')):
        x = next(q_ for q_ in o['by_group'] if q_['scope'] == osc and q_['stat'] == oname[dk])
        for ship, k in (('Somers', 'a'), ('Gearing', 'b')):
            CH.append(chg_row(f"{sc}, {ship}, {lab}: deaths per 100, now caught", x[k], r(sc, ship)[ck]['value'], 'same list'))
            CH.append(chg_row(f"{sc}, {ship}, {lab}: deaths per 100, now died", x[k], r(sc, ship)[dk]['value'], 'new death metric'))
        g = find(T2, scope=sc)
        CH.append(chg_row(f"{sc}, {lab}: Somers minus Gearing, now caught", f"{x['diff']:+.1f} ({x['lo']:+.1f} to {x['hi']:+.1f})" if x['diff'] is not None else None, fdiff(g[ck]).replace(' *', ''), 'same list; interval now from diff_ci', '{}'))
        CH.append(chg_row(f"{sc}, {lab}: Somers minus Gearing, now died", f"{x['diff']:+.1f} ({x['lo']:+.1f} to {x['hi']:+.1f})" if x['diff'] is not None else None, fdiff(g[dk]).replace(' *', ''), 'new death metric', '{}'))
nun = sum(1 for q_ in CH if q_[3] == 'unchanged'); CH = [q_ for q_ in CH if q_[3] != 'unchanged']
M.append('**Changed from round 5b:** round 5b did not redo this item; the "round 5b" column is round 5 with the clock fix (`round5b/part-a/out-a3.json`).')
M.append('')
M.append(md_table(['number', 'round 5b', 'round 5c', 'why'], CH))
M.append('')
M.append(f'{nun} other compared numbers are unchanged (the caught rates).')
M.append('')
J['changed'] = CH
CHK = [['A3 Top 6: Somers vs Gearing, died / caught per 100', 'a3.py', "T1 / J['rates']", f"{r('Top 6', 'Somers')['died100']['value']} vs {r('Top 6', 'Gearing')['died100']['value']} / {r('Top 6', 'Somers')['caught100']['value']} vs {r('Top 6', 'Gearing')['caught100']['value']}"],
       ['A3 Rest: Somers vs Gearing, died / caught per 100', 'a3.py', "T1 / J['rates']", f"{r('Rest', 'Somers')['died100']['value']} vs {r('Rest', 'Gearing')['died100']['value']} / {r('Rest', 'Somers')['caught100']['value']} vs {r('Rest', 'Gearing')['caught100']['value']}"],
       ['A3 Somers minus Gearing inside Rest: died / caught', 'a3.py', "T2 / J['somers_minus_gearing']", f"{fdiff(gR['died100'])} / {fdiff(gR['caught100'])}"],
       ['A3 Somers minus Gearing inside Top 6: died / caught', 'a3.py', "T2 / J['somers_minus_gearing']", f"{fdiff(gT['died100'])} / {fdiff(gT['caught100'])}"],
       ['A3 Gearing, Top 6 minus Rest: died / caught', 'a3.py', "T3 / J['top6_minus_rest']", f"{fdiff(tG['died100'])} / {fdiff(tG['caught100'])}"]]
save('out-a3', J, '\n'.join(M), CHK)
