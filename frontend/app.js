/**
 * StyleSync AI Mail — Frontend Application Logic
 * ================================================
 * Handles API calls, UI rendering, streaming animations,
 * Chart.js analytics, and the human-review workflow.
 */

const API = 'http://localhost:5000/api';

// ── State ───────────────────────────────────────────────────────────────────
let allEmails = [];
let selectedEmailId = null;
let currentFilter = 'all';
let intentChart = null;
let urgencyChart = null;

// ── DOM References ──────────────────────────────────────────────────────────
const emailList         = document.getElementById('emailList');
const emptyState        = document.getElementById('emptyState');
const emailDetail       = document.getElementById('emailDetail');
const emailFrom         = document.getElementById('emailFrom');
const emailSubject      = document.getElementById('emailSubject');
const emailTime         = document.getElementById('emailTime');
const emailBody         = document.getElementById('emailBody');
const emailStatusBadge  = document.getElementById('emailStatusBadge');
const senderAvatar      = document.getElementById('senderAvatar');
const classificationCard= document.getElementById('classificationCard');
const intentLabel       = document.getElementById('intentLabel');
const intentIconLarge   = document.getElementById('intentIconLarge');
const urgencyChip       = document.getElementById('urgencyChip');
const sentimentChip     = document.getElementById('sentimentChip');
const modeChip          = document.getElementById('modeChip');
const confCircle        = document.getElementById('confCircle');
const confText          = document.getElementById('confText');
const confidenceBars    = document.getElementById('confidenceBars');
const draftCard         = document.getElementById('draftCard');
const draftTextDisplay  = document.getElementById('draftTextDisplay');
const draftEditor       = document.getElementById('draftEditor');
const ragContextText    = document.getElementById('ragContextText');
const actionSummaryText = document.getElementById('actionSummaryText');
const processBtn        = document.getElementById('processBtn');
const processBtnText    = document.getElementById('processBtnText');
const approveBtn        = document.getElementById('approveBtn');
const rejectBtn         = document.getElementById('rejectBtn');
const copyDraftBtn      = document.getElementById('copyDraftBtn');
const processingOverlay = document.getElementById('processingOverlay');
const processingTitle   = document.getElementById('processingTitle');
const modeBadge         = document.getElementById('modeBadge');
const modeText          = document.getElementById('modeText');
const ragBadge          = document.getElementById('ragBadge');
const ragCount          = document.getElementById('ragCount');
const statPending       = document.getElementById('statPending');
const statApproved      = document.getElementById('statApproved');

// ── Init ─────────────────────────────────────────────────────────────────────
(async function init() {
  await fetchStatus();
  await loadEmails();
  setupTabs();
  setupFilters();
  setupSearch();
  document.getElementById('resetBtn').addEventListener('click', resetDemo);
  document.getElementById('processAllBtn').addEventListener('click', processAllEmails);
  processBtn.addEventListener('click', () => processEmail(selectedEmailId));
  approveBtn.addEventListener('click', approveEmail);
  rejectBtn.addEventListener('click', rejectEmail);
  copyDraftBtn.addEventListener('click', copyDraft);
})();

// ── API Helpers ──────────────────────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
  return res.json();
}

// ── Status ────────────────────────────────────────────────────────────────────
async function fetchStatus() {
  try {
    const data = await apiFetch('/status');
    modeText.textContent = data.demo_mode ? 'Demo Mode' : 'Live (LLM)';
    if (!data.demo_mode) {
      modeBadge.style.borderColor = 'rgba(16,185,129,0.4)';
      modeBadge.style.color = '#10b981';
      modeBadge.querySelector('.badge-dot').style.background = '#10b981';
      modeBadge.querySelector('.badge-dot').style.boxShadow = '0 0 6px #10b981';
    }
    ragCount.textContent = data.rag.count > 0 ? `${data.rag.count} chunks` : 'initializing';
  } catch (e) {
    modeText.textContent = 'Server offline';
    modeBadge.style.color = '#ef4444';
    showToast('⚠️ Cannot connect to server. Make sure app.py is running on port 5000.', 'error', 6000);
  }
}

