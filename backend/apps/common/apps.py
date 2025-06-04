"""
Django app configuration for the common app.
"""

from django.apps import AppConfig


class CommonConfig(AppConfig):
    """Configuration for the common app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"
    verbose_name = "Common Utilities"

    def ready(self):
        """Initialize app when Django starts."""
        # Configure structured logging when app is ready
        from apps.common.logging import configure_django_logging, configure_structlog

        configure_structlog()
        configure_django_logging()
