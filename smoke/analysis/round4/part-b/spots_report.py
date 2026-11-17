# Writes spots.json and SPOTS.md. Executed at the end of spots_build.py (shares its variables); not run on its own.
def cap1(s): return s[:1].upper() + s[1:]
NOUN = {'cap sitters': 'cap-sitter smokes', 'parked cruiser smoke': 'parked cruiser smokes', 'flank smoke lines': 'flank smoke lines', 'moving exhaust': 'moving exhaust smokes'}
EXTRA = {'mr-parked-h1': ' Eight of the 12 are Jinan, a ship no Rest clan smoked with on this map, so part of this gap is ship choice.'}
def scale_note(c):
    out = []
    for h in ('1.5', '2.5'):
        rows = [r for r in CHK['scales'][h]['rows'] if r['map'] == c['map'] and r['subject'] == c['subject'] and math.hypot(r['cx'] - c['e'][0], r['cz'] - c['e'][1]) <= 3 * KM]
        out.append(f"{h} km: " + ('not found' if not rows else 'passes' if any(r['passes'] for r in rows) else 'found, interval touches zero'))
    return '; '.join(out)
def nt_words(ct):
    if not ct['nt_n']: return 'no damaged enemy had a recorded position'
    parts = []
    for role, n in ct['nt'].most_common():
        ships = C(); [ships.update({f'{sh} ({cl})': v}) for (r, sh, cl), v in ct['nt_ship'].items() if r == role]
        parts.append(f"{role} {n} ({top1(ships, 2)})")
    return f"of {ct['nt_n']} damaged enemies with a recorded position, the nearest ally was " + ', '.join(parts) + f"; median {ct['nt_dist'] / 1000:.1f} km away"
def near_words(ct):
    if not ct['near_cls']: return 'no other ally within 5 km'
    by_cls = collections.defaultdict(C)
    for (cl, how), v in ct['near_cls'].items(): by_cls[cl][how] += v
    parts = [f"{cl}s {sum(v.values())} ({', '.join(f'{h} {n}' for h, n in v.most_common())})" for cl, v in sorted(by_cls.items(), key=lambda kv: -sum(kv[1].values()))]
    return f"{ct['near_per_smoke']:.1f} other allies within 5 km per smoke: " + '; '.join(parts) + f"; most common {top1(ct['near_ship'], 3)}"
def dd_words(ct):
    if not ct['dd_n']: return 'no other destroyer had a recorded position'
    return (f"nearest other destroyer recorded for {ct['dd_n']} of {ct['n']} ({top1(ct['dd_ship'], 2)}): median {ct['dd_dist'] / 1000:.1f} km from the smoke, "
            f"forward of it in {ct['dd_fwd']} of {ct['dd_n']}, most often in {top1(ct['dd_cell'], 2)}; median {abs(ct['dd_cap_edge']) / 1000:.1f} km {'inside' if ct['dd_cap_edge'] < 0 else 'outside'} the contested cap's edge (inside the cap {ct['dd_in_cap']} of {ct['dd_cap_n']})")
def cr_words(ct):
    if not ct['cr_smokes']: return 'no other cruiser inside'
    return f"a cruiser inside in {ct['cr_smokes']} of {ct['n']} ({top1(ct['cr_ship'], 3)}; radar cruiser in {ct['cr_radar']}), median {ct['cr_dist'] / 1000:.1f} km from the nearest puff"
def partner_words(c):
    if not c['partner']: return 'no ally covered'
    sh, n = c['partner']; return f"{sh} ({n} of {len(c['tin'])} smokes)" if n >= 3 else f"none usual (most common {sh}, {n} of {len(c['tin'])})"
def formation(c):
    return f"{form_words(c)}: {c['f_top']} of {len(c['tin'])} Top 6 smokes; Rest {c['f_rest']} of {len(c['rin'])} in the same spot"
