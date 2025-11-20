"""
Hotel Management System - Backend Application
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.utils.database import init_db
import os

def create_app(config_name='development'):
    """Application factory for creating Flask app instance"""
    # Get the absolute path to frontend directory
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))
    app = Flask(__name__, static_folder=frontend_path, static_url_path='')
    
    # Configuration
    if config_name == 'production':
        app.config['DEBUG'] = False
    else:
        app.config['DEBUG'] = True
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.routes import auth, sales, employees, rooms, reports, dashboard
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(sales.bp)
    app.register_blueprint(employees.bp)
    app.register_blueprint(rooms.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(dashboard.bp)
    
    # Serve frontend files
    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_path, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.isfile(os.path.join(frontend_path, path)):
            return send_from_directory(frontend_path, path)
        return send_from_directory(frontend_path, 'index.html')
    
    return app
