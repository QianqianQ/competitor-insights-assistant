# Coding Style Guide - Competitor Insights Assistant

## **Overview**

This guide establishes consistent coding standards for our Django + Vue 3 + TypeScript full-stack application. Following these guidelines ensures maintainable, readable, and scalable code across the entire team.

## **General Principles**

### **Consistency is King**
- Follow established patterns within each file and across the codebase
- Use existing conventions in the project before introducing new ones
- Separate style changes from logic changes in commits

### **Readability Above Efficiency**
- Write code that is self-documenting through clear naming and structure
- Prefer explicit over implicit code
- Choose clarity over cleverness

### **Type Safety First**
- Use type hints in Python and strict TypeScript settings
- Leverage Pydantic models for data validation
- Define clear interfaces and contracts

### **Fail Fast and Explicitly**
- Use proper error handling and validation
- Prefer early returns over deep nesting
- Make errors obvious and actionable

## **Python/Django Standards**

### **Imports and Structure**
```python
# Standard library
import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

# Third-party
import structlog
from django.db import models
from rest_framework import serializers

# Local imports
from .models import BusinessProfile
from .services import ComparisonService
```

### **Naming Conventions**
```python
# Classes: PascalCase
class ComparisonService:
    pass

# Functions/variables: snake_case
def create_comparison_report() -> ComparisonReport:
    user_business_data = fetch_business_profile()
    return user_business_data

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT_SECONDS = 30
MAX_COMPETITORS_COUNT = 5

# Private methods: leading underscore
def _validate_business_identifier(self, identifier: str) -> bool:
    pass
```

### **Type Hints and Documentation**
```python
from typing import Optional, List, Dict, Any

def fetch_business_profile(
    identifier: str,
    include_images: bool = True,
    timeout_seconds: int = 30
) -> Optional[BusinessProfileData]:
    """
    Fetch business profile data from external API.

    Args:
        identifier: Business name or website URL
        include_images: Whether to fetch image count data
        timeout_seconds: Request timeout duration

    Returns:
        BusinessProfileData if found, None otherwise

    Raises:
        ValidationError: If identifier format is invalid
        ExternalAPIError: If external service fails
    """
    pass
```

### **Error Handling**
```python
# Use specific exception types
class BusinessNotFoundError(Exception):
    """Raised when business cannot be found in external data source"""
    pass

# Log errors with context
logger = structlog.get_logger()

try:
    profile = await self.data_provider.fetch_business_profile(identifier)
except ExternalAPIError as e:
    logger.error(
        "external_api_failure",
        provider="serper",
        identifier=identifier,
        error=str(e)
    )
    raise BusinessNotFoundError(f"Could not fetch profile for {identifier}")
```

## **Vue 3/TypeScript Standards**

### **Component Structure**
```vue
<script setup lang="ts">
// Imports
import { ref, computed, onMounted } from 'vue'
import type { ComparisonReport, BusinessSearchResult } from '@/types'

// Props with interface
interface Props {
  report: ComparisonReport
  isLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false
})

// Emits
interface Emits {
  (e: 'comparison-created', report: ComparisonReport): void
  (e: 'error', message: string): void
}

const emit = defineEmits<Emits>()

// Reactive state
const searchQuery = ref<string>('')
const searchResults = ref<BusinessSearchResult[]>([])

// Computed properties
const hasResults = computed(() => searchResults.value.length > 0)

// Methods
const handleSearch = async (): Promise<void> => {
  // Implementation
}

// Lifecycle
onMounted(() => {
  // Setup logic
})
</script>

<template>
  <div class="business-search">
    <!-- Template content -->
  </div>
</template>

<style scoped>
/* Component-specific styles */
.business-search {
  @apply space-y-4 p-6;
}
</style>
```

