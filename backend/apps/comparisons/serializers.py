"""
Django REST Framework serializers for comparison operations.

This module defines serializers for API request/response handling
following DRF best practices.
"""

from rest_framework import serializers

from apps.businesses.models import BusinessProfile
from apps.comparisons.models import ComparisonReport


class ComparisonRequestSerializer(serializers.Serializer):
    """Serializer for comparison creation requests."""

    user_business_identifier = serializers.CharField(
        max_length=500, help_text="User's business name or website URL"
    )

    def validate_user_business_identifier(self, value: str) -> str:
        """Validate user business identifier."""
        if not value.strip():
            raise serializers.ValidationError("Business identifier cannot be empty")
        return value.strip()


class BusinessProfileSerializer(serializers.ModelSerializer):
    """Serializer for business profile information."""

    class Meta:
        model = BusinessProfile
        fields = [
            "id",
            "name",
            "website",
            "address",
            "latitude",
            "longitude",
            "rating",
            "rating_count",
            "image_count",
            "type",
            "has_hours",
            "has_description",
            "has_menu_link",
            "has_price_level",
            "created_at",
            "updated_at",
        ]


class ComparisonReportSerializer(serializers.ModelSerializer):
    """Serializer for comparison report responses."""

    user_business = BusinessProfileSerializer(read_only=True)
    competitor_businesses = BusinessProfileSerializer(many=True, read_only=True)
    competitor_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ComparisonReport
        fields = [
            "id",
            "report_id",
            "user_business",
            "competitor_businesses",
            "competitor_count",
            "ai_comparison_summary",
            "ai_improvement_suggestions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
