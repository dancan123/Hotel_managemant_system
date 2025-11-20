"""Reports generation routes"""
from flask import Blueprint, request, jsonify, send_file
from app.models.sales import Sales
from app.utils.auth import token_required, role_required
from app.utils.export import export_to_excel, export_to_pdf
from datetime import datetime, timedelta
import os

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp.route('/daily/<date>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_daily_report(date):
    """Get daily sales report"""
    sales = Sales.get_all_daily_sales(date)
    
    total_sales = sum(row[2] for row in sales)
    total_transactions = sum(row[3] for row in sales)
    
    return jsonify({
        'success': True,
        'report': {
            'date': date,
            'total_sales': total_sales,
            'total_transactions': total_transactions,
            'employees': [{
                'user_id': row[0],
                'employee_name': row[1],
                'total_sales': row[2],
                'transactions': row[3]
            } for row in sales]
        }
    }), 200

@bp.route('/monthly/<year>/<month>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_monthly_report(year, month):
    """Get monthly sales report"""
    sales = Sales.get_all_daily_sales.__doc__  # This is a placeholder for proper monthly aggregation
    
    # Aggregate monthly data
    summary = Sales.get_monthly_summary(int(year), int(month))
    
    total_sales = 0
    total_transactions = 0
    
    if summary:
        total_sales = sum(row[4] for row in summary if row[4])
        total_transactions = sum(row[8] for row in summary if row[8])
    
    return jsonify({
        'success': True,
        'report': {
            'year': year,
            'month': month,
            'total_sales': total_sales,
            'total_transactions': total_transactions
        }
    }), 200

@bp.route('/yearly/<year>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_yearly_report(year):
    """Get yearly sales report"""
    yearly_total = 0
    yearly_data = []
    
    for month in range(1, 13):
        summary = Sales.get_monthly_summary(int(year), month)
        month_total = sum(row[4] for row in summary if row[4]) if summary else 0
        yearly_total += month_total
        yearly_data.append({
            'month': month,
            'total': month_total
        })
    
    return jsonify({
        'success': True,
        'report': {
            'year': year,
            'total_sales': yearly_total,
            'monthly_breakdown': yearly_data
        }
    }), 200

@bp.route('/employee-performance/<employee_id>/<period>', methods=['GET'])
@token_required
def get_employee_report(employee_id, period):
    """Get employee performance report"""
    performance = Sales.get_employee_daily_performance(int(employee_id))
    
    total_sales = sum(row[3] for row in performance if row[3])
    avg_daily_sales = total_sales / len(performance) if performance else 0
    
    return jsonify({
        'success': True,
        'report': {
            'employee_id': employee_id,
            'period': period,
            'total_sales': total_sales,
            'avg_daily_sales': avg_daily_sales,
            'daily_performance': [{
                'date': row[2],
                'total_sales': row[3],
                'room_sales': row[4],
                'food_sales': row[5],
                'beverage_sales': row[6],
                'service_sales': row[7],
                'transactions': row[8]
            } for row in performance]
        }
    }), 200

@bp.route('/export/daily/<date>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def export_daily_report(date):
    """Export daily report to Excel or PDF"""
    export_format = request.args.get('format', 'excel')
    
    sales = Sales.get_all_daily_sales(date)
    
    data = [{
        'Employee': row[1],
        'Total Sales': row[2],
        'Transactions': row[3]
    } for row in sales]
    
    filename = f"daily_report_{date}_.{'xlsx' if export_format == 'excel' else 'pdf'}"
    filepath = os.path.join('/tmp', filename)
    
    if export_format == 'excel':
        result_file, status = export_to_excel(data, filepath, f"Daily Sales Report - {date}")
    else:
        result_file, status = export_to_pdf(data, filepath, f"Daily Sales Report - {date}")
    
    if result_file:
        return send_file(result_file, as_attachment=True, download_name=filename)
    else:
        return jsonify({'success': False, 'error': status}), 500

@bp.route('/export/monthly/<year>/<month>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def export_monthly_report(year, month):
    """Export monthly report to Excel or PDF"""
    export_format = request.args.get('format', 'excel')
    
    summary = Sales.get_monthly_summary(int(year), int(month))
    
    data = [{
        'Employee': row[2] if row[2] else 'N/A',
        'Total Sales': row[4],
        'Room Sales': row[5],
        'Food Sales': row[6],
        'Beverage Sales': row[7],
        'Service Sales': row[8]
    } for row in summary] if summary else []
    
    filename = f"monthly_report_{year}_{month:02d}_.{'xlsx' if export_format == 'excel' else 'pdf'}"
    filepath = os.path.join('/tmp', filename)
    
    if export_format == 'excel':
        result_file, status = export_to_excel(data, filepath, f"Monthly Sales Report - {year}-{month:02d}")
    else:
        result_file, status = export_to_pdf(data, filepath, f"Monthly Sales Report - {year}-{month:02d}")
    
    if result_file:
        return send_file(result_file, as_attachment=True, download_name=filename)
    else:
        return jsonify({'success': False, 'error': status}), 500
