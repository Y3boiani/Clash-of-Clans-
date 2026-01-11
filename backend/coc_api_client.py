"""
Clash of Clans API Client

Production-grade async client for CoC API with:
- Rate limiting (respects API throttling)
- Automatic retries with exponential backoff
- Connection pooling
- Error handling
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)


class CoCAPIClient:
    """
    Async client for Clash of Clans API.
    
    Rate Limiting Strategy:
    - Silver tier: ~10 requests/second
    - Implements token bucket algorithm
    - Automatic backoff on 429 errors
    """
    
    BASE_URL = "https://api.clashofclans.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_tokens = 10  # Token bucket for rate limiting
        self.max_tokens = 10
        self.token_refill_rate = 0.1  # Refill 1 token per 0.1 seconds (10/sec)
        self.last_refill = time.time()
        self._lock = asyncio.Lock()
        
    async def _ensure_session(self):
        """Lazy initialization of aiohttp session with connection pooling."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Accept": "application/json"
                }
            )
    
    async def _refill_tokens(self):
        """Refill rate limit tokens using token bucket algorithm."""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed / self.token_refill_rate
        self.rate_limit_tokens = min(self.max_tokens, self.rate_limit_tokens + tokens_to_add)
        self.last_refill = now
    
    async def _wait_for_token(self):
        """Wait until a rate limit token is available."""
        async with self._lock:
            await self._refill_tokens()
            while self.rate_limit_tokens < 1:
                await asyncio.sleep(0.1)
                await self._refill_tokens()
            self.rate_limit_tokens -= 1
    
    async def _request(self, endpoint: str, max_retries: int = 3) -> Optional[Dict[Any, Any]]:
        """
        Make an API request with retry logic.
        
        Args:
            endpoint: API endpoint (e.g., '/clans/%23ABC123')
            max_retries: Maximum number of retry attempts
            
        Returns:
            JSON response as dict, or None on failure
        """
        await self._ensure_session()
        url = f"{self.BASE_URL}{endpoint}"
        
        for attempt in range(max_retries):
            try:
                await self._wait_for_token()
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        logger.warning(f"Resource not found: {endpoint}")
                        return None
                    elif response.status == 429:
                        # Rate limited - exponential backoff
                        wait_time = (2 ** attempt) * 1
                        logger.warning(f"Rate limited, waiting {wait_time}s")
                        await asyncio.sleep(wait_time)
                    elif response.status == 403:
                        logger.error(f"Forbidden - check API key permissions")
                        return None
                    else:
                        logger.error(f"API error {response.status}: {await response.text()}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Request error: {e}")
                await asyncio.sleep(2 ** attempt)
        
        return None
    
    async def get_clan(self, clan_tag: str) -> Optional[Dict[Any, Any]]:
        """
        Get current clan information.
        
        Args:
            clan_tag: Clan tag (e.g., '#2PP')
            
        Returns:
            Clan data including members, war stats, etc.
        """
        # URL encode the # symbol
        encoded_tag = clan_tag.replace('#', '%23')
        return await self._request(f"/clans/{encoded_tag}")
    
    async def get_player(self, player_tag: str) -> Optional[Dict[Any, Any]]:
        """
        Get current player information.
        
        Args:
            player_tag: Player tag (e.g., '#ABC123')
            
        Returns:
            Player data including trophies, donations, war stats, etc.
        """
        encoded_tag = player_tag.replace('#', '%23')
        return await self._request(f"/players/{encoded_tag}")
    
    async def get_clan_war_log(self, clan_tag: str) -> Optional[List[Dict[Any, Any]]]:
        """
        Get clan war log (requires public war log).
        
        Returns:
            List of war results with timestamps, outcomes, star counts
        """
        encoded_tag = clan_tag.replace('#', '%23')
        result = await self._request(f"/clans/{encoded_tag}/warlog")
        return result.get('items', []) if result else None
    
    async def get_current_war(self, clan_tag: str) -> Optional[Dict[Any, Any]]:
        """
        Get current war information (if in war).
        
        Returns:
            Detailed war data including attacks, stars, destruction percentages
        """
        encoded_tag = clan_tag.replace('#', '%23')
        return await self._request(f"/clans/{encoded_tag}/currentwar")
    
    async def get_clan_war_league_group(self, clan_tag: str) -> Optional[Dict[Any, Any]]:
        """
        Get CWL group information (during CWL season).
        
        Returns:
            CWL round data, clans in group, war tags
        """
        encoded_tag = clan_tag.replace('#', '%23')
        return await self._request(f"/clans/{encoded_tag}/currentwar/leaguegroup")
    
    async def get_cwl_war(self, war_tag: str) -> Optional[Dict[Any, Any]]:
        """
        Get specific CWL war details.
        
        Args:
            war_tag: War tag from CWL group
        """
        encoded_tag = war_tag.replace('#', '%23')
        return await self._request(f"/clanwarleagues/wars/{encoded_tag}")
    
    async def get_clan_capital_raid_seasons(self, clan_tag: str, limit: int = 10) -> Optional[List[Dict[Any, Any]]]:
        """
        Get clan capital raid weekend history.
        
        Returns:
            Capital raid data including contributions, raid medals, attacks
        """
        encoded_tag = clan_tag.replace('#', '%23')
        result = await self._request(f"/clans/{encoded_tag}/capitalraidseasons?limit={limit}")
        return result.get('items', []) if result else None
    
    async def search_clans(self, name: str = None, war_frequency: str = None, 
                          location_id: int = None, min_members: int = None,
                          limit: int = 10) -> Optional[List[Dict[Any, Any]]]:
        """
        Search for clans by various criteria.
        
        Useful for building datasets across multiple clans.
        """
        params = []
        if name:
            params.append(f"name={name}")
        if war_frequency:
            params.append(f"warFrequency={war_frequency}")
        if location_id:
            params.append(f"locationId={location_id}")
        if min_members:
            params.append(f"minMembers={min_members}")
        params.append(f"limit={limit}")
        
        query = "&".join(params)
        result = await self._request(f"/clans?{query}")
        return result.get('items', []) if result else None
    
    async def close(self):
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
