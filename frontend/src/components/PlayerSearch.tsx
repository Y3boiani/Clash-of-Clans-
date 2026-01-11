'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

const API = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api`

interface PlayerData {
  player: {
    name: string
    tag: string
    townHallLevel: number
    trophies: number
    warStars: number
    donations: number
  }
  clan?: {
    name: string
    tag: string
    clanLevel: number
    members: number
    warWins: number
    warWinStreak: number
  }
}

interface PlayerSearchProps {
  onPlayerFound?: (data: PlayerData) => void
}

export default function PlayerSearch({ onPlayerFound }: PlayerSearchProps) {
  const [playerTag, setPlayerTag] = useState('')
  const [loading, setLoading] = useState(false)
  const [playerData, setPlayerData] = useState<PlayerData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const searchPlayer = async () => {
    if (!playerTag.trim()) {
      setError('Please enter a player tag')
      return
    }

    setLoading(true)
    setError(null)
    setPlayerData(null)

    try {
      let formattedTag = playerTag.trim().toUpperCase()
      if (!formattedTag.startsWith('#')) {
        formattedTag = '#' + formattedTag
      }
      const encodedTag = formattedTag.replace('#', '%23')

      const response = await axios.get(`${API}/player/${encodedTag}`)
      
      setPlayerData(response.data)
      
      if (onPlayerFound) {
        onPlayerFound(response.data)
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message
      
      if (err.response?.status === 404) {
        setError(`❌ Player not found: "${playerTag}"\n\nMake sure you entered the correct player tag (starts with #).`)
      } else if (errorMsg.includes('API') || errorMsg.includes('COC_API_KEY')) {
        setError(`⚠️ API Configuration Issue: ${errorMsg}`)
      } else {
        setError(`Error: ${errorMsg}`)
      }
    } finally {
      setLoading(false)
    }
  }

  const goToDashboard = () => {
    if (playerData?.clan?.tag) {
      router.push(`/unified-dashboard?clan=${encodeURIComponent(playerData.clan.tag)}`)
    }
  }

  return (
    <div className="coc-card p-8 border-4 mb-8">
      <h2 className="text-3xl font-bold text-coc-gold mb-4 uppercase flex items-center gap-3">
        <span className="coc-badge w-12 h-12 text-2xl">🔍</span>
        Scout Your Account
      </h2>
      
      <div className="mb-6">
        <label className="block text-yellow-100 mb-2 font-semibold">Enter Player Tag</label>
        <div className="flex gap-2">
          <input
            type="text"
            value={playerTag}
            onChange={(e) => setPlayerTag(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchPlayer()}
            placeholder="e.g., #2YJ2URLQJ"
            className="flex-1 coc-input"
          />
          <button
            onClick={searchPlayer}
            disabled={loading}
            className="coc-button px-8 py-3"
          >
            {loading ? '⏳ Scouting...' : '🔍 Search'}
          </button>
        </div>
      </div>

      {error && (
        <div className="coc-alert coc-alert-error mb-4">
          <div className="font-bold mb-2">⚠️ Scout Report</div>
          <div className="whitespace-pre-line text-sm">{error}</div>
        </div>
      )}

      {playerData && (
        <div className="coc-alert coc-alert-success">
          <div className="font-bold mb-3">✅ Player Found!</div>
          <div className="grid md:grid-cols-2 gap-4">
            {/* Player Info */}
            <div className="bg-black/20 rounded-lg p-4">
              <h4 className="text-coc-gold font-bold mb-2 flex items-center gap-2">
                ⚔️ {playerData.player?.name}
              </h4>
              <div className="text-sm space-y-1 text-yellow-200">
                <div>🏠 Town Hall: <span className="text-white">{playerData.player?.townHallLevel}</span></div>
                <div>🏆 Trophies: <span className="text-white">{playerData.player?.trophies}</span></div>
                <div>⭐ War Stars: <span className="text-white">{playerData.player?.warStars}</span></div>
                <div>💎 Donations: <span className="text-white">{playerData.player?.donations}</span></div>
              </div>
            </div>
            
            {/* Clan Info */}
            {playerData.clan ? (
              <div className="bg-black/20 rounded-lg p-4">
                <h4 className="text-coc-gold font-bold mb-2 flex items-center gap-2">
                  🏰 {playerData.clan?.name}
                </h4>
                <div className="text-sm space-y-1 text-yellow-200">
                  <div>📊 Level: <span className="text-white">{playerData.clan?.clanLevel}</span></div>
                  <div>👥 Members: <span className="text-white">{playerData.clan?.members}/50</span></div>
                  <div>🎖️ War Wins: <span className="text-white">{playerData.clan?.warWins}</span></div>
                  <div>🔥 Win Streak: <span className="text-white">{playerData.clan?.warWinStreak}</span></div>
                </div>
                <button 
                  onClick={goToDashboard}
                  className="coc-button mt-3 w-full py-2 text-sm"
                >
                  📊 Analyze This Clan
                </button>
              </div>
            ) : (
              <div className="bg-black/20 rounded-lg p-4 flex items-center justify-center">
                <span className="text-yellow-200">Player is not in a clan</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Helper Section */}
      <div className="mt-6 coc-glass rounded-lg p-4">
        <h3 className="text-yellow-100 font-bold mb-3 flex items-center gap-2">
          <span className="coc-icon w-8 h-8 text-lg">📋</span>
          How to Find Your Tag
        </h3>
        <ol className="text-yellow-200 text-sm space-y-2 list-decimal list-inside">
          <li>Open Clash of Clans on your device</li>
          <li>Tap your name/profile picture</li>
          <li>Your tag is below your name (starts with #)</li>
          <li>Copy and paste it here</li>
        </ol>
      </div>
    </div>
  )
}
