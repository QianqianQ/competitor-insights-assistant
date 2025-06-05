"""
Django REST Framework views for comparison operations.

This module implements ViewSets and API views following DRF best practices
with proper error handling, permissions, and async support.
"""

from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.logging import get_logger
from apps.comparisons.serializers import (
    ComparisonReportSerializer,
    ComparisonRequestSerializer,
)
from apps.comparisons.services import ComparisonService

logger = get_logger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination configuration for API responses."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ComparisonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing business comparisons.

    Provides CRUD operations for comparison reports with
    custom actions for business search and analysis.
    """

    serializer_class = ComparisonReportSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]  # TODO: Update for auth

    # def get_queryset(self):
    #     """Return queryset with optimized queries."""
    #     return ComparisonReport.objects.select_related(
    #         "user_business",
    #         "user_business__attributes"
    #     ).prefetch_related(
    #         "competitors",
    #         "competitors__attributes"
    #     ).order_by("-created_at")

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "create":
            return ComparisonRequestSerializer
        return ComparisonReportSerializer

    def create(self, request: Request) -> Response:
        """
        Create a new business comparison.

        Validates input, fetches business data, runs comparison analysis,
        and returns the generated report.
        """
        try:
            # Validate request data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user_business_identifier = serializer.validated_data[
                "user_business_identifier"
            ]
            report_style = serializer.validated_data.get(
                "report_style", "casual"
            )

            logger.info(
                "comparison_creation_started",
                user_business_identifier=user_business_identifier,
                report_style=report_style,
            )

            # Initialize comparison service
            comparison_service = ComparisonService()

            # Create comparison report
            report = comparison_service.create_comparison(
                user_business_identifier=user_business_identifier,
                report_style=report_style,
            )

            logger.info(
                "comparison_creation_completed",
                user_business=report.user_business,
                analysis_length=len(report.ai_comparison_summary),
                suggestions_count=len(report.ai_improvement_suggestions),
            )

            # Serialize response
            response_serializer = ComparisonReportSerializer(report)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception(
                "comparison_unexpected_error",
                error=str(e),
                error_type=type(e).__name__,
            )
            return Response(
                {"error": "Unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # @action(
    #     detail=False,
    #     methods=["get"],
    #     url_path="businesses/search",
    #     serializer_class=BusinessSearchRequestSerializer
    # )

    # def search_businesses(self, request: Request) -> Response:
    #     """
    #     Search for businesses by name or identifier.

    #     This endpoint allows users to search for and preview
    #     business information before creating comparisons.
    #     """
    #     try:
    #         # Validate query parameters
    #         serializer = BusinessSearchRequestSerializer(
    #             data=request.query_params)
    #         serializer.is_valid(raise_exception=True)

    #         query = serializer.validated_data["q"]
    #         limit = serializer.validated_data.get("limit", 10)

    #         logger.info(
    #             "business_search_started",
    #             query=query,
    #             limit=limit
    #         )

    #         # Search existing businesses first
    #         existing_businesses = BusinessProfile.objects.filter(
    #             name__icontains=query
    #         ).select_related("attributes")[:limit]

    #         results = []
    #         for business in existing_businesses:
    #             business_data = business.to_dict()
    #             if hasattr(business, "attributes"):
    #                 business_data.update(business.attributes.to_dict())
    #             results.append(business_data)

    #         # If we have fewer results than requested, could fetch from
    #         # external APIs to supplement (implement later)
    #         if len(results) < limit:
    #             logger.info(
    #                 "business_search_could_fetch_external",
    #                 existing_count=len(results),
    #                 requested_limit=limit
    #             )
    #             # TODO: Fetch additional results from external APIs

    #         logger.info(
    #             "business_search_completed",
    #             query=query,
    #             results_count=len(results)
    #         )

    #         return Response({
    #             "query": query,
    #             "count": len(results),
    #             "results": results
    #         })

    #     except Exception as e:
    #         logger.exception(
    #             "business_search_error",
    #             query=request.query_params.get("q", ""),
    #             error=str(e)
    #         )
    #         return Response(
    #             {"error": "Search failed", "detail": str(e)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )
