#!/usr/bin/env python3
"""
Backend API Testing for CoC ML Research Platform
Tests the basic health check endpoints after frontend migration.
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import sys

# Backend URL from frontend/.env
BACKEND_URL = "https://zero-hassle-ml.preview.emergentagent.com"

class BackendTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = []
        
    async def test_endpoint(self, method, endpoint, expected_status=200, description=""):
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    status = response.status
                    try:
                        data = await response.json()
                    except:
                        data = await response.text()
                    
                    success = status == expected_status
                    
                    result = {
                        "endpoint": endpoint,
                        "method": method,
                        "url": url,
                        "status_code": status,
                        "expected_status": expected_status,
                        "success": success,
                        "response_data": data,
                        "description": description,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    self.results.append(result)
                    
                    print(f"{'✅' if success else '❌'} {method} {endpoint} - Status: {status} (Expected: {expected_status})")
                    if not success:
                        print(f"   Response: {data}")
                    
                    return result
                    
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": method,
                "url": url,
                "status_code": None,
                "expected_status": expected_status,
                "success": False,
                "error": str(e),
                "description": description,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            print(f"❌ {method} {endpoint} - Error: {str(e)}")
            return result

    async def test_post_endpoint(self, endpoint, payload, expected_status=200, description=""):
        """Test a POST endpoint with JSON payload"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, 
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    status = response.status
                    try:
                        data = await response.json()
                    except:
                        data = await response.text()
                    
                    success = status == expected_status
                    
                    result = {
                        "endpoint": endpoint,
                        "method": "POST",
                        "url": url,
                        "payload": payload,
                        "status_code": status,
                        "expected_status": expected_status,
                        "success": success,
                        "response_data": data,
                        "description": description,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    self.results.append(result)
                    
                    print(f"{'✅' if success else '❌'} POST {endpoint} - Status: {status} (Expected: {expected_status})")
                    if not success:
                        print(f"   Response: {data}")
                    elif isinstance(data, dict):
                        # Print key response fields for successful ML analysis
                        if 'leadership_entropy' in data:
                            print(f"   ✓ Leadership analysis returned entropy data")
                        if 'network_stats' in data:
                            print(f"   ✓ Donation analysis returned network stats")
                        if 'contribution_analysis' in data:
                            print(f"   ✓ Capital analysis returned contribution data")
                    
                    return result
                    
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": "POST",
                "url": url,
                "payload": payload,
                "status_code": None,
                "expected_status": expected_status,
                "success": False,
                "error": str(e),
                "description": description,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            print(f"❌ POST {endpoint} - Error: {str(e)}")
            return result

    async def run_health_checks(self):
        """Run the basic health check tests as requested"""
        print(f"🚀 Testing CoC ML Research Platform Backend")
        print(f"📍 Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test 1: Root API endpoint
        await self.test_endpoint(
            "GET", 
            "/api/", 
            200, 
            "Root API endpoint - should return platform info and available modules"
        )
        
        # Test 2: System IP endpoint  
        await self.test_endpoint(
            "GET", 
            "/api/system/ip", 
            200, 
            "System IP endpoint - should return current system IP address"
        )
        
        # Test 3: Data clans listing
        await self.test_endpoint(
            "GET", 
            "/api/data/clans", 
            200, 
            "Data clans endpoint - should return list of tracked clans"
        )
        
        print("=" * 60)
        return self.results

    async def run_real_data_tests(self):
        """Run tests with real CoC data for clan #9PC99CP8 (Amber Amry)"""
        print(f"🎯 Testing CoC ML Research Platform with REAL DATA")
        print(f"📍 Backend URL: {self.base_url}")
        print(f"🏰 Clan: #9PC99CP8 (Amber Amry)")
        print(f"👤 Player: #U8YQR92L (Anirban)")
        print("=" * 60)
        
        # Test 1: Player Search - Anirban from Amber Amry
        await self.test_endpoint(
            "GET", 
            "/api/player/%23U8YQR92L", 
            200, 
            "Player search for Anirban (#U8YQR92L) - should return player from Amber Amry clan"
        )
        
        # Test 2: Clan Stats - Amber Amry data availability
        await self.test_endpoint(
            "GET", 
            "/api/data/clan/%239PC99CP8/stats", 
            200, 
            "Clan stats for Amber Amry (#9PC99CP8) - should show collected data (player_snapshots > 0, capital_raids > 0)"
        )
        
        # Test 3: Leadership Analysis
        await self.test_post_endpoint(
            "/api/ml/leadership/analyze",
            {"clan_tag": "#9PC99CP8"},
            200,
            "Leadership analysis for Amber Amry - should return leadership_entropy and top_leaders"
        )
        
        # Test 4: Donation Analysis  
        await self.test_post_endpoint(
            "/api/ml/donations/analyze",
            {"clan_tag": "#9PC99CP8"},
            200,
            "Donation analysis for Amber Amry - should return network_stats and top_contributors"
        )
        
        # Test 5: Capital Analysis
        await self.test_post_endpoint(
            "/api/ml/capital/analyze", 
            {"clan_tag": "#9PC99CP8"},
            200,
            "Capital analysis for Amber Amry - should return contribution_analysis with player profiles"
        )
        
        print("=" * 60)
        return self.results

    def print_summary(self):
        """Print test summary"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"\n📊 TEST SUMMARY")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n🔍 FAILED TESTS:")
            for result in self.results:
                if not result['success']:
                    print(f"  - {result['method']} {result['endpoint']}")
                    if 'error' in result:
                        print(f"    Error: {result['error']}")
                    else:
                        print(f"    Status: {result['status_code']} (Expected: {result['expected_status']})")

async def main():
    """Main test runner"""
    tester = BackendTester(BACKEND_URL)
    
    try:
        # Run the real data tests as requested in the review
        results = await tester.run_real_data_tests()
        tester.print_summary()
        
        # Return results for further processing
        return results
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return []

if __name__ == "__main__":
    results = asyncio.run(main())