@echo off
REM Clean up all backend processes on port 8000
REM Run this as Administrator

echo Stopping all processes on port 8000...

taskkill /F /PID 84912
taskkill /F /PID 31032
taskkill /F /PID 61808

echo.
echo All backend processes stopped.
echo.
echo Now you can start a fresh backend instance using start_backend_with_keys.bat
pause
