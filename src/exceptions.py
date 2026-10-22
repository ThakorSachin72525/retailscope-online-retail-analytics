"""Custom exceptions used across RetailScope."""
class RetailScopeError(Exception):
    """Base exception for expected project errors."""

class DataSourceError(RetailScopeError):
    """Raised when the public dataset cannot be retrieved."""

class SchemaValidationError(RetailScopeError):
    """Raised when source data does not meet the required schema."""
