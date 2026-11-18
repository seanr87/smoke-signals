# Shared setup for the round 3 analysis modules. Read-only on the batch; writes only under smoke/analysis/round3/.
# Usage inside a module script (smoke/analysis/round3/module-N/x.py):
#   import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#   from common import *
#   S, G = load()
import csv, json, os, sys, math, random, statistics, collections, subprocess, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# SMOKE_DATA_ROOT names the folder that holds output/ when it is not this checkout (a second working folder);
# SMOKE_BATCH names another batch folder under output/.
ROOT = os.environ.get('SMOKE_DATA_ROOT') or os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BATCH_NAME = 'output/' + (os.environ.get('SMOKE_BATCH') or '20261117-122135')
BATCH = os.path.join(ROOT, *BATCH_NAME.split('/'))
MAP_SRC = os.path.join(ROOT, 'output', '20261103-143026', 'maps')
MAP_DST = os.path.join(HERE, 'maps')
TOP = {'H-SR', 'RESIN', 'HTDOG', 'KITE', 'VRTUS', 'BONKZ'}
PN = 'PN'
WU = 30.0  # metres per world unit
C = collections.Counter
random.seed(19)

BLUE, ORANGE, VIOLET, INK, MUTED, GRID, BG = '#2a78d6', '#eb6834', '#6250d6', '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
AQUA, YELLOW, MAGENTA, GREEN, RED = '#1baf7a', '#eda100', '#e87ba4', '#008300', '#e34948'
SERIES = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED]
SEQ = ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b']  # light to dark, one hue
GROUP_COLOR = {'top': BLUE, 'rest': ORANGE}
GROUP_LABEL = {'top': 'Top 6', 'rest': 'Rest'}

F = lambda v: float(v) if v not in ('', None) else None
def secs(c):
    m, s = c.split(':'); return int(m) * 60 + int(s)
def mean(v):
    v = list(v); return sum(v) / len(v) if v else None
def med(v):
    v = list(v); return statistics.median(v) if v else None
def q(v, p):
    v = sorted(v)
    if not v: return None
    k = (len(v) - 1) * p; f = int(k)
    return v[f] + (v[min(f + 1, len(v) - 1)] - v[f]) * (k - f)
def pct(v, f=lambda x: x):
    v = list(v); return 100 * sum(1 for x in v if f(x)) / len(v) if v else None
def n0(x, f='{:,.0f}'): return '-' if x is None else f.format(x)
def sg(x, f='{:+,.0f}'): return '-' if x is None else f.format(x)
def small(n): return ' (small n)' if n < 15 else ''

# ---------- maps and team normalization
MAPS = {m['title']: m for m in json.load(open(os.path.join(MAP_SRC, 'maps.json'), encoding='utf-8'))}
DIAGONAL = {'Okinawa'}  # spawns north-east and south-west; every other map spawns north and south
def norm(mapname, side, x, z):
    """Team-normalize a world position so the smoking team's spawn is at the bottom of the map.
    South-spawn teams are unchanged. North-spawn teams are mirrored north-south (z -> -z); on Okinawa,
    whose spawns sit on the NE-SW diagonal, they are mirrored across the NW-SE diagonal ((x, z) -> (-z, -x)).
    Every map's caps map onto caps under its mirror, so the minimap stays a valid background."""
    if side == 'south': return x, z
    return (-z, -x) if mapname in DIAGONAL else (x, -z)
NORM_NOTE = {m: ('north-spawn teams mirrored across the NW-SE diagonal (spawns are NE and SW)' if m in DIAGONAL else 'north-spawn teams mirrored north-south') for m in MAPS}
def cell(mapname, x, z):
    """(col, row) on the 10 x 10 grid: col 0..9 west to east (numbers 1..10), row 0..9 north to south (letters A..J)."""
    size = MAPS[mapname]['space_size']
    c = min(9, max(0, int((x + size / 2) / size * 10))); r = min(9, max(0, int((size / 2 - z) / size * 10)))
    return c, r
def cell_name(c, r): return 'ABCDEFGHIJ'[r] + str(c + 1)
def cell_centre(mapname, c, r):
    size = MAPS[mapname]['space_size']
    return (c + 0.5) / 10 * size - size / 2, size / 2 - (r + 0.5) / 10 * size

