#!/usr/bin/env python3
"""
Run script for Dustbin
Uses gunicorn to run the application
"""
import os
from app import app

# Check db exists
if not os.path.exists('dustbin.db'):
    print("Database not found!")
    print("Creating database...")
    os.system('python create_db.py')
    print("Database created!")

if __name__ == '__main__':
    app.run(debug=True)
