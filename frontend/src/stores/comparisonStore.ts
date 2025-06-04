import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import { fetchComparisonAPI } from '@/services/comparisonService';
import type { ComparisonState, ComparisonReportData, ComparisonRequestPayload } from '@/types/comparison';

export const useComparisonStore = defineStore('comparison', {
  state: (): ComparisonState => ({
    isLoading: false,
    error: null,
    report: null,
    userInput: '',
    isNavigating: false,
  }),
  actions: {
    async fetchComparisonReport(payload: ComparisonRequestPayload) {
      this.isLoading = true;
      this.error = null;
      this.report = null; // Clear previous report
      this.userInput = payload.user_business_identifier; // Store user input
      const router = useRouter(); // Get router instance inside action

      try {
        // Assuming your API service returns ComparisonReportData directly
        // The actual backend response might need mapping if it doesn't match ComparisonReportData perfectly
        const data = await fetchComparisonAPI(payload);
        console.log('data', data);
        // Map backend data to frontend DisplayBusinessProfile, calculating scores
        const processedUserBusiness = this.processBusinessProfile(data.user_business);
        const processedCompetitors = data.competitor_businesses.map(comp => this.processBusinessProfile(comp));

        // Rank businesses based on score - Simplified: We only care about user's business score for now
        // If competitors are not displayed, extensive ranking might be overkill.
        // The user's business will have its score. If needed later, ranking can be expanded.
        const allBusinesses = [processedUserBusiness, ...processedCompetitors]
          .sort((a, b) => (b.profile_score || 0) - (a.profile_score || 0));

        allBusinesses.forEach((biz, index) => {
          biz.rank = index + 1;
        });

        this.report = {
          ...data,
          user_business: processedUserBusiness, // User business with its score
          competitor_businesses: processedCompetitors, // Still store processed competitors, even if not displayed in detail
                                             // This allows AI summary/suggestions to use them if backend sends them
                                             // and facilitates re-adding display later.
        };

        // Navigate to results page upon success
        // It's generally better to handle navigation in the component after the action resolves,
        // but for simplicity in MVP, we can do it here or ensure router is available.
        // However, useRouter() composable should be called within a setup function or a component.
        // For store actions, it's better to pass router instance or handle navigation in component.
        // Let's assume navigation happens in the component for now.
        // router.push('/comparison-results'); // Example, better handled in component

      } catch (err: any) {
        this.error = err.message || 'Failed to fetch comparison report.';
        console.error('Error fetching comparison report:', err);
      } finally {
        this.isLoading = false;
      }
    },

    // Helper to calculate profile score (based on backend logic)
    calculateProfileScore(business: any): number {
      let score = 0;
      const fieldsToCheck = ['has_hours', 'has_description', 'has_menu_link'];
      let completed_fields = 0;

      fieldsToCheck.forEach(field => {
        if (business[field] === true || business[field] === 'true') { // Check for boolean true or string 'true'
          completed_fields++;
        }
      });

      if (fieldsToCheck.length > 0) {
         score = completed_fields / fieldsToCheck.length;
      }

      if (business.rating_count && business.rating_count > 0) {
        score += 0.1;
      }
      if (business.image_count && business.image_count > 0) {
        score += 0.1;
      }
      return parseFloat(Math.min(score, 1.0).toFixed(2)); // Return as number, rounded
    },

    processBusinessProfile(businessData: any) {
      // The backend user_business and competitors are already dicts from .to_dict()
      // The `map_response_to_profile` in `data_providers.py` creates `BusinessProfileData`
      // which has fields like `name`, `rating_count` etc. `BusinessProfileData.to_dict()` makes them available.
      // The API spec structure for `user_business` and `competitors` is a bit different, where attributes are nested.
      // For now, I'll assume the backend response for user_business and competitors matches `DisplayBusinessProfile` directly
      // or can be easily mapped.
      // If `attributes` is a nested object in the response:
      // const attributes = businessData.attributes || {};
      // const profile_score = this.calculateProfileScore({ ...businessData, ...attributes });
      // return { ...businessData, ...attributes, profile_score };

      // If attributes are flat as in BusinessProfileData.to_dict():
      const profile_score = this.calculateProfileScore(businessData);
      // Ensure all DisplayBusinessProfile fields from the API response are mapped
      // and defaults are applied if necessary.
      return {
        name: businessData.name || 'N/A',
        website: businessData.website,
        address: businessData.address,
        rating: businessData.rating,
        rating_count: businessData.rating_count,
        image_count: businessData.image_count,
        category: businessData.category || businessData.type, // API spec uses 'type', frontend type uses 'category'
        has_hours: businessData.has_hours,
        has_description: businessData.has_description,
        has_menu_link: businessData.has_menu_link,
        has_price_level: businessData.has_price_level,
        latitude: businessData.latitude,
        longitude: businessData.longitude,
        identifier_used: businessData.identifier_used || businessData.name,
        profile_data_source: businessData.profile_data_source || 'Unknown',
        profile_score, // Calculated score
        rank: businessData.rank, // Rank might come from backend or be calculated; for now, pass through if present
      };
    },

    clearReport() {
      this.report = null;
      this.error = null;
      this.userInput = '';
      this.isNavigating = false;
    }
  },
  getters: {
    hasReport(): boolean {
      return !!this.report;
    }
  }
});