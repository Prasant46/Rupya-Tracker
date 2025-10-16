import { toast } from "react-hot-toast";

export const showToast = (
  msg = "Here is your toast",
  type = "success",
  time = 2000
) => {
  toast[type](msg, { duration: time, position: "top-center" });
};

export function capitalizeFirstLetter(str = "") {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    month: "long",
    day: "2-digit",
    year: "numeric",
  });
}

export const setLocalStorageItem = (key, value) =>
  localStorage.setItem(key, JSON.stringify(value));
export const getLocalStorageItem = (key) => {
  const item = localStorage.getItem(key);
  return item ? JSON.parse(item) : null;
};
export const removeLocalStorageItem = (key) => localStorage.removeItem(key);

export const validateEmail = (email) =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
export const validatePassword = (password) => (password || "").length >= 8;

export function formatDateForInput(dateString) {
  const date = new Date(dateString);
  return date.toISOString().split("T")[0];
}

export function calculateTotalAmount(expenses) {
  return (expenses || []).reduce((sum, e) => sum + (Number(e.amount) || 0), 0);
}

const isWithinLastNDays = (dateString, n) => {
  const now = new Date();
  const expenseDate = new Date(dateString);
  const nDaysAgo = new Date(now.getTime() - n * 24 * 60 * 60 * 1000);
  return expenseDate >= nDaysAgo && expenseDate <= now;
};

const filterExpensesForLastNDays = (allExpenses = [], n) =>
  allExpenses.filter((exp) => isWithinLastNDays(exp.date, n));

export const filterExpensesForLast7Days = (allExpenses) =>
  filterExpensesForLastNDays(allExpenses, 7);
export const filterExpensesForLast14Days = (allExpenses) =>
  filterExpensesForLastNDays(allExpenses, 14);

export const filterExpensesForLast1Month = (allExpenses = []) => {
  const now = new Date();
  const oneMonthAgo = new Date(
    now.getFullYear(),
    now.getMonth() - 1,
    now.getDate()
  );
  return allExpenses.filter((exp) => new Date(exp.date) >= oneMonthAgo);
};

export const filterExpensesForCustomDateRange = (
  allExpenses = [],
  startDate,
  endDate
) => {
  const start = new Date(startDate);
  const end = new Date(endDate);
  return allExpenses.filter((expense) => {
    const d = new Date(expense.date);
    return d >= start && d <= end;
  });
};
