<script setup lang="ts">
import BusinessSearchForm from '../components/business/BusinessSearchForm.vue'
import FeatureCard from '../components/FeatureCard.vue'

</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
    <!-- Hero Section -->
    <section class="relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
        <div class="md:flex md:items-center md:justify-between">
          <div class="md:w-1/2 animate-slide-up">
            <h1 class="text-4xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-secondary-600">
              Boost Your Local Business Visibility
            </h1>
            <p class="text-lg md:text-xl mb-8 text-gray-600 leading-relaxed">
              Compare your business profile against local competitors and get AI-powered recommendations to improve your online presence.
            </p>
            <BusinessSearchForm />
          </div>
          <div class="hidden md:block md:w-1/2">
            <img
              src="https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
              alt="Business growth analysis"
              class="w-full h-auto rounded-2xl shadow-2xl animate-fade-in transform hover:scale-105 transition-transform duration-500"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-4xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-secondary-600">
          How It Works
        </h2>

        <div class="grid md:grid-cols-3 gap-12">
          <FeatureCard
            title="Enter Your Business"
            description="Start by entering your business name or website to create a profile baseline."
            icon="pi-search"
            color="primary"
          />

          <FeatureCard
            title="Compare Competitors"
            description="See how your business stacks up against similar local competitors."
            icon="pi-chart-bar"
            color="secondary"
          />

          <FeatureCard
            title="Get AI Recommendations"
            description="Receive personalized recommendations to improve your online visibility."
            icon="pi-lightbulb"
            color="accent"
          />
        </div>
      </div>
    </section>
  </div>
</template>
