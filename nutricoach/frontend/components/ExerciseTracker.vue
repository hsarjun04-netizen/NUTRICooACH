<template>
  <div class="exercise-tracker">
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

    <main class="main-content">
      <header class="page-header">
        <h1>&#127939; Exercise Tracker</h1>
        <p class="subtitle">Log your workouts and track your fitness progress</p>
      </header>

      <!-- Today's Summary -->
      <div class="summary-cards">
        <div class="summary-card calories-card">
          <span class="summary-icon">&#128293;</span>
          <div class="summary-info">
            <span class="summary-value">{{ todayStats.total_calories_burned || 0 }}</span>
            <span class="summary-label">Calories Burned</span>
          </div>
        </div>
        <div class="summary-card duration-card">
          <span class="summary-icon">&#9201;</span>
          <div class="summary-info">
            <span class="summary-value">{{ todayStats.total_duration_minutes || 0 }}</span>
            <span class="summary-label">Minutes Active</span>
          </div>
        </div>
        <div class="summary-card workouts-card">
          <span class="summary-icon">&#127942;</span>
          <div class="summary-info">
            <span class="summary-value">{{ todayStats.exercises ? todayStats.exercises.length : 0 }}</span>
            <span class="summary-label">Workouts Today</span>
          </div>
        </div>
      </div>

      <!-- Log Exercise Form -->
      <div class="card form-card">
        <h3>&#128170; Log Exercise</h3>
        <form @submit.prevent="logExercise">
          <div class="form-row">
            <div class="form-group">
              <label>Exercise Name</label>
              <input 
                v-model="exerciseForm.exercise_name" 
                type="text" 
                placeholder="e.g., Running, Weight Training" 
                required 
                list="exercise-suggestions"
                @input="autoFillExercise"
              />
              <datalist id="exercise-suggestions">
                <option v-for="ex in exerciseSuggestions" :key="ex.name" :value="ex.name"></option>
              </datalist>
            </div>
            <div class="form-group small">
              <label>Intensity</label>
              <select v-model="exerciseForm.intensity">
                <option value="low">Low</option>
                <option value="moderate">Moderate</option>
                <option value="high">High</option>
                <option value="very high">Very High</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Duration (minutes)</label>
              <input v-model.number="exerciseForm.duration_minutes" type="number" placeholder="30" min="1" required />
            </div>
            <div class="form-group">
              <label>Calories Burned</label>
              <input v-model.number="exerciseForm.calories_burned" type="number" placeholder="Auto" min="0" :class="{ 'auto-filled': showAutoFillBadge }" />
              <div v-if="showAutoFillBadge" class="auto-fill-badge">
                <span class="badge-icon">&#10003;</span> Estimated
              </div>
            </div>
            <div class="form-group">
              <label>Date</label>
              <input v-model="exerciseForm.date" type="date" :max="today" />
            </div>
          </div>
          <div class="form-group full">
            <label>Notes (optional)</label>
            <input v-model="exerciseForm.notes" type="text" placeholder="e.g., Felt great, increased weight" />
          </div>
          <button type="submit" :disabled="saving" class="btn-primary">
            {{ saving ? 'Saving...' : 'Log Exercise' }}
          </button>
        </form>
      </div>

      <!-- Today's Exercises -->
      <div class="exercises-section">
        <h3>Today's Workouts</h3>
        <div v-if="todayExercises.length" class="exercises-list">
          <div v-for="exercise in todayExercises" :key="exercise.id" class="exercise-card" :class="exercise.intensity || 'moderate'">
            <div class="exercise-header">
              <div class="exercise-name">
                <span class="exercise-icon">{{ getExerciseIcon(exercise.exercise_name) }}</span>
                <h4>{{ exercise.exercise_name }}</h4>
              </div>
              <span class="intensity-badge" :class="exercise.intensity || 'moderate'">{{ exercise.intensity || 'moderate' }}</span>
            </div>
            <div class="exercise-stats">
              <div class="stat">
                <span class="stat-icon">&#9201;</span>
                <span>{{ exercise.duration_minutes || 0 }} min</span>
              </div>
              <div class="stat">
                <span class="stat-icon">&#128293;</span>
                <span>{{ exercise.calories_burned ? Math.round(exercise.calories_burned) : 0 }} kcal</span>
              </div>
              <div class="stat">
                <span class="stat-icon">&#128197;</span>
                <span>{{ formatDate(exercise.date) }}</span>
              </div>
            </div>
            <p v-if="exercise.notes" class="exercise-notes">{{ exercise.notes }}</p>
          </div>
        </div>
        <div v-else class="empty-state">
          <div class="empty-icon">&#127939;</div>
          <h3>No exercises logged today</h3>
          <p>Start by logging your first workout above!</p>
        </div>
      </div>

      <!-- Exercise History -->
      <div class="history-section">
        <h3>&#128203; Exercise History</h3>
        <div v-if="loadingHistory" class="loading-state">
          <div class="spinner"></div>
          <p>Loading history...</p>
        </div>
        <div v-else-if="exerciseHistory.length" class="history-table">
          <div class="table-header">
            <span>Date</span>
            <span>Exercise</span>
            <span>Duration</span>
            <span>Calories</span>
            <span>Intensity</span>
          </div>
          <div v-for="ex in exerciseHistory" :key="ex.id" class="table-row">
            <span>{{ formatDate(ex.date) }}</span>
            <span class="exercise-name-cell">{{ getExerciseIcon(ex.exercise_name) }} {{ ex.exercise_name }}</span>
            <span>{{ ex.duration_minutes || 0 }} min</span>
            <span>{{ ex.calories_burned ? Math.round(ex.calories_burned) : 0 }} kcal</span>
            <span>
              <span class="intensity-badge small" :class="ex.intensity || 'moderate'">{{ ex.intensity || 'moderate' }}</span>
            </span>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>No exercise history yet. Start logging your workouts!</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../src/stores/auth'
