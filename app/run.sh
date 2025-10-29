#!/bin/bash

# Run script for Wisconsin Excise Tax XML Generator (Mac/Linux)

echo "================================================"
echo "Wisconsin Excise Tax XML Generator"
echo "Starting application..."
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the application
echo "Starting Flask application..."
python3 app.py

# Deactivate virtual environment on exit
deactivate

