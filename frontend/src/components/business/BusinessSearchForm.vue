<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useComparisonStore } from '@/stores/comparisonStore';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';

const store = useComparisonStore();
const router = useRouter();

const userBusinessIdentifier = ref('');
const enableCompetitorsType = ref(false);
const competitorType = ref('');
const reportStyle = ref<'casual' | 'data-driven'>('casual');

const validateForm = (): boolean => {
  if (!userBusinessIdentifier.value.trim()) {
    store.error = 'Please enter a business identifier.';
    return false;
  }

//   if (searchType.value === 'name' && !businessName.value.trim()) {
//     store.error = 'Please enter a business name'
//     return false
//   }

//   if (searchType.value === 'website' && !businessWebsite.value.trim()) {
//     store.error = 'Please enter a business website'
//     return false
//   }

//   if (searchType.value === 'website' && !isValidUrl(businessWebsite.value)) {
//     store.error = 'Please enter a valid website URL'
//     return false
//   }

  return true
}

const isValidUrl = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

async function submitComparisonRequest() {
  if (!validateForm()) return;

  await store.fetchComparisonReport({
    user_business_identifier: userBusinessIdentifier.value,
    report_style: reportStyle.value
  });
  if (store.report && !store.error) {
    // Navigate to comparison view to show detailed comparison first
    router.push({ name: 'comparison' });
  }
}

</script>

<template>
  <div class="bg-white p-6 rounded-xl shadow-lg max-w-2xl animate-fade-in">
    <h3 class="text-xl font-semibold text-gray-800 mb-4">Find Your Business</h3>

    <form @submit.prevent="submitComparisonRequest" class="input-form">
    <div class="mb-4">
      <!-- <div class="flex space-x-4 mb-4">
        <div class="flex items-center">
          <input
            id="search-by-name"
            type="radio"
            v-model="searchType"
            value="name"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500"
          />
          <label for="search-by-name" class="ml-2 text-gray-700">Search by name</label>
        </div>
        <div class="flex items-center">
          <input
            id="search-by-website"
            type="radio"
            v-model="searchType"
            value="website"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500"
          />
          <label for="search-by-website" class="ml-2 text-gray-700">Search by website</label>
        </div>
      </div> -->

      <!-- <div v-if="searchType === 'name'" class="mb-4">
        <label for="business-name" class="block text-md font-medium text-gray-700 mb-1">Business Name</label>
        <input
          type="text"
          id="business-name"
          v-model="businessName"
          placeholder="e.g., Joe's Pizza"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>

      <div v-if="searchType === 'website'" class="mb-4">
        <label for="business-website" class="block text-md font-medium text-gray-700 mb-1">Business Website</label>
        <input
          type="url"
          id="business-website"
          v-model="businessWebsite"
          placeholder="e.g., https://example.com"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div> -->
      <div class="mb-4">
        <label for="business-identifier" class="block text-md font-medium text-gray-700 mb-1">Business Name</label>
        <input
          type="text"
          id="business-identifier"
          v-model="userBusinessIdentifier"
          placeholder="e.g., Joe's Pizza or https://your-restaurant.com"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>
      <p v-if="store.error" class="text-error-600 text-sm mt-1">{{ store.error }}</p>
    </div>

    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <label class="text-md font-medium text-gray-700">Select competitor type (Not implemented yet)</label>
        <div class="relative inline-block w-12 h-6 transition duration-200 ease-in-out">
          <input
            type="checkbox"
            v-model="enableCompetitorsType"
            class="peer sr-only"
            id="competitor-switch"
          />
          <label
            for="competitor-switch"
            class="block h-6 bg-gray-200 peer-checked:bg-primary-600 rounded-full cursor-pointer transition-colors duration-300"
          >
            <span
              class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform duration-300 transform peer-checked:translate-x-6"
            ></span>
          </label>
        </div>
      </div>

      <div v-if="enableCompetitorsType" class="animate-fade-in">
        <label class="block text-md font-medium text-gray-700 mb-2">Find competitors by:</label>
        <div class="flex space-x-4">
          <div class="flex items-center">
            <input
              id="nearby-competitors"
              type="radio"
              v-model="competitorType"
              value="nearby"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500"
            />
            <label for="nearby-competitors" class="ml-2 text-gray-700">Nearby businesses</label>
          </div>
          <div class="flex items-center">
            <input
              id="similar-competitors"
              type="radio"
              v-model="competitorType"
              value="similar"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500"
            />
            <label for="similar-competitors" class="ml-2 text-gray-700">Similar businesses</label>
          </div>
        </div>
      </div>
    </div>

    <div class="mb-6">
      <label class="block text-md font-medium text-gray-700 mb-4">Report Style</label>
      <div class="flex space-x-4">
        <div class="flex items-center">
          <input
            id="casual-style"
            type="radio"
            v-model="reportStyle"
            value="casual"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500"
          />
          <label for="casual-style" class="ml-2 text-gray-700">
            <span class="font-medium">Casual</span>
            <span class="text-sm text-gray-500 block">Friendly, easy-to-understand</span>
          </label>
        </div>
        <div class="flex items-center">
          <input
            id="data-driven-style"
            type="radio"
            v-model="reportStyle"
            value="data-driven"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500"
          />
          <label for="data-driven-style" class="ml-2 text-gray-700">
            <span class="font-medium">Data-driven</span>
            <span class="text-sm text-gray-500 block">Analytical, metrics-focused</span>
          </label>
        </div>
      </div>
    </div>

    <button type="submit"
      class="w-full btn btn-primary flex items-center justify-center"
      :disabled="store.isLoading"
    >
      <i v-if="store.isLoading" class="pi pi-spin pi-spinner mr-2"></i>
      <span v-if="!store.isLoading">Get Insights</span>
      <span v-else>Analyzing...</span>
    </button>
    </form>

    <LoadingSpinner v-if="store.isLoading" />
    <ErrorMessage v-if="store.error" :message="store.error" />
  </div>
</template>
