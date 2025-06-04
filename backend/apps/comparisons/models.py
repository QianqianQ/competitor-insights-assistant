"""
Django models for business comparison reports.

This module defines models for storing comparison results and AI-generated
insights and recommendations.
"""

import uuid

from django.db import models


class ComparisonReport(models.Model):
    """
    Stores the results of a business profile comparison.

    This model contains the comparison results, AI-generated summary,
    and improvement suggestions for a business comparison session.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_id = models.CharField(
        max_length=50, unique=True, help_text="Human-readable report identifier"
    )

    # Business relationships
    # user_business = models.ForeignKey(
    #     BusinessProfile,
    #     on_delete=models.CASCADE,
    #     related_name="user_comparison_reports",
    #     help_text="The user's business being compared"
    # )
    # competitor_businesses = models.ManyToManyField(
    #     BusinessProfile,
    #     related_name="competitor_comparison_reports",
    #     help_text="Competitor businesses in this comparison"
    # )
    user_business = models.JSONField(default=dict, help_text="User's business profile")
    competitor_businesses = models.JSONField(
        default=list, help_text="Competitor businesses in this comparison"
    )

    # AI-generated content
    ai_comparison_summary = models.TextField(
        help_text="AI-generated summary of the comparison"
    )
    ai_improvement_suggestions = models.JSONField(
        default=list, help_text="List of AI-generated improvement suggestions"
    )

    # Comparison metadata
    comparison_data = models.JSONField(
        default=dict, help_text="Structured comparison data used for analysis"
    )
    # llm_provider = models.CharField(
    #     max_length=50,
    #     default="openai",
    #     help_text="LLM provider used for analysis"
    # )
    # llm_model = models.CharField(
    #     max_length=100,
    #     default="gpt-4",
    #     help_text="Specific LLM model used"
    # )
    # tokens_used = models.PositiveIntegerField(
    #     default=0,
    #     help_text="Total tokens used for LLM processing"
    # )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comparison_reports"
        indexes = [
            models.Index(fields=["user_business"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return (
            f"Comparison {self.report_id} for "
            f"{self.user_business.name or self.user_business.website}"
        )

    def save(self, *args, **kwargs):
        """Generate report_id if not provided."""
        if not self.report_id:
            self.report_id = f"comp_rpt_{uuid.uuid4().hex[:10]}"
        super().save(*args, **kwargs)

    @property
    def competitor_count(self) -> int:
        """Return the number of competitors in this comparison."""
        return len(self.competitor_businesses)

    def get_summary_data(self) -> dict:
        """
        Get a summary of the comparison for API responses.

        Returns:
            Dictionary containing comparison summary data
        """
        return {
            "report_id": self.report_id,
            "user_business": {
                "name": self.user_business.name,
                "website": self.user_business.website,
                "address": self.user_business.address,
                "latitude": self.user_business.latitude,
                "longitude": self.user_business.longitude,
                "rating": self.user_business.rating,
                "rating_count": self.user_business.rating_count,
                "image_count": self.user_business.image_count,
                "category": self.user_business.category,
                "has_hours": self.user_business.has_hours,
                "has_description": self.user_business.has_description,
                "has_menu_link": self.user_business.has_menu_link,
                "has_price_level": self.user_business.has_price_level,
            },
            "competitor_count": self.competitor_count,
            "ai_summary": self.ai_comparison_summary,
            "suggestions_count": len(self.ai_improvement_suggestions),
        }
