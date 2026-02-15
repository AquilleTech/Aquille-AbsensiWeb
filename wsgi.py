"""
WSGI entry point for production deployment
"""
import os
import sys

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application

# Ensure data files exist
from app import (
    DATA_FILE, ATTENDANCE_FILE, USERS_FILE, 
    LEAVES_FILE, SETTINGS_FILE, DEFAULT_SETTINGS
)
import json

def init_data_files():
    """Initialize data files if they don't exist"""
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"students": []}, f, indent=4)
    
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
    
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"users": []}, f, indent=4)
    
    if not os.path.exists(LEAVES_FILE):
        with open(LEAVES_FILE, 'w', encoding='utf-8') as f:
            json.dump({"leaves": []}, f, indent=4)
    
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)

# Initialize on startup
init_data_files()

if __name__ == "__main__":
    application.run()
