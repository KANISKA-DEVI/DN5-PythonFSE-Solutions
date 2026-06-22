// ============================================================
// Hands-On 9: Accessibility JavaScript
// File: app.js
// ============================================================

// Task 2, Step 128: Hamburger menu with aria-expanded toggle
const hamburger = document.getElementById('hamburger-btn');
const navMenu   = document.getElementById('nav-menu');

if (hamburger && navMenu) {
  hamburger.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', String(isOpen));
  });
}

// Task 2, Step 129: Keyboard Enter on course cards
const courseGrid = document.getElementById('course-grid');
if (courseGrid) {
  courseGrid.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const card = e.target.closest('.course-card');
      if (card) {
        const title = card.querySelector('h3')?.textContent;
        alert(`Selected: ${title}`);
      }
    }
  });

  // Click handler for mouse users
  courseGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.course-card');
    if (card) {
      const title = card.querySelector('h3')?.textContent;
      console.log(`Course selected: ${title}`);
    }
  });
}

// Task 2, Step 130: Live region — update results count on search
const searchInput  = document.getElementById('search-courses');
const resultsCount = document.getElementById('results-count');
const cards        = document.querySelectorAll('.course-card');

if (searchInput && resultsCount) {
  searchInput.addEventListener('input', (e) => {
    const term    = e.target.value.toLowerCase();
    let visible   = 0;

    cards.forEach(card => {
      const title = card.querySelector('h3')?.textContent.toLowerCase() || '';
      const show  = title.includes(term);
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    // aria-live="polite" will announce this change to screen readers
    resultsCount.textContent = `Showing ${visible} course${visible !== 1 ? 's' : ''}`;
  });
}