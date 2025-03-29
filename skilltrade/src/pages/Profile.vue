<template>
    <div class="mx-auto p-6  min-h-screen">
      <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">Profile</h2>
  
      <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
        <!-- Profile Picture Card -->
        <div class="bg-white md:col-span-1 border-2 rounded-lg max-h-96 p-6 flex flex-col justify-center items-center">
          <img v-if="user?.avatar" :src="user?.avatar" alt="Profile Picture" class="w-28 h-28 rounded-full border-2 border-gray-300">
          <div v-else class="w-48 h-48 flex items-center justify-center rounded-full bg-gray-500 text-white text-8xl font-bold">
              {{ user?.username.charAt(0).toUpperCase() }}
            </div>
          <h3 class="mt-4 text-lg font-semibold">{{ user?.username }}</h3>
          <p class="text-gray-600">{{ user?.email }}</p>
        </div>
  
        <!-- Account Information Card -->
        <div class="md:col-span-2  p-6 flex-col gap-36">
            <h3 class="text-xl font-semibold text-gray-800 mb-4">Account Information</h3>
            <div class="flex-col gap-10">
                <div class=" bg-white p-4 flex-col gap-4 mb-4  ">
                    <label class="block text-xl font-normal mb-2">Username</label>
                    <input v-model="form.username" type="text" class="w-full bg-white px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-300">
                </div>

                <div class=" bg-white p-4 flex-col gap-4 mb-4 ">
                    <label class="block text-xl font-normal mb-2">Email</label>
                    <input v-model="form.email" type="text" class="w-full bg-white px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-300">
                </div>
                <div class=" bg-white p-4 flex-col gap-4 mb-4 ">
                    <label class="block text-xl font-normal mb-2">Phone Number</label>
                    <input v-model="form.phoneNumber" type="text" class="w-full bg-white px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-300">
                </div>

                <div class=" bg-white p-4 flex-col gap-4 mb-4 ">
                    <label class="block text-xl font-normal mb-2">Address</label>
                    <input v-model="form.address" type="text" class="w-full bg-white px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-300">
                </div>
               
            </div>
        </div>
      </div>
  
      <!-- Update Profile Button -->
      <div class="mt-6 flex justify-end">
        <button @click="updateProfile" class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition">
          Update Profile
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, computed, onMounted } from "vue";
  import { useUsersStore } from "@/store/users";
  
  const usersStore = useUsersStore();
  const user = computed(() => usersStore.currentUser);
  
  // Fetch the current user on mount
  onMounted(() => {
    usersStore.getCurrentUser();
  });
  
  // Initialize form with user data
  const form = ref({
    username: "",
    email: "",
    phoneNumber: "",
    address: ""
  });
  
  // Watch for user updates and sync form data
  import { watch } from "vue";
  watch(user, (newUser) => {
    if (newUser) {
      form.value.username = newUser.username;
      form.value.email = newUser.email;
      form.value.phoneNumber = newUser.phone_number;
      form.value.address = newUser.address;
    }
  }, { immediate: true });
  
  const updateProfile = () => {
    usersStore.updateUser(form.value);
  };
  </script>
  