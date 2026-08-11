/* ========================
   GENESIS AI — APP LOGIC
   Emergency Operations Center
   ======================== */

const API_URL = 'http://127.0.0.1:8000';

// ── State ──────────────────────────────────────────────────────────────────
const state = {
  currentThreadId: null,
  incidentStartTime: null,
  stats: { incidents: 0, approved: 0, rejected: 0, totalMs: 0 },
  history: [],
  leafletMap: null,
  leafletMarker: null,
};

// ── On load ────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  updateClock();
  setInterval(updateClock, 1000);
  checkApiStatus();
  setInterval(checkApiStatus, 15000);
});

function updateClock() {
  const el = document.getElementById('timeDisplay');
  if (!el) return;
  el.textContent = new Date().toLocaleTimeString('en-US', {
    hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit',
  });
}

// ── API health check ───────────────────────────────────────────────────────
async function checkApiStatus() {
  const dot  = document.getElementById('apiStatusDot');
  const text = document.getElementById('apiStatusText');
  try {
    const res = await fetch(`${API_URL}/health`, { signal: AbortSignal.timeout(3000) });
    if (res.ok) {
      dot.className  = 'status-dot online';
      text.textContent = 'API Online — Ready';
    } else { throw new Error('non-2xx'); }
  } catch {
    dot.className  = 'status-dot offline';
    text.textContent = 'API Offline';
  }
}

// ── Toast ──────────────────────────────────────────────────────────────────
function showToast(msg, durationMs = 3000) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), durationMs);
}

// ── Pipeline step helpers ──────────────────────────────────────────────────
function setStep(id, status) {            // status: '' | 'active' | 'done'
  const el = document.getElementById(`step-${id}`);
  if (el) el.className = `pipeline-step ${status}`;
}

function resetPipeline() {
  ['alert','image','plan','quality','approval','execute'].forEach(s => setStep(s, ''));
}

