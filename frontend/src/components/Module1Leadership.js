import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import {
  LearningObjectives,
  FormulaCard,
  MetricCard,
  ConceptExplainer,
  CodeWalkthrough,
  QuickQuiz,
  FileReference,
  ChartPlaceholder
} from './EducationalComponents';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const Module1Leadership = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await axios.post(`${API}/ml/leadership/analyze`, {
        clan_tag: '#DEMO001'
      });
      setData(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-white">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-purple-900 to-blue-950">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <Link to="/dashboard" className="text-blue-300 hover:text-blue-100 mb-4 inline-block">
            ← Back to Dashboard
          </Link>
          <h1 className="text-5xl font-bold text-white mb-4" data-testid="module1-title">
            Module 1: Leadership Entropy
          </h1>
          <p className="text-xl text-blue-200">
            Using information theory to infer organizational structure from behavioral data
          </p>
        </div>

        {/* Learning Objectives */}
        <LearningObjectives
          objectives={[
            'Understand Shannon entropy and its application to organizations',
            'Learn how to extract behavioral signals from time-series data',
            'Apply graph centrality measures to identify influential members',
            'Use Gini coefficient to measure authority concentration',
            'Implement multi-signal weighted scoring models'
          ]}
        />

        {/* Key Concepts */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">💡 Key Concepts</h2>
          
          <ConceptExplainer
            concept="Shannon Entropy"
            simpleExplanation="Entropy measures how 'spread out' or 'concentrated' something is. Low entropy = one person does everything. High entropy = many people share responsibility equally."
            technicalExplanation="Shannon entropy H = -Σ(p_i * log(p_i)) where p_i is the probability (proportion) of influence held by member i. Maximum entropy occurs when all members have equal influence."
            realWorldAnalogy="Think of entropy like measuring how a pizza is shared. If one person eats 90% (low entropy), it's concentrated. If 10 people each eat 10% (high entropy), it's distributed evenly."
          />

          <ConceptExplainer
            concept="Gini Coefficient"
            simpleExplanation="The Gini coefficient measures inequality. 0 = perfect equality (everyone has the same), 1 = perfect inequality (one person has everything)."
            technicalExplanation="A statistical measure of dispersion from economics. For influence distribution, Gini = (2 * Σ(i * x_i)) / (n * Σx_i) - (n+1)/n where x_i is sorted influence scores."
            realWorldAnalogy="Used to measure wealth inequality in countries. If Gini is high in your clan, a few players carry all the burden (like wealth concentration)."
          />
        </div>

        {/* Results */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">📈 Analysis Results</h2>
          
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <MetricCard
              label="Leadership Type"
              value={data?.leadership_entropy?.leadership_type || 'N/A'}
              unit=""
              color="blue"
              interpretation={data?.leadership_entropy?.interpretation}
            />
            <MetricCard
              label="Entropy Score"
              value={(data?.leadership_entropy?.entropy || 0).toFixed(2)}
              unit=" bits"
              color="purple"
              interpretation="Higher = more distributed"
            />
            <MetricCard
              label="Gini Coefficient"
              value={(data?.leadership_entropy?.gini_coefficient || 0).toFixed(2)}
              unit=""
              color="orange"
              interpretation="Lower = more equal"
            />
            <MetricCard
              label="Normalized Entropy"
              value={((data?.leadership_entropy?.normalized_entropy || 0) * 100).toFixed(0)}
              unit="%"
              color="green"
              interpretation="Percentage of max possible"
            />
          </div>

          <ChartPlaceholder
            title="Leadership Distribution Visualization"
            description="Would show entropy over time and influence distribution"
          />
        </div>

        {/* Top Leaders */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">🏆 Top Leaders by Influence</h2>
          <div className="bg-white/10 backdrop-blur-lg rounded-xl border border-white/20 overflow-hidden">
            <table className="w-full">
              <thead className="bg-white/5">
                <tr>
                  <th className="text-left p-4 text-blue-200">Rank</th>
                  <th className="text-left p-4 text-blue-200">Player</th>
                  <th className="text-left p-4 text-blue-200">Influence Score</th>
                  <th className="text-left p-4 text-blue-200">Formal Role</th>
                </tr>
              </thead>
              <tbody>
                {data?.top_leaders?.slice(0, 10).map((leader) => (
                  <tr key={leader.rank} className="border-t border-white/10">
                    <td className="p-4 text-white font-bold">{leader.rank}</td>
                    <td className="p-4 text-white">{leader.player_name}</td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-white/10 rounded-full h-2 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-full"
                            style={{ width: `${leader.influence_score * 100}%` }}
                          />
                        </div>
                        <span className="text-white text-sm">{leader.influence_score.toFixed(3)}</span>
                      </div>
                    </td>
                    <td className="p-4 text-blue-200 capitalize">{leader.formal_role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quiz */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">🧠 Test Your Understanding</h2>
          <QuickQuiz
            question="What does it mean when a clan has HIGH entropy (e.g., 4.5 bits) in their leadership structure?"
            options={[
              'One leader dominates all decisions',
              'Leadership is distributed among many members equally',
              'The clan is disorganized and chaotic',
              'The data is insufficient for analysis'
            ]}
            correctAnswer={1}
            explanation="High entropy means the 'information' or 'decision-making power' is spread out. This indicates democratic, distributed leadership where many members contribute equally to clan activities."
          />
        </div>

        {/* File References */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">📁 Source Code Reference</h2>
          <FileReference
            filename="/backend/ml_module_1_leadership.py"
            description="Main implementation of the leadership entropy model"
            keyFunctions={[
              'compute_leadership_influence_scores()',
              'compute_organizational_entropy()',
              '_compute_behavioral_signals()',
              '_compute_gini()'
            ]}
          />
        </div>

        {/* Next Steps */}
        <div className="bg-gradient-to-r from-blue-900/40 to-purple-900/40 rounded-xl p-6 border border-blue-500/30">
          <h3 className="text-white font-bold mb-3">➡️ Next Steps</h3>
          <ul className="space-y-2 text-blue-200">
            <li>• Open <code className="text-yellow-300">/backend/ml_module_1_leadership.py</code> and read the code</li>
            <li>• Try modifying the weight coefficients</li>
            <li>• Experiment with different entropy thresholds</li>
            <li>• Move on to Module 5 (Donation Networks) for graph analytics</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Module1Leadership;