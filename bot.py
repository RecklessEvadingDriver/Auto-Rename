import os
import sys
import time
import signal
import asyncio
import pyromod.listen
from datetime import datetime, timedelta
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import pyrogram.utils
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.logging_config import logger

pyrogram.utils.MIN_CHANNEL_ID = -1002964099736
PORT = Config.PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="rexbots",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        self.start_time = time.time()
        self.is_shutting_down = False

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME
        
        # Start web server if webhook enabled
        if Config.WEBHOOK:
            try:
                app = web.AppRunner(await web_server())
                await app.setup()
                await web.TCPSite(app, "0.0.0.0", PORT).start()
                logger.info(f"Web server started on port {PORT}")
            except Exception as e:
                logger.error(f"Failed to start web server: {e}")
        
        logger.info(f"✨ {me.first_name} is now running!")
        logger.info(f"📊 Bot Username: @{me.username}")
        logger.info(f"🆔 Bot ID: {me.id}")
        
        # Send startup notification
        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(timedelta(seconds=uptime_seconds))
        
        for chat_id in [Config.LOG_CHANNEL, Config.SUPPORT_CHAT]:
            if chat_id == 0:  # Skip if not configured
                continue
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC,
                    caption=(
                        "**I ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ !**\n\n"
                        f"ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​: `{uptime_string}`"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/cantarellabots")]]
                    )
                )
            except Exception as e:
                logger.error(f"Failed to send startup message to {chat_id}: {e}")
    
    async def stop(self, *args):
        """Graceful shutdown handler"""
        if self.is_shutting_down:
            return
        
        self.is_shutting_down = True
        logger.info("🛑 Shutting down gracefully...")
        
        # Send shutdown notification
        for chat_id in [Config.LOG_CHANNEL, Config.SUPPORT_CHAT]:
            if chat_id == 0:
                continue
            try:
                uptime = str(timedelta(seconds=int(time.time() - self.start_time)))
                await self.send_message(
                    chat_id=chat_id,
                    text=f"**Bot is shutting down**\n\nUptime: `{uptime}`"
                )
            except Exception as e:
                logger.error(f"Failed to send shutdown message: {e}")
        
        await super().stop()
        logger.info("✅ Bot stopped successfully")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, initiating shutdown...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Validate configuration before starting
        Config.validate()
        
        # Create and run bot
        bot = Bot()
        logger.info("Starting Auto-Rename Bot...")
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Bot has been stopped")
