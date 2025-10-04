-- Seed Data: Users
-- Description: Initial users for testing
-- Note: Passwords are hashed with bcrypt, plain text shown in comments

-- Admin user (password: admin123)
INSERT INTO users (user_id, username, password_hash, full_name, email, role, status)
VALUES (
    'USR-ADMIN-001',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYhKCXhKzze',  -- admin123
    'System Administrator',
    'admin@accountsystem.com',
    'admin',
    'active'
);

-- Account officer (password: officer123)
INSERT INTO users (user_id, username, password_hash, full_name, email, role, status)
VALUES (
    'USR-OFFICER-001',
    'officer',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXe.vZVadjHTgPZ1FHzhz5pS3nNP3Cn6LG',  -- officer123
    'John Officer',
    'officer@accountsystem.com',
    'officer',
    'active'
);

-- Viewer user (password: viewer123)
INSERT INTO users (user_id, username, password_hash, full_name, email, role, status)
VALUES (
    'USR-VIEWER-001',
    'viewer',
    '$2b$12$9H0jhz5hv2L4vSqY1qUDOe.aJz5wK5pJwK5sXh4qYh8hL4z5aZ4nO',  -- viewer123
    'Jane Viewer',
    'viewer@accountsystem.com',
    'viewer',
    'active'
);

-- ============================================================================
-- NOTES
-- ============================================================================
-- Default credentials for testing:
--   Admin:   admin / admin123
--   Officer: officer / officer123
--   Viewer:  viewer / viewer123
--
-- In production, these should be changed immediately
-- Password hashes generated with bcrypt (cost=12)
