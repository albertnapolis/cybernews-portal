#!/usr/bin/env python
"""
Simple script to run the FastAPI application without reload
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app
import uvicorn

if __name__ == "__main__":
    # Run without reload to avoid import issues
    uvicorn.run(app, host="127.0.0.1", port=8001)