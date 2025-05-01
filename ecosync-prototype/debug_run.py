"""
Debug Runner for EcoSync Prototype
This script runs the EcoSync application with unbuffered output to ensure
that print statements immediately appear in the terminal.
"""
import os
import sys

# Set environment variable to ensure Python doesn't buffer stdout
os.environ['PYTHONUNBUFFERED'] = '1'

# Import and run the Flask application
from app import app

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 STARTING ECOSYNC IN DEBUG MODE WITH UNBUFFERED OUTPUT")
    print("="*80)
    print("📝 All agent interactions will be logged to this terminal")
    print("="*80 + "\n")
    
    # Run with debug mode and without output buffering
    app.run(debug=True, use_reloader=False)