import { useThemeStore } from '../src/stores/theme'
import api, { logExercise as logExerciseApi, getExerciseHistory, getTodayExercise } from '../src/api'

const router = useRouter()
const auth = useAuthStore()
const theme = useThemeStore()

const exerciseForm = ref({
  exercise_name: '',
  duration_minutes: null,
  calories_burned: null,
  intensity: 'moderate',
  date: new Date().toISOString().split('T')[0],
  notes: ''
})

const todayStats = ref({})
const todayExercises = ref([])
const exerciseHistory = ref([])
const loadingHistory = ref(false)
const saving = ref(false)
const showAutoFillBadge = ref(false)

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: '&#127968;' },
  { to: '/meal-plan', label: 'Meal Plan', icon: '&#128197;' },
  { to: '/tracker', label: 'Food Tracker', icon: '&#127859;' },
  { to: '/recipes', label: 'Recipes', icon: '&#128214;' },
  { to: '/shopping-list', label: 'Shopping List', icon: '&#128722;' },
  { to: '/exercises', label: 'Exercise Tracker', icon: '&#127939;' },
  { to: '/progress', label: 'Progress', icon: '&#128200;' },
  { to: '/profile', label: 'Profile', icon: '&#9881;' }
]

const exerciseDatabase = [
  { name: 'Running', caloriesPerMin: 11.5, category: 'cardio' },
  { name: 'Walking', caloriesPerMin: 4.5, category: 'cardio' },
  { name: 'Cycling', caloriesPerMin: 8.5, category: 'cardio' },
  { name: 'Swimming', caloriesPerMin: 9.5, category: 'cardio' },
  { name: 'Weight Training', caloriesPerMin: 6, category: 'strength' },
  { name: 'Yoga', caloriesPerMin: 3.5, category: 'flexibility' },
  { name: 'HIIT', caloriesPerMin: 12, category: 'cardio' },
  { name: 'Jump Rope', caloriesPerMin: 11, category: 'cardio' },
  { name: 'Push-ups', caloriesPerMin: 7, category: 'strength' },
  { name: 'Squats', caloriesPerMin: 6.5, category: 'strength' },
  { name: 'Plank', caloriesPerMin: 4, category: 'core' },
  { name: 'Burpees', caloriesPerMin: 12, category: 'cardio' },
  { name: 'Lunges', caloriesPerMin: 6, category: 'strength' },
  { name: 'Pull-ups', caloriesPerMin: 7.5, category: 'strength' },
  { name: 'Dancing', caloriesPerMin: 7, category: 'cardio' },
  { name: 'Boxing', caloriesPerMin: 10, category: 'cardio' },
  { name: 'Rowing', caloriesPerMin: 9, category: 'cardio' },
  { name: 'Elliptical', caloriesPerMin: 8, category: 'cardio' },
  { name: 'Stair Climbing', caloriesPerMin: 9.5, category: 'cardio' },
  { name: 'Pilates', caloriesPerMin: 4.5, category: 'flexibility' }
]

