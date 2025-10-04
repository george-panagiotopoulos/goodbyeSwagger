import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { accountService } from '../services/accountService';
import type { Account } from '../types/account';
import type { Transaction } from '../types/transaction';

export default function AccountDetail() {
  const { id } = useParams<{ id: string }>();
  const [account, setAccount] = useState<Account | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadAccountData(id);
    }
  }, [id]);

  const loadAccountData = async (accountId: string) => {
    try {
      setLoading(true);
      const [accountData, transactionsData] = await Promise.all([
        accountService.getById(accountId),
        accountService.getTransactions(accountId),
      ]);
      setAccount(accountData);
      setTransactions(transactionsData);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load account');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading account...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!account) return <div>Account not found</div>;

  return (
    <div className="account-detail-page">
      <h1>Account Details</h1>

      <div className="account-info">
        <div className="info-group">
          <label>Account Number:</label>
          <span>{account.account_number}</span>
        </div>
        <div className="info-group">
          <label>Customer ID:</label>
          <span>{account.customer_id}</span>
        </div>
        <div className="info-group">
          <label>Currency:</label>
          <span>{account.currency}</span>
        </div>
        <div className="info-group">
          <label>Balance:</label>
          <span className="balance">${parseFloat(account.balance).toFixed(2)}</span>
        </div>
        <div className="info-group">
          <label>Status:</label>
          <span className={`status ${account.status.toLowerCase()}`}>{account.status}</span>
        </div>
        <div className="info-group">
          <label>Opening Date:</label>
          <span>{new Date(account.opening_date).toLocaleDateString()}</span>
        </div>
      </div>

      <h2>Transaction History</h2>
      <table className="transactions-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Type</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn) => (
            <tr key={txn.transaction_id}>
              <td>{new Date(txn.transaction_date).toLocaleString()}</td>
              <td><span className={`txn-type ${txn.transaction_type.toLowerCase()}`}>{txn.transaction_type}</span></td>
              <td>{txn.description}</td>
              <td className={txn.transaction_type === 'Credit' ? 'credit' : 'debit'}>
                {txn.transaction_type === 'Credit' ? '+' : '-'}${parseFloat(txn.amount).toFixed(2)}
              </td>
              <td className="balance">${parseFloat(txn.running_balance).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
