// ============================================================
// app.js — Main JavaScript Application
// File: app.js
// Location: C:\DigitalNurture5\Module2_FrontendDev\hands_on_03\
// ============================================================

// Import course data using ES6 import
import { courses } from './data.js';

// ---- TASK 1: ES6+ Syntax Practice ----

// Destructuring in a loop
console.log("--- Destructuring Demo ---");
for (const course of courses) {
  const { name, credits } = course;   // ES6 destructuring
  console.log(`Course: ${name}, Credits: ${credits}`);
}

// Array.map() — format course string
const formattedCourses = courses.map(
  ({ code, name, credits }) => `${code} — ${name} (${credits} credits)`
);
console.log("\n--- Formatted Courses (map) ---");
formattedCourses.forEach(c => console.log(c));

// Array.filter() — courses with 4+ credits
const highCreditCourses = courses.filter(c => c.credits >= 4);
console.log(`\n--- High Credit Courses (filter): ${highCreditCourses.length} courses ---`);

// Array.reduce() — total credits
const totalCredits = courses.reduce((sum, c) => sum + c.credits, 0);
console.log(`\n--- Total Credits (reduce): ${totalCredits} ---`);


// ---- TASK 2: DOM Rendering ----

const grid        = document.querySelector('#course-grid');
const totalEl     = document.querySelector('#total-credits');
const selectedDiv = document.querySelector('#selected-course');
const selectedTitleEl = document.querySelector('#selected-title');
const selectedGradeEl = document.querySelector('#selected-grade');

// Render courses from data array into the DOM
function renderCourses(courseList) {
  // Clear existing content to avoid duplicates
  grid.innerHTML = '';

  if (courseList.length === 0) {
    grid.innerHTML = '<p style="color:#999; grid-column:1/-1;">No courses found.</p>';
    return;
  }

  // Use DocumentFragment for efficient batch DOM insertion
  const fragment = document.createDocumentFragment();

  courseList.forEach(course => {
    const article = document.createElement('article');
    article.className = 'course-card';
    article.tabIndex = 0;                // Make keyboard-accessible
    article.dataset.id = course.id;      // Store course id for event delegation

    // Build inner HTML using template literal
    article.innerHTML = `
      <span class="grade-badge">Grade: ${course.grade}</span>
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span class="credits">${course.credits} Credits</span>
    `;

    fragment.appendChild(article);
  });

  grid.appendChild(fragment);

  // Update total credits
  const shownTotal = courseList.reduce((sum, c) => sum + c.credits, 0);
  totalEl.textContent = `Total Credits: ${shownTotal}`;
}

// Initial render
renderCourses(courses);


// ---- TASK 3: Event Listeners & Interactivity ----

// Search — filter on each keystroke
const searchInput = document.querySelector('#search-courses');
searchInput.addEventListener('input', (e) => {
  const term = e.target.value.toLowerCase();
  const filtered = courses.filter(c => c.name.toLowerCase().includes(term));
  renderCourses(filtered);
});

// Sort by Credits button
const sortBtn = document.querySelector('#sort-btn');
let sortAscending = false;

sortBtn.addEventListener('click', () => {
  sortAscending = !sortAscending;
  const sorted = [...courses].sort((a, b) =>
    sortAscending ? a.credits - b.credits : b.credits - a.credits
  );
  sortBtn.textContent = sortAscending ? 'Sort by Credits ↑' : 'Sort by Credits ↓';
  renderCourses(sorted);
});

// Event Delegation — single listener on the grid container
// Handles clicks on ALL cards without individual listeners per card
grid.addEventListener('click', (e) => {
  const card = e.target.closest('.course-card');
  if (!card) return;                         // Clicked outside a card

  const courseId = parseInt(card.dataset.id);
  const course   = courses.find(c => c.id === courseId);

  if (course) {
    selectedTitleEl.textContent = `📚 ${course.name} (${course.code})`;
    selectedGradeEl.textContent = `Your Grade: ${course.grade} | Credits: ${course.credits}`;
    selectedDiv.style.display   = 'block';
  }
});

// Also handle keyboard Enter on focused cards
grid.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const card = e.target.closest('.course-card');
    if (card) card.click();
  }
});