// Account repository
pub struct AccountRepository;
impl AccountRepository { pub fn new() -> Self { AccountRepository } }
impl Default for AccountRepository { fn default() -> Self { Self::new() } }
