# Part B: signature spots. Finds the spots, measures each one and its supporting cast, writes SPOTS.md, spots.json and the figures.
# Run from the repo root: python -I -X utf8 smoke/analysis/round4/part-b/spots_build.py
# (explore_candidates.py must have been run once: it writes checks.json with the scale and placebo checks.)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spotlib import *
OUT = os.path.dirname(os.path.abspath(__file__))
S, G = load()
CHK = json.load(open(os.path.join(OUT, 'checks.json'), encoding='utf-8'))
MAPAB = {'Sleeping Giant': 'sg', 'Hotspot': 'hs', 'Mountain Range': 'mr', 'Land of Fire': 'lof', 'Sea of Fortune': 'sof', 'Loop': 'loop', 'Okinawa': 'oki'}
km = lambda units: units * WU / 1000

nsub, ncl, cands = candidates(S)
for c in cands:
    c['cells'] = [k for k, v in C(s['ncell_name'] for s in c['tin']).most_common() if v >= 2] or [c['tin'][0]['ncell_name']]
    c['id'] = f"{MAPAB[c['map']]}-{c['subject'].split()[0].lower().replace('.', '')}-{c['cells'][0].lower()}".replace('ń', 'n')
def same_place(a, b): return a['map'] == b['map'] and math.hypot(a['e'][0] - b['e'][0], a['e'][1] - b['e'][1]) <= 3 * KM

# classify: signature / lead / other. A ship spot and a habit spot in the same place: keep the ship if it passes, else the habit.
sig = [c for c in cands if passes(c)]
drop = set()
for a in sig:
    for b in sig:
        if a is not b and a['kind'] == 'ship' and b['kind'] == 'habit' and HABIT.get(a['subject']) == b['subject'] and same_place(a, b):
            drop.add(id(b)); a.setdefault('dup', []).append(b)
sig = sorted([c for c in sig if id(c) not in drop], key=lambda c: -c['gap'])
lead = []
for c in cands:
    if passes(c) or any(c is d for a in sig for d in a.get('dup', [])): continue
    if len(c['clans']) < 2 or c['gap'] is None or c['gap'] < 10: continue
    if c['kind'] == 'habit' and any(o is not c and o['kind'] == 'ship' and HABIT.get(o['subject']) == c['subject'] and same_place(o, c) and o['gap'] >= 10 and len(o['clans']) >= 2 for o in cands): continue
    c['twin'] = next((a for a in sig if same_place(a, c)), None)
    lead.append(c)
lead.sort(key=lambda c: -c['gap'])
single = [c for c in cands if len(c['clans']) < 2 and c['gap'] and c['gap'] >= 10]
reverse = [c for c in cands if c['hi'] is not None and c['hi'] < 0]

LABEL = {  # plain-words names, written after looking at the map views
    'sof-svea-h7': 'open water on the own side of cap D, south-east',
    'lof-svea-f5': 'own-side rim of cap B, centre of the map',
    'loop-cap-f7': 'own-side and east half of cap B',
    'mr-parked-h1': 'far west edge, own-side rim of the big cap A',
    'sg-harugumo-g1': 'west edge, own side of cap A',
    'sg-flank-f9': 'east edge, outside cap D',
    'loop-gdansk-f8': 'own-side rim of cap B',
    'sg-somers-f9': 'east edge, outside cap D',
    'mr-svea-g4': 'own side of cap B, west-centre',
    'hs-flank-g6': 'own-side rim of cap C, centre',
    'sg-gdansk-g6': 'between caps B and D, own side',
}

def cap_xy(s):
    c = next((c for c in ncaps(G[s['game']], s['map'], s['side']) if c['cap'] == s['cap']), None)
    return (c['x'], c['z'], c['r']) if c else None

