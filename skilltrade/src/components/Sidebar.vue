<template>
    <div :class="['h-screen bg-gray-800 text-white w-64 fixed top-0 left-0 transform transition-transform', isSidebarOpen ? 'translate-x-0' : '-translate-x-64']">
      <!-- Sidebar Header -->
      <div class="p-4 flex justify-between items-center border-b border-gray-700">
        <h2 class="text-xl font-bold">Dashboard</h2>
        <button @click="toggleSidebar" class="md:hidden">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
  
      <!-- Sidebar Links -->
      <nav class="mt-4">
        <RouterLink to="/dashboard" class="block px-4 py-2 hover:bg-gray-700">🏠 Dashboard</RouterLink>
        <RouterLink to="/bookings" class="block px-4 py-2 hover:bg-gray-700">📅 Bookings</RouterLink>
        <RouterLink to="/profile" class="block px-4 py-2 hover:bg-gray-700">👤 Profile</RouterLink>
        <RouterLink to="/settings" class="block px-4 py-2 hover:bg-gray-700">⚙️ Settings</RouterLink>
      </nav>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const isSidebarOpen = ref(true);
  
  const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value;
  };
  </script>
  