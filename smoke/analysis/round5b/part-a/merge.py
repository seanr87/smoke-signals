# Builds part-a/topics.json from the four out-aN.json files, and reruns two headline numbers a second way straight from the raw records.
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
T = {}
for k in ('a1', 'a2', 'a3', 'a4'):
    T[k.upper()] = json.load(open(os.path.join(HERE_A, f'out-{k}.json'), encoding='utf-8'))
T['meta'] = dict(batch=BATCH_NAME, part='a', min_n=MIN_N, small_n='8 to 14', intervals='95%, whole clans resampled; clear = interval excludes zero',
                 groups=dict(top6=sorted(TOP), rest='every other clan'), destroyer_smokes=dict(top6=len(TOPS(DD)), rest=len(RESTS(DD))))
json.dump(T, open(os.path.join(HERE_A, 'topics.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
# second-way checks (raw csv / json fields only)
cc = [s for s in S if s['r']['smoker_class'] == 'destroyer' and s['r']['primary_purpose'] == 'cap_contest']
def chk(grp, cover):
    v = [s for s in cc if (s['team'] in TOP) == (grp == 'top') and s['cover3'] == cover and s['own'] != 'ours']
    return sum(1 for s in v if s['r']['cap_won']), len(v)
print('A1 cap_won / n (cap not ours): T6 radar', chk('top', 'radar cruiser inside'), 'T6 none', chk('top', 'no cruiser'), 'Rest radar', chk('rest', 'radar cruiser inside'), 'Rest none', chk('rest', 'no cruiser'))
dd = [s for s in S if s['r']['smoker_class'] == 'destroyer']
fl = [s for s in dd if any(x['kind'] == 'radar' for m in s['j']['smokees'] if m['how'] != 'none' for x in m.get('detected_by', []))]
print('A2 broad radar smokes', len(fl), 'deaths', sum(int(s['r']['smoke_deaths'] or 0) for s in fl), '| other smokes', len(dd) - len(fl), 'deaths', sum(int(s['r']['smoke_deaths'] or 0) for s in dd) - sum(int(s['r']['smoke_deaths'] or 0) for s in fl))
print('A2 totals: DD smokes', len(dd), 'deaths', sum(int(s['r']['smoke_deaths'] or 0) for s in dd), '| all smokes', len(S), sum(int(s['r']['smoke_deaths'] or 0) for s in S))
for sh in ('Somers', 'Gearing'):
    for g in (True, False):
        v = [s for s in dd if s['r']['ship'].replace(chr(160), ' ') == sh and (s['team'] in TOP) == g]
        print('A3', sh, 'Top 6' if g else 'Rest', len(v), sum(int(s['r']['smoke_deaths'] or 0) for s in v))
print('A4 counter rows', sum(1 for s in dd if s['r']['counter_smoke_of']))
print('topics.json written', os.path.getsize(os.path.join(HERE_A, 'topics.json')))
