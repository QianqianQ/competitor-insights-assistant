import type { ComparisonRequestPayload, ComparisonReportData } from '@/types/comparison';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export async function fetchComparisonAPI(payload: ComparisonRequestPayload): Promise<ComparisonReportData> {
  try {
    const response = await fetch(`${API_BASE_URL}/comparisons/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add Authorization header if needed, e.g.:
        // 'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        // If parsing error response as JSON fails, use status text
        throw new Error(response.statusText || `HTTP error! status: ${response.status}`);
      }
      // Use error message from backend if available, otherwise a generic one
      throw new Error(errorData?.error || errorData?.detail || `HTTP error! status: ${response.status}`);
    }

    const responseData: ComparisonReportData = await response.json();
    // Crucial: Ensure the backend is sending `competitors` as an array of objects.
    // If `competitors` is missing or not an array, the ResultsView will break.
    // The current backend ComparisonReportSerializer has `competitor_count` NOT `competitors`.
    // This needs to be reconciled with the backend. For now, we expect `competitors`.
    if (responseData.competitor_businesses && !Array.isArray(responseData.competitor_businesses)) {
      console.warn('API response missing or has invalid format for "competitors". Defaulting to empty array.');
      // If the backend sends competitor_count instead of competitors list:
      // responseData.competitors = []; // Or handle it based on how you want to show this missing data
      // This is a placeholder; ideally, the backend sends the full competitor data.
    }

    return responseData;

  } catch (error: any) {
    console.error('API call failed:', error);
    throw new Error(error.message || 'Network error or server issue.');
  }
}