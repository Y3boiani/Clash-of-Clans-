"""
Clash of Clans ML Research Platform - Main Server

Production-grade FastAPI server exposing all 7 ML research modules.

API Structure:
- /api/data: Data collection endpoints
- /api/ml/leadership: Leadership entropy analysis
- /api/ml/pressure: Performance pressure modeling
- /api/ml/coordination: War coordination analysis
- /api/ml/volatility: Trophy volatility modeling
- /api/ml/donations: Donation network analysis
- /api/ml/capital: Clan capital investment analysis
- /api/ml/fairness: Matchmaking fairness audit

Educational Note:
This server demonstrates production ML deployment patterns:
- Async request handling
- Caching for expensive computations
- Background task scheduling
- Comprehensive error handling
"""

from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os
import logging
import asyncio
from pathlib import Path

# Import our ML modules
from ml_module_1_leadership import LeadershipEntropyModel
from ml_module_2_pressure import PressureFunctionModel
from ml_module_3_coordination import CoordinationModel
from ml_module_4_volatility import TrophyVolatilityModel
from ml_module_5_donations import DonationNetworkModel
from ml_module_6_capital import CapitalInvestmentModel
from ml_module_7_fairness import MatchmakingFairnessModel

# Import data infrastructure
from coc_api_client import CoCAPIClient
from data_collector import DataCollector

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize ML models
ml_models = {
    'leadership': LeadershipEntropyModel(),
    'pressure': PressureFunctionModel(),
    'coordination': CoordinationModel(),
    'volatility': TrophyVolatilityModel(),
    'donations': DonationNetworkModel(),
    'capital': CapitalInvestmentModel(),
    'fairness': MatchmakingFairnessModel()
}

# Initialize CoC API client
coc_api_key = os.environ.get('COC_API_KEY', '')
coc_client = CoCAPIClient(coc_api_key) if coc_api_key else None
data_collector = DataCollector(db, coc_api_key) if coc_api_key else None

# Create the main app
app = FastAPI(title="Clash of Clans ML Research Platform")

# Create API router
api_router = APIRouter(prefix="/api")


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AddClanRequest(BaseModel):
    clan_tag: str

class MLAnalysisRequest(BaseModel):
    clan_tag: Optional[str] = None
    player_tag: Optional[str] = None
    war_id: Optional[str] = None
    force_refresh: bool = False


# ============================================================================
# DATA COLLECTION ENDPOINTS
# ============================================================================

@api_router.get("/player/{player_tag}")
async def lookup_player(player_tag: str, background_tasks: BackgroundTasks):
    """
    Look up a player by tag and return their info + clan info.
    This is the main entry point for users to search any player.
    """
    if not coc_client:
        raise HTTPException(status_code=500, detail="CoC API client not initialized. Check COC_API_KEY.")
    
    # Format tag properly
    if not player_tag.startswith('#') and not player_tag.startswith('%23'):
        player_tag = '#' + player_tag
    player_tag = player_tag.replace('%23', '#')
    
    # Fetch player from CoC API
    player_data = await coc_client.get_player(player_tag)
    if not player_data:
        raise HTTPException(status_code=404, detail=f"Player {player_tag} not found in CoC API")
    
    # Extract clan info if player is in a clan
    clan_info = player_data.get('clan', {})
    clan_tag = clan_info.get('tag') if clan_info else None
    
    response = {
        "player": {
            "tag": player_data.get('tag'),
            "name": player_data.get('name'),
            "townHallLevel": player_data.get('townHallLevel'),
            "trophies": player_data.get('trophies'),
            "bestTrophies": player_data.get('bestTrophies'),
            "warStars": player_data.get('warStars'),
            "attackWins": player_data.get('attackWins'),
            "defenseWins": player_data.get('defenseWins'),
            "donations": player_data.get('donations'),
            "donationsReceived": player_data.get('donationsReceived'),
            "role": player_data.get('role'),
            "expLevel": player_data.get('expLevel')
        },
        "clan": None
    }
    
    # If player is in a clan, fetch clan data and start tracking
    if clan_tag and data_collector:
        clan_data = await coc_client.get_clan(clan_tag)
        if clan_data:
            response["clan"] = {
                "tag": clan_data.get('tag'),
                "name": clan_data.get('name'),
                "clanLevel": clan_data.get('clanLevel'),
                "members": clan_data.get('members'),
                "warWins": clan_data.get('warWins'),
                "warWinStreak": clan_data.get('warWinStreak'),
                "description": clan_data.get('description', '')[:100]
            }
            # Auto-track clan in background
            await data_collector.add_clan_to_track(clan_tag)
            background_tasks.add_task(data_collector.collect_clan_snapshot, clan_tag)
    
    return response


