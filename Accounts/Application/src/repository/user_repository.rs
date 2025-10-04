// User repository
pub struct UserRepository;
impl UserRepository { pub fn new() -> Self { UserRepository } }
impl Default for UserRepository { fn default() -> Self { Self::new() } }
