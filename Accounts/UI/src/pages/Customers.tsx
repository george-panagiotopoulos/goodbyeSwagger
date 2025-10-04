import { useState, useEffect } from 'react';
import { customerService } from '../services/customerService';
import type { Customer } from '../types/customer';

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.customer_id}>
              <td>{customer.external_customer_id}</td>
              <td>{customer.customer_name}</td>
              <td>{customer.customer_type}</td>
              <td>{customer.email}</td>
              <td>{customer.phone}</td>
              <td><span className={`status ${customer.status.toLowerCase()}`}>{customer.status}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
