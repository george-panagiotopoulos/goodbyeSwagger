import { useState } from 'react';
import type { Product } from '../types/product';
import { productService } from '../services/productService';

interface ProductFormProps {
  onSuccess?: (product: Product) => void;
  onCancel?: () => void;
}

export default function ProductForm({ onSuccess, onCancel }: ProductFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [formData, setFormData] = useState({
    product_name: '',
    product_code: '',
    description: '',
    currency: 'USD',
    interest_rate: '',
    minimum_balance_for_interest: '',
    monthly_maintenance_fee: '',
    transaction_fee: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const productData = {
        product_name: formData.product_name,
        product_code: formData.product_code || `PRD-${Date.now()}`,
        description: formData.description,
        currency: formData.currency,
        interest_rate: formData.interest_rate || '0',
        minimum_balance_for_interest: formData.minimum_balance_for_interest || '0',
        monthly_maintenance_fee: formData.monthly_maintenance_fee || '0',
        transaction_fee: formData.transaction_fee || '0',
      };

      const newProduct = await productService.create(productData);

      // Reset form
      setFormData({
        product_name: '',
        product_code: '',
        description: '',
        currency: 'USD',
        interest_rate: '',
        minimum_balance_for_interest: '',
        monthly_maintenance_fee: '',
        transaction_fee: '',
      });

      if (onSuccess) {
        onSuccess(newProduct);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to create product');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="product-form">
      <h3>Create New Product</h3>

      {error && <div className="error-message">{error}</div>}

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="product_name">Product Name *</label>
          <input
            id="product_name"
            type="text"
            value={formData.product_name}
            onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
            required
            placeholder="e.g., Premium Checking"
          />
        </div>

        <div className="form-group">
          <label htmlFor="product_code">Product Code</label>
          <input
            id="product_code"
            type="text"
            value={formData.product_code}
            onChange={(e) => setFormData({ ...formData, product_code: e.target.value })}
            placeholder="Auto-generated if blank"
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <input
          id="description"
          type="text"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="Product description"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="currency">Currency *</label>
          <select
            id="currency"
            value={formData.currency}
            onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
            required
          >
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="GBP">GBP</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="interest_rate">Interest Rate (decimal, e.g., 0.025 for 2.5%)</label>
          <input
            id="interest_rate"
            type="text"
            value={formData.interest_rate}
            onChange={(e) => setFormData({ ...formData, interest_rate: e.target.value })}
            placeholder="e.g., 0.025"
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="minimum_balance_for_interest">Minimum Balance for Interest</label>
          <input
            id="minimum_balance_for_interest"
            type="text"
            value={formData.minimum_balance_for_interest}
            onChange={(e) => setFormData({ ...formData, minimum_balance_for_interest: e.target.value })}
            placeholder="e.g., 1000.00"
          />
        </div>

        <div className="form-group">
          <label htmlFor="monthly_maintenance_fee">Monthly Maintenance Fee</label>
          <input
            id="monthly_maintenance_fee"
            type="text"
            value={formData.monthly_maintenance_fee}
            onChange={(e) => setFormData({ ...formData, monthly_maintenance_fee: e.target.value })}
            placeholder="e.g., 5.00"
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="transaction_fee">Transaction Fee</label>
        <input
          id="transaction_fee"
          type="text"
          value={formData.transaction_fee}
          onChange={(e) => setFormData({ ...formData, transaction_fee: e.target.value })}
          placeholder="e.g., 0.50"
        />
      </div>

      <div className="form-actions">
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Creating...' : 'Create Product'}
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
