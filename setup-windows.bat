@echo off
REM ========================================
REM CoC ML Research Platform - Windows Setup
REM ========================================
REM This script sets up the entire project for local development
REM Prerequisites: Python 3.10+, Node.js 18+, MongoDB

echo.
echo ========================================
echo  CoC ML Research Platform Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM Setup Backend
echo [1/4] Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env >nul
    echo.
    echo [ACTION REQUIRED] Edit backend\.env and add your CoC API key!
    echo Get your key from: https://developer.clashofclans.com
)

cd ..
echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo [2/4] Setting up Frontend...
cd frontend

if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env >nul
)

echo Installing Node.js dependencies (this may take a minute)...
npm install --silent

cd ..
echo [OK] Frontend setup complete
echo.

REM MongoDB check
echo [3/4] Checking MongoDB...
echo Please ensure MongoDB is running on localhost:27017
echo Download MongoDB: https://www.mongodb.com/try/download/community
echo.

REM Final Instructions
echo [4/4] Setup Complete!
echo.
echo ========================================
echo  HOW TO RUN THE APPLICATION
echo ========================================
echo.
echo TERMINAL 1 - Start Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
echo.
echo TERMINAL 2 - Start Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
echo ========================================
echo  IMPORTANT: CoC API Key Setup
echo ========================================
echo.
echo 1. Go to https://developer.clashofclans.com
echo 2. Create or edit an API key
echo 3. Add your local IP (find it at https://whatismyip.com)
echo 4. Put the key in backend\.env (COC_API_KEY=your_key)
echo.
pause
