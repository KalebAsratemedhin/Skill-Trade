<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-2xl font-bold text-center mb-4">Sign In</h2>
        <form @submit.prevent="signIn">
          <BaseInput 
            v-model="username" 
            label="Username" 
            type="text" 
            placeholder="Enter your username" 
            :error="errors.username"
          />
          <BaseInput 
            v-model="password" 
            label="Password" 
            type="password" 
            placeholder="Enter your password" 
            :error="errors.password" 
            class="mt-3"
          />
          <BaseButton class="mt-4">Sign In</BaseButton>
        </form>
        <p class="mt-3 text-center text-sm">
          Don't have an account? <RouterLink to="/signup" class="text-indigo-600">Sign Up</RouterLink>
        </p>
      </div>
      <Snackbar ref="snackbarRef" />
    </div>
  </template>
  
  <script setup>
    import { ref } from "vue";
    import BaseInput from "@/components/BaseInput.vue";
    import BaseButton from "@/components/BaseButton.vue";
    import { useAuthStore} from "@/store/auth";
    import Snackbar from "@/components/Snackbar.vue"

    import { useRouter } from 'vue-router';

    const router = useRouter();
    
    // Form data
    const username = ref("");
    const password = ref("");
    const snackbarRef = ref(null);


    const authStore = useAuthStore();
    
    // Error tracking
    const errors = ref({
      username: "",
      password: "",
    });
    
    // Validation function
    const validate = () => {
      errors.value = {}; // Reset errors
      
      let isValid = true;
      
      // Username validation
      if (!username.value) {
        errors.value.username = "Username is required.";
        isValid = false;
      }
      
      // Password validation
      if (!password.value || password.value.length < 6) {
        errors.value.password = "Password must be at least 6 characters long.";
        isValid = false;
      }
      
      return isValid;
    };
    
    const signIn = async () => {
      if (validate()) {

        const response = await authStore.signIn({ username: username.value, password: password.value });

        if (response) {
            snackbarRef.value.showSnackbar("User registered successfully!", "success");
            router.push('/profile');
        } else {
            snackbarRef.value.showSnackbar(authStore.error, "error");
        }
      
      }
    };
  </script>
  