import { useState } from 'react';
import type { Transaction } from '../types/transaction';
import { accountService } from '../services/accountService';

interface TransactionFormProps {
  accountId: string;
  accountCurrency: string;
  onSuccess?: (transaction: Transaction) => void;
  onCancel?: () => void;
}

export default function TransactionForm({ accountId, accountCurrency, onSuccess, onCancel }: TransactionFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [formData, setFormData] = useState({
    type: 'CREDIT',
    amount: '',
    description: '',
    reference: '',
    channel: 'ONLINE',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const amount = parseFloat(formData.amount);

      if (amount <= 0) {
        throw new Error('Amount must be greater than 0');
      }

      if (!/^\d+(\.\d{1,2})?$/.test(formData.amount)) {
        throw new Error('Amount must have at most 2 decimal places');
      }

      const transactionData = {
        amount: amount.toString(),
        description: formData.description,
        reference: formData.reference || `TXN-${Date.now()}`,
        channel: formData.channel,
      };

      let newTransaction: Transaction;

      if (formData.type === 'CREDIT') {
        newTransaction = await accountService.credit(accountId, transactionData);
      } else {
        newTransaction = await accountService.debit(accountId, transactionData);
      }

      // Reset form
      setFormData({
        type: 'CREDIT',
        amount: '',
        description: '',
        reference: '',
        channel: 'ONLINE',
      });

      if (onSuccess) {
        onSuccess(newTransaction);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to process transaction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="transaction-form">
      <h3>New Transaction</h3>

      {error && <div className="error-message">{error}</div>}

      <div className="form-group">
        <label htmlFor="type">Transaction Type *</label>
        <select
          id="type"
          value={formData.type}
          onChange={(e) => setFormData({ ...formData, type: e.target.value })}
          required
        >
          <option value="CREDIT">Credit (Deposit)</option>
          <option value="DEBIT">Debit (Withdrawal)</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="amount">Amount ({accountCurrency}) *</label>
        <input
          id="amount"
          type="number"
          step="0.01"
          min="0.01"
          value={formData.amount}
          onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
          required
          placeholder="e.g., 100.00"
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <input
          id="description"
          type="text"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="e.g., Salary deposit, ATM withdrawal"
        />
      </div>

      <div className="form-group">
        <label htmlFor="reference">Reference</label>
        <input
          id="reference"
          type="text"
          value={formData.reference}
          onChange={(e) => setFormData({ ...formData, reference: e.target.value })}
          placeholder="Auto-generated if blank"
        />
      </div>

      <div className="form-group">
        <label htmlFor="channel">Channel *</label>
        <select
          id="channel"
          value={formData.channel}
          onChange={(e) => setFormData({ ...formData, channel: e.target.value })}
          required
        >
          <option value="BRANCH">Branch</option>
          <option value="ATM">ATM</option>
          <option value="ONLINE">Online</option>
          <option value="MOBILE">Mobile</option>
          <option value="TRANSFER">Transfer</option>
        </select>
      </div>

      <div className="form-actions">
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Processing...' : `${formData.type === 'CREDIT' ? 'Deposit' : 'Withdraw'} Funds`}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="btn-secondary">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
