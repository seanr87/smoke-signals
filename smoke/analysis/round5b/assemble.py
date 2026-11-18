# Builds the round 5 deliverables from the part folders: FINDINGS.md, spots.json, clan_styles.json, ships.json, CHECK.md.
# Run: python -I -X utf8 assemble.py   (after every part script has run). Reads only round5/part-*; writes only round5/.
import json, os, re, shutil
H = os.path.dirname(os.path.abspath(__file__))
BATCH = 'output/20261117-122135'
rd = lambda p: open(os.path.join(H, p), encoding='utf-8').read().strip() + '\n'
jl = lambda p: json.load(open(os.path.join(H, p), encoding='utf-8'))

# ---- FINDINGS.md
parts = [('Part A: topic cards (A1-A4)', 'part-a/FINDINGS-A.md'), ('Part B: ship tendencies (B1-B4)', 'part-b/FINDINGS-B.md'),
         ('Part C: caps and danger zones (C1-C3)', 'part-c1/FINDINGS-C1.md'), ('Part C: spots per map (C4)', 'part-c4/FINDINGS-C4.md'),
         ('Part C: map-specific questions (C5)', 'part-c5/FINDINGS-C5.md'), ('Part D: clan styles (D1-D3)', 'part-d/FINDINGS-D.md')]
out = [rd('FINDINGS-HEAD.md')]
for title, p in parts:
    t = rd(p)
    t = re.sub(r'^# .*\n', '', t, count=1) if t.startswith('# ') else t   # drop the part's own top title
    t = re.sub(r'^## ', '### ', t, flags=re.M) if p.endswith('C5.md') or p.endswith('C4.md') else t
    out.append(f'\n---\n\n## {title}\n\nSource: `{p}`.\n\n' + t)
open(os.path.join(H, 'FINDINGS.md'), 'w', encoding='utf-8').write(''.join(out))

# ---- spots.json
spots = []
for src, recs in (('part-c4', jl('part-c4/spots.json')), ('part-c5', jl('part-c5/spots.json')), ('part-c1', jl('part-c1/danger-zones.json'))):
    for i, r in enumerate(recs):
        r = dict(r); r['source'] = src
        if 'id' not in r:
            r['id'] = 'c1-danger-' + re.sub(r'[^a-z0-9]+', '-', (r['map'] + ' ' + r['name']).lower()).strip('-')
        if src == 'part-c5' and r['mode'] == 'top6':
            r['selection_note'] = ('Carried over from round 4 or from a map-specific question: the place was chosen because it showed a gap, '
                                   'and it is defined for one ship or habit. The blind search in part C4 (any place where a kind of smoke '
                                   'concentrates) labelled no place Top 6. Treat as a lead; see FINDINGS.md "Top 6 or Shared: how to read it".')
        if src == 'part-c1':
            r['display'] = 'show' if r['map'] == 'Hotspot' else 'reference only (n 8, in line with chance)'
        spots.append(r)
ids = [s['id'] for s in spots]; assert len(ids) == len(set(ids)), 'duplicate spot id'
json.dump(dict(batch=BATCH,
               frame='0-1 minimap frame, same as the atlas: origin top-left, u to the right (west to east), v down (north to south); '
                     'positions are team-normalized, own spawn at the bottom (bottom-left on Okinawa). Shapes: circle (u, v, r), '
                     'ellipse, polygon (points), cells (grid cell names plus centre u, v).',
               kinds=['top6_spot', 'shared_spot', 'selfish_spot', 'early_cruiser_spot', 'high_cell', 'danger_zone'],
               mode_rule='top6 = the share of Top 6 smokes (of that kind on that map) in the spot is clearly higher than the Rest share '
                         '(95% interval by resampling clans excludes zero); otherwise shared.',
               small_n='n 8 to 14 is small n; no spot has fewer than 8 smokes except where a record says so in its note.',
               spots=spots), open(os.path.join(H, 'spots.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- clan_styles.json, ships.json (as produced by parts D and B), plus the other tables for reference
shutil.copyfile(os.path.join(H, 'part-d/clan_styles.json'), os.path.join(H, 'clan_styles.json'))
ships = jl('part-b/ships.json'); ships = dict(batch=BATCH, note='Tables B1-B4 of FINDINGS.md. Intervals are 95%, clans resampled.', **ships)
json.dump(ships, open(os.path.join(H, 'ships.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- CHECK.md
chk = [rd('CHECK-HEAD.md')]
for title, p in (('Part A', 'part-a/CHECK-A.md'), ('Part B', 'part-b/CHECK-B.md'), ('Part C1-C3', 'part-c1/CHECK-C1.md'), ('Part C4', 'part-c4/CHECK-C4.md'),
                 ('Part C5', 'part-c5/CHECK-C5.md'), ('Part D', 'part-d/CHECK-D.md')):
    t = rd(p); t = re.sub(r'^# .*\n', '', t, count=1) if t.startswith('# ') else t
    chk.append(f'\n---\n\n## {title}\n\nScripts in `{os.path.dirname(p)}/`.\n\n' + t)
open(os.path.join(H, 'CHECK.md'), 'w', encoding='utf-8').write(''.join(chk))
print('spots', len(spots), {k: sum(1 for s in spots if s['kind'] == k) for k in sorted({s['kind'] for s in spots})},
      'top6', sum(s['mode'] == 'top6' for s in spots))
