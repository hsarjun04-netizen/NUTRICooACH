<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Login to NutriCoach AI</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="email" required placeholder="your@email.com" />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required placeholder="Your password" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">{{ loading ? 'Logging in...' : 'Login' }}</button>
      </form>
      <p class="alt-link">Don't have an account? <router-link to="/register">Register</router-link></p>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../src/stores/auth'

export default {
  data() {
    return { email: '', password: '', error: '', loading: false }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      try {
        const auth = useAuthStore()
        await auth.login(this.email, this.password)
        this.$router.push('/dashboard')
      } catch (e) {
        this.error = e.response?.data?.error || 'Login failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5f5;
  font-family: Arial, sans-serif;
}
.auth-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}
h2 { text-align: center; color: #333; margin-bottom: 24px; }
.form-group { margin-bottom: 16px; }
label { display: block; margin-bottom: 4px; color: #555; font-size: 0.9rem; }
input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 8px;
}
button:hover { background-color: #45a049; }
button:disabled { background-color: #a5d6a7; cursor: not-allowed; }
.error { color: #e53935; font-size: 0.9rem; margin: 8px 0; }
.alt-link { text-align: center; margin-top: 16px; color: #666; }
.alt-link a { color: #4CAF50; text-decoration: none; }
</style>
