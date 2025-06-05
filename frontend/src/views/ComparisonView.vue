<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
    <!-- Loading State -->
    <div v-if="store.isLoading" class="flex items-center justify-center min-h-[400px]">
      <LoadingSpinner message="Loading comparison data..." />
    </div>

    <!-- Error State -->
    <div v-else-if="store.error" class="flex items-center justify-center min-h-[400px]">
      <ErrorMessage :message="store.error" />
    </div>

    <!-- No Report State -->
    <div v-else-if="!hasReport && !store.isNavigating" class="flex flex-col items-center justify-center min-h-[400px]">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">No Comparison Data Available</h1>
        <p class="text-gray-600 mb-8">Start a new comparison to see detailed insights about your business.</p>
      </div>
      <BusinessSearchForm />
    </div>

    <!-- Report Available State -->
    <div v-else class="animate-fade-in">
      <div class="mb-8">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Business Profile Comparison</h1>
            <p class="text-gray-600">
              Comparing <span class="font-semibold text-primary-700">{{ userBusiness?.name }}</span>
              with {{ competitors.length }} competitors
            </p>
          </div>
          <div class="flex space-x-2">
            <button
              @click="viewDetailedReport"
              class="btn btn-primary flex items-center"
            >
              <i class="pi pi-file-pdf mr-2"></i>
              View Report
            </button>
            <button
              @click="startNewComparison"
              class="btn btn-secondary flex items-center"
            >
              <i class="pi pi-refresh mr-2"></i>
              New Comparison
            </button>
          </div>
        </div>
      </div>

      <!-- Your Business Profile -->
      <div class="mb-8">
        <div class="card">
          <h2 class="text-xl font-semibold mb-4">Your Business Profile</h2>
          <BusinessProfileCard
            v-if="userBusiness"
            :business="userBusiness"
            :is-user-business="true"
          />
        </div>
      </div>

      <!-- Competitors Section (Collapsible) -->
      <div class="mb-8">
        <div class="card">
          <div class="flex justify-between items-center cursor-pointer group" @click="showCompetitors = !showCompetitors">
            <h2 class="text-xl font-semibold group-hover:text-primary-600 transition-colors duration-200">Competitor Profiles</h2>
            <div class="flex items-center">
              <span class="text-sm text-gray-500 mr-2 group-hover:text-primary-600 transition-colors duration-200">
                {{ showCompetitors ? 'Hide' : 'Show' }}
              </span>
              <i :class="`pi pi-chevron-${showCompetitors ? 'up' : 'down'} text-gray-500 group-hover:text-primary-600 transition-all duration-200 transform group-hover:scale-110`"></i>
            </div>
          </div>

          <div v-if="showCompetitors && competitors.length > 0" class="mt-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <BusinessProfileCard
                v-for="competitor in competitors"
                :key="competitor.name"
                :business="competitor"
                :is-user-business="false"
              />
            </div>
          </div>

          <div v-else-if="showCompetitors && competitors.length === 0" class="mt-6 text-center text-gray-500">
            No competitors found.
          </div>
        </div>
      </div>

      <!-- Metrics Comparison -->
      <div class="mb-8">
        <div class="card">
          <h2 class="text-xl font-semibold mb-6">Performance Rankings</h2>

          <!-- Overall Scores Summary -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-primary-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Profile Score</h3>
              <div class="text-3xl font-bold text-primary-700">
                {{ userBusiness?.profile_score }}%
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Rating</h3>
              <div class="text-3xl font-bold text-gray-700">
                {{ userBusiness?.rating }}
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Number of Ratings</h3>
              <div class="text-3xl font-bold text-gray-700">
                {{ userBusiness?.rating_count }}
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Profile Rank</h3>
              <div class="text-3xl font-bold text-gray-700">
                #{{ userBusiness?.profile_rank }}
              </div>
            </div>
          </div>

          <!-- Ranked Metrics Charts -->
          <div class="space-y-8">
            <div v-for="(metric, index) in rankedMetrics" :key="index" class="border-b border-gray-200 pb-8 last:border-b-0">
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-lg font-semibold">{{ metric.name }}</h3>
                <div v-if="metric.maxValue" class="text-sm text-gray-500">Max: {{ metric.maxValue }}</div>
              </div>

              <!-- Ranked entries -->
              <div class="space-y-4">
                <div v-for="(entry, rankIndex) in metric.entries" :key="entry.name"
                     class="flex items-center p-4 rounded-lg transition-all duration-200 hover:shadow-md"
                     :class="{
                       'bg-primary-50 border-l-4 border-primary-500': entry.isUserBusiness,
                       'bg-yellow-50 border-l-4 border-yellow-400': entry.isAverage,
                       'bg-gray-50': !entry.isUserBusiness && !entry.isAverage
                     }">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center mr-4"
                       :class="getRankBadgeClass(rankIndex)">
                    <span class="text-white font-bold text-sm">{{ rankIndex + 1 }}</span>
                  </div>
                  <div class="flex-1">
                    <div class="flex justify-between items-center mb-2">
                      <span class="font-medium text-gray-800">
                        {{ entry.name }}
                        <span v-if="entry.isUserBusiness" class="text-sm text-primary-600 ml-2">(Your Business)</span>
                        <span v-if="entry.isAverage" class="text-sm text-yellow-600 ml-2">(Average)</span>
                      </span>
                      <span class="font-mono text-sm text-gray-600">
                        {{ entry.score }}{{ metric.maxValue ? ` / ${metric.maxValue}` : '' }}
                      </span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-3">
                      <div
                        class="h-3 rounded-full transition-all duration-500"
                        :class="entry.isAverage ? 'bg-yellow-500' : getScoreColor(entry.score, metric.maxValue || 100)"
                        :style="`width: ${Math.min((entry.score / (metric.maxValue || 100)) * 100, 100)}%`"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-center space-x-4">
        <button @click="viewDetailedReport" class="btn btn-primary flex items-center">
          <span>View Detailed Report</span>
          <i class="pi pi-arrow-right ml-2"></i>
        </button>
        <button @click="startNewComparison" class="btn btn-secondary flex items-center">
          <span>New Comparison</span>
          <i class="pi pi-refresh ml-2"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComparisonStore } from '@/stores/comparisonStore'
