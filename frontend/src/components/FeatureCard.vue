<script setup lang="ts">
defineProps<{
  title: string;
  description: string;
  icon: string;
  color: 'primary' | 'secondary' | 'accent';
}>();

const getColorClass = (color: string) => {
  const colorMap = {
    primary: 'bg-primary-100 text-primary-600',
    secondary: 'bg-secondary-100 text-secondary-600',
    accent: 'bg-accent-100 text-accent-600'
  };

  return colorMap[color as keyof typeof colorMap] || colorMap.primary;
};
</script>

<template>
  <div class="group bg-white/50 backdrop-blur-sm rounded-2xl p-8 hover:bg-white hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2">
    <div class="flex flex-col items-center text-center">
      <div
        :class="`w-16 h-16 rounded-2xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-all duration-500 ${getColorClass(color)}`"
      >
        <i :class="`pi ${icon} text-3xl`"></i>
      </div>
      <h3 class="text-2xl font-semibold mb-4 text-gray-800">{{ title }}</h3>
      <p class="text-gray-600 leading-relaxed">{{ description }}</p>
    </div>
  </div>
</template>
