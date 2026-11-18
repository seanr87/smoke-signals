# D1: score every clan on the six dimensions. Writes d1_scores.json (values, intervals, percentiles, notes) and prints tables.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_lib import *
HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(519)

V = {t: feats(t, strict=True) for t in CLANS}
I = {t: boot_clan(t) for t in CLANS}
POOL = {k: [V[t][k] for t in CLANS7 if V[t][k] is not None] for k in ALLKEYS}
PC = {t: {k: pctile(V[t][k], POOL[k]) for k in ALLKEYS} for t in CLANS}

# sanity
dd = [s for s in S if s['cls'] == 'destroyer']
print('smokes', len(S), 'sum over clans', sum(V[t]['n_smokes'] for t in CLANS), '| games', len(G), 'team-games', sum(NG.values()),
      '| DD smokes top/rest', sum(s['grp'] == 'top' for s in dd), sum(s['grp'] == 'rest' for s in dd))
print('clans', len(CLANS), '7+ games', len(CLANS7), 'small', SMALL)
print('ships with smoke_variant not in any list:', C(nb(p['ship']) for r in RO.values() for p in r if carries(p)).most_common(40))
print('long/sitter ships WITHOUT smoke_variant:', C(nb(p['ship']) for r in RO.values() for p in r if not carries(p) and nb(p['ship']) in LONG_SHIPS + SITTERS + EXHAUST + PARKED_CA))
print('min n: dd smokes', min((V[t]['n_dd_smokes'], t) for t in CLANS7), 'take known', min((V[t]['n_take_known'], t) for t in CLANS7), 'hold known', min((V[t]['n_hold_known'], t) for t in CLANS7))
print('movement labels', C(s['movement'] for s in S))
print('no taken answer', sum(s['we_took'] is None for s in S), '| not-lost answer within 2 km', sum(s['enemy_took'] is not None and s['near_cap_edge_m'] <= HOLD_NEAR_M for s in S), 'of', len(S),
      '| clans (7+ games) with under 8 such smokes:', [(t, V[t]['n_hold_known']) for t in CLANS7 if V[t]['n_hold_known'] < 8])

# notes per clan: smoke ships brought (share of games), ships inside the clan's destroyer smokes, caps
NOTES = {}
SMOKE_SHIPS = [x for x, _ in C(nb(p['ship']) for r in RO.values() for p in r if carries(p)).most_common()]
for t in CLANS:
    n = NG[t]; ss = [s for s in S if s['team'] == t]; dds = [s for s in ss if s['cls'] == 'destroyer']
    brought = C()
    for k in GAMES[t]:
        for sh in {nb(p['ship']) for p in RO[(t, k)] if carries(p)}: brought[sh] += 1
    ins = C()
    for s in dds:
        for sh in {nb(p['ship']) for p in s['partners'] if p['how'] == 'inside'}: ins[sh] += 1
    caps = C((s['map'], s['near_ncap']) for s in ss)
    role = C(s['j']['classification'].get('cap_role') for s in ss)
    NOTES[t] = dict(
        smoke_ships_share_of_games={sh: round(100 * c / n) for sh, c in brought.most_common()},
        ships_inside_dd_smokes=({sh: round(100 * c / len(dds)) for sh, c in ins.most_common(5)} if len(dds) >= 8 else 'too few destroyer smokes'),
        n_dd_smokes=len(dds),
        top_caps=[f'{m} {c} ({k})' for (m, c), k in caps.most_common(3)],
        cap_role_pct={r: round(100 * c / len(ss)) for r, c in role.most_common()},
        lane_pct={l: round(100 * c / len(ss)) for l, c in C(s['lane'] for s in ss).most_common()},
        movement_pct={MOVE[m]: round(100 * c / len(ss)) for m, c in C(s['movement'] for s in ss).most_common()})

