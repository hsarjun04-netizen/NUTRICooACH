<template>
  <div class="tracker-page">
    <div class="tracker-container">
      <div class="page-header">
        <h1>Meal Tracker</h1>
        <p class="subtitle">Log your meals and track your nutrition</p>
      </div>

      <!-- Add Meal Form -->
      <div class="card form-card">
        <h3>Add a Meal</h3>
        <form @submit.prevent="logMeal">
          <div class="form-row">
            <div class="form-group">
              <label>Meal Name</label>
              <input v-model="mealForm.name" type="text" placeholder="e.g., Grilled Chicken Salad" required />
            </div>
            <div class="form-group small">
              <label>Type</label>
              <select v-model="mealForm.meal_type">
                <option value="breakfast">Breakfast</option>
                <option value="lunch">Lunch</option>
                <option value="dinner">Dinner</option>
                <option value="snack">Snack</option>
              </select>
            </div>
          </div>
          <div class="form-row macros">
            <div class="form-group">
              <label>Calories</label>
              <input v-model.number="mealForm.calories" type="number" placeholder="0" min="0" />
            </div>
            <div class="form-group">
              <label>Protein (g)</label>
              <input v-model.number="mealForm.protein" type="number" placeholder="0" min="0" />
            </div>
            <div class="form-group">
              <label>Carbs (g)</label>
              <input v-model.number="mealForm.carbs" type="number" placeholder="0" min="0" />
            </div>
            <div class="form-group">
              <label>Fats (g)</label>
              <input v-model.number="mealForm.fats" type="number" placeholder="0" min="0" />
            </div>
          </div>
          <button type="submit" :disabled="saving" class="submit-btn">{{ saving ? 'Saving...' : 'Log Meal' }}</button>
        </form>
      </div>

      <!-- Today's Summary -->
      <div class="summary-bar">
        <div class="summary-item">
          <span class="summary-value">{{ todayCalories }}</span>
          <span class="summary-label">kcal</span>
        </div>
        <div class="summary-item">
          <span class="summary-value">{{ todayProtein }}g</span>
          <span class="summary-label">Protein</span>
        </div>
        <div class="summary-item">
          <span class="summary-value">{{ todayCarbs }}g</span>
          <span class="summary-label">Carbs</span>
        </div>
        <div class="summary-item">
          <span class="summary-value">{{ todayFats }}g</span>
          <span class="summary-label">Fats</span>
        </div>
      </div>

      <!-- Meal Cards -->
      <div class="meals-section">
        <h3>Today's Meals</h3>
        <div v-if="meals.length" class="meals-grid">
          <div v-for="meal in meals" :key="meal.id" class="meal-card" :class="meal.meal_type">
            <div class="meal-header">
              <span class="meal-type-badge">{{ meal.meal_type }}</span>
              <span class="meal-calories">{{ meal.calories }} kcal</span>
            </div>
            <div class="meal-name">{{ meal.name }}</div>
            <div class="meal-macros">
              <span>P: {{ meal.protein || 0 }}g</span>
              <span>C: {{ meal.carbs || 0 }}g</span>
              <span>F: {{ meal.fats || 0 }}g</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>No meals logged today. Start by adding your first meal above!</p>
        </div>
      </div>

      <!-- Log Weight -->
      <div class="card weight-card">
        <h3>Log Weight</h3>
        <form @submit.prevent="logWeight">
          <div class="weight-row">
            <input v-model.number="weightForm.weight" type="number" step="0.1" placeholder="Weight in kg" required />
            <button type="submit" :disabled="savingWeight">{{ savingWeight ? 'Saving...' : 'Log Weight' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../src/api'

export default {
  data() {
    return {
      meals: [],
      mealForm: {
        name: '',
        calories: null,
        protein: null,
        carbs: null,
        fats: null,
        meal_type: 'breakfast'
      },
      weightForm: { weight: null },
      saving: false,
      savingWeight: false
    }
  },
  computed: {
    todayCalories() {
      return this.meals.reduce((sum, m) => sum + (m.calories || 0), 0)
    },
    todayProtein() {
      return this.meals.reduce((sum, m) => sum + (m.protein || 0), 0)
    },
    todayCarbs() {
      return this.meals.reduce((sum, m) => sum + (m.carbs || 0), 0)
    },
    todayFats() {
      return this.meals.reduce((sum, m) => sum + (m.fats || 0), 0)
    }
  },
  mounted() {
    this.loadMeals()
  },
  methods: {
    async loadMeals() {
      try {
        const res = await api.get('/meals/today')
        this.meals = res.data.meals || []
      } catch (e) {
        console.error('Failed to load meals:', e)
      }
    },
    async logMeal() {
      this.saving = true
      try {
        await api.post('/meals/log', this.mealForm)
        this.mealForm = { name: '', calories: null, protein: null, carbs: null, fats: null, meal_type: 'breakfast' }
        await this.loadMeals()
      } catch (e) {
        console.error('Failed to log meal:', e)
        alert('Failed to log meal')
      } finally {
        this.saving = false
      }
    },
    async logWeight() {
      this.savingWeight = true
      try {
        await api.post('/weight/log', this.weightForm)
        this.weightForm.weight = null
        alert('Weight logged successfully!')
      } catch (e) {
        console.error('Failed to log weight:', e)
        alert('Failed to log weight')
      } finally {
        this.savingWeight = false
      }
    }
  }
}
</script>

<style scoped>
.tracker-page { max-width: 800px; margin: 0 auto; padding: 32px 20px; font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; min-height: 100vh; }
.tracker-container { display: flex; flex-direction: column; gap: 20px; }
.page-header { margin-bottom: 4px; }
.page-header h1 { margin: 0; font-size: 1.5rem; color: #1a1a2e; }
.subtitle { margin: 4px 0 0 0; color: #888; font-size: 0.9rem; }

.card {
  background: white;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.card h3 { margin: 0 0 16px 0; font-size: 1rem; color: #333; }

.form-row { display: flex; gap: 14px; margin-bottom: 14px; }
.form-row .form-group { flex: 1; }
.form-row .form-group.small { flex: 0.4; }
.form-group label { display: block; margin-bottom: 5px; font-size: 0.8rem; color: #666; font-weight: 500; }
.form-group input, .form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  box-sizing: border-box;
  background: #fafafa;
}
.form-group input:focus, .form-group select:focus { outline: none; border-color: #4CAF50; background: white; }

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 4px;
}
.submit-btn:hover { background: #45a049; }
.submit-btn:disabled { background: #a5d6a7; cursor: not-allowed; }

.summary-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
.summary-item {
  background: white;
  border-radius: 14px;
  padding: 18px;
  text-align: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.summary-value { display: block; font-size: 1.4rem; font-weight: 700; color: #1a1a2e; }
.summary-label { font-size: 0.75rem; color: #999; text-transform: uppercase; letter-spacing: 0.5px; }

.meals-section h3 { margin: 8px 0 14px 0; font-size: 1rem; color: #333; }
.meals-grid { display: flex; flex-direction: column; gap: 12px; }
.meal-card {
  background: white;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  border-left: 4px solid #ccc;
}
.meal-card.breakfast { border-left-color: #FF9800; }
.meal-card.lunch { border-left-color: #4CAF50; }
.meal-card.dinner { border-left-color: #2196F3; }
.meal-card.snack { border-left-color: #9c27b0; }
.meal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.meal-type-badge {
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: 700;
  color: #888;
  letter-spacing: 0.5px;
}
.meal-calories { font-size: 0.85rem; font-weight: 700; color: #2e7d32; }
.meal-name { font-size: 1rem; font-weight: 600; color: #333; margin-bottom: 8px; }
.meal-macros { display: flex; gap: 16px; }
.meal-macros span { font-size: 0.8rem; color: #888; }

.empty-state { text-align: center; padding: 30px; color: #bbb; font-size: 0.9rem; }

.weight-card .weight-row { display: flex; gap: 12px; }
.weight-card input { flex: 1; padding: 10px 12px; border: 1px solid #e0e0e0; border-radius: 8px; font-size: 0.95rem; }
.weight-card button {
  padding: 10px 20px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.weight-card button:hover { background: #1976d2; }
.weight-card button:disabled { background: #90caf9; cursor: not-allowed; }

@media (max-width: 600px) {
  .form-row { flex-direction: column; gap: 10px; }
  .form-row.macros { display: grid; grid-template-columns: 1fr 1fr; }
  .summary-bar { grid-template-columns: 1fr 1fr; }
}
</style>