SITE = 'https://seanr87.github.io/smoke-signals/smoke/'
# Module 1's four smoke habits (ship clusters). Ships outside the 14 clustered there are 'other'.
HABIT = {**{k: 'flank smoke lines' for k in ('Somers', 'Gearing', 'Harugumo', 'Delny')},
         **{k: 'cap sitters' for k in ('Daring', 'Z-42', 'Gda\u0144sk', 'Grozovoi', 'Shimakaze')},
         **{k: 'parked cruiser smoke' for k in ('Svea', 'Jinan')},
         **{k: 'moving exhaust' for k in ('Napoli', 'Venezia', 'C. Colombo')}}
HABITS = ['flank smoke lines', 'cap sitters', 'parked cruiser smoke', 'moving exhaust']
def forward(mapname, dx, dz):
    """Metres toward the enemy spawn (positive = forward) of a team-normalized offset in world units.
    North-south maps: +z. Okinawa: along the south-west to north-east diagonal."""
    return ((dx + dz) / math.sqrt(2) if mapname in DIAGONAL else dz) * WU
def uv(mapname, nx, nz):
    """Team-normalized world position to the 0-1 minimap frame: origin top-left, u to the right (west to east),
    v down (north to south); own spawn at the bottom (bottom-left on Okinawa). Same frame as the map image."""
    size = MAPS[mapname]['space_size']
    return (nx + size / 2) / size, (size / 2 - nz) / size
def uv_len(mapname, metres):
    return metres / WU / MAPS[mapname]['space_size']