def cast_of(ss):
    """Supporting cast over a list of smokes, at the moment each smoke was fully laid."""
    n = len(ss); o = dict(n=n)
    near = [(s, a) for s in ss for a in s['cast'] if a['ally'] and not a['is_smoker'] and a['dist_m'] <= 5000]
    o['near_per_smoke'] = len(near) / n if n else None
    o['near_cls'] = C((a['cls'], 'inside' if a['how'] == 'inside' else 'behind' if a['how'] == 'behind' else 'outside') for _, a in near)
    o['near_ship'] = C(a['ship'] for _, a in near)
    o['near_med'] = med(a['dist_m'] for _, a in near)
    # cruiser inside (not the smoker), by the batch's own inside test
    cr = [(s, a) for s in ss for a in s['cast'] if a['ally'] and not a['is_smoker'] and a['cls'] == 'cruiser' and a['how'] == 'inside']
    o['cr_smokes'] = len({id(s) for s, _ in cr}); o['cr_ship'] = C(a['ship'] for _, a in cr)
    o['cr_radar'] = len({id(s) for s, a in cr if a['radar']})
    o['cr_pos'] = (mean(a['nx'] for _, a in cr), mean(a['nz'] for _, a in cr)) if cr else None
    o['cr_dist'] = med(a['dist_m'] for _, a in cr)
    # nearest allied destroyer that is not the smoker
    dd = []
    for s in ss:
        d = [a for a in s['cast'] if a['ally'] and not a['is_smoker'] and a['cls'] == 'destroyer']
        if d: dd.append((s, min(d, key=lambda a: a['dist_m'])))
    o['dd_n'] = len(dd); o['dd_ship'] = C(a['ship'] for _, a in dd)
    o['dd_fwd'] = sum(a['fwd_m'] > 0 for _, a in dd); o['dd_dist'] = med(a['dist_m'] for _, a in dd); o['dd_fwd_m'] = med(a['fwd_m'] for _, a in dd)
    o['dd_pos'] = (mean(a['nx'] for _, a in dd), mean(a['nz'] for _, a in dd)) if dd else None
    o['dd_cell'] = C(cell_name(*cell(s['map'], a['nx'], a['nz'])) for s, a in dd)
    o['dd_how'] = C(a['how'] for _, a in dd)
    capd = []
    for s, a in dd:
        c = cap_xy(s)
        if c: capd.append((math.hypot(a['nx'] - c[0], a['nz'] - c[1]) - c[2]) * WU)
    o['dd_cap_edge'] = med(capd); o['dd_in_cap'] = sum(d < 0 for d in capd); o['dd_cap_n'] = len(capd)
    # stand-in for the spotter: the allied ship nearest each damaged enemy
    nt = C(); ntship = C(); ntd = []; unk = 0
    for s in ss:
        allies = [a for a in s['cast'] if a['ally']]
        for t in s['targets']:
            if t['nx'] is None or not allies: unk += 1; continue
            a = min(allies, key=lambda a: math.hypot(a['nx'] - t['nx'], a['nz'] - t['nz']))
            role = 'the smoker' if a['is_smoker'] else 'a ship inside the smoke' if a['how'] == 'inside' else 'another ship'
            nt[role] += 1; ntship[(role, a['ship'], a['cls'])] += 1; ntd.append(math.hypot(a['nx'] - t['nx'], a['nz'] - t['nz']) * WU)
    o['nt'] = nt; o['nt_ship'] = ntship; o['nt_dist'] = med(ntd); o['nt_n'] = sum(nt.values()); o['nt_unknown'] = unk
    # formation: (cruiser inside?, second destroyer forward / back / none)
    def form(s):
        ci = any(a['ally'] and not a['is_smoker'] and a['cls'] == 'cruiser' and a['how'] == 'inside' for a in s['cast'])
        d = [a for a in s['cast'] if a['ally'] and not a['is_smoker'] and a['cls'] == 'destroyer']
        return ci, ('none' if not d else 'forward' if min(d, key=lambda a: a['dist_m'])['fwd_m'] > 0 else 'back')
    o['form'] = C(form(s) for s in ss); o['form_fn'] = form
    return o

