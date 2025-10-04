export interface Transaction {
  transaction_id: string;
  account_id: string;
  transaction_type: 'Credit' | 'Debit';
  category: string;
  amount: string;
  currency: string;
  running_balance: string;
  description: string;
  reference: string;
  channel: string;
  transaction_date: string;
  value_date: string;
  created_at: string;
  created_by: string;
}

export interface CreditRequest {
  amount: string;
  description: string;
  reference: string;
}

export interface DebitRequest {
  amount: string;
  description: string;
  reference: string;
}
