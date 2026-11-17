import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m3lib import *
P = print
for s in S:
    s['dd_dmg'] = sum(t['dmg'] for t in s['targets'] if t['cls'] == 'destroyer')
    s['dd_hit'] = any(t['cls'] == 'destroyer' and t['dmg'] > 0 for t in s['targets'])
    s['dd_sunk'] = sum(1 for t in s['targets'] if t['cls'] == 'destroyer' and t['sunk'])
    cd = s['j'].get('cap_denial') or {}
    s['den'] = (cd.get('enemies_during') - cd.get('enemies_before')) if cd.get('enemies_before') is not None and cd.get('enemies_during') is not None else None
    s['takeable'] = s['own'] in ('neutral', 'theirs')
def out(ss, label):
    if not ss: P(f'  {label}: n=0'); return
    tk = [s for s in ss if s['takeable']]
    P(f'  {label}: n={len(ss)}{small(len(ss))} | cap taken (not ours at start) {n0(pct(tk, lambda s: s["cap_won"]))}% of {len(tk)} | conc mean {mean(s["conc"] for s in ss):,.0f} med {med(s["conc"] for s in ss):,.0f} | >=20k {pct(ss, lambda s: s["conc"]>=20000):.0f}% | DD dmg mean {mean(s["dd_dmg"] for s in ss):,.0f} DD hit {pct(ss, lambda s: s["dd_hit"]):.0f}% DD sunk/100 {100*mean(s["dd_sunk"] for s in ss):.0f} | kills/100 {100*mean(s["kills"] for s in ss):.0f} deaths/100 {100*mean(s["deaths"] for s in ss):.0f} | taken while radar-spotted mean {mean(s["rsd"] for s in ss):,.0f} | enemy near cap change {mean([s["den"] for s in ss if s["den"] is not None]) or 0:+.2f}')

P('== A. radar pressed vs not, same setup: DD smokes with a radar ship inside (stack or screen)')
setup = [s for s in DD if s['radar_in'] or (s['rship'] and not s['rship']['is_smoker'])]
used = [s for s in setup if s['off_radar']]; notused = [s for s in setup if not s['off_radar']]
out(used, 'radar run from inside'); out(notused, 'radar ship inside, radar not run')
out([s for s in used if s['spots'] == 0], '  run, 0 spotted'); out([s for s in used if s['spots'] == 1], '  run, 1 spotted'); out([s for s in used if s['spots'] >= 2], '  run, 2+ spotted')
for grp in ('top', 'rest'):
    out([s for s in used if s['grp'] == grp], f'  run {grp}'); out([s for s in notused if s['grp'] == grp], f'  not run {grp}')
def dstat(f):
    return lambda x: (f([s for s in x if s['off_radar']]) - f([s for s in x if not s['off_radar']])) if any(s['off_radar'] for s in x) and any(not s['off_radar'] for s in x) else None
for nm, f, fmt in (('conc', lambda x: mean(s['conc'] for s in x), '{:+,.0f}'), ('DD dmg', lambda x: mean(s['dd_dmg'] for s in x), '{:+,.0f}'), ('DD hit pts', lambda x: pct(x, lambda s: s['dd_hit']), '{:+.0f}'),
                   ('cap taken pts (takeable)', lambda x: pct([s for s in x if s['takeable']], lambda s: s['cap_won']), '{:+.0f}'), ('kills/100', lambda x: 100 * mean(s['kills'] for s in x), '{:+.0f}'),
                   ('deaths/100', lambda x: 100 * mean(s['deaths'] for s in x), '{:+.0f}'), ('>=20k pts', lambda x: pct(x, lambda s: s['conc'] >= 20000), '{:+.0f}')):
    d = dstat(f); P(f'   run minus not run, {nm}: {fmt.format(d(setup))} CI {ci(boot_stat(setup, d), fmt)}')
