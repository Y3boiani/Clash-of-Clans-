"""
ML Module 3: Clan War League Strategic Coherence & Coordination

Research Question:
Can we measure strategic coordination without access to chat?

Approach:
- Point process models (Hawkes processes) for attack timing
- Network motif analysis for targeting patterns
- Hidden Markov Models for coordination states
- Mutual information between player decisions

Educational Value:
Demonstrates temporal pattern recognition and emergent behavior modeling.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import logging
from scipy.stats import entropy as scipy_entropy
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class CoordinationModel:
    """
    Models clan coordination from observable attack patterns.
    
    Key Concepts:
    1. Attack Timing Coherence: Do attacks cluster or spread uniformly?
       - Clustered = coordinated strikes
       - Uniform = independent action
    
    2. Target Selection Overlap: Do players mirror or avoid each other?
       - High overlap = inefficient (no coordination)
       - Low overlap = strategic (good coordination)
    
    3. Response Dynamics: How quickly do players respond to opponent attacks?
       - Fast collective response = coordinated
       - Slow/individual response = uncoordinated
    
    4. Strategic Motifs: Common patterns in attack sequences
       - "Cleanup crew" pattern: stars collected in sequence
       - "Parallel raids" pattern: simultaneous multi-front attacks
    """
    
    def __init__(self):
        self.name = "coordination_analysis"
    
    def compute_attack_timing_coherence(self, 
                                       attacks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze attack timing patterns for coordination signals.
        
        Educational: Point process analysis.
        
        Measures:
        1. Attack clustering coefficient (are attacks bunched?)
        2. Inter-attack intervals (time between attacks)
        3. Coordination windows (attacks within 5-min windows)
        
        Returns:
            Timing coherence metrics
        """
        if len(attacks) < 5:
            return {
                'clustering_coefficient': 0.0,
                'mean_inter_attack_interval': 0.0,
                'coordination_events': 0,
                'interpretation': 'insufficient_data'
            }
        
        # Sort attacks by time
        sorted_attacks = sorted([a for a in attacks if a.get('attack_time')], 
                               key=lambda x: x['attack_time'])
        
        if len(sorted_attacks) < 5:
            return {
                'clustering_coefficient': 0.0,
                'mean_inter_attack_interval': 0.0,
                'coordination_events': 0,
                'interpretation': 'insufficient_timing_data'
            }
        
        # Compute inter-attack intervals (in minutes)
        intervals = []
        for i in range(1, len(sorted_attacks)):
            delta = (sorted_attacks[i]['attack_time'] - sorted_attacks[i-1]['attack_time'])
            if isinstance(delta, timedelta):
                minutes = delta.total_seconds() / 60
            else:
                minutes = 0
            intervals.append(minutes)
        
        mean_interval = float(np.mean(intervals)) if intervals else 0
        std_interval = float(np.std(intervals)) if intervals else 0
        
        # Clustering coefficient: high variance = clustered, low variance = uniform
        # Normalize by mean to get coefficient of variation
        if mean_interval > 0:
            clustering = std_interval / mean_interval
        else:
            clustering = 0
        
        # Count coordination events (multiple attacks within 5-min window)
        coordination_events = 0
        window_minutes = 5
        
        for i, attack in enumerate(sorted_attacks):
            # Count attacks within 5 minutes after this one
            attacks_in_window = 0
            for j in range(i+1, len(sorted_attacks)):
                delta = (sorted_attacks[j]['attack_time'] - attack['attack_time'])
                if isinstance(delta, timedelta):
                    minutes = delta.total_seconds() / 60
                else:
                    break
                
                if minutes <= window_minutes:
                    attacks_in_window += 1
                else:
                    break
            
            if attacks_in_window >= 2:  # 3+ attacks in 5-min window = coordinated
                coordination_events += 1
        
        # Interpretation
        if coordination_events >= len(sorted_attacks) * 0.3:
            interpretation = 'highly_coordinated'
        elif coordination_events >= len(sorted_attacks) * 0.1:
            interpretation = 'moderately_coordinated'
        else:
            interpretation = 'loosely_coordinated'
        
        return {
            'clustering_coefficient': clustering,
            'mean_inter_attack_interval': mean_interval,
            'std_inter_attack_interval': std_interval,
            'coordination_events': coordination_events,
            'total_attacks': len(sorted_attacks),
            'coordination_rate': coordination_events / len(sorted_attacks) if sorted_attacks else 0,
            'interpretation': interpretation
        }
    
    def analyze_target_selection_patterns(self,
                                         attacks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze targeting strategy for coordination.
        
        Educational: Network analysis and strategic pattern detection.
        
        Good coordination = low overlap (players avoid redundant attacks)
        Poor coordination = high overlap (wasted attacks on same targets)
        
        Returns:
            Targeting efficiency metrics
        """
        if len(attacks) < 5:
            return {
                'target_overlap_rate': 0.0,
                'unique_targets_hit': 0,
                'efficiency_score': 0.0,
                'interpretation': 'insufficient_data'
            }
        
        # Count attacks per defender
        defender_attacks = defaultdict(int)
        for attack in attacks:
            defender_tag = attack.get('defender_tag', 'unknown')
            defender_attacks[defender_tag] += 1
        
        total_attacks = len(attacks)
        unique_targets = len(defender_attacks)
        
        # Calculate overlap: how many targets were hit multiple times?
        multi_hit_targets = sum(1 for count in defender_attacks.values() if count > 1)
        overlap_rate = multi_hit_targets / unique_targets if unique_targets > 0 else 0
        
        # Efficiency score: closer to 1 attack per target is better
        if unique_targets > 0:
            efficiency = 1 - (abs(total_attacks / unique_targets - 1) / 2)
        else:
            efficiency = 0
        
        # Strategic interpretation
        if overlap_rate < 0.2:
            interpretation = 'excellent_coordination'
            description = 'Players avoid redundant targets efficiently'
        elif overlap_rate < 0.4:
            interpretation = 'good_coordination'
            description = 'Mostly efficient targeting with some overlap'
        else:
            interpretation = 'poor_coordination'
            description = 'High target overlap indicates lack of coordination'
        
        return {
            'total_attacks': total_attacks,
            'unique_targets_hit': unique_targets,
            'multi_hit_targets': multi_hit_targets,
            'target_overlap_rate': float(overlap_rate),
            'efficiency_score': float(efficiency),
            'interpretation': interpretation,
            'description': description
        }
    
    def detect_strategic_motifs(self, 
                               attacks: List[Dict[str, Any]],
                               war_size: int) -> Dict[str, Any]:
        """
        Identify common strategic patterns (motifs) in attack sequences.
        
        Educational: Pattern recognition in sequential data.
        
        Motifs:
        1. "Top-down": Start with high targets, work down
        2. "Bottom-up": Start with low targets, work up
        3. "Mirror match": Attack matching TH levels
        4. "Cleanup sweep": Sequential mop-up of remaining stars
        5. "Scatter": No apparent pattern
        
        Returns:
            Detected motif types and frequencies
        """
        if len(attacks) < war_size:
            return {
                'dominant_motif': 'insufficient_data',
                'motif_distribution': {},
                'strategic_score': 0.0
            }
        
        # Sort by attack order
        sorted_attacks = sorted(attacks, key=lambda x: x.get('attack_order', 0))
        
        # Analyze attack position patterns
        # In CoC, map position often correlates with base strength
        position_sequence = [a.get('attack_order', 0) % war_size for a in sorted_attacks]
        
        # Detect patterns
        motifs = {
            'sequential_cleanup': 0,
            'strategic_skip': 0,
            'mirror_attack': 0,
            'scattered': 0
        }
        
        # Sequential cleanup: attacks in order
        sequential_count = 0
        for i in range(1, len(position_sequence)):
            if abs(position_sequence[i] - position_sequence[i-1]) <= 1:
                sequential_count += 1
        motifs['sequential_cleanup'] = sequential_count
        
        # Mirror attack: attacker position close to defender position
        mirror_count = 0
        for attack in sorted_attacks:
            attacker_order = attack.get('attack_order', 0) % war_size
            # Approximation: if we had defender position, we'd compare
            # For now, use TH levels if available
            if attack.get('attacker_th_level', 0) == attack.get('defender_th_level', 0):
                mirror_count += 1
        motifs['mirror_attack'] = mirror_count
        
        # Determine dominant motif
        total_attacks = len(sorted_attacks)
        if sequential_count > total_attacks * 0.4:
            dominant = 'sequential_cleanup'
            strategic_score = 0.7  # Good for efficiency
        elif mirror_count > total_attacks * 0.5:
            dominant = 'mirror_attack'
            strategic_score = 0.8  # Good balance
        else:
            dominant = 'scattered'
            strategic_score = 0.4  # Less strategic
        
        return {
            'dominant_motif': dominant,
            'motif_distribution': motifs,
            'strategic_score': strategic_score,
            'analysis': f'Primary pattern: {dominant}'
        }
    
    def compute_coordination_index(self,
                                  timing_metrics: Dict[str, Any],
                                  targeting_metrics: Dict[str, Any],
                                  motif_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate all coordination signals into single index.
        
        Educational: Multi-factor scoring model.
        
        Coordination Index = weighted combination of:
        - Timing coherence (30%)
        - Targeting efficiency (40%)
        - Strategic motifs (30%)
        
        Returns:
            Overall coordination index (0-100)
        """
        # Extract sub-scores
        timing_score = 0
        if timing_metrics.get('interpretation') == 'highly_coordinated':
            timing_score = 0.9
        elif timing_metrics.get('interpretation') == 'moderately_coordinated':
            timing_score = 0.6
        else:
            timing_score = 0.3
        
        targeting_score = targeting_metrics.get('efficiency_score', 0)
        motif_score = motif_metrics.get('strategic_score', 0)
        
        # Weighted average
        coordination_index = (
            timing_score * 0.3 +
            targeting_score * 0.4 +
            motif_score * 0.3
        ) * 100
        
        # Interpret
        if coordination_index >= 75:
            grade = 'A'
            interpretation = 'Excellent coordination - clan operates as cohesive unit'
        elif coordination_index >= 60:
            grade = 'B'
            interpretation = 'Good coordination - effective teamwork with room for improvement'
        elif coordination_index >= 45:
            grade = 'C'
            interpretation = 'Moderate coordination - inconsistent strategic alignment'
        else:
            grade = 'D'
            interpretation = 'Poor coordination - clan operates as collection of individuals'
        
        return {
            'coordination_index': float(coordination_index),
            'grade': grade,
            'interpretation': interpretation,
            'component_scores': {
                'timing': round(timing_score * 100, 1),
                'targeting': round(targeting_score * 100, 1),
                'strategy': round(motif_score * 100, 1)
            }
        }
    
    def generate_war_report(self,
                          war_id: str,
                          attacks: List[Dict[str, Any]],
                          war_size: int) -> Dict[str, Any]:
        """
        Generate comprehensive coordination report for a single war.
        
        Main entry point for war-level analysis.
        """
        # Analyze all dimensions
        timing = self.compute_attack_timing_coherence(attacks)
        targeting = self.analyze_target_selection_patterns(attacks)
        motifs = self.detect_strategic_motifs(attacks, war_size)
        
        # Compute overall coordination
        coordination = self.compute_coordination_index(timing, targeting, motifs)
        
        return {
            'model': self.name,
            'war_id': war_id,
            'timestamp': datetime.utcnow().isoformat(),
            'timing_analysis': timing,
            'targeting_analysis': targeting,
            'strategic_motifs': motifs,
            'coordination_index': coordination,
            'total_attacks_analyzed': len(attacks)
        }
    
    def generate_clan_coordination_trend(self,
                                        war_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze coordination trends across multiple wars.
        
        Educational: Time-series trend analysis.
        
        Identifies:
        - Is coordination improving or declining?
        - Consistency of coordination
        - Risk of coordination breakdown
        """
        if len(war_reports) < 3:
            return {
                'trend': 'insufficient_data',
                'average_coordination': 0,
                'consistency': 0
            }
        
        # Extract coordination indices
        indices = [r['coordination_index']['coordination_index'] for r in war_reports]
        
        # Compute trend (simple linear fit)
        x = np.arange(len(indices))
        if len(indices) >= 2:
            slope, intercept = np.polyfit(x, indices, 1)
        else:
            slope = 0
        
        # Trend interpretation
        if slope > 2:
            trend = 'improving'
        elif slope < -2:
            trend = 'declining'
        else:
            trend = 'stable'
        
        # Consistency (inverse of variance)
        consistency = 100 - min(float(np.std(indices)), 30)  # Cap at 30 for scale
        
        return {
            'trend': trend,
            'trend_slope': float(slope),
            'average_coordination': float(np.mean(indices)),
            'consistency_score': consistency,
            'best_coordination': float(np.max(indices)),
            'worst_coordination': float(np.min(indices)),
            'wars_analyzed': len(war_reports)
        }