# ---------- load
_cache = None
def load():
    """Returns (S, G): smokes (list of dicts) and games (dict keyed by (match_id, game_no)).
    Smoke fields (all positions in world units, 1 unit = 30 m; n* = team-normalized):
      team, opponent, grp ('top'|'rest'), is_pn, cls ('destroyer'|'cruiser'|'battleship'), ship, map, side, game (key),
      el (seconds elapsed at activation), win (team won the game), x, z, nx, nz (centroid of the laid path), path, npath,
      ncell (col, row), ncell_name, radius_m, emission_s, life_s, kind ('long DD'|'short DD'|'cruiser'|'exhaust'|'other'),
      edge (m from smoke edge to contested cap edge, negative inside), inside (bool), cap (contested cap letter), ncap (letter of
      the cap at the normalized position), cap_r_m, mrA (tied to Mountain Range cap A), own ('ours'|'theirs'|'neutral'),
      conc (concealed smoke damage incl. torpedoes), total, guns, torp, deaths, kills, cap_won, cap_def (0/1), swing (score gap
      change activation to capture), score_diff (ours - theirs at activation), coverage, movement, pp (primary purpose or 'none'),
      tags (all purpose tags), counter_of (smoke id or ''), overlap_ids, selfish (bool),
      partners: list of {ship, cls, how ('inside'|'behind'|'line_of_fire'), radar (bool), secs, dmg, conc, nx, nz} (allies covered, not the smoker),
      shooters: list of {ship, cls, radar, dmg, conc, kills, is_smoker}, smoker_radar (bool),
      radar_cap {cap, ship, coverage_pct, full, activated} or None, off_radar {ship, activations, enemies_spotted} or None,
      radar_on_us (count of radar detections of our ships inside), targets: list of {ship, cls, dmg, sunk},
      r (csv row), j (json record).
    Round 4 additions: habit (Module 1 cluster of the ship, or 'other'), radar_ca_inside (a radar cruiser was inside the smoke),
      radar_ca_any (a radar cruiser was covered: inside, behind or in the line of fire), radar_play (primary purpose is cap_control or
      radar_trap), slug, link (smoke page on the published site), obs_emission_s, cut_short, path_m (length laid),
      cast: every ship with a known position at the moment the smoke was fully laid (the only moment the batch records positions):
        {eid, ally, ship, cls, radar, nx, nz, dist_m (to the nearest puff centre), is_smoker, how ('inside'|'behind'|'line_of_fire'|
        'outside' for allies, 'enemy' for enemies), fwd_m (metres toward the enemy relative to the smoke centre)},
      targets also carry eid, nx, nz (position at that same moment, None if unknown).
    Game fields: key, map, mapid, teams (names), winner, len (seconds), caps [{cap, x, z, r}], sides {team: side},
      roster {entity_id: player dict + team}, j."""
    global _cache
    if _cache: return _cache
    G = {}
    gd = os.path.join(BATCH, 'games')
    for d in sorted(os.listdir(gd)):
        p = os.path.join(gd, d, 'game.json')
        if not os.path.exists(p): continue
        j = json.load(open(p, encoding='utf-8'))
        k = (j['match_id'], j['game_no'])
        if k in G: continue
        roster = {}
        for t in j['teams']:
            for pl in t['players']: roster[pl['entity_id']] = dict(pl, team=t['name'])
        G[k] = dict(key=k, map=j['map_display'], mapid=j['map'], teams=[t['name'] for t in j['teams']],
                    winner=(j['outcome'].get('win') or {}).get('team'), len=None,
                    caps=[dict(cap=c['cap'], x=c['position']['x'], z=c['position']['z'], r=c['radius']) for c in j['caps']],
                    sides={t['name']: t['spawn_side'] for t in j['teams']}, final={t['name']: t['final_score'] for t in j['teams']}, roster=roster, j=j)
        be = j.get('battle_end') or {}
        if be.get('clock'): G[k]['len'] = 1200 - secs(be['clock'])
    rows = list(csv.DictReader(open(os.path.join(BATCH, 'smokes.csv'), encoding='utf-8')))
    js = {(s['match_id'], int(s['game_no']), str(s['smoke_id'])): s for s in json.load(open(os.path.join(BATCH, 'smokes.json'), encoding='utf-8'))}
    S = []
    for r in rows:
        j = js[(r['match_id'], int(r['game_no']), r['smoke_id'])]; g = G[(r['match_id'], int(r['game_no']))]
        s = dict(r=r, j=j, id=r['smoke_id'], team=r['team'], opponent=r['opponent'], grp='top' if r['team'] in TOP else 'rest', is_pn=r['team'] == PN,
                 cls=r['smoker_class'], ship=r['ship'].replace('\xa0', ' '), map=r['map_display'], side=r['spawn_side'], game=g['key'], player=r['player'])
        c = r['t_activate_clock'] or r['t_created_clock']
        s['el'] = 1200 - secs(c)
        s['win'] = g['winner'] == r['team']
        xs = [p['x'] for p in j['path']]; zs = [p['z'] for p in j['path']]
        s['x'], s['z'] = mean(xs), mean(zs)
        s['path'] = [(p['x'], p['z']) for p in j['path']]
        s['npath'] = [norm(s['map'], s['side'], x, z) for x, z in s['path']]
        s['nx'], s['nz'] = norm(s['map'], s['side'], s['x'], s['z'])
        s['ncell'] = cell(s['map'], s['nx'], s['nz']); s['ncell_name'] = cell_name(*s['ncell'])
        s['radius_m'] = F(r['radius']) * WU; s['emission_s'] = F(r['base_emission_s']); s['life_s'] = F(r['base_puff_life_s'])
        st = r['smoke_type']
        s['kind'] = ('exhaust' if st == 'exhaust' else 'short DD' if s['cls'] == 'destroyer' and st == 'cruiser' else 'long DD' if s['cls'] == 'destroyer' and st == 'standard'
                     else 'cruiser' if s['cls'] == 'cruiser' else 'other')
        s['edge'] = F(r['avg_contested_cap_dist_m']); s['inside'] = s['edge'] < 0
        s['cap'] = r['contested_cap_name']; s['cap_r_m'] = F(r['contested_cap_radius_m']); s['mrA'] = s['cap_r_m'] > 9000
        s['ncap'] = ncap_name(g, s['map'], s['side'], s['cap'])
        own = 'unknown'
        for part in r['cap_state_act'].split():
            kk, v = part.split(':', 1)
            if kk == s['cap']:
                v = v.rstrip('!'); own = 'neutral' if v == '-' else ('ours' if v == r['team'] else 'theirs')
        s['own'] = own
        s['conc'] = F(r['smoke_damage_concealed']) or 0.0; s['total'] = F(r['smoke_damage_total']) or 0.0
        s['guns'] = sum(F(r[k]) or 0 for k in ('damage_shell', 'damage_fire', 'damage_airstrike')); s['torp'] = F(r.get('damage_torpedo')) or 0.0
        s['deaths'] = int(r['smoke_deaths'] or 0); s['kills'] = int(r['kills_from_smoke'] or 0)
        s['cap_won'] = 1 if r['cap_won'] else 0; s['cap_def'] = 1 if r['cap_defended'] else 0
        s['score_diff'] = int(r['score_ours_act']) - int(r['score_theirs_act'])
        s['swing'] = (int(r['score_ours_cap']) - int(r['score_theirs_cap'])) - s['score_diff'] if r['score_ours_cap'] != '' else None
        s['coverage'] = r['coverage']; s['movement'] = r['movement'] or 'unclassified'; s['pp'] = r['primary_purpose'] or 'none'
        s['tags'] = [p['tag'] for p in j['classification']['purposes']]
        s['counter_of'] = r['counter_smoke_of']; s['overlap_ids'] = [str(x) for x in j['overlapping_smoke_ids']]; s['selfish'] = r['selfish_smoke'] == 'true'
        pos = {p['entity_id']: p['position'] for p in j['ships_at_capture'] if p.get('position')}
        ro = g['roster']
        smoker_eid = next((x['entity_id'] for x in j['smokees'] if x['role'] == 'smoker'), None)
        s['smoker_radar'] = bool(ro.get(smoker_eid, {}).get('radar_m'))
        s['partners'] = []
        for x in j['smokees']:
            if x['role'] == 'smoker' or x['how'] == 'none': continue
            pl = ro.get(x['entity_id'], {})
            p = pos.get(x['entity_id'])
            nx, nz = norm(s['map'], s['side'], p['x'], p['z']) if p else (None, None)
            s['partners'].append(dict(ship=x['ship'], cls=x['ship_class'].lower(), how=x['how'], radar=bool(pl.get('radar_m')), secs=x['seconds_concealed'],
                                      dmg=x['damage'], conc=x['split']['concealed'], nx=nx, nz=nz))
        s['shooters'] = [dict(ship=x['ship'], cls=(ro.get(x['entity_id'], {}).get('ship_class') or '').lower(), radar=bool(ro.get(x['entity_id'], {}).get('radar_m')),
                              dmg=x['damage'], conc=x['split']['concealed'], kills=x['kills'], is_smoker=x['entity_id'] == smoker_eid) for x in j['shooter_detail']]
        s['radar_cap'] = j.get('radar_cap'); s['off_radar'] = j.get('offensive_radar')
        s['radar_on_us'] = int(r['radar_detections_count'] or 0)
        s['targets'] = [dict(ship=x['ship'], cls=x['ship_class'].lower(), dmg=x['damage'], sunk=x['sunk']) for x in j['targets_hit']]
        # round 4 additions
        s['habit'] = HABIT.get(s['ship'], 'other')
        s['radar_ca_inside'] = any(p['cls'] == 'cruiser' and p['radar'] and p['how'] == 'inside' for p in s['partners'])
        s['radar_ca_any'] = any(p['cls'] == 'cruiser' and p['radar'] for p in s['partners'])
        s['radar_play'] = s['pp'] in ('cap_control', 'radar_trap')
        s['slug'] = f"{r['match_id'].split('_')[1]}_g{r['game_no']}_{r['smoke_id']}"; s['link'] = SITE + 'smokes/' + s['slug'] + '.html'
        s['obs_emission_s'] = F(r['observed_emission_s']); s['cut_short'] = r['emission_cut_short'] == 'true'
        s['path_m'] = F(r['movement_path_m'])
        how = {x['entity_id']: x['how'] for x in j['smokees']}
        s['smoker_eid'] = smoker_eid
        cast = []
        for p in j['ships_at_capture']:
            if not p.get('position'): continue
            pl = ro.get(p['entity_id'], {})
            nx, nz = norm(s['map'], s['side'], p['position']['x'], p['position']['z'])
            d = min(math.hypot(nx - a, nz - b) for a, b in s['npath']) * WU
            cast.append(dict(eid=p['entity_id'], ally=p['team'] == r['team'], ship=(pl.get('ship') or '?').replace('\xa0', ' '), cls=p['ship_class'].lower(),
                             radar=bool(pl.get('radar_m')), nx=nx, nz=nz, dist_m=d, is_smoker=p['entity_id'] == smoker_eid,
                             how=how.get(p['entity_id'], 'outside') if p['team'] == r['team'] else 'enemy',
                             fwd_m=forward(s['map'], nx - s['nx'], nz - s['nz'])))
        s['cast'] = cast
        tpos = {c['eid']: c for c in cast}
        for t, x in zip(s['targets'], j['targets_hit']):
            c = tpos.get(x['entity_id']); t['eid'] = x['entity_id']; t['nx'], t['nz'] = (c['nx'], c['nz']) if c else (None, None)
        S.append(s)
    _cache = (S, G)
    return _cache