@api_router.post("/data/add-clan")
async def add_clan_to_tracking(request: AddClanRequest, background_tasks: BackgroundTasks):
    """
    Add a clan to the tracking system.
    
    This triggers:
    1. Immediate data collection for the clan
    2. Addition to scheduled collection
    
    Educational: Background task pattern for long-running operations.
    """
    if not data_collector:
        raise HTTPException(status_code=500, detail="Data collector not initialized. Check COC_API_KEY.")
    
    clan_tag = request.clan_tag
    
    # Validate clan exists
    clan_data = await coc_client.get_clan(clan_tag)
    if not clan_data:
        raise HTTPException(status_code=404, detail=f"Clan {clan_tag} not found in CoC API")
    
    # Add to tracking
    await data_collector.add_clan_to_track(clan_tag)
    
    # Trigger immediate collection in background
    background_tasks.add_task(data_collector.collect_clan_snapshot, clan_tag)
    
    return {
        "message": f"Clan {clan_tag} added to tracking",
        "clan_name": clan_data.get('name'),
        "status": "collecting_data"
    }

@api_router.get("/data/clans")
async def list_tracked_clans():
    """Get list of all tracked clans."""
    config = await db.config.find_one({"key": "tracked_clans"})
    clans = config.get('clans', []) if config else []
    return {"tracked_clans": clans, "count": len(clans)}

@api_router.get("/data/clan/{clan_tag}/stats")
async def get_clan_data_stats(clan_tag: str):
    """
    Get data collection statistics for a clan.
    
    Shows how much historical data is available for ML models.
    """
    clan_tag = clan_tag.replace('#', '%23')
    
    # Count snapshots
    player_snapshots = await db.players_history.count_documents({"clan_tag": clan_tag})
    clan_snapshots = await db.clans_history.count_documents({"clan_tag": clan_tag})
    wars = await db.wars_history.count_documents({"clan_tag": clan_tag})
    war_attacks = await db.war_attacks.count_documents({"clan_tag": clan_tag})
    capital_raids = await db.capital_raids_history.count_documents({"clan_tag": clan_tag})
    
    # Get date range
    oldest_clan = await db.clans_history.find_one(
        {"clan_tag": clan_tag},
        sort=[("snapshot_time", 1)]
    )
    latest_clan = await db.clans_history.find_one(
        {"clan_tag": clan_tag},
        sort=[("snapshot_time", -1)]
    )
    
    if oldest_clan and latest_clan:
        days_of_data = (latest_clan['snapshot_time'] - oldest_clan['snapshot_time']).days
    else:
        days_of_data = 0
    
    return {
        "clan_tag": clan_tag,
        "data_availability": {
            "player_snapshots": player_snapshots,
            "clan_snapshots": clan_snapshots,
            "wars": wars,
            "war_attacks": war_attacks,
            "capital_raids": capital_raids,
            "days_of_data": days_of_data
        },
        "ml_readiness": {
            "leadership_analysis": clan_snapshots >= 3 and player_snapshots >= 10,
            "pressure_analysis": war_attacks >= 20,
            "coordination_analysis": war_attacks >= 30,
            "volatility_analysis": player_snapshots >= 30,
            "donation_analysis": player_snapshots >= 5,
            "capital_analysis": capital_raids >= 3,
            "fairness_analysis": wars >= 10
        }
    }


# ============================================================================
# ML MODULE 1: LEADERSHIP ENTROPY
# ============================================================================

@api_router.post("/ml/leadership/analyze")
async def analyze_leadership(request: MLAnalysisRequest):
    """
    Analyze clan leadership structure using entropy modeling.
    
    Returns:
    - Leadership influence scores per member
    - Organizational entropy metrics
    - Stability predictions
    
    Educational: Demonstrates latent variable modeling and social network analysis.
    """
    if not request.clan_tag:
        raise HTTPException(status_code=400, detail="clan_tag required")
    
    clan_tag = request.clan_tag
    
    # Check cache unless force refresh
    if not request.force_refresh:
        cached = await db.ml_results.find_one({
            "model_name": "leadership_entropy",
            "entity_id": clan_tag,
            "valid_until": {"$gt": datetime.utcnow()}
        })
        if cached:
            return cached['results']
    
    # Fetch data
    player_snapshots = await db.players_history.find({"clan_tag": clan_tag}).to_list(10000)
    war_attacks = await db.war_attacks.find({"clan_tag": clan_tag}).to_list(5000)
    clan_snapshots = await db.clans_history.find({"clan_tag": clan_tag}).to_list(1000)
    
    if not player_snapshots or not clan_snapshots:
        raise HTTPException(status_code=404, detail="Insufficient data for analysis. Clan may need more collection time.")
    
    # Run ML model
    model = ml_models['leadership']
    results = model.generate_report(player_snapshots, war_attacks, clan_snapshots)
    
    # Cache results for 24 hours
    await db.ml_results.insert_one({
        "model_name": "leadership_entropy",
        "entity_type": "clan",
        "entity_id": clan_tag,
        "computed_at": datetime.utcnow(),
        "valid_until": datetime.utcnow() + timedelta(hours=24),
        "results": results,
        "data_points_used": len(player_snapshots)
    })
    
    return results


