use crate::domain::account::{Account, AccountStatus};
use crate::error::AppError;
use rusqlite::{params, Connection, OptionalExtension, Row};
use rust_decimal::Decimal;
use rust_decimal::prelude::ToPrimitive;
use std::str::FromStr;

pub struct AccountRepository {
    connection: Connection,
}

impl AccountRepository {
    pub fn new(db_path: &str) -> Result<Self, AppError> {
        let connection = Connection::open(db_path)?;
        Ok(AccountRepository { connection })
    }

    pub fn create(&self, account: &Account) -> Result<(), AppError> {
        self.connection.execute(
            "INSERT INTO accounts (
                account_id, account_number, product_id, customer_id, currency, balance,
                interest_accrued, status, opening_date, closing_date,
                created_at, updated_at
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12)",
            params![
                account.account_id,
                account.account_number,
                account.product_id,
                account.customer_id,
                account.currency,
                account.balance.to_f64().unwrap_or(0.0),
                account.interest_accrued.to_f64().unwrap_or(0.0),
                account.status.to_string(),
                account.opening_date.format("%Y-%m-%d").to_string(),
                account.closing_date.as_ref().map(|d| d.format("%Y-%m-%d").to_string()),
                account.created_at.format("%Y-%m-%d %H:%M:%S").to_string(),
                account.updated_at.format("%Y-%m-%d %H:%M:%S").to_string(),
            ],
        )?;
        Ok(())
    }

    pub fn find_by_id(&self, account_id: &str) -> Result<Option<Account>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT account_id, account_number, product_id, customer_id, balance,
                    interest_accrued, status, opening_date, closing_date,
                    created_at, updated_at
             FROM accounts WHERE account_id = ?1",
        )?;

        let account = stmt
            .query_row(params![account_id], |row| self.row_to_account(row))
            .optional()?;

        Ok(account)
    }

    pub fn find_by_account_number(&self, account_number: &str) -> Result<Option<Account>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT account_id, account_number, product_id, customer_id, balance,
                    interest_accrued, status, opening_date, closing_date,
                    created_at, updated_at
             FROM accounts WHERE account_number = ?1",
        )?;

        let account = stmt
            .query_row(params![account_number], |row| self.row_to_account(row))
            .optional()?;

        Ok(account)
    }

    pub fn find_by_customer(&self, customer_id: &str) -> Result<Vec<Account>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT account_id, account_number, product_id, customer_id, balance,
                    interest_accrued, status, opening_date, closing_date,
                    created_at, updated_at
             FROM accounts WHERE customer_id = ?1 ORDER BY opening_date DESC",
        )?;

        let accounts = stmt
            .query_map(params![customer_id], |row| self.row_to_account(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(accounts)
    }

    pub fn list_active(&self) -> Result<Vec<Account>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT account_id, account_number, product_id, customer_id, balance,
                    interest_accrued, status, opening_date, closing_date,
                    created_at, updated_at
             FROM accounts WHERE status = 'Active' ORDER BY opening_date DESC",
        )?;

        let accounts = stmt
            .query_map([], |row| self.row_to_account(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(accounts)
    }

    pub fn update(&self, account: &Account) -> Result<(), AppError> {
        let rows_affected = self.connection.execute(
            "UPDATE accounts SET
                balance = ?1, interest_accrued = ?2, status = ?3,
                closing_date = ?4, updated_at = ?5
             WHERE account_id = ?6",
            params![
                account.balance.to_f64().unwrap_or(0.0),
                account.interest_accrued.to_f64().unwrap_or(0.0),
                account.status.to_string(),
                account.closing_date.as_ref().map(|d| d.format("%Y-%m-%d").to_string()),
                account.updated_at.format("%Y-%m-%d %H:%M:%S").to_string(),
                account.account_id,
            ],
        )?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "Account".to_string(),
                account.account_id.clone()
            ));
        }

        Ok(())
    }

    pub fn delete(&self, account_id: &str) -> Result<(), AppError> {
        let rows_affected = self
            .connection
            .execute("DELETE FROM accounts WHERE account_id = ?1", params![account_id])?;

        if rows_affected == 0 {
            return Err(AppError::NotFoundError(
                "Account".to_string(),
                account_id.to_string()
            ));
        }

        Ok(())
    }

    fn row_to_account(&self, row: &Row) -> rusqlite::Result<Account> {
        let balance_f64: f64 = row.get(4)?;
        let balance = Decimal::from_f64_retain(balance_f64).unwrap_or(Decimal::ZERO);

        let interest_accrued_f64: f64 = row.get(5)?;
        let interest_accrued = Decimal::from_f64_retain(interest_accrued_f64).unwrap_or(Decimal::ZERO);

        let status_str: String = row.get(6)?;
        let status = AccountStatus::from_str(&status_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(6, rusqlite::types::Type::Text, Box::new(std::io::Error::new(std::io::ErrorKind::InvalidData, e))))?;

        let opened_date_str: String = row.get(7)?;
        let opened_date = chrono::NaiveDate::parse_from_str(&opened_date_str, "%Y-%m-%d")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(7, rusqlite::types::Type::Text, Box::new(e)))?;

        let closed_date: Option<String> = row.get(8)?;
        let closed_date = closed_date.map(|s| {
            chrono::NaiveDate::parse_from_str(&s, "%Y-%m-%d")
                .map_err(|e| rusqlite::Error::FromSqlConversionFailure(8, rusqlite::types::Type::Text, Box::new(e)))
        }).transpose()?;

        let created_at_str: String = row.get(9)?;
        let created_at = chrono::NaiveDateTime::parse_from_str(&created_at_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(9, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        let updated_at_str: String = row.get(10)?;
        let updated_at = chrono::NaiveDateTime::parse_from_str(&updated_at_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(10, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        Ok(Account {
            account_id: row.get(0)?,
            account_number: row.get(1)?,
            product_id: row.get(2)?,
            customer_id: row.get(3)?,
            currency: "USD".to_string(), // Default, should be from product or explicit column
            status,
            balance,
            interest_accrued,
            opening_date: opened_date,
            closing_date: closed_date,
            created_at,
            updated_at,
            created_by: None,
        })
    }
}
