@echo off
echo ======================================================================
echo  Starting CarePulse Hospital Management System (Django 5.x + SQLite)
echo ======================================================================
echo.
echo Open your web browser and visit:
echo   http://127.0.0.1:8000/
echo.
echo Demo Accounts:
echo   - Patient Account:  patient / patient123
echo   - Admin Panel:      admin / admin123
echo.
echo Press Ctrl+C in this terminal window to stop the server anytime.
echo ======================================================================
echo.

py manage.py runserver 0.0.0.0:8000 2>nul || python manage.py runserver 0.0.0.0:8000
pause
