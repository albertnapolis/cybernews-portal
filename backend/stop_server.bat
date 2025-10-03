@echo off
echo Stopping Cybersecurity News Portal Backend...

REM Find and kill process using port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing process %%a
    taskkill //F //PID %%a >nul 2>&1
)

echo Server stopped.
pause