def notes(c):
    n = []
    if c['e'][2] * WU > 6000: n.append('wide zone, not a tight spot')
    if c.get('dup'): n.append('same place at habit level: ' + ', '.join(f"{d['subject']} ({len(d['tin'])}/{len(d['top'])} vs {len(d['rin'])}/{len(d['rest'])}, gap {d['gap']:+.0f})" for d in c['dup']))
    if c.get('twin'): n.append(f"same place as signature spot {c['twin']['id']}")
    if len(c['rest']) < MIN_N: n.append(f"Rest barely field this subject on this map (n {len(c['rest'])}), so the shares cannot be compared")
    if c['kind'] == 'habit': n.append('ships in the spot: ' + top1(C(s['ship'] for s in c['tin']), 4))
    n.append(f"without {c['big']} the Top 6 share is {c['ts_wo']:.0f}%")
    n.append('other scales: ' + scale_note(c))
    if c['tin'][0]['cls'] != 'destroyer' and c['kind'] == 'ship': n.append('cruiser smoke: the cruiser slot is for a second cruiser inside')
    return '; '.join(n)

recs = []
for c in sig + lead:
    e = c['e']; ct = c['ct']; m = c['map']; cu = uv(m, e[0], e[1])
    recs.append(dict(
        id=c['id'], map=m, kind='signature' if c in sig else 'lead', subject=c['subject'], label=c['label'], cells=c['cells'],
        centre_uv=[round(cu[0], 4), round(cu[1], 4)],
        ellipse_uv=dict(ru=round(uv_len(m, e[2] * WU), 4), rv=round(uv_len(m, e[3] * WU), 4), angle_deg=round(-math.degrees(e[4]), 1)),
        top6=dict(n_in=len(c['tin']), n_total=len(c['top']), share_pct=round(c['ts'], 1), clans=dict(c['clans'].most_common())),
        rest=dict(n_in=len(c['rin']), n_total=len(c['rest']), share_pct=round(c['rs'], 1)),
        gap_pts=round(c['gap'], 1), ci_pts=[round(c['lo'], 1), round(c['hi'], 1)], median_time_s=round(c['med_el']),
        usual_partner=c['partner'][0] if c['partner'] and c['partner'][1] >= 3 else None,
        conc_per_smoke=round(c['conc']), deaths_per_100=round(c['deaths'], 1), cap_won_pct=round(c['capwon'], 1) if c['capwon'] is not None else None, cap_won_n=c['capwon_n'],
        formation=formation(c), formation_top6=dict(count=c['f_top'], of=len(c['tin'])), formation_rest=dict(count=c['f_rest'], of=len(c['rin'])),
        cast=dict(
            cruiser=dict(ship=ct['cr_ship'].most_common(1)[0][0], centre_uv=[round(v, 4) for v in uv(m, *ct['cr_pos'])], n=ct['cr_smokes']) if ct['cr_smokes'] else None,
            second_dd=dict(ship=ct['dd_ship'].most_common(1)[0][0], centre_uv=[round(v, 4) for v in uv(m, *ct['dd_pos'])], n=ct['dd_n'], forward_share_pct=round(100 * ct['dd_fwd'] / ct['dd_n'], 1)) if ct['dd_n'] else None,
            nearest_to_target=dict(description=nt_words(ct), n=ct['nt_n']) if ct['nt_n'] else None),
        examples=[s['link'] for s in c['examples']], small_n=len(c['tin']) < 15, notes=notes(c)))
