<template>
  <div class="progress-page">
    <div class="progress-container">
      <div class="page-header">
        <h1>Your Progress</h1>
        <p class="subtitle">Track your weight journey and celebrate milestones</p>
      </div>

      <!-- Summary Stats -->
      <div class="stats-row">
        <div class="stat-card">
          <span class="stat-label">Starting Weight</span>
          <span class="stat-value">{{ startWeight || '--' }} <small>kg</small></span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Current Weight</span>
          <span class="stat-value">{{ latestWeight || '--' }} <small>kg</small></span>
        </div>
        <div class="stat-card" :class="weightChangeClass">
          <span class="stat-label">Change</span>
          <span class="stat-value">{{ weightChange > 0 ? '+' : ''}}{{ weightChange || '--' }} <small>kg</small></span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Goal Progress</span>
          <span class="stat-value">{{ goalProgress || 0 }}<small>%</small></span>
        </div>
      </div>

      <!-- Weight Chart -->
      <div class="chart-card">
        <h3>&#128200; Weight Over Time</h3>
        <div v-if="weightHistory.length > 1" class="chart-wrap">
          <Line :data="weightChartData" :options="chartOptions" />
        </div>
        <div v-else class="empty-chart">
          <p>Log your weight at least twice to see your trend.</p>
        </div>
      </div>

      <!-- Water Intake Chart -->
      <div class="chart-card">
        <h3>&#128167; Water Intake (Last 7 Days)</h3>
        <div v-if="waterData.length > 0" class="chart-wrap">
          <Bar :data="waterChartData" :options="barChartOptions" />
        </div>
        <div v-else class="empty-chart">
          <p>No water intake data yet. Start tracking in the dashboard!</p>
        </div>
      </div>

      <!-- Exercise Stats -->
      <div class="stats-row">
        <div class="stat-card exercise-card">
          <span class="stat-icon">&#127939;</span>
          <span class="stat-label">Total Workouts</span>
          <span class="stat-value">{{ totalWorkouts || 0 }}</span>
        </div>
        <div class="stat-card exercise-card">
          <span class="stat-icon">&#128293;</span>
          <span class="stat-label">Calories Burned</span>
          <span class="stat-value">{{ totalCaloriesBurned || 0 }} <small>kcal</small></span>
        </div>
        <div class="stat-card exercise-card">
          <span class="stat-icon">&#9201;</span>
          <span class="stat-label">Active Minutes</span>
          <span class="stat-value">{{ totalActiveMinutes || 0 }} <small>min</small></span>
        </div>
      </div>

      <!-- Recent Measurements -->
      <div class="chart-card" v-if="measurements.length > 0">
        <h3>&#128207; Body Measurements</h3>
        <div class="measurements-grid">
          <div v-for="m in latestMeasurements" :key="m.type" class="measurement-item">
            <span class="measurement-label">{{ m.label }}</span>
            <span class="measurement-value">{{ m.value }} <small>{{ m.unit }}</small></span>
          </div>
        </div>
      </div>

      <!-- History Table -->
      <div class="history-card">
        <h3>Weight History</h3>
        <div v-if="weightHistory.length" class="history-list">
          <div v-for="entry in weightHistory" :key="entry.date" class="history-item">
            <span class="history-date">{{ formatDate(entry.date) }}</span>
            <span class="history-weight">{{ entry.weight }} kg</span>
            <span class="history-change" :class="entry.change > 0 ? 'up' : 'down'">
              {{ entry.change > 0 ? '+' : '' }}{{ entry.change }} kg
            </span>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>No weight entries yet. Start logging in the Food Tracker!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Line, Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import api, { getMeasurementsHistory, getExerciseHistory, getGoals } from '../src/api'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler)

