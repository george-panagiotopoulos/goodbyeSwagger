export interface Product {
  product_id: string;
  product_code: string;
  product_name: string;
  description: string;
  currency: string;
  interest_rate: string;
  minimum_balance_for_interest: string;
  monthly_maintenance_fee: string;
  transaction_fee: string;
  status: 'Active' | 'Inactive';
  created_at: string;
  updated_at: string;
  _links?: Record<string, { href: string; method?: string }>;
}

export interface CreateProductRequest {
  product_name: string;
  product_code: string;
  description: string;
  currency: string;
  interest_rate: string;
  minimum_balance_for_interest: string;
  monthly_maintenance_fee: string;
  transaction_fee: string;
}
