# Writing Good Interfaces - Competitor Insights Assistant

## **Overview**

This guide outlines principles for designing clean, intuitive, and maintainable interfaces in our full-stack application. It covers API design, UI/UX patterns, and component interfaces.

## **API Interface Design**

### **RESTful Principles**

#### **Resource-Oriented URLs**
```python
# Good: Resource-oriented, clear hierarchy
POST /api/v1/comparisons              # Create comparison
GET  /api/v1/comparisons/{id}         # Get specific comparison
GET  /api/v1/businesses/search        # Search businesses

# Bad: Action-oriented, unclear purpose
POST /api/v1/create-comparison
GET  /api/v1/get-comparison-by-id
POST /api/v1/search-for-businesses
```

#### **HTTP Methods and Status Codes**
```python
# Use appropriate HTTP methods
GET    # Retrieve data (idempotent)
POST   # Create resources or actions
PUT    # Update/replace entire resource
PATCH  # Partial updates
DELETE # Remove resources

# Return meaningful status codes
200    # OK - Successful GET, PATCH
201    # Created - Successful POST
400    # Bad Request - Validation errors
401    # Unauthorized - Authentication required
404    # Not Found - Resource doesn't exist
422    # Unprocessable Entity - Business logic errors
500    # Internal Server Error - Unexpected errors
```

### **Request/Response Structure**

#### **Consistent Request Format**
```python
# POST /api/v1/comparisons
{
  "user_business_identifier": "mario-restaurant.com",
  "competitor_identifiers": [
    "luigi-pizzeria.com",
    "Tony's Italian Kitchen"
  ],
  "options": {
    "mock_data": false,
    "include_detailed_analysis": true
  }
}
```

#### **Standardized Response Format**
```python
# Success Response (201 Created)
{
  "report_id": "comp_rpt_xyz123",
  "user_business": {
    "name": "Mario's Restaurant",
    "identifier_used": "mario-restaurant.com",
    "attributes": {
      "review_count": 150,
      "average_rating": 4.5,
      "number_of_images": 25,
      "has_hours": true,
      "has_description": true,
      "has_menu_link": true
    },
    "profile_data_source": "serper"
  },
  "competitors": [...],
  "ai_comparison_summary": "Your restaurant shows strong ratings...",
  "ai_improvement_suggestions": [
    "Add at least 10 more photos to your profile.",
    "Consider responding to recent reviews to increase engagement."
  ],
  "created_at": "2023-10-27T10:30:00Z"
}

# Error Response (400 Bad Request)
{
  "error": {
    "type": "ValidationError",
    "message": "Invalid business identifier format",
    "details": {
      "field": "user_business_identifier",
      "reason": "Must be a valid website URL or business name (min 3 characters)"
    }
  }
}
```

### **Input Validation and Error Handling**

#### **Comprehensive Validation**
```python
from pydantic import BaseModel, validator
from typing import List, Optional

class CreateComparisonRequest(BaseModel):
    user_business_identifier: str
    competitor_identifiers: List[str]
    options: Optional[ComparisonOptions] = None

    @validator('user_business_identifier')
    def validate_user_business(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Business identifier must be at least 3 characters')
        return v.strip()

    @validator('competitor_identifiers')
    def validate_competitors(cls, v):
        if not v:
            raise ValueError('At least one competitor is required')
        if len(v) > 5:
            raise ValueError('Maximum 5 competitors allowed')
        cleaned = [comp.strip() for comp in v if comp.strip()]
        if not cleaned:
            raise ValueError('At least one valid competitor is required')
        return cleaned

class ComparisonOptions(BaseModel):
    mock_data: bool = False
    include_detailed_analysis: bool = True
```