export default {
  components: { Line, Bar },
  data() {
    return {
      weightHistory: [],
      startWeight: null,
      latestWeight: null,
      goalProgress: 0,
      waterData: [],
      waterGoal: 2500,
      totalWorkouts: 0,
      totalCaloriesBurned: 0,
      totalActiveMinutes: 0,
      measurements: [],
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: false, grid: { color: '#f0f0f0' } },
          x: { grid: { display: false } }
        },
        elements: { line: { tension: 0.4 }, point: { radius: 4, hoverRadius: 6 } }
      },
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: '#f0f0f0' } },
          x: { grid: { display: false } }
        }
      }
    }
  },
  computed: {
    weightChange() {
      if (!this.startWeight || !this.latestWeight) return null
      return Math.round((this.latestWeight - this.startWeight) * 10) / 10
    },
    weightChangeClass() {
      if (!this.weightChange) return ''
      return this.weightChange < 0 ? 'positive' : 'negative'
    },
    weightChartData() {
      return {
        labels: this.weightHistory.map(w => w.date.slice(5)),
        datasets: [{
          label: 'Weight (kg)',
          data: this.weightHistory.map(w => w.weight),
          fill: true,
          borderColor: '#4CAF50',
          backgroundColor: 'rgba(76, 175, 80, 0.08)',
          tension: 0.4,
          pointBackgroundColor: '#4CAF50',
          pointBorderColor: '#fff',
          pointBorderWidth: 2
        }]
      }
    },
    waterChartData() {
      return {
        labels: this.waterData.map(w => w.date.slice(5)),
        datasets: [{
          label: 'Water Intake (ml)',
          data: this.waterData.map(w => w.amount),
          backgroundColor: 'rgba(33, 150, 243, 0.6)',
          borderColor: '#2196F3',
          borderWidth: 2
        }]
      }
    },
    latestMeasurements() {
      if (this.measurements.length === 0) return []
      const latest = this.measurements[0]
      const result = []
      if (latest.body_fat) result.push({ type: 'body_fat', label: 'Body Fat', value: latest.body_fat, unit: '%' })
      if (latest.waist) result.push({ type: 'waist', label: 'Waist', value: latest.waist, unit: 'cm' })
      if (latest.hips) result.push({ type: 'hips', label: 'Hips', value: latest.hips, unit: 'cm' })
      if (latest.chest) result.push({ type: 'chest', label: 'Chest', value: latest.chest, unit: 'cm' })
      return result
    }
  },
  async mounted() {
    await this.loadData()
    await this.loadWaterData()
    await this.loadExerciseData()
    await this.loadMeasurements()
    await this.loadGoals()
  },
  methods: {
    async loadData() {
      try {
        const res = await api.get('/weight/history')
        const history = res.data.history || []

        // Calculate changes
        this.weightHistory = history.map((entry, i) => ({
          ...entry,
          change: i > 0 ? Math.round((entry.weight - history[i - 1].weight) * 10) / 10 : 0
        })).reverse()

        if (history.length > 0) {
          this.startWeight = history[history.length - 1].weight
          this.latestWeight = history[0].weight
        }

        const dashRes = await api.get('/dashboard/summary')
        this.goalProgress = dashRes.data.goal_progress_percent || 0
      } catch (e) {
        console.error('Failed to load progress:', e)
      }
    },
    formatDate(dateStr) {
      const d = new Date(dateStr)
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    },
    async loadWaterData() {
      try {
        // Generate last 7 days water data (demo - replace with actual API when available)
        const today = new Date()
        const waterData = []
        for (let i = 6; i >= 0; i--) {
          const date = new Date(today)
          date.setDate(date.getDate() - i)
          const dateStr = date.toISOString().split('T')[0]
          // Demo data - in production, fetch from API
          waterData.push({
            date: dateStr,
            amount: Math.floor(Math.random() * 1000) + 1500
          })
        }
        this.waterData = waterData
      } catch (e) {
        console.error('Failed to load water data:', e)
      }
    },
    async loadExerciseData() {
      try {
        const res = await getExerciseHistory()
        const exercises = res.data.exercises || []
        this.totalWorkouts = exercises.length
        this.totalCaloriesBurned = Math.round(exercises.reduce((sum, ex) => sum + (ex.calories_burned || 0), 0))
        this.totalActiveMinutes = Math.round(exercises.reduce((sum, ex) => sum + (ex.duration_minutes || 0), 0))
      } catch (e) {
        console.error('Failed to load exercise data:', e)
      }
    },
    async loadMeasurements() {
      try {
        const res = await getMeasurementsHistory()
        this.measurements = res.data.measurements || []
      } catch (e) {
        console.error('Failed to load measurements:', e)
      }
    },
    async loadGoals() {
      try {
        const res = await getGoals()
        this.waterGoal = res.data.water_goal_ml || 2500
      } catch (e) {
        console.error('Failed to load goals:', e)
      }
    }
  }
}
</script>

