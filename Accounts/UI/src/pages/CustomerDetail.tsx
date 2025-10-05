import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { customerService } from '../services/customerService';
import { accountService } from '../services/accountService';
import type { Customer } from '../types/customer';
import type { Account } from '../types/account';
import AccountForm from '../components/AccountForm';

export default function CustomerDetail() {
  const { id } = useParams<{ id: string }>();
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAccountForm, setShowAccountForm] = useState(false);

  useEffect(() => {
    loadCustomerData();
  }, [id]);

  const loadCustomerData = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const [customerData, allAccounts] = await Promise.all([
        customerService.getById(id),
        accountService.getAll()
      ]);

      setCustomer(customerData);
      // Filter accounts for this customer
      setAccounts(allAccounts.filter(acc => acc.customer_id === id));
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load customer data');
    } finally {
      setLoading(false);
    }
  };

  const handleAccountCreated = async () => {
    setShowAccountForm(false);
    // Reload customer data to show new account
    await loadCustomerData();
  };

  if (loading) return <div>Loading customer details...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!customer) return <div>Customer not found</div>;

  return (
    <div className="customer-detail-page">
      <div className="page-header">
        <Link to="/customers" className="back-link">← Back to Customers</Link>
        <h1>Customer Details</h1>
      </div>

      <div className="customer-info-card">
        <h2>{customer.customer_name}</h2>
        <div className="info-grid">
          <div className="info-item">
            <label>Customer ID:</label>
            <span>{customer.external_customer_id}</span>
          </div>
          <div className="info-item">
            <label>Type:</label>
            <span>{customer.customer_type}</span>
          </div>
          <div className="info-item">
            <label>Email:</label>
            <span>{customer.email}</span>
          </div>
          <div className="info-item">
            <label>Phone:</label>
            <span>{customer.phone}</span>
          </div>
          <div className="info-item">
            <label>Status:</label>
            <span className={`status ${customer.status.toLowerCase()}`}>
              {customer.status}
            </span>
          </div>
        </div>
      </div>

      <div className="accounts-section">
        <div className="section-header">
          <h2>Accounts</h2>
          <button
            onClick={() => setShowAccountForm(!showAccountForm)}
            className="btn-primary"
          >
            {showAccountForm ? 'Cancel' : 'Open New Account'}
          </button>
        </div>

        {showAccountForm && (
          <div className="form-container" style={{ marginBottom: '2rem' }}>
            <AccountForm
              customerId={customer.customer_id}
              onSuccess={handleAccountCreated}
              onCancel={() => setShowAccountForm(false)}
            />
          </div>
        )}

        {accounts.length === 0 ? (
          <p className="info-message">No accounts found for this customer.</p>
        ) : (
          <table className="accounts-table">
            <thead>
              <tr>
                <th>Account Number</th>
                <th>Product</th>
                <th>Currency</th>
                <th>Balance</th>
                <th>Status</th>
                <th>Opening Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map((account) => (
                <tr key={account.account_id}>
                  <td>{account.account_number}</td>
                  <td>{account.product_id}</td>
                  <td>{account.currency}</td>
                  <td className="amount">${parseFloat(account.balance).toFixed(2)}</td>
                  <td>
                    <span className={`status ${account.status.toLowerCase()}`}>
                      {account.status}
                    </span>
                  </td>
                  <td>{account.opening_date}</td>
                  <td>
                    <Link to={`/accounts/${account.account_id}`} className="btn-link">
                      View Details
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
