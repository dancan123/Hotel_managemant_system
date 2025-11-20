"""Room management routes"""
from flask import Blueprint, request, jsonify
from app.models.room import Room
from app.utils.auth import token_required, role_required
from app.utils.database import generate_occupancy_report

bp = Blueprint('rooms', __name__, url_prefix='/api/rooms')

@bp.route('/', methods=['GET'])
@token_required
def get_rooms():
    """Get all rooms"""
    rooms = Room.get_all_rooms()
    
    return jsonify({
        'success': True,
        'rooms': [{
            'room_id': row[0],
            'room_number': row[1],
            'room_type': row[2],
            'capacity': row[3],
            'price_per_night': row[4],
            'status': row[5]
        } for row in rooms]
    }), 200

@bp.route('/available', methods=['GET'])
@token_required
def get_available_rooms():
    """Get available rooms"""
    rooms = Room.get_available_rooms()
    
    return jsonify({
        'success': True,
        'rooms': [{
            'room_id': row[0],
            'room_number': row[1],
            'room_type': row[2],
            'capacity': row[3],
            'price_per_night': row[4]
        } for row in rooms]
    }), 200

@bp.route('/', methods=['POST'])
@token_required
@role_required('Admin')
def create_room():
    """Create new room (Admin only)"""
    data = request.get_json()
    
    required_fields = ['room_number', 'room_type', 'capacity', 'price_per_night']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    result = Room.create_room(
        room_number=data['room_number'],
        room_type=data['room_type'],
        capacity=int(data['capacity']),
        price_per_night=float(data['price_per_night'])
    )
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Room created successfully',
            'room_id': result['room_id']
        }), 201
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@bp.route('/<int:room_id>/check-in', methods=['POST'])
@token_required
def check_in_room(room_id):
    """Check in a guest"""
    data = request.get_json()
    
    required_fields = ['guest_name', 'check_in_date', 'check_out_date']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    result = Room.check_in(
        room_id=room_id,
        guest_name=data['guest_name'],
        employee_id=request.user['user_id'],
        check_in_date=data['check_in_date'],
        check_out_date=data['check_out_date'],
        guest_email=data.get('guest_email'),
        guest_phone=data.get('guest_phone'),
        number_of_guests=int(data.get('number_of_guests', 1)),
        notes=data.get('notes')
    )
    
    if result['success']:
        # Generate occupancy report
        generate_occupancy_report()
        
        return jsonify({
            'success': True,
            'message': 'Guest checked in successfully',
            'check_in_id': result['check_in_id']
        }), 201
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@bp.route('/<int:room_id>/check-out', methods=['POST'])
@token_required
def check_out_room(room_id):
    """Check out a guest"""
    data = request.get_json()
    
    if 'check_in_id' not in data:
        return jsonify({'success': False, 'error': 'Check-in ID required'}), 400
    
    result = Room.check_out(room_id, data['check_in_id'])
    
    if result['success']:
        # Generate occupancy report
        generate_occupancy_report()
        
        return jsonify({
            'success': True,
            'message': 'Guest checked out successfully'
        }), 200
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@bp.route('/active-check-ins', methods=['GET'])
@token_required
def get_active_check_ins():
    """Get all active check-ins"""
    check_ins = Room.get_active_check_ins()
    
    return jsonify({
        'success': True,
        'check_ins': [{
            'check_in_id': row[0],
            'room_id': row[1],
            'guest_name': row[2],
            'guest_email': row[3],
            'guest_phone': row[4],
            'check_in_date': row[5],
            'check_out_date': row[6],
            'number_of_guests': row[7],
            'room_number': row[10],
            'employee_name': row[11]
        } for row in check_ins]
    }), 200

@bp.route('/occupancy-report', methods=['GET'])
@token_required
@role_required('Manager', 'Admin')
def get_occupancy_report():
    """Get occupancy report"""
    generate_occupancy_report()
    
    report = Room.get_occupancy_report()
    
    if report:
        return jsonify({
            'success': True,
            'occupancy': {
                'occupancy_id': report[0],
                'report_date': report[1],
                'total_rooms': report[2],
                'occupied_rooms': report[3],
                'available_rooms': report[4],
                'maintenance_rooms': report[5],
                'occupancy_rate': report[6]
            }
        }), 200
    else:
        return jsonify({'success': True, 'occupancy': None}), 200
