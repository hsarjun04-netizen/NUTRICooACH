import { defineStore } from 'pinia'
import api from '../api'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null,
    healthProfile: null,
    dashboardSummary: null
  }),

  actions: {
    async fetchProfile() {
      const response = await api.get('/users/profile')
      this.profile = response.data
    },

    async updateProfile(data) {
      await api.put('/users/profile', data)
      this.profile = { ...this.profile, ...data }
    },

    async calculateHealth() {
      const response = await api.post('/health/calculate')
      this.healthProfile = response.data
      return response.data
    },

    async fetchHealthProfile() {
      const response = await api.get('/health/profile')
      this.healthProfile = response.data
    },

    async fetchDashboardSummary() {
      const response = await api.get('/dashboard/summary')
      this.dashboardSummary = response.data
      return response.data
    }
  }
})
