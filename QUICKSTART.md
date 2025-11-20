# Quick Start Guide

## 5-Minute Setup

### Prerequisites Check
- Python 3.8+ installed
- Browser available

### Step 1: Install Backend (2 minutes)

```bash
cd hotel_management_system/backend
pip install -r requirements.txt
```

### Step 2: Start Backend (1 minute)

```bash
python run.py
```

Output should show:
```
Running on http://0.0.0.0:5000
```

### Step 3: Open Frontend (1 minute)

Open `hotel_management_system/frontend/index.html` in your browser

### Step 4: Login (1 minute)

Use demo credentials:
- **Admin**: admin / admin123
- **Manager**: manager1 / manager123
- **Employee**: waiter1 / waiter123

---

## System Overview

### What Each Role Can Do

#### Admin
✓ View all sales  
✓ Manage all employees  
✓ Create/delete rooms  
✓ Generate all reports  
✓ View analytics  

#### Manager
✓ View all employee sales  
✓ View rooms status  
✓ Check in/out guests  
✓ Generate reports  
✓ View leaderboards  

#### Employee
✓ Record own sales  
✓ View own performance  
✓ Check room status  

---

## Basic Workflows

### Record a Sale (Employee)

1. Navigate to **Sales** tab
2. Click **Record Sale**
3. Fill in:
   - Sale Date
   - Category (Food, Beverage, Room, Services, Other)
   - Amount ($)
   - Payment Method
   - Description (optional)
4. Click **Record Sale**

### Check In Guest (Receptionist/Manager)

1. Navigate to **Rooms** tab
2. Click **Check In Guest**
3. Select room from dropdown
4. Fill in guest information:
   - Guest Name
   - Check-in Date
   - Check-out Date
   - Phone/Email (optional)
5. Click **Check In**

### View Daily Report (Manager)

1. Navigate to **Reports** tab
2. Report Type: Select "Daily"
3. Date: Choose date
4. Click **Generate Report**
5. (Optional) Click **Export** to download as Excel/PDF

### Add Employee (Admin)

1. Navigate to **Employees** tab
2. Click **Add Employee**
3. Fill in:
   - Username
   - Password
   - Email
   - Full Name
   - Role
   - Department
4. Click **Add Employee**

---

## Dashboard Explained

### Stats Cards
- **Today's Sales**: Total revenue for the current day
- **Transactions**: Number of transactions today
- **Occupancy Rate**: Percentage of occupied rooms
- **Occupied Rooms**: Actual count vs total

### Charts
- **Sales Trend**: Last 7 days of sales (line chart)
- **Sales by Category**: Distribution across categories (pie chart)

### Top Performers
- Leaderboard of top 10 employees by sales
- Shows total sales and transaction count

---

## Common Tasks

### Export Daily Report as PDF

1. Go to **Reports**
2. Select "Daily" report type
3. Choose date
4. Select "PDF" in Export As dropdown
5. Click **Generate Report**
6. Click **Export**

### Check Occupancy

1. Go to **Rooms** tab
2. View room cards (green=available, red=occupied)
3. Check occupancy percentage at top

### View Employee Performance

1. As Manager: Go to **Reports** > "Employee Performance"
2. Select employee's date range
3. View daily breakdown by category

### Deactivate Employee

1. As Admin: Go to **Employees** tab
2. Find employee in list
3. Click **Deactivate** button (if available)

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Navigate form fields |
| `Enter` | Submit form |
| `Escape` | Close dialog |

---

## Troubleshooting Quick Fixes

### Problem: "Cannot connect to API"
**Solution**: 
- Verify backend running: `python run.py`
- Check API URL in `frontend/js/api.js`
- Ensure port 5000 is not blocked

### Problem: "Login failed"
**Solution**:
- Clear browser cache
- Try demo credentials
- Restart backend

### Problem: "Database error"
**Solution**:
- Delete `backend/database/hotel_management.db`
- Restart backend (database auto-creates)

### Problem: "Charts not showing"
**Solution**:
- Wait 5 seconds for data to load
- Refresh page (F5)
- Check browser console for errors

