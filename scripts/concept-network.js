import { nodes, edges } from '../data/euclidGraph.js';

function render() {
  const container = document.getElementById('network');

  const sectionNodes = nodes.filter(n => n.type === 'section');
  const systemNodes = nodes.filter(n => n.type === 'system');

  container.innerHTML = `
    <div class="network-layout">
      <div class="network-section">
        <h2>Lesson Spine (Concept Handoffs)</h2>
        <div class="spine">
          ${sectionNodes.map(n => `
            <div class="node-card ${n.day}">
              <h3>${n.label}</h3>
              <p>${n.summary}</p>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="network-section">
        <h2>Systems</h2>
        <div class="systems">
          ${systemNodes.map(n => `
            <div class="system-card">
              <h3>${n.label}</h3>
              <p>${n.summary}</p>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="network-section">
        <h2>Concept Handoffs</h2>
        <div class="handoffs">
          ${edges.filter(e => e.type === 'concept_handoff').map(e => `
            <div class="handoff">
              <strong>${e.source} → ${e.target}</strong>
              <div>${e.label}</div>
              <p>${e.summary}</p>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', render);
