import { useState } from 'react';
import { apiClient } from '../services/api';

interface AccrualResult {
  account_number: string;
  months: number;
  total_interest: number;
}

interface RunAccrualsResponse {
  success: boolean;
  accounts_processed: number;
  months_processed: number;
  total_interest: number;
  results: AccrualResult[];
  output: string;
}

interface AccrualHistoryItem {
  monthly_accrual_id: string;
  account_id: string;
  account_number: string;
  accrual_month: string;
  posting_date: string;
  month_end_balance: number;
  annual_interest_rate: number;
  monthly_interest: number;
  processing_date: string;
  processing_status: string;
}

export default function BatchProcesses() {
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState<RunAccrualsResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [history, setHistory] = useState<AccrualHistoryItem[]>([]);
  const [showOutput, setShowOutput] = useState(false);

  const runMonthlyAccruals = async () => {
    setProcessing(true);
    setError('');
    setResult(null);

    try {
      const response = await apiClient.post<RunAccrualsResponse>('/api/batch/monthly-accruals', {
        dry_run: false
      });

      setResult(response.data);

      // Refresh history
      loadHistory();
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to run batch process');
    } finally {
      setProcessing(false);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await apiClient.get<AccrualHistoryItem[]>('/api/batch/accrual-history?limit=20');
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  return (
    <div className="batch-processes-page">
      <h1>Batch Processes</h1>
      <p style={{ color: '#666', marginBottom: '2rem' }}>
        Execute batch operations and view processing history
      </p>

      {/* Monthly Accruals Card */}
      <div className="card" style={{ marginBottom: '2rem', padding: '2rem' }}>
        <h2 style={{ marginTop: 0, marginBottom: '1rem' }}>📊 Monthly Interest Accruals (30/360)</h2>
        <p style={{ color: '#666', marginBottom: '1.5rem' }}>
          Calculate and post monthly interest for all eligible accounts using the 30/360 day count convention.
          The system will process all missing months from account opening to current month.
        </p>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            onClick={runMonthlyAccruals}
            disabled={processing}
            className="btn-primary"
            style={{ fontSize: '1rem', padding: '0.75rem 2rem' }}
          >
            {processing ? '⏳ Processing...' : '▶️ Run Monthly Accruals'}
          </button>

          {result && (
            <button
              onClick={() => setShowOutput(!showOutput)}
              className="btn-secondary"
            >
              {showOutput ? 'Hide Details' : 'Show Details'}
            </button>
          )}
        </div>

        {error && (
          <div className="error-message" style={{ marginTop: '1rem' }}>
            {error}
          </div>
        )}

        {result && (
          <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#f5f5f5', borderRadius: '8px' }}>
            <h3 style={{ marginTop: 0, color: '#28a745' }}>✓ Processing Complete</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginTop: '1rem' }}>
              <div>
                <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Accounts Processed</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1a1a2e' }}>
                  {result.accounts_processed}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Months Processed</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1a1a2e' }}>
                  {result.months_processed}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Interest</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#28a745' }}>
                  ${result.total_interest.toFixed(2)}
                </div>
              </div>
            </div>

            {showOutput && result.output && (
              <div style={{ marginTop: '1.5rem' }}>
                <h4>Detailed Output:</h4>
                <pre style={{
                  background: '#1a1a2e',
                  color: '#fff',
                  padding: '1rem',
                  borderRadius: '6px',
                  fontSize: '0.85rem',
                  overflow: 'auto',
                  maxHeight: '400px',
                  lineHeight: '1.5'
                }}>
                  {result.output}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Accrual History */}
      <div className="card" style={{ padding: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2 style={{ margin: 0 }}>📜 Accrual History</h2>
          <button onClick={loadHistory} className="btn-secondary">
            🔄 Refresh
          </button>
        </div>

        {history.length === 0 ? (
          <p style={{ color: '#999', textAlign: 'center', padding: '2rem' }}>
            No accrual history yet. Run the monthly accruals batch to see results here.
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th>Account</th>
                  <th>Month</th>
                  <th>Month-End Balance</th>
                  <th>Interest Rate</th>
                  <th>Monthly Interest</th>
                  <th>Posted Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.monthly_accrual_id}>
                    <td style={{ fontFamily: 'monospace' }}>{item.account_number}</td>
                    <td>{item.accrual_month}</td>
                    <td style={{ textAlign: 'right', fontFamily: 'monospace' }}>
                      ${item.month_end_balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      {(item.annual_interest_rate * 100).toFixed(2)}%
                    </td>
                    <td style={{ textAlign: 'right', fontWeight: 'bold', color: '#28a745', fontFamily: 'monospace' }}>
                      ${item.monthly_interest.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td>{new Date(item.posting_date).toLocaleDateString()}</td>
                    <td>
                      <span className="status active">{item.processing_status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Information Box */}
      <div style={{
        marginTop: '2rem',
        padding: '1.5rem',
        background: '#e3f2fd',
        borderRadius: '8px',
        borderLeft: '4px solid #2196f3'
      }}>
        <h3 style={{ marginTop: 0, color: '#1976d2' }}>ℹ️ About 30/360 Convention</h3>
        <p style={{ margin: '0.5rem 0', color: '#333' }}>
          <strong>Formula:</strong> Monthly Interest = (Balance × Annual Rate × 30) / 360
        </p>
        <p style={{ margin: '0.5rem 0', color: '#333' }}>
          <strong>Convention:</strong> Every month = 30 days, Every year = 360 days
        </p>
        <p style={{ margin: '0.5rem 0', color: '#333' }}>
          <strong>Processing:</strong> Interest is calculated and posted on the last day of each month
        </p>
        <p style={{ margin: '0.5rem 0', color: '#333' }}>
          <strong>Catch-up:</strong> System automatically processes all missing months from account opening
        </p>
      </div>
    </div>
  );
}