# ============================================================================
# ML MODULE 2: PRESSURE FUNCTION
# ============================================================================

@api_router.post("/ml/pressure/analyze-player")
async def analyze_player_pressure(request: MLAnalysisRequest):
    """
    Analyze individual player performance under pressure.
    
    Returns:
    - Baseline performance metrics
    - Pressure sensitivity coefficient
    - Choking probability
    - Reliability score
    - Player archetype
    
    Educational: Demonstrates variance modeling and contextual performance analysis.
    """
    if not request.player_tag:
        raise HTTPException(status_code=400, detail="player_tag required")
    
    player_tag = request.player_tag
    
    # Fetch player's attacks
    attacks = await db.war_attacks.find({"attacker_tag": player_tag}).to_list(1000)
    
    if not attacks:
        raise HTTPException(status_code=404, detail="No attack data found for player")
    
    # Get war contexts
    war_ids = list(set(a['war_id'] for a in attacks))
    war_contexts = []
    for war_id in war_ids:
        # Compute war context from attacks
        war_attacks = [a for a in attacks if a['war_id'] == war_id]
        our_stars = sum(a['stars'] for a in war_attacks)
        context = {
            'war_id': war_id,
            'our_stars': our_stars,
            'their_stars': 0,  # Would need opponent data
            'team_size': 15,  # Default
            'is_cwl': False
        }
        war_contexts.append(context)
    
    # Run ML model
    model = ml_models['pressure']
    results = model.generate_player_report(player_tag, attacks, war_contexts)
    
    return results

@api_router.post("/ml/pressure/analyze-clan")
async def analyze_clan_pressure(request: MLAnalysisRequest):
    """
    Analyze clan-wide pressure performance.
    
    Identifies most reliable players for high-pressure situations.
    """
    if not request.clan_tag:
        raise HTTPException(status_code=400, detail="clan_tag required")
    
    clan_tag = request.clan_tag
    
    # Get all attacks for clan
    attacks = await db.war_attacks.find({"clan_tag": clan_tag}).to_list(10000)
    
    if not attacks:
        raise HTTPException(status_code=404, detail="No attack data found")
    
    # Group by player
    player_attacks = {}
    for attack in attacks:
        tag = attack['attacker_tag']
        if tag not in player_attacks:
            player_attacks[tag] = []
        player_attacks[tag].append(attack)
    
    # War contexts
    war_ids = list(set(a['war_id'] for a in attacks))
    war_contexts = []
    for war_id in war_ids:
        war_attacks = [a for a in attacks if a['war_id'] == war_id]
        context = {
            'war_id': war_id,
            'our_stars': sum(a['stars'] for a in war_attacks),
            'their_stars': 0,
            'team_size': 15,
            'is_cwl': False
        }
        war_contexts.append(context)
    
    # Run ML model
    model = ml_models['pressure']
    results = model.generate_clan_report(player_attacks, war_contexts)
    
    return results


# ============================================================================
# ML MODULE 3: COORDINATION
# ============================================================================

@api_router.post("/ml/coordination/analyze-war")
async def analyze_war_coordination(request: MLAnalysisRequest):
    """
    Analyze coordination patterns for a specific war.
    
    Returns:
    - Attack timing coherence
    - Targeting efficiency
    - Strategic motifs
    - Coordination index
    
    Educational: Demonstrates temporal pattern recognition and emergent behavior.
    """
    if not request.war_id:
        raise HTTPException(status_code=400, detail="war_id required")
    
    war_id = request.war_id
    
    # Get attacks for this war
    attacks = await db.war_attacks.find({"war_id": war_id}).to_list(1000)
    
    if not attacks:
        raise HTTPException(status_code=404, detail="No attacks found for this war")
    
    war_size = 15  # Default, could be derived from attacks
    
    # Run ML model
    model = ml_models['coordination']
    results = model.generate_war_report(war_id, attacks, war_size)
    
    return results

