"""
Vercel serverless function entry point for Flask app
This file is required for Vercel to recognize and deploy the Flask application.
"""
import os
import sys

# Add parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set Vercel environment variable
os.environ['VERCEL'] = '1'

# Import Flask app
from app import app

# Vercel expects the app to be accessible
# The @vercel/python builder will automatically wrap this
__all__ = ['app']
