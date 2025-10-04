import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="app-layout">
      <nav className="navbar">
        <div className="nav-brand">
          <Link to="/">Account Processing System</Link>
        </div>
        <ul className="nav-links">
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/products">Products</Link></li>
          <li><Link to="/customers">Customers</Link></li>
          <li><Link to="/accounts">Accounts</Link></li>
        </ul>
      </nav>

      <main className="main-content">
        <Outlet />
      </main>

      <footer className="footer">
        <p>&copy; 2025 Account Processing System - MVP</p>
      </footer>
    </div>
  );
}
