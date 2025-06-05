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
    report_style = serializers.ChoiceField(
        choices=[
            ("casual", "Casual"),
            ("data-driven", "Data-driven"),
        ],
        default="casual",
        required=False,
        help_text="AI report style",
    )

    def validate_user_business_identifier(self, value: str) -> str:
        """Validate user business identifier."""
        if not value.strip():
            raise serializers.ValidationError(
                "Business identifier cannot be empty"
            )
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

    # User business: dict from BusinessProfileData.to_dict()
    user_business = serializers.JSONField()
    # Competitors: list of dicts from BusinessProfileData.to_dict()
    competitor_businesses = serializers.ListField(
        child=serializers.JSONField(),
        read_only=True
    )
    competitor_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ComparisonReport
        fields = [
            # "report_id",  # Added report_id for future frontend use
            "user_business",
            "competitor_businesses",
            "competitor_count",  # Remove if sending the full list
            "ai_comparison_summary",
            "ai_improvement_suggestions",
            "metadata",
            "created_at",  # Added created_at for future frontend use
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
