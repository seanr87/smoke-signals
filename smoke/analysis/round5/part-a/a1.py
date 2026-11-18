# A1. Cap-contest smokes split by cover: radar cruiser inside / non-radar cruiser inside / no cruiser (+ 'other' remainder).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
L = []; P = lambda *a: L.append(' '.join(str(x) for x in a))
CC = [s for s in DD if 'cap_contest' in s['tags']]
CCP = [s for s in DD if s['pp'] == 'cap_contest']
P('cap_contest tag n', len(CC), '| primary purpose n', len(CCP), '| same smokes', {id(s) for s in CC} == {id(s) for s in CCP})
P('top/rest', len(TOPS(CC)), len(RESTS(CC)), '| contested cap == nearest cap', sum(s['cap'] == s['near_cap'] for s in CC), 'of', len(CC))
P('snapshots in window: median', med(s['took_window'] for s in CC), 'zero', sum(s['took_window'] == 0 for s in CC), '| own at activation', dict(C(s['near_own'] for s in CC)))
GROUPS = ['radar cruiser inside', 'non-radar cruiser inside', 'no cruiser', 'other']
STATS = [('cap_taken_snapshot_pct', share(lambda s: s['we_took'], lambda s: s['we_took'] is not None)),
         ('cap_won_batch_pct', share(lambda s: s['cap_won'], lambda s: s['own'] != 'ours')),
         ('enemy_prevented_pct', share(lambda s: s['enemy_took'] is False, lambda s: s['enemy_took'] is not None)),
         ('concealed_damage', avg('conc')), ('deaths_per_100', per100('deaths'))]
DEC = lambda name: 0 if name == 'concealed_damage' else 1
rows = []
for g in GROUPS:
    ss = [s for s in CC if s['cover3'] == g]
    row = dict(group=g, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)), note=sm(min(len(TOPS(ss)), len(RESTS(ss)))), clans=clan_dict(ss), clans_text=clan_counts(ss))
    for name, st in STATS:
        row[name] = dict(all=one(ss, st, DEC(name)), split=gap(ss, st, DEC(name)))
    rows.append(row)
hdr = ['group', 'n (T6/Rest)', 'stat', 'all (n) [95%]', 'Top 6 (n)', 'Rest (n)', 'T6-Rest interval']
tb = []
for r in rows:
    for name, _ in STATS:
        a, sp = r[name]['all'], r[name]['split']; f = '{:,.0f}' if name == 'concealed_damage' else '{:.1f}'; fs = '{:+,.0f}' if name == 'concealed_damage' else '{:+.1f}'
        tb.append([r['group'], f"{r['n']} ({r['n_top6']}/{r['n_rest']})", name, f"{fv(a['value'], f)} ({a['n']}) [{fci(a, f)}]", f"{fv(sp['top6'], f)} ({sp['n_top6']})", f"{fv(sp['rest'], f)} ({sp['n_rest']})", fci(sp, fs)])
P(md_table(hdr, tb))
for r in rows: P(r['group'], '|', r['clans_text'])
# differences between cover groups (all clans, and within Top 6 / Rest)
pairs = [('radar cruiser inside', 'non-radar cruiser inside'), ('radar cruiser inside', 'no cruiser'), ('non-radar cruiser inside', 'no cruiser')]
cmp_rows = []
for scope, base in (('all', CC), ('top6', TOPS(CC)), ('rest', RESTS(CC))):
    for a, b in pairs:
        A = [s for s in base if s['cover3'] == a]; B = [s for s in base if s['cover3'] == b]
        for name, st in STATS:
            x = diff2(A, B, st, DEC(name)); x.update(scope=scope, a_group=a, b_group=b, stat=name); cmp_rows.append(x)
P('\nDifferences between cover groups (a - b), interval by resampling clans')
P(md_table(['scope', 'a', 'b', 'stat', 'a (n)', 'b (n)', 'diff', 'interval'],
           [[x['scope'], x['a_group'], x['b_group'], x['stat'], f"{fv(x['a'])} ({x['n_a']})", f"{fv(x['b'])} ({x['n_b']})", fv(x['diff'], '{:+.1f}'), fci(x)] for x in cmp_rows]))
# like-with-like on the starting owner of the cap (neutral vs enemy-held), since "taken" is easier on a neutral cap
own_rows = []
for own in ('neutral', 'theirs', 'ours'):
    for g in GROUPS[:3]:
        ss = [s for s in CC if s['cover3'] == g and s['near_own'] == own]
        own_rows.append(dict(cap_at_activation=own, group=g, n=len(ss), n_top6=len(TOPS(ss)), n_rest=len(RESTS(ss)),
                             cap_taken=one(ss, STATS[0][1]), cap_won_batch=one(ss, STATS[1][1]), enemy_prevented=one(ss, STATS[2][1])))