import BusinessProfileCard from '@/components/business/BusinessProfileCard.vue'
import BusinessSearchForm from '@/components/business/BusinessSearchForm.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

const router = useRouter();
const store = useComparisonStore();
const showCompetitors = ref(false); // Toggle state for competitor section

// Computed properties for easier access to store data
const userBusiness = computed(() => store.report?.user_business);
const competitors = computed(() => store.report?.competitor_businesses || []);
const hasReport = computed(() => store.hasReport);

// Metrics with ranking
const rankedMetrics = computed(() => {
  if (!store.report) return [];

  return [
    {
      name: 'Rating',
      maxValue: 5 as number | null,
      entries: getRankedEntries('rating')
    },
    {
      name: 'Number of Ratings',
      maxValue: null, // Dynamic max based on highest value
      entries: getRankedEntries('rating_count')
    },
    {
      name: 'Profile Score',
      maxValue: 100,
      entries: getRankedEntries('profile_score')
    },
    {
      name: 'Number of Images',
      maxValue: 50,
      entries: getRankedEntries('image_count')
    }
  ].map(metric => {
    // Set dynamic max value if not specified
    if (metric.maxValue === null) {
      const maxScore = Math.max(...metric.entries.map(e => e.score));
      metric.maxValue = Math.max(maxScore, 100); // Minimum of 100 for better visualization
    }
    return metric;
  })
});

// Helper function to get ranked entries for a metric
const getRankedEntries = (metricKey: string) => {
  if (!store.report) return [];

  const user = store.report.user_business;
  const competitorValues = competitors.value;

  // Create entries for user business
  const userEntry = {
    name: user.name || 'Your Business',
    score: getMetricValue(user, metricKey),
    isUserBusiness: true,
    isAverage: false
  };

  // Create entries for competitors
  const competitorEntries = competitorValues.map((competitor, index) => ({
    name: competitor.name || `Competitor ${index + 1}`,
    score: getMetricValue(competitor, metricKey),
    isUserBusiness: false,
    isAverage: false
  }));

  // Calculate average score across all businesses (user + competitors)
  const allScores = [userEntry.score, ...competitorEntries.map(c => c.score)]
    .filter(score => score > 0);
  const averageScore = allScores.length > 0 ?
  allScores.reduce((sum, score) => sum + score, 0) / allScores.length : 0;

  const averageEntry = {
    name: 'Average Score',
    score: Math.round(averageScore * 100) / 100, // Round to 2 decimal places
    isUserBusiness: false,
    isAverage: true
  };

  // Get top 5 competitors
  const topCompetitors = competitorEntries
    .sort((a, b) => b.score - a.score)
    .slice(0, 5);

  // Combine all entries and sort by score
  const allEntries = [...topCompetitors, userEntry, averageEntry]
    .sort((a, b) => b.score - a.score);

  return allEntries;
}

// Helper function to get metric value from business object
const getMetricValue = (business: any, metricKey: string) => {
  switch (metricKey) {
    case 'rating':
      return business.rating
    case 'rating_count':
      return business.rating_count
    case 'profile_score':
      return business.profile_score
    case 'image_count':
      return business.image_count
    default:
      return 0
  }
}

const getScoreColor = (score: number, maxValue: number) => {
  const percentage = (score / maxValue) * 100;
  if (percentage >= 80) return 'bg-success-500';
  if (percentage >= 60) return 'bg-secondary-500';
  if (percentage >= 40) return 'bg-warning-500';
  return 'bg-error-500';
}

const getRankBadgeClass = (rankIndex: number) => {
  if (rankIndex === 0) return 'bg-yellow-500'; // Gold for 1st place
  if (rankIndex === 1) return 'bg-gray-400';   // Silver for 2nd place
  if (rankIndex === 2) return 'bg-amber-600';  // Bronze for 3rd place
  return 'bg-gray-300';                        // Default for others
}

const viewDetailedReport = () => {
  router.push({ name: 'report' });
}

const startNewComparison = () => {
  store.isNavigating = true;
  router.push({ name: 'home' }).then(() => {
    store.clearReport();
    store.isNavigating = false;
  })
}

onMounted(() => {
  // If no report exists, redirect to home
  if (!store.hasReport) {
    router.push({ name: 'home' });
  }
})
</script>
