"""Room model for room management and check-in/check-out operations"""
import sqlite3
from app.utils.database import get_db

class Room:
    """Room model for database operations"""
    
    @staticmethod
    def create_room(room_number, room_type, capacity, price_per_night):
        """Create a new room"""
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO rooms (room_number, room_type, capacity, price_per_night)
                VALUES (?, ?, ?, ?)
            ''', (room_number, room_type, capacity, price_per_night))
            db.commit()
            return {'success': True, 'room_id': cursor.lastrowid}
        except sqlite3.IntegrityError:
            return {'success': False, 'error': 'Room number already exists'}
    
    @staticmethod
    def get_all_rooms():
        """Get all rooms"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM rooms ORDER BY room_number')
        return cursor.fetchall()
    
    @staticmethod
    def get_room_by_id(room_id):
        """Get room by ID"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id,))
        return cursor.fetchone()
    
    @staticmethod
    def get_available_rooms():
        """Get all available rooms"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM rooms WHERE status = "Available" ORDER BY room_number')
        return cursor.fetchall()
    
    @staticmethod
    def update_room_status(room_id, status):
        """Update room status"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE rooms SET status = ? WHERE room_id = ?', (status, room_id))
        db.commit()
        return {'success': True}
    
    @staticmethod
    def check_in(room_id, guest_name, employee_id, check_in_date, check_out_date, 
                 guest_email=None, guest_phone=None, number_of_guests=1, notes=None):
        """Record a check-in"""
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO check_ins 
                (room_id, guest_name, guest_email, guest_phone, check_in_date, check_out_date, 
                 number_of_guests, check_in_employee_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (room_id, guest_name, guest_email, guest_phone, check_in_date, 
                  check_out_date, number_of_guests, employee_id, notes))
            
            # Update room status to Occupied
            Room.update_room_status(room_id, 'Occupied')
            db.commit()
            
            return {'success': True, 'check_in_id': cursor.lastrowid}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def check_out(room_id, check_in_id):
        """Record a check-out"""
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute('''
                UPDATE check_ins 
                SET status = "Completed" 
                WHERE check_in_id = ?
            ''', (check_in_id,))
            
            # Update room status to Available
            Room.update_room_status(room_id, 'Available')
            db.commit()
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_active_check_ins():
        """Get all active check-ins"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT c.*, r.room_number, u.full_name as employee_name
            FROM check_ins c
            JOIN rooms r ON c.room_id = r.room_id
            JOIN users u ON c.check_in_employee_id = u.user_id
            WHERE c.status = "Active"
            ORDER BY c.check_in_date
        ''')
        return cursor.fetchall()
    
    @staticmethod
    def get_occupancy_report(report_date=None):
        """Get occupancy report for a date"""
        db = get_db()
        cursor = db.cursor()
        
        if report_date:
            cursor.execute('''
                SELECT * FROM occupancy_report WHERE report_date = ?
            ''', (report_date,))
        else:
            cursor.execute('''
                SELECT * FROM occupancy_report 
                ORDER BY report_date DESC 
                LIMIT 1
            ''')
        
        return cursor.fetchone()
