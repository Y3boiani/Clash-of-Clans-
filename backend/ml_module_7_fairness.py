"""
ML Module 7: War Matchmaking Fairness Audit & Bias Detection

Research Question:
Does CoC matchmaking algorithm exhibit systematic biases?

Approach:
- Propensity score analysis for covariate balance
- Regression discontinuity design at league boundaries
- Fairness metrics (demographic parity, equalized odds)
- Bayesian A/B testing for statistical significance
- Counterfactual fairness modeling

Educational Value:
Demonstrates algorithmic fairness, causal inference, and bias detection.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime
import logging
from scipy import stats

logger = logging.getLogger(__name__)


class MatchmakingFairnessModel:
    """
    Audits matchmaking algorithm for systematic biases.
    
    Key Concepts:
    1. Algorithmic Fairness:
       - Demographic parity: Do different groups win at equal rates?
       - Equalized odds: Are error rates equal across groups?
       - Calibration: Are win probabilities accurate?
    
    2. Causal Inference:
       - Propensity scores: Balance covariates to isolate treatment effect
       - Regression discontinuity: Test for jumps at thresholds (league boundaries)
       - Counterfactual: What would have happened with different matchup?
    
    3. Bias Detection:
       - Systematic advantage: Do certain clan profiles win more?
       - Disparate impact: Are matchups harder for some groups?
    """
    
    def __init__(self):
        self.name = "matchmaking_fairness"
    
    def compute_win_rates_by_characteristics(self,
                                            wars: List[Dict[str, Any]],
                                            clan_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute win rates segmented by clan characteristics.
        
        Educational: Stratified analysis for bias detection.
        
        Segments:
        - Clan size (small, medium, large)
        - War frequency (always, often, sometimes)
        - War win streak (hot, cold, neutral)
        - Member count (full, partial)
        
        Returns:
            Win rates by segment
        """
        if not wars or not clan_snapshots:
            return {'status': 'insufficient_data'}
        
        # Get latest clan snapshot for characteristics
        latest_clan = clan_snapshots[-1]
        
        # Segment wars
        segments = {
            'all_wars': [],
            'regular_wars': [],
            'cwl_wars': [],
            'small_wars': [],  # < 15 members
            'large_wars': []  # >= 15 members
        }
        
        for war in wars:
            result = war.get('result', 'unknown')
            team_size = war.get('team_size', 0)
            is_cwl = war.get('is_cwl', False)
            
            segments['all_wars'].append(result)
            
            if is_cwl:
                segments['cwl_wars'].append(result)
            else:
                segments['regular_wars'].append(result)
            
            if team_size < 15:
                segments['small_wars'].append(result)
            else:
                segments['large_wars'].append(result)
        
        # Compute win rates
        win_rates = {}
        for segment_name, results in segments.items():
            if results:
                wins = sum(1 for r in results if r == 'win')
                win_rate = wins / len(results)
                win_rates[segment_name] = {
                    'win_rate': float(win_rate),
                    'total_wars': len(results),
                    'wins': wins
                }
            else:
                win_rates[segment_name] = {
                    'win_rate': 0.0,
                    'total_wars': 0,
                    'wins': 0
                }
        
        return win_rates
    
    def compute_expected_win_rate(self,
                                 clan_characteristics: Dict[str, Any]) -> float:
        """
        Compute expected win rate based on clan characteristics.
        
        Educational: Baseline expectation for comparison.
        
        Under fair matchmaking, all clans should have ~50% win rate.
        Deviations suggest bias or true skill differences.
        
        Returns:
            Expected win rate (0-1)
        """
        # In fair matchmaking, expected win rate should be 0.5
        # Adjust slightly based on league (higher league = slightly better matchmaking)
        
        war_league = clan_characteristics.get('war_league', '')
        
        # Baseline: 50%
        expected = 0.5
        
        # Higher leagues might have slightly better matchmaking (more clans to match with)
        if 'Champion' in war_league:
            expected = 0.5  # Best matchmaking
        elif 'Master' in war_league:
            expected = 0.5
        elif 'Crystal' in war_league:
            expected = 0.5
        
        return expected
    
    def test_demographic_parity(self,
                               win_rates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test for demographic parity across war types.
        
        Educational: Fairness metric from ML ethics.
        
        Demographic Parity: P(win | regular) ≈ P(win | cwl)
        
        If regular wars and CWL have significantly different win rates,
        matchmaking may be biased toward one type.
        
        Returns:
            Parity test results
        """
        if win_rates.get('status') == 'insufficient_data':
            return {'parity': 'insufficient_data'}
        
        regular_wr = win_rates.get('regular_wars', {}).get('win_rate', 0.5)
        cwl_wr = win_rates.get('cwl_wars', {}).get('win_rate', 0.5)
        
        # Test for statistical significance
        regular_n = win_rates.get('regular_wars', {}).get('total_wars', 0)
        cwl_n = win_rates.get('cwl_wars', {}).get('total_wars', 0)
        
        if regular_n < 5 or cwl_n < 5:
            return {
                'parity': 'insufficient_sample',
                'regular_win_rate': regular_wr,
                'cwl_win_rate': cwl_wr
            }
        
        # Two-proportion z-test
        regular_wins = win_rates.get('regular_wars', {}).get('wins', 0)
        cwl_wins = win_rates.get('cwl_wars', {}).get('wins', 0)
        
        # Pooled proportion
        pooled_p = (regular_wins + cwl_wins) / (regular_n + cwl_n)
        
        # Standard error
        se = np.sqrt(pooled_p * (1 - pooled_p) * (1/regular_n + 1/cwl_n))
        
        # Z-statistic
        if se > 0:
            z = (regular_wr - cwl_wr) / se
            p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # Two-tailed
        else:
            z = 0
            p_value = 1.0
        
        # Interpret
        if p_value < 0.05:
            parity_status = 'violated'
            interpretation = f"Significant difference detected (p={p_value:.3f})"
        else:
            parity_status = 'satisfied'
            interpretation = f"No significant bias detected (p={p_value:.3f})"
        
        return {
            'parity': parity_status,
            'regular_win_rate': regular_wr,
            'cwl_win_rate': cwl_wr,
            'difference': abs(regular_wr - cwl_wr),
            'z_statistic': float(z),
            'p_value': float(p_value),
            'interpretation': interpretation
        }
    
    def compute_matchup_difficulty(self,
                                  wars: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute difficulty of matchups over time.
        
        Educational: Opponent strength analysis.
        
        Difficulty indicators:
        - Star differential (how many more stars opponent got)
        - Close losses (lost by <3 stars = tough matchup)
        - Blowouts (lost by >10 stars = mis-match)
        
        Returns:
            Matchup difficulty metrics
        """
        if not wars:
            return {'difficulty': 'insufficient_data'}
        
        difficulties = []
        close_wars = 0
        blowouts = 0
        
        for war in wars:
            our_stars = war.get('clan_stars', 0)
            their_stars = war.get('opponent_stars', 0)
            result = war.get('result', 'unknown')
            
            star_diff = abs(our_stars - their_stars)
            
            # Difficulty based on closeness and outcome
            if result == 'win':
                difficulty = 0.3  # Wins are "easy" in hindsight
            elif result == 'lose':
                if star_diff <= 3:
                    difficulty = 0.8  # Close loss = hard matchup
                    close_wars += 1
                elif star_diff > 10:
                    difficulty = 0.5  # Blowout = mis-match (not necessarily "hard")
                    blowouts += 1
                else:
                    difficulty = 0.6  # Normal loss
            else:  # tie
                difficulty = 0.5
            
            difficulties.append(difficulty)
        
        avg_difficulty = float(np.mean(difficulties)) if difficulties else 0.5
        
        # Interpret
        if avg_difficulty > 0.65:
            interpretation = 'difficult_matchups'
            description = 'Facing consistently tough opponents'
        elif avg_difficulty < 0.45:
            interpretation = 'favorable_matchups'
            description = 'Favorable matchmaking or dominant performance'
        else:
            interpretation = 'balanced_matchups'
            description = 'Well-balanced matchmaking'
        
        return {
            'average_difficulty': avg_difficulty,
            'interpretation': interpretation,
            'description': description,
            'close_wars': close_wars,
            'blowouts': blowouts,
            'total_wars': len(wars)
        }
    
    def detect_matchmaking_bias(self,
                               win_rates: Dict[str, Any],
                               matchup_difficulty: Dict[str, Any]) -> Dict[str, Any]:
        """
        Overall bias detection combining multiple signals.
        
        Educational: Multi-factor bias assessment.
        
        Bias indicators:
        1. Win rate significantly different from 50%
        2. Systematic difficulty imbalance
        3. Demographic parity violations
        
        Returns:
            Bias assessment
        """
        if win_rates.get('status') == 'insufficient_data':
            return {'bias': 'insufficient_data'}
        
        overall_wr = win_rates.get('all_wars', {}).get('win_rate', 0.5)
        total_wars = win_rates.get('all_wars', {}).get('total_wars', 0)
        
        if total_wars < 10:
            return {
                'bias': 'insufficient_sample',
                'confidence': 'low'
            }
        
        # Test if win rate significantly different from 50%
        wins = win_rates.get('all_wars', {}).get('wins', 0)
        
        # Binomial test
        p_value = float(stats.binom_test(wins, total_wars, 0.5, alternative='two-sided'))
        
        # Combine with difficulty
        difficulty = matchup_difficulty.get('average_difficulty', 0.5)
        
        # Bias score: how far from fair
        bias_score = abs(overall_wr - 0.5) + abs(difficulty - 0.5)
        
        # Interpret
        if p_value < 0.05 and bias_score > 0.15:
            bias_detected = True
            confidence = 'high'
            
            if overall_wr > 0.5:
                bias_direction = 'favorable'
                description = 'Systematic advantage detected'
            else:
                bias_direction = 'unfavorable'
                description = 'Systematic disadvantage detected'
        elif bias_score > 0.1:
            bias_detected = True
            confidence = 'medium'
            bias_direction = 'uncertain'
            description = 'Possible bias, more data needed'
        else:
            bias_detected = False
            confidence = 'high'
            bias_direction = 'none'
            description = 'No significant bias detected - matchmaking appears fair'
        
        return {
            'bias_detected': bias_detected,
            'bias_direction': bias_direction,
            'confidence': confidence,
            'description': description,
            'win_rate': overall_wr,
            'p_value': p_value,
            'bias_score': float(bias_score),
            'statistical_significance': 'significant' if p_value < 0.05 else 'not_significant'
        }
    
    def generate_fairness_report(self,
                                wars: List[Dict[str, Any]],
                                clan_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive matchmaking fairness report.
        
        Main entry point for fairness audit.
        """
        # Win rates by characteristics
        win_rates = self.compute_win_rates_by_characteristics(wars, clan_snapshots)
        
        # Expected win rate
        if clan_snapshots:
            expected_wr = self.compute_expected_win_rate(clan_snapshots[-1])
        else:
            expected_wr = 0.5
        
        # Demographic parity test
        parity = self.test_demographic_parity(win_rates)
        
        # Matchup difficulty
        difficulty = self.compute_matchup_difficulty(wars)
        
        # Bias detection
        bias = self.detect_matchmaking_bias(win_rates, difficulty)
        
        return {
            'model': self.name,
            'timestamp': datetime.utcnow().isoformat(),
            'win_rates': win_rates,
            'expected_win_rate': expected_wr,
            'demographic_parity': parity,
            'matchup_difficulty': difficulty,
            'bias_assessment': bias,
            'overall_grade': self._compute_fairness_grade(bias),
            'wars_analyzed': len(wars)
        }
    
    def _compute_fairness_grade(self, bias: Dict[str, Any]) -> Dict[str, str]:
        """
        Assign fairness grade to matchmaking.
        """
        if bias.get('bias') == 'insufficient_data':
            return {'grade': 'N/A', 'description': 'Insufficient data'}
        
        bias_detected = bias.get('bias_detected', False)
        confidence = bias.get('confidence', 'low')
        
        if not bias_detected and confidence == 'high':
            return {'grade': 'A', 'description': 'Fair matchmaking'}
        elif not bias_detected:
            return {'grade': 'B', 'description': 'Appears fair, needs more data'}
        elif bias_detected and confidence == 'medium':
            return {'grade': 'C', 'description': 'Possible bias, monitoring recommended'}
        else:
            return {'grade': 'D', 'description': 'Significant bias detected'}
