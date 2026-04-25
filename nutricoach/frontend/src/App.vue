<template>
  <div id="app" :class="{ 'dark-mode': theme.isDark }">
    <nav v-if="showNav" class="top-nav">
      <button class="back-btn" @click="goBack">
        <span class="arrow">&#8592;</span>
        <span>Back</span>
      </button>
      <span class="nav-title">NutriCoach AI</span>
      <div class="nav-actions">
        <button class="theme-toggle" @click="theme.toggle" :title="theme.isDark ? 'Switch to light' : 'Switch to dark'">
          <span v-if="theme.isDark">&#9788;</span>
          <span v-else>&#9790;</span>
        </button>
      </div>
    </nav>
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import { useThemeStore } from './stores/theme.js'

export default {
  name: 'App',
  setup() {
    const theme = useThemeStore()
    return { theme }
  },
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
/* ===== CSS VARIABLES ===== */
:root {
  --bg-body: #f1f5f9;
  --bg-card: #ffffff;
  --bg-sidebar: #1e293b;
  --bg-input: #ffffff;
  --bg-hover: #f8fafc;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --border-color: #e2e8f0;
  --accent: #a3e635;
  --accent-hover: #84cc16;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.12);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="dark"] {
  --bg-body: #0f172a;
  --bg-card: #1e293b;
  --bg-sidebar: #0f172a;
  --bg-input: #334155;
  --bg-hover: #283548;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --border-color: #334155;
  --accent: #a3e635;
  --accent-hover: #bef264;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.5);
}

/* ===== GLOBAL STYLES ===== */
* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg-body);
  color: var(--text-primary);
  transition: background var(--transition-slow), color var(--transition-slow);
  -webkit-font-smoothing: antialiased;
}

/* Scrollbar styling */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

/* Selection */
::selection { background: var(--accent); color: #1e293b; }

/* ===== TOP NAV ===== */
.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-card);
  color: var(--text-primary);
  padding: 12px 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
  transition: background var(--transition-slow), color var(--transition-slow);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.back-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all var(--transition-base);
}
.back-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
  transform: translateX(-2px);
}
.nav-title {
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: -0.5px;
}
.nav-actions { display: flex; gap: 8px; align-items: center; }
.theme-toggle {
  width: 36px; height: 36px; border-radius: 10px;
  border: 1px solid var(--border-color); background: var(--bg-card);
  color: var(--text-secondary); cursor: pointer; font-size: 1rem;
  display: flex; align-items: center; justify-content: center;
  transition: all var(--transition-base);
}
.theme-toggle:hover {
  background: var(--bg-hover); color: var(--text-primary);
  transform: rotate(15deg) scale(1.1);
  box-shadow: var(--shadow-md);
}

/* ===== PAGE TRANSITIONS ===== */
.page-enter-active,
.page-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.page-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.98);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.98);
}

/* ===== FOCUS STYLES ===== */
button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* ===== TOAST NOTIFICATIONS ===== */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.toast {
  padding: 14px 20px;
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  font-weight: 500;
  color: white;
  box-shadow: var(--shadow-lg);
  animation: toastIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) both;
  max-width: 320px;
  word-break: break-word;
}
.toast.toast-success { background: linear-gradient(135deg, #22c55e, #16a34a); }
.toast.toast-error { background: linear-gradient(135deg, #ef4444, #dc2626); }
.toast.toast-info { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.toast.toast-leave { animation: toastOut 0.3s cubic-bezier(0.4, 0, 0.2, 1) both; }
@keyframes toastIn {
  from { opacity: 0; transform: translateX(40px) scale(0.9); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes toastOut {
  from { opacity: 1; transform: translateX(0); }
  to { opacity: 0; transform: translateX(40px); }
}

@media (max-width: 500px) {
  .nav-title { font-size: 0.95rem; }
  .back-btn { padding: 6px 10px; font-size: 0.85rem; }
}
</style>
