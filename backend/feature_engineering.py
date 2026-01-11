"""
Feature Engineering Utilities

Production-grade feature extraction from raw CoC data.

Educational Note:
ML models require carefully engineered features.
These utilities transform raw API data into statistical signals.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


def compute_trophy_momentum(snapshots: List[Dict[str, Any]], window_days: int = 7) -> float:
    """
    Compute trophy change velocity over time window.
    
    Educational: First derivative of trophy trajectory.
    Positive = climbing, negative = falling, zero = stable.
    
    Args:
        snapshots: List of player snapshots ordered by time
        window_days: Look-back window
        
    Returns:
        Trophies per day change rate
    """
    if len(snapshots) < 2:
        return 0.0
    
    cutoff = datetime.utcnow() - timedelta(days=window_days)
    recent = [s for s in snapshots if s['snapshot_time'] > cutoff]
    
    if len(recent) < 2:
        return 0.0
    
    # Sort by time
    recent.sort(key=lambda x: x['snapshot_time'])
    
    # Linear regression on trophy trajectory
    times = [(s['snapshot_time'] - recent[0]['snapshot_time']).total_seconds() / 86400 
             for s in recent]
    trophies = [s['trophies'] for s in recent]
    
    if len(times) < 2:
        return 0.0
    
    # Simple slope calculation
    slope = (trophies[-1] - trophies[0]) / max(times[-1], 1)
    return slope


def compute_trophy_volatility(snapshots: List[Dict[str, Any]], window_days: int = 30) -> float:
    """
    Compute trophy standard deviation (volatility).
    
    Educational: Measures rank stability.
    High volatility = inconsistent performance or tilt.
    Low volatility = stable player.
    
    Returns:
        Standard deviation of trophies
    """
    if len(snapshots) < 3:
        return 0.0
    
    cutoff = datetime.utcnow() - timedelta(days=window_days)
    recent = [s for s in snapshots if s['snapshot_time'] > cutoff]
    
    trophies = [s['trophies'] for s in recent]
    return float(np.std(trophies))


def compute_donation_ratio(snapshots: List[Dict[str, Any]]) -> float:
    """
    Compute ratio of donations given to received.
    
    Educational: Identifies benefactors (>1) vs parasites (<1).
    
    Returns:
        Donation ratio (given / received)
    """
    if not snapshots:
        return 1.0
    
    latest = snapshots[-1]
    given = latest.get('donations', 0)
    received = latest.get('donations_received', 1)  # Avoid division by zero
    
    return given / max(received, 1)


def detect_activity_streak(snapshots: List[Dict[str, Any]]) -> Tuple[int, str]:
    """
    Detect consecutive activity or inactivity streaks.
    
    Educational: Behavioral pattern detection.
    
    Returns:
        (streak_length, streak_type): e.g., (5, 'active') or (3, 'inactive')
    """
    if len(snapshots) < 2:
        return 0, 'unknown'
    
    # Sort by time
    snapshots = sorted(snapshots, key=lambda x: x['snapshot_time'], reverse=True)
    
    # Consider activity if donations or trophies changed
    streak = 0
    streak_type = 'unknown'
    
    for i in range(len(snapshots) - 1):
        current = snapshots[i]
        previous = snapshots[i + 1]
        
        donation_change = abs(current['donations'] - previous['donations'])
        trophy_change = abs(current['trophies'] - previous['trophies'])
        
        is_active = donation_change > 0 or trophy_change > 5
        
        if i == 0:
            streak_type = 'active' if is_active else 'inactive'
            streak = 1
        elif (streak_type == 'active' and is_active) or (streak_type == 'inactive' and not is_active):
            streak += 1
        else:
            break
    
    return streak, streak_type


def compute_war_participation_rate(war_attacks: List[Dict[str, Any]], 
                                   total_wars: int) -> float:
    """
    Compute player's war participation rate.
    
    Educational: Measures engagement level.
    
    Returns:
        Participation rate (0-1)
    """
    if total_wars == 0:
        return 0.0
    
    # Count unique wars player participated in
    war_ids = set(a['war_id'] for a in war_attacks)
    return len(war_ids) / total_wars


def compute_attack_consistency(war_attacks: List[Dict[str, Any]]) -> float:
    """
    Compute consistency of attack performance (inverse of star variance).
    
    Educational: Low variance = reliable, high variance = inconsistent.
    
    Returns:
        Consistency score (0-1), higher is more consistent
    """
    if len(war_attacks) < 3:
        return 0.5  # Neutral for insufficient data
    
    stars = [a['stars'] for a in war_attacks]
    variance = np.var(stars)
    
    # Normalize: variance ranges from 0 (all same) to ~2 (max variance for 0-3 stars)
    # Convert to consistency: high variance = low consistency
    consistency = 1 - min(variance / 2.0, 1.0)
    return float(consistency)


def identify_attack_pressure_context(attack: Dict[str, Any], 
                                     war_state: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute pressure metrics for an attack based on war state.
    
    Educational: Contextual features for pressure modeling.
    
    Returns:
        Dict with pressure indicators
    """
    pressure = {
        'position_pressure': 0.0,  # Early attacks have more pressure
        'score_pressure': 0.0,  # Losing = more pressure
        'importance': 0.0,  # Critical attack = more pressure
    }
    
    # Position pressure: early attacks set the tone
    total_attacks = war_state.get('team_size', 0) * 2  # Each player gets 2 attacks
    if total_attacks > 0:
        attack_order = attack.get('attack_order', 0)
        # First 25% of attacks have high pressure
        pressure['position_pressure'] = max(0, 1 - (attack_order / (total_attacks * 0.25)))
    
    # Score pressure: are we behind?
    our_stars = war_state.get('our_stars', 0)
    their_stars = war_state.get('their_stars', 0)
    star_diff = our_stars - their_stars
    
    if star_diff < 0:
        pressure['score_pressure'] = min(abs(star_diff) / 10, 1.0)
    
    # Importance: is this attack critical?
    stars_needed = max(0, their_stars - our_stars + 1)
    if stars_needed <= 3:  # One good attack could swing it
        pressure['importance'] = 1.0
    
    return pressure


