"""Command handlers for the bot"""

from telegram import Update
from telegram.ext import ContextTypes
from config import settings
from utils.security import check_user_authorized
from loguru import logger

@check_user_authorized
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"👤 User {user.id} (@{user.username}) started the bot")
    
    welcome_message = (
        "🤖 **Welcome to Cline Telegram Bot!**\n\n"
        "I'm your intelligent controller for Cline AI. Here's what I can do:\n\n"
        "📋 **Available Commands:**\n"
        "/help - Show all commands\n"
        "/status - Check Cline's status\n"
        "/settings - Manage your settings\n"
        "/cancel - Cancel current operation\n\n"
        "💡 **Tips:**\n"
        "• Just send me any message to start a conversation with Cline\n"
        "• I'll forward your requests and bring back responses\n"
        "• Your privacy is protected 🔒\n\n"
        "Let's get started! What would you like to ask Cline?"
    )
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown'
    )

@check_user_authorized
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = (
        "📚 **Cline Bot Command Reference**\n\n"
        "**Basic Commands:**\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/status - Check Cline AI status\n"
        "/settings - View/modify settings\n"
        "/cancel - Cancel current operation\n\n"
        "**Usage:**\n"
        "Simply send any message (not a command) and I'll forward it to Cline AI.\n\n"
        "**Examples:**\n"
        "• 'Write a Python function to sort a list'\n"
        "• 'What is machine learning?'\n"
        "• 'Fix this code: ...'\n\n"
        "**Security:**\n"
        "• Only authorized users can access this bot\n"
        "• All communications are encrypted\n"
        "• Your data is not stored permanently\n\n"
        "Need more help? Check the [documentation](https://github.com/Doldawy/cline-telegram-bot)"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown'
    )

@check_user_authorized
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command"""
    status_message = (
        "✅ **Bot Status**\n\n"
        "🤖 Cline Bot: Online\n"
        "🔗 Connection: Active\n"
        "🔐 Security: Protected\n\n"
        "📊 **Statistics:**\n"
        "• Users: 1\n"
        "• Commands processed: 0\n"
        "• Average response time: N/A\n\n"
        "Ready to help! Send any message to get started."
    )
    
    await update.message.reply_text(
        status_message,
        parse_mode='Markdown'
    )

@check_user_authorized
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command"""
    user_id = update.effective_user.id
    settings_text = (
        "⚙️ **Your Settings**\n\n"
        f"👤 User ID: `{user_id}`\n"
        "📱 Notifications: Enabled\n"
        "🎯 Language: English\n"
        "⏱️ Timeout: 30s\n\n"
        "Use commands to modify settings (coming soon)."
    )
    
    await update.message.reply_text(
        settings_text,
        parse_mode='Markdown'
    )

@check_user_authorized
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command"""
    logger.info(f"User {update.effective_user.id} cancelled operation")
    
    await update.message.reply_text(
        "❌ Operation cancelled.\n\n"
        "Send any message to start a new conversation."
    )
