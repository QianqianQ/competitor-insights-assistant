<template>
  <footer class="bg-white border-t border-gray-200 py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4 md:mb-0">
          <p class="text-gray-500 text-sm">
            © {{ new Date().getFullYear() }} Competitor Insights Assistant. All rights reserved.
          </p>
        </div>
        <div class="flex space-x-6">
          <a href="#" class="text-gray-500 hover:text-primary-600 transition-colors">
            <span class="sr-only">Terms</span>
            <span class="text-sm">Terms of Service</span>
          </a>
          <a href="#" class="text-gray-500 hover:text-primary-600 transition-colors">
            <span class="sr-only">Privacy</span>
            <span class="text-sm">Privacy Policy</span>
          </a>
          <a href="#" class="text-gray-500 hover:text-primary-600 transition-colors">
            <span class="sr-only">Contact</span>
            <span class="text-sm">Contact Us</span>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>
