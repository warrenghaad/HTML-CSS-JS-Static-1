(function () {
  'use strict';

  const PROVISIONAL_THRESHOLD = 0.7;
  const PROVISIONAL_REVIEW_DAYS = 14;

  const SAMPLE_DOCS = [
    {
      id: 'sample-circle',
      name: 'circle-week1-draft.md',
      status: 'Active Review',
      destination: 'data/obsidian-ready/circle-week1.md',
      notes: '',
      validationIssues: [
        {
          id: 'issue-circle-evidence',
          claim: 'Wheel-origin artifact linkage needs one primary source citation.',
          likelihood: 0.84,
          validationMode: 'Deferred',
          clearanceQuestion: 'Which single source citation confirms the wheel-origin claim in this lesson?',
          clearanceAnswer: '',
          critical: false,
          reviewDue: '',
          resolved: false,
        },
      ],
      content: `# Circle — Week 1 (Shamash)

## B1 Bridge Review
Connects to Day A introduction of equidistance.

## B2 Math Proof
All points on a circle are equidistant from the center.

### Sub-proof: compass construction
A compass enforces equidistance by construction.

## B3 STEM History
Mesopotamian use of the wheel and circular pottery.

## B4 Cultural Connection
Shamash, sun god, and the disk symbol.

## B5 Cumulative Synthesis
(First element — no prior elements to chain.)

## B6 Engineering Activity
Build a string-and-pin compass.

## B7 Advanced Application
Estimate the area of irregular shapes by inscribing circles.

## B8 Reflection / Assessment
What did we learn about equidistance?
`,
    },
    {
      id: 'sample-star',
      name: 'star-week2-fragment.md',
      status: 'Fragment',
      destination: '',
      notes: 'Need to clarify 8-fold vs 4-fold symmetry framing for Grade 3.',
      validationIssues: [
        {
          id: 'issue-star-g3',
          claim: 'Grade 3 language may still be too abstract for 8-fold symmetry.',
          likelihood: 0.62,
          validationMode: 'Blocking',
          clearanceQuestion: 'What exact sentence will explain 8-fold symmetry to Grade 3 without abstraction?',
          clearanceAnswer: '',
          critical: true,
          reviewDue: '',
          resolved: false,
        },
      ],
      content: `# 8-Pointed Star — Week 2 (Ishtar)

## Open Questions
- How do we explain 8-fold symmetry to Grade 3?
- Which artifact image leads the lesson?

## Notes
Radial symmetry as repeated rotation.
`,
    },
    {
      id: 'sample-readme',
      name: 'workbench-readme.md',
      status: 'Inbox',
      destination: '',
      notes: '',
      validationIssues: [],
      content: `# Review Workbench — How to use this v0.1

1. Click a document on the left to load it.
2. Edit the text in the center.
3. Pick a status and write notes on the right.
4. Click **Generate Provisional TOC** to scan headings.
5. Click **Create Placement Map Note** to produce a JSON summary.
6. Use **Open .md** to load a file from your computer; **Save .md** to download the editor as a file.

Edits, status, destination, and notes are auto-saved to this browser's storage and survive a page refresh. Nothing is written to disk on the server — use **Save .md** to export a file to your computer.
`,
    },
  ];

  // -------- Persistence (localStorage) --------
  const STORAGE_KEY = 'review-workbench:v1';
  const STORAGE_VERSION = 3;

  function createIssueId() {
    return 'issue-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
  }

  function autoClearanceQuestion(claim) {
    const trimmed = String(claim || '').trim();
    if (!trimmed) return 'What single answer would resolve this uncertainty?';
    return `What single answer would resolve this uncertainty: "${trimmed}"?`;
  }

  function toNumber(value, fallback) {
    const n = Number(value);
    if (!Number.isFinite(n)) return fallback;
    return Math.min(1, Math.max(0, n));
  }

  function normalizeIssue(raw) {
    const claim = typeof raw.claim === 'string' ? raw.claim : '';
    const clearanceQuestion =
      typeof raw.clearanceQuestion === 'string' && raw.clearanceQuestion.trim()
        ? raw.clearanceQuestion
        : autoClearanceQuestion(claim);
    const clearanceAnswer = typeof raw.clearanceAnswer === 'string' ? raw.clearanceAnswer : '';
    return {
      id: typeof raw.id === 'string' ? raw.id : createIssueId(),
      claim,
      likelihood: toNumber(raw.likelihood, 0.5),
      validationMode: raw.validationMode === 'Blocking' ? 'Blocking' : 'Deferred',
      clearanceQuestion,
      clearanceAnswer,
      critical: Boolean(raw.critical),
      reviewDue: typeof raw.reviewDue === 'string' ? raw.reviewDue : '',
      resolved: clearanceAnswer.trim().length > 0 || Boolean(raw.resolved),
    };
  }

  function loadPersistedState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || parsed.version !== STORAGE_VERSION) return null;
      if (!Array.isArray(parsed.docs)) return null;
      const docs = parsed.docs
        .filter((d) => d && typeof d.id === 'string' && typeof d.name === 'string')
        .map((d) => ({
          id: d.id,
          name: d.name,
          status: typeof d.status === 'string' ? d.status : 'Inbox',
          destination: typeof d.destination === 'string' ? d.destination : '',
          notes: typeof d.notes === 'string' ? d.notes : '',
          content: typeof d.content === 'string' ? d.content : '',
          source: d.source === 'file' ? 'file' : undefined,
          validationIssues: Array.isArray(d.validationIssues) ? d.validationIssues.map(normalizeIssue) : [],
        }));
      return {
        docs,
        activeId: typeof parsed.activeId === 'string' ? parsed.activeId : null,
      };
    } catch {
      return null;
    }
  }

  function savePersistedState() {
    try {
      const payload = {
        version: STORAGE_VERSION,
        savedAt: new Date().toISOString(),
        activeId: state.activeId,
        docs: state.docs.map((d) => ({
          id: d.id,
          name: d.name,
          status: d.status || 'Inbox',
          destination: d.destination || '',
          notes: d.notes || '',
          content: d.content || '',
          source: d.source,
          validationIssues: Array.isArray(d.validationIssues)
            ? d.validationIssues.map((issue) => normalizeIssue(issue))
            : [],
        })),
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch {
      // Quota exceeded or storage unavailable — ignore silently so the
      // workbench keeps functioning in-memory.
    }
  }

  let saveTimer = null;
  function schedulePersist() {
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      saveTimer = null;
      persistActive();
      savePersistedState();
      refreshValidationQueue();
    }, 250);
  }

  function createDefaultIssue() {
    return {
      id: createIssueId(),
      claim: '',
      likelihood: 0.7,
      validationMode: 'Deferred',
      clearanceQuestion: 'What single answer would resolve this uncertainty?',
      clearanceAnswer: '',
      critical: false,
      reviewDue: '',
      resolved: false,
    };
  }

  const persisted = loadPersistedState();
  const state = {
    docs:
      persisted && persisted.docs.length
        ? persisted.docs.map((d) => ({ ...d, validationIssues: Array.isArray(d.validationIssues) ? d.validationIssues : [] }))
        : SAMPLE_DOCS.map((d) => ({
            ...d,
            validationIssues: Array.isArray(d.validationIssues) ? d.validationIssues.map(normalizeIssue) : [],
          })),
    activeId: null,
  };
  let initialActiveId =
    persisted && persisted.activeId && state.docs.some((d) => d.id === persisted.activeId)
      ? persisted.activeId
      : null;

  // -------- Element refs --------
  const $ = (id) => document.getElementById(id);
  const els = {
    fileList: $('rwFileList'),
    editor: $('rwEditor'),
    docTitle: $('rwDocTitle'),
    docMeta: $('rwDocMeta'),
    status: $('rwStatus'),
    destination: $('rwDestination'),
    notes: $('rwNotes'),
    tocList: $('rwTocList'),
    mapOutput: $('rwMapOutput'),
    openBtn: $('rwOpenFile'),
    fileInput: $('rwFileInput'),
    saveBtn: $('rwSaveFile'),
    genTocBtn: $('rwGenTOC'),
    genMapBtn: $('rwGenMap'),
    copyMapBtn: $('rwCopyMap'),
    issueList: $('rwIssueList'),
    addIssueBtn: $('rwAddIssue'),
    validationSummary: $('rwValidationSummary'),
    validationQueue: $('rwValidationQueue'),
  };

  function getActiveDoc() {
    return state.docs.find((d) => d.id === state.activeId) || null;
  }

  function summarizeDocValidation(doc) {
    const issues = Array.isArray(doc.validationIssues) ? doc.validationIssues.map(normalizeIssue) : [];
    const unresolved = issues.filter((i) => !i.resolved);
    const unresolvedBlocking = unresolved.filter((i) => i.validationMode === 'Blocking');
    const unresolvedCritical = unresolvedBlocking.filter((i) => i.critical);
    const unresolvedDeferred = unresolved.filter((i) => i.validationMode === 'Deferred');
    const provisionalEligible =
      unresolved.length > 0 &&
      unresolvedBlocking.length === 0 &&
      unresolvedDeferred.every((i) => i.likelihood >= PROVISIONAL_THRESHOLD);
    return {
      total: issues.length,
      resolvedCount: issues.length - unresolved.length,
      unresolved,
      unresolvedBlocking,
      unresolvedCritical,
      provisionalEligible,
      allResolved: issues.length > 0 && unresolved.length === 0,
    };
  }

  function applyValidationPolicy(doc) {
    if (!doc) return;
    doc.validationIssues = (Array.isArray(doc.validationIssues) ? doc.validationIssues : []).map(normalizeIssue);
    const summary = summarizeDocValidation(doc);

    if (summary.provisionalEligible) {
      if (doc.status === 'Canon' || doc.status === 'Canon Candidate') {
        doc.status = 'Provisional Canon';
      }
      summary.unresolved.forEach((issue) => {
        if (!issue.reviewDue) {
          const due = new Date();
          due.setDate(due.getDate() + PROVISIONAL_REVIEW_DAYS);
          issue.reviewDue = due.toISOString().slice(0, 10);
        }
      });
    }

    if (summary.allResolved) {
      if (doc.status === 'Provisional Canon' || doc.status === 'Canon Candidate') {
        doc.status = 'Canon';
      } else if (doc.status !== 'Canon') {
        doc.status = 'Canon Candidate';
      }
    }

    if (summary.unresolvedCritical.length > 0 && (doc.status === 'Canon' || doc.status === 'Provisional Canon')) {
      doc.status = 'Active Review';
    }
  }

  // -------- File list --------
  function renderFileList() {
    els.fileList.innerHTML = '';
    state.docs.forEach((doc) => {
      const li = document.createElement('li');
      li.className = 'rw-file-item' + (doc.id === state.activeId ? ' active' : '');
      li.dataset.id = doc.id;
      li.setAttribute('role', 'button');
      li.setAttribute('tabindex', '0');
      li.setAttribute('aria-pressed', doc.id === state.activeId ? 'true' : 'false');
      li.setAttribute('aria-label', `Load document ${doc.name}, status ${doc.status}`);
      li.innerHTML = `
        <span class="rw-file-name">${escapeHtml(doc.name)}</span>
        <span class="rw-file-status">${escapeHtml(doc.status)}</span>
      `;
      li.addEventListener('click', () => loadDoc(doc.id));
      li.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          loadDoc(doc.id);
        }
      });
      els.fileList.appendChild(li);
    });
  }

  function renderValidationSummary(doc) {
    const summary = summarizeDocValidation(doc);
    if (!summary.total) {
      els.validationSummary.innerHTML = '<span class="rw-tag">No issues</span>';
      return;
    }
    const gate = summary.unresolvedCritical.length > 0
      ? '<span class="rw-tag rw-tag-warning">Blocked</span>'
      : summary.provisionalEligible
      ? '<span class="rw-tag rw-tag-warning">Provisional Allowed</span>'
      : '<span class="rw-tag rw-tag-success">Ready</span>';
    const counts = `${summary.resolvedCount}/${summary.total} resolved`;
    els.validationSummary.innerHTML = `${gate} ${escapeHtml(counts)}`;
  }

  function renderIssues() {
    const doc = getActiveDoc();
    if (!doc) return;
    doc.validationIssues = (Array.isArray(doc.validationIssues) ? doc.validationIssues : []).map(normalizeIssue);

    if (doc.validationIssues.length === 0) {
      els.issueList.innerHTML = '<p class="rw-hint">No issues yet. Add one when a validation question appears.</p>';
      renderValidationSummary(doc);
      return;
    }

    els.issueList.innerHTML = '';
    doc.validationIssues.forEach((issue, index) => {
      const card = document.createElement('div');
      card.className = 'rw-issue-card';
      card.innerHTML = `
        <div class="rw-issue-row">
          <div>
            <label class="rw-label">Claim / uncertainty</label>
            <input class="rw-input" data-field="claim" data-idx="${index}" type="text" value="${escapeHtml(issue.claim)}" placeholder="What needs validation?">
          </div>
          <div>
            <label class="rw-label">Likelihood (0-1)</label>
            <input class="rw-input" data-field="likelihood" data-idx="${index}" type="number" min="0" max="1" step="0.01" value="${issue.likelihood}">
          </div>
        </div>
        <div class="rw-issue-row">
          <div>
            <label class="rw-label">Validation mode</label>
            <select class="rw-input" data-field="validationMode" data-idx="${index}">
              <option ${issue.validationMode === 'Blocking' ? 'selected' : ''}>Blocking</option>
              <option ${issue.validationMode === 'Deferred' ? 'selected' : ''}>Deferred</option>
            </select>
          </div>
          <div class="rw-issue-inline">
            <label class="rw-label" for="critical-${issue.id}">Critical</label>
            <input class="rw-input" id="critical-${issue.id}" data-field="critical" data-idx="${index}" type="checkbox" ${issue.critical ? 'checked' : ''}>
            <span class="rw-tag ${issue.resolved ? 'rw-tag-success' : 'rw-tag-warning'}">${issue.resolved ? 'Resolved' : 'Open'}</span>
          </div>
        </div>
        <div class="rw-issue-row">
          <div>
            <label class="rw-label">Clearance question</label>
            <input class="rw-input" data-field="clearanceQuestion" data-idx="${index}" type="text" value="${escapeHtml(issue.clearanceQuestion)}">
          </div>
          <div>
            <label class="rw-label">Clearance answer</label>
            <input class="rw-input" data-field="clearanceAnswer" data-idx="${index}" type="text" value="${escapeHtml(issue.clearanceAnswer)}" placeholder="Answer resolves issue">
          </div>
        </div>
        <div class="rw-issue-row">
          <div>
            <label class="rw-label">Review due</label>
            <input class="rw-input" data-field="reviewDue" data-idx="${index}" type="date" value="${escapeHtml(issue.reviewDue || '')}">
          </div>
          <div class="rw-issue-actions">
            <button class="btn rw-btn-sm secondary" type="button" data-remove-idx="${index}">Remove</button>
          </div>
        </div>
      `;
      els.issueList.appendChild(card);
    });

    els.issueList.querySelectorAll('[data-field]').forEach((input) => {
      const eventName = input.type === 'checkbox' ? 'change' : 'input';
      input.addEventListener(eventName, (e) => {
        const idx = Number(e.target.dataset.idx);
        const field = e.target.dataset.field;
        const targetIssue = doc.validationIssues[idx];
        if (!targetIssue) return;

        if (field === 'critical') {
          targetIssue.critical = e.target.checked;
        } else if (field === 'likelihood') {
          targetIssue.likelihood = toNumber(e.target.value, targetIssue.likelihood);
        } else {
          targetIssue[field] = e.target.value;
        }

        if (field === 'claim' && !targetIssue.clearanceQuestion.trim()) {
          targetIssue.clearanceQuestion = autoClearanceQuestion(targetIssue.claim);
        }

        targetIssue.resolved = String(targetIssue.clearanceAnswer || '').trim().length > 0;
        applyValidationPolicy(doc);
        els.status.value = doc.status || 'Inbox';
        renderIssues();
        renderFileList();
        savePersistedState();
        refreshValidationQueue();
      });
    });

    els.issueList.querySelectorAll('[data-remove-idx]').forEach((button) => {
      button.addEventListener('click', (e) => {
        const idx = Number(e.currentTarget.dataset.removeIdx);
        doc.validationIssues.splice(idx, 1);
        applyValidationPolicy(doc);
        els.status.value = doc.status || 'Inbox';
        renderIssues();
        renderFileList();
        savePersistedState();
        refreshValidationQueue();
      });
    });

    renderValidationSummary(doc);
  }

  function loadDoc(id) {
    persistActive();
    const doc = state.docs.find((d) => d.id === id);
    if (!doc) return;
    state.activeId = id;
    applyValidationPolicy(doc);
    savePersistedState();
    els.editor.value = doc.content;
    els.docTitle.textContent = doc.name;
    els.docMeta.textContent = doc.source === 'file' ? 'opened from file · auto-saved' : 'auto-saved';
    els.status.value = doc.status || 'Inbox';
    els.destination.value = doc.destination || '';
    els.notes.value = doc.notes || '';
    els.tocList.innerHTML = '<li class="rw-empty">Click <em>Generate Provisional TOC</em> to scan headings.</li>';
    els.mapOutput.textContent = '// Click "Create Placement Map Note" to generate.';
    renderIssues();
    renderFileList();
    refreshValidationQueue();
  }

  function persistActive() {
    if (!state.activeId) return;
    const doc = state.docs.find((d) => d.id === state.activeId);
    if (!doc) return;
    doc.content = els.editor.value;
    doc.status = els.status.value;
    doc.destination = els.destination.value;
    doc.notes = els.notes.value;
    applyValidationPolicy(doc);
  }

  function buildValidationQueue() {
    const rows = [];
    state.docs.forEach((doc) => {
      const issues = Array.isArray(doc.validationIssues) ? doc.validationIssues.map(normalizeIssue) : [];
      issues.forEach((issue) => {
        if (issue.resolved) return;
        rows.push({
          docId: doc.id,
          docName: doc.name,
          mode: issue.validationMode,
          critical: issue.critical,
          likelihood: issue.likelihood,
          question: issue.clearanceQuestion,
          due: issue.reviewDue || '',
        });
      });
    });
    rows.sort((a, b) => {
      const aScore = (a.mode === 'Blocking' ? 2 : 0) + (a.critical ? 1 : 0);
      const bScore = (b.mode === 'Blocking' ? 2 : 0) + (b.critical ? 1 : 0);
      if (aScore !== bScore) return bScore - aScore;
      if (a.due && b.due) return a.due.localeCompare(b.due);
      if (a.due) return -1;
      if (b.due) return 1;
      return b.likelihood - a.likelihood;
    });
    return rows;
  }

  function refreshValidationQueue() {
    const queue = buildValidationQueue();
    if (!queue.length) {
      els.validationQueue.innerHTML = '<li class="rw-empty">No unresolved issues.</li>';
      return;
    }
    els.validationQueue.innerHTML = queue
      .map((item) => {
        const dueText = item.due ? ` · due ${item.due}` : '';
        const modeText = item.critical ? `${item.mode}/Critical` : item.mode;
        return `<li><strong>${escapeHtml(item.docName)}</strong> · ${escapeHtml(modeText)} · p=${item.likelihood.toFixed(2)}${escapeHtml(dueText)}<br>${escapeHtml(item.question || 'No clearance question yet.')}</li>`;
      })
      .join('');
  }

  // -------- TOC generation --------
  function generateTOC() {
    persistActive();
    const lines = els.editor.value.split(/\r?\n/);
    const headings = [];
    for (const line of lines) {
      const m = /^(#{1,3})\s+(.+?)\s*#*\s*$/.exec(line);
      if (m) headings.push({ level: m[1].length, text: m[2].trim() });
    }
    if (headings.length === 0) {
      els.tocList.innerHTML = '<li class="rw-empty">No Markdown headings (<code>#</code>, <code>##</code>, <code>###</code>) found.</li>';
      return headings;
    }
    els.tocList.innerHTML = headings
      .map((h) => `<li class="rw-toc-h${h.level}">${'·'.repeat(h.level)} ${escapeHtml(h.text)}</li>`)
      .join('');
    return headings;
  }

  // -------- Placement map --------
  function generatePlacementMap() {
    persistActive();
    const doc = state.docs.find((d) => d.id === state.activeId);
    const headings = generateTOC();
    const summary = doc ? summarizeDocValidation(doc) : null;
    const unresolved = summary ? summary.unresolved : [];
    const queue = buildValidationQueue();
    const map = {
      schema: 'placement-map/v0.2',
      generated_at: new Date().toISOString(),
      document: doc ? doc.name : 'Untitled',
      status: els.status.value,
      future_destination: els.destination.value || null,
      review_notes: els.notes.value || null,
      detected_headings: headings,
      validation_policy: {
        provisional_threshold: PROVISIONAL_THRESHOLD,
        rule: 'High confidence + non-critical deferred unknowns = Provisional Canon; critical/blocking unknowns stay in Active Review.',
        provisional_review_days: PROVISIONAL_REVIEW_DAYS,
      },
      validation_summary: summary
        ? {
            total_issues: summary.total,
            resolved_issues: summary.resolvedCount,
            unresolved_blocking: summary.unresolvedBlocking.length,
            unresolved_critical: summary.unresolvedCritical.length,
            provisional_eligible: summary.provisionalEligible,
          }
        : null,
      unresolved_questions: unresolved.map((i) => i.clearanceQuestion || autoClearanceQuestion(i.claim)),
      issues: doc ? (doc.validationIssues || []).map((i) => normalizeIssue(i)) : [],
      validation_queue: queue,
    };
    els.mapOutput.textContent = JSON.stringify(map, null, 2);
    return map;
  }

  // -------- File open / save --------
  function openLocalFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
      const id = 'file-' + Date.now();
      const doc = {
        id,
        name: file.name,
        status: 'Inbox',
        destination: '',
        notes: '',
        content: String(reader.result || ''),
        source: 'file',
        validationIssues: [],
      };
      state.docs.unshift(doc);
      renderFileList();
      loadDoc(id);
      savePersistedState();
      refreshValidationQueue();
    };
    reader.readAsText(file);
  }

  function saveLocalFile() {
    persistActive();
    const doc = state.docs.find((d) => d.id === state.activeId);
    const name = (doc && doc.name) || 'untitled.md';
    const blob = new Blob([els.editor.value], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name.endsWith('.md') ? name : name + '.md';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  // -------- Helpers --------
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  // -------- Wire events --------
  document.addEventListener('DOMContentLoaded', () => {
    renderFileList();
    const firstId = initialActiveId || (state.docs.length ? state.docs[0].id : null);
    if (firstId) loadDoc(firstId);

    els.genTocBtn.addEventListener('click', generateTOC);
    els.genMapBtn.addEventListener('click', generatePlacementMap);

    els.addIssueBtn.addEventListener('click', () => {
      const doc = getActiveDoc();
      if (!doc) return;
      doc.validationIssues = Array.isArray(doc.validationIssues) ? doc.validationIssues : [];
      doc.validationIssues.push(createDefaultIssue());
      applyValidationPolicy(doc);
      renderIssues();
      renderFileList();
      savePersistedState();
      refreshValidationQueue();
    });

    els.openBtn.addEventListener('click', () => els.fileInput.click());
    els.fileInput.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      if (file) openLocalFile(file);
      e.target.value = '';
    });
    els.saveBtn.addEventListener('click', saveLocalFile);

    els.copyMapBtn.addEventListener('click', async () => {
      const text = els.mapOutput.textContent || '';
      try {
        await navigator.clipboard.writeText(text);
        els.copyMapBtn.textContent = 'Copied!';
        setTimeout(() => (els.copyMapBtn.textContent = 'Copy'), 1200);
      } catch {
        els.copyMapBtn.textContent = 'Copy failed';
        setTimeout(() => (els.copyMapBtn.textContent = 'Copy'), 1500);
      }
    });

    [els.editor, els.status, els.destination, els.notes].forEach((el) => {
      el.addEventListener('change', () => {
        persistActive();
        savePersistedState();
        renderIssues();
        renderFileList();
        refreshValidationQueue();
      });
      el.addEventListener('input', schedulePersist);
    });

    // Final flush before the tab unloads, in case a debounced save is pending.
    window.addEventListener('beforeunload', () => {
      if (saveTimer) {
        clearTimeout(saveTimer);
        saveTimer = null;
      }
      persistActive();
      savePersistedState();
    });
  });
})();