### **TypeScript Interfaces and Types**
```typescript
// Use interfaces for object shapes
interface BusinessProfileData {
  name: string
  identifier_used: string
  review_count: number
  average_rating: number
  number_of_images: number
  has_hours: boolean
  has_description: boolean
  has_menu_link: boolean
  address?: string
  website_url?: string
}

// Use type unions for specific values
type DataSource = 'mock' | 'serper' | 'google'
type LLMProvider = 'openai' | 'ollama' | 'local-ai'

// Use generic types appropriately
interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
}
```

### **Composables Pattern**
```typescript
// useBusinessComparison.ts
import { ref, computed } from 'vue'
import type { ComparisonReport, CreateComparisonRequest } from '@/types'

export const useBusinessComparison = () => {
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const report = ref<ComparisonReport | null>(null)

  const hasReport = computed(() => report.value !== null)

  const createComparison = async (request: CreateComparisonRequest): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.comparisons.create(request)
      report.value = response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
    } finally {
      isLoading.value = false
    }
  }

  const clearComparison = (): void => {
    report.value = null
    error.value = null
  }

  return {
    // State
    isLoading: readonly(isLoading),
    error: readonly(error),
    report: readonly(report),

    // Computed
    hasReport,

    // Actions
    createComparison,
    clearComparison
  }
}
```

## **Styling Standards (Tailwind CSS)**

### **Class Organization**
```vue
<template>
  <!-- Layout → Display → Spacing → Sizing → Colors → Typography → Effects -->
  <div class="flex flex-col justify-center items-center gap-4 p-6 w-full max-w-2xl bg-white text-gray-900 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold text-center">Business Comparison</h2>

    <!-- Use semantic color classes -->
    <button class="btn-primary">
      Create Comparison
    </button>

    <!-- Responsive design -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Grid items -->
    </div>
  </div>
</template>

<style scoped>
/* Custom component classes using @apply */
.btn-primary {
  @apply px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors;
}
</style>
```

## **API and Data Handling**

### **API Client Structure**
```typescript
// api/client.ts
interface ApiClient {
  comparisons: {
    create(request: CreateComparisonRequest): Promise<ApiResponse<ComparisonReport>>
    get(id: string): Promise<ApiResponse<ComparisonReport>>
  }
  businesses: {
    search(query: string, location?: string): Promise<ApiResponse<BusinessSearchResult[]>>
  }
}

// Use consistent error handling
const handleApiError = (error: unknown): string => {
  if (error instanceof Response) {
    return `API Error: ${error.status} ${error.statusText}`
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'An unexpected error occurred'
}
```

### **Data Validation**
```python
# Use Pydantic for request/response validation
from pydantic import BaseModel, validator

class CreateComparisonRequest(BaseModel):
    user_business_identifier: str
    competitor_identifiers: List[str]

    @validator('user_business_identifier')
    def validate_user_business(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Business identifier must be at least 3 characters')
        return v.strip()

    @validator('competitor_identifiers')
    def validate_competitors(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one competitor is required')
        if len(v) > 5:
            raise ValueError('Maximum 5 competitors allowed')
        return [comp.strip() for comp in v if comp.strip()]
```

## **Testing Standards**

### **Python Tests**
```python
# test_comparison_service.py
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_data_provider():
    provider = Mock()
    provider.fetch_business_profile = AsyncMock()
    return provider

@pytest.fixture
def comparison_service(mock_data_provider, mock_llm_provider):
    return ComparisonService(
        data_provider=mock_data_provider,
        llm_provider=mock_llm_provider
    )

@pytest.mark.asyncio
async def test_create_comparison_success(comparison_service, mock_data_provider):
    # Arrange
    mock_data_provider.fetch_business_profile.return_value = BusinessProfileData(
        name="Test Restaurant",
        # ... other fields
    )

    # Act
    result = await comparison_service.create_comparison(
        user_business="test-restaurant",
        competitors=["competitor-1"]
    )

    # Assert
    assert result.user_business.name == "Test Restaurant"
    assert len(result.competitors) == 1
```

