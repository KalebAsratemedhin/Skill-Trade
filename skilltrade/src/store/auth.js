import { defineStore } from "pinia";
import { signInService, signUpCustomerService, signUpTechnicianService } from "../services/authService";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
    const access = ref(localStorage.getItem("access") || null);
    const refresh = ref( localStorage.getItem("refresh") || null);

    const user = ref(JSON.parse(localStorage.getItem("user")) || null);
    const error = ref(null);

    const isAuthenticated = !!access.value;

    const setCredentials = (response) => {
        access.value = response.access;
        refresh.value = response.refresh;
        user.value = response.user;

        localStorage.setItem("access", access.value);
        localStorage.setItem("refresh", refresh.value);
        localStorage.setItem("user", JSON.stringify(user.value));
    }
  
    const signUp = async (data) => {
      error.value = null; 
      try {
        if (data.role === "customer"){
            const response = await signUpCustomerService({
                username: data.username,
                email: data.email,
                phone_number: data.phoneNumber, 
                role: data.role,
                password: data.password,
                address: data.address,

            });

            setCredentials(response);

            return true;
        } else {
            const response = await signUpTechnicianService({
              username: data.username,
                email: data.email,
                phone_number: data.phoneNumber, 
                role: data.role,
                password: data.password,
                address: data.address,
                technician_profile: {
                  expertise: data.expertise,
                  experience_years: data.experienceInYears,
                  available: data.available
                }
            });

            setCredentials(response);
            return true;
        }
        
      } catch (err) {
        error.value = err.message; 
        return null;
      }
    };
  
    const signIn = async (data) => {
      error.value = null; 
      try {
        const response = await signInService(data);
        
        setCredentials(response);
        return true;

      } catch (err) {
        error.value = err.message;
        return null;
      }
    };
  
    const signOut = () => {
      access.value = null;
      refresh.value = null;
      user.value = null;

      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");

    };
  
    return {
      isAuthenticated,
      access,
      user,
      error,
      signUp,
      signIn,
      signOut,
    };
  });