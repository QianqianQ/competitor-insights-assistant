<template>
  <div v-if="message" class="error-message-banner">
    <p>{{ message }}</p>
    <button @click="clearError" class="close-button">&times;</button>
  </div>
</template>

<script setup lang="ts">
import { useComparisonStore } from '@/stores/comparisonStore';

interface Props {
  message: string | null;
}

defineProps<Props>();

const store = useComparisonStore();

function clearError() {
  store.error = null;
}
</script>

<style scoped>
.error-message-banner {
  background-color: #f8d7da; /* Bootstrap danger background */
  color: #721c24; /* Bootstrap danger text */
  border: 1px solid #f5c6cb; /* Bootstrap danger border */
  padding: 15px 20px;
  border-radius: 8px;
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.error-message-banner p {
  margin: 0;
  font-size: 1em;
  font-weight: 500;
}

.close-button {
  background: none;
  border: none;
  color: #721c24;
  font-size: 1.5em;
  font-weight: bold;
  cursor: pointer;
  padding: 0 5px;
  line-height: 1;
}

.close-button:hover {
  opacity: 0.7;
}
</style>