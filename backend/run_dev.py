#!/usr/bin/env python
"""Wrapper script to run Uvicorn from the backend directory."""

import os
import sys
import subprocess

# Change to backend directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run uvicorn
sys.exit(subprocess.call([
    sys.executable, '-m', 'uvicorn',
    'app.main:app',
    '--host', '127.0.0.1',
    '--port', '8000',
    '--reload'
]))