P('  share run: top', pct([s for s in setup if s['grp'] == 'top'], lambda s: bool(s['off_radar'])), 'rest', pct([s for s in setup if s['grp'] == 'rest'], lambda s: bool(s['off_radar'])), 'CI', ci(boot_diff(setup, lambda x: pct(x, lambda s: bool(s['off_radar']))), '{:+.0f}'), 'n', sum(s['grp'] == 'top' for s in setup), sum(s['grp'] == 'rest' for s in setup))
sp = [s for s in DD if s['spots'] > 0]
P('  spots per radar run smoke: top', mean(s['spots'] for s in used if s['grp'] == 'top'), 'rest', mean(s['spots'] for s in used if s['grp'] == 'rest'), 'CI', ci(boot_diff(used, lambda x: mean(s['spots'] for s in x)), '{:+.2f}'))
P('  enemies spotted per team-game: top %.2f rest %.2f CI %s' % ((lambda c: (rate(c, 'top'), rate(c, 'rest'), ci(boot_rate_diff(c), '{:+.2f}')))(collections.Counter({t: sum(s['spots'] for s in sp if s['team'] == t) for t in GAMES}))))
P('  radar-run DD smokes per team-game: top %.2f rest %.2f CI %s' % ((lambda c: (rate(c, 'top'), rate(c, 'rest'), ci(boot_rate_diff(c), '{:+.2f}')))(C(s['team'] for s in DD if s['off_radar']))))

P('\n== B. cap_control vs cap_contest, takeable caps only')
cc = [s for s in DD if s['cc']]; ct = [s for s in DD if s['pp'] == 'cap_contest']
out(cc, 'cap_control'); out(ct, 'cap_contest')
out([s for s in ct if s['radar_in']], 'cap_contest with radar ship inside (radar not at 90% or not run)'); out([s for s in ct if not s['radar_in']], 'cap_contest no radar ship inside')
both = [s for s in cc + ct if s['takeable']]
d = lambda x: (pct([s for s in x if s['cc']], lambda s: s['cap_won']) - pct([s for s in x if not s['cc']], lambda s: s['cap_won'])) if any(s['cc'] for s in x) and any(not s['cc'] for s in x) else None
P('  cap taken diff (takeable):', d(both), ci(boot_stat(both, d), '{:+.0f}'))
for grp in ('top', 'rest'): out([s for s in cc if s['grp'] == grp], 'cc ' + grp)
P('  cc conc top-rest CI', ci(boot_diff(cc, lambda x: mean(s['conc'] for s in x))), ' cap taken top-rest', ci(boot_diff([s for s in cc if s['takeable']], lambda x: pct(x, lambda s: s['cap_won'])), '{:+.0f}'))
out([s for s in DD if s['play'] == 'radar_trap'], 'radar_trap')
P('  trap inside cap?', C(s['inside'] for s in DD if s['play'] == 'radar_trap'), 'edge med m', med(s['edge'] for s in DD if s['play'] == 'radar_trap'), 'cc edge med', med(s['edge'] for s in cc))
P('  trap coverage_pct', sorted(round((s['radar_cap'] or {}).get('coverage_pct', -1)) for s in DD if s['play'] == 'radar_trap'))
P('  trap score_diff mean top/rest', mean(s['score_diff'] for s in DD if s['play'] == 'radar_trap' and s['grp'] == 'top'), mean(s['score_diff'] for s in DD if s['play'] == 'radar_trap' and s['grp'] == 'rest'), 'cc', mean(s['score_diff'] for s in cc))

P('\n== C. per map x cap (DD plays)')
rows = []
for m in MAPORDER:
    for c in 'ABCDE':
        ss = [s for s in DD if s['play'] and s['map'] == m and s['ncap'] == c]
        if len(ss) < 4: continue
        tk = [s for s in ss if s['takeable']]
        rows.append((m, c, len(ss), sum(s['cc'] for s in ss), sum(s['grp'] == 'top' for s in ss), f"{pct(ss, lambda s: s['early']):.0f}%", f"{sum(s['cap_won'] for s in tk)}/{len(tk)}", n0(mean(s['conc'] for s in ss)), f"{mean(s['spots'] for s in ss):.1f}", C(s['ncell_name'] for s in ss).most_common(3), C(s['rship']['ship'] for s in ss).most_common(2)))
