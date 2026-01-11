'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import axios from 'axios'

const API = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api`

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const clanTag = '#DEMO001'

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API}/ml/dashboard/${encodeURIComponent(clanTag)}`)
      setData(response.data)
      setError(null)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-coc-dark coc-wood-bg flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mb-4 mx-auto"></div>
          <div className="text-coc-gold text-xl">Loading ML analyses...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-coc-dark coc-wood-bg flex items-center justify-center">
        <div className="coc-card p-8 text-center">
          <div className="text-red-400 text-xl mb-4">Error: {error}</div>
          <Link href="/" className="coc-button px-6 py-3">
            Return Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-coc-dark coc-wood-bg">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-4xl font-bold text-coc-gold mb-2 gold-shine">ML Analysis Dashboard</h1>
            <p className="text-yellow-200">Clan: {clanTag}</p>
          </div>
          <Link href="/" className="text-coc-gold hover:text-yellow-300">← Back to Home</Link>
        </div>

        {/* Data Stats */}
        <div className="coc-card p-6 mb-8">
          <h2 className="text-xl font-bold text-coc-gold mb-4">Data Availability</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="coc-stat-box">
              <div className="text-3xl font-bold text-blue-400">{data?.data_stats?.data_availability?.player_snapshots}</div>
              <div className="text-sm text-yellow-200">Player Snapshots</div>
            </div>
            <div className="coc-stat-box">
              <div className="text-3xl font-bold text-purple-400">{data?.data_stats?.data_availability?.wars}</div>
              <div className="text-sm text-yellow-200">Wars</div>
            </div>
            <div className="coc-stat-box">
              <div className="text-3xl font-bold text-green-400">{data?.data_stats?.data_availability?.war_attacks}</div>
              <div className="text-sm text-yellow-200">Attacks</div>
            </div>
            <div className="coc-stat-box">
              <div className="text-3xl font-bold text-orange-400">{data?.data_stats?.data_availability?.days_of_data}</div>
              <div className="text-sm text-yellow-200">Days of Data</div>
            </div>
          </div>
        </div>

        {/* Analysis Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          {data?.analyses?.leadership && (
            <div className="coc-card p-6">
              <h3 className="text-2xl font-bold text-coc-gold mb-4">🏛️ Leadership Entropy</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-yellow-200">Leadership Type</div>
                  <div className="text-xl font-bold text-blue-400 uppercase">
                    {data.analyses.leadership.leadership_entropy?.leadership_type}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-yellow-200">Entropy Score</div>
                  <div className="text-xl font-bold text-purple-400">
                    {data.analyses.leadership.leadership_entropy?.entropy?.toFixed(2)}
                  </div>
                </div>
              </div>
              <Link href="/module/1" className="mt-4 inline-block text-coc-gold hover:text-yellow-300">
                View Details →
              </Link>
            </div>
          )}

          {data?.analyses?.donations && (
            <div className="coc-card p-6">
              <h3 className="text-2xl font-bold text-coc-gold mb-4">💰 Donation Network</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-yellow-200">Health Grade</div>
                  <div className="text-3xl font-bold text-green-400">
                    {data.analyses.donations.overall_health_score?.grade}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-yellow-200">Parasites Detected</div>
                  <div className="text-xl font-bold text-red-400">
                    {data.analyses.donations.parasites_detected}
                  </div>
                </div>
              </div>
              <Link href="/module/5" className="mt-4 inline-block text-coc-gold hover:text-yellow-300">
                View Details →
              </Link>
            </div>
          )}

          {data?.analyses?.capital && (
            <div className="coc-card p-6">
              <h3 className="text-2xl font-bold text-coc-gold mb-4">🏰 Capital Investment</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-yellow-200">Free Riders</div>
                  <div className="text-xl font-bold text-orange-400">
                    {data.analyses.capital.free_riders?.count}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-yellow-200">Inequality Status</div>
                  <div className="text-white uppercase">
                    {data.analyses.capital.inequality?.interpretation}
                  </div>
                </div>
              </div>
              <Link href="/module/6" className="mt-4 inline-block text-coc-gold hover:text-yellow-300">
                View Details →
              </Link>
            </div>
          )}

          {data?.analyses?.fairness && (
            <div className="coc-card p-6">
              <h3 className="text-2xl font-bold text-coc-gold mb-4">⚖️ Matchmaking Fairness</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-yellow-200">Fairness Grade</div>
                  <div className="text-3xl font-bold text-blue-400">
                    {data.analyses.fairness.overall_grade?.grade}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-yellow-200">Win Rate</div>
                  <div className="text-xl font-bold text-purple-400">
                    {((data.analyses.fairness.win_rates?.all_wars?.win_rate || 0) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
              <Link href="/module/7" className="mt-4 inline-block text-coc-gold hover:text-yellow-300">
                View Details →
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