#### **Graceful Error Responses**
```python
# Custom exception handling
class APIError(Exception):
    def __init__(self, message: str, error_type: str = "APIError", status_code: int = 400):
        self.message = message
        self.error_type = error_type
        self.status_code = status_code

class BusinessNotFoundError(APIError):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"Business '{identifier}' could not be found",
            error_type="BusinessNotFoundError",
            status_code=404
        )

# Error handling in views
try:
    comparison = await comparison_service.create_comparison(request_data)
    return Response(comparison.dict(), status=201)
except ValidationError as e:
    return Response({
        "error": {
            "type": "ValidationError",
            "message": str(e),
            "details": e.errors() if hasattr(e, 'errors') else None
        }
    }, status=400)
except BusinessNotFoundError as e:
    return Response({
        "error": {
            "type": e.error_type,
            "message": e.message
        }
    }, status=e.status_code)
```

## **Frontend Component Interface Design**

### **Props and Events Pattern**

#### **Clear Props Interface**
```typescript
// BusinessInputForm.vue
interface Props {
  // Required props
  onSubmit: (userBusiness: string, competitors: string[]) => void

  // Optional props with defaults
  isLoading?: boolean
  maxCompetitors?: number
  allowUrlInput?: boolean

  // Initial values for form restoration
  initialUserBusiness?: string
  initialCompetitors?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
  maxCompetitors: 5,
  allowUrlInput: true,
  initialUserBusiness: '',
  initialCompetitors: () => []
})
```

#### **Typed Event Emissions**
```typescript
interface Emits {
  // Form submission with validated data
  (e: 'submit', data: { userBusiness: string; competitors: string[] }): void

  // Validation errors
  (e: 'validation-error', errors: string[]): void

  // User interactions for analytics
  (e: 'competitor-added', competitor: string): void
  (e: 'competitor-removed', index: number): void
}

const emit = defineEmits<Emits>()

// Usage with proper typing
const handleSubmit = () => {
  if (isValid.value) {
    emit('submit', {
      userBusiness: userBusiness.value,
      competitors: competitors.value
    })
  } else {
    emit('validation-error', validationErrors.value)
  }
}
```

### **Composables for Reusable Logic**

#### **Well-Defined Composable Interface**
```typescript
// useBusinessComparison.ts
interface UseBusinessComparisonReturn {
  // State (readonly for consumers)
  readonly isLoading: Readonly<Ref<boolean>>
  readonly error: Readonly<Ref<string | null>>
  readonly report: Readonly<Ref<ComparisonReport | null>>

  // Computed properties
  readonly hasReport: Readonly<Ref<boolean>>
  readonly canCreateComparison: Readonly<Ref<boolean>>

  // Actions (clear method signatures)
  createComparison: (request: CreateComparisonRequest) => Promise<void>
  clearComparison: () => void
  retryComparison: () => Promise<void>
}

export const useBusinessComparison = (): UseBusinessComparisonReturn => {
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const report = ref<ComparisonReport | null>(null)
  const lastRequest = ref<CreateComparisonRequest | null>(null)

  const hasReport = computed(() => report.value !== null)
  const canCreateComparison = computed(() => !isLoading.value)

  const createComparison = async (request: CreateComparisonRequest): Promise<void> => {
    isLoading.value = true
    error.value = null
    lastRequest.value = request

    try {
      const response = await apiClient.comparisons.create(request)
      report.value = response
    } catch (err) {
      error.value = handleApiError(err)
      throw err // Re-throw for component-level handling if needed
    } finally {
      isLoading.value = false
    }
  }

  const clearComparison = (): void => {
    report.value = null
    error.value = null
    lastRequest.value = null
  }

  const retryComparison = async (): Promise<void> => {
    if (lastRequest.value) {
      await createComparison(lastRequest.value)
    }
  }

  return {
    // State
    isLoading: readonly(isLoading),
    error: readonly(error),
    report: readonly(report),

    // Computed
    hasReport,
    canCreateComparison,

    // Actions
    createComparison,
    clearComparison,
    retryComparison
  }
}
```

### **Slot-Based Component Design**

