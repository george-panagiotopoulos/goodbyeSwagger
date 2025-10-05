use actix_web::{web, HttpResponse};
use serde::{Deserialize, Serialize};
use std::process::Command;
use crate::models::common::ErrorResponse;

#[derive(Debug, Deserialize)]
pub struct RunAccrualsRequest {
    pub month: Option<String>,  // Optional: YYYY-MM format
    pub dry_run: Option<bool>,
}

#[derive(Debug, Serialize)]
pub struct AccrualResult {
    pub account_number: String,
    pub months: i32,
    pub total_interest: f64,
}

#[derive(Debug, Serialize)]
pub struct RunAccrualsResponse {
    pub success: bool,
    pub accounts_processed: i32,
    pub months_processed: i32,
    pub total_interest: f64,
    pub results: Vec<AccrualResult>,
    pub output: String,
}

#[derive(Debug, Serialize)]
pub struct AccrualHistoryItem {
    pub monthly_accrual_id: String,
    pub account_id: String,
    pub account_number: String,
    pub accrual_month: String,
    pub posting_date: String,
    pub month_end_balance: f64,
    pub annual_interest_rate: f64,
    pub monthly_interest: f64,
    pub processing_date: String,
    pub processing_status: String,
}

pub async fn run_monthly_accruals(
    request: web::Json<RunAccrualsRequest>,
) -> HttpResponse {
    log::info!("Running monthly accruals batch process");

    // Build command
    let script_path = "../Database/scripts/batch_monthly_accruals.py";
    let mut cmd = Command::new("python3");
    cmd.arg(script_path);

    if let Some(ref month) = request.month {
        cmd.arg("--month").arg(month);
    }

    if request.dry_run.unwrap_or(false) {
        cmd.arg("--dry-run");
    }

    // Execute the Python script
    match cmd.output() {
        Ok(output) => {
            let stdout = String::from_utf8_lossy(&output.stdout).to_string();
            let stderr = String::from_utf8_lossy(&output.stderr).to_string();

            if output.status.success() {
                log::info!("Monthly accruals completed successfully");

                // Parse output to extract summary (simple approach)
                let mut accounts_processed = 0;
                let mut months_processed = 0;
                let mut total_interest = 0.0;

                for line in stdout.lines() {
                    if line.contains("Accounts Processed:") {
                        if let Some(num) = line.split(':').nth(1) {
                            accounts_processed = num.trim().parse().unwrap_or(0);
                        }
                    } else if line.contains("Months Processed:") {
                        if let Some(num) = line.split(':').nth(1) {
                            months_processed = num.trim().parse().unwrap_or(0);
                        }
                    } else if line.contains("Total Interest Posted:") {
                        if let Some(amount) = line.split('$').nth(1) {
                            total_interest = amount.trim().replace(',', "").parse().unwrap_or(0.0);
                        }
                    }
                }

                HttpResponse::Ok().json(RunAccrualsResponse {
                    success: true,
                    accounts_processed,
                    months_processed,
                    total_interest,
                    results: Vec::new(), // Could parse detailed results if needed
                    output: stdout,
                })
            } else {
                log::error!("Monthly accruals failed: {}", stderr);
                HttpResponse::InternalServerError().json(ErrorResponse::new(
                    "BATCH_PROCESSING_ERROR",
                    &format!("Batch processing failed: {}", stderr),
                ))
            }
        }
        Err(e) => {
            log::error!("Failed to execute batch script: {}", e);
            HttpResponse::InternalServerError().json(ErrorResponse::new(
                "SCRIPT_EXECUTION_ERROR",
                &format!("Failed to execute batch script: {}", e),
            ))
        }
    }
}

pub async fn get_accrual_history(
    state: web::Data<crate::app_state::AppState>,
    query: web::Query<std::collections::HashMap<String, String>>,
) -> HttpResponse {
    let conn = match state.get_connection() {
        Ok(c) => c,
        Err(e) => {
            log::error!("Database connection error: {}", e);
            return HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                "Database connection failed"
            ));
        }
    };

    let account_id = query.get("account_id");
    let limit: i32 = query.get("limit").and_then(|l| l.parse().ok()).unwrap_or(50);

    let sql = if let Some(acc_id) = account_id {
        format!(
            "SELECT ma.monthly_accrual_id, ma.account_id, a.account_number, ma.accrual_month,
                    ma.posting_date, ma.month_end_balance, ma.annual_interest_rate,
                    ma.monthly_interest, ma.processing_date, ma.processing_status
             FROM monthly_interest_accruals ma
             JOIN accounts a ON ma.account_id = a.account_id
             WHERE ma.account_id = '{}'
             ORDER BY ma.accrual_month DESC
             LIMIT {}",
            acc_id, limit
        )
    } else {
        format!(
            "SELECT ma.monthly_accrual_id, ma.account_id, a.account_number, ma.accrual_month,
                    ma.posting_date, ma.month_end_balance, ma.annual_interest_rate,
                    ma.monthly_interest, ma.processing_date, ma.processing_status
             FROM monthly_interest_accruals ma
             JOIN accounts a ON ma.account_id = a.account_id
             ORDER BY ma.accrual_month DESC, a.account_number
             LIMIT {}",
            limit
        )
    };

    let mut stmt = match conn.prepare(&sql) {
        Ok(s) => s,
        Err(e) => {
            log::error!("SQL preparation error: {}", e);
            return HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                "Database query error"
            ));
        }
    };

    let history_iter = stmt.query_map([], |row| {
        Ok(AccrualHistoryItem {
            monthly_accrual_id: row.get(0)?,
            account_id: row.get(1)?,
            account_number: row.get(2)?,
            accrual_month: row.get(3)?,
            posting_date: row.get(4)?,
            month_end_balance: row.get(5)?,
            annual_interest_rate: row.get(6)?,
            monthly_interest: row.get(7)?,
            processing_date: row.get(8)?,
            processing_status: row.get(9)?,
        })
    });

    match history_iter {
        Ok(items) => {
            let history: Vec<AccrualHistoryItem> = items.filter_map(Result::ok).collect();
            HttpResponse::Ok().json(history)
        }
        Err(e) => {
            log::error!("Query execution error: {}", e);
            HttpResponse::InternalServerError().json(ErrorResponse::internal_error(
                "Failed to fetch accrual history"
            ))
        }
    }
}
