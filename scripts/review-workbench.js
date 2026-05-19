(function () {
  'use strict';

  const FILE_TYPE_LABELS = {
    markdown: 'markdown',
    text: 'text',
    html: 'html',
    javascript: 'javascript',
    jsx: 'jsx',
    typescript: 'typescript',
    tsx: 'tsx',
    python: 'python',
  };

  const SAMPLE_DOCS = [
    {
      id: 'sample-circle',
      name: 'circle-week1-draft.md',
      fileType: 'markdown',
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
      fileType: 'markdown',
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
      fileType: 'markdown',
      status: 'Inbox',
      destination: '',
      notes: '',
      content: `# Review Workbench — How to use this v0.2

1. Click a document on the left to load it.
2. Edit the text in the center.
3. Pick a status and write notes on the right.
4. Click **Generate Provisional TOC** to scan Markdown headings.
5. Click **Create Placement Map Note** to produce a JSON summary.
6. Use **Open file** to load Markdown, HTML, JS, JSX, TS, TSX, or Python; **Save file** downloads the current editor contents.

Edits, status, destination, and notes are auto-saved to this browser's storage and survive a page refresh. HTML files render in the preview pane. JS/TS/JSX/TSX/Python stay in code view until a runtime or transform pipeline exists.
`,
    },
  ];

  const STORAGE_KEY = 'review-workbench:v1';
  const STORAGE_VERSION = 3;

  function deriveFileType(name) {
    const lower = String(name || '').toLowerCase();
    if (lower.endsWith('.md') || lower.endsWith('.markdown')) return 'markdown';
    if (lower.endsWith('.html')) return 'html';
    if (lower.endsWith('.jsx')) return 'jsx';
    if (lower.endsWith('.tsx')) return 'tsx';
    if (lower.endsWith('.ts')) return 'typescript';
    if (lower.endsWith('.js')) return 'javascript';
    if (lower.endsWith('.py')) return 'python';
    return 'text';
  }

  function fileMimeType(fileType) {
    return {
      markdown: 'text/markdown',
      text: 'text/plain',
      html: 'text/html',
      javascript: 'text/javascript',
      jsx: 'text/plain',
      typescript: 'text/plain',
      tsx: 'text/plain',
      python: 'text/x-python',
    }[fileType] || 'text/plain';
  }

  function fileTypeLabel(fileType) {
    return FILE_TYPE_LABELS[fileType] || 'text';
  }

  function supportsHeadingScan(fileType) {
    return fileType === 'markdown' || fileType === 'text';
  }

  function editorPlaceholder(fileType) {
    if (fileType === 'html') return '<!DOCTYPE html>\n<html>\n  <head></head>\n  <body></body>\n</html>';
    if (fileType === 'javascript') return '// Write JavaScript here...';
    if (fileType === 'jsx') return 'export default function Example() {\n  return <div>Hello</div>;\n}';
    if (fileType === 'typescript') return 'export type Example = {\n  id: string;\n};';
    if (fileType === 'tsx') return 'export function Example(): JSX.Element {\n  return <div>Hello</div>;\n}';
    if (fileType === 'python') return 'def main():\n    print("Hello")';
    if (fileType === 'text') return 'Write or paste text here...';
    return '# Heading\nWrite or paste Markdown here...';
  }

  function previewMeta(fileType) {
    return fileType === 'html' ? 'sandboxed html preview' : `${fileTypeLabel(fileType)} code view`;
  }

  function previewMessage(fileType) {
    if (fileType === 'html') return '';
    if (fileType === 'markdown' || fileType === 'text') {
      return 'Markdown/text files stay in editor mode here. Use TOC and Placement Map tools below for structure.';
    }
    if (fileType === 'python') {
      return 'Python files open in code view only. Use the backend file catalog endpoints to collect script links and stack inventory.';
    }
    return 'JS/TS/JSX/TSX files open in code view only until a runtime/build transform is added.';
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
          fileType: typeof d.fileType === 'string' ? d.fileType : deriveFileType(d.name),
          status: typeof d.status === 'string' ? d.status : 'Inbox',
          destination: typeof d.destination === 'string' ? d.destination : '',
          notes: typeof d.notes === 'string' ? d.notes : '',
          content: typeof d.content === 'string' ? d.content : '',
          source: d.source === 'file' ? 'file' : undefined,
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
          fileType: d.fileType || deriveFileType(d.name),
          status: d.status || 'Inbox',
          destination: d.destination || '',
          notes: d.notes || '',
          content: d.content || '',
          source: d.source,
        })),
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch {
      // Storage is best-effort only.
    }
  }

  let saveTimer = null;
  function schedulePersist() {
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      saveTimer = null;
      persistActive();
      savePersistedState();
      refreshPreview();
    }, 250);
  }

  const persisted = loadPersistedState();
  const state = {
    docs:
      persisted && persisted.docs.length
        ? persisted.docs
        : SAMPLE_DOCS.map((d) => ({ ...d })),
    activeId: null,
  };
  let initialActiveId =
    persisted && persisted.activeId &&
    state.docs.some((d) => d.id === persisted.activeId)
      ? persisted.activeId
      : null;

  const $ = (id) => document.getElementById(id);
  const els = {
    fileList: $('rwFileList'),
    editor: $('rwEditor'),
    docTitle: $('rwDocTitle'),
    docMeta: $('rwDocMeta'),
    fileKind: $('rwFileKind'),
    previewMeta: $('rwPreviewMeta'),
    previewEmpty: $('rwPreviewEmpty'),
    previewFrame: $('rwPreviewFrame'),
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

  function activeDoc() {
    return state.docs.find((d) => d.id === state.activeId) || null;
  }

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
        <span class="rw-file-status">${escapeHtml(doc.status)} · ${escapeHtml(fileTypeLabel(doc.fileType || deriveFileType(doc.name)))}</span>
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

  function updateDocChrome(doc) {
    const fileType = doc.fileType || deriveFileType(doc.name);
    els.docTitle.textContent = doc.name;
    els.fileKind.textContent = fileTypeLabel(fileType);
    els.docMeta.textContent = doc.source === 'file' ? 'opened from file · auto-saved' : 'auto-saved';
    els.editor.placeholder = editorPlaceholder(fileType);
    els.previewMeta.textContent = previewMeta(fileType);
  }

  function refreshPreview() {
    const doc = activeDoc();
    if (!doc) return;
    const fileType = doc.fileType || deriveFileType(doc.name);
    els.previewMeta.textContent = previewMeta(fileType);
    if (fileType === 'html') {
      els.previewEmpty.hidden = true;
      els.previewFrame.hidden = false;
      els.previewFrame.srcdoc = els.editor.value;
      return;
    }
    els.previewFrame.hidden = true;
    els.previewFrame.srcdoc = '';
    els.previewEmpty.hidden = false;
    els.previewEmpty.textContent = previewMessage(fileType);
  }

  function loadDoc(id) {
    persistActive();
    const doc = state.docs.find((d) => d.id === id);
    if (!doc) return;
    doc.fileType = doc.fileType || deriveFileType(doc.name);
    state.activeId = id;
    savePersistedState();
    els.editor.value = doc.content;
    els.status.value = doc.status || 'Inbox';
    els.destination.value = doc.destination || '';
    els.notes.value = doc.notes || '';
    els.tocList.innerHTML = '<li class="rw-empty">Click <em>Generate Provisional TOC</em> to scan headings.</li>';
    els.mapOutput.textContent = '// Click "Create Placement Map Note" to generate.';
    updateDocChrome(doc);
    refreshPreview();
    renderFileList();
  }

  function persistActive() {
    const doc = activeDoc();
    if (!doc) return;
    doc.content = els.editor.value;
    doc.status = els.status.value;
    doc.destination = els.destination.value;
    doc.notes = els.notes.value;
    doc.fileType = doc.fileType || deriveFileType(doc.name);
  }

  function generateTOC() {
    persistActive();
    const doc = activeDoc();
    const fileType = doc ? doc.fileType || deriveFileType(doc.name) : 'text';
    if (!supportsHeadingScan(fileType)) {
      els.tocList.innerHTML = '<li class="rw-empty">Heading scan is available for Markdown and text files.</li>';
      return [];
    }
    const lines = els.editor.value.split(/\r?\n/);
    const headings = [];
    for (const line of lines) {
      const match = /^(#{1,3})\s+(.+?)\s*#*\s*$/.exec(line);
      if (match) headings.push({ level: match[1].length, text: match[2].trim() });
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

  function generatePlacementMap() {
    persistActive();
    const doc = activeDoc();
    const headings = generateTOC();
    const map = {
      schema: 'placement-map/v0.2',
      generated_at: new Date().toISOString(),
      document: doc ? doc.name : 'Untitled',
      file_type: doc ? doc.fileType || deriveFileType(doc.name) : 'text',
      status: els.status.value,
      future_destination: els.destination.value || null,
      review_notes: els.notes.value || null,
      detected_headings: headings,
      unresolved_questions: [],
    };
    els.mapOutput.textContent = JSON.stringify(map, null, 2);
    return map;
  }

  function openLocalFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
      const id = 'file-' + Date.now();
      const doc = {
        id,
        name: file.name,
        fileType: deriveFileType(file.name),
        status: 'Inbox',
        destination: '',
        notes: '',
        content: String(reader.result || ''),
        source: 'file',
      };
      state.docs.unshift(doc);
      renderFileList();
      loadDoc(id);
      savePersistedState();
    };
    reader.readAsText(file);
  }

  function saveLocalFile() {
    persistActive();
    const doc = activeDoc();
    const name = (doc && doc.name) || 'untitled.txt';
    const fileType = (doc && doc.fileType) || deriveFileType(name);
    const blob = new Blob([els.editor.value], { type: fileMimeType(fileType) });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  document.addEventListener('DOMContentLoaded', () => {
    renderFileList();
    const firstId =
      initialActiveId || (state.docs.length ? state.docs[0].id : null);
    if (firstId) loadDoc(firstId);

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

    [els.editor, els.status, els.destination, els.notes].forEach((el) => {
      el.addEventListener('change', () => {
        persistActive();
        savePersistedState();
        refreshPreview();
      });
      el.addEventListener('input', schedulePersist);
    });

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
