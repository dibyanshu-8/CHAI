@echo off
REM CHAI 2.0 Dashboard - Startup Script
REM This script starts both the Flask API and Streamlit Dashboard

echo.
echo ==========================================
echo   CHAI 2.0 - Startup Script
echo   Cognitive Hazard AI Dashboard
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if requirements are installed
echo [*] Checking dependencies...
pip list | findstr "streamlit flask plotly" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements
        pause
        exit /b 1
    )
)

echo.
echo [*] Starting CHAI 2.0 Dashboard System...
echo.

REM Start API in a new window
echo [*] Starting API Server (Port 5000)...
start /T "CHAI API Server" python api.py

REM Wait for API to start
timeout /t 3 /nobreak

REM Start Dashboard
echo [*] Starting Dashboard (Port 8501)...
echo.
echo ==========================================
echo   Dashboard will open in your browser
echo   If not, visit: http://localhost:8501
echo.
echo   API: http://localhost:5000
echo   Docs: Open DASHBOARD_README.md
echo.
echo   Press Ctrl+C in console windows to stop
echo ==========================================
echo.

streamlit run dashboard.py

pause
