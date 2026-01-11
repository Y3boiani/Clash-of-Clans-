import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import {
  LeadershipNetwork,
  DonationFlowViz,
  CapitalInvestmentViz,
  FairnessScaleViz,
  TrophyVolatilityViz,
  CoordinationHeatmap,
  MiniStatViz
} from './MLVisualizations';

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
  <div className="space-y-8">
    {/* Quick Stats Row with Animations */}
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {analyses.leadership && !analyses.leadership.error && (
        <MiniStatViz 
          type="leadership" 
          value={analyses.leadership.leadership_entropy?.entropy || 0}
          label="Leadership Entropy"
          trend={analyses.leadership.leadership_entropy?.entropy > 2 ? 'up' : 'stable'}
        />
      )}
      {analyses.donations && !analyses.donations.error && (
        <MiniStatViz 
          type="donation" 
          value={analyses.donations.overall_health_score?.score || 0}
          label="Donation Health"
          trend="stable"
        />
      )}
      {analyses.capital && !analyses.capital.error && (
        <MiniStatViz 
          type="capital" 
          value={analyses.capital.contribution_analysis?.raids_analyzed || 0}
          label="Raids Analyzed"
          trend="up"
        />
      )}
      {analyses.fairness && !analyses.fairness.error && (
        <MiniStatViz 
          type="fairness" 
          value={(analyses.fairness.win_rates?.all_wars?.win_rate || 0) * 100}
          label="Win Rate %"
          trend={analyses.fairness.win_rates?.all_wars?.win_rate > 0.5 ? 'up' : 'down'}
        />
      )}
    </div>

    {/* Visualization Cards */}
    <div className="grid md:grid-cols-2 gap-6">
      {/* Leadership Visualization */}
      {analyses.leadership && !analyses.leadership.error && (
        <div className="coc-card p-6 border-4">
          <h3 className="text-2xl font-bold text-coc-gold mb-4 flex items-center gap-3">
            <span className="coc-icon text-xl">👑</span>
            Leadership Network
          </h3>
          <LeadershipNetwork 
            leaders={analyses.leadership.top_leaders || []}
            entropy={analyses.leadership.leadership_entropy?.entropy}
            leadershipType={analyses.leadership.leadership_entropy?.leadership_type}
          />
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-sm text-yellow-200">Structure</div>
              <div className="text-lg font-bold text-coc-gold capitalize">
                {analyses.leadership.leadership_entropy?.leadership_type}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-yellow-200">Top Leader</div>
              <div className="text-lg font-bold text-white">
                {analyses.leadership.top_leaders?.[0]?.player_name || 'N/A'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Donations Visualization */}
      {analyses.donations && !analyses.donations.error && (
        <div className="coc-card p-6 border-4">
          <h3 className="text-2xl font-bold text-coc-gold mb-4 flex items-center gap-3">
            <span className="coc-icon text-xl">💎</span>
            Donation Economy
          </h3>
          <DonationFlowViz 
            contributors={analyses.donations.top_contributors || []}
            parasites={analyses.donations.parasites_detected || 0}
            healthGrade={analyses.donations.overall_health_score?.grade || 'B'}
          />
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-sm text-yellow-200">Reciprocity</div>
              <div className="text-lg font-bold text-white capitalize">
                {analyses.donations.reciprocity?.interpretation || 'N/A'}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-yellow-200">Network Density</div>
              <div className="text-lg font-bold text-purple-400">
                {((analyses.donations.network_metrics?.density || 0) * 100).toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Capital Investment Visualization */}
      {analyses.capital && !analyses.capital.error && (
        <div className="coc-card p-6 border-4">
          <h3 className="text-2xl font-bold text-coc-gold mb-4 flex items-center gap-3">
            <span className="coc-icon text-xl">🏰</span>
            Capital Investment
          </h3>
          <CapitalInvestmentViz 
            freeRiders={analyses.capital.free_riders?.count || 0}
            inequality={analyses.capital.inequality?.interpretation || 'moderate'}
            raidsAnalyzed={analyses.capital.contribution_analysis?.raids_analyzed || 0}
          />
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-sm text-yellow-200">Gini Index</div>
              <div className="text-lg font-bold text-orange-400">
                {(analyses.capital.inequality?.gini_coefficient || 0).toFixed(3)}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-yellow-200">Avg Contribution</div>
              <div className="text-lg font-bold text-green-400">
                {Math.round(analyses.capital.contribution_analysis?.mean_contribution || 0)}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Fairness Visualization */}
      {analyses.fairness && !analyses.fairness.error && (
        <div className="coc-card p-6 border-4">
          <h3 className="text-2xl font-bold text-coc-gold mb-4 flex items-center gap-3">
            <span className="coc-icon text-xl">⚖️</span>
            Matchmaking Fairness
          </h3>
          <FairnessScaleViz 
            grade={analyses.fairness.overall_grade?.grade || 'B'}
            winRate={analyses.fairness.win_rates?.all_wars?.win_rate || 0.5}
            warsAnalyzed={analyses.fairness.wars_analyzed || 0}
          />
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-sm text-yellow-200">Bias Score</div>
              <div className="text-lg font-bold text-blue-400">
                {(analyses.fairness.strength_bias?.bias_score || 0).toFixed(2)}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-yellow-200">Description</div>
              <div className="text-sm font-bold text-white">
                {analyses.fairness.overall_grade?.description || 'N/A'}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>

    {/* Pending Modules Section */}
    <div className="coc-card p-6 border-4">
      <h3 className="text-2xl font-bold text-coc-gold mb-4 flex items-center gap-3">
        <span className="coc-icon text-xl">🔮</span>
        Coming Soon - Data Collection in Progress
      </h3>
      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-black/30 rounded-lg p-4 border border-amber-900/50">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-2xl">🎯</span>
            <div>
              <div className="font-bold text-yellow-100">Pressure Analysis</div>
              <div className="text-xs text-yellow-200">Module 2</div>
            </div>
          </div>
          <div className="text-sm text-yellow-200">Requires individual attack data from war logs</div>
          <div className="coc-progress-bar h-2 mt-3">
            <div className="coc-progress-fill" style={{ width: '30%' }}></div>
          </div>
        </div>
        
        <div className="bg-black/30 rounded-lg p-4 border border-amber-900/50">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-2xl">🤝</span>
            <div>
              <div className="font-bold text-yellow-100">Coordination Analysis</div>
              <div className="text-xs text-yellow-200">Module 3</div>
            </div>
          </div>
          <CoordinationHeatmap />
          <div className="text-xs text-yellow-200 mt-2">Preview: Attack timing patterns</div>
        </div>
        
        <div className="bg-black/30 rounded-lg p-4 border border-amber-900/50">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-2xl">🏆</span>
            <div>
              <div className="font-bold text-yellow-100">Trophy Volatility</div>
              <div className="text-xs text-yellow-200">Module 4</div>
            </div>
          </div>
          <TrophyVolatilityViz prediction="stable" />
          <div className="text-xs text-yellow-200 mt-2">Needs 30+ days of snapshots</div>
        </div>
      </div>
    </div>
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
      {/* Leadership Network Visualization */}
      <div className="coc-card p-6 border-4">
        <h2 className="text-2xl font-bold text-coc-gold mb-6 flex items-center gap-3">
          <span className="coc-icon text-xl">👑</span>
          Clan Hierarchy Visualization
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <LeadershipNetwork 
              leaders={data.top_leaders || []}
              entropy={data.leadership_entropy?.entropy}
              leadershipType={data.leadership_entropy?.leadership_type}
            />
          </div>
          <div className="space-y-4">
            <div className="bg-black/30 p-4 rounded-lg border border-amber-900/50">
              <h4 className="text-coc-gold font-bold mb-2">📊 What is Leadership Entropy?</h4>
              <p className="text-yellow-200 text-sm">
                Shannon Entropy measures how distributed power is in your clan. 
                Higher entropy = more shared leadership. Lower entropy = concentrated power.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-3xl font-bold text-coc-gold">{data.leadership_entropy?.entropy?.toFixed(2)}</div>
                <div className="text-xs text-yellow-200 uppercase">Entropy (bits)</div>
              </div>
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-3xl font-bold text-purple-400 capitalize">{data.leadership_entropy?.leadership_type}</div>
                <div className="text-xs text-yellow-200 uppercase">Structure Type</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Top Leaders Table */}
      <div className="coc-card p-6 border-4">
        <h2 className="text-2xl font-bold text-coc-gold mb-6">⚔️ Top 10 Influential Warriors</h2>
        <div className="overflow-x-auto">
          <table className="w-full coc-table">
            <thead>
              <tr>
                <th className="text-left p-3">Rank</th>
                <th className="text-left p-3">Warrior</th>
                <th className="text-left p-3">Influence Power</th>
                <th className="text-left p-3">Role</th>
              </tr>
            </thead>
            <tbody>
              {data.top_leaders?.slice(0, 10).map((leader) => (
                <tr key={leader.rank} className="border-t border-amber-900/30">
                  <td className="p-3">
                    <span className="coc-badge w-8 h-8 text-sm">
                      {leader.rank <= 3 ? ['🥇', '🥈', '🥉'][leader.rank - 1] : leader.rank}
                    </span>
                  </td>
                  <td className="p-3 text-yellow-100 font-bold">{leader.player_name}</td>
                  <td className="p-3">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 coc-progress-bar h-3">
                        <div
                          className="coc-progress-fill"
                          style={{ width: `${leader.influence_score * 100}%` }}
                        />
                      </div>
                      <span className="text-coc-gold text-sm font-bold">{(leader.influence_score * 100).toFixed(1)}%</span>
                    </div>
                  </td>
                  <td className="p-3 text-yellow-200 capitalize">{leader.formal_role}</td>
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
      {/* Donation Flow Visualization */}
      <div className="coc-card p-6 border-4">
        <h2 className="text-2xl font-bold text-coc-gold mb-6 flex items-center gap-3">
          <span className="coc-icon text-xl">💎</span>
          Resource Flow Analysis
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <DonationFlowViz 
              contributors={data.top_contributors || []}
              parasites={data.parasites_detected || 0}
              healthGrade={data.overall_health_score?.grade || 'B'}
            />
          </div>
          <div className="space-y-4">
            <div className="bg-black/30 p-4 rounded-lg border border-amber-900/50">
              <h4 className="text-coc-gold font-bold mb-2">📈 Network Health Explained</h4>
              <p className="text-yellow-200 text-sm">
                We analyze donation patterns using graph theory. Healthy clans have 
                balanced give-and-take relationships. Parasites take more than they give.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-5xl font-bold text-green-400">{data.overall_health_score?.grade}</div>
                <div className="text-xs text-yellow-200 uppercase">Health Grade</div>
              </div>
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-3xl font-bold text-red-400">{data.parasites_detected || 0}</div>
                <div className="text-xs text-yellow-200 uppercase">Parasites Found</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Top Contributors */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="coc-card p-6 border-4">
          <h3 className="text-xl font-bold text-coc-gold mb-4">🌟 Top Contributors</h3>
          <div className="space-y-3">
            {data.top_contributors?.slice(0, 5).map((contributor, i) => (
              <div key={i} className="flex justify-between items-center bg-black/20 p-3 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="coc-badge w-8 h-8 text-sm">{i + 1}</span>
                  <span className="text-yellow-100 font-bold">{contributor.player_name || `Player ${i + 1}`}</span>
                </div>
                <span className="text-coc-gold font-bold">{contributor.donations_given || 0} 💎</span>
              </div>
            ))}
          </div>
        </div>
        
        <div className="coc-card p-6 border-4">
          <h3 className="text-xl font-bold text-coc-gold mb-4">📊 Network Metrics</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Reciprocity</span>
              <span className="text-white capitalize font-bold">{data.reciprocity?.interpretation || 'N/A'}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Network Density</span>
              <span className="text-purple-400 font-bold">{((data.network_metrics?.density || 0) * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Gini Coefficient</span>
              <span className="text-orange-400 font-bold">{(data.inequality?.gini || 0).toFixed(3)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Total Flow</span>
              <span className="text-coc-gold font-bold">{data.network_metrics?.total_donations || 0}</span>
            </div>
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
    <div className="space-y-6">
      {/* Capital Investment Visualization */}
      <div className="coc-card p-6 border-4">
        <h2 className="text-2xl font-bold text-coc-gold mb-6 flex items-center gap-3">
          <span className="coc-icon text-xl">🏰</span>
          Clan Capital Analysis
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <CapitalInvestmentViz 
              freeRiders={data.free_riders?.count || 0}
              inequality={data.inequality?.interpretation || 'moderate'}
              raidsAnalyzed={data.contribution_analysis?.raids_analyzed || 0}
            />
          </div>
          <div className="space-y-4">
            <div className="bg-black/30 p-4 rounded-lg border border-amber-900/50">
              <h4 className="text-coc-gold font-bold mb-2">🎮 Public Goods Game Theory</h4>
              <p className="text-yellow-200 text-sm">
                Clan Capital is a classic public goods problem. We detect free-riders 
                (who benefit without contributing) using contribution thresholds and 
                Gini coefficient analysis.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-3xl font-bold text-orange-400">{data.free_riders?.count || 0}</div>
                <div className="text-xs text-yellow-200 uppercase">Free Riders</div>
              </div>
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-3xl font-bold text-coc-gold">{data.contribution_analysis?.raids_analyzed || 0}</div>
                <div className="text-xs text-yellow-200 uppercase">Raids Analyzed</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contribution Stats */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="coc-card p-6 border-4 text-center">
          <div className="text-4xl font-bold text-green-400 mb-2">
            {Math.round(data.contribution_analysis?.mean_contribution || 0)}
          </div>
          <div className="text-yellow-200">Average Contribution</div>
        </div>
        <div className="coc-card p-6 border-4 text-center">
          <div className="text-4xl font-bold text-purple-400 mb-2">
            {(data.inequality?.gini_coefficient || 0).toFixed(3)}
          </div>
          <div className="text-yellow-200">Gini Coefficient</div>
        </div>
        <div className="coc-card p-6 border-4 text-center">
          <div className="text-4xl font-bold capitalize" style={{ color: data.inequality?.interpretation === 'low' ? '#00ff00' : data.inequality?.interpretation === 'high' ? '#ff4500' : '#ffd700' }}>
            {data.inequality?.interpretation || 'N/A'}
          </div>
          <div className="text-yellow-200">Inequality Level</div>
        </div>
      </div>

      {/* Free Riders List */}
      {data.free_riders?.players && data.free_riders.players.length > 0 && (
        <div className="coc-card p-6 border-4">
          <h3 className="text-xl font-bold text-red-400 mb-4">⚠️ Detected Free Riders</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
            {data.free_riders.players.map((player, i) => (
              <div key={i} className="bg-red-900/20 p-3 rounded-lg border border-red-900/50 flex items-center gap-3">
                <span className="text-2xl">🦥</span>
                <div>
                  <div className="text-yellow-100 font-bold">{player.name || `Player ${i + 1}`}</div>
                  <div className="text-xs text-red-400">Contribution: {player.contribution || 0}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const FairnessTab = ({ data }) => {
  if (!data || data.error) {
    return <div className="text-white">Error loading fairness data</div>;
  }

  return (
    <div className="space-y-6">
      {/* Fairness Scale Visualization */}
      <div className="coc-card p-6 border-4">
        <h2 className="text-2xl font-bold text-coc-gold mb-6 flex items-center gap-3">
          <span className="coc-icon text-xl">⚖️</span>
          Matchmaking Fairness Audit
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <FairnessScaleViz 
              grade={data.overall_grade?.grade || 'B'}
              winRate={data.win_rates?.all_wars?.win_rate || 0.5}
              warsAnalyzed={data.wars_analyzed || 0}
            />
          </div>
          <div className="space-y-4">
            <div className="bg-black/30 p-4 rounded-lg border border-amber-900/50">
              <h4 className="text-coc-gold font-bold mb-2">📐 Fairness Metrics</h4>
              <p className="text-yellow-200 text-sm">
                We analyze matchmaking using demographic parity and propensity scores. 
                A balanced scale means fair matchups. Tilted = systematic advantage/disadvantage.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-5xl font-bold text-blue-400">{data.overall_grade?.grade}</div>
                <div className="text-xs text-yellow-200 uppercase">Fairness Grade</div>
              </div>
              <div className="bg-black/30 p-3 rounded-lg text-center">
                <div className="text-3xl font-bold text-purple-400">
                  {((data.win_rates?.all_wars?.win_rate || 0) * 100).toFixed(1)}%
                </div>
                <div className="text-xs text-yellow-200 uppercase">Overall Win Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Stats */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="coc-card p-6 border-4">
          <h3 className="text-xl font-bold text-coc-gold mb-4">📊 War Statistics</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Wars Analyzed</span>
              <span className="text-white font-bold">{data.wars_analyzed || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Wins</span>
              <span className="text-green-400 font-bold">{data.win_rates?.all_wars?.wins || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Losses</span>
              <span className="text-red-400 font-bold">{data.win_rates?.all_wars?.losses || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Draws</span>
              <span className="text-yellow-400 font-bold">{data.win_rates?.all_wars?.draws || 0}</span>
            </div>
          </div>
        </div>
        
        <div className="coc-card p-6 border-4">
          <h3 className="text-xl font-bold text-coc-gold mb-4">🎯 Bias Analysis</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Strength Bias Score</span>
              <span className="text-blue-400 font-bold">{(data.strength_bias?.bias_score || 0).toFixed(3)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-yellow-200">Bias Interpretation</span>
              <span className="text-white font-bold capitalize">{data.strength_bias?.interpretation || 'N/A'}</span>
            </div>
            <div className="coc-divider my-4"></div>
            <div className="text-center">
              <div className="text-sm text-yellow-200 mb-2">Grade Description</div>
              <div className="text-white">{data.overall_grade?.description || 'No assessment available'}</div>
            </div>
          </div>
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