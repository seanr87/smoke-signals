import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_lib import *
cols = ['n_smokes', 'n_games', 'smokes_per_game'] + [k for k in STATS]
def row(lab, d): print(f'{lab:8}', ' '.join(f'{d[c]:7.1f}' if d[c] is not None else '      -' for c in cols))
print(' ' * 8, ' '.join(c[:7].rjust(7) for c in cols))
for t in STYLE_A + MID + STYLE_B + ['PN']: row(t, CLAN_NUM[t])
row('A', numbers(STYLE_A)); row('B', numbers(STYLE_B)); row('Rest', numbers([t for t in GAMES if t not in TOP]))
print('\ndistances top6 + PN')
tt = STYLE_A + MID + STYLE_B + ['PN']
for a in tt: print(f'{a:6}', ' '.join(f'{dist(Z[a], Z[b]):5.2f}' for b in tt))
print('\nnearest style (dist A, dist B)')
for t in sorted(CLANS7, key=lambda t: nearest(t)[0] - nearest(t)[1]):
    a, b, lab = nearest(t); print(f'{t:6} {a:5.2f} {b:5.2f} {lab:14} games {len(GAMES[t])} smokes {len(BY_TEAM[t])} W-L {WL[t]}')
print('\ncast')
for lab, teams in [(t, [t]) for t in tt] + [('A', STYLE_A), ('B', STYLE_B), ('Rest', [t for t in GAMES if t not in TOP])]:
    c = cast_numbers(teams); print(f'{lab:6}', {k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items()})
for km in (5, 8, 10, 15):
    print(km, [round(pct([s for s in smokes_of(x) if s['cls'] == 'destroyer'], lambda s: second_fwd(s, km))) for x in (STYLE_A, STYLE_B, MID)])
A, B = smokes_of(STYLE_A), smokes_of(STYLE_B)
for k in ['stacked_pct', 'selfish_pct', 'stationary_pct', 'flank_lines_pct', 'parked_cruiser_pct', 'cap_sitters_pct', 'moving_exhaust_pct', 'cruiser_dmg_pct', 'first_smoke_s', 'long_dd_pct']:
    print(k, round(STATS[k](A), 1), round(STATS[k](B), 1), ci(boot2(A, B, STATS[k]), '{:+.0f}'))
dA, dB = [s for s in A if s['cls'] == 'destroyer'], [s for s in B if s['cls'] == 'destroyer']
print('2nd dd fwd', ci(boot2(dA, dB, lambda ss: pct(ss, second_fwd)), '{:+.0f}'))
print('\nmaps')
for m in MAIN_MAPS:
    for lab, teams in (('A', STYLE_A), ('B', STYLE_B), ('K', MID)):
        ss = [s for s in smokes_of(teams) if s['map'] == m]
        if not ss: print(m, lab, 0); continue
        ng = len({(s['game'], s['team']) for s in ss}); size = MAPS[m]['space_size']
        print(f'{m:15} {lab} n={len(ss):3} games={ng:2} dd%={pct(ss, lambda s: s["cls"] == "destroyer"):3.0f} inside%={pct(ss, lambda s: s["inside"]):3.0f} '
              f'medfwd%={100 * med((s["nz"] + size / 2) / size for s in ss):3.0f} ownhalf%={pct(ss, lambda s: s["nz"] < 0):3.0f} west%={pct(ss, lambda s: s["nx"] < -size / 6):3.0f} mid%={pct(ss, lambda s: abs(s["nx"]) <= size / 6):3.0f} east%={pct(ss, lambda s: s["nx"] > size / 6):3.0f} '
              f'caps={dict(C(s["ncap"] for s in ss).most_common())} cells={C(s["ncell_name"] for s in ss).most_common(4)} early%={pct(ss, lambda s: s["el"] <= 300):3.0f} stat%={pct(ss, lambda s: s["movement"] == "stationary"):3.0f} ships={C(s["ship"] for s in ss).most_common(5)}')
