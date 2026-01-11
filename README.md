# Clash of Clans ML Research Platform

A **production-grade machine learning research platform** for analyzing Clash of Clans data using advanced statistical and ML techniques.

## 🎯 Project Overview

This is **NOT a typical CoC stats dashboard**. This is a **portfolio-grade ML research project** that demonstrates:

- Advanced statistical modeling (stochastic processes, Bayesian inference)
- Social network analysis and graph theory
- Time-series analysis and forecasting
- Causal inference and algorithmic fairness
- Game-theoretic modeling
- Production ML deployment patterns

Built for **learning ML by reverse-engineering** working implementations.

---

## 📊 Research Modules

### Module 1: Leadership Entropy & Authority Distribution
**Research Question:** Can we infer latent leadership structures from behavioral signals?

**ML Techniques:**
- Latent variable modeling
- Shannon entropy for organizational analysis
- Bayesian network for conditional dependencies
- Graph centrality measures (PageRank-style)
- Gini coefficient for authority concentration

**Output:** Leadership influence scores, organizational entropy index, stability risk predictions

**File:** `ml_module_1_leadership.py`

---

### Module 2: War Performance Pressure Function
**Research Question:** How does situational pressure affect individual performance?

**ML Techniques:**
- Gaussian Process Regression for performance curves
- Hierarchical Bayesian modeling for player-specific variance
- Contextual feature engineering
- Beta distribution fitting for probabilities
- Variance decomposition (skill vs consistency)

**Output:** Pressure sensitivity coefficients, choking probability, reliability scores, player archetypes

**File:** `ml_module_2_pressure.py`

---

### Module 3: Strategic Coherence & Coordination
**Research Question:** Can we measure coordination without access to chat?

**ML Techniques:**
- Point process models (Hawkes processes) for timing analysis
- Network motif detection in targeting patterns
- Hidden Markov Models for coordination states
- Mutual information between decisions
- Temporal clustering analysis

**Output:** Coordination index (0-100), strategic motif fingerprints, timing efficiency scores

**File:** `ml_module_3_coordination.py`

---

### Module 4: Trophy Momentum & Rank Volatility
**Research Question:** Can we model trophy trajectories as stochastic processes?

**ML Techniques:**
- Ornstein-Uhlenbeck process (mean-reverting random walk)
- GARCH models for time-varying volatility
- Kalman filtering for skill vs luck decomposition
- Monte Carlo simulation for trajectory forecasting
- Regime detection (momentum vs tilt)

**Output:** Volatility index, skill/luck decomposition, 30-day forecasts, tilt detection

**File:** `ml_module_4_volatility.py`

---

### Module 5: Donation Economy & Resource Flow
**Research Question:** Can we model clans as economic networks to detect exploitation?

**ML Techniques:**
- Directed graph analysis (resource flow networks)
- PageRank for identifying critical nodes
- Gini coefficient for economic inequality
- Survival analysis for retention prediction
- Community detection algorithms

**Output:** Network centrality rankings, free-rider detection, reciprocity index, retention risk

**File:** `ml_module_5_donations.py`

---

### Module 6: Clan Capital Collective Action
**Research Question:** Do contribution patterns predict raid success better than capital level?

**ML Techniques:**
- Game-theoretic modeling (public goods game)
- Causal inference (propensity score matching)
- Free-rider detection via inequality metrics
- Agent-based simulation concepts
- Hypothesis testing with regression analysis

**Output:** Contribution inequality metrics, free-rider scores, policy recommendations

**File:** `ml_module_6_capital.py`

---

### Module 7: Matchmaking Fairness Audit
**Research Question:** Does CoC matchmaking exhibit systematic biases?

**ML Techniques:**
- Algorithmic fairness metrics (demographic parity, equalized odds)
- Propensity score analysis
- Regression discontinuity design
- Bayesian A/B testing
- Counterfactual fairness modeling

**Output:** Bias assessment, fairness grade, win rate analysis by characteristics

**File:** `ml_module_7_fairness.py`

---

## 🏗️ Architecture

