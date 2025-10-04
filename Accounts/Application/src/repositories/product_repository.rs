use crate::domain::product::{Product, ProductStatus};
use crate::error::AppError;
use rusqlite::{params, Connection, OptionalExtension, Row};
use rust_decimal::Decimal;
use rust_decimal::prelude::ToPrimitive;
use std::str::FromStr;

pub struct ProductRepository {
    connection: Connection,
}

impl ProductRepository {
    pub fn new(db_path: &str) -> Result<Self, AppError> {
        let connection = Connection::open(db_path)?;
        Ok(ProductRepository { connection })
    }

    pub fn create(&self, product: &Product) -> Result<(), AppError> {
        self.connection.execute(
            "INSERT INTO products (
                product_id, product_name, product_code, status, currency,
                interest_rate, minimum_balance_for_interest, monthly_maintenance_fee,
                transaction_fee, created_at, updated_at
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)",
            params![
                product.product_id,
                product.product_name,
                product.product_code,
                product.status.to_string(),
                product.currency,
                product.interest_rate.to_f64().unwrap_or(0.0),
                product.minimum_balance_for_interest.to_f64().unwrap_or(0.0),
                product.monthly_maintenance_fee.to_f64().unwrap_or(0.0),
                product.transaction_fee.to_f64().unwrap_or(0.0),
                product.created_at.format("%Y-%m-%d %H:%M:%S").to_string(),
                product.updated_at.format("%Y-%m-%d %H:%M:%S").to_string(),
            ],
        )?;
        Ok(())
    }

    pub fn find_by_id(&self, product_id: &str) -> Result<Option<Product>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT product_id, product_name, product_code, status, currency,
                    interest_rate, minimum_balance_for_interest, monthly_maintenance_fee,
                    transaction_fee, created_at, updated_at
             FROM products WHERE product_id = ?1",
        )?;

        let product = stmt
            .query_row(params![product_id], |row| self.row_to_product(row))
            .optional()?;

        Ok(product)
    }

    pub fn find_by_code(&self, product_code: &str) -> Result<Option<Product>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT product_id, product_name, product_code, status, currency,
                    interest_rate, minimum_balance_for_interest, monthly_maintenance_fee,
                    transaction_fee, created_at, updated_at
             FROM products WHERE product_code = ?1",
        )?;

        let product = stmt
            .query_row(params![product_code], |row| self.row_to_product(row))
            .optional()?;

        Ok(product)
    }

    pub fn list_all(&self) -> Result<Vec<Product>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT product_id, product_name, product_code, status, currency,
                    interest_rate, minimum_balance_for_interest, monthly_maintenance_fee,
                    transaction_fee, created_at, updated_at
             FROM products ORDER BY created_at DESC",
        )?;

        let products = stmt
            .query_map([], |row| self.row_to_product(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(products)
    }

    pub fn list_active(&self) -> Result<Vec<Product>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT product_id, product_name, product_code, status, currency,
                    interest_rate, minimum_balance_for_interest, monthly_maintenance_fee,
                    transaction_fee, created_at, updated_at
             FROM products WHERE status = 'Active' ORDER BY product_name",
        )?;

        let products = stmt
            .query_map([], |row| self.row_to_product(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(products)
    }

    pub fn update(&self, product: &Product) -> Result<(), AppError> {
        let rows_affected = self.connection.execute(
            "UPDATE products SET
                product_name = ?1, status = ?2, interest_rate = ?3,
                minimum_balance_for_interest = ?4, monthly_maintenance_fee = ?5,
                transaction_fee = ?6, updated_at = ?7
             WHERE product_id = ?8",
            params![
                product.product_name,
                product.status.to_string(),
                product.interest_rate.to_f64().unwrap_or(0.0),
                product.minimum_balance_for_interest.to_f64().unwrap_or(0.0),
                product.monthly_maintenance_fee.to_f64().unwrap_or(0.0),
                product.transaction_fee.to_f64().unwrap_or(0.0),
                product.updated_at.format("%Y-%m-%d %H:%M:%S").to_string(),
                product.product_id,
            ],
        )?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "Product".to_string(),
                product.product_id.clone()
            ));
        }

        Ok(())
    }

    pub fn delete(&self, product_id: &str) -> Result<(), AppError> {
        let rows_affected = self
            .connection
            .execute("DELETE FROM products WHERE product_id = ?1", params![product_id])?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "Product".to_string(),
                product_id.to_string()
            ));
        }

        Ok(())
    }

    fn row_to_product(&self, row: &Row) -> rusqlite::Result<Product> {
        let status_str: String = row.get(3)?;
        let status = ProductStatus::from_str(&status_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(3, rusqlite::types::Type::Text, Box::new(std::io::Error::new(std::io::ErrorKind::InvalidData, e))))?;

        let interest_rate_f64: f64 = row.get(5)?;
        let interest_rate = Decimal::from_f64_retain(interest_rate_f64).unwrap_or(Decimal::ZERO);

        let min_balance_f64: f64 = row.get(6)?;
        let minimum_balance_for_interest = Decimal::from_f64_retain(min_balance_f64).unwrap_or(Decimal::ZERO);

        let maintenance_fee_f64: f64 = row.get(7)?;
        let monthly_maintenance_fee = Decimal::from_f64_retain(maintenance_fee_f64).unwrap_or(Decimal::ZERO);

        let transaction_fee_f64: f64 = row.get(8)?;
        let transaction_fee = Decimal::from_f64_retain(transaction_fee_f64).unwrap_or(Decimal::ZERO);

        let created_at_str: String = row.get(9)?;
        let created_at = chrono::NaiveDateTime::parse_from_str(&created_at_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(9, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        let updated_at_str: String = row.get(10)?;
        let updated_at = chrono::NaiveDateTime::parse_from_str(&updated_at_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(10, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        Ok(Product {
            product_id: row.get(0)?,
            product_name: row.get(1)?,
            product_code: row.get(2)?,
            description: None,
            status,
            currency: row.get(4)?,
            interest_rate,
            minimum_balance_for_interest,
            monthly_maintenance_fee,
            transaction_fee,
            created_at,
            updated_at,
            created_by: None,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::product::ProductStatus;
    use rust_decimal_macros::dec;
    use uuid::Uuid;

    fn setup_test_db() -> ProductRepository {
        let db_path = format!(":memory:");
        let repo = ProductRepository::new(&db_path).unwrap();

        // Create table
        repo.connection.execute(
            "CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                product_code TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL,
                currency TEXT NOT NULL,
                interest_rate REAL NOT NULL,
                minimum_balance_for_interest REAL NOT NULL,
                monthly_maintenance_fee REAL NOT NULL,
                transaction_fee REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )",
            [],
        ).unwrap();

        repo
    }

    #[test]
    fn test_create_and_find_product() {
        let repo = setup_test_db();
        let product = Product::new(
            "Test Savings".to_string(),
            "TST-SAV-001".to_string(),
            None,
            "USD".to_string(),
            dec!(0.05),
            dec!(100.00),
            dec!(5.00),
            dec!(0.50),
            None,
        ).unwrap();

        repo.create(&product).unwrap();

        let found = repo.find_by_id(&product.product_id).unwrap();
        assert!(found.is_some());
        let found_product = found.unwrap();
        assert_eq!(found_product.product_name, "Test Savings");
        assert_eq!(found_product.product_code, "TST-SAV-001");
    }

    #[test]
    fn test_list_active_products() {
        let repo = setup_test_db();

        let mut product1 = Product::new(
            "Active Product".to_string(),
            "ACT-001".to_string(),
            None,
            "USD".to_string(),
            dec!(0.05),
            dec!(100.00),
            dec!(5.00),
            dec!(0.50),
            None,
        ).unwrap();

        let mut product2 = Product::new(
            "Inactive Product".to_string(),
            "INACT-001".to_string(),
            None,
            "USD".to_string(),
            dec!(0.03),
            dec!(50.00),
            dec!(3.00),
            dec!(0.25),
            None,
        ).unwrap();

        product2.deactivate();

        repo.create(&product1).unwrap();
        repo.create(&product2).unwrap();

        let active_products = repo.list_active().unwrap();
        assert_eq!(active_products.len(), 1);
        assert_eq!(active_products[0].product_code, "ACT-001");
    }
}