def describe(c):
    t, r = c['tin'], c['rin']; e = c['e']
    c['label'] = LABEL.get(c['id'], 'around ' + '/'.join(c['cells'][:2]))
    c['med_el'] = med(s['el'] for s in t)
    pc = C(sh for s in t for sh in {p['ship'] for p in s['partners']})
    c['partner'] = pc.most_common(1)[0] if pc else None
    c['conc'] = mean(s['conc'] for s in t); c['deaths'] = 100 * mean(s['deaths'] for s in t)
    cw = [s for s in t if s['own'] != 'ours']; c['capwon_n'] = len(cw); c['capwon'] = pct(cw, lambda s: s['cap_won']) if cw else None
    c['rconc'] = mean(s['conc'] for s in r) if r else None
    c['edge'] = med(s['edge'] for s in t); c['redge_all'] = med(s['edge'] for s in c['rest']) if c['rest'] else None; c['tedge_all'] = med(s['edge'] for s in c['top'])
    c['cap'] = C(s['ncap'] for s in t).most_common(1)[0][0]
    cx, cz = e[0], e[1]
    ex = sorted(t, key=lambda s: math.hypot(s['nx'] - cx, s['nz'] - cz)); seen = set(); c['examples'] = []
    for s in ex:  # nearest to the centre, one per clan first
        if s['team'] not in seen: c['examples'].append(s); seen.add(s['team'])
    c['examples'] = (c['examples'] + [s for s in ex if s not in c['examples']])[:3]
    c['ct'] = cast_of(t); c['cr'] = cast_of(r) if r else None
    key = c['ct']['form'].most_common(1)[0][0]; c['fkey'] = key
    c['f_top'] = c['ct']['form'][key]; c['f_rest'] = c['cr']['form'][key] if c['cr'] else 0
    c['pn'] = sum(1 for s in S if s['is_pn'] and s['map'] == c['map'] and s[c['kind']] == c['subject'] and inside(e, s['nx'], s['nz']))
    c['pn_total'] = sum(1 for s in S if s['is_pn'] and s['map'] == c['map'] and s[c['kind']] == c['subject'])
for c in sig + lead: describe(c)

def top1(cnt, k=1): return ', '.join(f'{a} {b}' for a, b in cnt.most_common(k))
def form_words(c, key=None):
    ci, dd = key or c['fkey']; ct = c['ct']
    a = f"a cruiser inside ({top1(ct['cr_ship'])})" if ci else 'no other cruiser inside'
    b = {'forward': f"second destroyer forward of the smoke (most often in {top1(ct['dd_cell']).split()[0]})", 'back': f"second destroyer level with or behind the smoke (most often in {top1(ct['dd_cell']).split()[0]})", 'none': 'no second destroyer on the map'}[dd]
    subj = {'cap sitters': 'cap-sitter', 'flank smoke lines': 'flank-line destroyer', 'parked cruiser smoke': 'parked cruiser'}.get(c['subject'], c['subject'])
    return f"{subj} smoke at {'/'.join(c['cells'][:2])} + {a} + {b}"
def mmss(x): return f'{int(x) // 60}:{int(x) % 60:02d}'

# ---------- cross-map cast pattern: a radar cruiser inside plus a second destroyer forward, all destroyer smokes
dds = [s for s in S if s['cls'] == 'destroyer']
def second_dd_fwd(s):
    d = [a for a in s['cast'] if a['ally'] and not a['is_smoker'] and a['cls'] == 'destroyer']
    return bool(d) and min(d, key=lambda a: a['dist_m'])['fwd_m'] > 0
PATS = {'radar cruiser inside + second destroyer forward': lambda s: s['radar_ca_inside'] and second_dd_fwd(s),
        'radar cruiser inside': lambda s: s['radar_ca_inside'],
        'any cruiser inside': lambda s: any(a['ally'] and not a['is_smoker'] and a['cls'] == 'cruiser' and a['how'] == 'inside' for a in s['cast']),
        'second destroyer forward': second_dd_fwd,
        'second destroyer alive with a known position': lambda s: any(a['ally'] and not a['is_smoker'] and a['cls'] == 'destroyer' for a in s['cast'])}