def ncaps(g, mapname, side):
    """Caps of a game in the normalized frame for a team spawning on `side`: list of {cap (real letter), x, z, r}."""
    return [dict(cap=c['cap'], r=c['r'], **dict(zip(('x', 'z'), norm(mapname, side, c['x'], c['z'])))) for c in g['caps']]
def ncap_name(g, mapname, side, cap):
    """Letter of the cap that sits where `cap` lands after normalization (so 'A' always means the same place on the map)."""
    c = next((c for c in g['caps'] if c['cap'] == cap), None)
    if not c: return cap
    x, z = norm(mapname, side, c['x'], c['z'])
    return min(g['caps'], key=lambda o: math.hypot(o['x'] - x, o['z'] - z))['cap']
def map_caps(G, mapname):
    """Caps of a map in real map coordinates (same in every game of that map)."""
    return next(g['caps'] for g in G.values() if g['map'] == mapname)
def win_loss(G):
    w, n = C(), C()
    for g in G.values():
        for t in g['teams']: n[t] += 1; w[t] += g['winner'] == t
    return {t: (w[t], n[t] - w[t]) for t in n}
def team_games(G):
    """List of (game key, team) for every team-game, for per-game rates."""
    return [(g['key'], t) for g in G.values() for t in g['teams']]
