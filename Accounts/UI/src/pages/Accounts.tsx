import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { accountService } from '../services/accountService';
import type { Account } from '../types/account';

export default function Accounts() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAccounts();
  }, []);

  const loadAccounts = async () => {
    try {
      setLoading(true);
      const data = await accountService.getAll();
      setAccounts(data);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load accounts');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading accounts...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="accounts-page">
      <h1>Accounts</h1>
      <table className="accounts-table">
        <thead>
          <tr>
            <th>Account Number</th>
            <th>Customer ID</th>
            <th>Currency</th>
            <th>Balance</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((account) => (
            <tr key={account.account_id}>
              <td>{account.account_number}</td>
              <td>{account.customer_id}</td>
              <td>{account.currency}</td>
              <td className="balance">${parseFloat(account.balance).toFixed(2)}</td>
              <td><span className={`status ${account.status.toLowerCase()}`}>{account.status}</span></td>
              <td>
                <Link to={`/accounts/${account.account_id}`} className="btn btn-sm">View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
