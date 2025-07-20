-- Tax Engine Database Schema
-- Create database
CREATE DATABASE IF NOT EXISTS tax_engine;
USE tax_engine;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- Documents table
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    document_type ENUM('w2', '1099', 'receipt', 'bank_statement', 'other') DEFAULT 'other',
    status ENUM('uploaded', 'processing', 'processed', 'error') DEFAULT 'uploaded',
    extracted_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_document_type (document_type)
);

-- Tax forms table
CREATE TABLE tax_forms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    form_type VARCHAR(50) NOT NULL,
    tax_year INT NOT NULL,
    status ENUM('draft', 'in_progress', 'completed', 'filed') DEFAULT 'draft',
    form_data JSON,
    calculated_tax DECIMAL(10, 2),
    refund_amount DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_tax_year (tax_year),
    INDEX idx_status (status),
    UNIQUE KEY unique_user_form_year (user_id, form_type, tax_year)
);

-- Payments table
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    form_id INT,
    payment_type ENUM('tax_payment', 'refund', 'penalty', 'interest') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    payment_method VARCHAR(50),
    reference_number VARCHAR(100),
    transaction_id VARCHAR(100),
    due_date DATE,
    processed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (form_id) REFERENCES tax_forms(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_payment_type (payment_type),
    INDEX idx_reference_number (reference_number)
);

-- Audit logs table
CREATE TABLE audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_entity_type (entity_type),
    INDEX idx_created_at (created_at)
);

-- Tax calculations table
CREATE TABLE tax_calculations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    form_id INT NOT NULL,
    calculation_type VARCHAR(50) NOT NULL,
    input_data JSON NOT NULL,
    result_data JSON NOT NULL,
    calculation_version VARCHAR(20) DEFAULT '1.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (form_id) REFERENCES tax_forms(id) ON DELETE CASCADE,
    INDEX idx_form_id (form_id),
    INDEX idx_calculation_type (calculation_type)
);

-- Notifications table
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('info', 'warning', 'error', 'success') DEFAULT 'info',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
);

-- Insert sample data for testing
INSERT INTO users (email, hashed_password, full_name, phone, address) VALUES
('admin@taxengine.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6QJZzQAUxO', 'Admin User', '555-0001', '123 Admin St, Admin City, AC 12345'),
('john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6QJZzQAUxO', 'John Doe', '555-0002', '456 Main St, Anytown, AT 67890');

-- Insert sample tax forms
INSERT INTO tax_forms (user_id, form_type, tax_year, status, form_data, calculated_tax) VALUES
(2, '1040', 2023, 'in_progress', '{"income": 75000, "deductions": 12950}', 8500.00),
(2, '1040', 2022, 'completed', '{"income": 70000, "deductions": 12550}', 7200.00);

-- Insert sample notifications
INSERT INTO notifications (user_id, title, message, type) VALUES
(2, 'Welcome to Tax Engine', 'Your account has been created successfully. Start by uploading your tax documents.', 'success'),
(2, 'Document Processing Complete', 'Your W-2 form has been processed and data extracted successfully.', 'info');