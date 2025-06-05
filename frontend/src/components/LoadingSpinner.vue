<template>
  <div class="loading-spinner-overlay">
    <div class="spinner"></div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message?: string;
}

defineProps<Props>();
</script>

<style scoped>
.loading-spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.spinner {
  border: 6px solid #f3f3f3; /* Light grey */
  border-top: 6px solid #007bff; /* Blue */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-spinner-overlay p {
  font-size: 1.1em;
  color: #333;
  font-weight: 500;
}
</style>
