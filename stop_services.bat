@echo off
echo ========================================
echo Force Stopping All Services
echo ========================================
echo.

echo Stopping all Python processes...
taskkill /F /IM python.exe /T 2>nul

echo.
echo Stopping specific service windows...
taskkill /F /FI "WindowTitle eq API Gateway*" 2>nul
taskkill /F /FI "WindowTitle eq Blog Service*" 2>nul
taskkill /F /FI "WindowTitle eq Settings Service*" 2>nul
taskkill /F /FI "WindowTitle eq UI Service*" 2>nul

echo.
echo Stopping any remaining cmd windows running services...
taskkill /F /FI "WindowTitle eq *Gateway*" /FI "IMAGENAME eq cmd.exe" 2>nul
taskkill /F /FI "WindowTitle eq *Service*" /FI "IMAGENAME eq cmd.exe" 2>nul

echo.
echo Waiting for processes to terminate...
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All services have been stopped!
echo ========================================
echo.

pause

@REM Made with Bob
