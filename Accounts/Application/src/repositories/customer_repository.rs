use crate::domain::customer::{Customer, CustomerStatus, CustomerType};
use crate::error::AppError;
use rusqlite::{params, Connection, OptionalExtension, Row};
use std::str::FromStr;

pub struct CustomerRepository {
    connection: Connection,
}

impl CustomerRepository {
    pub fn new(db_path: &str) -> Result<Self, AppError> {
        let connection = Connection::open(db_path)?;
        Ok(CustomerRepository { connection })
    }

    pub fn create(&self, customer: &Customer) -> Result<(), AppError> {
        self.connection.execute(
            "INSERT INTO customers (
                customer_id, external_customer_id, customer_name, customer_type,
                status, email, phone, created_at, updated_at
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)",
            params![
                customer.customer_id,
                customer.external_customer_id,
                customer.customer_name,
                customer.customer_type.to_string(),
                customer.status.to_string(),
                customer.email,
                customer.phone,
                customer.created_at.format("%Y-%m-%d %H:%M:%S").to_string(),
                customer.updated_at.format("%Y-%m-%d %H:%M:%S").to_string(),
            ],
        )?;
        Ok(())
    }

    pub fn find_by_id(&self, customer_id: &str) -> Result<Option<Customer>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT customer_id, external_customer_id, customer_name, customer_type,
                    status, email, phone, created_at, updated_at
             FROM customers WHERE customer_id = ?1",
        )?;

        let customer = stmt
            .query_row(params![customer_id], |row| self.row_to_customer(row))
            .optional()?;

        Ok(customer)
    }

    pub fn find_by_external_id(&self, external_id: &str) -> Result<Option<Customer>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT customer_id, external_customer_id, customer_name, customer_type,
                    status, email, phone, created_at, updated_at
             FROM customers WHERE external_customer_id = ?1",
        )?;

        let customer = stmt
            .query_row(params![external_id], |row| self.row_to_customer(row))
            .optional()?;

        Ok(customer)
    }

    pub fn list_all(&self) -> Result<Vec<Customer>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT customer_id, external_customer_id, customer_name, customer_type,
                    status, email, phone, created_at, updated_at
             FROM customers ORDER BY customer_name",
        )?;

        let customers = stmt
            .query_map([], |row| self.row_to_customer(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(customers)
    }

    pub fn list_active(&self) -> Result<Vec<Customer>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT customer_id, external_customer_id, customer_name, customer_type,
                    status, email, phone, created_at, updated_at
             FROM customers WHERE status = 'Active' ORDER BY customer_name",
        )?;

        let customers = stmt
            .query_map([], |row| self.row_to_customer(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(customers)
    }

    pub fn list_by_type(&self, customer_type: CustomerType) -> Result<Vec<Customer>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT customer_id, external_customer_id, customer_name, customer_type,
                    status, email, phone, created_at, updated_at
             FROM customers WHERE customer_type = ?1 ORDER BY customer_name",
        )?;

        let customers = stmt
            .query_map(params![customer_type.to_string()], |row| self.row_to_customer(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(customers)
    }

    pub fn update(&self, customer: &Customer) -> Result<(), AppError> {
        let rows_affected = self.connection.execute(
            "UPDATE customers SET
                customer_name = ?1, status = ?2, email = ?3, phone = ?4, updated_at = ?5
             WHERE customer_id = ?6",
            params![
                customer.customer_name,
                customer.status.to_string(),
                customer.email,
                customer.phone,
                customer.updated_at.format("%Y-%m-%d %H:%M:%S").to_string(),
                customer.customer_id,
            ],
        )?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "Customer".to_string(),
                customer.customer_id.clone(),
            ));
        }

        Ok(())
    }

    pub fn delete(&self, customer_id: &str) -> Result<(), AppError> {
        let rows_affected = self
            .connection
            .execute("DELETE FROM customers WHERE customer_id = ?1", params![customer_id])?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "Customer".to_string(),
                customer_id.to_string(),
            ));
        }

        Ok(())
    }

    fn row_to_customer(&self, row: &Row) -> rusqlite::Result<Customer> {
        let customer_type_str: String = row.get(3)?;
        let customer_type = CustomerType::from_str(&customer_type_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(3, rusqlite::types::Type::Text, Box::new(std::io::Error::new(std::io::ErrorKind::InvalidData, e))))?;

        let status_str: String = row.get(4)?;
        let status = CustomerStatus::from_str(&status_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(4, rusqlite::types::Type::Text, Box::new(std::io::Error::new(std::io::ErrorKind::InvalidData, e))))?;

        let created_at_str: String = row.get(7)?;
        let created_at = chrono::NaiveDateTime::parse_from_str(&created_at_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(7, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        let updated_at_str: String = row.get(8)?;
        let updated_at = chrono::NaiveDateTime::parse_from_str(&updated_at_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(8, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        Ok(Customer {
            customer_id: row.get(0)?,
            external_customer_id: row.get(1)?,
            customer_name: row.get(2)?,
            customer_type,
            status,
            email: row.get(5)?,
            phone: row.get(6)?,
            created_at,
            updated_at,
        })
    }
}