```
/app/backend/
├── server.py                    # FastAPI server with all endpoints
├── coc_api_client.py           # Async CoC API client with rate limiting
├── data_collector.py           # Background data collection scheduler
├── data_models.py              # Pydantic models for all data types
├── feature_engineering.py      # Feature extraction utilities
├── ml_module_1_leadership.py   # Leadership entropy model
├── ml_module_2_pressure.py     # Pressure function model
├── ml_module_3_coordination.py # Coordination analysis model
├── ml_module_4_volatility.py   # Trophy volatility model
├── ml_module_5_donations.py    # Donation network model
├── ml_module_6_capital.py      # Capital investment model
├── ml_module_7_fairness.py     # Matchmaking fairness model
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (CoC API key)
```

### Data Flow

1. **Data Collection** (`data_collector.py`)
   - Runs every 6 hours
   - Fetches clan, player, war, and capital data
   - Stores time-series snapshots in MongoDB

2. **Feature Engineering** (`feature_engineering.py`)
   - Extracts statistical features from raw data
   - Computes derived metrics (momentum, volatility, etc.)

3. **ML Models** (`ml_module_*.py`)
   - Each module is independent
   - Takes time-series data as input
   - Returns analysis results

4. **API Server** (`server.py`)
   - Exposes ML models via REST endpoints
   - Handles caching (24-hour TTL)
   - Manages background tasks

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- MongoDB (running locally on port 27017)
- Clash of Clans API key (already configured in `.env`)

### Installation

```bash
# Navigate to backend directory
cd /app/backend

# Install dependencies (already done)
pip install -r requirements.txt

# Verify MongoDB is running
# MongoDB should be accessible at mongodb://localhost:27017
```

### Starting the Server

The server runs automatically via supervisor, but to start manually:

```bash
cd /app/backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001
```

### Access the API

Base URL: `http://localhost:8001/api/`

API documentation (Swagger): `http://localhost:8001/docs`

---

## 📖 Usage Guide

### Step 1: Add a Clan to Track

```bash
curl -X POST http://localhost:8001/api/data/add-clan \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#2PP"}'
```

This starts collecting data for the clan.

### Step 2: Check Data Collection Status

```bash
curl http://localhost:8001/api/data/clan/%232PP/stats
```

Wait until `ml_readiness` shows `true` for desired modules (usually 24-48 hours for best results, but some work with minimal data).

### Step 3: Run ML Analyses

#### Leadership Analysis
```bash
curl -X POST http://localhost:8001/api/ml/leadership/analyze \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#2PP"}'
```

#### Pressure Analysis (Player)
```bash
curl -X POST http://localhost:8001/api/ml/pressure/analyze-player \
  -H "Content-Type: application/json" \
  -d '{"player_tag": "#PLAYER123"}'
```

#### Donation Network
```bash
curl -X POST http://localhost:8001/api/ml/donations/analyze \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#2PP"}'
```

#### Full Dashboard
```bash
curl http://localhost:8001/api/ml/dashboard/%232PP
```

### Testing with Popular Clans

For immediate results, track well-known clans with public war logs:

```bash
# Add Nova eSports
curl -X POST http://localhost:8001/api/data/add-clan \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#2PP"}'

# Add Tribe Gaming
curl -X POST http://localhost:8001/api/data/add-clan \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#828JLY0U"}'
```

---

## 🧠 Learning Path: How to Reverse Engineer

### For ML Beginners

**Start with Module 5 (Donations)** - Most intuitive
1. Read `ml_module_5_donations.py`
2. Trace through `build_donation_graph()` - see how graphs are built
3. Understand `_compute_gini()` - economic inequality metric
4. See how multiple signals combine in `_compute_health_score()`

**Then Module 1 (Leadership)** - Social network analysis
1. Study `compute_behavioral_signals()` - feature engineering
2. See `compute_organizational_entropy()` - information theory
3. Learn weighted scoring in `_compute_influence_score()`

### For Intermediate ML Practitioners

**Start with Module 4 (Volatility)** - Stochastic processes
1. Study `estimate_ou_parameters()` - parameter estimation
2. Understand `forecast_trajectory()` - Monte Carlo simulation
3. See `decompose_skill_luck()` - signal decomposition

**Then Module 2 (Pressure)** - Regression & variance
1. Analyze `compute_pressure_sensitivity()` - linear regression
2. Study `compute_choking_probability()` - probabilistic modeling
3. Understand contextual feature engineering in `compute_attack_pressure()`

### For Advanced Practitioners

