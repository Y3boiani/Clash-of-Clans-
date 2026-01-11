"""
ML Module 6: Clan Capital Investment & Collective Action Problem

Research Question:
Can contribution patterns predict raid success better than capital level?

Approach:
- Game-theoretic modeling (public goods game)
- Causal inference (propensity score matching)
- Free-rider detection via contribution inequality
- Agent-based simulation for optimal policies

Educational Value:
Demonstrates game theory, causal inference, and multi-agent systems.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CapitalInvestmentModel:
    """
    Models clan capital as collective action problem.
    
    Key Concepts:
    1. Public Goods Game:
       - Capital is public good (everyone benefits from raids)
       - Free-rider problem: incentive to not contribute but enjoy rewards
       - Tragedy of the commons: under-investment without coordination
    
    2. Contribution Patterns:
       - Timing: Do players contribute early or late?
       - Consistency: Regular small contributions vs sporadic large ones
       - Inequality: Is contribution burden shared or concentrated?
    
    3. Causal Question:
       Does contribution BEHAVIOR (not just total) cause raid success?
       Hypothesis: Coordinated contribution patterns indicate overall
       clan coordination, which drives success beyond capital level.
    """
    
    def __init__(self):
        self.name = "capital_investment"
    
    def analyze_contribution_patterns(self,
                                     raid_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze individual contribution patterns in capital raids.
        
        Educational: Feature extraction from event data.
        
        Returns:
            Per-player contribution profiles
        """
        if not raid_data:
            return {'status': 'no_data'}
        
        # Aggregate contributions per player across raids
        player_contributions = defaultdict(lambda: {
            'total_contributed': 0,
            'raids_participated': 0,
            'total_attacks': 0,
            'total_looted': 0,
            'contributions_history': []
        })
        
        for raid in raid_data:
            members = raid.get('member_contributions', [])
            for member in members:
                tag = member['tag']
                contributed = member.get('capital_resources_looted', 0)  # Note: API uses 'looted' for contributions
                attacks = member.get('attacks', 0)
                
                player_contributions[tag]['total_contributed'] += contributed
                player_contributions[tag]['raids_participated'] += 1
                player_contributions[tag]['total_attacks'] += attacks
                player_contributions[tag]['total_looted'] += contributed
                player_contributions[tag]['contributions_history'].append(contributed)
        
        # Classify contribution types
        classified_players = []
        
        for tag, data in player_contributions.items():
            avg_contribution = data['total_contributed'] / max(data['raids_participated'], 1)
            participation_rate = data['raids_participated'] / len(raid_data)
            
            # Compute consistency (inverse of variance)
            if len(data['contributions_history']) > 1:
                std = float(np.std(data['contributions_history']))
                mean = float(np.mean(data['contributions_history']))
                consistency = 1 - min(std / max(mean, 1), 1.0)
            else:
                consistency = 0.5
            
            # Classify player type
            if participation_rate < 0.3:
                player_type = 'inactive'
            elif avg_contribution < 100:
                player_type = 'free_rider'
            elif avg_contribution >= 100 and consistency > 0.6:
                player_type = 'consistent_contributor'
            else:
                player_type = 'irregular_contributor'
            
            classified_players.append({
                'player_tag': tag,
                'total_contributed': data['total_contributed'],
                'avg_contribution': avg_contribution,
                'participation_rate': participation_rate,
                'consistency': consistency,
                'player_type': player_type,
                'total_attacks': data['total_attacks']
            })
        
        return {
            'players_analyzed': len(classified_players),
            'player_profiles': classified_players,
            'raids_analyzed': len(raid_data)
        }
    
    def detect_free_riders(self,
                          contribution_patterns: Dict[str, Any],
                          threshold_percentile: float = 25) -> List[Dict[str, Any]]:
        """
        Identify free-riders (low contributors relative to clan).
        
        Educational: Percentile-based outlier detection.
        
        Free-riders contribute below 25th percentile but participate in raids.
        
        Returns:
            List of identified free-riders
        """
        if contribution_patterns.get('status') == 'no_data':
            return []
        
        players = contribution_patterns['player_profiles']
        
        # Compute contribution distribution
        contributions = [p['total_contributed'] for p in players if p['participation_rate'] > 0.3]
        
        if not contributions:
            return []
        
        threshold = np.percentile(contributions, threshold_percentile)
        
        free_riders = []
        for player in players:
            # Free-rider: participates but contributes below threshold
            if (player['participation_rate'] > 0.3 and 
                player['total_contributed'] < threshold):
                
                free_rider_score = 1 - (player['total_contributed'] / threshold)
                
                free_riders.append({
                    'player_tag': player['player_tag'],
                    'total_contributed': player['total_contributed'],
                    'clan_threshold': threshold,
                    'participation_rate': player['participation_rate'],
                    'free_rider_score': min(free_rider_score, 1.0),
                    'player_type': player['player_type']
                })
        
        # Sort by free-rider score
        free_riders.sort(key=lambda x: x['free_rider_score'], reverse=True)
        
        return free_riders
    
    def compute_contribution_inequality(self,
                                       contribution_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Measure inequality in contribution distribution.
        
        Educational: Gini coefficient application.
        
        High inequality = few players carry the burden
        Low inequality = contributions well distributed
        
        Returns:
            Inequality metrics
        """
        if contribution_patterns.get('status') == 'no_data':
            return {'gini': 0, 'interpretation': 'no_data'}
        
        players = contribution_patterns['player_profiles']
        contributions = [p['total_contributed'] for p in players]
        
        gini = self._compute_gini(contributions)
        
        # Interpret
        if gini < 0.3:
            interpretation = 'equal'
            description = 'Contributions evenly distributed - healthy'
        elif gini < 0.5:
            interpretation = 'moderate'
            description = 'Some inequality - few players contribute more'
        else:
            interpretation = 'high'
            description = 'High inequality - burden on few players (burnout risk)'
        
        # Also compute top contributor concentration
        total_contrib = sum(contributions)
        sorted_contrib = sorted(contributions, reverse=True)
        top_10_pct = sum(sorted_contrib[:max(1, len(sorted_contrib)//10)])
        top_10_concentration = top_10_pct / total_contrib if total_contrib > 0 else 0
        
        return {
            'gini_coefficient': float(gini),
            'interpretation': interpretation,
            'description': description,
            'top_10_pct_concentration': float(top_10_concentration)
        }
    
    def _compute_gini(self, values: List[float]) -> float:
        """
        Compute Gini coefficient.
        """
        if not values or sum(values) == 0:
            return 0.0
        
        sorted_values = sorted([v for v in values if v >= 0])
        n = len(sorted_values)
        
        if n == 0:
            return 0.0
        
        cumsum = np.cumsum(sorted_values)
        gini = (2 * sum((i + 1) * val for i, val in enumerate(sorted_values))) / (n * sum(sorted_values)) - (n + 1) / n
        return max(0, min(float(gini), 1.0))
    
    def analyze_raid_outcomes(self,
                             raid_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze raid weekend outcomes and metrics.
        
        Educational: Performance measurement.
        
        Returns:
            Raid success metrics
        """
        if not raid_data:
            return {'status': 'no_data'}
        
        total_loot = sum(r.get('total_loot', 0) for r in raid_data)
        total_attacks = sum(r.get('total_attacks', 0) for r in raid_data)
        avg_loot = total_loot / len(raid_data)
        
        # Efficiency: loot per attack
        if total_attacks > 0:
            loot_per_attack = total_loot / total_attacks
        else:
            loot_per_attack = 0
        
        # Success trend
        if len(raid_data) >= 3:
            recent_loot = [r.get('total_loot', 0) for r in raid_data[-3:]]
            trend = 'improving' if recent_loot[-1] > recent_loot[0] else 'declining'
        else:
            trend = 'insufficient_data'
        
        return {
            'raids_analyzed': len(raid_data),
            'total_loot': total_loot,
            'average_loot_per_raid': avg_loot,
            'total_attacks': total_attacks,
            'loot_per_attack': loot_per_attack,
            'trend': trend
        }
    
    def test_contribution_pattern_hypothesis(self,
                                           raid_data: List[Dict[str, Any]],
                                           contribution_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test whether contribution patterns predict raid success.
        
        Educational: Causal inference and hypothesis testing.
        
        Hypothesis: Clans with:
        1. Lower contribution inequality
        2. Higher participation rates
        3. More consistent contributors
        ...perform better in raids (controlling for capital level)
        
        Note: This is observational, not experimental, so we can only
        show correlation, not causation. Full causal inference would
        require propensity score matching across multiple clans.
        
        Returns:
            Hypothesis test results
        """
        if not raid_data or contribution_patterns.get('status') == 'no_data':
            return {'hypothesis': 'insufficient_data'}
        
        # Extract features
        inequality = self.compute_contribution_inequality(contribution_patterns)
        gini = inequality['gini_coefficient']
        
        # Participation rate
        players = contribution_patterns['player_profiles']
        avg_participation = float(np.mean([p['participation_rate'] for p in players]))
        
        # Consistency
        consistent_players = sum(1 for p in players if p['player_type'] == 'consistent_contributor')
        consistency_rate = consistent_players / len(players) if players else 0
        
        # Outcome: average raid performance
        outcomes = self.analyze_raid_outcomes(raid_data)
        avg_loot = outcomes['average_loot_per_raid']
        
        # Simple correlation analysis
        # In real implementation, would use regression with multiple clans
        
        # Predict expected performance based on patterns
        # Lower inequality + higher participation + more consistency = better
        pattern_score = (
            (1 - gini) * 0.4 +  # Lower inequality is better
            avg_participation * 0.3 +
            consistency_rate * 0.3
        ) * 100
        
        # Interpretation
        if pattern_score > 70:
            prediction = 'high_performance_expected'
            confidence = 'medium'
        elif pattern_score > 50:
            prediction = 'moderate_performance_expected'
            confidence = 'low'
        else:
            prediction = 'improvement_needed'
            confidence = 'medium'
        
        return {
            'hypothesis': 'contribution_patterns_matter',
            'pattern_score': float(pattern_score),
            'prediction': prediction,
            'confidence': confidence,
            'observed_performance': avg_loot,
            'key_factors': {
                'contribution_inequality': gini,
                'participation_rate': avg_participation,
                'consistency_rate': consistency_rate
            },
            'interpretation': f"Pattern score: {pattern_score:.1f}/100. {prediction.replace('_', ' ').title()}."
        }
    
    def generate_optimal_contribution_policy(self,
                                           contribution_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate recommendations for optimal contribution policy.
        
        Educational: Policy recommendation from data.
        
        Based on analysis, suggest:
        - Minimum contribution requirements
        - Participation incentives
        - Free-rider management
        
        Returns:
            Policy recommendations
        """
        if contribution_patterns.get('status') == 'no_data':
            return {'policy': 'insufficient_data'}
        
        players = contribution_patterns['player_profiles']
        inequality = self.compute_contribution_inequality(contribution_patterns)
        
        # Compute recommended minimum
        contributions = [p['total_contributed'] for p in players]
        median_contribution = float(np.median(contributions))
        mean_contribution = float(np.mean(contributions))
        
        # Policy recommendations
        policies = []
        
        # 1. Minimum contribution policy
        recommended_minimum = median_contribution * 0.5  # 50% of median
        policies.append({
            'policy_type': 'minimum_contribution',
            'recommendation': f"Set minimum weekly contribution: {int(recommended_minimum)}",
            'rationale': 'Reduces free-riding while being achievable for most members'
        })
        
        # 2. Inequality reduction
        if inequality['gini_coefficient'] > 0.5:
            policies.append({
                'policy_type': 'burden_sharing',
                'recommendation': 'Encourage broader participation - top contributors may burn out',
                'rationale': f"Current Gini: {inequality['gini_coefficient']:.2f} - high inequality detected"
            })
        
        # 3. Free-rider management
        free_riders = self.detect_free_riders(contribution_patterns)
        if len(free_riders) > len(players) * 0.2:  # >20% free-riders
            policies.append({
                'policy_type': 'free_rider_management',
                'recommendation': f"Address {len(free_riders)} low contributors (>{20}% of clan)",
                'rationale': 'High free-rider rate may demotivate contributors'
            })
        
        return {
            'policy_recommendations': policies,
            'recommended_minimum': int(recommended_minimum),
            'current_median': int(median_contribution),
            'inequality_status': inequality['interpretation']
        }
    
    def generate_clan_report(self,
                           raid_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive capital investment analysis.
        
        Main entry point for clan capital analysis.
        """
        # Analyze contribution patterns
        patterns = self.analyze_contribution_patterns(raid_data)
        
        # Detect free-riders
        free_riders = self.detect_free_riders(patterns)
        
        # Contribution inequality
        inequality = self.compute_contribution_inequality(patterns)
        
        # Raid outcomes
        outcomes = self.analyze_raid_outcomes(raid_data)
        
        # Test hypothesis
        hypothesis = self.test_contribution_pattern_hypothesis(raid_data, patterns)
        
        # Policy recommendations
        policy = self.generate_optimal_contribution_policy(patterns)
        
        return {
            'model': self.name,
            'timestamp': datetime.utcnow().isoformat(),
            'contribution_analysis': patterns,
            'free_riders': {
                'count': len(free_riders),
                'top_free_riders': free_riders[:10]
            },
            'inequality': inequality,
            'raid_outcomes': outcomes,
            'hypothesis_test': hypothesis,
            'policy_recommendations': policy
        }
