<template>
  <div class="recipe-browser">
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
        <h1>&#127859; Recipe Browser</h1>
        <p class="subtitle">Discover healthy and delicious recipes</p>
      </header>

      <!-- Filters -->
      <div class="filters-card">
        <div class="filter-group">
          <label>Diet Type</label>
          <select v-model="filters.diet_type" @change="loadRecipes">
            <option value="">All</option>
            <option value="veg">Vegetarian</option>
            <option value="non-veg">Non-Vegetarian</option>
            <option value="vegan">Vegan</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Meal Type</label>
          <select v-model="filters.meal_type" @change="loadRecipes">
            <option value="">All</option>
            <option value="breakfast">Breakfast</option>
            <option value="lunch">Lunch</option>
            <option value="dinner">Dinner</option>
            <option value="snack">Snack</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Max Calories</label>
          <input type="number" v-model="filters.max_calories" @input="loadRecipes" placeholder="Any" />
        </div>
        <button class="btn-primary" @click="loadSuggestions">&#128257; Get Suggestions</button>
      </div>

      <!-- Recipe Grid -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading recipes...</p>
      </div>

      <div v-else-if="recipes.length === 0" class="empty-state">
        <div class="empty-icon">&#127859;</div>
        <h3>No recipes found</h3>
        <p>Try adjusting your filters or get personalized suggestions</p>
      </div>

      <div v-else class="recipe-grid">
        <div v-for="recipe in recipes" :key="recipe.id" class="recipe-card" @click="viewRecipe(recipe)">
          <div class="recipe-image">
            <span class="recipe-emoji">{{ getRecipeEmoji(recipe.name) }}</span>
            <button class="fav-btn" @click.stop="toggleFavorite(recipe)" :class="{ active: recipe.is_favorite }">
              {{ recipe.is_favorite ? '&#10084;' : '&#9825;' }}
            </button>
          </div>
          <div class="recipe-info">
            <h3>{{ recipe.name }}</h3>
            <p class="recipe-desc">{{ recipe.description || 'Healthy and delicious recipe' }}</p>
            <div class="recipe-meta">
              <span class="meta-item">&#128293; {{ Math.round(recipe.calories) }} kcal</span>
              <span class="meta-item">&#9201; {{ recipe.prep_time + recipe.cook_time }} min</span>
            </div>
            <div class="recipe-macros">
              <span class="macro">P: {{ Math.round(recipe.protein) }}g</span>
              <span class="macro">C: {{ Math.round(recipe.carbs) }}g</span>
              <span class="macro">F: {{ Math.round(recipe.fats) }}g</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recipe Detail Modal -->
      <div v-if="selectedRecipe" class="modal-overlay" @click="selectedRecipe = null">
        <div class="modal-content" @click.stop>
          <button class="close-btn" @click="selectedRecipe = null">&times;</button>
          <h2>{{ selectedRecipe.name }}</h2>
          <p class="modal-desc">{{ selectedRecipe.description }}</p>
          
          <div class="modal-stats">
            <div class="stat-item">
              <span class="stat-value">{{ Math.round(selectedRecipe.calories) }}</span>
              <span class="stat-label">Calories</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ Math.round(selectedRecipe.protein) }}g</span>
              <span class="stat-label">Protein</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ Math.round(selectedRecipe.carbs) }}g</span>
              <span class="stat-label">Carbs</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ Math.round(selectedRecipe.fats) }}g</span>
              <span class="stat-label">Fats</span>
            </div>
          </div>

          <div class="serving-info">
            <span class="serving-label">&#127860; Servings:</span>
            <span class="serving-value">{{ selectedRecipe.servings || 1 }}</span>
            <span class="per-serving-note">(Nutritional values are per serving)</span>
          </div>

          <div class="modal-details">
            <div class="detail-section">
              <h3>&#128203; Ingredients</h3>
              <ul class="ingredient-list">
                <li v-for="(ingredient, idx) in parseIngredients(selectedRecipe.ingredients)" :key="idx">{{ ingredient }}</li>
              </ul>
            </div>
            <div class="detail-section">
              <h3>&#127859; Instructions</h3>
              <ol class="instruction-list">
                <li v-for="(step, idx) in parseInstructions(selectedRecipe.instructions)" :key="idx">{{ step }}</li>
              </ol>
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn-secondary" @click="addToMealPlan(selectedRecipe)">
              &#128197; Add to Meal Plan
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../src/stores/auth'
import { useThemeStore } from '../src/stores/theme'
import api, { getRecipes, getRecipeSuggestions, toggleRecipeFavorite } from '../src/api'

const router = useRouter()
const auth = useAuthStore()
const theme = useThemeStore()

const recipes = ref([])
const loading = ref(false)
const selectedRecipe = ref(null)
const filters = ref({
  diet_type: '',
  meal_type: '',
  max_calories: ''
})

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

const userInitial = computed(() => {
  return auth.user?.name?.charAt(0).toUpperCase() || 'U'
})

const logout = () => {
  auth.logout()
  router.push('/login')
}

const loadRecipes = async () => {
  loading.value = true
  try {
    const response = await getRecipes(filters.value)
    recipes.value = response.data.recipes
  } catch (error) {
    console.error('Failed to load recipes:', error)
  } finally {
    loading.value = false
  }
}