for r in rows: P('  ', r)
P('\n== D. top6 per clan: plays, per game, cc, trap, radar ships')
for t in sorted(GAMES, key=lambda t: -sum(1 for s in DD if s['play'] and s['team'] == t) / GAMES[t]):
    ss = [s for s in DD if s['play'] and s['team'] == t]
    if t in TOP or t == PN or len(ss) >= 4:
        P(f'  {t}{"*" if t in TOP else ""}: games {GAMES[t]} plays {len(ss)} per game {len(ss)/GAMES[t]:.2f} cc {sum(s["cc"] for s in ss)} trap {sum(not s["cc"] for s in ss)} | CA plays {sum(1 for s in CA if s["play"] and s["team"]==t)} | ships {C(s["rship"]["ship"] for s in ss).most_common(3)} | maps {C(s["map"] for s in ss).most_common(3)}')
P('\n== E. radar ship distance from smoke centre / cap, and how far inside its own half')
for s in DD:
    if s['play']:
        g = G[s['game']]; cp = next((c for c in ncaps(g, s['map'], s['side']) if c['cap'] == s['cap']), None)
        s['r2cap'] = math.hypot(s['rship']['nx'] - cp['x'], s['rship']['nz'] - cp['z']) * WU if cp else None
P('  radar ship to cap centre km: median', med(s['r2cap'] for s in DD if s['play'] and s.get('r2cap')) / 1000, 'q25/q75', q([s['r2cap'] for s in DD if s['cc']], .25) / 1000, q([s['r2cap'] for s in DD if s['cc']], .75) / 1000)
P('  cc inside cap', pct(cc, lambda s: s['inside']), 'cap_contest inside', pct(ct, lambda s: s['inside']))
P('  radar range by ship', {k: v for k, v in C((p['ship'].replace('\xa0', ' '), p['radar_m']) for g in G.values() for p in g['roster'].values() if p.get('radar_m')).items()})
P('\n== F. timing')
for lab, ss in (('cc', cc), ('trap', [s for s in DD if s['play'] == 'radar_trap']), ('all DD', DD)):
    P(f'  {lab}: n={len(ss)} early {pct(ss, lambda s: s["early"]):.0f}% median {mmss(med(s["el"] for s in ss))} | bins 0-2:{sum(s["el"]<120 for s in ss)} 2-5:{sum(120<=s["el"]<300 for s in ss)} 5-10:{sum(300<=s["el"]<600 for s in ss)} 10+:{sum(s["el"]>=600 for s in ss)}')
d = lambda x: pct([s for s in x if s['cc']], lambda s: s['early']) - pct([s for s in x if not s['cc']], lambda s: s['early']) if any(s['cc'] for s in x) else None
P('  cc early minus other DD early', d(DD), ci(boot_stat(DD, d), '{:+.0f}'))
P('  early stack overall CI exact', boot_diff([s for s in DD if s['early'] and s['stack']], lambda x: pct(x, lambda s: s['radar_in'])))
es = [s for s in DD if s['early'] and s['stack']]
out([s for s in es if s['radar_in']], 'early stack with radar ship'); out([s for s in es if not s['radar_in']], 'early stack without')
d = lambda x: (pct([s for s in x if s['radar_in'] and s['takeable']], lambda s: s['cap_won']) - pct([s for s in x if not s['radar_in'] and s['takeable']], lambda s: s['cap_won'])) if any(s['radar_in'] and s['takeable'] for s in x) and any(not s['radar_in'] and s['takeable'] for s in x) else None
P('  early stack cap taken diff radar vs none', d(es), ci(boot_stat(es, d), '{:+.0f}'))
P('  CA: Svea smokes total', sum(1 for s in CA if s['ship'] == 'Svea'), 'by grp', C(s['grp'] for s in CA if s['ship'] == 'Svea'), 'plays', C(s['grp'] for s in CA if s['play']), 'CA plays ncap', C((s['map'], s['ncap']) for s in CA if s['play']).most_common(5))
out([s for s in CA if s['play']], 'CA radar plays'); out([s for s in CA if s['ship'] == 'Svea' and not s['play']], 'Svea smokes no play')