def build_donation_network(clan_snapshots: List[Dict[str, Any]], 
                          player_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build donation network graph.
    
    Educational: Network analysis for social structure.
    
    Returns:
        Dict with nodes (players) and edges (inferred donation flows)
    """
    # Get latest clan snapshot for membership
    if not clan_snapshots:
        return {"nodes": [], "edges": []}
    
    latest_clan = clan_snapshots[-1]
    member_tags = latest_clan.get('member_tags', [])
    
    # Build nodes with donation stats
    nodes = []
    for tag in member_tags:
        player_snaps = [s for s in player_snapshots if s['player_tag'] == tag]
        if not player_snaps:
            continue
        
        latest = player_snaps[-1]
        nodes.append({
            'id': tag,
            'name': latest['name'],
            'donations_given': latest['donations'],
            'donations_received': latest['donations_received'],
            'net_donations': latest['donations'] - latest['donations_received']
        })
    
    # Note: Edges are inferred since API doesn't provide who donated to whom
    # For full network, would need to track deltas between snapshots
    
    return {
        "nodes": nodes,
        "edges": []  # Would require delta analysis between snapshots
    }


def compute_clan_activity_rhythm(clan_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze clan activity patterns over time.
    
    Educational: Time-series pattern detection.
    
    Returns:
        Dict with rhythm metrics
    """
    if len(clan_snapshots) < 7:
        return {"rhythm_type": "insufficient_data"}
    
    # Sort by time
    snapshots = sorted(clan_snapshots, key=lambda x: x['snapshot_time'])
    
    # Compute member count changes
    member_counts = [s['member_count'] for s in snapshots]
    member_volatility = float(np.std(member_counts))
    
    # Compute war frequency
    war_wins = [s['war_wins'] for s in snapshots]
    war_rate = (war_wins[-1] - war_wins[0]) / max(len(snapshots), 1)
    
    return {
        "rhythm_type": "stable" if member_volatility < 2 else "volatile",
        "member_volatility": member_volatility,
        "war_rate_per_snapshot": war_rate,
        "average_member_count": float(np.mean(member_counts))
    }
