"""Error handler for the bot"""

from telegram.ext import ContextTypes
from loguru import logger
import traceback

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot"""
    logger.error(f"Update {update} caused error {context.error}")
    
    # Log full traceback
    logger.error(traceback.format_exc())
    
    # Notify user if possible
    if hasattr(update, 'message') and update.message:
        try:
            await update.message.reply_text(
                "❌ An error occurred while processing your request.\n"
                "Please try again or contact support."
            )
        except Exception as e:
            logger.error(f"Could not send error message: {e}")
