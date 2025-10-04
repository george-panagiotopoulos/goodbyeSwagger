import { apiClient } from './api';
import type { Account, CreateAccountRequest } from '../types/account';
import type { Transaction, CreditRequest, DebitRequest } from '../types/transaction';

interface ApiResponse<T> {
  success: boolean;
  data: T;
}

export const accountService = {
  getAll: async (): Promise<Account[]> => {
    const response = await apiClient.get<ApiResponse<Account[]>>('/api/accounts');
    return response.data.data;
  },

  getById: async (id: string): Promise<Account> => {
    const response = await apiClient.get<ApiResponse<Account>>(`/api/accounts/${id}`);
    return response.data.data;
  },

  create: async (account: CreateAccountRequest): Promise<Account> => {
    const response = await apiClient.post<ApiResponse<Account>>('/api/accounts', account);
    return response.data.data;
  },

  getTransactions: async (id: string): Promise<Transaction[]> => {
    const response = await apiClient.get<ApiResponse<Transaction[]>>(`/api/accounts/${id}/transactions`);
    return response.data.data;
  },

  credit: async (id: string, request: CreditRequest): Promise<Transaction> => {
    const response = await apiClient.post<ApiResponse<Transaction>>(`/api/accounts/${id}/credit`, request);
    return response.data.data;
  },

  debit: async (id: string, request: DebitRequest): Promise<Transaction> => {
    const response = await apiClient.post<ApiResponse<Transaction>>(`/api/accounts/${id}/debit`, request);
    return response.data.data;
  },
};
