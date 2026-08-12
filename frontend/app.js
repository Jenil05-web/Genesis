/* ════════════════════════════════════════════
   GENESIS  —  App Logic v3
════════════════════════════════════════════ */

// In production, window.GENESIS_API_URL is set by a <script> block in index.html
// injected at build/deploy time. Locally it falls back to the dev server.
const API = window.GENESIS_API_URL || 'http://127.0.0.1:8000';


const S = {
  threadId:  null,
  startTime: null,
  map:       null,
  stats: { total: 0, approved: 0, rejected: 0, totalMs: 0 },
};

// ── Boot ───────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  bootSequence();
  startClock();
  checkApi();
  setInterval(checkApi, 15_000);

  // Char counter
  const ta = document.getElementById('situationInput');
  const cc = document.getElementById('charCounter');
  ta.addEventListener('input', () => {
    cc.textContent = `${ta.value.length} characters`;
  });
});

function bootSequence() {
  const loader = document.getElementById('pageLoader');
  const header = document.getElementById('appHeader');
  const msg    = document.getElementById('loaderMsg');
  const steps  = ['Initializing…', 'Loading response protocols…', 'Ready.'];
  let i = 0;
  const iv = setInterval(() => { if (i < steps.length) msg.textContent = steps[i++]; }, 520);
  setTimeout(() => {
    clearInterval(iv);
    loader.classList.add('out');
    header.classList.add('visible');
  }, 1750);
}

function startClock() {
  const el = document.getElementById('timeDisplay');
  const tick = () => {
    el.textContent = new Date().toLocaleTimeString('en-US', { hour12: false });
  };
  tick();
  setInterval(tick, 1000);
}

// ── API health ─────────────────────────────────────────────────────────
async function checkApi() {
  const dot   = document.getElementById('apiDot');
  const label = document.getElementById('apiLabel');
  try {
    const r = await fetch(`${API}/health`, { signal: AbortSignal.timeout(3000) });
    if (r.ok) {
      dot.className   = 'api-dot online';
      label.textContent = 'API Online';
    } else throw 0;
  } catch {
    dot.className   = 'api-dot offline';
    label.textContent = 'API Offline';
  }
}

// ── Toast ──────────────────────────────────────────────────────────────
function toast(msg, ms = 3200) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), ms);
}

// ── Pipeline helpers ───────────────────────────────────────────────────
const STEPS = ['alert', 'image', 'plan', 'quality', 'approval', 'execute'];

const PROC_LABELS = {
  alert:    'Classifying alert signal…',
  image:    'Analyzing imagery…',
  plan:     'Drafting response plan…',
  quality:  'Running quality checks…',
  approval: 'Awaiting authorization…',
  execute:  'Dispatching field actions…',
};

function setNode(id, state) {    // '' | 'active' | 'done'
  const el = document.getElementById(`step-${id}`);
  if (el) el.className = `pp-node ${state}`;
}

function resetPipeline() {
  STEPS.forEach(s => setNode(s, ''));
  setFill(0);
  const dot = document.getElementById('ppDot');
  if (dot) dot.className = 'pp-dot';
}

function setFill(pct) {
  const el = document.getElementById('trackFill');
  if (el) el.style.width = `${pct}%`;
}

function setProcMsg(text) {
  const el = document.getElementById('procStep');
  if (!el) return;
  el.style.opacity = '0';
  setTimeout(() => { el.textContent = text; el.style.opacity = '1'; }, 160);
}

