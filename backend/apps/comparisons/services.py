"""
Service layer for business comparison operations.

This module implements the core business logic for comparing business profiles
and generating AI-powered insights and recommendations.
"""

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List
from config.settings.base import PERPELEXITY_AI_API_KEY

from apps.businesses.models import BusinessProfileData
from apps.common.exceptions import BusinessDataError, ValidationError
from apps.common.logging import get_logger
from apps.comparisons.models import ComparisonReport
from apps.providers.data_providers import SerperBusinessDataProvider
from apps.providers.llm_providers import OpenAIProvider

logger = get_logger(__name__)


@dataclass
class LLMResponse:
    """LLM response data class."""

    content: str
    suggestions: List[str]
    tokens_used: int
    model: str
    provider: str


class ComparisonService:
    """
    Service class for handling business profile comparisons.

    This service orchestrates the entire comparison workflow:
    1. Fetch business data from external providers
    2. Store/update business profiles in database
    3. Generate AI-powered comparison analysis
    4. Store and return comparison results
    """

    def __init__(self):
        """Initialize the comparison service with providers."""
        self.data_provider = SerperBusinessDataProvider(
            api_key="mock-key",  # Will be replaced with real key
        )
        self.llm_provider = OpenAIProvider(
            api_key=PERPELEXITY_AI_API_KEY
        )

    def create_comparison(
        self,
        user_business_identifier: str,
        report_style: str = "casual",
        max_competitors: int = 50,
        **kwargs
    ) -> ComparisonReport:
        """
        Create a complete business comparison report.

        Args:
            user_business_identifier: User's business name or identifier
            report_style: Style for report ('casual' or 'data-driven')
            max_competitors: Maximum number of competitors to find
            **kwargs: Additional parameters for customization

        Returns:
            ComparisonReport with analysis and recommendations

        Raises:
            BusinessDataError: If business data is invalid
            ValidationError: If input validation fails
        """
        logger.info(
            "comparison_started",
            user_business=user_business_identifier,
            max_competitors=max_competitors,
            report_style=report_style,
        )

        # Validate inputs
        self._validate_comparison_inputs(user_business_identifier)

        try:
            # Fetch and store user business profile
            user_business = self._fetch_business(
                user_business_identifier
            )

            # Automatically find competitors based on user business
            competitor_businesses = self._find_competitors(
                user_business, max_competitors
            )

            # Generate comparison analysis
            comparison_data = self._prepare_comparison_data(
                user_business, competitor_businesses
            )

            # Single LLM call for both analysis and suggestions
            llm_response = asyncio.run(self.llm_provider.generate_comparison_analysis(
                user_business_data=comparison_data["user_business"],
                competitor_data=comparison_data["competitors"],
                report_style=report_style,
            ))
            # For local development
            # llm_response = self.llm_provider.generate_comparison_analysis_test(
            #     user_business_data=comparison_data["user_business"],
            #     competitor_data=comparison_data["competitors"],
            #     report_style=report_style,
            # )

            # Create and save comparison report
            report = ComparisonReport(
                user_business=user_business.to_dict(),
                competitor_businesses=[c.to_dict() for c in competitor_businesses],
                ai_comparison_summary=llm_response.content,
                ai_improvement_suggestions=llm_response.suggestions,
                metadata={
                    "llm_provider": llm_response.provider,
                    "llm_model": llm_response.model,
                    "tokens_used": llm_response.tokens_used,
                    # "comparison_data": comparison_data,
                },
            )

            logger.info(
                "comparison_completed",
                report_id=str(report.id),
                user_business=user_business.name,
                competitor_count=len(competitor_businesses),
                tokens_used=llm_response.tokens_used,
            )

            return report

        except Exception as e:
            logger.error(
                "comparison_failed",
                user_business=user_business_identifier,
                error=str(e),
                error_type=type(e).__name__,
            )
            raise

    def _validate_comparison_inputs(self, user_business_identifier: str) -> None:
        """Validate comparison inputs."""
        if not user_business_identifier.strip():
            raise ValidationError("User business identifier is required")

    def _fetch_business(
        self, identifier: str
    ) -> BusinessProfileData:
        """
        Fetch business data and store/update in database.

        Args:
            identifier: Business identifier
            is_user_business: Whether this is the user's business

        Returns:
            BusinessProfile instance

        Raises:
            BusinessDataError: If business data cannot be fetched or is invalid
        """
        # Check if business already exists by name
        # existing_business = BusinessProfile.objects.filter(
        #     Q(name__iexact=identifier.strip()) |
        #     Q(website__iexact=identifier.strip())
        # ).first()

        try:
            # Fetch from external provider - run async method in sync context
            if self.data_provider.use_mock:
                business_profile = self.data_provider.fetch_business_from_mock_data(
                    identifier
                )
            else:
                business_profile: BusinessProfileData = asyncio.run(
                    self.data_provider.fetch_business_profile(identifier)
                )

            logger.info(
                "business_data_fetched",
                identifier=identifier,
                business_name=business_profile.name,
            )

            return business_profile

        except Exception as e:
            logger.error("business_fetch_failed", identifier=identifier, error=str(e))
            raise BusinessDataError(
                f"Could not fetch business data for '{identifier}': {str(e)}",
                business_name=identifier,
            )

    def _find_competitors(
        self, user_business: BusinessProfileData, max_competitors: int = 3
    ) -> List[BusinessProfileData]:
        """
        Automatically find competitors for the user's business.

        Args:
            user_business: User's business profile
            max_competitors: Maximum number of competitors to find

        Returns:
            List of competitor BusinessProfile instances
        """
        logger.info(
            "finding_competitors",
            business_name=user_business.name,
            business_category=user_business.category,
            max_competitors=max_competitors,
        )
        if self.data_provider.use_mock:
            mock_data = self.data_provider.get_mock_data()
            competitor_businesses = [
                self.data_provider.map_response_to_profile(c)
                for c in mock_data.get("places", [])
            ]
        else:
            competitor_businesses = asyncio.run(
                self.data_provider.search_competitors_data(
                    query=user_business.category, limit=max_competitors
                )
            )

        return competitor_businesses

        # Create search query based on business type or name
        # search_query = (
        #     user_business.type if user_business.type else user_business.name
        # )

        # # Extract location from address for better search results
        # location = None
        # if user_business.address:
        #     # Simple extraction - could be improved with proper address parsing
        #     address_parts = user_business.address.split(',')
        #     if len(address_parts) >= 2:
        #         # Assume last part is city/state
        #         location = address_parts[-1].strip()

        # try:
        #     # Search for similar businesses
        #     competitor_data_list = asyncio.run(
        #         self.data_provider.search_competitors_data(
        #             query=search_query,
        #             location=location,
        #             # Get extra to filter out user's business
        #             limit=max_competitors + 2
        #         )
        #     )

        #     competitor_businesses = []
        #     user_business_name_lower = user_business.name.lower()

        #     for competitor_data in competitor_data_list:
        #         # Skip if it's the same business as the user
        #         if competitor_data.name.lower() == user_business_name_lower:
        #             continue

        #         # Check if competitor already exists in database
        #         existing_competitor = BusinessProfile.objects.filter(
        #             Q(name__iexact=competitor_data.name.strip()) |
        #             Q(website__iexact=competitor_data.website.strip())
        #         ).first()

        #         if existing_competitor:
        #             competitor_businesses.append(existing_competitor)
        #         else:
        #             # Create new competitor profile
        #             competitor_profile = BusinessProfile.objects.create(
        #                 name=competitor_data.name,
        #                 website=competitor_data.website,
        #                 address=competitor_data.address,
        #                 latitude=competitor_data.latitude,
        #                 longitude=competitor_data.longitude,
        #                 rating=competitor_data.average_rating,
        #                 rating_count=competitor_data.review_count,
        #                 image_count=competitor_data.number_of_images,
        #                 has_hours=competitor_data.has_hours,
        #                 has_description=competitor_data.has_description,
        #                 has_menu_link=competitor_data.has_menu_link,
        #                 has_price_level=False
        #             )
        #             competitor_businesses.append(competitor_profile)

        #         # Stop when we have enough competitors
        #         if len(competitor_businesses) >= max_competitors:
        #             break

        #     logger.info(
        #         "competitors_found",
        #         business_name=user_business.name,
        #         competitor_count=len(competitor_businesses),
        #         competitor_names=[comp.name for comp in competitor_businesses]
        #     )

        #     return competitor_businesses

        # except Exception as e:
        #     logger.error(
        #         "competitor_search_failed",
        #         business_name=user_business.name,
        #         error=str(e)
        #     )
        #     # Return empty list if competitor search fails
        #     return []

    def _prepare_comparison_data(
        self,
        user_business: BusinessProfileData,
        competitor_businesses: List[BusinessProfileData],
    ) -> Dict[str, Any]:
        """
        Prepare structured data for LLM analysis.

        Args:
            user_business: User's business profile
            competitor_businesses: List of competitor profiles

        Returns:
            Structured comparison data
        """
        user_data = user_business.to_dict()

        competitor_data = [c.to_dict() for c in competitor_businesses]

        return {
            "user_business": user_data,
            "competitors": competitor_data,
            "comparison_metadata": {"competitor_count": len(competitor_businesses)},
        }
