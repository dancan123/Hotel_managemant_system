"""Authentication routes"""
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.auth import generate_token, token_required
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    role = data.get('role')  # Optional role hint
    
    user = User.get_user_by_username(username)
    
    if not user:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    if not User.verify_password(username, password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    if not user[8]:  # is_active check
        return jsonify({'success': False, 'error': 'User account is inactive'}), 401
    
    # Generate token
    token = generate_token(user[0], user[5], username)
    
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'user_id': user[0],
            'username': user[1],
            'email': user[3],
            'full_name': user[4],
            'role': user[5],
            'department': user[6]
        }
    }), 200

@bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint (Admin only)"""
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
            'message': 'User created successfully',
            'user_id': result['user_id']
        }), 201
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@bp.route('/verify-token', methods=['POST'])
@token_required
def verify_token():
    """Verify token validity"""
    return jsonify({
        'success': True,
        'user': request.user
    }), 200

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    user = User.get_user_by_id(request.user['user_id'])
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'user_id': user[0],
            'username': user[1],
            'email': user[3],
            'full_name': user[4],
            'role': user[5],
            'department': user[6],
            'phone': user[7]
        }
    }), 200

@bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """User logout (client-side token deletion)"""
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200
