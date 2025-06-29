"""
Data providers for fetching business profile information from external sources.

This module contains implementations for different business data providers,
including real APIs and mock implementations for development and testing.
"""

import json
import random
from pathlib import Path
from typing import List, Optional

from apps.businesses.models import BusinessProfileData
from apps.common.logging import get_logger

logger = get_logger(__name__)


class SerperBusinessDataProvider:
    """Serper.dev API implementation for business data retrieval."""

    def __init__(self, api_key: str, use_mock: bool = True):
        self.api_key = api_key
        self.provider_name = "serper"
        self.base_url = "https://google.serper.dev/places"  # maps / search
        # google_places = (
        #     "https://places.googleapis.com/v1/places:searchText"
        # )  # Text search
        self.use_mock = use_mock
        if use_mock:
            self._mock_data = self._load_mock_data()

    #########################################################
    # Helper methods
    #########################################################

    def map_response_to_profile(self, data: dict) -> BusinessProfileData:
        """Map API response directly to BusinessProfile model."""
        return BusinessProfileData(
            name=data.get("title", ""),
            address=data.get("address", ""),
            website=data.get("website", ""),
            rating_count=data.get("ratingCount", 0),
            rating=float(data.get("rating", 0.0)),
            image_count=random.randint(1, 20),
            category=data.get("type", ""),
            has_hours=bool(data.get("openingHours")),
            has_description=bool(data.get("description")),
            has_price_level=bool(data.get("priceLevel")),
            has_menu_link=bool(data.get("bookingLinks")),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )

    #########################################################
    # Mock data methods
    #########################################################

    def _load_mock_data(self) -> dict:
        """Load development data from JSON file."""
        try:
            current_dir = Path(__file__).parent
            data_path = current_dir / "mock_data.json"

            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Development data file not found")
            return {"places": []}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse data file: {e}")
            return {"places": []}

    def get_mock_data(self) -> dict:
        """Get mock data."""
        return self._mock_data

    def fetch_business_from_mock_data(self, identifier: str) -> BusinessProfileData:
        """Fetch from mock data."""
        identifier_lower = identifier.lower().strip()
        is_website = identifier_lower.startswith(("http://", "https://", "www."))

        for place in self._mock_data.get("places", []):

            # Website match (if identifier is a URL)
            if is_website and identifier_lower in place.get("website", "").lower():
                return self.map_response_to_profile(place)

            # Name match (if identifier is not a URL)
            if not is_website:
                # Exact name match
                if place.get("title", "").lower() == identifier_lower:
                    return self.map_response_to_profile(place)

                # Partial name match
                if identifier_lower in place.get("title", "").lower():
                    return self.map_response_to_profile(place)

        logger.warning("business_not_found", identifier=identifier)

        # Return fallback profile if business is not found
        return BusinessProfileData(
            name=identifier if not is_website else "Your Business",
            rating_count=random.randint(10, 1000),
            rating=round(random.uniform(3.5, 4.8), 1),
            image_count=random.randint(1, 100),
            has_hours=random.choice([True, False]),
            has_description=random.choice([True, False]),
            has_menu_link=random.choice([True, False]),
            has_price_level=random.choice([True, False]),
            category=random.choice(["Restaurant", "Bar", "Cafe"]),
            website=identifier if is_website
            else f"https://{identifier.lower().strip()}.com",
            address="Finland" if is_website
            else f"{identifier.lower().strip()}, Finland",
            latitude=random.uniform(59.9, 60.1),
            longitude=random.uniform(24.9, 25.1),
        )

    def search_competitors_from_mock_data(
        self, query: str, limit: int
    ) -> List[BusinessProfileData]:
        """Search in mock data."""
        query_lower = query.lower().strip()

        if not query_lower:
            return [
                self.map_response_to_profile(place)
                for place in self._mock_data.get("places", [])
            ]

        results = []
        for place in self._mock_data.get("places", []):
            title = place.get("title", "").lower()
            description = place.get("description", "").lower()
            category = place.get("type", "").lower()

            if (
                query_lower in title
                or query_lower in description
                or query_lower in category
            ):

                business_data = self.map_response_to_profile(place)
                results.append(business_data)

                if len(results) >= limit:
                    break

        return results

    #########################################################
    # Real data methods
    #########################################################

    async def fetch_business_profile(self, identifier: str) -> BusinessProfileData:
        """
        Fetch business data from Serper API or development data
        given identifier (name or website).

        Args:
            identifier: Business name or website URL

        Returns:
            BusinessProfileData instance
        """
        logger.info(
            "serper_fetch_business",
            identifier=identifier,
            provider=self.provider_name,
            mode="development" if self.use_mock else "production",
        )

        return await self._fetch_business(identifier)

    async def search_competitors_data(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        limit: int = 10,
    ) -> List[BusinessProfileData]:
        """Search for businesses using Serper API or development data."""
        logger.info(
            "serper_search",
            query=query,
            location=location,
            limit=limit,
            mode="development" if self.use_mock else "production",
        )

        return await self._search_competitors(query, location, limit)

    async def _fetch_business(self, identifier: str) -> BusinessProfileData:
        """
        Fetch from externnal API
        (Serper.dev / Google Places API /
        LangChain GoogleSerperAPIWrapper for Google Places).
        # TODO: Solution for search via website URL
        """
        # For name
        # headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}

        # payload = {
        #     "q": identifier,
        #     "location": "Helsinki, Finland",
        #     "gl": "fi",
        #     "hl": "en"
        # }

        # response = requests.post(self.base_url, headers=headers, json=payload)
        # data = response.json()

        # return self.map_response_to_profile(data["places"][0])

        # For website, text-based search -> Place ID -> Place Details
        # may be a solution

        raise NotImplementedError("Real API search integration pending")

    async def _search_competitors(
        self, query: str, location: Optional[str], limit: int
    ) -> List[BusinessProfileData]:
        """
        Search using real Serper API.
        TODO: Implement actual API integration
        """
        # Google Places API search / LangChain GoogleSerperAPIWrapper
        # may be good option for search competitors

        # search_query = f"{query} {location}" if location else query

        # payload = {"q": search_query, "gl": "us", "hl": "en", "num": limit}

        # headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}

        # async with httpx.AsyncClient() as client:
        #     response = await client.post(self.base_url,headers=headers, json=payload)
        #     data = response.json()

        #     return [self.map_response_to_profile(place) for place in data.get("places", [])]

        raise NotImplementedError("Real API search integration pending")
