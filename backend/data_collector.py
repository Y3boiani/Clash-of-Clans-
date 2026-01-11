"""
Data Collection Workers

Background tasks that periodically collect data from CoC API and store in MongoDB.

Production Strategy:
- Run as background asyncio tasks
- Collect data every 6 hours for longitudinal analysis
- Handle errors gracefully with retry logic
- Track collection metadata for monitoring
"""

import asyncio
from datetime import datetime, timedelta
import logging
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from data_models import (
    PlayerSnapshot, ClanSnapshot, WarRecord, 
    WarAttack, CWLRound, CapitalRaidSeason
)
from coc_api_client import CoCAPIClient
import os

logger = logging.getLogger(__name__)


class DataCollector:
    """
    Orchestrates data collection from CoC API into MongoDB.
    
    Educational Note:
    Time-series ML requires consistent data snapshots.
    This collector runs on schedule to build historical datasets.
    """
    
    def __init__(self, db: AsyncIOMotorClient, api_key: str):
        self.db = db
        self.api_key = api_key
        self.coc_client = CoCAPIClient(api_key)
        self.tracked_clans: List[str] = []  # Will be populated from DB or config
        
    async def initialize(self):
        """Initialize collector and load tracked entities."""
        await self.coc_client._ensure_session()
        
        # Load tracked clans from config collection
        config = await self.db.config.find_one({"key": "tracked_clans"})
        if config:
            self.tracked_clans = config.get("clans", [])
        
        logger.info(f"Data collector initialized. Tracking {len(self.tracked_clans)} clans.")
    
    async def add_clan_to_track(self, clan_tag: str):
        """
        Add a clan to tracking list.
        
        This will trigger data collection for the clan and all its members.
        """
        if clan_tag not in self.tracked_clans:
            self.tracked_clans.append(clan_tag)
            
            # Persist to DB
            await self.db.config.update_one(
                {"key": "tracked_clans"},
                {"$set": {"clans": self.tracked_clans, "updated_at": datetime.utcnow()}},
                upsert=True
            )
            logger.info(f"Added clan {clan_tag} to tracking")
    
    async def collect_player_snapshot(self, player_tag: str) -> Optional[PlayerSnapshot]:
        """
        Collect and store current player state.
        
        Returns:
            PlayerSnapshot object if successful
        """
        try:
            data = await self.coc_client.get_player(player_tag)
            if not data:
                return None
            
            snapshot = PlayerSnapshot(
                player_tag=data['tag'],
                name=data['name'],
                town_hall_level=data['townHallLevel'],
                trophies=data['trophies'],
                best_trophies=data['bestTrophies'],
                war_stars=data.get('warStars', 0),
                attack_wins=data.get('attackWins', 0),
                defense_wins=data.get('defenseWins', 0),
                donations=data.get('donations', 0),
                donations_received=data.get('donationsReceived', 0),
                clan_tag=data.get('clan', {}).get('tag'),
                clan_name=data.get('clan', {}).get('name'),
                clan_role=data.get('role'),
                league_name=data.get('league', {}).get('name'),
                experience_level=data.get('expLevel', 0)
            )
            
            # Store in MongoDB
            await self.db.players_history.insert_one(snapshot.model_dump())
            logger.debug(f"Collected snapshot for player {player_tag}")
            return snapshot
            
        except Exception as e:
            logger.error(f"Error collecting player {player_tag}: {e}")
            return None
    
    async def collect_clan_snapshot(self, clan_tag: str) -> Optional[ClanSnapshot]:
        """
        Collect and store current clan state.
        
        Also triggers player snapshots for all members.
        """
        try:
            data = await self.coc_client.get_clan(clan_tag)
            if not data:
                return None
            
            member_tags = [m['tag'] for m in data.get('memberList', [])]
            
            snapshot = ClanSnapshot(
                clan_tag=data['tag'],
                name=data['name'],
                clan_level=data['clanLevel'],
                member_count=data['members'],
                member_tags=member_tags,
                war_wins=data.get('warWins', 0),
                war_ties=data.get('warTies', 0),
                war_losses=data.get('warLosses', 0),
                war_win_streak=data.get('warWinStreak', 0),
                is_war_log_public=data.get('isWarLogPublic', False),
                war_league=data.get('warLeague', {}).get('name'),
                clan_capital_points=data.get('clanCapitalPoints', 0),
                clan_capital_league=data.get('capitalLeague', {}).get('name'),
                required_trophies=data.get('requiredTrophies', 0),
                war_frequency=data.get('warFrequency', 'unknown'),
                location_name=data.get('location', {}).get('name')
            )
            
            # Store clan snapshot
            await self.db.clans_history.insert_one(snapshot.model_dump())
            
            # Collect snapshots for all members (in parallel)
            tasks = [self.collect_player_snapshot(tag) for tag in member_tags[:50]]  # Limit to avoid rate limit
            await asyncio.gather(*tasks, return_exceptions=True)
            
            logger.info(f"Collected snapshot for clan {clan_tag} with {len(member_tags)} members")
            return snapshot
            
        except Exception as e:
            logger.error(f"Error collecting clan {clan_tag}: {e}")
            return None
    
    async def collect_war_log(self, clan_tag: str):
        """
        Collect war history for a clan.
        
        Stores individual war records for outcome analysis.
        """
        try:
            wars = await self.coc_client.get_clan_war_log(clan_tag)
            if not wars:
                return
            
            for war in wars:
                # Check if already stored
                existing = await self.db.wars_history.find_one({
                    "clan_tag": clan_tag,
                    "end_time": war.get('endTime')
                })
                
                if existing:
                    continue
                
                record = WarRecord(
                    clan_tag=clan_tag,
                    result=war.get('result', 'unknown'),
                    end_time=war.get('endTime', ''),
                    team_size=war.get('teamSize', 0),
                    clan_stars=war.get('clan', {}).get('stars', 0),
                    clan_destruction_percentage=war.get('clan', {}).get('destructionPercentage', 0),
                    clan_attacks=war.get('clan', {}).get('attacks', 0),
                    opponent_tag=war.get('opponent', {}).get('tag'),
                    opponent_name=war.get('opponent', {}).get('name'),
                    opponent_stars=war.get('opponent', {}).get('stars', 0),
                    opponent_destruction_percentage=war.get('opponent', {}).get('destructionPercentage', 0)
                )
                
                await self.db.wars_history.insert_one(record.model_dump())
            
            logger.info(f"Collected {len(wars)} war records for {clan_tag}")
            
        except Exception as e:
            logger.error(f"Error collecting war log for {clan_tag}: {e}")
    
    async def collect_current_war(self, clan_tag: str):
        """
        Collect detailed current war data including individual attacks.
        
        This provides granular data for pressure modeling.
        """
        try:
            war = await self.coc_client.get_current_war(clan_tag)
            if not war or war.get('state') == 'notInWar':
                return
            
            war_id = f"{clan_tag}_{war.get('preparationStartTime', '')}"[:50]
            
            # Process attacks from our clan
            if 'clan' in war and 'members' in war['clan']:
                for member in war['clan']['members']:
                    if 'attacks' not in member:
                        continue
                    
                    for attack_num, attack in enumerate(member['attacks']):
                        attack_record = WarAttack(
                            war_id=war_id,
                            clan_tag=clan_tag,
                            attacker_tag=member['tag'],
                            attacker_name=member['name'],
                            attacker_th_level=member.get('townhallLevel', 0),
                            defender_tag=attack['defenderTag'],
                            defender_name='',  # Not always available
                            defender_th_level=0,
                            stars=attack['stars'],
                            destruction_percentage=attack['destructionPercentage'],
                            attack_order=attack.get('order', 0)
                        )
                        
                        # Store attack (avoid duplicates)
                        await self.db.war_attacks.update_one(
                            {
                                "war_id": war_id,
                                "attacker_tag": attack_record.attacker_tag,
                                "attack_order": attack_record.attack_order
                            },
                            {"$set": attack_record.model_dump()},
                            upsert=True
                        )
            
            logger.info(f"Collected current war data for {clan_tag}")
            
        except Exception as e:
            logger.error(f"Error collecting current war for {clan_tag}: {e}")
    
    async def collect_capital_raids(self, clan_tag: str):
        """
        Collect clan capital raid weekend history.
        
        Critical for free-rider detection and collective action analysis.
        """
        try:
            raids = await self.coc_client.get_clan_capital_raid_seasons(clan_tag, limit=10)
            if not raids:
                return
            
            for raid in raids:
                # Check if already stored
                existing = await self.db.capital_raids_history.find_one({
                    "clan_tag": clan_tag,
                    "start_time": raid.get('startTime')
                })
                
                if existing:
                    continue
                
                # Extract member contributions
                members = raid.get('members', [])
                member_data = [
                    {
                        "tag": m.get('tag'),
                        "name": m.get('name'),
                        "capital_resources_looted": m.get('capitalResourcesLooted', 0),
                        "attacks": m.get('attacks', 0)
                    }
                    for m in members
                ]
                
                raid_record = CapitalRaidSeason(
                    clan_tag=clan_tag,
                    start_time=raid.get('startTime', ''),
                    end_time=raid.get('endTime', ''),
                    state=raid.get('state', 'ended'),
                    total_loot=raid.get('totalLoot', 0),
                    raids_completed=raid.get('raidsCompleted', 0),
                    total_attacks=raid.get('totalAttacks', 0),
                    enemy_districts_destroyed=raid.get('enemyDistrictsDestroyed', 0),
                    defensive_reward=raid.get('defensiveReward', 0),
                    member_contributions=member_data
                )
                
                await self.db.capital_raids_history.insert_one(raid_record.model_dump())
            
            logger.info(f"Collected {len(raids)} capital raid records for {clan_tag}")
            
        except Exception as e:
            logger.error(f"Error collecting capital raids for {clan_tag}: {e}")
    
    async def run_collection_cycle(self):
        """
        Run a full collection cycle for all tracked clans.
        
        This is the main method called by the scheduler.
        """
        logger.info(f"Starting collection cycle for {len(self.tracked_clans)} clans")
        
        for clan_tag in self.tracked_clans:
            try:
                # Collect all data types
                await self.collect_clan_snapshot(clan_tag)
                await self.collect_war_log(clan_tag)
                await self.collect_current_war(clan_tag)
                await self.collect_capital_raids(clan_tag)
                
                # Small delay between clans to respect rate limits
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error in collection cycle for {clan_tag}: {e}")
        
        logger.info("Collection cycle completed")
    
    async def start_scheduler(self, interval_hours: int = 6):
        """
        Start the background scheduler.
        
        Runs collection cycles every N hours.
        """
        await self.initialize()
        
        while True:
            try:
                await self.run_collection_cycle()
            except Exception as e:
                logger.error(f"Error in scheduler: {e}")
            
            # Wait for next cycle
            await asyncio.sleep(interval_hours * 3600)
