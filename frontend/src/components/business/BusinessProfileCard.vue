<template>
  <div class="business-profile-card" :class="{ 'user-business': isUserBusiness }">
    <div class="card-header">
      <h3>{{ business.name }} <span v-if="business.rank">(Rank: {{ business.rank }})</span></h3>
      <p v-if="business.website" class="website-link">
        <a :href="business.website" target="_blank" rel="noopener noreferrer">{{ business.website }}</a>
      </p>
      <p v-if="business.address" class="address">{{ business.address }}</p>
    </div>

    <div class="card-body">
      <h4>Key Metrics:</h4>
      <ul>
        <li><strong>Rating:</strong> {{ business.rating?.toFixed(1) || 'N/A' }} / 5 ({{ business.rating_count || 0 }} reviews)</li>
        <li><strong>Images:</strong> {{ business.image_count || 0 }}</li>
        <li><strong>Category:</strong> {{ business.category || 'N/A' }}</li>
        <li><strong>Profile Score:</strong> {{ business.profile_score?.toFixed(2) || 'N/A' }} / 1.0</li>
      </ul>

      <h4>Profile Checklist:</h4>
      <ul class="checklist">
        <li :class="{ 'checked': business.has_hours }">Business Hours Listed</li>
        <li :class="{ 'checked': business.has_description }">Description Provided</li>
        <li :class="{ 'checked': business.has_menu_link }">Menu/Services Link</li>
        <li :class="{ 'checked': business.has_price_level }">Price Level Indicated</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DisplayBusinessProfile } from '@/types/comparison';

interface Props {
  business: DisplayBusinessProfile;
  isUserBusiness?: boolean;
}

defineProps<Props>();
</script>

<style scoped>
.business-profile-card {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
  height: 100%; /* Ensure cards in a grid take same height */
}

.business-profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.business-profile-card.user-business {
  border-left: 5px solid #007bff;
}

.card-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.card-header h3 {
  margin: 0 0 5px 0;
  font-size: 1.5em;
  color: #0056b3; /* Darker blue for emphasis */
}

.card-header h3 span {
  font-size: 0.8em;
  color: #555;
  font-weight: normal;
}

.website-link a {
  color: #007bff;
  text-decoration: none;
  font-size: 0.95em;
}
.website-link a:hover {
  text-decoration: underline;
}

.address {
  font-size: 0.9em;
  color: #777;
  margin-top: 5px;
}

.card-body h4 {
  font-size: 1.1em;
  color: #333;
  margin-top: 20px;
  margin-bottom: 10px;
}

.card-body ul {
  list-style-type: none;
  padding-left: 0;
  margin-bottom: 15px;
}

.card-body li {
  font-size: 0.95em;
  color: #555;
  padding: 6px 0;
  border-bottom: 1px dashed #f0f0f0;
}
.card-body li:last-child {
  border-bottom: none;
}

.checklist li {
  padding-left: 25px;
  position: relative;
}

.checklist li::before {
  content: '\2717'; /* Cross mark */
  color: #dc3545; /* Red */
  position: absolute;
  left: 0;
  font-weight: bold;
}

.checklist li.checked::before {
  content: '\2713'; /* Check mark */
  color: #28a745; /* Green */
}

.card-footer {
  margin-top: auto; /* Pushes footer to the bottom */
  padding-top: 15px;
  border-top: 1px solid #eee;
  text-align: right;
}
.card-footer small {
  font-size: 0.8em;
  color: #999;
}
</style>