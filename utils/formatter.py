"""Message formatting utilities"""

from typing import Dict, Any

def format_code_block(code: str, language: str = 'python') -> str:
    """Format code as a code block"""
    return f"```{language}\n{code}\n```"

def format_error_message(error: str) -> str:
    """Format error message"""
    return f"❌ **Error:** {error}"

def format_success_message(message: str) -> str:
    """Format success message"""
    return f"✅ **Success:** {message}"

def format_info_message(message: str) -> str:
    """Format info message"""
    return f"ℹ️ **Info:** {message}"

def format_response(response: Dict[str, Any]) -> str:
    """Format Cline API response"""
    if response.get('status') == 'success':
        return f"✅ {response.get('message', 'Success')}"
    else:
        return f"❌ {response.get('message', 'Unknown error')}"