<style scoped>
.progress-page { max-width: 900px; margin: 0 auto; padding: 32px 20px; font-family: 'Segoe UI', Arial, sans-serif; background: var(--bg-body); min-height: 100vh; transition: background var(--transition-slow); }
.progress-container { display: flex; flex-direction: column; gap: 20px; }
.page-header { margin-bottom: 4px; }
.page-header h1 { margin: 0; font-size: 1.5rem; color: var(--text-primary); transition: color var(--transition-slow); }
.subtitle { margin: 4px 0 0 0; color: var(--text-muted); font-size: 0.9rem; transition: color var(--transition-slow); }

.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; }
.stat-card {
  background: var(--bg-card);
  border-radius: 14px;
  padding: 20px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all var(--transition-slow);
}
.stat-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.stat-card.positive { border-left: 4px solid #22c55e; }
.stat-card.negative { border-left: 4px solid #ef4444; }
.stat-card.exercise-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}
.stat-card.exercise-card .stat-label,
.stat-card.exercise-card .stat-value {
  color: white;
}
.stat-card.exercise-card .stat-value small {
  color: rgba(255, 255, 255, 0.8);
}
.stat-icon {
  position: absolute;
  right: 15px;
  top: 15px;
  font-size: 32px;
  opacity: 0.3;
}
.stat-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; transition: color var(--transition-slow); }
.stat-value { font-size: 1.4rem; font-weight: 700; color: var(--text-primary); transition: color var(--transition-slow); }
.stat-value small { font-size: 0.85rem; color: var(--text-muted); font-weight: 400; transition: color var(--transition-slow); }

.chart-card {
  background: var(--bg-card);
  border-radius: 14px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-slow);
}
.chart-card:hover { box-shadow: var(--shadow-md); }
.chart-card h3 { margin: 0 0 16px 0; font-size: 1rem; color: var(--text-primary); transition: color var(--transition-slow); }
.chart-wrap { height: 300px; }
.empty-chart { text-align: center; padding: 50px; color: var(--text-muted); font-size: 0.9rem; }

.history-card {
  background: var(--bg-card);
  border-radius: 14px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-slow);
}
.history-card:hover { box-shadow: var(--shadow-md); }
.history-card h3 { margin: 0 0 16px 0; font-size: 1rem; color: var(--text-primary); transition: color var(--transition-slow); }
.history-list { display: flex; flex-direction: column; gap: 8px; }
.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-hover);
  border-radius: 10px;
  transition: all var(--transition-base);
}
.history-item:hover { transform: translateX(3px); }
.history-date { font-size: 0.9rem; color: var(--text-secondary); transition: color var(--transition-slow); }
.history-weight { font-size: 1rem; font-weight: 700; color: var(--text-primary); transition: color var(--transition-slow); }
.history-change { font-size: 0.85rem; font-weight: 600; padding: 4px 10px; border-radius: 12px; }
.history-change.up { background: #fef2f2; color: #dc2626; }
.history-change.down { background: #f0fdf4; color: #16a34a; }

.empty-state { text-align: center; padding: 30px; color: var(--text-muted); font-size: 0.9rem; }

.measurements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 15px;
}
.measurement-item {
  background: var(--bg-hover);
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  transition: all var(--transition-base);
}
.measurement-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
.measurement-label {
  display: block;
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}
.measurement-value {
  display: block;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}
.measurement-value small {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 400;
}

@media (max-width: 600px) {
  .stats-row { grid-template-columns: 1fr 1fr; }
}
</style>
