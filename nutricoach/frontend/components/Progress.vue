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
        <h3>Weight Over Time</h3>
        <div v-if="weightHistory.length > 1" class="chart-wrap">
          <Line :data="weightChartData" :options="chartOptions" />
        </div>
        <div v-else class="empty-chart">
          <p>Log your weight at least twice to see your trend.</p>
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
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import api from '../src/api'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

export default {
  components: { Line },
  data() {
    return {
      weightHistory: [],
      startWeight: null,
      latestWeight: null,
      goalProgress: 0,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: false, grid: { color: '#f0f0f0' } },
          x: { grid: { display: false } }
        },
        elements: { line: { tension: 0.4 }, point: { radius: 4, hoverRadius: 6 } }
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
    }
  },
  mounted() {
    this.loadData()
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

@media (max-width: 600px) {
  .stats-row { grid-template-columns: 1fr 1fr; }
}
</style>
