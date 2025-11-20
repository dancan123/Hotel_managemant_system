"""
Main entry point for Hotel Management System Backend
Run this file to start the Flask application
"""
import os
import sys
from app import create_app

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

app = create_app('development')

if __name__ == '__main__':
    # Run the Flask application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
