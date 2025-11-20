# Database Schema Documentation

## Overview

The Hotel Management System uses SQLite3 as its database. The schema is designed to be normalized, scalable, and efficient for real-time operations and analytics.

## Database File Location

```
backend/database/hotel_management.db
```

## Tables

### 1. Users Table

Stores information about all system users (employees, managers, admins).

```sql
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- Hashed password using Werkzeug
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Employee', 'Manager', 'Admin')),
    department TEXT,
    phone TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `user_id`: Unique identifier (auto-increment)
- `username`: Unique login username
- `password`: Bcrypt hashed password
- `email`: Unique email address
- `full_name`: User's full name
- `role`: User role (Employee, Manager, Admin)
- `department`: Department assignment (e.g., Dining, Front Desk, Management)
- `phone`: Contact phone number
- `is_active`: Soft delete flag (0 = inactive/deleted)
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

**Indexes:**
- PRIMARY KEY on `user_id`
- UNIQUE on `username`, `email`

**Constraints:**
- Role must be one of: Employee, Manager, Admin
- is_active is boolean

**Sample Data:**
```
user_id=1, username=admin, role=Admin, full_name=Administrator
user_id=2, username=manager1, role=Manager, full_name=John Manager
user_id=3, username=waiter1, role=Employee, full_name=James Smith
```

---

### 2. Rooms Table

Stores hotel room information and status.

```sql
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
```

**Columns:**
- `room_id`: Unique identifier (auto-increment)
- `room_number`: Unique room number (e.g., "101", "202")
- `room_type`: Type of room (Single, Double, Suite, Deluxe)
- `capacity`: Maximum number of guests
- `price_per_night`: Nightly rate in USD
- `status`: Current room status (Available, Occupied, Maintenance)
- `created_at`: Room creation timestamp
- `updated_at`: Last update timestamp

**Indexes:**
- PRIMARY KEY on `room_id`
- UNIQUE on `room_number`

**Sample Data:**
```
room_id=1, room_number=101, room_type=Single, capacity=1, price_per_night=50.00, status=Available
room_id=2, room_number=102, room_type=Double, capacity=2, price_per_night=75.00, status=Occupied
```

---

### 3. Check-ins Table

Records guest check-in and check-out information.

```sql
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
```

**Columns:**
- `check_in_id`: Unique identifier (auto-increment)
- `room_id`: Reference to rooms table
- `guest_name`: Name of the guest
- `guest_email`: Guest's email address
- `guest_phone`: Guest's phone number
- `check_in_date`: Check-in date
- `check_out_date`: Check-out date
- `number_of_guests`: Count of guests
- `check_in_employee_id`: Employee who processed check-in
- `status`: Current status (Active, Completed, Cancelled)
- `notes`: Additional notes about the stay
- `created_at`: Check-in creation timestamp
- `updated_at`: Last update timestamp

**Foreign Keys:**
- `room_id` → rooms.room_id
- `check_in_employee_id` → users.user_id

**Indexes:**
- PRIMARY KEY on `check_in_id`
- Composite index on (room_id, status)

---

### 4. Sales Table

Records all sales transactions by employees.

```sql
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
```

**Columns:**
- `sale_id`: Unique identifier (auto-increment)
- `employee_id`: Employee who made the sale
- `sale_date`: Date of the sale
- `category`: Sales category (Room, Food, Beverage, Services, Other)
- `description`: Description of the sale
- `amount`: Sale amount in USD
- `payment_method`: Payment method used
- `transaction_id`: External transaction ID (if applicable)
- `notes`: Additional notes
- `created_at`: Transaction timestamp

**Foreign Keys:**
- `employee_id` → users.user_id

**Indexes:**
- PRIMARY KEY on `sale_id`
- Composite index on (employee_id, sale_date)
- Index on sale_date
- UNIQUE on transaction_id

**Sample Data:**
```
sale_id=1, employee_id=3, sale_date=2024-11-20, category=Food, amount=45.50, payment_method=Card
sale_id=2, employee_id=3, sale_date=2024-11-20, category=Beverage, amount=12.00, payment_method=Cash
```

---

### 5. Daily Sales Summary Table

Pre-calculated daily totals per employee for quick reporting.

```sql
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
```

**Columns:**
- `summary_id`: Unique identifier
- `employee_id`: Employee ID (NULL for company-wide totals)
- `sale_date`: Summary date
- `total_sales`: Total sales amount
- `room_sales`: Sales from room category
- `food_sales`: Sales from food category
- `beverage_sales`: Sales from beverage category
- `service_sales`: Sales from services category
- `transaction_count`: Total number of transactions
- `created_at`: Summary creation timestamp
- `updated_at`: Last update timestamp

**Unique Constraint:**
- (employee_id, sale_date) - One summary per employee per day

**Purpose:**
- Pre-calculated for fast dashboard queries
- Updated whenever a sale is recorded
- Enables quick daily performance analysis

---

### 6. Monthly Sales Report Table

Pre-calculated monthly totals for efficient reporting.

```sql
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
```

**Columns:**
- Similar to daily_sales_summary
- `year`: Year of the report
- `month`: Month of the report (1-12)

**Unique Constraint:**
- (employee_id, year, month) - One report per employee per month

**Purpose:**
- Fast monthly report generation
- Trend analysis
- Year-over-year comparisons

---

### 7. Occupancy Report Table

Daily occupancy metrics.

```sql
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
```

**Columns:**
- `occupancy_id`: Unique identifier
- `report_date`: Date of the report
- `total_rooms`: Total number of rooms in hotel
- `occupied_rooms`: Currently occupied rooms
- `available_rooms`: Available rooms
- `maintenance_rooms`: Rooms in maintenance
- `occupancy_rate`: Percentage occupancy (0-100)
- `created_at`: Report creation timestamp

**Unique Constraint:**
- One report per day

**Calculation:**
```
occupancy_rate = (occupied_rooms / total_rooms) * 100
```

---

### 8. Audit Log Table

Tracks all system changes for security and compliance.

```sql
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
```

**Columns:**
- `log_id`: Unique identifier
- `user_id`: User who made the change
- `action`: Action performed (CREATE, UPDATE, DELETE)
- `entity_type`: Type of entity modified (User, Sale, Room, etc.)
- `entity_id`: ID of the modified entity
- `old_value`: Previous value (JSON or text)
- `new_value`: New value (JSON or text)
- `created_at`: Change timestamp

**Foreign Keys:**
- `user_id` → users.user_id

**Indexes:**
- Index on user_id
- Index on created_at

**Purpose:**
- Compliance and auditing
- Change tracking
- Debugging and support

---

## Indexes

Performance-critical indexes:

```sql
CREATE INDEX idx_sales_employee_date ON sales(employee_id, sale_date);
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_check_ins_room ON check_ins(room_id);
CREATE INDEX idx_check_ins_date ON check_ins(check_in_date, check_out_date);
CREATE INDEX idx_daily_summary_date ON daily_sales_summary(sale_date);
CREATE INDEX idx_monthly_report_date ON monthly_sales_report(year, month);
CREATE INDEX idx_audit_log_user ON audit_log(user_id);
```

---

## Data Relationships

```
users (1) ──────────── (many) sales
users (1) ──────────── (many) check_ins
users (1) ──────────── (many) daily_sales_summary
users (1) ──────────── (many) monthly_sales_report

