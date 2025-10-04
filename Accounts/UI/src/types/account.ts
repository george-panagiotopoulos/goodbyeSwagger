export interface Account {
  account_id: string;
  account_number: string;
  product_id: string;
  customer_id: string;
  currency: string;
  balance: string;
  interest_accrued: string;
  status: 'Active' | 'Closed' | 'Frozen' | 'Dormant';
  opening_date: string;
  closing_date?: string;
  created_at: string;
  updated_at: string;
  _links?: Record<string, { href: string; method?: string }>;
}

export interface CreateAccountRequest {
  product_id: string;
  customer_id: string;
  opening_balance: string;
}
