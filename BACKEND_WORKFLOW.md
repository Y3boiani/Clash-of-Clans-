# 🔧 Backend Architecture & Workflow Guide

## Complete Understanding of the ML Pipeline

This guide explains **EXACTLY** how data flows from Clash of Clans API through the backend to produce ML insights.

---

## 📊 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLASH OF CLANS API                          │
│              (Player Data, Clan Data, Wars, etc.)               │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ HTTP Requests (every 6 hours)
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    COC API CLIENT                                │
│  - Rate limiting (token bucket)                                  │
│  - Retry logic with exponential backoff                          │
│  - Connection pooling (aiohttp)                                  │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ Parsed JSON Data
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA COLLECTOR                                 │
│  - Async background scheduler                                    │
│  - Tracks multiple clans                                         │
│  - Collects: players, wars, attacks, capital raids              │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ Validated Pydantic Models
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MONGODB                                     │
│  Collections:                                                    │
│  - players_history (time-series)                                 │
│  - clans_history                                                 │
│  - wars_history                                                  │
│  - war_attacks                                                   │
│  - capital_raids_history                                         │
│  - ml_results (cached)                                           │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ Historical Data
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                FEATURE ENGINEERING                               │
│  - Extract statistical features                                  │
│  - Compute derived metrics                                       │
│  - Time-series transformations                                   │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ Feature Vectors
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    7 ML MODULES                                  │
│  1. Leadership Entropy (Shannon entropy, Gini)                   │
│  2. Pressure Function (Gaussian processes)                       │
│  3. Coordination (Point processes, HMM)                          │
│  4. Volatility (Ornstein-Uhlenbeck, Monte Carlo)                │
│  5. Donations (Graph analytics, PageRank)                        │
│  6. Capital (Game theory, causal inference)                      │
│  7. Fairness (Algorithmic fairness, bias detection)              │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ ML Results + Interpretations
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI SERVER                                │
│  - REST API endpoints                                            │
│  - Result caching (24h TTL)                                      │
│  - CORS handling                                                 │
│  - Background tasks                                              │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ JSON Responses
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   REACT FRONTEND                                 │
│  - Unified Dashboard                                             │
│  - Interactive visualizations                                    │
│  - Educational components                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow: Step-by-Step

### Step 1: Data Collection (Every 6 Hours)

**File:** `/app/backend/data_collector.py`

**What Happens:**
1. Background task wakes up every 6 hours
2. Loads list of tracked clans from MongoDB
3. For each clan, makes API calls to get:
   - Current clan state (members, level, stats)
   - All member player data (trophies, donations, etc.)
   - War log history
   - Current war details (if in war)
   - Capital raid history

**Code Flow:**
```python
async def start_scheduler(interval_hours=6):
    while True:
        await run_collection_cycle()
        await asyncio.sleep(interval_hours * 3600)

async def run_collection_cycle():
    for clan_tag in tracked_clans:
        await collect_clan_snapshot(clan_tag)      # Clan data
        await collect_war_log(clan_tag)            # War history
        await collect_current_war(clan_tag)        # Current war
        await collect_capital_raids(clan_tag)      # Capital
```

**Data Validation:**
- All data goes through Pydantic models
- Type checking, required fields enforced
- Invalid data rejected before storage

**Result:** 
- New documents inserted into MongoDB collections
- Time-series data accumulates over days/weeks

---

### Step 2: Data Storage (MongoDB)

**Collections Structure:**

```javascript
// players_history
{
  id: "uuid",
  player_tag: "#2YJ2URLQJ",
  snapshot_time: ISODate("2026-01-11T18:00:00Z"),
  name: "Arceus",
  trophies: 5200,
  donations: 1500,
  donations_received: 800,
  // ... more fields
}

// wars_history
{
  id: "uuid",
  clan_tag: "#2G8VUQGP8",
  result: "win",
  end_time: "2026-01-10T12:00:00Z",
  clan_stars: 42,
  opponent_stars: 38,
  // ... more fields
}
```

**Indexes for Performance:**
```python
# MongoDB automatically indexes:
players_history.create_index([
    ("player_tag", 1), 
    ("snapshot_time", -1)
])

wars_history.create_index([
    ("clan_tag", 1),
    ("end_time", -1)
])
```

