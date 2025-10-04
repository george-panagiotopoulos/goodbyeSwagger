import { apiClient } from './api';
import type { Product, CreateProductRequest } from '../types/product';

interface ApiResponse<T> {
  success: boolean;
  data: T;
}

export const productService = {
  getAll: async (): Promise<Product[]> => {
    const response = await apiClient.get<ApiResponse<Product[]>>('/api/products');
    return response.data.data;
  },

  getActive: async (): Promise<Product[]> => {
    const response = await apiClient.get<ApiResponse<Product[]>>('/api/products/active');
    return response.data.data;
  },

  getById: async (id: string): Promise<Product> => {
    const response = await apiClient.get<ApiResponse<Product>>(`/api/products/${id}`);
    return response.data.data;
  },

  create: async (product: CreateProductRequest): Promise<Product> => {
    const response = await apiClient.post<ApiResponse<Product>>('/api/products', product);
    return response.data.data;
  },
};
