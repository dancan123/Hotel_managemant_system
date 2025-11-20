"""Dashboard routes for analytics"""
from flask import Blueprint, request, jsonify
from app.models.sales import Sales
from app.models.room import Room
from app.utils.auth import token_required, role_required
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/overview', methods=['GET'])
@token_required
def get_dashboard_overview():
    """Get dashboard overview data"""
    today = datetime.now().date().isoformat()
    
    # Get today's sales
    daily_sales = Sales.get_all_daily_sales(today)
    total_today = sum(row[2] for row in daily_sales)
    
    # Get occupancy
    occupancy = Room.get_occupancy_report(today)
    
    return jsonify({
        'success': True,
        'overview': {
            'today_sales': total_today,
            'total_transactions': sum(row[3] for row in daily_sales),
            'occupancy_rate': occupancy[6] if occupancy else 0,
            'occupied_rooms': occupancy[3] if occupancy else 0,
            'total_rooms': occupancy[2] if occupancy else 0
        }
    }), 200

@bp.route('/sales-trend/<int:days>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_sales_trend(days):
    """Get sales trend for last N days"""
    trend_data = []
    
    for i in range(days, 0, -1):
        date = (datetime.now().date() - timedelta(days=i)).isoformat()
        sales = Sales.get_all_daily_sales(date)
        total = sum(row[2] for row in sales)
        
        trend_data.append({
            'date': date,
            'total_sales': total,
            'transaction_count': sum(row[3] for row in sales)
        })
    
    return jsonify({
        'success': True,
        'trend': trend_data
    }), 200

@bp.route('/employee-leaderboard', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_employee_leaderboard():
    """Get top performing employees"""
    days = int(request.args.get('days', 30))
    
    employee_totals = {}
    
    for i in range(days, 0, -1):
        date = (datetime.now().date() - timedelta(days=i)).isoformat()
        sales = Sales.get_all_daily_sales(date)
        
        for row in sales:
            emp_id = row[0]
            if emp_id not in employee_totals:
                employee_totals[emp_id] = {
                    'name': row[1],
                    'total': 0,
                    'transactions': 0
                }
            employee_totals[emp_id]['total'] += row[2]
            employee_totals[emp_id]['transactions'] += row[3]
    
    # Sort by total sales
    leaderboard = sorted(
        employee_totals.values(),
        key=lambda x: x['total'],
        reverse=True
    )[:10]
    
    return jsonify({
        'success': True,
        'leaderboard': leaderboard,
        'period_days': days
    }), 200

@bp.route('/category-breakdown/<date>', methods=['GET'])
@token_required
def get_category_breakdown(date):
    """Get sales breakdown by category"""
    from app.utils.database import get_db
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT category, SUM(amount) as total
        FROM sales
        WHERE sale_date = ?
        GROUP BY category
    ''', (date,))
    
    results = cursor.fetchall()
    
    return jsonify({
        'success': True,
        'breakdown': [{
            'category': row[0],
            'total': row[1]
        } for row in results]
    }), 200

@bp.route('/payment-method-breakdown/<date>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_payment_breakdown(date):
    """Get payment method breakdown"""
    from app.utils.database import get_db
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT payment_method, COUNT(*) as count, SUM(amount) as total
        FROM sales
        WHERE sale_date = ?
        GROUP BY payment_method
    ''', (date,))
    
    results = cursor.fetchall()
    
    return jsonify({
        'success': True,
        'breakdown': [{
            'payment_method': row[0],
            'count': row[1],
            'total': row[2]
        } for row in results]
    }), 200
