#!/usr/bin/env python3
"""
Telegram Silver Price Monitor Bot
Monitors silver spot prices and sends alerts/updates via Telegram
"""

import requests
import json
import time
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')  # Get from @BotFather on Telegram
PRICE_API_URL = "https://api.metals.live/v1/spot/silver"  # Alternative: metals-api.com

class SilverPriceMonitor:
    def __init__(self):
        self.alert_thresholds = {}  # user_id: {'high': price, 'low': price}
        self.monitoring_users = set()
        
    def get_silver_price(self):
        """Fetch current silver spot price with multiple fallback APIs"""
        
        # Try Method 1: metals.live (free, no key)
        try:
            response = requests.get(
                "https://api.metals.live/v1/spot/silver",
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'price': round(data[0]['price'], 2),
                'currency': 'USD',
                'unit': 'troy ounce',
                'timestamp': data[0]['timestamp']
            }
        except Exception as e:
            logger.warning(f"metals.live failed: {e}")
        
        # Try Method 2: metals-api.com (requires free API key but more reliable)
        # Sign up at https://metals-api.com for free tier (100 requests/month)
        metals_api_key = os.getenv('METALS_API_KEY')
        if metals_api_key:
            try:
                response = requests.get(
                    f"https://metals-api.com/api/latest?access_key={metals_api_key}&base=USD&symbols=XAG",
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('success'):
                    # metals-api returns price per gram, convert to troy ounce (31.1035 grams)
                    price_per_gram = 1 / data['rates']['XAG']
                    price_per_oz = price_per_gram * 31.1035
                    
                    return {
                        'price': round(price_per_oz, 2),
                        'currency': 'USD',
                        'unit': 'troy ounce',
                        'timestamp': data['timestamp']
                    }
            except Exception as e:
                logger.warning(f"metals-api.com failed: {e}")
        
        # Try Method 3: goldapi.io (requires free API key)
        goldapi_key = os.getenv('GOLDAPI_KEY')
        if goldapi_key:
            try:
                response = requests.get(
                    "https://www.goldapi.io/api/XAG/USD",
                    headers={'x-access-token': goldapi_key},
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    'price': round(data['price'], 2),
                    'currency': 'USD',
                    'unit': 'troy ounce',
                    'timestamp': int(time.time())
                }
            except Exception as e:
                logger.warning(f"goldapi.io failed: {e}")
        
        logger.error("All price APIs failed")
        return None

monitor = SilverPriceMonitor()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    welcome_msg = (
        "🪙 *Silver Price Monitor Bot*\n\n"
        "Available commands:\n"
        "/price - Get current silver spot price\n"
        "/alert <high> <low> - Set price alerts (e.g., /alert 32 28)\n"
        "/monitor - Start periodic price updates (every 30 min)\n"
        "/stop - Stop periodic updates\n"
        "/status - Check your alert settings\n"
        "/help - Show this message"
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current silver price"""
    price_data = monitor.get_silver_price()
    
    if price_data:
        msg = (
            f"💰 *Silver Spot Price*\n\n"
            f"Price: ${price_data['price']} per {price_data['unit']}\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("⚠️ Unable to fetch price data. Please try again later.")

async def set_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set price alert thresholds"""
    user_id = update.effective_user.id
    
    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage: /alert <high_price> <low_price>\n"
            "Example: /alert 32 28"
        )
        return
    
    try:
        high_price = float(context.args[0])
        low_price = float(context.args[1])
        
        if high_price <= low_price:
            await update.message.reply_text("⚠️ High price must be greater than low price!")
            return
        
        monitor.alert_thresholds[user_id] = {
            'high': high_price,
            'low': low_price
        }
        
        await update.message.reply_text(
            f"✅ Alerts set!\n"
            f"High: ${high_price}\n"
            f"Low: ${low_price}\n\n"
            f"Use /monitor to start checking prices."
        )
    except ValueError:
        await update.message.reply_text("⚠️ Please provide valid numbers!")

async def start_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start periodic price monitoring"""
    user_id = update.effective_user.id
    monitor.monitoring_users.add(user_id)
    
    await update.message.reply_text(
        "✅ Monitoring started! You'll receive updates every 30 minutes.\n"
        "Use /stop to stop monitoring."
    )

async def stop_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop periodic price monitoring"""
    user_id = update.effective_user.id
    
    if user_id in monitor.monitoring_users:
        monitor.monitoring_users.remove(user_id)
        await update.message.reply_text("🛑 Monitoring stopped.")
    else:
        await update.message.reply_text("You're not currently monitoring prices.")

async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check alert status"""
    user_id = update.effective_user.id
    
    status_msg = "📊 *Your Settings*\n\n"
    
    if user_id in monitor.alert_thresholds:
        thresholds = monitor.alert_thresholds[user_id]
        status_msg += f"Alert High: ${thresholds['high']}\n"
        status_msg += f"Alert Low: ${thresholds['low']}\n"
    else:
        status_msg += "No alerts set\n"
    
    if user_id in monitor.monitoring_users:
        status_msg += "\nMonitoring: ✅ Active"
    else:
        status_msg += "\nMonitoring: ⭕ Inactive"
    
    await update.message.reply_text(status_msg, parse_mode='Markdown')

async def check_alerts(context: ContextTypes.DEFAULT_TYPE):
    """Background task to check prices and send alerts"""
    price_data = monitor.get_silver_price()
    
    if not price_data:
        return
    
    current_price = price_data['price']
    
    for user_id in list(monitor.monitoring_users):
        try:
            # Send regular update
            msg = f"📊 Silver: ${current_price}/oz"
            await context.bot.send_message(chat_id=user_id, text=msg)
            
            # Check alerts
            if user_id in monitor.alert_thresholds:
                thresholds = monitor.alert_thresholds[user_id]
                
                if current_price >= thresholds['high']:
                    alert_msg = f"🚨 *ALERT!* Silver price hit ${current_price} (above ${thresholds['high']})"
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=alert_msg,
                        parse_mode='Markdown'
                    )
                elif current_price <= thresholds['low']:
                    alert_msg = f"🚨 *ALERT!* Silver price hit ${current_price} (below ${thresholds['low']})"
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=alert_msg,
                        parse_mode='Markdown'
                    )
        except Exception as e:
            logger.error(f"Error sending message to {user_id}: {e}")

def main():
    """Start the bot"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ Please set your Telegram bot token in the script!")
        print("Get a token from @BotFather on Telegram")
        return
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("price", get_price))
    application.add_handler(CommandHandler("alert", set_alert))
    application.add_handler(CommandHandler("monitor", start_monitoring))
    application.add_handler(CommandHandler("stop", stop_monitoring))
    application.add_handler(CommandHandler("status", check_status))
    
    # Add job to check prices every 30 minutes (1800 seconds)
    job_queue = application.job_queue
    job_queue.run_repeating(check_alerts, interval=1800, first=10)
    
    # Start bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()