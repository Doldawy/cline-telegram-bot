"""Security utilities for the bot"""

from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import settings
from loguru import logger

def check_user_authorized(func):
    """Decorator to check if user is authorized"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        if not settings.is_user_allowed(user.id):
            logger.warning(f"🚫 Unauthorized access attempt from user {user.id}")
            await update.message.reply_text(
                "🔒 Sorry, you are not authorized to use this bot.\n\n"
                "If you think this is a mistake, please contact the bot owner."
            )
            return
        
        return await func(update, context)
    
    return wrapper

def sanitize_message(text: str) -> str:
    """Sanitize message content"""
    if not settings.enable_message_sanitization:
        return text
    
    # Remove sensitive patterns
    import re
    
    # Remove potential sensitive data
    text = re.sub(r'(?:token|password|key|secret)\s*=\s*[^\s]+', '[REDACTED]', text, flags=re.IGNORECASE)
    
    return text

def is_rate_limited(user_id: int) -> bool:
    """Check if user is rate limited"""
    if not settings.enable_rate_limiting:
        return False
    
    # TODO: Implement rate limiting with Redis
    return False
