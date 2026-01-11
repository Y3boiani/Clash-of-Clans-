# Clash of Clans ML Research Platform

A portfolio-grade machine learning research platform that analyzes Clash of Clans battle strategies using advanced ML techniques.

![CoC ML Platform](https://img.shields.io/badge/Next.js-15-black) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)

## 🎯 Overview

This platform demonstrates advanced ML concepts through real-world Clash of Clans data:

- **7 ML Modules** covering entropy, stochastic processes, graph analytics, game theory, and fairness auditing
- **Educational Design** - Learn ML by reverse-engineering the analysis
- **Beautiful CoC-Themed UI** - Dark theme with gold accents matching the game
- **Real API Integration** - Connect to official CoC API

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **MongoDB** (running on localhost:27017)

### Windows Setup

```batch
# Double-click or run in Command Prompt:
setup-windows.bat
```

### Linux/Mac Setup

```bash
chmod +x setup-unix.sh
./setup-unix.sh
```

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

# Create .env file
echo "COC_API_KEY=your_key_here" > .env
echo "MONGO_URL=mongodb://localhost:27017" >> .env
echo "DB_NAME=coc_ml_research" >> .env
echo "CORS_ORIGINS=*" >> .env

# Start the backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

#### Frontend
```bash
cd frontend
npm install

# Create .env file
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8001" > .env

# Start the frontend
npm run dev
```

#### Access the App
Open http://localhost:3000 in your browser.

## 🔑 CoC API Key Setup

1. Go to https://developer.clashofclans.com
2. Create or edit an API key
3. Add your machine's IP address to allowed IPs
4. Copy the key to `backend/.env`

## 🧠 ML Modules

| Module | Name | ML Concepts |
|--------|------|-------------|
| 1 | Leadership Entropy | Shannon Entropy, Network Analysis, Bayesian Models |
| 2 | Pressure Function | Gaussian Processes, Variance Modeling, Beta Distribution |
| 3 | Coordination Analysis | Point Processes, Hidden Markov Models, Motif Detection |
| 4 | Trophy Volatility | Ornstein-Uhlenbeck, Monte Carlo, Kalman Filtering |
| 5 | Donation Networks | Graph Analytics, Gini Coefficient, PageRank |
| 6 | Capital Investment | Public Goods Game, Causal Inference, Free-Rider Detection |
| 7 | Matchmaking Fairness | Demographic Parity, Propensity Scores, Bias Detection |

## 📁 Project Structure

```
/app
├── backend/
│   ├── server.py              # FastAPI server
│   ├── coc_api_client.py     # CoC API wrapper
│   ├── data_collector.py     # Background data collection
│   ├── feature_engineering.py
│   ├── ml_module_1_leadership.py
│   ├── ml_module_2_pressure.py
│   ├── ml_module_3_coordination.py
│   ├── ml_module_4_volatility.py
│   ├── ml_module_5_donations.py
│   ├── ml_module_6_capital.py
│   ├── ml_module_7_fairness.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # React components
│   │   └── lib/              # Utilities
│   ├── package.json
│   └── tailwind.config.ts
│
├── setup-windows.bat      # Windows setup script
├── setup-unix.sh          # Linux/Mac setup script
└── README.md
```

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python 3.10+
- **Database**: MongoDB
- **ML Libraries**: NumPy, SciPy, NetworkX

## 📚 Learning Path

1. **Beginner**: Start with Module 5 (Donation Networks) - learn graph theory basics
2. **Intermediate**: Module 4 (Trophy Volatility) - stochastic processes
3. **Advanced**: Module 7 (Matchmaking Fairness) - causal inference and bias detection

## 🤝 Contributing

Feel free to fork and extend the platform with:
- New ML modules
- Additional visualizations
- UI improvements
- Documentation

## 📄 License

MIT License - feel free to use for learning and portfolio purposes.

---

*Built with ⚔️ for ML enthusiasts and Clash of Clans players*
