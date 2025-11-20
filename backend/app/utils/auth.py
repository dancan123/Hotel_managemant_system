"""Authentication utilities and JWT token handling"""
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
TOKEN_EXPIRY = 86400  # 24 hours

def generate_token(user_id, role, username):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'role': role,
        'username': username,
        'exp': datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRY),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'success': False, 'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401
        
        request.user = payload
        return f(*args, **kwargs)
    
    return decorated

def role_required(*required_roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({'success': False, 'error': 'User not authenticated'}), 401
            
            if request.user.get('role') not in required_roles:
                return jsonify({'success': False, 'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator
