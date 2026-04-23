<template>
  <div class="landing-page">
    <header>
      <h1>NutriCoach AI</h1>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
        <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
        <router-link v-if="isLoggedIn" to="/dashboard">Dashboard</router-link>
        <a href="#" v-if="isLoggedIn" @click.prevent="logout">Logout</a>
      </nav>
    </header>
    <section class="hero">
      <h2>Personalized Diet Plans for Your Goals</h2>
      <p>Smart nutrition coaching powered by AI. Get custom meal plans, track your progress, and achieve your health goals.</p>
      <div class="features">
        <div class="feature">
          <h3>Smart Calculations</h3>
          <p>BMI, BMR, daily calorie needs computed automatically</p>
        </div>
        <div class="feature">
          <h3>AI Meal Plans</h3>
          <p>Personalized Indian meal plans for your diet type</p>
        </div>
        <div class="feature">
          <h3>Track Progress</h3>
          <p>Log meals, track weight, and visualize your journey</p>
        </div>
      </div>
      <router-link v-if="!isLoggedIn" to="/register" class="cta-btn">Get Started</router-link>
      <router-link v-else to="/dashboard" class="cta-btn">Go to Dashboard</router-link>
    </section>
  </div>
</template>

<script>
import { useAuthStore } from '../src/stores/auth'

export default {
  computed: {
    isLoggedIn() {
      const auth = useAuthStore()
      return auth.isLoggedIn
    }
  },
  methods: {
    logout() {
      const auth = useAuthStore()
      auth.logout()
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.landing-page {
  font-family: Arial, sans-serif;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}
h1 { color: #2e7d32; margin: 0; }
nav { display: flex; gap: 16px; }
nav a { color: #555; text-decoration: none; font-size: 0.95rem; }
nav a:hover { color: #2e7d32; }
.hero {
  text-align: center;
  padding: 50px 20px;
}
.hero h2 { color: #333; margin-bottom: 12px; }
.hero > p { color: #666; max-width: 500px; margin: 0 auto 30px; }
.features {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  justify-content: center;
}
.feature {
  flex: 1;
  min-width: 200px;
  max-width: 260px;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.feature h3 { color: #2e7d32; margin: 0 0 8px 0; font-size: 1rem; }
.feature p { color: #666; font-size: 0.85rem; margin: 0; }
.cta-btn {
  display: inline-block;
  padding: 14px 36px;
  background-color: #4CAF50;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: bold;
  transition: background 0.2s;
}
.cta-btn:hover { background-color: #45a049; }
@media (max-width: 600px) {
  .landing-page { padding: 10px; }
  .hero { padding: 30px 10px; }
  .features { flex-direction: column; align-items: center; }
}
</style>
