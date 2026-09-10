@echo off
REM Start FastAPI backend from the backend directory
cd /d "%~dp0"
"%~dp0venv\Scripts\uvicorn" app.main:app --host 0.0.0.0 --port 8000
