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
h1 { color: #22c55e; margin: 0; }
nav { display: flex; gap: 16px; }
nav a { color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color var(--transition-base); }
nav a:hover { color: #22c55e; }
.hero {
  text-align: center;
  padding: 50px 20px;
}
.hero h2 { color: var(--text-primary); margin-bottom: 12px; transition: color var(--transition-slow); }
.hero > p { color: var(--text-secondary); max-width: 500px; margin: 0 auto 30px; transition: color var(--transition-slow); }
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
  background: var(--bg-card);
  padding: 20px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-slow);
}
.feature:hover { box-shadow: var(--shadow-md); transform: translateY(-3px); }
.feature h3 { color: #22c55e; margin: 0 0 8px 0; font-size: 1rem; }
.feature p { color: var(--text-secondary); font-size: 0.85rem; margin: 0; transition: color var(--transition-slow); }
.cta-btn {
  display: inline-block;
  padding: 14px 36px;
  background: var(--text-primary);
  color: var(--bg-card);
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: bold;
  transition: all var(--transition-base);
}
.cta-btn:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
@media (max-width: 600px) {
  .landing-page { padding: 10px; }
  .hero { padding: 30px 10px; }
  .features { flex-direction: column; align-items: center; }
}
</style>
