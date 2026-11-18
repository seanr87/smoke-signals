# Builds the round 5c deliverables: FINDINGS.md, clan_styles.json, ships.json, CHECK.md (spots.json comes from spots_5c.py).
# Run after the x1, x2, x3 scripts, spots_5c.py and the verify scripts:  python -I -X utf8 assemble_5c.py
import json, os, re, shutil
H = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(H, p), encoding='utf-8').read().strip() + '\n'
jl = lambda p: json.load(open(os.path.join(H, p), encoding='utf-8'))
def body(p):
    t = rd(p)
    t = re.sub(r'^# .*\n', '', t, count=1) if t.startswith('# ') else t
    return re.sub(r'^## ', '### ', t, flags=re.M)

def changed_blocks(p):
    """(item heading, text of its 'Changed from round 5b' block) for every item of a findings file."""
    t = rd(p); out = []
    heads = list(re.finditer(r'^#{2,3} (.+)$', t, flags=re.M))
    for i, m in enumerate(heads):
        seg = t[m.end():heads[i + 1].start()] if i + 1 < len(heads) else t[m.end():]
        c = re.search(r'^\*\*Changed from round 5b[^*]*\*\*:?(.*)', seg, flags=re.M | re.S)
        if c:
            txt = c.group(1).strip()
            cut = re.search(r'^\*\*[A-Z][^*]*:\*\*', txt, flags=re.M)   # stop at the next bold block label, if any
            out.append((m.group(1).strip(), (txt[:cut.start()] if cut else txt).strip()))
    return out

parts = [('Items 1 to 4: topic cards (A1 to A4)', 'x1-topics/FINDINGS-X1.md'),
         ('Items 5 to 7: getaway smokes (B2), long smokes (B3), map rows that quote a cap result (C4, C5)', 'x2-ships-maps/FINDINGS-X2.md'),
         ('Item 8: clan styles (D1 to D3)', 'x3-clans/FINDINGS-X3.md')]
sec = ['## 3. Every number that changed from Round 5b\n',
       'For an item Round 5b did not redo, "Round 5b" means the Round 5 number after the clock fix. Each block is that item\'s own old-to-new list. '
       'Package changes (spots.json, the four reworded lines) are in section 2 and in README.md.\n']
for title, p in parts:
    for item, text in changed_blocks(p):
        sec.append(f'**{item}** (`{p}`)\n\n{text}\n')
out = [rd('FINDINGS-HEAD.md'), '\n', '\n'.join(sec), '\n## 4. The items redone in Round 5c\n']
for title, p in parts:
    out.append(f'\n---\n\n## {title}\n\nSource: `{p}`.\n\n' + body(p))
out.append('\n---\n\n' + rd('FINDINGS-TAIL.md'))
open(os.path.join(H, 'FINDINGS.md'), 'w', encoding='utf-8').write(''.join(out))

shutil.copyfile(os.path.join(H, 'x3-clans', 'clan_styles.json'), os.path.join(H, 'clan_styles.json'))
b = jl('../round5b/ships.json'); x2 = jl('x2-ships-maps/ships-maps.json')
ships = dict(batch='output/20261117-230933',
             note='Round 5b ships.json (B1 to B4 and B3_per_shot) plus the round 5c tables: B2_5c and B3_5c carry both death metrics '
                  '(died = track deaths, caught = batch list) and the smoker\'s undetected share from the track; they supersede the death and '
                  'undetected columns of B2 and B3. map_cap_rows_5c holds item 7 (cap results from the cap timeline).',
             **{k: v for k, v in b.items() if k not in ('batch', 'note')})
ships['B2_5c'] = x2['B2']; ships['B3_5c'] = x2['B3']
ships['map_cap_rows_5c'] = {k: x2[k] for k in ('C7a', 'C7b', 'C7c', 'C7d')}
json.dump(ships, open(os.path.join(H, 'ships.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

chk = [rd('CHECK-HEAD.md')]
for title, p in (('Items 1 to 4', 'x1-topics/CHECK-X1.md'), ('Items 5 to 7', 'x2-ships-maps/CHECK-X2.md'), ('Item 8', 'x3-clans/CHECK-X3.md')):
    chk.append(f'\n---\n\n## {title}\n\nScripts in `{os.path.dirname(p)}/`.\n\n' + body(p))
open(os.path.join(H, 'CHECK.md'), 'w', encoding='utf-8').write(''.join(chk))
t = ''.join(out)
print('FINDINGS lines', t.count('\n'), '| changed blocks', sum(len(changed_blocks(p)) for _, p in parts), '| non-ASCII dashes', len(re.findall('[–—]', t)))
