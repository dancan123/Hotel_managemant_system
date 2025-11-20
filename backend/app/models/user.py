"""User model for authentication and user management"""
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.database import get_db

class User:
    """User model for database operations"""
    
    @staticmethod
    def create_user(username, password, email, full_name, role, department=None, phone=None):
        """Create a new user in the database"""
        db = get_db()
        hashed_password = generate_password_hash(password)
        
        try:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, email, full_name, role, department, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, email, full_name, role, department, phone))
            db.commit()
            return {'success': True, 'user_id': cursor.lastrowid}
        except sqlite3.IntegrityError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_user_by_username(username):
        """Retrieve user by username"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve user by ID"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        return user
    
    @staticmethod
    def verify_password(username, password):
        """Verify user password"""
        user = User.get_user_by_username(username)
        if user:
            # user[2] is the password column (hashed)
            return check_password_hash(user[2], password)
        return False
    
    @staticmethod
    def get_all_users(role=None):
        """Get all users, optionally filtered by role"""
        db = get_db()
        cursor = db.cursor()
        if role:
            cursor.execute('SELECT * FROM users WHERE role = ? AND is_active = 1', (role,))
        else:
            cursor.execute('SELECT * FROM users WHERE is_active = 1')
        return cursor.fetchall()
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user information"""
        db = get_db()
        cursor = db.cursor()
        
        allowed_fields = {'email', 'full_name', 'department', 'phone', 'is_active'}
        fields_to_update = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not fields_to_update:
            return {'success': False, 'error': 'No valid fields to update'}
        
        set_clause = ', '.join([f'{key} = ?' for key in fields_to_update.keys()])
        values = list(fields_to_update.values()) + [user_id]
        
        try:
            cursor.execute(f'UPDATE users SET {set_clause} WHERE user_id = ?', values)
            db.commit()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate a user"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE users SET is_active = 0 WHERE user_id = ?', (user_id,))
        db.commit()
        return {'success': True}
