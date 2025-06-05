<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="text-center mb-8">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-secondary-600">
          Business Comparison Report
        </h1>
        <p v-if="store.report" class="text-lg text-gray-600 mb-6">
          Comprehensive analysis of <span class="font-semibold text-primary-700">{{ store.report.user_business.name }}</span> against competitors
        </p>
        <div class="flex justify-center space-x-4">
          <button @click="goBack" class="btn btn-secondary flex items-center">
            <i class="pi pi-arrow-left mr-2"></i>
            New Comparison
          </button>
          <button @click="goToComparison" class="btn btn-primary flex items-center">
            <i class="pi pi-chart-bar mr-2"></i>
            View Comparison
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="store.isLoading" class="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner message="Generating report..." />
      </div>

      <!-- Error State -->
      <div v-else-if="store.error" class="flex items-center justify-center min-h-[400px]">
        <ErrorMessage :message="store.error" />
      </div>

      <!-- No Report State -->
      <div v-else-if="!store.report && !store.isNavigating" class="flex flex-col items-center justify-center min-h-[400px]">
        <div class="text-center">
          <i class="pi pi-file-excel text-6xl text-gray-400 mb-4"></i>
          <h2 class="text-2xl font-semibold text-gray-800 mb-2">No Report Available</h2>
          <p class="text-gray-600 mb-6">Start a new comparison to generate your business report.</p>
          <button @click="goBack" class="btn btn-primary">
            Start New Comparison
          </button>
        </div>
      </div>

      <!-- Report Content -->
      <div v-else class="space-y-8 animate-fade-in">
        <!-- Quick Stats Overview -->
        <div class="card">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <i class="pi pi-chart-line text-primary-600 mr-3"></i>
            Performance Overview
          </h2>
          <div v-if="store.report" class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="text-center p-4 bg-gradient-to-br from-primary-50 to-primary-100 rounded-xl">
              <div class="text-3xl font-bold text-primary-700 mb-1">
                #{{ store.report.user_business.profile_rank }}
              </div>
              <div class="text-sm text-primary-600 font-medium">Profile Rank</div>
            </div>
            <div class="text-center p-4 bg-gradient-to-br from-secondary-50 to-secondary-100 rounded-xl">
              <div class="text-3xl font-bold text-secondary-700 mb-1">
                {{ store.report.user_business.rating }}
              </div>
              <div class="text-sm text-secondary-600 font-medium">Average Rating</div>
            </div>
            <div class="text-center p-4 bg-gradient-to-br from-success-50 to-success-100 rounded-xl">
              <div class="text-3xl font-bold text-success-700 mb-1">
                {{ store.report.user_business.rating_count }}
              </div>
              <div class="text-sm text-success-600 font-medium">Total Reviews</div>
            </div>
            <div class="text-center p-4 bg-gradient-to-br from-accent-50 to-accent-100 rounded-xl">
              <div class="text-3xl font-bold text-accent-700 mb-1">
                {{ store.report.user_business.profile_score }}%
              </div>
              <div class="text-sm text-accent-600 font-medium">Profile Score</div>
            </div>
          </div>
        </div>

        <!-- Your Business Profile -->
        <div class="card">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <i class="pi pi-building text-primary-600 mr-3"></i>
            Your Business Profile
          </h2>
          <div v-if="store.report" class="bg-gradient-to-r from-primary-50 to-secondary-50 p-6 rounded-xl">
            <BusinessProfileCard :business="store.report.user_business" :is-user-business="true" />
          </div>
        </div>

        <!-- AI-Powered Summary -->
        <div class="card">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <i class="pi pi-lightbulb text-warning-500 mr-3"></i>
            AI-Powered Analysis
          </h2>

          <div v-if="parsedAnalysis" class="space-y-6">
            <!-- Overview Section -->
            <div v-if="parsedAnalysis.overview" class="bg-gradient-to-r from-primary-50 to-secondary-50 p-6 rounded-xl border-l-4 border-primary-400">
              <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                <i class="pi pi-info-circle text-primary-600 mr-2"></i>
                Market Overview
              </h3>
              <p class="text-gray-700 leading-relaxed">{{ parsedAnalysis.overview }}</p>
            </div>

            <!-- Strengths Section -->
            <div v-if="parsedAnalysis.strengths?.length" class="bg-gradient-to-r from-success-50 to-primary-50 p-6 rounded-xl border-l-4 border-success-400">
              <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <i class="pi pi-check-circle text-success-600 mr-2"></i>
                Your Strengths
              </h3>
              <ul class="space-y-2">
                <li v-for="(strength, index) in parsedAnalysis.strengths" :key="index" class="flex items-start">
                  <i class="pi pi-plus text-success-600 mr-3 mt-1 text-sm"></i>
                  <span class="text-gray-700">{{ strength }}</span>
                </li>
              </ul>
            </div>

            <!-- Weaknesses Section -->
            <div v-if="parsedAnalysis.weaknesses?.length" class="bg-gradient-to-r from-warning-50 to-accent-50 p-6 rounded-xl border-l-4 border-warning-400">
              <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <i class="pi pi-exclamation-triangle text-warning-600 mr-2"></i>
                Areas for Improvement
              </h3>
              <ul class="space-y-2">
                <li v-for="(weakness, index) in parsedAnalysis.weaknesses" :key="index" class="flex items-start">
                  <i class="pi pi-minus text-warning-600 mr-3 mt-1 text-sm"></i>
                  <span class="text-gray-700">{{ weakness }}</span>
                </li>
              </ul>
            </div>

            <!-- Competitive Position Section -->
            <div v-if="parsedAnalysis.competitive_position" class="bg-gradient-to-r from-secondary-50 to-accent-50 p-6 rounded-xl border-l-4 border-secondary-400">
              <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                <i class="pi pi-chart-bar text-secondary-600 mr-2"></i>
                Competitive Position
              </h3>
              <p class="text-gray-700 leading-relaxed">{{ parsedAnalysis.competitive_position }}</p>
            </div>
          </div>

          <!-- Fallback for plain text analysis -->
          <div v-else class="bg-gradient-to-r from-warning-50 to-accent-50 p-6 rounded-xl border-l-4 border-warning-400">
            <div class="prose prose-lg max-w-none">
              <p v-if="store.report" class="text-gray-700 leading-relaxed text-lg">
                {{ store.report.ai_comparison_summary }}
              </p>
              <p v-else class="text-gray-700 leading-relaxed text-lg">
                No analysis available
              </p>
            </div>
          </div>
        </div>

        <!-- Improvement Suggestions -->
        <div class="card">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <i class="pi pi-thumbs-up text-success-600 mr-3"></i>
            Actionable Recommendations
          </h2>
          <div v-if="store.report" class="space-y-4">
            <div
              v-for="(suggestion, index) in store.report.ai_improvement_suggestions"
              :key="index"
              class="group relative overflow-hidden"
            >
              <div class="flex items-start p-6 bg-gradient-to-r from-success-50 to-primary-50 rounded-xl border border-success-200 hover:shadow-md transition-all duration-300">
                <div class="flex-shrink-0 mr-4">
                  <div class="w-8 h-8 bg-success-500 text-white rounded-full flex items-center justify-center font-bold text-sm">
                    {{ index + 1 }}
                  </div>
                </div>
                <div class="flex-1">
                  <p class="text-gray-800 leading-relaxed">{{ suggestion }}</p>
                </div>
                <div class="flex-shrink-0 ml-4">
                  <i class="pi pi-arrow-right text-success-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Competitors Preview -->
        <div v-if="store.report && store.report.competitor_businesses?.length > 0" class="card">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <i class="pi pi-users text-secondary-600 mr-3"></i>
            Top Competitors
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="competitor in topCompetitors"
              :key="competitor.name"
              class="bg-gradient-to-br from-gray-50 to-secondary-50 p-4 rounded-xl border border-gray-200 hover:shadow-md transition-all duration-300"
            >
              <div class="text-center">
                <h3 class="font-semibold text-gray-800 mb-2">{{ competitor.name }}</h3>
                <div class="flex justify-center space-x-4 text-sm text-gray-600">
                  <div>
                    <span class="font-medium">{{ competitor.rating }}</span>
                    <i class="pi pi-star-fill text-yellow-400 ml-1"></i>
                  </div>
                  <div>
                    <span class="font-medium">{{ competitor.rating_count }}</span>
                    <span class="text-xs ml-1">reviews</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-6 text-center">
            <button @click="goToComparison" class="btn btn-secondary">
              View Detailed Comparison
            </button>
          </div>
        </div>

        <!-- Report Metadata -->
        <div class="card bg-gradient-to-r from-gray-50 to-primary-50">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
            <div class="mb-4 md:mb-0">
              <h3 class="text-lg font-semibold text-gray-800 mb-2">Report Information</h3>
              <p class="text-gray-600">
                Generated on {{ new Date(store.report?.created_at || Date.now()).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                }) }}
              </p>
              <p v-if="store.report?.metadata" class="text-sm text-gray-500 mt-1">
                Powered by {{ store.report.metadata.llm_provider || 'AI' }}
                <span v-if="store.report.metadata.llm_model">({{ store.report.metadata.llm_model }})</span>
              </p>
            </div>
            <div class="flex space-x-3">
              <button @click="goToComparison" class="btn btn-secondary flex items-center">
                <i class="pi pi-chart-bar mr-2"></i>
                View Comparison
              </button>
              <button @click="goBack" class="btn btn-primary flex items-center">
                <i class="pi pi-plus mr-2"></i>
                New Analysis
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useComparisonStore } from '@/stores/comparisonStore';
import BusinessProfileCard from '@/components/business/BusinessProfileCard.vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';

