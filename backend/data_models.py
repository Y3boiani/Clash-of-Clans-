"""
Data Models for MongoDB Storage

Defines Pydantic models for all CoC data types.
These models serve dual purpose:
1. Data validation and type safety
2. Documentation for reverse engineering the data structures
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


class PlayerSnapshot(BaseModel):
    """
    Time-series snapshot of player data.
    
    Collected periodically to build longitudinal dataset for ML models.
    Key for analyzing trophy trajectories, donation patterns, activity trends.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    player_tag: str
    snapshot_time: datetime = Field(default_factory=datetime.utcnow)
    
    # Identity
    name: str
    town_hall_level: int
    
    # Trophies (for momentum/volatility modeling)
    trophies: int
    best_trophies: int
    
    # War stats
    war_stars: int
    attack_wins: int
    defense_wins: int
    
    # Donations (for network analysis)
    donations: int
    donations_received: int
    
    # Clan context
    clan_tag: Optional[str] = None
    clan_name: Optional[str] = None
    clan_role: Optional[str] = None  # member, admin, coLeader, leader
    
    # League
    league_name: Optional[str] = None
    
    # Additional fields for context
    experience_level: int = 0
    

class ClanSnapshot(BaseModel):
    """
    Time-series snapshot of clan data.
    
    Tracks clan evolution over time for organizational analysis.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clan_tag: str
    snapshot_time: datetime = Field(default_factory=datetime.utcnow)
    
    # Identity
    name: str
    clan_level: int
    
    # Membership
    member_count: int
    member_tags: List[str] = []  # For tracking membership changes
    
    # War stats
    war_wins: int
    war_ties: int = 0
    war_losses: int = 0
    war_win_streak: int = 0
    is_war_log_public: bool
    
    # War league
    war_league: Optional[str] = None
    
    # Capital
    clan_capital_points: int = 0
    clan_capital_league: Optional[str] = None
    
    # Activity indicators
    required_trophies: int
    war_frequency: str  # always, often, sometimes, rarely, never
    
    # Location
    location_name: Optional[str] = None
    

class WarRecord(BaseModel):
    """
    Individual war record from war log.
    
    Critical for performance pressure modeling and coordination analysis.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clan_tag: str
    
    # War metadata
    result: str  # win, lose, tie
    end_time: str  # ISO format timestamp
    team_size: int
    
    # Our clan's performance
    clan_stars: int
    clan_destruction_percentage: float
    clan_attacks: int = 0
    
    # Opponent performance  
    opponent_tag: Optional[str] = None
    opponent_name: Optional[str] = None
    opponent_stars: int
    opponent_destruction_percentage: float
    
    # For tracking wins/losses context
    is_cwl: bool = False
    

class WarAttack(BaseModel):
    """
    Individual attack within a war.
    
    Granular data for pressure modeling and clutch factor analysis.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    war_id: str  # Link to parent war
    clan_tag: str
    
    # Attacker info
    attacker_tag: str
    attacker_name: str
    attacker_th_level: int = 0
    
    # Defender info
    defender_tag: str
    defender_name: str
    defender_th_level: int = 0
    
    # Attack outcome
    stars: int
    destruction_percentage: float
    attack_order: int  # Position in war (1-N)
    
    # Timing context (requires current war API)
    attack_time: Optional[datetime] = None
    
    # War state context (computed)
    war_score_before_attack: Optional[int] = None  # Our score before this attack
    opponent_score_before_attack: Optional[int] = None
    is_cleanup_attack: bool = False  # Attack after war essentially decided
    

class CWLRound(BaseModel):
    """
    CWL war data.
    
    For strategic coherence and coordination analysis.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clan_tag: str
    season: str  # YYYY-MM format
    round_number: int
    
    war_tag: str
    result: str
    
    clan_stars: int
    clan_destruction: float
    clan_attacks_used: int
    
    opponent_tag: str
    opponent_name: str
    opponent_stars: int
    opponent_destruction: float
    
    # League context
    league_name: Optional[str] = None
    

class CapitalRaidSeason(BaseModel):
    """
    Clan capital raid weekend data.
    
    For collective action problem modeling and free-rider detection.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clan_tag: str
    
    # Season info
    start_time: str
    end_time: str
    state: str  # ongoing, ended
    
    # Aggregate outcomes
    total_loot: int
    raids_completed: int
    total_attacks: int
    enemy_districts_destroyed: int
    
    # Defensive
    defensive_reward: int
    
    # Member contributions (critical for free-rider analysis)
    member_contributions: List[Dict[str, Any]] = []  # {tag, name, capital_resources_looted, attacks}
    

class MLModelResult(BaseModel):
    """
    Cached ML model output.
    
    Stores computed ML results to avoid recomputation.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    model_name: str  # e.g., 'leadership_entropy', 'pressure_function'
    entity_type: str  # 'player', 'clan', 'war'
    entity_id: str  # player_tag, clan_tag, or war_id
    
    computed_at: datetime = Field(default_factory=datetime.utcnow)
    valid_until: datetime  # TTL for cache invalidation
    
    # Model outputs (flexible dict for different model types)
    results: Dict[str, Any]
    
    # Metadata for debugging
    data_points_used: int  # How many historical records were used
    confidence_score: Optional[float] = None
