"""
ML Module 5: Donation Economy & Resource Flow Network Analysis

Research Question:
Can we model clan economies as directed graphs to detect exploitation?

Approach:
- Directed graph analysis with weighted edges
- PageRank for identifying key resource providers
- Community detection for donation cliques
- Gini coefficient for inequality measurement
- Survival analysis for retention vs donation balance

Educational Value:
Demonstrates graph analytics and economic network theory.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DonationNetworkModel:
    """
    Models clan donation economy as resource flow network.
    
    Key Concepts:
    1. Directed Graph: 
       - Nodes = players
       - Edges = donation flows (inferred from deltas)
       - Edge weight = donation volume
    
    2. Network Roles:
       - Benefactor: High out-degree (gives much more than receives)
       - Balanced: In-degree ≈ Out-degree
       - Parasite: High in-degree (receives much more than gives)
       - Inactive: Low degree overall
    
    3. Economic Health Metrics:
       - Gini coefficient: Inequality in giving/receiving
       - Network centrality: Who are critical providers?
       - Reciprocity index: Balance of give-and-take
       - Sustainability: Are parasites driving away benefactors?
    """
    
    def __init__(self):
        self.name = "donation_network"
    
    def build_donation_graph(self,
                           player_snapshots: List[Dict[str, Any]],
                           clan_tag: str) -> Dict[str, Any]:
        """
        Build donation network graph from player snapshots.
        
        Educational: Graph construction from time-series data.
        
        Since API doesn't tell us who donated to whom, we:
        1. Track each player's donation giving/receiving over time
        2. Build nodes with net donation statistics
        3. Infer network structure from aggregate patterns
        
        Returns:
            Graph structure with nodes and aggregated metrics
        """
        # Group snapshots by player
        player_data = defaultdict(list)
        for snap in player_snapshots:
            if snap.get('clan_tag') == clan_tag:
                player_data[snap['player_tag']].append(snap)
        
        nodes = []
        
        for player_tag, snapshots in player_data.items():
            if not snapshots:
                continue
            
            # Sort by time
            snapshots = sorted(snapshots, key=lambda x: x['snapshot_time'])
            latest = snapshots[-1]
            
            # Current donation stats
            donations_given = latest.get('donations', 0)
            donations_received = latest.get('donations_received', 0)
            net_donations = donations_given - donations_received
            
            # Donation velocity (donations per day)
            if len(snapshots) >= 2:
                days = (snapshots[-1]['snapshot_time'] - snapshots[0]['snapshot_time']).days
                if days > 0:
                    velocity_given = (snapshots[-1]['donations'] - snapshots[0]['donations']) / days
                    velocity_received = (snapshots[-1]['donations_received'] - snapshots[0]['donations_received']) / days
                else:
                    velocity_given = 0
                    velocity_received = 0
            else:
                velocity_given = 0
                velocity_received = 0
            
            # Classify role
            role = self._classify_donation_role(donations_given, donations_received)
            
            nodes.append({
                'player_tag': player_tag,
                'player_name': latest['name'],
                'donations_given': donations_given,
                'donations_received': donations_received,
                'net_donations': net_donations,
                'donation_ratio': donations_given / max(donations_received, 1),
                'velocity_given': velocity_given,
                'velocity_received': velocity_received,
                'role': role,
                'snapshots_count': len(snapshots)
            })
        
        return {
            'nodes': nodes,
            'total_members': len(nodes),
            'graph_type': 'directed_weighted'
        }
    
    def _classify_donation_role(self, given: int, received: int) -> str:
        """
        Classify player's role in donation economy.
        
        Educational: Threshold-based classification.
        """
        if given == 0 and received == 0:
            return 'inactive'
        
        ratio = given / max(received, 1)
        
        if ratio >= 2.0:
            return 'benefactor'
        elif ratio >= 0.8:
            return 'balanced'
        elif ratio >= 0.3:
            return 'mild_parasite'
        else:
            return 'parasite'
    
    def compute_network_centrality(self,
                                  graph: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Compute centrality scores for network nodes.
        
        Educational: PageRank-style importance ranking.
        
        High centrality = critical to clan economy
        If high centrality player leaves, donation economy collapses.
        
        Returns:
            Nodes ranked by centrality (importance)
        """
        nodes = graph['nodes']
        
        if not nodes:
            return []
        
        # Compute simple centrality based on:
        # 1. Absolute giving (volume)
        # 2. Net giving (generosity)
        # 3. Consistency (velocity)
        
        for node in nodes:
            # Centrality score components
            volume_score = min(node['donations_given'] / 1000, 1.0)  # Normalize by 1000
            generosity_score = min(max(node['net_donations'], 0) / 500, 1.0)
            consistency_score = min(node['velocity_given'] / 10, 1.0)
            
            # Weighted combination
            centrality = (
                volume_score * 0.5 +
                generosity_score * 0.3 +
                consistency_score * 0.2
            )
            
            node['centrality_score'] = centrality
        
        # Rank by centrality
        ranked = sorted(nodes, key=lambda x: x['centrality_score'], reverse=True)
        
        return ranked
    
    def compute_economic_inequality(self,
                                   graph: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute inequality metrics for donation distribution.
        
        Educational: Gini coefficient and Lorenz curve.
        
        Gini = 0: Perfect equality (everyone gives/receives equally)
        Gini = 1: Perfect inequality (one person does all giving)
        
        Returns:
            Inequality metrics and interpretation
        """
        nodes = graph['nodes']
        
        if not nodes:
            return {
                'gini_giving': 0,
                'gini_receiving': 0,
                'interpretation': 'no_data'
            }
        
        # Extract giving and receiving distributions
        giving = [n['donations_given'] for n in nodes]
        receiving = [n['donations_received'] for n in nodes]
        
        # Compute Gini coefficients
        gini_giving = self._compute_gini(giving)
        gini_receiving = self._compute_gini(receiving)
        
        # Interpret
        if gini_giving < 0.3:
            giving_interp = 'equal'
            giving_desc = 'Donations distributed evenly across members'
        elif gini_giving < 0.5:
            giving_interp = 'moderate'
            giving_desc = 'Some members give significantly more than others'
        else:
            giving_interp = 'concentrated'
            giving_desc = 'Donation giving highly concentrated in few members'
        
        # Health assessment
        if gini_giving > 0.6:
            health_status = 'at_risk'
            health_desc = 'High dependence on few benefactors - retention risk'
        elif gini_giving > 0.4:
            health_status = 'moderate'
            health_desc = 'Moderate inequality - encourage broader participation'
        else:
            health_status = 'healthy'
            health_desc = 'Good distribution of giving responsibility'
        
        return {
            'gini_giving': float(gini_giving),
            'gini_receiving': float(gini_receiving),
            'giving_interpretation': giving_interp,
            'giving_description': giving_desc,
            'health_status': health_status,
            'health_description': health_desc
        }
    
    def _compute_gini(self, values: List[float]) -> float:
        """
        Compute Gini coefficient.
        
        Educational: Economic inequality metric.
        """
        if not values or sum(values) == 0:
            return 0.0
        
        sorted_values = sorted([v for v in values if v >= 0])
        n = len(sorted_values)
        
        if n == 0:
            return 0.0
        
        cumsum = np.cumsum(sorted_values)
        
        # Gini formula
        gini = (2 * sum((i + 1) * val for i, val in enumerate(sorted_values))) / (n * sum(sorted_values)) - (n + 1) / n
        return max(0, min(float(gini), 1.0))
    
    def detect_parasites(self,
                        graph: Dict[str, Any],
                        threshold_ratio: float = 0.3) -> List[Dict[str, Any]]:
        """
        Identify parasitic members (take much more than give).
        
        Educational: Threshold-based anomaly detection.
        
        Returns:
            List of parasitic members with exploitation metrics
        """
        nodes = graph['nodes']
        parasites = []
        
        for node in nodes:
            ratio = node['donation_ratio']
            role = node['role']
            
            if role in ['parasite', 'mild_parasite'] and ratio < threshold_ratio:
                exploitation_score = 1 - ratio  # Higher = more exploitative
                
                parasites.append({
                    'player_tag': node['player_tag'],
                    'player_name': node['player_name'],
                    'donations_given': node['donations_given'],
                    'donations_received': node['donations_received'],
                    'donation_ratio': ratio,
                    'exploitation_score': exploitation_score,
                    'role': role
                })
        
        # Sort by exploitation score
        parasites.sort(key=lambda x: x['exploitation_score'], reverse=True)
        
        return parasites
    
    def predict_retention_risk(self,
                             graph: Dict[str, Any],
                             player_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predict member retention risk based on donation imbalance.
        
        Educational: Survival analysis concept.
        
        Hypothesis: Players who feel exploited (give much more than receive)
        are more likely to leave.
        
        Returns:
            Risk scores per player and overall clan risk
        """
        nodes = graph['nodes']
        
        risk_scores = []
        
        for node in nodes:
            player_tag = node['player_tag']
            role = node['role']
            net_donations = node['net_donations']
            
            # Benefactors giving too much may burn out
            if role == 'benefactor' and net_donations > 1000:
                risk = min(net_donations / 2000, 1.0)
                risk_type = 'burnout'
            # Parasites may be asked to leave
            elif role in ['parasite', 'mild_parasite']:
                risk = node.get('exploitation_score', 0.5)
                risk_type = 'exploitation'
            # Inactive may naturally drift away
            elif role == 'inactive':
                risk = 0.6
                risk_type = 'disengagement'
            else:
                risk = 0.2  # Balanced players are stable
                risk_type = 'low'
            
            risk_scores.append({
                'player_tag': player_tag,
                'player_name': node['player_name'],
                'risk_score': risk,
                'risk_type': risk_type,
                'role': role
            })
        
        # Overall clan risk: weighted average
        if risk_scores:
            avg_risk = float(np.mean([r['risk_score'] for r in risk_scores]))
        else:
            avg_risk = 0.0
        
        # Identify high-risk members
        high_risk = [r for r in risk_scores if r['risk_score'] > 0.6]
        
        return {
            'average_clan_risk': avg_risk,
            'high_risk_members': len(high_risk),
            'high_risk_players': sorted(high_risk, key=lambda x: x['risk_score'], reverse=True)[:10],
            'total_analyzed': len(risk_scores)
        }
    
    def compute_reciprocity_index(self,
                                 graph: Dict[str, Any]) -> Dict[str, float]:
        """
        Compute clan-wide reciprocity index.
        
        Educational: Network balance metric.
        
        High reciprocity = healthy give-and-take
        Low reciprocity = imbalanced, exploitative
        
        Returns:
            Reciprocity metrics
        """
        nodes = graph['nodes']
        
        if not nodes:
            return {'reciprocity_index': 0, 'interpretation': 'no_data'}
        
        # Count role distribution
        role_counts = defaultdict(int)
        for node in nodes:
            role_counts[node['role']] += 1
        
        total = len(nodes)
        balanced_ratio = role_counts['balanced'] / total if total > 0 else 0
        parasite_ratio = (role_counts['parasite'] + role_counts['mild_parasite']) / total if total > 0 else 0
        benefactor_ratio = role_counts['benefactor'] / total if total > 0 else 0
        
        # Reciprocity index: high when most players are balanced
        reciprocity = balanced_ratio - (parasite_ratio * 0.5)
        reciprocity = max(0, min(reciprocity, 1.0))
        
        # Interpret
        if reciprocity > 0.6:
            interpretation = 'healthy'
        elif reciprocity > 0.3:
            interpretation = 'moderate'
        else:
            interpretation = 'poor'
        
        return {
            'reciprocity_index': float(reciprocity),
            'interpretation': interpretation,
            'role_distribution': {
                'benefactors': benefactor_ratio,
                'balanced': balanced_ratio,
                'parasites': parasite_ratio,
                'inactive': role_counts['inactive'] / total if total > 0 else 0
            }
        }
    
    def generate_clan_report(self,
                           player_snapshots: List[Dict[str, Any]],
                           clan_tag: str) -> Dict[str, Any]:
        """
        Generate comprehensive donation economy report for a clan.
        
        Main entry point for clan analysis.
        """
        # Build graph
        graph = self.build_donation_graph(player_snapshots, clan_tag)
        
        # Compute centrality
        ranked_nodes = self.compute_network_centrality(graph)
        
        # Economic inequality
        inequality = self.compute_economic_inequality(graph)
        
        # Detect parasites
        parasites = self.detect_parasites(graph)
        
        # Retention risk
        retention = self.predict_retention_risk(graph, player_snapshots)
        
        # Reciprocity
        reciprocity = self.compute_reciprocity_index(graph)
        
        return {
            'model': self.name,
            'clan_tag': clan_tag,
            'timestamp': datetime.utcnow().isoformat(),
            'network_stats': {
                'total_members': graph['total_members'],
                'total_giving': sum(n['donations_given'] for n in graph['nodes']),
                'total_receiving': sum(n['donations_received'] for n in graph['nodes'])
            },
            'top_contributors': ranked_nodes[:10],
            'economic_inequality': inequality,
            'parasites_detected': len(parasites),
            'parasite_details': parasites[:10],
            'retention_risk': retention,
            'reciprocity': reciprocity,
            'overall_health_score': self._compute_health_score(inequality, reciprocity, retention)
        }
    
    def _compute_health_score(self,
                            inequality: Dict[str, Any],
                            reciprocity: Dict[str, float],
                            retention: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate health score for donation economy.
        
        Educational: Composite scoring model.
        """
        # Lower inequality is better
        inequality_score = 1 - inequality['gini_giving']
        
        # Higher reciprocity is better
        reciprocity_score = reciprocity['reciprocity_index']
        
        # Lower retention risk is better
        retention_score = 1 - retention['average_clan_risk']
        
        # Weighted average
        health = (
            inequality_score * 0.3 +
            reciprocity_score * 0.4 +
            retention_score * 0.3
        ) * 100
        
        if health >= 75:
            grade = 'A'
            interpretation = 'Healthy donation economy'
        elif health >= 60:
            grade = 'B'
            interpretation = 'Good but room for improvement'
        elif health >= 45:
            grade = 'C'
            interpretation = 'Moderate issues detected'
        else:
            grade = 'D'
            interpretation = 'Significant economic imbalances'
        
        return {
            'health_score': float(health),
            'grade': grade,
            'interpretation': interpretation
        }
