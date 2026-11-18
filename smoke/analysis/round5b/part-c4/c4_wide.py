# C4 sensitivity: the same spot search at a wider scale (circles 2.5 to 3.5 km radius), labels only. Writes wide.txt.
# Run after c4_spots.py: python -I -X utf8 c4_wide.py
import sys, os, io, contextlib
sys.argv.append('--nofig'); os.environ['C4_IMPORT'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c4_spots as c
from r5lib import *
c.H_KM, c.MERGE_KM, c.R_MIN, c.R_MAX, c.R_SEED = 1.5, 1.0, 2.5, 3.5, 3.0
c.RNG = random.Random(520)
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); out.append(line); print(line)
P('Wider scale: bandwidth 1.5 km, circle radius 2.5 to 3.5 km, same minimums (8 smokes and 10% of the kind on the map)')
ntop = n = 0; found = []
for m in c.MAPORDER:
    ms = [s for s in c.S if s['map'] == m]
    for fam, tag, jkind, test, plain in c.FAMILIES:
        pool = [s for s in ms if test(s)]
        for cx, cz, r, mem in sorted(c.find_spots(pool), key=lambda x: -len(x[3])):
            t = c.share_test(pool, mem); mode, note = c.label(t, mem); n += 1; ntop += mode == 'top6'
            found.append((pool, mem))
            P(f"{m} | {fam} | {c.where(m, cx, cz)} {c.cells_of(mem)} r {r / c.KM:.1f} km | n {len(mem)} (Top 6 {sum(s['grp'] == 'top' for s in mem)}, Rest {sum(s['grp'] == 'rest' for s in mem)}) | "
              f"share {t['st']:.0f}% vs {t['sr']:.0f}% | interval {'-' if t['lo'] is None else f'{t['lo']:+.0f} to {t['hi']:+.0f}'} | {mode} {note} | {clan_counts(mem)} | dmg {mean(s['conc'] for s in mem):,.0f}")
P(f'TOTAL wide spots {n}, labelled Top 6: {ntop}')
# placebo at the wide scale
rest_s = [s for s in c.S if s['grp'] == 'rest']; busy = [k for k, _ in C(s['team'] for s in rest_s).most_common(12)]
pl = []
for m in c.MAPORDER:
    ms = [s for s in rest_s if s['map'] == m]
    for fam, tag, jkind, test, plain in c.FAMILIES:
        pool = [s for s in ms if test(s)]
        for cx, cz, r, mem in c.find_spots(pool): pl.append((pool, mem))
cnt = []
for _ in range(200):
    fake = set(c.RNG.sample(busy, 6))
    cnt.append(sum(c.label(c.share_test(pool, mem, topset=fake, reps=400), mem, fake)[0] == 'top6' for pool, mem in pl))
P(f'PLACEBO wide: {len(pl)} Rest-only spots, labelled top by chance: mean {mean(cnt):.2f}, range {min(cnt)} to {max(cnt)}, draws with >= {ntop}: {100 * sum(x >= ntop for x in cnt) / len(cnt):.0f}%')
open(os.path.join(c.OUT, 'wide.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
