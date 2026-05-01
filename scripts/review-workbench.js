(function () {
  'use strict';

  const SAMPLE_DOCS = [
    {
      id: 'sample-circle',
      name: 'circle-week1-draft.md',
      status: 'Active Review',
      destination: 'data/obsidian-ready/circle-week1.md',
      notes: '',
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
      content: `# Review Workbench — How to use this v0.1

1. Click a document on the left to load it.
2. Edit the text in the center.
3. Pick a status and write notes on the right.
4. Click **Generate Provisional TOC** to scan headings.
5. Click **Create Placement Map Note** to produce a JSON summary.
6. Use **Open .md** to load a file from your computer; **Save .md** to download the editor as a file.

Nothing is written to disk automatically. Edits live in this browser tab until you save.
`,
    },
  ];

  const state = {
    docs: SAMPLE_DOCS.map((d) => ({ ...d })),
    activeId: null,
  };

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
  };

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

  function loadDoc(id) {
    persistActive();
    const doc = state.docs.find((d) => d.id === id);
    if (!doc) return;
    state.activeId = id;
    els.editor.value = doc.content;
    els.docTitle.textContent = doc.name;
    els.docMeta.textContent = doc.source === 'file' ? 'opened from file' : 'browser-memory';
    els.status.value = doc.status || 'Inbox';
    els.destination.value = doc.destination || '';
    els.notes.value = doc.notes || '';
    els.tocList.innerHTML = '<li class="rw-empty">Click <em>Generate Provisional TOC</em> to scan headings.</li>';
    els.mapOutput.textContent = '// Click "Create Placement Map Note" to generate.';
    renderFileList();
  }

  function persistActive() {
    if (!state.activeId) return;
    const doc = state.docs.find((d) => d.id === state.activeId);
    if (!doc) return;
    doc.content = els.editor.value;
    doc.status = els.status.value;
    doc.destination = els.destination.value;
    doc.notes = els.notes.value;
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
    const map = {
      schema: 'placement-map/v0.1',
      generated_at: new Date().toISOString(),
      document: doc ? doc.name : 'Untitled',
      status: els.status.value,
      future_destination: els.destination.value || null,
      review_notes: els.notes.value || null,
      detected_headings: headings,
      unresolved_questions: [],
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
      };
      state.docs.unshift(doc);
      renderFileList();
      loadDoc(id);
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
    if (state.docs.length) loadDoc(state.docs[0].id);

    els.genTocBtn.addEventListener('click', generateTOC);
    els.genMapBtn.addEventListener('click', generatePlacementMap);

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

    [els.editor, els.status, els.destination, els.notes].forEach((el) =>
      el.addEventListener('change', persistActive)
    );
  });
})();
