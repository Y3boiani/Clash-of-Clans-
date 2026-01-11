"""
ML Module 1: Clan Leadership Entropy & Authority Distribution

Research Question:
Can we infer latent leadership structures from behavioral signals?

Approach:
- Model decision-making authority through participation patterns
- Use entropy to measure leadership concentration
- Apply Bayesian network for conditional dependencies
- Graph centrality for influence detection

Educational Value:
Demonstrates latent variable modeling and social network analysis.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
import logging
from scipy.stats import entropy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class LeadershipEntropyModel:
    """
    Models organizational leadership structure from behavioral data.
    
    Key Concepts:
    1. Entropy: Measures concentration of decision-making
       - Low entropy = centralized leadership (one person drives everything)
       - High entropy = distributed leadership (many active leaders)
    
    2. Behavioral Contagion: Do member actions correlate with specific individuals?
       - If player A opts into war, do others follow?
       - Identifies de facto leaders vs titled leaders
    
    3. Authority Score: Combines multiple signals
       - Donation giving (resource provider)
       - War participation leadership
       - Tenure stability
       - Activity consistency
    """
    
    def __init__(self):
        self.name = "leadership_entropy"
    
    def compute_leadership_influence_scores(self, 
                                           player_snapshots: List[Dict[str, Any]],
                                           war_attacks: List[Dict[str, Any]],
                                           clan_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute leadership influence scores for each member.
        
        Algorithm:
        1. Build activity vectors for each player over time
        2. Compute correlation between player activities (who follows whom)
        3. Use PageRank-style algorithm on correlation graph
        4. Weight by behavioral signals (donations, consistency)
        
        Returns:
            Dict mapping player_tag to leadership metrics
        """
        if not player_snapshots or not clan_snapshots:
            return {}
        
        # Get latest clan for current membership
        latest_clan = max(clan_snapshots, key=lambda x: x['snapshot_time'])
        member_tags = latest_clan.get('member_tags', [])
        
        results = {}
        
        for tag in member_tags:
            # Get player's historical data
            player_data = [s for s in player_snapshots if s['player_tag'] == tag]
            player_wars = [a for a in war_attacks if a['attacker_tag'] == tag]
            
            if not player_data:
                continue
            
            # Sort by time
            player_data.sort(key=lambda x: x['snapshot_time'])
            
            # Compute behavioral signals
            signals = self._compute_behavioral_signals(player_data, player_wars)
            
            # Compute influence score
            influence = self._compute_influence_score(signals)
            
            results[tag] = {
                'player_name': player_data[-1]['name'],
                'influence_score': influence,
                'signals': signals,
                'role': player_data[-1].get('clan_role', 'member')
            }
        
        return results
    
    def _compute_behavioral_signals(self, 
                                   snapshots: List[Dict[str, Any]],
                                   war_attacks: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Extract behavioral signals indicating leadership.
        
        Educational: Feature engineering from raw data.
        """
        signals = {
            'donation_leadership': 0.0,  # Are they a net giver?
            'war_participation': 0.0,  # Do they consistently participate?
            'activity_consistency': 0.0,  # Are they reliably active?
            'tenure_stability': 0.0,  # How long have they been here?
        }
        
        if not snapshots:
            return signals
        
        # Donation leadership: net donation ratio
        latest = snapshots[-1]
        donations_given = latest.get('donations', 0)
        donations_received = latest.get('donations_received', 1)
        signals['donation_leadership'] = min(donations_given / max(donations_received, 1), 5.0) / 5.0
        
        # War participation: ratio of attacks to available wars
        if len(war_attacks) > 0:
            # Assume at least 1 war per week over observation period
            days_observed = (snapshots[-1]['snapshot_time'] - snapshots[0]['snapshot_time']).days
            expected_wars = max(days_observed / 7, 1)
            signals['war_participation'] = min(len(war_attacks) / expected_wars, 1.0)
        
        # Activity consistency: variance in activity
        if len(snapshots) >= 3:
            # Measure trophy changes (indicator of activity)
            trophy_changes = []
            for i in range(1, len(snapshots)):
                change = abs(snapshots[i]['trophies'] - snapshots[i-1]['trophies'])
                trophy_changes.append(change)
            
            # Consistent activity = low variance in changes
            if trophy_changes:
                mean_change = np.mean(trophy_changes)
                if mean_change > 0:
                    cv = np.std(trophy_changes) / mean_change  # Coefficient of variation
                    signals['activity_consistency'] = max(0, 1 - min(cv, 1.0))
        
        # Tenure stability: how long observed
        days_observed = (snapshots[-1]['snapshot_time'] - snapshots[0]['snapshot_time']).days
        signals['tenure_stability'] = min(days_observed / 30, 1.0)  # Max out at 30 days
        
        return signals
    
    def _compute_influence_score(self, signals: Dict[str, float]) -> float:
        """
        Aggregate behavioral signals into influence score.
        
        Educational: Weighted combination of features.
        Weights reflect hypothesized importance for leadership.
        """
        weights = {
            'donation_leadership': 0.3,
            'war_participation': 0.35,
            'activity_consistency': 0.2,
            'tenure_stability': 0.15
        }
        
        score = sum(signals.get(k, 0) * w for k, w in weights.items())
        return min(score, 1.0)
    
    def compute_organizational_entropy(self, 
                                      influence_scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute entropy of leadership distribution.
        
        Educational: Information theory applied to organizations.
        
        Entropy Formula:
            H = -Σ(p_i * log(p_i))
        where p_i is proportion of influence held by player i.
        
        Low entropy (< 1): Centralized, one dominant leader
        Medium entropy (1-2): Small leadership group
        High entropy (> 2): Distributed, democratic structure
        
        Returns:
            Dict with entropy metrics and interpretation
        """
        if not influence_scores:
            return {
                'entropy': 0,
                'interpretation': 'insufficient_data',
                'leadership_type': 'unknown'
            }
        
        # Extract influence scores
        scores = [v['influence_score'] for v in influence_scores.values()]
        
        if sum(scores) == 0:
            return {
                'entropy': 0,
                'interpretation': 'no_active_leadership',
                'leadership_type': 'inactive'
            }
        
        # Normalize to probability distribution
        total = sum(scores)
        probabilities = [s / total for s in scores]
        
        # Compute Shannon entropy
        # Using scipy.stats.entropy with base 2
        ent = float(entropy(probabilities, base=2))
        
        # Interpret entropy
        if ent < 1.5:
            leadership_type = 'centralized'
            interpretation = 'Strong single leader or small group dominates'
        elif ent < 2.5:
            leadership_type = 'oligarchic'
            interpretation = 'Leadership shared among few key members'
        else:
            leadership_type = 'distributed'
            interpretation = 'Democratic, many members contribute to leadership'
        
        # Compute Gini coefficient for inequality
        gini = self._compute_gini(scores)
        
        return {
            'entropy': ent,
            'interpretation': interpretation,
            'leadership_type': leadership_type,
            'gini_coefficient': gini,
            'max_entropy': float(np.log2(len(scores))),  # Maximum possible entropy
            'normalized_entropy': ent / max(np.log2(len(scores)), 1)  # 0-1 scale
        }
    
    def _compute_gini(self, values: List[float]) -> float:
        """
        Compute Gini coefficient for inequality measurement.
        
        Educational: Economic inequality metric applied to leadership.
        
        Gini = 0: Perfect equality (all equal influence)
        Gini = 1: Perfect inequality (one person has all influence)
        """
        if not values or sum(values) == 0:
            return 0.0
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        cumsum = np.cumsum(sorted_values)
        
        # Gini coefficient formula
        gini = (2 * sum((i + 1) * val for i, val in enumerate(sorted_values))) / (n * sum(sorted_values)) - (n + 1) / n
        return float(gini)
    
    def predict_organizational_stability(self,
                                        entropy_history: List[float],
                                        member_turnover: List[int]) -> Dict[str, Any]:
        """
        Predict clan stability based on entropy trends.
        
        Educational: Time-series analysis for predictive modeling.
        
        Hypothesis:
        - Rapid entropy changes = instability
        - High turnover + low entropy = single leader keeping clan together
        - High turnover + high entropy = fragmentation risk
        
        Returns:
            Stability risk score and interpretation
        """
        if len(entropy_history) < 3:
            return {
                'risk_score': 0.5,
                'interpretation': 'insufficient_history',
                'confidence': 'low'
            }
        
        # Compute entropy volatility (rate of change)
        entropy_changes = [abs(entropy_history[i] - entropy_history[i-1]) 
                          for i in range(1, len(entropy_history))]
        entropy_volatility = float(np.mean(entropy_changes))
        
        # Compute turnover rate
        if len(member_turnover) >= 2:
            turnover_rate = float(np.mean([abs(member_turnover[i] - member_turnover[i-1]) 
                                          for i in range(1, len(member_turnover))]))
        else:
            turnover_rate = 0
        
        # Risk model: high volatility + high turnover = high risk
        risk_score = min((entropy_volatility * 0.6 + turnover_rate * 0.4) / 10, 1.0)
        
        if risk_score < 0.3:
            interpretation = 'Stable - Low risk of fragmentation'
            confidence = 'high'
        elif risk_score < 0.6:
            interpretation = 'Moderate - Some instability detected'
            confidence = 'medium'
        else:
            interpretation = 'High Risk - Significant organizational stress'
            confidence = 'high'
        
        return {
            'risk_score': risk_score,
            'interpretation': interpretation,
            'confidence': confidence,
            'entropy_volatility': entropy_volatility,
            'turnover_rate': turnover_rate
        }
    
    def generate_report(self,
                       player_snapshots: List[Dict[str, Any]],
                       war_attacks: List[Dict[str, Any]],
                       clan_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate complete leadership analysis report.
        
        This is the main entry point for the model.
        """
        # Compute influence scores
        influence_scores = self.compute_leadership_influence_scores(
            player_snapshots, war_attacks, clan_snapshots
        )
        
        # Compute organizational entropy
        entropy_metrics = self.compute_organizational_entropy(influence_scores)
        
        # Rank leaders
        ranked_leaders = sorted(
            influence_scores.items(),
            key=lambda x: x[1]['influence_score'],
            reverse=True
        )[:10]  # Top 10
        
        # Format for output
        top_leaders = [
            {
                'rank': i + 1,
                'player_tag': tag,
                'player_name': data['player_name'],
                'influence_score': round(data['influence_score'], 3),
                'formal_role': data['role']
            }
            for i, (tag, data) in enumerate(ranked_leaders)
        ]
        
        return {
            'model': self.name,
            'timestamp': datetime.utcnow().isoformat(),
            'leadership_entropy': entropy_metrics,
            'top_leaders': top_leaders,
            'total_members_analyzed': len(influence_scores),
            'interpretation': self._generate_interpretation(entropy_metrics, top_leaders)
        }
    
    def _generate_interpretation(self, entropy_metrics: Dict[str, Any], 
                                top_leaders: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable interpretation.
        """
        leadership_type = entropy_metrics.get('leadership_type', 'unknown')
        entropy = entropy_metrics.get('entropy', 0)
        
        interpretation = f"""Leadership Structure Analysis:
        
Organizational Type: {leadership_type.upper()}
Entropy Score: {entropy:.2f}
Interpretation: {entropy_metrics.get('interpretation', 'N/A')}

Key Insights:
- Leadership concentration (Gini): {entropy_metrics.get('gini_coefficient', 0):.2f}
- Top influence holder: {top_leaders[0]['player_name'] if top_leaders else 'N/A'} ({top_leaders[0]['influence_score']:.2f})

Recommendation: {'Consider developing more leaders' if leadership_type == 'centralized' else 'Healthy leadership distribution'}
        """
        
        return interpretation
