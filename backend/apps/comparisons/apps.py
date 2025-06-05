"""
Django app configuration for the comparisons app.
"""

from django.apps import AppConfig


class ComparisonsConfig(AppConfig):
    """Configuration for the comparisons app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.comparisons"
    verbose_name = "Business Comparisons"
