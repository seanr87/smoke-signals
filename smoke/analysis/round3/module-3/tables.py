import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m3lib import *
P = print
P('roster keys', list(next(iter(next(iter(G.values()))['roster'].values())).keys()))
P('team games top/rest', sum(GAMES[t] for t in GAMES if t in TOP), sum(GAMES[t] for t in GAMES if t not in TOP), 'PN', GAMES[PN])

def grpline(ss, label):
    P(f'  {label}: n={len(ss)} top={sum(s["grp"]=="top" for s in ss)} rest={sum(s["grp"]=="rest" for s in ss)} PN={sum(s["is_pn"] for s in ss)}')

P('\n== 1. counts')
for nm, base in (('DD', DD), ('CA', CA)):
    for tag in ('cc', 'rt'):
        ss = [s for s in base if s[tag] and (tag == 'cc' or not s['cc'])]
        grpline(ss, f'{nm} {tag}')
        cnt = C(s['team'] for s in ss)
        P(f'    per team-game top {rate(cnt,"top"):.2f} rest {rate(cnt,"rest"):.2f} diff CI {ci(boot_rate_diff(cnt), "{:+.2f}")}')
        sh = lambda x, tag=tag: pct(x, lambda s: s['play'] == ('cap_control' if tag == 'cc' else 'radar_trap'))
        P(f'    share of smokes top {sh([s for s in base if s["grp"]=="top"]):.1f}% rest {sh([s for s in base if s["grp"]=="rest"]):.1f}% CI {ci(boot_diff(base, sh), "{:+.1f}")}')
ddp = [s for s in DD if s['play']]
cnt = C(s['team'] for s in ddp)
P('DD any radar play per team-game: top %.2f rest %.2f CI %s' % (rate(cnt, 'top'), rate(cnt, 'rest'), ci(boot_rate_diff(cnt), '{:+.2f}')))
P('per clan DD plays/games:', sorted(((t, cnt[t], GAMES[t], round(cnt[t] / GAMES[t], 2)) for t in GAMES), key=lambda x: -x[3]))
# share of games with at least one play
gp = {(s['game'], s['team']) for s in S if s['play']}
for grp in ('top', 'rest'):
    tg = [(k, t) for k, t in TG if (t in TOP) == (grp == 'top')]
    P(grp, 'team-games with >=1 radar play (any class): %d of %d = %.0f%%' % (sum(x in gp for x in tg), len(tg), 100 * sum(x in gp for x in tg) / len(tg)))

P('\n== 2. who is the radar ship (DD smokes with a play)')
P(' ship', C(s['rship']['ship'] for s in ddp).most_common())
P(' is_smoker', C((s['play'], s['rship']['is_smoker']) for s in ddp))
P(' cls', C((s['play'], s['rship']['cls'], s['grp']) for s in ddp))
P(' how', C(s['rship']['how'] for s in ddp))
P(' CA plays: ship', C(s['rship']['ship'] for s in CA if s['play']).most_common(), 'is_smoker', C(s['rship']['is_smoker'] for s in CA if s['play']))
P(' coverage', C((s['play'], s['coverage']) for s in ddp))
P(' kind', C((s['play'], s['kind']) for s in ddp))
P(' pos missing', sum(s['rship']['nx'] is None for s in ddp))

P('\n== 3. when')
for tag in ('cap_control', 'radar_trap'):
    for grp in ('top', 'rest'):
        e = [s['el'] for s in ddp if s['play'] == tag and s['grp'] == grp]
        P(f' {tag} {grp} n={len(e)} median {mmss(med(e))} q25 {mmss(q(e,.25))} q75 {mmss(q(e,.75))} early% {pct(e, lambda x: x<300):.0f}')
