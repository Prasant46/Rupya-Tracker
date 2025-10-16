import { create } from "zustand";
import { getCurrentUser, signOutAccount } from "@/lib/api";
export const useAuthStore = create((set, get) => ({
  isLoggedIn: false,
  isAuthLoading: true,
  user: null,

  checkAuth: async () => {
    try {
      const res = await getCurrentUser();

      // Handle response format: { success, message, data }
      if (res?.success && res?.data) {
        set({
          isLoggedIn: true,
          isAuthLoading: false,
          user: res.data,
        });
      } else {
        // Not authenticated
        set({
          isLoggedIn: false,
          isAuthLoading: false,
          user: null,
        });
      }
    } catch (error) {
      // If 401 or any error, user is not authenticated
      set({
        isLoggedIn: false,
        isAuthLoading: false,
        user: null,
      });
    }
  },

  setAuth: (userData) => {
    // userData could be response object { success, message, data } or direct user object
    const user = userData?.data || userData;
    set({
      isLoggedIn: !!user?.$id,
      isAuthLoading: false,
      user,
    });
  },

  logOut: async () => {
    set({
      isAuthLoading: true,
    });

    const res = await signOutAccount();
    set({
      isLoggedIn: false,
      isAuthLoading: false,
      user: null,
    });
  },
}));

export const useExpenseStore = create((set, get) => ({
  actionType: "add",
  actionType: "add",
  isOpenModal: false,
  editableItem: null,
  isOpenDeleteModal: false,
  deleteItem: null,
  filteredExpenses: [],
  searchText: "",
  isOpenDetails: false,
  clickedItem: "",

  toggleModal: (type, clickedItem) => {
    if (type === "edit") {
      set({ editableItem: clickedItem });
    }

    set({
      isOpenModal: !get().isOpenModal,
      actionType: type === "edit" ? "edit" : "add",
    });
  },

  toggleDeleteModal: (clickedItem) => {
    set({
      isOpenDeleteModal: !get().isOpenDeleteModal,
      deleteItem: clickedItem || null,
    });
  },

  setFilteredExpenses: (value) => {
    set({
      filteredExpenses: value,
    });
  },

  setSearchText: (value) => {
    set({ searchText: value });
  },

  toggleDetails: (item) => {
    set({
      isOpenDetails: !get().isOpenDetails,
      clickedItem: item,
    });
  },
}));

export const useThemeStore = create((set) => ({
  darkMode: localStorage.getItem("darkMode") === "true",

  toggleDarkMode: () => {
    set((state) => {
      const newDarkMode = !state.darkMode;
      localStorage.setItem("darkMode", newDarkMode.toString());

      if (newDarkMode) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }

      return { darkMode: newDarkMode };
    });
  },

  enableDarkMode: () => {
    localStorage.setItem("darkMode", "true");
    document.documentElement.classList.add("dark");
  },
}));