**Query Pattern:**
```python
# Get last 30 days of player data
snapshots = await db.players_history.find({
    "player_tag": "#2YJ2URLQJ",
    "snapshot_time": {"$gt": datetime.utcnow() - timedelta(days=30)}
}).sort("snapshot_time", 1).to_list(1000)
```

---

### Step 3: Feature Engineering

**File:** `/app/backend/feature_engineering.py`

**Purpose:** Transform raw data into ML-ready features

**Example 1: Trophy Momentum**
```python
def compute_trophy_momentum(snapshots, window_days=7):
    """
    Compute rate of trophy change (velocity).
    
    Mathematical Formula:
        momentum = (trophies_end - trophies_start) / days
    
    Interpretation:
        > 0: Player climbing
        < 0: Player falling
        = 0: Stable
    """
    # Filter to window
    recent = [s for s in snapshots 
              if s['snapshot_time'] > now - timedelta(days=window_days)]
    
    # Linear regression on trophy trajectory
    times = [(s['snapshot_time'] - recent[0]['snapshot_time']).days 
             for s in recent]
    trophies = [s['trophies'] for s in recent]
    
    slope = (trophies[-1] - trophies[0]) / max(times[-1], 1)
    return slope
```

**Example 2: Donation Ratio**
```python
def compute_donation_ratio(snapshot):
    """
    Ratio of donations given to received.
    
    Interpretation:
        > 1: Net giver (benefactor)
        = 1: Balanced
        < 1: Net receiver (parasite)
    """
    given = snapshot['donations']
    received = snapshot['donations_received']
    return given / max(received, 1)
```

**Example 3: Activity Consistency**
```python
def compute_activity_consistency(snapshots):
    """
    Measure how consistently active a player is.
    
    Uses coefficient of variation (CV):
        CV = std_deviation / mean
    
    Low CV = consistent activity
    High CV = sporadic activity
    """
    trophy_changes = np.diff([s['trophies'] for s in snapshots])
    mean_change = np.mean(trophy_changes)
    cv = np.std(trophy_changes) / mean_change
    
    consistency = 1 - min(cv, 1.0)  # Invert so higher = more consistent
    return consistency
```

---

### Step 4: ML Model Execution

**Each ML module follows this pattern:**

```python
class MLModel:
    def __init__(self):
        self.name = "model_name"
    
    def extract_features(self, raw_data):
        """Transform raw data into feature vector"""
        features = []
        for record in raw_data:
            feature = compute_something(record)
            features.append(feature)
        return features
    
    def apply_algorithm(self, features):
        """Apply ML/statistical algorithm"""
        # Could be:
        # - Shannon entropy calculation
        # - Linear regression
        # - Graph centrality computation
        # - Monte Carlo simulation
        # etc.
        results = algorithm(features)
        return results
    
    def interpret_results(self, results):
        """Convert numbers to human-readable insights"""
        if results > threshold:
            interpretation = "High X detected"
        else:
            interpretation = "Low X detected"
        
        return {
            'metrics': results,
            'interpretation': interpretation,
            'confidence': calculate_confidence(results)
        }
    
    def generate_report(self, raw_data):
        """Main entry point"""
        features = self.extract_features(raw_data)
        results = self.apply_algorithm(features)
        interpreted = self.interpret_results(results)
        
        return {
            'model': self.name,
            'timestamp': datetime.utcnow(),
            'analysis': interpreted
        }
```

**Example: Leadership Entropy Module**

```python
# File: ml_module_1_leadership.py

def generate_report(player_snapshots, war_attacks, clan_snapshots):
    # STEP 1: Extract behavioral signals for each player
    for player_tag in member_tags:
        player_data = [s for s in player_snapshots if s['player_tag'] == player_tag]
        
        signals = {
            'donation_leadership': compute_donation_ratio(player_data[-1]),
            'war_participation': len([a for a in war_attacks if a['attacker_tag'] == player_tag]) / expected_wars,
            'activity_consistency': compute_consistency(player_data),
            'tenure_stability': days_observed / 30
        }
        
        # STEP 2: Combine into influence score
        influence = (
            signals['donation_leadership'] * 0.3 +
            signals['war_participation'] * 0.35 +
            signals['activity_consistency'] * 0.2 +
            signals['tenure_stability'] * 0.15
        )
        
        influence_scores[player_tag] = influence
    
    # STEP 3: Compute Shannon entropy
    # H = -Σ(p_i * log(p_i))
    total = sum(influence_scores.values())
    probabilities = [score / total for score in influence_scores.values()]
    entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
    
    # STEP 4: Interpret
    if entropy < 1.5:
        leadership_type = "centralized"
    elif entropy < 2.5:
        leadership_type = "oligarchic"
    else:
        leadership_type = "distributed"
    
    return {
        'entropy': entropy,
        'leadership_type': leadership_type,
        'top_leaders': sorted_by_influence[:10]
    }
```

