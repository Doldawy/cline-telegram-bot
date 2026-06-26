"""Concierge service module for intelligent user assistance"""

from enum import Enum
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger
import json

class TicketStatus(str, Enum):
    """Support ticket status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"

class PriorityLevel(str, Enum):
    """Ticket priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class SupportTicket:
    """Support ticket data model"""
    ticket_id: str
    user_id: int
    title: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: TicketStatus = TicketStatus.OPEN
    priority: PriorityLevel = PriorityLevel.MEDIUM
    messages: List[Dict[str, Any]] = field(default_factory=list)
    assigned_to: Optional[str] = None
    
    def add_message(self, sender: str, message: str, timestamp: Optional[datetime] = None) -> None:
        """Add a message to the ticket"""
        self.messages.append({
            'sender': sender,
            'message': message,
            'timestamp': timestamp or datetime.now()
        })
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ticket to dictionary"""
        return {
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status.value,
            'priority': self.priority.value,
            'messages': self.messages,
            'assigned_to': self.assigned_to
        }

class ConciergeAI:
    """Intelligent Concierge AI for user assistance"""
    
    # Common help topics and responses
    HELP_TOPICS = {
        'commands': (
            "📋 **Available Commands:**\n\n"
            "/start - Start the bot\n"
            "/help - Show all commands\n"
            "/status - Check Cline status\n"
            "/ask <message> - Ask Cline AI\n"
            "/support - Open a support ticket\n"
            "/ticket <id> - Check ticket status\n"
            "/cancel - Cancel current operation\n\n"
            "💡 Just send any message to chat with Cline!"
        ),
        'getting_started': (
            "🚀 **Getting Started Guide**\n\n"
            "1️⃣ Send /start to initialize\n"
            "2️⃣ Type any question or task\n"
            "3️⃣ I'll forward it to Cline AI\n"
            "4️⃣ Get instant responses\n\n"
            "📝 **Examples:**\n"
            "• 'Write a Python function'\n"
            "• 'Explain machine learning'\n"
            "• 'Debug this code'\n\n"
            "🆘 Need help? Use /support"
        ),
        'security': (
            "🔒 **Security & Privacy**\n\n"
            "✅ Your data is encrypted\n"
            "✅ Only authorized users can access\n"
            "✅ Messages are not stored permanently\n"
            "✅ All communications are secure\n\n"
            "⚠️ **Best Practices:**\n"
            "• Don't share passwords\n"
            "• Keep your token secret\n"
            "• Report suspicious activity\n\n"
            "Questions? Contact /support"
        ),
        'faq': (
            "❓ **Frequently Asked Questions**\n\n"
            "**Q: What is Cline Bot?**\n"
            "A: An AI assistant controller accessible via Telegram\n\n"
            "**Q: How fast are responses?**\n"
            "A: Usually within 1-3 seconds\n\n"
            "**Q: Can I use it offline?**\n"
            "A: No, internet connection required\n\n"
            "**Q: Is my data safe?**\n"
            "A: Yes, fully encrypted and secure\n\n"
            "More questions? Use /support"
        ),
        'troubleshooting': (
            "🔧 **Troubleshooting Guide**\n\n"
            "**Bot not responding?**\n"
            "• Check your internet connection\n"
            "• Try /start again\n"
            "• Restart the application\n\n"
            "**Getting errors?**\n"
            "• Note the error message\n"
            "• Use /support to report\n"
            "• Include error details\n\n"
            "**Still having issues?**\n"
            "Contact support: /support"
        )
    }
    
    def __init__(self):
        """Initialize Concierge AI"""
        self.tickets: Dict[str, SupportTicket] = {}
        self.user_sessions: Dict[int, Dict[str, Any]] = {}
        logger.info("🧎 Concierge AI initialized")
    
    def get_help(self, topic: Optional[str] = None) -> str:
        """Get help for a specific topic"""
        if not topic or topic.lower() not in self.HELP_TOPICS:
            return (
                "📚 **Help Topics Available:**\n\n"
                "• /help commands - Show all commands\n"
                "• /help getting_started - Quick start guide\n"
                "• /help security - Security info\n"
                "• /help faq - FAQ\n"
                "• /help troubleshooting - Troubleshooting\n\n"
                "Use /help <topic> for more details."
            )
        
        return self.HELP_TOPICS.get(topic.lower(), "Topic not found")
    
    def create_support_ticket(self, user_id: int, title: str, description: str, 
                            priority: PriorityLevel = PriorityLevel.MEDIUM) -> SupportTicket:
        """Create a new support ticket"""
        ticket_id = f"TK-{user_id}-{int(datetime.now().timestamp())}"
        
        ticket = SupportTicket(
            ticket_id=ticket_id,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority
        )
        
        self.tickets[ticket_id] = ticket
        logger.info(f"🎫 Support ticket created: {ticket_id}")
        
        return ticket
    
    def get_ticket(self, ticket_id: str) -> Optional[SupportTicket]:
        """Get a support ticket by ID"""
        return self.tickets.get(ticket_id)
    
    def add_ticket_message(self, ticket_id: str, sender: str, message: str) -> bool:
        """Add a message to a ticket"""
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False
        
        ticket.add_message(sender, message)
        logger.debug(f"💬 Message added to ticket {ticket_id}")
        return True
    
    def update_ticket_status(self, ticket_id: str, status: TicketStatus) -> bool:
        """Update ticket status"""
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False
        
        ticket.status = status
        ticket.updated_at = datetime.now()
        logger.info(f"📋 Ticket {ticket_id} status updated to {status.value}")
        return True
    
    def get_user_tickets(self, user_id: int) -> List[SupportTicket]:
        """Get all tickets for a user"""
        return [t for t in self.tickets.values() if t.user_id == user_id]
    
    def get_open_tickets(self) -> List[SupportTicket]:
        """Get all open tickets"""
        return [t for t in self.tickets.values() if t.status in [TicketStatus.OPEN, TicketStatus.IN_PROGRESS]]
    
    def intelligently_respond(self, user_message: str) -> str:
        """Generate intelligent response based on user message"""
        message_lower = user_message.lower()
        
        # Detect user intent
        if any(word in message_lower for word in ['help', 'how', 'what', '?']):
            return self._handle_help_request(user_message)
        elif any(word in message_lower for word in ['error', 'problem', 'issue', 'bug', 'broken']):
            return self._handle_problem_report(user_message)
        elif any(word in message_lower for word in ['thank', 'thanks', 'thanks!']):
            return self._handle_appreciation()
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
            return self._handle_greeting()
        else:
            return self._default_response()
    
    def _handle_help_request(self, message: str) -> str:
        """Handle help requests"""
        return (
            "📖 **I'm here to help!**\n\n"
            "What do you need assistance with?\n\n"
            "• 'help commands' - Show all commands\n"
            "• 'help getting_started' - Quick start\n"
            "• 'help faq' - FAQ\n"
            "• 'support' - Open a support ticket\n\n"
            "Or just describe your issue and I'll help! 😊"
        )
    
    def _handle_problem_report(self, message: str) -> str:
        """Handle problem reports"""
        return (
            "🔧 **I'm sorry to hear you're experiencing an issue.**\n\n"
            "Let me help you:\n\n"
            "1️⃣ Try: /status (check if bot is online)\n"
            "2️⃣ Try: /help troubleshooting (for common issues)\n"
            "3️⃣ Use: /support (to open a support ticket)\n\n"
            "📝 In your support ticket, please include:\n"
            "• What were you trying to do?\n"
            "• What went wrong?\n"
            "• Any error messages?\n\n"
            "I'll get back to you as soon as possible! 🚀"
        )
    
    def _handle_appreciation(self) -> str:
        """Handle appreciation messages"""
        return (
            "😊 **You're welcome!**\n\n"
            "I'm happy I could help! 🎉\n\n"
            "If you need anything else, just let me know. "
            "Feel free to use /support for any additional assistance."
        )
    
    def _handle_greeting(self) -> str:
        """Handle greetings"""
        return (
            "👋 **Hello there!**\n\n"
            "Welcome to Cline Bot! 🤖\n\n"
            "I'm your intelligent assistant. Here's what I can do:\n\n"
            "• Answer your questions\n"
            "• Forward requests to Cline AI\n"
            "• Help you with issues\n"
            "• Provide technical support\n\n"
            "What can I help you with today?"
        )
    
    def _default_response(self) -> str:
        """Default response for other messages"""
        return (
            "👍 **Got it!**\n\n"
            "I'll help you with that.\n\n"
            "You can:\n"
            "• Ask me a question\n"
            "• Request support: /support\n"
            "• Get help: /help\n\n"
            "What would you like to do?"
        )
    
    def get_ticket_status_message(self, ticket: SupportTicket) -> str:
        """Generate ticket status message"""
        status_emoji = {
            TicketStatus.OPEN: "🆕",
            TicketStatus.IN_PROGRESS: "⏳",
            TicketStatus.WAITING: "⏸️",
            TicketStatus.RESOLVED: "✅",
            TicketStatus.CLOSED: "❌"
        }
        
        priority_emoji = {
            PriorityLevel.LOW: "🟢",
            PriorityLevel.MEDIUM: "🟡",
            PriorityLevel.HIGH: "🟠",
            PriorityLevel.URGENT: "🔴"
        }
        
        return (
            f"🎫 **Support Ticket: {ticket.ticket_id}**\n\n"
            f"📋 **Title:** {ticket.title}\n"
            f"{status_emoji.get(ticket.status, '❓')} **Status:** {ticket.status.value}\n"
            f"{priority_emoji.get(ticket.priority, '❓')} **Priority:** {ticket.priority.value}\n"
            f"👤 **Assigned to:** {ticket.assigned_to or 'Pending'}\n"
            f"⏰ **Created:** {ticket.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"🔄 **Updated:** {ticket.updated_at.strftime('%Y-%m-%d %H:%M')}\n\n"
            f"💬 **Messages:** {len(ticket.messages)}\n"
        )

# Global Concierge instance
concierge = ConciergeAI()
