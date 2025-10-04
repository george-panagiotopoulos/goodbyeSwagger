use actix_web::{web, HttpResponse, Result};
use accounts_application::repositories::{AccountRepository, TransactionRepository};
use accounts_application::domain::account::Account;
use accounts_application::domain::transaction::{Transaction, TransactionType, TransactionCategory};
use crate::app_state::AppState;
use crate::models::common::ApiResponse;
use crate::models::account_models::*;
use rust_decimal::Decimal;

pub async fn list_accounts(state: web::Data<AppState>) -> Result<HttpResponse> {
    let repo = AccountRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let accounts = repo
        .list_active()
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response: Vec<AccountResponse> = accounts
        .into_iter()
        .map(|a| AccountResponse {
            account_id: a.account_id,
            account_number: a.account_number,
            customer_id: a.customer_id,
            product_id: a.product_id,
            currency: a.currency,
            status: a.status.as_str().to_string(),
            balance: a.balance,
            interest_accrued: a.interest_accrued,
            opening_date: a.opening_date.format("%Y-%m-%d").to_string(),
            closing_date: a.closing_date.map(|d| d.format("%Y-%m-%d").to_string()),
            created_at: a.created_at.to_rfc3339(),
            updated_at: a.updated_at.to_rfc3339(),
        })
        .collect();

    Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
}

pub async fn get_account(
    state: web::Data<AppState>,
    account_id: web::Path<String>,
) -> Result<HttpResponse> {
    let repo = AccountRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    match repo.find_by_id(&account_id).map_err(|e| actix_web::error::ErrorInternalServerError(e))? {
        Some(a) => {
            let response = AccountResponse {
                account_id: a.account_id,
                account_number: a.account_number,
                customer_id: a.customer_id,
                product_id: a.product_id,
                currency: a.currency,
                status: a.status.as_str().to_string(),
                balance: a.balance,
                interest_accrued: a.interest_accrued,
                opening_date: a.opening_date.format("%Y-%m-%d").to_string(),
                closing_date: a.closing_date.map(|d| d.format("%Y-%m-%d").to_string()),
                created_at: a.created_at.to_rfc3339(),
                updated_at: a.updated_at.to_rfc3339(),
            };
            Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
        }
        None => Ok(HttpResponse::NotFound().json(ApiResponse::<()>::error(
            "NOT_FOUND".to_string(),
            format!("Account {} not found", account_id),
        ))),
    }
}

pub async fn create_account(
    state: web::Data<AppState>,
    req: web::Json<CreateAccountRequest>,
) -> Result<HttpResponse> {
    let account = Account::new(
        req.account_number.clone(),
        req.customer_id.clone(),
        req.product_id.clone(),
        req.currency.clone(),
        req.opening_balance,
        None, // created_by - TODO: get from auth context
    )
    .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    let repo = AccountRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    repo.create(&account)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Create opening transaction
    if req.opening_balance > Decimal::ZERO {
        let transaction = Transaction::new(
            account.account_id.clone(),
            TransactionType::Credit,
            TransactionCategory::Opening,
            req.opening_balance,
            req.currency.clone(),
            req.opening_balance, // running balance
            "Opening balance".to_string(),
            Some("OPENING".to_string()),
            "API".to_string(),
            None, // created_by - TODO: get from auth context
        )
        .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

        let txn_repo = TransactionRepository::new(&state.db_path)
            .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;
        txn_repo
            .create(&transaction)
            .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;
    }

    let response = AccountResponse {
        account_id: account.account_id.clone(),
        account_number: account.account_number,
        customer_id: account.customer_id,
        product_id: account.product_id,
        currency: account.currency,
        status: account.status.as_str().to_string(),
        balance: account.balance,
        interest_accrued: account.interest_accrued,
        opening_date: account.opening_date.format("%Y-%m-%d").to_string(),
        closing_date: account.closing_date.map(|d| d.format("%Y-%m-%d").to_string()),
        created_at: account.created_at.to_rfc3339(),
        updated_at: account.updated_at.to_rfc3339(),
    };

    Ok(HttpResponse::Created().json(ApiResponse::success(response)))
}

