"""
Demo Data Generator

Creates realistic synthetic CoC data for demonstrating the ML platform.

This allows the platform to work without needing real API access,
perfect for learning and testing.
"""

import asyncio
from datetime import datetime, timedelta
import random
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


async def generate_demo_clan(clan_tag: str = "#DEMO001"):
    """Generate a complete demo clan with 30 days of data."""
    
    print(f"Generating demo data for clan {clan_tag}...")
    
    # Generate 30 members
    member_tags = [f"#MEMBER{i:03d}" for i in range(1, 31)]
    member_names = [f"Player{i}" for i in range(1, 31)]
    
    # Generate 30 days of historical data
    start_date = datetime.utcnow() - timedelta(days=30)
    
    # Clear existing data
    await db.players_history.delete_many({"clan_tag": clan_tag})
    await db.clans_history.delete_many({"clan_tag": clan_tag})
    await db.wars_history.delete_many({"clan_tag": clan_tag})
    await db.war_attacks.delete_many({"clan_tag": clan_tag})
    await db.capital_raids_history.delete_many({"clan_tag": clan_tag})
    
    print("Generating player snapshots...")
    # Generate player snapshots (4 per day for 30 days)
    player_snapshots = []
    for day in range(30):
        for snapshot_num in range(4):  # 4 snapshots per day
            snapshot_time = start_date + timedelta(days=day, hours=snapshot_num * 6)
            
            for i, (tag, name) in enumerate(zip(member_tags, member_names)):
                # Each player has their own "trajectory"
                base_trophies = 3000 + (i * 100)  # Different skill levels
                volatility = 50 + (i % 10) * 10  # Different volatilities
                
                # Random walk for trophies
                trophy_change = np.random.normal(0, volatility / 4)
                trophies = max(1000, int(base_trophies + trophy_change * day))
                
                # Donations with some players being benefactors
                if i < 5:  # Top 5 are benefactors
                    donations = int(50 + day * 20 + np.random.normal(0, 10))
                    donations_received = int(10 + day * 5 + np.random.normal(0, 5))
                elif i >= 25:  # Bottom 5 are parasites
                    donations = int(5 + day * 2 + np.random.normal(0, 2))
                    donations_received = int(30 + day * 15 + np.random.normal(0, 5))
                else:  # Middle are balanced
                    donations = int(25 + day * 10 + np.random.normal(0, 5))
                    donations_received = int(25 + day * 10 + np.random.normal(0, 5))
                
                snapshot = {
                    "id": f"{tag}_{snapshot_time.isoformat()}",
                    "player_tag": tag,
                    "snapshot_time": snapshot_time,
                    "name": name,
                    "town_hall_level": 13 + (i % 3),
                    "trophies": trophies,
                    "best_trophies": trophies + random.randint(0, 500),
                    "war_stars": 100 + day * 3 + i * 10,
                    "attack_wins": 500 + day * 5 + i * 20,
                    "defense_wins": 300 + day * 3 + i * 10,
                    "donations": max(0, donations),
                    "donations_received": max(0, donations_received),
                    "clan_tag": clan_tag,
                    "clan_name": "Demo Clan",
                    "clan_role": "leader" if i == 0 else "coLeader" if i < 3 else "admin" if i < 8 else "member",
                    "league_name": "Champion League" if i < 10 else "Master League" if i < 20 else "Crystal League",
                    "experience_level": 100 + i * 10
                }
                player_snapshots.append(snapshot)
    
    await db.players_history.insert_many(player_snapshots)
    print(f"Generated {len(player_snapshots)} player snapshots")
    
    print("Generating clan snapshots...")
    # Generate clan snapshots
    clan_snapshots = []
    for day in range(30):
        for snapshot_num in range(4):
            snapshot_time = start_date + timedelta(days=day, hours=snapshot_num * 6)
            
            snapshot = {
                "id": f"{clan_tag}_{snapshot_time.isoformat()}",
                "clan_tag": clan_tag,
                "snapshot_time": snapshot_time,
                "name": "Demo Clan",
                "clan_level": 10,
                "member_count": 30,
                "member_tags": member_tags,
                "war_wins": 100 + day * 2,
                "war_ties": 5,
                "war_losses": 50 + day,
                "war_win_streak": max(0, 10 - day % 15),
                "is_war_log_public": True,
                "war_league": "Champion League III",
                "clan_capital_points": 10000 + day * 500,
                "clan_capital_league": "Capital Peak",
                "required_trophies": 2500,
                "war_frequency": "always",
                "location_name": "United States"
            }
            clan_snapshots.append(snapshot)
    
    await db.clans_history.insert_many(clan_snapshots)
    print(f"Generated {len(clan_snapshots)} clan snapshots")
    
    print("Generating war records...")
    # Generate wars (roughly 2 per week for 8 weeks)
    wars = []
    for week in range(8):
        for war_num in range(2):
            day = week * 7 + war_num * 3
            end_time = (start_date + timedelta(days=day)).isoformat()
            
            # Vary outcomes
            result = random.choices(['win', 'lose', 'tie'], weights=[0.55, 0.40, 0.05])[0]
            our_stars = random.randint(35, 45)
            their_stars = our_stars - 5 if result == 'win' else our_stars + 5 if result == 'lose' else our_stars
            
            war = {
                "id": f"{clan_tag}_war_{week}_{war_num}",
                "clan_tag": clan_tag,
                "result": result,
                "end_time": end_time,
                "team_size": 15,
                "clan_stars": our_stars,
                "clan_destruction_percentage": 85.0 + random.uniform(-10, 10),
                "clan_attacks": 28 + random.randint(-2, 2),
                "opponent_tag": f"#OPP{week}{war_num:02d}",
                "opponent_name": f"Opponent {week}-{war_num}",
                "opponent_stars": their_stars,
                "opponent_destruction_percentage": 85.0 + random.uniform(-10, 10),
                "is_cwl": week % 4 == 0  # Every 4th week is CWL
            }
            wars.append(war)
    
    await db.wars_history.insert_many(wars)
    print(f"Generated {len(wars)} war records")
    
    print("Generating war attacks...")
    # Generate war attacks for each war
    all_attacks = []
    for war in wars:
        war_id = war['id']
        # Each war has ~28 attacks (not all players attack twice)
        attack_order = 1
        
        for member_idx in range(15):  # 15 players in war
            tag = member_tags[member_idx]
            name = member_names[member_idx]
            
            # Most players get 2 attacks
            num_attacks = 2 if random.random() > 0.1 else 1
            
            for attack_num in range(num_attacks):
                # Performance varies by player and pressure
                base_stars = 2.5 if member_idx < 10 else 2.0  # Better players do better
                
                # Add randomness
                stars = min(3, max(0, int(base_stars + random.normalvariate(0, 0.7))))
                
                # Some players choke under pressure (late game, losing)
                if attack_order > 20 and war['result'] == 'lose':
                    if member_idx > 20:  # Some players are pressure-sensitive
                        stars = max(0, stars - 1)
                
                attack = {
                    "id": f"{war_id}_attack_{attack_order}",
                    "war_id": war_id,
                    "clan_tag": clan_tag,
                    "attacker_tag": tag,
                    "attacker_name": name,
                    "attacker_th_level": 13 + (member_idx % 3),
                    "defender_tag": f"#DEF{member_idx}",
                    "defender_name": f"Defender {member_idx}",
                    "defender_th_level": 13 + (member_idx % 3),
                    "stars": stars,
                    "destruction_percentage": min(100.0, stars * 33.0 + random.uniform(0, 10)),
                    "attack_order": attack_order,
                    "attack_time": datetime.fromisoformat(war['end_time']) - timedelta(hours=24-attack_order),
                    "war_score_before_attack": attack_order * 2,
                    "opponent_score_before_attack": attack_order * 2,
                    "is_cleanup_attack": attack_order > 25
                }
                all_attacks.append(attack)
                attack_order += 1
    
    await db.war_attacks.insert_many(all_attacks)
    print(f"Generated {len(all_attacks)} war attacks")
    
    print("Generating capital raids...")
    # Generate capital raid weekends (roughly 1 per week for 8 weeks)
    raids = []
    for week in range(8):
        start_time = (start_date + timedelta(days=week * 7, hours=12)).isoformat()
        end_time = (start_date + timedelta(days=week * 7 + 3, hours=12)).isoformat()
        
        # Generate member contributions
        contributions = []
        for i, (tag, name) in enumerate(zip(member_tags, member_names)):
            # Some contribute more than others
            if i < 5:  # Top contributors
                looted = random.randint(2000, 4000)
                attacks = random.randint(5, 6)
            elif i >= 25:  # Free riders
                looted = random.randint(0, 500)
                attacks = random.randint(0, 2)
            else:  # Average
                looted = random.randint(800, 2000)
                attacks = random.randint(3, 5)
            
            contributions.append({
                "tag": tag,
                "name": name,
                "capital_resources_looted": looted,
                "attacks": attacks
            })
        
        raid = {
            "id": f"{clan_tag}_raid_{week}",
            "clan_tag": clan_tag,
            "start_time": start_time,
            "end_time": end_time,
            "state": "ended",
            "total_loot": sum(c['capital_resources_looted'] for c in contributions),
            "raids_completed": 5 + random.randint(-1, 1),
            "total_attacks": sum(c['attacks'] for c in contributions),
            "enemy_districts_destroyed": 25 + random.randint(-5, 5),
            "defensive_reward": 500 + random.randint(-100, 100),
            "member_contributions": contributions
        }
        raids.append(raid)
    
    await db.capital_raids_history.insert_many(raids)
    print(f"Generated {len(raids)} capital raid records")
    
    # Add to tracked clans
    await db.config.update_one(
        {"key": "tracked_clans"},
        {"$addToSet": {"clans": clan_tag}},
        upsert=True
    )
    
    print(f"\n✅ Demo data generation complete!")
    print(f"\nClan Tag: {clan_tag}")
    print(f"Members: 30")
    print(f"Days of data: 30")
    print(f"Total records: {len(player_snapshots) + len(clan_snapshots) + len(wars) + len(all_attacks) + len(raids)}")
    print(f"\nYou can now test all ML modules with this clan!")


if __name__ == "__main__":
    asyncio.run(generate_demo_clan("#DEMO001"))
