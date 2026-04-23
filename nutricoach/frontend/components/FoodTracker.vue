<template>
  <div class="tracker-page">
    <header class="page-header">
      <h2>Food Tracker</h2>
    </header>

    <div class="tracker-layout">
      <div class="log-section">
        <h3>Log a Meal</h3>
        <form @submit.prevent="logMeal">
          <div class="form-group">
            <label>Food Name</label>
            <input type="text" v-model="form.name" required placeholder="e.g., Roti with Dal" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Calories</label>
              <input type="number" v-model.number="form.calories" placeholder="0" min="0" />
            </div>
            <div class="form-group">
              <label>Meal Type</label>
              <select v-model="form.meal_type">
                <option value="breakfast">Breakfast</option>
                <option value="lunch">Lunch</option>
                <option value="dinner">Dinner</option>
                <option value="snack">Snack</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Protein (g)</label>
              <input type="number" v-model.number="form.protein" placeholder="0" min="0" step="0.1" />
            </div>
            <div class="form-group">
              <label>Carbs (g)</label>
              <input type="number" v-model.number="form.carbs" placeholder="0" min="0" step="0.1" />
            </div>
            <div class="form-group">
              <label>Fats (g)</label>
              <input type="number" v-model.number="form.fats" placeholder="0" min="0" step="0.1" />
            </div>
          </div>
          <button type="submit" :disabled="logging">{{ logging ? 'Logging...' : 'Log Meal' }}</button>
        </form>
      </div>

      <div class="today-section">
        <h3>Today's Log</h3>
        <div class="calorie-summary">
          <div class="calorie-bar">
            <div class="calorie-fill" :style="{ width: caloriePercent + '%' }"></div>
          </div>
          <p>{{ todayTotal }} / {{ targetCalories }} kcal</p>
        </div>

        <div v-if="todayMeals.length" class="meals-list">
          <div v-for="meal in todayMeals" :key="meal.id" class="meal-item">
            <div class="meal-info">
              <span class="meal-type-tag">{{ meal.meal_type }}</span>
              <strong>{{ meal.name }}</strong>
            </div>
            <div class="meal-macros">
              <span>{{ meal.calories }} kcal</span>
              <span>P:{{ meal.protein }}g</span>
              <span>C:{{ meal.carbs }}g</span>
              <span>F:{{ meal.fats }}g</span>
            </div>
          </div>
        </div>
        <p v-else class="empty">No meals logged today.</p>
      </div>
    </div>

    <div class="weight-section">
      <h3>Log Weight</h3>
      <form @submit.prevent="logWeight" class="weight-form">
        <input type="number" v-model.number="weightInput" required placeholder="Weight in kg" step="0.1" min="20" />
        <button type="submit" :disabled="weightLogging">{{ weightLogging ? 'Saving...' : 'Log Weight' }}</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../src/api'

export default {
  data() {
    return {
      form: { name: '', calories: null, protein: null, carbs: null, fats: null, meal_type: 'lunch' },
      todayMeals: [],
      todayTotal: 0,
      targetCalories: 2000,
      logging: false,
      weightInput: null,
      weightLogging: false
    }
  },
  computed: {
    caloriePercent() {
      return Math.min((this.todayTotal / this.targetCalories) * 100, 100)
    }
  },
  mounted() {
    this.loadTodayMeals()
    this.loadTarget()
  },
  methods: {
    async loadTodayMeals() {
      try {
        const response = await api.get('/meals/today')
        this.todayMeals = response.data.meals
        this.todayTotal = response.data.total_calories
      } catch (e) {
        console.error('Failed to load meals:', e)
      }
    },
    async loadTarget() {
      try {
        const response = await api.get('/health/profile')
        if (response.data.target_calories) {
          this.targetCalories = response.data.target_calories
        }
      } catch (e) {
        // May not exist yet, use default
      }
    },
    async logMeal() {
      this.logging = true
      try {
        await api.post('/meals/log', {
          name: this.form.name,
          calories: this.form.calories || 0,
          protein: this.form.protein || 0,
          carbs: this.form.carbs || 0,
          fats: this.form.fats || 0,
          meal_type: this.form.meal_type
        })
        this.form = { name: '', calories: null, protein: null, carbs: null, fats: null, meal_type: 'lunch' }
        await this.loadTodayMeals()
      } catch (e) {
        console.error('Failed to log meal:', e)
      } finally {
        this.logging = false
      }
    },
    async logWeight() {
      this.weightLogging = true
      try {
        await api.post('/weight/log', { weight: this.weightInput })
        this.weightInput = null
      } catch (e) {
        console.error('Failed to log weight:', e)
      } finally {
        this.weightLogging = false
      }
    }
  }
}
</script>

<style scoped>
.tracker-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px 20px;
  font-family: Arial, sans-serif;
}
h2 { color: #333; }
h3 { color: #555; margin-bottom: 12px; }
.tracker-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
.form-group { margin-bottom: 10px; }
.form-row { display: flex; gap: 10px; }
.form-row .form-group { flex: 1; }
label { display: block; margin-bottom: 2px; color: #555; font-size: 0.85rem; }
input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
}
button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
}
button:hover { background-color: #45a049; }
button:disabled { background-color: #a5d6a7; cursor: not-allowed; }
.log-section, .today-section { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.calorie-summary { margin-bottom: 16px; }
.calorie-bar { background: #e0e0e0; border-radius: 8px; height: 12px; overflow: hidden; margin-bottom: 6px; }
.calorie-fill { background: #4CAF50; height: 100%; border-radius: 8px; transition: width 0.3s; }
.calorie-summary p { margin: 0; font-size: 0.85rem; color: #666; text-align: center; }
.meals-list { max-height: 300px; overflow-y: auto; }
.meal-item { padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
.meal-info { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.meal-type-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.7rem;
  background: #e8f5e9;
  color: #2e7d32;
  font-weight: bold;
  text-transform: capitalize;
}
.meal-macros { display: flex; gap: 10px; color: #888; font-size: 0.8rem; }
.empty { color: #999; text-align: center; padding: 20px; }
.weight-section { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.weight-form { display: flex; gap: 12px; align-items: flex-end; }
.weight-form input { flex: 1; }
.weight-form button { width: auto; }
@media (max-width: 700px) {
  .tracker-layout { grid-template-columns: 1fr; }
}
</style>
