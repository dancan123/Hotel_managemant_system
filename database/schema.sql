-- Hotel Management System Database Schema

-- Users/Employees Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Employee', 'Manager', 'Admin')),
    department TEXT,
    phone TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rooms Table
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT UNIQUE NOT NULL,
    room_type TEXT NOT NULL CHECK(room_type IN ('Single', 'Double', 'Suite', 'Deluxe')),
    capacity INTEGER NOT NULL,
    price_per_night REAL NOT NULL,
    status TEXT DEFAULT 'Available' CHECK(status IN ('Available', 'Occupied', 'Maintenance')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Guest Check-ins Table
CREATE TABLE IF NOT EXISTS check_ins (
    check_in_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    guest_name TEXT NOT NULL,
    guest_email TEXT,
    guest_phone TEXT,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_guests INTEGER DEFAULT 1,
    check_in_employee_id INTEGER NOT NULL,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Completed', 'Cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    FOREIGN KEY (check_in_employee_id) REFERENCES users(user_id)
);

-- Sales Table (Daily Sales per Employee)
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Room', 'Food', 'Beverage', 'Services', 'Other')),
    description TEXT,
    amount REAL NOT NULL,
    payment_method TEXT CHECK(payment_method IN ('Cash', 'Card', 'Mobile', 'Check', 'Online')),
    transaction_id TEXT UNIQUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES users(user_id)
);

-- Daily Sales Summary Table
CREATE TABLE IF NOT EXISTS daily_sales_summary (
    summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    sale_date DATE NOT NULL,
    total_sales REAL DEFAULT 0,
    room_sales REAL DEFAULT 0,
    food_sales REAL DEFAULT 0,
    beverage_sales REAL DEFAULT 0,
    service_sales REAL DEFAULT 0,
    transaction_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES users(user_id),
    UNIQUE(employee_id, sale_date)
);

-- Monthly Sales Report Table
CREATE TABLE IF NOT EXISTS monthly_sales_report (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK(month >= 1 AND month <= 12),
    total_sales REAL DEFAULT 0,
    room_sales REAL DEFAULT 0,
    food_sales REAL DEFAULT 0,
    beverage_sales REAL DEFAULT 0,
    service_sales REAL DEFAULT 0,
    transaction_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES users(user_id),
    UNIQUE(employee_id, year, month)
);

-- Occupancy Report Table
CREATE TABLE IF NOT EXISTS occupancy_report (
    occupancy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date DATE NOT NULL,
    total_rooms INTEGER NOT NULL,
    occupied_rooms INTEGER DEFAULT 0,
    available_rooms INTEGER DEFAULT 0,
    maintenance_rooms INTEGER DEFAULT 0,
    occupancy_rate REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(report_date)
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create Indexes for Better Performance
CREATE INDEX IF NOT EXISTS idx_sales_employee_date ON sales(employee_id, sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_check_ins_room ON check_ins(room_id);
CREATE INDEX IF NOT EXISTS idx_check_ins_date ON check_ins(check_in_date, check_out_date);
CREATE INDEX IF NOT EXISTS idx_daily_summary_date ON daily_sales_summary(sale_date);
CREATE INDEX IF NOT EXISTS idx_monthly_report_date ON monthly_sales_report(year, month);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
