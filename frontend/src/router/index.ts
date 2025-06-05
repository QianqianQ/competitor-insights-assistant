import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReportView from '../views/ReportView.vue'
import ComparisonView from '../views/ComparisonView.vue'
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
      path: '/comparison',
      name: 'comparison',
      component: ComparisonView,
      beforeEnter: (to: any, from: any, next: any) => {
        // Guard to ensure comparison page is only accessible if a report exists
        const store = useComparisonStore();
        store.hasReport ? next() : next({ name: 'home' });
      },
    },
    {
      path: '/report',
      name: 'report',
      component: ReportView,
      beforeEnter: (to: any, from: any, next: any) => {
        const store = useComparisonStore();
        store.hasReport ? next() : next({ name: 'home' });
      },
    },
  ],
  // Move scrollBehavior here (as a root router option)
  scrollBehavior(to, from, savedPosition) {
    if (to.name === 'report') {
      return { top: 0, behavior: 'smooth' };  // Add smooth scrolling
    }
    return savedPosition || { top: 0 };
  }
})

export default router
