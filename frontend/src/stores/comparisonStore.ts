import { defineStore } from 'pinia';
import { fetchComparisonAPI } from '@/services/comparisonService';
import type { ComparisonState, ComparisonRequestPayload, DisplayBusinessProfile } from '@/types/comparison';

export const useComparisonStore = defineStore('comparison', {
  state: (): ComparisonState => ({
    isLoading: false,
    error: null,
    report: null,
    userInput: '',
    isNavigating: false,
  }),
  actions: {
    // Action to fetch comparison report
    async fetchComparisonReport(payload: ComparisonRequestPayload) {
      this.isLoading = true;
      this.error = null;
      this.report = null; // Clear previous report
      this.userInput = payload.user_business_identifier; // Store user input

      try {
        const data = await fetchComparisonAPI(payload);

        // Map backend data to frontend DisplayBusinessProfile, calculating scores
        const processedUserBusiness = this.processBusinessProfile(data.user_business);
        const processedCompetitors = data.competitor_businesses.map(
          comp => this.processBusinessProfile(comp));

        // Profile rank businesses based on profile score
        const allBusinesses = [processedUserBusiness, ...processedCompetitors]
          .sort((a, b) => (b.profile_score || 0) - (a.profile_score || 0));

        allBusinesses.forEach((biz, index) => {
          biz.profile_rank = index + 1;
        });

        // Create report object
        this.report = {
          ...data,
          user_business: processedUserBusiness,
          competitor_businesses: processedCompetitors,
        };
        console.log('report', this.report);

      } catch (err: any) {
        this.error = err.message || 'Failed to fetch comparison report.';
        console.error('Error fetching comparison report:', err);
      } finally {
        this.isLoading = false;
      }
    },
    // Helper to process business profile
    processBusinessProfile(businessData: any): DisplayBusinessProfile {

      const profile_score = this.calculateProfileScore(businessData);
      return {
        name: businessData.name || 'N/A',
        website: businessData.website,
        address: businessData.address,
        rating: businessData.rating,
        rating_count: businessData.rating_count,
        image_count: businessData.image_count,
        category: businessData.category,
        has_hours: businessData.has_hours,
        has_description: businessData.has_description,
        has_menu_link: businessData.has_menu_link,
        has_price_level: businessData.has_price_level,
        latitude: businessData.latitude,
        longitude: businessData.longitude,
        profile_score,
      };
    },
    // Helper to calculate profile score
    calculateProfileScore(business: any): number {
      let score = 0;
      const fieldsToCheck = [
        'has_hours',
        'has_description',
        'has_menu_link',
        'has_price_level'
      ];
      let completed_fields = 0;

      fieldsToCheck.forEach(field => {
        if (business[field] === true || business[field] === 'true') {
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

      return Math.min(parseFloat((score * 100).toFixed(2)), 100);
    },
    // Helper to clear report
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