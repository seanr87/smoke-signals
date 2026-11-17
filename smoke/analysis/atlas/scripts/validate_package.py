# Package checks: spots.json, caps.json, maps/, figures/ and the links in ATLAS-CONTENT.md.
# Run from the repo root: python -I -X utf8 smoke/analysis/atlas/scripts/validate_package.py
import sys, os, re, json, collections
sys.dont_write_bytecode = True
ATLAS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://seanr87.github.io/smoke-signals/smoke/'
KINDS = {'signature', 'lead', 'paying_high', 'paying_low', 'radar', 'deaths', 'early_smoke', 'cast_cruiser', 'cast_second_dd'}
FIELDS = ['id', 'map', 'kind', 'label', 'subject', 'parent', 'centre_uv', 'shape', 'numbers', 'small_n', 'links', 'notes']
bad = []
d = json.load(open(os.path.join(ATLAS, 'spots.json'), encoding='utf-8'))
assert d['batch'] and d['frame']
ids = {s['id'] for s in d['spots']}
maps = {m['title']: m for m in json.load(open(os.path.join(ATLAS, 'maps', 'maps.json'), encoding='utf-8'))}
for s in d['spots']:
    for f in FIELDS:
        if f not in s: bad.append((s.get('id'), 'missing ' + f))
    if s['kind'] not in KINDS: bad.append((s['id'], 'kind'))
    if s['map'] not in maps: bad.append((s['id'], 'map'))
    u, v = s['centre_uv']
    if not (0 <= u <= 1 and 0 <= v <= 1): bad.append((s['id'], 'centre_uv out of range'))
    sh = s['shape']
    if sh['type'] == 'ellipse':
        if not (sh['ru'] > 0 and sh['rv'] > 0 and 'angle_deg' in sh): bad.append((s['id'], 'ellipse'))
    elif sh['type'] == 'polygon':
        if len(sh['points_uv']) < 3 or any(not (0 <= a <= 1 and 0 <= b <= 1) for a, b in sh['points_uv']): bad.append((s['id'], 'polygon'))
    else: bad.append((s['id'], 'shape type'))
    for l in s['links']:
        if not l.startswith(SITE): bad.append((s['id'], 'link ' + l))
    if s['parent'] is not None and s['parent'] not in ids: bad.append((s['id'], 'parent'))
    if (s['kind'].startswith('cast_')) != (s['parent'] is not None): bad.append((s['id'], 'parent/kind mismatch'))
    if any(isinstance(x, (dict, list)) for x in s['numbers'].values()): bad.append((s['id'], 'numbers not flat'))
    if s['kind'] not in ('cast_cruiser', 'cast_second_dd') and s['numbers'].get('n', 0) < 8: bad.append((s['id'], 'n below 8'))
print('spots.json records:', len(d['spots']), dict(collections.Counter(s['kind'] for s in d['spots'])))
print('records per map:', dict(collections.Counter(s['map'] for s in d['spots'])))
print('cast records with a count below 8 (formation drawing only):', sorted(s['id'] for s in d['spots'] if s['kind'].startswith('cast_') and s['numbers']['n'] < 8))
c = json.load(open(os.path.join(ATLAS, 'caps.json'), encoding='utf-8'))
for m, v in c['maps'].items():
    if m not in maps: bad.append((m, 'caps map'))
    for cap in v['caps']:
        u, w = cap['centre_uv']
        if not (0 <= u <= 1 and 0 <= w <= 1 and 0 < cap['radius_u'] < 0.5): bad.append((m, cap['letter'], 'cap geometry'))
print('caps.json maps:', len(c['maps']), 'caps:', sum(len(v['caps']) for v in c['maps'].values()))
for m in maps.values():
    for f in (m['file'], m['webp']):
        if not os.path.exists(os.path.join(ATLAS, 'maps', f)): bad.append((f, 'missing map file'))
    b = open(os.path.join(ATLAS, 'maps', m['file']), 'rb').read(24)
    w, h = int.from_bytes(b[16:20], 'big'), int.from_bytes(b[20:24], 'big')
    if (w, h) != (m['width_px'], m['height_px']): bad.append((m['file'], 'size', w, h))
print('maps:', len(maps), 'png + webp present, sizes match maps.json')
figs = [f for f in os.listdir(os.path.join(ATLAS, 'figures'))]
for stem in ['map-sg', 'map-hs', 'map-loop', 'map-mr', 'map-lof', 'map-sof', 'map-oki', 'clan-styles']:
    for ext in ('.png', '.svg'):
        if stem + ext not in figs: bad.append((stem + ext, 'missing figure'))
    svg = open(os.path.join(ATLAS, 'figures', stem + '.svg'), encoding='utf-8').read()
    for href in set(re.findall(r'href="([^"]+)"', svg)):
        if not href.startswith('../maps/') or not os.path.exists(os.path.join(ATLAS, 'figures', href)): bad.append((stem, 'href ' + href))
print('figures:', len(figs), 'files; SVG images point at ../maps/')
txt = open(os.path.join(ATLAS, 'ATLAS-CONTENT.md'), encoding='utf-8').read()
links = re.findall(r'\]\(([^)]+)\)', txt)
all_links = {l for s in json.load(open(os.path.join(ATLAS, 'spots.json'), encoding='utf-8'))['spots'] for l in s['links']}
for l in links:
    if not l.startswith(SITE + 'smokes/'): bad.append(('content link', l))
print('ATLAS-CONTENT.md links:', len(links), 'all start with the site URL:', all(l.startswith(SITE) for l in links))
for sid in re.findall(r'<!-- ([a-z0-9-]+)[ ;]', txt):
    if sid not in ids and not sid.startswith('Smoke'): bad.append(('content spot id', sid))
print('RESULT:', 'ok' if not bad else bad)
sys.exit(1 if bad else 0)
