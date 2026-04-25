import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    mode: localStorage.getItem('theme') || 'auto'
  }),

  getters: {
    isDark: (state) => {
      if (state.mode === 'dark') return true
      if (state.mode === 'light') return false
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    },
    currentMode: (state) => state.mode
  },

  actions: {
    setTheme(mode) {
      this.mode = mode
      localStorage.setItem('theme', mode)
      this.applyTheme()
    },
    toggle() {
      const next = this.isDark ? 'light' : 'dark'
      this.setTheme(next)
    },
    applyTheme() {
      const dark = this.isDark
      document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
    },
    init() {
      this.applyTheme()
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (this.mode === 'auto') this.applyTheme()
      })
    }
  }
})