// ── Load Emails ──────────────────────────────────────────────────────────────
async function loadEmails() {
  try {
    allEmails = await apiFetch('/emails');
    renderEmailList();
    updateInboxStats();
  } catch (e) {
    emailList.innerHTML = `<div style="padding:20px;text-align:center;color:var(--text-muted);font-size:13px;">⚠️ Could not load emails. Is the server running?</div>`;
  }
}

function renderEmailList(filter = currentFilter, searchQuery = '') {
  let filtered = allEmails;

  if (filter !== 'all') {
    filtered = filtered.filter(e => e.status === filter);
  }

  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(e =>
      e.sender.toLowerCase().includes(q) ||
      e.subject.toLowerCase().includes(q) ||
      (e.intent && e.intent.toLowerCase().includes(q))
    );
  }

  if (filtered.length === 0) {
    emailList.innerHTML = `<div style="padding:30px;text-align:center;color:var(--text-muted);font-size:13px;">No emails found</div>`;
    return;
  }

  emailList.innerHTML = filtered.map(email => `
    <div class="email-card ${email.id === selectedEmailId ? 'active' : ''}"
         data-id="${email.id}"
         style="--intent-color: ${email.color || '#6366f1'};"
         onclick="selectEmail('${email.id}')">
      <div class="card-top">
        <div class="card-sender">${escHtml(extractName(email.sender))}</div>
        <div class="card-time">${formatTime(email.timestamp)}</div>
      </div>
      <div class="card-subject">${escHtml(email.subject)}</div>
      <div class="card-bottom">
        ${email.intent
          ? `<div class="intent-badge" style="background:${email.color}88;">${email.icon} ${email.intent}</div>`
          : `<div class="intent-badge" style="background:rgba(255,255,255,0.06);color:var(--text-muted);">📧 Unclassified</div>`
        }
        <div class="status-dot status-${email.status}" title="${email.status}"></div>
      </div>
    </div>
  `).join('');
}

function updateInboxStats() {
  const pending  = allEmails.filter(e => e.status === 'pending').length;
  const approved = allEmails.filter(e => e.status === 'approved').length;
  statPending.textContent  = `${pending} pending`;
  statApproved.textContent = `${approved} approved`;
}

// ── Select Email ──────────────────────────────────────────────────────────────
async function selectEmail(id) {
  selectedEmailId = id;
  renderEmailList(currentFilter, document.getElementById('searchInput').value);

  emptyState.classList.add('hidden');
  emailDetail.classList.remove('hidden');

  // Load full detail
  try {
    const data = await apiFetch(`/email/${id}`);
    renderEmailDetail(data);
  } catch (e) {
    showToast('Failed to load email details', 'error');
  }
}

