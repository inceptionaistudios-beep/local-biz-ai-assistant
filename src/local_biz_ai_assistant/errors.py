"""Domain exceptions with user-safe messages."""


class LocalBizAssistantError(Exception):
    """Base exception for expected application errors."""


class ConfigurationError(LocalBizAssistantError):
    """Raised when local configuration is invalid or incomplete."""


class ProviderError(LocalBizAssistantError):
    """Raised when an optional remote provider fails safely."""
