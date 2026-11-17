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

  // Clans page: charts for the chosen lens, bars sorted best first.
  if (window.CLAN_METRICS && window.CLAN_SPEC && document.getElementById('clans-class')) {
    var clansSel = ['clans-class', 'clans-type'].map(function(id){ return document.getElementById(id); });
    clansSel[0].value = 'destroyer';
    var renderClans = function(){
      var key = lensKey('clans'), data = window.CLAN_METRICS[key] || {};
      var total = 0;
      window.CLAN_TEAMS.forEach(function(t){ total += (data[t] && data[t].n) || 0; });
      document.getElementById('clans-count').textContent = total + ' smokes in this lens';
      window.CLAN_SPEC.forEach(function(spec){
        var el = document.querySelector('.cchart[data-key="' + spec.key + '"]');
        if (!el) return;
        var rows = window.CLAN_TEAMS.map(function(t){ var m = (data[t] || {})[spec.key] || [null, 0]; return {team: t, v: m[0], n: m[1], color: (window.TEAM_COLORS||{})[t] || '#94A3B8'}; });
        var known = rows.filter(function(r){ return r.v !== null; }), unknown = rows.filter(function(r){ return r.v === null; });
        known.sort(function(a, b){ return spec.lower ? a.v - b.v : b.v - a.v; });
        el.innerHTML = panelHtml(termHtml(spec), known.concat(unknown), spec.fmt, noteFor(spec));
      });
    };
    clansSel.forEach(function(s){ s.addEventListener('change', renderClans); });
    renderClans();
  }

  // Clan page: the stat tiles for the chosen lens.
  if (window.CLAN_METRICS && window.CLAN_TEAM && document.getElementById('clan-class')) {
    var leadKeys = ['uptime', 'swing', 'punished'];
    var tile = function(spec, m){
      return '<div class="stat" style="--c:' + ((window.TEAM_COLORS||{})[window.CLAN_TEAM] || '#94A3B8') + '"><b>' + fmtVal(m[0], spec.fmt) + '</b><span>' + termHtml(spec) + ' (n = ' + m[1] + ')</span></div>';
    };
    var renderClan = function(){
      var data = (window.CLAN_METRICS[lensKey('clan')] || {})[window.CLAN_TEAM] || {};
      var leadHtml = '', moreHtml = '';
      window.CLAN_SPEC.forEach(function(spec){ var m = data[spec.key] || [null, 0]; if (leadKeys.indexOf(spec.key) >= 0) leadHtml += tile(spec, m); else moreHtml += tile(spec, m); });
      document.getElementById('clan-lead').innerHTML = leadHtml;
      document.getElementById('clan-more').innerHTML = moreHtml + '<div class="stat"><b>' + (data.n || 0) + '</b><span>smokes in this lens (' + (data.games || 0) + ' games)</span></div>';
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

  // Maps page: filters per map section and four by-clan charts of the smokes shown.
  document.querySelectorAll('.map-section').forEach(function(sec){
    var paths = Array.from(sec.querySelectorAll('a.smokepath'));
    var lo = sec.querySelector('.t-lo'), hi = sec.querySelector('.t-hi');
    var clan = sec.querySelector('.f-clan'), spawn = sec.querySelector('.f-spawn'), ship = sec.querySelector('.f-ship'), fcls = sec.querySelector('.f-cls'), ftype = sec.querySelector('.f-type');
    var chart = sec.querySelector('.chart'), count = sec.querySelector('.count'), ships = sec.querySelector('.ships');
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
    function shown(p){
      var t = parseInt(p.dataset.t, 10);
      if (t >= 0 && (t < parseInt(lo.value,10) || t > parseInt(hi.value,10))) return false;
      if (clan.value && p.dataset.team !== clan.value) return false;
      if (spawn.value && p.dataset.spawn !== spawn.value) return false;
      if (ship.value && p.dataset.ship !== ship.value) return false;
      if (fcls && fcls.value && p.dataset.cls !== fcls.value) return false;
      if (ftype && ftype.value && p.dataset.type !== ftype.value) return false;
      return true;
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
    function render(){
      var vis = paths.filter(function(p){ var s = shown(p); p.classList.toggle('hide', !s); return s; });
      count.textContent = vis.length + ' of ' + paths.length + ' smokes shown';
      sec.querySelector('.lo').textContent = clockText(parseInt(lo.value,10));
      sec.querySelector('.hi').textContent = clockText(parseInt(hi.value,10));
      var teams = Array.from(new Set(paths.map(function(p){ return p.dataset.team; })));
      var order = ['H-SR','RESIN','PN']; teams.sort(function(a,b){ return order.indexOf(a) - order.indexOf(b); });
      function rows(f){ return teams.map(function(t){ var list = vis.filter(function(p){ return p.dataset.team === t; }); return {team:t, v:f(list), n:list.length, color:(window.TEAM_COLORS||{})[t]||'#94A3B8'}; }); }
      function avg(list, key){ var xs = list.map(function(p){ return p.dataset[key]; }).filter(function(x){ return x !== ''; }).map(Number); return xs.length ? xs.reduce(function(a,b){return a+b;},0)/xs.length : null; }
      chart.innerHTML =
        panel('Smokes', rows(function(l){ return l.length ? l.length : null; }), '', false) +
        panel('Average smoke damage', rows(function(l){ return avg(l, 'dmg'); }), '', false) +
        panel('<abbr class="term" title="' + (window.CONTEST_DEF||'') + '">Average distance to the nearest contested cap</abbr> (negative = inside)', rows(function(l){ return avg(l, 'contested'); }), 'km', false) +
        panel('<abbr class="term" title="' + (window.SELFISH_DEF||'') + '">Selfish smoke</abbr> share', rows(function(l){ var v = avg(l, 'selfish'); return v === null ? null : v * 100; }), '', true);
      if (ships) { var counts = {}; vis.forEach(function(p){ counts[p.dataset.ship] = (counts[p.dataset.ship]||0) + 1; }); ships.innerHTML = donut(counts); }
    }
    function clamp(){ if (parseInt(lo.value,10) > parseInt(hi.value,10)) { if (document.activeElement === lo) hi.value = lo.value; else lo.value = hi.value; } }
    [lo, hi].forEach(function(r){ r.addEventListener('input', function(){ clamp(); render(); }); });
    [clan, spawn, ship, fcls, ftype].forEach(function(s){ if (s) s.addEventListener('change', render); });
    // Filters can be preset from the query string: ?clan=RESIN&spawn=north&ship=Harugumo&from=0&to=600 (seconds since battle start).
    var q = new URLSearchParams(location.search);
    if (q.get('clan')) clan.value = q.get('clan');
    if (q.get('spawn')) spawn.value = q.get('spawn');
    if (q.get('ship')) ship.value = q.get('ship');
    if (q.get('from')) lo.value = q.get('from');
    if (q.get('to')) hi.value = q.get('to');
    clamp(); render();
  });

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

  if (!window.SMOKES) return;
  var rows = window.SMOKES, tbody = document.querySelector('#smokes tbody');
  function fill(id, key){ var sel = document.getElementById(id); var vals = Array.from(new Set(rows.map(function(r){return r[key];}))).filter(Boolean).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', render); }
  fill('f-team','team'); fill('f-player','player'); fill('f-ship','ship'); fill('f-map','map'); fill('f-game','game'); fill('f-type','type'); fill('f-phase','phase');
  fill('f-cls','cls'); fill('f-movement','movement'); fill('f-coverage','coverage'); fill('f-primary','primary'); fill('f-zone','zone'); fill('f-lane','lane');
  (function(){ var sel = document.getElementById('f-purpose'); var vals = Array.from(new Set(rows.flatMap(function(r){ return r.purposes; }))).sort(); vals.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.textContent=v; sel.appendChild(o); }); sel.addEventListener('change', render); })();
  document.getElementById('f-sort').addEventListener('change', render);
  function val(id){ return document.getElementById(id).value; }
  function bar(v, max, color){ var w = max ? Math.max(0, Math.min(1, v/max))*80 : 0; return '<span class="mini"><i style="width:'+w.toFixed(0)+'px;background:'+color+'"></i></span>'; }
  function render(){
    var f = {team:val('f-team'), player:val('f-player'), ship:val('f-ship'), map:val('f-map'), game:val('f-game'), type:val('f-type'), phase:val('f-phase'), cls:val('f-cls'), movement:val('f-movement'), coverage:val('f-coverage'), primary:val('f-primary'), zone:val('f-zone'), lane:val('f-lane')};
    var purpose = val('f-purpose');
    var sort = val('f-sort'), asc = sort==='contested' || sort==='elapsed';
    var list = rows.filter(function(r){ return Object.keys(f).every(function(k){ return !f[k] || r[k]===f[k]; }) && (!purpose || r.purposes.indexOf(purpose) >= 0); });
    list.sort(function(a,b){ var x=a[sort], y=b[sort]; if (x==null) x = asc? Infinity : -Infinity; if (y==null) y = asc? Infinity : -Infinity; return asc ? x-y : y-x; });
    tbody.innerHTML = list.map(function(r){
      var con = r.contested==null ? '-' : (r.contested<0 ? Math.round(r.depth)+'% into '+r.contested_name : (r.contested/1000).toFixed(1)+' km to '+r.contested_name);
      var outcome = r.won ? 'near capture of '+r.won : (r.defended ? 'defended '+r.defended : '-');
      return '<tr data-href="'+r.href+'"><td>'+r.thumb+'</td>'+
        '<td><span class="tag" style="--c:'+r.color+'">'+r.team+'</span></td><td>'+r.player+'</td><td>'+r.ship+'</td><td>'+r.map+'</td>'+
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
  }
  render();
})();