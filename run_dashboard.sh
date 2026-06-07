#!/bin/bash
# CHAI 2.0 Dashboard - Startup Script for Mac/Linux
# This script starts both the Flask API and Streamlit Dashboard

echo ""
echo "==========================================="
echo "  CHAI 2.0 - Startup Script"
echo "  Cognitive Hazard AI Dashboard"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check if pip packages are installed
echo "[*] Checking dependencies..."
python3 -m pip list | grep -q streamlit
if [ $? -ne 0 ]; then
    echo "[*] Installing required packages..."
    python3 -m pip install -r requirements.txt
fi

echo ""
echo "[*] Starting CHAI 2.0 Dashboard System..."
echo ""

# Start API in background
echo "[*] Starting API Server (Port 5000)..."
python3 api.py &
API_PID=$!

# Wait for API to start
sleep 3

# Start Dashboard
echo "[*] Starting Dashboard (Port 8501)..."
echo ""
echo "==========================================="
echo "  Dashboard will open in your browser"
echo "  If not, visit: http://localhost:8501"
echo ""
echo "  API: http://localhost:5000"
echo "  Docs: Read QUICKSTART.md or SETUP_GUIDE.md"
echo ""
echo "  Press Ctrl+C to stop"
echo "==========================================="
echo ""

streamlit run dashboard.py

# Cleanup on exit
trap "kill $API_PID 2>/dev/null" EXIT
