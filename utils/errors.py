class BotError(Exception):
    """Base exception for bot errors"""
    pass

class ConfigError(BotError):
    """Configuration error"""
    pass