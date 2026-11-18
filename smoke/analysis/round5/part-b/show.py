# Prints compact views of ships.json (used to write FINDINGS-B.md). Run: python -I -X utf8 show.py
import json, os
J = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ships.json'), encoding='utf-8'))
def rows(rs, keys, groups=None):
    for r in rs:
        if groups and not any(r['group'].startswith(g) for g in groups): continue
        print(r['group'][:28], r['split'], r.get('n', ''), '|', ' | '.join(f"{k}={r.get(k)}{'' if not r.get(k + '_ci') else ' ' + str(r[k + '_ci'])}" for k in keys))
def cons(cs, pref=None):
    for c in cs:
        if pref and not any(p in c['contrast'] for p in pref): continue
        print(c['contrast'], '|', c['metric'], c['diff'], c['ci'], '*' if c['clear'] else '')
print('--B3'); rows(J['B3']['rows'], ['conc_per_smoke', 'edge_med_m', 'teammate_share_of_damage_pct', 'selfish_pct', 'smoker_only_label_pct', 'enemy_radar_spotted_pct', 'enemy_radar_broad_pct'])
print(); rows(J['B3']['rows'], ['centre_pct', 'side_lane_pct', 'map_edge_pct', 'land_med_m', 'near_land_pct', 'open_water_pct', 'deaths_per_100'])
cons(J['B3']['contrasts'])
print('--B3H'); rows(J['B3']['harugumo']['rows'], ['own_gun_share_pct', 'own_conc_per_smoke', 'mate_conc_per_smoke', 'smoker_dealt_any_pct', 'smoker_dealt_5k_pct', 'smoker_time_in_smoke_s_med', 'smoker_time_share_of_life_pct'])
print(); rows(J['B3']['harugumo']['rows'], ['second_dd_recorded_pct', 'second_dd_forward_pct', 'second_dd_in_smoke_pct', 'radar_cruiser_inside_pct', 'our_radar_used_from_smoke_pct', 'path_med_m'])
cons(J['B3']['harugumo']['contrasts'])
print('--B4'); rows(J['B4']['rows'], ['spread_km', 'edge_iqr_m', 'edge_med_m', 'top_purpose_pct', 'purpose_entropy_bits', 'parked_pct', 'between_pct', 'line_1km_pct', 'path_med_m'])
cons(J['B4']['contrasts'])
