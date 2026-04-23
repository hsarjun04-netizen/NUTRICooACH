import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../components/LandingPage.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import ProfileSetup from '../components/ProfileSetup.vue'
import Dashboard from '../components/Dashboard.vue'
import MealPlan from '../components/MealPlan.vue'
import FoodTracker from '../components/FoodTracker.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/setup', component: ProfileSetup, meta: { requiresAuth: true } },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/meal-plan', component: MealPlan, meta: { requiresAuth: true } },
  { path: '/tracker', component: FoodTracker, meta: { requiresAuth: true } }
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
