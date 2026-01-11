#!/bin/bash
# ========================================
# CoC ML Research Platform - Linux/Mac Setup
# ========================================

echo ""
echo "========================================"
echo " CoC ML Research Platform Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.10+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed"
    echo "Please install Node.js 18+"
    exit 1
fi

echo "[OK] Python and Node.js found"
echo ""

# Setup Backend
echo "[1/4] Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
COC_API_KEY=your_api_key_here
MONGO_URL=mongodb://localhost:27017
DB_NAME=coc_ml_research
CORS_ORIGINS=*
EOF
    echo ""
    echo "[IMPORTANT] Please edit backend/.env and add your CoC API key!"
fi

cd ..
echo "[OK] Backend setup complete"
echo ""

# Setup Frontend
echo "[2/4] Setting up Frontend..."
cd frontend

echo "Installing Node.js dependencies..."
npm install

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8001" > .env
fi

cd ..
echo "[OK] Frontend setup complete"
echo ""

# Check MongoDB
echo "[3/4] Checking MongoDB..."
echo "Please ensure MongoDB is running on localhost:27017"
echo ""

# Final Instructions
echo "[4/4] Setup Complete!"
echo ""
echo "========================================"
echo " HOW TO RUN THE APPLICATION"
echo "========================================"
echo ""
echo "1. Start MongoDB (if not running)"
echo ""
echo "2. Start the Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
echo ""
echo "3. Start the Frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "========================================"
echo " IMPORTANT: CoC API Key Setup"
echo "========================================"
echo ""
echo "To use player search, you need a CoC API key:"
echo "1. Go to https://developer.clashofclans.com"
echo "2. Create/edit your API key"
echo "3. Add your local IP to allowed IPs"
echo "4. Put the key in backend/.env"
echo ""
