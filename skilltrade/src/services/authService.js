import axios from "axios";
import { handleErrors } from "../utils/errorHandling";

const apiUrl = "http://localhost:8000/api/auth"; 

export const signUpCustomerService = async (data) => {
  try {
    const response = await axios.post(`${apiUrl}/register/customer`, data);
    return response.data;
  } catch (error) {
    throw Error("Signup failed");
  }
};

export const signUpTechnicianService = async (data) => {
    try {
      const response = await axios.post(`${apiUrl}/register/technician`, data);
      return response.data;
    } catch (error) {
      throw new Error("Signup failed");
    }
  };

export const signInService = async (data) => {
  try {
    const response = await axios.post(`${apiUrl}/login`, data);
    return response.data;
  } catch (error) {
    throw new Error("Signin failed");
  }
};