const exerciseSuggestions = computed(() => {
  if (!exerciseForm.value.exercise_name || exerciseForm.value.exercise_name.length < 2) {
    return exerciseDatabase
  }
  const search = exerciseForm.value.exercise_name.toLowerCase()
  return exerciseDatabase.filter(ex => 
    ex.name.toLowerCase().includes(search)
  ).slice(0, 10)
})

const today = computed(() => {
  return new Date().toISOString().split('T')[0]
})

const logout = () => {
  auth.logout()
  router.push('/login')
}

const autoFillExercise = () => {
  if (!exerciseForm.value.exercise_name || !exerciseForm.value.duration_minutes) {
    return
  }
  
  const search = exerciseForm.value.exercise_name.toLowerCase()
  const matchedExercise = exerciseDatabase.find(ex => 
    ex.name.toLowerCase() === search || 
    ex.name.toLowerCase().includes(search)
  )
  
  if (matchedExercise && exerciseForm.value.duration_minutes) {
    // Adjust calories based on intensity
    const intensityMultipliers = {
      'low': 0.7,
      'moderate': 1.0,
      'high': 1.3,
      'very high': 1.6
    }
    
    const multiplier = intensityMultipliers[exerciseForm.value.intensity] || 1.0
    const estimatedCalories = Math.round(matchedExercise.caloriesPerMin * exerciseForm.value.duration_minutes * multiplier)
    
    exerciseForm.value.calories_burned = estimatedCalories
    
    showAutoFillBadge.value = true
    setTimeout(() => {
      showAutoFillBadge.value = false
    }, 2000)
  }
}

const getExerciseIcon = (name) => {
  if (!name) return '&#127939;'
  const lower = name.toLowerCase()
  if (lower.includes('run')) return '&#127939;'
  if (lower.includes('walk')) return '&#128694;'
  if (lower.includes('cycle') || lower.includes('bike')) return '&#128690;'
  if (lower.includes('swim')) return '&#127946;'
  if (lower.includes('weight') || lower.includes('strength')) return '&#127947;'
  if (lower.includes('yoga')) return '&#129492;'
  if (lower.includes('hiit')) return '&#128293;'
  if (lower.includes('jump')) return '&#9917;'
  if (lower.includes('push-up')) return '&#128170;'
  if (lower.includes('squat')) return '&#127939;'
  if (lower.includes('plank')) return '&#128203;'
  if (lower.includes('burpee')) return '&#128165;'
  if (lower.includes('lunge')) return '&#127939;'
  if (lower.includes('pull-up')) return '&#128170;'
  if (lower.includes('dance')) return '&#128131;'
  if (lower.includes('box')) return '&#129342;'
  if (lower.includes('row')) return '&#128675;'
  if (lower.includes('elliptical')) return '&#127939;'
  if (lower.includes('stair')) return '&#127968;'
  if (lower.includes('pilates')) return '&#129492;'
  return '&#127939;'
}

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const logExercise = async () => {
  saving.value = true
  try {
    const response = await logExerciseApi(exerciseForm.value)
    
    // Show calculated calories from backend
    const calculatedCalories = response.data.calories_calculated
    if (calculatedCalories) {
      alert(`Exercise logged successfully! Calories burned: ${calculatedCalories} kcal`)
    } else {
      alert('Exercise logged successfully!')
    }
    
    // Reset form
    exerciseForm.value = {
      exercise_name: '',
      duration_minutes: null,
      calories_burned: null,
      intensity: 'moderate',
      date: new Date().toISOString().split('T')[0],
      notes: ''
    }
    
    // Reload data
    await loadTodayExercise()
    await loadExerciseHistory()
  } catch (error) {
    console.error('Failed to log exercise:', error)
    alert('Failed to log exercise. Please try again.')
  } finally {
    saving.value = false
  }
}

const loadTodayExercise = async () => {
  try {
    const response = await getTodayExercise()
    todayStats.value = response.data
    todayExercises.value = response.data.exercises || []
  } catch (error) {
    console.error('Failed to load today exercises:', error)
  }
}

const loadExerciseHistory = async () => {
  loadingHistory.value = true
  try {
    const response = await getExerciseHistory()
    exerciseHistory.value = response.data.exercises || []
  } catch (error) {
    console.error('Failed to load exercise history:', error)
  } finally {
    loadingHistory.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    loadTodayExercise(),
    loadExerciseHistory()
  ])
})
</script>

