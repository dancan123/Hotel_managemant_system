"""Database connection and initialization utilities"""
import sqlite3
import os
from flask import g

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../database/hotel_management.db')

def get_db():
    """Get database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    """Close database connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    """Initialize database with schema"""
    app.teardown_appcontext(close_db)
    
    # Create database if it doesn't exist
    if not os.path.exists(DATABASE_PATH):
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        # Read and execute schema
        schema_path = os.path.join(os.path.dirname(__file__), '../../database/schema.sql')
        if os.path.exists(schema_path):
            db = sqlite3.connect(DATABASE_PATH)
            with open(schema_path, 'r') as f:
                db.executescript(f.read())
            db.commit()
            db.close()
            
            # Create sample data
            _create_sample_data()

def _create_sample_data():
    """Create sample data for testing"""
    from app.models.user import User
    
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()
    
    # Check if admin already exists
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Create admin user
        User.create_user('admin', 'admin123', 'admin@hotel.com', 'Administrator', 'Admin')
        # Create manager user
        User.create_user('manager1', 'manager123', 'manager1@hotel.com', 'John Manager', 'Manager', 'Management')
        # Create employees
        User.create_user('waiter1', 'waiter123', 'waiter1@hotel.com', 'James Smith', 'Employee', 'Dining')
        User.create_user('waiter2', 'waiter123', 'waiter2@hotel.com', 'Sarah Johnson', 'Employee', 'Dining')
        User.create_user('receptionist1', 'recept123', 'recept1@hotel.com', 'Emma Davis', 'Employee', 'Front Desk')
        
        # Create sample rooms
        rooms = [
            ('101', 'Single', 1, 50.00),
            ('102', 'Double', 2, 75.00),
            ('201', 'Suite', 4, 150.00),
            ('202', 'Deluxe', 2, 100.00),
            ('301', 'Single', 1, 50.00),
            ('302', 'Double', 2, 75.00),
        ]
        
        for room_num, room_type, capacity, price in rooms:
            cursor.execute('''
                INSERT INTO rooms (room_number, room_type, capacity, price_per_night)
                VALUES (?, ?, ?, ?)
            ''', (room_num, room_type, capacity, price))
        
        db.commit()
    
    db.close()

def generate_occupancy_report():
    """Generate occupancy report"""
    from datetime import datetime
    
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()
    
    # Count rooms by status
    cursor.execute('SELECT COUNT(*) FROM rooms')
    total_rooms = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM rooms WHERE status = "Occupied"')
    occupied_rooms = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM rooms WHERE status = "Maintenance"')
    maintenance_rooms = cursor.fetchone()[0]
    
    available_rooms = total_rooms - occupied_rooms - maintenance_rooms
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Insert or update report
    today = datetime.now().date()
    cursor.execute('''
        INSERT INTO occupancy_report 
        (report_date, total_rooms, occupied_rooms, available_rooms, maintenance_rooms, occupancy_rate)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(report_date) DO UPDATE SET
            occupied_rooms = ?, available_rooms = ?, maintenance_rooms = ?, occupancy_rate = ?
    ''', (today, total_rooms, occupied_rooms, available_rooms, maintenance_rooms, occupancy_rate,
          occupied_rooms, available_rooms, maintenance_rooms, occupancy_rate))
    
    db.commit()
    db.close()
