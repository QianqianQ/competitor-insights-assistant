# User Stories for Competitor Insights Assistant MVP

## 1. User Story: Identify Own Business

*   **As a** Restaurant Owner (USER),
*   **I want to** input my business name or website,
*   **so that** the system can fetch and identify my current online business profile data.
*   **Resources involved:**
    *   `BusinessProfile` (for user's business)
    *   External data source API (e.g., Serper.dev or mock)
*   **Operation:** CREATE (a `BusinessProfile` representation internally, or initiate data fetching), READ (from external API)
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   The system should provide feedback if the business cannot be uniquely identified (though for MVP, we might assume a single best match or require a very specific input).
    *   Input field should accept either a name or a valid URL.
    *   Profile is stored for comparison; user is not required to create an account in MVP

## 2. User Story: Identify Competitor Businesses

*   **As a** Restaurant Owner (USER),
*   **I want to** input the names or websites of one or more competitor businesses,
*   **so that** the system can fetch their online business profile data for comparison.
*   **Resources involved:**
    *   `BusinessProfile` (for competitor businesses)
    *   External data source API
*   **Operation:** CREATE (internal `BusinessProfile` representations), READ (from external API)
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   MVP might limit the number of competitors that can be entered (e.g., 1-3).
    *   System should handle multiple competitor inputs.
    *   Competitor data can be fetched from mock/external APIs.
    *   System should auto-suggest competitors but allow manual override.

## 3. User Story: Initiate Profile Comparison

*   **As a** Restaurant Owner (USER),
*   **I want to** trigger a comparison process after providing my business and competitor details,
*   **so that** the system can gather all necessary data and prepare a comparative analysis.
*   **Resources involved:**
    *   `BusinessProfile` (user's and competitors')
    *   `ProfileAttributes` (to be populated)
    *   `ComparisonReport` (to be created)
    *   External data source API
    *   LLM API
*   **Operation:** CREATE (`ComparisonReport`, `ProfileAttributes`), READ (data from `BusinessProfile` entities and external APIs), PROCESS (data comparison logic, LLM interaction)
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   The system should provide a loading/processing indicator as this may take a few seconds.
    *   Error handling for API failures during data fetching or LLM processing.
    *   MVP might not persist the comparison report, but should provide a way to view it.
    *   Comparisons are generated on demand and stored.

## 4. User Story: View Key Attribute Comparison

*   **As a** Restaurant Owner (USER),
*   **I want to** see a comparison of key attributes (like review count, average rating, number of images, presence of hours, description, menu links) between my business and my competitors,
*   **so that** I can quickly identify my profile's strengths and weaknesses relative to them.
*   **Resources involved:**
    *   `ComparisonReport` (containing aggregated/compared data derived from `ProfileAttributes`)
*   **Operation:** READ
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   The presentation should be clear and easy to understand (e.g., a simple table or side-by-side list).
    *   Backend will normalize fields for comparison (image count, reviews, etc.)

## 5. User Story: View AI-Generated Comparison Summary

*   **As a** Restaurant Owner (USER),
*   **I want to** read an AI-generated summary that highlights the main differences and overall standing of my profile compared to competitors,
*   **so that** I can get a quick, digestible overview of the competitive landscape.
*   **Resources involved:**
    *   `ComparisonReport` (specifically the `comparison_summary_llm` field)
*   **Operation:** READ
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   The summary should be concise and focus on actionable insights.
    *   Data should be returned in a structured and user-friendly format

## 6. User Story: Receive AI-Generated Improvement Suggestions

*   **As a** Restaurant Owner (USER),
*   **I want to** receive concrete, AI-generated suggestions on how to improve my business profile,
*   **so that** I have actionable steps to enhance my online visibility and attract more customers.
*   **Resources involved:**
    *   `ComparisonReport` (specifically the `improvement_suggestions_llm` field)
*   **Operation:** READ
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   Suggestions should be specific (e.g., "You're missing photos. Your competitors average 20+.").
    *   Suggestions should be relevant to the compared attributes.
    *   MVP could skip it.

## 7. User Story: (Optional MVP) View Past Comparison Reports

*   **As a** registered Restaurant Owner (USER),
*   **I want to** be able to see a list of my previously generated comparison reports,
*   **so that** I can track changes or refer back to insights without re-running the comparison.
*   **Resources involved:**
    *   `User` (for authentication)
    *   `ComparisonReport`
*   **Operation:** READ (list of user's reports)
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   Requires user authentication (JWT).
    *   MVP might only show a limited history or just the most recent report.
    *   `ComparisonReport` would need a `user_id` foreign key if this is implemented.

## 8. User Story: (Optional MVP) View Past Comparison Reports

*   **As a** registered Restaurant Owner (USER),
*   **I want to** be able to see a list of my previously generated comparison reports,
*   **so that** I can track changes or refer back to insights without re-running the comparison.
*   **Resources involved:**
    *   `User` (for authentication)
    *   `ComparisonReport`
*   **Operation:** READ (list of user's reports)
*   **User ROLE:** USER
*   **Additional considerations/constraints:**
    *   Requires user authentication (JWT).
    *   MVP might only show a limited history or just the most recent report.
    *   `ComparisonReport` would need a `user_id` foreign key if this is implemented.
