export interface Customer {
  customer_id: string;
  external_customer_id: string;
  customer_name: string;
  customer_type: 'Individual' | 'Business';
  email: string;
  phone: string;
  address: string;
  status: 'Active' | 'Inactive' | 'Suspended';
  created_at: string;
  updated_at: string;
  _links?: Record<string, { href: string; method?: string }>;
}

export interface CreateCustomerRequest {
  external_customer_id: string;
  customer_name: string;
  customer_type: 'Individual' | 'Business';
  email: string;
  phone: string;
  address: string;
}
