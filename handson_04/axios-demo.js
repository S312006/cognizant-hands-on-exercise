// Axios automatically parses JSON and throws on non-2xx responses

// Basic GET request
axios.get("https://jsonplaceholder.typicode.com/posts/1")
  .then((response) => {
    console.log("Axios GET result:", response.data.title);
  })
  .catch((error) => {
    console.error("Axios error:", error.message);
  });

// GET with params - fetch posts belonging to user 1
axios.get("https://jsonplaceholder.typicode.com/posts", { params: { userId: 1 } })
  .then((response) => {
    console.log("User 1 posts count:", response.data.length);
  });

// Request interceptor - logs before every request
axios.interceptors.request.use((config) => {
  console.log("API call started:", config.url);
  return config;
});

axios.get("https://jsonplaceholder.typicode.com/users/3").then((response) => {
  console.log("Axios interceptor demo - user name:", response.data.name);
});

/*
Fetch vs Axios - 3 key differences:
1. Axios automatically parses JSON (response.data ready to use).
   Fetch requires manually calling response.json() as a separate step.
2. Axios throws an error automatically on non-2xx HTTP status codes.
   Fetch only rejects on network failure - you must check response.ok yourself.
3. Axios supports request/response interceptors out of the box (e.g., logging,
   attaching auth tokens). Fetch has no built-in interceptor system.
*/