#### **Flexible Component Composition**
```vue
<!-- ComparisonCard.vue -->
<template>
  <div class="comparison-card">
    <header class="card-header">
      <slot name="header" :business="business">
        <h3>{{ business.name }}</h3>
      </slot>
    </header>

    <main class="card-content">
      <slot name="content" :business="business" :attributes="business.attributes">
        <!-- Default content -->
        <BusinessAttributesList :attributes="business.attributes" />
      </slot>
    </main>

    <footer class="card-footer">
      <slot name="actions" :business="business">
        <button @click="$emit('view-details', business)">
          View Details
        </button>
      </slot>
    </footer>
  </div>
</template>

<!-- Usage with custom content -->
<ComparisonCard
  :business="userBusiness"
  @view-details="handleViewDetails"
>
  <template #header="{ business }">
    <div class="flex items-center space-x-2">
      <UserIcon class="h-5 w-5" />
      <h3 class="font-bold">{{ business.name }} (Your Business)</h3>
    </div>
  </template>

  <template #content="{ attributes }">
    <BusinessMetrics
      :attributes="attributes"
      :highlight-improvements="true"
    />
  </template>
</ComparisonCard>
```

## **Data Interface Design**

### **Type-Safe Data Models**

#### **Backend Data Models**
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DataSource(str, Enum):
    MOCK = "mock"
    SERPER = "serper"
    GOOGLE = "google"

class BusinessProfileData(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    identifier_used: str = Field(..., description="Original identifier provided by user")
    review_count: int = Field(..., ge=0)
    average_rating: float = Field(..., ge=0, le=5)
    number_of_images: int = Field(..., ge=0)
    has_hours: bool
    has_description: bool
    has_menu_link: bool
    address: Optional[str] = Field(None, max_length=500)
    website_url: Optional[str] = Field(None, regex=r'^https?://.+')
    data_source: DataSource

    class Config:
        schema_extra = {
            "example": {
                "name": "Mario's Italian Restaurant",
                "identifier_used": "mario-restaurant.com",
                "review_count": 150,
                "average_rating": 4.5,
                "number_of_images": 25,
                "has_hours": True,
                "has_description": True,
                "has_menu_link": True,
                "address": "123 Main St, City, State 12345",
                "website_url": "https://mario-restaurant.com",
                "data_source": "serper"
            }
        }
```

#### **Frontend Type Definitions**
```typescript
// types/api.ts
export interface BusinessProfileData {
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
  data_source: DataSource
}

export type DataSource = 'mock' | 'serper' | 'google'

export interface ComparisonReport {
  report_id: string
  user_business: BusinessProfileData
  competitors: BusinessProfileData[]
  ai_comparison_summary: string
  ai_improvement_suggestions: string[]
  created_at: string
}

// API request/response types
export interface CreateComparisonRequest {
  user_business_identifier: string
  competitor_identifiers: string[]
  options?: {
    mock_data?: boolean
    include_detailed_analysis?: boolean
  }
}

export interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
}

export interface ApiError {
  error: {
    type: string
    message: string
    details?: Record<string, any>
  }
}
```

## **User Experience Interface Patterns**

### **Progressive Disclosure**

#### **Multi-Step Form Flow**
```vue
<!-- ComparisonWizard.vue -->
<template>
  <div class="comparison-wizard">
    <!-- Progress indicator -->
    <ProgressSteps
      :steps="steps"
      :current-step="currentStep"
    />

    <!-- Step content -->
    <Transition name="slide" mode="out-in">
      <component
        :is="currentStepComponent"
        v-bind="currentStepProps"
        @next="handleNext"
        @previous="handlePrevious"
        @complete="handleComplete"
      />
    </Transition>

    <!-- Navigation -->
    <div class="wizard-navigation">
      <button
        v-if="!isFirstStep"
        @click="handlePrevious"
        class="btn-secondary"
      >
        Previous
      </button>

      <button
        v-if="!isLastStep"
        @click="handleNext"
        :disabled="!canProceed"
        class="btn-primary"
      >
        Next
      </button>

      <button
        v-if="isLastStep"
        @click="handleComplete"
        :disabled="!canComplete"
        class="btn-primary"
      >
        Create Comparison
      </button>
    </div>
  </div>
