use serde::{Deserialize, Serialize};
use rust_decimal::Decimal;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProductResponse {
    pub product_id: String,
    pub product_name: String,
    pub product_code: String,
    pub description: Option<String>,
    pub status: String,
    pub currency: String,
    pub interest_rate: Decimal,
    pub minimum_balance_for_interest: Decimal,
    pub monthly_maintenance_fee: Decimal,
    pub transaction_fee: Decimal,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateProductRequest {
    pub product_name: String,
    pub product_code: String,
    pub description: Option<String>,
    pub currency: String,
    pub interest_rate: Decimal,
    pub minimum_balance_for_interest: Decimal,
    pub monthly_maintenance_fee: Decimal,
    pub transaction_fee: Decimal,
}

#[derive(Debug, Deserialize)]
pub struct UpdateProductRequest {
    pub product_name: Option<String>,
    pub description: Option<String>,
    pub interest_rate: Option<Decimal>,
    pub minimum_balance_for_interest: Option<Decimal>,
    pub monthly_maintenance_fee: Option<Decimal>,
    pub transaction_fee: Option<Decimal>,
}
