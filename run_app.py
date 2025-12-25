"""
Quick start script to run the web application
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed."""
    required = ['flask', 'flask_cors', 'spacy', 'sklearn', 'PyPDF2', 'docx']
    missing = []
    
    for package in required:
        try:
            if package == 'flask_cors':
                __import__('flask_cors')
            elif package == 'sklearn':
                __import__('sklearn')
            elif package == 'docx':
                __import__('docx')
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install them with:")
        print("   pip install -r requirements.txt")
        print("\n📚 Also download spaCy model:")
        print("   python -m spacy download en_core_web_sm")
        return False
    
    return True

def main():
    print("=" * 60)
    print("🚀 Starting AI Resume Matcher Web Application")
    print("=" * 60)
    print()
    
    if not check_dependencies():
        sys.exit(1)
    
    # Check spaCy model
    try:
        import spacy
        spacy.load("en_core_web_sm")
    except OSError:
        print("⚠️  Warning: spaCy English model not found.")
        print("   Download it with: python -m spacy download en_core_web_sm")
        print("   The app will work with basic parsing, but NLP features will be limited.")
        print()
    
    # Create uploads directory
    os.makedirs('uploads', exist_ok=True)
    
    print("✅ All checks passed!")
    print()
    print("🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    print("=" * 60)
    print()
    
    # Import and run app
    from app import app
    
    # Get port from environment variable (Render provides this) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Disable debug mode in production (Render sets environment)
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()

