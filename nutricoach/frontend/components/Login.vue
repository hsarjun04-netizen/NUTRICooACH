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
  background: var(--bg-card);
  padding: 40px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  width: 100%;
  max-width: 400px;
  transition: all var(--transition-slow);
}
h2 { text-align: center; color: var(--text-primary); margin-bottom: 24px; transition: color var(--transition-slow); }
.form-group { margin-bottom: 16px; }
label { display: block; margin-bottom: 4px; color: var(--text-secondary); font-size: 0.9rem; transition: color var(--transition-slow); }
input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 1rem;
  box-sizing: border-box;
  background: var(--bg-input);
  color: var(--text-primary);
  transition: all var(--transition-base);
}
input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(163, 230, 53, 0.15); outline: none; }
button {
  width: 100%;
  padding: 12px;
  background: var(--text-primary);
  color: var(--bg-card);
  border: none;
  border-radius: var(--radius-sm);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  transition: all var(--transition-base);
}
button:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.error { color: #ef4444; font-size: 0.9rem; margin: 8px 0; }
.alt-link { text-align: center; margin-top: 16px; color: var(--text-muted); transition: color var(--transition-slow); }
.alt-link a { color: #22c55e; text-decoration: none; font-weight: 600; }
</style>