// ── Run Incident ───────────────────────────────────────────────────────
async function runIncident() {
  const situation = document.getElementById('situationInput').value.trim();
  if (!situation) { toast('Enter a situation description first.'); return; }

  const imageUrl = document.getElementById('imageInput').value.trim() || null;

  // Reset
  hide('emptyState');
  hide('resultsContainer');
  hide('approvalBox');
  hide('executionCard');

  show('pipelineStatus');
  show('processingOverlay');
  resetPipeline();

  const ppDot = document.getElementById('ppDot');
  if (ppDot) ppDot.className = 'pp-dot running';

  const btn = document.getElementById('runBtn');
  btn.disabled = true;
  btn.innerHTML = `<div class="btn-spin"></div> Running…`;

  S.startTime = Date.now();

  try {
    setNode('alert', 'active');
    setFill(8);
    setProcMsg(PROC_LABELS.alert);

    const res = await fetch(`${API}/incidents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ situation, image_path: imageUrl }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }

    const data = await res.json();
    S.threadId = data.thread_id;

    // Animate steps completing
    const stepSeq = [
      ['alert', 'image', 18, PROC_LABELS.image],
      ['image', 'plan',  36, PROC_LABELS.plan],
      ['plan',  'quality', 55, PROC_LABELS.quality],
      ['quality', null,  72, null],
    ];

    for (const [done, next, pct, nextLabel] of stepSeq) {
      await sleep(300);
      setNode(done, 'done');
      if (next) { setNode(next, 'active'); setProcMsg(nextLabel); }
      setFill(pct);
    }

    // Hide processing overlay
    hide('processingOverlay');

    // Populate cards
    populateAlert(data.alert_info);
    populateImage(data.image_findings, imageUrl);
    populatePlan(data.response_plan);
    populateQuality(data.quality_result, data.retry_count);
    populateMap(data.location_coords);

    show('resultsContainer');
    show('approvalBox');

    setNode('approval', 'active');
    setFill(85);

    S.stats.total++;
    updateStats();
    toast('Pipeline complete — review and authorize dispatch.');

  } catch (err) {
    hide('processingOverlay');
    resetPipeline();
    show('emptyState');
    toast(`Error: ${err.message}`, 5000);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><polygon points="4,2 16,10 4,18"/></svg> Run Pipeline`;
  }
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── Authorize / Reject ─────────────────────────────────────────────────
async function approveIncident(approved) {
  if (!S.threadId) return;

  const aBtn = document.getElementById('approveBtn');
  const rBtn = document.getElementById('rejectBtn');
  aBtn.disabled = rBtn.disabled = true;
  aBtn.innerHTML = `<div class="btn-spin" style="border-top-color:var(--green);width:11px;height:11px;"></div> Processing…`;

  setNode('approval', 'done');
  setNode('execute', 'active');
  setFill(92);
  show('processingOverlay');
  setProcMsg(PROC_LABELS.execute);

  try {
    const res = await fetch(`${API}/incidents/${S.threadId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ approved }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }

    const data = await res.json();

    hide('processingOverlay');
    setNode('execute', 'done');
    setFill(100);

    const ppDot = document.getElementById('ppDot');
    if (ppDot) ppDot.className = 'pp-dot';

    populateExecution(data.execution_result, approved);
    hide('approvalBox');

    const elapsed = Date.now() - S.startTime;
    if (approved) S.stats.approved++; else S.stats.rejected++;
    S.stats.totalMs += elapsed;

    addLogItem(
      document.getElementById('situationInput').value.trim(),
      approved,
    );
    updateStats();

    toast(approved ? 'Actions authorized and dispatched.' : 'Plan rejected.');

  } catch (err) {
    hide('processingOverlay');
    setNode('execute', '');
    toast(`Error: ${err.message}`, 5000);
  } finally {
    aBtn.disabled = rBtn.disabled = false;
    aBtn.innerHTML = `<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><polyline points="14,4 6.5,12 2,8"/></svg> Authorize`;
  }
}

// ── Populate cards ─────────────────────────────────────────────────────
function populateAlert(info) {
  if (!info || !Object.keys(info).length) return;

  const isSos    = info.is_actionable_sos;
  const severity = (info.severity || 'unknown').toLowerCase();
  const type     = cap((info.disaster_type || 'unknown').replace(/_/g, ' '));

  setText('disasterType', type);
  setText('locationHint', info.location_hint || 'Not identified');
  setText('alertReason',  info.reason || '—');

  const sosEl = document.getElementById('isSos');
  sosEl.textContent = isSos ? 'Yes — Urgent' : 'No';
  sosEl.style.color = isSos ? 'var(--red)' : 'var(--green)';

  const sevEl = document.getElementById('severityBadge');
  sevEl.textContent = cap(severity);
  sevEl.className = `dc-val sev-${severity}`;

  const badge = document.getElementById('alertBadge');
  badge.textContent = isSos ? 'SOS Active' : 'Monitoring';
  badge.className = `dc-badge ${isSos ? 'badge-red' : 'badge-neutral'}`;

  show('alertCard');
}

function populateImage(findings, imageUrl) {
  if (!findings || !Object.keys(findings).length) return;
  if (!findings.severity_estimate && !findings.notes && !imageUrl) return;

  const fmt = v => v == null ? '—' : v === true ? 'Yes' : v === false ? 'No' : String(v);
  setText('imgFlooded',    fmt(findings.flooded_zones));
  setText('imgRoads',      fmt(findings.blocked_roads));
  setText('imgStructures', fmt(findings.collapsed_structures));
  setText('imgNotes',      findings.notes || '—');

  const sev = (findings.severity_estimate || 'unknown').toLowerCase();
  const sevEl = document.getElementById('imgSeverity');
  sevEl.textContent = cap(sev);
  sevEl.className = `dc-val sev-${sev}`;

  show('imageCard');
}

function populatePlan(plan) {
  if (!plan || !Object.keys(plan).length) return;

  const fillList = (id, raw) => {
    const ul = document.getElementById(id);
    ul.innerHTML = '';
    const items = raw
      ? raw.split(/\n|(?=\d+\.\s)/).map(s => s.replace(/^\d+\.\s*/, '').trim()).filter(Boolean)
      : [];
    (items.length ? items : ['No actions specified.']).forEach(txt => {
      const li = document.createElement('li');
      li.textContent = txt;
      if (!items.length) li.style.color = 'var(--t3)';
      ul.appendChild(li);
    });
  };

  fillList('immediateList', plan.immediate);
  fillList('shortTermList', plan.short_term);
  fillList('recoveryList',  plan.recovery);
  show('planCard');
}

function populateQuality(qa, retries) {
  if (!qa || !Object.keys(qa).length) return;

  const passed = qa.passed;
  setText('qaStatus',  passed ? 'Passed' : 'Failed');
  setText('qaRetries', String(retries ?? 0));

  document.getElementById('qaStatus').style.color = passed ? 'var(--green)' : 'var(--amber)';

  const fill  = document.getElementById('qaMeterFill');
  const label = document.getElementById('qaBarLabel');
  fill.className = `qa-bar-fill ${passed ? 'pass' : 'fail'}`;
  label.textContent = passed ? 'All checks passed' : 'Issues detected';
  setTimeout(() => {
    fill.style.width = passed ? '100%' : `${Math.max(15, 100 - (retries || 1) * 22)}%`;
  }, 50);

  const badge = document.getElementById('qualityBadge');
  badge.textContent = passed ? 'Passed' : 'Failed';
  badge.className = `dc-badge ${passed ? 'badge-green' : 'badge-amber'}`;

  const issues = qa.issues || [];
  if (issues.length) {
    const wrap = document.getElementById('qaIssuesWrap');
    const list = document.getElementById('qaIssuesList');
    list.innerHTML = '';
    issues.forEach(iss => {
      const li = document.createElement('li');
      li.textContent = iss;
      list.appendChild(li);
    });
    wrap.style.display = 'block';
  }

  show('qualityCard');
}

function populateExecution(result, approved) {
  if (!result) return;

  const log  = document.getElementById('execLog');
  const badge = document.getElementById('execBadge');
  log.innerHTML = '';

  if (!result.executed) {
    const div = document.createElement('div');
    div.className = 'dl-denied';
    div.textContent = result.log?.[0] || 'Plan rejected — no actions dispatched.';
    log.appendChild(div);
    badge.textContent = 'Rejected';
    badge.className = 'dc-badge badge-amber';
  } else {
    badge.textContent = 'Dispatched';
    badge.className = 'dc-badge badge-green';

    (result.log || []).forEach((entry, i) => {
      const div = document.createElement('div');
      div.className = 'dl-entry';
      div.style.animationDelay = `${i * 55}ms`;

      const phase = document.createElement('span');
      phase.className = `dl-phase dl-phase-${entry.phase || 'immediate'}`;
      phase.textContent = (entry.phase || 'action').replace('_', ' ').toUpperCase();

      const content = document.createElement('div');
      content.className = 'dl-content';

      const action = document.createElement('div');
      action.className = 'dl-action';
      action.textContent = entry.action || String(entry);

      const status = document.createElement('div');
      status.className = 'dl-status';
      status.textContent = entry.status || 'Logged';

      content.appendChild(action);
      content.appendChild(status);
      div.appendChild(phase);
      div.appendChild(content);
      log.appendChild(div);
    });

    if (result.timestamp) {
      const ts = document.createElement('div');
      ts.className = 'dl-ts';
      ts.textContent = `Dispatched ${new Date(result.timestamp).toLocaleString()}`;
      log.appendChild(ts);
    }

    if (result.quality_warning) {
      const warn = document.createElement('div');
      warn.className = 'qa-warn-banner';
      warn.innerHTML = `<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" width="13" height="13"><path d="M8 2L1 14h14L8 2z"/><line x1="8" y1="6" x2="8" y2="9"/><circle cx="8" cy="11.5" r=".7" fill="currentColor"/></svg> Dispatched after retry limit — quality check did not fully pass.`;
      log.appendChild(warn);
    }
  }

  show('executionCard');
}

// ── Map ────────────────────────────────────────────────────────────────
function populateMap(coords) {
  if (!coords || coords.lat == null) return;

  setText('coordLat', coords.lat.toFixed(5));
  setText('coordLon', coords.lon.toFixed(5));
  hide('mapEmpty');
  show('mapContent');

  if (S.map) { S.map.remove(); S.map = null; }

  setTimeout(() => {
    const map = L.map('leafletMap', {
      center:           [coords.lat, coords.lon],
      zoom:             11,
      zoomControl:      true,
      scrollWheelZoom:  true,     // ← enabled so user can zoom without clicking
      attributionControl: false,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    // Precision marker
    const icon = L.divIcon({
      html: `<div style="
        width:14px;height:14px;
        background:#ef4444;
        border:2px solid #fff;
        border-radius:50%;
        box-shadow:0 0 0 3px rgba(239,68,68,.25),0 2px 8px rgba(0,0,0,.6);
      "></div>`,
      className: '',
      iconAnchor: [7, 7],
    });

    L.marker([coords.lat, coords.lon], { icon }).addTo(map);

    // Radius ring — subtle context
    L.circle([coords.lat, coords.lon], {
      radius:      4000,
      color:       'rgba(239,68,68,.25)',
      fillColor:   'rgba(239,68,68,.04)',
      fillOpacity: 1,
      weight:      1,
    }).addTo(map);

    S.map = map;
  }, 100);
}

// ── Phase tabs ─────────────────────────────────────────────────────────
function switchPhase(id, btn) {
  document.querySelectorAll('.phase-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.pt-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`phase-${id}`).classList.add('active');
  btn.classList.add('active');
}

// ── Stats ──────────────────────────────────────────────────────────────
function updateStats() {
  countUp('statIncidents', S.stats.total);
  countUp('statApproved',  S.stats.approved);
  countUp('statRejected',  S.stats.rejected);
  if (S.stats.total > 0) {
    const avg = Math.round(S.stats.totalMs / S.stats.total / 1000);
    document.getElementById('statAvgTime').textContent = `${avg}s`;
  }
}

function countUp(id, target) {
  const el   = document.getElementById(id);
  const from = parseInt(el.textContent) || 0;
  const t0   = Date.now();
  const dur  = 500;
  const tick = () => {
    const p = Math.min(1, (Date.now() - t0) / dur);
    el.textContent = Math.round(from + (target - from) * easeOut(p));
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

const easeOut = t => 1 - Math.pow(1 - t, 3);

// ── Log items ──────────────────────────────────────────────────────────
function addLogItem(situation, approved) {
  const list = document.getElementById('historyList');
  const void_ = list.querySelector('.log-void');
  if (void_) void_.remove();

  const item = document.createElement('div');
  item.className = 'log-item';
  const time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });

  item.innerHTML = `
    <div class="log-item-title">${esc(situation.slice(0, 60))}${situation.length > 60 ? '…' : ''}</div>
    <div class="log-item-meta">
      <span class="dc-badge ${approved ? 'badge-green' : 'badge-amber'}" style="font-size:9.5px;padding:1px 7px;">${approved ? 'Authorized' : 'Rejected'}</span>
      <span class="log-item-time">${time}</span>
    </div>`;
  list.prepend(item);
}

// ── Helpers ────────────────────────────────────────────────────────────
const show    = id => { const e = document.getElementById(id); if (e) e.style.display = 'block'; };
const hide    = id => { const e = document.getElementById(id); if (e) e.style.display = 'none'; };
const setText = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
const cap     = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
const esc     = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
