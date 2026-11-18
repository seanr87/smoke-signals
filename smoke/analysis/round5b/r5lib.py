# Shared definitions for analysis round 5. Read-only on the batch; writes only under smoke/analysis/round5/.
# Usage inside a part script (smoke/analysis/round5/part-x/y.py), run with: python -I -X utf8 y.py
#   import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#   from r5lib import *
#   S, G = load5()
# Everything in round3/common.py is re-exported (load, boot_diff, boot_stat, Panel, Fig, uv, ...).
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), 'round3'))
# Round 5b reads the batch named in batch.json. Batch outputs stay out of git, so in a second working folder the
# data root is the checkout that holds output/ (data_root_fallback, relative to the repository root).
import json as _json
_cfg = _json.load(open(os.path.join(_HERE, 'batch.json'), encoding='utf-8'))
os.environ.setdefault('SMOKE_BATCH', _cfg['batch'])
_repo = os.path.abspath(os.path.join(_HERE, '..', '..', '..'))
if not os.path.isdir(os.path.join(_repo, 'output', _cfg['batch'])):
    os.environ.setdefault('SMOKE_DATA_ROOT', os.path.abspath(os.path.join(_repo, _cfg['data_root_fallback'])))
from common import *
import csv, json, math, collections

R5 = _HERE
EARLY_S = 300          # "early" = activated in the first 5 minutes
HURT_SHARE = 1 / 3     # "lost at least a third of its health"
TOOK_GRACE_S = 60      # how long after a smoke clears a cap snapshot still counts for "enemy took the cap"
LONG_SHIPS = ('Somers', 'Gearing', 'Harugumo', 'Delny')
SITTERS = ('Daring', 'Gdańsk', 'Z-42', 'Z-52', 'Grozovoi', 'Shimakaze')
GETAWAY = ('Napoli', 'Venezia', 'C. Colombo', 'Conte Verde')

# Seconds by which common.py overstates elapsed time in a game that did not run on a 20-minute clock (filled by load5).
CLOCK_OFFSET = {}
_common_snapshots = snapshots
def snapshots(S, gkey):
    """common.snapshots with the elapsed times corrected for games on a shorter clock."""
    off = CLOCK_OFFSET.get(gkey, 0)
    return [(t - off, a, b) for t, a, b in _common_snapshots(S, gkey)]

def el_of(clock):
    return 1200 - secs(clock) if clock else None

def score_state(d):
    return 'behind 50+' if d <= -50 else 'ahead 50+' if d >= 50 else 'level'

def clan_counts(ss, top_first=True):
    """'RESIN 5, H-SR 4 | Rest: PN 2, MZY 1' style clan counts for a list of smokes."""
    c = C(s['team'] for s in ss)
    t = ', '.join(f'{k} {v}' for k, v in c.most_common() if k in TOP) or 'none'
    r = ', '.join(f'{k} {v}' for k, v in c.most_common() if k not in TOP) or 'none'
    return f'Top 6: {t} | Rest: {r}'
def clan_dict(ss):
    c = C(s['team'] for s in ss)
    return dict(top6={k: v for k, v in c.most_common() if k in TOP}, rest={k: v for k, v in c.most_common() if k not in TOP})
def cruiser_counts(ss, how=None):
    """Counter of cruiser ship names covered by the smokes (how: None = any, or 'inside' / 'screened')."""
    return C(c['ship'] for s in ss for c in s['cruisers'] if how is None or (c['how'] == 'inside') == (how == 'inside'))

