"""Message handler for forwarding to Cline"""

from telegram import Update
from telegram.ext import ContextTypes
from config import settings
from utils.security import check_user_authorized
from utils.logger import log_message
from loguru import logger

@check_user_authorized
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and forward to Cline"""
    user = update.effective_user
    message_text = update.message.text
    
    logger.info(f"📨 Message from {user.id} (@{user.username}): {message_text[:50]}...")
    
    # Show typing indicator
    await update.message.chat.send_action('typing')
    
    try:
        # Log message
        log_message(user.id, message_text, 'user')
        
        # TODO: Forward to Cline API
        # response = await forward_to_cline(message_text)
        
        # For now, send a placeholder response
        response = (
            "🤖 *Cline AI Response*\n\n"
            "Thank you for your message! This is a test response.\n\n"
            "*Note:* Cline API integration coming soon! ⏳"
        )
        
        await update.message.reply_text(
            response,
            parse_mode='Markdown'
        )
        
        log_message(user.id, response, 'bot')
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            f"❌ An error occurred: {str(e)}\n\n"
            "Please try again or contact support."
        )
