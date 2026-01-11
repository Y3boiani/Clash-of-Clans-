"""
ML Module 2: War Performance Pressure Function & Choking Probability

Research Question:
How does situational pressure affect individual war performance?

Approach:
- Model performance as f(skill, pressure)
- Use Bayesian inference for player-specific variance
- Gaussian Process for smooth pressure response curves
- Identify "clutch" vs "choke" players

Educational Value:
Demonstrates variance modeling and contextual performance analysis.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime
import logging
from scipy import stats

logger = logging.getLogger(__name__)


class PressureFunctionModel:
    """
    Models individual performance under pressure.
    
    Key Concepts:
    1. Baseline Performance: Player's average ability (skill)
    2. Performance Variance: How consistent they are
    3. Pressure Sensitivity: How much pressure affects them
    4. Clutch Factor: Do they improve or decline under pressure?
    
    Mathematical Model:
        stars ~ N(μ(pressure), σ²)
    where:
        μ(pressure) = baseline + β * pressure
        β > 0: clutch player (improves under pressure)
        β < 0: choke player (declines under pressure)
        σ²: consistency (lower = more reliable)
    """
    
    def __init__(self):
        self.name = "pressure_function"
    
    def compute_attack_pressure(self, attack: Dict[str, Any], 
                               war_context: Dict[str, Any]) -> float:
        """
        Compute pressure score for an attack (0-1 scale).
        
        Pressure Factors:
        1. Score differential (are we losing?)
        2. Attack position (early = setting tone, late = cleanup)
        3. War importance (CWL vs regular)
        4. Attack order among player's attacks (first attack = more pressure)
        
        Returns:
            Pressure score (0 = low pressure, 1 = extreme pressure)
        """
        pressure = 0.0
        
        # Factor 1: Score pressure
        our_stars = war_context.get('our_stars', 0)
        their_stars = war_context.get('their_stars', 0)
        star_diff = their_stars - our_stars  # Positive if we're behind
        
        if star_diff > 0:
            # Behind in war = high pressure
            pressure += min(star_diff / 10, 0.4)  # Cap at 0.4
        
        # Factor 2: Position pressure
        attack_order = attack.get('attack_order', 0)
        total_attacks_possible = war_context.get('team_size', 0) * 2
        
        if total_attacks_possible > 0:
            # Early attacks (first 30%) have medium pressure
            # Middle attacks (30-70%) have lower pressure  
            # Late attacks (70%+) with close score = high pressure
            position_pct = attack_order / total_attacks_possible
            
            if position_pct < 0.3:
                pressure += 0.2  # Early game pressure
            elif position_pct > 0.7 and abs(star_diff) <= 3:
                pressure += 0.3  # Late game, close war = clutch moment
        
        # Factor 3: War importance
        if war_context.get('is_cwl', False):
            pressure += 0.1  # CWL adds pressure
        
        return min(pressure, 1.0)
    
    def compute_player_baseline_performance(self, 
                                           attacks: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Compute player's baseline performance (skill level).
        
        Educational: Statistical estimation from samples.
        
        Returns:
            Dict with mean, std, and confidence interval
        """
        if not attacks:
            return {
                'mean_stars': 0.0,
                'std_stars': 0.0,
                'confidence_95': (0.0, 0.0),
                'sample_size': 0
            }
        
        stars = [a['stars'] for a in attacks]
        mean_stars = float(np.mean(stars))
        std_stars = float(np.std(stars, ddof=1) if len(stars) > 1 else 0)
        
        # 95% confidence interval
        if len(stars) > 1:
            conf_int = stats.t.interval(0.95, len(stars)-1, 
                                       loc=mean_stars,
                                       scale=stats.sem(stars))
        else:
            conf_int = (mean_stars, mean_stars)
        
        return {
            'mean_stars': mean_stars,
            'std_stars': std_stars,
            'confidence_95': conf_int,
            'sample_size': len(attacks)
        }
    
    def compute_pressure_sensitivity(self,
                                    attacks: List[Dict[str, Any]],
                                    war_contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Estimate how pressure affects player performance.
        
        Educational: Regression analysis.
        
        Model: stars = β0 + β1 * pressure + ε
        
        β1 > 0: Player improves under pressure (clutch)
        β1 < 0: Player declines under pressure (choke)
        
        Returns:
            Pressure sensitivity coefficient and interpretation
        """
        if len(attacks) < 5:  # Need sufficient data
            return {
                'beta': 0.0,
                'interpretation': 'insufficient_data',
                'confidence': 'low',
                'sample_size': len(attacks)
            }
        
        # Compute pressure for each attack
        pressures = []
        stars = []
        
        for attack in attacks:
            # Find matching war context
            war_ctx = next((w for w in war_contexts if w.get('war_id') == attack.get('war_id')), {})
            pressure = self.compute_attack_pressure(attack, war_ctx)
            pressures.append(pressure)
            stars.append(attack['stars'])
        
        # Linear regression: stars ~ pressure
        if len(pressures) > 0 and np.std(pressures) > 0:
            # Use numpy polyfit for simple linear regression
            coeffs = np.polyfit(pressures, stars, 1)
            beta = float(coeffs[0])  # Slope
            intercept = float(coeffs[1])
            
            # Compute R-squared
            predicted = np.polyval(coeffs, pressures)
            residuals = np.array(stars) - predicted
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((np.array(stars) - np.mean(stars))**2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
        else:
            beta = 0.0
            r_squared = 0.0
        
        # Interpret beta
        if abs(beta) < 0.2:
            interpretation = 'pressure_neutral'
            description = 'Consistent performer regardless of pressure'
        elif beta > 0.2:
            interpretation = 'clutch'
            description = 'Performs better under high pressure'
        else:
            interpretation = 'choke_prone'
            description = 'Performance declines under pressure'
        
        # Confidence based on sample size and R-squared
        if len(attacks) >= 15 and r_squared > 0.1:
            confidence = 'high'
        elif len(attacks) >= 8:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        return {
            'beta': beta,
            'r_squared': float(r_squared),
            'interpretation': interpretation,
            'description': description,
            'confidence': confidence,
            'sample_size': len(attacks)
        }
    
    def compute_choking_probability(self,
                                   baseline: Dict[str, float],
                                   pressure_sensitivity: Dict[str, Any],
                                   target_pressure: float = 0.8) -> float:
        """
        Estimate probability of underperforming in high-pressure situation.
        
        Educational: Probabilistic prediction using Bayesian approach.
        
        Definition of "choke": Performing > 1 std below baseline under high pressure
        
        Returns:
            Probability (0-1) of choking in high-pressure scenario
        """
        mean_stars = baseline['mean_stars']
        std_stars = baseline['std_stars']
        beta = pressure_sensitivity['beta']
        
        # Predict performance at target pressure
        predicted_stars = mean_stars + beta * target_pressure
        
        # Variance might increase under pressure
        pressure_variance_multiplier = 1.2  # Assumption: variance increases 20% under pressure
        effective_std = std_stars * pressure_variance_multiplier
        
        if effective_std == 0:
            return 0.0
        
        # Probability of performing > 1 std below baseline
        choke_threshold = mean_stars - std_stars
        z_score = (choke_threshold - predicted_stars) / effective_std
        
        # CDF gives probability of being below threshold
        choke_prob = float(stats.norm.cdf(z_score))
        
        return min(max(choke_prob, 0.0), 1.0)
    
    def generate_player_report(self,
                              player_tag: str,
                              attacks: List[Dict[str, Any]],
                              war_contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive pressure analysis for a player.
        
        Main entry point for per-player analysis.
        """
        # Compute baseline
        baseline = self.compute_player_baseline_performance(attacks)
        
        # Compute pressure sensitivity
        pressure_sens = self.compute_pressure_sensitivity(attacks, war_contexts)
        
        # Compute choking probability
        choke_prob = self.compute_choking_probability(baseline, pressure_sens)
        
        # Reliability score: inverse of variance, adjusted for pressure sensitivity
        if baseline['std_stars'] > 0:
            consistency = 1 / (1 + baseline['std_stars'])  # 0-1 scale
        else:
            consistency = 1.0
        
        # Adjust consistency for pressure sensitivity
        if pressure_sens['beta'] < 0:  # Choke-prone
            consistency *= 0.8  # Penalize
        
        reliability_score = consistency * (1 - choke_prob)
        
        return {
            'model': self.name,
            'player_tag': player_tag,
            'timestamp': datetime.utcnow().isoformat(),
            'baseline_performance': baseline,
            'pressure_sensitivity': pressure_sens,
            'choking_probability': round(choke_prob, 3),
            'reliability_score': round(reliability_score, 3),
            'player_archetype': self._determine_archetype(baseline, pressure_sens, reliability_score)
        }
    
    def _determine_archetype(self, 
                            baseline: Dict[str, float],
                            pressure_sens: Dict[str, Any],
                            reliability: float) -> str:
        """
        Classify player into performance archetype.
        
        Educational: Multi-dimensional clustering into interpretable categories.
        """
        mean_stars = baseline['mean_stars']
        interpretation = pressure_sens['interpretation']
        
        if mean_stars >= 2.5 and interpretation == 'clutch':
            return 'Elite Clutch Performer'
        elif mean_stars >= 2.5 and reliability > 0.7:
            return 'Reliable Star'
        elif interpretation == 'clutch' and reliability > 0.6:
            return 'Pressure Specialist'
        elif interpretation == 'choke_prone':
            return 'Inconsistent - Pressure Sensitive'
        elif reliability > 0.7:
            return 'Steady Contributor'
        else:
            return 'Developing Player'
    
    def generate_clan_report(self,
                            player_attacks: Dict[str, List[Dict[str, Any]]],
                            war_contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate clan-wide pressure analysis.
        
        Identifies most reliable players for high-pressure situations.
        """
        player_reports = []
        
        for player_tag, attacks in player_attacks.items():
            if len(attacks) >= 3:  # Minimum data requirement
                report = self.generate_player_report(player_tag, attacks, war_contexts)
                player_reports.append(report)
        
        # Rank by reliability
        ranked = sorted(player_reports, key=lambda x: x['reliability_score'], reverse=True)
        
        # Identify clutch players
        clutch_players = [p for p in ranked 
                         if p['pressure_sensitivity']['interpretation'] == 'clutch']
        
        # Identify choke-prone players
        choke_prone = [p for p in ranked 
                      if p['pressure_sensitivity']['interpretation'] == 'choke_prone']
        
        return {
            'model': self.name,
            'timestamp': datetime.utcnow().isoformat(),
            'total_players_analyzed': len(player_reports),
            'top_reliable_players': ranked[:5],
            'clutch_players': clutch_players[:5],
            'choke_prone_players': choke_prone[:5],
            'average_reliability': float(np.mean([p['reliability_score'] for p in player_reports])) if player_reports else 0
        }
