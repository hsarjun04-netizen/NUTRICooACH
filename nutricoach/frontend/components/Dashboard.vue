<template>
  <div class="dashboard">
    <!-- Dark Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-brand">.Diet</div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item" :class="{ active: $route.path === '/dashboard' }">
          <span class="nav-icon">&#127968;</span>
        </router-link>
        <router-link to="/meal-plan" class="nav-item" :class="{ active: $route.path === '/meal-plan' }">
          <span class="nav-icon">&#128197;</span>
        </router-link>
        <router-link to="/tracker" class="nav-item" :class="{ active: $route.path === '/tracker' }">
          <span class="nav-icon">&#127860;</span>
        </router-link>
        <router-link to="/chat" class="nav-item" :class="{ active: $route.path === '/chat' }">
          <span class="nav-icon">&#128172;</span>
        </router-link>
        <router-link to="/progress" class="nav-item" :class="{ active: $route.path === '/progress' }">
          <span class="nav-icon">&#128200;</span>
        </router-link>
        <router-link to="/profile" class="nav-item" :class="{ active: $route.path === '/profile' }">
          <span class="nav-icon">&#9881;</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <a href="#" class="nav-item" @click.prevent="logout">
          <span class="nav-icon">&#128682;</span>
        </a>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Top Header -->
      <header class="top-header">
        <div class="greeting">
          <h1>Hello {{ summary?.name?.split(' ')[0] || 'there' }}, <span class="sprout">&#127793;</span></h1>
          <p class="greeting-sub">Lets start living healthy from now on</p>
        </div>
        <div class="header-actions">
          <div class="search-box">
            <span class="search-icon">&#128269;</span>
            <input type="text" placeholder="Search" />
          </div>
          <button class="notif-btn">
            <span>&#128276;</span>
          </button>
        </div>
      </header>

      <div v-if="summary" class="dashboard-grid">
        <!-- Left Column -->
        <div class="col-left">
          <!-- Hero Banner -->
          <div class="hero-card">
            <div class="hero-content">
              <div class="hero-badge">&#127947; Challenge</div>
              <h2>The 5 a day<br/>challenge <span class="fire">&#128293;</span></h2>
              <p>Eat 5 servings of fruits & vegetables daily</p>
              <div class="hero-avatars">
                <span class="avatar">&#128100;</span>
                <span class="avatar">&#128105;</span>
                <span class="avatar">&#128104;</span>
                <span class="avatar-more">+2k</span>
              </div>
            </div>
            <div class="hero-image">
              <div class="food-plate">&#129367;</div>
              <div class="dumbbell dumbbell-1">&#127947;</div>
              <div class="dumbbell dumbbell-2">&#127947;</div>
            </div>
          </div>

          <!-- Bottom Row: Daily Recap + Daily Calories -->
          <div class="bottom-row">
            <!-- Daily Recap -->
            <div class="recap-card">
              <h3>Daily Recap</h3>
              <div class="macro-list">
                <div class="macro-item">
                  <div class="macro-color carbs"></div>
                  <div class="macro-info">
                    <span class="macro-name">Carbohydrate</span>
                    <span class="macro-bar"><span class="macro-fill carbs-fill" :style="{ width: macroPercent.carbs + '%' }"></span></span>
                  </div>
                  <span class="macro-pct">{{ macroPercent.carbs }}%</span>
                </div>
                <div class="macro-item">
                  <div class="macro-color protein"></div>
                  <div class="macro-info">
                    <span class="macro-name">Protein</span>
                    <span class="macro-bar"><span class="macro-fill protein-fill" :style="{ width: macroPercent.protein + '%' }"></span></span>
                  </div>
                  <span class="macro-pct">{{ macroPercent.protein }}%</span>
                </div>
                <div class="macro-item">
                  <div class="macro-color fats"></div>
                  <div class="macro-info">
                    <span class="macro-name">Fats</span>
                    <span class="macro-bar"><span class="macro-fill fats-fill" :style="{ width: macroPercent.fats + '%' }"></span></span>
                  </div>
                  <span class="macro-pct">{{ macroPercent.fats }}%</span>
                </div>
              </div>
            </div>

            <!-- Daily Calories -->
            <div class="meals-card">
              <h3>Daily Calories</h3>
              <div class="meal-list">
                <div v-for="meal in todayMeals.slice(0, 3)" :key="meal.id" class="meal-row">
                  <div class="meal-dot" :class="meal.meal_type"></div>
                  <div class="meal-info">
                    <div class="meal-name">{{ capitalize(meal.meal_type) }}</div>
                    <div class="meal-desc">{{ meal.name }}</div>
                  </div>
                  <div class="meal-cal">{{ meal.calories }} Kcal</div>
                  <span class="meal-arrow">&#10132;</span>
                </div>
                <div v-if="todayMeals.length === 0" class="empty-meals">
                  <p>No meals logged today</p>
                </div>
              </div>
              <div class="remaining-bar">
                <span>Remaining</span>
                <div class="rem-progress"><span class="rem-fill" :style="{ width: remainingPercent + '%' }"></span></div>
                <span>{{ summary.remaining_calories }} kcal</span>
              </div>
              <button class="add-meal-btn" @click="$router.push('/tracker')">+</button>
            </div>
          </div>
        </div>

        <!-- Middle Column -->
        <div class="col-mid">
          <!-- Daily Activity -->
          <div class="activity-card">
            <div class="activity-header">
              <h3>Daily activity</h3>
              <span class="activity-val">{{ summary.consumed_calories }}Kcal</span>
            </div>
            <div class="chart-area">
              <Line :data="activityData" :options="activityOptions" />
            </div>
            <div class="activity-badge">
              <span class="badge-pct">{{ caloriePercent }}%</span>
              <span class="badge-label">{{ caloriePercent < 100 ? 'Remaining' : 'Completed' }}</span>
            </div>
          </div>

          <!-- Calendar -->
          <div class="calendar-card">
            <div class="cal-header">
              <span class="cal-month">{{ currentMonth }}</span>
              <div class="cal-nav">
                <button @click="prevMonth">&#10094;</button>
                <button @click="nextMonth">&#10095;</button>
              </div>
            </div>
            <div class="cal-days">
              <span v-for="d in dayLabels" :key="d" class="cal-day-label">{{ d }}</span>
            </div>
            <div class="cal-dates">
              <span
                v-for="date in calendarDates"
                :key="date.day"
                class="cal-date"
                :class="{ today: date.isToday, active: date.isActive }"
              >{{ date.day }}</span>
            </div>
          </div>
        </div>

        <!-- Right Column -->
        <div class="col-right">
          <!-- Calories Budget Donut -->
          <div class="budget-card">
            <h3>Calories Budget</h3>
            <div class="donut-wrap">
              <Doughnut :data="donutData" :options="donutOptions" />
              <div class="donut-center">
                <span class="donut-val">{{ summary.consumed_calories }}</span>
                <span class="donut-label">Kcal</span>
              </div>
            </div>
            <div class="donut-legend">
              <span class="legend-item"><span class="legend-dot eaten"></span> Eaten</span>
              <span class="legend-item"><span class="legend-dot remaining"></span> Remaining</span>
            </div>
          </div>

          <!-- Water Tracker -->
          <div class="water-tracker-card">
            <div class="water-content">
              <h3>Drink {{ waterCupsGoal }}<br/>Cups Water</h3>
              <p>{{ waterCupsCurrent }} / {{ waterCupsGoal }} cups</p>
            </div>
            <div class="water-ring">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="#e0e8f0" stroke-width="10" fill="none"/>
                <circle cx="50" cy="50" r="40" stroke="#4facfe" stroke-width="10" fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="waterRingCircumference"
                  :stroke-dashoffset="waterRingOffset"
                  transform="rotate(-90 50 50)"
                />
              </svg>
              <div class="water-ring-center">
                <span>{{ waterPercent }}%</span>
              </div>
            </div>
            <button class="water-add" @click="addWater(250)">+</button>
          </div>
        </div>
      </div>

      <div v-else class="loading">
        <p>Loading dashboard...</p>
      </div>
    </main>
  </div>
