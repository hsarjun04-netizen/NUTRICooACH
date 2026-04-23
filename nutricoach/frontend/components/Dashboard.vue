<template>
  <div class="dashboard">
    <aside class="sidebar">
      <div class="brand">NutriCoach AI</div>
      <nav>
        <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/profile" class="nav-link">My Profile</router-link>
        <router-link to="/meal-plan" class="nav-link">Meal Plan</router-link>
        <router-link to="/tracker" class="nav-link">Food Tracker</router-link>
        <router-link to="/chat" class="nav-link">AI Coach</router-link>
        <router-link to="/progress" class="nav-link">Progress</router-link>
        <a href="#" class="nav-link" @click.prevent="logout">Logout</a>
      </nav>
    </aside>

    <main class="main-content">
      <div v-if="summary" class="dashboard-container">
        <!-- Header -->
        <div class="page-header">
          <div>
            <h1>Dashboard</h1>
            <p class="subtitle">Welcome back, {{ summary.name || 'there' }}!</p>
          </div>
          <div class="goal-badge">{{ formatGoal(summary.goal) }}</div>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
          <!-- Calories Card -->
          <div class="stat-card calories-card">
            <div class="stat-icon">&#127828;</div>
            <div class="stat-info">
              <span class="stat-label">Daily Calories</span>
              <span class="stat-value">{{ summary.consumed_calories }} <small>/ {{ summary.target_calories }} kcal</small></span>
            </div>
            <div class="progress-wrap">
              <div class="progress-bar">
                <div class="progress-fill" :class="calorieFillClass" :style="{ width: caloriePercent + '%' }"></div>
              </div>
              <span class="progress-text">{{ caloriePercent }}%</span>
            </div>
          </div>

          <!-- Water Card -->
          <div class="stat-card water-card">
            <div class="stat-icon">&#128167;</div>
            <div class="stat-info">
              <span class="stat-label">Water Intake</span>
              <span class="stat-value">{{ waterTotal }} <small>/ {{ waterGoal }} ml</small></span>
            </div>
            <div class="progress-wrap">
              <div class="progress-bar">
                <div class="progress-fill water-fill" :style="{ width: waterPercent + '%' }"></div>
              </div>
              <span class="progress-text">{{ waterPercent }}%</span>
            </div>
            <div class="water-actions">
              <button @click="addWater(250)" class="water-btn">+ 250ml</button>
              <button @click="addWater(500)" class="water-btn">+ 500ml</button>
            </div>
          </div>

          <!-- Weight Card -->
          <div class="stat-card weight-card">
            <div class="stat-icon">&#9878;</div>
            <div class="stat-info">
              <span class="stat-label">Current Weight</span>
              <span class="stat-value">{{ summary.latest_weight || '--' }} <small>kg</small></span>
            </div>
            <p class="stat-hint">{{ weightChangeText }}</p>
          </div>

          <!-- BMI Card -->
          <div class="stat-card bmi-card">
            <div class="stat-icon">&#10084;</div>
            <div class="stat-info">
              <span class="stat-label">BMI</span>
              <span class="stat-value">{{ summary.bmi || '--' }}</span>
            </div>
            <p class="stat-hint">{{ bmiStatus }}</p>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="section-title">Weekly Progress</div>
        <div class="chart-card">
          <div v-if="weeklyData.labels.length > 0" class="chart-wrap">
            <Bar :data="weeklyData" :options="barOptions" />
          </div>
          <div v-else class="empty-state">
            <p>Log your meals daily to see your weekly calorie chart.</p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="section-title">Quick Actions</div>
        <div class="actions-grid">
          <router-link to="/meal-plan" class="action-card">
            <span class="action-icon">&#127860;</span>
            <span class="action-text">View Meal Plan</span>
          </router-link>
          <router-link to="/tracker" class="action-card">
            <span class="action-icon">&#128221;</span>
            <span class="action-text">Log a Meal</span>
          </router-link>
          <router-link to="/chat" class="action-card">
            <span class="action-icon">&#128172;</span>
            <span class="action-text">Ask AI Coach</span>
          </router-link>
          <router-link to="/progress" class="action-card">
            <span class="action-icon">&#128200;</span>
            <span class="action-text">View Progress</span>
          </router-link>
        </div>
      </div>

      <div v-else class="loading">
        <p>Loading dashboard...</p>
      </div>
    </main>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import api from '../src/api'