def snapshots(S, gkey):
    """Score and cap-owner snapshots of one game, from every smoke's activation and capture states, sorted by elapsed seconds.
    Each: (el, {team: score}, {cap: owner team or None}). The batch has no continuous score or cap timeline; this is the nearest thing."""
    out = []
    for s in S:
        if s['game'] != gkey: continue
        for st, clock in ((s['j']['state_at_activate'], s['r']['t_activate_clock'] or s['r']['t_created_clock']), (s['j']['state_at_capture'], s['r']['t_capture_clock'])):
            if not st or not clock or st.get('score_ours') is None: continue
            out.append((1200 - secs(clock), {s['team']: st['score_ours'], s['opponent']: st['score_theirs']}, {c['cap']: c['owner'] for c in st['cap_state']}))
    return sorted(out, key=lambda x: x[0])

# ---------- intervals
def by(ss, key):
    d = collections.defaultdict(list)
    for s in ss: d[key(s) if callable(key) else s[key]].append(s)
    return d
def boot_diff(ss, stat, reps=1000):
    """95% interval of stat(top smokes) - stat(rest smokes), resampling whole clans within each group. stat takes a list of smokes."""
    cl = by(ss, 'team'); tops = [c for c in cl if c in TOP]; rest = [c for c in cl if c not in TOP]
    if not tops or not rest: return (None, None)
    out = []
    for _ in range(reps):
        a = [x for c in random.choices(tops, k=len(tops)) for x in cl[c]]; b = [x for c in random.choices(rest, k=len(rest)) for x in cl[c]]
        va, vb = stat(a), stat(b)
        if va is not None and vb is not None: out.append(va - vb)
    if not out: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def boot_stat(ss, stat, cluster='team', reps=1000):
    """95% interval of stat(smokes), resampling whole clusters (clans by default; pass cluster='game' where clans do not apply)."""
    cl = by(ss, cluster); keys = list(cl)
    if not keys: return (None, None)
    out = []
    for _ in range(reps):
        v = stat([x for c in random.choices(keys, k=len(keys)) for x in cl[c]])
        if v is not None: out.append(v)
    if not out: return (None, None)
    out.sort(); return out[int(.025 * len(out))], out[max(0, int(.975 * len(out)) - 1)]
def ci(lohi, f='{:+,.0f}'):
    if lohi[0] is None: return '-'
    return f'{f.format(lohi[0])} to {f.format(lohi[1])}' + (' *' if lohi[0] * lohi[1] > 0 else '')
