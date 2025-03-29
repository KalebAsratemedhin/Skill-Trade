import { defineStore } from "pinia";
import { getCurrentCustomerService, getCurrentTechnicianService } from "../services/userService";
import { ref } from "vue";
import { useAuthStore } from "./auth";

export const useUsersStore = defineStore("users", () => {

    const currentUser = ref(null);
    const error = ref(null);

  
    const getCurrentUser = async () => {
        const authStore = useAuthStore()
        const role = authStore.user.role;
        console.log("getting current user", role)

      error.value = null; 
      try {
        if (role === "customer"){
            const response = await getCurrentCustomerService();
            currentUser.value = response;
            return true;
        } else {
            const response = await getCurrentTechnicianService();

            currentUser.value = response
            return true;
        }
        
      } catch (err) {
        error.value = err.message; 
        return null;
      }
    };
  
    return {
      currentUser,
      error,
      getCurrentUser
    };
  });