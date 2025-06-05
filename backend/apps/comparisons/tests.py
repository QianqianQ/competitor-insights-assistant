"""
Tests for comparison functionality.

This module implements comprehensive tests for the comparison service
and API endpoints using pytest-django best practices.
"""

from decimal import Decimal
from unittest.mock import AsyncMock, Mock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.businesses.models import BusinessProfile
from apps.common.exceptions import BusinessDataError, LLMServiceError
from apps.comparisons.models import ComparisonReport
from apps.comparisons.services import ComparisonService
from apps.providers.llm_providers import LLMResponse


@pytest.fixture
def api_client():
    """Provide API client for testing."""
    return APIClient()


@pytest.fixture
def sample_business_data():
    """Provide sample business data for testing."""
    return {
        "name": "Mario's Restaurant",
        "address": "123 Main St, Test City, TC 12345",
        "website": "https://marios-restaurant.com",
        "phone": "(555) 123-4567",
        "data_source": "mock",
        "external_id": "mario_001",
    }


@pytest.fixture
def sample_attributes_data():
    """Provide sample business attributes data for testing."""
    return {
        "review_count": 125,
        "average_rating": Decimal("4.5"),
        "number_of_images": 15,
        "has_hours": True,
        "has_description": True,
        "has_menu_link": True,
        "response_rate": Decimal("85.0"),
    }


@pytest.fixture
def business_profile(db, sample_business_data):
    """Create a test business profile."""
    return BusinessProfile.objects.create(**sample_business_data)


@pytest.fixture
def business_with_attributes(db, business_profile, sample_attributes_data):
    """Create a business profile with attributes."""
    ProfileAttributes.objects.create(
        business=business_profile, **sample_attributes_data
    )
    return business_profile


@pytest.fixture
def competitor_businesses(db):
    """Create competitor business profiles for testing."""
    competitors = []

    # Luigi's Pizza
    luigi = BusinessProfile.objects.create(
        name="Luigi's Pizza",
        address="456 Oak Ave, Test City, TC 12346",
        data_source="mock",
        external_id="luigi_001",
    )
    ProfileAttributes.objects.create(
        business=luigi,
        review_count=89,
        average_rating=Decimal("4.2"),
        number_of_images=12,
        has_hours=True,
        has_description=True,
        has_menu_link=False,
        response_rate=Decimal("75.0"),
    )
    competitors.append(luigi)

    # Tony's Kitchen
    tony = BusinessProfile.objects.create(
        name="Tony's Kitchen",
        address="789 Pine St, Test City, TC 12347",
        data_source="mock",
        external_id="tony_001",
    )
    ProfileAttributes.objects.create(
        business=tony,
        review_count=156,
        average_rating=Decimal("4.7"),
        number_of_images=20,
        has_hours=True,
        has_description=False,
        has_menu_link=True,
        response_rate=Decimal("90.0"),
    )
    competitors.append(tony)

    return competitors


@pytest.fixture
def comparison_report(db, business_with_attributes, competitor_businesses):
    """Create a sample comparison report."""
    report = ComparisonReport.objects.create(
        user_business=business_with_attributes,
        analysis_text="Mock analysis text",
        suggestions=["Suggestion 1", "Suggestion 2"],
        metadata={"llm_provider": "openai", "model": "gpt-4o-mini", "tokens_used": 450},
    )
    report.competitors.set(competitor_businesses)
    return report


@pytest.fixture
def mock_llm_response():
    """Provide mock LLM response for testing."""
    return LLMResponse(
        content="Mock analysis content",
        tokens_used=450,
        model="gpt-4o-mini",
        provider="openai",
        metadata={"mock": True},
    )


class TestBusinessProfileModel:
    """Test cases for BusinessProfile model."""

    def test_business_profile_creation(self, db, sample_business_data):
        """Test creating a business profile."""
        business = BusinessProfile.objects.create(**sample_business_data)

        assert business.name == sample_business_data["name"]
        assert business.data_source == sample_business_data["data_source"]
        assert business.external_id == sample_business_data["external_id"]
        assert str(business) == f"{business.name} ({business.data_source})"

    def test_business_profile_to_dict(self, business_profile):
        """Test business profile serialization."""
        data = business_profile.to_dict()

        assert data["name"] == business_profile.name
        assert data["data_source"] == business_profile.data_source
        assert "created_at" in data
        assert "updated_at" in data

    def test_needs_refresh_new_business(self, business_profile):
        """Test that new business needs refresh."""
        assert business_profile.needs_refresh()

    def test_mark_refreshed(self, business_profile):
        """Test marking business as refreshed."""
        business_profile.mark_refreshed()
        assert not business_profile.needs_refresh(hours=1)

    @pytest.mark.django_db
    def test_get_or_create_from_external(self, sample_business_data):
        """Test get_or_create_from_external method."""
        business, created = BusinessProfile.get_or_create_from_external(
            name=sample_business_data["name"],
            data_source=sample_business_data["data_source"],
            external_id=sample_business_data["external_id"],
        )

        assert created
        assert business.name == sample_business_data["name"]

        # Test get existing
        business2, created2 = BusinessProfile.get_or_create_from_external(
            name=sample_business_data["name"],
            data_source=sample_business_data["data_source"],
            external_id=sample_business_data["external_id"],
        )

        assert not created2
        assert business.pk == business2.pk