def md_table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)

# ---------- figures (SVG, rendered to PNG with headless Edge; no plotting library is installed)
def ensure_maps():
    os.makedirs(MAP_DST, exist_ok=True)
    for m in MAPS.values():
        src = os.path.join(MAP_SRC, m['image'].replace('.png', '.webp')); dst = os.path.join(MAP_DST, os.path.basename(src))
        if not os.path.exists(dst): shutil.copyfile(src, dst)
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def T(x, y, s, size=11.5, fill=MUTED, anchor='middle', weight='400', halo=False):
    h = f' stroke="{BG}" stroke-width="3" paint-order="stroke" stroke-linejoin="round"' if halo else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{h}>{esc(s)}</text>'

class Panel:
    """One map view. World coordinates in, pixels out. If normalized=True the caller passes team-normalized coordinates
    (own spawn at the bottom) and the panel labels itself that way."""
    def __init__(self, mapname, x0, y0, size, G, title=None, dim=0.35, grid=True, caps=True, normalized=True, grid_labels=True):
        self.map, self.x0, self.y0, self.size = mapname, x0, y0, size
        Panel._n = getattr(Panel, '_n', 0) + 1; self.uid = Panel._n  # unique clip id (object ids get reused)
        self.space = MAPS[mapname]['space_size']; self.out = []
        img = '../maps/' + MAPS[mapname]['image'].replace('.png', '.webp')
        o = f'<image href="{img}" x="{x0}" y="{y0}" width="{size}" height="{size}" preserveAspectRatio="none"/>'
        o += f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" fill="{BG}" opacity="{dim}"/>'
        if grid:
            for i in range(11):
                p = i * size / 10
                o += f'<line x1="{x0+p:.1f}" y1="{y0}" x2="{x0+p:.1f}" y2="{y0+size}" stroke="{INK}" stroke-width="0.5" opacity="0.25"/>'
                o += f'<line x1="{x0}" y1="{y0+p:.1f}" x2="{x0+size}" y2="{y0+p:.1f}" stroke="{INK}" stroke-width="0.5" opacity="0.25"/>'
            if grid_labels:
                for i in range(10):
                    o += T(x0 + (i + .5) * size / 10, y0 - 3, str(i + 1), size=8.5) + T(x0 - 4, y0 + (i + .5) * size / 10 + 3, 'ABCDEFGHIJ'[i], size=8.5, anchor='end')
        o += f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" fill="none" stroke="{MUTED}" stroke-width="1"/>'
        if caps:
            for c in map_caps(G, mapname):
                px, py = self.xy(c['x'], c['z']); r = c['r'] / self.space * size
                o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.8" clip-path="url(#clip{self.uid})"/>'
                if x0 - 1 <= px <= x0 + size + 1: o += T(min(max(px, x0 + 8), x0 + size - 8), py + 4, c['cap'], size=11, fill=INK, weight='700', halo=True)
        if title: o += T(x0, y0 - (16 if grid and grid_labels else 6), title, size=12.5, fill=INK, anchor='start', weight='600')
        if normalized: o += T(x0 + size / 2, y0 + size + 12, 'own spawn at the bottom left' if mapname in DIAGONAL else 'own spawn at the bottom', size=9)
        self.base = f'<clipPath id="clip{self.uid}"><rect x="{x0}" y="{y0}" width="{size}" height="{size}"/></clipPath>' + o
    def xy(self, x, z):
        return self.x0 + (x + self.space / 2) / self.space * self.size, self.y0 + (self.space / 2 - z) / self.space * self.size
    def px(self, metres): return metres / WU / self.space * self.size
    def dot(self, x, z, r=3, fill=BLUE, opacity=0.6, stroke=None, title=None):
        px, py = self.xy(x, z); st = f' stroke="{stroke}" stroke-width="1"' if stroke else ''
        tt = f'<title>{esc(title)}</title>' if title else ''
        self.out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{fill}" opacity="{opacity}"{st}>{tt}</circle>')
    def ring(self, x, z, r, stroke=INK, width=1.5, dash=None, opacity=1):
        px, py = self.xy(x, z); d = f' stroke-dasharray="{dash}"' if dash else ''
        self.out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="none" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"{d}/>')
    def line(self, pts, stroke=BLUE, width=1.5, opacity=0.7, arrow=False, dash=None):
        p = [self.xy(x, z) for x, z in pts]
        if len(p) < 2: return
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.out.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in p)}" fill="none" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"{d}/>')
        if arrow:
            (x1, y1), (x2, y2) = p[-2], p[-1]; a = math.atan2(y2 - y1, x2 - x1); L = 5 + width
            pts2 = [(x2, y2), (x2 - L * math.cos(a - .45), y2 - L * math.sin(a - .45)), (x2 - L * math.cos(a + .45), y2 - L * math.sin(a + .45))]
            self.out.append(f'<polygon points="{" ".join(f"{a_:.1f},{b_:.1f}" for a_, b_ in pts2)}" fill="{stroke}" opacity="{opacity}"/>')
    def cellfill(self, c, r, fill, opacity=0.75, text=None, text_fill=INK, sub=None, stroke=None):
        s = self.size / 10; x, y = self.x0 + c * s, self.y0 + r * s
        st = f' stroke="{stroke}" stroke-width="2"' if stroke else ''
        self.out.append(f'<rect x="{x+1:.1f}" y="{y+1:.1f}" width="{s-2:.1f}" height="{s-2:.1f}" rx="2" fill="{fill}" opacity="{opacity}"{st}/>')
        if text is not None: self.out.append(T(x + s / 2, y + s / 2 + (0 if sub else 3.5), text, size=max(7.5, s * 0.3), fill=text_fill, weight='600'))
        if sub is not None: self.out.append(T(x + s / 2, y + s / 2 + s * 0.32, sub, size=max(6.5, s * 0.22), fill=text_fill))
    def text(self, x, z, s, size=10, fill=INK, weight='600', anchor='middle', dy=0):
        px, py = self.xy(x, z); self.out.append(T(px, py + dy, s, size=size, fill=fill, weight=weight, anchor=anchor, halo=True))
    def raw(self, svg): self.out.append(svg)
    def render(self):
        return self.base + f'<g clip-path="url(#clip{self.uid})">' + ''.join(self.out) + '</g>'

