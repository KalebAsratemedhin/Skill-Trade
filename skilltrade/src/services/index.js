import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: {
        "Content-Type": "application/json",
    },
});

// Attach token to all requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Handling 401 errors and refreshing token
api.interceptors.response.use(
    (response) => response, 
    async (error) => {
        const originalRequest = error.config;

        // If request is unauthorized and it's not a retry
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Request a new access token using refresh token
                const refreshToken = localStorage.getItem("refresh");
                if (!refreshToken) {
                    throw new Error("No refresh token available.");
                }

                const response = await axios.post("http://localhost:8000/api/auth/token/refresh", {
                    refresh: refreshToken
                });

                const newAccessToken = response.data.access;
                localStorage.setItem("access", newAccessToken);

                // Update the Authorization header with the new token
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

                // Retry the original request with the new token
                return api(originalRequest);
            } catch (refreshError) {
                console.error("Refresh token expired or invalid.", refreshError);
                localStorage.removeItem("access");
                localStorage.removeItem("refresh");
                window.location.href = "/login"; // Redirect to login page
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;
