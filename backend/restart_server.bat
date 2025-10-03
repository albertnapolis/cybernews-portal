@echo off
echo Restarting Cybersecurity News Portal Backend...

REM Kill any existing process on port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Stopping existing server (PID: %%a)
    taskkill //F //PID %%a >nul 2>&1
)

echo Starting fresh server...
python simple_run.py