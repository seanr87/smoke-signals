# Round 5c shared definitions. Analysis only: reads batch output/20261117-230933, writes only under smoke/analysis/round5c/.
# Usage inside a script in round5c/<folder>/ (run: python -I -X utf8 script.py):
#   import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#   from r5clib import *
#   S, G = load5c()
# Re-exports everything from round5b/r5lib.py (load5, boot_diff, boot_stat, ci, md_table, by, clan_counts, spot_record, ...),
# round3/common.py (Panel, Fig, uv, ...) and round5b/tl.py (TL, add_times, in_smoke, smoke_dist_m, dist_m, runs).
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), 'round5b'))
from r5lib import *
from tl import *
import math, collections, random

R5C = _HERE
DEATH_GRACE_S = 20.0     # "died": between activation and exactly 20 s after the smoke dispersed
CAP_GRACE_S = 60.0       # cap results: owner changes up to 60 s after the smoke dispersed
EARLY_S = 300.0          # "early": replay clock under 300 s at activation

def smoke_end(s):
    """Elapsed second at which the smoke had dispersed; estimated from emission time and puff life when the replay ended first."""
    return s['e1'] if s['e1'] is not None else s['e0'] + (s['emission_s'] or 0) + (s['life_s'] or 0)

def _took(g, cap, t0, t1, team, other):
    """(we_took, enemy_took) for one cap from the cap timeline. None when not applicable (cap already that side's at t0)."""
    if not cap or cap not in g.caps: return None, None
    own = g.owner_at(cap, t0)
    ch = g.owner_changes(cap, t0, t1)
    we = None if own == team else any(o == team for _, o in ch)
    en = None if own == other else any(o == other for _, o in ch)
    return we, en

_cache = None
def load5c():
    """Returns (S, G) with the round 5c fields on every smoke.

    Time
      e0, ecap, eend, e1 (from tl.add_times), end (= smoke_end), early (bool: e0 < 300 s; the HUD-clock `el` is not used).
    Deaths, two metrics kept side by side
      caught*: the batch `smoke_deaths` list (ships that died while the smoke concealed them or just after it cleared around them).
        caught (count), caught_smoker (0/1), caught_cr (sheltering cruisers), caught_other.
      died*: track deaths. A covered ship (the smoker, or a ship the batch lists as inside or behind the smoke) that died between
        e0 and end + 20 s, using the exact death time in the game record. Each dead ship is counted once: it is given to the
        latest smoke (largest e0) that covered it within the window, so sums over smokes count distinct ships.
        died (count), died_smoker (0/1), died_cr (sheltering cruisers), died_other, died_list [{eid, ship, cls, is_smoker, t}].
        died_any* (died_any, died_any_smoker, died_any_cr): the same without the once-only rule (a ship that dies within the
        window of two smokes counts in both); use only when a table needs every smoke judged on its own.
      covered: [{eid, ship, cls, is_smoker, how}] the smoker plus ships inside or behind. n_cr_cov: sheltering cruisers among them.
      died_ok: False for the 9 smokes of the single-replay game laid by the team with no replay (batch one_sided): their covered
        ships are known from the other side only. Leave them out of every "died" rate (they stay in "caught", as the batch has them).
    Caps (cap timeline only; never cap_won or the snapshot fields)
      For the contested cap (batch contested_cap_name, suffix _c) and the nearest cap (suffix _n), fixed at activation:
      own_c / own_n ('ours' | 'theirs' | 'neutral' at e0), we_took_c / we_took_n, enemy_took_c / enemy_took_n: an owner change to
      that side in (e0, end + 60 s]; None when not applicable (the cap was already that side's at e0).
    Radar (radar log)
      radar_pressed: a ship of the smoking team pressed radar while standing in this smoke (activation with this smoke id).
      radar_pressed_by_ca: that ship was a radar cruiser.
      lit_covered: a covered ship carried the radar flag at some time in [e0, end] (enemy radar).
    """
    global _cache
    if _cache: return _cache
    S, G = load5(); add_times(S)
    start = {k: g['j']['battle_start_s'] for k, g in G.items()}
    death_e = {k: {e: p['death']['seconds'] - start[k] for e, p in g['roster'].items() if p.get('death')} for k, g in G.items()}
    for s in S:
        g = TL(s['game']); ro = G[s['game']]['roster']
        s['end'] = smoke_end(s); s['early'] = s['e0'] < EARLY_S
        s['died_ok'] = s['r']['one_sided'] != 'true'
        cov = {}
        for x in s['shelter']:
            if x['how'] in ('smoker', 'inside', 'behind'):
                cov[x['eid']] = dict(eid=x['eid'], ship=x['ship'], cls=x['cls'], is_smoker=x['how'] == 'smoker', how=x['how'])
        if s['smoker_eid'] is not None and s['smoker_eid'] not in cov:
            cov[s['smoker_eid']] = dict(eid=s['smoker_eid'], ship=s['ship'], cls=s['cls'], is_smoker=True, how='smoker')
        s['covered'] = list(cov.values())
        s['n_cr_cov'] = sum(1 for c in s['covered'] if c['cls'] == 'cruiser' and not c['is_smoker'])
        s['caught'] = len(s['dead']); s['caught_smoker'] = s['d_smoker']; s['caught_cr'] = s['d_cr']; s['caught_other'] = s['d_other']
        de = death_e[s['game']]
        s['_cand'] = [dict(c, t=de[c['eid']]) for c in s['covered'] if c['eid'] in de and s['e0'] <= de[c['eid']] <= s['end'] + DEATH_GRACE_S]
        s['died_any'] = len(s['_cand']); s['died_any_smoker'] = int(any(c['is_smoker'] for c in s['_cand']))
        s['died_any_cr'] = sum(1 for c in s['_cand'] if c['cls'] == 'cruiser' and not c['is_smoker'])
        s['died_list'] = []
        for suf, cap in (('_c', s['cap']), ('_n', s['near_cap'])):
            o = g.owner_at(cap, s['e0']) if cap in g.caps else None
            s['own' + suf] = 'neutral' if o is None else 'ours' if o == s['team'] else 'theirs'
            s['we_took' + suf], s['enemy_took' + suf] = _took(g, cap, s['e0'], s['end'] + CAP_GRACE_S, s['team'], s['opponent'])
        sid = int(s['id'])
        pressed = [r for r in g.activations('radar', team=s['team']) if sid in r['source_in_smoke'] and s['e0'] - 1 <= r['elapsed_s'] <= s['end'] + 1]
        s['radar_pressed'] = bool(pressed)
        s['radar_pressed_by_ca'] = any((ro.get(r['entity_id'], {}).get('ship_class') or '').lower() == 'cruiser' for r in pressed)
        ids = set(cov)
        s['lit_covered'] = any(r['target_entity_id'] in ids and r['lit_end_elapsed_s'] >= s['e0'] and r['lit_start_elapsed_s'] <= s['end']
                               for r in g.lit('radar', target_team=s['team']))
    # each dead ship goes to the latest smoke that covered it within the window
    owner = {}
    for s in S:
        for c in s['_cand']:
            k = (s['game'], c['eid'])
            if k not in owner or s['e0'] > owner[k]['e0']: owner[k] = s
    for s in S:
        s['died_list'] = [c for c in s['_cand'] if owner[(s['game'], c['eid'])] is s]
        s['died'] = len(s['died_list']); s['died_smoker'] = int(any(c['is_smoker'] for c in s['died_list']))
        s['died_cr'] = sum(1 for c in s['died_list'] if c['cls'] == 'cruiser' and not c['is_smoker'])
        s['died_other'] = s['died'] - s['died_smoker'] - s['died_cr']
        del s['_cand']
    _cache = (S, G)
    return _cache

