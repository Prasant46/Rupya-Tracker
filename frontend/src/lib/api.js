import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "";

const client = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
  withCredentials: true, // Important: send cookies with every request
});

export async function createUserAccount(user) {
  const res = await client.post("/auth/register", user);
  return res.data;
}

export async function signInAccount(user) {
  const res = await client.post("/auth/login", user);
  return res.data;
}

export async function signOutAccount() {
  const res = await client.post("/auth/logout");
  return res.data;
}

export async function saveUserToDB(user) {
  const res = await client.post("/users", user);
  return res.data; // Return user data from response
}

export async function saveUserAfterSocialAuth(token) {
  // Set the JWT token as a cookie
  document.cookie = `access_token_cookie=${token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
  
  // Fetch user data to verify authentication
  try {
    const res = await client.get("/auth/me");
    return res.data;
  } catch (error) {
    return { success: false, message: "Authentication failed" };
  }
}

export async function signInWithGithub() {
  window.location.href = `${API_BASE}/auth/oauth/github`;
}

export async function signInWithGoogle() {
  window.location.href = `${API_BASE}/auth/oauth/google`;
}

export async function getAccount() {
  try {
    const res = await client.get("/auth/me");
    return res.data;
  } catch (error) {
    return null;
  }
}

export async function getCurrentUser() {
  try {
    const res = await client.get("/users/me");
    return res.data; // Return user data from response
  } catch (error) {
    return null; // Return null if error (not authenticated)
  }
}

export async function createExpense(newExpense) {
  const res = await client.post("/expenses", newExpense);
  return res.data; // Return full response { success, message, data }
}

export async function updateExpense({ newData, originalData, owner }) {
  const res = await client.put(`/expenses/${originalData.$id}`, newData);
  return res.data; // Return full response { success, message, data }
}

export async function getExpenses({ userId, forToday = false }) {
  const params = {};
  if (userId) params.userId = userId;
  if (forToday) params.forToday = true;
  const res = await client.get("/expenses", { params });
  return res.data.data || res.data; // Return data array (backwards compat)
}

export async function getTrashedExpenses(owner) {
  const res = await client.get("/expenses/trashed", { params: { owner } });
  return res.data.data || res.data; // Return data array (backwards compat)
}

export async function moveToTrashExpense({ deleteItem, owner }) {
  const res = await client.post(`/expenses/${deleteItem.$id}/trash`, { owner });
  return res.data; // Return full response with success, message, data
}

export async function restoreExpenseFromTrash({ trashedItem, owner }) {
  const res = await client.post(`/expenses/${trashedItem.$id}/restore`, {
    owner,
  });
  return res.data; // Return full response with success, message, data
}

export async function deleteExpense({ deleteItem, owner }) {
  const res = await client.delete(`/expenses/${deleteItem.$id}`);
  return res.data; // Return full response with success, message, data
}

export default client;
