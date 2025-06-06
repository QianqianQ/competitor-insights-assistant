# Competitor Insights Assistant - Backend

## Overview

This Django backend implements a **Service Layer + Provider Pattern** architecture for the Competitor Insights Assistant. It provides AI-powered business profile comparison with support for multiple data sources and LLM providers.

## Architecture

### 🏗️ Service Layer Pattern
- **Clean separation** between API, business logic, and data access
- **(TODO) Provider abstractions** for easy switching between data sources and LLM services
- **Structured logging** with observability from day one
- **Type-safe** implementation with comprehensive error handling

### 📦 App Structure
```
apps/
├── common/          # Shared utilities, exceptions, logging
├── businesses/      # Business profile models and data
├── comparisons/     # Comparison logic, services, and API
└── providers/       # Data and LLM provider abstractions
```

## Features Implemented

### ✅ Core MVP Features
- **Business Profile Management**: Store and manage business profiles with attributes
- **Mock Data Provider**: Development-ready mock business data
- **AI Comparison Engine**: Generate insights using LLM providers
- **REST API**: Complete API endpoints for frontend integration
- **Structured Logging**: Observability with structured logs

### 🔌 Provider Pattern Implementation
- **Data Providers**:
  - `SerperBusinessDataProvider`
- **LLM Providers**:
  - `OpenAIProvider` (mock implementation, ready for real API)
  -  ` (TODO) OllamaProvider` (placeholder for local models)

### 🚀 API Endpoints

#### Comparison Operations
```
POST   /api/v1/comparisons/              # Create comparison
```

### 4. Test the API
```bash
# Create a comparison
curl -X POST http://localhost:8000/api/v1/comparisons/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_business_identifier": "Mario'\''s Restaurant",
    "report_style": "casual"
  }'
```

## Configuration

### (TO UPDATE) Environment Variables
```bash
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key

# External API Keys (when ready)
OPENAI_API_KEY=your-openai-key
SERPER_API_KEY=your-serper-key

# LLM Provider Settings
LLM_PROVIDER=openai  # or 'ollama'
LLM_MODEL=gpt-4      # or 'llama2'
OLLAMA_BASE_URL=http://localhost:11434
```

## Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.comparisons

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage
- ✅ Service layer logic
- ✅ API endpoints
- ✅ Provider implementations
- ✅ Data models
- ✅ Serializers and validation

## Data Models

### BusinessProfile (Not In Use)
- Core business information (name, address, website)
- Data source tracking
- User business identification
- Comparable metrics (reviews, ratings, images)
- Business completeness indicators
- Raw data snapshots for LLM context

### ComparisonReport
- AI-generated analysis and recommendations
- Metadata (tokens used, provider, model)
- Relationship tracking between user and competitors

**Note:** BusinessProfileData with `dataclass` decorator is used for simplicity in this stage.

## (TODO)Provider Pattern Details

### Data Provider Interface
```python
class BusinessDataProvider(ABC):
    async def fetch_business_profile(identifier: str) -> BusinessProfileData
    async def search_businesses(query: str, location: str, limit: int) -> List[BusinessSearchResult]
```

### LLM Provider Interface
```python
class LLMProvider(ABC):
    async def generate_comparison_analysis(user_data, competitor_data) -> LLMResponse
    async def generate_suggestions(comparison_data) -> List[str]
```

## Next Steps

### Phase 2: Real API Integration
1. **Implement Serper.dev integration**
   ```python
   # In apps/providers/data_providers.py
   class SerperBusinessDataProvider:
       async def fetch_business_profile(self, identifier):
           # Implement real API calls
   ```

### Phase 3: Enhanced Features
- **Caching layer** for expensive API calls
- **Rate limiting** for external APIs

### Phase 4: Production Readiness
- **PostgreSQL** database configuration
- **Redis** for caching and sessions
- **Celery** for background tasks
- **Monitoring** and alerting

### (TODO) Adding New Providers

1. **Create provider class**:
   ```python
   class NewDataProvider(BusinessDataProvider):
       async def fetch_business_profile(self, identifier):
           # Implementation
   ```

2. **Update service configuration**:
   ```python
   # In apps/comparisons/services.py
   def get_data_provider():
       provider_type = settings.DATA_PROVIDER
       if provider_type == 'new_provider':
           return NewDataProvider()
   ```

3. **Add tests**:
   ```python
   class NewProviderTest(TestCase):
       def test_provider_functionality(self):
           # Test implementation
   ```
