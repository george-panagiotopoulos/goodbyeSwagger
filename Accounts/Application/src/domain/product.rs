// Product domain model

use chrono::{DateTime, Utc};
use rust_decimal::Decimal;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ProductStatus {
    Active,
    Inactive,
}

impl ProductStatus {
    pub fn as_str(&self) -> &str {
        match self {
            ProductStatus::Active => "Active",
            ProductStatus::Inactive => "Inactive",
        }
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "Active" => Ok(ProductStatus::Active),
            "Inactive" => Ok(ProductStatus::Inactive),
            _ => Err(format!("Invalid product status: {}", s)),
        }
    }
}

impl std::fmt::Display for ProductStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Product {
    pub product_id: String,
    pub product_name: String,
    pub product_code: String,
    pub description: Option<String>,
    pub status: ProductStatus,
    pub currency: String,

    // Interest configuration (MVP: simple interest only)
    pub interest_rate: Decimal,  // Annual rate (e.g., 0.025 for 2.5%)
    pub minimum_balance_for_interest: Decimal,

    // Fee configuration (MVP: fixed amounts only)
    pub monthly_maintenance_fee: Decimal,
    pub transaction_fee: Decimal,

    // Audit fields
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub created_by: Option<String>,
}

impl Product {
    /// Create a new product with validation
    pub fn new(
        product_name: String,
        product_code: String,
        description: Option<String>,
        currency: String,
        interest_rate: Decimal,
        minimum_balance_for_interest: Decimal,
        monthly_maintenance_fee: Decimal,
        transaction_fee: Decimal,
        created_by: Option<String>,
    ) -> Result<Self, String> {
        // Validation
        if product_name.trim().is_empty() {
            return Err("Product name cannot be empty".to_string());
        }
        if product_code.trim().is_empty() {
            return Err("Product code cannot be empty".to_string());
        }
        if currency.len() != 3 {
            return Err("Currency code must be exactly 3 characters".to_string());
        }
        if interest_rate < Decimal::ZERO || interest_rate > Decimal::ONE {
            return Err("Interest rate must be between 0 and 1".to_string());
        }
        if minimum_balance_for_interest < Decimal::ZERO {
            return Err("Minimum balance for interest cannot be negative".to_string());
        }
        if monthly_maintenance_fee < Decimal::ZERO {
            return Err("Monthly maintenance fee cannot be negative".to_string());
        }
        if transaction_fee < Decimal::ZERO {
            return Err("Transaction fee cannot be negative".to_string());
        }

        let now = Utc::now();
        let product_id = format!("PROD-{}", uuid::Uuid::new_v4());

        Ok(Product {
            product_id,
            product_name,
            product_code,
            description,
            status: ProductStatus::Active,
            currency,
            interest_rate,
            minimum_balance_for_interest,
            monthly_maintenance_fee,
            transaction_fee,
            created_at: now,
            updated_at: now,
            created_by,
        })
    }

    /// Check if product is active
    pub fn is_active(&self) -> bool {
        matches!(self.status, ProductStatus::Active)
    }

    /// Activate product
    pub fn activate(&mut self) {
        self.status = ProductStatus::Active;
        self.updated_at = Utc::now();
    }

    /// Deactivate product
    pub fn deactivate(&mut self) {
        self.status = ProductStatus::Inactive;
        self.updated_at = Utc::now();
    }

    /// Update product configuration
    pub fn update(
        &mut self,
        product_name: Option<String>,
        description: Option<String>,
        interest_rate: Option<Decimal>,
        minimum_balance_for_interest: Option<Decimal>,
        monthly_maintenance_fee: Option<Decimal>,
        transaction_fee: Option<Decimal>,
    ) -> Result<(), String> {
        if let Some(name) = product_name {
            if name.trim().is_empty() {
                return Err("Product name cannot be empty".to_string());
            }
            self.product_name = name;
        }

        if let Some(desc) = description {
            self.description = Some(desc);
        }

        if let Some(rate) = interest_rate {
            if rate < Decimal::ZERO || rate > Decimal::ONE {
                return Err("Interest rate must be between 0 and 1".to_string());
            }
            self.interest_rate = rate;
        }

        if let Some(min_balance) = minimum_balance_for_interest {
            if min_balance < Decimal::ZERO {
                return Err("Minimum balance cannot be negative".to_string());
            }
            self.minimum_balance_for_interest = min_balance;
        }

        if let Some(fee) = monthly_maintenance_fee {
            if fee < Decimal::ZERO {
                return Err("Monthly fee cannot be negative".to_string());
            }
            self.monthly_maintenance_fee = fee;
        }

        if let Some(fee) = transaction_fee {
            if fee < Decimal::ZERO {
                return Err("Transaction fee cannot be negative".to_string());
            }
            self.transaction_fee = fee;
        }

        self.updated_at = Utc::now();
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rust_decimal_macros::dec;

    #[test]
    fn test_create_valid_product() {
        let product = Product::new(
            "Basic Checking".to_string(),
            "CHK-BASIC-001".to_string(),
            Some("A basic checking account".to_string()),
            "USD".to_string(),
            dec!(0.025),  // 2.5%
            dec!(100.00),
            dec!(5.00),
            dec!(1.00),
            Some("USR-001".to_string()),
        );

        assert!(product.is_ok());
        let p = product.unwrap();
        assert_eq!(p.product_name, "Basic Checking");
        assert_eq!(p.interest_rate, dec!(0.025));
        assert!(p.is_active());
    }

    #[test]
    fn test_invalid_currency_code() {
        let product = Product::new(
            "Basic Checking".to_string(),
            "CHK-BASIC-001".to_string(),
            None,
            "US".to_string(),  // Invalid: only 2 chars
            dec!(0.025),
            dec!(100.00),
            dec!(5.00),
            dec!(1.00),
            None,
        );

        assert!(product.is_err());
    }

    #[test]
    fn test_invalid_interest_rate() {
        let product = Product::new(
            "Basic Checking".to_string(),
            "CHK-BASIC-001".to_string(),
            None,
            "USD".to_string(),
            dec!(1.5),  // Invalid: > 1
            dec!(100.00),
            dec!(5.00),
            dec!(1.00),
            None,
        );

        assert!(product.is_err());
    }

    #[test]
    fn test_product_status_change() {
        let mut product = Product::new(
            "Basic Checking".to_string(),
            "CHK-BASIC-001".to_string(),
            None,
            "USD".to_string(),
            dec!(0.025),
            dec!(100.00),
            dec!(5.00),
            dec!(1.00),
            None,
        ).unwrap();

        assert!(product.is_active());

        product.deactivate();
        assert!(!product.is_active());

        product.activate();
        assert!(product.is_active());
    }
}