</template>

<script>
import { Line, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import api from '../src/api'
import { useAuthStore } from '../src/stores/auth'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler)

export default {
  components: { Line, Doughnut },
  data() {
    return {
      summary: null,
      waterTotal: 0,
      waterGoal: 2500,
      todayMeals: [],
      activityData: { labels: [], datasets: [] },
      donutData: { labels: [], datasets: [] },
      activityOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { display: false }
        },
        elements: { line: { tension: 0.4 }, point: { radius: 0 } }
      },
      donutOptions: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        plugins: { legend: { display: false } }
      },
      waterRingCircumference: 2 * Math.PI * 40,
      currentMonth: new Date().toLocaleString('default', { month: 'long' }),
      dayLabels: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
    }
  },
  computed: {
    caloriePercent() {
      if (!this.summary || !this.summary.target_calories) return 0
      return Math.min(Math.round((this.summary.consumed_calories / this.summary.target_calories) * 100), 100)
    },
    remainingPercent() {
      if (!this.summary || !this.summary.target_calories) return 0
      return Math.max(Math.round((this.summary.remaining_calories / this.summary.target_calories) * 100), 0)
    },
    waterPercent() {
      return Math.min(Math.round((this.waterTotal / this.waterGoal) * 100), 100)
    },
    waterRingOffset() {
      return this.waterRingCircumference - (this.waterPercent / 100) * this.waterRingCircumference
    },
    waterCupsGoal() {
      return Math.round(this.waterGoal / 250)
    },
    waterCupsCurrent() {
      return Math.round(this.waterTotal / 250)
    },
    macroPercent() {
      const total = this.todayMeals.reduce((s, m) => s + (m.carbs || 0) + (m.protein || 0) + (m.fats || 0), 0) || 1
      const carbs = this.todayMeals.reduce((s, m) => s + (m.carbs || 0), 0)
      const protein = this.todayMeals.reduce((s, m) => s + (m.protein || 0), 0)
      const fats = this.todayMeals.reduce((s, m) => s + (m.fats || 0), 0)
      return {
        carbs: Math.round((carbs / total) * 100),
        protein: Math.round((protein / total) * 100),
        fats: Math.round((fats / total) * 100)
      }
    },
    calendarDates() {
      const now = new Date()
      const year = now.getFullYear()
      const month = now.getMonth()
      const daysInMonth = new Date(year, month + 1, 0).getDate()
      const firstDay = new Date(year, month, 1).getDay()
      const today = now.getDate()
      const dates = []
      for (let i = 0; i < firstDay; i++) dates.push({ day: '', isToday: false, isActive: false })
      for (let d = 1; d <= daysInMonth; d++) {
        dates.push({ day: d, isToday: d === today, isActive: d === today })
      }
      return dates
    }
  },
  mounted() {
    this.loadSummary()
    this.loadWater()
    this.loadMeals()
    this.buildCharts()
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
    async loadMeals() {
      try {
        const res = await api.get('/meals/today')
        this.todayMeals = res.data.meals || []
      } catch (e) {
        console.error('Failed to load meals:', e)
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
    buildCharts() {
      const hours = ['6am', '8am', '10am', '12pm', '2pm', '4pm', '6pm', '8pm']
      const base = this.summary?.consumed_calories || 1500
      this.activityData = {
        labels: hours,
        datasets: [{
          data: hours.map(() => Math.floor(Math.random() * base * 0.3 + base * 0.1)),
          borderColor: '#a3e635',
          backgroundColor: 'rgba(163, 230, 53, 0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 2
        }, {
          data: hours.map(() => Math.floor(Math.random() * base * 0.2 + base * 0.05)),
          borderColor: '#34d399',
          backgroundColor: 'transparent',
          fill: false,
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 2
        }]
      }
      const eaten = this.summary?.consumed_calories || 0
      const remaining = Math.max((this.summary?.target_calories || 2000) - eaten, 0)
      this.donutData = {
        labels: ['Eaten', 'Remaining'],
        datasets: [{
          data: [eaten, remaining],
          backgroundColor: ['#fbbf24', '#e2e8f0'],
          borderWidth: 0,
          hoverOffset: 4
        }]
      }
    },
    capitalize(s) {
      return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''
    },
    prevMonth() {},
    nextMonth() {},
    logout() {
      const auth = useAuthStore()
      auth.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.dashboard { display: flex; min-height: 100vh; font-family: 'Segoe UI', system-ui, sans-serif; background: #f1f5f9; }

/* Sidebar */
.sidebar {
  width: 64px;
  background: #1e293b;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  flex-shrink: 0;
  border-radius: 0 20px 20px 0;
  margin: 12px 0 12px 0;
}
.sidebar-brand { color: #94a3b8; font-size: 0.75rem; font-weight: 700; margin-bottom: 32px; letter-spacing: 1px; }
.sidebar-nav { display: flex; flex-direction: column; gap: 8px; flex: 1; }
.sidebar-footer { margin-top: auto; padding-top: 16px; }
.nav-item {
  width: 44px; height: 44px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 12px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 1.2rem;
  transition: all 0.2s;
}
.nav-item:hover, .nav-item.active { background: #a3e635; color: #1e293b; }

/* Main Content */
.main-content { flex: 1; padding: 24px 32px; overflow-y: auto; }

/* Top Header */
.top-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.greeting h1 { margin: 0; font-size: 1.4rem; color: #1e293b; font-weight: 700; }
.sprout { font-size: 1.1rem; }
.greeting-sub { margin: 4px 0 0 0; color: #94a3b8; font-size: 0.8rem; }
.header-actions { display: flex; gap: 12px; align-items: center; }
.search-box {
  display: flex; align-items: center; gap: 8px;
  background: white; padding: 8px 14px; border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.search-box input { border: none; outline: none; font-size: 0.85rem; width: 120px; background: transparent; }
.search-icon { color: #94a3b8; font-size: 0.9rem; }
.notif-btn {
  width: 40px; height: 40px;
  border-radius: 12px; border: none; background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  cursor: pointer; font-size: 1.1rem;
}

/* Dashboard Grid */
.dashboard-grid { display: grid; grid-template-columns: 1.4fr 0.9fr 0.7fr; gap: 20px; }

/* Hero Card */
.hero-card {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-radius: 20px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}
.hero-badge { display: inline-block; background: white; color: #16a34a; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; margin-bottom: 10px; }
.hero-content h2 { margin: 0 0 6px 0; font-size: 1.3rem; color: #166534; font-weight: 800; line-height: 1.3; }
.hero-content p { margin: 0 0 12px 0; color: #15803d; font-size: 0.8rem; }
.fire { font-size: 1rem; }
.hero-avatars { display: flex; align-items: center; }
.avatar { width: 28px; height: 28px; background: #fde047; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; margin-right: -8px; border: 2px solid white; }
.avatar-more { margin-left: 14px; font-size: 0.7rem; color: #166534; font-weight: 600; }
.hero-image { position: relative; width: 100px; height: 80px; }
.food-plate { font-size: 3.5rem; position: absolute; right: 0; top: 0; }
.dumbbell { font-size: 1.5rem; position: absolute; color: #86efac; }
.dumbbell-1 { top: -10px; left: -20px; transform: rotate(-30deg); }
.dumbbell-2 { bottom: 0; right: 20px; transform: rotate(15deg); }

/* Bottom Row */
.bottom-row { display: grid; grid-template-columns: 1fr 1.2fr; gap: 20px; }

/* Recap Card */
.recap-card { background: white; border-radius: 20px; padding: 20px; }
.recap-card h3 { margin: 0 0 16px 0; font-size: 0.95rem; color: #1e293b; }
.macro-list { display: flex; flex-direction: column; gap: 14px; }
.macro-item { display: flex; align-items: center; gap: 10px; }
.macro-color { width: 32px; height: 32px; border-radius: 8px; flex-shrink: 0; }
.macro-color.carbs { background: #67e8f9; }
.macro-color.protein { background: #fbbf24; }
.macro-color.fats { background: #86efac; }
.macro-info { flex: 1; }
.macro-name { display: block; font-size: 0.75rem; color: #64748b; margin-bottom: 4px; }
.macro-bar { display: block; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden; }
.macro-fill { display: block; height: 100%; border-radius: 3px; }
.macro-fill.carbs-fill { background: #67e8f9; }
.macro-fill.protein-fill { background: #fbbf24; }
.macro-fill.fats-fill { background: #86efac; }
.macro-pct { font-size: 0.8rem; font-weight: 700; color: #1e293b; min-width: 32px; text-align: right; }

/* Meals Card */
.meals-card { background: white; border-radius: 20px; padding: 20px; position: relative; }
.meals-card h3 { margin: 0 0 16px 0; font-size: 0.95rem; color: #1e293b; }
.meal-list { display: flex; flex-direction: column; gap: 12px; }
.meal-row { display: flex; align-items: center; gap: 12px; padding: 10px 12px; background: #f8fafc; border-radius: 12px; }
.meal-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.meal-dot.breakfast { background: #fbbf24; }
.meal-dot.lunch { background: #86efac; }
.meal-dot.dinner { background: #67e8f9; }
.meal-dot.snack { background: #c084fc; }
.meal-info { flex: 1; }
.meal-name { font-size: 0.8rem; font-weight: 700; color: #1e293b; }
.meal-desc { font-size: 0.7rem; color: #94a3b8; }
.meal-cal { font-size: 0.8rem; font-weight: 700; color: #1e293b; }
.meal-arrow { color: #94a3b8; font-size: 0.9rem; }
.empty-meals { text-align: center; padding: 20px; color: #cbd5e1; font-size: 0.8rem; }
.remaining-bar { display: flex; align-items: center; gap: 8px; margin-top: 14px; font-size: 0.7rem; color: #94a3b8; }
.rem-progress { flex: 1; height: 4px; background: #f1f5f9; border-radius: 2px; overflow: hidden; }
.rem-fill { height: 100%; background: linear-gradient(90deg, #fbbf24, #f59e0b); border-radius: 2px; }
.add-meal-btn {
  position: absolute; bottom: 20px; right: 20px;
  width: 36px; height: 36px; border-radius: 10px;
  background: #1e293b; color: white; border: none;
  font-size: 1.2rem; cursor: pointer;
}

/* Activity Card */
.activity-card {
  background: #1e293b;
  border-radius: 20px;
  padding: 20px;
  color: white;
  margin-bottom: 20px;
}
.activity-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.activity-header h3 { margin: 0; font-size: 0.9rem; font-weight: 600; }
.activity-val { font-size: 0.75rem; color: #94a3b8; }
.chart-area { height: 100px; }
.activity-badge {
  display: inline-flex; flex-direction: column;
  background: white; color: #1e293b;
  padding: 8px 14px; border-radius: 12px;
  margin-top: 10px;
}
.badge-pct { font-size: 0.85rem; font-weight: 700; }
.badge-label { font-size: 0.65rem; color: #94a3b8; }

/* Calendar */
.calendar-card { background: white; border-radius: 20px; padding: 20px; }
.cal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.cal-month { font-size: 0.9rem; font-weight: 700; color: #1e293b; }
.cal-nav { display: flex; gap: 6px; }
.cal-nav button { background: #f1f5f9; border: none; border-radius: 8px; width: 28px; height: 28px; cursor: pointer; color: #64748b; font-size: 0.7rem; }
.cal-days { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin-bottom: 6px; }
.cal-day-label { text-align: center; font-size: 0.65rem; color: #94a3b8; font-weight: 600; }
.cal-dates { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.cal-date { text-align: center; font-size: 0.7rem; padding: 6px 0; border-radius: 8px; color: #475569; }
.cal-date.today { background: #1e293b; color: white; font-weight: 700; }
.cal-date.active { background: #dcfce7; color: #166534; font-weight: 700; }

/* Budget Card */
.budget-card { background: white; border-radius: 20px; padding: 20px; margin-bottom: 20px; text-align: center; }
.budget-card h3 { margin: 0 0 16px 0; font-size: 0.95rem; color: #1e293b; text-align: left; }
.donut-wrap { position: relative; height: 140px; }
.donut-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.donut-val { display: block; font-size: 1.3rem; font-weight: 800; color: #1e293b; }
.donut-label { font-size: 0.7rem; color: #94a3b8; }
.donut-legend { display: flex; justify-content: center; gap: 16px; margin-top: 12px; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.75rem; color: #64748b; }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; }
.legend-dot.eaten { background: #fbbf24; }
.legend-dot.remaining { background: #e2e8f0; }

/* Water Tracker */
.water-tracker-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 20px;
  padding: 20px;
  color: white;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.water-content h3 { margin: 0 0 4px 0; font-size: 0.95rem; font-weight: 700; line-height: 1.3; }
.water-content p { margin: 0; font-size: 0.75rem; opacity: 0.9; }
.water-ring { position: relative; width: 70px; height: 70px; }
.water-ring svg { width: 100%; height: 100%; }
.water-ring-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 0.75rem; font-weight: 700; }
.water-add {
  position: absolute; bottom: 14px; right: 14px;
  width: 32px; height: 32px; border-radius: 50%;
  background: rgba(255,255,255,0.25); color: white;
  border: none; font-size: 1.2rem; cursor: pointer;
  backdrop-filter: blur(4px);
}

.loading { text-align: center; padding: 80px; color: #94a3b8; }

@media (max-width: 1100px) {
  .dashboard-grid { grid-template-columns: 1fr 1fr; }
  .col-right { grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
}
@media (max-width: 800px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .col-right { grid-column: auto; display: flex; flex-direction: column; }
  .bottom-row { grid-template-columns: 1fr; }
  .sidebar { width: 52px; }
}
</style>
