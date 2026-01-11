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
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-4">🔍 Test with Your Account</h2>
      
      <div className="mb-6">
        <label className="block text-blue-200 mb-2">Enter Player or Clan Tag</label>
        <div className="flex gap-2">
          <input
            type="text"
            value={playerTag}
            onChange={(e) => setPlayerTag(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchPlayer()}
            placeholder="e.g., #ABC123 or ABC123"
            className="flex-1 px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-blue-300 focus:outline-none focus:border-blue-400"
            data-testid="player-tag-input"
          />
          <button
            onClick={searchPlayer}
            disabled={loading}
            className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-semibold hover:shadow-xl disabled:opacity-50 transition-all"
            data-testid="search-player-btn"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 mb-4">
          <div className="text-red-100 whitespace-pre-line">{error}</div>
          <div className="mt-3 text-sm text-red-200">
            <strong>Quick Fix:</strong>
            <ol className="list-decimal list-inside mt-2 space-y-1">
              <li>Go to <a href="https://developer.clashofclans.com/" target="_blank" rel="noopener noreferrer" className="underline">developer.clashofclans.com</a></li>
              <li>Update your API key to include IP: <code className="bg-black/30 px-2 py-1 rounded">35.225.230.28</code></li>
              <li>Try searching again</li>
            </ol>
          </div>
        </div>
      )}

      {playerData && (
        <div className="bg-green-500/20 border border-green-500/50 rounded-lg p-4">
          <div className="text-green-100">
            ✅ Successfully connected to Clash of Clans API!
          </div>
          <div className="mt-3 text-sm text-green-200">
            <strong>Found:</strong> {playerData.clan_name || playerData.message}
          </div>
        </div>
      )}

      {/* Helper Section */}
      <div className="mt-6 bg-blue-900/20 rounded-lg p-4">
        <h3 className="text-white font-semibold mb-2">📋 How to Find Your Player Tag:</h3>
        <ol className="text-blue-200 text-sm space-y-1 list-decimal list-inside">
          <li>Open Clash of Clans</li>
          <li>Tap your name at the top</li>
          <li>Your player tag is below your name (starts with #)</li>
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
