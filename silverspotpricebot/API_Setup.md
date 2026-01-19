# API_Setup.md

# API Setup Guide for Silver Price Bot

The bot now uses multiple API sources with automatic fallbacks for better reliability.

## Current Issue

The free metals.live API is experiencing SSL issues on Fly.io. To fix this, you should add one of these free backup APIs.

## Recommended: Add metals-api.com (Free Tier)

**Why:** Most reliable, 100 free requests/month is plenty for your bot

### Setup Steps:

1. **Sign up for free API key:**
   - Go to https://metals-api.com
   - Click "Get Free API Key"
   - Sign up (no credit card required)
   - Copy your API key

2. **Add to Fly.io:**
   ```bash
   flyctl secrets set METALS_API_KEY="your_metals_api_key_here"
   ```

3. **Deploy:**
   ```bash
   fly deploy
   ```

## Alternative: Add goldapi.io (Free Tier)

**Why:** Also reliable, 100 requests/month free

### Setup Steps:

1. **Sign up for free API key:**
   - Go to https://www.goldapi.io
   - Click "Get Free API Key"
   - Sign up and verify email
   - Copy your API key

2. **Add to Fly.io:**
   ```bash
   flyctl secrets set GOLDAPI_KEY="your_goldapi_key_here"
   ```

3. **Deploy:**
   ```bash
   fly deploy
   ```

## How the Fallback System Works

The bot tries APIs in this order:
1. **metals.live** (free, no key) - tries first
2. **metals-api.com** (if METALS_API_KEY is set) - fallback
3. **goldapi.io** (if GOLDAPI_KEY is set) - last resort

You only need ONE backup API key. I recommend metals-api.com.

## Quick Fix Command

```bash
# 1. Get your API key from metals-api.com
# 2. Set it in Fly.io
flyctl secrets set METALS_API_KEY="your_key_here"

# 3. Redeploy
fly deploy

# 4. Test
fly logs
```

## Verify It's Working

```bash
# Check logs
fly logs

# You should see successful price fetches, not SSL errors
```

Then test on Telegram with `/price` command.

## Monthly Usage Estimate

With monitoring every 5 minutes:
- 12 checks per hour × 24 hours = 288 checks per day
- 288 × 30 days = 8,640 requests per month

**Problem:** This exceeds the 100 free requests! 

## Solution: Adjust Update Interval

Edit `silver_price_bot.py` line 224:
```python
# Change from every 5 minutes (300 seconds)
job_queue.run_repeating(check_alerts, interval=300, first=10)

# To every 30 minutes (1800 seconds) = 1,440 requests/month
job_queue.run_repeating(check_alerts, interval=1800, first=10)

# Or every 1 hour (3600 seconds) = 720 requests/month
job_queue.run_repeating(check_alerts, interval=3600, first=10)
```

Then redeploy:
```bash
fly deploy
```

## Best Configuration for Free Tier

**Recommendation:** 
- Use metals-api.com as backup
- Set interval to 30 minutes (1800 seconds)
- This gives you plenty of headroom within free tier

```python
job_queue.run_repeating(check_alerts, interval=1800, first=10)
```

## Summary

```bash
# Quick setup
flyctl secrets set METALS_API_KEY="your_key_from_metals-api.com"
fly deploy
fly logs
```

Your bot will now work reliably! 🎉