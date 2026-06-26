"""Concierge handlers for bot integration"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from loguru import logger
from concierge.service import concierge, TicketStatus, PriorityLevel
from utils.security import check_user_authorized

# Conversation states
ASK_TITLE = 1
ASK_DESCRIPTION = 2
ASK_PRIORITY = 3

@check_user_authorized
async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /support command - start support ticket creation"""
    user = update.effective_user
    logger.info(f"🆘 Support requested by {user.id}")
    
    await update.message.reply_text(
        "🆘 **Create Support Ticket**\n\n"
        "I'll help you report an issue or request assistance.\n\n"
        "What is the title of your issue? "
        "(e.g., 'Bot not responding', 'Feature request')"
    )
    
    return ASK_TITLE

async def ask_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get ticket title"""
    context.user_data['title'] = update.message.text
    
    await update.message.reply_text(
        "✏️ **Now, describe the issue in detail:**\n\n"
        "Please provide as much information as possible to help us understand your issue."
    )
    
    return ASK_DESCRIPTION

async def ask_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get ticket description"""
    context.user_data['description'] = update.message.text
    
    priority_buttons = (
        "🟢 Low - General inquiry\n"
        "🟡 Medium - Normal issue\n"
        "🟠 High - Important problem\n"
        "🔴 Urgent - Critical issue\n\n"
        "Reply with the priority level or type 'medium' to continue."
    )
    
    await update.message.reply_text(
        "⚡ **Set Priority Level:**\n\n" + priority_buttons
    )
    
    return ASK_PRIORITY

async def ask_priority(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get priority and create ticket"""
    user = update.effective_user
    priority_text = update.message.text.lower()
    
    # Map priority input to enum
    priority_map = {
        'low': PriorityLevel.LOW,
        'green': PriorityLevel.LOW,
        '🟢': PriorityLevel.LOW,
        'medium': PriorityLevel.MEDIUM,
        'yellow': PriorityLevel.MEDIUM,
        '🟡': PriorityLevel.MEDIUM,
        'high': PriorityLevel.HIGH,
        'orange': PriorityLevel.HIGH,
        '🟠': PriorityLevel.HIGH,
        'urgent': PriorityLevel.URGENT,
        'red': PriorityLevel.URGENT,
        '🔴': PriorityLevel.URGENT
    }
    
    priority = priority_map.get(priority_text, PriorityLevel.MEDIUM)
    
    # Create the ticket
    ticket = concierge.create_support_ticket(
        user_id=user.id,
        title=context.user_data['title'],
        description=context.user_data['description'],
        priority=priority
    )
    
    logger.info(f"🎫 Ticket created for user {user.id}: {ticket.ticket_id}")
    
    response = (
        f"✅ **Support Ticket Created!**\n\n"
        f"🎫 **Ticket ID:** `{ticket.ticket_id}`\n"
        f"📋 **Title:** {ticket.title}\n"
        f"⚡ **Priority:** {priority.value}\n\n"
        f"Thank you for contacting support! We'll review your issue and get back to you soon.\n\n"
        f"You can check your ticket status anytime with:\n"
        f"`/ticket {ticket.ticket_id}`"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')
    
    return ConversationHandler.END

async def cancel_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel support ticket creation"""
    await update.message.reply_text(
        "❌ **Support ticket creation cancelled.**\n\n"
        "You can always open a ticket later using /support."
    )
    return ConversationHandler.END

@check_user_authorized
async def ticket_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ticket command - check ticket status"""
    user = update.effective_user
    
    if not context.args:
        # Show user's tickets
        tickets = concierge.get_user_tickets(user.id)
        
        if not tickets:
            await update.message.reply_text(
                "🗂️ **No Tickets Found**\n\n"
                "You don't have any support tickets yet.\n\n"
                "Use /support to create one."
            )
            return
        
        # List all user tickets
        response = "📋 **Your Support Tickets:**\n\n"
        for ticket in tickets:
            response += f"🎫 **{ticket.ticket_id}** - {ticket.title}\n"
            response += f"   Status: {ticket.status.value}\n\n"
        
        response += "Use `/ticket <ticket_id>` to see details."
        await update.message.reply_text(response)
    else:
        # Get specific ticket
        ticket_id = context.args[0]
        ticket = concierge.get_ticket(ticket_id)
        
        if not ticket or ticket.user_id != user.id:
            await update.message.reply_text(
                "❌ **Ticket Not Found**\n\n"
                "The ticket ID you provided doesn't exist or doesn't belong to you."
            )
            return
        
        response = concierge.get_ticket_status_message(ticket)
        
        # Add recent messages
        if ticket.messages:
            response += "\n💬 **Recent Messages:**\n\n"
            for msg in ticket.messages[-3:]:  # Last 3 messages
                sender = "👤 You" if msg['sender'] == 'user' else "🤖 Support"
                response += f"{sender}: {msg['message'][:100]}...\n"
        
        await update.message.reply_text(response, parse_mode='Markdown')

@check_user_authorized
async def concierge_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle concierge help requests"""
    topic = ' '.join(context.args).lower() if context.args else None
    response = concierge.get_help(topic)
    
    await update.message.reply_text(response, parse_mode='Markdown')

@check_user_authorized
async def intelligent_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate intelligent Concierge response"""
    message_text = update.message.text
    
    logger.debug(f"🤖 Concierge processing: {message_text[:50]}...")
    
    response = concierge.intelligently_respond(message_text)
    await update.message.reply_text(response, parse_mode='Markdown')
