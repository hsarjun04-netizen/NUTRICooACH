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
              <input 
                v-model="mealForm.name" 
                type="text" 
                placeholder="e.g., Grilled Chicken Salad" 
                required 
                @input="autoFillNutrition"
                list="food-suggestions"
              />
              <datalist id="food-suggestions">
                <option v-for="food in foodSuggestions" :key="food.name" :value="food.name"></option>
              </datalist>
              <div v-if="showAutoFillBadge" class="auto-fill-badge">
                <span class="badge-icon">&#10003;</span> Auto-filled
              </div>
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
            <div class="form-group small">
              <label>Servings</label>
              <input v-model.number="mealForm.servings" type="number" placeholder="1" min="0.5" step="0.5" @input="autoFillNutrition" />
            </div>
          </div>
          <div class="form-row macros">
            <div class="form-group">
              <label>Calories</label>
              <input v-model.number="mealForm.calories" type="number" placeholder="Auto" min="0" :class="{ 'auto-filled': showAutoFillBadge }" />
            </div>
            <div class="form-group">
              <label>Protein (g)</label>
              <input v-model.number="mealForm.protein" type="number" placeholder="Auto" min="0" :class="{ 'auto-filled': showAutoFillBadge }" />
            </div>
            <div class="form-group">
              <label>Carbs (g)</label>
              <input v-model.number="mealForm.carbs" type="number" placeholder="Auto" min="0" :class="{ 'auto-filled': showAutoFillBadge }" />
            </div>
            <div class="form-group">
              <label>Fats (g)</label>
              <input v-model.number="mealForm.fats" type="number" placeholder="Auto" min="0" :class="{ 'auto-filled': showAutoFillBadge }" />
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
              <span class="meal-type-badge">{{ capitalize(meal.meal_type) }}</span>
              <span class="meal-calories">{{ meal.calories }} kcal</span>
            </div>
            <div class="meal-name">{{ meal.name }}</div>
            <div v-if="meal.servings" class="meal-servings">
              <span class="servings-icon">&#127860;</span>
              <span class="servings-text">{{ meal.servings }} serving{{ meal.servings > 1 ? 's' : '' }}</span>
            </div>
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
        meal_type: 'breakfast',
        servings: 1
      },
      weightForm: { weight: null },
      saving: false,
      savingWeight: false,
      showAutoFillBadge: false,
      foodDatabase: [
        // Breakfast items
        { name: 'Oatmeal with Berries', calories: 350, protein: 12, carbs: 58, fats: 8 },
        { name: 'Vegetable Omelette', calories: 280, protein: 18, carbs: 8, fats: 20 },
        { name: 'Greek Yogurt Parfait', calories: 320, protein: 20, carbs: 45, fats: 8 },
        { name: 'Chicken Breakfast Burrito', calories: 450, protein: 35, carbs: 42, fats: 15 },
        { name: 'Smoothie Bowl', calories: 380, protein: 15, carbs: 62, fats: 10 },
        { name: 'Pancakes', calories: 350, protein: 8, carbs: 52, fats: 12 },
        { name: 'Scrambled Eggs', calories: 220, protein: 14, carbs: 2, fats: 18 },
        { name: 'Toast with Butter', calories: 180, protein: 4, carbs: 22, fats: 9 },
        { name: 'Cereal with Milk', calories: 250, protein: 8, carbs: 45, fats: 5 },
        { name: 'Bagel with Cream Cheese', calories: 330, protein: 10, carbs: 48, fats: 11 },
        
        // Lunch items
        { name: 'Grilled Chicken Salad', calories: 420, protein: 35, carbs: 18, fats: 22 },
        { name: 'Quinoa Buddha Bowl', calories: 480, protein: 18, carbs: 65, fats: 16 },
        { name: 'Turkey Wrap', calories: 380, protein: 28, carbs: 42, fats: 12 },
        { name: 'Paneer Tikka Masala', calories: 520, protein: 25, carbs: 35, fats: 30 },
        { name: 'Salmon Rice Bowl', calories: 550, protein: 40, carbs: 55, fats: 18 },
        { name: 'Chicken Sandwich', calories: 450, protein: 30, carbs: 45, fats: 16 },
        { name: 'Caesar Salad', calories: 320, protein: 22, carbs: 15, fats: 20 },
        { name: 'Pasta with Marinara', calories: 480, protein: 16, carbs: 72, fats: 14 },
        { name: 'Veggie Burger', calories: 390, protein: 18, carbs: 48, fats: 15 },
        { name: 'Chicken Soup', calories: 280, protein: 24, carbs: 28, fats: 8 },
        
        // Dinner items
        { name: 'Grilled Chicken with Vegetables', calories: 450, protein: 42, carbs: 28, fats: 18 },
        { name: 'Vegetable Stir Fry with Tofu', calories: 380, protein: 22, carbs: 35, fats: 16 },
        { name: 'Fish Curry with Rice', calories: 520, protein: 38, carbs: 48, fats: 20 },
        { name: 'Lentil Dal with Roti', calories: 420, protein: 20, carbs: 68, fats: 8 },
        { name: 'Egg Fried Rice', calories: 450, protein: 18, carbs: 62, fats: 14 },
        { name: 'Steak with Potatoes', calories: 620, protein: 45, carbs: 42, fats: 28 },
        { name: 'Spaghetti Bolognese', calories: 550, protein: 28, carbs: 68, fats: 18 },
        { name: 'Grilled Fish with Salad', calories: 380, protein: 36, carbs: 12, fats: 20 },
        { name: 'Chicken Curry with Rice', calories: 580, protein: 35, carbs: 65, fats: 22 },
        { name: 'Tacos', calories: 460, protein: 26, carbs: 42, fats: 20 },
        
        // Snacks
        { name: 'Trail Mix', calories: 250, protein: 8, carbs: 28, fats: 14 },
        { name: 'Hummus with Vegetables', calories: 180, protein: 6, carbs: 22, fats: 8 },
        { name: 'Protein Energy Balls', calories: 150, protein: 10, carbs: 18, fats: 6 },
        { name: 'Fruit Smoothie', calories: 220, protein: 12, carbs: 38, fats: 3 },
        { name: 'Roasted Chickpeas', calories: 180, protein: 10, carbs: 28, fats: 4 },
        { name: 'Apple with Peanut Butter', calories: 200, protein: 6, carbs: 24, fats: 10 },
        { name: 'Granola Bar', calories: 190, protein: 5, carbs: 28, fats: 7 },
        { name: 'Cheese and Crackers', calories: 220, protein: 8, carbs: 20, fats: 12 },
        { name: 'Mixed Nuts', calories: 210, protein: 7, carbs: 9, fats: 18 },
        { name: 'Banana', calories: 105, protein: 1, carbs: 27, fats: 0 },
        
        // Common items
        { name: 'Chicken Breast', calories: 165, protein: 31, carbs: 0, fats: 3.6 },
        { name: 'Brown Rice', calories: 216, protein: 5, carbs: 45, fats: 1.8 },
        { name: 'Broccoli', calories: 55, protein: 3.7, carbs: 11, fats: 0.6 },
        { name: 'Sweet Potato', calories: 103, protein: 2.3, carbs: 24, fats: 0.1 },
        { name: 'Salmon', calories: 208, protein: 20, carbs: 0, fats: 13 },
        { name: 'Egg', calories: 78, protein: 6, carbs: 0.6, fats: 5 },
        { name: 'Avocado', calories: 160, protein: 2, carbs: 9, fats: 15 },
        { name: 'Almonds', calories: 164, protein: 6, carbs: 6, fats: 14 },
        { name: 'Banana', calories: 105, protein: 1.3, carbs: 27, fats: 0.4 },
        { name: 'Apple', calories: 95, protein: 0.5, carbs: 25, fats: 0.3 }
      ]
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
    },
    foodSuggestions() {
      if (!this.mealForm.name || this.mealForm.name.length < 2) {
        return this.foodDatabase
      }
      const search = this.mealForm.name.toLowerCase()
      return this.foodDatabase.filter(food => 
        food.name.toLowerCase().includes(search)
      ).slice(0, 10)
    }
  },
  mounted() {
    this.loadMeals()
  },
  methods: {
    capitalize(type) {
      return type ? type.charAt(0).toUpperCase() + type.slice(1) : ''
    },
    autoFillNutrition() {
      if (!this.mealForm.name || this.mealForm.name.length < 2) {
        return
      }
      
      const search = this.mealForm.name.toLowerCase()
      const matchedFood = this.foodDatabase.find(food => 
        food.name.toLowerCase() === search || 
        food.name.toLowerCase().includes(search)
      )
      
      if (matchedFood) {
        const servings = this.mealForm.servings || 1
        this.mealForm.calories = Math.round(matchedFood.calories * servings)
        this.mealForm.protein = Math.round(matchedFood.protein * servings * 10) / 10
        this.mealForm.carbs = Math.round(matchedFood.carbs * servings * 10) / 10
        this.mealForm.fats = Math.round(matchedFood.fats * servings * 10) / 10
        
        // Show auto-fill badge
        this.showAutoFillBadge = true
        setTimeout(() => {
          this.showAutoFillBadge = false
        }, 2000)
      }
    },
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
        this.mealForm = { name: '', calories: null, protein: null, carbs: null, fats: null, meal_type: 'breakfast', servings: 1 }
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
.tracker-page { max-width: 800px; margin: 0 auto; padding: 32px 20px; font-family: 'Segoe UI', Arial, sans-serif; background: var(--bg-body); min-height: 100vh; transition: background var(--transition-slow); }
.tracker-container { display: flex; flex-direction: column; gap: 20px; }
.page-header { margin-bottom: 4px; }
.page-header h1 { margin: 0; font-size: 1.5rem; color: var(--text-primary); transition: color var(--transition-slow); }
.subtitle { margin: 4px 0 0 0; color: var(--text-muted); font-size: 0.9rem; transition: color var(--transition-slow); }

.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-slow);
}
.card:hover { box-shadow: var(--shadow-md); }
.card h3 { margin: 0 0 16px 0; font-size: 1rem; color: var(--text-primary); transition: color var(--transition-slow); }

