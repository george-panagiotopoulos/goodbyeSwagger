use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct CustomerResponse {
    pub customer_id: String,
    pub external_customer_id: Option<String>,
    pub customer_name: String,
    pub customer_type: String,
    pub status: String,
    pub email: Option<String>,
    pub phone: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateCustomerRequest {
    pub customer_name: String,
    pub customer_type: String, // "Individual" or "Business"
    pub external_customer_id: Option<String>,
    pub email: Option<String>,
    pub phone: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct UpdateCustomerRequest {
    pub customer_name: Option<String>,
    pub email: Option<String>,
    pub phone: Option<String>,
}
