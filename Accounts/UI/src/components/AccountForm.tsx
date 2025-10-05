import { useState, useEffect } from 'react';
import type { Account } from '../types/account';
import type { Product } from '../types/product';
import { accountService } from '../services/accountService';
import { productService } from '../services/productService';

interface AccountFormProps {
  customerId: string;
  onSuccess?: (account: Account) => void;
  onCancel?: () => void;
}

export default function AccountForm({ customerId, onSuccess, onCancel }: AccountFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [products, setProducts] = useState<Product[]>([]);
  const [formData, setFormData] = useState({
    product_id: '',
    opening_balance: '',
  });

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const activeProducts = await productService.getActive();
        setProducts(activeProducts);
        if (activeProducts.length > 0) {
          setFormData((prev) => ({ ...prev, product_id: activeProducts[0].product_id }));
        }
      } catch (err) {
        console.error('Failed to load products:', err);
        setError('Failed to load products');
      }
    };

    fetchProducts();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Creating account with data:', {
        customer_id: customerId,
        product_id: formData.product_id,
        opening_balance: formData.opening_balance || '0',
      });

      const accountData = {
        customer_id: customerId,
        product_id: formData.product_id,
        opening_balance: formData.opening_balance || '0',
      };

      const newAccount = await accountService.create(accountData);
      console.log('Account created successfully:', newAccount);

      alert(`Account ${newAccount.account_number} created successfully!`);

      // Reset form
      setFormData({
        product_id: products.length > 0 ? products[0].product_id : '',
        opening_balance: '',
      });

      if (onSuccess) {
        onSuccess(newAccount);
      }
    } catch (err: unknown) {
      console.error('Account creation error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to create account';
      setError(errorMessage);
      alert(`Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  if (products.length === 0) {
    return <div className="info-message">No active products available. Please create a product first.</div>;
  }

  const selectedProduct = products.find((p) => p.product_id === formData.product_id);

  return (
    <form onSubmit={handleSubmit} className="account-form">
      <h3>Open New Account</h3>

      {error && <div className="error-message">{error}</div>}

      <div className="form-group">
        <label htmlFor="product_id">Product *</label>
        <select
          id="product_id"
          value={formData.product_id}
          onChange={(e) => setFormData({ ...formData, product_id: e.target.value })}
          required
        >
          {products.map((product) => (
            <option key={product.product_id} value={product.product_id}>
              {product.product_name} - {product.interest_rate}% APR
            </option>
          ))}
        </select>
        {selectedProduct && (
          <div className="product-details">
            <small>
              Currency: {selectedProduct.currency} | Min Balance: {selectedProduct.minimum_balance_for_interest} | Monthly Fee: {selectedProduct.monthly_maintenance_fee}
            </small>
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="opening_balance">Opening Balance {selectedProduct ? `(${selectedProduct.currency})` : ''}</label>
        <input
          id="opening_balance"
          type="text"
          value={formData.opening_balance}
          onChange={(e) => setFormData({ ...formData, opening_balance: e.target.value })}
          placeholder="e.g., 1000.00"
        />
      </div>

      <div className="form-actions">
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Opening...' : 'Open Account'}
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
