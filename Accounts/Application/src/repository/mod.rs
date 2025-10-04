// Repository layer - Database access
// Repositories handle CRUD operations and database interactions

pub mod product_repository;
pub mod account_repository;
pub mod transaction_repository;
pub mod user_repository;
pub mod interest_repository;

// Re-export repository traits and implementations
pub use product_repository::ProductRepository;
pub use account_repository::AccountRepository;
pub use transaction_repository::TransactionRepository;
pub use user_repository::UserRepository;
pub use interest_repository::InterestRepository;