const store = useComparisonStore();
const router = useRouter();

// Parse the AI analysis JSON if it's structured
const parsedAnalysis = computed(() => {
  if (!store.report?.ai_comparison_summary) return null;

  try {
    // Try to parse as JSON
    const parsed = JSON.parse(store.report.ai_comparison_summary);

    // Validate that it has the expected structure
    if (typeof parsed === 'object' && parsed !== null) {
      return parsed;
    }
    return null;
  } catch (error) {
    // If parsing fails, return null to fall back to plain text
    return null;
  }
});

// Get top 3 competitors sorted by rating and rating count
const topCompetitors = computed(() => {
  if (!store.report?.competitor_businesses?.length) return [];

  return store.report.competitor_businesses
    .slice() // Create a copy to avoid mutating the original array
    .sort((a, b) => {
      // Primary sort: by rating (higher is better)
      const ratingA = a.rating || 0;
      const ratingB = b.rating || 0;

      if (ratingB !== ratingA) {
        return ratingB - ratingA; // Higher rating first
      }

      // Secondary sort: by rating count (more reviews is better)
      const countA = a.rating_count || 0;
      const countB = b.rating_count || 0;

      return countB - countA; // Higher count first
    })
    .slice(0, 3); // Take top 3
});

function goBack() {
  store.isNavigating = true;
  router.push({ name: 'home' }).then(() => {
    store.clearReport();
    store.isNavigating = false;
  });
}

function goToComparison() {
  router.push({ name: 'comparison' });
}
</script>
