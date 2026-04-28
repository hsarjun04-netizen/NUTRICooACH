import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../components/LandingPage.vue') },
  { path: '/login', component: () => import('../components/Login.vue') },
  { path: '/register', component: () => import('../components/Register.vue') },
  { path: '/setup', component: () => import('../components/ProfileSetup.vue'), meta: { requiresAuth: true } },
  { path: '/profile', component: () => import('../components/Profile.vue'), meta: { requiresAuth: true } },
  { path: '/dashboard', component: () => import('../components/Dashboard.vue'), meta: { requiresAuth: true } },
  { path: '/meal-plan', component: () => import('../components/MealPlan.vue'), meta: { requiresAuth: true } },
  { path: '/tracker', component: () => import('../components/FoodTracker.vue'), meta: { requiresAuth: true } },
  { path: '/recipes', component: () => import('../components/Recipes.vue'), meta: { requiresAuth: true } },

  { path: '/exercises', component: () => import('../components/ExerciseTracker.vue'), meta: { requiresAuth: true } },
  { path: '/progress', component: () => import('../components/Progress.vue'), meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