_cache5 = None
def load5():
    """Returns (S, G) from common.load() with round 5 fields added to every smoke:
      t0, t1: elapsed seconds at activation and when the smoke had dispersed.
      state: 'behind 50+' | 'level' | 'ahead 50+' (score gap at activation).
      land_m, lane ('left'|'center'|'right', batch field, real map side), lane_offset_m, frontline_m.
      cruisers: [{ship, how ('inside'|'screened'), radar}] allied cruisers covered by the smoke. 'screened' = behind the smoke or
        firing through it (batch 'behind' and 'line_of_fire'); 'inside' = inside it.
      cr_inside (any cruiser inside), cr_screened (a cruiser covered but none inside), cr_any.
      early_cruiser: destroyer smoke, activated in the first 5 minutes, covering at least one cruiser (any destroyer ship).
        early_mode: 'inside' | 'screened' for those, else None.
      cover3: 'radar cruiser inside' | 'non-radar cruiser inside' (a cruiser inside and no radar-equipped ship inside, smoker
        included) | 'no cruiser' (no cruiser inside or screened) | 'other' (cruiser screened only, or a non-radar cruiser inside
        next to a radar ship of another class).
      near_cap: letter of the nearest cap (smoke centre to cap edge, computed here; the batch's contested cap is a different thing),
        near_ncap: that cap's letter in the team-normalized frame, near_cap_edge_m: metres from smoke centre to its edge (negative inside); near_own: 'ours'|'theirs'|'neutral' at activation.
      enemy_took: True / False / None. For the nearest cap: the cap was not the enemy's at activation, and a cap snapshot taken
        while the smoke stood or within 60 s after it cleared shows the enemy owning it. None = cap already the enemy's, or no
        snapshot in that window (the batch has cap owners only at the activation and capture moments of each smoke in the game).
      we_took: same test for our side (cap not ours at activation, ours in a later snapshot in the window).
      took_window: number of snapshots available in the window (0 = unknown).
      dead: list of ships that died in or behind this smoke (batch smoke_deaths):
        {eid, ship, cls, is_smoker, where ('inside'|'behind'), t (elapsed s), after_cleared, radar_lit (bool: an enemy radar
         detected this ship in this smoke within 40 s before the death), radar_src {ship, cls, dist_m} or None,
         killers [{ship, cls, kind, dmg}] damage on the victim in the last 20 s before death (from damage_events.csv),
         kinds {kind: damage}, torp (bool: any torpedo damage in those 20 s), top_kind, by_cls {attacker class: damage}}.
      d_smoker (1 if the smoker died), d_cr (cruisers that died), d_other.
      shelter: [{eid, ship, cls, how, taken, hp_est, hurt (died or took >= 1/3 of estimated health), died}] every allied ship the
        smoke covered, smoker included (how 'smoker'). n_cr_in: cruisers inside or behind. hurt_smoker (0/1), hurt_cr (count).
      detect: Counter of detection kinds recorded on the smoker while concealed (batch smokees.detected_by).
      undetected_pct: share of the smoker's concealed time it stayed undetected (batch).
    Health estimate: the batch has no ship health. hp_est(ship) is the lower quartile of total damage received by ships of that
      type that died (damage_events.csv), which is close to base health for destroyers and roughly 10-20% high for ships that heal; ship types with fewer than 8 deaths use their class median.
    """
    global _cache5
    if _cache5: return _cache5
    S, G = load()
    # Round 5b fix: common.py reads elapsed time as 1200 - HUD clock, which assumes a 20-minute game. Two games ran on a
    # 15-minute clock, so their elapsed times were 300 s too high. The offset per game comes from the exact elapsed time
    # of its smokes (replay clock minus battle start).
    import statistics as _st
    import tl as _tl
    _d = collections.defaultdict(list)
    for s in S:
        j = s['j']; t = j.get('t_activate') or j.get('t_created')
        _d[s['game']].append(s['el'] - (t['seconds'] - _tl.run_start(j['match_id'], j['game_no'], j['primary_replay'])))
    CLOCK_OFFSET.clear()
    CLOCK_OFFSET.update({k: int(round(_st.median(v) / 60.0)) * 60 for k, v in _d.items() if abs(_st.median(v)) >= 30})
    for s in S:
        s['el'] -= CLOCK_OFFSET.get(s['game'], 0)
    for k, off in CLOCK_OFFSET.items():
        if G[k]['len'] is not None: G[k]['len'] -= off
    # damage events, one run per game
    gd = os.path.join(BATCH, 'games'); ev = {}
    for d in sorted(os.listdir(gd)):
        p = os.path.join(gd, d, 'game.json')
        if not os.path.exists(p): continue
        j = json.load(open(p, encoding='utf-8')); k = (j['match_id'], j['game_no'])
        if k in ev: continue
        rows = []
        f = os.path.join(gd, d, 'damage_events.csv')
        if os.path.exists(f):
            for r in csv.DictReader(open(f, encoding='utf-8')):
                rows.append((int(r['victim']), float(r['damage_s']), float(r['amount']), r['kind'], int(r['attacker']) if r['attacker'] else None))
        ev[k] = rows
        G[k]['t_start'] = j['battle_start_s']
    by_victim = {k: by([dict(v=a, t=b, amt=c, kind=d_, att=e) for a, b, c, d_, e in rows], 'v') for k, rows in ev.items()}
    taken = collections.defaultdict(list)
    for k, g in G.items():
        for e, p in g['roster'].items():
            if p.get('death'):
                tot = sum(x['amt'] for x in by_victim[k].get(e, []))
                if tot > 0: taken[p['ship'].replace('\xa0', ' ')].append(tot)
    hp = {sh: q(v, .25) for sh, v in taken.items() if len(v) >= 8}
    cls_hp = collections.defaultdict(list)
    for k, g in G.items():
        for p in g['roster'].values():
            sh = p['ship'].replace('\xa0', ' ')
            if sh in hp: cls_hp[p['ship_class'].lower()].append(hp[sh])
    cls_hp = {c: med(v) for c, v in cls_hp.items()}
    G['_hp'] = None  # placeholder removed below
    del G['_hp']
    snaps = {}
    for s in S:
        r, j, g = s['r'], s['j'], G[s['game']]
        ro = g['roster']
        _off = CLOCK_OFFSET.get(s['game'], 0)
        s['t0'] = s['el']; s['t1'] = (el_of(r['t_dispersed_clock']) - _off) if r['t_dispersed_clock'] else (s['el'] + (s['emission_s'] or 0) + (s['life_s'] or 0))
        s['state'] = score_state(s['score_diff'])
        s['land_m'] = F(r['land_distance_m']); s['lane'] = r['lane']; s['lane_offset_m'] = F(r['lane_offset_m']); s['frontline_m'] = F(r['frontline_distance_m'])
        s['cruisers'] = [dict(ship=p['ship'].replace('\xa0', ' '), how='inside' if p['how'] == 'inside' else 'screened', radar=p['radar']) for p in s['partners'] if p['cls'] == 'cruiser']
        s['cr_inside'] = any(c['how'] == 'inside' for c in s['cruisers']); s['cr_any'] = bool(s['cruisers']); s['cr_screened'] = s['cr_any'] and not s['cr_inside']
        s['early_cruiser'] = s['cls'] == 'destroyer' and s['el'] < EARLY_S and s['cr_any']
        s['early_mode'] = ('inside' if s['cr_inside'] else 'screened') if s['early_cruiser'] else None
        radar_inside = s['smoker_radar'] or any(p['radar'] and p['how'] == 'inside' for p in s['partners'])
        s['cover3'] = ('radar cruiser inside' if s['radar_ca_inside'] else 'non-radar cruiser inside' if s['cr_inside'] and not radar_inside
                       else 'no cruiser' if not s['cr_any'] else 'other')
        # nearest cap and what happened to it
        nc = min(g['caps'], key=lambda c: math.hypot(c['x'] - s['x'], c['z'] - s['z']) - c['r'])
        s['near_cap'] = nc['cap']; s['near_cap_edge_m'] = (math.hypot(nc['x'] - s['x'], nc['z'] - s['z']) - nc['r']) * WU
        s['near_ncap'] = ncap_name(g, s['map'], s['side'], nc['cap'])
        own = {c['cap']: c['owner'] for c in j['state_at_activate']['cap_state']} if j.get('state_at_activate') else {}
        o = own.get(s['near_cap'])
        s['near_own'] = 'neutral' if o is None else 'ours' if o == s['team'] else 'theirs'
        if s['game'] not in snaps: snaps[s['game']] = snapshots(S, s['game'])
        win = [x for x in snaps[s['game']] if s['t0'] < x[0] <= s['t1'] + TOOK_GRACE_S]
        s['took_window'] = len(win)
        owners = [x[2].get(s['near_cap']) for x in win]
        s['enemy_took'] = None if (s['near_own'] == 'theirs' or not win or not s['near_cap']) else any(x == s['opponent'] for x in owners)
        s['we_took'] = None if (s['near_own'] == 'ours' or not win or not s['near_cap']) else any(x == s['team'] for x in owners)
        # deaths
        smk = {x['entity_id']: x for x in j['smokees']}
        dead = []
        for d in j['smoke_deaths']:
            e = d['entity_id']; pl = ro.get(e, {}); td = d['death']['seconds']
            rd = [x for x in j['radar_detections_in_smoke'] if x['ship_entity'] == e and td - 40 <= x['seconds'] <= td + 1]
            src = None
            if rd:
                x = rd[-1]; sp = ro.get(x['source_entity'], {})
                src = dict(ship=(sp.get('ship') or '?').replace('\xa0', ' '), cls=(sp.get('ship_class') or '').lower(), dist_m=x['source_distance_m'])
            last = [x for x in by_victim[s['game']].get(e, []) if td - 20 <= x['t'] <= td + 1]
            kinds = C(); bycls = C(); kl = C()
            for x in last:
                ap = ro.get(x['att'], {}); kinds[x['kind']] += x['amt']; bycls[(ap.get('ship_class') or 'unknown').lower()] += x['amt']
                kl[((ap.get('ship') or '?').replace('\xa0', ' '), (ap.get('ship_class') or 'unknown').lower(), x['kind'])] += x['amt']
            dead.append(dict(eid=e, ship=(pl.get('ship') or d['ship']).replace('\xa0', ' '), cls=(pl.get('ship_class') or '').lower(), is_smoker=e == s['smoker_eid'],
                             where=d['concealed'], t=1200 - secs(d['death']['clock']) - _off, after_cleared=d['after_cleared'], radar_lit=bool(rd), radar_src=src,
                             killers=[dict(ship=a, cls=b, kind=c_, dmg=v) for (a, b, c_), v in kl.most_common(5)], kinds=dict(kinds), torp=kinds.get('torpedo', 0) > 0,
                             top_kind=kinds.most_common(1)[0][0] if kinds else None, by_cls=dict(bycls)))
        s['dead'] = dead
        s['d_smoker'] = int(any(d['is_smoker'] for d in dead)); s['d_cr'] = sum(1 for d in dead if d['cls'] == 'cruiser' and not d['is_smoker'])
        s['d_other'] = len(dead) - s['d_smoker'] - s['d_cr']
        dead_ids = {d['eid'] for d in dead}
        sh = []
        for x in j['smokees']:
            if x['how'] == 'none': continue
            pl = ro.get(x['entity_id'], {}); name = (pl.get('ship') or x['ship']).replace('\xa0', ' '); cl = x['ship_class'].lower()
            h = hp.get(name) or cls_hp.get(cl)
            died = x['entity_id'] in dead_ids
            sh.append(dict(eid=x['entity_id'], ship=name, cls=cl, how='smoker' if x['role'] == 'smoker' else x['how'], taken=x.get('damage_taken') or 0.0, hp_est=h,
                           died=died, hurt=died or (h is not None and (x.get('damage_taken') or 0) >= HURT_SHARE * h)))
        s['shelter'] = sh
        s['n_cr_in'] = sum(1 for x in sh if x['cls'] == 'cruiser' and x['how'] in ('inside', 'behind'))
        s['hurt_smoker'] = int(any(x['hurt'] for x in sh if x['how'] == 'smoker'))
        s['hurt_cr'] = sum(1 for x in sh if x['cls'] == 'cruiser' and x['how'] in ('inside', 'behind') and x['hurt'])
        me = smk.get(s['smoker_eid'], {})
        s['detect'] = C(x['kind'] for x in me.get('detected_by', [])); s['undetected_pct'] = me.get('undetected_pct')
    _cache5 = (S, G)
    load5.hp = hp; load5.cls_hp = cls_hp
    return _cache5

