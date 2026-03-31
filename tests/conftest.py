import sys
import os

# Add the project root directory to the path so pytest can find pawpal_system.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
