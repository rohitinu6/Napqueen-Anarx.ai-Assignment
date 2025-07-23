@echo off
echo Product Data AI Agent - Startup Script
echo ======================================

echo.
echo [INFO] Starting API Server...
echo [INFO] The API will be available at: http://localhost:8000
echo [INFO] Press Ctrl+C to stop the server
echo.

python api_server.py

pause 