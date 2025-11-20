"""Sales routes"""
from flask import Blueprint, request, jsonify
from app.models.sales import Sales
from app.models.user import User
from app.utils.auth import token_required, role_required
from datetime import datetime

bp = Blueprint('sales', __name__, url_prefix='/api/sales')

@bp.route('/record', methods=['POST'])
@token_required
def record_sale():
    """Record a new sale"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ['sale_date', 'category', 'amount']):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    # Employee can only record their own sales
    employee_id = data.get('employee_id')
    if request.user['role'] == 'Employee':
        employee_id = request.user['user_id']
    elif not employee_id and request.user['role'] in ['Manager', 'Admin']:
        return jsonify({'success': False, 'error': 'Employee ID required'}), 400
    
    result = Sales.record_sale(
        employee_id=employee_id,
        sale_date=data['sale_date'],
        category=data['category'],
        amount=float(data['amount']),
        description=data.get('description'),
        payment_method=data.get('payment_method'),
        transaction_id=data.get('transaction_id'),
        notes=data.get('notes')
    )
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Sale recorded successfully',
            'sale_id': result['sale_id']
        }), 201
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@bp.route('/daily/<employee_id>/<date>', methods=['GET'])
@token_required
def get_daily_sales(employee_id, date):
    """Get daily sales for an employee"""
    sales = Sales.get_daily_sales(int(employee_id), date)
    
    return jsonify({
        'success': True,
        'sales': [{
            'sale_id': row[0],
            'employee_id': row[1],
            'sale_date': row[2],
            'category': row[3],
            'description': row[4],
            'amount': row[5],
            'payment_method': row[6]
        } for row in sales]
    }), 200

@bp.route('/monthly/<year>/<month>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_monthly_sales(year, month):
    """Get monthly sales"""
    employee_id = request.args.get('employee_id')
    
    sales = Sales.get_monthly_sales(
        employee_id=int(employee_id) if employee_id else None,
        year=int(year),
        month=int(month)
    )
    
    return jsonify({
        'success': True,
        'sales': [{
            'sale_id': row[0],
            'employee_id': row[1],
            'sale_date': row[2],
            'category': row[3],
            'amount': row[5]
        } for row in sales]
    }), 200

@bp.route('/daily-summary/<date>', methods=['GET'])
@token_required
def get_daily_summary(date):
    """Get daily summary across all employees"""
    summary = Sales.get_all_daily_sales(date)
    
    return jsonify({
        'success': True,
        'summary': [{
            'user_id': row[0],
            'employee_name': row[1],
            'total_sales': row[2],
            'transactions': row[3]
        } for row in summary]
    }), 200

@bp.route('/employee-performance/<employee_id>', methods=['GET'])
@token_required
def get_employee_performance(employee_id):
    """Get employee's performance summary"""
    performance = Sales.get_employee_daily_performance(int(employee_id))
    
    return jsonify({
        'success': True,
        'performance': [{
            'summary_id': row[0],
            'employee_id': row[1],
            'sale_date': row[2],
            'total_sales': row[3],
            'room_sales': row[4],
            'food_sales': row[5],
            'beverage_sales': row[6],
            'service_sales': row[7],
            'transaction_count': row[8]
        } for row in performance]
    }), 200

@bp.route('/categories', methods=['GET'])
@token_required
def get_sale_categories():
    """Get available sale categories"""
    return jsonify({
        'success': True,
        'categories': ['Room', 'Food', 'Beverage', 'Services', 'Other']
    }), 200

@bp.route('/payment-methods', methods=['GET'])
@token_required
def get_payment_methods():
    """Get available payment methods"""
    return jsonify({
        'success': True,
        'methods': ['Cash', 'Card', 'Mobile', 'Check', 'Online']
    }), 200
