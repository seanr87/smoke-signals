# Compares every file the rerun round 5 scripts wrote in round5b/part-* and round5b/verify with the round 5 copy.
# Figures are skipped (PNG rendering is not byte-stable). Prints a Markdown table.
import os, sys, json, re
H = os.path.dirname(os.path.abspath(__file__)); OLD = os.path.join(os.path.dirname(H), 'round5')
skip = ('.png', '.svg', '.pyc', '.py')
same, diff, new = [], [], []
def norm(t):
    t = t.replace('\r\n', '\n')
    t = t.replace('20261117-230933', '20261117-122135')
    return t
for d in sorted(os.listdir(H)):
    if not (d.startswith('part-') or d == 'verify'): continue
    for f in sorted(os.listdir(os.path.join(H, d))):
        p = os.path.join(H, d, f)
        if not os.path.isfile(p) or f.endswith(skip): continue
        q = os.path.join(OLD, d, f)
        if not os.path.exists(q): new.append(f'{d}/{f}'); continue
        a = norm(open(p, encoding='utf-8', errors='replace').read()); b = norm(open(q, encoding='utf-8', errors='replace').read())
        if a == b: same.append(f'{d}/{f}')
        else:
            la, lb = a.split('\n'), b.split('\n')
            n = sum(1 for x, y in zip(la, lb) if x != y) + abs(len(la) - len(lb))
            first = next(((x, y) for x, y in zip(la, lb) if x != y), ('', ''))
            diff.append((f'{d}/{f}', n, len(la), first))
print(f'identical: {len(same)} files; different: {len(diff)}; only in round5b: {len(new)}')
for f, n, tot, (x, y) in diff:
    print(f'- DIFF {f}: {n} of {tot} lines\n    new: {x[:160]}\n    old: {y[:160]}')
print('only in round5b:', new)
missing = [f'{d}/{f}' for d in sorted(os.listdir(OLD)) if d.startswith('part-') or d == 'verify' for f in sorted(os.listdir(os.path.join(OLD, d)))
           if os.path.isfile(os.path.join(OLD, d, f)) and not f.endswith(skip) and not os.path.exists(os.path.join(H, d, f))]
print('in round 5 but not regenerated:', missing)
