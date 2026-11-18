# Builds the round 5b deliverables: FINDINGS.md, spots.json, clan_styles.json, ships.json, CHECK.md.
# Run after run_round5_scripts.sh, the new-n* scripts and clock_fix_changes.py:  python -I -X utf8 assemble.py
import json, os, re, shutil
H = os.path.dirname(os.path.abspath(__file__))
BATCH = 'output/' + json.load(open(os.path.join(H, 'batch.json'), encoding='utf-8'))['batch']
rd = lambda p: open(os.path.join(H, p), encoding='utf-8').read().strip() + '\n'
jl = lambda p: json.load(open(os.path.join(H, p), encoding='utf-8'))
def body(p, demote=False):
    t = rd(p)
    t = re.sub(r'^# .*\n', '', t, count=1) if t.startswith('# ') else t
    return re.sub(r'^## ', '### ', t, flags=re.M) if demote else t

# ---- section 3: every number that changed
def changed_blocks(p):
    """(item heading, text of its 'Changed from ...' block) for every item of a new findings file."""
    t = rd(p); out = []
    for m in re.finditer(r'^### (.+)$', t, flags=re.M):
        seg = t[m.end():]; nxt = re.search(r'^#{2,3} ', seg, flags=re.M)
        seg = seg[:nxt.start()] if nxt else seg
        c = re.search(r'^\*\*Changed from [^*]*\*\*:?(.*)', seg, flags=re.M | re.S)
        if c: out.append((m.group(1).strip(), c.group(1).strip()))
    return out
sec3 = ['## 3. Every number that changed from Round 5\n',
        'Three sources of change. (a) New data: items redone from the timelines; each block below is the full old-to-new list '
        'from that item. (b) The 15-minute-clock fix, which touches items that were not redone. (c) Nothing else: with the '
        'Round 5 definitions unchanged, the Round 5 scripts give the Round 5 outputs again on the new batch '
        '(`rerun/same-definitions.txt`).\n',
        '### 3a. Changed because of the new data\n']
for p in ('new-n1/FINDINGS-N1.md', 'new-n2/FINDINGS-N2.md', 'new-n3/FINDINGS-N3.md', 'new-n4/FINDINGS-N4.md'):
    for title, text in changed_blocks(p):
        sec3.append(f'**{title}** (`{p}`)\n\n{text}\n')
sec3.append('### 3b. Changed because of the 15-minute-clock fix\n')
sec3.append(rd('CLOCKFIX-SUMMARY.md'))

# ---- section 4: items in round 5 order
def supersede(text, marks):
    """Insert a 'superseded' banner under the named headings of the Round 5 text."""
    for head, note in marks:
        assert text.count(head) == 1, head
        text = text.replace(head, head + f'\n\n> **Superseded in Round 5b.** {note} The Round 5 text is kept below for reference.\n')
    return text
A = supersede(body('part-a/FINDINGS-A.md'), [('### A2. Smoke deaths drill-down', 'Deaths, leaving the smoke and radar deaths are redone from ship tracks and the radar log: see "A2 (Round 5b)" above this part\'s Round 5 text. Where, when and score-state patterns below still hold in shape, but the rates use the batch death list, which undercounts.')])
B = supersede(body('part-b/FINDINGS-B.md'), [('### B3. Long smokes (Somers, Gearing, Harugumo, Delny)', 'The "who spots for the Harugumo" and second-destroyer numbers are redone per shot: see "B3 (Round 5b)". The deployment tables below are unchanged.')])
C1 = supersede(body('part-c1/FINDINGS-C1.md'), [('### C1. Cap defence', 'Redone from the cap timeline: see "C1 (Round 5b)". The definition of `cap_defended` and the ribbon source check below still stand.'),
                                                ('### C2. Cap holder at 8:00 and winning', 'Redone at exactly 8:00 for 166 games: see "C2 (Round 5b)".'),
                                                ('### C3. Danger zones', 'Redone with real health and death positions: see "C3 (Round 5b)". No zone is kept.')])