rngp = random.Random(7); pat = {}
for name, f in PATS.items():
    t = [s for s in dds if s['grp'] == 'top']; r = [s for s in dds if s['grp'] == 'rest']
    pat[name] = dict(top=pct(t, f), rest=pct(r, f), nt=len(t), nr=len(r), ci=boot_gap(t, r, f, 1000, rngp),
                     maps={m: (pct([s for s in t if s['map'] == m], f), pct([s for s in r if s['map'] == m], f), sum(s['map'] == m for s in t)) for m in MAPS})
    print(name, {k: v for k, v in pat[name].items() if k != 'maps'}); print('   ', {m: (n0(a), n0(b), n) for m, (a, b, n) in pat[name]['maps'].items()})
HEAD = 'radar cruiser inside + second destroyer forward'
# the same pattern inside the signature destroyer spots
spot_dd = [s for c in sig if c['tin'][0]['cls'] == 'destroyer' for s in c['tin']]
print('pattern in signature DD spots', pct(spot_dd, PATS[HEAD]), len(spot_dd))

# ---------- explicit check: Sleeping Giant, Top 6 Harugumo at G1/F1
chk = next(c for c in sig + lead if c['id'] == 'sg-harugumo-g1')
ck = chk['ct']

# ---------- console dump
for c in sig + lead:
    ct = c['ct']; e = c['e']
    print(f"\n== {'SIG ' if c in sig else 'LEAD'} {c['id']} | {c['map']} | {c['subject']} | {c['cells']} | centre ({e[0]:.0f},{e[1]:.0f}) r {km(e[2]):.1f}x{km(e[3]):.1f} km ang {math.degrees(e[4]):.0f}")
    print(f"   top {len(c['tin'])}/{len(c['top'])} {c['ts']:.0f}% rest {len(c['rin'])}/{len(c['rest'])} {c['rs']:.0f}% gap {c['gap']:+.0f} [{c['lo']:+.0f},{c['hi']:+.0f}] clans {dict(c['clans'])} without {c['big']}: {c['ts_wo']:.0f}%")
    print(f"   t {mmss(c['med_el'])} partner {c['partner']} conc {c['conc']:.0f} deaths/100 {c['deaths']:.0f} capwon {n0(c['capwon'])}% of {c['capwon_n']} | edge spot {c['edge']:.0f} top-all {c['tedge_all']:.0f} rest-all {n0(c['redge_all'])} cap {c['cap']} PN {c['pn']}/{c['pn_total']}")
    print(f"   near/smoke {ct['near_per_smoke']:.1f} {dict(ct['near_cls'])} ships {ct['near_ship'].most_common(5)}")
    print(f"   cruiser inside {ct['cr_smokes']}/{ct['n']} radar {ct['cr_radar']} {ct['cr_ship'].most_common(4)} dist {n0(ct['cr_dist'])}")
    print(f"   2nd DD {ct['dd_n']}/{ct['n']} {ct['dd_ship'].most_common(4)} fwd {ct['dd_fwd']} dist {n0(ct['dd_dist'])} fwd_m {n0(ct['dd_fwd_m'])} cells {ct['dd_cell'].most_common(4)} how {dict(ct['dd_how'])} cap edge {n0(ct['dd_cap_edge'])} in cap {ct['dd_in_cap']}/{ct['dd_cap_n']}")
    print(f"   nearest to target {dict(ct['nt'])} of {ct['nt_n']} (unknown {ct['nt_unknown']}) med {n0(ct['nt_dist'])} {ct['nt_ship'].most_common(5)}")
    print(f"   formation top {dict(ct['form'])} rest {dict(c['cr']['form']) if c['cr'] else None}")
print('\nsingle-clan:', [(c['id'], dict(c['clans']), round(c['gap'])) for c in single])
print('reverse:', [(c['id'], round(c['gap']), round(c['lo']), round(c['hi']), len(c['tin']), len(c['rin'])) for c in reverse])

# ---------- figures
os.makedirs(os.path.join(OUT, 'maps'), exist_ok=True)  # Panel links the minimap as ../maps/ relative to the figure folder
for mm in MAPS.values():
    src = os.path.join(MAP_SRC, mm['image'].replace('.png', '.webp')); dst = os.path.join(OUT, 'maps', os.path.basename(src))
    if not os.path.exists(dst): shutil.copyfile(src, dst)
