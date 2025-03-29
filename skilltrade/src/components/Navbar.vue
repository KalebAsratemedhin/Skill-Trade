<template>
    <nav class="flex items-center h-24 justify-between px-6 py-3 shadow-md bg-gradient-to-r from-indigo-600 to-purple-700 text-white">
      <button @click="toggleSidebar" class="md:hidden focus:outline-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
        </svg>
      </button>

      <h1 class="text-xl font-bold">SkillTrade</h1>
  
      <div class="hidden md:flex items-center space-x-6">
        <RouterLink to="/" class="text-white hover:text-white hover:underline hover:underline-offset-8 transition duration-200">Home</RouterLink>
        <RouterLink to="/about" class="text-white hover:text-white hover:underline hover:underline-offset-8 transition duration-200">About</RouterLink>
        <RouterLink to="/find-technician" class="text-white hover:text-white hover:underline hover:underline-offset-8 transition duration-200">Find Technician</RouterLink>
        <RouterLink to="/bookings" class="text-white hover:text-white hover:underline hover:underline-offset-8 transition duration-200">Bookings</RouterLink>
      </div>
  
      <div class="flex items-center space-x-4">
        <button @click="toggleTheme" class="focus:outline-none">
          <svg v-if="isDarkMode" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m8.66-8.66h1m-18 0h1M16.24 7.76l.71-.71m-9.9 9.9l.71.71m9.9 0l.71-.71m-9.9-9.9l.71.71M12 5a7 7 0 110 14 7 7 0 010-14z"></path>
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.293 19.293A8 8 0 118.707 4.707a8 8 0 018.586 14.586z"></path>
          </svg>
        </button>
  
        <button class="relative focus:outline-none">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .417-.162.82-.405 1.095L4 17h5m6 0a3 3 0 01-6 0"></path>
          </svg>
          <span v-if="notifications.length" class="absolute -top-1 -right-2 bg-red-500 text-white text-xs rounded-full px-2">
            {{ notifications.length }}
          </span>
        </button>
  
        <div class="relative">
          <button @click="toggleDropdown" class="flex items-center focus:outline-none">
            <img v-if="user.avatar" :src="user.avatar" alt="Profile" class="w-8 h-8 rounded-full border-2 border-white">
            <div v-else class="w-8 h-8 flex items-center justify-center rounded-full bg-gray-500 text-white text-lg font-bold">
              {{ user.username.charAt(0).toUpperCase() }}
            </div>
          </button>
  
          <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-40 bg-white text-gray-800 rounded-lg shadow-lg overflow-hidden">
            <RouterLink to="/profile" class="block px-4 py-2 hover:bg-gray-200">Profile</RouterLink>
            <RouterLink to="/settings" class="block px-4 py-2 hover:bg-gray-200">Settings</RouterLink>
            <button @click="logout" class="w-full text-left px-4 py-2 hover:bg-gray-200">Logout</button>
          </div>
        </div>
      </div>
  
      <div v-if="sidebarOpen" class="fixed inset-0 z-40" @click="toggleSidebar"></div>
      <div :class="['fixed top-0 left-0 h-full w-64 bg-white text-gray-900 transform transition-transform', sidebarOpen ? 'translate-x-0' : '-translate-x-full']">
        <button @click="toggleSidebar" class="absolute top-4 right-4 text-gray-800">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
        <div class="mt-16 space-y-6 px-6">
          <RouterLink to="/" class="block text-black py-2 hover:bg-gray-300  bg-blue-50 p-2 rounded-md">Home</RouterLink>
          <RouterLink to="/about" class="block text-black py-2 hover:bg-gray-300  bg-blue-50 p-2 rounded-md">About</RouterLink>
          <RouterLink to="/find-technician" class="block text-black py-2 hover:bg-gray-300  bg-blue-50 p-2 rounded-md">Find Technician</RouterLink>
          <RouterLink to="/bookings" class="block text-black py-2 hover:bg-gray-300  bg-blue-50 p-2 rounded-md">Bookings</RouterLink>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref, computed } from "vue";
  import { useAuthStore } from "@/store/auth";
  
  const authStore = useAuthStore();
  const user = computed(() => authStore.user || { username: "User", avatar: null });
  const dropdownOpen = ref(false);
  const sidebarOpen = ref(false);
  const isDarkMode = ref(false);
  const notifications = ref([/* Example: { id: 1, message: "New Booking!" } */]);
  
  const toggleDropdown = () => {
    dropdownOpen.value = !dropdownOpen.value;
  };
  
  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
  };
  
  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value;
    document.documentElement.classList.toggle("dark");
  };
  
  const logout = () => {
    authStore.logout();
    dropdownOpen.value = false;
  };
  </script>
  