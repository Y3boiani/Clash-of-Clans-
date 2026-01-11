# 🔑 Clash of Clans API Setup Guide

## Current Status

**Issue:** Your CoC API key is restricted to a different IP address than where this system is running.

- **Your API Key IP Restriction:** `36.255.16.54`
- **This System's IP Address:** `35.225.230.28`

**Result:** API calls are blocked with "403 Forbidden" error.

---

## ✅ How to Fix (5 minutes)

### Step 1: Access Developer Portal

1. Go to: https://developer.clashofclans.com/
2. Click **"Sign In"** (top right)
3. Login with your **Supercell ID** (same one used for Clash of Clans)

### Step 2: Find Your API Key

1. After logging in, you'll see **"My Account"** dashboard
2. Scroll down to **"My Keys"** section
3. You should see your existing key listed

### Step 3: Update IP Address

**Option A: Edit Existing Key (Recommended)**
1. Click on your existing key
2. Click **"Edit"** or **"Update IP"**
3. Add this IP address: `35.225.230.28`
4. Click **"Update"**
5. Copy the key (it might regenerate)

**Option B: Create New Key**
1. Click **"Create New Key"**
2. Name: `CoC ML Research Platform`
3. Description: `Machine learning analysis platform`
4. Allowed IP Addresses: `35.225.230.28`
5. Click **"Create Key"**
6. **Copy the generated key immediately** (you can't see it again)

### Step 4: Update the System

**Method 1: Quick Test (Temporary)**
```bash
# SSH into your system and test:
curl -X POST http://localhost:8001/api/data/add-clan \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#YOUR_CLAN_TAG"}'
```

**Method 2: Update Environment Variable (Permanent)**

1. Update `/app/backend/.env`:
```bash
COC_API_KEY="YOUR_NEW_API_KEY_HERE"
```

2. Restart the backend:
```bash
sudo supervisorctl restart backend
```

---

## 🎮 Finding Your Player/Clan Tag

### Player Tag:
1. Open Clash of Clans on your device
2. Tap your **profile picture** (top left)
3. Your player tag is below your name (e.g., `#ABC123XYZ`)
4. Tap to copy it

### Clan Tag:
1. Open your **Clan** page in-game
2. Tap the **info button** (i icon)
3. Your clan tag is shown (e.g., `#2PP`)
4. Tap to copy it

---

## 🧪 Testing the API

### Test 1: Check API Status
```bash
# From your terminal:
curl http://localhost:8001/api/
```

**Expected Output:**
```json
{
  "message": "Clash of Clans ML Research Platform",
  "version": "1.0.0",
  "modules": {...}
}
```

### Test 2: Search for a Well-Known Clan
```bash
curl -X POST http://localhost:8001/api/data/add-clan \
  -H "Content-Type: application/json" \
  -d '{"clan_tag": "#2PP"}'
```

**If Working:**
```json
{
  "message": "Clan #2PP added to tracking",
  "clan_name": "Nova Esports",
  "status": "collecting_data"
}
```

**If Not Working:**
```json
{
  "detail": "Clan #2PP not found in CoC API"
}
```
→ This means IP address still not updated

### Test 3: Use Your Player Name (Arceus)

Once the API key is updated, use the frontend:

1. Go to: http://localhost:3000
2. Scroll to **"Test with Your Account"** section
3. Enter your player tag (from steps above)
4. Click **"Search"**

If successful, you'll see:
- ✅ Your clan information
- Member list
- War stats
- Donation data

---

## 🔧 Troubleshooting

### Problem: "403 Forbidden" Error
**Solution:** 
- IP address not added to API key
- Double-check you added `35.225.230.28` exactly
- Wait 1-2 minutes after updating (DNS propagation)

### Problem: "404 Not Found" Error
**Solution:**
- Player/Clan tag is incorrect
- Make sure to include the `#` symbol
- Tag is case-sensitive

### Problem: API Key Expired
**Solution:**
- Create a new key at developer.clashofclans.com
- Keys can expire or be revoked

### Problem: Rate Limiting
**Solution:**
- CoC API has rate limits (Silver tier: ~10 requests/second)
- Our system includes automatic rate limiting and retries
- If you hit limits, wait a few minutes

---

## 📊 What Data Gets Collected

Once your API key is working, the system automatically collects every 6 hours:

**Player Data:**
- Trophies (for volatility analysis)
- Donations given/received (for network analysis)
- War stars
- Town Hall level
- Activity timestamps

**Clan Data:**
- Member list (for leadership analysis)
- War wins/losses
- War log (for coordination analysis)
- Clan capital raids (for investment analysis)

**War Data:**
- Individual attacks (for pressure analysis)
- Attack outcomes (stars, destruction)
- Attack timing
- War results

**All data is stored in MongoDB and used to train the ML models!**

---

## 🎓 Next Steps After API Setup

1. ✅ **Verify API Working:** Test with your player tag
2. ✅ **Add Your Clan:** System starts collecting data automatically
3. ✅ **Wait 24 Hours:** Best results come after 1-3 days of data collection
4. ✅ **Explore ML Models:** See analysis of YOUR clan's patterns
5. ✅ **Learn by Experimenting:** Modify code, see real results

---

## 🆘 Need Help?

**API Key Issues:**
- Email: support@supercell.com
- Developer Forum: https://forum.supercell.com/forumdisplay.php/4-Developer-Forum

**System Issues:**
- Check logs: `tail -f /var/log/supervisor/backend.err.log`
- Restart services: `sudo supervisorctl restart all`

**Learning Resources:**
- Read: `/app/README.md`
- Source code: `/app/backend/ml_module_*.py`
- API docs: http://localhost:8001/docs

---

## 📝 Quick Reference

| Item | Value |
|------|-------|
| **System IP** | `35.225.230.28` |
| **CoC Dev Portal** | https://developer.clashofclans.com/ |
| **Frontend URL** | http://localhost:3000 |
| **Backend API** | http://localhost:8001/docs |
| **Your Player Name** | Arceus |
| **Your Player Tag** | (You need to provide this) |

---

## ✨ What You'll See After Setup

Once your API key is working:

**🎯 Real-Time Analysis:**
- Your clan's leadership structure (who's really in charge?)
- Player reliability under pressure (who chokes in important wars?)
- Donation network (who are the true benefactors?)
- War coordination quality (how well do you work together?)

**📈 Predictions:**
- Trophy trajectory forecasts for players
- Clan stability risk assessment
- Free-rider detection in capital raids
- Matchmaking fairness audit for your war results

**🧠 ML Insights:**
- See exactly how each model works
- Understand the math behind predictions
- Learn production ML patterns
- Experiment with real data

---

## 🚀 Ready to Begin?

1. Update your API key now: https://developer.clashofclans.com/
2. Add IP: `35.225.230.28`
3. Provide your player tag below so I can test it for you!

**Just reply with your player tag and I'll verify everything is working! 🎮**
