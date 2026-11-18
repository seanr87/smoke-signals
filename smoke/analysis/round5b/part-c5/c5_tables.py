import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
# Prints the markdown tables that FINDINGS-C5.md quotes, from map-questions.json (run after c5_merge.py).
Q = json.load(open(os.path.join(HERE, 'map-questions.json'), encoding='utf-8'))['questions']
print('SG-2 list')
print('| Smoke | Clan | Time | Cell | Cruiser | Other destroyers alive | Second destroyer recorded (where) |\n|---|---|---|---|---|---|---|')
for r in Q['C5-SG-2']['smokes']:
    d = '; '.join(f"{x['ship']} in {x['cell']}, {x['dist_m'] / 1000:.1f} km from the smoke, {x['fwd_m'] / 1000:+.1f} km forward, " + ('inside the smoke' if x['how'] == 'inside' else f"{abs(x['cap_edge_m']) / 1000:.1f} km {'inside' if x['cap_edge_m'] < 0 else 'outside'} cap {x['cap']}") for x in r['second_dds']) or 'none recorded'
    print(f"| [{r['slug']}]({r['link']}) | {r['team']} | {r['time']} | {r['cell']} | {', '.join(c[0] + ' ' + c[1] for c in r['cruisers']) or 'none'} | {', '.join(r['other_dds_alive'])} | {d} |")
print('\nHS-3 list')
for r in Q['C5-HS-3']['smokes']: print(f"- [{r['team']} {r['ship']} {r['time']} {r['cell']}]({r['link']}): {', '.join(c[0] + ' ' + c[1] for c in r['cruisers']) or 'no cruiser'}")
print('\nMR-2 list')
for r in Q['C5-MR-2']['smokes']: print(f"- [{r['team']} {r['ship']} {r['time']}]({r['link']}): B {r['own']} at start; enemy took B: {r['enemy_took']}; we took B: {r['we_took']}")
print('\nOK-1')
print('| Ship | Class | Smokes | Team-games with the ship in the lineup | Ships fielded | Smokes per team-game played | Top 6 smokes | Concealed dmg per smoke | Deaths per 100 |\n|---|---|---|---|---|---|---|---|---|')
for d in Q['C5-OK-1']['ships'][:6]: print(f"| {d['ship']} | {d['cls']} | {d['smokes']} | {d['team_games_in_lineup']} (Top 6 {d['top6_team_games']}) | {d['ship_slots']} | {d['smokes_per_team_game']} | {d['top6_smokes']} | {d['conc'] / 1000:.1f}k | {d['deaths_per_100']} |")