class TestProfileAttributesModel:
    """Test cases for ProfileAttributes model."""

    def test_profile_attributes_creation(
        self, business_profile, sample_attributes_data
    ):
        """Test creating profile attributes."""
        attributes = ProfileAttributes.objects.create(
            business=business_profile, **sample_attributes_data
        )

        assert attributes.business == business_profile
        assert attributes.review_count == sample_attributes_data["review_count"]
        assert attributes.average_rating == sample_attributes_data["average_rating"]

    def test_completeness_score(self, business_with_attributes):
        """Test completeness score calculation."""
        score = business_with_attributes.attributes.completeness_score()

        # Base score: 3/3 = 1.0, bonus: +0.1 reviews, +0.1 images = 1.0 (capped)
        assert score == 1.0

    def test_engagement_score(self, business_with_attributes):
        """Test engagement score calculation."""
        score = business_with_attributes.attributes.engagement_score()

        # Should be a float between 0 and 1
        assert 0.0 <= score <= 1.0
        assert isinstance(score, float)

    def test_to_dict(self, business_with_attributes):
        """Test attributes serialization."""
        data = business_with_attributes.attributes.to_dict()

        assert data["business_id"] == business_with_attributes.pk
        assert "review_count" in data
        assert "average_rating" in data
        assert "created_at" in data

    @pytest.mark.django_db
    def test_create_from_data(self, business_profile, sample_attributes_data):
        """Test create_from_data class method."""
        attributes = ProfileAttributes.create_from_data(
            business=business_profile, data=sample_attributes_data
        )

        assert attributes.business == business_profile
        assert attributes.review_count == sample_attributes_data["review_count"]


class TestComparisonService:
    """Test cases for ComparisonService."""

    @pytest.mark.asyncio
    async def test_create_comparison_success(
        self, db, mock_llm_response, business_with_attributes, competitor_businesses
    ):
        """Test successful comparison creation."""
        service = ComparisonService()

        with patch.object(
            service.data_provider, "get_business_data", new_callable=AsyncMock
        ) as mock_get_data:
            with patch.object(
                service.llm_provider,
                "generate_comparison_analysis",
                new_callable=AsyncMock,
                return_value=mock_llm_response,
            ) as mock_llm:

                # Setup mock data provider responses
                mock_get_data.side_effect = [
                    {
                        "name": business_with_attributes.name,
                        "review_count": 125,
                        "average_rating": 4.5,
                        "number_of_images": 15,
                        "has_hours": True,
                        "has_description": True,
                        "has_menu_link": True,
                    },
                    {
                        "name": competitor_businesses[0].name,
                        "review_count": 89,
                        "average_rating": 4.2,
                        "number_of_images": 12,
                        "has_hours": True,
                        "has_description": True,
                        "has_menu_link": False,
                    },
                ]

                report = await service.create_comparison(
                    user_business_name=business_with_attributes.name,
                    competitor_names=[competitor_businesses[0].name],
                )

                assert report is not None
                assert report.user_business.name == business_with_attributes.name
                assert report.competitors.count() == 1
                assert mock_llm.called

    def test_create_comparison_business_not_found(self):
        """Test comparison creation with non-existent business."""
        service = ComparisonService()

        with patch.object(
            service.data_provider,
            "get_business_data",
            new_callable=AsyncMock,
            side_effect=BusinessDataError("Business not found"),
        ):
            with pytest.raises(BusinessDataError):
                # Run async function in sync context for testing
                import asyncio

                asyncio.run(
                    service.create_comparison(
                        user_business_name="Non-existent Business",
                        competitor_names=["Another Non-existent"],
                    )
                )

    @pytest.mark.asyncio
    async def test_regenerate_analysis(self, comparison_report, mock_llm_response):
        """Test regenerating analysis for existing comparison."""
        service = ComparisonService()

        with patch.object(
            service.llm_provider,
            "generate_comparison_analysis",
            new_callable=AsyncMock,
            return_value=mock_llm_response,
        ) as mock_llm:

            updated_report = await service.regenerate_analysis(comparison_report)

            assert updated_report.pk == comparison_report.pk
            assert mock_llm.called


