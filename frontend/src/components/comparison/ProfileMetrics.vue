<script setup lang="ts">
import { computed } from 'vue'
import type { Business, ComparisonMetric } from '../../types'

const props = defineProps<{
  businessName: string;
  competitors: Business[];
  metrics: ComparisonMetric[];
}>();

const getScoreColor = (score: number, metric: ComparisonMetric) => {
  const percentage = (score / metric.maxValue) * 100;

  if (percentage >= 80) return 'bg-success-500';
  if (percentage >= 60) return 'bg-secondary-500';
  if (percentage >= 40) return 'bg-warning-500';
  return 'bg-error-500';
};

const getCompetitorName = (index: number): string => {
  return props.competitors[index]?.name || `Competitor ${index + 1}`;
};

const averageScore = computed(() => {
  if (!props.metrics.length) return 0;

  const total = props.metrics.reduce((sum, metric) => {
    return sum + (metric.yourScore / metric.maxValue) * 100;
  }, 0);

  return Math.round(total / props.metrics.length);
});

const competitorAverages = computed(() => {
  if (!props.metrics.length || !props.competitors.length) return [];

  return props.competitors.map((_, competitorIndex) => {
    const total = props.metrics.reduce((sum, metric) => {
      return sum + (metric.competitorScores[competitorIndex] / metric.maxValue) * 100;
    }, 0);

    return Math.round(total / props.metrics.length);
  });
});

const industryAverage = computed(() => {
  if (!props.metrics.length) return 0;

  const total = props.metrics.reduce((sum, metric) => {
    return sum + (metric.industry / metric.maxValue) * 100;
  }, 0);

  return Math.round(total / props.metrics.length);
});
</script>

<template>
  <div>
    <!-- Overall scores -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-primary-50 rounded-lg p-4 text-center">
        <h3 class="text-sm font-medium text-gray-600 mb-1">Your Score</h3>
        <div class="text-3xl font-bold text-primary-700">{{ averageScore }}%</div>
      </div>

      <template v-for="(competitor, index) in competitors" :key="index">
        <div class="bg-gray-50 rounded-lg p-4 text-center">
          <h3 class="text-sm font-medium text-gray-600 mb-1">{{ competitor.name }}</h3>
          <div class="text-3xl font-bold text-gray-700">{{ competitorAverages[index] }}%</div>
        </div>
      </template>

      <div class="bg-gray-50 rounded-lg p-4 text-center">
        <h3 class="text-sm font-medium text-gray-600 mb-1">Industry Average</h3>
        <div class="text-3xl font-bold text-gray-700">{{ industryAverage }}%</div>
      </div>
    </div>

    <!-- Detailed metrics -->
    <div class="space-y-6">
      <div v-for="(metric, index) in metrics" :key="index" class="border-b border-gray-200 pb-6">
        <div class="flex justify-between items-center mb-2">
          <h3 class="font-medium">{{ metric.name }}</h3>
          <div class="text-gray-500 text-sm">Max: {{ metric.maxValue }}</div>
        </div>

        <!-- Your business -->
        <div class="mb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="text-sm font-medium">{{ businessName }}</div>
            <div class="text-sm">{{ metric.yourScore }} / {{ metric.maxValue }}</div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div
              class="h-2.5 rounded-full transition-all duration-500"
              :class="getScoreColor(metric.yourScore, metric)"
              :style="`width: ${(metric.yourScore / metric.maxValue) * 100}%`"
            ></div>
          </div>
        </div>

        <!-- Competitors -->
        <div v-for="(score, compIndex) in metric.competitorScores" :key="compIndex" class="mb-4">
          <div class="flex justify-between items-center mb-1">
            <div class="text-sm font-medium">{{ getCompetitorName(compIndex) }}</div>
            <div class="text-sm">{{ score }} / {{ metric.maxValue }}</div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div
              class="h-2.5 rounded-full transition-all duration-500"
              :class="getScoreColor(score, metric)"
              :style="`width: ${(score / metric.maxValue) * 100}%`"
            ></div>
          </div>
        </div>

        <!-- Industry average -->
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
</template>
