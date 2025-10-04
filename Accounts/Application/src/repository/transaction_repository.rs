// Transaction repository
pub struct TransactionRepository;
impl TransactionRepository { pub fn new() -> Self { TransactionRepository } }
impl Default for TransactionRepository { fn default() -> Self { Self::new() } }