function renderEmailDetail(data) {
  const { email, classification, draft, status, intent_color, intent_icon } = data;

  // Header
  const name = extractName(email.sender);
  senderAvatar.textContent = name.charAt(0).toUpperCase();
  senderAvatar.style.background = `linear-gradient(135deg, ${intent_color || '#6366f1'}, ${intent_color || '#8b5cf6'})`;
  emailFrom.textContent    = email.sender;
  emailSubject.textContent = email.subject;
  emailTime.textContent    = formatDateTime(email.timestamp);

  // Status badge
  const statusStyles = {
    pending:   { bg: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)',    label: '⏳ Pending' },
    reviewing: { bg: 'rgba(245,158,11,0.15)',  color: 'var(--accent-amber)', label: '🔍 In Review' },
    approved:  { bg: 'rgba(16,185,129,0.15)',  color: 'var(--accent-green)', label: '✅ Approved' },
    rejected:  { bg: 'rgba(239,68,68,0.15)',   color: 'var(--accent-red)',   label: '❌ Rejected' },
  };
  const ss = statusStyles[status] || statusStyles.pending;
  emailStatusBadge.style.background = ss.bg;
  emailStatusBadge.style.color = ss.color;
  emailStatusBadge.textContent = ss.label;

  // Body
  emailBody.textContent = email.body;

  // Classification
  if (classification) {
    classificationCard.classList.remove('hidden');
    intentLabel.textContent    = classification.primary_intent;
    intentIconLarge.textContent = intent_icon || '📧';
    urgencyChip.textContent    = classification.urgency || '—';
    sentimentChip.textContent  = classification.sentiment || '—';
    modeChip.textContent       = classification.mode === 'demo' ? 'Demo' : 'Live';

    // Urgency color
    const urgencyColors = { low: '#10b981', medium: '#f59e0b', high: '#f97316', critical: '#ef4444' };
    urgencyChip.style.color = urgencyColors[classification.urgency] || 'var(--accent-amber)';
    urgencyChip.style.borderColor = (urgencyColors[classification.urgency] || '#f59e0b') + '55';
    urgencyChip.style.background  = (urgencyColors[classification.urgency] || '#f59e0b') + '15';

    // Confidence ring
    const scores = classification.confidence_scores || {};
    const maxConf = Math.max(...Object.values(scores));
    const dashArray = 125.66;
    const offset = dashArray - (dashArray * maxConf);
    confCircle.style.strokeDashoffset = offset;
    confText.textContent = `${Math.round(maxConf * 100)}%`;

    // Confidence bars
    const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
    const intentColors = {
      'Order Status': '#6366f1', 'Return/Exchange': '#f59e0b', 'Sizing Help': '#10b981',
      'Complaint': '#ef4444', 'Compliment': '#22d3ee', 'Shipping Delay': '#f97316',
      'Payment Issue': '#ec4899', 'General Inquiry': '#8b5cf6',
    };

    confidenceBars.innerHTML = sorted.map(([intent, score]) => `
      <div class="conf-bar-row">
        <div class="conf-bar-label">${intent}</div>
        <div class="conf-bar-track">
          <div class="conf-bar-fill" style="width:${Math.round(score*100)}%;background:${intentColors[intent]||'#6366f1'};"></div>
        </div>
        <div class="conf-bar-value">${Math.round(score*100)}%</div>
      </div>
    `).join('');
  } else {
    classificationCard.classList.add('hidden');
  }

  // Draft
  if (draft) {
    draftCard.classList.remove('hidden');
    draftTextDisplay.innerHTML = escHtml(draft.draft_text) + '<span class="typing-cursor" style="display:none"></span>';
    draftEditor.value = draft.draft_text;
    ragContextText.textContent = draft.rag_context_used || 'No context retrieved.';
    actionSummaryText.textContent = draft.action_summary || '—';
  } else {
    draftCard.classList.add('hidden');
    draftEditor.value = '';
  }

  // Process button state
  if (status === 'approved') {
    processBtn.textContent = '✅ Already Approved';
    processBtn.disabled = true;
  } else if (status === 'rejected') {
    processBtnText.textContent = '🔄 Re-classify & Draft';
    processBtn.disabled = false;
  } else if (draft) {
    processBtnText.textContent = '🔄 Regenerate Reply';
    processBtn.disabled = false;
  } else {
    processBtnText.textContent = 'Classify & Draft Reply';
    processBtn.disabled = false;
  }
}

// ── Process Email ─────────────────────────────────────────────────────────────
async function processEmail(id) {
  if (!id) return;
  showProcessingOverlay();

  try {
    // Step 1
    setProcessStep(1);
    await sleep(400);
    setProcessStep(2);
    await sleep(300);
    setProcessStep(3);

    const data = await apiFetch(`/process/${id}`, { method: 'POST' });

    hideProcessingOverlay();

    // Update local state
    const idx = allEmails.findIndex(e => e.id === id);
    if (idx >= 0) {
      allEmails[idx].status   = 'reviewing';
      allEmails[idx].intent   = data.classification.primary_intent;
      allEmails[idx].urgency  = data.classification.urgency;
      allEmails[idx].sentiment= data.classification.sentiment;
      allEmails[idx].confidence = Math.max(...Object.values(data.classification.confidence_scores));
      allEmails[idx].color    = data.intent_color;
      allEmails[idx].icon     = data.intent_icon;
    }

    renderEmailList(currentFilter, document.getElementById('searchInput').value);
    updateInboxStats();

    // Animate draft
    classificationCard.classList.remove('hidden');
    draftCard.classList.remove('hidden');

    intentLabel.textContent = data.classification.primary_intent;
    intentIconLarge.textContent = data.intent_icon;
    urgencyChip.textContent  = data.classification.urgency;
    sentimentChip.textContent = data.classification.sentiment;
    modeChip.textContent = data.classification.mode === 'demo' ? 'Demo' : 'Live';

    const maxConf = Math.max(...Object.values(data.classification.confidence_scores));
    confCircle.style.strokeDashoffset = 125.66 - (125.66 * maxConf);
    confText.textContent = `${Math.round(maxConf * 100)}%`;

    ragContextText.textContent  = data.draft.rag_context_used;
    actionSummaryText.textContent = data.draft.action_summary;

    // Streaming text animation
    await typewriterEffect(draftTextDisplay, data.draft.draft_text);
    draftEditor.value = data.draft.draft_text;

    processBtnText.textContent = '🔄 Regenerate Reply';
    showToast('✨ AI draft generated successfully!', 'success');

    // Refresh confidence bars
    const fullData = await apiFetch(`/email/${id}`);
    renderEmailDetail(fullData);

  } catch (e) {
    hideProcessingOverlay();
    showToast(`Error: ${e.message}`, 'error');
  }
}

