import { useState, useEffect } from 'react';
import { productService } from '../services/productService';
import type { Product } from '../types/product';
import ProductForm from '../components/ProductForm';

export default function Products() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const data = await productService.getAll();
      setProducts(data);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const handleProductCreated = (newProduct: Product) => {
    setProducts([...products, newProduct]);
    setShowForm(false);
  };

  if (loading) return <div>Loading products...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="products-page">
      <div className="page-header">
        <h1>Products</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary">
          {showForm ? 'Cancel' : 'Create New Product'}
        </button>
      </div>

      {showForm && (
        <div className="form-container">
          <ProductForm
            onSuccess={handleProductCreated}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}

      <div className="products-grid">
        {products.map((product) => (
          <div key={product.product_id} className="product-card">
            <h3>{product.product_name}</h3>
            <p className="product-code">{product.product_code}</p>
            <p>{product.description}</p>
            <div className="product-details">
              <p><strong>Currency:</strong> {product.currency}</p>
              <p><strong>Interest Rate:</strong> {product.interest_rate}%</p>
              <p><strong>Monthly Fee:</strong> ${product.monthly_maintenance_fee}</p>
              <p><strong>Status:</strong> <span className={`status ${product.status.toLowerCase()}`}>{product.status}</span></p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
