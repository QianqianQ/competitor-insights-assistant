<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import type { Business, ComparisonMetric } from '../../types'

Chart.register(...registerables)

const props = defineProps<{
  businessName: string;
  competitors: Business[];
  metrics: ComparisonMetric[];
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null)
const chart = ref<Chart | null>(null)

const createChart = () => {
  if (!chartCanvas.value || !props.metrics.length) return;

  // Destroy existing chart if it exists
  if (chart.value) {
    chart.value.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')
  if (!ctx) return;

  const labels = props.metrics.map(metric => metric.name);
  const yourData = props.metrics.map(metric => metric.yourScore);

  // Create datasets for competitors
  const competitorDatasets = props.competitors.map((competitor, index) => {
    return {
      label: competitor.name,
      data: props.metrics.map(metric => metric.competitorScores[index] || 0),
      backgroundColor: index === 0 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(139, 92, 246, 0.2)',
      borderColor: index === 0 ? 'rgb(16, 185, 129)' : 'rgb(139, 92, 246)',
      borderWidth: 2,
      tension: 0.1
    };
  });

  // Create dataset for industry average
  const industryData = {
    label: 'Industry Average',
    data: props.metrics.map(metric => metric.industry),
    backgroundColor: 'rgba(107, 114, 128, 0.2)',
    borderColor: 'rgb(107, 114, 128)',
    borderWidth: 2,
    borderDash: [5, 5],
    tension: 0.1
  };

  chart.value = new Chart(ctx, {
    type: 'radar',
    data: {
      labels,
      datasets: [
        {
          label: props.businessName,
          data: yourData,
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          borderColor: 'rgb(59, 130, 246)',
          borderWidth: 2,
          tension: 0.1
        },
        ...competitorDatasets,
        industryData
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          beginAtZero: true,
          min: 0,
          max: 100,
          ticks: {
            stepSize: 20
          }
        }
      }
    }
  });
};

onMounted(() => {
  createChart();
});

watch([() => props.competitors, () => props.metrics], () => {
  createChart();
}, { deep: true });
</script>

<template>
  <div class="h-[400px]">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>
