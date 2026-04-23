import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userId: localStorage.getItem('user_id') || null,
    name: localStorage.getItem('user_name') || null,
    user: null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    async register(name, email, password) {
      const response = await api.post('/auth/register', { name, email, password })
      this.token = response.data.token
      this.userId = response.data.user_id
      localStorage.setItem('token', this.token)
      localStorage.setItem('user_id', this.userId)
      await this.fetchUser()
    },

    async login(email, password) {
      const response = await api.post('/auth/login', { email, password })
      this.token = response.data.token
      this.userId = response.data.user_id
      this.name = response.data.name
      localStorage.setItem('token', this.token)
      localStorage.setItem('user_id', this.userId)
      localStorage.setItem('user_name', this.name)
      await this.fetchUser()
    },

    async fetchUser() {
      try {
        const response = await api.get('/auth/me')
        this.user = response.data
        this.name = response.data.name
        localStorage.setItem('user_name', this.name)
      } catch (e) {
        this.logout()
      }
    },

    logout() {
      this.token = null
      this.userId = null
      this.name = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user_name')
    }
  }
})