def fmt(k, v):
    if v is None: return 'too few'
    if k.endswith('_pg') and k != 'conc_pg': return f'{v:.1f}'
    if k in ('conc_pg', 'conc_per_smoke', 'edge_m'): return f'{v:,.0f}'
    if k == 'first_smoke_s': return f'{int(v) // 60}:{int(v) % 60:02d}'
    return f'{v:.0f}'
def row(t, keys):
    return [('*' if t in TOP else '') + t + (' (flag)' if t in SMALL else ''), f'{WLD[t][0]}-{WLD[t][1]}', V[t]['n_smokes']] + [fmt(k, V[t][k]) for k in keys]
out = []
for d in DIMS + [dict(name='Extra', keys=['smoke_ships_pg', 'dd_pg', 'early_pct', 'selfish_pct', 'cruiser_inside_pct', 'sideways_pct', 'caps_taken_pg', 'cap_won_pg', 'cap_def_pg', 'deaths_pg'])]:
    out.append(f"\n#### {d['name']}\n")
    out.append(md_table(['Clan', 'W-L', 'Smokes'] + [LABEL[k] for k in d['keys']], [row(t, d['keys']) for t in CLANS]))
out.append('\n#### Headline value, 95% interval (games resampled within the clan), percentile among the 24 clans\n')
hk = [d['headline'] for d in DIMS]
out.append(md_table(['Clan', 'Games'] + [LABEL[k] for k in hk],
                    [[('*' if t in TOP else '') + t + (' (flag)' if t in SMALL else ''), NG[t]] +
                     [f"{fmt(k, V[t][k])} ({fmt(k, I[t][k][0])} to {fmt(k, I[t][k][1])}) p{PC[t][k]:.0f}" if V[t][k] is not None else 'too few' for k in hk] for t in CLANS]))
out.append('\n#### Smoke ships brought (share of games) and ships inside destroyer smokes (share of destroyer smokes)\n')
out.append(md_table(['Clan', 'Games', 'Brings (share of games)', 'DD smokes', 'Inside its destroyer smokes', 'Most-used caps (smokes)', 'Centre / flank lanes'],
                    [[('*' if t in TOP else '') + t + (' (flag)' if t in SMALL else ''), NG[t],
                      ', '.join(f'{a} {b}%' for a, b in list(NOTES[t]['smoke_ships_share_of_games'].items())[:6]), NOTES[t]['n_dd_smokes'],
                      NOTES[t]['ships_inside_dd_smokes'] if isinstance(NOTES[t]['ships_inside_dd_smokes'], str) else (', '.join(f'{a} {b}%' for a, b in list(NOTES[t]['ships_inside_dd_smokes'].items())[:4]) or 'none recorded'),
                      '; '.join(NOTES[t]['top_caps']), f"{NOTES[t]['lane_pct'].get('center', 0)} / {100 - NOTES[t]['lane_pct'].get('center', 0)}"] for t in CLANS]))

# field-wide lineup shares and inside ships (Top 6 vs Rest), for the D1 answer
def grp_brings(clans):
    n = sum(NG[t] for t in clans); c = C()
    for t in clans:
        for k in GAMES[t]:
            for sh in {nb(p['ship']) for p in RO[(t, k)] if carries(p)}: c[sh] += 1
    return {sh: 100 * v / n for sh, v in c.items()}, n
def grp_inside(clans):
    dds = [s for s in S if s['team'] in clans and s['cls'] == 'destroyer']; c = C()
    for s in dds:
        for sh in {nb(p['ship']) for p in s['partners'] if p['how'] == 'inside'}: c[sh] += 1
    return {sh: 100 * v / len(dds) for sh, v in c.items()}, len(dds)