def seq_color(v, vmax, vmin=0):
    if v is None or vmax is None or vmax <= vmin: return GRID
    t = min(1, max(0, (v - vmin) / (vmax - vmin))); return SEQ[min(len(SEQ) - 1, int(t * len(SEQ)))]
def seq_text(v, vmax, vmin=0):
    if v is None or vmax is None or vmax <= vmin: return INK
    return BG if (v - vmin) / (vmax - vmin) > 0.45 else INK
def div_color(v, vmax):
    """Diverging: blue for positive (top / good), orange for negative, grey at zero."""
    if v is None or not vmax: return GRID
    t = max(-1, min(1, v / vmax)); ramp_pos = ['#f0efec', '#b7d3f6', '#6da7ec', '#2a78d6', '#184f95']; ramp_neg = ['#f0efec', '#f8c9b6', '#f29a78', '#eb6834', '#b0451c']
    r = ramp_pos if t >= 0 else ramp_neg; return r[min(4, int(abs(t) * 4 + 0.5))]

class Fig:
    def __init__(self, w, h, title, sub=''):
        self.w, self.h, self.body = w, h, []
        self.body.append(f'<rect width="{w}" height="{h}" fill="{BG}"/>' + T(24, 30, title, size=17, fill=INK, anchor='start', weight='600') + (T(24, 48, sub, size=12, anchor='start') if sub else ''))
    def add(self, svg): self.body.append(svg if isinstance(svg, str) else svg.render())
    def legend(self, x, y, items, r=6):
        """items: [(label, colour)] drawn in one row."""
        for lab, col in items:
            self.body.append(f'<rect x="{x}" y="{y-9}" width="12" height="12" rx="2" fill="{col}"/>' + T(x + 17, y + 1, lab, size=12, fill=INK, anchor='start'))
            x += 17 + 7 * len(lab) + 22
    def save(self, path_no_ext, png=True):
        os.makedirs(os.path.dirname(path_no_ext), exist_ok=True); ensure_maps()
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" font-family="Segoe UI, Arial, sans-serif">' + ''.join(self.body) + '</svg>'
        open(path_no_ext + '.svg', 'w', encoding='utf-8').write(svg)
        if png: render_png(path_no_ext + '.svg', self.w, self.h)

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
def render_png(svg_path, w, h, scale=2):
    """SVG to PNG next to it, with headless Edge. Edge can return before the file is written, so wait for it."""
    import time
    png = svg_path[:-4] + '.png'
    if os.path.exists(png): os.remove(png)
    prof = tempfile.mkdtemp(prefix='edge-r3-')
    url = 'file:///' + os.path.abspath(svg_path).replace('\\', '/').replace(' ', '%20')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--force-device-scale-factor={scale}', f'--user-data-dir={prof}',
                    f'--window-size={w},{h}', f'--screenshot={os.path.abspath(png)}', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    for _ in range(40):
        if os.path.exists(png) and os.path.getsize(png) > 0: break
        time.sleep(0.25)
    shutil.rmtree(prof, ignore_errors=True)
    return png