P('\nBy who held the cap at activation')
P(md_table(['cap at activation', 'group', 'n (T6/Rest)', 'cap taken % (n) [95%]', 'cap_won % (n)', 'enemy prevented % (n) [95%]'],
           [[x['cap_at_activation'], x['group'], f"{x['n']} ({x['n_top6']}/{x['n_rest']})", f"{fv(x['cap_taken']['value'])} ({x['cap_taken']['n']}) [{fci(x['cap_taken'], '{:.1f}')}]",
             f"{fv(x['cap_won_batch']['value'])} ({x['cap_won_batch']['n']})", f"{fv(x['enemy_prevented']['value'])} ({x['enemy_prevented']['n']}) [{fci(x['enemy_prevented'], '{:.1f}')}]"] for x in own_rows]))
# neutral-cap-only comparison radar vs no cruiser
neu = [s for s in CC if s['near_own'] == 'neutral']
nd = []
for a, b in pairs:
    for name, st in STATS[:3]:
        x = diff2([s for s in neu if s['cover3'] == a], [s for s in neu if s['cover3'] == b], st); x.update(a_group=a, b_group=b, stat=name); nd.append(x)
P('\nNeutral caps only, differences')
P(md_table(['a', 'b', 'stat', 'a (n)', 'b (n)', 'diff', 'interval'], [[x['a_group'], x['b_group'], x['stat'], f"{fv(x['a'])} ({x['n_a']})", f"{fv(x['b'])} ({x['n_b']})", fv(x['diff'], '{:+.1f}'), fci(x)] for x in nd]))
P('\nContext: share activated in first 5 min, share inside the cap, median elapsed')
for g in GROUPS:
    ss = [s for s in CC if s['cover3'] == g]
    P(g, 'early %', r1(pct(ss, lambda s: s['el'] < 300)), 'inside cap %', r1(pct(ss, lambda s: s['inside'])), 'median el', med(s['el'] for s in ss), 'radar_cap set %', r1(pct(ss, lambda s: bool(s['radar_cap']))),
      'own', dict(C(s['near_own'] for s in ss)), 'cruisers inside', dict(cruiser_counts(ss, 'inside').most_common(6)), 'smoker ships', dict(C(s['ship'] for s in ss).most_common(5)))
both = [s for s in CC if s['we_took'] is not None and s['own'] != 'ours']
P('\nagreement we_took vs cap_won (n', len(both), '): (we_took, cap_won)', dict(C((bool(s['we_took']), bool(s['cap_won'])) for s in both)))
fig = Fig(1100, 380, 'A1. Cap-contest destroyer smokes by cover', 'Top 6 blue, Rest orange. n in the right margin as Top 6 / Rest. Cap taken excludes caps already ours. Association only.')
fig.legend(40, 72, [('Top 6', BLUE), ('Rest', ORANGE)])
for i, (name, title, f) in enumerate([('cap_taken_snapshot_pct', 'Cap taken (%)', '{:.0f}%'), ('enemy_prevented_pct', 'Enemy kept off the cap (%)', '{:.0f}%'), ('concealed_damage', 'Concealed damage per smoke', '{:,.0f}')]):
    x = 30 + i * 355
    fig.add(T(x + 10, 105, title, size=13, fill=INK, anchor='start', weight='600'))
    bar_rows(fig, x, 118, 345, [(r['group'].replace(' inside', ' in').replace('cruiser', 'CA'), {'top': r[name]['split']['top6'], 'rest': r[name]['split']['rest']}, f"{r[name]['split']['n_top6']}/{r[name]['split']['n_rest']}") for r in rows], fmt=f, row_h=44, label_w=118)
fig.add(T(40, 325, 'CA = cruiser. "radar CA in" = a radar cruiser inside the smoke; "non-radar CA in" = a cruiser inside and no radar ship inside; "other" = cruiser screened only, or mixed.', size=11, anchor='start'))
fig.add(T(40, 343, 'Missing bar = fewer than 8 smokes (too few). Cap owners come from snapshots at smoke moments only, so "taken" and "kept off" are approximate.', size=11, anchor='start'))
fig.save(os.path.join(FIGS, 'a1-cap-contest-by-cover'))
out('out-a1', dict(definition='destroyer smokes with the cap_contest purpose tag (identical to primary purpose cap_contest in this batch)', n=len(CC), rows=rows, group_differences=cmp_rows, by_cap_owner=own_rows, neutral_only_differences=nd), '\n'.join(L))