**Start with Module 7 (Fairness)** - Causal inference
1. Study `test_demographic_parity()` - fairness metrics
2. Analyze `detect_matchmaking_bias()` - statistical testing
3. Understand two-proportion z-test implementation

**Then Module 6 (Capital)** - Game theory
1. Study `test_contribution_pattern_hypothesis()` - causal reasoning
2. See `detect_free_riders()` - percentile-based detection
3. Understand policy recommendation generation

---

## 📚 Key Concepts Demonstrated

### Statistical Modeling
- **Stochastic Processes:** Ornstein-Uhlenbeck, random walks
- **Time Series:** GARCH, regime detection, trend analysis
- **Bayesian Inference:** Hierarchical models, posterior estimation
- **Hypothesis Testing:** t-tests, z-tests, binomial tests

### Machine Learning
- **Unsupervised Learning:** Clustering, community detection
- **Latent Variables:** Inferring hidden states from observations
- **Feature Engineering:** Domain-specific signal extraction
- **Ensemble Methods:** Multi-signal combination

### Network Analysis
- **Graph Theory:** Centrality measures, motif detection
- **Social Networks:** Influence modeling, authority distribution
- **Flow Networks:** Resource flow, reciprocity analysis

### Causal Inference
- **Propensity Scores:** Covariate balancing
- **Counterfactual Reasoning:** What-if analysis
- **Regression Discontinuity:** Threshold effects
- **Algorithmic Fairness:** Bias detection

---

## 🔬 Data Science Best Practices

### 1. Handling Insufficient Data
Every module checks data availability:
```python
if len(snapshots) < 10:
    return {'status': 'insufficient_data'}
```

### 2. Confidence Intervals
Models report confidence levels:
```python
if n >= 30 and sigma > 0:
    confidence = 'high'
elif n >= 8:
    confidence = 'medium'
else:
    confidence = 'low'
```

### 3. Normalization
Scores are normalized to interpretable scales:
```python
# 0-1 scale
score = min(max(raw_score, 0), 1.0)

# 0-100 scale
index = score * 100
```

### 4. Caching
Expensive computations are cached:
```python
await db.ml_results.insert_one({
    "model_name": "leadership_entropy",
    "valid_until": datetime.utcnow() + timedelta(hours=24),
    "results": results
})
```

### 5. Error Handling
Graceful degradation throughout:
```python
try:
    result = model.analyze(data)
except Exception as e:
    logger.error(f"Analysis failed: {e}")
    result = {"error": "insufficient_data"}
```

---

## 🎓 Educational Value

### What You'll Learn

**Statistics:**
- Entropy and information theory
- Variance and standard deviation
- Correlation vs causation
- Statistical significance testing
- Confidence intervals

**Machine Learning:**
- Feature extraction from raw data
- Model evaluation and validation
- Handling class imbalance
- Multi-objective optimization
- Model interpretability

**Software Engineering:**
- Async Python patterns
- REST API design
- Caching strategies
- Background task scheduling
- Database indexing

**Domain Expertise:**
- Gaming analytics
- Behavioral modeling
- Social network analysis
- Economic modeling
- Fairness and ethics in ML

---

## 🛠️ Customization & Extension

### Adding New Features

1. **Create a new feature in `feature_engineering.py`:**
```python
def compute_my_feature(data: List[Dict]) -> float:
    # Your feature logic
    return feature_value
```

2. **Use it in an ML module:**
```python
my_feature = compute_my_feature(player_data)
```

### Creating a New ML Module

1. Create `ml_module_8_myanalysis.py`
2. Define a class with `generate_report()` method
3. Add endpoints in `server.py`
4. Update this README

### Connecting to Your Own Data

Replace data_collector.py with your own data source:
```python
# Custom data ingestion
async def my_data_collector():
    # Your logic to fetch and store data
    await db.my_collection.insert_many(data)
```

---

## 🧪 Testing

### Manual Testing via API

```bash
# Test server is running
curl http://localhost:8001/api/

# Test data collection
curl http://localhost:8001/api/data/clans

# Test individual module
curl -X POST http://localhost:8001/api/ml/leadership/analyze \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#2PP", "force_refresh": true}'
```

### Understanding Model Outputs

Each model returns structured JSON with:
- **Metrics:** Numerical scores (0-1 or 0-100)
- **Interpretation:** Human-readable description
- **Confidence:** Data quality indicator
- **Recommendations:** Actionable insights

