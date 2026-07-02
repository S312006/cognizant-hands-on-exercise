// ---- 1. fetchUser using .then() chaining ----
function fetchUser(id) {
  return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
    .then((response) => response.json())
    .then((user) => {
      console.log("fetchUser (.then) name:", user.name);
      return user;
    });
}
fetchUser(1);

// ---- 2. Same thing rewritten with async/await + try/catch ----
async function fetchUserAsync(id) {
  try {
    const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
    const user = await response.json();
    console.log("fetchUserAsync name:", user.name);
    return user;
  } catch (error) {
    console.error("fetchUserAsync error:", error);
  }
}
fetchUserAsync(2);

// ---- 3. Simulated network delay using local course data ----
import { courses } from "./data.js";

function fetchAllCourses() {
  return new Promise((resolve) => {
    setTimeout(() => resolve(courses), 1000);
  });
}

async function loadCourses() {
  console.log("Loading courses...");
  const data = await fetchAllCourses();
  console.log("Courses loaded:", data);
}
loadCourses();

// ---- 4. Promise.all(): fetch two users simultaneously ----
async function fetchTwoUsers() {
  const [user1, user2] = await Promise.all([
    fetch("https://jsonplaceholder.typicode.com/users/1").then((r) => r.json()),
    fetch("https://jsonplaceholder.typicode.com/users/2").then((r) => r.json()),
  ]);
  console.log("Promise.all results:", user1.name, "&", user2.name);
}
fetchTwoUsers();