json.dump(recs, open(os.path.join(OUT, 'spots.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---------- SPOTS.md
pl = CHK['placebo']; pl_pass = [p['passed'] for p in pl]; pl_c = [p['candidates'] for p in pl]
raw_pass = sum(passes(c) for c in cands)
P = pat[HEAD]; PR = pat['radar cruiser inside']; PD = pat['second destroyer forward']; PA = pat['second destroyer alive with a known position']
def row(i, c):
    return [i, c['map'], c['subject'], c['label'], '/'.join(c['cells'][:4]), f"{len(c['tin'])} of {len(c['top'])} ({c['ts']:.0f}%)", f"{len(c['rin'])} of {len(c['rest'])} ({c['rs']:.0f}%)",
            f"{c['gap']:+.0f} ({c['lo']:+.0f} to {c['hi']:+.0f})", ', '.join(f'{k} {v}' for k, v in c['clans'].most_common()), f"{c['f_top']} of {len(c['tin'])}" + (' (small n)' if len(c['tin']) < 15 else '')]
HDR = ['#', 'Map', 'Ship / habit', 'Spot', 'Cells', 'Top 6 in spot', 'Rest in spot', 'Gap, pts (95%)', 'Top 6 clans', 'Formation count']
def para(i, c):
    e = c['e']; ct = c['ct']; cu = uv(c['map'], e[0], e[1])
    wide = ' This is a wide zone, not a tight spot.' if e[2] * WU > 6000 else ''
    o = f"**{i}. {c['map']}, {c['subject']}: {c['label']} ({'/'.join(c['cells'][:4])}).** "
    o += f"Top 6 put {len(c['tin'])} of {len(c['top'])} {NOUN.get(c['subject'], c['subject'] + ' smokes')} here ({c['ts']:.0f}%); the Rest {len(c['rin'])} of {len(c['rest'])} ({c['rs']:.0f}%). Gap {c['gap']:+.0f} pts ({c['lo']:+.0f} to {c['hi']:+.0f}). "
    o += f"Clans: {', '.join(f'{k} {v}' for k, v in c['clans'].most_common())}; without {c['big']} the Top 6 share is still {c['ts_wo']:.0f}%. "
    if c['kind'] == 'habit': o += f"Ships: {top1(C(s['ship'] for s in c['tin']), 4)}. "
    o += f"Centre u {cu[0]:.2f}, v {cu[1]:.2f}; radii {km(e[2]):.1f} x {km(e[3]):.1f} km.{wide}{EXTRA.get(c['id'], '')} "
    o += f"Median time {mmss(c['med_el'])}. Usual partner: {partner_words(c)}. This spot returned {c['conc']:,.0f} concealed damage per smoke, {c['deaths']:.0f} deaths per 100, and the contested cap was won on {n0(c['capwon'])}% of {c['capwon_n']} smokes where it was not already ours" + (' (small n)' if c['capwon_n'] < 15 else '') + '. '
    o += f"\n   - Cast when the smoke was fully laid: {near_words(ct)}. {cap1(cr_words(ct))}. {cap1(dd_words(ct))}."
    o += f"\n   - Nearest ally to the targets: {nt_words(ct)}."
    o += f"\n   - Formation: {formation(c)}." + (' The Rest have too few smokes here to compare.' if len(c['rin']) < MIN_N else '')
    if c.get('dup'): o += f"\n   - Same place at habit level ({c['dup'][0]['subject']}): {len(c['dup'][0]['tin'])} of {len(c['dup'][0]['top'])} vs {len(c['dup'][0]['rin'])} of {len(c['dup'][0]['rest'])}; the ship-level spot is kept."
    o += f"\n   - Other scales: {scale_note(c)}. Examples: " + ', '.join(f"[{s['team']} {s['slug']}]({s['link']})" for s in c['examples']) + f". Figure: `fig/spots-{MAPAB[c['map']]}.png`."
    return o

som = [s for s in S if s['map'] == 'Sleeping Giant' and s['ship'] == 'Somers']
west = lambda ss: pct(ss, lambda s: s['ncell'][0] <= 2); east = lambda ss: pct(ss, lambda s: s['ncell'][0] >= 7)
st, sr = [s for s in som if s['grp'] == 'top'], [s for s in som if s['grp'] == 'rest']
rg = random.Random(3)
ci_e = boot_gap(st, sr, lambda s: s['ncell'][0] >= 7, 1000, rg); ci_w = boot_gap(st, sr, lambda s: s['ncell'][0] <= 2, 1000, rg)
lofs = [s for s in S if s['map'] == 'Land of Fire' and s['ship'] == 'Svea']
pn_dd = [s for s in S if s['is_pn'] and s['cls'] == 'destroyer']
pn_in = [(s, c) for s in pn_dd for c in sig + lead if c['map'] == s['map'] and s[c['kind']] == c['subject'] and inside(c['e'], s['nx'], s['nz'])]
mrf = [c for c in cands if c['map'] == 'Mountain Range' and c['subject'] == 'flank smoke lines']
rv = reverse[0] if reverse else None

L = []
L.append('# Part B: signature spots\n')
L.append(f"Batch `{BATCH_NAME}`. Positions are team-normalized: own spawn at the bottom; north-spawn teams are mirrored north-south, and on Okinawa across the NW-SE diagonal (own spawn bottom-left). Everything here is association: where Top 6 smoke and what those smokes returned, not what causes a win.\n")
L.append('## Findings\n')
L.append(f"- **{len(sig)} signature spots and {len(lead)} leads**, from {len(cands)} candidate spots tested ({nsub} ship-or-habit x map combinations had at least 8 Top 6 smokes). {raw_pass} candidates passed the rule; {raw_pass - len(sig)} were the same place seen at both ship and habit level.")
L.append(f"- **Read these as 'where the Top 6 go', not as proven differences.** A placebo run (the same search with six busy Rest clans standing in as the 'top' group, 20 draws) passed {mean(pl_pass):.1f} spots on average (range {min(pl_pass)} to {max(pl_pass)}) out of {mean(pl_c):.0f} candidates. So any six clans show a few favourite spots; the Top 6 show {raw_pass}, more than any placebo draw, but roughly 2 or 3 of them are the kind any group would produce. Best supported as tight spots: 2 (Land of Fire Svea) and 5 (Sleeping Giant Harugumo). Spots 1 and 3 are clear but are wide zones. Weakest: 4 (two clans, and mostly a ship the Rest did not bring) and 6 (interval barely clear of zero).")
L.append(f"- **The one cast pattern that holds across maps is a radar cruiser inside the destroyer smoke**: {PR['top']:.0f}% of Top 6 destroyer smokes vs {PR['rest']:.0f}% of the Rest (gap {PR['top'] - PR['rest']:+.0f} pts, {PR['ci'][0]:+.0f} to {PR['ci'][1]:+.0f}). Adding 'second destroyer forward' makes it rare: {P['top']:.0f}% vs {P['rest']:.0f}%.")
L.append(f"- **Sleeping Giant Harugumo at G1/F1**: a radar cruiser is inside in {ck['cr_smokes']} of {ck['n']} (Des Moines or Worcester, not Brisbane); a second destroyer is recorded in {ck['dd_n']} of {ck['n']}.\n")
L.append('## Signature spots, ranked by gap\n')
L.append(md_table(HDR, [row(i + 1, c) for i, c in enumerate(sig)]))
L.append("\n'Formation count' = Top 6 smokes in the spot that match the spot's most common formation (described below). All spots have fewer than 15 Top 6 smokes unless stated, so every per-spot number is small n.\n")
for i, c in enumerate(sig): L.append(para(i + 1, c) + '\n')
L.append('## Leads (at least 2 Top 6 clans, interval touches zero or cannot be compared)\n')
L.append(md_table(HDR, [row('L%d' % (i + 1), c) for i, c in enumerate(lead)]))
L.append('')
for i, c in enumerate(lead):
    ct = c['ct']
    why = (f"the Rest have only {len(c['rest'])} {c['subject']} smoke on this map, so there is nothing to compare; it is the destroyer behind signature spot 3" if len(c['rest']) < MIN_N else
           f"same place as signature spot {c['twin']['id']}, one ship only" if c.get('twin') else f"without {c['big']} the Top 6 share falls to {c['ts_wo']:.0f}%")
    L.append(f"- **L{i + 1}. {c['map']}, {c['subject']}, {c['label']}**: {why}. Formation: {formation(c)}. Examples: " + ', '.join(f"[{s['team']} {s['slug']}]({s['link']})" for s in c['examples']) + '.')
L.append('')
L.append('Not spots, but worth knowing:')
L.append(f"- One-clan habits (fail the 2-clan rule): HTDOG on Sleeping Giant put {next(len(c['tin']) for c in single if c['id'] == 'sg-daring-f1')} of 16 Top 6 Daring smokes and {next(len(c['tin']) for c in single if c['id'] == 'sg-parked-g2')} of 20 parked cruiser smokes in the west by cap A (F1 to G2). The earlier 'Top 6 Daring west at G1/F1' is HTDOG alone.")
if rv: L.append(f"- A Rest spot: on Hotspot the east edge (G10/F10) holds {len(rv['rin'])} of {len(rv['rest'])} Rest flank-line smokes ({rv['rs']:.0f}%) vs {len(rv['tin'])} of {len(rv['top'])} Top 6 ({rv['ts']:.0f}%), gap {rv['gap']:+.0f} ({rv['lo']:+.0f} to {rv['hi']:+.0f}). Top 6 smoke there less.")
L.append(f"- Mountain Range Gearing/Somers under B and C: both places are real clusters (Top 6 {len(mrf[0]['tin'])} and {len(mrf[1]['tin']) if len(mrf) > 1 else 0} flank-line smokes) but the Rest smoke there at nearly the same rate (gaps {', '.join(f'{c_['gap']:+.0f}' for c_ in mrf)} pts, intervals span zero). Not a signature.")
L.append(f"- Sleeping Giant Somers: Top 6 {east(st):.0f}% in columns 7 to 10 vs Rest {east(sr):.0f}% (gap {east(st) - east(sr):+.0f}, {ci_e[0]:+.0f} to {ci_e[1]:+.0f}); in columns 1 to 3, Top 6 {west(st):.0f}% vs Rest {west(sr):.0f}% (gap {west(st) - west(sr):+.0f}, {ci_w[0]:+.0f} to {ci_w[1]:+.0f}). The east lean is confirmed as a half-map split; the tight east-edge spot is lead L{1 + next(i for i, c in enumerate(lead) if c['id'] == 'sg-somers-f9')}.")
L.append(f"- Land of Fire Svea: confirmed. Median distance from smoke edge to the contested cap edge: Top 6 {med(s['edge'] for s in lofs if s['grp'] == 'top') / 1000:.1f} km, Rest {med(s['edge'] for s in lofs if s['grp'] == 'rest') / 1000:.1f} km.")
L.append(f"- PN: {len(pn_in)} of its {len(pn_dd)} destroyer smokes fall in any spot above" + (' (' + ', '.join(f"{s['ship']} in {c['id']}" for s, c in pn_in) + ')' if pn_in else '') + '. Small n.\n')

L.append('## Explicit check: Sleeping Giant, Top 6 Harugumo at G1/F1\n')
L.append(f"{ck['n']} Top 6 smokes in the spot (RESIN 5, H-SR 4, BONKZ 2), median time {mmss(chk['med_el'])}. Figure: `fig/check-sg-harugumo.png`.\n")
L.append(f"- **Is a cruiser inside?** Yes, in {ck['cr_smokes']} of {ck['n']}: {top1(ck['cr_ship'], 4)}. All {ck['cr_radar']} are radar cruisers, sitting a median {ck['cr_dist'] / 1000:.1f} km from the nearest puff. It is not Brisbane here (Brisbane is the east-edge cruiser, spot 6).")
L.append(f"- **Is a second destroyer present?** A position is recorded for one in {ck['dd_n']} of {ck['n']} ({top1(ck['dd_ship'], 3)}). It is forward of the smoke in {ck['dd_fwd']} of {ck['dd_n']}, a median {ck['dd_dist'] / 1000:.1f} km away, most often in {top1(ck['dd_cell'], 3)}: the same west lane, up at cap A. It was inside the smoke itself in {ck['dd_how']['inside']}.")
L.append(f"- **Who was nearest the targets?** {cap1(nt_words(ck))}. So mostly not the Harugumo and not the cruiser beside it: the targets sit north of cap A and north of the central island, and the closest ally is usually a ship outside the smoke.")
L.append(f"- Formation: cruiser inside + second destroyer forward {ck['form'][(True, 'forward')]} of {ck['n']}; cruiser inside, no second destroyer recorded {ck['form'][(True, 'none')]}; cruiser inside, second destroyer behind {ck['form'][(True, 'back')]}; no cruiser inside {ck['n'] - ck['cr_smokes']}.\n")

L.append('## Cast pattern across maps\n')
L.append(f"All destroyer smokes (Top 6 {P['nt']}, Rest {P['nr']}).\n")
L.append(md_table(['Pattern', 'Top 6', 'Rest', 'Gap, pts (95%)', 'Maps where Top 6 is higher'],
                  [[k, f"{v['top']:.0f}%", f"{v['rest']:.0f}%", f"{v['top'] - v['rest']:+.0f} ({v['ci'][0]:+.0f} to {v['ci'][1]:+.0f})", f"{sum(1 for a, b, n in v['maps'].values() if a is not None and b is not None and a > b)} of 7"] for k, v in pat.items()]))
L.append(f"\n- **Yes, one pattern: a radar cruiser inside the destroyer smoke.** {PR['top']:.0f}% vs {PR['rest']:.0f}%. Sleeping Giant is the exception ({PR['maps']['Sleeping Giant'][0]:.0f}% vs {PR['maps']['Sleeping Giant'][1]:.0f}%): the Rest do it there too.")
L.append(f"- 'Radar cruiser inside plus second destroyer forward' is higher for Top 6 on every map ({P['top']:.0f}% vs {P['rest']:.0f}%, {P['ci'][0]:+.0f} to {P['ci'][1]:+.0f}) but it is about one smoke in six, so it is not the typical formation. Inside the signature destroyer spots it is {pct(spot_dd, PATS[HEAD]):.0f}% of {len(spot_dd)}.")
L.append(f"- 'Second destroyer forward' on its own does not separate the groups ({PD['top']:.0f}% vs {PD['rest']:.0f}%, interval touches zero), and part of it is that Top 6 more often still have a second destroyer with a recorded position ({PA['top']:.0f}% vs {PA['rest']:.0f}%).")
L.append('- The Svea spots (1, 2, 4) are a different shape: no cruiser inside; the Svea parks alone and a destroyer works a few km ahead.\n')

L.append('## Method and cautions\n')
L.append(f"- **Search.** Every ship and every habit cluster (flank smoke lines, cap sitters, parked cruiser smoke, moving exhaust) on every map, destroyers and cruisers, with at least 8 Top 6 smokes: {nsub} combinations. Top 6 smoke centres were clustered by mean-shift (Gaussian kernel, {H_KM:.1f} km bandwidth; density peaks within {MERGE_KM:.0f} km merged): {ncl} clusters, most of them one or two smokes. A spot's region is the 2-standard-deviation ellipse of its cluster (each radius at least 1 km). Any ellipse holding at least 8 Top 6 smokes is a candidate: {len(cands)}.")
L.append('- **Test.** Share of the Top 6 smokes of that ship or habit on that map that fall inside the ellipse, minus the same share for the Rest. 95% interval by resampling clans, 1000 times. Kept if at least 8 Top 6 smokes, at least 2 Top 6 clans, the Rest have at least 8 smokes of that subject on the map, and the interval is above zero.')
L.append(f"- **The test flatters the Top 6.** The ellipse is drawn around Top 6 smokes and then used to count them, and clans simply have habits. That is what the placebo measures: {mean(pl_pass):.1f} passes per draw with no real Top 6 in it. With 2 to 4 Top 6 clans behind each spot the clan resampling also has little to work with (the Mountain Range interval of +31 to +40 is narrow only because no Rest smoke is there at all).")
L.append(f"- **Scale matters.** At 1.5 km: {CHK['scales']['1.5']['candidates']} candidates, {CHK['scales']['1.5']['passed']} pass. At 2.5 km: {CHK['scales']['2.5']['candidates']} candidates, {CHK['scales']['2.5']['passed']} pass. Each spot lists how it fares at the other two scales. Spots 1 and 3 only appear at 2 km and wider and are zones 17 to 20 km long, not tight spots.")
L.append('- **Cast positions come from one moment only**: when each smoke was fully laid. Not at activation and not continuously. On top of that, the batch has a position at that moment for only about 4 allied ships per smoke (median), so "no second destroyer recorded" does not mean there was none, and the nearest-ally stand-in picks from the ships that have a position.')
L.append('- **Spotting cannot be attributed from the batch.** "Nearest allied ship to the target" is a stand-in. Median distances of 8 to 9 km mean the nearest ally is often outside destroyer detection range, so treat it as "who was closest", not "who spotted".')
L.append("- **Inside / behind / outside** is the batch's own label for each ally over the smoke's life; line of fire is counted as outside. Distances are to the nearest puff centre at the laid moment.")
L.append('- Concealed damage includes torpedoes launched from smoke. Cap won is counted only on smokes whose contested cap was not already ours. Mountain Range cap A (10 km) is kept.')
L.append('- `ellipse_uv.angle_deg` in `spots.json` is the rotation of the `ru` axis clockwise on screen from the u (east) axis, as used by SVG `rotate`.')
L.append('- Files: `spotlib.py` (search and test), `explore_candidates.py` (scales and placebo, writes `checks.json`), `spots_build.py` + `spots_report.py` (measures, figures, this file, `spots.json`). Figures in `fig/`.')
open(os.path.join(OUT, 'SPOTS.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('wrote SPOTS.md, spots.json', len(recs))
