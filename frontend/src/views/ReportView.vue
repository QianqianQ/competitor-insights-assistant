<template>
  <div class="results-view" v-if="store.report">
    <header class="results-header">
      <h1>Comparison Report</h1>
      <p>Insightful analysis of {{ store.report.user_business.name }} against its competitors.</p>
      <button @click="goBack" class="back-button">New Comparison</button>
    </header>

    <div v-if="store.isLoading" class="loading-section">
      <LoadingSpinner message="Loading report..." />
    </div>
    <div v-else-if="store.error" class="error-section">
      <ErrorMessage :message="store.error" />
    </div>

    <div v-else-if="store.report" class="report-content">
      <!-- User Business Profile -->
      <section class="business-section user-business-section">
        <h2>Your Business (Rank: {{ store.report.user_business.rank || 'N/A' }})</h2>
        <BusinessProfileCard :business="store.report.user_business" :is-user-business="true" />
      </section>

      <!-- AI Summary -->
      <section class="ai-summary-section card-style">
        <h2>AI-Powered Summary</h2>
        <p>{{ store.report.ai_comparison_summary }}</p>
      </section>

      <!-- AI Suggestions -->
      <section class="ai-suggestions-section card-style">
        <h2>Improvement Suggestions</h2>
        <ul>
          <li v-for="(suggestion, index) in store.report.ai_improvement_suggestions" :key="index">
            {{ suggestion }}
          </li>
        </ul>
      </section>

      <!-- Visual Comparison Charts -->
      <!-- <section class="charts-section card-style">
        <h2>Visual Comparison</h2>
        <div class="charts-grid">
          <ComparisonChart
            title="Average Customer Rating"
            :user-value="store.report.user_business.rating || 0"
            :user-label="store.report.user_business.name"
            :competitor-values="[]"
            :competitor-labels="[]"
            data-suffix=" / 5"
            :max-value="5"
           />
          <ComparisonChart
            title="Number of Reviews"
            :user-value="store.report.user_business.rating_count || 0"
            :user-label="store.report.user_business.name"
            :competitor-values="[]"
            :competitor-labels="[]"
          />
          <ComparisonChart
            title="Profile Completeness Score"
            :user-value="store.report.user_business.profile_score || 0"
            :user-label="store.report.user_business.name"
            :competitor-values="[]"
            :competitor-labels="[]"
            data-suffix=" / 1.0"
            :max-value="1"
           />
        </div>
      </section> -->

       <footer class="report-footer">
        <p>Report generated on: {{ new Date(store.report.created_at || Date.now()).toLocaleDateString() }}</p>
        <p v-if="store.report.metadata">LLM Provider: {{ store.report.metadata.llm_provider || 'N/A' }}, Model: {{ store.report.metadata.llm_model || 'N/A' }}</p>
      </footer>
    </div>

    <div v-else class="no-report-message">
        <p>No comparison report available. Please start a new comparison.</p>
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

function goBack() {
  store.clearReport();
  router.push({ name: 'home' });
}

// Ensure report is available, otherwise redirect (though router guard should handle this)
if (!store.report) {
  // router.push({ name: 'Input' }); // Can be redundant due to route guard
}
</script>

<style scoped>
.results-view {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.results-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.results-header h1 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 5px;
}

.results-header p {
  font-size: 1.1em;
  color: #666;
  margin-bottom: 15px;
}

.back-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #0056b3;
}

.report-content {
  display: grid;
  gap: 30px;
}

.business-section h2,
.ai-summary-section h2,
.ai-suggestions-section h2,
.charts-section h2 {
  font-size: 1.8em;
  color: #444;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #007bff;
}

.card-style {
  background-color: #fff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.user-business-section .card-style {
  border-left: 5px solid #007bff; /* Accent for user's business */
}

.ai-suggestions-section ul {
  list-style-type: none;
  padding-left: 0;
}

.ai-suggestions-section li {
  background-color: #e9f5ff;
  padding: 12px 15px;
  margin-bottom: 10px;
  border-radius: 6px;
  border-left: 4px solid #007bff;
  color: #333;
  font-size: 1em;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.loading-section, .error-section, .no-report-message {
  text-align: center;
  padding: 50px 20px;
}
.no-report-message p {
    font-size: 1.2em;
    color: #777;
}

.report-footer {
  margin-top: 40px;
  text-align: center;
  font-size: 0.9em;
  color: #888;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}
</style>