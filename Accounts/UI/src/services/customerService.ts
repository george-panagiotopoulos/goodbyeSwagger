import { apiClient } from './api';
import type { Customer, CreateCustomerRequest } from '../types/customer';

interface ApiResponse<T> {
  success: boolean;
  data: T;
}

export const customerService = {
  getAll: async (): Promise<Customer[]> => {
    const response = await apiClient.get<ApiResponse<Customer[]>>('/api/customers');
    return response.data.data;
  },

  getById: async (id: string): Promise<Customer> => {
    const response = await apiClient.get<ApiResponse<Customer>>(`/api/customers/${id}`);
    return response.data.data;
  },

  create: async (customer: CreateCustomerRequest): Promise<Customer> => {
    const response = await apiClient.post<ApiResponse<Customer>>('/api/customers', customer);
    return response.data.data;
  },
};
