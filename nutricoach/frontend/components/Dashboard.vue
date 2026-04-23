<template>
  <div class="dashboard">
    <aside class="sidebar">
      <div class="brand">NutriCoach AI</div>
      <nav>
        <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/setup" class="nav-link">Profile</router-link>
        <router-link to="/meal-plan" class="nav-link">Meal Plan</router-link>
        <router-link to="/tracker" class="nav-link">Food Tracker</router-link>
        <a href="#" class="nav-link" @click.prevent="logout">Logout</a>
      </nav>
    </aside>

    <main class="main-content">
      <div v-if="summary" class="dashboard-grid">
        <!-- Welcome Card -->
        <div class="card welcome-card">
          <h2>Welcome back, {{ summary.name || 'there' }}!</h2>
          <p>Goal: <strong>{{ formatGoal(summary.goal) }}</strong></p>
        </div>

        <!-- Health Stats -->
        <div class="card stats-card">
          <h3>Health Stats</h3>
          <div class="stats-row">
            <div class="stat">
              <span class="stat-val">{{ summary.bmi || '--' }}</span>
              <span class="stat-label">BMI</span>
            </div>
            <div class="stat">
              <span class="stat-val">{{ summary.bmr || '--' }}</span>
              <span class="stat-label">BMR (kcal)</span>
            </div>
            <div class="stat">
              <span class="stat-val">{{ summary.target_calories || '--' }}</span>
              <span class="stat-label">Daily Target</span>
            </div>
            <div class="stat">
              <span class="stat-val">{{ summary.latest_weight || '--' }}</span>
              <span class="stat-label">Weight (kg)</span>
            </div>
          </div>
        </div>

        <!-- Calorie Progress -->
        <div class="card calorie-card">
          <h3>Today's Calories</h3>
          <div class="calorie-circle-wrapper">
            <div class="calorie-ring">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="#e0e0e0" stroke-width="10" fill="none"/>
                <circle cx="50" cy="50" r="40" :stroke="calorieColor" stroke-width="10" fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="circumference"
                  :stroke-dashoffset="dashOffset"
                  transform="rotate(-90 50 50)" />
              </svg>
              <div class="calorie-center">
                <span class="consumed">{{ summary.consumed_calories }}</span>
                <span class="label">kcal</span>
              </div>
            </div>
            <div class="calorie-details">
              <p>Target: <strong>{{ summary.target_calories }} kcal</strong></p>
              <p>Remaining: <strong :class="remaining < 0 ? 'over' : 'under'">{{ summary.remaining_calories }} kcal</strong></p>
            </div>
          </div>
        </div>

        <!-- Goal Progress -->
        <div class="card progress-card">
          <h3>Goal Progress</h3>
          <div class="progress-bar-wrap">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: (summary.goal_progress_percent || 0) + '%' }"></div>
            </div>
            <span>{{ summary.goal_progress_percent || 0 }}%</span>
          </div>
          <p class="progress-hint">Keep it up! Log your weight daily to track progress.</p>
        </div>

        <!-- Weight Chart -->
        <div class="card chart-card" v-if="weightHistory.length > 1">
          <h3>Weight History</h3>
          <Line :data="weightChartData" :options="chartOptions" />
        </div>
        <div class="card chart-card" v-else>
          <h3>Weight History</h3>
          <p class="empty-chart">Log your weight in the Food Tracker to see your trend here.</p>
        </div>

        <!-- Quick Links -->
        <div class="card quick-links-card">
          <h3>Quick Actions</h3>
          <router-link to="/meal-plan" class="quick-link-btn">View Meal Plan</router-link>
          <router-link to="/tracker" class="quick-link-btn">Log Meal</router-link>
          <router-link to="/setup" class="quick-link-btn">Update Profile</router-link>
        </div>
      </div>

      <div v-else class="loading">
        <p>Loading dashboard...</p>
      </div>
    </main>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import api from '../src/api'
