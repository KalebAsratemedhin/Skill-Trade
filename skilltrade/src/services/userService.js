import api from "./index.js";
import { handleErrors } from "../utils/errorHandling";

export const getCurrentCustomerService = async() => {
    try {
        const response = await api.get(`auth/current/customer`);
        return response.data;
    } catch (error) {
        throw Error("current user couldn't be fetched.");
    }
}

export const getCurrentTechnicianService = async() => {
    try {
        const response = await api.get(`auth/current/technician`);
        return response.data;
    } catch (error) {
        throw Error("current user couldn't be fetched.");
    }
}