"""
Django app configuration for the businesses app.
"""

from django.apps import AppConfig


class BusinessesConfig(AppConfig):
    """Configuration for the businesses app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.businesses"
    verbose_name = "Business Profiles"
