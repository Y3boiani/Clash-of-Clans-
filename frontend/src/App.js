import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Main Landing Page
const Landing = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-purple-900 to-blue-950">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-4" data-testid="main-title">
            Clash of Clans
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
              ML Research Platform
            </span>
          </h1>
          <p className="text-xl text-blue-200 max-w-3xl mx-auto">
            Learn machine learning by reverse-engineering production-grade models
          </p>
        </div>

        {/* Quick Start */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-12 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-4">🚀 Quick Start</h2>
          <p className="text-blue-200 mb-6">
            Demo data is already loaded! Click below to explore ML models:
          </p>
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-4 rounded-xl font-semibold hover:shadow-xl hover:scale-105 transition-all"
            data-testid="explore-dashboard-btn"
          >
            Explore ML Dashboard →
          </button>
        </div>

        {/* ML Modules Grid */}
        <h2 className="text-3xl font-bold text-white mb-8 text-center">7 Research Modules</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {[
            {
              num: 1,
              title: 'Leadership Entropy',
              desc: 'Infer latent leadership structures from behavior',
              concepts: ['Shannon Entropy', 'Network Analysis', 'Bayesian Models'],
              color: 'from-blue-500 to-cyan-500'
            },
            {
              num: 2,
              title: 'Pressure Function',
              desc: 'Model performance under situational pressure',
              concepts: ['Gaussian Processes', 'Variance Modeling', 'Beta Distribution'],
              color: 'from-purple-500 to-pink-500'
            },
            {
              num: 3,
              title: 'Coordination Analysis',
              desc: 'Detect strategic coordination patterns',
              concepts: ['Point Processes', 'Hidden Markov Models', 'Motif Detection'],
              color: 'from-green-500 to-emerald-500'
            },
            {
              num: 4,
              title: 'Trophy Volatility',
              desc: 'Stochastic process modeling of rank dynamics',
              concepts: ['Ornstein-Uhlenbeck', 'Monte Carlo', 'Kalman Filtering'],
              color: 'from-orange-500 to-red-500'
            },
            {
              num: 5,
              title: 'Donation Networks',
              desc: 'Economic graph theory and resource flows',
              concepts: ['Graph Analytics', 'Gini Coefficient', 'PageRank'],
              color: 'from-yellow-500 to-orange-500'
            },
            {
              num: 6,
              title: 'Capital Investment',
              desc: 'Game theory and collective action problems',
              concepts: ['Public Goods Game', 'Causal Inference', 'Free-Rider Detection'],
              color: 'from-indigo-500 to-purple-500'
            },
            {
              num: 7,
              title: 'Matchmaking Fairness',
              desc: 'Algorithmic bias detection and fairness audit',
              concepts: ['Demographic Parity', 'Propensity Scores', 'A/B Testing'],
              color: 'from-pink-500 to-rose-500'
            }
          ].map((module) => (
            <div
              key={module.num}
              className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 hover:border-white/40 transition-all hover:scale-105 cursor-pointer"
              onClick={() => navigate(`/module/${module.num}`)}
              data-testid={`module-${module.num}-card`}
            >
              <div className={`text-3xl font-bold bg-gradient-to-r ${module.color} text-transparent bg-clip-text mb-2`}>
                Module {module.num}
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{module.title}</h3>
              <p className="text-blue-200 text-sm mb-4">{module.desc}</p>
              <div className="flex flex-wrap gap-2">
                {module.concepts.map((concept, idx) => (
                  <span key={idx} className="text-xs bg-white/20 px-2 py-1 rounded text-white">
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Learning Path */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-4">📚 Recommended Learning Path</h2>
          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="bg-green-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">1</div>
              <div>
                <div className="text-white font-semibold">Beginners: Start with Module 5 (Donations)</div>
                <div className="text-blue-200 text-sm">Most intuitive - learn graphs, Gini coefficient, network analysis</div>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">2</div>
              <div>
                <div className="text-white font-semibold">Intermediate: Module 4 (Volatility)</div>
                <div className="text-blue-200 text-sm">Stochastic processes, forecasting, Monte Carlo simulation</div>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="bg-purple-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">3</div>
              <div>
                <div className="text-white font-semibold">Advanced: Module 7 (Fairness)</div>
                <div className="text-blue-200 text-sm">Causal inference, bias detection, algorithmic fairness</div>
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
        <Route path="/module/:id" element={<ModuleDetailWrapper />} />
      </Routes>
    </BrowserRouter>
  );
}

const ModuleDetailWrapper = () => {
  const { id } = require('react-router-dom').useParams();
  return <ModuleDetail moduleNum={parseInt(id)} />;
};

export default App;