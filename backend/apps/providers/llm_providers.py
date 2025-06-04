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
        **kwargs,
    ) -> LLMResponse:
        """Generate analysis with JSON response parsing."""
        try:
            # Real OpenAI API implementation
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_comparison_prompt(
                user_business_data, competitor_data
            )

            response_format = {
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

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                response_format=response_format,
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

    def _build_system_prompt(self) -> str:
        """Build system prompt for JSON-formatted analysis."""
        return """
        You are an expert business analyst specializing in competitive analysis.
        Provide your analysis in strict JSON format with these required keys:
        {
            "analysis": {
                "overview": "competitive landscape summary",
                "strengths": ["list", "of", "strengths"],
                "weaknesses": ["list", "of", "weaknesses"],
                "competitive_position": "summary text"
            },
            "suggestions": ["list", "of", "actionable", "suggestions"]
        }

        Requirements:
        - Respond ONLY with valid JSON.
        Ensure the output is valid JSON with all strings terminated and objects closed.
        - Include exactly 3-5 suggestions
        - Keep analysis data-driven and specific
        - Do not include any text outside the JSON structure
        """.strip()

    def _build_comparison_prompt(
        self, user_business_data: Dict[str, Any], competitor_data: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for JSON-formatted analysis."""

        prompt = f"""
        Analyze this competitive data and return JSON with:
        1. Analysis of competitive landscape
        2. Key strengths/weaknesses
        3. Competitive position assessment
        4. 3-5 specific suggestions

        Data:
        - Your Business: {user_business_data}
        - Competitors: {competitor_data}

        Respond ONLY with valid JSON matching the specified format.
        Do not include any explanatory text outside the JSON.
        """.strip()

        return prompt

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
                f"• Increase review count - competitors average "
                f"{avg_competitor_reviews:.0f} reviews"
            )

        # Business info completeness
        if not user_data.get("has_hours", False):
            recommendations.append("• Add business hours information")

        if not user_data.get("has_description", False):
            recommendations.append("• Add a business description")

        if not user_data.get("has_menu_link", False):
            recommendations.append("• Add menu link or information")

        return recommendations

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
                "overview": f"{user_name} competes with {competitor_count} similar businesses in the area",
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