import { useAuthStore } from '../src/stores/auth'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default {
  components: { Line },
  data() {
    return {
      summary: null,
      weightHistory: [],
      circumference: 2 * Math.PI * 40,
      chartOptions: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: false } }
      }
    }
  },
  computed: {
    caloriePercent() {
      if (!this.summary) return 0
      return Math.min((this.summary.consumed_calories / this.summary.target_calories) * 100, 100)
    },
    dashOffset() {
      return this.circumference - (this.caloriePercent / 100) * this.circumference
    },
    calorieColor() {
      return this.caloriePercent > 100 ? '#f44336' : this.caloriePercent > 80 ? '#FF9800' : '#4CAF50'
    },
    remaining() {
      return this.summary ? this.summary.remaining_calories : 0
    },
    weightChartData() {
      return {
        labels: this.weightHistory.map(w => w.date),
        datasets: [{
          label: 'Weight (kg)',
          data: this.weightHistory.map(w => w.weight),
          fill: false,
          borderColor: '#4CAF50',
          tension: 0.3,
          pointBackgroundColor: '#4CAF50'
        }]
      }
    }
  },
  mounted() {
    this.loadSummary()
    this.loadWeightHistory()
  },
  methods: {
    async loadSummary() {
      try {
        const res = await api.get('/dashboard/summary')
        this.summary = res.data
      } catch (e) {
        console.error('Failed to load summary:', e)
      }
    },
    async loadWeightHistory() {
      try {
        const res = await api.get('/weight/history')
        this.weightHistory = res.data.history
      } catch (e) {
        console.error('Failed to load weight history:', e)
      }
    },
    formatGoal(goal) {
      if (!goal) return 'Not set'
      return goal.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    logout() {
      const auth = useAuthStore()
      auth.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.dashboard { display: flex; min-height: 100vh; font-family: Arial, sans-serif; background: #f5f5f5; }
.sidebar {
  width: 200px;
  background: #2e7d32;
  color: white;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}
.brand { font-size: 1.1rem; font-weight: bold; margin-bottom: 20px; }
.nav-link {
  display: block;
  padding: 10px 12px;
  border-radius: 6px;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 0.9rem;
  transition: background 0.2s;
}
.nav-link:hover, .nav-link.router-link-active { background: rgba(255,255,255,0.2); color: white; }
.main-content { flex: 1; padding: 30px; overflow-y: auto; }
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.welcome-card { grid-column: 1 / -1; }
.welcome-card h2 { margin: 0 0 6px 0; color: #333; }
.welcome-card p { margin: 0; color: #666; }
h3 { margin: 0 0 12px 0; color: #444; font-size: 1rem; }
.stats-row { display: flex; gap: 16px; flex-wrap: wrap; }
.stat { flex: 1; text-align: center; min-width: 80px; }
.stat-val { display: block; font-size: 1.5rem; font-weight: bold; color: #2e7d32; }
.stat-label { display: block; font-size: 0.75rem; color: #888; }
.calorie-circle-wrapper { display: flex; align-items: center; gap: 20px; }
.calorie-ring { position: relative; width: 120px; flex-shrink: 0; }
.calorie-ring svg { width: 100%; }
.calorie-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.consumed { display: block; font-size: 1.3rem; font-weight: bold; color: #333; }
.calorie-center .label { font-size: 0.7rem; color: #888; }
.calorie-details p { margin: 4px 0; font-size: 0.9rem; color: #555; }
.over { color: #f44336; }
.under { color: #2e7d32; }
.progress-bar-wrap { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.progress-bar { flex: 1; background: #e0e0e0; border-radius: 8px; height: 14px; overflow: hidden; }
.progress-fill { background: #4CAF50; height: 100%; border-radius: 8px; transition: width 0.4s; }
.progress-hint { color: #888; font-size: 0.8rem; margin: 0; }
.chart-card { grid-column: 1 / -1; }
.empty-chart { color: #999; text-align: center; padding: 20px; }
.quick-links-card { display: flex; flex-direction: column; gap: 10px; }
.quick-link-btn {
  display: block;
  padding: 10px 14px;
  background: #e8f5e9;
  color: #2e7d32;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.9rem;
  text-align: center;
  font-weight: bold;
}
.quick-link-btn:hover { background: #c8e6c9; }
.loading { text-align: center; padding: 80px; color: #999; }
@media (max-width: 700px) {
  .sidebar { width: 100%; flex-direction: row; flex-wrap: wrap; padding: 12px; }
  .dashboard-grid { grid-template-columns: 1fr; }
  .welcome-card, .chart-card { grid-column: 1; }
}
</style>
