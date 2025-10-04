import { Link } from 'react-router-dom';

export default function Dashboard() {
  return (
    <div className="dashboard">
      <h1>Account Processing System</h1>
      <p>Welcome to the Account Processing System MVP</p>

      <div className="grid">
        <Link to="/products" className="card">
          <h2>Products</h2>
          <p>Manage account products and configurations</p>
        </Link>

        <Link to="/customers" className="card">
          <h2>Customers</h2>
          <p>Manage customer information</p>
        </Link>

        <Link to="/accounts" className="card">
          <h2>Accounts</h2>
          <p>View and manage customer accounts</p>
        </Link>
      </div>
    </div>
  );
}