rooms (1) ──────────── (many) check_ins
```

---

## SQL Queries Examples

### Get daily sales total by employee

```sql
SELECT 
    u.full_name,
    SUM(s.amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales s
JOIN users u ON s.employee_id = u.user_id
WHERE s.sale_date = '2024-11-20'
GROUP BY s.employee_id
ORDER BY total_sales DESC;
```

### Get occupancy rate for date range

```sql
SELECT 
    report_date,
    occupancy_rate,
    occupied_rooms,
    available_rooms
FROM occupancy_report
WHERE report_date BETWEEN '2024-11-01' AND '2024-11-30'
ORDER BY report_date;
```

### Get active guests

```sql
SELECT 
    c.guest_name,
    c.guest_email,
    r.room_number,
    r.room_type,
    c.check_in_date,
    c.check_out_date,
    c.number_of_guests
FROM check_ins c
JOIN rooms r ON c.room_id = r.room_id
WHERE c.status = 'Active'
AND CURRENT_DATE BETWEEN c.check_in_date AND c.check_out_date
ORDER BY c.check_in_date;
```

### Get sales by category for a date

```sql
SELECT 
    category,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM sales
WHERE sale_date = '2024-11-20'
GROUP BY category
ORDER BY total_amount DESC;
```

### Get top performing employees

```sql
SELECT 
    u.full_name,
    SUM(s.amount) as total_sales,
    COUNT(*) as transactions,
    AVG(s.amount) as avg_transaction
FROM sales s
JOIN users u ON s.employee_id = u.user_id
WHERE s.sale_date >= DATE('now', '-30 days')
AND u.role = 'Employee'
GROUP BY s.employee_id
ORDER BY total_sales DESC
LIMIT 10;
```

---

## Database Maintenance

### Backup Database

```bash
sqlite3 backend/database/hotel_management.db ".backup backup.db"
```

### Optimize Database

```bash
sqlite3 backend/database/hotel_management.db "VACUUM;"
```

### Check Database Integrity

```bash
sqlite3 backend/database/hotel_management.db "PRAGMA integrity_check;"
```

### View Database Statistics

```bash
sqlite3 backend/database/hotel_management.db "SELECT name, COUNT(*) FROM (SELECT * FROM users UNION ALL SELECT * FROM sales) GROUP BY name;"
```

---

## Database Size Estimation

For 1 year of operation with 30 employees:
- **Users table**: ~100 KB (50-100 records)
- **Sales table**: ~50 MB (500,000+ transactions)
- **Rooms table**: ~50 KB (100-200 rooms)
- **Check-ins table**: ~10 MB (100,000+ check-ins)
- **Reports tables**: ~5 MB (aggregated data)
- **Total**: ~65 MB

---

## Migration & Version Control

For schema updates, create migration files:

```sql
-- migrations/001_initial_schema.sql
-- migrations/002_add_audit_log.sql
```

Apply migrations:

```python
def run_migration(migration_file):
    db = sqlite3.connect(DATABASE_PATH)
    with open(migration_file, 'r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
```

---

## Performance Tips

1. **Indexes**: Use indexes on frequently filtered columns
2. **Aggregation**: Use pre-calculated summary tables
3. **Archiving**: Archive old data (>1 year) to separate database
4. **Vacuuming**: Run VACUUM periodically to optimize
5. **Batch Operations**: Group updates for efficiency

---

## Security Considerations

1. **Password Storage**: Always hashed using Werkzeug
2. **Soft Deletes**: Users marked inactive, not deleted
3. **Audit Trail**: All changes logged in audit_log
4. **Foreign Keys**: Referential integrity enforced
5. **Backups**: Regular backups recommended for production

---

## Disaster Recovery

### Full Backup

```bash
cp backend/database/hotel_management.db backup_$(date +%Y%m%d).db
```

### Point-in-Time Recovery

```bash
# Restore from backup
cp backup_20241120.db backend/database/hotel_management.db

# Verify integrity
sqlite3 backend/database/hotel_management.db "PRAGMA integrity_check;"
```
