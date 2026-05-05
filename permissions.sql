CREATE TABLE IF NOT EXISTS permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    permission_name VARCHAR(100) NOT NULL UNIQUE
);


INSERT INTO permissions (permission_name) VALUES
('can_access_main'),
('can_manage_admins'),
('can_manage_permissions');