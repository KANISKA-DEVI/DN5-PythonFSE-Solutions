// ============================================================
// Hands-On 4: Async JS, Fetch API & Axios
// File: app.js
// Location: C:\DigitalNurture5\Module2_FrontendDev\hands_on_04\
// ============================================================

const BASE_URL = 'https://jsonplaceholder.typicode.com';

// ============================================================
// TASK 1: Promises and async/await
// ============================================================

// Fetch a single user — Promise chain version
function fetchUserPromise(id) {
  return fetch(`${BASE_URL}/users/${id}`)
    .then(response => response.json())
    .then(user => {
      console.log(`[Promise] User ${id}: ${user.name}`);
      return user;
    });
}

// Same function — async/await version (cleaner)
async function fetchUser(id) {
  try {
    const response = await fetch(`${BASE_URL}/users/${id}`);
    const user     = await response.json();
    console.log(`[Async/Await] User ${id}: ${user.name}`);
    return user;
  } catch (error) {
    console.error(`Failed to fetch user ${id}:`, error);
  }
}

// Simulate 1-second network delay, then return course data
function fetchAllCourses() {
  return new Promise(resolve => {
    const courses = [
      { id:1, name:"Data Structures & Algorithms", credits:4 },
      { id:2, name:"Database Management Systems",  credits:3 },
      { id:3, name:"Object Oriented Programming",  credits:4 },
    ];
    setTimeout(() => resolve(courses), 1000);  // 1 second delay
  });
}

// Promise.all — fetch two users simultaneously
async function fetchTwoUsersTogether() {
  const [user1, user2] = await Promise.all([fetchUser(1), fetchUser(2)]);
  const el = document.querySelector('#users-output');
  el.innerHTML = `
    <div class="user-results">
      <p><strong>User 1:</strong> ${user1?.name} (${user1?.email})</p>
      <p><strong>User 2:</strong> ${user2?.name} (${user2?.email})</p>
      <p style="margin-top:8px; color:#34a853;">✓ Both loaded simultaneously with Promise.all</p>
    </div>
  `;
}

fetchTwoUsersTogether();


// ============================================================
// TASK 2: Fetch API with Error Handling
// ============================================================

// Reusable fetch helper that throws on non-OK responses
async function apiFetch(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status} ${response.statusText} for ${url}`);
  }
  return response.json();
}

// Show/hide loading spinner
function setLoading(containerId, isLoading) {
  const loadingEl = document.querySelector(`#${containerId} .loading`);
  if (loadingEl) loadingEl.style.display = isLoading ? 'block' : 'none';
}

// Render notifications from API data
function renderNotifications(posts) {
  const container = document.querySelector('#notifications-container');
  container.innerHTML = '';

  posts.slice(0, 5).forEach(post => {
    const card = document.createElement('div');
    card.className = 'notification-card';
    card.innerHTML = `
      <h3>${post.title}</h3>
      <p>${post.body.substring(0, 100)}...</p>
    `;
    container.appendChild(card);
  });
}

// Show error with retry button
function showError(message, retryFn) {
  const errorContainer = document.querySelector('#error-container');
  const notifContainer = document.querySelector('#notifications-container');

  notifContainer.innerHTML = '';
  errorContainer.style.display = 'block';
  errorContainer.innerHTML = `
    <div class="error-box">
      <p>❌ ${message}</p>
      <button class="retry-btn" id="retry-btn">🔄 Retry</button>
    </div>
  `;

  document.querySelector('#retry-btn').addEventListener('click', retryFn);
}

// Load notifications
async function loadNotifications() {
  const errorContainer = document.querySelector('#error-container');
  errorContainer.style.display = 'none';
  document.querySelector('#notifications-container').innerHTML =
    '<div class="loading">Loading notifications...</div>';

  try {
    const posts = await apiFetch(`${BASE_URL}/posts`);
    renderNotifications(posts);
  } catch (error) {
    showError(error.message, loadNotifications);
  }
}

loadNotifications();


// ============================================================
// TASK 3: Axios
// ============================================================

// Axios request interceptor — logs every request
axios.interceptors.request.use(config => {
  console.log(`[Axios Interceptor] API call started: ${config.url}`);
  return config;
});

// Fetch posts for user 1 using Axios params
async function loadWithAxios() {
  try {
    // Axios auto-parses JSON and throws on non-2xx
    const response = await axios.get(`${BASE_URL}/posts`, {
      params: { userId: 1 }  // Filters posts by userId=1
    });

    const posts = response.data;   // Axios puts data directly in .data
    const outputEl = document.querySelector('#axios-output');

    outputEl.innerHTML = `
      <div class="user-results">
        <p>✓ Loaded <strong>${posts.length} posts</strong> for User 1 using Axios</p>
        <p style="margin-top:8px; color:#555;">First post title: "${posts[0]?.title}"</p>
        <hr style="margin:12px 0; border-color:#eee;" />
        <p style="font-size:0.85rem; color:#888;">
          <strong>Fetch vs Axios comparison:</strong><br/>
          1. Axios auto-parses JSON; Fetch requires .json()<br/>
          2. Axios throws on 4xx/5xx errors; Fetch only throws on network failure<br/>
          3. Axios has built-in request/response interceptors; Fetch does not
        </p>
      </div>
    `;
  } catch (error) {
    document.querySelector('#axios-output').innerHTML =
      `<div class="error-box">Axios error: ${error.message}</div>`;
  }
}

loadWithAxios();