# Hotel Management and Sales Analysis System

## Project Overview

A comprehensive, full-stack Hotel Management System built with Python (Flask) backend and HTML/CSS/JavaScript frontend. This system provides complete functionality for managing hotel operations, employee sales tracking, room management, and generating detailed analytics reports.

## Features

### Core Functionality

1. **Role-Based Access Control**
   - Employee: Record sales, view personal performance
   - Manager: Manage employees, view all sales, generate reports
   - Admin: Full system access including employee and room management

2. **Sales Management**
   - Record daily sales by employee
   - Track sales by category (Room, Food, Beverage, Services, Other)
   - Support multiple payment methods
   - Transaction tracking and audit logs

3. **Room Management**
   - Guest check-in/check-out functionality
   - Room status tracking (Available, Occupied, Maintenance)
   - Occupancy rate calculations
   - Room inventory management

4. **Employee Management**
   - Employee registration and profile management
   - Department assignment
   - Performance tracking
   - User deactivation

5. **Analytics & Reporting**
   - Daily sales summaries
   - Monthly and yearly reports
   - Employee performance leaderboards
   - Sales trend visualization
   - Occupancy analytics
   - Export to Excel and PDF

6. **Dashboard**
   - Real-time sales overview
   - Key performance indicators
   - Interactive charts and graphs
   - Sales trend analysis

## Project Structure

```
hotel_management_system/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py          # User model and authentication
│   │   │   ├── sales.py         # Sales tracking model
│   │   │   └── room.py          # Room management model
│   │   ├── routes/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── sales.py         # Sales API routes
│   │   │   ├── employees.py     # Employee management routes
│   │   │   ├── rooms.py         # Room management routes
│   │   │   ├── reports.py       # Report generation routes
│   │   │   └── dashboard.py     # Dashboard analytics routes
│   │   ├── utils/
│   │   │   ├── database.py      # Database connection and initialization
│   │   │   ├── auth.py          # JWT token management
│   │   │   └── export.py        # Excel/PDF export functionality
│   │   └── __init__.py          # Flask app factory
│   ├── run.py                   # Application entry point
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── index.html               # Main application page
│   ├── css/
│   │   ├── styles.css           # Main stylesheet
│   │   └── responsive.css       # Mobile responsive styles
│   ├── js/
│   │   ├── api.js               # API service module
│   │   ├── app.js               # Main application controller
│   │   └── charts.js            # Chart visualization service
│   └── assets/                  # Images and resources
├── database/
│   ├── schema.sql               # Database schema
│   └── hotel_management.db      # SQLite database (created at runtime)
└── docs/
    ├── README.md                # This file
    ├── SETUP.md                 # Installation and setup guide
    ├── API_DOCUMENTATION.md     # API endpoints documentation
    └── DATABASE_SCHEMA.md       # Database schema details
```

## Technology Stack

### Backend
- **Framework**: Flask 2.3.0
- **Database**: SQLite3
- **Authentication**: JWT (JSON Web Tokens)
- **Export**: openpyxl (Excel), reportlab (PDF)
- **Security**: Werkzeug password hashing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design with Grid/Flexbox
- **JavaScript**: Vanilla JS (ES6+)
- **Charts**: Chart.js for data visualization
- **API**: Fetch API for backend communication

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js (optional, for local development server)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Backend Setup

1. **Install Python Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

2. **Initialize Database**

The database is automatically initialized when the application first runs.

3. **Run the Server**

```bash
python run.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Open in Browser**

Simply open `frontend/index.html` in your web browser, or serve it through a local web server:

```bash
# Using Python
cd frontend
python -m http.server 8000

# Using Node.js http-server
cd frontend
npx http-server
```

Then navigate to `http://localhost:8000`

### Important Configuration

Update the API base URL in `frontend/js/api.js` if your backend is running on a different URL:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## Demo Credentials