---

## File Structure Quick Reference

```
hotel_management_system/
├── backend/run.py              ← Start backend here
├── frontend/index.html         ← Open in browser
├── frontend/js/api.js          ← API configuration
├── database/hotel_management.db ← Auto-created database
└── docs/                       ← Full documentation
```

---

## API Endpoints Cheat Sheet

### Most Used Endpoints

```
POST   /api/auth/login                  - Login
POST   /api/sales/record                - Record sale
GET    /api/dashboard/overview          - Dashboard data
GET    /api/reports/daily/{date}        - Daily report
GET    /api/rooms/available             - Available rooms
POST   /api/rooms/{id}/check-in         - Check in guest
GET    /api/employees/                  - List employees
```

Full documentation: See `docs/API_DOCUMENTATION.md`

---

## Default Sample Data

### Employees
- Admin: admin (admin123)
- Manager: manager1 (manager123)
- Waiter: waiter1 (waiter123)
- Waiter: waiter2 (waiter123)
- Receptionist: receptionist1 (recept123)

### Rooms
- Room 101-102: Single/Double (Dining floor)
- Room 201-202: Suite/Deluxe (Premium floor)
- Room 301-302: Single/Double (Economy floor)

---

## Performance Tips

1. **Dashboard loads slow?**
   - Ensure backend has been running for a few minutes
   - Sales data calculates in real-time

2. **Too many rooms?**
   - Use search/filter if available
   - Navigate faster with keyboard (Tab/Enter)

3. **Need older data?**
   - Historical data preserved indefinitely
   - Use Reports section for date range queries

---

## Next Steps

1. **Read Full Documentation**: `docs/README.md`
2. **Explore API**: `docs/API_DOCUMENTATION.md`
3. **Understand Database**: `docs/DATABASE_SCHEMA.md`
4. **Deployment**: `docs/SETUP.md` (Production section)

---

## Need Help?

### Documentation Files
- **README.md** - Complete system overview
- **SETUP.md** - Detailed installation and configuration
- **API_DOCUMENTATION.md** - All API endpoints
- **DATABASE_SCHEMA.md** - Database structure

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Port 5000 in use | Another app using port | `netstat -ano \| findstr :5000` |
| Module not found | Missing dependencies | `pip install -r requirements.txt` |
| CORS error | API URL incorrect | Check `frontend/js/api.js` |
| Database locked | Concurrent access | Restart backend |

---

## Demo Workflow

Try this complete workflow:

1. **Login as Admin** (admin/admin123)
2. **View Dashboard** - See today's sales, occupancy
3. **Add Employee** - Create a new waiter
4. **Login as Employee** - Use new credentials
5. **Record Sales** - Add 3-4 sample sales
6. **View Performance** - See your daily totals
7. **Login as Manager** - View all employees' sales
8. **Generate Report** - Export daily sales as Excel
9. **Check In Guest** - Add a guest to a room
10. **View Occupancy** - See updated occupancy rate

---

## Security Reminders

- **Don't share credentials** via unencrypted channels
- **Change default passwords** in production
- **Use HTTPS** for deployment
- **Regular backups** of database
- **Keep software updated**

---

## Useful Commands

### Backend Management

```bash
# Start backend
cd backend && python run.py

# Reset database
rm backend/database/hotel_management.db

# Check Python version
python --version

# List installed packages
pip list
```

### Database Queries

```bash
# Access database directly
sqlite3 backend/database/hotel_management.db

# Check total sales
SELECT SUM(amount) FROM sales;

# List all users
SELECT user_id, full_name, role FROM users;

# Count active check-ins
SELECT COUNT(*) FROM check_ins WHERE status='Active';
```

---

## Version Information

- **System Version**: 1.0.0
- **Python Required**: 3.8+
- **Flask Version**: 2.3.0
- **Database**: SQLite3
- **Browser Support**: All modern browsers

---

## Feedback

For improvements or bug reports, refer to the documentation for advanced configuration options.

---

**Last Updated**: November 2025
**Status**: Production Ready
