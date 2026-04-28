<template>
  <div class="dashboard">
    <!-- Dark Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-brand">.Diet</div>
      <nav class="sidebar-nav">
        <router-link v-for="item in navItems" :key="item.to" :to="item.to" class="nav-item" :class="{ active: $route.path === item.to }" :title="item.label">
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <a href="#" class="nav-item" @click.prevent="logout" title="Logout">
          <span class="nav-icon">&#128682;</span>
        </a>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Skeleton Loading -->
      <div v-if="!summary" class="skeleton-grid">
        <div class="skeleton-header"><div class="skeleton-text" style="width:180px;height:28px"></div><div class="skeleton-text" style="width:120px;height:16px"></div></div>
        <div class="skeleton-hero"></div>
        <div class="skeleton-row"><div class="skeleton-card"></div><div class="skeleton-card"></div></div>
        <div class="skeleton-activity"></div>
        <div class="skeleton-calendar"></div>
        <div class="skeleton-budget"></div>
        <div class="skeleton-water"></div>
      </div>

      <div v-else class="dashboard-animate">
        <!-- Top Header -->
        <header class="top-header" :style="delayStyle(0)">
          <div class="greeting">
            <h1>Hello {{ displayName }}, <span class="sprout">&#127793;</span></h1>
            <p class="greeting-sub">Lets start living healthy from now on</p>
          </div>
          <div class="header-actions">
            <div class="search-box">
              <span class="search-icon">&#128269;</span>
              <input type="text" placeholder="Search" />
            </div>
            <button class="icon-btn notif-btn" :class="{ pulse: hasNotification }" title="Notifications">
              <span>&#128276;</span>
            </button>
            <button class="icon-btn theme-btn" @click="theme.toggle" :title="theme.isDark ? 'Light mode' : 'Dark mode'">
              <span v-if="theme.isDark">&#9788;</span>
              <span v-else>&#9790;</span>
            </button>
            <!-- Profile Dropdown -->
            <div class="profile-dropdown-wrap" ref="profileWrap">
              <button class="profile-avatar" @click="profileOpen = !profileOpen">
                <span class="avatar-initial">{{ userInitial }}</span>
              </button>
              <transition name="dropdown">
                <div v-if="profileOpen" class="profile-dropdown">
                  <div class="dropdown-header">
                    <span class="dropdown-name">{{ displayName }}</span>
                    <span class="dropdown-email">{{ userEmail }}</span>
                  </div>
                  <div class="dropdown-divider"></div>
                  <router-link to="/profile" class="dropdown-item" @click="profileOpen = false">
                    <span class="dropdown-icon" v-html="'&#128100;'"></span> My Profile
                  </router-link>
                  <router-link to="/setup" class="dropdown-item" @click="profileOpen = false">
                    <span class="dropdown-icon" v-html="'&#9881;'"></span> Settings
                  </router-link>
                  <div class="dropdown-divider"></div>
                  <a href="#" class="dropdown-item dropdown-danger" @click.prevent="doLogout">
                    <span class="dropdown-icon" v-html="'&#128682;'"></span> Logout
                  </a>
                </div>
              </transition>
            </div>
          </div>
        </header>

        <div class="dashboard-grid">
          <!-- Left Column -->
          <div class="col-left">
            <!-- Hero Banner -->
            <div class="hero-card" :style="delayStyle(1)">
              <div class="hero-content">
                <div class="hero-badge"><span class="badge-icon">&#127947;</span> Weekly Challenge</div>
                <h2>{{ currentChallenge.title }} <span class="fire">&#128293;</span></h2>
                <p>{{ currentChallenge.description }}</p>
                <div class="challenge-progress">
                  <div class="challenge-bar">
                    <span class="challenge-fill" :style="{ width: challengeProgress + '%' }"></span>
                  </div>
                  <span class="challenge-text">{{ challengeCurrent }} / {{ challengeGoal }} {{ currentChallenge.unit }}</span>
                </div>
                <div class="hero-avatars">
                  <span class="avatar" v-for="n in 3" :key="n">&#128100;</span>
                  <span class="avatar-more">+2k</span>
                </div>
              </div>
              <div class="hero-image">
                <div class="food-plate float">{{ currentChallenge.icon }}</div>
                <div class="dumbbell dumbbell-1 float-slow">&#127947;</div>
                <div class="dumbbell dumbbell-2 float-slow2">&#127947;</div>
              </div>
            </div>

            <!-- Bottom Row -->
            <div class="bottom-row">
              <!-- Daily Recap -->
              <div class="recap-card" :style="delayStyle(2)">
                <h3>Daily Recap</h3>
                <div class="macro-list">
                  <div class="macro-item" v-for="(macro, i) in macros" :key="macro.name" :style="delayStyle(3 + i * 0.1)">
                    <div class="macro-color" :class="macro.key"></div>
                    <div class="macro-info">
                      <span class="macro-name">{{ macro.name }}</span>
                      <span class="macro-bar"><span class="macro-fill" :class="macro.key + '-fill'" :style="{ width: animatedMacroPct[macro.key] + '%' }"></span></span>
                    </div>
                    <span class="macro-pct">{{ macroPercent[macro.key] }}%</span>
                  </div>
                </div>
              </div>

              <!-- Daily Calories -->
              <div class="meals-card" :style="delayStyle(3)">
                <h3>Daily Calories</h3>
                <transition-group name="meal-slide" tag="div" class="meal-list">
                  <div v-for="(meal, i) in todayMeals.slice(0, 3)" :key="meal.id" class="meal-row" :style="delayStyle(3.5 + i * 0.1)">
                    <div class="meal-dot" :class="meal.meal_type"></div>
                    <div class="meal-info">
                      <div class="meal-name">{{ capitalize(meal.meal_type) }}</div>
                      <div class="meal-desc">{{ meal.name }}</div>
                    </div>
                    <div class="meal-cal">{{ meal.calories }} Kcal</div>
                    <span class="meal-arrow">&#10132;</span>
                  </div>
                </transition-group>
                <div v-if="todayMeals.length === 0" class="empty-meals">
                  <p>No meals logged today</p>
                </div>
                <div class="remaining-bar">
                  <span>Remaining</span>
                  <div class="rem-progress"><span class="rem-fill" :style="{ width: animatedRemainingPct + '%' }"></span></div>
                  <span>{{ animatedRemaining }} kcal</span>
                </div>
                <button class="add-meal-btn ripple" @click="$router.push('/tracker')">
                  <span class="btn-icon">+</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Middle Column -->
          <div class="col-mid">
            <!-- Daily Activity -->
            <div class="activity-card" :style="delayStyle(4)">
              <div class="activity-header">
                <h3>Daily activity</h3>
                <span class="activity-val">{{ animatedCalories }}Kcal</span>
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
            <div class="calendar-card" :style="delayStyle(5)">
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
                <span v-for="(date, i) in calendarDates" :key="i" class="cal-date" :class="{ today: date.isToday, active: date.isActive }" :style="date.day ? delayStyle(5.2 + (i % 7) * 0.03) : {}">{{ date.day }}</span>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="col-right">
            <!-- Calories Budget Donut -->
            <div class="budget-card" :style="delayStyle(6)">
              <h3>Calories Budget</h3>
              <div class="donut-wrap">
                <Doughnut :data="donutData" :options="donutOptions" />
                <div class="donut-center">
                  <span class="donut-val">{{ animatedCalories }}</span>
                  <span class="donut-label">Kcal</span>
                </div>
              </div>
              <div class="donut-legend">
                <span class="legend-item"><span class="legend-dot eaten"></span> Eaten</span>
                <span class="legend-item"><span class="legend-dot remaining"></span> Remaining</span>
              </div>
            </div>

            <!-- Water Tracker -->
            <div class="water-tracker-card" :style="delayStyle(7)">
              <div class="water-content">
                <h3>Drink {{ waterCupsGoal }}<br/>Cups Water</h3>
                <p>{{ waterCupsCurrent }} / {{ waterCupsGoal }} cups</p>
              </div>
              <div class="water-ring" :class="{ pulse: waterPercent >= 100 }">
                <svg viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.2)" stroke-width="10" fill="none"/>
                  <circle cx="50" cy="50" r="40" stroke="white" stroke-width="10" fill="none" stroke-linecap="round" :stroke-dasharray="waterRingCircumference" :stroke-dashoffset="animatedWaterOffset" transform="rotate(-90 50 50)" class="water-progress"/>
                </svg>
                <div class="water-ring-center"><span>{{ waterPercent }}%</span></div>
              </div>
              <button class="water-add ripple" @click="addWater(250)"><span class="btn-icon">+</span></button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { Line, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import api from '../src/api'
import { useAuthStore } from '../src/stores/auth'
import { useThemeStore } from '../src/stores/theme'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler)