@api_router.post("/ml/coordination/analyze-clan-trend")
async def analyze_clan_coordination_trend(request: MLAnalysisRequest):
    """
    Analyze coordination trends across multiple wars.
    """
    if not request.clan_tag:
        raise HTTPException(status_code=400, detail="clan_tag required")
    
    clan_tag = request.clan_tag
    
    # Get recent wars
    wars = await db.wars_history.find({"clan_tag": clan_tag}).sort("end_time", -1).limit(20).to_list(20)
    
    if len(wars) < 3:
        raise HTTPException(status_code=404, detail="Insufficient war history (need at least 3 wars)")
    
    # Analyze each war
    war_reports = []
    model = ml_models['coordination']
    
    for war in wars:
        war_id = f"{clan_tag}_{war['end_time']}"
        attacks = await db.war_attacks.find({"war_id": war_id}).to_list(1000)
        
        if attacks:
            report = model.generate_war_report(war_id, attacks, war['team_size'])
            war_reports.append(report)
    
    # Generate trend analysis
    trend = model.generate_clan_coordination_trend(war_reports)
    
    return {
        "clan_tag": clan_tag,
        "trend_analysis": trend,
        "recent_wars": war_reports[:5]
    }


# ============================================================================
# ML MODULE 4: TROPHY VOLATILITY
# ============================================================================

@api_router.post("/ml/volatility/analyze")
async def analyze_trophy_volatility(request: MLAnalysisRequest):
    """
    Analyze player trophy dynamics using stochastic process modeling.
    
    Returns:
    - OU process parameters (skill, mean reversion, volatility)
    - Volatility index and stability score
    - Skill vs luck decomposition
    - Momentum/tilt detection
    - 30-day trajectory forecast
    
    Educational: Demonstrates stochastic process modeling and financial mathematics.
    """
    if not request.player_tag:
        raise HTTPException(status_code=400, detail="player_tag required")
    
    player_tag = request.player_tag
    
    # Fetch player snapshots
    snapshots = await db.players_history.find({"player_tag": player_tag}).sort("snapshot_time", 1).to_list(1000)
    
    if len(snapshots) < 10:
        raise HTTPException(status_code=404, detail="Insufficient data (need at least 10 snapshots)")
    
    # Run ML model
    model = ml_models['volatility']
    results = model.generate_player_report(player_tag, snapshots)
    
    return results


# ============================================================================
# ML MODULE 5: DONATION NETWORK
# ============================================================================

@api_router.post("/ml/donations/analyze")
async def analyze_donation_network(request: MLAnalysisRequest):
    """
    Analyze clan donation economy as resource flow network.
    
    Returns:
    - Network graph with centrality scores
    - Economic inequality metrics (Gini coefficient)
    - Parasite detection
    - Retention risk predictions
    - Reciprocity index
    
    Educational: Demonstrates graph analytics and economic network theory.
    """
    if not request.clan_tag:
        raise HTTPException(status_code=400, detail="clan_tag required")
    
    clan_tag = request.clan_tag
    
    # Fetch player snapshots
    player_snapshots = await db.players_history.find({"clan_tag": clan_tag}).to_list(10000)
    
    if not player_snapshots:
        raise HTTPException(status_code=404, detail="No player data found")
    
    # Run ML model
    model = ml_models['donations']
    results = model.generate_clan_report(player_snapshots, clan_tag)
    
    return results


# ============================================================================
# ML MODULE 6: CLAN CAPITAL
# ============================================================================

@api_router.post("/ml/capital/analyze")
async def analyze_capital_investment(request: MLAnalysisRequest):
    """
    Analyze clan capital as collective action problem.
    
    Returns:
    - Contribution pattern analysis
    - Free-rider detection
    - Contribution inequality metrics
    - Hypothesis test: do patterns predict success?
    - Policy recommendations
    
    Educational: Demonstrates game theory and causal inference.
    """
    if not request.clan_tag:
        raise HTTPException(status_code=400, detail="clan_tag required")
    
    clan_tag = request.clan_tag
    
    # Fetch capital raid data
    raids = await db.capital_raids_history.find({"clan_tag": clan_tag}).sort("start_time", -1).to_list(50)
    
    if not raids:
        raise HTTPException(status_code=404, detail="No capital raid data found")
    
    # Run ML model
    model = ml_models['capital']
    results = model.generate_clan_report(raids)
    
    return results