C5 = supersede(body('part-c5/FINDINGS-C5.md', demote=True), [('### C5-LP-4. Test: did Daring smokes follow a friendly radar lighting an enemy destroyer', 'Redone with the full radar log: see "C5-LP-4 (Round 5b)".')])
n1, n2, n3, n4 = (body(f'new-n{i}/FINDINGS-N{i}.md', demote=True) for i in (1, 2, 3, 4))
parts = [
 ('Page 1 carry-overs, re-tested (Round 5b)', 'new-n4/FINDINGS-N4.md', n4),
 ('Part A (Round 5b): deaths with real health, leaving the smoke, radar deaths (A2); danger zones (C3)', 'new-n2/FINDINGS-N2.md', n2),
 ('Part A: topic cards (A1-A4), Round 5 text', 'part-a/FINDINGS-A.md', A),
 ('Part B (Round 5b): Harugumo per shot (B3); Loop Daring after radar (C5-LP-4)', 'new-n3/FINDINGS-N3.md', n3),
 ('Part B: ship tendencies (B1-B4), Round 5 text', 'part-b/FINDINGS-B.md', B),
 ('Part C (Round 5b): cap defence from the timeline (C1), cap holder at exactly 8:00 (C2)', 'new-n1/FINDINGS-N1.md', n1),
 ('Part C: caps and danger zones (C1-C3), Round 5 text', 'part-c1/FINDINGS-C1.md', C1),
 ('Part C: spots per map (C4), rerun with the clock fix', 'part-c4/FINDINGS-C4.md', body('part-c4/FINDINGS-C4.md', demote=True)),
 ('Part C: map-specific questions (C5), Round 5 text', 'part-c5/FINDINGS-C5.md', C5),
 ('Part D: clan styles (D1-D3), Round 5 text', 'part-d/FINDINGS-D.md', body('part-d/FINDINGS-D.md')),
]
out = [rd('FINDINGS-HEAD.md'), '\n', '\n'.join(sec3), '\n## 4. The items\n']
for title, p, t in parts:
    out.append(f'\n---\n\n## {title}\n\nSource: `{p}`.\n\n' + t)
open(os.path.join(H, 'FINDINGS.md'), 'w', encoding='utf-8').write(''.join(out))

# ---- spots.json: round 5 spots rerun, danger zones replaced by the round 5b ones
spots = []
for src, recs in (('part-c4', jl('part-c4/spots.json')), ('part-c5', jl('part-c5/spots.json')), ('new-n2', jl('new-n2/danger-zones.json'))):
    for r in recs:
        r = dict(r); r['source'] = src
        if src == 'part-c5' and r['mode'] == 'top6':
            r['selection_note'] = ('Carried over from round 4 or from a map-specific question: the place was chosen because it showed a gap, and it '
                                   'is defined for one ship or habit. The blind search in part C4 labelled no place Top 6. Treat as a lead.')
        if src == 'new-n2':
            r['display'] = 'reference only: no danger zone is kept in round 5b (flags are in line with chance, n 8 to 14)'
        spots.append(r)
ids = [s['id'] for s in spots]; assert len(ids) == len(set(ids)), 'duplicate spot id'
json.dump(dict(batch=BATCH,
               frame='0-1 minimap frame, same as the atlas: origin top-left, u to the right, v down; positions are team-normalized, own spawn at the '
                     'bottom (bottom-left on Okinawa). Shapes: circle (u, v, r), ellipse, polygon (points), cells (grid cell names plus centre u, v).',
               kinds=['top6_spot', 'shared_spot', 'selfish_spot', 'early_cruiser_spot', 'high_cell', 'danger_zone'],
               mode_rule='top6 = the share of Top 6 smokes (of that kind on that map) in the spot is clearly higher than the Rest share; otherwise shared.',
               changed_from_round5='The four round 5 danger zones from part C1 are removed; the five round 5b candidates are listed as reference only. '
                                   'Other spots are the round 5 spots rerun with the 15-minute-clock fix.',
               spots=spots), open(os.path.join(H, 'spots.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- clan_styles.json, ships.json
shutil.copyfile(os.path.join(H, 'part-d', 'clan_styles.json'), os.path.join(H, 'clan_styles.json'))
ships = dict(batch=BATCH, note='Tables B1-B4 (round 5 scripts rerun) plus B3_per_shot: the Harugumo spotting redo from new-n3. '
                               'B3.harugumo.nearest_ally_to_targets and the second-destroyer rows are superseded by B3_per_shot.', **jl('part-b/ships.json'))
ships['B3_per_shot'] = jl('new-n3/b3.json')
json.dump(ships, open(os.path.join(H, 'ships.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- CHECK.md
chk = [rd('CHECK-HEAD.md')]
for title, p in (('New: caps (C1, C2)', 'new-n1/CHECK-N1.md'), ('New: deaths and danger zones (A2, C3)', 'new-n2/CHECK-N2.md'), ('New: Harugumo and Loop (B3, C5)', 'new-n3/CHECK-N3.md'),
                 ('New: page 1 carry-overs', 'new-n4/CHECK-N4.md'), ('Part A (round 5)', 'part-a/CHECK-A.md'), ('Part B (round 5)', 'part-b/CHECK-B.md'),
                 ('Part C1-C3 (round 5)', 'part-c1/CHECK-C1.md'), ('Part C4 (round 5)', 'part-c4/CHECK-C4.md'), ('Part C5 (round 5)', 'part-c5/CHECK-C5.md'), ('Part D (round 5)', 'part-d/CHECK-D.md')):
    chk.append(f'\n---\n\n## {title}\n\nScripts in `{os.path.dirname(p)}/`.\n\n' + body(p))
open(os.path.join(H, 'CHECK.md'), 'w', encoding='utf-8').write(''.join(chk))
print('spots', len(spots), {k: sum(1 for s in spots if s['kind'] == k) for k in sorted({s['kind'] for s in spots})})
