#!/usr/bin/env python3
"""
Cline Telegram Bot
Main bot entry point
"""

import asyncio
import argparse
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from loguru import logger
import sys

from config import settings
from handlers.commands import (
    start_command,
    help_command,
    status_command,
    settings_command,
    cancel_command
)
from handlers.messages import handle_message
from handlers.errors import error_handler
from utils.security import check_user_authorized

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.bot_log_level
)

class ClineTelegramBot:
    """Main Cline Telegram Bot class"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the bot
        
        Args:
            token: Telegram bot token (overrides config if provided)
        """
        self.token = token or settings.telegram_bot_token
        
        if not self.token:
            raise ValueError("Telegram bot token not provided")
        
        self.app: Optional[Application] = None
        logger.info("🤖 Cline Telegram Bot initialized")
    
    def setup_handlers(self) -> None:
        """Setup all command and message handlers"""
        if not self.app:
            raise RuntimeError("Application not initialized")
        
        # Command handlers
        self.app.add_handler(CommandHandler('start', start_command))
        self.app.add_handler(CommandHandler('help', help_command))
        self.app.add_handler(CommandHandler('status', status_command))
        self.app.add_handler(CommandHandler('settings', settings_command))
        self.app.add_handler(CommandHandler('cancel', cancel_command))
        
        # Message handler
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        ))
        
        # Error handler
        self.app.add_error_handler(error_handler)
        
        logger.info("✅ All handlers registered")
    
    async def start(self) -> None:
        """Start the bot"""
        try:
            # Validate configuration
            settings.validate_config()
            
            # Create application
            self.app = Application.builder().token(self.token).build()
            
            # Setup handlers
            self.setup_handlers()
            
            logger.info("🚀 Starting bot polling...")
            logger.info(f"🔐 Allowed users: {settings.allowed_users}")
            
            # Start the bot
            async with self.app:
                await self.app.start()
                logger.success("✅ Bot started successfully")
                await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
                logger.info("📡 Polling started")
                
        except ValueError as e:
            logger.error(f"❌ Configuration error: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            sys.exit(1)
    
    async def stop(self) -> None:
        """Stop the bot"""
        if self.app:
            await self.app.stop()
            logger.info("🛑 Bot stopped")

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='🤖 Cline Telegram Bot - Control Cline AI from Telegram'
    )
    parser.add_argument(
        '-k', '--token',
        help='Telegram bot token (overrides TELEGRAM_BOT_TOKEN env var)'
    )
    parser.add_argument(
        '--allowed-user-id',
        help='Comma-separated list of allowed user IDs (overrides config)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Override settings if arguments provided
    if args.token:
        settings.telegram_bot_token = args.token
    if args.allowed_user_id:
        settings.allowed_user_ids = args.allowed_user_id
    if args.log_level:
        settings.bot_log_level = args.log_level
    
    # Create and start bot
    bot = ClineTelegramBot(token=args.token)
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("⏹️  Bot interrupted by user")
        await bot.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
