"""
Custom exceptions for the Competitor Insights Assistant.

This module defines application-specific exceptions that provide
clear error handling and meaningful messages throughout the system.
"""

from typing import Any, Dict, Optional


class CompetitorInsightsError(Exception):
    """Base exception for all Competitor Insights Assistant errors."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class BusinessNotFoundError(CompetitorInsightsError):
    """Raised when a business cannot be found by the data provider."""

    def __init__(self, identifier: str, provider: str = "unknown"):
        super().__init__(
            message=f"Business '{identifier}' could not be found",
            error_code="BUSINESS_NOT_FOUND",
            details={"identifier": identifier, "provider": provider},
        )


class BusinessDataError(CompetitorInsightsError):
    """Raised when business data is invalid or insufficient."""

    def __init__(self, message: str, business_name: str = None):
        super().__init__(
            message=f"Business data error: {message}",
            error_code="BUSINESS_DATA_ERROR",
            details={"business_name": business_name},
        )


class ExternalAPIError(CompetitorInsightsError):
    """Raised when external API calls fail."""

    def __init__(self, provider: str, message: str, status_code: Optional[int] = None):
        super().__init__(
            message=f"External API error from {provider}: {message}",
            error_code="EXTERNAL_API_ERROR",
            details={"provider": provider, "status_code": status_code},
        )


class LLMServiceError(CompetitorInsightsError):
    """Raised when LLM service calls fail."""

    def __init__(self, provider: str, message: str):
        super().__init__(
            message=f"LLM service error from {provider}: {message}",
            error_code="LLM_SERVICE_ERROR",
            details={"provider": provider},
        )


class RateLimitError(CompetitorInsightsError):
    """Raised when API rate limits are exceeded."""

    def __init__(self, provider: str, message: str = None):
        default_message = f"Rate limit exceeded for {provider}"
        super().__init__(
            message=message or default_message,
            error_code="RATE_LIMIT_ERROR",
            details={"provider": provider},
        )


class ServiceError(CompetitorInsightsError):
    """Raised when service operations fail."""

    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"Service error in {service}: {message}",
            error_code="SERVICE_ERROR",
            details={"service": service},
        )


class ValidationError(CompetitorInsightsError):
    """Raised when input validation fails."""

    def __init__(self, field: str, message: str, value: Optional[Any] = None):
        super().__init__(
            message=f"Validation error for {field}: {message}",
            error_code="VALIDATION_ERROR",
            details={"field": field, "value": value},
        )


class InsufficientDataError(CompetitorInsightsError):
    """Raised when there's not enough data to perform comparison."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="INSUFFICIENT_DATA",
        )
