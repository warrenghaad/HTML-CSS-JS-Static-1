/**
 * Mycelial Network — Interactive Canvas Visualization
 *
 * Domains: Theory · Research · Pedagogy · Design
 * Spores (branches): Idea Organization · Visualization Specs · Prompts & Skills ·
 *   Proposed Functionality · Actively Execute · Health · Needed Connectivity
 * Integrations: Supabase · Notion
 */

(function () {
  'use strict';

  /* ── Palette helpers ── */
  const PALETTE = {
    theory:   '#c084fc',
    research: '#38bdf8',
    pedagogy: '#4ade80',
    design:   '#fb923c',
    supabase: '#3ecf8e',
    notion:   '#a0a0a0',
  };

  /* ── Node definitions ── */
  const SPORE_LABELS = [
    'Idea Organization',
    'Visualization Specs',
    'Prompts & Skills',
    'Proposed Functionality',
    'Actively Execute',
    'Health',
    'Needed Connectivity',
  ];

  const SPORE_DESCRIPTIONS = [
    'How concepts cluster, map, and relate to one another',
    'Specs for interactive diagrams, dashboards, and views',
    'Prompt templates, skill taxonomies, and direction sets',
    'Functionality planned but not yet built',
    'Work actively in-progress or being executed now',
    'System health, gaps, blockers, and dependencies',
    'Integrations, APIs, and bridges needed to connect',
  ];

  const DOMAINS = [
    {
      id: 'theory',
      label: 'Theory',
      color: PALETTE.theory,
      desc: 'Foundational theoretical frameworks, ontologies, and conceptual models that underpin the curriculum system.',
      spores: SPORE_LABELS.map((l, i) => ({
        label: l,
        desc: SPORE_DESCRIPTIONS[i],
        status: ['active', 'planned', 'building', 'planned', 'building', 'active', 'planned'][i],
      })),
    },
    {
      id: 'research',
      label: 'Research',
      color: PALETTE.research,
      desc: 'Source material ingestion, literature review, ontology tagging, and knowledge graph construction.',
      spores: SPORE_LABELS.map((l, i) => ({
        label: l,
        desc: SPORE_DESCRIPTIONS[i],
        status: ['active', 'active', 'building', 'planned', 'active', 'building', 'planned'][i],
      })),
    },
    {
      id: 'pedagogy',
      label: 'Pedagogy',
      color: PALETTE.pedagogy,
      desc: 'Lesson design, cognitive scaffolding, curriculum standards mapping, and student-facing delivery.',
      spores: SPORE_LABELS.map((l, i) => ({
        label: l,
        desc: SPORE_DESCRIPTIONS[i],
        status: ['active', 'building', 'active', 'building', 'active', 'active', 'building'][i],
      })),
    },
    {
      id: 'design',
      label: 'Design',
      color: PALETTE.design,
      desc: 'Visual language, UI/UX, asset pipeline, image sourcing, 3D studio, and media production.',
      spores: SPORE_LABELS.map((l, i) => ({
        label: l,
        desc: SPORE_DESCRIPTIONS[i],
        status: ['active', 'active', 'building', 'planned', 'building', 'building', 'planned'][i],
      })),
    },
  ];

  const INTEGRATIONS = [
    {
      id: 'supabase',
      label: 'Supabase',
      color: PALETTE.supabase,
      desc: 'Postgres-backed live database. Stores nodes, edges, lesson records, asset metadata, and status fields for every domain.',
      url: 'https://supabase.com',
      connects: ['theory', 'research', 'pedagogy', 'design'],
    },
    {
      id: 'notion',
      label: 'Notion',
      color: PALETTE.notion,
      desc: 'Networked knowledge workspace. Houses docs, outlines, prompts, and planning pages that feed into each domain.',
      url: 'https://notion.so',
      connects: ['theory', 'research', 'pedagogy', 'design'],
    },
  ];

  /* ── Physics / layout constants ── */
  const DOMAIN_R   = 38;
  const SPORE_R    = 18;
  const INTEG_R    = 30;
  const ORBIT      = 145;   // domain spore orbit radius
  const DOMAIN_GAP = 340;   // spacing between domain centres

  /* ── State ── */
  let canvas, ctx, wrap;
  let W = 0, H = 0;
  let nodes = [];
  let edges = [];
  let pan   = { x: 0, y: 0 };
  let zoom  = 1;
  let dragging = false;
  let dragStart = null;
  let panStart  = null;
  let animId    = null;
  let t         = 0;          // animation time
  let expandedDomains = new Set();
  let selectedNode = null;
  let hoveredNode  = null;
  let activeFilter = null;    // 'theory' | 'research' | 'pedagogy' | 'design' | null

  /* ── Build graph ── */
  function buildGraph() {
    nodes = [];
    edges = [];

    const cx = 0, cy = 0;
    const domainCenters = [];

    /* Domain nodes */
    DOMAINS.forEach((d, di) => {
      const angle = (di / DOMAINS.length) * Math.PI * 2 - Math.PI / 2;
      const r     = DOMAIN_GAP * 0.8;
      const x = cx + Math.cos(angle) * r;
      const y = cy + Math.sin(angle) * r;
      domainCenters.push({ x, y });

      nodes.push({
        id:     d.id,
        type:   'domain',
        label:  d.label,
        color:  d.color,
        desc:   d.desc,
        r:      DOMAIN_R,
        x, y,
        vx: 0, vy: 0,
        domain: d.id,
        data:   d,
      });

      /* Spore nodes */
      d.spores.forEach((s, si) => {
        const sa = (si / d.spores.length) * Math.PI * 2 - Math.PI / 2;
        const sx = x + Math.cos(sa) * ORBIT;
        const sy = y + Math.sin(sa) * ORBIT;
        const nid = `${d.id}-spore-${si}`;

        nodes.push({
          id:     nid,
          type:   'spore',
          label:  s.label,
          color:  d.color,
          desc:   s.desc,
          status: s.status,
          r:      SPORE_R,
          x: sx, y: sy,
          vx: 0, vy: 0,
          domain: d.id,
          parentId: d.id,
          visible: false,   // starts collapsed
        });

        edges.push({
          source: d.id,
          target: nid,
          color:  d.color,
          type:   'spore',
          domain: d.id,
        });
      });
    });

    /* Integration nodes — placed above & below the cluster */
    INTEGRATIONS.forEach((integ, ii) => {
      const x = cx + (ii === 0 ? -300 : 300);
      const y = cy;

      nodes.push({
        id:    integ.id,
        type:  'integration',
        label: integ.label,
        color: integ.color,
        desc:  integ.desc,
        url:   integ.url,
        r:     INTEG_R,
        x, y,
        vx: 0, vy: 0,
        domain: null,
      });

      integ.connects.forEach(did => {
        edges.push({
          source: integ.id,
          target: did,
          color:  integ.color,
          type:   'integration',
          domain: did,
        });
      });
    });

    /* Cross-domain edges (theory ↔ pedagogy, research ↔ knowledge-graph, etc.) */
    const crossLinks = [
      ['theory', 'research'],
      ['research', 'pedagogy'],
      ['pedagogy', 'design'],
      ['design', 'theory'],
    ];
    crossLinks.forEach(([a, b]) => {
      edges.push({ source: a, target: b, color: 'rgba(255,255,255,0.12)', type: 'cross', domain: null });
    });
  }

  /* ── Canvas setup ── */
  function init() {
    canvas = document.getElementById('mycelial-canvas');
    wrap   = document.getElementById('network-wrap');
    ctx    = canvas.getContext('2d');

    resize();
    window.addEventListener('resize', resize);
    buildGraph();

    /* Default: expand all domains */
    DOMAINS.forEach(d => toggleDomain(d.id, true));

    /* Center view */
    pan.x = W / 2;
    pan.y = H / 2;
    zoom  = Math.min(W, H) / 1100;

    bindEvents();
    startLoop();
  }

  function resize() {
    W = wrap.clientWidth;
    H = wrap.clientHeight;
    canvas.width  = W * devicePixelRatio;
    canvas.height = H * devicePixelRatio;
    canvas.style.width  = W + 'px';
    canvas.style.height = H + 'px';
    ctx.scale(devicePixelRatio, devicePixelRatio);
  }

  /* ── Expand / collapse domain spores ── */
  function toggleDomain(domainId, force) {
    const isOpen = expandedDomains.has(domainId);
    const open   = force !== undefined ? force : !isOpen;
    if (open) expandedDomains.add(domainId);
    else       expandedDomains.delete(domainId);

    nodes.forEach(n => {
      if (n.type === 'spore' && n.domain === domainId) {
        n.visible = open;
      }
    });
  }

  /* ── Coordinate helpers ── */
  function worldToScreen(wx, wy) {
    return {
      x: wx * zoom + pan.x,
      y: wy * zoom + pan.y,
    };
  }

  function screenToWorld(sx, sy) {
    return {
      x: (sx - pan.x) / zoom,
      y: (sy - pan.y) / zoom,
    };
  }

  function nodeAtScreen(sx, sy) {
    const w = screenToWorld(sx, sy);
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      if (n.type === 'spore' && !n.visible) continue;
      const dx = n.x - w.x;
      const dy = n.y - w.y;
      if (Math.sqrt(dx * dx + dy * dy) <= n.r + 6) return n;
    }
    return null;
  }

  /* ── Draw ── */
  function draw() {
    ctx.clearRect(0, 0, W, H);

    ctx.save();
    ctx.translate(pan.x, pan.y);
    ctx.scale(zoom, zoom);

    drawEdges();
    drawNodes();

    ctx.restore();
  }

  function hexAlpha(hex, a) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${a})`;
  }

  function drawEdges() {
    edges.forEach(e => {
      const src = nodes.find(n => n.id === e.source);
      const tgt = nodes.find(n => n.id === e.target);
      if (!src || !tgt) return;

      /* Hide spore edges if collapsed */
      if (e.type === 'spore') {
        if (!tgt.visible) return;
      }

      /* Dim if filter active and edge doesn't belong */
      let alpha = 1;
      if (activeFilter) {
        const relevant = (e.domain === activeFilter) || (e.source === activeFilter) || (e.target === activeFilter);
        if (!relevant) alpha = 0.06;
      }
      if (alpha < 0.07) {
        return;
      }

      const pulse = (Math.sin(t * 0.012 + src.x * 0.005) + 1) / 2;

      ctx.save();
      ctx.globalAlpha = alpha;

      if (e.type === 'spore') {
        /* Organic curved stroke */
        drawMycelialEdge(src, tgt, e.color, 1.4 + pulse * 0.6);
      } else if (e.type === 'integration') {
        drawDashedEdge(src, tgt, e.color);
      } else {
        /* Cross-domain faint thread */
        drawMycelialEdge(src, tgt, e.color, 0.7);
      }

      ctx.restore();
    });
  }

  function drawMycelialEdge(src, tgt, color, width) {
    const pulse = (Math.sin(t * 0.008 + src.x * 0.003 + tgt.y * 0.002) + 1) / 2;
    const midX  = (src.x + tgt.x) / 2 + Math.sin(t * 0.006 + src.x) * 8;
    const midY  = (src.y + tgt.y) / 2 + Math.cos(t * 0.006 + tgt.y) * 8;

    /* Glow */
    ctx.beginPath();
    ctx.moveTo(src.x, src.y);
    ctx.quadraticCurveTo(midX, midY, tgt.x, tgt.y);
    ctx.strokeStyle = hexAlpha(color.startsWith('#') ? color : '#7dd3fc', 0.12 + pulse * 0.08);
    ctx.lineWidth = width * 4;
    ctx.lineCap = 'round';
    ctx.stroke();

    /* Core */
    ctx.beginPath();
    ctx.moveTo(src.x, src.y);
    ctx.quadraticCurveTo(midX, midY, tgt.x, tgt.y);
    ctx.strokeStyle = color.startsWith('#') ? hexAlpha(color, 0.55 + pulse * 0.2) : color;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.stroke();
  }

  function drawDashedEdge(src, tgt, color) {
    ctx.beginPath();
    ctx.setLineDash([6, 8]);
    ctx.moveTo(src.x, src.y);
    ctx.lineTo(tgt.x, tgt.y);
    ctx.strokeStyle = hexAlpha(color, 0.45);
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.setLineDash([]);
  }

  function drawNodes() {
    nodes.forEach(n => {
      if (n.type === 'spore' && !n.visible) return;

      let alpha = 1;
      if (activeFilter) {
        if (n.type === 'integration') alpha = 0.25;
        else if (n.domain !== activeFilter) alpha = 0.15;
      }

      ctx.save();
      ctx.globalAlpha = alpha;

      const pulse = (Math.sin(t * 0.01 + n.x * 0.007) + 1) / 2;
      const isHovered  = hoveredNode === n;
      const isSelected = selectedNode === n;
      const scale = isHovered ? 1.18 : isSelected ? 1.12 : 1;

      ctx.save();
      ctx.translate(n.x, n.y);
      ctx.scale(scale, scale);
      ctx.translate(-n.x, -n.y);

      if (n.type === 'domain') {
        drawDomainNode(n, pulse);
      } else if (n.type === 'spore') {
        drawSporeNode(n, pulse);
      } else {
        drawIntegrationNode(n, pulse);
      }

      ctx.restore();
      ctx.restore();
    });
  }

  function drawDomainNode(n, pulse) {
    const r = n.r;

    /* Outer glow rings */
    for (let i = 3; i >= 1; i--) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + i * 8 + pulse * 4, 0, Math.PI * 2);
      ctx.fillStyle = hexAlpha(n.color, 0.04 + (4 - i) * 0.01);
      ctx.fill();
    }

    /* Fill */
    const grad = ctx.createRadialGradient(n.x - r * 0.3, n.y - r * 0.3, 0, n.x, n.y, r);
    grad.addColorStop(0, hexAlpha(n.color, 0.95));
    grad.addColorStop(1, hexAlpha(n.color, 0.55));
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    /* Border */
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.strokeStyle = hexAlpha(n.color, 0.9);
    ctx.lineWidth = 2;
    ctx.stroke();

    /* Label */
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 12px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(n.label, n.x, n.y);
  }

  function drawSporeNode(n, pulse) {
    const r = n.r;

    /* Glow */
    ctx.beginPath();
    ctx.arc(n.x, n.y, r + 6 + pulse * 3, 0, Math.PI * 2);
    ctx.fillStyle = hexAlpha(n.color, 0.07 + pulse * 0.04);
    ctx.fill();

    /* Fill */
    const grad = ctx.createRadialGradient(n.x - r * 0.3, n.y - r * 0.3, 0, n.x, n.y, r);
    grad.addColorStop(0, hexAlpha(n.color, 0.75));
    grad.addColorStop(1, hexAlpha(n.color, 0.3));
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.strokeStyle = hexAlpha(n.color, 0.7);
    ctx.lineWidth = 1.2;
    ctx.stroke();

    /* Status dot */
    const dotColor = { active: '#4ade80', planned: '#fbbf24', building: '#7dd3fc' }[n.status] || '#888';
    ctx.beginPath();
    ctx.arc(n.x + r * 0.6, n.y - r * 0.6, 4, 0, Math.PI * 2);
    ctx.fillStyle = dotColor;
    ctx.fill();

    /* Short label (wrap if needed) */
    ctx.fillStyle = 'rgba(255,255,255,0.9)';
    ctx.font = '9px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const words = n.label.split(' ');
    if (words.length <= 2) {
      ctx.fillText(n.label, n.x, n.y);
    } else {
      ctx.fillText(words.slice(0, 2).join(' '), n.x, n.y - 5);
      ctx.fillText(words.slice(2).join(' '),    n.x, n.y + 5);
    }
  }

  function drawIntegrationNode(n, pulse) {
    const r = n.r;

    /* Dashed orbit ring */
    ctx.beginPath();
    ctx.arc(n.x, n.y, r + 12 + pulse * 3, 0, Math.PI * 2);
    ctx.setLineDash([4, 8]);
    ctx.strokeStyle = hexAlpha(n.color, 0.25);
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.setLineDash([]);

    const grad = ctx.createRadialGradient(n.x - r * 0.3, n.y - r * 0.3, 0, n.x, n.y, r);
    grad.addColorStop(0, hexAlpha(n.color, 0.85));
    grad.addColorStop(1, hexAlpha(n.color, 0.4));
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.strokeStyle = hexAlpha(n.color, 0.85);
    ctx.lineWidth = 1.8;
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 11px ' + getComputedStyle(document.body).fontFamily;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(n.label, n.x, n.y);
  }

  /* ── Animation loop ── */
  function startLoop() {
    function loop() {
      t++;
      draw();
      animId = requestAnimationFrame(loop);
    }
    loop();
  }

  /* ── Events ── */
  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    if (e.touches) {
      return { x: e.touches[0].clientX - rect.left, y: e.touches[0].clientY - rect.top };
    }
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  function bindEvents() {
    /* Drag to pan */
    canvas.addEventListener('mousedown',  onDragStart);
    canvas.addEventListener('touchstart', onDragStart, { passive: true });
    window.addEventListener('mousemove',  onDragMove);
    window.addEventListener('touchmove',  onDragMove, { passive: false });
    window.addEventListener('mouseup',    onDragEnd);
    window.addEventListener('touchend',   onDragEnd);

    /* Scroll to zoom */
    canvas.addEventListener('wheel', onWheel, { passive: false });

    /* Click / tap */
    canvas.addEventListener('click', onClick);

    /* Hover for tooltip */
    canvas.addEventListener('mousemove', onHover);
    canvas.addEventListener('mouseleave', () => { hoveredNode = null; hideTooltip(); });

    /* Filter buttons */
    document.querySelectorAll('[data-filter]').forEach(btn => {
      btn.addEventListener('click', () => {
        const f = btn.dataset.filter;
        activeFilter = activeFilter === f ? null : f;
        document.querySelectorAll('[data-filter]').forEach(b => b.classList.toggle('active', b.dataset.filter === activeFilter));
      });
    });

    /* Expand-all / collapse-all */
    document.getElementById('btn-expand-all').addEventListener('click', () => {
      DOMAINS.forEach(d => toggleDomain(d.id, true));
    });
    document.getElementById('btn-collapse-all').addEventListener('click', () => {
      DOMAINS.forEach(d => toggleDomain(d.id, false));
    });
    document.getElementById('btn-reset-view').addEventListener('click', resetView);

    /* Side panel close */
    document.getElementById('panel-close').addEventListener('click', closePanel);

    /* Keyboard */
    window.addEventListener('keydown', e => {
      if (e.key === 'Escape') { closePanel(); activeFilter = null; }
    });
  }

  let dragMoved = false;

  function onDragStart(e) {
    dragging  = true;
    dragMoved = false;
    const pos = getPos(e);
    dragStart = pos;
    panStart  = { x: pan.x, y: pan.y };
  }

  function onDragMove(e) {
    if (!dragging) {
      const pos = getPos(e);
      const n   = nodeAtScreen(pos.x, pos.y);
      if (n !== hoveredNode) {
        hoveredNode = n;
        if (n) showTooltip(n, pos.x, pos.y);
        else   hideTooltip();
      }
      return;
    }
    if (e.cancelable) e.preventDefault();
    const pos = getPos(e);
    pan.x = panStart.x + (pos.x - dragStart.x);
    pan.y = panStart.y + (pos.y - dragStart.y);
    const d = Math.hypot(pos.x - dragStart.x, pos.y - dragStart.y);
    if (d > 4) dragMoved = true;
  }

  function onDragEnd() {
    dragging = false;
  }

  function onWheel(e) {
    e.preventDefault();
    const pos   = getPos(e);
    const delta = e.deltaY > 0 ? 0.92 : 1.09;
    const wx    = (pos.x - pan.x) / zoom;
    const wy    = (pos.y - pan.y) / zoom;
    zoom = Math.min(3, Math.max(0.25, zoom * delta));
    pan.x = pos.x - wx * zoom;
    pan.y = pos.y - wy * zoom;
  }

  function onClick(e) {
    if (dragMoved) return;
    const pos = getPos(e);
    const n   = nodeAtScreen(pos.x, pos.y);

    if (!n) { closePanel(); selectedNode = null; return; }
    selectedNode = n;

    if (n.type === 'domain') {
      toggleDomain(n.id);
    }

    openPanel(n);
  }

  function onHover(e) {
    if (dragging) return;
    const pos = getPos(e);
    const n   = nodeAtScreen(pos.x, pos.y);
    if (n !== hoveredNode) {
      hoveredNode = n;
      if (n) showTooltip(n, e.clientX, e.clientY);
      else   hideTooltip();
    } else if (n) {
      moveTooltip(e.clientX, e.clientY);
    }
  }

  /* ── Tooltip ── */
  const tooltip = document.getElementById('node-tooltip');

  function showTooltip(n, cx, cy) {
    tooltip.querySelector('.tt-title').textContent = n.label;
    tooltip.querySelector('.tt-body').textContent  = n.desc || '';
    const tags = tooltip.querySelector('.tt-tags');
    tags.innerHTML = '';
    if (n.status) {
      const t = document.createElement('span');
      t.className = 'tt-tag';
      t.textContent = n.status;
      t.style.color = { active: '#4ade80', planned: '#fbbf24', building: '#7dd3fc' }[n.status] || '#aaa';
      tags.appendChild(t);
    }
    if (n.type === 'domain') {
      const t = document.createElement('span');
      t.className = 'tt-tag';
      t.textContent = 'Click to expand / collapse';
      tags.appendChild(t);
    }
    moveTooltip(cx, cy);
    tooltip.classList.add('visible');
  }

  function moveTooltip(cx, cy) {
    const tw = tooltip.offsetWidth  || 240;
    const th = tooltip.offsetHeight || 80;
    let  tx  = cx + 14;
    let  ty  = cy - 14;
    if (tx + tw > window.innerWidth  - 12) tx = cx - tw - 14;
    if (ty + th > window.innerHeight - 12) ty = cy - th + 14;
    tooltip.style.left = tx + 'px';
    tooltip.style.top  = ty + 'px';
  }

  function hideTooltip() { tooltip.classList.remove('visible'); }

  /* ── Side panel ── */
  const panel = document.getElementById('side-panel');

  function openPanel(n) {
    const title = document.getElementById('panel-title');
    const body  = document.getElementById('panel-body-content');
    title.textContent = n.label;

    let html = '';

    /* Domain heading color */
    const colorStyle = `color: ${n.color || '#fff'}`;

    html += `<div class="panel-section">`;
    html += `<p class="panel-section-title">Description</p>`;
    html += `<p style="font-size:0.84rem;line-height:1.55;">${n.desc || '—'}</p>`;
    html += `</div>`;

    if (n.type === 'domain') {
      html += `<div class="panel-section">`;
      html += `<p class="panel-section-title">Category Spores</p>`;
      n.data.spores.forEach((s, i) => {
        const badge = `<span class="health-badge ${s.status}">${s.status}</span>`;
        html += `<div class="attr-row"><span class="attr-label">${s.label}</span>${badge}</div>`;
      });
      html += `</div>`;
    }

    if (n.type === 'spore') {
      html += `<div class="panel-section">`;
      html += `<div class="attr-row"><span class="attr-label">Domain</span><span class="attr-value" style="${colorStyle}">${capitalize(n.domain)}</span></div>`;
      html += `<div class="attr-row"><span class="attr-label">Status</span><span class="health-badge ${n.status}">${n.status}</span></div>`;
      html += `</div>`;
    }

    if (n.type === 'integration') {
      html += `<div class="panel-section">`;
      html += `<p class="panel-section-title">Integration Link</p>`;
      html += `<a href="${n.url}" target="_blank" rel="noopener" class="int-link">`;
      html += `<span class="int-dot" style="background:${n.color}"></span>`;
      html += `Open ${n.label} ↗`;
      html += `</a>`;
      html += `</div>`;
      html += `<div class="panel-section">`;
      html += `<p class="panel-section-title">Connected Domains</p>`;
      INTEGRATIONS.find(i => i.id === n.id).connects.forEach(did => {
        const dom = DOMAINS.find(d => d.id === did);
        html += `<div class="attr-row"><span class="int-dot" style="background:${dom.color};display:inline-block;margin-right:6px;border-radius:50%;width:8px;height:8px;"></span><span>${dom.label}</span></div>`;
      });
      html += `</div>`;
    }

    body.innerHTML = html;
    panel.classList.add('open');
  }

  function closePanel() { panel.classList.remove('open'); }

  /* ── View controls ── */
  function resetView() {
    pan.x = W / 2;
    pan.y = H / 2;
    zoom  = Math.min(W, H) / 1100;
  }

  function capitalize(s) { return s ? s[0].toUpperCase() + s.slice(1) : ''; }

  /* ── Init on DOM ready ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