async function processAllEmails() {
  const pending = allEmails.filter(e => e.status === 'pending');
  if (pending.length === 0) { showToast('No pending emails to process', 'info'); return; }

  showToast(`🤖 Processing ${pending.length} emails...`, 'info', 3000);

  for (const email of pending) {
    try {
      showProcessingOverlay(`Processing ${email.id}...`);
      setProcessStep(1);
      await sleep(200);
      setProcessStep(2);
      await sleep(150);
      setProcessStep(3);
      await apiFetch(`/process/${email.id}`, { method: 'POST' });
    } catch (e) {
      console.warn(`Failed to process ${email.id}:`, e);
    }
  }

  hideProcessingOverlay();
  await loadEmails();
  showToast(`✅ All emails processed!`, 'success');
  updateAnalytics();
}

// ── Approve / Reject ─────────────────────────────────────────────────────────
async function approveEmail() {
  if (!selectedEmailId) return;
  const editedText = draftEditor.value.trim();

  try {
    await apiFetch(`/approve/${selectedEmailId}`, {
      method: 'POST',
      body: JSON.stringify({ edited_text: editedText }),
    });

    const idx = allEmails.findIndex(e => e.id === selectedEmailId);
    if (idx >= 0) allEmails[idx].status = 'approved';

    renderEmailList(currentFilter, document.getElementById('searchInput').value);
    updateInboxStats();

    // Reload detail
    const data = await apiFetch(`/email/${selectedEmailId}`);
    renderEmailDetail(data);

    showToast('✅ Email approved and marked as sent!', 'success');
    updateAnalytics();

  } catch (e) {
    showToast(`Approval failed: ${e.message}`, 'error');
  }
}

async function rejectEmail() {
  if (!selectedEmailId) return;
  try {
    await apiFetch(`/reject/${selectedEmailId}`, {
      method: 'POST',
      body: JSON.stringify({ reason: 'Manually rejected by reviewer' }),
    });

    const idx = allEmails.findIndex(e => e.id === selectedEmailId);
    if (idx >= 0) {
      allEmails[idx].status  = 'rejected';
      allEmails[idx].intent  = null;
      allEmails[idx].color   = '#666';
    }

    renderEmailList(currentFilter, document.getElementById('searchInput').value);
    updateInboxStats();

    const data = await apiFetch(`/email/${selectedEmailId}`);
    renderEmailDetail(data);

    showToast('❌ Draft rejected. You can re-process this email.', 'info');
    updateAnalytics();

  } catch (e) {
    showToast(`Reject failed: ${e.message}`, 'error');
  }
}

function copyDraft() {
  const text = draftEditor.value || draftTextDisplay.innerText;
  navigator.clipboard.writeText(text).then(() => {
    showToast('📋 Draft copied to clipboard!', 'success', 2000);
  });
}

