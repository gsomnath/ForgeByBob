@echo off
echo Starting Blog Writer Microservices...
echo.

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Services will start on the following ports:
echo - API Gateway: http://localhost:8000
echo - Blog Service: http://localhost:8001  
echo - Settings Service: http://localhost:8002
echo - UI Service: http://localhost:8003
echo.

echo Starting services...
echo Press Ctrl+C to stop all services
echo.

start "API Gateway" cmd /k "call venv\Scripts\activate.bat & python -m services.api_gateway.main"
timeout /t 2 /nobreak >nul

start "Blog Service" cmd /k "call venv\Scripts\activate.bat & python -m services.blog_service.main"
timeout /t 2 /nobreak >nul

start "Settings Service" cmd /k "call venv\Scripts\activate.bat & python -m services.settings_service.main"
timeout /t 2 /nobreak >nul

start "UI Service" cmd /k "call venv\Scripts\activate.bat & python -m services.ui_service.main"

echo All services started!
echo Open http://localhost:8003 in your browser to access the application.
pause
