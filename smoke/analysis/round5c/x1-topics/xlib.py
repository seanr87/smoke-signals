# Round 5c, worker x1: shared helpers for a1.py .. a4.py. Run scripts as: python -I -X utf8 a1.py
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5clib import *
# set after the import: round3/common.py exports a variable named HERE that would send output to round3/
MYDIR = os.path.dirname(os.path.abspath(__file__))
R5B_A = os.path.join(os.path.dirname(R5C), 'round5b', 'part-a')
MIN_N = 8
SEED = 19
S, G = load5c()
DD = [s for s in S if s['cls'] == 'destroyer']
TOPS = lambda ss: [s for s in ss if s['grp'] == 'top']
RESTS = lambda ss: [s for s in ss if s['grp'] == 'rest']
SCOPES = [('All', lambda ss: ss), ('Top 6', TOPS), ('Rest', RESTS)]

class Stat:
    """A statistic with its own count of what it is measured on (min n 8 applies to that count)."""
    def __init__(self, key, label, fn, nfn, fmt='{:.1f}', sfmt='{:+.1f}'):
        self.key, self.label, self.fn, self.nfn, self.fmt, self.sfmt = key, label, fn, nfn, fmt, sfmt
    def n(self, ss): return self.nfn(ss)
    def v(self, ss): return self.fn(ss) if self.nfn(ss) >= MIN_N else None
_ok = lambda ss: [s for s in ss if s['died_ok']]
def _appl(key): return lambda ss: sum(1 for s in ss if s[key] is not None)
def _crate(num, den, ok):
    def f(ss):
        v = _ok(ss) if ok else ss; d = sum(s[den] for s in v)
        return 100.0 * sum(s[num] for s in v) / d if d else None
    return f
WE_C = Stat('we_took_c', 'we took, contested cap %', share_stat('we_took_c'), _appl('we_took_c'))
WE_N = Stat('we_took_n', 'we took, nearest cap %', share_stat('we_took_n'), _appl('we_took_n'))
EN_C = Stat('enemy_took_c', 'enemy took, contested cap %', share_stat('enemy_took_c'), _appl('enemy_took_c'))
EN_N = Stat('enemy_took_n', 'enemy took, nearest cap %', share_stat('enemy_took_n'), _appl('enemy_took_n'))
CONC = Stat('conc', 'concealed damage per smoke', lambda ss: sum(s['conc'] for s in ss) / len(ss) if ss else None, len, '{:,.0f}', '{:+,.0f}')
DIED = Stat('died100', 'died per 100', died100, lambda ss: len(_ok(ss)))
CAUGHT = Stat('caught100', 'caught per 100', caught100, len)
DIED_S = Stat('died_smoker100', 'smoker died per 100', died_smoker100, lambda ss: len(_ok(ss)))
CAUGHT_S = Stat('caught_smoker100', 'smoker caught per 100', caught_smoker100, len)
DIED_CR = Stat('died_cr100', 'cruisers died per 100 sheltering', _crate('died_cr', 'n_cr_cov', True), lambda ss: sum(s['n_cr_cov'] for s in _ok(ss)))
CAUGHT_CR = Stat('caught_cr100', 'cruisers caught per 100 sheltering', _crate('caught_cr', 'n_cr_in', False), lambda ss: sum(s['n_cr_in'] for s in ss))
DEATHS6 = [DIED, CAUGHT, DIED_S, CAUGHT_S, DIED_CR, CAUGHT_CR]

def r1(x, d=1): return None if x is None else round(x, d)
def val(ss, st, with_ci=False):
    v = st.v(ss); out = dict(value=r1(v, 2), n=st.n(ss))
    if with_ci:
        random.seed(SEED); lo, hi = boot_stat(ss, st.fn) if v is not None else (None, None)
        out.update(lo=r1(lo, 2), hi=r1(hi, 2))
    return out
def gap_tr(ss, st):
    """Top 6 minus Rest with the 95% interval (whole clans resampled inside each group)."""
    t, r = TOPS(ss), RESTS(ss); a, b = st.v(t), st.v(r)
    random.seed(SEED); lo, hi = boot_diff(ss, st.fn) if a is not None and b is not None else (None, None)
    return dict(top6=r1(a, 2), n_top6=st.n(t), rest=r1(b, 2), n_rest=st.n(r), diff=r1(a - b, 2) if lo is not None else None, lo=r1(lo, 2), hi=r1(hi, 2),
                clear=bool(lo is not None and lo * hi > 0))
def gap_ab(a, b, st):
    """stat(a) minus stat(b) for two kinds of smoke, 95% interval from r5clib.diff_ci (whole clans resampled over the union)."""
    va, vb = st.v(a), st.v(b)
    lo, hi = diff_ci(a, b, st.fn, seed=SEED) if va is not None and vb is not None else (None, None)
    return dict(a=r1(va, 2), n_a=st.n(a), b=r1(vb, 2), n_b=st.n(b), diff=r1(va - vb, 2) if lo is not None else None, lo=r1(lo, 2), hi=r1(hi, 2),
                clear=bool(lo is not None and lo * hi > 0))
def fv(x, f='{:.1f}'): return 'too few' if x is None else f.format(x)
def fn_(x, n, f='{:.1f}'): return f'{fv(x, f)} ({n})'
def fci(d, f='{:+.1f}'):
    if d.get('lo') is None: return '-'
    return f'{f.format(d["lo"])} to {f.format(d["hi"])}' + (' *' if d['lo'] * d['hi'] > 0 else '')
def fvci(d, f='{:.1f}'):
    return 'too few' if d.get('value') is None else f'{f.format(d["value"])} [{f.format(d["lo"])} to {f.format(d["hi"])}]'
def fdiff(d, f='{:+.1f}'):
    return 'too few' if d.get('diff') is None else f'{f.format(d["diff"])} ({fci(d, f)})'
def note(*ns):
    m = min(ns); return 'too few' if m < MIN_N else 'small n' if m < 15 else ''
def clear_word(d): return 'clear' if d.get('clear') else 'not clear'
def old(name):
    return json.load(open(os.path.join(R5B_A, name), encoding='utf-8'))
def chg_row(number, a, b, why, f='{:.1f}'):
    """One row of the 'Changed from round 5b' table; a = round 5b value, b = round 5c value."""
    fa = '-' if a is None else f.format(a) if isinstance(a, (int, float)) else str(a)
    fb = '-' if b is None else f.format(b) if isinstance(b, (int, float)) else str(b)
    same = fa == fb or (isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 0.06 and '.1f' in f)
    return [number, fa, fb, 'unchanged' if same else why]
def find(T, **kw): return next(x for x in T if all(x[k] == v for k, v in kw.items()))
def save(name, tables, md, check):
    json.dump(dict(tables=tables, md=md, check=check), open(os.path.join(MYDIR, name + '.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
    print(md)
DIED_NOTE = ('"Died" rates leave out the 9 smokes of the single-replay game laid by the team with no replay (their covered ships are known from the other side only); '
             '"caught" rates keep them.')
