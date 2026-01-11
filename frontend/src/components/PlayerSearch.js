import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const PlayerSearch = () => {
  const [playerTag, setPlayerTag] = useState('');
  const [loading, setLoading] = useState(false);
  const [playerData, setPlayerData] = useState(null);
  const [error, setError] = useState(null);

  const searchPlayer = async () => {
    if (!playerTag.trim()) {
      setError('Please enter a player tag');
      return;
    }

    setLoading(true);
    setError(null);
    setPlayerData(null);

    try {
      // Format tag (add # if missing)
      let formattedTag = playerTag.trim();
      if (!formattedTag.startsWith('#')) {
        formattedTag = '#' + formattedTag;
      }

      // Test API by trying to get clan for the player
      const response = await axios.post(`${API}/data/add-clan`, {
        clan_tag: formattedTag
      });

      setPlayerData(response.data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      
      if (errorMsg.includes('not found') || errorMsg.includes('API')) {
        setError(`⚠️ API Issue: ${errorMsg}\n\nThis might mean:\n1. Player/Clan tag is incorrect\n2. API key needs IP address updated (35.225.230.28)\n3. API key permissions issue\n\nUsing demo data instead for learning!`);
      } else {
        setError(errorMsg);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="coc-card p-8 border-4 mb-8">
      <h2 className="text-3xl font-bold text-coc-gold mb-4 uppercase flex items-center gap-3">
        <span className="coc-badge w-12 h-12 text-2xl">🔍</span>
        Scout Your Account
      </h2>
      
      <div className="mb-6">
        <label className="block text-yellow-100 mb-2 font-semibold">Enter Player or Clan Tag</label>
        <div className="flex gap-2">
          <input
            type="text"
            value={playerTag}
            onChange={(e) => setPlayerTag(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchPlayer()}
            placeholder="e.g., #2YJ2URLQJ"
            className="flex-1 coc-input"
            data-testid="player-tag-input"
          />
          <button
            onClick={searchPlayer}
            disabled={loading}
            className="coc-button px-8 py-3"
            data-testid="search-player-btn"
          >
            {loading ? '⏳ Searching...' : '🔍 Search'}
          </button>
        </div>
      </div>

      {error && (
        <div className="coc-alert coc-alert-error mb-4">
          <div className="font-bold mb-2">⚠️ Battle Report</div>
          <div className="whitespace-pre-line text-sm">{error}</div>
        </div>
      )}

      {playerData && (
        <div className="coc-alert coc-alert-success">
          <div className="font-bold mb-2">✅ Successfully Connected!</div>
          <div className="text-sm">
            <strong>Found:</strong> {playerData.clan_name || playerData.message}
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

      {/* Current System Status */}
      <div className="mt-6 bg-yellow-900/20 rounded-lg p-4 border border-yellow-500/30">
        <h3 className="text-white font-semibold mb-2">🔧 Current System Status:</h3>
        <div className="text-yellow-200 text-sm space-y-1">
          <div>• API Key: Configured ✅</div>
          <div>• System IP: <code className="bg-black/30 px-2 py-1 rounded">35.225.230.28</code></div>
          <div>• Allowed IP in Key: <code className="bg-black/30 px-2 py-1 rounded">36.255.16.54</code> ⚠️</div>
          <div className="mt-2 text-yellow-300">
            ⚠️ IP mismatch - Update your API key to include system IP above
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlayerSearch;
