<script setup lang="ts">
import { ref } from 'vue'

const recommendations = ref([
  {
    id: 1,
    title: 'Complete your business profile',
    description: 'Your business profile is missing key information that customers look for. Add business hours, services offered, and a complete description.',
    priority: 'high',
    impact: 'high',
    effort: 'low'
  },
  {
    id: 2,
    title: 'Improve photo quality and quantity',
    description: 'High-quality photos drive engagement. Add more professional photos of your interior, products, and team.',
    priority: 'medium',
    impact: 'high',
    effort: 'medium'
  },
  {
    id: 3,
    title: 'Respond to negative reviews',
    description: 'You have 5 negative reviews without responses. Responding professionally to negative reviews shows that you value customer feedback.',
    priority: 'high',
    impact: 'medium',
    effort: 'low'
  },
  {
    id: 4,
    title: 'Add more business categories',
    description: 'Your competitors appear in more category searches. Add additional relevant business categories to increase visibility.',
    priority: 'medium',
    impact: 'medium',
    effort: 'low'
  },
  {
    id: 5,
    title: 'Create Google Posts regularly',
    description: 'Your competitors post updates 3x more frequently. Regular posts about promotions and events increase engagement.',
    priority: 'low',
    impact: 'medium',
    effort: 'medium'
  }
]);

const getPriorityColor = (priority: string) => {
  switch(priority) {
    case 'high': return 'bg-error-500';
    case 'medium': return 'bg-warning-500';
    case 'low': return 'bg-secondary-500';
    default: return 'bg-gray-500';
  }
};

const getImpactColor = (impact: string) => {
  switch(impact) {
    case 'high': return 'text-error-700 bg-error-50';
    case 'medium': return 'text-warning-700 bg-warning-50';
    case 'low': return 'text-secondary-700 bg-secondary-50';
    default: return 'text-gray-700 bg-gray-100';
  }
};

const getEffortColor = (effort: string) => {
  switch(effort) {
    case 'high': return 'text-error-700 bg-error-50';
    case 'medium': return 'text-warning-700 bg-warning-50';
    case 'low': return 'text-success-700 bg-success-50';
    default: return 'text-gray-700 bg-gray-100';
  }
};
</script>

<template>
  <div class="card">
    <h2 class="text-xl font-semibold mb-6">AI-Powered Recommendations</h2>

    <div class="space-y-6">
      <div
        v-for="recommendation in recommendations"
        :key="recommendation.id"
        class="border border-gray-200 rounded-lg p-5 transition-all duration-300 hover:shadow-md"
      >
        <div class="flex items-start">
          <div
            class="w-4 h-4 rounded-full flex-shrink-0 mt-1.5 mr-4"
            :class="getPriorityColor(recommendation.priority)"
          ></div>

          <div class="flex-1">
            <h3 class="text-lg font-medium mb-2">{{ recommendation.title }}</h3>
            <p class="text-gray-600 mb-4">{{ recommendation.description }}</p>

            <div class="flex flex-wrap gap-2">
              <span
                class="text-xs px-2 py-1 rounded-full font-medium"
                :class="getImpactColor(recommendation.impact)"
              >
                Impact: {{ recommendation.impact }}
              </span>

              <span
                class="text-xs px-2 py-1 rounded-full font-medium"
                :class="getEffortColor(recommendation.effort)"
              >
                Effort: {{ recommendation.effort }}
              </span>

              <span
                class="text-xs px-2 py-1 rounded-full font-medium text-gray-700 bg-gray-100"
              >
                Priority: {{ recommendation.priority }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
