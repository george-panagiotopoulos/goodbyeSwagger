import { useState, useEffect } from 'react';
import React from 'react';
import { customerService } from '../services/customerService';
import type { Customer } from '../types/customer';
import type { Account } from '../types/account';
import AccountForm from '../components/AccountForm';

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showFormForCustomer, setShowFormForCustomer] = useState<string | null>(null);

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      const data = await customerService.getAll();
      setCustomers(data);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load customers');
    } finally {
      setLoading(false);
    }
  };

  const handleAccountCreated = (_newAccount: Account) => {
    setShowFormForCustomer(null);
    // Optionally refresh customers or display success message
  };

  if (loading) return <div>Loading customers...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="customers-page">
      <h1>Customers</h1>
      <table className="customers-table">
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <React.Fragment key={customer.customer_id || customer.external_customer_id}>
              <tr>
                <td>{customer.external_customer_id}</td>
                <td>{customer.customer_name}</td>
                <td>{customer.customer_type}</td>
                <td>{customer.email}</td>
                <td>{customer.phone}</td>
                <td><span className={`status ${customer.status.toLowerCase()}`}>{customer.status}</span></td>
                <td>
                  <button
                    onClick={() => window.location.href = `/customers/${customer.customer_id}`}
                    className="btn-secondary"
                    style={{ marginRight: '0.5rem' }}
                  >
                    View Details
                  </button>
                  <button
                    onClick={() => setShowFormForCustomer(showFormForCustomer === customer.customer_id ? null : customer.customer_id)}
                    className="btn-primary"
                  >
                    {showFormForCustomer === customer.customer_id ? 'Cancel' : 'Open Account'}
                  </button>
                </td>
              </tr>
              {showFormForCustomer === customer.customer_id && (
                <tr>
                  <td colSpan={7}>
                    <div className="form-container">
                      <AccountForm
                        customerId={customer.customer_id}
                        onSuccess={handleAccountCreated}
                        onCancel={() => setShowFormForCustomer(null)}
                      />
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}
