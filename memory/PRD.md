# Clash of Clans ML Research Platform - PRD

## Original Problem Statement
Build an in-depth, novel machine learning research platform using data from the Clash of Clans public REST API. The goal is to create a portfolio-grade ML project demonstrating advanced feature engineering, modeling of uncertainty, inference of latent variables, and decision-support intelligence.

## Hard Constraints
1. All ideas must be feasible using ONLY data from the CoC API
2. No access to chat logs, attack replays, base layouts
3. Insights derived from longitudinal/time-series data, statistical structure, behavioral patterns, or graph modeling
4. Avoid generic/commonly done ideas (simple win prediction, basic ranking)

## User Personas
- ML enthusiasts wanting to learn through a real-world project
- Clash of Clans players interested in data-driven insights
- Portfolio builders demonstrating advanced ML concepts

## Core Requirements
- 7 ML modules implementing novel research approaches
- Educational experience for "reverse engineering" ML concepts
- Unified dashboard for visualizing all model outputs
- CoC-themed UI matching the game's aesthetic

---

## What's Been Implemented (December 2025)

### Backend (Fully Implemented)
- **API Client** (`coc_api_client.py`): Handles CoC API communication
- **Data Collector** (`data_collector.py`): Orchestrates data fetching and storage
- **Feature Engineering** (`feature_engineering.py`): Prepares data for ML models
- **7 ML Modules**:
  1. Leadership Entropy (Shannon Entropy, Network Analysis, Bayesian)
  2. Pressure Function (Gaussian Processes, Variance Modeling)
  3. Coordination Analysis (Point Processes, HMM, Motif Detection)
  4. Trophy Volatility (Ornstein-Uhlenbeck, Monte Carlo, Kalman)
  5. Donation Networks (Graph Analytics, Gini Coefficient, PageRank)
  6. Capital Investment (Public Goods Game, Causal Inference)
  7. Matchmaking Fairness (Demographic Parity, Propensity Scores)

### Frontend (Fully Implemented)
- React app with CoC-themed dark UI (gold/amber accents)
- Unified Dashboard (`UnifiedDashboard.js`) displaying all 7 model outputs
- Player/Clan Search component (`PlayerSearch.js`)
- Module cards with concept badges
- Training path section for learning progression

### Animated Visualizations (NEW - December 2025)
Created `/app/frontend/src/components/MLVisualizations.js` with:
1. **LeadershipNetwork** - Animated hierarchical network showing clan influence flow with pulsing nodes
2. **DonationFlowViz** - Animated stream diagram showing resource flow between players with gem animation
3. **CapitalInvestmentViz** - Animated bar chart with growing bars and castle icons
4. **FairnessScaleViz** - Animated balance scale showing matchmaking balance with pulse effects
5. **TrophyVolatilityViz** - Animated line chart showing trophy trajectory with prediction indicator
6. **CoordinationHeatmap** - Interactive heatmap showing attack timing patterns
7. **MiniStatViz** - Animated counter cards with trend indicators

### CSS Animations Added
- Node pulse animations for network visualizations
- Flow stream animations for donation streams
- Scale balance animations
- Trophy bounce effects
- Glow pulse for important elements
- Staggered fade-in animations
- Bar chart grow animations
- Heatmap cell hover effects

### Integration
- CoC API key configured and working
- User's clan data (Arceus from Mystic Legions) successfully collected

### Documentation
- README.md
- BACKEND_WORKFLOW.md (educational guide)
- COC_API_SETUP.md
- COC_THEME_GUIDE.md

---

## Bug Fixes (December 2025)
- ✅ Fixed JSX syntax error in App.js (duplicate closing tags at lines 146-148)
- ✅ Fixed ESLint unescaped apostrophe warning
- ✅ Fixed ESLint setState synchronous warning in FairnessScaleViz

---

## Remaining Tasks

### P1 (High Priority)
- [ ] Fix `useEffect` missing dependency warning in App.js (line ~377)
- [ ] Add more educational explanations for each ML concept

### P2 (Medium Priority)
- [ ] Add interactivity - click module summaries for detailed breakdowns
- [ ] Refactor App.js into smaller components
- [ ] Add unit tests for ML modules

### P3 (Future)
- [ ] Historical data trend visualizations
- [ ] Player comparison features
- [ ] Export/share analysis results
- [ ] Real-time data refresh

---

## Tech Stack
- **Backend**: FastAPI, Python, MongoDB
- **Frontend**: React, TailwindCSS
- **ML/Stats**: NetworkX, NumPy, SciPy

## Key API Endpoints
- `GET /api/player/{player_tag}` - **NEW** Look up any player and auto-track their clan
- `POST /api/clan/{clan_tag}` - Trigger data collection
- `GET /api/ml/dashboard/{clan_tag}` - Get all 7 model results
- `GET /api/ml/{model_name}/{clan_tag}` - Individual model results
- `GET /api/system/ip` - Get current server IP for API key setup

## Third-Party Integration
- Clash of Clans Official API (key in `/app/backend/.env`)
- **IMPORTANT**: API key must include the server's IP address (currently `34.16.56.64`)
