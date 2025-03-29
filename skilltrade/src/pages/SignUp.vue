<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <Snackbar ref="snackbarRef" />
      <div class="bg-white p-6 rounded-lg shadow-lg m-auto sm:px-20">
        <h2 class="text-2xl font-bold text-center mb-4">Sign Up</h2>
        <form @submit.prevent="signUp" class="md:w-96">
          <BaseInput 
            v-model="email" 
            label="Email" 
            type="email" 
            placeholder="Enter your email" 
            :error="errors.email" 
          />
          <BaseInput 
            v-model="password" 
            label="Password" 
            type="password" 
            placeholder="Enter your password" 
            :error="errors.password" 
            class="mt-3" 
          />
          
          <!-- Role Selection -->
          <div class="mt-3">
            <label class="block text-sm font-medium text-gray-700">Select Role</label>
            <select v-model="role" class="w-full px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-300">
              <option value="customer">Customer</option>
              <option value="technician">Technician</option>
            </select>
          </div>
  
          <!-- Customer Fields -->
          <div v-if="role === 'customer'" class="mt-4 ">
            <BaseInput 
              v-model="username" 
              label="Username" 
              type="text" 
              placeholder="Enter your username" 
              :error="errors.username" 
            />
            <BaseInput 
              v-model="phoneNumber" 
              label="Phone Number" 
              type="tel" 
              placeholder="Enter your phone number" 
              :error="errors.phoneNumber" 
            />
            <BaseInput 
              v-model="address" 
              label="Address" 
              type="text" 
              placeholder="Enter your address" 
              :error="errors.address" 
            />
          </div>
  
          <!-- Technician Fields -->
          <div v-if="role === 'technician'" class="mt-4">
            <BaseInput 
              v-model="username" 
              label="Username" 
              type="text" 
              placeholder="Enter your username" 
              :error="errors.username" 
            />
            <BaseInput 
              v-model="phoneNumber" 
              label="Phone Number" 
              type="tel" 
              placeholder="Enter your phone number" 
              :error="errors.phoneNumber" 
            />
            <BaseInput 
              v-model="address" 
              label="Address" 
              type="text" 
              placeholder="Enter your address" 
              :error="errors.address" 
            />
            <BaseInput 
              v-model="experienceInYears" 
              label="Experience (Years)" 
              type="number" 
              placeholder="Enter your years of experience" 
              :error="errors.experienceInYears" 
            />
            <BaseInput 
              v-model="expertise" 
              label="Expertise" 
              type="text" 
              placeholder="Enter your expertise" 
              :error="errors.expertise" 
            />
            <div class="mt-3">
              <label class="block text-sm font-medium text-gray-700">Available</label>
              <input type="checkbox" v-model="available" class="mr-2" />
              <span>Yes, I'm available</span>
            </div>
          </div>
  
          <BaseButton class="mt-4">Sign Up</BaseButton>
        </form>
        <p class="mt-3 text-center text-sm">
          Already have an account? <RouterLink to="/signin" class="text-indigo-600">Sign In</RouterLink>
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
    import { ref } from "vue";
    import BaseInput from "@/components/BaseInput.vue";
    import BaseButton from "@/components/BaseButton.vue";
    import { useAuthStore } from "@/store/auth";
    import {signUpCustomerService} from "@/services/authService"
    import Snackbar from "@/components/Snackbar.vue";
    const snackbarRef = ref(null);

    // Form data
    const email = ref("");
    const password = ref("");
    const username = ref("");
    const phoneNumber = ref("");
    const address = ref("");
    const experienceInYears = ref(null);
    const expertise = ref("");
    const available = ref(false);
    
    // User role selection (customer or technician)
    const role = ref("customer");
    const authStore = useAuthStore();
    
    // Error tracking
    const errors = ref({
      email: "",
      password: "",
      username: "",
      phoneNumber: "",
      address: "",
      experienceInYears: "",
      expertise: "",
    });
    
    // Validation functions
    const validate = () => {
      errors.value = {}; // Reset errors
      
      let isValid = true;
      
      // Email validation
      if (!email.value || !/\S+@\S+\.\S+/.test(email.value)) {
        errors.value.email = "Please enter a valid email address.";
        isValid = false;
      }
      
      // Password validation
      if (!password.value || password.value.length < 6) {
        errors.value.password = "Password must be at least 6 characters long.";
        isValid = false;
      }
      
      // Common field validations (username, phone, address)
      if (!username.value) {
        errors.value.username = "Username is required.";
        isValid = false;
      }
      
      if (!phoneNumber.value || !/\d{10}/.test(phoneNumber.value)) {
        errors.value.phoneNumber = "Please enter a valid phone number.";
        isValid = false;
      }
      
      if (!address.value) {
        errors.value.address = "Address is required.";
        isValid = false;
      }
      
      // Technician specific validations
      if (role.value === "technician") {
        if (!experienceInYears.value || experienceInYears.value < 0) {
          errors.value.experienceInYears = "Please enter a valid number of years of experience.";
          isValid = false;
        }
        
        if (!expertise.value) {
          errors.value.expertise = "Expertise is required.";
          isValid = false;
        }
      }
      
      return isValid;
    };


  
    const signUp = async () => {
      if (validate()) {

        const data = {
            email: email.value,
            password: password.value,
            username: username.value,
            role: role.value,
            phoneNumber: phoneNumber.value,
            address: address.value,
            experienceInYears: experienceInYears.value,
            expertise: expertise.value,
            available: available.value,
        }


        const response = await authStore.signUp(data);
        console.log('response', response)
        if (response) {
            snackbarRef.value.showSnackbar("User registered successfully!", "success");
            router.push('/profile');

        } else {
            snackbarRef.value.showSnackbar(authStore.error, "error");
        }

        
      }
    };
  </script>
  