import { apiClient } from './api';
import type { Account, CreateAccountRequest } from '../types/account';
import type { Transaction, CreditRequest, DebitRequest } from '../types/transaction';

export const accountService = {
  getAll: async (): Promise<Account[]> => {
    const response = await apiClient.get<Account[]>('/api/accounts');
    return response.data;
  },

  getById: async (id: string): Promise<Account> => {
    const response = await apiClient.get<Account>(`/api/accounts/${id}`);
    return response.data;
  },

  create: async (account: CreateAccountRequest): Promise<Account> => {
    const response = await apiClient.post<Account>('/api/accounts', account);
    return response.data;
  },

  getTransactions: async (id: string): Promise<Transaction[]> => {
    const response = await apiClient.get<Transaction[]>(`/api/accounts/${id}/transactions`);
    return response.data;
  },

  credit: async (id: string, request: CreditRequest): Promise<Transaction> => {
    const response = await apiClient.post<Transaction>(`/api/accounts/${id}/credit`, request);
    return response.data;
  },

  debit: async (id: string, request: DebitRequest): Promise<Transaction> => {
    const response = await apiClient.post<Transaction>(`/api/accounts/${id}/debit`, request);
    return response.data;
  },
};
