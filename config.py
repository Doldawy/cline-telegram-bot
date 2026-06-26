import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Bot configuration settings"""
    
    # Telegram Configuration
    telegram_bot_token: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    allowed_user_ids: str = os.getenv('ALLOWED_USER_IDS', '')
    
    # Cline Configuration
    cline_api_url: str = os.getenv('CLINE_API_URL', 'http://localhost:3000')
    cline_api_key: str = os.getenv('CLINE_API_KEY', '')
    
    # Bot Settings
    bot_log_level: str = os.getenv('BOT_LOG_LEVEL', 'INFO')
    bot_timeout: int = int(os.getenv('BOT_TIMEOUT', '30'))
    bot_rate_limit: int = int(os.getenv('BOT_RATE_LIMIT', '10'))
    
    # Redis Configuration
    redis_host: str = os.getenv('REDIS_HOST', 'localhost')
    redis_port: int = int(os.getenv('REDIS_PORT', '6379'))
    redis_db: int = int(os.getenv('REDIS_DB', '0'))
    
    # Security
    enable_rate_limiting: bool = os.getenv('ENABLE_RATE_LIMITING', 'true').lower() == 'true'
    enable_message_sanitization: bool = os.getenv('ENABLE_MESSAGE_SANITIZATION', 'true').lower() == 'true'
    session_timeout_minutes: int = int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
    
    class Config:
        env_file = '.env'
    
    @property
    def allowed_users(self) -> List[int]:
        """Parse allowed user IDs from string"""
        if not self.allowed_user_ids:
            return []
        try:
            return [int(uid.strip()) for uid in self.allowed_user_ids.split(',')]
        except ValueError:
            return []
    
    def is_user_allowed(self, user_id: int) -> bool:
        """Check if user is in allowed list"""
        return user_id in self.allowed_users
    
    def validate_config(self) -> bool:
        """Validate essential configuration"""
        if not self.telegram_bot_token:
            raise ValueError('TELEGRAM_BOT_TOKEN is not set')
        if not self.allowed_user_ids:
            raise ValueError('ALLOWED_USER_IDS is not set')
        return True

# Global settings instance
settings = Settings()
