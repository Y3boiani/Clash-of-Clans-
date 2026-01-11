'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import PlayerSearch from '@/components/PlayerSearch'

const API = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api`

const modules = [
  {
    num: 1,
    title: 'Leadership Entropy',
    desc: "Discover your clan's true leaders through behavioral analysis",
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
    desc: "Measure your clan's teamwork and strategic coordination",
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
]

export default function Home() {
  const router = useRouter()
  const [foundPlayer, setFoundPlayer] = useState<any>(null)
  const [systemIp, setSystemIp] = useState('Loading...')

  useEffect(() => {
    axios.get(`${API}/system/ip`).then(res => {
      setSystemIp(res.data.ip || 'Unknown')
    }).catch(() => setSystemIp('Unable to fetch'))
  }, [])

  const handlePlayerFound = (data: any) => {
    setFoundPlayer(data)
  }

  return (
    <div className="min-h-screen bg-coc-dark coc-wood-bg">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-coc-gold mb-4 gold-shine">
            ⚔️ CLASH OF CLANS ⚔️
            <span className="block text-4xl md:text-5xl mt-2">
              ML Research Platform
            </span>
          </h1>
          <p className="text-xl text-yellow-200 max-w-3xl mx-auto">
            Learn machine learning by analyzing YOUR clan&apos;s battle strategies
          </p>
        </div>

        {/* Player Found Card */}
        {foundPlayer && (
          <div className="coc-card p-8 mb-12 border-4 border-green-500 fade-in-up">
            <h2 className="text-3xl font-bold text-coc-gold mb-4 uppercase">🏆 Player Found!</h2>
            <p className="text-yellow-100 mb-6">
              <strong className="text-coc-gold">{foundPlayer.player?.name}</strong>
              {foundPlayer.clan && (
                <> from <strong className="text-coc-gold">{foundPlayer.clan?.name}</strong></>
              )}
              {' '}- Ready to analyze!
            </p>
            <div className="flex flex-wrap gap-4">
              {foundPlayer.clan && (
                <button
                  onClick={() => router.push(`/unified-dashboard?clan=${encodeURIComponent(foundPlayer.clan.tag)}`)}
                  className="coc-button px-8 py-4 text-lg"
                >
                  ⚔️ Analyze Clan (All 7 Models)
                </button>
              )}
              <button
                onClick={() => router.push('/dashboard')}
                className="coc-button px-8 py-4 text-lg bg-gradient-to-b from-green-500 to-green-700"
              >
                🎮 Demo Dashboard
              </button>
            </div>
          </div>
        )}

        {/* Player Search */}
        <PlayerSearch onPlayerFound={handlePlayerFound} />

        {/* API Key Setup Notice */}
        <div className="coc-card p-6 mb-12 border-2 border-yellow-500">
          <h3 className="text-xl font-bold text-coc-gold mb-3">🔑 API Key Setup Required</h3>
          <p className="text-yellow-200 text-sm mb-3">
            To search for players, your Clash of Clans API key must allow this server&apos;s IP address:
          </p>
          <div className="bg-black/50 p-3 rounded-lg mb-3">
            <code className="text-green-400 text-lg font-mono">{systemIp}</code>
          </div>
          <ol className="text-yellow-200 text-sm space-y-1 list-decimal list-inside">
            <li>Go to <a href="https://developer.clashofclans.com" target="_blank" rel="noreferrer" className="text-blue-400 underline">developer.clashofclans.com</a></li>
            <li>Edit your API key or create a new one</li>
            <li>Add the IP address shown above to the allowed IPs</li>
            <li>Update the COC_API_KEY in /app/backend/.env</li>
          </ol>
        </div>

        {/* ML Modules Grid */}
        <h2 className="text-4xl font-bold text-coc-gold mb-8 text-center uppercase">⚔️ 7 Battle Analysis Modules ⚔️</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {modules.map((module) => (
            <Link
              key={module.num}
              href={`/module/${module.num}`}
              className="coc-card p-6 module-card fade-in-up block"
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
            </Link>
          ))}
        </div>

        {/* Learning Path */}
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
  )
}
