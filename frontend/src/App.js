import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import PlayerSearch from './components/PlayerSearch';
import UnifiedDashboard from './components/UnifiedDashboard';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Main Landing Page
const Landing = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-coc-dark coc-wood-bg">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header with CoC styling */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-coc-gold mb-4 gold-shine" data-testid="main-title">
            ⚔️ CLASH OF CLANS ⚔️
            <span className="block text-5xl mt-2">
              ML Research Platform
            </span>
          </h1>
          <p className="text-xl text-yellow-200 max-w-3xl mx-auto">
            Learn machine learning by analyzing YOUR clan's battle strategies
          </p>
        </div>

        {/* Quick Start with CoC cards */}
        <div className="coc-card p-8 mb-12">
          <h2 className="text-3xl font-bold text-coc-gold mb-4 uppercase">🏆 Your Clan is Ready</h2>
          <p className="text-yellow-100 mb-6">
            <strong className="text-coc-gold">Arceus</strong> from <strong className="text-coc-gold">Mystic Legions</strong> - Your data is being analyzed!
          </p>
          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => navigate('/unified-dashboard')}
              className="coc-button px-8 py-4 text-lg"
              data-testid="unified-dashboard-btn"
            >
              ⚔️ Battle Analysis (All 7 Models)
            </button>
            <button
              onClick={() => navigate('/dashboard')}
              className="coc-button px-8 py-4 text-lg bg-gradient-to-b from-green-500 to-green-700"
              data-testid="explore-dashboard-btn"
            >
              🎮 Demo Dashboard
            </button>
          </div>
        </div>

        {/* Player Search */}
        <PlayerSearch />

        {/* ML Modules Grid with CoC styling */}
        <h2 className="text-4xl font-bold text-coc-gold mb-8 text-center uppercase">⚔️ 7 Battle Analysis Modules ⚔️</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {[
            {
              num: 1,
              title: 'Leadership Entropy',
              desc: 'Discover your clan\'s true leaders through behavioral analysis',
              concepts: ['Shannon Entropy', 'Network Analysis', 'Bayesian Models'],
              icon: '👑',
              color: 'from-yellow-600 to-yellow-800'
            },
            {
              num: 2,
              title: 'Pressure Function',
              desc: 'Who performs under pressure? Find your clutch players',
              concepts: ['Gaussian Processes', 'Variance Modeling', 'Beta Distribution'],
              icon: '🎯',
              color: 'from-red-600 to-red-800'
            },
            {
              num: 3,
              title: 'Coordination Analysis',
              desc: 'Measure your clan\'s teamwork and strategic coordination',
              concepts: ['Point Processes', 'Hidden Markov Models', 'Motif Detection'],
              icon: '🤝',
              color: 'from-green-600 to-green-800'
            },
            {
              num: 4,
              title: 'Trophy Volatility',
              desc: 'Predict trophy trajectories and identify tilt patterns',
              concepts: ['Ornstein-Uhlenbeck', 'Monte Carlo', 'Kalman Filtering'],
              icon: '🏆',
              color: 'from-orange-600 to-orange-800'
            },
            {
              num: 5,
              title: 'Donation Networks',
              desc: 'Visualize resource flows and detect free-riders',
              concepts: ['Graph Analytics', 'Gini Coefficient', 'PageRank'],
              icon: '💎',
              color: 'from-purple-600 to-purple-800'
            },
            {
              num: 6,
              title: 'Capital Investment',
              desc: 'Analyze raid weekend contributions and predict success',
              concepts: ['Public Goods Game', 'Causal Inference', 'Free-Rider Detection'],
              icon: '🏰',
              color: 'from-blue-600 to-blue-800'
            },
            {
              num: 7,
              title: 'Matchmaking Fairness',
              desc: 'Audit war matchmaking for systematic biases',
              concepts: ['Demographic Parity', 'Propensity Scores', 'A/B Testing'],
              icon: '⚖️',
              color: 'from-pink-600 to-pink-800'
            }
          ].map((module) => (
            <div
              key={module.num}
              className="coc-card p-6 module-card fade-in-up"
              onClick={() => navigate(`/module/${module.num}`)}
              data-testid={`module-${module.num}-card`}
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="coc-badge w-16 h-16 text-3xl">
                  {module.icon}
                </div>
                <div>
                  <div className="text-2xl font-bold text-coc-gold">
                    Module {module.num}
                  </div>
                  <h3 className="text-lg font-bold text-yellow-100">{module.title}</h3>
                </div>
              </div>
              <p className="text-yellow-200 text-sm mb-4">{module.desc}</p>
              <div className="flex flex-wrap gap-2">
                {module.concepts.map((concept, idx) => (
                  <span key={idx} className="text-xs bg-gradient-to-r from-amber-900 to-amber-800 px-3 py-1 rounded-full text-yellow-100 border border-amber-700">
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Learning Path with CoC styling */}
        <div className="coc-card p-8 border-4">
          <h2 className="text-3xl font-bold text-coc-gold mb-6 uppercase flex items-center gap-3">
            <span className="coc-badge w-12 h-12 text-2xl">📚</span>
            Training Path
          </h2>
          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="coc-badge w-16 h-16 flex-shrink-0">
                <span className="text-2xl font-bold text-coc-gold">1</span>
              </div>
              <div className="flex-1">
                <div className="text-yellow-100 font-bold text-lg mb-1">🎯 Recruit: Start with Module 5 (Donations)</div>
                <div className="text-yellow-200 text-sm">Learn graphs, Gini coefficient, network analysis - perfect for beginners</div>
                <div className="coc-progress-bar h-2 mt-2">
                  <div className="coc-progress-fill" style={{ width: '100%' }}></div>
                </div>
              </div>
            </div>
            <div className="coc-divider"></div>
            <div className="flex items-start gap-4">
              <div className="coc-badge w-16 h-16 flex-shrink-0">
                <span className="text-2xl font-bold text-coc-gold">2</span>
              </div>
              <div className="flex-1">
                <div className="text-yellow-100 font-bold text-lg mb-1">⚔️ Warrior: Module 4 (Volatility)</div>
                <div className="text-yellow-200 text-sm">Stochastic processes, forecasting, Monte Carlo - intermediate level</div>
                <div className="coc-progress-bar h-2 mt-2">
                  <div className="coc-progress-fill bg-gradient-to-r from-yellow-400 to-yellow-600" style={{ width: '60%' }}></div>
                </div>
              </div>
            </div>
            <div className="coc-divider"></div>
            <div className="flex items-start gap-4">
              <div className="coc-badge w-16 h-16 flex-shrink-0">
                <span className="text-2xl font-bold text-coc-gold">3</span>
              </div>
              <div className="flex-1">
                <div className="text-yellow-100 font-bold text-lg mb-1">🏆 Champion: Module 7 (Fairness)</div>
                <div className="text-yellow-200 text-sm">Causal inference, bias detection - master level</div>
                <div className="coc-progress-bar h-2 mt-2">
                  <div className="coc-progress-fill bg-gradient-to-r from-purple-400 to-purple-600" style={{ width: '30%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Dashboard with all analyses
const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const clanTag = '#DEMO001';

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/ml/dashboard/${encodeURIComponent(clanTag)}`);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-950 via-purple-900 to-blue-950 flex items-center justify-center">
        <div className="text-white text-xl">Loading ML analyses...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-950 via-purple-900 to-blue-950 flex items-center justify-center">
        <div className="text-red-400">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-purple-900 to-blue-950">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2" data-testid="dashboard-title">ML Analysis Dashboard</h1>
            <p className="text-blue-200">Clan: {clanTag}</p>
          </div>
          <Link to="/" className="text-blue-300 hover:text-blue-100">← Back to Home</Link>
        </div>

        {/* Data Stats */}
        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 mb-8 border border-white/20">
          <h2 className="text-xl font-bold text-white mb-4">Data Availability</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-3xl font-bold text-blue-400">{data?.data_stats?.data_availability?.player_snapshots}</div>
              <div className="text-sm text-blue-200">Player Snapshots</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-400">{data?.data_stats?.data_availability?.wars}</div>
              <div className="text-sm text-blue-200">Wars</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-400">{data?.data_stats?.data_availability?.war_attacks}</div>
              <div className="text-sm text-blue-200">Attacks</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-400">{data?.data_stats?.data_availability?.days_of_data}</div>
              <div className="text-sm text-blue-200">Days of Data</div>
            </div>
          </div>
        </div>

        {/* Analysis Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Leadership */}
          {data?.analyses?.leadership && (
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-2xl font-bold text-white mb-4">🏛️ Leadership Entropy</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-blue-200">Leadership Type</div>
                  <div className="text-xl font-bold text-blue-400">
                    {data.analyses.leadership.leadership_entropy.leadership_type.toUpperCase()}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-blue-200">Entropy Score</div>
                  <div className="text-xl font-bold text-purple-400">
                    {data.analyses.leadership.leadership_entropy.entropy.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-blue-200">Top Leader</div>
                  <div className="text-white">
                    {data.analyses.leadership.top_leaders[0]?.player_name} 
                    ({data.analyses.leadership.top_leaders[0]?.influence_score.toFixed(2)})
                  </div>
                </div>
              </div>
              <Link to="/module/1" className="mt-4 inline-block text-blue-300 hover:text-blue-100">
                View Details →
              </Link>
            </div>
          )}

          {/* Donations */}
          {data?.analyses?.donations && (
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-2xl font-bold text-white mb-4">💰 Donation Network</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-blue-200">Health Grade</div>
                  <div className="text-3xl font-bold text-green-400">
                    {data.analyses.donations.overall_health_score.grade}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-blue-200">Parasites Detected</div>
                  <div className="text-xl font-bold text-red-400">
                    {data.analyses.donations.parasites_detected}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-blue-200">Reciprocity</div>
                  <div className="text-white">
                    {data.analyses.donations.reciprocity.interpretation.toUpperCase()}
                  </div>
                </div>
              </div>
              <Link to="/module/5" className="mt-4 inline-block text-blue-300 hover:text-blue-100">
                View Details →
              </Link>
            </div>
          )}

          {/* Capital */}
          {data?.analyses?.capital && (
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-2xl font-bold text-white mb-4">🏰 Capital Investment</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-blue-200">Free Riders</div>
                  <div className="text-xl font-bold text-orange-400">
                    {data.analyses.capital.free_riders.count}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-blue-200">Inequality Status</div>
                  <div className="text-white">
                    {data.analyses.capital.inequality.interpretation.toUpperCase()}
                  </div>
                </div>
              </div>
              <Link to="/module/6" className="mt-4 inline-block text-blue-300 hover:text-blue-100">
                View Details →
              </Link>
            </div>
          )}

          {/* Fairness */}
          {data?.analyses?.fairness && (
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-2xl font-bold text-white mb-4">⚖️ Matchmaking Fairness</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-blue-200">Fairness Grade</div>
                  <div className="text-3xl font-bold text-blue-400">
                    {data.analyses.fairness.overall_grade.grade}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-blue-200">Win Rate</div>
                  <div className="text-xl font-bold text-purple-400">
                    {(data.analyses.fairness.win_rates.all_wars.win_rate * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
              <Link to="/module/7" className="mt-4 inline-block text-blue-300 hover:text-blue-100">
                View Details →
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Module Detail Page - Route to specific module components
const ModuleDetail = ({ moduleNum }) => {
  // Import the educational module component
  const Module1 = require('./components/Module1Leadership').default;
  
  // Route to appropriate module
  if (moduleNum === 1) {
    return <Module1 />;
  }
  
  // For other modules, show coming soon
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-purple-900 to-blue-950">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center">
          <Link to="/dashboard" className="text-blue-300 hover:text-blue-100 mb-8 inline-block">← Back to Dashboard</Link>
          <h1 className="text-5xl font-bold text-white mb-4">Module {moduleNum}</h1>
          <p className="text-xl text-blue-200 mb-8">
            Detailed educational content for this module is being prepared!
          </p>
          <p className="text-blue-300 mb-4">
            For now, you can explore the source code at:
          </p>
          <code className="text-yellow-300 bg-black/30 px-4 py-2 rounded">
            /app/backend/ml_module_{moduleNum}_*.py
          </code>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/unified-dashboard" element={<UnifiedDashboard />} />
        <Route path="/module/:id" element={<ModuleDetailWrapper />} />
      </Routes>
    </BrowserRouter>
  );
}

const ModuleDetailWrapper = () => {
  const { id } = useParams();
  return <ModuleDetail moduleNum={parseInt(id)} />;
};

export default App;