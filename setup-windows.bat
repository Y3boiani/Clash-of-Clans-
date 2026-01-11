@echo off
REM ========================================
REM CoC ML Research Platform - Windows Setup
REM ========================================

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

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python and Node.js found
echo.

REM Setup Backend
echo [1/4] Setting up Backend...
cd backend
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

if not exist ".env" (
    echo Creating .env file...
    echo COC_API_KEY=your_api_key_here > .env
    echo MONGO_URL=mongodb://localhost:27017 >> .env
    echo DB_NAME=coc_ml_research >> .env
    echo CORS_ORIGINS=* >> .env
    echo.
    echo [IMPORTANT] Please edit backend\.env and add your CoC API key!
)

cd ..
echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo [2/4] Setting up Frontend...
cd frontend

echo Installing Node.js dependencies...
npm install

if not exist ".env" (
    echo Creating .env file...
    echo NEXT_PUBLIC_BACKEND_URL=http://localhost:8001 > .env
)

cd ..
echo [OK] Frontend setup complete
echo.

REM Check MongoDB
echo [3/4] Checking MongoDB...
echo Please ensure MongoDB is running on localhost:27017
echo You can download MongoDB from https://www.mongodb.com/try/download/community
echo.

REM Final Instructions
echo [4/4] Setup Complete!
echo.
echo ========================================
echo  HOW TO RUN THE APPLICATION
echo ========================================
echo.
echo 1. Start MongoDB (if not running)
echo.
echo 2. Start the Backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn server:app --host 0.0.0.0 --port 8001 --reload
echo.
echo 3. Start the Frontend (in another terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:3000 in your browser
echo.
echo ========================================
echo  IMPORTANT: CoC API Key Setup
echo ========================================
echo.
echo To use player search, you need a CoC API key:
echo 1. Go to https://developer.clashofclans.com
echo 2. Create/edit your API key
echo 3. Add your local IP to allowed IPs
echo 4. Put the key in backend\.env
echo.
pause
