import { apiClient } from './api';
import type { Customer, CreateCustomerRequest } from '../types/customer';

export const customerService = {
  getAll: async (): Promise<Customer[]> => {
    const response = await apiClient.get<Customer[]>('/api/customers');
    return response.data;
  },

  getById: async (id: string): Promise<Customer> => {
    const response = await apiClient.get<Customer>(`/api/customers/${id}`);
    return response.data;
  },

  create: async (customer: CreateCustomerRequest): Promise<Customer> => {
    const response = await apiClient.post<Customer>('/api/customers', customer);
    return response.data;
  },
};
