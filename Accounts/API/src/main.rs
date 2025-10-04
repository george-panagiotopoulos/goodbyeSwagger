use actix_web::{middleware::Logger, web, App, HttpResponse, HttpServer};
use actix_cors::Cors;
use dotenv::dotenv;
use std::env;

mod handlers;
mod models;
mod app_state;

use app_state::AppState;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Load environment variables
    dotenv().ok();

    // Initialize logger
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    // Get configuration from environment
    let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("PORT").unwrap_or_else(|_| "6600".to_string());
    let db_path = env::var("DATABASE_PATH")
        .unwrap_or_else(|_| "../Database/accounts.db".to_string());
    let bind_address = format!("{}:{}", host, port);

    log::info!("Starting Accounts API server at http://{}", bind_address);
    log::info!("Database: {}", db_path);

    // Create shared application state
    let app_state = AppState::new(db_path);

    // Start HTTP server
    HttpServer::new(move || {
        // Configure CORS
        let cors = Cors::default()
            .allowed_origin("http://localhost:6601") // React UI
            .allowed_methods(vec!["GET", "POST", "PUT", "PATCH", "DELETE"])
            .allowed_headers(vec![
                actix_web::http::header::AUTHORIZATION,
                actix_web::http::header::ACCEPT,
                actix_web::http::header::CONTENT_TYPE,
            ])
            .max_age(3600);

        App::new()
            .app_data(web::Data::new(app_state.clone()))
            .wrap(cors)
            .wrap(Logger::default())
            .route("/", web::get().to(health_check))
            .route("/health", web::get().to(health_check))
            .service(
                web::scope("/api")
                    // Product routes
                    .service(
                        web::scope("/products")
                            .route("", web::get().to(handlers::product_handlers::list_products))
                            .route("", web::post().to(handlers::product_handlers::create_product))
                            .route("/active", web::get().to(handlers::product_handlers::list_active_products))
                            .route("/{id}", web::get().to(handlers::product_handlers::get_product))
                    )
                    // Customer routes
                    .service(
                        web::scope("/customers")
                            .route("", web::get().to(handlers::customer_handlers::list_customers))
                            .route("", web::post().to(handlers::customer_handlers::create_customer))
                            .route("/{id}", web::get().to(handlers::customer_handlers::get_customer))
                    )
                    // Account routes
                    .service(
                        web::scope("/accounts")
                            .route("", web::get().to(handlers::account_handlers::list_accounts))
                            .route("", web::post().to(handlers::account_handlers::create_account))
                            .route("/{id}", web::get().to(handlers::account_handlers::get_account))
                            .route("/{id}/debit", web::post().to(handlers::account_handlers::debit_account))
                            .route("/{id}/credit", web::post().to(handlers::account_handlers::credit_account))
                            .route("/{id}/transactions", web::get().to(handlers::account_handlers::get_account_transactions))
                    )
            )
    })
    .bind(&bind_address)?
    .run()
    .await
}

async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "service": "accounts-api",
        "version": env!("CARGO_PKG_VERSION")
    }))
}
