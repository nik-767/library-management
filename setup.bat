@echo off
echo ============================================
echo   Library Management System - Setup Script
echo ============================================
echo.

echo [1/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (echo ERROR: pip install failed & pause & exit /b 1)

echo.
echo [2/5] Running database migrations...
python manage.py makemigrations library
python manage.py migrate
if errorlevel 1 (echo ERROR: migration failed & pause & exit /b 1)

echo.
echo [3/5] Seeding fake data (60+ books, students)...
python seed_data.py
if errorlevel 1 (echo ERROR: seed failed & pause & exit /b 1)

echo.
echo [4/5] Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo   Admin Login:  admin / admin123
echo   Start server: python manage.py runserver
echo   Open browser: http://127.0.0.1:8000
echo ============================================
echo.
pause
