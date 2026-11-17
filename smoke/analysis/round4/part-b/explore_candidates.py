# Prints every candidate spot with its test at three scales, plus placebo runs. Results are saved to checks.json for spots_build.py.
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spotlib import *
HERE_B = os.path.dirname(os.path.abspath(__file__))
S, G = load()
out = {'scales': {}, 'placebo': []}
for h in (1.5, 2.0, 2.5):
    t0 = time.time(); nsub, ncl, cands = candidates(S, h_km=h)
    print(f'\nbandwidth {h} km: subjects {nsub}, clusters {ncl}, candidates tested {len(cands)}, pass {sum(passes(c) for c in cands)}  ({time.time()-t0:.0f}s)')
    rows = []
    for c in sorted(cands, key=lambda c: -(c['gap'] if c['gap'] is not None else -999)):
        cx, cz, r1, r2, ang = c['e']
        cells = C(s['ncell_name'] for s in c['tin']).most_common(4)
        print(f"{'*' if passes(c) else ' '} {c['map']:15} {c['kind']:5} {c['subject']:22} top {len(c['tin'])}/{len(c['top'])} {c['ts']:.0f}%  rest {len(c['rin'])}/{len(c['rest'])} {n0(c['rs'])}%  gap {sg(c['gap'])} [{sg(c['lo'])},{sg(c['hi'])}]  wo {c['big']} {n0(c['ts_wo'])}%  clans {dict(c['clans'])}  r {r1*WU/1000:.1f}x{r2*WU/1000:.1f}km  {cells}")
        rows.append(dict(map=c['map'], subject=c['subject'], cx=cx, cz=cz, passes=passes(c), gap=c['gap'], lo=c['lo'], hi=c['hi'], n_in=len(c['tin'])))
    out['scales'][str(h)] = dict(subjects=nsub, clusters=ncl, candidates=len(cands), passed=sum(passes(c) for c in cands), rows=rows)

# Placebo: the real Top 6 are removed; six clans drawn from the eleven busiest Rest clans stand in as the "top" group against the
# remaining Rest. Same search, same rule. Spots that pass here are passing without any real Top 6 habit behind them.
cnt = C(s['team'] for s in S if s['team'] not in TOP)
busy = [t for t, n in cnt.most_common(11)]
rng = random.Random(4)
for i in range(20):
    fake = set(rng.sample(busy, 6))
    nsub, ncl, cands = candidates(S, topset=fake, exclude=TOP, h_km=2.0, reps=400, seed=100 + i)
    p = sum(passes(c) for c in cands)
    out['placebo'].append(dict(fake=sorted(fake), smokes=sum(cnt[t] for t in fake), subjects=nsub, candidates=len(cands), passed=p))
    print('placebo', i, sorted(fake), 'smokes', sum(cnt[t] for t in fake), 'subjects', nsub, 'candidates', len(cands), 'pass', p)
json.dump(out, open(os.path.join(HERE_B, 'checks.json'), 'w', encoding='utf-8'), indent=1)
