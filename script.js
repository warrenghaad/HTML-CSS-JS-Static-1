document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('.content-section');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      navLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      
      sections.forEach(section => section.classList.remove('active'));
      
      const targetId = this.getAttribute('href').substring(1);
      const targetSection = document.getElementById(targetId);
      
      if (targetSection) {
        targetSection.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  });

  if (window.location.hash) {
    const targetId = window.location.hash.substring(1);
    const targetLink = document.querySelector(`a[href="#${targetId}"]`);
    const targetSection = document.getElementById(targetId);
    
    if (targetLink && targetSection) {
      navLinks.forEach(l => l.classList.remove('active'));
      sections.forEach(s => s.classList.remove('active'));
      targetLink.classList.add('active');
      targetSection.classList.add('active');
    }
  }
});