def cap_holders(S, G, gkey, t=480, tol=60):
    """Cap owners of one game at elapsed second t, from the nearest smoke snapshot within tol seconds. Returns {cap: team or None}
    or None when no snapshot is that close."""
    sn = snapshots(S, gkey)
    if not sn: return None
    x = min(sn, key=lambda x: abs(x[0] - t))
    return x[2] if abs(x[0] - t) <= tol else None

def rate100(ss, key):
    return 100 * sum(s[key] for s in ss) / len(ss) if ss else None

def spot_record(map_, kind, mode, name, ss_all, members, shape, extra=None):
    """One spots.json record. members = the smokes in the spot; shape = dict(type='circle', u, v, r) or dict(type='cells', cells=[..])
    or dict(type='polygon', points=[[u, v], ...]) in the 0-1 minimap frame (see common.uv). mode is 'top6' or 'shared'."""
    top = [s for s in members if s['grp'] == 'top']; rest = [s for s in members if s['grp'] == 'rest']
    rec = dict(map=map_, kind=kind, mode=mode, name=name, shape=shape, n=len(members), n_top6=len(top), n_rest=len(rest),
               small_n=len(members) < 15, clans=clan_dict(members),
               concealed_damage_per_smoke=round(mean(s['conc'] for s in members)) if members else None,
               deaths_per_100=round(rate100(members, 'deaths'), 1) if members else None,
               cruisers=dict(top6=dict(cruiser_counts(top).most_common()), rest=dict(cruiser_counts(rest).most_common())),
               examples=[s['link'] for s in sorted(members, key=lambda s: -s['conc'])[:3]])
    if extra: rec.update(extra)
    return rec
