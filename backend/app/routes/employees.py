"""Employee management routes"""
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.auth import token_required, role_required

bp = Blueprint('employees', __name__, url_prefix='/api/employees')

@bp.route('/', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_employees():
    """Get all employees"""
    role = request.args.get('role')
    users = User.get_all_users(role)
    
    return jsonify({
        'success': True,
        'employees': [{
            'user_id': row[0],
            'username': row[1],
            'email': row[3],
            'full_name': row[4],
            'role': row[5],
            'department': row[6],
            'phone': row[7],
            'is_active': row[8]
        } for row in users]
    }), 200

@bp.route('/<int:employee_id>', methods=['GET'])
@token_required
def get_employee(employee_id):
    """Get employee details"""
    # Users can only view their own profile or managers/admins can view all
    if request.user['role'] not in ['Manager', 'Admin'] and request.user['user_id'] != employee_id:
        return jsonify({'success': False, 'error': 'Insufficient permissions'}), 403
    
    user = User.get_user_by_id(employee_id)
    
    if not user:
        return jsonify({'success': False, 'error': 'Employee not found'}), 404
    
    return jsonify({
        'success': True,
        'employee': {
            'user_id': user[0],
            'username': user[1],
            'email': user[3],
            'full_name': user[4],
            'role': user[5],
            'department': user[6],
            'phone': user[7],
            'is_active': user[8]
        }
    }), 200

@bp.route('/', methods=['POST'])
@token_required
@role_required('Admin')
def create_employee():
    """Create new employee (Admin only)"""
    data = request.get_json()
    
    required_fields = ['username', 'password', 'email', 'full_name', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    result = User.create_user(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        full_name=data['full_name'],
        role=data['role'],
        department=data.get('department'),
        phone=data.get('phone')
    )
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Employee created successfully',
            'user_id': result['user_id']
        }), 201
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@bp.route('/<int:employee_id>', methods=['PUT'])
@token_required
@role_required('Admin', 'Manager')
def update_employee(employee_id):
    """Update employee details"""
    data = request.get_json()
    
    result = User.update_user(employee_id, **data)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Employee updated successfully'
        }), 200
    else:
        return jsonify({'success': False, 'error': result.get('error')}), 400

@bp.route('/<int:employee_id>/deactivate', methods=['PUT'])
@token_required
@role_required('Admin')
def deactivate_employee(employee_id):
    """Deactivate employee"""
    result = User.deactivate_user(employee_id)
    
    return jsonify({
        'success': True,
        'message': 'Employee deactivated successfully'
    }), 200

@bp.route('/by-department/<department>', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_employees_by_department(department):
    """Get employees by department"""
    users = User.get_all_users()
    
    filtered = [row for row in users if row[6] == department]
    
    return jsonify({
        'success': True,
        'employees': [{
            'user_id': row[0],
            'username': row[1],
            'full_name': row[4],
            'department': row[6]
        } for row in filtered]
    }), 200
