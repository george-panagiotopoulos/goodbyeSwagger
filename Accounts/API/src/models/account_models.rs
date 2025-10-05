use serde::{Deserialize, Serialize};
use rust_decimal::Decimal;

#[derive(Debug, Serialize, Deserialize)]
pub struct AccountResponse {
    pub account_id: String,
    pub account_number: String,
    pub customer_id: String,
    pub product_id: String,
    pub currency: String,
    pub status: String,
    pub balance: Decimal,
    pub interest_accrued: Decimal,
    pub opening_date: String,
    pub closing_date: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateAccountRequest {
    pub customer_id: String,
    pub product_id: String,
    pub opening_balance: String, // Changed to String to match UI
}

#[derive(Debug, Deserialize)]
pub struct TransactionRequest {
    pub amount: Decimal,
    pub description: String,
    pub reference: Option<String>,
}
