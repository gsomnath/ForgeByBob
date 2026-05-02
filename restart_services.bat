@echo off
echo Stopping all Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 3 /nobreak >nul

echo Starting services...
python start_all_services.py

@REM Made with Bob
