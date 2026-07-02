const notificationsContent = document.getElementById("notifications-content");

async function apiFetch(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}

function showLoading() {
  notificationsContent.innerHTML = `<p class="loading">Loading notifications...</p>`;
}

function showError(message) {
  notificationsContent.innerHTML = `
    <p class="error-message">? ${message}</p>
    <button id="retry-btn">Retry</button>
  `;
  document.getElementById("retry-btn").addEventListener("click", loadNotifications);
}

function renderNotifications(posts) {
  notificationsContent.innerHTML = "";
  posts.slice(0, 5).forEach((post) => {
    const card = document.createElement("div");
    card.className = "notification-card";
    card.innerHTML = `<h4>${post.title}</h4><p>${post.body}</p>`;
    notificationsContent.appendChild(card);
  });
}

async function loadNotifications() {
  showLoading();
  try {
    const posts = await apiFetch("https://jsonplaceholder.typicode.com/posts");
    renderNotifications(posts);
  } catch (error) {
    showError(error.message);
  }
}

loadNotifications();
