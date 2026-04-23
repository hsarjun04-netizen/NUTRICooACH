<template>
  <div class="meal-plan-page">
    <header class="page-header">
      <h2>Your Meal Plan</h2>
      <button @click="generateNewPlan" :disabled="generating">
        {{ generating ? 'Generating...' : 'Generate New Plan' }}
      </button>
    </header>

    <div v-if="plan && plan.meals.length" class="plan-container">
      <div v-if="plan.safety_warnings && plan.safety_warnings.length" class="safety-banner">
        <div v-for="(warning, idx) in plan.safety_warnings" :key="idx" class="warning-item">
          <span class="warning-icon">&#9888;</span> {{ warning }}
        </div>
      </div>

      <div v-if="plan.medical_conditions && plan.medical_conditions.length" class="medical-badge-bar">
        <span class="medical-label">Tailored for:</span>
        <span v-for="condition in plan.medical_conditions" :key="condition" class="medical-badge">
          {{ condition }}
        </span>
      </div>
      <div class="summary-bar">
        <div class="summary-item">
          <span class="label">Total Calories</span>
          <span class="value">{{ plan.total_calories }} kcal</span>
        </div>
        <div class="summary-item">
          <span class="label">Protein</span>
          <span class="value">{{ plan.total_protein }}g</span>
        </div>
        <div class="summary-item">
          <span class="label">Carbs</span>
          <span class="value">{{ plan.total_carbs }}g</span>
        </div>
        <div class="summary-item">
          <span class="label">Fats</span>
          <span class="value">{{ plan.total_fats }}g</span>
        </div>
      </div>

      <div class="meals-grid">
        <div v-for="meal in plan.meals" :key="meal.name" class="meal-card" :class="meal.meal_type">
          <div class="meal-type-badge">{{ formatMealType(meal.meal_type) }}</div>
          <h3>{{ meal.name }}</h3>
          <div class="macros">
            <span>{{ meal.calories }} kcal</span>
            <span>P: {{ meal.protein }}g</span>
            <span>C: {{ meal.carbs }}g</span>
            <span>F: {{ meal.fats }}g</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>No meal plan generated yet.</p>
      <button @click="generateNewPlan" :disabled="generating">Generate Your First Plan</button>
    </div>
  </div>
</template>

<script>
import api from '../src/api'

export default {
  data() {
    return { plan: null, generating: false }
  },
  mounted() {
    this.loadCurrentPlan()
  },
  methods: {
    async loadCurrentPlan() {
      try {
        const response = await api.get('/meal-plans/current')
        this.plan = response.data
      } catch (e) {
        console.error('Failed to load meal plan:', e)
      }
    },
    async generateNewPlan() {
      this.generating = true
      try {
        const response = await api.post('/meal-plans/generate')
        this.plan = response.data
      } catch (e) {
        console.error('Failed to generate plan:', e)
      } finally {
        this.generating = false
      }
    },
    formatMealType(type) {
      return type.charAt(0).toUpperCase() + type.slice(1)
    }
  }
}
</script>

<style scoped>
.meal-plan-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px 20px;
  font-family: Arial, sans-serif;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
h2 { color: #333; margin: 0; }
button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  cursor: pointer;
}
button:hover { background-color: #45a049; }
button:disabled { background-color: #a5d6a7; cursor: not-allowed; }
.summary-bar {
  display: flex;
  gap: 16px;
  background: #e8f5e9;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.summary-item { flex: 1; text-align: center; min-width: 100px; }
.summary-item .label { display: block; color: #666; font-size: 0.8rem; }
.summary-item .value { display: block; font-size: 1.2rem; font-weight: bold; color: #2e7d32; }
.meals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.meal-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border-left: 4px solid #4CAF50;
}
.meal-card.breakfast { border-left-color: #FF9800; }
.meal-card.lunch { border-left-color: #4CAF50; }
.meal-card.dinner { border-left-color: #2196F3; }
.meal-card.snack { border-left-color: #9C27B0; }
.meal-type-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  color: white;
  background: #666;
  margin-bottom: 8px;
}
.breakfast .meal-type-badge { background: #FF9800; }
.lunch .meal-type-badge { background: #4CAF50; }
.dinner .meal-type-badge { background: #2196F3; }
.snack .meal-type-badge { background: #9C27B0; }
h3 { margin: 0 0 8px 0; color: #333; font-size: 1.05rem; }
.macros { display: flex; gap: 12px; flex-wrap: wrap; color: #666; font-size: 0.85rem; }
.empty-state { text-align: center; padding: 60px 20px; color: #999; }
.safety-banner { background: #fff3e0; border-left: 4px solid #ff9800; padding: 14px 16px; border-radius: 6px; margin-bottom: 16px; }
.warning-item { color: #e65100; font-size: 0.9rem; margin-bottom: 6px; display: flex; align-items: flex-start; gap: 8px; }
.warning-item:last-child { margin-bottom: 0; }
.warning-icon { font-size: 1.1rem; flex-shrink: 0; }
.medical-badge-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
.medical-label { color: #666; font-size: 0.9rem; }
.medical-badge { background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; text-transform: capitalize; }
</style>
