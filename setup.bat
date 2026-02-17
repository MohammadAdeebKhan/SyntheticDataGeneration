@echo off
REM Setup script for Data Generation Platform

echo.
echo ========================================
echo Data Generation Platform Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "env\" (
    echo Creating virtual environment...
    python -m venv env
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call env\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Checking for .env file...
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created. Please edit it with your credentials.
) else (
    echo .env file already exists.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your database credentials
echo 2. Run: streamlit run streamlit_app.py
echo 3. Open: http://localhost:8501
echo.
pause