### **Vue Tests**
```typescript
// BusinessInputForm.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import BusinessInputForm from '@/components/BusinessInputForm.vue'

describe('BusinessInputForm', () => {
  it('validates required fields', async () => {
    const wrapper = mount(BusinessInputForm, {
      props: {
        onSubmit: vi.fn()
      }
    })

    const submitButton = wrapper.find('[data-testid="submit-button"]')
    await submitButton.trigger('click')

    expect(wrapper.find('.error-message').text()).toContain('Business name is required')
  })

  it('emits submit event with valid data', async () => {
    const mockSubmit = vi.fn()
    const wrapper = mount(BusinessInputForm, {
      props: {
        onSubmit: mockSubmit
      }
    })

    await wrapper.find('input[name="business"]').setValue('Test Restaurant')
    await wrapper.find('input[name="competitor"]').setValue('Competitor 1')
    await wrapper.find('form').trigger('submit')

    expect(mockSubmit).toHaveBeenCalledWith('Test Restaurant', ['Competitor 1'])
  })
})
```

## **Logging and Observability**

### **Structured Logging**
```python
import structlog

logger = structlog.get_logger()

# Good: Structured with context
logger.info(
    "comparison_created",
    user_business=user_business_id,
    competitor_count=len(competitors),
    processing_time_ms=processing_time,
    llm_provider=llm_provider_name
)

# Bad: Unstructured string formatting
logger.info(f"Created comparison for {user_business_id} with {len(competitors)} competitors")
```

### **Frontend Error Tracking**
```typescript
// utils/errorTracking.ts
interface ErrorContext {
  component?: string
  action?: string
  metadata?: Record<string, any>
}

const trackError = (error: Error, context: ErrorContext = {}): void => {
  console.error('Application Error:', {
    message: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString(),
    ...context
  })

  // In production, send to error tracking service
  if (process.env.NODE_ENV === 'production') {
    // Send to Sentry, LogRocket, etc.
  }
}
```

## **Security Guidelines**

### **Input Sanitization**
```python
from django.utils.html import escape
from urllib.parse import urlparse

def validate_business_url(url: str) -> bool:
    """Validate business website URL"""
    try:
        parsed = urlparse(url)
        return parsed.scheme in ['http', 'https'] and bool(parsed.netloc)
    except Exception:
        return False

# Always escape user input
business_name = escape(user_input.strip())
```

### **Environment Configuration**
```python
# settings.py
import os
from pathlib import Path

# Never commit secrets
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Use secure defaults
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
```

## **Performance Guidelines**

### **Database Optimization**
```python
# Use select_related for foreign keys
businesses = BusinessProfile.objects.select_related('user').filter(active=True)

# Use prefetch_related for many-to-many
reports = ComparisonReport.objects.prefetch_related('competitors').all()

# Add database indexes
class BusinessProfile(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'active']),
        ]
```

### **Frontend Performance**
```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

// Lazy load heavy components
const ComparisonChart = defineAsyncComponent(
  () => import('@/components/ComparisonChart.vue')
)

// Use computed for expensive operations
const expensiveCalculation = computed(() => {
  return heavyCalculation(props.data)
})
</script>
```

## **Git and Commit Guidelines**

### **Commit Message Format**
```
feat(api): add business search endpoint

- Implement search functionality for competitor discovery
- Add location-based filtering
- Include pagination support

Closes #123
```

### **Branch Naming**
- `feat/business-search-api` - New features
- `fix/comparison-error-handling` - Bug fixes
- `refactor/llm-provider-abstraction` - Code refactoring
- `docs/api-documentation` - Documentation updates

## **TODO and FIXME Comments**

### **TODO Format**
```python
# TODO(COMP-123): Add caching for business profile data when we implement Redis
# TODO: Implement rate limiting before production deployment
# TODO: Add input validation for competitor URLs when frontend adds URL support
```

### **FIXME Format**
```python
# FIXME: Remove hardcoded API key before merge
# FIXME: Handle empty competitor list error case
# FIXME: Add proper error message for LLM timeout
```

**Rationale**: TODOs document future improvements while FIXMEs mark issues that must be resolved before code submission.

---

This style guide is a living document. Update it as the project evolves and new patterns emerge.