<template>
  <div id="app">
    <nav v-if="showNav" class="top-nav">
      <button class="back-btn" @click="goBack">
        <span class="arrow">&#8592;</span> Back
      </button>
      <span class="nav-title">NutriCoach AI</span>
      <span class="nav-spacer"></span>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    showNav() {
      return this.$route.path !== '/'
    }
  },
  methods: {
    goBack() {
      if (window.history.length > 1) {
        this.$router.back()
      } else {
        this.$router.push('/')
      }
    }
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f5f5f5;
}
.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #2e7d32;
  color: white;
  padding: 12px 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.back-btn {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}
.back-btn:hover {
  background: rgba(255,255,255,0.35);
}
.arrow {
  font-size: 1.1rem;
}
.nav-title {
  font-weight: bold;
  font-size: 1.1rem;
}
.nav-spacer {
  width: 80px;
}
@media (max-width: 500px) {
  .nav-title { font-size: 0.95rem; }
  .back-btn { padding: 6px 10px; font-size: 0.85rem; }
}
</style>