def ell_svg(p, e, stroke=INK, width=2, dash=None):
    px, py = p.xy(e[0], e[1]); d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{e[2] / p.space * p.size:.1f}" ry="{e[3] / p.space * p.size:.1f}" transform="rotate({-math.degrees(e[4]):.1f} {px:.1f} {py:.1f})" '
            f'fill="none" stroke="{stroke}" stroke-width="{width}"{d}/>')
def diamond(p, x, z, r=7, fill=VIOLET):
    px, py = p.xy(x, z); return f'<polygon points="{px:.1f},{py-r:.1f} {px+r:.1f},{py:.1f} {px:.1f},{py+r:.1f} {px-r:.1f},{py:.1f}" fill="{fill}" stroke="{BG}" stroke-width="1.5"/>'
def tri(p, x, z, r=7, fill=GREEN):
    px, py = p.xy(x, z); return f'<polygon points="{px:.1f},{py-r:.1f} {px+r*.9:.1f},{py+r*.75:.1f} {px-r*.9:.1f},{py+r*.75:.1f}" fill="{fill}" stroke="{BG}" stroke-width="1.5"/>'
def cross(p, x, z, r=4, col=RED):
    px, py = p.xy(x, z); return f'<path d="M{px-r:.1f},{py-r:.1f} L{px+r:.1f},{py+r:.1f} M{px-r:.1f},{py+r:.1f} L{px+r:.1f},{py-r:.1f}" stroke="{col}" stroke-width="1.8" fill="none"/>'