Default users are automatically created on first run:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| manager1 | manager123 | Manager |
| waiter1 | waiter123 | Employee |
| waiter2 | waiter123 | Employee |
| receptionist1 | recept123 | Employee |

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/verify-token` - Verify JWT token
- `GET /api/auth/profile` - Get current user profile

### Sales Management
- `POST /api/sales/record` - Record a new sale
- `GET /api/sales/daily/<employee_id>/<date>` - Get daily sales
- `GET /api/sales/monthly/<year>/<month>` - Get monthly sales
- `GET /api/sales/daily-summary/<date>` - Get daily summary
- `GET /api/sales/employee-performance/<employee_id>` - Get employee performance

### Employee Management
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee (Admin only)
- `GET /api/employees/<employee_id>` - Get employee details
- `PUT /api/employees/<employee_id>` - Update employee (Admin only)
- `PUT /api/employees/<employee_id>/deactivate` - Deactivate employee (Admin only)

### Room Management
- `GET /api/rooms/` - List all rooms
- `GET /api/rooms/available` - Get available rooms
- `POST /api/rooms/` - Create new room (Admin only)
- `POST /api/rooms/<room_id>/check-in` - Check in guest
- `POST /api/rooms/<room_id>/check-out` - Check out guest
- `GET /api/rooms/active-check-ins` - Get active check-ins
- `GET /api/rooms/occupancy-report` - Get occupancy report

### Dashboard & Reports
- `GET /api/dashboard/overview` - Get dashboard overview
- `GET /api/dashboard/sales-trend/<days>` - Get sales trend
- `GET /api/dashboard/employee-leaderboard` - Get top performers
- `GET /api/dashboard/category-breakdown/<date>` - Sales by category
- `GET /reports/daily/<date>` - Daily report
- `GET /reports/monthly/<year>/<month>` - Monthly report
- `GET /reports/yearly/<year>` - Yearly report
- `GET /reports/export/daily/<date>?format=excel|pdf` - Export daily report
- `GET /reports/export/monthly/<year>/<month>?format=excel|pdf` - Export monthly report

## Database Schema

### Users Table
```sql
- user_id (PRIMARY KEY)
- username (UNIQUE)
- password (hashed)
- email (UNIQUE)
- full_name
- role (Employee, Manager, Admin)
- department
- phone
- is_active
- created_at, updated_at
```

### Sales Table
```sql
- sale_id (PRIMARY KEY)
- employee_id (FOREIGN KEY)
- sale_date
- category (Room, Food, Beverage, Services, Other)
- description
- amount
- payment_method (Cash, Card, Mobile, Check, Online)
- transaction_id (UNIQUE)
- notes
- created_at
```

### Rooms Table
```sql
- room_id (PRIMARY KEY)
- room_number (UNIQUE)
- room_type (Single, Double, Suite, Deluxe)
- capacity
- price_per_night
- status (Available, Occupied, Maintenance)
- created_at, updated_at
```

### Check-ins Table
```sql
- check_in_id (PRIMARY KEY)
- room_id (FOREIGN KEY)
- guest_name
- guest_email
- guest_phone
- check_in_date
- check_out_date
- number_of_guests
- check_in_employee_id (FOREIGN KEY)
- status (Active, Completed, Cancelled)
- notes
- created_at, updated_at
```

### Daily/Monthly Sales Summary Tables
- Aggregate sales data by date and employee
- Breakdown by category
- Transaction counts
- Used for quick report generation

### Occupancy Report Table
```sql
- occupancy_id (PRIMARY KEY)
- report_date (UNIQUE)
- total_rooms
- occupied_rooms
- available_rooms
- maintenance_rooms
- occupancy_rate (percentage)
- created_at
```

## User Interface

### Login Page
- Role selection dropdown
- Username and password fields
- Demo credentials display
- Responsive login form

### Dashboard
- Key performance indicators (KPIs) cards
- Sales trend line chart (7 days)
- Sales breakdown by category (doughnut chart)
- Top 10 performing employees leaderboard
- Real-time occupancy metrics

### Sales Page
- Record new sale form
- Today's sales list
- Sale details: date, category, amount, payment method
- Employees can only see their own sales

### Rooms Page
- Visual room cards showing status
- Check-in/check-out functionality
- Active guest check-ins list
- Occupancy rate indicator

### Employees Page
- List all employees (Manager/Admin only)
- Add new employee form (Admin only)
- Employee details: name, role, department, status
- Deactivation functionality

### Reports Page
- Multiple report types: Daily, Monthly, Yearly, Employee Performance
- Dynamic date selection
- Export to Excel or PDF
- Tabular and graphical representations

## Security Features

1. **Authentication**
   - JWT-based token authentication
   - Secure password hashing with Werkzeug
   - Token expiry (24 hours)

2. **Authorization**
   - Role-based access control (RBAC)
   - Endpoint-level permission checks
   - Resource-level access restrictions

3. **Data Protection**
   - SQL injection prevention via parameterized queries
   - Input validation on all forms
   - CORS enabled for frontend-backend communication

4. **Audit Trail**
   - Audit log table for tracking changes
   - User action logging
   - Timestamp tracking on all records

## Performance Considerations

1. **Database Indexes**
   - Indexes on frequently queried columns
   - Composite indexes for common query patterns
   - Optimized for real-time dashboard queries

2. **Caching**
   - Daily and monthly summaries pre-calculated
   - Occupancy reports generated on demand

3. **API Optimization**
   - Efficient database queries
   - Pagination support for large datasets
   - Minimal data transfer

## Export Functionality

### Excel Export
- Formatted spreadsheets with:
  - Title and timestamp
  - Styled headers
  - Auto-adjusted column widths
  - Data tables with borders

### PDF Export
- Professional PDF documents with:
  - Report title
  - Formatted tables
  - Generation timestamp
  - Print-ready formatting

## Mobile Responsiveness

The frontend is fully responsive with breakpoints for:
- Desktop (>1024px)
- Tablet (768px - 1024px)
- Mobile (<768px)

Features:
- Hamburger menu on mobile
- Stacked layouts
- Touch-friendly buttons
- Optimized table display

## Troubleshooting

### Backend Won't Start
- Ensure Python 3.8+ is installed
- Check all dependencies: `pip install -r requirements.txt`
- Verify port 5000 is not in use: `lsof -i :5000`

### Frontend Not Loading Data
- Check backend is running on correct port
- Verify API_BASE_URL in `js/api.js`
- Check browser console for errors
- Ensure CORS is enabled in Flask app

### Database Issues
- Delete `database/hotel_management.db` to reset
- Database will auto-initialize on next backend start
- Check file permissions on database directory

### Login Issues
- Clear browser localStorage: `localStorage.clear()`
- Verify demo credentials above
- Check backend logs for authentication errors

## Future Enhancements

1. Multi-language support
2. Advanced analytics with machine learning predictions
3. Mobile app (React Native/Flutter)
4. Real-time notifications
5. SMS/Email notifications for guests
6. Inventory management system
7. Guest loyalty program
8. Third-party payment integration
9. Temperature and occupancy sensors
10. Mobile check-in/check-out

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the documentation in `/docs`
2. Review API endpoints in `API_DOCUMENTATION.md`
3. Examine database schema in `DATABASE_SCHEMA.md`
4. Check browser console and backend logs for errors

## Version

Hotel Management System v1.0.0
Last Updated: November 2025
