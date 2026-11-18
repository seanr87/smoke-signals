# Timeline access for round 5b: the files smoke-signals 0.4.0 writes beside the smoke records.
# Usage (after `from r5lib import *` and `S, G = load5()`):
#   from tl import *
#   add_times(S)                 # exact elapsed seconds on every smoke: e0 (activation), ecap (fully laid), e1 (dispersed)
#   g = TL(s['game'])            # timelines of one game, cached
# All times here are elapsed seconds since battle start (the `elapsed_s` column), the same moment in both runs of a
# game to within 0.75 s. Positions are raw world units unless a function says normalized.
import os, csv, json, bisect, math, collections
import common
from common import BATCH, WU, norm, F

GAMES_DIR = os.path.join(BATCH, 'games')
TL_DIR = os.path.join(BATCH, 'timelines')

def _csv(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))
def _f(v):
    return float(v) if v not in ('', None) else None

_runs = None
def runs():
    """Every run folder: list of dicts {dir, key (match_id, game_no), team (primary team name), primary_replay, start (battle
    start in that run's replay clock), game (its game.json)}."""
    global _runs
    if _runs is None:
        _runs = []
        for d in sorted(os.listdir(GAMES_DIR)):
            p = os.path.join(GAMES_DIR, d, 'game.json')
            if not os.path.exists(p): continue
            g = json.load(open(p, encoding='utf-8'))
            _runs.append(dict(dir=d, key=(g['match_id'], g['game_no']), primary_replay=g['primary_replay'], start=g['battle_start_s'], game=g))
    return _runs

_start = None
def run_start(match_id, game_no, primary_replay):
    global _start
    if _start is None:
        _start = {(r['key'][0], r['key'][1], r['primary_replay']): r['start'] for r in runs()}
    return _start[(match_id, game_no, primary_replay)]

def add_times(S):
    """Adds exact elapsed seconds to every smoke from its own run's replay clock: e0 activation (creation when no activation
    was seen), ecap fully laid, eend emission end, e1 dispersed (None when the replay ended first)."""
    for s in S:
        j = s['j']; st = run_start(j['match_id'], j['game_no'], j['primary_replay'])
        sec = lambda k: (j[k]['seconds'] - st) if j.get(k) else None
        s['e0'] = sec('t_activate') if j.get('t_activate') else sec('t_created')
        s['ecap'] = sec('t_capture'); s['eend'] = sec('t_emission_end'); s['e1'] = sec('t_dispersed')
    return S

class Track:
    """One ship's samples every 2 s from its own team's replay: t, x, z (world units), alive, det (True/False/None), hp, maxhp."""
    __slots__ = ('eid', 'player', 'ship', 'team', 'own', 't', 'x', 'z', 'alive', 'det', 'hp', 'maxhp')
    def __init__(self, eid, player, ship, team, own):
        self.eid, self.player, self.ship, self.team, self.own = eid, player, ship, team, own
        self.t, self.x, self.z, self.alive, self.det, self.hp, self.maxhp = [], [], [], [], [], [], []
    def idx(self, t):
        """Index of the last sample at or before t (None before the first)."""
        i = bisect.bisect_right(self.t, t) - 1
        return i if i >= 0 else None
    def pos(self, t):
        """(x, z) at t, interpolated between the two neighbouring samples; None when unknown."""
        i = self.idx(t)
        if i is None: return None
        if self.x[i] is None: return None
        if i + 1 < len(self.t) and self.x[i + 1] is not None and self.t[i + 1] > self.t[i]:
            f = (t - self.t[i]) / (self.t[i + 1] - self.t[i])
            return self.x[i] + (self.x[i + 1] - self.x[i]) * f, self.z[i] + (self.z[i + 1] - self.z[i]) * f
        return self.x[i], self.z[i]
    def health(self, t):
        """(health, max health) at the last sample at or before t; None when unknown."""
        i = self.idx(t)
        return (self.hp[i], self.maxhp[i]) if i is not None and self.hp[i] is not None else None
    def death_t(self):
        """Elapsed second of the first sample at which the ship is no longer alive; None when it survived."""
        for i, a in enumerate(self.alive):
            if not a: return self.t[i]
        return None
    def last_alive_pos(self):
        """Position at the last sample while alive (the death position to within 2 s)."""
        for i in range(len(self.t) - 1, -1, -1):
            if self.alive[i] and self.x[i] is not None: return self.x[i], self.z[i]
        return None

