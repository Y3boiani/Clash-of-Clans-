#!/usr/bin/env python3
"""
Detailed Backend API Testing for CoC ML Research Platform
Examines response data quality and content validation.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

BACKEND_URL = "https://zero-hassle-ml.preview.emergentagent.com"

async def detailed_test():
    """Run detailed tests and examine response data"""
    
    print("🔍 DETAILED RESPONSE ANALYSIS")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Player Search - Detailed Analysis
        print("1️⃣ PLAYER SEARCH TEST")
        async with session.get(f"{BACKEND_URL}/api/player/%23U8YQR92L") as response:
            player_data = await response.json()
            print(f"   Status: {response.status}")
            print(f"   Player Name: {player_data.get('player', {}).get('name', 'N/A')}")
            print(f"   Clan Name: {player_data.get('clan', {}).get('name', 'N/A')}")
            print(f"   Clan Tag: {player_data.get('clan', {}).get('tag', 'N/A')}")
            print(f"   Town Hall Level: {player_data.get('player', {}).get('townHallLevel', 'N/A')}")
            print(f"   Trophies: {player_data.get('player', {}).get('trophies', 'N/A')}")
        
        print()
        
        # Test 2: Clan Stats - Data Availability
        print("2️⃣ CLAN STATS TEST")
        async with session.get(f"{BACKEND_URL}/api/data/clan/%239PC99CP8/stats") as response:
            stats_data = await response.json()
            print(f"   Status: {response.status}")
            data_avail = stats_data.get('data_availability', {})
            print(f"   Player Snapshots: {data_avail.get('player_snapshots', 0)}")
            print(f"   Clan Snapshots: {data_avail.get('clan_snapshots', 0)}")
            print(f"   Wars: {data_avail.get('wars', 0)}")
            print(f"   War Attacks: {data_avail.get('war_attacks', 0)}")
            print(f"   Capital Raids: {data_avail.get('capital_raids', 0)}")
            print(f"   Days of Data: {data_avail.get('days_of_data', 0)}")
            
            ml_ready = stats_data.get('ml_readiness', {})
            print(f"   ML Ready - Leadership: {ml_ready.get('leadership_analysis', False)}")
            print(f"   ML Ready - Donations: {ml_ready.get('donation_analysis', False)}")
            print(f"   ML Ready - Capital: {ml_ready.get('capital_analysis', False)}")
        
        print()
        
        # Test 3: Leadership Analysis
        print("3️⃣ LEADERSHIP ANALYSIS TEST")
        async with session.post(
            f"{BACKEND_URL}/api/ml/leadership/analyze",
            json={"clan_tag": "#9PC99CP8"}
        ) as response:
            leadership_data = await response.json()
            print(f"   Status: {response.status}")
            print(f"   Leadership Entropy: {leadership_data.get('leadership_entropy', 'N/A')}")
            
            top_leaders = leadership_data.get('top_leaders', [])
            print(f"   Top Leaders Count: {len(top_leaders)}")
            if top_leaders:
                print(f"   Top Leader: {top_leaders[0].get('name', 'N/A')} (Score: {top_leaders[0].get('influence_score', 'N/A')})")
        
        print()
        
        # Test 4: Donation Analysis
        print("4️⃣ DONATION ANALYSIS TEST")
        async with session.post(
            f"{BACKEND_URL}/api/ml/donations/analyze",
            json={"clan_tag": "#9PC99CP8"}
        ) as response:
            donation_data = await response.json()
            print(f"   Status: {response.status}")
            
            network_stats = donation_data.get('network_stats', {})
            print(f"   Total Nodes: {network_stats.get('total_nodes', 'N/A')}")
            print(f"   Total Edges: {network_stats.get('total_edges', 'N/A')}")
            print(f"   Network Density: {network_stats.get('network_density', 'N/A')}")
            
            top_contributors = donation_data.get('top_contributors', [])
            print(f"   Top Contributors Count: {len(top_contributors)}")
            if top_contributors:
                print(f"   Top Contributor: {top_contributors[0].get('name', 'N/A')} (Score: {top_contributors[0].get('centrality_score', 'N/A')})")
        
        print()
        
        # Test 5: Capital Analysis
        print("5️⃣ CAPITAL ANALYSIS TEST")
        async with session.post(
            f"{BACKEND_URL}/api/ml/capital/analyze",
            json={"clan_tag": "#9PC99CP8"}
        ) as response:
            capital_data = await response.json()
            print(f"   Status: {response.status}")
            
            contrib_analysis = capital_data.get('contribution_analysis', {})
            print(f"   Total Raids Analyzed: {contrib_analysis.get('total_raids', 'N/A')}")
            print(f"   Average Contribution: {contrib_analysis.get('avg_contribution_per_raid', 'N/A')}")
            
            player_profiles = contrib_analysis.get('player_profiles', [])
            print(f"   Player Profiles Count: {len(player_profiles)}")
            if player_profiles:
                print(f"   Top Contributor: {player_profiles[0].get('name', 'N/A')} (Avg: {player_profiles[0].get('avg_contribution', 'N/A')})")

if __name__ == "__main__":
    asyncio.run(detailed_test())