</template>
```

### **Loading and Error States**

#### **Comprehensive State Management**
```vue
<template>
  <div class="comparison-results">
    <!-- Loading state -->
    <LoadingSpinner
      v-if="isLoading"
      message="Analyzing your business profile..."
      :progress="loadingProgress"
    />

    <!-- Error state -->
    <ErrorMessage
      v-else-if="error"
      :error="error"
      @retry="retryComparison"
      @contact-support="openSupportDialog"
    />

    <!-- Empty state -->
    <EmptyState
      v-else-if="!hasReport"
      title="No comparison yet"
      description="Create your first business comparison to get started"
      @create-comparison="$emit('create-comparison')"
    />

    <!-- Success state -->
    <ComparisonReport
      v-else
      :report="report"
      @save-report="handleSaveReport"
    />
  </div>
</template>
```

### **Accessibility and Semantic HTML**

#### **Proper ARIA Labels and Roles**
```vue
<template>
  <form
    @submit.prevent="handleSubmit"
    role="form"
    aria-labelledby="comparison-form-title"
  >
    <h2 id="comparison-form-title">
      Create Business Comparison
    </h2>

    <fieldset class="business-input-group">
      <legend>Your Business Information</legend>

      <div class="form-field">
        <label for="user-business">
          Business Name or Website
          <span class="required" aria-label="required">*</span>
        </label>
        <input
          id="user-business"
          v-model="userBusiness"
          type="text"
          required
          :aria-invalid="hasUserBusinessError"
          :aria-describedby="hasUserBusinessError ? 'user-business-error' : undefined"
          placeholder="e.g., Mario's Restaurant or mario-restaurant.com"
        />
        <div
          v-if="hasUserBusinessError"
          id="user-business-error"
          class="error-message"
          role="alert"
        >
          {{ userBusinessError }}
        </div>
      </div>
    </fieldset>

    <!-- Competitor list with proper labeling -->
    <fieldset class="competitors-input-group">
      <legend>Competitor Businesses</legend>

      <div
        v-for="(competitor, index) in competitors"
        :key="index"
        class="competitor-input"
        role="group"
        :aria-labelledby="`competitor-label-${index}`"
      >
        <label :id="`competitor-label-${index}`">
          Competitor {{ index + 1 }}
        </label>
        <div class="input-with-button">
          <input
            v-model="competitors[index]"
            type="text"
            :placeholder="`Enter competitor ${index + 1} name or website`"
          />
          <button
            type="button"
            @click="removeCompetitor(index)"
            :aria-label="`Remove competitor ${index + 1}`"
            class="btn-icon"
          >
            <XIcon class="h-4 w-4" />
          </button>
        </div>
      </div>
    </fieldset>
  </form>
</template>
```

## **API Client Interface**

### **Consistent API Client Design**
```typescript
// api/client.ts
interface ApiClientConfig {
  baseURL: string
  timeout: number
  apiKey?: string
}

class ApiClient {
  private config: ApiClientConfig
  private httpClient: HttpClient

  constructor(config: ApiClientConfig) {
    this.config = config
    this.httpClient = new HttpClient(config)
  }

  // Comparison endpoints
  readonly comparisons = {
    create: async (request: CreateComparisonRequest): Promise<ComparisonReport> => {
      const response = await this.httpClient.post<ComparisonReport>(
        '/api/v1/comparisons',
        request
      )
      return response.data
    },

    get: async (id: string): Promise<ComparisonReport> => {
      const response = await this.httpClient.get<ComparisonReport>(
        `/api/v1/comparisons/${id}`
      )
      return response.data
    }
  }

