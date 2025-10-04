// Error types for the application layer

use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    // Database errors
    #[error("Database error: {0}")]
    DatabaseError(#[from] rusqlite::Error),

    // Validation errors
    #[error("Validation error: {0}")]
    ValidationError(String),

    // Business rule errors
    #[error("Business rule violation: {0}")]
    BusinessRuleError(String),

    // Not found errors
    #[error("{0} not found with id: {1}")]
    NotFoundError(String, String),

    // Insufficient balance
    #[error("Insufficient balance: available {available}, required {required}")]
    InsufficientBalance {
        available: rust_decimal::Decimal,
        required: rust_decimal::Decimal,
    },

    // Account closed
    #[error("Account is closed and cannot perform this operation")]
    AccountClosed,

    // Product inactive
    #[error("Product is inactive and cannot be used for new accounts")]
    ProductInactive,

    // Authentication errors
    #[error("Authentication failed: {0}")]
    AuthenticationError(String),

    // Password hashing errors
    #[error("Password hashing error: {0}")]
    PasswordHashError(String),

    // Generic errors
    #[error("Internal error: {0}")]
    InternalError(String),
}

pub type AppResult<T> = Result<T, AppError>;

// Helper implementations
impl From<bcrypt::BcryptError> for AppError {
    fn from(err: bcrypt::BcryptError) -> Self {
        AppError::PasswordHashError(err.to_string())
    }
}