top = [t for t in CLANS if t in TOP]; rest = [t for t in CLANS if t not in TOP]
bt, nt = grp_brings(top); br, nr = grp_brings(rest)
out.append(f'\n#### Smoke ships brought, share of games: Top 6 ({nt} team-games) vs Rest ({nr})\n')
def clan_diff(f, reps=1000):
    """95% interval of f(top clans) - f(rest clans), resampling whole clans."""
    o = []
    for _ in range(reps):
        o.append(f(random.choices(top, k=len(top))) - f(random.choices(rest, k=len(rest))))
    o.sort(); return o[int(.025 * len(o))], o[int(.975 * len(o)) - 1]
rows = []
for sh in sorted(set(bt) | set(br), key=lambda x: -(bt.get(x, 0) * nt + br.get(x, 0) * nr))[:14]:
    lo, hi = clan_diff(lambda cl: grp_brings(cl)[0].get(sh, 0))
    rows.append([sh, f'{bt.get(sh, 0):.0f}%', f'{br.get(sh, 0):.0f}%', ci((lo, hi), '{:+.0f}')])
out.append(md_table(['Ship', 'Top 6', 'Rest', 'Gap (95%, clans resampled)'], rows))
it, mt = grp_inside(top); ir, mr = grp_inside(rest)
out.append(f'\n#### Ships inside destroyer smokes, share of destroyer smokes: Top 6 (n {mt}) vs Rest (n {mr})\n')
rows = []
for sh in sorted(set(it) | set(ir), key=lambda x: -(it.get(x, 0) * mt + ir.get(x, 0) * mr))[:10]:
    lo, hi = clan_diff(lambda cl: grp_inside(cl)[0].get(sh, 0))
    rows.append([sh, f'{it.get(sh, 0):.0f}%', f'{ir.get(sh, 0):.0f}%', ci((lo, hi), '{:+.0f}')])
out.append(md_table(['Ship inside', 'Top 6', 'Rest', 'Gap (95%, clans resampled)'], rows))

# Top 6 minus Rest on every score: group value (pooled games) and clan-resampled interval
out.append('\n#### Top 6 minus Rest on every score (pooled over the group\'s games; 95% interval, whole clans resampled)\n')
def pooled(cl, k):
    return feats(cl[0], [g for t in cl for g in GAMES[t]]) if False else None
def grp_feats(cl):
    # pool by treating the group as one clan: temporary keys
    games = []
    for i, t in enumerate(cl):
        for g in GAMES[t]:
            key = ('_grp', i, t, g); SG[('_grp', key)] = SG[(t, g)]; RO[('_grp', key)] = RO[(t, g)]; games.append(key)
    return feats('_grp', games)
ft, fr = grp_feats(top), grp_feats(rest)
GAPS = {}
rows = []
random.seed(1000)
REPS = [(grp_feats(random.choices(top, k=len(top))), grp_feats(random.choices(rest, k=len(rest)))) for _ in range(500)]
for k in ALLKEYS:
    o = sorted(a[k] - b[k] for a, b in REPS if a[k] is not None and b[k] is not None)
    lo, hi = o[int(.025 * len(o))], o[int(.975 * len(o)) - 1]
    GAPS[k] = dict(top6=ft[k], rest=fr[k], lo=lo, hi=hi, clear=lo * hi > 0)
    rows.append([LABEL[k], fmt(k, ft[k]), fmt(k, fr[k]), f'{lo:+,.1f} to {hi:+,.1f}' + (' *' if lo * hi > 0 else '')])
out.append(md_table(['Score', 'Top 6', 'Rest', 'Gap (95%)'], rows))
print('group n: top smokes', ft['n_smokes'], 'games', ft['n_games'], '| rest smokes', fr['n_smokes'], 'games', fr['n_games'])

open(os.path.join(HERE, 'd1_tables.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for t in CLANS:
    for k in ALLKEYS:
        if V[t][k] is None: I[t].pop(k, None)
json.dump(dict(values=V, intervals=I, percentiles=PC, notes=NOTES, gaps=GAPS, group=dict(top6=ft, rest=fr)), open(os.path.join(HERE, 'd1_scores.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote d1_tables.md, d1_scores.json')
