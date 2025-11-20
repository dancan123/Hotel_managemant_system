# API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

All endpoints (except `/auth/login`) require a JWT token in the `Authorization` header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Response Format

All responses are JSON with the following format:

```json
{
  "success": true/false,
  "data": {...},
  "error": "error message (if applicable)"
}
```

---

## Authentication Endpoints

### POST /auth/login

Login and obtain JWT token.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123",
  "role": "Admin"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "user_id": 1,
    "username": "admin",
    "email": "admin@hotel.com",
    "full_name": "Administrator",
    "role": "Admin",
    "department": null
  }
}
```

**Status Codes:**
- 200: Login successful
- 400: Missing fields
- 401: Invalid credentials

---

### POST /auth/logout

Logout user (client-side token deletion).

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### POST /auth/verify-token

Verify token validity.

**Response:**
```json
{
  "success": true,
  "user": {
    "user_id": 1,
    "role": "Admin",
    "username": "admin"
  }
}
```

---

### GET /auth/profile

Get current user profile.

**Response:**
```json
{
  "success": true,
  "user": {
    "user_id": 1,
    "username": "admin",
    "email": "admin@hotel.com",
    "full_name": "Administrator",
    "role": "Admin",
    "department": null,
    "phone": null
  }
}
```

---

## Sales Endpoints

### POST /sales/record

Record a new sale.

**Required Permission:** Employee (own sales), Manager/Admin (any sales)

**Request:**
```json
{
  "sale_date": "2024-11-20",
  "category": "Food",
  "amount": 45.50,
  "description": "Lunch service",
  "payment_method": "Card",
  "transaction_id": "TXN123456",
  "employee_id": 2  // Required if Manager/Admin recording for someone else
}
```

**Response:**
```json
{
  "success": true,
  "message": "Sale recorded successfully",
  "sale_id": 42
}
```

**Category Options:** Room, Food, Beverage, Services, Other

**Payment Methods:** Cash, Card, Mobile, Check, Online

---

### GET /sales/daily/<employee_id>/<date>

Get daily sales for an employee.

**Example:** `/sales/daily/2/2024-11-20`

**Response:**
```json
{
  "success": true,
  "sales": [
    {
      "sale_id": 1,
      "employee_id": 2,
      "sale_date": "2024-11-20",
      "category": "Food",
      "description": "Lunch",
      "amount": 45.50,
      "payment_method": "Card"
    }
  ]
}
```

---

### GET /sales/monthly/<year>/<month>

Get monthly sales.

**Example:** `/sales/monthly/2024/11`

**Query Parameters:**
- `employee_id` (optional): Filter by specific employee

**Response:**
```json
{
  "success": true,
  "sales": [
    {
      "sale_id": 1,
      "employee_id": 2,
      "sale_date": "2024-11-20",
      "category": "Food",
      "amount": 45.50
    }
  ]
}
```

---

### GET /sales/daily-summary/<date>

Get daily sales summary across all employees.

**Example:** `/sales/daily-summary/2024-11-20`

**Response:**
```json
{
  "success": true,
  "summary": [
    {
      "user_id": 2,
      "employee_name": "James Smith",
      "total_sales": 450.00,
      "transactions": 12
    }
  ]
}
```

---

### GET /sales/employee-performance/<employee_id>

Get employee's last 30 days of performance.

**Example:** `/sales/employee-performance/2`

**Response:**
```json
{
  "success": true,
  "performance": [
    {
      "summary_id": 1,
      "employee_id": 2,
      "sale_date": "2024-11-20",
      "total_sales": 450.00,
      "room_sales": 100.00,
      "food_sales": 200.00,
      "beverage_sales": 100.00,
      "service_sales": 50.00,
      "transaction_count": 12
    }
  ]
}
```

---

### GET /sales/categories

Get available sale categories.

**Response:**
```json
{
  "success": true,
  "categories": ["Room", "Food", "Beverage", "Services", "Other"]
}
```

---

### GET /sales/payment-methods

Get available payment methods.

**Response:**
```json
{
  "success": true,
  "methods": ["Cash", "Card", "Mobile", "Check", "Online"]
}
```

---

## Employee Endpoints

### GET /employees/

List all employees.

**Required Permission:** Manager, Admin

**Query Parameters:**
- `role` (optional): Filter by role (Employee, Manager, Admin)

**Response:**
```json
{
  "success": true,
  "employees": [
    {
      "user_id": 2,
      "username": "waiter1",
      "email": "waiter1@hotel.com",
      "full_name": "James Smith",
      "role": "Employee",
      "department": "Dining",
      "phone": null,
      "is_active": true
    }
  ]
}
```

---

### GET /employees/<employee_id>

Get employee details.

**Response:**
```json
{
  "success": true,
  "employee": {
    "user_id": 2,
    "username": "waiter1",
    "email": "waiter1@hotel.com",
    "full_name": "James Smith",
    "role": "Employee",
    "department": "Dining",
    "phone": null,
    "is_active": true
  }
}
```

---

### POST /employees/

Create new employee.

**Required Permission:** Admin

**Request:**
```json
{
  "username": "newwaiter",
  "password": "password123",
  "email": "newwaiter@hotel.com",
  "full_name": "New Waiter",
  "role": "Employee",
  "department": "Dining",
  "phone": "555-1234"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Employee created successfully",
  "user_id": 10
}
```

---

### PUT /employees/<employee_id>

Update employee information.

**Required Permission:** Admin, Manager

**Request:**
```json
{
  "email": "newemail@hotel.com",
  "full_name": "Updated Name",
  "department": "Front Desk"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Employee updated successfully"
}
```

---

### PUT /employees/<employee_id>/deactivate

Deactivate employee.

**Required Permission:** Admin

**Response:**
```json
{
  "success": true,
  "message": "Employee deactivated successfully"
}
```

---

## Room Endpoints

### GET /rooms/

List all rooms.

**Response:**
```json
{
  "success": true,
  "rooms": [
    {
      "room_id": 1,
      "room_number": "101",
      "room_type": "Single",
      "capacity": 1,
      "price_per_night": 50.00,
      "status": "Available"
    }
  ]
}
```

---

### GET /rooms/available

Get available rooms only.

**Response:**
```json
{
  "success": true,
  "rooms": [
    {
      "room_id": 1,
      "room_number": "101",
      "room_type": "Single",
      "capacity": 1,
      "price_per_night": 50.00
    }
  ]
}
```

---

### POST /rooms/

Create new room.

**Required Permission:** Admin

**Request:**
```json
{
  "room_number": "401",
  "room_type": "Suite",
  "capacity": 4,
  "price_per_night": 150.00
}
```

**Response:**
```json
{
  "success": true,
  "message": "Room created successfully",
  "room_id": 10
}
```

**Room Types:** Single, Double, Suite, Deluxe

---

### POST /rooms/<room_id>/check-in

Check in a guest.

**Request:**
```json
{
  "guest_name": "John Doe",
  "check_in_date": "2024-11-20",
  "check_out_date": "2024-11-23",
  "guest_email": "john@example.com",
  "guest_phone": "555-1234",
  "number_of_guests": 2,
  "notes": "Non-smoking room preferred"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Guest checked in successfully",
  "check_in_id": 5
}
```

---

### POST /rooms/<room_id>/check-out

Check out a guest.

**Request:**
```json
{
  "check_in_id": 5
}
```

**Response:**
```json
{
  "success": true,
  "message": "Guest checked out successfully"
}
```

---

### GET /rooms/active-check-ins

Get all active guest check-ins.

**Required Permission:** Manager, Admin

**Response:**
```json
{
  "success": true,
  "check_ins": [
    {
      "check_in_id": 5,
      "room_id": 1,
      "guest_name": "John Doe",
      "guest_email": "john@example.com",
      "guest_phone": "555-1234",
      "check_in_date": "2024-11-20",
      "check_out_date": "2024-11-23",
      "number_of_guests": 2,
      "room_number": "101",
      "employee_name": "James Smith"
    }
  ]
}
```

---

### GET /rooms/occupancy-report

Get current occupancy report.

**Required Permission:** Manager, Admin

**Response:**
```json
{
  "success": true,
  "occupancy": {
    "occupancy_id": 1,
    "report_date": "2024-11-20",
    "total_rooms": 6,
    "occupied_rooms": 3,
    "available_rooms": 2,
    "maintenance_rooms": 1,
    "occupancy_rate": 50.0
  }
}
```

---

## Dashboard Endpoints

### GET /dashboard/overview

Get dashboard overview data.

**Response:**
```json
{
  "success": true,
  "overview": {
    "today_sales": 2450.00,
    "total_transactions": 45,
    "occupancy_rate": 50.0,
    "occupied_rooms": 3,
    "total_rooms": 6
  }
}
```

---

### GET /dashboard/sales-trend/<days>

Get sales trend for last N days.

**Example:** `/dashboard/sales-trend/7`

**Response:**
```json
{
  "success": true,
  "trend": [
    {
      "date": "2024-11-14",
      "total_sales": 1500.00,
      "transaction_count": 30
    },
    {
      "date": "2024-11-15",
      "total_sales": 1750.00,
      "transaction_count": 35
    }
  ]
}
```

---

### GET /dashboard/employee-leaderboard

Get top 10 performing employees.

**Query Parameters:**
- `days` (optional, default: 30): Number of days to analyze

**Response:**
```json
{
  "success": true,
  "leaderboard": [
    {
      "name": "James Smith",
      "total": 5600.00,
      "transactions": 120
    }
  ],
  "period_days": 30
}
```

---

### GET /dashboard/category-breakdown/<date>

Get sales breakdown by category.

**Example:** `/dashboard/category-breakdown/2024-11-20`

**Response:**
```json
{
  "success": true,
  "breakdown": [
    {
      "category": "Food",
      "total": 800.00
    },
    {
      "category": "Room",
      "total": 1200.00
    }
  ]
}
```

---

### GET /dashboard/payment-method-breakdown/<date>

Get payment method breakdown.

**Example:** `/dashboard/payment-method-breakdown/2024-11-20`

**Required Permission:** Manager, Admin

**Response:**
```json
{
  "success": true,
  "breakdown": [
    {
      "payment_method": "Card",
      "count": 25,
      "total": 1500.00
    }
  ]
}
```

---

## Reports Endpoints

### GET /reports/daily/<date>

Get daily sales report.

**Example:** `/reports/daily/2024-11-20`

**Required Permission:** Manager, Admin

**Response:**
```json
{
  "success": true,
  "report": {
    "date": "2024-11-20",
    "total_sales": 2450.00,
    "total_transactions": 45,
    "employees": [
      {
        "user_id": 2,
        "employee_name": "James Smith",
        "total_sales": 450.00,
        "transactions": 12
      }
    ]
  }
}
```

---

### GET /reports/monthly/<year>/<month>

Get monthly sales report.

**Example:** `/reports/monthly/2024/11`

**Required Permission:** Manager, Admin

**Response:**
```json
{
  "success": true,
  "report": {
    "year": 2024,
    "month": 11,
    "total_sales": 75000.00,
    "total_transactions": 1500
  }
}
```

---

### GET /reports/yearly/<year>

Get yearly sales report.

**Example:** `/reports/yearly/2024`

**Required Permission:** Manager, Admin

**Response:**
```json
{
  "success": true,
  "report": {
    "year": 2024,
    "total_sales": 850000.00,
    "monthly_breakdown": [
      {
        "month": 1,
        "total": 70000.00
      }
    ]
  }
}
```

---

### GET /reports/employee-performance/<employee_id>/<period>

Get employee performance report.

**Example:** `/reports/employee-performance/2/monthly`

**Response:**
```json
{
  "success": true,
  "report": {
    "employee_id": 2,
    "period": "monthly",
    "total_sales": 5400.00,
    "avg_daily_sales": 180.00,
    "daily_performance": [
      {
        "date": "2024-11-01",
        "total_sales": 150.00,
        "room_sales": 0.00,
        "food_sales": 100.00,
        "beverage_sales": 50.00,
        "service_sales": 0.00,
        "transactions": 5
      }
    ]
  }
}
```

---

### GET /reports/export/daily/<date>

Export daily report to Excel or PDF.

**Example:** `/reports/export/daily/2024-11-20?format=excel`

**Query Parameters:**
- `format`: excel or pdf

**Response:** File download

**Required Permission:** Manager, Admin

---

### GET /reports/export/monthly/<year>/<month>

Export monthly report to Excel or PDF.

**Example:** `/reports/export/monthly/2024/11?format=pdf`

**Query Parameters:**
- `format`: excel or pdf

**Response:** File download

**Required Permission:** Manager, Admin

---

## Error Responses

### Unauthorized (401)

```json
{
  "success": false,
  "error": "Token is missing"
}
```

### Forbidden (403)

```json
{
  "success": false,
  "error": "Insufficient permissions"
}
```

### Bad Request (400)

```json
{
  "success": false,
  "error": "Missing required fields"
}
```

### Not Found (404)

```json
{
  "success": false,
  "error": "Employee not found"
}
```

### Server Error (500)

```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Rate Limiting

Currently not implemented. Will be added in future versions for production use.

## Webhooks

Not currently available. Integration roadmap item for future releases.
