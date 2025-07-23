@echo off
echo Product Data AI Agent - Web Interface
echo =====================================

echo.
echo [INFO] Starting Web Interface...
echo [INFO] The web interface will be available at: http://localhost:8501
echo [INFO] Make sure the API server is running first!
echo [INFO] Press Ctrl+C to stop the interface
echo.

streamlit run web_interface.py

pause 