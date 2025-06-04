<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComparisonStore } from '@/stores/comparisonStore'
import BusinessProfileCard from '@/components/business/BusinessProfileCard.vue'
import BusinessSearchForm from '@/components/business/BusinessSearchForm.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

const router = useRouter()
const store = useComparisonStore()
const showCompetitors = ref(false) // Toggle state for competitor section

// Computed properties for easier access to store data
const userBusiness = computed(() => store.report?.user_business)
const competitors = computed(() => store.report?.competitor_businesses || [])
const hasReport = computed(() => store.hasReport)

// Simple metrics calculation based on available data
const comparisonMetrics = computed(() => {
  if (!store.report) return []

  const user = store.report.user_business
  const competitorValues = competitors.value

  return [
    {
      name: 'Rating',
      yourScore: user.rating || 0,
      competitorScores: competitorValues.map(c => c.rating || 0),
      industry: 4.4, // Static for now
      maxValue: 5
    },
    // {
    //   name: 'Number of Ratings',
    //   yourScore: user.rating_count || 0,
    //   competitorScores: competitorValues.map(c => c.rating_count || 0),
    //   industry: 75, // Static for now
    //   maxValue: 200
    // },
    // {
    //   name: 'Profile Completeness Score',
    //   yourScore: Math.round((user.profile_score || 0) * 100),
    //   competitorScores: competitorValues.map(c => Math.round((c.profile_score || 0) * 100)),
    //   industry: 75, // Static for now
    //   maxValue: 100
    // },
    // {
    //   name: 'Number of Images',
    //   yourScore: user.image_count || 0,
    //   competitorScores: competitorValues.map(c => c.image_count || 0),
    //   industry: 15, // Static for now
    //   maxValue: 50
    // }
  ]
})

const getScoreColor = (score: number, maxValue: number) => {
  const percentage = (score / maxValue) * 100
  if (percentage >= 80) return 'bg-success-500'
  if (percentage >= 60) return 'bg-secondary-500'
  if (percentage >= 40) return 'bg-warning-500'
  return 'bg-error-500'
}

const viewDetailedReport = () => {
  router.push({ name: 'report' })
}

const startNewComparison = () => {
  store.clearReport()
  router.push({ name: 'home' })
}

onMounted(() => {
  // If no report exists, redirect to home
  if (!store.hasReport) {
    router.push({ name: 'home' })
  }
})
</script>

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
    <div v-else-if="!hasReport" class="flex flex-col items-center justify-center min-h-[400px]">
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
          <button @click="startNewComparison" class="btn btn-secondary">
            New Comparison
          </button>
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
                :key="competitor.identifier_used || competitor.name"
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
          <h2 class="text-xl font-semibold mb-6">Performance Metrics</h2>

          <!-- Overall Scores Summary -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-primary-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Profile Score</h3>
              <div class="text-3xl font-bold text-primary-700">
                {{ Math.round((userBusiness?.profile_score || 0) * 100) }}%
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Rating</h3>
              <div class="text-3xl font-bold text-gray-700">
                {{ userBusiness?.rating?.toFixed(1) || 'N/A' }}
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Number of Ratings</h3>
              <div class="text-3xl font-bold text-gray-700">
                {{ userBusiness?.rating_count || 0 }}
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 text-center">
              <h3 class="text-sm font-medium text-gray-600 mb-1">Your Rank</h3>
              <div class="text-3xl font-bold text-gray-700">
                #{{ userBusiness?.rank || 'N/A' }}
              </div>
            </div>
          </div>

          <!-- Detailed Metrics -->
          <div class="space-y-6">
            <div v-for="(metric, index) in comparisonMetrics" :key="index" class="border-b border-gray-200 pb-6">
              <div class="flex justify-between items-center mb-2">
                <h3 class="font-medium">{{ metric.name }}</h3>
                <div class="text-gray-500 text-sm">Max: {{ metric.maxValue }}</div>
              </div>

              <!-- Your Score -->
              <div class="mb-4">
                <div class="flex justify-between items-center mb-1">
                  <div class="text-sm font-medium">{{ userBusiness?.name }}</div>
                  <div class="text-sm">{{ metric.yourScore }} / {{ metric.maxValue }}</div>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    class="h-2.5 rounded-full transition-all duration-500"
                    :class="getScoreColor(metric.yourScore, metric.maxValue)"
                    :style="`width: ${(metric.yourScore / metric.maxValue) * 100}%`"
                  ></div>
                </div>
              </div>

              <!-- Competitors -->
              <div v-for="(score, compIndex) in metric.competitorScores" :key="compIndex" class="mb-4">
                <div class="flex justify-between items-center mb-1">
                  <div class="text-sm font-medium">
                    {{ competitors[compIndex]?.name || `Competitor ${compIndex + 1}` }}
                  </div>
                  <div class="text-sm">{{ score }} / {{ metric.maxValue }}</div>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    class="h-2.5 rounded-full transition-all duration-500"
                    :class="getScoreColor(score, metric.maxValue)"
                    :style="`width: ${(score / metric.maxValue) * 100}%`"
                  ></div>
                </div>
              </div>

              <!-- Industry Average -->
              <div>
                <div class="flex justify-between items-center mb-1">
                  <div class="text-sm font-medium">Industry Average</div>
                  <div class="text-sm">{{ metric.industry }} / {{ metric.maxValue }}</div>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    class="h-2.5 bg-gray-600 rounded-full transition-all duration-500"
                    :style="`width: ${(metric.industry / metric.maxValue) * 100}%`"
                  ></div>
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
