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
  font-family: 'Segoe UI', Arial, sans-serif;
  background: var(--bg-body);
  min-height: 100vh;
  transition: background var(--transition-slow);
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
h2 { color: var(--text-primary); margin: 0; transition: color var(--transition-slow); }
button {
  padding: 10px 20px;
  background: var(--text-primary);
  color: var(--bg-card);
  border: none;
  border-radius: var(--radius-sm);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}
button:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.summary-bar {
  display: flex;
  gap: 16px;
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  padding: 16px;
  border-radius: var(--radius-sm);
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.summary-item { flex: 1; text-align: center; min-width: 100px; }
.summary-item .label { display: block; color: #166534; font-size: 0.8rem; }
.summary-item .value { display: block; font-size: 1.2rem; font-weight: bold; color: #166534; }
.meals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.meal-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  border-left: 4px solid #22c55e;
  transition: all var(--transition-slow);
}
.meal-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.meal-card.breakfast { border-left-color: #f59e0b; }
.meal-card.lunch { border-left-color: #22c55e; }
.meal-card.dinner { border-left-color: #3b82f6; }
.meal-card.snack { border-left-color: #a855f7; }
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
.breakfast .meal-type-badge { background: #f59e0b; }
.lunch .meal-type-badge { background: #22c55e; }
.dinner .meal-type-badge { background: #3b82f6; }
.snack .meal-type-badge { background: #a855f7; }
h3 { margin: 0 0 8px 0; color: var(--text-primary); font-size: 1.05rem; transition: color var(--transition-slow); }
.macros { display: flex; gap: 12px; flex-wrap: wrap; color: var(--text-secondary); font-size: 0.85rem; transition: color var(--transition-slow); }
.empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
.safety-banner { background: #fff7ed; border-left: 4px solid #f97316; padding: 14px 16px; border-radius: 6px; margin-bottom: 16px; }
.warning-item { color: #c2410c; font-size: 0.9rem; margin-bottom: 6px; display: flex; align-items: flex-start; gap: 8px; }
.warning-item:last-child { margin-bottom: 0; }
.warning-icon { font-size: 1.1rem; flex-shrink: 0; }
.medical-badge-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
.medical-label { color: var(--text-secondary); font-size: 0.9rem; transition: color var(--transition-slow); }
.medical-badge { background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; text-transform: capitalize; }
</style>