const loadSuggestions = async () => {
  loading.value = true
  try {
    const response = await getRecipeSuggestions()
    recipes.value = response.data.recipes
  } catch (error) {
    console.error('Failed to load suggestions:', error)
  } finally {
    loading.value = false
  }
}

const toggleFavorite = async (recipe) => {
  try {
    const response = await toggleRecipeFavorite(recipe.id)
    recipe.is_favorite = response.data.is_favorite
  } catch (error) {
    console.error('Failed to toggle favorite:', error)
  }
}

const viewRecipe = (recipe) => {
  selectedRecipe.value = recipe
}

const getRecipeEmoji = (name) => {
  const lower = name.toLowerCase()
  if (lower.includes('chicken') || lower.includes('egg')) return '&#129370;'
  if (lower.includes('fish') || lower.includes('salmon')) return '&#128031;'
  if (lower.includes('salad') || lower.includes('vegetable')) return '&#129388;'
  if (lower.includes('rice') || lower.includes('dal')) return '&#127838;'
  if (lower.includes('pasta') || lower.includes('noodle')) return '&#127837;'
  if (lower.includes('smoothie') || lower.includes('juice')) return '&#129387;'
  if (lower.includes('bread') || lower.includes('toast')) return '&#127838;'
  if (lower.includes('fruit') || lower.includes('berry')) return '&#127827;'
  return '&#127859;'
}

const parseIngredients = (ingredients) => {
  if (!ingredients) return []
  return ingredients.split(',').map(i => i.trim()).filter(i => i)
}

const parseInstructions = (instructions) => {
  if (!instructions) return []
  return instructions.split('.').map(i => i.trim()).filter(i => i).map(i => i + '.')
}

const addToMealPlan = async (recipe) => {
  try {
    await api.post('/meals/log', {
      name: recipe.name,
      calories: recipe.calories,
      protein: recipe.protein,
      carbs: recipe.carbs,
      fats: recipe.fats,
      meal_type: recipe.meal_type,
      date: new Date().toISOString().split('T')[0]
    })
    alert('Recipe added to meal plan!')
    selectedRecipe.value = null
  } catch (error) {
    console.error('Failed to add to meal plan:', error)
    alert('Failed to add recipe to meal plan')
  }
}

onMounted(() => {
  loadRecipes()
})
</script>

<style scoped>
.recipe-browser {
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

.filters-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  gap: 20px;
  align-items: flex-end;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a2e;
}

.filter-group select,
.filter-group input {
  padding: 10px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  min-width: 150px;
}

.btn-primary {
  padding: 10px 20px;
  background: #16c79a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #13b386;
}

.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.recipe-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.recipe-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.recipe-image {
  height: 150px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.recipe-emoji {
  font-size: 64px;
}

.fav-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.fav-btn.active {
  color: #e74c3c;
}

.recipe-info {
  padding: 20px;
}

.recipe-info h3 {
  font-size: 18px;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.recipe-desc {
  color: #8b8b9e;
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.4;
}

.recipe-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
}

.meta-item {
  font-size: 13px;
  color: #1a1a2e;
  font-weight: 500;
}

.recipe-macros {
  display: flex;
  gap: 10px;
}

.macro {
  padding: 4px 10px;
  background: #f0f0f0;
  border-radius: 12px;
  font-size: 12px;
  color: #1a1a2e;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 40px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: #8b8b9e;
}

.modal-content h2 {
  font-size: 28px;
  color: #1a1a2e;
  margin-bottom: 10px;
}

.modal-desc {
  color: #8b8b9e;
  margin-bottom: 30px;
}

.modal-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.serving-info {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  padding: 15px 20px;
  border-radius: 10px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-left: 4px solid #0ea5e9;
}

.serving-label {
  font-size: 16px;
  font-weight: 600;
  color: #0369a1;
}

.serving-value {
  font-size: 20px;
  font-weight: bold;
  color: #0ea5e9;
}

.per-serving-note {
  font-size: 13px;
  color: #64748b;
  font-style: italic;
  margin-left: auto;
}

.stat-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 12px;
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #16c79a;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #8b8b9e;
  margin-top: 5px;
}

.modal-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.detail-section h3 {
  font-size: 20px;
  color: #1a1a2e;
  margin-bottom: 15px;
}

.ingredient-list,
.instruction-list {
  padding-left: 0;
  list-style: none;
}

.ingredient-list li,
.instruction-list li {
  margin-bottom: 12px;
  color: #1a1a2e;
  line-height: 1.5;
  padding: 10px 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #16c79a;
}

.ingredient-list li {
  font-weight: 500;
  position: relative;
  padding-left: 35px;
}

.ingredient-list li::before {
  content: '✓';
  position: absolute;
  left: 12px;
  color: #16c79a;
  font-weight: bold;
  font-size: 16px;
}

.modal-actions {
  display: flex;
  gap: 10px;
}

.btn-secondary {
  padding: 12px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-secondary:hover {
  background: #5568d3;
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
  
  .filters-card {
    flex-direction: column;
  }
  
  .recipe-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .modal-details {
    grid-template-columns: 1fr;
  }
}
</style>