def bar_rows(fig, x, y, w, rows, vmax=None, fmt='{:,.0f}', row_h=22, label_w=120, colors=None, note=None):
    """Horizontal bars. rows: [(label, value, n or None)] or grouped [(label, {'top': v, 'rest': v}, note)]. Returns the y after the block."""
    vals = []
    for r in rows:
        vals += [v for v in (r[1].values() if isinstance(r[1], dict) else [r[1]]) if v is not None]
    vmax = vmax or (max(vals) if vals else 1) or 1
    for lab, v, nn in rows:
        fig.add(T(x + label_w - 8, y + row_h / 2 + 4, lab, size=11.5, fill=INK, anchor='end'))
        items = list(v.items()) if isinstance(v, dict) else [(None, v)]
        bh = (row_h - 6) / len(items)
        for i, (g, val) in enumerate(items):
            if val is None: continue
            col = (colors or GROUP_COLOR).get(g, BLUE) if g else BLUE
            bw = max(1, (w - label_w - 70) * val / vmax)
            fig.add(f'<rect x="{x+label_w}" y="{y+3+i*bh:.1f}" width="{bw:.1f}" height="{bh-1.5:.1f}" rx="2" fill="{col}"/>' + T(x + label_w + bw + 4, y + 3 + i * bh + bh - 3, fmt.format(val), size=9.5, anchor='start'))
        if nn is not None: fig.add(T(x + w, y + row_h / 2 + 4, str(nn), size=9.5, anchor='end'))
        y += row_h
    return y

if __name__ == '__main__':
    S, G = load()
    wl = win_loss(G)
    print('batch', BATCH_NAME, 'smokes', len(S), 'games', len(G))
    print('top 6 W-L:', {t: wl[t] for t in sorted(TOP)}, '| PN', wl.get(PN))
    dd = [s for s in S if s['cls'] == 'destroyer']
    print('DD smokes top/rest/PN:', sum(s['grp'] == 'top' for s in dd), sum(s['grp'] == 'rest' for s in dd), sum(s['is_pn'] for s in dd), '| kinds', dict(C(s['kind'] for s in S)))
    print('partners per smoke', round(mean(len(s['partners']) for s in S), 2), '| partner pos missing', sum(1 for s in S for p in s['partners'] if p['nx'] is None), 'of', sum(len(s['partners']) for s in S))
    print('ncap changes', sum(s['cap'] != s['ncap'] for s in S), '| swing missing', sum(s['swing'] is None for s in S), '| game len missing', sum(g['len'] is None for g in G.values()))
    maps = sorted(MAPS, key=lambda m: -sum(s['map'] == m for s in dd))
    fig = Fig(1180, 760, 'Check: destroyer smokes, team-normalized', 'Top 6 blue, rest orange. Dot = centre of the laid smoke.')
    for i, m in enumerate(maps):
        p = Panel(m, 40 + (i % 4) * 285, 110 + (i // 4) * 320, 250, G, title=m)
        for s in dd:
            if s['map'] == m: p.dot(s['nx'], s['nz'], r=2.6, fill=GROUP_COLOR[s['grp']], opacity=0.55)
        fig.add(p)
    fig.legend(40, 68, [('Top 6', BLUE), ('Rest', ORANGE)])
    fig.save(os.path.join(HERE, 'check', 'normalized-check'))
    print('figure ok')
