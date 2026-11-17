# Helpers for module 5 that common.py lacks.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
HERE5 = os.path.dirname(os.path.abspath(__file__))
S, G = load()
DD = [s for s in S if s['cls'] == 'destroyer']
TG = team_games(G)
WL = win_loss(G)
NG = {t: sum(WL[t]) for t in WL}

def grp_of(t): return 'top' if t in TOP else 'rest'
def conc_per(ss): return mean(s['conc'] for s in ss)
def d100(ss): return 100 * sum(s['deaths'] for s in ss) / len(ss) if ss else None
def lohi(v):
    v = sorted(x for x in v if x is not None)
    if not v: return (None, None)
    return v[int(.025 * len(v))], v[max(0, int(.975 * len(v)) - 1)]

def boot_clans(fn, reps=1000, groups=True):
    """fn(list of clan names, with repeats) -> number. If groups, returns interval of fn(top sample) - fn(rest sample); else interval of fn(all)."""
    clans = sorted(NG); tops = [c for c in clans if c in TOP]; rest = [c for c in clans if c not in TOP]
    out = []
    for _ in range(reps):
        if groups:
            a, b = fn(random.choices(tops, k=len(tops))), fn(random.choices(rest, k=len(rest)))
            out.append(None if a is None or b is None else a - b)
        else:
            out.append(fn(random.choices(clans, k=len(clans))))
    return lohi(out)

def f1(x, f='{:.1f}'): return '-' if x is None else f.format(x)
def k(x): return '-' if x is None else f'{x/1000:.1f}k'
def band(e):
    return 'inside cap' if e < 0 else '0 to 1 km' if e < 1000 else '1 to 3 km' if e < 3000 else '3 to 5 km' if e < 5000 else '5 km +'
BANDS = ['inside cap', '0 to 1 km', '1 to 3 km', '3 to 5 km', '5 km +']

def vbars(fig, x, y, w, h, cats, series, fmt='{:.1f}', ymax=None, ylabel='', colors=None, err=None, val_size=9.5):
    """Grouped vertical bars. cats: labels; series: [(name, [values])]; err: {name: [(lo, hi)]}. Baseline at zero."""
    vals = [v for _, vs in series for v in vs if v is not None]
    if err: vals += [e[1] for es in err.values() for e in es if e and e[1] is not None]
    ymax = ymax or (max(vals) * 1.15 if vals else 1)
    fig.add(f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{MUTED}" stroke-width="1"/>')
    for i in range(1, 5):
        gy = y + h - h * i / 4
        fig.add(f'<line x1="{x}" y1="{gy:.1f}" x2="{x+w}" y2="{gy:.1f}" stroke="{GRID}" stroke-width="1"/>' + T(x - 5, gy + 3.5, fmt.format(ymax * i / 4), size=9.5, anchor='end'))
    if ylabel: fig.add(T(x - 5, y - 8, ylabel, size=10, anchor='start'))
    cw = w / len(cats); bw = min(34, cw * 0.8 / len(series))
    for ci_, c in enumerate(cats):
        cx = x + cw * (ci_ + .5)
        for li, line in enumerate(str(c).split('\n')): fig.add(T(cx, y + h + 14 + li * 12, line, size=10.5, fill=INK))
        for si, (name, vs) in enumerate(series):
            v = vs[ci_]
            if v is None: continue
            col = (colors or {}).get(name, SERIES[si]); bx = cx - bw * len(series) / 2 + si * bw
            bh = h * v / ymax
            fig.add(f'<rect x="{bx+1:.1f}" y="{y+h-bh:.1f}" width="{bw-2:.1f}" height="{bh:.1f}" rx="2" fill="{col}"/>')
            top = y + h - bh
            if err and err.get(name) and err[name][ci_] and err[name][ci_][0] is not None:
                lo, hi = err[name][ci_]; y1, y2 = y + h - h * max(0, lo) / ymax, y + h - h * min(ymax, hi) / ymax
                fig.add(f'<line x1="{bx+bw/2:.1f}" y1="{y1:.1f}" x2="{bx+bw/2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="1.2"/>')
                top = min(top, y2)
            fig.add(T(bx + bw / 2, top - 3, fmt.format(v), size=val_size, fill=INK))