<style scoped>
.exercise-tracker {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 200px;
  background: #1a1a2e;
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-brand {
  font-size: 24px;
  font-weight: bold;
  padding: 0 20px;
  margin-bottom: 30px;
  color: #16c79a;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: #8b8b9e;
  text-decoration: none;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.nav-item:hover,
.nav-item.active {
  background: #16213e;
  color: #16c79a;
  border-left-color: #16c79a;
}

.nav-icon {
  font-size: 20px;
}

.nav-label {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #16213e;
}

.main-content {
  flex: 1;
  margin-left: 200px;
  padding: 30px;
  background: #f8f9fa;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 32px;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.subtitle {
  color: #8b8b9e;
  font-size: 16px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.summary-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.summary-icon {
  font-size: 48px;
  opacity: 0.8;
}

.calories-card .summary-icon { color: #ef4444; }
.duration-card .summary-icon { color: #3b82f6; }
.workouts-card .summary-icon { color: #f59e0b; }

.summary-info {
  display: flex;
  flex-direction: column;
}

.summary-value {
  font-size: 32px;
  font-weight: bold;
  color: #1a1a2e;
}

.summary-label {
  font-size: 14px;
  color: #8b8b9e;
  font-weight: 500;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card h3 {
  font-size: 20px;
  color: #1a1a2e;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  position: relative;
}

.form-group.small {
  flex: 0.5;
}

.form-group.full {
  margin-bottom: 15px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a2e;
}

.form-group input,
.form-group select {
  padding: 10px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #16c79a;
  box-shadow: 0 0 0 3px rgba(22, 199, 154, 0.1);
}

.form-group input.auto-filled {
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  border-color: #10b981;
  font-weight: 600;
  color: #059669;
}

.auto-fill-badge {
  position: absolute;
  right: 10px;
  top: 35px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  animation: slideIn 0.3s ease-out;
}

.badge-icon {
  font-size: 12px;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.btn-primary {
  width: 100%;
  padding: 12px 24px;
  background: #16c79a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #13b386;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.exercises-section,
.history-section {
  margin-bottom: 30px;
}

.exercises-section h3,
.history-section h3 {
  font-size: 24px;
  color: #1a1a2e;
  margin-bottom: 20px;
}

.exercises-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.exercise-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #3b82f6;
}

.exercise-card.low { border-left-color: #22c55e; }
.exercise-card.moderate { border-left-color: #3b82f6; }
.exercise-card.high { border-left-color: #f59e0b; }
.exercise-card.very-high { border-left-color: #ef4444; }

.exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.exercise-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.exercise-icon {
  font-size: 32px;
}

.exercise-name h4 {
  font-size: 18px;
  color: #1a1a2e;
  margin: 0;
}

.intensity-badge {
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.intensity-badge.low {
  background: #dcfce7;
  color: #166534;
}

.intensity-badge.moderate {
  background: #dbeafe;
  color: #1e40af;
}

.intensity-badge.high {
  background: #fef3c7;
  color: #92400e;
}

.intensity-badge.very-high {
  background: #fee2e2;
  color: #991b1b;
}

.intensity-badge.small {
  padding: 4px 8px;
  font-size: 11px;
}

.exercise-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 10px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #6b7280;
}

.stat-icon {
  font-size: 16px;
}

.exercise-notes {
  margin: 10px 0 0 0;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
  font-size: 14px;
  color: #6b7280;
  font-style: italic;
}

.history-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: grid;
  grid-template-columns: 100px 2fr 100px 100px 100px;
  padding: 15px 20px;
  background: #1a1a2e;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.table-row {
  display: grid;
  grid-template-columns: 100px 2fr 100px 100px 100px;
  padding: 15px 20px;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
  color: #1a1a2e;
  align-items: center;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: #f8f9fa;
}

.exercise-name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f0f0f0;
  border-top-color: #16c79a;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 24px;
  color: #1a1a2e;
  margin-bottom: 10px;
}

.empty-state p {
  color: #8b8b9e;
  font-size: 16px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 64px;
  }
  
  .nav-label {
    display: none;
  }
  
  .main-content {
    margin-left: 64px;
    padding: 20px;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 80px 1.5fr 70px 70px;
  }
  
  .table-header span:nth-child(5),
  .table-row span:nth-child(5) {
    display: none;
  }
}
</style>
