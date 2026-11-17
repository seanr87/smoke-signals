# Word limits and wording check for ATLAS-CONTENT.md. Prints the counts; exits 1 if a limit is broken or causal wording is found.
# Run from the repo root: python -I -X utf8 smoke/analysis/atlas/scripts/check_copy.py
# Counting rule: a word is a whitespace-separated token holding at least one letter or digit, after markdown marks are removed.
# A markdown link counts its label only (the URL is not a word). HTML comments are not counted.
import sys, os, re
sys.dont_write_bytecode = True
ATLAS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
text = open(os.path.join(ATLAS, 'ATLAS-CONTENT.md'), encoding='utf-8').read()
text = re.sub(r'<!--.*?-->', '', text, flags=re.S)

def words(t):
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)      # links: keep the label
    t = re.sub(r'[*_`#|>]', ' ', t)
    return [w for w in t.split() if re.search(r'[A-Za-z0-9]', w)]

sections = re.split(r'(?m)^## ', text)[1:]
bad = 0
def report(name, n, limit):
    global bad
    flag = '' if limit is None or n <= limit else '   <-- OVER'
    if flag: bad += 1
    print(f'{name:<58} {n:>4}' + (f' / {limit}' if limit else '') + flag)

for sec in sections:
    title, _, body = sec.partition('\n')
    title = title.strip()
    if title.startswith('Page 1'):
        rules = re.findall(r'(?m)^\d+\.\s+(.*)$', body)
        print(f'{title}: {len(rules)} rules (limit 5 to 8)'); bad += not (5 <= len(rules) <= 8)
        for i, r in enumerate(rules, 1): report(f'  rule {i}', len(words(r)), 25)
        report('  whole page (no limit)', len(words(body)), None)
    elif re.match(r'Page [2-8]\b', title):
        map_title = title.split(':', 1)[1] if ':' in title else title
        report(title + ' (whole page, title included)', len(words(map_title)) + len(words(body)), 220)
        for line in re.findall(r'(?m)^- \*\*(?:Signature|Lead)[^\n]*$', body):
            report('  ' + ' '.join(words(line)[:4]) + ' ...', len(words(line[2:])), 30)
        links = re.findall(r'\]\((https?://[^)]+)\)', body)
        print(f'  example links: {len(links)}'); bad += len(links) < 3
    elif title.startswith('Page 9'):
        report(title, len(words(body)), 250)
    elif title.startswith('Sidebar'):
        report(title, len(words(body)), 120)
    else:
        report(title + ' (no limit)', len(words(body)), None)

print()
causal = r"\b(win|wins|winning|winner|causes|caused|cause of|leads to|lead to|best way|should|must|guarantee\w*|makes? (?:a|the) team)\b"
hits = []
for i, line in enumerate(text.splitlines(), 1):
    for m in re.finditer(causal, line, flags=re.I):
        # allowed: the fixed phrase "association, not cause" (does not match the pattern) and nothing else
        hits.append((i, m.group(0), line.strip()[:140]))
print('causal wording hits:', len(hits))
for h in hits: print('  line', h[0], repr(h[1]), '|', h[2])
bad += len(hits)
print('RESULT:', 'ok' if not bad else f'{bad} problem(s)')
sys.exit(1 if bad else 0)
