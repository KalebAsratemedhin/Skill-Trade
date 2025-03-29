
export const signUpCustomerService = async (data) => {
  try {
    const response = await api.post(`auth/register/customer`, data);
    return response.data;
  } catch (error) {
    throw Error("Signup failed");
  }
};

export const signUpTechnicianService = async (data) => {
    try {
      const response = await api.post(`auth/register/technician`, data);
      return response.data;
    } catch (error) {
      throw new Error("Signup failed");
    }
  };

export const signInService = async (data) => {
  try {
    const response = await api.post(`auth/login`, data);
    return response.data;
  } catch (error) {
    throw new Error("Signin failed");
  }
};
