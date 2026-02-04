document.addEventListener('DOMContentLoaded', function() {
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      document.body.classList.toggle('light');
      localStorage.setItem('theme', document.body.classList.contains('light') ? 'light' : 'dark');
    });
    
    if (localStorage.getItem('theme') === 'light') {
      document.body.classList.add('light');
    }
  }

  const engineCards = document.querySelectorAll('.engine-card');
  engineCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      const engine = this.dataset.engine;
      highlightConnections(engine);
    });
    
    card.addEventListener('mouseleave', function() {
      resetConnections();
    });
  });
});

function highlightConnections(engine) {
  const connectors = document.querySelectorAll('.flow-connector');
  connectors.forEach(c => c.style.opacity = '0.3');
  
  const card = document.querySelector(`[data-engine="${engine}"]`);
  if (card) {
    const cardConnectors = card.querySelectorAll('.flow-connector');
    cardConnectors.forEach(c => c.style.opacity = '1');
  }
}

function resetConnections() {
  const connectors = document.querySelectorAll('.flow-connector');
  connectors.forEach(c => c.style.opacity = '1');
}

function updateHealth(engineId, status) {
  const card = document.querySelector(`[data-engine="${engineId}"]`);
  if (card) {
    const indicator = card.querySelector('.health-indicator');
    indicator.className = 'health-indicator ' + status;
  }
}

function updateToolStatus(engineId, toolIndex, status) {
  const card = document.querySelector(`[data-engine="${engineId}"]`);
  if (card) {
    const tools = card.querySelectorAll('.tool');
    if (tools[toolIndex]) {
      tools[toolIndex].dataset.status = status;
    }
  }
}
