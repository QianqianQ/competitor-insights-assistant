"""
Structured logging configuration using structlog.

This module configures structlog for the Django application with
proper development and production configurations based on Context7
best practices.
"""

import logging
import sys
from typing import Any, Dict

import structlog
from django.conf import settings


def configure_structlog() -> None:
    """
    Configure structlog for Django application with clean line breaks.
    """
    # Shared processors for both environments
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        # structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
    ]

    # Determine if we're in a development environment
    is_development = getattr(settings, "DEBUG", False) and sys.stderr.isatty()

    if is_development:
        # Pretty printing for development with clean line breaks
        def add_newline(_, __, event_dict):
            """Add newline before/after each log entry."""
            event_dict["message"] = f"\n{event_dict.get('message', '')}\n"
            return event_dict

        processors = shared_processors + [
            add_newline,  # Add newlines
            structlog.dev.ConsoleRenderer(
                colors=True,
                force_colors=True,  # Ensure colors work in all terminals
                pad_event=30,  # Pad events for alignment
            ),
        ]
    else:
        # JSON output for production (single-line by default)
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def configure_django_logging() -> None:
    """
    Configure Django's logging to work with structlog.

    This ensures that Django's internal logging (database queries,
    request processing, etc.) is formatted consistently with structlog.
    """
    # timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    # pre_chain = [
    #     structlog.stdlib.add_log_level,
    #     structlog.stdlib.ExtraAdder(),
    #     # timestamper,
    # ]

    # Determine log level from Django settings
    log_level = getattr(settings, "LOG_LEVEL", "INFO")
    is_development = getattr(settings, "DEBUG", False) and sys.stderr.isatty()

    formatter_config = {
        "()": structlog.stdlib.ProcessorFormatter,
        "processors": [
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            # Skip Django's log level by omitting `add_log_level` here
            (
                structlog.dev.ConsoleRenderer(colors=True)
                if is_development
                else structlog.processors.JSONRenderer()
            ),
        ],
        "foreign_pre_chain": [
            # Only include processors that don't add log levels
            structlog.stdlib.ExtraAdder(),
        ],
    }

    # Django logging configuration
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": formatter_config,
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "structured",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": log_level,
                "propagate": True,
            },
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": "DEBUG" if is_development else "INFO",
                "propagate": False,
            },
            "apps": {  # Our application logs
                "handlers": ["console"],
                "level": "DEBUG" if is_development else "INFO",
                "propagate": False,
            },
        },
    }

    # Apply the configuration
    logging.config.dictConfig(LOGGING)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """
    Get a configured structlog logger.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured structlog logger instance
    """
    return structlog.get_logger(name)


def bind_request_context(request) -> None:
    """
    Bind Django request context to structlog.

    This should be called in middleware to add request-specific
    context to all log messages during request processing.

    Args:
        request: Django HttpRequest object
    """
    # Clear any existing context
    structlog.contextvars.clear_contextvars()

    # Extract useful request information
    user_id = None
    username = None
    if hasattr(request, "user") and request.user.is_authenticated:
        user_id = request.user.pk
        username = request.user.username

    # Get client IP
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.META.get("REMOTE_ADDR", "unknown")

    # Bind context variables
    context = {
        "request_id": request.META.get("HTTP_X_REQUEST_ID", "unknown"),
        "method": request.method,
        "path": request.path,
        "client_ip": client_ip,
        "user_agent": request.META.get("HTTP_USER_AGENT", "unknown"),
    }

    if user_id:
        context.update(
            {
                "user_id": user_id,
                "username": username,
            }
        )

    structlog.contextvars.bind_contextvars(**context)


def bind_business_context(business_data: Dict[str, Any]) -> None:
    """
    Bind business-specific context to structlog.

    Args:
        business_data: Dictionary containing business information
    """
    context = {}

    if "id" in business_data:
        context["business_id"] = business_data["id"]
    if "name" in business_data:
        context["business_name"] = business_data["name"]
    if "data_source" in business_data:
        context["data_source"] = business_data["data_source"]

    structlog.contextvars.bind_contextvars(**context)


def bind_comparison_context(
    user_business_id: int, competitor_ids: list, comparison_id: str = None
) -> None:
    """
    Bind comparison-specific context to structlog.

    Args:
        user_business_id: ID of the user's business
        competitor_ids: List of competitor business IDs
        comparison_id: Optional comparison report ID
    """
    context = {
        "user_business_id": user_business_id,
        "competitor_count": len(competitor_ids),
        "competitor_ids": competitor_ids,
    }

    if comparison_id:
        context["comparison_id"] = comparison_id

    structlog.contextvars.bind_contextvars(**context)


class RequestLoggingMiddleware:
    """
    Middleware to add request context to all log messages.

    This middleware should be added near the top of the middleware stack
    to ensure all subsequent logging includes request context.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bind request context at the start of request processing
        bind_request_context(request)

        # Get logger for request logging
        logger = get_logger(__name__)

        # Log request start
        logger.info(
            "request_started",
            method=request.method,
            path=request.path,
            content_length=request.META.get("CONTENT_LENGTH", 0),
        )

        response = self.get_response(request)

        # Log request completion
        logger.info(
            "request_completed",
            status_code=response.status_code,
            content_length=(
                len(response.content) if hasattr(response, "content") else 0
            ),
        )

        # Clear context at the end of request
        structlog.contextvars.clear_contextvars()

        return response


# Initialize logging configuration
configure_structlog()
configure_django_logging()