P(' minute hist cc', sorted(C(s['el'] // 120 * 2 for s in ddp if s['cc']).items()))
P(' minute hist rt', sorted(C(s['el'] // 120 * 2 for s in ddp if not s['cc']).items()))
P(' all DD smokes early%', pct(DD, lambda s: s['early']))

P('\n== 4. where: map x ncap, cells')
for m in MAPORDER:
    ss = [s for s in ddp if s['map'] == m]
    ng = sum(g['map'] == m for g in G.values())
    P(f' {m} games {ng} plays {len(ss)} (cc {sum(s["cc"] for s in ss)}, rt {sum(not s["cc"] for s in ss)}) top {sum(s["grp"]=="top" for s in ss)} rest {sum(s["grp"]=="rest" for s in ss)} | per team-game {len(ss)/(2*ng):.2f}')
    P('    ncap', C(s['ncap'] for s in ss).most_common(), 'mrA', sum(s['mrA'] for s in ss))
    P('    cells', C(s['ncell_name'] for s in ss).most_common(6))
    P('    own', C(s['own'] for s in ss), 'cap_won', sum(s['cap_won'] for s in ss))
    P('    CA plays', len([s for s in CA if s['play'] and s['map'] == m]), C(s['ncap'] for s in CA if s['play'] and s['map'] == m).most_common())

P('\n== 5. outcomes: DD smokes near a cap, radar play vs none')
def out(ss, label):
    if not ss: return
    P(f'  {label}: n={len(ss)}{small(len(ss))} cap_won {pct(ss, lambda s: s["cap_won"]):.0f}% conc mean {mean(s["conc"] for s in ss):,.0f} med {med(s["conc"] for s in ss):,.0f} kills/smoke {mean(s["kills"] for s in ss):.2f} deaths/smoke {mean(s["deaths"] for s in ss):.2f} radar_on_us% {pct(ss, lambda s: s["radar_on_us"]>0):.0f} win% {pct(ss, lambda s: s["win"]):.0f} swing {mean([s["swing"] for s in ss if s["swing"] is not None]) or 0:+.0f}')
cc = [s for s in DD if s['cc']]; ct = [s for s in DD if s['pp'] == 'cap_contest']
out(cc, 'cap_control'); out(ct, 'cap_contest (no radar play)')
out([s for s in cc if s['grp'] == 'top'], 'cap_control top'); out([s for s in cc if s['grp'] == 'rest'], 'cap_control rest')
out([s for s in ct if s['grp'] == 'top'], 'cap_contest top'); out([s for s in ct if s['grp'] == 'rest'], 'cap_contest rest')
both = cc + ct
for nm, f in (('cap_won pts', lambda x: pct(x, lambda s: s['cap_won'])), ('conc', lambda x: mean(s['conc'] for s in x)), ('kills', lambda x: mean(s['kills'] for s in x)), ('deaths', lambda x: mean(s['deaths'] for s in x))):
    d = lambda x, f=f: (f([s for s in x if s['cc']]) - f([s for s in x if not s['cc']])) if any(s['cc'] for s in x) and any(not s['cc'] for s in x) else None
    P(f'   cap_control minus cap_contest {nm}: {d(both):+.2f} CI {ci(boot_stat(both, d), "{:+.2f}")}')
# by ownership
for o in ('neutral', 'theirs', 'ours'):
    out([s for s in cc if s['own'] == o], f'cap_control own={o}'); out([s for s in ct if s['own'] == o], f'cap_contest own={o}')
# early
out([s for s in cc if s['early']], 'cap_control early'); out([s for s in ct if s['early']], 'cap_contest early')
out([s for s in cc if s['mrA']], 'cap_control mrA'); out([s for s in cc if not s['mrA']], 'cap_control not mrA')
out([s for s in DD if s['rt'] and not s['cc']], 'radar_trap DD')
out([s for s in DD if not s['play']], 'all other DD')
out([s for s in CA if s['cc']], 'CA cap_control'); out([s for s in CA if s['rt'] and not s['cc']], 'CA radar_trap'); out([s for s in CA if not s['play']], 'CA other')

P('\n== 6. offensive radar from smoke (all inferred)')
for nm, base in (('DD', DD), ('CA', CA)):
    orr = [s for s in base if s['off_radar']]
    P(f' {nm} smokes with radar run inside: {len(orr)} ; spotted>=1: {sum(s["spots"]>0 for s in orr)} ; total spots {sum(s["spots"] for s in orr)}')
    for lab, ss in (('spots=0', [s for s in orr if s['spots'] == 0]), ('spots=1', [s for s in orr if s['spots'] == 1]), ('spots>=2', [s for s in orr if s['spots'] >= 2])):
        if ss: P(f'   {lab} n={len(ss)}{small(len(ss))} rsd mean {mean(s["rsd"] for s in ss):,.0f} med {med(s["rsd"] for s in ss):,.0f} rsd>0 {pct(ss, lambda s: s["rsd"]>0):.0f}% conc {mean(s["conc"] for s in ss):,.0f} kills {mean(s["kills"] for s in ss):.2f} cap_won {pct(ss, lambda s: s["cap_won"]):.0f}% deaths {mean(s["deaths"] for s in ss):.2f}')
    sp = [s for s in orr if s['spots'] > 0]
    for grp in ('top', 'rest'):
        ss = [s for s in sp if s['grp'] == grp]
        if ss: P(f'   spotted {grp} n={len(ss)} rsd mean {mean(s["rsd"] for s in ss):,.0f} med {med(s["rsd"] for s in ss):,.0f} spots/smoke {mean(s["spots"] for s in ss):.2f} kills {mean(s["kills"] for s in ss):.2f} cap_won {pct(ss, lambda s: s["cap_won"]):.0f}%')
    if nm == 'DD':
        P('   rsd top-rest CI', ci(boot_diff(sp, lambda x: mean(s['rsd'] for s in x))), ' spots/smoke CI', ci(boot_diff(sp, lambda x: mean(s['spots'] for s in x)), '{:+.2f}'))
        cnt2 = C(s['team'] for s in sp)
        P('   spotting smokes per team-game top %.2f rest %.2f CI %s' % (rate(cnt2, 'top'), rate(cnt2, 'rest'), ci(boot_rate_diff(cnt2), '{:+.2f}')))
        tot = collections.Counter()
        for s in sp: tot[s['team']] += s['rsd']
        P('   radar-spotted dmg per team-game top %.0f rest %.0f CI %s' % (rate(tot, 'top'), rate(tot, 'rest'), ci(boot_rate_diff(tot))))
        P('   by map spotted n, rsd mean, total:', [(m, len(x), round(mean(s['rsd'] for s in x) or 0), round(sum(s['rsd'] for s in x))) for m in MAPORDER for x in [[s for s in sp if s['map'] == m]]])
        P('   by ncap:', [(m, c, len(x), round(mean(s['rsd'] for s in x))) for m in MAPORDER for c in 'ABCDE' for x in [[s for s in sp if s['map'] == m and s['ncap'] == c]] if len(x) >= 5])
        P('   radar ship type (spotting smokes): ', [(k, len(x), round(mean(s['rsd'] for s in x)), round(mean(s['spots'] for s in x), 2)) for k, x in sorted(by(sp, lambda s: s['rship']['ship']).items(), key=lambda kv: -len(kv[1]))])
        P('   targets hit classes in top-rsd smokes:', C(t['cls'] for s in sp if s['rsd'] > 0 for t in s['targets']))
        P('   share of conc that is rsd among spotting smokes', sum(s['rsd'] for s in sp) / max(1, sum(s['total'] for s in sp)))
        P('   biggest rsd:', [(s['team'], s['map'], s['ncap'], s['ncell_name'], mmss(s['el']), round(s['rsd']), s['rship']['ship'], s['spots'], s['kills']) for s in sorted(sp, key=lambda s: -s['rsd'])[:8]])
P(' rsd<=total?', sum(s['rsd'] > s['total'] + 1 for s in S), 'rsd>conc', sum(s['rsd'] > s['conc'] + 1 for s in S if s['rsd']))
P(' off_radar without play tag', sum(1 for s in S if s['off_radar'] and not s['play']), ' of which spots>0', sum(1 for s in S if s['off_radar'] and not s['play'] and s['spots'] > 0))
P(' cc without off_radar', sum(1 for s in S if s['cc'] and not s['off_radar']))

P('\n== 7. early stacks with a radar ship (DD smokes, el<300, stacked)')
es = [s for s in DD if s['early'] and s['stack']]
for key, lab in (('radar_in', 'radar partner inside'), ('radar_any', 'radar partner covered (any how)')):
    f = lambda x, key=key: pct(x, lambda s: s[key])
    P(f' {lab}: top {f([s for s in es if s["grp"]=="top"]):.0f}% (n={sum(s["grp"]=="top" for s in es)}) rest {f([s for s in es if s["grp"]=="rest"]):.0f}% (n={sum(s["grp"]=="rest" for s in es)}) CI {ci(boot_diff(es, f), "{:+.0f}")}')
    for m in MAPORDER:
        a = [s for s in es if s['map'] == m and s['grp'] == 'top']; b = [s for s in es if s['map'] == m and s['grp'] == 'rest']
        P(f'    {m}: top {n0(f(a))}% n={len(a)}{small(len(a))} | rest {n0(f(b))}% n={len(b)}{small(len(b))} | CI {ci(boot_diff([s for s in es if s["map"]==m], f), "{:+.0f}")}')
P(' PN early stacks', len([s for s in es if s['is_pn']]), 'with radar inside', sum(s['radar_in'] for s in es if s['is_pn']))
P(' smoker itself radar DD among early stacks', pct(es, lambda s: s['smoker_radar']), 'top', pct([s for s in es if s['grp'] == 'top'], lambda s: s['smoker_radar']), 'rest', pct([s for s in es if s['grp'] == 'rest'], lambda s: s['smoker_radar']))
P(' early stack share of early DD smokes: top', pct([s for s in DD if s['early'] and s['grp'] == 'top'], lambda s: s['stack']), 'rest', pct([s for s in DD if s['early'] and s['grp'] == 'rest'], lambda s: s['stack']))
P(' early radar stacks per team-game:', 'top %.2f rest %.2f' % (rate(C(s['team'] for s in es if s['radar_in']), 'top'), rate(C(s['team'] for s in es if s['radar_in']), 'rest')), ci(boot_rate_diff(C(s['team'] for s in es if s['radar_in'])), '{:+.2f}'))
P(' of early radar stacks, radar actually used (off_radar or cc):', pct([s for s in es if s['radar_in']], lambda s: bool(s['off_radar'])), 'top', pct([s for s in es if s['radar_in'] and s['grp'] == 'top'], lambda s: bool(s['off_radar'])), 'rest', pct([s for s in es if s['radar_in'] and s['grp'] == 'rest'], lambda s: bool(s['off_radar'])))
out([s for s in es if s['radar_in']], 'early stack with radar'); out([s for s in es if not s['radar_in']], 'early stack no radar')
P(' radar partner ship types in early stacks', C(p['ship'] for s in es for p in s['partners'] if p['radar'] and p['how'] == 'inside').most_common(8))
P(' early radar stack ncap by map', [(m, C(s['ncap'] for s in es if s['radar_in'] and s['map'] == m).most_common(3)) for m in MAPORDER])

P('\n== 8. radar ready (full cover) but not activated, DD smokes')
rc = [s for s in DD if s['radar_cap'] and s['radar_cap']['coverage_pct'] >= 90]
f = lambda x: pct(x, lambda s: s['radar_cap']['activated'])
P(' >=90% cover n', len(rc), 'activated top', f([s for s in rc if s['grp'] == 'top']), 'rest', f([s for s in rc if s['grp'] == 'rest']), 'CI', ci(boot_diff(rc, f), '{:+.0f}'), 'n top/rest', sum(s['grp'] == 'top' for s in rc), sum(s['grp'] == 'rest' for s in rc))
P(' activated but <90', sum(1 for s in DD if s['radar_cap'] and s['radar_cap']['activated'] and s['radar_cap']['coverage_pct'] < 90))
P(' PN plays:', [(s['cls'], s['play'], s['map'], s['ncap'], s['ncell_name'], mmss(s['el']), s['rship']['ship'], s['spots'], round(s['rsd']), s['cap_won']) for s in S if s['is_pn'] and s['play']])
P(' PN DD smokes', sum(s['is_pn'] for s in DD), 'PN off_radar', [(s['cls'], s['spots'], round(s['rsd'])) for s in S if s['is_pn'] and s['off_radar']])
