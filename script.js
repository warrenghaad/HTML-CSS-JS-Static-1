document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      navLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      
      const sections = document.querySelectorAll('.content-section');
      sections.forEach(section => section.classList.remove('active'));
      
      const targetId = this.getAttribute('href').substring(1);
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  });
});

function toggleContent(contentId) {
  const content = document.getElementById(contentId);
  if (content) {
    content.classList.toggle('show');
  }
}

function checkAnswer(result) {
  const resultElement = document.getElementById('quiz-result');
  if (result === 'correct') {
    resultElement.textContent = '✓ Correct! Great job!';
    resultElement.style.color = '#28a745';
  } else {
    resultElement.textContent = '✗ Not quite. Try again!';
    resultElement.style.color = '#dc3545';
  }
}
