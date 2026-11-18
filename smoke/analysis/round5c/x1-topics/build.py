# Runs a1..a4 and writes FINDINGS-X1.md, topics.json and CHECK-X1.md from their outputs. Run: python -I -X utf8 build.py
import sys, os, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = ['a1', 'a2', 'a3', 'a4']
if '--no-run' not in sys.argv:
    for it in ITEMS:
        subprocess.run([sys.executable, '-I', '-X', 'utf8', os.path.join(HERE, it + '.py')], check=True, stdout=subprocess.DEVNULL)
out = {it: json.load(open(os.path.join(HERE, f'out-{it}.json'), encoding='utf-8')) for it in ITEMS}
head = ['# Round 5c findings, worker x1 (items A1 to A4)', '',
        'Batch `output/20261117-230933`. Written by `x1-topics/build.py` from `a1.py` to `a4.py`. Two death metrics side by side everywhere: '
        '"died" = a covered ship died between activation and exactly 20 s after the smoke dispersed (each ship counted once); "caught" = the batch list of smoke deaths (round 5\'s deaths). '
        'Cap results come from the cap timeline with 60 s after dispersal. Intervals are 95%, resampling whole clans; * = the interval excludes zero ("clear"). '
        'Under 8 = too few (no rate); 8 to 14 = small n. Everything is association, not cause.', '']
open(os.path.join(HERE, 'FINDINGS-X1.md'), 'w', encoding='utf-8').write('\n'.join(head) + '\n' + '\n'.join(out[it]['md'] + '\n' for it in ITEMS))
topics = {it.upper(): out[it]['tables'] for it in ITEMS}
topics['A2'].pop('radar_death_rows', None)   # per-death rows stay in out-a2.json
json.dump(topics, open(os.path.join(HERE, 'topics.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
chk = ['# CHECK-X1: where each headline number comes from', '', 'All scripts are in `round5c/x1-topics/`; shared helpers in `xlib.py`; definitions in `round5c/r5clib.py`. Tables are also in `topics.json` (key = item) and `out-aN.json`.', '',
       '| headline number | script | variable | value |', '|---|---|---|---|']
for it in ITEMS:
    for r in out[it]['check']: chk.append('| ' + ' | '.join(str(c) for c in r) + ' |')
open(os.path.join(HERE, 'CHECK-X1.md'), 'w', encoding='utf-8').write('\n'.join(chk) + '\n')
print('written', {f: os.path.getsize(os.path.join(HERE, f)) for f in ('FINDINGS-X1.md', 'topics.json', 'CHECK-X1.md')})