class TestComparisonAPI:
    """Test cases for comparison API endpoints."""

    def test_create_comparison_success(
        self, api_client, business_with_attributes, competitor_businesses
    ):
        """Test successful comparison creation via API."""
        url = reverse("comparison-list")
        data = {
            "user_business_name": business_with_attributes.name,
            "competitor_names": [comp.name for comp in competitor_businesses],
        }

        with patch(
            "apps.comparisons.services.ComparisonService.create_comparison"
        ) as mock_create:
            mock_create.return_value = ComparisonReport(
                id="test-id",
                user_business=business_with_attributes,
                analysis_text="Mock analysis",
                suggestions=["Suggestion 1"],
                metadata={},
            )

            response = api_client.post(url, data, format="json")

            assert response.status_code == status.HTTP_201_CREATED
            assert "analysis_text" in response.data

    def test_create_comparison_invalid_data(self, api_client):
        """Test comparison creation with invalid data."""
        url = reverse("comparison-list")
        data = {
            "user_business_name": "",  # Invalid empty name
            "competitor_names": [],  # Invalid empty list
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data or "errors" in response.data

    def test_get_comparison_success(self, api_client, comparison_report):
        """Test retrieving existing comparison."""
        url = reverse("comparison-detail", kwargs={"pk": comparison_report.pk})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(comparison_report.id)
        assert response.data["analysis_text"] == comparison_report.analysis_text

    def test_get_comparison_not_found(self, api_client):
        """Test retrieving non-existent comparison."""
        url = reverse("comparison-detail", kwargs={"pk": "non-existent-id"})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    def test_list_comparisons(self, api_client, comparison_report):
        """Test listing comparisons with pagination."""
        url = reverse("comparison-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data or len(response.data) > 0

    def test_search_businesses(self, api_client, business_with_attributes):
        """Test business search endpoint."""
        url = reverse("comparison-search-businesses")

        response = api_client.get(url, {"q": business_with_attributes.name})

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert response.data["count"] >= 1

    def test_regenerate_analysis(self, api_client, comparison_report):
        """Test regenerating analysis for existing comparison."""
        url = reverse(
            "comparison-regenerate-analysis", kwargs={"pk": comparison_report.pk}
        )

        with patch(
            "apps.comparisons.services.ComparisonService.regenerate_analysis"
        ) as mock_regen:
            mock_regen.return_value = comparison_report

            response = api_client.post(url)

            assert response.status_code == status.HTTP_200_OK
            assert mock_regen.called


class TestBusinessProfileAPI:
    """Test cases for business profile API endpoints."""

    def test_list_business_profiles(self, api_client, business_with_attributes):
        """Test listing business profiles."""
        url = reverse("businessprofile-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data or len(response.data) > 0

    def test_get_business_profile(self, api_client, business_with_attributes):
        """Test retrieving specific business profile."""
        url = reverse(
            "businessprofile-detail", kwargs={"pk": business_with_attributes.pk}
        )

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == business_with_attributes.name
        assert response.data["data_source"] == business_with_attributes.data_source


@pytest.mark.django_db
class TestIntegration:
    """Integration tests combining multiple components."""

    def test_end_to_end_comparison_flow(
        self, api_client, sample_business_data, sample_attributes_data
    ):
        """Test complete comparison flow from API to database."""
        # Create test businesses
        user_business = BusinessProfile.objects.create(**sample_business_data)
        ProfileAttributes.objects.create(
            business=user_business, **sample_attributes_data
        )

        competitor_data = sample_business_data.copy()
        competitor_data.update(
            {"name": "Competitor Restaurant", "external_id": "competitor_001"}
        )
        competitor = BusinessProfile.objects.create(**competitor_data)

        competitor_attrs = sample_attributes_data.copy()
        competitor_attrs.update({"review_count": 200})
        ProfileAttributes.objects.create(business=competitor, **competitor_attrs)

        # Test comparison creation
        url = reverse("comparison-list")
        data = {
            "user_business_name": user_business.name,
            "competitor_names": [competitor.name],
        }

        with patch(
            "apps.comparisons.services.ComparisonService.create_comparison"
        ) as mock_create:
            mock_report = ComparisonReport(
                id="integration-test",
                user_business=user_business,
                analysis_text="Integration test analysis",
                suggestions=["Test suggestion"],
                metadata={"test": True},
            )
            mock_create.return_value = mock_report

            response = api_client.post(url, data, format="json")

            assert response.status_code == status.HTTP_201_CREATED
            assert mock_create.called

            # Verify the service was called with correct parameters
            call_args = mock_create.call_args
            assert call_args.kwargs["user_business_name"] == user_business.name
            assert competitor.name in call_args.kwargs["competitor_names"]
