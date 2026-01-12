class DomainError(Exception):
    """Base class for all domain-level errors."""


class InvalidParameterError(DomainError):
    """Raised when domain objects receive invalid parameters."""


class NoEquilibriumError(DomainError):
    """Raised when a valid economic equilibrium cannot be formed."""
