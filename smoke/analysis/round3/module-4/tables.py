import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m4lib import *
random.seed(4)
print('DD smokes', len(DD), '| ncap != zone', sum(s['ncap'] != s['zone'] for s in DD))
high_all, low_all = set(), set()
for m in MAP_ORDER:
    ms, avg, cells = map_cells(m)
    st = stats(ms)
    print(f"\n== {m}: games {GAMES_PER_MAP[m]}, DD smokes {st['n']} (top {st['top']}, PN {sum(s['is_pn'] for s in ms)}), avg conc {k(avg)}, deaths/100 {st['d100']:.0f}, cap won {st['capw']:.0f}%, mrA {sum(s['mrA'] for s in ms)}")
    print('  cells n>=8:')
    for c, x in sorted(cells.items(), key=lambda kv: -kv[1]['conc']):
        if not x['rated']: continue
        lo = in_out_ci(ms, lambda s, c=c: s['ncell'] == c)
        v = [s for s in ms if s['ncell'] == c]
        w = [s for s in v if s['win']]; l = [s for s in v if not s['win']]; t = [s for s in v if s['grp'] == 'top']; r = [s for s in v if s['grp'] == 'rest']
        if x['mark'] == 'high': high_all.add((m, c))
        if x['mark'] == 'low': low_all.add((m, c))
        print(f"   {cell_name(*c):4} n {x['n']:3}{'*' if x['small'] else ' '} conc {k(x['conc']):>6} (med {k(x['med'])}) vs rest of map {ci(lo)} | d100 {x['d100']:3.0f} ({x['deaths']}) | capwon {x['capw']:3.0f}% | "
              f"clans {x['clans']} games {x['games']} el {x['el']:.0f}s | win {k(conc(w)) if w else '-'}/{len(w)} loss {k(conc(l)) if l else '-'}/{len(l)} | top {k(conc(t)) if t else '-'}/{len(t)} rest {k(conc(r)) if r else '-'}/{len(r)} "
              f"| zone {dict(C(s['zone'] for s in v))} mrA {sum(s['mrA'] for s in v)} | {x['mark'].upper()}")
    print('  zones (nearest cap):')
    for z, v in sorted(by(ms, 'zone').items()):
        x = stats(v); lo = in_out_ci(ms, lambda s, z=z: s['zone'] == z)
        lod = in_out_ci(ms, lambda s, z=z: s['zone'] == z, stat=d100); loc = in_out_ci(ms, lambda s, z=z: s['zone'] == z, stat=capw)
        t, r, d = share_ci(ms, lambda s, z=z: s['zone'] == z)
        w = [s for s in v if s['win']]; l = [s for s in v if not s['win']]; tt = [s for s in v if s['grp'] == 'top']; rr = [s for s in v if s['grp'] == 'rest']
        print(f"   {z} n {x['n']:3} conc {k(x['conc']):>6} (med {k(x['med'])}) diff {ci(lo)} | d100 {x['d100']:3.0f} diff {ci(lod, '{:+.0f}')} | capwon {x['capw']:3.0f}% diff {ci(loc, '{:+.0f}')} | share top {t:.0f}% rest {r:.0f}% diff {ci(d, '{:+.0f}')} "
              f"| win {k(conc(w))}/{len(w)} loss {k(conc(l))}/{len(l)} | top {k(conc(tt)) if tt else '-'}/{len(tt)} rest {k(conc(rr)) if rr else '-'}/{len(rr)} | PN {sum(s['is_pn'] for s in v)}")
    hs = {c for (mm, c) in high_all if mm == m}; ls = {c for (mm, c) in low_all if mm == m}
    for lab, cs in (('HIGH', hs), ('LOW', ls)):
        if not cs: continue
        t, r, d = share_ci(ms, lambda s: s['ncell'] in cs)
        print(f"  {lab} cells {[cell_name(*c) for c in sorted(cs)]}: top share {t:.0f}% rest {r:.0f}% diff {ci(d, '{:+.0f}')} pts")
print('\n== pooled, all maps')
for lab, cs in (('HIGH', high_all), ('LOW', low_all)):
    pred = lambda s: (s['map'], s['ncell']) in cs
    t, r, d = share_ci(DD, pred)
    v = [s for s in DD if pred(s)]
    print(f" {lab}: {len(cs)} cells, n {len(v)}, top share {t:.1f}% rest {r:.1f}% diff {ci(d, '{:+.1f}')} pts; conc in those cells top {k(conc([s for s in v if s['grp']=='top']))} rest {k(conc([s for s in v if s['grp']=='rest']))}"
          f" win {k(conc([s for s in v if s['win']]))} loss {k(conc([s for s in v if not s['win']]))}; d100 {d100(v):.0f}")
    for tm in sorted(TOP | {PN}):
        a = [s for s in DD if s['team'] == tm]
        print(f"    {tm}: {pct(a, pred):.0f}% of {len(a)}")
# leave-one-clan-out style check: are high cells still high among rest only / losers only
v = [s for s in DD if (s['map'], s['ncell']) in high_all]; o = [s for s in DD if (s['map'], s['ncell']) not in high_all]
for lab, f in (('rest clans', lambda s: s['grp'] == 'rest'), ('top clans', lambda s: s['grp'] == 'top'), ('losses', lambda s: not s['win']), ('wins', lambda s: s['win'])):
    print(f"  high cells vs elsewhere, {lab}: {k(conc([s for s in v if f(s)]))} (n {sum(1 for s in v if f(s))}) vs {k(conc([s for s in o if f(s)]))} (n {sum(1 for s in o if f(s))})")
print(' win rate of smokes in high cells', pct(v, lambda s: s['win']), 'elsewhere', pct(o, lambda s: s['win']))
