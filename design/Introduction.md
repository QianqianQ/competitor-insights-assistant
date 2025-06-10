# Introduction

### Walk me through the overall architecture of your application

    The application follows a clean architecture pattern with clear separation of concerns:

    Frontend: Vue 3 SPA with TypeScript, using Pinia for state management and Tailwind for styling

    Backend: Django REST API implementing a service layer pattern (Privoder parttern is todo)

    Data Layer: Django ORM with models for BusinessProfile and ComparisonReport. Now dataclass is used for simplicity in this stage.

    External Integrations: Provider pattern for LLM (Perplexity AI) and data sources (mock Serper.dev structure)


### How does your AI comparison analysis work

    A: "The AI analysis follows a structured approach:

    Data Preparation: Calculate comparative metrics (ratings, review counts, image counts)

    Prompt Engineering: Build context-aware prompts with business data and competitive metrics

    Structured Output: Use JSON schema to ensure consistent LLM responses

    Fallback Handling: Graceful degradation if JSON parsing fails

### How did you handle async operations in Django