export default {
  components: { Line, Doughnut },
  setup() {
    const theme = useThemeStore()
    return { theme }
  },
  data() {
    return {
      summary: null,
      waterTotal: 0,
      waterGoal: 2500,
      todayMeals: [],
      currentChallenge: {
        id: 1,
        title: '5 a Day Challenge',
        description: 'Eat 5 servings of fruits & vegetables daily',
        icon: '&#129367;',
        goal: 35,
        unit: 'servings',
        weekStartDate: new Date().toISOString()
      },
      challengeCurrent: 0,
      challengeProgress: 0,
      activityData: { labels: [], datasets: [] },
      donutData: { labels: [], datasets: [] },
      hasNotification: true,
      profileOpen: false,
      animatedCalories: 0,
      animatedRemaining: 0,
      animatedMacroPct: { carbs: 0, protein: 0, fats: 0 },
      animatedWaterOffset: 2 * Math.PI * 40,
      animatedRemainingPct: 0,
      navItems: [
        { to: '/dashboard', icon: '&#127968;', label: 'Dashboard' },
        { to: '/meal-plan', icon: '&#128197;', label: 'Meal Plan' },
        { to: '/tracker', icon: '&#127860;', label: 'Food Tracker' },
        { to: '/recipes', icon: '&#127859;', label: 'Recipes' },
        { to: '/exercises', icon: '&#127947;', label: 'Exercise Tracker' },
        { to: '/progress', icon: '&#128200;', label: 'Progress' },
        { to: '/profile', icon: '&#9881;', label: 'Profile' }
      ],
      macros: [
        { name: 'Carbohydrate', key: 'carbs' },
        { name: 'Protein', key: 'protein' },
        { name: 'Fats', key: 'fats' }
      ],
      activityOptions: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 1500, easing: 'easeOutQuart' },
        plugins: { legend: { display: false } },
        scales: { x: { display: false }, y: { display: false } },
        elements: { line: { tension: 0.4 }, point: { radius: 0 } }
      },
      donutOptions: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        animation: { animateRotate: true, duration: 2000, easing: 'easeOutQuart' },
        plugins: { legend: { display: false } }
      },
      waterRingCircumference: 2 * Math.PI * 40,
      currentMonth: new Date().toLocaleString('default', { month: 'long' }),
      dayLabels: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
    }
  },
  computed: {
    displayName() {
      const auth = useAuthStore()
      const name = auth.name || this.summary?.name || 'there'
      return name.split(' ')[0]
    },
    userInitial() {
      const auth = useAuthStore()
      const name = auth.name || this.summary?.name || 'U'
      return name.charAt(0).toUpperCase()
    },
    userEmail() {
      const auth = useAuthStore()
      return auth.user?.email || this.summary?.email || ''
    },
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
    waterCupsGoal() { return Math.round(this.waterGoal / 250) },
    waterCupsCurrent() { return Math.round(this.waterTotal / 250) },
    challengeGoal() { return this.currentChallenge.goal || 35 },
    macroPercent() {
      const total = this.todayMeals.reduce((s, m) => s + (m.carbs || 0) + (m.protein || 0) + (m.fats || 0), 0) || 1
      const carbs = this.todayMeals.reduce((s, m) => s + (m.carbs || 0), 0)
      const protein = this.todayMeals.reduce((s, m) => s + (m.protein || 0), 0)
      const fats = this.todayMeals.reduce((s, m) => s + (m.fats || 0), 0)
      return { carbs: Math.round((carbs / total) * 100), protein: Math.round((protein / total) * 100), fats: Math.round((fats / total) * 100) }
    },
    calendarDates() {
      const now = new Date()
      const year = now.getFullYear(), month = now.getMonth()
      const daysInMonth = new Date(year, month + 1, 0).getDate()
      const firstDay = new Date(year, month, 1).getDay()
      const today = now.getDate()
      const dates = []
      for (let i = 0; i < firstDay; i++) dates.push({ day: '', isToday: false, isActive: false })
      for (let d = 1; d <= daysInMonth; d++) dates.push({ day: d, isToday: d === today, isActive: d === today })
      return dates
    }
  },
  mounted() {
    this.loadSummary()
    this.loadWater()
    this.loadMeals()
    this.loadChallenge()
    this.buildCharts()
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    async loadSummary() {
      try {
        const res = await api.get('/dashboard/summary')
        this.summary = res.data
        this.$nextTick(() => {
          this.animateNumbers()
          this.animateProgressBars()
          this.animateWaterRing()
        })
      } catch (e) { console.error('Failed to load summary:', e) }
    },
    async loadWater() {
      try {
        const res = await api.get('/water/today')
        this.waterTotal = res.data.total_ml
      } catch (e) { console.error('Failed to load water:', e) }
    },
    async loadMeals() {
      try {
        const res = await api.get('/meals/today')
        this.todayMeals = res.data.meals || []
      } catch (e) { console.error('Failed to load meals:', e) }
    },
    async loadChallenge() {
      try {
        const res = await api.get('/challenges/current')
        if (res.data) {
          this.currentChallenge = {
            id: res.data.id,
            title: res.data.title,
            description: res.data.description,
            icon: res.data.icon || '&#129367;',
            goal: res.data.goal,
            unit: res.data.unit,
            weekStartDate: res.data.week_start_date
          }
          this.challengeCurrent = res.data.current_progress || 0
          this.challengeProgress = res.data.progress_percent || 0
        }
      } catch (e) { 
        console.error('Failed to load challenge:', e)
        // Fallback to default challenge if API fails
        this.challengeCurrent = 0
        this.challengeProgress = 0
      }
    },
    async addWater(amount) {
      try {
        await api.post('/water/log', { amount_ml: amount })
        this.waterTotal += amount
        this.animateWaterRing()
        this.showToast('Water added! +' + amount + 'ml', 'success')
      } catch (e) { console.error('Failed to log water:', e) }
    },
    buildCharts() {
      const hours = ['6am', '8am', '10am', '12pm', '2pm', '4pm', '6pm', '8pm']
      const base = this.summary?.consumed_calories || 1500
      this.activityData = {
        labels: hours,
        datasets: [
          { data: hours.map(() => Math.floor(Math.random() * base * 0.3 + base * 0.1)), borderColor: '#a3e635', backgroundColor: 'rgba(163, 230, 53, 0.1)', fill: true, tension: 0.4, pointRadius: 0, borderWidth: 2 },
          { data: hours.map(() => Math.floor(Math.random() * base * 0.2 + base * 0.05)), borderColor: '#34d399', backgroundColor: 'transparent', fill: false, tension: 0.4, pointRadius: 0, borderWidth: 2 }
        ]
      }
      const eaten = this.summary?.consumed_calories || 0
      const remaining = Math.max((this.summary?.target_calories || 2000) - eaten, 0)
      this.donutData = {
        labels: ['Eaten', 'Remaining'],
        datasets: [{ data: [eaten, remaining], backgroundColor: ['#fbbf24', '#e2e8f0'], borderWidth: 0, hoverOffset: 4 }]
      }
    },
    animateNumbers() {
      this.animateValue('animatedCalories', 0, this.summary?.consumed_calories || 0, 1200)
      this.animateValue('animatedRemaining', 0, this.summary?.remaining_calories || 0, 1200)
    },
    animateProgressBars() {
      const targets = this.macroPercent
      Object.keys(targets).forEach((key, i) => {
        setTimeout(() => { this.animateValue('animatedMacroPct.' + key, 0, targets[key], 800) }, i * 150)
      })
      this.animateValue('animatedRemainingPct', 0, this.remainingPercent, 1000)
    },
    animateWaterRing() {
      const start = this.animatedWaterOffset
      const end = this.waterRingOffset
      const duration = 1200
      const startTime = performance.now()
      const tick = (now) => {
        const elapsed = now - startTime
        const progress = Math.min(elapsed / duration, 1)
        const ease = 1 - Math.pow(1 - progress, 3)
        this.animatedWaterOffset = start + (end - start) * ease
        if (progress < 1) requestAnimationFrame(tick)
      }
      requestAnimationFrame(tick)
    },
    animateValue(key, start, end, duration) {
      const startTime = performance.now()
      const tick = (now) => {
        const elapsed = now - startTime
        const progress = Math.min(elapsed / duration, 1)
        const ease = 1 - Math.pow(1 - progress, 3)
        const val = Math.round(start + (end - start) * ease)
        const keys = key.split('.')
        if (keys.length === 2) this[keys[0]][keys[1]] = val
        else this[key] = val
        if (progress < 1) requestAnimationFrame(tick)
      }
      requestAnimationFrame(tick)
    },
    delayStyle(seconds) { return { animationDelay: seconds + 's' } },
    capitalize(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : '' },
    prevMonth() {}, nextMonth() {},
    handleClickOutside(e) {
      if (this.$refs.profileWrap && !this.$refs.profileWrap.contains(e.target)) {
        this.profileOpen = false
      }
    },
    doLogout() {
      this.profileOpen = false
      this.logout()
    },
    logout() {
      const auth = useAuthStore()
      auth.logout()
      this.$router.push('/login')
    },
    showToast(msg, type) {
      const container = document.querySelector('.toast-container') || (() => {
        const el = document.createElement('div')
        el.className = 'toast-container'
        document.body.appendChild(el)
        return el
      })()
      const toast = document.createElement('div')
      toast.className = 'toast toast-' + type
      toast.textContent = msg
      container.appendChild(toast)
      setTimeout(() => {
        toast.classList.add('toast-leave')
        setTimeout(() => toast.remove(), 300)
      }, 2500)
    }
  }
}
</script>