// ── Analytics ─────────────────────────────────────────────────────────────────
async function updateAnalytics() {
  try {
    const data = await apiFetch('/analytics');

    document.getElementById('anaTotalEmails').textContent = data.total_emails;
    document.getElementById('anaApproved').textContent   = data.approved;
    document.getElementById('anaPending').textContent    = data.pending + data.total_emails - data.processed;
    document.getElementById('anaRejected').textContent   = data.rejected;

    // Intent Chart
    const intents = data.intent_distribution;
    const intentLabels = intents.map(i => i.intent);
    const intentData   = intents.map(i => i.count);
    const intentColors = intents.map(i => i.color + 'cc');
    const intentBorders= intents.map(i => i.color);

    if (intentChart) intentChart.destroy();
    const ctx1 = document.getElementById('intentChart').getContext('2d');
    intentChart = new Chart(ctx1, {
      type: 'doughnut',
      data: {
        labels: intentLabels,
        datasets: [{
          data: intentData,
          backgroundColor: intentColors,
          borderColor: intentBorders,
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(14,14,26,0.95)',
            titleColor: '#f0f0ff',
            bodyColor: '#9898b8',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
          }
        },
        cutout: '65%',
      }
    });

    // Urgency chart
    const urg = data.urgency_distribution;
    const sent = data.sentiment_distribution;

    if (urgencyChart) urgencyChart.destroy();
    const ctx2 = document.getElementById('urgencyChart').getContext('2d');
    urgencyChart = new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: ['Low', 'Medium', 'High', 'Critical', 'Positive', 'Neutral', 'Negative', 'Very Neg'],
        datasets: [{
          label: 'Count',
          data: [
            urg.low || 0, urg.medium || 0, urg.high || 0, urg.critical || 0,
            sent.positive || 0, sent.neutral || 0, sent.negative || 0, sent.very_negative || 0,
          ],
          backgroundColor: [
            '#10b981cc','#f59e0bcc','#f97316cc','#ef4444cc',
            '#22d3eecc','#6366f1cc','#f59e0bcc','#ec4899cc',
          ],
          borderRadius: 6,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(14,14,26,0.95)',
            titleColor: '#f0f0ff',
            bodyColor: '#9898b8',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#5a5a7a', font: { size: 10 } } },
          y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#5a5a7a', font: { size: 10 } }, beginAtZero: true },
        }
      }
    });

    // Intent Legend
    const legend = document.getElementById('intentLegend');
    legend.innerHTML = intents.map(i => `
      <div class="legend-item">
        <div class="legend-dot" style="background:${i.color}"></div>
        ${i.icon} ${i.intent}: <strong>${i.count}</strong>
      </div>
    `).join('');

  } catch (e) {
    console.error('Analytics error:', e);
  }
}

// ── Prompt Templates ──────────────────────────────────────────────────────────
async function loadPromptTemplates() {
  const container = document.getElementById('promptsList');
  try {
    const templates = await apiFetch('/prompt-templates');
    container.innerHTML = templates.map(t => `
      <div class="prompt-card" id="prompt-${t.id}">
        <div class="prompt-card-header" onclick="togglePrompt('${t.id}')">
          <span class="prompt-id">${t.id}</span>
          <span class="prompt-name">${t.name}</span>
          <span class="prompt-model">${t.model}</span>
          <svg class="prompt-chevron" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </div>
        <div class="prompt-body">
          <div class="prompt-section">
            <div class="prompt-section-label">Purpose</div>
            <p>${escHtml(t.purpose)}</p>
          </div>
          <div class="prompt-section">
            <div class="prompt-section-label">Input Variables</div>
            <div class="vars">${t.variables.map(v => `<span class="var-pill">${escHtml(v)}</span>`).join('')}</div>
          </div>
          <div class="prompt-section">
            <div class="prompt-section-label">Output Format</div>
            <p>${escHtml(t.output_format)}</p>
          </div>
          <div class="prompt-section">
            <div class="prompt-section-label">Example Input</div>
            <div class="prompt-code">${escHtml(t.example_input)}</div>
          </div>
          <div class="prompt-section">
            <div class="prompt-section-label">Example Output</div>
            <div class="prompt-code">${escHtml(t.example_output)}</div>
          </div>
          <div class="prompt-section">
            <div class="prompt-section-label">System Prompt</div>
            <div class="prompt-code">${escHtml(t.system_prompt)}</div>
          </div>
          <div class="prompt-section">
            <div class="prompt-section-label">User Prompt Template</div>
            <div class="prompt-code">${escHtml(t.user_prompt)}</div>
          </div>
        </div>
      </div>
    `).join('');
  } catch (e) {
    container.innerHTML = `<p style="color:var(--text-muted);font-size:13px;">Could not load prompt templates: ${e.message}</p>`;
  }
}