import { useAuthStore } from '../src/stores/auth'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  components: { Bar },
  data() {
    return {
      summary: null,
      waterTotal: 0,
      waterGoal: 2500,
      weeklyData: { labels: [], datasets: [] },
      barOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    }
  },
  computed: {
    caloriePercent() {
      if (!this.summary || !this.summary.target_calories) return 0
      return Math.min(Math.round((this.summary.consumed_calories / this.summary.target_calories) * 100), 100)
    },
    calorieFillClass() {
      if (this.caloriePercent > 100) return 'over'
      if (this.caloriePercent > 80) return 'warning'
      return 'good'
    },
    waterPercent() {
      return Math.min(Math.round((this.waterTotal / this.waterGoal) * 100), 100)
    },
    bmiStatus() {
      const bmi = this.summary?.bmi
      if (!bmi) return 'Complete your profile to calculate BMI'
      if (bmi < 18.5) return 'Underweight'
      if (bmi < 25) return 'Healthy weight'
      if (bmi < 30) return 'Overweight'
      return 'Obese'
    },
    weightChangeText() {
      return this.summary?.latest_weight ? 'Keep tracking daily!' : 'Log your weight to track changes'
    }
  },
  mounted() {
    this.loadSummary()
    this.loadWater()
    this.loadWeeklyData()
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
    async loadWater() {
      try {
        const res = await api.get('/water/today')
        this.waterTotal = res.data.total_ml
      } catch (e) {
        console.error('Failed to load water:', e)
      }
    },
    async addWater(amount) {
      try {
        await api.post('/water/log', { amount_ml: amount })
        this.waterTotal += amount
      } catch (e) {
        console.error('Failed to log water:', e)
      }
    },
    async loadWeeklyData() {
      try {
        const res = await api.get('/meals/today')
        // Build simple weekly mock for demo; in production, fetch last 7 days
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        const todayIdx = new Date().getDay() - 1
        const orderedDays = [...days.slice(todayIdx + 1), ...days.slice(0, todayIdx + 1)]
        const values = orderedDays.map(() => Math.floor(Math.random() * 800 + 1200))
        values[6] = this.summary?.consumed_calories || 1500
        this.weeklyData = {
          labels: orderedDays,
          datasets: [{
            label: 'Calories',
            data: values,
            backgroundColor: '#4CAF50',
            borderRadius: 6
          }]
        }
      } catch (e) {
        console.error('Failed to load weekly data:', e)
      }
    },
    formatGoal(goal) {
      if (!goal) return 'No Goal Set'
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
.dashboard { display: flex; min-height: 100vh; font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; }
.sidebar {
  width: 210px;
  background: #fff;
  border-right: 1px solid #e0e0e0;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex-shrink: 0;
}
.brand { font-size: 1.15rem; font-weight: 800; color: #2e7d32; margin-bottom: 24px; letter-spacing: -0.3px; }
.nav-link {
  display: block;
  padding: 10px 14px;
  border-radius: 8px;
  color: #555;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}
.nav-link:hover, .nav-link.router-link-active { background: #e8f5e9; color: #2e7d32; }
.main-content { flex: 1; padding: 32px; overflow-y: auto; max-width: 1100px; }

.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.page-header h1 { margin: 0; font-size: 1.6rem; color: #1a1a2e; }
.subtitle { margin: 4px 0 0 0; color: #888; font-size: 0.95rem; }
.goal-badge {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 8px 18px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
}

.section-title { font-size: 1rem; font-weight: 700; color: #333; margin: 28px 0 14px 0; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }
.stat-card {
  background: white;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.stat-icon { font-size: 1.6rem; }
.stat-info { display: flex; flex-direction: column; gap: 2px; }
.stat-label { font-size: 0.8rem; color: #888; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-value { font-size: 1.4rem; font-weight: 700; color: #1a1a2e; }
.stat-value small { font-size: 0.85rem; color: #999; font-weight: 400; }
.stat-hint { margin: 0; font-size: 0.8rem; color: #aaa; }

.progress-wrap { display: flex; align-items: center; gap: 10px; }
.progress-bar { flex: 1; background: #f0f0f0; border-radius: 10px; height: 10px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 10px; transition: width 0.4s ease; }
.progress-fill.good { background: #4CAF50; }
.progress-fill.warning { background: #FF9800; }
.progress-fill.over { background: #f44336; }
.progress-fill.water-fill { background: #2196F3; }
.progress-text { font-size: 0.75rem; color: #999; font-weight: 600; min-width: 32px; text-align: right; }

.water-actions { display: flex; gap: 8px; }
.water-btn {
  flex: 1;
  padding: 8px;
  background: #e3f2fd;
  color: #1976d2;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.water-btn:hover { background: #bbdefb; }

.chart-card {
  background: white;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  height: 280px;
}
.chart-wrap { height: 100%; }
.empty-state { text-align: center; color: #bbb; padding: 40px; }

.actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; }
.action-card {
  background: white;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  text-decoration: none;
  color: #333;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: transform 0.15s, box-shadow 0.15s;
}
.action-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.action-icon { font-size: 1.8rem; }
.action-text { font-size: 0.85rem; font-weight: 600; }

.loading { text-align: center; padding: 80px; color: #999; }

@media (max-width: 700px) {
  .dashboard { flex-direction: column; }
  .sidebar { width: 100%; flex-direction: row; flex-wrap: wrap; padding: 12px; border-right: none; border-bottom: 1px solid #e0e0e0; }
  .brand { margin-bottom: 8px; width: 100%; }
  .main-content { padding: 20px; }
}
</style>
