import os
import sys

# Configure UTF-8 encoding on Windows consoles
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure current working directory and sys.path are always set to the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print("RAITASAATHIAI -- AGRICULTURAL INTELLIGENCE PLATFORM")
    print("   'Understand Every Farmer. Empower Every Field.'")
    print(f"   URL: http://127.0.0.1:{port}")
    print("   Demo Login: demo_farmer / kisan2026")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=True)