.form-row { display: flex; gap: 14px; margin-bottom: 14px; }
.form-row .form-group { flex: 1; }
.form-row .form-group.small { flex: 0.4; }
.form-group { position: relative; }
.form-group label { display: block; margin-bottom: 5px; font-size: 0.8rem; color: var(--text-secondary); font-weight: 500; transition: color var(--transition-slow); }
.form-group input, .form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.95rem;
  box-sizing: border-box;
  background: var(--bg-input);
  color: var(--text-primary);
  transition: all var(--transition-base);
}
.form-group input:focus, .form-group select:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(163, 230, 53, 0.15); background: var(--bg-input); }
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
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
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

.submit-btn {
  width: 100%;
  padding: 12px;
  background: var(--text-primary);
  color: var(--bg-card);
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 4px;
  transition: all var(--transition-base);
}
.submit-btn:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.summary-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
.summary-item {
  background: var(--bg-card);
  border-radius: 14px;
  padding: 18px;
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-slow);
}
.summary-value { display: block; font-size: 1.4rem; font-weight: 700; color: var(--text-primary); transition: color var(--transition-slow); }
.summary-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; transition: color var(--transition-slow); }

.meals-section h3 { margin: 8px 0 14px 0; font-size: 1rem; color: var(--text-primary); transition: color var(--transition-slow); }
.meals-grid { display: flex; flex-direction: column; gap: 12px; }
.meal-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 18px;
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--border-color);
  transition: all var(--transition-slow);
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
  color: var(--text-muted);
  letter-spacing: 0.5px;
  transition: color var(--transition-slow);
}
.meal-calories { font-size: 0.85rem; font-weight: 700; color: #22c55e; }
.meal-name { font-size: 1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 8px; transition: color var(--transition-slow); }
.meal-servings {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
  padding: 6px 10px;
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-radius: 6px;
  width: fit-content;
}
.servings-icon { font-size: 16px; }
.servings-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #0369a1;
}
.meal-macros { display: flex; gap: 16px; }
.meal-macros span { font-size: 0.8rem; color: var(--text-muted); transition: color var(--transition-slow); }

.empty-state { text-align: center; padding: 30px; color: var(--text-muted); font-size: 0.9rem; }

.weight-card .weight-row { display: flex; gap: 12px; }
.weight-card input { flex: 1; padding: 10px 12px; border: 1px solid var(--border-color); border-radius: 8px; font-size: 0.95rem; background: var(--bg-input); color: var(--text-primary); }
.weight-card button {
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}
.weight-card button:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.weight-card button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

@media (max-width: 600px) {
  .form-row { flex-direction: column; gap: 10px; }
  .form-row.macros { display: grid; grid-template-columns: 1fr 1fr; }
  .summary-bar { grid-template-columns: 1fr 1fr; }
}
</style>
