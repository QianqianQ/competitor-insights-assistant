<script setup lang="ts">
import { ref } from 'vue'

const insights = ref([
  {
    id: 1,
    category: 'Reviews',
    insight: 'Response rate is 45% lower than top competitors',
    action: 'Set up a system to respond to all new reviews within 24 hours',
    competitorComparison: 'Top competitors respond to 95% of reviews'
  },
  {
    id: 2,
    category: 'Photos',
    insight: 'Your profile has 8 photos vs. competitor average of 24',
    action: 'Add 15+ high-quality photos showcasing your business, products, and team',
    competitorComparison: 'Businesses with 20+ photos get 35% more clicks'
  },
  {
    id: 3,
    category: 'Business Hours',
    insight: 'Hours accuracy score is 70% vs. competitor average of 98%',
    action: 'Update your business hours and add special holiday hours',
    competitorComparison: 'Incorrect hours is the #1 customer complaint for local businesses'
  },
  {
    id: 4,
    category: 'Keywords',
    insight: 'Missing key search terms that competitors rank for',
    action: 'Update business description to include terms: "artisanal", "authentic", "family-owned"',
    competitorComparison: 'Top competitor appears in 40% more relevant searches'
  }
]);

const getCategoryIcon = (category: string) => {
  switch(category.toLowerCase()) {
    case 'reviews': return 'pi-star';
    case 'photos': return 'pi-camera';
    case 'business hours': return 'pi-clock';
    case 'keywords': return 'pi-search';
    default: return 'pi-info-circle';
  }
};

const getCategoryColor = (category: string) => {
  switch(category.toLowerCase()) {
    case 'reviews': return 'bg-yellow-100 text-yellow-600';
    case 'photos': return 'bg-blue-100 text-blue-600';
    case 'business hours': return 'bg-green-100 text-green-600';
    case 'keywords': return 'bg-purple-100 text-purple-600';
    default: return 'bg-gray-100 text-gray-600';
  }
};
</script>

<template>
  <div class="card">
    <h2 class="text-xl font-semibold mb-6">Actionable Insights</h2>

    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Insight</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recommended Action</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Competitor Comparison</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="insight in insights" :key="insight.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div :class="`w-8 h-8 rounded-full flex items-center justify-center mr-2 ${getCategoryColor(insight.category)}`">
                  <i :class="`pi ${getCategoryIcon(insight.category)}`"></i>
                </div>
                <span class="font-medium">{{ insight.category }}</span>
              </div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900">{{ insight.insight }}</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900">{{ insight.action }}</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-500">{{ insight.competitorComparison }}</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
