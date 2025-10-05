import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

interface User {
  username: string;
  full_name: string;
  role: string;
}

export default function Layout() {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      setUser(JSON.parse(userStr));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="app-layout">
      <nav className="navbar">
        <div className="nav-brand">
          <Link to="/">🏦 Account Processing System</Link>
        </div>
        <ul className="nav-links">
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/products">Products</Link></li>
          <li><Link to="/customers">Customers</Link></li>
          <li><Link to="/accounts">Accounts</Link></li>
          <li><Link to="/batch">Batch Processes</Link></li>
        </ul>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {user && (
            <div style={{ color: 'white', fontSize: '0.9rem' }}>
              <span style={{ opacity: 0.8 }}>👤 </span>
              <span style={{ fontWeight: '600' }}>{user.full_name}</span>
              <span style={{ opacity: 0.6, marginLeft: '0.5rem', fontSize: '0.8rem' }}>
                ({user.role})
              </span>
            </div>
          )}
          <button
            onClick={handleLogout}
            style={{
              padding: '0.5rem 1rem',
              background: 'rgba(255,255,255,0.2)',
              color: 'white',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.9rem',
              transition: 'background 0.2s',
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.3)'}
            onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.2)'}
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="main-content">
        <Outlet />
      </main>

      <footer className="footer">
        <p>&copy; 2025 Account Processing System - MVP | Powered by Rust + React</p>
      </footer>
    </div>
  );
}