// ── Run Incident ───────────────────────────────────────────────────────────
async function runIncident() {
  const situation = document.getElementById('situationInput').value.trim();
  if (!situation) { showToast('⚠️  Please enter a situation description.'); return; }

  const imageUrl = document.getElementById('imageInput').value.trim() || null;

  // Reset UI
  document.getElementById('emptyState').style.display     = 'none';
  document.getElementById('resultsContainer').style.display = 'none';
  document.getElementById('approvalBox').style.display      = 'none';
  document.getElementById('executionCard').style.display    = 'none';

  const btn = document.getElementById('runBtn');
  btn.disabled = true;
  btn.innerHTML = `<div class="spinner"></div> Running AI Pipeline…`;

  document.getElementById('pipelineStatus').style.display = 'block';
  resetPipeline();
  setStep('alert', 'active');

  state.incidentStartTime = Date.now();

  try {
    const res = await fetch(`${API_URL}/incidents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ situation, image_path: imageUrl }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'API error');
    }

    const data = await res.json();
    state.currentThreadId = data.thread_id;

    // Animate pipeline steps completing
    await animatePipelineComplete(data);

    // Populate result cards
    populateAlertCard(data.alert_info);
    populateImageCard(data.image_findings, imageUrl);
    populatePlanCard(data.response_plan);
    populateQualityCard(data.quality_result, data.retry_count);
    populateMap(data.location_coords);

    document.getElementById('resultsContainer').style.display = 'block';
    document.getElementById('approvalBox').style.display      = 'block';

    setStep('approval', 'active');

    state.stats.incidents++;
    updateStats();
    showToast('✅ Pipeline complete — awaiting your approval');

  } catch (err) {
    showToast(`❌ Error: ${err.message}`, 5000);
    resetPipeline();
    document.getElementById('emptyState').style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><polygon points="5,3 19,12 5,21"/></svg> Run AI Pipeline`;
  }
}

async function animatePipelineComplete(data) {
  const steps = ['alert','image','plan','quality'];
  for (const s of steps) {
    await sleep(350);
    setStep(s, 'done');
  }
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Approve / Reject ───────────────────────────────────────────────────────
async function approveIncident(approved) {
  if (!state.currentThreadId) return;

  const approveBtn = document.querySelector('.btn-approve');
  const rejectBtn  = document.querySelector('.btn-reject');
  approveBtn.disabled = true;
  rejectBtn.disabled  = true;
  approveBtn.innerHTML = `<div class="spinner"></div> Processing…`;

  setStep('approval', 'done');
  setStep('execute', 'active');

  try {
    const res = await fetch(`${API_URL}/incidents/${state.currentThreadId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ approved }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'API error');
    }

    const data = await res.json();

    setStep('execute', 'done');
    populateExecutionCard(data.execution_result, approved);

    document.getElementById('approvalBox').style.display = 'none';

    // Update stats
    const elapsed = Date.now() - state.incidentStartTime;
    if (approved) { state.stats.approved++; }
    else          { state.stats.rejected++; }
    state.stats.totalMs += elapsed;

    // Add to history
    addToHistory(
      document.getElementById('situationInput').value.trim(),
      approved,
      elapsed,
      state.currentThreadId,
    );

    updateStats();
    showToast(approved ? '🚀 Actions dispatched!' : '🚫 Plan rejected.', 4000);

  } catch (err) {
    showToast(`❌ Approval failed: ${err.message}`, 5000);
    setStep('execute', '');
  } finally {
    approveBtn.disabled = false;
    rejectBtn.disabled  = false;
    approveBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16"><polyline points="20,6 9,17 4,12"/></svg> Approve &amp; Dispatch`;
  }
}

// ── Populate Cards ─────────────────────────────────────────────────────────
function populateAlertCard(info) {
  if (!info || !Object.keys(info).length) return;

  const isSos      = info.is_actionable_sos;
  const severity   = (info.severity || 'unknown').toLowerCase();
  const disType    = (info.disaster_type || 'unknown').replace('_', ' ');
  const locHint    = info.location_hint || 'Not detected';
  const reason     = info.reason || '—';

  document.getElementById('disasterType').textContent = capitalize(disType);
  document.getElementById('locationHint').textContent = locHint;
  document.getElementById('alertReason').textContent  = reason;

  // SOS badge
  const alertBadge = document.getElementById('alertBadge');
  if (isSos) {
    alertBadge.textContent  = '🚨 SOS Active';
    alertBadge.className    = 'badge badge-sos';
  } else {
    alertBadge.textContent  = 'Monitoring';
    alertBadge.className    = 'badge badge-info';
  }

  // SOS text
  const sosEl = document.getElementById('isSos');
  sosEl.textContent = isSos ? 'Yes — Urgent' : 'No';
  sosEl.style.color = isSos ? 'var(--red)' : 'var(--green)';

  // Severity
  const sevEl = document.getElementById('severityBadge');
  sevEl.textContent = capitalize(severity);
  sevEl.className   = `info-value severity-badge severity-${severity}`;

  show('alertCard');
}

function populateImageCard(findings, imageUrl) {
  if (!findings || !Object.keys(findings).length) return;

  const hasData = findings.severity_estimate || findings.notes;
  if (!hasData && !imageUrl) return;

  const fmt = v => v === null ? '—' : v === true ? '✓ Yes' : v === false ? '✗ No' : String(v);

  document.getElementById('imgFlooded').textContent    = fmt(findings.flooded_zones);
  document.getElementById('imgRoads').textContent      = fmt(findings.blocked_roads);
  document.getElementById('imgStructures').textContent = fmt(findings.collapsed_structures);
  document.getElementById('imgNotes').textContent      = findings.notes || '—';

  const sevEl = document.getElementById('imgSeverity');
  const sev   = (findings.severity_estimate || 'unknown').toLowerCase();
  sevEl.textContent = capitalize(sev);
  sevEl.className   = `info-value severity-badge severity-${sev}`;

  show('imageCard');
}

function populatePlanCard(plan) {
  if (!plan || !Object.keys(plan).length) return;

  const makeItems = (text) => {
    if (!text) return [];
    // Split on numbered items or newlines
    return text
      .split(/\n|(?=\d+\.\s)/)
      .map(s => s.replace(/^\d+\.\s*/, '').trim())
      .filter(Boolean);
  };

  const fillList = (listId, items) => {
    const ul = document.getElementById(listId);
    ul.innerHTML = '';
    items.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      ul.appendChild(li);
    });
    if (!items.length) {
      const li = document.createElement('li');
      li.textContent = 'No actions specified.';
      li.style.color = 'var(--text-muted)';
      ul.appendChild(li);
    }
  };

  fillList('immediateList', makeItems(plan.immediate));
  fillList('shortTermList', makeItems(plan.short_term));
  fillList('recoveryList',  makeItems(plan.recovery));

  show('planCard');
}

function populateQualityCard(qa, retries) {
  if (!qa || !Object.keys(qa).length) return;

  const passed = qa.passed;

  document.getElementById('qaRetries').textContent = retries ?? 0;

  const statusEl = document.getElementById('qaStatus');
  statusEl.textContent = passed ? '✓ Passed' : '⚠ Failed';
  statusEl.style.color = passed ? 'var(--green)' : 'var(--amber)';

  const badge = document.getElementById('qualityBadge');
  badge.textContent = passed ? 'QA Passed' : 'QA Failed';
  badge.className   = `badge ${passed ? 'badge-ok' : 'badge-warn'}`;

  const issues = qa.issues || [];
  if (issues.length > 0) {
    const wrap = document.getElementById('qaIssuesWrap');
    const list = document.getElementById('qaIssuesList');
    list.innerHTML = '';
    issues.forEach(issue => {
      const li = document.createElement('li');
      li.textContent = issue;
      list.appendChild(li);
    });
    wrap.style.display = 'block';
  }

  show('qualityCard');
}

function populateExecutionCard(execResult, approved) {
  if (!execResult) return;

  const logEl  = document.getElementById('execLog');
  const badge  = document.getElementById('execBadge');
  logEl.innerHTML = '';

  if (!execResult.executed) {
    const msg = document.createElement('div');
    msg.className   = 'log-entry log-denied';
    msg.textContent = execResult.log?.[0] || 'Plan was rejected — no actions taken.';
    logEl.appendChild(msg);
    badge.textContent = 'Rejected';
    badge.className   = 'badge badge-warn';
  } else {
    badge.textContent = '✓ Dispatched';
    badge.className   = 'badge badge-ok';

    const entries = execResult.log || [];
    entries.forEach(entry => {
      const div = document.createElement('div');
      div.className = 'log-entry log-success';

      const tag = document.createElement('span');
      tag.className   = `log-phase-tag log-phase-${entry.phase || 'immediate'}`;
      tag.textContent = (entry.phase || 'action').replace('_', ' ').toUpperCase();

      const action = document.createElement('span');
      action.className   = 'log-action';
      action.textContent = entry.action || entry;

      const status = document.createElement('span');
      status.className   = 'log-status';
      status.textContent = entry.status || 'logged';

      div.appendChild(tag);
      div.appendChild(action);
      div.appendChild(status);
      logEl.appendChild(div);
    });

    // Timestamp
    if (execResult.timestamp) {
      const ts = document.createElement('div');
      ts.style.cssText = 'font-size:11px;color:var(--text-muted);margin-top:8px;font-family:JetBrains Mono,monospace;';
      ts.textContent   = `Dispatched at: ${new Date(execResult.timestamp).toLocaleString()}`;
      logEl.appendChild(ts);
    }
  }

  show('executionCard');
}

// ── Map ────────────────────────────────────────────────────────────────────
function populateMap(coords) {
  if (!coords || coords.lat == null || coords.lon == null) return;

  document.getElementById('coordLat').textContent = coords.lat.toFixed(5);
  document.getElementById('coordLon').textContent = coords.lon.toFixed(5);
  document.getElementById('mapEmpty').style.display   = 'none';
  document.getElementById('mapContent').style.display = 'block';

  // Destroy old map if any
  if (state.leafletMap) {
    state.leafletMap.remove();
    state.leafletMap   = null;
    state.leafletMarker = null;
  }

  // Small delay to let DOM show the container
  setTimeout(() => {
    const map = L.map('leafletMap', {
      center: [coords.lat, coords.lon],
      zoom: 10,
      zoomControl: true,
      scrollWheelZoom: false,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    // Custom red marker icon
    const icon = L.divIcon({
      html: `<div style="
        width:18px;height:18px;
        background:var(--red);
        border:3px solid white;
        border-radius:50%;
        box-shadow:0 0 10px rgba(255,77,77,0.7);
      "></div>`,
      className: '',
      iconAnchor: [9, 9],
    });

    L.marker([coords.lat, coords.lon], { icon }).addTo(map);
    state.leafletMap = map;
  }, 100);
}

// ── Stats ──────────────────────────────────────────────────────────────────
function updateStats() {
  document.getElementById('statIncidents').textContent = state.stats.incidents;
  document.getElementById('statApproved').textContent  = state.stats.approved;
  document.getElementById('statRejected').textContent  = state.stats.rejected;

  if (state.stats.incidents > 0) {
    const avgSec = Math.round(state.stats.totalMs / state.stats.incidents / 1000);
    document.getElementById('statAvgTime').textContent = `${avgSec}s`;
  }
}

// ── History ────────────────────────────────────────────────────────────────
function addToHistory(situation, approved, elapsedMs, threadId) {
  state.history.unshift({ situation, approved, elapsedMs, threadId, time: new Date() });

  const list = document.getElementById('historyList');

  // Remove empty placeholder
  const empty = list.querySelector('.history-empty');
  if (empty) empty.remove();

  const item = document.createElement('div');
  item.className = 'history-item';
  item.innerHTML = `
    <div class="history-item-title">${escHtml(situation.slice(0, 60))}${situation.length > 60 ? '…' : ''}</div>
    <div class="history-item-meta">
      <span class="badge ${approved ? 'badge-ok' : 'badge-warn'}" style="font-size:10px;padding:2px 7px;">
        ${approved ? 'Approved' : 'Rejected'}
      </span>
      <span class="history-item-time">${new Date().toLocaleTimeString('en-US',{hour12:false,hour:'2-digit',minute:'2-digit'})}</span>
    </div>
  `;
  list.prepend(item);
}

// ── Utilities ──────────────────────────────────────────────────────────────
function show(id) { document.getElementById(id).style.display = 'block'; }
function capitalize(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; }
function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
