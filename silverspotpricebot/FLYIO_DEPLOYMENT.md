# Deploy Silver Price Bot to Fly.io

Complete guide to deploying your Telegram bot on Fly.io for free.

## Prerequisites

1. A Telegram bot token from @BotFather
2. A Fly.io account (free tier available)
3. flyctl CLI installed on your computer

## Step 1: Install Fly.io CLI

### macOS
```bash
brew install flyctl
```

### Linux
```bash
curl -L https://fly.io/install.sh | sh
```

### Windows
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

## Step 2: Sign Up and Login

```bash
# Sign up for Fly.io (free tier)
flyctl auth signup

# Or login if you already have an account
flyctl auth login
```

## Step 3: Prepare Your Files

Make sure you have these files in your directory:
- `silver_price_bot.py` (the bot script)
- `requirements.txt` (Python dependencies)
- `Dockerfile` (container configuration)
- `fly.toml` (Fly.io configuration)
- `.dockerignore` (files to exclude from build)

## Step 4: Create Your Fly.io App

```bash
# Navigate to your bot directory
cd /path/to/your/bot

# Launch the app (this creates it on Fly.io)
flyctl launch
```

When prompted:
- **App name**: Accept the suggested name or choose your own (e.g., `silver-price-bot-yourname`)
- **Region**: Choose the closest region to you (e.g., `iad` for US East)
- **Set up PostgreSQL**: NO
- **Set up Redis**: NO
- **Deploy now**: NO (we need to add secrets first)

## Step 5: Set Your Bot Token as a Secret

**IMPORTANT:** Never commit your bot token to code. Use Fly.io secrets instead.

```bash
# Set your Telegram bot token securely
flyctl secrets set TELEGRAM_BOT_TOKEN="your_actual_bot_token_here"
```

Replace `your_actual_bot_token_here` with your actual token from @BotFather.

## Step 6: Deploy Your Bot

```bash
# Deploy the application
flyctl deploy
```

This will:
1. Build your Docker image
2. Push it to Fly.io
3. Deploy and start your bot

## Step 7: Verify Deployment

```bash
# Check if your app is running
flyctl status

# View live logs
flyctl logs

# Check machine status
flyctl machines list
```

## Step 8: Test Your Bot

1. Open Telegram
2. Search for your bot (the username you created with @BotFather)
3. Send `/start` to begin using it

## Useful Commands

### Monitor your bot
```bash
# View real-time logs
flyctl logs

# Check app status
flyctl status

# SSH into your machine
flyctl ssh console
```

### Manage your bot
```bash
# Restart the bot
flyctl apps restart

# Scale resources (if needed)
flyctl scale memory 512

# Stop the bot
flyctl apps stop

# Start the bot
flyctl apps start
```

### Update your bot
```bash
# After making changes to your code
flyctl deploy

# Update secrets
flyctl secrets set TELEGRAM_BOT_TOKEN="new_token"
```

## Cost Information

**Fly.io Free Tier includes:**
- Up to 3 shared-cpu-1x VMs with 256MB RAM each
- 160GB outbound data transfer per month
- 3GB persistent storage

**Your bot uses:** 1 VM with 256MB RAM (well within free tier)

## Troubleshooting

### Bot not responding
```bash
# Check logs for errors
flyctl logs

# Verify bot is running
flyctl status
```

### Out of memory
```bash
# Increase memory allocation
flyctl scale memory 512
```

### Connection issues
```bash
# Restart the application
flyctl apps restart
```

### Check environment variables
```bash
# List all secrets
flyctl secrets list
```

## Security Best Practices

1. ✅ **Never** commit your bot token to Git
2. ✅ Use `flyctl secrets` for sensitive data
3. ✅ Keep your `.env` file in `.gitignore`
4. ✅ Regularly update dependencies

## Updating Your Bot

When you make changes to your code:

```bash
# 1. Edit your files locally
# 2. Deploy the changes
flyctl deploy

# 3. Monitor the deployment
flyctl logs
```

## Deleting Your App

If you want to remove your bot from Fly.io:

```bash
flyctl apps destroy silver-price-bot
```

## Alternative: Using fly.toml Configuration

You can also configure everything in `fly.toml` before deployment. The provided `fly.toml` file includes:
- VM resources (256MB RAM, 1 CPU)
- Auto-start/stop settings (disabled for always-on)
- Region settings

## Need Help?

- Fly.io Documentation: https://fly.io/docs/
- Fly.io Community: https://community.fly.io/
- Check logs: `flyctl logs`

## Summary

```bash
# Quick deployment steps
flyctl auth login
flyctl launch
flyctl secrets set TELEGRAM_BOT_TOKEN="your_token"
flyctl deploy
flyctl logs
```

Your bot should now be running 24/7 on Fly.io's free tier! 🎉