PS, GAPX = 380, 36
for m in MAPS:
    cs = [c for c in sig + lead if c['map'] == m]
    if not cs: continue
    cols = min(3, len(cs)); rows = (len(cs) + cols - 1) // cols
    W = max(1010, 40 + cols * (PS + GAPX)); Hh = 100 + rows * (PS + 108)
    fig = Fig(W, Hh, f'{m}: where Top 6 concentrate a ship or habit more than the Rest',
              f'Each dot is the centre of one laid smoke, team-normalized ({NORM_NOTE[m]}). Outline = the spot (solid = signature, dashed = lead).')
    fig.legend(40, 72, [('Top 6 smoke', BLUE), ('Rest smoke', ORANGE), ('mean cruiser inside (Top 6, spot)', VIOLET), ('mean second destroyer (Top 6, spot)', GREEN)])
    for i, c in enumerate(cs):
        x0 = 40 + (i % cols) * (PS + GAPX); y0 = 118 + (i // cols) * (PS + 108)
        p = Panel(m, x0, y0, PS, G, title=f"{'Signature' if c in sig else 'Lead'}: {c['subject']}, {c['label']}")
        for s in c['rest']: p.dot(s['nx'], s['nz'], r=3.2, fill=ORANGE, opacity=0.75, stroke=BG)
        for s in c['top']: p.dot(s['nx'], s['nz'], r=3.2, fill=BLUE, opacity=0.8, stroke=BG)
        p.raw(ell_svg(p, c['e'], dash=None if c in sig else '6 4'))
        ct = c['ct']
        if ct['dd_pos'] and ct['dd_n'] >= 3: p.raw(tri(p, *ct['dd_pos']))
        if ct['cr_pos'] and ct['cr_smokes'] >= 3: p.raw(diamond(p, *ct['cr_pos']))
        fig.add(p)
        yy = y0 + PS + 30
        fig.add(T(x0, yy, f"In the spot: Top 6 {len(c['tin'])}/{len(c['top'])} ({c['ts']:.0f}%), Rest {len(c['rin'])}/{len(c['rest'])} ({c['rs']:.0f}%). Gap {c['gap']:+.0f} ({c['lo']:+.0f} to {c['hi']:+.0f}).", size=11, fill=INK, anchor='start'))
        fig.add(T(x0, yy + 16, f"Cruiser inside: {ct['cr_smokes']} of {ct['n']} Top 6 smokes" + (f" ({top1(ct['cr_ship'], 2)})" if ct['cr_smokes'] else '') + '.', size=11, anchor='start'))
        fig.add(T(x0, yy + 32, f"2nd destroyer: position recorded {ct['dd_n']} of {ct['n']}, forward of the smoke {ct['dd_fwd']}" + (f" ({top1(ct['dd_ship'], 1)})" if ct['dd_n'] else '') + '.', size=11, anchor='start'))
    fig.save(os.path.join(OUT, 'fig', 'spots-' + MAPAB[m]))

# explicit check figure
fig = Fig(1040, 650, 'Check: Sleeping Giant, Top 6 Harugumo smoke on the west edge by cap A (G1/F1)',
          f"{len(chk['tin'])} Top 6 smokes in the spot. Positions are from the one moment the batch records: when each smoke was fully laid. {NORM_NOTE['Sleeping Giant'].capitalize()}.")
fig.legend(40, 72, [('Harugumo smoke (laid path)', BLUE), ('cruiser inside', VIOLET), ('nearest other destroyer', GREEN), ('enemy damaged from the smoke', RED)])
p1 = Panel('Sleeping Giant', 40, 118, 470, G, title='The smokes and who was with them')
p2 = Panel('Sleeping Giant', 550, 118, 470, G, title='Enemies damaged, joined to the nearest allied ship')
for p in (p1, p2):
    p.raw(ell_svg(p, chk['e'], width=1.5))
    for s in chk['tin']: p.line(s['npath'], stroke=BLUE, width=5, opacity=0.55)
for s in chk['tin']:
    for a in s['cast']:
        if a['ally'] and not a['is_smoker'] and a['cls'] == 'cruiser' and a['how'] == 'inside': p1.raw(diamond(p1, a['nx'], a['nz'], r=5))
    d = [a for a in s['cast'] if a['ally'] and not a['is_smoker'] and a['cls'] == 'destroyer']
    if d:
        a = min(d, key=lambda a: a['dist_m']); p1.line([(s['nx'], s['nz']), (a['nx'], a['nz'])], stroke=GREEN, width=1, opacity=0.6); p1.raw(tri(p1, a['nx'], a['nz'], r=5))
    allies = [a for a in s['cast'] if a['ally']]
    for t in s['targets']:
        if t['nx'] is None or not allies: continue
        a = min(allies, key=lambda a: math.hypot(a['nx'] - t['nx'], a['nz'] - t['nz']))
        col = BLUE if a['is_smoker'] else VIOLET if a['how'] == 'inside' else GREEN if a['cls'] == 'destroyer' else MUTED
        p2.line([(t['nx'], t['nz']), (a['nx'], a['nz'])], stroke=col, width=1.3, opacity=0.8); p2.raw(cross(p2, t['nx'], t['nz']))
        p2.dot(a['nx'], a['nz'], r=3.5, fill=col, opacity=1, stroke=BG)
fig.add(p1); fig.add(p2)
fig.add(T(40, 612, f"Cruiser inside in {ck['cr_smokes']} of {ck['n']} ({top1(ck['cr_ship'], 3)}).", size=11.5, fill=INK, anchor='start'))
fig.add(T(40, 628, f"Another destroyer recorded in {ck['dd_n']} of {ck['n']}, forward of the smoke in {ck['dd_fwd']} (green line joins it to its smoke).", size=11.5, fill=INK, anchor='start'))
fig.add(T(550, 612, 'Dot = the ally nearest to each damaged enemy. Blue: the Harugumo. Violet: a ship inside the smoke.', size=11, anchor='start'))
fig.add(T(550, 628, 'Green: another destroyer. Grey: any other ship.', size=11, anchor='start'))
fig.save(os.path.join(OUT, 'fig', 'check-sg-harugumo'))

globals_for_report = dict(sig=sig, lead=lead, single=single, reverse=reverse, nsub=nsub, ncl=ncl, ncand=len(cands), pat=pat)
exec(open(os.path.join(OUT, 'spots_report.py'), encoding='utf-8').read())
