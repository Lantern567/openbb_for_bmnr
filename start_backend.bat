@echo off
REM BMNR Stock Analysis Backend Startup Script
REM This script starts the backend server with API keys configured

echo ============================================================
echo BMNR Stock Analysis Backend
echo ============================================================
echo.

REM Activate conda environment
echo [1/3] Activating conda environment...
call conda activate bmnr_analysis
if errorlevel 1 (
    echo [ERROR] Failed to activate conda environment
    echo Please make sure conda is installed and bmnr_analysis environment exists
    pause
    exit /b 1
)
echo [OK] Environment activated
echo.

REM Navigate to backend directory
echo [2/3] Changing to backend directory...
cd /d "%~dp0backend"
if errorlevel 1 (
    echo [ERROR] Failed to change directory
    pause
    exit /b 1
)
echo [OK] Directory: %CD%
echo.

REM Start backend server
echo [3/3] Starting FastAPI backend server...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ============================================================
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM If server stops, pause to show any error messages
pause
