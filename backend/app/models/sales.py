"""Sales model for tracking and reporting sales data"""
import sqlite3
from datetime import datetime, timedelta
from app.utils.database import get_db

class Sales:
    """Sales model for database operations"""
    
    @staticmethod
    def record_sale(employee_id, sale_date, category, amount, description=None, 
                   payment_method=None, transaction_id=None, notes=None):
        """Record a new sale"""
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO sales 
                (employee_id, sale_date, category, amount, description, payment_method, transaction_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (employee_id, sale_date, category, amount, description, payment_method, transaction_id, notes))
            db.commit()
            
            # Update daily summary
            Sales.update_daily_summary(employee_id, sale_date)
            
            return {'success': True, 'sale_id': cursor.lastrowid}
        except sqlite3.IntegrityError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_daily_sales(employee_id=None, sale_date=None):
        """Get sales for a specific date"""
        db = get_db()
        cursor = db.cursor()
        
        if employee_id and sale_date:
            cursor.execute('''
                SELECT * FROM sales 
                WHERE employee_id = ? AND sale_date = ?
                ORDER BY created_at DESC
            ''', (employee_id, sale_date))
        elif sale_date:
            cursor.execute('''
                SELECT * FROM sales 
                WHERE sale_date = ?
                ORDER BY created_at DESC
            ''', (sale_date,))
        else:
            cursor.execute('SELECT * FROM sales ORDER BY created_at DESC LIMIT 100')
        
        return cursor.fetchall()
    
    @staticmethod
    def get_monthly_sales(employee_id=None, year=None, month=None):
        """Get sales for a specific month"""
        db = get_db()
        cursor = db.cursor()
        
        date_filter = f' AND strftime("%Y", sale_date) = "{year}" AND strftime("%m", sale_date) = "{month:02d}"'
        
        if employee_id:
            query = f'SELECT * FROM sales WHERE employee_id = {employee_id}{date_filter}'
        else:
            query = f'SELECT * FROM sales WHERE 1=1{date_filter}'
        
        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod
    def update_daily_summary(employee_id, sale_date):
        """Update or create daily sales summary"""
        db = get_db()
        cursor = db.cursor()
        
        # Calculate totals for the day
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN category = "Room" THEN amount ELSE 0 END) as room_sales,
                SUM(CASE WHEN category = "Food" THEN amount ELSE 0 END) as food_sales,
                SUM(CASE WHEN category = "Beverage" THEN amount ELSE 0 END) as beverage_sales,
                SUM(CASE WHEN category = "Services" THEN amount ELSE 0 END) as service_sales,
                SUM(amount) as total_sales,
                COUNT(*) as transaction_count
            FROM sales
            WHERE employee_id = ? AND sale_date = ?
        ''', (employee_id, sale_date))
        
        result = cursor.fetchone()
        
        # Insert or update summary
        cursor.execute('''
            INSERT INTO daily_sales_summary 
            (employee_id, sale_date, total_sales, room_sales, food_sales, beverage_sales, service_sales, transaction_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(employee_id, sale_date) DO UPDATE SET
                total_sales = ?, room_sales = ?, food_sales = ?, beverage_sales = ?, service_sales = ?, transaction_count = ?
        ''', (employee_id, sale_date, 
              result[4] or 0, result[0] or 0, result[1] or 0, result[2] or 0, result[3] or 0, result[5] or 0,
              result[4] or 0, result[0] or 0, result[1] or 0, result[2] or 0, result[3] or 0, result[5] or 0))
        db.commit()
    
    @staticmethod
    def get_employee_daily_performance(employee_id):
        """Get employee's daily performance summary"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT * FROM daily_sales_summary
            WHERE employee_id = ?
            ORDER BY sale_date DESC
            LIMIT 30
        ''', (employee_id,))
        return cursor.fetchall()
    
    @staticmethod
    def get_all_daily_sales(sale_date):
        """Get all sales for a date across all employees"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT u.user_id, u.full_name, SUM(s.amount) as total,
                   COUNT(*) as transactions
            FROM sales s
            JOIN users u ON s.employee_id = u.user_id
            WHERE s.sale_date = ?
            GROUP BY s.employee_id
        ''', (sale_date,))
        return cursor.fetchall()
    
    @staticmethod
    def get_monthly_summary(year, month, employee_id=None):
        """Get monthly summary"""
        db = get_db()
        cursor = db.cursor()
        
        if employee_id:
            cursor.execute('''
                SELECT * FROM monthly_sales_report
                WHERE year = ? AND month = ? AND employee_id = ?
            ''', (year, month, employee_id))
        else:
            cursor.execute('''
                SELECT * FROM monthly_sales_report
                WHERE year = ? AND month = ?
            ''', (year, month))
        
        return cursor.fetchall()
