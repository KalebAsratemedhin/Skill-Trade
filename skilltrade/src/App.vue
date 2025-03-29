<template>
  <div class="flex">
    <!-- <Sidebar v-if="authStore.isAuthenticated" /> -->
    <div class="flex-1">
      <Navbar />
      <main class="p-4">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import Sidebar from "@/components/Sidebar.vue";
import { useAuthStore } from "@/store/auth";

const authStore = useAuthStore();
</script>