class GameTL:
    def __init__(self, key):
        self.key = key
        rs = [r for r in runs() if r['key'] == key]
        self.runs = rs
        d = next((x for x in os.listdir(TL_DIR) if _meta(x)['match_id'] == key[0] and _meta(x)['game_no'] == key[1]), None)
        self.dir = d; self.meta = _meta(d)
        self.one_sided = self.meta['one_sided']
        base = os.path.join(TL_DIR, d)
        # caps: {real letter: [(t, owner or None, invader or None)]}; frame: {team: {real letter: frame letter}}
        self.caps = collections.defaultdict(list); self.frame = {}
        for r in _csv(os.path.join(base, 'caps_timeline.csv')):
            self.caps[r['cap']].append((float(r['elapsed_s']), r['owner'] or None, r['invader'] or None))
            for i in (0, 1):
                if r.get(f'frame_team_{i}'): self.frame.setdefault(r[f'frame_team_{i}'], {})[r['cap']] = r[f'cap_frame_{i}'] or None
        self.score = collections.defaultdict(list)
        for r in _csv(os.path.join(base, 'score.csv')):
            self.score[r['team']].append((float(r['elapsed_s']), int(r['score'])))
        # radar and hydro rows, numbers converted
        self.sensor = []
        for r in _csv(os.path.join(base, 'radar.csv')):
            for k in ('t_s', 'elapsed_s', 'x', 'z', 'range_m', 'duration_s', 'end_elapsed_s', 'lit_start_elapsed_s', 'lit_end_elapsed_s', 'target_x', 'target_z',
                      'target_distance_m', 'target_min_distance_m'):
                r[k] = _f(r[k])
            for k in ('entity_id', 'target_entity_id'):
                r[k] = int(r[k]) if r[k] else None
            r['ambiguous'] = r['ambiguous'] == 'true'
            r['source_in_smoke'] = [int(x) for x in r['source_in_smoke'].split(';') if x]
            r['target_in_smoke'] = [int(x) for x in r['target_in_smoke'].split(';') if x]
            self.sensor.append(r)
        # tracks from every run (each run holds its own team; a single-replay game holds both in its one run)
        self.tracks = {}
        self.ribbons = []
        for run in rs:
            p = os.path.join(GAMES_DIR, run['dir'], 'tracks.csv')
            if os.path.exists(p):
                for r in _csv(p):
                    e = int(r['entity_id'])
                    tr = self.tracks.get(e)
                    if tr is None:
                        tr = self.tracks[e] = Track(e, r['player'], r['ship'].replace('\xa0', ' '), r['team'], r['own_replay'] == 'true')
                    tr.t.append(float(r['elapsed_s'])); tr.x.append(_f(r['x'])); tr.z.append(_f(r['z']))
                    tr.alive.append(r['alive'] == 'true'); tr.det.append(None if r['detected'] == '' else r['detected'] == 'true')
                    tr.hp.append(_f(r['health'])); tr.maxhp.append(_f(r['max_health']))
            p = os.path.join(GAMES_DIR, run['dir'], 'ribbons.csv')
            if os.path.exists(p):
                for r in _csv(p):
                    r['elapsed_s'] = float(r['elapsed_s']); r['count'] = int(r['count']); r['entity_id'] = int(r['entity_id']) if r['entity_id'] else None
                    self.ribbons.append(r)
        self.ribbons.sort(key=lambda r: r['elapsed_s'])
    # ---- caps
    def owner_at(self, cap, t):
        """Owner team name (None = neutral) of real cap letter `cap` at elapsed t."""
        ev = self.caps.get(cap, [])
        i = bisect.bisect_right([e[0] for e in ev], t) - 1
        return ev[i][1] if i >= 0 else None
    def owner_changes(self, cap, t0, t1):
        """[(t, new owner)] for every owner change of `cap` in (t0, t1]."""
        out = []; prev = self.owner_at(cap, t0)
        for t, owner, _ in self.caps.get(cap, []):
            if t0 < t <= t1 and owner != prev:
                out.append((t, owner))
            if t > t0: prev = owner
        return out
    def invaded(self, cap, team, t0, t1):
        """Seconds within [t0, t1] during which `team` was the invader of `cap`."""
        ev = self.caps.get(cap, []); tot = 0.0
        for i, (t, _, inv) in enumerate(ev):
            end = ev[i + 1][0] if i + 1 < len(ev) else t1
            a, b = max(t, t0), min(end, t1)
            if inv == team and b > a: tot += b - a
        return tot
    def frame_letter(self, team, cap):
        return (self.frame.get(team) or {}).get(cap) or cap
    # ---- score
    def score_at(self, team, t):
        ev = self.score.get(team, [])
        i = bisect.bisect_right([e[0] for e in ev], t) - 1
        return ev[i][1] if i >= 0 else None
    # ---- ships
    def pos(self, eid, t):
        tr = self.tracks.get(eid)
        return tr.pos(t) if tr else None
    def npos(self, eid, t, mapname, side):
        """Team-normalized position of ship eid at t for a team spawning on `side`."""
        p = self.pos(eid, t)
        return norm(mapname, side, p[0], p[1]) if p else None
    def ships(self, team=None, alive_at=None):
        return [tr for tr in self.tracks.values() if (team is None or tr.team == team) and (alive_at is None or (tr.idx(alive_at) is not None and tr.alive[tr.idx(alive_at)]))]
    # ---- radar
    def activations(self, kind='radar', team=None):
        return [r for r in self.sensor if r['row'] == 'activation' and r['kind'] == kind and (team is None or r['team'] == team)]
    def lit(self, kind='radar', target=None, target_team=None, include_unattributed=True):
        return [r for r in self.sensor if r['kind'] == kind and (r['row'] == 'lit' or (include_unattributed and r['row'] == 'lit_unattributed'))
                and (target is None or r['target_entity_id'] == target) and (target_team is None or r['target_team'] == target_team)]

_metas = {}
def _meta(d):
    if d not in _metas:
        _metas[d] = json.load(open(os.path.join(TL_DIR, d, 'meta.json'), encoding='utf-8'))
    return _metas[d]

_tl = {}
def TL(key):
    if key not in _tl:
        _tl[key] = GameTL(key)
    return _tl[key]

def dist_m(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) * WU

def smoke_dist_m(s, p):
    """Metres from raw world point p to the nearest puff centre of smoke s, minus nothing (centre distance)."""
    return min(math.hypot(p[0] - x, p[1] - z) for x, z in s['path']) * WU

def in_smoke(s, p):
    """True when raw world point p lies inside smoke s (within one smoke radius of a puff centre)."""
    return smoke_dist_m(s, p) <= s['radius_m']