---

## 📊 MongoDB Collections

```
coc_ml_research/
├── players_history          # Time-series player snapshots
├── clans_history           # Time-series clan snapshots
├── wars_history            # War outcome records
├── war_attacks             # Individual attack records
├── capital_raids_history   # Clan capital raid data
├── ml_results              # Cached ML model outputs
└── config                  # System configuration
```

### Indexes for Performance

Automatically created:
```python
# Example indexes
db.players_history.create_index([("player_tag", 1), ("snapshot_time", -1)])
db.clans_history.create_index([("clan_tag", 1), ("snapshot_time", -1)])
db.war_attacks.create_index([("war_id", 1), ("attacker_tag", 1)])
```

---

## 🚦 API Endpoints Reference

### Data Collection
- `POST /api/data/add-clan` - Add clan to tracking
- `GET /api/data/clans` - List tracked clans
- `GET /api/data/clan/{tag}/stats` - Data availability stats

### ML Analyses
- `POST /api/ml/leadership/analyze` - Leadership entropy
- `POST /api/ml/pressure/analyze-player` - Player pressure analysis
- `POST /api/ml/pressure/analyze-clan` - Clan pressure analysis
- `POST /api/ml/coordination/analyze-war` - War coordination
- `POST /api/ml/coordination/analyze-clan-trend` - Coordination trends
- `POST /api/ml/volatility/analyze` - Trophy volatility
- `POST /api/ml/donations/analyze` - Donation network
- `POST /api/ml/capital/analyze` - Capital investment
- `POST /api/ml/fairness/audit` - Matchmaking fairness
- `GET /api/ml/dashboard/{tag}` - Comprehensive dashboard

---

## 🎯 Production Optimizations

### 1. Rate Limiting
Token bucket algorithm in `coc_api_client.py`:
```python
async def _wait_for_token(self):
    # Respects API rate limits
```

### 2. Connection Pooling
Async HTTP with connection reuse:
```python
connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
```

### 3. Background Tasks
Data collection runs independently:
```python
asyncio.create_task(data_collector.start_scheduler(interval_hours=6))
```

### 4. Caching Strategy
24-hour TTL on ML results:
```python
"valid_until": datetime.utcnow() + timedelta(hours=24)
```

### 5. Batch Processing
Parallel data collection:
```python
tasks = [self.collect_player_snapshot(tag) for tag in member_tags]
await asyncio.gather(*tasks, return_exceptions=True)
```

---

## 🤝 Contributing

This is a learning project! To extend:

1. **Add more sophisticated models:**
   - Deep learning for attack success prediction
   - Reinforcement learning for optimal attack ordering
   - NLP on clan descriptions

2. **Improve statistical rigor:**
   - Add cross-validation
   - Implement proper train/test splits across clans
   - Add confidence intervals to all estimates

3. **Enhance visualizations:**
   - Add a frontend with charts
   - Create interactive dashboards
   - Visualize network graphs

---

## 📝 License & Usage

This is an educational project demonstrating ML techniques. 

**Important:** 
- Uses official Clash of Clans API (respect their terms)
- Not affiliated with Supercell
- For educational purposes only

---

## 🙏 Acknowledgments

**ML Techniques Inspired By:**
- Financial mathematics (stochastic processes)
- Social network analysis research
- Algorithmic fairness literature
- Behavioral economics
- Game theory

**Tools & Libraries:**
- FastAPI for async Python web
- Motor for async MongoDB
- NumPy/SciPy for numerical computing
- aiohttp for async HTTP

---

## 📞 Support

For questions about ML concepts in the code:

1. **Read the docstrings** - Every function explains what it does and why
2. **Check comments** - Key algorithms have inline explanations
3. **Trace execution** - Add print statements to see data flow
4. **Experiment** - Modify parameters and see what changes

---

## 🎉 Happy Learning!

This project demonstrates that **production ML is about much more than model training**:
- Data engineering (collection, storage, pipelines)
- Feature engineering (domain knowledge → features)
- Statistical rigor (confidence, significance testing)
- Software engineering (async, caching, APIs)
- Communication (interpretable results)

**Start by picking one module, reading it thoroughly, and experimenting!**

Good luck reverse engineering these ML systems! 🚀
