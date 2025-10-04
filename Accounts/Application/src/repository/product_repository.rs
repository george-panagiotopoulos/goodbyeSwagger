// Product repository - Database access for products
// TODO: Implement full CRUD operations

pub struct ProductRepository;

impl ProductRepository {
    pub fn new() -> Self {
        ProductRepository
    }
}

impl Default for ProductRepository {
    fn default() -> Self {
        Self::new()
    }
}
