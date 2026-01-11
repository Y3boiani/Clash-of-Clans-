# ⚔️ Clash of Clans ML Research Platform

A portfolio-grade machine learning research platform that analyzes Clash of Clans battle strategies using advanced ML techniques. **Learn ML by reverse-engineering real-world game data!**

![Next.js](https://img.shields.io/badge/Next.js-15-black) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **MongoDB** - [Download](https://www.mongodb.com/try/download/community)

### Windows
```batch
# Double-click or run:
setup-windows.bat
```

### Linux/Mac
```bash
chmod +x setup-unix.sh
./setup-unix.sh
```

### Then:
1. **Edit `backend/.env`** - Add your CoC API key (see below)
2. **Start MongoDB** (if not running)
3. **Start Backend**: `cd backend && venv\Scripts\activate && uvicorn server:app --port 8001 --reload`
4. **Start Frontend**: `cd frontend && npm run dev`
5. **Open**: http://localhost:3000

---

## 🔑 CoC API Key Setup

1. Go to https://developer.clashofclans.com
2. Sign in and create a new API key
3. **Add your IP address** to the allowed IPs:
   - Find your IP: https://whatismyip.com
   - Add it to the key's allowed IPs list
4. Copy the key to `backend/.env`:
   ```
   COC_API_KEY=your_key_here
   ```

---

## 🧠 The 7 ML Modules

| # | Module | What You'll Learn |
|---|--------|-------------------|
| 1 | **Leadership Entropy** | Shannon Entropy, Network Analysis, Bayesian Estimation |
| 2 | **Pressure Function** | Gaussian Processes, Variance Modeling, Beta Distribution |
| 3 | **Coordination Analysis** | Point Processes, Hidden Markov Models, Motif Detection |
| 4 | **Trophy Volatility** | Ornstein-Uhlenbeck Process, Kalman Filter, Monte Carlo |
| 5 | **Donation Networks** | Graph Theory, Gini Coefficient, PageRank Algorithm |
| 6 | **Capital Investment** | Game Theory, Free-Rider Detection, Causal Inference |
| 7 | **Matchmaking Fairness** | Demographic Parity, Propensity Scores, Bias Detection |

---

## 📁 Project Structure

```
coc-ml-research/
├── backend/                    # FastAPI + Python ML
│   ├── server.py              # Main API server
│   ├── coc_api_client.py      # CoC API wrapper
│   ├── data_collector.py      # Background data collection
│   ├── ml_module_1_leadership.py
│   ├── ml_module_2_pressure.py
│   ├── ml_module_3_coordination.py
│   ├── ml_module_4_volatility.py
│   ├── ml_module_5_donations.py
│   ├── ml_module_6_capital.py
│   ├── ml_module_7_fairness.py
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
├── frontend/                   # Next.js 15 + TypeScript
│   ├── src/app/               # Pages (App Router)
│   ├── src/components/        # React components
│   ├── package.json           # Node dependencies
│   └── .env.example           # Environment template
│
├── setup-windows.bat          # Windows setup script
├── setup-unix.sh              # Linux/Mac setup script
└── README.md                  # This file
```

---

## 📚 Learning Path

**Beginner** → Start with **Module 5 (Donation Networks)**
- Learn graph theory basics
- Understand Gini coefficient for inequality
- See PageRank in action

**Intermediate** → Try **Module 4 (Trophy Volatility)**
- Stochastic differential equations
- Kalman filtering for prediction
- Monte Carlo simulations

**Advanced** → Master **Module 7 (Matchmaking Fairness)**
- Causal inference techniques
- Bias detection in algorithms
- Fairness metrics

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React 19, TypeScript, TailwindCSS |
| Backend | FastAPI, Python 3.10+ |
| Database | MongoDB |
| ML | NumPy, SciPy, NetworkX |
| API | Clash of Clans Official API |

---

## 🤝 Contributing

Feel free to:
- Add new ML modules
- Improve visualizations
- Fix bugs
- Enhance documentation

---

## 📄 License

MIT License - Use freely for learning and portfolio purposes.

---

*Built with ⚔️ for ML enthusiasts and Clash of Clans players*
