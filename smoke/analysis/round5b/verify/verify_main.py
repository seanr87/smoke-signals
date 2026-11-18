# Independent recheck of headline numbers from parts A, C1 and C4 (written by the main session, not by the workers).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
S, G = load5()
D = [s for s in S if s['cls'] == 'destroyer']
def p(v): return '-' if v is None else f'{v:.1f}'
print('A1 cap-contest destroyer smokes', len([s for s in D if 'cap_contest' in s['tags']]))
for grp in ('top', 'rest'):
    for cov in ('radar cruiser inside', 'no cruiser'):
        ss = [s for s in D if 'cap_contest' in s['tags'] and s['cover3'] == cov and s['grp'] == grp]
        e = [s for s in ss if s['we_took'] is not None]
        print(' ', grp, cov, 'n', len(ss), 'cap taken', p(pct(e, lambda s: s['we_took'])), 'of', len(e), 'conc', round(mean(s['conc'] for s in ss)))
print('A2 deaths per 100 destroyer smokes: top', p(rate100([s for s in D if s['grp']=='top'], 'deaths')), 'rest', p(rate100([s for s in D if s['grp']=='rest'], 'deaths')))
print('   smoker died per 100: all', p(rate100(D, 'd_smoker')), 'cruiser per 100 sheltering', p(100*sum(s['d_cr'] for s in D)/sum(s['n_cr_in'] for s in D)), sum(s['n_cr_in'] for s in D))
def broad(s): return any(any(k['kind']=='radar' for k in x.get('detected_by', [])) for x in s['j']['smokees'] if x['how']!='none')
calm = [s for s in D if s['state'] != 'behind 50+' and not broad(s) and s['radar_on_us'] == 0]
print('   calm smokes', len(calm), 'deaths', sum(s['deaths'] for s in calm), p(rate100(calm, 'deaths')), '| total deaths', sum(s['deaths'] for s in D))
for st in ('ahead 50+', 'level', 'behind 50+'):
    ss = [s for s in D if s['state'] == st]; print('  ', st, len(ss), p(rate100(ss, 'deaths')), 'top', p(rate100([s for s in ss if s['grp']=='top'],'deaths')), 'rest', p(rate100([s for s in ss if s['grp']=='rest'],'deaths')))
for ship in ('Somers', 'Gearing'):
    for grp in ('top', 'rest'):
        ss = [s for s in D if s['ship'] == ship and s['grp'] == grp]; print('A3', ship, grp, len(ss), p(rate100(ss, 'deaths')))
cs = [s for s in D if s['counter_of']]
print('A4 counter smokes with id', len(cs), 'radar cruiser inside', len([s for s in cs if s['radar_ca_inside']]), round(mean(s['conc'] for s in cs if s['radar_ca_inside'])), 'all', round(mean(s['conc'] for s in cs)))
print('C1 cap_defended share', p(pct(S, lambda s: s['cap_def'])), sum(s['cap_def'] for s in S))
e = [s for s in S if s['enemy_took'] is not None]; print('   enemy_took yes', sum(s['enemy_took'] for s in e), 'no', len(e)-sum(s['enemy_took'] for s in e), 'n/a', len(S)-len(e))
for grp in ('top', 'rest'):
    ee = [s for s in e if s['cls']=='destroyer' and s['grp']==grp and s['near_cap_edge_m'] <= 2000]; print('   dd within 2 km', grp, len(ee), p(pct(ee, lambda s: s['enemy_took'])))
hs = [s for s in D if s['map']=='Hotspot' and s['near_cap_edge_m'] < 0 and s['near_ncap']=='C']
print('C3 Hotspot inside C', len(hs), 'hurt', sum(s['hurt_smoker'] for s in hs), clan_counts(hs))
g1 = [s for s in D if s['map']=='Sleeping Giant' and s['ncell_name']=='G1']; oth = [s for s in D if s['map']=='Sleeping Giant' and s['ncell_name']!='G1']
print('C4 SG G1', len(g1), round(mean(s['conc'] for s in g1)), 'elsewhere', round(mean(s['conc'] for s in oth)))
# C2 reference row: more caps at 8:00
w = n = 0
for k, g in G.items():
    h = cap_holders(S, G, k)
    if not h: continue
    c = C(v for v in h.values() if v)
    a, b = g['teams']
    if c[a] == c[b]: continue
    lead = a if c[a] > c[b] else b; n += 1; w += g['winner'] == lead
print('C2 more caps at 8:00 won', w, 'of', n)