pub async fn debit_account(
    state: web::Data<AppState>,
    account_id: web::Path<String>,
    req: web::Json<TransactionRequest>,
) -> Result<HttpResponse> {
    // Get account
    let account_repo = AccountRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let mut account = account_repo
        .find_by_id(&account_id)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?
        .ok_or_else(|| actix_web::error::ErrorNotFound(format!("Account {} not found", account_id)))?;

    // Debit the account
    account
        .debit(req.amount)
        .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    // Update account in database
    account_repo
        .update(&account)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Create transaction record
    let transaction = Transaction::new(
        account.account_id.clone(),
        TransactionType::Debit,
        TransactionCategory::Withdrawal,
        req.amount,
        account.currency.clone(),
        account.balance,
        req.description.clone(),
        req.reference.clone(),
        "API".to_string(),
        None, // created_by - TODO: get from auth context
    )
    .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    let txn_repo = TransactionRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;
    txn_repo
        .create(&transaction)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response = AccountResponse {
        account_id: account.account_id.clone(),
        account_number: account.account_number,
        customer_id: account.customer_id,
        product_id: account.product_id,
        currency: account.currency,
        status: account.status.as_str().to_string(),
        balance: account.balance,
        interest_accrued: account.interest_accrued,
        opening_date: account.opening_date.format("%Y-%m-%d").to_string(),
        closing_date: account.closing_date.map(|d| d.format("%Y-%m-%d").to_string()),
        created_at: account.created_at.to_rfc3339(),
        updated_at: account.updated_at.to_rfc3339(),
    };

    Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
}

pub async fn credit_account(
    state: web::Data<AppState>,
    account_id: web::Path<String>,
    req: web::Json<TransactionRequest>,
) -> Result<HttpResponse> {
    // Get account
    let account_repo = AccountRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let mut account = account_repo
        .find_by_id(&account_id)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?
        .ok_or_else(|| actix_web::error::ErrorNotFound(format!("Account {} not found", account_id)))?;

    // Credit the account
    account
        .credit(req.amount)
        .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    // Update account in database
    account_repo
        .update(&account)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    // Create transaction record
    let transaction = Transaction::new(
        account.account_id.clone(),
        TransactionType::Credit,
        TransactionCategory::Deposit,
        req.amount,
        account.currency.clone(),
        account.balance,
        req.description.clone(),
        req.reference.clone(),
        "API".to_string(),
        None, // created_by - TODO: get from auth context
    )
    .map_err(|e| actix_web::error::ErrorBadRequest(e))?;

    let txn_repo = TransactionRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;
    txn_repo
        .create(&transaction)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response = AccountResponse {
        account_id: account.account_id.clone(),
        account_number: account.account_number,
        customer_id: account.customer_id,
        product_id: account.product_id,
        currency: account.currency,
        status: account.status.as_str().to_string(),
        balance: account.balance,
        interest_accrued: account.interest_accrued,
        opening_date: account.opening_date.format("%Y-%m-%d").to_string(),
        closing_date: account.closing_date.map(|d| d.format("%Y-%m-%d").to_string()),
        created_at: account.created_at.to_rfc3339(),
        updated_at: account.updated_at.to_rfc3339(),
    };

    Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
}

pub async fn get_account_transactions(
    state: web::Data<AppState>,
    account_id: web::Path<String>,
) -> Result<HttpResponse> {
    let repo = TransactionRepository::new(&state.db_path)
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let transactions = repo
        .find_by_account(&account_id, Some(50)) // Last 50 transactions
        .map_err(|e| actix_web::error::ErrorInternalServerError(e))?;

    let response: Vec<serde_json::Value> = transactions
        .into_iter()
        .map(|t| {
            serde_json::json!({
                "transaction_id": t.transaction_id,
                "transaction_type": t.transaction_type.as_str(),
                "category": t.category.as_str(),
                "amount": t.amount,
                "running_balance": t.running_balance,
                "description": t.description,
                "reference": t.reference,
                "transaction_date": t.transaction_date.to_rfc3339(),
            })
        })
        .collect();

    Ok(HttpResponse::Ok().json(ApiResponse::success(response)))
}
