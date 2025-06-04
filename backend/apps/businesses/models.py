"""
Business profile models.

This module defines models for storing business profile information
and related attributes used in competitive analysis.
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from django.core.validators import MinValueValidator
from django.db import models

from apps.common.logging import get_logger

logger = get_logger(__name__)


class BusinessProfile(models.Model):
    """
    Model representing a business profile.

    Stores core business information including name, website, address, and
    other business attributes.
    """

    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Business name as it appears in search results",
    )
    website = models.URLField(blank=True, help_text="Business website URL")
    address = models.TextField(blank=True, help_text="Full business address")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Business latitude",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Business longitude",
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Business rating",
    )
    rating_count = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)], help_text="Number of ratings"
    )
    image_count = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of business photos",
    )
    type = models.CharField(max_length=255, blank=True, help_text="Business type")
    has_hours = models.BooleanField(
        default=False, help_text="Whether business hours are listed"
    )
    has_description = models.BooleanField(
        default=False, help_text="Whether business description is provided"
    )
    has_menu_link = models.BooleanField(
        default=False, help_text="Whether menu/services link is available"
    )
    has_price_level = models.BooleanField(
        default=False, help_text="Whether price level is provided"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Profile"
        verbose_name_plural = "Business Profiles"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name", "website"]),
        ]

    def __str__(self) -> str:
        return f"{self.name}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert business profile to dictionary format.

        Returns:
            Dictionary representation of the business profile
        """
        return {
            "id": self.pk,
            "name": self.name,
            "website": self.website,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "rating": self.rating,
            "rating_count": self.rating_count,
            "image_count": self.image_count,
            "type": self.type,
            "has_hours": self.has_hours,
            "has_description": self.has_description,
            "has_menu_link": self.has_menu_link,
            "has_price_level": self.has_price_level,
            # "created_at": self.created_at.isoformat(),
            # "updated_at": self.updated_at.isoformat(),
        }

    def completeness_score(self) -> float:
        """
        Calculate profile completeness score.

        Returns:
            Score from 0.0 to 1.0 representing profile completeness
        """
        total_fields = 3  # hours, description, menu_link
        completed_fields = sum(
            [
                self.has_hours,
                self.has_description,
                self.has_menu_link,
            ]
        )

        base_score = completed_fields / total_fields

        # Bonus points for having reviews and images
        if self.rating_count > 0:
            base_score += 0.1
        if self.image_count > 0:
            base_score += 0.1

        return min(base_score, 1.0)


@dataclass
class BusinessProfileData:
    name: str = ""
    website: str = ""
    address: str = ""
    rating: float = 0.0
    rating_count: int = 0
    image_count: int = 0
    category: str = ""
    has_hours: bool = False
    has_description: bool = False
    has_menu_link: bool = False
    has_price_level: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def completeness_score(self) -> float:
        """Calculate profile completeness score."""
        completed_fields = sum(
            [
                self.has_hours,
                self.has_description,
                self.has_menu_link,
            ]
        )
        base_score = completed_fields / 3
        if self.rating_count > 0:
            base_score += 0.1
        if self.image_count > 0:
            base_score += 0.1
        return min(base_score, 1.0)
