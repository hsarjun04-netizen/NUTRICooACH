import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get('PORT', 5000))
    serve(app, host='0.0.0.0', port=port)