---

### Step 5: API Endpoint

**File:** `/app/backend/server.py`

**Endpoint Pattern:**
```python
@api_router.post("/ml/leadership/analyze")
async def analyze_leadership(request: MLAnalysisRequest):
    """
    Endpoint for leadership entropy analysis.
    
    Request Body:
        {
            "clan_tag": "#2G8VUQGP8",
            "force_refresh": false
        }
    
    Response:
        {
            "model": "leadership_entropy",
            "timestamp": "2026-01-11T18:00:00Z",
            "leadership_entropy": {
                "entropy": 4.2,
                "leadership_type": "distributed",
                ...
            },
            "top_leaders": [...]
        }
    """
    
    # STEP 1: Check cache (avoid recomputation)
    if not request.force_refresh:
        cached = await db.ml_results.find_one({
            "model_name": "leadership_entropy",
            "entity_id": request.clan_tag,
            "valid_until": {"$gt": datetime.utcnow()}
        })
        
        if cached:
            return cached['results']  # Return cached result
    
    # STEP 2: Fetch required data from MongoDB
    player_snapshots = await db.players_history.find({
        "clan_tag": request.clan_tag
    }).to_list(10000)
    
    war_attacks = await db.war_attacks.find({
        "clan_tag": request.clan_tag
    }).to_list(5000)
    
    clan_snapshots = await db.clans_history.find({
        "clan_tag": request.clan_tag
    }).to_list(1000)
    
    # STEP 3: Check data sufficiency
    if not player_snapshots or not clan_snapshots:
        raise HTTPException(
            status_code=404,
            detail="Insufficient data for analysis"
        )
    
    # STEP 4: Run ML model
    model = ml_models['leadership']
    results = model.generate_report(
        player_snapshots, 
        war_attacks, 
        clan_snapshots
    )
    
    # STEP 5: Cache results (24 hour TTL)
    await db.ml_results.insert_one({
        "model_name": "leadership_entropy",
        "entity_type": "clan",
        "entity_id": request.clan_tag,
        "computed_at": datetime.utcnow(),
        "valid_until": datetime.utcnow() + timedelta(hours=24),
        "results": results,
        "data_points_used": len(player_snapshots)
    })
    
    # STEP 6: Return results
    return results
```

**Why Caching?**
- ML computations can take 1-10 seconds
- Data doesn't change that frequently
- Reduces MongoDB queries
- Improves user experience

---

### Step 6: Frontend Display

**File:** `/app/frontend/src/components/UnifiedDashboard.js`

**React Flow:**
```javascript
const UnifiedDashboard = () => {
    const [analyses, setAnalyses] = useState({});
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        loadAllAnalyses();
    }, []);
    
    const loadAllAnalyses = async () => {
        // Fetch all 7 models in parallel
        const promises = {
            leadership: axios.post(`${API}/ml/leadership/analyze`, {...}),
            donations: axios.post(`${API}/ml/donations/analyze`, {...}),
            // ... etc for all 7
        };
        
        const results = await Promise.all(Object.values(promises));
        
        // Store results
        const analysesData = {};
        Object.keys(promises).forEach((key, i) => {
            analysesData[key] = results[i].data;
        });
        
        setAnalyses(analysesData);
        setLoading(false);
    };
    
    return (
        <div>
            {/* Display all results */}
            <LeadershipSection data={analyses.leadership} />
            <DonationsSection data={analyses.donations} />
            {/* ... etc */}
        </div>
    );
};
```

---

## 🎓 Key Learning Points

### 1. Async/Await Pattern
**Why?** Python and JavaScript are single-threaded. Async allows non-blocking I/O.

