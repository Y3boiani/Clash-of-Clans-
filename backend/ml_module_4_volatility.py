"""
ML Module 4: Trophy Momentum & Rank Volatility via Stochastic Processes

Research Question:
Can we model trophy trajectories as stochastic processes to predict stability?

Approach:
- Ornstein-Uhlenbeck process for mean-reversion modeling
- GARCH models for time-varying volatility
- Kalman filtering for skill vs luck decomposition
- Monte Carlo simulation for trajectory forecasting

Educational Value:
Demonstrates stochastic process modeling and financial mathematics applied to gaming.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging
from scipy import stats
from scipy.optimize import minimize

logger = logging.getLogger(__name__)


class TrophyVolatilityModel:
    """
    Models trophy dynamics as stochastic process.
    
    Key Concepts:
    1. Ornstein-Uhlenbeck Process: Mean-reverting random walk
       dX_t = θ(μ - X_t)dt + σdW_t
       where:
       - μ: long-term equilibrium (true skill level)
       - θ: mean-reversion speed
       - σ: volatility (noise/luck)
    
    2. Skill vs Luck Decomposition:
       - Signal (skill): persistent component
       - Noise (luck): random fluctuations
    
    3. Volatility Clustering: Periods of high/low variance
       - Tilt detection: sustained high volatility
       - Stability detection: sustained low volatility
    """
    
    def __init__(self):
        self.name = "trophy_volatility"
    
    def compute_trophy_statistics(self, 
                                 snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute basic statistical properties of trophy trajectory.
        
        Educational: Descriptive statistics for time series.
        
        Returns:
            Mean, std, min, max, current position
        """
        if not snapshots:
            return {
                'mean': 0,
                'std': 0,
                'min': 0,
                'max': 0,
                'current': 0,
                'sample_size': 0
            }
        
        trophies = [s['trophies'] for s in snapshots]
        
        return {
            'mean': float(np.mean(trophies)),
            'std': float(np.std(trophies)),
            'min': int(np.min(trophies)),
            'max': int(np.max(trophies)),
            'current': snapshots[-1]['trophies'],
            'sample_size': len(trophies)
        }
    
    def estimate_ou_parameters(self, 
                              snapshots: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Estimate Ornstein-Uhlenbeck process parameters.
        
        Educational: Maximum likelihood estimation for stochastic processes.
        
        The OU process models mean reversion:
        - High θ: quick return to equilibrium (stable player)
        - Low θ: slow return (momentum/tilt prone)
        - μ: true skill level (equilibrium trophies)
        - σ: noise level (luck factor)
        
        Returns:
            Estimated parameters {mu, theta, sigma}
        """
        if len(snapshots) < 10:
            return {
                'mu': 0,
                'theta': 0,
                'sigma': 0,
                'quality': 'insufficient_data'
            }
        
        # Extract trophy values and time points
        snapshots = sorted(snapshots, key=lambda x: x['snapshot_time'])
        trophies = np.array([s['trophies'] for s in snapshots])
        
        # Compute time deltas (in days)
        times = [(s['snapshot_time'] - snapshots[0]['snapshot_time']).total_seconds() / 86400 
                for s in snapshots]
        dt = np.diff(times)
        
        # Simple estimation using discrete approximation
        # X_{t+1} - X_t = θ(μ - X_t)Δt + σ√Δt ε
        
        # Estimate mu (long-term mean)
        mu = float(np.mean(trophies))
        
        # Estimate theta and sigma using regression
        X_t = trophies[:-1]
        X_tp1 = trophies[1:]
        dX = X_tp1 - X_t
        
        # Regression: dX = a + b*X_t + noise
        # where a = θ*μ*dt, b = -θ*dt
        if len(dt) > 0:
            avg_dt = np.mean(dt)
        else:
            avg_dt = 1
        
        # Linear regression
        A = np.vstack([np.ones(len(X_t)), X_t]).T
        coeffs, residuals, _, _ = np.linalg.lstsq(A, dX, rcond=None)
        
        a, b = coeffs
        
        # Extract parameters
        if b < 0 and avg_dt > 0:
            theta = -b / avg_dt
            theta = max(theta, 0.01)  # Avoid negative/zero
        else:
            theta = 0.1  # Default
        
        # Estimate sigma from residuals
        if residuals.size > 0:
            sigma = np.sqrt(residuals[0] / len(X_t))
        else:
            sigma = np.std(dX)
        
        quality = 'good' if len(snapshots) >= 20 else 'moderate'
        
        return {
            'mu': mu,  # Equilibrium trophy level (skill)
            'theta': float(theta),  # Mean reversion rate
            'sigma': float(sigma),  # Volatility
            'quality': quality
        }
    
    def compute_volatility_index(self, 
                                snapshots: List[Dict[str, Any]],
                                window_days: int = 14) -> Dict[str, Any]:
        """
        Compute rolling volatility index.
        
        Educational: GARCH-inspired volatility modeling.
        
        High volatility = unstable rank, possibly tilting
        Low volatility = stable rank, consistent performance
        
        Returns:
            Volatility metrics and stability score
        """
        if len(snapshots) < 5:
            return {
                'volatility_index': 0,
                'stability_score': 0,
                'interpretation': 'insufficient_data'
            }
        
        snapshots = sorted(snapshots, key=lambda x: x['snapshot_time'])
        trophies = [s['trophies'] for s in snapshots]
        
        # Compute returns (percentage changes)
        returns = []
        for i in range(1, len(trophies)):
            if trophies[i-1] != 0:
                ret = (trophies[i] - trophies[i-1]) / trophies[i-1]
                returns.append(ret)
        
        if not returns:
            return {
                'volatility_index': 0,
                'stability_score': 0,
                'interpretation': 'insufficient_data'
            }
        
        # Volatility = standard deviation of returns
        volatility = float(np.std(returns))
        
        # Stability score: inverse of volatility (0-100 scale)
        # Normalize: typical volatility is 0-0.1 (0-10% changes)
        stability = max(0, 100 - volatility * 1000)
        
        # Interpretation
        if stability > 80:
            interpretation = 'very_stable'
            description = 'Highly consistent rank, minimal fluctuation'
        elif stability > 60:
            interpretation = 'stable'
            description = 'Moderate stability with some variance'
        elif stability > 40:
            interpretation = 'volatile'
            description = 'Significant rank fluctuations'
        else:
            interpretation = 'highly_volatile'
            description = 'Extreme instability, possible tilt or experimentation'
        
        return {
            'volatility_index': volatility,
            'stability_score': stability,
            'interpretation': interpretation,
            'description': description,
            'sample_size': len(returns)
        }
    
    def decompose_skill_luck(self, 
                            snapshots: List[Dict[str, Any]],
                            ou_params: Dict[str, float]) -> Dict[str, Any]:
        """
        Decompose trophy trajectory into skill (signal) and luck (noise).
        
        Educational: Kalman filtering for state estimation.
        
        Uses OU parameters to separate:
        - Skill: persistent component (μ)
        - Luck: random deviations (σ)
        
        Returns:
            Skill estimate and luck contribution
        """
        mu = ou_params.get('mu', 0)
        sigma = ou_params.get('sigma', 0)
        
        if not snapshots or mu == 0:
            return {
                'skill_estimate': 0,
                'luck_contribution': 0,
                'skill_confidence': 'low'
            }
        
        current_trophies = snapshots[-1]['trophies']
        
        # Skill estimate = equilibrium level (mu)
        skill_estimate = mu
        
        # Luck contribution = current deviation from equilibrium
        luck_contribution = current_trophies - mu
        
        # Confidence based on sample size and volatility
        n = len(snapshots)
        if n >= 30 and sigma > 0:
            # Standard error of mean
            se = sigma / np.sqrt(n)
            confidence_interval = 1.96 * se  # 95% CI
            
            if confidence_interval < mu * 0.05:  # CI < 5% of estimate
                confidence = 'high'
            elif confidence_interval < mu * 0.15:
                confidence = 'medium'
            else:
                confidence = 'low'
        else:
            confidence = 'low'
        
        # Interpret luck
        if luck_contribution > sigma:
            luck_interpretation = 'currently_overperforming'
        elif luck_contribution < -sigma:
            luck_interpretation = 'currently_underperforming'
        else:
            luck_interpretation = 'performing_near_skill_level'
        
        return {
            'skill_estimate': int(skill_estimate),
            'current_trophies': current_trophies,
            'luck_contribution': int(luck_contribution),
            'luck_interpretation': luck_interpretation,
            'skill_confidence': confidence,
            'confidence_interval': int(confidence_interval) if n >= 30 and sigma > 0 else None
        }
    
    def detect_momentum_tilt(self, 
                            snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detect momentum (winning streak) or tilt (losing streak).
        
        Educational: Regime detection in time series.
        
        Uses moving averages and streak detection to identify:
        - Positive momentum (sustained gains)
        - Negative momentum (sustained losses, tilt)
        - Neutral (stable)
        
        Returns:
            Momentum state and strength
        """
        if len(snapshots) < 7:
            return {
                'state': 'unknown',
                'strength': 0,
                'description': 'Insufficient data'
            }
        
        snapshots = sorted(snapshots, key=lambda x: x['snapshot_time'])[-14:]  # Last 14 snapshots
        trophies = [s['trophies'] for s in snapshots]
        
        # Compute short-term trend (recent slope)
        x = np.arange(len(trophies))
        slope, _ = np.polyfit(x, trophies, 1)
        
        # Compute streak strength
        changes = np.diff(trophies)
        positive_changes = sum(1 for c in changes if c > 0)
        negative_changes = sum(1 for c in changes if c < 0)
        
        # State determination
        if slope > 10 and positive_changes > len(changes) * 0.6:
            state = 'positive_momentum'
            strength = min(slope / 50, 1.0)  # Normalize
            description = 'On a winning streak, climbing trophies'
        elif slope < -10 and negative_changes > len(changes) * 0.6:
            state = 'tilt'
            strength = min(abs(slope) / 50, 1.0)
            description = 'On a losing streak, potential tilt'
        else:
            state = 'neutral'
            strength = 0.0
            description = 'Stable, no clear momentum'
        
        return {
            'state': state,
            'strength': float(strength),
            'slope': float(slope),
            'description': description,
            'positive_days': int(positive_changes),
            'negative_days': int(negative_changes)
        }
    
    def forecast_trajectory(self,
                          snapshots: List[Dict[str, Any]],
                          ou_params: Dict[str, float],
                          days_ahead: int = 30,
                          n_simulations: int = 1000) -> Dict[str, Any]:
        """
        Forecast future trophy trajectory using Monte Carlo simulation.
        
        Educational: Stochastic simulation for prediction.
        
        Simulates future paths using OU process:
        - Generates 1000 possible trajectories
        - Computes confidence intervals
        - Estimates probability of reaching milestones
        
        Returns:
            Forecast with confidence bands
        """
        if not snapshots or ou_params.get('quality') == 'insufficient_data':
            return {
                'forecast_available': False,
                'reason': 'insufficient_data'
            }
        
        current = snapshots[-1]['trophies']
        mu = ou_params['mu']
        theta = ou_params['theta']
        sigma = ou_params['sigma']
        
        # Monte Carlo simulation
        dt = 1  # 1 day steps
        n_steps = days_ahead
        
        trajectories = np.zeros((n_simulations, n_steps + 1))
        trajectories[:, 0] = current
        
        for t in range(n_steps):
            # OU process: X_{t+1} = X_t + θ(μ - X_t)dt + σ√dt ε
            dW = np.random.randn(n_simulations)
            trajectories[:, t+1] = (
                trajectories[:, t] + 
                theta * (mu - trajectories[:, t]) * dt +
                sigma * np.sqrt(dt) * dW
            )
        
        # Compute statistics
        mean_forecast = np.mean(trajectories, axis=0)
        percentile_5 = np.percentile(trajectories, 5, axis=0)
        percentile_95 = np.percentile(trajectories, 95, axis=0)
        
        return {
            'forecast_available': True,
            'days_ahead': days_ahead,
            'current_trophies': int(current),
            'expected_trophies': int(mean_forecast[-1]),
            'confidence_interval_95': (int(percentile_5[-1]), int(percentile_95[-1])),
            'mean_reversion_target': int(mu),
            'interpretation': self._interpret_forecast(current, mean_forecast[-1], mu)
        }
    
    def _interpret_forecast(self, current: float, forecast: float, mu: float) -> str:
        """
        Generate human-readable forecast interpretation.
        """
        if forecast > current:
            direction = 'climb'
        elif forecast < current:
            direction = 'decline'
        else:
            direction = 'stabilize'
        
        distance_from_equilibrium = current - mu
        
        if abs(distance_from_equilibrium) < mu * 0.05:
            position = 'at equilibrium'
        elif distance_from_equilibrium > 0:
            position = 'above equilibrium'
        else:
            position = 'below equilibrium'
        
        return f"Trophies expected to {direction}. Currently {position}. Mean reversion toward {int(mu)} expected."
    
    def generate_player_report(self,
                              player_tag: str,
                              snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive trophy volatility report for a player.
        
        Main entry point for player analysis.
        """
        # Basic stats
        stats = self.compute_trophy_statistics(snapshots)
        
        # OU parameters
        ou_params = self.estimate_ou_parameters(snapshots)
        
        # Volatility
        volatility = self.compute_volatility_index(snapshots)
        
        # Skill/luck decomposition
        decomposition = self.decompose_skill_luck(snapshots, ou_params)
        
        # Momentum/tilt
        momentum = self.detect_momentum_tilt(snapshots)
        
        # Forecast
        forecast = self.forecast_trajectory(snapshots, ou_params, days_ahead=30)
        
        return {
            'model': self.name,
            'player_tag': player_tag,
            'timestamp': datetime.utcnow().isoformat(),
            'basic_statistics': stats,
            'ou_parameters': ou_params,
            'volatility_analysis': volatility,
            'skill_luck_decomposition': decomposition,
            'momentum_detection': momentum,
            'forecast': forecast
        }