function togglePrompt(id) {
  const card = document.getElementById(`prompt-${id}`);
  card.classList.toggle('open');
}

// ── Tabs ──────────────────────────────────────────────────────────────────────
function setupTabs() {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.tab;
      document.getElementById(target).classList.add('active');

      if (target === 'analytics') updateAnalytics();
      if (target === 'promptDocs') loadPromptTemplates();
    });
  });
}

// ── Filters ──────────────────────────────────────────────────────────────────
function setupFilters() {
  document.querySelectorAll('.filter-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.filter;
      renderEmailList(currentFilter, document.getElementById('searchInput').value);
    });
  });
}

// ── Search ────────────────────────────────────────────────────────────────────
function setupSearch() {
  document.getElementById('searchInput').addEventListener('input', e => {
    renderEmailList(currentFilter, e.target.value);
  });
}

// ── Reset Demo ────────────────────────────────────────────────────────────────
async function resetDemo() {
  try {
    await apiFetch('/reset', { method: 'POST' });
    selectedEmailId = null;
    emptyState.classList.remove('hidden');
    emailDetail.classList.add('hidden');
    await loadEmails();
    showToast('🔄 Demo reset — all emails set to pending', 'info');
  } catch (e) {
    showToast('Reset failed', 'error');
  }
}

// ── Processing Overlay ────────────────────────────────────────────────────────
function showProcessingOverlay(title = 'Classifying Intent...') {
  processingTitle.textContent = title;
  document.querySelectorAll('.proc-step').forEach(s => {
    s.classList.remove('active', 'done');
  });
  processingOverlay.classList.remove('hidden');
}

function hideProcessingOverlay() {
  // Mark all steps done briefly
  document.querySelectorAll('.proc-step').forEach(s => s.classList.add('done'));
  setTimeout(() => {
    processingOverlay.classList.add('hidden');
  }, 300);
}

function setProcessStep(step) {
  const steps = document.querySelectorAll('.proc-step');
  steps.forEach((s, i) => {
    if (i < step - 1) { s.classList.remove('active'); s.classList.add('done'); }
    else if (i === step - 1) { s.classList.add('active'); s.classList.remove('done'); }
    else { s.classList.remove('active', 'done'); }
  });
  const titles = ['Analyzing email content...', 'Retrieving knowledge base context...', 'Generating AI draft reply...'];
  processingTitle.textContent = titles[step - 1] || 'Processing...';
}

// ── Typewriter Animation ──────────────────────────────────────────────────────
async function typewriterEffect(el, text, speed = 8) {
  el.innerHTML = '<span class="typing-cursor"></span>';
  const cursor = el.querySelector('.typing-cursor');

  let displayed = '';
  for (let i = 0; i < text.length; i++) {
    displayed += text[i];
    cursor.insertAdjacentText('beforebegin', text[i]);
    if (i % 3 === 0) await sleep(speed);
  }
  cursor.style.display = 'none';
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function showToast(msg, type = 'info', duration = 4000) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span class="toast-icon">${icons[type] || 'ℹ️'}</span><span>${msg}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('removing');
    setTimeout(() => toast.remove(), 280);
  }, duration);
}

// ── Utility ──────────────────────────────────────────────────────────────────
function escHtml(str) {
  return String(str)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function extractName(email) {
  const local = email.split('@')[0];
  return local.replace(/[._\-0-9]/g, ' ').split(' ').filter(Boolean)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ').trim() || email;
}

function formatTime(ts) {
  const d = new Date(ts);
  const now = new Date();
  const diff = now - d;
  if (diff < 3600000) return `${Math.floor(diff/60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff/3600000)}h ago`;
  return d.toLocaleDateString('en-PK', { day:'numeric', month:'short' });
}

function formatDateTime(ts) {
  return new Date(ts).toLocaleString('en-PK', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
