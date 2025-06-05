"""
LLM provider abstractions and implementations.

This module implements the Provider Pattern for LLM services,
allowing easy switching between OpenAI, local models (Ollama), etc.
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI

from apps.common.exceptions import LLMServiceError
from apps.common.logging import get_logger

logger = get_logger(__name__)


@dataclass
class LLMResponse:
    """Data class for LLM response information."""

    content: str
    suggestions: List[str]
    tokens_used: int
    model: str
    provider: str
    metadata: Optional[Dict[str, Any]] = None


class OpenAIProvider:
    """OpenAI API implementation using modern async patterns."""

    def __init__(self, api_key: Optional[str] = None, model: str = "sonar"):
        self.api_key = api_key
        self.model = model
        self.provider_name = "perplexity"

        # Initialize async client with proper configuration
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            max_retries=3,
            timeout=30.0,
            base_url="https://api.perplexity.ai",
        )

    async def generate_comparison_analysis(
        self,
        user_business_data: Dict[str, Any],
        competitor_data: List[Dict[str, Any]],
        comparison_metrics: Dict[str, Any],
        report_style: str = "casual",
        **kwargs,
    ) -> LLMResponse:
        """Generate analysis with JSON response parsing."""
        try:
            system_prompt = self._build_system_prompt(report_style)
            user_prompt = self._build_comparison_prompt(
                user_business_data,
                competitor_data,
                comparison_metrics,
                report_style
            )

            response_format = self._get_response_format()

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=response_format,
                temperature=0.7,
                max_tokens=300,
            )

            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            # Parse JSON response
            try:
                result = json.loads(content)
                suggestions = result.get("suggestions", [])
                analysis_content = json.dumps(result.get("analysis", {}))

                if not suggestions:
                    logger.warning("no_suggestions_in_json", content=content[:100])
                    suggestions = self._generate_fallback_suggestions()

                return LLMResponse(
                    content=analysis_content,
                    suggestions=suggestions,
                    tokens_used=tokens_used,
                    model=self.model,
                    provider=self.provider_name,
                    metadata={"request_id": response._request_id, "format": "json"},
                )
            except json.JSONDecodeError as e:
                logger.warning(
                    "invalid_json_response", error=str(e), content=content[:100]
                )
                # Fallback to text parsing
                suggestions = self._generate_fallback_recommendations(
                    user_business_data, competitor_data)
                return LLMResponse(
                    content=content,
                    suggestions=suggestions,
                    tokens_used=tokens_used,
                    model=self.model,
                    provider=self.provider_name,
                    metadata={
                        "request_id": response._request_id,
                        "format": "text",
                        "warning": "failed_to_parse_json",
                    },
                )

        except Exception as e:
            logger.error(
                "llm_service_error",
                provider=self.provider_name,
                model=self.model,
                error=str(e),
                error_type=type(e).__name__,
            )
            raise LLMServiceError(self.provider_name, str(e))

    #########################################################
    # Build prompts and response format
    #########################################################

    def _build_system_prompt(self, report_style: str = "casual") -> str:
        """Build system prompt for JSON-formatted analysis."""

        style_instruction = (
            "Make analysis and suggestions data-driven " +
            "with specific metrics and percentages"
            if report_style == "data-driven"
            else "Make analysis and suggestions friendly and easy to understand"
        )

        return f"""
        You are an expert business analyst specializing in competitive analysis.
        Provide your analysis in strict JSON format with these required keys:
        {{
            "analysis": {{
                "overview": "competitive landscape summary",
                "strengths": ["list", "of", "strengths"],
                "weaknesses": ["list", "of", "weaknesses"],
                "competitive_position": "summary text"
            }},
            "suggestions": ["list", "of", "actionable", "suggestions"]
        }}

        Requirements:
        - {style_instruction}
        - Suggestions should be concise and direct, starting with phrases like:
            - 'You're missing...'
            - 'Consider...'
            - 'Your competitors average...'
        - Include exactly 3-5 suggestions.
        - Respond ONLY with valid JSON.
        - Do not include any text outside the JSON structure.
        """.strip()

    def _build_comparison_prompt(
        self,
        user_business_data: Dict[str, Any],
        competitor_data: List[Dict[str, Any]],
        comparison_metrics: Dict[str, Any],
        report_style: str = "casual",
    ) -> str:
        """Build prompt for JSON-formatted analysis."""

        style_note = (
            "Focus on metrics, percentages, and data-driven insights"
            if report_style == "data-driven"
            else "Use friendly, accessible language"
        )

        metrics_context = f"""
        Competitive Metrics Analysis:
        1. RATING:
        • Yours: {user_business_data.get('rating', 'N/A')}
        • Avg: {comparison_metrics.get('avg_competitor_rating', 'N/A')}
        • Top: {comparison_metrics.get('top_competitor_rating', 'N/A')}
        • Rank: {comparison_metrics.get('user_rating_rank', 'N/A')}/
        {comparison_metrics.get('total_businesses', 'N/A')}
        • Gap to top: {comparison_metrics.get('rating_gap', 0):.1f} points

        2. RATING COUNT:
        • Yours: {user_business_data.get('rating_count', 0)}
        • Avg: {comparison_metrics.get('avg_competitor_review_count', 0)}
        • Top: {comparison_metrics.get('top_review_count', 0)}
        • Needed to match avg: {comparison_metrics.get('review_gap_to_avg', 0)}

        3. IMAGES:
        • Yours: {user_business_data.get('image_count', 0)}
        • Avg: {comparison_metrics.get('avg_competitor_images', 0)}
        • Top: {comparison_metrics.get('top_image_count', 0)}
        • Needed to match avg: {comparison_metrics.get('image_gap_to_avg', 0)}
        """.strip()
        print(metrics_context)

        prompt = f"""
        {metrics_context}

        Analyze this competitive data and return JSON with:
        1. Analysis of competitive landscape.
        2. Key strengths/weaknesses (reference metrics where relevant).
        3. Competitive position assessment.
        4. 3-5 specific suggestions ({style_note}).

        Suggestions should be concise and direct, such as:
        - "Your rating is {comparison_metrics.get('rating_gap', 0)} points below the leader"
        - "Your rating count is {comparison_metrics.get('review_gap', 0)} below the leader"
        - "You're missing photos. Your competitors average {comparison_metrics.get('avg_competitor_images', 0)}+"
        - "You haven't responded to recent reviews, consider replying to stay relevant."

        Avoid bullet points in suggestions.

        Data:
        - My Business: {user_business_data}
        - Competitors: {competitor_data}

        Respond ONLY with valid JSON matching the specified format.
        Do not include any explanatory text outside the JSON.
        """.strip()

        return prompt

    def _get_response_format(self) -> Dict[str, Any]:
        """Response format for JSON-formatted analysis."""
        return {
            "type": "json_schema",
            "json_schema": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "analysis": {
                            "type": "object",
                            "properties": {
                                "overview": {"type": "string"},
                                "strengths": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "weaknesses": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "competitive_position": {"type": "string"}
                            },
                            "required": [
                                "overview",
                                "strengths",
                                "weaknesses",
                                "competitive_position"
                            ]
                        },
                        "suggestions": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["analysis", "suggestions"]
                }
            }
        }

    #########################################################
    # Fallback methods
    #########################################################

    def _genereate_fallback_response(
        self,
        user_business_data: Dict[str, Any],
        competitor_data: List[Dict[str, Any]]
    ) -> LLMResponse:
        """Generate mock JSON response for development."""
        import json

        user_name = user_business_data.get("name", "Your Business")
        competitor_count = len(competitor_data)

        mock_response = {
            "analysis": {
                "overview": f"{user_name} competes with " +
                f"{competitor_count} similar businesses in the area",
                "strengths": [
                    "Strong customer review ratings",
                    "Complete business profile information"
                ],
                "weaknesses": [
                    "Fewer reviews than competitors",
                    "Limited business photos"
                ],
                "competitive_position": "Middle-tier competitive position with room for improvement"
            },
            "suggestions": self._generate_fallback_recommendations(
                user_business_data, competitor_data)
        }

        return LLMResponse(
            content=json.dumps(mock_response["analysis"]),
            suggestions=mock_response["suggestions"],
            tokens_used=350,
            model=self.model,
            provider=self.provider_name,
            metadata={"mock": True, "format": "json"}
        )

    def _generate_fallback_recommendations(
        self, user_data: Dict[str, Any], competitor_data: List[Dict[str, Any]]
    ) -> str:
        """Generate specific recommendations."""
        recommendations = []

        # Review count analysis
        avg_competitor_reviews = sum(
            c.get("rating_count", 0) for c in competitor_data
        ) / max(len(competitor_data), 1)

        if user_data.get("rating_count", 0) < avg_competitor_reviews:
            recommendations.append(
                f"Increase review count - competitors average "
                f"{avg_competitor_reviews:.0f} reviews"
            )

        # Business info completeness
        if not user_data.get("has_hours", False):
            recommendations.append("Add business hours information")

        if not user_data.get("has_description", False):
            recommendations.append("Add a business description")

        if not user_data.get("has_menu_link", False):
            recommendations.append("Add menu link or information")

        return recommendations

    #########################################################
    # For local development
    #########################################################

    def generate_comparison_analysis_test(
        self,
        user_business_data: Dict[str, Any],
        competitor_data: List[Dict[str, Any]],
        comparison_metrics: Dict[str, Any],
        report_style: str = "casual",
        **kwargs
    ) -> LLMResponse:
        """Generate analysis with JSON response parsing."""
        response = {
            "user_business": {
                "name": "Restaurant Everest Katajanokka",
                "website": "http://everestnokka.fi/",
                "address": "Luotsikatu 12 A, 00160 Helsinki",
                "rating": 4.6,
                "rating_count": 980,
                "image_count": 12,
                "category": "Restaurant",
                "has_hours": True,
                "has_description": False,
                "has_menu_link": True,
                "has_price_level": True,
                "latitude": 60.1678712,
                "longitude": 24.966352399999998
            },
            "competitor_count": 20,
            "ai_comparison_summary": "{\"overview\": \"The competitive landscape in Helsinki is highly competitive with several restaurants achieving high ratings and customer reviews. Key factors influencing success include high-quality food, customer service, and a unique dining atmosphere.\", \"strengths\": [\"Highly rated with a strong customer base\", \"Presence of essential business features like menu links and price levels\", \"Located in a prime area with potential for local and tourist traffic\"], \"weaknesses\": [\"Lack of descriptive content on the website\", \"Potential for improving customer engagement through social media or additional services\"], \"competitive_position\": \"Restaurant Everest Katajanokka is well-positioned in the market with a strong rating and customer base, but it faces intense competition from other highly-rated establishments.\"}",
            "ai_improvement_suggestions": self._get_styled_suggestions_test(
                report_style
            ),
            "metadata": {
                "llm_provider": "perplexity",
                "llm_model": "sonar",
                "tokens_used": 2948
            }
        }
        return LLMResponse(
                    content=response["ai_comparison_summary"],
                    suggestions=response["ai_improvement_suggestions"],
                    tokens_used=response["metadata"]["tokens_used"],
                    model=self.model,
                    provider=self.provider_name,
                    metadata=response["metadata"],
                )

    def _get_styled_suggestions_test(self, suggestion_style: str) -> List[str]:
        """Get suggestions based on the selected style."""
        if suggestion_style == "data-driven":
            return [
                "Increase review count by 25% through targeted customer follow-up campaigns",
                "Benchmark against competitors averaging 4.8 rating to identify improvement areas",
                "Add business description to improve conversion rates by 15-20%",
                "Optimize for image count (current: 12, competitor average: 18) to boost engagement",
                "Implement pricing transparency to match 85% of successful competitors"
            ]
        else:  # casual style
            return [
                "Add a compelling business description to help customers understand what makes you special",
                "Engage with customers more to boost your review count and ratings",
                "Share more photos of your food and restaurant atmosphere online",
                "Make your hours and pricing clear so customers know what to expect",
                "Consider joining local restaurant events to increase your visibility"
            ]
