import os
import sys

# Ensure root directory is in sys.path so 'backend' module can be imported properly by Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.main import app
