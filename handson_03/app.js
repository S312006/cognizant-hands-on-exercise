import { courses } from "./data.js";

const courseGrid = document.querySelector(".course-grid");
const searchInput = document.getElementById("search-courses");
const sortButton = document.getElementById("sort-credits");
const selectedCourseDiv = document.getElementById("selected-course");

let currentCourses = [...courses];

function renderCourses(courseList) {
  courseGrid.innerHTML = "";
  courseList.forEach((course) => {
    const article = document.createElement("article");
    article.className = "course-card";
    article.dataset.id = course.id;
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;
    courseGrid.appendChild(article);
  });

  const total = courseList.reduce((sum, c) => sum + c.credits, 0);
  const totalEl = document.getElementById("total-credits");
  if (totalEl) totalEl.textContent = `Total Credits: ${total}`;
}

searchInput.addEventListener("input", (e) => {
  const term = e.target.value.toLowerCase();
  const filtered = currentCourses.filter((course) =>
    course.name.toLowerCase().includes(term)
  );
  renderCourses(filtered);
});

sortButton.addEventListener("click", () => {
  currentCourses = [...currentCourses].sort((a, b) => b.credits - a.credits);
  renderCourses(currentCourses);
});

courseGrid.addEventListener("click", (e) => {
  const card = e.target.closest(".course-card");
  if (!card) return;
  const id = Number(card.dataset.id);
  const course = courses.find((c) => c.id === id);
  selectedCourseDiv.textContent = `Selected: ${course.name} - Grade: ${course.grade}`;
});

renderCourses(currentCourses);
