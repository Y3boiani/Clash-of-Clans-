import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Get Arceus's clan tag
const ARCEUS_CLAN = '#2G8VUQGP8';

export const UnifiedDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [analyses, setAnalyses] = useState({});
  const [dataStats, setDataStats] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAllAnalyses();
  }, []);

  const loadAllAnalyses = async () => {
    setLoading(true);
    try {
      // First check data availability
      const statsResponse = await axios.get(
        `${API}/data/clan/${encodeURIComponent(ARCEUS_CLAN)}/stats`
      );
      setDataStats(statsResponse.data);

      // Load all 7 ML analyses in parallel
      const analysisPromises = {
        leadership: axios.post(`${API}/ml/leadership/analyze`, { clan_tag: ARCEUS_CLAN }).catch(e => ({ error: e.message })),
        donations: axios.post(`${API}/ml/donations/analyze`, { clan_tag: ARCEUS_CLAN }).catch(e => ({ error: e.message })),
        capital: axios.post(`${API}/ml/capital/analyze`, { clan_tag: ARCEUS_CLAN }).catch(e => ({ error: e.message })),
        fairness: axios.post(`${API}/ml/fairness/audit`, { clan_tag: ARCEUS_CLAN }).catch(e => ({ error: e.message })),
      };

      const results = await Promise.all(Object.values(analysisPromises));
      const keys = Object.keys(analysisPromises);
      
      const analysesData = {};
      keys.forEach((key, index) => {
        analysesData[key] = results[index].data || results[index];
      });

      setAnalyses(analysesData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-950 via-purple-900 to-blue-950 flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mb-4 mx-auto"></div>
          <div className="text-white text-xl">Loading ML analyses...</div>
          <div className="text-blue-300 text-sm mt-2">Running 7 ML models on your clan data</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-coc-dark coc-wood-bg">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link to="/" className="text-coc-gold hover:text-yellow-300 mb-4 inline-block font-semibold">
            ← Return to Base
          </Link>
          <h1 className="text-5xl font-bold text-coc-gold mb-2 gold-shine uppercase" data-testid="unified-dashboard-title">
            ⚔️ War Room Dashboard ⚔️
          </h1>
          <p className="text-2xl text-yellow-200">
            Complete battle analysis of <span className="text-coc-gold font-bold">Mystic Legions</span>
          </p>
        </div>

        {/* Data Stats Banner */}
        {dataStats && (
          <div className="coc-card p-6 mb-8 border-4">
            <h3 className="text-2xl font-bold text-coc-gold mb-4 uppercase flex items-center gap-3">
              <span className="coc-icon">📊</span>
              Intelligence Gathered
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="coc-stat-box">
                <div className="text-4xl font-bold text-coc-gold mb-1">{dataStats.data_availability.player_snapshots}</div>
                <div className="text-xs text-yellow-200 uppercase">Warriors</div>
              </div>
              <div className="coc-stat-box">
                <div className="text-4xl font-bold text-orange-400 mb-1">{dataStats.data_availability.wars}</div>
                <div className="text-xs text-yellow-200 uppercase">Battles</div>
              </div>
              <div className="coc-stat-box">
                <div className="text-4xl font-bold text-red-400 mb-1">{dataStats.data_availability.war_attacks}</div>
                <div className="text-xs text-yellow-200 uppercase">Attacks</div>
              </div>
              <div className="coc-stat-box">
                <div className="text-4xl font-bold text-purple-400 mb-1">{dataStats.data_availability.capital_raids}</div>
                <div className="text-xs text-yellow-200 uppercase">Raids</div>
              </div>
              <div className="coc-stat-box">
                <div className="text-4xl font-bold text-green-400 mb-1">{dataStats.data_availability.days_of_data}</div>
                <div className="text-xs text-yellow-200 uppercase">Days</div>
              </div>
            </div>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {[
            { id: 'overview', label: '📋 Overview' },
            { id: 'leadership', label: '👑 Leadership' },
            { id: 'donations', label: '💎 Donations' },
            { id: 'capital', label: '🏰 Capital' },
            { id: 'fairness', label: '⚖️ Fairness' },
            { id: 'backend', label: '🔧 Backend' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`coc-tab px-6 py-3 rounded-t-lg font-bold transition-all whitespace-nowrap ${
                activeTab === tab.id ? 'active' : ''
              }`}
              data-testid={`tab-${tab.id}`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="animate-fade-in">
          {activeTab === 'overview' && <OverviewTab analyses={analyses} />}
          {activeTab === 'leadership' && <LeadershipTab data={analyses.leadership} />}
          {activeTab === 'donations' && <DonationsTab data={analyses.donations} />}
          {activeTab === 'capital' && <CapitalTab data={analyses.capital} />}
          {activeTab === 'fairness' && <FairnessTab data={analyses.fairness} />}
          {activeTab === 'backend' && <BackendFlowTab />}
        </div>
      </div>
    </div>
  );
};

// Overview Tab
const OverviewTab = ({ analyses }) => (
  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
    {/* Leadership Summary */}
    {analyses.leadership && !analyses.leadership.error && (
      <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-4">👑 Leadership Structure</h3>
        <div className="space-y-3">
          <div>
            <div className="text-sm text-blue-200">Type</div>
            <div className="text-xl font-bold text-blue-400 capitalize">
              {analyses.leadership.leadership_entropy?.leadership_type}
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Entropy Score</div>
            <div className="text-xl font-bold text-purple-400">
              {analyses.leadership.leadership_entropy?.entropy?.toFixed(2)} bits
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Top Leader</div>
            <div className="text-white">
              {analyses.leadership.top_leaders?.[0]?.player_name}
            </div>
          </div>
        </div>
      </div>
    )}

    {/* Donations Summary */}
    {analyses.donations && !analyses.donations.error && (
      <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-4">💰 Donation Economy</h3>
        <div className="space-y-3">
          <div>
            <div className="text-sm text-blue-200">Health Grade</div>
            <div className="text-4xl font-bold text-green-400">
              {analyses.donations.overall_health_score?.grade}
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Parasites Detected</div>
            <div className="text-xl font-bold text-red-400">
              {analyses.donations.parasites_detected}
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Reciprocity</div>
            <div className="text-white capitalize">
              {analyses.donations.reciprocity?.interpretation}
            </div>
          </div>
        </div>
      </div>
    )}

    {/* Capital Summary */}
    {analyses.capital && !analyses.capital.error && (
      <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-4">🏰 Capital Investment</h3>
        <div className="space-y-3">
          <div>
            <div className="text-sm text-blue-200">Free Riders</div>
            <div className="text-xl font-bold text-orange-400">
              {analyses.capital.free_riders?.count || 0}
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Inequality Status</div>
            <div className="text-white capitalize">
              {analyses.capital.inequality?.interpretation}
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Raids Analyzed</div>
            <div className="text-white">
              {analyses.capital.contribution_analysis?.raids_analyzed || 0}
            </div>
          </div>
        </div>
      </div>
    )}

    {/* Fairness Summary */}
    {analyses.fairness && !analyses.fairness.error && (
      <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-4">⚖️ Matchmaking Fairness</h3>
        <div className="space-y-3">
          <div>
            <div className="text-sm text-blue-200">Fairness Grade</div>
            <div className="text-4xl font-bold text-blue-400">
              {analyses.fairness.overall_grade?.grade}
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Win Rate</div>
            <div className="text-xl font-bold text-purple-400">
              {((analyses.fairness.win_rates?.all_wars?.win_rate || 0) * 100).toFixed(1)}%
            </div>
          </div>
          <div>
            <div className="text-sm text-blue-200">Wars Analyzed</div>
            <div className="text-white">
              {analyses.fairness.wars_analyzed || 0}
            </div>
          </div>
        </div>
      </div>
    )}

    {/* Module Status Cards */}
    <ModuleStatusCard
      title="Pressure Analysis"
      status="Needs War Data"
      description="Requires individual attack data"
    />
    <ModuleStatusCard
      title="Coordination Analysis"
      status="Needs War Data"
      description="Requires attack timing data"
    />
    <ModuleStatusCard
      title="Trophy Volatility"
      status="Collecting"
      description="Needs 30 days of player snapshots"
    />
  </div>
);

const ModuleStatusCard = ({ title, status, description }) => (
  <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
    <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
    <div className="text-yellow-400 font-semibold mb-2">{status}</div>
    <div className="text-blue-200 text-sm">{description}</div>
  </div>
);

// Other tabs implementations...
const LeadershipTab = ({ data }) => {
  if (!data || data.error) {
    return <div className="text-white">Error loading leadership data</div>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Top 10 Influential Leaders</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-white/5">
              <tr>
                <th className="text-left p-3 text-blue-200">Rank</th>
                <th className="text-left p-3 text-blue-200">Player</th>
                <th className="text-left p-3 text-blue-200">Influence</th>
                <th className="text-left p-3 text-blue-200">Role</th>
              </tr>
            </thead>
            <tbody>
              {data.top_leaders?.slice(0, 10).map((leader) => (
                <tr key={leader.rank} className="border-t border-white/10">
                  <td className="p-3 text-white font-bold">{leader.rank}</td>
                  <td className="p-3 text-white">{leader.player_name}</td>
                  <td className="p-3">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-white/10 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full"
                          style={{ width: `${leader.influence_score * 100}%` }}
                        />
                      </div>
                      <span className="text-white text-sm">{leader.influence_score.toFixed(3)}</span>
                    </div>
                  </td>
                  <td className="p-3 text-blue-200 capitalize">{leader.formal_role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const DonationsTab = ({ data }) => {
  if (!data || data.error) {
    return <div className="text-white">Error loading donation data</div>;
  }

  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
          <h3 className="text-xl font-bold text-white mb-4">Network Health</h3>
          <div className="text-6xl font-bold text-green-400 mb-2">
            {data.overall_health_score?.grade}
          </div>
          <div className="text-blue-200">{data.overall_health_score?.interpretation}</div>
        </div>
        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
          <h3 className="text-xl font-bold text-white mb-4">Top Contributors</h3>
          <div className="space-y-2">
            {data.top_contributors?.slice(0, 5).map((contributor, i) => (
              <div key={i} className="flex justify-between items-center">
                <span className="text-white">{contributor.player_name || `Player ${i + 1}`}</span>
                <span className="text-blue-400">{contributor.donations_given || 0}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const CapitalTab = ({ data }) => {
  if (!data || data.error) {
    return <div className="text-white">Error loading capital data</div>;
  }

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-4">Capital Investment Analysis</h2>
      <div className="space-y-4">
        <div>
          <div className="text-sm text-blue-200">Free Riders Detected</div>
          <div className="text-3xl font-bold text-orange-400">{data.free_riders?.count || 0}</div>
        </div>
        <div>
          <div className="text-sm text-blue-200">Contribution Inequality</div>
          <div className="text-xl text-white capitalize">{data.inequality?.interpretation}</div>
        </div>
      </div>
    </div>
  );
};

const FairnessTab = ({ data }) => {
  if (!data || data.error) {
    return <div className="text-white">Error loading fairness data</div>;
  }

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-4">Matchmaking Fairness Audit</h2>
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <div className="text-sm text-blue-200">Fairness Grade</div>
          <div className="text-6xl font-bold text-blue-400 mb-2">{data.overall_grade?.grade}</div>
          <div className="text-blue-200">{data.overall_grade?.description}</div>
        </div>
        <div>
          <div className="text-sm text-blue-200">Overall Win Rate</div>
          <div className="text-3xl font-bold text-purple-400">
            {((data.win_rates?.all_wars?.win_rate || 0) * 100).toFixed(1)}%
          </div>
          <div className="text-sm text-blue-200 mt-2">From {data.wars_analyzed} wars</div>
        </div>
      </div>
    </div>
  );
};

// Backend Flow Tab - Educational
const BackendFlowTab = () => (
  <div className="space-y-6">
    <div className="bg-gradient-to-br from-green-900/40 to-emerald-900/40 rounded-xl p-6 border border-green-500/30">
      <h2 className="text-2xl font-bold text-white mb-4">🔧 Backend Architecture & Workflow</h2>
      <p className="text-blue-200 mb-4">
        Learn how the ML pipeline works from data collection to analysis.
      </p>
    </div>

    {/* Workflow Steps */}
    {[
      {
        step: 1,
        title: 'Data Collection',
        file: 'data_collector.py',
        description: 'Background scheduler fetches data from CoC API every 6 hours',
        code: `async def run_collection_cycle():
    for clan_tag in tracked_clans:
        await collect_clan_snapshot(clan_tag)
        await collect_war_log(clan_tag)
        await collect_capital_raids(clan_tag)`
      },
      {
        step: 2,
        title: 'Data Storage',
        file: 'MongoDB Collections',
        description: 'Time-series data stored in MongoDB for historical analysis',
        code: `Collections:
- players_history (snapshots every 6h)
- clans_history (clan state over time)
- wars_history (war outcomes)
- war_attacks (individual attacks)
- capital_raids_history (weekend raids)`
      },
      {
        step: 3,
        title: 'Feature Engineering',
        file: 'feature_engineering.py',
        description: 'Extract statistical features from raw data',
        code: `def compute_trophy_momentum(snapshots):
    # Calculate velocity of trophy changes
    slope = (trophies[-1] - trophies[0]) / days
    return slope  # Positive = climbing`
      },
      {
        step: 4,
        title: 'ML Model Execution',
        file: 'ml_module_*.py',
        description: 'Each module processes features and generates insights',
        code: `def generate_report(data):
    # Extract features
    features = extract_features(data)
    
    # Apply ML algorithm
    results = model.predict(features)
    
    # Add interpretation
    return {
        'metrics': results,
        'interpretation': explain(results)
    }`
      },
      {
        step: 5,
        title: 'API Endpoint',
        file: 'server.py',
        description: 'FastAPI exposes results via REST endpoints',
        code: `@api_router.post("/ml/leadership/analyze")
async def analyze_leadership(request):
    # Check cache
    cached = await db.ml_results.find_one(...)
    if cached: return cached
    
    # Run model
    results = model.generate_report(data)
    
    # Cache for 24h
    await db.ml_results.insert_one({
        'valid_until': now + timedelta(hours=24),
        'results': results
    })`
      },
      {
        step: 6,
        title: 'Frontend Display',
        file: 'UnifiedDashboard.js',
        description: 'React fetches and displays results with visualizations',
        code: `const loadAnalysis = async () => {
    const response = await axios.post(
        '/api/ml/leadership/analyze',
        { clan_tag: '#YOUR_TAG' }
    );
    setData(response.data);
}`
      }
    ].map((workflow) => (
      <div key={workflow.step} className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
        <div className="flex items-start gap-4">
          <div className="bg-blue-500 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold flex-shrink-0">
            {workflow.step}
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold text-white mb-2">{workflow.title}</h3>
            <code className="text-yellow-300 text-sm">{workflow.file}</code>
            <p className="text-blue-200 mt-2 mb-3">{workflow.description}</p>
            <pre className="bg-black/40 p-3 rounded text-green-300 text-xs overflow-x-auto">
              <code>{workflow.code}</code>
            </pre>
          </div>
        </div>
      </div>
    ))}

    {/* File Structure */}
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
      <h3 className="text-xl font-bold text-white mb-4">📁 Backend File Structure</h3>
      <div className="bg-black/40 p-4 rounded font-mono text-sm text-green-300">
        <div>/app/backend/</div>
        <div>├── server.py              # FastAPI server (entry point)</div>
        <div>├── coc_api_client.py     # CoC API wrapper</div>
        <div>├── data_collector.py     # Background scheduler</div>
        <div>├── data_models.py        # Pydantic models</div>
        <div>├── feature_engineering.py # Feature extraction</div>
        <div>├── ml_module_1_leadership.py</div>
        <div>├── ml_module_2_pressure.py</div>
        <div>├── ml_module_3_coordination.py</div>
        <div>├── ml_module_4_volatility.py</div>
        <div>├── ml_module_5_donations.py</div>
        <div>├── ml_module_6_capital.py</div>
        <div>└── ml_module_7_fairness.py</div>
      </div>
    </div>
  </div>
);

export default UnifiedDashboard;