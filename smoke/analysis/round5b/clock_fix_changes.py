# Lists what the 15-minute-clock fix changed in the outputs of the Round 5 scripts (rerun in round5b/part-*), against the
# Round 5 copies in ../round5. Writes rerun/clock-fix-changes.md. Run after run_round5_scripts.sh.
import os, re, difflib, json
H = os.path.dirname(os.path.abspath(__file__)); OLD = os.path.join(os.path.dirname(H), 'round5')
STDOUT = {'c5_sg.txt': 'part-c5/out-sg.txt', 'c5_hs.txt': 'part-c5/out-hs.txt', 'c5_lp.txt': 'part-c5/out-lp.txt', 'c5_lp_daring.txt': 'part-c5/out-lp-daring.txt',
          'c5_rest.txt': 'part-c5/out-rest.txt', 'c5_tables.txt': 'part-c5/out-tables.txt', 'd2_structure.txt': 'part-d/d2_output.txt', 'show.txt': 'part-b/show.txt'}
SKIP_NAMES = ('FINDINGS-', 'CHECK-', 'head.md')
def read(p):
    return open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').replace('20261117-230933', '20261117-122135')
pairs = []
for d in sorted(os.listdir(H)):
    if not (d.startswith('part-') or d == 'verify'): continue
    for f in sorted(os.listdir(os.path.join(H, d))):
        p, q = os.path.join(H, d, f), os.path.join(OLD, d, f)
        if os.path.isfile(p) and os.path.exists(q) and f.endswith(('.txt', '.md', '.json', '.csv')) and not f.startswith(SKIP_NAMES):
            pairs.append((f'{d}/{f}', p, q))
for f, o in STDOUT.items():
    p, q = os.path.join(H, 'rerun', 'stdout', f), os.path.join(OLD, *o.split('/'))
    if os.path.exists(p) and os.path.exists(q): pairs.append((o + ' (script output)', p, q))
num = re.compile(r'-?\d[\d,]*\.?\d*')
def same_numbers(a, b):
    """True when two lines hold the same numbers in a different order (ties listed in another order)."""
    return sorted(num.findall(a)) == sorted(num.findall(b)) and sorted(re.findall(r'[A-Za-zÀ-ſ][\wÀ-ſ.\- ]+', a)) == sorted(re.findall(r'[A-Za-zÀ-ſ][\wÀ-ſ.\- ]+', b))
out = ['# What the 15-minute-clock fix changed in the Round 5 script outputs', '',
       'Two games (kots19na_7971 game 1 on Hotspot, KSE against PFANS; kots19na_7976 game 1 on Loop, KSE against VRTUS) ran on a 15-minute clock.',
       'Rounds 3 to 5 read elapsed time as 20:00 minus the HUD clock, so their 17 smokes (11 by destroyers) were placed 300 seconds late.',
       'Each block lists the lines that differ: Round 5 first, Round 5b second. Lines that only list equal counts in another order are counted, not shown.', '']
summary = []
for name, p, q in pairs:
    a, b = read(q).split('\n'), read(p).split('\n')
    if a == b: summary.append((name, 0, 0)); continue
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    changes = []; ties = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': continue
        olds, news = a[i1:i2], b[j1:j2]
        for k in range(max(len(olds), len(news))):
            x = olds[k] if k < len(olds) else ''; y = news[k] if k < len(news) else ''
            if x and y and same_numbers(x, y): ties += 1
            else: changes.append((x, y))
    summary.append((name, len(changes), ties))
    if not changes: continue
    out.append(f'## {name}: {len(changes)} lines changed' + (f' ({ties} more differ only in the order of ties)' if ties else ''))
    out.append('')
    if name.endswith('.json'):
        out.append('(JSON file: the same values appear in the text outputs listed here; line count only.)'); out.append(''); continue
    for x, y in changes[:60]:
        out.append('```'); out.append('round 5 : ' + x.strip()[:300]); out.append('round 5b: ' + y.strip()[:300]); out.append('```')
    if len(changes) > 60: out.append(f'... and {len(changes) - 60} more lines.')
    out.append('')
out[5:5] = ['| output | lines changed | lines differing only in tie order |', '|---|---|---|'] + [f'| {n} | {c} | {t} |' for n, c, t in summary] + ['']
open(os.path.join(H, 'rerun', 'clock-fix-changes.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(f'{n}: {c} changed, {t} ties' for n, c, t in summary if c or t))