```python
# Synchronous (BAD - blocks for 5 seconds)
def fetch_data():
    response = requests.get(url)  # Waits here
    return response.json()

# Asynchronous (GOOD - can handle other requests while waiting)
async def fetch_data():
    async with session.get(url) as response:  # Doesn't block
        return await response.json()
```

### 2. Rate Limiting (Token Bucket Algorithm)
**Why?** CoC API limits requests to ~10/second.

```python
class RateLimiter:
    def __init__(self):
        self.tokens = 10  # Start with 10 tokens
        self.max_tokens = 10
        self.refill_rate = 0.1  # 1 token per 0.1s = 10/s
    
    async def wait_for_token(self):
        # Refill tokens based on time passed
        time_passed = now - last_refill
        self.tokens += time_passed / self.refill_rate
        self.tokens = min(self.tokens, self.max_tokens)
        
        # Wait if no tokens available
        while self.tokens < 1:
            await asyncio.sleep(0.1)
            # Refill again
        
        self.tokens -= 1  # Consume token
```

### 3. Pydantic Validation
**Why?** Ensures data integrity before storage.

```python
class PlayerSnapshot(BaseModel):
    player_tag: str  # Required
    trophies: int    # Type-checked
    name: str        # Validated
    snapshot_time: datetime = Field(default_factory=datetime.utcnow)
    
# If you try:
PlayerSnapshot(player_tag=123)  # ERROR: must be string
PlayerSnapshot(trophies="abc")  # ERROR: must be int
```

### 4. Connection Pooling
**Why?** Reuse HTTP connections instead of creating new ones.

```python
# Without pooling (SLOW):
for i in range(100):
    response = requests.get(url)  # New connection each time

# With pooling (FAST):
async with ClientSession() as session:  # Connection pool
    for i in range(100):
        response = await session.get(url)  # Reuses connections
```

### 5. Background Tasks
**Why?** Don't block user requests while collecting data.

```python
@app.on_event("startup")
async def startup():
    # Start background task
    asyncio.create_task(data_collector.start_scheduler())
    # Returns immediately, task runs in background

# Main request handling continues normally
@app.get("/api/data")
async def get_data():
    # This can respond immediately
    # Background collector runs separately
```

---

## 🔍 How to Debug

### Check Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.err.log

# Frontend logs
tail -f /var/log/supervisor/frontend.out.log

# MongoDB
sudo systemctl status mongodb
```

### Test API Manually
```bash
# Test endpoint
curl -X POST http://localhost:8001/api/ml/leadership/analyze \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#2G8VUQGP8"}'

# Check what data exists
curl http://localhost:8001/api/data/clan/%232G8VUQGP8/stats
```

### Inspect MongoDB
```bash
# Connect to MongoDB
mongosh

# Switch to database
use coc_ml_research

# Count documents
db.players_history.countDocuments({clan_tag: "#2G8VUQGP8"})

# View sample
db.players_history.findOne({clan_tag: "#2G8VUQGP8"})
```

---

## 📚 Next Steps for Learning

1. **Trace a single request:** 
   - Add `print()` statements in server.py
   - Make API call
   - Watch logs to see execution flow

2. **Modify feature engineering:**
   - Edit `feature_engineering.py`
   - Change weight coefficients
   - See how results change

3. **Create your own ML module:**
   - Copy `ml_module_1_leadership.py`
   - Rename to `ml_module_8_yourname.py`
   - Implement your own analysis

4. **Experiment with algorithms:**
   - Replace entropy with different metric
   - Try different regression methods
   - Add new statistical tests

5. **Visualize the pipeline:**
   - Add charts to frontend
   - Show data flow
   - Display intermediate results

---

## 🎯 Summary

**Data Journey:**
```
CoC API → API Client → Data Collector → MongoDB → 
Feature Engineering → ML Models → FastAPI → React → User
```

**Time Scale:**
- Data collection: Every 6 hours
- Cache TTL: 24 hours
- Best results: After 7-30 days of data

**Key Files to Study:**
1. `server.py` - API endpoints
2. `data_collector.py` - Data pipeline
3. `ml_module_1_leadership.py` - Example ML model
4. `feature_engineering.py` - Feature extraction

**This is production-grade ML engineering!** 🚀