  // Business search endpoints
  readonly businesses = {
    search: async (
      query: string,
      options?: { location?: string; limit?: number }
    ): Promise<BusinessSearchResult[]> => {
      const params = new URLSearchParams({ query })
      if (options?.location) params.append('location', options.location)
      if (options?.limit) params.append('limit', options.limit.toString())

      const response = await this.httpClient.get<{
        results: BusinessSearchResult[]
      }>(`/api/v1/businesses/search?${params}`)

      return response.data.results
    }
  }
}

// Error handling with proper typing
class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public data?: any
  ) {
    super(`API Error: ${status} ${statusText}`)
  }
}

// HTTP client with interceptors
class HttpClient {
  private client: AxiosInstance

  constructor(config: ApiClientConfig) {
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout,
      headers: {
        'Content-Type': 'application/json',
        ...(config.apiKey && { 'Authorization': `Bearer ${config.apiKey}` })
      }
    })

    // Response interceptor for consistent error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          throw new ApiError(
            error.response.status,
            error.response.statusText,
            error.response.data
          )
        }
        throw error
      }
    )
  }

  async get<T>(url: string): Promise<{ data: T }> {
    const response = await this.client.get<T>(url)
    return { data: response.data }
  }

  async post<T>(url: string, data: any): Promise<{ data: T }> {
    const response = await this.client.post<T>(url, data)
    return { data: response.data }
  }
}
```

## **Documentation Interface**

### **Self-Documenting Code**
```python
# services/comparison_service.py
class ComparisonService:
    """
    Service for creating and managing business profile comparisons.

    This service orchestrates the process of:
    1. Fetching business profile data from external sources
    2. Comparing key attributes between businesses
    3. Generating AI-powered insights and recommendations

    Example:
        service = ComparisonService(data_provider, llm_provider)
        report = await service.create_comparison(
            user_business="mario-restaurant.com",
            competitors=["luigi-pizzeria.com", "tony-italian.com"]
        )
    """

    def __init__(
        self,
        data_provider: BusinessDataProvider,
        llm_provider: LLMProvider
    ):
        """
        Initialize the comparison service.

        Args:
            data_provider: Provider for fetching business profile data
            llm_provider: Provider for generating AI insights
        """
        self.data_provider = data_provider
        self.llm_provider = llm_provider
        self.logger = structlog.get_logger()

    async def create_comparison(
        self,
        user_business: str,
        competitors: List[str],
        options: Optional[ComparisonOptions] = None
    ) -> ComparisonReport:
        """
        Create a comprehensive business profile comparison.

        Args:
            user_business: Business name or website URL to analyze
            competitors: List of competitor business identifiers
            options: Additional options for comparison generation

        Returns:
            Complete comparison report with AI insights

        Raises:
            BusinessNotFoundError: If user business cannot be found
            InsufficientDataError: If not enough competitor data available
            LLMServiceError: If AI analysis fails

        Example:
            report = await service.create_comparison(
                user_business="Mario's Restaurant",
                competitors=["Luigi's Pizza", "Tony's Kitchen"],
                options=ComparisonOptions(include_detailed_analysis=True)
            )
        """
        # Implementation with comprehensive logging
        pass
```

## **Key Interface Design Principles Summary**

1. **Consistency**: Use consistent patterns across API endpoints, components, and data structures
2. **Type Safety**: Leverage TypeScript and Pydantic for compile-time error detection
3. **Progressive Disclosure**: Show information progressively to avoid overwhelming users
4. **Error Handling**: Provide clear, actionable error messages with recovery options
5. **Accessibility**: Design interfaces that work for all users with proper ARIA labels
6. **Documentation**: Write self-documenting code with clear examples and expected behavior
7. **Separation of Concerns**: Keep business logic, presentation, and data access clearly separated
8. **Predictable Behavior**: Follow established patterns so interfaces behave as expected

These principles ensure our interfaces are maintainable, scalable, and provide excellent user experience across all layers of the application.