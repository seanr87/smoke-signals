# Part A helpers (round 5). Run scripts as: python -I -X utf8 a1.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from r5lib import *
import json
HERE_A = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(R5, 'figures')
MIN_N = 8
S, G = load5()
DD = [s for s in S if s['cls'] == 'destroyer']
TOPS = lambda ss: [s for s in ss if s['grp'] == 'top']
RESTS = lambda ss: [s for s in ss if s['grp'] == 'rest']
ALWAYS = lambda s: True

def share(pred, among=ALWAYS):
    """Percent of rows (passing `among`) for which pred is true; None under MIN_N rows."""
    def f(ss):
        v = [s for s in ss if among(s)]
        return 100 * sum(1 for s in v if pred(s)) / len(v) if len(v) >= MIN_N else None
    f.among = among; return f
def per100(key, among=ALWAYS):
    def f(ss):
        v = [s for s in ss if among(s)]
        return 100 * sum(s[key] for s in v) / len(v) if len(v) >= MIN_N else None
    f.among = among; return f
def avg(key, among=ALWAYS):
    def f(ss):
        v = [s for s in ss if among(s)]
        return sum(s[key] for s in v) / len(v) if len(v) >= MIN_N else None
    f.among = among; return f
def ratio100(num, den):
    """100 * sum(num) / sum(den), e.g. cruiser deaths per 100 sheltering cruisers; None when the den total is under MIN_N."""
    def f(ss):
        d = sum(s[den] for s in ss)
        return 100 * sum(s[num] for s in ss) / d if d >= MIN_N else None
    f.among = ALWAYS; f.den = den; return f
def nn(ss, stat):
    if hasattr(stat, 'den'): return sum(s[stat.den] for s in ss)
    return sum(1 for s in ss if getattr(stat, 'among', ALWAYS)(s))
def r1(x, d=1): return None if x is None else round(x, d)
def gap(ss, stat, d=1):
    """Top 6 vs Rest for one statistic, with the 95% interval of the difference (whole clans resampled)."""
    t, r = TOPS(ss), RESTS(ss); a, b = stat(t), stat(r)
    lo, hi = boot_diff(ss, stat) if a is not None and b is not None else (None, None)
    return dict(top6=r1(a, d), n_top6=nn(t, stat), rest=r1(b, d), n_rest=nn(r, stat), diff=r1(a - b, d) if lo is not None else None,
                lo=r1(lo, d), hi=r1(hi, d), clear=bool(lo is not None and lo * hi > 0))
def one(ss, stat, d=1):
    v = stat(ss); lo, hi = boot_stat(ss, stat) if v is not None else (None, None)
    return dict(value=r1(v, d), n=nn(ss, stat), lo=r1(lo, d), hi=r1(hi, d))
def diff2(a, b, stat, d=1):
    """stat(a) - stat(b) for two disjoint sets of smokes, interval by resampling whole clans over the union."""
    ia = {id(s) for s in a}; u = list(a) + list(b)
    def f(ss):
        x, y = stat([s for s in ss if id(s) in ia]), stat([s for s in ss if id(s) not in ia])
        return None if x is None or y is None else x - y
    v = f(u); lo, hi = boot_stat(u, f) if v is not None else (None, None)
    return dict(a=r1(stat(a), d), n_a=nn(a, stat), b=r1(stat(b), d), n_b=nn(b, stat), diff=r1(v, d), lo=r1(lo, d), hi=r1(hi, d), clear=bool(lo is not None and lo * hi > 0))
def sm(n): return 'too few' if n < MIN_N else 'small n' if n < 15 else ''
def fv(x, f='{:.1f}'): return 'too few' if x is None else f.format(x)
def fci(d, f='{:+.1f}'):
    if d.get('lo') is None: return '-'
    return f'{f.format(d["lo"])} to {f.format(d["hi"])}' + (' *' if d['lo'] * d['hi'] > 0 else '')
def out(name, obj, text):
    json.dump(obj, open(os.path.join(HERE_A, name + '.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
    open(os.path.join(HERE_A, name + '.txt'), 'w', encoding='utf-8').write(text)
    print(text)
