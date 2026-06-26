"""Logging utilities"""

from loguru import logger
from datetime import datetime
from typing import Optional

def log_message(user_id: int, message: str, sender: str = 'user') -> None:
    """Log a message"""
    timestamp = datetime.now().isoformat()
    
    if sender == 'user':
        logger.debug(f"[{timestamp}] USER {user_id}: {message[:100]}...")
    elif sender == 'bot':
        logger.debug(f"[{timestamp}] BOT -> USER {user_id}: {message[:100]}...")
    else:
        logger.debug(f"[{timestamp}] {sender}: {message[:100]}...")

def log_command(user_id: int, command: str) -> None:
    """Log a command execution"""
    logger.info(f"CMD [{user_id}]: /{command}")

def log_error(error_message: str, context: Optional[str] = None) -> None:
    """Log an error"""
    if context:
        logger.error(f"[{context}] {error_message}")
    else:
        logger.error(error_message)