# ---------- rates, always the two death metrics side by side
def per100(ss, key):
    return 100.0 * sum(s[key] for s in ss) / len(ss) if ss else None

def death_rates(ss):
    """Both death metrics for a list of smokes. 'died' rates leave out smokes with died_ok False.
    Returns dict: n, n_died_base, died (ships), died_per100, died_smoker_per100, died_cr_per100_cov (per 100 sheltering cruisers),
    caught, caught_per100, caught_smoker_per100, caught_cr_per100_cov."""
    ok = [s for s in ss if s['died_ok']]
    ncr = sum(s['n_cr_cov'] for s in ok); ncr_all = sum(s['n_cr_in'] for s in ss)
    return dict(n=len(ss), n_died_base=len(ok), died=sum(s['died'] for s in ok), died_per100=per100(ok, 'died'),
                died_smoker_per100=per100(ok, 'died_smoker'), died_cr_per100_cov=100.0 * sum(s['died_cr'] for s in ok) / ncr if ncr else None,
                caught=sum(s['caught'] for s in ss), caught_per100=per100(ss, 'caught'), caught_smoker_per100=per100(ss, 'caught_smoker'),
                caught_cr_per100_cov=100.0 * sum(s['caught_cr'] for s in ss) / ncr_all if ncr_all else None)

def died100(ss):
    ok = [s for s in ss if s['died_ok']]
    return per100(ok, 'died')
def caught100(ss):
    return per100(ss, 'caught')
def died_smoker100(ss):
    return per100([s for s in ss if s['died_ok']], 'died_smoker')
def caught_smoker100(ss):
    return per100(ss, 'caught_smoker')

def share(ss, key):
    """Percent of smokes with s[key] True among those where it is not None; (pct, n applicable)."""
    v = [s[key] for s in ss if s[key] is not None]
    return (100.0 * sum(1 for x in v if x) / len(v) if v else None), len(v)

def share_stat(key, min_n=1):
    """A stat for boot_diff / boot_stat: percent True of s[key] among applicable smokes (None when fewer than min_n)."""
    def f(ss):
        v = [s[key] for s in ss if s[key] is not None]
        return 100.0 * sum(1 for x in v if x) / len(v) if len(v) >= min_n else None
    return f

def diff_ci(a, b, stat, reps=1000, seed=19):
    """95% interval of stat(a) - stat(b) for two lists of smokes, resampling whole clans over the union (a clan keeps its smokes in
    both lists). Use for gaps between two kinds of smoke inside one group."""
    rng = random.Random(seed)
    ca, cb = by(a, 'team'), by(b, 'team'); clans = sorted(set(ca) | set(cb))
    if not clans: return (None, None)
    out = []
    for _ in range(reps):
        pick = [rng.choice(clans) for _ in clans]
        x = stat([s for c in pick for s in ca.get(c, [])]); y = stat([s for c in pick for s in cb.get(c, [])])
        if x is not None and y is not None: out.append(x - y)
    if not out: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]

def tag(n):
    return 'too few' if n < 8 else 'small n' if n < 15 else ''
