# Exploration only: sizes of early, radar and death clusters per map at the 2 km scale. Prints; writes nothing.
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_lib import *
S, G = load()
DD = [s for s in S if s['cls'] == 'destroyer']
print('early DD el<300:', sum(s['el'] < 300 and s['grp'] == 'top' for s in DD), sum(s['el'] < 300 and s['grp'] == 'rest' for s in DD),
      '| el<=300:', sum(s['el'] <= 300 and s['grp'] == 'top' for s in DD), sum(s['el'] <= 300 and s['grp'] == 'rest' for s in DD))
print('radar plays DD', sum(s['radar_play'] for s in DD), 'cruiser', sum(s['radar_play'] and s['cls'] == 'cruiser' for s in S), C(s['ship'] for s in S if s['radar_play'] and s['cls'] == 'cruiser'))
print('deaths DD smokes', sum(s['deaths'] > 0 for s in DD), 'deaths', sum(s['deaths'] for s in DD), '| all classes smokes', sum(s['deaths'] > 0 for s in S), sum(s['deaths'] for s in S))
def show(name, ss, m, h=H_KM):
    if not ss: print('  ', name, 'none'); return
    cl = mean_shift([(s['nx'], s['nz']) for s in ss], h)
    out = []
    for idx in cl[:6]:
        pts = [(ss[i]['nx'], ss[i]['nz']) for i in idx]
        cx, cz = mean(p[0] for p in pts), mean(p[1] for p in pts)
        out.append(f"{len(idx)} ({sum(ss[i]['grp'] == 'top' for i in idx)}T) {'/'.join(cells_of(m, pts, 2))} {side_words(G, m, cx, cz)}")
    print('  ', name, 'n', len(ss), '|', ' ; '.join(out))
for m in MAP_ORDER:
    ms = [s for s in DD if s['map'] == m]; allm = [s for s in S if s['map'] == m]
    print('==', m, len(ms))
    e = [s for s in ms if s['el'] < EARLY_S]
    show('early all', e, m); show('early top', [s for s in e if s['grp'] == 'top'], m)
    show('early 2.5', e, m, 2.5)
    show('radar DD', [s for s in ms if s['radar_play']], m); show('radar DD 3km', [s for s in ms if s['radar_play']], m, 3.0)
    print('   radar by ncap', dict(C(s['ncap'] for s in ms if s['radar_play'])), 'by nearest', dict(C(nearest_cap(G, m, s['nx'], s['nz'])[0] for s in ms if s['radar_play'])))
    show('radar Svea', [s for s in allm if s['radar_play'] and s['cls'] == 'cruiser'], m)
    show('deaths DD', [s for s in ms if s['deaths'] > 0], m); show('deaths all', [s for s in allm if s['deaths'] > 0], m)
    show('deaths all 2.5', [s for s in allm if s['deaths'] > 0], m, 2.5)
