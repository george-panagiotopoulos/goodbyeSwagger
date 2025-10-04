// Customer domain model

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum CustomerType {
    Individual,
    Business,
}

impl CustomerType {
    pub fn as_str(&self) -> &str {
        match self {
            CustomerType::Individual => "Individual",
            CustomerType::Business => "Business",
        }
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "Individual" => Ok(CustomerType::Individual),
            "Business" => Ok(CustomerType::Business),
            _ => Err(format!("Invalid customer type: {}", s)),
        }
    }
}

impl std::fmt::Display for CustomerType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum CustomerStatus {
    Active,
    Inactive,
    Suspended,
}

impl CustomerStatus {
    pub fn as_str(&self) -> &str {
        match self {
            CustomerStatus::Active => "Active",
            CustomerStatus::Inactive => "Inactive",
            CustomerStatus::Suspended => "Suspended",
        }
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "Active" => Ok(CustomerStatus::Active),
            "Inactive" => Ok(CustomerStatus::Inactive),
            "Suspended" => Ok(CustomerStatus::Suspended),
            _ => Err(format!("Invalid customer status: {}", s)),
        }
    }
}

impl std::fmt::Display for CustomerStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Customer {
    pub customer_id: String,
    pub external_customer_id: Option<String>, // ID from external system
    pub customer_name: String,
    pub customer_type: CustomerType,
    pub status: CustomerStatus,
    pub email: Option<String>,
    pub phone: Option<String>,

    // Audit fields
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Customer {
    /// Create a new customer
    pub fn new(
        customer_name: String,
        customer_type: CustomerType,
        external_customer_id: Option<String>,
        email: Option<String>,
        phone: Option<String>,
    ) -> Result<Self, String> {
        // Validation
        if customer_name.trim().is_empty() {
            return Err("Customer name cannot be empty".to_string());
        }

        // Validate email if provided
        if let Some(ref e) = email {
            if !e.trim().is_empty() && !e.contains('@') {
                return Err("Invalid email address".to_string());
            }
        }

        let now = Utc::now();
        let customer_id = format!("CUST-{}", uuid::Uuid::new_v4());

        Ok(Customer {
            customer_id,
            external_customer_id,
            customer_name,
            customer_type,
            status: CustomerStatus::Active,
            email,
            phone,
            created_at: now,
            updated_at: now,
        })
    }

    /// Check if customer is active
    pub fn is_active(&self) -> bool {
        matches!(self.status, CustomerStatus::Active)
    }

    /// Activate customer
    pub fn activate(&mut self) {
        self.status = CustomerStatus::Active;
        self.updated_at = Utc::now();
    }

    /// Deactivate customer
    pub fn deactivate(&mut self) {
        self.status = CustomerStatus::Inactive;
        self.updated_at = Utc::now();
    }

    /// Suspend customer
    pub fn suspend(&mut self) {
        self.status = CustomerStatus::Suspended;
        self.updated_at = Utc::now();
    }

    /// Update customer information
    pub fn update(
        &mut self,
        customer_name: Option<String>,
        email: Option<String>,
        phone: Option<String>,
    ) -> Result<(), String> {
        if let Some(name) = customer_name {
            if name.trim().is_empty() {
                return Err("Customer name cannot be empty".to_string());
            }
            self.customer_name = name;
        }

        if let Some(e) = email {
            if !e.trim().is_empty() && !e.contains('@') {
                return Err("Invalid email address".to_string());
            }
            self.email = Some(e);
        }

        if let Some(p) = phone {
            self.phone = Some(p);
        }

        self.updated_at = Utc::now();
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_individual_customer() {
        let customer = Customer::new(
            "John Doe".to_string(),
            CustomerType::Individual,
            Some("EXT-12345".to_string()),
            Some("john@example.com".to_string()),
            Some("+1-555-0100".to_string()),
        );

        assert!(customer.is_ok());
        let c = customer.unwrap();
        assert_eq!(c.customer_name, "John Doe");
        assert_eq!(c.customer_type, CustomerType::Individual);
        assert!(c.is_active());
        assert_eq!(c.external_customer_id, Some("EXT-12345".to_string()));
    }

    #[test]
    fn test_create_business_customer() {
        let customer = Customer::new(
            "Acme Corp".to_string(),
            CustomerType::Business,
            None,
            Some("contact@acme.com".to_string()),
            None,
        );

        assert!(customer.is_ok());
        let c = customer.unwrap();
        assert_eq!(c.customer_type, CustomerType::Business);
    }

    #[test]
    fn test_invalid_email() {
        let customer = Customer::new(
            "John Doe".to_string(),
            CustomerType::Individual,
            None,
            Some("invalid-email".to_string()),
            None,
        );

        assert!(customer.is_err());
    }

    #[test]
    fn test_customer_status_changes() {
        let mut customer = Customer::new(
            "John Doe".to_string(),
            CustomerType::Individual,
            None,
            Some("john@example.com".to_string()),
            None,
        )
        .unwrap();

        assert!(customer.is_active());

        customer.suspend();
        assert_eq!(customer.status, CustomerStatus::Suspended);

        customer.deactivate();
        assert_eq!(customer.status, CustomerStatus::Inactive);
        assert!(!customer.is_active());

        customer.activate();
        assert!(customer.is_active());
    }

    #[test]
    fn test_update_customer() {
        let mut customer = Customer::new(
            "John Doe".to_string(),
            CustomerType::Individual,
            None,
            Some("john@example.com".to_string()),
            None,
        )
        .unwrap();

        let result = customer.update(
            Some("Jane Doe".to_string()),
            Some("jane@example.com".to_string()),
            Some("+1-555-9999".to_string()),
        );

        assert!(result.is_ok());
        assert_eq!(customer.customer_name, "Jane Doe");
        assert_eq!(customer.email, Some("jane@example.com".to_string()));
        assert_eq!(customer.phone, Some("+1-555-9999".to_string()));
    }
}