# ============================================================================
# ML MODULE 7: MATCHMAKING FAIRNESS
# ============================================================================

@api_router.post("/ml/fairness/audit")
async def audit_matchmaking_fairness(request: MLAnalysisRequest):
    """
    Audit war matchmaking algorithm for systematic biases.
    
    Returns:
    - Win rates by characteristics
    - Demographic parity tests
    - Matchup difficulty analysis
    - Bias detection and assessment
    - Fairness grade
    
    Educational: Demonstrates algorithmic fairness and bias detection.
    """
    if not request.clan_tag:
        raise HTTPException(status_code=400, detail="clan_tag required")
    
    clan_tag = request.clan_tag
    
    # Fetch war history
    wars = await db.wars_history.find({"clan_tag": clan_tag}).to_list(1000)
    clan_snapshots = await db.clans_history.find({"clan_tag": clan_tag}).to_list(1000)
    
    if len(wars) < 10:
        raise HTTPException(status_code=404, detail="Insufficient war history (need at least 10 wars)")
    
    # Run ML model
    model = ml_models['fairness']
    results = model.generate_fairness_report(wars, clan_snapshots)
    
    return results


# ============================================================================
# COMPREHENSIVE CLAN DASHBOARD
# ============================================================================

@api_router.get("/ml/dashboard/{clan_tag}")
async def get_clan_ml_dashboard(clan_tag: str):
    """
    Get comprehensive ML analysis dashboard for a clan.
    
    Runs all applicable ML models and returns unified view.
    
    Educational: Shows how to compose multiple ML modules into application.
    """
    clan_tag = clan_tag.replace('%23', '#')
    
    # Check data availability first
    stats = await get_clan_data_stats(clan_tag)
    readiness = stats['ml_readiness']
    
    dashboard = {
        "clan_tag": clan_tag,
        "generated_at": datetime.utcnow().isoformat(),
        "data_stats": stats,
        "analyses": {}
    }
    
    # Run each analysis if data is ready
    try:
        if readiness['leadership_analysis']:
            dashboard['analyses']['leadership'] = await analyze_leadership(
                MLAnalysisRequest(clan_tag=clan_tag)
            )
    except Exception as e:
        dashboard['analyses']['leadership'] = {"error": str(e)}
    
    try:
        if readiness['donation_analysis']:
            dashboard['analyses']['donations'] = await analyze_donation_network(
                MLAnalysisRequest(clan_tag=clan_tag)
            )
    except Exception as e:
        dashboard['analyses']['donations'] = {"error": str(e)}
    
    try:
        if readiness['capital_analysis']:
            dashboard['analyses']['capital'] = await analyze_capital_investment(
                MLAnalysisRequest(clan_tag=clan_tag)
            )
    except Exception as e:
        dashboard['analyses']['capital'] = {"error": str(e)}
    
    try:
        if readiness['fairness_analysis']:
            dashboard['analyses']['fairness'] = await audit_matchmaking_fairness(
                MLAnalysisRequest(clan_tag=clan_tag)
            )
    except Exception as e:
        dashboard['analyses']['fairness'] = {"error": str(e)}
    
    return dashboard


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@api_router.get("/")
async def root():
    """
    API root with available endpoints.
    """
    return {
        "message": "Clash of Clans ML Research Platform",
        "version": "1.0.0",
        "modules": {
            "Module 1": "Leadership Entropy & Authority Distribution",
            "Module 2": "War Performance Pressure Function",
            "Module 3": "Strategic Coherence & Coordination",
            "Module 4": "Trophy Momentum & Rank Volatility",
            "Module 5": "Donation Economy & Resource Flow",
            "Module 6": "Clan Capital Collective Action",
            "Module 7": "Matchmaking Fairness Audit"
        },
        "endpoints": {
            "data_collection": "/api/data/*",
            "ml_analyses": "/api/ml/*",
            "dashboard": "/api/ml/dashboard/{clan_tag}"
        }
    }


# ============================================================================
# APP SETUP
# ============================================================================

# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize background data collection."""
    logger.info("Starting CoC ML Research Platform...")
    
    if data_collector:
        # Start data collection scheduler in background
        asyncio.create_task(data_collector.start_scheduler(interval_hours=6))
        logger.info("Data collector scheduler started (6-hour intervals)")
    else:
        logger.warning("Data collector not initialized - COC_API_KEY not set")
    
    logger.info("Server ready!")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Clean shutdown."""
    client.close()
    if coc_client:
        await coc_client.close()
    logger.info("Server shutdown complete")
