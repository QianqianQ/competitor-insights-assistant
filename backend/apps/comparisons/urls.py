"""
URL configuration for comparison operations.

This module defines the URL patterns for business comparison
and business profile endpoints using DRF routers.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.comparisons import views

# Create router for ViewSets
router = DefaultRouter()
router.register("comparisons", views.ComparisonViewSet, basename="comparison")
# router.register('businesses', views.BusinessProfileViewSet, basename='business')

app_name = "comparisons"

urlpatterns = [
    # Include all router URLs
    path("", include(router.urls)),
]
