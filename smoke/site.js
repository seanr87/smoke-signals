(function(){
  document.querySelectorAll('.clip').forEach(function(c){
    var v = c.querySelector('video');
    c.querySelectorAll('button.speed').forEach(function(b){
      b.addEventListener('click', function(){ v.playbackRate = parseFloat(b.dataset.rate); c.querySelectorAll('button.speed').forEach(function(x){x.classList.toggle('on', x===b);}); });
    });
    var first = c.querySelector('button.speed'); if (first) first.classList.add('on');
  });
  function clockText(elapsed){ var m = Math.floor(elapsed/60), s = elapsed%60; return m + ':' + (s<10?'0':'') + s; }
  function fmt(n){ return Math.round(n).toLocaleString(); }

  // Shared horizontal bar panel: rows of {team, v, n, color}; values formatted by a code.
  function fmtVal(v, fmt){
    if (v === null || v === undefined) return '-';
    if (fmt === 'pct') return Math.round(v) + '%';
    if (fmt === 's') return Math.round(v) + ' s';
    if (fmt === 'f1') return v.toFixed(1);
    if (fmt === 'f2') return v.toFixed(2);
    if (fmt === 'pts') return (v >= 0 ? '+' : '') + Math.round(v) + ' pts';
    if (fmt === 'km') return (v/1000).toFixed(1) + ' km';
    return Math.round(v).toLocaleString();
  }
  function panelHtml(title, rows, fmtCode, note){
    var vals = rows.map(function(r){ return r.v; }).filter(function(v){ return v !== null && v !== undefined; });
    var max = Math.max(0, Math.max.apply(null, vals.length ? vals : [0])), min = Math.min(0, Math.min.apply(null, vals.length ? vals : [0]));
    var span = (max - min) || 1, zero = (-min) / span * 100;
    var html = '<h4>' + title + '</h4>';
    rows.forEach(function(r){
      var bar = '';
      if (r.v !== null && r.v !== undefined) {
        var left = r.v >= 0 ? zero : zero + r.v / span * 100, w = Math.abs(r.v) / span * 100;
        bar = '<i style="left:' + left.toFixed(1) + '%;width:' + w.toFixed(1) + '%;background:' + r.color + '"></i>' + (min < 0 ? '<b style="left:' + zero.toFixed(1) + '%"></b>' : '');
      }
      html += '<div class="row' + (r.dim ? ' dim' : '') + '"><span>' + r.team + '</span><span class="bar">' + bar + '</span><span>' + fmtVal(r.v, fmtCode) + (r.n !== undefined ? ' (n=' + r.n + ')' : '') + '</span></div>';
    });
    if (note) html += '<p class="muted small">' + note + '</p>';
    return html;
  }
  function lensKey(prefix){ return document.getElementById(prefix + '-class').value + '|' + document.getElementById(prefix + '-type').value; }
  function noteFor(spec){ return spec.key === 'charge' ? 'n = charges carried' : (spec.key === 'coverage' ? 'n = smokes with a concealed radar ship' : (spec.key === 'offensive' ? 'n = games' : '')); }
  function termHtml(spec){ return spec.def ? '<abbr class="term" title="' + spec.def.replace(/"/g, '&quot;') + '">' + spec.title + '</abbr>' : spec.title; }

  // Clans page: the sortable table (values or percentiles) and the charts for the chosen lens, bars sorted best first.
  function pctShade(p){ return p === null || p === undefined ? '' : ' style="background:rgba(93,173,226,' + (0.05 + 0.55 * p / 100).toFixed(2) + ')"'; }
  if (window.CLAN_METRICS && window.CLAN_SPEC && document.getElementById('clans-class')) {
    var clansSel = ['clans-class', 'clans-type'].map(function(id){ return document.getElementById(id); });
    clansSel[0].value = 'destroyer';
    var allBox = document.getElementById('clans-all');
    var tableSort = {key: 'concealed_per_game', asc: false};
    var tableMode = new URLSearchParams(location.search).get('mode') === 'pct' ? 'pct' : 'values';
    document.querySelectorAll('#clans-mode button').forEach(function(b){ b.classList.toggle('on', b.dataset.mode === tableMode); });
    var renderClans = function(){
      var key = lensKey('clans'), data = window.CLAN_METRICS[key] || {}, pcts = (window.CLAN_PCT || {})[key] || {};
      var total = 0;
      window.CLAN_TEAMS.forEach(function(t){ total += (data[t] && data[t].n) || 0; });
      document.getElementById('clans-count').textContent = total + ' smokes in this lens';
      var small = function(t){ return (window.CLAN_GAMES||{})[t] < (window.CLAN_MIN_GAMES||0); };
      window.CLAN_SPEC.forEach(function(spec){
        var el = document.querySelector('.cchart[data-key="' + spec.key + '"]');
        if (!el) return;
        var rows = window.CLAN_TEAMS.map(function(t){ var m = (data[t] || {})[spec.key] || [null, 0]; return {team: t, v: m[0], n: m[1], color: (window.TEAM_COLORS||{})[t] || '#94A3B8', dim: small(t)}; });
        var known = rows.filter(function(r){ return r.v !== null; }), unknown = rows.filter(function(r){ return r.v === null; });
        known.sort(function(a, b){ return spec.lower ? a.v - b.v : b.v - a.v; });
        var list = known.concat(unknown);
        if (!(allBox && allBox.checked)) list = list.slice(0, 12);
        el.innerHTML = panelHtml(termHtml(spec), list, spec.fmt, noteFor(spec) + (list.length < rows.length ? (noteFor(spec) ? '; ' : '') + 'top ' + list.length + ' of ' + rows.length : ''));
      });
      // The table: one row per clan, sorted by the chosen column's value in both modes.
      var tbody = document.querySelector('#clan-table tbody');
      if (tbody) {
        var rowsT = window.CLAN_TEAMS.map(function(t){ var m = data[t] || {}; return {team: t, m: m, games: m.games || 0, n: m.n || 0, wins: m.wins || 0, losses: m.losses || 0, win_pct: m.win_pct}; });
        var val = function(r){
          if (tableSort.key === 'games') return r.games;
          if (tableSort.key === 'n') return r.n;
          if (tableSort.key === 'wins') return r.wins + (r.win_pct || 0) / 1000;
          if (tableSort.key === 'win_pct') return r.win_pct === null || r.win_pct === undefined ? (tableSort.asc ? Infinity : -Infinity) : r.win_pct;
          var x = (r.m[tableSort.key] || [null])[0]; return x === null || x === undefined ? (tableSort.asc ? Infinity : -Infinity) : x;
        };
        rowsT.sort(function(a, b){ return tableSort.asc ? val(a) - val(b) : val(b) - val(a); });
        var base = window.CLAN_BASE || 0;
        tbody.innerHTML = rowsT.map(function(r){
          var cells = '<td><a href="' + (window.CLAN_HREF||{})[r.team] + '"><span class="tag" style="--c:' + ((window.TEAM_COLORS||{})[r.team]||'#94A3B8') + '">' + r.team + '</span></a>' + (small(r.team) ? ' <span class="pill warn-pill" title="fewer than ' + window.CLAN_MIN_GAMES + ' games: ranked against the ' + base + ' clans with enough games">small sample</span>' : '') + '</td>'
            + '<td>' + r.games + '</td><td>' + r.wins + '-' + r.losses + '</td><td>' + (r.win_pct === null || r.win_pct === undefined ? '-' : Math.round(r.win_pct) + '%') + '</td><td>' + r.n + '</td>';
          window.CLAN_SPEC.forEach(function(spec){
            var m = r.m[spec.key] || [null, 0], p = (pcts[r.team] || {})[spec.key];
            var pTxt = p === null || p === undefined ? '-' : String(Math.round(p));
            var vTxt = fmtVal(m[0], spec.fmt) + ' (n=' + m[1] + ')';
            if (tableMode === 'pct') cells += '<td class="pcell"' + pctShade(p) + ' title="' + vTxt.replace(/"/g, '&quot;') + '">' + pTxt + '</td>';
            else cells += '<td class="pcell"' + pctShade(p) + ' title="percentile ' + pTxt + ' among ' + base + ' clans with ' + window.CLAN_MIN_GAMES + '+ games">' + fmtVal(m[0], spec.fmt) + ' <span class="n">(' + m[1] + ')</span></td>';
          });
          return '<tr class="' + (small(r.team) ? 'small-sample' : '') + '">' + cells + '</tr>';
        }).join('');
      }
    };
    clansSel.forEach(function(s){ s.addEventListener('change', renderClans); });
    if (allBox) allBox.addEventListener('change', renderClans);
    document.querySelectorAll('#clans-mode button').forEach(function(b){ b.addEventListener('click', function(){ tableMode = b.dataset.mode; document.querySelectorAll('#clans-mode button').forEach(function(x){ x.classList.toggle('on', x === b); }); renderClans(); }); });
    document.querySelectorAll('#clan-table th[data-key]').forEach(function(th){
      th.addEventListener('click', function(){ if (tableSort.key === th.dataset.key) tableSort.asc = !tableSort.asc; else { tableSort.key = th.dataset.key; tableSort.asc = th.dataset.key === 'deaths'; } renderClans(); });
    });
    renderClans();
  }

  // Players leaderboard: clan filter and the minimum-smokes toggle.
  var ptable = document.getElementById('players');
  if (ptable && document.getElementById('p-clan')) {
    var prows = Array.from(ptable.querySelectorAll('tbody tr'));
    var prender = function(){
      var c = document.getElementById('p-clan').value, min = document.getElementById('p-min').checked, n = 0;
      prows.forEach(function(r){ var ok = (!c || r.dataset.team === c) && (!min || parseInt(r.dataset.smokes, 10) >= 5); r.hidden = !ok; if (ok) n++; });
      document.getElementById('p-count').textContent = n + ' of ' + prows.length + ' players';
    };
    ['p-clan', 'p-min'].forEach(function(id){ document.getElementById(id).addEventListener('change', prender); });
    prender();
  }

  // Clan page: the stat tiles and the tendency strip for the chosen lens.
  if (window.CLAN_METRICS && window.CLAN_TEAM && document.getElementById('clan-class')) {
    var leadKeys = ['uptime', 'swing', 'punished'];
    var tile = function(spec, m){
      return '<div class="stat" style="--c:' + ((window.TEAM_COLORS||{})[window.CLAN_TEAM] || '#94A3B8') + '"><b>' + fmtVal(m[0], spec.fmt) + '</b><span>' + termHtml(spec) + ' (n = ' + m[1] + ')</span></div>';
    };
    var specOf = {}; window.CLAN_SPEC.forEach(function(s){ specOf[s.key] = s; });
    var renderClan = function(){
      var key = lensKey('clan');
      var data = (window.CLAN_METRICS[key] || {})[window.CLAN_TEAM] || {};
      var leadHtml = '', moreHtml = '';
      window.CLAN_SPEC.forEach(function(spec){ var m = data[spec.key] || [null, 0]; if (leadKeys.indexOf(spec.key) >= 0) leadHtml += tile(spec, m); else moreHtml += tile(spec, m); });
      document.getElementById('clan-lead').innerHTML = leadHtml;
      document.getElementById('clan-more').innerHTML = moreHtml + '<div class="stat"><b>' + (data.n || 0) + '</b><span>smokes in this lens (' + (data.games || 0) + ' games)</span></div>';
      var strip = document.getElementById('clan-tendency'), pcts = (window.CLAN_PCT || {})[key] || {};
      if (strip) {
        strip.innerHTML = (window.CLAN_TENDENCY || []).map(function(t){
          var p = pcts[t[0]], m = data[t[0]] || [null, 0], spec = specOf[t[0]] || {fmt: 'int'};
          var word = p === null || p === undefined ? '' : (p >= 80 ? t[2] : (p <= 20 ? t[3] : ''));
          var pTxt = p === null || p === undefined ? '-' : Math.round(p);
          return '<div class="tcell"' + pctShade(p) + ' title="' + fmtVal(m[0], spec.fmt).replace(/"/g, '&quot;') + ' (n=' + m[1] + ')"><b>' + pTxt + '</b><span>' + t[1] + '</span>' + (word ? '<em>' + word + '</em>' : '<em class="none">&nbsp;</em>') + '</div>';
        }).join('');
      }
    };
    document.getElementById('clan-class').value = 'destroyer';
    ['clan-class', 'clan-type'].forEach(function(id){ document.getElementById(id).addEventListener('change', renderClan); });
    renderClan();
  }

  // Award lens toggles (Home, Players).
  document.querySelectorAll('.lens-toggle').forEach(function(bar){
    bar.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click', function(){
        bar.querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x === b); });
        var el = bar.nextElementSibling;
        while (el && el.classList.contains('lens-set')) { el.hidden = el.dataset.lens !== b.dataset.lens; el = el.nextElementSibling; }
      });
    });
  });

  // Player page: lens over the cards and the damage chart.
  if (window.PLAYER_SMOKES && document.getElementById('player-class')) {
    var renderPlayer = function(){
      var cls = document.getElementById('player-class').value, typ = document.getElementById('player-type').value, n = 0;
      document.querySelectorAll('#player-cards .smoke-card').forEach(function(c){ var ok = (cls === 'all' || c.dataset.cls === cls) && (typ === 'all' || c.dataset.type === typ); c.hidden = !ok; if (ok) n++; });
      var rows = window.PLAYER_SMOKES.filter(function(r){ return (cls === 'all' || r.cls === cls) && (typ === 'all' || r.type === typ); }).slice(0, 12);
      var max = Math.max(1, Math.max.apply(null, rows.map(function(r){ return r.v; }).concat([0])));
      var html = '<h4>Damage per smoke, top 12 of ' + n + ' shown; click a bar to open the smoke</h4>';
      rows.forEach(function(r){ html += '<a class="row wide" href="' + r.href + '"><span title="' + r.label.replace(/"/g, '&quot;') + '">' + r.label + '</span><span class="bar"><i style="left:0;width:' + (r.v / max * 100).toFixed(1) + '%;background:' + r.color + '"></i></span><span>' + Math.round(r.v).toLocaleString() + '</span></a>'; });
      document.getElementById('player-chart').innerHTML = rows.length ? html : '<p class="muted small">Nothing here, just clear skies.</p>';
      document.getElementById('player-count').textContent = n + ' smokes shown';
    };
    ['player-class', 'player-type'].forEach(function(id){ document.getElementById(id).addEventListener('change', renderPlayer); });
    renderPlayer();
  }

  // Maps page: zone overlay toggle.
  var zonesBox = document.getElementById('showzones');
  if (zonesBox) {
    var applyZones = function(){ document.querySelectorAll('.mapwrap').forEach(function(m){ m.classList.toggle('showzones', zonesBox.checked); }); };
    zonesBox.addEventListener('change', applyZones);
    if (location.hash.indexOf('zones') >= 0 || new URLSearchParams(location.search).get('zones')) { zonesBox.checked = true; applyZones(); }
  }

  // Multi-select: a button that opens a searchable checkbox list. Empty selection means all.
  function makeMulti(el, options, onChange){
    var selected = [];
    el.innerHTML = '<button type="button" class="msel-btn">all</button><div class="msel-pop" hidden><input class="msel-search" placeholder="search"><div class="msel-acts"><a class="msel-clear">clear</a><a class="msel-close">close</a></div><div class="msel-list"></div></div>';
    var btn = el.querySelector('.msel-btn'), pop = el.querySelector('.msel-pop'), list = el.querySelector('.msel-list'), search = el.querySelector('.msel-search');
    list.innerHTML = options.map(function(o){ return '<label data-v="' + escA(o.value) + '"><input type="checkbox" value="' + escA(o.value) + '"> <span>' + escA(o.label) + '</span>' + (o.count !== undefined ? '<span class="n">' + o.count + '</span>' : '') + '</label>'; }).join('');
    function label(){ if (!selected.length) return 'all'; var names = selected.slice(0, 3).join(', '); return selected.length > 3 ? names + ' +' + (selected.length - 3) : names; }
    function sync(){ btn.textContent = label(); btn.classList.toggle('on', selected.length > 0); list.querySelectorAll('input').forEach(function(i){ i.checked = selected.indexOf(i.value) >= 0; }); }
    list.addEventListener('change', function(){ selected = Array.from(list.querySelectorAll('input:checked')).map(function(i){ return i.value; }); sync(); onChange(); });
    search.addEventListener('input', function(){ var q = search.value.toLowerCase(); list.querySelectorAll('label').forEach(function(l){ l.classList.toggle('hide', q && l.dataset.v.toLowerCase().indexOf(q) < 0); }); });
    btn.addEventListener('click', function(e){ e.preventDefault(); pop.hidden = !pop.hidden; if (!pop.hidden) search.focus(); });
    el.querySelector('.msel-clear').addEventListener('click', function(){ selected = []; sync(); onChange(); });
    el.querySelector('.msel-close').addEventListener('click', function(){ pop.hidden = true; });
    document.addEventListener('click', function(e){ if (!el.contains(e.target)) pop.hidden = true; });
    sync();
    return { get: function(){ return selected.slice(); }, set: function(vals){ selected = (vals || []).filter(function(v){ return options.some(function(o){ return o.value === v; }); }); sync(); } };
  }
  function escA(t){ return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function listParam(q, name){ var v = q.get(name); return v ? v.split(',').map(function(x){ return x.trim(); }).filter(Boolean) : []; }

  // Maps page: one filter bar for every map; a density of origins, or the smokes themselves when few remain.
  var mapsBar = document.getElementById('maps-filters');
  if (mapsBar) {
    var wantedSlug = location.hash.indexOf('#smoke-') === 0 ? location.hash.slice(7) : '';
    var opts = window.MAPS_OPTS || {clans: [], ships: []};
    var mMap = document.getElementById('m-map'), mPlayer = document.getElementById('m-player'), mPurpose = document.getElementById('m-purpose'), mSpawn = document.getElementById('m-spawn'), mCls = document.getElementById('m-cls'), mType = document.getElementById('m-type');
    var lo = document.getElementById('m-lo'), hi = document.getElementById('m-hi'), mCount = document.getElementById('m-count');
    var DRAW_MAX = window.MAP_DRAW_MAX || 25, N = 768;
    var mClan = makeMulti(document.getElementById('m-clan'), opts.clans.map(function(c){ return {value: c[0], label: c[0], count: c[1]}; }), renderAll);
    var mShip = makeMulti(document.getElementById('m-ship'), opts.ships.map(function(c){ return {value: c[0], label: c[0], count: c[1]}; }), renderAll);
    var slugId = function(t){ return String(t).replace(/[^A-Za-z0-9_-]+/g, '_').replace(/^_+|_+$/g, '') || 'x'; };
    function view(){ var r = document.querySelector('input[name=m-view]:checked'); return r ? r.value : 'auto'; }
    function setView(v){ var r = document.querySelector('input[name=m-view][value="' + v + '"]'); if (r) r.checked = true; }
    function shown(r){
      var t = r.t;
      if (t >= 0 && (t < parseInt(lo.value,10) * 60 || t >= parseInt(hi.value,10) * 60 + (parseInt(hi.value,10) === 20 ? 1 : 0))) return false;
      var clans = mClan.get(), ships = mShip.get();
      if (clans.length && clans.indexOf(r.team) < 0) return false;
      if (ships.length && ships.indexOf(r.ship) < 0) return false;
      if (mPlayer.value && r.player !== mPlayer.value) return false;
      if (mPurpose.value && r.purposes.indexOf(mPurpose.value) < 0) return false;
      if (mSpawn.value && r.spawn !== mSpawn.value) return false;
      if (mCls.value && r.cls !== mCls.value) return false;
      if (mType.value && r.type !== mType.value) return false;
      return true;
    }
    function heatRects(rows){
      var cells = {}, peak = 0, step = N / 10;
      rows.forEach(function(r){ var p = r.pts[0]; var cx = Math.min(9, Math.max(0, Math.floor(p[0] / step))), cy = Math.min(9, Math.max(0, Math.floor(p[1] / step))); var k = cx + ',' + cy; cells[k] = (cells[k] || 0) + 1; if (cells[k] > peak) peak = cells[k]; });
      var letters = 'ABCDEFGHIJ';
      return Object.keys(cells).map(function(k){ var cx = parseInt(k.split(',')[0], 10), cy = parseInt(k.split(',')[1], 10), n = cells[k]; return '<rect x="' + (cx * step) + '" y="' + (cy * step) + '" width="' + step + '" height="' + step + '" fill="#F5C542" fill-opacity="' + (0.12 + 0.68 * n / peak).toFixed(2) + '"><title>' + letters[cy] + (cx + 1) + ': ' + n + ' smokes</title></rect>'; }).join('');
    }
    function smokeMarkup(r, markerPrefix){
      var pts = r.pts.map(function(p){ return p[0] + ',' + p[1]; }).join(' ');
      var color = (window.TEAM_COLORS||{})[r.team] || '#94A3B8';
      var cloud = r.r > 0 ? '<polyline class="cloud" points="' + pts + '" stroke="' + color + '" style="stroke-width:' + (2 * r.r).toFixed(1) + 'px"/>' : '';
      return '<a href="' + r.href + '" id="smoke-' + r.slug + '" class="smokepath" data-team="' + escA(r.team) + '">' + cloud + '<polyline points="' + pts + '" stroke="' + color + '"' + (r.dashed ? ' stroke-dasharray="6,4"' : '') + ' marker-end="url(#' + markerPrefix + '-arrow-' + slugId(r.team) + ')"/><title>' + escA(r.title) + '</title></a>';
    }
    function panel(title, rows, unit, pct){
      var vals = rows.map(function(r){ return r.v; }).filter(function(v){ return v !== null; });
      var max = Math.max(0, Math.max.apply(null, vals.length ? vals : [0])), min = Math.min(0, Math.min.apply(null, vals.length ? vals : [0]));
      var span = (max - min) || 1, zero = (-min) / span * 100;
      var html = '<h4>' + title + '</h4>';
      rows.forEach(function(r){
        var bar = '';
        if (r.v !== null) {
          var left = r.v >= 0 ? zero : zero + r.v / span * 100, w = Math.abs(r.v) / span * 100;
          bar = '<i style="left:' + left.toFixed(1) + '%;width:' + w.toFixed(1) + '%;background:' + r.color + '"></i>' + (min < 0 ? '<b style="left:' + zero.toFixed(1) + '%"></b>' : '');
        }
        var text = r.v === null ? '-' : (pct ? Math.round(r.v) + '%' : (unit === 'km' ? (r.v/1000).toFixed(1) + ' km' : fmt(r.v)));
        html += '<div class="row' + (r.n < 5 ? ' dim' : '') + '"><span>' + r.team + '</span><span class="bar">' + bar + '</span><span>' + text + ' (n=' + r.n + ')</span></div>';
      });
      return '<div class="panel">' + html + '</div>';
    }
    function donut(counts){
      var names = Object.keys(counts).sort(function(a,b){ return counts[b] - counts[a]; });
      var total = names.reduce(function(a,n){ return a + counts[n]; }, 0);
      if (!total) return '<span class="muted small">Nothing here, just clear skies.</span>';
      var size = 120, cx = 60, cy = 60, r = 58, angle = -Math.PI/2, svg = '', legend = '';
      names.forEach(function(n){
        var frac = counts[n]/total, a2 = angle + frac*2*Math.PI, color = (window.SHIP_COLORS||{})[n] || '#94A3B8';
        if (frac >= 0.999) svg += '<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="'+color+'"><title>'+n+': '+counts[n]+'</title></circle>';
        else svg += '<path d="M'+cx+','+cy+' L'+(cx+r*Math.cos(angle)).toFixed(1)+','+(cy+r*Math.sin(angle)).toFixed(1)+' A'+r+','+r+' 0 '+(frac>0.5?1:0)+',1 '+(cx+r*Math.cos(a2)).toFixed(1)+','+(cy+r*Math.sin(a2)).toFixed(1)+' Z" fill="'+color+'"><title>'+n+': '+counts[n]+' ('+Math.round(frac*100)+'%)</title></path>';
        legend += '<span class="legend"><i style="background:'+color+'"></i>'+n+' '+counts[n]+'</span>';
        angle = a2;
      });
      svg += '<circle cx="'+cx+'" cy="'+cy+'" r="'+(r*0.6)+'" fill="var(--panel)"/>';
      return '<svg viewBox="0 0 '+size+' '+size+'" width="'+size+'" height="'+size+'" class="donut">'+svg+'</svg><div class="legend-row">'+legend+'</div>';
    }
    var sections = Array.from(document.querySelectorAll('.map-section')).map(function(sec){
      var wrap = sec.querySelector('.mapwrap'), svg = wrap ? wrap.querySelector('svg') : null;
      var marker = svg ? svg.querySelector('marker') : null;
      return { el: sec, map: sec.dataset.map, url: sec.dataset.paths, rows: null, wrap: wrap, heat: svg ? svg.querySelector('g.heat') : null, paths: svg ? svg.querySelector('g.paths') : null,
        markerPrefix: marker ? marker.id.replace(/-arrow-.*$/, '') : 'm', chart: sec.querySelector('.chart'), count: sec.querySelector('.count'), ships: sec.querySelector('.ships') };
    });
    function renderSection(s){
      var hidden = !!(mMap.value && mMap.value !== s.map);
      s.el.hidden = hidden;
      if (hidden || !s.rows) return 0;
      var vis = s.rows.filter(shown);
      var v = view(), drawn = v === 'smokes' || (v === 'auto' && vis.length <= DRAW_MAX);
      if (s.wrap) s.wrap.classList.toggle('lines', drawn);
      if (drawn) { s.paths.innerHTML = vis.map(function(r){ return smokeMarkup(r, s.markerPrefix); }).join(''); s.heat.innerHTML = ''; }
      else { s.heat.innerHTML = heatRects(vis); s.paths.innerHTML = ''; }
      s.count.textContent = vis.length + ' smokes ' + (drawn ? 'drawn' : 'in the density') + (v === 'auto' && !drawn ? ' (narrow to ' + DRAW_MAX + ' or fewer to draw them)' : '');
      var teams = Array.from(new Set(s.rows.map(function(r){ return r.team; })));
      if (mClan.get().length) teams = teams.filter(function(t){ return mClan.get().indexOf(t) >= 0; });
      var counts0 = {}; vis.forEach(function(r){ counts0[r.team] = (counts0[r.team]||0) + 1; });
      teams.sort(function(a,b){ return (counts0[b]||0) - (counts0[a]||0) || a.localeCompare(b); });
      var others = [];
      if (!mClan.get().length && teams.length > 10) { others = teams.slice(10); teams = teams.slice(0, 10); }
      function rows(f){
        var out = teams.map(function(t){ var list = vis.filter(function(r){ return r.team === t; }); return {team:t, v:f(list), n:list.length, color:(window.TEAM_COLORS||{})[t]||'#94A3B8'}; });
        if (others.length) { var list = vis.filter(function(r){ return others.indexOf(r.team) >= 0; }); out.push({team:'others (' + others.length + ')', v:f(list), n:list.length, color:'#475569'}); }
        return out;
      }
      function avg(list, key){ var xs = list.map(function(r){ return r[key]; }).filter(function(x){ return x !== null && x !== undefined; }).map(Number); return xs.length ? xs.reduce(function(a,b){return a+b;},0)/xs.length : null; }
      s.chart.innerHTML =
        panel('Smokes', rows(function(l){ return l.length ? l.length : null; }), '', false) +
        panel('Average smoke damage', rows(function(l){ return avg(l, 'dmg'); }), '', false) +
        panel('<abbr class="term" title="' + (window.CONTEST_DEF||'') + '">Average distance to the nearest contested cap</abbr> (negative = inside)', rows(function(l){ return avg(l, 'contested'); }), 'km', false) +
        panel('<abbr class="term" title="' + (window.SELFISH_DEF||'') + '">Selfish smoke</abbr> share', rows(function(l){ var v = avg(l, 'selfish'); return v === null ? null : v * 100; }), '', true);
      if (s.ships) { var counts = {}; vis.forEach(function(r){ counts[r.ship] = (counts[r.ship]||0) + 1; }); s.ships.innerHTML = donut(counts); }
      return vis.length;
    }
    function writeUrl(){
      var q = new URLSearchParams();
      if (mMap.value) q.set('map', mMap.value);
      if (mClan.get().length) q.set('clan', mClan.get().join(','));
      if (mShip.get().length) q.set('ship', mShip.get().join(','));
      if (mPlayer.value) q.set('player', mPlayer.value);
      if (mPurpose.value) q.set('purpose', mPurpose.value);
      if (mSpawn.value) q.set('spawn', mSpawn.value);
      if (mCls.value) q.set('cls', mCls.value);
      if (mType.value) q.set('type', mType.value);
      if (lo.value !== '0' || hi.value !== '20') q.set('t', lo.value + '-' + hi.value);
      if (view() !== 'auto') q.set('view', view());
      var s = q.toString().replace(/%2C/g, ',');
      history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + (wantedSlug ? '#smoke-' + wantedSlug : ''));
    }
    function renderAll(){
      document.querySelector('#maps-filters .lo').textContent = clockText(parseInt(lo.value,10) * 60);
      document.querySelector('#maps-filters .hi').textContent = clockText(parseInt(hi.value,10) * 60);
      var total = 0, all = 0;
      sections.forEach(function(s){ total += renderSection(s); if (!s.el.hidden && s.rows) all += s.rows.length; });
      mCount.textContent = total + ' of ' + all + ' smokes';
      writeUrl();
    }
    function clamp(){ if (parseInt(lo.value,10) > parseInt(hi.value,10)) { if (document.activeElement === lo) hi.value = lo.value; else lo.value = hi.value; } }
    [lo, hi].forEach(function(r){ r.addEventListener('input', function(){ clamp(); renderAll(); }); });
    [mMap, mPlayer, mPurpose, mSpawn, mCls, mType].forEach(function(s){ s.addEventListener('change', renderAll); });
    document.querySelectorAll('input[name=m-view]').forEach(function(r){ r.addEventListener('change', renderAll); });
    // Filters from the address bar: ?map=...&clan=A,B&ship=X,Y&player=...&purpose=...&spawn=...&cls=...&type=...&t=0-4&view=smokes (older links: from/to in seconds).
    var q = new URLSearchParams(location.search);
    if (q.get('map')) mMap.value = q.get('map');
    mClan.set(listParam(q, 'clan'));
    mShip.set(listParam(q, 'ship'));
    if (q.get('player')) mPlayer.value = q.get('player');
    if (q.get('purpose')) mPurpose.value = q.get('purpose');
    if (q.get('spawn')) mSpawn.value = q.get('spawn');
    if (q.get('cls')) mCls.value = q.get('cls');
    if (q.get('type')) mType.value = q.get('type');
    if (q.get('t') && /^\d+-\d+$/.test(q.get('t'))) { lo.value = q.get('t').split('-')[0]; hi.value = q.get('t').split('-')[1]; }
    if (q.get('from')) lo.value = Math.floor(parseInt(q.get('from'),10) / 60);
    if (q.get('to')) hi.value = Math.ceil(parseInt(q.get('to'),10) / 60);
    if (q.get('view')) setView(q.get('view'));
    // A smoke page's "its path on the map" link: that smoke's map and clan, drawn, and scrolled to.
    var target = wantedSlug && (window.SMOKE_MAP||{})[wantedSlug];
    if (target) { mMap.value = target[0]; mClan.set([target[1]]); setView('smokes'); }
    clamp();
    Promise.all(sections.map(function(s){ return fetch(s.url).then(function(r){ return r.json(); }).then(function(rows){ s.rows = rows; }).catch(function(){ s.rows = []; s.count.textContent = 'paths could not be loaded'; }); })).then(function(){
      renderAll();
      if (target) { var el = document.getElementById('smoke-' + wantedSlug); if (el) { el.querySelectorAll('polyline:not(.cloud)').forEach(function(p){ p.style.strokeWidth = '7px'; }); el.scrollIntoView({block: 'center'}); } }
    });
  }

  // Games page: group stage filters.
  var gtable = document.getElementById('games');
  if (gtable && document.getElementById('g-clan')) {
    var grows = Array.from(gtable.querySelectorAll('tbody tr'));
    function grender(){
      var c = document.getElementById('g-clan').value, m = document.getElementById('g-map').value, n = 0;
      grows.forEach(function(r){ var ok = (!c || r.dataset.clan.split(';').indexOf(c) >= 0) && (!m || r.dataset.map === m); r.hidden = !ok; if (ok) n++; });
      document.getElementById('g-count').textContent = n + ' of ' + grows.length + ' games';
      document.getElementById('g-empty').hidden = n > 0;
    }
    ['g-clan','g-map'].forEach(function(id){ document.getElementById(id).addEventListener('change', grender); });
    grender();
  }

  // Players leaderboard: click a heading to sort.
  document.querySelectorAll('table.sortable').forEach(function(t){
    var tbody = t.querySelector('tbody');
    t.querySelectorAll('th[data-key]').forEach(function(th){
      th.addEventListener('click', function(){
        var key = th.dataset.key, asc = th.dataset.asc === '1';
        var rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort(function(a,b){ var x = parseFloat(a.dataset[key]||0), y = parseFloat(b.dataset[key]||0); return asc ? x - y : y - x; });
        rows.forEach(function(r){ tbody.appendChild(r); });
        th.dataset.asc = asc ? '0' : '1';
      });
    });
  });

  if (!window.SMOKES_URL) return;
  var rows = [], tbody = document.querySelector('#smokes tbody'), PAGE = 100, limit = PAGE;
  var more = document.getElementById('showmore');
  var multi = {};
  more.addEventListener('click', function(){ limit += PAGE; render(); });
  fetch(window.SMOKES_URL).then(function(r){ return r.json(); }).then(function(data){ rows = data; start(); }).catch(function(){ document.getElementById('count').textContent = 'the smoke table could not be loaded'; });
  function start(){
  function fill(id, key){ var sel = document.getElementById(id); var vals = Array.from(new Set(rows.map(function(r){return r[key];}))).filter(Boolean).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', function(){ limit = PAGE; render(); }); }
  function fillMulti(id, key){ var counts = {}; rows.forEach(function(r){ if (r[key]) counts[r[key]] = (counts[r[key]]||0) + 1; }); var vals = Object.keys(counts).sort(); multi[key] = makeMulti(document.getElementById(id), vals.map(function(v){ return {value: v, label: v, count: counts[v]}; }), function(){ limit = PAGE; render(); }); }
  fillMulti('f-team','team'); fill('f-player','player'); fillMulti('f-ship','ship'); fill('f-map','map'); fill('f-game','game'); fill('f-type','type'); fill('f-phase','phase');
  fill('f-cls','cls'); fill('f-movement','movement'); fill('f-coverage','coverage'); fill('f-primary','primary'); fill('f-zone','zone'); fill('f-lane','lane');
  (function(){ var sel = document.getElementById('f-purpose'); var vals = Array.from(new Set(rows.flatMap(function(r){ return r.purposes; }))).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', function(){ limit = PAGE; render(); }); })();
  document.getElementById('f-sort').addEventListener('change', function(){ limit = PAGE; render(); });
  // Filters from the address bar: ?clan=A,B&ship=X,Y plus any single select by its name (player, map, game, type, cls, ...); 'team' is the older name of 'clan'.
  var q = new URLSearchParams(location.search);
  multi.team.set(listParam(q, 'clan').concat(listParam(q, 'team')));
  multi.ship.set(listParam(q, 'ship'));
  SINGLE.forEach(function(k){ if (q.get(k)) document.getElementById('f-' + k).value = q.get(k); });
  if (q.get('purpose')) document.getElementById('f-purpose').value = q.get('purpose');
  if (q.get('sort')) document.getElementById('f-sort').value = q.get('sort');
  render();
  }
  var SINGLE = ['player','map','game','type','phase','cls','movement','coverage','primary','zone','lane'];
  function val(id){ return document.getElementById(id).value; }
  function bar(v, max, color){ var w = max ? Math.max(0, Math.min(1, v/max))*80 : 0; return '<span class="mini"><i style="width:'+w.toFixed(0)+'px;background:'+color+'"></i></span>'; }
  function writeUrl(f, purpose, sort){
    var q = new URLSearchParams();
    if (multi.team.get().length) q.set('clan', multi.team.get().join(','));
    if (multi.ship.get().length) q.set('ship', multi.ship.get().join(','));
    SINGLE.forEach(function(k){ if (f[k]) q.set(k, f[k]); });
    if (purpose) q.set('purpose', purpose);
    if (sort !== 'total') q.set('sort', sort);
    var s = q.toString().replace(/%2C/g, ',');
    history.replaceState(null, '', location.pathname + (s ? '?' + s : ''));
  }
  function render(){
    var f = {};
    SINGLE.forEach(function(k){ f[k] = val('f-' + k); });
    var clans = multi.team.get(), ships = multi.ship.get();
    var purpose = val('f-purpose');
    var sort = val('f-sort'), asc = sort==='contested' || sort==='elapsed';
    var list = rows.filter(function(r){ return Object.keys(f).every(function(k){ return !f[k] || r[k]===f[k]; }) && (!clans.length || clans.indexOf(r.team) >= 0) && (!ships.length || ships.indexOf(r.ship) >= 0) && (!purpose || r.purposes.indexOf(purpose) >= 0); });
    list.sort(function(a,b){ var x=a[sort], y=b[sort]; if (x==null) x = asc? Infinity : -Infinity; if (y==null) y = asc? Infinity : -Infinity; return asc ? x-y : y-x; });
    var shownRows = list.slice(0, limit);
    more.hidden = list.length <= limit;
    more.textContent = 'Show ' + Math.min(PAGE, list.length - limit) + ' more (' + shownRows.length + ' of ' + list.length + ' shown)';
    tbody.innerHTML = shownRows.map(function(r){
      var con = r.contested==null ? '-' : (r.contested<0 ? Math.round(r.depth)+'% into '+r.contested_name : (r.contested/1000).toFixed(1)+' km to '+r.contested_name);
      var outcome = r.won ? 'near capture of '+r.won : (r.defended ? 'defended '+r.defended : '-');
      var marks = (r.one_sided ? ' <span class="pill warn-pill" title="one replay for this game: inferred smoke, no damage counted">one-sided</span>' : '') + (r.quality ? ' <span class="pill warn-pill" title="' + r.quality.replace(/"/g, '&quot;') + '">drift</span>' : '');
      var thumb = r.thumb ? '<img class="thumb" loading="lazy" width="84" height="84" src="' + r.thumb + '" alt="">' : '';
      return '<tr data-href="'+r.href+'"><td>'+thumb+'</td>'+
        '<td><span class="tag" style="--c:'+r.color+'">'+r.team+'</span></td><td>'+r.player+marks+'</td><td>'+r.ship+'</td><td>'+r.map+'</td>'+
        '<td class="small" title="'+r.game.replace(/"/g,'&quot;')+'">'+r.game_short+'</td><td>'+(r.elapsed!=null?clockText(r.elapsed):'?')+'</td>'+
        '<td class="small tagcell" title="'+r.tags_text.replace(/"/g,'&quot;')+'"><span class="pill cls">'+r.cls_short+'</span> <span class="pill">'+r.movement+'</span> <span class="pill">'+r.coverage+'</span><br>'+(r.primary==='none'?'<span class="muted">no tactic</span>':'<b>'+r.primary+'</b>')+(r.purposes.length>1?' <span class="muted">+'+(r.purposes.length-1)+'</span>':'')+'</td>'+
        '<td class="small">'+(r.zone||'-')+'<br><span class="muted">'+(r.lane?r.lane+' lane':'')+'</span></td>'+
        '<td>'+r.total.toLocaleString()+' '+bar(r.total, window.MAX_TOTAL, '#F5C542')+'<br><span class="muted small">'+r.concealed.toLocaleString()+' / '+r.detected.toLocaleString()+'</span></td>'+
        '<td>'+r.dd.toLocaleString()+'</td>'+
        '<td>'+con+'</td><td>'+outcome+'</td><td>'+r.radar+'</td><td>'+r.offensive+'</td><td>'+r.kills+'</td><td>'+r.deaths+'</td><td>'+(r.selfish?'yes':'no')+'</td></tr>';
    }).join('');
    Array.from(tbody.querySelectorAll('tr[data-href]')).forEach(function(tr){ tr.addEventListener('click', function(){ location.href = tr.dataset.href; }); });
    document.getElementById('empty').hidden = list.length>0;
    document.getElementById('count').textContent = list.length + ' of ' + rows.length + ' smokes';
    writeUrl(f, purpose, sort);
  }
})();