use crate::domain::transaction::{Transaction, TransactionType, TransactionCategory};
use crate::error::AppError;
use rusqlite::{params, Connection, OptionalExtension, Row};
use rust_decimal::Decimal;
use std::str::FromStr;

pub struct TransactionRepository {
    connection: Connection,
}

impl TransactionRepository {
    pub fn new(db_path: &str) -> Result<Self, AppError> {
        let connection = Connection::open(db_path)?;
        Ok(TransactionRepository { connection })
    }

    pub fn create(&self, transaction: &Transaction) -> Result<(), AppError> {
        use rust_decimal::prelude::ToPrimitive;

        self.connection.execute(
            "INSERT INTO transactions (
                transaction_id, account_id, type, category, amount, currency,
                running_balance, description, reference, channel, transaction_date,
                value_date, created_at, created_by
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14)",
            params![
                transaction.transaction_id,
                transaction.account_id,
                transaction.transaction_type.to_string(),
                transaction.category.to_string(),
                transaction.amount.to_f64().unwrap_or(0.0),
                transaction.currency,
                transaction.running_balance.to_f64().unwrap_or(0.0),
                transaction.description,
                transaction.reference,
                transaction.channel,
                transaction.transaction_date.format("%Y-%m-%d %H:%M:%S").to_string(),
                transaction.value_date.format("%Y-%m-%d").to_string(),
                transaction.created_at.format("%Y-%m-%d %H:%M:%S").to_string(),
                transaction.created_by,
            ],
        )?;
        Ok(())
    }

    pub fn find_by_id(&self, transaction_id: &str) -> Result<Option<Transaction>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT transaction_id, account_id, type, category, amount, currency,
                    running_balance, description, reference, channel, transaction_date,
                    value_date, created_at, created_by
             FROM transactions WHERE transaction_id = ?1",
        )?;

        let transaction = stmt
            .query_row(params![transaction_id], |row| self.row_to_transaction(row))
            .optional()?;

        Ok(transaction)
    }

    pub fn find_by_account(&self, account_id: &str, limit: Option<usize>) -> Result<Vec<Transaction>, AppError> {
        let query = if let Some(lim) = limit {
            format!(
                "SELECT transaction_id, account_id, type, category, amount, currency,
                        running_balance, description, reference, channel, transaction_date,
                        value_date, created_at, created_by
                 FROM transactions WHERE account_id = ?1
                 ORDER BY created_at DESC LIMIT {}",
                lim
            )
        } else {
            "SELECT transaction_id, account_id, type, category, amount, currency,
                    running_balance, description, reference, channel, transaction_date,
                    value_date, created_at, created_by
             FROM transactions WHERE account_id = ?1
             ORDER BY created_at DESC".to_string()
        };

        let mut stmt = self.connection.prepare(&query)?;

        let transactions = stmt
            .query_map(params![account_id], |row| self.row_to_transaction(row))?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(transactions)
    }

    pub fn find_by_reference(&self, reference: &str) -> Result<Option<Transaction>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT transaction_id, account_id, type, category, amount, currency,
                    running_balance, description, reference, channel, transaction_date,
                    value_date, created_at, created_by
             FROM transactions WHERE reference = ?1",
        )?;

        let transaction = stmt
            .query_row(params![reference], |row| self.row_to_transaction(row))
            .optional()?;

        Ok(transaction)
    }

    pub fn find_by_date_range(
        &self,
        account_id: &str,
        start_date: &str,
        end_date: &str,
    ) -> Result<Vec<Transaction>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT transaction_id, account_id, type, category, amount, currency,
                    running_balance, description, reference, channel, transaction_date,
                    value_date, created_at, created_by
             FROM transactions
             WHERE account_id = ?1 AND created_at BETWEEN ?2 AND ?3
             ORDER BY created_at DESC",
        )?;

        let transactions = stmt
            .query_map(params![account_id, start_date, end_date], |row| {
                self.row_to_transaction(row)
            })?
            .collect::<Result<Vec<_>, _>>()?;

        Ok(transactions)
    }

    pub fn get_account_balance(&self, account_id: &str) -> Result<Option<Decimal>, AppError> {
        let mut stmt = self.connection.prepare(
            "SELECT running_balance FROM transactions
             WHERE account_id = ?1
             ORDER BY created_at DESC LIMIT 1",
        )?;

        let balance_str: Option<String> = stmt
            .query_row(params![account_id], |row| row.get(0))
            .optional()?;

        if let Some(balance) = balance_str {
            let decimal = Decimal::from_str(&balance)
                .map_err(|e| AppError::ValidationError(format!("Invalid balance format: {}", e)))?;
            Ok(Some(decimal))
        } else {
            Ok(None)
        }
    }

    fn row_to_transaction(&self, row: &Row) -> rusqlite::Result<Transaction> {
        use rust_decimal::prelude::FromPrimitive;

        let transaction_type_str: String = row.get(2)?;
        let transaction_type = TransactionType::from_str(&transaction_type_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(2, rusqlite::types::Type::Text, Box::new(std::io::Error::new(std::io::ErrorKind::InvalidData, e))))?;

        let category_str: String = row.get(3)?;
        let category = TransactionCategory::from_str(&category_str)
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(3, rusqlite::types::Type::Text, Box::new(std::io::Error::new(std::io::ErrorKind::InvalidData, e))))?;

        let amount_f64: f64 = row.get(4)?;
        let amount = Decimal::from_f64(amount_f64).unwrap_or(Decimal::ZERO);

        let balance_f64: f64 = row.get(6)?;
        let running_balance = Decimal::from_f64(balance_f64).unwrap_or(Decimal::ZERO);

        let transaction_date_str: String = row.get(10)?;
        let transaction_date = chrono::NaiveDateTime::parse_from_str(&transaction_date_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(10, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        let value_date_str: String = row.get(11)?;
        let value_date = chrono::NaiveDate::parse_from_str(&value_date_str, "%Y-%m-%d")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(11, rusqlite::types::Type::Text, Box::new(e)))?;

        let created_at_str: String = row.get(12)?;
        let created_at = chrono::NaiveDateTime::parse_from_str(&created_at_str, "%Y-%m-%d %H:%M:%S")
            .map_err(|e| rusqlite::Error::FromSqlConversionFailure(12, rusqlite::types::Type::Text, Box::new(e)))?
            .and_utc();

        Ok(Transaction {
            transaction_id: row.get(0)?,
            account_id: row.get(1)?,
            transaction_date,
            value_date,
            transaction_type,
            category,
            amount,
            currency: row.get(5)?,
            running_balance,
            description: row.get(7)?,
            reference: row.get(8)?,
            channel: row.get(9)?,
            status: "Posted".to_string(),
            created_at,
            created_by: row.get(13)?,
        })
    }
}
