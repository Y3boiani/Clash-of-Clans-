#!/bin/bash
# ========================================
# CoC ML Research Platform - Linux/Mac Setup
# ========================================
# This script sets up the entire project for local development
# Prerequisites: Python 3.10+, Node.js 18+, MongoDB

set -e

echo ""
echo "========================================"
echo " CoC ML Research Platform Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi
echo "[OK] Python found: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
echo "[OK] Node.js found: $(node --version)"
echo ""

# Setup Backend
echo "[1/4] Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt --quiet

if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "[ACTION REQUIRED] Edit backend/.env and add your CoC API key!"
    echo "Get your key from: https://developer.clashofclans.com"
fi

cd ..
echo "[OK] Backend setup complete"
echo ""

# Setup Frontend
echo "[2/4] Setting up Frontend..."
cd frontend

if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
fi

echo "Installing Node.js dependencies (this may take a minute)..."
npm install --silent

cd ..
echo "[OK] Frontend setup complete"
echo ""

# MongoDB check
echo "[3/4] Checking MongoDB..."
echo "Please ensure MongoDB is running on localhost:27017"
echo "Download MongoDB: https://www.mongodb.com/try/download/community"
echo ""

# Final Instructions
echo "[4/4] Setup Complete!"
echo ""
echo "========================================"
echo " HOW TO RUN THE APPLICATION"
echo "========================================"
echo ""
echo "TERMINAL 1 - Start Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
echo ""
echo "TERMINAL 2 - Start Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "========================================"
echo " IMPORTANT: CoC API Key Setup"
echo "========================================"
echo ""
echo "1. Go to https://developer.clashofclans.com"
echo "2. Create or edit an API key"
echo "3. Add your local IP (find it at https://whatismyip.com)"
echo "4. Put the key in backend/.env (COC_API_KEY=your_key)"
echo ""
