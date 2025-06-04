import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReportView from '../views/ReportView.vue'
import { useComparisonStore } from '@/stores/comparisonStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/report',
      name: 'report',
      component: ReportView,
      beforeEnter: (to: any, from: any, next: any) => {
        // Guard to ensure results page is only accessible if a report exists
        const store = useComparisonStore();
        if (store.hasReport) {
          next();
        } else {
          // If no report, redirect to input page
          next({ name: 'home' });
        }
      },
    },
  ],
})

export default router