<style scoped>
/* ===== BASE ===== */
.dashboard { display: flex; min-height: 100vh; background: var(--bg-body); transition: background var(--transition-slow); }

/* ===== SIDEBAR ===== */
.sidebar {
  width: 200px; background: var(--bg-sidebar);
  display: flex; flex-direction: column; align-items: stretch;
  padding: 20px 0; flex-shrink: 0;
  border-radius: 0 20px 20px 0; margin: 12px 0 12px 0;
  transition: background var(--transition-slow);
}
.sidebar-brand { color: var(--text-muted); font-size: 0.75rem; font-weight: 700; margin-bottom: 32px; letter-spacing: 1px; }
.sidebar-nav { display: flex; flex-direction: column; gap: 8px; flex: 1; }
.sidebar-footer { margin-top: auto; padding-top: 16px; }
.nav-item {
  height: 44px;
  display: flex; align-items: center; gap: 12px;
  padding: 0 16px;
  border-radius: 12px; color: var(--text-muted);
  text-decoration: none; font-size: 0.9rem;
  transition: all var(--transition-base);
  position: relative;
  margin: 0 8px;
}
.nav-item::before {
  content: ''; position: absolute; inset: 0; border-radius: 12px;
  background: var(--accent); opacity: 0; transform: scale(0.8);
  transition: all var(--transition-base); z-index: 0;
}
.nav-item:hover, .nav-item.active { color: #1e293b; transform: scale(1.1); }
.nav-item:hover::before, .nav-item.active::before { opacity: 1; transform: scale(1); }
.nav-item:hover { box-shadow: 0 0 16px rgba(163, 230, 53, 0.4); }
.nav-icon { position: relative; z-index: 1; font-size: 1.2rem; }
.nav-label { position: relative; z-index: 1; font-weight: 500; }

/* ===== MAIN ===== */
.main-content { flex: 1; padding: 24px 32px; overflow-y: auto; }

/* ===== SKELETON ===== */
.skeleton-grid { padding: 0; }
.skeleton-text, .skeleton-hero, .skeleton-card, .skeleton-activity, .skeleton-calendar, .skeleton-budget, .skeleton-water {
  background: linear-gradient(90deg, var(--border-color) 25%, var(--bg-hover) 50%, var(--border-color) 75%);
  background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 12px;
}
.skeleton-hero { height: 140px; margin-bottom: 20px; border-radius: var(--radius-lg); }
.skeleton-row { display: grid; grid-template-columns: 1fr 1.2fr; gap: 20px; margin-bottom: 20px; }
.skeleton-card { height: 180px; }
.skeleton-activity { height: 200px; margin-bottom: 20px; border-radius: var(--radius-lg); }
.skeleton-calendar { height: 220px; margin-bottom: 20px; border-radius: var(--radius-lg); }
.skeleton-budget { height: 200px; margin-bottom: 20px; border-radius: var(--radius-lg); }
.skeleton-water { height: 120px; border-radius: var(--radius-lg); }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* ===== ENTRANCE ===== */
.dashboard-animate > * { animation: fadeInUp 0.6s ease-out both; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }

/* ===== HEADER ===== */
.top-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.greeting h1 { margin: 0; font-size: 1.4rem; color: var(--text-primary); font-weight: 700; transition: color var(--transition-slow); }
.sprout { font-size: 1.1rem; display: inline-block; animation: wiggle 2s ease-in-out infinite; }
@keyframes wiggle { 0%, 100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
.greeting-sub { margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.8rem; transition: color var(--transition-slow); }

.header-actions { display: flex; gap: 10px; align-items: center; }
.search-box {
  display: flex; align-items: center; gap: 8px;
  background: var(--bg-card); padding: 8px 14px; border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm); transition: all var(--transition-base);
}
.search-box:focus-within { box-shadow: var(--shadow-md); transform: translateY(-1px); }
.search-box input { border: none; outline: none; font-size: 0.85rem; width: 120px; background: transparent; color: var(--text-primary); }
.search-icon { color: var(--text-muted); font-size: 0.9rem; }

.icon-btn {
  width: 40px; height: 40px; border-radius: var(--radius-sm); border: none;
  background: var(--bg-card); box-shadow: var(--shadow-sm); cursor: pointer; font-size: 1.1rem;
  display: flex; align-items: center; justify-content: center; color: var(--text-secondary);
  transition: all var(--transition-base);
}
.icon-btn:hover { transform: scale(1.1); box-shadow: var(--shadow-md); color: var(--text-primary); }
.notif-btn.pulse { animation: bellPulse 2s ease-in-out infinite; }
@keyframes bellPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
.theme-btn:hover { transform: rotate(15deg) scale(1.15); }

/* Profile Dropdown */
.profile-dropdown-wrap { position: relative; }
.profile-avatar {
  width: 40px; height: 40px; border-radius: 50%; border: 2px solid var(--accent);
  background: linear-gradient(135deg, #4facfe, #00f2fe); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all var(--transition-base); overflow: hidden;
}
.profile-avatar:hover { transform: scale(1.1); box-shadow: 0 0 0 4px rgba(163, 230, 53, 0.2); }
.avatar-initial { font-size: 1rem; font-weight: 800; color: white; }
.profile-dropdown {
  position: absolute; top: 52px; right: 0;
  background: var(--bg-card); border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg); min-width: 200px; padding: 8px 0;
  z-index: 200; border: 1px solid var(--border-color);
  transform-origin: top right;
}
.dropdown-header { padding: 12px 16px; }
.dropdown-name { display: block; font-weight: 700; color: var(--text-primary); font-size: 0.9rem; }
.dropdown-email { display: block; font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; }
.dropdown-divider { height: 1px; background: var(--border-color); margin: 4px 12px; }
.dropdown-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 16px; color: var(--text-primary); text-decoration: none;
  font-size: 0.85rem; transition: all var(--transition-fast);
}
.dropdown-item:hover { background: var(--bg-hover); }
.dropdown-icon { font-size: 1rem; }
.dropdown-danger { color: #ef4444; }
.dropdown-danger:hover { background: #fef2f2; }

.dropdown-enter-active, .dropdown-leave-active { transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: scale(0.92) translateY(-6px); }

/* ===== GRID ===== */
.dashboard-grid { display: grid; grid-template-columns: 1.4fr 0.9fr 0.7fr; gap: 20px; }

/* ===== HERO ===== */
.hero-card {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-radius: var(--radius-lg); padding: 24px;
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 20px; position: relative; overflow: hidden;
  transition: all var(--transition-slow);
}
.hero-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(22, 163, 74, 0.15); }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: white; color: #16a34a; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; margin-bottom: 10px; animation: fadeIn 0.5s ease-out both; animation-delay: 0.3s; }
.hero-content h2 { margin: 0 0 6px 0; font-size: 1.3rem; color: #166534; font-weight: 800; line-height: 1.3; }
.hero-content p { margin: 0 0 12px 0; color: #15803d; font-size: 0.8rem; }
.challenge-progress { margin-bottom: 12px; }
.challenge-bar { height: 8px; background: rgba(255,255,255,0.5); border-radius: 4px; overflow: hidden; margin-bottom: 6px; }
.challenge-fill { height: 100%; background: linear-gradient(90deg, #fbbf24, #f59e0b); border-radius: 4px; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
.challenge-text { font-size: 0.75rem; color: #166534; font-weight: 600; }
.fire { font-size: 1rem; display: inline-block; animation: flame 1.5s ease-in-out infinite; }
@keyframes flame { 0%, 100% { transform: scale(1) rotate(-5deg); } 50% { transform: scale(1.2) rotate(5deg); } }
.hero-avatars { display: flex; align-items: center; }
.avatar { width: 28px; height: 28px; background: #fde047; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; margin-right: -8px; border: 2px solid white; animation: popIn 0.4s ease-out both; }
.avatar:nth-child(1) { animation-delay: 0.5s; }
.avatar:nth-child(2) { animation-delay: 0.6s; }
.avatar:nth-child(3) { animation-delay: 0.7s; }
@keyframes popIn { from { opacity: 0; transform: scale(0) translateY(10px); } to { opacity: 1; transform: scale(1) translateY(0); } }
.avatar-more { margin-left: 14px; font-size: 0.7rem; color: #166534; font-weight: 600; }
.hero-image { position: relative; width: 100px; height: 80px; }
.food-plate { font-size: 3.5rem; position: absolute; right: 0; top: 0; }
.dumbbell { font-size: 1.5rem; position: absolute; color: #86efac; }
.dumbbell-1 { top: -10px; left: -20px; transform: rotate(-30deg); }
.dumbbell-2 { bottom: 0; right: 20px; transform: rotate(15deg); }
.float { animation: float 3s ease-in-out infinite; }
.float-slow { animation: float 4s ease-in-out infinite; animation-delay: 0.5s; }
.float-slow2 { animation: float 3.5s ease-in-out infinite; animation-delay: 1s; }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }

.bottom-row { display: grid; grid-template-columns: 1fr 1.2fr; gap: 20px; }

/* ===== CARDS ===== */
.recap-card, .meals-card, .calendar-card, .budget-card {
  background: var(--bg-card); border-radius: var(--radius-lg); padding: 20px;
  transition: all var(--transition-slow);
}
.recap-card:hover, .meals-card:hover, .calendar-card:hover, .budget-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.recap-card h3, .meals-card h3, .calendar-card h3, .budget-card h3 { margin: 0 0 16px 0; font-size: 0.95rem; color: var(--text-primary); transition: color var(--transition-slow); }

.macro-list { display: flex; flex-direction: column; gap: 14px; }
.macro-item { display: flex; align-items: center; gap: 10px; }
.macro-color { width: 32px; height: 32px; border-radius: 8px; flex-shrink: 0; animation: scaleIn 0.4s ease-out both; }
.macro-color.carbs { background: #67e8f9; }
.macro-color.protein { background: #fbbf24; }
.macro-color.fats { background: #86efac; }
.macro-info { flex: 1; }
.macro-name { display: block; font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 4px; transition: color var(--transition-slow); }
.macro-bar { display: block; height: 6px; background: var(--border-color); border-radius: 3px; overflow: hidden; transition: background var(--transition-slow); }
.macro-fill { display: block; height: 100%; border-radius: 3px; transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1); }
.macro-fill.carbs-fill { background: linear-gradient(90deg, #67e8f9, #22d3ee); }
.macro-fill.protein-fill { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
.macro-fill.fats-fill { background: linear-gradient(90deg, #86efac, #4ade80); }
.macro-pct { font-size: 0.8rem; font-weight: 700; color: var(--text-primary); min-width: 32px; text-align: right; transition: color var(--transition-slow); }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }

/* Meals */
.meal-list { display: flex; flex-direction: column; gap: 12px; }
.meal-row { display: flex; align-items: center; gap: 12px; padding: 10px 12px; background: var(--bg-hover); border-radius: var(--radius-sm); transition: all var(--transition-base); cursor: pointer; }
.meal-row:hover { background: var(--border-color); transform: translateX(4px); }
.meal-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.meal-dot.breakfast { background: #fbbf24; }
.meal-dot.lunch { background: #86efac; }
.meal-dot.dinner { background: #67e8f9; }
.meal-dot.snack { background: #c084fc; }
.meal-info { flex: 1; }
.meal-name { font-size: 0.8rem; font-weight: 700; color: var(--text-primary); transition: color var(--transition-slow); }
.meal-desc { font-size: 0.7rem; color: var(--text-muted); transition: color var(--transition-slow); }
.meal-cal { font-size: 0.8rem; font-weight: 700; color: var(--text-primary); transition: color var(--transition-slow); }
.meal-arrow { color: var(--text-muted); font-size: 0.9rem; transition: all var(--transition-base); }
.meal-row:hover .meal-arrow { transform: translateX(4px); color: #6366f1; }
.empty-meals { text-align: center; padding: 20px; color: var(--text-muted); font-size: 0.8rem; }
.remaining-bar { display: flex; align-items: center; gap: 8px; margin-top: 14px; font-size: 0.7rem; color: var(--text-muted); }
.rem-progress { flex: 1; height: 4px; background: var(--border-color); border-radius: 2px; overflow: hidden; transition: background var(--transition-slow); }
.rem-fill { height: 100%; background: linear-gradient(90deg, #fbbf24, #f59e0b); border-radius: 2px; transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1); }
.add-meal-btn { position: absolute; bottom: 20px; right: 20px; width: 36px; height: 36px; border-radius: 10px; background: var(--text-primary); color: var(--bg-card); border: none; font-size: 1.2rem; cursor: pointer; overflow: hidden; transition: all var(--transition-base); display: flex; align-items: center; justify-content: center; }
.add-meal-btn:hover { transform: scale(1.15); box-shadow: var(--shadow-md); }
.add-meal-btn:active { transform: scale(0.95); }
.btn-icon { display: block; transition: transform var(--transition-base); }
.add-meal-btn:hover .btn-icon { transform: rotate(90deg); }
.meal-slide-enter-active, .meal-slide-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.meal-slide-enter-from, .meal-slide-leave-to { opacity: 0; transform: translateX(20px); }

/* Activity */
.activity-card { background: #1e293b; border-radius: var(--radius-lg); padding: 20px; color: white; margin-bottom: 20px; transition: all var(--transition-slow); }
.activity-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(30, 41, 59, 0.25); }
.activity-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.activity-header h3 { margin: 0; font-size: 0.9rem; font-weight: 600; }
.activity-val { font-size: 0.75rem; color: #94a3b8; }
.chart-area { height: 100px; }
.activity-badge { display: inline-flex; flex-direction: column; background: white; color: #1e293b; padding: 8px 14px; border-radius: var(--radius-md); margin-top: 10px; animation: fadeInUp 0.5s ease-out both; animation-delay: 0.8s; }
.badge-pct { font-size: 0.85rem; font-weight: 700; }
.badge-label { font-size: 0.65rem; color: #94a3b8; }

/* Calendar */
.cal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.cal-month { font-size: 0.9rem; font-weight: 700; color: var(--text-primary); transition: color var(--transition-slow); }
.cal-nav { display: flex; gap: 6px; }
.cal-nav button { background: var(--bg-hover); border: none; border-radius: 8px; width: 28px; height: 28px; cursor: pointer; color: var(--text-secondary); font-size: 0.7rem; transition: all var(--transition-base); }
.cal-nav button:hover { background: var(--text-primary); color: var(--bg-card); transform: scale(1.1); }
.cal-days { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin-bottom: 6px; }
.cal-day-label { text-align: center; font-size: 0.65rem; color: var(--text-muted); font-weight: 600; transition: color var(--transition-slow); }
.cal-dates { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.cal-date { text-align: center; font-size: 0.7rem; padding: 6px 0; border-radius: 8px; color: var(--text-secondary); transition: all var(--transition-base); cursor: pointer; animation: fadeIn 0.3s ease-out both; }
.cal-date:hover { background: var(--bg-hover); transform: scale(1.15); }
.cal-date.today { background: var(--text-primary); color: var(--bg-card); font-weight: 700; animation: popIn 0.4s ease-out; }
.cal-date.active { background: #dcfce7; color: #166534; font-weight: 700; }

/* Budget */
.donut-wrap { position: relative; height: 140px; }
.donut-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.donut-val { display: block; font-size: 1.3rem; font-weight: 800; color: var(--text-primary); transition: color var(--transition-slow); }
.donut-label { font-size: 0.7rem; color: var(--text-muted); transition: color var(--transition-slow); }
.donut-legend { display: flex; justify-content: center; gap: 16px; margin-top: 12px; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.75rem; color: var(--text-secondary); transition: color var(--transition-slow); }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; }
.legend-dot.eaten { background: #fbbf24; }
.legend-dot.remaining { background: var(--border-color); transition: background var(--transition-slow); }

/* Water */
.water-tracker-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: var(--radius-lg); padding: 20px; color: white;
  position: relative; display: flex; justify-content: space-between; align-items: center;
  transition: all var(--transition-slow);
}
.water-tracker-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(79, 172, 254, 0.3); }
.water-content h3 { margin: 0 0 4px 0; font-size: 0.95rem; font-weight: 700; line-height: 1.3; }
.water-content p { margin: 0; font-size: 0.75rem; opacity: 0.9; }
.water-ring { position: relative; width: 70px; height: 70px; }
.water-ring svg { width: 100%; height: 100%; }
.water-progress { transition: stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1); }
.water-ring-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 0.75rem; font-weight: 700; }
.water-ring.pulse { animation: ringPulse 2s ease-in-out infinite; }
@keyframes ringPulse { 0%, 100% { filter: drop-shadow(0 0 0 rgba(255,255,255,0)); } 50% { filter: drop-shadow(0 0 8px rgba(255,255,255,0.6)); } }
.water-add { position: absolute; bottom: 14px; right: 14px; width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.25); color: white; border: none; font-size: 1.2rem; cursor: pointer; backdrop-filter: blur(4px); overflow: hidden; transition: all var(--transition-base); display: flex; align-items: center; justify-content: center; }
.water-add:hover { transform: scale(1.2); background: rgba(255,255,255,0.4); }
.water-add:active { transform: scale(0.9); }

/* Ripple */
.ripple { position: relative; overflow: hidden; }
.ripple::after { content: ''; position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; background-image: radial-gradient(circle, rgba(255,255,255,0.3) 10%, transparent 10.01%); background-repeat: no-repeat; background-position: 50%; transform: scale(10, 10); opacity: 0; transition: transform 0.5s, opacity 1s; }
.ripple:active::after { transform: scale(0, 0); opacity: 0.3; transition: 0s; }

.loading { text-align: center; padding: 80px; color: var(--text-muted); }

@media (max-width: 1100px) {
  .dashboard-grid { grid-template-columns: 1fr 1fr; }
  .col-right { grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
}
@media (max-width: 800px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .col-right { grid-column: auto; display: flex; flex-direction: column; }
  .bottom-row { grid-template-columns: 1fr; }
  .sidebar { width: 60px; }
  .nav-label { display: none; }
  .nav-item { justify-content: center; padding: 0; margin: 0 4px; }
  .header-actions { gap: 6px; }
  .search-box { display: none; }
}
</style>
