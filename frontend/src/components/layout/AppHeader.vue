<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const mobileMenuOpen = ref(false);

const navigateTo = (route: string) => {
  router.push(route);
  mobileMenuOpen.value = false;
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
}
</script>

<template>
  <header class="bg-white shadow-sm sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="flex items-center">
              <span class="text-primary-700 text-xl font-bold">Business Profile Comparator</span>
            </router-link>
          </div>

          <!-- Desktop Navigation -->
          <nav class="hidden md:ml-10 md:flex md:space-x-8">
            <router-link
              to="/"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-primary-500 transition-all duration-300"
              active-class="border-primary-500 text-primary-600"
            >
              Home
            </router-link>
            <!-- <router-link
              to="/comparison"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-primary-500 transition-all duration-300"
              active-class="border-primary-500 text-primary-600"
            >
              Comparison
            </router-link>
            <router-link
              to="/report"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-primary-500 transition-all duration-300"
              active-class="border-primary-500 text-primary-600"
            >
              Reports
            </router-link> -->
          </nav>
        </div>

        <!-- Mobile menu button -->
        <div class="flex items-center md:hidden">
          <button
            @click="toggleMobileMenu"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
          >
            <span class="sr-only">Open main menu</span>
            <i v-if="!mobileMenuOpen" class="pi pi-bars text-xl"></i>
            <i v-else class="pi pi-times text-xl"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileMenuOpen" class="md:hidden animate-fade-in">
      <div class="pt-2 pb-3 space-y-1 bg-white shadow-lg">
        <a
          @click="navigateTo('/')"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-primary-600 cursor-pointer"
          :class="{ 'bg-primary-50 text-primary-600': $route.path === '/' }"
        >
          Home
        </a>
        <a
          @click="navigateTo('/comparison')"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-primary-600 cursor-pointer"
          :class="{ 'bg-primary-50 text-primary-600': $route.path === '/comparison' }"
        >
          Comparison
        </a>
        <a
          @click="navigateTo('/report')"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-primary-600 cursor-pointer"
          :class="{ 'bg-primary-50 text-primary-600': $route.path === '/report' }"
        >
          Reports
        </a>
      </div>
    </div>
  </header>
</template>