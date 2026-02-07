const DocEditor = {
  modal: null,
  currentDocKey: null,
  unsavedChanges: false,

  init() {
    this.createModal();
    this.bindEvents();
  },

  createModal() {
    const overlay = document.createElement('div');
    overlay.id = 'editorOverlay';
    overlay.className = 'editor-overlay';
    overlay.innerHTML = `
      <div class="editor-modal" id="editorModal">
        <div class="editor-topbar">
          <div class="editor-topbar-left">
            <span class="editor-title-label">Editing:</span>
            <input type="text" id="editorDocTitle" class="editor-title-input" placeholder="Document title...">
          </div>
          <div class="editor-topbar-right">
            <button class="editor-btn editor-btn-secondary" id="editorVersionsBtn">Versions</button>
            <button class="editor-btn editor-btn-primary" id="editorSaveBtn">Save</button>
            <button class="editor-btn editor-btn-close" id="editorCloseBtn">&times;</button>
          </div>
        </div>
        <div class="editor-body">
          <div class="editor-main" id="editorMainPanel">
            <textarea id="editorContent" class="editor-textarea" placeholder="Start writing your document content here..."></textarea>
          </div>
          <div class="editor-sidebar hidden" id="editorSidebar">
            <div class="editor-sidebar-header">
              <h4>Version History</h4>
              <button class="editor-btn editor-btn-close editor-btn-sm" id="closeSidebarBtn">&times;</button>
            </div>
            <div class="editor-versions-list" id="editorVersionsList"></div>
          </div>
        </div>
        <div class="editor-statusbar" id="editorStatusbar">
          Ready
        </div>
      </div>
      <div class="editor-save-dialog hidden" id="saveDialog">
        <div class="editor-save-dialog-content">
          <h4>Save Version</h4>
          <p>Add a note describing your changes (optional):</p>
          <input type="text" id="saveNoteInput" class="editor-save-note" placeholder="e.g., Updated agent rules for RWI system">
          <div class="editor-save-actions">
            <button class="editor-btn editor-btn-secondary" id="saveCancelBtn">Cancel</button>
            <button class="editor-btn editor-btn-primary" id="saveConfirmBtn">Save Version</button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    this.modal = overlay;
  },

  bindEvents() {
    document.getElementById('editorCloseBtn').addEventListener('click', () => this.close());
    document.getElementById('editorOverlay').addEventListener('click', (e) => {
      if (e.target.id === 'editorOverlay') this.close();
    });
    document.getElementById('editorSaveBtn').addEventListener('click', () => this.showSaveDialog());
    document.getElementById('editorVersionsBtn').addEventListener('click', () => this.toggleSidebar());
    document.getElementById('closeSidebarBtn').addEventListener('click', () => this.toggleSidebar());
    document.getElementById('saveCancelBtn').addEventListener('click', () => this.hideSaveDialog());
    document.getElementById('saveConfirmBtn').addEventListener('click', () => this.confirmSave());
    document.getElementById('editorContent').addEventListener('input', () => {
      this.unsavedChanges = true;
      this.updateStatus('Unsaved changes');
    });
    document.getElementById('editorDocTitle').addEventListener('input', () => {
      this.unsavedChanges = true;
    });
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.key === 's' && this.isOpen()) {
        e.preventDefault();
        this.showSaveDialog();
      }
      if (e.key === 'Escape' && this.isOpen()) {
        this.close();
      }
    });
  },

  isOpen() {
    return this.modal && this.modal.classList.contains('active');
  },

  async open(docKey, defaultTitle) {
    this.currentDocKey = docKey;
    this.unsavedChanges = false;
    document.getElementById('editorDocTitle').value = defaultTitle || '';
    document.getElementById('editorContent').value = '';
    this.modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    this.updateStatus('Loading...');

    try {
      const res = await fetch(`/api/documents/${docKey}`);
      const doc = await res.json();
      if (doc.exists) {
        document.getElementById('editorDocTitle').value = doc.title;
        document.getElementById('editorContent').value = doc.content;
        this.updateStatus(`Loaded — last saved ${this.formatDate(doc.updated_at)}`);
      } else {
        this.updateStatus('New document — start editing and save when ready');
      }
    } catch (err) {
      this.updateStatus('Error loading document');
      console.error(err);
    }
  },

  close() {
    if (this.unsavedChanges) {
      if (!confirm('You have unsaved changes. Close without saving?')) return;
    }
    this.modal.classList.remove('active');
    document.body.style.overflow = '';
    document.getElementById('editorSidebar').classList.add('hidden');
    this.hideSaveDialog();
  },

  showSaveDialog() {
    document.getElementById('saveDialog').classList.remove('hidden');
    document.getElementById('saveNoteInput').value = '';
    document.getElementById('saveNoteInput').focus();
  },

  hideSaveDialog() {
    document.getElementById('saveDialog').classList.add('hidden');
  },

  async confirmSave() {
    const title = document.getElementById('editorDocTitle').value.trim() || 'Untitled';
    const content = document.getElementById('editorContent').value;
    const saveNote = document.getElementById('saveNoteInput').value.trim();

    this.updateStatus('Saving...');
    this.hideSaveDialog();

    try {
      const res = await fetch(`/api/documents/${this.currentDocKey}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content, save_note: saveNote })
      });
      const result = await res.json();
      if (result.success) {
        this.unsavedChanges = false;
        this.updateStatus(`Saved as version ${result.version} — ${this.formatDate(result.saved_at)}`);
        if (!document.getElementById('editorSidebar').classList.contains('hidden')) {
          this.loadVersions();
        }
      } else {
        this.updateStatus('Error saving document');
      }
    } catch (err) {
      this.updateStatus('Error saving document');
      console.error(err);
    }
  },

  toggleSidebar() {
    const sidebar = document.getElementById('editorSidebar');
    sidebar.classList.toggle('hidden');
    if (!sidebar.classList.contains('hidden')) {
      this.loadVersions();
    }
  },

  async loadVersions() {
    const list = document.getElementById('editorVersionsList');
    list.innerHTML = '<div class="editor-loading">Loading versions...</div>';

    try {
      const res = await fetch(`/api/documents/${this.currentDocKey}/versions`);
      const versions = await res.json();

      if (versions.length === 0) {
        list.innerHTML = '<div class="editor-empty">No saved versions yet</div>';
        return;
      }

      list.innerHTML = versions.map(v => `
        <div class="version-item" data-version="${v.version_number}">
          <div class="version-header">
            <span class="version-number">v${v.version_number}</span>
            <span class="version-date">${this.formatDate(v.saved_at)}</span>
          </div>
          ${v.save_note ? `<div class="version-note">${this.escapeHtml(v.save_note)}</div>` : ''}
          <div class="version-actions">
            <button class="editor-btn editor-btn-sm editor-btn-secondary" onclick="DocEditor.viewVersion(${v.version_number})">View</button>
            <button class="editor-btn editor-btn-sm editor-btn-secondary" onclick="DocEditor.restoreVersion(${v.version_number})">Restore</button>
          </div>
        </div>
      `).join('');
    } catch (err) {
      list.innerHTML = '<div class="editor-empty">Error loading versions</div>';
      console.error(err);
    }
  },

  async viewVersion(versionNumber) {
    try {
      const res = await fetch(`/api/documents/${this.currentDocKey}/versions/${versionNumber}`);
      const version = await res.json();
      const viewWindow = window.open('', '_blank', 'width=700,height=500');
      viewWindow.document.write(`
        <!DOCTYPE html>
        <html><head><title>Version ${versionNumber} — ${this.escapeHtml(version.title)}</title>
        <style>
          body { font-family: monospace; background: #0f1420; color: #e2e8f0; padding: 2rem; margin: 0; }
          h2 { color: #7dd3fc; margin-bottom: 0.5rem; }
          .meta { color: #94a3b8; font-size: 0.875rem; margin-bottom: 1.5rem; }
          pre { white-space: pre-wrap; word-wrap: break-word; line-height: 1.6; }
        </style></head><body>
        <h2>${this.escapeHtml(version.title)} — Version ${versionNumber}</h2>
        <div class="meta">Saved: ${this.formatDate(version.saved_at)}${version.save_note ? ' — ' + this.escapeHtml(version.save_note) : ''}</div>
        <pre>${this.escapeHtml(version.content)}</pre>
        </body></html>
      `);
    } catch (err) {
      console.error(err);
      alert('Error loading version');
    }
  },

  async restoreVersion(versionNumber) {
    if (!confirm(`Restore version ${versionNumber}? This will replace your current content and create a new version.`)) return;

    this.updateStatus('Restoring...');
    try {
      const res = await fetch(`/api/documents/${this.currentDocKey}/versions/${versionNumber}/restore`, {
        method: 'POST'
      });
      const result = await res.json();
      if (result.success) {
        const docRes = await fetch(`/api/documents/${this.currentDocKey}`);
        const doc = await docRes.json();
        document.getElementById('editorDocTitle').value = doc.title;
        document.getElementById('editorContent').value = doc.content;
        this.unsavedChanges = false;
        this.updateStatus(`Restored from version ${versionNumber} → now version ${result.version}`);
        this.loadVersions();
      }
    } catch (err) {
      this.updateStatus('Error restoring version');
      console.error(err);
    }
  },

  updateStatus(msg) {
    const bar = document.getElementById('editorStatusbar');
    if (bar) bar.textContent = msg;
  },

  formatDate(isoStr) {
    if (!isoStr) return 'Unknown';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) +
           ' at ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  },

  escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
};

document.addEventListener('DOMContentLoaded', () => DocEditor.init());
