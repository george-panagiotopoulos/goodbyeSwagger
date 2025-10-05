use rusqlite::Connection;

#[derive(Clone)]
pub struct AppState {
    pub db_path: String,
}

impl AppState {
    pub fn new(db_path: String) -> Self {
        AppState { db_path }
    }

    pub fn get_connection(&self) -> Result<Connection, rusqlite::Error> {
        Connection::open(&self.db_path)
    }
}
