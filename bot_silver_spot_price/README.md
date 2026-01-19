# Silver Price Monitor Telegram Bot

A Telegram bot that monitors silver spot prices and sends alerts when prices cross your thresholds.

## Features

- 💰 Check current silver spot price on demand
- 🚨 Set custom price alerts (high/low thresholds)
- 📊 Receive periodic price updates every 5 minutes
- 🔔 Get notifications when price crosses your alert levels

## Setup Instructions

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to BotFather
3. Follow the prompts to choose a name and username for your bot
4. BotFather will give you a **bot token** - save this!

### 2. Install Dependencies

```bash
pip install python-telegram-bot requests --break-system-packages
```

Or using a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install python-telegram-bot requests
```

### 3. Configure the Bot

1. Open `silver_price_bot.py`
2. Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token from BotFather:
   ```python
   TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
   ```

### 4. Run the Bot

```bash
python3 silver_price_bot.py
```

Keep the script running to monitor prices continuously.

## Usage

Once the bot is running, open Telegram and start a chat with your bot:

### Commands

- `/start` or `/help` - Show available commands
- `/price` - Get current silver spot price
- `/alert <high> <low>` - Set price alerts
  - Example: `/alert 32 28` (alert when price > $32 or < $28)
- `/monitor` - Start receiving price updates every 5 minutes
- `/stop` - Stop periodic updates
- `/status` - Check your current alert settings

### Example Usage

```
You: /price
Bot: 💰 Silver Spot Price
     Price: $29.45 per troy ounce
     Time: 2026-01-19 14:30:00

You: /alert 31 28
Bot: ✅ Alerts set!
     High: $31
     Low: $28

You: /monitor
Bot: ✅ Monitoring started! You'll receive updates every 5 minutes.

[5 minutes later]
Bot: 📊 Silver: $29.50/oz

[When price crosses threshold]
Bot: 🚨 ALERT! Silver price hit $31.20 (above $31)
```

## Running as a Background Service

### Using screen (Linux/Mac)

```bash
screen -S silver-bot
python3 silver_price_bot.py
# Press Ctrl+A then D to detach
# Reattach with: screen -r silver-bot
```

### Using systemd (Linux)

Create `/etc/systemd/system/silver-bot.service`:

```ini
[Unit]
Description=Silver Price Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 /path/to/bot/silver_price_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable silver-bot
sudo systemctl start silver-bot
sudo systemctl status silver-bot
```

## Price Data Source

The bot uses the metals.live API which provides free, real-time precious metals prices without requiring an API key.

## Customization

You can modify the following in the script:

- **Update interval**: Change `interval=300` (in seconds) in the `job_queue.run_repeating()` call
- **Price API**: Add your own API key for alternative sources (code included for goldapi.io)
- **Currency**: Modify to track silver in different currencies

## Troubleshooting

**Bot doesn't respond:**
- Make sure the script is running
- Check your bot token is correct
- Verify you're messaging the correct bot

**Price fetch errors:**
- Check your internet connection
- The metals.live API might be temporarily down
- Consider adding an alternative API key

**Multiple users:**
- The bot supports multiple users simultaneously
- Each user can set their own alerts and monitoring preferences

## Security Notes

- Keep your bot token private
- Don't commit the token to version control
- Consider using environment variables for the token:
  ```python
  import os
  TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
  ```

## License

Free to use and modify for your personal or commercial projects.
